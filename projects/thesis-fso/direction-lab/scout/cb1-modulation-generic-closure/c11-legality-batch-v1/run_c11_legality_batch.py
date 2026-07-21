"""C11 legality batch runner — single entry point.

    python run_c11_legality_batch.py --tune-and-eval

Implements batch-contract.v1.yaml:
  Phase 1: tune switch_point_block + dd_step_size on validation cells ×
           validation seeds [31-35] (NEW, disjoint from B01-R seeds).
  Phase 2: held-out evaluation on 7 cells × 10 test seeds [41-50] (NEW).
  Phase 3: hierarchical paired bootstrap CI on macro paired delta.
  Phase 4: adjudicate A/B/C.

Discipline:
  * No-leakage seed split (asserted in code).
  * fixed_mu_cma μ = 0.03 INHERITED from B01-R HF6 (NOT re-tuned — no double-dip).
  * C11_legal stage1_mu = 0.03 (= fixed_mu_cma μ; fair stage-1).
  * Switch point selected on validation, frozen BEFORE test.
  * dd_step_size grid includes 0 (identity gate).
  * Reports paired delta + per-cell CI + pass/access counts + divergence.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import yaml

HERE = Path(__file__).resolve()
BATCH_DIR = HERE.parent                       # .../c11-legality-batch-v1
CB1_ROOT = BATCH_DIR.parent                   # .../cb1-modulation-generic-closure
B01R_DIR = CB1_ROOT / "fairness-batch-b01r"
ATLAS_DIR = CB1_ROOT / "baseline-atlas"
REPO_ROOT = HERE.parents[6]                   # worktree root
SIM_DIR = REPO_ROOT / "projects" / "simulation"
for p in (str(SIM_DIR), str(ATLAS_DIR), str(B01R_DIR), str(BATCH_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402
import cb1_evaluator as evaluator  # noqa: E402
import cb1_cell_runner as atlas_runner  # noqa: E402
import c11_causal  # noqa: E402


# =============================================================================
# Contract constants (mirror batch-contract.v1.yaml)
# =============================================================================

FROZEN = {
    "alpha": 4.2, "beta": 1.4, "block": 100, "t_s": 4e-10, "method": "gar",
    "cma_mu_fixed": 0.03,  # INHERITED from B01-R HF6 interior optimum
    "cma_taps": 11, "cma_block_size": 64,
    "r2_qam16": 1.32, "affine_ridge": 1e-6,
}
MDE = 0.005  # practical significance threshold (PI-SER absolute)
R2_16QAM = 1.32

# 11 atlas cells (SAME as B01 / B01-R; raw preserved).
ATLAS_V1_16QAM_CELLS = [
    {"id": "16qam-snr05-nominal-short", "snr_db": 5.0,  "f_g_hz": 30.0,  "sop_rate": 4e-6, "n_symbols": 512, "modulation": "qam16"},
    {"id": "16qam-snr10-nominal-short", "snr_db": 10.0, "f_g_hz": 30.0,  "sop_rate": 4e-6, "n_symbols": 512, "modulation": "qam16"},
    {"id": "16qam-snr15-nominal-short", "snr_db": 15.0, "f_g_hz": 30.0,  "sop_rate": 4e-6, "n_symbols": 512, "modulation": "qam16"},
    {"id": "16qam-snr20-nominal-short", "snr_db": 20.0, "f_g_hz": 30.0,  "sop_rate": 4e-6, "n_symbols": 512, "modulation": "qam16"},
    {"id": "16qam-snr25-nominal-short", "snr_db": 25.0, "f_g_hz": 30.0,  "sop_rate": 4e-6, "n_symbols": 512, "modulation": "qam16"},
    {"id": "16qam-snr20-fg100-short",   "snr_db": 20.0, "f_g_hz": 100.0, "sop_rate": 4e-6, "n_symbols": 512, "modulation": "qam16"},
    {"id": "16qam-snr20-fg1000-short",  "snr_db": 20.0, "f_g_hz": 1000.0,"sop_rate": 4e-6, "n_symbols": 512, "modulation": "qam16"},
    {"id": "16qam-snr20-sop40e-short",  "snr_db": 20.0, "f_g_hz": 30.0,  "sop_rate": 4e-5, "n_symbols": 512, "modulation": "qam16"},
    {"id": "16qam-snr10-fg100-long",    "snr_db": 10.0, "f_g_hz": 100.0, "sop_rate": 4e-6, "n_symbols": 8192, "modulation": "qam16"},
    {"id": "16qam-snr15-fg1000-long",   "snr_db": 15.0, "f_g_hz": 1000.0,"sop_rate": 4e-6, "n_symbols": 8192, "modulation": "qam16"},
    {"id": "16qam-snr20-nominal-long",  "snr_db": 20.0, "f_g_hz": 30.0,  "sop_rate": 4e-6, "n_symbols": 8192, "modulation": "qam16"},
]

VALIDATION_CELL_IDS = {
    "16qam-snr20-nominal-short",
    "16qam-snr20-fg1000-short",
    "16qam-snr20-sop40e-short",
    "16qam-snr20-nominal-long",
}
HELD_OUT_CELL_IDS = {
    "16qam-snr05-nominal-short",
    "16qam-snr10-nominal-short",
    "16qam-snr15-nominal-short",
    "16qam-snr25-nominal-short",
    "16qam-snr20-fg100-short",
    "16qam-snr10-fg100-long",
    "16qam-snr15-fg1000-long",
}

# NEW disjoint seeds (no reuse of B01-R's 11-15 / 21-30).
VALIDATION_SEEDS = [31, 32, 33, 34, 35]
TEST_SEEDS = [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
_B01R_SEEDS = set(list(range(11, 16)) + list(range(21, 31)))
assert set(VALIDATION_SEEDS).isdisjoint(set(TEST_SEEDS)), "LEAKAGE: val/test overlap"
assert set(VALIDATION_SEEDS).isdisjoint(_B01R_SEEDS), "LEAKAGE: val overlaps B01-R"
assert set(TEST_SEEDS).isdisjoint(_B01R_SEEDS), "LEAKAGE: test overlaps B01-R"

# DD step grid (FROZEN — mirrors batch-contract.v1.yaml). MUST include 0.
DD_STEP_GRID = [0.0, 1e-6, 3e-6, 1e-5, 3e-5, 1e-4, 3e-4]

# Switch-point candidates: convergence-plateau block + small offsets.
# Plateau = block index after which cumulative |Δw_norm| over the last 4 blocks
# drops below 1% of init norm (per contract switch_point_policy).
SWITCH_OFFSETS = [0, 1, 2]  # blocks after plateau


# =============================================================================
# Realisation + PI-SER helpers
# =============================================================================

def make_realization(cell, seed):
    gamma_bar = float(10.0 ** (float(cell["snr_db"]) / 10.0))
    return generate_shared_realization_dp(
        int(cell["n_symbols"]), float(FROZEN["alpha"]), float(FROZEN["beta"]),
        float(cell["f_g_hz"]), sop_rate=float(cell["sop_rate"]), seed=int(seed),
        gamma_bar=gamma_bar, block=int(FROZEN["block"]), t_s=float(FROZEN["t_s"]),
        method=str(FROZEN["method"]), modulation=str(cell.get("modulation", "qam16")),
    )


def _eval_window_for_cell(cell):
    return atlas_runner.eval_window_for(
        int(cell["n_symbols"]), int(FROZEN["cma_taps"]),
        window_symbols=256, block_size=int(FROZEN["cma_block_size"]),
    )


def pi_ser_from_z(zX, zY, realization, *, eval_start, calibration_end, eval_end):
    zXa = np.asarray(zX)
    zYa = np.asarray(zY)
    z_calib = np.column_stack((zXa[eval_start:calibration_end], zYa[eval_start:calibration_end]))
    z_eval = np.column_stack((zXa[calibration_end:eval_end], zYa[calibration_end:eval_end]))
    truth_calib = np.column_stack((
        realization["sX"][eval_start:calibration_end],
        realization["sY"][eval_start:calibration_end],
    ))
    truth_eval = np.column_stack((
        realization["sX"][calibration_end:eval_end],
        realization["sY"][calibration_end:eval_end],
    ))
    bits_x_eval = realization["bitsX"][calibration_end * 4:eval_end * 4]
    bits_y_eval = realization["bitsY"][calibration_end * 4:eval_end * 4]
    nearest_pred = evaluator.hard_16qam(z_eval)
    # oracle_affine ONLY as Kill bound (FR-21); reported as headroom, never as Go.
    oracle_corr = evaluator.oracle_affine_bound_16qam(
        z_calib, z_eval, truth_calib, ridge=FROZEN["affine_ridge"])
    nearest_m = evaluator.evaluate_dual_16qam(
        nearest_pred[:, 0], nearest_pred[:, 1],
        truth_eval[:, 0], truth_eval[:, 1], bits_x_eval, bits_y_eval)
    oracle_m = evaluator.evaluate_dual_16qam(
        oracle_corr[:, 0], oracle_corr[:, 1],
        truth_eval[:, 0], truth_eval[:, 1], bits_x_eval, bits_y_eval)
    return {
        "nearest_pi_ser": float(nearest_m["pi_ser"]),
        "oracle_pi_ser": float(oracle_m["pi_ser"]),
        "nearest_fixed_ser": float(nearest_m["fixed_label_ser"]),
    }


# =============================================================================
# Method runners
# =============================================================================

def run_fixed_mu_cma(cell, realization):
    """System anchor + Go comparator. μ = 0.03 INHERITED from B01-R HF6.
    ONE causal pass."""
    return atlas_runner.standard_cma_godard_with_z(
        realization["rX"], realization["rY"],
        n_tap=int(FROZEN["cma_taps"]), mu=float(FROZEN["cma_mu_fixed"]),
        R2=R2_16QAM, block_size=int(FROZEN["cma_block_size"]),
    )


def run_c11_legal(cell, realization, *, dd_step_size, switch_point_block):
    """Legal causal one-pass CMA→DD-LMS. Stage-1 μ = 0.03 (= fixed_mu_cma μ;
    fair stage-1). UNIFIED bilinear convention. ONE causal pass."""
    return c11_causal.c11_cma_dd_lms_causal(
        realization["rX"], realization["rY"],
        n_tap=int(FROZEN["cma_taps"]), cma_mu=float(FROZEN["cma_mu_fixed"]),
        cma_R2=R2_16QAM, cma_block_size=int(FROZEN["cma_block_size"]),
        dd_step_size=float(dd_step_size),
        switch_point_block=int(switch_point_block),
        hard_decision_fn=evaluator.hard_16qam,
    )


# =============================================================================
# Switch-point estimation (validation only)
# =============================================================================

def estimate_plateau_block(realization, cell):
    """Block index after which cumulative |Δw_norm| over the last 4 blocks
    drops below 1% of init norm. Uses fixed-μ CMA trajectory."""
    out = run_fixed_mu_cma(cell, realization)
    if out.get("diverged", False) or not out.get("trace"):
        # Diverged or no trace: fall back to a conservative mid-stream plateau.
        n_valid = cell["n_symbols"] - int(FROZEN["cma_taps"]) + 1
        n_blocks = n_valid // int(FROZEN["cma_block_size"])
        return max(1, n_blocks // 2)
    init_norm = float(out["init_w_norm"])
    trace = out["trace"]
    wn = np.array([t["w_norm"] for t in trace], dtype=float)
    # |Δw_norm| rolling over last 4 blocks
    if len(wn) < 5:
        return max(1, len(wn) - 1)
    deltas = np.abs(np.diff(wn))
    # Rolling 4-block sum
    for i in range(3, len(deltas)):
        window_sum = float(np.sum(deltas[i - 3:i + 1]))
        if window_sum < 0.01 * init_norm:
            return i  # block index after which plateau holds
    # No plateau found: use mid-stream
    return max(1, len(wn) // 2)


# =============================================================================
# Tuning (validation cells × validation seeds ONLY)
# =============================================================================

def tune_c11_legal(validation_cells, log=print):
    """Tune switch_point_block (per cell) and dd_step_size (global).

    Switch_point_block: each cell uses its OWN plateau block + best offset
    from {0, +1, +2}, picked on validation.
    dd_step_size: single global value picked by minimising macro mean PI-SER
    across validation cells × validation seeds."""
    log("  [tune] estimating plateau block per validation cell...")
    plateau_per_cell: dict[str, int] = {}
    for cell in validation_cells:
        # Plateau estimated from a single representative realization (seed=31).
        realization = make_realization(cell, seed=VALIDATION_SEEDS[0])
        plateau_per_cell[cell["id"]] = int(estimate_plateau_block(realization, cell))
        log(f"    {cell['id']}: plateau_block={plateau_per_cell[cell['id']]}")

    log("  [tune] scanning dd_step_size × switch_offset on validation...")
    best_dd = None
    best_score = None
    best_offset = None
    for dd in DD_STEP_GRID:
        for offset in SWITCH_OFFSETS:
            pis: list[float] = []
            n_div = 0
            n_total = 0
            for cell in validation_cells:
                sw = plateau_per_cell[cell["id"]] + offset
                for seed in VALIDATION_SEEDS:
                    n_total += 1
                    realization = make_realization(cell, seed)
                    out = run_c11_legal(cell, realization,
                                        dd_step_size=dd, switch_point_block=sw)
                    if out.get("diverged", False):
                        pis.append(1.0)
                        n_div += 1
                        continue
                    es, ce, ee, _ = _eval_window_for_cell(cell)
                    m = pi_ser_from_z(out["zX"], out["zY"], realization,
                                      eval_start=es, calibration_end=ce, eval_end=ee)
                    pis.append(m["nearest_pi_ser"])
            mean_pi = float(np.mean(pis)) if pis else 1.0
            div_rate = n_div / max(n_total, 1)
            score = -(mean_pi + 0.1 * div_rate)
            if best_score is None or score > best_score:
                best_score = score
                best_dd = dd
                best_offset = offset
            log(f"    dd={dd:.1e} offset=+{offset}: mean_PI={mean_pi:.4f} "
                f"div_rate={div_rate:.2f} score={score:.4f}")
    log(f"  [tune] BEST dd_step_size={best_dd}, switch_offset=+{best_offset}, "
        f"score={best_score:.4f}")
    return {
        "best_dd_step_size": float(best_dd),
        "best_switch_offset": int(best_offset),
        "plateau_block_per_cell": plateau_per_cell,
    }


# =============================================================================
# Held-out evaluation (test seeds ONLY)
# =============================================================================

def evaluate_held_out(tune_result, log=print):
    results: dict[str, Any] = {"cells": []}
    best_dd = tune_result["best_dd_step_size"]
    best_offset = tune_result["best_switch_offset"]
    plateau_per_cell = tune_result["plateau_block_per_cell"]

    for cell in ATLAS_V1_16QAM_CELLS:
        t_start = time.time()
        is_val = cell["id"] in VALIDATION_CELL_IDS
        is_held = cell["id"] in HELD_OUT_CELL_IDS
        cell_record = {
            "cell_id": cell["id"],
            "is_validation_cell": is_val,
            "is_held_out_cell": is_held,
            "axes": {"snr_db": cell["snr_db"], "f_g_hz": cell["f_g_hz"],
                     "sop_rate": cell["sop_rate"], "n_symbols": cell["n_symbols"]},
            "plateau_block": int(plateate := plateau_per_cell.get(cell["id"], estimate_plateau_block_fallback(cell))),
            "switch_point_block": int(plateate + best_offset),
            "per_seed": [],
        }
        es, ce, ee, _ = _eval_window_for_cell(cell)
        cell_record["eval_window"] = {"eval_start": es, "calibration_end": ce, "eval_end": ee}

        for seed in TEST_SEEDS:
            realization = make_realization(cell, seed)
            seed_record = {"seed": int(seed), "methods": {}}

            # fixed-μ CMA (Go comparator)
            fmu_out = run_fixed_mu_cma(cell, realization)
            if fmu_out["diverged"]:
                seed_record["methods"]["fixed_mu_cma"] = {"diverged": True}
            else:
                m = pi_ser_from_z(fmu_out["zX"], fmu_out["zY"], realization,
                                  eval_start=es, calibration_end=ce, eval_end=ee)
                seed_record["methods"]["fixed_mu_cma"] = {"diverged": False, **m}

            # C11_legal
            sw = cell_record["switch_point_block"]
            # Reset access counts BEFORE the call so the post-call read reflects
            # exactly this single invocation.
            c11_causal.reset_access_counts()
            c11_out = run_c11_legal(cell, realization,
                                    dd_step_size=best_dd, switch_point_block=sw)
            visits = c11_causal.get_access_counts().get("stage2_center_visits", np.array([]))
            max_visits = int(np.max(visits)) if len(visits) else 0
            if c11_out["diverged"]:
                seed_record["methods"]["C11_legal"] = {
                    "diverged": True, "stage2_max_visits_per_sample": max_visits,
                }
            else:
                m = pi_ser_from_z(c11_out["zX"], c11_out["zY"], realization,
                                  eval_start=es, calibration_end=ce, eval_end=ee)
                seed_record["methods"]["C11_legal"] = {
                    "diverged": False, "stage2_max_visits_per_sample": max_visits,
                    **m,
                }

            cell_record["per_seed"].append(seed_record)

        cell_record["aggregate"] = _aggregate_cell(cell_record["per_seed"])
        elapsed = time.time() - t_start
        agg = cell_record["aggregate"]
        log(f"  cell {cell['id']}: {elapsed:.1f}s — "
            f"fixed_mu={agg['fixed_mu_cma']['nearest_pi_ser_mean']:.4f}, "
            f"C11_legal={agg['C11_legal']['nearest_pi_ser_mean']:.4f}, "
            f"Δ={agg['C11_legal']['nearest_pi_ser_mean'] - agg['fixed_mu_cma']['nearest_pi_ser_mean']:+.4f}")
        results["cells"].append(cell_record)
    return results


def estimate_plateau_block_fallback(cell):
    """Fallback when plateau wasn't pre-computed (held-out cells)."""
    realization = make_realization(cell, seed=VALIDATION_SEEDS[0])
    return int(estimate_plateau_block(realization, cell))


def _aggregate_cell(per_seed):
    agg: dict[str, Any] = {}
    for method in ("fixed_mu_cma", "C11_legal"):
        vals_near = []
        vals_orac = []
        vals_fixed = []
        n_div = 0
        max_visits = 0
        for s in per_seed:
            m = s["methods"].get(method)
            if m is None:
                continue
            if m.get("diverged", False):
                n_div += 1
                continue
            if not np.isnan(m.get("nearest_pi_ser", float("nan"))):
                vals_near.append(m["nearest_pi_ser"])
            if not np.isnan(m.get("oracle_pi_ser", float("nan"))):
                vals_orac.append(m["oracle_pi_ser"])
            if not np.isnan(m.get("nearest_fixed_ser", float("nan"))):
                vals_fixed.append(m["nearest_fixed_ser"])
            mv = m.get("stage2_max_visits_per_sample", 0)
            if mv > max_visits:
                max_visits = mv
        agg[method] = {
            "nearest_pi_ser_mean": float(np.mean(vals_near)) if vals_near else float("nan"),
            "oracle_pi_ser_mean": float(np.mean(vals_orac)) if vals_orac else float("nan"),
            "nearest_fixed_ser_mean": float(np.mean(vals_fixed)) if vals_fixed else float("nan"),
            "headroom_mean": float(np.mean([max(n - o, 0.0) for n, o in zip(vals_near, vals_orac)])) if vals_near and vals_orac else float("nan"),
            "n_non_diverged_seeds": int(len(vals_near)),
            "n_diverged_seeds": int(n_div),
            "stage2_max_visits_per_sample_max_over_seeds": int(max_visits),
        }
    return agg


# =============================================================================
# Hierarchical paired bootstrap CI
# =============================================================================

def paired_delta_per_seed(cell_record, method_a, method_b):
    deltas = []
    for s in cell_record["per_seed"]:
        ma = s["methods"].get(method_a, {})
        mb = s["methods"].get(method_b, {})
        if ma.get("diverged") or mb.get("diverged"):
            continue
        pa = ma.get("nearest_pi_ser"); pb = mb.get("nearest_pi_ser")
        if pa is None or pb is None or np.isnan(pa) or np.isnan(pb):
            continue
        deltas.append(float(pa - pb))  # negative = a better
    return deltas


def paired_bootstrap_ci(deltas: list[float], *, n_boot: int = 10000, alpha: float = 0.05) -> dict[str, float]:
    if not deltas:
        return {"mean": float("nan"), "lower": float("nan"), "upper": float("nan"), "n": 0}
    arr = np.asarray(deltas, dtype=float)
    n = len(arr)
    rng = np.random.default_rng(20260721)
    boot_means = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, n, size=n)
        boot_means[b] = float(np.mean(arr[idx]))
    return {
        "mean": float(arr.mean()),
        "lower": float(np.percentile(boot_means, 100 * (alpha / 2))),
        "upper": float(np.percentile(boot_means, 100 * (1 - alpha / 2))),
        "n": int(n),
    }


def hierarchical_paired_bootstrap(results, *, n_boot: int = 10000) -> dict[str, Any]:
    """Two-level paired bootstrap: resample cells (with replacement), then
    within each resampled cell resample seeds (with replacement). Macro mean
    of per-cell paired deltas. Mirrors the contract's primary_statistic."""
    held = [c for c in results["cells"] if c["is_held_out_cell"]]
    per_cell_deltas = []
    for c in held:
        d = paired_delta_per_seed(c, "C11_legal", "fixed_mu_cma")
        per_cell_deltas.append(d)
    # Per-cell paired delta mean (C11_legal - fixed_mu_cma; negative = C11 better)
    cell_means = np.array([float(np.mean(d)) if d else float("nan") for d in per_cell_deltas])
    valid_cells = [d for d in per_cell_deltas if len(d) > 0]
    if not valid_cells:
        return {"macro_mean": float("nan"), "lower": float("nan"), "upper": float("nan"),
                "n_cells": 0, "per_cell_means": cell_means.tolist()}
    rng = np.random.default_rng(20260721)
    n_cells = len(valid_cells)
    boot_macros = np.empty(n_boot)
    for b in range(n_boot):
        cell_idx = rng.integers(0, n_cells, size=n_cells)
        macro = []
        for ci in cell_idx:
            d = valid_cells[ci]
            seed_idx = rng.integers(0, len(d), size=len(d))
            macro.append(float(np.mean(np.asarray(d)[seed_idx])))
        boot_macros[b] = float(np.mean(macro))
    macro_mean = float(np.mean(cell_means[~np.isnan(cell_means)]))
    return {
        "macro_mean": macro_mean,
        "lower": float(np.percentile(boot_macros, 2.5)),
        "upper": float(np.percentile(boot_macros, 97.5)),
        "n_cells": int(n_cells),
        "per_cell_means": cell_means.tolist(),
        "n_boot": int(n_boot),
    }


# =============================================================================
# Adjudication (A/B/C, frozen BEFORE running)
# =============================================================================

def adjudicate(results, hier_ci, tune_result):
    held = [c for c in results["cells"] if c["is_held_out_cell"]]
    macro_mean = hier_ci["macro_mean"]
    ci_upper = hier_ci["upper"]
    best_dd = tune_result["best_dd_step_size"]

    # Per-cell paired CI (secondary / exploratory).
    per_cell_ci = {}
    for c in held:
        per_cell_ci[c["cell_id"]] = paired_bootstrap_ci(
            paired_delta_per_seed(c, "C11_legal", "fixed_mu_cma"))

    # Divergence rates
    div_C11 = np.mean([c["aggregate"]["C11_legal"]["n_diverged_seeds"] for c in held]) / 10.0
    div_fmu = np.mean([c["aggregate"]["fixed_mu_cma"]["n_diverged_seeds"] for c in held]) / 10.0

    # Worst-cell paired delta
    worst_cell_delta = float(np.nanmax(hier_ci["per_cell_means"])) if hier_ci["per_cell_means"] else float("nan")

    # Access budget: max stage2 visits per sample across all cells/seeds (must be 1)
    max_visits = max(
        (s["methods"]["C11_legal"].get("stage2_max_visits_per_sample", 0)
         for c in held for s in c["per_seed"] if "C11_legal" in s["methods"]),
        default=0,
    )

    # Verdict
    if macro_mean < 0 and best_dd != 0.0:
        signal_survives = (ci_upper < 0 and macro_mean <= -MDE
                           and worst_cell_delta <= 0.0
                           and div_C11 <= div_fmu + 0.05)
        verdict = "A_C11_CAUSAL_SIGNAL_SURVIVES" if signal_survives else "B_C11_SIGNAL_DISAPPEARS_AFTER_LEGALIZATION"
    else:
        verdict = "B_C11_SIGNAL_DISAPPEARS_AFTER_LEGALIZATION"

    return {
        "verdict": verdict,
        "macro_paired_delta_mean": macro_mean,
        "macro_paired_delta_ci_upper_95": ci_upper,
        "macro_paired_delta_ci_lower_95": hier_ci["lower"],
        "practical_significance_threshold": -MDE,
        "best_dd_step_size": best_dd,
        "best_switch_offset": tune_result["best_switch_offset"],
        "per_cell_paired_delta_means": hier_ci["per_cell_means"],
        "per_cell_paired_ci_95": per_cell_ci,
        "worst_cell_paired_delta": worst_cell_delta,
        "divergence_rate_C11_legal": float(div_C11),
        "divergence_rate_fixed_mu_cma": float(div_fmu),
        "stage2_max_visits_per_sample_global": int(max_visits),
        "n_held_out_cells": len(held),
    }


# =============================================================================
# Source-closure provenance (audit issue #5 fix)
# =============================================================================

def _sha256_of_file(path: Path) -> str:
    """SHA-256 of a file's bytes (read in binary so encoding is irrelevant)."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# Frozen at import time: the set of source files whose bytes produced this
# artifact. The closure spans: contract, runner, new C11 module, tests,
# evaluator, cell runner, CMA anchor dependency, channel generator. Adding a
# path here is fine; modifying the set after a run invalidates the hash.
_SOURCE_CLOSURE_PATHS = [
    BATCH_DIR / "batch-contract.v1.yaml",
    BATCH_DIR / "run_c11_legality_batch.py",
    BATCH_DIR / "c11_causal.py",
    BATCH_DIR / "tests" / "test_c11_legality.py",
    BATCH_DIR / "R001-c11-legality-root-cause.md",
    ATLAS_DIR / "cb1_evaluator.py",
    ATLAS_DIR / "cb1_cell_runner.py",
    REPO_ROOT / "projects" / "simulation" / "common" / "_dual_pol_channel.py",
    REPO_ROOT / "projects" / "simulation" / "common" / "_modulation.py",
]


def _source_closure_hashes() -> dict[str, str]:
    """Return {relative_path: sha256} for every file in the source closure."""
    out: dict[str, str] = {}
    base = REPO_ROOT
    for p in _SOURCE_CLOSURE_PATHS:
        if not p.exists():
            out[str(p.relative_to(base))] = "MISSING"
            continue
        try:
            rel = str(p.relative_to(base))
        except ValueError:
            rel = str(p)
        out[rel] = _sha256_of_file(p)
    return out


# =============================================================================
# Main
# =============================================================================

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tune-and-eval", action="store_true")
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()

    out_path = BATCH_DIR / "artifacts" / "result.v1.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    global ATLAS_V1_16QAM_CELLS, TEST_SEEDS, VALIDATION_SEEDS
    if args.smoke:
        ATLAS_V1_16QAM_CELLS = [c for c in ATLAS_V1_16QAM_CELLS if c["id"] in
                                {"16qam-snr20-nominal-short", "16qam-snr25-nominal-short",
                                 "16qam-snr20-nominal-long", "16qam-snr10-fg100-long"}]
        TEST_SEEDS = [41, 42]
        VALIDATION_SEEDS = [31]

    log = lambda msg: print(msg, flush=True)

    log("[C11-LEGAL] Phase 0: identity-gate tests (must PASS before any evaluation)")
    # Run the gate tests in-process by importing pytest.
    import pytest
    exit_code = pytest.main([
        "-x", "--tb=short", "-q",
        str(BATCH_DIR / "tests" / "test_c11_legality.py"),
        "-k", "not OldImplementation and not SourceContractRunner",
    ])
    if exit_code != 0:
        log(f"[C11-LEGAL] FATAL: identity gates FAILED (pytest exit {exit_code}). "
            "Aborting per contract: identity_gate_tests_REQUIRED_PASS_before_any_evaluation.")
        sys.exit(2)
    log("[C11-LEGAL] identity gates PASS.")

    log("[C11-LEGAL] Phase 1: tuning on validation cells × validation seeds (NEW disjoint)")
    validation_cells = [c for c in ATLAS_V1_16QAM_CELLS if c["id"] in VALIDATION_CELL_IDS]
    log(f"  validation cells ({len(validation_cells)}): {[c['id'] for c in validation_cells]}")
    log(f"  validation_seeds={VALIDATION_SEEDS}  test_seeds={TEST_SEEDS}  (disjoint asserted)")
    tune_result = tune_c11_legal(validation_cells, log=log)

    # Persist frozen params (per-cell switch + global dd).
    frozen_out = {
        "fixed_mu_cma_mu": float(FROZEN["cma_mu_fixed"]),
        "c11_legal_stage1_mu": float(FROZEN["cma_mu_fixed"]),
        "c11_legal_best_dd_step_size": float(tune_result["best_dd_step_size"]),
        "c11_legal_best_switch_offset": int(tune_result["best_switch_offset"]),
        "plateau_block_per_cell": tune_result["plateau_block_per_cell"],
        "dd_step_grid": DD_STEP_GRID,
        "switch_offsets": SWITCH_OFFSETS,
        "validation_seeds": VALIDATION_SEEDS,
        "test_seeds": TEST_SEEDS,
        "mde": MDE,
    }
    params_path = BATCH_DIR / "artifacts" / "frozen-params.v1.yaml"
    with open(params_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(frozen_out, f, sort_keys=False, allow_unicode=True)
    log(f"[C11-LEGAL] frozen params: {params_path}")

    log("[C11-LEGAL] Phase 2: held-out evaluation on 11 cells × 10 fresh test seeds")
    results = evaluate_held_out(tune_result, log=log)

    log("[C11-LEGAL] Phase 3: hierarchical paired bootstrap CI on 7 held-out cells × 10 test seeds")
    hier_ci = hierarchical_paired_bootstrap(results, n_boot=10000)
    results["hierarchical_paired_ci"] = hier_ci
    log(f"  macro paired Δ (C11_legal - fixed_mu) = {hier_ci['macro_mean']:+.5f}  "
        f"95% CI=[{hier_ci['lower']:+.5f}, {hier_ci['upper']:+.5f}]")

    log("[C11-LEGAL] Phase 4: adjudication (A/B/C, frozen BEFORE running)")
    adjudication = adjudicate(results, hier_ci, tune_result)
    results["adjudication"] = adjudication
    log(f"[C11-LEGAL] VERDICT: {adjudication['verdict']}")
    log(f"  macro Δ mean = {adjudication['macro_paired_delta_mean']:+.5f}")
    log(f"  macro CI upper 95% = {adjudication['macro_paired_delta_ci_upper_95']:+.5f}  "
        f"(need < 0 for Verdict A)")
    log(f"  best dd_step_size = {adjudication['best_dd_step_size']:.1e}")
    log(f"  worst-cell Δ = {adjudication['worst_cell_paired_delta']:+.5f}")
    log(f"  divergence rate C11_legal = {adjudication['divergence_rate_C11_legal']:.2f}, "
        f"fixed_mu = {adjudication['divergence_rate_fixed_mu_cma']:.2f}")
    log(f"  stage2 max visits per sample (global) = {adjudication['stage2_max_visits_per_sample_global']}")

    results["frozen_params"] = frozen_out
    results["metadata"] = {
        "schema": "direction-lab.cb1.c11-legality-batch.v1",
        "campaign_id": "science-scout-2026-07-20.dual-pol-osl",
        "source_research_note": "c11-legality-batch-v1/R001-c11-legality-root-cause.md",
        "amends_subclaim_of": "D010",
        "MDE": MDE,
        "validation_seeds": VALIDATION_SEEDS,
        "test_seeds": TEST_SEEDS,
        "leakage_check": (
            "set(val) ∩ set(test) = ∅; "
            "set(val,test) ∩ set(B01-R 11-15,21-30) = ∅ (both asserted in code)"
        ),
        "R2_qam16": R2_16QAM,
        "elapsed_seconds": time.time() - t0,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "dd_step_grid": DD_STEP_GRID,
        "switch_offsets": SWITCH_OFFSETS,
        "fixed_mu_cma_mu_inherited_from": "B01-R HF6 interior optimum (NOT re-tuned)",
        # Minimal provenance: SHA-256 of the source closure (contract + runner +
        # new module + evaluator + cell runner + channel + cma anchor) so a future
        # reader can verify the artifact was produced by THIS source set.
        # Fix for audit issue #5 (artifact missing source closure hash). Read-only
        # wrt protected history (B01/B01-R raw untouched).
        "source_closure_sha256": _source_closure_hashes(),
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)
    log(f"[C11-LEGAL] DONE in {time.time() - t0:.1f}s — {out_path}")


if __name__ == "__main__":
    main()
