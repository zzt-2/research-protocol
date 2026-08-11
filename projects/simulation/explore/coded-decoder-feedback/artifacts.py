"""Strict canonical serialization and crash-fail-closed artifact writes.

This module owns mechanics only.  It does not know scientific rows, run a
simulation, or create a directory merely by being imported.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
import errno
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import tempfile
from typing import Any
import uuid
import weakref


DEV_ARTIFACT_NAMES = (
    "dev_manifest.json",
    "raw_bps_dev.jsonl",
    "hmm_grid_dev_chunks.jsonl",
    "raw_b2_tuple_clean_dev.jsonl",
    "raw_b2_tuple_controlled_dev.jsonl",
    "dev_freeze.json",
    "dev_freeze_receipt.json",
)

REQUIRED_BUNDLE_BINDINGS = (
    "owner_sha256",
    "contract_sha256",
    "source_sha256",
    "code_sha256",
    "manifest_sha256",
    "raw_sha256",
    "chunk_sha256",
    "freeze_sha256",
    "selection_sha256",
    "seed_sha256",
    "summary_sha256",
    "ledger_sha256",
)

_SHA256_LENGTH = 64
_JSONL_SORT_KEYS: dict[str, tuple[str, ...]] = {
    "raw_bps_dev.jsonl": ("tuple_id", "B", "Nw", "seed", "cell_id", "polarization"),
    "hmm_grid_dev_chunks.jsonl": (
        "tuple_id", "p_s_index", "sigma_e2_index", "stratum_role", "cell_id",
        "polarization", "chunk_id",
    ),
    "raw_b2_tuple_clean_dev.jsonl": ("tuple_id", "seed", "cell_id", "polarization"),
    "raw_b2_tuple_controlled_dev.jsonl": (
        "tuple_id", "seed", "cell_id", "target_polarization", "fixture_id",
        "row_polarization",
    ),
    "decoder_hard_outputs.jsonl": ("decoder_hard_output_sha256",),
    "ordinary_consumer_provenance.jsonl": ("payload.logical_computation_id",),
}


class ArtifactError(ValueError):
    """An artifact is not canonically serializable or fails its contract."""


@dataclass(frozen=True, slots=True)
class ArtifactReceipt:
    logical_name: str
    sha256: str
    byte_count: int
    record_count: int
    directory_fsync_status: str


@dataclass(frozen=True, slots=True)
class BundleReceipt:
    generation: str
    receipt_logical_name: str
    bindings: tuple[tuple[str, str], ...]
    artifacts: tuple[ArtifactReceipt, ...]
    receipt_sha256: str
    receipt_byte_count: int
    directory_fsync_status: str
    complete: bool


@dataclass(frozen=True, slots=True, init=False, weakref_slot=True)
class EvidenceReceipt:
    """Hash binding for one independently materialized engineering check."""

    logical_name: str
    sha256: str
    byte_count: int

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        raise ArtifactError("EvidenceReceipt construction is controlled by exact bytes")


_EVIDENCE_ISSUANCE: dict[int, tuple[weakref.ReferenceType[EvidenceReceipt], tuple[str, str, int]]] = {}


def _register_evidence_receipt(receipt: EvidenceReceipt) -> None:
    marker = id(receipt)

    def discard(reference: weakref.ReferenceType[EvidenceReceipt], *, key: int = marker) -> None:
        current = _EVIDENCE_ISSUANCE.get(key)
        if current is not None and current[0] is reference:
            _EVIDENCE_ISSUANCE.pop(key, None)

    _EVIDENCE_ISSUANCE[marker] = (
        weakref.ref(receipt, discard),
        (receipt.logical_name, receipt.sha256, receipt.byte_count),
    )


def assert_evidence_receipt(receipt: EvidenceReceipt) -> None:
    """Reject caller-forged or post-construction-mutated evidence receipts."""

    if type(receipt) is not EvidenceReceipt:
        raise ArtifactError("issued EvidenceReceipt required")
    issued = _EVIDENCE_ISSUANCE.get(id(receipt))
    fingerprint = (receipt.logical_name, receipt.sha256, receipt.byte_count)
    if issued is None or issued[0]() is not receipt or issued[1] != fingerprint:
        raise ArtifactError("EvidenceReceipt was not issued from exact bytes")


def build_evidence_receipt(logical_name: str, exact_bytes: bytes) -> EvidenceReceipt:
    """Bind evidence to its actual bytes; caller-supplied digests are forbidden."""

    name = _safe_logical_name(logical_name)
    if type(exact_bytes) is not bytes or not exact_bytes:
        raise ArtifactError("evidence must be non-empty exact bytes")
    receipt = object.__new__(EvidenceReceipt)
    object.__setattr__(receipt, "logical_name", name)
    object.__setattr__(receipt, "sha256", hashlib.sha256(exact_bytes).hexdigest())
    object.__setattr__(receipt, "byte_count", len(exact_bytes))
    _register_evidence_receipt(receipt)
    return receipt


def _plain_json_tree(value: Any, active: set[int] | None = None) -> Any:
    """Copy mappings (including MappingProxy) into a strict JSON value tree."""

    if active is None:
        active = set()
    if value is None or type(value) in (bool, int, str):
        return value
    if type(value) is float:
        if not math.isfinite(value):
            raise ArtifactError("JSON floats must be finite")
        return value
    if isinstance(value, Mapping):
        marker = id(value)
        if marker in active:
            raise ArtifactError("cyclic JSON mapping")
        active.add(marker)
        try:
            result: dict[str, Any] = {}
            for key, item in value.items():
                if type(key) is not str:
                    raise ArtifactError("JSON mapping keys must be exact strings")
                result[key] = _plain_json_tree(item, active)
            return result
        finally:
            active.remove(marker)
    if type(value) in (list, tuple):
        marker = id(value)
        if marker in active:
            raise ArtifactError("cyclic JSON sequence")
        active.add(marker)
        try:
            return [_plain_json_tree(item, active) for item in value]
        finally:
            active.remove(marker)
    raise ArtifactError(f"unsupported JSON value type: {type(value).__name__}")


def canonical_json_bytes(value: Any) -> bytes:
    """Return the sole accepted UTF-8 representation of a strict JSON value."""

    plain = _plain_json_tree(value)
    return json.dumps(
        plain,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _normalize_sort_key(sort_key: str | Sequence[str] | None) -> tuple[str, ...]:
    if type(sort_key) is str:
        keys = (sort_key,)
    elif type(sort_key) in (tuple, list):
        keys = tuple(sort_key)
    else:
        raise ArtifactError("a sort key is required for canonical JSONL")
    if not keys or any(type(key) is not str or not key or key.startswith(".")
                       or key.endswith(".") or ".." in key for key in keys):
        raise ArtifactError("sort keys must be non-empty dotted field names")
    if len(set(keys)) != len(keys):
        raise ArtifactError("sort-key fields must be unique")
    return keys


def _field_at(row: Mapping[str, Any], dotted: str) -> Any:
    value: Any = row
    for component in dotted.split("."):
        if not isinstance(value, Mapping) or component not in value:
            raise ArtifactError(f"missing JSONL sort-key field: {dotted}")
        value = value[component]
    return value


def _sortable_atom(value: Any) -> tuple[int, Any]:
    if type(value) is str:
        return (0, value)
    if type(value) is int:
        return (1, value)
    if type(value) is float and math.isfinite(value):
        return (2, value)
    raise ArtifactError("sort-key atoms must be finite string/int/float scalars")


def _validate_schema(rows: tuple[dict[str, Any], ...], schema: Any) -> tuple[str, ...] | None:
    if schema is None:
        return None
    if callable(schema):
        schema(rows)
        return None
    if not isinstance(schema, Mapping):
        raise ArtifactError("schema must be a mapping or whole-table validator")
    exact = schema.get("exact_cardinality")
    if exact is not None and (type(exact) is not int or len(rows) != exact):
        raise ArtifactError(f"exact cardinality mismatch: {len(rows)} != {exact}")
    required = schema.get("required_fields", ())
    if type(required) not in (tuple, list) or any(type(field) is not str for field in required):
        raise ArtifactError("required_fields must be a string sequence")
    for row in rows:
        missing = [field for field in required if field not in row]
        if missing:
            raise ArtifactError(f"missing required fields: {missing}")
    for rule in schema.get("foreign_keys", ()):
        if not isinstance(rule, Mapping) or type(rule.get("field")) is not str:
            raise ArtifactError("foreign-key rules require field and values")
        allowed = tuple(rule.get("values", ()))
        field = rule["field"]
        for row in rows:
            if field not in row or row[field] not in allowed:
                raise ArtifactError(f"foreign-key violation: {field}")
    validator = schema.get("validator")
    if validator is not None:
        if not callable(validator):
            raise ArtifactError("validator must be callable")
        validator(rows)
    manifest_validator = schema.get("manifest_validator")
    if manifest_validator is not None:
        if not callable(manifest_validator):
            raise ArtifactError("manifest_validator must be callable")
        manifest_validator(rows)
    key = schema.get("sort_key", schema.get("primary_key"))
    return None if key is None else _normalize_sort_key(key)


def _prepare_jsonl(
    rows: Iterable[Mapping[str, Any]],
    *,
    sort_key: str | Sequence[str] | None,
    schema: Any = None,
) -> tuple[bytes, tuple[dict[str, Any], ...]]:
    try:
        materialized = tuple(_plain_json_tree(row) for row in rows)
    except TypeError as exc:
        raise ArtifactError("rows must be iterable") from exc
    if any(type(row) is not dict for row in materialized):
        raise ArtifactError("every JSONL record must be a mapping")
    schema_key = _validate_schema(materialized, schema)
    keys = _normalize_sort_key(sort_key) if sort_key is not None else schema_key
    if keys is None:
        raise ArtifactError("schema or call must supply a JSONL sort key")
    decorated: list[tuple[tuple[tuple[int, Any], ...], dict[str, Any]]] = []
    seen: set[tuple[tuple[int, Any], ...]] = set()
    for row in materialized:
        key = tuple(_sortable_atom(_field_at(row, field)) for field in keys)
        if key in seen:
            raise ArtifactError("duplicate JSONL sort/primary key")
        seen.add(key)
        decorated.append((key, row))
    decorated.sort(key=lambda item: item[0])
    ordered = tuple(item[1] for item in decorated)
    payload = b"".join(canonical_json_bytes(row) + b"\n" for row in ordered)
    return payload, ordered


def canonical_jsonl_bytes(
    rows: Iterable[Mapping[str, Any]],
    *,
    sort_key: str | Sequence[str],
) -> bytes:
    return _prepare_jsonl(rows, sort_key=sort_key)[0]


def _emit(hook: Callable[[str, Path], None] | None, event: str, path: Path) -> None:
    if hook is not None:
        hook(event, path)


def _fsync_directory(path: Path) -> tuple[str, str | None]:
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    descriptor: int | None = None
    try:
        descriptor = os.open(path, flags)
        os.fsync(descriptor)
        return "SUPPORTED", None
    except OSError as exc:
        unsupported = {
            errno.EACCES, errno.EBADF, errno.EINVAL, errno.ENOTSUP,
            getattr(errno, "EOPNOTSUPP", errno.ENOTSUP),
        }
        if exc.errno in unsupported or getattr(exc, "winerror", None) in (5, 6, 50):
            return "UNSUPPORTED", f"{type(exc).__name__}:{exc.errno}"
        raise
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _write_bytes_atomic(
    target: Path,
    payload: bytes,
    *,
    event_hook: Callable[[str, Path], None] | None = None,
) -> tuple[str, bytes]:
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(
        dir=target.parent, prefix=f".{target.name}.", suffix=".tmp"
    )
    temp_path = Path(temp_name)
    _emit(event_hook, "temp_created", temp_path)
    replaced = False
    try:
        with os.fdopen(descriptor, "wb") as stream:
            descriptor = -1
            stream.write(payload)
            _emit(event_hook, "written", temp_path)
            stream.flush()
            _emit(event_hook, "flushed", temp_path)
            os.fsync(stream.fileno())
            _emit(event_hook, "file_fsynced", temp_path)
        _emit(event_hook, "closed", temp_path)
        os.replace(temp_path, target)
        replaced = True
        _emit(event_hook, "replaced", target)
        _emit(event_hook, "directory_fsync_attempted", target.parent)
        status, _reason = _fsync_directory(target.parent)
        _emit(event_hook, "directory_fsync_recorded", target.parent)
        landed = target.read_bytes()
        if landed != payload:
            raise ArtifactError("landed bytes differ from the fully materialized payload")
        return status, landed
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if not replaced:
            try:
                temp_path.unlink()
            except FileNotFoundError:
                pass


def write_jsonl_atomic(
    path: str | os.PathLike[str],
    rows: Iterable[Mapping[str, Any]],
    schema: Any = None,
    *,
    sort_key: str | Sequence[str] | None = None,
    validator: Callable[[tuple[dict[str, Any], ...]], None] | None = None,
    logical_name: str | None = None,
    event_hook: Callable[[str, Path], None] | None = None,
) -> ArtifactReceipt:
    """Validate/materialize first, then replace one JSONL file atomically."""

    payload, materialized = _prepare_jsonl(rows, sort_key=sort_key, schema=schema)
    if validator is not None:
        if not callable(validator):
            raise ArtifactError("validator must be callable")
        validator(materialized)
    target = Path(path)
    name = target.name if logical_name is None else logical_name
    if type(name) is not str or not name or Path(name).name != name:
        raise ArtifactError("logical_name must be one safe basename")
    status, landed = _write_bytes_atomic(target, payload, event_hook=event_hook)
    return ArtifactReceipt(
        logical_name=name,
        sha256=hashlib.sha256(landed).hexdigest(),
        byte_count=len(landed),
        record_count=len(materialized),
        directory_fsync_status=status,
    )


def _safe_logical_name(name: Any) -> str:
    if type(name) is not str or not name or Path(name).name != name or name in (".", ".."):
        raise ArtifactError("artifact logical names must be safe basenames")
    return name


def _bundle_sort_key(name: str, rows: tuple[dict[str, Any], ...]) -> tuple[str, ...]:
    candidates = _JSONL_SORT_KEYS.get(name)
    if candidates is None:
        raise ArtifactError(f"no canonical sort key registered for {name}")
    # Synthetic unit slices may carry only a prefix of a real compound key.  The
    # full owner rows carry every component, so the complete primary key is used.
    present = tuple(key for key in candidates if all(
        isinstance(_field_at(row, key.rsplit(".", 1)[0]), Mapping)
        and key.rsplit(".", 1)[1] in _field_at(row, key.rsplit(".", 1)[0])
        if "." in key else key in row
        for row in rows
    ))
    if not present:
        raise ArtifactError(f"registered sort key absent from {name}")
    return present


def _artifact_payload(name: str, value: Any, schema: Any) -> tuple[bytes, int]:
    if name.endswith(".jsonl"):
        materialized = tuple(_plain_json_tree(row) for row in value)
        if any(type(row) is not dict for row in materialized):
            raise ArtifactError(f"{name} records must be mappings")
        key = _bundle_sort_key(name, materialized)
        payload, rows = _prepare_jsonl(materialized, sort_key=key, schema=schema)
        return payload, len(rows)
    if not name.endswith(".json"):
        raise ArtifactError("bundle core accepts only canonical .json/.jsonl")
    plain = _plain_json_tree(value)
    if schema is not None:
        if not callable(schema):
            raise ArtifactError("JSON document schema must be callable")
        schema(plain)
    return canonical_json_bytes(plain), 1


def _artifact_receipt_payload(item: ArtifactReceipt) -> dict[str, Any]:
    return {
        "logical_name": item.logical_name,
        "sha256": item.sha256,
        "byte_count": item.byte_count,
        "record_count": item.record_count,
        "directory_fsync_status": item.directory_fsync_status,
    }


def _validate_bindings(bindings: Mapping[str, str]) -> tuple[tuple[str, str], ...]:
    plain = _plain_json_tree(bindings)
    if type(plain) is not dict or tuple(sorted(plain)) != tuple(sorted(REQUIRED_BUNDLE_BINDINGS)):
        raise ArtifactError("bundle bindings must contain the exact required logical names")
    for name, digest in plain.items():
        if (type(digest) is not str or len(digest) != _SHA256_LENGTH
                or any(character not in "0123456789abcdef" for character in digest)):
            raise ArtifactError(f"binding {name} must be lowercase SHA256")
    return tuple((name, plain[name]) for name in sorted(plain))


def write_bundle_atomic(
    root: str | os.PathLike[str],
    files: Mapping[str, Any],
    *,
    bindings: Mapping[str, str],
    receipt_name: str = "receipt.json",
    required_names: Sequence[str] | None = None,
    schemas: Mapping[str, Any] | None = None,
    validator: Callable[[Mapping[str, Any]], None] | None = None,
    event_hook: Callable[[str, Path], None] | None = None,
) -> BundleReceipt:
    """Publish an immutable generation, then atomically swing ``CURRENT.json``.

    The old pointer is not touched until every data byte and the receipt have
    landed and been re-read.  Thus an injected failure leaves an already valid
    generation readable instead of merely detecting a torn replacement.
    """

    receipt_name = _safe_logical_name(receipt_name)
    if not isinstance(files, Mapping):
        raise ArtifactError("files must be a logical-name mapping")
    file_names = tuple(_safe_logical_name(name) for name in files)
    if len(set(file_names)) != len(file_names) or receipt_name in files:
        raise ArtifactError("duplicate names or caller-supplied receipt forbidden")
    expected = tuple(file_names) + (receipt_name,) if required_names is None else tuple(
        _safe_logical_name(name) for name in required_names
    )
    if len(set(expected)) != len(expected) or set(expected) != set(file_names) | {receipt_name}:
        raise ArtifactError("required_names must exactly equal data files plus receipt")
    data_order = tuple(name for name in expected if name != receipt_name)
    binding_items = _validate_bindings(bindings)
    schema_map = {} if schemas is None else dict(schemas)

    prepared: dict[str, bytes] = {}
    counts: dict[str, int] = {}
    for name in data_order:
        prepared[name], counts[name] = _artifact_payload(name, files[name], schema_map.get(name))
    if validator is not None:
        if not callable(validator):
            raise ArtifactError("bundle validator must be callable")
        validator(_plain_json_tree(files))

    generation = "generation-" + uuid.uuid4().hex
    artifact_receipts = tuple(
        ArtifactReceipt(
            logical_name=name,
            sha256=hashlib.sha256(prepared[name]).hexdigest(),
            byte_count=len(prepared[name]),
            record_count=counts[name],
            directory_fsync_status="DEFERRED_TO_ATOMIC_POINTER",
        )
        for name in data_order
    )
    receipt_document = {
        "schema": "coded_decoder_feedback.d0.bundle_receipt.v1",
        "complete": True,
        "receipt_logical_name": receipt_name,
        "required_names": list(expected),
        "bindings": [
            {"logical_name": name, "sha256": digest} for name, digest in binding_items
        ],
        "artifacts": [_artifact_receipt_payload(item) for item in artifact_receipts],
        "directory_fsync_status": "DEFERRED_TO_ATOMIC_POINTER",
    }
    receipt_bytes = canonical_json_bytes(receipt_document)
    receipt_sha256 = hashlib.sha256(receipt_bytes).hexdigest()
    pointer_bytes = canonical_json_bytes({
        "schema": "coded_decoder_feedback.d0.bundle_pointer.v1",
        "generation": generation,
        "receipt_logical_name": receipt_name,
        "receipt_sha256": receipt_sha256,
    })

    bundle_root = Path(root)
    generations_root = bundle_root / ".generations"
    generation_path = generations_root / generation
    pointer_committed = False
    pointer_replaced = False

    def pointer_event(event: str, path: Path) -> None:
        nonlocal pointer_replaced
        if event == "replaced":
            pointer_replaced = True
        _emit(event_hook, event, path)

    try:
        generations_root.mkdir(parents=True, exist_ok=True)
        generation_path.mkdir()
        for name in data_order:
            _write_bytes_atomic(generation_path / name, prepared[name])
            if (generation_path / name).read_bytes() != prepared[name]:
                raise ArtifactError(f"post-write byte verification failed for {name}")
            _emit(event_hook, "bundle_artifact_committed", generation_path / name)
        _write_bytes_atomic(generation_path / receipt_name, receipt_bytes)
        _emit(event_hook, "bundle_artifact_committed", generation_path / receipt_name)
        _validate_generation(generation_path, expected, receipt_name, receipt_sha256)
        _emit(event_hook, "bundle_before_pointer", bundle_root / "CURRENT.json")
        pointer_status, _landed = _write_bytes_atomic(
            bundle_root / "CURRENT.json", pointer_bytes, event_hook=pointer_event
        )
        pointer_committed = True
        _emit(event_hook, "bundle_pointer_committed", bundle_root / "CURRENT.json")
    except BaseException:
        if not pointer_committed and not pointer_replaced and generation_path.exists():
            shutil.rmtree(generation_path)
        raise
    return BundleReceipt(
        generation=generation,
        receipt_logical_name=receipt_name,
        bindings=binding_items,
        artifacts=artifact_receipts,
        receipt_sha256=receipt_sha256,
        receipt_byte_count=len(receipt_bytes),
        directory_fsync_status=pointer_status,
        complete=True,
    )


def _parse_canonical_json(path: Path) -> tuple[dict[str, Any], bytes]:
    try:
        payload = path.read_bytes()
        document = json.loads(payload.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ArtifactError(f"missing or invalid canonical JSON: {path.name}") from exc
    if type(document) is not dict or canonical_json_bytes(document) != payload:
        raise ArtifactError(f"non-canonical JSON bytes: {path.name}")
    return document, payload


def _validate_generation(
    generation_path: Path,
    required_names: Sequence[str],
    receipt_name: str,
    pointer_receipt_sha256: str,
) -> BundleReceipt:
    expected = tuple(required_names)
    actual = tuple(sorted(path.name for path in generation_path.iterdir() if path.is_file()))
    if set(actual) != set(expected) or len(actual) != len(expected):
        raise ArtifactError("bundle has missing or extra logical names")
    receipt_doc, receipt_bytes = _parse_canonical_json(generation_path / receipt_name)
    actual_receipt_sha = hashlib.sha256(receipt_bytes).hexdigest()
    if actual_receipt_sha != pointer_receipt_sha256:
        raise ArtifactError("receipt hash does not match the landed exact bytes")
    if (
        receipt_doc.get("schema") != "coded_decoder_feedback.d0.bundle_receipt.v1"
        or receipt_doc.get("complete") is not True
        or receipt_doc.get("receipt_logical_name") != receipt_name
        or tuple(receipt_doc.get("required_names", ())) != expected
    ):
        raise ArtifactError("receipt identity/completeness mismatch")
    raw_bindings = receipt_doc.get("bindings")
    if type(raw_bindings) is not list:
        raise ArtifactError("receipt bindings missing")
    try:
        binding_map = {item["logical_name"]: item["sha256"] for item in raw_bindings}
    except (TypeError, KeyError) as exc:
        raise ArtifactError("receipt bindings malformed") from exc
    binding_items = _validate_bindings(binding_map)
    if len(raw_bindings) != len(binding_items):
        raise ArtifactError("duplicate receipt binding logical name")
    raw_artifacts = receipt_doc.get("artifacts")
    if type(raw_artifacts) is not list:
        raise ArtifactError("receipt artifacts missing")
    artifacts: list[ArtifactReceipt] = []
    names: set[str] = set()
    for raw in raw_artifacts:
        if type(raw) is not dict:
            raise ArtifactError("artifact receipt malformed")
        try:
            name = _safe_logical_name(raw["logical_name"])
            item = ArtifactReceipt(
                logical_name=name,
                sha256=raw["sha256"],
                byte_count=raw["byte_count"],
                record_count=raw["record_count"],
                directory_fsync_status=raw["directory_fsync_status"],
            )
        except (KeyError, TypeError) as exc:
            raise ArtifactError("artifact receipt fields malformed") from exc
        if name in names or name == receipt_name:
            raise ArtifactError("duplicate/wrong artifact logical name")
        names.add(name)
        landed = (generation_path / name).read_bytes()
        if type(item.byte_count) is not int or len(landed) != item.byte_count:
            raise ArtifactError(f"artifact byte count mismatch: {name}")
        if hashlib.sha256(landed).hexdigest() != item.sha256:
            raise ArtifactError(f"artifact hash mismatch: {name}")
        if name.endswith(".jsonl"):
            if landed and not landed.endswith(b"\n"):
                raise ArtifactError(f"JSONL terminal LF missing: {name}")
            lines = landed.splitlines()
            if len(lines) != item.record_count:
                raise ArtifactError(f"artifact record count mismatch: {name}")
            for line in lines:
                parsed = json.loads(line.decode("utf-8"))
                if canonical_json_bytes(parsed) != line:
                    raise ArtifactError(f"non-canonical JSONL record: {name}")
        else:
            _parse_canonical_json(generation_path / name)
            if item.record_count != 1:
                raise ArtifactError(f"JSON document record count mismatch: {name}")
        artifacts.append(item)
    if names != set(expected) - {receipt_name}:
        raise ArtifactError("receipt omits or adds an artifact logical name")
    return BundleReceipt(
        generation=generation_path.name,
        receipt_logical_name=receipt_name,
        bindings=binding_items,
        artifacts=tuple(artifacts),
        receipt_sha256=actual_receipt_sha,
        receipt_byte_count=len(receipt_bytes),
        directory_fsync_status=receipt_doc.get("directory_fsync_status", "MISSING"),
        complete=True,
    )


def validate_complete_bundle(
    root: str | os.PathLike[str],
    *,
    required_names: Sequence[str],
    receipt_name: str = "receipt.json",
) -> BundleReceipt:
    """Resolve only the atomic pointer and fail closed on any byte/name drift."""

    bundle_root = Path(root)
    receipt_name = _safe_logical_name(receipt_name)
    expected = tuple(_safe_logical_name(name) for name in required_names)
    pointer, pointer_bytes = _parse_canonical_json(bundle_root / "CURRENT.json")
    if (
        pointer.get("schema") != "coded_decoder_feedback.d0.bundle_pointer.v1"
        or pointer.get("receipt_logical_name") != receipt_name
        or type(pointer.get("generation")) is not str
        or not pointer["generation"].startswith("generation-")
        or type(pointer.get("receipt_sha256")) is not str
    ):
        raise ArtifactError("bundle pointer identity mismatch")
    generation = pointer["generation"]
    if Path(generation).name != generation:
        raise ArtifactError("unsafe bundle generation")
    return _validate_generation(
        bundle_root / ".generations" / generation,
        expected,
        receipt_name,
        pointer["receipt_sha256"],
    )
