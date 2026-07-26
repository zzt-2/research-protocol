"""T008 v2 CPE core — fixed-window, adaptive-window phase estimators.

Block-buffered CPE families, all receiver-visible (no truth in the signature):

  - vv_block_mean(rx, N, modulation): block-mean Viterbi-Viterbi. Raises rx to
    M=4, averages over N symbols, takes the angle, divides by 4, subtracts the
    modulation-dependent deterministic pi/4 bias (deployable). The remaining
    pi/2 global ambiguity is left to the evaluator's legal global resolve.
  - pilot_block_mean(rx, pilot_mask, pilot_symbols, N): pilot moving-average
    CPE over N pilot phases, equal overhead charged by the runner.

Adaptive controllers (P1/P2/P3) pick N per block from the shared window grid
{8,16,32,64,128,256} using receiver-visible features ONLY.

v2 identity closures:
  - B*/B-cond are FROZEN INTEGERS chosen on validation; the test phase reads
    the frozen integer and never re-selects from test truth (gap1 closure).
  - The per-block oracle candidate set == window_grid; B* is a member by
    construction (oracle BER <= B* BER per block) (gap3 closure).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

import numpy as np

from channel import estimate_phase_innovation_hat, estimate_snr_hat


WINDOW_GRID = (8, 16, 32, 64, 128, 256)
M0 = 4   # QPSK/16-QAM square constellation raised-power order
PI4_BIAS = np.pi / 4.0   # QPSK deterministic fourth-power bias


def raised_power_bias(modulation: str) -> float:
    """Deterministic fourth-power bias = angle(E[constellation^4]) / M0.

    Receiver-visible (the constellation is known at the receiver). QPSK: pi/4.
    16-QAM: |E[s^4]|≈0 (raised mean cancels) → bias undefined → use 0 and rely
    on legal pi/2 resolve; V&V is approximate for 16-QAM (residual noise is
    irreducible V&V error for non-PSK constellations).
    """
    if modulation == "qpsk":
        return PI4_BIAS
    if modulation == "qam16":
        pts = np.array([(di + 1j * dq) / np.sqrt(10)
                        for di in (-3, -1, 1, 3) for dq in (-3, -1, 1, 3)])
        raised = pts ** M0
        m = raised.mean()
        if np.abs(m) < 1e-9:
            return 0.0
        return float(np.angle(m) / M0)
    raise ValueError(f"modulation must be 'qpsk' or 'qam16', got {modulation!r}")


# ---------------------------------------------------------------------------
# Fixed-window VV (block-buffered, causal, block latency 0)
# ---------------------------------------------------------------------------
def vv_block_mean(rx: np.ndarray, N: int, modulation: str = "qpsk") -> np.ndarray:
    """Block-mean Viterbi-Viterbi CPE with window N.

    Raises rx to M0=4, averages each contiguous block of N symbols, takes the
    angle, divides by M0, subtracts the deterministic bias. Returns the
    per-symbol phase-compensated RX (block-buffered, causal). The last partial
    block (shorter than N) is dropped.
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
        amp = np.abs(raised)
        if np.any(amp > 1e8):
            raised = raised / np.maximum(amp, 1e-12) * 1e8
        phi_raised = np.angle(raised.mean())
        phi_est = phi_raised / M0 - bias
        rx_comp[lo:hi] = block * np.exp(-1j * phi_est)
    return rx_comp


def pilot_block_mean(rx: np.ndarray, pilot_mask: np.ndarray,
                     pilot_symbols: np.ndarray, N: int) -> np.ndarray:
    """Pilot moving-average CPE over N pilot symbols (causal, equal overhead)."""
    rx = np.asarray(rx, dtype=complex)
    pilot_idx = np.where(pilot_mask)[0]
    n_pilots = len(pilot_idx)
    if n_pilots == 0:
        return rx.copy()
    pilot_phase = np.angle(rx[pilot_idx] / pilot_symbols)
    rx_comp = rx.copy()
    n_blocks = n_pilots // N
    for k in range(n_blocks):
        lo_p, hi_p = k * N, (k + 1) * N
        phi_est = pilot_phase[lo_p:hi_p].mean()
        sym_lo = pilot_idx[lo_p]
        sym_hi = pilot_idx[hi_p - 1] + 1 if hi_p - 1 < n_pilots else len(rx)
        rx_comp[sym_lo:sym_hi] = rx[sym_lo:sym_hi] * np.exp(-1j * phi_est)
    last_sym = pilot_idx[n_blocks * N - 1] + 1 if n_blocks * N >= 1 else 0
    rx_comp = rx_comp[:last_sym]
    return rx_comp


# ---------------------------------------------------------------------------
# Adaptive window application (block-buffered, causal; per-block N from grid)
# ---------------------------------------------------------------------------
def adaptive_window_apply(rx: np.ndarray, n_per_block: np.ndarray,
                          block: int, modulation: str = "qpsk") -> np.ndarray:
    """Apply a per-block window choice to the RX (block-buffered, causal).

    The block length `block` is the unit of adaptation. Within each block the
    window N (from WINDOW_GRID) is the VV averaging length: average the whole
    block when N>=block, or split into N-length mini-blocks when N<block. The
    deterministic bias is subtracted. Reads only the current block (no future).
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
            raised = block_rx ** M0
            amp = np.abs(raised)
            if np.any(amp > 1e8):
                raised = raised / np.maximum(amp, 1e-12) * 1e8
            phi_raised = np.angle(raised.mean())
            phi_est = phi_raised / M0 - bias
            rx_comp[lo:hi] = block_rx * np.exp(-1j * phi_est)
        else:
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


# ---------------------------------------------------------------------------
# Validation freezing: B* (single global N) and B-cond (one N per condition)
# ---------------------------------------------------------------------------
@dataclass
class FrozenBaselines:
    """Validation-frozen baseline windows (gap1 closure).

    bstar_n is a SINGLE integer chosen on validation across ALL cells.
    bcond_n_by_condition maps condition key -> a single integer.
    Both are FROZEN; the test phase reads these integers only and never
    re-selects from test truth.
    """
    bstar_n: int
    bcond_n_by_condition: dict   # {condition_key: int}


def select_bstar_bcond(validation_rows: list, fallback_metric: str = "mean_log_ber") -> FrozenBaselines:
    """Select B* (single global N) and B-cond (one N per condition) on VALIDATION.

    `validation_rows` is a list of dicts with keys:
        modulation, condition, snr_db, seed, per_window_BER (list aligned to WINDOW_GRID),
        required_snr_at_fec (float or nan), per_window_log_ber (optional).

    Selection rule:
      - B* = single N minimizing the AGGREGATE required-SNR across all cells
        (mean over cells where FEC is reachable). When FEC is unreachable for
        all cells, fall back to minimizing the aggregate mean-log-BER (the
        fair single-number proxy when no legal crossing exists).
      - B-cond = per condition, the N minimizing aggregate required-SNR (or
        mean-log-BER fallback) within that condition.

    The returned integers are FROZEN; test reads them only.
    """
    # Aggregate required-SNR per N (cells where reachable).
    req_by_n = {N: [] for N in WINDOW_GRID}
    meanlog_by_n = {N: [] for N in WINDOW_GRID}
    req_by_cond_n = {}   # (condition, N) -> list of req_snr
    meanlog_by_cond_n = {}
    for r in validation_rows:
        pwl = r["per_window_BER"]
        per_w_log = [float(np.log10(max(b, 1e-12))) for b in pwl]
        for j, N in enumerate(WINDOW_GRID):
            meanlog_by_n[N].append(per_w_log[j])
            req = r.get("per_window_required_snr", [float("nan")] * len(WINDOW_GRID))
            if not np.isnan(req[j]):
                req_by_n[N].append(float(req[j]))
        cond = r["condition"]
        for j, N in enumerate(WINDOW_GRID):
            meanlog_by_cond_n.setdefault((cond, N), []).append(per_w_log[j])
            req = r.get("per_window_required_snr", [float("nan")] * len(WINDOW_GRID))
            if not np.isnan(req[j]):
                req_by_cond_n.setdefault((cond, N), []).append(float(req[j]))

    def _pick(metric_dict, keys):
        # Prefer required-SNR; fallback to mean-log-BER if no reachable cell.
        reachable = {k: v for k, v in metric_dict.items() if len(v) > 0}
        if reachable:
            best = min(reachable, key=lambda k: float(np.mean(reachable[k])))
        else:
            best = None
        return best

    # B* (keyed by N only): build req_by_n_flat
    req_flat = {N: req_by_n[N] for N in WINDOW_GRID}
    ml_flat = {N: meanlog_by_n[N] for N in WINDOW_GRID}
    bstar_req = _pick(req_flat, WINDOW_GRID)
    if bstar_req is not None:
        bstar_n = int(bstar_req)
    else:
        # fallback to mean-log-BER (lower = better)
        bstar_n = int(min(ml_flat, key=lambda N: float(np.mean(ml_flat[N]))))

    # B-cond per condition.
    conditions = sorted(set(r["condition"] for r in validation_rows))
    bcond = {}
    for cond in conditions:
        req_c = {N: req_by_cond_n.get((cond, N), []) for N in WINDOW_GRID}
        ml_c = {N: meanlog_by_cond_n.get((cond, N), []) for N in WINDOW_GRID}
        bc_req = _pick(req_c, WINDOW_GRID)
        if bc_req is not None:
            bcond[cond] = int(bc_req)
        else:
            bcond[cond] = int(min(ml_c, key=lambda N: float(np.mean(ml_c[N]))))

    return FrozenBaselines(bstar_n=bstar_n, bcond_n_by_condition=bcond)


# ---------------------------------------------------------------------------
# Adaptive window controllers (P1 / P2 / P3) — receiver-visible only
# ---------------------------------------------------------------------------
@dataclass
class AdaptiveResult:
    n_per_block: np.ndarray
    rx_comp: np.ndarray
    method: str


def _blocks_and_features(rx: np.ndarray, block: int):
    rx = np.asarray(rx, dtype=complex)
    n = len(rx)
    nb = n // block
    L = nb * block
    rx_trim = rx[:L]
    snr_hat = estimate_snr_hat(rx_trim, window=block)
    innov_hat = estimate_phase_innovation_hat(rx_trim, m0=M0, window=block)
    return rx_trim, nb, block, snr_hat, innov_hat


def p1_physics_ratio_rule(rx: np.ndarray, block: int,
                          snr_lo_db: float, snr_hi_db: float,
                          innov_lo: float, innov_hi: float,
                          modulation: str = "qpsk",
                          innov_weight: float = 0.5,
                          bstar_n: int = 64) -> AdaptiveResult:
    """P1 — physics-ratio rule.

    Maps receiver-visible (SNR_hat, phase_innovation_hat) to N via a monotone
    clipped interpolation following E1 (SNR down -> N up) and E2 (innov up ->
    N down). Reads NO oracle / NO truth. Out-of-range / uninformative -> B*.
    """
    rx_trim, nb, _, snr_hat, innov_hat = _blocks_and_features(rx, block)
    snr_norm = np.clip((snr_hat - snr_lo_db) / max(snr_hi_db - snr_lo_db, 1e-12), 0.0, 1.0)
    innov_norm = np.clip((innov_hat - innov_lo) / max(innov_hi - innov_lo, 1e-12), 0.0, 1.0)
    w = float(innov_weight)
    large_n_score = (1.0 - w) * (1.0 - snr_norm) + w * (1.0 - innov_norm)
    idx = np.clip(np.round(large_n_score * (len(WINDOW_GRID) - 1)).astype(int),
                  0, len(WINDOW_GRID) - 1)
    n_per_block = np.array(WINDOW_GRID)[idx]
    rx_comp = adaptive_window_apply(rx_trim, n_per_block, block, modulation)
    return AdaptiveResult(n_per_block=n_per_block, rx_comp=rx_comp, method="p1_physics_ratio_rule")


def p2_lookup_hysteresis(rx: np.ndarray, block: int,
                         lookup_table: dict,
                         hysteresis_band: float,
                         initial_n: int = 32,
                         modulation: str = "qpsk") -> AdaptiveResult:
    """P2 — validation lookup table on (SNR_hat, phase_innovation_hat) + hysteresis.

    Across blocks, N switches only when the (snr_bin, innov_bin) crosses a
    hysteresis band by more than `hysteresis_band`. Suppresses window chatter.
    Reads NO oracle / NO truth.
    """
    rx_trim, nb, _, snr_hat, innov_hat = _blocks_and_features(rx, block)
    snr_edges = lookup_table["snr_edges"]
    innov_edges = lookup_table["innov_edges"]
    table = np.asarray(lookup_table["table"])
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
    """P3 — confidence-safe selector. Validation-learned per-window regret ->
    N; low confidence falls back to B*. NO test labels, NO oracle best N.
    Frozen shallow table only.
    """
    rx_trim, nb, _, snr_hat, innov_hat = _blocks_and_features(rx, block)
    snr_edges = regret_table["snr_edges"]
    innov_edges = regret_table["innov_edges"]
    regret = np.asarray(regret_table["regret"])
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
        spread = (sorted_r[-1] - sorted_r[0]) if len(sorted_r) > 1 else 1e-12
        conf = gap / max(spread, 1e-12)
        if conf >= confidence_threshold:
            n_per_block[k] = int(WINDOW_GRID[best_j])
        else:
            n_per_block[k] = int(bstar_n)
    rx_comp = adaptive_window_apply(rx_trim, n_per_block, block, modulation)
    return AdaptiveResult(n_per_block=n_per_block, rx_comp=rx_comp, method="p3_confidence_safe")


# ---------------------------------------------------------------------------
# Majority-fixed baseline (the strong naive observability comparator, gap4)
# ---------------------------------------------------------------------------
def majority_fixed_apply(rx: np.ndarray, majority_n: int, block: int,
                         modulation: str = "qpsk") -> np.ndarray:
    """Majority-fixed: apply the SINGLE most-frequent oracle-best-N (validation)
    to every block. The strong naive observability comparator — if a deployable
    method cannot beat this, it has no real selectivity.
    """
    n_per_block = np.full(len(rx) // block, int(majority_n), dtype=int)
    return adaptive_window_apply(rx, n_per_block, block, modulation)
