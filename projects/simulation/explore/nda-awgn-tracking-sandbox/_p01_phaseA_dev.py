# -*- coding: utf-8 -*-
"""P01 Phase A.5 — dev mismatch scan + harm judgment.

Runs the 15 main cells (weak/moderate/strong × {5,7,9,11,13} dB) × 7 deltas
× dev seeds 0-9, computes per-seed common-768 gain_db and paired Δgain(δ)
vs δ=0, then applies the FROZEN substantial-harm criterion:
  harm ⇔ mean(Δgain(δ)) ≤ −0.3 dB AND CI95_high(Δgain(δ)) < 0 dB.

Outputs the raw per-seed rows + per-(scene,γ,δ) paired aggregate + CI, and
prints a verdict table. Saves artifacts to results/p01_cpr_snr_mismatch/.
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

from _p01_cpr_snr_mismatch_probe import run_case_multidelta, DELTAS, N_WINDOWS  # noqa: E402

# Frozen criterion (must match worker-log §1)
HARM_GAIN_DROP_DB = 0.3
MAIN_CELLS = [
    ("weak", 5.0), ("weak", 7.0), ("weak", 9.0), ("weak", 11.0), ("weak", 13.0),
    ("moderate", 5.0), ("moderate", 7.0), ("moderate", 9.0), ("moderate", 11.0), ("moderate", 13.0),
    ("strong", 5.0), ("strong", 7.0), ("strong", 9.0), ("strong", 11.0), ("strong", 13.0),
]
ANCHOR_GAIN_FLOOR = 0.5   # only judge cells with anchor gain ≥ 0.5 dB

OUT_DIR = os.path.join(_SIM_ROOT, "results", "p01_cpr_snr_mismatch")


def ci_t(data):
    """Match anchor ci_t: two-sided Student-t 95% half-width."""
    a = np.asarray(data, dtype=float)
    n = len(a)
    mean = float(np.mean(a))
    std = float(np.std(a, ddof=1)) if n > 1 else 0.0
    hw = float(stats.t.ppf(0.975, n - 1)) * std / np.sqrt(n) if n > 1 else 0.0
    return mean, std, hw, mean - hw, mean + hw


def run_scan(seeds, tag, cells=MAIN_CELLS, deltas=DELTAS, extra_selector=None):
    """Run the mismatch scan; return raw_rows + aggregates."""
    t0 = time.time()
    raw_rows = []
    # per_window choice flips bookkeeping for semantic smoke
    for ci, (scene, snr) in enumerate(cells):
        for seed in seeds:
            md = run_case_multidelta(scene, snr, seed, deltas=deltas,
                                     extra_selector=extra_selector)
            base = md["base"]
            nda_common = base["fixed_nda_errors"]
            da_common = base["fixed_da_errors"]
            lcb = base["lower_count_bound_errors"]
            tor = base["true_oracle_errors"]
            tob = base["true_oracle_bits"]
            # baseline (delta=0) choices for selection-error-rate computation
            base_choices = md["per_delta_orig"][0.0]["choices"]
            for delta in deltas:
                per = md["per_delta_orig"][delta]
                sel = per["selected_errors"]
                n_da = per["n_select_da"]
                n_nda = per["n_select_nda"]
                flips = sum(1 for a, b in zip(base_choices, per["choices"]) if a != b)
                gain_db = 10 * np.log10(nda_common / sel) if sel > 0 else float("inf")
                row = {
                    "tag": tag,
                    "scene": scene,
                    "gamma_true_db": float(snr),
                    "delta_db": float(delta),
                    "gamma_hat_db": float(snr + delta),
                    "seed_index": int(seed),
                    "n_windows": int(N_WINDOWS),
                    "n_bits_common768": int(N_WINDOWS * 768),
                    "fixed_nda_errors_common768": int(nda_common),
                    "fixed_da_errors_common768": int(da_common),
                    "lower_count_bound_errors": int(lcb),
                    "true_oracle_errors": int(tor),
                    "true_oracle_bits": int(tob),
                    "selected_errors_common768": int(sel),
                    "n_select_da": int(n_da),
                    "n_select_nda": int(n_nda),
                    "selection_error_rate_vs_d0": float(flips / N_WINDOWS),
                    "gain_db_common768": float(gain_db),
                }
                # extra selectors (adapter / candidates), same channel
                if extra_selector is not None and "per_delta_extra" in md:
                    for name, permap in md["per_delta_extra"].items():
                        pe = permap[delta]
                        row[f"selected_errors_{name}"] = int(pe["selected_errors"])
                        row[f"n_select_da_{name}"] = int(pe["n_select_da"])
                        row[f"n_select_nda_{name}"] = int(pe["n_select_nda"])
                        row[f"gain_db_{name}"] = float(
                            10 * np.log10(nda_common / pe["selected_errors"])
                            if pe["selected_errors"] > 0 else float("inf"))
                raw_rows.append(row)
        print(f"  [{tag}] {scene}@{snr:.0f}dB done ({ci+1}/{len(cells)} cells, "
              f"{time.time()-t0:.0f}s)", flush=True)

    # ---- aggregates: per (scene, gamma_true, delta) paired across seeds ----
    aggregates = []
    for scene, snr in cells:
        for delta in deltas:
            sub = [r for r in raw_rows
                   if r["scene"] == scene
                   and abs(r["gamma_true_db"] - snr) < 1e-9
                   and abs(r["delta_db"] - delta) < 1e-9]
            gains = [r["gain_db_common768"] for r in sub]
            mean, std, hw, lo, hi = ci_t(gains)
            # paired Δgain vs δ=0: per seed (gain(δ) - gain(0))
            if delta != 0.0:
                d0 = {(r["scene"], r["gamma_true_db"], r["seed_index"]): r["gain_db_common768"]
                      for r in raw_rows
                      if abs(r["delta_db"]) < 1e-9}
                deltas_paired = []
                for r in sub:
                    g0 = d0.get((r["scene"], r["gamma_true_db"], r["seed_index"]))
                    if g0 is not None:
                        deltas_paired.append(r["gain_db_common768"] - g0)
                m_d, s_d, hw_d, lo_d, hi_d = ci_t(deltas_paired) if deltas_paired else (None,)*5
            else:
                m_d = s_d = hw_d = lo_d = hi_d = None
                deltas_paired = []
            n_da_mean = float(np.mean([r["n_select_da"] for r in sub]))
            n_nda_mean = float(np.mean([r["n_select_nda"] for r in sub]))
            ser_mean = float(np.mean([r["selection_error_rate_vs_d0"] for r in sub]))
            agg = {
                "tag": tag, "scene": scene, "gamma_true_db": float(snr),
                "delta_db": float(delta),
                "n_seeds": int(len(sub)),
                "gain_db_mean": mean, "gain_db_std": std,
                "gain_db_ci95": [lo, hi],
                "delta_gain_vs_d0_mean": m_d, "delta_gain_vs_d0_std": s_d,
                "delta_gain_vs_d0_ci95": [lo_d, hi_d] if lo_d is not None else None,
                "n_select_da_mean": n_da_mean, "n_select_nda_mean": n_nda_mean,
                "selection_error_rate_mean": ser_mean,
            }
            # extra-selector aggregates
            for r in sub:
                pass  # handled below if needed
            aggregates.append(agg)
    return raw_rows, aggregates


def judge(aggregates, tag):
    """Apply frozen substantial-harm criterion. Returns list of harm cells."""
    print(f"\n=== Harm judgment [{tag}] (frozen: mean Δgain ≤ −0.3 dB AND CI_high < 0) ===")
    print(f"{'cell':<20}{'d':>5}{'gain_d':>8}{'Δgain':>9}{'CI95[lo,hi]':>20}{'harm?':>8}")
    harm_cells = []
    # gather anchor (δ=0) gains to filter by ANCHOR_GAIN_FLOOR
    anchor_gain = {}
    for a in aggregates:
        if abs(a["delta_db"]) < 1e-9:
            anchor_gain[(a["scene"], a["gamma_true_db"])] = a["gain_db_mean"]
    for a in aggregates:
        if abs(a["delta_db"]) < 1e-9:
            continue
        ag = anchor_gain.get((a["scene"], a["gamma_true_db"]), 0.0)
        if ag < ANCHOR_GAIN_FLOOR:
            continue   # only judge cells with anchor gain ≥ 0.5 dB
        m_d = a["delta_gain_vs_d0_mean"]
        ci = a["delta_gain_vs_d0_ci95"]
        if m_d is None or ci is None:
            continue
        harm = (m_d <= -HARM_GAIN_DROP_DB) and (ci[1] < 0)
        cell = f"{a['scene']}@{a['gamma_true_db']:.0f}dB"
        ci_str = f"[{ci[0]:+.3f},{ci[1]:+.3f}]" if ci else "   n/a   "
        print(f"{cell:<20}{a['delta_db']:+5.0f}{a['gain_db_mean']:+8.3f}"
              f"{m_d:+9.3f}{ci_str:>20}{'HARM' if harm else '':>8}")
        if harm:
            harm_cells.append((a["scene"], a["gamma_true_db"], a["delta_db"], m_d, ci))
    return harm_cells, anchor_gain


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="dev")
    ap.add_argument("--seeds", type=int, nargs="+", default=list(range(10)))
    ap.add_argument("--out", default=os.path.join(OUT_DIR, "phaseA_dev.json"))
    a = ap.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"Phase A scan [{a.tag}] seeds={a.seeds} cells={len(MAIN_CELLS)} "
          f"deltas={list(DELTAS)} → {len(MAIN_CELLS)*len(DELTAS)*len(a.seeds)} runs")
    raw_rows, aggregates = run_scan(a.seeds, a.tag)

    harm_cells, anchor_gain = judge(aggregates, a.tag)
    print(f"\nAnchor (δ=0) common-768 gains [dB]:")
    for (sc, sn), g in sorted(anchor_gain.items()):
        flag = "  (≥0.5, judged)" if g >= ANCHOR_GAIN_FLOOR else "  (<0.5, not judged)"
        print(f"  {sc}@{sn:.0f}dB: {g:+.3f}{flag}")
    print(f"\nSubstantial-harm cells: {len(harm_cells)}")
    for h in harm_cells:
        print(f"  {h[0]}@{h[1]:.0f}dB δ={h[2]:+.0f}: Δgain={h[3]:+.3f} CI={h[4]}")

    verdict = ("PROBLEM_ABSENT_UNDER_TESTED_MISMATCH" if not harm_cells
               else "PROBLEM_PRESENT (→ Phase B)")
    print(f"\n>>> PHASE A VERDICT [{a.tag}]: {verdict}")

    out = {
        "tag": a.tag,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "seeds": list(a.seeds),
        "cells": [list(c) for c in MAIN_CELLS],
        "deltas": list(DELTAS),
        "criterion": {
            "harm_gain_drop_db": HARM_GAIN_DROP_DB,
            "anchor_gain_floor_db": ANCHOR_GAIN_FLOOR,
            "ci_rule": "paired per-seed Δgain Student-t 95%, harm if mean≤-0.3 AND CI_high<0",
            "judged_deltas": [d for d in DELTAS if d != 0.0],
        },
        "anchor_gain_d0_db": {f"{s}|{g:g}": v for (s, g), v in anchor_gain.items()},
        "harm_cells": [{"scene": h[0], "gamma_true_db": h[1], "delta_db": h[2],
                        "delta_gain_mean": h[3], "delta_gain_ci95": h[4]}
                       for h in harm_cells],
        "verdict": verdict,
        "raw_rows": raw_rows,
        "aggregates": aggregates,
    }
    with open(a.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"[saved] {a.out}")


if __name__ == "__main__":
    main()
