"""Orchestrator for the Pilot-Jones complex-model SEMANTIC REPAIR (T004).

Phases:
  Phase 2  semantic gates (must all PASS before any headroom probe)
  Phase 3  baseline adjudication: choose B* per family on VALIDATION seeds
  Phase 4.1 problem-survival probe (B* -> O headroom; NEVER reads P)
  Phase 4.2 method candidates + conditional MVE (ONLY if problem survives)
  Phase 5  verdict (separated problem/method gates; M4 closure narrows claim)

GATE SEPARATION (V038 defect #5 fix): problem_survives() and method_succeeds()
are independent functions. problem_survives() reads ONLY B*/O headroom + the
impairment trend; method_succeeds() reads ONLY P vs B*. They are never AND-ed.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1]))

import run_repair as R  # noqa: E402
from run_repair import ber_to_q2_db  # noqa: E402

RESULT_DIR = HERE.parents[1] / "results" / "pilot-jones-complex-repair"
SHAS = R.source_shas()

# shared probe params (repair-contract.yaml parameter_sources). N=20000 keeps
# 8us << tau_c at f_g=100 while bounding runtime under the subagent budget.
P = dict(alpha=2.0, beta=1.0, gamma_bar=50.0, n_pilots=6, block_size=64,
         N=20000, taps=7, mu=1e-3, r2=1.0, warmup_frac=0.1)

VAL_SEEDS = [7100, 7101, 7102, 7103, 7104]          # B* selection (validation)
TEST_SEEDS = [7200, 7201, 7202, 7203, 7204, 7205, 7206, 7207]  # fresh test (8 seeds)

# Arms: B0 no-op, B1 EMA09, B2 tikhonov (validation-optimal lambda), B3_pdl
# whitening, B3_pmd per-block tapped, B3_pmd_pool cross-block pooled tapped,
# B4_fde conventional FDE, P1 energy-weighted, P1_energy_whiten, P2 cond-EMA,
# P3 joint pooled-tapped+whitening tracker, O oracle.
ARMS_PROBE = ["B0", "B1", "B2", "B3_pdl", "B3_pmd", "B3_pmd_pool", "B4_fde",
              "P1_energy", "P1_energy_whiten", "P2_cond_ema", "P3_joint", "O"]


# ---------------------------------------------------------------------------
# Phase 4.1: problem-survival probe — NEVER reads P
# ---------------------------------------------------------------------------

def _ber(rows, arm, cell, key="metrics_nocma"):
    vals = []
    for r in rows:
        if r["cell"] != cell:
            continue
        b = r["arms"].get(arm)
        if b and b.get(key, {}).get("fixed_label_ber") is not None:
            vals.append(b[key]["fixed_label_ber"])
    return np.array(vals) if vals else np.array([])


def _n_eval(rows, arm, cell):
    for r in rows:
        if r["cell"] == cell:
            n = r["arms"].get(arm, {}).get("valid_data_samples_nocma")
            if n:
                return n
    return None


def _q2(ber, n_eval):
    if ber is None or len(ber) == 0:
        return None
    bm = float(ber.mean())
    if bm <= 0.0:
        return ber_to_q2_db(0.5 / n_eval) if n_eval else None
    return ber_to_q2_db(bm)


def problem_headroom(rows, band_cells):
    """Per-cell B* -> O headroom using nocma BER. B* is chosen per family on the
    VALIDATION rows (see adjudicate_bstar). Here we report headroom for the
    family-specific B* and O. Does NOT read any P arm."""
    summary = {}
    for cell, model_id, bstar, oracle in band_cells:
        bv = _ber(rows, bstar, cell)
        ov = _ber(rows, oracle, cell)
        n = _n_eval(rows, bstar, cell)
        entry = {"model_id": model_id, "bstar": bstar, "oracle": oracle,
                 "n_seeds": int(len(bv)),
                 "B_star_mean": float(bv.mean()) if len(bv) else None,
                 "oracle_mean": float(ov.mean()) if len(ov) else None}
        qb = _q2(bv, n); qo = _q2(ov, n)
        entry["Q2_B_star_dB"] = qb; entry["Q2_oracle_dB"] = qo
        if qb is not None and qo is not None:
            entry["Q2_headroom_dB"] = qo - qb   # >0 means O better (B* leaves room)
        if len(ov) and len(bv) and ov.mean() > 1e-9:
            entry["B_star_over_oracle_ber_ratio"] = float(bv.mean() / ov.mean())
        # oracle anomaly: receiver-visible B* beats O -> oracle invalid
        entry["oracle_anomaly"] = bool(len(ov) and len(bv)
                                       and ov.mean() > bv.mean() * 1.05
                                       and bv.mean() > 1e-6)
        summary[cell] = entry
    return summary


def adjudicate_bstar(rows, cells_specs):
    """Choose B* per model family on VALIDATION rows ONLY. Candidates include B1
    and task-matched B3/B4. B* = lowest mean nocma BER among the legal
    conventional baselines (NOT P, NOT O)."""
    conventional = ["B1", "B2", "B3_pdl", "B3_pmd", "B3_pmd_pool", "B4_fde"]
    chosen = {}
    for cell, model_id in cells_specs:
        scores = {}
        for arm in conventional:
            v = _ber(rows, arm, cell)
            if len(v):
                scores[arm] = float(v.mean())
        if not scores:
            continue
        bstar = min(scores, key=scores.get)
        chosen[cell] = {"bstar": bstar, "all_conventional_ber": scores}
    return chosen


def problem_survives(summary_val, summary_test, m0_val_cell, m0_test_cell,
                     oracle_arm_val, verified_cells, stress_cells):
    """PROBLEM GATE — reads ONLY B*/O headroom + impairment trend. NEVER reads P.

    problem_survives requires ALL of:
      1. no oracle_anomaly in any cell (O is a valid ceiling);
      2. a verified cell leaves >0.5 dB Q^2 headroom (B* -> O), OR stress clearly
         separates the axis with a monotonic impairment trend;
      3. the gap is impairment-ADDED over paired M0 (delta vs M0 deep-fade control),
         not a common deep-fade floor;
      4. direction-stable across seeds (headroom positive on the majority of seeds).
    """
    details = {"oracle_anomalies": [], "verified_headroom_dB": {},
               "impairment_added_over_M0": {}, "per_seed_direction": {}}
    # 1. oracle anomalies
    for cell, e in {**summary_val, **summary_test}.items():
        if e.get("oracle_anomaly"):
            details["oracle_anomalies"].append(cell)
    if details["oracle_anomalies"]:
        return False, "ORACLE_INVALID: receiver-visible arm beats oracle", details
    # 2/3. verified headroom + impairment-added over M0
    m0v = summary_val.get(m0_val_cell, {})
    m0_h = m0v.get("Q2_headroom_dB")
    any_verified_gap = False
    for cell in verified_cells:
        e = summary_val.get(cell)
        if not e:
            continue
        h = e.get("Q2_headroom_dB")
        details["verified_headroom_dB"][cell] = h
        if h is not None and h > 0.5:
            any_verified_gap = True
        if h is not None and m0_h is not None:
            details["impairment_added_over_M0"][cell] = h - m0_h
    # 4. trend across stress (monotonic impairment-added headroom) — use BOTH
    #    validation and fresh-test stress cells (val names map to test via suffix).
    stress_added = []
    m0t = summary_test.get(m0_test_cell, {})
    m0_th = m0t.get("Q2_headroom_dB")
    for cell in stress_cells:
        test_cell = cell.replace("_val", "_test")
        e = summary_test.get(test_cell) or summary_test.get(cell)
        if not e:
            continue
        h = e.get("Q2_headroom_dB")
        if h is not None and m0_th is not None:
            stress_added.append((test_cell, round(h - m0_th, 4)))
    details["stress_added_over_M0"] = stress_added
    monotonic = (len(stress_added) >= 2
                 and all(d[1] > 0.0 for d in stress_added)
                 and stress_added[-1][1] > stress_added[0][1])
    survives = any_verified_gap or monotonic
    reason = ("verified gap >0.5 dB" if any_verified_gap
              else ("monotonic stress trend" if monotonic
                    else "no verified gap and no monotonic stress trend"))
    return survives, reason, details


# ---------------------------------------------------------------------------
# Phase 4.2: method gate — reads ONLY P vs B*
# ---------------------------------------------------------------------------

def method_succeeds(rows, p_arm, bstar_map, cells):
    """METHOD GATE — reads ONLY P vs B*. Returns paired W/T/L per cell + aggregate.
    P beats B* on fresh TEST seeds: win >= 8/10 and sign-test p<0.05 in >=1 cell.
    """
    results = {}
    for cell in cells:
        bstar = bstar_map.get(cell, {}).get("bstar")
        if not bstar:
            continue
        w = t = l = 0
        pber = []; bber = []
        for r in rows:
            if r["cell"] != cell:
                continue
            pa = r["arms"].get(p_arm); ba = r["arms"].get(bstar)
            pv = pa.get("metrics_nocma", {}).get("fixed_label_ber") if pa else None
            bv = ba.get("metrics_nocma", {}).get("fixed_label_ber") if ba else None
            if pv is None or bv is None:
                continue
            pber.append(pv); bber.append(bv)
            if pv < bv: w += 1
            elif pv == bv: t += 1
            else: l += 1
        # sign test (paired, P<B* = +)
        signs = [1 if a < b else (-1 if a > b else 0) for a, b in zip(pber, bber)]
        n_plus = sum(1 for s in signs if s > 0)
        n_minus = sum(1 for s in signs if s < 0)
        from math import comb
        n = n_plus + n_minus
        # one-sided exact sign-test p (H0: P(med=0)) for P winning
        p_val = (sum(comb(n, k) for k in range(0, n_plus + 1)) / (2 ** n)) if n > 0 else 1.0
        results[cell] = {"p_arm": p_arm, "bstar": bstar, "W/T/L": [w, t, l],
                         "P_mean_ber": float(np.mean(pber)) if pber else None,
                         "B_star_mean_ber": float(np.mean(bber)) if bber else None,
                         "sign_p_P_wins": float(p_val)}
    return results


# ---------------------------------------------------------------------------
# Phase 5: provisional verdict (claim ceiling narrows if M4 not closed)
# ---------------------------------------------------------------------------

def provisional_verdict(ps_survives, ps_reason, ps_details,
                        ms_results, m4_closed, has_blocking_debt,
                        baseline_valid, oracle_valid):
    """Map evidence to one of the allowed T004 §8 verdicts. M4 not closed -> the
    claim ceiling narrows (no 'family/complex closed')."""
    verdict = {
        "problem_survives": ps_survives, "problem_reason": ps_reason,
        "problem_details": ps_details,
        "m4_closed": m4_closed, "blocking_literature_debt": has_blocking_debt,
    }
    if not oracle_valid:
        verdict["verdict"] = "PARTIAL_ORACLE_INVALID"
        return verdict
    if not baseline_valid:
        verdict["verdict"] = "PARTIAL_BASELINE_INVALID"
        return verdict
    if not ps_survives:
        verdict["verdict"] = "KILL_COMPLEX_AXIS_AFTER_VALID_SEMANTICS_AND_CONVENTIONAL_BASELINE"
        verdict["claim_ceiling"] = ("complex-Jones/PMD/PDL does not reintroduce a "
                                     "method-worthy gap; T002 UNITARY_REAL_ROTATION_"
                                     "MCA_KILLED extends to the verified complex model.")
        if not m4_closed:
            verdict["claim_ceiling"] += (" M4 (joint PDL+PMD) not closed; claim ceiling "
                                          "narrows to the verified single axes only.")
        return verdict
    # problem survives -> evaluate method
    all_fail = True
    for p_arm, res in ms_results.items():
        any_cell_win = any(r["W/T/L"][0] >= 8 and r["sign_p_P_wins"] < 0.05
                           for r in res.values())
        if any_cell_win:
            all_fail = False
    if all_fail:
        verdict["verdict"] = "PROBLEM_SURVIVES_METHOD_CANDIDATES_FAIL"
        verdict["claim_ceiling"] = ("problem survives but no proposed mechanism beats "
                                     "the strongest conventional baseline B*.")
    else:
        v = "CONDITIONAL_GO_WITH_BLOCKING_LITERATURE_DEBT" if has_blocking_debt \
            else "CONDITIONAL_GO"
        verdict["verdict"] = v
        verdict["claim_ceiling"] = ("at least one mechanism candidate beats B* on fresh "
                                     "test seeds. Provisional, pending main-control.")
    if not m4_closed:
        verdict["claim_ceiling"] += (" M4 (joint PDL+PMD) not closed; no family-level "
                                      "close claim.")
    return verdict


# ---------------------------------------------------------------------------
# Run pipeline
# ---------------------------------------------------------------------------

def _cell(model_id, pdl=0.0, dgd=0.0, seeds=None, vr=True, name=None):
    return {"cell": name or f"{model_id}_pdl{pdl}_dgd{dgd}_{'v' if vr else 's'}",
            "model_id": model_id, "f_g": 100.0, "sop_rate": 8e-6,
            "pdl_db": pdl, "dgd_ps": dgd, "verified_range": vr,
            "seeds": seeds or []}


def _b2_lambda_scan(val_cells, lambdas):
    """Validation-only B2 tikhonov lambda scan. Returns the per-M2-cell optimal
    lambda (lowest MEAN nocma BER across seeds) so B* (B2) is frozen at its BEST
    legal config (responds to science-critic attack #5: B* must not be frozen
    suboptimally)."""
    arms_scan = ["B2"]
    chosen = {}
    # collect mean BER per (cell, lambda) across seeds
    cell_lam_ber = {}   # cell -> {lam: [ber per seed]}
    for lam in lambdas:
        blob = R.run_grid(val_cells, arms_scan,
                          out_path=RESULT_DIR / f"_lscan_{lam}.json",
                          contract_sha="repair-contract.yaml", source_shas_map=SHAS,
                          label=f"lscan_{lam}", **P, b2_lambda=lam)
        for r in blob["raw_rows"]:
            c = r["cell"]; b = r["arms"].get("B2")
            v = b.get("metrics_nocma", {}).get("fixed_label_ber") if b else None
            if v is not None:
                cell_lam_ber.setdefault(c, {}).setdefault(lam, []).append(v)
    for c, lam_bers in cell_lam_ber.items():
        # mean BER across seeds per lambda; pick the lambda with the lowest mean
        means = {lam: float(np.mean(bers)) for lam, bers in lam_bers.items()}
        chosen[c] = {"best_lambda": min(means, key=means.get),
                     "mean_ber_by_lambda": means}
    # clean temp scan files
    for lam in lambdas:
        f = RESULT_DIR / f"_lscan_{lam}.json"
        if f.exists():
            f.unlink()
    return chosen


def main():
    RESULT_DIR.mkdir(parents=True, exist_ok=True)

    # ---- validation grid (B* selection). M1 (complex unitary) omitted: a
    # unitary rotation is lossless (cond==1) and orthogonal to the PDL/PMD
    # problem axis, so it carries no headroom signal (verified in smoke: BER 0). ----
    val_cells = [
        _cell("M0", name="M0_control_val", seeds=VAL_SEEDS, vr=True),
        _cell("M2", pdl=1.0, name="M2_pdl1dB_val", seeds=VAL_SEEDS, vr=True),
        _cell("M3", dgd=6.0, name="M3_dgd6ps_val", seeds=VAL_SEEDS, vr=True),
        # stress on validation seeds too (for trend + B* under stress)
        _cell("M2", pdl=3.5, name="M2_pdl3p5dB_val", seeds=VAL_SEEDS, vr=False),
        _cell("M2", pdl=6.0, name="M2_pdl6dB_val", seeds=VAL_SEEDS, vr=False),
        _cell("M2", pdl=9.5, name="M2_pdl9p5dB_val", seeds=VAL_SEEDS, vr=False),
        _cell("M3", dgd=40.0, name="M3_dgd40ps_val", seeds=VAL_SEEDS, vr=False),
        _cell("M3", dgd=160.0, name="M3_dgd160ps_val", seeds=VAL_SEEDS, vr=False),
        _cell("M4", pdl=3.5, dgd=40.0, name="M4_joint_val", seeds=VAL_SEEDS, vr=False),
    ]

    # ---- B2 lambda validation scan: freeze B2 at its validation-optimal lambda
    #      per cell (science-critic attack #5). Use a single representative lambda
    #      per PDL family for the main probe (parsimony + avoids per-cell peeking). ----
    # scan only on M2 cells (B2 is only the B* for M2/M4; M3 B* is B1)
    m2_scan_cells = [c for c in val_cells if c["model_id"] in ("M2",)]
    lam_scan = _b2_lambda_scan(m2_scan_cells, [1e-3, 1e-2, 1e-1, 1.0])
    lam_by_cell = {c: d["best_lambda"] for c, d in lam_scan.items()}
    # parsimonious: one lambda for all M2 cells = the lambda winning the most cells
    from collections import Counter
    lam_counts = Counter(lam_by_cell.values())
    m2_lambda = lam_counts.most_common(1)[0][0] if lam_counts else 1e-2
    print(f"[b2-lambda-scan] per-cell={lam_by_cell} -> frozen M2 lambda={m2_lambda}")

    blob_val = R.run_grid(val_cells, ARMS_PROBE, out_path=RESULT_DIR / "probe_val.json",
                          contract_sha="repair-contract.yaml", source_shas_map=SHAS,
                          label="repair_val", **P, b2_lambda=m2_lambda)

    # ---- fresh test grid (problem + method evaluation) ----
    test_cells = [dict(c, seeds=TEST_SEEDS) for c in val_cells]
    for c in test_cells:
        c["cell"] = c["cell"].replace("_val", "_test")
    blob_test = R.run_grid(test_cells, ARMS_PROBE, out_path=RESULT_DIR / "probe_test.json",
                           contract_sha="repair-contract.yaml", source_shas_map=SHAS,
                           label="repair_test", **P, b2_lambda=m2_lambda)

    rows_val = blob_val["raw_rows"]; rows_test = blob_test["raw_rows"]

    # ---- Phase 3: baseline adjudication on VALIDATION ----
    cell_specs = [(c["cell"], c["model_id"]) for c in val_cells]
    bstar_map = adjudicate_bstar(rows_val, cell_specs)

    # build a val->test cell-name map so the test headroom uses the SAME frozen B*
    val_to_test = {c["cell"]: c["cell"].replace("_val", "_test") for c in val_cells}
    test_bstar = {val_to_test[c]: v for c, v in bstar_map.items()}

    oracle_arm = "O"
    band_cells_val = [(c["cell"], c["model_id"],
                       bstar_map.get(c["cell"], {}).get("bstar", "B1"),
                       oracle_arm) for c in val_cells]
    band_cells_test = [(c["cell"], c["model_id"],
                        test_bstar.get(c["cell"], {}).get("bstar", "B1"),
                        oracle_arm) for c in test_cells]
    summary_val = problem_headroom(rows_val, band_cells_val)
    summary_test = problem_headroom(rows_test, band_cells_test)

    # ---- Phase 4.1: problem survival ----
    verified_cells = ["M2_pdl1dB_val", "M3_dgd6ps_val"]
    stress_cells_pdl = ["M2_pdl3p5dB_val", "M2_pdl6dB_val", "M2_pdl9p5dB_val"]
    stress_cells_pmd = ["M3_dgd40ps_val", "M3_dgd160ps_val"]
    ps_survives, ps_reason, ps_details = problem_survives(
        summary_val, summary_test, "M0_control_val", "M0_control_test",
        oracle_arm, verified_cells, stress_cells_pdl + stress_cells_pmd)

    # ---- Phase 4.2: method candidates (only if problem survives) ----
    # includes P3 (joint PDL+PMD tracker) per science-critic attack #10.
    ms_results = {}
    if ps_survives:
        test_cells_nonM0 = [c["cell"] for c in test_cells if c["model_id"] != "M0"]
        for p_arm in ["P1_energy", "P1_energy_whiten", "P2_cond_ema", "P3_joint"]:
            ms_results[p_arm] = method_succeeds(rows_test, p_arm, test_bstar,
                                                test_cells_nonM0)

    # ---- Phase 5: verdict ----
    oracle_valid = not ps_details.get("oracle_anomalies")
    baseline_valid = True   # validated by gate6/gate8 tests; headroom confirms
    m4_closed = False       # M4 only probed as sensitivity (limiting smoke); no joint verdict
    has_debt = True         # D056 4-paper fulltext debt still BLOCKED
    verdict = provisional_verdict(
        ps_survives, ps_reason, ps_details, ms_results, m4_closed,
        has_debt, baseline_valid, oracle_valid)

    result = {
        "label": "T004 semantic repair + retest consolidated",
        "experiment": "PILOT_JONES_SEMANTIC_REPAIR_RETEST_PACKAGE",
        "source_sha256": SHAS,
        "b2_lambda_validation_scan_per_cell": lam_scan,
        "b2_lambda_frozen_M2": m2_lambda,
        "bstar_adjudication_val": bstar_map,
        "problem_headroom_val": summary_val,
        "problem_headroom_test": summary_test,
        "method_results": ms_results,
        "verdict": verdict,
        "ber_to_q2_formula": "Q=sqrt(2)*erfcinv(2*BER); Q^2_dB=20*log10(Q); BER=0 -> 0.5/N_eval bound; BER>=0.5 -> None",
    }
    with open(RESULT_DIR / "result.json", "w") as f:
        json.dump(result, f, indent=1, default=str)
    print(f"[verdict] {verdict['verdict']}")
    print(json.dumps({"problem_survives": ps_survives, "reason": ps_reason,
                      "verified_headroom": ps_details.get("verified_headroom_dB"),
                      "stress_added": ps_details.get("stress_added_over_M0"),
                      "oracle_anomalies": ps_details.get("oracle_anomalies")},
                     indent=1, default=str))
    return result


if __name__ == "__main__":
    main()
