"""Unique preflight/assessment gate for the Headroom Atlas.

This module is the ONLY entrypoint that may run a Headroom Atlas cell or write
an Atlas state summary. It binds three things together before any Atlas work:

1. a claim-scope assessment that the validator must PASS on the exact bytes
   presented at authorize-time (not merely the bytes that some receipt was
   once written against);
2. a content-addressed PASS receipt whose ``assessment_sha256`` and
   ``validator_sha256`` match the exact files at authorize-time (so a receipt
   issued against an older assessment, an edited assessment, or a different
   validator build is rejected); and
3. the live ``batch-plan.v2.yaml`` guard flags (B001-B003 read-only, B004
   forbidden, ML training forbidden, Queue/Registry forbidden, formal promotion
   forbidden, no candidate/family exit without certificate).

The gate records every authorize attempt, every cell run and every summary
write to an append-only JSONL audit log. Old receipts and old audit records are
never overwritten; close-out requires a fresh NEW assessment + NEW receipt
(separate token type), so a cell-run token cannot authorize an Atlas-level
exit.

Design rules (DL-Process v0.4 / batch-plan.v2.yaml / D058):

- A PASS receipt is necessary but not sufficient: the gate always re-runs the
  claim-scope validator on the exact assessment bytes. This prevents a hand
  written PASS receipt from laundering an assessment that actually FAILs.
- The validator module is loaded by path (not import) so that this gate does
  not need to live inside the same package as the validator, and so the SHA we
  bind is the SHA of the exact validator file used.
- Tokens are immutable and bound to the audit path they were issued for, so a
  token minted for workspace A cannot be replayed to write a summary into
  workspace B's audit log.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import secrets
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Mapping

import yaml


RECEIPT_SCHEMA_VERSION = "direction-lab.claim-scope-validation-receipt.v1"
CLAIM_SCOPE_SCHEMA_VERSION = "direction-lab.claim-scope.v1"
BATCH_PLAN_SCHEMA_VERSION = "direction-lab.batch-plan-overlay.v1"

REQUIRED_BATCH_GUARDS = {
    "B001_B002_B003_read_only": True,
    "B004_forbidden": True,
    "P03_ML_training_forbidden": True,
    "Queue_Registry_forbidden": True,
    "formal_promotion_forbidden": True,
    "no_candidate_or_family_exit_without_certificate": True,
}


class UnauthorizedAtlasRun(RuntimeError):
    """Raised when an Atlas action is attempted without a valid token."""


def _load_validator(validator_path: Path):
    spec = importlib.util.spec_from_file_location("atlas_gate_claim_scope_validator", validator_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load validator at {validator_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} root must be a mapping")
    return data


def _audit_identity(audit_path: Path) -> str:
    """Stable identity of an audit log file.

    Tokens bind to the audit file's canonical path (not its byte content),
    because the byte content grows on every write that the token itself
    authorizes. Binding to the path is enough to prevent a token minted for
    workspace A from authorizing writes into workspace B's audit log, while
    still allowing the same token to write multiple records into its own log.
    """
    resolved = Path(audit_path).resolve()
    # absolute path string; resolve collapses any '..' so two relative paths
    # that point at the same file collapse to the same identity
    return str(resolved)


def _append_audit(audit_path: Path, record: dict[str, Any]) -> None:
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, sort_keys=True, separators=(",", ":"))
    # 'a' mode never overwrites; we never truncate this file anywhere
    with audit_path.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


@dataclass(frozen=True)
class AuthorizationToken:
    authorized: bool
    reason: str
    assessment_sha256: str
    validator_sha256: str
    receipt_id: str
    audit_identity: str
    token_type: str  # "CELL_RUN" or "CLOSEOUT"
    nonce: str = field(default_factory=lambda: secrets.token_hex(8))

    def _require(self, action: str) -> None:
        if not self.authorized:
            raise UnauthorizedAtlasRun(
                f"{action} refused: {self.reason}"
            )


def _check_batch_plan(batch_plan_path: Path) -> tuple[bool, str]:
    if not batch_plan_path.exists():
        return False, "batch plan missing"
    plan = _load_yaml(batch_plan_path)
    if plan.get("schema_version") != BATCH_PLAN_SCHEMA_VERSION:
        return False, f"batch plan schema_version must be {BATCH_PLAN_SCHEMA_VERSION}"
    guards = plan.get("guards", {})
    for flag, required in REQUIRED_BATCH_GUARDS.items():
        if guards.get(flag) != required:
            return False, f"batch plan guard {flag} must be {required}, got {guards.get(flag)!r}"
    return True, ""


def _authorize(
    *,
    assessment_path: Path,
    receipt_path: Path,
    audit_path: Path,
    batch_plan_path: Path,
    validator_path: Path,
    token_type: str,
) -> AuthorizationToken:
    assessment_path = Path(assessment_path).resolve()
    receipt_path = Path(receipt_path).resolve()
    audit_path = Path(audit_path).resolve()
    batch_plan_path = Path(batch_plan_path).resolve()

    ok, reason = _check_batch_plan(batch_plan_path)
    if not ok:
        token = AuthorizationToken(
            authorized=False,
            reason=reason,
            assessment_sha256=_sha(assessment_path) if assessment_path.exists() else "",
            validator_sha256=_sha(validator_path) if validator_path.exists() else "",
            receipt_id="",
            audit_identity=_audit_identity(audit_path),
            token_type=token_type,
        )
        _append_audit(
            audit_path,
            {
                "ts": time.time(),
                "decision": "BLOCKED",
                "reason": reason,
                "token_type": token_type,
                "assessment_sha256": token.assessment_sha256,
                "validator_sha256": token.validator_sha256,
            },
        )
        return token

    assessment_hash = _sha(assessment_path)
    validator_hash = _sha(validator_path)

    # 1. receipt must exist and be a PASS bound to these exact hashes
    if not receipt_path.exists():
        reason = "receipt missing; a fresh PASS receipt bound to the exact assessment and validator hashes is required"
        _append_audit(
            audit_path,
            {
                "ts": time.time(),
                "decision": "BLOCKED",
                "reason": reason,
                "token_type": token_type,
                "assessment_sha256": assessment_hash,
                "validator_sha256": validator_hash,
            },
        )
        return AuthorizationToken(
            authorized=False,
            reason=reason,
            assessment_sha256=assessment_hash,
            validator_sha256=validator_hash,
            receipt_id="",
            audit_identity=_audit_identity(audit_path),
            token_type=token_type,
        )

    receipt = _load_yaml(receipt_path)
    if receipt.get("schema_version") != RECEIPT_SCHEMA_VERSION:
        reason = f"receipt schema_version must be {RECEIPT_SCHEMA_VERSION}"
    elif receipt.get("status") != "PASS":
        reason = "receipt status must be PASS"
    elif receipt.get("assessment_sha256") != assessment_hash:
        reason = (
            f"receipt assessment SHA mismatch: receipt={receipt.get('assessment_sha256')}, "
            f"actual={assessment_hash}"
        )
    elif receipt.get("validator_sha256") != validator_hash:
        reason = (
            f"receipt validator SHA mismatch: receipt={receipt.get('validator_sha256')}, "
            f"actual={validator_hash}"
        )
    else:
        reason = ""

    if reason:
        _append_audit(
            audit_path,
            {
                "ts": time.time(),
                "decision": "BLOCKED",
                "reason": reason,
                "token_type": token_type,
                "assessment_sha256": assessment_hash,
                "validator_sha256": validator_hash,
                "receipt_status": receipt.get("status"),
            },
        )
        return AuthorizationToken(
            authorized=False,
            reason=reason,
            assessment_sha256=assessment_hash,
            validator_sha256=validator_hash,
            receipt_id=str(receipt.get("receipt_id", "")),
            audit_identity=_audit_identity(audit_path),
            token_type=token_type,
        )

    # 2. re-run the validator on the exact assessment bytes; a PASS receipt
    #    alone is not trusted (defends against a hand-written PASS receipt
    #    laundering an assessment that actually FAILs)
    validator_module = _load_validator(validator_path)
    assessment_doc = _load_yaml(assessment_path)
    report = validator_module.validate_claim_scope(assessment_doc, base_dir=assessment_path.parent)
    if not report.passed:
        reason = f"assessment FAILS claim-scope validator: {report.errors[:3]}"
        _append_audit(
            audit_path,
            {
                "ts": time.time(),
                "decision": "BLOCKED",
                "reason": reason,
                "token_type": token_type,
                "assessment_sha256": assessment_hash,
                "validator_sha256": validator_hash,
                "validator_errors": list(report.errors)[:10],
            },
        )
        return AuthorizationToken(
            authorized=False,
            reason=reason,
            assessment_sha256=assessment_hash,
            validator_sha256=validator_hash,
            receipt_id=str(receipt.get("receipt_id", "")),
            audit_identity=_audit_identity(audit_path),
            token_type=token_type,
        )

    receipt_id = str(receipt.get("receipt_id", ""))
    audit_identity = _audit_identity(audit_path)
    token = AuthorizationToken(
        authorized=True,
        reason="ok",
        assessment_sha256=assessment_hash,
        validator_sha256=validator_hash,
        receipt_id=receipt_id,
        audit_identity=audit_identity,
        token_type=token_type,
    )
    _append_audit(
        audit_path,
        {
            "ts": time.time(),
            "decision": "AUTHORIZED",
            "reason": "ok",
            "token_type": token_type,
            "assessment_sha256": assessment_hash,
            "validator_sha256": validator_hash,
            "receipt_id": receipt_id,
            "nonce": token.nonce,
            "audit_identity": audit_identity,
        },
    )
    return token


def authorize(
    *,
    assessment_path: Path,
    receipt_path: Path,
    audit_path: Path,
    batch_plan_path: Path,
    validator_path: Path | None = None,
) -> AuthorizationToken:
    """Authorize a cell-run under the Headroom Atlas.

    The returned token must be passed to :class:`AtlasRunner.run_cell` and
    :meth:`AtlasRunner.write_summary`; those methods refuse to operate without
    it or with a token that does not match the live audit file.
    """
    if validator_path is None:
        # parents[0]=headroom-atlas, [1]=P03-U19-residual-headroom,
        # [2]=scout, [3]=direction-lab
        validator_path = (
            Path(__file__).resolve().parents[3] / "tools" / "validate_claim_scope.py"
        )
    return _authorize(
        assessment_path=assessment_path,
        receipt_path=receipt_path,
        audit_path=audit_path,
        batch_plan_path=batch_plan_path,
        validator_path=validator_path,
        token_type="CELL_RUN",
    )


def authorize_closeout(
    *,
    assessment_path: Path,
    receipt_path: Path,
    audit_path: Path,
    batch_plan_path: Path,
    validator_path: Path | None = None,
) -> AuthorizationToken:
    """Authorize an Atlas close-out (writes the Atlas-level verdict).

    Reuses :func:`authorize` machinery but stamps a distinct token type so a
    cell-run token cannot be replayed to authorize an Atlas-level exit. The
    caller must present a fresh NEW assessment + NEW receipt describing the
    Atlas close-out.
    """
    if validator_path is None:
        validator_path = (
            Path(__file__).resolve().parents[3] / "tools" / "validate_claim_scope.py"
        )
    return _authorize(
        assessment_path=assessment_path,
        receipt_path=receipt_path,
        audit_path=audit_path,
        batch_plan_path=batch_plan_path,
        validator_path=validator_path,
        token_type="CLOSEOUT",
    )


class AtlasRunner:
    """Guarded runner: the only object permitted to run Atlas cells and write
    Atlas summaries. Every method requires a valid :class:`AuthorizationToken`
    bound to the audit file being written to.
    """

    def __init__(self, *, cell_runner: Callable[..., Any]):
        self._cell_runner = cell_runner

    @staticmethod
    def _verify(token: AuthorizationToken, audit_path: Path, action: str, expected_type: str | None = None) -> None:
        token._require(action)
        if expected_type is not None and token.token_type != expected_type:
            raise UnauthorizedAtlasRun(
                f"{action} refused: token type {token.token_type!r} does not match required {expected_type!r}"
            )
        if _audit_identity(Path(audit_path)) != token.audit_identity:
            raise UnauthorizedAtlasRun(
                f"{action} refused: audit log identity mismatch (token bound to a different audit file)"
            )

    def run_cell(
        self,
        *,
        cell_id: str,
        payload: Mapping[str, Any],
        token: AuthorizationToken | None = None,
        audit_path: Path | None = None,
    ) -> Any:
        if token is None:
            raise UnauthorizedAtlasRun("run_cell refused: no authorization token provided")
        if audit_path is None:
            raise UnauthorizedAtlasRun("run_cell refused: audit_path is required to bind the token")
        # cell runs may use either CELL_RUN or CLOSEOUT tokens (a close-out may
        # also run a final confirmation cell); but the token must be valid and
        # bound to this audit file
        self._verify(token, audit_path=Path(audit_path), action="run_cell")
        return self._cell_runner(cell_id, **dict(payload))

    def write_summary(
        self,
        *,
        token: AuthorizationToken,
        audit_path: Path,
        summary: Mapping[str, Any],
    ) -> None:
        self._verify(token, audit_path=audit_path, action="write_summary", expected_type="CELL_RUN")
        record = {
            "ts": time.time(),
            "decision": "SUMMARY_WRITTEN",
            "token_type": token.token_type,
            "receipt_id": token.receipt_id,
            "assessment_sha256": token.assessment_sha256,
            "validator_sha256": token.validator_sha256,
            "nonce": token.nonce,
            "summary": dict(summary),
        }
        _append_audit(Path(audit_path), record)

    def write_closeout(
        self,
        *,
        token: AuthorizationToken,
        audit_path: Path,
        closeout: Mapping[str, Any],
    ) -> None:
        self._verify(token, audit_path=audit_path, action="write_closeout", expected_type="CLOSEOUT")
        record = {
            "ts": time.time(),
            "decision": "CLOSEOUT_WRITTEN",
            "token_type": token.token_type,
            "receipt_id": token.receipt_id,
            "assessment_sha256": token.assessment_sha256,
            "validator_sha256": token.validator_sha256,
            "nonce": token.nonce,
            "closeout": dict(closeout),
        }
        _append_audit(Path(audit_path), record)
