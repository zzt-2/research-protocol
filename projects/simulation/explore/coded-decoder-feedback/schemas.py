"""Pure, fail-closed value schemas for the frozen D0 v3 tables.

No I/O, selection, reduction, RNG, runner, or scientific execution belongs
in this module.
"""

from __future__ import annotations

from collections import Counter
import base64
from copy import deepcopy
from dataclasses import dataclass, fields, is_dataclass, make_dataclass, replace
from functools import lru_cache
from fractions import Fraction
import hashlib
from itertools import product
import json
import math
import re
from types import MappingProxyType
from typing import Any, Mapping
import weakref

import numpy as np

from contract import (
    ContractError,
    D0Contract,
    D0OwnerIdentityAuthority,
    assert_frozen_d0_identity,
    assert_frozen_owner_identity_authority,
)


class SchemaError(ValueError):
    """A row or relational bundle violates the machine-owned contract."""


_DECODER_HARD_OUTPUT_SCHEMA = "coded_decoder_feedback.d0.decoder_hard_output.v1"
_DECODER_HARD_OUTPUT_STORE_SCHEMA = (
    "coded_decoder_feedback.d0.decoder_hard_output_store_record.v1"
)
_DECODER_HARD_OUTPUT_FIELDS = (
    "schema",
    "cw_count",
    "information_bits_per_cw",
    "cw_order",
    "bit_packing",
    "decoded_information_bits_base64",
)
_DECODER_HARD_OUTPUT_STORE_FIELDS = (
    "schema",
    "decoder_hard_output_sha256",
    "payload",
)


def _canonical_json_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise SchemaError("value is not canonical-JSON encodable") from exc


def _decoder_hard_output_payload(encoded: str) -> dict[str, Any]:
    return {
        "schema": _DECODER_HARD_OUTPUT_SCHEMA,
        "cw_count": 16,
        "information_bits_per_cw": 1024,
        "cw_order": "TRANSMITTED_CW_INDEX_0_THROUGH_15",
        "bit_packing": "CW_MAJOR_MSB_FIRST_RFC4648_BASE64",
        "decoded_information_bits_base64": encoded,
    }


def _decode_hard_output_payload(payload: Mapping[str, Any]) -> np.ndarray:
    if type(payload) not in (dict, MappingProxyType):
        raise SchemaError("decoder hard-output payload must be an exact mapping")
    if tuple(payload) != _DECODER_HARD_OUTPUT_FIELDS:
        raise SchemaError("decoder hard-output payload fields/order mismatch")
    encoded = payload.get("decoded_information_bits_base64")
    expected = _decoder_hard_output_payload(encoded) if type(encoded) is str else None
    if expected is None or any(payload[key] != value for key, value in expected.items()):
        raise SchemaError("decoder hard-output payload constants mismatch")
    if (
        len(encoded) != 2732
        or not encoded.endswith("=")
        or encoded.count("=") != 1
        or any(character.isspace() for character in encoded)
    ):
        raise SchemaError("decoder hard-output base64 framing mismatch")
    try:
        packed = base64.b64decode(encoded, validate=True)
    except (ValueError, TypeError) as exc:
        raise SchemaError("decoder hard-output base64 is invalid") from exc
    if len(packed) != 2048 or base64.b64encode(packed).decode("ascii") != encoded:
        raise SchemaError("decoder hard-output base64 round trip mismatch")
    return np.unpackbits(
        np.frombuffer(packed, dtype=np.uint8), bitorder="big"
    ).reshape(16, 1024).copy()


def _make_decoder_hard_output_ref_type():
    token = object()

    class _DecoderHardOutputRef:
        __slots__ = ("_payload_json", "_root", "__weakref__")

        def __new__(cls, *args, **kwargs):
            if len(args) != 1 or args[0] is not token or kwargs:
                raise TypeError("DecoderHardOutputRef is factory-only")
            return super().__new__(cls)

        def __setattr__(self, _name, _value):
            raise AttributeError("DecoderHardOutputRef is immutable")

        @property
        def decoder_hard_output_sha256(self) -> str:
            return self._root

        @property
        def payload(self) -> Mapping[str, Any]:
            raw = json.loads(self._payload_json)
            return MappingProxyType({key: raw[key] for key in _DECODER_HARD_OUTPUT_FIELDS})

        @property
        def store_record(self) -> Mapping[str, Any]:
            return MappingProxyType({
                "schema": _DECODER_HARD_OUTPUT_STORE_SCHEMA,
                "decoder_hard_output_sha256": self._root,
                "payload": self.payload,
            })

        @property
        def info_bits(self) -> np.ndarray:
            return _decode_hard_output_payload(self.payload)

    _DecoderHardOutputRef.__name__ = "DecoderHardOutputRef"
    _DecoderHardOutputRef.__qualname__ = "DecoderHardOutputRef"

    def construct(payload_json: str, root: str):
        value = _DecoderHardOutputRef(token)
        object.__setattr__(value, "_payload_json", payload_json)
        object.__setattr__(value, "_root", root)
        return value

    return _DecoderHardOutputRef, construct


DecoderHardOutputRef, _new_decoder_hard_output_ref = _make_decoder_hard_output_ref_type()
_ISSUED_DECODER_HARD_OUTPUT_REFS: weakref.WeakSet[Any] = weakref.WeakSet()


def build_decoder_hard_output_ref(bits: np.ndarray) -> DecoderHardOutputRef:
    """Canonicalize one exact D0 16-codeword hard output into an opaque ref."""
    value = np.asarray(bits)
    if value.shape != (16, 1024):
        raise ValueError("decoder hard output must have exact shape (16,1024)")
    dtype = value.dtype
    if (
        dtype.hasobject
        or dtype.fields is not None
        or not (
            np.issubdtype(dtype, np.bool_)
            or np.issubdtype(dtype, np.integer)
            or np.issubdtype(dtype, np.floating)
        )
    ):
        raise TypeError("decoder hard output must use a plain real numeric or bool dtype")
    if not np.all(np.isfinite(value)) or not np.all((value == 0) | (value == 1)):
        raise ValueError("decoder hard output must contain finite binary values")
    packed = np.packbits(
        value.astype(np.uint8, copy=False).reshape(-1), bitorder="big"
    ).tobytes()
    if len(packed) != 2048:
        raise AssertionError("decoder hard-output packed length invariant")
    encoded = base64.b64encode(packed).decode("ascii")
    payload = _decoder_hard_output_payload(encoded)
    payload_json = _canonical_json_bytes(payload).decode("utf-8")
    root = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()
    ref = _new_decoder_hard_output_ref(payload_json, root)
    _ISSUED_DECODER_HARD_OUTPUT_REFS.add(ref)
    return ref


def assert_decoder_hard_output_ref(value: DecoderHardOutputRef) -> None:
    """Fail closed unless *value* is an issued, internally canonical authority."""
    if type(value) is not DecoderHardOutputRef or value not in _ISSUED_DECODER_HARD_OUTPUT_REFS:
        raise TypeError("issued DecoderHardOutputRef required")
    if type(value._payload_json) is not str or type(value._root) is not str:
        raise SchemaError("decoder hard-output ref fields are not canonical")
    payload = value.payload
    bits = _decode_hard_output_payload(payload)
    canonical = _canonical_json_bytes(dict(payload))
    root = hashlib.sha256(canonical).hexdigest()
    if canonical.decode("utf-8") != value._payload_json or root != value._root:
        raise SchemaError("decoder hard-output ref root/payload mismatch")
    if not np.array_equal(bits, value.info_bits):
        raise SchemaError("decoder hard-output ref materialization mismatch")


def validate_decoder_hard_output_store(
    records: Any,
    *,
    referenced_roots: frozenset[str],
) -> None:
    """Validate root uniqueness plus exact forward/reverse reference coverage."""
    if type(referenced_roots) is not frozenset or any(
        type(root) is not str or re.fullmatch(r"[0-9a-f]{64}", root) is None
        for root in referenced_roots
    ):
        raise TypeError("referenced_roots must be a frozenset of lowercase SHA256")
    if type(records) not in (tuple, list):
        raise TypeError("hard-output store records must be an ordered tuple/list")
    found: list[str] = []
    for record in records:
        if type(record) not in (dict, MappingProxyType):
            raise TypeError("hard-output store record must be an exact mapping")
        if tuple(record) != _DECODER_HARD_OUTPUT_STORE_FIELDS:
            raise SchemaError("hard-output store record fields/order mismatch")
        if record["schema"] != _DECODER_HARD_OUTPUT_STORE_SCHEMA:
            raise SchemaError("hard-output store record schema mismatch")
        root = record["decoder_hard_output_sha256"]
        if type(root) is not str or re.fullmatch(r"[0-9a-f]{64}", root) is None:
            raise SchemaError("hard-output store root is not lowercase SHA256")
        payload = record["payload"]
        _decode_hard_output_payload(payload)
        if hashlib.sha256(_canonical_json_bytes(dict(payload))).hexdigest() != root:
            raise SchemaError("hard-output store root/payload mismatch")
        found.append(root)
    if len(found) != len(set(found)):
        raise SchemaError("hard-output store roots must be unique")
    if frozenset(found) != referenced_roots:
        raise SchemaError("hard-output store forward/reverse reference mismatch")


@dataclass(frozen=True, slots=True)
class _Field:
    kind: str
    const: Any = None
    enum: tuple[Any, ...] | None = None
    minimum: int | float | None = None
    maximum: int | float | None = None


def F(kind: str, *, const: Any = None, enum=(), minimum=None, maximum=None) -> _Field:
    return _Field(kind, const, tuple(enum) or None, minimum, maximum)


POL = ("X", "Y")
FIXTURES = (
    "B04_K1", "B04_K2", "B04_K3", "B08_K1", "B08_K2", "B08_K3",
    "B12_K1", "B12_K2", "B12_K3",
)
CANDIDATES = ("NOOP",) + FIXTURES
S2_METHODS = (
    "GLOBAL_FOUR_ROTATION_DECODER_SELECTION",
    "OFC17_16QAM_EXTFRAME_V1",
    "TRUTH_BOUNDARY_ROTATION_CORRECTION",
)
TUPLES = ("M2_N100", "M3_N10", "M3_N20", "M3_N100", "M3_N200")
N_OVERHEAD_IDENTITIES = MappingProxyType({
    10: (684, 6860),
    20: (325, 6501),
    100: (64, 6240),
    200: (32, 6208),
})
S4_CHECK_IDS = (
    "no_slip_noiseless_B0_B1_O1_identity",
    "all_rotation_boundary_noiseless_O1_zero_error",
    "mapping_rotation_truth_metamorphic_pass",
    "candidate_isolation_and_empty_decoder_state_pass",
    "all_scores_finite_and_deterministic",
    "no_truth_field_reaches_receiver_view",
    "diagnostic_cost_ledger_complete",
)


_SPECS: dict[str, dict[str, _Field]] = {
    "s1_trajectory": {
        "record_type": F("str", const="S1_TRAJECTORY"),
        "seed": F("int", minimum=0), "cell_id": F("str"),
        "target_polarization": F("str", enum=POL),
        "persistent_transition_count": F("int", minimum=0),
        "persistent_transition_after_symbol": F("int_list", minimum=0),
        "event_present": F("bool"), "trajectory_receipt_sha256": F("sha"),
    },
    "s2_method": {
        "record_type": F("str", const="S2_METHOD"), "seed": F("int", minimum=0),
        "cell_id": F("str"), "target_polarization": F("str", enum=POL),
        "fixture_id": F("str", enum=FIXTURES),
        "boundary_after_cw": F("int", enum=(4, 8, 12)),
        "rotation_k": F("int", enum=(1, 2, 3)), "jump_present": F("bool"),
        "projection_role": F("str", enum=("DIRECT_ON", "CACHED_OFF_PROJECTION")),
        "physical_case_id": F("str"), "computation_id": F("str"),
        "method_id": F("str", enum=S2_METHODS),
        "affected_cw_errors": F("int", minimum=0),
        "affected_cw_total": F("int", enum=(4, 8, 12)),
        "information_bit_errors": F("int", minimum=0),
        "information_bit_total": F("int", const=16384),
        "total_transmitted_symbols_per_polarization": F("int", minimum=6208),
        "result_receipt_sha256": F("sha"),
    },
    "s3_candidate": {
        "record_type": F("str", enum=("S3_CANDIDATE_DEV", "S3_CANDIDATE_TEST")),
        "seed": F("int", minimum=0), "cell_id": F("str"),
        "target_polarization": F("str", enum=POL),
        "fixture_id": F("str", enum=FIXTURES),
        "truth_candidate_id": F("str", enum=FIXTURES),
        "candidate_id": F("str", enum=CANDIDATES),
        "pilot_score": F("float"), "decoder_score": F("float"),
        "computation_id": F("str"),
        "changed_cw_decodes": F("int", enum=(4, 8, 12, 16)),
        "cached_unchanged_cw_nll_reads": F("int", enum=(0, 4, 8, 12)),
        "result_receipt_sha256": F("sha"),
    },
    "s3_lambda_freeze": {
        "record_type": F("str", const="S3_LAMBDA_FREEZE"),
        "lambda_frozen": F("float", enum=(0.25, 0.5, 1.0, 2.0, 4.0)),
        "dev_rows_sha256": F("sha"),
        "objective": F("str", const="macro_MRR_then_macro_top1_then_smaller_lambda"),
        "test_rows_read_during_selection": F("bool", const=False),
        "freeze_receipt_sha256": F("sha"),
    },
    "s4_check": {
        "record_type": F("str", const="S4_CHECK"),
        "check_id": F("str", enum=S4_CHECK_IDS),
        "tested_instances": F("int", minimum=1),
        "failed_instances": F("int", minimum=0), "passed": F("bool"),
        "evidence_sha256": F("sha"),
    },
    "computation_ledger": {
        "record_type": F("str", const="COMPUTATION"), "computation_id": F("str"),
        "phase": F("str", enum=("BPS_DEV", "B2_DEV", "S2", "S3_DEV", "S3_TEST", "S4")),
        "operation": F("str", enum=("B1_DECODE", "B2_DECODE", "O1_DECODE",
                                     "CANDIDATE_DECODE", "HMM_GRID_SCORE", "OTHER_S4_CHECK")),
        "physical_case_id": F("str"),
        "cost_scope": F("str", enum=("DUAL_POL_METHOD_FRAME", "TARGET_POL_INCREMENTAL", "NON_DECODER")),
        "cache_status": F("str", enum=("EXECUTED", "CACHE_READ")),
        "source_computation_id": F("optional_str"), "content_sha256": F("sha"),
        "logical_decoder_batches": F("int", minimum=0),
        "logical_cw_decodes": F("int", minimum=0),
        "logical_bp_iterations": F("int", minimum=0),
        "materialized_decoder_batches": F("int", minimum=0),
        "materialized_cw_decodes": F("int", minimum=0),
        "materialized_bp_iterations": F("int", minimum=0),
        "physical_api_invocations": F("int", minimum=0),
        "api_batch_cw_count": F("int", minimum=0),
        "hmm_dual_pol_frame_parameter_pair_scores": F("int", minimum=0),
        "hmm_primitive_pol_trajectory_parameter_pair_scores": F("int", minimum=0),
        "selected_pair_symbol_state_evaluations": F("int", minimum=0),
        "wall_latency_ms": F("float", minimum=0.0),
    },
    "bps_dev_score": {
        "record_type": F("str", const="BPS_DEV_SCORE"),
        "tuple_id": F("str", enum=TUPLES), "M": F("int", enum=(2, 3)),
        "N": F("int", enum=(10, 20, 100, 200)), "B": F("int", enum=(32, 64)),
        "Nw": F("int", enum=(31, 61, 127)), "seed": F("int", minimum=0),
        "cell_id": F("str"), "polarization": F("str", enum=POL),
        "method_id": F("str", const="GLOBAL_FOUR_ROTATION_DECODER_SELECTION"),
        "selected_global_rotation_k": F("int", enum=(0, 1, 2, 3)),
        "selected_normalized_reencode_nll": F("float"),
        "successful_cw_count": F("int", minimum=0, maximum=16),
        "delivered_information_bits": F("int", minimum=0, maximum=16384),
        "full_frame_cw_errors": F("int", minimum=0, maximum=16),
        "full_frame_cw_total": F("int", const=16),
        "information_bit_errors": F("int", minimum=0, maximum=16384),
        "information_bit_total": F("int", const=16384),
        "total_transmitted_symbols_per_polarization": F("int", enum=(6208, 6240, 6501, 6860)),
        "computation_id": F("str"), "cache_status": F("str", enum=("EXECUTED", "CACHE_READ")),
        "source_computation_id": F("optional_str"), "result_receipt_sha256": F("sha"),
    },
    "b2_hmm_grid_chunk": {
        "record_type": F("str", const="B2_HMM_GRID_CHUNK"),
        "tuple_id": F("str", enum=TUPLES), "M": F("int", enum=(2, 3)),
        "N": F("int", enum=(10, 20, 100, 200)),
        "p_s_index": F("int", minimum=0, maximum=121), "p_s_float64_hex": F("float_hex"),
        "sigma_e2_index": F("int", minimum=0, maximum=5),
        "sigma_e2_float64_hex": F("float_hex"),
        "stratum_role": F("str", enum=("CLEAN_INCLUDED", "CONTROLLED_TARGET_INCLUDED",
                                        "CONTROLLED_SENTINEL_EXCLUDED")),
        "cell_id": F("str"), "polarization": F("str", enum=POL), "chunk_id": F("str"),
        "pilot_count": F("int", enum=(32, 64, 325, 684)),
        "member_count": F("int", minimum=1), "member_key_manifest_sha256": F("sha"),
        "normalized_nll_exact_sum_numerator_decimal": F("decimal_int"),
        "normalized_nll_exact_sum_denominator_power2": F("int", minimum=0),
        "objective_included": F("bool"), "computation_ids_manifest_sha256": F("sha"),
        "content_sha256": F("sha"),
    },
    "b2_tuple_clean_dev": {
        "record_type": F("str", const="B2_TUPLE_CLEAN_DEV"),
        "tuple_id": F("str", enum=TUPLES), "seed": F("int", minimum=0),
        "cell_id": F("str"), "polarization": F("str", enum=POL),
        "bps_freeze_ref": F("str"), "statistic_freeze_ref": F("str"),
        "successful_cw_count": F("int", minimum=0, maximum=16),
        "delivered_information_bits": F("int", minimum=0, maximum=16384),
        "full_frame_cw_errors": F("int", minimum=0, maximum=16),
        "information_bit_errors": F("int", minimum=0, maximum=16384),
        "total_transmitted_symbols_per_polarization": F("int", enum=(6208, 6240, 6501, 6860)),
        "computation_id": F("str"), "result_receipt_sha256": F("sha"),
    },
    "b2_tuple_controlled_dev": {
        "record_type": F("str", const="B2_TUPLE_CONTROLLED_DEV"),
        "tuple_id": F("str", enum=TUPLES), "seed": F("int", minimum=0),
        "cell_id": F("str"), "target_polarization": F("str", enum=POL),
        "row_polarization": F("str", enum=POL),
        "row_role": F("str", enum=("TARGET_INCLUDED", "SENTINEL_EXCLUDED")),
        "fixture_id": F("str", enum=FIXTURES),
        "boundary_after_cw": F("int", enum=(4, 8, 12)),
        "rotation_k": F("int", enum=(1, 2, 3)),
        "bps_freeze_ref": F("str"), "statistic_freeze_ref": F("str"),
        "successful_cw_count": F("int", minimum=0, maximum=16),
        "delivered_information_bits": F("int", minimum=0, maximum=16384),
        "full_frame_cw_errors": F("int", minimum=0, maximum=16),
        "affected_cw_errors": F("int", minimum=0, maximum=12),
        "affected_cw_total": F("int", enum=(4, 8, 12)),
        "total_transmitted_symbols_per_polarization": F("int", enum=(6208, 6240, 6501, 6860)),
        "computation_id": F("str"), "cache_status": F("str", enum=("EXECUTED", "CACHE_READ")),
        "source_computation_id": F("optional_str"), "result_receipt_sha256": F("sha"),
    },
}


_TYPES = {
    "str": str, "int": int, "float": float, "bool": bool, "sha": str,
    "optional_str": str | None, "int_list": tuple[int, ...],
    "decimal_int": str, "float_hex": str,
}
_CLASS_NAMES = {
    "s1_trajectory": "S1TrajectoryRow", "s2_method": "S2MethodRow",
    "s3_candidate": "S3CandidateRow", "s3_lambda_freeze": "S3LambdaFreezeRow",
    "s4_check": "S4CheckRow", "computation_ledger": "ComputationLedgerRow",
    "bps_dev_score": "BpsDevScoreRow", "b2_hmm_grid_chunk": "B2HmmGridChunkRow",
    "b2_tuple_clean_dev": "B2TupleCleanDevRow",
    "b2_tuple_controlled_dev": "B2TupleControlledDevRow",
}
TABLE_FIELDS = {name: tuple(spec) for name, spec in _SPECS.items()}
TABLE_MODELS = {
    name: make_dataclass(
        _CLASS_NAMES[name],
        [(field, _TYPES[rule.kind]) for field, rule in spec.items()],
        frozen=True, slots=True,
    )
    for name, spec in _SPECS.items()
}
for _model in TABLE_MODELS.values():
    _model.__module__ = __name__
globals().update({model.__name__: model for model in TABLE_MODELS.values()})


def _fail(scope: str, message: str) -> None:
    raise SchemaError(f"{scope}: {message}")


def _validate_value(scope: str, value: Any, rule: _Field) -> Any:
    kind = rule.kind
    if kind == "int":
        if type(value) is not int:
            _fail(scope, "must be an exact int (bool/coercion forbidden)")
    elif kind == "float":
        if type(value) is not float or not math.isfinite(value):
            _fail(scope, "must be a finite exact float")
    elif kind == "bool":
        if type(value) is not bool:
            _fail(scope, "must be an exact bool")
    elif kind in {"str", "sha", "decimal_int", "float_hex"}:
        if type(value) is not str or not value:
            _fail(scope, "must be a non-empty exact string")
        if kind == "sha" and re.fullmatch(r"[0-9a-f]{64}", value) is None:
            _fail(scope, "must be lowercase SHA256")
        if kind == "decimal_int" and re.fullmatch(r"-?(0|[1-9][0-9]*)", value) is None:
            _fail(scope, "must be a canonical decimal integer")
        if kind == "float_hex":
            try:
                parsed = float.fromhex(value)
            except ValueError:
                _fail(scope, "must be float64 hex")
            if not math.isfinite(parsed):
                _fail(scope, "float64 hex must be finite")
    elif kind == "optional_str":
        if value is not None and (type(value) is not str or not value):
            _fail(scope, "must be None or a non-empty exact string")
    elif kind == "int_list":
        if type(value) is not list or any(type(item) is not int for item in value):
            _fail(scope, "must be a list of exact ints")
        if rule.minimum is not None and any(item < rule.minimum for item in value):
            _fail(scope, "list item below minimum")
        value = tuple(value)
    else:
        _fail(scope, f"unknown schema kind {kind}")
    if rule.const is not None and value != rule.const:
        _fail(scope, f"must equal {rule.const!r}")
    if rule.enum is not None and value not in rule.enum:
        _fail(scope, f"not in frozen enum {rule.enum!r}")
    if kind in {"int", "float"}:
        if rule.minimum is not None and value < rule.minimum:
            _fail(scope, "below minimum")
        if rule.maximum is not None and value > rule.maximum:
            _fail(scope, "above maximum")
    return value


def _tuple_identity(tuple_id: str) -> tuple[int, int]:
    return {
        "M2_N100": (2, 100), "M3_N10": (3, 10), "M3_N20": (3, 20),
        "M3_N100": (3, 100), "M3_N200": (3, 200),
    }[tuple_id]


def _fixture_identity(fixture: str) -> tuple[int, int]:
    return int(fixture[1:3]), int(fixture[-1])


def _local_invariants(table: str, row: Any) -> None:
    if table == "s1_trajectory":
        if row.event_present != (row.persistent_transition_count > 0):
            _fail(table, "event/count mismatch")
        if len(row.persistent_transition_after_symbol) != row.persistent_transition_count:
            _fail(table, "transition array length mismatch")
    elif table == "s2_method":
        if row.affected_cw_errors > row.affected_cw_total or row.information_bit_errors > row.information_bit_total:
            _fail(table, "errors exceed totals")
        if row.affected_cw_total != 16 - row.boundary_after_cw:
            _fail(table, "affected total/boundary mismatch")
        if _fixture_identity(row.fixture_id) != (row.boundary_after_cw, row.rotation_k):
            _fail(table, "fixture bijection mismatch")
        if row.jump_present != (row.projection_role == "DIRECT_ON"):
            _fail(table, "projection/jump mismatch")
        allowed = S2_METHODS if row.jump_present else (S2_METHODS[0],)
        if row.method_id not in allowed:
            _fail(table, "method invalid for projection role")
    elif table == "s3_candidate":
        if row.truth_candidate_id != row.fixture_id:
            _fail(table, "truth candidate must equal fixture")
        boundary = 0 if row.candidate_id == "NOOP" else int(row.candidate_id[1:3])
        if row.changed_cw_decodes != 16 - boundary or row.cached_unchanged_cw_nll_reads != boundary:
            _fail(table, "candidate cost identity mismatch")
    elif table == "s4_check":
        if row.failed_instances > row.tested_instances or row.passed != (row.failed_instances == 0):
            _fail(table, "S4 count/pass mismatch")
    elif table == "computation_ledger":
        if row.logical_bp_iterations != 20 * row.logical_cw_decodes:
            _fail(table, "logical BP identity mismatch")
        if row.materialized_bp_iterations != 20 * row.materialized_cw_decodes:
            _fail(table, "materialized BP identity mismatch")
        if row.cache_status == "EXECUTED" and row.source_computation_id is not None:
            _fail(table, "executed row cannot have source")
        if row.cache_status == "CACHE_READ":
            if row.source_computation_id is None:
                _fail(table, "cache row requires source")
            materialized = (
                row.materialized_decoder_batches, row.materialized_cw_decodes,
                row.materialized_bp_iterations, row.physical_api_invocations,
                row.selected_pair_symbol_state_evaluations,
            )
            if any(materialized):
                _fail(table, "cache row must have zero materialized costs")
    elif table in {"bps_dev_score", "b2_hmm_grid_chunk"}:
        if _tuple_identity(row.tuple_id) != (row.M, row.N):
            _fail(table, "tuple M/N mismatch")
        expected_pilot, expected_total = N_OVERHEAD_IDENTITIES[row.N]
        if table == "bps_dev_score":
            if row.total_transmitted_symbols_per_polarization != expected_total:
                _fail(table, "N/transmitted-symbol overhead mismatch")
            if row.delivered_information_bits != 1024 * row.successful_cw_count:
                _fail(table, "delivered bits mismatch")
            if row.full_frame_cw_errors != 16 - row.successful_cw_count:
                _fail(table, "frame error mismatch")
        else:
            if row.pilot_count != expected_pilot:
                _fail(table, "N/pilot-count overhead mismatch")
            expected = row.stratum_role != "CONTROLLED_SENTINEL_EXCLUDED"
            if row.objective_included != expected:
                _fail(table, "stratum/objective mismatch")
    elif table in {"b2_tuple_clean_dev", "b2_tuple_controlled_dev"}:
        _, n_value = _tuple_identity(row.tuple_id)
        _, expected_total = N_OVERHEAD_IDENTITIES[n_value]
        if row.total_transmitted_symbols_per_polarization != expected_total:
            _fail(table, "tuple/transmitted-symbol overhead mismatch")
        if row.delivered_information_bits != 1024 * row.successful_cw_count:
            _fail(table, "delivered bits mismatch")
        if row.full_frame_cw_errors != 16 - row.successful_cw_count:
            _fail(table, "frame error mismatch")
        if table == "b2_tuple_controlled_dev":
            if _fixture_identity(row.fixture_id) != (row.boundary_after_cw, row.rotation_k):
                _fail(table, "fixture bijection mismatch")
            if row.affected_cw_total != 16 - row.boundary_after_cw:
                _fail(table, "affected total mismatch")
            if row.affected_cw_errors > row.affected_cw_total:
                _fail(table, "affected errors exceed total")
            expected_role = "TARGET_INCLUDED" if row.row_polarization == row.target_polarization else "SENTINEL_EXCLUDED"
            if row.row_role != expected_role:
                _fail(table, "row polarization/role mismatch")


def row_from_mapping(table: str, mapping: Mapping[str, Any]) -> Any:
    if table not in _SPECS:
        _fail("table", f"unknown table {table!r}")
    if type(mapping) is not dict:
        _fail(table, "row must be an exact dict")
    expected = TABLE_FIELDS[table]
    if tuple(mapping) != expected or set(mapping) != set(expected):
        missing = set(expected) - set(mapping)
        extra = set(mapping) - set(expected)
        _fail(table, f"exact fields/order required; missing={sorted(missing)} extra={sorted(extra)}")
    values = {
        name: _validate_value(f"{table}.{name}", mapping[name], rule)
        for name, rule in _SPECS[table].items()
    }
    row = TABLE_MODELS[table](**values)
    _local_invariants(table, row)
    return row


def row_to_mapping(row: Any) -> dict[str, Any]:
    if not is_dataclass(row):
        _fail("row", "must be a typed dataclass")
    table = next((name for name, model in TABLE_MODELS.items() if type(row) is model), None)
    if table is None:
        _fail("row", "unknown row model")
    result = {field.name: getattr(row, field.name) for field in fields(row)}
    for name, rule in _SPECS[table].items():
        if rule.kind == "int_list":
            result[name] = list(result[name])
    return result


EXPLICIT_PARTIAL = "EXPLICIT_PARTIAL"
FULL_D0_ARTIFACT = "FULL_D0_ARTIFACT"


@dataclass(frozen=True, slots=True)
class CellDomain:
    name: str
    exact_values: tuple[str, ...]

    def __post_init__(self) -> None:
        if type(self.name) is not str or not self.name:
            _fail("CellDomain", "non-empty name required")
        if (type(self.exact_values) is not tuple or not self.exact_values
                or any(type(value) is not str or not value for value in self.exact_values)
                or len(set(self.exact_values)) != len(self.exact_values)):
            _fail("CellDomain", "non-empty unique exact string values required")


@dataclass(frozen=True, slots=True)
class SeedSet:
    record_type: str
    exact_values: tuple[int, ...]

    def __post_init__(self) -> None:
        if type(self.record_type) is not str or not self.record_type:
            _fail("SeedSet", "non-empty record type required")
        if (type(self.exact_values) is not tuple or not self.exact_values
                or any(type(value) is not int or value < 0 for value in self.exact_values)
                or len(set(self.exact_values)) != len(self.exact_values)):
            _fail("SeedSet", "non-empty unique exact integer seeds required")


@dataclass(frozen=True, slots=True)
class IdentityProjection:
    fields: tuple[str, ...]
    expected_key_count: int
    expected_keys_sha256: str
    multiplicity_by_key_sha256: str

    def __post_init__(self) -> None:
        if (type(self.fields) is not tuple or not self.fields
                or any(type(field) is not str or not field for field in self.fields)
                or len(set(self.fields)) != len(self.fields)):
            _fail("IdentityProjection", "non-empty unique fields required")
        if type(self.expected_key_count) is not int or self.expected_key_count < 1:
            _fail("IdentityProjection", "positive exact key count required")
        _validate_value("expected_keys_sha256", self.expected_keys_sha256, F("sha"))
        _validate_value("multiplicity_by_key_sha256", self.multiplicity_by_key_sha256, F("sha"))


@dataclass(frozen=True, slots=True)
class TableExpectation:
    table: str
    projections: tuple[IdentityProjection, ...]

    def __post_init__(self) -> None:
        if type(self.table) is not str or self.table not in TABLE_MODELS:
            _fail("TableExpectation", "known table required")
        if (type(self.projections) is not tuple or not self.projections
                or any(type(item) is not IdentityProjection for item in self.projections)):
            _fail("TableExpectation", "non-empty typed projections required")
        seen = set()
        allowed = set(TABLE_FIELDS[self.table])
        for projection in self.projections:
            if not set(projection.fields) <= allowed:
                _fail("TableExpectation", "projection field is not in table")
            if projection.fields in seen:
                _fail("TableExpectation", "duplicate projection")
            seen.add(projection.fields)


@dataclass(frozen=True, slots=True)
class RelationalManifest:
    scope: str
    cell_domains: tuple[CellDomain, ...]
    seed_sets: tuple[SeedSet, ...]
    tables: tuple[TableExpectation, ...]
    coverage_sha256: str

    def __post_init__(self) -> None:
        if type(self.scope) is not str or self.scope != EXPLICIT_PARTIAL:
            _fail("manifest", "RelationalManifest is EXPLICIT_PARTIAL only")
        if (type(self.cell_domains) is not tuple or not self.cell_domains
                or any(type(item) is not CellDomain for item in self.cell_domains)
                or len({item.name for item in self.cell_domains}) != len(self.cell_domains)):
            _fail("manifest", "non-empty unique cell domains required")
        if (type(self.seed_sets) is not tuple or not self.seed_sets
                or any(type(item) is not SeedSet for item in self.seed_sets)
                or len({item.record_type for item in self.seed_sets}) != len(self.seed_sets)):
            _fail("manifest", "non-empty unique seed sets required")
        if (type(self.tables) is not tuple or not self.tables
                or any(type(item) is not TableExpectation for item in self.tables)
                or len({item.table for item in self.tables}) != len(self.tables)):
            _fail("manifest", "non-empty unique table expectations required")
        _validate_value("coverage_sha256", self.coverage_sha256, F("sha"))


@dataclass(frozen=True, slots=True)
class HmmPreexecutionPlan:
    tuple_ids: tuple[str, ...]
    p_s_indices: tuple[int, ...]
    sigma_e2_indices: tuple[int, ...]
    roles: tuple[str, ...]
    cell_ids: tuple[str, ...]
    polarizations: tuple[str, ...]
    member_counts: tuple[tuple[str, int], ...]
    binding_scheme: str
    member_namespace_sha256: str
    computation_namespace_sha256: str

    def __post_init__(self) -> None:
        axes = (self.tuple_ids, self.p_s_indices, self.sigma_e2_indices,
                self.roles, self.cell_ids, self.polarizations)
        if any(type(axis) is not tuple or not axis or len(set(axis)) != len(axis) for axis in axes):
            _fail("HmmPreexecutionPlan", "non-empty unique axes required")
        if (any(type(value) is not str or not value for value in self.tuple_ids + self.roles
                + self.cell_ids + self.polarizations)
                or any(type(value) is not int or value < 0
                       for value in self.p_s_indices + self.sigma_e2_indices)):
            _fail("HmmPreexecutionPlan", "invalid axis value")
        if (type(self.member_counts) is not tuple or not self.member_counts
                or any(type(item) is not tuple or len(item) != 2
                       or type(item[0]) is not str or type(item[1]) is not int or item[1] < 1
                       for item in self.member_counts)
                or len({item[0] for item in self.member_counts}) != len(self.member_counts)):
            _fail("HmmPreexecutionPlan", "exact positive role member counts required")
        if self.binding_scheme != "D0_HMM_GROUP_SHA256_V1":
            _fail("HmmPreexecutionPlan", "unknown binding scheme")
        _validate_value("member_namespace_sha256", self.member_namespace_sha256, F("sha"))
        _validate_value("computation_namespace_sha256", self.computation_namespace_sha256, F("sha"))


@dataclass(frozen=True, slots=True)
class ComputationPlanEntry:
    computation_id: str
    phase: str
    operation: str
    cache_status: str
    source_computation_id: str | None

    def __post_init__(self) -> None:
        if type(self.computation_id) is not str or not self.computation_id:
            _fail("ComputationPlanEntry", "non-empty computation id required")
        if type(self.phase) is not str or type(self.operation) is not str:
            _fail("ComputationPlanEntry", "phase/operation strings required")
        if self.cache_status not in {"EXECUTED", "CACHE_READ"}:
            _fail("ComputationPlanEntry", "invalid cache status")
        if self.source_computation_id is not None and (
                type(self.source_computation_id) is not str or not self.source_computation_id):
            _fail("ComputationPlanEntry", "invalid source computation id")
        if self.cache_status == "EXECUTED" and self.source_computation_id is not None:
            _fail("ComputationPlanEntry", "executed plan entry cannot have source")
        if self.cache_status == "CACHE_READ" and self.source_computation_id is None:
            _fail("ComputationPlanEntry", "cache plan entry requires source")


@dataclass(frozen=True, slots=True)
class ComputationPreexecutionPlan:
    entries: tuple[ComputationPlanEntry, ...]

    def __post_init__(self) -> None:
        if (type(self.entries) is not tuple or not self.entries
                or any(type(item) is not ComputationPlanEntry for item in self.entries)):
            _fail("ComputationPreexecutionPlan", "non-empty typed entries required")
        identities = {item.computation_id for item in self.entries}
        if len(identities) != len(self.entries):
            _fail("ComputationPreexecutionPlan", "duplicate computation id")
        if any(item.source_computation_id is not None
               and item.source_computation_id not in identities for item in self.entries):
            _fail("ComputationPreexecutionPlan", "orphan cache source")


FULL_MANIFEST_SCHEMA_VERSION = "coded_decoder_feedback.d0.full_manifest.v1"
FROZEN_D0_OWNER_SHA256 = "c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d"


@dataclass(frozen=True, slots=True)
class FullManifestSpec:
    manifest_schema_version: str
    owner_contract: D0Contract
    owner_sha256: str
    s1_extent: str
    hmm_preexecution_plan: HmmPreexecutionPlan
    computation_preexecution_plan: ComputationPreexecutionPlan

    def __post_init__(self) -> None:
        _validate_full_manifest_spec(self)


@dataclass(frozen=True, slots=True, init=False)
class FullRelationalManifest:
    spec: FullManifestSpec
    scope: str
    cell_domains: tuple[CellDomain, ...]
    seed_sets: tuple[SeedSet, ...]
    tables: tuple[TableExpectation, ...]
    coverage_sha256: str
    authority_sha256: str

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        _fail("FULL manifest", "direct construction forbidden; use factory")


def _canonical_atom(value: Any) -> list[Any]:
    if type(value) is str:
        return ["str", value]
    if type(value) is bool:
        return ["bool", value]
    if type(value) is int:
        return ["int", str(value)]
    if type(value) is float and math.isfinite(value):
        return ["float", value.hex()]
    if value is None:
        return ["none", None]
    _fail("coverage", f"unsupported key atom type {type(value).__name__}")


def _canonical_key(key: tuple[Any, ...]) -> str:
    if type(key) is not tuple:
        _fail("coverage", "expected keys must be explicit tuples, not rows")
    return json.dumps([_canonical_atom(value) for value in key], ensure_ascii=False,
                      separators=(",", ":"), sort_keys=True)


def _digest(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, separators=(",", ":"),
                         sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _validate_full_manifest_spec(spec: FullManifestSpec) -> None:
    if type(spec) is not FullManifestSpec:
        _fail("FULL spec", "exact FullManifestSpec required")
    if (type(spec.manifest_schema_version) is not str
            or spec.manifest_schema_version != FULL_MANIFEST_SCHEMA_VERSION):
        _fail("FULL spec", "manifest schema identity mismatch")
    if type(spec.owner_contract) is not D0Contract:
        _fail("FULL spec", "exact owner contract required")
    try:
        assert_frozen_d0_identity(spec.owner_contract)
    except ContractError as error:
        _fail("FULL spec", f"owner identity mismatch: {error}")
    if type(spec.owner_sha256) is not str or spec.owner_sha256 != FROZEN_D0_OWNER_SHA256:
        _fail("FULL spec", "owner SHA identity mismatch")
    if type(spec.s1_extent) is not str or spec.s1_extent not in {"FIRST_STAGE", "MAXIMUM"}:
        _fail("FULL spec", "S1 extent must be FIRST_STAGE or MAXIMUM")
    if type(spec.hmm_preexecution_plan) is not HmmPreexecutionPlan:
        _fail("FULL spec", "exact HMM preexecution plan required")
    if type(spec.computation_preexecution_plan) is not ComputationPreexecutionPlan:
        _fail("FULL spec", "exact computation preexecution plan required")
    spec.hmm_preexecution_plan.__post_init__()
    spec.computation_preexecution_plan.__post_init__()


def _projection_digests(keys: tuple[tuple[Any, ...], ...], field_count: int) -> tuple[int, str, str]:
    if type(keys) is not tuple or not keys:
        _fail("coverage", "non-empty caller-supplied expected keys required")
    encoded = []
    for key in keys:
        if type(key) is not tuple or len(key) != field_count:
            _fail("coverage", "expected key shape mismatch")
        encoded.append(_canonical_key(key))
    counts = Counter(encoded)
    ordered = sorted(counts)
    return len(counts), _digest(ordered), _digest([[key, counts[key]] for key in ordered])


def build_identity_projection(*, fields: tuple[str, ...],
                              expected_keys: tuple[tuple[Any, ...], ...]) -> IdentityProjection:
    if (type(fields) is not tuple or not fields
            or any(type(field) is not str or not field for field in fields)
            or len(set(fields)) != len(fields)):
        _fail("coverage", "non-empty unique explicit projection fields required")
    count, key_sha, multiplicity_sha = _projection_digests(expected_keys, len(fields))
    return IdentityProjection(fields, count, key_sha, multiplicity_sha)


def _coverage_sha256(scope: str, *, cell_domains: tuple[CellDomain, ...],
                     seed_sets: tuple[SeedSet, ...],
                     tables: tuple[TableExpectation, ...]) -> str:
    if (type(cell_domains) is not tuple or any(type(item) is not CellDomain for item in cell_domains)
            or type(seed_sets) is not tuple or any(type(item) is not SeedSet for item in seed_sets)
            or type(tables) is not tuple or any(type(item) is not TableExpectation for item in tables)):
        _fail("coverage", "typed tuples required")
    payload = {
        "scope": scope,
        "cell_domains": [[item.name, list(item.exact_values)] for item in cell_domains],
        "seed_sets": [[item.record_type, list(item.exact_values)] for item in seed_sets],
        "tables": [[item.table, [[list(projection.fields), projection.expected_key_count,
                                    projection.expected_keys_sha256,
                                    projection.multiplicity_by_key_sha256]
                                   for projection in item.projections]] for item in tables],
    }
    return _digest(payload)


def partial_coverage_sha256(*, cell_domains: tuple[CellDomain, ...],
                            seed_sets: tuple[SeedSet, ...],
                            tables: tuple[TableExpectation, ...]) -> str:
    return _coverage_sha256(EXPLICIT_PARTIAL, cell_domains=cell_domains,
                            seed_sets=seed_sets, tables=tables)


def full_coverage_sha256(*, cell_domains: tuple[CellDomain, ...],
                         seed_sets: tuple[SeedSet, ...],
                         tables: tuple[TableExpectation, ...]) -> str:
    return _coverage_sha256(FULL_D0_ARTIFACT, cell_domains=cell_domains,
                            seed_sets=seed_sets, tables=tables)


def build_partial_relational_manifest(*, cell_domains: tuple[CellDomain, ...],
                                      seed_sets: tuple[SeedSet, ...],
                                      tables: tuple[TableExpectation, ...],
                                      coverage_sha256: str) -> RelationalManifest:
    if type(tables) is not tuple or not tables:
        _fail("manifest", "partial manifest requires non-empty explicit tables")
    expected = partial_coverage_sha256(
        cell_domains=cell_domains, seed_sets=seed_sets, tables=tables,
    )
    _validate_value("coverage_sha256", coverage_sha256, F("sha"))
    if coverage_sha256 != expected:
        _fail("manifest", "coverage digest mismatch")
    return RelationalManifest(EXPLICIT_PARTIAL, cell_domains, seed_sets, tables, expected)


_PK = {
    "s1_trajectory": ("record_type", "seed", "cell_id", "target_polarization"),
    "s2_method": ("record_type", "seed", "cell_id", "target_polarization", "fixture_id", "jump_present", "method_id"),
    "s3_candidate": ("record_type", "seed", "cell_id", "target_polarization", "fixture_id", "candidate_id"),
    "s3_lambda_freeze": ("record_type",),
    "s4_check": ("record_type", "check_id"),
    "computation_ledger": ("computation_id",),
    "bps_dev_score": ("record_type", "tuple_id", "B", "Nw", "seed", "cell_id", "polarization"),
    "b2_hmm_grid_chunk": ("record_type", "tuple_id", "p_s_index", "sigma_e2_index", "stratum_role", "cell_id", "polarization", "chunk_id"),
    "b2_tuple_clean_dev": ("record_type", "tuple_id", "seed", "cell_id", "polarization"),
    "b2_tuple_controlled_dev": ("record_type", "tuple_id", "seed", "cell_id", "target_polarization", "fixture_id", "row_polarization"),
}

_CONSUMER_LEDGER_SIGNATURES = frozenset({
    ("S2", "B1_DECODE"), ("S2", "B2_DECODE"), ("S2", "O1_DECODE"),
    ("S3_DEV", "CANDIDATE_DECODE"), ("S3_TEST", "CANDIDATE_DECODE"),
    ("BPS_DEV", "B1_DECODE"), ("B2_DEV", "B2_DECODE"),
})
_STANDALONE_LEDGER_SIGNATURES = frozenset({
    ("B2_DEV", "HMM_GRID_SCORE"),
    ("S4", "OTHER_S4_CHECK"),
})


def _expectation(table: str, fields_: tuple[str, ...],
                 keys: tuple[tuple[Any, ...], ...]) -> TableExpectation:
    return TableExpectation(table, (build_identity_projection(fields=fields_, expected_keys=keys),))


def _hmm_expectation(plan: HmmPreexecutionPlan) -> TableExpectation:
    member_counts = dict(plan.member_counts)
    pk_keys = []
    binding_keys = []
    for tuple_id, p_index, sigma_index, role, cell_id, polarization in product(
            plan.tuple_ids, plan.p_s_indices, plan.sigma_e2_indices,
            plan.roles, plan.cell_ids, plan.polarizations):
        group = f"{tuple_id}|{p_index}|{sigma_index}|{role}|{cell_id}|{polarization}"
        chunk_id = f"hmm|{group}"
        count = member_counts[role]
        member_sha = hashlib.sha256(
            f"{plan.member_namespace_sha256}|{group}|{count}".encode("utf-8")
        ).hexdigest()
        computation_sha = hashlib.sha256(
            f"{plan.computation_namespace_sha256}|{group}|{count}".encode("utf-8")
        ).hexdigest()
        pk = ("B2_HMM_GRID_CHUNK", tuple_id, p_index, sigma_index, role,
              cell_id, polarization, chunk_id)
        pk_keys.append(pk)
        binding_keys.append(pk + (count, member_sha,
                                  role != "CONTROLLED_SENTINEL_EXCLUDED",
                                  computation_sha))
    pk_fields = _PK["b2_hmm_grid_chunk"]
    binding_fields = pk_fields + (
        "member_count", "member_key_manifest_sha256", "objective_included",
        "computation_ids_manifest_sha256",
    )
    return TableExpectation("b2_hmm_grid_chunk", (
        build_identity_projection(fields=pk_fields, expected_keys=tuple(pk_keys)),
        build_identity_projection(fields=binding_fields, expected_keys=tuple(binding_keys)),
    ))


@lru_cache(maxsize=4)
def _compile_full_relational_manifest_primitives(
    *, owner_contract: D0Contract, s1_extent: str,
    hmm_preexecution_plan: HmmPreexecutionPlan,
    computation_preexecution_plan: ComputationPreexecutionPlan,
) -> tuple[Any, ...]:
    spec = FullManifestSpec(
        manifest_schema_version=FULL_MANIFEST_SCHEMA_VERSION,
        owner_contract=deepcopy(owner_contract),
        owner_sha256=FROZEN_D0_OWNER_SHA256,
        s1_extent=s1_extent,
        hmm_preexecution_plan=deepcopy(hmm_preexecution_plan),
        computation_preexecution_plan=deepcopy(computation_preexecution_plan),
    )
    owner_contract = spec.owner_contract
    hmm_preexecution_plan = spec.hmm_preexecution_plan
    computation_preexecution_plan = spec.computation_preexecution_plan

    cells = tuple(cell.cell_id for cell in owner_contract.population_manifest)
    pols = owner_contract.population.polarizations
    aliases = ("hard", "mid", "clean")
    expected_roles = ("CLEAN_INCLUDED", "CONTROLLED_TARGET_INCLUDED",
                      "CONTROLLED_SENTINEL_EXCLUDED")
    if (hmm_preexecution_plan.tuple_ids != TUPLES
            or hmm_preexecution_plan.p_s_indices != tuple(range(122))
            or hmm_preexecution_plan.sigma_e2_indices != tuple(range(6))
            or hmm_preexecution_plan.roles != expected_roles
            or hmm_preexecution_plan.cell_ids != cells
            or hmm_preexecution_plan.polarizations != POL
            or hmm_preexecution_plan.member_counts != (
                (expected_roles[0], 10), (expected_roles[1], 90), (expected_roles[2], 90))):
        _fail("FULL manifest", "HMM preexecution axes/counts mismatch owner")
    allowed_signatures = _CONSUMER_LEDGER_SIGNATURES | _STANDALONE_LEDGER_SIGNATURES
    if any((entry.phase, entry.operation) not in allowed_signatures
           for entry in computation_preexecution_plan.entries):
        _fail("FULL manifest", "computation plan phase/operation mismatch")

    registry = owner_contract.seed_registry
    common_seeds = registry.range_for("common_cpr_and_b2_dev").values
    s2_seeds = registry.range_for("controlled_damage_recovery").values
    s3_dev_seeds = registry.range_for("observability_fusion_dev").values
    s3_test_seeds = registry.range_for("controlled_observability").values
    s1_seeds = (registry.first_stage_natural.values if s1_extent == "FIRST_STAGE"
                else registry.range_for("natural_occurrence").values)
    cell_domains = (CellDomain("population", cells), CellDomain("aliases", aliases))
    seed_sets = (
        SeedSet("S1_TRAJECTORY", s1_seeds), SeedSet("S2_METHOD", s2_seeds),
        SeedSet("S3_CANDIDATE_DEV", s3_dev_seeds),
        SeedSet("S3_CANDIDATE_TEST", s3_test_seeds),
        SeedSet("BPS_DEV_SCORE", common_seeds),
        SeedSet("B2_TUPLE_CLEAN_DEV", common_seeds),
        SeedSet("B2_TUPLE_CONTROLLED_DEV", common_seeds),
    )

    s2_keys = []
    for seed, alias, pol, fixture in product(s2_seeds, aliases, pols, FIXTURES):
        s2_keys.extend((
            ("S2_METHOD", seed, alias, pol, fixture, True, method)
            for method in S2_METHODS
        ))
        s2_keys.append(("S2_METHOD", seed, alias, pol, fixture, False, S2_METHODS[0]))
    s3_keys = tuple(
        (record_type, seed, alias, pol, fixture, candidate)
        for record_type, seeds_ in (("S3_CANDIDATE_DEV", s3_dev_seeds),
                                    ("S3_CANDIDATE_TEST", s3_test_seeds))
        for seed, alias, pol, fixture, candidate in product(
            seeds_, aliases, pols, FIXTURES, CANDIDATES)
    )
    ledger_keys = tuple(
        (entry.computation_id, entry.phase, entry.operation,
         entry.cache_status, entry.source_computation_id)
        for entry in computation_preexecution_plan.entries
    )
    tables = (
        _expectation("s1_trajectory", _PK["s1_trajectory"], tuple(
            ("S1_TRAJECTORY", seed, cell, pol)
            for seed, cell, pol in product(s1_seeds, cells, pols))),
        _expectation("s2_method", _PK["s2_method"], tuple(s2_keys)),
        _expectation("s3_candidate", _PK["s3_candidate"], s3_keys),
        _expectation("s3_lambda_freeze", _PK["s3_lambda_freeze"],
                     (("S3_LAMBDA_FREEZE",),)),
        _expectation("s4_check", _PK["s4_check"],
                     tuple(("S4_CHECK", check_id) for check_id in S4_CHECK_IDS)),
        _expectation("computation_ledger",
                     ("computation_id", "phase", "operation", "cache_status",
                      "source_computation_id"), ledger_keys),
        _expectation("bps_dev_score", _PK["bps_dev_score"], tuple(
            ("BPS_DEV_SCORE", tuple_id, b, nw, seed, cell, pol)
            for tuple_id, b, nw, seed, cell, pol in product(
                TUPLES, (32, 64), (31, 61, 127), common_seeds, cells, pols))),
        _hmm_expectation(hmm_preexecution_plan),
        _expectation("b2_tuple_clean_dev", _PK["b2_tuple_clean_dev"], tuple(
            ("B2_TUPLE_CLEAN_DEV", tuple_id, seed, cell, pol)
            for tuple_id, seed, cell, pol in product(TUPLES, common_seeds, cells, pols))),
        _expectation("b2_tuple_controlled_dev", _PK["b2_tuple_controlled_dev"], tuple(
            ("B2_TUPLE_CONTROLLED_DEV", tuple_id, seed, cell, target_pol,
             fixture, row_pol)
            for tuple_id, seed, cell, target_pol, fixture, row_pol in product(
                TUPLES, common_seeds, cells, pols, FIXTURES, pols))),
    )
    coverage_sha = full_coverage_sha256(
        cell_domains=cell_domains, seed_sets=seed_sets, tables=tables,
    )
    authority_sha = _full_authority_sha256(
        spec=spec, cell_domains=cell_domains, seed_sets=seed_sets,
        tables=tables, coverage_sha256=coverage_sha,
    )
    return _freeze_full_components(
        cell_domains=cell_domains, seed_sets=seed_sets, tables=tables,
        coverage_sha256=coverage_sha, authority_sha256=authority_sha,
    )


def _full_authority_sha256(*, spec: FullManifestSpec,
                           cell_domains: tuple[CellDomain, ...],
                           seed_sets: tuple[SeedSet, ...],
                           tables: tuple[TableExpectation, ...],
                           coverage_sha256: str) -> str:
    _validate_full_manifest_spec(spec)
    control = spec.owner_contract.control
    population = spec.owner_contract.population
    registry = spec.owner_contract.seed_registry
    payload = {
        "authority": "D0_FULL_RELATIONAL_AUTHORITY_V1",
        "manifest_schema_version": spec.manifest_schema_version,
        "owner_sha256": spec.owner_sha256,
        "owner_schema_version": spec.owner_contract.schema_version,
        "owner_control": [[item.name, getattr(control, item.name)] for item in fields(control)],
        "owner_population": {
            "modulation": population.modulation,
            "polarizations": population.polarizations,
            "code": [[item.name, getattr(population.code, item.name)]
                     for item in fields(population.code)],
            "symbol_rate_baud": population.symbol_rate_baud,
            "snr_db": population.snr_db,
            "linewidth_hz": population.linewidth_hz,
        },
        "owner_seed_registry": [
            [[label, seed_range.first, seed_range.last] for label, seed_range in registry.entries],
            [registry.first_stage_natural.first, registry.first_stage_natural.last],
        ],
        "s1_extent": spec.s1_extent,
        "hmm_plan": [[item.name, getattr(spec.hmm_preexecution_plan, item.name)]
                     for item in fields(spec.hmm_preexecution_plan)],
        "computation_plan": [
            [[item.name, getattr(entry, item.name)] for item in fields(entry)]
            for entry in spec.computation_preexecution_plan.entries
        ],
        "cell_domains": [[item.name, item.exact_values] for item in cell_domains],
        "seed_sets": [[item.record_type, item.exact_values] for item in seed_sets],
        "tables": [
            [table.table, [
                [projection.fields, projection.expected_key_count,
                 projection.expected_keys_sha256,
                 projection.multiplicity_by_key_sha256]
                for projection in table.projections
            ]]
            for table in tables
        ],
        "coverage_sha256": coverage_sha256,
    }
    return _digest(payload)


def _freeze_full_components(*, cell_domains: tuple[CellDomain, ...],
                            seed_sets: tuple[SeedSet, ...],
                            tables: tuple[TableExpectation, ...],
                            coverage_sha256: str,
                            authority_sha256: str) -> tuple[Any, ...]:
    """Return only recursively immutable primitives suitable for memoization."""

    return (
        tuple((item.name, tuple(item.exact_values)) for item in cell_domains),
        tuple((item.record_type, tuple(item.exact_values)) for item in seed_sets),
        tuple(
            (table.table, tuple(
                (tuple(projection.fields), projection.expected_key_count,
                 projection.expected_keys_sha256,
                 projection.multiplicity_by_key_sha256)
                for projection in table.projections
            ))
            for table in tables
        ),
        coverage_sha256,
        authority_sha256,
    )


def _materialize_full_components(*, spec: FullManifestSpec,
                                 primitives: tuple[Any, ...]) -> FullRelationalManifest:
    cell_data, seed_data, table_data, coverage_sha256, authority_sha256 = primitives
    cell_domains = tuple(CellDomain(name, tuple(values)) for name, values in cell_data)
    seed_sets = tuple(SeedSet(record_type, tuple(values))
                      for record_type, values in seed_data)
    tables = tuple(
        TableExpectation(table, tuple(
            IdentityProjection(tuple(fields_), count, key_sha, multiplicity_sha)
            for fields_, count, key_sha, multiplicity_sha in projection_data
        ))
        for table, projection_data in table_data
    )
    return _new_full_relational_manifest(
        spec=spec, cell_domains=cell_domains, seed_sets=seed_sets, tables=tables,
        coverage_sha256=coverage_sha256, authority_sha256=authority_sha256,
    )


def _new_full_relational_manifest(*, spec: FullManifestSpec,
                                  cell_domains: tuple[CellDomain, ...],
                                  seed_sets: tuple[SeedSet, ...],
                                  tables: tuple[TableExpectation, ...],
                                  coverage_sha256: str,
                                  authority_sha256: str) -> FullRelationalManifest:
    value = object.__new__(FullRelationalManifest)
    object.__setattr__(value, "spec", spec)
    object.__setattr__(value, "scope", FULL_D0_ARTIFACT)
    object.__setattr__(value, "cell_domains", cell_domains)
    object.__setattr__(value, "seed_sets", seed_sets)
    object.__setattr__(value, "tables", tables)
    object.__setattr__(value, "coverage_sha256", coverage_sha256)
    object.__setattr__(value, "authority_sha256", authority_sha256)
    return value


def _compile_full_relational_manifest(*, owner_contract: D0Contract, s1_extent: str,
                                      hmm_preexecution_plan: HmmPreexecutionPlan,
                                      computation_preexecution_plan: ComputationPreexecutionPlan
                                      ) -> FullRelationalManifest:
    spec = FullManifestSpec(
        manifest_schema_version=FULL_MANIFEST_SCHEMA_VERSION,
        owner_contract=deepcopy(owner_contract),
        owner_sha256=FROZEN_D0_OWNER_SHA256,
        s1_extent=s1_extent,
        hmm_preexecution_plan=deepcopy(hmm_preexecution_plan),
        computation_preexecution_plan=deepcopy(computation_preexecution_plan),
    )
    primitives = _compile_full_relational_manifest_primitives(
        owner_contract=deepcopy(spec.owner_contract),
        s1_extent=spec.s1_extent,
        hmm_preexecution_plan=deepcopy(spec.hmm_preexecution_plan),
        computation_preexecution_plan=deepcopy(spec.computation_preexecution_plan),
    )
    return _materialize_full_components(spec=spec, primitives=primitives)


def _clone_full_relational_manifest(value: FullRelationalManifest) -> FullRelationalManifest:
    return _new_full_relational_manifest(
        spec=deepcopy(value.spec),
        cell_domains=deepcopy(value.cell_domains),
        seed_sets=deepcopy(value.seed_sets),
        tables=deepcopy(value.tables),
        coverage_sha256=value.coverage_sha256,
        authority_sha256=value.authority_sha256,
    )


def build_full_relational_manifest(*, owner_contract: D0Contract, s1_extent: str,
                                   hmm_preexecution_plan: HmmPreexecutionPlan,
                                   computation_preexecution_plan: ComputationPreexecutionPlan
                                   ) -> FullRelationalManifest:
    probe = FullManifestSpec(
        manifest_schema_version=FULL_MANIFEST_SCHEMA_VERSION,
        owner_contract=deepcopy(owner_contract),
        owner_sha256=FROZEN_D0_OWNER_SHA256,
        s1_extent=s1_extent,
        hmm_preexecution_plan=deepcopy(hmm_preexecution_plan),
        computation_preexecution_plan=deepcopy(computation_preexecution_plan),
    )
    canonical = _compile_full_relational_manifest(
        owner_contract=probe.owner_contract,
        s1_extent=probe.s1_extent,
        hmm_preexecution_plan=probe.hmm_preexecution_plan,
        computation_preexecution_plan=probe.computation_preexecution_plan,
    )
    return _clone_full_relational_manifest(canonical)


def assert_full_manifest_authority(manifest: FullRelationalManifest) -> None:
    if type(manifest) is not FullRelationalManifest:
        _fail("FULL authority", "exact opaque FullRelationalManifest required")
    if type(manifest.spec) is not FullManifestSpec:
        _fail("FULL authority", "exact FullManifestSpec required")
    _validate_full_manifest_spec(manifest.spec)
    if (type(manifest.scope) is not str or manifest.scope != FULL_D0_ARTIFACT
            or type(manifest.cell_domains) is not tuple
            or any(type(item) is not CellDomain for item in manifest.cell_domains)
            or type(manifest.seed_sets) is not tuple
            or any(type(item) is not SeedSet for item in manifest.seed_sets)
            or type(manifest.tables) is not tuple
            or any(type(item) is not TableExpectation for item in manifest.tables)
            or type(manifest.coverage_sha256) is not str
            or type(manifest.authority_sha256) is not str):
        _fail("FULL authority", "typed canonical fields required")
    canonical = _compile_full_relational_manifest(
        owner_contract=manifest.spec.owner_contract,
        s1_extent=manifest.spec.s1_extent,
        hmm_preexecution_plan=manifest.spec.hmm_preexecution_plan,
        computation_preexecution_plan=manifest.spec.computation_preexecution_plan,
    )
    if manifest != canonical:
        _fail("FULL authority", "canonical recompilation mismatch")


@dataclass(frozen=True, slots=True)
class TypedIdentityField:
    name: str
    atom_type: str
    value: str | int | bool

    def __post_init__(self) -> None:
        if type(self.name) is not str or not self.name:
            _fail("ordinary identity field", "non-empty name required")
        expected = {"str": str, "int": int, "bool": bool}.get(self.atom_type)
        if expected is None or type(self.value) is not expected:
            _fail("ordinary identity field", "exact declared atom type required")


@dataclass(frozen=True, slots=True)
class TypedConsumerPrimaryKey:
    schema: str
    table: str
    fields: tuple[TypedIdentityField, ...]

    def __post_init__(self) -> None:
        if type(self.schema) is not str or type(self.table) is not str:
            _fail("ordinary consumer key", "schema/table strings required")
        if (type(self.fields) is not tuple or not self.fields
                or any(type(item) is not TypedIdentityField for item in self.fields)
                or len({item.name for item in self.fields}) != len(self.fields)):
            _fail("ordinary consumer key", "unique typed fields required")


@dataclass(frozen=True, slots=True)
class TypedWorkKey:
    schema: str
    kind: str
    fields: tuple[TypedIdentityField, ...]

    def __post_init__(self) -> None:
        if type(self.schema) is not str or type(self.kind) is not str:
            _fail("ordinary work key", "schema/kind strings required")
        if (type(self.fields) is not tuple or not self.fields
                or any(type(item) is not TypedIdentityField for item in self.fields)
                or len({item.name for item in self.fields}) != len(self.fields)):
            _fail("ordinary work key", "unique typed fields required")


@dataclass(frozen=True, slots=True)
class OrdinaryLogicalIdentity:
    projection: str
    schema: str
    phase: str
    operation: str
    work_key: TypedWorkKey
    computation_id: str

    def __post_init__(self) -> None:
        if any(type(value) is not str or not value for value in (
                self.projection, self.schema, self.phase, self.operation,
                self.computation_id)):
            _fail("ordinary logical identity", "non-empty exact strings required")
        if type(self.work_key) is not TypedWorkKey:
            _fail("ordinary logical identity", "typed work key required")
        if not re.fullmatch(r"d0c1-[0-9a-f]{64}", self.computation_id):
            _fail("ordinary logical identity", "canonical computation id required")


@dataclass(frozen=True, slots=True)
class OrdinaryIdentityBinding:
    projection: str
    table: str
    binding_kind: str
    consumer_primary_key: TypedConsumerPrimaryKey
    logical_computation_id: str

    def __post_init__(self) -> None:
        if any(type(value) is not str or not value for value in (
                self.projection, self.table, self.binding_kind,
                self.logical_computation_id)):
            _fail("ordinary binding", "non-empty exact strings required")
        if type(self.consumer_primary_key) is not TypedConsumerPrimaryKey:
            _fail("ordinary binding", "typed consumer key required")
        if self.table != self.consumer_primary_key.table:
            _fail("ordinary binding", "table/key mismatch")
        if not re.fullmatch(r"d0c1-[0-9a-f]{64}", self.logical_computation_id):
            _fail("ordinary binding", "canonical computation id required")


@dataclass(frozen=True, slots=True, init=False)
class OrdinaryIdentityPlan:
    owner_sha256: str
    identity_binding_sha256: str
    computations: tuple[OrdinaryLogicalIdentity, ...]
    bindings: tuple[OrdinaryIdentityBinding, ...]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        _fail("ordinary identity plan", "direct construction forbidden; use factory")


_ORDINARY_PROJECTIONS = (
    "S2_off", "S2_on", "S3", "BPS", "B2_clean", "B2_controlled", "S4",
)
_ORDINARY_EXPECTED_COUNTS = {
    "S2_off": (540, 60), "S2_on": (1620, 1620), "S3": (10800, 10800),
    "BPS": (7200, 3600), "B2_clean": (1200, 600),
    "B2_controlled": (21600, 10800), "S4": (7, 7),
}


def _ordinary_authority(owner_authority: Any) -> D0OwnerIdentityAuthority:
    if type(owner_authority) is not D0OwnerIdentityAuthority:
        _fail("ordinary identity", "exact D0OwnerIdentityAuthority required")
    try:
        assert_frozen_owner_identity_authority(owner_authority)
    except ContractError as error:
        _fail("ordinary identity", f"owner authority mismatch: {error}")
    return owner_authority


def _ordinary_value(source: str, raw: Mapping[str, Any]) -> Any:
    if source.startswith("raw."):
        name = source[4:]
        if name not in raw:
            _fail("ordinary identity", f"raw source {source} is absent")
        return raw[name]
    if source.startswith("literal.") and len(source) > len("literal."):
        return source[len("literal."):]
    _fail("ordinary identity", f"unsupported owner source {source}")


def _ordinary_fields(descriptors: Any, raw: Mapping[str, Any]) -> tuple[TypedIdentityField, ...]:
    if type(descriptors) is not tuple or not descriptors:
        _fail("ordinary identity", "owner descriptor tuple required")
    result = []
    for descriptor in descriptors:
        if not isinstance(descriptor, Mapping) or tuple(descriptor) != (
                "name", "source", "atom_type"):
            _fail("ordinary identity", "exact owner descriptor required")
        name = descriptor["name"]
        source = descriptor["source"]
        atom_type = descriptor["atom_type"]
        if any(type(value) is not str or not value for value in (name, source, atom_type)):
            _fail("ordinary identity", "descriptor strings required")
        result.append(TypedIdentityField(name, atom_type, _ordinary_value(source, raw)))
    return tuple(result)


def _ordinary_rule(rule: Any, raw: Mapping[str, Any]) -> str:
    if not isinstance(rule, Mapping) or type(rule.get("kind")) is not str:
        _fail("ordinary identity", "typed phase/operation rule required")
    if rule["kind"] == "literal" and tuple(rule) == ("kind", "value"):
        value = rule["value"]
    elif rule["kind"] == "enum_map" and tuple(rule) == ("kind", "source", "values"):
        source = _ordinary_value(rule["source"], raw)
        values = rule["values"]
        if not isinstance(values, Mapping) or source not in values:
            _fail("ordinary identity", "enum-map source outside owner domain")
        value = values[source]
    else:
        _fail("ordinary identity", "unknown or malformed owner rule")
    if type(value) is not str or not value:
        _fail("ordinary identity", "rule result must be a non-empty string")
    return value


def _ordinary_raw_records(owner: D0OwnerIdentityAuthority):
    contract = owner.contract
    domain = owner.ordinary_domain
    fixtures = domain.fixtures
    tuples = domain.tuple_ids
    cells = tuple(cell.cell_id for cell in contract.population_manifest)
    pols = domain.polarizations
    aliases = domain.controlled_cell_aliases
    registry = contract.seed_registry
    s2_seeds = registry.range_for("controlled_damage_recovery").values
    s3_dev = registry.range_for("observability_fusion_dev").values
    s3_test = registry.range_for("controlled_observability").values
    common = registry.range_for("common_cpr_and_b2_dev").values

    for seed, cell, pol, fixture in product(s2_seeds, aliases, pols, fixtures):
        yield "S2_off", {
            "record_type": domain.s2_record_types[0], "seed": seed, "cell_id": cell,
            "target_polarization": pol, "fixture_id": fixture,
            "jump_present": False, "method_id": domain.s2_methods[0],
        }
    methods = domain.s2_methods
    for seed, cell, pol, fixture, method in product(
            s2_seeds, aliases, pols, fixtures, methods):
        yield "S2_on", {
            "record_type": domain.s2_record_types[0], "seed": seed, "cell_id": cell,
            "target_polarization": pol, "fixture_id": fixture,
            "jump_present": True, "method_id": method,
        }
    splits = domain.s3_record_types
    split_seeds = dict(zip(splits, (s3_dev, s3_test), strict=True))
    for record_type in splits:
        for seed, cell, pol, fixture, candidate in product(
                split_seeds[record_type], aliases, pols, fixtures, domain.candidates):
            yield "S3", {
                "record_type": record_type, "seed": seed, "cell_id": cell,
                "target_polarization": pol, "fixture_id": fixture,
                "candidate_id": candidate,
            }
    for tuple_id, b, nw, seed, cell, pol in product(
            tuples, domain.b_values, domain.nw_values, common, cells, pols):
        yield "BPS", {
            "record_type": domain.bps_record_types[0], "tuple_id": tuple_id,
            "B": b, "Nw": nw, "seed": seed, "cell_id": cell,
            "polarization": pol,
        }
    for tuple_id, seed, cell, pol in product(tuples, common, cells, pols):
        yield "B2_clean", {
            "record_type": domain.b2_clean_record_types[0], "tuple_id": tuple_id,
            "seed": seed, "cell_id": cell, "polarization": pol,
        }
    for tuple_id, seed, cell, target, fixture, row_pol in product(
            tuples, common, cells, pols, fixtures, pols):
        yield "B2_controlled", {
            "record_type": domain.b2_controlled_record_types[0], "tuple_id": tuple_id,
            "seed": seed, "cell_id": cell, "target_polarization": target,
            "fixture_id": fixture, "row_polarization": row_pol,
        }
    for check_id in domain.s4_checks:
        yield "S4", {"record_type": domain.s4_record_types[0], "check_id": check_id}


def _identity_payload(identity: OrdinaryLogicalIdentity) -> dict[str, Any]:
    return {
        "schema": identity.schema,
        "phase": identity.phase,
        "operation": identity.operation,
        "work_key": {
            "schema": identity.work_key.schema,
            "kind": identity.work_key.kind,
            "fields": [
                {"name": item.name, "atom": {"type": item.atom_type, "value": item.value}}
                for item in identity.work_key.fields
            ],
        },
    }


def _new_ordinary_plan(*, owner_sha256: str, identity_binding_sha256: str,
                       computations: tuple[OrdinaryLogicalIdentity, ...],
                       bindings: tuple[OrdinaryIdentityBinding, ...]) -> OrdinaryIdentityPlan:
    value = object.__new__(OrdinaryIdentityPlan)
    object.__setattr__(value, "owner_sha256", owner_sha256)
    object.__setattr__(value, "identity_binding_sha256", identity_binding_sha256)
    object.__setattr__(value, "computations", computations)
    object.__setattr__(value, "bindings", bindings)
    return value


def _compile_ordinary_identity_plan(owner_authority: D0OwnerIdentityAuthority) -> OrdinaryIdentityPlan:
    owner = _ordinary_authority(owner_authority)
    identity = owner.identity_binding
    payloads = identity.payload_schemas
    projections = identity.consumer_bindings["projections"]
    if tuple(projections) != (
            "S2_off", "S2_on", "S3", "BPS", "B2_clean", "B2_controlled",
            "HMM_chunk", "S4"):
        _fail("ordinary identity", "owner projection order mismatch")
    pk_schema = payloads["consumer_primary_key"]["version"]
    work_schema = payloads["typed_work_key"]["version"]
    logical_schema = payloads["logical_computation_identity"]["version"]
    computations_by_id: dict[str, OrdinaryLogicalIdentity] = {}
    bindings = []
    for projection_name, raw in _ordinary_raw_records(owner):
        projection = projections[projection_name]
        if projection["exact_binding_kind"] != "LOGICAL_COMPUTATION_ID":
            _fail("ordinary identity", "ordinary binding kind mismatch")
        table = projection["table"]
        pk_fields = _ordinary_fields(projection["consumer_pk_fields"], raw)
        if tuple(item.name for item in pk_fields) != _PK[table]:
            _fail("ordinary identity", "consumer PK descriptor order mismatch")
        work_fields = _ordinary_fields(projection["work_key_fields"], raw)
        if "work_key_order" in projection and tuple(item.name for item in work_fields) != tuple(
                projection["work_key_order"]):
            _fail("ordinary identity", "work-key descriptor order mismatch")
        work_key = TypedWorkKey(work_schema, projection["work_key_kind"], work_fields)
        phase = _ordinary_rule(projection["phase_rule"], raw)
        operation = _ordinary_rule(projection["operation_rule"], raw)
        logical_probe = OrdinaryLogicalIdentity(
            projection_name, logical_schema, phase, operation, work_key,
            "d0c1-" + "0" * 64,
        )
        computation_id = "d0c1-" + _digest(_identity_payload(logical_probe))
        logical = replace(logical_probe, computation_id=computation_id)
        previous = computations_by_id.setdefault(computation_id, logical)
        if previous != logical:
            _fail("ordinary identity", "canonical logical-id collision")
        consumer_key = TypedConsumerPrimaryKey(pk_schema, table, pk_fields)
        bindings.append(OrdinaryIdentityBinding(
            projection_name, table, projection["exact_binding_kind"],
            consumer_key, computation_id,
        ))
    computations = tuple(computations_by_id.values())
    bindings_tuple = tuple(bindings)
    binding_counts = Counter(item.projection for item in bindings_tuple)
    computation_counts = Counter(item.projection for item in computations)
    if ({name: (binding_counts[name], computation_counts[name])
         for name in _ORDINARY_PROJECTIONS} != _ORDINARY_EXPECTED_COUNTS
            or len(bindings_tuple) != 42967 or len(computations) != 27487
            or len({item.consumer_primary_key for item in bindings_tuple}) != 42967):
        _fail("ordinary identity", "D018 exact cardinality mismatch")
    return _new_ordinary_plan(
        owner_sha256=owner.owner_sha256,
        identity_binding_sha256=owner.identity_binding_sha256,
        computations=computations,
        bindings=bindings_tuple,
    )


def build_ordinary_identity_plan(*, owner_authority: D0OwnerIdentityAuthority) -> OrdinaryIdentityPlan:
    """Build a fresh owner-authenticated ordinary identity graph."""

    return _compile_ordinary_identity_plan(owner_authority)


def assert_ordinary_identity_plan(
    plan: OrdinaryIdentityPlan, *, owner_authority: D0OwnerIdentityAuthority,
) -> None:
    """Freshly recompile and compare; plan-carried seals are never authority."""

    owner = _ordinary_authority(owner_authority)
    if type(plan) is not OrdinaryIdentityPlan:
        _fail("ordinary identity plan", "exact opaque plan required")
    if (type(plan.owner_sha256) is not str
            or type(plan.identity_binding_sha256) is not str
            or type(plan.computations) is not tuple
            or any(type(item) is not OrdinaryLogicalIdentity for item in plan.computations)
            or type(plan.bindings) is not tuple
            or any(type(item) is not OrdinaryIdentityBinding for item in plan.bindings)):
        _fail("ordinary identity plan", "typed frozen graph required")
    canonical = _compile_ordinary_identity_plan(owner)
    if plan != canonical:
        _fail("ordinary identity plan", "fresh canonical recompilation mismatch")


def _require_hard_output(value: Any) -> None:
    try:
        assert_decoder_hard_output_ref(value)
    except (TypeError, SchemaError) as error:
        _fail("ordinary consumer output", f"issued hard-output ref required: {error}")


@dataclass(frozen=True, slots=True)
class S2OffConsumerOutput:
    hard_output: DecoderHardOutputRef

    def __post_init__(self) -> None:
        _require_hard_output(self.hard_output)


@dataclass(frozen=True, slots=True)
class S2OnConsumerOutput:
    hard_output: DecoderHardOutputRef

    def __post_init__(self) -> None:
        _require_hard_output(self.hard_output)


@dataclass(frozen=True, slots=True)
class S3ConsumerOutput:
    hard_output: DecoderHardOutputRef
    pilot_score: float
    decoder_score: float

    def __post_init__(self) -> None:
        _require_hard_output(self.hard_output)
        if (type(self.pilot_score) is not float or type(self.decoder_score) is not float
                or not math.isfinite(self.pilot_score)
                or not math.isfinite(self.decoder_score)):
            _fail("S3 consumer output", "finite exact float64 scores required")


@dataclass(frozen=True, slots=True)
class BpsConsumerOutput:
    hard_output: DecoderHardOutputRef
    selected_global_rotation_k: int
    selected_normalized_reencode_nll: float

    def __post_init__(self) -> None:
        _require_hard_output(self.hard_output)
        if (type(self.selected_global_rotation_k) is not int
                or self.selected_global_rotation_k not in (0, 1, 2, 3)):
            _fail("BPS consumer output", "exact rotation integer required")
        if (type(self.selected_normalized_reencode_nll) is not float
                or not math.isfinite(self.selected_normalized_reencode_nll)):
            _fail("BPS consumer output", "finite exact float64 NLL required")


@dataclass(frozen=True, slots=True)
class B2CleanConsumerOutput:
    hard_output: DecoderHardOutputRef

    def __post_init__(self) -> None:
        _require_hard_output(self.hard_output)


@dataclass(frozen=True, slots=True)
class B2ControlledConsumerOutput:
    hard_output: DecoderHardOutputRef

    def __post_init__(self) -> None:
        _require_hard_output(self.hard_output)


@dataclass(frozen=True, slots=True)
class S4ConsumerOutput:
    tested_instances: int
    failed_instances: int
    passed: bool
    evidence_sha256: str

    def __post_init__(self) -> None:
        if (type(self.tested_instances) is not int or self.tested_instances < 1
                or type(self.failed_instances) is not int
                or not 0 <= self.failed_instances <= self.tested_instances
                or type(self.passed) is not bool
                or self.passed != (self.failed_instances == 0)
                or type(self.evidence_sha256) is not str
                or re.fullmatch(r"[0-9a-f]{64}", self.evidence_sha256) is None):
            _fail("S4 consumer output", "exact count/pass/evidence fields required")


_ORDINARY_OUTPUT_TYPES = {
    "S2_off": S2OffConsumerOutput,
    "S2_on": S2OnConsumerOutput,
    "S3": S3ConsumerOutput,
    "BPS": BpsConsumerOutput,
    "B2_clean": B2CleanConsumerOutput,
    "B2_controlled": B2ControlledConsumerOutput,
    "S4": S4ConsumerOutput,
}
_ORDINARY_OUTPUT_SCHEMAS = {
    "S2_off": "coded_decoder_feedback.d0.consumer_output.s2_off.v1",
    "S2_on": "coded_decoder_feedback.d0.consumer_output.s2_on.v1",
    "S3": "coded_decoder_feedback.d0.consumer_output.s3.v1",
    "BPS": "coded_decoder_feedback.d0.consumer_output.bps.v1",
    "B2_clean": "coded_decoder_feedback.d0.consumer_output.b2_clean.v1",
    "B2_controlled": "coded_decoder_feedback.d0.consumer_output.b2_controlled.v1",
    "S4": "coded_decoder_feedback.d0.consumer_output.s4.v1",
}


def _ordinary_output_payload(projection: str, output: Any) -> dict[str, Any]:
    expected = _ORDINARY_OUTPUT_TYPES.get(projection)
    if expected is None or type(output) is not expected:
        _fail("ordinary consumer output", f"wrong typed variant for {projection}")
    schema = _ORDINARY_OUTPUT_SCHEMAS[projection]
    if projection == "S4":
        return {
            "schema": schema,
            "tested_instances": output.tested_instances,
            "failed_instances": output.failed_instances,
            "passed": output.passed,
            "evidence_sha256": output.evidence_sha256,
        }
    _require_hard_output(output.hard_output)
    payload = {
        "schema": schema,
        "decoder_hard_output_sha256": output.hard_output.decoder_hard_output_sha256,
    }
    if projection == "S3":
        payload["pilot_score_float64_hex"] = output.pilot_score.hex()
        payload["decoder_score_float64_hex"] = output.decoder_score.hex()
    elif projection == "BPS":
        payload["selected_global_rotation_k"] = output.selected_global_rotation_k
        payload["selected_normalized_reencode_nll_float64_hex"] = (
            output.selected_normalized_reencode_nll.hex()
        )
    return payload


def _typed_pk_payload(key: TypedConsumerPrimaryKey) -> dict[str, Any]:
    if type(key) is not TypedConsumerPrimaryKey:
        _fail("ordinary provenance", "typed consumer primary key required")
    return {
        "schema": key.schema,
        "table": key.table,
        "fields": [
            {"name": field.name, "atom": {"type": field.atom_type, "value": field.value}}
            for field in key.fields
        ],
    }


@dataclass(frozen=True, slots=True)
class OrdinaryProvenanceEntry:
    ordinal: int
    consumer_primary_key: TypedConsumerPrimaryKey
    consumer_output: Any
    cache_status: str
    source_computation_id: str | None
    source_consumer_primary_key: TypedConsumerPrimaryKey | None
    projection: str

    @property
    def payload(self) -> Mapping[str, Any]:
        return MappingProxyType({
            "ordinal": self.ordinal,
            "consumer_primary_key": _typed_pk_payload(self.consumer_primary_key),
            "consumer_output": _ordinary_output_payload(self.projection, self.consumer_output),
            "cache_status": self.cache_status,
            "source_computation_id": self.source_computation_id,
            "source_consumer_primary_key": (
                None if self.source_consumer_primary_key is None
                else _typed_pk_payload(self.source_consumer_primary_key)
            ),
        })


@dataclass(frozen=True, slots=True)
class OrdinaryProvenanceRecord:
    logical_computation_id: str
    entries: tuple[OrdinaryProvenanceEntry, ...]
    ordinary_consumer_provenance_manifest_sha256: str

    @property
    def payload(self) -> Mapping[str, Any]:
        return MappingProxyType({
            "schema": "coded_decoder_feedback.d0.ordinary_consumer_provenance.v1",
            "logical_computation_id": self.logical_computation_id,
            "entries": [dict(entry.payload) for entry in self.entries],
        })

    @property
    def store_record(self) -> Mapping[str, Any]:
        return MappingProxyType({
            "schema": "coded_decoder_feedback.d0.ordinary_consumer_provenance_store_record.v1",
            "ordinary_consumer_provenance_manifest_sha256": (
                self.ordinary_consumer_provenance_manifest_sha256
            ),
            "payload": self.payload,
        })


@dataclass(frozen=True, slots=True)
class OrdinaryAggregateLedgerBinding:
    computation_id: str
    phase: str
    operation: str
    cache_status: str
    source_computation_id: str | None
    content_sha256: str


@dataclass(frozen=True, slots=True, init=False, weakref_slot=True)
class OrdinaryRuntimeBundle:
    records: tuple[OrdinaryProvenanceRecord, ...]
    aggregate_ledger: tuple[OrdinaryAggregateLedgerBinding, ...]
    hard_output_store: tuple[DecoderHardOutputRef, ...]
    counts: Mapping[str, int]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        _fail("ordinary runtime bundle", "direct construction forbidden; use factory")


_ORDINARY_BUNDLE_ISSUANCE: dict[int, tuple[Any, str, str, str]] = {}


def _structural_fingerprint(value: Any) -> str:
    """Process-local exact structural fingerprint; no carried hash is authority."""
    digest = hashlib.sha256()

    def frame(tag: bytes, payload: bytes = b"") -> None:
        digest.update(tag)
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)

    def walk(item: Any) -> None:
        if item is None:
            frame(b"N")
        elif type(item) is bool:
            frame(b"B", b"1" if item else b"0")
        elif type(item) is int:
            frame(b"I", str(item).encode("ascii"))
        elif type(item) is float:
            if not math.isfinite(item):
                _fail("structural fingerprint", "non-finite float forbidden")
            frame(b"F", item.hex().encode("ascii"))
        elif type(item) is str:
            frame(b"S", item.encode("utf-8"))
        elif type(item) is DecoderHardOutputRef:
            frame(b"R", str(id(item)).encode("ascii"))
            frame(b"r", item._root.encode("ascii"))
            frame(b"p", item._payload_json.encode("utf-8"))
        elif type(item) in (tuple, list):
            frame(b"T" if type(item) is tuple else b"L", str(len(item)).encode("ascii"))
            for child in item:
                walk(child)
        elif isinstance(item, Mapping):
            frame(b"M", str(len(item)).encode("ascii"))
            for key, child in item.items():
                walk(key)
                walk(child)
        elif is_dataclass(item):
            frame(b"D", type(item).__qualname__.encode("utf-8"))
            for field in fields(item):
                frame(b"K", field.name.encode("utf-8"))
                walk(getattr(item, field.name))
        else:
            _fail("structural fingerprint", f"unsupported exact type: {type(item)!r}")

    walk(value)
    return digest.hexdigest()


def _register_ordinary_bundle(bundle: OrdinaryRuntimeBundle,
                              owner: D0OwnerIdentityAuthority) -> None:
    key = id(bundle)
    reference = weakref.ref(bundle, lambda _ref, identity=key: _ORDINARY_BUNDLE_ISSUANCE.pop(identity, None))
    _ORDINARY_BUNDLE_ISSUANCE[key] = (
        reference, owner.owner_sha256, owner.identity_binding_sha256,
        _structural_fingerprint(bundle),
    )


def _assert_issued_ordinary_bundle(bundle: OrdinaryRuntimeBundle, *,
                                   owner_authority: D0OwnerIdentityAuthority) -> None:
    owner = _ordinary_authority(owner_authority)
    if type(bundle) is not OrdinaryRuntimeBundle:
        _fail("ordinary runtime bundle", "exact factory-issued bundle required")
    issuance = _ORDINARY_BUNDLE_ISSUANCE.get(id(bundle))
    if (issuance is None or issuance[0]() is not bundle
            or issuance[1] != owner.owner_sha256
            or issuance[2] != owner.identity_binding_sha256
            or issuance[3] != _structural_fingerprint(bundle)):
        _fail("ordinary runtime bundle", "issuance/owner/current fingerprint mismatch")


def _new_ordinary_runtime_bundle(*, records, aggregate_ledger, hard_output_store,
                                 counts) -> OrdinaryRuntimeBundle:
    value = object.__new__(OrdinaryRuntimeBundle)
    object.__setattr__(value, "records", records)
    object.__setattr__(value, "aggregate_ledger", aggregate_ledger)
    object.__setattr__(value, "hard_output_store", hard_output_store)
    object.__setattr__(value, "counts", MappingProxyType(dict(counts)))
    return value


def _pk_values(key: TypedConsumerPrimaryKey) -> dict[str, Any]:
    return {field.name: field.value for field in key.fields}


def _pk_index_key(projection: str, key: TypedConsumerPrimaryKey):
    return projection, tuple((field.name, field.value) for field in key.fields)


def _lookup_pk(index, projection: str, fields: tuple[tuple[str, Any], ...]):
    try:
        return index[(projection, fields)]
    except KeyError as error:
        _fail("ordinary provenance", f"canonical source PK absent for {projection}")


def _build_ordinary_runtime_bundle(*, plan: OrdinaryIdentityPlan,
                                   owner_authority: D0OwnerIdentityAuthority,
                                   outputs_by_pk: Mapping[TypedConsumerPrimaryKey, Any],
                                   reauthenticate: bool) -> OrdinaryRuntimeBundle:
    owner = _ordinary_authority(owner_authority)
    if reauthenticate:
        assert_ordinary_identity_plan(plan, owner_authority=owner)
    if not isinstance(outputs_by_pk, Mapping):
        _fail("ordinary runtime bundle", "outputs_by_pk mapping required")
    binding_by_pk = {binding.consumer_primary_key: binding for binding in plan.bindings}
    if (len(outputs_by_pk) != len(binding_by_pk)
            or set(outputs_by_pk) != set(binding_by_pk)):
        _fail("ordinary runtime bundle", "outputs_by_pk exact coverage mismatch")
    for pk, output in outputs_by_pk.items():
        binding = binding_by_pk[pk]
        _ordinary_output_payload(binding.projection, output)

    pk_index = {
        _pk_index_key(binding.projection, binding.consumer_primary_key):
        binding.consumer_primary_key
        for binding in plan.bindings
    }
    groups: dict[str, list[OrdinaryIdentityBinding]] = {}
    for binding in plan.bindings:
        groups.setdefault(binding.logical_computation_id, []).append(binding)
    logical_by_id = {item.computation_id: item for item in plan.computations}
    pol_order = {value: index for index, value in enumerate(owner.ordinary_domain.polarizations)}
    fixture_order = {value: index for index, value in enumerate(owner.ordinary_domain.fixtures)}
    entry_by_pk: dict[TypedConsumerPrimaryKey, OrdinaryProvenanceEntry] = {}
    records = []
    aggregate = []
    hard_refs: dict[str, DecoderHardOutputRef] = {}
    counters = Counter()

    for computation_id, raw_group in groups.items():
        projection = raw_group[0].projection
        if any(item.projection != projection for item in raw_group):
            _fail("ordinary provenance", "cross-projection logical group")
        if projection == "S2_off":
            ordered = sorted(raw_group, key=lambda item: fixture_order[_pk_values(item.consumer_primary_key)["fixture_id"]])
        elif projection in ("BPS", "B2_clean"):
            ordered = sorted(raw_group, key=lambda item: pol_order[_pk_values(item.consumer_primary_key)["polarization"]])
        elif projection == "B2_controlled":
            ordered = sorted(raw_group, key=lambda item: (
                _pk_values(item.consumer_primary_key)["row_polarization"]
                != _pk_values(item.consumer_primary_key)["target_polarization"]
            ))
        else:
            ordered = list(raw_group)
        counters[{1: "singleton_groups", 2: "two_entry_groups", 9: "nine_entry_groups"}.get(len(ordered), "bad_group")] += 1
        entries = []
        for ordinal, binding in enumerate(ordered):
            pk = binding.consumer_primary_key
            values = _pk_values(pk)
            status = "EXECUTED"
            source_pk = None
            source_id = None
            if projection == "S2_off" and ordinal > 0:
                status = "CACHE_READ"
                source_pk = ordered[0].consumer_primary_key
                source_id = computation_id
                counters["s2_cache_edges"] += 1
            elif projection == "BPS" and values["tuple_id"] == "M3_N100":
                status = "CACHE_READ"
                source_fields = tuple(
                    (field.name, "M2_N100" if field.name == "tuple_id" else field.value)
                    for field in pk.fields
                )
                source_pk = _lookup_pk(pk_index, "BPS", source_fields)
                source_id = binding_by_pk[source_pk].logical_computation_id
                counters["bps_cache_edges"] += 1
            elif projection == "B2_controlled" and (
                    values["row_polarization"] != values["target_polarization"]):
                status = "CACHE_READ"
                source_fields = (
                    ("record_type", owner.ordinary_domain.b2_clean_record_types[0]),
                    ("tuple_id", values["tuple_id"]),
                    ("seed", values["seed"]),
                    ("cell_id", values["cell_id"]),
                    ("polarization", values["row_polarization"]),
                )
                source_pk = _lookup_pk(pk_index, "B2_clean", source_fields)
                source_id = binding_by_pk[source_pk].logical_computation_id
                counters["b2_cache_edges"] += 1
            entry = OrdinaryProvenanceEntry(
                ordinal, pk, outputs_by_pk[pk], status, source_id, source_pk, projection
            )
            entries.append(entry)
            entry_by_pk[pk] = entry
            counters["executed_entries" if status == "EXECUTED" else "cache_read_entries"] += 1
            if projection != "S4":
                ref = outputs_by_pk[pk].hard_output
                previous = hard_refs.setdefault(ref.decoder_hard_output_sha256, ref)
                if dict(previous.payload) != dict(ref.payload):
                    _fail("ordinary provenance", "hard-output root collision")
        payload = {
            "schema": "coded_decoder_feedback.d0.ordinary_consumer_provenance.v1",
            "logical_computation_id": computation_id,
            "entries": [dict(entry.payload) for entry in entries],
        }
        root = hashlib.sha256(_canonical_json_bytes(payload)).hexdigest()
        records.append(OrdinaryProvenanceRecord(computation_id, tuple(entries), root))
        executed = [entry for entry in entries if entry.cache_status == "EXECUTED"]
        if executed:
            aggregate_status, aggregate_source = "EXECUTED", None
            counters["aggregate_executed"] += 1
        else:
            sources = {entry.source_computation_id for entry in entries}
            if len(sources) != 1 or None in sources:
                _fail("ordinary provenance", "all-cache group has non-unique source")
            aggregate_status, aggregate_source = "CACHE_READ", next(iter(sources))
            counters["aggregate_cache_read"] += 1
        logical = logical_by_id[computation_id]
        aggregate.append(OrdinaryAggregateLedgerBinding(
            computation_id, logical.phase, logical.operation, aggregate_status,
            aggregate_source, root,
        ))

    for entry in entry_by_pk.values():
        if entry.cache_status == "CACHE_READ":
            source = entry_by_pk.get(entry.source_consumer_primary_key)
            if (source is None or source.cache_status != "EXECUTED"
                    or source.source_computation_id is not None
                    or source.source_consumer_primary_key is not None
                    or binding_by_pk[source.consumer_primary_key].logical_computation_id
                    != entry.source_computation_id):
                _fail("ordinary provenance", "cache source is not a direct EXECUTED leaf")
            consumer_payload = _ordinary_output_payload(entry.projection, entry.consumer_output)
            source_projection = binding_by_pk[source.consumer_primary_key].projection
            source_payload = _ordinary_output_payload(source_projection, source.consumer_output)
            if (consumer_payload.get("decoder_hard_output_sha256")
                    != source_payload.get("decoder_hard_output_sha256")):
                _fail("ordinary provenance", "cache/source decoded content mismatch")
            if entry.projection == source_projection and consumer_payload != source_payload:
                _fail("ordinary provenance", "cache/source output mismatch")

    records.sort(key=lambda item: item.logical_computation_id)
    aggregate.sort(key=lambda item: item.computation_id)
    hard_store = tuple(sorted(hard_refs.values(), key=lambda item: item.decoder_hard_output_sha256))
    validate_decoder_hard_output_store(
        tuple(item.store_record for item in hard_store),
        referenced_roots=frozenset(hard_refs),
    )
    counts = {
        "records": len(records), "entries": len(entry_by_pk),
        "executed_entries": counters["executed_entries"],
        "cache_read_entries": counters["cache_read_entries"],
        "s2_cache_edges": counters["s2_cache_edges"],
        "bps_cache_edges": counters["bps_cache_edges"],
        "b2_cache_edges": counters["b2_cache_edges"],
        "singleton_groups": counters["singleton_groups"],
        "nine_entry_groups": counters["nine_entry_groups"],
        "two_entry_groups": counters["two_entry_groups"],
        "aggregate_executed": counters["aggregate_executed"],
        "aggregate_cache_read": counters["aggregate_cache_read"],
    }
    expected_counts = {
        "records": 27487, "entries": 42967, "executed_entries": 30247,
        "cache_read_entries": 12720, "s2_cache_edges": 480,
        "bps_cache_edges": 1440, "b2_cache_edges": 10800,
        "singleton_groups": 12427, "nine_entry_groups": 60,
        "two_entry_groups": 15000, "aggregate_executed": 26767,
        "aggregate_cache_read": 720,
    }
    if counts != expected_counts or counters["bad_group"]:
        _fail("ordinary runtime bundle", "owner static counts mismatch")
    return _new_ordinary_runtime_bundle(
        records=tuple(records), aggregate_ledger=tuple(aggregate),
        hard_output_store=hard_store, counts=counts,
    )


def build_ordinary_runtime_bundle(*, plan: OrdinaryIdentityPlan,
                                  owner_authority: D0OwnerIdentityAuthority,
                                  outputs_by_pk: Mapping[TypedConsumerPrimaryKey, Any]) -> OrdinaryRuntimeBundle:
    owner = _ordinary_authority(owner_authority)
    bundle = _build_ordinary_runtime_bundle(
        plan=plan, owner_authority=owner_authority, outputs_by_pk=outputs_by_pk,
        reauthenticate=True,
    )
    _register_ordinary_bundle(bundle, owner)
    return bundle


def assert_ordinary_runtime_bundle(bundle: OrdinaryRuntimeBundle, *,
                                   plan: OrdinaryIdentityPlan,
                                   owner_authority: D0OwnerIdentityAuthority) -> None:
    if type(bundle) is not OrdinaryRuntimeBundle:
        _fail("ordinary runtime bundle", "exact opaque bundle required")
    outputs = {}
    for record in bundle.records:
        if type(record) is not OrdinaryProvenanceRecord:
            _fail("ordinary runtime bundle", "typed provenance records required")
        for entry in record.entries:
            if type(entry) is not OrdinaryProvenanceEntry or entry.consumer_primary_key in outputs:
                _fail("ordinary runtime bundle", "duplicate or untyped provenance entry")
            outputs[entry.consumer_primary_key] = entry.consumer_output
    canonical = _build_ordinary_runtime_bundle(
        plan=plan, owner_authority=owner_authority, outputs_by_pk=outputs,
        reauthenticate=True,
    )
    if bundle != canonical:
        _fail("ordinary runtime bundle", "fresh canonical recompilation mismatch")


@dataclass(frozen=True, slots=True)
class ResolvedMemberContent:
    ordinal: int
    content_sha256: str
    normalized_nll: float

    def __post_init__(self) -> None:
        if (type(self.ordinal) is not int or self.ordinal < 0
                or type(self.content_sha256) is not str
                or re.fullmatch(r"[0-9a-f]{64}", self.content_sha256) is None
                or type(self.normalized_nll) is not float
                or not math.isfinite(self.normalized_nll)):
            _fail("resolved HMM member", "exact ordinal/content/binary64 required")


@dataclass(frozen=True, slots=True, init=False)
class HmmRuntimeAggregateContent:
    stratum_role: str
    computation_ids_manifest_sha256: str
    resolved_members: tuple[ResolvedMemberContent, ...]
    normalized_nll_exact_sum_numerator_decimal: str
    normalized_nll_exact_sum_denominator_power2: int
    member_count: int
    content_sha256: str

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        _fail("HMM runtime aggregate", "direct construction forbidden; use factory")

    @property
    def payload(self) -> Mapping[str, Any]:
        return MappingProxyType({
            "schema": "coded_decoder_feedback.d0.hmm_runtime_aggregate_content.v1",
            "computation_ids_manifest_sha256": self.computation_ids_manifest_sha256,
            "resolved_member_contents": [
                {"ordinal": item.ordinal, "content_sha256": item.content_sha256}
                for item in self.resolved_members
            ],
            "normalized_nll_exact_sum_numerator_decimal": (
                self.normalized_nll_exact_sum_numerator_decimal
            ),
            "normalized_nll_exact_sum_denominator_power2": (
                self.normalized_nll_exact_sum_denominator_power2
            ),
            "member_count": self.member_count,
        })


def _new_hmm_runtime_content(*, role, manifest, members, numerator, exponent, root):
    value = object.__new__(HmmRuntimeAggregateContent)
    object.__setattr__(value, "stratum_role", role)
    object.__setattr__(value, "computation_ids_manifest_sha256", manifest)
    object.__setattr__(value, "resolved_members", members)
    object.__setattr__(value, "normalized_nll_exact_sum_numerator_decimal", str(numerator))
    object.__setattr__(value, "normalized_nll_exact_sum_denominator_power2", exponent)
    object.__setattr__(value, "member_count", len(members))
    object.__setattr__(value, "content_sha256", root)
    return value


def build_hmm_runtime_aggregate_content(*, stratum_role: str,
                                        computation_ids_manifest_sha256: str,
                                        resolved_members: tuple[ResolvedMemberContent, ...]
                                        ) -> HmmRuntimeAggregateContent:
    expected_counts = {
        "CLEAN_INCLUDED": 10,
        "CONTROLLED_TARGET_INCLUDED": 90,
        "CONTROLLED_SENTINEL_EXCLUDED": 90,
    }
    if stratum_role not in expected_counts:
        _fail("HMM runtime aggregate", "unknown stratum role")
    if (type(computation_ids_manifest_sha256) is not str
            or re.fullmatch(r"[0-9a-f]{64}", computation_ids_manifest_sha256) is None):
        _fail("HMM runtime aggregate", "canonical computation manifest root required")
    if (type(resolved_members) is not tuple
            or len(resolved_members) != expected_counts[stratum_role]
            or any(type(item) is not ResolvedMemberContent for item in resolved_members)
            or tuple(item.ordinal for item in resolved_members) != tuple(range(len(resolved_members)))):
        _fail("HMM runtime aggregate", "exact ordered role member set required")
    total = sum((Fraction.from_float(item.normalized_nll) for item in resolved_members), Fraction())
    denominator = total.denominator
    if denominator & (denominator - 1):
        raise AssertionError("binary64 exact sum denominator is not a power of two")
    exponent = denominator.bit_length() - 1
    probe = _new_hmm_runtime_content(
        role=stratum_role, manifest=computation_ids_manifest_sha256,
        members=resolved_members, numerator=total.numerator, exponent=exponent,
        root="0" * 64,
    )
    root = hashlib.sha256(_canonical_json_bytes(dict(probe.payload))).hexdigest()
    return _new_hmm_runtime_content(
        role=stratum_role, manifest=computation_ids_manifest_sha256,
        members=resolved_members, numerator=total.numerator, exponent=exponent, root=root,
    )


def assert_hmm_runtime_aggregate_content(content: HmmRuntimeAggregateContent, *,
                                         stratum_role: str) -> None:
    if type(content) is not HmmRuntimeAggregateContent:
        _fail("HMM runtime aggregate", "exact opaque runtime content required")
    canonical = build_hmm_runtime_aggregate_content(
        stratum_role=stratum_role,
        computation_ids_manifest_sha256=content.computation_ids_manifest_sha256,
        resolved_members=content.resolved_members,
    )
    if content != canonical:
        _fail("HMM runtime aggregate", "canonical runtime recompilation mismatch")


@dataclass(frozen=True, slots=True)
class HmmTrajectoryAuthority:
    computation_id: str
    tuple_id: str
    stratum_role: str
    seed: int
    cell_id: str
    polarization: str
    target_polarization: str | None
    fixture_id: str | None
    cache_status: str
    source_computation_id: str | None
    logical_primitive_scores: int
    materialized_primitive_scores: int
    dual_pol_pair_scores: int


@dataclass(frozen=True, slots=True, init=False)
class OwnerHmmRuntimePlan:
    trajectories: tuple[HmmTrajectoryAuthority, ...]
    trajectory_count: int
    chunk_count: int
    executed_count: int
    cache_read_count: int
    full_ledger_count_with_ordinary: int
    trajectory_authority_sha256: str
    chunk_identity_sha256: str
    golden_roots: Mapping[str, str]
    authority_sha256: str

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        _fail("owner HMM runtime plan", "direct construction forbidden; use factory")


def _typed_atom(name: str, atom_type: str, value: Any) -> dict[str, Any]:
    return {"name": name, "atom": {"type": atom_type, "value": value}}


def _typed_payload(schema: str, kind_name: str, kind: str,
                   items: tuple[tuple[str, str, Any], ...]) -> dict[str, Any]:
    return {"schema": schema, kind_name: kind,
            "fields": [_typed_atom(name, atom_type, value) for name, atom_type, value in items]}


def _hmm_logical_id(tuple_id: str, role: str, seed: int, cell: str, pol: str,
                    target: str | None = None, fixture: str | None = None) -> str:
    items = [
        ("tuple_id", "str", tuple_id), ("stratum_role", "str", role),
        ("seed", "int", seed), ("cell_id", "str", cell),
        ("polarization", "str", pol),
    ]
    if role != "CLEAN_INCLUDED":
        items.extend((("target_polarization", "str", target),
                      ("fixture_id", "str", fixture)))
    work = _typed_payload(
        "coded_decoder_feedback.d0.typed_work_key.v1", "kind",
        "HMM_TRAJECTORY_FULL_122_BY_6_GRID", tuple(items),
    )
    logical = {
        "schema": "coded_decoder_feedback.d0.logical_computation_identity.v1",
        "phase": "B2_DEV", "operation": "HMM_GRID_SCORE", "work_key": work,
    }
    return "d0c1-" + hashlib.sha256(_canonical_json_bytes(logical)).hexdigest()


def _hmm_primary_key(table: str, items: tuple[tuple[str, str, Any], ...]) -> dict[str, Any]:
    return {
        "schema": "coded_decoder_feedback.d0.consumer_primary_key.v1",
        "table": table,
        "fields": [_typed_atom(name, atom_type, value) for name, atom_type, value in items],
    }


def _hmm_chunk_vector(owner: D0OwnerIdentityAuthority, *, tuple_id: str, role: str,
                      cell: str, pol: str, p_index: int = 0, sigma_index: int = 0):
    identity = owner.identity_binding
    hmm = identity.hmm_authority
    p_value = identity.grid_authority["p_s"]["standalone_payload"]["values"][p_index]["float64_hex"]
    sigma_value = identity.grid_authority["sigma_e2"]["standalone_payload"]["values"][sigma_index]["float64_hex"]
    pilot = hmm["pilot_count_by_tuple"][tuple_id]
    group = _typed_payload(
        "coded_decoder_feedback.d0.hmm_group_identity.v1", "kind",
        "HMM_GRID_CHUNK_GROUP", (
            ("tuple_id", "str", tuple_id), ("p_s_index", "int", p_index),
            ("p_s_float64_hex", "float64_hex", p_value),
            ("sigma_e2_index", "int", sigma_index),
            ("sigma_e2_float64_hex", "float64_hex", sigma_value),
            ("stratum_role", "str", role), ("cell_id", "str", cell),
            ("polarization", "str", pol), ("pilot_count", "int", pilot),
        ),
    )
    chunk_id = "hmmg1-" + hashlib.sha256(_canonical_json_bytes(group)).hexdigest()
    chunk_pk = _hmm_primary_key("b2_hmm_grid_chunk", (
        ("record_type", "str", "B2_HMM_GRID_CHUNK"),
        ("tuple_id", "str", tuple_id), ("p_s_index", "int", p_index),
        ("sigma_e2_index", "int", sigma_index), ("stratum_role", "str", role),
        ("cell_id", "str", cell), ("polarization", "str", pol),
        ("chunk_id", "str", chunk_id),
    ))
    opposite = next(value for value in owner.ordinary_domain.polarizations if value != pol)
    axes = ([(seed, None, None) for seed in range(8000, 8010)]
            if role == "CLEAN_INCLUDED" else
            [(seed, fixture, pol if role == "CONTROLLED_TARGET_INCLUDED" else opposite)
             for seed in range(8000, 8010)
             for fixture in owner.identity_binding.hmm_authority["fixture_owner_legal_order"]])
    members = []
    bindings = []
    for ordinal, (seed, fixture, target) in enumerate(axes):
        if role == "CLEAN_INCLUDED":
            member_pk = _hmm_primary_key("b2_tuple_clean_dev", (
                ("record_type", "str", "B2_TUPLE_CLEAN_DEV"),
                ("tuple_id", "str", tuple_id), ("seed", "int", seed),
                ("cell_id", "str", cell), ("polarization", "str", pol),
            ))
        else:
            member_pk = _hmm_primary_key("b2_tuple_controlled_dev", (
                ("record_type", "str", "B2_TUPLE_CONTROLLED_DEV"),
                ("tuple_id", "str", tuple_id), ("seed", "int", seed),
                ("cell_id", "str", cell), ("target_polarization", "str", target),
                ("fixture_id", "str", fixture), ("row_polarization", "str", pol),
            ))
        computation_id = _hmm_logical_id(tuple_id, role, seed, cell, pol, target, fixture)
        status, source = "EXECUTED", None
        if tuple_id == "M3_N100" or role == "CONTROLLED_SENTINEL_EXCLUDED":
            status = "CACHE_READ"
            source_tuple = "M2_N100" if tuple_id == "M3_N100" else tuple_id
            source_role = "CLEAN_INCLUDED" if role == "CONTROLLED_SENTINEL_EXCLUDED" else role
            source = _hmm_logical_id(
                source_tuple, source_role, seed, cell, pol,
                target if source_role != "CLEAN_INCLUDED" else None,
                fixture if source_role != "CLEAN_INCLUDED" else None,
            )
        members.append({"ordinal": ordinal, "member_primary_key": member_pk})
        bindings.append({
            "schema": "coded_decoder_feedback.d0.hmm_computation_binding.v1",
            "ordinal": ordinal, "member_primary_key": member_pk,
            "computation_id": computation_id, "cache_status": status,
            "source_computation_id": source,
        })
    member_manifest = {
        "schema": "coded_decoder_feedback.d0.hmm_member_key_manifest.v1",
        "consumer_primary_key": chunk_pk, "members": members,
    }
    computation_manifest = {
        "schema": "coded_decoder_feedback.d0.computation_id_manifest.v1",
        "group": {"group_identity": group, "chunk_id": chunk_id,
                  "consumer_primary_key": chunk_pk, "pilot_count": pilot},
        "aggregate": {"algorithm": "CANONICAL_BINARY64_EXACT_RATIONAL_SUM_V1",
                      "member_count": len(members)},
        "bindings": bindings,
    }
    return {
        "chunk_id": chunk_id,
        "member_root": hashlib.sha256(_canonical_json_bytes(member_manifest)).hexdigest(),
        "computation_root": hashlib.sha256(_canonical_json_bytes(computation_manifest)).hexdigest(),
        "first_id": bindings[0]["computation_id"],
        "first_source": bindings[0]["source_computation_id"],
    }


def hmm_chunk_authority_binding(*, owner_authority: D0OwnerIdentityAuthority,
                                tuple_id: str, stratum_role: str, cell_id: str,
                                polarization: str, p_s_index: int,
                                sigma_e2_index: int) -> Mapping[str, str]:
    """Recompute one HMM chunk's owner-bound identity commitments.

    Callers that consume evidence must separately authenticate the complete owner
    once; this narrow projection contains no caller-supplied seed axis.
    """

    if type(owner_authority) is not D0OwnerIdentityAuthority:
        _fail("HMM chunk authority", "exact owner authority required")
    try:
        vector = _hmm_chunk_vector(
            owner_authority, tuple_id=tuple_id, role=stratum_role,
            cell=cell_id, pol=polarization, p_index=p_s_index,
            sigma_index=sigma_e2_index,
        )
    except (KeyError, IndexError, StopIteration, TypeError) as exc:
        _fail("HMM chunk authority", f"group is outside owner axes: {exc}")
    return MappingProxyType({
        "chunk_id": vector["chunk_id"],
        "member_root": vector["member_root"],
        "computation_root": vector["computation_root"],
    })


def _compile_owner_hmm_runtime_plan(owner_authority: D0OwnerIdentityAuthority) -> OwnerHmmRuntimePlan:
    owner = _ordinary_authority(owner_authority)
    hmm = owner.identity_binding.hmm_authority
    tuples = tuple(hmm["tuple_legal_order"])
    cells = tuple(cell.cell_id for cell in owner.contract.population_manifest)
    pols = owner.ordinary_domain.polarizations
    fixtures = tuple(hmm["fixture_owner_legal_order"])
    seeds = tuple(range(hmm["seed_axis"]["first"], hmm["seed_axis"]["last"] + 1))
    trajectories = []
    trajectory_hasher = hashlib.sha256()
    for tuple_id, seed, cell, pol in product(tuples, seeds, cells, pols):
        opposite = next(value for value in pols if value != pol)
        cases = [("CLEAN_INCLUDED", None, None)]
        cases.extend(("CONTROLLED_TARGET_INCLUDED", pol, fixture) for fixture in fixtures)
        cases.extend(("CONTROLLED_SENTINEL_EXCLUDED", opposite, fixture) for fixture in fixtures)
        for role, target, fixture in cases:
            computation_id = _hmm_logical_id(tuple_id, role, seed, cell, pol, target, fixture)
            status, source = "EXECUTED", None
            if tuple_id == "M3_N100" or role == "CONTROLLED_SENTINEL_EXCLUDED":
                status = "CACHE_READ"
                source_tuple = "M2_N100" if tuple_id == "M3_N100" else tuple_id
                source_role = "CLEAN_INCLUDED" if role == "CONTROLLED_SENTINEL_EXCLUDED" else role
                source = _hmm_logical_id(
                    source_tuple, source_role, seed, cell, pol,
                    target if source_role != "CLEAN_INCLUDED" else None,
                    fixture if source_role != "CLEAN_INCLUDED" else None,
                )
            item = HmmTrajectoryAuthority(
                computation_id, tuple_id, role, seed, cell, pol, target, fixture,
                status, source, 732, 732 if status == "EXECUTED" else 0,
                732 if pol == pols[0] else 0,
            )
            trajectories.append(item)
            trajectory_hasher.update(_canonical_json_bytes([
                item.computation_id, item.tuple_id, item.stratum_role, item.seed,
                item.cell_id, item.polarization, item.target_polarization,
                item.fixture_id, item.cache_status, item.source_computation_id,
                item.logical_primitive_scores, item.materialized_primitive_scores,
                item.dual_pol_pair_scores,
            ]))
            trajectory_hasher.update(b"\n")
    by_id = {item.computation_id: item for item in trajectories}
    if len(by_id) != len(trajectories):
        _fail("owner HMM runtime plan", "trajectory identity collision")
    for item in trajectories:
        if item.cache_status == "CACHE_READ":
            source = by_id.get(item.source_computation_id)
            if (source is None or source.cache_status != "EXECUTED"
                    or source.source_computation_id is not None
                    or item.materialized_primitive_scores != 0):
                _fail("owner HMM runtime plan", "cache source/cost is not a direct leaf")
    grid = owner.identity_binding.grid_authority
    p_values = tuple(grid["p_s"]["standalone_payload"]["values"])
    sigma_values = tuple(grid["sigma_e2"]["standalone_payload"]["values"])
    chunk_hasher = hashlib.sha256()
    chunk_count = 0
    for tuple_id, p_value, sigma_value, role, cell, pol in product(
            tuples, p_values, sigma_values,
            ("CLEAN_INCLUDED", "CONTROLLED_TARGET_INCLUDED", "CONTROLLED_SENTINEL_EXCLUDED"),
            cells, pols):
        pilot = hmm["pilot_count_by_tuple"][tuple_id]
        group_probe = [
            tuple_id, p_value["index"], p_value["float64_hex"],
            sigma_value["index"], sigma_value["float64_hex"], role, cell, pol, pilot,
        ]
        chunk_hasher.update(_canonical_json_bytes(group_probe))
        chunk_hasher.update(b"\n")
        chunk_count += 1
    golden_specs = {
        "clean10": ("M2_N100", "CLEAN_INCLUDED", pols[0]),
        "target90": ("M2_N100", "CONTROLLED_TARGET_INCLUDED", pols[0]),
        "sentinel90_to_clean": ("M2_N100", "CONTROLLED_SENTINEL_EXCLUDED", pols[1]),
        "M3_N100_direct_to_M2": ("M3_N100", "CLEAN_INCLUDED", pols[0]),
    }
    golden_roots = {}
    goldens = owner.identity_binding.golden_vectors
    for name, (tuple_id, role, pol) in golden_specs.items():
        vector = _hmm_chunk_vector(owner, tuple_id=tuple_id, role=role,
                                   cell=cells[0], pol=pol)
        expected = goldens[name]
        if (vector["chunk_id"] != expected["chunk_id"]
                or vector["member_root"] != expected["member_key_manifest_sha256"]
                or vector["computation_root"] != expected["computation_ids_manifest_sha256"]
                or vector["first_id"] != expected["first_logical_computation_id"]
                or ("first_source_computation_id" in expected
                    and vector["first_source"] != expected["first_source_computation_id"])):
            _fail("owner HMM runtime plan", f"owner golden mismatch: {name}")
        golden_roots[name] = vector["computation_root"]
    counts = Counter(item.cache_status for item in trajectories)
    authority_payload = {
        "schema": "coded_decoder_feedback.d0.owner_hmm_runtime_plan.v1",
        "owner_sha256": owner.owner_sha256,
        "trajectory_count": len(trajectories), "chunk_count": chunk_count,
        "executed_count": counts["EXECUTED"], "cache_read_count": counts["CACHE_READ"],
        "trajectory_authority_sha256": trajectory_hasher.hexdigest(),
        "chunk_identity_sha256": chunk_hasher.hexdigest(),
        "golden_roots": golden_roots,
    }
    if (len(trajectories), chunk_count, counts["EXECUTED"], counts["CACHE_READ"]) != (
            22800, 263520, 9600, 13200):
        _fail("owner HMM runtime plan", "exact owner counts mismatch")
    value = object.__new__(OwnerHmmRuntimePlan)
    for name, field_value in (
        ("trajectories", tuple(trajectories)), ("trajectory_count", len(trajectories)),
        ("chunk_count", chunk_count), ("executed_count", counts["EXECUTED"]),
        ("cache_read_count", counts["CACHE_READ"]),
        ("full_ledger_count_with_ordinary", 27487 + len(trajectories)),
        ("trajectory_authority_sha256", trajectory_hasher.hexdigest()),
        ("chunk_identity_sha256", chunk_hasher.hexdigest()),
        ("golden_roots", MappingProxyType(dict(golden_roots))),
        ("authority_sha256", hashlib.sha256(_canonical_json_bytes(authority_payload)).hexdigest()),
    ):
        object.__setattr__(value, name, field_value)
    return value


def build_owner_hmm_runtime_plan(*, owner_authority: D0OwnerIdentityAuthority) -> OwnerHmmRuntimePlan:
    return _compile_owner_hmm_runtime_plan(owner_authority)


def assert_owner_hmm_runtime_plan(plan: OwnerHmmRuntimePlan, *,
                                  owner_authority: D0OwnerIdentityAuthority) -> None:
    if type(plan) is not OwnerHmmRuntimePlan:
        _fail("owner HMM runtime plan", "exact opaque plan required")
    if plan != _compile_owner_hmm_runtime_plan(owner_authority):
        _fail("owner HMM runtime plan", "fresh canonical recompilation mismatch")


@dataclass(frozen=True, slots=True, init=False, weakref_slot=True)
class AuthenticatedFullAuthority:
    owner_sha256: str
    ordinary_bundle: OrdinaryRuntimeBundle
    hmm_plan: OwnerHmmRuntimePlan
    hmm_runtime_contents: tuple[HmmRuntimeAggregateContent, ...]
    ordinary_ledger_count: int
    hmm_ledger_count: int
    total_ledger_count: int
    raw_table_authority_sha256: str
    authority_sha256: str

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        _fail("authenticated FULL", "direct construction forbidden; use factory")


_AUTHENTICATED_FULL_ISSUANCE: dict[int, tuple[Any, str, str]] = {}


def _authenticated_full_structural_fingerprint(value: AuthenticatedFullAuthority) -> str:
    return _structural_fingerprint((
        value.owner_sha256, id(value.ordinary_bundle), value.hmm_plan,
        value.hmm_runtime_contents, value.ordinary_ledger_count,
        value.hmm_ledger_count, value.total_ledger_count,
        value.raw_table_authority_sha256, value.authority_sha256,
    ))


def _authenticated_full_payload(*, owner: D0OwnerIdentityAuthority,
                                ordinary_bundle: OrdinaryRuntimeBundle,
                                hmm_plan: OwnerHmmRuntimePlan,
                                hmm_runtime_contents: tuple[HmmRuntimeAggregateContent, ...],
                                raw_root: str) -> dict[str, Any]:
    return {
        "schema": "coded_decoder_feedback.d0.authenticated_full_authority.v1",
        "owner_sha256": owner.owner_sha256,
        "ordinary_record_roots_sha256": _digest([
            item.ordinary_consumer_provenance_manifest_sha256
            for item in ordinary_bundle.records
        ]),
        "hmm_plan_sha256": hmm_plan.authority_sha256,
        "hmm_runtime_content_roots": [item.content_sha256 for item in hmm_runtime_contents],
        "ordinary_ledger_count": 27487, "hmm_ledger_count": 22800,
        "total_ledger_count": 50287, "raw_table_authority_sha256": raw_root,
    }


def _register_authenticated_full(value: AuthenticatedFullAuthority,
                                 owner: D0OwnerIdentityAuthority) -> None:
    key = id(value)
    reference = weakref.ref(value, lambda _ref, identity=key: _AUTHENTICATED_FULL_ISSUANCE.pop(identity, None))
    _AUTHENTICATED_FULL_ISSUANCE[key] = (
        reference, owner.owner_sha256, _authenticated_full_structural_fingerprint(value),
    )


def build_authenticated_full_authority(*, owner_authority: D0OwnerIdentityAuthority,
                                       ordinary_bundle: OrdinaryRuntimeBundle,
                                       hmm_runtime_contents: tuple[HmmRuntimeAggregateContent, ...]
    ) -> AuthenticatedFullAuthority:
    owner = _ordinary_authority(owner_authority)
    _assert_issued_ordinary_bundle(ordinary_bundle, owner_authority=owner)
    hmm_plan = build_owner_hmm_runtime_plan(owner_authority=owner)
    if (type(hmm_runtime_contents) is not tuple or not hmm_runtime_contents
            or any(type(item) is not HmmRuntimeAggregateContent for item in hmm_runtime_contents)):
        _fail("authenticated FULL", "typed representative HMM runtime contents required")
    for item in hmm_runtime_contents:
        assert_hmm_runtime_aggregate_content(item, stratum_role=item.stratum_role)
    if (len(hmm_runtime_contents) != 4
            or {item.computation_ids_manifest_sha256 for item in hmm_runtime_contents}
            != set(hmm_plan.golden_roots.values())):
        _fail("authenticated FULL", "exact four representative HMM runtime groups required")
    raw_root = _digest({
        "owner_sha256": owner.owner_sha256,
        "tables": [[table, list(_PK[table])] for table in sorted(_PK)],
    })
    payload = _authenticated_full_payload(
        owner=owner, ordinary_bundle=ordinary_bundle, hmm_plan=hmm_plan,
        hmm_runtime_contents=hmm_runtime_contents, raw_root=raw_root,
    )
    value = object.__new__(AuthenticatedFullAuthority)
    for name, field_value in (
        ("owner_sha256", owner.owner_sha256), ("ordinary_bundle", ordinary_bundle),
        ("hmm_plan", hmm_plan), ("hmm_runtime_contents", hmm_runtime_contents),
        ("ordinary_ledger_count", 27487), ("hmm_ledger_count", 22800),
        ("total_ledger_count", 50287), ("raw_table_authority_sha256", raw_root),
        ("authority_sha256", hashlib.sha256(_canonical_json_bytes(payload)).hexdigest()),
    ):
        object.__setattr__(value, name, field_value)
    _register_authenticated_full(value, owner)
    return value


def assert_authenticated_full_authority(authority: AuthenticatedFullAuthority, *,
                                        owner_authority: D0OwnerIdentityAuthority) -> None:
    if type(authority) is not AuthenticatedFullAuthority:
        _fail("authenticated FULL", "exact opaque FULL authority required")
    owner = _ordinary_authority(owner_authority)
    issuance = _AUTHENTICATED_FULL_ISSUANCE.get(id(authority))
    if (issuance is None or issuance[0]() is not authority
            or issuance[1] != owner.owner_sha256
            or issuance[2] != _authenticated_full_structural_fingerprint(authority)):
        _fail("authenticated FULL", "issuance/current fingerprint mismatch")
    _assert_issued_ordinary_bundle(authority.ordinary_bundle, owner_authority=owner)
    for content in authority.hmm_runtime_contents:
        assert_hmm_runtime_aggregate_content(content, stratum_role=content.stratum_role)
    if (type(authority.hmm_plan) is not OwnerHmmRuntimePlan
            or authority.hmm_plan.trajectory_count != 22800
            or authority.hmm_plan.chunk_count != 263520
            or authority.hmm_plan.executed_count != 9600
            or authority.hmm_plan.cache_read_count != 13200):
        _fail("authenticated FULL", "issued HMM plan counts mismatch")
    expected_payload = _authenticated_full_payload(
        owner=owner, ordinary_bundle=authority.ordinary_bundle,
        hmm_plan=authority.hmm_plan,
        hmm_runtime_contents=authority.hmm_runtime_contents,
        raw_root=authority.raw_table_authority_sha256,
    )
    if (authority.owner_sha256 != owner.owner_sha256
            or authority.ordinary_ledger_count != 27487
            or authority.hmm_ledger_count != 22800
            or authority.total_ledger_count != 50287
            or authority.authority_sha256
            != hashlib.sha256(_canonical_json_bytes(expected_payload)).hexdigest()):
        _fail("authenticated FULL", "canonical FULL authority mismatch")


def _expected_ledger_signature(table: str, row: Any) -> tuple[str, str]:
    if table == "s2_method":
        operation = {
            S2_METHODS[0]: "B1_DECODE",
            S2_METHODS[1]: "B2_DECODE",
            S2_METHODS[2]: "O1_DECODE",
        }[row.method_id]
        return "S2", operation
    if table == "s3_candidate":
        phase = "S3_DEV" if row.record_type == "S3_CANDIDATE_DEV" else "S3_TEST"
        return phase, "CANDIDATE_DECODE"
    if table == "bps_dev_score":
        return "BPS_DEV", "B1_DECODE"
    if table in {"b2_tuple_clean_dev", "b2_tuple_controlled_dev"}:
        return "B2_DEV", "B2_DECODE"
    _fail("relations", f"no ledger consumer contract for {table}")


def _validate_relational_rows(
    rows_by_table: Mapping[str, tuple[Any, ...]],
    manifest: RelationalManifest | FullRelationalManifest,
) -> None:
    if (type(rows_by_table) is not dict
            or type(manifest) not in {RelationalManifest, FullRelationalManifest}):
        _fail("relations", "exact dict and typed manifest required")
    if any(table not in TABLE_MODELS for table in rows_by_table):
        _fail("relations", "unknown table")
    seeds = {item.record_type: set(item.exact_values) for item in manifest.seed_sets}
    cells = {value for domain in manifest.cell_domains for value in domain.exact_values}
    for table, rows in rows_by_table.items():
        if type(rows) is not tuple:
            _fail(table, "rows must be tuple")
        keys = []
        for row in rows:
            if type(row) is not TABLE_MODELS[table]:
                _fail(table, "wrong row model")
            _local_invariants(table, row)
            keys.append(tuple(getattr(row, field) for field in _PK[table]))
            if hasattr(row, "cell_id") and row.cell_id not in cells:
                _fail(table, "orphan/cross-cell FK")
            if hasattr(row, "seed"):
                label = row.record_type
                if label not in seeds or row.seed not in seeds[label]:
                    _fail(table, "orphan/cross-seed FK")
        if len(keys) != len(set(keys)):
            _fail(table, "duplicate primary key")

    ledger = rows_by_table.get("computation_ledger", ())
    computations = {row.computation_id: row for row in ledger}
    consumers: dict[str, list[tuple[str, Any]]] = {}
    for table, rows in rows_by_table.items():
        if table == "computation_ledger":
            continue
        for row in rows:
            if not hasattr(row, "computation_id"):
                continue
            computation = computations.get(row.computation_id)
            if computation is None:
                _fail(table, "orphan computation FK")
            expected = _expected_ledger_signature(table, row)
            if (computation.phase, computation.operation) != expected:
                _fail(table, "computation phase/operation binding mismatch")
            if hasattr(row, "cache_status") and (
                row.cache_status != computation.cache_status
                or row.source_computation_id != computation.source_computation_id
            ):
                _fail(table, "raw/ledger cache provenance mismatch")
            consumers.setdefault(row.computation_id, []).append((table, row))
    for row in ledger:
        signature = (row.phase, row.operation)
        if signature not in _CONSUMER_LEDGER_SIGNATURES | _STANDALONE_LEDGER_SIGNATURES:
            _fail("computation_ledger", "invalid phase/operation pairing")
        if row.source_computation_id is not None:
            source = computations.get(row.source_computation_id)
            if source is None or source.content_sha256 != row.content_sha256:
                _fail("computation_ledger", "cache source reverse binding mismatch")
        if signature in _CONSUMER_LEDGER_SIGNATURES and row.computation_id not in consumers:
            _fail("computation_ledger", "decoder computation has no compatible consumer")

    s2 = rows_by_table.get("s2_method", ())
    s2_groups: dict[tuple[Any, ...], list[Any]] = {}
    for row in s2:
        s2_groups.setdefault((row.seed, row.cell_id, row.target_polarization), []).append(row)
    for group in s2_groups.values():
        if {row.fixture_id for row in group} != set(FIXTURES):
            _fail("s2_method", "group must contain all nine fixtures")
        off_ids = set()
        off_cases = set()
        for fixture in FIXTURES:
            fixture_rows = [row for row in group if row.fixture_id == fixture]
            on = [row for row in fixture_rows if row.jump_present]
            off = [row for row in fixture_rows if not row.jump_present]
            if {row.method_id for row in on} != set(S2_METHODS) or len(on) != 3:
                _fail("s2_method", "on fixture requires exactly B1/B2/O1")
            if len(off) != 1 or off[0].method_id != S2_METHODS[0]:
                _fail("s2_method", "off fixture requires exactly B1")
            off_ids.add(off[0].computation_id)
            off_cases.add(off[0].physical_case_id)
        if len(off_ids) != 1 or len(off_cases) != 1:
            _fail("s2_method", "nine off projections require one computation/case")

    s3 = rows_by_table.get("s3_candidate", ())
    s3_groups: dict[tuple[Any, ...], list[Any]] = {}
    for row in s3:
        key = (row.record_type, row.seed, row.cell_id, row.target_polarization, row.fixture_id)
        s3_groups.setdefault(key, []).append(row)
    for group in s3_groups.values():
        if len(group) != 10 or {row.candidate_id for row in group} != set(CANDIDATES):
            _fail("s3_candidate", "each stratum/case requires exactly ten candidates")

    controlled = rows_by_table.get("b2_tuple_controlled_dev", ())
    control_groups: dict[tuple[Any, ...], list[Any]] = {}
    for row in controlled:
        key = (row.tuple_id, row.seed, row.cell_id, row.target_polarization, row.fixture_id)
        control_groups.setdefault(key, []).append(row)
    for group in control_groups.values():
        if len(group) != 2 or {row.row_polarization for row in group} != set(POL):
            _fail("b2_tuple_controlled_dev", "fixture requires target and sentinel rows")
        if {row.row_role for row in group} != {"TARGET_INCLUDED", "SENTINEL_EXCLUDED"}:
            _fail("b2_tuple_controlled_dev", "target/sentinel reverse binding missing")


def _validate_exact_coverage(rows_by_table: Mapping[str, tuple[Any, ...]],
                             manifest: RelationalManifest | FullRelationalManifest) -> None:
    if (type(rows_by_table) is not dict
            or type(manifest) not in {RelationalManifest, FullRelationalManifest}):
        _fail("relations", "exact dict and typed manifest required")
    expectations = {item.table: item for item in manifest.tables}
    if set(rows_by_table) != set(expectations) or len(rows_by_table) != len(expectations):
        _fail("relations", "exact declared table set required")
    for table, expectation in expectations.items():
        rows = rows_by_table[table]
        if type(rows) is not tuple or any(type(row) is not TABLE_MODELS[table] for row in rows):
            _fail(table, "typed row tuple required before coverage validation")
        for projection in expectation.projections:
            actual_keys = tuple(
                tuple(getattr(row, field) for field in projection.fields)
                for row in rows
            )
            if not actual_keys:
                _fail(table, "declared projection cannot be empty")
            count, key_sha, multiplicity_sha = _projection_digests(
                actual_keys, len(projection.fields),
            )
            if (count != projection.expected_key_count
                    or key_sha != projection.expected_keys_sha256
                    or multiplicity_sha != projection.multiplicity_by_key_sha256):
                _fail(table, "exact projection key/multiplicity coverage mismatch")


def validate_partial_relations(rows_by_table: Mapping[str, tuple[Any, ...]],
                               manifest: RelationalManifest) -> None:
    if type(manifest) is not RelationalManifest or manifest.scope != EXPLICIT_PARTIAL:
        _fail("relations", "EXPLICIT_PARTIAL manifest required")
    _validate_exact_coverage(rows_by_table, manifest)
    _validate_relational_rows(rows_by_table, manifest)


def validate_relations(rows_by_table: Mapping[str, tuple[Any, ...]],
                       manifest: FullRelationalManifest) -> None:
    assert_full_manifest_authority(manifest)
    _validate_exact_coverage(rows_by_table, manifest)
    _validate_relational_rows(rows_by_table, manifest)


@dataclass(frozen=True, slots=True)
class S4Artifact:
    contract_sha256: str
    receipt_sha256: str
    entries: tuple[Any, ...]

    def __post_init__(self) -> None:
        _validate_value("S4Artifact.contract_sha256", self.contract_sha256, F("sha"))
        _validate_value("S4Artifact.receipt_sha256", self.receipt_sha256, F("sha"))
        if type(self.entries) is not tuple:
            _fail("S4Artifact", "entries must be tuple")


def validate_s4_schema(
    artifact: S4Artifact,
    *,
    expected_contract_sha256: str,
    expected_receipt_sha256: str,
    evidence_sha256s: frozenset[str],
) -> None:
    if type(artifact) is not S4Artifact or type(evidence_sha256s) is not frozenset:
        _fail("S4", "typed artifact and frozen evidence set required")
    if artifact.contract_sha256 != expected_contract_sha256:
        _fail("S4", "contract identity mismatch")
    if artifact.receipt_sha256 != expected_receipt_sha256:
        _fail("S4", "receipt identity mismatch")
    if len(artifact.entries) != 7:
        _fail("S4", "exactly seven entries required")
    checked = []
    for entry in artifact.entries:
        if type(entry) is not TABLE_MODELS["s4_check"]:
            _fail("S4", "wrong entry type")
        checked.append(row_from_mapping("s4_check", row_to_mapping(entry)))
    identities = tuple(entry.check_id for entry in checked)
    if identities != S4_CHECK_IDS or len(set(identities)) != 7:
        _fail("S4", "stable seven-kind identity/order required")
    if any(entry.evidence_sha256 not in evidence_sha256s for entry in checked):
        _fail("S4", "orphan evidence FK")
