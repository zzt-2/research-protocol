"""Fairness Batch B01-R driver — runs the correction contract.

Single entry point:
    python run_fairness_batch_b01r.py --tune-and-eval

Fixes vs B01:
  1. No-leakage seed split: tuning=[11..15], test=[21..30] (disjoint).
  2. Validation-optimal fixed-μ CMA is genuinely tuned as a Go comparator.
  3. Decision-rule denominator = 7 held-out cells (achievable: 5/7 = close).
  4. 4-category label audit (inner-ring, AWGN-dominated, healthy, ambiguous).
  5. Real detector metrics: per-cell AUROC (NA for single-class), PR-AUC,
     recall@5%FPR, false-alarm, degradation onset, warning lead time,
     Brier/ECE.
  6. Paired bootstrap CI over seeds (10k resamples).
  7. C05 score uses REAL alert output (earliness), not -min(z2_ratio).

Per batch-contract.v1.yaml (B01-R):
  - tuning: 4 validation cells × 5 tuning seeds, per-method grid,
    divergence penalty.
  - held-out eval: 7 held-out cells × 10 test seeds (NEW, disjoint).
  - aggregate Go/Kill uses ONLY held-out × test_seeds.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import yaml

HERE = Path(__file__).resolve()
BATCH_DIR = HERE.parent
CB1_ROOT = BATCH_DIR.parent
B01_DIR = CB1_ROOT / "fairness-batch-b01"
ATLAS_DIR = CB1_ROOT / "baseline-atlas"
ADJUD_DIR = CB1_ROOT / "baseline-adjudication-batch"
REPO_ROOT = HERE.parents[6]
SIM_DIR = REPO_ROOT / "projects" / "simulation"
for p in (str(SIM_DIR), str(BATCH_DIR), str(B01_DIR), str(ATLAS_DIR), str(ADJUD_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402
import cb1_evaluator as evaluator  # noqa: E402
import cb1_cell_runner as atlas_runner  # noqa: E402
import b01_candidates as cand  # noqa: E402
import b01r_detector as det  # noqa: E402


# =============================================================================
# Contract constants (frozen; mirror batch-contract.v1.yaml B01-R)
# =============================================================================

FROZEN = {
    "alpha": 4.2, "beta": 1.4, "block": 100, "t_s": 4e-10, "method": "gar",
    "cma_mu_anchor": 0.001, "cma_taps": 11, "cma_block_size": 64,
    "r2_qam16": 1.32, "affine_ridge": 1e-6,
}
MDE = 0.005
R2_16QAM = 1.32

# 11 atlas cells (SAME as B01; raw preserved).
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

# B01-R NO-LEAKAGE split.
VALIDATION_CELL_IDS = {
    "16qam-snr20-nominal-short",
    "16qam-snr20-fg1000-short",
    "16qam-snr20-sop40e-short",
    "16qam-snr20-nominal-long",  # long cell so tuning sees convergence stability
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
TUNING_SEEDS = [11, 12, 13, 14, 15]  # disjoint from test
TEST_SEEDS = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30]  # FRESH, disjoint
assert set(TUNING_SEEDS).isdisjoint(set(TEST_SEEDS)), "LEAKAGE: tuning/test seeds overlap"

# Tuning grids per method (B01-R; mirror batch-contract.v1.yaml B01-R).
TUNE_GRID = {
    "fixed_mu_cma": {  # NEW genuine comparator
        "mu": [1e-4, 3e-4, 1e-3, 3e-3, 1e-2],
    },
    "C08": {
        "alpha": [0.1, 1.0, 10.0],
    },
    "C10": {
        "mu": [1e-5, 1e-4, 3e-4, 1e-3, 3e-3],
    },
    "C11": {
        "dd_step_size": [1e-4, 3e-4, 1e-3, 3e-3, 1e-2],
    },
    "C05": {  # tuned by macro-AUROC over two-class validation cells ONLY
        "z2_ratio_threshold": [0.2, 0.3, 0.4, 0.5, 0.6],
        "cusum_drift": [0.01, 0.05, 0.1],
    },
}

CLOSE_THRESHOLD = 5  # of 7 held-out cells (was 9/11 unreachable)


# =============================================================================
# Realisation + PI-SER helpers (re-used from B01 design)
# =============================================================================

def make_realization(cell, seed):
    gamma_bar = float(10.0 ** (float(cell["snr_db"]) / 10.0))
    return generate_shared_realization_dp(
        int(cell["n_symbols"]), float(FROZEN["alpha"]), float(FROZEN["beta"]),
        float(cell["f_g_hz"]), sop_rate=float(cell["sop_rate"]), seed=int(seed),
        gamma_bar=gamma_bar, block=int(FROZEN["block"]), t_s=float(FROZEN["t_s"]),
        method=str(FROZEN["method"]), modulation=str(cell.get("modulation", "qam16")),
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
    oracle_corr = evaluator.oracle_affine_bound_16qam(z_calib, z_eval, truth_calib, ridge=FROZEN["affine_ridge"])
    nearest_m = evaluator.evaluate_dual_16qam(
        nearest_pred[:, 0], nearest_pred[:, 1],
        truth_eval[:, 0], truth_eval[:, 1], bits_x_eval, bits_y_eval,
    )
    oracle_m = evaluator.evaluate_dual_16qam(
        oracle_corr[:, 0], oracle_corr[:, 1],
        truth_eval[:, 0], truth_eval[:, 1], bits_x_eval, bits_y_eval,
    )
    return {
        "nearest_pi_ser": float(nearest_m["pi_ser"]),
        "oracle_pi_ser": float(oracle_m["pi_ser"]),
    }


def _eval_window_for_cell(cell):
    return atlas_runner.eval_window_for(
        int(cell["n_symbols"]), int(FROZEN["cma_taps"]),
        window_symbols=256, block_size=int(FROZEN["cma_block_size"]),
    )


# =============================================================================
# Method runners
# =============================================================================

def run_anchor(cell, realization):
    """CMA anchor (block_size=64, μ=0.001) — Atlas v1 identity, byte-regression."""
    return atlas_runner.standard_cma_godard_with_z(
        realization["rX"], realization["rY"],
        n_tap=int(FROZEN["cma_taps"]), mu=float(FROZEN["cma_mu_anchor"]),
        R2=R2_16QAM, block_size=int(FROZEN["cma_block_size"]),
    )


def run_fixed_mu_cma(cell, realization, *, mu):
    """Validation-optimal fixed-μ CMA (genuine Go comparator).

    Same as anchor but with μ = tuned value (NOT frozen 0.001).
    """
    return atlas_runner.standard_cma_godard_with_z(
        realization["rX"], realization["rY"],
        n_tap=int(FROZEN["cma_taps"]), mu=float(mu), R2=R2_16QAM,
        block_size=int(FROZEN["cma_block_size"]),
    )


def run_c08(cell, realization, *, alpha):
    return cand.c08_adaptive_mu_bandit(
        realization["rX"], realization["rY"],
        n_tap=int(FROZEN["cma_taps"]), R2=R2_16QAM,
        block_size=int(FROZEN["cma_block_size"]),
        mu_candidates=(1e-4, 3e-4, 1e-3, 3e-3, 1e-2), alpha=float(alpha),
    )


def run_c10(cell, realization, *, mu):
    return cand.c10_per_symbol_cma(
        realization["rX"], realization["rY"],
        n_tap=int(FROZEN["cma_taps"]), mu=float(mu), R2=R2_16QAM,
    )


def run_c11(cell, realization, *, dd_step_size):
    return cand.c11_cma_dd_lms_cascade(
        realization["rX"], realization["rY"],
        n_tap=int(FROZEN["cma_taps"]), cma_mu=float(FROZEN["cma_mu_anchor"]),
        cma_R2=R2_16QAM, cma_block_size=int(FROZEN["cma_block_size"]),
        dd_step_size=float(dd_step_size), dd_iterations=1,
        hard_decision_fn=evaluator.hard_16qam,
    )


# =============================================================================
# Tuning (validation cells × tuning seeds ONLY)
# =============================================================================

def _eval_combo_piser(method, combo, cells, seeds):
    """Negative mean PI-SER + divergence penalty (higher = better)."""
    pis: list[float] = []
    n_div = 0
    n_total = 0
    for cell in cells:
        for seed in seeds:
            n_total += 1
            realization = make_realization(cell, seed)
            if method == "fixed_mu_cma":
                out = run_fixed_mu_cma(cell, realization, mu=combo["mu"])
            elif method == "C08":
                out = run_c08(cell, realization, alpha=combo["alpha"])
            elif method == "C10":
                out = run_c10(cell, realization, mu=combo["mu"])
            elif method == "C11":
                out = run_c11(cell, realization, dd_step_size=combo["dd_step_size"])
            else:
                raise ValueError(method)
            if out.get("diverged", False):
                pis.append(1.0)
                n_div += 1
                continue
            es, ce, ee, _ = _eval_window_for_cell(cell)
            m = pi_ser_from_z(out["zX"], out["zY"], realization,
                              eval_start=es, calibration_end=ce, eval_end=ee)
            pis.append(m["nearest_pi_ser"])
    if not pis:
        return -1.0
    mean_pi = float(np.mean(pis))
    div_rate = n_div / max(n_total, 1)
    return -(mean_pi + 0.1 * div_rate)


def _eval_combo_c05(combo, cells, seeds):
    """Macro-AUROC over TWO-CLASS validation cells only (single-class excluded).

    Score = REAL C05 alert earliness (-first_alert_block, -inf if no alert).
    """
    per_cell_aurocs: list[float] = []
    for cell in cells:
        scores: list[float] = []
        labels: list[int] = []
        for seed in seeds:
            realization = make_realization(cell, seed)
            anchor_out = run_anchor(cell, realization)
            es, ce, ee, _ = _eval_window_for_cell(cell)
            m = pi_ser_from_z(anchor_out["zX"], anchor_out["zY"], realization,
                              eval_start=es, calibration_end=ce, eval_end=ee)
            # 4-category label (derive ratios from output_power if direct field absent)
            ratios = []
            for t in anchor_out["trace"]:
                r = t.get("z2_over_R2_ratio")
                if r is None or (isinstance(r, float) and np.isnan(r)):
                    op = t.get("output_power")
                    if op is None or (isinstance(op, float) and np.isnan(op)):
                        ratios.append(float("nan"))
                    else:
                        ratios.append(float(op) / (2.0 * R2_16QAM) if R2_16QAM > 0 else float("nan"))
                else:
                    ratios.append(float(r))
            ratios = [r for r in ratios if not np.isnan(r)]
            label_4cat = det.assign_label_4cat(
                nearest_pi_ser=m["nearest_pi_ser"],
                oracle_pi_ser=m["oracle_pi_ser"],
                mean_z2_ratio=float(np.mean(ratios)) if ratios else float("nan"),
                min_z2_ratio=float(np.min(ratios)) if ratios else float("nan"),
                mde=MDE,
            )
            bin_label = det.collapse_label_for_auroc(label_4cat)
            if bin_label is None:
                continue  # AWGN-dominated / ambiguous excluded from AUROC tuning
            alert_out = det.c05_alert_score(
                anchor_out["trace"],
                z2_ratio_threshold=combo["z2_ratio_threshold"],
                cusum_drift=combo["cusum_drift"],
            )
            scores.append(alert_out["score"])
            labels.append(bin_label)
        if not scores:
            continue
        a = det.auroc_or_none(scores, labels)
        if a is not None:
            per_cell_aurocs.append(a)
    if not per_cell_aurocs:
        return -1.0  # no two-class cells → cannot tune; record -1
    return float(np.mean(per_cell_aurocs))


def tune_method(method, cells, seeds, log=print):
    log(f"  [tune] {method}: scanning grid...")
    grid_keys = list(TUNE_GRID[method].keys())
    grid_values = [TUNE_GRID[method][k] for k in grid_keys]
    combos = [{}]
    for k, vals in zip(grid_keys, grid_values):
        new = []
        for c in combos:
            for v in vals:
                new.append({**c, k: v})
        combos = new
    best_combo = None
    best_score = None
    for combo in combos:
        try:
            if method == "C05":
                score = _eval_combo_c05(combo, cells, seeds)
            else:
                score = _eval_combo_piser(method, combo, cells, seeds)
        except Exception as exc:
            log(f"    combo {combo}: FAILED ({exc})")
            continue
        if best_score is None or score > best_score:
            best_score = score
            best_combo = combo
    log(f"  [tune] {method}: best={best_combo} score={best_score:.4f}")
    return {"method": method, "best_combo": best_combo, "best_score": float(best_score)}


# =============================================================================
# Held-out evaluation (test seeds ONLY)
# =============================================================================

def evaluate_held_out(frozen_params, log=print):
    results: dict[str, Any] = {"cells": []}
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
        es, ce, ee, _ = _eval_window_for_cell(cell)
        cell_record["eval_window"] = {"eval_start": es, "calibration_end": ce, "eval_end": ee}

        for seed in TEST_SEEDS:
            realization = make_realization(cell, seed)
            seed_record = {"seed": int(seed), "methods": {}}

            # Anchor
            anchor_out = run_anchor(cell, realization)
            if anchor_out["diverged"]:
                anchor_m = {"nearest_pi_ser": float("nan"), "oracle_pi_ser": float("nan")}
            else:
                anchor_m = pi_ser_from_z(anchor_out["zX"], anchor_out["zY"], realization,
                                         eval_start=es, calibration_end=ce, eval_end=ee)

            # 4-category label audit on anchor trace.
            # The anchor's trace has `output_power` (mean |z_x|^2+|z_y|^2 per block)
            # but NOT a direct `z2_over_R2_ratio` field; derive ratio here so the
            # label does not silently fall to NaN when the field is absent.
            ratios: list[float] = []
            for t in anchor_out["trace"]:
                r = t.get("z2_over_R2_ratio")
                if r is None or (isinstance(r, float) and np.isnan(r)):
                    op = t.get("output_power")
                    if op is None or (isinstance(op, float) and np.isnan(op)):
                        ratios.append(float("nan"))
                    else:
                        ratios.append(float(op) / (2.0 * R2_16QAM) if R2_16QAM > 0 else float("nan"))
                else:
                    ratios.append(float(r))
            ratios_clean = [r for r in ratios if not np.isnan(r)]
            mean_r = float(np.mean(ratios_clean)) if ratios_clean else float("nan")
            min_r = float(np.min(ratios_clean)) if ratios_clean else float("nan")
            label_4cat = det.assign_label_4cat(
                nearest_pi_ser=anchor_m["nearest_pi_ser"],
                oracle_pi_ser=anchor_m["oracle_pi_ser"],
                mean_z2_ratio=mean_r, min_z2_ratio=min_r, mde=MDE,
            )
            seed_record["methods"]["anchor"] = {
                "diverged": bool(anchor_out["diverged"]),
                **anchor_m,
                "trace_summary": _summarize_trace(anchor_out["trace"]),
                "label_4cat": label_4cat,
                "collapse_label_for_auroc": det.collapse_label_for_auroc(label_4cat),
                "mean_z2_ratio": mean_r,
                "min_z2_ratio": min_r,
                "degradation_onset_block": det.degradation_onset_block(anchor_out["trace"]),
                "_trace": anchor_out["trace"],  # kept for detector eval
            }

            # Detector baselines (run on anchor trace)
            # 1. min-z2-ratio scoring baseline (zero-param)
            min_z2_score = det.min_z2_ratio_score(anchor_out["trace"])
            # 2. C05 CUSUM/threshold detector (tuned)
            c05_params = frozen_params["C05"]["best_combo"]
            c05_out = det.c05_alert_score(
                anchor_out["trace"],
                z2_ratio_threshold=c05_params["z2_ratio_threshold"],
                cusum_drift=c05_params["cusum_drift"],
            )
            # Lead time = onset - alert_block. Positive = detector fires BEFORE onset (good).
            onset = seed_record["methods"]["anchor"]["degradation_onset_block"]
            alert_block = c05_out["first_alert_block"]
            if onset is not None and alert_block is not None:
                lead_time = onset - alert_block  # > 0 means detector precedes onset
            else:
                lead_time = None
            seed_record["methods"]["C05"] = {
                "score_min_z2_ratio": min_z2_score,
                "score_c05_alert_earliness": c05_out["score"],
                "alert_any": c05_out["alert_any"],
                "first_alert_block": alert_block,
                "n_alerts": c05_out["n_alerts"],
                "label_4cat": label_4cat,
                "collapse_label_for_auroc": det.collapse_label_for_auroc(label_4cat),
                "degradation_onset_block": onset,
                "warning_lead_time_blocks": lead_time,
                "tuned_params": c05_params,
            }

            # fixed-μ CMA (validation-optimal)
            fmu = frozen_params["fixed_mu_cma"]["best_combo"]
            fmu_out = run_fixed_mu_cma(cell, realization, mu=fmu["mu"])
            if fmu_out["diverged"]:
                seed_record["methods"]["fixed_mu_cma"] = {"diverged": True, "mu": fmu["mu"]}
            else:
                m = pi_ser_from_z(fmu_out["zX"], fmu_out["zY"], realization,
                                  eval_start=es, calibration_end=ce, eval_end=ee)
                seed_record["methods"]["fixed_mu_cma"] = {"diverged": False, "mu": fmu["mu"], **m}

            # C08
            c08p = frozen_params["C08"]["best_combo"]
            c08_out = run_c08(cell, realization, alpha=c08p["alpha"])
            if c08_out["diverged"]:
                seed_record["methods"]["C08"] = {"diverged": True, "alpha": c08p["alpha"]}
            else:
                m = pi_ser_from_z(c08_out["zX"], c08_out["zY"], realization,
                                  eval_start=es, calibration_end=ce, eval_end=ee)
                seed_record["methods"]["C08"] = {"diverged": False, "alpha": c08p["alpha"], **m}

            # C10
            c10p = frozen_params["C10"]["best_combo"]
            c10_out = run_c10(cell, realization, mu=c10p["mu"])
            if c10_out["diverged"]:
                seed_record["methods"]["C10"] = {"diverged": True, "mu": c10p["mu"]}
            else:
                m = pi_ser_from_z(c10_out["zX"], c10_out["zY"], realization,
                                  eval_start=es, calibration_end=ce, eval_end=ee)
                seed_record["methods"]["C10"] = {"diverged": False, "mu": c10p["mu"], **m}

            # C11
            c11p = frozen_params["C11"]["best_combo"]
            c11_out = run_c11(cell, realization, dd_step_size=c11p["dd_step_size"])
            if c11_out["diverged"]:
                seed_record["methods"]["C11"] = {"diverged": True, "dd_step_size": c11p["dd_step_size"]}
            else:
                m = pi_ser_from_z(c11_out["zX"], c11_out["zY"], realization,
                                  eval_start=es, calibration_end=ce, eval_end=ee)
                seed_record["methods"]["C11"] = {"diverged": False, "dd_step_size": c11p["dd_step_size"], **m}

            cell_record["per_seed"].append(seed_record)

        cell_record["aggregate"] = _aggregate_cell(cell_record["per_seed"])
        elapsed = time.time() - t_start
        log(f"  cell {cell['id']}: {elapsed:.1f}s — "
            f"anchor={cell_record['aggregate']['anchor']['nearest_pi_ser_mean']:.4f}, "
            f"fixed_mu={cell_record['aggregate']['fixed_mu_cma']['nearest_pi_ser_mean']:.4f}, "
            f"C08={cell_record['aggregate']['C08']['nearest_pi_ser_mean']:.4f}, "
            f"C10={cell_record['aggregate']['C10']['nearest_pi_ser_mean']:.4f}, "
            f"C11={cell_record['aggregate']['C11']['nearest_pi_ser_mean']:.4f}")
        results["cells"].append(cell_record)
    return results


def _summarize_trace(trace):
    if not trace:
        return {}
    ratios = [t.get("z2_over_R2_ratio", float("nan")) for t in trace if "z2_over_R2_ratio" in t]
    ratios = [r for r in ratios if not np.isnan(r)]
    return {
        "n_blocks": len(trace),
        "z2_ratio_min": float(np.min(ratios)) if ratios else float("nan"),
        "z2_ratio_max": float(np.max(ratios)) if ratios else float("nan"),
        "z2_ratio_final": float(ratios[-1]) if ratios else float("nan"),
    }


def _aggregate_cell(per_seed):
    agg: dict[str, Any] = {}

    # 4-category label counts
    label_counts: dict[str, int] = {}
    for s in per_seed:
        lbl = s["methods"]["anchor"].get("label_4cat", "ambiguous")
        label_counts[lbl] = label_counts.get(lbl, 0) + 1
    agg["label_4cat_counts"] = label_counts

    # PI-SER aggregates per method
    for method in ("anchor", "fixed_mu_cma", "C08", "C10", "C11"):
        vals_near = []
        vals_orac = []
        n_div = 0
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
        agg[method] = {
            "nearest_pi_ser_mean": float(np.mean(vals_near)) if vals_near else float("nan"),
            "oracle_pi_ser_mean": float(np.mean(vals_orac)) if vals_orac else float("nan"),
            "headroom_mean": float(np.mean([max(n - o, 0.0) for n, o in zip(vals_near, vals_orac)])) if vals_near and vals_orac else float("nan"),
            "n_non_diverged_seeds": int(len(vals_near)),
            "n_diverged_seeds": int(n_div),
        }

    # C05 detector metrics (REAL — fixes findings #2, #7, #8)
    # Use min_z2_score as the ranking score (zero-param baseline) AND
    # c05_alert_earliness as the tuned-detector ranking score.
    for score_key, score_field in [
        ("min_z2_ratio", "score_min_z2_ratio"),
        ("c05_alert_earliness", "score_c05_alert_earliness"),
    ]:
        scores: list[float] = []
        labels: list[int] = []
        lead_times: list[int] = []
        for s in per_seed:
            m = s["methods"].get("C05")
            if m is None:
                continue
            bin_label = m.get("collapse_label_for_auroc")
            if bin_label is None:
                continue  # exclude AWGN/ambiguous from AUROC
            score = m.get(score_field, float("nan"))
            if np.isnan(score):
                continue
            scores.append(float(score))
            labels.append(int(bin_label))
            lt = m.get("warning_lead_time_blocks")
            if lt is not None:
                lead_times.append(int(lt))
        auroc = det.auroc_or_none(scores, labels)
        pr = det.pr_auc_or_none(scores, labels)
        rec5 = det.recall_at_fpr(scores, labels, fpr=0.05)
        # False-alarm rate when declaring top-1 seed positive (per cell, n=10 seeds)
        far = det.false_alarm_rate(scores, labels, threshold_rank=1)
        # Brier/ECE: convert scores to pseudo-probabilities (note limitation)
        if scores:
            s_arr = np.asarray(scores)
            scale = max(float(np.std(s_arr)), 1e-6)
            probs = [det.detector_score_to_prob(s, score_scale=scale) for s in scores]
            brier = det.brier_score(probs, labels)
            ece = det.expected_calibration_error(probs, labels)
        else:
            brier = float("nan")
            ece = float("nan")
        agg[f"detector_{score_key}"] = {
            "auroc": auroc,  # may be None (single-class)
            "pr_auc": pr,
            "recall_at_5pct_fpr": rec5,
            "false_alarm_rate_top1": far,
            "brier_score": brier,
            "ece": ece,
            "n_scores": int(len(scores)),
            "n_pos": int(sum(labels)),
            "n_neg": int(len(labels) - sum(labels)),
            "warning_lead_time_blocks_mean": float(np.mean(lead_times)) if lead_times else None,
            "warning_lead_time_blocks_min": int(np.min(lead_times)) if lead_times else None,
            "warning_lead_time_blocks_max": int(np.max(lead_times)) if lead_times else None,
            "n_seeds_with_lead_time": int(len(lead_times)),
        }

    return agg


# =============================================================================
# Paired bootstrap CI (fixes "no paired uncertainty" concern)
# =============================================================================

def paired_bootstrap_ci(deltas: list[float], *, n_boot: int = 10000, alpha: float = 0.05) -> dict[str, float]:
    """Paired bootstrap CI on the mean of `deltas`.

    Each bootstrap resample draws `len(deltas)` indices with replacement,
    computes the resampled mean. Returns mean, lower, upper (95% CI).
    """
    if not deltas:
        return {"mean": float("nan"), "lower": float("nan"), "upper": float("nan"), "n": 0}
    arr = np.asarray(deltas, dtype=float)
    n = len(arr)
    rng = np.random.default_rng(20260721)
    boot_means = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, n, size=n)
        boot_means[b] = float(np.mean(arr[idx]))
    lower = float(np.percentile(boot_means, 100 * (alpha / 2)))
    upper = float(np.percentile(boot_means, 100 * (1 - alpha / 2)))
    return {"mean": float(arr.mean()), "lower": lower, "upper": upper, "n": int(n)}


def paired_delta_per_seed(cell_record, method_a, method_b):
    """Per-seed Δ PI-SER = method_a - method_b (negative = a better)."""
    deltas = []
    for s in cell_record["per_seed"]:
        ma = s["methods"].get(method_a, {})
        mb = s["methods"].get(method_b, {})
        if ma.get("diverged") or mb.get("diverged"):
            continue
        pa = ma.get("nearest_pi_ser")
        pb = mb.get("nearest_pi_ser")
        if pa is None or pb is None or np.isnan(pa) or np.isnan(pb):
            continue
        deltas.append(float(pa - pb))
    return deltas


# =============================================================================
# Adjudication
# =============================================================================

def adjudicate(results):
    """Apply B01-R decision rule (achievable denominator = 7 held-out cells)."""
    held_cells = [c for c in results["cells"] if c["is_held_out_cell"]]

    method_closes = {m: 0 for m in ("fixed_mu_cma", "C08", "C10", "C11")}
    method_per_cell = {m: {} for m in ("fixed_mu_cma", "C08", "C10", "C11")}

    for c in held_cells:
        agg = c["aggregate"]
        # "Closes a cell" = headroom < MDE
        for m in ("fixed_mu_cma", "C08", "C10", "C11"):
            headroom = agg[m]["headroom_mean"]
            method_per_cell[m][c["cell_id"]] = float(headroom)
            if not np.isnan(headroom) and headroom < MDE:
                method_closes[m] += 1

    n_held = len(held_cells)
    # CLOSE_THRESHOLD = 5 of 7 (achievable). Any method that closes ≥ 5/7 → CLOSED.
    any_close = any(cnt >= CLOSE_THRESHOLD for cnt in method_closes.values())

    # Detector readiness: ≥2 two-class test cells (held-out) for either detector score.
    # Two-class = both n_pos > 0 and n_neg > 0.
    det_two_class_counts = {"min_z2_ratio": 0, "c05_alert_earliness": 0}
    for c in held_cells:
        for k in det_two_class_counts:
            d = c["aggregate"].get(f"detector_{k}", {})
            if d.get("n_pos", 0) > 0 and d.get("n_neg", 0) > 0:
                det_two_class_counts[k] += 1
    detector_target_ready = all(v >= 2 for v in det_two_class_counts.values())

    if any_close:
        verdict = "C_B01R_PROBLEM_CLOSED_BY_FAIR_CONVENTIONAL_BASELINE"
    elif detector_target_ready:
        verdict = "A_B01R_FAIRNESS_SURVIVES_AND_DETECTOR_TARGET_READY"
    else:
        verdict = "B_B01R_FAIRNESS_SURVIVES_BUT_DETECTOR_TARGET_NOT_READY"

    return {
        "verdict": verdict,
        "method_closes_held_out_of_7": method_closes,
        "method_per_cell_headroom": method_per_cell,
        "n_held_out_cells": n_held,
        "close_threshold": CLOSE_THRESHOLD,
        "detector_two_class_held_out_counts": det_two_class_counts,
        "detector_target_ready": detector_target_ready,
    }


# =============================================================================
# Main
# =============================================================================

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tune-and-eval", action="store_true")
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()

    out_path = BATCH_DIR / "artifacts" / "fairness-batch-b01r-v1.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    global ATLAS_V1_16QAM_CELLS, TEST_SEEDS, TUNING_SEEDS
    if args.smoke:
        ATLAS_V1_16QAM_CELLS = [c for c in ATLAS_V1_16QAM_CELLS if c["id"] in
                                {"16qam-snr20-nominal-short", "16qam-snr25-nominal-short",
                                 "16qam-snr20-nominal-long", "16qam-snr10-fg100-long"}]
        TEST_SEEDS = [21, 22]
        TUNING_SEEDS = [11]

    log = lambda msg: print(msg, flush=True)

    log("[B01-R] Phase 1: tuning on validation cells × tuning seeds (disjoint from test)")
    validation_cells = [c for c in ATLAS_V1_16QAM_CELLS if c["id"] in VALIDATION_CELL_IDS]
    log(f"  validation cells ({len(validation_cells)}): {[c['id'] for c in validation_cells]}")
    log(f"  tuning_seeds={TUNING_SEEDS}  test_seeds={TEST_SEEDS}  (disjoint asserted)")

    frozen_params = {}
    for method in ("fixed_mu_cma", "C08", "C10", "C11", "C05"):
        t_tune = time.time()
        res = tune_method(method, validation_cells, TUNING_SEEDS, log=log)
        frozen_params[method] = {"best_combo": res["best_combo"], "best_score": res["best_score"]}
        log(f"  [tune] {method} took {time.time() - t_tune:.1f}s")

    params_out = BATCH_DIR / "artifacts" / "frozen-params-b01r-v1.yaml"
    with open(params_out, "w") as f:
        yaml.safe_dump({"frozen_params": frozen_params}, f, sort_keys=False)
    log(f"[B01-R] frozen params: {params_out}")

    log("[B01-R] Phase 2: held-out evaluation on 11 cells × 10 test seeds (NEW, disjoint)")
    results = evaluate_held_out(frozen_params, log=log)

    log("[B01-R] Phase 3: paired bootstrap CI on held-out cells")
    paired_cis = {}
    for c in results["cells"]:
        if not c["is_held_out_cell"]:
            continue
        cell_ci = {}
        for m in ("fixed_mu_cma", "C08", "C10", "C11"):
            deltas = paired_delta_per_seed(c, m, "anchor")
            cell_ci[m] = paired_bootstrap_ci(deltas)
        paired_cis[c["cell_id"]] = cell_ci
    results["paired_cis_held_out"] = paired_cis

    log("[B01-R] Phase 4: adjudication (denominator = 7 held-out cells)")
    adjudication = adjudicate(results)
    results["adjudication"] = adjudication
    log(f"[B01-R] VERDICT: {adjudication['verdict']}")
    log(f"  method_closes_held_out_of_7: {adjudication['method_closes_held_out_of_7']}")
    log(f"  detector_two_class_held_out: {adjudication['detector_two_class_held_out_counts']}")

    results["frozen_params"] = frozen_params
    results["metadata"] = {
        "schema": "direction-lab.cb1.fairness-batch-b01r.v1",
        "campaign_id": "science-scout-2026-07-20.dual-pol-osl",
        "MDE": MDE,
        "tuning_seeds": TUNING_SEEDS,
        "test_seeds": TEST_SEEDS,
        "validation_cells": sorted(VALIDATION_CELL_IDS),
        "held_out_cells": sorted(HELD_OUT_CELL_IDS),
        "leakage_check": "set(tuning_seeds) ∩ set(test_seeds) = ∅ (asserted)",
        "R2_qam16": R2_16QAM,
        "elapsed_seconds": time.time() - t0,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "close_threshold": CLOSE_THRESHOLD,
    }

    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    log(f"[B01-R] DONE in {time.time() - t0:.1f}s — {out_path}")


if __name__ == "__main__":
    main()
