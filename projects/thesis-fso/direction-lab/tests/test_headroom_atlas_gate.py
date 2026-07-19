"""TDD tests for the unique Headroom Atlas preflight/assessment gate.

The gate is the ONLY entrypoint that may run an Atlas cell or write an Atlas
state summary. It must:

- enforce the claim-scope validator and consume a fresh PASS receipt bound to
  the exact assessment SHA and validator SHA;
- block when the receipt is missing, stale, hash-mismatched, or when the
  assessment FAILs the validator;
- block a direct runner call that bypasses the gate;
- record an append-only audit log and never silently overwrite an old receipt.

These tests are written first and are expected to fail until the gate module
exists.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import pytest
import yaml


LAB_ROOT = Path(__file__).resolve().parents[1]
GATE_PATH = (
    LAB_ROOT / "scout" / "P03-U19-residual-headroom" / "headroom-atlas" / "atlas_gate.py"
)
VALIDATOR_PATH = LAB_ROOT / "tools" / "validate_claim_scope.py"
P03_ASSESSMENT = (
    LAB_ROOT / "scout" / "P03-U19-residual-headroom" / "claim-scope-assessment.v1.yaml"
)
BATCH_PLAN_V2 = LAB_ROOT / "batch-plan.v2.yaml"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def gate():
    return _load_module("direction_lab_headroom_atlas_gate", GATE_PATH)


@pytest.fixture(scope="module")
def validator():
    return _load_module("direction_lab_claim_scope_validator", VALIDATOR_PATH)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _receipt_payload(assessment_path: Path, *, status: str = "PASS") -> dict:
    payload = {
        "schema_version": "direction-lab.claim-scope-validation-receipt.v1",
        "status": status,
        "assessment_sha256": _sha(assessment_path),
        "validator_sha256": _sha(VALIDATOR_PATH),
        "validator_version": "direction-lab.claim-scope.v1",
    }
    receipt_id = hashlib.sha256(
        ("\x00".join([payload["status"], payload["assessment_sha256"], payload["validator_sha256"]])).encode("utf-8")
    ).hexdigest()
    return {**payload, "receipt_id": receipt_id}


def _write_receipt(path: Path, receipt: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(receipt, sort_keys=True), encoding="utf-8")


def _make_workspace(tmp_path: Path, *, write_receipt: bool = True) -> dict:
    assessment = tmp_path / "assessment.yaml"
    assessment.write_bytes(P03_ASSESSMENT.read_bytes())
    receipt_path = tmp_path / "receipts" / "claim-scope.yaml"
    if write_receipt:
        _write_receipt(receipt_path, _receipt_payload(assessment))
    audit_path = tmp_path / "audit" / "atlas-audit.jsonl"
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    return {
        "root": tmp_path,
        "assessment": assessment,
        "receipt": receipt_path,
        "audit": audit_path,
    }


# ---------------------------------------------------------------------------
# 1. Happy path: a fresh PASS receipt bound to the exact assessment and
#    validator hashes authorizes a single Atlas entrypoint run and writes an
#    audit entry.
# ---------------------------------------------------------------------------


def test_fresh_pass_receipt_bound_to_exact_hashes_authorizes_run(gate, tmp_path):
    ws = _make_workspace(tmp_path)
    token = gate.authorize(
        assessment_path=ws["assessment"],
        receipt_path=ws["receipt"],
        audit_path=ws["audit"],
        batch_plan_path=BATCH_PLAN_V2,
    )
    assert token.authorized is True
    assert token.assessment_sha256 == _sha(ws["assessment"])
    assert token.validator_sha256 == _sha(VALIDATOR_PATH)
    assert token.receipt_id  # non-empty
    # audit log now contains exactly one JSON-line record of this authorization
    lines = [json.loads(line) for line in ws["audit"].read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(lines) == 1
    assert lines[0]["decision"] == "AUTHORIZED"
    assert lines[0]["receipt_id"] == token.receipt_id


# ---------------------------------------------------------------------------
# 2. Blocking: missing receipt, stale receipt (assessment edited after
#    issuance), wrong validator SHA, FAIL status, and a FAILing assessment.
# ---------------------------------------------------------------------------


def test_missing_receipt_blocks_run(gate, tmp_path):
    ws = _make_workspace(tmp_path, write_receipt=False)
    token = gate.authorize(
        assessment_path=ws["assessment"],
        receipt_path=ws["receipt"],
        audit_path=ws["audit"],
        batch_plan_path=BATCH_PLAN_V2,
    )
    assert token.authorized is False
    assert "receipt" in token.reason.lower()
    # a blocked attempt must still append an audit record so it cannot be hidden
    lines = [json.loads(line) for line in ws["audit"].read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(lines) == 1
    assert lines[0]["decision"] == "BLOCKED"


def test_stale_receipt_after_assessment_edit_blocks_run(gate, tmp_path):
    ws = _make_workspace(tmp_path)
    # edit the assessment after the receipt was issued -> assessment SHA drifts
    edited = yaml.safe_load(ws["assessment"].read_text(encoding="utf-8"))
    edited["adjudicated_candidate_status"] = "P03_DOMAIN_ADEQUACY_UNRESOLVED_EDITED"
    ws["assessment"].write_text(yaml.safe_dump(edited, sort_keys=False), encoding="utf-8")
    token = gate.authorize(
        assessment_path=ws["assessment"],
        receipt_path=ws["receipt"],
        audit_path=ws["audit"],
        batch_plan_path=BATCH_PLAN_V2,
    )
    assert token.authorized is False
    assert "assessment" in token.reason.lower() and "sha" in token.reason.lower()


def test_wrong_validator_sha_blocks_run(gate, tmp_path):
    ws = _make_workspace(tmp_path)
    receipt = yaml.safe_load(ws["receipt"].read_text(encoding="utf-8"))
    receipt["validator_sha256"] = "0" * 64
    ws["receipt"].write_text(yaml.safe_dump(receipt, sort_keys=True), encoding="utf-8")
    token = gate.authorize(
        assessment_path=ws["assessment"],
        receipt_path=ws["receipt"],
        audit_path=ws["audit"],
        batch_plan_path=BATCH_PLAN_V2,
    )
    assert token.authorized is False
    assert "validator" in token.reason.lower()


def test_failed_receipt_status_blocks_run(gate, tmp_path):
    ws = _make_workspace(tmp_path)
    receipt = yaml.safe_load(ws["receipt"].read_text(encoding="utf-8"))
    receipt["status"] = "FAIL"
    ws["receipt"].write_text(yaml.safe_dump(receipt, sort_keys=True), encoding="utf-8")
    token = gate.authorize(
        assessment_path=ws["assessment"],
        receipt_path=ws["receipt"],
        audit_path=ws["audit"],
        batch_plan_path=BATCH_PLAN_V2,
    )
    assert token.authorized is False
    assert "pass" in token.reason.lower()


def test_assessment_that_fails_validator_blocks_even_with_a_fake_pass_receipt(gate, validator, tmp_path):
    """A PASS receipt alone must not be trusted; the gate re-runs the validator
    on the exact assessment bytes and blocks when the assessment FAILs."""
    ws = _make_workspace(tmp_path)
    # build an assessment that the validator will reject (missing a verdict level)
    bad = yaml.safe_load(ws["assessment"].read_text(encoding="utf-8"))
    bad["verdicts"].pop("FAMILY")
    ws["assessment"].write_text(yaml.safe_dump(bad, sort_keys=False), encoding="utf-8")
    # write a PASS receipt that *claims* to match the (bad) assessment bytes
    _write_receipt(ws["receipt"], _receipt_payload(ws["assessment"]))
    token = gate.authorize(
        assessment_path=ws["assessment"],
        receipt_path=ws["receipt"],
        audit_path=ws["audit"],
        batch_plan_path=BATCH_PLAN_V2,
    )
    assert token.authorized is False
    assert "assessment" in token.reason.lower() and "fail" in token.reason.lower()


# ---------------------------------------------------------------------------
# 3. Direct runner bypass: the gate exposes a guarded runner hook; calling the
#    cell runner without first obtaining an authorization token raises.
# ---------------------------------------------------------------------------


def test_runner_hook_requires_authorization_token(gate, tmp_path):
    ws = _make_workspace(tmp_path)
    runner = gate.AtlasRunner(cell_runner=lambda *_a, **_kw: {"ran": True})
    with pytest.raises(gate.UnauthorizedAtlasRun):
        runner.run_cell(cell_id="qpsk-snr20", payload={}, audit_path=ws["audit"])
    # after authorizing, the same runner accepts the token
    token = gate.authorize(
        assessment_path=ws["assessment"],
        receipt_path=ws["receipt"],
        audit_path=ws["audit"],
        batch_plan_path=BATCH_PLAN_V2,
    )
    result = runner.run_cell(cell_id="qpsk-snr20", payload={}, token=token, audit_path=ws["audit"])
    assert result == {"ran": True}


def test_runner_rejects_a_token_from_a_different_workspace(gate, tmp_path):
    ws = _make_workspace(tmp_path)
    other_root = tmp_path / "other"
    other_root.mkdir()
    other_assessment = other_root / "assessment.yaml"
    other_assessment.write_bytes(P03_ASSESSMENT.read_bytes())
    other_receipt = other_root / "receipt.yaml"
    _write_receipt(other_receipt, _receipt_payload(other_assessment))
    other_audit = other_root / "audit.jsonl"
    other_token = gate.authorize(
        assessment_path=other_assessment,
        receipt_path=other_receipt,
        audit_path=other_audit,
        batch_plan_path=BATCH_PLAN_V2,
    )
    assert other_token.authorized is True
    runner = gate.AtlasRunner(cell_runner=lambda *_a, **_kw: {"ran": True})
    # this workspace has its own authorized token; the other workspace's token
    # must not authorize writing to this workspace's audit
    this_audit = ws["audit"]
    with pytest.raises(gate.UnauthorizedAtlasRun):
        runner.write_summary(
            token=other_token,
            audit_path=this_audit,
            summary={"cell": "qpsk-snr20", "verdict": "NO_HEADROOM"},
        )


# ---------------------------------------------------------------------------
# 4. Audit is append-only: a second run appends rather than overwriting; the
#    old receipt id remains in history.
# ---------------------------------------------------------------------------


def test_audit_is_append_only_across_runs(gate, tmp_path):
    ws = _make_workspace(tmp_path)
    token1 = gate.authorize(
        assessment_path=ws["assessment"],
        receipt_path=ws["receipt"],
        audit_path=ws["audit"],
        batch_plan_path=BATCH_PLAN_V2,
    )
    runner = gate.AtlasRunner(cell_runner=lambda cell_id, **_: {"cell": cell_id})
    runner.run_cell(cell_id="qpsk-snr20", payload={}, token=token1, audit_path=ws["audit"])
    runner.write_summary(
        token=token1,
        audit_path=ws["audit"],
        summary={"cell": "qpsk-snr20", "verdict": "NO_HEADROOM"},
    )
    # edit the assessment, then re-issue a fresh receipt (simulating Atlas close-out)
    edited = yaml.safe_load(ws["assessment"].read_text(encoding="utf-8"))
    edited["adjudicated_candidate_status"] = edited["adjudicated_candidate_status"] + "_V2"
    ws["assessment"].write_text(yaml.safe_dump(edited, sort_keys=False), encoding="utf-8")
    _write_receipt(ws["receipt"], _receipt_payload(ws["assessment"]))
    token2 = gate.authorize(
        assessment_path=ws["assessment"],
        receipt_path=ws["receipt"],
        audit_path=ws["audit"],
        batch_plan_path=BATCH_PLAN_V2,
    )
    runner.run_cell(cell_id="qpsk-snr15", payload={}, token=token2, audit_path=ws["audit"])
    runner.write_summary(
        token=token2,
        audit_path=ws["audit"],
        summary={"cell": "qpsk-snr15", "verdict": "HEADROOM_FOUND"},
    )
    records = [json.loads(line) for line in ws["audit"].read_text(encoding="utf-8").splitlines() if line.strip()]
    decisions = [r["decision"] for r in records]
    # both authorization records and both summary records survive (>=4 lines)
    assert decisions.count("AUTHORIZED") >= 2
    assert decisions.count("SUMMARY_WRITTEN") >= 2
    receipt_ids = {r["receipt_id"] for r in records}
    assert token1.receipt_id in receipt_ids
    assert token2.receipt_id in receipt_ids
    assert token1.receipt_id != token2.receipt_id


# ---------------------------------------------------------------------------
# 5. Closing the Atlas requires re-running the claim-scope gate against a NEW
#    assessment; the closing summary may only be written when a new PASS
#    receipt exists.
# ---------------------------------------------------------------------------


def test_closing_summary_requires_fresh_new_receipt_after_atlas(gate, tmp_path):
    ws = _make_workspace(tmp_path)
    token = gate.authorize(
        assessment_path=ws["assessment"],
        receipt_path=ws["receipt"],
        audit_path=ws["audit"],
        batch_plan_path=BATCH_PLAN_V2,
    )
    runner = gate.AtlasRunner(cell_runner=lambda cell_id, **_: {"cell": cell_id})
    runner.run_cell(cell_id="qpsk-snr20", payload={}, token=token, audit_path=ws["audit"])
    # build a new assessment describing the Atlas close-out (still LOCAL_NEGATIVE
    # at cell/slice, with higher levels open as before)
    new_assessment = tmp_path / "atlas-closeout-assessment.yaml"
    new_assessment.write_bytes(P03_ASSESSMENT.read_bytes())
    new_receipt = tmp_path / "atlas-closeout-receipt.yaml"
    _write_receipt(new_receipt, _receipt_payload(new_assessment))
    close_token = gate.authorize_closeout(
        assessment_path=new_assessment,
        receipt_path=new_receipt,
        audit_path=ws["audit"],
        batch_plan_path=BATCH_PLAN_V2,
    )
    assert close_token.authorized is True
    # the original cell-run token must NOT be reusable to authorize the close-out
    with pytest.raises(gate.UnauthorizedAtlasRun):
        runner.write_closeout(
            token=token,
            audit_path=ws["audit"],
            closeout={"atlas": "stage-a", "verdict": "NO_HEADROOM_IN_REPRESENTATIVE_DOMAIN_WITH_CERTIFICATE"},
        )


# ---------------------------------------------------------------------------
# 6. BatchPlan prerequisites: the gate refuses when batch-plan.v2.yaml has
#    been deleted or when its mandatory guard flags are flipped off.
# ---------------------------------------------------------------------------


def test_gate_refuses_when_batch_plan_prerequisites_violated(gate, tmp_path):
    ws = _make_workspace(tmp_path)
    bad_plan = tmp_path / "batch-plan.yaml"
    plan = yaml.safe_load(BATCH_PLAN_V2.read_text(encoding="utf-8"))
    plan["guards"]["B004_forbidden"] = False
    bad_plan.write_text(yaml.safe_dump(plan, sort_keys=False), encoding="utf-8")
    token = gate.authorize(
        assessment_path=ws["assessment"],
        receipt_path=ws["receipt"],
        audit_path=ws["audit"],
        batch_plan_path=bad_plan,
    )
    assert token.authorized is False
    assert "batch" in token.reason.lower() or "guard" in token.reason.lower()


# ---------------------------------------------------------------------------
# ADVERSARIAL REVIEWS (appended by independent verifier)
#
# Each test below targets one specific bypass vector NOT already covered by
# the tests above. The verifier is trying to BREAK the gate, not confirm it.
# ---------------------------------------------------------------------------


def test_adversarial_closeout_token_cannot_be_used_for_write_summary(gate, tmp_path):
    """BYPASS attempt: mint a CLOSEOUT token, then try to use it to call
    write_summary (which requires CELL_RUN). This is the reverse cross-type
    misuse of bypass #8 (which tests CELL_RUN -> write_closeout).
    The gate must refuse: token_type mismatch."""
    ws = _make_workspace(tmp_path)
    closeout_token = gate.authorize_closeout(
        assessment_path=ws["assessment"],
        receipt_path=ws["receipt"],
        audit_path=ws["audit"],
        batch_plan_path=BATCH_PLAN_V2,
    )
    assert closeout_token.authorized is True
    assert closeout_token.token_type == "CLOSEOUT"
    runner = gate.AtlasRunner(cell_runner=lambda cell_id, **_: {"cell": cell_id})
    with pytest.raises(gate.UnauthorizedAtlasRun):
        runner.write_summary(
            token=closeout_token,
            audit_path=ws["audit"],
            summary={"cell": "qpsk-snr20", "verdict": "NO_HEADROOM"},
        )
    # ensure nothing was written
    records = [json.loads(line) for line in ws["audit"].read_text(encoding="utf-8").splitlines() if line.strip()]
    assert all(r["decision"] != "SUMMARY_WRITTEN" for r in records)


def test_adversarial_run_cell_with_audit_path_none_raises(gate, tmp_path):
    """BYPASS attempt: call run_cell with a valid token but audit_path=None,
    hoping to skip the audit-identity binding check entirely and run the cell
    without leaving a trace. The gate must raise rather than silently fall back."""
    ws = _make_workspace(tmp_path)
    token = gate.authorize(
        assessment_path=ws["assessment"],
        receipt_path=ws["receipt"],
        audit_path=ws["audit"],
        batch_plan_path=BATCH_PLAN_V2,
    )
    assert token.authorized is True
    runner = gate.AtlasRunner(cell_runner=lambda cell_id, **_: {"cell": cell_id})
    with pytest.raises(gate.UnauthorizedAtlasRun):
        runner.run_cell(cell_id="qpsk-snr20", payload={}, token=token, audit_path=None)


def test_adversarial_batch_plan_with_wrong_schema_version_blocks(gate, tmp_path):
    """BYPASS attempt: present a batch-plan file whose schema_version has been
    tampered (so guard flags cannot be trusted to mean what the gate thinks they
    mean). The gate must refuse before consulting guard flags."""
    ws = _make_workspace(tmp_path)
    plan = yaml.safe_load(BATCH_PLAN_V2.read_text(encoding="utf-8"))
    plan["schema_version"] = "direction-lab.batch-plan-overlay.v2"
    bad_plan = tmp_path / "batch-plan.yaml"
    bad_plan.write_text(yaml.safe_dump(plan, sort_keys=False), encoding="utf-8")
    token = gate.authorize(
        assessment_path=ws["assessment"],
        receipt_path=ws["receipt"],
        audit_path=ws["audit"],
        batch_plan_path=bad_plan,
    )
    assert token.authorized is False
    assert "schema_version" in token.reason.lower() or "batch" in token.reason.lower()


def test_adversarial_receipt_with_wrong_schema_version_blocks(gate, tmp_path):
    """BYPASS attempt: a hand-edited receipt whose schema_version does not
    match the canonical receipt schema. The gate must refuse on schema alone."""
    ws = _make_workspace(tmp_path)
    receipt = yaml.safe_load(ws["receipt"].read_text(encoding="utf-8"))
    receipt["schema_version"] = "direction-lab.claim-scope-validation-receipt.v2"
    ws["receipt"].write_text(yaml.safe_dump(receipt, sort_keys=True), encoding="utf-8")
    token = gate.authorize(
        assessment_path=ws["assessment"],
        receipt_path=ws["receipt"],
        audit_path=ws["audit"],
        batch_plan_path=BATCH_PLAN_V2,
    )
    assert token.authorized is False
    assert "schema_version" in token.reason.lower()


def test_adversarial_hand_edited_receipt_id_does_not_grant_authority(gate, tmp_path):
    """BYPASS attempt: attacker hand-writes a PASS receipt with a freshly
    recomputed receipt_id that matches a mutated payload, hoping the gate
    trusts the receipt_id as authority. The gate must NOT trust receipt_id;
    it derives authority from the SHA match + validator re-run. Here we
    tamper with the assessment, then recompute receipt_id to match the bad
    payload (but the assessment SHA inside the receipt is recomputed to
    match the mutated bytes, AND the validator still runs on the mutated
    assessment and should reject it)."""
    ws = _make_workspace(tmp_path)
    # mutate the assessment in a way that fails the validator (drop FAMILY verdict)
    bad = yaml.safe_load(ws["assessment"].read_text(encoding="utf-8"))
    bad["verdicts"].pop("FAMILY")
    ws["assessment"].write_text(yaml.safe_dump(bad, sort_keys=False), encoding="utf-8")
    # hand-write a PASS receipt whose hashes are HONEST about the mutated bytes,
    # and recompute receipt_id to "prove" authenticity
    payload = {
        "schema_version": "direction-lab.claim-scope-validation-receipt.v1",
        "status": "PASS",
        "assessment_sha256": _sha(ws["assessment"]),
        "validator_sha256": _sha(VALIDATOR_PATH),
        "validator_version": "direction-lab.claim-scope.v1",
    }
    receipt_id = hashlib.sha256(
        ("\x00".join([payload["status"], payload["assessment_sha256"], payload["validator_sha256"]])).encode("utf-8")
    ).hexdigest()
    _write_receipt(ws["receipt"], {**payload, "receipt_id": receipt_id})
    token = gate.authorize(
        assessment_path=ws["assessment"],
        receipt_path=ws["receipt"],
        audit_path=ws["audit"],
        batch_plan_path=BATCH_PLAN_V2,
    )
    assert token.authorized is False
    # blocked by the validator re-run, not by receipt_id mismatch
    assert "fail" in token.reason.lower() or "validator" in token.reason.lower()


def test_adversarial_run_cell_then_closeout_with_same_cellrun_token_blocks(gate, tmp_path):
    """BYPASS attempt #8 (already partially covered), but exercised via the
    direct runner path: obtain a CELL_RUN token, run a cell, then attempt to
    use the SAME CELL_RUN token to write an Atlas-level close-out. Must raise
    token_type mismatch."""
    ws = _make_workspace(tmp_path)
    token = gate.authorize(
        assessment_path=ws["assessment"],
        receipt_path=ws["receipt"],
        audit_path=ws["audit"],
        batch_plan_path=BATCH_PLAN_V2,
    )
    runner = gate.AtlasRunner(cell_runner=lambda cell_id, **_: {"cell": cell_id})
    runner.run_cell(cell_id="qpsk-snr20", payload={}, token=token, audit_path=ws["audit"])
    with pytest.raises(gate.UnauthorizedAtlasRun):
        runner.write_closeout(
            token=token,
            audit_path=ws["audit"],
            closeout={"atlas": "stage-a", "verdict": "NO_HEADROOM_IN_REPRESENTATIVE_DOMAIN_WITH_CERTIFICATE"},
        )
    records = [json.loads(line) for line in ws["audit"].read_text(encoding="utf-8").splitlines() if line.strip()]
    assert all(r["decision"] != "CLOSEOUT_WRITTEN" for r in records)


def test_adversarial_token_from_different_audit_path_rejected_by_path_collision(gate, tmp_path):
    """BYPASS attempt #7 variant: a token minted for one audit path (and
    therefore bound to that path's resolved identity) must not authorize a
    write to a different audit file, even if the attacker hands the foreign
    token in alongside a fresh local audit_path. The audit_identity check
    must compare the resolved paths."""
    # workspace A: mint a valid CELL_RUN token
    (tmp_path / "a").mkdir()
    ws_a = _make_workspace(tmp_path / "a")
    token_a = gate.authorize(
        assessment_path=ws_a["assessment"],
        receipt_path=ws_a["receipt"],
        audit_path=ws_a["audit"],
        batch_plan_path=BATCH_PLAN_V2,
    )
    assert token_a.authorized is True
    # workspace B: separate audit file
    (tmp_path / "b").mkdir()
    ws_b = _make_workspace(tmp_path / "b")
    runner = gate.AtlasRunner(cell_runner=lambda cell_id, **_: {"cell": cell_id})
    with pytest.raises(gate.UnauthorizedAtlasRun):
        runner.write_summary(
            token=token_a,
            audit_path=ws_b["audit"],
            summary={"cell": "qpsk-snr20", "verdict": "HEADROOM_FOUND"},
        )


def test_adversarial_second_authorize_does_not_overwrite_old_receipt_id(gate, tmp_path):
    """BYPASS attempt #10: the audit log must be append-only. After a second
    authorize, the first authorize's receipt_id must still be present in the
    log (no truncation, no overwrite)."""
    ws = _make_workspace(tmp_path)
    token1 = gate.authorize(
        assessment_path=ws["assessment"],
        receipt_path=ws["receipt"],
        audit_path=ws["audit"],
        batch_plan_path=BATCH_PLAN_V2,
    )
    first_log = ws["audit"].read_text(encoding="utf-8")
    assert token1.receipt_id in first_log
    # second authorize (re-using the same valid receipt) appends another record
    token2 = gate.authorize(
        assessment_path=ws["assessment"],
        receipt_path=ws["receipt"],
        audit_path=ws["audit"],
        batch_plan_path=BATCH_PLAN_V2,
    )
    second_log = ws["audit"].read_text(encoding="utf-8")
    # first receipt_id still survives
    assert token1.receipt_id in second_log
    # second receipt_id also present
    assert token2.receipt_id in second_log
    # log grew, was not replaced
    assert len(second_log) > len(first_log)
    records = [json.loads(line) for line in second_log.splitlines() if line.strip()]
    assert sum(1 for r in records if r["decision"] == "AUTHORIZED") >= 2
