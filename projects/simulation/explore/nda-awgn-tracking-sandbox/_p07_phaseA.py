# -*- coding: utf-8 -*-
"""P07 (family F) Phase A — problem existence under fixed-gain ADC (BATCHED + MP).

FROZEN BEFORE reading any result (FROZEN_CONTRACT.md §4):
  - MDE = 0.15 dB; >= 3 cells must pass; cross-bitwidth consistent.
  - Problem-gate: dev-tuned BEST fixed-gain ADC at bitwidth W has paired regret
    vs ideal float ADC with pooled mean >= MDE AND pooled CI_lo > 0, AND this
    holds CONSISTENTLY across {6,8,10} bit.
  - Fixed-gain ladder (pre-registered): {0.5,0.75,1.0,1.25,1.5,2.0,2.5,3.0,4.0}.
  - Phase-A dev grid (representative subset, see FROZEN_CONTRACT §4):
    scenes {weak,moderate,strong} x SNR {5,9,13,17,21} dB x dev seeds {0..4}
    = 75 cells.
  - oracle per-block gain = headroom/Kill bound ONLY.

Uses _p07_batch.eval_cell_fixed_gains (ONE channel gen per cell, all 28 configs
on identical channel). multiprocessing across cells.

paired_regret_dB = 10*log10(selected_errors_ADC / selected_errors_idealfloat).
"""
import os
import sys
import json
import time
from multiprocessing import Pool

import numpy as np
from scipy import stats

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
sys.path[:0] = [_SIM_ROOT, os.path.join(_SIM_ROOT, 'simulator'), _HERE]

import _p07_adapters as AD  # noqa: E402
import _p07_batch as BATCH  # noqa: E402
from common import save_results  # noqa: E402

# Phase-A dev grid (FROZEN representative subset).
SCENES = ("weak", "moderate", "strong")
SNR_DB = (5.0, 9.0, 13.0, 17.0, 21.0)   # 5 points spanning low-mid-high
DEV_SEEDS = (0, 1, 2, 3, 4)             # 5 dev seeds
BITWIDTHS = AD.BITWIDTHS                 # (6, 8, 10)
FIXED_GAINS = AD.FIXED_GAIN_LADDER
MDE = 0.15
N_WORKERS = min(24, os.cpu_count() or 8)

OUT_DIR = os.path.join(_SIM_ROOT, "results", "p07_agc_adc_dynamic_range")
OUT_PHASEA = os.path.join(OUT_DIR, "p07_phaseA_dev.json")


def ci_t(data):
    a = np.asarray(data, dtype=float)
    n = len(a)
    mean = float(np.mean(a)) if n else float("nan")
    std = float(np.std(a, ddof=1)) if n > 1 else 0.0
    hw = float(stats.t.ppf(0.975, n - 1)) * std / np.sqrt(n) if n > 1 else 0.0
    return {"mean": mean, "std": std, "hw": hw, "ci_lo": mean - hw, "ci_hi": mean + hw, "n": n}


def _build_configs():
    cfgs = [{"gain": 1.0, "W": AD.FLOAT_BYPASS_W, "fs": AD.FLOAT_BYPASS_FS,
             "tag": "ideal_float"}]
    for W in BITWIDTHS:
        for gain in FIXED_GAINS:
            cfgs.append({"gain": gain, "W": W, "fs": AD.FS,
                         "tag": f"fixed_g{gain:g}_W{W}"})
    return cfgs


def _worker(args):
    """Worker: evaluate one cell. Must re-import (fork/spawn safe on win = spawn)."""
    scene, g, seed, configs = args
    cell = BATCH.eval_cell_fixed_gains(scene, g, seed, configs)
    idl_sel = cell["ideal_float"]["selected_errors"]
    rows = []
    for c in configs:
        if c["tag"] == "ideal_float":
            continue
        row = cell[c["tag"]]
        sel = row["selected_errors"]
        regret = 10.0 * np.log10(sel / idl_sel) if idl_sel > 0 else 0.0
        rows.append({
            "scene": scene, "gamma_true_db": float(g),
            "seed": int(seed), "W": int(c["W"]), "gain": float(c["gain"]),
            "selected_errors": int(sel),
            "ideal_float_selected_errors": int(idl_sel),
            "fixed_da_errors": int(row["fixed_da_errors"]),
            "fixed_nda_errors": int(row["fixed_nda_errors"]),
            "clipping_rate": float(row["mean_clipping_rate"]),
            "code_utilization": float(row["mean_code_utilization"]),
            "paired_regret_dB": float(regret),
        })
    return rows


def main():
    t0 = time.time()
    configs = _build_configs()
    tasks = [(sc, g, seed, configs)
             for sc in SCENES for g in SNR_DB for seed in DEV_SEEDS]
    print(f"Phase A (MP): {len(tasks)} cells x {len(configs)} configs, "
          f"{N_WORKERS} workers ...", flush=True)

    raw_rows = []
    with Pool(N_WORKERS) as pool:
        for i, rows in enumerate(pool.imap_unordered(_worker, tasks)):
            raw_rows.extend(rows)
            if (i + 1) % 15 == 0:
                print(f"  {i+1}/{len(tasks)} cells ({round(time.time()-t0,1)}s)", flush=True)
    print(f"  all {len(tasks)} cells done ({round(time.time()-t0,1)}s)", flush=True)

    # dev-aggregate: per-bitwidth BEST fixed gain (min pooled regret)
    per_bitwidth = {}
    for W in BITWIDTHS:
        best_gain = None
        best_mean = float("inf")
        gain_summary = {}
        for gain in FIXED_GAINS:
            rows = [r for r in raw_rows if r["W"] == W and r["gain"] == gain]
            ci = ci_t([r["paired_regret_dB"] for r in rows])
            gain_summary[f"{gain:g}"] = ci
            if ci["mean"] < best_mean:
                best_mean = ci["mean"]
                best_gain = gain
        best_rows = [r for r in raw_rows if r["W"] == W and r["gain"] == best_gain]
        pooled = ci_t([r["paired_regret_dB"] for r in best_rows])
        per_cell = {}
        cells_passing = 0
        for scene in SCENES:
            for g in SNR_DB:
                cell_rows = [r for r in best_rows
                             if r["scene"] == scene and r["gamma_true_db"] == g]
                cci = ci_t([r["paired_regret_dB"] for r in cell_rows])
                per_cell[f"{scene}|{g:g}"] = cci
                if cci["mean"] >= MDE and cci["ci_lo"] > 0:
                    cells_passing += 1
        per_bitwidth[f"W{W}"] = {
            "best_gain": best_gain,
            "pooled_regret_dB": pooled,
            "n_cells_passing_mde": cells_passing,
            "per_cell_regret_dB": per_cell,
            "gain_ladder_summary": gain_summary,
        }

    bitwidths_pass = []
    for W in BITWIDTHS:
        pb = per_bitwidth[f"W{W}"]
        pooled_pass = (pb["pooled_regret_dB"]["mean"] >= MDE
                       and pb["pooled_regret_dB"]["ci_lo"] > 0)
        cells_pass = pb["n_cells_passing_mde"] >= 3
        bitwidths_pass.append(pooled_pass and cells_pass)
    cross_consistent = all(bitwidths_pass)
    problem_established = bool(cross_consistent)

    out = {
        "package": "P07", "family": "F_AGC_ADC_DYNAMIC_RANGE_UNDER_GG",
        "phase": "A_dev",
        "frozen": {"MDE": MDE, "bitwidths": list(BITWIDTHS),
                   "fixed_gain_ladder": list(FIXED_GAINS),
                   "dev_seeds": list(DEV_SEEDS),
                   "dev_snr_grid": list(SNR_DB),
                   "min_cells_passing": 3, "fs": AD.FS,
                   "n_workers": N_WORKERS},
        "n_raw_rows": len(raw_rows),
        "per_bitwidth": per_bitwidth,
        "cross_bitwidth_consistent": cross_consistent,
        "problem_established": problem_established,
        "elapsed_s": round(time.time() - t0, 1),
        "raw_rows": raw_rows,
    }
    os.makedirs(OUT_DIR, exist_ok=True)
    save_results(out, OUT_PHASEA, os.path.basename(__file__))
    summary = {
        "problem_established": problem_established,
        "cross_bitwidth_consistent": cross_consistent,
        "per_bitwidth_pooled": {str(W): {
            "best_gain": per_bitwidth[f"W{W}"]["best_gain"],
            "pooled_mean": per_bitwidth[f"W{W}"]["pooled_regret_dB"]["mean"],
            "pooled_ci_lo": per_bitwidth[f"W{W}"]["pooled_regret_dB"]["ci_lo"],
            "pooled_ci_hi": per_bitwidth[f"W{W}"]["pooled_regret_dB"]["ci_hi"],
            "n_cells_passing": per_bitwidth[f"W{W}"]["n_cells_passing_mde"],
        } for W in BITWIDTHS},
        "elapsed_s": out["elapsed_s"],
    }
    print(json.dumps(summary, indent=2))
    return out


if __name__ == "__main__":
    main()
