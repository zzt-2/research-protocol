"""Run the frozen C0-C5 gates and emit an auditable receipt."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import platform
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


SEAM = Path(__file__).resolve().parent
TEST_PATH = SEAM / "tests" / "test_scaled_unitary.py"
RECEIPT_PATH = SEAM / "correctness_receipt.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_tests():
    spec = importlib.util.spec_from_file_location("t069_correctness_tests", TEST_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load frozen correctness tests")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    tests = _load_tests()
    gate_functions = {
        "C0": tests.test_c0_no_noise_exact_recovery,
        "C1": tests.test_c1_balanced_direct_and_post_ls_are_equivalent,
        "C2": tests.test_c2_biunitary_equivariance_and_complex_scale_identities,
        "C3": tests.test_c3_paired_delta_theory_projection_bias_and_residual,
        "C4": tests.test_c4_truth_firewall_is_byte_identical,
        "C5": tests.test_c5_invalid_inputs_fail_closed_without_near_zero_threshold,
    }
    gates: dict[str, dict[str, str]] = {}
    for gate, function in gate_functions.items():
        try:
            function()
            gates[gate] = {"status": "PASS"}
        except Exception:
            gates[gate] = {"status": "FAIL", "traceback": traceback.format_exc()}

    all_pass = all(result["status"] == "PASS" for result in gates.values())
    receipt = {
        "schema_version": "t069.correctness-receipt.v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "authority": "T069/T068/V023",
        "base_commit": "9a31d5d73e87c37417840a66767a20d8df0f8e36",
        "control_epoch": 11,
        "mission_checkpoint": "CP011",
        "repair_rounds_used": 0,
        "gates": gates,
        "all_pass": all_pass,
        "terminal": "CORRECTNESS_PASS" if all_pass else "INVALID_TESTBED",
        "hashes": {
            "manifest_sha256": _sha256(SEAM / "development_manifest.json"),
            "implementation_sha256": _sha256(SEAM / "scaled_unitary.py"),
            "tests_sha256": _sha256(TEST_PATH),
        },
        "environment": {
            "python": sys.version,
            "python_executable": sys.executable,
            "platform": platform.platform(),
            "numpy": np.__version__,
        },
    }
    RECEIPT_PATH.write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2, ensure_ascii=False))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
