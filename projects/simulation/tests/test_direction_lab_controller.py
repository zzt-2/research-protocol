"""RED tests for the first Direction Lab governance pilot controller.

These tests intentionally describe actions that must be blocked.  The B5
sandbox is referenced as a read-only historical input; fixtures are synthetic
so the pilot cannot alter or promote research results.
"""

import json
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
            "baseline.fft_foe": {
                "component_id": "baseline.fft_foe",
                "fingerprint": "sha-baseline-1",
                "status": "canonical",
            },
            "method.b5_short_time": {
                "component_id": "method.b5_short_time",
                "fingerprint": "sha-method-1",
                "status": "canonical",
            },
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
        controller.check(
            manifest(evidence_status="PARTIAL", promotion_allowed=True),
            action="PROMOTE",
        )


def test_missing_or_unknown_evidence_cannot_be_promoted(controller):
    for evidence_status in (None, "NONE", "UNKNOWN"):
        values = {} if evidence_status is None else {"evidence_status": evidence_status}
        candidate = manifest(promotion_allowed=True, **values)
        if evidence_status is None:
            candidate.pop("evidence_status")
        with pytest.raises(GovernanceViolation, match="evidence"):
            controller.check(candidate, action="PROMOTE")


def test_unknown_action_is_blocked(controller):
    with pytest.raises(GovernanceViolation, match="action"):
        controller.check(manifest(), action="DELETE_EVIDENCE")


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


def test_baseline_fingerprint_change_marks_old_result_stale(controller):
    stale = controller.check(
        manifest(baseline_fingerprint="sha-baseline-2"),
        action="REUSE_RESULT",
    )
    assert stale["result_status"] == "STALE"
    assert stale["blocked"] is True
    assert controller.audit_events[-1]["repair"] == "mark_stale"


def test_both_fingerprints_drift_stale_reuse_is_not_executed(controller):
    called = []
    with pytest.raises(GovernanceViolation, match="STALE|blocked"):
        controller.execute(
            manifest(
                baseline_fingerprint="sha-baseline-2",
                component_fingerprint="sha-method-2",
            ),
            action="REUSE_RESULT",
            operation=lambda: called.append("reused"),
        )
    assert called == []


def test_guarded_entry_does_not_call_operation_when_blocked(controller):
    called = []
    with pytest.raises(GovernanceViolation):
        controller.execute(
            None,
            action="RUN",
            operation=lambda: called.append("ran"),
        )
    assert called == []


def test_guarded_entry_calls_operation_only_after_validation(controller):
    called = []
    envelope = controller.execute(
        manifest(),
        action="RUN",
        operation=lambda: called.append("ran") or "ok",
    )
    assert envelope["result"] == "ok"
    assert called == ["ran"]


def test_guarded_entry_does_not_execute_stale_reuse(controller):
    called = []
    with pytest.raises(GovernanceViolation, match="blocked|STALE"):
        controller.execute(
            manifest(component_fingerprint="sha-old"),
            action="REUSE_RESULT",
            operation=lambda: called.append("reused"),
        )
    assert called == []


def test_noncanonical_reuse_is_stale_and_not_executed(tmp_path):
    guarded = GovernanceController(
        registry={
            "baseline.fft_foe": {"fingerprint": "sha-baseline-1", "status": "canonical"},
            "method.b5_short_time": {"fingerprint": "sha-method-1", "status": "legacy"},
        },
        audit_path=tmp_path / "audit.jsonl",
    )
    called = []
    with pytest.raises(GovernanceViolation, match="STALE|blocked"):
        guarded.execute(
            manifest(),
            action="REUSE_RESULT",
            operation=lambda: called.append("reused"),
        )
    assert called == []


def test_noncanonical_registry_component_cannot_run(tmp_path):
    guarded = GovernanceController(
        registry={
            "baseline.fft_foe": {"fingerprint": "sha-baseline-1", "status": "canonical"},
            "method.b5_short_time": {"fingerprint": "sha-method-1", "status": "legacy"},
        },
        audit_path=tmp_path / "audit.jsonl",
    )
    with pytest.raises(GovernanceViolation, match="status"):
        guarded.check(manifest(), action="RUN")


def test_promotion_requires_explicit_permission(controller):
    candidate = manifest(evidence_status="FULL")
    candidate.pop("promotion_allowed", None)
    with pytest.raises(GovernanceViolation, match="promotion"):
        controller.check(candidate, action="PROMOTE")

    allowed = controller.check(
        manifest(evidence_status="FULL", promotion_allowed=True),
        action="PROMOTE",
    )
    assert allowed["blocked"] is False


def test_real_b5_sandbox_manifest_runs_only_through_guarded_entry(controller):
    manifest_path = (
        Path(__file__).parents[1]
        / "verify"
        / "direction_lab_pilot"
        / "b5_pilot_manifest.json"
    )
    real_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    called = []
    envelope = controller.execute(
        real_manifest,
        action="RUN",
        operation=lambda: called.append("ran") or "ok",
    )
    assert envelope["result"] == "ok"
    assert called == ["ran"]


def test_real_b5_sandbox_manifest_cannot_be_promoted(controller):
    manifest_path = (
        Path(__file__).parents[1]
        / "verify"
        / "direction_lab_pilot"
        / "b5_pilot_manifest.json"
    )
    real_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    called = []
    with pytest.raises(GovernanceViolation, match="sandbox|promotion"):
        controller.execute(
            real_manifest,
            action="PROMOTE",
            operation=lambda: called.append("promoted"),
        )
    assert called == []


def test_audit_survives_new_controller_instance_and_repeated_violation(tmp_path):
    audit_path = tmp_path / "audit.jsonl"
    registry = {
        "baseline.fft_foe": {"fingerprint": "sha-baseline-1", "status": "canonical"},
        "method.b5_short_time": {"fingerprint": "sha-method-1", "status": "canonical"},
    }
    first = GovernanceController(registry=registry, audit_path=audit_path)
    for _ in range(2):
        with pytest.raises(GovernanceViolation):
            first.check(None, action="RUN")

    recovered = GovernanceController(registry=registry, audit_path=audit_path)
    recovered.check(manifest(), action="RUN")

    events = [json.loads(line) for line in audit_path.read_text(encoding="utf-8").splitlines()]
    assert [event["blocked"] for event in events] == [True, True, False]


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
