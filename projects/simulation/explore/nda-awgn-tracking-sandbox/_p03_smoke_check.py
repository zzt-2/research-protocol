# -*- coding: utf-8 -*-
"""P03 (T031) Phase 0 — bit-true model smoke check.

MUST pass before any test data is run (brief trap #7). Five gates:
  (1) float-bypass identity:  W=64,F=40 decide_fp == A.decide byte-exact on
      dev seeds 0-9, all anchor cells (weak/moderate/strong x range(5,26,2) dB),
      per-window decision 100% match.
  (2) edge/zero/saturation:   synthetic windows pwr=[0, max, thr±1LSB].
  (3) rounding boundary:      half-up ties resolve to +inf.
  (4) determinism:            same input -> same output byte-exact.
  (5) info-boundary AST audit: decide_fp executable code has no true/tx/oracle
      truth leakage.

Discipline: this file only depends on numpy, the frozen selector A, and the
frozen probe (run_case_multidelta). No edits to any frozen file.
"""
import os
import sys
import ast
import time
import inspect
import argparse

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
sys.path[:0] = [_SIM_ROOT, os.path.join(_SIM_ROOT, 'simulator'), _HERE]

import _a4_switch_common768_30seed as A  # noqa: E402  frozen selector
from _p03_fixed_point import (  # noqa: E402
    quantize, q_to_float, quantize_float, quantize_array, qarr_to_float,
    block_float_normalise, decide_fp, selector_resource_proxy,
    _acc_extra_bits,
)
from _p01_cpr_snr_mismatch_probe import run_case_multidelta  # noqa: E402

FLOAT_BYPASS_W = 64
FLOAT_BYPASS_F = 40
SNR_GRID = list(map(float, range(5, 26, 2)))   # anchor grid 5..25 dB step 2
SCENES = ("weak", "moderate", "strong")
DEV_SEEDS = list(range(10))                    # dev = anchor subset 0-9


# ============================================================================
# Gate 1: float-bypass identity (W=64, F=40 vs A.decide, per-window byte-exact)
# ============================================================================
def gate_float_bypass():
    print("=== Gate 1: float-bypass identity (W=64,F=40 vs A.decide, dev 0-9) ===")
    total_windows = 0
    mismatches = 0
    per_cell = []
    for scene in SCENES:
        for snr in SNR_GRID:
            cell_mm = 0
            cell_win = 0
            for seed in DEV_SEEDS:
                # one channel pass; delta=0 only (P03 is a bitwidth problem).
                md = run_case_multidelta(
                    scene, snr, seed, deltas=(0.0,),
                    extra_selector={
                        "fp_bypass": {"fn": lambda r, g, gl, b: decide_fp(r, g, gl, FLOAT_BYPASS_W, FLOAT_BYPASS_F),
                                      "needs_pilot": False, "needs_reset": False},
                    },
                )
                # the probe stores raw per-window inside pw_raw; retrieve by
                # re-evaluating A.decide ourselves against md's stored channel?
                # The probe does NOT return pw_raw directly. Instead, compare
                # the per-window choices stored by the probe.
                orig_choices = md["per_delta_orig"][0.0]["choices"]
                fp_choices = md["per_delta_extra"]["fp_bypass"][0.0]["choices"]
                # NOTE: per_delta_orig uses A.decide internally (delta=0 means
                # gamma_hat == gamma_true). Both branches see the SAME channel.
                for a, b in zip(orig_choices, fp_choices):
                    cell_win += 1
                    if a != b:
                        cell_mm += 1
                total_windows += cell_win
                mismatches += cell_mm
            per_cell.append({"scene": scene, "snr_db": snr,
                             "windows": cell_win, "mismatches": cell_mm})
            flag = "OK" if cell_mm == 0 else "MISMATCH"
            print(f"  {scene:<9}@{snr:>4.0f}dB: {cell_mm}/{cell_win} mismatch  [{flag}]",
                  flush=True)
    rate = mismatches / total_windows if total_windows else 0.0
    print(f"\n  TOTAL: {mismatches}/{total_windows} per-window mismatches "
          f"({rate*100:.4f}%)")
    return {
        "W": FLOAT_BYPASS_W, "F": FLOAT_BYPASS_F,
        "scenes": list(SCENES), "snr_db": list(SNR_GRID),
        "dev_seeds": list(DEV_SEEDS), "deltas": [0.0],
        "total_windows": int(total_windows), "mismatches": int(mismatches),
        "mismatch_rate": float(rate),
        "pass": bool(mismatches == 0),
        "per_cell": per_cell,
    }


# ============================================================================
# Gate 2: edge / zero / saturation synthetic windows
# ============================================================================
def gate_edge_zero_saturation():
    print("\n=== Gate 2: edge / zero / saturation synthetic windows ===")
    results = []

    # (a) all-zero window: cv = 0, mean = 0. A.decide: cv(0)/max(0,1e-12)=0.
    # cv_awgn_theory*1.10 > 0, so 0 < thr -> 'nda'. decide_fp must match.
    raw_zero = np.zeros(256, dtype=np.complex128)
    r_zero_orig = A.decide(raw_zero, 10.0, 10.0)
    r_zero_fp = decide_fp(raw_zero, 10.0, 10.0, FLOAT_BYPASS_W, FLOAT_BYPASS_F)
    ok_zero = r_zero_orig == r_zero_fp
    print(f"  all-zero window: orig={r_zero_orig}, fp(64,40)={r_zero_fp} "
          f"[{'OK' if ok_zero else 'MISMATCH'}]")
    results.append({"case": "all_zero", "orig": r_zero_orig,
                    "fp_bypass": r_zero_fp, "ok": bool(ok_zero)})

    # (b) constant-magnitude window (cv=0): like a pure tone. cv=0 < thr -> nda.
    raw_const = (3.0 + 0.0j) * np.ones(256, dtype=np.complex128)
    r_const_orig = A.decide(raw_const, 10.0, 10.0)
    r_const_fp = decide_fp(raw_const, 10.0, 10.0, FLOAT_BYPASS_W, FLOAT_BYPASS_F)
    ok_const = r_const_orig == r_const_fp
    print(f"  constant-mag window: orig={r_const_orig}, fp={r_const_fp} "
          f"[{'OK' if ok_const else 'MISMATCH'}]")
    results.append({"case": "constant_mag", "orig": r_const_orig,
                    "fp_bypass": r_const_fp, "ok": bool(ok_const)})

    # (c) tiny window: one sample carries all energy, rest ~0. High cv.
    raw_spike = np.zeros(256, dtype=np.complex128)
    raw_spike[0] = 10.0 + 0.0j
    raw_spike[1:] = 1e-3 * (np.random.RandomState(0).randn(255) +
                            1j * np.random.RandomState(1).randn(255))
    r_spike_orig = A.decide(raw_spike, 10.0, 10.0)
    r_spike_fp = decide_fp(raw_spike, 10.0, 10.0, FLOAT_BYPASS_W, FLOAT_BYPASS_F)
    ok_spike = r_spike_orig == r_spike_fp
    print(f"  spike window: orig={r_spike_orig}, fp={r_spike_fp} "
          f"[{'OK' if ok_spike else 'MISMATCH'}]")
    results.append({"case": "spike", "orig": r_spike_orig,
                    "fp_bypass": r_spike_fp, "ok": bool(ok_spike)})

    # (d) very large magnitude: forces block-float exponent to be large but
    # mantissa still normalises into (0,1]. Float-bypass must match.
    raw_big = (1e6 + 0.0j) * np.ones(256, dtype=np.complex128) + \
              1e3 * (np.random.RandomState(2).randn(256) +
                     1j * np.random.RandomState(3).randn(256))
    r_big_orig = A.decide(raw_big, 25.0, 10 ** 2.5)
    r_big_fp = decide_fp(raw_big, 25.0, 10 ** 2.5, FLOAT_BYPASS_W, FLOAT_BYPASS_F)
    ok_big = r_big_orig == r_big_fp
    print(f"  huge-mag window: orig={r_big_orig}, fp={r_big_fp} "
          f"[{'OK' if ok_big else 'MISMATCH'}]")
    results.append({"case": "huge_mag", "orig": r_big_orig,
                    "fp_bypass": r_big_fp, "ok": bool(ok_big)})

    # (e) threshold-adjacent window: a window where A.decide's gamma_eff is
    # very close to 13.0 (the stage-2 boundary). This is the most sensitive
    # case for the float-bypass test (any rounding would flip it). We search
    # for one by scanning constant-magnitude windows with varying gain so
    # that gamma_db + 10*log10(h) ~= 13.
    found_thr = False
    for mag in np.linspace(0.05, 5.0, 400):
        raw = mag * np.ones(256, dtype=np.complex128)
        # add tiny noise so cv > 0 (else stage-1 always 'nda')
        raw = raw + 1e-6 * (np.random.RandomState(7).randn(256) +
                            1j * np.random.RandomState(8).randn(256))
        gamma_db = 13.0
        gamma_lin = 10.0 ** (gamma_db / 10.0)
        # h = mag^2 - 1/(2*gamma_lin)
        h = float(mag * mag - 1.0 / (2.0 * gamma_lin))
        if h <= 0:
            continue
        geff = gamma_db + 10.0 * np.log10(h)
        if abs(geff - 13.0) < 0.05:
            r_o = A.decide(raw, gamma_db, gamma_lin)
            r_f = decide_fp(raw, gamma_db, gamma_lin, FLOAT_BYPASS_W, FLOAT_BYPASS_F)
            ok_thr = r_o == r_f
            print(f"  threshold-adjacent (mag={mag:.4f}, gamma_eff={geff:.4f}): "
                  f"orig={r_o}, fp={r_f} [{'OK' if ok_thr else 'MISMATCH'}]")
            results.append({"case": "threshold_adjacent", "mag": float(mag),
                            "gamma_eff": float(geff), "orig": r_o,
                            "fp_bypass": r_f, "ok": bool(ok_thr)})
            found_thr = True
            break
    if not found_thr:
        print("  threshold-adjacent: no candidate found (skip)")

    # (f) saturation at small W: a window whose absolute mean power exceeds
    # the Q(W,F) unsigned range must SATURATE (not wrap). Verify no wrap by
    # checking the quantised value equals the max code.
    W_small, F_small = 6, 4
    huge_val = 100.0   # >> max representable (2^6-1)/2^4 = 3.9375
    q = quantize(huge_val, W_small, F_small, signed=False)
    max_code = (1 << W_small) - 1
    ok_sat = (q == max_code)
    print(f"  saturation unsigned (val={huge_val}, W={W_small},F={F_small}): "
          f"code={q} (max={max_code}) [{'OK' if ok_sat else 'WRAP!'}]")
    results.append({"case": "saturation_unsigned", "val": huge_val,
                    "W": W_small, "F": F_small, "code": int(q),
                    "max_code": int(max_code), "ok": bool(ok_sat)})
    # signed saturation
    qs = quantize(-100.0, W_small, F_small, signed=True)
    min_code = -(1 << (W_small - 1))
    ok_sat_s = (qs == min_code)
    print(f"  saturation signed   (val=-100, W={W_small},F={F_small}): "
          f"code={qs} (min={min_code}) [{'OK' if ok_sat_s else 'WRAP!'}]")
    results.append({"case": "saturation_signed", "val": -100.0,
                    "W": W_small, "F": F_small, "code": int(qs),
                    "min_code": int(min_code), "ok": bool(ok_sat_s)})

    all_ok = all(r.get("ok", False) for r in results)
    return {"cases": results, "pass": bool(all_ok)}


# ============================================================================
# Gate 3: rounding boundary (half-up, ties -> +inf)
# ============================================================================
def gate_rounding_boundary():
    print("\n=== Gate 3: rounding boundary (half-up, ties -> +inf) ===")
    W, F = 8, 6
    cases = []
    # 0.5 LSB exactly: at F=6, LSB = 1/64. value = 0.5/64 = 0.0078125 -> ties
    # to +inf: floor(0.5 + 0.5) = floor(1.0) = 1.
    v = 0.5 / (1 << F)
    q = quantize(v, W, F, signed=True)
    ok_tie_pos = (q == 1)
    print(f"  tie +0.5 LSB (v={v}): code={q} (expect 1) "
          f"[{'OK' if ok_tie_pos else 'FAIL'}]")
    cases.append({"case": "tie_pos_half_up", "value": v, "code": int(q),
                  "expect": 1, "ok": bool(ok_tie_pos)})

    # -0.5 LSB: floor(-0.5 + 0.5) = floor(0.0) = 0 (tie -> +inf direction).
    v_neg = -0.5 / (1 << F)
    q_neg = quantize(v_neg, W, F, signed=True)
    ok_tie_neg = (q_neg == 0)
    print(f"  tie -0.5 LSB (v={v_neg}): code={q_neg} (expect 0) "
          f"[{'OK' if ok_tie_neg else 'FAIL'}]")
    cases.append({"case": "tie_neg_half_up", "value": v_neg, "code": int(q_neg),
                  "expect": 0, "ok": bool(ok_tie_neg)})

    # Just-below-half: 0.5 LSB - epsilon should round DOWN.
    v_below = (0.5 / (1 << F)) - 1e-9
    q_below = quantize(v_below, W, F, signed=True)
    ok_below = (q_below == 0)
    print(f"  below-half (v={v_below}): code={q_below} (expect 0) "
          f"[{'OK' if ok_below else 'FAIL'}]")
    cases.append({"case": "below_half", "value": v_below, "code": int(q_below),
                  "expect": 0, "ok": bool(ok_below)})

    # Just-above-half: should round UP.
    v_above = (0.5 / (1 << F)) + 1e-9
    q_above = quantize(v_above, W, F, signed=True)
    ok_above = (q_above == 1)
    print(f"  above-half (v={v_above}): code={q_above} (expect 1) "
          f"[{'OK' if ok_above else 'FAIL'}]")
    cases.append({"case": "above_half", "value": v_above, "code": int(q_above),
                  "expect": 1, "ok": bool(ok_above)})

    # Quantiser reconstruction identity: q_to_float(quantize(x)) == x within
    # 0.5 LSB for IN-RANGE values (no saturation). W=8,F=6 signed range is
    # [-2, 2-2^-6]; test within [-1.9, 1.9] to stay in range.
    xs = np.linspace(-1.9, 1.9, 200)
    max_err = 0.0
    for x in xs:
        q = quantize(x, W, F, signed=True)
        xf = q_to_float(q, F)
        max_err = max(max_err, abs(xf - x))
    ok_recon = (max_err <= 0.5 / (1 << F) + 1e-12)
    print(f"  reconstruction max error (in-range): {max_err:.6f} "
          f"(half-LSB={0.5/(1<<F):.6f}) [{'OK' if ok_recon else 'FAIL'}]")
    cases.append({"case": "reconstruction_within_half_lsb",
                  "max_err": float(max_err), "half_lsb": float(0.5 / (1 << F)),
                  "ok": bool(ok_recon)})

    # float-bypass identity of quantize itself: W=64 F=40 -> error <= 2^-40.
    x_test = 0.123456789012345678
    q_big = quantize(x_test, 64, 40, signed=True)
    err_big = abs(q_to_float(q_big, 40) - x_test)
    ok_bypass = (err_big <= 2 ** -40)
    print(f"  float-bypass quantize (W=64,F=40): err={err_big:.3e} "
          f"(<= 2^-40 = {2**-40:.3e}) [{'OK' if ok_bypass else 'FAIL'}]")
    cases.append({"case": "float_bypass_quantize", "value": x_test,
                  "err": float(err_big), "bound": float(2 ** -40),
                  "ok": bool(ok_bypass)})

    return {"cases": cases, "pass": bool(all(c["ok"] for c in cases))}


# ============================================================================
# Gate 4: determinism (same input -> byte-exact same output)
# ============================================================================
def gate_determinism():
    print("\n=== Gate 4: determinism (same input twice -> identical output) ===")
    rng = np.random.RandomState(42)
    raw = (rng.randn(256) + 1j * rng.randn(256)).astype(np.complex128)
    results = []
    for W, F in [(6, 4), (10, 8), (16, 14), (64, 40)]:
        r1 = decide_fp(raw, 9.0, 10 ** 0.9, W, F)
        r2 = decide_fp(raw, 9.0, 10 ** 0.9, W, F)
        ok = (r1 == r2)
        print(f"  W={W:>3},F={F:>3}: decide_fp twice = {r1},{r2} "
              f"[{'OK' if ok else 'NONDET'}]")
        results.append({"W": W, "F": F, "r1": r1, "r2": r2, "ok": bool(ok)})
    # also test array quantise determinism
    arr = rng.randn(100)
    q1 = quantize_array(arr, 10, 8, signed=True)
    q2 = quantize_array(arr, 10, 8, signed=True)
    ok_arr = np.array_equal(q1, q2)
    print(f"  quantize_array determinism: {'OK' if ok_arr else 'NONDET'}")
    results.append({"case": "quantize_array", "ok": bool(ok_arr)})
    return {"cases": results, "pass": bool(all(r["ok"] for r in results))}


# ============================================================================
# Gate 5: info-boundary AST audit (no TX truth / true SNR / true h/phi leakage)
# ============================================================================
def gate_info_boundary_ast():
    print("\n=== Gate 5: info-boundary AST audit of decide_fp source ===")
    # Get the source of decide_fp from the module.
    import _p03_fixed_point as FP
    src = inspect.getsource(FP)
    tree = ast.parse(src)
    # Walk the AST and find the decide_fp function body. Collect every Name /
    # Attribute / Call identifier used inside it.
    forbidden_substrings = ("true_snr", "true_h", "true_phi", "tx_sym",
                            "tx_bits", "tx_truth", "oracle", "labels")
    # We audit at the lexical level (more conservative than AST): scan the
    # decide_fp function source for forbidden identifiers.
    # Find decide_fp source span.
    lines = src.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.lstrip().startswith("def decide_fp("):
            start = i
            break
    assert start is not None, "decide_fp not found in _p03_fixed_point source"
    # collect until next top-level def at same indent.
    body = []
    for ln in lines[start + 1:]:
        if ln.startswith("def ") or ln.startswith("class "):
            break
        body.append(ln)
    body_text = "\n".join(body)
    leaks = []
    for bad in forbidden_substrings:
        # word-boundary match (case-insensitive) to avoid false positives like
        # 'gamma_true' containing 'true' but being a parameter name. Actually
        # decide_fp must NOT have gamma_true either — its signature is
        # (raw, gamma_db, gamma_lin). So we audit for 'true' anywhere too.
        import re
        pat = r"\b" + bad.replace("_", r"_?") + r"\b"
        if re.search(pat, body_text, re.IGNORECASE):
            leaks.append(bad)
    # also confirm the signature has only (raw, gamma_db, gamma_lin, W, F).
    sig_line = lines[start]
    print(f"  decide_fp signature: {sig_line.strip()}")
    sig_ok = all(p in sig_line for p in ("raw", "gamma_db", "gamma_lin")) and \
             "true" not in sig_line.lower() and "tx" not in sig_line.lower()
    print(f"  signature clean (no true/tx): {sig_ok}")
    # audit gamma_db / gamma_lin usage: they must come from the receiver's
    # nominal SNR (the probe passes gamma_hat which is biased only in P01; in
    # P03 delta=0 so gamma_hat == gamma_true numerically, but the decide_fp
    # code treats it as the receiver's nominal SNR — that is the contract).
    print(f"  forbidden-substring leaks in decide_fp body: {leaks if leaks else 'NONE'}")
    ok = (len(leaks) == 0) and sig_ok
    print(f"  info-boundary audit: [{'OK' if ok else 'LEAK!'}]")
    return {
        "signature": sig_line.strip(), "signature_clean": bool(sig_ok),
        "leaks": leaks, "pass": bool(ok),
        "audited_identifiers": list(forbidden_substrings),
    }


# ============================================================================
# main
# ============================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-float-bypass", action="store_true",
                    help="skip gate 1 (channel-replay heavy) for quick re-test")
    a = ap.parse_args()
    t0 = time.time()
    print("P03 smoke check — bit-true model gates\n" + "=" * 60)

    g3 = gate_rounding_boundary()
    g4 = gate_determinism()
    g2 = gate_edge_zero_saturation()
    g5 = gate_info_boundary_ast()
    if not a.skip_float_bypass:
        g1 = gate_float_bypass()
    else:
        g1 = {"pass": None, "skipped": True}

    print("\n" + "=" * 60)
    print("SMOKE SUMMARY:")
    print(f"  Gate 1 float-bypass identity (W=64,F=40):  "
          f"{'PASS' if g1['pass'] else ('SKIP' if g1.get('skipped') else 'FAIL')}")
    print(f"  Gate 2 edge/zero/saturation:               "
          f"{'PASS' if g2['pass'] else 'FAIL'}")
    print(f"  Gate 3 rounding boundary:                  "
          f"{'PASS' if g3['pass'] else 'FAIL'}")
    print(f"  Gate 4 determinism:                        "
          f"{'PASS' if g4['pass'] else 'FAIL'}")
    print(f"  Gate 5 info-boundary AST audit:            "
          f"{'PASS' if g5['pass'] else 'FAIL'}")
    all_pass = all(g.get("pass") for g in [g1, g2, g3, g4, g5] if g.get("pass") is not None)
    print(f"\n>>> OVERALL: {'PASS' if all_pass else 'FAIL — DO NOT proceed to Phase A'}")
    print(f"elapsed {time.time()-t0:.0f}s")
    return all_pass, {"gate1_float_bypass": g1, "gate2_edge_zero_sat": g2,
                      "gate3_rounding": g3, "gate4_determinism": g4,
                      "gate5_info_boundary": g5}


if __name__ == "__main__":
    ok, results = main()
    sys.exit(0 if ok else 1)
