# -*- coding: utf-8 -*-
"""P01 Phase B/C — conventional SNR adapter + robust selector candidates.

All estimators/deciders here use ONLY receiver-visible quantities (raw rx, known
pilots, known pilot spacing). They NEVER see true gamma. The biased nominal
gamma_hat (delta-corrupted) is discarded by the adapter; the robust candidates
may still consume gamma_hat but combine it with uncertainty-aware logic.

Selector signature (so the multidelta runner can call any of them uniformly):
    decide_fn(raw, gamma_hat_db, gamma_hat_lin, b) -> 'da' or 'nda'
where gamma_hat_db / gamma_hat_lin are the (biased) nominal SNR the receiver
holds. The adapter IGNORES these and re-estimates from raw + pilots.
"""
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
sys.path[:0] = [_SIM_ROOT, os.path.join(_SIM_ROOT, 'simulator'), _HERE]

import _b11_params as P  # noqa: E402
import _a4_switch_common768_30seed as A  # noqa: E402  (frozen selector)


# ----------------------------------------------------------------------
# Phase B: conventional pilot-based SNR estimator (receiver-visible).
# ----------------------------------------------------------------------
# The DA receiver knows the pilot symbols tx_sym at pilot positions. It can form
# an unbiased noise-variance estimate from the pilot residuals. We attach the
# pilot tx symbols to the per-window state via a closure (set_pilots_for_window)
# because the multidelta runner only passes `raw` to decide_fn. To keep the
# signature uniform, we stash the latest pilot array in a module-global that the
# runner refreshes each window BEFORE calling decide.
_PILOT_TX = None   # set per-window by the runner via set_window_pilots


def set_window_pilots(tx_sym):
    """Runner hook: publish this window's pilot tx symbols for pilot-based estimators."""
    global _PILOT_TX
    pidx = np.arange(0, P.N_DFT, P.DA_PILOT_SPACING)
    _PILOT_TX = (pidx, np.asarray(tx_sym[pidx], dtype=complex))


def estimate_snr_pilot(raw, return_pieces=False):
    """Conventional data-aided SNR estimate from pilot residuals.

    Uses the block-wise non-coherent moment split (calibration shows this is the
    least-biased conventional DA-SNR estimator under turbulence; coherent/M2M4
    variants are 2-4x more biased due to fading-induced phase/amplitude variance).

    At pilot position p: e(p) = r(p)/s(p) = sqrt(h(p)) e^{j phi(p)} + n(p)/s(p).
    Within a channel block (h ~ constant): h_blk = mean|e|^2; noise from the
    within-block deviation Var(|e|^2) = sigma2^2 + 2 h sigma2 (complex AWGN) =>
    sigma2 = -h_blk + sqrt(h_blk^2 + Var). gamma_est = (h_blk - sigma2)/sigma2.

    Returns gamma_est_dB. Bias under turbulence ~ -2..-3.5 dB (measured, see
    _p01_estimator_calib.py) — this is the inherent limit of receiver-visible
    SNR estimation under fading and is part of the honest comparator result.
    """
    global _PILOT_TX
    pidx, sp = _PILOT_TX
    e = np.asarray(raw, dtype=complex)[pidx] / sp
    mag2 = np.abs(e) ** 2
    n_pilots_per_block = max(1, P.CH_BLOCK // P.DA_PILOT_SPACING)
    S_acc = s2_acc = 0.0
    n_blk = 0
    for i in range(0, len(mag2), n_pilots_per_block):
        seg = mag2[i:i + n_pilots_per_block]
        if len(seg) < 2:
            continue
        h_blk = float(np.mean(seg))
        v = float(np.var(seg))
        s2 = -h_blk + np.sqrt(max(h_blk * h_blk + v, 0.0))
        s2 = max(s2, 1e-12)
        S_acc += max(h_blk - s2, 1e-12)
        s2_acc += s2
        n_blk += 1
    if n_blk == 0:
        gamma_est_dB = 30.0
        h_hat, sigma2_hat = 1.0, 1e-12
    else:
        h_hat = max(S_acc / n_blk, 1e-12)
        sigma2_hat = max(s2_acc / n_blk, 1e-12)
        gamma_est_dB = 10.0 * np.log10(h_hat / sigma2_hat)
    if return_pieces:
        return gamma_est_dB, h_hat, sigma2_hat
    return gamma_est_dB


def estimate_snr_pilot_coherent(raw, return_pieces=False):
    """Coherent pilot SNR estimator (more biased under fading; secondary comparator)."""
    global _PILOT_TX
    pidx, sp = _PILOT_TX
    e = np.asarray(raw, dtype=complex)[pidx] / sp
    mu = np.mean(e)
    h = float(np.abs(mu) ** 2)
    sigma2 = max(float(np.mean(np.abs(e - mu) ** 2)), 1e-12)
    g = 10.0 * np.log10(max(h / sigma2, 1e-12))
    if return_pieces:
        return g, h, sigma2
    return g


def decide_adapter_pilot(raw, gamma_hat_db, gamma_hat_lin, b):
    """Phase B conventional comparator: pilot SNR estimator + ORIGINAL decide rule.

    Ignores the biased nominal gamma_hat; re-estimates gamma from pilots then
    applies the frozen A.decide logic unchanged.
    """
    g_est_db = estimate_snr_pilot(raw)
    g_est_lin = 10.0 ** (g_est_db / 10.0)
    return A.decide(raw, g_est_db, g_est_lin)


def decide_adapter_pilot_coh(raw, gamma_hat_db, gamma_hat_lin, b):
    """Secondary comparator: coherent pilot estimator + original decide."""
    g_est_db = estimate_snr_pilot_coherent(raw)
    g_est_lin = 10.0 ** (g_est_db / 10.0)
    return A.decide(raw, g_est_db, g_est_lin)


# ----------------------------------------------------------------------
# Phase C: robust candidates (mechanism-different, receiver-visible only).
# Each addresses a different failure mode revealed by Phase A:
#   - harm at delta=-3 (low SNR): selector too NDA-conservative due to noise-
#     subtraction blow-up at low gamma_lin. Robustness = guard the stage-2
#     noise subtraction against gamma_lin collapse.
#   - harm at delta=+3 (high SNR cells): stage-2 gamma_hat_db+10log10(h) crosses
#     13 -> forces NDA where DA would help. Robustness = uncertainty band on gamma.
# ----------------------------------------------------------------------

# Candidate 1: uncertainty-band robust threshold.
# Use a gamma_hat confidence band; pick the branch that is safe under BOTH bounds.
# Implementation: estimate gamma from pilots (like adapter) but blend with nominal
# gamma_hat via a confidence weight, then run decide with the worst-case (min)
# gamma for the stage-1 boundary AND a guarded stage-2.
def decide_cand_uncertainty(raw, gamma_hat_db, gamma_hat_lin, b,
                            blend=0.5):
    """Candidate 1: blend nominal gamma_hat with pilot estimate; guard stage-2.

    gamma_used_db = blend*gamma_hat_db + (1-blend)*g_est_pilot_db.
    Stage-2 noise subtraction uses gamma_used_lin (guarded, floor 1e-3).
    """
    g_est_db = estimate_snr_pilot(raw)
    g_used_db = blend * gamma_hat_db + (1.0 - blend) * g_est_db
    g_used_lin = max(10.0 ** (g_used_db / 10.0), 1e-3)
    # replicate A.decide but with the blended gamma
    pwr = np.abs(raw) ** 2
    cv = float(np.std(pwr) / max(np.mean(pwr), 1e-12))
    if cv < A.cv_awgn_theory(g_used_db) * A.CV_MARGIN:
        return 'nda'
    h = max(float(np.mean(pwr) - 1.0 / (2 * g_used_lin)), 1e-6)
    return 'da' if g_used_db + 10 * np.log10(h) < A.GAMMA_EFF_TH else 'nda'


# Candidate 2: minimax branch rule over gamma uncertainty interval.
# Define an interval [gamma_hat - W, gamma_hat + W]; for each window evaluate the
# branch that is "safe" (does not lose much) under the WORST gamma in the interval.
# Operational proxy: if the CV/stage tests disagree across the interval, fall back
# to the branch that the PILOT estimate recommends (pilot estimate is delta-free).
def decide_cand_minimax(raw, gamma_hat_db, gamma_hat_lin, b,
                        width_db=2.0):
    """Candidate 2: worst-case-over-interval branch, fallback to pilot estimate."""
    g_est_db = estimate_snr_pilot(raw)
    lo = gamma_hat_db - width_db
    hi = gamma_hat_db + width_db
    choices = []
    for g_db in (lo, gamma_hat_db, hi):
        g_lin = 10.0 ** (g_db / 10.0)
        choices.append(A.decide(raw, g_db, g_lin))
    # if all three agree, that's robust -> use it
    if choices[0] == choices[1] == choices[2]:
        return choices[1]
    # otherwise trust the pilot estimate (delta-independent)
    g_est_lin = 10.0 ** (g_est_db / 10.0)
    return A.decide(raw, g_est_db, g_est_lin)


# Candidate 3: confidence-gated fallback near the 13 dB threshold.
# When gamma_eff is within ±margin of GAMMA_EFF_TH, the stage-2 decision is
# fragile; fall back to the pilot-estimated gamma's decision.
def decide_cand_conf_gate(raw, gamma_hat_db, gamma_hat_lin, b,
                          margin_db=2.0):
    """Candidate 3: near-threshold fallback to pilot estimate."""
    pwr = np.abs(raw) ** 2
    cv = float(np.std(pwr) / max(np.mean(pwr), 1e-12))
    if cv < A.cv_awgn_theory(gamma_hat_db) * A.CV_MARGIN:
        return 'nda'
    h = max(float(np.mean(pwr) - 1.0 / (2 * gamma_hat_lin)), 1e-6)
    gamma_eff = gamma_hat_db + 10 * np.log10(h)
    if abs(gamma_eff - A.GAMMA_EFF_TH) <= margin_db:
        # fragile zone: defer to pilot estimate
        g_est_db = estimate_snr_pilot(raw)
        g_est_lin = 10.0 ** (g_est_db / 10.0)
        return A.decide(raw, g_est_db, g_est_lin)
    return 'da' if gamma_eff < A.GAMMA_EFF_TH else 'nda'


# Candidate 4: calibration-free rank/statistic selector.
# Does NOT use gamma magnitude at all. Decides via the RANK of the window's CV
# against a fixed reference (the AWGN-theory CV at a FIXED reference SNR, e.g.
# the operating band center 9 dB). This makes the stage-1 boundary gamma-free.
def decide_cand_rank(raw, gamma_hat_db, gamma_hat_lin, b,
                     ref_snr_db=9.0):
    """Candidate 4: gamma-magnitude-free stage-1 boundary at fixed reference."""
    pwr = np.abs(raw) ** 2
    cv = float(np.std(pwr) / max(np.mean(pwr), 1e-12))
    # stage-1 boundary fixed at reference SNR (gamma-magnitude-free)
    if cv < A.cv_awgn_theory(ref_snr_db) * A.CV_MARGIN:
        return 'nda'
    # stage-2: use pilot estimate for the (still magnitude-dependent) gamma_eff test
    g_est_db = estimate_snr_pilot(raw)
    g_est_lin = 10.0 ** (g_est_db / 10.0)
    h = max(float(np.mean(pwr) - 1.0 / (2 * g_est_lin)), 1e-6)
    return 'da' if g_est_db + 10 * np.log10(h) < A.GAMMA_EFF_TH else 'nda'


# Candidate 5: hysteretic / smoothed gamma selector.
# Smooth gamma_hat across the last few windows to avoid single-window gamma spikes
# flipping the branch. Implemented with an EMA on gamma_hat_db.
_EMA_STATE = {"gamma_db_ema": None}


def decide_cand_hysteresis(raw, gamma_hat_db, gamma_hat_lin, b,
                           alpha=0.3):
    """Candidate 5: EMA-smoothed gamma_hat then original decide."""
    if _EMA_STATE["gamma_db_ema"] is None:
        _EMA_STATE["gamma_db_ema"] = gamma_hat_db
    else:
        _EMA_STATE["gamma_db_ema"] = (
            alpha * gamma_hat_db + (1 - alpha) * _EMA_STATE["gamma_db_ema"])
    g_db = _EMA_STATE["gamma_db_ema"]
    g_lin = 10.0 ** (g_db / 10.0)
    return A.decide(raw, g_db, g_lin)


def reset_hysteresis():
    _EMA_STATE["gamma_db_ema"] = None


def _hysteresis_wrapper(raw, gamma_hat_db, gamma_hat_lin, b):
    return decide_cand_hysteresis(raw, gamma_hat_db, gamma_hat_lin, b)


# Registry: name -> dict(fn=decide_fn, needs_pilot, needs_reset, hyperparams)
CANDIDATES = {
    "adapter_pilot": (decide_adapter_pilot, True, False),
    "adapter_pilot_coh": (decide_adapter_pilot_coh, True, False),
    "cand_uncertainty": (decide_cand_uncertainty, True, False),
    "cand_minimax": (decide_cand_minimax, True, False),
    "cand_conf_gate": (decide_cand_conf_gate, True, False),
    "cand_rank": (decide_cand_rank, True, False),
    "cand_hysteresis": (_hysteresis_wrapper, True, True),
}
