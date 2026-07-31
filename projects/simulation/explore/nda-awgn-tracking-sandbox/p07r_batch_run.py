# -*- coding: utf-8 -*-
"""P07-R — Phase A (problem existence) + four-way decomposition (BATCHED + MP).

Frozen BEFORE reading results (D046 / FROZEN_CONTRACT §4):
  - MDE = 0.15 dB (unchanged from P07; no pre-registered reason to change).
  - At least 3 cells must pass the problem gate per bitwidth; cross-{6,8,10}
    consistent.
  - Problem gate: dev-tuned BEST fixed-gain full_adc, at bitwidth W, has paired
    regret (vs ideal_float = scale_only g=1) with pooled mean >= MDE AND
    CI_lo > 0, consistent across bitwidths.
  - Fixed-gain ladder (pre-registered): {0.5,0.75,1.0,1.25,1.5,2.0,2.5,3.0,4.0}.
  - rho levels via f_G in {30,100,1000} Hz at window_dt=56us -> rho ~0.99/0.97/0.70.
  - Seed isolation: dev seeds 300-309; held-out 500-519 (FRESH, disjoint from
    campaign history 0-99, 200-239, 500-519 used here only for P07-R; 71-80
    forbidden). Read fresh seeds only at adjudication.

Four-way decomposition (task section VI): scale_only / clip_only / quant_only /
full_adc are run on the SAME shared trajectory, isolating each impairment so we
can attribute residual regret to clipping / quantization / causal lag / scale.
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

import p07r_adapters as AD  # noqa: E402
import p07r_runner as R  # noqa: E402
from common import save_results  # noqa: E402

SCENES = ("weak", "moderate", "strong")
SNR_DB = (5.0, 9.0, 13.0, 17.0, 21.0)
DEV_SEEDS = tuple(range(300, 310))      # 10 fresh dev seeds
HELDOUT_SEEDS = tuple(range(500, 520))  # 20 fresh held-out seeds
BITWIDTHS = AD.BITWIDTHS
FIXED_GAINS = AD.FIXED_GAIN_LADDER
F_G_LEVELS = R.F_G_LEVELS
MDE = 0.15
N_WORKERS = min(24, os.cpu_count() or 8)

OUT_DIR = os.path.join(_SIM_ROOT, "results", "p07r_agc_adc_repair")
OUT_PHASEA = os.path.join(OUT_DIR, "p07r_phaseA_dev.json")
OUT_DECOMP = os.path.join(OUT_DIR, "p07r_fourway_decomp.json")


def ci_t(data):
    a = np.asarray(data, dtype=float)
    n = len(a)
    mean = float(np.mean(a)) if n else float("nan")
    std = float(np.std(a, ddof=1)) if n > 1 else 0.0
    hw = float(stats.t.ppf(0.975, n - 1)) * std / np.sqrt(n) if n > 1 else 0.0
    return {"mean": mean, "std": std, "hw": hw, "ci_lo": mean - hw,
            "ci_hi": mean + hw, "n": n}


def _fixed_configs(W, include_decomp=False):
    cfgs = [{"gain": 1.0, "W": AD.FLOAT_BYPASS_W, "fs": AD.FLOAT_BYPASS_FS,
             "decomp": "scale_only", "tag": "ideal_float"}]
    for g in FIXED_GAINS:
        cfgs.append({"gain": g, "W": W, "fs": AD.FS, "decomp": "full_adc",
                     "tag": f"g{g:g}_W{W}"})
    if include_decomp:
        for d in ("scale_only", "clip_only", "quant_only"):
            cfgs.append({"gain": 1.0, "W": W, "fs": AD.FS, "decomp": d,
                         "tag": f"decomp_{d}_g1.0_W{W}"})
    return cfgs


def _worker_phaseA(args):
    """One (scene, snr, f_G, seed) cell -> rows for all (gain,W) configs.

    Builds ONE shared trajectory and evaluates ALL bitwidths in a single pass
    (the trajectory is shared; only the ADC differs per config). ideal_float is
    computed once on the scale_only arm and reused as the regret reference.
    """
    scene, g, fG, seed = args
    wins, _ = R.make_trajectory(scene, g, fG, seed)
    # one combined config list: ideal_float + all (W,gain) full_adc
    cfgs = [{"gain": 1.0, "W": AD.FLOAT_BYPASS_W, "fs": AD.FLOAT_BYPASS_FS,
             "decomp": "scale_only", "tag": "ideal_float"}]
    for W in BITWIDTHS:
        for gain in FIXED_GAINS:
            cfgs.append({"gain": gain, "W": W, "fs": AD.FS, "decomp": "full_adc",
                         "tag": f"g{gain:g}_W{W}"})
    res = R.eval_cell_fixed_gains(wins, g, cfgs)
    idl = res["ideal_float"]["selected_errors"]
    rows = []
    for c in cfgs:
        if c["tag"] == "ideal_float":
            continue
        r = res[c["tag"]]
        sel = r["selected_errors"]
        regret = 10.0 * np.log10(sel / idl) if idl > 0 else 0.0
        rows.append({
            "scene": scene, "gamma_true_db": float(g), "f_G": float(fG),
            "seed": int(seed), "W": int(c["W"]), "gain": float(c["gain"]),
            "selected_errors": int(sel),
            "ideal_float_selected_errors": int(idl),
            "fixed_da_errors": int(r["fixed_da_errors"]),
            "fixed_nda_errors": int(r["fixed_nda_errors"]),
            "clipping_rate": float(r["mean_clipping_rate"]),
            "paired_regret_dB": float(regret),
        })
    return rows


def run_phaseA(seeds):
    t0 = time.time()
    tasks = [(sc, g, fG, seed) for fG in F_G_LEVELS for sc in SCENES
             for g in SNR_DB for seed in seeds]
    print(f"Phase A (MP): {len(tasks)} cells x {len(BITWIDTHS)*len(FIXED_GAINS)} "
          f"gains, {N_WORKERS} workers ...", flush=True)
    raw = []
    with Pool(N_WORKERS) as pool:
        for i, rows in enumerate(pool.imap_unordered(_worker_phaseA, tasks)):
            raw.extend(rows)
            if (i + 1) % 30 == 0:
                print(f"  {i+1}/{len(tasks)} cells ({round(time.time()-t0,1)}s)", flush=True)
    print(f"  all {len(tasks)} cells done ({round(time.time()-t0,1)}s)", flush=True)

    # aggregate per (f_G, W): best fixed gain by min pooled regret across all cells
    out_perFG = {}
    for fG in F_G_LEVELS:
        perW = {}
        for W in BITWIDTHS:
            best_g, best_mean = None, float("inf")
            gsum = {}
            for gain in FIXED_GAINS:
                rows = [r for r in raw if r["f_G"] == fG and r["W"] == W
                        and r["gain"] == gain]
                ci = ci_t([r["paired_regret_dB"] for r in rows])
                gsum[f"{gain:g}"] = ci
                if ci["mean"] < best_mean:
                    best_mean, best_g = ci["mean"], gain
            best_rows = [r for r in raw if r["f_G"] == fG and r["W"] == W
                         and r["gain"] == best_g]
            pooled = ci_t([r["paired_regret_dB"] for r in best_rows])
            cells_pass = 0
            per_cell = {}
            for sc in SCENES:
                for g in SNR_DB:
                    cr = [r for r in best_rows if r["scene"] == sc
                          and r["gamma_true_db"] == g]
                    cci = ci_t([r["paired_regret_dB"] for r in cr])
                    per_cell[f"{sc}|{g:g}"] = cci
                    if cci["mean"] >= MDE and cci["ci_lo"] > 0:
                        cells_pass += 1
            perW[f"W{W}"] = {"best_gain": best_g, "pooled": pooled,
                             "n_cells_passing": cells_pass,
                             "per_cell": per_cell, "gain_summary": gsum}
        # cross-bitwidth problem gate for this f_G
        bw_pass = []
        for W in BITWIDTHS:
            p = perW[f"W{W}"]["pooled"]
            cp = perW[f"W{W}"]["n_cells_passing"]
            bw_pass.append(p["mean"] >= MDE and p["ci_lo"] > 0 and cp >= 3)
        out_perFG[f"fG{int(fG)}"] = {
            "rho": round(R.TR.rho_from_fG(fG, R.WINDOW_DT), 4),
            "per_bitwidth": perW,
            "problem_established": bool(all(bw_pass)),
        }
    return {"raw_rows": raw, "per_fG": out_perFG, "elapsed_s": round(time.time()-t0, 1)}


def run_fourway_decomp(seeds, W=8):
    """Four-way decomposition: scale_only/clip_only/quant_only/full_adc at g=1.0
    (best-fixed region) on the SAME shared trajectory, attributing regret."""
    t0 = time.time()
    rows = []
    for fG in F_G_LEVELS:
        for sc in SCENES:
            for g in SNR_DB:
                for seed in seeds:
                    wins, _ = R.make_trajectory(sc, g, fG, seed)
                    cfgs = [{"gain": 1.0, "W": AD.FLOAT_BYPASS_W,
                             "fs": AD.FLOAT_BYPASS_FS, "decomp": "scale_only",
                             "tag": "ideal_float"}]
                    for d in ("scale_only", "clip_only", "quant_only", "full_adc"):
                        cfgs.append({"gain": 1.0, "W": W, "fs": AD.FS,
                                     "decomp": d, "tag": d})
                    res = R.eval_cell_fixed_gains(wins, g, cfgs)
                    idl = res["ideal_float"]["selected_errors"]
                    for d in ("scale_only", "clip_only", "quant_only", "full_adc"):
                        sel = res[d]["selected_errors"]
                        regret = 10.0 * np.log10(sel / idl) if idl > 0 else 0.0
                        rows.append({"scene": sc, "gamma_true_db": float(g),
                                     "f_G": float(fG), "seed": int(seed),
                                     "decomp": d, "clipping_rate": float(res[d]["mean_clipping_rate"]),
                                     "paired_regret_dB": float(regret)})
    # aggregate per (f_G, decomp)
    agg = {}
    for fG in F_G_LEVELS:
        agg[f"fG{int(fG)}"] = {}
        for d in ("scale_only", "clip_only", "quant_only", "full_adc"):
            r = [x for x in rows if x["f_G"] == fG and x["decomp"] == d]
            agg[f"fG{int(fG)}"][d] = ci_t([x["paired_regret_dB"] for x in r])
    return {"W": W, "raw_rows": rows, "per_fG_decomp": agg,
            "elapsed_s": round(time.time() - t0, 1)}


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    t0 = time.time()
    print("=" * 60, "\nP07-R Phase A (problem existence, dev seeds 300-309)\n", "=" * 60)
    phaseA = run_phaseA(DEV_SEEDS)
    pa_out = {"package": "P07-R", "phase": "A_dev",
              "frozen": {"MDE": MDE, "bitwidths": list(BITWIDTHS),
                         "fixed_gain_ladder": list(FIXED_GAINS),
                         "dev_seeds": list(DEV_SEEDS), "snr_grid": list(SNR_DB),
                         "f_G_levels": list(F_G_LEVELS),
                         "window_dt": R.WINDOW_DT, "min_cells_passing": 3,
                         "fs": AD.FS},
              **phaseA}
    save_results(pa_out, OUT_PHASEA, os.path.basename(__file__))
    print("\n=== Phase A summary ===")
    for fGk, v in phaseA["per_fG"].items():
        print(f"{fGk} (rho={v['rho']}): problem_established={v['problem_established']}")
        for W in BITWIDTHS:
            p = v["per_bitwidth"][f"W{W}"]
            print(f"  W{W}: best_gain={p['best_gain']} pooled={p['pooled']['mean']:.4f} "
                  f"CI=[{p['pooled']['ci_lo']:.4f},{p['pooled']['ci_hi']:.4f}] "
                  f"cells_pass={p['n_cells_passing']}")

    print("\n" + "=" * 60, "\nP07-R four-way decomposition (dev seeds 300-309, W=8)\n", "=" * 60)
    decomp = run_fourway_decomp(DEV_SEEDS, W=8)
    save_results(decomp, OUT_DECOMP, os.path.basename(__file__))
    print("\n=== Four-way decomposition summary (pooled regret dB) ===")
    for fGk, v in decomp["per_fG_decomp"].items():
        print(f"{fGk}: " + " | ".join(f"{d}={v[d]['mean']:.4f}" for d in v))

    print(f"\nTOTAL elapsed: {round(time.time()-t0,1)}s")
    print(f"Saved -> {OUT_PHASEA}\n         {OUT_DECOMP}")


if __name__ == "__main__":
    main()
