"""Small, deterministic hard-gate controller for the Direction Lab pilot.

The controller only validates a proposed action.  It never edits a manifest or
result in place; every decision is appended to an audit JSONL file.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


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

            baseline_fp = manifest.get("baseline_fingerprint")
            component_fp = manifest.get("component_fingerprint")
            if baseline_fp != baseline.get("fingerprint"):
                raise GovernanceViolation("baseline fingerprint mismatch")
            if component_fp != component.get("fingerprint"):
                if action == "REUSE_RESULT":
                    event.update({"blocked": True, "repair": "mark_stale", "reason": "component fingerprint changed"})
                    result = dict(manifest)
                    result.update({"result_status": "STALE", "blocked": True})
                    self._record(event)
                    return result
                raise GovernanceViolation("component fingerprint mismatch")

            if action in {"GO", "KILL"} and manifest.get("state") != "BOARD_READY":
                raise GovernanceViolation("GO/KILL requires BOARD_READY")
            if action == "PROMOTE" and manifest.get("evidence_status") == "PARTIAL":
                raise GovernanceViolation("PARTIAL evidence cannot be promoted")

            result = dict(manifest)
            result["blocked"] = False
            self._record(event)
            return result
        except GovernanceViolation as exc:
            event.update({"blocked": True, "reason": str(exc)})
            self._record(event)
            raise

    def _record(self, event: dict[str, Any]) -> None:
        event = dict(event)
        self.audit_events.append(event)
        with self.audit_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
