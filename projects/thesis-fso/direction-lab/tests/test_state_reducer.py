from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
REDUCER_PATH = ROOT / "tools" / "reduce_state.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("direction_lab_state_reducer", REDUCER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def _write_base(path: Path) -> None:
    path.write_text(
        yaml.safe_dump(
            {
                "schema_version": "direction-lab.canonical-state.v1",
                "state_id": "test-state",
                "baseline": {"id": "baseline.standard_cma.godard_z", "status": "canonical"},
                "formal_research_state": {"status": "BLOCKED"},
                "sandbox_state": {"status": "BOARD_READY"},
                "last_completed_batch": {"batch_id": "B002", "status": "COMPLETED_SANDBOX_VERIFIED"},
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )


def _event(reducer, base: Path, *, sequence: int = 1, previous: str | None = None) -> dict:
    event = {
        "schema_version": "direction-lab.completion-event.v1",
        "event_id": "completion.B003.verified",
        "event_type": "batch_completion_verified",
        "sequence": sequence,
        "prev_event_hash": previous,
        "pre_state": {
            "base_state_sha256": reducer.sha256(base),
            "snapshot_pointer": base.name,
            "event_head_hash": previous,
            "event_count": sequence - 1,
        },
        "batch": {
            "batch_id": "B003",
            "run_id": "run-B003",
            "status": "COMPLETED_SANDBOX_VERIFIED",
            "status_source": "batches/B003/execution-status.yaml",
            "manifest_hash": "manifest-hash",
            "result_hash": "result-hash",
            "evidence_gate": "ACCEPTED/TRUSTED",
            "verifier_verdict": "PASS",
            "promotion_effect": "none",
        },
    }
    event["event_hash"] = reducer.event_hash(event)
    return event


def test_reducer_materializes_new_completion_without_changing_base(tmp_path: Path):
    reducer = _load_module()
    base = tmp_path / "canonical-state.yaml"
    output = tmp_path / "reduced.yaml"
    events = tmp_path / "completion-events.jsonl"
    _write_base(base)
    event = _event(reducer, base)
    events.write_text(json.dumps(event, sort_keys=True) + "\n", encoding="utf-8")

    result = reducer.reduce_state(base, events, output)

    state = yaml.safe_load(output.read_text(encoding="utf-8"))
    assert state["last_completed_batch"]["batch_id"] == "B003"
    assert state["last_completed_batch"]["status"] == "COMPLETED_SANDBOX_VERIFIED"
    assert state["completion_history"][0]["batch_id"] == "B002"
    assert state["completion_history"][-1]["batch_id"] == "B003"
    assert state["state_provenance"]["base_state_sha256"] == reducer.sha256(base)
    assert state["state_provenance"]["event_count"] == 1
    assert result["event_head_hash"] == event["event_hash"]
    assert yaml.safe_load(base.read_text(encoding="utf-8"))["last_completed_batch"]["batch_id"] == "B002"


def test_reducer_rejects_duplicate_or_broken_chain(tmp_path: Path):
    reducer = _load_module()
    base = tmp_path / "canonical-state.yaml"
    output = tmp_path / "reduced.yaml"
    events = tmp_path / "completion-events.jsonl"
    _write_base(base)
    first = _event(reducer, base)
    second = _event(reducer, base, sequence=2, previous=first["event_hash"])
    second["event_id"] = first["event_id"]
    second["event_hash"] = reducer.event_hash(second)
    events.write_text(
        "\n".join(json.dumps(item, sort_keys=True) for item in (first, second)) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(reducer.StateReductionError, match="duplicate event_id"):
        reducer.reduce_state(base, events, output)


def test_reducer_rejects_stale_pre_state(tmp_path: Path):
    reducer = _load_module()
    base = tmp_path / "canonical-state.yaml"
    output = tmp_path / "reduced.yaml"
    events = tmp_path / "completion-events.jsonl"
    _write_base(base)
    event = _event(reducer, base)
    event["pre_state"]["base_state_sha256"] = "stale-state"
    event["event_hash"] = reducer.event_hash(event)
    events.write_text(json.dumps(event, sort_keys=True) + "\n", encoding="utf-8")

    with pytest.raises(reducer.StateReductionError, match="base_state_sha256"):
        reducer.reduce_state(base, events, output)


def test_reducer_rejects_referenced_evidence_hash_mismatch(tmp_path: Path):
    reducer = _load_module()
    base = tmp_path / "canonical-state.yaml"
    output = tmp_path / "reduced.yaml"
    events = tmp_path / "completion-events.jsonl"
    evidence = tmp_path / "evidence.json"
    _write_base(base)
    evidence.write_text("{}", encoding="utf-8")
    event = _event(reducer, base)
    event["evidence"] = {
        "manifest": {"path": "evidence.json", "file_sha256": "wrong-hash"}
    }
    event["event_hash"] = reducer.event_hash(event)
    events.write_text(json.dumps(event, sort_keys=True) + "\n", encoding="utf-8")

    with pytest.raises(reducer.StateReductionError, match="evidence hash mismatch"):
        reducer.reduce_state(base, events, output, repo_root=tmp_path)


def test_legacy_snapshot_resolver_falls_back_only_for_expected_state_sha(tmp_path: Path):
    reducer = _load_module()
    expected = "a" * 64
    immutable = tmp_path / "state" / "projections" / f"{expected}.yaml"
    immutable.parent.mkdir(parents=True)
    immutable.write_text("state: old\n", encoding="utf-8")
    actual_expected = reducer.sha256(immutable)
    immutable.rename(tmp_path / "state" / "projections" / f"{actual_expected}.yaml")

    resolved = reducer.resolve_legacy_snapshot("canonical-state.yaml", actual_expected, tmp_path)
    assert resolved.name == f"{actual_expected}.yaml"
    with pytest.raises(reducer.StateReductionError, match="no immutable snapshot"):
        reducer.resolve_legacy_snapshot("other.py", "b" * 64, tmp_path)
