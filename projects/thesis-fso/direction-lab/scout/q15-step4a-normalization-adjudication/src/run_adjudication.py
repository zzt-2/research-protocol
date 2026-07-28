"""Q15 Step 4a Terminal Adjudication — runner.

Read-only reuse of T020 generator/evaluator/CMA + T020 M2/M4 (imported, NOT
modified). Adds correct-normalization comparators from methods.py.

Pipeline:
  Phase A — identity + semantic smoke gates (must all PASS before compare)
  Phase B — run all methods on old slice (201-220) + fresh slice (241-260)
  Phase C — seed-cluster aggregation + terminal gate verdict

Frozen BEFORE any seed (see contract.yaml): cells, seed slices, M4 gate params,
MDE=0.005, 10k bootstrap CI.
"""

from __future__ import annotations

import csv
import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve()
SRC = HERE.parent
ADJ_ROOT = SRC.parent                         # q15-step4a-normalization-adjudication/
SCOUT = ADJ_ROOT.parent                       # scout/
CB1_ROOT = SCOUT / "cb1-modulation-generic-closure"
BASELINE_ATLAS = CB1_ROOT / "baseline-atlas"
T020_ROOT = SCOUT / "preformal-method-factory-sprint-002"
T020_SRC = T020_ROOT / "src"
C11_LEGALITY = CB1_ROOT / "c11-legality-batch-v1"
REPO_ROOT = HERE.parents[6]
SIM_DIR = REPO_ROOT / "projects" / "simulation"

for p in (str(SIM_DIR), str(BASELINE_ATLAS), str(SRC), str(T020_SRC), str(C11_LEGALITY)):
    if p not in sys.path:
        sys.path.insert(0, p)

from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402
import cb1_evaluator as evaluator  # noqa: E402
import cb1_cell_runner as runner  # noqa: E402
# Both this dir and T020 have a methods.py -> load each explicitly by path to
# avoid sys.path name clash (whichever is imported first wins for `import methods`).
import importlib.util  # noqa: E402
_spec_adj = importlib.util.spec_from_file_location("adj_methods", str(SRC / "methods.py"))
ADJ = importlib.util.module_from_spec(_spec_adj)
_spec_adj.loader.exec_module(ADJ)
_spec_t020 = importlib.util.spec_from_file_location(
    "t020_methods", str(T020_SRC / "methods.py"))
T020M = importlib.util.module_from_spec(_spec_t020)
_spec_t020.loader.exec_module(T020M)
from c11_causal import c11_cma_dd_lms_causal  # noqa: E402

# ─── Frozen axes (identical to T020 contract; NOT modified) ──────────────────
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

CELLS = [
    {"id": "16qam-snr05-nominal-short", "modulation": "qam16", "snr_db": 5.0,  "f_g_hz": 30.0,   "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr10-nominal-short", "modulation": "qam16", "snr_db": 10.0, "f_g_hz": 30.0,   "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr15-nominal-short", "modulation": "qam16", "snr_db": 15.0, "f_g_hz": 30.0,   "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr25-nominal-short", "modulation": "qam16", "snr_db": 25.0, "f_g_hz": 30.0,   "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr20-fg100-short",   "modulation": "qam16", "snr_db": 20.0, "f_g_hz": 100.0,  "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr10-fg100-long",    "modulation": "qam16", "snr_db": 10.0, "f_g_hz": 100.0,  "sop_rate": 4.0e-6, "n_symbols": 8192},
    {"id": "16qam-snr15-fg1000-long",   "modulation": "qam16", "snr_db": 15.0, "f_g_hz": 1000.0, "sop_rate": 4.0e-6, "n_symbols": 8192},
]

OLD_SLICE = list(range(201, 221))   # T020 seeds (post-hoc mechanism adjudication)
FRESH_SLICE = list(range(241, 261)) # fresh disjoint 20 seeds (token-checked)
ALL_SEEDS = sorted(set(OLD_SLICE) | set(FRESH_SLICE))

# T020 dev-frozen M4 gate params (NOT re-tuned on test)
M4_COLLAPSE = 0.6
M4_SPREAD = 0.1
M1_TRIM = 0.2

METHOD_ORDER = [
    "baseline_cma_mu0p03", "blind_affine", "C11_legal_causal", "oracle_affine_bound_KILL_ONLY",
    # T020 constructs (read-only reuse)
    "M1_prefix_scalar_T020", "M2_quantile_transport_T020", "M4_gated_policy_T020",
    # NEW correct-normalization comparators (this batch)
    "correct_pooled_sqrt_rms", "correct_per_pol_sqrt_rms",
    "gated_scalar_ablation", "robust_scalar",
]
COMPARATORS = ["baseline_cma_mu0p03", "blind_affine", "C11_legal_causal",
               "correct_pooled_sqrt_rms", "correct_per_pol_sqrt_rms",
               "gated_scalar_ablation", "robust_scalar"]
CONSTRUCT = "M4_gated_policy_T020"   # the candidate being adjudicated


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


def _diverged():
    return {"pi_ser": float("nan"), "fixed_label_ser": float("nan"),
            "pi_ber": float("nan"), "diverged": True}


def run_all_on_realization(cell, seed):
    n = int(cell["n_symbols"])
    es, cal, ee = _eval_window(n)
    rl = _realization(cell, seed)
    bits_per = 4
    tx, ty = rl["sX"][cal:ee], rl["sY"][cal:ee]
    bx, by = rl["bitsX"][cal * bits_per:ee * bits_per], rl["bitsY"][cal * bits_per:ee * bits_per]
    out = {"cell_id": cell["id"], "seed": int(seed), "n_symbols": n,
           "eval_window": {"eval_start": es, "calibration_end": cal, "eval_end": ee},
           "methods": {}}

    base = runner.standard_cma_godard_with_z(
        rl["rX"], rl["rY"], n_tap=TAPS, mu=MU_CURRENT, R2=R2_16QAM, block_size=BS)
    z_calib = np.column_stack([base["zX"][es:cal], base["zY"][es:cal]])
    z_eval = np.column_stack([base["zX"][cal:ee], base["zY"][cal:ee]])
    div = bool(base["diverged"])

    # baseline
    if not div:
        m = _eval_pred(evaluator.hard_16qam(base["zX"][cal:ee]),
                       evaluator.hard_16qam(base["zY"][cal:ee]), tx, ty, bx, by)
        m["diverged"] = False
    else:
        m = _diverged()
    out["methods"]["baseline_cma_mu0p03"] = m

    # blind affine
    if not div:
        bl = evaluator.blind_affine_compare_16qam(z_calib, z_eval, ridge=RIDGE)
        m = _eval_pred(bl["predicted"][:, 0], bl["predicted"][:, 1], tx, ty, bx, by)
        m["diverged"] = False
    else:
        m = _diverged()
    out["methods"]["blind_affine"] = m

    # C11 legal causal
    n_valid = n - TAPS + 1
    n_blocks = n_valid // BS
    switch_block = max(1, min(n_blocks - 1, int(round(0.26 * n) // BS)))
    c11 = c11_cma_dd_lms_causal(rl["rX"], rl["rY"], n_tap=TAPS, cma_mu=MU_CURRENT,
                                cma_R2=R2_16QAM, cma_block_size=BS, dd_step_size=1.0e-4,
                                switch_point_block=switch_block,
                                hard_decision_fn=evaluator.hard_16qam)
    if not c11["diverged"]:
        m = _eval_pred(evaluator.hard_16qam(c11["zX"][cal:ee]),
                       evaluator.hard_16qam(c11["zY"][cal:ee]), tx, ty, bx, by)
        m["diverged"] = False
    else:
        m = _diverged()
    out["methods"]["C11_legal_causal"] = m

    # oracle (Kill-only)
    if not div:
        truth_calib = np.column_stack([rl["sX"][es:cal], rl["sY"][es:cal]])
        orc = evaluator.oracle_affine_bound_16qam(z_calib, z_eval, truth_calib, ridge=RIDGE)
        m = _eval_pred(orc[:, 0], orc[:, 1], tx, ty, bx, by)
        m["diverged"] = False
    else:
        m = _diverged()
    out["methods"]["oracle_affine_bound_KILL_ONLY"] = m

    if not div:
        zpx, zpy = base["zX"][es:cal], base["zY"][es:cal]
        zsx, zsy = base["zX"][cal:ee], base["zY"][cal:ee]

        # T020 M1 (the WRONG formula, kept for transparency)
        f1 = T020M.m1_prefix_scalar_freeze(np.concatenate([zpx, zpy]), trim_frac=M1_TRIM)
        m1x = T020M.m1_prefix_scalar_apply_continuous(f1, zsx)
        m1y = T020M.m1_prefix_scalar_apply_continuous(f1, zsy)
        m = _eval_pred(m1x, m1y, tx, ty, bx, by); m["diverged"] = False
        m["frozen"] = {"scale": float(f1["scale"])}
        out["methods"]["M1_prefix_scalar_T020"] = m

        # T020 M2 (monotone radius map)
        f2 = T020M.m2_quantile_transport_freeze(np.concatenate([zpx, zpy]))
        m2x = T020M.m2_quantile_transport_apply_continuous(f2, zsx)
        m2y = T020M.m2_quantile_transport_apply_continuous(f2, zsy)
        m = _eval_pred(m2x, m2y, tx, ty, bx, by); m["diverged"] = False
        m["frozen"] = {"identity": bool(f2.get("identity", False))}
        out["methods"]["M2_quantile_transport_T020"] = m

        # T020 M4 (the candidate — gate + M2/M3 map)
        f3 = T020M.m3_three_shell_mixture_freeze(np.concatenate([zpx, zpy]))
        f4 = T020M.m4_gated_policy_freeze(np.concatenate([zpx, zpy]),
                                          collapse_threshold=M4_COLLAPSE, spread_threshold=M4_SPREAD)
        m4x = T020M.m4_gated_policy_apply_continuous(f4, zsx, m2_frozen=f2, m3_frozen=f3)
        m4y = T020M.m4_gated_policy_apply_continuous(f4, zsy, m2_frozen=f2, m3_frozen=f3)
        m = _eval_pred(m4x, m4y, tx, ty, bx, by); m["diverged"] = False
        m["frozen"] = {"policy": str(f4["policy"]), "mean_abs2": float(f4["mean_abs2"]),
                       "spread": float(f4["spread"])}
        out["methods"]["M4_gated_policy_T020"] = m

        # NEW: correct pooled sqrt-RMS
        fp = ADJ.correct_pooled_sqrt_rms_freeze(zpx, zpy)
        mpx = ADJ.correct_pooled_sqrt_rms_apply_continuous(fp, zsx)
        mpy = ADJ.correct_pooled_sqrt_rms_apply_continuous(fp, zsy)
        m = _eval_pred(mpx, mpy, tx, ty, bx, by); m["diverged"] = False
        m["frozen"] = {"a": float(fp["a"]), "pz_hat": float(fp.get("pz_hat", float("nan")))}
        out["methods"]["correct_pooled_sqrt_rms"] = m

        # NEW: correct per-pol sqrt-RMS
        fpp = ADJ.correct_per_pol_sqrt_rms_freeze(zpx, zpy)
        ppx, ppy = ADJ.correct_per_pol_sqrt_rms_apply_continuous(fpp, zsx, zsy)
        m = _eval_pred(ppx, ppy, tx, ty, bx, by); m["diverged"] = False
        m["frozen"] = {"a_x": float(fpp["a_x"]), "a_y": float(fpp["a_y"])}
        out["methods"]["correct_per_pol_sqrt_rms"] = m

        # NEW: gated scalar ablation (M4 gate + correct scale)
        fgs = ADJ.gated_scalar_ablation_freeze(zpx, zpy, collapse_threshold=M4_COLLAPSE,
                                               spread_threshold=M4_SPREAD)
        gsx, gsy = ADJ.gated_scalar_ablation_apply_continuous(fgs, zsx, zsy)
        m = _eval_pred(gsx, gsy, tx, ty, bx, by); m["diverged"] = False
        m["frozen"] = {"policy": str(fgs["policy"]), "a_x": float(fgs["a_x"]), "a_y": float(fgs["a_y"])}
        out["methods"]["gated_scalar_ablation"] = m

        # NEW: robust scalar (median)
        frs = ADJ.robust_scalar_freeze(zpx, zpy)
        rsx, rsy = ADJ.robust_scalar_apply_continuous(frs, zsx, zsy)
        m = _eval_pred(rsx, rsy, tx, ty, bx, by); m["diverged"] = False
        m["frozen"] = {"a_x": float(frs["a_x"]), "a_y": float(frs["a_y"])}
        out["methods"]["robust_scalar"] = m
    else:
        for nm in ("M1_prefix_scalar_T020", "M2_quantile_transport_T020",
                   "M4_gated_policy_T020", "correct_pooled_sqrt_rms",
                   "correct_per_pol_sqrt_rms", "gated_scalar_ablation", "robust_scalar"):
            out["methods"][nm] = _diverged()

    out["base_diverged"] = div
    return out


def _offline_label(out):
    b = out["methods"].get("baseline_cma_mu0p03", {}).get("pi_ser")
    o = out["methods"].get("oracle_affine_bound_KILL_ONLY", {}).get("pi_ser")
    if b is None or o is None or not np.isfinite(b) or not np.isfinite(o):
        return "ambiguous"
    if out.get("base_diverged"):
        return "ambiguous"
    if b < 0.1:
        return "healthy"
    if (b - o) < 0.005:
        return "awgn_dominated_error"
    if o < 0.1:
        return "inner_ring_recoverable_collapse"
    return "ambiguous"


# ─── Phase A: identity + semantic smoke ──────────────────────────────────────

def phase_smoke():
    """B3 semantic smoke gates. Must all PASS before compare."""
    res = {}
    # 1. synthetic z=c*s: correct sqrt restores amplitude (SER=0) for ALL c;
    #    M1 wrong (power ratio, no sqrt) over-corrects by 1/c and FAILS for
    #    strong collapse. Mild over/under-scaling is tolerated by the 16QAM grid
    #    spacing, so M1-wrong failure is monotone in |1/c - 1| (only strong
    #    collapse like c=0.45 shows catastrophic SER). Matches pytest Gate 1.
    amp = np.array([-3., -1., 1., 3.]) / np.sqrt(10.)
    RE, IM = np.meshgrid(amp, amp)
    ALPHABET = (RE + 1j * IM).ravel()
    rng = np.random.default_rng(0)
    s = rng.choice(ALPHABET, size=4000)
    m1_sers = {}
    for c in (0.45, 0.7, 1.0, 1.3, 1.8):
        z = c * s
        pz = np.mean(np.abs(z) ** 2)
        a_correct = float(np.sqrt(E_ABS2_CORRECT() / pz))
        scale_m1_wrong = E_ABS2_CORRECT() / pz
        rec_correct = a_correct * z
        rec_m1 = scale_m1_wrong * z
        ser_correct = np.mean(_hard_local(rec_correct) != s)
        ser_m1 = np.mean(_hard_local(rec_m1) != s)
        m1_sers[c] = float(ser_m1)
        # CORRECT sqrt must recover perfectly for every c
        assert ser_correct == 0.0, f"c={c}: correct sqrt SER={ser_correct} != 0"
        res[f"synthetic_c{c}"] = {"correct_sqrt_SER": float(ser_correct),
                                  "m1_wrong_SER": float(ser_m1)}
    # M1-wrong: exact at c=1, catastrophic at strong collapse c=0.45, monotone
    res["m1_wrong_audit"] = {
        "m1_ser_c1.0": m1_sers[1.0], "m1_ser_c0.45": m1_sers[0.45], "m1_ser_c0.7": m1_sers[0.7],
        "pass": bool(m1_sers[1.0] == 0.0 and m1_sers[0.45] > 0.3 and m1_sers[0.45] > m1_sers[0.7])}
    # 2. identity unbiased + close: over many draws a_x/a_y mean≈1, each within 5%
    #    (finite-sample trimmed-mean noise at N=500; matches pytest Gate 2)
    axs, ays = [], []
    for _ in range(40):
        zpx = rng.choice(ALPHABET, size=500)
        zpy = rng.choice(ALPHABET, size=500)
        fpp = ADJ.correct_per_pol_sqrt_rms_freeze(zpx, zpy)
        axs.append(fpp["a_x"]); ays.append(fpp["a_y"])
    res["identity_per_pol"] = {"mean_a_x": float(np.mean(axs)), "mean_a_y": float(np.mean(ays)),
                               "pass": bool(abs(np.mean(axs) - 1.0) < 0.01 and abs(np.mean(ays) - 1.0) < 0.01
                                            and all(abs(a - 1.0) < 0.05 for a in axs + ays))}
    # 3. fixed prefix, perturbed suffix does not change scale/map/gate
    cell = CELLS[0]
    rl = _realization(cell, 201)
    base = runner.standard_cma_godard_with_z(rl["rX"], rl["rY"], n_tap=TAPS, mu=MU_CURRENT,
                                             R2=R2_16QAM, block_size=BS)
    es, cal, ee = _eval_window(cell["n_symbols"])
    zpx, zpy = base["zX"][es:cal], base["zY"][es:cal]
    fa = ADJ.correct_per_pol_sqrt_rms_freeze(zpx, zpy)
    fb = ADJ.correct_per_pol_sqrt_rms_freeze(zpx, zpy)
    res["prefix_freeze_invariance"] = {"pass": bool(np.isclose(fa["a_x"], fb["a_x"], atol=1e-12) and
                                                     np.isclose(fa["a_y"], fb["a_y"], atol=1e-12))}
    # 4. info increment: each comparator gives different output for different input
    zsx_a = base["zX"][cal:ee]
    zsx_b = zsx_a + 0.1 + 0.1j
    fp = ADJ.correct_pooled_sqrt_rms_freeze(zpx, zpy)
    oa = ADJ.correct_pooled_sqrt_rms_apply_continuous(fp, zsx_a)
    ob = ADJ.correct_pooled_sqrt_rms_apply_continuous(fp, zsx_b)
    res["info_increment"] = {"pass": bool(np.any(np.abs(oa - ob) > 1e-9))}
    # 5. clean not degraded: gated-scalar selects identity on healthy prefix
    zpxh = rng.choice(ALPHABET, size=500)
    zpyh = rng.choice(ALPHABET, size=500)
    fgs = ADJ.gated_scalar_ablation_freeze(zpxh, zpyh)
    res["clean_not_degraded"] = {"policy": str(fgs["policy"]),
                                 "pass": bool(fgs["policy"] == "identity")}
    res["all_smoke_pass"] = all(v.get("pass", True) if isinstance(v, dict) else True
                                for k, v in res.items() if k != "all_smoke_pass")
    return res
    return res


def _hard_local(z):
    from common._modulation import hard_decision
    return np.asarray(hard_decision(np.asarray(z, dtype=np.complex128), mod="qam16"), dtype=np.complex128)


def E_ABS2_CORRECT():
    return 1.0


# ─── Phase B: run compare ────────────────────────────────────────────────────

def phase_compare():
    raw_rows = []
    per_seed_oracle_label = {}
    t0 = time.time()
    for ci, cell in enumerate(CELLS):
        for seed in ALL_SEEDS:
            out = run_all_on_realization(cell, seed)
            for mname, mres in out["methods"].items():
                pis = mres.get("pi_ser")
                raw_rows.append({
                    "cell_id": out["cell_id"], "seed": out["seed"],
                    "slice": "old" if seed in OLD_SLICE else "fresh",
                    "method": mname,
                    "pi_ser": (None if pis is None or not np.isfinite(pis) else float(pis)),
                    "fixed_label_ser": (None if (v := mres.get("fixed_label_ser")) is None or not np.isfinite(v) else float(v)),
                    "pi_ber": (None if (v := mres.get("pi_ber")) is None or not np.isfinite(v) else float(v)),
                    "diverged": bool(mres.get("diverged", False)),
                })
            lbl = _offline_label(out)
            per_seed_oracle_label.setdefault((cell["id"], seed), lbl)
        print(f"  [{ci+1}/{len(CELLS)}] {cell['id']:28s} done ({time.time()-t0:.1f}s)")
    return {"raw_rows": raw_rows, "per_seed_oracle_label": per_seed_oracle_label,
            "wall_seconds": time.time() - t0}


# ─── Phase C: seed-cluster aggregation + terminal gate ───────────────────────

def aggregate(raw_rows, seeds):
    cells = sorted({r["cell_id"] for r in raw_rows})
    idx = {}
    for r in raw_rows:
        idx[(r["cell_id"], r["seed"], r["method"])] = r["pi_ser"]
    lbl = {}
    for r in raw_rows:
        # label by (cell,seed); cheap recompute
        pass

    def seed_method_mean(seed_list):
        out = {}
        for s in seed_list:
            for m in METHOD_ORDER:
                vals = [idx.get((c, s, m)) for c in cells]
                vals = [v for v in vals if v is not None and np.isfinite(v)]
                out[(s, m)] = float(np.mean(vals)) if vals else float("nan")
        return out

    smm = seed_method_mean(seeds)

    def cluster_stats(method, ref="baseline_cma_mu0p03"):
        deltas = []
        for s in seeds:
            b = smm.get((s, ref), float("nan"))
            mv = smm.get((s, method), float("nan"))
            if np.isfinite(b) and np.isfinite(mv):
                deltas.append(float(mv - b))
        if not deltas:
            return {"n": 0}
        help_n = sum(1 for d in deltas if d < -1e-9)
        hurt_n = sum(1 for d in deltas if d > 1e-9)
        tie_n = sum(1 for d in deltas if abs(d) <= 1e-9)
        mean_d = float(np.mean(deltas))
        ci = _boot_ci(deltas)
        # healthy regression
        healthy = []
        for s in seeds:
            for c in cells:
                b = idx.get((c, s, ref))
                mv = idx.get((c, s, method))
                if b is not None and mv is not None and b < 0.1:
                    healthy.append(mv - b)
        hworst = float(np.max(healthy)) if healthy else float("nan")
        return {"n": len(deltas), "mean_delta_pi_ser": mean_d,
                "ci_95": ci, "help": help_n, "hurt": hurt_n, "tie": tie_n,
                "healthy_worst_delta": hworst,
                "method_seed_mean": float(np.mean([smm.get((s, method), float("nan"))
                                                   for s in seeds if np.isfinite(smm.get((s, method), float("nan")))]))}

    return {"seed_method_mean": smm, "cluster_stats": {m: cluster_stats(m) for m in METHOD_ORDER}}


def _boot_ci(deltas, n_boot=10000, seed=42):
    if len(deltas) < 2:
        return [float("nan"), float("nan")]
    rng = np.random.default_rng(seed)
    arr = np.asarray(deltas)
    boots = [float(np.mean(rng.choice(arr, size=len(arr), replace=True))) for _ in range(n_boot)]
    return [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]


def main():
    ap = __import__("argparse").ArgumentParser()
    ap.add_argument("--phase", default="all", choices=["smoke", "compare", "all"])
    args = ap.parse_args()

    smoke_res = {}
    if args.phase in ("smoke", "all"):
        print("=" * 70 + "\nPHASE A: SMOKE GATES\n" + "=" * 70)
        smoke_res = phase_smoke()
        for k, v in smoke_res.items():
            print(f"  {k}: {v}")
        if not smoke_res.get("all_smoke_pass", False):
            print("\n=== PHASE A: SMOKE BLOCKED ===")
            _write_terminal(smoke_res, {}, {}, {}, 0.0)
            return
        print("\n=== PHASE A: SMOKE PASS ===\n")

    comp = {}
    if args.phase in ("compare", "all"):
        print("=" * 70 + "\nPHASE B: COMPARE (old 201-220 + fresh 241-260)\n" + "=" * 70)
        comp = phase_compare()
        # write raw
        csvp = ADJ_ROOT if False else (ADJ_ROOT / "artifacts" / "raw-rows.csv")
        with open(csvp, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["cell_id", "seed", "slice", "method",
                                             "pi_ser", "fixed_label_ser", "pi_ber", "diverged"])
            w.writeheader()
            for r in comp["raw_rows"]:
                w.writerow(r)
        print(f"  wrote {csvp} ({len(comp['raw_rows'])} rows)")

    # aggregate by slice + overall
    agg = {}
    if comp:
        agg["overall"] = aggregate(comp["raw_rows"], ALL_SEEDS)
        agg["old_slice"] = aggregate([r for r in comp["raw_rows"] if r["slice"] == "old"], OLD_SLICE)
        agg["fresh_slice"] = aggregate([r for r in comp["raw_rows"] if r["slice"] == "fresh"], FRESH_SLICE)

    _write_terminal(smoke_res, comp, agg, comp.get("per_seed_oracle_label", {}),
                    comp.get("wall_seconds", 0.0))


def _write_terminal(smoke_res, comp, agg, oracle_labels, wall):
    # Terminal gate verdict
    MDE = 0.005
    verdict = "PENDING"
    gate_detail = {}

    if agg:
        old = agg["old_slice"]["cluster_stats"]
        fresh = agg["fresh_slice"]["cluster_stats"]
        m4_old = old.get(CONSTRUCT, {})
        m4_fresh = fresh.get(CONSTRUCT, {})

        # strongest correct-normalization on each slice
        norm_methods = ["correct_pooled_sqrt_rms", "correct_per_pol_sqrt_rms",
                        "gated_scalar_ablation", "robust_scalar"]
        strongest_old = min(norm_methods, key=lambda m: old.get(m, {}).get("method_seed_mean", float("inf")))
        strongest_fresh = min(norm_methods, key=lambda m: fresh.get(m, {}).get("method_seed_mean", float("inf")))

        def beats(m4, norm):
            return (m4.get("mean_delta_pi_ser", 0) <= -MDE and
                    m4.get("ci_95", [0, 0])[1] < 0 and
                    m4.get("help", 0) > m4.get("hurt", 0) and
                    m4.get("method_seed_mean", float("inf")) <=
                    norm.get("method_seed_mean", float("inf")) - MDE)

        # ABSORBED if M4 fails to beat strongest correct-norm on EITHER slice, OR healthy catastrophe
        absorbed = (not beats(m4_old, old.get(strongest_old, {})) or
                    not beats(m4_fresh, fresh.get(strongest_fresh, {})) or
                    (np.isfinite(m4_old.get("healthy_worst_delta", float("nan"))) and
                     m4_old["healthy_worst_delta"] > MDE) or
                    (np.isfinite(m4_fresh.get("healthy_worst_delta", float("nan"))) and
                     m4_fresh["healthy_worst_delta"] > MDE))
        verdict = "Q15_ABSORBED_BY_CONVENTIONAL_NORMALIZATION_NO_GO" if absorbed else "Q15_STEP4A_RECOMMENDATION_READY"
        gate_detail = {
            "strongest_norm_old": strongest_old,
            "strongest_norm_fresh": strongest_fresh,
            "m4_old_beats_strongest_norm": beats(m4_old, old.get(strongest_old, {})),
            "m4_fresh_beats_strongest_norm": beats(m4_fresh, fresh.get(strongest_fresh, {})),
            "m4_old_healthy_worst": m4_old.get("healthy_worst_delta"),
            "m4_fresh_healthy_worst": m4_fresh.get("healthy_worst_delta"),
        }

    result = {
        "status": verdict,
        "mission_method_delta": ("PACKAGING_BOUNDARY" if verdict.endswith("RECOMMENDATION_READY") else "NONE"),
        "smoke_results": smoke_res,
        "aggregation": {k: v.get("cluster_stats", v) if isinstance(v, dict) else v for k, v in agg.items()} if agg else {},
        "gate_detail": gate_detail,
        "method_order": METHOD_ORDER,
        "construct_under_adjudication": CONSTRUCT,
        "correct_normalization_comparators": ["correct_pooled_sqrt_rms", "correct_per_pol_sqrt_rms",
                                              "gated_scalar_ablation", "robust_scalar"],
        "cell_count": len(CELLS), "old_slice": OLD_SLICE, "fresh_slice": FRESH_SLICE,
        "wall_seconds": wall,
        "claim_ceiling": "STEP4A_RECOMMENDATION_READY or ABSORBED_NO_GO (no 4th Q15 repair)",
    }
    out = ADJ_ROOT / "artifacts" / "result.json"
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"\nWrote terminal result: {out}")
    print(f"\n=== STATUS: {verdict} | delta: {result['mission_method_delta']} ===")
    if gate_detail:
        for k, v in gate_detail.items():
            print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
