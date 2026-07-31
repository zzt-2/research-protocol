# -*- coding: utf-8 -*-
"""P07 — frozen-receiver runner WITH analog AGC+ADC insertion.

This module mirrors `_p01_cpr_snr_mismatch_probe.run_case_multidelta` window-by-
window, but inserts the AGC+ADC adapter on rx_raw BEFORE the frozen receiver
chain consumes it. The RNG draw order and receiver math are byte-identical to
run_case_multidelta; the ONLY change is `raw -> adc(raw, gain_b)` where gain_b
is decided causally from past quantized windows.

float-bypass identity (FROZEN_CONTRACT §3): with gain=1.0, FS=large, W=64 the
ADC reconstruction error is <= 2^-40 and the per-window receiver outputs
(DA/NDA errors, branch counts, oracle errors) MUST match the original
run_case_multidelta byte-exactly. This is the BLOCKER Phase-0 gate.

Discipline:
  - true h/alpha/beta/tx/phi NEVER enter decide_gain (AST-audited).
  - gain at window b is decided ONLY from windows < b.
  - delta=0 (P07 is an AGC/ADC problem, not an SNR-mismatch problem).
  - the frozen receiver functions (estimate_h_blind/pilot_perblock,
    amp_limit, mmse_equalize, A.per_block, A.decide, S.ber_oracle_turb) are
    imported and called UNCHANGED — they consume the ADC-quantized raw.
"""
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
sys.path[:0] = [_SIM_ROOT, os.path.join(_SIM_ROOT, 'simulator'), _HERE]

import _b11_params as P  # noqa: E402
import _a4_switch_common768_30seed as A  # noqa: E402  (frozen selector)
import sc_nda_ml_sim as S  # noqa: E402
from common import (  # noqa: E402
    amp_limit, mmse_equalize, generate_shared_realization_apsk,
)
from params import SimulationConfig  # noqa: E402

import _p07_adapters as AD  # noqa: E402

N_WINDOWS = 400
SCENES = ("weak", "moderate", "strong")
SNR_DB = tuple(map(float, range(5, 26, 2)))   # 5..25 dB, matches anchor


def _per_window_receiver_outputs(raw, bits, tx, r, gl_true):
    """Mirror run_case_multidelta per-window receiver math EXACTLY.

    Returns (nn_all1024, nd_DA_common768, nc_NDA_common768, oracle_err, oracle_bits).
    Consumes `raw` (which may be the ADC-quantized version). Uses true h ONLY
    for offline BER eval (true_oracle) and for the blind/pilot estimators
    exactly as the anchor does.
    """
    hb = S.estimate_h_blind_perblock(raw, gl_true)
    hp = S.estimate_h_pilot_perblock(raw, tx, gl_true)
    blind = amp_limit(mmse_equalize(raw, hb, gl_true), 3.0)
    pilot = amp_limit(mmse_equalize(raw, hp, gl_true), 3.0)
    nn, nd, nc = A.per_block(blind, pilot, bits, tx)
    trueh = amp_limit(mmse_equalize(raw, r["h"], gl_true), 3.0)
    no, nob = S.ber_oracle_turb(trueh, bits, r["phi"])
    return int(nn), int(nd), int(nc), int(no), int(nob)


def run_case_with_adc(scene, gamma_true_db, seed_index, agc, fs, W,
                      n_windows=N_WINDOWS, return_gain_trace=False):
    """Run one (scene, gamma_true, seed) cell through AGC + ADC + frozen receiver.

    Parameters
    ----------
    agc : _BaseAGC instance (reset() called at start; stateful across windows).
          gain for window b is decided from windows < b (causal).
    fs : float ADC full-scale.
    W : int ADC bit width (W=64 + large fs == float-bypass).

    Returns dict with per-cell aggregates + per-window traces (raw rows).
    Identical channel realization to run_case_multidelta (same seed schedule).
    """
    cfg = SimulationConfig()
    gl_true = 10 ** (gamma_true_db / 10)
    start = P.SEED_TURB0 + seed_index * N_WINDOWS

    agc.reset()

    fixed_nda = 0      # NDA common-768 cumulative
    fixed_da = 0       # DA common-768 cumulative
    selected_errors = 0   # branch the selector picks on the ADC-quantized raw
    n_select_da = 0
    n_select_nda = 0
    lower_bound = 0
    true_oracle_errors = 0
    true_oracle_bits = 0
    pw_da_err = np.empty(n_windows, dtype=np.int64)
    pw_nda_err = np.empty(n_windows, dtype=np.int64)
    pw_clipping = np.empty(n_windows, dtype=np.float64)   # rail-hit fraction
    pw_code_util = np.empty(n_windows, dtype=np.float64)  # distinct codes / 2^W
    pw_gain = np.empty(n_windows, dtype=np.float64)

    for b in range(n_windows):
        ws = start + b
        r = generate_shared_realization_apsk(P.N_DFT, gl_true, scene,
                                             cfg.doppler.DOPPLER_HIGH,
                                             mod="m16apsk", seed=ws)
        raw_float, bits, tx = r["rx_raw"], r["bits"], r["tx"]

        # --- causal gain: decided from PAST windows (< b) ---
        gain_b = agc.gain_for_next()
        pw_gain[b] = float(gain_b)

        # --- analog gain + clip + quantize (this window) ---
        q_raw, cr, ci, rr, ri = AD.quantize_iq(raw_float, gain_b, fs, W)
        rail = rr | ri
        pw_clipping[b] = float(np.mean(rail))
        all_codes = np.concatenate([cr, ci])
        pw_code_util[b] = float(len(np.unique(all_codes)) / (2 ** W))

        # --- frozen receiver on quantized raw ---
        nn, nd, nc, no, nob = _per_window_receiver_outputs(
            q_raw, bits, tx, r, gl_true)
        fixed_nda += nc
        fixed_da += nd
        lower_bound += min(nc, nd)
        pw_da_err[b] = nd
        pw_nda_err[b] = nc
        true_oracle_errors += no
        true_oracle_bits += nob
        # --- selector CHOICE on the ADC-quantized raw (delta=0: gamma_hat=true) ---
        # Mirrors run_case_multidelta _eval_selector at delta=0. The selector sees
        # the SAME (biased=unbiased here) gamma and the quantized raw.
        choice = A.decide(q_raw, gamma_true_db, gl_true)
        if choice == "da":
            n_select_da += 1
            selected_errors += int(nd)
        else:
            n_select_nda += 1
            selected_errors += int(nc)

        # --- AGC observes the PAST quantized window for the NEXT decision ---
        if isinstance(agc, AD.ClippingAwareAGC):
            agc.update(q_raw, rail_past=rail)
        else:
            agc.update(q_raw)

    out = {
        "key": f"{scene}|{gamma_true_db:g}|{seed_index}|{agc.name}|W{W}|fs{fs:g}",
        "scene": scene,
        "gamma_true_db": float(gamma_true_db),
        "seed_index": int(seed_index),
        "agc_name": agc.name,
        "W": int(W),
        "fs": float(fs),
        "n_windows": int(n_windows),
        "n_bits_common768": int(n_windows * 768),
        "window_seed_start": int(start),
        "window_seed_end": int(start + n_windows - 1),
        "fixed_nda_errors": int(fixed_nda),
        "fixed_da_errors": int(fixed_da),
        "selected_errors": int(selected_errors),
        "n_select_da": int(n_select_da),
        "n_select_nda": int(n_select_nda),
        "lower_count_bound_errors": int(lower_bound),
        "true_oracle_errors": int(true_oracle_errors),
        "true_oracle_bits": int(true_oracle_bits),
        "mean_clipping_rate": float(np.mean(pw_clipping)),
        "mean_code_utilization": float(np.mean(pw_code_util)),
        "mean_gain": float(np.mean(pw_gain)),
        "per_window_da_err": pw_da_err,
        "per_window_nda_err": pw_nda_err,
        "per_window_clipping": pw_clipping,
        "per_window_code_util": pw_code_util,
        "per_window_gain": pw_gain,
        "agc_state": agc.state_summary(),
    }
    if return_gain_trace:
        out["_gain_trace"] = pw_gain
    return out
