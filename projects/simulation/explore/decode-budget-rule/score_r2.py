"""Round-2 confirm scoring (contract_r2 verdict + Pareto + ablation + pool).

Verdict layers (pre-registered):
  PRIMARY (D063 user criterion): FER_a(rule) <= FER_a(B0 fix20) in all three
      c2 conditions AND iteration saving vs B0 (20 - mean_it) CI95 lower > 0.
  STRICT (honest boundary): FER loss vs cap200-ES <= 0.2pp + saving CI > 0.
  cap50 reading: diffs reported, no gate.

Writes summary_r2.json (save_results). evaluate_batch() is shared with
sweep_score_r2.py.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SIM_ROOT = HERE.parents[1]
sys.path.insert(0, str(SIM_ROOT))
sys.path.insert(0, str(HERE))
OUT_DIR = SIM_ROOT / "results" / "decode-budget-rule"

from common._experiment import save_results  # noqa: E402
from _common import (  # noqa: E402
    ACCEPT, CAP, CUT_CORRECT, CUT_WRONG, EXHAUST, pool_simulate,
    simulate_rule_r2,
)

BOOTSTRAP_N = 10000
RNG_SEED = 20260930
FER_LOSS_GATE = 0.002
R3_CITED_R1 = {"c2_M15": (0.2271, 24.85), "c2_W12": (0.2451, 25.18),
               "c2_S16": (0.2368, 25.24)}  # round-1 batches, labeled


def paired_boot(d: np.ndarray) -> dict:
    rng = np.random.default_rng(RNG_SEED)
    n = len(d)
    boots = np.array([d[rng.integers(0, n, n)].mean()
                      for _ in range(BOOTSTRAP_N)])
    lo, hi = (float(x) for x in np.quantile(boots, [0.025, 0.975]))
    wins, losses = int((d > 0).sum()), int((d < 0).sum())
    from scipy.stats import binomtest
    p = float(binomtest(wins, wins + losses, 0.5).pvalue) if wins + losses else 1.0
    return {"mean": float(d.mean()), "ci95": [lo, hi],
            "wins": wins, "losses": losses, "p_sign": p}


def evaluate_batch(b: dict, rec: dict, rules: dict) -> dict:
    """All strategies on one batch. b = traj batch dict, rec = iterates rec."""
    sw = np.array(b["syndrome_weights"], dtype=np.int32)
    conv = np.array(b["converged_at"], dtype=np.int64)
    acc_ok = np.array(b["accepted_info_ok"], dtype=bool)
    ie20 = np.array(b["info_errors_at_20"], dtype=np.int64)
    ie200 = np.array(b["info_errors_at_200"], dtype=np.int64)
    ie_at = {c: np.array(rec[f"ie_at_{c}"], dtype=np.int64)
             for c in (10, 15, 30, 50, 100)}
    n = sw.shape[0]

    def stop_ie(idx: np.ndarray, stops: np.ndarray) -> np.ndarray:
        """ie at the given frames' stop iterates (idx = frame indices)."""
        src = {20: ie20, CAP: ie200, **ie_at}
        out = np.empty(stops.shape[0], dtype=np.int64)
        for v in np.unique(stops):
            v = int(v)
            if v not in src:
                raise RuntimeError("stop iterate not covered by extraction caps")
            m = stops == v
            out[m] = src[v][idx[m]]
        return out

    strat: dict[str, dict] = {}

    def add_es_cap(cap: int, ie_cap: np.ndarray):
        accepted = (conv > 0) & (conv <= cap)
        stop = np.where(conv > 0, np.minimum(conv, cap), cap)
        fer_a = float(1.0 - ((accepted & acc_ok) |
                             (~accepted & (ie_cap == 0))).mean())
        ber = int(ie_cap[~accepted].sum())
        strat[f"NOMS_ES_cap{cap}"] = {
            "fer_a": fer_a, "fer_b": float(1.0 - (accepted & acc_ok).mean()),
            "mean_it": float(stop.mean()), "ber_bits": ber}

    strat["B0_fix20"] = {"fer_a": float((ie20 > 0).mean()),
                         "fer_b": float((ie20 > 0).mean()), "mean_it": 20.0,
                         "ber_bits": int(ie20.sum())}
    accepted20 = (conv > 0) & (conv <= 20)
    strat["B0_ES_cap20"] = {
        "fer_a": float(1.0 - ((accepted20 & acc_ok) |
                              (~accepted20 & (ie20 == 0))).mean()),
        "fer_b": float(1.0 - (accepted20 & acc_ok).mean()),
        "mean_it": float(np.where(conv > 0, np.minimum(conv, 20), 20).mean()),
        "ber_bits": int(ie20[~accepted20].sum())}
    add_es_cap(10, ie_at[10])
    add_es_cap(15, ie_at[15])
    add_es_cap(50, ie_at[50])
    accepted200 = conv > 0
    strat["NOMS_ES_cap200"] = {
        "fer_a": float(1.0 - ((accepted200 & acc_ok) |
                              (~accepted200 & (ie200 == 0))).mean()),
        "fer_b": float(1.0 - (accepted200 & acc_ok).mean()),
        "mean_it": float(np.where(conv > 0, conv, CAP).mean()),
        "ber_bits": int(ie200[~accepted200].sum())}

    def add_rule(tag: str, spec: dict, cut_ie_full=None):
        """cut_ie_full: per-frame ie at stop for cut frames (needed for rules
        whose stops fall outside the extraction cap set, e.g. per-iteration
        ablations); None -> checkpoint lookup via stop_ie()."""
        stop, outcome = simulate_rule_r2(sw, conv, spec)
        accepted = outcome == ACCEPT
        cut = (outcome == CUT_CORRECT) | (outcome == CUT_WRONG)
        exh = outcome == EXHAUST
        # accepted frames stop at their (arbitrary) convergence iterate and
        # are correct by construction (acc_ok measured); only cut/exhaust
        # stops need ie lookups (cut stops at checkpoints, exhaust at CAP)
        ie_stop = np.zeros(n, dtype=np.int64)
        if cut_ie_full is None:
            ie_stop[cut] = stop_ie(np.flatnonzero(cut), stop[cut])
        else:
            ie_stop[cut] = np.asarray(cut_ie_full)[cut]
        ie_stop[exh] = ie200[exh]
        success_a = (accepted & acc_ok) | (cut & (ie_stop == 0)) | \
                    (exh & (ie200 == 0))
        strat[tag] = {
            "fer_a": float(1.0 - success_a.mean()),
            "fer_b": float(1.0 - (accepted & acc_ok).mean()),
            "mean_it": float(stop.mean()),
            "ber_bits": int(ie_stop[cut].sum() + ie200[exh].sum()),
            "counts": {"accept": int(accepted.sum()),
                       "cut_correct": int((outcome == CUT_CORRECT).sum()),
                       "cut_wrong": int((outcome == CUT_WRONG).sum()),
                       "exhaust": int(exh.sum())},
            "stop": stop.tolist(), "outcome": outcome.tolist()}

    add_rule("RULE_frozen", rules["rule"])
    a1_idx = np.array(rec["A1_cut_index"], dtype=np.int64)
    a1_full = np.zeros(n, dtype=np.int64)
    a1_full[a1_idx] = np.array(rec["A1_cut_ie_at_stop"], dtype=np.int64)
    add_rule("ABL_A1_gclrpc1", rules["A1_gclrpc1"], cut_ie_full=a1_full)
    a2_idx = np.array(rec["A2_cut_index"], dtype=np.int64)
    a2_full = np.zeros(n, dtype=np.int64)
    a2_full[a2_idx] = np.array(rec["A2_cut_ie_at_stop"], dtype=np.int64)
    add_rule("ABL_A2_osc3", rules["A2_osc3"], cut_ie_full=a2_full)

    # pool variants (stops at checkpoints / conv / CAP only)
    for c in (15, 20, 25):
        stop, outcome, over = pool_simulate(
            sw, conv, rules["rule"], block=32, budget_per_frame=float(c))
        accepted = outcome == ACCEPT
        nonacc = ~accepted
        ie_stop = np.zeros(n, dtype=np.int64)
        ie_stop[nonacc] = stop_ie(np.flatnonzero(nonacc), stop[nonacc])
        success_a = (accepted & acc_ok) | (nonacc & (ie_stop == 0))
        strat[f"POOL_c{c}"] = {
            "fer_a": float(1.0 - success_a.mean()),
            "fer_b": float(1.0 - (accepted & acc_ok).mean()),
            "mean_it": float(stop.mean()),
            "ber_bits": int(ie_stop[nonacc].sum()),
            "blocks_overshoot": int(np.sum(over)),
            "n_blocks": int(np.ceil(n / 32))}
    return strat


def main() -> int:
    traj = json.load(open(OUT_DIR / "raw_traj_r2_confirm.json"))
    iters = json.load(open(OUT_DIR / "raw_iterates_r2.json"))
    frozen = json.load(open(OUT_DIR / "frozen_rule_r2.json"))
    rules = {"rule": frozen["selected_rule"], **frozen["ablation_rules"]}

    per_cond = {}
    for cond, b in traj["batches"].items():
        strat = evaluate_batch(b, iters["batches"][cond], rules)
        r = strat["RULE_frozen"]
        stop = np.array(r["stop"])
        per_cond[cond] = {
            "n": len(b["seeds"]),
            "strategies": {k: {x: v[x] for x in v if not x.startswith("_")}
                           for k, v in strat.items()},
            "primary_vs_b0": {
                "fer_rule_minus_b0": r["fer_a"] - strat["B0_fix20"]["fer_a"],
                "iter_saving_b0": paired_boot(20.0 - stop)},
            "strict_vs_cap200": {
                "fer_loss": paired_boot(
                    ((~(np.array(r["outcome"]) == ACCEPT)).astype(int) -
                     (~((np.array(b["converged_at"], dtype=np.int64) > 0) &
                        np.array(b["accepted_info_ok"], dtype=bool))).astype(int)
                    ).astype(float)),
                "iter_saving": paired_boot(
                    np.where(np.array(b["converged_at"], dtype=np.int64) > 0,
                             np.minimum(np.array(b["converged_at"], dtype=np.int64), CAP),
                             CAP) - stop)},
            "vs_cap50": {
                "fer_rule_minus_cap50": r["fer_a"] - strat["NOMS_ES_cap50"]["fer_a"],
                "iter_diff_cap50": paired_boot(
                    np.where(np.array(b["converged_at"], dtype=np.int64) > 0,
                             np.minimum(np.array(b["converged_at"], dtype=np.int64), 50),
                             50) - stop)},
        }
        print(f"[{cond}] rule FER_a={r['fer_a']:.4f} mean_it={r['mean_it']:.2f} "
              f"W={r['counts']['cut_wrong']} | B0 {strat['B0_fix20']['fer_a']:.4f}/20 "
              f"| cap50 {strat['NOMS_ES_cap50']['fer_a']:.4f}/{strat['NOMS_ES_cap50']['mean_it']:.1f} "
              f"| cap200 {strat['NOMS_ES_cap200']['fer_a']:.4f}/{strat['NOMS_ES_cap200']['mean_it']:.1f} "
              f"| A1 {strat['ABL_A1_gclrpc1']['fer_a']:.4f}/{strat['ABL_A1_gclrpc1']['mean_it']:.1f} "
              f"W={strat['ABL_A1_gclrpc1']['counts']['cut_wrong']} "
              f"| A2 {strat['ABL_A2_osc3']['fer_a']:.4f}/{strat['ABL_A2_osc3']['mean_it']:.1f} "
              f"W={strat['ABL_A2_osc3']['counts']['cut_wrong']}", flush=True)

    primary_ok = [c["primary_vs_b0"]["fer_rule_minus_b0"] <= 0 and
                  c["primary_vs_b0"]["iter_saving_b0"]["ci95"][0] > 0
                  for c in per_cond.values()]
    strict_ok = [c["strict_vs_cap200"]["fer_loss"]["mean"] <= FER_LOSS_GATE and
                 c["strict_vs_cap200"]["iter_saving"]["ci95"][0] > 0
                 for c in per_cond.values()]

    summary = {
        "schema_version": "decode-budget-rule.summary-r2.v1",
        "contract": "contract_r2 (v1, frozen) + D063 verdict criteria",
        "frozen_rule": rules["rule"],
        "frozen_at": frozen["frozen_at"],
        "selection_fallback_used": frozen["selection_criterion"]["fallback_used"],
        "gates": traj["gates"],
        "per_condition": per_cond,
        "verdict": {
            "PRIMARY_deployable_vs_B0": "PASS" if all(primary_ok) else "FAIL",
            "STRICT_cap200_parity_boundary":
                "PASS" if all(strict_ok) else "FAIL",
            "per_condition_primary": primary_ok,
            "per_condition_strict": strict_ok,
        },
        "notes": {
            "r3_cited": ("R3 numbers are round-1-batch coordinates (different "
                         "seeds), cited for context only"),
            "ablation": ("A1=GC-LDPC C1-type, A2=N04 3-shift oscillation stop; "
                         "dev-calibrated under the same W-preferred criterion"),
            "pool": ("exploratory cross-frame budget pool, block=32, checkpoint "
                     "budget guard, c in {15,20,25}"),
        },
    }
    save_results(summary, str(OUT_DIR / "summary_r2.json"), "decode-budget-rule-r2")
    print(f"verdict: primary={'PASS' if all(primary_ok) else 'FAIL'} "
          f"strict={'PASS' if all(strict_ok) else 'FAIL'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
