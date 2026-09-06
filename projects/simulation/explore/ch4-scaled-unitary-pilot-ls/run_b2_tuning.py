"""T086 disjoint B2 development-tuning runner."""

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
REPO_ROOT = SEAM.parents[3]
MANIFEST_PATH = SEAM / "b2_tuning_manifest.json"
RAW_PATH = SEAM / "b2_tuning_raw.json"
CHECKPOINT_PATH = SEAM / "b2_tuning_checkpoint.json"
PARAMS_PATH = SIM_ROOT / "params.py"
FROZEN_MANIFEST_SHA256 = "e35c418d176904b4048fe1b83fe22865e01223f51017953a6443776b8a6a312a"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _code_path(relative: str) -> Path:
    return SIM_ROOT / relative if relative.startswith("common/") else SEAM / relative


def _git_head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=SEAM,
        capture_output=True, text=True, check=True,
    ).stdout.strip()


def verify_authority(manifest: dict) -> None:
    if file_sha256(MANIFEST_PATH) != FROZEN_MANIFEST_SHA256:
        raise RuntimeError("frozen tuning manifest file changed")
    if manifest != load_json(MANIFEST_PATH):
        raise RuntimeError("supplied tuning manifest differs from the frozen file")
    required = {
        "schema_version": "t086.b2-tuning-manifest.v1",
        "authority": "T086/D065/V040",
        "action_class": "CH4_DIRECTION_SCALE_FAMILY_FREEZE",
        "mission_checkpoint": "CP027",
        "control_epoch": 27,
        "base_commit": "d3d98c6fc92642e4d6b964d086c1f3bea2018d1d",
    }
    for key, expected in required.items():
        if manifest.get(key) != expected:
            raise RuntimeError(f"manifest authority mismatch: {key}")
    expected_grid = {
        "scenes": ["weak", "moderate", "strong"],
        "pilot_symbols_per_polarization": [2, 4, 8, 16],
        "snr_db": [15.0, 25.0, 35.0],
        "tau_candidates": [0.0, 0.25, 0.5, 0.75, 1.0],
        "windows_per_scene": 32,
        "payload_symbols_per_polarization": 4096,
        "max_pilots": 16,
    }
    if manifest.get("grid") != expected_grid:
        raise RuntimeError("manifest tuning grid changed")
    if _git_head() != manifest["base_commit"]:
        raise RuntimeError("base commit changed")
    expected_code_keys = {"production_core.py", "common/_modulation.py", "scaled_unitary.py"}
    hashes = manifest.get("code_hashes")
    if not isinstance(hashes, dict) or set(hashes) != expected_code_keys:
        raise RuntimeError("frozen code hash key set changed")
    for relative, expected in hashes.items():
        if file_sha256(_code_path(relative)) != expected:
            raise RuntimeError(f"frozen code hash changed: {relative}")
    expected_t085 = {
        "manifest_sha256": SEAM / "corrected_anchor_manifest.json",
        "raw_sha256": SEAM / "corrected_anchor_raw.json",
        "receipt_sha256": SEAM / "corrected_anchor_receipt.json",
    }
    for field, path in expected_t085.items():
        if file_sha256(path) != manifest.get("t085_bindings", {}).get(field):
            raise RuntimeError(f"T085 binding mismatch: {field}")
    if manifest["t085_bindings"].get("terminal") != "CHEAP_COMPARATOR_NOT_CLEARED":
        raise RuntimeError("T085 terminal changed")
    for scene, expected in manifest.get("resolved_scenes", {}).items():
        snapshot = core._resolved_turbulence(scene)
        if (snapshot["alpha"], snapshot["beta"]) != (expected.get("alpha"), expected.get("beta")):
            raise RuntimeError(f"turbulence runtime snapshot changed: {scene}")


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


def checkpoint_binding(manifest: dict, purpose: str, latent_ids: list[int]) -> dict:
    verify_authority(manifest)
    identifiers = [int(value) for value in latent_ids]
    if purpose == "canonical_tuning_non_thesis":
        if identifiers != list(range(21000, 21032)):
            raise RuntimeError("canonical tuning IDs changed")
    elif purpose == "tuning_preflight_smoke_non_thesis":
        if identifiers != [20999]:
            raise RuntimeError("tuning smoke IDs changed")
    else:
        raise RuntimeError("unregistered tuning purpose")
    return {
        "authority": manifest["authority"],
        "base_commit": manifest["base_commit"],
        "purpose": purpose,
        "latent_ids": identifiers,
        "frozen_hashes": {
            "manifest": file_sha256(MANIFEST_PATH),
            "runner": file_sha256(Path(__file__)),
            **manifest["code_hashes"],
            "projects/simulation/params.py": file_sha256(PARAMS_PATH),
        },
        "resolved_scenes": manifest["resolved_scenes"],
        "turbulence_authority": manifest["turbulence_authority"],
    }


def _build_latent_record(manifest: dict, scene: str, latent_id: int) -> dict:
    grid = manifest["grid"]
    latent = core.make_latent_window(
        scene, latent_id, grid["payload_symbols_per_polarization"], grid["max_pilots"]
    )
    cells = []
    for n_pilots in grid["pilot_symbols_per_polarization"]:
        for snr_db in grid["snr_db"]:
            observation = core.observe_latent(latent, snr_db, n_pilots)
            rows = []
            arms = [
                *(('B2_TUNED_CANDIDATE', 'B2', float(tau)) for tau in grid["tau_candidates"]),
                ("C4_FWD", "C4", None),
                ("B3_PSC", "B3_PSC", 1.0),
            ]
            for public_role, runtime_arm, parameter in arms:
                started = time.perf_counter_ns()
                action = core.receiver_action(
                    runtime_arm, observation["x_pilots"], observation["y_pilots"],
                    observation["y_payload"], parameter,
                )
                runtime_ns = time.perf_counter_ns() - started
                metrics = core.score_action(action, latent["bits"], latent["h_true"])
                rows.append({
                    "public_role": public_role,
                    "runtime_arm": runtime_arm,
                    "parameter": parameter,
                    "metrics": metrics,
                    "validity": "VALID",
                    "action_sha256": _hash_action(action),
                    "runtime_ns": int(runtime_ns),
                })
            cells.append({
                "cell_id": f"{scene}_np{n_pilots}_snr{int(snr_db)}",
                "scene": scene,
                "snr_db": float(snr_db),
                "pilot_symbols_per_polarization": int(n_pilots),
                "observation_hashes": observation["observation_hashes"],
                "rows": rows,
            })
    return {
        "scene": scene,
        "latent_id": int(latent_id),
        "rng_namespace": latent["rng_namespace"],
        "latent_hashes": latent["latent_hashes"],
        "turbulence": latent["turbulence"],
        "cells": cells,
    }


def _scientific_record(record: dict) -> dict:
    normalized = json.loads(json.dumps(record))
    for cell in normalized.get("cells", []):
        for row in cell.get("rows", []):
            row.pop("runtime_ns", None)
    return normalized


def _write_checkpoint(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, indent=2), encoding="utf-8")
    os.replace(temporary, path)


def build_raw(
    manifest: dict,
    latent_ids: list[int],
    *,
    purpose: str,
    checkpoint_path: Path,
    retain_checkpoint: bool = False,
) -> dict:
    binding = checkpoint_binding(manifest, purpose, latent_ids)
    identifiers = binding["latent_ids"]
    if checkpoint_path.exists():
        checkpoint = load_json(checkpoint_path)
        if checkpoint.get("binding") != binding:
            raise RuntimeError("CH4_FAMILY_FREEZE_INVALID: checkpoint binding mismatch")
        records = checkpoint.get("latents")
        if not isinstance(records, list):
            raise RuntimeError("CH4_FAMILY_FREEZE_INVALID: checkpoint records invalid")
    else:
        records = []
    expected_keys = [(scene, latent_id) for scene in manifest["grid"]["scenes"] for latent_id in identifiers]
    completed = [(record.get("scene"), int(record.get("latent_id"))) for record in records]
    if len(completed) != len(set(completed)) or any(key not in expected_keys for key in completed):
        raise RuntimeError("CH4_FAMILY_FREEZE_INVALID: checkpoint census invalid")
    for record in records:
        key = (record["scene"], int(record["latent_id"]))
        rebuilt = _build_latent_record(manifest, *key)
        if _scientific_record(record) != _scientific_record(rebuilt):
            raise RuntimeError(f"CH4_FAMILY_FREEZE_INVALID: checkpoint record mismatch {key}")
    for scene, latent_id in expected_keys:
        if (scene, latent_id) in completed:
            continue
        records.append(_build_latent_record(manifest, scene, latent_id))
        completed.append((scene, latent_id))
        _write_checkpoint(checkpoint_path, {"binding": binding, "latents": records})
        print(f"{scene} latent {latent_id}: {len(records)}/{len(expected_keys)}")
    records.sort(key=lambda item: (manifest["grid"]["scenes"].index(item["scene"]), int(item["latent_id"])))
    observed_keys = [(record["scene"], int(record["latent_id"])) for record in records]
    if observed_keys != expected_keys:
        raise RuntimeError("CH4_FAMILY_FREEZE_INVALID: completed latent census invalid")
    raw = {
        "schema_version": "t086.b2-tuning-raw.v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": purpose,
        "authority": manifest["authority"],
        "base_commit": manifest["base_commit"],
        "control_epoch": manifest["control_epoch"],
        "mission_checkpoint": manifest["mission_checkpoint"],
        "manifest_sha256": file_sha256(MANIFEST_PATH),
        "runner_sha256": file_sha256(Path(__file__)),
        "code_hashes": manifest["code_hashes"],
        "params_authority": {
            "path": "projects/simulation/params.py",
            "sha256": file_sha256(PARAMS_PATH),
            "resolved_scenes": manifest["resolved_scenes"],
        },
        "grid": manifest["grid"],
        "truth_firewall": "O1_ABSENT_FROM_TUNING_DEPLOYABLE_ROWS",
        "latents": records,
    }
    return raw


def _atomic_save(raw: dict, target: Path, script_name: str) -> None:
    from projects.simulation.common import save_results

    temporary = target.with_suffix(target.suffix + ".tmp")
    save_results(raw, str(temporary), script_name)
    os.replace(temporary, target)


def save_raw_and_clear_checkpoint(raw: dict, target: Path, checkpoint: Path, script_name: str) -> None:
    """Keep resumable state unless and until the atomic final save succeeds."""
    _atomic_save(raw, target, script_name)
    if checkpoint.exists():
        checkpoint.unlink()


def validated_temporary_output_dir(path: Path) -> Path:
    """Smoke artifacts must live outside the repository/tracked workspace."""
    resolved = Path(path).resolve()
    repository = REPO_ROOT.resolve()
    if resolved == repository or repository in resolved.parents:
        raise RuntimeError("smoke output must use a temporary directory outside the repository")
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    manifest = load_json(MANIFEST_PATH)
    if not truth_firewall_passes():
        raise RuntimeError("CH4_FAMILY_FREEZE_INVALID: deployable truth firewall failed")
    if args.smoke:
        if args.output_dir is None:
            raise SystemExit("--smoke requires --output-dir")
        output_dir = validated_temporary_output_dir(args.output_dir)
        checkpoint = output_dir / "b2_tuning_smoke_checkpoint.json"
        raw = build_raw(
            manifest, [20999], purpose="tuning_preflight_smoke_non_thesis",
            checkpoint_path=checkpoint,
        )
        from b2_tuning_reducer import reduce_raw

        smoke_aggregate = reduce_raw(raw, manifest, file_sha256(MANIFEST_PATH))
        if smoke_aggregate["census"] != {
            "scene_latents": 3, "observation_cells": 36, "arm_rows": 252
        }:
            raise RuntimeError("CH4_FAMILY_FREEZE_INVALID: tuning smoke census mismatch")
        target = output_dir / "b2_tuning_smoke_raw.json"
        save_raw_and_clear_checkpoint(
            raw, target, checkpoint, "t086_b2_tuning_preflight_smoke_non_thesis"
        )
        print(f"TUNING_SMOKE_STRUCTURAL_PASS {target}")
        return 0
    if args.output_dir is not None:
        raise SystemExit("canonical run does not accept --output-dir")
    if RAW_PATH.exists():
        raise RuntimeError("canonical tuning raw already exists; refusing rerun")
    raw = build_raw(
        manifest, list(range(21000, 21032)), purpose="canonical_tuning_non_thesis",
        checkpoint_path=CHECKPOINT_PATH,
    )
    save_raw_and_clear_checkpoint(
        raw, RAW_PATH, CHECKPOINT_PATH, "t086_b2_canonical_tuning_non_thesis"
    )
    print("CANONICAL_TUNING_COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
