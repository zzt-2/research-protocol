"""C12 GMI soft-output Scout runner.

Single entry point. Pipeline:
  1. Run the REQUIRED-PASS identity tests (RED -> abort).
  2. Run the semantic smoke (3 frozen checks on clean/collapsed/oracle). FAIL
     -> report DIAGNOSTIC and STOP (per contract).
  3. Run the full batch: 6 cells x 6 seeds. For each (cell, seed):
       fixed-μ CMA (μ=0.03) -> z_eval + truth_eval + truth_bits.
       Shared oracle-affine carrier alignment applied IDENTICALLY to all 3
       demappers (isolates the noise-MODEL comparison).
       3 demappers (standard / mixture / oracle) -> per-bit LLRs.
       GMI (histogram, primary) + GMI (analytic, secondary) per demapper.
  4. Aggregate per-cell (mean over 6 seeds) and macro Δ(mixture - standard).
  5. Write artifacts/result.v1.json.

Reuses (READ-ONLY imports, no modification):
  - generate_shared_realization_dp  (projects/simulation/common/_dual_pol_channel)
  - standard_cma_godard_with_z      (baseline-atlas/cb1_cell_runner)
  - eval_window_for                 (baseline-atlas/cb1_cell_runner)
  - oracle_affine_bound_16qam       (baseline-atlas/cb1_evaluator) [shared alignment]
  - hard_16qam                      (baseline-atlas/cb1_evaluator) [for σ² blind estimate]
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
# HERE.parents[6] = worktree root (src->c12->cb1-closure->scout->dir-lab->thesis-fso->projects->root)
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
import soft_demap as sd  # noqa: E402
import gmi  # noqa: E402

SCOUT_DIR = HERE.parent                                   # c12-gmi-soft-output-scout
ARTIFACTS = SCOUT_DIR / "artifacts"
ARTIFACTS.mkdir(parents=True, exist_ok=True)


# ─── Frozen contract (mirrors batch-contract.v1.yaml) ────────────────────────
FROZEN_AXES = {
    "alpha": 4.2, "beta": 1.4, "block": 100, "t_s": 4e-10, "method": "gar",
    "cma_mu": 0.03, "cma_taps": 11, "r2_qam16": 1.32, "cma_block_size": 64,
}
AFFINE_RIDGE = 1e-6
SEEDS = [71, 72, 73, 74, 75, 76]
CELLS = [
    {"id": "snr05-nominal-short", "modulation": "qam16", "snr_db": 5.0,  "f_g_hz": 30.0,  "sop_rate": 4e-6, "n_symbols": 512},
    {"id": "snr15-nominal-short", "modulation": "qam16", "snr_db": 15.0, "f_g_hz": 30.0,  "sop_rate": 4e-6, "n_symbols": 512},
    {"id": "snr20-nominal-short", "modulation": "qam16", "snr_db": 20.0, "f_g_hz": 30.0,  "sop_rate": 4e-6, "n_symbols": 512},
    {"id": "snr25-nominal-short", "modulation": "qam16", "snr_db": 25.0, "f_g_hz": 30.0,  "sop_rate": 4e-6, "n_symbols": 512},
    {"id": "snr20-fg100-short",   "modulation": "qam16", "snr_db": 20.0, "f_g_hz": 100.0, "sop_rate": 4e-6, "n_symbols": 512},
    {"id": "snr15-fg1000-long",   "modulation": "qam16", "snr_db": 15.0, "f_g_hz": 1000.0,"sop_rate": 4e-6, "n_symbols": 8192},
]
GMI_BINS = 16


# ─── helpers ─────────────────────────────────────────────────────────────────
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


def _truth_bits_for_eval(realization: dict, ce: int, ee: int) -> np.ndarray:
    """TX truth bits for the eval window, shape (N_eval, 4), int8.

    The generator's ``bitsX``/``bitsY`` are flat 4*len(symbols) arrays
    (Gray 16QAM, 4 bits/symbol). We stack both polarizations into one stream
    of (2*N_eval, 4) for the GMI estimation (pooling both pols doubles the
    sample count for the histogram MI, which is sample-hungry).
    """
    bx = np.asarray(realization["bitsX"][ce * 4:ee * 4], dtype=np.int8).reshape(-1, 4)
    by = np.asarray(realization["bitsY"][ce * 4:ee * 4], dtype=np.int8).reshape(-1, 4)
    return np.vstack([bx, by])


def _eval_streams(realization: dict, raw: dict, es: int, ce: int, ee: int):
    """Return (z_eval_aligned, truth_eval) each shape (2*N_eval,) complex, dual-pol stacked.

    Applies the shared oracle-affine carrier alignment (dual-pol 2x2 fit on the
    calibration slice, applied to the eval slice) IDENTICALLY to the returned
    z for all three demappers. truth_eval is the on-grid TX truth.
    """
    zX, zY = np.asarray(raw["zX"]), np.asarray(raw["zY"])
    z_calib = np.column_stack((zX[es:ce], zY[es:ce]))
    z_eval = np.column_stack((zX[ce:ee], zY[ce:ee]))
    truth_calib = np.column_stack((
        realization["sX"][es:ce], realization["sY"][es:ce],
    ))
    truth_eval = np.column_stack((
        realization["sX"][ce:ee], realization["sY"][ce:ee],
    ))
    # Shared carrier alignment (oracle-affine, dual-pol). Applied to z_eval.
    z_eval_aligned = evaluator.oracle_affine_bound_16qam(
        z_calib, z_eval, truth_calib, ridge=AFFINE_RIDGE,
    )
    # Stack both polarizations into one stream.
    z_flat = np.concatenate([z_eval_aligned[:, 0], z_eval_aligned[:, 1]])
    s_flat = np.concatenate([truth_eval[:, 0], truth_eval[:, 1]])
    return z_flat, s_flat, z_eval_aligned, truth_eval


def _blind_sigma2(z_calib_flat: np.ndarray) -> float:
    """Blind per-symbol noise variance from calib residuals (z - hard_16qam).

    Standard-demapper input. Uses only z + the public alphabet (no TX truth).
    """
    hard = evaluator.hard_16qam(z_calib_flat)
    resid = z_calib_flat - hard
    s2 = float(np.mean(np.abs(resid) ** 2))
    return max(s2, 1e-9)


def _demap_all_three(z_eval_flat, s_eval_flat, z_calib_flat):
    """Run all three demappers on the SAME aligned z_eval.

    Returns dict of {standard, mixture, oracle} -> (N,4) LLRs.
    Standard & mixture use the SAME blind calib-derived σ² / mixture params
    (fit on z_calib). Oracle uses truth-conditioned variance on z_eval (Kill).
    """
    sigma2 = _blind_sigma2(z_calib_flat)
    llr_std = sd.maxlog_soft_demap_16qam(z_eval_flat, sigma2)
    llr_mix, mix_info = sd.mixture_soft_demap_16qam(z_calib_flat, z_eval_flat)
    llr_ora = sd.oracle_soft_demap_16qam(z_eval_flat, s_eval_flat)
    return {
        "standard": llr_std,
        "mixture": llr_mix,
        "oracle": llr_ora,
        "diagnostics": {
            "blind_sigma2": sigma2,
            "mix_re": {"w": mix_info["re"]["w"].tolist(),
                       "mu": mix_info["re"]["mu"].tolist(),
                       "var": mix_info["re"]["var"].tolist()},
            "mix_im": {"w": mix_info["im"]["w"].tolist(),
                       "mu": mix_info["im"]["mu"].tolist(),
                       "var": mix_info["im"]["var"].tolist()},
        },
    }


def _gmi_for(llrs: np.ndarray, bits: np.ndarray) -> dict[str, Any]:
    """Primary (histogram) + secondary (analytic) GMI for one demapper's LLRs."""
    return {
        "histogram": gmi.compute_gmi(llrs, bits, n_bins=GMI_BINS),
        "analytic": gmi.compute_gmi_analytic(llrs, bits),
    }


# ─── step 1: identity tests ──────────────────────────────────────────────────
def run_identity_tests() -> dict[str, Any]:
    """Run the REQUIRED-PASS identity tests; return {passed, n, n_failed}."""
    print("=" * 70)
    print("STEP 1: identity / sanity tests (REQUIRED PASS before any evaluation)")
    print("=" * 70)
    import subprocess
    t0 = time.time()
    # Run as a subprocess to mirror pytest semantics and isolate sys.path.
    proc = subprocess.run(
        [sys.executable, str(HERE / "test_soft_demap_identity.py")],
        capture_output=True, text=True,
    )
    dt = time.time() - t0
    # The standalone runner prints "N passed, M failed" on the last line.
    last = [ln for ln in proc.stdout.strip().splitlines() if ln.strip()][-1]
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


# ─── step 2: semantic smoke ──────────────────────────────────────────────────
def _run_one_seed_gmi(cell: dict, seed: int) -> dict[str, Any]:
    """Run CMA + 3 demappers + GMI for one (cell, seed). Returns per-demapper GMI."""
    gamma_bar = float(10.0 ** (cell["snr_db"] / 10.0))
    n_symbols = int(cell["n_symbols"])
    realization = generate_shared_realization_dp(
        n_symbols, FROZEN_AXES["alpha"], FROZEN_AXES["beta"], float(cell["f_g_hz"]),
        sop_rate=float(cell["sop_rate"]), seed=int(seed), gamma_bar=gamma_bar,
        block=int(FROZEN_AXES["block"]), t_s=float(FROZEN_AXES["t_s"]),
        method=str(FROZEN_AXES["method"]), modulation="qam16",
    )
    raw = runner.standard_cma_godard_with_z(
        realization["rX"], realization["rY"],
        n_tap=int(FROZEN_AXES["cma_taps"]), mu=float(FROZEN_AXES["cma_mu"]),
        R2=float(FROZEN_AXES["r2_qam16"]), block_size=int(FROZEN_AXES["cma_block_size"]),
    )
    es, ce, ee, _ = runner.eval_window_for(
        n_symbols, int(FROZEN_AXES["cma_taps"]),
        window_symbols=256, block_size=int(FROZEN_AXES["cma_block_size"]),
    )
    diverged = bool(raw["diverged"])
    result: dict[str, Any] = {
        "seed": int(seed), "diverged": diverged,
        "identity_gate": raw["provenance"].get("gradient", ""),
    }
    if diverged:
        return result
    z_eval_flat, s_eval_flat, _, _ = _eval_streams(realization, raw, es, ce, ee)
    # Calib stream (dual-pol stacked) for blind σ² / mixture fit.
    zX, zY = np.asarray(raw["zX"]), np.asarray(raw["zY"])
    z_calib_flat = np.concatenate([zX[es:ce], zY[es:ce]])
    bits_eval = _truth_bits_for_eval(realization, ce, ee)
    demap = _demap_all_three(z_eval_flat, s_eval_flat, z_calib_flat)
    diag = demap.pop("diagnostics")
    result["gmi"] = {
        name: _gmi_for(llrs, bits_eval) for name, llrs in demap.items()
    }
    result["diagnostics"] = diag
    result["n_eval_samples"] = int(len(z_eval_flat))
    return result


def run_semantic_smoke() -> dict[str, Any]:
    """Three frozen smoke checks. FAIL -> DIAGNOSTIC and STOP."""
    print("\n" + "=" * 70)
    print("STEP 2: semantic smoke (3 frozen checks; FAIL -> DIAGNOSTIC, STOP)")
    print("=" * 70)
    clean = next(c for c in CELLS if c["id"] == "snr25-nominal-short")
    collapsed = next(c for c in CELLS if c["id"] == "snr05-nominal-short")
    # Use the first seed for the smoke (fast).
    r_clean = _run_one_seed_gmi(clean, SEEDS[0])
    r_coll = _run_one_seed_gmi(collapsed, SEEDS[0])
    if r_clean.get("diverged") or r_coll.get("diverged"):
        print("  SMOKE FAIL: a smoke cell diverged — cannot evaluate.")
        return {"passed": False, "reason": "smoke_cell_diverged",
                "clean": r_clean, "collapsed": r_coll}
    g_clean_std = r_clean["gmi"]["standard"]["histogram"]["gmi"]
    g_coll_std = r_coll["gmi"]["standard"]["histogram"]["gmi"]
    # oracle >= standard on both smoke cells
    ora_ge_std_clean = r_clean["gmi"]["oracle"]["histogram"]["gmi"] >= g_clean_std - 1e-9
    ora_ge_std_coll = r_coll["gmi"]["oracle"]["histogram"]["gmi"] >= g_coll_std - 1e-9

    checks = {
        "smoke_clean_standard_gmi_gt_3p0": g_clean_std > 3.0,
        "smoke_collapsed_standard_gmi_lower": g_coll_std < g_clean_std - 0.5,
        "smoke_oracle_ge_standard_all_cells": ora_ge_std_clean and ora_ge_std_coll,
    }
    print(f"  clean   (snr25) standard GMI = {g_clean_std:.4f}  (>3.0 ? {checks['smoke_clean_standard_gmi_gt_3p0']})")
    print(f"  collaps (snr05) standard GMI = {g_coll_std:.4f}  (lower by {g_clean_std-g_coll_std:.4f} ? {checks['smoke_collapsed_standard_gmi_lower']})")
    print(f"  oracle >= standard on both   ? {checks['smoke_oracle_ge_standard_all_cells']}")
    passed = all(checks.values())
    print(f"  SMOKE: {'PASS' if passed else 'FAIL'}")
    return {"passed": bool(passed), "checks": checks,
            "clean_standard_gmi": g_clean_std, "collapsed_standard_gmi": g_coll_std,
            "clean": r_clean, "collapsed": r_coll}


# ─── step 3: full batch ──────────────────────────────────────────────────────
def _paired_bootstrap_ci(deltas: np.ndarray, *, n_boot: int = 10000, seed: int = 0) -> list[float]:
    """Paired bootstrap 95% CI on the mean of ``deltas`` (cells+seeds paired)."""
    deltas = np.asarray(deltas, dtype=np.float64)
    n = deltas.size
    if n == 0:
        return [float("nan"), float("nan")]
    rng = np.random.default_rng(seed)
    means = np.array([np.mean(deltas[rng.integers(0, n, n)]) for _ in range(n_boot)])
    return [float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))]


def run_full_batch() -> dict[str, Any]:
    print("\n" + "=" * 70)
    print("STEP 3: full batch (6 cells x 6 seeds)")
    print("=" * 70)
    cell_results = []
    t_start = time.time()
    all_pair_dmix: list[float] = []   # per-(cell,seed) Δ(mixture-standard)
    all_pair_dora: list[float] = []   # per-(cell,seed) Δ(oracle-standard)
    for ci, cell in enumerate(CELLS):
        t0 = time.time()
        per_seed = []
        for seed in SEEDS:
            per_seed.append(_run_one_seed_gmi(cell, seed))
        dt = time.time() - t0
        # Aggregate per-cell: mean histogram GMI per demapper over non-diverged seeds.
        valid = [r for r in per_seed if "gmi" in r]
        n_div = sum(1 for r in per_seed if r.get("diverged"))
        agg = {}
        for name in ("standard", "mixture", "oracle"):
            gmis = [r["gmi"][name]["histogram"]["gmi"] for r in valid]
            gmis_ana = [r["gmi"][name]["analytic"]["gmi"] for r in valid]
            agg[name] = {
                "gmi_hist_mean": float(np.mean(gmis)) if gmis else float("nan"),
                "gmi_ana_mean": float(np.mean(gmis_ana)) if gmis_ana else float("nan"),
            }
        delta_mix_std = agg["mixture"]["gmi_hist_mean"] - agg["standard"]["gmi_hist_mean"]
        delta_ora_std = agg["oracle"]["gmi_hist_mean"] - agg["standard"]["gmi_hist_mean"]
        recovery_frac = (delta_mix_std / delta_ora_std) if abs(delta_ora_std) > 1e-12 else float("nan")
        # Collect per-(cell,seed) paired deltas for the macro bootstrap CI.
        for r in valid:
            all_pair_dmix.append(r["gmi"]["mixture"]["histogram"]["gmi"] - r["gmi"]["standard"]["histogram"]["gmi"])
            all_pair_dora.append(r["gmi"]["oracle"]["histogram"]["gmi"] - r["gmi"]["standard"]["histogram"]["gmi"])
        # mean diagnostics over seeds
        diag_means = {}
        if valid:
            ws_re = np.mean([r["diagnostics"]["mix_re"]["w"] for r in valid], axis=0)
            ws_im = np.mean([r["diagnostics"]["mix_im"]["w"] for r in valid], axis=0)
            vs_re = np.mean([r["diagnostics"]["mix_re"]["var"] for r in valid], axis=0)
            blind = float(np.mean([r["diagnostics"]["blind_sigma2"] for r in valid]))
            diag_means = {"mix_re_w": ws_re.tolist(), "mix_im_w": ws_im.tolist(),
                          "mix_re_var": vs_re.tolist(), "blind_sigma2_mean": blind}
        cell_results.append({
            "cell_id": cell["id"], "axes": {k: cell[k] for k in
                ("snr_db", "f_g_hz", "sop_rate", "n_symbols")},
            "n_seeds_valid": len(valid), "n_seeds_diverged": n_div,
            "gmi": agg,
            "delta_mixture_minus_standard": delta_mix_std,
            "delta_oracle_minus_standard": delta_ora_std,
            "recovery_fraction_of_oracle_headroom": recovery_frac,
            "diagnostics_mean": diag_means,
            "wall_time_seconds": dt,
        })
        g = agg
        print(f"  [{ci+1}/{len(CELLS)}] {cell['id']:22s} t={dt:5.1f}s "
              f"std={g['standard']['gmi_hist_mean']:.3f} "
              f"mix={g['mixture']['gmi_hist_mean']:.3f} "
              f"ora={g['oracle']['gmi_hist_mean']:.3f} "
              f"Δ(mix-std)={delta_mix_std:+.4f} "
              f"Δ(ora-std)={delta_ora_std:+.4f} "
              f"rec={recovery_frac if not np.isnan(recovery_frac) else float('nan'):.2f} "
              f"(div={n_div})")
    total_dt = time.time() - t_start
    print(f"\n  batch wall time: {total_dt:.1f}s ({total_dt/60:.2f} min)")

    # Macro Δ over cells (paired by cell).
    macro_mix_std = float(np.mean([c["delta_mixture_minus_standard"] for c in cell_results]))
    macro_ora_std = float(np.mean([c["delta_oracle_minus_standard"] for c in cell_results]))
    # Paired bootstrap CIs on the per-(cell,seed) deltas (cells+seeds paired).
    dmx = np.asarray(all_pair_dmix, dtype=np.float64)
    dor = np.asarray(all_pair_dora, dtype=np.float64)
    ci_mix = _paired_bootstrap_ci(dmx)
    ci_ora = _paired_bootstrap_ci(dor)
    frac_mix_pos = float(np.mean(dmx > 0)) if dmx.size else float("nan")
    frac_ora_pos = float(np.mean(dor > 0)) if dor.size else float("nan")
    # Macro recovery restricted to cells where oracle shows headroom.
    headroom_cells = [c for c in cell_results if c["delta_oracle_minus_standard"] > 1e-6]
    macro_recovery = (float(np.mean([c["recovery_fraction_of_oracle_headroom"] for c in headroom_cells]))
                      if headroom_cells else float("nan"))
    return {
        "cell_results": cell_results,
        "macro": {
            "delta_mixture_minus_standard": macro_mix_std,
            "delta_mixture_minus_standard_ci95": ci_mix,
            "delta_mixture_minus_standard_frac_positive": frac_mix_pos,
            "delta_oracle_minus_standard": macro_ora_std,
            "delta_oracle_minus_standard_ci95": ci_ora,
            "delta_oracle_minus_standard_frac_positive": frac_ora_pos,
            "macro_recovery_fraction_of_oracle_headroom": macro_recovery,
            "n_cells_with_oracle_headroom": len(headroom_cells),
            "n_paired_cell_seed_points": int(dmx.size),
        },
        "wall_time_seconds": total_dt,
    }


# ─── main ────────────────────────────────────────────────────────────────────
def main():
    t0 = time.time()
    identity = run_identity_tests()
    if not identity["passed"]:
        print("\nABORT: identity gate FAILED — cannot trust any Scout result.")
        sys.exit(1)

    smoke = run_semantic_smoke()
    if not smoke["passed"]:
        # Write a DIAGNOSTIC-only artifact and stop (per contract).
        result = {
            "schema_version": "direction-lab.cb1.c12-gmi-soft-output-scout.v1",
            "campaign_id": "science-scout-2026-07-20.dual-pol-osl",
            "status": "DIAGNOSTIC_SMOKE_FAILED",
            "claim_ceiling": "DIAGNOSTIC",
            "identity": identity,
            "smoke": smoke,
            "note": "Semantic smoke FAILED — evaluator degenerate/confounded; no Scout inference.",
            "wall_time_seconds": time.time() - t0,
        }
        (ARTIFACTS / "result.v1.json").write_text(
            json.dumps(_jsonable(result), indent=2, sort_keys=True), encoding="utf-8")
        print(f"\nWrote {ARTIFACTS / 'result.v1.json'} (DIAGNOSTIC, smoke failed)")
        return

    batch = run_full_batch()
    result = {
        "schema_version": "direction-lab.cb1.c12-gmi-soft-output-scout.v1",
        "campaign_id": "science-scout-2026-07-20.dual-pol-osl",
        "candidate_id": "C12",
        "status": "EXECUTED",
        "claim_ceiling": "LOCAL_SLICE",
        "metric_primary": "histogram_GMI_bits_per_symbol",
        "metric_ceiling": 4.0,
        "frozen_axes": FROZEN_AXES,
        "seeds": SEEDS,
        "n_bins_histogram": GMI_BINS,
        "identity": identity,
        "smoke": {k: v for k, v in smoke.items() if k not in ("clean", "collapsed")},
        "batch": batch,
        "wall_time_seconds": time.time() - t0,
    }
    out = ARTIFACTS / "result.v1.json"
    out.write_text(json.dumps(_jsonable(result), indent=2, sort_keys=True), encoding="utf-8")
    print(f"\nWrote {out}")
    m = batch["macro"]
    print(f"\nMacro Δ(mixture - standard) = {m['delta_mixture_minus_standard']:+.5f} bits/symbol "
          f"95% CI [{m['delta_mixture_minus_standard_ci95'][0]:+.5f},{m['delta_mixture_minus_standard_ci95'][1]:+.5f}] "
          f"frac>0={m['delta_mixture_minus_standard_frac_positive']:.2f}")
    print(f"Macro Δ(oracle  - standard) = {m['delta_oracle_minus_standard']:+.5f} bits/symbol "
          f"95% CI [{m['delta_oracle_minus_standard_ci95'][0]:+.5f},{m['delta_oracle_minus_standard_ci95'][1]:+.5f}] "
          f"frac>0={m['delta_oracle_minus_standard_frac_positive']:.2f}")
    print(f"Macro recovery fraction    = {m['macro_recovery_fraction_of_oracle_headroom']:.3f} "
          f"(n_cells_with_oracle_headroom={m['n_cells_with_oracle_headroom']})")


if __name__ == "__main__":
    main()
