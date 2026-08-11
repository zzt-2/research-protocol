"""Frozen D0 B0/B1 methods and evaluator-only O1 diagnostic.

The deployable methods accept receiver-visible symbol streams only.  Truth is
used exclusively by :func:`evaluate_o1_inverse`, after B0/B1 outputs have been
sealed by :func:`freeze_deployable_outputs`.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
from types import MappingProxyType
from typing import Any, Mapping, Sequence
import weakref

import numpy as np


_DATA_SYMBOLS = 6144
_CW_COUNT = 16
_CODED_BITS_PER_CW = 1536
_BOUNDARY_TO_ID = {1536: "B04", 3072: "B08", 4608: "B12"}


class MethodError(ValueError):
    """Raised when a frozen D0 method contract is violated."""


def _readonly(value: Any, *, shape: tuple[int, ...] | None = None) -> np.ndarray:
    array = np.asarray(value)
    if shape is not None and array.shape != shape:
        raise MethodError(f"array must have exact shape {shape}")
    if not np.iscomplexobj(array) or not np.all(np.isfinite(array)):
        raise MethodError("symbol arrays must contain finite complex values")
    result = np.array(array, dtype=np.complex128, order="C", copy=True)
    result.setflags(write=False)
    return result


def _cw_ids(values: Sequence[str]) -> tuple[str, ...]:
    result = tuple(values)
    if (
        len(result) != _CW_COUNT
        or any(type(value) is not str or not value for value in result)
        or len(set(result)) != len(result)
    ):
        raise MethodError("cw_ids must be sixteen unique non-empty strings")
    return result


def _llr_for(codec: Any, samples: np.ndarray, noise: float) -> np.ndarray:
    llr = np.asarray(
        codec.demap(samples, complex_noise_power=noise), dtype=np.float64
    )
    if llr.size != _CW_COUNT * _CODED_BITS_PER_CW or not np.all(np.isfinite(llr)):
        raise MethodError("codec demapper must return 24,576 finite LLRs")
    return np.array(llr.reshape(_CW_COUNT, _CODED_BITS_PER_CW), copy=True)


@dataclass(frozen=True, slots=True)
class MethodResult:
    method_id: str
    decoded: Any
    selected_rotation_k: int
    candidate_scores: tuple[float, ...]
    receipt: Mapping[str, Any]


@dataclass(frozen=True, slots=True, init=False, weakref_slot=True)
class FrozenDeployableOutputs:
    b0: Any
    b1: Any
    deployment_seal: Any
    fixture_id: str
    fixture_identity: int

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        raise PermissionError(
            "FrozenDeployableOutputs construction is controlled by freeze_deployable_outputs()"
        )

    @property
    def is_frozen(self) -> bool:
        _authenticate_frozen_outputs(self)
        return True


@dataclass(frozen=True, slots=True, init=False, weakref_slot=True)
class ControlledFixture:
    samples: np.ndarray
    target_polarization: int
    boundary_after_data: int
    boundary_time: int
    rotation_k: int
    fixture_id: str

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        raise PermissionError(
            "ControlledFixture construction is controlled by inject_controlled_fixture()"
        )


@dataclass(frozen=True, slots=True)
class O1Result:
    method_id: str
    decoded: Any
    corrected_samples: np.ndarray
    evaluator_only: bool
    receipt: Mapping[str, Any]


_CONTROLLED_FIXTURE_ISSUANCE: dict[
    int, tuple[weakref.ReferenceType[ControlledFixture], tuple[Any, ...]]
] = {}
_FROZEN_OUTPUT_ISSUANCE: dict[
    int, tuple[weakref.ReferenceType[FrozenDeployableOutputs], tuple[Any, ...]]
] = {}


def _array_sha256(value: np.ndarray) -> str:
    array = np.ascontiguousarray(value)
    digest = hashlib.sha256()
    digest.update(array.dtype.str.encode("ascii"))
    digest.update(str(array.shape).encode("ascii"))
    digest.update(array.tobytes(order="C"))
    return digest.hexdigest()


def _fixture_fingerprint(fixture: ControlledFixture) -> tuple[Any, ...]:
    return (
        _array_sha256(fixture.samples),
        fixture.target_polarization,
        fixture.boundary_after_data,
        fixture.boundary_time,
        fixture.rotation_k,
        fixture.fixture_id,
    )


def _frozen_fingerprint(value: FrozenDeployableOutputs) -> tuple[Any, ...]:
    return (
        id(value.b0), id(value.b1), id(value.deployment_seal),
        value.fixture_id, value.fixture_identity,
    )


def _register_issued(registry: dict[int, Any], value: Any, fingerprint: tuple[Any, ...]) -> None:
    marker = id(value)

    def discard(reference: weakref.ReferenceType[Any], *, key: int = marker) -> None:
        current = registry.get(key)
        if current is not None and current[0] is reference:
            registry.pop(key, None)

    registry[marker] = (weakref.ref(value, discard), fingerprint)


def _authenticate_fixture(value: Any) -> ControlledFixture:
    if type(value) is not ControlledFixture:
        raise PermissionError("authenticated ControlledFixture required")
    issued = _CONTROLLED_FIXTURE_ISSUANCE.get(id(value))
    if issued is None or issued[0]() is not value:
        raise PermissionError("authenticated ControlledFixture required")
    if issued[1] != _fixture_fingerprint(value):
        raise PermissionError("tampered ControlledFixture rejected")
    return value


def _authenticate_frozen_outputs(value: Any) -> FrozenDeployableOutputs:
    if type(value) is not FrozenDeployableOutputs:
        raise PermissionError("authenticated frozen deployable outputs required")
    issued = _FROZEN_OUTPUT_ISSUANCE.get(id(value))
    if issued is None or issued[0]() is not value:
        raise PermissionError("authenticated frozen deployable outputs required")
    if issued[1] != _frozen_fingerprint(value):
        raise PermissionError("tampered frozen deployable outputs rejected")
    from verify import _authenticate_deployment_seal

    _authenticate_deployment_seal(value.deployment_seal)
    return value


def run_b0(
    codec: Any,
    data_symbols: np.ndarray,
    *,
    complex_noise_power: float,
    cw_ids: Sequence[str],
) -> MethodResult:
    """Decode the common-BPS output exactly once."""

    samples = _readonly(data_symbols, shape=(_DATA_SYMBOLS,))
    ids = _cw_ids(cw_ids)
    llr = _llr_for(codec, samples, complex_noise_power)
    decoded = codec.decode_fresh(llr, cw_ids=ids, candidate_id="B0")
    return MethodResult(
        method_id="COMMON_BPS_PLUS_ONE_LDPC",
        decoded=decoded,
        selected_rotation_k=0,
        candidate_scores=(),
        receipt=MappingProxyType(
            {"decoder_calls": 1, "whole_frame_rotation": 0, "truth_inputs": ()}
        ),
    )


def run_b1(
    codec: Any,
    data_symbols: np.ndarray,
    *,
    complex_noise_power: float,
    cw_ids: Sequence[str],
) -> MethodResult:
    """Decode all four whole-frame rotations and select normalized NLL."""

    samples = _readonly(data_symbols, shape=(_DATA_SYMBOLS,))
    ids = _cw_ids(cw_ids)
    decoded_candidates: list[Any] = []
    scores: list[float] = []
    for k in range(4):
        corrected = samples * np.exp(-0.5j * np.pi * k)
        llr = _llr_for(codec, corrected, complex_noise_power)
        decoded = codec.decode_fresh(llr, cw_ids=ids, candidate_id=f"B1_K{k}")
        coded_hat = codec.encode(decoded.info_bits)
        score = float(codec.reencode_nll(coded_hat, llr))
        if not math.isfinite(score):
            raise MethodError("B1 candidate NLL must be finite")
        decoded_candidates.append(decoded)
        scores.append(score)
    selected = min(range(4), key=lambda k: (scores[k], k))
    return MethodResult(
        method_id="GLOBAL_FOUR_ROTATION_DECODER_SELECTION",
        decoded=decoded_candidates[selected],
        selected_rotation_k=selected,
        candidate_scores=tuple(scores),
        receipt=MappingProxyType(
            {
                "candidate_rotations": (0, 1, 2, 3),
                "decoder_calls": 4,
                "message_state_reuse": False,
                "selection_score": "full_frame_normalized_reencode_nll",
                "tie_break": "lower_rotation_k",
                "truth_inputs": (),
            }
        ),
    )


def freeze_deployable_outputs(
    *, b0: Any, b1: Any, deployment_seal: Any, fixture: ControlledFixture
) -> FrozenDeployableOutputs:
    """Seal the two deployable diagnostic outputs before evaluator truth use."""

    if type(b0) is not MethodResult or b0.method_id != "COMMON_BPS_PLUS_ONE_LDPC":
        raise MethodError("b0 output has the wrong method identity")
    if (
        type(b1) is not MethodResult
        or b1.method_id != "GLOBAL_FOUR_ROTATION_DECODER_SELECTION"
    ):
        raise MethodError("b1 output has the wrong method identity")
    from verify import _authenticate_deployment_seal

    _authenticate_deployment_seal(deployment_seal)
    issued_fixture = _authenticate_fixture(fixture)
    frozen = object.__new__(FrozenDeployableOutputs)
    for name, value in {
        "b0": b0,
        "b1": b1,
        "deployment_seal": deployment_seal,
        "fixture_id": issued_fixture.fixture_id,
        "fixture_identity": id(issued_fixture),
    }.items():
        object.__setattr__(frozen, name, value)
    _register_issued(_FROZEN_OUTPUT_ISSUANCE, frozen, _frozen_fingerprint(frozen))
    _authenticate_frozen_outputs(frozen)
    return frozen


def inject_controlled_fixture(
    samples: np.ndarray,
    *,
    target_polarization: int,
    boundary_after_data: int,
    rotation_k: int,
    data_to_time: np.ndarray | None = None,
) -> ControlledFixture:
    """Copy and rotate one target suffix at the frozen common-CPR output."""

    value = np.asarray(samples)
    if value.ndim != 2 or value.shape[0] != 2 or value.shape[1] < _DATA_SYMBOLS:
        raise MethodError("controlled samples must have shape (2, >=6144)")
    frozen = _readonly(value)
    if type(target_polarization) is not int or target_polarization not in (0, 1):
        raise MethodError("target_polarization must be 0 or 1")
    if type(boundary_after_data) is not int or boundary_after_data not in _BOUNDARY_TO_ID:
        raise MethodError("boundary_after_data must be 1536, 3072, or 4608")
    if type(rotation_k) is not int or rotation_k not in (1, 2, 3):
        raise MethodError("controlled rotation_k must be 1, 2, or 3")
    if data_to_time is None:
        boundary_time = boundary_after_data
    else:
        mapping = np.asarray(data_to_time)
        if (
            mapping.shape != (_DATA_SYMBOLS,)
            or not np.issubdtype(mapping.dtype, np.integer)
            or np.any(np.diff(mapping) <= 0)
        ):
            raise MethodError("data_to_time must be a strict 6144-rank integer map")
        boundary_time = int(mapping[boundary_after_data])
    if boundary_time < 0 or boundary_time >= frozen.shape[1]:
        raise MethodError("controlled boundary time is outside the samples")
    injected = np.array(frozen, order="C", copy=True)
    injected[target_polarization, boundary_time:] *= np.exp(
        0.5j * np.pi * rotation_k
    )
    injected.setflags(write=False)
    fixture = object.__new__(ControlledFixture)
    for name, item in {
        "samples": injected,
        "target_polarization": target_polarization,
        "boundary_after_data": boundary_after_data,
        "boundary_time": boundary_time,
        "rotation_k": rotation_k,
        "fixture_id": f"{_BOUNDARY_TO_ID[boundary_after_data]}_K{rotation_k}",
    }.items():
        object.__setattr__(fixture, name, item)
    _register_issued(_CONTROLLED_FIXTURE_ISSUANCE, fixture, _fixture_fingerprint(fixture))
    _authenticate_fixture(fixture)
    return fixture


def evaluate_o1_inverse(
    codec: Any,
    fixture: ControlledFixture,
    *,
    frozen_outputs: FrozenDeployableOutputs,
    complex_noise_power: float,
    cw_ids: Sequence[str],
) -> O1Result:
    """Evaluator-only truth inverse, inaccessible before deployable freeze."""

    frozen_outputs = _authenticate_frozen_outputs(frozen_outputs)
    fixture = _authenticate_fixture(fixture)
    if (
        frozen_outputs.fixture_identity != id(fixture)
        or frozen_outputs.fixture_id != fixture.fixture_id
    ):
        raise PermissionError("frozen deployable outputs are not bound to this fixture")
    corrected = np.array(fixture.samples, order="C", copy=True)
    corrected[fixture.target_polarization, fixture.boundary_time:] *= np.exp(
        -0.5j * np.pi * fixture.rotation_k
    )
    corrected.setflags(write=False)
    ids = _cw_ids(cw_ids)
    llr = _llr_for(
        codec, corrected[fixture.target_polarization], complex_noise_power
    )
    decoded = codec.decode_fresh(llr, cw_ids=ids, candidate_id="O1")
    return O1Result(
        method_id="TRUTH_BOUNDARY_ROTATION_CORRECTION",
        decoded=decoded,
        corrected_samples=corrected,
        evaluator_only=True,
        receipt=MappingProxyType(
            {
                "fixture_id": fixture.fixture_id,
                "boundary_after_data": fixture.boundary_after_data,
                "rotation_k": fixture.rotation_k,
                "decoder_calls": 1,
                "truth_used_after_outputs_freeze": True,
            }
        ),
    )


__all__ = [
    "ControlledFixture",
    "FrozenDeployableOutputs",
    "MethodError",
    "MethodResult",
    "O1Result",
    "evaluate_o1_inverse",
    "freeze_deployable_outputs",
    "inject_controlled_fixture",
    "run_b0",
    "run_b1",
]
