"""Small, deterministic hard-gate controller for the Direction Lab pilot.

The controller only validates a proposed action.  It never edits a manifest or
result in place; every decision is appended to an audit JSONL file.
"""

from __future__ import annotations

import json
import hashlib
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping


ALLOWED_ACTIONS = {"RUN", "GO", "KILL", "PROMOTE", "REUSE_RESULT"}
PROMOTABLE_EVIDENCE = {"FULL", "VERIFIED_RUN", "PAPER_READY"}
DESTINATION_ACTIONS = {
    "evidence_ledger": ALLOWED_ACTIONS,
    "promotion_board": {"GO", "KILL", "PROMOTE"},
    "formal_materials": {"PROMOTE"},
}


class GovernanceViolation(RuntimeError):
    """A proposed action crossed a machine-enforceable governance gate."""


@dataclass
class GovernanceController:
    registry: Mapping[str, Mapping[str, str]]
    audit_path: Path

    def __post_init__(self) -> None:
        self.audit_events: list[dict[str, Any]] = []
        self.audit_path.parent.mkdir(parents=True, exist_ok=True)

    def check(self, manifest: Mapping[str, Any] | None, *, action: str) -> dict[str, Any]:
        """Check one action and append an immutable decision record.

        ``REUSE_RESULT`` is special: a fingerprint drift is not silently
        accepted; it is converted into an explicitly blocked ``STALE`` result
        so downstream code cannot reuse an old result as current evidence.
        """

        event: dict[str, Any] = {
            "original_action": action,
            "run_id": manifest.get("run_id") if manifest else None,
            "blocked": False,
            "repair": None,
        }

        try:
            if action not in ALLOWED_ACTIONS:
                raise GovernanceViolation(f"action is not allowed: {action}")
            if manifest is None:
                raise GovernanceViolation("manifest is required")
            if not manifest.get("run_id"):
                raise GovernanceViolation("run_id is required")

            baseline_id = manifest.get("baseline_id")
            component_id = manifest.get("component_id")
            baseline = self.registry.get(baseline_id)
            component = self.registry.get(component_id)
            if baseline is None:
                raise GovernanceViolation(f"baseline_id not found: {baseline_id}")
            if component is None:
                raise GovernanceViolation(f"component_id not found: {component_id}")
            if action != "REUSE_RESULT" and baseline.get("status") != "canonical":
                raise GovernanceViolation(f"baseline status is not canonical: {baseline.get('status')}")
            allowed_component_statuses = {"canonical"}
            if action == "RUN":
                allowed_component_statuses.add("sandbox-candidate")
            if action != "REUSE_RESULT" and component.get("status") not in allowed_component_statuses:
                raise GovernanceViolation(f"component status is not canonical: {component.get('status')}")

            baseline_fp = manifest.get("baseline_fingerprint")
            component_fp = manifest.get("component_fingerprint")
            fingerprint_drift = []
            status_drift = []
            if baseline.get("status") != "canonical":
                status_drift.append("baseline status")
            if component.get("status") != "canonical":
                status_drift.append("component status")
            if baseline_fp != baseline.get("fingerprint"):
                fingerprint_drift.append("baseline")
            if component_fp != component.get("fingerprint"):
                fingerprint_drift.append("component")
            if (fingerprint_drift or status_drift) and action == "REUSE_RESULT":
                drift = fingerprint_drift + status_drift
                event.update(
                    {
                        "blocked": True,
                        "repair": "mark_stale",
                        "reason": f"component state changed: {', '.join(drift)}",
                    }
                )
                result = dict(manifest)
                receipt = self._attach_receipt(event, manifest, action=action, allowed=False)
                result.update(
                    {
                        "result_status": "STALE",
                        "blocked": True,
                        "decision_receipt": receipt,
                    }
                )
                self._record(event)
                return result
            if "baseline" in fingerprint_drift:
                raise GovernanceViolation("baseline fingerprint mismatch")
            if "component" in fingerprint_drift:
                raise GovernanceViolation("component fingerprint mismatch")

            if action in {"GO", "KILL"} and manifest.get("state") != "BOARD_READY":
                raise GovernanceViolation("GO/KILL requires BOARD_READY")
            if action == "PROMOTE" and (
                manifest.get("sandbox_only") is True
                or manifest.get("promotion_allowed") is not True
            ):
                raise GovernanceViolation("sandbox manifest does not allow promotion")
            if action == "PROMOTE" and manifest.get("evidence_status") not in PROMOTABLE_EVIDENCE:
                raise GovernanceViolation(
                    f"evidence cannot be promoted: {manifest.get('evidence_status')}"
                )

            result = dict(manifest)
            result["blocked"] = False
            result["decision_receipt"] = self._attach_receipt(
                event,
                manifest,
                action=action,
                allowed=True,
            )
            self._record(event)
            return result
        except GovernanceViolation as exc:
            event.update({"blocked": True, "reason": str(exc)})
            self._attach_receipt(event, manifest, action=action, allowed=False)
            self._record(event)
            raise

    def execute(
        self,
        manifest: Mapping[str, Any] | None,
        *,
        action: str,
        operation: Callable[[], Any],
    ) -> Any:
        """Run an operation only after its proposed action passes governance."""

        checked = self.check(manifest, action=action)
        if checked.get("blocked") or checked.get("result_status") == "STALE":
            raise GovernanceViolation("action is blocked by STALE governance result")
        operation_result = operation()
        result_hash = _value_hash(operation_result)
        self._record(
            {
                "event_type": "EXECUTION",
                "blocked": False,
                "decision_id": checked["decision_receipt"]["decision_id"],
                "run_id": checked["decision_receipt"]["run_id"],
                "result_hash": result_hash,
            }
        )
        return {
            "result": operation_result,
            "result_hash": result_hash,
            "manifest": dict(manifest or {}),
            "decision_receipt": checked["decision_receipt"],
        }

    def _attach_receipt(
        self,
        event: dict[str, Any],
        manifest: Mapping[str, Any] | None,
        *,
        action: str,
        allowed: bool,
    ) -> dict[str, Any]:
        receipt = {
            "decision_id": f"decision-{uuid.uuid4().hex}",
            "run_id": manifest.get("run_id") if manifest else None,
            "action": action,
            "manifest_hash": _manifest_hash(manifest),
            "allowed": allowed,
            "blocked": not allowed,
        }
        event["decision_receipt"] = receipt
        return receipt

    def _record(self, event: dict[str, Any]) -> None:
        event = dict(event)
        self.audit_events.append(event)
        with self.audit_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


def _manifest_hash(manifest: Mapping[str, Any] | None) -> str | None:
    if manifest is None:
        return None
    payload = json.dumps(
        manifest,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _value_hash(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


@dataclass
class EvidenceGate:
    audit_path: Path
    destinations: Mapping[str, Path]
    gate_audit_path: Path | None = None
    require_artifact_pointer: bool = False

    def __post_init__(self) -> None:
        if self.gate_audit_path is None:
            self.gate_audit_path = self.audit_path.with_name("evidence-gate-audit.jsonl")

    def submit(self, envelope: Mapping[str, Any], *, destination: str) -> dict[str, Any]:
        if destination not in DESTINATION_ACTIONS or destination not in self.destinations:
            raise GovernanceViolation(f"unknown evidence destination: {destination}")

        receipt = envelope.get("decision_receipt")
        if not isinstance(receipt, Mapping):
            return self._reject(
                destination,
                artifact_status="ORPHAN",
                reason="controller decision receipt is missing",
            )

        recorded = self._recorded_receipt(receipt.get("decision_id"))
        manifest = envelope.get("manifest")
        trusted = (
            recorded is not None
            and dict(receipt) == recorded
            and receipt.get("allowed") is True
            and receipt.get("blocked") is False
            and isinstance(manifest, Mapping)
            and receipt.get("manifest_hash") == _manifest_hash(manifest)
            and receipt.get("run_id") == manifest.get("run_id")
            and envelope.get("result_hash") == _value_hash(envelope.get("result"))
            and self._recorded_execution(
                receipt.get("decision_id"),
                envelope.get("result_hash"),
            )
        )
        if not trusted:
            return self._reject(
                destination,
                artifact_status="UNTRUSTED",
                reason="receipt is absent from audit or does not match the artifact",
            )

        if self.require_artifact_pointer:
            pointer = envelope.get("artifact_pointer")
            pointer_error = None
            if not isinstance(pointer, Mapping):
                pointer_error = "lean evidence requires an artifact_pointer; full result cannot enter the ledger"
            else:
                relative = Path(str(pointer.get("path", "")))
                root = self.audit_path.parent.resolve()
                if relative.is_absolute() or ".." in relative.parts or not relative.parts or relative.parts[0] != "artifacts":
                    pointer_error = "artifact_pointer path must be relative and contained under artifacts/"
                else:
                    artifact = (root / relative).resolve()
                    try:
                        artifact.relative_to(root)
                    except ValueError:
                        pointer_error = "artifact_pointer escapes the governed output directory"
                    if pointer_error is None and not artifact.is_file():
                        pointer_error = "artifact_pointer target does not exist"
                    if pointer_error is None:
                        expected_bytes = pointer.get("bytes")
                        expected_sha = pointer.get("sha256")
                        if not isinstance(expected_bytes, int) or expected_bytes != artifact.stat().st_size:
                            pointer_error = "artifact_pointer byte count does not match the artifact"
                        elif not isinstance(expected_sha, str) or expected_sha != hashlib.sha256(artifact.read_bytes()).hexdigest():
                            pointer_error = "artifact_pointer sha256 does not match the artifact"
            if pointer_error is not None:
                return self._reject(
                    destination,
                    artifact_status="ORPHAN",
                    reason=pointer_error,
                    trust_status="TRUSTED",
                    decision_id=receipt.get("decision_id"),
                )

        if self._has_later_stale_invalidation(
            receipt.get("decision_id"),
            receipt.get("run_id"),
        ):
            return self._reject(
                destination,
                artifact_status="STALE",
                reason="a later controller decision invalidated this run",
                trust_status="TRUSTED",
                decision_id=receipt.get("decision_id"),
            )

        if self._already_admitted(destination, receipt.get("decision_id")):
            return self._reject(
                destination,
                artifact_status="REPLAY",
                reason="decision receipt has already been admitted to this destination",
                trust_status="TRUSTED",
                decision_id=receipt.get("decision_id"),
            )

        action = receipt.get("action")
        if action not in DESTINATION_ACTIONS[destination]:
            return self._reject(
                destination,
                artifact_status="BLOCKED",
                reason=f"action {action} cannot enter {destination}",
                trust_status="TRUSTED",
                decision_id=receipt.get("decision_id"),
            )

        accepted = {
            "destination": destination,
            "accepted": True,
            "artifact_status": "ACCEPTED",
            "trust_status": "TRUSTED",
            "decision_id": receipt.get("decision_id"),
            "run_id": receipt.get("run_id"),
            "action": action,
            "manifest_hash": receipt.get("manifest_hash"),
            "result_hash": envelope.get("result_hash"),
        }
        if envelope.get("artifact_pointer") is not None:
            accepted["artifact_pointer"] = envelope.get("artifact_pointer")
        else:
            accepted["result"] = envelope.get("result")
        self._append_jsonl(self.destinations[destination], accepted)
        self._append_jsonl(self.gate_audit_path, accepted)
        return accepted

    def _recorded_receipt(self, decision_id: Any) -> dict[str, Any] | None:
        if not decision_id or not self.audit_path.exists():
            return None
        for line in self.audit_path.read_text(encoding="utf-8").splitlines():
            event = json.loads(line)
            receipt = event.get("decision_receipt")
            if isinstance(receipt, dict) and receipt.get("decision_id") == decision_id:
                if event.get("blocked") is False:
                    return receipt
                return None
        return None

    def _has_later_stale_invalidation(self, decision_id: Any, run_id: Any) -> bool:
        if not decision_id or not run_id or not self.audit_path.exists():
            return False
        seen_decision = False
        for line in self.audit_path.read_text(encoding="utf-8").splitlines():
            event = json.loads(line)
            event_receipt = event.get("decision_receipt")
            if not isinstance(event_receipt, dict):
                continue
            if event_receipt.get("decision_id") == decision_id:
                seen_decision = True
                continue
            if (
                seen_decision
                and event_receipt.get("run_id") == run_id
                and event.get("repair") == "mark_stale"
            ):
                return True
        return False

    def _recorded_execution(self, decision_id: Any, result_hash: Any) -> bool:
        if not decision_id or not result_hash or not self.audit_path.exists():
            return False
        for line in self.audit_path.read_text(encoding="utf-8").splitlines():
            event = json.loads(line)
            if (
                event.get("event_type") == "EXECUTION"
                and event.get("decision_id") == decision_id
                and event.get("result_hash") == result_hash
                and event.get("blocked") is False
            ):
                return True
        return False

    def _already_admitted(self, destination: str, decision_id: Any) -> bool:
        path = self.destinations[destination]
        if not decision_id or not path.exists():
            return False
        for line in path.read_text(encoding="utf-8").splitlines():
            if json.loads(line).get("decision_id") == decision_id:
                return True
        return False

    def _reject(
        self,
        destination: str,
        *,
        artifact_status: str,
        reason: str,
        trust_status: str = "UNTRUSTED",
        decision_id: Any = None,
    ) -> dict[str, Any]:
        verdict = {
            "destination": destination,
            "accepted": False,
            "artifact_status": artifact_status,
            "trust_status": trust_status,
            "decision_id": decision_id,
            "reason": reason,
        }
        self._append_jsonl(self.gate_audit_path, verdict)
        return verdict

    @staticmethod
    def _append_jsonl(path: Path | None, value: Mapping[str, Any]) -> None:
        if path is None:
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n")
