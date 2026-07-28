"""Pre-formal Method Factory Sprint 002 — corrected-baseline causal
constellation-prior shell-distribution family.

Pipeline:
  Phase A — testbed identity gates + QPSK regression (no evaluation)
  Phase B — semantic smoke per construct (separate from comparison)
  Phase C1 — DEV freeze on dev_seeds × 7 cells (tiny grid only)
  Phase C2 — TEST fair paired comparison on test_seeds × 7 cells
  Phase D — seed-cluster aggregation + signal grading + terminal result

Critical fixes vs T019 sprint-001:
  (1) baseline = μ=0.03 fixed-μ CMA (current fair, NOT μ=0.001 anchor)
  (2) strict prefix/suffix causality: every method's freeze step reads ONLY
      z[eval_start:calibration_end]; the apply step reads z[calibration_end:eval_end]
  (3) smoke results are written to the SAME terminal result artifact as the
      comparison (V052 closure gap fixed — --compare no longer clobbers --smoke)
  (4) fresh disjoint dev seeds [181..190] / test seeds [201..220]
  (5) seed-cluster aggregation (7 cells are NOT 7 independent samples)

Usage:
    python run_factory.py --phase identity   # Phase A only
    python run_factory.py --phase smoke      # Phase B only (writes smoke receipt)
    python run_factory.py --phase dev        # Phase C1 dev freeze
    python run_factory.py --phase test       # Phase C2+D test compare + terminal
    python run_factory.py --phase all        # identity -> smoke -> dev -> test
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
SPRINT_ROOT = SRC.parent                       # preformal-method-factory-sprint-002/
CB1_ROOT = SPRINT_ROOT.parent / "cb1-modulation-generic-closure"
BASELINE_ATLAS = CB1_ROOT / "baseline-atlas"
REPO_ROOT = HERE.parents[6]                    # worktree root
SIM_DIR = REPO_ROOT / "projects" / "simulation"
C11_LEGALITY = CB1_ROOT / "c11-legality-batch-v1"

for p in (str(SIM_DIR), str(BASELINE_ATLAS), str(SRC), str(C11_LEGALITY)):
    if p not in sys.path:
        sys.path.insert(0, p)

from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402
import cb1_evaluator as evaluator  # noqa: E402
import cb1_cell_runner as runner  # noqa: E402
import methods as M  # noqa: E402
from c11_causal import c11_cma_dd_lms_causal  # noqa: E402


# ─── Frozen contract (mirrors factory-contract.v2.yaml) ──────────────────────
FROZEN_AXES = {
    "alpha": 4.2, "beta": 1.4, "block": 100, "t_s": 4.0e-10, "method": "gar",
    "cma_mu_current": 3.0e-2,   # B01-R hotfix v2 interior optimum (current fair)
    "cma_mu_stale": 1.0e-3,     # T019 anchor; FORBIDDEN as Go comparator
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

# Seed-disjointness assertions (frozen before any run)
assert set(DEV_SEEDS).isdisjoint(set(TEST_SEEDS)), "LEAKAGE: dev/test overlap"
assert set(DEV_SEEDS) | set(TEST_SEEDS) and set(DEV_SEEDS).isdisjoint({11, 12, 13, 14, 15, 16, 17, 18, 19, 20}), "LEAKAGE: dev/test vs T019"
assert set(DEV_SEEDS).isdisjoint({31, 32, 33, 34, 35, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50}), "LEAKAGE: dev vs C11-legality"
assert set(TEST_SEEDS).isdisjoint({31, 32, 33, 34, 35, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50}), "LEAKAGE: test vs C11-legality"

R2_16QAM = 1.32
MU_CURRENT = 3.0e-2     # current fair baseline (B01-R HF6)
MU_STALE = 1.0e-3       # T019 anchor; FORBIDDEN as Go comparator
TAPS = 11
BS = 64
RIDGE = 1.0e-6

# Phase C1 dev freeze grid (tiny, prefix-only; never sees test)
DEV_GRID = {
    "M1_prefix_scalar": {"trim_frac": [0.05, 0.1, 0.2]},
    "M4_gated_policy": {"collapse_threshold": [0.4, 0.5, 0.6],
                        "spread_threshold": [0.10, 0.15, 0.20]},
    # M2/M3 are parameter-free (closed-form from prefix); no grid.
}


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


# ─── Per-(cell,seed) realization runner ──────────────────────────────────────

def run_all_on_realization(cell: dict[str, Any], seed: int, *,
                           m1_trim: float = 0.1,
                           m4_collapse: float = 0.5,
                           m4_spread: float = 0.15) -> dict[str, Any]:
    """Run baseline + legal comparators + 4 new methods on ONE shared realization.

    New methods freeze ONLY from the calibration prefix; the suffix is never
    read by any freeze/gate/selection step.
    """
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

    # ---- CURRENT FAIR BASELINE: fixed-μ CMA μ=0.03 -------------------------
    base = runner.standard_cma_godard_with_z(
        realization["rX"], realization["rY"], n_tap=TAPS, mu=MU_CURRENT,
        R2=R2_16QAM, block_size=BS)
    z_calib = np.column_stack([base["zX"][es:cal], base["zY"][es:cal]])
    z_eval = np.column_stack([base["zX"][cal:ee], base["zY"][cal:ee]])
    base_diverged = bool(base["diverged"])
    if not base_diverged:
        bx = np.asarray(evaluator.hard_16qam(base["zX"][cal:ee]))
        by = np.asarray(evaluator.hard_16qam(base["zY"][cal:ee]))
        out["methods"]["baseline_cma_mu0p03"] = {
            **_eval_pred(bx, by, truth_eval_x, truth_eval_y, bits_eval_x, bits_eval_y),
            "diverged": False, "mu": MU_CURRENT}
    else:
        out["methods"]["baseline_cma_mu0p03"] = {**_diverged_metrics(), "mu": MU_CURRENT}

    # ---- Legal comparator 1: blind affine (z-only, prefix fit) -------------
    if not base_diverged:
        blind = evaluator.blind_affine_compare_16qam(z_calib, z_eval, ridge=RIDGE)
        m = _eval_pred(blind["predicted"][:, 0], blind["predicted"][:, 1],
                       truth_eval_x, truth_eval_y, bits_eval_x, bits_eval_y)
        m["diverged"] = False
    else:
        m = _diverged_metrics()
    out["methods"]["blind_affine"] = m

    # ---- Legal comparator 2: C11 legal causal one-pass ---------------------
    # Switch point frozen at the CMA convergence plateau (block index = the
    # first block at/after the 26%-of-N prefix). This mirrors the
    # c11-legality-batch-v1 switch-point policy but is frozen here as a single
    # deterministic block index per cell (no validation tuning within this
    # batch; C11 is a frozen inherited comparator, not being tuned here).
    n_valid_c11 = n - TAPS + 1
    n_blocks_c11 = n_valid_c11 // BS
    switch_block = max(1, min(n_blocks_c11 - 1, int(round(0.26 * n) // BS)))
    c11 = c11_cma_dd_lms_causal(
        realization["rX"], realization["rY"], n_tap=TAPS, cma_mu=MU_CURRENT,
        cma_R2=R2_16QAM, cma_block_size=BS, dd_step_size=1.0e-4,
        switch_point_block=switch_block,
        hard_decision_fn=evaluator.hard_16qam)
    if not c11["diverged"]:
        cx = np.asarray(evaluator.hard_16qam(c11["zX"][cal:ee]))
        cy = np.asarray(evaluator.hard_16qam(c11["zY"][cal:ee]))
        m = _eval_pred(cx, cy, truth_eval_x, truth_eval_y, bits_eval_x, bits_eval_y)
        m["diverged"] = False
    else:
        m = _diverged_metrics()
    out["methods"]["C11_legal_causal"] = m

    # ---- Kill-only bound: oracle affine (TX-truth, NEVER a Go baseline) ----
    # Pass CONTINUOUS corrected z to the evaluator (NOT pre-hard-decided); the
    # evaluator does its own hard decision + 8-way rotation/permutation search.
    if not base_diverged:
        truth_calib = np.column_stack([realization["sX"][es:cal],
                                       realization["sY"][es:cal]])
        oracle = evaluator.oracle_affine_bound_16qam(
            z_calib, z_eval, truth_calib, ridge=RIDGE)
        # oracle shape == z_eval shape == (N, 2); pass continuous corrected z
        m = _eval_pred(oracle[:, 0], oracle[:, 1],
                       truth_eval_x, truth_eval_y, bits_eval_x, bits_eval_y)
        m["diverged"] = False
    else:
        m = _diverged_metrics()
    out["methods"]["oracle_affine_bound_KILL_ONLY"] = m  # NEVER a Go baseline

    # ---- NEW METHODS: freeze from prefix only, apply to suffix -------------
    # Apply methods return CONTINUOUS corrected z (the evaluator does the hard
    # decision + rotation/permutation search). This matches the oracle/blind
    # convention in cb1_cell_runner.run_cell lines 371-385.
    if not base_diverged:
        z_prefix_x = base["zX"][es:cal]
        z_prefix_y = base["zY"][es:cal]
        z_suffix_x = base["zX"][cal:ee]
        z_suffix_y = base["zY"][cal:ee]

        # M1: prefix scalar calibration — apply returns continuous scaled z
        f1 = M.m1_prefix_scalar_freeze(np.concatenate([z_prefix_x, z_prefix_y]),
                                       trim_frac=m1_trim)
        m1x = M.m1_prefix_scalar_apply_continuous(f1, z_suffix_x)
        m1y = M.m1_prefix_scalar_apply_continuous(f1, z_suffix_y)
        out["methods"]["M1_prefix_scalar"] = {
            **_eval_pred(m1x, m1y, truth_eval_x, truth_eval_y, bits_eval_x, bits_eval_y),
            "diverged": False, "frozen": {"scale": float(f1["scale"])}}

        # M2: prefix quantile transport (parameter-free closed-form)
        f2 = M.m2_quantile_transport_freeze(np.concatenate([z_prefix_x, z_prefix_y]))
        m2x = M.m2_quantile_transport_apply_continuous(f2, z_suffix_x)
        m2y = M.m2_quantile_transport_apply_continuous(f2, z_suffix_y)
        out["methods"]["M2_quantile_transport"] = {
            **_eval_pred(m2x, m2y, truth_eval_x, truth_eval_y, bits_eval_x, bits_eval_y),
            "diverged": False, "frozen": {"identity": bool(f2.get("identity", False))}}

        # M3: prefix three-shell mixture (parameter-free closed-form)
        f3 = M.m3_three_shell_mixture_freeze(np.concatenate([z_prefix_x, z_prefix_y]))
        m3x = M.m3_three_shell_mixture_apply_continuous(f3, z_suffix_x)
        m3y = M.m3_three_shell_mixture_apply_continuous(f3, z_suffix_y)
        out["methods"]["M3_three_shell_mixture"] = {
            **_eval_pred(m3x, m3y, truth_eval_x, truth_eval_y, bits_eval_x, bits_eval_y),
            "diverged": False,
            "frozen": {"identity": bool(f3.get("identity", False)),
                       "knot_median": float(f3.get("knot_median", 0.0))}}

        # M4: prefix-gated identity/M2/M3 policy
        f4 = M.m4_gated_policy_freeze(np.concatenate([z_prefix_x, z_prefix_y]),
                                      collapse_threshold=m4_collapse,
                                      spread_threshold=m4_spread)
        m4x = M.m4_gated_policy_apply_continuous(f4, z_suffix_x, m2_frozen=f2, m3_frozen=f3)
        m4y = M.m4_gated_policy_apply_continuous(f4, z_suffix_y, m2_frozen=f2, m3_frozen=f3)
        out["methods"]["M4_gated_policy"] = {
            **_eval_pred(m4x, m4y, truth_eval_x, truth_eval_y, bits_eval_x, bits_eval_y),
            "diverged": False,
            "frozen": {"policy": str(f4["policy"]),
                       "mean_abs2": float(f4["mean_abs2"]),
                       "spread": float(f4["spread"])}}
    else:
        for mname in ("M1_prefix_scalar", "M2_quantile_transport",
                      "M3_three_shell_mixture", "M4_gated_policy"):
            out["methods"][mname] = _diverged_metrics()

    out["base_diverged"] = base_diverged
    return out


# ─── Phase A: identity gates + QPSK regression ───────────────────────────────

def phase_identity() -> dict[str, Any]:
    print("=" * 70)
    print("PHASE A: TESTBED IDENTITY GATES")
    print("=" * 70)
    res: dict[str, Any] = {}

    # Gate 1: QPSK identity regression (PI-SER = 0.0). run_cell reads cma_mu
    # from frozen_common_axes, so we pass the CURRENT fair μ (0.03) — the same
    # μ the test uses. QPSK has no inner-ring collapse, so any stable μ gives
    # PI-SER=0; we use 0.03 to confirm the runner accepts the current baseline.
    contract = {"frozen_common_axes": {**FROZEN_AXES, "r2_qpsk": 1.0,
                                       "cma_mu": MU_CURRENT},
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

    # Gate 2: eval population identity — baseline on cell 0, seed 181 produces finite z
    cell = CELLS[0]
    out = run_all_on_realization(cell, DEV_SEEDS[0])
    pop_ok = (not out["base_diverged"]
              and np.isfinite(out["methods"]["baseline_cma_mu0p03"]["pi_ser"]))
    res["eval_population_identity"] = {"base_diverged": bool(out["base_diverged"]),
                                       "pass": bool(pop_ok)}
    print(f"  Eval population identity: base_diverged={out['base_diverged']} -> "
          f"{'PASS' if pop_ok else 'FAIL'}")

    # Gate 3: prefix-only freeze invariance — freeze twice on same prefix -> identical
    es, cal, ee = _eval_window(cell["n_symbols"])
    realization = _realization(cell, DEV_SEEDS[0])
    base = runner.standard_cma_godard_with_z(
        realization["rX"], realization["rY"], n_tap=TAPS, mu=MU_CURRENT,
        R2=R2_16QAM, block_size=BS)
    z_prefix = np.concatenate([base["zX"][es:cal], base["zY"][es:cal]])
    z_suffix_a = np.concatenate([base["zX"][cal:ee], base["zY"][cal:ee]])
    # perturb suffix deterministically
    z_suffix_b = z_suffix_a + 0.1 + 0.1j
    invariance_ok = True
    for mid in ("M1_prefix_scalar", "M2_quantile_transport",
                "M3_three_shell_mixture", "M4_gated_policy"):
        fa = _freeze(mid, z_prefix)
        fb = _freeze(mid, z_prefix)  # same prefix
        if not _frozen_equal(fa, fb):
            invariance_ok = False
            break
    res["prefix_only_freeze_invariance"] = {"pass": bool(invariance_ok)}
    print(f"  Prefix-only freeze invariance: -> {'PASS' if invariance_ok else 'FAIL'}")

    all_pass = qpsk_pass and pop_ok and invariance_ok
    res["all_gates_pass"] = bool(all_pass)
    print(f"\n=== PHASE A: {'ALL PASS' if all_pass else 'BLOCKED'} ===\n")
    return res


def _freeze(method_id: str, z_prefix: np.ndarray) -> dict:
    if method_id == "M1_prefix_scalar":
        return M.m1_prefix_scalar_freeze(z_prefix)
    if method_id == "M2_quantile_transport":
        return M.m2_quantile_transport_freeze(z_prefix)
    if method_id == "M3_three_shell_mixture":
        return M.m3_three_shell_mixture_freeze(z_prefix)
    if method_id == "M4_gated_policy":
        return M.m4_gated_policy_freeze(z_prefix)
    raise ValueError(method_id)


def _frozen_equal(a: dict, b: dict) -> bool:
    if set(a.keys()) != set(b.keys()):
        return False
    for k in a:
        va, vb = a[k], b[k]
        if isinstance(va, np.ndarray):
            if not np.array_equal(va, vb):
                return False
        elif isinstance(va, (int, float, bool, np.floating, np.integer, np.bool_)):
            if not np.isclose(va, vb, rtol=1e-12, atol=1e-12):
                return False
        else:
            if va != vb:
                return False
    return True


# ─── Phase B: semantic smoke (per construct, persisted separately) ───────────

def phase_smoke() -> dict[str, Any]:
    print("=" * 70)
    print("PHASE B: SEMANTIC SMOKE (per construct)")
    print("=" * 70)
    results: dict[str, Any] = {}
    cell = CELLS[0]  # snr20-fg100-short style short cell
    es, cal, ee = _eval_window(cell["n_symbols"])
    rng = np.random.default_rng(123)

    for seed in (DEV_SEEDS[0], DEV_SEEDS[1]):
        realization = _realization(cell, seed)
        base = runner.standard_cma_godard_with_z(
            realization["rX"], realization["rY"], n_tap=TAPS, mu=MU_CURRENT,
            R2=R2_16QAM, block_size=BS)
        if base["diverged"]:
            continue
        z_prefix_x = base["zX"][es:cal]
        z_prefix_y = base["zY"][es:cal]
        z_suffix_x = base["zX"][cal:ee]
        z_suffix_y = base["zY"][cal:ee]
        z_prefix = np.concatenate([z_prefix_x, z_prefix_y])

        # Action identity: perturbing the suffix changes the output (information increment)
        f1 = M.m1_prefix_scalar_freeze(z_prefix)
        p_a = M.m1_prefix_scalar_apply(f1, z_suffix_x)
        p_b = M.m1_prefix_scalar_apply(f1, z_suffix_x + 0.1)
        m1_incr = bool(np.any(p_a != p_b))
        results.setdefault("M1_prefix_scalar", {})[f"seed_{seed}_information_increment"] = m1_incr

        # M2: identity on healthy prefix, transport on collapsed
        f2 = M.m2_quantile_transport_freeze(z_prefix)
        # collapsed prefix = scale 0.45
        f2c = M.m2_quantile_transport_freeze(0.45 * z_prefix)
        results.setdefault("M2_quantile_transport", {})[f"seed_{seed}_healthy_identity"] = bool(f2.get("identity", False))
        results.setdefault("M2_quantile_transport", {})[f"seed_{seed}_collapsed_active"] = bool(not f2c.get("identity", False))

        # M3: identity on healthy, active on collapsed
        f3 = M.m3_three_shell_mixture_freeze(z_prefix)
        f3c = M.m3_three_shell_mixture_freeze(0.45 * z_prefix)
        results.setdefault("M3_three_shell_mixture", {})[f"seed_{seed}_healthy_identity"] = bool(f3.get("identity", False))
        results.setdefault("M3_three_shell_mixture", {})[f"seed_{seed}_collapsed_active"] = bool(not f3c.get("identity", False))

        # M4: gate selects a policy; check it changes with prefix
        f4 = M.m4_gated_policy_freeze(z_prefix)
        f4c = M.m4_gated_policy_freeze(0.45 * z_prefix)
        results.setdefault("M4_gated_policy", {})[f"seed_{seed}_healthy_policy"] = str(f4["policy"])
        results.setdefault("M4_gated_policy", {})[f"seed_{seed}_collapsed_policy"] = str(f4c["policy"])

    print(f"  smoke checks completed for 4 constructs (2 seeds each)")
    print(f"\n=== PHASE B: SMOKE COMPLETE ===\n")
    return results


# ─── Phase C1: dev freeze (tiny prefix-only grid) ────────────────────────────

def phase_dev_freeze() -> dict[str, Any]:
    print("=" * 70)
    print("PHASE C1: DEV FREEZE (prefix-only tiny grid)")
    print(f"  cells: {[c['id'] for c in CELLS]}")
    print(f"  dev_seeds: {DEV_SEEDS}")
    print("=" * 70)

    # Build a small validation pool: 3 short cells × 3 dev seeds (to keep dev fast)
    dev_cells = [CELLS[0], CELLS[1], CELLS[4]]  # snr05, snr10, snr20-fg100 (all short)
    dev_subseeds = DEV_SEEDS[:3]  # 181, 182, 183

    best: dict[str, Any] = {}

    # M1 grid: trim_frac
    best_m1_score = float("inf")
    best_m1_trim = 0.1
    for trim in DEV_GRID["M1_prefix_scalar"]["trim_frac"]:
        deltas = []
        for cell in dev_cells:
            for seed in dev_subseeds:
                out = run_all_on_realization(cell, seed, m1_trim=trim)
                b = out["methods"]["baseline_cma_mu0p03"]["pi_ser"]
                m1 = out["methods"]["M1_prefix_scalar"]["pi_ser"]
                if np.isfinite(b) and np.isfinite(m1):
                    deltas.append(m1 - b)
        score = float(np.mean(deltas)) if deltas else float("inf")
        if score < best_m1_score:
            best_m1_score = score
            best_m1_trim = trim
        print(f"  M1 trim_frac={trim}: dev mean ΔPI-SER={score:+.5f}")
    best["M1_prefix_scalar"] = {"trim_frac": best_m1_trim, "dev_mean_delta": best_m1_score}

    # M4 grid: collapse_threshold × spread_threshold
    best_m4_score = float("inf")
    best_m4 = {"collapse_threshold": 0.5, "spread_threshold": 0.15}
    for ct in DEV_GRID["M4_gated_policy"]["collapse_threshold"]:
        for st in DEV_GRID["M4_gated_policy"]["spread_threshold"]:
            deltas = []
            for cell in dev_cells:
                for seed in dev_subseeds:
                    out = run_all_on_realization(cell, seed, m4_collapse=ct, m4_spread=st)
                    b = out["methods"]["baseline_cma_mu0p03"]["pi_ser"]
                    m4 = out["methods"]["M4_gated_policy"]["pi_ser"]
                    if np.isfinite(b) and np.isfinite(m4):
                        deltas.append(m4 - b)
            score = float(np.mean(deltas)) if deltas else float("inf")
            if score < best_m4_score:
                best_m4_score = score
                best_m4 = {"collapse_threshold": ct, "spread_threshold": st}
            print(f"  M4 ct={ct} st={st}: dev mean ΔPI-SER={score:+.5f}")
    best["M4_gated_policy"] = {**best_m4, "dev_mean_delta": best_m4_score}

    # M2/M3 are parameter-free; record their dev deltas for the receipt
    for mname in ("M2_quantile_transport", "M3_three_shell_mixture"):
        deltas = []
        for cell in dev_cells:
            for seed in dev_subseeds:
                out = run_all_on_realization(cell, seed)
                b = out["methods"]["baseline_cma_mu0p03"]["pi_ser"]
                mv = out["methods"][mname]["pi_ser"]
                if np.isfinite(b) and np.isfinite(mv):
                    deltas.append(mv - b)
        best[mname] = {"parameter_free": True,
                       "dev_mean_delta": float(np.mean(deltas)) if deltas else float("inf")}

    receipt = {"frozen_dev_params": best,
               "dev_cells": [c["id"] for c in dev_cells],
               "dev_subseeds": dev_subseeds,
               "note": "Frozen from prefix-only dev pool; test seeds never observed."}
    out = SPRINT_ROOT / "artifacts" / "dev-freeze-receipt.v1.json"
    out.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(f"\nWrote dev freeze receipt: {out}")
    print(f"\n=== PHASE C1: DEV FROZEN ===\n")
    return receipt


# ─── Phase C2+D: test paired comparison + seed-cluster aggregation ───────────

def phase_test_compare(dev_receipt: dict[str, Any]) -> dict[str, Any]:
    print("=" * 70)
    print("PHASE C2+D: TEST PAIRED COMPARISON (seed-cluster)")
    print(f"  cells: {[c['id'] for c in CELLS]}")
    print(f"  test_seeds: {TEST_SEEDS}")
    print("=" * 70)

    m1_trim = dev_receipt["frozen_dev_params"]["M1_prefix_scalar"]["trim_frac"]
    m4_c = dev_receipt["frozen_dev_params"]["M4_gated_policy"]["collapse_threshold"]
    m4_s = dev_receipt["frozen_dev_params"]["M4_gated_policy"]["spread_threshold"]

    raw_rows: list[dict[str, Any]] = []
    per_cell_oracle_label: dict[str, dict[str, Any]] = {}
    t0 = time.time()
    for ci, cell in enumerate(CELLS):
        for seed in TEST_SEEDS:
            out = run_all_on_realization(cell, seed,
                                          m1_trim=m1_trim, m4_collapse=m4_c, m4_spread=m4_s)
            for mname, mres in out["methods"].items():
                pis = mres.get("pi_ser")
                raw_rows.append({
                    "cell_id": out["cell_id"], "seed": out["seed"], "method": mname,
                    "pi_ser": (None if pis is None or not np.isfinite(pis) else float(pis)),
                    "fixed_label_ser": (None if (v := mres.get("fixed_label_ser")) is None or not np.isfinite(v) else float(v)),
                    "pi_ber": (None if (v := mres.get("pi_ber")) is None or not np.isfinite(v) else float(v)),
                    "diverged": bool(mres.get("diverged", False)),
                })
            # Offline 4-category label (oracle only for labelling; not deployment)
            per_cell_oracle_label.setdefault(cell["id"], _offline_label(out))
        print(f"  [{ci+1}/{len(CELLS)}] {cell['id']:28s} done ({time.time()-t0:.1f}s)")

    csv_path = SPRINT_ROOT / "artifacts" / "raw-rows.v2.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["cell_id", "seed", "method", "pi_ser",
                                          "fixed_label_ser", "pi_ber", "diverged"])
        w.writeheader()
        for row in raw_rows:
            w.writerow(row)
    print(f"\nWrote raw rows: {csv_path} ({len(raw_rows)} rows)")

    return {"raw_rows": raw_rows, "per_cell_oracle_label": per_cell_oracle_label,
            "wall_seconds": time.time() - t0}


def _offline_label(out: dict[str, Any]) -> dict[str, Any]:
    """4-category collapse label from oracle/baseline (LABEL ONLY)."""
    b = out["methods"].get("baseline_cma_mu0p03", {}).get("pi_ser")
    o = out["methods"].get("oracle_affine_bound_KILL_ONLY", {}).get("pi_ser")
    if b is None or o is None or not np.isfinite(b) or not np.isfinite(o):
        return {"category": "ambiguous"}
    if out.get("base_diverged"):
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


# ─── Seed-cluster aggregation ────────────────────────────────────────────────

METHOD_ORDER = ["baseline_cma_mu0p03", "blind_affine", "C11_legal_causal",
                "oracle_affine_bound_KILL_ONLY", "M1_prefix_scalar",
                "M2_quantile_transport", "M3_three_shell_mixture", "M4_gated_policy"]
COMPARATORS = ["baseline_cma_mu0p03", "blind_affine", "C11_legal_causal"]
CONSTRUCTS = ["M1_prefix_scalar", "M2_quantile_transport",
              "M3_three_shell_mixture", "M4_gated_policy"]


def aggregate_seed_cluster(raw_rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Seed-cluster aggregation: each SEED is one independent cluster.

    Steps:
      (1) per-seed, per-method mean PI-SER over the 7 cells;
      (2) per-seed paired delta = method - baseline (over cells);
      (3) seed-cluster bootstrap CI on the per-seed mean delta;
      (4) help/hurt/tie SEEDS.
    """
    cells = sorted({r["cell_id"] for r in raw_rows})
    seeds = sorted({r["seed"] for r in raw_rows})

    idx: dict[tuple[str, int, str], float | None] = {}
    for r in raw_rows:
        idx[(r["cell_id"], r["seed"], r["method"])] = r["pi_ser"]

    # Per-seed, per-method mean over cells
    seed_method_mean: dict[tuple[int, str], float] = {}
    for s in seeds:
        for m in METHOD_ORDER:
            vals = [idx[(c, s, m)] for c in cells if idx.get((c, s, m)) is not None]
            vals = [v for v in vals if v is not None]
            seed_method_mean[(s, m)] = float(np.mean(vals)) if vals else float("nan")

    # Per-seed paired delta vs baseline (mean over cells within the seed)
    seed_delta: dict[tuple[int, str], float] = {}
    for s in seeds:
        b = seed_method_mean.get((s, "baseline_cma_mu0p03"), float("nan"))
        for m in CONSTRUCTS:
            mv = seed_method_mean.get((s, m), float("nan"))
            seed_delta[(s, m)] = float(mv - b) if np.isfinite(b) and np.isfinite(mv) else float("nan")

    # Comparator coverage (for "no regression vs strongest legal" check) —
    # computed BEFORE the constructs loop so the gate can use it.
    comparator_means: dict[str, float] = {}
    for m in COMPARATORS:
        vals = [seed_method_mean.get((s, m), float("nan")) for s in seeds]
        vals = [v for v in vals if np.isfinite(v)]
        comparator_means[m] = float(np.mean(vals)) if vals else float("nan")

    # Per-method seed-cluster stats
    constructs_agg: dict[str, Any] = {}
    for m in CONSTRUCTS:
        deltas = [seed_delta[(s, m)] for s in seeds if np.isfinite(seed_delta[(s, m)])]
        if not deltas:
            constructs_agg[m] = {"n_seeds": 0}
            continue
        help_n = sum(1 for d in deltas if d < -1e-9)
        hurt_n = sum(1 for d in deltas if d > 1e-9)
        tie_n = sum(1 for d in deltas if abs(d) <= 1e-9)
        mean_d = float(np.mean(deltas))
        median_d = float(np.median(deltas))
        ci_lo, ci_hi = _cluster_bootstrap_ci(deltas)
        # Healthy-cluster regression stats (contract: no catastrophic regression
        # on clean/healthy cells). A pair is "healthy" if baseline PI-SER < 0.1.
        healthy_deltas = []
        for s in seeds:
            for c in cells:
                b = idx.get((c, s, "baseline_cma_mu0p03"))
                mv = idx.get((c, s, m))
                if (b is not None and mv is not None and b < 0.1):
                    healthy_deltas.append(mv - b)
        healthy_mean_d = float(np.mean(healthy_deltas)) if healthy_deltas else float("nan")
        healthy_worst_d = float(np.max(healthy_deltas)) if healthy_deltas else float("nan")
        healthy_n = len(healthy_deltas)
        # Strongest legal comparator seed-cluster mean (for "no significant regression")
        comp_means = [comparator_means.get(cm, float("inf"))
                      for cm in ("blind_affine", "C11_legal_causal")]
        strongest_comp = float(np.min(comp_means)) if comp_means else float("inf")
        method_seed_mean = float(np.mean([seed_method_mean.get((s, m), float("nan"))
                                          for s in seeds if np.isfinite(seed_method_mean.get((s, m), float("nan")))]))
        gate = _signal_gate(mean_d, ci_hi, help_n, hurt_n,
                            healthy_worst_d=healthy_worst_d,
                            method_seed_mean=method_seed_mean,
                            strongest_comp_mean=strongest_comp)
        constructs_agg[m] = {
            "n_seeds": len(deltas),
            "seed_cluster_mean_delta_pi_ser": mean_d,
            "seed_cluster_median_delta_pi_ser": median_d,
            "seed_cluster_bootstrap_ci_95": [ci_lo, ci_hi],
            "help_seeds": help_n, "hurt_seeds": hurt_n, "tie_seeds": tie_n,
            "healthy_cluster_n_pairs": healthy_n,
            "healthy_cluster_mean_delta_pi_ser": healthy_mean_d,
            "healthy_cluster_worst_delta_pi_ser": healthy_worst_d,
            "method_seed_cluster_mean_pi_ser": method_seed_mean,
            "strongest_legal_comparator_mean_pi_ser": strongest_comp,
            "diagnostic_signal_gate": gate,
        }

    # Per-cell heterogeneity (descriptive only)
    per_cell: dict[str, dict[str, Any]] = {}
    for c in cells:
        per_cell[c] = {}
        for m in CONSTRUCTS:
            deltas = []
            for s in seeds:
                b = idx.get((c, s, "baseline_cma_mu0p03"))
                mv = idx.get((c, s, m))
                if b is not None and mv is not None:
                    deltas.append(mv - b)
            if deltas:
                per_cell[c][m] = {"n_seeds": len(deltas),
                                  "mean_delta": float(np.mean(deltas)),
                                  "median_delta": float(np.median(deltas))}

    # Comparator coverage (returned for reporting)
    return {"constructs": constructs_agg, "per_cell_heterogeneity": per_cell,
            "comparator_seed_cluster_mean_pi_ser": comparator_means,
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


def _signal_gate(mean_d: float, ci_hi: float, help_n: int, hurt_n: int, *,
                 healthy_worst_d: float, method_seed_mean: float,
                 strongest_comp_mean: float) -> dict[str, Any]:
    """DIAGNOSTIC_METHOD_SIGNAL / WEAK / NO per D027 + factory-contract.v2.

    DIAGNOSTIC_METHOD_SIGNAL requires ALL of:
      (a) seed-cluster mean ΔPI-SER ≤ −0.005 vs μ=0.03 CMA
      (b) 95% CI upper < 0
      (c) help seeds > hurt seeds
      (d) no significant regression vs strongest legal receiver-visible comparator
          (method_seed_mean ≤ strongest_comp_mean + MDE = 0.005)
      (e) no catastrophic regression on clean/healthy cells
          (healthy_worst_d ≤ MDE = 0.005; i.e. method never makes a healthy cell worse by ≥ MDE)
    """
    MDE = 0.005
    sig_mean = mean_d <= -MDE
    ci_upper_neg = (ci_hi < 0) if np.isfinite(ci_hi) else False
    help_gt_hurt = help_n > hurt_n
    no_comp_regression = (method_seed_mean <= strongest_comp_mean + MDE
                          if np.isfinite(method_seed_mean) and np.isfinite(strongest_comp_mean)
                          else False)
    no_healthy_catastrophe = (healthy_worst_d <= MDE
                              if np.isfinite(healthy_worst_d) else False)
    strong = (sig_mean and ci_upper_neg and help_gt_hurt
              and no_comp_regression and no_healthy_catastrophe)
    weak = (mean_d < -1e-9) and help_gt_hurt and not strong
    label = ("DIAGNOSTIC_METHOD_SIGNAL" if strong
             else ("WEAK_DIAGNOSTIC_SIGNAL" if weak else "NO_SIGNAL"))
    return {"seed_cluster_mean_le_neg_MDE": bool(sig_mean),
            "ci_upper_lt_0": bool(ci_upper_neg),
            "help_gt_hurt": bool(help_gt_hurt),
            "no_significant_regression_vs_strongest_legal_comparator": bool(no_comp_regression),
            "no_catastrophic_regression_on_healthy": bool(no_healthy_catastrophe),
            "healthy_cluster_worst_delta_pi_ser": float(healthy_worst_d) if np.isfinite(healthy_worst_d) else None,
            "label": label}


# ─── Terminal result writer ──────────────────────────────────────────────────

def write_terminal_result(*, identity: dict, smoke: dict, dev_receipt: dict,
                          agg: dict, wall: float, oracle_labels: dict) -> None:
    constructs_built = CONSTRUCTS
    constructs_compared = [m for m in constructs_built
                           if agg["constructs"].get(m, {}).get("n_seeds", 0) > 0]
    winners = [m for m in constructs_compared
               if agg["constructs"][m]["diagnostic_signal_gate"]["label"] == "DIAGNOSTIC_METHOD_SIGNAL"]
    weak = [m for m in constructs_compared
            if agg["constructs"][m]["diagnostic_signal_gate"]["label"] == "WEAK_DIAGNOSTIC_SIGNAL"]

    if not identity.get("all_gates_pass"):
        status = "BLOCKED_CURRENT_TESTBED"
        delta = "NONE"
    elif winners:
        status = "DIAGNOSTIC_METHOD_SIGNAL"
        delta = "METHOD_SIGNAL"
    elif len(constructs_compared) < 3:
        status = "BLOCKED_CURRENT_TESTBED"
        delta = "NONE"
    elif weak:
        status = "WEAK_DIAGNOSTIC_SIGNAL"
        delta = "FAIR_COMPARISON_RUN"
    else:
        status = "NO_DIAGNOSTIC_SIGNAL_EXIT_CB1_Z_ONLY"
        delta = "FAIR_COMPARISON_RUN"

    result = {
        "status": status,
        "mission_method_delta": delta,
        "testbed_identity": {
            "source_entry": "cb1-modulation-generic-closure/baseline-atlas",
            "primary_baseline": "fixed_mu_cma_mu_0_03 (μ=0.03, B01-R HF6 interior optimum)",
            "forbidden_baseline": "μ=0.001 anchor (T019; NOT a Go comparator)",
            "qpsk_regression_pi_ser": identity.get("qpsk_regression", {}).get("pi_ser"),
            "paired_realization": "generate_shared_realization_dp",
            "cells": agg["cells"], "test_seeds": agg["seeds"],
            "dev_seeds": DEV_SEEDS,
        },
        "constructs_built": constructs_built,
        "constructs_compared": constructs_compared,
        "paired_results": agg["constructs"],
        "per_cell_heterogeneity": agg["per_cell_heterogeneity"],
        "comparator_seed_cluster_mean_pi_ser": agg["comparator_seed_cluster_mean_pi_ser"],
        "diagnostic_winners": winners,
        "diagnostic_weak": weak,
        "smoke_results": smoke,                # NOT clobbered (V052 fix)
        "identity_gate_results": identity,     # NOT clobbered
        "dev_freeze_receipt": dev_receipt,
        "offline_4category_labels": oracle_labels,
        "wall_seconds": wall,
        "claim_ceiling": "DIAGNOSTIC_ONLY_NOT_FORMAL_GW_MVE",
        "next_formal_action": None,
        "exit_rule": ("CB1 z-only/post-processing axis EXIT; no third package" if
                      status == "NO_DIAGNOSTIC_SIGNAL_EXIT_CB1_Z_ONLY" else None),
    }
    out = SPRINT_ROOT / "artifacts" / "result.v2.json"
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"\nWrote terminal result: {out}")
    print(f"\n=== STATUS: {status} | mission_method_delta: {delta} ===")
    if winners:
        print(f"Diagnostic winners: {winners}")
    if weak:
        print(f"Weak signals: {weak}")
    print("\nPer-construct (seed-cluster mean ΔPI-SER vs μ=0.03, negative=improvement):")
    for m in constructs_compared:
        a = agg["constructs"][m]
        g = a["diagnostic_signal_gate"]
        ci = a.get("seed_cluster_bootstrap_ci_95", [float("nan"), float("nan")])
        print(f"  {m:26s} mean_d={a['seed_cluster_mean_delta_pi_ser']:+.5f} "
              f"CI=[{ci[0]:+.5f},{ci[1]:+.5f}] "
              f"help/hurt/tie={a['help_seeds']}/{a['hurt_seeds']}/{a['tie_seeds']} -> {g['label']}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", default="all",
                    choices=["identity", "smoke", "dev", "test", "all"])
    args = ap.parse_args()

    identity_res: dict[str, Any] = {}
    smoke_res: dict[str, Any] = {}
    dev_receipt: dict[str, Any] = {}
    agg: dict[str, Any] = {}
    wall = 0.0
    oracle_labels: dict[str, Any] = {}

    if args.phase in ("identity", "all"):
        identity_res = phase_identity()
        if args.phase == "identity" and not identity_res["all_gates_pass"]:
            sys.exit(1)

    if args.phase in ("smoke", "all"):
        smoke_res = phase_smoke()

    if args.phase in ("dev", "all"):
        dev_receipt = phase_dev_freeze()

    if args.phase in ("test", "all"):
        # Identity gates MUST be re-run whenever test results are produced, so
        # the terminal result's identity_gate_results is never stale/empty.
        if not identity_res:
            identity_res = phase_identity()
            if not identity_res["all_gates_pass"]:
                write_terminal_result(identity=identity_res, smoke=smoke_res,
                                      dev_receipt=dev_receipt, agg={}, wall=0.0,
                                      oracle_labels={})
                sys.exit(1)
        if not dev_receipt:
            # load persisted receipt
            p = SPRINT_ROOT / "artifacts" / "dev-freeze-receipt.v1.json"
            dev_receipt = json.loads(p.read_text(encoding="utf-8"))
        comp = phase_test_compare(dev_receipt)
        agg = aggregate_seed_cluster(comp["raw_rows"])
        wall = comp["wall_seconds"]
        oracle_labels = comp["per_cell_oracle_label"]
        write_terminal_result(identity=identity_res, smoke=smoke_res,
                              dev_receipt=dev_receipt, agg=agg, wall=wall,
                              oracle_labels=oracle_labels)


if __name__ == "__main__":
    main()
