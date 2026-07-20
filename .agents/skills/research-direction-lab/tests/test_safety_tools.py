from hashlib import sha256
import json
import multiprocessing
from pathlib import Path
import sys

import pytest


SCRIPTS = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from append_event import append_event
from hash_bundle import hash_bundle
from rebuild_state import rebuild_state
from render_status import render_status
from validate_receipt import validate_receipt


def canonical(value):
    return json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    )


def chained_record(payload, previous_head):
    unhashed = {**payload, "previous_head": previous_head}
    event_hash = sha256(canonical(unhashed).encode("utf-8")).hexdigest()
    return {**unhashed, "event_hash": event_hash}


def concurrent_append_worker(
    ledger_path, expected_head, event_id, ready_queue, start_event, result_queue
):
    ready_queue.put(event_id)
    start_event.wait()
    try:
        result = append_event(
            Path(ledger_path),
            {"event_id": event_id, "writer_fact": event_id},
            expected_head,
        )
    except Exception as exc:
        result_queue.put(("error", event_id, type(exc).__name__, str(exc)))
    else:
        result_queue.put(("ok", event_id, result))


def test_hash_bundle_sorts_paths_and_returns_known_digests(tmp_path):
    (tmp_path / "z.txt").write_text("last", encoding="utf-8")
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "a.txt").write_bytes(b"abc")

    result = hash_bundle(tmp_path, [tmp_path / "z.txt", Path("nested/a.txt")])

    assert list(result) == ["nested/a.txt", "z.txt"]
    assert result["nested/a.txt"] == (
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    )
    assert result["z.txt"] == sha256(b"last").hexdigest()
    assert hash_bundle(tmp_path, []) == {}


@pytest.mark.parametrize("bad_kind", ["traversal", "duplicate", "missing", "directory"])
def test_hash_bundle_rejects_invalid_paths(tmp_path, bad_kind):
    file_path = tmp_path / "item.txt"
    file_path.write_text("item", encoding="utf-8")

    bad_paths = {
        "traversal": [Path("..") / "outside.txt"],
        "duplicate": [Path("item.txt"), file_path],
        "missing": [Path("missing.txt")],
        "directory": [Path(".")],
    }

    with pytest.raises(ValueError):
        hash_bundle(tmp_path, bad_paths[bad_kind])


def test_hash_bundle_rejects_symlink_escape_where_supported(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_text("outside", encoding="utf-8")
    link = root / "escape.txt"
    try:
        link.symlink_to(outside)
    except (OSError, NotImplementedError):
        pytest.skip("file symlinks are unavailable in this environment")

    with pytest.raises(ValueError):
        hash_bundle(root, [link])


def test_validate_receipt_reports_stable_missing_and_mismatch_errors():
    receipt = {"same": "ok", "wrong": "actual", "extra": "permitted"}
    expected = {"wrong": "expected", "same": "ok", "absent": "value"}

    assert validate_receipt(receipt, expected) == [
        "missing:absent",
        "mismatch:wrong",
    ]


def test_append_event_builds_a_two_event_canonical_hash_chain(tmp_path):
    ledger = tmp_path / "events.jsonl"
    first_payload = {"event_id": "E001", "event_type": "OPEN", "note": "起点"}
    first_hash = append_event(ledger, first_payload, expected_head=None)
    second_payload = {"event_id": "E002", "event_type": "COMPLETED", "subject_id": "C1"}
    second_hash = append_event(ledger, second_payload, expected_head=first_hash)

    lines = ledger.read_text(encoding="utf-8").splitlines()
    first = json.loads(lines[0])
    second = json.loads(lines[1])
    assert first == chained_record(first_payload, None)
    assert second == chained_record(second_payload, first_hash)
    assert first_hash == first["event_hash"]
    assert second_hash == second["event_hash"]
    assert ledger.read_bytes() == (
        (canonical(first) + "\n" + canonical(second) + "\n").encode("utf-8")
    )


def test_append_event_rejects_replayed_event_ids(tmp_path):
    ledger = tmp_path / "events.jsonl"
    head = append_event(ledger, {"event_id": "E001"}, expected_head=None)

    with pytest.raises(ValueError):
        append_event(ledger, {"event_id": "E001", "new_fact": True}, head)


def test_append_event_wrong_expected_head_preserves_exact_bytes(tmp_path):
    ledger = tmp_path / "events.jsonl"
    append_event(ledger, {"event_id": "E001"}, expected_head=None)
    before = ledger.read_bytes()

    with pytest.raises(ValueError):
        append_event(ledger, {"event_id": "E002"}, expected_head="wrong")

    assert ledger.read_bytes() == before


def test_append_event_wrong_head_does_not_create_a_missing_ledger(tmp_path):
    ledger = tmp_path / "missing.jsonl"

    with pytest.raises(ValueError):
        append_event(ledger, {"event_id": "E001"}, expected_head="wrong")

    assert not ledger.exists()


def test_append_event_serializes_competing_processes_with_the_same_head(tmp_path):
    ledger = tmp_path / "events.jsonl"
    records = []
    head = None
    for index in range(4000):
        record = chained_record(
            {"event_id": f"BASE-{index:04d}", "padding": "x" * 128}, head
        )
        records.append(record)
        head = record["event_hash"]
    before = "".join(canonical(record) + "\n" for record in records).encode("utf-8")
    ledger.write_bytes(before)

    context = multiprocessing.get_context("spawn")
    ready_queue = context.Queue()
    result_queue = context.Queue()
    start_event = context.Event()
    processes = [
        context.Process(
            target=concurrent_append_worker,
            args=(ledger, head, event_id, ready_queue, start_event, result_queue),
        )
        for event_id in ("WRITER-A", "WRITER-B")
    ]
    for process in processes:
        process.start()
    assert {ready_queue.get(timeout=10) for _ in processes} == {"WRITER-A", "WRITER-B"}
    start_event.set()
    results = [result_queue.get(timeout=20) for _ in processes]
    for process in processes:
        process.join(timeout=10)
        if process.is_alive():
            process.terminate()
            process.join(timeout=5)
        assert process.exitcode == 0

    successes = [result for result in results if result[0] == "ok"]
    failures = [result for result in results if result[0] == "error"]
    assert len(successes) == 1, results
    assert len(failures) == 1, results

    final_bytes = ledger.read_bytes()
    assert final_bytes.startswith(before)
    appended_lines = final_bytes[len(before) :].splitlines()
    assert len(appended_lines) == 1
    appended = json.loads(appended_lines[0])
    assert appended == chained_record(
        {"event_id": successes[0][1], "writer_fact": successes[0][1]}, head
    )
    assert appended["event_hash"] == successes[0][2]


@pytest.mark.parametrize("reserved", ["previous_head", "event_hash"])
def test_append_event_rejects_caller_spoofing(tmp_path, reserved):
    with pytest.raises(ValueError):
        append_event(
            tmp_path / "events.jsonl",
            {"event_id": "E001", reserved: "spoofed"},
            expected_head=None,
        )


@pytest.mark.parametrize("corruption", ["json", "non_object", "previous_head", "hash"])
def test_append_event_rejects_corrupt_existing_chain(tmp_path, corruption):
    ledger = tmp_path / "events.jsonl"
    valid = chained_record({"event_id": "E001"}, None)
    corrupt_lines = {
        "json": "{not-json}\n",
        "non_object": "[]\n",
        "previous_head": canonical({**valid, "previous_head": "wrong"}) + "\n",
        "hash": canonical({**valid, "event_hash": "0" * 64}) + "\n",
    }
    ledger.write_text(corrupt_lines[corruption], encoding="utf-8")
    before = ledger.read_bytes()

    with pytest.raises(ValueError):
        append_event(ledger, {"event_id": "E002"}, expected_head=None)

    assert ledger.read_bytes() == before


@pytest.mark.parametrize("event_id", [None, "", "   ", 7])
def test_append_event_requires_a_nonempty_string_event_id(tmp_path, event_id):
    with pytest.raises(ValueError):
        append_event(
            tmp_path / "events.jsonl",
            {"event_id": event_id},
            expected_head=None,
        )


def test_rebuild_state_derives_only_deterministic_recorded_facts():
    events = [
        {
            "event_id": "E1",
            "event_type": "COMPLETED",
            "subject_id": "zeta",
            "event_hash": "h1",
            "next_action": "first action",
        },
        {
            "event_id": "E2",
            "event_type": "STALE",
            "subject_id": "old",
            "event_hash": "h2",
            "next_action": "",
        },
        {
            "event_id": "E3",
            "event_type": "COMPLETED",
            "subject_id": "alpha",
            "event_hash": "h3",
            "next_action": "recorded action",
        },
        {
            "event_id": "E4",
            "event_type": "COMPLETED",
            "subject_id": "alpha",
            "event_hash": "h4",
        },
    ]

    expected = {
        "completed_ids": ["alpha", "zeta"],
        "stale_ids": ["old"],
        "last_event_head": "h4",
        "recorded_next_action": "recorded action",
    }
    assert rebuild_state(events) == expected
    assert rebuild_state(iter(events)) == expected
    assert rebuild_state([]) == {
        "completed_ids": [],
        "stale_ids": [],
        "last_event_head": None,
        "recorded_next_action": None,
    }


def test_rebuild_state_rejects_replayed_event_ids():
    with pytest.raises(ValueError):
        rebuild_state([{"event_id": "same"}, {"event_id": "same"}])


@pytest.mark.parametrize("event_type", ["COMPLETED", "STALE"])
@pytest.mark.parametrize("subject_id", [None, "", "  ", 3])
def test_rebuild_state_rejects_invalid_required_subject(event_type, subject_id):
    with pytest.raises(ValueError):
        rebuild_state(
            [{"event_id": "E1", "event_type": event_type, "subject_id": subject_id}]
        )


def test_render_status_is_deterministic_and_reports_only_recorded_facts():
    adapter = {
        "formal_goal": {
            "statement": "Explore safely",
            "authorized_actions": ["inspect", "record"],
            "prohibited_actions": ["run"],
        },
        "anchor": {"scenario": "generic", "evidence_status": "VALID"},
        "ignored_adapter_fact": "not part of status contract",
    }
    state = {
        "recorded_next_action": "Inspect existing evidence",
        "last_event_head": "abc",
        "completed_ids": ["C2"],
    }
    portfolio = {
        "candidates": [
            {"candidate_id": "C2", "status": "READY"},
            {"candidate_id": "C1", "status": "BLOCKED"},
        ]
    }
    harvest = {"items": [{"item_id": "H1", "kind": "lesson"}]}

    first = render_status(adapter, state, portfolio, harvest)
    second = render_status(adapter, state, portfolio, harvest)

    assert first == second
    assert first.encode("utf-8") == second.encode("utf-8")
    for fact in (
        "Explore safely",
        "inspect",
        "generic",
        "abc",
        "C1",
        "C2",
        "H1",
        "Inspect existing evidence",
    ):
        assert fact in first
    assert "ignored_adapter_fact" not in first
    forbidden_decisions = (
        "selected candidate",
        "recommended candidate",
        "candidate ranking",
        "promote C",
    )
    assert not [phrase for phrase in forbidden_decisions if phrase in first.lower()]


def test_render_status_does_not_invent_a_next_action():
    output = render_status(
        {"formal_goal": {}, "anchor": {}},
        {"last_event_head": None},
        {"candidates": [{"candidate_id": "C9"}]},
        {},
    )

    assert "C9" in output
    assert "recorded next action" in output.lower()
    assert "none recorded" in output.lower()
