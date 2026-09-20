"""Step-1 feature analysis on the existing confirm2048 sample (read-only).

Answers the applicability-condition question on existing data before any new
condition is generated:

1. Frame categories over the B0-failed subset (501 frames at 15 dB):
   R3-only rescue (R3 final correct & R1 final wrong), R1-only, both rescued,
   both failed, plus R3-vs-F discordant frames.
2. Per-category feature distributions, split into
   - receiver-observable (no truth): |LLR| statistics, B0 syndrome trajectory
     features (s_1, s_20, min, tail behaviour classification), stage-2
     iterations/final syndrome;
   - truth-based explanatory (NOT deployable): channel hard-decision error
     count (sign(LLR) vs truth_coded, convention llr>0 -> bit 1, probed),
     B0 info/coded errors.
3. Summary tables only; per-frame lists only for the small discordant sets.

Writes analysis_confirm2048_features.json next to the raw file.  Never
modifies any existing artifact.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RESULTS = HERE.parents[1] / "results" / "decode-failure-rescue"
RAW = RESULTS / "raw_confirm2048.json"
CACHE = RESULTS / "llr_cache" / "confirm2048"
OUT = RESULTS / "analysis_confirm2048_features.json"


def llr_features(llr: np.ndarray) -> dict:
    a = np.abs(llr)
    return {
        "mean_abs_llr": float(a.mean()),
        "median_abs_llr": float(np.median(a)),
        "q10_abs_llr": float(np.percentile(a, 10)),
        "q90_abs_llr": float(np.percentile(a, 90)),
        "frac_abs_lt_0p5": float((a < 0.5).mean()),
        "frac_abs_lt_1": float((a < 1.0).mean()),
    }


def b0_traj_features(block: dict) -> dict:
    w = block["syndrome_weights"]
    return {
        "s1": int(w[0]),
        "s20": int(w[-1]),
        "s_min": int(min(w)),
        "s_max": int(max(w)),
        "classification": block["classification"],
        "info_errors": block["info_errors"],
        "coded_errors": block["coded_errors"],
    }


def summarize(values: list[float]) -> dict:
    if not values:
        return {"n": 0}
    arr = np.asarray(values, dtype=float)
    return {
        "n": len(arr),
        "mean": float(arr.mean()),
        "median": float(np.median(arr)),
        "q25": float(np.percentile(arr, 25)),
        "q75": float(np.percentile(arr, 75)),
    }


def main() -> int:
    raw = json.loads(RAW.read_text(encoding="utf-8"))
    frames = raw["frames"]

    # ---- merge LLR-cache features (channel HD errors need truth: explanatory)
    per_frame = []
    for rec in frames:
        seed = rec["seed"]
        with np.load(CACHE / f"frame_{seed}.npz") as d:
            llr = d["llr"].astype(np.float32)
            tc = d["truth_coded"].astype(np.uint8)
        hd = (llr > 0).astype(np.uint8)
        ch_err = int(np.count_nonzero(hd != tc))  # truth-based, explanatory
        row = {
            "seed": seed,
            "ch_hd_errors": ch_err,           # truth-based explanatory
            **llr_features(llr),               # receiver-observable
            "B0": b0_traj_features(rec["B0"]),
        }
        r1, r3, f = rec["arms"]["R1"], rec["arms"]["R3"], rec["arms"]["F"]
        row["R1_final_err"] = r1["final"]["info_errors"]
        row["R3_final_err"] = r3["final"]["info_errors"]
        row["F_final_err"] = f["final"]["info_errors"]
        row["F1_err"] = rec["F1"]["info_errors"]
        for name, arm in (("R1", r1), ("R3", r3), ("F", f)):
            s2 = arm["stage2"]
            if s2 is not None:
                row[f"{name}_s2_iters"] = s2["iterations_run"]
                row[f"{name}_s2_final_syn"] = s2["final_syndrome"]
                row[f"{name}_s2_accepted"] = s2["accepted"]
        per_frame.append(row)

    b0_wrong = [r for r in per_frame if r["B0"]["info_errors"] > 0]
    cats = {
        "r3_only_rescue": [r for r in b0_wrong
                           if r["R3_final_err"] == 0 and r["R1_final_err"] > 0],
        "r1_only_rescue": [r for r in b0_wrong
                           if r["R1_final_err"] == 0 and r["R3_final_err"] > 0],
        "both_rescued": [r for r in b0_wrong
                         if r["R1_final_err"] == 0 and r["R3_final_err"] == 0],
        "both_failed": [r for r in b0_wrong
                        if r["R1_final_err"] > 0 and r["R3_final_err"] > 0],
        "b0_correct": [r for r in per_frame if r["B0"]["info_errors"] == 0],
    }
    discord_r3f = {
        "r3_better": [r for r in per_frame
                      if r["R3_final_err"] == 0 and r["F_final_err"] > 0],
        "f_better": [r for r in per_frame
                     if r["F_final_err"] == 0 and r["R3_final_err"] > 0],
    }

    def cat_table(cat: list[dict]) -> dict:
        out: dict = {"n": len(cat)}
        for key in ("mean_abs_llr", "median_abs_llr", "q10_abs_llr",
                    "frac_abs_lt_0p5", "frac_abs_lt_1", "ch_hd_errors"):
            out[key] = summarize([r[key] for r in cat])
        for key in ("s1", "s20", "s_min"):
            out[f"B0_{key}"] = summarize([r["B0"][key] for r in cat])
        out["B0_classification"] = {
            c: sum(1 for r in cat if r["B0"]["classification"] == c)
            for c in ("stagnated", "oscillating", "descending", "other", "converged_wrong", None)
        }
        out["B0_info_errors"] = summarize([r["B0"]["info_errors"] for r in cat])
        return out

    result = {
        "schema_version": "dfr.analysis.confirm2048-features.v1",
        "source": {"raw": str(RAW), "cache": str(CACHE),
                   "llr_sign_convention": "llr>0 -> bit1 (probed: hd errors 1-14% per frame)"},
        "feature_semantics": {
            "receiver_observable": ["mean/median/q10/q90 |LLR|", "frac |LLR|<thr",
                                    "B0 syndrome trajectory s1/s20/s_min/classification",
                                    "stage2 iters/final syndrome"],
            "truth_based_explanatory_only": ["ch_hd_errors (channel hard-decision errors)",
                                             "B0 info/coded errors"],
        },
        "counts": {
            "total": len(per_frame),
            "b0_wrong": len(b0_wrong),
            **{k: len(v) for k, v in cats.items()},
            "r3_vs_f_r3_better": len(discord_r3f["r3_better"]),
            "r3_vs_f_f_better": len(discord_r3f["f_better"]),
        },
        "categories": {k: cat_table(v) for k, v in cats.items()},
        "r3_vs_f": {k: cat_table(v) for k, v in discord_r3f.items()},
        "r3_only_rescue_seeds": [r["seed"] for r in cats["r3_only_rescue"]],
        "r1_only_rescue_seeds": [r["seed"] for r in cats["r1_only_rescue"]],
        "r3_vs_f_discordant_seeds": {
            "r3_better": [r["seed"] for r in discord_r3f["r3_better"]],
            "f_better": [r["seed"] for r in discord_r3f["f_better"]],
        },
        # rescue mechanics among B0-failed: acceptance vs fallback vs remained-wrong
        "stage2_detail": {},
    }

    for arm in ("R1", "R3", "F"):
        acc = [r for r in b0_wrong if r.get(f"{arm}_s2_accepted")]
        triggered = [r for r in per_frame if f"{arm}_s2_iters" in r]
        acc_wrong = [r for r in acc if r[f"{arm}_final_err"] > 0]
        result["stage2_detail"][arm] = {
            "triggered": len(triggered),
            "accepted": len(acc),
            "accepted_but_wrong": len(acc_wrong),
            "not_accepted_kept_b0_wrong": sum(
                1 for r in b0_wrong
                if f"{arm}_s2_iters" in r and not r.get(f"{arm}_s2_accepted")),
            "s2_iters_on_triggered": summarize(
                [r[f"{arm}_s2_iters"] for r in per_frame if f"{arm}_s2_iters" in r]),
        }

    OUT.write_text(json.dumps(result, indent=1), encoding="utf-8")

    # compact print
    print(f"counts: {result['counts']}")
    for name in ("r3_only_rescue", "both_rescued", "both_failed", "b0_correct"):
        c = result["categories"][name]
        print(f"\n[{name}] n={c['n']}")
        print(f"  mean|llr| med={c['mean_abs_llr']['median']:.2f} "
              f"[q25 {c['mean_abs_llr']['q25']:.2f}, q75 {c['mean_abs_llr']['q75']:.2f}]"
              f" | ch_hd_err med={c['ch_hd_errors']['median']:.0f} "
              f"[{c['ch_hd_errors']['q25']:.0f},{c['ch_hd_errors']['q75']:.0f}]"
              f" | B0 s1 med={c['B0_s1']['median']:.0f} s20 med={c['B0_s20']['median']:.0f}"
              f" | B0 info_err med={c['B0_info_errors']['median']:.0f}")
        print(f"  cls: {c['B0_classification']}")
    print(f"\nwrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
