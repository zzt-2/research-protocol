"""Fairness Batch B01 driver — runs the frozen contract.

Single entry point:
    python run_fairness_batch_b01.py --tune-and-eval
        (1) tune C05/C08/C10/C11 on validation_cells × 5 seeds,
        (2) freeze per-method hyperparameters,
        (3) evaluate on 11 atlas_v1 cells × 10 paired seeds,
        (4) emit artifacts/fairness-batch-b01-v1.json + synthesis MD.

    python run_fairness_batch_b01.py --smoke    # tiny subset for debugging
    python run_fairness_batch_b01.py --eval-only --params <yaml>
        (skip tuning; use pre-frozen params)

Per batch-contract.v1.yaml:
  - tuning_protocol: 3 validation cells, 5 seeds each, 5 hyperparameter
    candidates per method. Freeze before held-out eval.
  - tuning_protocol fairness: per-METHOD budget (not identical hyperparams).
  - held_out evaluation: 11 atlas cells (incl. validation for completeness),
    10 paired seeds, shared channel realisations.
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
ATLAS_DIR = CB1_ROOT / "baseline-atlas"
ADJUD_DIR = CB1_ROOT / "baseline-adjudication-batch"
REPO_ROOT = HERE.parents[6]
SIM_DIR = REPO_ROOT / "projects" / "simulation"
for p in (str(SIM_DIR), str(BATCH_DIR), str(str(ATLAS_DIR)), str(ADJUD_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402
import cb1_evaluator as evaluator  # noqa: E402
import cb1_cell_runner as atlas_runner  # noqa: E402
import b01_candidates as cand  # noqa: E402


# =============================================================================
# Contract constants (frozen; mirror batch-contract.v1.yaml)
# =============================================================================

FROZEN = {
    "alpha": 4.2, "beta": 1.4, "block": 100, "t_s": 4e-10, "method": "gar",
    "cma_mu": 0.001, "cma_taps": 11, "cma_block_size": 64,
    "r2_qam16": 1.32, "affine_ridge": 1e-6,
}
MDE = 0.005
R2_16QAM = 1.32

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

# Validation cells include 1 long cell so tuning sees convergence-length
# stability (D007 fairness debt #2: N=32768 / long-N convergence). This is
# a deliberate departure from a pure short-cell validation subset: without a
# long cell, methods that diverge at long N (per-symbol CMA with large mu,
# DD-LMS with large step) would be unfairly selected.
VALIDATION_CELL_IDS = {
    "16qam-snr20-nominal-short",   # short, nominal SOP, moderate f_g
    "16qam-snr20-fg1000-short",    # short, high f_g (fast fading)
    "16qam-snr20-sop40e-short",    # short, high SOP rate
    "16qam-snr20-nominal-long",    # LONG: convergence-length stability probe
}
TUNING_SEEDS = [11, 12, 13, 14, 15]
PAIRED_SEEDS = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

# Tuning grids per method (per batch-contract.v1.yaml).
# Reconciled with frozen contract: C05 thresholds [0.2, 0.3, 0.4, 0.5, 0.6],
# C05 cusum_drift [0.01, 0.05, 0.1], C10 mu [1e-5, 1e-4, 3e-4, 1e-3, 3e-3],
# C11 dd_step_size [1e-4, 3e-4, 1e-3, 3e-3, 1e-2].
TUNE_GRID = {
    "C05": {  # detector: maximise AUROC on validation
        "z2_ratio_threshold": [0.2, 0.3, 0.4, 0.5, 0.6],
        "cusum_drift": [0.01, 0.05, 0.1],
        # fixed cusum_threshold=3.0
    },
    "C08": {  # bandit: minimise PI-SER on validation
        "alpha": [0.1, 1.0, 10.0],
        # mu_candidates fixed = (1e-4, 3e-4, 1e-3, 3e-3, 1e-2)
    },
    "C10": {  # per-symbol CMA: minimise PI-SER on validation
        # Per-symbol updates need smaller mu than block-end (block-end averages
        # 64 gradients). Mu too large => divergence; mu grid covers stable range.
        "mu": [1e-5, 1e-4, 3e-4, 1e-3, 3e-3],
    },
    "C11": {  # CMA + DD-LMS: minimise PI-SER on validation
        "dd_step_size": [1e-4, 3e-4, 1e-3, 3e-3, 1e-2],
        # dd_iterations=1 fixed
    },
}


# =============================================================================
# Realisation cache (deterministic per cell+seed)
# =============================================================================

def make_realization(cell, seed):
    gamma_bar = float(10.0 ** (float(cell["snr_db"]) / 10.0))
    return generate_shared_realization_dp(
        int(cell["n_symbols"]), float(FROZEN["alpha"]), float(FROZEN["beta"]),
        float(cell["f_g_hz"]), sop_rate=float(cell["sop_rate"]), seed=int(seed),
        gamma_bar=gamma_bar, block=int(FROZEN["block"]), t_s=float(FROZEN["t_s"]),
        method=str(FROZEN["method"]), modulation=str(cell.get("modulation", "qam16")),
    )


def slice_eval_window(realization, algo_output, *, eval_start, calibration_end, eval_end):
    """Slice the algo output and realization truth to the eval window."""
    zX = np.asarray(algo_output["zX"])
    zY = np.asarray(algo_output["zY"])
    z_calib = np.column_stack((zX[eval_start:calibration_end], zY[eval_start:calibration_end]))
    z_eval = np.column_stack((zX[calibration_end:eval_end], zY[calibration_end:eval_end]))
    truth_calib = np.column_stack((
        realization["sX"][eval_start:calibration_end],
        realization["sY"][eval_start:calibration_end],
    ))
    truth_eval = np.column_stack((
        realization["sX"][calibration_end:eval_end],
        realization["sY"][calibration_end:eval_end],
    ))
    bits_per_sym = 4
    bits_x_calib = realization["bitsX"][eval_start * bits_per_sym:calibration_end * bits_per_sym]
    bits_y_calib = realization["bitsY"][eval_start * bits_per_sym:calibration_end * bits_per_sym]
    bits_x_eval = realization["bitsX"][calibration_end * bits_per_sym:eval_end * bits_per_sym]
    bits_y_eval = realization["bitsY"][calibration_end * bits_per_sym:eval_end * bits_per_sym]
    return z_calib, z_eval, truth_calib, truth_eval, bits_x_calib, bits_y_calib, bits_x_eval, bits_y_eval


def pi_ser_from_z(zX, zY, realization, *, eval_start, calibration_end, eval_end):
    """Compute nearest-PI-SER and oracle-PI-SER for a z-stream."""
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
        "nearest_fixed_ser": float(nearest_m.get("fixed_label_ser", float("nan"))),
        "oracle_fixed_ser": float(oracle_m.get("fixed_label_ser", float("nan"))),
    }


# =============================================================================
# Per-candidate execution
# =============================================================================

def run_anchor(cell, realization):
    """CMA anchor (block_size=64, mu=0.001) — the Atlas v1 identity."""
    return atlas_runner.standard_cma_godard_with_z(
        realization["rX"], realization["rY"],
        n_tap=int(FROZEN["cma_taps"]), mu=float(FROZEN["cma_mu"]),
        R2=R2_16QAM, block_size=int(FROZEN["cma_block_size"]),
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
        n_tap=int(FROZEN["cma_taps"]), cma_mu=float(FROZEN["cma_mu"]),
        cma_R2=R2_16QAM, cma_block_size=int(FROZEN["cma_block_size"]),
        dd_step_size=float(dd_step_size), dd_iterations=1,
        hard_decision_fn=evaluator.hard_16qam,
    )


def run_c05_on_trace(trace, *, z2_ratio_threshold, cusum_drift):
    return cand.c05_threshold_detector(
        trace, z2_ratio_threshold=float(z2_ratio_threshold),
        cusum_drift=float(cusum_drift), cusum_threshold=3.0,
        R2=R2_16QAM,
    )


# =============================================================================
# Tuning (validation cells only)
# =============================================================================

def _eval_window_for_cell(cell):
    return atlas_runner.eval_window_for(
        int(cell["n_symbols"]), int(FROZEN["cma_taps"]),
        window_symbols=256, block_size=int(FROZEN["cma_block_size"]),
    )


def tune_method(method, cells, seeds, log=print):
    """Grid-search the method's hyperparameters on validation cells.

    Returns the best hyperparameter dict by the method's tuning metric.
    Grids come from TUNE_GRID. For each combo, run all validation cells ×
    tuning seeds, compute the mean metric, pick the best.
    """
    log(f"  [tune] {method}: scanning grid...")
    grid_keys = list(TUNE_GRID[method].keys())
    grid_values = [TUNE_GRID[method][k] for k in grid_keys]

    # Enumerate combos.
    combos = [{}]
    for k, vals in zip(grid_keys, grid_values):
        new_combos = []
        for c in combos:
            for v in vals:
                new_combos.append({**c, k: v})
        combos = new_combos

    best_combo = None
    best_score = None  # higher = better (we negate PI-SER, use AUROC directly)
    for combo in combos:
        try:
            score = _eval_combo(method, combo, cells, seeds)
        except Exception as exc:  # noqa: BLE001
            log(f"    combo {combo}: FAILED ({exc})")
            continue
        if best_score is None or score > best_score:
            best_score = score
            best_combo = combo
    log(f"  [tune] {method}: best combo = {best_combo} score={best_score:.4f}")
    return {"method": method, "best_combo": best_combo, "best_score": float(best_score)}


def _eval_combo(method, combo, cells, seeds):
    """Return the tuning metric (higher=better) for one combo across cells/seeds.

    C05: mean AUROC of collapse detection (label from oracle PI-SER > 0.3).
    C08/C10/C11: negative mean PI-SER (so higher = less error), with a
    divergence penalty so unstable hyperparameters are dispreferred.
    """
    if method == "C05":
        return _eval_combo_c05(combo, cells, seeds)
    # C08/C10/C11: gather per-seed PI-SER on nearest decision.
    pis = []
    n_div = 0
    n_total = 0
    for cell in cells:
        for seed in seeds:
            n_total += 1
            realization = make_realization(cell, seed)
            if method == "C08":
                out = run_c08(cell, realization, alpha=combo["alpha"])
            elif method == "C10":
                out = run_c10(cell, realization, mu=combo["mu"])
            elif method == "C11":
                out = run_c11(cell, realization, dd_step_size=combo["dd_step_size"])
            else:
                raise ValueError(method)
            if out.get("diverged", False):
                pis.append(1.0)  # diverged = worst PI-SER
                n_div += 1
                continue
            es, ce, ee, _ = _eval_window_for_cell(cell)
            m = pi_ser_from_z(out["zX"], out["zY"], realization,
                              eval_start=es, calibration_end=ce, eval_end=ee)
            pis.append(m["nearest_pi_ser"])
    if not pis:
        return -1.0
    mean_pi = float(np.mean(pis))
    # Divergence penalty: a hyperparameter that diverges on any validation
    # seed is strictly worse than one that doesn't, even if mean PI-SER is
    # similar. Penalty = 0.1 * divergence_rate (so 100% divergence ≈ +0.1 PI-SER).
    div_rate = n_div / max(n_total, 1)
    return -(mean_pi + 0.1 * div_rate)


def _eval_combo_c05(combo, cells, seeds):
    """Compute AUROC of C05 detector across validation cells × tuning seeds.

    For each (cell, seed), we run the CMA anchor (block_size=64), emit its
    trace, run C05 detector with `combo`, and label the seed from oracle
    PI-SER > 0.3. Aggregate scores+labels across all (cell, seed) and compute
    AUROC.
    """
    scores: list[float] = []
    labels: list[int] = []
    for cell in cells:
        for seed in seeds:
            realization = make_realization(cell, seed)
            anchor_out = run_anchor(cell, realization)
            es, ce, ee, _ = _eval_window_for_cell(cell)
            # Oracle PI-SER for label.
            m_oracle = pi_ser_from_z(anchor_out["zX"], anchor_out["zY"], realization,
                                     eval_start=es, calibration_end=ce, eval_end=ee)
            label = cand.c05_label_from_oracle(m_oracle["oracle_pi_ser"])
            # C05 detector: take max alert over the trace (1 if ANY block alert).
            det = run_c05_on_trace(
                anchor_out["trace"],
                z2_ratio_threshold=combo["z2_ratio_threshold"],
                cusum_drift=combo["cusum_drift"],
            )
            # Score = -min(z2_ratio) over non-warmup blocks (lower ratio = more collapse-like = higher score).
            ratios = [a["z2_ratio"] for a in det["alerts"] if not np.isnan(a["z2_ratio"])]
            if not ratios:
                continue
            score = -float(np.min(ratios))
            scores.append(score)
            labels.append(label)
    return _auroc(scores, labels)


def _auroc(scores, labels):
    """Compute AUROC via the rank-based formula (Mann-Whitney U / (n_pos*n_neg))."""
    scores = np.asarray(scores, dtype=float)
    labels = np.asarray(labels, dtype=int)
    n_pos = int(np.sum(labels == 1))
    n_neg = int(np.sum(labels == 0))
    if n_pos == 0 or n_neg == 0:
        return 0.5  # undefined; neutral
    order = np.argsort(scores)
    ranks = np.empty_like(order, dtype=float)
    ranks[order] = np.arange(1, len(scores) + 1)
    # Handle ties via average ranks.
    sorted_scores = scores[order]
    i = 0
    while i < len(sorted_scores):
        j = i
        while j + 1 < len(sorted_scores) and sorted_scores[j + 1] == sorted_scores[i]:
            j += 1
        if j > i:
            avg_rank = (i + 1 + j + 1) / 2.0
            ranks[order[i:j + 1]] = avg_rank
        i = j + 1
    sum_pos = float(np.sum(ranks[labels == 1]))
    u = sum_pos - n_pos * (n_pos + 1) / 2.0
    return u / (n_pos * n_neg)


# =============================================================================
# Held-out evaluation
# =============================================================================

def evaluate_held_out(frozen_params, log=print):
    """Evaluate all methods on all 11 cells × 10 paired seeds with frozen params."""
    results: dict[str, Any] = {"cells": []}
    for cell in ATLAS_V1_16QAM_CELLS:
        t_cell_start = time.time()
        cell_record = {
            "cell_id": cell["id"],
            "is_validation_cell": cell["id"] in VALIDATION_CELL_IDS,
            "axes": {"snr_db": cell["snr_db"], "f_g_hz": cell["f_g_hz"],
                     "sop_rate": cell["sop_rate"], "n_symbols": cell["n_symbols"]},
            "per_seed": [],
        }
        es, ce, ee, _ = _eval_window_for_cell(cell)
        cell_record["eval_window"] = {"eval_start": es, "calibration_end": ce, "eval_end": ee}

        for seed in PAIRED_SEEDS:
            realization = make_realization(cell, seed)
            seed_record = {"seed": int(seed), "methods": {}}

            # CMA anchor (diagnostic, paired delta reference).
            anchor_out = run_anchor(cell, realization)
            if anchor_out["diverged"]:
                seed_record["methods"]["anchor"] = {"diverged": True}
                anchor_m = {"nearest_pi_ser": float("nan"), "oracle_pi_ser": float("nan"),
                            "nearest_fixed_ser": float("nan"), "oracle_fixed_ser": float("nan")}
            else:
                anchor_m = pi_ser_from_z(anchor_out["zX"], anchor_out["zY"], realization,
                                         eval_start=es, calibration_end=ce, eval_end=ee)
                seed_record["methods"]["anchor"] = {
                    "diverged": False,
                    **anchor_m,
                    "trace_summary": _summarize_trace(anchor_out["trace"]),
                    "_trace_for_c05": anchor_out["trace"],  # kept for C05 detector eval
                }

            # C05 detector on the anchor trace.
            c05_params = frozen_params["C05"]["best_combo"]
            det = run_c05_on_trace(
                anchor_out["trace"],
                z2_ratio_threshold=c05_params["z2_ratio_threshold"],
                cusum_drift=c05_params["cusum_drift"],
            )
            seed_record["methods"]["C05"] = {
                "alert_any": int(any(a["alert"] == 1 for a in det["alerts"])),
                "alert_first_block": next((a["block"] for a in det["alerts"] if a["alert"] == 1), None),
                "n_alerts": int(sum(a["alert"] for a in det["alerts"])),
                "label": int(cand.c05_label_from_oracle(anchor_m["oracle_pi_ser"])),
                "oracle_pi_ser_for_label": float(anchor_m["oracle_pi_ser"]),
                "baseline_ratio": float(det.get("baseline", float("nan"))),
                "detector_score": float(-np.nanmin([a["z2_ratio"] for a in det["alerts"]])
                                        if any(not np.isnan(a["z2_ratio"]) for a in det["alerts"]) else float("nan")),
            }

            # C08 bandit.
            c08_params = frozen_params["C08"]["best_combo"]
            c08_out = run_c08(cell, realization, alpha=c08_params["alpha"])
            if c08_out["diverged"]:
                seed_record["methods"]["C08"] = {"diverged": True, "alpha": c08_params["alpha"]}
            else:
                c08_m = pi_ser_from_z(c08_out["zX"], c08_out["zY"], realization,
                                      eval_start=es, calibration_end=ce, eval_end=ee)
                seed_record["methods"]["C08"] = {
                    "diverged": False, "alpha": c08_params["alpha"],
                    "arm_history": c08_out["arm_history"],
                    **c08_m,
                }

            # C10 per-symbol CMA.
            c10_params = frozen_params["C10"]["best_combo"]
            c10_out = run_c10(cell, realization, mu=c10_params["mu"])
            if c10_out["diverged"]:
                seed_record["methods"]["C10"] = {"diverged": True, "mu": c10_params["mu"]}
            else:
                c10_m = pi_ser_from_z(c10_out["zX"], c10_out["zY"], realization,
                                      eval_start=es, calibration_end=ce, eval_end=ee)
                seed_record["methods"]["C10"] = {"diverged": False, "mu": c10_params["mu"], **c10_m}

            # C11 CMA + DD-LMS cascade.
            c11_params = frozen_params["C11"]["best_combo"]
            c11_out = run_c11(cell, realization, dd_step_size=c11_params["dd_step_size"])
            if c11_out["diverged"]:
                seed_record["methods"]["C11"] = {"diverged": True, "dd_step_size": c11_params["dd_step_size"]}
            else:
                c11_m = pi_ser_from_z(c11_out["zX"], c11_out["zY"], realization,
                                      eval_start=es, calibration_end=ce, eval_end=ee)
                seed_record["methods"]["C11"] = {
                    "diverged": False, "dd_step_size": c11_params["dd_step_size"],
                    "stage_2_diverged": c11_out.get("stage_2", {}).get("diverged", False),
                    **c11_m,
                }

            cell_record["per_seed"].append(seed_record)

        # Aggregate cell-level means.
        cell_record["aggregate"] = _aggregate_cell(cell_record["per_seed"])
        elapsed = time.time() - t_cell_start
        log(f"  cell {cell['id']}: {elapsed:.1f}s — "
            f"anchor PI-SER={cell_record['aggregate']['anchor']['nearest_pi_ser_mean']:.4f}, "
            f"C08={cell_record['aggregate']['C08']['nearest_pi_ser_mean']:.4f}, "
            f"C10={cell_record['aggregate']['C10']['nearest_pi_ser_mean']:.4f}, "
            f"C11={cell_record['aggregate']['C11']['nearest_pi_ser_mean']:.4f}")
        results["cells"].append(cell_record)
    return results


def _summarize_trace(trace):
    """Compact trace summary (avoid storing full trace in JSON)."""
    if not trace:
        return {}
    ratios = [t.get("z2_over_R2_ratio", float("nan")) for t in trace if "z2_over_R2_ratio" in t]
    ratios = [r for r in ratios if not np.isnan(r)] if ratios else []
    return {
        "n_blocks": len(trace),
        "z2_ratio_min": float(np.min(ratios)) if ratios else float("nan"),
        "z2_ratio_max": float(np.max(ratios)) if ratios else float("nan"),
        "z2_ratio_final": float(ratios[-1]) if ratios else float("nan"),
    }


def _aggregate_cell(per_seed):
    """Mean PI-SER per method across non-diverged seeds."""
    agg: dict[str, Any] = {}
    for method in ("anchor", "C05", "C08", "C10", "C11"):
        if method == "C05":
            # Detector: AUROC over seeds in this cell.
            scores = [s["methods"]["C05"]["detector_score"] for s in per_seed
                      if "C05" in s["methods"] and not np.isnan(s["methods"]["C05"].get("detector_score", float("nan")))]
            labels = [s["methods"]["C05"]["label"] for s in per_seed
                      if "C05" in s["methods"]]
            n_alert = sum(s["methods"]["C05"]["alert_any"] for s in per_seed if "C05" in s["methods"])
            n_label = sum(labels)
            agg["C05"] = {
                "auroc_in_cell": float(_auroc(scores, labels)) if scores else float("nan"),
                "alert_rate": float(np.mean([s["methods"]["C05"]["alert_any"] for s in per_seed if "C05" in s["methods"]])),
                "collapse_label_rate": float(np.mean(labels)) if labels else float("nan"),
                "n_seeds_with_label_1": int(n_label),
                "n_seeds_with_alert": int(n_alert),
            }
            continue
        # PI-SER-based methods.
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
    return agg


# =============================================================================
# Main
# =============================================================================

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tune-and-eval", action="store_true",
                    help="Run tuning on validation cells then evaluate on all cells.")
    ap.add_argument("--eval-only", action="store_true",
                    help="Skip tuning; load frozen params from --params.")
    ap.add_argument("--params", type=str, default=None,
                    help="YAML file with frozen params (for --eval-only).")
    ap.add_argument("--smoke", action="store_true",
                    help="Tiny subset for debugging (3 cells x 2 seeds).")
    args = ap.parse_args()

    out_path = BATCH_DIR / "artifacts" / "fairness-batch-b01-v1.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    if args.smoke:
        global ATLAS_V1_16QAM_CELLS, PAIRED_SEEDS, TUNING_SEEDS
        ATLAS_V1_16QAM_CELLS = [c for c in ATLAS_V1_16QAM_CELLS if c["id"] in
                                {"16qam-snr20-nominal-short", "16qam-snr25-nominal-short", "16qam-snr20-nominal-long"}]
        PAIRED_SEEDS = [11, 12]
        TUNING_SEEDS = [11]

    log = lambda msg: print(msg, flush=True)

    if args.eval_only:
        if not args.params:
            print("--eval-only requires --params", file=sys.stderr)
            sys.exit(2)
        with open(args.params) as f:
            frozen_params = yaml.safe_load(f)["frozen_params"]
        log(f"[B01] eval-only with frozen params: {frozen_params}")
    elif args.tune_and_eval or True:  # default = tune-and-eval
        log("[B01] Phase 1: tuning on validation cells")
        validation_cells = [c for c in ATLAS_V1_16QAM_CELLS if c["id"] in VALIDATION_CELL_IDS]
        log(f"  validation cells ({len(validation_cells)}): {[c['id'] for c in validation_cells]}")
        frozen_params = {}
        for method in ("C05", "C08", "C10", "C11"):
            t_tune = time.time()
            res = tune_method(method, validation_cells, TUNING_SEEDS, log=log)
            frozen_params[method] = {"best_combo": res["best_combo"], "best_score": res["best_score"]}
            log(f"  [tune] {method} took {time.time() - t_tune:.1f}s")
        # Persist frozen params for audit.
        params_out = BATCH_DIR / "artifacts" / "frozen-params.v1.yaml"
        with open(params_out, "w") as f:
            yaml.safe_dump({"frozen_params": frozen_params}, f, sort_keys=False)
        log(f"[B01] frozen params written to {params_out}")

        log("[B01] Phase 2: held-out evaluation on all 11 cells x 10 seeds")
        results = evaluate_held_out(frozen_params, log=log)
    else:
        print("specify --tune-and-eval or --eval-only", file=sys.stderr)
        sys.exit(2)

    results["frozen_params"] = frozen_params
    results["metadata"] = {
        "schema": "direction-lab.cb1.fairness-batch-b01.v1",
        "campaign_id": "science-scout-2026-07-20.dual-pol-osl",
        "MDE": MDE,
        "paired_seeds": PAIRED_SEEDS,
        "tuning_seeds": TUNING_SEEDS,
        "validation_cells": sorted(VALIDATION_CELL_IDS),
        "R2_qam16": R2_16QAM,
        "elapsed_seconds": time.time() - t0,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    log(f"[B01] DONE in {time.time() - t0:.1f}s — artifacts: {out_path}")


if __name__ == "__main__":
    main()
