"""Source-native fixed-lambda B10 pilot-RLS estimator.

RLS recursion follows Deka et al. 2024 p.166 Eq.(3)-(6). The 128-pilot
training, periodic regressor, and DD residual update follow p.166-167
Eq.(7)-(8) and Fig.1. T010 uses radians throughout, hence F=2*pi/h1,128.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from common._modulation import hard_decision


PACKAGE_DIR = Path(__file__).resolve().parent
PILOT_COUNT = 128


def _pilot_symbols() -> np.ndarray:
    raw = json.loads((PACKAGE_DIR / "pilot-manifest.json").read_text(encoding="utf-8"))
    return np.asarray([complex(real, imag) for real, imag in raw["symbols"]])


def _update(h: np.ndarray, p: np.ndarray, x: np.ndarray, y: float, lam: float):
    # Deka et al. 2024 p.166 Eq.(3)-(6).
    error = float(y - np.dot(h, x))
    px = p @ x
    gain = px / (lam + np.dot(x, px))
    h_new = h + gain * error
    p_new = (p - np.outer(gain, x) @ p) / lam
    return h_new, p_new, error


def operational_residual(derotated: complex, decision: complex) -> float:
    """Return the residual under T010 D019's positive-phase convention.

    B10 Eq.(8)'s literal text has a sign tension with Eq.(1) and negative
    derotation. D019/V008 adjudicates the operational residual as
    angle(derotated * conj(decision)).
    """
    return float(np.angle(derotated * np.conj(decision)))


def run_source_native_rls(
    rx: np.ndarray,
    *,
    forgetting_factor: float,
    symbol_rate: float = 28e9,
) -> dict:
    """Run 128 known manifest pilots, freeze F once, then strict DD."""
    rx = np.asarray(rx, dtype=complex)
    if len(rx) <= PILOT_COUNT:
        raise ValueError("rx must contain data after 128 pilots")
    if not 0.0 < forgetting_factor <= 1.0:
        raise ValueError("forgetting_factor must lie in (0,1]")
    pilots = _pilot_symbols()
    observed = np.unwrap(np.angle(rx[:PILOT_COUNT] / pilots))
    h = np.zeros(2, dtype=float)
    p = np.eye(2, dtype=float) * 0.5  # delta=2 -> P0=delta^-1 I
    corrected = np.empty_like(rx)
    errors = []

    for index in range(PILOT_COUNT):
        k = float(index + 1)
        x = np.asarray([1.0, k])
        h, p, error = _update(h, p, x, float(observed[index]), forgetting_factor)
        errors.append(error)
        corrected[index] = rx[index] * np.exp(-1j * np.dot(h, x))

    slope = float(h[1])
    if not np.isfinite(slope) or slope <= 0.0:
        raise ValueError("source-native identity requires finite positive CFO slope")
    period = 2.0 * np.pi / slope
    frozen_period = period
    estimates = np.empty(len(rx), dtype=float)
    estimates[:PILOT_COUNT] = observed

    for index in range(PILOT_COUNT, len(rx)):
        k = float(index + 1)
        x = np.asarray([1.0, np.mod(k, frozen_period)])
        predicted = float(np.dot(h, x))
        derotated = rx[index] * np.exp(-1j * predicted)
        decided = hard_decision(derotated, mod="qam16")
        residual = operational_residual(derotated, decided)
        desired = predicted + residual
        corrected[index] = derotated
        estimates[index] = predicted
        h, p, error = _update(h, p, x, desired, forgetting_factor)
        errors.append(error)

    state_finite = bool(
        np.all(np.isfinite(h))
        and np.all(np.isfinite(p))
        and np.all(np.isfinite(corrected))
    )
    return {
        "corrected": corrected,
        "phase_estimate": estimates,
        "h_final": h,
        "p_final": p,
        "h_initial": [0.0, 0.0],
        "p_initial": [[0.5, 0.0], [0.0, 0.5]],
        "delta": 2.0,
        "units": "radians",
        "training_symbols": PILOT_COUNT,
        "switch_index_zero_based": PILOT_COUNT,
        "period": frozen_period,
        "period_freeze_count": 1,
        "training_slope": slope,
        "estimated_cfo_hz": slope * symbol_rate / (2.0 * np.pi),
        "state_finite": state_finite,
        "update_count": len(rx),
        "errors": np.asarray(errors),
    }
