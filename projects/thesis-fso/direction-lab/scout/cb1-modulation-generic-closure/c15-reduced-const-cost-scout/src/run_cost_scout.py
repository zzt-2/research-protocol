"""C15 reduced-constellation / ring-aware cost Scout runner.

Single entry point. Pipeline (mirrors c12-gmi-soft-output-scout):
  1. Run the REQUIRED-PASS identity tests (RED -> abort).
  2. Run the semantic smoke (3 frozen checks). FAIL -> DIAGNOSTIC and STOP.
  3. Run the full batch: 11 cells x 10 seeds x 4 costs (godard anchor, ring-aware,
     rccma, plus the cma_godard engine reference for identity). For each (cell,
     seed, cost): run the equalizer, slice the eval window, evaluate PI-SER and
     the collapse indicator (E|z|^2 < 0.6).
  4. Aggregate per-cell collapse_rate + PI-SER over seeds; macro paired deltas
     vs Godard with hierarchical paired bootstrap 95% CI.
  5. Apply the frozen decision rule. Write artifacts/result.v1.json.

Cost-isolation: all costs share the EXACT anchor structure (11 taps, block=64,
mu=0.03, center-tap init). ONLY the cost function differs. The Godard
comparator uses the READ-ONLY anchor import (protected provenance stamp); the
candidates use cma_cost_variants.

Reuses (READ-ONLY imports, no modification):
  - generate_shared_realization_dp  (projects/simulation/common/_dual_pol_channel)
  - standard_cma_godard_with_z      (baseline-atlas/cb1_cell_runner) [ANCHOR]
  - eval_window_for                 (baseline-atlas/cb1_cell_runner)
  - evaluate_dual_16qam             (baseline-atlas/cb1_evaluator) [PI-SER]
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

# ─── path bootstrap (mirrors the test file) ──────────────────────────────────
HERE = Path(__file__).resolve().parent                       # .../src
SRC = HERE
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
# HERE.parents[6] = worktree root (src->c15->cb1-closure->scout->dir-lab->thesis-fso->projects->root)
SIM_DIR = HERE.parents[6] / "projects" / "simulation"
if str(SIM_DIR) not in sys.path:
    sys.path.insert(0, str(SIM_DIR))
# HERE.parents[1] = cb1-modulation-generic-closure (sibling of baseline-atlas)
BASELINE_ATLAS = HERE.parents[1] / "baseline-atlas"
if str(BASELINE_ATLAS) not in sys.path:
    sys.path.insert(0, str(BASELINE_ATLAS))

from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402
import cb1_cell_runner as runner  # noqa: E402
import cb1_evaluator as evaluator  # noqa: E402
import cma_cost_variants as ccv  # noqa: E402

SCOUT_DIR = HERE.parent                                   # c15-reduced-const-cost-scout
ARTIFACTS = SCOUT_DIR / "artifacts"
ARTIFACTS.mkdir(parents=True, exist_ok=True)


# ─── Frozen contract (mirrors batch-contract.v1.yaml) ────────────────────────
FROZEN_AXES = {
    "alpha": 4.2, "beta": 1.4, "block": 100, "t_s": 4e-10, "method": "gar",
    "cma_mu": 0.03, "cma_taps": 11, "cma_block_size": 64,
    "r2_qam16_godard": 1.32,
    "ring_squared_radii": [0.2, 1.0, 1.8],
    "ring_boundaries_squared": [0.6, 1.4],
    "rccma_outer_R2": 1.8,
    "rccma_outer_threshold_squared": 1.4,
    "affine_ridge": 1e-6,
}
SEEDS = [71, 72, 73, 74, 75, 76, 77, 78, 79, 80]
CELLS = [
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
# Collapse threshold: eval-window mean |zX|^2 + |zY|^2 below this = collapsed
# (healthy Godard ~2.0-2.6; inner-ring collapse ~0.3; midpoint 0.6 = boundary).
COLLAPSE_POWER_THRESHOLD = 0.6
# 16QAM random-decision PI-SER ceiling (sanity blow-up bound).
QAM16_RANDOM_CEILING = 0.9375


# ─── helpers ─────────────────────────────────────────────────────────────────
def _jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    if isinstance(value, np.ndarray):
        return [_jsonable(v) for v in value.tolist()]
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        v = float(value)
        return v if not np.isnan(v) else None
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, complex):
        return {"real": value.real, "imag": value.imag}
    if isinstance(value, (str, int, float, bool)) or value is None:
        if isinstance(value, float) and np.isnan(value):
            return None
        return value
    return str(value)


# ─── cost registry (the ONLY thing that differs across costs) ────────────────
# Each entry: (cost_name, callable). The Godard comparator uses the READ-ONLY
# anchor import so its provenance stamp is the protected one.
def _run_cost(cost_name: str, rX, rY):
    mu = float(FROZEN_AXES["cma_mu"])
    n_tap = int(FROZEN_AXES["cma_taps"])
    bs = int(FROZEN_AXES["cma_block_size"])
    if cost_name == "godard":
        return runner.standard_cma_godard_with_z(
            rX, rY, n_tap=n_tap, mu=mu, R2=float(FROZEN_AXES["r2_qam16_godard"]),
            block_size=bs,
        )
    if cost_name == "ring_aware":
        return ccv.cma_ring_aware(rX, rY, n_tap=n_tap, mu=mu, block_size=bs)
    if cost_name == "rccma":
        return ccv.cma_rccma(rX, rY, n_tap=n_tap, mu=mu, block_size=bs)
    raise ValueError(f"unknown cost {cost_name!r}")


COSTS = ["godard", "ring_aware", "rccma"]


# ─── step 1: identity tests ──────────────────────────────────────────────────
def run_identity_tests() -> dict[str, Any]:
    """Run the REQUIRED-PASS identity tests; return {passed, n, n_failed}."""
    print("=" * 70)
    print("STEP 1: identity / sanity tests (REQUIRED PASS before any evaluation)")
    print("=" * 70)
    import subprocess
    t0 = time.time()
    proc = subprocess.run(
        [sys.executable, str(HERE / "test_cost_identity.py")],
        capture_output=True, text=True,
    )
    dt = time.time() - t0
    last = [ln for ln in proc.stdout.strip().splitlines() if ln.strip()][-1] if proc.stdout.strip() else "(no output)"
    print(f"  ({dt:.1f}s) {last}")
    if proc.returncode != 0:
        print(proc.stdout)
        print(proc.stderr)
    n_passed = n_failed = 0
    for ln in proc.stdout.splitlines():
        ln = ln.strip()
        if ln.startswith("PASS"):
            n_passed += 1
        elif ln.startswith("FAIL"):
            n_failed += 1
    ok = proc.returncode == 0 and n_failed == 0
    print(f"  identity gate: {'PASS' if ok else 'FAIL'} ({n_passed} passed, {n_failed} failed)")
    return {"passed": bool(ok), "n_passed": n_passed, "n_failed": n_failed,
            "wall_time_seconds": dt}


# ─── one (cell, seed, cost) ──────────────────────────────────────────────────
def _run_one(cell: dict, seed: int, cost_name: str) -> dict[str, Any]:
    """Run one cost on one (cell, seed); return PI-SER + collapse indicator."""
    gamma_bar = float(10.0 ** (cell["snr_db"] / 10.0))
    n_symbols = int(cell["n_symbols"])
    realization = generate_shared_realization_dp(
        n_symbols, FROZEN_AXES["alpha"], FROZEN_AXES["beta"], float(cell["f_g_hz"]),
        sop_rate=float(cell["sop_rate"]), seed=int(seed), gamma_bar=gamma_bar,
        block=int(FROZEN_AXES["block"]), t_s=float(FROZEN_AXES["t_s"]),
        method=str(FROZEN_AXES["method"]), modulation="qam16",
    )
    raw = _run_cost(cost_name, realization["rX"], realization["rY"])
    es, ce, ee, _ = runner.eval_window_for(
        n_symbols, int(FROZEN_AXES["cma_taps"]),
        window_symbols=256, block_size=int(FROZEN_AXES["cma_block_size"]),
    )
    diverged = bool(raw["diverged"])
    result: dict[str, Any] = {
        "seed": int(seed), "cost": cost_name,
        "diverged": diverged,
        "identity_gate": raw["provenance"].get("gradient", ""),
        "final_w_norm": float(raw["final_w_norm"]),
        "init_w_norm": float(raw["init_w_norm"]),
    }
    if diverged:
        # Divergence counts as a failure observation (collapse-equivalent for
        # the collapse_rate metric: a diverged run is certainly not healthy).
        result["collapsed"] = True
        result["pi_ser"] = float(QAM16_RANDOM_CEILING)
        result["mean_eval_power"] = float("nan")
        result["divergence_symbol"] = int(raw["divergence_symbol"]) if raw["divergence_symbol"] is not None else None
        return result

    zX = np.asarray(raw["zX"])
    zY = np.asarray(raw["zY"])
    z_eval_x = zX[ce:ee]
    z_eval_y = zY[ce:ee]
    mean_power = float(np.mean(np.abs(z_eval_x) ** 2 + np.abs(z_eval_y) ** 2))
    collapsed = bool(mean_power < COLLAPSE_POWER_THRESHOLD)

    truth_eval = np.column_stack((
        realization["sX"][ce:ee], realization["sY"][ce:ee],
    ))
    bits_x_eval = realization["bitsX"][ce * 4:ee * 4]
    bits_y_eval = realization["bitsY"][ce * 4:ee * 4]
    m = evaluator.evaluate_dual_16qam(
        z_eval_x, z_eval_y,
        truth_eval[:, 0], truth_eval[:, 1],
        bits_x_eval, bits_y_eval,
    )
    result["collapsed"] = collapsed
    result["pi_ser"] = float(m["pi_ser"])
    result["fixed_label_ser"] = float(m["fixed_label_ser"])
    result["mean_eval_power"] = mean_power
    return result


# ─── step 2: semantic smoke ──────────────────────────────────────────────────
def run_semantic_smoke() -> dict[str, Any]:
    """Three frozen smoke checks. FAIL -> DIAGNOSTIC and STOP."""
    print("\n" + "=" * 70)
    print("STEP 2: semantic smoke (3 frozen checks; FAIL -> DIAGNOSTIC, STOP)")
    print("=" * 70)
    clean = next(c for c in CELLS if c["id"] == "16qam-snr25-nominal-short")
    nominal = next(c for c in CELLS if c["id"] == "16qam-snr20-nominal-short")
    seed0 = SEEDS[0]  # 71

    g_nominal = _run_one(nominal, seed0, "godard")
    g_clean = _run_one(clean, seed0, "godard")
    ra_clean = _run_one(clean, seed0, "ring_aware")
    ra_nominal = _run_one(nominal, seed0, "ring_aware")

    checks = {
        # (a) Godard reproduces the known collapse: a seed collapses
        #     (E|z|^2 < 0.6) on a nominal-SNR cell. seed 71 is known to collapse.
        "smoke_godard_reproduces_collapse_on_seed71": bool(
            g_nominal["collapsed"] or g_nominal["diverged"]
        ),
        # (b) Ring-aware does NOT diverge on the clean cell.
        "smoke_ring_aware_no_diverge_clean": not bool(ra_clean["diverged"]),
        # (c) Ring-aware achieves PI-SER comparable to Godard on clean (not at
        #     the random ceiling 0.9375 = blow-up signature).
        "smoke_ring_aware_pi_ser_below_random_ceiling_clean": bool(
            ra_clean["pi_ser"] < QAM16_RANDOM_CEILING - 1e-9
        ),
    }
    print(f"  godard snr20-seed71: collapsed={g_nominal['collapsed']} div={g_nominal['diverged']} "
          f"E|z|^2={g_nominal['mean_eval_power']:.3f}  (reproduces collapse? {checks['smoke_godard_reproduces_collapse_on_seed71']})")
    print(f"  godard snr25-seed71: pi_ser={g_clean['pi_ser']:.4f} E|z|^2={g_clean['mean_eval_power']:.3f}")
    print(f"  ring_aware snr25-seed71: div={ra_clean['diverged']} pi_ser={ra_clean['pi_ser']:.4f} "
          f"E|z|^2={ra_clean['mean_eval_power']:.3f}  (no div? {checks['smoke_ring_aware_no_diverge_clean']}; "
          f"<ceiling? {checks['smoke_ring_aware_pi_ser_below_random_ceiling_clean']})")
    print(f"  ring_aware snr20-seed71: collapsed={ra_nominal['collapsed']} pi_ser={ra_nominal['pi_ser']:.4f} E|z|^2={ra_nominal['mean_eval_power']:.3f}")
    passed = all(checks.values())
    print(f"  SMOKE: {'PASS' if passed else 'FAIL'}")
    return {"passed": bool(passed), "checks": checks,
            "godard_nominal_seed71": g_nominal, "godard_clean_seed71": g_clean,
            "ring_aware_clean_seed71": ra_clean, "ring_aware_nominal_seed71": ra_nominal}


# ─── step 3: full batch ──────────────────────────────────────────────────────
def _paired_bootstrap_ci(deltas: np.ndarray, *, n_boot: int = 10000, seed: int = 0) -> list[float]:
    """Paired bootstrap 95% CI on the mean of ``deltas``."""
    deltas = np.asarray(deltas, dtype=np.float64)
    n = deltas.size
    if n == 0:
        return [float("nan"), float("nan")]
    rng = np.random.default_rng(seed)
    means = np.array([np.mean(deltas[rng.integers(0, n, n)]) for _ in range(n_boot)])
    return [float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))]


def run_full_batch() -> dict[str, Any]:
    print("\n" + "=" * 70)
    print(f"STEP 3: full batch ({len(CELLS)} cells x {len(SEEDS)} seeds x {len(COSTS)} costs)")
    print("=" * 70)
    cell_results = []
    t_start = time.time()
    # Per-(cell,seed,cost) paired collapse indicators & PI-SER for the bootstrap.
    pair_collapse: dict[str, list[int]] = {c: [] for c in COSTS}
    pair_pi: dict[str, list[float]] = {c: [] for c in COSTS}
    pair_diverge: dict[str, list[int]] = {c: [] for c in COSTS}

    for ci, cell in enumerate(CELLS):
        t0 = time.time()
        per_cost: dict[str, list[dict[str, Any]]] = {c: [] for c in COSTS}
        for seed in SEEDS:
            for cost_name in COSTS:
                row = _run_one(cell, seed, cost_name)
                per_cost[cost_name].append(row)
                # paired arrays (aligned by (cell,seed,cost) order)
                pair_collapse[cost_name].append(int(row["collapsed"]))
                pair_pi[cost_name].append(float(row["pi_ser"]))
                pair_diverge[cost_name].append(int(row["diverged"]))
        dt = time.time() - t0

        agg = {}
        for cost_name in COSTS:
            rows = per_cost[cost_name]
            n_div = sum(1 for r in rows if r["diverged"])
            n_col = sum(1 for r in rows if r["collapsed"])
            pis = [r["pi_ser"] for r in rows]
            pows = [r["mean_eval_power"] for r in rows if not np.isnan(r["mean_eval_power"])]
            agg[cost_name] = {
                "pi_ser_mean": float(np.mean(pis)),
                "collapse_rate": n_col / len(rows),
                "divergence_rate": n_div / len(rows),
                "mean_eval_power_mean": float(np.mean(pows)) if pows else float("nan"),
                "n_seeds": len(rows),
                "n_collapsed": n_col,
                "n_diverged": n_div,
            }
        # per-cell paired deltas vs godard (collapse_rate, pi_ser)
        dcol_ra = agg["ring_aware"]["collapse_rate"] - agg["godard"]["collapse_rate"]
        dcol_rc = agg["rccma"]["collapse_rate"] - agg["godard"]["collapse_rate"]
        dpi_ra = agg["ring_aware"]["pi_ser_mean"] - agg["godard"]["pi_ser_mean"]
        dpi_rc = agg["rccma"]["pi_ser_mean"] - agg["godard"]["pi_ser_mean"]
        cell_results.append({
            "cell_id": cell["id"], "axes": {k: cell[k] for k in
                ("snr_db", "f_g_hz", "sop_rate", "n_symbols")},
            "per_cost": agg,
            "delta_collapse_rate_vs_godard": {"ring_aware": dcol_ra, "rccma": dcol_rc},
            "delta_pi_ser_vs_godard": {"ring_aware": dpi_ra, "rccma": dpi_rc},
            "wall_time_seconds": dt,
        })
        print(f"  [{ci+1:2d}/{len(CELLS)}] {cell['id']:28s} t={dt:5.1f}s  "
              f"GOD pi={agg['godard']['pi_ser_mean']:.4f} col={agg['godard']['collapse_rate']:.2f} div={agg['godard']['divergence_rate']:.2f} | "
              f"RA pi={agg['ring_aware']['pi_ser_mean']:.4f} col={agg['ring_aware']['collapse_rate']:.2f} div={agg['ring_aware']['divergence_rate']:.2f} | "
              f"RC pi={agg['rccma']['pi_ser_mean']:.4f} col={agg['rccma']['collapse_rate']:.2f} div={agg['rccma']['divergence_rate']:.2f}")
    total_dt = time.time() - t_start
    print(f"\n  batch wall time: {total_dt:.1f}s ({total_dt/60:.2f} min)")

    # Macro paired deltas + bootstrap CIs on per-(cell,seed) indicators.
    gcol = np.asarray(pair_collapse["godard"], dtype=np.float64)
    gpi = np.asarray(pair_pi["godard"], dtype=np.float64)
    macro = {}
    for cost_name in ("ring_aware", "rccma"):
        ccol = np.asarray(pair_collapse[cost_name], dtype=np.float64)
        cpi = np.asarray(pair_pi[cost_name], dtype=np.float64)
        # Per-cell paired collapse-rate delta, macro-meaned (hierarchical): use
        # the per-(cell,seed) paired differences for the bootstrap CI (cells+seeds
        # paired), and also report the macro mean of per-cell deltas.
        per_cell_delta_col = [c["delta_collapse_rate_vs_godard"][cost_name] for c in cell_results]
        per_cell_delta_pi = [c["delta_pi_ser_vs_godard"][cost_name] for c in cell_results]
        dcol_pair = ccol - gcol
        dpi_pair = cpi - gpi
        macro[cost_name] = {
            "macro_delta_collapse_rate_vs_godard": float(np.mean(per_cell_delta_col)),
            "macro_delta_collapse_rate_ci95": _paired_bootstrap_ci(dcol_pair),
            "macro_delta_pi_ser_vs_godard": float(np.mean(per_cell_delta_pi)),
            "macro_delta_pi_ser_ci95": _paired_bootstrap_ci(dpi_pair),
            "mean_collapse_rate": float(np.mean(ccol)),
            "mean_pi_ser": float(np.mean(cpi)),
            "mean_divergence_rate": float(np.mean(pair_diverge[cost_name])),
            "frac_pair_collapse_reduced": float(np.mean(dcol_pair < 0)) if dcol_pair.size else float("nan"),
            "frac_pair_pi_improved": float(np.mean(dpi_pair < 0)) if dpi_pair.size else float("nan"),
            "n_paired_cell_seed_points": int(ccol.size),
        }
    macro["godard"] = {
        "mean_collapse_rate": float(np.mean(gcol)),
        "mean_pi_ser": float(np.mean(gpi)),
        "mean_divergence_rate": float(np.mean(pair_diverge["godard"])),
    }
    return {
        "cell_results": cell_results,
        "macro": macro,
        "wall_time_seconds": total_dt,
    }


# ─── decision rule ───────────────────────────────────────────────────────────
def _apply_decision_rule(batch: dict[str, Any]) -> dict[str, Any]:
    """Apply the frozen decision rule for the ring-aware candidate."""
    m = batch["macro"]
    ra = m["ring_aware"]
    MDE = 0.005
    # POSITIVE requires all-of.
    ci_col = ra["macro_delta_collapse_rate_ci95"]
    ci_pi = ra["macro_delta_pi_ser_ci95"]
    positive = (
        ra["macro_delta_collapse_rate_vs_godard"] <= -MDE
        and ci_col[1] < 0.0
        and ra["macro_delta_pi_ser_vs_godard"] <= +MDE
    )
    # BLOWS_UP: diverged on >= 2 cells.
    n_div_cells = sum(1 for c in batch["cell_results"]
                      if c["per_cost"]["ring_aware"]["n_diverged"] > 0)
    blows_up = n_div_cells >= 2
    if positive:
        return {"verdict": "C15_RING_AWARE_REDUCES_COLLAPSE",
                "ring_aware_diverged_cells": n_div_cells}
    if blows_up:
        return {"verdict": "C15_RING_AWARE_BLOWS_UP",
                "ring_aware_diverged_cells": n_div_cells}
    return {"verdict": "C15_RING_AWARE_DOES_NOT_REDUCE_COLLAPSE",
            "ring_aware_diverged_cells": n_div_cells,
            "macro_delta_collapse_rate": ra["macro_delta_collapse_rate_vs_godard"],
            "macro_delta_collapse_rate_ci95": ci_col,
            "macro_delta_pi_ser": ra["macro_delta_pi_ser_vs_godard"]}


# ─── main ────────────────────────────────────────────────────────────────────
def main():
    t0 = time.time()
    identity = run_identity_tests()
    if not identity["passed"]:
        print("\nABORT: identity gate FAILED — cannot trust any Scout result.")
        sys.exit(1)

    smoke = run_semantic_smoke()
    if not smoke["passed"]:
        result = {
            "schema_version": "direction-lab.cb1.c15-reduced-const-cost-scout.v1",
            "campaign_id": "science-scout-2026-07-20.dual-pol-osl",
            "candidate_id": "C15",
            "status": "DIAGNOSTIC_SMOKE_FAILED",
            "claim_ceiling": "DIAGNOSTIC",
            "identity": identity,
            "smoke": {k: v for k, v in smoke.items()},
            "note": "Semantic smoke FAILED — evaluator degenerate/confounded; no Scout inference.",
            "wall_time_seconds": time.time() - t0,
        }
        (ARTIFACTS / "result.v1.json").write_text(
            json.dumps(_jsonable(result), indent=2, sort_keys=True), encoding="utf-8")
        print(f"\nWrote {ARTIFACTS / 'result.v1.json'} (DIAGNOSTIC, smoke failed)")
        return

    batch = run_full_batch()
    decision = _apply_decision_rule(batch)
    result = {
        "schema_version": "direction-lab.cb1.c15-reduced-const-cost-scout.v1",
        "campaign_id": "science-scout-2026-07-20.dual-pol-osl",
        "candidate_id": "C15",
        "status": "EXECUTED",
        "claim_ceiling": "LOCAL_SLICE_DIAGNOSTIC",
        "metric_primary": "PI_SER",
        "metric_secondary": ["collapse_rate", "divergence_rate", "fixed_label_ser"],
        "collapse_power_threshold": COLLAPSE_POWER_THRESHOLD,
        "qam16_random_ceiling": QAM16_RANDOM_CEILING,
        "frozen_axes": FROZEN_AXES,
        "seeds": SEEDS,
        "costs": COSTS,
        "identity": identity,
        "smoke": {k: v for k, v in smoke.items() if k not in
                  ("godard_nominal_seed71", "godard_clean_seed71",
                   "ring_aware_clean_seed71", "ring_aware_nominal_seed71")},
        "smoke_detail": {
            "godard_nominal_seed71": smoke["godard_nominal_seed71"],
            "godard_clean_seed71": smoke["godard_clean_seed71"],
            "ring_aware_clean_seed71": smoke["ring_aware_clean_seed71"],
            "ring_aware_nominal_seed71": smoke["ring_aware_nominal_seed71"],
        },
        "batch": batch,
        "decision": decision,
        "wall_time_seconds": time.time() - t0,
    }
    out = ARTIFACTS / "result.v1.json"
    out.write_text(json.dumps(_jsonable(result), indent=2, sort_keys=True), encoding="utf-8")
    print(f"\nWrote {out}")
    print("\n" + "=" * 70)
    print("VERDICT (ring-aware):", decision["verdict"])
    print("=" * 70)
    m = batch["macro"]
    for cn in ("godard", "ring_aware", "rccma"):
        d = m[cn]
        print(f"  {cn:11s} collapse={d['mean_collapse_rate']:.3f} "
              f"pi={d['mean_pi_ser']:.4f} div={d['mean_divergence_rate']:.3f}")
    ra = m["ring_aware"]
    rc = m["rccma"]
    print(f"\n  ring_aware Δcollapse vs godard = {ra['macro_delta_collapse_rate_vs_godard']:+.5f} "
          f"CI [{ra['macro_delta_collapse_rate_ci95'][0]:+.5f},{ra['macro_delta_collapse_rate_ci95'][1]:+.5f}] "
          f"frac<0={ra['frac_pair_collapse_reduced']:.2f}")
    print(f"  ring_aware Δpi_ser   vs godard = {ra['macro_delta_pi_ser_vs_godard']:+.5f} "
          f"CI [{ra['macro_delta_pi_ser_ci95'][0]:+.5f},{ra['macro_delta_pi_ser_ci95'][1]:+.5f}] "
          f"frac<0={ra['frac_pair_pi_improved']:.2f}")
    print(f"  rccma      Δcollapse vs godard = {rc['macro_delta_collapse_rate_vs_godard']:+.5f} "
          f"CI [{rc['macro_delta_collapse_rate_ci95'][0]:+.5f},{rc['macro_delta_collapse_rate_ci95'][1]:+.5f}]")
    print(f"  rccma      Δpi_ser   vs godard = {rc['macro_delta_pi_ser_vs_godard']:+.5f} "
          f"CI [{rc['macro_delta_pi_ser_ci95'][0]:+.5f},{rc['macro_delta_pi_ser_ci95'][1]:+.5f}]")


if __name__ == "__main__":
    main()
