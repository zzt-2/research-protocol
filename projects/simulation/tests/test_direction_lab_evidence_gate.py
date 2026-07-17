"""Behavior tests for Direction Lab decision receipts and evidence admission."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from verify.direction_lab_pilot.controller import (
    EvidenceGate,
    GovernanceController,
    GovernanceViolation,
)


@pytest.fixture
def registry():
    return {
        "baseline.fft_foe": {
            "fingerprint": "sha-baseline-1",
            "status": "canonical",
        },
        "method.b5_short_time": {
            "fingerprint": "sha-method-1",
            "status": "canonical",
        },
    }


@pytest.fixture
def audit_path(tmp_path: Path) -> Path:
    return tmp_path / "audit.jsonl"


@pytest.fixture
def controller(registry, audit_path: Path) -> GovernanceController:
    return GovernanceController(registry=registry, audit_path=audit_path)


def manifest(**overrides):
    value = {
        "run_id": "pilot-b5-receipt-001",
        "baseline_id": "baseline.fft_foe",
        "component_id": "method.b5_short_time",
        "baseline_fingerprint": "sha-baseline-1",
        "component_fingerprint": "sha-method-1",
        "evidence_status": "FULL",
        "state": "BOARD_READY",
        "result_status": "VALID",
        "sandbox_only": True,
        "promotion_allowed": False,
    }
    value.update(overrides)
    return value


def canonical_hash(value) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def test_allowed_decision_receipt_binds_required_fields(controller):
    proposed = manifest()
    checked = controller.check(proposed, action="RUN")

    receipt = checked["decision_receipt"]
    assert receipt["decision_id"]
    assert receipt["run_id"] == proposed["run_id"]
    assert receipt["action"] == "RUN"
    assert receipt["manifest_hash"] == canonical_hash(proposed)
    assert receipt["allowed"] is True
    assert receipt["blocked"] is False


def test_blocked_decision_still_records_bound_receipt(controller):
    proposed = manifest(state="PROBED")
    with pytest.raises(GovernanceViolation, match="BOARD_READY"):
        controller.check(proposed, action="GO")

    receipt = controller.audit_events[-1]["decision_receipt"]
    assert receipt["decision_id"]
    assert receipt["run_id"] == proposed["run_id"]
    assert receipt["action"] == "GO"
    assert receipt["manifest_hash"] == canonical_hash(proposed)
    assert receipt["allowed"] is False
    assert receipt["blocked"] is True


def test_execute_returns_result_envelope_with_receipt(controller):
    proposed = manifest()
    envelope = controller.execute(
        proposed,
        action="RUN",
        operation=lambda: {"signal": "synthetic-positive"},
    )

    assert envelope["result"] == {"signal": "synthetic-positive"}
    assert envelope["manifest"] == proposed
    assert envelope["decision_receipt"]["allowed"] is True
    assert envelope["decision_receipt"]["action"] == "RUN"


@pytest.fixture
def destinations(tmp_path: Path):
    return {
        "evidence_ledger": tmp_path / "evidence-ledger.jsonl",
        "promotion_board": tmp_path / "promotion-board.jsonl",
        "formal_materials": tmp_path / "formal-materials.jsonl",
    }


@pytest.fixture
def gate(audit_path: Path, destinations) -> EvidenceGate:
    return EvidenceGate(audit_path=audit_path, destinations=destinations)


def test_valid_guarded_result_enters_evidence_ledger(
    controller,
    gate: EvidenceGate,
    destinations,
):
    envelope = controller.execute(
        manifest(),
        action="RUN",
        operation=lambda: {"signal": "synthetic-positive"},
    )

    verdict = gate.submit(envelope, destination="evidence_ledger")

    assert verdict["accepted"] is True
    assert verdict["artifact_status"] == "ACCEPTED"
    assert verdict["trust_status"] == "TRUSTED"
    lines = destinations["evidence_ledger"].read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1


def test_bypass_artifact_is_orphan_untrusted_and_enters_no_destination(
    gate: EvidenceGate,
    destinations,
):
    bypass = {
        "result": {"signal": "beautiful-but-bypassed"},
        "manifest": manifest(),
    }

    for destination in destinations:
        verdict = gate.submit(bypass, destination=destination)
        assert verdict["accepted"] is False
        assert verdict["artifact_status"] == "ORPHAN"
        assert verdict["trust_status"] == "UNTRUSTED"

    assert all(not path.exists() for path in destinations.values())


def test_forged_or_manifest_mismatched_receipt_is_untrusted(
    controller,
    gate: EvidenceGate,
    destinations,
):
    envelope = controller.execute(
        manifest(),
        action="RUN",
        operation=lambda: {"signal": "synthetic"},
    )
    forged = dict(envelope)
    forged["decision_receipt"] = dict(envelope["decision_receipt"])
    forged["decision_receipt"]["decision_id"] = "decision-forged"
    forged_verdict = gate.submit(forged, destination="evidence_ledger")

    mutated = dict(envelope)
    mutated["manifest"] = dict(envelope["manifest"], component_fingerprint="sha-mutated")
    mutated_verdict = gate.submit(mutated, destination="evidence_ledger")

    assert forged_verdict["trust_status"] == "UNTRUSTED"
    assert mutated_verdict["trust_status"] == "UNTRUSTED"
    assert not destinations["evidence_ledger"].exists()


def test_run_receipt_cannot_enter_promotion_or_formal_materials(
    controller,
    gate: EvidenceGate,
    destinations,
):
    envelope = controller.execute(
        manifest(),
        action="RUN",
        operation=lambda: {"signal": "synthetic"},
    )

    for destination in ("promotion_board", "formal_materials"):
        verdict = gate.submit(envelope, destination=destination)
        assert verdict["accepted"] is False
        assert verdict["artifact_status"] == "BLOCKED"

    assert not destinations["promotion_board"].exists()
    assert not destinations["formal_materials"].exists()


def test_only_eligible_promote_receipt_enters_formal_materials(
    controller,
    gate: EvidenceGate,
    destinations,
):
    promotable = manifest(
        sandbox_only=False,
        promotion_allowed=True,
        evidence_status="FULL",
        state="BOARD_READY",
    )
    envelope = controller.execute(
        promotable,
        action="PROMOTE",
        operation=lambda: {"claim": "synthetic-governance-fixture"},
    )

    verdict = gate.submit(envelope, destination="formal_materials")

    assert verdict["accepted"] is True
    assert destinations["formal_materials"].exists()


def test_later_stale_decision_invalidates_earlier_result_receipt(
    controller,
    gate: EvidenceGate,
    destinations,
):
    old_envelope = controller.execute(
        manifest(),
        action="RUN",
        operation=lambda: {"signal": "old-result"},
    )
    controller.check(
        manifest(
            baseline_fingerprint="sha-baseline-old",
            component_fingerprint="sha-method-old",
        ),
        action="REUSE_RESULT",
    )

    verdict = gate.submit(old_envelope, destination="evidence_ledger")

    assert verdict["accepted"] is False
    assert verdict["artifact_status"] == "STALE"
    assert not destinations["evidence_ledger"].exists()


def test_result_mutation_after_execute_is_untrusted(
    controller,
    gate: EvidenceGate,
    destinations,
):
    envelope = controller.execute(
        manifest(),
        action="RUN",
        operation=lambda: {"signal": "controller-result"},
    )
    envelope["result"] = {"signal": "forged-after-execute"}

    verdict = gate.submit(envelope, destination="evidence_ledger")

    assert verdict["accepted"] is False
    assert verdict["trust_status"] == "UNTRUSTED"
    assert not destinations["evidence_ledger"].exists()


def test_check_only_receipt_cannot_be_promoted_into_result_envelope(
    controller,
    gate: EvidenceGate,
    destinations,
):
    checked = controller.check(manifest(), action="RUN")
    forged = {
        "manifest": manifest(),
        "decision_receipt": checked["decision_receipt"],
        "result": {"signal": "check-only-forged"},
    }

    verdict = gate.submit(forged, destination="evidence_ledger")

    assert verdict["accepted"] is False
    assert verdict["trust_status"] == "UNTRUSTED"
    assert not destinations["evidence_ledger"].exists()


def test_same_receipt_cannot_be_admitted_twice(
    controller,
    gate: EvidenceGate,
    destinations,
):
    envelope = controller.execute(
        manifest(),
        action="RUN",
        operation=lambda: {"signal": "one-shot"},
    )
    first = gate.submit(envelope, destination="evidence_ledger")
    second = gate.submit(envelope, destination="evidence_ledger")

    assert first["accepted"] is True
    assert second["accepted"] is False
    assert second["artifact_status"] == "REPLAY"
    assert len(destinations["evidence_ledger"].read_text(encoding="utf-8").splitlines()) == 1
