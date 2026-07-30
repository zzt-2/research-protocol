# -*- coding: utf-8 -*-
"""P04 Phase A — problem-bearing probe on the continuous-GG dev grid.

Frozen criterion (worker-log step-031 §1.1): selector-specific regret exists iff
  (P1) orig selected_errors > lower_count_bound on the cell (selector picks worse branch),
  (P2) pooled regret_db(orig vs best-fixed-branch) >= MDE=0.15 with CI_low>0 on held-out,
  (P3) failure is NOT just common-branch degradation (both fixed branches do not collapse
       together; the selector had a real branch to choose).

regret_db(cell, method) = 10*log10(method_errors / min(fixed_DA, fixed_NDA))  [>=0 always].
"""
import os
import sys
import json
import time

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
sys.path[:0] = [_SIM_ROOT, os.path.join(_SIM_ROOT, 'simulator'), _HERE]

import _p04_continuous_gg as P4  # noqa: E402

OUT_DIR = os.path.join(_SIM_ROOT, "results", "p04_continuous_gg_ood")


def run_grid(sigma2_list, seeds, tag):
    """Run full grid; return raw_rows (per cell per seed) + per-(sigma2,gamma) aggregates."""
    t0 = time.time()
    raw_rows = []
    for s2 in sigma2_list:
        a, b = P4.sigma2_to_ab(s2)
        is_anchor = s2 in P4.FROZEN_ANCHOR_AB
        for gamma_db in P4.SNR_DB:
            for seed in seeds:
                r = P4.run_case_contgg(a, b, gamma_db, seed)
                base = r["base"]
                orig = r["orig"]
                fixed_DA = base["fixed_da_errors"]
                fixed_NDA = base["fixed_nda_errors"]
                best_fixed = min(fixed_DA, fixed_NDA)
                sel = orig["selected_errors"]
                # regret vs best fixed branch (>=0); guard log of 0
                regret_sel = float(10 * np.log10(sel / best_fixed)) if sel > 0 and best_fixed > 0 else float("inf")
                # how much worse is each fixed branch vs best (P3: common-collapse check)
                regret_DA = float(10 * np.log10(fixed_DA / best_fixed)) if fixed_DA > 0 else float("inf")
                regret_NDA = float(10 * np.log10(fixed_NDA / best_fixed)) if fixed_NDA > 0 else float("inf")
                raw_rows.append({
                    "tag": tag, "sigma2": float(s2), "alpha": float(a), "beta": float(b),
                    "is_anchor": bool(is_anchor), "gamma_db": float(gamma_db),
                    "seed_index": int(seed),
                    "fixed_DA_errors": int(fixed_DA), "fixed_NDA_errors": int(fixed_NDA),
                    "best_fixed_errors": int(best_fixed),
                    "lower_count_bound_errors": int(base["lower_count_bound_errors"]),
                    "true_oracle_errors": int(base["true_oracle_errors"]),
                    "selected_errors": int(sel),
                    "n_select_da": int(orig["n_select_da"]),
                    "n_select_nda": int(orig["n_select_nda"]),
                    "regret_sel_db": regret_sel,
                    "regret_DA_db": regret_DA, "regret_NDA_db": regret_NDA,
                    # gain vs fixed-NDA (P01 convention, for cross-check)
                    "gain_vs_NDA_db": float(10 * np.log10(fixed_NDA / sel)) if sel > 0 else float("inf"),
                })
    elapsed = time.time() - t0
    return raw_rows, elapsed


def aggregate(raw_rows):
    """Per-(sigma2,gamma) mean regret + CI; pooled over interior held-out cells."""
    from collections import defaultdict
    by_cell = defaultdict(list)
    for r in raw_rows:
        by_cell[(r["sigma2"], r["gamma_db"])].append(r)
    aggs = []
    for (s2, g), rows in sorted(by_cell.items()):
        regrets = [r["regret_sel_db"] for r in rows if np.isfinite(r["regret_sel_db"])]
        if not regrets:
            continue
        mean, std, hw, lo, hi = P4.ci_t(regrets)
        # branch occupancy + P3 common-collapse: mean regret of DA and NDA vs best
        rDA = [r["regret_DA_db"] for r in rows if np.isfinite(r["regret_DA_db"])]
        rNDA = [r["regret_NDA_db"] for r in rows if np.isfinite(r["regret_NDA_db"])]
        sel_DA = np.mean([r["n_select_da"] for r in rows])
        aggs.append({
            "sigma2": float(s2), "gamma_db": float(g),
            "is_anchor": rows[0]["is_anchor"], "alpha": rows[0]["alpha"], "beta": rows[0]["beta"],
            "n_seeds": len(rows),
            "regret_sel_mean": mean, "regret_sel_ci_lo": lo, "regret_sel_ci_hi": hi,
            "mean_regret_DA": float(np.mean(rDA)) if rDA else None,
            "mean_regret_NDA": float(np.mean(rNDA)) if rNDA else None,
            "mean_n_select_da": float(sel_DA),
            "mean_gain_vs_NDA": float(np.mean([r["gain_vs_NDA_db"] for r in rows if np.isfinite(r["gain_vs_NDA_db"])])),
        })
    return aggs


def judge(aggs, mde=P4.MDE, interior_only=True):
    """Phase A problem gate on pooled interior-cell regret."""
    sel = [a for a in aggs if (not a["is_anchor"]) or (not interior_only)]
    regrets = [a["regret_sel_mean"] for a in sel]
    mean, std, hw, lo, hi = P4.ci_t(regrets) if regrets else (0, 0, 0, 0, 0)
    # P3: are there interior cells where both fixed branches are far from best (common collapse)?
    # selector-specific requires the selector to have a real choice: at regret-bearing cells,
    # min(fixed_DA,fixed_NDA) should be meaningfully < max (branch difference exists).
    problem = (mean >= mde) and (lo > 0)
    print(f"\n=== Phase A problem gate ({'interior-only' if interior_only else 'all'} pooled) ===")
    print(f"  n_cells={len(regrets)} pooled mean regret_sel = {mean:+.4f} dB  CI=[{lo:+.4f},{hi:+.4f}]")
    print(f"  MDE={mde}  =>  problem_holds = {problem}")
    # per-cell breakdown
    print("\n  per-cell (sigma2, gamma) mean regret_sel_db  [is_anchor]:")
    for a in sorted(aggs, key=lambda x: (x["sigma2"], x["gamma_db"])):
        flag = "ANCHOR" if a["is_anchor"] else "interior"
        mark = "  <-- >=MDE & CI_lo>0" if (a["regret_sel_mean"] >= mde and a["regret_sel_ci_lo"] > 0) else ""
        print(f"    s2={a['sigma2']:.2f} (a={a['alpha']:.2f},b={a['beta']:.2f}) g={a['gamma_db']:.0f} "
              f"regret={a['regret_sel_mean']:+.4f} [{a['regret_sel_ci_lo']:+.4f},{a['regret_sel_ci_hi']:+.4f}] "
              f"DAocc={a['mean_n_select_da']:.0f} [{flag}]{mark}")
    # anchor regression sanity: anchor cells should have ~0 regret (selector trained there)
    anchor_reg = [a["regret_sel_mean"] for a in aggs if a["is_anchor"]]
    print(f"\n  anchor-cell mean regret (should be ~0 / non-positive if trained): "
          f"{np.mean(anchor_reg) if anchor_reg else float('nan'):+.4f} dB over {len(anchor_reg)} cells")
    return {"problem_holds": bool(problem), "pooled_mean": mean, "pooled_ci_lo": lo,
            "pooled_ci_hi": hi, "n_cells": len(regrets)}


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print("=== Phase A dev grid (9 sigma^2 x 5 SNR x 10 seeds = 450 cells) ===")
    raw, elapsed = run_grid(P4.DEV_SIGMA2, P4.DEV_SEEDS, "dev")
    aggs = aggregate(raw)
    verdict = judge(aggs)
    out = {
        "phase": "A_dev", "tag": "dev", "sigma2_grid": list(P4.DEV_SIGMA2),
        "snr_db": list(P4.SNR_DB), "seeds": list(P4.DEV_SEEDS), "mde": P4.MDE,
        "n_raw_rows": len(raw), "elapsed_s": elapsed,
        "raw_rows": raw, "aggregates": aggs, "verdict": verdict,
    }
    with open(os.path.join(OUT_DIR, "phaseA_dev.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nwrote {len(raw)} raw rows -> {os.path.join(OUT_DIR, 'phaseA_dev.json')} ({elapsed:.1f}s)")
    return verdict


if __name__ == "__main__":
    main()
