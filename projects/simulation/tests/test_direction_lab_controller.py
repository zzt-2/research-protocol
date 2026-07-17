"""RED tests for the first Direction Lab governance pilot controller.

These tests intentionally describe actions that must be blocked.  The B5
sandbox is referenced as a read-only historical input; fixtures are synthetic
so the pilot cannot alter or promote research results.
"""

from pathlib import Path

import pytest

from verify.direction_lab_pilot.controller import (
    GovernanceController,
    GovernanceViolation,
)


@pytest.fixture
def controller(tmp_path: Path) -> GovernanceController:
    return GovernanceController(
        registry={
            "baseline.fft_foe": {"component_id": "baseline.fft_foe", "fingerprint": "sha-baseline-1"},
            "method.b5_short_time": {"component_id": "method.b5_short_time", "fingerprint": "sha-method-1"},
        },
        audit_path=tmp_path / "violations.jsonl",
    )


def manifest(**overrides):
    value = {
        "run_id": "pilot-b5-001",
        "baseline_id": "baseline.fft_foe",
        "component_id": "method.b5_short_time",
        "baseline_fingerprint": "sha-baseline-1",
        "component_fingerprint": "sha-method-1",
        "evidence_status": "FULL",
        "state": "BOARD_READY",
        "result_status": "VALID",
    }
    value.update(overrides)
    return value


def test_missing_manifest_is_blocked_and_audited(controller):
    with pytest.raises(GovernanceViolation, match="manifest"):
        controller.check(None, action="RUN")
    event = controller.audit_events[-1]
    assert event["blocked"] is True
    assert event["original_action"] == "RUN"


def test_missing_run_id_is_blocked(controller):
    with pytest.raises(GovernanceViolation, match="run_id"):
        controller.check(manifest(run_id=""), action="RUN")


def test_unknown_or_mismatched_component_is_blocked(controller):
    with pytest.raises(GovernanceViolation, match="component"):
        controller.check(manifest(component_id="method.unknown"), action="RUN")
    with pytest.raises(GovernanceViolation, match="fingerprint"):
        controller.check(manifest(component_fingerprint="sha-old"), action="RUN")


def test_component_fingerprint_change_blocks_new_run(controller):
    with pytest.raises(GovernanceViolation, match="fingerprint"):
        controller.check(manifest(component_fingerprint="sha-old"), action="RUN")


def test_go_or_kill_before_board_ready_is_blocked(controller):
    for action in ("GO", "KILL"):
        with pytest.raises(GovernanceViolation, match="BOARD_READY"):
            controller.check(manifest(state="PROBED"), action=action)


def test_partial_evidence_cannot_be_promoted(controller):
    with pytest.raises(GovernanceViolation, match="PARTIAL"):
        controller.check(manifest(evidence_status="PARTIAL"), action="PROMOTE")


def test_component_change_marks_old_result_stale(controller):
    checked = controller.check(manifest(), action="RUN")
    assert checked["result_status"] == "VALID"
    stale = controller.check(
        manifest(component_fingerprint="sha-method-2", result_status="VALID"),
        action="REUSE_RESULT",
    )
    assert stale["result_status"] == "STALE"
    assert stale["blocked"] is True
    assert controller.audit_events[-1]["repair"] == "mark_stale"


def test_valid_run_is_allowed_without_silent_repair(controller):
    checked = controller.check(manifest(), action="RUN")
    assert checked["blocked"] is False
    assert controller.audit_events[-1]["blocked"] is False


def test_every_decision_is_represented_as_parseable_jsonl(controller):
    controller.check(manifest(), action="RUN")
    with pytest.raises(GovernanceViolation):
        controller.check(None, action="RUN")
    lines = controller.audit_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert all('"original_action": "RUN"' in line for line in lines)
    assert all('"blocked":' in line for line in lines)
