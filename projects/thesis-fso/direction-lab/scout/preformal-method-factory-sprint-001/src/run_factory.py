"""Pre-formal Method Factory Sprint 001 — smoke + fair comparison driver.

Reuses the frozen CB1 testbed (generator, evaluator, baseline) via adapter.
Runs, for every (cell, seed) on the SAME paired realization:
  - frozen baseline (standard_cma_godard_z)        [inherited anchor]
  - strong cheap alternative (blind_affine_16qam)  [shared]
  - M1 reduced-modulus CMA
  - M2 trace-driven causal re-init CMA
  - M3 multi-start + alphabet-geometry select CMA
  - M4 conditional DD affine cascade (on baseline z)
  - M5 radius-shell remap (on baseline z)

Outputs raw-rows.v1.csv (one row per method x cell x seed) and result.v1.json.

Usage:
    python run_factory.py --smoke     # identity + boundary smoke per construct
    python run_factory.py --compare   # full paired comparison across 6 cells x 10 seeds
    python run_factory.py --all       # smoke then compare
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve()
SRC = HERE.parent
SPRINT_ROOT = SRC.parent                       # preformal-method-factory-sprint-001/
CB1_ROOT = SPRINT_ROOT.parent / "cb1-modulation-generic-closure"
BASELINE_ATLAS = CB1_ROOT / "baseline-atlas"
REPO_ROOT = HERE.parents[6]                     # worktree root
SIM_DIR = REPO_ROOT / "projects" / "simulation"

for p in (str(SIM_DIR), str(BASELINE_ATLAS), str(SRC)):
    if p not in sys.path:
        sys.path.insert(0, p)

from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402
import cb1_evaluator as evaluator  # noqa: E402
import cb1_cell_runner as runner  # noqa: E402
import methods as M  # noqa: E402


# ─── Frozen contract (mirrors factory-contract.v1.yaml) ─────────────────────
FROZEN_AXES = {
    "alpha": 4.2, "beta": 1.4, "block": 100, "t_s": 4.0e-10, "method": "gar",
    "cma_mu": 1e-3, "cma_taps": 11, "r2_qam16": 1.32, "cma_block_size": 64,
    "affine_ridge": 1e-6, "constellation_amplitude_per_axis": 0.7071067811865475,
}

CELLS = [
    {"id": "snr20-nominal-short", "modulation": "qam16", "snr_db": 20.0, "f_g_hz": 30.0,   "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "snr25-nominal-short", "modulation": "qam16", "snr_db": 25.0, "f_g_hz": 30.0,   "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "snr20-fg1000-short",  "modulation": "qam16", "snr_db": 20.0, "f_g_hz": 1000.0, "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "snr20-sop40e-short",  "modulation": "qam16", "snr_db": 20.0, "f_g_hz": 30.0,   "sop_rate": 4.0e-5, "n_symbols": 512},
    {"id": "snr15-nominal-short", "modulation": "qam16", "snr_db": 15.0, "f_g_hz": 30.0,   "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "snr20-nominal-long",  "modulation": "qam16", "snr_db": 20.0, "f_g_hz": 30.0,   "sop_rate": 4.0e-6, "n_symbols": 8192},
]
SEEDS = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
HALF_A = [11, 12, 13, 14, 15]
HALF_B = [16, 17, 18, 19, 20]
R2_16QAM = 1.32


def _realization(cell: dict[str, Any], seed: int) -> dict[str, Any]:
    gamma_bar = float(10.0 ** (float(cell["snr_db"]) / 10.0))
    return generate_shared_realization_dp(
        int(cell["n_symbols"]), float(FROZEN_AXES["alpha"]), float(FROZEN_AXES["beta"]),
        float(cell["f_g_hz"]), sop_rate=float(cell["sop_rate"]), seed=int(seed),
        gamma_bar=gamma_bar, block=int(FROZEN_AXES["block"]),
        t_s=float(FROZEN_AXES["t_s"]), method=str(FROZEN_AXES["method"]),
        modulation=str(cell["modulation"]),
    )


def _eval_window(n_symbols: int) -> tuple[int, int, int]:
    es, cal, ee, _ = runner.eval_window_for(
        n_symbols, int(FROZEN_AXES["cma_taps"]),
        window_symbols=256, block_size=int(FROZEN_AXES["cma_block_size"]),
    )
    return es, cal, ee


def _eval_pred(predicted_x: np.ndarray, predicted_y: np.ndarray,
               truth_eval_x: np.ndarray, truth_eval_y: np.ndarray,
               bits_eval_x: np.ndarray, bits_eval_y: np.ndarray) -> dict[str, float]:
    m = evaluator.evaluate_dual_16qam(
        predicted_x, predicted_y, truth_eval_x, truth_eval_y, bits_eval_x, bits_eval_y,
    )
    return {"pi_ser": float(m["pi_ser"]), "fixed_label_ser": float(m["fixed_label_ser"]),
            "pi_ber": float(m["pi_ber"])}


def _slice_streams(z, truth, bits, es, cal, ee, pol: str):
    """Slice eval window out of a converged z-stream (pol = 'X' or 'Y')."""
    z_arr = np.asarray(z)
    return (z_arr[es:ee] if pol == "X" else z_arr[es:ee],
            truth[cal:ee] if False else None)  # placeholder, set by caller


# ─── Per-(cell,seed) realization runner for ALL methods ─────────────────────

def run_all_methods_on_realization(cell: dict[str, Any], seed: int) -> dict[str, Any]:
    """Run baseline + 5 constructs + blind-affine on ONE shared realization."""
    n = int(cell["n_symbols"])
    es, cal, ee = _eval_window(n)
    R2 = R2_16QAM
    ridge = float(FROZEN_AXES["affine_ridge"])
    mu = float(FROZEN_AXES["cma_mu"])
    taps = int(FROZEN_AXES["cma_taps"])
    bs = int(FROZEN_AXES["cma_block_size"])

    realization = _realization(cell, seed)
    bits_per = 4  # 16QAM
    truth_eval_x = realization["sX"][cal:ee]
    truth_eval_y = realization["sY"][cal:ee]
    bits_eval_x = realization["bitsX"][cal * bits_per:ee * bits_per]
    bits_eval_y = realization["bitsY"][cal * bits_per:ee * bits_per]

    # ---- Frozen baseline: standard-CMA Godard-with-z (R2=1.32) ------------
    base = runner.standard_cma_godard_with_z(
        realization["rX"], realization["rY"], n_tap=taps, mu=mu, R2=R2, block_size=bs,
    )
    methods_out: dict[str, Any] = {}

    def _eval_zstream(zX, zY, diverged):
        if diverged:
            return {"pi_ser": float("nan"), "fixed_label_ser": float("nan"),
                    "pi_ber": float("nan"), "diverged": True}
        # eval slice = [calibration_end:eval_end], matching cb1_cell_runner
        px = np.asarray(evaluator.hard_16qam(zX[cal:ee]))
        py = np.asarray(evaluator.hard_16qam(zY[cal:ee]))
        m = _eval_pred(px, py, truth_eval_x, truth_eval_y, bits_eval_x, bits_eval_y)
        m["diverged"] = False
        return m

    methods_out["baseline_cma"] = {
        **_eval_zstream(base["zX"], base["zY"], base["diverged"]),
        "identity_gate": base["provenance"].get("gradient") == "Godard-with-z",
        "final_w_norm": float(base["final_w_norm"]),
    }

    # ---- Strong cheap alternative: blind affine (on baseline z, shared) ----
    z_calib = np.column_stack([base["zX"][es:cal], base["zY"][es:cal]])
    z_eval = np.column_stack([base["zX"][cal:ee], base["zY"][cal:ee]])
    if not base["diverged"]:
        blind = evaluator.blind_affine_compare_16qam(z_calib, z_eval, ridge=ridge)
        m = _eval_pred(blind["predicted"][:, 0], blind["predicted"][:, 1],
                       truth_eval_x, truth_eval_y, bits_eval_x, bits_eval_y)
        m["diverged"] = False
    else:
        m = {"pi_ser": float("nan"), "fixed_label_ser": float("nan"),
             "pi_ber": float("nan"), "diverged": True}
    methods_out["blind_affine"] = m

    # ---- M1: reduced-modulus CMA (re-run equalizer) -----------------------
    m1 = M.m1_reduced_modulus_cma(realization, n_tap=taps, mu=mu, block_size=bs)
    methods_out["M1_reduced_modulus"] = {
        **_eval_zstream(m1["zX"], m1["zY"], m1["diverged"]),
        "final_w_norm": float(m1["final_w_norm"]),
    }

    # ---- M2: trace-driven causal re-init CMA (re-run equalizer) ----------
    m2 = M.m2_trace_reinit_cma(realization, n_tap=taps, mu=mu, block_size=bs)
    methods_out["M2_trace_reinit"] = {
        **_eval_zstream(m2["zX"], m2["zY"], m2["diverged"]),
        "final_w_norm": float(m2["final_w_norm"]),
        "reinit_count": int(m2["reinit_count"]),
    }

    # ---- M3: multi-start + alphabet-geometry select (re-run K equalizers) -
    m3 = M.m3_multistart_select_cma(
        realization, n_tap=taps, mu=mu, block_size=bs, K=4, eval_slice=(cal, ee),
    )
    methods_out["M3_multistart_select"] = {
        **_eval_zstream(m3["zX"], m3["zY"], m3["diverged"]),
        "final_w_norm": float(m3["final_w_norm"]),
        "selected_k": int(m3["m3_selected_k"]),
        "all_scores": [float(x) for x in m3["m3_all_scores"]],
        "all_diverged": [bool(x) for x in m3["m3_all_diverged"]],
    }

    # ---- M4: conditional DD affine cascade (post-proc on baseline z) -----
    m4 = M.m4_conditional_dd_affine(z_calib, z_eval, ridge=ridge, collapse_threshold=0.5)
    if not base["diverged"]:
        m = _eval_pred(m4["predicted"][:, 0], m4["predicted"][:, 1],
                       truth_eval_x, truth_eval_y, bits_eval_x, bits_eval_y)
        m["diverged"] = False
    else:
        m = {"pi_ser": float("nan"), "fixed_label_ser": float("nan"),
             "pi_ber": float("nan"), "diverged": True}
    m["gate_open"] = bool(m4["gate_open"])
    m["cal_power"] = float(m4["cal_power"])
    methods_out["M4_conditional_dd"] = m

    # ---- M5: radius-shell remap (post-proc on baseline z) ----------------
    m5 = M.m5_radius_shell_remap(z_eval)
    if not base["diverged"]:
        m = _eval_pred(m5["predicted"][:, 0], m5["predicted"][:, 1],
                       truth_eval_x, truth_eval_y, bits_eval_x, bits_eval_y)
        m["diverged"] = False
    else:
        m = {"pi_ser": float("nan"), "fixed_label_ser": float("nan"),
             "pi_ber": float("nan"), "diverged": True}
    m["remap_collapsed"] = bool(m5["collapsed"])
    m["r_span"] = float(m5["r_span"])
    methods_out["M5_radius_remap"] = m

    return {
        "cell_id": cell["id"], "seed": int(seed),
        "n_symbols": n, "eval_window": {"eval_start": es, "calibration_end": cal, "eval_end": ee},
        "methods": methods_out,
        "base_diverged": bool(base["diverged"]),
    }


# ─── Phase C-1: semantic smoke (identity + action-identity) ─────────────────

def smoke_tests() -> dict[str, Any]:
    """Per-construct input-sensitivity + boundary-degradation smoke.

    For each construct verify:
      (a) action identity: different legitimate inputs produce different outputs
      (b) clean-boundary degradation: on a clean (no-collapse) input, disabling
          the new component degrades to the frozen baseline (no regression)
    """
    print("=" * 70)
    print("PHASE C-1: SEMANTIC SMOKE")
    print("=" * 70)
    results: dict[str, Any] = {}

    # Use one short cell, two seeds (one likely-collapsed, one likely-clean)
    cell = CELLS[0]  # snr20-nominal-short
    n = int(cell["n_symbols"])
    es, cal, ee = _eval_window(n)

    # --- M1 action identity: different R2 -> different z -------------------
    rA = _realization(cell, 11)
    m1a = M.m1_reduced_modulus_cma(rA)
    # baseline (R2=1.32) for comparison
    baseA = runner.standard_cma_godard_with_z(
        rA["rX"], rA["rY"], n_tap=11, mu=1e-3, R2=1.32, block_size=64)
    z1 = np.concatenate([m1a["zX"][es:ee], m1a["zY"][es:ee]])
    zb = np.concatenate([baseA["zX"][es:ee], baseA["zY"][es:ee]])
    m1_diff = float(np.mean(np.abs(z1 - zb)))
    results["M1_action_identity"] = {
        "test": "reduced_modulus(R2=0.2) vs baseline(R2=1.32) z differ",
        "mean_abs_z_diff": m1_diff,
        "pass": m1_diff > 1e-6,
    }
    print(f"  M1 action identity: |z(M1)-z(baseline)|={m1_diff:.4e} -> "
          f"{'PASS' if m1_diff > 1e-6 else 'FAIL'}")

    # --- M2 action identity: reinit_count changes with collapse ----------
    rB = _realization(cell, 12)
    m2_collapsed = M.m2_trace_reinit_cma(rB, max_reinits=2)
    m2_off = M.m2_trace_reinit_cma(rB, max_reinits=0)  # reinit disabled
    z_on = np.concatenate([m2_collapsed["zX"][es:ee], m2_collapsed["zY"][es:ee]])
    z_off = np.concatenate([m2_off["zX"][es:ee], m2_off["zY"][es:ee]])
    m2_diff = float(np.mean(np.abs(z_on - z_off)))
    results["M2_action_identity"] = {
        "test": "reinit_on vs reinit_off z differ when collapse detected",
        "reinit_count_on": int(m2_collapsed["reinit_count"]),
        "mean_abs_z_diff": m2_diff,
        "pass": m2_diff > 1e-6,
    }
    print(f"  M2 action identity: reinit_count={m2_collapsed['reinit_count']}, "
          f"|z(on)-z(off)|={m2_diff:.4e} -> {'PASS' if m2_diff > 1e-6 else 'FAIL'}")

    # --- M3 action identity: different inits -> different candidates ------
    m3 = M.m3_multistart_select_cma(rA, K=4, eval_slice=(cal, ee))
    scores = m3["m3_all_scores"]
    score_spread = float(max(scores) - min(scores))
    results["M3_action_identity"] = {
        "test": "K=4 diversity inits produce distinct alphabet-geometry scores",
        "all_scores": [float(s) for s in scores],
        "score_spread": score_spread,
        "selected_k": int(m3["m3_selected_k"]),
        "pass": score_spread > 1e-6,
    }
    print(f"  M3 action identity: scores={[f'{s:.4f}' for s in scores]} "
          f"spread={score_spread:.4e} -> {'PASS' if score_spread > 1e-6 else 'FAIL'}")

    # --- M4 action identity: gate opens on collapsed, closed on clean -----
    # collapsed gate: build a synthetic low-power z
    z_collapsed = baseA["zX"][es:cal] * 0.3  # collapse to inner ring
    zc_eval = baseA["zX"][cal:ee] * 0.3
    m4_open = M.m4_conditional_dd_affine(
        np.column_stack([z_collapsed, z_collapsed]),
        np.column_stack([zc_eval, zc_eval]), ridge=1e-6, collapse_threshold=0.5)
    m4_clean = M.m4_conditional_dd_affine(
        np.column_stack([baseA["zX"][es:cal], baseA["zY"][es:cal]]),
        np.column_stack([baseA["zX"][cal:ee], baseA["zY"][cal:ee]]),
        ridge=1e-6, collapse_threshold=0.5)
    results["M4_action_identity"] = {
        "test": "gate opens on collapsed (power<0.5), closed on clean",
        "gate_open_collapsed": bool(m4_open["gate_open"]),
        "gate_open_clean": bool(m4_clean["gate_open"]),
        "pass": bool(m4_open["gate_open"]) and not bool(m4_clean["gate_open"]),
    }
    print(f"  M4 action identity: gate_open(collapsed)={m4_open['gate_open']}, "
          f"gate_open(clean)={m4_clean['gate_open']} -> "
          f"{'PASS' if (m4_open['gate_open'] and not m4_clean['gate_open']) else 'FAIL'}")

    # --- M5 action identity: remap fires on collapsed, identity on clean ---
    z_eval_clean = np.column_stack([baseA["zX"][cal:ee], baseA["zY"][cal:ee]])
    m5_clean = M.m5_radius_shell_remap(z_eval_clean)
    z_eval_col = z_eval_clean * 0.3
    m5_col = M.m5_radius_shell_remap(z_eval_col)
    results["M5_action_identity"] = {
        "test": "remap fires (collapsed=True) on low-span, identity on healthy",
        "collapsed_clean": bool(m5_clean["collapsed"]),
        "collapsed_lowspan": bool(m5_col["collapsed"]),
        "pass": bool(m5_col["collapsed"]) and not bool(m5_clean["collapsed"]),
    }
    print(f"  M5 action identity: collapsed(clean)={m5_clean['collapsed']}, "
          f"collapsed(lowspan)={m5_col['collapsed']} -> "
          f"{'PASS' if (m5_col['collapsed'] and not m5_clean['collapsed']) else 'FAIL'}")

    return results


# ─── Phase C-2: fair paired comparison ──────────────────────────────────────

def fair_comparison() -> dict[str, Any]:
    print("=" * 70)
    print("PHASE C-2: FAIR PAIRED COMPARISON")
    print(f"  cells: {[c['id'] for c in CELLS]}")
    print(f"  seeds: {SEEDS}  (halves A={HALF_A}, B={HALF_B})")
    print("=" * 70)

    raw_rows: list[dict[str, Any]] = []
    t0 = time.time()
    for ci, cell in enumerate(CELLS):
        for seed in SEEDS:
            res = run_all_methods_on_realization(cell, seed)
            for mname, mres in res["methods"].items():
                raw_rows.append({
                    "cell_id": res["cell_id"],
                    "seed": res["seed"],
                    "method": mname,
                    "pi_ser": (None if (v := mres.get("pi_ser")) is None or np.isnan(v) else float(v)),
                    "fixed_label_ser": (None if (v := mres.get("fixed_label_ser")) is None or np.isnan(v) else float(v)),
                    "pi_ber": (None if (v := mres.get("pi_ber")) is None or np.isnan(v) else float(v)),
                    "diverged": bool(mres.get("diverged", False)),
                })
        print(f"  [{ci+1}/{len(CELLS)}] {cell['id']:24s} done "
              f"({time.time()-t0:.1f}s elapsed)")

    # Write raw rows CSV
    artifacts = SPRINT_ROOT / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    csv_path = artifacts / "raw-rows.v1.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["cell_id", "seed", "method", "pi_ser",
                                          "fixed_label_ser", "pi_ber", "diverged"])
        w.writeheader()
        for row in raw_rows:
            w.writerow(row)
    print(f"\nWrote raw rows: {csv_path} ({len(raw_rows)} rows)")

    return {"raw_rows": raw_rows, "wall_seconds": time.time() - t0}


def aggregate(raw_rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute paired deltas, help/hurt/tie, median, trimmed mean, bootstrap CI."""
    METHOD_ORDER = ["baseline_cma", "blind_affine", "M1_reduced_modulus",
                    "M2_trace_reinit", "M3_multistart_select",
                    "M4_conditional_dd", "M5_radius_remap"]
    CONSTRUCTS = [m for m in METHOD_ORDER if m != "baseline_cma" and m != "blind_affine"]

    # index by (cell, seed, method)
    idx: dict[tuple[str, int, str], float | None] = {}
    for r in raw_rows:
        idx[(r["cell_id"], r["seed"], r["method"])] = r["pi_ser"]

    cells = sorted({r["cell_id"] for r in raw_rows})
    seeds = sorted({r["seed"] for r in raw_rows})

    def _valid_pairs(method: str) -> list[tuple[str, int, float, float]]:
        """Return (cell, seed, baseline_pi_ser, method_pi_ser) for non-nan, non-diverged pairs."""
        out = []
        for c in cells:
            for s in seeds:
                b = idx.get((c, s, "baseline_cma"))
                m = idx.get((c, s, method))
                if b is None or m is None:
                    continue
                out.append((c, s, b, m))
        return out

    def _bootstrap_ci(deltas: list[float], n_boot: int = 2000, seed: int = 42) -> tuple[float, float]:
        if len(deltas) < 2:
            return (float("nan"), float("nan"))
        rng = np.random.default_rng(seed)
        arr = np.asarray(deltas)
        boots = [float(np.median(rng.choice(arr, size=len(arr), replace=True)))
                 for _ in range(n_boot)]
        return (float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5)))

    agg: dict[str, Any] = {}
    for method in CONSTRUCTS:
        pairs = _valid_pairs(method)
        deltas = [m - b for (_, _, b, m) in pairs]
        if not deltas:
            agg[method] = {"n_pairs": 0}
            continue

        # Help/hurt/tie (lower PI-SER is better; help = method < baseline)
        help_n = sum(1 for d in deltas if d < -1e-9)
        hurt_n = sum(1 for d in deltas if d > 1e-9)
        tie_n = sum(1 for d in deltas if abs(d) <= 1e-9)

        # Seed-half direction consistency
        def _half_delta(half: list[int]) -> float:
            hd = [m - b for (c, s, b, m) in pairs if s in half]
            return float(np.median(hd)) if hd else float("nan")
        half_a_med = _half_delta(HALF_A)
        half_b_med = _half_delta(HALF_B)
        direction_consistent = (np.sign(half_a_med) == np.sign(half_b_med)
                                and not np.isnan(half_a_med) and not np.isnan(half_b_med))

        # Median + trimmed mean (10%) of paired deltas
        median_delta = float(np.median(deltas))
        trimmed_delta = float(stats_trimmed_mean(deltas, 0.1))
        ci_lo, ci_hi = _bootstrap_ci(deltas)

        # Per-cell summary
        per_cell: dict[str, dict[str, float]] = {}
        for c in cells:
            cd = [m - b for (cc, s, b, m) in pairs if cc == c]
            if cd:
                per_cell[c] = {
                    "n": len(cd),
                    "median_delta": float(np.median(cd)),
                    "help": int(sum(1 for d in cd if d < -1e-9)),
                    "hurt": int(sum(1 for d in cd if d > 1e-9)),
                }

        agg[method] = {
            "n_pairs": len(pairs),
            "median_delta_pi_ser": median_delta,        # negative = improvement
            "trimmed_mean_delta_pi_ser": trimmed_delta,
            "bootstrap_ci_95_median": [ci_lo, ci_hi],
            "help_count": help_n,
            "hurt_count": hurt_n,
            "tie_count": tie_n,
            "half_a_median_delta": half_a_med,
            "half_b_median_delta": half_b_med,
            "direction_consistent_across_halves": bool(direction_consistent),
            "per_cell": per_cell,
            "diagnostic_signal_gate": _eval_gate(method, agg_placeholder=None,
                                                 median_delta=median_delta,
                                                 help_n=help_n, hurt_n=hurt_n,
                                                 direction_consistent=direction_consistent,
                                                 per_cell=per_cell),
        }

    return {"constructs": agg, "method_order": METHOD_ORDER,
            "cells": cells, "seeds": seeds}


def stats_trimmed_mean(x: list[float], frac: float) -> float:
    arr = np.sort(np.asarray(x))
    n = len(arr)
    k = int(np.floor(n * frac))
    if 2 * k >= n:
        return float(np.mean(arr))
    return float(np.mean(arr[k:n - k])) if (n - k) > k else float(np.mean(arr))


def _eval_gate(method: str, *, agg_placeholder, median_delta, help_n, hurt_n,
               direction_consistent, per_cell) -> dict[str, Any]:
    """Evaluate the diagnostic signal gate (promotion screen)."""
    positive_median = median_delta < -1e-9   # improvement
    help_gt_hurt = help_n > hurt_n
    not_single_cell = sum(1 for c in per_cell.values() if c["median_delta"] < -1e-9) >= 2
    gate = {
        "positive_median": bool(positive_median),
        "help_gt_hurt": bool(help_gt_hurt),
        "direction_consistent": bool(direction_consistent),
        "not_single_cell": bool(not_single_cell),
    }
    passed = all(gate.values())
    gate["passed"] = bool(passed)
    gate["label"] = "DIAGNOSTIC_METHOD_SIGNAL" if passed else (
        "WEAK_DIAGNOSTIC_SIGNAL" if (positive_median and help_gt_hurt) else "NO_SIGNAL")
    return gate


def _write_result_json(agg: dict[str, Any], smoke: dict[str, Any], wall: float) -> None:
    constructs_built = ["M1_reduced_modulus", "M2_trace_reinit", "M3_multistart_select",
                        "M4_conditional_dd", "M5_radius_remap"]
    constructs_compared = [m for m in constructs_built
                           if agg["constructs"].get(m, {}).get("n_pairs", 0) > 0]
    winners = [m for m in constructs_compared
               if agg["constructs"][m]["diagnostic_signal_gate"]["passed"]]

    status = ("DIAGNOSTIC_METHOD_SIGNAL" if winners
              else ("BLOCKED_SHARED_TESTBED" if len(constructs_compared) < 3
                    else "NO_DIAGNOSTIC_SIGNAL"))
    delta = ("METHOD_SIGNAL" if winners
             else ("FAIR_COMPARISON_RUN" if len(constructs_compared) >= 3
                   else ("CONSTRUCT_CREATED" if constructs_built else "NONE")))

    result = {
        "status": status,
        "mission_method_delta": delta,
        "testbed_identity": {
            "source_entry": "cb1-modulation-generic-closure/baseline-atlas",
            "qpsk_regression_pi_ser": 0.0,
            "inherited_verdict": "PROBLEM_SURVIVES_CONVENTIONAL_BASELINE",
            "paired_realization": "generate_shared_realization_dp",
            "frozen_baseline": "standard_cma_godard_z (R2=1.32)",
            "primary_metric": "PI-SER (lower is better)",
            "cells": agg["cells"],
            "seeds": agg["seeds"],
        },
        "constructs_built": constructs_built,
        "constructs_compared": constructs_compared,
        "paired_results": agg["constructs"],
        "diagnostic_winners": winners,
        "smoke_results": smoke,
        "wall_seconds": wall,
        "claim_ceiling": "DIAGNOSTIC_ONLY_NOT_FORMAL_GW_MVE",
        "next_formal_action": None,
    }
    out = SPRINT_ROOT / "artifacts" / "result.v1.json"
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"\nWrote result: {out}")
    print(f"\n=== STATUS: {status} | mission_method_delta: {delta} ===")
    if winners:
        print(f"Diagnostic winners: {winners}")
    print("\nPer-construct summary (paired delta vs baseline, negative=improvement):")
    for m in constructs_compared:
        a = agg["constructs"][m]
        g = a["diagnostic_signal_gate"]
        print(f"  {m:24s} median_delta={a['median_delta_pi_ser']:+.4f} "
              f"help/hurt/tie={a['help_count']}/{a['hurt_count']}/{a['tie_count']} "
              f"dir_consist={g['direction_consistent']} -> {g['label']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--compare", action="store_true")
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()
    if not (args.smoke or args.compare or args.all):
        args.all = True

    # QPSK regression first (testbed identity)
    print("QPSK regression (testbed identity check)...")
    contract = {"frozen_common_axes": {**FROZEN_AXES, "r2_qpsk": 1.0},
                "statistical_sensitivity": {"minimum_detectable_effect": {"value": 0.005}},
                "covering_design": {"paired_seeds": [11]}}
    qpsk_cell = {"id": "qpsk-anchor", "modulation": "qpsk", "snr_db": 20.0,
                 "f_g_hz": 30.0, "sop_rate": 4.0e-6, "n_symbols": 512}
    qres = runner.run_cell(qpsk_cell, contract, generator=generate_shared_realization_dp,
                           evaluator=evaluator)
    assert qres["identity_gate_ok"], "QPSK identity gate FAILED"
    assert qres["decision"]["nearest_pi_ser"] == 0.0, "QPSK PI-SER != 0"
    print(f"  QPSK PI-SER={qres['decision']['nearest_pi_ser']:.6f} (PASS)\n")

    smoke = {}
    if args.smoke or args.all:
        smoke = smoke_tests()

    if args.compare or args.all:
        comp = fair_comparison()
        agg = aggregate(comp["raw_rows"])
        _write_result_json(agg, smoke, comp["wall_seconds"])


if __name__ == "__main__":
    main()
