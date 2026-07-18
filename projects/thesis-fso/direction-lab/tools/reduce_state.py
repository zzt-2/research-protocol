"""Deterministically materialize Direction Lab state from immutable state + events."""

from __future__ import annotations

import argparse
import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

import yaml


SCHEMA_VERSION = "direction-lab.completion-event.v1"
FORBIDDEN_DELTA_KEYS = {"baseline", "metric_contract", "simulator", "formal_research_state", "promotion"}


class StateReductionError(ValueError):
    """Raised when an event stream cannot produce a safe state projection."""


def sha256(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def resolve_legacy_snapshot(expected_path: str | Path, expected_sha256: str, repo_root: str | Path) -> Path:
    """Resolve an old canonical-state path without weakening arbitrary source closure."""
    repo_root = Path(repo_root).resolve()
    direct = repo_root / Path(str(expected_path).replace("\\", "/"))
    if direct.is_file() and sha256(direct) == expected_sha256:
        return direct
    if Path(str(expected_path).replace("\\", "/")).name != "canonical-state.yaml":
        raise StateReductionError(f"no immutable snapshot for non-state source: {expected_path}")
    snapshot = repo_root / "state" / "projections" / f"{expected_sha256}.yaml"
    if snapshot.is_file() and sha256(snapshot) == expected_sha256:
        return snapshot
    raise StateReductionError(f"no immutable snapshot for expected SHA: {expected_sha256}")


def _canonical_json(value: Mapping[str, Any]) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def event_hash(event: Mapping[str, Any]) -> str:
    payload = {key: value for key, value in event.items() if key != "event_hash"}
    return hashlib.sha256(_canonical_json(payload)).hexdigest()


def _load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise StateReductionError(f"state must be a mapping: {path}")
    return value


def _load_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    seen_runs: set[str] = set()
    previous_hash: str | None = None
    expected_sequence = 1
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise StateReductionError(f"invalid event JSON at line {line_number}") from exc
        if not isinstance(event, dict) or event.get("schema_version") != SCHEMA_VERSION:
            raise StateReductionError(f"unknown event schema at line {line_number}")
        event_id = str(event.get("event_id", ""))
        run_id = str(event.get("batch", {}).get("run_id", "")) if isinstance(event.get("batch"), dict) else ""
        if not event_id or event_id in seen_ids:
            raise StateReductionError(f"duplicate event_id at line {line_number}")
        if not run_id or run_id in seen_runs:
            raise StateReductionError(f"duplicate run_id at line {line_number}")
        if event.get("sequence") != expected_sequence:
            raise StateReductionError(f"sequence gap or reorder at line {line_number}")
        if event.get("prev_event_hash") != previous_hash:
            raise StateReductionError(f"prev_event_hash mismatch at line {line_number}")
        if event.get("event_hash") != event_hash(event):
            raise StateReductionError(f"event_hash mismatch at line {line_number}")
        events.append(event)
        seen_ids.add(event_id)
        seen_runs.add(run_id)
        previous_hash = event["event_hash"]
        expected_sequence += 1
    return events


def _assert_immutable_sections(base: Mapping[str, Any], reduced: Mapping[str, Any]) -> None:
    for key in ("baseline", "metric_contract", "simulator", "formal_research_state"):
        if reduced.get(key) != base.get(key):
            raise StateReductionError(f"reducer changed immutable section: {key}")


def _resolve_repo_pointer(repo_root: Path, pointer: str) -> Path:
    normalized = pointer.replace("\\", "/")
    relative = Path(normalized)
    if relative.is_absolute() or ".." in relative.parts:
        raise StateReductionError(f"invalid evidence pointer: {pointer}")
    resolved = (repo_root / relative).resolve()
    if repo_root.resolve() not in resolved.parents and resolved != repo_root.resolve():
        raise StateReductionError(f"evidence pointer escapes repository: {pointer}")
    return resolved


def _validate_evidence(event: Mapping[str, Any], repo_root: Path | None) -> None:
    if repo_root is None or "evidence" not in event:
        return
    evidence = event.get("evidence")
    if not isinstance(evidence, Mapping):
        raise StateReductionError("event evidence must be a mapping")
    for label, record in evidence.items():
        if not isinstance(record, Mapping) or "path" not in record:
            continue
        file_hash = record.get("file_sha256")
        if file_hash is None:
            continue
        path = _resolve_repo_pointer(repo_root, str(record["path"]))
        if not path.is_file() or sha256(path) != file_hash:
            raise StateReductionError(f"evidence hash mismatch: {label}")


def _apply_completion(state: dict[str, Any], event: Mapping[str, Any]) -> None:
    if event.get("event_type") != "batch_completion_verified":
        raise StateReductionError(f"unsupported event_type: {event.get('event_type')}")
    batch = event.get("batch")
    if not isinstance(batch, Mapping):
        raise StateReductionError("completion event batch must be a mapping")
    evidence = event.get("evidence")
    if isinstance(evidence, Mapping):
        manifest = evidence.get("manifest")
        ledger = evidence.get("ledger")
        if isinstance(manifest, Mapping) and not batch.get("manifest_hash"):
            batch = dict(batch)
            batch["manifest_hash"] = manifest.get("manifest_hash")
        if isinstance(ledger, Mapping) and not batch.get("result_hash"):
            batch = dict(batch)
            batch["result_hash"] = ledger.get("result_hash")
        execution_status = evidence.get("execution_status")
        verifier = evidence.get("verifier")
        if isinstance(execution_status, Mapping) and not batch.get("evidence_gate"):
            batch = dict(batch)
            batch["evidence_gate"] = execution_status.get("evidence_gate")
        if isinstance(verifier, Mapping) and not batch.get("verifier_verdict"):
            batch = dict(batch)
            batch["verifier_verdict"] = verifier.get("verdict")
    required = ("batch_id", "run_id", "status", "status_source", "manifest_hash", "result_hash")
    missing = [key for key in required if not str(batch.get(key, "")).strip()]
    if missing:
        raise StateReductionError(f"completion event missing batch fields: {missing}")
    if batch.get("status") != "COMPLETED_SANDBOX_VERIFIED":
        raise StateReductionError("completion event status must be COMPLETED_SANDBOX_VERIFIED")
    if batch.get("evidence_gate") != "ACCEPTED/TRUSTED":
        raise StateReductionError("completion event requires ACCEPTED/TRUSTED evidence gate")
    if batch.get("verifier_verdict") != "PASS":
        raise StateReductionError("completion event requires verifier PASS")
    delta = event.get("state_delta", {})
    if not isinstance(delta, Mapping):
        delta = {}
    forbidden = sorted(FORBIDDEN_DELTA_KEYS & set(delta))
    if forbidden:
        raise StateReductionError(f"forbidden state delta: {forbidden}")
    previous = deepcopy(state.get("last_completed_batch"))
    history = list(state.get("completion_history", []))
    if previous and not history:
        history.append(previous)
    if any(item.get("batch_id") == batch["batch_id"] for item in history if isinstance(item, Mapping)):
        raise StateReductionError(f"duplicate completed batch: {batch['batch_id']}")
    completion = {
        "batch_id": batch["batch_id"],
        "status": batch["status"],
        "run_id": batch["run_id"],
        "status_source": batch["status_source"],
        "manifest_hash": batch["manifest_hash"],
        "result_hash": batch["result_hash"],
        "promotion_effect": batch.get("promotion_effect", "none"),
    }
    if isinstance(delta.get("runtime_rule_observations"), Mapping):
        completion["runtime_rule_observations"] = deepcopy(delta["runtime_rule_observations"])
    history.append(completion)
    state["completion_history"] = history
    state["last_completed_batch"] = completion


def reduce_state(
    base_path: str | Path,
    events_path: str | Path,
    output_path: str | Path,
    *,
    repo_root: str | Path | None = None,
) -> dict[str, Any]:
    base_path, events_path, output_path = Path(base_path), Path(events_path), Path(output_path)
    base = _load_yaml(base_path)
    base_hash = sha256(base_path)
    events = _load_events(events_path)
    state = deepcopy(base)
    for event in events:
        pre_state = event.get("pre_state")
        if not isinstance(pre_state, Mapping) or pre_state.get("base_state_sha256") != base_hash:
            raise StateReductionError("base_state_sha256 does not match immutable base projection")
        _validate_evidence(event, Path(repo_root) if repo_root is not None else None)
        _apply_completion(state, event)
    head = events[-1] if events else None
    state["state_provenance"] = {
        "base_state_sha256": base_hash,
        "event_count": len(events),
        "head_sequence": head.get("sequence") if head else 0,
        "head_event_id": head.get("event_id") if head else None,
        "head_event_hash": head.get("event_hash") if head else None,
        "event_log_sha256": sha256(events_path),
    }
    _assert_immutable_sections(base, state)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(yaml.safe_dump(state, sort_keys=False, allow_unicode=True), encoding="utf-8", newline="\n")
    return {
        "base_state_sha256": base_hash,
        "event_count": len(events),
        "event_head_hash": head.get("event_hash") if head else None,
        "output_sha256": sha256(output_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_state", type=Path)
    parser.add_argument("events", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--repo-root", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(reduce_state(args.base_state, args.events, args.output, repo_root=args.repo_root), sort_keys=True))
    except StateReductionError as exc:
        print(f"FAIL: {exc}")
        return 1
    print(f"PASS: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
