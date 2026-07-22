"""C14 init-strategy Scout runner.

Single entry point. Pipeline:
  1. Run the REQUIRED-PASS identity tests (RED -> abort).
  2. Run the semantic smoke (3 frozen checks). FAIL -> report DIAGNOSTIC, STOP.
  3. Run the full batch: 11 cells x 10 seeds x 4 inits. For each (cell, seed):
       - generate the shared dual-pol realization (frozen axes, mu=0.03).
       - estimate 4 inits from the SAME calibration region of the received signal:
           center_tap  | whitening (r) | oracle_wiener (r+truth, Kill) | multistart (r)
       - run the SAME Godard-with-z CMA from each init (only w_init differs).
       - score the converged tail on the SAME frozen PI-SER eval window.
  4. Aggregate per-cell (mean PI-SER over 10 seeds, collapse_rate, divergence_rate)
     and the oracle-escape test (does oracle init escape center-tap's collapses?).
  5. Paired bootstrap adjudication: candidate collapse_rate vs center per cell.
  6. Write artifacts/result.v1.json.

The scientific question is init-dependence: is the inner-ring collapse a
property of (center-tap + Godard) or of the Godard cost alone? The oracle
Wiener init is the kill bound — if it ALSO collapses, C14 is closed.

Reuses (READ-ONLY imports, no modification):
  - generate_shared_realization_dp  (projects/simulation/common/_dual_pol_channel)
  - eval_window_for                 (baseline-atlas/cb1_cell_runner)
  - hard_16qam, evaluate_dual_16qam (baseline-atlas/cb1_evaluator)
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

# ─── path bootstrap ───────────────────────────────────────────────────────────
HERE = Path(__file__).resolve().parent                       # .../src
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
SIM_DIR = HERE.parents[6] / "projects" / "simulation"
if str(SIM_DIR) not in sys.path:
    sys.path.insert(0, str(SIM_DIR))
BASELINE_ATLAS = HERE.parents[1] / "baseline-atlas"
if str(BASELINE_ATLAS) not in sys.path:
    sys.path.insert(0, str(BASELINE_ATLAS))

from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402
import cb1_cell_runner as anchor  # noqa: E402  (eval_window_for)
import cb1_evaluator as evaluator  # noqa: E402  (hard_16qam, evaluate_dual_16qam)
import cma_custom_init as ci  # noqa: E402

SCOUT_DIR = HERE.parent                                   # c14-init-strategy-scout
ARTIFACTS = SCOUT_DIR / "artifacts"
ARTIFACTS.mkdir(parents=True, exist_ok=True)

# ─── Frozen contract (mirrors batch-contract.v1.yaml) ─────────────────────────
FROZEN_AXES = {
    "alpha": 4.2, "beta": 1.4, "block": 100, "t_s": 4e-10, "method": "gar",
    "cma_mu": 0.03, "cma_taps": 11, "r2_qam16": 1.32, "cma_block_size": 64,
}
MU = FROZEN_AXES["cma_mu"]
N_TAP = FROZEN_AXES["cma_taps"]
R2 = FROZEN_AXES["r2_qam16"]
BLOCK = FROZEN_AXES["cma_block_size"]
COLLAPSE_PI_SER = 0.3          # matches B01 collapse label (oracle_pi_ser>0.3)
ORACLE_ESCAPE_PI_SER = 0.1     # oracle "escapes" if it reaches <= this
SEEDS = [71, 72, 73, 74, 75, 76, 77, 78, 79, 80]
MULTISTART_K = 5
MULTISTART_WARMUP = 1

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
INIT_IDS = ["center_tap", "whitening", "multistart", "oracle_wiener"]


# ─── helpers ──────────────────────────────────────────────────────────────────
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


def _pi_ser_for_eval(realization: dict, raw: dict, ce: int, ee: int) -> tuple[float, str]:
    """Score the converged tail on the frozen PI-SER eval window.

    Returns (pi_ser, status) where status is 'ok' | 'diverged' | 'nan'."""
    if raw["diverged"]:
        return float("nan"), "diverged"
    zX = np.asarray(raw["zX"]); zY = np.asarray(raw["zY"])
    z_eval = np.column_stack((zX[ce:ee], zY[ce:ee]))
    truth_eval = np.column_stack((realization["sX"][ce:ee], realization["sY"][ce:ee]))
    bitsx = realization["bitsX"][ce * 4:ee * 4]
    bitsy = realization["bitsY"][ce * 4:ee * 4]
    pred = evaluator.hard_16qam(z_eval)
    m = evaluator.evaluate_dual_16qam(
        pred[:, 0], pred[:, 1], truth_eval[:, 0], truth_eval[:, 1], bitsx, bitsy,
    )
    pi = float(m["pi_ser"])
    if not np.isfinite(pi):
        return float("nan"), "nan"
    return pi, "ok"


def _estimate_inits(realization: dict, n_symbols: int, eval_start: int) -> dict[str, dict]:
    """Estimate the 4 init vectors from the SAME received-signal calibration region.

    The calibration region is the received signal from the L-tap warmup prefix
    up to eval_start (the region whose later blocks are scored). For each
    realization this region is computed ONCE and reused for every init, so the
    comparison is purely over the init DIRECTION (whitening/multistart/oracle
    see the same r window; oracle additionally sees truth on that window)."""
    rX = np.asarray(realization["rX"], dtype=complex)
    rY = np.asarray(realization["rY"], dtype=complex)
    half = N_TAP // 2
    # Calibration window: from the first valid window (offset half) up to
    # eval_start, capped at a generous length (>= 2*block_size).
    lo = half
    hi = max(lo + 2 * BLOCK, min(eval_start, n_symbols))
    rX_calib = rX[lo:hi]
    rY_calib = rY[lo:hi]
    sX_calib = np.asarray(realization["sX"], dtype=complex)[lo:hi]
    sY_calib = np.asarray(realization["sY"], dtype=complex)[lo:hi]

    inits: dict[str, dict] = {}
    inits["center_tap"] = ci.center_tap_init(N_TAP)
    inits["whitening"] = ci.whitening_init(rX_calib, rY_calib, n_tap=N_TAP)
    inits["oracle_wiener"] = ci.oracle_wiener_init(
        rX_calib, rY_calib, sX_calib, sY_calib, n_tap=N_TAP,
    )
    # Deterministic per-realization rng (seeded by the realization seed for
    # reproducibility; NOT a function of TX truth).
    rseed = int(realization.get("seed", 0)) * 7919 + 17
    rng = np.random.default_rng(rseed)
    ms_init, ms_costs = ci.random_multistart_init(
        rX_calib, rY_calib, n_tap=N_TAP, mu=MU, R2=R2, block_size=BLOCK,
        K=MULTISTART_K, warmup_blocks=MULTISTART_WARMUP, rng=rng,
    )
    inits["multistart"] = ms_init
    inits["_multistart_costs"] = {"costs": ms_costs}  # diagnostic only
    return inits


def _run_one(realization: dict, init: dict, n_symbols: int, es: int, ce: int, ee: int) -> dict:
    """Run the Godard-with-z CMA from one init and score PI-SER."""
    raw = ci.standard_cma_godard_with_z_custom_init(
        realization["rX"], realization["rY"],
        n_tap=N_TAP, mu=MU, R2=R2, block_size=BLOCK, w_init=init,
    )
    pi, status = _pi_ser_for_eval(realization, raw, ce, ee)
    return {
        "pi_ser": pi,
        "status": status,
        "diverged": bool(raw["diverged"]),
        "init_w_norm": float(raw["init_w_norm"]),
        "final_w_norm": float(raw["final_w_norm"]),
        "provenance_gradient": raw["provenance"]["gradient"],
    }


# ─── Semantic smoke ───────────────────────────────────────────────────────────
def run_semantic_smoke() -> dict[str, Any]:
    """Three frozen checks (batch-contract semantic_smoke)."""
    checks: dict[str, Any] = {}
    # Use snr25-nominal-short (the strongest collapse cell) for the collapse
    # reproduction check, seeds 71-72 (one collapses, one converges).
    cell = CELLS[4]  # 16qam-snr25-nominal-short
    gamma = 10.0 ** (cell["snr_db"] / 10.0)
    es, ce, ee, half = anchor.eval_window_for(
        cell["n_symbols"], N_TAP, window_symbols=256, block_size=BLOCK,
    )
    # check 1: center-tap reproduces the bimodal collapse.
    ct_pis = []
    for seed in (71, 72, 73, 74):
        r = generate_shared_realization_dp(
            cell["n_symbols"], FROZEN_AXES["alpha"], FROZEN_AXES["beta"],
            cell["f_g_hz"], sop_rate=cell["sop_rate"], seed=seed,
            gamma_bar=gamma, block=FROZEN_AXES["block"], t_s=FROZEN_AXES["t_s"],
            method=FROZEN_AXES["method"], modulation="qam16",
        )
        out = _run_one(r, ci.center_tap_init(N_TAP), cell["n_symbols"], es, ce, ee)
        ct_pis.append(out["pi_ser"])
    n_collapsed = sum(1 for p in ct_pis if p > COLLAPSE_PI_SER)
    checks["smoke_center_tap_reproduces_collapse"] = {
        "cell": cell["id"], "seeds": [71, 72, 73, 74], "center_pi_ser": ct_pis,
        "n_collapsed": n_collapsed, "pass": n_collapsed >= 1 and any(p < 0.05 for p in ct_pis),
    }
    # check 2: center-tap identity (byte-for-byte) — done in identity tests;
    # re-assert here against the anchor for the smoke cell.
    r = generate_shared_realization_dp(
        cell["n_symbols"], FROZEN_AXES["alpha"], FROZEN_AXES["beta"],
        cell["f_g_hz"], sop_rate=cell["sop_rate"], seed=71, gamma_bar=gamma,
        block=FROZEN_AXES["block"], t_s=FROZEN_AXES["t_s"],
        method=FROZEN_AXES["method"], modulation="qam16",
    )
    ref = anchor.standard_cma_godard_with_z(
        r["rX"], r["rY"], n_tap=N_TAP, mu=MU, R2=R2, block_size=BLOCK,
    )
    ct = ci.standard_cma_godard_with_z_custom_init(
        r["rX"], r["rY"], n_tap=N_TAP, mu=MU, R2=R2, block_size=BLOCK,
        w_init=ci.center_tap_init(N_TAP),
    )
    dz = float(max(
        np.max(np.abs(np.asarray(ref["zX"]) - np.asarray(ct["zX"]))),
        np.max(np.abs(np.asarray(ref["zY"]) - np.asarray(ct["zY"]))),
    ))
    checks["smoke_center_tap_identity"] = {
        "max_abs_dz": dz, "pass": dz == 0.0,
    }
    # check 3: oracle init is sensible (finite, non-degenerate) and report
    # whether it escapes the collapse on the collapsed seed(s).
    oracle_pis = {}
    for seed in (71, 72, 73, 74):
        r = generate_shared_realization_dp(
            cell["n_symbols"], FROZEN_AXES["alpha"], FROZEN_AXES["beta"],
            cell["f_g_hz"], sop_rate=cell["sop_rate"], seed=seed, gamma_bar=gamma,
            block=FROZEN_AXES["block"], t_s=FROZEN_AXES["t_s"],
            method=FROZEN_AXES["method"], modulation="qam16",
        )
        inits = _estimate_inits(r, cell["n_symbols"], es)
        ow = inits["oracle_wiener"]
        finite = all(np.all(np.isfinite(ow[k])) for k in ("wxx", "wxy", "wyx", "wyy"))
        norm = ci.init_norm(ow)
        out = _run_one(r, ow, cell["n_symbols"], es, ce, ee)
        oracle_pis[seed] = {"pi_ser": out["pi_ser"], "finite": finite, "norm": norm}
    # oracle escapes if on the collapsed center-tap seeds it reaches low PI-SER
    collapsed_ct_seeds = [71 + i for i, p in enumerate(ct_pis) if p > COLLAPSE_PI_SER]
    oracle_escapes_collapsed = [
        s for s in collapsed_ct_seeds
        if oracle_pis[s]["pi_ser"] <= ORACLE_ESCAPE_PI_SER
    ]
    checks["smoke_oracle_init_is_sensible"] = {
        "oracle_pi_ser": {str(s): oracle_pis[s]["pi_ser"] for s in oracle_pis},
        "oracle_finite": all(oracle_pis[s]["finite"] for s in oracle_pis),
        "oracle_norm": {str(s): oracle_pis[s]["norm"] for s in oracle_pis},
        "collapsed_ct_seeds": collapsed_ct_seeds,
        "oracle_escapes_collapsed_seeds": oracle_escapes_collapsed,
        "pass": all(oracle_pis[s]["finite"] for s in oracle_pis),
    }
    all_pass = all(checks[k]["pass"] for k in checks)
    return {"all_pass": all_pass, "checks": checks}


# ─── Full batch ───────────────────────────────────────────────────────────────
def run_batch(verbose: bool = True) -> dict[str, Any]:
    cell_results = []
    t_start = time.time()
    for ci_idx, cell in enumerate(CELLS):
        gamma = 10.0 ** (cell["snr_db"] / 10.0)
        es, ce, ee, half = anchor.eval_window_for(
            cell["n_symbols"], N_TAP, window_symbols=256, block_size=BLOCK,
        )
        per_seed: list[dict[str, Any]] = []
        t0 = time.time()
        for seed in SEEDS:
            realization = generate_shared_realization_dp(
                cell["n_symbols"], FROZEN_AXES["alpha"], FROZEN_AXES["beta"],
                cell["f_g_hz"], sop_rate=cell["sop_rate"], seed=seed,
                gamma_bar=gamma, block=FROZEN_AXES["block"], t_s=FROZEN_AXES["t_s"],
                method=FROZEN_AXES["method"], modulation="qam16",
            )
            inits = _estimate_inits(realization, cell["n_symbols"], es)
            ms_costs = inits.pop("_multistart_costs", None)
            seed_row: dict[str, Any] = {"seed": int(seed)}
            for init_id in INIT_IDS:
                seed_row[init_id] = _run_one(realization, inits[init_id], cell["n_symbols"], es, ce, ee)
            if ms_costs is not None:
                seed_row["multistart_warmup_costs"] = ms_costs
            per_seed.append(seed_row)
        # Aggregate per init.
        agg: dict[str, Any] = {}
        for init_id in INIT_IDS:
            pis = [row[init_id]["pi_ser"] for row in per_seed]
            valid = [p for p in pis if np.isfinite(p)]
            n_div = sum(1 for row in per_seed if row[init_id]["diverged"])
            n_col = sum(1 for p in valid if p > COLLAPSE_PI_SER)
            agg[init_id] = {
                "mean_pi_ser": float(np.mean(valid)) if valid else float("nan"),
                "median_pi_ser": float(np.median(valid)) if valid else float("nan"),
                "collapse_rate": float(n_col / len(SEEDS)),
                "collapse_count": n_col,
                "divergence_rate": float(n_div / len(SEEDS)),
                "divergence_count": n_div,
                "n_valid": len(valid),
                "per_seed_pi_ser": pis,
            }
        # Oracle-escape test: for seeds where center collapsed, did oracle escape?
        ct_collapsed_seeds = [
            row["seed"] for row in per_seed
            if np.isfinite(row["center_tap"]["pi_ser"]) and row["center_tap"]["pi_ser"] > COLLAPSE_PI_SER
        ]
        oracle_escape = {
            str(s): {
                "center_pi_ser": next(row["center_tap"]["pi_ser"] for row in per_seed if row["seed"] == s),
                "oracle_pi_ser": next(row["oracle_wiener"]["pi_ser"] for row in per_seed if row["seed"] == s),
                "oracle_escaped": next(row["oracle_wiener"]["pi_ser"] for row in per_seed if row["seed"] == s) <= ORACLE_ESCAPE_PI_SER,
            }
            for s in ct_collapsed_seeds
        }
        n_oracle_escaped = sum(1 for v in oracle_escape.values() if v["oracle_escaped"])
        cell_results.append({
            "cell_id": cell["id"],
            "axes": {"snr_db": cell["snr_db"], "f_g_hz": cell["f_g_hz"],
                     "sop_rate": cell["sop_rate"], "n_symbols": cell["n_symbols"]},
            "eval_window": {"eval_start": es, "calibration_end": ce, "eval_end": ee},
            "per_seed": per_seed,
            "aggregate": agg,
            "oracle_escape_test": {
                "center_collapsed_seeds": ct_collapsed_seeds,
                "oracle_escaped_seeds": [s for s, v in oracle_escape.items() if v["oracle_escaped"]],
                "n_center_collapsed": len(ct_collapsed_seeds),
                "n_oracle_escaped": n_oracle_escaped,
                "oracle_escape_rate_on_collapsed": (
                    float(n_oracle_escaped / len(ct_collapsed_seeds)) if ct_collapsed_seeds else None
                ),
                "per_seed": oracle_escape,
            },
        })
        dt = time.time() - t0
        if verbose:
            a = agg
            print(f"[{ci_idx+1:2d}/{len(CELLS)}] {cell['id']:28s} t={dt:5.1f}s "
                  f"ct={a['center_tap']['mean_pi_ser']:.3f}(col{a['center_tap']['collapse_count']}) "
                  f"wh={a['whitening']['mean_pi_ser']:.3f}(col{a['whitening']['collapse_count']}) "
                  f"ms={a['multistart']['mean_pi_ser']:.3f}(col{a['multistart']['collapse_count']}) "
                  f"ow={a['oracle_wiener']['mean_pi_ser']:.3f}(col{a['oracle_wiener']['collapse_count']}) "
                  f"ow_esc={n_oracle_escaped}/{len(ct_collapsed_seeds)}")
    total_dt = time.time() - t_start
    if verbose:
        print(f"\nTotal batch wall time: {total_dt:.1f}s ({total_dt/60:.2f} min)")
    return {"cell_results": cell_results, "wall_time_seconds": total_dt}


# ─── Paired bootstrap adjudication ────────────────────────────────────────────
def paired_bootstrap_delta(
    a_vals: list[float], b_vals: list[float], *, n_boot: int = 2000, rng=None,
) -> dict[str, float]:
    """Paired bootstrap on the difference (a - b). Returns mean, lo, hi (95%)."""
    if rng is None:
        rng = np.random.default_rng(0)
    a = np.asarray(a_vals, dtype=float)
    b = np.asarray(b_vals, dtype=float)
    mask = np.isfinite(a) & np.isfinite(b)
    a, b = a[mask], b[mask]
    n = len(a)
    if n == 0:
        return {"mean_delta": float("nan"), "ci_lo": float("nan"), "ci_hi": float("nan"), "n": 0}
    diffs = a - b
    boot_means = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, n, n)
        boot_means[i] = np.mean(diffs[idx])
    return {
        "mean_delta": float(np.mean(diffs)),
        "ci_lo": float(np.percentile(boot_means, 2.5)),
        "ci_hi": float(np.percentile(boot_means, 97.5)),
        "n": int(n),
    }


def adjudicate(batch: dict[str, Any]) -> dict[str, Any]:
    """Macro + per-cell collapse-rate and PI-SER deltas (candidate vs center)."""
    macro = {init_id: {"collapse_rate": 0.0, "mean_pi_ser": 0.0, "divergence_rate": 0.0}
             for init_id in INIT_IDS}
    per_cell = []
    n_cells = len(batch["cell_results"])
    oracle_collapsed_total = 0
    oracle_escaped_total = 0
    center_collapsed_total = 0
    for cr in batch["cell_results"]:
        agg = cr["aggregate"]
        row = {"cell_id": cr["cell_id"]}
        for init_id in INIT_IDS:
            macro[init_id]["collapse_rate"] += agg[init_id]["collapse_rate"]
            macro[init_id]["mean_pi_ser"] += agg[init_id]["mean_pi_ser"]
            macro[init_id]["divergence_rate"] += agg[init_id]["divergence_rate"]
        # paired bootstrap PI-SER delta (candidate - center)
        ct = agg["center_tap"]["per_seed_pi_ser"]
        for cand in ("whitening", "multistart", "oracle_wiener"):
            cv = agg[cand]["per_seed_pi_ser"]
            row[f"delta_pi_ser_{cand}_minus_center"] = paired_bootstrap_delta(cv, ct)
            # collapse indicator delta (1 if collapsed else 0)
            ct_col = [1.0 if (np.isfinite(p) and p > COLLAPSE_PI_SER) else 0.0 for p in ct]
            cv_col = [1.0 if (np.isfinite(p) and p > COLLAPSE_PI_SER) else 0.0 for p in cv]
            row[f"delta_collapse_{cand}_minus_center"] = paired_bootstrap_delta(cv_col, ct_col)
        per_cell.append(row)
        oe = cr["oracle_escape_test"]
        oracle_collapsed_total += sum(
            1 for v in oe["per_seed"].values() if v["oracle_pi_ser"] > COLLAPSE_PI_SER)
        oracle_escaped_total += oe["n_oracle_escaped"]
        center_collapsed_total += oe["n_center_collapsed"]
    for init_id in INIT_IDS:
        macro[init_id]["collapse_rate"] /= n_cells
        macro[init_id]["mean_pi_ser"] /= n_cells
        macro[init_id]["divergence_rate"] /= n_cells
    # macro deltas (candidate - center)
    macro_delta = {}
    for cand in ("whitening", "multistart", "oracle_wiener"):
        macro_delta[cand] = {
            "collapse_rate": macro[cand]["collapse_rate"] - macro["center_tap"]["collapse_rate"],
            "mean_pi_ser": macro[cand]["mean_pi_ser"] - macro["center_tap"]["mean_pi_ser"],
        }
    oracle_escape_macro = {
        "center_collapsed_seed_events": center_collapsed_total,
        "oracle_also_collapsed_seed_events": oracle_collapsed_total,
        "oracle_escaped_seed_events": oracle_escaped_total,
        "oracle_escape_rate_on_collapsed": (
            float(oracle_escaped_total / center_collapsed_total) if center_collapsed_total else None
        ),
        "verdict": (
            "INIT_DEPENDENT" if oracle_escaped_total > center_collapsed_total / 2
            else "COST_FUNDAMENTAL"
        ),
    }
    return {
        "macro": macro,
        "macro_delta_candidate_minus_center": macro_delta,
        "per_cell": per_cell,
        "oracle_escape": oracle_escape_macro,
    }


# ─── identity test runner ─────────────────────────────────────────────────────
def run_identity_tests() -> dict[str, Any]:
    """Run src/test_init_identity.py and parse the summary line."""
    try:
        proc = subprocess.run(
            [sys.executable, str(HERE / "test_init_identity.py")],
            capture_output=True, text=True, timeout=120,
        )
        out = proc.stdout + proc.stderr
        last = [ln for ln in out.strip().splitlines() if ln.strip()][-1] if out.strip() else ""
        ok = proc.returncode == 0
        return {"pass": ok, "summary": last, "stdout_tail": out[-1500:]}
    except Exception as exc:  # noqa: BLE001
        return {"pass": False, "summary": f"exception: {exc}", "stdout_tail": str(exc)}


# ─── main ─────────────────────────────────────────────────────────────────────
def main():
    print("=" * 72)
    print("C14 init-strategy Scout — STEP 1: identity tests (REQUIRED PASS)")
    print("=" * 72)
    identity = run_identity_tests()
    print(f"identity tests: {'PASS' if identity['pass'] else 'FAIL'}  ({identity['summary']})")
    if not identity["pass"]:
        print(identity["stdout_tail"])
        print("\nABORT: identity gate failed — custom-init runner is confounded.")
        sys.exit(1)

    print("\n" + "=" * 72)
    print("STEP 2: semantic smoke (3 frozen checks)")
    print("=" * 72)
    smoke = run_semantic_smoke()
    for k, v in smoke["checks"].items():
        print(f"  {k}: {'PASS' if v['pass'] else 'FAIL'}")
    if not smoke["all_pass"]:
        print("\nDIAGNOSTIC: semantic smoke FAILED. Reporting and stopping.")
        result = {
            "schema_version": "direction-lab.cb1.c14-init-strategy-scout.v1",
            "campaign_id": "science-scout-2026-07-20.dual-pol-osl",
            "identity": identity,
            "smoke": smoke,
            "status": "DIAGNOSTIC_SMOKE_FAILED",
        }
        (ARTIFACTS / "result.v1.json").write_text(
            json.dumps(_jsonable(result), indent=2), encoding="utf-8")
        print(f"Wrote {ARTIFACTS / 'result.v1.json'}")
        return

    print("\n" + "=" * 72)
    print("STEP 3: full batch (11 cells x 10 seeds x 4 inits)")
    print("=" * 72)
    batch = run_batch(verbose=True)

    print("\n" + "=" * 72)
    print("STEP 4: adjudication (paired bootstrap, oracle-escape test)")
    print("=" * 72)
    adjud = adjudicate(batch)
    print("\nMacro collapse_rate per init:")
    for init_id in INIT_IDS:
        print(f"  {init_id:16s} collapse_rate={adjud['macro'][init_id]['collapse_rate']:.3f} "
              f"mean_pi_ser={adjud['macro'][init_id]['mean_pi_ser']:.4f} "
              f"div_rate={adjud['macro'][init_id]['divergence_rate']:.3f}")
    print("\nMacro delta (candidate - center):")
    for cand in ("whitening", "multistart", "oracle_wiener"):
        d = adjud["macro_delta_candidate_minus_center"][cand]
        print(f"  {cand:16s} dCollapse={d['collapse_rate']:+.3f} dPI-SER={d['mean_pi_ser']:+.4f}")
    oe = adjud["oracle_escape"]
    print("\nORACLE-ESCAPE TEST (the key result):")
    print(f"  center-tap collapsed seed-events: {oe['center_collapsed_seed_events']}")
    print(f"  oracle init escaped (PI-SER<={ORACLE_ESCAPE_PI_SER}): {oe['oracle_escaped_seed_events']}")
    print(f"  oracle also collapsed: {oe['oracle_also_collapsed_seed_events']}")
    print(f"  oracle_escape_rate_on_collapsed = {oe['oracle_escape_rate_on_collapsed']}")
    print(f"  >>> VERDICT: {oe['verdict']}")

    result = {
        "schema_version": "direction-lab.cb1.c14-init-strategy-scout.v1",
        "campaign_id": "science-scout-2026-07-20.dual-pol-osl",
        "candidate_id": "C14",
        "contract_frozen_axes": FROZEN_AXES,
        "collapse_pi_ser_threshold": COLLAPSE_PI_SER,
        "oracle_escape_pi_ser_threshold": ORACLE_ESCAPE_PI_SER,
        "seeds": SEEDS,
        "multistart_K": MULTISTART_K,
        "multistart_warmup_blocks": MULTISTART_WARMUP,
        "init_ids": INIT_IDS,
        "identity": identity,
        "smoke": smoke,
        "batch": batch,
        "adjudication": adjud,
        "status": "COMPLETE",
    }
    out_json = ARTIFACTS / "result.v1.json"
    out_json.write_text(json.dumps(_jsonable(result), indent=2), encoding="utf-8")
    print(f"\nWrote {out_json}")


if __name__ == "__main__":
    main()
