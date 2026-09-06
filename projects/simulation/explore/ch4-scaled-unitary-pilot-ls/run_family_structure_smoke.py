"""T086 family-structure smoke helpers (formal production is forbidden here)."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import time
from collections.abc import Callable, Mapping
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import production_core as core


SEAM = Path(__file__).resolve().parent
REPO_ROOT = SEAM.parents[3]
SIM_ROOT = SEAM.parents[1]
SCHEMA_PATH = SEAM / "ch4_scientific_manifest_schema.json"
TUNING_MANIFEST_PATH = SEAM / "b2_tuning_manifest.json"
TUNING_RAW_PATH = SEAM / "b2_tuning_raw.json"
TUNING_AGGREGATE_PATH = SEAM / "b2_tuning_aggregate.json"
TUNING_RECEIPT_PATH = SEAM / "b2_tuning_receipt.json"
_SHA_CHARS = set("0123456789abcdef")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _valid_sha(value: object) -> bool:
    return isinstance(value, str) and len(value) == 64 and set(value) <= _SHA_CHARS


def mismatch_channel(latent: Mapping[str, object], delta: float) -> np.ndarray:
    """Return the frozen Q-R direction-scale mismatch; delta=0 aliases primary H."""
    value = float(delta)
    if not np.isfinite(value) or value < 0.0 or value >= 1.0:
        raise ValueError("delta must be finite in [0,1)")
    h_true = np.asarray(latent["h_true"])
    if value == 0.0:
        return h_true
    gain = float(latent["gain"])
    q = np.asarray(latent["q"])
    right = np.asarray(latent["mismatch_right"])
    d = np.diag([1.0 + value, 1.0 - value]) / np.sqrt(1.0 + value**2)
    result = gain * q @ right @ d @ right.conj().T
    if result.shape != (2, 2) or not np.all(np.isfinite(result)):
        raise ValueError("mismatch channel is invalid")
    return result


def observe_mismatch(
    latent: Mapping[str, object], snr_db: float, n_pilots: int, delta: float
) -> dict[str, object]:
    """Observe H_delta with the frozen latent's exact bits and base-noise arrays."""
    value = float(delta)
    if value == 0.0:
        primary = core.observe_latent(latent, snr_db, n_pilots)
        return {**primary, "h_true": np.asarray(latent["h_true"]), "latent_hashes": dict(latent["latent_hashes"])}
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
    if not (np.all(np.isfinite(y_pilots)) and np.all(np.isfinite(y_payload))):
        raise core.InvalidEstimate("mismatch observation is non-finite")
    return {
        "scenario": latent["scenario"], "latent_id": int(latent["latent_id"]),
        "snr_db": snr, "n_pilots": count, "delta": value,
        "noise_scale": noise_scale, "x_pilots": x_pilots,
        "y_pilots": y_pilots, "y_payload": y_payload,
        "pilot_noise": pilot_noise.copy(), "h_true": channel,
        "latent_hashes": dict(latent["latent_hashes"]),
        "observation_hashes": {
            "x_pilots": core._hash_arrays(x_pilots),
            "y_pilots": core._hash_arrays(y_pilots),
            "y_payload": core._hash_arrays(y_payload),
        },
    }


def formal_smoke_cells() -> list[dict[str, object]]:
    """Return the exact T086 ID=21999 structural smoke census."""
    cells = []
    for n_pilots in (2, 4):
        for snr_db in (5.0, 41.0):
            cells.append({
                "cell_id": f"moderate_np{n_pilots}_snr{int(snr_db)}_primary",
                "kind": "primary", "scene": "moderate", "n_pilots": n_pilots,
                "snr_db": snr_db, "delta": None,
            })
    for n_pilots in (8, 16):
        cells.append({
            "cell_id": f"moderate_np{n_pilots}_snr25_primary",
            "kind": "primary", "scene": "moderate", "n_pilots": n_pilots,
            "snr_db": 25.0, "delta": None,
        })
    for scene in ("weak", "strong"):
        cells.append({
            "cell_id": f"{scene}_np2_snr25_primary",
            "kind": "primary", "scene": scene, "n_pilots": 2,
            "snr_db": 25.0, "delta": None,
        })
    cells.extend([
        {
            "cell_id": "moderate_np2_snr25_primary", "kind": "primary",
            "scene": "moderate", "n_pilots": 2, "snr_db": 25.0, "delta": None,
        },
        {
            "cell_id": "moderate_np2_snr25_delta0p4", "kind": "mismatch",
            "scene": "moderate", "n_pilots": 2, "snr_db": 25.0, "delta": 0.4,
        },
        {
            "cell_id": "mismatch_delta0_reference", "kind": "reference", "delta": 0.0,
            "references_cell_id": "moderate_np2_snr25_primary",
        },
    ])
    return cells


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
    """Map a public role to the frozen runtime arm before calling the receiver."""
    if public_role not in runtime_roles:
        raise ValueError(f"unknown public role: {public_role}")
    role = runtime_roles[public_role]
    runtime_arm = role.get("runtime_arm")
    if runtime_arm == "O1_TRUTH_ONLY" or public_role == "O1":
        raise ValueError("O1 is truth-only and cannot enter the deployable receiver")
    if public_role == "B2_TUNED":
        parameter = float(selected_tau)
    else:
        parameter = role.get("parameter")
    return receiver(runtime_arm, x_pilots, y_pilots, y_payload, parameter)


def structure_binding(
    schema: Mapping[str, object],
    aggregate: Mapping[str, object],
    receipt: Mapping[str, object],
    *,
    schema_sha256: str,
    receipt_sha256: str,
) -> dict[str, object]:
    if schema.get("schema_version") != "t086.ch4-scientific-manifest-schema.v1":
        raise ValueError("structure smoke schema mismatch")
    if not (_valid_sha(schema_sha256) and _valid_sha(receipt_sha256)):
        raise ValueError("structure smoke binding SHA is invalid")
    if aggregate.get("decision", {}).get("terminal") != "CH4_FAMILY_PRODUCTION_FREEZE_READY":
        raise ValueError("structure smoke requires family-freeze-ready tuning decision")
    if receipt.get("terminal") != "CH4_B2_TUNING_ACCEPTED":
        raise ValueError("structure smoke requires accepted tuning receipt")
    selections = aggregate.get("selected_tau_by_scene_np")
    expected_keys = {f"{scene}_np{n}" for scene in ("weak", "moderate", "strong") for n in (2, 4, 8, 16)}
    if not isinstance(selections, Mapping) or set(selections) != expected_keys:
        raise ValueError("structure smoke requires all 12 selected taus")
    if receipt.get("selected_tau_by_scene_np") != selections:
        raise ValueError("tuning aggregate/receipt selected-tau mismatch")
    if any(float(value) not in (0.0, 0.25, 0.5, 0.75, 1.0) for value in selections.values()):
        raise ValueError("structure smoke selected tau is outside the frozen grid")
    return {
        "authority": schema["authority"],
        "base_commit": schema["base_commit"],
        "latent_id": 21999,
        "schema_sha256": schema_sha256,
        "tuning_receipt_sha256": receipt_sha256,
        "selected_tau_by_scene_np": dict(selections),
        "runtime_roles": schema["runtime_roles"],
    }


def validated_temporary_output_dir(path: Path) -> Path:
    resolved = Path(path).resolve()
    repository = REPO_ROOT.resolve()
    if resolved == repository or repository in resolved.parents:
        raise RuntimeError("structure smoke output must use a temporary directory outside the repository")
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def _oracle_action(y_payload: np.ndarray, h_true: np.ndarray) -> dict:
    channel = np.asarray(h_true, dtype=np.complex128)
    payload = np.asarray(y_payload, dtype=np.complex128)
    if channel.shape != (2, 2) or payload.ndim != 2 or payload.shape[0] != 2:
        raise core.InvalidEstimate("invalid truth-only oracle input")
    inverse = np.linalg.inv(channel)
    singular = np.linalg.svd(channel, compute_uv=False)
    return {
        "arm": "O1", "z": inverse @ payload, "h_hat": channel.copy(), "w": inverse,
        "rho": float(singular[0] / singular[1]), "singular_values": singular,
        "scale": float(np.mean(singular)), "psc_scale": 1.0,
    }


def _hash_action(action: Mapping[str, object]) -> str:
    digest = hashlib.sha256()
    for key in ("z", "h_hat", "w"):
        value = np.ascontiguousarray(action[key], dtype=np.complex128)
        digest.update(key.encode("ascii"))
        digest.update(value.tobytes())
    return digest.hexdigest()


def _build_rows(
    observation: Mapping[str, object], latent: Mapping[str, object],
    runtime_roles: Mapping[str, Mapping[str, object]], selected_tau: float,
) -> list[dict[str, object]]:
    rows = []
    for public_role in ("B0", "B2_TUNED", "C4_FWD", "B3_PSC", "O1"):
        started = time.perf_counter_ns()
        if public_role == "O1":
            action = _oracle_action(observation["y_payload"], observation["h_true"])
            runtime_arm = "O1_TRUTH_ONLY"
            parameter = None
        else:
            action = deployable_action(
                public_role, runtime_roles, selected_tau,
                observation["x_pilots"], observation["y_pilots"], observation["y_payload"],
                receiver=core.receiver_action,
            )
            runtime_arm = runtime_roles[public_role]["runtime_arm"]
            parameter = selected_tau if public_role == "B2_TUNED" else runtime_roles[public_role]["parameter"]
        runtime_ns = time.perf_counter_ns() - started
        metrics = core.score_action(action, latent["bits"], observation["h_true"])
        rows.append({
            "public_role": public_role, "runtime_arm": runtime_arm, "parameter": parameter,
            "metrics": metrics, "validity": "VALID", "action_sha256": _hash_action(action),
            "runtime_ns": int(runtime_ns),
        })
    return rows


def build_structure_raw(
    schema: Mapping[str, object], binding: Mapping[str, object]
) -> dict[str, object]:
    latent_id = int(binding["latent_id"])
    signal = schema["signal"]
    latents = {
        scene: core.make_latent_window(
            scene, latent_id, signal["payload_symbols_per_polarization"], 16
        ) for scene in ("weak", "moderate", "strong")
    }
    cells = []
    primary_by_id = {}
    for spec in formal_smoke_cells():
        if spec["kind"] == "reference":
            primary = primary_by_id[spec["references_cell_id"]]
            cells.append({
                **spec,
                "h_true_sha256": primary["h_true_sha256"],
                "reference_observation_hashes": dict(primary["observation_hashes"]),
            })
            continue
        latent = latents[spec["scene"]]
        if spec["kind"] == "mismatch":
            observation = observe_mismatch(latent, spec["snr_db"], spec["n_pilots"], spec["delta"])
        else:
            observed = core.observe_latent(latent, spec["snr_db"], spec["n_pilots"])
            observation = {
                **observed, "h_true": np.asarray(latent["h_true"]),
                "latent_hashes": dict(latent["latent_hashes"]),
            }
        tau_key = f"{spec['scene']}_np{spec['n_pilots']}"
        cell = {
            **spec, "latent_id": latent_id,
            "h_true_sha256": core._hash_arrays(observation["h_true"]),
            "latent_hashes": dict(latent["latent_hashes"]),
            "observation_hashes": dict(observation["observation_hashes"]),
            "rows": _build_rows(
                observation, latent, binding["runtime_roles"],
                float(binding["selected_tau_by_scene_np"][tau_key]),
            ),
        }
        cells.append(cell)
        primary_by_id[spec["cell_id"]] = cell
    return {
        "schema_version": "t086.family-structure-smoke-raw.v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "formal_structure_smoke_non_thesis",
        "authority": binding["authority"], "base_commit": binding["base_commit"],
        "latent_id": latent_id,
        "binding": {
            "schema_sha256": binding["schema_sha256"],
            "tuning_receipt_sha256": binding["tuning_receipt_sha256"],
        },
        "selected_tau_by_scene_np": dict(binding["selected_tau_by_scene_np"]),
        "truth_firewall": "O1_SEPARATE_TRUTH_ONLY_PATH",
        "cells": cells,
    }


def validate_structure_raw(raw: Mapping[str, object], binding: Mapping[str, object]) -> dict[str, object]:
    required = {
        "schema_version": "t086.family-structure-smoke-raw.v1",
        "purpose": "formal_structure_smoke_non_thesis",
        "authority": binding["authority"], "latent_id": 21999,
    }
    for key, expected in required.items():
        if raw.get(key) != expected:
            raise ValueError(f"structure raw header mismatch: {key}")
    raw_binding = raw.get("binding")
    if not isinstance(raw_binding, Mapping) or raw_binding.get("schema_sha256") != binding["schema_sha256"] or raw_binding.get("tuning_receipt_sha256") != binding["tuning_receipt_sha256"]:
        raise ValueError("structure raw binding mismatch")
    if raw.get("selected_tau_by_scene_np") != binding["selected_tau_by_scene_np"]:
        raise ValueError("structure raw selected-tau map mismatch")
    cells = raw.get("cells")
    expected_specs = formal_smoke_cells()
    if not isinstance(cells, list) or len(cells) != len(expected_specs):
        raise ValueError("structure cell census invalid")
    observed_ids = [cell.get("cell_id") for cell in cells if isinstance(cell, Mapping)]
    if observed_ids != [cell["cell_id"] for cell in expected_specs]:
        raise ValueError("structure cell census/order invalid")
    actual = {}
    expected_roles = [
        ("B0", "B0", None), ("B2_TUNED", "B2", None),
        ("C4_FWD", "C4", None), ("B3_PSC", "B3_PSC", 1.0),
        ("O1", "O1_TRUTH_ONLY", None),
    ]
    for cell, spec in zip(cells, expected_specs):
        for key, value in spec.items():
            if cell.get(key) != value:
                raise ValueError(f"structure cell contract mismatch: {spec['cell_id']}/{key}")
        if spec["kind"] == "reference":
            referenced = actual.get(spec["references_cell_id"])
            if referenced is None or cell.get("h_true_sha256") != referenced.get("h_true_sha256") or cell.get("reference_observation_hashes") != referenced.get("observation_hashes"):
                raise ValueError("delta-zero reference is not exact primary identity")
            if "rows" in cell:
                raise ValueError("delta-zero reference must not duplicate rows")
            continue
        if cell.get("latent_id") != 21999:
            raise ValueError("structure smoke latent ID changed")
        for name in ("h_true_sha256",):
            if not _valid_sha(cell.get(name)):
                raise ValueError(f"invalid structure hash: {name}")
        for hashes_name, expected_keys in (
            ("observation_hashes", {"x_pilots", "y_pilots", "y_payload"}),
            ("latent_hashes", {"payload_bits", "channel_q", "gg_gain", "pilot_noise", "payload_noise", "mismatch_left", "mismatch_right"}),
        ):
            hashes = cell.get(hashes_name)
            if not isinstance(hashes, Mapping) or set(hashes) != expected_keys or not all(_valid_sha(value) for value in hashes.values()):
                raise ValueError(f"invalid structure hashes: {hashes_name}")
        rows = cell.get("rows")
        if not isinstance(rows, list) or len(rows) != 5:
            raise ValueError("structure arm row census invalid")
        tau = binding["selected_tau_by_scene_np"][f"{spec['scene']}_np{spec['n_pilots']}"]
        for row, (role, runtime, fixed_parameter) in zip(rows, expected_roles):
            expected_parameter = tau if role == "B2_TUNED" else fixed_parameter
            if (row.get("public_role"), row.get("runtime_arm"), row.get("parameter")) != (role, runtime, expected_parameter):
                raise ValueError("structure public/runtime role mapping invalid")
            if row.get("validity") != "VALID" or not _valid_sha(row.get("action_sha256")):
                raise ValueError("structure row validity/hash invalid")
            metrics = row.get("metrics")
            if not isinstance(metrics, Mapping) or metrics.get("payload_bits") != 32768:
                raise ValueError("structure row metrics/bits invalid")
            numbers = [metrics.get(key) for key in ("bit_errors", "ber", "channel_nmse", "inverse_residual", "rho")]
            if not all(np.isfinite(float(value)) for value in numbers):
                raise ValueError("structure row metric is non-finite")
            if int(metrics["bit_errors"]) < 0 or int(metrics["bit_errors"]) > 32768 or float(metrics["ber"]) != int(metrics["bit_errors"]) / 32768:
                raise ValueError("structure row raw counts are inconsistent")
        actual[spec["cell_id"]] = cell

    from family_freeze_contract import required_snr

    crossing_states = {}
    for role in ("B0", "B2_TUNED", "C4_FWD", "B3_PSC", "O1"):
        curve = [actual[f"moderate_np2_snr{snr}_primary"] for snr in (5, 41)]
        row_index = ("B0", "B2_TUNED", "C4_FWD", "B3_PSC", "O1").index(role)
        result = required_snr(
            [5.0, 41.0],
            [int(cell["rows"][row_index]["metrics"]["bit_errors"]) for cell in curve],
            [32768, 32768], threshold=0.0038,
        )
        crossing_states[role] = result["status"]
    return {"status": "STRUCTURE_SMOKE_PASS", "actual_cells": 10, "references": 1, "crossing_states": crossing_states}


def verify_structure_provenance(schema: dict, aggregate: dict, receipt: dict) -> None:
    if subprocess.run(["git", "rev-parse", "HEAD"], cwd=SEAM, capture_output=True, text=True, check=True).stdout.strip() != schema.get("base_commit"):
        raise RuntimeError("structure smoke base commit mismatch")
    for relative, expected in schema.get("frozen_code_hashes", {}).items():
        path = SIM_ROOT / relative if relative.startswith("common/") else SEAM / relative
        if file_sha256(path) != expected:
            raise RuntimeError(f"structure smoke frozen code mismatch: {relative}")
    params = schema.get("params_authority", {})
    if file_sha256(SIM_ROOT / "params.py") != params.get("sha256"):
        raise RuntimeError("structure smoke params SHA mismatch")
    for scene, expected in params.get("resolved_scenes", {}).items():
        actual = core._resolved_turbulence(scene)
        if (actual["alpha"], actual["beta"]) != (expected.get("alpha"), expected.get("beta")):
            raise RuntimeError(f"structure smoke turbulence snapshot mismatch: {scene}")
    artifact_hashes = receipt.get("artifact_hashes", {})
    for name, path in (
        ("manifest_sha256", TUNING_MANIFEST_PATH),
        ("raw_sha256", TUNING_RAW_PATH),
        ("aggregate_sha256", TUNING_AGGREGATE_PATH),
    ):
        if artifact_hashes.get(name) != file_sha256(path):
            raise RuntimeError(f"structure smoke tuning lineage mismatch: {name}")
    if aggregate.get("selected_tau_by_scene_np") != receipt.get("selected_tau_by_scene_np"):
        raise RuntimeError("structure smoke tuning selection mismatch")


def _atomic_save(data: dict, target: Path, script_name: str) -> None:
    from projects.simulation.common import save_results

    temporary = target.with_suffix(target.suffix + ".tmp")
    save_results(data, str(temporary), script_name)
    os.replace(temporary, target)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    output_dir = validated_temporary_output_dir(args.output_dir)
    schema = load_json(SCHEMA_PATH)
    aggregate = load_json(TUNING_AGGREGATE_PATH)
    receipt = load_json(TUNING_RECEIPT_PATH)
    verify_structure_provenance(schema, aggregate, receipt)
    binding = structure_binding(
        schema, aggregate, receipt,
        schema_sha256=file_sha256(SCHEMA_PATH), receipt_sha256=file_sha256(TUNING_RECEIPT_PATH),
    )
    raw = build_structure_raw(schema, binding)
    validation = validate_structure_raw(raw, binding)
    raw_path = output_dir / "ch4_family_structure_smoke_raw.json"
    _atomic_save(raw, raw_path, "t086_ch4_family_structure_smoke_non_thesis")
    structure_receipt = {
        "schema_version": "t086.family-structure-smoke-receipt.v1",
        "authority": schema["authority"], "base_commit": schema["base_commit"],
        "status": validation["status"], "latent_id": 21999,
        "checks": {
            "finite_schema_pairing": "PASS", "o1_separate_truth_only": "PASS",
            "delta_zero_exact_reference": "PASS", "unreached_crossing_safe": "PASS",
            "scientific_numbers_reported": False,
        },
        "raw_sha256": file_sha256(raw_path),
        "binding": raw["binding"],
    }
    receipt_path = output_dir / "ch4_family_structure_smoke_receipt.json"
    _atomic_save(structure_receipt, receipt_path, "t086_ch4_family_structure_smoke_receipt")
    print(f"STRUCTURE_SMOKE_PASS {receipt_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
