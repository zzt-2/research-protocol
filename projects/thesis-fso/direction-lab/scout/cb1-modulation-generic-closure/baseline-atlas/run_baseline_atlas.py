"""CB1 baseline Atlas driver.

Single entry point: builds the contract + cells + closure, runs the cells,
writes raw JSON (synthesis markdown is written separately).

Usage:
    python baseline-atlas/run_baseline_atlas.py            # QPSK regression only (default)
    python baseline-atlas/run_baseline_atlas.py --qpsk     # QPSK regression only
    python baseline-atlas/run_baseline_atlas.py --full     # full 16QAM Atlas (11 cells x 10 seeds) + QPSK regression
    python baseline-atlas/run_baseline_atlas.py --priority # 5-cell priority subset x 5 seeds (time-budget fallback)
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
BASELINE_ATLAS = HERE.parent
CB1_ROOT = BASELINE_ATLAS.parent  # .../cb1-modulation-generic-closure
SCOUT_ROOT = CB1_ROOT.parent
REPO_ROOT = HERE.parents[6]  # .../direction-lab-capability-atlas
SIM_DIR = REPO_ROOT / "projects" / "simulation"

sys.path.insert(0, str(SIM_DIR))
sys.path.insert(0, str(BASELINE_ATLAS))

from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402
import cb1_evaluator as evaluator  # noqa: E402
import cb1_cell_runner as runner  # noqa: E402


# ─── Contract (mirrors P03 stage-a-contract.v1.yaml frozen_common_axes) ──────

CONTRACT: dict[str, Any] = {
    "frozen_common_axes": {
        "alpha": 4.2,
        "beta": 1.4,
        "block": 100,
        "t_s": 0.0000000004,
        "method": "gar",
        "cma_mu": 0.001,
        "cma_taps": 11,
        "r2_qpsk": 1.0,
        "r2_qam16": 1.32,
        "cma_block_size": 64,
        "fade_threshold_h": 0.1,
        "clip_norm": 1.0,
        "csi_access_class": "CSI_NONE",
        "constellation_amplitude_per_axis": 0.7071067811865475,
        "affine_ridge": 0.000001,
        "tail_energy_threshold": 0.25,
        "calibration_fraction": 0.25,
    },
    "statistical_sensitivity": {
        "primary_metric": "PI-SER",
        "secondary_metric": "fixed-label SER",
        "minimum_detectable_effect": {"value": 0.005, "unit": "per-symbol"},
        "zero_error_confidence": "rule_of_three_one_sided_95pc_upper_bound",
        "sequential_sampling_budget": "10_to_40_paired_seeds",
    },
    "covering_design": {
        "strategy": "covering_array_with_anchors",
        "paired_seeds": [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    },
}


# QPSK regression cell: P03 v1 anchor (snr=20, f_g=30, sop=4e-6, N=512)
QPSK_ANCHOR_CELL = {
    "id": "qpsk-snr20-nominal-short-P03v1-anchor",
    "modulation": "qpsk",
    "snr_db": 20.0,
    "f_g_hz": 30.0,
    "sop_rate": 0.000004,
    "n_symbols": 512,
}


# Full 16QAM cell set (mirrors P03 11-cell design, modulation=qam16)
QAM16_CELLS = [
    {"id": "16qam-snr05-nominal-short", "modulation": "qam16", "snr_db": 5.0,  "f_g_hz": 30.0,  "sop_rate": 0.000004, "n_symbols": 512},
    {"id": "16qam-snr10-nominal-short", "modulation": "qam16", "snr_db": 10.0, "f_g_hz": 30.0,  "sop_rate": 0.000004, "n_symbols": 512},
    {"id": "16qam-snr15-nominal-short", "modulation": "qam16", "snr_db": 15.0, "f_g_hz": 30.0,  "sop_rate": 0.000004, "n_symbols": 512},
    {"id": "16qam-snr20-nominal-short", "modulation": "qam16", "snr_db": 20.0, "f_g_hz": 30.0,  "sop_rate": 0.000004, "n_symbols": 512},
    {"id": "16qam-snr25-nominal-short", "modulation": "qam16", "snr_db": 25.0, "f_g_hz": 30.0,  "sop_rate": 0.000004, "n_symbols": 512},
    {"id": "16qam-snr20-fg100-short",   "modulation": "qam16", "snr_db": 20.0, "f_g_hz": 100.0, "sop_rate": 0.000004, "n_symbols": 512},
    {"id": "16qam-snr20-fg1000-short",  "modulation": "qam16", "snr_db": 20.0, "f_g_hz": 1000.0,"sop_rate": 0.000004, "n_symbols": 512},
    {"id": "16qam-snr20-sop40e-short",  "modulation": "qam16", "snr_db": 20.0, "f_g_hz": 30.0,  "sop_rate": 0.000040, "n_symbols": 512},
    {"id": "16qam-snr10-fg100-long",    "modulation": "qam16", "snr_db": 10.0, "f_g_hz": 100.0, "sop_rate": 0.000004, "n_symbols": 8192},
    {"id": "16qam-snr15-fg1000-long",   "modulation": "qam16", "snr_db": 15.0, "f_g_hz": 1000.0,"sop_rate": 0.000004, "n_symbols": 8192},
    {"id": "16qam-snr20-nominal-long",  "modulation": "qam16", "snr_db": 20.0, "f_g_hz": 30.0,  "sop_rate": 0.000004, "n_symbols": 8192},
]

# Time-budget priority subset (if full sweep too slow)
QAM16_PRIORITY_CELLS = [
    "16qam-snr10-nominal-short",
    "16qam-snr15-nominal-short",
    "16qam-snr20-nominal-short",
    "16qam-snr20-fg1000-short",
    "16qam-snr15-fg1000-long",
]


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


def run_qpsk_regression(verbose: bool = True) -> dict[str, Any]:
    """Run the QPSK anchor cell (single seed=11, P03 v1) to verify wiring."""
    # Override seeds to just [11] for a fast regression check
    contract = json.loads(json.dumps(CONTRACT))
    contract["covering_design"]["paired_seeds"] = [11]
    t0 = time.time()
    result = runner.run_cell(QPSK_ANCHOR_CELL, contract, generator=generate_shared_realization_dp, evaluator=evaluator)
    dt = time.time() - t0
    if verbose:
        d = result["decision"]
        print(f"[QPSK regression] cell={result['cell_id']}  seed=11  time={dt:.2f}s")
        print(f"  identity_gate_ok = {result['identity_gate_ok']}")
        print(f"  nearest_pi_ser = {d['nearest_pi_ser']:.6f}")
        print(f"  oracle_pi_ser  = {d['oracle_pi_ser']:.6f}")
        print(f"  visible_headroom = {d['visible_headroom']:.6f}")
        print(f"  decision_class = {d['decision_class']}  status = {d['status']}")
        print(f"  mean_fixed_label_ser.nearest = {result['mean_fixed_label_ser']['nearest']:.6f}")
    return result


def run_full_atlas(verbose: bool = True, full_seeds: bool = True, cells_override: list[str] | None = None) -> dict[str, Any]:
    """Run the 16QAM baseline Atlas. Returns dict for JSON dump."""
    contract = json.loads(json.dumps(CONTRACT))
    if not full_seeds:
        contract["covering_design"]["paired_seeds"] = [11, 12, 13, 14, 15]

    cells_to_run = QAM16_CELLS
    if cells_override is not None:
        cells_to_run = [c for c in QAM16_CELLS if c["id"] in cells_override]

    cell_results = []
    t_start = time.time()
    for i, cell in enumerate(cells_to_run):
        t0 = time.time()
        result = runner.run_cell(cell, contract, generator=generate_shared_realization_dp, evaluator=evaluator)
        dt = time.time() - t0
        cell_results.append(result)
        if verbose:
            d = result["decision"]
            print(f"[{i+1}/{len(cells_to_run)}] {result['cell_id']:36s} t={dt:5.1f}s "
                  f"near_pi={d['nearest_pi_ser']:.4f} blind_pi={d['blind_pi_ser']:.4f} "
                  f"orac_pi={d['oracle_pi_ser']:.4f} headroom={d['visible_headroom']:.4f} "
                  f"-> {d['decision_class']}  (n_seed={result['n_paired_seeds']}, div={result['n_diverged_seeds']})")
    total_dt = time.time() - t_start
    if verbose:
        print(f"\nTotal Atlas wall time: {total_dt:.1f}s ({total_dt/60:.2f} min)")

    return {
        "schema_version": "direction-lab.cb1.baseline-atlas.v1",
        "campaign_id": "science-scout-2026-07-20.dual-pol-osl",
        "modulation_axis_status": "16QAM_UNBLOCKED (CB1 closure)",
        "contract": CONTRACT,
        "qpsk_anchor": QPSK_ANCHOR_CELL,
        "cells_run": [c["id"] for c in cells_to_run],
        "n_seeds_per_cell": len(contract["covering_design"]["paired_seeds"]),
        "wall_time_seconds": total_dt,
        "cell_results": cell_results,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--qpsk", action="store_true", help="Run only the QPSK regression anchor cell")
    ap.add_argument("--full", action="store_true", help="Run the full 16QAM Atlas (11 cells x 10 seeds)")
    ap.add_argument("--priority", action="store_true", help="Run the 5-cell priority subset x 5 seeds (time-budget)")
    args = ap.parse_args()

    if args.qpsk or not (args.full or args.priority):
        run_qpsk_regression()
        return

    # Always run QPSK regression first
    print("=" * 70)
    print("STEP 1: QPSK regression (P03 v1 anchor)")
    print("=" * 70)
    qpsk_result = run_qpsk_regression()
    if not qpsk_result["identity_gate_ok"]:
        print("ABORT: QPSK identity gate failed — runner bug, cannot trust 16QAM")
        sys.exit(1)
    anchor_pi = qpsk_result["decision"]["nearest_pi_ser"]
    if anchor_pi > 0.01:
        print(f"ABORT: QPSK anchor PI-SER={anchor_pi:.4f} != 0.0 — runner wiring bug")
        sys.exit(1)
    print(f"QPSK regression PASS (PI-SER={anchor_pi:.6f})\n")

    print("=" * 70)
    print("STEP 2: 16QAM baseline Atlas")
    print("=" * 70)
    if args.full:
        atlas = run_full_atlas(full_seeds=True)
    else:  # priority
        atlas = run_full_atlas(full_seeds=False, cells_override=QAM16_PRIORITY_CELLS)
    atlas["qpsk_regression"] = {
        "cell_id": qpsk_result["cell_id"],
        "identity_gate_ok": qpsk_result["identity_gate_ok"],
        "nearest_pi_ser": qpsk_result["decision"]["nearest_pi_ser"],
        "oracle_pi_ser": qpsk_result["decision"]["oracle_pi_ser"],
        "visible_headroom": qpsk_result["decision"]["visible_headroom"],
        "decision_class": qpsk_result["decision"]["decision_class"],
        "mean_fixed_label_ser": qpsk_result["mean_fixed_label_ser"],
    }

    artifacts_dir = BASELINE_ATLAS / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    out_json = artifacts_dir / "cb1-baseline-atlas-v1.json"
    out_json.write_text(json.dumps(_jsonable(atlas), indent=2, sort_keys=True), encoding="utf-8")
    print(f"\nWrote {out_json}")


if __name__ == "__main__":
    main()
