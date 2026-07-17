"""Small, deterministic hard-gate controller for the Direction Lab pilot.

The controller only validates a proposed action.  It never edits a manifest or
result in place; every decision is appended to an audit JSONL file.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping


ALLOWED_ACTIONS = {"RUN", "GO", "KILL", "PROMOTE", "REUSE_RESULT"}
PROMOTABLE_EVIDENCE = {"FULL", "VERIFIED_RUN", "PAPER_READY"}


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
            if action != "REUSE_RESULT" and component.get("status") != "canonical":
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
                result.update({"result_status": "STALE", "blocked": True})
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
            self._record(event)
            return result
        except GovernanceViolation as exc:
            event.update({"blocked": True, "reason": str(exc)})
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
        return operation()

    def _record(self, event: dict[str, Any]) -> None:
        event = dict(event)
        self.audit_events.append(event)
        with self.audit_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
