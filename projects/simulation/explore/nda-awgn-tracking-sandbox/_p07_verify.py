# -*- coding: utf-8 -*-
"""P07 — independent verifier (V071).

Independently recomputes / audits the P07 result WITHOUT reusing the executor's
aggregation. Checks (each PASS/FAIL):

  V1  ADC math: round-half-up, saturating no-wrap, signed I/Q (re-run on synth).
  V2  float-bypass identity: re-run run_case_with_adc(gain=1,W=64,fs=1e6) on a
      fresh cell, confirm byte-identical to run_case_multidelta (independent
      re-call, not reusing executor output).
  V3  info-boundary AST: re-parse _p07_adapters.py, zero forbidden substrings.
  V4  causality: re-instantiate AGCs, confirm window-0 nominal + deterministic.
  V5  raw->aggregate recompute: reload raw_rows, recompute pooled regret per
      bitwidth, match executor's aggregate to <= 1e-9 relative error.
  V6  seed isolation: dev seeds disjoint from held-out; no 71-80 pollution.
  V7  paired realization: same (scene,g,seed) -> same channel across configs
      (verify the batched evaluator shares one channel-gen via independent
      re-call of eval_cell_fixed_gains on one cell).
  V8  terminal verdict correctness: re-derive from the aggregates + frozen gate.
  V9  frozen-files unchanged: git diff --stat empty on common/, params.py,
      _a4_switch_common768_30seed.py, _p01_*.py, anchor JSON.

Run: python _p07_verify.py
"""
import os
import sys
import json
import ast
import subprocess

import numpy as np
from scipy import stats

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
sys.path[:0] = [_SIM_ROOT, os.path.join(_SIM_ROOT, 'simulator'), _HERE]

import _p07_adapters as AD  # noqa: E402
import _p07_runner as R  # noqa: E402
import _p07_batch as BATCH  # noqa: E402
from _p01_cpr_snr_mismatch_probe import run_case_multidelta  # noqa: E402

OUT_DIR = os.path.join(_SIM_ROOT, "results", "p07_agc_adc_dynamic_range")
FORBIDDEN = ("alpha", "beta", " tx ", ".tx", " phi", " bits",
             "oracle", "true_h", "r['h']", 'r["h"]', "future")


def ci_t(data):
    a = np.asarray(data, dtype=float)
    n = len(a)
    mean = float(np.mean(a)) if n else float("nan")
    std = float(np.std(a, ddof=1)) if n > 1 else 0.0
    hw = float(stats.t.ppf(0.975, n - 1)) * std / np.sqrt(n) if n > 1 else 0.0
    return {"mean": mean, "std": std, "hw": hw, "ci_lo": mean - hw, "ci_hi": mean + hw, "n": n}


def v1_adc_math():
    fs = 1.0
    q, cr, ci, rr, ri = AD.quantize_iq(np.array([0.0625 + 1j * -0.0625]), 1.0, fs, 4)
    ok_round = (cr[0] == 1 and ci[0] == 0)
    q, cr, ci, rr, ri = AD.quantize_iq(np.array([100.0 + 1j * -100.0]), 1.0, fs, 4)
    ok_sat = (cr[0] == 7 and ci[0] == -8 and rr[0] and ri[0])
    q, cr2, _, _, _ = AD.quantize_iq(np.array([1000.0]), 1.0, fs, 4)
    ok_nowrap = (cr2[0] == 7)
    return {"pass": bool(ok_round and ok_sat and ok_nowrap),
            "round_half_up": bool(ok_round), "saturate": bool(ok_sat),
            "no_wrap": bool(ok_nowrap)}


def v2_floatbypass_identity():
    """Independent re-call: FixedGainAGC(1, W=64) == run_case_multidelta."""
    cells = [("weak", 9.0, 0), ("strong", 15.0, 1), ("moderate", 21.0, 2)]
    mism = []
    for (sc, g, s) in cells:
        a = R.run_case_with_adc(sc, g, s, AD.FixedGainAGC(gain=1.0, fs=AD.FLOAT_BYPASS_FS),
                                AD.FLOAT_BYPASS_FS, AD.FLOAT_BYPASS_W)
        md = run_case_multidelta(sc, g, s, deltas=(0.0,))["base"]
        for k in ("fixed_nda_errors", "fixed_da_errors", "true_oracle_errors",
                  "true_oracle_bits", "lower_count_bound_errors"):
            if a[k] != md[k]:
                mism.append((sc, g, s, k, a[k], md[k]))
        if not np.array_equal(a["per_window_da_err"], md["per_window_da_err"]):
            mism.append((sc, g, s, "per_window_da_err", "arr", "arr"))
    return {"pass": len(mism) == 0, "n_cells": len(cells), "mismatches": mism[:5]}


def v3_info_boundary_ast():
    src = open(os.path.join(_HERE, "_p07_adapters.py"), encoding="utf-8").read()
    tree = ast.parse(src)
    findings = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
            seg = ast.get_source_segment(src, node) or ""
            if (isinstance(node, ast.ClassDef) and node.name.endswith("AGC")) or \
               (isinstance(node, ast.FunctionDef) and node.name in ("quantize_iq",)):
                for sub in FORBIDDEN:
                    if sub in seg:
                        findings.append((node.name, sub))
    return {"pass": len(findings) == 0, "findings": findings,
            "forbidden": list(FORBIDDEN)}


def v4_causality():
    a = AD.CausalRMSAGC(); a.reset()
    g0 = a.gain_for_next()
    nominal_ok = abs(g0 - AD.NOMINAL_GAIN) < 1e-12
    a.update(np.ones(256) * 0.5 + 1j * np.zeros(256))
    g_small = a.gain_for_next()
    b = AD.CausalRMSAGC(); b.update(np.ones(256) * 2.0 + 1j * np.zeros(256))
    g_large = b.gain_for_next()
    monotone = g_small > g_large
    return {"pass": bool(nominal_ok and monotone),
            "window0_nominal": nominal_ok, "monotone": monotone,
            "g_small": g_small, "g_large": g_large}


def v5_raw_aggregate_recompute(phasea_path):
    """Reload raw_rows, recompute pooled regret per bitwidth, match aggregate."""
    if not os.path.exists(phasea_path):
        return {"pass": False, "reason": "phaseA file missing"}
    with open(phasea_path, encoding="utf-8") as f:
        pa = json.load(f)
    raw = pa["raw_rows"]
    rel_errs = []
    for W in pa["frozen"]["bitwidths"]:
        key = f"W{W}"
        agg = pa["per_bitwidth"][key]
        best_gain = agg["best_gain"]
        rows = [r for r in raw if r["W"] == W and r["gain"] == best_gain]
        recomputed = ci_t([r["paired_regret_dB"] for r in rows])
        for k in ("mean", "ci_lo", "ci_hi"):
            av = agg["pooled_regret_dB"][k]
            rv = recomputed[k]
            if abs(av - rv) > 1e-9:
                rel_errs.append((key, k, av, rv))
    # also recompute paired_regret from selected_errors/ideal to confirm identity
    identity_violations = []
    for r in raw[:2000]:
        if r["ideal_float_selected_errors"] > 0:
            expected = 10.0 * np.log10(r["selected_errors"] / r["ideal_float_selected_errors"])
            if abs(expected - r["paired_regret_dB"]) > 1e-9:
                identity_violations.append((r["scene"], r["W"], r["gain"]))
    return {"pass": len(rel_errs) == 0 and len(identity_violations) == 0,
            "recompute_mismatches": rel_errs[:5],
            "regret_identity_violations": len(identity_violations)}


def v6_seed_isolation(phasea_path):
    if not os.path.exists(phasea_path):
        return {"pass": False, "reason": "phaseA file missing"}
    with open(phasea_path, encoding="utf-8") as f:
        pa = json.load(f)
    dev = set(pa["frozen"]["dev_seeds"])
    forbidden = set(range(71, 81))
    has_forbidden = bool(dev & forbidden)
    return {"pass": not has_forbidden, "dev_seeds": sorted(dev),
            "forbidden_71_80_present": has_forbidden}


def v7_paired_realization():
    """eval_cell_fixed_gains shares one channel-gen across configs; verify by
    checking that the ideal_float selected_errors from the batched call equals
    a direct float run on the same (scene,g,seed)."""
    configs = [{"gain": 1.0, "W": AD.FLOAT_BYPASS_W, "fs": AD.FLOAT_BYPASS_FS,
                "tag": "ideal_float"}]
    for (sc, g, s) in [("weak", 9.0, 0), ("strong", 15.0, 1)]:
        batched = BATCH.eval_cell_fixed_gains(sc, g, s, configs)["ideal_float"]
        direct = R.run_case_with_adc(sc, g, s, AD.FixedGainAGC(gain=1.0, fs=AD.FLOAT_BYPASS_FS),
                                     AD.FLOAT_BYPASS_FS, AD.FLOAT_BYPASS_W)
        if batched["selected_errors"] != direct["selected_errors"]:
            return {"pass": False, "cell": (sc, g, s),
                    "batched": batched["selected_errors"],
                    "direct": direct["selected_errors"]}
    return {"pass": True}


def v8_terminal_verdict(phasea_path):
    if not os.path.exists(phasea_path):
        return {"pass": False, "reason": "phaseA file missing"}
    with open(phasea_path, encoding="utf-8") as f:
        pa = json.load(f)
    # re-derive problem_established from per_bitwidth
    MDE = pa["frozen"]["MDE"]
    bw_pass = []
    for W in pa["frozen"]["bitwidths"]:
        pb = pa["per_bitwidth"][f"W{W}"]
        pooled = pb["pooled_regret_dB"]
        pooled_ok = pooled["mean"] >= MDE and pooled["ci_lo"] > 0
        cells_ok = pb["n_cells_passing_mde"] >= pa["frozen"]["min_cells_passing"]
        bw_pass.append(pooled_ok and cells_ok)
    re_derived = all(bw_pass)
    match = (re_derived == pa["problem_established"])
    return {"pass": match, "re_derived_problem_established": re_derived,
            "reported": pa["problem_established"]}


def v9_frozen_files_unchanged():
    try:
        r = subprocess.run(
            ["git", "diff", "--stat", "HEAD", "--",
             "projects/simulation/common/",
             "projects/simulation/params.py",
             "projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_switch_common768_30seed.py",
             "projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_branchrouted_30seed.py",
             "projects/simulation/explore/nda-awgn-tracking-sandbox/sc_nda_ml_sim.py",
             "projects/simulation/explore/nda-awgn-tracking-sandbox/_p01_cpr_snr_mismatch_probe.py",
             ],
            capture_output=True, text=True, cwd=_SIM_ROOT)
        return {"pass": r.stdout.strip() == "", "diff": r.stdout.strip()[:500]}
    except Exception as e:
        return {"pass": False, "error": str(e)}


def v10_phasebc_aggregate_recompute():
    """Reload Phase B/C, recompute conventional regret + candidate delta from
    heldout_rows, match the reported aggregates to <= 1e-9 rel err. Also
    re-derive terminal verdict from the aggregates + frozen gate logic."""
    path = os.path.join(OUT_DIR, "p07_phaseBC.json")
    if not os.path.exists(path):
        return {"pass": False, "reason": "phaseBC file missing"}
    with open(path, encoding="utf-8") as f:
        bc = json.load(f)
    rows = bc.get("heldout_rows", [])
    mism = []
    # recompute conv regret per family|W
    for key, agg in bc.get("phase_B_conventional_agg", {}).items():
        fam, W = key.split("|W")
        W = int(W)
        regrets = [r["regret"] for r in rows
                   if r.get("fam") == fam and r.get("W") == W]
        rc = ci_t(regrets)
        for k in ("mean", "ci_lo", "ci_hi"):
            if abs(agg[k] - rc[k]) > 1e-9:
                mism.append((key, k, agg[k], rc[k]))
    # re-derive terminal verdict
    MDE = bc["frozen"]["MDE"]
    sc = bc.get("phase_B_strongest_conv_per_bitwidth", {})
    conv_resolves = all(sc[f"W{W}"]["regret_ci"]["mean"] < MDE
                        for W in bc["frozen"]["bitwidths"])
    cross = bc.get("phase_C_cross_consistent", False)
    if conv_resolves:
        re_verdict = "PROBLEM_RESOLVED_BY_CONVENTIONAL_AGC"
    elif cross:
        re_verdict = "DIAGNOSTIC_METHOD_SIGNAL"
    else:
        re_verdict = "NO_DIAGNOSTIC_METHOD_SIGNAL"
    verdict_match = (re_verdict == bc["terminal_verdict"])
    return {"pass": len(mism) == 0 and verdict_match,
            "recompute_mismatches": mism[:5],
            "re_derived_verdict": re_verdict,
            "reported_verdict": bc["terminal_verdict"],
            "conv_resolves_re": conv_resolves}


def main():
    checks = {}
    phasea_path = os.path.join(OUT_DIR, "p07_phaseA_dev.json")
    checks["V1_adc_math"] = v1_adc_math()
    checks["V2_floatbypass_identity"] = v2_floatbypass_identity()
    checks["V3_info_boundary_ast"] = v3_info_boundary_ast()
    checks["V4_causality"] = v4_causality()
    checks["V5_raw_aggregate_recompute"] = v5_raw_aggregate_recompute(phasea_path)
    checks["V6_seed_isolation"] = v6_seed_isolation(phasea_path)
    checks["V7_paired_realization"] = v7_paired_realization()
    checks["V8_terminal_verdict"] = v8_terminal_verdict(phasea_path)
    checks["V9_frozen_files_unchanged"] = v9_frozen_files_unchanged()
    checks["V10_phasebc_aggregate_recompute"] = v10_phasebc_aggregate_recompute()

    n_pass = sum(1 for c in checks.values() if c.get("pass"))
    n_total = len(checks)
    out = {"package": "P07", "verifier": "V071",
           "n_pass": n_pass, "n_total": n_total,
           "accept": n_pass == n_total,
           "checks": checks}
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "p07_verifier_result.json"), "w",
              encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=str)
    print(json.dumps({"n_pass": n_pass, "n_total": n_total,
                      "accept": out["accept"],
                      "check_results": {k: v.get("pass") for k, v in checks.items()}},
                     indent=2))
    return out


if __name__ == "__main__":
    main()
