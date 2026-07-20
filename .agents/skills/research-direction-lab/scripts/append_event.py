from collections.abc import Mapping
from contextlib import contextmanager
from hashlib import sha256
import json
import os
from pathlib import Path


_RESERVED_FIELDS = {"previous_head", "event_hash"}


if os.name == "nt":
    import msvcrt

    @contextmanager
    def _exclusive_ledger_lock(stream):
        stream.seek(0)
        msvcrt.locking(stream.fileno(), msvcrt.LK_LOCK, 1)
        try:
            yield
        finally:
            stream.seek(0)
            msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)

elif os.name == "posix":
    import fcntl

    @contextmanager
    def _exclusive_ledger_lock(stream):
        fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(stream.fileno(), fcntl.LOCK_UN)

else:

    @contextmanager
    def _exclusive_ledger_lock(stream):
        raise RuntimeError(f"unsupported file-locking platform: {os.name}")
        yield


def _canonical(record: Mapping[str, object]) -> str:
    return json.dumps(
        record,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    )


def _hash_record(record: Mapping[str, object]) -> str:
    return sha256(_canonical(record).encode("utf-8")).hexdigest()


def _verified_ledger(raw: bytes) -> tuple[str | None, set[str]]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("ledger is not valid UTF-8") from exc

    current_head: str | None = None
    event_ids: set[str] = set()
    for line in text.splitlines():
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError("ledger contains corrupt JSON") from exc
        if not isinstance(record, dict):
            raise ValueError("ledger record must be an object")

        event_id = record.get("event_id")
        if not isinstance(event_id, str) or not event_id.strip():
            raise ValueError("ledger record has invalid event_id")
        if event_id in event_ids:
            raise ValueError("ledger contains a replayed event_id")
        if record.get("previous_head") != current_head:
            raise ValueError("ledger hash chain is broken")

        stored_hash = record.get("event_hash")
        unhashed = {key: value for key, value in record.items() if key != "event_hash"}
        if not isinstance(stored_hash, str) or stored_hash != _hash_record(unhashed):
            raise ValueError("ledger record hash is incorrect")

        event_ids.add(event_id)
        current_head = stored_hash
    return current_head, event_ids


def append_event(
    path: Path, event: Mapping[str, object], expected_head: str | None
) -> str:
    if _RESERVED_FIELDS.intersection(event):
        raise ValueError("caller may not provide reserved fields")
    event_id = event.get("event_id")
    if not isinstance(event_id, str) or not event_id.strip():
        raise ValueError("event_id must be a non-empty string")

    ledger = Path(path)
    if not ledger.exists() and expected_head is not None:
        raise ValueError("expected head does not match current head")
    if ledger.exists() and not ledger.is_file():
        raise ValueError("ledger path must be a file")
    with ledger.open("a+b") as stream:
        with _exclusive_ledger_lock(stream):
            stream.seek(0)
            raw = stream.read()
            current_head, event_ids = _verified_ledger(raw)
            if event_id in event_ids:
                raise ValueError("event_id has already been recorded")
            if expected_head != current_head:
                raise ValueError("expected head does not match current head")

            unhashed = {**dict(event), "previous_head": current_head}
            event_hash = _hash_record(unhashed)
            record = {**unhashed, "event_hash": event_hash}
            encoded = (_canonical(record) + "\n").encode("utf-8")
            prefix = b"\n" if raw and not raw.endswith((b"\n", b"\r")) else b""
            stream.seek(0, os.SEEK_END)
            stream.write(prefix + encoded)
            stream.flush()
            os.fsync(stream.fileno())
    return event_hash
