"""Truth-free scalar receiver front-end for the frozen D0 testbed.

Only receiver-visible samples and registered pilots enter this module.  The
common BPS implementation is wrapped without changing its numerical kernel.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from types import MappingProxyType
from typing import Any, Mapping

import numpy as np

from common._recovery import bps_cpr


class ReceiverError(ValueError):
    """Raised when a frozen scalar-receiver contract is violated."""


def _complex_vector(value: Any, name: str, *, minimum: int = 1) -> np.ndarray:
    array = np.asarray(value)
    if array.ndim != 1 or array.size < minimum:
        raise ReceiverError(f"{name} must be a one-dimensional complex vector")
    if not np.iscomplexobj(array) or not np.all(np.isfinite(array)):
        raise ReceiverError(f"{name} must contain finite complex samples")
    return np.asarray(array, dtype=np.complex128)


def _nonnegative_finite(value: Any, name: str) -> float:
    if isinstance(value, (bool, np.bool_)):
        raise TypeError(f"{name} must be a finite non-negative number")
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise TypeError(f"{name} must be a finite non-negative number") from exc
    if not math.isfinite(result) or result < 0.0:
        raise ReceiverError(f"{name} must be a finite non-negative number")
    return result


def _readonly(value: np.ndarray) -> np.ndarray:
    result = np.array(value, order="C", copy=True)
    result.setflags(write=False)
    return result


@dataclass(frozen=True, slots=True)
class PrefixCalibration:
    gain: complex
    c_pre_cplx: float
    receipt: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class BPSResult:
    samples: np.ndarray
    phase_trace: np.ndarray
    receipt: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class SymmetryResolution:
    samples: np.ndarray
    state: int
    receipt: Mapping[str, Any]


def estimate_prefix_calibration(
    received_prefix: np.ndarray, known_prefix: np.ndarray
) -> PrefixCalibration:
    """Fit one complex gain and estimate complex residual power as RSS/31."""
    received = _complex_vector(received_prefix, "received_prefix", minimum=32)
    known = _complex_vector(known_prefix, "known_prefix", minimum=32)
    if received.shape != (32,) or known.shape != (32,):
        raise ReceiverError("prefix calibration requires exactly 32 samples")
    energy = float(np.sum(np.abs(known) ** 2))
    if not math.isfinite(energy) or energy <= 0.0:
        raise ReceiverError("known_prefix must have positive finite energy")
    gain = complex(np.sum(np.conj(known) * received) / energy)
    residual = received - gain * known
    rss = float(np.sum(np.abs(residual) ** 2))
    c_pre = rss / 31.0
    return PrefixCalibration(
        gain=gain,
        c_pre_cplx=c_pre,
        receipt=MappingProxyType(
            {
                "estimator_id": "known_prefix_ls_rss_over_31_v1",
                "parameters": 1,
                "samples": 32,
                "residual_dof": 31,
            }
        ),
    )


def scalar_visible_power_equalize(
    samples: np.ndarray,
    *,
    c_pre_cplx: float,
    block_symbols: int = 100,
    amplitude_limit: float = 3.0,
) -> tuple[np.ndarray, Mapping[str, Any]]:
    """Equalize one polarization from observed block power only."""
    received = _complex_vector(samples, "samples")
    noise = _nonnegative_finite(c_pre_cplx, "c_pre_cplx")
    if isinstance(block_symbols, (bool, np.bool_)) or not isinstance(
        block_symbols, (int, np.integer)
    ) or int(block_symbols) != 100:
        raise ReceiverError("block_symbols must equal the frozen value 100")
    limit = _nonnegative_finite(amplitude_limit, "amplitude_limit")
    if limit != 3.0:
        raise ReceiverError("amplitude_limit must equal the frozen value 3.0")

    output = np.empty_like(received)
    visible_powers: list[float] = []
    for start in range(0, received.size, 100):
        block = received[start : start + 100]
        observed = float(np.mean(np.abs(block) ** 2))
        visible = max(observed - noise, 0.0)
        visible_powers.append(visible)
        denominator = visible + noise
        scale = math.sqrt(visible) / denominator if denominator > 0.0 else 0.0
        equalized = block * scale
        amplitudes = np.abs(equalized)
        clipped = amplitudes > limit
        if np.any(clipped):
            equalized = equalized.copy()
            equalized[clipped] *= limit / amplitudes[clipped]
        output[start : start + block.size] = equalized
    receipt = MappingProxyType(
        {
            "equalizer_id": "scalar_visible_power_mmse_v1",
            "block_symbols": 100,
            "amplitude_limit": 3.0,
            "visible_signal_power_per_block": tuple(visible_powers),
            "noiseless_branch": noise == 0.0,
            "truth_inputs": (),
        }
    )
    return _readonly(output), receipt


def run_common_bps(samples: np.ndarray, *, B: int, Nw: int) -> BPSResult:
    """Validate the frozen six-cell grid and call common square-16QAM BPS."""
    value = _complex_vector(samples, "samples")
    if isinstance(B, (bool, np.bool_)) or not isinstance(B, (int, np.integer)):
        raise TypeError("B must be an integer")
    if isinstance(Nw, (bool, np.bool_)) or not isinstance(Nw, (int, np.integer)):
        raise TypeError("Nw must be an integer")
    B, Nw = int(B), int(Nw)
    if B not in (32, 64) or Nw not in (31, 61, 127):
        raise ReceiverError("B/Nw must belong to the frozen six-cell BPS grid")
    corrected, phase = bps_cpr(value, B=B, Nw=Nw, mod="qam16")
    return BPSResult(
        samples=_readonly(corrected),
        phase_trace=_readonly(np.asarray(phase, dtype=np.float64)),
        receipt=MappingProxyType(
            {
                "implementation": "common._recovery.bps_cpr",
                "modulation": "qam16",
                "B": B,
                "Nw": Nw,
                "edge_rule": "numpy_convolve_same_zero_padding_full_Nw_denominator",
            }
        ),
    )


def resolve_global_symmetry(
    samples: np.ndarray, known_prefix: np.ndarray
) -> SymmetryResolution:
    """Resolve only the four legal pi/2 states from even prefix positions."""
    value = _complex_vector(samples, "samples", minimum=32)
    known = _complex_vector(known_prefix, "known_prefix", minimum=32)
    if known.shape != (32,):
        raise ReceiverError("known_prefix must contain exactly 32 samples")
    indices = np.arange(0, 32, 2)
    objectives = tuple(
        float(
            np.sum(
                np.abs(
                    value[indices] * np.exp(-0.5j * np.pi * state)
                    - known[indices]
                )
                ** 2
            )
        )
        for state in range(4)
    )
    state = int(np.argmin(objectives))
    resolved = value * np.exp(-0.5j * np.pi * state)
    return SymmetryResolution(
        samples=_readonly(resolved),
        state=state,
        receipt=MappingProxyType(
            {
                "candidate_states": (0, 1, 2, 3),
                "selection_indices": tuple(int(index) for index in indices),
                "tie_break": "lower_state",
                "objective_values": objectives,
            }
        ),
    )


def estimate_post_bps_residual(
    resolved_samples: np.ndarray, known_prefix: np.ndarray
) -> float:
    """Estimate C_post from odd prefix positions; this value is output-only."""
    resolved = _complex_vector(resolved_samples, "resolved_samples", minimum=32)
    known = _complex_vector(known_prefix, "known_prefix", minimum=32)
    if known.shape != (32,):
        raise ReceiverError("known_prefix must contain exactly 32 samples")
    odd = np.arange(1, 32, 2)
    return float(np.mean(np.abs(resolved[odd] - known[odd]) ** 2))


__all__ = [
    "BPSResult",
    "PrefixCalibration",
    "ReceiverError",
    "SymmetryResolution",
    "estimate_post_bps_residual",
    "estimate_prefix_calibration",
    "resolve_global_symmetry",
    "run_common_bps",
    "scalar_visible_power_equalize",
]
