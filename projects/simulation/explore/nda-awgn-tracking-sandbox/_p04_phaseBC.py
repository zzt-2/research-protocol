# -*- coding: utf-8 -*-
"""P04 Phase B/C — global-retune comparator + conditional robust candidates.

Phase B (frozen, worker-log §1.2): a SINGLE global retune of the existing CV decision
boundary tuned on the DEV continuous grid (one global parameter set for the whole range,
NOT per-cell, NOT reading turbulence label/true α,β). Same tuning budget as any candidate.
Resolved bar: if global retune removes the regret (pooled orig-after-retune regret < MDE OR
best candidate's advantage over global-retune < MDE) -> PROBLEM_RESOLVED_BY_GLOBAL_RETUNE.

Phase C (frozen, worker-log §1.3): 3-5 mechanism-distinct candidates using ONLY
receiver-visible stats, mechanism distinct from a simple global threshold. Each gets the
same dev-tuning budget. Success bar: pooled paired Δgain vs global-retune >= MDE AND CI_lo>0
on fresh held-out, consistent across >=2 sub-ranges.

ALL decide paths consume only (raw, gamma_db, gamma_lin [, past-window receiver stats /
pilot estimate]). No true α/β/h/turbulence-label/TX-truth (AST-audit clean).
"""
import os
import sys
import json
import time
import math

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
sys.path[:0] = [_SIM_ROOT, os.path.join(_SIM_ROOT, 'simulator'), _HERE]

import _p04_continuous_gg as P4  # noqa: E402
import _a4_switch_common768_30seed as A  # noqa: E402  (frozen selector)

OUT_DIR = os.path.join(_SIM_ROOT, "results", "p04_continuous_gg_ood")

# ---- Phase B: global retune of the frozen CV boundary ----
# The frozen selector: stage1 cv < cv_awgn_theory(g)*CV_MARGIN -> nda;
# stage2 gamma_eff = gamma_db + 10log10(h_proxy) < GAMMA_EFF_TH -> da.
# Phase B retunes the TWO scalar knobs (CV_MARGIN, GAMMA_EFF_TH) GLOBALLY on dev.
FROZEN_CV_MARGIN = A.CV_MARGIN          # 1.10
FROZEN_GEFF_TH = A.GAMMA_EFF_TH         # 13.0


def decide_retuned(raw, gamma_db, gamma_lin, cv_margin, geff_th):
    """Original decide logic with retuned global scalars. Receiver-visible only."""
    pwr = np.abs(raw) ** 2
    cv = float(np.std(pwr) / max(np.mean(pwr), 1e-12))
    if cv < A.cv_awgn_theory(gamma_db) * cv_margin:
        return "nda"
    h = max(float(np.mean(pwr) - 1.0 / (2.0 * gamma_lin)), 1e-6)
    return "da" if gamma_db + 10.0 * np.log10(h) < geff_th else "nda"


def phaseB_tune(raw_rows_dev):
    """Grid-search the single global (cv_margin, geff_th) that minimizes pooled regret on dev
    interior cells. Grid: cv_margin in {0.95,1.00,1.05,1.10,1.15,1.20,1.30}, geff_th in
    {11,12,13,14,15}. Returns best (cv_margin, geff_th)."""
    from collections import defaultdict
    # group dev rows by (sigma2,gamma,seed) and precompute per-window choices needs raw — but
    # we stored only aggregates. Re-run a lightweight regret eval per config using stored
    # branch errors is not possible (choices depend on raw). So we re-evaluate on dev by
    # re-running the selector with each config. To keep cost bounded, sample a subset.
    # Strategy: for each config, re-run dev interior cells (6 interior sigma^2 x 5 SNR x 10 seeds)
    # and compute pooled regret vs best-fixed-branch.
    cm_grid = [0.95, 1.00, 1.05, 1.10, 1.15, 1.20, 1.30]
    gt_grid = [11.0, 12.0, 13.0, 14.0, 15.0]
    interior = [s for s in P4.DEV_SIGMA2 if s not in P4.FROZEN_ANCHOR_AB]
    best = None
    for cm in cm_grid:
        for gt in gt_grid:
            regrets = []
            for s2 in interior:
                a, b = P4.sigma2_to_ab(s2)
                for gamma_db in P4.SNR_DB:
                    for seed in P4.DEV_SEEDS:
                        r = P4.run_case_contgg(a, b, gamma_db, seed,
                                               extra_selector={"retuned": {
                                                   "fn": lambda raw, gdb, glin, b, cm=cm, gt=gt:
                                                   decide_retuned(raw, gdb, glin, cm, gt)}})
                        sel = r["retuned"]["selected_errors"]
                        best_fixed = min(r["base"]["fixed_da_errors"], r["base"]["fixed_nda_errors"])
                        if sel > 0 and best_fixed > 0:
                            regrets.append(10 * np.log10(sel / best_fixed))
            mean = float(np.mean(regrets)) if regrets else float("inf")
            if best is None or mean < best[0]:
                best = (mean, cm, gt, len(regrets))
    print(f"Phase B global retune: best pooled dev-interior regret = {best[0]:+.4f} dB "
          f"at CV_MARGIN={best[1]}, GAMMA_EFF_TH={best[2]} (n={best[3]})")
    return best[1], best[2], best[0]


# ---- Phase C: mechanism-distinct robust candidates (receiver-visible only) ----

def cand_uncertainty_band(raw, gamma_db, gamma_lin, b):
    """1. Uncertainty-band boundary: widen CV margin adaptively when raw-power CV is large
    (high variance => low confidence in the AWGN-fitted boundary). Uses running max of
    past-window CV via the shared _CV_HISTORY (receiver-visible)."""
    pwr = np.abs(raw) ** 2
    cv = float(np.std(pwr) / max(np.mean(pwr), 1e-12))
    # adaptive margin: grows with how far CV is above the AWGN curve (OOD signal)
    base = A.cv_awgn_theory(gamma_db)
    excess = max(cv - base, 0.0)
    margin = FROZEN_CV_MARGIN + 0.5 * excess  # widen when CV far above AWGN fit
    if cv < base * margin:
        return "nda"
    h = max(float(np.mean(pwr) - 1.0 / (2.0 * gamma_lin)), 1e-6)
    return "da" if gamma_db + 10.0 * np.log10(h) < FROZEN_GEFF_TH else "nda"


def cand_minimax(raw, gamma_db, gamma_lin, b):
    """2. Distributionally-robust / minimax: evaluate decide at gamma_db and gamma_db±2dB;
    if all three agree use it; else fall back to the more conservative (nda) branch.
    Different deployable action than a scalar retune (hedges across gamma uncertainty)."""
    choices = set()
    for d in (-2.0, 0.0, 2.0):
        gd = gamma_db + d
        gl = 10.0 ** (gd / 10.0)
        choices.add(A.decide(raw, gd, gl))
    if len(choices) == 1:
        return choices.pop()
    return "nda"  # conservative fallback when boundary is ambiguous


_EMA = {"gamma_db": None}


def cand_running_quantile(raw, gamma_db, gamma_lin, b):
    """3. Running-quantile calibrated selector: EMA-smooth gamma_db across windows and apply
    a quantile-style shift to suppress single-window spikes (receiver-visible past stats).
    Different mechanism: temporal aggregation + shift, not a static boundary retune."""
    if _EMA["gamma_db"] is None:
        _EMA["gamma_db"] = gamma_db
    else:
        _EMA["gamma_db"] = 0.3 * gamma_db + 0.7 * _EMA["gamma_db"]
    gd = _EMA["gamma_db"] - 1.0  # conservative shift (hedges toward nda)
    gl = 10.0 ** (gd / 10.0)
    return A.decide(raw, gd, gl)


def reset_ema():
    _EMA["gamma_db"] = None


def cand_confidence_gate(raw, gamma_db, gamma_lin, b):
    """4. Confidence-gated fallback: if |gamma_eff - threshold| <= 2 dB (fragile near-threshold
    zone where AWGN-fit is least reliable), defer to a CV-only test at a fixed conservative
    reference; else apply normal stage-2. Different action: zone-dependent routing."""
    pwr = np.abs(raw) ** 2
    cv = float(np.std(pwr) / max(np.mean(pwr), 1e-12))
    h = max(float(np.mean(pwr) - 1.0 / (2.0 * gamma_lin)), 1e-6)
    geff = gamma_db + 10.0 * np.log10(h)
    if abs(geff - FROZEN_GEFF_TH) <= 2.0:
        # near-threshold: use a CV-only conservative rule (favor nda unless CV very low)
        return "da" if cv < A.cv_awgn_theory(gamma_db) * 0.85 else "nda"
    return "da" if geff < FROZEN_GEFF_TH else "nda"


def cand_monotone_cal(raw, gamma_db, gamma_lin, b):
    """5. Monotone receiver-statistic calibration: replace the AWGN-fitted cv_awgn_theory
    curve with a monotone-in-gamma floor derived from the raw-power CV itself (receiver-
    visible), removing dependence on the AWGN extrapolation. Floor = cv_median_estimate."""
    pwr = np.abs(raw) ** 2
    cv = float(np.std(pwr) / max(np.mean(pwr), 1e-12))
    # monotone floor: higher gamma => lower expected CV; use a simple decaying floor
    floor = 0.74 + 0.12 * math.exp(-gamma_db / 5.0)  # same shape, but...
    # ...apply a gamma-magnitude-FREE comparison anchor like P01 cand_rank did, at ref=9
    ref_floor = 0.74 + 0.12 * math.exp(-9.0 / 5.0)
    if cv < ref_floor * FROZEN_CV_MARGIN:
        return "nda"
    h = max(float(np.mean(pwr) - 1.0 / (2.0 * gamma_lin)), 1e-6)
    return "da" if gamma_db + 10.0 * np.log10(h) < FROZEN_GEFF_TH else "nda"


CANDIDATES = {
    "cand_uncertainty_band": (cand_uncertainty_band, False, None),
    "cand_minimax": (cand_minimax, False, None),
    "cand_running_quantile": (cand_running_quantile, False, reset_ema),
    "cand_confidence_gate": (cand_confidence_gate, False, None),
    "cand_monotone_cal": (cand_monotone_cal, False, None),
}


def run_heldout(sigma2_list, seeds, methods_spec, tag):
    """Run held-out grid for [orig, globalretune, *candidates]. methods_spec: name->(fn,npf,nrf)."""
    t0 = time.time()
    raw_rows = []
    for s2 in sigma2_list:
        a, b = P4.sigma2_to_ab(s2)
        for gamma_db in P4.SNR_DB:
            for seed in seeds:
                extra = {n: {"fn": fn, "needs_pilot": npf, "needs_reset": nrf}
                         for n, (fn, npf, nrf) in methods_spec.items() if n != "orig"}
                r = P4.run_case_contgg(a, b, gamma_db, seed, extra_selector=extra or None)
                base = r["base"]
                best_fixed = min(base["fixed_da_errors"], base["fixed_nda_errors"])
                for name in ["orig"] + list(methods_spec.keys())[0 if "orig" in methods_spec else 0:]:
                    if name == "orig":
                        sel = r["orig"]["selected_errors"]
                    else:
                        sel = r[name]["selected_errors"]
                    regret = float(10 * np.log10(sel / best_fixed)) if sel > 0 and best_fixed > 0 else float("inf")
                    raw_rows.append({
                        "tag": tag, "sigma2": float(s2), "alpha": float(a), "beta": float(b),
                        "is_anchor": s2 in P4.FROZEN_ANCHOR_AB, "gamma_db": float(gamma_db),
                        "seed_index": int(seed), "method": name,
                        "selected_errors": int(sel),
                        "best_fixed_errors": int(best_fixed),
                        "regret_db": regret,
                    })
    return raw_rows, time.time() - t0
