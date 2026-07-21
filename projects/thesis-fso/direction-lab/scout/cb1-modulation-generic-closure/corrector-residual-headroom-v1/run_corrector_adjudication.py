"""Corrector residual-headroom adjudication runner — single entry point.

    python run_corrector_adjudication.py --tune-and-eval

Implements batch-contract.v1.yaml (corrector-residual-headroom-v1):

  Phase 0: information-boundary tests (MUST PASS before any evaluation).
  Phase 1: tune blind affine ridge on validation cells × validation seeds.
  Phase 2: held-out evaluation on 11 cells × 10 fresh test seeds.
           For each (cell, seed):
             1. Run fixed-μ CMA μ=0.03 ONCE → zX, zY.
             2. Compute eval window ONCE for the cell.
             3. Apply all three comparators to the SAME z-stream, SAME window,
                SAME paired realization:
                  fixed_cma  = hard_16qam(z_eval)
                  blind      = blind_affine_compare_16qam(z_calib, z_eval, ridge)
                  oracle     = oracle_affine_bound_16qam(z_calib, z_eval, truth_calib, ridge)
             4. Evaluate each corrected stream with evaluate_dual_16qam
                (reports pi_ser AND fixed_label_ser separately).
  Phase 3: headroom decomposition + paired bootstrap CI.
  Phase 4: adjudicate A/B/C.

Discipline:
  * No-leakage seed split (asserted; disjoint from all prior batches).
  * fixed_mu_cma μ = 0.03 INHERITED from B01-R HF6 (NOT re-tuned).
  * blind_affine ridge tuned on validation, frozen BEFORE test.
  * All three comparators share the SAME z-stream, SAME window, SAME paired
    realization. CMA is run ONCE per (cell, seed).
  * oracle_affine is a Kill bound only (FR-21, FR-25); never a Go baseline.
  * pi_ser and fixed_label_ser reported SEPARATELY (metric contract invariant).
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
BATCH_DIR = HERE.parent                       # .../corrector-residual-headroom-v1
CB1_ROOT = BATCH_DIR.parent                   # .../cb1-modulation-generic-closure
ATLAS_DIR = CB1_ROOT / "baseline-atlas"
REPO_ROOT = HERE.parents[6]                   # worktree root
SIM_DIR = REPO_ROOT / "projects" / "simulation"
for p in (str(SIM_DIR), str(ATLAS_DIR), str(BATCH_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402
import cb1_evaluator as evaluator  # noqa: E402
import cb1_cell_runner as atlas_runner  # noqa: E402


# =============================================================================
# Contract constants (mirror batch-contract.v1.yaml)
# =============================================================================

FROZEN = {
    "alpha": 4.2, "beta": 1.4, "block": 100, "t_s": 4e-10, "method": "gar",
    "cma_mu_fixed": 0.03,  # INHERITED from B01-R HF6 (NOT re-tuned; no double-dip)
    "cma_taps": 11, "cma_block_size": 64,
    "r2_qam16": 1.32,
}
MDE = 0.005  # practical significance threshold (PI-SER absolute)
R2_16QAM = 1.32

# 11 atlas cells (SAME as B01 / B01-R / c11-legality; raw preserved).
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

# NEW disjoint seeds (no reuse of any prior batch).
VALIDATION_SEEDS = [61, 62, 63, 64, 65]
TEST_SEEDS = [71, 72, 73, 74, 75, 76, 77, 78, 79, 80]
# Union of all prior-batch seeds: B01 [11-20], B01-R [11-15, 21-30], c11-legality [31-35, 41-50].
_PRIOR_SEEDS = set(list(range(11, 21)) + list(range(21, 31)) + list(range(31, 36)) + list(range(41, 51)))
assert set(VALIDATION_SEEDS).isdisjoint(set(TEST_SEEDS)), "LEAKAGE: val/test overlap"
assert set(VALIDATION_SEEDS).isdisjoint(_PRIOR_SEEDS), "LEAKAGE: val overlaps prior batch"
assert set(TEST_SEEDS).isdisjoint(_PRIOR_SEEDS), "LEAKAGE: test overlaps prior batch"

# blind_affine ridge grid (FROZEN — mirrors batch-contract.v1.yaml).
RIDGE_GRID = [1e-8, 1e-6, 1e-4, 1e-2, 1.0]


# =============================================================================
# Realisation + window + CMA helpers
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
    """Compute eval window ONCE per cell; reused for all comparators."""
    return atlas_runner.eval_window_for(
        int(cell["n_symbols"]), int(FROZEN["cma_taps"]),
        window_symbols=256, block_size=int(FROZEN["cma_block_size"]),
    )


def run_fixed_mu_cma(cell, realization):
    """System anchor. μ = 0.03 INHERITED from B01-R HF6. ONE causal pass.
    Called ONCE per (cell, seed); zX/zY shared by all three comparators.
    """
    return atlas_runner.standard_cma_godard_with_z(
        realization["rX"], realization["rY"],
        n_tap=int(FROZEN["cma_taps"]), mu=float(FROZEN["cma_mu_fixed"]),
        R2=R2_16QAM, block_size=int(FROZEN["cma_block_size"]),
    )


# =============================================================================
# Per-(cell, seed) evaluation: SAME z-stream, SAME window, 3 comparators
# =============================================================================

def _split_calib_eval(zX, zY, realization, *, eval_start, calibration_end, eval_end):
    """Build the calib/eval slices for both z and truth (truth only for oracle)."""
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
    return {
        "z_calib": z_calib, "z_eval": z_eval,
        "truth_calib": truth_calib, "truth_eval": truth_eval,
        "bits_x_eval": bits_x_eval, "bits_y_eval": bits_y_eval,
    }


def _metrics_for_corrected_stream(corrected_x, corrected_y, *, truth_eval, bits_x_eval, bits_y_eval):
    """Evaluate a corrected dual-pol stream. Returns BOTH pi_ser AND
    fixed_label_ser (metric contract: report both, never interchange)."""
    m = evaluator.evaluate_dual_16qam(
        corrected_x, corrected_y,
        truth_eval[:, 0], truth_eval[:, 1], bits_x_eval, bits_y_eval,
    )
    return {
        "pi_ser": float(m["pi_ser"]),
        "fixed_label_ser": float(m["fixed_label_ser"]),
        "pi_ber": float(m["pi_ber"]),
        "fixed_label_ber": float(m["fixed_label_ber"]),
    }


def evaluate_one_cell_one_seed(cell, *, seed, ridge, eval_window):
    """The CORE adjudication primitive: ONE CMA run, ONE window, 3 comparators.

    Returns a dict with pi_ser and fixed_label_ser for all three comparators,
    computed from the SAME z-stream, SAME window, SAME paired realization.
    """
    realization = make_realization(cell, seed)
    cma_out = run_fixed_mu_cma(cell, realization)
    eval_start, calibration_end, eval_end, _ = eval_window

    if cma_out["diverged"]:
        return {
            "diverged": True,
            "pi_ser_fixed_cma": float("nan"),
            "pi_ser_blind": float("nan"),
            "pi_ser_oracle": float("nan"),
            "fixed_label_ser_fixed_cma": float("nan"),
            "fixed_label_ser_blind": float("nan"),
            "fixed_label_ser_oracle": float("nan"),
        }

    slices = _split_calib_eval(
        cma_out["zX"], cma_out["zY"], realization,
        eval_start=eval_start, calibration_end=calibration_end, eval_end=eval_end,
    )
    z_calib = slices["z_calib"]
    z_eval = slices["z_eval"]
    truth_calib = slices["truth_calib"]
    truth_eval = slices["truth_eval"]
    bits_x_eval = slices["bits_x_eval"]
    bits_y_eval = slices["bits_y_eval"]

    # --- Comparator 1: fixed_cma (nearest-16QAM on raw z_eval) ---
    fixed_pred = evaluator.hard_16qam(z_eval)
    m_fixed = _metrics_for_corrected_stream(
        fixed_pred[:, 0], fixed_pred[:, 1],
        truth_eval=truth_eval, bits_x_eval=bits_x_eval, bits_y_eval=bits_y_eval,
    )

    # --- Comparator 2: blind_affine (receiver-visible; NO TX truth) ---
    # NOTE: blind_affine_compare_16qam signature is (z_calibration, z_evaluation, *, ridge).
    # We do NOT pass truth_calibration. Information boundary is enforced by signature.
    blind_out = evaluator.blind_affine_compare_16qam(z_calib, z_eval, ridge=ridge)
    blind_corrected = blind_out["corrected"]
    m_blind = _metrics_for_corrected_stream(
        blind_corrected[:, 0], blind_corrected[:, 1],
        truth_eval=truth_eval, bits_x_eval=bits_x_eval, bits_y_eval=bits_y_eval,
    )

    # --- Comparator 3: oracle_affine (Kill bound; uses TX truth) ---
    oracle_corrected = evaluator.oracle_affine_bound_16qam(
        z_calib, z_eval, truth_calib, ridge=ridge,
    )
    m_oracle = _metrics_for_corrected_stream(
        oracle_corrected[:, 0], oracle_corrected[:, 1],
        truth_eval=truth_eval, bits_x_eval=bits_x_eval, bits_y_eval=bits_y_eval,
    )

    return {
        "diverged": False,
        "pi_ser_fixed_cma": m_fixed["pi_ser"],
        "pi_ser_blind": m_blind["pi_ser"],
        "pi_ser_oracle": m_oracle["pi_ser"],
        "fixed_label_ser_fixed_cma": m_fixed["fixed_label_ser"],
        "fixed_label_ser_blind": m_blind["fixed_label_ser"],
        "fixed_label_ser_oracle": m_oracle["fixed_label_ser"],
        # BER also kept for transparency (not used in verdict).
        "pi_ber_fixed_cma": m_fixed["pi_ber"],
        "pi_ber_blind": m_blind["pi_ber"],
        "pi_ber_oracle": m_oracle["pi_ber"],
    }


# =============================================================================
# Tuning (validation cells × validation seeds ONLY)
# =============================================================================

def tune_blind_ridge(validation_cells, log=print):
    """Pick ridge by minimizing mean PI-SER_blind over validation cells × seeds.

    Returns the frozen ridge value. Score = -(mean PI-SER + 0.1 * divergence_rate).
    """
    log("  [tune] scanning blind_affine ridge on validation...")
    best_ridge = None
    best_score = None
    for ridge in RIDGE_GRID:
        pis = []
        n_div = 0
        n_total = 0
        for cell in validation_cells:
            ew = _eval_window_for_cell(cell)
            for seed in VALIDATION_SEEDS:
                n_total += 1
                rec = evaluate_one_cell_one_seed(cell, seed=seed, ridge=ridge, eval_window=ew)
                if rec["diverged"]:
                    pis.append(1.0)
                    n_div += 1
                    continue
                pis.append(rec["pi_ser_blind"])
        mean_pi = float(np.mean(pis)) if pis else 1.0
        div_rate = n_div / max(n_total, 1)
        score = -(mean_pi + 0.1 * div_rate)
        if best_score is None or score > best_score:
            best_score = score
            best_ridge = ridge
        log(f"    ridge={ridge:.1e}: mean_PI_blind={mean_pi:.4f} "
            f"div_rate={div_rate:.2f} score={score:.4f}")
    log(f"  [tune] BEST ridge={best_ridge:.1e}, score={best_score:.4f}")
    return {"best_ridge": float(best_ridge), "ridge_grid": RIDGE_GRID}


# =============================================================================
# Held-out evaluation (test seeds ONLY)
# =============================================================================

def evaluate_held_out(frozen_ridge, log=print):
    results = {"cells": []}
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
            "per_seed": [],
        }
        ew = _eval_window_for_cell(cell)
        cell_record["eval_window"] = {
            "eval_start": ew[0], "calibration_end": ew[1], "eval_end": ew[2],
        }

        for seed in TEST_SEEDS:
            rec = evaluate_one_cell_one_seed(cell, seed=seed, ridge=frozen_ridge, eval_window=ew)
            rec["seed"] = int(seed)
            cell_record["per_seed"].append(rec)

        cell_record["aggregate"] = _aggregate_cell(cell_record["per_seed"])
        elapsed = time.time() - t_start
        agg = cell_record["aggregate"]
        log(f"  cell {cell['id']}: {elapsed:.1f}s — "
            f"fixed={agg['pi_ser_fixed_cma_mean']:.4f}, "
            f"blind={agg['pi_ser_blind_mean']:.4f}, "
            f"oracle={agg['pi_ser_oracle_mean']:.4f}, "
            f"H_total={agg['h_total_mean']:.4f}, "
            f"H_residual={agg['h_residual_mean']:.4f}, "
            f"coverage_blind={agg['coverage_blind_mean']:.4f}")
        results["cells"].append(cell_record)
    return results


def _aggregate_cell(per_seed):
    agg = {}
    n_div = sum(1 for s in per_seed if s.get("diverged", False))
    for comp in ("fixed_cma", "blind", "oracle"):
        pi_vals = [s[f"pi_ser_{comp}"] for s in per_seed
                   if not s.get("diverged", False) and np.isfinite(s[f"pi_ser_{comp}"])]
        fl_vals = [s[f"fixed_label_ser_{comp}"] for s in per_seed
                   if not s.get("diverged", False) and np.isfinite(s[f"fixed_label_ser_{comp}"])]
        agg[f"pi_ser_{comp}_mean"] = float(np.mean(pi_vals)) if pi_vals else float("nan")
        agg[f"fixed_label_ser_{comp}_mean"] = float(np.mean(fl_vals)) if fl_vals else float("nan")
    agg["n_diverged_seeds"] = int(n_div)
    # Headroom decomposition (per-cell means).
    # H_total = max(fixed - oracle, 0); G_blind = fixed - blind; H_residual = max(blind - oracle, 0)
    agg["h_total_mean"] = float(max(agg["pi_ser_fixed_cma_mean"] - agg["pi_ser_oracle_mean"], 0.0)) \
        if np.isfinite(agg["pi_ser_fixed_cma_mean"]) and np.isfinite(agg["pi_ser_oracle_mean"]) else float("nan")
    agg["g_blind_mean"] = float(agg["pi_ser_fixed_cma_mean"] - agg["pi_ser_blind_mean"]) \
        if np.isfinite(agg["pi_ser_fixed_cma_mean"]) and np.isfinite(agg["pi_ser_blind_mean"]) else float("nan")
    agg["h_residual_mean"] = float(max(agg["pi_ser_blind_mean"] - agg["pi_ser_oracle_mean"], 0.0)) \
        if np.isfinite(agg["pi_ser_blind_mean"]) and np.isfinite(agg["pi_ser_oracle_mean"]) else float("nan")
    agg["coverage_blind_mean"] = float(agg["g_blind_mean"] / agg["h_total_mean"]) \
        if (np.isfinite(agg["h_total_mean"]) and agg["h_total_mean"] > 0
            and np.isfinite(agg["g_blind_mean"])) else float("nan")
    return agg


# =============================================================================
# Paired bootstrap CI (cells + seeds paired, hierarchical)
# =============================================================================

def paired_bootstrap_ci(deltas, *, n_boot=10000, alpha=0.05, seed=20260721):
    if not deltas:
        return {"mean": float("nan"), "lower": float("nan"),
                "upper": float("nan"), "n": 0}
    arr = np.asarray(deltas, dtype=float)
    n = len(arr)
    rng = np.random.default_rng(seed)
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


def per_seed_delta(cell_record, *, comp_a, comp_b):
    """Per-seed Δ PI-SER = pi_ser_comp_a - pi_ser_comp_b."""
    deltas = []
    for s in cell_record["per_seed"]:
        if s.get("diverged", False):
            continue
        a = s.get(f"pi_ser_{comp_a}")
        b = s.get(f"pi_ser_{comp_b}")
        if a is None or b is None or np.isnan(a) or np.isnan(b):
            continue
        deltas.append(float(a - b))
    return deltas


def hierarchical_paired_bootstrap(results, *, comp_a, comp_b, n_boot=10000):
    """Two-level paired bootstrap: resample cells, then within each resampled
    cell resample seeds. Returns macro mean + 95% CI on (pi_ser_a - pi_ser_b)."""
    held = [c for c in results["cells"] if c["is_held_out_cell"]]
    per_cell = [per_seed_delta(c, comp_a=comp_a, comp_b=comp_b) for c in held]
    valid = [d for d in per_cell if len(d) > 0]
    if not valid:
        return {"macro_mean": float("nan"), "lower": float("nan"),
                "upper": float("nan"), "n_cells": 0,
                "per_cell_means": [float("nan")] * len(per_cell)}
    cell_means = np.array([float(np.mean(d)) for d in per_cell])
    rng = np.random.default_rng(20260721)
    n_cells = len(valid)
    boot_macros = np.empty(n_boot)
    for b in range(n_boot):
        cell_idx = rng.integers(0, n_cells, size=n_cells)
        macro = []
        for ci in cell_idx:
            d = valid[ci]
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

def adjudicate(results, frozen_ridge):
    held = [c for c in results["cells"] if c["is_held_out_cell"]]

    # Macro means over held-out cells.
    def macro(key):
        vals = [c["aggregate"][key] for c in held
                if np.isfinite(c["aggregate"].get(key, float("nan")))]
        return float(np.mean(vals)) if vals else float("nan")

    macro_h_total = macro("h_total_mean")
    macro_g_blind = macro("g_blind_mean")
    macro_h_residual = macro("h_residual_mean")
    macro_coverage = macro("coverage_blind_mean")

    # Per-cell counts.
    n_cells_h_total_ge_mde = sum(
        1 for c in held
        if np.isfinite(c["aggregate"].get("h_total_mean", float("nan")))
        and c["aggregate"]["h_total_mean"] >= MDE
    )
    n_cells_h_residual_ge_mde = sum(
        1 for c in held
        if np.isfinite(c["aggregate"].get("h_residual_mean", float("nan")))
        and c["aggregate"]["h_residual_mean"] >= MDE
    )
    # Worst-cell blind degradation (blind worse than fixed_cma).
    worst_blind_degradation = max(
        (c["aggregate"]["pi_ser_blind_mean"] - c["aggregate"]["pi_ser_fixed_cma_mean"]
         for c in held
         if np.isfinite(c["aggregate"].get("pi_ser_blind_mean", float("nan")))),
        default=float("nan"),
    )

    # Hierarchical paired CIs on the three key deltas.
    ci_h_total = hierarchical_paired_bootstrap(
        results, comp_a="fixed_cma", comp_b="oracle")
    ci_g_blind = hierarchical_paired_bootstrap(
        results, comp_a="fixed_cma", comp_b="blind")
    ci_h_residual = hierarchical_paired_bootstrap(
        results, comp_a="blind", comp_b="oracle")

    # Per-cell paired CIs (secondary).
    per_cell_ci_h_total = {}
    per_cell_ci_h_residual = {}
    for c in held:
        per_cell_ci_h_total[c["cell_id"]] = paired_bootstrap_ci(
            per_seed_delta(c, comp_a="fixed_cma", comp_b="oracle"))
        per_cell_ci_h_residual[c["cell_id"]] = paired_bootstrap_ci(
            per_seed_delta(c, comp_a="blind", comp_b="oracle"))

    # Verdict (frozen rule, batch-contract.v1.yaml decision_rule).
    # Per user brief: A = blind affine leaves a stable, MDE-sized, oracle-recoverable
    # residual. "Blind does not degrade" is NOT an A condition — if blind
    # degrades (G_blind < 0), the residual is LARGER and the target is EASIER.
    a_conditions = {
        "macro_h_total_ge_mde": macro_h_total >= MDE,
        "macro_h_residual_ge_mde": macro_h_residual >= MDE,
        "h_residual_ge_mde_in_at_least_5_of_7_cells": n_cells_h_residual_ge_mde >= 5,
        "ci_h_residual_lower_bound_gt_0": (
            np.isfinite(ci_h_residual.get("lower", float("nan")))
            and ci_h_residual["lower"] > 0.0
        ),
    }
    # B requires blind affine to ACTUALLY close a meaningful share (coverage ≥ 0.5).
    # Negative coverage (blind degrades) is NOT B.
    b_conditions = {
        "macro_h_total_lt_mde": macro_h_total < MDE,
        "macro_h_residual_lt_mde_and_coverage_ge_0_5": (
            macro_h_residual < MDE and (
                np.isfinite(macro_coverage) and macro_coverage >= 0.5
            )
        ),
        "macro_coverage_blind_ge_0_95": (
            np.isfinite(macro_coverage) and macro_coverage >= 0.95
        ),
        "h_residual_ge_mde_in_less_than_5_of_7_cells_and_coverage_ge_0_5": (
            n_cells_h_residual_ge_mde < 5 and (
                np.isfinite(macro_coverage) and macro_coverage >= 0.5
            )
        ),
    }
    # Borderline check for C: macro_h_residual within 0.5*MDE of MDE AND
    # coverage is in [0, 0.5] (neither closes nor leaves clearly).
    borderline = (
        abs(macro_h_residual - MDE) < 0.5 * MDE
        and np.isfinite(macro_coverage)
        and 0.0 <= macro_coverage < 0.5
    )

    if all(a_conditions.values()):
        verdict = "A_LEARNED_CORRECTOR_TARGET_READY"
    elif any(b_conditions.values()):
        verdict = "B_LEGAL_BLIND_BASELINE_CLOSES_TARGET"
    elif borderline:
        verdict = "C_UNRESOLVED"
    else:
        # If A fails (e.g., residual not stable) AND B doesn't fire (coverage
        # not meaningful), default to B with a note — the target isn't clearly
        # ready and blind hasn't clearly closed it.
        verdict = "B_LEGAL_BLIND_BASELINE_CLOSES_TARGET"

    return {
        "verdict": verdict,
        "macro_h_total": macro_h_total,
        "macro_g_blind": macro_g_blind,
        "macro_h_residual": macro_h_residual,
        "macro_coverage_blind": macro_coverage,
        "n_cells_h_total_ge_mde": n_cells_h_total_ge_mde,
        "n_cells_h_residual_ge_mde": n_cells_h_residual_ge_mde,
        "n_held_out_cells": len(held),
        "worst_blind_degradation": worst_blind_degradation,
        "ci_h_total": ci_h_total,
        "ci_g_blind": ci_g_blind,
        "ci_h_residual": ci_h_residual,
        "per_cell_ci_h_total": per_cell_ci_h_total,
        "per_cell_ci_h_residual": per_cell_ci_h_residual,
        "mde": MDE,
        "a_conditions": a_conditions,
        "b_conditions": b_conditions,
        "borderline_residual_for_C": bool(borderline),
        "frozen_ridge": frozen_ridge,
    }


# =============================================================================
# Source-closure provenance
# =============================================================================

def _sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


_SOURCE_CLOSURE_PATHS = [
    BATCH_DIR / "batch-contract.v1.yaml",
    BATCH_DIR / "run_corrector_adjudication.py",
    BATCH_DIR / "tests" / "test_information_boundary.py",
    ATLAS_DIR / "cb1_evaluator.py",
    ATLAS_DIR / "cb1_cell_runner.py",
    REPO_ROOT / "projects" / "simulation" / "common" / "_dual_pol_channel.py",
    REPO_ROOT / "projects" / "simulation" / "common" / "_modulation.py",
]


def _source_closure_hashes() -> dict[str, str]:
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
        TEST_SEEDS = [71, 72]
        VALIDATION_SEEDS = [61]

    log = lambda msg: print(msg, flush=True)

    log("[CORR-ADJ] Phase 0: information-boundary tests (must PASS before any evaluation)")
    import pytest
    exit_code = pytest.main([
        "-x", "--tb=short", "-q",
        str(BATCH_DIR / "tests" / "test_information_boundary.py"),
    ])
    if exit_code != 0:
        log(f"[CORR-ADJ] FATAL: information-boundary tests FAILED (pytest exit {exit_code}). "
            "Aborting per contract.")
        sys.exit(2)
    log("[CORR-ADJ] information-boundary tests PASS.")

    log("[CORR-ADJ] Phase 1: tuning blind_affine ridge on validation cells × validation seeds")
    validation_cells = [c for c in ATLAS_V1_16QAM_CELLS if c["id"] in VALIDATION_CELL_IDS]
    log(f"  validation cells ({len(validation_cells)}): {[c['id'] for c in validation_cells]}")
    log(f"  validation_seeds={VALIDATION_SEEDS}  test_seeds={TEST_SEEDS}  (disjoint asserted)")
    tune_result = tune_blind_ridge(validation_cells, log=log)
    frozen_ridge = tune_result["best_ridge"]

    params_out = {
        "fixed_mu_cma_mu": float(FROZEN["cma_mu_fixed"]),
        "blind_affine_best_ridge": float(frozen_ridge),
        "ridge_grid": RIDGE_GRID,
        "validation_seeds": VALIDATION_SEEDS,
        "test_seeds": TEST_SEEDS,
        "mde": MDE,
    }
    params_path = BATCH_DIR / "artifacts" / "frozen-params.v1.yaml"
    with open(params_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(params_out, f, sort_keys=False, allow_unicode=True)
    log(f"[CORR-ADJ] frozen params: {params_path}")

    log("[CORR-ADJ] Phase 2: held-out evaluation on 11 cells × 10 fresh test seeds")
    results = evaluate_held_out(frozen_ridge, log=log)

    log("[CORR-ADJ] Phase 3: headroom decomposition + paired bootstrap CI on 7 held-out cells × 10 test seeds")

    log("[CORR-ADJ] Phase 4: adjudication (A/B/C, frozen BEFORE running)")
    adjudication = adjudicate(results, frozen_ridge)
    log(f"[CORR-ADJ] VERDICT: {adjudication['verdict']}")
    log(f"  macro H_total      = {adjudication['macro_h_total']:+.5f}  "
        f"(need ≥ {MDE} for A)")
    log(f"  macro G_blind      = {adjudication['macro_g_blind']:+.5f}")
    log(f"  macro H_residual   = {adjudication['macro_h_residual']:+.5f}  "
        f"(need ≥ {MDE} for A)")
    log(f"  macro coverage_blind = {adjudication['macro_coverage_blind']:.4f}  "
        f"(need < 0.95 for A)")
    log(f"  cells with H_residual ≥ MDE: {adjudication['n_cells_h_residual_ge_mde']}/7  "
        f"(need ≥ 5 for A)")
    log(f"  worst blind degradation = {adjudication['worst_blind_degradation']:+.5f}  "
        f"(need ≤ {MDE})")
    log(f"  CI on H_residual: [{adjudication['ci_h_residual']['lower']:+.5f}, "
        f"{adjudication['ci_h_residual']['upper']:+.5f}]")

    results["adjudication"] = adjudication
    results["frozen_params"] = params_out
    results["metadata"] = {
        "schema": "direction-lab.cb1.corrector-residual-headroom.v1",
        "campaign_id": "science-scout-2026-07-20.dual-pol-osl",
        "triggered_by": "S009_user_brief_2026-07-21",
        "related_decisions": ["D010", "D011-amended", "D012"],
        "MDE": MDE,
        "validation_seeds": VALIDATION_SEEDS,
        "test_seeds": TEST_SEEDS,
        "leakage_check": (
            "set(val) ∩ set(test) = ∅; "
            "set(val,test) ∩ set(B01 ∪ B01-R ∪ c11-legality {11-50}) = ∅ (asserted)"
        ),
        "R2_qam16": R2_16QAM,
        "elapsed_seconds": time.time() - t0,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "ridge_grid": RIDGE_GRID,
        "fixed_mu_cma_mu_inherited_from": "B01-R HF6 interior optimum (NOT re-tuned)",
        "source_closure_sha256": _source_closure_hashes(),
        "information_boundary_note": (
            "blind_affine_compare_16qam reads ONLY z-derived pseudo-labels; "
            "oracle_affine_bound_16qam reads TX truth (Kill bound only, FR-21/FR-25). "
            "All three comparators share the SAME z-stream, SAME eval window, "
            "SAME paired realization. fixed-μ CMA run ONCE per (cell, seed)."
        ),
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)
    log(f"[CORR-ADJ] DONE in {time.time() - t0:.1f}s — {out_path}")


if __name__ == "__main__":
    main()
