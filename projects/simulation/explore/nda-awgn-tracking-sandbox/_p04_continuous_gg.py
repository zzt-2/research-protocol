# -*- coding: utf-8 -*-
"""P04 — Continuous-GG OOD selector robustness probe (Phase A/B/C).

Binding-arbitration rewritten question (family C_CONTINUOUS_GG_OOD_SELECTOR_ROBUSTNESS):
  Does the AWGN-fitted CV decision boundary of the frozen DA/NDA selector
  (_a4_switch_common768_30seed.decide) produce a selector-specific regret on CONTINUOUS
  Gamma-Gamma distributions within the literature σ_R² range [0.2, 3.5] but OUTSIDE the
  three training anchors (weak/moderate/strong = 0.2/1.6/3.5)?

KEY DISCIPLINE (frozen in worker-log step-031 §1, BEFORE any test data):
  - σ_R² → (α,β) via the Al-Habash plane-wave CLOSED FORM documented in
    system_model.tex:16-21 (verified to reproduce the 3 anchors to ≤2.70%).
    The explore/mcs-gain-upperbound rytov_to_gg piecewise-symmetric proxy is NOT used.
  - Channel injection = explicit turb_params=(alpha,beta) on generate_shared_realization_apsk
    (common/_channel.py:97-99,10-24). Same shared GG-block + Doppler/laser-phase engine (TL-13).
  - The original selector decide() is fed the TRUE gamma_db (delta=0): the OOD variable is
    the GG SHAPE (alpha,beta), NOT a gamma mismatch. TRUE alpha/beta/true-h/turbulence-label
    NEVER enter decide() (AST-audit clean, as in P03/V067 check 5).
  - Frozen selector _a4_switch_common768_30seed.py / common/ / params.py UNCHANGED.
  - Anchor regression gate: at σ_R²∈{0.2,1.6,3.5} the explicit-(alpha,beta) path MUST
    reproduce the scene-name path's selected_errors + n_select_da/nda per seed exactly.

This mirrors _p01_cpr_snr_mismatch_probe.run_case_multidelta line-for-line, replacing the
scene-name channel call with an explicit-(alpha,beta) channel call, and dropping the
delta-loop (the OOD variable is (alpha,beta), not gamma mismatch).
"""
import os
import sys
import math
import json
import time

import numpy as np
from scipy import stats

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
sys.path[:0] = [_SIM_ROOT, os.path.join(_SIM_ROOT, 'simulator'), _EXP := _HERE]

import _b11_params as P  # noqa: E402
import _a4_switch_common768_30seed as A  # noqa: E402  (frozen selector, do not modify)
import sc_nda_ml_sim as S  # noqa: E402
from common import (  # noqa: E402
    amp_limit, mmse_equalize, generate_shared_realization_apsk,
)
from params import SimulationConfig  # noqa: E402

N_WINDOWS = 400
SNR_DB = (5.0, 7.0, 9.0, 11.0, 13.0)   # P01/P02 gain-bearing low-SNR band

# σ_R² → (α,β): Al-Habash plane-wave closed form (system_model.tex:16-21)
ANCHOR_SIGMA2 = {"weak": 0.2, "moderate": 1.6, "strong": 3.5}
# Frozen literature anchor pairs (params.get_turb_dict / system_model.tex:22) — used at the
# 3 training σ_R² for EXACT anchor regression (the selector anchor was trained on these
# rounded pairs, not the Al-Habash exact values). Al-Habash differs by ≤2.70% on anchors.
FROZEN_ANCHOR_AB = {0.2: (11.6, 10.1), 1.6: (4.0, 1.9), 3.5: (4.2, 1.4)}


def alhabash(sigma2):
    """Al-Habash plane-wave σ_R² → (α,β). system_model.tex:16-21. Verified ≤2.70% on anchors."""
    a = 1.0 / (math.exp(0.49 * sigma2 / ((1.0 + 1.11 * sigma2 ** (6.0 / 5.0)) ** (7.0 / 6.0))) - 1.0)
    b = 1.0 / (math.exp(0.51 * sigma2 / ((1.0 + 0.69 * sigma2 ** (6.0 / 5.0)) ** (5.0 / 6.0))) - 1.0)
    return a, b


def sigma2_to_ab(sigma2):
    """σ_R² → (α,β): frozen anchor pairs at the 3 training points (exact regression),
    Al-Habash closed form elsewhere (continuous interior points). One bounded deterministic
    fix (V067 allows one): exact regression requires the frozen rounded pairs the anchor was
    trained on; Al-Habash exact values differ by ≤2.70% and would break byte-exact regression
    at 'strong'. Continuous interior points use Al-Habash (≤2.70% from anchors → controlled
    extrapolation, not a discontinuous jump)."""
    if sigma2 in FROZEN_ANCHOR_AB:
        return FROZEN_ANCHOR_AB[sigma2]
    return alhabash(sigma2)


# Frozen grids (worker-log §1.4)
DEV_SIGMA2 = (0.2, 0.45, 0.7, 1.15, 1.6, 2.0, 2.55, 3.0, 3.5)          # 9 pts (incl. 3 anchors)
HELDOUT_SIGMA2 = (0.3, 0.9, 1.35, 1.85, 2.3, 3.15)                      # 6 interior-only pts
DEV_SEEDS = list(range(0, 10))
TUNE_SEEDS = list(range(10, 20))
HELDOUT_SEEDS = list(range(30, 50))
MDE = 0.15


def run_case_contgg(alpha, beta, gamma_db, seed_index, n_windows=N_WINDOWS,
                    extra_selector=None):
    """Run one (alpha,beta,gamma_db,seed) cell. Mirrors run_case_multidelta (P01 probe)
    but injects explicit turb_params=(alpha,beta). Selector fed TRUE gamma (delta=0).

    Returns base dict (fixed_DA/NDA common-768, lower_count_bound, oracle, per-window errs,
    pw_raw, pw_tx) and per-method selector results {name: {selected_errors,n_select_da,
    n_select_nda, choices}}.
    """
    cfg = SimulationConfig()
    gl_true = 10 ** (gamma_db / 10)
    start = P.SEED_TURB0 + seed_index * N_WINDOWS

    fixed_nda = 0
    fixed_da = 0
    lower_bound = 0
    true_oracle_errors = 0
    true_oracle_bits = 0
    pw_da_err = np.empty(n_windows, dtype=np.int64)
    pw_nda_err = np.empty(n_windows, dtype=np.int64)
    pw_raw = []
    pw_tx = []

    for b in range(n_windows):
        ws = start + b
        # explicit (alpha,beta) injection — scene name unused once turb_params given
        r = generate_shared_realization_apsk(
            P.N_DFT, gl_true, '_contgg', cfg.doppler.DOPPLER_HIGH,
            mod="m16apsk", seed=ws, turb_params=(alpha, beta))
        raw, bits, tx = r["rx_raw"], r["bits"], r["tx"]
        hb = S.estimate_h_blind_perblock(raw, gl_true)
        hp = S.estimate_h_pilot_perblock(raw, tx, gl_true)
        blind = amp_limit(mmse_equalize(raw, hb, gl_true), 3.0)
        pilot = amp_limit(mmse_equalize(raw, hp, gl_true), 3.0)
        nn, nd, nc = A.per_block(blind, pilot, bits, tx)
        fixed_nda += nc
        fixed_da += nd
        lower_bound += min(nc, nd)
        pw_da_err[b] = nd
        pw_nda_err[b] = nc
        pw_raw.append(raw)
        pw_tx.append(tx)
        trueh = amp_limit(mmse_equalize(raw, r["h"], gl_true), 3.0)
        no, nob = S.ber_oracle_turb(trueh, bits, r["phi"])
        true_oracle_errors += no
        true_oracle_bits += nob

    base = {
        "fixed_nda_errors": int(fixed_nda),
        "fixed_da_errors": int(fixed_da),
        "lower_count_bound_errors": int(lower_bound),
        "true_oracle_errors": int(true_oracle_errors),
        "true_oracle_bits": int(true_oracle_bits),
        "n_windows": int(n_windows),
    }

    def _eval(decide_fn, needs_pilot=False, needs_reset=None):
        if needs_reset is not None:
            needs_reset()
        choices = []
        sel_err = 0
        n_da = n_nda = 0
        glin = 10 ** (gamma_db / 10)
        for b in range(n_windows):
            if needs_pilot:
                _set_pilots(pw_tx[b])
            ch = decide_fn(pw_raw[b], gamma_db, glin, b)
            choices.append(ch)
            if ch == "da":
                n_da += 1
                sel_err += int(pw_da_err[b])
            else:
                n_nda += 1
                sel_err += int(pw_nda_err[b])
        return {"selected_errors": int(sel_err), "n_select_da": int(n_da),
                "n_select_nda": int(n_nda), "choices": choices}

    out = {"base": base,
           "orig": _eval(lambda raw, gdb, glin, b: A.decide(raw, gdb, glin))}
    if extra_selector:
        for name, spec in extra_selector.items():
            out[name] = _eval(spec["fn"], spec.get("needs_pilot", False),
                              spec.get("needs_reset"))
    return out


# pilot hooks (for any Phase-B/C pilot-based candidate; default no-op)
_set_pilots = lambda tx: None


def wire_pilot_hooks(set_pilots_fn):
    global _set_pilots
    _set_pilots = set_pilots_fn


def ci_t(data):
    a = np.asarray(data, dtype=float)
    n = len(a)
    mean = float(np.mean(a))
    std = float(np.std(a, ddof=1)) if n > 1 else 0.0
    hw = float(stats.t.ppf(0.975, n - 1)) * std / np.sqrt(n) if n > 1 else 0.0
    return mean, std, hw, mean - hw, mean + hw
