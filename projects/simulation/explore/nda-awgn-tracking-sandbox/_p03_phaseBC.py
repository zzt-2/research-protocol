# -*- coding: utf-8 -*-
"""P03 (T031) Phase B/C — mixed-precision candidates + fair comparison.

ONLY run if Phase A shows a real resource-performance tension. Runs on fresh
held-out seeds (dev-tuning uses seeds 10-19, disjoint from Phase A's dev 0-9
and from held-out 30-49 — see worker-log §1 for the seed isolation choice).

Candidates (each a DIFFERENT deployable bit-allocation / scaling action):
  M1 stage_widths       : CV datapath narrow, stage-2 datapath wide.
  M2 two_exp            : stage-2 carries its own block-float exponent.
  M3 boundary_adaptive  : narrow default, wide re-eval near decision boundary.
  M4 narrow_acc         : trim accumulator guard bits (resource only).

EFFICIENCY: the whole candidate search space (every dev config of every
mechanism + the uniform comparator ladder + float bypass) is batched into ONE
channel pass per (scene, gamma, seed) via extra_selector. This makes every
comparison strictly paired (identical channel) and avoids the ~20x channel-
regeneration cost of running candidates one-at-a-time.

Fair comparison:
  - uniform comparator gets the SAME dev tuning (best (W,F) on dev seeds 10-19).
  - each mixed candidate's per-stage widths are dev-tuned on seeds 10-19.
  - final comparison on fresh held-out seeds 30-49 (paired, channel-identical).
  - ablation: control total bit budget so mixed vs uniform at equal total bits.

Discipline: only the selector CONTROL PATH touched. Branch outputs are frozen
per-window errors from run_case_multidelta. delta=0 only.
"""
import os
import sys
import time
import argparse
from datetime import datetime, timezone

import numpy as np
from scipy import stats

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
sys.path[:0] = [_SIM_ROOT, os.path.join(_SIM_ROOT, 'simulator'), _HERE]

from _p01_cpr_snr_mismatch_probe import run_case_multidelta  # noqa: E402
from _p03_fixed_point import (  # noqa: E402
    decide_fp, decide_fp_mixed_stage_widths, decide_fp_mixed_two_exp,
    decide_fp_mixed_boundary_adaptive, decide_fp_mixed_narrow_acc,
    selector_resource_proxy, selector_resource_proxy_mixed,
)
from common import save_results  # noqa: E402

SCENES = ("weak", "moderate", "strong")
SNR_DB = tuple(map(float, range(5, 26, 2)))
FLOAT_BYPASS = (64, 40)

# Seed isolation (frozen in worker-log §1):
#   Phase A used dev seeds 0-9 (anchor subset, range-finding + uniform ladder).
#   Phase B dev-tuning uses seeds 10-19 (disjoint from 0-9 AND from held-out).
#   Fresh held-out test = seeds 30-49 (P01's held-out; P03 estimand is a
#   bitwidth CONFIG not a gain fit -> no leakage, brief §3.4).
DEV_SEEDS_BC = list(range(10, 20))         # 10 seeds, dev tuning for mixed
HELDOUT_SEEDS = list(range(30, 50))        # 20 fresh held-out seeds

OUT_DIR = os.path.join(_SIM_ROOT, "results", "p03_fixed_point_codesign")


def ci_t(data):
    a = np.asarray(data, dtype=float)
    n = len(a)
    mean = float(np.mean(a))
    std = float(np.std(a, ddof=1)) if n > 1 else 0.0
    hw = float(stats.t.ppf(0.975, n - 1)) * std / np.sqrt(n) if n > 1 else 0.0
    return mean, std, hw, mean - hw, mean + hw


# ============================================================================
# candidate factories: (name, fn) — each name encodes its config.
# ============================================================================
def _uniform_fn(W, F):
    return lambda raw, gdb, glin, b: decide_fp(raw, gdb, glin, W, F)


def _stage_widths_fn(W_cv, F_cv, W_s2, F_s2):
    return lambda raw, gdb, glin, b: decide_fp_mixed_stage_widths(
        raw, gdb, glin, W_cv, F_cv, W_s2, F_s2)


def _two_exp_fn(W, F):
    return lambda raw, gdb, glin, b: decide_fp_mixed_two_exp(raw, gdb, glin, W, F)


def _boundary_fn(W_n, F_n, W_w, F_w):
    return lambda raw, gdb, glin, b: decide_fp_mixed_boundary_adaptive(
        raw, gdb, glin, W_n, F_n, W_w, F_w)


def _narrow_acc_fn(W, F, acc_guard=0):
    return lambda raw, gdb, glin, b: decide_fp_mixed_narrow_acc(
        raw, gdb, glin, W, F)


# Frozen candidate dev search spaces (chosen BEFORE running dev data).
UNIFORM_SEARCH = [(6, 4), (8, 6), (10, 8), (12, 10), (14, 12), (16, 14)]
STAGE_WIDTHS_SEARCH = [
    (6, 4, 10, 8), (6, 4, 12, 10), (8, 6, 12, 10), (8, 6, 14, 12),
    (10, 8, 14, 12),
]
TWO_EXP_SEARCH = [(6, 4), (8, 6), (10, 8), (12, 10)]
BOUNDARY_SEARCH = [(6, 4, 12, 10), (6, 4, 14, 12), (8, 6, 14, 12)]
NARROW_ACC_SEARCH = [(8, 6), (10, 8), (12, 10)]


def _all_dev_configs():
    """Return {name: fn} for EVERY config in EVERY candidate's search space.

    This is the full dev-tuning set, batched into one channel pass per cell.
    Names are chosen so the mechanism + config can be parsed back out.
    """
    d = {}
    for (W, F) in UNIFORM_SEARCH:
        d[f"uniform_{W}_{F}"] = _uniform_fn(W, F)
    for (Wcv, Fcv, Ws2, Fs2) in STAGE_WIDTHS_SEARCH:
        d[f"stage_widths_{Wcv}_{Fcv}_{Ws2}_{Fs2}"] = _stage_widths_fn(Wcv, Fcv, Ws2, Fs2)
    for (W, F) in TWO_EXP_SEARCH:
        d[f"two_exp_{W}_{F}"] = _two_exp_fn(W, F)
    for (Wn, Fn, Ww, Fw) in BOUNDARY_SEARCH:
        d[f"boundary_{Wn}_{Fn}_{Ww}_{Fw}"] = _boundary_fn(Wn, Fn, Ww, Fw)
    for (W, F) in NARROW_ACC_SEARCH:
        d[f"narrow_acc_{W}_{F}"] = _narrow_acc_fn(W, F, 0)
    return d


# resource-proxy lookups per config (deterministic, no synthesis).
def _res_uniform(W, F):
    rp = selector_resource_proxy(W, F, 256)
    return {"op_bit_proxy": rp["op_bit_proxy"], "storage_bit_proxy": rp["storage_bit_proxy"]}


def _res_stage_widths(W_cv, F_cv, W_s2, F_s2):
    rp = selector_resource_proxy_mixed(
        {"kind": "stage_widths", "W_cv": W_cv, "F_cv": F_cv,
         "W_s2": W_s2, "F_s2": F_s2}, 256)
    return {"op_bit_proxy": rp["op_bit_proxy"], "storage_bit_proxy": rp["storage_bit_proxy"]}


def _res_two_exp(W, F):
    rp = selector_resource_proxy_mixed({"kind": "two_exp", "W": W, "F": F}, 256)
    return {"op_bit_proxy": rp["op_bit_proxy"], "storage_bit_proxy": rp["storage_bit_proxy"]}


def _res_boundary(W_n, F_n, W_w, F_w):
    rp = selector_resource_proxy_mixed(
        {"kind": "boundary_adaptive", "W_narrow": W_n, "F_narrow": F_n,
         "W_wide": W_w, "F_wide": F_w}, 256)
    return {"op_bit_proxy": rp["op_bit_proxy"], "storage_bit_proxy": rp["storage_bit_proxy"]}


def _res_narrow_acc(W, F):
    rp = selector_resource_proxy_mixed(
        {"kind": "narrow_acc", "W": W, "F": F, "acc_guard": 0}, 256)
    return {"op_bit_proxy": rp["op_bit_proxy"], "storage_bit_proxy": rp["storage_bit_proxy"]}


def _res_for_name(name):
    """Parse a config name back to its (mechanism, config, resource_proxy)."""
    parts = name.split("_")
    if name.startswith("uniform_"):
        W, F = int(parts[1]), int(parts[2])
        return "uniform", {"W": W, "F": F}, _res_uniform(W, F)
    if name.startswith("stage_widths_"):
        Wcv, Fcv, Ws2, Fs2 = (int(parts[2]), int(parts[3]), int(parts[4]), int(parts[5]))
        return "stage_widths", {"W_cv": Wcv, "F_cv": Fcv, "W_s2": Ws2, "F_s2": Fs2}, \
            _res_stage_widths(Wcv, Fcv, Ws2, Fs2)
    if name.startswith("two_exp_"):
        W, F = int(parts[2]), int(parts[3])
        return "two_exp", {"W": W, "F": F}, _res_two_exp(W, F)
    if name.startswith("boundary_"):
        Wn, Fn, Ww, Fw = (int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]))
        # NOTE: name is boundary_{Wn}_{Fn}_{Ww}_{Fw} (no 'boundary_' split issue
        # because mechanism prefix is 'boundary'). Re-derive robustly.
        nums = [p for p in parts if p.isdigit()]
        Wn, Fn, Ww, Fw = int(nums[0]), int(nums[1]), int(nums[2]), int(nums[3])
        return "boundary_adaptive", {"W_narrow": Wn, "F_narrow": Fn, "W_wide": Ww, "F_wide": Fw}, \
            _res_boundary(Wn, Fn, Ww, Fw)
    if name.startswith("narrow_acc_"):
        nums = [p for p in parts if p.isdigit()]
        W, F = int(nums[0]), int(nums[1])
        return "narrow_acc", {"W": W, "F": F, "acc_guard": 0}, _res_narrow_acc(W, F)
    raise ValueError(f"unknown config name: {name}")


# ============================================================================
# BATCHED evaluation: ALL selectors + bypass share ONE channel pass per cell.
# ============================================================================
def run_batched(cells, seeds, selectors, tag):
    """Run a dict of {name: fn} selectors over cells x seeds, batched.

    All selectors + the float bypass share ONE channel pass per
    (scene, gamma, seed) -> strictly paired, channel-identical comparison.
    Returns raw_rows.
    """
    t0 = time.time()
    raw_rows = []
    total = len(cells) * len(seeds)
    done = 0
    for scene, snr in cells:
        for seed in seeds:
            specs = {name: {"fn": fn, "needs_pilot": False, "needs_reset": False}
                     for name, fn in selectors.items()}
            specs["__bypass__"] = {"fn": _uniform_fn(*FLOAT_BYPASS),
                                   "needs_pilot": False, "needs_reset": False}
            md = run_case_multidelta(scene, snr, seed, deltas=(0.0,),
                                     extra_selector=specs)
            base = md["base"]
            pw_da = base["per_window_da_err"]
            pw_nda = base["per_window_nda_err"]
            n_win = base["n_windows"]
            bypass_choices = md["per_delta_extra"]["__bypass__"][0.0]["choices"]
            bypass_sel = md["per_delta_extra"]["__bypass__"][0.0]["selected_errors"]
            for name in selectors:
                pe = md["per_delta_extra"][name][0.0]
                ch = pe["choices"]
                fp_sel = pe["selected_errors"]
                agree = sum(1 for a, b in zip(bypass_choices, ch) if a == b) / n_win
                regret_err = 0
                for i in range(n_win):
                    if ch[i] != bypass_choices[i]:
                        fp_e = int(pw_da[i]) if ch[i] == "da" else int(pw_nda[i])
                        bp_e = int(pw_da[i]) if bypass_choices[i] == "da" else int(pw_nda[i])
                        regret_err += (fp_e - bp_e)
                regret_db = (10.0 * np.log10(fp_sel / bypass_sel)
                             if bypass_sel > 0 and fp_sel > 0
                             else (float("inf") if fp_sel > 0 else 0.0))
                raw_rows.append({
                    "tag": tag, "scene": scene, "gamma_true_db": float(snr),
                    "seed_index": int(seed), "method": name,
                    "fp_selected_errors": int(fp_sel),
                    "bypass_selected_errors": int(bypass_sel),
                    "decision_agreement_vs_float": float(agree),
                    "wrong_branch_regret_errors": int(regret_err),
                    "wrong_branch_regret_db": float(regret_db),
                    "n_windows": int(n_win),
                })
            done += 1
        el = time.time() - t0
        print(f"  [{tag}] {scene}@{snr:.0f}dB done ({done}/{total} seed-cells, "
              f"{el:.0f}s)", flush=True)
    return raw_rows


def aggregate_rows(raw_rows, names):
    """Per (method-name) pooled over cells; mean regret_db + CI + agreement."""
    out = []
    for n in names:
        sub = [r for r in raw_rows if r["method"] == n]
        if not sub:
            continue
        regrets = [r["wrong_branch_regret_db"] for r in sub
                   if r["wrong_branch_regret_db"] != float("inf")]
        agrees = [r["decision_agreement_vs_float"] for r in sub]
        m_r, s_r, _, lo_r, hi_r = ci_t(regrets) if regrets else (float("nan"),)*5
        m_a, *_ = ci_t(agrees)
        out.append({
            "method": n, "n_rows": int(len(sub)),
            "regret_db_mean": float(m_r), "regret_db_std": float(s_r),
            "regret_db_ci95": [float(lo_r), float(hi_r)],
            "decision_agreement_mean": float(m_a),
            "max_regret_db": float(max(regrets)) if regrets else 0.0,
        })
    return out


# ============================================================================
# Step B1: dev-tune each candidate on seeds 10-19 (BATCHED: all configs in one
# channel pass). Pick the per-candidate config that MINIMISES mean regret_db on
# dev (tie -> smaller op_bit_proxy).
# ============================================================================
def dev_tune(cells, dev_seeds):
    print(f"\n=== Step B1: dev tuning (seeds {dev_seeds[0]}-{dev_seeds[-1]}, "
          f"BATCHED one channel pass per cell) ===", flush=True)
    all_configs = _all_dev_configs()
    t0 = time.time()
    dev_rows = run_batched(cells, dev_seeds, all_configs, tag="dev_all")
    dev_aggs = {a["method"]: a for a in aggregate_rows(dev_rows, list(all_configs))}
    print(f"  dev pass done ({time.time()-t0:.0f}s, {len(all_configs)} configs "
          f"batched)", flush=True)

    chosen = {}
    dev_records = {}
    # group configs by mechanism
    by_mech = {"uniform": [], "stage_widths": [], "two_exp": [],
               "boundary_adaptive": [], "narrow_acc": []}
    for name in all_configs:
        mech, cfg, rp = _res_for_name(name)
        a = dev_aggs[name]
        rec = {"name": name, "config": cfg,
               "regret_db_mean": a["regret_db_mean"],
               "decision_agreement_mean": a["decision_agreement_mean"],
               "op_bit_proxy": rp["op_bit_proxy"],
               "storage_bit_proxy": rp["storage_bit_proxy"]}
        by_mech[mech].append(rec)
        dev_records.setdefault(mech, []).append(rec)

    for mech, recs in by_mech.items():
        # sort: min regret, tie-break min op_bit_proxy
        recs.sort(key=lambda r: (round(r["regret_db_mean"], 9), r["op_bit_proxy"]))
        best = recs[0]
        chosen[mech] = best
        print(f"  -> {mech:<18} chosen: {best['name']:<28} "
              f"regret={best['regret_db_mean']:+.5f}dB "
              f"agree={best['decision_agreement_mean']*100:.2f}% "
              f"op×bit={best['op_bit_proxy']}", flush=True)
    return chosen, dev_records, dev_rows


def build_frozen_selectors(chosen):
    """From dev-chosen configs, build the frozen selector dict for held-out.

    Keys are the config-encoded NAMES (e.g. 'uniform_14_12',
    'stage_widths_8_6_12_10') so they match `chosen[mech]['name']` and the
    downstream held-out row filter works. This keeps the chosen config's
    identity parseable by `_res_for_name`.
    """
    sels = {}
    for mech, best in chosen.items():
        name = best["name"]
        cfg = best["config"]
        if mech == "uniform":
            sels[name] = _uniform_fn(cfg["W"], cfg["F"])
        elif mech == "stage_widths":
            sels[name] = _stage_widths_fn(cfg["W_cv"], cfg["F_cv"],
                                          cfg["W_s2"], cfg["F_s2"])
        elif mech == "two_exp":
            sels[name] = _two_exp_fn(cfg["W"], cfg["F"])
        elif mech == "boundary_adaptive":
            sels[name] = _boundary_fn(cfg["W_narrow"], cfg["F_narrow"],
                                      cfg["W_wide"], cfg["F_wide"])
        elif mech == "narrow_acc":
            sels[name] = _narrow_acc_fn(cfg["W"], cfg["F"], cfg.get("acc_guard", 0))
    return sels


# ============================================================================
# Step C: fresh held-out comparison + Pareto + ablation.
# ============================================================================
def analyze_heldout(heldout_rows, chosen, heldout_uniform_rows, mde_db=0.15):
    """Compute the fair-comparison analysis on held-out rows (batched)."""
    chosen_names = {mech: best["name"] for mech, best in chosen.items()}
    method_names = list(chosen_names.values())

    aggs = aggregate_rows(heldout_rows, method_names)
    # attach mechanism + resource proxy per method
    for a in aggs:
        mech, cfg, rp = _res_for_name(a["method"])
        a["mechanism"] = mech
        a["config"] = cfg
        a["op_bit_proxy"] = rp["op_bit_proxy"]
        a["storage_bit_proxy"] = rp["storage_bit_proxy"]

    # uniform comparator = the dev-chosen uniform config
    uniform_agg = next(a for a in aggs if a["mechanism"] == "uniform")

    # full uniform ladder on held-out (for ablation: uniform at every width)
    ladder_names = [f"uniform_{W}_{F}" for (W, F) in UNIFORM_SEARCH]
    ladder_aggs = aggregate_rows(heldout_uniform_rows, ladder_names)
    for a in ladder_aggs:
        _, cfg, rp = _res_for_name(a["method"])
        a["config"] = cfg
        a["op_bit_proxy"] = rp["op_bit_proxy"]
        a["storage_bit_proxy"] = rp["storage_bit_proxy"]

    # Pareto dominance among the 5 chosen methods:
    # a method is dominated if another has regret <= AND op_bit <= (one strict).
    for a in aggs:
        a["pareto_dominated"] = False
        for b in aggs:
            if b is a:
                continue
            if (b["regret_db_mean"] <= a["regret_db_mean"] + 1e-9 and
                    b["op_bit_proxy"] <= a["op_bit_proxy"] + 1e-9 and
                    (b["regret_db_mean"] < a["regret_db_mean"] - 1e-9 or
                     b["op_bit_proxy"] < a["op_bit_proxy"] - 1e-9)):
                a["pareto_dominated"] = True
                break
    pareto_front = [a["method"] for a in aggs if not a["pareto_dominated"]]

    # mixed vs uniform: does any mixed method Pareto-dominate the uniform point?
    mixed_pareto_dominates_uniform = []
    mixed_strictly_better_by_mde = []
    for x in aggs:
        if x["mechanism"] == "uniform":
            continue
        regret_le = x["regret_db_mean"] <= uniform_agg["regret_db_mean"] + 1e-9
        op_less = x["op_bit_proxy"] < uniform_agg["op_bit_proxy"] - 1
        storage_less = x["storage_bit_proxy"] < uniform_agg["storage_bit_proxy"] - 1
        resource_less = op_less or storage_less
        if regret_le and resource_less:
            mixed_pareto_dominates_uniform.append(x["method"])
        advantage = uniform_agg["regret_db_mean"] - x["regret_db_mean"]
        if advantage >= mde_db and resource_less:
            mixed_strictly_better_by_mde.append(x["method"])

    # ablation: for each mixed method, find the uniform width with the CLOSEST
    # op_bit_proxy on held-out, compare regret (controls total bit budget).
    ablation = []
    for x in aggs:
        if x["mechanism"] == "uniform":
            continue
        target = x["op_bit_proxy"]
        cands = []
        for la in ladder_aggs:
            cands.append({"method": la["method"], "config": la["config"],
                          "op_bit_proxy": la["op_bit_proxy"],
                          "regret_db": la["regret_db_mean"],
                          "proxy_diff": abs(la["op_bit_proxy"] - target)})
        cands.sort(key=lambda c: c["proxy_diff"])
        closest = cands[0] if cands else None
        ablation.append({
            "mixed_method": x["method"], "mixed_mechanism": x["mechanism"],
            "mixed_op_bit_proxy": x["op_bit_proxy"],
            "mixed_regret_db": x["regret_db_mean"],
            "uniform_closest_budget": closest,
            "mixed_minus_uniform_at_budget_db": (
                x["regret_db_mean"] - closest["regret_db"] if closest else None),
        })

    return {
        "aggregates": aggs, "pareto_front": pareto_front,
        "uniform_ladder_aggregates": ladder_aggs,
        "ablation": ablation, "mde_db": mde_db,
        "mixed_pareto_dominates_uniform": mixed_pareto_dominates_uniform,
        "mixed_strictly_better_by_mde": mixed_strictly_better_by_mde,
        "uniform_point": {
            "method": uniform_agg["method"], "config": uniform_agg["config"],
            "regret_db_mean": uniform_agg["regret_db_mean"],
            "regret_db_ci95": uniform_agg["regret_db_ci95"],
            "op_bit_proxy": uniform_agg["op_bit_proxy"],
            "storage_bit_proxy": uniform_agg["storage_bit_proxy"],
            "decision_agreement_mean": uniform_agg["decision_agreement_mean"],
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=["dev", "heldout", "both"], default="both")
    ap.add_argument("--mde", type=float, default=0.15)
    a = ap.parse_args()
    os.makedirs(OUT_DIR, exist_ok=True)

    cells = [(sc, sn) for sc in SCENES for sn in SNR_DB]
    overall_t0 = time.time()
    chosen = None
    dev_records = None
    dev_rows = None
    heldout_rows = None
    heldout_uniform_rows = None
    analysis = None

    if a.phase in ("dev", "both"):
        chosen, dev_records, dev_rows = dev_tune(cells, DEV_SEEDS_BC)

    if a.phase in ("heldout", "both"):
        sels = build_frozen_selectors(chosen)
        mde = float(a.mde)
        # held-out: run all 5 chosen methods + full uniform ladder, BATCHED into
        # one channel pass per cell (all paired, channel-identical).
        print(f"\n=== Step C: fresh held-out (seeds {HELDOUT_SEEDS[0]}-"
              f"{HELDOUT_SEEDS[-1]}, {len(cells)} cells, BATCHED) ===", flush=True)
        t0 = time.time()
        all_heldout_sels = dict(sels)
        # add the full uniform ladder. The dev-chosen uniform's config-encoded
        # name (e.g. 'uniform_14_12') is already in `sels` under that same key;
        # the ladder loop re-sets it to the identical fn (harmless redundancy).
        for (W, F) in UNIFORM_SEARCH:
            all_heldout_sels[f"uniform_{W}_{F}"] = _uniform_fn(W, F)
        heldout_all_rows = run_batched(cells, HELDOUT_SEEDS, all_heldout_sels,
                                      tag="heldout_all")
        # split: chosen methods (by config-encoded name) + uniform ladder.
        chosen_names = [v["name"] for v in chosen.values()]
        heldout_rows = [r for r in heldout_all_rows if r["method"] in chosen_names]
        heldout_uniform_rows = [r for r in heldout_all_rows
                                if r["method"].startswith("uniform_")]
        el = time.time() - t0
        print(f"  held-out done ({el:.0f}s)", flush=True)
        analysis = analyze_heldout(heldout_rows, chosen, heldout_uniform_rows,
                                   mde_db=mde)

    elapsed = time.time() - overall_t0
    out = {
        "package": "P03", "task": "T031-p03-fixed-point-resource-codesign",
        "phase": "BC_mixed_precision_and_fair_comparison",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mde_db": a.mde,
        "scenes": list(SCENES), "snr_db": list(SNR_DB),
        "dev_seeds_bc": list(DEV_SEEDS_BC), "heldout_seeds": list(HELDOUT_SEEDS),
        "seed_isolation_note": (
            "Phase A used dev seeds 0-9. Phase B dev-tuning uses seeds 10-19 "
            "(disjoint from 0-9 AND from held-out 30-49). Held-out 30-49 is "
            "P01's set; P03's estimand is a bitwidth CONFIG not a gain fit, so "
            "no leakage (brief §3.4)."),
        "resource_proxy_note": (
            "op_bit_proxy / storage_bit_proxy are deterministic operand-bit / "
            "register-bit sums. NO real synthesis / LUT / DSP / power / area."),
        "chosen_configs": chosen,
        "dev_records": dev_records,
        "heldout_aggregates": analysis["aggregates"] if analysis else None,
        "uniform_ladder_aggregates": (analysis["uniform_ladder_aggregates"]
                                      if analysis else None),
        "pareto_front": analysis["pareto_front"] if analysis else None,
        "ablation": analysis["ablation"] if analysis else None,
        "mixed_pareto_dominates_uniform": (
            analysis["mixed_pareto_dominates_uniform"] if analysis else None),
        "mixed_strictly_better_by_mde": (
            analysis["mixed_strictly_better_by_mde"] if analysis else None),
        "uniform_point": (analysis["uniform_point"] if analysis else None),
        "dev_raw_rows": dev_rows,
        "heldout_raw_rows": heldout_rows,
        "heldout_uniform_ladder_raw_rows": heldout_uniform_rows,
        "elapsed_s": float(elapsed),
    }
    op = os.path.join(OUT_DIR, "phaseBC_mixed.json")
    save_results(out, op, os.path.basename(__file__))
    if a.phase in ("dev", "both"):
        dp = os.path.join(OUT_DIR, "phaseBC_dev_tuning.json")
        save_results({"chosen": chosen, "dev_records": dev_records,
                      "dev_raw_rows": dev_rows,
                      "dev_seeds": list(DEV_SEEDS_BC)},
                     dp, os.path.basename(__file__))
    print(f"\n=== Phase BC summary ===")
    if analysis:
        print(f"  Pareto front: {analysis['pareto_front']}")
        print(f"  Mixed Pareto-dominates uniform: "
              f"{analysis['mixed_pareto_dominates_uniform']}")
        print(f"  Mixed strictly better by MDE (>= {a.mde} dB) at lower resource: "
              f"{analysis['mixed_strictly_better_by_mde']}")
        up = analysis["uniform_point"]
        print(f"  Uniform comparator: {up['config']} regret={up['regret_db_mean']:+.5f}dB "
              f"op×bit={up['op_bit_proxy']} storage={up['storage_bit_proxy']}")
        print(f"  Ablation (mixed_regret - uniform_at_same_budget):")
        for ab in analysis["ablation"]:
            cu = ab["uniform_closest_budget"]
            cstr = (f"{cu['config']} regret={cu['regret_db']:+.5f} op×bit={cu['op_bit_proxy']}"
                    if cu else "N/A")
            print(f"    {ab['mixed_method']:<28} mixed={ab['mixed_regret_db']:+.5f} "
                  f"vs uniform@budget({cstr}) -> delta={ab['mixed_minus_uniform_at_budget_db']:+.5f}dB")
    print(f"[saved] {op} ({elapsed:.0f}s)")


if __name__ == "__main__":
    main()
