from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest
import yaml


LAB_ROOT = Path(__file__).parents[1]
MODULE_PATH = LAB_ROOT / "tools" / "validate_claim_scope.py"
P03_ASSESSMENT = LAB_ROOT / "scout" / "P03-U19-residual-headroom" / "claim-scope-assessment.v1.yaml"


def _load_gate():
    spec = importlib.util.spec_from_file_location("direction_lab_claim_scope_gate", MODULE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def gate():
    return _load_gate()


def _verdict(status: str, decision_class: str) -> dict[str, str]:
    return {"status": status, "decision_class": decision_class}


def _base_claim() -> dict:
    return {
        "schema_version": "direction-lab.claim-scope.v1",
        "evidence_scope": {
            "max_supported_level": "SLICE",
            "coverage": {
                "denominator": 0.25,
                "value": 0.80,
                "status": "MEASURED",
                "pass": False,
                "decision_class": "NON_DECISIVE",
            },
        },
        "verdicts": {
            "CELL": _verdict("LOCAL_NEGATIVE", "LOCAL_NEGATIVE"),
            "SLICE": _verdict("LOCAL_NEGATIVE", "LOCAL_NEGATIVE"),
            "DOMAIN": _verdict("UNRESOLVED", "NON_DECISIVE"),
            "CANDIDATE": _verdict("OPEN", "NON_DECISIVE"),
            "FAMILY": _verdict("OPEN", "NON_DECISIVE"),
        },
        "scope_certificate": None,
    }


def _pointer(tmp_path: Path, name: str, content: bytes) -> dict[str, str]:
    path = tmp_path / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return {"path": name, "sha256": hashlib.sha256(content).hexdigest()}


def _history() -> dict:
    return {
        "status": "RESOLVED",
        "items": [
            {
                "reference": "history:16qam-long-sequence",
                "disposition": "COVERED",
            }
        ],
    }


def _representative_certificate(
    tmp_path: Path,
    *,
    target_level: str = "CANDIDATE",
    decision_class: str = "RETIRE",
) -> dict:
    return {
        "target_level": target_level,
        "decision_class": decision_class,
        "type": "REPRESENTATIVE_DOMAIN_COVERAGE",
        "evidence": [_pointer(tmp_path, "evidence/atlas.yaml", b"atlas-v1")],
        "independent_verification": {
            "status": "PASS",
            "evidence": _pointer(tmp_path, "verification/report.yaml", b"verifier-pass-v1"),
        },
        "representative_axes": {
            "modulation": ["QPSK", "16QAM"],
            "snr_db": [10, 20, 30],
        },
        "statistical_sensitivity": {
            "status": "PASS",
            "target_effect": 0.001,
            "achieved_upper_bound": 0.0005,
        },
        "historical_counterexamples": _history(),
    }


def _mechanism_proof_certificate(tmp_path: Path, *, target_level: str = "FAMILY") -> dict:
    return {
        "target_level": target_level,
        "decision_class": "RETIRE",
        "type": "MECHANISM_PROOF",
        "evidence": [_pointer(tmp_path, "evidence/proof.md", b"proof-v1")],
        "independent_verification": {
            "status": "PASS",
            "evidence": _pointer(tmp_path, "verification/proof-review.yaml", b"proof-review-pass-v1"),
        },
        "historical_counterexamples": _history(),
    }


def _retire_candidate(claim: dict, certificate: dict) -> None:
    claim["verdicts"]["CANDIDATE"] = _verdict("RETIRED", "RETIRE")
    claim["scope_certificate"] = certificate
    claim["evidence_scope"]["coverage"].update(
        {"value": 0.95, "pass": True, "decision_class": "RETIRE"}
    )


def test_requires_all_five_ordered_verdict_levels(gate):
    claim = _base_claim()
    claim["verdicts"].pop("CANDIDATE")
    report = gate.validate_claim_scope(claim)
    assert any("CELL<SLICE<DOMAIN<CANDIDATE<FAMILY" in error for error in report.errors)


def test_each_verdict_requires_status_and_decision_class(gate):
    claim = _base_claim()
    claim["verdicts"]["CELL"] = {"status": "LOCAL_NEGATIVE"}
    report = gate.validate_claim_scope(claim)
    assert any("decision_class" in error and "CELL" in error for error in report.errors)


def test_local_negative_with_higher_levels_open_is_valid(gate):
    assert gate.validate_claim_scope(_base_claim()).errors == []


@pytest.mark.parametrize(
    "status",
    ("P03_NOT_RETIRED_BUT_STOP_SPECIFIC", "ADVANCE_SPECIFIC", "PROMOTED", "RETAINED_SPECIFIC"),
)
def test_free_text_decisive_status_cannot_masquerade_as_non_decisive(gate, status):
    claim = _base_claim()
    claim["verdicts"]["CANDIDATE"] = _verdict(status, "NON_DECISIVE")
    report = gate.validate_claim_scope(claim)
    assert any("DECISION_CLASS_MISMATCH" in error and "CANDIDATE" in error for error in report.errors)


def test_max_supported_level_above_slice_cannot_be_self_reported(gate):
    claim = _base_claim()
    claim["evidence_scope"]["max_supported_level"] = "DOMAIN"
    report = gate.validate_claim_scope(claim)
    assert any("SELF_REPORTED_SCOPE_LIMIT" in error for error in report.errors)


@pytest.mark.parametrize("level", ("DOMAIN", "CANDIDATE", "FAMILY"))
@pytest.mark.parametrize("decision_class", ("ADVANCE", "RETIRE"))
def test_domain_or_higher_decision_requires_scope_certificate(gate, level, decision_class):
    claim = _base_claim()
    status = "SUPPORTED" if decision_class == "ADVANCE" else "RETIRED"
    claim["verdicts"][level] = _verdict(status, decision_class)
    report = gate.validate_claim_scope(claim)
    assert any("SCOPE_CERTIFICATE_REQUIRED" in error and level in error for error in report.errors)


@pytest.mark.parametrize(
    ("mutation", "expected"),
    (
        ("value", "value=null"),
        ("status", "NOT_APPLICABLE_ZERO_HEADROOM"),
        ("pass", "pass=false"),
    ),
)
def test_zero_headroom_cannot_be_converted_to_coverage_pass(gate, mutation, expected):
    claim = _base_claim()
    coverage = claim["evidence_scope"]["coverage"]
    coverage.update(
        {
            "denominator": 0.0,
            "value": None,
            "status": "NOT_APPLICABLE_ZERO_HEADROOM",
            "pass": False,
            "decision_class": "LOCAL_NEGATIVE",
        }
    )
    if mutation == "value":
        coverage["value"] = 1.0
    elif mutation == "status":
        coverage["status"] = "MEASURED"
    else:
        coverage["pass"] = True
    report = gate.validate_claim_scope(claim)
    assert any(expected in error for error in report.errors)


def test_zero_headroom_allows_slice_local_but_blocks_domain_or_higher(gate):
    claim = _base_claim()
    claim["evidence_scope"]["coverage"] = {
        "denominator": 0.0,
        "value": None,
        "status": "NOT_APPLICABLE_ZERO_HEADROOM",
        "pass": False,
        "decision_class": "LOCAL_NEGATIVE",
    }
    claim["verdicts"] = {
        "CELL": _verdict("NO_VISIBLE_HEADROOM", "LOCAL_NEGATIVE"),
        "SLICE": _verdict("LOCAL_NEGATIVE", "LOCAL_NEGATIVE"),
        "DOMAIN": _verdict("UNRESOLVED", "NON_DECISIVE"),
        "CANDIDATE": _verdict("OPEN", "NON_DECISIVE"),
        "FAMILY": _verdict("OPEN", "NON_DECISIVE"),
    }
    assert gate.validate_claim_scope(claim).errors == []
    claim["verdicts"]["DOMAIN"] = _verdict("LOCAL_NEGATIVE", "LOCAL_NEGATIVE")
    report = gate.validate_claim_scope(claim)
    assert any("ZERO_HEADROOM_SCOPE_LIMIT" in error and "DOMAIN" in error for error in report.errors)


def test_repository_p03_overlay_is_valid_and_stays_local(gate):
    assessment = gate.load_document(P03_ASSESSMENT)
    report = gate.validate_claim_scope(assessment, base_dir=P03_ASSESSMENT.parent)

    assert report.errors == []
    assert assessment["verdicts"]["SLICE"]["decision_class"] == "LOCAL_NEGATIVE"
    assert assessment["verdicts"]["DOMAIN"]["decision_class"] == "NON_DECISIVE"
    assert assessment["verdicts"]["CANDIDATE"]["decision_class"] == "NON_DECISIVE"
    assert assessment["verdicts"]["FAMILY"]["decision_class"] == "NON_DECISIVE"


def test_candidate_retirement_accepts_a_complete_verified_scope_certificate(gate, tmp_path):
    claim = _base_claim()
    _retire_candidate(claim, _representative_certificate(tmp_path))
    assert gate.validate_claim_scope(claim, base_dir=tmp_path).errors == []


@pytest.mark.parametrize("target_level", ("CANDIDATE", "FAMILY"))
def test_candidate_or_family_retirement_requires_matching_scope_certificate(gate, target_level):
    claim = _base_claim()
    claim["verdicts"][target_level] = _verdict("RETIRED", "RETIRE")
    report = gate.validate_claim_scope(claim)
    assert any("SCOPE_CERTIFICATE_REQUIRED" in error and target_level in error for error in report.errors)


@pytest.mark.parametrize("bad_pointer", ("missing", "wrong_hash"))
def test_fake_evidence_pointer_or_hash_is_rejected(gate, tmp_path, bad_pointer):
    claim = _base_claim()
    certificate = _representative_certificate(tmp_path)
    _retire_candidate(claim, certificate)
    if bad_pointer == "missing":
        certificate["evidence"][0]["path"] = "evidence/does-not-exist.yaml"
    else:
        certificate["evidence"][0]["sha256"] = "0" * 64
    report = gate.validate_claim_scope(claim, base_dir=tmp_path)
    assert any("evidence pointer" in error for error in report.errors)


@pytest.mark.parametrize("mutation", ("missing", "not_pass", "bad_pointer"))
def test_independent_verification_requires_pass_and_verified_pointer(gate, tmp_path, mutation):
    claim = _base_claim()
    certificate = _representative_certificate(tmp_path)
    _retire_candidate(claim, certificate)
    if mutation == "missing":
        certificate.pop("independent_verification")
    elif mutation == "not_pass":
        certificate["independent_verification"]["status"] = "PARTIAL"
    else:
        certificate["independent_verification"]["evidence"]["sha256"] = "f" * 64
    report = gate.validate_claim_scope(claim, base_dir=tmp_path)
    assert any("independent_verification" in error for error in report.errors)


@pytest.mark.parametrize(
    ("field", "expected"),
    (
        ("representative_axes", "representative_axes"),
        ("statistical_sensitivity", "statistical_sensitivity"),
        ("historical_counterexamples", "historical_counterexamples"),
    ),
)
def test_representative_certificate_requires_axes_sensitivity_and_history(
    gate, tmp_path, field, expected
):
    claim = _base_claim()
    certificate = _representative_certificate(tmp_path)
    _retire_candidate(claim, certificate)
    certificate.pop(field)
    report = gate.validate_claim_scope(claim, base_dir=tmp_path)
    assert any(expected in error for error in report.errors)


def test_sensitivity_upper_bound_must_meet_target_effect(gate, tmp_path):
    claim = _base_claim()
    certificate = _representative_certificate(tmp_path)
    _retire_candidate(claim, certificate)
    certificate["statistical_sensitivity"]["achieved_upper_bound"] = 0.002
    report = gate.validate_claim_scope(claim, base_dir=tmp_path)
    assert any("achieved_upper_bound must be <= target_effect" in error for error in report.errors)


def test_unresolved_historical_counterexamples_are_rejected(gate, tmp_path):
    claim = _base_claim()
    certificate = _representative_certificate(tmp_path)
    _retire_candidate(claim, certificate)
    certificate["historical_counterexamples"]["status"] = "UNRESOLVED"
    report = gate.validate_claim_scope(claim, base_dir=tmp_path)
    assert any("historical_counterexamples status must be RESOLVED" in error for error in report.errors)


@pytest.mark.parametrize("mutation", ("coverage_failed", "decision_mismatch"))
def test_coverage_pass_and_decision_must_match_scope_certificate(gate, tmp_path, mutation):
    claim = _base_claim()
    certificate = _representative_certificate(tmp_path)
    _retire_candidate(claim, certificate)
    coverage = claim["evidence_scope"]["coverage"]
    if mutation == "coverage_failed":
        coverage["pass"] = False
    else:
        coverage["decision_class"] = "ADVANCE"
    report = gate.validate_claim_scope(claim, base_dir=tmp_path)
    assert any("COVERAGE_CERTIFICATE_DECISION_MISMATCH" in error for error in report.errors)


def test_representative_domain_coverage_cannot_retire_family(gate, tmp_path):
    claim = _base_claim()
    claim["verdicts"]["FAMILY"] = _verdict("RETIRED", "RETIRE")
    certificate = _representative_certificate(tmp_path, target_level="FAMILY")
    claim["scope_certificate"] = certificate
    claim["evidence_scope"]["coverage"].update(
        {"value": 0.95, "pass": True, "decision_class": "RETIRE"}
    )
    report = gate.validate_claim_scope(claim, base_dir=tmp_path)
    assert any("FAMILY_SCOPE_REQUIRES_MECHANISM_PROOF" in error for error in report.errors)


def test_verified_mechanism_proof_can_retire_family(gate, tmp_path):
    claim = _base_claim()
    claim["verdicts"]["FAMILY"] = _verdict("RETIRED", "RETIRE")
    claim["scope_certificate"] = _mechanism_proof_certificate(tmp_path)
    claim["evidence_scope"]["coverage"].update(
        {"value": 1.0, "pass": True, "decision_class": "RETIRE"}
    )
    assert gate.validate_claim_scope(claim, base_dir=tmp_path).errors == []


def test_cli_writes_content_addressed_receipt_only_for_pass(tmp_path):
    assessment = tmp_path / "assessment.yaml"
    receipt = tmp_path / "receipts" / "claim-scope.yaml"
    assessment.write_text(yaml.safe_dump(_base_claim(), sort_keys=True), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(MODULE_PATH), str(assessment), "--receipt", str(receipt)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    record = yaml.safe_load(receipt.read_text(encoding="utf-8"))
    assert record["status"] == "PASS"
    assert record["assessment_sha256"] == hashlib.sha256(assessment.read_bytes()).hexdigest()
    assert record["validator_sha256"] == hashlib.sha256(MODULE_PATH.read_bytes()).hexdigest()
    payload = {key: value for key, value in record.items() if key != "receipt_id"}
    expected_id = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    assert record["receipt_id"] == expected_id


def test_cli_does_not_write_receipt_for_failed_assessment(tmp_path):
    claim = _base_claim()
    claim["verdicts"].pop("FAMILY")
    assessment = tmp_path / "invalid.yaml"
    receipt = tmp_path / "receipt.yaml"
    assessment.write_text(yaml.safe_dump(claim, sort_keys=True), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(MODULE_PATH), str(assessment), "--receipt", str(receipt)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert not receipt.exists()
