# -*- coding: utf-8 -*-
"""P01 — CPR selector SNR-mismatch robustness probe (Phase A).

Goal (Task Brief T028-p01):
  - Phase A.1: reproduce the frozen anchor `ccisp_family1_selector_a_30seed.json`
    per-seed selected_errors + branch occupancy exactly (dev seeds 0-9).
  - Phase A.2-5: inject a biased nominal SNR held by the receiver,
        gamma_hat_dB = gamma_true_dB + delta, delta in {-3,-2,-1,0,+1,+2,+3} dB,
    and measure how the *original* DA/NDA selector behaves under this mismatch.

KEY DISCIPLINE (do not violate):
  - The signal is generated with TRUE gamma (generate_shared_realization_apsk(gl=true)).
  - The selector's decide() is fed the BIASED gamma_hat. TRUE gamma NEVER enters decide().
  - Offline BER evaluation of the DA branch / NDA branch uses the TRUE channel
    equalizer (true h, true phi) only to measure error counts; the branch *choice*
    is dictated by the biased gamma_hat.
  - Channel must use generate_shared_realization_apsk (TL-13 shared channel).
  - Do NOT modify common/, params.py, or the original selector _a4_switch_common768_30seed.py.
  - Reproduction: with delta=0 the probe MUST reproduce the anchor's
    selected_errors, n_select_da/nda per seed exactly.

The probe mirrors run_ccisp_family1_selector_a_30seed.py::run_case line-for-line for the
delta=0 path (so reproduction is byte-exact), then extends to biased gamma_hat and
records branch outputs / counts needed for the harm analysis.
"""
import os
import sys
import hashlib
from pathlib import Path

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_EXP = _HERE
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
sys.path[:0] = [_SIM_ROOT, os.path.join(_SIM_ROOT, 'simulator'), _EXP]

import _b11_params as P  # noqa: E402
import _a4_switch_common768_30seed as A  # noqa: E402  (frozen selector, do not modify)
import _a4_branchrouted_30seed as B  # noqa: E402
import sc_nda_ml_sim as S  # noqa: E402
from common import (  # noqa: E402
    amp_limit, mmse_equalize, generate_shared_realization_apsk,
)
from params import SimulationConfig  # noqa: E402

N_WINDOWS = 400
SCENES = ("weak", "moderate", "strong")
SNR_DB = tuple(map(float, range(5, 26, 2)))   # 5..25 dB, matches anchor
DELTAS = (-3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0)

# Hooks for pilot-based adapter/candidates (set by Phase B/C runner). Defaults are
# no-ops so reproduction (_p01_repro_check) and smoke (_p01_smoke_check) work
# without importing the adapter module (which depends on pilots).
_SET_PILOTS = lambda tx: None     # publish pilot tx symbols for the current window
_ADAPTER_RESET = None             # reset stateful selectors (e.g. hysteresis EMA)
_PILOTS_AVAILABLE = False         # True once an adapter import wires _SET_PILOTS


def wire_pilot_hooks(set_pilots_fn, reset_fn=None):
    """Called by Phase B/C runner to enable pilot-based selectors in the multidelta loop."""
    global _SET_PILOTS, _ADAPTER_RESET, _PILOTS_AVAILABLE
    _SET_PILOTS = set_pilots_fn
    _ADAPTER_RESET = reset_fn
    _PILOTS_AVAILABLE = True


# ----------------------------------------------------------------------
# Per-block receiver outputs (mirror run_ccisp_family1_selector_a_30seed.py exactly)
# ----------------------------------------------------------------------
def per_block_nda_receiver_output(rx_blind, bits):
    """Return NDA receiver output + post-hoc BER counts (all-1024 and common-768)."""
    omega = B.S.fft_foe_m0_omega(rx_blind, B.P.M0)
    k = np.arange(B.P.N_DFT)
    rc_nda, _, _, _ = B.nda_ml_recovery(rx_blind * np.exp(-1j * omega * k),
                                        B.P.M0, mod="m16apsk", assume_df_zero=True)
    tb = bits[:B.P.N_DFT * B.P.BITS_PER_SYM]
    resolved = B.resolve_m16apsk_blockwise(rc_nda, tb, block_size=B.P.BLOCK_SIZE_RESOLVE)
    dm = B.m16apsk_demod(resolved)
    ne_all = int(np.sum(tb != dm))
    pidx = np.arange(0, B.P.N_DFT, B.P.DA_PILOT_SPACING)
    is_data = np.ones(B.P.N_DFT, dtype=bool)
    is_data[pidx] = False
    ne_common = int(np.sum(tb.reshape(B.P.N_DFT, B.P.BITS_PER_SYM)[is_data]
                           != dm.reshape(B.P.N_DFT, B.P.BITS_PER_SYM)[is_data]))
    return ne_all, ne_common, rc_nda


def run_case_mismatch(scene, gamma_true_db, delta, seed_index,
                      n_windows=N_WINDOWS):
    """Run one (scene, gamma_true, delta, seed) cell.

    - gamma_true_db: TRUE SNR used to generate the signal + offline BER eval.
    - delta: receiver SNR bias (gamma_hat_dB = gamma_true_dB + delta).
    - The selector sees gamma_hat only.

    Reproduces the anchor exactly when delta=0 (verified 120/120 cells).
    """
    cfg = SimulationConfig()
    gl_true = 10 ** (gamma_true_db / 10)
    gamma_hat_db = gamma_true_db + delta
    gamma_hat_lin = 10 ** (gamma_hat_db / 10)
    start = P.SEED_TURB0 + seed_index * N_WINDOWS

    c = {
        "fixed_nda_errors": 0,        # NDA common-768 errors (true channel)
        "fixed_da_errors": 0,         # DA common-768 errors   (true channel)
        "selected_errors": 0,         # errors on the branch the (biased) selector picked
        "lower_count_bound_errors": 0,
        "true_oracle_errors": 0,
        "true_oracle_bits": 0,
        "n_select_da": 0,
        "n_select_nda": 0,
    }
    for b in range(n_windows):
        ws = start + b
        r = generate_shared_realization_apsk(P.N_DFT, gl_true, scene,
                                             cfg.doppler.DOPPLER_HIGH,
                                             mod="m16apsk", seed=ws)
        raw, bits, tx = r["rx_raw"], r["bits"], r["tx"]

        # ----- TRUE-channel receivers (only for offline BER eval) -----
        hb = S.estimate_h_blind_perblock(raw, gl_true)   # NDA uses blind estimate
        hp = S.estimate_h_pilot_perblock(raw, tx, gl_true)  # DA uses pilot estimate
        blind = amp_limit(mmse_equalize(raw, hb, gl_true), 3.0)
        pilot = amp_limit(mmse_equalize(raw, hp, gl_true), 3.0)
        nn, nd, nc = A.per_block(blind, pilot, bits, tx)  # nn=all-1024, nd=DA common768, nc=NDA common768

        # ----- selector CHOICE driven by BIASED gamma_hat (never true gamma) -----
        choice = A.decide(raw, gamma_hat_db, gamma_hat_lin)

        # ----- true-oracle reference (same as anchor) -----
        trueh = amp_limit(mmse_equalize(raw, r["h"], gl_true), 3.0)
        no, nob = S.ber_oracle_turb(trueh, bits, r["phi"])
        c["true_oracle_errors"] += no
        c["true_oracle_bits"] += nob

        # ----- accumulate -----
        c["fixed_nda_errors"] += nc
        c["fixed_da_errors"] += nd
        c["lower_count_bound_errors"] += min(nc, nd)
        c["selected_errors"] += nd if choice == "da" else nc
        c["n_select_" + choice] += 1

    return {
        "key": f"{scene}|{gamma_true_db:g}|{delta:+g}|{seed_index}",
        "scene": scene,
        "gamma_true_db": float(gamma_true_db),
        "delta_db": float(delta),
        "gamma_hat_db": float(gamma_hat_db),
        "seed_index": int(seed_index),
        "n_windows": int(n_windows),
        "n_bits_common768": int(n_windows * 768),
        "window_seed_start": int(start),
        "window_seed_end": int(start + n_windows - 1),
        "fixed_nda_errors": int(c["fixed_nda_errors"]),       # NDA common-768
        "fixed_da_errors": int(c["fixed_da_errors"]),         # DA common-768
        "selected_errors": int(c["selected_errors"]),         # branch chosen by biased selector
        "lower_count_bound_errors": int(c["lower_count_bound_errors"]),
        "true_oracle_errors": int(c["true_oracle_errors"]),
        "true_oracle_bits": int(c["true_oracle_bits"]),
        "n_select_da": int(c["n_select_da"]),
        "n_select_nda": int(c["n_select_nda"]),
    }


# ----------------------------------------------------------------------
# Fast multi-delta runner: generate channel ONCE per (scene, gamma_true, seed),
# evaluate DA/NDA common-768 errors per window, then apply selector under every
# delta. Identical result to run_case_mismatch per delta, but ~7x faster.
# ----------------------------------------------------------------------
def run_case_multidelta(scene, gamma_true_db, seed_index, deltas=DELTAS,
                        n_windows=N_WINDOWS, extra_selector=None):
    """Run one (scene, gamma_true, seed) cell across all deltas.

    Returns:
      base = {fixed_nda_errors, fixed_da_errors, lower_count_bound_errors,
              true_oracle_errors, true_oracle_bits, n_windows, per_window_da_err, per_window_nda_err}
        (channel-dependent, delta-independent)
      per_delta[delta] = {n_select_da, n_select_nda, selected_errors,
                          choices (list of 'da'/'nda' in window order)}
      If extra_selector is given, also evaluate that selector's per-window choice
      under each delta (for adapter/candidate comparison). Returns
      per_delta_extra[name][delta] = same dict.
    """
    cfg = SimulationConfig()
    gl_true = 10 ** (gamma_true_db / 10)
    start = P.SEED_TURB0 + seed_index * N_WINDOWS

    fixed_nda = 0           # NDA common-768 cumulative
    fixed_da = 0            # DA common-768 cumulative
    lower_bound = 0
    true_oracle_errors = 0
    true_oracle_bits = 0
    pw_da_err = np.empty(n_windows, dtype=np.int64)   # per-window DA common-768 errors
    pw_nda_err = np.empty(n_windows, dtype=np.int64)  # per-window NDA common-768 errors
    pw_raw = []            # per-window raw rx (re-used for selector decisions across deltas)
    pw_tx = []             # per-window tx symbols (for pilot-based adapter/candidates)

    for b in range(n_windows):
        ws = start + b
        r = generate_shared_realization_apsk(P.N_DFT, gl_true, scene,
                                             cfg.doppler.DOPPLER_HIGH,
                                             mod="m16apsk", seed=ws)
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
        "per_window_da_err": pw_da_err,
        "per_window_nda_err": pw_nda_err,
    }

    def _eval_selector(decide_fn, name, needs_pilot=False, needs_reset=False):
        per_delta = {}
        for delta in deltas:
            g_hat_db = gamma_true_db + delta
            g_hat_lin = 10 ** (g_hat_db / 10)
            choices = []
            sel_err = 0
            n_da = n_nda = 0
            if needs_reset and _ADAPTER_RESET is not None:
                _ADAPTER_RESET()
            for b in range(n_windows):
                if needs_pilot:
                    _SET_PILOTS(pw_tx[b])
                ch = decide_fn(pw_raw[b], g_hat_db, g_hat_lin, b)
                choices.append(ch)
                if ch == "da":
                    n_da += 1
                    sel_err += int(pw_da_err[b])
                else:
                    n_nda += 1
                    sel_err += int(pw_nda_err[b])
            per_delta[delta] = {
                "n_select_da": int(n_da),
                "n_select_nda": int(n_nda),
                "selected_errors": int(sel_err),
                "choices": choices,
            }
        return per_delta

    per_delta_orig = _eval_selector(_decide_original, "orig")
    out = {"base": base, "per_delta_orig": per_delta_orig}
    if extra_selector is not None:
        out["per_delta_extra"] = {}
        for name, spec in extra_selector.items():
            # spec is either a bare decide_fn (legacy) or a dict with metadata
            if callable(spec):
                fn = spec
                meta = {"needs_pilot": _PILOTS_AVAILABLE, "needs_reset": False}
            else:
                fn = spec["fn"]
                meta = {"needs_pilot": spec.get("needs_pilot", _PILOTS_AVAILABLE),
                        "needs_reset": spec.get("needs_reset", False)}
            out["per_delta_extra"][name] = _eval_selector(
                fn, name, needs_pilot=meta["needs_pilot"], needs_reset=meta["needs_reset"])
    return out


def _decide_original(raw, gamma_db, gamma_lin, b):
    """Wrap A.decide to the (raw, gamma_db, gamma_lin) signature used by _eval_selector."""
    return A.decide(raw, gamma_db, gamma_lin)
