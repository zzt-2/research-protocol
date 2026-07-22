"""Shared infrastructure for the information-source-portfolio Probe batch.

Frozen contract: ../probe-contract.v1.yaml (governed by D019/D020/S012).

This module is the ONE shared substrate for all three headroom/observability Probes
(F1-A model-prior oracle, F3-A causal-history MI, F4-A corrected soft/GMI oracle).
It guarantees:
  - same anchor (baseline.standard_cma.godard_z, fixed-mu=0.03)
  - same 11-cell slice
  - same eval window (256 symbols)
  - same paired realization (make_realization) across comparator and candidate per (cell,seed)
  - fresh disjoint seeds (validation 131-135, test 141-150; NOT 71-80)
  - source-closure SHA-256 hashing of all src files
  - receiver-visible vs oracle separation (oracle reads sX/sY/h/theta; visible path does NOT)

This is a HEADROOM/OBSERVABILITY Probe module. It does NOT train any model, build a router,
or implement an EKF/particle filter. Oracle results are scoring-only Kill/headroom bounds (FR-21),
never Go criteria (FR-25).
"""
from __future__ import annotations
import hashlib
import sys
import time
from pathlib import Path

import numpy as np
import yaml

HERE = Path(__file__).resolve()
SRC_DIR = HERE.parent
BATCH_DIR = SRC_DIR.parent                 # .../scout/info-source-portfolio-probe
SCOUT_DIR = BATCH_DIR.parent               # .../direction-lab/scout
CB1_ROOT = SCOUT_DIR / "cb1-modulation-generic-closure"
ATLAS_DIR = CB1_ROOT / "baseline-atlas"
MMA_DIR = CB1_ROOT / "baseline-adjudication-batch"
C12_DIR = CB1_ROOT / "c12-gmi-soft-output-scout" / "src"
REPO_ROOT = HERE.parents[6]                # worktree root (this batch is one level shallower than hybrid-routing-scout-v1)
SIM_DIR = REPO_ROOT / "projects" / "simulation"
for _p in (str(SIM_DIR), str(ATLAS_DIR), str(MMA_DIR), str(C12_DIR), str(SRC_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402
import cb1_evaluator as evaluator  # noqa: E402
import cb1_cell_runner as atlas_runner  # noqa: E402

# ─── Frozen contract constants (mirror hybrid-routing-scout-v1 for continuity) ───
FROZEN = {
    "alpha": 4.2, "beta": 1.4, "block": 100, "t_s": 4e-10,
    "method": "gar", "cma_mu_fixed": 0.03, "cma_taps": 11,
    "cma_block_size": 64, "r2_qam16": 1.32,
}
MDE = 0.005
PRACTICAL_HEADROOM_MIN = 0.03
R2_16QAM = 1.32
RANDOM_CEILING = 0.9375  # 16QAM random PI-SER (15/16)

VAL_SEEDS = [131, 132, 133, 134, 135]
TEST_SEEDS = [141, 142, 143, 144, 145, 146, 147, 148, 149, 150]
PRIOR_SEEDS_USED = ["11-20", "21-30", "31-35", "41-50", "61-65",
                    "71-80", "81-95", "101-105", "121-130"]

ATLAS_CELLS = [
    {"id": "16qam-snr05-nominal-short", "snr_db": 5.0,  "f_g_hz": 30.0,  "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr10-nominal-short", "snr_db": 10.0, "f_g_hz": 30.0,  "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr15-nominal-short", "snr_db": 15.0, "f_g_hz": 30.0,  "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr20-nominal-short", "snr_db": 20.0, "f_g_hz": 30.0,  "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr25-nominal-short", "snr_db": 25.0, "f_g_hz": 30.0,  "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr20-fg100-short",   "snr_db": 20.0, "f_g_hz": 100.0, "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr20-fg1000-short",  "snr_db": 20.0, "f_g_hz": 1000.0,"sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr20-sop40e-short",  "snr_db": 20.0, "f_g_hz": 30.0,  "sop_rate": 4.0e-5, "n_symbols": 512},
    {"id": "16qam-snr10-fg100-long",    "snr_db": 10.0, "f_g_hz": 100.0, "sop_rate": 4.0e-6, "n_symbols": 8192},
    {"id": "16qam-snr15-fg1000-long",   "snr_db": 15.0, "f_g_hz": 1000.0,"sop_rate": 4.0e-6, "n_symbols": 8192},
    {"id": "16qam-snr20-nominal-long",  "snr_db": 20.0, "f_g_hz": 30.0,  "sop_rate": 4.0e-6, "n_symbols": 8192},
]


def assert_seed_discipline():
    """Assert validation/test seeds are disjoint from each other and from all prior batches."""
    val = set(VAL_SEEDS)
    test = set(TEST_SEEDS)
    assert not (val & test), f"validation ∩ test = {val & test}"
    prior = set()
    for r in PRIOR_SEEDS_USED:
        lo, hi = map(int, r.split("-"))
        prior |= set(range(lo, hi + 1))
    assert not (val & prior), f"validation ∩ prior = {val & prior}"
    assert not (test & prior), f"test ∩ prior = {test & prior}"


def make_realization(cell, seed):
    """Build ONE shared realization (paired across comparator/candidate per (cell,seed))."""
    gamma_bar = float(10.0 ** (float(cell["snr_db"]) / 10.0))
    return generate_shared_realization_dp(
        int(cell["n_symbols"]), float(FROZEN["alpha"]), float(FROZEN["beta"]),
        float(cell["f_g_hz"]), sop_rate=float(cell["sop_rate"]), seed=int(seed),
        gamma_bar=gamma_bar, block=int(FROZEN["block"]), t_s=float(FROZEN["t_s"]),
        method=str(FROZEN["method"]), modulation="qam16")


def eval_window(cell):
    """Return (eval_start, calib_start, eval_end, total) window tuple."""
    return atlas_runner.eval_window_for(
        int(cell["n_symbols"]), int(FROZEN["cma_taps"]),
        window_symbols=256, block_size=int(FROZEN["cma_block_size"]))


def metrics(zX, zY, truth_eval, bx, by):
    """Compute pi_ser (primary) + fixed_label_ser (secondary) via cb1_evaluator."""
    m = evaluator.evaluate_dual_16qam(
        zX, zY, truth_eval[:, 0], truth_eval[:, 1], bx, by)
    return {"pi_ser": float(m["pi_ser"]), "fixed_label_ser": float(m["fixed_label_ser"])}


def run_cma_anchor(rX, rY):
    """The canonical anchor: standard_cma_godard_with_z at fixed mu=0.03 (B01-R fair fixed-mu)."""
    return atlas_runner.standard_cma_godard_with_z(
        rX, rY, n_tap=int(FROZEN["cma_taps"]), mu=float(FROZEN["cma_mu_fixed"]),
        R2=R2_16QAM, block_size=int(FROZEN["cma_block_size"]))


def reconstruct_jones(h, theta):
    """Reconstruct the real 2x2 SOP Jones matrix from channel state (analytic, matches
    _dual_pol_channel.py:127-132). J = sqrt(h) * [[cos, sin],[-sin, cos]].

    This is an ORACLE/privileged construction (uses eval-truth h, theta) — only for
    scoring-only headroom Probes (F1-A). NEVER feed to a receiver-visible path.
    """
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    sh = np.sqrt(h)
    # Return per-sample 2x2 as stacked arrays: J[0,0], J[0,1], J[1,0], J[1,1]
    return sh * cos_t, sh * sin_t, -sh * sin_t, sh * cos_t  # a,b,c,d


def mmse_equalize_oracle(rX, rY, h, theta, sX_calib, sY_calib, es, ce, ee):
    """Oracle per-block MMSE equalizer using TRUE channel state (h, theta).

    This is a scoring-only Kill/headroom bound (FR-21). It uses TX-truth calibration
    symbols AND true h/theta. It establishes the upper bound on what a model-based
    tracker COULD achieve if it recovered the Jones state perfectly.

    Method: per-block, undo the SOP rotation analytically (we know theta), then
    apply a per-block least-squares unmix on the de-rotated stream using TX-truth
    calibration symbols. This is the strongest 'model-based tracker -> MMSE' bound
    short of full per-sample Wiener.
    """
    a, b, c, d = reconstruct_jones(h, theta)
    # Invert the SOP rotation analytically: J^{-1} = (1/sqrt(h)) * [[cos,-sin],[sin,cos]]
    inv_det = 1.0 / (a * d - b * c + 1e-30)  # det = h (>=0); guard /0
    inv_a = d * inv_det
    inv_b = -b * inv_det
    inv_c = -c * inv_det
    inv_d = a * inv_det
    # De-rotate: r' = J^{-1} @ r  -> removes SOP, leaves sqrt(h)*s + J^{-1}@noise
    rX_derot = inv_a * rX + inv_b * rY
    rY_derot = inv_c * rX + inv_d * rY
    # Per-block complex scalar unmix on de-rotated stream using TX-truth calibration
    # (de-rotation leaves a per-block complex gain = sqrt(h) * constellation rotation;
    #  LS against TX truth removes it). Use calibration window then apply to eval window.
    def _ls_unmix(rx_cal, ry_cal, sx_cal, sy_cal):
        R = np.vstack([rx_cal, ry_cal])
        S = np.vstack([sx_cal, sy_cal])
        W, *_ = np.linalg.lstsq(R.T, S.T, rcond=1e-10)
        Z = W.T @ R
        return Z[0], Z[1]
    # Calibration on [es:ce], apply the SAME linear map to [ce:ee] (frozen before eval)
    zX_c, zY_c = _ls_unmix(rX_derot[es:ce], rY_derot[es:ce], sX_calib, sY_calib)
    # Reuse W on eval window
    R_eval = np.vstack([rX_derot[ce:ee], rY_derot[ce:ee]])
    R_cal = np.vstack([rX_derot[es:ce], rY_derot[es:ce]])
    S_cal = np.vstack([sX_calib, sY_calib])
    W, *_ = np.linalg.lstsq(R_cal.T, S_cal.T, rcond=1e-10)
    Z_eval = W.T @ R_eval
    return Z_eval[0], Z_eval[1]


def bootstrap_ci(data, n_boot=2000, alpha=0.05, rng_seed=0):
    """Paired bootstrap CI on a 1D array (returns mean, lo, hi)."""
    data = np.asarray(data, dtype=float)
    n = len(data)
    if n == 0:
        return float("nan"), float("nan"), float("nan")
    rng = np.random.default_rng(rng_seed)
    means = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, n, n)
        means[i] = float(np.mean(data[idx]))
    lo = float(np.quantile(means, alpha / 2))
    hi = float(np.quantile(means, 1 - alpha / 2))
    return float(np.mean(data)), lo, hi


def macro_aggregate(rows, key):
    """Macro mean = mean of per-cell means (hierarchical), with bootstrap CI on per-cell means."""
    by_cell = {}
    for r in rows:
        by_cell.setdefault(r["cell"], []).append(r[key])
    cell_means = [float(np.mean(v)) for v in by_cell.values()]
    macro, lo, hi = bootstrap_ci(cell_means)
    return {"macro": macro, "ci_lo": lo, "ci_hi": hi, "n_cells": len(cell_means),
            "cell_means": dict(zip(by_cell.keys(), cell_means))}


def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def source_closure_hashes(extra_files=None):
    """SHA-256 of all src files in this Probe batch (+ optionally extra dependency files)."""
    files = sorted(SRC_DIR.glob("*.py"))
    if extra_files:
        files = list(files) + list(extra_files)
    return {str(p.relative_to(BATCH_DIR)): sha256_of_file(p) for p in files}


def write_result(probe_id, payload, fname="result.v1.json"):
    """Write a Probe result.json with metadata + source closure hash."""
    out = BATCH_DIR / "artifacts" / f"{probe_id}-{fname}"
    out.parent.mkdir(parents=True, exist_ok=True)
    payload["metadata"] = {
        "probe_id": probe_id,
        "schema": "direction-lab.info-source-portfolio-probe.v1",
        "MDE": MDE,
        "practical_headroom_min": PRACTICAL_HEADROOM_MIN,
        "val_seeds": VAL_SEEDS,
        "test_seeds": TEST_SEEDS,
        "frozen": FROZEN,
        "elapsed_seconds": payload.pop("_elapsed_seconds", None),
        "source_closure_hashes": source_closure_hashes(),
    }
    import json
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, default=str, ensure_ascii=False)
    return out


def elapsed(timer_start):
    return round(time.time() - timer_start, 2)
