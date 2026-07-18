from __future__ import annotations

import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "tools" / "u25_sandbox_preflight.py"
spec = importlib.util.spec_from_file_location("direction_lab_u25_sandbox_preflight", MODULE_PATH)
assert spec and spec.loader
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)


def test_current_standard_cma_chain_is_explicitly_blocked_for_u25() -> None:
    report = preflight.evaluate_u25_readiness()
    assert report["status"] == "P01_BLOCKED"
    assert "ACTION_EFFECT_NOT_OBSERVABLE" in report["blockers"]
    assert "STATE_SNAPSHOT_MISSING" in report["blockers"]
    assert "RUNNER_U24_HARDCODED" in report["blockers"]
    assert report["trace_adapter"]["status"] == "PASS"
    assert "B003-20260718-live/artifacts/result.json" in report["trace_adapter"]["input_source"]
    assert report["formal_performance_run"] is False


def test_blocked_report_keeps_reusable_assets_and_next_candidate() -> None:
    report = preflight.evaluate_u25_readiness()
    assert "standard_cma_blind_trace" in report["reusable_assets"]
    assert "P02/U10" in report["next_candidate"]
    assert report["sandbox_queue_created"] is False
