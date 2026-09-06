"""T087 canonical formal raw-only reduction entry and provenance receipt."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
from collections.abc import Mapping
from pathlib import Path

import numpy as np

from ch4_formal_reducer import reduce_raw


SEAM = Path(__file__).resolve().parent
SIM_ROOT = SEAM.parents[1]
MANIFEST_PATH = SEAM / "ch4_scientific_manifest.json"
LOCK_PATH = SEAM / "ch4_formal_execution_lock.json"
RAW_PATH = SEAM / "ch4_formal_raw.json"
AGGREGATE_PATH = SEAM / "ch4_formal_aggregate.json"
RECEIPT_PATH = SEAM / "ch4_formal_receipt.json"
TESTS_PATH = SEAM / "tests/test_ch4_formal_production.py"
FROZEN_SCIENTIFIC_MANIFEST_SHA256 = (
    "417f334844f9092b02bab5d6478381ae7a57e2ff9b4a385ba37707f601521079"
)
BASE_COMMIT = "d3d98c6fc92642e4d6b964d086c1f3bea2018d1d"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _dependency_path(relative: str) -> Path:
    if relative == "projects/simulation/params.py":
        return SIM_ROOT / "params.py"
    return SIM_ROOT / relative if relative.startswith("common/") else SEAM / relative


def current_execution_hashes() -> dict[str, str]:
    return {
        "formal_runner_sha256": file_sha256(SEAM / "run_ch4_formal_production.py"),
        "formal_reducer_sha256": file_sha256(SEAM / "ch4_formal_reducer.py"),
        "formal_reducer_entry_sha256": file_sha256(Path(__file__)),
        "formal_tests_sha256": file_sha256(TESTS_PATH),
    }


def runtime_environment_snapshot() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "platform": platform.platform(),
    }


def verify_environment_authority(
    lock: Mapping[str, object],
    *,
    current_environment_snapshot: Mapping[str, str] | None = None,
) -> None:
    actual = dict(current_environment_snapshot or runtime_environment_snapshot())
    if lock.get("environment_snapshot") != actual:
        raise RuntimeError("execution environment snapshot mismatch")


def verify_provenance(
    manifest: Mapping[str, object],
    lock: Mapping[str, object],
    raw: Mapping[str, object],
) -> tuple[str, str]:
    """Bind the reduction to current on-disk dual-lock authority and raw."""
    verify_environment_authority(lock)
    manifest_sha = file_sha256(MANIFEST_PATH)
    lock_sha = file_sha256(LOCK_PATH)
    if manifest_sha != FROZEN_SCIENTIFIC_MANIFEST_SHA256:
        raise RuntimeError("scientific manifest SHA provenance mismatch")
    if manifest.get("base_commit") != BASE_COMMIT or lock.get("base_commit") != BASE_COMMIT:
        raise RuntimeError("base commit provenance mismatch")
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=SEAM,
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    if head != BASE_COMMIT:
        raise RuntimeError("current Git HEAD differs from frozen base commit")
    if lock.get("scientific_manifest_sha256") != manifest_sha:
        raise RuntimeError("execution lock scientific-manifest binding mismatch")
    if lock.get("execution_hashes") != current_execution_hashes():
        raise RuntimeError("execution lock code/tests binding mismatch")
    frozen = lock.get("frozen_dependency_hashes")
    if not isinstance(frozen, Mapping):
        raise RuntimeError("execution lock frozen dependencies missing")
    expected_frozen = dict(manifest.get("frozen_code_hashes", {}))
    expected_frozen["projects/simulation/params.py"] = manifest.get("params_authority", {}).get("sha256")
    if dict(frozen) != expected_frozen:
        raise RuntimeError("execution lock frozen-dependency set mismatch")
    for relative, expected in frozen.items():
        if file_sha256(_dependency_path(relative)) != expected:
            raise RuntimeError(f"actual frozen dependency mismatch: {relative}")
    if raw.get("purpose") != "canonical_formal_production":
        raise RuntimeError("canonical formal raw purpose mismatch")
    if raw.get("scientific_manifest_sha256") != manifest_sha:
        raise RuntimeError("raw scientific-manifest binding mismatch")
    if raw.get("execution_lock_sha256") != lock_sha:
        raise RuntimeError("raw execution-lock binding mismatch")
    if raw.get("execution_hashes") != lock.get("execution_hashes"):
        raise RuntimeError("raw execution code/tests binding mismatch")
    return manifest_sha, lock_sha


def build_receipt(
    aggregate: Mapping[str, object],
    *,
    manifest_sha256: str,
    lock_sha256: str,
    raw_sha256: str,
    aggregate_sha256: str,
) -> dict[str, object]:
    census = {
        "top_level_latents": 128,
        "scene_latents": 384,
        "actual_cells": 15232,
        "arm_rows": 76160,
        "delta_zero_references": 128,
    }
    if aggregate.get("census") != census:
        raise ValueError("formal aggregate census mismatch")
    grade = aggregate.get("grade")
    if grade not in {"A", "B", "C", "F"}:
        raise ValueError("formal aggregate grade invalid")
    hashes = {
        "scientific_manifest_sha256": manifest_sha256,
        "execution_lock_sha256": lock_sha256,
        "formal_raw_sha256": raw_sha256,
        "formal_aggregate_sha256": aggregate_sha256,
    }
    if not all(isinstance(value, str) and len(value) == 64 for value in hashes.values()):
        raise ValueError("formal receipt artifact hash invalid")
    return {
        "schema_version": "t087.ch4-formal-receipt.v1",
        "authority": "T087/D066/V041",
        "base_commit": BASE_COMMIT,
        "control_epoch": 28,
        "mission_checkpoint": "CP028",
        "terminal": "CH4_FORMAL_REDUCTION_ACCEPTED",
        "grade": grade,
        "chapter_gate": bool(aggregate.get("chapter_gate")),
        "checks": {
            "raw_only_reduction": "PASS",
            "dual_lock_actual_hashes": "PASS",
            "full_128_384_15232_76160_census": "PASS",
            "scene_local_pairing": "PASS",
            "delta_zero_no_duplicate_rows": "PASS",
            "truth_firewall": "PASS",
            "crossing_and_bootstrap_contract": "PASS",
        },
        "census": census,
        "artifact_hashes": hashes,
    }


def _save_temp(data: dict, target: Path, script_name: str) -> Path:
    from projects.simulation.common import save_results

    temporary = target.with_suffix(target.suffix + ".tmp")
    save_results(data, str(temporary), script_name)
    return temporary


def main() -> int:
    if AGGREGATE_PATH.exists() or RECEIPT_PATH.exists():
        raise RuntimeError("formal reduction artifacts already exist; refusing rerun")
    manifest = load_json(MANIFEST_PATH)
    lock = load_json(LOCK_PATH)
    raw = load_json(RAW_PATH)
    manifest_sha, lock_sha = verify_provenance(manifest, lock, raw)
    aggregate = reduce_raw(
        raw,
        manifest,
        lock,
        scientific_manifest_sha256=manifest_sha,
        execution_lock_sha256=lock_sha,
    )
    aggregate_temp = _save_temp(
        aggregate, AGGREGATE_PATH, "t087_ch4_formal_raw_only_aggregate"
    )
    receipt_temp = RECEIPT_PATH.with_suffix(RECEIPT_PATH.suffix + ".tmp")
    try:
        receipt = build_receipt(
            aggregate,
            manifest_sha256=manifest_sha,
            lock_sha256=lock_sha,
            raw_sha256=file_sha256(RAW_PATH),
            aggregate_sha256=file_sha256(aggregate_temp),
        )
        receipt_temp = _save_temp(
            receipt, RECEIPT_PATH, "t087_ch4_formal_acceptance_receipt"
        )
        os.replace(aggregate_temp, AGGREGATE_PATH)
        os.replace(receipt_temp, RECEIPT_PATH)
    except Exception:
        for path in (aggregate_temp, receipt_temp):
            if path.exists():
                path.unlink()
        raise
    print(json.dumps({"terminal": receipt["terminal"], "grade": receipt["grade"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
