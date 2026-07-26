"""Isolated, deployable primitives for T009 A4-v2.

The deployable path never accepts transmitter bits, true channel/SNR labels, or
future-block inputs.  Evaluator-only truth remains outside this module.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np


SIM_ROOT = Path(__file__).parents[2]
if str(SIM_ROOT) not in sys.path:
    sys.path.insert(0, str(SIM_ROOT))

from common._modulation import (  # noqa: E402
    _M16APSK_SYM,
    m16apsk_demod,
    m16apsk_mod,
)


def m16apsk_constellation() -> np.ndarray:
    return _M16APSK_SYM.copy()


def hard_decision_m16apsk(z):
    z = np.asarray(z, dtype=complex)
    flat = z.reshape(-1)
    idx = np.argmin(np.abs(flat[:, None] - _M16APSK_SYM[None, :]) ** 2, axis=1)
    out = _M16APSK_SYM[idx].reshape(z.shape)
    return complex(out) if out.ndim == 0 else out


def resolve_ambiguity_from_pilots(
    rx: np.ndarray,
    pilot_idx: np.ndarray,
    pilot_symbols: np.ndarray,
    *,
    m0: int = 8,
):
    """Resolve the M0-fold ambiguity from known receiver pilots only."""
    rx = np.asarray(rx, dtype=complex)
    pilot_idx = np.asarray(pilot_idx, dtype=int)
    pilot_symbols = np.asarray(pilot_symbols, dtype=complex)
    if pilot_idx.size == 0 or pilot_idx.size != pilot_symbols.size:
        raise ValueError("non-empty aligned pilot observations are required")
    scores = []
    for branch in range(m0):
        rot = branch * 2 * np.pi / m0
        residual = rx[pilot_idx] * np.exp(-1j * rot) - pilot_symbols
        scores.append(float(np.mean(np.abs(residual) ** 2)))
    best = int(np.argmin(scores))
    return rx * np.exp(-1j * best * 2 * np.pi / m0), best


class Dpll16Apsk:
    """Second-order DD loop whose VCO state persists across process() calls."""

    def __init__(self, *, omega_n: float, symbol_period: float, zeta=np.sqrt(2) / 2):
        w_t = min(float(omega_n) * float(symbol_period), 0.5)
        self.c1 = 2 * float(zeta) * w_t
        self.c2 = w_t**2
        self.integrator = 0.0
        self.vco_phase = 0.0

    def process(self, rx):
        rx = np.asarray(rx, dtype=complex)
        out = np.empty_like(rx)
        for k, sample in enumerate(rx):
            rotated = sample * np.exp(-1j * self.vco_phase)
            decision = hard_decision_m16apsk(rotated)
            error = np.angle(rotated * np.conj(decision))
            self.integrator += self.c2 * error
            self.vco_phase += self.c1 * error + self.integrator
            out[k] = sample * np.exp(-1j * self.vco_phase)
        return out


class FrozenSelectors:
    def __init__(
        self,
        *,
        power_threshold,
        innovation_threshold,
        bins,
        bin_actions,
        confidence_margin,
        global_best,
    ):
        self.power_threshold = float(power_threshold)
        self.innovation_threshold = float(innovation_threshold)
        self.bins = tuple(float(x) for x in bins)
        self.bin_actions = tuple(bin_actions)
        self.confidence_margin = float(confidence_margin)
        self.global_best = global_best

    def p1(self, history, current, **_ignored):
        return (
            "NDA"
            if current["power"] >= self.power_threshold
            and current["innovation"] <= self.innovation_threshold
            else "DA"
        )

    def p2(self, history, current, **_ignored):
        index = int(np.searchsorted(self.bins, current["power"], side="right"))
        return self.bin_actions[index]

    def p3(self, history, current, **_ignored):
        distance = min(abs(current["power"] - edge) for edge in self.bins)
        if distance < self.confidence_margin:
            return self.global_best
        return self.p2(history, current)


def required_snr_db(snr_db, ber, *, target):
    """Log-BER interpolation; never fabricates a dB value without a crossing."""
    x = np.asarray(snr_db, dtype=float)
    y = np.asarray(ber, dtype=float)
    for i in range(len(x) - 1):
        if (y[i] - target) * (y[i + 1] - target) <= 0 and y[i] != y[i + 1]:
            log_y = np.log10(y[i : i + 2])
            return float(np.interp(np.log10(target), log_y[::-1], x[i : i + 2][::-1]))
    return "UNRESOLVED_NO_CROSSING"


__all__ = [
    "Dpll16Apsk",
    "FrozenSelectors",
    "hard_decision_m16apsk",
    "m16apsk_constellation",
    "m16apsk_demod",
    "m16apsk_mod",
    "required_snr_db",
    "resolve_ambiguity_from_pilots",
]
