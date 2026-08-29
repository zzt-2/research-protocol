"""Write T071 aggregate and receipt from confirmation raw plus manifest only."""

from __future__ import annotations

import hashlib
import inspect
import json
from pathlib import Path

from confirmation_reducer import file_sha256, load_json, reduce_raw
from development import receiver_action


SEAM = Path(__file__).resolve().parent
MANIFEST_PATH = SEAM / "confirmation_manifest.json"
RAW_PATH = SEAM / "confirmation_raw.json"
AGGREGATE_PATH = SEAM / "confirmation_aggregate.json"
RECEIPT_PATH = SEAM / "confirmation_receipt.json"


def _combined_test_hash(test_dir: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(test_dir.glob("test_*.py")):
        digest.update(path.name.encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> int:
    from projects.simulation.common import save_results

    raw = load_json(RAW_PATH)
    manifest = load_json(MANIFEST_PATH)
    manifest_sha256 = file_sha256(MANIFEST_PATH)
    aggregate = reduce_raw(raw, manifest, manifest_sha256)
    save_results(
        aggregate,
        str(AGGREGATE_PATH),
        "t071_scaled_unitary_confirmation_raw_only_reducer",
    )
    signature = tuple(inspect.signature(receiver_action).parameters)
    if signature != ("arm", "x_pilots", "y_pilots", "y_payload", "parameter"):
        raise RuntimeError("deployable receiver truth firewall changed")
    receipt = {
        "schema_version": "t071.scaled-unitary-confirmation-receipt.v1",
        "authority": raw["authority"],
        "base_commit": raw["base_commit"],
        "control_epoch": raw["control_epoch"],
        "mission_checkpoint": raw["mission_checkpoint"],
        "checks": {
            "raw_only_reduction": "PASS",
            "frozen_development_hashes": "PASS",
            "manifest_hash": "PASS",
            "confirmation_only_split": "PASS",
            "seed_arithmetic_and_nonoverlap": "PASS",
            "paired_realization_hashes": "PASS",
            "paired_observation_hashes": "PASS",
            "fixed_arm_parameters": "PASS",
            "finiteness": "PASS",
            "truth_firewall": "PASS (deployable API has no truth input)",
        },
        "population": {
            "cells": len(raw["cells"]),
            "windows_per_cell": manifest["population"]["windows_per_cell"],
            "confirmation_windows": sum(len(cell["windows"]) for cell in raw["cells"]),
        },
        "bootstrap": manifest["bootstrap"],
        "decision": aggregate["decision"],
        "hashes": {
            "manifest_sha256": manifest_sha256,
            "raw_sha256": file_sha256(RAW_PATH),
            "aggregate_sha256": file_sha256(AGGREGATE_PATH),
            "runner_sha256": file_sha256(SEAM / "run_confirmation.py"),
            "reducer_sha256": file_sha256(SEAM / "confirmation_reducer.py"),
            "reducer_cli_sha256": file_sha256(SEAM / "reduce_confirmation.py"),
            "tests_sha256": _combined_test_hash(SEAM / "tests"),
            "frozen_development_hashes": manifest["frozen_development_hashes"],
        },
    }
    save_results(
        receipt,
        str(RECEIPT_PATH),
        "t071_scaled_unitary_confirmation_receipt",
    )
    print(json.dumps(receipt["decision"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
