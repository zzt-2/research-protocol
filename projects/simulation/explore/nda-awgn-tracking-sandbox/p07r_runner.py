# -*- coding: utf-8 -*-
"""P07-R — CORRECTED runner: gain-aware ADC + stateful trajectory + four-way decomp.

Combines:
  - p07r_adapters.quantize_iq_gainaware / decomp_*  (H1 SCALE fix)
  - p07r_adapters gain-aware AGCs (corrected incremental form, H2 CONTROL fix)
  - p07r_trajectory.generate_trajectory (shared stateful AR(1) GG, H3 fix)

Cell evaluation drives one AGC over the shared trajectory, applying the ADC to
each window's rx_raw and feeding q/g (NOT q) to the frozen receiver. All methods
share the IDENTICAL trajectory (TL-13 channel sharing).

Four-way decomposition (task section VI) is supported via the `decomp` kwarg:
  scale_only / clip_only / quant_only / full_adc  -- isolates each impairment.
"""
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
sys.path[:0] = [_SIM_ROOT, os.path.join(_SIM_ROOT, 'simulator'), _HERE]

import _b11_params as P  # noqa: E402
import _a4_switch_common768_30seed as A  # noqa: E402
import sc_nda_ml_sim as S  # noqa: E402
from common import amp_limit, mmse_equalize  # noqa: E402

import p07r_adapters as AD  # noqa: E402
import p07r_trajectory as TR  # noqa: E402

N_WINDOWS = 400
SCENES = ("weak", "moderate", "strong")
SNR_DB = (5.0, 9.0, 13.0, 17.0, 21.0)
# P06-precedent rho levels via f_G in {30,100,1000} Hz at window_dt=56us
F_G_LEVELS = (30.0, 100.0, 1000.0)
WINDOW_DT = 56e-6   # AGC update interval (P06 parity); rho spans 0.99/0.97/0.70


def _receiver_on(rx_in, win, gl_true, gamma_db):
    """Frozen receiver on the receiver-INPUT (q/g, scale restored)."""
    hb = S.estimate_h_blind_perblock(rx_in, gl_true)
    hp = S.estimate_h_pilot_perblock(rx_in, win["tx"], gl_true)
    blind = amp_limit(mmse_equalize(rx_in, hb, gl_true), 3.0)
    pilot = amp_limit(mmse_equalize(rx_in, hp, gl_true), 3.0)
    nn, nd, nc = A.per_block(blind, pilot, win["bits"], win["tx"])
    choice = A.decide(rx_in, gamma_db, gl_true)
    trueh = amp_limit(mmse_equalize(rx_in, win["h"], gl_true), 3.0)
    no, nob = S.ber_oracle_turb(trueh, win["bits"], win["phi"])
    return {"nn": int(nn), "nd": int(nd), "nc": int(nc),
            "choice": choice, "oracle_err": int(no), "oracle_bits": int(nob)}


def _apply_adc(rx_raw, gain_b, fs, W, decomp="full_adc"):
    """Apply the chosen ADC decomposition; return (rx_in, rail_r, rail_i, clip)."""
    if decomp == "full_adc":
        rx_in, cr, ci, rr, ri, step = AD.quantize_iq_gainaware(rx_raw, gain_b, fs, W)
        return rx_in, rr, ri
    if decomp == "scale_only":
        rx_in, rr, ri, _ = AD.decomp_scale_only(rx_raw, gain_b)
        return rx_in, rr, ri
    if decomp == "clip_only":
        rx_in, rr, ri, _ = AD.decomp_clip_only(rx_raw, gain_b, fs)
        return rx_in, rr, ri
    if decomp == "quant_only":
        rx_in, rr, ri, _ = AD.decomp_quant_only(rx_raw, gain_b,
                                                AD.FLOAT_BYPASS_FS, AD.FLOAT_BYPASS_W)
        return rx_in, rr, ri
    raise ValueError(f"unknown decomp {decomp!r}")


def eval_cell_agc(traj_windows, gamma_db, agc, fs, W, decomp="full_adc",
                  n_windows=N_WINDOWS):
    """Drive one AGC over the SHARED trajectory; return per-cell aggregates.

    The AGC observes the past RECEIVER-INPUT window (q/g, scale restored) and
    decides the next gain causally. Frozen receiver runs on q/g each window.
    """
    gl_true = 10.0 ** (gamma_db / 10.0)
    agc.reset()
    sel = da = nda = lb = orc_e = orc_b = n_da = n_nda = 0
    clp = []; util = []; gains = []
    for w in traj_windows[:n_windows]:
        gain_b = agc.gain_for_next()
        gains.append(float(gain_b))
        rx_in, rr, ri = _apply_adc(w["rx_raw"], gain_b, fs, W, decomp)
        rail = rr | ri
        clp.append(float(np.mean(rail)))
        codes = np.concatenate([rr.astype(np.int64), ri.astype(np.int64)]) if False else None
        out = _receiver_on(rx_in, w, gl_true, gamma_db)
        da += out["nd"]; nda += out["nc"]; lb += min(out["nd"], out["nc"])
        orc_e += out["oracle_err"]; orc_b += out["oracle_bits"]
        if out["choice"] == "da":
            n_da += 1; sel += out["nd"]
        else:
            n_nda += 1; sel += out["nc"]
        # AGC observes past receiver-input window (causal) + rail flags
        try:
            agc.update(rx_in, rail_past=(rr, ri))
        except TypeError:
            agc.update(rx_in)
    return {
        "agc_name": agc.name, "W": int(W), "fs": float(fs), "decomp": decomp,
        "n_windows": int(min(n_windows, len(traj_windows))),
        "selected_errors": int(sel), "fixed_da_errors": int(da),
        "fixed_nda_errors": int(nda), "lower_count_bound_errors": int(lb),
        "true_oracle_errors": int(orc_e), "true_oracle_bits": int(orc_b),
        "n_select_da": int(n_da), "n_select_nda": int(n_nda),
        "mean_clipping_rate": float(np.mean(clp)) if clp else 0.0,
        "mean_gain": float(np.mean(gains)) if gains else 0.0,
    }


def eval_cell_fixed_gains(traj_windows, gamma_db, configs, n_windows=N_WINDOWS):
    """Evaluate many fixed (gain, W, decomp) configs on ONE shared trajectory.

    configs: list of dicts {gain, W, fs, decomp, tag}. tag "ideal_float" is the
    gain-aware float reference (decomp=scale_only, g=1, W=64).
    """
    gl_true = 10.0 ** (gamma_db / 10.0)
    acc = {c["tag"]: {"sel": 0, "da": 0, "nda": 0, "lb": 0, "orc_e": 0, "orc_b": 0,
                      "n_da": 0, "n_nda": 0, "clp": []} for c in configs}
    for w in traj_windows[:n_windows]:
        for c in configs:
            rx_in, rr, ri = _apply_adc(w["rx_raw"], c["gain"], c["fs"],
                                       c["W"], c.get("decomp", "full_adc"))
            rail = rr | ri
            out = _receiver_on(rx_in, w, gl_true, gamma_db)
            a = acc[c["tag"]]
            a["da"] += out["nd"]; a["nda"] += out["nc"]; a["lb"] += min(out["nd"], out["nc"])
            a["orc_e"] += out["oracle_err"]; a["orc_b"] += out["oracle_bits"]
            if out["choice"] == "da":
                a["n_da"] += 1; a["sel"] += out["nd"]
            else:
                a["n_nda"] += 1; a["sel"] += out["nc"]
            a["clp"].append(float(np.mean(rail)))
    result = {}
    for c in configs:
        a = acc[c["tag"]]
        result[c["tag"]] = {
            "tag": c["tag"], "gain": float(c["gain"]), "W": int(c["W"]),
            "fs": float(c["fs"]), "decomp": c.get("decomp", "full_adc"),
            "n_windows": int(min(n_windows, len(traj_windows))),
            "selected_errors": int(a["sel"]), "fixed_da_errors": int(a["da"]),
            "fixed_nda_errors": int(a["nda"]), "lower_count_bound_errors": int(a["lb"]),
            "true_oracle_errors": int(a["orc_e"]), "true_oracle_bits": int(a["orc_b"]),
            "n_select_da": int(a["n_da"]), "n_select_nda": int(a["n_nda"]),
            "mean_clipping_rate": float(np.mean(a["clp"])) if a["clp"] else 0.0,
        }
    return result


def make_trajectory(scene, gamma_db, f_G, seed, n_windows=N_WINDOWS):
    """Build a shared stateful trajectory for one (scene, gamma, f_G, seed) cell."""
    gl_true = 10.0 ** (gamma_db / 10.0)
    wins, meta = TR.generate_trajectory(n_windows, scene, gl_true, f_G,
                                        WINDOW_DT, P.N_DFT, mod="m16apsk",
                                        seed=seed)
    return wins, meta
