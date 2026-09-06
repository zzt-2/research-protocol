"""Freeze the T086 scientific manifest from accepted on-disk tuning artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path

from family_freeze_contract import EXPECTED_TAU_KEYS, TAU_GRID, build_scientific_manifest
from reduce_b2_tuning import verify_provenance


SEAM = Path(__file__).resolve().parent
SIM_ROOT = SEAM.parents[1]
SCHEMA_PATH = SEAM / "ch4_scientific_manifest_schema.json"
MANIFEST_PATH = SEAM / "b2_tuning_manifest.json"
RAW_PATH = SEAM / "b2_tuning_raw.json"
AGGREGATE_PATH = SEAM / "b2_tuning_aggregate.json"
RECEIPT_PATH = SEAM / "b2_tuning_receipt.json"
FINAL_PATH = SEAM / "ch4_scientific_manifest.json"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_tau_arguments(values: list[str]) -> dict[str, float]:
    parsed: dict[str, float] = {}
    for value in values:
        if not isinstance(value, str) or "=" not in value:
            raise ValueError("each --tau must be KEY=VALUE")
        key, raw_tau = value.split("=", 1)
        if key in parsed:
            raise ValueError(f"duplicate --tau key: {key}")
        try:
            tau = float(raw_tau)
        except ValueError as error:
            raise ValueError(f"invalid tau for {key}") from error
        parsed[key] = tau
    if set(parsed) != EXPECTED_TAU_KEYS:
        raise ValueError("--tau must supply exactly all 12 scene x Np keys")
    if any(value not in TAU_GRID for value in parsed.values()):
        raise ValueError("--tau value is outside the frozen grid")
    return {key: parsed[key] for key in sorted(parsed)}


def _verify_schema_authority(schema: dict, manifest: dict) -> None:
    if schema.get("base_commit") != manifest.get("base_commit"):
        raise RuntimeError("scientific schema/base authority mismatch")
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=SEAM, capture_output=True, text=True, check=True
    ).stdout.strip()
    if schema.get("base_commit") != head:
        raise RuntimeError("scientific schema current base mismatch")
    if schema.get("frozen_code_hashes") != manifest.get("code_hashes"):
        raise RuntimeError("scientific schema frozen code map mismatch")
    for relative, expected in schema["frozen_code_hashes"].items():
        path = SIM_ROOT / relative if relative.startswith("common/") else SEAM / relative
        if file_sha256(path) != expected:
            raise RuntimeError(f"scientific schema actual code SHA mismatch: {relative}")
    params = schema.get("params_authority", {})
    if params.get("path") != "projects/simulation/params.py" or file_sha256(SIM_ROOT / "params.py") != params.get("sha256"):
        raise RuntimeError("scientific schema actual params SHA mismatch")
    if params.get("resolved_scenes") != manifest.get("resolved_scenes"):
        raise RuntimeError("scientific schema turbulence snapshot mismatch")


def verify_actual_tuning_lineage(supplied_selections: dict[str, float]) -> dict[str, str]:
    manifest = load_json(MANIFEST_PATH)
    raw = load_json(RAW_PATH)
    aggregate = load_json(AGGREGATE_PATH)
    receipt = load_json(RECEIPT_PATH)
    schema = load_json(SCHEMA_PATH)
    verify_provenance(manifest, raw)
    _verify_schema_authority(schema, manifest)

    actual = {
        "b2_tuning_manifest_sha256": file_sha256(MANIFEST_PATH),
        "b2_tuning_raw_sha256": file_sha256(RAW_PATH),
        "b2_tuning_aggregate_sha256": file_sha256(AGGREGATE_PATH),
        "b2_tuning_receipt_sha256": file_sha256(RECEIPT_PATH),
    }
    receipt_hashes = receipt.get("artifact_hashes", {})
    expected_receipt_bindings = {
        "manifest_sha256": actual["b2_tuning_manifest_sha256"],
        "raw_sha256": actual["b2_tuning_raw_sha256"],
        "aggregate_sha256": actual["b2_tuning_aggregate_sha256"],
    }
    if any(receipt_hashes.get(key) != value for key, value in expected_receipt_bindings.items()):
        raise RuntimeError("actual tuning artifact SHA does not match receipt lineage")
    if aggregate.get("manifest_sha256") != actual["b2_tuning_manifest_sha256"]:
        raise RuntimeError("aggregate manifest SHA lineage mismatch")
    if receipt.get("terminal") != "CH4_B2_TUNING_ACCEPTED":
        raise RuntimeError("tuning receipt is not accepted")
    if aggregate.get("decision", {}).get("terminal") != "CH4_FAMILY_PRODUCTION_FREEZE_READY":
        raise RuntimeError("development stop does not allow scientific manifest freeze")
    aggregate_tau = aggregate.get("selected_tau_by_scene_np")
    receipt_tau = receipt.get("selected_tau_by_scene_np")
    if aggregate_tau != receipt_tau or aggregate_tau != supplied_selections:
        raise RuntimeError("aggregate/receipt/supplied tau three-way identity failed")
    if set(aggregate_tau or {}) != EXPECTED_TAU_KEYS:
        raise RuntimeError("accepted tuning map does not contain exactly 12 entries")
    return actual


def build_final_manifest(supplied_selections: dict[str, float]) -> dict:
    lineage = verify_actual_tuning_lineage(supplied_selections)
    schema = load_json(SCHEMA_PATH)
    built = build_scientific_manifest(
        schema, supplied_selections,
        tuning_manifest_sha256=lineage["b2_tuning_manifest_sha256"],
        tuning_raw_sha256=lineage["b2_tuning_raw_sha256"],
        tuning_aggregate_sha256=lineage["b2_tuning_aggregate_sha256"],
        tuning_receipt_sha256=lineage["b2_tuning_receipt_sha256"],
        tuning_terminal="CH4_B2_TUNING_ACCEPTED",
    )
    built["scientific_contract_schema_sha256"] = file_sha256(SCHEMA_PATH)
    built["execution_lock_interface"]["scientific_manifest_binding_rule"] = (
        "T087 execution lock must bind the exact on-disk ch4_scientific_manifest.json SHA-256"
    )
    return built


def _atomic_save(data: dict, target: Path) -> None:
    from projects.simulation.common import save_results

    temporary = target.with_suffix(target.suffix + ".tmp")
    save_results(data, str(temporary), "t086_ch4_scientific_manifest_freeze")
    os.replace(temporary, target)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tau", action="append", required=True)
    args = parser.parse_args()
    if FINAL_PATH.exists():
        raise RuntimeError("scientific manifest already exists; refusing refreeze")
    selections = parse_tau_arguments(args.tau)
    built = build_final_manifest(selections)
    _atomic_save(built, FINAL_PATH)
    print(f"SCIENTIFIC_MANIFEST_FROZEN sha256={file_sha256(FINAL_PATH)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
