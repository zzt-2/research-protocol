"""T007 CPE core — fixed-window and adaptive-window phase estimators.

Two block-buffered CPE families, both receiver-visible (no truth in the
signature):

  - vv_block_mean(rx, N, modulation): block-mean Viterbi-Viterbi. Raises rx
    to M=4 (QPSK/16-QAM square constellation), averages over N symbols, takes
    the angle, divides by 4. The deterministic pi/4 fourth-power bias is
    corrected here (deployable). The remaining pi/2 global ambiguity is left
    to the evaluator's legal global resolve.
  - pilot_block_mean(rx, pilot_mask, pilot_symbols, N): pilot moving-average
    CPE over N pilot phases, equal overhead charged by the runner.

Adaptive controllers (P1/P2/P3) pick N per block from the shared window grid
{8,16,32,64,128,256} using receiver-visible features only.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional, Sequence

import numpy as np

from channel import estimate_phase_innovation_hat, estimate_snr_hat


WINDOW_GRID = (8, 16, 32, 64, 128, 256)
M0 = 4   # QPSK/16-QAM square constellation raised-power order


# ---------------------------------------------------------------------------
# Modulation-dependent deterministic fourth-power bias
# ---------------------------------------------------------------------------
# The M=4 raised-power Viterbi-Viterbi CPE has a DETERMINISTIC bias =
# angle(E[constellation^4]) / M0 that depends on the constellation. For QPSK
# the raised points are colinear at angle pi (bias = pi/4 = 45 deg, |E[s^4]|=1,
# clean). For 16-QAM the raised points are SPREAD (|E[s^4]|≈0) so the V&V
# estimate is noisy AND the bias is the angle of the (small) mean vector.
# Deployable code MUST correct this deterministic, constellation-known bias
# (the constellation is receiver-known, so this is receiver-visible). The
# remaining legal ambiguity is pi/2 (evaluator's legal global resolve only);
# the T006 "doc 4 / code 8 pi/4" mismatch is forbidden and tested.
#
# PI4_BIAS is kept as the QPSK value for backwards-compat naming; the actual
# deployable bias is computed by raised_power_bias(modulation) below.
PI4_BIAS = np.pi / 4.0   # QPSK deterministic fourth-power bias


def raised_power_bias(modulation: str) -> float:
    """Deterministic fourth-power bias = angle(E[constellation^4]) / M0.

    Receiver-visible (the constellation is known at the receiver). QPSK: pi/4.
    16-QAM: angle of the small raised-mean vector (V&V is approximate for QAM,
    this is the honest correction; the residual noise is irreducible V&V error
    for non-PSK constellations).
    """
    if modulation == "qpsk":
        return PI4_BIAS
    if modulation == "qam16":
        # E[constellation^4] for the canonical 16-QAM (Gray map, /sqrt(10)).
        from common._modulation import _M16APSK_SYM_BY_LABEL  # canonical
        # Use the standard square 16-QAM constellation directly.
        pts = np.array([(di + 1j * dq) / np.sqrt(10)
                        for di in (-3, -1, 1, 3) for dq in (-3, -1, 1, 3)])
        raised = pts ** M0
        m = raised.mean()
        if np.abs(m) < 1e-9:
            # Raised mean cancels (|E[s^4]|=0); bias is undefined, use 0 and
            # rely on legal pi/2 resolve. V&V is approximate for 16-QAM.
            return 0.0
        return float(np.angle(m) / M0)
    raise ValueError(f"modulation must be 'qpsk' or 'qam16', got {modulation!r}")


def vv_block_mean(rx: np.ndarray, N: int, modulation: str = "qpsk") -> np.ndarray:
    """Block-mean Viterbi-Viterbi CPE.

    Raises rx to M0=4, averages each contiguous block of N symbols, takes the
    angle, divides by M0, subtracts the modulation-dependent deterministic
    bias (raised_power_bias), and returns the per-symbol phase-compensated RX
    (block-buffered, causal, block latency 0 — reads only the current block).

    Parameters
    ----------
    rx : complex ndarray, the receiver-visible RX.
    N : int, the phase-estimation window length (symbols averaged per block).
    modulation : {'qpsk','qam16'}, the known constellation (receiver-visible).
        Bias correction is constellation-dependent; the remaining ambiguity is
        legal pi/2 global resolve only (evaluator).

    Returns
    -------
    rx_comp : complex ndarray, the per-symbol phase-compensated RX (same length
        as rx; the last partial block is dropped if it is shorter than N).
    """
    rx = np.asarray(rx, dtype=complex)
    bias = raised_power_bias(modulation)
    n = len(rx)
    nb = n // N
    L = nb * N
    rx_comp = np.zeros(L, dtype=complex)
    for k in range(nb):
        lo, hi = k * N, (k + 1) * N
        block = rx[lo:hi]
        raised = block ** M0
        # Guard against overflow on large amplitudes (matches common/vv_cpr).
        amp = np.abs(raised)
        if np.any(amp > 1e8):
            raised = raised / np.maximum(amp, 1e-12) * 1e8
        phi_raised = np.angle(raised.mean())
        phi_est = phi_raised / M0 - bias
        rx_comp[lo:hi] = block * np.exp(-1j * phi_est)
    return rx_comp


def pilot_block_mean(rx: np.ndarray, pilot_mask: np.ndarray,
                     pilot_symbols: np.ndarray, N: int) -> np.ndarray:
    """Pilot moving-average CPE over N pilot symbols.

    Collects the per-pilot phase estimate angle(rx[pilot]/pilot_sym) over the
    most recent N pilots (block-buffered, causal) and applies the averaged
    phase to the data symbols in the same block region. Equal pilot overhead
    is charged by the runner; this estimator does NOT read the oracle.
    """
    rx = np.asarray(rx, dtype=complex)
    pilot_idx = np.where(pilot_mask)[0]
    n_pilots = len(pilot_idx)
    if n_pilots == 0:
        return rx.copy()
    # Per-pilot phase estimate (no unwrap — pilot phases are well-separated).
    pilot_phase = np.angle(rx[pilot_idx] / pilot_symbols)
    rx_comp = rx.copy()
    # Block-buffered over groups of N pilots; apply the block pilot-phase mean
    # to all symbols in the span covered by that pilot group.
    n_blocks = n_pilots // N
    for k in range(n_blocks):
        lo_p, hi_p = k * N, (k + 1) * N
        phi_est = pilot_phase[lo_p:hi_p].mean()
        sym_lo = pilot_idx[lo_p]
        sym_hi = pilot_idx[hi_p - 1] + 1 if hi_p - 1 < n_pilots else len(rx)
        rx_comp[sym_lo:sym_hi] = rx[sym_lo:sym_hi] * np.exp(-1j * phi_est)
    # The partial trailing pilot group is dropped (matches fixed-window L
    # truncation, fair across arms).
    last_sym = pilot_idx[n_blocks * N - 1] + 1 if n_blocks * N >= 1 else 0
    rx_comp = rx_comp[:last_sym]
    return rx_comp


# ---------------------------------------------------------------------------
# Adaptive window controllers (P1 / P2 / P3) — receiver-visible only
# ---------------------------------------------------------------------------
@dataclass
class AdaptiveResult:
    """Output of an adaptive controller.

    `n_per_block` is the per-block window choice (for diagnostics / chatter);
    `rx_comp` is the per-symbol phase-compensated RX. The deployable signature
    exposes only rx + receiver-visible features; the truth never enters.
    """
    n_per_block: np.ndarray
    rx_comp: np.ndarray
    method: str


def _blocks_and_features(rx: np.ndarray, block: int):
    """Split rx into blocks and compute receiver-visible features per block."""
    rx = np.asarray(rx, dtype=complex)
    n = len(rx)
    nb = n // block
    L = nb * block
    rx_trim = rx[:L]
    snr_hat = estimate_snr_hat(rx_trim, window=block)
    innov_hat = estimate_phase_innovation_hat(rx_trim, m0=M0, window=block)
    return rx_trim, nb, block, snr_hat, innov_hat


def adaptive_window_apply(rx: np.ndarray, n_per_block: np.ndarray,
                          block: int, modulation: str = "qpsk") -> np.ndarray:
    """Apply a per-block window choice to the RX (block-buffered, causal).

    The block length `block` is the unit of adaptation; within each block the
    window choice N (from WINDOW_GRID) is the VV averaging length. We average
    the raised RX over the FULL block when block>=N, or over N consecutive
    mini-blocks when block<N, always reading only the current block. The
    modulation-dependent deterministic bias is subtracted.
    """
    rx = np.asarray(rx, dtype=complex)
    bias = raised_power_bias(modulation)
    nb = len(n_per_block)
    L = nb * block
    rx_comp = np.zeros(L, dtype=complex)
    for k in range(nb):
        lo, hi = k * block, (k + 1) * block
        block_rx = rx[lo:hi]
        N = int(n_per_block[k])
        if N >= block:
            # Average the whole block (single mini-block).
            raised = block_rx ** M0
            amp = np.abs(raised)
            if np.any(amp > 1e8):
                raised = raised / np.maximum(amp, 1e-12) * 1e8
            phi_raised = np.angle(raised.mean())
            phi_est = phi_raised / M0 - bias
            rx_comp[lo:hi] = block_rx * np.exp(-1j * phi_est)
        else:
            # Split the block into mini-blocks of length N (causal, no future).
            n_mini = block // N
            for j in range(n_mini):
                mlo = lo + j * N
                mhi = mlo + N
                mini = block_rx[j * N:(j + 1) * N]
                raised = mini ** M0
                amp = np.abs(raised)
                if np.any(amp > 1e8):
                    raised = raised / np.maximum(amp, 1e-12) * 1e8
                phi_raised = np.angle(raised.mean())
                phi_est = phi_raised / M0 - bias
                rx_comp[mlo:mhi] = mini * np.exp(-1j * phi_est)
    return rx_comp


def p1_analytic_ratio_rule(rx: np.ndarray, block: int,
                           snr_lo_db: float, snr_hi_db: float,
                           innov_lo: float, innov_hi: float,
                           modulation: str = "qpsk",
                           innov_weight: float = 0.5) -> AdaptiveResult:
    """P1 — analytic ratio rule.

    Maps receiver-visible (SNR_hat, phase_innovation_hat) to N via a monotone
    rule with hard bounds, following E1 (SNR down -> N up) and E2 (linewidth
    up -> innov up -> N down). Reads NO oracle / NO truth.

    The mapping is a clipped monotone interpolation: when SNR_hat is low AND
    innovation is low, N is large; when innovation is high, N is small. The
    `innov_weight` blends the two features (default 0.5; the structural gate
    tests whether innov_hat is informative at all — D-011/A1 found raised-power
    phase increments are noise-dominated, so this is an empirical question).
    """
    rx_trim, nb, _, snr_hat, innov_hat = _blocks_and_features(rx, block)
    # Normalize SNR_hat to [0,1] within [snr_lo, snr_hi] (clipped).
    snr_norm = np.clip((snr_hat - snr_lo_db) / max(snr_hi_db - snr_lo_db, 1e-12), 0.0, 1.0)
    # Normalize innovation to [0,1] within [innov_lo, innov_hi] (clipped).
    innov_norm = np.clip((innov_hat - innov_lo) / max(innov_hi - innov_lo, 1e-12), 0.0, 1.0)
    # Combined "want-large-N" score: high SNR (less noise) wants SMALLER N, low
    # SNR wants LARGER N; high innovation wants SMALLER N. So large-N score is
    # (1 - snr_norm) AND (1 - innov_norm), blended.
    w = float(innov_weight)
    large_n_score = (1.0 - w) * (1.0 - snr_norm) + w * (1.0 - innov_norm)
    # Map [0,1] to the window grid index (0 = smallest N, 5 = largest N).
    idx = np.clip(np.round(large_n_score * (len(WINDOW_GRID) - 1)).astype(int),
                  0, len(WINDOW_GRID) - 1)
    n_per_block = np.array(WINDOW_GRID)[idx]
    rx_comp = adaptive_window_apply(rx_trim, n_per_block, block, modulation)
    return AdaptiveResult(n_per_block=n_per_block, rx_comp=rx_comp, method="p1_analytic_ratio")


def p2_lookup_hysteresis(rx: np.ndarray, block: int,
                         lookup_table: dict,
                         hysteresis_band: float,
                         initial_n: int = 32,
                         modulation: str = "qpsk") -> AdaptiveResult:
    """P2 — validation lookup table on (SNR_hat, phase_innovation_hat) + hysteresis.

    `lookup_table` is a dict keyed by (snr_bin, innov_bin) -> N, learned on
    validation. Across blocks, N only switches when the (snr_bin, innov_bin)
    crosses a hysteresis band by more than `hysteresis_band`. This suppresses
    window chatter. Reads NO oracle / NO truth.
    """
    rx_trim, nb, _, snr_hat, innov_hat = _blocks_and_features(rx, block)
    # Bin the features using the table's bin edges.
    snr_edges = lookup_table["snr_edges"]
    innov_edges = lookup_table["innov_edges"]
    table = np.asarray(lookup_table["table"])  # shape (n_snr_bins, n_innov_bins)
    n_per_block = np.zeros(nb, dtype=int)
    cur_n = int(initial_n)
    cur_snr_bin = None
    cur_innov_bin = None
    for k in range(nb):
        si = int(np.searchsorted(snr_edges, snr_hat[k], side="right") - 1)
        ii = int(np.searchsorted(innov_edges, innov_hat[k], side="right") - 1)
        si = int(np.clip(si, 0, table.shape[0] - 1))
        ii = int(np.clip(ii, 0, table.shape[1] - 1))
        target_n = int(table[si, ii])
        # Hysteresis: switch only if the bin changed by more than the band in
        # EITHER feature (relative to the last committed bin).
        if cur_snr_bin is None:
            commit = True
        else:
            d_snr = abs(si - cur_snr_bin)
            d_innov = abs(ii - cur_innov_bin)
            commit = (d_snr + d_innov) > hysteresis_band
        if commit:
            cur_n = target_n
            cur_snr_bin = si
            cur_innov_bin = ii
        n_per_block[k] = cur_n
    rx_comp = adaptive_window_apply(rx_trim, n_per_block, block, modulation)
    return AdaptiveResult(n_per_block=n_per_block, rx_comp=rx_comp, method="p2_lookup_hysteresis")


def p3_confidence_safe(rx: np.ndarray, block: int,
                       regret_table: dict,
                       confidence_threshold: float,
                       bstar_n: int,
                       modulation: str = "qpsk") -> AdaptiveResult:
    """P3 — validation-learned per-window regret/confidence -> N; fallback to B*.

    `regret_table` maps (snr_bin, innov_bin) -> {N: regret} learned on
    validation. For the current block, pick the N with the lowest regret IF
    its confidence (1 - regret-gap-to-second-best, normalized) exceeds the
    threshold; otherwise fall back to the frozen B* window. NO test labels,
    NO oracle best N. Model family is a frozen shallow table only.
    """
    rx_trim, nb, _, snr_hat, innov_hat = _blocks_and_features(rx, block)
    snr_edges = regret_table["snr_edges"]
    innov_edges = regret_table["innov_edges"]
    regret = np.asarray(regret_table["regret"])  # shape (n_snr_bins, n_innov_bins, len(WINDOW_GRID))
    n_per_block = np.zeros(nb, dtype=int)
    for k in range(nb):
        si = int(np.searchsorted(snr_edges, snr_hat[k], side="right") - 1)
        ii = int(np.searchsorted(innov_edges, innov_hat[k], side="right") - 1)
        si = int(np.clip(si, 0, regret.shape[0] - 1))
        ii = int(np.clip(ii, 0, regret.shape[1] - 1))
        r = regret[si, ii]
        best_j = int(np.argmin(r))
        sorted_r = np.sort(r)
        gap = (sorted_r[1] - sorted_r[0]) if len(sorted_r) > 1 else 0.0
        # Confidence proxy: how much the best beats the second best, normalized
        # by the spread. Higher gap -> higher confidence in the best N.
        spread = (sorted_r[-1] - sorted_r[0]) if len(sorted_r) > 1 else 1e-12
        conf = gap / max(spread, 1e-12)
        if conf >= confidence_threshold:
            n_per_block[k] = int(WINDOW_GRID[best_j])
        else:
            n_per_block[k] = int(bstar_n)
    rx_comp = adaptive_window_apply(rx_trim, n_per_block, block, modulation)
    return AdaptiveResult(n_per_block=n_per_block, rx_comp=rx_comp, method="p3_confidence_safe")
