"""T086 canonical tuning raw-only reducer and provenance receipt writer."""

from __future__ import annotations

import hashlib
import json
import os
from collections.abc import Mapping
from pathlib import Path

from b2_tuning_reducer import EXPECTED_CELLS, reduce_raw
from run_b2_tuning import (
    MANIFEST_PATH,
    PARAMS_PATH,
    RAW_PATH,
    SEAM,
    _code_path,
    file_sha256,
    load_json,
    truth_firewall_passes,
    verify_authority,
)


AGGREGATE_PATH = SEAM / "b2_tuning_aggregate.json"
RECEIPT_PATH = SEAM / "b2_tuning_receipt.json"
TESTS_PATH = SEAM / "tests/test_direction_scale_family_freeze.py"


def verify_provenance(manifest: dict, raw: dict) -> None:
    """Bind canonical raw to actual on-disk authority; synthetic SHAs are rejected."""
    verify_authority(manifest)
    actual_manifest_sha = file_sha256(MANIFEST_PATH)
    if raw.get("manifest_sha256") != actual_manifest_sha:
        raise RuntimeError("manifest SHA provenance mismatch")
    if raw.get("runner_sha256") != file_sha256(SEAM / "run_b2_tuning.py"):
        raise RuntimeError("generator runner SHA provenance mismatch")
    if raw.get("base_commit") != manifest["base_commit"]:
        raise RuntimeError("base commit provenance mismatch")
    if raw.get("purpose") != "canonical_tuning_non_thesis":
        raise RuntimeError("canonical raw purpose mismatch")
    if raw.get("code_hashes") != manifest["code_hashes"]:
        raise RuntimeError("raw frozen code binding mismatch")
    for relative, expected in manifest["code_hashes"].items():
        if file_sha256(_code_path(relative)) != expected:
            raise RuntimeError(f"actual frozen code SHA mismatch: {relative}")
    params = raw.get("params_authority")
    if not isinstance(params, Mapping):
        raise RuntimeError("params authority provenance missing")
    if params.get("path") != "projects/simulation/params.py" or params.get("sha256") != file_sha256(PARAMS_PATH):
        raise RuntimeError("params actual SHA provenance mismatch")
    if params.get("resolved_scenes") != manifest["resolved_scenes"]:
        raise RuntimeError("params runtime-resolved scene snapshot mismatch")
    if not truth_firewall_passes():
        raise RuntimeError("deployable truth firewall failed")


def build_receipt(
    manifest: Mapping[str, object],
    raw: Mapping[str, object],
    aggregate: Mapping[str, object],
    *,
    artifact_hashes: Mapping[str, str],
) -> dict:
    expected_census = {"scene_latents": 96, "observation_cells": 1152, "arm_rows": 8064}
    if aggregate.get("census") != expected_census:
        raise ValueError("canonical aggregate census mismatch")
    selections = aggregate.get("selected_tau_by_scene_np")
    expected_keys = {f"{scene}_np{n_pilots}" for scene, n_pilots in EXPECTED_CELLS}
    if not isinstance(selections, Mapping) or set(selections) != expected_keys:
        raise ValueError("canonical aggregate selected-tau map is incomplete")
    decision = aggregate.get("decision")
    if not isinstance(decision, Mapping) or decision.get("terminal") not in {
        "CH4_FAMILY_PRODUCTION_FREEZE_READY", "TUNED_BASELINE_DOMINATES_DEVELOPMENT"
    }:
        raise ValueError("canonical aggregate decision terminal is invalid")
    required_hashes = {"manifest_sha256", "raw_sha256", "aggregate_sha256", "receipt_inputs_sha256"}
    if not isinstance(artifact_hashes, Mapping) or not required_hashes.issubset(artifact_hashes):
        raise ValueError("receipt artifact hashes are incomplete")
    for name in required_hashes:
        value = artifact_hashes[name]
        if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
            raise ValueError(f"invalid receipt hash: {name}")
    return {
        "schema_version": "t086.b2-tuning-receipt.v1",
        "authority": manifest["authority"],
        "base_commit": manifest["base_commit"],
        "control_epoch": manifest["control_epoch"],
        "mission_checkpoint": manifest["mission_checkpoint"],
        "purpose": "non-thesis development tuning acceptance",
        "terminal": "CH4_B2_TUNING_ACCEPTED",
        "development_stop": dict(decision),
        "selected_tau_by_scene_np": dict(selections),
        "checks": {
            "raw_only_reduction": "PASS",
            "full_96_1152_8064_census": "PASS",
            "shared_within_scene_pairing": "PASS",
            "cross_scene_pooling_absent": "PASS",
            "all_rows_valid_finite_equal_bits": "PASS",
            "truth_firewall": "PASS",
            "manifest_runner_core_params_hash_binding": "PASS",
            "development_numbers_are_thesis_evidence": False,
        },
        "census": expected_census,
        "artifact_hashes": dict(artifact_hashes),
    }


def _canonical_digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _save_temp(data: dict, target: Path, script_name: str) -> Path:
    from projects.simulation.common import save_results

    temporary = target.with_suffix(target.suffix + ".tmp")
    save_results(data, str(temporary), script_name)
    return temporary


def main() -> int:
    if AGGREGATE_PATH.exists() or RECEIPT_PATH.exists():
        raise RuntimeError("canonical tuning reduction artifacts already exist; refusing rerun")
    manifest = load_json(MANIFEST_PATH)
    raw = load_json(RAW_PATH)
    verify_provenance(manifest, raw)
    manifest_sha = file_sha256(MANIFEST_PATH)
    aggregate = reduce_raw(raw, manifest, manifest_sha)
    aggregate_temp = _save_temp(aggregate, AGGREGATE_PATH, "t086_b2_tuning_raw_only_aggregate")
    receipt_temp = RECEIPT_PATH.with_suffix(RECEIPT_PATH.suffix + ".tmp")
    try:
        artifact_hashes = {
            "manifest_sha256": manifest_sha,
            "raw_sha256": file_sha256(RAW_PATH),
            "aggregate_sha256": file_sha256(aggregate_temp),
            "receipt_inputs_sha256": _canonical_digest({
                "decision": aggregate["decision"],
                "selected_tau_by_scene_np": aggregate["selected_tau_by_scene_np"],
                "census": aggregate["census"],
            }),
            "generator_runner_sha256": raw["runner_sha256"],
            "reducer_core_sha256": file_sha256(SEAM / "b2_tuning_reducer.py"),
            "reducer_entry_sha256": file_sha256(Path(__file__)),
            "tests_sha256": file_sha256(TESTS_PATH),
            "params_sha256": file_sha256(PARAMS_PATH),
            **{f"frozen_{name}": value for name, value in manifest["code_hashes"].items()},
        }
        receipt = build_receipt(manifest, raw, aggregate, artifact_hashes=artifact_hashes)
        receipt_temp = _save_temp(receipt, RECEIPT_PATH, "t086_b2_tuning_acceptance_receipt")
        os.replace(aggregate_temp, AGGREGATE_PATH)
        os.replace(receipt_temp, RECEIPT_PATH)
    except Exception:
        for path in (aggregate_temp, receipt_temp):
            if path.exists():
                path.unlink()
        raise
    print(json.dumps({"terminal": receipt["terminal"], "development_stop": receipt["development_stop"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
