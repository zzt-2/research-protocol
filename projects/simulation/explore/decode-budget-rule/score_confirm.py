"""decode-budget-rule confirm scoring (contract v1 + amend v1.1, frozen).

Single-shot scoring of the frozen rule on the three confirm batches.

FER semantics (amend v1.1):
  (a) PRIMARY -- stop-iterate output semantics, same definition as the R036
      fixed-cap points: accepted frames output the syndrome-0 iterate
      (accepted_wrong measured, =0 in all runs); cut frames output the
      abort-iterate hard decisions (ie@cut from extract_iterates.py);
      exhausted frames output the cap iterate (ie@cap).
  (b) CONSERVATIVE -- acceptance semantics: every cut counts as failure
      (FER-loss upper bound); reported alongside, never hidden.

Pareto: B0 fixed20 / B0+ES cap20 / NOMS+ES cap{10,15,50,200} / R3 (cited) /
RULE. Paired bootstrap CI95 + sign tests. Pre-registered verdict.
Writes summary.json via save_results.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import binomtest

HERE = Path(__file__).resolve().parent
SIM_ROOT = HERE.parents[1]
sys.path.insert(0, str(SIM_ROOT))
sys.path.insert(0, str(HERE))
OUT_DIR = SIM_ROOT / "results" / "decode-budget-rule"

from common._experiment import save_results  # noqa: E402
from _common import (  # noqa: E402
    ACCEPT, CAP, CUT_CORRECT, CUT_WRONG, EXHAUST, candidate_key, es_point,
    simulate_rule,
)

BOOTSTRAP_N = 10000
RNG_SEED = 20260927
FER_LOSS_GATE = 0.002  # 0.2pp, pre-registered

# R036 §五 cited coordinates -- same caches (fer from fixed-cap arm outputs,
# mean_it under first-syndrome-0 ES), cited not re-run
R3_CITED = {
    "M15": {"fer": 0.2271, "mean_it": 24.85},
    "W12": {"fer": 0.2451, "mean_it": 25.18},
    "S16": {"fer": 0.2368, "mean_it": 25.24},
}
R036_FIXED_FER = {  # fixed-cap arm FER (ie@cap semantics) on the same caches
    "M15": {"B0_cap20": 0.2446, "NOMS_cap50": 0.2275, "NOMS_cap200": 0.2251},
    "W12": {"B0_cap20": 0.2817, "NOMS_cap50": 0.2441, "NOMS_cap200": 0.2344},
    "S16": {"B0_cap20": 0.2515, "NOMS_cap50": 0.2373, "NOMS_cap200": 0.2319},
}


def paired_boot(d: np.ndarray) -> dict:
    rng = np.random.default_rng(RNG_SEED)
    n = len(d)
    boots = np.array([d[rng.integers(0, n, n)].mean() for _ in range(BOOTSTRAP_N)])
    lo, hi = (float(x) for x in np.quantile(boots, [0.025, 0.975]))
    wins, losses = int((d > 0).sum()), int((d < 0).sum())
    p = float(binomtest(wins, wins + losses, 0.5).pvalue) if wins + losses else 1.0
    return {"mean": float(d.mean()), "ci95": [lo, hi],
            "wins": wins, "losses": losses, "p_sign": p}


def fer_es_semantics_a(conv: np.ndarray, acc_ok: np.ndarray,
                       ie_at_cap: np.ndarray, cap: int) -> float:
    """cap-ES point, semantics (a): conv<=cap -> accept iterate; else ie@cap."""
    success = ((conv > 0) & (conv <= cap) & acc_ok) | (~((conv > 0) & (conv <= cap)) & (ie_at_cap == 0))
    return float(1.0 - success.mean())


def main() -> int:
    raw = json.load(open(OUT_DIR / "raw_traj_confirm.json"))
    iters = json.load(open(OUT_DIR / "raw_iterates_confirm.json"))
    frozen = json.load(open(OUT_DIR / "frozen_rule.json"))
    spec = frozen["selected_rule"]

    per_cond: dict = {}
    for cond, b in raw["batches"].items():
        sw = np.array(b["syndrome_weights"], dtype=np.int32)
        conv = np.array(b["converged_at"], dtype=np.int64)
        acc_ok = np.array(b["accepted_info_ok"], dtype=bool)
        ie200 = np.array(b["info_errors_at_200"], dtype=np.int64)
        ext = iters["batches"][cond]
        ie10 = np.array(ext["ie_at_10"], dtype=np.int64)
        ie15 = np.array(ext["ie_at_15"], dtype=np.int64)
        cut_idx = np.array(ext["cut_frame_index"], dtype=np.int64)
        cut_ie = np.array(ext["cut_ie_at_stop"], dtype=np.int64)
        n = sw.shape[0]

        stop, outcome = simulate_rule(sw, conv, spec)
        accepted = outcome == ACCEPT
        cut_mask = (outcome == CUT_CORRECT) | (outcome == CUT_WRONG)
        exhaust_mask = outcome == EXHAUST

        # semantics (a): per-frame rule success
        success_a = accepted & acc_ok
        success_a[cut_mask] = cut_ie == 0
        success_a[exhaust_mask] = ie200[exhaust_mask] == 0
        fer_rule_a = float(1.0 - success_a.mean())
        # semantics (b): acceptance-strict
        fer_rule_b = float(1.0 - (accepted & acc_ok).mean())

        counts = {"accept": int(accepted.sum()),
                  "cut_correct": int((outcome == CUT_CORRECT).sum()),
                  "cut_wrong": int((outcome == CUT_WRONG).sum()),
                  "exhaust": int(exhaust_mask.sum())}
        wrong_cut_detail = []
        widx = np.flatnonzero(outcome == CUT_WRONG)
        wpos = {int(i): k for k, i in enumerate(cut_idx)}
        for i in widx:
            wrong_cut_detail.append({
                "seed": int(b["seeds"][i]),
                "cut_at": int(stop[i]),
                "s_at_cut": int(sw[i, stop[i] - 1]),
                "would_converge_at": int(conv[i]),
                "ie_at_cut": int(cut_ie[wpos[int(i)]]),
                "ie_at_200": int(ie200[i]),
            })

        # ES points, both semantics; mean_it identical under both
        es_pts = {}
        for cap, ie_cap in ((10, ie10), (15, ie15)):
            fer, mean_it, cw = es_point(sw, conv, acc_ok, cap)
            es_pts[cap] = {"fer_a": fer_es_semantics_a(conv, acc_ok, ie_cap, cap),
                           "fer_b": fer, "mean_it": mean_it}
        for cap in (20, 50, 200):
            fer, mean_it, cw = es_point(sw, conv, acc_ok, cap)
            es_pts[cap] = {"fer_b": fer, "mean_it": mean_it}
        # cap20/50/200 fer_a: R036 fixed-cap arm numbers (same caches);
        # cap200 additionally == (ie200>0).mean() by construction (G2-anchored)
        es_pts[20]["fer_a"] = R036_FIXED_FER[cond]["B0_cap20"]
        es_pts[50]["fer_a"] = R036_FIXED_FER[cond]["NOMS_cap50"]
        es_pts[200]["fer_a"] = R036_FIXED_FER[cond]["NOMS_cap200"]
        # cited constants are rounded to 4 decimals; allow that rounding
        assert abs(es_pts[200]["fer_a"] - float((ie200 > 0).mean())) < 5e-5

        # paired stats vs cap200-ES and cap50-ES
        it_cap200 = np.where(conv > 0, np.minimum(conv, CAP), CAP)
        it_cap50 = np.where(conv > 0, np.minimum(conv, 50), 50)
        fail_rule_a = ~success_a
        fail_rule_b = ~(accepted & acc_ok)
        fail_cap200_a = (ie200 > 0)
        fail_cap200_b = ~((conv > 0) & acc_ok)

        per_cond[cond] = {
            "n": n,
            "rule": {
                "fer_a": fer_rule_a, "fer_b": fer_rule_b,
                "mean_it": float(stop.mean()),
                "outcome_counts": counts,
                "accepted_wrong": int((accepted & ~acc_ok).sum()),
                "cut_frames_with_correct_info_at_cut": int((cut_ie == 0).sum()),
                "wrong_cut_detail": wrong_cut_detail,
            },
            "es_points": es_pts,
            "branchA": {
                "iter_saving_cap200es": paired_boot(it_cap200 - stop),
                "fer_loss_a": paired_boot(
                    (fail_rule_a.astype(int) - fail_cap200_a.astype(int)).astype(float)),
                "fer_loss_b": paired_boot(
                    (fail_rule_b.astype(int) - fail_cap200_b.astype(int)).astype(float)),
            },
            "branchB": {
                "fer_rule_minus_cap50_a": float(fer_rule_a - es_pts[50]["fer_a"]),
                "fer_rule_minus_cap50_b": float(fer_rule_b - es_pts[50]["fer_b"]),
                "iter_saving_vs_cap50": paired_boot(it_cap50 - stop),
            },
        }
        print(f"[{cond}] rule FER_a={fer_rule_a:.4f} FER_b={fer_rule_b:.4f} "
              f"mean_it={stop.mean():.2f} | cap200 fer_a={es_pts[200]['fer_a']:.4f} "
              f"it={es_pts[200]['mean_it']:.1f} | cap50 fer_a={es_pts[50]['fer_a']:.4f} "
              f"it={es_pts[50]['mean_it']:.1f} | wrong_cuts={counts['cut_wrong']} "
              f"cut_info_correct={int((cut_ie == 0).sum())}", flush=True)

    # pre-registered verdict under both semantics
    def verdict_for(field_fail, field_loss):
        a_ok, b_ok = [], []
        for cond, r in per_cond.items():
            sv = r["branchA"]["iter_saving_cap200es"]
            a_ok.append(sv["ci95"][0] > 0 and r["branchA"][field_loss]["point"] <= FER_LOSS_GATE)
            b_ok.append(r["branchB"][f"fer_rule_minus_cap50_{field_fail}"] <= 0
                        and r["branchB"]["iter_saving_vs_cap50"]["ci95"][0] > 0)
        kill = any(r["branchA"][field_loss]["point"] > FER_LOSS_GATE
                   or r["branchA"]["iter_saving_cap200es"]["ci95"][0] <= 0
                   for r in per_cond.values())
        return ("ALIVE" if (all(a_ok) or all(b_ok)) else "KILL"), a_ok, b_ok

    # attach point estimates for the loss gates (paired_boot mean == point for
    # frame-level indicator differences, but keep explicit fields)
    for cond, r in per_cond.items():
        r["branchA"]["fer_loss_a"]["point"] = r["branchA"]["fer_loss_a"]["mean"]
        r["branchA"]["fer_loss_b"]["point"] = r["branchA"]["fer_loss_b"]["mean"]

    verdict_a, a_ok, b_ok_a = verdict_for("a", "fer_loss_a")
    verdict_b, a_ok_b, b_ok_b = verdict_for("b", "fer_loss_b")
    final = "ALIVE" if (verdict_a == "ALIVE" and verdict_b == "ALIVE") else "KILL"

    pareto = {}
    for cond, r in per_cond.items():
        p = r["es_points"]
        pareto[cond] = {
            "B0_fix20": {"fer": R036_FIXED_FER[cond]["B0_cap20"], "mean_it": 20.0,
                         "source": "R036 cited"},
            "B0_ES_cap20": {"fer": R036_FIXED_FER[cond]["B0_cap20"],
                            "mean_it": p[20]["mean_it"], "source": "R036 fer / this-run it"},
            "NOMS_ES_cap10": {"fer": p[10]["fer_a"], "fer_b": p[10]["fer_b"],
                              "mean_it": p[10]["mean_it"], "source": "this run"},
            "NOMS_ES_cap15": {"fer": p[15]["fer_a"], "fer_b": p[15]["fer_b"],
                              "mean_it": p[15]["mean_it"], "source": "this run"},
            "NOMS_ES_cap50": {"fer": p[50]["fer_a"], "fer_b": p[50]["fer_b"],
                              "mean_it": p[50]["mean_it"], "source": "R036 fer / this-run it"},
            "NOMS_ES_cap200": {"fer": p[200]["fer_a"], "fer_b": p[200]["fer_b"],
                               "mean_it": p[200]["mean_it"], "source": "R036 fer / this-run it"},
            "R3_rescue": {**R3_CITED[cond], "source": "R036 cited"},
            "RULE_frozen_RC120": {"fer": r["rule"]["fer_a"], "fer_b": r["rule"]["fer_b"],
                                  "mean_it": r["rule"]["mean_it"], "source": "this run"},
        }

    summary = {
        "schema_version": "decode-budget-rule.summary.v2",
        "contract": "explore/decode-budget-rule/contract.yaml (v1 frozen + amend v1.1)",
        "frozen_rule": spec,
        "frozen_at": frozen["frozen_at"],
        "fallback_selection_used": frozen["selection_criterion"]["fallback_used"],
        "gates": raw["gates"],
        "fer_semantics": {
            "a_primary": ("stop-iterate output semantics (cut frames output the "
                          "abort iterate; same definition as R036 fixed-cap FER)"),
            "b_conservative": ("acceptance semantics (every cut counts as failure; "
                               "FER-loss upper bound)"),
        },
        "per_condition": per_cond,
        "verdict": {
            "verdict_semantics_a": verdict_a,
            "verdict_semantics_b": verdict_b,
            "final_verdict": final,
            "gate": "ALIVE iff saving CI95 lower>0 AND FER loss<=0.2pp vs same-cap "
                    "fixed point in all conditions (branch B: same-FER cost below "
                    "cap50); final verdict requires BOTH semantics ALIVE",
            "branchA_A_ok_semantics_a": a_ok, "branchB_B_ok_semantics_a": b_ok_a,
            "branchA_A_ok_semantics_b": a_ok_b, "branchB_B_ok_semantics_b": b_ok_b,
        },
        "pareto_fer_vs_mean_it": pareto,
        "notes": {
            "r3_cited": "R036 §五 same-cache coordinates, cited not re-run",
            "mean_it_crosscheck": ("cap50-ES / cap200-ES mean_it recomputed from "
                                   "this round's G2-anchored trajectories; expected "
                                   "to match R036's 16.6-18.9 / 53.8-58.3"),
        },
    }
    save_results(summary, str(OUT_DIR / "summary.json"), "decode-budget-rule")
    print(f"verdict: a={verdict_a} b={verdict_b} final={final} -> "
          f"{OUT_DIR / 'summary.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
