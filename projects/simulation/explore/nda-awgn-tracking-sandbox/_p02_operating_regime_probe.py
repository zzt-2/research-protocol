# -*- coding: utf-8 -*-
"""P02 (T029) — cand_rank operating-regime confirmation.

Mirrors _p01_phaseBC.py::run/main but evaluates ONLY the operating-regime cells
frozen in T029 §1:
  - Primary target = {weak} x {5,7,9} dB  (3 cells)
  - Boundary/control = {weak@11} U {moderate@5,7,9}  (4 cells)
  total = 7 cells.

Methods (frozen identities, T029 §2):
  - adapter_pilot : conventional pilot-SNR adapter (decide_adapter_pilot)
  - cand_rank     : candidate (decide_cand_rank, ref_snr_db=9.0 FIXED)
  - weakretune    : cheap alternative (decide_adapter_weakretune, ref dev-frozen)
  - oracle_true   : true-gamma upper bound ONLY (excluded from adjudication)

Seeds (T029 §4, disjoint from all prior use):
  - dev (cheap-alt tuning)       = seed_index 50..59
  - fresh held-out test          = seed_index {60..70} U {81..89} = 30 seeds
                                   (EXCLUDE polluted 71..80)

DELTAS: run full (-3..3) for audit/sanity (channel shared, cheap), but the primary
estimand uses delta=0 rows (adapter/cand_rank/weakretune are delta-invariant in
their internal estimates -> delta=0 is the mismatch-free control).

Discipline:
  - TRUE gamma enters ONLY signal generation + offline oracle BER + oracle_true
    upper bound. Every other decide is receiver-visible only (audit per call site).
  - Shared channel: one generation per (scene, gamma_true, seed) via
    generate_shared_realization_apsk (TL-13); all selectors see identical windows.
  - New file only; no edits to common/, params.py, frozen selectors, or P01 files.
"""
import os
import sys
import json
import time
import argparse
from datetime import datetime, timezone

import numpy as np
from scipy import stats

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
sys.path[:0] = [_SIM_ROOT, os.path.join(_SIM_ROOT, 'simulator'), _HERE]

import _p01_cpr_snr_mismatch_probe as PR  # noqa: E402  (frozen multidelta runner)
import _p01_adapter_and_candidates as AD  # noqa: E402  (frozen adapter + cand_rank)
from _p01_adapter_and_candidates import CANDIDATES  # noqa: E402
import _a4_switch_common768_30seed as A  # noqa: E402  (frozen inherited selector)
import _p02_weakretune_adapter as WR  # noqa: E402  (cheap alternative, Step A)

# wire pilot hooks so pilot-based selectors work in the multidelta loop
PR.wire_pilot_hooks(AD.set_window_pilots, AD.reset_hysteresis)

# ---- frozen cell grid (T029 §1) ----
TARGET_CELLS = [("weak", 5.0), ("weak", 7.0), ("weak", 9.0)]
BOUNDARY_CELLS = [("weak", 11.0), ("moderate", 5.0), ("moderate", 7.0), ("moderate", 9.0)]
ALL_CELLS = TARGET_CELLS + BOUNDARY_CELLS   # 7 cells

DELTAS = PR.DELTAS   # (-3..3); full sweep for audit, primary uses delta=0
MDE = 0.15           # frozen (T029 §4); do NOT lower
OUT_DIR = os.path.join(_SIM_ROOT, "results", "p02_cand_rank_operating_regime")

DEV_SEEDS = list(range(50, 60))                              # 10 seeds, dev tuning
# Held-out set: T029 line 82 specified {60..70} U {81..89} = 20 seeds, but the brief
# requires >=30 paired seeds/cell. In-package deterministic fix (controller-authorized):
# extend with seeds 90..99 (disjoint from all frozen ranges). Final = 30 seeds.
HELDOUT_SEEDS_ORIG = list(range(60, 71)) + list(range(81, 90))   # 20 seeds (original)
HELDOUT_SEEDS_EXTEND = list(range(90, 100))                      # 10 seeds added (fix)
HELDOUT_SEEDS = HELDOUT_SEEDS_ORIG + HELDOUT_SEEDS_EXTEND        # 30 seeds (final)
DEV_REFS = [7.0, 8.0, 9.0, 10.0, 11.0]                       # frozen dev search space

# Frozen exclusion ranges (T029 §4) — every held-out/dev seed MUST be disjoint from these.
FROZEN_EXCLUSIONS = {
    "anchor_0_29": set(range(0, 30)),
    "p01_dev_0_9": set(range(0, 10)),          # subset of anchor
    "p01_heldout_30_49": set(range(30, 50)),
    "dev_50_59": set(range(50, 60)),
    "pollution_71_80": set(range(71, 81)),
}


def verify_seed_disjointness(seeds, label="seeds"):
    """Raise if any seed collides with a frozen exclusion range. Returns the checked set."""
    s = set(int(x) for x in seeds)
    collisions = {}
    for name, excl in FROZEN_EXCLUSIONS.items():
        inter = s & excl
        if inter:
            collisions[name] = sorted(inter)
    if collisions:
        raise AssertionError(
            f"{label} collide with frozen exclusion ranges: {collisions}")
    # also check internal uniqueness
    if len(s) != len(seeds):
        raise AssertionError(f"{label} contain duplicates: {len(seeds)} given, {len(s)} unique")
    return s


def ci_t(data):
    """Paired Student-t 95% CI (matches P01 _p01_phaseBC.ci_t / anchor provenance)."""
    a = np.asarray(data, dtype=float)
    n = len(a)
    mean = float(np.mean(a))
    std = float(np.std(a, ddof=1)) if n > 1 else 0.0
    hw = float(stats.t.ppf(0.975, n - 1)) * std / np.sqrt(n) if n > 1 else 0.0
    return mean, std, hw, mean - hw, mean + hw


def _oracle_decide_factory(gamma_true_db):
    """TRUE-gamma selector (UPPER BOUND only; excluded from adjudication)."""
    g_lin = 10.0 ** (gamma_true_db / 10.0)
    def _f(raw, gamma_hat_db, gamma_hat_lin, b):
        return A.decide(raw, gamma_true_db, g_lin)
    return _f


def build_selector_specs(methods, cell_snr):
    """Per-cell selector specs dict for the multidelta runner.

    weakretune uses the CURRENT module-global ref (caller freezes it before running).
    oracle_true needs the cell's true gamma; all others come from the frozen registry.
    """
    specs = {}
    for m in methods:
        if m == "oracle_true":
            specs[m] = {"fn": _oracle_decide_factory(cell_snr),
                        "needs_pilot": False, "needs_reset": False}
        elif m == "weakretune":
            fn, npf, nrf = WR.decide_adapter_weakretune_fn()
            specs[m] = {"fn": fn, "needs_pilot": npf, "needs_reset": nrf}
        else:
            fn, npf, nrf = CANDIDATES[m]
            specs[m] = {"fn": fn, "needs_pilot": npf, "needs_reset": nrf}
    return specs


def run(cells, seeds, methods, tag):
    """Run the scan; return (raw_rows, aggregates).

    raw_rows: per (scene,gamma,delta,seed,method) selected_errors / branch counts /
              fixed_nda_errors_common768 / gain_db.
    aggregates: per (scene,gamma,delta,method) mean/std/CI over seeds of gain_db.
    """
    t0 = time.time()
    raw_rows = []
    for ci, (scene, snr) in enumerate(cells):
        specs_template = build_selector_specs(methods, snr)
        for seed in seeds:
            md = PR.run_case_multidelta(scene, snr, seed, deltas=DELTAS,
                                        extra_selector=specs_template)
            base = md["base"]
            nda_c = base["fixed_nda_errors"]
            for delta in DELTAS:
                # original selector (audit; not in adjudication)
                po = md["per_delta_orig"][delta]
                raw_rows.append({
                    "tag": tag, "scene": scene, "gamma_true_db": float(snr),
                    "delta_db": float(delta), "seed_index": int(seed), "method": "orig",
                    "selected_errors": int(po["selected_errors"]),
                    "n_select_da": int(po["n_select_da"]),
                    "n_select_nda": int(po["n_select_nda"]),
                    "fixed_nda_errors_common768": int(nda_c),
                    "gain_db": float(10 * np.log10(nda_c / po["selected_errors"])
                                     if po["selected_errors"] > 0 else float("inf")),
                })
                for m, permap in md.get("per_delta_extra", {}).items():
                    pe = permap[delta]
                    raw_rows.append({
                        "tag": tag, "scene": scene, "gamma_true_db": float(snr),
                        "delta_db": float(delta), "seed_index": int(seed), "method": m,
                        "selected_errors": int(pe["selected_errors"]),
                        "n_select_da": int(pe["n_select_da"]),
                        "n_select_nda": int(pe["n_select_nda"]),
                        "fixed_nda_errors_common768": int(nda_c),
                        "gain_db": float(10 * np.log10(nda_c / pe["selected_errors"])
                                         if pe["selected_errors"] > 0 else float("inf")),
                    })
        el = time.time() - t0
        print(f"  [{tag}] {scene}@{snr:.0f}dB done ({ci+1}/{len(cells)} cells, "
              f"{el:.0f}s)", flush=True)

    # ---- aggregates per (scene, gamma, delta, method) over seeds ----
    aggregates = compute_aggregates(raw_rows, cells, tag=tag)
    return raw_rows, aggregates


def compute_aggregates(raw_rows, cells, tag="heldout"):
    """Per (scene, gamma, delta, method) mean/std/CI over seeds of gain_db.

    Extracted from run() so the extend/merge phase can recompute aggregates over
    the merged raw_rows without re-running the channel.
    """
    aggregates = []
    methods_seen = sorted(set(r["method"] for r in raw_rows))
    for scene, snr in cells:
        for delta in DELTAS:
            for m in methods_seen:
                sub = [r for r in raw_rows
                       if r["scene"] == scene
                       and abs(r["gamma_true_db"] - snr) < 1e-9
                       and abs(r["delta_db"] - delta) < 1e-9
                       and r["method"] == m]
                if not sub:
                    continue
                gains = [r["gain_db"] for r in sub]
                mean, std, hw, lo, hi = ci_t(gains)
                aggregates.append({
                    "tag": tag, "scene": scene, "gamma_true_db": float(snr),
                    "delta_db": float(delta), "method": m,
                    "n_seeds": len(sub), "gain_db_mean": mean, "gain_db_std": std,
                    "gain_db_ci95": [lo, hi],
                })
    return aggregates


# ----------------------------------------------------------------------
# Paired diff helpers (delta=0 rows; cand_rank / adapter / weakretune are
# delta-invariant in their internal estimates, so delta=0 is the canonical
# mismatch-free control).
# ----------------------------------------------------------------------
def _gain_by_cell_seed(raw_rows, method, cells, delta=0.0):
    """Map (scene, gamma, seed_index) -> gain_db for `method` at the given delta."""
    out = {}
    for r in raw_rows:
        if (r["method"] == method and abs(r["delta_db"] - delta) < 1e-9):
            out[(r["scene"], r["gamma_true_db"], r["seed_index"])] = r["gain_db"]
    return out


def paired_diff(raw_rows, method_a, method_b, cells, delta=0.0):
    """Return list of per-seed paired diffs (a - b) pooled over the given cells.

    Only seeds present for BOTH methods at every cell are paired (seed-cluster paired).
    Returns (diffs, per_cell_diffs dict).
    """
    ga = _gain_by_cell_seed(raw_rows, method_a, cells, delta=delta)
    gb = _gain_by_cell_seed(raw_rows, method_b, cells, delta=delta)
    # seeds present for both at every cell
    common_seeds_per_cell = []
    per_cell_diffs = {}
    for (scene, snr) in cells:
        ds = []
        seeds_cell = sorted({s for (sc, g, s) in ga.keys()
                             if sc == scene and abs(g - snr) < 1e-9}
                            & {s for (sc, g, s) in gb.keys()
                               if sc == scene and abs(g - snr) < 1e-9})
        for s in seeds_cell:
            d = ga[(scene, snr, s)] - gb[(scene, snr, s)]
            ds.append(d)
        per_cell_diffs[(scene, snr)] = ds
        common_seeds_per_cell.append(ds)
    diffs = [d for cell_ds in common_seeds_per_cell for d in cell_ds]
    return diffs, per_cell_diffs


def summarize_diff(diffs):
    """Return (n, mean, std, ci_lo, ci_hi, n_help, n_hurt, n_tie)."""
    n = len(diffs)
    if n == 0:
        return 0, float("nan"), float("nan"), float("nan"), float("nan"), 0, 0, 0
    mean, std, hw, lo, hi = ci_t(diffs)
    arr = np.asarray(diffs, dtype=float)
    n_help = int(np.sum(arr > 1e-9))
    n_hurt = int(np.sum(arr < -1e-9))
    n_tie = int(np.sum(np.abs(arr) <= 1e-9))
    return n, mean, std, lo, hi, n_help, n_hurt, n_tie


# ======================================================================
# Step C — dev tuning of the cheap alternative (seeds 50-59, target cells)
# ======================================================================
def run_dev_tuning(methods_for_dev):
    """For ref in DEV_REFS: freeze, run dev on TARGET cells, compute mean paired
    (weakretune - adapter) over the 3 target cells x 10 dev seeds. Pick the ref
    maximizing it (tie -> smallest ref). Return full dev record + chosen ref.

    methods_for_dev: must include adapter_pilot + weakretune (+ cand_rank for audit).
    """
    print(f"=== Step C: dev tuning (seeds {DEV_SEEDS[0]}-{DEV_SEEDS[-1]}, "
          f"refs={DEV_REFS}, target cells only) ===", flush=True)
    ref_records = []
    chosen_ref = None
    chosen_mean = None
    for ref in DEV_REFS:
        WR.freeze_ref("weakretune", ref)
        t0 = time.time()
        raw_rows, _ = run(TARGET_CELLS, DEV_SEEDS, methods_for_dev, tag=f"dev_ref{ref:g}")
        el = time.time() - t0
        diffs, per_cell = paired_diff(raw_rows, "weakretune", "adapter_pilot",
                                      TARGET_CELLS, delta=0.0)
        n, mean, std, lo, hi, nh, nu, nt = summarize_diff(diffs)
        # cand_rank - adapter at this dev run, for audit (cand_rank is ref-invariant)
        d_crank, _ = paired_diff(raw_rows, "cand_rank", "adapter_pilot",
                                 TARGET_CELLS, delta=0.0)
        _, crank_mean, _, _, _, _, _, _ = summarize_diff(d_crank)
        rec = {
            "ref_snr_db": float(ref),
            "weakretune_minus_adapter_mean_db": float(mean),
            "weakretune_minus_adapter_ci95": [float(lo), float(hi)],
            "weakretune_minus_adapter_n": int(n),
            "cand_rank_minus_adapter_mean_db_audit": float(crank_mean),
            "elapsed_s": float(el),
        }
        ref_records.append(rec)
        print(f"  ref={ref:>4.1f}: weakretune-adapter mean={mean:+.4f} "
              f"CI=[{lo:+.4f},{hi:+.4f}] n={n}  (cand_rank-adapter audit={crank_mean:+.4f}) "
              f"[{el:.0f}s]", flush=True)
    # selection rule (frozen): maximize mean; tie -> smallest ref
    best = None
    for rec in ref_records:
        m = rec["weakretune_minus_adapter_mean_db"]
        if (best is None or m > best["weakretune_minus_adapter_mean_db"] + 1e-12):
            best = rec
    chosen_ref = best["ref_snr_db"]
    chosen_mean = best["weakretune_minus_adapter_mean_db"]
    print(f"  -> chosen ref={chosen_ref} (mean={chosen_mean:+.4f})", flush=True)
    return {
        "dev_seeds": list(DEV_SEEDS),
        "dev_cells": [list(c) for c in TARGET_CELLS],
        "search_refs": list(DEV_REFS),
        "selection_rule": "maximize mean paired (weakretune-adapter) over 3 target cells x dev seeds; tie -> smallest ref",
        "ref_records": ref_records,
        "chosen_ref_snr_db": float(chosen_ref),
        "chosen_weakretune_minus_adapter_mean_db": float(chosen_mean),
    }


# ======================================================================
# Step D — fresh held-out confirmation (seeds 60-70 + 81-89, all 7 cells)
# ======================================================================
def analyze_heldout(raw_rows):
    """Compute all Step D estimands from held-out raw rows.

    Returns a dict of analysis blocks (primary, per_target_cell, single_cell_dominance,
    cheap_alt_adjudication, boundary).
    """
    out = {}

    # ---- D1: primary — target-region (cand_rank - adapter) over 3 cells x 30 seeds
    diffs, per_cell = paired_diff(raw_rows, "cand_rank", "adapter_pilot",
                                  TARGET_CELLS, delta=0.0)
    n, mean, std, lo, hi, nh, nu, nt = summarize_diff(diffs)
    out["primary_cand_rank_minus_adapter"] = {
        "estimand": "target-region paired (cand_rank - adapter) mean over 3 target cells x held-out seeds",
        "n_paired": n, "mean_db": mean, "std_db": std, "ci95": [lo, hi],
        "n_help": nh, "n_hurt": nu, "n_tie": nt,
        "mean_ge_mde": bool(mean >= MDE), "ci_low_gt_0": bool(lo > 0),
    }

    # ---- D2: per target cell cand_rank - adapter
    per_cell_records = []
    for (scene, snr), ds in per_cell.items():
        n, mean, std, lo, hi, nh, nu, nt = summarize_diff(ds)
        per_cell_records.append({
            "scene": scene, "gamma_true_db": snr, "n_paired": n,
            "mean_db": mean, "std_db": std, "ci95": [lo, hi],
            "n_help": nh, "n_hurt": nu, "n_tie": nt,
            "positive_ci_low_gt_0": bool(lo > 0),
        })
    out["per_target_cell_cand_rank_minus_adapter"] = per_cell_records

    # ---- D3: single-cell-dominance — drop best cell, recompute over remaining 2
    cell_means = {f"{r['scene']}@{r['gamma_true_db']:g}": r["mean_db"]
                  for r in per_cell_records}
    best_cell = max(cell_means, key=cell_means.get)
    remaining_cells = [c for c in TARGET_CELLS
                       if f"{c[0]}@{c[1]:g}" != best_cell]
    diffs_rem, _ = paired_diff(raw_rows, "cand_rank", "adapter_pilot",
                               remaining_cells, delta=0.0)
    n, mean_rem, std, lo, hi, nh, nu, nt = summarize_diff(diffs_rem)
    out["single_cell_dominance"] = {
        "best_cell_dropped": best_cell,
        "best_cell_mean_db": cell_means[best_cell],
        "remaining_cells": [list(c) for c in remaining_cells],
        "remaining_n_paired": n, "remaining_mean_db": mean_rem,
        "remaining_ci95": [lo, hi],
        "no_single_cell_dominance": bool(mean_rem > 0),
    }

    # ---- D4: cheap-alt adjudication — (weakretune - adapter) & (cand_rank - weakretune)
    d_wr_adp, _ = paired_diff(raw_rows, "weakretune", "adapter_pilot",
                              TARGET_CELLS, delta=0.0)
    n1, m1, s1, lo1, hi1, _, _, _ = summarize_diff(d_wr_adp)
    out["cheap_alt_weakretune_minus_adapter"] = {
        "estimand": "target-region paired (weakretune - adapter)",
        "n_paired": n1, "mean_db": m1, "std_db": s1, "ci95": [lo1, hi1],
    }
    d_cr_wr, _ = paired_diff(raw_rows, "cand_rank", "weakretune",
                             TARGET_CELLS, delta=0.0)
    n2, m2, s2, lo2, hi2, _, _, _ = summarize_diff(d_cr_wr)
    out["cheap_alt_cand_rank_minus_weakretune"] = {
        "estimand": "target-region paired (cand_rank - weakretune)",
        "n_paired": n2, "mean_db": m2, "std_db": s2, "ci95": [lo2, hi2],
        "abs_mean_le_mde": bool(abs(m2) <= MDE),
    }

    # ---- D5: boundary cells cand_rank - adapter; flag catastrophic
    boundary_records = []
    any_catastrophic = False
    for cell in BOUNDARY_CELLS:
        d_b, _ = paired_diff(raw_rows, "cand_rank", "adapter_pilot", [cell], delta=0.0)
        n, mean, std, lo, hi, nh, nu, nt = summarize_diff(d_b)
        catastrophic = bool(mean < -0.5 and hi < 0)
        any_catastrophic = any_catastrophic or catastrophic
        boundary_records.append({
            "scene": cell[0], "gamma_true_db": cell[1], "n_paired": n,
            "mean_db": mean, "std_db": std, "ci95": [lo, hi],
            "catastrophic": catastrophic,
        })
    out["boundary_cand_rank_minus_adapter"] = boundary_records
    out["boundary_any_catastrophic"] = bool(any_catastrophic)

    return out


# ======================================================================
# Step E — frozen adjudication order (T029 §5)
# ======================================================================
def adjudicate(analysis):
    """Apply the frozen adjudication order exactly. Returns (verdict, reasoning)."""
    primary = analysis["primary_cand_rank_minus_adapter"]
    per_cell = analysis["per_target_cell_cand_rank_minus_adapter"]
    scd = analysis["single_cell_dominance"]
    wr_adp = analysis["cheap_alt_weakretune_minus_adapter"]
    cr_wr = analysis["cheap_alt_cand_rank_minus_weakretune"]
    boundary = analysis["boundary_cand_rank_minus_adapter"]
    any_cat = analysis["boundary_any_catastrophic"]

    crank_mean = primary["mean_db"]
    wr_mean = wr_adp["mean_db"]

    steps = []

    # Step 1: cheap-alt reaches cand_rank?
    # condition: |cand_rank - weakretune| <= MDE  AND  weakretune-adapter >= cand_rank-adapter - MDE
    s1_close = cr_wr["abs_mean_le_mde"]
    s1_reaches = bool(wr_mean >= crank_mean - MDE)
    s1_resolved = bool(s1_close and s1_reaches)
    steps.append({
        "step": 1,
        "name": "cheap_alt_reaches_cand_rank",
        "abs_cand_rank_minus_weakretune_le_mde": s1_close,
        "weakretune_minus_adapter_ge_cand_rank_minus_adapter_minus_mde": s1_reaches,
        "resolved": s1_resolved,
    })
    if s1_resolved:
        return ("PROBLEM_RESOLVED_BY_REGION_RETUNING", steps,
                "Step 1 triggered: |cand_rank-weakretune|<=MDE and "
                "weakretune-adapter >= cand_rank-adapter - MDE. A cheap region-retune "
                "of the SAME conventional lever captures cand_rank's gain -> cand_rank "
                "is not a distinct diagnostic method.")

    # Step 2: cand_rank target-region confirmation (ALL must hold)
    cells_pos_ci = sum(1 for r in per_cell if r["positive_ci_low_gt_0"])
    n_target = len(per_cell)
    ge2of3 = bool(cells_pos_ci >= 2)  # 2/3 of 3 cells
    no_scd = scd["no_single_cell_dominance"]
    no_boundary_cat = not any_cat
    mean_ok = primary["mean_ge_mde"]
    ci_low_ok = primary["ci_low_gt_0"]
    steps.append({
        "step": 2,
        "name": "cand_rank_target_confirmation",
        "mean_ge_mde": mean_ok,
        "ci_low_gt_0": ci_low_ok,
        "cells_with_positive_ci_low": cells_pos_ci,
        "n_target_cells": n_target,
        "ge_2of3_cells_positive_ci_low": ge2of3,
        "no_single_cell_dominance": no_scd,
        "no_boundary_catastrophic": no_boundary_cat,
        "all_hold": bool(mean_ok and ci_low_ok and ge2of3 and no_scd and no_boundary_cat),
    })
    if (mean_ok and ci_low_ok and ge2of3 and no_scd and no_boundary_cat):
        return ("BOUNDED_DIAGNOSTIC_METHOD_SIGNAL", steps,
                "Step 2 all conditions hold: mean>=MDE, CI_low>0, >=2/3 target cells "
                "positive(CI_low>0), no single-cell dominance, no boundary catastrophic.")

    # Step 3/4: else NO_CONFIRMATION
    failed = [k for k, v in [("mean>=MDE", mean_ok), ("CI_low>0", ci_low_ok),
                             (">=2/3 cells pos CI_low", ge2of3),
                             ("no single-cell dominance", no_scd),
                             ("no boundary catastrophic", no_boundary_cat)]
              if not v]
    return ("NO_CONFIRMATION", steps,
            f"Step 2 failed on: {failed}. cand_rank target-region signal not confirmed "
            f"on fresh held-out seeds.")


# ======================================================================
# main
# ======================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=["dev", "heldout", "extend", "both"],
                    default="both")
    ap.add_argument("--methods", nargs="+",
                    default=["adapter_pilot", "cand_rank", "weakretune", "oracle_true"])
    a = ap.parse_args()
    os.makedirs(OUT_DIR, exist_ok=True)

    overall_t0 = time.time()
    dev_record = None
    heldout_analysis = None
    heldout_raw_rows = None
    heldout_aggregates = None
    verdict = None
    verdict_steps = None
    verdict_reasoning = None

    if a.phase in ("dev", "both"):
        dev_record = run_dev_tuning(a.methods)
        # FREEZE the chosen ref for the held-out run (never touch dev again)
        WR.freeze_ref("weakretune", dev_record["chosen_ref_snr_db"])
        with open(os.path.join(OUT_DIR, "dev_tuning.json"), "w") as f:
            json.dump(dev_record, f, indent=2)
        print(f"[saved] {os.path.join(OUT_DIR, 'dev_tuning.json')}", flush=True)

    if a.phase in ("heldout", "both"):
        # verify held-out seed set disjoint from ALL frozen exclusion ranges
        verify_seed_disjointness(HELDOUT_SEEDS, "HELDOUT_SEEDS")
        verify_seed_disjointness(DEV_SEEDS, "DEV_SEEDS")
        if dev_record is not None:
            WR.freeze_ref("weakretune", dev_record["chosen_ref_snr_db"])
        else:
            # if heldout-only, read the frozen ref from dev_tuning.json
            dp = os.path.join(OUT_DIR, "dev_tuning.json")
            if os.path.exists(dp):
                with open(dp) as f:
                    dev_record = json.load(f)
                WR.freeze_ref("weakretune", dev_record["chosen_ref_snr_db"])
                print(f"[loaded] frozen weakretune ref={dev_record['chosen_ref_snr_db']} "
                      f"from dev_tuning.json", flush=True)
            else:
                raise RuntimeError("heldout phase needs dev_tuning.json; run --phase dev first.")
        print(f"\n=== Step D: fresh held-out (seeds {HELDOUT_SEEDS} = "
              f"{len(HELDOUT_SEEDS)} seeds, 7 cells, frozen weakretune ref="
              f"{WR.get_ref()}) ===", flush=True)
        t0 = time.time()
        heldout_raw_rows, heldout_aggregates = run(ALL_CELLS, HELDOUT_SEEDS,
                                                   a.methods, tag="heldout")
        el = time.time() - t0
        print(f"  held-out run done in {el:.0f}s", flush=True)
        heldout_analysis = analyze_heldout(heldout_raw_rows)
        verdict, verdict_steps, verdict_reasoning = adjudicate(heldout_analysis)
        print(f"\n=== Step E: recommended verdict = {verdict} ===", flush=True)
        print(f"  reasoning: {verdict_reasoning}", flush=True)

    if a.phase == "extend":
        # In-package deterministic fix (controller-authorized): extend held-out to 30
        # seeds by adding seeds 90..99 (disjoint from all frozen ranges + the 20 already
        # run). Merge raw_rows, recompute aggregates+analysis+adjudication over the full
        # 30-seed set. NO change to dev tuning, weakretune ref, cells, methods, or criteria.
        verify_seed_disjointness(HELDOUT_SEEDS_EXTEND, "HELDOUT_SEEDS_EXTEND")
        # frozen weakretune ref from dev (never re-tuned)
        dp = os.path.join(OUT_DIR, "dev_tuning.json")
        with open(dp) as f:
            dev_record = json.load(f)
        WR.freeze_ref("weakretune", dev_record["chosen_ref_snr_db"])
        print(f"[loaded] frozen weakretune ref={dev_record['chosen_ref_snr_db']} "
              f"from dev_tuning.json (unchanged)", flush=True)
        # load the existing 20-seed raw_rows
        hp = os.path.join(OUT_DIR, "heldout_confirmation.json")
        with open(hp) as f:
            prev = json.load(f)
        existing_rows = prev.get("raw_rows") or []
        existing_seeds = sorted(set(r["seed_index"] for r in existing_rows))
        print(f"\n=== Step D-ext: extend held-out by seeds {HELDOUT_SEEDS_EXTEND} "
              f"(existing={len(existing_seeds)} seeds, adding {len(HELDOUT_SEEDS_EXTEND)}, "
              f"frozen weakretune ref={WR.get_ref()}) ===", flush=True)
        # sanity: the new seeds must be disjoint from existing AND from exclusions
        new_set = set(HELDOUT_SEEDS_EXTEND)
        if new_set & set(existing_seeds):
            raise AssertionError("extend seeds collide with existing held-out seeds")
        t0 = time.time()
        new_rows, _ = run(ALL_CELLS, HELDOUT_SEEDS_EXTEND, a.methods, tag="heldout_ext")
        el = time.time() - t0
        print(f"  extend run ({len(HELDOUT_SEEDS_EXTEND)} seeds x {len(ALL_CELLS)} cells) "
              f"done in {el:.0f}s", flush=True)
        # MERGE raw_rows (dedupe by full key to be safe) and recompute
        merged_rows = existing_rows + new_rows
        seen_keys = set()
        deduped = []
        for r in merged_rows:
            k = (r["scene"], r["gamma_true_db"], r["delta_db"], r["seed_index"], r["method"])
            if k in seen_keys:
                continue
            seen_keys.add(k)
            deduped.append(r)
        merged_rows = deduped
        heldout_raw_rows = merged_rows
        heldout_aggregates = compute_aggregates(heldout_raw_rows, ALL_CELLS, tag="heldout")
        heldout_analysis = analyze_heldout(heldout_raw_rows)
        verdict, verdict_steps, verdict_reasoning = adjudicate(heldout_analysis)
        print(f"\n=== Step E (30-seed): recommended verdict = {verdict} ===", flush=True)
        print(f"  reasoning: {verdict_reasoning}", flush=True)

    elapsed = time.time() - overall_t0

    # ---- assemble held-out artifact ----
    seeds_in_rows = sorted(set(r["seed_index"] for r in heldout_raw_rows)) if heldout_raw_rows else []
    out = {
        "package": "P02",
        "task": "T029-p02-cand-rank-operating-regime-confirmation",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mde_db": MDE,
        "cells": {
            "target": [list(c) for c in TARGET_CELLS],
            "boundary": [list(c) for c in BOUNDARY_CELLS],
            "all": [list(c) for c in ALL_CELLS],
        },
        "deltas_run": list(DELTAS),
        "primary_delta": 0.0,
        "methods": list(a.methods),
        "dev_seeds": list(DEV_SEEDS),
        "heldout_seeds": seeds_in_rows,
        "heldout_seed_count": len(seeds_in_rows),
        "frozen_weakretune_ref_snr_db": float(WR.get_ref()),
        "analysis": heldout_analysis,
        "recommended_verdict": verdict,
        "adjudication_steps": verdict_steps,
        "verdict_reasoning": verdict_reasoning,
        "elapsed_s": float(elapsed),
        "raw_rows": heldout_raw_rows,
        "aggregates": heldout_aggregates,
        "meta": {
            "verdict": verdict,
            "verdict_step_triggered": (
                verdict_steps[-1]["step"] if verdict_steps else None),
            "verdict_reasoning": verdict_reasoning,
            "frozen_mde_db": MDE,
            "frozen_weakretune_ref_snr_db": float(WR.get_ref()),
            "primary_mean_db": (heldout_analysis["primary_cand_rank_minus_adapter"]["mean_db"]
                                if heldout_analysis else None),
            "primary_ci95": (heldout_analysis["primary_cand_rank_minus_adapter"]["ci95"]
                             if heldout_analysis else None),
            "primary_n_paired": (heldout_analysis["primary_cand_rank_minus_adapter"]["n_paired"]
                                 if heldout_analysis else None),
            "primary_n_help_hurt_tie": (
                [heldout_analysis["primary_cand_rank_minus_adapter"]["n_help"],
                 heldout_analysis["primary_cand_rank_minus_adapter"]["n_hurt"],
                 heldout_analysis["primary_cand_rank_minus_adapter"]["n_tie"]]
                if heldout_analysis else None),
            "discipline_notes": [
                "TRUE gamma enters ONLY signal generation + offline oracle BER + oracle_true upper bound.",
                "oracle_true is excluded from every adjudication step (upper bound only).",
                "Shared channel generate_shared_realization_apsk (TL-13); one generation per (scene,gamma,seed).",
                "adapter_pilot / cand_rank / weakretune are delta-invariant in their internal estimates; delta=0 is the mismatch-free control (primary estimand).",
                "weakretune ref frozen on dev seeds 50-59; held-out seeds never touched dev.",
            ],
        },
    }
    if a.phase == "extend":
        out["meta"]["seed_consolidation"] = {
            "fix_type": "in-package deterministic fix (controller-authorized)",
            "reason": ("T029 line 82 specified {60..70} U {81..89} = 20 seeds, but the brief "
                       "requires >=30 paired seeds/cell. The set [60,89]\\[71,80] yields only "
                       "20 disjoint seeds, so 10 additional seeds (90..99) were added."),
            "original_20_seeds": HELDOUT_SEEDS_ORIG,
            "added_10_seeds": HELDOUT_SEEDS_EXTEND,
            "final_30_seeds": HELDOUT_SEEDS,
            "added_seeds_verified_disjoint_from": list(FROZEN_EXCLUSIONS.keys())
                + ["the original 20 held-out seeds"],
            "criteria_unchanged": ("dev tuning, weakretune ref (frozen at 11.0 from dev seeds "
                                   "50-59), cells, methods, MDE=0.15, and the §5 adjudication "
                                   "order were ALL left unchanged; only the held-out seed set "
                                   "was extended."),
        }
    hp = os.path.join(OUT_DIR, "heldout_confirmation.json")
    with open(hp, "w") as f:
        json.dump(out, f, indent=2)
    print(f"[saved] {hp}", flush=True)
    print(f"[total elapsed] {elapsed:.0f}s", flush=True)


if __name__ == "__main__":
    main()
