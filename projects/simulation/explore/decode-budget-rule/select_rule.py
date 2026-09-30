"""decode-budget-rule dev selection (contract.yaml v1, frozen).

Loads raw_traj_dev.json, evaluates all 28 pre-registered candidates on the
pooled dev batches (1600 frames), applies the pre-registered selection
criterion, and writes frozen_rule.json. Dev data only -- confirm batches are
never touched here.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SIM_ROOT = HERE.parents[1]
OUT_DIR = SIM_ROOT / "results" / "decode-budget-rule"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from _common import (  # noqa: E402
    ACCEPT, CAP, CUT_WRONG, SIMPLICITY_ORDER, candidate_key, candidate_specs,
    es_point, first_zero, simulate_rule,
)

SELECTION = {  # pre-registered in contract
    "max_pooled_W": 2,
    "max_per_batch_W": 1,
}


def load_dev() -> dict[str, dict]:
    raw = json.load(open(OUT_DIR / "raw_traj_dev.json"))
    out = {}
    for name, b in raw["batches"].items():
        sw = np.array(b["syndrome_weights"], dtype=np.int32)
        conv = np.array(b["converged_at"], dtype=np.int64)
        acc_ok = np.array(b["accepted_info_ok"], dtype=bool)
        out[name] = {"sw": sw, "conv": conv, "acc_ok": acc_ok}
    return out


def main() -> int:
    dev = load_dev()
    n_total = sum(d["sw"].shape[0] for d in dev.values())
    print(f"dev pool: {n_total} frames across {list(dev)}")

    # dev baselines (cap200-ES reference points)
    baselines = {}
    for name, d in dev.items():
        fer, mean_it, cw = es_point(d["sw"], d["conv"], d["acc_ok"], CAP)
        baselines[name] = {"fer_cap200es": fer, "mean_it_cap200es": mean_it,
                           "converged_wrong": cw}
        print(f"[{name}] cap200-ES: FER={fer:.4f} mean_it={mean_it:.1f} conv_wrong={cw}")
    pool_mean_it = float(np.mean([
        es_point(d["sw"], d["conv"], d["acc_ok"], CAP)[1] for d in dev.values()
    ]))

    table = []
    for spec in candidate_specs():
        key = candidate_key(spec)
        per_batch = {}
        stops_all, conv_all, ok_all = [], [], []
        for name, d in dev.items():
            stop, outcome = simulate_rule(d["sw"], d["conv"], spec)
            wrong_cuts = int((outcome == CUT_WRONG).sum())
            accepted = (outcome == ACCEPT)
            n = d["sw"].shape[0]
            fer = 1.0 - (accepted & d["acc_ok"]).sum() / n
            per_batch[name] = {"W": wrong_cuts, "fer": fer,
                               "mean_it": float(stop.mean())}
            stops_all.append(stop)
            conv_all.append(d["conv"])
            ok_all.append(d["acc_ok"])
        stop_pool = np.concatenate(stops_all)
        pooled_W = sum(pb["W"] for pb in per_batch.values())
        table.append({
            "key": key, "spec": spec,
            "pooled_W": pooled_W,
            "per_batch": per_batch,
            "pooled_mean_it": float(stop_pool.mean()),
            "pooled_saving_vs_cap200es": pool_mean_it - float(stop_pool.mean()),
            "feasible": (pooled_W <= SELECTION["max_pooled_W"]
                         and all(pb["W"] <= SELECTION["max_per_batch_W"]
                                 for pb in per_batch.values())),
        })
        print(f"{key:>14}: W={pooled_W} mean_it={stop_pool.mean():5.1f} "
              f"saving={pool_mean_it - stop_pool.mean():5.1f} "
              f"per_batch_W={[per_batch[b]['W'] for b in per_batch]} "
              f"feasible={table[-1]['feasible']}", flush=True)

    feasible = [t for t in table if t["feasible"]]
    if feasible:
        # max saving -> smaller pooled W -> simplicity -> larger tau (conservative)
        def rank(t):
            tau = t["spec"].get("tau", t["spec"].get("tau_m", 0))
            return (-t["pooled_saving_vs_cap200es"], t["pooled_W"],
                    SIMPLICITY_ORDER[t["spec"]["family"]], -tau)
        chosen = min(feasible, key=rank)
        fallback_used = False
    else:
        def rank(t):
            tau = t["spec"].get("tau", t["spec"].get("tau_m", 0))
            return (t["pooled_W"], -t["pooled_saving_vs_cap200es"],
                    SIMPLICITY_ORDER[t["spec"]["family"]], -tau)
        chosen = min(table, key=rank)
        fallback_used = True

    frozen = {
        "schema_version": "decode-budget-rule.frozen-rule.v1",
        "contract": "explore/decode-budget-rule/contract.yaml (v1, frozen)",
        "selected_rule": {"key": chosen["key"], **chosen["spec"]},
        "selection_criterion": {
            "constraint": ("pooled_W <= 2 AND per-batch W <= 1; "
                           "maximize pooled mean-it saving vs dev cap200-ES; "
                           "tie-break smaller pooled W -> simplicity "
                           "RA>RC>RD>RB>RE -> larger tau"),
            "fallback": ("no feasible candidate -> min pooled_W "
                         "(tie: larger saving); expected confirm KILL risk"),
            "fallback_used": fallback_used,
        },
        "chosen_dev_diagnostics": chosen,
        "dev_baselines_cap200es": baselines,
        "dev_pool_mean_it_cap200es": pool_mean_it,
        "candidate_table": table,
        "n_dev_frames": n_total,
        "frozen_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    out_path = OUT_DIR / "frozen_rule.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(frozen, f, indent=1)
    print(f"\nfrozen rule: {chosen['key']} (fallback={fallback_used}) -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
