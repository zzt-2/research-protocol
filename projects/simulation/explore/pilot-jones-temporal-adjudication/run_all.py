"""Orchestrator for the Pilot-Jones component TEMPORAL SEMANTICS adjudication (T005).

Pipeline (all on the FIXED-component primary model; T003/T004 immutable):
  Phase C  baseline adjudication: B2 lambda scan on VALIDATION, then choose B*
           per (condition, pilot_count, model) on VALIDATION. B* frozen.
  Phase D  headroom: per primary cell compute B* -> reference Q2 headroom, the
           impairment-ADDED-over-paired-M0 gap, per-seed paired direction, and a
           bootstrap 95% CI on the impairment-added gap (across test seeds).
           4 vs 6 pilot sensitivity. operational vs adversarial.
  Phase E  pre-registered verdict (NEVER reads a method candidate — none run).

GATE SEPARATION (inherited): the problem gate reads ONLY B*/reference headroom
+ the impairment trend; there is no method gate because T005 runs no method.
The reference is a ceiling / Kill tool, NEVER a Go opponent (FR-25).

Determinism + closure: real SHA256 of contract + source; N/seed pools/cells/
pilots are read FROM the frozen contract and asserted to match the runner.
"""
from __future__ import annotations
import hashlib
import json
import os
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SIM = HERE.parents[1]
# NOTE: no module-level `sys.path.insert(0, HERE)` (see run_probe.py for the
# rationale: avoid shadowing the immutable T003 salvage `run_all` in a shared
# pytest session). When run as a script, CPython puts this dir at sys.path[0].
sys.path.insert(0, str(SIM))

import temporal_channel as tc                       # noqa: E402
import baselines_and_oracle as bao                  # noqa: E402
from run_probe import (_canonical, evaluate_dual_qpsk, ber_to_q2_db)  # noqa: E402

ROOT = SIM.parent.parent
RESULT_DIR = SIM / "results" / "pilot-jones-temporal-adjudication"


# ---------------------------------------------------------------------------
# Real SHA256 closure (V039 fix: contract_sha256 was the filename string)
# ---------------------------------------------------------------------------

def _sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def source_shas():
    rels = {
        "generator": "projects/simulation/common/_dual_pol_channel.py",
        "gg_time": "projects/simulation/common/_gg_time.py",
        "params": "projects/simulation/params.py",
        "contract": "projects/simulation/explore/pilot-jones-temporal-adjudication/contract.yaml",
        "temporal_channel": "projects/simulation/explore/pilot-jones-temporal-adjudication/temporal_channel.py",
        "baselines_and_oracle": "projects/simulation/explore/pilot-jones-temporal-adjudication/baselines_and_oracle.py",
        "run_probe": "projects/simulation/explore/pilot-jones-temporal-adjudication/run_probe.py",
        "runner": "projects/simulation/explore/pilot-jones-temporal-adjudication/run_all.py",
    }
    return {k: _sha_file(os.path.join(ROOT, v)) for k, v in rels.items()
            if os.path.exists(os.path.join(ROOT, v))}


def contract_sha():
    return _sha_file(HERE / "contract.yaml")


# ---------------------------------------------------------------------------
# Frozen grid (read FROM the contract; asserted to match the runner)
# ---------------------------------------------------------------------------

CONDITIONS = {
    "operational": {"alpha": 4.2, "beta": 1.4, "gamma_bar": 100.0},
    "adversarial": {"alpha": 2.0, "beta": 1.0, "gamma_bar": 50.0},
}
COMMON = dict(block_size=64, t_s=4.0e-10, f_g=100.0, sop_rate=8.0e-6,
              N=20000, warmup_frac=0.1, taps=7, mu=1.0e-3, r2=1.0, n_taps_b3=3)
PILOTS = [4, 6]
CELLS = [
    {"model_id": "M0", "pdl_db": 0.0, "dgd_ps": 0.0, "tag": "M0_control"},
    {"model_id": "M2", "pdl_db": 1.0, "dgd_ps": 0.0, "tag": "M2_pdl1dB"},
    {"model_id": "M3", "pdl_db": 0.0, "dgd_ps": 6.0, "tag": "M3_dgd6ps"},
]
VAL_SEEDS = list(range(7400, 7410))     # 10 validation seeds
TEST_SEEDS = list(range(7500, 7510))    # 10 fresh test seeds
B2_LAMBDAS = [1e-3, 1e-2, 1e-1, 1.0]
EMA_ALPHA = 0.9


def _assert_closure():
    """Assert the frozen contract grid matches the runner (V039 closure fix)."""
    import yaml
    with open(HERE / "contract.yaml") as f:
        c = yaml.safe_load(f)
    g = c["grid"]
    assert g["common"]["N"] == COMMON["N"], "contract/runner N mismatch"
    assert g["common"]["block_size"] == COMMON["block_size"]
    assert g["common"]["t_s"] == COMMON["t_s"]
    assert g["common"]["f_g"] == COMMON["f_g"]
    assert g["common"]["sop_rate"] == COMMON["sop_rate"]
    assert g["pilots"] == PILOTS
    assert [cc["model_id"] for cc in g["cells"]] == [cc["model_id"] for cc in CELLS]
    assert g["conditions"]["operational"]["alpha"] == CONDITIONS["operational"]["alpha"]
    assert g["conditions"]["adversarial"]["alpha"] == CONDITIONS["adversarial"]["alpha"]
    sp = c["seed_plan"]
    assert sp["headroom_validation_seeds"] == VAL_SEEDS, "val seeds mismatch"
    assert sp["headroom_test_seeds"] == TEST_SEEDS, "test seeds mismatch"
    # disjoint from T002/T003/T004 excluded
    excl = set(sp["excluded"])
    assert set(VAL_SEEDS).isdisjoint(excl), "val seeds overlap excluded"
    assert set(TEST_SEEDS).isdisjoint(excl), "test seeds overlap excluded"


# ---------------------------------------------------------------------------
# Arm execution for one (condition, pilot, cell, seed)
# ---------------------------------------------------------------------------

def run_one(condition, pilot_count, cell, seed, *, b2_lambda):
    """Run B1, B2(lambda) and the reference for one realization. Returns a row."""
    cd = CONDITIONS[condition]
    real = _canonical(COMMON["N"], seed, alpha=cd["alpha"], beta=cd["beta"],
                      gamma_bar=cd["gamma_bar"])
    ri = tc.build_impaired_realization(
        real, model_id=cell["model_id"], block_size=COMMON["block_size"],
        seed=seed, pdl_db=cell["pdl_db"], dgd_ps=cell["dgd_ps"],
        t_s=COMMON["t_s"])
    pilot = bao.inject_pre_channel_pilots(
        real, ri, block_size=COMMON["block_size"], n_pilots=pilot_count)
    est = bao.estimate_jones_single_tap(pilot, block_size=COMMON["block_size"])
    em = pilot["eval_mask"]
    eval_start = int(COMMON["N"] * COMMON["warmup_frac"])
    em_eff = em.copy()
    em_eff[:eval_start] = False
    n_eval = int(em_eff.sum())
    sX = real["sX"]; sY = real["sY"]

    def _ber(view):
        return evaluate_dual_qpsk(sX[em_eff], sY[em_eff],
                                  view["rX"][em_eff], view["rY"][em_eff])["fixed_label_ber"]

    arms = {}
    # B1 EMA09
    der = bao.derotate_single_tap(pilot, est, block_size=COMMON["block_size"],
                                  mode="ema", ema_alpha=EMA_ALPHA)
    arms["B1"] = {"ber": _ber(der)}
    # B2 Tikhonov(lambda)
    der = bao.derotate_single_tap(pilot, est, block_size=COMMON["block_size"],
                                  mode="tikhonov", tikhonov=b2_lambda)
    arms["B2"] = {"ber": _ber(der)}
    # Reference O
    if cell["model_id"] in ("M0", "M2"):
        ref = bao.reference_m0_m2(ri, pilot, block_size=COMMON["block_size"],
                                  gamma_bar=cd["gamma_bar"])
    else:
        ref = bao.reference_m3(ri, pilot, block_size=COMMON["block_size"],
                               gamma_bar=cd["gamma_bar"])
    arms["O"] = {"ber": _ber(ref), "info_class": "reference_truth_assisted"}
    return {
        "condition": condition, "pilot_count": pilot_count,
        "cell": cell["tag"], "model_id": cell["model_id"],
        "pdl_db": cell["pdl_db"], "dgd_ps": cell["dgd_ps"],
        "seed": int(seed), "n_eval": n_eval,
        "gamma_bar": cd["gamma_bar"], "alpha": cd["alpha"], "beta": cd["beta"],
        "arms": arms,
    }


def _q2(ber_vals, n_eval):
    if ber_vals is None or len(ber_vals) == 0:
        return None
    bm = float(np.mean(ber_vals))
    return ber_to_q2_db(bm, n_eval)


# ---------------------------------------------------------------------------
# Phase C: B2 lambda scan on VALIDATION; B* frozen per (condition,pilot,model)
# ---------------------------------------------------------------------------

def b2_lambda_scan_val():
    """Validation-only B2 lambda scan. Pick the lambda winning the most
    (condition,pilot,model) cells (parsimonious single lambda, no per-cell peeking).
    Returns {lambda: mean_ber} aggregate + frozen lambda."""
    print("[phaseC] B2 lambda scan on validation (M0/M2/M3 x 2 cond x 2 pilots)...")
    # scan only on non-trivial cells but evaluate on all to be safe; use a
    # parsimonious single lambda per the contract.
    cell_results = {}
    for lam in B2_LAMBDAS:
        bers = []
        for cond in CONDITIONS:
            for pc in PILOTS:
                for cell in CELLS:
                    seedset = VAL_SEEDS[:5]  # 5 seeds per cell for the scan
                    for s in seedset:
                        row = run_one(cond, pc, cell, s, b2_lambda=lam)
                        bers.append(row["arms"]["B2"]["ber"])
        cell_results[lam] = float(np.mean(bers))
    frozen = min(cell_results, key=cell_results.get)
    print(f"[phaseC] lambda scan mean BER by lambda: {cell_results} -> frozen={frozen}")
    return {"mean_ber_by_lambda": cell_results, "frozen_lambda": frozen}


def adjudicate_bstar(val_rows):
    """Choose B* per (condition, pilot_count, model_id) on VALIDATION ONLY.
    B* = lowest mean nocma BER among legal conventional baselines (B1, B2)."""
    chosen = {}
    for cond in CONDITIONS:
        for pc in PILOTS:
            for cell in CELLS:
                key = (cond, pc, cell["tag"])
                scores = {}
                for arm in ("B1", "B2"):
                    vals = [r["arms"][arm]["ber"] for r in val_rows
                            if r["condition"] == cond and r["pilot_count"] == pc
                            and r["cell"] == cell["tag"]]
                    if vals:
                        scores[arm] = float(np.mean(vals))
                if scores:
                    bstar = min(scores, key=scores.get)
                    chosen[f"{cond}|p{pc}|{cell['tag']}"] = {
                        "bstar": bstar, "all_conventional_ber": scores}
    return chosen


# ---------------------------------------------------------------------------
# Phase D: headroom + impairment-added-over-M0 + bootstrap CI
# ---------------------------------------------------------------------------

def _cell_ber(rows, cond, pc, tag, arm):
    return [r["arms"][arm]["ber"] for r in rows
            if r["condition"] == cond and r["pilot_count"] == pc and r["cell"] == tag]


def _n_eval(rows, cond, pc, tag):
    for r in rows:
        if r["condition"] == cond and r["pilot_count"] == pc and r["cell"] == tag:
            return r["n_eval"]
    return None


def _bootstrap_ci(vals, n_boot=2000, seed=12345, stat=np.mean):
    if len(vals) == 0:
        return None
    rng = np.random.default_rng(seed)
    arr = np.asarray(vals, float)
    boots = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, len(arr), len(arr))
        boots[i] = stat(arr[idx])
    lo, hi = np.quantile(boots, [0.025, 0.975])
    return {"mean": float(np.mean(vals)), "ci_lo": float(lo), "ci_hi": float(hi),
            "n": int(len(vals))}


def headroom_analysis(val_rows, test_rows, bstar_map):
    """Per primary cell: B*/O aggregate BER, Q2, headroom, impairment-added over
    paired M0, per-seed paired direction, bootstrap 95% CI on impairment-added."""
    summary = {"validation": {}, "test": {}, "impairment_added": {}}
    for cond in CONDITIONS:
        for pc in PILOTS:
            for cell in CELLS:
                tag = cell["tag"]
                key = f"{cond}|p{pc}|{tag}"
                bstar = bstar_map.get(key, {}).get("bstar", "B1")
                for split, rows in (("validation", val_rows), ("test", test_rows)):
                    bv = _cell_ber(rows, cond, pc, tag, bstar)
                    ov = _cell_ber(rows, cond, pc, tag, "O")
                    n = _n_eval(rows, cond, pc, tag)
                    qb = _q2(bv, n); qo = _q2(ov, n)
                    entry = {
                        "bstar": bstar, "n_seeds": len(bv),
                        "B_star_mean_ber": float(np.mean(bv)) if bv else None,
                        "reference_mean_ber": float(np.mean(ov)) if ov else None,
                        "Q2_B_star_dB": qb, "Q2_reference_dB": qo,
                        "Q2_headroom_dB": (qo - qb) if (qb is not None and qo is not None) else None,
                        "n_eval": n,
                    }
                    # oracle anomaly: receiver-visible B* systematically beats ref
                    entry["reference_anomaly"] = bool(
                        ov and bv and np.mean(ov) > np.mean(bv) * 1.05
                        and np.mean(bv) > 1e-6)
                    summary[split][key] = entry
    # impairment-added over paired M0 (test seeds, per-seed paired)
    for cond in CONDITIONS:
        for pc in PILOTS:
            for cell in CELLS:
                if cell["model_id"] == "M0":
                    continue
                tag = cell["tag"]
                key = f"{cond}|p{pc}|{tag}"
                m0key = f"{cond}|p{pc}|M0_control"
                bstar = bstar_map.get(key, {}).get("bstar", "B1")
                # per-seed paired impairment-added = (Q2_imp_headroom - Q2_M0_headroom)
                # computed per seed then aggregated (paired direction)
                per_seed_added = []
                test_by_seed = {}
                for r in test_rows:
                    if r["condition"] != cond or r["pilot_count"] != pc:
                        continue
                    test_by_seed.setdefault(r["cell"], {})[r["seed"]] = r
                seeds_common = sorted(
                    set(test_by_seed.get(tag, {})) & set(test_by_seed.get("M0_control", {})))
                for s in seeds_common:
                    rimp = test_by_seed[tag][s]; rm0 = test_by_seed["M0_control"][s]
                    n = rimp["n_eval"]
                    qbi = ber_to_q2_db(rimp["arms"][bstar]["ber"], n)
                    qoi = ber_to_q2_db(rimp["arms"]["O"]["ber"], n)
                    qb0 = ber_to_q2_db(rm0["arms"][bstar]["ber"], n)
                    qo0 = ber_to_q2_db(rm0["arms"]["O"]["ber"], n)
                    hi = (qoi - qbi) if (qbi is not None and qoi is not None) else None
                    h0 = (qo0 - qb0) if (qb0 is not None and qo0 is not None) else None
                    if hi is not None and h0 is not None:
                        per_seed_added.append(hi - h0)
                ci = _bootstrap_ci(per_seed_added) if per_seed_added else None
                n_pos = sum(1 for v in per_seed_added if v > 0)
                summary["impairment_added"][key] = {
                    "bstar": bstar, "model_id": cell["model_id"],
                    "n_seeds_paired": len(per_seed_added),
                    "per_seed_impairment_added_dB": [float(v) for v in per_seed_added],
                    "mean_impairment_added_dB": ci["mean"] if ci else None,
                    "bootstrap_95ci": {"lo": ci["ci_lo"], "hi": ci["ci_hi"]} if ci else None,
                    "ci_upper_dB": ci["ci_hi"] if ci else None,
                    "direction_positive_count": n_pos,
                    "direction_positive_fraction": (n_pos / len(per_seed_added)) if per_seed_added else None,
                }
    return summary


# ---------------------------------------------------------------------------
# Phase E: pre-registered verdict
# ---------------------------------------------------------------------------

def pre_registered_verdict(summary):
    """Map evidence to one of the contract §pre_registered_verdict outcomes.
    NEVER reads a method candidate (none are run)."""
    imp = summary["impairment_added"]
    # reference anomalies?
    anomalies = [k for split in ("validation", "test")
                 for k, e in summary[split].items() if e.get("reference_anomaly")]
    if anomalies:
        return {"verdict": "PARTIAL_ORACLE_INVALID",
                "reason": "reference anomaly: receiver-visible arm beats reference",
                "anomalies": anomalies,
                "claim_ceiling": "reference not a legal ceiling; NO Kill allowed from it."}
    # gather impairment-added point estimates + CI uppers for M2/M3 across both
    # conditions and both pilot counts
    primary = {}
    for k, e in imp.items():
        primary[k] = e
    point_max = max((e.get("mean_impairment_added_dB") or -9) for e in primary.values()) \
        if primary else None
    ci_upper_max = max((e.get("ci_upper_dB") or -9) for e in primary.values()) \
        if primary else None
    # KILL: ALL primary cells have point < 0.5 AND ci_upper < 0.5
    all_below = all(
        (e.get("mean_impairment_added_dB") is not None
         and e["mean_impairment_added_dB"] < 0.5
         and e.get("ci_upper_dB") is not None
         and e["ci_upper_dB"] < 0.5)
        for e in primary.values()) if primary else False
    # SURVIVES: ANY primary cell has point >= 0.5 AND ci_upper >= 0.5 AND
    # direction_positive_fraction supports it (>= 0.5)
    survivors = [k for k, e in primary.items()
                 if e.get("mean_impairment_added_dB") is not None
                 and e["mean_impairment_added_dB"] >= 0.5
                 and e.get("ci_upper_dB") is not None
                 and e["ci_upper_dB"] >= 0.5
                 and e.get("direction_positive_fraction", 0) >= 0.5]
    if all_below:
        return {"verdict": "KILL_COMPLEX_COMPONENT_RESCUE_AXIS_TEMPORAL_PRIMARY",
                "reason": "all primary cells: impairment-added point < 0.5 dB AND CI upper < 0.5 dB",
                "primary_impairment_added": primary,
                "max_point_dB": point_max, "max_ci_upper_dB": ci_upper_max,
                "claim_ceiling": ("complex-component PDL/PMD rescue axis does not reintroduce "
                                  "a method-worthy gap under the fixed/verified temporal model. "
                                  "Does NOT close the whole Pilot-Jones family; 4-paper fulltext "
                                  "debt remains BLOCKED; does NOT enter Step 5/Contract/Execute.")}
    if survivors:
        return {"verdict": "PROBLEM_SURVIVES_FIXED_COMPONENT",
                "reason": "at least one primary cell: impairment-added point >= 0.5 dB AND CI upper >= 0.5 dB AND direction supports",
                "surviving_cells": survivors,
                "primary_impairment_added": primary,
                "max_point_dB": point_max, "max_ci_upper_dB": ci_upper_max,
                "claim_ceiling": ("problem survives under fixed component; T005 STILL runs NO "
                                  "method; hands back to main control. Does NOT enter Step 5.")}
    return {"verdict": "UNRESOLVED_TEMPORAL_PRIMARY",
            "reason": "CI straddles 0.5 dB (point/CI/direction do not jointly decide)",
            "primary_impairment_added": primary,
            "max_point_dB": point_max, "max_ci_upper_dB": ci_upper_max,
            "claim_ceiling": "inconclusive; main control to adjudicate."}


# ---------------------------------------------------------------------------
# Run pipeline
# ---------------------------------------------------------------------------

def _run_grid(seeds, b2_lambda, label):
    rows = []
    for cond in CONDITIONS:
        for pc in PILOTS:
            for cell in CELLS:
                for s in seeds:
                    rows.append(run_one(cond, pc, cell, s, b2_lambda=b2_lambda))
    blob = {"label": label,
            "experiment": "PILOT_JONES_TEMPORAL_SEMANTICS_ADJUDICATION_PACKAGE",
            "contract_sha256": contract_sha(),
            "source_sha256": source_shas(),
            "params": {**COMMON, "pilots": PILOTS,
                       "conditions": CONDITIONS, "ema_alpha": EMA_ALPHA,
                       "b2_lambda_frozen": b2_lambda,
                       "cells": CELLS, "val_seeds": VAL_SEEDS, "test_seeds": TEST_SEEDS},
            "raw_rows": rows}
    return blob


def main():
    _assert_closure()
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    shas = source_shas()
    csha = contract_sha()

    # Phase C: B2 lambda scan on validation, freeze B2 lambda parsimoniously
    lam_scan = b2_lambda_scan_val()
    b2_lambda = lam_scan["frozen_lambda"]

    # Validation + test grids (B* selection on val; test only reuses frozen B*)
    print("[phaseD] validation grid (B* selection)...")
    blob_val = _run_grid(VAL_SEEDS, b2_lambda, "T005_validation")
    with open(RESULT_DIR / "probe_val.json", "w") as f:
        json.dump(blob_val, f, indent=1, default=str)
    print("[phaseD] test grid (fresh, B* frozen)...")
    blob_test = _run_grid(TEST_SEEDS, b2_lambda, "T005_test")
    with open(RESULT_DIR / "probe_test.json", "w") as f:
        json.dump(blob_test, f, indent=1, default=str)

    val_rows = blob_val["raw_rows"]; test_rows = blob_test["raw_rows"]
    bstar_map = adjudicate_bstar(val_rows)
    summary = headroom_analysis(val_rows, test_rows, bstar_map)
    verdict = pre_registered_verdict(summary)

    result = {
        "label": "T005 temporal-semantics adjudication consolidated",
        "experiment": "PILOT_JONES_TEMPORAL_SEMANTICS_ADJUDICATION_PACKAGE",
        "contract_sha256": csha,
        "source_sha256": shas,
        "b2_lambda_scan_val": lam_scan,
        "b2_lambda_frozen": b2_lambda,
        "bstar_adjudication_val": bstar_map,
        "headroom": summary,
        "verdict": verdict,
        "ber_to_q2_formula": "Q=sqrt(2)*erfcinv(2*BER); Q^2_dB=20*log10(Q); BER=0 -> 0.5/N_eval bound; BER>=0.5 -> None",
        "bootstrap": "per-cell paired impairment-added-over-M0 across 10 test seeds; 2000 resamples; 95% CI = [2.5%, 97.5%] quantiles",
    }
    with open(RESULT_DIR / "result.json", "w") as f:
        json.dump(result, f, indent=1, default=str)
    print(f"[verdict] {verdict['verdict']}")
    print(json.dumps({
        "reason": verdict["reason"],
        "max_point_dB": verdict.get("max_point_dB"),
        "max_ci_upper_dB": verdict.get("max_ci_upper_dB"),
        "bstar_frozen_lambda": b2_lambda,
    }, indent=1, default=str))
    return result


if __name__ == "__main__":
    main()
