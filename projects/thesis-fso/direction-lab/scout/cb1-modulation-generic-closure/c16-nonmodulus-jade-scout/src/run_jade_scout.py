"""Runner for the C16 non-modulus HOS paradigm Scout.

Compares Godard CMA (anchor, modulus-based) vs HOS kurtosis-max equalizer
(non-modulus) vs oracle unmix (Kill bound) on the 16QAM inner-ring collapse.

The decisive question: does the non-modulus paradigm escape the collapse?
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
REPO_ROOT = HERE.parents[7]
SIM_DIR = REPO_ROOT / "projects" / "simulation"
for p in (str(SIM_DIR), str(ATLAS_DIR), str(SRC_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402
import cb1_evaluator as evaluator  # noqa: E402
import cb1_cell_runner as atlas_runner  # noqa: E402
import hos_equalizer as hos  # noqa: E402

FROZEN = {"alpha": 4.2, "beta": 1.4, "block": 100, "t_s": 4e-10,
          "method": "gar", "cma_mu_fixed": 0.03, "cma_taps": 11,
          "cma_block_size": 64, "r2_qam16": 1.32}
MDE = 0.005
R2_16QAM = 1.32

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
TEST_SEEDS = list(range(71, 81))


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
    """Oracle 2x2 unmixing via LS fit to TX truth (Kill bound)."""
    R = np.vstack([rX, rY])  # [2, N]
    S = np.vstack([sX, sY])  # [2, N]
    W, _, _, _ = np.linalg.lstsq(R.T, S.T, rcond=1e-10)  # solve S^T = R^T W
    Z = W.T @ R  # [2, N]
    return Z[0], Z[1]


def run_cell_seed(cell, seed, log=print):
    """Run all 3 methods on one (cell, seed)."""
    realization = make_realization(cell, seed)
    rX = realization["rX"]
    rY = realization["rY"]
    sX = realization["sX"]
    sY = realization["sY"]
    es, ce, ee, _ = eval_window(cell)

    # Godard CMA (anchor)
    cma = atlas_runner.standard_cma_godard_with_z(
        rX, rY, n_tap=int(FROZEN["cma_taps"]), mu=float(FROZEN["cma_mu_fixed"]),
        R2=R2_16QAM, block_size=int(FROZEN["cma_block_size"]))
    truth_eval = np.column_stack((sX[ce:ee], sY[ce:ee]))
    bx = realization["bitsX"][ce * 4:ee * 4]
    by = realization["bitsY"][ce * 4:ee * 4]

    if cma["diverged"]:
        m_cma = {"pi_ser": 0.9375, "fixed_label_ser": 0.9375}
    else:
        m_cma = metrics(cma["zX"][ce:ee], cma["zY"][ce:ee], truth_eval, bx, by)

    # HOS non-modulus (candidate) — run on eval window [es:ee], but evaluate on [ce:ee]
    # to match truth_eval (CMA is evaluated on the converged [ce:ee] sub-window).
    zX_hos_full, zY_hos_full, hos_info = hos.hos_equalize_dp(rX[es:ee], rY[es:ee])
    # Extract the [ce:ee] sub-window from HOS output (offset by -es)
    offset = ce - es
    end_offset = ee - es
    zX_hos = zX_hos_full[offset:end_offset]
    zY_hos = zY_hos_full[offset:end_offset]
    m_hos = metrics(zX_hos, zY_hos, truth_eval, bx, by)

    # Oracle unmix (Kill bound) — fit on [es:ee], evaluate on [ce:ee]
    zX_oracle_full, zY_oracle_full = oracle_unmix(rX[es:ee], rY[es:ee], sX[es:ee], sY[es:ee])
    offset = ce - es
    end_offset = ee - es
    zX_oracle = zX_oracle_full[offset:end_offset]
    zY_oracle = zY_oracle_full[offset:end_offset]
    m_oracle = metrics(zX_oracle, zY_oracle, truth_eval, bx, by)

    return {
        "pi_ser_cma": m_cma["pi_ser"],
        "pi_ser_hos": m_hos["pi_ser"],
        "pi_ser_oracle": m_oracle["pi_ser"],
        "hos_objective": hos_info["best_objective"],
    }


def main():
    out_path = BATCH_DIR / "artifacts" / "result.v1.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    log = lambda msg: print(msg, flush=True)

    log("[C16] Semantic smoke: clean cell (snr25) + collapsed cell (snr05)")
    for smoke_cell_id, expected in [("16qam-snr25-nominal-short", "clean"),
                                     ("16qam-snr05-nominal-short", "collapsed")]:
        cell = next(c for c in ATLAS_CELLS if c["id"] == smoke_cell_id)
        r = run_cell_seed(cell, 71, log=log)
        log(f"  {smoke_cell_id}: cma_pi_ser={r['pi_ser_cma']:.4f}, "
            f"hos_pi_ser={r['pi_ser_hos']:.4f}, oracle_pi_ser={r['pi_ser_oracle']:.4f}")

    log("[C16] Full eval: 11 cells x 10 seeds")
    cells_results = []
    for cell in ATLAS_CELLS:
        per_seed = []
        for seed in TEST_SEEDS:
            r = run_cell_seed(cell, seed, log=log)
            r["seed"] = seed
            per_seed.append(r)
        cma_vals = [s["pi_ser_cma"] for s in per_seed if np.isfinite(s["pi_ser_cma"])]
        hos_vals = [s["pi_ser_hos"] for s in per_seed if np.isfinite(s["pi_ser_hos"])]
        ora_vals = [s["pi_ser_oracle"] for s in per_seed if np.isfinite(s["pi_ser_oracle"])]
        cells_results.append({
            "cell_id": cell["id"],
            "per_seed": per_seed,
            "cma_pi_ser_mean": float(np.mean(cma_vals)) if cma_vals else float("nan"),
            "hos_pi_ser_mean": float(np.mean(hos_vals)) if hos_vals else float("nan"),
            "oracle_pi_ser_mean": float(np.mean(ora_vals)) if ora_vals else float("nan"),
        })
        c = cells_results[-1]
        log(f"  {cell['id']}: cma={c['cma_pi_ser_mean']:.4f}, "
            f"hos={c['hos_pi_ser_mean']:.4f}, oracle={c['oracle_pi_ser_mean']:.4f}")

    # Aggregate
    cma_all = [s["pi_ser_cma"] for c in cells_results for s in c["per_seed"]]
    hos_all = [s["pi_ser_hos"] for c in cells_results for s in c["per_seed"]]
    cma_collapse = float(np.mean([1 if v > 0.3 else 0 for v in cma_all]))
    hos_collapse = float(np.mean([1 if v > 0.3 else 0 for v in hos_all]))
    macro_cma = float(np.mean([c["cma_pi_ser_mean"] for c in cells_results]))
    macro_hos = float(np.mean([c["hos_pi_ser_mean"] for c in cells_results]))

    log(f"[C16] macro PI-SER: cma={macro_cma:.4f}, hos={macro_hos:.4f}")
    log(f"[C16] collapse rate: cma={cma_collapse:.3f}, hos={hos_collapse:.3f}")

    results = {
        "cells": cells_results,
        "aggregate": {
            "macro_pi_ser_cma": macro_cma,
            "macro_pi_ser_hos": macro_hos,
            "collapse_rate_cma": cma_collapse,
            "collapse_rate_hos": hos_collapse,
        },
        "metadata": {
            "schema": "direction-lab.cb1.c16-nonmodulus-jade.v1",
            "MDE": MDE,
            "test_seeds": TEST_SEEDS,
            "elapsed_seconds": time.time() - t0,
        },
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)
    log(f"[C16] DONE in {time.time() - t0:.1f}s — {out_path}")


if __name__ == "__main__":
    main()
