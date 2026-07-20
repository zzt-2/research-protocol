"""CB1 Baseline Adjudication Shared Batch — driver.

Single entry point: runs the two adjudication axes from
``batch-contract.v1.yaml``:

  Axis 1 — atlas_v1_cells_with_mma:
      Re-run the 11 Atlas-v1 16QAM cells with both standard-CMA (anchor)
      and MMA (main Go comparator), 10 paired seeds each.
  Axis 2 — convergence_length_adjudication:
      Re-run a 4-cell x {N=512, N=32768} probe with both comparators,
      5 paired seeds each, to decompose task-mismatch from under-convergence.

Usage:
    python run_baseline_adjudication.py --axis1            # 11 cells x 2 algos x 10 seeds
    python run_baseline_adjudication.py --axis2            # 4 cells x 2 lengths x 2 algos x 5 seeds
    python run_baseline_adjudication.py --axis1 --axis2    # both
    python run_baseline_adjudication.py --smoke            # tiny subset (debugging)

Outputs:
    artifacts/baseline-adjudication-v1.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve()
BATCH_DIR = HERE.parent                      # baseline-adjudication-batch/
CB1_ROOT = BATCH_DIR.parent                  # cb1-modulation-generic-closure/
ATLAS_DIR = CB1_ROOT / "baseline-atlas"      # cb1_cell_runner / cb1_evaluator
REPO_ROOT = HERE.parents[6]
SIM_DIR = REPO_ROOT / "projects" / "simulation"

for p in (str(SIM_DIR), str(BATCH_DIR), str(ATLAS_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402
import cb1_evaluator as evaluator  # noqa: E402
import cb1_cell_runner as atlas_runner  # noqa: E402 — for eval_window_for
from cb1_cell_runner import eval_window_for  # noqa: E402
from mma_comparator import mma_yang_werner_dumont, mma_dispersion_constants_sq_qam16  # noqa: E402


# ─── Contract (frozen; mirrors batch-contract.v1.yaml) ───────────────────────

FROZEN_AXES = {
    "alpha": 4.2, "beta": 1.4, "block": 100, "t_s": 4e-10, "method": "gar",
    "cma_mu": 0.001, "cma_taps": 11, "cma_block_size": 64,
    "r2_qpsk": 1.0, "r2_qam16": 1.32,  # CMA R^2
    "affine_ridge": 1e-6,
}
MDE = 0.005

ATLAS_V1_16QAM_CELLS = [
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

# Convergence-length probe: 4 cells x {short=512, long=32768}.
# Picks cells where Atlas v1 reported ADVANCE (large headroom) so that
# length effects are visible if they exist. snr=25 nominal + snr=20 fg=1000 +
# snr=20 sop=40e + snr=15 nominal (covers high-SNR collapse regime).
CONVERGENCE_PROBE_CELLS = [
    {"id": "16qam-snr25-nominal", "snr_db": 25.0, "f_g_hz": 30.0,  "sop_rate": 4e-6},
    {"id": "16qam-snr20-fg1000",  "snr_db": 20.0, "f_g_hz": 1000.0,"sop_rate": 4e-6},
    {"id": "16qam-snr20-sop40e",  "snr_db": 20.0, "f_g_hz": 30.0,  "sop_rate": 4e-5},
    {"id": "16qam-snr15-nominal", "snr_db": 15.0, "f_g_hz": 30.0,  "sop_rate": 4e-6},
]
CONVERGENCE_LENGTHS = [512, 32768]

QPSK_ANCHOR_CELL = {
    "id": "qpsk-snr20-nominal-short-P03v1-anchor", "modulation": "qpsk",
    "snr_db": 20.0, "f_g_hz": 30.0, "sop_rate": 4e-6, "n_symbols": 512,
}


# ─── Per-seed comparator evaluation ──────────────────────────────────────────

def _evaluate_16qam_block(
    raw: dict[str, Any],
    realization: dict[str, Any],
    eval_start: int,
    calibration_end: int,
    eval_end: int,
    *,
    ridge: float,
) -> dict[str, Any]:
    """Slice the eval window and run the same 3-probe evaluation as Atlas v1.

    Returns nearest / blind / oracle metrics on this comparator's output.
    """
    zX = np.asarray(raw["zX"])
    zY = np.asarray(raw["zY"])
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
    bits_x_eval = realization["bitsX"][calibration_end * 4:eval_end * 4]
    bits_y_eval = realization["bitsY"][calibration_end * 4:eval_end * 4]

    nearest_predicted = evaluator.hard_16qam(z_eval)
    blind = evaluator.blind_affine_compare_16qam(z_calib, z_eval, ridge=ridge)
    oracle_corrected = evaluator.oracle_affine_bound_16qam(
        z_calib, z_eval, truth_calib, ridge=ridge,
    )
    nearest_m = evaluator.evaluate_dual_16qam(
        nearest_predicted[:, 0], nearest_predicted[:, 1],
        truth_eval[:, 0], truth_eval[:, 1], bits_x_eval, bits_y_eval,
    )
    blind_m = evaluator.evaluate_dual_16qam(
        blind["predicted"][:, 0], blind["predicted"][:, 1],
        truth_eval[:, 0], truth_eval[:, 1], bits_x_eval, bits_y_eval,
    )
    oracle_m = evaluator.evaluate_dual_16qam(
        oracle_corrected[:, 0], oracle_corrected[:, 1],
        truth_eval[:, 0], truth_eval[:, 1], bits_x_eval, bits_y_eval,
    )
    return {"nearest": nearest_m, "blind": blind_m, "oracle": oracle_m}


def run_comparator_per_seed(
    comparator_id: str,
    realization: dict[str, Any],
    *,
    cma_taps: int, mu: float, block_size: int, ridge: float,
    eval_start: int, calibration_end: int, eval_end: int,
) -> dict[str, Any]:
    """Run one comparator (CMA anchor or MMA) on one channel realisation."""
    if comparator_id == "standard_cma_godard_z":
        raw = atlas_runner.standard_cma_godard_with_z(
            realization["rX"], realization["rY"],
            n_tap=cma_taps, mu=mu, R2=1.32, block_size=block_size,
        )
    elif comparator_id == "mma_yang_werner_dumont":
        R_R2, R_I2 = mma_dispersion_constants_sq_qam16()
        raw = mma_yang_werner_dumont(
            realization["rX"], realization["rY"],
            n_tap=cma_taps, mu=mu, R_R2=R_R2, R_I2=R_I2, block_size=block_size,
        )
    else:
        raise ValueError(f"unknown comparator {comparator_id!r}")

    identity_ok = raw["provenance"].get("gradient") in (
        "Godard-with-z", "Yang-Werner-Dumont MMA",
    )
    if not identity_ok or raw["diverged"]:
        return {
            "comparator": comparator_id,
            "identity_gate": "PASS" if identity_ok else "FAILED",
            "diverged": bool(raw["diverged"]),
            "divergence_symbol": int(raw["divergence_symbol"]) if raw["divergence_symbol"] is not None else None,
            "nearest": None, "blind": None, "oracle": None,
        }
    metrics = _evaluate_16qam_block(
        raw, realization, eval_start, calibration_end, eval_end, ridge=ridge,
    )
    return {
        "comparator": comparator_id,
        "identity_gate": "PASS",
        "diverged": False,
        **metrics,
    }


# ─── Cell aggregation ────────────────────────────────────────────────────────

def aggregate_cell(per_seed_rows: list[dict[str, Any]], comparator_id: str) -> dict[str, Any]:
    """Aggregate per-seed metrics for one comparator within one cell.

    Mirrors cb1_cell_runner aggregation: simple mean of per-seed PI-SER.
    per_seed_rows contains BOTH comparators' rows (CMA + MMA per seed);
    n_total_seeds is the count of rows belonging to THIS comparator only.
    """
    comparator_rows = [
        row for row in per_seed_rows
        if row.get("comparator") == comparator_id
    ]
    valid = [
        row for row in comparator_rows
        if row.get("identity_gate") == "PASS"
        and not row.get("diverged", False)
        and row.get("nearest") is not None
    ]
    diverged = [
        row for row in comparator_rows
        if row.get("identity_gate") == "PASS"
        and row.get("diverged", False)
    ]

    def _mean(key, metric="pi_ser"):
        vals = [float(row[key][metric]) for row in valid]
        return float(np.mean(vals)) if vals else float("nan")

    nearest_pi = _mean("nearest")
    blind_pi = _mean("blind")
    oracle_pi = _mean("oracle")
    headroom = (
        float("nan") if any(np.isnan(v) for v in (nearest_pi, oracle_pi))
        else max(nearest_pi - oracle_pi, 0.0)
    )
    simple_gain = (
        float("nan") if any(np.isnan(v) for v in (nearest_pi, blind_pi))
        else max(nearest_pi - min(nearest_pi, blind_pi), 0.0)
    )
    return {
        "comparator": comparator_id,
        "n_valid_seeds": len(valid),
        "n_diverged_seeds": len(diverged),
        "n_total_seeds": len(comparator_rows),
        "nearest_pi_ser": nearest_pi,
        "blind_pi_ser": blind_pi,
        "oracle_pi_ser": oracle_pi,
        "visible_headroom": headroom,
        "simple_gain": simple_gain,
        "meets_mde": (not np.isnan(headroom)) and headroom >= MDE,
    }


def run_axis1_cell(cell: dict[str, Any], seeds: list[int]) -> dict[str, Any]:
    """Axis 1: one Atlas-v1 cell x both comparators x all seeds."""
    n_symbols = int(cell["n_symbols"])
    gamma_bar = float(10.0 ** (float(cell["snr_db"]) / 10.0))
    eval_start, calibration_end, eval_end, _ = eval_window_for(
        n_symbols, int(FROZEN_AXES["cma_taps"]),
        window_symbols=256, block_size=int(FROZEN_AXES["cma_block_size"]),
    )

    per_seed: list[dict[str, Any]] = []
    for seed in seeds:
        realization = generate_shared_realization_dp(
            n_symbols, float(FROZEN_AXES["alpha"]), float(FROZEN_AXES["beta"]),
            float(cell["f_g_hz"]), sop_rate=float(cell["sop_rate"]), seed=int(seed),
            gamma_bar=gamma_bar, block=int(FROZEN_AXES["block"]),
            t_s=float(FROZEN_AXES["t_s"]), method=str(FROZEN_AXES["method"]),
            modulation="qam16",
        )
        for comparator_id in ("standard_cma_godard_z", "mma_yang_werner_dumont"):
            row = run_comparator_per_seed(
                comparator_id, realization,
                cma_taps=int(FROZEN_AXES["cma_taps"]), mu=float(FROZEN_AXES["cma_mu"]),
                block_size=int(FROZEN_AXES["cma_block_size"]), ridge=float(FROZEN_AXES["affine_ridge"]),
                eval_start=eval_start, calibration_end=calibration_end, eval_end=eval_end,
            )
            row["seed"] = int(seed)
            per_seed.append(row)

    return {
        "cell_id": cell["id"],
        "axes": {
            "modulation": "qam16", "snr_db": float(cell["snr_db"]),
            "f_g_hz": float(cell["f_g_hz"]), "sop_rate": float(cell["sop_rate"]),
            "n_symbols": n_symbols,
        },
        "eval_window": {"eval_start": eval_start, "calibration_end": calibration_end, "eval_end": eval_end},
        "per_seed": per_seed,
        "aggregated": {
            "standard_cma_godard_z": aggregate_cell(per_seed, "standard_cma_godard_z"),
            "mma_yang_werner_dumont": aggregate_cell(per_seed, "mma_yang_werner_dumont"),
        },
    }


def run_axis2_cell(cell: dict[str, Any], n_symbols: int, seeds: list[int]) -> dict[str, Any]:
    """Axis 2: one convergence-probe cell at a specific length, both comparators."""
    gamma_bar = float(10.0 ** (float(cell["snr_db"]) / 10.0))
    eval_start, calibration_end, eval_end, _ = eval_window_for(
        n_symbols, int(FROZEN_AXES["cma_taps"]),
        window_symbols=256, block_size=int(FROZEN_AXES["cma_block_size"]),
    )

    per_seed: list[dict[str, Any]] = []
    for seed in seeds:
        realization = generate_shared_realization_dp(
            n_symbols, float(FROZEN_AXES["alpha"]), float(FROZEN_AXES["beta"]),
            float(cell["f_g_hz"]), sop_rate=float(cell["sop_rate"]), seed=int(seed),
            gamma_bar=gamma_bar, block=int(FROZEN_AXES["block"]),
            t_s=float(FROZEN_AXES["t_s"]), method=str(FROZEN_AXES["method"]),
            modulation="qam16",
        )
        for comparator_id in ("standard_cma_godard_z", "mma_yang_werner_dumont"):
            row = run_comparator_per_seed(
                comparator_id, realization,
                cma_taps=int(FROZEN_AXES["cma_taps"]), mu=float(FROZEN_AXES["cma_mu"]),
                block_size=int(FROZEN_AXES["cma_block_size"]), ridge=float(FROZEN_AXES["affine_ridge"]),
                eval_start=eval_start, calibration_end=calibration_end, eval_end=eval_end,
            )
            row["seed"] = int(seed)
            per_seed.append(row)

    return {
        "cell_id": f"{cell['id']}-N{n_symbols}",
        "axes": {
            "modulation": "qam16", "snr_db": float(cell["snr_db"]),
            "f_g_hz": float(cell["f_g_hz"]), "sop_rate": float(cell["sop_rate"]),
            "n_symbols": n_symbols,
        },
        "eval_window": {"eval_start": eval_start, "calibration_end": calibration_end, "eval_end": eval_end},
        "per_seed": per_seed,
        "aggregated": {
            "standard_cma_godard_z": aggregate_cell(per_seed, "standard_cma_godard_z"),
            "mma_yang_werner_dumont": aggregate_cell(per_seed, "mma_yang_werner_dumont"),
        },
    }


# ─── JSON serialization ──────────────────────────────────────────────────────

def _jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    if isinstance(value, np.ndarray):
        return [_jsonable(v) for v in value.tolist()]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        v = float(value)
        return v if not np.isnan(v) else None
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, complex):
        return {"real": value.real, "imag": value.imag}
    if isinstance(value, (str, int, float, bool)) or value is None:
        if isinstance(value, float) and np.isnan(value):
            return None
        return value
    return str(value)


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--axis1", action="store_true", help="Atlas v1 cells x {CMA, MMA} x 10 seeds")
    ap.add_argument("--axis2", action="store_true", help="Convergence probe x {N=512, N=32768} x {CMA, MMA} x 5 seeds")
    ap.add_argument("--smoke", action="store_true", help="Tiny subset for debugging")
    args = ap.parse_args()
    if not (args.axis1 or args.axis2 or args.smoke):
        args.axis1 = True
        args.axis2 = True

    out: dict[str, Any] = {
        "schema_version": "direction-lab.cb1.baseline-adjudication.v1",
        "campaign_id": "science-scout-2026-07-20.dual-pol-osl",
        "contract": "batch-contract.v1.yaml",
        "frozen_axes": FROZEN_AXES,
        "MDE": MDE,
        "comparators": ["standard_cma_godard_z", "mma_yang_werner_dumont"],
        "axes_run": [],
    }

    # ─── QPSK anchor regression (always run first as wiring sanity) ───────────
    print("=" * 78)
    print("QPSK anchor regression (P03 v1 byte-identity; MMA degenerates to CMA)")
    print("=" * 78)
    t0 = time.time()
    realization = generate_shared_realization_dp(
        512, 4.2, 1.4, 30.0, sop_rate=4e-6, seed=11, gamma_bar=100.0,
        block=100, t_s=4e-10, method="gar", modulation="qpsk",
    )
    raw_cma = atlas_runner.standard_cma_godard_with_z(
        realization["rX"], realization["rY"], n_tap=11, mu=1e-3, R2=1.0, block_size=64,
    )
    raw_mma = mma_yang_werner_dumont(
        realization["rX"], realization["rY"], n_tap=11, mu=1e-3,
        R_R2=1.0, R_I2=1.0, block_size=64,  # QPSK: R_R^2 = R_I^2 = 1.0
    )
    eval_start, calibration_end, eval_end, _ = eval_window_for(
        512, 11, window_symbols=256, block_size=64,
    )
    p03 = evaluator._P03
    amp = 1.0 / np.sqrt(2.0)

    def _qpsk_pi(raw):
        z_eval = np.column_stack((
            raw["zX"][calibration_end:eval_end], raw["zY"][calibration_end:eval_end]
        ))
        truth = np.column_stack((
            realization["sX"][calibration_end:eval_end],
            realization["sY"][calibration_end:eval_end],
        ))
        nearest = p03.hard_qpsk(z_eval, amp)
        m = p03.evaluate_dual_qpsk(nearest[:, 0], nearest[:, 1], truth[:, 0], truth[:, 1])
        return m["pi_ser"]

    cma_pi = _qpsk_pi(raw_cma)
    mma_pi = _qpsk_pi(raw_mma)
    dt = time.time() - t0
    print(f"  CMA anchor PI-SER = {cma_pi:.6f} (expected 0.0)")
    print(f"  MMA      PI-SER = {mma_pi:.6f} (expected 0.0; MMA degenerates on QPSK)")
    print(f"  time = {dt:.2f}s")
    out["qpsk_anchor_regression"] = {
        "cma_pi_ser": cma_pi, "mma_pi_ser": mma_pi,
        "expected": 0.0, "pass": (cma_pi == 0.0 and mma_pi == 0.0),
    }

    # ─── Axis 1: Atlas v1 cells with both comparators ─────────────────────────
    if args.axis1 or args.smoke:
        print("\n" + "=" * 78)
        print("Axis 1: Atlas v1 cells x {CMA, MMA} (adjudicates task-mismatch)")
        print("=" * 78)
        cells = ATLAS_V1_16QAM_CELLS
        seeds = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        if args.smoke:
            cells = cells[:3]
            seeds = [11, 12]
        cell_results = []
        t_start = time.time()
        for i, cell in enumerate(cells):
            t0 = time.time()
            result = run_axis1_cell(cell, seeds)
            dt = time.time() - t0
            cell_results.append(result)
            cma = result["aggregated"]["standard_cma_godard_z"]
            mma = result["aggregated"]["mma_yang_werner_dumont"]
            print(
                f"[{i+1:2d}/{len(cells)}] {result['cell_id']:36s} t={dt:5.1f}s\n"
                f"         CMA: near_pi={cma['nearest_pi_ser']:.4f} "
                f"orac_pi={cma['oracle_pi_ser']:.4f} "
                f"headroom={cma['visible_headroom']:.4f} "
                f"(n={cma['n_valid_seeds']}/{cma['n_total_seeds']})\n"
                f"         MMA: near_pi={mma['nearest_pi_ser']:.4f} "
                f"orac_pi={mma['oracle_pi_ser']:.4f} "
                f"headroom={mma['visible_headroom']:.4f} "
                f"(n={mma['n_valid_seeds']}/{mma['n_total_seeds']})"
            )
        total_dt = time.time() - t_start
        print(f"\nAxis 1 wall time: {total_dt:.1f}s ({total_dt/60:.2f} min)")
        out["axes_run"].append({
            "axis_id": "atlas_v1_cells_with_mma",
            "wall_time_seconds": total_dt,
            "n_cells": len(cell_results),
            "n_seeds_per_cell": len(seeds),
            "cell_results": cell_results,
        })

    # ─── Axis 2: Convergence length adjudication ─────────────────────────────
    if args.axis2 or args.smoke:
        print("\n" + "=" * 78)
        print("Axis 2: Convergence probe x {N=512, N=32768} (adjudicates under-convergence)")
        print("=" * 78)
        cells = CONVERGENCE_PROBE_CELLS
        lengths = CONVERGENCE_LENGTHS
        seeds = [11, 12, 13, 14, 15]
        if args.smoke:
            cells = cells[:1]
            lengths = [512]
            seeds = [11, 12]
        cell_results = []
        t_start = time.time()
        for i, cell in enumerate(cells):
            for n_symbols in lengths:
                t0 = time.time()
                result = run_axis2_cell(cell, n_symbols, seeds)
                dt = time.time() - t0
                cell_results.append(result)
                cma = result["aggregated"]["standard_cma_godard_z"]
                mma = result["aggregated"]["mma_yang_werner_dumont"]
                print(
                    f"[{result['cell_id']:28s}] t={dt:6.1f}s\n"
                    f"         CMA: near_pi={cma['nearest_pi_ser']:.4f} "
                    f"orac_pi={cma['oracle_pi_ser']:.4f} "
                    f"headroom={cma['visible_headroom']:.4f}\n"
                    f"         MMA: near_pi={mma['nearest_pi_ser']:.4f} "
                    f"orac_pi={mma['oracle_pi_ser']:.4f} "
                    f"headroom={mma['visible_headroom']:.4f}"
                )
        total_dt = time.time() - t_start
        print(f"\nAxis 2 wall time: {total_dt:.1f}s ({total_dt/60:.2f} min)")
        out["axes_run"].append({
            "axis_id": "convergence_length_adjudication",
            "wall_time_seconds": total_dt,
            "n_cells": len(cell_results),
            "n_seeds_per_cell": len(seeds),
            "cell_results": cell_results,
        })

    # ─── Write raw JSON ───────────────────────────────────────────────────────
    out_path = BATCH_DIR / "artifacts" / "baseline-adjudication-v1.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(_jsonable(out), f, indent=2, ensure_ascii=False)
    print(f"\nRaw JSON written: {out_path}")
    print(f"Total wall time: {sum(ax['wall_time_seconds'] for ax in out['axes_run']):.1f}s")


if __name__ == "__main__":
    main()
