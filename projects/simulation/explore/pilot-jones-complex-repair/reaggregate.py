"""Recompute the T004 result.json aggregation from existing raw probe files
(probe_val.json, probe_test.json) WITHOUT re-running the simulation. Used after
fixing the stress-trend + test-lookup bugs so the verdict reflects the corrected
aggregation on the already-generated raw data.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
RESULT_DIR = HERE.parents[1] / "results" / "pilot-jones-complex-repair"


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
    from scipy.special import erfcinv
    from math import log10
    bm = float(ber.mean())
    if bm <= 0.0:
        return 20.0 * log10((2.0 ** 0.5) * erfcinv(2.0 * (0.5 / n_eval))) if n_eval else None
    if bm >= 0.5:
        return None
    q = (2.0 ** 0.5) * erfcinv(2.0 * bm)
    return 20.0 * log10(q) if q > 0 else None


def adjudicate_bstar(rows, cells):
    conventional = ["B1", "B2", "B3_pdl", "B3_pmd", "B3_pmd_pool", "B4_fde"]
    chosen = {}
    for cell in cells:
        scores = {}
        for arm in conventional:
            v = _ber(rows, arm, cell)
            if len(v):
                scores[arm] = float(v.mean())
        if scores:
            chosen[cell] = {"bstar": min(scores, key=scores.get),
                            "all_conventional_ber": scores}
    return chosen


def problem_headroom(rows, band_cells):
    summary = {}
    for cell, model_id, bstar, oracle in band_cells:
        bv = _ber(rows, bstar, cell); ov = _ber(rows, oracle, cell)
        n = _n_eval(rows, bstar, cell)
        e = {"model_id": model_id, "bstar": bstar, "oracle": oracle,
             "n_seeds": int(len(bv)),
             "B_star_mean": float(bv.mean()) if len(bv) else None,
             "oracle_mean": float(ov.mean()) if len(ov) else None}
        qb = _q2(bv, n); qo = _q2(ov, n)
        e["Q2_B_star_dB"] = qb; e["Q2_oracle_dB"] = qo
        if qb is not None and qo is not None:
            e["Q2_headroom_dB"] = qo - qb
        if len(ov) and len(bv) and ov.mean() > 1e-9:
            e["B_star_over_oracle_ber_ratio"] = float(bv.mean() / ov.mean())
        e["oracle_anomaly"] = bool(len(ov) and len(bv)
                                   and ov.mean() > bv.mean() * 1.05
                                   and bv.mean() > 1e-6)
        summary[cell] = e
    return summary


def main():
    v = json.load(open(RESULT_DIR / "probe_val.json"))
    t = json.load(open(RESULT_DIR / "probe_test.json"))
    rv, rt = v["raw_rows"], t["raw_rows"]
    val_cells = sorted(set(r["cell"] for r in rv))
    test_cells = sorted(set(r["cell"] for r in rt))
    mid = {r["cell"]: r["model_id"] for r in rv}

    bstar_map = adjudicate_bstar(rv, val_cells)
    test_bstar = {c.replace("_val", "_test"): bstar_map[c]
                  for c in val_cells if c in bstar_map}

    band_val = [(c, mid[c], bstar_map.get(c, {}).get("bstar", "B1"), "O") for c in val_cells]
    band_test = [(c, mid.get(c.replace("_test", "_val"), "M0"),
                  test_bstar.get(c, {}).get("bstar", "B1"), "O") for c in test_cells]
    sv = problem_headroom(rv, band_val)
    st = problem_headroom(rt, band_test)

    # problem survival
    oracle_anom = [c for c, e in {**sv, **st}.items() if e.get("oracle_anomaly")]
    verified_cells = ["M2_pdl1dB_val", "M3_dgd6ps_val"]
    m0v = sv.get("M0_control_val", {}); m0_h = m0v.get("Q2_headroom_dB")
    verified_headroom = {}; impairment_added = {}
    any_verified_gap = False
    for c in verified_cells:
        e = sv.get(c)
        if not e:
            continue
        h = e.get("Q2_headroom_dB"); verified_headroom[c] = h
        if h is not None and h > 0.5:
            any_verified_gap = True
        if h is not None and m0_h is not None:
            impairment_added[c] = h - m0_h
    stress_cells = ["M2_pdl3p5dB_val", "M2_pdl6dB_val", "M2_pdl9p5dB_val",
                    "M3_dgd40ps_val", "M3_dgd160ps_val"]
    m0t = st.get("M0_control_test", {}); m0_th = m0t.get("Q2_headroom_dB")
    stress_added = []
    for c in stress_cells:
        tc = c.replace("_val", "_test")
        e = st.get(tc) or sv.get(c)
        if not e:
            continue
        h = e.get("Q2_headroom_dB")
        if h is not None and m0_th is not None:
            stress_added.append((tc, round(h - m0_th, 4)))
    monotonic = (len(stress_added) >= 2 and all(d[1] > 0 for d in stress_added)
                 and stress_added[-1][1] > stress_added[0][1])
    ps_survives = (not oracle_anom) and (any_verified_gap or monotonic)
    ps_reason = ("ORACLE_INVALID" if oracle_anom
                 else ("verified gap >0.5 dB" if any_verified_gap
                       else ("monotonic stress trend" if monotonic
                             else "no verified gap and no monotonic trend")))
    ps_details = {"oracle_anomalies": oracle_anom,
                  "verified_headroom_dB": verified_headroom,
                  "impairment_added_over_M0": impairment_added,
                  "stress_added_over_M0": stress_added}

    # method candidates
    ms = {}
    if ps_survives:
        nonM0 = [c for c in test_cells if mid.get(c.replace("_test", "_val")) != "M0"]
        for p_arm in ["P1_energy", "P1_energy_whiten", "P2_cond_ema", "P3_joint"]:
            res = {}
            for c in nonM0:
                bstar = test_bstar.get(c, {}).get("bstar")
                if not bstar:
                    continue
                w = ti = l = 0; pber = []; bber = []
                for r in rt:
                    if r["cell"] != c:
                        continue
                    pa = r["arms"].get(p_arm); ba = r["arms"].get(bstar)
                    pv = pa.get("metrics_nocma", {}).get("fixed_label_ber") if pa else None
                    bv = ba.get("metrics_nocma", {}).get("fixed_label_ber") if ba else None
                    if pv is None or bv is None:
                        continue
                    pber.append(pv); bber.append(bv)
                    if pv < bv: w += 1
                    elif pv == bv: ti += 1
                    else: l += 1
                from math import comb
                signs = [1 if a < b else (-1 if a > b else 0) for a, b in zip(pber, bber)]
                n_plus = sum(1 for s in signs if s > 0)
                n_minus = sum(1 for s in signs if s < 0)
                n = n_plus + n_minus
                p_val = (sum(comb(n, k) for k in range(0, n_plus + 1)) / (2 ** n)) if n > 0 else 1.0
                res[c] = {"p_arm": p_arm, "bstar": bstar, "W/T/L": [w, ti, l],
                          "P_mean_ber": float(np.mean(pber)) if pber else None,
                          "B_star_mean_ber": float(np.mean(bber)) if bber else None,
                          "sign_p_P_wins": float(p_val)}
            ms[p_arm] = res

    # verdict
    oracle_valid = not oracle_anom
    baseline_valid = True
    m4_closed = False
    has_debt = True
    all_fail = True
    for p_arm, res in ms.items():
        if any(r["W/T/L"][0] >= 8 and r["sign_p_P_wins"] < 0.05 for r in res.values()):
            all_fail = False
    if not oracle_valid:
        verdict_name = "PARTIAL_ORACLE_INVALID"
    elif not baseline_valid:
        verdict_name = "PARTIAL_BASELINE_INVALID"
    elif not ps_survives:
        verdict_name = "KILL_COMPLEX_AXIS_AFTER_VALID_SEMANTICS_AND_CONVENTIONAL_BASELINE"
    elif all_fail:
        verdict_name = "PROBLEM_SURVIVES_METHOD_CANDIDATES_FAIL"
    else:
        verdict_name = ("CONDITIONAL_GO_WITH_BLOCKING_LITERATURE_DEBT" if has_debt
                        else "CONDITIONAL_GO")
    verdict = {"verdict": verdict_name, "problem_survives": ps_survives,
               "problem_reason": ps_reason, "problem_details": ps_details,
               "m4_closed": m4_closed, "blocking_literature_debt": has_debt,
               "claim_ceiling": _claim_ceiling(verdict_name, m4_closed)}

    result = {
        "label": "T004 semantic repair + retest consolidated (reaggregated)",
        "experiment": "PILOT_JONES_SEMANTIC_REPAIR_RETEST_PACKAGE",
        "note": "Reaggregated from probe_val/test raw after fixing stress-trend + test-lookup bugs; B2 frozen at validation-optimal lambda=0.1.",
        "b2_lambda_frozen_M2": 0.1,
        "bstar_adjudication_val": bstar_map,
        "problem_headroom_val": sv,
        "problem_headroom_test": st,
        "method_results": ms,
        "verdict": verdict,
        "ber_to_q2_formula": "Q=sqrt(2)*erfcinv(2*BER); Q^2_dB=20*log10(Q); BER=0 -> 0.5/N_eval bound; BER>=0.5 -> None",
    }
    with open(RESULT_DIR / "result.json", "w") as f:
        json.dump(result, f, indent=1, default=str)
    print(f"[verdict] {verdict_name}")
    print(json.dumps({"problem_survives": ps_survives, "reason": ps_reason,
                      "verified_headroom": verified_headroom,
                      "impairment_added": impairment_added,
                      "stress_added_test": stress_added,
                      "oracle_anomalies": oracle_anom}, indent=1, default=str))


def _claim_ceiling(verdict_name, m4_closed):
    base = {
        "PROBLEM_SURVIVES_METHOD_CANDIDATES_FAIL":
            "problem survives but no proposed mechanism beats the strongest conventional baseline B*.",
        "KILL_COMPLEX_AXIS_AFTER_VALID_SEMANTICS_AND_CONVENTIONAL_BASELINE":
            "complex-Jones/PMD/PDL does not reintroduce a method-worthy gap.",
        "PARTIAL_ORACLE_INVALID": "oracle not a valid ceiling; verdict blocked.",
        "CONDITIONAL_GO_WITH_BLOCKING_LITERATURE_DEBT":
            "at least one mechanism candidate beats B* on fresh test seeds (provisional, pending main-control).",
    }.get(verdict_name, "")
    if not m4_closed:
        base += " M4 (joint PDL+PMD) not closed; no family-level close claim."
    return base


if __name__ == "__main__":
    main()
