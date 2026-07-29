"""Pre-formal Method Factory Sprint 003 — update-granularity CMA family.

Pipeline:
  Phase A — testbed identity gates (QPSK regression, eval-population identity,
            prefix-only freeze invariance, gradient-identity stamp check)
  Phase B — semantic smoke per construct (its own z, gradient identity, parity)
  Phase C1 — DEV freeze: tune comparator mu (grid) + candidate mu/granularity
             on dev cells × dev subseeds (prefix-only selection)
  Phase C2 — TEST fair paired comparison on test_seeds × 7 cells
  Phase D — seed-cluster aggregation + comparator-aware signal gate
  Phase E — ablation: block_size × mu / effective-update-budget for any winner

Critical contract properties (HARD):
  (1) comparator = tuned per-symbol Godard-with-z CMA (canonical, contains z);
      its gradient provenance is cb1_cell_runner.py:124-129. The scalar-error
      CMAEqualizer2x2 (missing z) is FORBIDDEN as the comparator.
  (2) every construct acts on RAW rX/rY and produces its OWN z (NOT z-only
      post-processing of the block-64 output).
  (3) all methods on the SAME paired (cell, seed) realization, SAME eval window.
  (4) smoke written into the SAME terminal result.json as compare (NOT clobbered).
  (5) 5-way terminal verdict (see _terminal_verdict).

Usage:
    python run_factory.py --phase identity
    python run_factory.py --phase smoke
    python run_factory.py --phase dev
    python run_factory.py --phase test
    python run_factory.py --phase ablation
    python run_factory.py --phase all
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
SPRINT_ROOT = SRC.parent                       # preformal-method-factory-sprint-003/
CB1_ROOT = SPRINT_ROOT.parent / "cb1-modulation-generic-closure"
BASELINE_ATLAS = CB1_ROOT / "baseline-atlas"
REPO_ROOT = HERE.parents[6]                    # worktree root
SIM_DIR = REPO_ROOT / "projects" / "simulation"

for p in (str(SIM_DIR), str(BASELINE_ATLAS), str(SRC)):
    if p not in sys.path:
        sys.path.insert(0, p)

from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402
import cb1_evaluator as evaluator  # noqa: E402
import cb1_cell_runner as runner  # noqa: E402
import methods as M  # noqa: E402


# ─── Frozen contract (mirrors factory-contract.v3.yaml) ──────────────────────
FROZEN_AXES = {
    "alpha": 4.2, "beta": 1.4, "block": 100, "t_s": 4.0e-10, "method": "gar",
    "cma_taps": 11, "r2_qam16": 1.32, "cma_block_size": 64,
    "affine_ridge": 1.0e-6, "constellation_amplitude_per_axis": 0.7071067811865475,
}

CELLS = [
    {"id": "16qam-snr05-nominal-short", "modulation": "qam16", "snr_db": 5.0,  "f_g_hz": 30.0,   "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr10-nominal-short", "modulation": "qam16", "snr_db": 10.0, "f_g_hz": 30.0,   "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr15-nominal-short", "modulation": "qam16", "snr_db": 15.0, "f_g_hz": 30.0,   "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr25-nominal-short", "modulation": "qam16", "snr_db": 25.0, "f_g_hz": 30.0,   "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr20-fg100-short",   "modulation": "qam16", "snr_db": 20.0, "f_g_hz": 100.0,  "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr10-fg100-long",    "modulation": "qam16", "snr_db": 10.0, "f_g_hz": 100.0,  "sop_rate": 4.0e-6, "n_symbols": 8192},
    {"id": "16qam-snr15-fg1000-long",   "modulation": "qam16", "snr_db": 15.0, "f_g_hz": 1000.0, "sop_rate": 4.0e-6, "n_symbols": 8192},
]

DEV_SEEDS = [181, 182, 183, 184, 185, 186, 187, 188, 189, 190]
TEST_SEEDS = [201, 202, 203, 204, 205, 206, 207, 208, 209, 210,
              211, 212, 213, 214, 215, 216, 217, 218, 219, 220]
FORBIDDEN_SEEDS = {71, 72, 73, 74, 75, 76, 77, 78, 79, 80}

# Seed-disjointness + contamination assertions (frozen before any run)
assert set(DEV_SEEDS).isdisjoint(set(TEST_SEEDS)), "LEAKAGE: dev/test overlap"
assert set(DEV_SEEDS).isdisjoint(FORBIDDEN_SEEDS), "LEAKAGE: dev uses contaminated 71-80"
assert set(TEST_SEEDS).isdisjoint(FORBIDDEN_SEEDS), "LEAKAGE: test uses contaminated 71-80"

R2_16QAM = 1.32
TAPS = 11
BS = 64
RIDGE = 1.0e-6
MU_ANCHOR = 3.0e-2     # inherited block-64 mu (FROZEN, NOT re-tuned)

# Method ids (terminal order)
METHOD_ORDER = [
    "block64_cma_mu0p03",                 # (a) inherited anchor
    "persymbol_cma_godard_with_z",        # (b) traditional comparator
    "block8_cma_godard_with_z",           # (c) smaller block
    "block16_cma_godard_with_z",          # (c) smaller block
    "sliding_window_recursive_cma",       # (d) recursive memory
    "oracle_affine_bound_KILL_ONLY",      # kill-only bound (offline)
]
COMPARATOR = "persymbol_cma_godard_with_z"
ANCHOR = "block64_cma_mu0p03"
CANDIDATES = ["block8_cma_godard_with_z", "block16_cma_godard_with_z",
              "sliding_window_recursive_cma"]

# Phase C1 dev grids (tiny, prefix-only; never sees test). Per-symbol/block mu
# is typically much smaller than block-64 mu because each update is full-strength.
COMPARATOR_MU_GRID = [1.0e-3, 3.0e-3, 1.0e-2, 3.0e-2, 1.0e-1]
BLOCK8_MU_GRID = [1.0e-3, 3.0e-3, 1.0e-2, 3.0e-2]
BLOCK16_MU_GRID = [1.0e-3, 3.0e-3, 1.0e-2, 3.0e-2]
RECURSIVE_MU_GRID = [3.0e-4, 1.0e-3, 3.0e-3, 1.0e-2]
RECURSIVE_LAM_GRID = [0.8, 0.9]


# ─── Realization + eval helpers ──────────────────────────────────────────────

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
        n_symbols, TAPS, window_symbols=256, block_size=BS)
    return es, cal, ee


def _eval_pred(predicted_x: np.ndarray, predicted_y: np.ndarray,
               truth_eval_x: np.ndarray, truth_eval_y: np.ndarray,
               bits_eval_x: np.ndarray, bits_eval_y: np.ndarray) -> dict[str, float]:
    m = evaluator.evaluate_dual_16qam(
        predicted_x, predicted_y, truth_eval_x, truth_eval_y, bits_eval_x, bits_eval_y)
    return {"pi_ser": float(m["pi_ser"]), "fixed_label_ser": float(m["fixed_label_ser"]),
            "pi_ber": float(m["pi_ber"])}


def _diverged_metrics() -> dict[str, Any]:
    return {"pi_ser": float("nan"), "fixed_label_ser": float("nan"),
            "pi_ber": float("nan"), "diverged": True}


# ─── Equalizer dispatch (each method produces its OWN z) ─────────────────────

def _equalize(method_id: str, realization: dict[str, Any], *,
              frozen_mu: dict[str, float],
              frozen_lam: dict[str, float] | None = None) -> dict[str, Any]:
    """Run ONE equalizer variant on raw rX/rY, return its zX/zY/diverged/provenance."""
    rX = realization["rX"]
    rY = realization["rY"]
    if method_id == "block64_cma_mu0p03":
        return M.block64_cma_mu0p03(rX, rY, n_tap=TAPS, mu=MU_ANCHOR,
                                    R2=R2_16QAM, block_size=BS)
    if method_id == "persymbol_cma_godard_with_z":
        return M.persymbol_cma_godard_with_z(rX, rY, n_tap=TAPS,
                                             mu=frozen_mu[method_id], R2=R2_16QAM)
    if method_id == "block8_cma_godard_with_z":
        return M.blockN_cma_godard_with_z(rX, rY, n_tap=TAPS,
                                          mu=frozen_mu[method_id], R2=R2_16QAM,
                                          block_size=8)
    if method_id == "block16_cma_godard_with_z":
        return M.blockN_cma_godard_with_z(rX, rY, n_tap=TAPS,
                                          mu=frozen_mu[method_id], R2=R2_16QAM,
                                          block_size=16)
    if method_id == "sliding_window_recursive_cma":
        lam = (frozen_lam or {}).get(method_id, 0.9)
        return M.sliding_window_recursive_cma(rX, rY, n_tap=TAPS,
                                              mu=frozen_mu[method_id], R2=R2_16QAM,
                                              lam=lam)
    raise ValueError(method_id)


# ─── Per-(cell,seed) paired runner ───────────────────────────────────────────

def run_all_on_realization(cell: dict[str, Any], seed: int, *,
                           frozen_mu: dict[str, float],
                           frozen_lam: dict[str, float] | None = None) -> dict[str, Any]:
    """Run anchor + comparator + candidates + kill-only bound on ONE shared
    realization. Every equalizer runs over the FULL signal; only [cal, ee) is
    scored. All methods share the SAME eval window."""
    n = int(cell["n_symbols"])
    es, cal, ee = _eval_window(n)
    realization = _realization(cell, seed)
    bits_per = 4
    truth_eval_x = realization["sX"][cal:ee]
    truth_eval_y = realization["sY"][cal:ee]
    bits_eval_x = realization["bitsX"][cal * bits_per:ee * bits_per]
    bits_eval_y = realization["bitsY"][cal * bits_per:ee * bits_per]

    out: dict[str, Any] = {"cell_id": cell["id"], "seed": int(seed), "n_symbols": n,
                           "eval_window": {"eval_start": es, "calibration_end": cal, "eval_end": ee},
                           "methods": {}}

    # ---- Equalizer methods (each its own z) --------------------------------
    for mid in (ANCHOR, COMPARATOR, *CANDIDATES):
        eq = _equalize(mid, realization, frozen_mu=frozen_mu, frozen_lam=frozen_lam)
        grad_ok = (eq.get("provenance", {}).get("gradient") == "Godard-with-z")
        if (not eq["diverged"]) and grad_ok:
            bx = np.asarray(evaluator.hard_16qam(eq["zX"][cal:ee]))
            by = np.asarray(evaluator.hard_16qam(eq["zY"][cal:ee]))
            m = _eval_pred(bx, by, truth_eval_x, truth_eval_y, bits_eval_x, bits_eval_y)
            m["diverged"] = False
            m["gradient_identity_ok"] = bool(grad_ok)
            out["methods"][mid] = m
        else:
            m = _diverged_metrics()
            m["gradient_identity_ok"] = bool(grad_ok)
            out["methods"][mid] = m

    # ---- Kill-only bound: oracle affine (TX-truth, NEVER a Go comparator) ---
    # Computed from the ANCHOR z-stream (block-64), consistent with cb1_cell_runner
    # run_cell convention (oracle applied to the nearest-decision z). Offline use
    # only: 4-category labelling + headroom.
    base_eq = _equalize(ANCHOR, realization, frozen_mu={ANCHOR: MU_ANCHOR})
    if not base_eq["diverged"]:
        z_calib = np.column_stack([base_eq["zX"][es:cal], base_eq["zY"][es:cal]])
        z_eval = np.column_stack([base_eq["zX"][cal:ee], base_eq["zY"][cal:ee]])
        truth_calib = np.column_stack([realization["sX"][es:cal],
                                       realization["sY"][es:cal]])
        oracle = evaluator.oracle_affine_bound_16qam(z_calib, z_eval, truth_calib, ridge=RIDGE)
        m = _eval_pred(oracle[:, 0], oracle[:, 1],
                       truth_eval_x, truth_eval_y, bits_eval_x, bits_eval_y)
        m["diverged"] = False
        out["methods"]["oracle_affine_bound_KILL_ONLY"] = m  # NEVER a Go comparator
    else:
        out["methods"]["oracle_affine_bound_KILL_ONLY"] = _diverged_metrics()

    return out


# ─── Phase A: identity gates ─────────────────────────────────────────────────

def phase_identity() -> dict[str, Any]:
    print("=" * 70)
    print("PHASE A: TESTBED IDENTITY GATES")
    print("=" * 70)
    res: dict[str, Any] = {}

    # Gate 1: QPSK regression (PI-SER = 0 at inherited mu=0.03)
    contract = {"frozen_common_axes": {**FROZEN_AXES, "r2_qpsk": 1.0,
                                       "cma_mu": MU_ANCHOR},
                "statistical_sensitivity": {"minimum_detectable_effect": {"value": 0.005}},
                "covering_design": {"paired_seeds": [181]}}
    qpsk_cell = {"id": "qpsk-anchor", "modulation": "qpsk", "snr_db": 20.0,
                 "f_g_hz": 30.0, "sop_rate": 4.0e-6, "n_symbols": 512}
    qres = runner.run_cell(qpsk_cell, contract, generator=generate_shared_realization_dp,
                           evaluator=evaluator)
    qpsk_pass = (qres["identity_gate_ok"]
                 and qres["decision"]["nearest_pi_ser"] == 0.0)
    res["qpsk_regression"] = {"pi_ser": float(qres["decision"]["nearest_pi_ser"]),
                              "identity_gate_ok": bool(qres["identity_gate_ok"]),
                              "pass": bool(qpsk_pass)}
    print(f"  QPSK regression: PI-SER={qres['decision']['nearest_pi_ser']:.6f} -> "
          f"{'PASS' if qpsk_pass else 'FAIL'}")

    # Gate 2: eval-population identity (all methods finite z on held-out cell/seed)
    cell = CELLS[0]
    frozen_mu = {COMPARATOR: 1.0e-3, "block8_cma_godard_with_z": 3.0e-3,
                 "block16_cma_godard_with_z": 3.0e-3,
                 "sliding_window_recursive_cma": 1.0e-3}
    frozen_lam = {"sliding_window_recursive_cma": 0.9}
    out = run_all_on_realization(cell, DEV_SEEDS[0], frozen_mu=frozen_mu, frozen_lam=frozen_lam)
    pop_ok = all((not out["methods"][m].get("diverged", True))
                 and np.isfinite(out["methods"][m].get("pi_ser", float("nan")))
                 for m in (ANCHOR, COMPARATOR, *CANDIDATES))
    res["eval_population_identity"] = {
        "anchor_diverged": bool(out["methods"][ANCHOR].get("diverged", True)),
        "comparator_diverged": bool(out["methods"][COMPARATOR].get("diverged", True)),
        "pass": bool(pop_ok)}
    print(f"  Eval population identity: anchor_div={out['methods'][ANCHOR].get('diverged')} "
          f"comp_div={out['methods'][COMPARATOR].get('diverged')} -> {'PASS' if pop_ok else 'FAIL'}")

    # Gate 3: prefix-only freeze invariance — re-running on the SAME raw input
    # yields bit-identical z (equalizers are deterministic; no suffix-dependent
    # selection enters them). mu/granularity frozen on dev, applied unchanged.
    es, cal, ee = _eval_window(cell["n_symbols"])
    realization = _realization(cell, DEV_SEEDS[0])
    invariance_ok = True
    for mid in (COMPARATOR, *CANDIDATES):
        eq1 = _equalize(mid, realization, frozen_mu=frozen_mu, frozen_lam=frozen_lam)
        eq2 = _equalize(mid, realization, frozen_mu=frozen_mu, frozen_lam=frozen_lam)
        z1 = eq1["zX"][cal:ee]
        z2 = eq2["zX"][cal:ee]
        if not np.array_equal(z1, z2):
            invariance_ok = False
            break
    res["prefix_only_freeze_invariance"] = {"pass": bool(invariance_ok)}
    print(f"  Prefix-only freeze invariance: -> {'PASS' if invariance_ok else 'FAIL'}")

    # Gate 4: gradient identity — comparator + candidates all stamp Godard-with-z
    grad_ok = True
    for mid in (ANCHOR, COMPARATOR, *CANDIDATES):
        eq = _equalize(mid, realization, frozen_mu=frozen_mu, frozen_lam=frozen_lam)
        g = eq.get("provenance", {}).get("gradient")
        if g != "Godard-with-z":
            grad_ok = False
            break
    res["gradient_identity"] = {"comparator_and_candidates_godard_with_z": bool(grad_ok),
                                "pass": bool(grad_ok)}
    print(f"  Gradient identity (all Godard-with-z): -> {'PASS' if grad_ok else 'FAIL'}")

    all_pass = qpsk_pass and pop_ok and invariance_ok and grad_ok
    res["all_gates_pass"] = bool(all_pass)
    print(f"\n=== PHASE A: {'ALL PASS' if all_pass else 'BLOCKED'} ===\n")
    return res


# ─── Phase B: semantic smoke ─────────────────────────────────────────────────

def phase_smoke() -> dict[str, Any]:
    print("=" * 70)
    print("PHASE B: SEMANTIC SMOKE (per construct)")
    print("=" * 70)
    results: dict[str, Any] = {}
    cell = CELLS[0]
    frozen_mu = {COMPARATOR: 1.0e-3, "block8_cma_godard_with_z": 3.0e-3,
                 "block16_cma_godard_with_z": 3.0e-3,
                 "sliding_window_recursive_cma": 1.0e-3}
    frozen_lam = {"sliding_window_recursive_cma": 0.9}

    for seed in (DEV_SEEDS[0], DEV_SEEDS[1]):
        realization = _realization(cell, seed)
        es, cal, ee = _eval_window(cell["n_symbols"])

        # (i) Each construct produces its OWN z (distinct from anchor z, unless
        #     it degenerates). Action identity: per-symbol z != block-64 z on
        #     the scored suffix.
        base = M.block64_cma_mu0p03(realization["rX"], realization["rY"], n_tap=TAPS,
                                    mu=MU_ANCHOR, R2=R2_16QAM, block_size=BS)
        if base["diverged"]:
            continue
        for mid in (COMPARATOR, *CANDIDATES):
            eq = _equalize(mid, realization, frozen_mu=frozen_mu, frozen_lam=frozen_lam)
            distinct = bool(not np.allclose(eq["zX"][cal:ee], base["zX"][cal:ee], atol=1e-12))
            grad_ok = bool(eq.get("provenance", {}).get("gradient") == "Godard-with-z")
            results.setdefault(mid, {})[f"seed_{seed}_z_distinct_from_anchor"] = distinct
            results.setdefault(mid, {})[f"seed_{seed}_gradient_godard_with_z"] = grad_ok
            results.setdefault(mid, {})[f"seed_{seed}_diverged"] = bool(eq["diverged"])

        # (ii) Identity-determinism: same raw input -> bit-identical z
        for mid in (COMPARATOR, *CANDIDATES):
            a = _equalize(mid, realization, frozen_mu=frozen_mu, frozen_lam=frozen_lam)
            b = _equalize(mid, realization, frozen_mu=frozen_mu, frozen_lam=frozen_lam)
            det = bool(np.array_equal(a["zX"][cal:ee], b["zX"][cal:ee]))
            results.setdefault(mid, {})[f"seed_{seed}_deterministic_z"] = det

    print(f"  smoke completed for {len(CANDIDATES)+1} constructs (anchor excluded; 2 seeds)")
    print(f"\n=== PHASE B: SMOKE COMPLETE ===\n")
    return results


# ─── Phase C1: dev freeze (tune comparator mu + candidate mu/granularity) ────

def phase_dev_freeze() -> dict[str, Any]:
    print("=" * 70)
    print("PHASE C1: DEV FREEZE (tune comparator mu + candidate mu/granularity)")
    print(f"  cells: {[CELLS[0]['id'], CELLS[1]['id'], CELLS[4]['id']]}")
    print(f"  dev_subseeds: {DEV_SEEDS[:3]}")
    print("=" * 70)

    dev_cells = [CELLS[0], CELLS[1], CELLS[4]]   # snr05, snr10, snr20-fg100 (all short)
    dev_subseeds = DEV_SEEDS[:3]                 # 181, 182, 183

    frozen_mu: dict[str, float] = {ANCHOR: MU_ANCHOR}
    tuning_trace: dict[str, Any] = {}

    # ---- Comparator mu grid (minimize seed-cluster mean PI-SER over dev) -----
    best_comp_mu, best_comp_score = None, float("inf")
    for mu in COMPARATOR_MU_GRID:
        pis = []
        for cell in dev_cells:
            for seed in dev_subseeds:
                out = run_all_on_realization(cell, seed,
                                             frozen_mu={COMPARATOR: mu, ANCHOR: MU_ANCHOR,
                                                        **{c: 3e-3 for c in CANDIDATES}})
                v = out["methods"][COMPARATOR]["pi_ser"]
                if np.isfinite(v):
                    pis.append(v)
        score = float(np.mean(pis)) if pis else float("inf")
        tuning_trace.setdefault(COMPARATOR, {})[str(mu)] = score
        print(f"  {COMPARATOR} mu={mu}: dev mean PI-SER={score:.5f} (n={len(pis)})")
        if score < best_comp_score:
            best_comp_score, best_comp_mu = score, mu
    frozen_mu[COMPARATOR] = best_comp_mu
    print(f"  -> {COMPARATOR} frozen mu={best_comp_mu}")

    # ---- Candidate mu grids (each candidate vs COMPARATOR at its frozen mu) ---
    # The signal gate is comparator-aware, so we tune candidates to minimize
    # PI-SER on dev (the comparator is already frozen; dev-optimal candidate mu).
    candidate_grids = {
        "block8_cma_godard_with_z": BLOCK8_MU_GRID,
        "block16_cma_godard_with_z": BLOCK16_MU_GRID,
        "sliding_window_recursive_cma": RECURSIVE_MU_GRID,
    }
    for cand, grid in candidate_grids.items():
        best_mu, best_score = None, float("inf")
        for mu in grid:
            pis = []
            for cell in dev_cells:
                for seed in dev_subseeds:
                    fm = {**frozen_mu, ANCHOR: MU_ANCHOR, cand: mu}
                    for c in CANDIDATES:
                        fm.setdefault(c, 3e-3)
                    out = run_all_on_realization(cell, seed, frozen_mu=fm,
                                                 frozen_lam={"sliding_window_recursive_cma": 0.9})
                    v = out["methods"][cand]["pi_ser"]
                    if np.isfinite(v):
                        pis.append(v)
            score = float(np.mean(pis)) if pis else float("inf")
            tuning_trace.setdefault(cand, {})[str(mu)] = score
            print(f"  {cand} mu={mu}: dev mean PI-SER={score:.5f} (n={len(pis)})")
            if score < best_score:
                best_score, best_mu = score, mu
        frozen_mu[cand] = best_mu
        print(f"  -> {cand} frozen mu={best_mu}")

    frozen_lam = {"sliding_window_recursive_cma": 0.9}

    receipt = {
        "frozen_mu": {k: float(v) for k, v in frozen_mu.items()},
        "frozen_lam": frozen_lam,
        "dev_cells": [c["id"] for c in dev_cells],
        "dev_subseeds": dev_subseeds,
        "tuning_trace": tuning_trace,
        "comparator_provenance": {
            "gradient": "Godard-with-z",
            "entry": "per-symbol standard-CMA (canonical Godard-with-z)",
            "gradient_provenance": "cb1_cell_runner.py:124-129",
        },
        "note": "Frozen from prefix-only dev pool; test seeds never observed.",
    }
    out = SPRINT_ROOT / "artifacts" / "dev-freeze-receipt.v1.json"
    out.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(f"\nWrote dev freeze receipt: {out}")
    print(f"\n=== PHASE C1: DEV FROZEN ===\n")
    return receipt


# ─── Phase C2: test paired comparison ────────────────────────────────────────

def phase_test_compare(dev_receipt: dict[str, Any]) -> dict[str, Any]:
    print("=" * 70)
    print("PHASE C2: TEST PAIRED COMPARISON (seed-cluster)")
    print(f"  cells: {[c['id'] for c in CELLS]}")
    print(f"  test_seeds: {TEST_SEEDS}")
    print("=" * 70)

    frozen_mu = {k: float(v) for k, v in dev_receipt["frozen_mu"].items()}
    frozen_lam = dev_receipt.get("frozen_lam", {"sliding_window_recursive_cma": 0.9})
    for m in METHOD_ORDER:
        if m not in frozen_mu and m not in ("oracle_affine_bound_KILL_ONLY",):
            frozen_mu.setdefault(m, MU_ANCHOR)

    raw_rows: list[dict[str, Any]] = []
    per_cell_oracle_label: dict[str, dict[str, Any]] = {}
    t0 = time.time()
    for ci, cell in enumerate(CELLS):
        for seed in TEST_SEEDS:
            out = run_all_on_realization(cell, seed, frozen_mu=frozen_mu, frozen_lam=frozen_lam)
            for mname, mres in out["methods"].items():
                pis = mres.get("pi_ser")
                raw_rows.append({
                    "cell_id": out["cell_id"], "seed": out["seed"], "method": mname,
                    "pi_ser": (None if pis is None or not np.isfinite(pis) else float(pis)),
                    "fixed_label_ser": (None if (v := mres.get("fixed_label_ser")) is None or not np.isfinite(v) else float(v)),
                    "pi_ber": (None if (v := mres.get("pi_ber")) is None or not np.isfinite(v) else float(v)),
                    "diverged": bool(mres.get("diverged", False)),
                })
            per_cell_oracle_label.setdefault(cell["id"], _offline_label(out))
        print(f"  [{ci+1}/{len(CELLS)}] {cell['id']:28s} done ({time.time()-t0:.1f}s)")

    csv_path = SPRINT_ROOT / "artifacts" / "raw-rows.v3.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["cell_id", "seed", "method", "pi_ser",
                                          "fixed_label_ser", "pi_ber", "diverged"])
        w.writeheader()
        for row in raw_rows:
            w.writerow(row)
    print(f"\nWrote raw rows: {csv_path} ({len(raw_rows)} rows)")

    return {"raw_rows": raw_rows, "per_cell_oracle_label": per_cell_oracle_label,
            "wall_seconds": time.time() - t0, "frozen_mu": frozen_mu,
            "frozen_lam": frozen_lam}


def _offline_label(out: dict[str, Any]) -> dict[str, Any]:
    """4-category collapse label from oracle/anchor (LABEL ONLY)."""
    b = out["methods"].get(ANCHOR, {}).get("pi_ser")
    o = out["methods"].get("oracle_affine_bound_KILL_ONLY", {}).get("pi_ser")
    if b is None or o is None or not np.isfinite(b) or not np.isfinite(o):
        return {"category": "ambiguous"}
    if b < 0.1:
        return {"category": "healthy", "baseline_pi_ser": float(b)}
    if (b - o) < 0.005:
        return {"category": "awgn_dominated_error", "baseline_pi_ser": float(b),
                "oracle_pi_ser": float(o)}
    if o < 0.1:
        return {"category": "inner_ring_recoverable_collapse", "baseline_pi_ser": float(b),
                "oracle_pi_ser": float(o)}
    return {"category": "ambiguous", "baseline_pi_ser": float(b), "oracle_pi_ser": float(o)}


# ─── Seed-cluster aggregation (comparator-aware) ─────────────────────────────

def aggregate_seed_cluster(raw_rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Each SEED is ONE cluster. Per-seed mean PI-SER over the 7 cells; per-seed
    paired delta vs the TUNED PER-SYMBOL COMPARATOR (signal gate) AND vs the
    inherited ANCHOR (context)."""
    cells = sorted({r["cell_id"] for r in raw_rows})
    seeds = sorted({r["seed"] for r in raw_rows})

    idx: dict[tuple[str, int, str], float | None] = {}
    for r in raw_rows:
        idx[(r["cell_id"], r["seed"], r["method"])] = r["pi_ser"]

    seed_method_mean: dict[tuple[int, str], float] = {}
    for s in seeds:
        for m in METHOD_ORDER:
            vals = [idx[(c, s, m)] for c in cells if idx.get((c, s, m)) is not None]
            vals = [v for v in vals if v is not None]
            seed_method_mean[(s, m)] = float(np.mean(vals)) if vals else float("nan")

    # Seed-cluster mean per method (mean over seeds of per-seed mean)
    method_cluster_mean: dict[str, float] = {}
    for m in METHOD_ORDER:
        vals = [seed_method_mean.get((s, m), float("nan")) for s in seeds]
        vals = [v for v in vals if np.isfinite(v)]
        method_cluster_mean[m] = float(np.mean(vals)) if vals else float("nan")

    comparator_mean = method_cluster_mean.get(COMPARATOR, float("nan"))
    anchor_mean = method_cluster_mean.get(ANCHOR, float("nan"))

    constructs_agg: dict[str, Any] = {}
    for m in (COMPARATOR, *CANDIDATES):
        ref = comparator_mean if m != COMPARATOR else anchor_mean
        ref_id = COMPARATOR if m != COMPARATOR else ANCHOR
        deltas = []
        for s in seeds:
            mv = seed_method_mean.get((s, m), float("nan"))
            rv = seed_method_mean.get((s, ref_id), float("nan"))
            if np.isfinite(mv) and np.isfinite(rv):
                deltas.append(float(mv - rv))
        if not deltas:
            constructs_agg[m] = {"n_seeds": 0}
            continue
        help_n = sum(1 for d in deltas if d < -1e-9)
        hurt_n = sum(1 for d in deltas if d > 1e-9)
        tie_n = sum(1 for d in deltas if abs(d) <= 1e-9)
        mean_d = float(np.mean(deltas))
        ci_lo, ci_hi = _cluster_bootstrap_ci(deltas)
        # Healthy-cluster regression (anchor PI-SER < 0.1 cells), vs the same ref
        healthy_deltas = []
        for s in seeds:
            for c in cells:
                ab = idx.get((c, s, ANCHOR))
                mv = idx.get((c, s, m))
                rv = idx.get((c, s, ref_id))
                if (ab is not None and mv is not None and rv is not None and ab < 0.1):
                    healthy_deltas.append(mv - rv)
        healthy_worst_d = float(np.max(healthy_deltas)) if healthy_deltas else float("nan")
        gate = _signal_gate(m, mean_d, ci_hi, help_n, hurt_n, healthy_worst_d,
                            method_cluster_mean[m], comparator_mean)
        constructs_agg[m] = {
            "n_seeds": len(deltas),
            "reference": ref_id,
            "seed_cluster_mean_delta_pi_ser_vs_ref": mean_d,
            "seed_cluster_bootstrap_ci_95_vs_ref": [ci_lo, ci_hi],
            "help_seeds": help_n, "hurt_seeds": hurt_n, "tie_seeds": tie_n,
            "healthy_cluster_worst_delta_pi_ser_vs_ref": healthy_worst_d,
            "method_seed_cluster_mean_pi_ser": method_cluster_mean[m],
            "diagnostic_signal_gate": gate,
        }

    # Per-cell heterogeneity (descriptive: per-cell mean PI-SER per method)
    per_cell: dict[str, dict[str, Any]] = {}
    for c in cells:
        per_cell[c] = {}
        for m in (ANCHOR, COMPARATOR, *CANDIDATES, "oracle_affine_bound_KILL_ONLY"):
            vals = [idx.get((c, s, m)) for s in seeds if idx.get((c, s, m)) is not None]
            vals = [v for v in vals if v is not None]
            if vals:
                per_cell[c][m] = {"n_seeds": len(vals), "mean_pi_ser": float(np.mean(vals))}

    return {"constructs": constructs_agg, "per_cell": per_cell,
            "method_seed_cluster_mean_pi_ser": method_cluster_mean,
            "comparator_seed_cluster_mean_pi_ser": comparator_mean,
            "anchor_seed_cluster_mean_pi_ser": anchor_mean,
            "seeds": seeds, "cells": cells}


def _cluster_bootstrap_ci(deltas: list[float], n_boot: int = 10000,
                          seed: int = 42) -> tuple[float, float]:
    if len(deltas) < 2:
        return (float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    arr = np.asarray(deltas)
    boots = [float(np.mean(rng.choice(arr, size=len(arr), replace=True)))
             for _ in range(n_boot)]
    return (float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5)))


def _signal_gate(method_id: str, mean_d: float, ci_hi: float, help_n: int,
                 hurt_n: int, healthy_worst_d: float,
                 method_mean: float, comparator_mean: float) -> dict[str, Any]:
    """Comparator-aware signal gate. For CANDIDATES the reference IS the tuned
    per-symbol comparator; for the COMPARATOR itself the reference is the anchor
    (context only — the comparator beating the anchor is NOT a candidate signal)."""
    MDE = 0.005
    is_candidate = method_id in CANDIDATES
    sig_mean = mean_d <= -MDE
    ci_upper_neg = (ci_hi < 0) if np.isfinite(ci_hi) else False
    help_gt_hurt = help_n > hurt_n
    no_healthy_catastrophe = (healthy_worst_d <= MDE
                              if np.isfinite(healthy_worst_d) else False)
    if is_candidate:
        strong = sig_mean and ci_upper_neg and help_gt_hurt and no_healthy_catastrophe
        label = "DIAGNOSTIC_METHOD_SIGNAL" if strong else "NO_SIGNAL_vs_comparator"
    else:
        # Comparator vs anchor is descriptive context, not a candidate signal.
        label = "COMPARATOR_CONTEXT_vs_anchor"
    return {"reference_is_comparator": is_candidate,
            "seed_cluster_mean_le_neg_MDE": bool(sig_mean),
            "ci_upper_lt_0": bool(ci_upper_neg),
            "help_gt_hurt": bool(help_gt_hurt),
            "no_catastrophic_regression_on_healthy": bool(no_healthy_catastrophe),
            "label": label}


# ─── Collapse-removal check (for PROBLEM_RESOLVED verdict) ───────────────────

def collapse_removal_check(raw_rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Did the tuned per-symbol comparator remove the block-64 collapse?
    A cell 'collapses' under the anchor if its per-seed mean anchor PI-SER >= 0.1.
    The comparator 'removes' it if that cell's per-seed mean comparator PI-SER < 0.1."""
    cells = sorted({r["cell_id"] for r in raw_rows})
    seeds = sorted({r["seed"] for r in raw_rows})
    idx: dict[tuple[str, int, str], float | None] = {}
    for r in raw_rows:
        idx[(r["cell_id"], r["seed"], r["method"])] = r["pi_ser"]
    per_cell_anchor = {}
    per_cell_comp = {}
    collapse_cells = []
    removed_cells = []
    for c in cells:
        a_vals = [idx.get((c, s, ANCHOR)) for s in seeds if idx.get((c, s, ANCHOR)) is not None]
        c_vals = [idx.get((c, s, COMPARATOR)) for s in seeds if idx.get((c, s, COMPARATOR)) is not None]
        a_mean = float(np.mean(a_vals)) if a_vals else float("nan")
        c_mean = float(np.mean(c_vals)) if c_vals else float("nan")
        per_cell_anchor[c] = a_mean
        per_cell_comp[c] = c_mean
        if np.isfinite(a_mean) and a_mean >= 0.1:
            collapse_cells.append(c)
            if np.isfinite(c_mean) and c_mean < 0.1:
                removed_cells.append(c)
    return {
        "per_cell_anchor_pi_ser": per_cell_anchor,
        "per_cell_comparator_pi_ser": per_cell_comp,
        "collapse_cells_under_anchor": collapse_cells,
        "collapse_cells_removed_by_comparator": removed_cells,
        "comparator_removes_all_anchor_collapses": (
            len(removed_cells) == len(collapse_cells) and len(collapse_cells) > 0),
    }


# ─── Phase E: ablation (block_size × mu / effective-update-budget) ───────────

def phase_ablation(dev_receipt: dict[str, Any], agg: dict[str, Any],
                   collapse: dict[str, Any]) -> dict[str, Any]:
    print("=" * 70)
    print("PHASE E: ABLATION (granularity vs more-updates vs tuning)")
    print("=" * 70)
    # Identify the best candidate (lowest seed-cluster mean PI-SER) if any.
    cand_means = {m: agg["method_seed_cluster_mean_pi_ser"].get(m, float("inf"))
                  for m in CANDIDATES}
    comp_mean = agg["comparator_seed_cluster_mean_pi_ser"]
    best_cand = min(cand_means, key=cand_means.get) if cand_means else None
    best_delta_vs_comp = None
    if best_cand is not None:
        best_delta_vs_comp = (cand_means[best_cand] - comp_mean
                              if np.isfinite(cand_means[best_cand]) and np.isfinite(comp_mean)
                              else float("nan"))

    print(f"  comparator seed-cluster mean PI-SER: {comp_mean:.5f}")
    for m in CANDIDATES:
        d = (cand_means[m] - comp_mean) if np.isfinite(cand_means[m]) and np.isfinite(comp_mean) else float("nan")
        print(f"  {m}: mean={cand_means[m]:.5f}  delta_vs_comp={d:+.5f}")
    print(f"  best candidate: {best_cand} (delta_vs_comp={best_delta_vs_comp:+.5f})")

    ablation: dict[str, Any] = {
        "comparator_seed_cluster_mean_pi_ser": float(comp_mean) if np.isfinite(comp_mean) else None,
        "candidate_seed_cluster_mean_pi_ser": {m: (float(v) if np.isfinite(v) else None)
                                               for m, v in cand_means.items()},
        "best_candidate": best_cand,
        "best_candidate_delta_vs_comparator": (float(best_delta_vs_comp)
                                               if best_delta_vs_comp is not None
                                               and np.isfinite(best_delta_vs_comp) else None),
    }

    # Effective-update-budget table (mechanism fingerprint, no re-run needed).
    updates = {
        "block64_cma_mu0p03": M.updates_per_symbol("block_end_averaged", 64),
        "block16_cma_godard_with_z": M.updates_per_symbol("block_end_averaged", 16),
        "block8_cma_godard_with_z": M.updates_per_symbol("block_end_averaged", 8),
        "persymbol_cma_godard_with_z": M.updates_per_symbol("per_symbol"),
        "sliding_window_recursive_cma": M.updates_per_symbol("per_symbol"),
    }
    ablation["updates_per_symbol"] = updates

    # Matched-budget test: does a block-64 CMA at a mu that makes its EFFECTIVE
    # per-symbol step comparable already tie the best candidate? We approximate
    # "matched effective update budget" by sweeping the block-64 mu on a short
    # dev cell and checking whether block-64 can reach the best candidate's dev
    # PI-SER. If yes, the win is "more-updates", not granularity.
    if best_cand is not None and best_delta_vs_comp is not None and best_delta_vs_comp < -0.005:
        print("  Winner detected vs comparator -> running matched-budget block-64 sweep on dev")
        dev_cells = [CELLS[0], CELLS[1], CELLS[4]]
        dev_subseeds = DEV_SEEDS[:3]
        # Sweep block-64 mu widely (it is NOT the frozen anchor here; it is an
        # ablation probe allowed to use ANY mu to match the candidate budget).
        probe_mus = [1e-3, 3e-3, 1e-2, 3e-2, 1e-1, 3e-1, 1.0]
        best_b64_probe = float("inf")
        for mu in probe_mus:
            pis = []
            for cell in dev_cells:
                for seed in dev_subseeds:
                    realization = _realization(cell, seed)
                    eq = M.block64_cma_mu0p03(realization["rX"], realization["rY"],
                                              n_tap=TAPS, mu=mu, R2=R2_16QAM, block_size=BS)
                    if not eq["diverged"]:
                        es, cal, ee = _eval_window(cell["n_symbols"])
                        bx = np.asarray(evaluator.hard_16qam(eq["zX"][cal:ee]))
                        by = np.asarray(evaluator.hard_16qam(eq["zY"][cal:ee]))
                        bits_per = 4
                        m = _eval_pred(bx, by, realization["sX"][cal:ee], realization["sY"][cal:ee],
                                       realization["bitsX"][cal*bits_per:ee*bits_per],
                                       realization["bitsY"][cal*bits_per:ee*bits_per])
                        pis.append(m["pi_ser"])
            score = float(np.mean(pis)) if pis else float("inf")
            print(f"    block-64 probe mu={mu}: dev mean PI-SER={score:.5f}")
            if score < best_b64_probe:
                best_b64_probe = score
        # Best candidate dev PI-SER
        cand_dev_pis = []
        fm = {**dev_receipt["frozen_mu"]}
        for cell in dev_cells:
            for seed in dev_subseeds:
                out = run_all_on_realization(cell, seed, frozen_mu=fm,
                                             frozen_lam=dev_receipt.get("frozen_lam", {}))
                v = out["methods"][best_cand]["pi_ser"]
                if np.isfinite(v):
                    cand_dev_pis.append(v)
        cand_dev_mean = float(np.mean(cand_dev_pis)) if cand_dev_pis else float("inf")
        # If block-64 at its best probed mu reaches within MDE of the candidate,
        # the win is explained by "more-updates/tuning", not granularity.
        matched = (best_b64_probe <= cand_dev_mean + 0.005)
        ablation["matched_budget_block64_dev_mean_pi_ser"] = best_b64_probe
        ablation["best_candidate_dev_mean_pi_ser"] = cand_dev_mean
        ablation["matched_budget_block64_ties_candidate"] = bool(matched)
        if matched:
            ablation["win_explanation"] = "more_updates_or_tuning"
        else:
            ablation["win_explanation"] = "granularity"
        print(f"  -> matched block-64 dev mean={best_b64_probe:.5f}, candidate dev mean={cand_dev_mean:.5f}, "
              f"ties={matched} -> {ablation['win_explanation']}")
    else:
        ablation["win_explanation"] = "no_winner_vs_comparator"

    print(f"\n=== PHASE E: ABLATION DONE ===\n")
    return ablation


# ─── Terminal result + 5-way verdict ─────────────────────────────────────────

def _terminal_verdict(identity: dict, agg: dict, collapse: dict,
                      ablation: dict) -> tuple[str, str]:
    """5-way verdict per contract §2.4."""
    if not identity.get("all_gates_pass"):
        return "BLOCKED_SHARED_TESTBED", "identity gates did not pass"

    # Is the comparator gradient identity valid? (defensive — gate 4 already checks)
    # (handled by gate; if we got here it passed.)

    # Did the comparator remove the anchor collapse?
    comp_removes = bool(collapse.get("comparator_removes_all_anchor_collapses"))
    n_collapse = len(collapse.get("collapse_cells_under_anchor", []))

    # Does any candidate stably beat the comparator?
    winners = [m for m in CANDIDATES
               if agg["constructs"].get(m, {}).get("diagnostic_signal_gate", {}).get("label")
               == "DIAGNOSTIC_METHOD_SIGNAL"]

    if winners:
        # A winner exists vs comparator. Ablation must rule out artifacts.
        win_exp = ablation.get("win_explanation", "no_winner_vs_comparator")
        if win_explanation_is_artifact(win_exp):
            # Artifact-explained win is NOT a signal.
            if comp_removes or n_collapse == 0:
                return ("PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR",
                        "winner(s) advantage explained by "
                        f"{win_exp}; comparator {'removed' if comp_removes else 'saw no'} collapse")
            return ("NO_DIAGNOSTIC_SIGNAL",
                    f"winner(s) {winners} advantage explained by {win_exp} "
                    "(artifact), comparator did not remove collapse")
        return ("DIAGNOSTIC_METHOD_SIGNAL",
                f"winner(s) {winners} stably beat comparator; ablation ruled out artifacts")

    # No winner vs comparator.
    if comp_removes or n_collapse == 0:
        return ("PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR",
                f"tuned per-symbol Godard-with-z CMA "
                f"{'removed all ' + str(n_collapse) + ' collapse cells' if comp_removes else 'saw no collapse'}; "
                "no construct stably beats it")
    return ("NO_DIAGNOSTIC_SIGNAL",
            "no construct stably beats the tuned per-symbol comparator, "
            "and the comparator did NOT remove the collapse")


def win_explanation_is_artifact(win_exp: str) -> bool:
    return win_exp in ("more_updates_or_tuning", "tuning", "more_updates")


def write_terminal_result(*, identity: dict, smoke: dict, dev_receipt: dict,
                          agg: dict, collapse: dict, ablation: dict,
                          wall: float, oracle_labels: dict) -> str:
    verdict, rationale = _terminal_verdict(identity, agg, collapse, ablation)
    result = {
        "terminal_verdict": verdict,
        "verdict_rationale": rationale,
        "claim_ceiling": "DIAGNOSTIC_ONLY_NOT_FORMAL_GW_MVE",
        "testbed_identity": {
            "source_entry": "cb1-modulation-generic-closure/baseline-atlas",
            "inherited_anchor": "block64_cma_mu0p03 (mu=0.03 FROZEN, NOT re-tuned)",
            "traditional_comparator": "persymbol_cma_godard_with_z (canonical Godard-with-z, provenance cb1_cell_runner.py:124-129)",
            "forbidden_as_comparator": "common/_cma.py CMAEqualizer2x2 (scalar-error, missing z factor)",
            "qpsk_regression_pi_ser": identity.get("qpsk_regression", {}).get("pi_ser"),
            "paired_realization": "generate_shared_realization_dp",
            "cells": agg.get("cells"), "test_seeds": agg.get("seeds"),
            "dev_seeds": DEV_SEEDS,
        },
        "constructs_built": [ANCHOR, COMPARATOR, *CANDIDATES],
        "constructs_compared": [m for m in (COMPARATOR, *CANDIDATES)
                                if agg["constructs"].get(m, {}).get("n_seeds", 0) > 0],
        "comparator_aware_paired_results": agg["constructs"],
        "per_cell_pi_ser": agg["per_cell"],
        "method_seed_cluster_mean_pi_ser": agg["method_seed_cluster_mean_pi_ser"],
        "comparator_seed_cluster_mean_pi_ser": agg["comparator_seed_cluster_mean_pi_ser"],
        "anchor_seed_cluster_mean_pi_ser": agg["anchor_seed_cluster_mean_pi_ser"],
        "collapse_removal_check": collapse,
        "ablation": ablation,
        "diagnostic_winners_vs_comparator": [m for m in CANDIDATES
                                             if agg["constructs"].get(m, {}).get("diagnostic_signal_gate", {}).get("label")
                                             == "DIAGNOSTIC_METHOD_SIGNAL"],
        "smoke_results": smoke,                 # NOT clobbered (V052 fix)
        "identity_gate_results": identity,      # NOT clobbered
        "dev_freeze_receipt": dev_receipt,
        "offline_4category_labels": oracle_labels,
        "wall_seconds": wall,
        "next_formal_action": None,
    }
    out = SPRINT_ROOT / "artifacts" / "result.v3.json"
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"\nWrote terminal result: {out}")
    print(f"\n=== TERMINAL VERDICT: {verdict} ===")
    print(f"    rationale: {rationale}")
    print("\nComparator-aware per-construct (seed-cluster mean ΔPI-SER vs ref, negative=improvement):")
    for m in (COMPARATOR, *CANDIDATES):
        a = agg["constructs"].get(m, {})
        if a.get("n_seeds", 0) == 0:
            continue
        ci = a.get("seed_cluster_bootstrap_ci_95_vs_ref", [float("nan"), float("nan")])
        g = a.get("diagnostic_signal_gate", {})
        print(f"  {m:32s} ref={a.get('reference'):28s} mean_d={a.get('seed_cluster_mean_delta_pi_ser_vs_ref', float('nan')):+.5f} "
              f"CI=[{ci[0]:+.5f},{ci[1]:+.5f}] help/hurt/tie={a.get('help_seeds')}/{a.get('hurt_seeds')}/{a.get('tie_seeds')} -> {g.get('label')}")
    print(f"\nCollapse removal: anchor collapse cells={collapse.get('collapse_cells_under_anchor')}; "
          f"removed by comparator={collapse.get('collapse_cells_removed_by_comparator')}")
    return verdict


# ─── Prefix receipt (freeze provenance) ──────────────────────────────────────

def write_prefix_receipt(identity: dict) -> None:
    receipt = {
        "frozen_common_axes": FROZEN_AXES,
        "cells": [c["id"] for c in CELLS],
        "dev_seeds": DEV_SEEDS,
        "test_seeds": TEST_SEEDS,
        "forbidden_seeds": sorted(FORBIDDEN_SEEDS),
        "eval_window_geometry": {
            "n512": list(_eval_window(512)),
            "n8192": list(_eval_window(8192)),
        },
        "inherited_anchor_mu": MU_ANCHOR,
        "comparator_gradient_provenance": "cb1_cell_runner.py:124-129 (Godard-with-z, per-symbol analogue drops mean)",
        "identity_gate_summary": {k: v.get("pass", v) if isinstance(v, dict) else v
                                  for k, v in identity.items()},
    }
    out = SPRINT_ROOT / "artifacts" / "prefix-receipt.json"
    out.write_text(json.dumps(receipt, indent=2, default=str), encoding="utf-8")
    print(f"Wrote prefix receipt: {out}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", default="all",
                    choices=["identity", "smoke", "dev", "test", "ablation", "all"])
    args = ap.parse_args()

    identity_res: dict[str, Any] = {}
    smoke_res: dict[str, Any] = {}
    dev_receipt: dict[str, Any] = {}
    agg: dict[str, Any] = {}
    collapse: dict[str, Any] = {}
    ablation: dict[str, Any] = {}
    wall = 0.0
    oracle_labels: dict[str, Any] = {}

    if args.phase in ("identity", "all"):
        identity_res = phase_identity()
        write_prefix_receipt(identity_res)
        if args.phase == "identity" and not identity_res["all_gates_pass"]:
            sys.exit(1)

    if args.phase in ("smoke", "all"):
        smoke_res = phase_smoke()

    if args.phase in ("dev", "all"):
        dev_receipt = phase_dev_freeze()

    if args.phase in ("test", "all"):
        if not identity_res:
            identity_res = phase_identity()
            write_prefix_receipt(identity_res)
            if not identity_res["all_gates_pass"]:
                write_terminal_result(identity=identity_res, smoke=smoke_res,
                                      dev_receipt=dev_receipt, agg={"constructs": {}, "per_cell": {},
                                                                    "method_seed_cluster_mean_pi_ser": {},
                                                                    "comparator_seed_cluster_mean_pi_ser": float("nan"),
                                                                    "anchor_seed_cluster_mean_pi_ser": float("nan"),
                                                                    "seeds": [], "cells": []},
                                      collapse={}, ablation={}, wall=0.0, oracle_labels={})
                sys.exit(1)
        # Smoke MUST be in the same terminal result as compare (NOT clobbered).
        # If smoke was not run in this process, run it now so the terminal
        # result.json always carries the smoke receipt (V052 closure fix).
        if not smoke_res:
            smoke_res = phase_smoke()
        if not dev_receipt:
            p = SPRINT_ROOT / "artifacts" / "dev-freeze-receipt.v1.json"
            dev_receipt = json.loads(p.read_text(encoding="utf-8"))
        comp = phase_test_compare(dev_receipt)
        agg = aggregate_seed_cluster(comp["raw_rows"])
        collapse = collapse_removal_check(comp["raw_rows"])
        wall = comp["wall_seconds"]
        oracle_labels = comp["per_cell_oracle_label"]

    if args.phase in ("ablation", "all"):
        if not agg:
            # load raw rows from disk if re-running just ablation
            csv_path = SPRINT_ROOT / "artifacts" / "raw-rows.v3.csv"
            raw_rows = []
            with open(csv_path, encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    row["seed"] = int(row["seed"])
                    row["pi_ser"] = None if row["pi_ser"] in ("", "nan") else float(row["pi_ser"])
                    row["diverged"] = row["diverged"] == "True"
                    raw_rows.append(row)
            agg = aggregate_seed_cluster(raw_rows)
            collapse = collapse_removal_check(raw_rows)
        if not dev_receipt:
            p = SPRINT_ROOT / "artifacts" / "dev-freeze-receipt.v1.json"
            dev_receipt = json.loads(p.read_text(encoding="utf-8"))
        ablation = phase_ablation(dev_receipt, agg, collapse)

    if args.phase in ("test", "all"):
        write_terminal_result(identity=identity_res, smoke=smoke_res,
                              dev_receipt=dev_receipt, agg=agg, collapse=collapse,
                              ablation=ablation, wall=wall, oracle_labels=oracle_labels)
    elif args.phase == "ablation":
        # re-write terminal result with ablation filled in
        prev_path = SPRINT_ROOT / "artifacts" / "result.v3.json"
        prev = json.loads(prev_path.read_text(encoding="utf-8")) if prev_path.exists() else {}
        write_terminal_result(identity=prev.get("identity_gate_results", identity_res),
                              smoke=prev.get("smoke_results", smoke_res),
                              dev_receipt=dev_receipt, agg=agg, collapse=collapse,
                              ablation=ablation,
                              wall=prev.get("wall_seconds", wall),
                              oracle_labels=prev.get("offline_4category_labels", oracle_labels))


if __name__ == "__main__":
    main()
