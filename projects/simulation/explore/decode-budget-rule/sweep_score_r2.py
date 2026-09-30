"""Round-2 sweep scoring (contract_r2 sweep_protocol): full-terrain assembly.

14 new SNR points + 3 c2 anchor conditions: per point, per strategy
(B0 fix20 / B0+ES cap20 / NOMS+ES cap{10,15,50,200} / RULE / A1 / A2 /
POOL_c20), FER_a + mean_it (+ BER); bootstrap CI for rule-vs-B0 FER diff and
iteration saving. No gates at sweep points (terrain description).
Writes sweep_summary_r2.json (save_results).
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
from score_r2 import evaluate_batch, paired_boot  # noqa: E402
from gen_batches import BATCHES  # noqa: E402


def main() -> int:
    traj = json.load(open(OUT_DIR / "raw_traj_r2_sweep.json"))
    iters = json.load(open(OUT_DIR / "raw_iterates_r2.json"))
    frozen = json.load(open(OUT_DIR / "frozen_rule_r2.json"))
    rules = {"rule": frozen["selected_rule"], **frozen["ablation_rules"]}

    points = []
    for name in sorted(traj["batches"]):
        spec = BATCHES[name]
        b = traj["batches"][name]
        strat = evaluate_batch(b, iters["batches"][name], rules)
        r = strat["RULE_frozen"]
        stop = np.array(r["stop"])
        outcome = np.array(r["outcome"])
        conv = np.array(b["converged_at"], dtype=np.int64)
        acc_ok = np.array(b["accepted_info_ok"], dtype=bool)
        ie20 = np.array(b["info_errors_at_20"], dtype=np.int64)
        ie200 = np.array(b["info_errors_at_200"], dtype=np.int64)
        ie_at = {c: np.array(iters["batches"][name][f"ie_at_{c}"], dtype=np.int64)
                 for c in (10, 15, 30, 50, 100)}
        src = {20: ie20, 200: ie200, **ie_at}
        accepted = outcome == 0
        nonacc = ~accepted
        ie_stop = np.zeros(len(stop), dtype=np.int64)
        for v in np.unique(stop[nonacc]):
            ie_stop[nonacc & (stop == v)] = src[int(v)][nonacc & (stop == v)]
        fail_rule = ~(accepted & acc_ok) & ~(nonacc & (ie_stop == 0))
        fail_b0 = ie20 > 0
        entry = {
            "batch": name, "tier": name.split("_")[1], "snr_db": spec["snr"],
            "n": len(b["seeds"]),
            "strategies": {k: {"fer_a": v["fer_a"], "mean_it": v["mean_it"],
                               "ber_bits": v.get("ber_bits")}
                           for k, v in strat.items()},
            "rule_vs_b0": {
                "fer_diff": paired_boot(
                    (fail_rule.astype(int) - fail_b0.astype(int)).astype(float)),
                "iter_saving": paired_boot(20.0 - stop)},
            "rule_wrong_cuts": r["counts"]["cut_wrong"],
        }
        points.append(entry)
        print(f"[{name}] FER_b0={strat['B0_fix20']['fer_a']:.4f} "
              f"rule={r['fer_a']:.4f}/{r['mean_it']:.1f} "
              f"cap50={strat['NOMS_ES_cap50']['fer_a']:.4f}/{strat['NOMS_ES_cap50']['mean_it']:.1f} "
              f"cap200={strat['NOMS_ES_cap200']['fer_a']:.4f} "
              f"W={r['counts']['cut_wrong']}", flush=True)

    # c2 anchors appended as points (same evaluator, fresh seeds)
    ctraj = json.load(open(OUT_DIR / "raw_traj_r2_confirm.json"))
    for name, b in ctraj["batches"].items():
        spec = BATCHES[name]
        strat = evaluate_batch(b, iters["batches"][name], rules)
        r = strat["RULE_frozen"]
        stop = np.array(r["stop"])
        outcome = np.array(r["outcome"])
        acc_ok = np.array(b["accepted_info_ok"], dtype=bool)
        ie20 = np.array(b["info_errors_at_20"], dtype=np.int64)
        ie200 = np.array(b["info_errors_at_200"], dtype=np.int64)
        ie_at = {c: np.array(iters["batches"][name][f"ie_at_{c}"], dtype=np.int64)
                 for c in (10, 15, 30, 50, 100)}
        src = {20: ie20, 200: ie200, **ie_at}
        accepted = outcome == 0
        nonacc = ~accepted
        ie_stop = np.zeros(len(stop), dtype=np.int64)
        for v in np.unique(stop[nonacc]):
            ie_stop[nonacc & (stop == v)] = src[int(v)][nonacc & (stop == v)]
        fail_rule = ~(accepted & acc_ok) & ~(nonacc & (ie_stop == 0))
        points.append({
            "batch": name, "tier": {"c2_M15": "mod", "c2_W12": "weak",
                                    "c2_S16": "strg"}[name],
            "snr_db": spec["snr"], "n": len(b["seeds"]),
            "strategies": {k: {"fer_a": v["fer_a"], "mean_it": v["mean_it"],
                               "ber_bits": v.get("ber_bits")}
                           for k, v in strat.items()},
            "rule_vs_b0": {
                "fer_diff": paired_boot(
                    (fail_rule.astype(int) - (ie20 > 0).astype(int)).astype(float)),
                "iter_saving": paired_boot(20.0 - stop)},
            "rule_wrong_cuts": r["counts"]["cut_wrong"],
        })

    tiers = {}
    for p in points:
        tiers.setdefault(p["tier"], []).append(
            {"snr_db": p["snr_db"], "batch": p["batch"],
             "fer_b0": p["strategies"]["B0_fix20"]["fer_a"],
             "fer_rule": p["strategies"]["RULE_frozen"]["fer_a"],
             "fer_cap50": p["strategies"]["NOMS_ES_cap50"]["fer_a"],
             "fer_cap200": p["strategies"]["NOMS_ES_cap200"]["fer_a"],
             "mean_it_rule": p["strategies"]["RULE_frozen"]["mean_it"],
             "mean_it_cap50": p["strategies"]["NOMS_ES_cap50"]["mean_it"],
             "mean_it_cap200": p["strategies"]["NOMS_ES_cap200"]["mean_it"],
             "fer_cap10": p["strategies"]["NOMS_ES_cap10"]["fer_a"],
             "fer_cap15": p["strategies"]["NOMS_ES_cap15"]["fer_a"],
             "mean_it_cap10": p["strategies"]["NOMS_ES_cap10"]["mean_it"],
             "mean_it_cap15": p["strategies"]["NOMS_ES_cap15"]["mean_it"],
             "fer_A1": p["strategies"]["ABL_A1_gclrpc1"]["fer_a"],
             "mean_it_A1": p["strategies"]["ABL_A1_gclrpc1"]["mean_it"],
             "fer_A2": p["strategies"]["ABL_A2_osc3"]["fer_a"],
             "mean_it_A2": p["strategies"]["ABL_A2_osc3"]["mean_it"],
             "wrong_cuts": p["rule_wrong_cuts"]})
    for t in tiers:
        tiers[t] = sorted(tiers[t], key=lambda x: x["snr_db"])

    summary = {
        "schema_version": "decode-budget-rule.sweep-r2.v1",
        "contract": "contract_r2 sweep_protocol (terrain, no gates)",
        "frozen_rule": rules["rule"],
        "tiers": tiers,
        "points": points,
        "notes": {"tiers": "mod=4.0x1.9, weak=11.6x10.1, strg=4.2x1.4; "
                           "anchors = c2 fresh-seed batches"},
    }
    save_results(summary, str(OUT_DIR / "sweep_summary_r2.json"),
                 "decode-budget-rule-r2-sweep")
    print("sweep summary written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
