"""Macro A runner: oracle complementarity among LEGAL FIR-aligned experts.

Frozen contract: batch-contract.v1.yaml (A/B/C/D criteria frozen before reading test).

Experts:
  - CMA_godard_z (anchor, mu=0.03 from B01-R fair fixed-mu)
  - MMA_ywd (legal fallback 1, per-cost mu tuned on validation)
  - DD_LMS_cold_start (legal fallback 2, per-cost mu tuned; expected to diverge cold)
  - oracle_unmix (Kill bound ONLY, TX-truth LS)

Seeds: validation [101-105] for mu-tuning; test [121-130] for confirmatory (FRESH,
disjoint from all prior batches — NOT 71-80).

Output: artifacts/result.v1.json + per-realization pairing for downstream routing.
"""
from __future__ import annotations
import json
import sys
import time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve()
SRC_DIR = HERE.parent
BATCH_DIR = SRC_DIR.parent
CB1_ROOT = BATCH_DIR.parent
ATLAS_DIR = CB1_ROOT / "baseline-atlas"
MMA_DIR = CB1_ROOT / "baseline-adjudication-batch"
REPO_ROOT = HERE.parents[7]
SIM_DIR = REPO_ROOT / "projects" / "simulation"
for p in (str(SIM_DIR), str(ATLAS_DIR), str(MMA_DIR), str(SRC_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402
import cb1_evaluator as evaluator  # noqa: E402
import cb1_cell_runner as atlas_runner  # noqa: E402
import mma_comparator as mma_mod  # noqa: E402
import dd_lms_equalizer as ddlms_mod  # noqa: E402

FROZEN = {"alpha": 4.2, "beta": 1.4, "block": 100, "t_s": 4e-10,
          "method": "gar", "cma_mu_fixed": 0.03, "cma_taps": 11,
          "cma_block_size": 64, "r2_qam16": 1.32,
          "mma_R_R2": 0.82, "mma_R_I2": 0.82}
MDE = 0.005
R2_16QAM = 1.32
RANDOM_CEILING = 0.9375  # 16QAM random PI-SER

VAL_SEEDS = [101, 102, 103, 104, 105]
TEST_SEEDS = [121, 122, 123, 124, 125, 126, 127, 128, 129, 130]
MU_GRID = [1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1]

ATLAS_CELLS = [
    {"id": "16qam-snr05-nominal-short", "snr_db": 5.0,  "f_g_hz": 30.0,  "sop_rate": 4e-6, "n_symbols": 512},
    {"id": "16qam-snr10-nominal-short", "snr_db": 10.0, "f_g_hz": 30.0,  "sop_rate": 4e-6, "n_symbols": 512},
    {"id": "16qam-snr15-nominal-short", "snr_db": 15.0, "f_g_hz": 30.0,  "sop_rate": 4e-6, "n_symbols": 512},
    {"id": "16qam-snr20-nominal-short", "snr_db": 20.0, "f_g_hz": 30.0,  "sop_rate": 4e-6, "n_symbols": 512},
    {"id": "16qam-snr25-nominal-short", "snr_db": 25.0, "f_g_hz": 30.0,  "sop_rate": 4e-6, "n_symbols": 512},
    {"id": "16qam-snr20-fg100-short",   "snr_db": 20.0, "f_g_hz": 100.0, "sop_rate": 4e-6, "n_symbols": 512},
    {"id": "16qam-snr20-fg1000-short",  "snr_db": 20.0, "f_g_hz": 1000.0,"sop_rate": 4e-6, "n_symbols": 512},
    {"id": "16qam-snr20-sop40e-short",  "snr_db": 20.0, "f_g_hz": 30.0,  "sop_rate": 4e-5, "n_symbols": 512},
    {"id": "16qam-snr10-fg100-long",    "snr_db": 10.0, "f_g_hz": 100.0, "sop_rate": 4e-6, "n_symbols": 8192},
    {"id": "16qam-snr15-fg1000-long",   "snr_db": 15.0, "f_g_hz": 1000.0,"sop_rate": 4e-6, "n_symbols": 8192},
    {"id": "16qam-snr20-nominal-long",  "snr_db": 20.0, "f_g_hz": 30.0,  "sop_rate": 4e-6, "n_symbols": 8192},
]


def make_realization(cell, seed):
    gamma_bar = float(10.0 ** (float(cell["snr_db"]) / 10.0))
    return generate_shared_realization_dp(
        int(cell["n_symbols"]), float(FROZEN["alpha"]), float(FROZEN["beta"]),
        float(cell["f_g_hz"]), sop_rate=float(cell["sop_rate"]), seed=int(seed),
        gamma_bar=gamma_bar, block=int(FROZEN["block"]), t_s=float(FROZEN["t_s"]),
        method=str(FROZEN["method"]), modulation="qam16")


def eval_window(cell):
    return atlas_runner.eval_window_for(
        int(cell["n_symbols"]), int(FROZEN["cma_taps"]),
        window_symbols=256, block_size=int(FROZEN["cma_block_size"]))


def metrics(zX, zY, truth_eval, bx, by):
    m = evaluator.evaluate_dual_16qam(zX, zY, truth_eval[:, 0], truth_eval[:, 1], bx, by)
    return {"pi_ser": float(m["pi_ser"]), "fixed_label_ser": float(m["fixed_label_ser"])}


def oracle_unmix(rX, rY, sX, sY):
    R = np.vstack([rX, rY]); S = np.vstack([sX, sY])
    W, *_ = np.linalg.lstsq(R.T, S.T, rcond=1e-10)
    Z = W.T @ R
    return Z[0], Z[1]


def run_experts(cell, seed, mma_mu, dd_mu, log):
    """Run all experts on one (cell, seed) shared realization."""
    realization = make_realization(cell, seed)
    rX, rY, sX, sY = realization["rX"], realization["rY"], realization["sX"], realization["sY"]
    es, ce, ee, _ = eval_window(cell)
    truth_eval = np.column_stack((sX[ce:ee], sY[ce:ee]))
    bx = realization["bitsX"][ce * 4:ee * 4]
    by = realization["bitsY"][ce * 4:ee * 4]

    out = {}

    # CMA anchor (fixed mu=0.03, the B01-R fair fixed-mu)
    cma = atlas_runner.standard_cma_godard_with_z(
        rX, rY, n_tap=int(FROZEN["cma_taps"]), mu=float(FROZEN["cma_mu_fixed"]),
        R2=R2_16QAM, block_size=int(FROZEN["cma_block_size"]))
    if cma["diverged"]:
        out["cma"] = {"pi_ser": RANDOM_CEILING, "diverged": True}
    else:
        m = metrics(cma["zX"][ce:ee], cma["zY"][ce:ee], truth_eval, bx, by)
        out["cma"] = {**m, "diverged": False}

    # MMA (legal fallback 1, tuned mu)
    mm = mma_mod.mma_yang_werner_dumont(
        rX, rY, n_tap=int(FROZEN["cma_taps"]), mu=mma_mu,
        R_R2=float(FROZEN["mma_R_R2"]), R_I2=float(FROZEN["mma_R_I2"]),
        block_size=int(FROZEN["cma_block_size"]))
    if mm["diverged"]:
        out["mma"] = {"pi_ser": RANDOM_CEILING, "diverged": True}
    else:
        m = metrics(mm["zX"][ce:ee], mm["zY"][ce:ee], truth_eval, bx, by)
        out["mma"] = {**m, "diverged": False}

    # DD-LMS cold start (legal fallback 2, tuned mu)
    dd = ddlms_mod.dd_lms_cold_start(
        rX, rY, n_tap=int(FROZEN["cma_taps"]), mu=dd_mu,
        block_size=int(FROZEN["cma_block_size"]))
    if dd["diverged"]:
        out["ddlms"] = {"pi_ser": RANDOM_CEILING, "diverged": True}
    else:
        m = metrics(dd["zX"][ce:ee], dd["zY"][ce:ee], truth_eval, bx, by)
        out["ddlms"] = {**m, "diverged": False}

    # Oracle unmix (Kill bound)
    zX_o_f, zY_o_f = oracle_unmix(rX[es:ee], rY[es:ee], sX[es:ee], sY[es:ee])
    off, oef = ce - es, ee - es
    m = metrics(zX_o_f[off:oef], zY_o_f[off:oef], truth_eval, bx, by)
    out["oracle"] = m

    return out


def tune_mu(cell_subset, seeds, log):
    """Per-expert mu tuning on validation seeds. Returns best mu per expert (min macro PI-SER)."""
    best = {}
    for expert in ("mma", "ddlms"):
        best_mu, best_score = None, float("inf")
        for mu in MU_GRID:
            scores = []
            for cell in cell_subset:
                r = run_experts(cell, seeds[0], mma_mu=mu if expert == "mma" else 1e-3,
                                dd_mu=mu if expert == "ddlms" else 1e-3, log=log)
                scores.append(r[expert]["pi_ser"])
            mean = float(np.mean(scores))
            log(f"    tune {expert} mu={mu}: macro_pi_ser={mean:.4f}")
            if mean < best_score:
                best_score, best_mu = mean, mu
        best[expert] = {"mu": best_mu, "val_macro_pi_ser": best_score}
        log(f"  {expert} best mu={best_mu} (val macro {best_score:.4f})")
    return best


def main():
    out_path = BATCH_DIR / "artifacts" / "result.v1.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    log = lambda msg: print(msg, flush=True)

    log("[MacroA] Identity tests")
    import test_hybrid_identity as tid
    tid._run_all()

    # Phase 1: per-expert mu tuning on validation seeds (subset of cells for speed)
    log("[MacroA] Phase 1: per-expert mu tuning on VAL seeds [101-105]")
    val_cells = [c for c in ATLAS_CELLS if c["id"] in
                 ("16qam-snr20-nominal-short", "16qam-snr15-fg1000-long",
                  "16qam-snr05-nominal-short", "16qam-snr20-fg1000-short")]
    tuned = tune_mu(val_cells, VAL_SEEDS, log)

    mma_mu = tuned["mma"]["mu"]
    dd_mu = tuned["ddlms"]["mu"]

    # Phase 2: confirmatory run on FRESH test seeds [121-130]
    log(f"[MacroA] Phase 2: confirmatory on TEST seeds {TEST_SEEDS} (mma_mu={mma_mu}, dd_mu={dd_mu})")
    cells_results = []
    for cell in ATLAS_CELLS:
        per_seed = []
        for seed in TEST_SEEDS:
            r = run_experts(cell, seed, mma_mu=mma_mu, dd_mu=dd_mu, log=log)
            r["seed"] = seed
            per_seed.append(r)
        cells_results.append({"cell_id": cell["id"], "per_seed": per_seed})
        means = {k: float(np.mean([s[k]["pi_ser"] for s in per_seed]))
                 for k in ("cma", "mma", "ddlms", "oracle")}
        log(f"  {cell['id']}: cma={means['cma']:.4f} mma={means['mma']:.4f} "
            f"ddlms={means['ddlms']:.4f} oracle={means['oracle']:.4f}")

    # Aggregate + complementarity analysis
    rows = []
    for c in cells_results:
        for ps in c["per_seed"]:
            rows.append({"cell": c["cell_id"], "seed": ps["seed"],
                         "cma": ps["cma"]["pi_ser"], "mma": ps["mma"]["pi_ser"],
                         "ddlms": ps["ddlms"]["pi_ser"], "oracle": ps["oracle"]["pi_ser"]})

    macro = {k: float(np.mean([r[k] for r in rows])) for k in ("cma", "mma", "ddlms", "oracle")}

    # Per-realization oracle selectors (Kill/headroom bounds)
    oracle_sel_cma_mma = [min(r["cma"], r["mma"]) for r in rows]
    oracle_sel_cma_ddlms = [min(r["cma"], r["ddlms"]) for r in rows]
    oracle_sel_all3 = [min(r["cma"], r["mma"], r["ddlms"]) for r in rows]
    macro_sel_cma_mma = float(np.mean(oracle_sel_cma_mma))
    macro_sel_cma_ddlms = float(np.mean(oracle_sel_cma_ddlms))
    macro_sel_all3 = float(np.mean(oracle_sel_all3))

    # Complementarity fractions (threshold = MDE)
    thr = MDE
    def comp(a, b):
        better = sum(1 for r in rows if r[b] < r[a] - thr)
        worse = sum(1 for r in rows if r[b] > r[a] + thr)
        tie = len(rows) - better - worse
        return {"better": better, "worse": worse, "tie": tie,
                "frac_better": better / len(rows), "frac_worse": worse / len(rows)}

    # Collapse-subset complementarity (CMA > 0.3)
    collapse_rows = [r for r in rows if r["cma"] > 0.3]

    aggregate = {
        "macro_pi_ser": macro,
        "oracle_selector_macro": {
            "cma_vs_mma": macro_sel_cma_mma,
            "cma_vs_ddlms": macro_sel_cma_ddlms,
            "all3": macro_sel_all3,
        },
        "oracle_headroom_over_cma": {
            "cma_vs_mma": macro["cma"] - macro_sel_cma_mma,
            "cma_vs_ddlms": macro["cma"] - macro_sel_cma_ddlms,
            "all3": macro["cma"] - macro_sel_all3,
        },
        "complementarity_vs_cma": {
            "mma": comp("cma", "mma"),
            "ddlms": comp("cma", "ddlms"),
        },
        "collapse_subset_cma_gt_0p3": {
            "n": len(collapse_rows),
            "mma_better": sum(1 for r in collapse_rows if r["mma"] < r["cma"] - thr),
            "ddlms_better": sum(1 for r in collapse_rows if r["ddlms"] < r["cma"] - thr),
        },
        "practical_threshold_headroom_min": 0.03,
        "headroom_meets_threshold": {
            "cma_vs_mma": (macro["cma"] - macro_sel_cma_mma) >= 0.03,
            "cma_vs_ddlms": (macro["cma"] - macro_sel_cma_ddlms) >= 0.03,
            "all3": (macro["cma"] - macro_sel_all3) >= 0.03,
        },
    }

    log("[MacroA] === AGGREGATE ===")
    log(f"  macro PI-SER: cma={macro['cma']:.4f} mma={macro['mma']:.4f} "
        f"ddlms={macro['ddlms']:.4f} oracle={macro['oracle']:.4f}")
    log(f"  oracle selector macro: cma_vs_mma={macro_sel_cma_mma:.4f} "
        f"cma_vs_ddlms={macro_sel_cma_ddlms:.4f} all3={macro_sel_all3:.4f}")
    log(f"  headroom over cma: cma_vs_mma={macro['cma']-macro_sel_cma_mma:.4f} "
        f"cma_vs_ddlms={macro['cma']-macro_sel_cma_ddlms:.4f} all3={macro['cma']-macro_sel_all3:.4f}")
    log(f"  complementarity mma: {comp('cma','mma')}")
    log(f"  complementarity ddlms: {comp('cma','ddlms')}")

    results = {
        "cells": cells_results,
        "aggregate": aggregate,
        "tuning": tuned,
        "metadata": {
            "schema": "direction-lab.cb1.hybrid-routing.v1",
            "MDE": MDE,
            "val_seeds": VAL_SEEDS,
            "test_seeds": TEST_SEEDS,
            "frozen": FROZEN,
            "elapsed_seconds": time.time() - t0,
        },
    }
    out_path.write_text(json.dumps(results, indent=1), encoding="utf-8")
    log(f"[MacroA] wrote {out_path} ({time.time()-t0:.1f}s)")


if __name__ == "__main__":
    main()
