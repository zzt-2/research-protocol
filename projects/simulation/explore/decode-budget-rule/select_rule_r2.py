"""Round-2 rule selection + ablation calibration (contract_r2, dev data only).

Dev pool = round-1 dev (1600 frames, raw_traj_dev.json) + dev2_W12 (1024,
raw_traj_r2_dev.json) = 2624 frames. Deployable families F1(RD)/F2(PL)/F3(PR)
under the pre-registered W=0 hard constraint; ablation families A1(C1)/A2(OSC)
calibrated under the same criterion (not deployable). Writes frozen_rule_r2.json.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE.parents[1] / "results" / "decode-budget-rule"
sys.path.insert(0, str(HERE))

from _common import (  # noqa: E402
    ACCEPT, CAP, CUT_WRONG, SIMPLICITY_ORDER, simulate_rule_r2, es_point,
)


def load_dev_pool() -> dict[str, dict]:
    pool = {}
    r1 = json.load(open(OUT_DIR / "raw_traj_dev.json"))
    for name, b in r1["batches"].items():
        pool[name] = {
            "sw": np.array(b["syndrome_weights"], dtype=np.int32),
            "conv": np.array(b["converged_at"], dtype=np.int64),
            "acc_ok": np.array(b["accepted_info_ok"], dtype=bool),
        }
    r2 = json.load(open(OUT_DIR / "raw_traj_r2_dev.json"))
    for name, b in r2["batches"].items():
        pool[name] = {
            "sw": np.array(b["syndrome_weights"], dtype=np.int32),
            "conv": np.array(b["converged_at"], dtype=np.int64),
            "acc_ok": np.array(b["accepted_info_ok"], dtype=bool),
        }
    return pool


def deployable_specs() -> list[dict]:
    specs = [{"family": "RD", "tau": t} for t in (0.55, 0.65, 0.75)]
    specs += [{"family": "PL", "ta": a, "tb": b}
              for a in (100, 120, 140) for b in (100, 120, 140)]
    specs += [{"family": "PR", "tau": t} for t in (0.5, 0.6, 0.7)]
    assert len(specs) == 15
    return specs


def ablation_specs() -> list[dict]:
    a1 = [{"family": "C1", "s_thr": s, "T": T, "l1_min": 20}
          for s in (100, 120, 140) for T in (5, 8)]
    a2 = [{"family": "OSC", "l_min": m} for m in (10, 20, 30)]
    return a1 + a2


FAM_ORDER = {"RD": 0, "PR": 1, "PL": 2}


def evaluate(pool, spec):
    per_batch, stops = {}, []
    for name, d in pool.items():
        stop, out = simulate_rule_r2(d["sw"], d["conv"], spec)
        n = d["sw"].shape[0]
        fer = 1.0 - (out == ACCEPT).sum() / n  # acceptance semantics; acc_ok measured all True
        per_batch[name] = {"W": int((out == CUT_WRONG).sum()),
                           "fer": fer, "mean_it": float(stop.mean())}
        stops.append(stop)
    pooled_W = sum(pb["W"] for pb in per_batch.values())
    return {"per_batch": per_batch, "pooled_W": pooled_W,
            "pooled_mean_it": float(np.concatenate(stops).mean())}


def main() -> int:
    pool = load_dev_pool()
    n_total = sum(d["sw"].shape[0] for d in pool.values())
    print(f"dev pool: {n_total} frames across {list(pool)}")

    baselines = {}
    pool_mean_it_cap200 = np.mean([
        es_point(d["sw"], d["conv"], d["acc_ok"], CAP)[1] for d in pool.values()])
    for name, d in pool.items():
        fer, mean_it, cw = es_point(d["sw"], d["conv"], d["acc_ok"], CAP)
        baselines[name] = {"fer_cap200es": fer, "mean_it_cap200es": mean_it,
                           "converged_wrong": cw}

    table = []
    for spec in deployable_specs() + ablation_specs():
        r = evaluate(pool, spec)
        saving = pool_mean_it_cap200 - r["pooled_mean_it"]
        table.append({"spec": spec, **r,
                      "pooled_saving_vs_cap200es": saving,
                      "deployable": spec["family"] in ("RD", "PL", "PR")})
        key = (f"{spec['family']}_" +
               (f"{spec['tau']:g}" if "tau" in spec else
                f"{spec.get('ta')}_{spec.get('tb')}" if spec["family"] == "PL" else
                f"{spec.get('s_thr')}_T{spec.get('T')}" if spec["family"] == "C1" else
                f"lmin{spec.get('l_min')}"))
        print(f"{key:>16}: W={r['pooled_W']} mean_it={r['pooled_mean_it']:5.1f} "
              f"saving={saving:5.1f} "
              f"per_batch_W={[r['per_batch'][b]['W'] for b in r['per_batch']]}",
              flush=True)

    def pick(specs_sub, hard_w0=True):
        feas = [t for t in table if t["spec"] in specs_sub
                and (t["pooled_W"] == 0 if hard_w0 else t["pooled_W"] <= 1)]
        if feas:
            def rank(t):
                s = t["spec"]
                tie = (s.get("tau", 0) if s["family"] != "PL"
                       else s["ta"] + s["tb"])
                return (-t["pooled_saving_vs_cap200es"],
                        FAM_ORDER.get(s["family"], 9), -tie)
            return min(feas, key=rank), False
        # fallback: min W, tie larger saving
        sub = [t for t in table if t["spec"] in specs_sub]

        def rank2(t):
            s = t["spec"]
            tie = (s.get("tau", 0) if s["family"] != "PL"
                   else s["ta"] + s["tb"])
            return (t["pooled_W"], -t["pooled_saving_vs_cap200es"], -tie)
        return min(sub, key=rank2), True

    dep = deployable_specs()
    chosen_dep, dep_fallback = pick(dep, hard_w0=True)
    chosen_a1, a1_fb = pick([s for s in ablation_specs() if s["family"] == "C1"])
    chosen_a2, a2_fb = pick([s for s in ablation_specs() if s["family"] == "OSC"])

    frozen = {
        "schema_version": "decode-budget-rule.frozen-rule-r2.v1",
        "contract": "explore/decode-budget-rule/contract_r2.yaml (v1, frozen)",
        "selected_rule": chosen_dep["spec"],
        "selection_criterion": {
            "constraint": "pooled dev W == 0 over 2624 frames; max pooled "
                          "saving vs cap200-ES; tie: F1>F3>F2, larger tau",
            "fallback_used": dep_fallback,
            "ablation_calibration": "A1/A2 grids calibrated under the same "
                                    "W=0/max-saving criterion (controls, not "
                                    "deployable)",
            "a1_fallback": a1_fb, "a2_fallback": a2_fb,
        },
        "ablation_rules": {"A1_gclrpc1": chosen_a1["spec"],
                           "A2_osc3": chosen_a2["spec"]},
        "dev_baselines_cap200es": baselines,
        "dev_pool_mean_it_cap200es": float(pool_mean_it_cap200),
        "candidate_table": table,
        "n_dev_frames": n_total,
        "frozen_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    path = OUT_DIR / "frozen_rule_r2.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(frozen, f, indent=1)
    print(f"\nfrozen r2 rule: {chosen_dep['spec']} (fallback={dep_fallback})")
    print(f"ablations: {chosen_a1['spec']} / {chosen_a2['spec']} -> {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
