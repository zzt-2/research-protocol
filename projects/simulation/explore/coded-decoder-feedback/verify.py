"""Fail-closed D0 engineering accounting and S4 diagnostics.

This module emits engineering diagnostics only.  It never evaluates or names a
scientific gate, method signal, BER, goodput, PASS/KILL, or science result.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import hashlib
import inspect
import json
import math
import sys
from types import MappingProxyType
from typing import Any
from typing import get_args, get_origin
import weakref

import numpy as np

import artifacts as artifacts_module
import b2 as b2_module
import benchmark as benchmark_module
import contract as contract_module
import methods as methods_module
import receiver as receiver_module
from artifacts import ArtifactError, EvidenceReceipt, assert_evidence_receipt
from schemas import S4_CHECK_IDS


FROZEN_LOGICAL = (69_360, 1_032_000, 20_640_000)
FROZEN_MATERIALIZED = (48_900, 704_640, 14_092_800)
FROZEN_HMM = (8_344_800, 16_689_600, 7_027_200)


@dataclass(frozen=True, slots=True)
class CostLedgerSummary:
    logical: tuple[int, int, int]
    materialized: tuple[int, int, int]
    hmm: tuple[int, int, int]
    executed_rows: int
    cache_read_rows: int


@dataclass(frozen=True, slots=True)
class EngineeringDiagnostic:
    status: str
    check_count: int
    evidence_count: int
    scientific_verdict: None = None


@dataclass(frozen=True, slots=True, init=False, weakref_slot=True)
class DeploymentSeal:
    phase: str
    dev_freeze_sha256: str
    callable_ids: tuple[tuple[str, str, str], ...]
    output_sha256: str
    bps_choice: tuple[int, int]
    score: float
    receipt_bytes: bytes
    receipt_sha256: str

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        raise PermissionError("DeploymentSeal construction is controlled by seal()")

    @property
    def receipt_document(self) -> Mapping[str, Any]:
        _authenticate_deployment_seal(self)
        return MappingProxyType(json.loads(self.receipt_bytes.decode("utf-8")))


_DEPLOYMENT_SEAL_ISSUANCE: dict[
    int,
    tuple[weakref.ReferenceType[DeploymentSeal], tuple[Any, ...]],
] = {}


def _deployment_seal_fingerprint(seal: DeploymentSeal) -> tuple[Any, ...]:
    return (
        seal.phase,
        seal.dev_freeze_sha256,
        seal.callable_ids,
        seal.output_sha256,
        seal.bps_choice,
        seal.score,
        seal.receipt_bytes,
        seal.receipt_sha256,
    )


def _authenticate_deployment_seal(seal: Any) -> DeploymentSeal:
    if type(seal) is not DeploymentSeal:
        raise PermissionError("authenticated DeploymentSeal required before evaluator truth")
    issued = _DEPLOYMENT_SEAL_ISSUANCE.get(id(seal))
    if issued is None or issued[0]() is not seal:
        raise PermissionError("authenticated DeploymentSeal required before evaluator truth")
    if issued[1] != _deployment_seal_fingerprint(seal):
        raise PermissionError("tampered DeploymentSeal rejected")
    if hashlib.sha256(seal.receipt_bytes).hexdigest() != seal.receipt_sha256:
        raise PermissionError("tampered DeploymentSeal receipt hash rejected")
    try:
        document = json.loads(seal.receipt_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PermissionError("tampered DeploymentSeal canonical receipt rejected") from exc
    if artifacts_module.canonical_json_bytes(document) != seal.receipt_bytes:
        raise PermissionError("tampered DeploymentSeal canonical receipt rejected")
    expected = {
        "schema", "phase", "dev_freeze_sha256", "benchmark_freeze_binding_sha256",
        "callables", "output_sha256", "bps_choice", "score_float64_hex",
    }
    if (
        type(document) is not dict
        or set(document) != expected
        or document["schema"] != "coded_decoder_feedback.d0.deployment_seal.v1"
        or document["phase"] != seal.phase
        or document["dev_freeze_sha256"] != seal.dev_freeze_sha256
        or document["callables"] != [list(item) for item in seal.callable_ids]
        or document["output_sha256"] != seal.output_sha256
        or document["bps_choice"] != {"B": seal.bps_choice[0], "Nw": seal.bps_choice[1]}
        or document["score_float64_hex"] != seal.score.hex()
    ):
        raise PermissionError("tampered DeploymentSeal callable/freeze binding rejected")
    return seal


def _gated_evaluator(
    seal: Any,
    truth: Any = None,
    *,
    decoded_information_bits: np.ndarray,
) -> contract_module.EvaluatedTruthView:
    """Expose the real evaluator only after an authenticated deployment seal."""

    _authenticate_deployment_seal(seal)
    if type(truth) is not contract_module.TruthView:
        raise TypeError("exact TruthView required only after deployment seal")
    return contract_module.finalize_truth_view(
        truth, decoded_information_bits=decoded_information_bits
    )


_DEPLOYMENT_COMPONENTS = (
    "receiver", "B0", "B1", "B2", "scorer", "artifact", "evaluator", "benchmark",
)
_EXPECTED_CALLABLES = MappingProxyType({
    "receiver": receiver_module.run_common_bps,
    "B0": methods_module.run_b0,
    "B1": methods_module.run_b1,
    "B2": b2_module.run_b2,
    "scorer": receiver_module.estimate_post_bps_residual,
    "artifact": artifacts_module.canonical_json_bytes,
    "evaluator": _gated_evaluator,
    "benchmark": benchmark_module.run_engineering_benchmark,
})
_TRUTH_TOKENS = (
    "truthview", "truth_view", "truth", "transmitted", "tx_payload", "true_phase",
    "true_cfo", "physical_snr", "final_correctness", "event_label",
)


def deployment_callable_registry() -> Mapping[str, Any]:
    """Return the exact real production callables covered by the D0 seal."""

    return MappingProxyType(dict(_EXPECTED_CALLABLES))


def _truth_name(value: str) -> bool:
    normalized = value.replace("-", "_").replace(" ", "_").lower()
    return any(token in normalized for token in _TRUTH_TOKENS)


def _assert_truth_free_value(value: Any, path: str, active: set[int]) -> None:
    if value is inspect.Signature.empty or value is None:
        return
    if type(value) is str:
        if _truth_name(value):
            raise ValueError(f"truth-bearing callable metadata at {path}")
        return
    origin = get_origin(value)
    if origin is not None:
        _assert_truth_free_value(origin, f"{path}.origin", active)
        for index, item in enumerate(get_args(value)):
            _assert_truth_free_value(item, f"{path}.arg[{index}]", active)
        return
    if inspect.isclass(value):
        if _truth_name(f"{value.__module__}.{value.__qualname__}"):
            raise ValueError(f"truth-bearing nested type at {path}")
        return
    if type(value) in (bool, int, float, complex, bytes):
        return
    marker = id(value)
    if marker in active:
        return
    active.add(marker)
    try:
        if isinstance(value, Mapping):
            for key, item in value.items():
                _assert_truth_free_value(key, f"{path}.key", active)
                _assert_truth_free_value(item, f"{path}[{key!r}]", active)
        elif type(value) in (tuple, list, set, frozenset):
            for index, item in enumerate(value):
                _assert_truth_free_value(item, f"{path}[{index}]", active)
        elif callable(value):
            _assert_truth_free_callable(value, active=active)
        elif hasattr(value, "__dict__"):
            _assert_truth_free_value(vars(value), f"{path}.__dict__", active)
    finally:
        active.remove(marker)


def _assert_truth_free_callable(callable_value: Any, *, active: set[int] | None = None) -> None:
    if not callable(callable_value):
        raise TypeError("truth scan requires a callable")
    active = set() if active is None else active
    signature = inspect.signature(callable_value)
    for name, parameter in signature.parameters.items():
        if _truth_name(name):
            raise ValueError(f"truth-bearing callable parameter: {name}")
        _assert_truth_free_value(
            parameter.annotation, f"signature.{name}.annotation", active
        )
        _assert_truth_free_value(
            parameter.default, f"signature.{name}.default", active
        )
    _assert_truth_free_value(signature.return_annotation, "signature.return", active)
    try:
        closure = inspect.getclosurevars(callable_value)
    except TypeError:
        closure = None
    if closure is not None:
        _assert_truth_free_value(closure.nonlocals, "closure.nonlocals", active)


class DeploymentBoundary:
    """Truth-separated real-callable and dev-freeze integration boundary."""

    def __init__(self, registry: Mapping[str, Any]):
        self._registry = registry

    @staticmethod
    def assert_truth_free_callable(callable_value: Any) -> None:
        _assert_truth_free_callable(callable_value)

    def _validated_registry(self) -> Mapping[str, Any]:
        registry = self._registry
        if not isinstance(registry, Mapping) or set(registry) != set(_DEPLOYMENT_COMPONENTS):
            raise ValueError("deployment callable registry must be exact and non-empty")
        for name in _DEPLOYMENT_COMPONENTS:
            value = registry[name]
            if not callable(value):
                raise ValueError(f"deployment component {name} requires a callable")
            expected = _EXPECTED_CALLABLES[name]
            if value is not expected:
                raise ValueError(f"deployment component {name} is not the real callable")
            module_name = expected.__module__
            module = sys.modules.get(module_name)
            if module is None or getattr(module, expected.__name__, None) is not expected:
                raise ValueError(f"deployment callable module missing or rebound: {module_name}")
            if name != "evaluator":
                _assert_truth_free_callable(value)
        return registry

    @staticmethod
    def _bps_choice(resolved: contract_module.ResolvedDevFreeze) -> tuple[int, int]:
        try:
            tuple_id = resolved.parameters["final_b2_tuple"]["tuple_id"]
            matches = tuple(
                item for item in resolved.parameters["common_bps"]
                if item["tuple_id"] == tuple_id
            )
            winner = matches[0]["winner"]
            choice = (winner["B"], winner["Nw"])
        except (KeyError, IndexError, TypeError) as exc:
            raise ValueError("resolved freeze lacks one exact final BPS choice") from exc
        if len(matches) != 1 or choice[0] not in (32, 64) or choice[1] not in (31, 61, 127):
            raise ValueError("resolved freeze lacks one exact final BPS choice")
        return choice

    def seal(
        self,
        owner: contract_module.D0Contract,
        receiver_view: contract_module.ReceiverView,
        resolved: contract_module.ResolvedDevFreeze,
        *,
        phase: str,
        phase_receipts: Sequence[Mapping[str, Any]],
    ) -> DeploymentSeal:
        registry = self._validated_registry()
        if type(phase) is not str or not phase:
            raise ValueError("deployment phase must be a non-empty authorized action")
        if type(owner) is not contract_module.D0Contract:
            raise TypeError("exact D0Contract required")
        contract_module.assert_action_authorized(phase, owner)
        if type(receiver_view) is not contract_module.ReceiverView:
            raise TypeError("exact ReceiverView required")
        if type(resolved) is not contract_module.ResolvedDevFreeze:
            raise TypeError("exact ResolvedDevFreeze required")
        binding = benchmark_module.bind_resolved_freeze(
            resolved,
            tuple(phase_receipts),
            benchmark_freeze_sha256=resolved.freeze_id,
        )
        B, Nw = self._bps_choice(resolved)
        bps_result = registry["receiver"](
            receiver_view.equalized_samples[0], B=B, Nw=Nw
        )
        score = float(registry["scorer"](
            bps_result.samples, receiver_view.known_prefix[0]
        ))
        if not math.isfinite(score):
            raise ValueError("deployable score must be finite")
        digest = hashlib.sha256()
        for value in (bps_result.samples, bps_result.phase_trace):
            array = np.ascontiguousarray(value)
            digest.update(array.dtype.str.encode("ascii"))
            digest.update(str(array.shape).encode("ascii"))
            digest.update(array.tobytes(order="C"))
        output_sha256 = digest.hexdigest()
        callable_ids = tuple(
            (name, registry[name].__module__, registry[name].__qualname__)
            for name in _DEPLOYMENT_COMPONENTS
        )
        document = {
            "schema": "coded_decoder_feedback.d0.deployment_seal.v1",
            "phase": phase,
            "dev_freeze_sha256": resolved.freeze_id,
            "benchmark_freeze_binding_sha256": binding.receipt_sha256,
            "callables": callable_ids,
            "output_sha256": output_sha256,
            "bps_choice": {"B": B, "Nw": Nw},
            "score_float64_hex": score.hex(),
        }
        receipt_bytes = registry["artifact"](document)
        seal = object.__new__(DeploymentSeal)
        values = {
            "phase": phase,
            "dev_freeze_sha256": resolved.freeze_id,
            "callable_ids": callable_ids,
            "output_sha256": output_sha256,
            "bps_choice": (B, Nw),
            "score": score,
            "receipt_bytes": receipt_bytes,
            "receipt_sha256": hashlib.sha256(receipt_bytes).hexdigest(),
        }
        for name, value in values.items():
            object.__setattr__(seal, name, value)
        marker = id(seal)

        def discard(
            reference: weakref.ReferenceType[DeploymentSeal], *, key: int = marker
        ) -> None:
            current = _DEPLOYMENT_SEAL_ISSUANCE.get(key)
            if current is not None and current[0] is reference:
                _DEPLOYMENT_SEAL_ISSUANCE.pop(key, None)

        _DEPLOYMENT_SEAL_ISSUANCE[marker] = (
            weakref.ref(seal, discard),
            _deployment_seal_fingerprint(seal),
        )
        _authenticate_deployment_seal(seal)
        return seal

    def evaluate_after_seal(
        self,
        seal: DeploymentSeal,
        truth: contract_module.TruthView,
        *,
        decoded_information_bits: np.ndarray,
    ) -> contract_module.EvaluatedTruthView:
        registry = self._validated_registry()
        if type(seal) is not DeploymentSeal:
            raise TypeError("exact DeploymentSeal required before evaluator truth")
        if type(truth) is not contract_module.TruthView:
            raise TypeError("exact TruthView required only after deployment seal")
        return registry["evaluator"](
            seal, truth, decoded_information_bits=decoded_information_bits
        )


def _field(row: Any, name: str) -> Any:
    try:
        return row[name] if isinstance(row, Mapping) else getattr(row, name)
    except (KeyError, AttributeError) as exc:
        raise ValueError(f"ledger/check field missing: {name}") from exc


def _triple(row: Any, prefix: str) -> tuple[int, int, int]:
    values = tuple(_field(row, f"{prefix}_{suffix}") for suffix in (
        "decoder_batches", "cw_decodes", "bp_iterations"
    ))
    if any(type(value) is not int or value < 0 for value in values):
        raise ValueError(f"{prefix} costs must be non-negative exact integers")
    if values[2] != 20 * values[1]:
        raise ValueError(f"{prefix} BP iterations must equal 20 times CW decodes")
    return values


def reduce_cost_ledger(rows: Sequence[Any]) -> CostLedgerSummary:
    rows = tuple(rows)
    if not rows:
        raise ValueError("cost ledger cannot be empty")
    by_id: dict[str, Any] = {}
    logical = [0, 0, 0]
    materialized = [0, 0, 0]
    hmm = [0, 0, 0]
    statuses = {"EXECUTED": 0, "CACHE_READ": 0}
    for row in rows:
        computation_id = _field(row, "computation_id")
        if type(computation_id) is not str or not computation_id or computation_id in by_id:
            raise ValueError("ledger computation IDs must be unique non-empty strings")
        by_id[computation_id] = row
        status = _field(row, "cache_status")
        if status not in statuses:
            raise ValueError("ledger cache status is invalid")
        statuses[status] += 1
        source = _field(row, "source_computation_id")
        lcost = _triple(row, "logical")
        mcost = _triple(row, "materialized")
        if status == "EXECUTED" and source is not None:
            raise ValueError("executed ledger row cannot name a cache source")
        if status == "CACHE_READ" and (type(source) is not str or not source or any(mcost)):
            raise ValueError("cache ledger row requires a source and zero materialized cost")
        for index in range(3):
            logical[index] += lcost[index]
            materialized[index] += mcost[index]
        hcost = tuple(_field(row, name) for name in (
            "hmm_dual_pol_frame_parameter_pair_scores",
            "hmm_primitive_pol_trajectory_parameter_pair_scores",
            "materialized_hmm_primitive_pol_trajectory_parameter_pair_scores",
        ))
        if any(type(value) is not int or value < 0 for value in hcost):
            raise ValueError("HMM costs must be non-negative exact integers")
        for index in range(3):
            hmm[index] += hcost[index]
    for row in rows:
        if _field(row, "cache_status") == "CACHE_READ":
            source = by_id.get(_field(row, "source_computation_id"))
            if source is None or _field(source, "cache_status") != "EXECUTED":
                raise ValueError("cache source must be a direct executed ledger leaf")
            if _field(row, "content_sha256") != _field(source, "content_sha256"):
                raise ValueError("cache and source content hashes must match")
    return CostLedgerSummary(tuple(logical), tuple(materialized), tuple(hmm),
                             statuses["EXECUTED"], statuses["CACHE_READ"])


def assert_frozen_cost_totals(summary: CostLedgerSummary) -> None:
    if type(summary) is not CostLedgerSummary or (
        summary.logical, summary.materialized, summary.hmm
    ) != (FROZEN_LOGICAL, FROZEN_MATERIALIZED, FROZEN_HMM):
        raise ValueError("frozen D0 logical/materialized/HMM totals mismatch")


def assert_s3_cache_exposure(rows: Sequence[Any]) -> dict[str, int]:
    rows = tuple(rows)
    if not rows:
        raise ValueError("S3 exposure rows must be non-empty")
    groups: dict[str, dict[str, Any]] = {}
    computation_ids: set[str] = set()
    for row in rows:
        case = _field(row, "physical_case_id")
        candidate = _field(row, "candidate_id")
        computation_id = _field(row, "computation_id")
        changed = _field(row, "changed_cw_decodes")
        cached = _field(row, "cached_unchanged_cw_nll_reads")
        if type(changed) is not int or type(cached) is not int:
            raise ValueError("S3 changed/cache counts must be exact built-in ints")
        if changed < 0 or cached < 0:
            raise ValueError("S3 changed/cache counts must be non-negative")
        if computation_id in computation_ids:
            raise ValueError("S3 computation cannot cross a case or candidate")
        computation_ids.add(computation_id)
        group = groups.setdefault(case, {})
        if candidate in group:
            raise ValueError("duplicate S3 candidate exposure")
        group[candidate] = row
    expected = {"NOOP", "B04R1", "B04R2", "B04R3", "B08R1", "B08R2",
                "B08R3", "B12R1", "B12R2", "B12R3"}
    changed_total = cached_total = 0
    for group in groups.values():
        if set(group) != expected or len(group) != 10:
            raise ValueError("each S3 case requires exactly ten candidate exposures")
        changed = sum(_field(row, "changed_cw_decodes") for row in group.values())
        cached = sum(_field(row, "cached_unchanged_cw_nll_reads") for row in group.values())
        if changed != 88 or cached != 72 or any(
            _field(row, "changed_cw_decodes")
            + _field(row, "cached_unchanged_cw_nll_reads") != 16
            for row in group.values()
        ):
            raise ValueError("S3 changed/cache exposure identity mismatch")
        changed_total += changed
        cached_total += cached
    return {"physical_cases": len(groups), "logical_computations": len(rows),
            "changed_cw_decodes": changed_total,
            "cached_unchanged_cw_nll_reads": cached_total}


def assert_independent_s4_evidence(
    rows: Sequence[Any], evidence: Mapping[str, EvidenceReceipt]
) -> tuple[str, ...]:
    rows = tuple(rows)
    if tuple(_field(row, "check_id") for row in rows) != S4_CHECK_IDS:
        raise ValueError("S4 requires the exact seven checks in canonical order")
    if set(evidence) != set(S4_CHECK_IDS) or len(evidence) != 7:
        raise ValueError("S4 evidence must map one-to-one to all seven checks")
    receipts = tuple(evidence[check_id] for check_id in S4_CHECK_IDS)
    if any(type(item) is not EvidenceReceipt for item in receipts):
        raise ValueError("S4 evidence requires issued exact-byte receipts")
    try:
        for receipt in receipts:
            assert_evidence_receipt(receipt)
    except ArtifactError as exc:
        raise ValueError("S4 evidence requires receipts issued from exact bytes") from exc
    if len({item.sha256 for item in receipts}) != 7 or len({item.logical_name for item in receipts}) != 7:
        raise ValueError("S4 evidence must be seven independent one-to-one receipts")
    for row, receipt in zip(rows, receipts):
        if _field(row, "evidence_sha256") != receipt.sha256:
            raise ValueError("S4 evidence hash does not bind the actual receipt bytes")
    return S4_CHECK_IDS


def reduce_s4_engineering(
    rows: Sequence[Any], *, evidence: Mapping[str, EvidenceReceipt],
    ledger: CostLedgerSummary,
) -> EngineeringDiagnostic:
    rows = tuple(rows)
    assert_frozen_cost_totals(ledger)
    assert_independent_s4_evidence(rows, evidence)
    for row in rows:
        tested = _field(row, "tested_instances")
        failed = _field(row, "failed_instances")
        passed = _field(row, "passed")
        if (type(tested) is not int or tested < 1 or type(failed) is not int
                or not 0 <= failed <= tested or type(passed) is not bool
                or passed != (failed == 0) or not passed):
            raise ValueError("S4 engineering check failed closed")
    return EngineeringDiagnostic("ENGINEERING_DIAGNOSTIC_PASS", 7, 7)


def assert_i11_source_scope(paths: Sequence[str]) -> tuple[str, ...]:
    paths = tuple(path.replace("\\", "/") for path in paths)
    allowed = (
        "projects/simulation/explore/coded-decoder-feedback/verify.py",
        "projects/simulation/explore/coded-decoder-feedback/artifacts.py",
        "projects/simulation/tests/test_d0_artifacts_cost_s4.py",
    )
    if any(path not in allowed or "/common/" in path.lower()
           or "p05" in path.lower() or "/p08" in path.lower()
           or path.endswith("/source.py") for path in paths):
        raise ValueError("I11 source scope violation")
    return paths


__all__ = [
    "S4_CHECK_IDS", "CostLedgerSummary", "DeploymentBoundary", "DeploymentSeal",
    "EngineeringDiagnostic", "deployment_callable_registry",
    "reduce_cost_ledger", "assert_frozen_cost_totals", "assert_s3_cache_exposure",
    "assert_independent_s4_evidence", "reduce_s4_engineering",
    "assert_i11_source_scope",
]
