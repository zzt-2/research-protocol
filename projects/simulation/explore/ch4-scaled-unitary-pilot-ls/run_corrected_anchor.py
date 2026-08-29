"""T085 fixed A2 bridge runner over one shared set of production latents."""

from __future__ import annotations

import argparse
import hashlib
import inspect
import json
import os
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import production_core as core


SEAM = Path(__file__).resolve().parent
SIM_ROOT = SEAM.parents[1]
MANIFEST_PATH = SEAM / "corrected_anchor_manifest.json"
RAW_PATH = SEAM / "corrected_anchor_raw.json"
CHECKPOINT_PATH = SEAM / "corrected_anchor_checkpoint.json"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _manifest_hash() -> str:
    return file_sha256(MANIFEST_PATH)


def _code_path(relative: str) -> Path:
    return SIM_ROOT / relative if relative.startswith("common/") else SEAM / relative


def verify_authority(manifest: dict) -> None:
    required = {
        "schema_version": "t085.corrected-anchor.v1",
        "authority": "T085/D064/V039",
        "action_class": "CH4_PRODUCTION_SEAM_BRIDGE",
        "mission_checkpoint": "CP026",
        "control_epoch": 26,
        "payload_symbols_per_polarization": 4096,
        "max_pilots": 4,
    }
    for key, expected in required.items():
        if manifest.get(key) != expected:
            raise RuntimeError(f"manifest authority mismatch: {key}")
    expected_cells = [(14.0, 2), (14.0, 4), (18.0, 2), (18.0, 4)]
    actual_cells = [
        (float(c["snr_db"]), int(c["pilot_symbols_per_polarization"]))
        for c in manifest.get("cells", [])
    ]
    if actual_cells != expected_cells:
        raise RuntimeError("manifest cell grid changed")
    population = manifest.get("population", {})
    if population != {
        "windows_per_cell": 64,
        "canonical_latent_ids": {"start": 20000, "stop_inclusive": 20063},
        "smoke_latent_id": 19999,
        "shared_across_cells": True,
    }:
        raise RuntimeError("manifest population changed")
    if list(manifest.get("arms", {})) != ["B0", "B2", "B3_PSC", "C4", "O1"]:
        raise RuntimeError("manifest arm order changed")
    expected_arms = {
        "B0": {"parameter": None, "access": "receiver-visible"},
        "B2": {"parameter": 1.0, "access": "receiver-visible"},
        "B3_PSC": {"parameter": 1.0, "access": "receiver-visible pilots only"},
        "C4": {"parameter": None, "access": "receiver-visible"},
        "O1": {"parameter": None, "access": "truth-only runner path; never receiver_action"},
    }
    if manifest.get("arms") != expected_arms:
        raise RuntimeError("manifest arm contract changed")
    expected_bootstrap = {
        "rng": "PCG64",
        "seed": 2026083006,
        "resamples": 5000,
        "confidence": 0.95,
        "stream_rule": "reset seed for each named paired comparison",
        "pooled_np2_cluster": "64 latent IDs; each resample carries both 14 and 18 dB rows",
    }
    if manifest.get("bootstrap") != expected_bootstrap:
        raise RuntimeError("manifest bootstrap contract changed")
    expected_code_keys = {"production_core.py", "common/_modulation.py", "scaled_unitary.py"}
    if set(manifest.get("code_hashes", {})) != expected_code_keys:
        raise RuntimeError("manifest code hash key set changed")
    for relative, expected in manifest.get("code_hashes", {}).items():
        if file_sha256(_code_path(relative)) != expected:
            raise RuntimeError(f"frozen code hash changed: {relative}")
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=SEAM, capture_output=True, text=True, check=True
    ).stdout.strip()
    if commit != manifest.get("base_commit"):
        raise RuntimeError("base commit changed")
    snapshot = core.make_latent_window("moderate", 19999, 1, 4)["turbulence"]
    scene = manifest.get("scene", {})
    for key in ("name", "alpha", "beta", "authority"):
        source_key = "scenario" if key == "name" else key
        if scene.get(key) != snapshot.get(source_key):
            raise RuntimeError(f"turbulence authority mismatch: {key}")


def truth_firewall_passes() -> bool:
    signature = tuple(inspect.signature(core.receiver_action).parameters)
    source = inspect.getsource(core.receiver_action).lower()
    return signature == ("arm", "x_pilots", "y_pilots", "y_payload", "parameter") and not any(
        token in source for token in ("h_true", "bits", "decision", "truth")
    )


def _hash_action(action: dict) -> str:
    digest = hashlib.sha256()
    for key in ("z", "h_hat", "w"):
        value = np.ascontiguousarray(action[key], dtype=np.complex128)
        digest.update(key.encode("ascii"))
        digest.update(value.tobytes())
    return digest.hexdigest()


def _oracle_action(y_payload: np.ndarray, h_true: np.ndarray) -> dict:
    """Truth-only O1 path; deliberately separate from deployable receiver_action."""
    channel = np.asarray(h_true, dtype=np.complex128)
    payload = np.asarray(y_payload, dtype=np.complex128)
    if channel.shape != (2, 2) or payload.ndim != 2 or payload.shape[0] != 2:
        raise core.InvalidEstimate("invalid oracle input")
    if not (np.all(np.isfinite(channel)) and np.all(np.isfinite(payload))):
        raise core.InvalidEstimate("nonfinite oracle input")
    try:
        inverse = np.linalg.inv(channel)
        singular = np.linalg.svd(channel, compute_uv=False)
    except np.linalg.LinAlgError as error:
        raise core.InvalidEstimate("oracle inversion failed") from error
    return {
        "arm": "O1",
        "z": inverse @ payload,
        "h_hat": channel.copy(),
        "w": inverse,
        "rho": float(singular[0] / singular[1]),
        "singular_values": singular,
        "scale": float(np.mean(singular)),
        "psc_scale": 1.0,
    }


def _build_latent_record(manifest: dict, latent_id: int) -> dict:
    latent = core.make_latent_window(
        manifest["scene"]["name"], latent_id,
        manifest["payload_symbols_per_polarization"], manifest["max_pilots"],
    )
    cells = []
    for cell in manifest["cells"]:
        observation = core.observe_latent(
            latent, cell["snr_db"], cell["pilot_symbols_per_polarization"]
        )
        rows = []
        for arm, arm_contract in manifest["arms"].items():
            parameter = arm_contract["parameter"]
            started = time.perf_counter_ns()
            if arm == "O1":
                action = _oracle_action(observation["y_payload"], latent["h_true"])
            else:
                action = core.receiver_action(
                    arm, observation["x_pilots"], observation["y_pilots"],
                    observation["y_payload"], parameter,
                )
            runtime_ns = time.perf_counter_ns() - started
            metrics = core.score_action(action, latent["bits"], latent["h_true"])
            rows.append({
                "arm": arm,
                "parameter": parameter,
                "metrics": metrics,
                "public_scale": action.get("scale"),
                "psc_scale": float(action.get("psc_scale", 1.0)),
                "validity": "VALID",
                "action_sha256": _hash_action(action),
                "runtime_ns": int(runtime_ns),
            })
        cells.append({
            "cell_id": cell["cell_id"],
            "snr_db": float(cell["snr_db"]),
            "pilot_symbols_per_polarization": int(cell["pilot_symbols_per_polarization"]),
            "observation_hashes": observation["observation_hashes"],
            "rows": rows,
        })
    return {
        "latent_id": int(latent_id),
        "rng_namespace": latent["rng_namespace"],
        "latent_hashes": latent["latent_hashes"],
        "turbulence": latent["turbulence"],
        "cells": cells,
    }


def _binding(manifest: dict, purpose: str, latent_ids: list[int]) -> dict:
    return {
        "manifest_sha256": _manifest_hash(),
        "base_commit": manifest["base_commit"],
        "code_hashes": manifest["code_hashes"],
        "runner_sha256": file_sha256(Path(__file__)),
        "purpose": purpose,
        "latent_ids": latent_ids,
    }


def _write_checkpoint(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, indent=2), encoding="utf-8")
    os.replace(temporary, path)


def _scientific_record(record: dict) -> dict:
    """Return the deterministic record content, excluding diagnostic runtime."""
    normalized = json.loads(json.dumps(record))
    for cell in normalized.get("cells", []):
        for row in cell.get("rows", []):
            row.pop("runtime_ns", None)
    return normalized


def build_raw(
    manifest: dict,
    latent_ids: list[int],
    *,
    purpose: str,
    checkpoint_path: Path,
    retain_checkpoint: bool = False,
) -> dict:
    verify_authority(manifest)
    identifiers = [int(value) for value in latent_ids]
    canonical = list(range(20000, 20064))
    if purpose == "a2_bridge_non_thesis":
        if identifiers != canonical:
            raise RuntimeError("canonical latent IDs changed")
    elif purpose == "smoke_non_thesis":
        if identifiers != [19999]:
            raise RuntimeError("smoke latent ID changed")
    else:
        raise RuntimeError("unregistered bridge purpose")
    binding = _binding(manifest, purpose, identifiers)
    if checkpoint_path.exists():
        checkpoint = load_json(checkpoint_path)
        if checkpoint.get("binding") != binding:
            raise RuntimeError("checkpoint binding mismatch")
        records = checkpoint.get("latents")
        if not isinstance(records, list):
            raise RuntimeError("checkpoint records invalid")
    else:
        records = []
    completed = [int(record["latent_id"]) for record in records]
    if len(completed) != len(set(completed)) or any(value not in identifiers for value in completed):
        raise RuntimeError("checkpoint latent census invalid")
    for record in records:
        latent_id = int(record["latent_id"])
        expected_record = _build_latent_record(manifest, latent_id)
        if _scientific_record(record) != _scientific_record(expected_record):
            raise RuntimeError(f"checkpoint record mismatch: latent {latent_id}")
    for latent_id in identifiers:
        if latent_id in completed:
            continue
        records.append(_build_latent_record(manifest, latent_id))
        completed.append(latent_id)
        _write_checkpoint(checkpoint_path, {"binding": binding, "latents": records})
        print(f"latent {latent_id}: {len(records)}/{len(identifiers)}")
    records.sort(key=lambda item: int(item["latent_id"]))
    if [int(item["latent_id"]) for item in records] != identifiers:
        raise RuntimeError("completed latent census invalid")
    raw = {
        "schema_version": "t085.corrected-anchor-raw.v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": purpose,
        "authority": manifest["authority"],
        "base_commit": manifest["base_commit"],
        "control_epoch": manifest["control_epoch"],
        "mission_checkpoint": manifest["mission_checkpoint"],
        "manifest_sha256": _manifest_hash(),
        "code_hashes": manifest["code_hashes"],
        "scene": manifest["scene"],
        "cells": manifest["cells"],
        "payload_symbols_per_polarization": manifest["payload_symbols_per_polarization"],
        "max_pilots": manifest["max_pilots"],
        "truth_firewall": "O1_SEPARATE_TRUTH_ONLY_PATH",
        "latents": records,
    }
    if not retain_checkpoint and checkpoint_path.exists():
        checkpoint_path.unlink()
    return raw


def _atomic_save(raw: dict, target: Path, script_name: str) -> None:
    from projects.simulation.common import save_results

    temporary = target.with_suffix(target.suffix + ".tmp")
    save_results(raw, str(temporary), script_name)
    os.replace(temporary, target)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    manifest = load_json(MANIFEST_PATH)
    if not truth_firewall_passes():
        raise RuntimeError("deployable receiver truth firewall failed")
    if args.smoke:
        if args.output_dir is None:
            raise SystemExit("--smoke requires --output-dir")
        target = args.output_dir.resolve() / "corrected_anchor_smoke_raw.json"
        checkpoint = args.output_dir.resolve() / "corrected_anchor_smoke_checkpoint.json"
        raw = build_raw(manifest, [19999], purpose="smoke_non_thesis", checkpoint_path=checkpoint)
        _atomic_save(raw, target, "t085_corrected_anchor_one_latent_smoke_non_thesis")
        print(f"SMOKE_STRUCTURAL_PASS {target}")
        return 0
    if args.output_dir is not None:
        raise SystemExit("canonical run does not accept --output-dir")
    if RAW_PATH.exists():
        raise RuntimeError("canonical raw already exists; refusing rerun")
    raw = build_raw(
        manifest, list(range(20000, 20064)), purpose="a2_bridge_non_thesis",
        checkpoint_path=CHECKPOINT_PATH,
    )
    _atomic_save(raw, RAW_PATH, "t085_corrected_anchor_fixed_a2_bridge_raw")
    print("CANONICAL_4X64_COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
