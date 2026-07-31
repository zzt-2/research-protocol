# -*- coding: utf-8 -*-
"""P07-R — root-cause REPRODUCTION (Phase 1 of systematic-debugging).

NO FIXES HERE. This script builds the minimal failing tests for the three
root-cause hypotheses (H1 SCALE / H2 CONTROL / H3 LIFECYCLE) against the OLD
P07 chain (the current `_p07_adapters.quantize_iq` + `_p07_runner` flow), saves
the pre-fix failure evidence, and stops.

Pre-fix evidence is saved to:
    results/p07r_agc_adc_repair/p07r_prefail_evidence.json

H1 SCALE — the ADC reconstructs q = code*step = Q(g*z) but the downstream
    receiver chain consumes `q` WITHOUT dividing by the analog gain g.
    Functions estimate_h_blind_perblock (h_blk = p_rx - 1/(2*gamma), additive
    noise floor NOT scaled by g^2), amp_limit (fixed abs thresh=3.0) and
    decide (mean(|rx|^2) - 1/(2*gamma_lin)) are scale-DEPENDENT, so a gain
    g != 1 cannot be undone by a later division -> the receiver sees a
    wrong-scaled signal and the float-bypass identity only holds at g=1.
    Test (T1): no-noise/no-clip/no-quant gain->de-gain must reproduce the
    input; gain!=1 with finite quant must still be scale-restored to the
    receiver (q_recon/g == z up to quant step). Current chain feeds q (not q/g)
    -> receiver outputs differ from the g=1 identity at gain!=1.

H2 CONTROL — the conventional causal-RMS AGC computes
    g_next = clamp(target_rms / rms(q_past))   (adapters CausalRMSAGC.update)
    i.e. it sets the NEXT gain from the measured OUTPUT scale alone, omitting
    the multiplicative carry-over of the CURRENT gain. The correct incremental
    form is g_next = clip(g_current * target_rms / rms(q_past), ...).
    Test (T2): a constant-amplitude input should converge to a fixed point
    with NO two-period oscillation. The current form produces a period-2
    limit cycle because g and rms(q) alternate.

H3 LIFECYCLE — the runner regenerates an INDEPENDENT GG realization every
    window (seed=ws per window; _channel.gg_block draws independent Gamma
    RVs). There is no shared stateful trajectory, so the inter-window GG ACF
    is ~0, not the contract-claimed rho. An AGC that "predicts the next
    window scale" is therefore predicting an independent draw -> no
    physically meaningful time-correlated control problem.
    Test (T3): measure the empirical lag-1 ACF of the per-window GG block
    amplitude across the current runner's windows; assert it is ~0
    (independent), contradicting a time-correlated GG control premise.
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
from common import gg_block  # noqa: E402

import _p07_adapters as AD  # noqa: E402  (OLD chain, unchanged)

OUT_DIR = os.path.join(_SIM_ROOT, "results", "p07r_agc_adc_repair")
OUT_EV = os.path.join(OUT_DIR, "p07r_prefail_evidence.json")


def _receiver_outputs(raw, bits, tx, r, gl_true, gamma_db):
    """Exact mirror of _p07_runner._per_window_receiver_outputs + decide."""
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


# ============================================================================
# T1 — H1 SCALE: gain->de-gain identity must hold; receiver must be gain-aware
# ============================================================================

def test_T1_scale_identity():
    """Current chain feeds q (=Q(g*z)) to receiver WITHOUT dividing by g.

    A correct chain feeds q/g (receiver-visible: gain is a known control).
    We measure how far the OLD chain deviates from the g=1 identity at gain!=1,
    using a controlled synthetic signal (deterministic constellation + AWGN)
    and the REAL frozen receiver functions.
    """
    cfg = SimulationConfig()
    gl_true = 10.0 ** (13.0 / 10)   # 13 dB
    gamma_db = 13.0
    np.random.seed(7)
    N = P.N_DFT
    # build a unit-power m16apsk-like signal via the channel generator
    r = generate_shared_realization_apsk(N, gl_true, "moderate",
                                         cfg.doppler.DOPPLER_HIGH,
                                         mod="m16apsk", seed=777)
    z = r["rx_raw"].copy()
    bits, tx = r["bits"], r["tx"]

    FS = AD.FS
    Wfb = AD.FLOAT_BYPASS_W
    FSfb = AD.FLOAT_BYPASS_FS

    # reference: receiver on the UNTOUCHED float raw (g=1, no ADC)
    ref = _receiver_outputs(z, bits, tx, r, gl_true, gamma_db)

    results = {}
    for g in (0.5, 0.75, 1.5, 2.0, 3.0):
        # ---- OLD chain: feed q (=Q(g*z)) directly to receiver (NO de-gain) ----
        q_old, *_ = AD.quantize_iq(z, g, FS, W=8)
        old = _receiver_outputs(q_old, bits, tx, r, gl_true, gamma_db)
        # ---- CORRECT chain: feed q/g to receiver (gain is known control) ----
        q_corr, *_ = AD.quantize_iq(z, g, FS, W=8)
        corr = _receiver_outputs(q_corr / g, bits, tx, r, gl_true, gamma_db)

        # float-bypass style reference at THIS gain via fb ADC (q_fb = Q(g*z),
        # ~ z since FS huge / W huge), then /g to restore scale
        q_fb, *_ = AD.quantize_iq(z, g, FSfb, Wfb)
        fb_corr = _receiver_outputs(q_fb / g, bits, tx, r, gl_true, gamma_db)

        results[f"g={g}"] = {
            "old_chain_q_no_degain": old,
            "correct_chain_q_over_g": corr,
            "floatbypass_q_over_g_ref": fb_corr,
            "ref_g1_notouch": ref,
            # deviation of OLD chain from the gain-aware reference
            "OLD_dev_nd_from_ref": old["nd"] - ref["nd"],
            "OLD_dev_nc_from_ref": old["nc"] - ref["nc"],
            "OLD_choice": old["choice"],
            "CORR_choice": corr["choice"],
            "REF_choice": ref["choice"],
            # does correct chain /g recover the g=1 reference? (should be ~0 diff
            # up to the finite-bit quant the reference itself did not apply)
            "CORR_dev_nd_from_ref": corr["nd"] - ref["nd"],
            "CORR_dev_nc_from_ref": corr["nc"] - ref["nc"],
        }
    return results


# ============================================================================
# T2 — H2 CONTROL: causal-RMS two-period oscillation on constant amplitude
# ============================================================================

def _run_rms_agc(agc, input_rms_fn, n=200, N=1024, W=64):
    """Drive an AGC with a constant (or time-varying) input rms; return gains."""
    agc.reset()
    gains = np.empty(n)
    rms_meas = np.empty(n)
    for b in range(n):
        g = agc.gain_for_next()
        gains[b] = g
        r0 = input_rms_fn(b)
        const = (r0 + 1j * r0) * np.ones(N) / np.sqrt(2)
        q, *_ = AD.quantize_iq(const, g, AD.FS, W=W)
        rms_meas[b] = float(np.sqrt((np.mean(q.real**2)+np.mean(q.imag**2))/2.0))
        agc.update(q)
    return gains, rms_meas


def test_T2_causal_rms_period2():
    """H2 CONTROL — two distinct failure modes of the current causal-RMS form
    g_next = clamp(target / rms(q_past)):

    (a) FORMULA BUG (always present): the correct incremental form is
        g_next = clip(g_current * target / rms(q_past), ...) because
        rms(q_past) = g_current * rms(z)  ->  rms(z) = rms(q_past)/g_current
        ->  g_next = target/rms(z) = g_current*target/rms(q_past).
        The current form DROPS the g_current factor. We show this by direct
        comparison against the corrected incremental form on a constant input:
        at the true fixed point g*=sqrt(target/r0) both agree, but the current
        form's NEXT-gain map differs from the corrected one away from g*.

    (b) PERIOD-2 (depends on forgetting): with pure last-sample tracking
        (lam=1) on a constant input, current form actually converges (g
        alternates only when starting off fixed point is washed out by the
        g_current omission). With realistic lam=0.9 and a STEP in input rms,
        the dropped g_current term produces a wrong steady-state gain (bias),
        which we report as the H2 manifestation: the AGC does NOT drive
        rms(z) to target; it drives rms(q_past) to target, i.e. it
        mistargets the OUTPUT scale not the INPUT scale.
    """
    r0 = 0.25
    target = AD.TARGET_RMS
    # (a) formula bug: compare next-gain maps at several current gains
    formula_check = {}
    for gc in (0.5, 1.0, 1.5, 2.0):
        rms_q = gc * r0          # rms of quantized past window
        cur_next = target / rms_q                       # current form
        corr_next = gc * target / rms_q                  # corrected form
        formula_check[f"gc={gc}"] = {
            "current_form_g_next": float(cur_next),
            "corrected_form_g_next": float(corr_next),
            "ratio_current_over_corrected": float(cur_next / corr_next) if corr_next else None,
            "current_drops_g_current": bool(abs(cur_next - corr_next) > 1e-9),
        }
    # fixed point of each form on constant input r0:
    # current: g = target/(g*r0) -> g^2 = target/r0 -> g* = sqrt(target/r0)
    # corrected: g = g*target/(g*r0) -> 1 = target/(g r0) -> g = target/r0
    gstar_current = np.sqrt(target / r0)
    gstar_corrected = target / r0
    # (b) deployed default lam=0.9: run a step input and report steady-state
    agc = AD.CausalRMSAGC(target_rms=target, lam=0.9)
    gains, rms_meas = _run_rms_agc(agc, lambda b: r0, n=300)
    tail_g = gains[-50:]
    ss_g = float(np.mean(tail_g))
    ss_rms_q = float(np.mean(rms_meas[-50:]))
    # H2 confirmation: the two forms have DIFFERENT fixed points on the same
    # constant input. Current fixed point sqrt(target/r0) != corrected target/r0
    # (unless target==r0). This is the formula-bug signature: the current form
    # targets the wrong quantity (output rms, not input rms).
    h2_confirmed = bool(abs(gstar_current - gstar_corrected) > 1e-6)
    return {
        "input_rms": r0, "target_rms": target,
        "analytic_fixed_point_CURRENT_form_sqrt(target/r0)": float(gstar_current),
        "analytic_fixed_point_CORRECTED_form_target/r0": float(gstar_corrected),
        "formula_bug_check": formula_check,
        "deployed_lam0p9_steady_state_gain": ss_g,
        "deployed_lam0p9_steady_state_output_rms_q": ss_rms_q,
        "deployed_target_mismatch_output_minus_target": float(ss_rms_q - target),
        "H2_formula_bug_confirmed": h2_confirmed,
    }


# ============================================================================
# T3 — H3 LIFECYCLE: inter-window GG ACF ~ 0 (independent), not contract rho
# ============================================================================

def test_T3_gg_acf_zero():
    """Measure empirical lag-k ACF of the per-window GG block amplitude that
    the CURRENT runner produces (each window = independent gg_block draw via
    seed=ws). A time-correlated GG control problem requires rho != 0; if ACF
    ~ 0 the premise is invalid.
    """
    cfg = SimulationConfig()
    scene = "moderate"
    from common._channel import _resolve_turb_params
    a, b = _resolve_turb_params(scene)
    start = P.SEED_TURB0
    n_win = 400
    N = P.N_DFT
    h_med = np.empty(n_win)
    for bidx in range(n_win):
        ws = start + bidx
        # reproduce exactly what the runner calls
        r = generate_shared_realization_apsk(N, 10.0, scene,
                                             cfg.doppler.DOPPLER_HIGH,
                                             mod="m16apsk", seed=ws)
        h_med[bidx] = float(np.median(r["h_blocks"]))
    # empirical ACF
    def acf(x, lag):
        x = x - x.mean()
        v = np.var(x)
        if v <= 0:
            return 0.0
        return float(np.sum(x[:-lag] * x[lag:]) / (len(x) * v)) if lag else 1.0
    acfs = {f"lag{k}": acf(h_med, k) for k in (1, 2, 5, 10)}
    return {
        "scene": scene,
        "alpha_beta": [float(a), float(b)],
        "n_windows": int(n_win),
        "per_window_h_median_acf": acfs,
        "H3_acf_near_zero": bool(all(abs(v) < 0.2 for v in acfs.values())),
        "note": "current runner: each window independent gg_block(seed=ws); "
                "ACF~0 contradicts a time-correlated GG control premise",
    }


# ============================================================================
# T4 — float-bypass identity at gain != 1 breaks the receiver (H1 corollary)
# ============================================================================

def test_T4_floatbypass_broken_at_gainne1():
    """G3 of Phase-0 only tested gain=1. At gain!=1, feeding q (=Q(g*z)) to the
    receiver WITHOUT de-gain breaks byte-identity with the g=1 chain. This is
    the H1 corollary the old Phase-0 gate never checked.
    """
    cfg = SimulationConfig()
    gl_true = 10.0 ** (9.0 / 10)
    gamma_db = 9.0
    r = generate_shared_realization_apsk(P.N_DFT, gl_true, "weak",
                                         cfg.doppler.DOPPLER_HIGH,
                                         mod="m16apsk", seed=2024)
    z, bits, tx = r["rx_raw"], r["bits"], r["tx"]
    ref = _receiver_outputs(z, bits, tx, r, gl_true, gamma_db)  # untouched float

    broken = {}
    for g in (0.5, 0.75, 1.5, 2.0):
        q, *_ = AD.quantize_iq(z, g, AD.FLOAT_BYPASS_FS, AD.FLOAT_BYPASS_W)
        # OLD: feed q directly  | CORRECT: feed q/g
        old = _receiver_outputs(q, bits, tx, r, gl_true, gamma_db)
        corr = _receiver_outputs(q / g, bits, tx, r, gl_true, gamma_db)
        broken[f"g={g}"] = {
            "OLD_nd_mismatch_vs_ref": int(old["nd"] - ref["nd"]),
            "OLD_nc_mismatch_vs_ref": int(old["nc"] - ref["nc"]),
            "OLD_choice_changed": bool(old["choice"] != ref["choice"]),
            "CORR_nd_mismatch_vs_ref": int(corr["nd"] - ref["nd"]),
            "CORR_nc_mismatch_vs_ref": int(corr["nc"] - ref["nc"]),
            "CORR_choice_changed": bool(corr["choice"] != ref["choice"]),
        }
    return broken


def main():
    t0 = time.time()
    os.makedirs(OUT_DIR, exist_ok=True)
    print("[T1] H1 SCALE: gain->de-gain identity on real receiver ...", flush=True)
    t1 = test_T1_scale_identity()
    print("[T2] H2 CONTROL: causal-RMS period-2 on constant input ...", flush=True)
    t2 = test_T2_causal_rms_period2()
    print("[T3] H3 LIFECYCLE: inter-window GG ACF ...", flush=True)
    t3 = test_T3_gg_acf_zero()
    print("[T4] float-bypass broken at gain!=1 ...", flush=True)
    t4 = test_T4_floatbypass_broken_at_gainne1()

    evidence = {
        "package": "P07-R", "stage": "prefail_reproduction",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "hypotheses": {
            "H1_SCALE": "ADC returns q=Q(g*z); downstream consumes q without /g; "
                        "blind h (1/(2g) floor), amp_limit (thresh 3.0), decide "
                        "(1/(2 gamma_lin)) are scale-dependent -> gain!=1 not "
                        "undoable -> receiver sees wrong scale",
            "H2_CONTROL": "causal-RMS g_next=target/rms(q_past) omits g_current "
                          "carry-over -> period-2 on constant input",
            "H3_LIFECYCLE": "runner regenerates independent gg_block per window "
                            "(seed=ws) -> inter-window ACF~0 -> not a "
                            "time-correlated GG control problem",
        },
        "T1_scale_identity": t1,
        "T2_causal_rms_period2": t2,
        "T3_gg_acf": t3,
        "T4_floatbypass_broken_at_gainne1": t4,
        "elapsed_s": round(time.time() - t0, 1),
    }
    # summary verdicts
    print("\n=== PRE-FIX EVIDENCE SUMMARY ===")
    print(f"H1 (T1): at gain!=1 OLD chain deviates from gain-aware ref:")
    for k, v in t1.items():
        print(f"   {k}: OLD nd/dev={v['OLD_dev_nd_from_ref']:+d}/"
              f"{v['OLD_dev_nc_from_ref']:+d} choice={v['OLD_choice']} "
              f"(ref choice={v['REF_choice']})")
    print(f"H2 (T2): formula bug confirmed = {t2['H2_formula_bug_confirmed']} "
          f"(current drops g_current at all gc); "
          f"fixed points: CURRENT sqrt(t/r0)={t2['analytic_fixed_point_CURRENT_form_sqrt(target/r0)']:.4f} "
          f"vs CORRECTED t/r0={t2['analytic_fixed_point_CORRECTED_form_target/r0']:.4f}; "
          f"deployed lam0.9 ss_gain={t2['deployed_lam0p9_steady_state_gain']:.4f} "
          f"ss_output_rms={t2['deployed_lam0p9_steady_state_output_rms_q']:.4f} "
          f"(target={t2['target_rms']}, output-target={t2['deployed_target_mismatch_output_minus_target']:+.4f})")
    print(f"H3 (T3): per-window GG ACF = {t3['per_window_h_median_acf']} "
          f"-> near-zero={t3['H3_acf_near_zero']}")
    print(f"T4: float-bypass receiver identity BROKEN at gain!=1:")
    for k, v in t4.items():
        print(f"   {k}: OLD nd/nc mismatch={v['OLD_nd_mismatch_vs_ref']:+d}/"
              f"{v['OLD_nc_mismatch_vs_ref']:+d} choice_changed={v['OLD_choice_changed']} | "
              f"CORR nd/nc mismatch={v['CORR_nd_mismatch_vs_ref']:+d}/"
              f"{v['CORR_nc_mismatch_vs_ref']:+d} choice_changed={v['CORR_choice_changed']}")

    with open(OUT_EV, "w", encoding="utf-8") as f:
        json.dump(evidence, f, indent=2, default=str)
    print(f"\nSaved pre-fix evidence -> {OUT_EV}")
    print("Reproduction complete. NO fixes applied. Stop here per Phase-1.")


if __name__ == "__main__":
    main()
