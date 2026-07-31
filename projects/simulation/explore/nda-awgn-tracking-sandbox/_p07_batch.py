# -*- coding: utf-8 -*-
"""P07 — BATCHED per-cell evaluator (one channel generation per cell).

For Phase A we evaluate MANY (gain, W) configs on the SAME channel realization
per (scene, g, seed). The channel generation (generate_shared_realization_apsk)
is the dominant cost, so batching configs per cell gives a large speedup with
NO scientific change: every config still sees the identical channel + selector.

This mirrors P03's batched extra_selector pattern. The receiver math
(estimate_h_blind/pilot_perblock, amp_limit, mmse_equalize, A.per_block,
A.decide, S.ber_oracle_turb) is called UNCHANGED per config — but only on the
quantized raw, and the float raw is computed once and reused for the ideal
reference.

Float-bypass identity is preserved: the (gain=1, W=64, fs=large) config in the
batch reproduces the float receiver byte-exactly (Phase-0 G3 guarantees this).
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
from common import (  # noqa: E402
    amp_limit, mmse_equalize, generate_shared_realization_apsk,
)
from params import SimulationConfig  # noqa: E402

import _p07_adapters as AD  # noqa: E402

N_WINDOWS = 400


def _receiver_on_raw(raw, bits, tx, r, gl_true, gamma_db):
    """Run the full frozen receiver on `raw` for one window; return dict."""
    hb = S.estimate_h_blind_perblock(raw, gl_true)
    hp = S.estimate_h_pilot_perblock(raw, tx, gl_true)
    blind = amp_limit(mmse_equalize(raw, hb, gl_true), 3.0)
    pilot = amp_limit(mmse_equalize(raw, hp, gl_true), 3.0)
    nn, nd, nc = A.per_block(blind, pilot, bits, tx)
    choice = A.decide(raw, gamma_db, gl_true)
    trueh = amp_limit(mmse_equalize(raw, r["h"], gl_true), 3.0)
    no, nob = S.ber_oracle_turb(trueh, bits, r["phi"])
    return {"nn": int(nn), "nd": int(nd), "nc": int(nc),
            "choice": choice, "oracle_err": int(no), "oracle_bits": int(nob)}


def eval_cell_fixed_gains(scene, gamma_true_db, seed, configs, n_windows=N_WINDOWS):
    """Evaluate many (gain, W, fs) configs on ONE channel realization.

    Parameters
    ----------
    configs : list of dicts [{"gain":g, "W":W, "fs":fs, "tag":str}, ...].
        The tag "ideal_float" is reserved for (gain=1, W=64, fs=1e6) reference.

    Returns
    -------
    dict: per-config aggregates + per-config per-window traces.
    Each config shares the IDENTICAL channel realization (same window seeds).
    """
    cfg = SimulationConfig()
    gl_true = 10 ** (gamma_true_db / 10)
    start = P.SEED_TURB0 + seed * N_WINDOWS

    # per-config accumulators
    acc = {c["tag"]: {"sel": 0, "da": 0, "nda": 0, "lb": 0,
                      "orc_e": 0, "orc_b": 0, "n_da": 0, "n_nda": 0,
                      "clp": [], "util": []}
           for c in configs}

    for b in range(n_windows):
        ws = start + b
        r = generate_shared_realization_apsk(P.N_DFT, gl_true, scene,
                                             cfg.doppler.DOPPLER_HIGH,
                                             mod="m16apsk", seed=ws)
        raw_float, bits, tx = r["rx_raw"], r["bits"], r["tx"]
        for c in configs:
            q, cr, ci, rr, ri = AD.quantize_iq(raw_float, c["gain"], c["fs"], c["W"])
            rail = rr | ri
            out = _receiver_on_raw(q, bits, tx, r, gl_true, gamma_true_db)
            a = acc[c["tag"]]
            a["da"] += out["nd"]
            a["nda"] += out["nc"]
            a["lb"] += min(out["nd"], out["nc"])
            a["orc_e"] += out["oracle_err"]
            a["orc_b"] += out["oracle_bits"]
            if out["choice"] == "da":
                a["n_da"] += 1
                a["sel"] += out["nd"]
            else:
                a["n_nda"] += 1
                a["sel"] += out["nc"]
            a["clp"].append(float(np.mean(rail)))
            a["util"].append(float(len(np.unique(np.concatenate([cr, ci]))) / (2 ** c["W"])))

    result = {}
    for c in configs:
        a = acc[c["tag"]]
        result[c["tag"]] = {
            "scene": scene, "gamma_true_db": float(gamma_true_db),
            "seed": int(seed), "tag": c["tag"], "gain": float(c["gain"]),
            "W": int(c["W"]), "fs": float(c["fs"]),
            "n_windows": int(n_windows),
            "selected_errors": int(a["sel"]),
            "fixed_da_errors": int(a["da"]),
            "fixed_nda_errors": int(a["nda"]),
            "lower_count_bound_errors": int(a["lb"]),
            "true_oracle_errors": int(a["orc_e"]),
            "true_oracle_bits": int(a["orc_b"]),
            "n_select_da": int(a["n_da"]),
            "n_select_nda": int(a["n_nda"]),
            "mean_clipping_rate": float(np.mean(a["clp"])),
            "mean_code_utilization": float(np.mean(a["util"])),
        }
    return result


def eval_cell_agc(scene, gamma_true_db, seed, agc_specs, W, fs, n_windows=N_WINDOWS):
    """Evaluate many causal-AGC configs on ONE channel realization.

    agc_specs : list of (tag, agc_factory) where agc_factory() returns a fresh
    _BaseAGC instance. gain for window b is decided from windows < b across all
    windows; each AGC is independent (own state).

    Returns dict per-tag (same schema as eval_cell_fixed_gains).
    """
    cfg = SimulationConfig()
    gl_true = 10 ** (gamma_true_db / 10)
    start = P.SEED_TURB0 + seed * n_windows

    agcs = [(tag, fac()) for tag, fac in agc_specs]
    for _, agc in agcs:
        agc.reset()

    acc = {tag: {"sel": 0, "da": 0, "nda": 0, "lb": 0,
                 "orc_e": 0, "orc_b": 0, "n_da": 0, "n_nda": 0,
                 "clp": [], "util": [], "gains": []}
           for tag, _ in agcs}

    for b in range(n_windows):
        ws = start + b
        r = generate_shared_realization_apsk(P.N_DFT, gl_true, scene,
                                             cfg.doppler.DOPPLER_HIGH,
                                             mod="m16apsk", seed=ws)
        raw_float, bits, tx = r["rx_raw"], r["bits"], r["tx"]
        for tag, agc in agcs:
            gain_b = agc.gain_for_next()
            q, cr, ci, rr, ri = AD.quantize_iq(raw_float, gain_b, fs, W)
            rail = rr | ri
            out = _receiver_on_raw(q, bits, tx, r, gl_true, gamma_true_db)
            a = acc[tag]
            a["da"] += out["nd"]; a["nda"] += out["nc"]
            a["lb"] += min(out["nd"], out["nc"])
            a["orc_e"] += out["oracle_err"]; a["orc_b"] += out["oracle_bits"]
            if out["choice"] == "da":
                a["n_da"] += 1; a["sel"] += out["nd"]
            else:
                a["n_nda"] += 1; a["sel"] += out["nc"]
            a["clp"].append(float(np.mean(rail)))
            a["util"].append(float(len(np.unique(np.concatenate([cr, ci]))) / (2 ** W)))
            a["gains"].append(float(gain_b))
            # AGC observes the past quantized window for NEXT decision
            if hasattr(agc, 'update'):
                try:
                    agc.update(q, rail_past=rail)
                except TypeError:
                    agc.update(q)

    result = {}
    for tag, agc in agcs:
        a = acc[tag]
        result[tag] = {
            "scene": scene, "gamma_true_db": float(gamma_true_db),
            "seed": int(seed), "tag": tag, "agc_name": agc.name,
            "W": int(W), "fs": float(fs), "n_windows": int(n_windows),
            "selected_errors": int(a["sel"]),
            "fixed_da_errors": int(a["da"]), "fixed_nda_errors": int(a["nda"]),
            "lower_count_bound_errors": int(a["lb"]),
            "true_oracle_errors": int(a["orc_e"]),
            "true_oracle_bits": int(a["orc_b"]),
            "n_select_da": int(a["n_da"]), "n_select_nda": int(a["n_nda"]),
            "mean_clipping_rate": float(np.mean(a["clp"])),
            "mean_code_utilization": float(np.mean(a["util"])),
            "mean_gain": float(np.mean(a["gains"])),
        }
    return result
