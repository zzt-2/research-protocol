"""Validate that a Direction Lab claim does not outrun its evidence scope.

The validator is future-facing and deliberately independent of the frozen v3
controller and queue validator.  A PASS may be materialized as a
content-addressed receipt for later transition gates.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml


SCHEMA_VERSION = "direction-lab.claim-scope.v1"
RECEIPT_SCHEMA_VERSION = "direction-lab.claim-scope-validation-receipt.v1"
LEVELS = ("CELL", "SLICE", "DOMAIN", "CANDIDATE", "FAMILY")
LEVEL_INDEX = {level: index for index, level in enumerate(LEVELS)}
ORDER_LABEL = "CELL<SLICE<DOMAIN<CANDIDATE<FAMILY"
DECISION_CLASSES = {"NON_DECISIVE", "LOCAL_NEGATIVE", "ADVANCE", "RETIRE"}
SCOPE_DECISIONS = {"ADVANCE", "RETIRE"}
CERTIFICATE_TYPES = {
    "MECHANISM_PROOF",
    "REPRESENTATIVE_DOMAIN_COVERAGE",
    "STRONG_BASELINE_DOMINANCE",
}
DOMAIN_COVERAGE_CERTIFICATES = {
    "REPRESENTATIVE_DOMAIN_COVERAGE",
    "STRONG_BASELINE_DOMINANCE",
}
RETIRE_WORDS = re.compile(
    r"(?:^|[^A-Z0-9])(STOP(?:PED)?|RETIR(?:E|ED|EMENT)|KILL(?:ED)?|REJECT(?:ED)?)(?:$|[^A-Z0-9])"
)
ADVANCE_WORDS = re.compile(
    r"(?:^|[^A-Z0-9])(ADVANCE(?:D)?|PROMOT(?:E|ED|ION)|RETAIN(?:ED)?)(?:$|[^A-Z0-9])"
)


class ValidationReport:
    def __init__(self, errors: list[str]) -> None:
        self.errors = errors

    @property
    def passed(self) -> bool:
        return not self.errors


def _finite_number(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def _verdict_parts(verdict: Any, level: str, errors: list[str]) -> tuple[str, str]:
    if not isinstance(verdict, Mapping):
        errors.append(f"{level} verdict must be a mapping with status and decision_class")
        return "", ""
    status = str(verdict.get("status", "")).strip().upper()
    decision_class = str(verdict.get("decision_class", "")).strip().upper()
    if not status:
        errors.append(f"verdict status must be non-empty: {level}")
    if decision_class not in DECISION_CLASSES:
        errors.append(
            f"{level} verdict decision_class must be one of {sorted(DECISION_CLASSES)}"
        )
    if RETIRE_WORDS.search(status) and decision_class != "RETIRE":
        errors.append(
            f"DECISION_CLASS_MISMATCH: {level} status contains stop/retire language "
            f"but decision_class={decision_class}"
        )
    if ADVANCE_WORDS.search(status) and decision_class != "ADVANCE":
        errors.append(
            f"DECISION_CLASS_MISMATCH: {level} status contains advance/promote/retain "
            f"language but decision_class={decision_class}"
        )
    return status, decision_class


def _validate_coverage(coverage: Any, decisions: Mapping[str, str]) -> list[str]:
    if not isinstance(coverage, Mapping):
        return ["evidence_scope.coverage must be a mapping"]
    errors: list[str] = []
    denominator = coverage.get("denominator")
    if not _finite_number(denominator) or float(denominator) < 0.0:
        return ["coverage denominator must be a finite non-negative number"]

    coverage_decision = str(coverage.get("decision_class", "")).strip().upper()
    if coverage_decision not in DECISION_CLASSES:
        errors.append(
            f"coverage decision_class must be one of {sorted(DECISION_CLASSES)}"
        )

    if float(denominator) == 0.0:
        if coverage.get("value") is not None:
            errors.append("zero-headroom coverage requires value=null")
        if coverage.get("status") != "NOT_APPLICABLE_ZERO_HEADROOM":
            errors.append("zero-headroom coverage status must be NOT_APPLICABLE_ZERO_HEADROOM")
        if coverage.get("pass") is not False:
            errors.append("zero-headroom coverage requires pass=false")
        if coverage_decision != "LOCAL_NEGATIVE":
            errors.append("zero-headroom coverage decision_class must be LOCAL_NEGATIVE")
        for level in LEVELS[2:]:
            if decisions.get(level) != "NON_DECISIVE":
                errors.append(
                    f"ZERO_HEADROOM_SCOPE_LIMIT: {level} must remain NON_DECISIVE; "
                    "zero headroom may support a CELL finding and a SLICE-local verdict, "
                    "but no DOMAIN-or-higher conclusion"
                )
        return errors

    value = coverage.get("value")
    if not _finite_number(value) or not 0.0 <= float(value) <= 1.0:
        errors.append("measured coverage value must be a finite number in [0,1]")
    if coverage.get("status") != "MEASURED":
        errors.append("positive-denominator coverage status must be MEASURED")
    if not isinstance(coverage.get("pass"), bool):
        errors.append("measured coverage pass must be boolean")
    return errors


def _validate_evidence_pointer(pointer: Any, base_dir: Path | None, label: str) -> list[str]:
    if not isinstance(pointer, Mapping):
        return [f"{label} evidence pointer must be a mapping with path and sha256"]
    relative_text = str(pointer.get("path", "")).strip()
    recorded_hash = str(pointer.get("sha256", "")).strip().lower()
    if not relative_text or not re.fullmatch(r"[0-9a-f]{64}", recorded_hash):
        return [f"{label} evidence pointer requires a relative path and SHA-256"]
    relative = Path(relative_text)
    if relative.is_absolute() or ".." in relative.parts:
        return [f"{label} evidence pointer must stay within the assessment directory"]
    if base_dir is None:
        return [f"{label} evidence pointer cannot be verified without base_dir"]
    root = base_dir.resolve()
    target = (root / relative).resolve()
    try:
        target.relative_to(root)
    except ValueError:
        return [f"{label} evidence pointer escapes the assessment directory"]
    if not target.is_file():
        return [f"{label} evidence pointer target does not exist: {relative_text}"]
    actual_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    if actual_hash != recorded_hash:
        return [
            f"{label} evidence pointer SHA mismatch: recorded={recorded_hash}, actual={actual_hash}"
        ]
    return []


def _validate_history(history: Any) -> list[str]:
    if not isinstance(history, Mapping):
        return ["historical_counterexamples must be a mapping"]
    errors: list[str] = []
    if history.get("status") != "RESOLVED":
        errors.append("historical_counterexamples status must be RESOLVED")
    items = history.get("items")
    if not isinstance(items, list):
        errors.append("historical_counterexamples items must be a list")
        return errors
    allowed = {"COVERED", "EXCLUDED_WITH_JUSTIFICATION", "SUPERSEDED"}
    for index, item in enumerate(items):
        if not isinstance(item, Mapping) or not str(item.get("reference", "")).strip():
            errors.append(f"historical_counterexamples item {index} requires a reference")
            continue
        disposition = item.get("disposition")
        if disposition not in allowed:
            errors.append(
                f"historical_counterexamples item {index} has invalid disposition: {disposition}"
            )
        if disposition == "EXCLUDED_WITH_JUSTIFICATION" and not str(
            item.get("justification", "")
        ).strip():
            errors.append(
                f"historical_counterexamples item {index} exclusion requires justification"
            )
    return errors


def _validate_axes(axes: Any) -> list[str]:
    if not isinstance(axes, Mapping) or not axes:
        return ["representative_axes must be a non-empty mapping"]
    errors: list[str] = []
    for name, values in axes.items():
        if not str(name).strip() or not isinstance(values, list) or not values:
            errors.append(f"representative_axes entry must contain planned points: {name}")
    return errors


def _validate_sensitivity(sensitivity: Any) -> list[str]:
    if not isinstance(sensitivity, Mapping):
        return ["statistical_sensitivity must be a mapping"]
    errors: list[str] = []
    if sensitivity.get("status") != "PASS":
        errors.append("statistical_sensitivity status must be PASS")
    target = sensitivity.get("target_effect")
    achieved = sensitivity.get("achieved_upper_bound")
    for field, value in (("target_effect", target), ("achieved_upper_bound", achieved)):
        if not _finite_number(value) or float(value) < 0.0:
            errors.append(f"statistical_sensitivity {field} must be finite and non-negative")
    if _finite_number(target) and _finite_number(achieved) and float(achieved) > float(target):
        errors.append("statistical_sensitivity achieved_upper_bound must be <= target_effect")
    return errors


def _validate_independent_verification(
    verification: Any,
    base_dir: Path | None,
) -> list[str]:
    if not isinstance(verification, Mapping):
        return ["independent_verification must be a mapping with PASS evidence"]
    errors: list[str] = []
    if verification.get("status") != "PASS":
        errors.append("independent_verification status must be PASS")
    errors.extend(
        _validate_evidence_pointer(
            verification.get("evidence"), base_dir, "independent_verification"
        )
    )
    return errors


def _validate_scope_certificate(
    certificate: Any,
    elevated: list[tuple[str, str]],
    coverage: Mapping[str, Any],
    base_dir: Path | None,
) -> list[str]:
    if not elevated:
        return []
    target_level, target_decision = elevated[-1]
    if not isinstance(certificate, Mapping):
        return [
            f"SCOPE_CERTIFICATE_REQUIRED: {target_level} {target_decision} "
            "requires a verified scope certificate"
        ]

    errors: list[str] = []
    if certificate.get("target_level") != target_level:
        errors.append(
            f"scope certificate target_level must match highest decision {target_level}: "
            f"actual={certificate.get('target_level')}"
        )
    certificate_decision = str(certificate.get("decision_class", "")).strip().upper()
    if certificate_decision != target_decision:
        errors.append(
            "scope certificate decision_class must match its target verdict: "
            f"expected={target_decision}, actual={certificate_decision}"
        )
    certificate_type = certificate.get("type")
    if certificate_type not in CERTIFICATE_TYPES:
        errors.append(f"scope certificate type is invalid: {certificate_type}")
    if target_level == "FAMILY" and certificate_type != "MECHANISM_PROOF":
        errors.append("FAMILY_SCOPE_REQUIRES_MECHANISM_PROOF")
    if certificate_type in DOMAIN_COVERAGE_CERTIFICATES and LEVEL_INDEX[target_level] > LEVEL_INDEX["CANDIDATE"]:
        errors.append("representative domain coverage can support at most CANDIDATE scope")

    evidence = certificate.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        errors.append("scope certificate evidence must contain at least one pointer")
    else:
        for index, pointer in enumerate(evidence):
            errors.extend(
                _validate_evidence_pointer(pointer, base_dir, f"scope certificate evidence pointer {index}")
            )
    errors.extend(
        _validate_independent_verification(
            certificate.get("independent_verification"), base_dir
        )
    )
    errors.extend(_validate_history(certificate.get("historical_counterexamples")))
    if certificate_type in DOMAIN_COVERAGE_CERTIFICATES:
        errors.extend(_validate_axes(certificate.get("representative_axes")))
        errors.extend(_validate_sensitivity(certificate.get("statistical_sensitivity")))

    coverage_decision = str(coverage.get("decision_class", "")).strip().upper()
    if coverage.get("pass") is not True or coverage_decision != certificate_decision:
        errors.append(
            "COVERAGE_CERTIFICATE_DECISION_MISMATCH: scope certificate requires "
            "coverage pass=true and the same decision_class"
        )
    return errors


def validate_claim_scope(
    document: Mapping[str, Any],
    *,
    base_dir: str | Path | None = None,
) -> ValidationReport:
    errors: list[str] = []
    if document.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")

    evidence_scope = document.get("evidence_scope")
    if not isinstance(evidence_scope, Mapping):
        return ValidationReport(errors + ["evidence_scope must be a mapping"])
    supported_level = evidence_scope.get("max_supported_level")
    if supported_level not in ("CELL", "SLICE"):
        errors.append(
            f"SELF_REPORTED_SCOPE_LIMIT: max_supported_level must be CELL or SLICE, not {supported_level}"
        )
        supported_index = LEVEL_INDEX["SLICE"]
    else:
        supported_index = LEVEL_INDEX[str(supported_level)]

    verdicts = document.get("verdicts")
    if not isinstance(verdicts, Mapping) or set(verdicts) != set(LEVELS):
        errors.append(f"verdicts must contain exactly the five levels {ORDER_LABEL}")
        verdicts = verdicts if isinstance(verdicts, Mapping) else {}

    decisions: dict[str, str] = {}
    for level in LEVELS:
        _, decision = _verdict_parts(verdicts.get(level), level, errors)
        decisions[level] = decision

    elevated: list[tuple[str, str]] = []
    for level in LEVELS:
        decision = decisions.get(level)
        if LEVEL_INDEX[level] <= supported_index:
            continue
        if decision == "LOCAL_NEGATIVE":
            errors.append(
                f"BLOCKED_SCOPE_ESCALATION: {level} LOCAL_NEGATIVE exceeds "
                f"max_supported_level={supported_level}"
            )
        elif decision in SCOPE_DECISIONS:
            if LEVEL_INDEX[level] < LEVEL_INDEX["DOMAIN"]:
                errors.append(
                    f"BLOCKED_SCOPE_ESCALATION: {level} {decision} exceeds "
                    f"max_supported_level={supported_level}"
                )
            else:
                elevated.append((level, decision))

    coverage = evidence_scope.get("coverage")
    errors.extend(_validate_coverage(coverage, decisions))
    errors.extend(
        _validate_scope_certificate(
            document.get("scope_certificate"),
            elevated,
            coverage if isinstance(coverage, Mapping) else {},
            Path(base_dir) if base_dir is not None else None,
        )
    )
    return ValidationReport(errors)


def load_document(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        document = yaml.safe_load(handle)
    if not isinstance(document, dict):
        raise ValueError("claim-scope document root must be a mapping")
    return document


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_receipt(assessment: Path, receipt_path: Path) -> None:
    payload = {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "status": "PASS",
        "assessment_sha256": _sha256(assessment),
        "validator_sha256": _sha256(Path(__file__)),
        "validator_version": SCHEMA_VERSION,
    }
    receipt_id = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    receipt = {**payload, "receipt_id": receipt_id}
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(yaml.safe_dump(receipt, sort_keys=True), encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("claim_path", type=Path)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args(argv)
    report = validate_claim_scope(
        load_document(args.claim_path), base_dir=args.claim_path.parent
    )
    if report.passed:
        if args.receipt is not None:
            _write_receipt(args.claim_path, args.receipt)
        print(f"PASS: {args.claim_path}")
        return 0
    print(f"FAIL: {args.claim_path}")
    for error in report.errors:
        print(f"- {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
