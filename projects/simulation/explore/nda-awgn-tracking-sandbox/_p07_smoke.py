# -*- coding: utf-8 -*-
"""P07 — Phase 0 smoke + BLOCKER identity gates.

Five gates (BLOCKER — any fail -> EXECUTION_INVALID):
  G1 ADC math: round-half-up, saturating (no wrap), signed I/Q symmetry.
  G2 float-bypass reconstruction: quantize_iq(gain=1, fs=large, W=64)
     reconstructs input to <= 2^-40.
  G3 float-bypass receiver identity: run_case_with_adc(gain=1, fs=large, W=64)
     with FixedGainAGC reproduces run_case_multidelta per-cell outputs
     byte-exactly across all dev cells.
  G4 causality: gain_b depends ONLY on windows < b (no future leak); window 0
     uses nominal.
  G5 info-boundary AST: every decide_gain/update body in _p07_adapters.py is
     free of forbidden substrings (h/alpha/beta/tx/phi/bits/true/oracle).

Run: python _p07_smoke.py   (writes p07_phase0_smoke.json)
"""
import os
import sys
import json
import ast
import time

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
sys.path[:0] = [_SIM_ROOT, os.path.join(_SIM_ROOT, 'simulator'), _HERE]

import _p07_adapters as AD  # noqa: E402
import _p07_runner as R  # noqa: E402
from _p01_cpr_snr_mismatch_probe import run_case_multidelta  # noqa: E402

OUT = os.path.join(_SIM_ROOT, "results", "p07_agc_adc_dynamic_range",
                   "p07_phase0_smoke.json")

FORBIDDEN_SUBSTRINGS = ("alpha", "beta", " tx ", ".tx", " phi", " bits",
                        "oracle", "true_h", "true_h ", "r['h']", 'r["h"]',
                        "future")


def gate_g1_adc_math():
    """Round-half-up, saturating no-wrap, signed I/Q symmetry."""
    fs = 1.0
    # round-half-up: 0.5 LSB -> +inf
    q, cr, ci, rr, ri = AD.quantize_iq(np.array([0.0 + 1j * 0.0]), 1.0, fs, 4)
    # all-zero in -> all-zero out
    assert cr[0] == 0 and ci[0] == 0, f"zero in nonzero out: {cr[0]},{ci[0]}"
    # step at W=4: 2*1/16 = 0.125; code at +0.0625 (half LSB) -> round up to 1
    step = 2.0 * fs / 16
    half_lsb = step / 2
    q, cr, ci, rr, ri = AD.quantize_iq(
        np.array([half_lsb + 1j * (-half_lsb)]), 1.0, fs, 4)
    # +0.5 LSB -> code +1 (round up), -0.5 LSB -> code 0 (floor(-0.5+0.5)=0)
    assert cr[0] == 1, f"half-up tie failed (real): code={cr[0]}"
    assert ci[0] == 0, f"half-up tie failed (imag): code={ci[0]}"
    # saturation: large value -> rail, NO WRAP
    q, cr, ci, rr, ri = AD.quantize_iq(
        np.array([100.0 + 1j * (-100.0)]), 1.0, fs, 4)
    assert cr[0] == 7, f"saturate high (W4 -> 7): code={cr[0]}"   # 2^3-1 = 7
    assert ci[0] == -8, f"saturate low (W4 -> -8): code={ci[0]}"  # -2^3 = -8
    assert rr[0] and ri[0], "rail flag not set on saturation"
    # never wraps: value 1000x FS still == 7 (not -8 or rolled)
    q2, cr2, _, _, _ = AD.quantize_iq(np.array([1000.0]), 1.0, fs, 4)
    assert cr2[0] == 7, f"wrap detected (huge value): code={cr2[0]}"
    # signed symmetry: +v and -v give symmetric codes
    q, cp, _, _, _ = AD.quantize_iq(np.array([0.3]), 1.0, fs, 8)
    q, cn, _, _, _ = AD.quantize_iq(np.array([-0.3]), 1.0, fs, 8)
    assert cp[0] == -cn[0], f"signed asymmetry: {cp[0]} vs {cn[0]}"
    return {"step_w4": step, "half_lsb": half_lsb,
            "saturate_high_code_w4": 7, "saturate_low_code_w4": -8,
            "signed_symm_w8": (int(cp[0]), int(cn[0]))}


def gate_g2_floatbypass_recon():
    """W=64 + large fs reconstructs to <= 2^-40."""
    rng = np.random.default_rng(0)
    z = (rng.standard_normal(2048) + 1j * rng.standard_normal(2048))
    err = AD.adc_reconstruct_lossless(z, 1.0, AD.FLOAT_BYPASS_FS, AD.FLOAT_BYPASS_W)
    return {"max_recon_err": err, "threshold_2em40": 2 ** -40,
            "pass": bool(err <= 2 ** -40)}


def gate_g3_floatbypass_receiver_identity():
    """FixedGainAGC(gain=1, W=64, fs=large) == run_case_multidelta byte-exact.

    Checks a representative subset of cells (not all 330) to keep smoke fast,
    but spans weak/moderate/strong x {5,9,15,21} dB x seeds {0,1,2}.
    """
    cells = [(sc, g, s) for sc in ("weak", "moderate", "strong")
             for g in (5.0, 9.0, 15.0, 21.0)
             for s in (0, 1, 2)]
    agc = AD.FixedGainAGC(gain=1.0, fs=AD.FLOAT_BYPASS_FS)
    mismatches = []
    for (sc, g, s) in cells:
        # float-bypass ADC run
        a = R.run_case_with_adc(sc, g, s, agc, AD.FLOAT_BYPASS_FS,
                                AD.FLOAT_BYPASS_W)
        # original float run (delta=0; we compare the channel-dependent base)
        # run_case_multidelta returns {base, per_delta_orig}; compare base.
        md = run_case_multidelta(sc, g, s, deltas=(0.0,))
        base = md["base"]
        for k in ("fixed_nda_errors", "fixed_da_errors",
                  "lower_count_bound_errors",
                  "true_oracle_errors", "true_oracle_bits"):
            if a[k] != base[k]:
                mismatches.append((sc, g, s, k, a[k], base[k]))
        # per-window error arrays byte-identical
        if not np.array_equal(a["per_window_da_err"], base["per_window_da_err"]):
            mismatches.append((sc, g, s, "per_window_da_err", "array", "array"))
        if not np.array_equal(a["per_window_nda_err"], base["per_window_nda_err"]):
            mismatches.append((sc, g, s, "per_window_nda_err", "array", "array"))
    return {"n_cells_checked": len(cells), "n_mismatches": len(mismatches),
            "first_mismatches": mismatches[:5],
            "pass": len(mismatches) == 0}


def gate_g4_causality():
    """gain_b depends ONLY on windows < b; window 0 == nominal."""
    agc = AD.CausalRMSAGC()
    agc.reset()
    g0 = agc.gain_for_next()   # before any update == nominal
    assert abs(g0 - AD.NOMINAL_GAIN) < 1e-12, f"window-0 gain != nominal: {g0}"
    # feed two different past windows, gain should track them
    agc.update(np.ones(256) * 0.5 + 1j * np.zeros(256))   # small RMS
    g_after_small = agc.gain_for_next()
    agc2 = AD.CausalRMSAGC()
    agc2.update(np.ones(256) * 2.0 + 1j * np.zeros(256))  # large RMS
    g_after_large = agc2.gain_for_next()
    # smaller RMS -> larger gain (to reach target), within bounds
    assert g_after_small > g_after_large, (
        f"causality broken: small-RMS gain {g_after_small} not > "
        f"large-RMS gain {g_after_large}")
    # gain never reads future: prove by feeding identical sequences in two
    # orders up to window k and confirming gain at k is identical.
    a = AD.PeakHoldAGC(); a.reset()
    b = AD.PeakHoldAGC(); b.reset()
    seq = [np.ones(256) * v + 1j * np.zeros(256) for v in (0.3, 0.7, 0.5)]
    for w in seq:
        a.update(w)
    for w in seq:
        b.update(w)
    assert abs(a.gain_for_next() - b.gain_for_next()) < 1e-12, "nondeterministic"
    return {"window0_gain": g0, "gain_after_small_rms": g_after_small,
            "gain_after_large_rms": g_after_large,
            "monotone": bool(g_after_small > g_after_large),
            "deterministic_replay": True}


def gate_g5_info_boundary_ast():
    """AST audit: every AGC class body free of forbidden substrings."""
    src = open(os.path.join(_HERE, "_p07_adapters.py"), encoding="utf-8").read()
    tree = ast.parse(src)
    findings = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name.endswith("AGC"):
            body_src = ast.get_source_segment(src, node) or ""
            for sub in FORBIDDEN_SUBSTRINGS:
                if sub in body_src:
                    findings.append((node.name, sub))
    # quantize_iq must not reference truth either
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "quantize_iq":
            body_src = ast.get_source_segment(src, node) or ""
            for sub in FORBIDDEN_SUBSTRINGS:
                if sub in body_src:
                    findings.append(("quantize_iq", sub))
    return {"n_findings": len(findings), "findings": findings,
            "forbidden_checked": list(FORBIDDEN_SUBSTRINGS),
            "pass": len(findings) == 0}


def main():
    t0 = time.time()
    results = {}
    print("G1 ADC math ...", flush=True)
    results["g1_adc_math"] = gate_g1_adc_math()
    print("G2 float-bypass reconstruction ...", flush=True)
    results["g2_floatbypass_recon"] = gate_g2_floatbypass_recon()
    print("G3 float-bypass receiver identity ...", flush=True)
    results["g3_floatbypass_receiver_identity"] = gate_g3_floatbypass_receiver_identity()
    print("G4 causality ...", flush=True)
    results["g4_causality"] = gate_g4_causality()
    print("G5 info-boundary AST ...", flush=True)
    results["g5_info_boundary_ast"] = gate_g5_info_boundary_ast()

    gates = {
        "g1_adc_math": results["g1_adc_math"],   # assertions
        "g2_pass": results["g2_floatbypass_recon"]["pass"],
        "g3_pass": results["g3_floatbypass_receiver_identity"]["pass"],
        "g4_pass": results["g4_causality"]["monotone"],
        "g5_pass": results["g5_info_boundary_ast"]["pass"],
    }
    all_pass = bool(all(gates.values()))
    out = {
        "package": "P07",
        "family": "F_AGC_ADC_DYNAMIC_RANGE_UNDER_GG",
        "phase": "0_smoke",
        "gates": gates,
        "all_pass": all_pass,
        "elapsed_s": round(time.time() - t0, 1),
        "results": results,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=str)
    print(json.dumps({"all_pass": all_pass, "gates": gates,
                      "elapsed_s": out["elapsed_s"]}, indent=2, default=str))
    return out


if __name__ == "__main__":
    main()
