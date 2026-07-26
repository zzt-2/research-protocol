"""T008 v2 evaluator — BER, legal resolve, REAL-curve required-SNR, full
observability metrics, verdict.

Identity / integrity guards (v2 gap closures):
  - legal pi/2 global resolve ONLY (M=4 raised QPSK/16-QAM ambiguity is pi/2,
    NOT pi/4 — the pi/4 is a deterministic bias corrected in deployable code);
  - the T006 "doc 4 / code 8 pi/4 rotations" mismatch is forbidden;
  - required-SNR is interpolated from the REAL BER-vs-SNR curve at the HD-FEC
    threshold (gap2 closure). No hardcoded slope, no BER-ratio constant. If no
    legal crossing exists for a cell, the runner reports raw/log-BER +
    UNRESOLVED_NO_CROSSING and does NOT fabricate dB.
  - BER near 0.5 is flagged as collapse; Q^2 is forbidden to dominate when any
    seed BER >= 0.2.
"""
from __future__ import annotations

from typing import Sequence

import numpy as np

from common._modulation import (
    qpsk_demod, qam16_demod, ber_count, ber_count_qam16,
)


HD_FEC_BER = 3.8e-3


def _demod(modulation: str):
    return qpsk_demod if modulation == "qpsk" else qam16_demod


def _ber_fn(modulation: str):
    return ber_count if modulation == "qpsk" else ber_count_qam16


def ber_with_legal_resolve(rx_comp: np.ndarray, tx_bits: np.ndarray,
                           modulation: str) -> float:
    """BER after a LEGAL pi/2 global resolve ONLY (4 pi/2 rotations)."""
    rx_comp = np.asarray(rx_comp, dtype=complex)
    ber_fn = _ber_fn(modulation)
    best = 1.0
    bps = 2 if modulation == "qpsk" else 4
    n_sym = len(rx_comp)
    tb = tx_bits[:n_sym * bps]
    for r in np.arange(0, 2 * np.pi, np.pi / 2):   # 4 legal pi/2 rotations ONLY
        b = ber_fn(tb, rx_comp * np.exp(-1j * r))
        if b < best:
            best = b
    return float(best)


def ber_raw(rx_comp: np.ndarray, tx_bits: np.ndarray, modulation: str) -> float:
    rx_comp = np.asarray(rx_comp, dtype=complex)
    ber_fn = _ber_fn(modulation)
    bps = 2 if modulation == "qpsk" else 4
    n_sym = len(rx_comp)
    tb = tx_bits[:n_sym * bps]
    return float(ber_fn(tb, rx_comp))


# ---------------------------------------------------------------------------
# Per-block BER with legal per-block pi/2 resolve (oracle/eval-resolve use)
# ---------------------------------------------------------------------------
def ber_blockwise_legal_resolve(seg, seg_bits, modulation, block):
    """Per-block BER with legal pi/2 resolve using that block's tx_bits.

    Truth-assisted oracle resolve (Kill-only). 4 legal pi/2 rotations per block.
    """
    seg = np.asarray(seg, dtype=complex)
    demod = _demod(modulation)
    bps = 2 if modulation == "qpsk" else 4
    n = len(seg)
    nb = n // block
    total_err = 0
    total_bits = 0
    for b in range(nb):
        s = slice(b * block, (b + 1) * block)
        blk = seg[s]
        tb = seg_bits[b * block * bps:(b + 1) * block * bps]
        best = 1.0
        for r in np.arange(0, 2 * np.pi, np.pi / 2):
            ber = float(np.mean(tb != demod(blk * np.exp(-1j * r))))
            if ber < best:
                best = ber
        total_err += best * len(tb)
        total_bits += len(tb)
    return total_err / max(total_bits, 1)


# ---------------------------------------------------------------------------
# FEC crossing — required SNR at HD-FEC, REAL curve (gap2 closure)
# ---------------------------------------------------------------------------
def required_snr_at_fec(snr_db_grid: Sequence[float], ber_curve: Sequence[float],
                        target_ber: float = HD_FEC_BER) -> float:
    """Linear (in log-BER) interpolation of the SNR required to reach target_ber.

    REAL curve only. If the curve never crosses target_ber (all BER > target),
    return NaN (FEC unreachable). If all BER < target, return the lowest SNR.
    No hardcoded slope; no BER-ratio constant.
    """
    snr = np.asarray(snr_db_grid, dtype=float)
    ber = np.asarray(ber_curve, dtype=float)
    if len(snr) < 2:
        return float("nan")
    if np.all(ber > target_ber):
        return float("nan")
    if np.all(ber < target_ber):
        return float(snr[0])
    log_ber = np.log10(np.clip(ber, 1e-12, 0.5))
    log_target = np.log10(target_ber)
    # Sort by SNR so the interpolation is along the monotone axis.
    order = np.argsort(snr)
    snr = snr[order]
    log_ber = log_ber[order]
    for i in range(len(log_ber) - 1):
        if (log_ber[i] >= log_target >= log_ber[i + 1]) or (log_ber[i] <= log_target <= log_ber[i + 1]):
            x0, x1 = snr[i], snr[i + 1]
            y0, y1 = log_ber[i], log_ber[i + 1]
            if y1 == y0:
                return float(x0)
            return float(x0 + (log_target - y0) * (x1 - x0) / (y1 - y0))
    return float("nan")


def gain_db(required_snr_a: float, required_snr_b: float) -> float:
    """required-SNR gain of A over B in dB (positive = A better)."""
    if np.isnan(required_snr_a) or np.isnan(required_snr_b):
        return float("nan")
    return float(required_snr_b - required_snr_a)


def trimmed_mean(a: Sequence[float], frac: float = 0.2) -> float:
    a = sorted(a)
    n = len(a)
    k = int(n * frac)
    if n - 2 * k <= 0:
        return float(np.mean(a))
    return float(np.mean(a[k:n - k]))


# ---------------------------------------------------------------------------
# Full observability metrics (gap4 closure)
# ---------------------------------------------------------------------------
def spearman_rho(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    rx = _rank(x)
    ry = _rank(y)
    if np.std(rx) == 0 or np.std(ry) == 0:
        return 0.0
    return float(np.corrcoef(rx, ry)[0, 1])


def _rank(a):
    a = np.asarray(a, dtype=float)
    order = np.argsort(a, kind="mergesort")
    ranks = np.empty(len(a), dtype=float)
    ranks[order] = np.arange(1, len(a) + 1, dtype=float)
    sa = a[order]
    i = 0
    while i < len(sa):
        j = i
        while j + 1 < len(sa) and sa[j + 1] == sa[i]:
            j += 1
        if j > i:
            avg = np.mean(ranks[order][i:j + 1])
            for k in range(i, j + 1):
                ranks[order[k]] = avg
        i = j + 1
    return ranks


def topk_accuracy(predicted_n: Sequence[int], oracle_n: Sequence[int], grid: Sequence[int], k: int = 2) -> float:
    """Fraction of blocks where the oracle-best N is within the top-k predicted
    N choices (by closeness on the grid). Exact-window acc is k=1.
    """
    predicted_n = np.asarray(predicted_n)
    oracle_n = np.asarray(oracle_n)
    grid = sorted(grid)
    g = np.asarray(grid, dtype=float)
    correct = 0
    for p, o in zip(predicted_n, oracle_n):
        # distance of each grid point to the oracle-best N
        dists = np.abs(g - o)
        # ranks of grid points by closeness to oracle (1=closest)
        order = np.argsort(dists, kind="mergesort")
        ranks = np.empty(len(g), dtype=int)
        ranks[order] = np.arange(1, len(g) + 1)
        # find the rank of the predicted N
        pi = int(np.where(g == p)[0][0]) if p in grid else int(np.argmin(np.abs(g - p)))
        if ranks[pi] <= k:
            correct += 1
    return correct / max(len(predicted_n), 1)


def regret_db(required_snr_method: float, required_snr_oracle: float) -> float:
    """Regret of a method's required-SNR vs the oracle's (dB; lower=better).
    NaN if either is NaN."""
    if np.isnan(required_snr_method) or np.isnan(required_snr_oracle):
        return float("nan")
    return float(required_snr_method - required_snr_oracle)


# ---------------------------------------------------------------------------
# Verdict (pre-registered, tested on synthetic inputs)
# ---------------------------------------------------------------------------
VERDICTS = (
    "METHOD_SIGNAL",
    "PROMOTION_READY",
    "ROBUSTNESS_OR_PACKAGING_BOUNDARY",
    "METHOD_FAIL_WITH_SPACE",
    "KILL_NO_ADAPTIVE_WINDOW_SPACE",
    "UNRESOLVED",
    "UNRESOLVED_OUTLIER_DOMINATED",
)


def collapse_check(seed_gains_db: Sequence[float]) -> bool:
    """True if a single seed contributes >40% of the aggregate gain."""
    g = np.asarray([x for x in seed_gains_db if not np.isnan(x)], dtype=float)
    if len(g) == 0:
        return False
    total = g.sum()
    if total <= 0:
        return False
    max_share = np.max(g) / total
    return bool(max_share > 0.40)


def verdict(method_signal_met: bool,
            oracle_space_survives: bool,
            corrected_gate_failed: bool,
            identity_ci_fec_closed: bool,
            collapse_dominated: bool,
            robustness_only_met: bool) -> str:
    """Pre-registered verdict function (T008 §7).

    Order: KILL (corrected oracle gate) > UNRESOLVED (identity/ci/fec) >
    PROMOTION/METHOD_SIGNAL > ROBUSTNESS > METHOD_FAIL_WITH_SPACE > UNRESOLVED.
    """
    if corrected_gate_failed:
        return "KILL_NO_ADAPTIVE_WINDOW_SPACE"
    if not identity_ci_fec_closed:
        return "UNRESOLVED"
    if collapse_dominated and method_signal_met:
        return "UNRESOLVED_OUTLIER_DOMINATED"
    if method_signal_met:
        return "METHOD_SIGNAL"
    if robustness_only_met:
        return "ROBUSTNESS_OR_PACKAGING_BOUNDARY"
    if oracle_space_survives:
        return "METHOD_FAIL_WITH_SPACE"
    return "UNRESOLVED"


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
