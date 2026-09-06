"""T087 frozen Ch4 formal-production runner.

The module exposes pure census/authority helpers for static review.  Its CLI is
the only execution entry point and accepts only the registered smoke or formal
population; it intentionally has no scientific-grid overrides.
"""

from __future__ import annotations

import argparse
import hashlib
import inspect
import json
import os
import platform
import subprocess
import sys
import tempfile
import time
from collections.abc import Callable, Mapping
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import production_core as core


SEAM = Path(__file__).resolve().parent
SIM_ROOT = SEAM.parents[1]
REPO_ROOT = SEAM.parents[3]
MANIFEST_PATH = SEAM / "ch4_scientific_manifest.json"
LOCK_PATH = SEAM / "ch4_formal_execution_lock.json"
RAW_PATH = SEAM / "ch4_formal_raw.json"
CHECKPOINT_PATH = SEAM / "ch4_formal_checkpoint.json"
TESTS_PATH = SEAM / "tests/test_ch4_formal_production.py"
FROZEN_SCIENTIFIC_MANIFEST_SHA256 = (
    "417f334844f9092b02bab5d6478381ae7a57e2ff9b4a385ba37707f601521079"
)
BASE_COMMIT = "d3d98c6fc92642e4d6b964d086c1f3bea2018d1d"
PUBLIC_ROLES = ("B0", "B2_TUNED", "C4_FWD", "B3_PSC", "O1")
SCENES = ("weak", "moderate", "strong")
_SHA_CHARS = set("0123456789abcdef")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _valid_sha(value: object) -> bool:
    return isinstance(value, str) and len(value) == 64 and set(value) <= _SHA_CHARS


def _git_head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=SEAM,
        capture_output=True, text=True, check=True,
    ).stdout.strip()


def _dependency_path(relative: str) -> Path:
    if relative == "projects/simulation/params.py":
        return SIM_ROOT / "params.py"
    return SIM_ROOT / relative if relative.startswith("common/") else SEAM / relative


def current_execution_hashes() -> dict[str, str]:
    return {
        "formal_runner_sha256": file_sha256(Path(__file__)),
        "formal_reducer_sha256": file_sha256(SEAM / "ch4_formal_reducer.py"),
        "formal_reducer_entry_sha256": file_sha256(SEAM / "reduce_ch4_formal_production.py"),
        "formal_tests_sha256": file_sha256(TESTS_PATH),
    }


def registered_latent_ids(manifest: Mapping[str, object], purpose: str) -> list[int]:
    if purpose == "smoke":
        return [29999]
    if purpose == "formal":
        population = manifest.get("formal_population")
        if not isinstance(population, Mapping):
            raise RuntimeError("formal population missing")
        interval = population.get("latent_ids")
        if not isinstance(interval, Mapping):
            raise RuntimeError("formal population IDs missing")
        start = int(interval.get("start"))
        stop = int(interval.get("stop_inclusive"))
        if (start, stop, population.get("clusters")) != (30000, 30127, 128):
            raise RuntimeError("formal population changed")
        return list(range(start, stop + 1))
    raise RuntimeError("unregistered execution purpose")


def expected_census(purpose: str) -> dict[str, int]:
    if purpose == "smoke":
        clusters = 1
    elif purpose == "formal":
        clusters = 128
    else:
        raise ValueError("unregistered execution purpose")
    return {
        "top_level_latents": clusters,
        "scene_latents": 3 * clusters,
        "actual_cells": 119 * clusters,
        "arm_rows": 119 * 5 * clusters,
        "delta_zero_references": clusters,
    }


def _delta_label(delta: float) -> str:
    return str(float(delta)).replace(".", "p")


def formal_cell_specs(manifest: Mapping[str, object]) -> list[dict[str, object]]:
    """Return the frozen 119 actual cells plus one no-row delta-zero reference."""
    snr_grid = [float(value) for value in manifest.get("snr_grid_db", [])]
    if snr_grid != [float(value) for value in range(5, 42, 2)]:
        raise ValueError("scientific SNR grid changed")
    slices = manifest.get("slices")
    if not isinstance(slices, Mapping):
        raise ValueError("scientific slices missing")
    np_by_scene = {
        "weak": list(slices.get("weak_full_curve_np", [])),
        "moderate": list(slices.get("moderate_full_curve_np", [])),
        "strong": list(slices.get("strong_full_curve_np", [])),
    }
    if np_by_scene != {"weak": [2], "moderate": [2, 4, 8, 16], "strong": [2]}:
        raise ValueError("scientific scene/Np slices changed")
    cells: list[dict[str, object]] = []
    for scene in SCENES:
        for n_pilots in np_by_scene[scene]:
            for snr_db in snr_grid:
                cells.append({
                    "cell_id": f"{scene}_np{n_pilots}_snr{int(snr_db)}_primary",
                    "kind": "primary",
                    "scene": scene,
                    "n_pilots": int(n_pilots),
                    "snr_db": float(snr_db),
                    "delta": None,
                })
    mismatch = slices.get("mismatch")
    if not isinstance(mismatch, Mapping):
        raise ValueError("scientific mismatch slice missing")
    if (
        mismatch.get("scene") != "moderate"
        or mismatch.get("pilot_symbols_per_polarization") != 2
        or float(mismatch.get("snr_db")) != 25.0
        or [float(value) for value in mismatch.get("delta", [])]
        != [0.0, 0.05, 0.1, 0.2, 0.3, 0.4]
    ):
        raise ValueError("scientific mismatch slice changed")
    for delta in (0.05, 0.1, 0.2, 0.3, 0.4):
        cells.append({
            "cell_id": f"moderate_np2_snr25_delta{_delta_label(delta)}",
            "kind": "mismatch",
            "scene": "moderate",
            "n_pilots": 2,
            "snr_db": 25.0,
            "delta": delta,
        })
    cells.append({
        "cell_id": "mismatch_delta0_reference",
        "kind": "reference",
        "delta": 0.0,
        "references_cell_id": "moderate_np2_snr25_primary",
    })
    if len(cells) != 120 or len({item["cell_id"] for item in cells}) != 120:
        raise ValueError("formal cell census is not 119 actual plus one reference")
    return cells


def truth_firewall_passes() -> bool:
    signature = tuple(inspect.signature(core.receiver_action).parameters)
    source = inspect.getsource(core.receiver_action).lower()
    return signature == ("arm", "x_pilots", "y_pilots", "y_payload", "parameter") and not any(
        token in source for token in ("h_true", "bits", "decision", "truth")
    )


def verify_execution_authority(
    manifest: Mapping[str, object],
    lock: Mapping[str, object],
    *,
    purpose: str,
    scientific_manifest_sha256: str,
    actual_execution_hashes: Mapping[str, str] | None = None,
    git_head: str | None = None,
    current_environment_snapshot: Mapping[str, str] | None = None,
) -> None:
    """Fail closed unless both the scientific manifest and execution lock match."""
    if scientific_manifest_sha256 != FROZEN_SCIENTIFIC_MANIFEST_SHA256:
        raise RuntimeError("scientific manifest SHA mismatch")
    if manifest.get("base_commit") != BASE_COMMIT:
        raise RuntimeError("scientific manifest base commit mismatch")
    required_manifest = {
        "schema_version": "t086.ch4-scientific-manifest.v1",
        "formal_population": {
            "latent_ids": {"start": 30000, "stop_inclusive": 30127},
            "clusters": 128,
            "cluster_key": "latent_id",
            "shared_across_all_slices_snr_np_and_mismatch": True,
        },
    }
    for key, expected in required_manifest.items():
        if manifest.get(key) != expected:
            raise RuntimeError(f"scientific manifest contract mismatch: {key}")
    required_lock = {
        "schema_version": "t087.ch4-formal-execution-lock.v1",
        "authority": "T087/D066/V041",
        "action_class": "CH4_FORMAL_EXECUTION_SEAM",
        "mission_checkpoint": "CP028",
        "control_epoch": 28,
        "base_commit": BASE_COMMIT,
        "scientific_manifest_sha256": FROZEN_SCIENTIFIC_MANIFEST_SHA256,
    }
    for key, expected in required_lock.items():
        if lock.get(key) != expected:
            raise RuntimeError(f"execution lock mismatch: {key}")
    expected_populations = {
        "smoke": [29999],
        "formal": {"start": 30000, "stop_inclusive": 30127},
    }
    if lock.get("allowed_populations") != expected_populations:
        raise RuntimeError("execution population lock mismatch")
    expected_execution_keys = {
        "formal_runner_sha256", "formal_reducer_sha256",
        "formal_reducer_entry_sha256", "formal_tests_sha256",
    }
    locked_hashes = lock.get("execution_hashes")
    if not isinstance(locked_hashes, Mapping) or set(locked_hashes) != expected_execution_keys:
        raise RuntimeError("execution hash key set mismatch")
    actual = dict(actual_execution_hashes or current_execution_hashes())
    if actual != dict(locked_hashes):
        raise RuntimeError("execution hash mismatch")
    frozen = lock.get("frozen_dependency_hashes")
    manifest_frozen = manifest.get("frozen_code_hashes")
    params = manifest.get("params_authority")
    expected_frozen = dict(manifest_frozen) if isinstance(manifest_frozen, Mapping) else {}
    expected_frozen["projects/simulation/params.py"] = (
        params.get("sha256") if isinstance(params, Mapping) else None
    )
    if frozen != expected_frozen:
        raise RuntimeError("frozen dependency lock mismatch")
    for relative, expected in frozen.items():
        if not _valid_sha(expected):
            raise RuntimeError(f"frozen dependency hash invalid: {relative}")
        if actual_execution_hashes is None and file_sha256(_dependency_path(relative)) != expected:
            raise RuntimeError(f"frozen dependency hash mismatch: {relative}")
    if (git_head or _git_head()) != BASE_COMMIT:
        raise RuntimeError("execution base commit mismatch")
    actual_environment = dict(current_environment_snapshot or environment_snapshot())
    if lock.get("environment_snapshot") != actual_environment:
        raise RuntimeError("execution environment snapshot mismatch")
    registered_latent_ids(manifest, purpose)
    formal_cell_specs(manifest)


def deployable_action(
    public_role: str,
    runtime_roles: Mapping[str, Mapping[str, object]],
    selected_tau: float,
    x_pilots: object,
    y_pilots: object,
    y_payload: object,
    *,
    receiver: Callable[..., dict],
) -> dict:
    if public_role not in runtime_roles:
        raise ValueError(f"unknown public role: {public_role}")
    role = runtime_roles[public_role]
    runtime_arm = role.get("runtime_arm")
    if public_role == "O1" or runtime_arm == "O1_TRUTH_ONLY":
        raise ValueError("O1 is truth-only and cannot enter the deployable receiver")
    parameter = float(selected_tau) if public_role == "B2_TUNED" else role.get("parameter")
    return receiver(runtime_arm, x_pilots, y_pilots, y_payload, parameter)


def mismatch_channel(latent: Mapping[str, object], delta: float) -> np.ndarray:
    value = float(delta)
    if not np.isfinite(value) or not 0.0 <= value < 1.0:
        raise ValueError("delta must be finite in [0,1)")
    if value == 0.0:
        return np.asarray(latent["h_true"])
    gain = float(latent["gain"])
    q = np.asarray(latent["q"])
    right = np.asarray(latent["mismatch_right"])
    diagonal = np.diag([1.0 + value, 1.0 - value]) / np.sqrt(1.0 + value**2)
    channel = gain * q @ right @ diagonal @ right.conj().T
    if channel.shape != (2, 2) or not np.all(np.isfinite(channel)):
        raise core.InvalidEstimate("mismatch channel is invalid")
    return channel


def observe_mismatch(
    latent: Mapping[str, object], snr_db: float, n_pilots: int, delta: float
) -> dict[str, object]:
    value = float(delta)
    if value == 0.0:
        primary = core.observe_latent(latent, snr_db, n_pilots)
        return {
            **primary,
            "h_true": np.asarray(latent["h_true"]),
            "latent_hashes": dict(latent["latent_hashes"]),
        }
    channel = mismatch_channel(latent, value)
    snr = float(snr_db)
    count = int(n_pilots)
    if count not in (2, 4, 8, 16) or count > int(latent["max_pilots"]):
        raise ValueError("unsupported mismatch pilot count")
    if not np.isfinite(snr):
        raise ValueError("mismatch SNR must be finite")
    noise_scale = float(np.sqrt(10.0 ** (-snr / 10.0) / 2.0))
    x_pilots = core.balanced_pilots(count)
    pilot_noise = np.asarray(latent["pilot_noise"])[:, :count]
    payload_noise = np.asarray(latent["payload_noise"])
    y_pilots = channel @ x_pilots + noise_scale * pilot_noise
    y_payload = channel @ np.asarray(latent["x_payload"]) + noise_scale * payload_noise
    return {
        "scenario": latent["scenario"],
        "latent_id": int(latent["latent_id"]),
        "snr_db": snr,
        "n_pilots": count,
        "delta": value,
        "noise_scale": noise_scale,
        "x_pilots": x_pilots,
        "y_pilots": y_pilots,
        "y_payload": y_payload,
        "h_true": channel,
        "latent_hashes": dict(latent["latent_hashes"]),
        "observation_hashes": {
            "x_pilots": core._hash_arrays(x_pilots),
            "y_pilots": core._hash_arrays(y_pilots),
            "y_payload": core._hash_arrays(y_payload),
        },
    }


def _oracle_action(y_payload: np.ndarray, h_true: np.ndarray) -> dict:
    channel = np.asarray(h_true, dtype=np.complex128)
    payload = np.asarray(y_payload, dtype=np.complex128)
    inverse = np.linalg.inv(channel)
    singular = np.linalg.svd(channel, compute_uv=False)
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


def _hash_action(action: Mapping[str, object]) -> str:
    digest = hashlib.sha256()
    for key in ("z", "h_hat", "w"):
        value = np.ascontiguousarray(action[key], dtype=np.complex128)
        digest.update(key.encode("ascii"))
        digest.update(value.tobytes())
    return digest.hexdigest()


def _build_rows(
    observation: Mapping[str, object],
    latent: Mapping[str, object],
    manifest: Mapping[str, object],
    selected_tau: float,
) -> list[dict[str, object]]:
    rows = []
    runtime_roles = manifest["runtime_roles"]
    for public_role in PUBLIC_ROLES:
        started = time.perf_counter_ns()
        if public_role == "O1":
            action = _oracle_action(observation["y_payload"], observation["h_true"])
            runtime_arm = "O1_TRUTH_ONLY"
            parameter = None
        else:
            action = deployable_action(
                public_role,
                runtime_roles,
                selected_tau,
                observation["x_pilots"],
                observation["y_pilots"],
                observation["y_payload"],
                receiver=core.receiver_action,
            )
            runtime_arm = runtime_roles[public_role]["runtime_arm"]
            parameter = selected_tau if public_role == "B2_TUNED" else runtime_roles[public_role]["parameter"]
        runtime_ns = time.perf_counter_ns() - started
        metrics = core.score_action(action, latent["bits"], observation["h_true"])
        metrics.update({
            "public_scale": None if action.get("scale") is None else float(action["scale"]),
            "psc_scale": float(action.get("psc_scale", 1.0)),
            "channel_nmse_semantics": (
                "pre_calibration_inherited" if public_role == "B3_PSC" else "direct_estimate"
            ),
        })
        rows.append({
            "public_role": public_role,
            "runtime_arm": runtime_arm,
            "parameter": parameter,
            "metrics": metrics,
            "validity": "VALID",
            "action_sha256": _hash_action(action),
            "runtime_ns": int(runtime_ns),
        })
    return rows


def _build_latent_record(
    manifest: Mapping[str, object], latent_id: int
) -> dict[str, object]:
    signal = manifest["signal"]
    latents = {
        scene: core.make_latent_window(
            scene, latent_id, int(signal["payload_symbols_per_polarization"]), 16
        )
        for scene in SCENES
    }
    cells_by_scene: dict[str, list[dict[str, object]]] = {scene: [] for scene in SCENES}
    primary_by_id: dict[str, dict[str, object]] = {}
    for spec in formal_cell_specs(manifest):
        if spec["kind"] == "reference":
            continue
        scene = str(spec["scene"])
        latent = latents[scene]
        if spec["kind"] == "mismatch":
            observation = observe_mismatch(
                latent, float(spec["snr_db"]), int(spec["n_pilots"]), float(spec["delta"])
            )
        else:
            observed = core.observe_latent(latent, spec["snr_db"], spec["n_pilots"])
            observation = {
                **observed,
                "h_true": np.asarray(latent["h_true"]),
                "latent_hashes": dict(latent["latent_hashes"]),
            }
        tau_key = f"{scene}_np{spec['n_pilots']}"
        selected_tau = float(manifest["tuned_tau_by_scene_np"][tau_key])
        cell = {
            **spec,
            "latent_id": int(latent_id),
            "h_true_sha256": core._hash_arrays(observation["h_true"]),
            "latent_hashes": dict(latent["latent_hashes"]),
            "observation_hashes": dict(observation["observation_hashes"]),
            "rows": _build_rows(observation, latent, manifest, selected_tau),
        }
        cells_by_scene[scene].append(cell)
        primary_by_id[spec["cell_id"]] = cell
    primary = primary_by_id["moderate_np2_snr25_primary"]
    reference = {
        "cell_id": "mismatch_delta0_reference",
        "kind": "reference",
        "delta": 0.0,
        "references_cell_id": primary["cell_id"],
        "latent_id": int(latent_id),
        "h_true_sha256": primary["h_true_sha256"],
        "reference_observation_hashes": dict(primary["observation_hashes"]),
    }
    scene_records = []
    for scene in SCENES:
        latent = latents[scene]
        scene_records.append({
            "scene": scene,
            "latent_id": int(latent_id),
            "rng_namespace": latent["rng_namespace"],
            "latent_hashes": latent["latent_hashes"],
            "turbulence": latent["turbulence"],
            "cells": cells_by_scene[scene],
        })
    return {
        "latent_id": int(latent_id),
        "scenes": scene_records,
        "delta_zero_reference": reference,
    }


def _canonical_digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _write_checkpoint(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, indent=2), encoding="utf-8")
    os.replace(temporary, path)


def build_raw(
    manifest: Mapping[str, object],
    lock: Mapping[str, object],
    *,
    purpose: str,
    checkpoint_path: Path,
    scientific_manifest_sha256: str,
    execution_lock_sha256: str,
) -> dict[str, object]:
    execution_purpose = "smoke" if purpose == "formal_smoke_non_thesis" else "formal"
    if purpose not in {"formal_smoke_non_thesis", "canonical_formal_production"}:
        raise RuntimeError("unregistered raw purpose")
    verify_execution_authority(
        manifest,
        lock,
        purpose=execution_purpose,
        scientific_manifest_sha256=scientific_manifest_sha256,
    )
    identifiers = registered_latent_ids(manifest, execution_purpose)
    binding = {
        "purpose": purpose,
        "latent_ids": identifiers,
        "scientific_manifest_sha256": scientific_manifest_sha256,
        "execution_lock_sha256": execution_lock_sha256,
        "execution_hashes": dict(lock["execution_hashes"]),
    }
    records: list[dict[str, object]] = []
    if checkpoint_path.exists():
        checkpoint = load_json(checkpoint_path)
        if checkpoint.get("binding") != binding:
            raise RuntimeError("CH4_FORMAL_INVALID: checkpoint binding mismatch")
        entries = checkpoint.get("records")
        if not isinstance(entries, list):
            raise RuntimeError("CH4_FORMAL_INVALID: checkpoint records invalid")
        for entry in entries:
            if not isinstance(entry, Mapping) or set(entry) != {"record", "sha256"}:
                raise RuntimeError("CH4_FORMAL_INVALID: checkpoint entry invalid")
            record = entry["record"]
            if entry["sha256"] != _canonical_digest(record):
                raise RuntimeError("CH4_FORMAL_INVALID: checkpoint record hash mismatch")
            records.append(record)
    completed = [int(record.get("latent_id")) for record in records]
    if completed != identifiers[: len(completed)] or len(completed) != len(set(completed)):
        raise RuntimeError("CH4_FORMAL_INVALID: checkpoint latent census invalid")
    for latent_id in identifiers[len(records) :]:
        record = _build_latent_record(manifest, latent_id)
        records.append(record)
        checkpoint_records = [
            {"record": item, "sha256": _canonical_digest(item)} for item in records
        ]
        _write_checkpoint(checkpoint_path, {"binding": binding, "records": checkpoint_records})
        print(f"latent {latent_id}: {len(records)}/{len(identifiers)}")
    if [int(record["latent_id"]) for record in records] != identifiers:
        raise RuntimeError("CH4_FORMAL_INVALID: completed latent census invalid")
    return {
        "schema_version": "t087.ch4-formal-raw.v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": purpose,
        "authority": lock["authority"],
        "base_commit": lock["base_commit"],
        "control_epoch": lock["control_epoch"],
        "mission_checkpoint": lock["mission_checkpoint"],
        "scientific_manifest_sha256": scientific_manifest_sha256,
        "execution_lock_sha256": execution_lock_sha256,
        "execution_hashes": dict(lock["execution_hashes"]),
        "truth_firewall": "O1_SEPARATE_TRUTH_ONLY_PATH",
        "latent_ids": identifiers,
        "latents": records,
    }


def _worktree_roots() -> list[Path]:
    output = subprocess.run(
        ["git", "worktree", "list", "--porcelain"], cwd=SEAM,
        capture_output=True, text=True, check=True,
    ).stdout
    return [Path(line[9:]).resolve() for line in output.splitlines() if line.startswith("worktree ")]


def validated_temporary_output_dir(path: Path) -> Path:
    resolved = Path(path).resolve()
    temp_root = Path(tempfile.gettempdir()).resolve()
    if resolved != temp_root and temp_root not in resolved.parents:
        raise RuntimeError("smoke output must be inside the OS temporary directory")
    for root in _worktree_roots():
        if resolved == root or root in resolved.parents:
            raise RuntimeError("smoke output must be outside every Git worktree")
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def resolve_execution_lock_path(
    *,
    smoke: bool,
    temporary_lock: Path | None,
    worktree_roots: list[Path] | None = None,
) -> Path:
    """Keep the required temp-smoke -> tracked-formal lock order executable."""
    if not smoke:
        if temporary_lock is not None:
            raise RuntimeError("formal production forbids an execution-lock override")
        return LOCK_PATH
    if temporary_lock is None:
        raise RuntimeError("smoke requires an OS-temporary execution lock")
    resolved = Path(temporary_lock).resolve()
    temp_root = Path(tempfile.gettempdir()).resolve()
    if resolved != temp_root and temp_root not in resolved.parents:
        raise RuntimeError("smoke execution lock must be inside the OS temporary directory")
    roots = _worktree_roots() if worktree_roots is None else [Path(root).resolve() for root in worktree_roots]
    for root in roots:
        if resolved == root or root in resolved.parents:
            raise RuntimeError("smoke execution lock must be outside every Git worktree")
    return resolved


def _atomic_save(data: dict, target: Path, script_name: str) -> None:
    from projects.simulation.common import save_results

    temporary = target.with_suffix(target.suffix + ".tmp")
    save_results(data, str(temporary), script_name)
    os.replace(temporary, target)


def save_raw_and_clear_checkpoint(raw: dict, target: Path, checkpoint: Path, script_name: str) -> None:
    _atomic_save(raw, target, script_name)
    if checkpoint.exists():
        checkpoint.unlink()


def environment_snapshot() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "platform": platform.platform(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    population = parser.add_mutually_exclusive_group(required=True)
    population.add_argument("--smoke", action="store_true")
    population.add_argument("--formal", action="store_true")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--temporary-lock", type=Path)
    args = parser.parse_args()
    lock_path = resolve_execution_lock_path(
        smoke=bool(args.smoke), temporary_lock=args.temporary_lock
    )
    if not lock_path.is_file():
        raise RuntimeError("execution lock is absent")
    manifest = load_json(MANIFEST_PATH)
    lock = load_json(lock_path)
    if not truth_firewall_passes():
        raise RuntimeError("CH4_FORMAL_INVALID: deployable truth firewall failed")
    manifest_sha = file_sha256(MANIFEST_PATH)
    lock_sha = file_sha256(lock_path)
    if args.smoke:
        if args.output_dir is None:
            raise SystemExit("--smoke requires --output-dir")
        output_dir = validated_temporary_output_dir(args.output_dir)
        checkpoint = output_dir / "ch4_formal_smoke_checkpoint.json"
        raw = build_raw(
            manifest,
            lock,
            purpose="formal_smoke_non_thesis",
            checkpoint_path=checkpoint,
            scientific_manifest_sha256=manifest_sha,
            execution_lock_sha256=lock_sha,
        )
        from ch4_formal_reducer import reduce_raw

        aggregate = reduce_raw(
            raw,
            manifest,
            lock,
            scientific_manifest_sha256=manifest_sha,
            execution_lock_sha256=lock_sha,
        )
        if aggregate.get("terminal") != "FORMAL_SMOKE_STRUCTURAL_PASS":
            raise RuntimeError("CH4_FORMAL_INVALID: smoke reduction failed")
        target = output_dir / "ch4_formal_smoke_raw.json"
        save_raw_and_clear_checkpoint(raw, target, checkpoint, "t087_ch4_formal_smoke_non_thesis")
        print(f"FORMAL_SMOKE_STRUCTURAL_PASS {target}")
        return 0
    if args.output_dir is not None:
        raise SystemExit("formal production does not accept --output-dir")
    if RAW_PATH.exists():
        raise RuntimeError("canonical formal raw already exists; refusing rerun")
    raw = build_raw(
        manifest,
        lock,
        purpose="canonical_formal_production",
        checkpoint_path=CHECKPOINT_PATH,
        scientific_manifest_sha256=manifest_sha,
        execution_lock_sha256=lock_sha,
    )
    save_raw_and_clear_checkpoint(raw, RAW_PATH, CHECKPOINT_PATH, "t087_ch4_canonical_formal_production")
    print("CH4_FORMAL_PRODUCTION_COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
