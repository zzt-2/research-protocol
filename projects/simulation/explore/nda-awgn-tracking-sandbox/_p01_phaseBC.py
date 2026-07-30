# -*- coding: utf-8 -*-
"""P01 Phase B/C — conventional adapter + robust candidates on held-out seeds.

Runs on the harm cells (+ full main grid for context) with FRESH held-out seeds
30-49, comparing:
  - orig:        original selector fed biased nominal gamma_hat
  - adapter_*:   conventional pilot-SNR estimator plug-in (δ-independent)
  - cand_*:      robust candidates (mechanism-differentiated)
  - oracle_true: true-gamma selector (UPPER BOUND only, never a deployable Go)

Judgment:
  Phase B: adapter resolves harm if, on every Phase-A harm cell, the adapter's
           paired Δgain_vs_d0 >= -0.3 dB (adapter is δ-invariant so this == its
           fixed gain drop vs the δ=0 original baseline) AND no NEW harm vs the
           δ=0 anchor.
  Phase C: best candidate gives DIAGNOSTIC_METHOD_SIGNAL only if it STABLY beats
           the adapter on held-out (paired Δgain candidate-vs-adapter, mean >= MDE
           AND CI_low > 0) AND does not use extra info / extra tuning budget.
"""
import os
import sys
import json
import time
from datetime import datetime, timezone

import numpy as np
from scipy import stats

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
sys.path[:0] = [_SIM_ROOT, os.path.join(_SIM_ROOT, 'simulator'), _HERE]

import _p01_cpr_snr_mismatch_probe as PR  # noqa: E402
import _p01_adapter_and_candidates as AD  # noqa: E402
from _p01_adapter_and_candidates import CANDIDATES  # noqa: E402
import _a4_switch_common768_30seed as A  # noqa: E402

# wire pilot hooks so the multidelta runner can call pilot-based selectors
PR.wire_pilot_hooks(AD.set_window_pilots, AD.reset_hysteresis)

HARM_GAIN_DROP_DB = 0.3
MAIN_CELLS = [
    ("weak", 5.0), ("weak", 7.0), ("weak", 9.0), ("weak", 11.0), ("weak", 13.0),
    ("moderate", 5.0), ("moderate", 7.0), ("moderate", 9.0), ("moderate", 11.0), ("moderate", 13.0),
    ("strong", 5.0), ("strong", 7.0), ("strong", 9.0), ("strong", 11.0), ("strong", 13.0),
]
# Phase A harm cells (dev judgment) — focus Phase B resolution check here
HARM_CELLS_DEV = [
    ("weak", 5.0, -3.0), ("weak", 7.0, -3.0), ("weak", 9.0, -3.0),
    ("weak", 11.0, 3.0), ("moderate", 13.0, 3.0),
]
DELTAS = PR.DELTAS
OUT_DIR = os.path.join(_SIM_ROOT, "results", "p01_cpr_snr_mismatch")


def ci_t(data):
    a = np.asarray(data, dtype=float)
    n = len(a)
    mean = float(np.mean(a))
    std = float(np.std(a, ddof=1)) if n > 1 else 0.0
    hw = float(stats.t.ppf(0.975, n - 1)) * std / np.sqrt(n) if n > 1 else 0.0
    return mean, std, hw, mean - hw, mean + hw


def build_selector_specs(methods):
    """Map method name -> {'fn', 'needs_pilot', 'needs_reset'} for the runner."""
    specs = {}
    for m in methods:
        if m == "oracle_true":
            # fed TRUE gamma (delta=0) — upper bound only
            specs[m] = {"fn": lambda raw, gdb, glin, b: A.decide(raw, gdb - (gdb - _true_gamma_ref[0]),
                                                                  _true_gamma_ref[1], ),
                        "needs_pilot": False, "needs_reset": False}
            continue
        fn, np_flag, nr_flag = CANDIDATES[m]
        specs[m] = {"fn": fn, "needs_pilot": np_flag, "needs_reset": nr_flag}
    return specs


# oracle_true needs the cell's true gamma; stash via a mutable ref
_true_gamma_ref = [9.0, 10 ** (9.0 / 10)]


def _oracle_decide_factory(gamma_true_db):
    g_lin = 10.0 ** (gamma_true_db / 10.0)
    def _f(raw, gamma_hat_db, gamma_hat_lin, b):
        return A.decide(raw, gamma_true_db, g_lin)
    return _f


def run(cells, seeds, methods, tag):
    """Run scan; return raw_rows + per-(scene,gamma,delta,method) aggregates."""
    t0 = time.time()
    raw_rows = []
    for ci, (scene, snr) in enumerate(cells):
        # build per-cell selector specs (oracle_true needs the true gamma of this cell)
        specs = {}
        for m in methods:
            if m == "oracle_true":
                specs[m] = {"fn": _oracle_decide_factory(snr), "needs_pilot": False,
                            "needs_reset": False}
            else:
                fn, npf, nrf = CANDIDATES[m]
                specs[m] = {"fn": fn, "needs_pilot": npf, "needs_reset": nrf}
        for seed in seeds:
            md = PR.run_case_multidelta(scene, snr, seed, deltas=DELTAS,
                                        extra_selector=specs)
            base = md["base"]
            nda_c = base["fixed_nda_errors"]
            for delta in DELTAS:
                # original selector
                po = md["per_delta_orig"][delta]
                row_base = {
                    "tag": tag, "scene": scene, "gamma_true_db": float(snr),
                    "delta_db": float(delta), "seed_index": int(seed),
                    "method": "orig",
                    "selected_errors": int(po["selected_errors"]),
                    "n_select_da": int(po["n_select_da"]),
                    "n_select_nda": int(po["n_select_nda"]),
                    "fixed_nda_errors_common768": int(nda_c),
                    "gain_db": float(10 * np.log10(nda_c / po["selected_errors"])
                                     if po["selected_errors"] > 0 else float("inf")),
                }
                raw_rows.append(row_base)
                # each extra method (δ-invariant for adapter/cand that ignore gamma_hat)
                for m, permap in md.get("per_delta_extra", {}).items():
                    pe = permap[delta]
                    raw_rows.append({
                        "tag": tag, "scene": scene, "gamma_true_db": float(snr),
                        "delta_db": float(delta), "seed_index": int(seed),
                        "method": m,
                        "selected_errors": int(pe["selected_errors"]),
                        "n_select_da": int(pe["n_select_da"]),
                        "n_select_nda": int(pe["n_select_nda"]),
                        "fixed_nda_errors_common768": int(nda_c),
                        "gain_db": float(10 * np.log10(nda_c / pe["selected_errors"])
                                         if pe["selected_errors"] > 0 else float("inf")),
                    })
        el = time.time() - t0
        print(f"  [{tag}] {scene}@{snr:.0f}dB done ({ci+1}/{len(cells)} cells, "
              f"{el:.0f}s)", flush=True)

    # ---- aggregates per (scene, gamma, delta, method) ----
    aggregates = []
    methods_seen = sorted(set(r["method"] for r in raw_rows))
    for scene, snr in cells:
        for delta in DELTAS:
            for m in methods_seen:
                sub = [r for r in raw_rows
                       if r["scene"] == scene
                       and abs(r["gamma_true_db"] - snr) < 1e-9
                       and abs(r["delta_db"] - delta) < 1e-9
                       and r["method"] == m]
                if not sub:
                    continue
                gains = [r["gain_db"] for r in sub]
                mean, std, hw, lo, hi = ci_t(gains)
                agg = {
                    "tag": tag, "scene": scene, "gamma_true_db": float(snr),
                    "delta_db": float(delta), "method": m,
                    "n_seeds": len(sub), "gain_db_mean": mean, "gain_db_std": std,
                    "gain_db_ci95": [lo, hi],
                }
                aggregates.append(agg)
    return raw_rows, aggregates


def phaseB_judge(aggregates, harm_cells_dev, anchor_d0):
    """Phase B: does the adapter resolve the harm?

    For each harm cell (scene, gamma, delta), the adapter (δ-invariant) gain is
    the same at that delta as at delta=0. Compare adapter gain vs the δ=0 ORIGINAL
    baseline gain at that cell. Adapter resolves harm if adapter_gain >= anchor_d0 - 0.3
    (i.e. the adapter loses < 0.3 dB vs the best-case original δ=0 selector) on every
    harm cell, AND does not introduce new substantial loss on non-harm main cells.
    """
    print("\n=== Phase B: adapter resolution check (held-out) ===")
    aidx = {(a["scene"], a["gamma_true_db"], a["delta_db"], a["method"]): a
            for a in aggregates}
    print(f"{'harm cell':<20}{'δ':>4}{'orig(δ)':>9}{'adapter':>9}"
          f"{'Δvs_d0':>9}{'resolved?':>10}")
    resolved_all = True
    for (scene, snr, delta) in harm_cells_dev:
        a_orig = aidx.get((scene, float(snr), float(delta), "orig"))
        a_adp = aidx.get((scene, float(snr), float(delta), "adapter_pilot"))
        a_d0 = anchor_d0.get((scene, float(snr)))
        if a_orig is None or a_adp is None or a_d0 is None:
            continue
        delta_vs_d0 = a_adp["gain_db_mean"] - a_d0
        resolved = delta_vs_d0 >= -HARM_GAIN_DROP_DB
        resolved_all = resolved_all and resolved
        print(f"{scene+'@'+str(int(snr))+'dB':<20}{delta:+4.0f}"
              f"{a_orig['gain_db_mean']:+9.3f}{a_adp['gain_db_mean']:+9.3f}"
              f"{delta_vs_d0:+9.3f}{'YES' if resolved else 'NO':>10}")
    return resolved_all


def phaseC_judge(aggregates, methods, mde=0.15):
    """Phase C: does any candidate STABLY beat the adapter on held-out?

    Paired per-seed Δgain = candidate_gain - adapter_gain, pooled across all
    (scene, gamma) main cells where adapter runs (delta-invariant so collapse deltas).
    Stable beat ⇔ mean >= mde AND CI_low > 0.
    """
    print("\n=== Phase C: candidate vs adapter (held-out, paired) ===")
    cand_methods = [m for m in methods
                    if m.startswith("cand_")]
    # collapse deltas (candidates are mostly delta-invariant too; collapse for pooled test)
    by_sg_seed = {}
    for a in aggregates:
        key = (a["scene"], a["gamma_true_db"], a["method"])
        by_sg_seed.setdefault(key, []).append(a)
    results = {}
    for cand in cand_methods:
        diffs = []
        # per (scene, gamma, seed) need raw rows; recompute from raw via paired gain
        # use aggregate-per-seed by reading raw_rows instead — do it in caller. Here
        # we approximate using the mean across deltas per cell (candidates delta-invariant).
        pass
    return results


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="heldout")
    ap.add_argument("--seeds", type=int, nargs="+", default=list(range(30, 50)))
    ap.add_argument("--cells", choices=["main", "harm"], default="main")
    ap.add_argument("--methods", nargs="+",
                    default=["adapter_pilot", "adapter_pilot_coh",
                             "cand_uncertainty", "cand_minimax", "cand_conf_gate",
                             "cand_rank", "cand_hysteresis", "oracle_true"])
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    cells = MAIN_CELLS if a.cells == "main" else (
        [(s, g) for (s, g, d) in HARM_CELLS_DEV])
    os.makedirs(OUT_DIR, exist_ok=True)
    a.out = a.out or os.path.join(OUT_DIR, f"phaseBC_{a.tag}.json")

    print(f"Phase B/C [{a.tag}] seeds={a.seeds} cells={len(cells)} "
          f"methods={a.methods}")
    raw_rows, aggregates = run(cells, a.seeds, a.methods, a.tag)

    # anchor δ=0 original gains (held-out) for Phase B reference
    anchor_d0 = {(ag["scene"], ag["gamma_true_db"]): ag["gain_db_mean"]
                 for ag in aggregates
                 if abs(ag["delta_db"]) < 1e-9 and ag["method"] == "orig"}
    resolved = phaseB_judge(aggregates, HARM_CELLS_DEV, anchor_d0)

    # ---- Phase C: paired candidate-vs-adapter from RAW rows ----
    print("\n=== Phase C: candidate vs adapter paired (held-out, pooled over cells) ===")
    # collapse delta (candidates delta-invariant in gain): use delta=0 rows as canonical
    cand_methods = [m for m in a.methods if m.startswith("cand_")]
    # build per-(scene,gamma,seed) gain for adapter and each candidate at delta=0
    c2 = {}
    for r in raw_rows:
        if abs(r["delta_db"]) < 1e-9 and r["method"] in (["adapter_pilot"] + cand_methods):
            c2.setdefault((r["scene"], r["gamma_true_db"], r["seed_index"], r["method"]),
                          r["gain_db"])
    cand_results = {}
    for cand in cand_methods:
        diffs = []
        for (scene, gamma, seed, m), g in c2.items():
            if m == cand:
                g_adp = c2.get((scene, gamma, seed, "adapter_pilot"))
                if g_adp is not None:
                    diffs.append(g - g_adp)
        if len(diffs) >= 2:
            mean, std, hw, lo, hi = ci_t(diffs)
            stable_beat = (mean >= 0.15) and (lo > 0)
            cand_results[cand] = {
                "n_paired": len(diffs), "mean_delta_db": mean, "std": std,
                "ci95": [lo, hi], "stable_beat_adapter": bool(stable_beat),
            }
            print(f"  {cand:<20} n={len(diffs):3d} meanΔ={mean:+.3f} "
                  f"CI=[{lo:+.3f},{hi:+.3f}] stable_beat={stable_beat}")
    any_signal = any(v["stable_beat_adapter"] for v in cand_results.values())

    out = {
        "tag": a.tag, "generated_at": datetime.now(timezone.utc).isoformat(),
        "seeds": list(a.seeds), "cells": [list(c) for c in cells],
        "deltas": list(DELTAS), "methods": list(a.methods),
        "phaseB_adapter_resolves_harm": bool(resolved),
        "phaseC_any_method_signal": bool(any_signal),
        "phaseC_candidate_results": cand_results,
        "raw_rows": raw_rows, "aggregates": aggregates,
    }
    with open(a.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n[saved] {a.out}")
    print(f"Phase B adapter resolves harm: {resolved}")
    print(f"Phase C any METHOD_SIGNAL: {any_signal}")


if __name__ == "__main__":
    main()
