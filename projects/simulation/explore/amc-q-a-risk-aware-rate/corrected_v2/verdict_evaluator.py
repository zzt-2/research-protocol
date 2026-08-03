"""Phase D + F verdict evaluator: feasibility-first constrained-goodput.

Reads probe_corrected_v2_raw.json and emits the per-cell verdict table +
terminal verdict per the brief Phase D (5 cell classes) and Phase F (primary
criteria A-E).

Cell classes (Phase D):
  1. baseline & candidate both feasible  -> compare paired goodput
  2. baseline infeasible, candidate feasible -> RELIABILITY_RECOVERY_SIGNAL
  3. baseline feasible, candidate infeasible -> candidate FAIL
  4. all deployable infeasible, oracle feasible -> action/information gap
  5. oracle also infeasible -> action-contract/operating-point unsuitable
  6. simple conventional baseline feasible & covers candidate -> PROBLEM_RESOLVED_BY_CONVENTIONAL_BASELINE
"""
from __future__ import annotations
import json
from pathlib import Path

_RAW = Path(__file__).resolve().parent.parent.parent.parent / "results" / "amc_q_a_risk_aware_rate" / "probe_corrected_v2_raw.json"
TARGET = 1e-6
METHODS = ["B0", "B1", "B2", "B3", "B4", "B5", "C1", "O1", "O2"]
ENH_BASELINES = ["B2", "B3", "B4", "B5"]


def classify_cell(c):
    feas = {m: c["results"][m]["fer_mean"] <= TARGET for m in METHODS}
    any_deploy_feas = any(feas[m] for m in ("B0","B1","B2","B3","B4","B5","C1"))
    oracle_feas = feas["O1"] or feas["O2"]
    best_enh_feas = [m for m in ENH_BASELINES if feas[m]]
    best_enh = max(best_enh_feas, key=lambda m: c["results"][m]["expected_goodput"]) if best_enh_feas else None
    c1_feas = feas["C1"]
    if not oracle_feas and not any_deploy_feas:
        return "5_ACTION_CONTRACT_OR_OPERATING_POINT_INFEASIBLE", best_enh, feas
    if not any_deploy_feas and oracle_feas:
        return "4_ACTION_OR_INFORMATION_GAP", best_enh, feas
    if best_enh and c1_feas and c["results"]["C1"]["expected_goodput"] <= c["results"][best_enh]["expected_goodput"] + 1e-9:
        # check conventional baseline covers candidate
        return "6_PROBLEM_RESOLVED_BY_CONVENTIONAL_BASELINE", best_enh, feas
    if best_enh and c1_feas:
        gp_c1 = c["results"]["C1"]["expected_goodput"]
        gp_best = c["results"][best_enh]["expected_goodput"]
        rel = (gp_c1 - gp_best) / max(gp_best, 1e-9) * 100.0
        if rel >= 5.0:
            return f"1_C1_BEATS_BASELINE_+{rel:.1f}%", best_enh, feas
        return f"1_BOTH_FEASIBLE_C1_{rel:+.1f}%_vs_{best_enh}", best_enh, feas
    if (not best_enh) and c1_feas:
        # all enhanced baselines infeasible, C1 feasible
        return "2_RELIABILITY_RECOVERY_SIGNAL", best_enh, feas
    if best_enh and (not c1_feas):
        return "3_CANDIDATE_INFEASIBLE_BASELINE_FEASIBLE", best_enh, feas
    return "UNCLASSIFIED", best_enh, feas


def main():
    d = json.load(open(_RAW))
    for contract in ("contract_A_galijasevic_original", "contract_B_symmetric_no_transmit"):
        cells = d[contract]
        print(f"\n{'='*90}\n{contract}  (FER target {TARGET})\n{'='*90}")
        from collections import Counter
        cls_counts = Counter()
        c1_beats = []
        for c in cells:
            cls, best_enh, feas = classify_cell(c)
            cls_counts[cls.split('_')[0] + '_' + '_'.join(cls.split('_')[1:])[:40]] += 1
            tag = f"a={c['alpha']} b={c['beta']} sig={c['sigma_est']} td={c['td_ratio']}"
            o1fer = c["results"]["O1"]["fer_mean"]
            c1fer = c["results"]["C1"]["fer_mean"]
            c1gp = c["results"]["C1"]["expected_goodput"]
            ben_gp = c["results"][best_enh]["expected_goodput"] if best_enh else float('nan')
            print(f"  {tag:30s} cls={cls[:48]:48s} O1fer={o1fer:.1e} C1fer={c1fer:.1e} C1gp={c1gp:.3f} bestEnh={best_enh}({ben_gp:.3f})")
        print(f"\n  class tally: {dict(cls_counts)}")
        # terminal verdict (Phase F A-E)
        n_o1_feas = sum(1 for c in cells if c["results"]["O1"]["fer_mean"] <= TARGET)
        n_c1_feas = sum(1 for c in cells if c["results"]["C1"]["fer_mean"] <= TARGET)
        n_any_feas = sum(1 for c in cells if any(c["results"][m]["fer_mean"] <= TARGET for m in METHODS))
        print(f"  O1 feasible: {n_o1_feas}/27 | C1 feasible: {n_c1_feas}/27 | any method feasible: {n_any_feas}/27")


if __name__ == "__main__":
    main()
