"""G1_SAFE_GATED_NORMALIZATION — formal Step 4a confirm runner (Groundwork B).

Frozen-contract MVE. Implements B2 (run + receipts) and B4 (preregistered gate).
Read-only reuse of T020 generator/evaluator/CMA + T020 M4 (imported, NOT
modified). Adds the correct-normalization comparators + faithful D4 from
methods.py.

Pipeline:
  Phase A — 9 semantic smoke gates (must all PASS before compare)  [tests/]
  Phase B — run all 8 methods on 7 cells x 20 fresh seeds (261-280) = 1120 rows
  Phase C — seed-cluster aggregation + 7 preregistered B4 gates + dual report

Frozen BEFORE any seed (see contract.yaml + artifacts/seed-freeze-receipt.md):
cells, FRESH_SEEDS=261..280, M4/G1 gate params (collapse=0.6, spread=0.1),
MDE=0.005, 10k bootstrap CI, stat_unit=seed_cluster. No post-hoc rescue.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve()
SRC = HERE.parent
G1_ROOT = SRC.parent                            # g1-safe-gated-normalization-confirm/
SCOUT = G1_ROOT.parent                          # scout/
CB1_ROOT = SCOUT / "cb1-modulation-generic-closure"
BASELINE_ATLAS = CB1_ROOT / "baseline-atlas"
T020_ROOT = SCOUT / "preformal-method-factory-sprint-002"
T020_SRC = T020_ROOT / "src"
C11_LEGALITY = CB1_ROOT / "c11-legality-batch-v1"
REPO_ROOT = HERE.parents[6]
SIM_DIR = REPO_ROOT / "projects" / "simulation"

for p in (str(SIM_DIR), str(BASELINE_ATLAS), str(C11_LEGALITY)):
    if p not in sys.path:
        sys.path.insert(0, p)

from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402
import cb1_evaluator as evaluator  # noqa: E402
import cb1_cell_runner as runner  # noqa: E402
# Both this dir and T020 have a methods.py -> load each explicitly by path to
# avoid sys.path name clash (whichever is imported first wins for `import methods`).
import importlib.util  # noqa: E402
_spec_g1 = importlib.util.spec_from_file_location("g1_methods", str(SRC / "methods.py"))
G1M = importlib.util.module_from_spec(_spec_g1)
_spec_g1.loader.exec_module(G1M)
_spec_t020 = importlib.util.spec_from_file_location("t020_methods", str(T020_SRC / "methods.py"))
T020M = importlib.util.module_from_spec(_spec_t020)
_spec_t020.loader.exec_module(T020M)

# ─── Frozen axes (identical to T020/T023 contract; NOT modified) ─────────────
FROZEN_AXES = {
    "alpha": 4.2, "beta": 1.4, "block": 100, "t_s": 4.0e-10, "method": "gar",
    "cma_mu_current": 3.0e-2, "cma_mu_stale": 1.0e-3,
    "cma_taps": 11, "r2_qam16": 1.32, "cma_block_size": 64,
    "affine_ridge": 1.0e-6, "constellation_amplitude_per_axis": 0.7071067811865475,
}
R2_16QAM = 1.32
MU_CURRENT = 3.0e-2
TAPS = 11
BS = 64
RIDGE = 1.0e-6

# 7 T020 cells UNCHANGED (copied from run_adjudication.py)
CELLS = [
    {"id": "16qam-snr05-nominal-short", "modulation": "qam16", "snr_db": 5.0,  "f_g_hz": 30.0,   "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr10-nominal-short", "modulation": "qam16", "snr_db": 10.0, "f_g_hz": 30.0,   "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr15-nominal-short", "modulation": "qam16", "snr_db": 15.0, "f_g_hz": 30.0,   "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr25-nominal-short", "modulation": "qam16", "snr_db": 25.0, "f_g_hz": 30.0,   "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr20-fg100-short",   "modulation": "qam16", "snr_db": 20.0, "f_g_hz": 100.0,  "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr10-fg100-long",    "modulation": "qam16", "snr_db": 10.0, "f_g_hz": 100.0,  "sop_rate": 4.0e-6, "n_symbols": 8192},
    {"id": "16qam-snr15-fg1000-long",   "modulation": "qam16", "snr_db": 15.0, "f_g_hz": 1000.0, "sop_rate": 4.0e-6, "n_symbols": 8192},
]

# Frozen seeds (B2) — token-clean vs T019-T023 (seed-freeze-receipt.md)
FRESH_SEEDS = list(range(261, 281))   # 261..280
OLD_201_220 = list(range(201, 221))   # T020/T023 old
FRESH_241_260 = list(range(241, 261)) # T023 fresh
DEV_181_190 = list(range(181, 191))   # T020 dev
# asserts (frozen in seed-freeze-receipt.md)
assert FRESH_SEEDS == list(range(261, 281))
assert set(FRESH_SEEDS).isdisjoint(set(OLD_201_220))
assert set(FRESH_SEEDS).isdisjoint(set(FRESH_241_260))
assert set(FRESH_SEEDS).isdisjoint(set(DEV_181_190))

# T020 dev-frozen gate params (NOT re-tuned on fresh)
G1_COLLAPSE = 0.6
G1_SPREAD = 0.1
M4_COLLAPSE = 0.6      # M4 lineage ablation uses the SAME frozen gate
M4_SPREAD = 0.1
M1_TRIM = 0.2

CALIB_PREFIX = 128     # contract information_boundary

# 8 methods on the same footing
METHOD_ORDER = [
    "baseline_cma_mu0p03",          # 1. the M (tuned fixed-mu CMA identity)
    "correct_pooled_sqrt_rms",      # 2. always-on pooled sqrt
    "correct_per_pol_sqrt_rms",     # 3. always-on per-pol sqrt
    "robust_scalar",                # 4. always-on median sqrt [primary always-on]
    "gated_scalar",                 # 5. G1 = gate + per-pol correct sqrt (CANDIDATE)
    "M4_gated_policy",              # 6. Q15 nonlinear map (lineage ablation ONLY)
    "D4_likelihood_gated_rde",      # 7. Di Rosa JLT 2021 likelihood RDE
    "oracle_affine_bound",          # 8. KILL-ONLY (label only)
]
COMPARATORS = ["baseline_cma_mu0p03", "correct_pooled_sqrt_rms",
               "correct_per_pol_sqrt_rms", "robust_scalar",
               "M4_gated_policy", "D4_likelihood_gated_rde"]
CANDIDATE = "gated_scalar"          # G1
PRIMARY_ALWAYS_ON = "robust_scalar"
MDE = 0.005
N_BOOT = 10000


def _realization(cell, seed):
    gamma_bar = float(10.0 ** (float(cell["snr_db"]) / 10.0))
    return generate_shared_realization_dp(
        int(cell["n_symbols"]), float(FROZEN_AXES["alpha"]), float(FROZEN_AXES["beta"]),
        float(cell["f_g_hz"]), sop_rate=float(cell["sop_rate"]), seed=int(seed),
        gamma_bar=gamma_bar, block=int(FROZEN_AXES["block"]),
        t_s=float(FROZEN_AXES["t_s"]), method=str(FROZEN_AXES["method"]),
        modulation=str(cell["modulation"]))


def _eval_window(n_symbols):
    es, cal, ee, _ = runner.eval_window_for(n_symbols, TAPS, window_symbols=256, block_size=BS)
    return es, cal, ee


def _eval_pred(px, py, tx, ty, bx, by):
    m = evaluator.evaluate_dual_16qam(px, py, tx, ty, bx, by)
    return {"pi_ser": float(m["pi_ser"]), "fixed_label_ser": float(m["fixed_label_ser"]),
            "pi_ber": float(m["pi_ber"])}


def _nan_metrics(diverged=True):
    return {"pi_ser": float("nan"), "fixed_label_ser": float("nan"),
            "pi_ber": float("nan"), "diverged": bool(diverged)}


def run_all_on_realization(cell, seed):
    """Run all 8 methods on ONE shared (cell,seed) realization.

    Returns out dict with per-method metrics + the prefix receipt (G1 freeze)
    + offline label inputs. Non-finite metrics are encoded with explicit flags
    (no silent row drop)."""
    n = int(cell["n_symbols"])
    es, cal, ee = _eval_window(n)
    rl = _realization(cell, seed)
    bits_per = 4
    tx, ty = rl["sX"][cal:ee], rl["sY"][cal:ee]
    bx = rl["bitsX"][cal * bits_per:ee * bits_per]
    by = rl["bitsY"][cal * bits_per:ee * bits_per]
    out = {"cell_id": cell["id"], "seed": int(seed), "n_symbols": n,
           "eval_window": {"eval_start": es, "calibration_end": cal, "eval_end": ee},
           "calib_prefix_symbols": int(cal - es),
           "methods": {}}

    # The tuned-CMA whose output z is scored (the caller for all methods)
    base = runner.standard_cma_godard_with_z(
        rl["rX"], rl["rY"], n_tap=TAPS, mu=MU_CURRENT, R2=R2_16QAM, block_size=BS)
    div = bool(base["diverged"])
    zpx, zpy = base["zX"][es:cal], base["zY"][es:cal]   # calibration prefix (128)
    zsx, zsy = base["zX"][cal:ee], base["zY"][cal:ee]   # scored suffix (128)
    truth_calib_x, truth_calib_y = rl["sX"][es:cal], rl["sY"][es:cal]

    def _record(name, m, **extra):
        m = dict(m)
        m.update(extra)
        out["methods"][name] = m

    # 1. baseline (identity over the converged CMA z)
    if not div:
        m = _eval_pred(evaluator.hard_16qam(zsx), evaluator.hard_16qam(zsy), tx, ty, bx, by)
    else:
        m = _nan_metrics()
    _record("baseline_cma_mu0p03", m, diverged=div)

    # 8. oracle (Kill-only) — needed for the offline label; compute first
    if not div:
        oxp, oyp = G1M.oracle_affine_bound_apply(
            zpx, zpy, zsx, zsy, truth_calib_x, truth_calib_y, ridge=RIDGE, evaluator_mod=evaluator)
        m = _eval_pred(oxp, oyp, tx, ty, bx, by)
    else:
        m = _nan_metrics()
    _record("oracle_affine_bound", m, diverged=div, kill_only=True)

    # offline 4-category label + receipt inputs (recomputed here = row-recomputable)
    b_ser = out["methods"]["baseline_cma_mu0p03"].get("pi_ser")
    o_ser = out["methods"]["oracle_affine_bound"].get("pi_ser")
    b_finite = (b_ser is not None and np.isfinite(b_ser))
    o_finite = (o_ser is not None and np.isfinite(o_ser))
    label, label_bin = _offline_label_pair(b_ser, o_ser, div, b_finite, o_finite)
    out["offline_4category"] = label
    out["offline_binary_label"] = label_bin
    out["baseline_pi_ser"] = (float(b_ser) if b_finite else None)
    out["oracle_pi_ser"] = (float(o_ser) if o_finite else None)
    out["oracle_gap"] = (float(b_ser - o_ser) if (b_finite and o_finite) else None)
    out["baseline_diverged"] = bool(div)
    out["baseline_metric_finite"] = bool(b_finite)
    out["oracle_metric_finite"] = bool(o_finite)

    # G1 prefix receipt (freeze once; row-recomputable from the call chain)
    g1_fr = G1M.gated_scalar_freeze(zpx, zpy, collapse_threshold=G1_COLLAPSE, spread_threshold=G1_SPREAD)
    out["g1_receipt"] = {
        "gate_policy": str(g1_fr["policy"]), "gate_active": bool(g1_fr["gate_active"]),
        "mean_abs2": float(g1_fr["mean_abs2"]), "spread": float(g1_fr["spread"]),
        "a_x": float(g1_fr["a_x"]), "a_y": float(g1_fr["a_y"]),
        "collapse_threshold": float(G1_COLLAPSE), "spread_threshold": float(G1_SPREAD),
        "offline_4category": label, "offline_binary_label": label_bin,
        "baseline_pi_ser": out["baseline_pi_ser"], "oracle_pi_ser": out["oracle_pi_ser"],
        "oracle_gap": out["oracle_gap"], "baseline_diverged": out["baseline_diverged"],
        "baseline_metric_finite": out["baseline_metric_finite"],
        "oracle_metric_finite": out["oracle_metric_finite"],
        "label_caller": "run_g1_confirm._offline_label_pair (== run_factory._offline_label:558)",
        "label_window": f"z[{es}:{cal}] prefix / z[{cal}:{ee}] suffix",
    }

    if div:
        # all non-baseline/non-oracle methods inherit the divergence flag
        for nm in ("correct_pooled_sqrt_rms", "correct_per_pol_sqrt_rms", "robust_scalar",
                   "gated_scalar", "M4_gated_policy", "D4_likelihood_gated_rde"):
            _record(nm, _nan_metrics(), diverged=True)
        out["base_diverged"] = True
        return out

    # 2. correct pooled sqrt-RMS
    fp = G1M.correct_pooled_sqrt_rms_freeze(zpx, zpy)
    ppx, ppy = G1M.correct_pooled_sqrt_rms_apply_continuous(fp, zsx, zsy)
    _record("correct_pooled_sqrt_rms", _eval_pred(ppx, ppy, tx, ty, bx, by),
            scale_a_x=float(fp["a"]), scale_a_y=float(fp["a"]))

    # 3. correct per-pol sqrt-RMS
    fpp = G1M.correct_per_pol_sqrt_rms_freeze(zpx, zpy)
    ppx, ppy = G1M.correct_per_pol_sqrt_rms_apply_continuous(fpp, zsx, zsy)
    _record("correct_per_pol_sqrt_rms", _eval_pred(ppx, ppy, tx, ty, bx, by),
            scale_a_x=float(fpp["a_x"]), scale_a_y=float(fpp["a_y"]))

    # 4. robust scalar (median) — primary always-on comparator
    frs = G1M.robust_scalar_freeze(zpx, zpy)
    rsx, rsy = G1M.robust_scalar_apply_continuous(frs, zsx, zsy)
    _record("robust_scalar", _eval_pred(rsx, rsy, tx, ty, bx, by),
            scale_a_x=float(frs["a_x"]), scale_a_y=float(frs["a_y"]))

    # 5. G1 = gated_scalar (candidate)
    gsx, gsy = G1M.gated_scalar_apply_continuous(g1_fr, zsx, zsy)
    _record("gated_scalar", _eval_pred(gsx, gsy, tx, ty, bx, by),
            gate_policy=str(g1_fr["policy"]), gate_active=bool(g1_fr["gate_active"]),
            scale_a_x=float(g1_fr["a_x"]), scale_a_y=float(g1_fr["a_y"]))

    # 6. M4 gated policy (Q15 nonlinear map; lineage ablation ONLY)
    f2 = T020M.m2_quantile_transport_freeze(np.concatenate([zpx, zpy]))
    f3 = T020M.m3_three_shell_mixture_freeze(np.concatenate([zpx, zpy]))
    f4 = G1M.m4_gated_policy_freeze(zpx, zpy, collapse_threshold=M4_COLLAPSE,
                                    spread_threshold=M4_SPREAD, t020m=T020M)
    m4x, m4y = G1M.m4_gated_policy_apply_continuous(f4, zsx, zsy,
                                                    m2_frozen=f2, m3_frozen=f3, t020m=T020M)
    _record("M4_gated_policy", _eval_pred(m4x, m4y, tx, ty, bx, by),
            gate_policy=str(f4["policy"]), gate_active=(str(f4["policy"]) != "identity"))

    # 7. D4 likelihood-gated RDE (faithful; output = converged-CMA z)
    fd4 = G1M.d4_likelihood_gated_rde_freeze(zpx, zpy)
    d4x, d4y = G1M.d4_likelihood_gated_rde_apply(fd4, zsx, zsy)
    _record("D4_likelihood_gated_rde", _eval_pred(d4x, d4y, tx, ty, bx, by),
            alpha_th=float(fd4["alpha_th"]), sigma2_hat=float(fd4["sigma2_hat"]),
            alpha_prefix_mean=float(fd4.get("alpha_prefix_mean", float("nan"))))

    out["base_diverged"] = False
    return out


def _offline_label_pair(b, o, base_diverged, b_finite, o_finite):
    """EXACTLY _offline_label from run_factory.py:558 (task-native).
    Returns (category, binary_label). binary_label = 1 if recoverable_failure
    else 0 if healthy else None (awgn_dominated/ambiguous excluded from the
    binary classification denominators)."""
    if b is None or o is None or not b_finite or not o_finite:
        return "ambiguous", None
    if base_diverged:
        return "ambiguous", None
    if b < 0.1:
        return "healthy", 0
    if (b - o) < 0.005:
        return "awgn_dominated_error", None
    if o < 0.1:
        return "inner_ring_recoverable_collapse", 1   # recoverable_failure
    return "ambiguous", None


# ─── Phase B: run compare + emit receipts ────────────────────────────────────

RAW_FIELDS = ["cell", "seed", "method", "pi_ser", "fixed_label_ser", "pi_ber",
              "gate_policy", "scale_a_x", "scale_a_y",
              "offline_4category", "offline_binary_label",
              "baseline_pi_ser", "oracle_pi_ser", "oracle_gap",
              "baseline_diverged", "baseline_metric_finite", "oracle_metric_finite"]

PREFIX_FIELDS = ["cell", "seed", "gate_policy", "gate_active", "mean_abs2", "spread",
                 "a_x", "a_y", "offline_4category", "offline_binary_label",
                 "baseline_pi_ser", "oracle_pi_ser", "oracle_gap",
                 "baseline_diverged", "baseline_metric_finite", "oracle_metric_finite",
                 "label_caller", "label_window"]


def _fnum(v):
    if v is None:
        return ""
    try:
        if not np.isfinite(v):
            return ""
    except (TypeError, ValueError):
        return ""
    return float(v)


def phase_compare():
    raw_rows = []
    prefix_rows = []
    per_pair_label = {}
    t0 = time.time()
    for ci, cell in enumerate(CELLS):
        for seed in FRESH_SEEDS:
            out = run_all_on_realization(cell, seed)
            bpi = out["baseline_pi_ser"]
            opi = out["oracle_pi_ser"]
            for mname in METHOD_ORDER:
                mres = out["methods"].get(mname, {})
                pis = mres.get("pi_ser")
                raw_rows.append({
                    "cell": out["cell_id"], "seed": out["seed"], "method": mname,
                    "pi_ser": (_fnum(pis) if pis is not None else ""),
                    "fixed_label_ser": (_fnum(mres.get("fixed_label_ser")) if mres.get("fixed_label_ser") is not None else ""),
                    "pi_ber": (_fnum(mres.get("pi_ber")) if mres.get("pi_ber") is not None else ""),
                    "gate_policy": str(mres.get("gate_policy", "")),
                    "scale_a_x": (_fnum(mres.get("scale_a_x")) if mres.get("scale_a_x") is not None else ""),
                    "scale_a_y": (_fnum(mres.get("scale_a_y")) if mres.get("scale_a_y") is not None else ""),
                    "offline_4category": out["offline_4category"],
                    "offline_binary_label": ("" if out["offline_binary_label"] is None else int(out["offline_binary_label"])),
                    "baseline_pi_ser": ("" if bpi is None else _fnum(bpi)),
                    "oracle_pi_ser": ("" if opi is None else _fnum(opi)),
                    "oracle_gap": ("" if out["oracle_gap"] is None else _fnum(out["oracle_gap"])),
                    "baseline_diverged": bool(out["baseline_diverged"]),
                    "baseline_metric_finite": bool(out["baseline_metric_finite"]),
                    "oracle_metric_finite": bool(out["oracle_metric_finite"]),
                })
            gr = out["g1_receipt"]
            prefix_rows.append({
                "cell": out["cell_id"], "seed": out["seed"],
                "gate_policy": gr["gate_policy"], "gate_active": gr["gate_active"],
                "mean_abs2": _fnum(gr["mean_abs2"]), "spread": _fnum(gr["spread"]),
                "a_x": _fnum(gr["a_x"]), "a_y": _fnum(gr["a_y"]),
                "offline_4category": gr["offline_4category"],
                "offline_binary_label": ("" if gr["offline_binary_label"] is None else int(gr["offline_binary_label"])),
                "baseline_pi_ser": ("" if bpi is None else _fnum(bpi)),
                "oracle_pi_ser": ("" if opi is None else _fnum(opi)),
                "oracle_gap": ("" if out["oracle_gap"] is None else _fnum(out["oracle_gap"])),
                "baseline_diverged": bool(out["baseline_diverged"]),
                "baseline_metric_finite": bool(out["baseline_metric_finite"]),
                "oracle_metric_finite": bool(out["oracle_metric_finite"]),
                "label_caller": gr["label_caller"], "label_window": gr["label_window"],
            })
            per_pair_label[(cell["id"], seed)] = out["offline_4category"]
        print(f"  [{ci+1}/{len(CELLS)}] {cell['id']:28s} done ({time.time()-t0:.1f}s)")
    return {"raw_rows": raw_rows, "prefix_rows": prefix_rows,
            "per_pair_label": per_pair_label, "wall_seconds": time.time() - t0}


def _write_csv(path, rows, fields):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


# ─── Phase C: seed-cluster aggregation + 7 preregistered B4 gates ────────────

def _boot_ci(deltas, n_boot=N_BOOT, seed=42):
    if len(deltas) < 2:
        return [float("nan"), float("nan")]
    rng = np.random.default_rng(seed)
    arr = np.asarray(deltas, dtype=float)
    boots = np.mean(rng.choice(arr, size=(n_boot, len(arr)), replace=True), axis=1)
    return [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]


def _balanced_accuracy_bootstrap(y_true, y_pred, mask, n_boot=N_BOOT, seed=123):
    """Cluster bootstrap over the (cell,seed) pairs in `mask`. y_true/y_pred are
    binary (0/1). Returns (point_bacc, ci_lo, ci_hi, n_pos, n_neg, tp, fp, fn, tn)."""
    idx = np.where(mask)[0]
    yt = np.asarray(y_true)[idx]
    yp = np.asarray(y_pred)[idx]
    n_pos = int(np.sum(yt == 1))
    n_neg = int(np.sum(yt == 0))
    tp = int(np.sum((yt == 1) & (yp == 1)))
    fp = int(np.sum((yt == 0) & (yp == 1)))
    fn = int(np.sum((yt == 1) & (yp == 0)))
    tn = int(np.sum((yt == 0) & (yp == 0)))

    def _bacc(yt, yp):
        tpr = float(np.mean(yp[yt == 1] == 1)) if np.any(yt == 1) else 0.0
        tnr = float(np.mean(yp[yt == 0] == 0)) if np.any(yt == 0) else 0.0
        return 0.5 * (tpr + tnr)
    point = _bacc(yt, yp)
    if len(idx) < 2 or n_pos == 0 or n_neg == 0:
        return point, float("nan"), float("nan"), n_pos, n_neg, tp, fp, fn, tn
    rng = np.random.default_rng(seed)
    n = len(idx)
    boots = []
    for _ in range(n_boot):
        s = rng.integers(0, n, size=n)          # positional resample over yt/yp
        boots.append(_bacc(yt[s], yp[s]))
    return point, float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5)), n_pos, n_neg, tp, fp, fn, tn


def aggregate(raw_rows, prefix_rows):
    """Seed-cluster aggregation. Statistics unit = seed-cluster: within each
    seed, average the paired delta over the cells where that stratum appears
    (equal weight); one seed = one cluster value. Strata: overall / healthy /
    collapse(recoverable_failure)."""
    cells = sorted({r["cell"] for r in raw_rows})
    seeds = sorted({r["seed"] for r in raw_rows})

    # per (cell,seed) lookup
    pis = {}
    for r in raw_rows:
        v = r["pi_ser"]
        pis[(r["cell"], r["seed"], r["method"])] = (float(v) if v != "" else None)

    # per (cell,seed) label
    lbl = {}
    for r in prefix_rows:
        lbl[(r["cell"], r["seed"])] = r["offline_4category"]

    def _seed_deltas(method, ref, stratum):
        """Return list of per-seed mean-delta values (one per seed that has the
        stratum in >=1 cell). Within a seed: average (method-ref) over the
        cells where `stratum` matches; equal weight per cell."""
        deltas = []
        per_pair = []      # per-pair deltas for healthy-worst / safety
        for s in seeds:
            ds = []
            for c in cells:
                if stratum == "overall" or lbl.get((c, s)) == stratum:
                    b = pis.get((c, s, ref))
                    mv = pis.get((c, s, method))
                    if b is not None and mv is not None:
                        ds.append(float(mv - b))
                        if stratum == "healthy":
                            per_pair.append((c, s, float(mv - b)))
            if ds:
                deltas.append(float(np.mean(ds)))
        return deltas, per_pair

    def _cluster_stats(method, stratum):
        deltas, per_pair = _seed_deltas(method, "baseline_cma_mu0p03", stratum)
        if not deltas:
            return {"n_seeds": 0, "mean_delta": float("nan"),
                    "ci_95": [float("nan"), float("nan")],
                    "help": 0, "hurt": 0, "tie": 0, "healthy_worst": float("nan"),
                    "seed_mean_method": float("nan")}
        help_n = int(sum(1 for d in deltas if d < -1e-9))
        hurt_n = int(sum(1 for d in deltas if d > 1e-9))
        tie_n = int(sum(1 for d in deltas if abs(d) <= 1e-9))
        ci = _boot_ci(deltas)
        # seed-mean of the method's PI-SER over stratum cells
        method_seeds = []
        for s in seeds:
            ms = []
            for c in cells:
                if stratum == "overall" or lbl.get((c, s)) == stratum:
                    mv = pis.get((c, s, method))
                    if mv is not None:
                        ms.append(mv)
            if ms:
                method_seeds.append(float(np.mean(ms)))
        hworst = float("nan")
        if stratum == "healthy" and per_pair:
            hworst = float(max(d for _, _, d in per_pair))
        return {"n_seeds": len(deltas), "mean_delta": float(np.mean(deltas)),
                "ci_95": ci, "help": help_n, "hurt": hurt_n, "tie": tie_n,
                "healthy_worst": hworst,
                "seed_mean_method": (float(np.mean(method_seeds)) if method_seeds else float("nan"))}

    # also compute the per-pair healthy degradation distribution for G1 + every competitor
    def _healthy_pair_deltas(method):
        out = []
        for s in seeds:
            for c in cells:
                if lbl.get((c, s)) == "healthy":
                    b = pis.get((c, s, "baseline_cma_mu0p03"))
                    mv = pis.get((c, s, method))
                    if b is not None and mv is not None:
                        out.append({"cell": c, "seed": int(s), "delta": float(mv - b)})
        return out

    stats = {}
    for stratum in ("overall", "healthy", "collapse"):
        stats[stratum] = {m: _cluster_stats(m, "overall" if stratum == "overall"
                                            else ("healthy" if stratum == "healthy" else "inner_ring_recoverable_collapse"))
                          for m in METHOD_ORDER}

    # G1 vs M4 collapse ablation (delta of deltas)
    g1_c = _seed_deltas("gated_scalar", "baseline_cma_mu0p03", "inner_ring_recoverable_collapse")[0]
    m4_c = _seed_deltas("M4_gated_policy", "baseline_cma_mu0p03", "inner_ring_recoverable_collapse")[0]
    # align by seed index (both built over the same seed iteration order)
    g1_vm4 = [g - m for g, m in zip(g1_c, m4_c) if np.isfinite(g) and np.isfinite(m)]

    # per-seed collapse deltas (method - baseline) for every comparator, aligned
    # by the SAME seed iteration order, so apply_b4_gates can compute paired
    # (competitor - G1) without rebuilding the index.
    collapse_seed_deltas = {}
    for m in METHOD_ORDER:
        collapse_seed_deltas[m] = _seed_deltas(m, "baseline_cma_mu0p03",
                                               "inner_ring_recoverable_collapse")[0]

    # activation classification: predict recoverable_failure from gate_active
    # binary classification: positive=recoverable_failure(1), negative=healthy(0);
    # awgn_dominated/ambiguous excluded from precision/recall denominators but kept in counts.
    y_true, y_pred, mask = [], [], []
    false_activation_healthy = 0
    n_healthy_pairs = 0
    for r in prefix_rows:
        lt = r["offline_4category"]
        ga = bool(r["gate_active"])
        bin_true = r["offline_binary_label"]
        if lt == "healthy":
            n_healthy_pairs += 1
            if ga:
                false_activation_healthy += 1
        # only healthy(0) and recoverable(1) enter the precision/recall denominators
        include = (bin_true == 0 or bin_true == 1)
        y_true.append(int(bin_true) if bin_true != "" else -1)
        y_pred.append(int(ga))
        mask.append(include)

    bacc_point, bacc_lo, bacc_hi, n_pos, n_neg, tp, fp, fn, tn = _balanced_accuracy_bootstrap(
        y_true, y_pred, np.array(mask))
    precision = float(tp / (tp + fp)) if (tp + fp) > 0 else float("nan")
    recall = float(tp / (tp + fn)) if (tp + fn) > 0 else float("nan")
    # collapse activation: gate must hit >=1 offline collapse pair
    collapse_hits = int(sum(1 for r in prefix_rows
                            if r["offline_4category"] == "inner_ring_recoverable_collapse"
                            and bool(r["gate_active"])))

    # healthy degradation distribution for every comparator
    healthy_dist = {m: _healthy_pair_deltas(m) for m in METHOD_ORDER}

    return {
        "cluster_stats": stats,
        "collapse_seed_deltas": collapse_seed_deltas,
        "g1_vs_m4_collapse": {"n": len(g1_vm4), "mean_delta_G1_minus_M4": (float(np.mean(g1_vm4)) if g1_vm4 else float("nan")),
                              "ci_95": (_boot_ci(g1_vm4) if g1_vm4 else [float("nan"), float("nan")])},
        "activation": {
            "bacc_point": bacc_point, "bacc_ci_95": [bacc_lo, bacc_hi],
            "n_pos_recoverable": n_pos, "n_neg_healthy": n_neg,
            "tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "precision": precision, "recall": recall,
            "collapse_pairs_hit_by_gate": collapse_hits,
            "false_activation_healthy": false_activation_healthy,
            "n_healthy_pairs": n_healthy_pairs,
        },
        "healthy_degradation_distribution": healthy_dist,
        "label_counts": {lbl_v: int(sum(1 for r in prefix_rows if r["offline_4category"] == lbl_v))
                         for lbl_v in ("healthy", "awgn_dominated_error",
                                       "inner_ring_recoverable_collapse", "ambiguous")},
        "n_seeds": len(seeds), "n_cells": len(cells),
        "n_pairs": len(prefix_rows),
    }


def apply_b4_gates(agg):
    """Apply the 7 preregistered B4 gates. Returns (verdict, gate_details)."""
    cs = agg["cluster_stats"]
    coll = cs["collapse"]
    heal = cs["healthy"]
    act = agg["activation"]
    g1_coll = coll["gated_scalar"]
    g1_heal = heal["gated_scalar"]
    m4_coll = coll["M4_gated_policy"]
    g1_vm4 = agg["g1_vs_m4_collapse"]
    details = {}
    verdicts = {}

    # Gate 1: class support
    # >=5 seed-clusters with a healthy pair AND >=5 with a recoverable_failure pair
    n_healthy_seeds = heal["gated_scalar"]["n_seeds"]   # seeds that have >=1 healthy cell
    n_coll_seeds = coll["gated_scalar"]["n_seeds"]
    g1_pass = (n_healthy_seeds >= 5 and n_coll_seeds >= 5)
    verdicts["gate1_class_support"] = {
        "pass": g1_pass, "n_healthy_seeds": n_healthy_seeds, "n_collapse_seeds": n_coll_seeds,
        "rule": ">=5 healthy AND >=5 recoverable_failure seed-clusters"}
    if not g1_pass:
        return "G1_BLOCKED_CLASS_SUPPORT_NO_GO", verdicts, details

    # Gate 2: G1 vs tuned CMA on collapse stratum
    g2_mean = g1_coll["mean_delta"]
    g2_cihi = g1_coll["ci_95"][1]
    g2_pass = (np.isfinite(g2_mean) and g2_mean <= -MDE and g2_cihi < 0
               and g1_coll["help"] > g1_coll["hurt"])
    verdicts["gate2_g1_vs_cma_collapse"] = {
        "pass": bool(g2_pass), "mean_delta": g2_mean, "ci_95": g1_coll["ci_95"],
        "help": g1_coll["help"], "hurt": g1_coll["hurt"],
        "rule": "mean<=-0.005 AND CI_hi<0 AND help>hurt"}

    # Gate 3: healthy safety hard constraint (EVERY healthy pair <= MDE)
    g1_heal_pairs = agg["healthy_degradation_distribution"]["gated_scalar"]
    g1_heal_worst = max((p["delta"] for p in g1_heal_pairs), default=float("nan"))
    g3_pass = (np.isfinite(g1_heal_worst) and g1_heal_worst <= MDE)
    verdicts["gate3_healthy_safety"] = {
        "pass": bool(g3_pass), "g1_healthy_worst_pair": g1_heal_worst,
        "g1_healthy_cluster_mean": g1_heal["mean_delta"], "g1_healthy_ci_95": g1_heal["ci_95"],
        "false_activation_healthy": act["false_activation_healthy"],
        "n_healthy_pairs": act["n_healthy_pairs"],
        "rule": "every healthy pair delta<=0.005"}

    # Gate 4: strongest in safe-feasible set (apply healthy-safety to each competitor)
    safe_feasible = {}
    comp_vs_g1 = {}
    absorbed_by = None
    csd = agg["collapse_seed_deltas"]   # {method: [per-seed collapse delta vs baseline]}
    g1_sd = csd["gated_scalar"]
    for m in ("correct_pooled_sqrt_rms", "correct_per_pol_sqrt_rms", "robust_scalar",
              "M4_gated_policy", "D4_likelihood_gated_rde"):
        mpairs = agg["healthy_degradation_distribution"][m]
        hworst = max((p["delta"] for p in mpairs), default=float("nan"))
        safe = np.isfinite(hworst) and hworst <= MDE
        # paired (competitor - G1) on collapse, per seed (aligned order).
        # ABSORPTION = competitor IMPROVES over G1 by >MDE: competitor's collapse
        # delta is MORE NEGATIVE than G1's by >MDE, with paired CI UPPER < 0.
        comp_sd = csd[m]
        diff = [(cv - gv) for gv, cv in zip(g1_sd, comp_sd) if np.isfinite(gv) and np.isfinite(cv)]
        mean_diff = float(np.mean(diff)) if diff else float("nan")
        ci = (_boot_ci(diff) if diff else [float("nan"), float("nan")])
        comp_vs_g1[m] = {"mean_comp_minus_g1": mean_diff, "ci_95": ci,
                         "healthy_worst": hworst, "safe": bool(safe)}
        safe_feasible[m] = {"healthy_worst": hworst, "safe": bool(safe)}
        if safe and diff:
            if mean_diff < -MDE and ci[1] < 0:
                absorbed_by = m
    verdicts["gate4_strongest_safe_feasible"] = {
        "pass": bool(absorbed_by is None),
        "safe_feasible": safe_feasible,
        "comp_vs_g1_collapse_paired": comp_vs_g1,
        "absorbed_by_competitor": absorbed_by,
        "rule": "no safe-feasible competitor improves over G1 on collapse by >0.005 (paired CI_hi<0)"}
    g4_pass = (absorbed_by is None)

    # Gate 5: G1 vs M4 lineage ablation (collapse)
    g5_mean = g1_vm4["mean_delta_G1_minus_M4"]
    g5_cihi = g1_vm4["ci_95"][1]
    g5_pass = (np.isfinite(g5_mean) and g5_mean <= 0 and g5_cihi <= MDE)
    verdicts["gate5_g1_vs_m4_ablation"] = {
        "pass": bool(g5_pass), "mean_G1_minus_M4": g5_mean, "ci_95": g1_vm4["ci_95"],
        "rule": "mean<=0 AND CI_hi<=0.005"}

    # Gate 6: activation non-degeneracy + classification
    policies = set()
    # need to re-scan prefix_rows for policy diversity — use cluster_stats isn't enough;
    # pull from the activation build (we stored gate_active counts). Re-derive policy set
    # from the per-pair healthy_worst input is not available here; instead require:
    #   gate shows BOTH identity and active in fresh, hits >=1 collapse pair, and
    #   point precision>0.5, recall>0.5, bacc CI_lo>0.5.
    # policy diversity: false_activation_healthy>0 OR collapse_hits>0 means active seen;
    # and (n_healthy_pairs - false_activation_healthy)>0 OR exists identity on healthy.
    act_seen = (act["collapse_pairs_hit_by_gate"] > 0 or act["false_activation_healthy"] > 0)
    id_seen = (act["n_healthy_pairs"] - act["false_activation_healthy"] > 0) or \
              (act["tn"] > 0)  # tn = healthy correctly identity
    prec = act["precision"]
    rec = act["recall"]
    bacc_lo = act["bacc_ci_95"][0]
    g6_pass = (act_seen and id_seen and act["collapse_pairs_hit_by_gate"] >= 1
               and np.isfinite(prec) and prec > 0.5
               and np.isfinite(rec) and rec > 0.5
               and np.isfinite(bacc_lo) and bacc_lo > 0.5)
    verdicts["gate6_activation_non_degeneracy"] = {
        "pass": bool(g6_pass), "active_seen": bool(act_seen), "identity_seen": bool(id_seen),
        "collapse_pairs_hit": act["collapse_pairs_hit_by_gate"],
        "precision": prec, "recall": rec, "bacc_point": act["bacc_point"],
        "bacc_ci_95": act["bacc_ci_95"],
        "n_pos_recoverable": act["n_pos_recoverable"], "n_neg_healthy": act["n_neg_healthy"],
        "tp": act["tp"], "fp": act["fp"], "fn": act["fn"], "tn": act["tn"],
        "rule": "both policies seen AND >=1 collapse hit AND prec>0.5 AND rec>0.5 AND bacc_CI_lo>0.5"}

    # Gate 7: D4 recent comparator (subset of gate 4 but reported separately)
    d4_absorbs = (absorbed_by == "D4_likelihood_gated_rde")
    verdicts["gate7_d4_target_comparator"] = {
        "pass": bool(not d4_absorbs),
        "d4_healthy_worst": safe_feasible.get("D4_likelihood_gated_rde", {}).get("healthy_worst"),
        "d4_absorbs_g1": bool(d4_absorbs),
        "rule": "if D4 safe AND beats G1 on collapse by >0.005 (CI_lo>0) -> ABSORBED"}

    all_pass = all(verdicts[k]["pass"] for k in
                   ("gate1_class_support", "gate2_g1_vs_cma_collapse", "gate3_healthy_safety",
                    "gate4_strongest_safe_feasible", "gate5_g1_vs_m4_ablation",
                    "gate6_activation_non_degeneracy", "gate7_d4_target_comparator"))
    if all_pass:
        verdict = "G1_FORMAL_RECOMMENDATION_READY"
    elif not g1_pass:
        verdict = "G1_BLOCKED_CLASS_SUPPORT_NO_GO"
    elif d4_absorbs:
        verdict = "G1_ABSORBED_BY_TARGET_COMPARATOR_NO_GO"
    elif absorbed_by is not None:
        verdict = "G1_ABSORBED_BY_COMPETITOR_NO_GO"
    else:
        verdict = "G1_FORMAL_CONFIRM_NO_GO"
    return verdict, verdicts, details


def _source_hashes():
    def _sha(p):
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT).decode().strip()
    except Exception:
        commit = "unknown"
    return {
        "parent_commit": commit,
        "methods_py_sha256": _sha(SRC / "methods.py"),
        "run_g1_confirm_py_sha256": _sha(SRC / "run_g1_confirm.py"),
        "contract_yaml_sha256": _sha(G1_ROOT / "contract.yaml"),
        "t020_methods_py_sha256": _sha(T020_SRC / "methods.py"),
        "cb1_evaluator_py_sha256": _sha(BASELINE_ATLAS / "cb1_evaluator.py"),
        "cb1_cell_runner_py_sha256": _sha(BASELINE_ATLAS / "cb1_cell_runner.py"),
        "dual_pol_channel_py_sha256": _sha(SIM_DIR / "common" / "_dual_pol_channel.py"),
    }


def _formula_receipt():
    return {
        "G1_identity": "gate(healthy) -> z'=z (bit-identical to baseline)",
        "G1_collapsed": "gate(collapsed) -> a_x=sqrt(E|s|^2/robust_trim_mean(|z_pref_x|^2)), a_y similarly, z'=a*z",
        "E_abs2_Ps": float(G1M.E_ABS2),
        "gate_thresholds": {"collapse": G1_COLLAPSE, "spread": G1_SPREAD},
        "gate_features": ["mean_abs2", "spread_coeff_of_var"],
        "calib_prefix_symbols": CALIB_PREFIX,
        "offline_label": "run_factory._offline_label:558 (healthy b<0.1; awgn b>=0.1 & (b-o)<0.005; recoverable b>=0.1 & o<0.1 & (b-o)>=0.005; else ambiguous)",
        "MDE": MDE, "bootstrap": N_BOOT, "stat_unit": "seed_cluster",
        "primary_always_on_comparator": PRIMARY_ALWAYS_ON,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", default="all", choices=["smoke", "compare", "all"])
    ap.add_argument("--no-smoke", action="store_true", help="skip smoke (smoke already run via pytest)")
    args = ap.parse_args()

    smoke_ok = True
    if args.phase in ("smoke", "all") and not args.no_smoke:
        print("=" * 70 + "\nPHASE A: SMOKE (invoking pytest on tests/test_g1_semantic_smoke.py)\n" + "=" * 70)
        rc = subprocess.call([sys.executable, "-m", "pytest",
                              str(G1_ROOT / "tests" / "test_g1_semantic_smoke.py"), "-q"])
        smoke_ok = (rc == 0)
        if not smoke_ok:
            print("\n=== PHASE A: SMOKE BLOCKED ===")
            _write_result("G1_IDENTITY_OR_RECEIPT_BLOCKED_NO_GO", {}, {}, {}, {}, 0.0)
            return
        print("\n=== PHASE A: SMOKE PASS (9/9) ===\n")

    comp = {}
    if args.phase in ("compare", "all"):
        print("=" * 70 + f"\nPHASE B: COMPARE (7 cells x 20 fresh seeds 261-280; 8 methods)\n" + "=" * 70)
        comp = phase_compare()
        raw_p = G1_ROOT / "artifacts" / "raw-rows.csv"
        pre_p = G1_ROOT / "artifacts" / "prefix-receipt.csv"
        _write_csv(raw_p, comp["raw_rows"], RAW_FIELDS)
        _write_csv(pre_p, comp["prefix_rows"], PREFIX_FIELDS)
        print(f"  wrote {raw_p} ({len(comp['raw_rows'])} rows)")
        print(f"  wrote {pre_p} ({len(comp['prefix_rows'])} rows)")

    agg = {}
    verdict = "PENDING"
    gate_verdicts = {}
    if comp:
        print("\n" + "=" * 70 + "\nPHASE C: SEED-CLUSTER AGGREGATION + B4 GATES\n" + "=" * 70)
        agg = aggregate(comp["raw_rows"], comp["prefix_rows"])
        verdict, gate_verdicts, _det = apply_b4_gates(agg)
        _write_result(verdict, agg, gate_verdicts, comp, {}, comp["wall_seconds"])
        print(f"\n=== STATUS: {verdict} ===")
        for k, v in gate_verdicts.items():
            print(f"  {k}: {'PASS' if v.get('pass') else 'FAIL'} {v}")


def _write_result(verdict, agg, gate_verdicts, comp, smoke_res, wall):
    result = {
        "status": verdict,
        "candidate": "G1_SAFE_GATED_NORMALIZATION",
        "claim_ceiling": "CANDIDATE/LOCAL_SLICE",
        "method_identity": {
            "candidate": "gated_scalar (T020 gate collapse=0.6/spread=0.1 + per-pol correct sqrt scale)",
            "M": "baseline_cma_mu0p03 (tuned fixed-mu CMA identity)",
            "primary_always_on_comparator": "robust_scalar",
            "lineage_ablation": "M4_gated_policy (Q15 nonlinear map, NOT re-tuned)",
            "target_comparator": "D4_likelihood_gated_rde (Di Rosa JLT 2021 likelihood RDE)",
            "kill_only": "oracle_affine_bound (FR-21/FR-25; label only)",
        },
        "source_hashes": _source_hashes(),
        "seed_receipt": {
            "FRESH_SEEDS": FRESH_SEEDS, "n_seeds": len(FRESH_SEEDS),
            "disjoint_from": {"T020_T023_old_201_220": OLD_201_220,
                              "T023_fresh_241_260": FRESH_241_260,
                              "T020_dev_181_190": DEV_181_190},
            "receipt_file": "artifacts/seed-freeze-receipt.md",
        },
        "formula_receipt": _formula_receipt(),
        "frozen_axes": FROZEN_AXES,
        "cells": [c["id"] for c in CELLS],
        "method_order": METHOD_ORDER,
        "n_pairs": len(comp.get("prefix_rows", [])) if comp else 0,
        "n_raw_rows": len(comp.get("raw_rows", [])) if comp else 0,
        "wall_seconds": wall,
        "aggregation": agg,
        "b4_gate_verdicts": gate_verdicts,
        "smoke_results": smoke_res,
    }
    out = G1_ROOT / "artifacts" / "result.json"
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"\nWrote terminal result: {out}")


if __name__ == "__main__":
    main()
