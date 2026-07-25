"""T007 evaluator — BER, legal resolve, FEC crossing, verdict.

Identity / integrity guards:
  - legal pi/2 global resolve ONLY (M=4 raised QPSK/16-QAM ambiguity is pi/2,
    NOT pi/4 — the pi/4 is a deterministic bias corrected in deployable code);
  - the T006 "doc 4 / code 8 pi/4 rotations" mismatch is forbidden;
  - BER near 0.5 is flagged as collapse; Q^2 is forbidden to dominate when any
    seed BER >= 0.2 (the metric must not be saved by a non-linear transform on
    near-random seeds).
"""
from __future__ import annotations

from typing import Sequence

import numpy as np

from common._modulation import (
    qpsk_demod, qam16_demod, ber_count, ber_count_qam16,
)


HD_FEC_BER = 3.8e-3


# ---------------------------------------------------------------------------
# BER with legal pi/2 global resolve ONLY
# ---------------------------------------------------------------------------
def _demod(modulation: str):
    return qpsk_demod if modulation == "qpsk" else qam16_demod


def _ber_fn(modulation: str):
    return ber_count if modulation == "qpsk" else ber_count_qam16


def ber_with_legal_resolve(rx_comp: np.ndarray, tx_bits: np.ndarray,
                           modulation: str) -> float:
    """BER after a LEGAL pi/2 global resolve ONLY.

    The M=4 raised QPSK/16-QAM ambiguity is pi/2 (4 spokes). The pi/4 bias is
    corrected in deployable code (cpe.PI4_BIAS), so the only remaining legal
    global ambiguity is pi/2. We try the 4 pi/2 rotations and take the minimum
    BER. This is the legal-resolve oral; the T006 8-pi/4-rotation mismatch is
    forbidden and tested.
    """
    rx_comp = np.asarray(rx_comp, dtype=complex)
    demod = _demod(modulation)
    ber_fn = _ber_fn(modulation)
    best = 1.0
    # Trim tx_bits to match rx_comp length (window truncation drops tail).
    bps = 2 if modulation == "qpsk" else 4
    n_sym = len(rx_comp)
    tb = tx_bits[:n_sym * bps]
    for r in np.arange(0, 2 * np.pi, np.pi / 2):   # 4 legal pi/2 rotations ONLY
        b = ber_fn(tb, rx_comp * np.exp(-1j * r))
        if b < best:
            best = b
    return float(best)


def ber_raw(rx_comp: np.ndarray, tx_bits: np.ndarray, modulation: str) -> float:
    """Raw BER (no resolve)."""
    rx_comp = np.asarray(rx_comp, dtype=complex)
    ber_fn = _ber_fn(modulation)
    bps = 2 if modulation == "qpsk" else 4
    n_sym = len(rx_comp)
    tb = tx_bits[:n_sym * bps]
    return float(ber_fn(tb, rx_comp))


# ---------------------------------------------------------------------------
# FEC crossing (required SNR at BER=HD_FEC_BER)
# ---------------------------------------------------------------------------
def required_snr_at_fec(snr_db_grid: Sequence[float], ber_curve: Sequence[float],
                        target_ber: float = HD_FEC_BER) -> float:
    """Linear interpolation of the SNR required to reach `target_ber`.

    If the curve never crosses target_ber (all BER > target), return NaN
    (FEC not reachable). If all BER < target, return the lowest SNR.
    """
    snr = np.asarray(snr_db_grid, dtype=float)
    ber = np.asarray(ber_curve, dtype=float)
    if np.all(ber > target_ber):
        return float("nan")
    if np.all(ber < target_ber):
        return float(snr[0])
    # log-BER interpolation is more stable near the waterfall.
    log_ber = np.log10(np.clip(ber, 1e-12, 0.5))
    log_target = np.log10(target_ber)
    # Find the bracket where ber crosses target from above.
    for i in range(len(log_ber) - 1):
        if log_ber[i] >= log_target >= log_ber[i + 1] or log_ber[i] <= log_target <= log_ber[i + 1]:
            x0, x1 = snr[i], snr[i + 1]
            y0, y1 = log_ber[i], log_ber[i + 1]
            if y1 == y0:
                return float(x0)
            return float(x0 + (log_target - y0) * (x1 - x0) / (y1 - y0))
    return float("nan")


def gain_db(required_snr_a: float, required_snr_b: float) -> float:
    """required-SNR gain of A over B in dB (positive = A is better)."""
    if np.isnan(required_snr_a) or np.isnan(required_snr_b):
        return float("nan")
    return float(required_snr_b - required_snr_a)


# ---------------------------------------------------------------------------
# Verdict function (pre-registered, tested on synthetic inputs)
# ---------------------------------------------------------------------------
VERDICTS = (
    "GO_ADAPTIVE_WINDOW_METHOD",
    "ROBUSTNESS_ONLY",
    "METHOD_FAIL_WITH_SPACE",
    "KILL_NO_ADAPTIVE_WINDOW_SPACE",
    "UNRESOLVED",
    "UNRESOLVED_OUTLIER_DOMINATED",
)


def collapse_check(seed_gains_db: Sequence[float]) -> bool:
    """Return True if a single seed contributes >40% of the aggregate gain."""
    g = np.asarray([x for x in seed_gains_db if not np.isnan(x)], dtype=float)
    if len(g) == 0:
        return False
    total = g.sum()
    if total <= 0:
        return False
    max_share = np.max(g) / total
    return bool(max_share > 0.40)


def verdict(structural_gate_passed: bool,
            go_conditions_met: bool,
            robustness_only_met: bool,
            oracle_space_exists: bool,
            identity_ci_fec_closed: bool,
            collapse_dominated: bool) -> str:
    """Pre-registered verdict function.

    Order matters: KILL (structural) > UNRESOLVED (outlier/identity) >
    GO > ROBUSTNESS_ONLY > METHOD_FAIL_WITH_SPACE.
    """
    if not structural_gate_passed:
        return "KILL_NO_ADAPTIVE_WINDOW_SPACE"
    if not identity_ci_fec_closed:
        return "UNRESOLVED"
    if collapse_dominated and go_conditions_met:
        return "UNRESOLVED_OUTLIER_DOMINATED"
    if go_conditions_met:
        return "GO_ADAPTIVE_WINDOW_METHOD"
    if robustness_only_met:
        return "ROBUSTNESS_ONLY"
    if oracle_space_exists:
        return "METHOD_FAIL_WITH_SPACE"
    return "UNRESOLVED"


# ---------------------------------------------------------------------------
# Bootstrap CI helper
# ---------------------------------------------------------------------------
def bootstrap_ci(seed_gains_db: Sequence[float], n_resample: int = 2000,
                 confidence: float = 0.95, rng_seed: int = 0) -> tuple:
    """Bootstrap CI on the mean of per-seed gains (dB). Returns (mean, lo, hi)."""
    g = np.asarray([x for x in seed_gains_db if not np.isnan(x)], dtype=float)
    if len(g) < 2:
        m = float(np.mean(g)) if len(g) == 1 else float("nan")
        return (m, float("nan"), float("nan"))
    rng = np.random.default_rng(rng_seed)
    boots = np.array([np.mean(rng.choice(g, size=len(g), replace=True))
                      for _ in range(n_resample)])
    alpha = (1.0 - confidence) / 2.0
    lo = float(np.quantile(boots, alpha))
    hi = float(np.quantile(boots, 1.0 - alpha))
    return (float(np.mean(g)), lo, hi)
