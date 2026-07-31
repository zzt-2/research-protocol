# -*- coding: utf-8 -*-
"""P07-R — unit verification of the CORRECTED adapter (before any rerun).

Verifies the H1 SCALE fix (gain->de-gain identity, scale-restore to the real
frozen receiver) and the H2 CONTROL fix (incremental AGC fixed-point / no
period-2 / correct target). These are the unit gates the corrected chain must
pass BEFORE the full fresh-seed rerun.

Gates:
  U1 identity (no clip no quant): decomp_scale_only(z,g) == z for any g
  U2 scale-restore to receiver: at gain!=1 with WIDE rails + fine ADC, the
      corrected chain (q/g) reproduces the g=1 reference receiver outputs
      (selected_errors / branch / oracle) -- the H1 fix.
  U3 four-way decomp primitives each isolate their impairment:
      scale_only == float reference; clip_only only clips; quant_only only
      rounds; full_adc == clip+quant.
  U4 corrected causal-RMS fixed point: constant input -> g converges to
      target/r0 (the INPUT-scale fixed point), no period-2.
  U5 attack-release converges, log-domain stable.
"""
import os
import sys
import json
import time

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

import p07r_adapters as AD  # noqa: E402  CORRECTED chain

OUT_DIR = os.path.join(_SIM_ROOT, "results", "p07r_agc_adc_repair")
OUT = os.path.join(OUT_DIR, "p07r_unit_verify.json")


def _receiver(raw, bits, tx, r, gl_true, gamma_db):
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


def gate_U1_identity():
    """decomp_scale_only(z,g) == z for any g (no clip, no quant)."""
    np.random.seed(1)
    z = (np.random.randn(1024) + 1j * np.random.randn(1024))
    maxerr = 0.0
    for g in (0.125, 0.5, 1.0, 2.0, 4.0, 8.0):
        rx_in, *_ = AD.decomp_scale_only(z, g)
        maxerr = max(maxerr, float(np.max(np.abs(rx_in - z))))
    return {"max_abs_err_vs_z": maxerr, "pass": bool(maxerr <= 1e-12)}


def gate_U2_scale_restore_to_receiver():
    """CORRECTED chain q/g reproduces g=1 reference at gain!=1 (H1 fix).

    Uses WIDE rails (FS=1e6) + fine ADC (W=64) so quant/clip are negligible;
    then the corrected chain must match the untouched-float reference exactly.
    """
    cfg = SimulationConfig()
    gl_true = 10.0 ** (9.0 / 10)
    gamma_db = 9.0
    r = generate_shared_realization_apsk(P.N_DFT, gl_true, "weak",
                                         cfg.doppler.DOPPLER_HIGH,
                                         mod="m16apsk", seed=2024)
    z, bits, tx = r["rx_raw"], r["bits"], r["tx"]
    ref = _receiver(z, bits, tx, r, gl_true, gamma_db)
    res = {}
    all_match = True
    for g in (0.5, 0.75, 1.5, 2.0, 3.0):
        rx_in, *_ = AD.quantize_iq_gainaware(z, g, AD.FLOAT_BYPASS_FS, AD.FLOAT_BYPASS_W)
        out = _receiver(rx_in, bits, tx, r, gl_true, gamma_db)
        match = (out["nd"] == ref["nd"] and out["nc"] == ref["nc"]
                 and out["choice"] == ref["choice"]
                 and out["oracle_err"] == ref["oracle_err"])
        res[f"g={g}"] = {"nd": out["nd"], "nc": out["nc"],
                         "choice": out["choice"], "oracle": out["oracle_err"],
                         "matches_ref": match}
        all_match = all_match and match
    res["ref"] = ref
    res["pass"] = bool(all_match)
    return res


def gate_U3_fourway_isolation():
    """scale_only == float; clip_only clips but no rounding; quant_only rounds
    but no clipping; full_adc = clip+quant."""
    np.random.seed(2)
    N = 2048
    z = 0.6 * (np.random.randn(N) + 1j * np.random.randn(N))
    g, fs, W = 2.0, 1.0, 6
    sc, *_ = AD.decomp_scale_only(z, g)
    cl, rrc, rri, _ = AD.decomp_clip_only(z, g, fs)
    qu, rrq, rriq, _ = AD.decomp_quant_only(z, g, AD.FLOAT_BYPASS_FS, AD.FLOAT_BYPASS_W)
    fu, crf, cif, rrf, rrif, stepf = AD.decomp_full_adc(z, g, fs, W)
    return {
        "scale_only_max_err_vs_z": float(np.max(np.abs(sc - z))),
        "scale_only_pass": bool(np.max(np.abs(sc - z)) <= 1e-12),
        "clip_only_any_clip": bool(np.any(rrc | rri)),
        "quant_only_wide_no_clip": bool(not np.any(rrq | rriq)),
        "quant_only_has_rounding": bool(np.max(np.abs(qu - z)) > 0),
        "full_adc_has_clip_and_round": bool(np.any(rrf | rrif) and np.max(np.abs(fu - z)) > 0),
        "pass": bool(np.max(np.abs(sc - z)) <= 1e-12
                     and np.any(rrc | rri)
                     and not np.any(rrq | rriq)
                     and np.max(np.abs(qu - z)) > 0
                     and (np.any(rrf | rrif) and np.max(np.abs(fu - z)) > 0)),
    }


def _drive(agc, r0, n=400, N=1024, fs=AD.FS, W=64):
    agc.reset()
    gains = np.empty(n)
    for b in range(n):
        g = agc.gain_for_next()
        gains[b] = g
        const = (r0 + 1j * r0) * np.ones(N) / np.sqrt(2)
        rx_in, cr, ci, rr, ri, step = AD.quantize_iq_gainaware(const, g, fs, W)
        rail = rr | ri
        try:
            agc.update(rx_in, rail_past=(rr, ri))
        except TypeError:
            try:
                agc.update(rx_in, rail_past=rail)
            except TypeError:
                agc.update(rx_in)
    return gains


def gate_U4_causal_rms_fixedpoint():
    """Constant input -> corrected causal-RMS converges to the INPUT-scale
    fixed point target/rms_perIQ, no period-2.

    const = (r0+1j*r0)/sqrt(2) -> per-I/Q rms = r0/sqrt(2). The AGC measures
    pwr = (mean(re^2)+mean(im^2))/2 = r0^2/2 -> rms = r0/sqrt(2). So the correct
    INPUT-scale fixed point is g_fp = target / (r0/sqrt(2)) = target*sqrt(2)/r0.
    """
    r0 = 0.25
    target = AD.TARGET_RMS
    rms_perIQ = r0 / np.sqrt(2)
    expected_fp = target / rms_perIQ   # INPUT-scale fixed point (H2 fix)
    agc = AD.CausalRMSAGC(target_rms=target, lam=0.9, blend=1.0)
    gains = _drive(agc, r0)
    tail = gains[100:]
    ss = float(np.mean(tail))
    p2 = float(np.mean(np.abs(tail[2:] - tail[:-2])))
    p1 = float(np.mean(np.abs(tail[1:] - tail[:-1])))
    return {
        "input_r0": r0, "perIQ_rms": float(rms_perIQ), "target": target,
        "expected_fixed_point_target_over_perIQ_rms": float(expected_fp),
        "steady_state_gain": ss,
        "ss_minus_expected": float(ss - expected_fp),
        "period2_metric": p2, "period1_metric": p1,
        "pass": bool(abs(ss - expected_fp) < 0.05 and p2 < 1e-3),
    }


def gate_U5_attack_release_logdomain():
    """attack-release & log-domain converge (no divergence / no p2)."""
    r0 = 0.25
    out = {}
    for name, cls in (("attack_release", AD.AttackReleaseAGC),
                      ("log_domain", AD.LogDomainAGC)):
        agc = cls()
        gains = _drive(agc, r0)
        tail = gains[100:]
        out[name] = {
            "steady_state_gain": float(np.mean(tail)),
            "period2_metric": float(np.mean(np.abs(tail[2:] - tail[:-2]))),
            "bounded": bool(np.all(np.isfinite(tail))),
        }
    out["pass"] = bool(all(v["bounded"] and v["period2_metric"] < 1e-2 for v in out.values()))
    return out


def main():
    t0 = time.time()
    os.makedirs(OUT_DIR, exist_ok=True)
    gates = {
        "U1_identity": gate_U1_identity(),
        "U2_scale_restore_to_receiver": gate_U2_scale_restore_to_receiver(),
        "U3_fourway_isolation": gate_U3_fourway_isolation(),
        "U4_causal_rms_fixedpoint": gate_U4_causal_rms_fixedpoint(),
        "U5_attack_release_logdomain": gate_U5_attack_release_logdomain(),
    }
    all_pass = all(g.get("pass", False) for g in gates.values())
    summary = {k: v.get("pass") for k, v in gates.items()}
    print("=== P07-R UNIT VERIFY (corrected adapter) ===")
    for k, v in gates.items():
        print(f"  {k}: pass={v.get('pass')}")
    print(f"ALL PASS = {all_pass}")
    if not all_pass:
        print("!!! CORRECTED CHAIN FAILED A UNIT GATE — DO NOT PROCEED TO RERUN")
    out = {"package": "P07-R", "stage": "unit_verify_corrected_adapter",
           "all_pass": all_pass, "gates": gates,
           "summary": summary, "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"Saved -> {OUT}")


if __name__ == "__main__":
    main()
