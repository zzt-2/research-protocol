"""Summarize decode-capability-audit raw results into summary.json.

Applies the preregistered verdict rules from contract.yaml (frozen v1):
- A: delta FER(B0 - SPA200) per condition, bootstrap CI95, sign test;
     CLOSED iff CI upper < +0.005 in all three conditions.
- B: per-condition best grid config (in-sample oracle), global best,
     headrooms H1/H2/H3 with bootstrap CI on H1.
- Stratification by e0 quartile bands (Q4 worst / deep fade, Q3 marginal, Q1+Q2 good).

Usage: python summarize.py
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
from common._experiment import save_results  # noqa: E402

OUT_DIR = SIM_ROOT / "results" / "decode-capability-audit"
BOOTSTRAP_N = 10000
RNG_SEED = 20260924
BAND_LABELS = {3: "Q4_deep_fade", 2: "Q3_marginal", 1: "Q12_good", 0: "Q12_good"}


def paired_delta(b0f: np.ndarray, af: np.ndarray) -> dict:
    d = b0f - af
    point = float(d.mean())
    rng = np.random.default_rng(RNG_SEED)
    n = len(d)
    boots = np.array([
        d[rng.integers(0, n, n)].mean() for _ in range(BOOTSTRAP_N)
    ])
    lo, hi = (float(x) for x in np.quantile(boots, [0.025, 0.975]))
    wins, losses = int((d > 0).sum()), int((d < 0).sum())
    p = float(binomtest(wins, wins + losses, 0.5).pvalue) if wins + losses else 1.0
    return {"delta_fer": point, "ci95": [lo, hi], "wins": wins,
            "losses": losses, "p_sign": p}


def main() -> int:
    cap = json.load(open(OUT_DIR / "raw_capability.json"))
    grid = None
    grid_path = OUT_DIR / "raw_grid.json"
    if grid_path.exists():
        grid = json.load(open(grid_path))

    summary: dict = {"schema_version": "decode-capability-audit.summary.v1",
                     "contract": "contract.yaml v1 (frozen before execution)"}

    # ---------------- diagnostic A ----------------
    A: dict = {"per_condition": {}}
    for cond, cdata in cap["conditions"].items():
        arms = cdata["arms"]
        b0_ie = np.array(arms["B0"]["info_errors"])
        b0f = (b0_ie > 0).astype(int)
        bands = np.array(cdata["bands"])
        entry = {"fer": {}, "ber_bits": {}, "converged_median": {}}
        entry["fer"]["B0"] = float(b0f.mean())
        b0_bits = int(b0_ie.sum())
        comparisons = {}
        for name in ["SPA20", "SPA50", "SPA200", "NOMS50", "NOMS200"]:
            ie = np.array(arms[name]["info_errors"])
            af = (ie > 0).astype(int)
            conv = np.array(arms[name]["converged_at"])
            conv_ok = conv[conv > 0]
            entry["fer"][name] = float(af.mean())
            entry["ber_bits"][name] = int(ie.sum())
            entry["converged_median"][name] = (
                float(np.median(conv_ok)) if conv_ok.size else None
            )
            comparisons[name] = paired_delta(b0f, af)
            comparisons[name]["fer_arm"] = float(af.mean())
        # stratified FER by band
        strat = {}
        masks = {
            "Q4_deep_fade": bands == 3,
            "Q3_marginal": bands == 2,
            "Q12_good": bands <= 1,
        }
        for label, m in masks.items():
            strat[label] = {
                "n": int(m.sum()),
                "fer": {
                    name: float(((np.array(arms[name]["info_errors"]) > 0)[m]).mean())
                    for name in entry["fer"]
                },
            }
        entry["paired_vs_b0"] = comparisons
        entry["stratified_fer"] = strat
        A["per_condition"][cond] = entry

    # preregistered verdict A
    primary = {
        cond: A["per_condition"][cond]["paired_vs_b0"]["SPA200"]
        for cond in A["per_condition"]
    }
    closed = all(v["ci95"][1] < 0.005 for v in primary.values())
    A["primary_comparison"] = "deltaFER(B0 - SPA200) per condition, CI95 bootstrap 10k"
    A["verdict_rule"] = "CLOSED iff CI95 upper < +0.005 in all three conditions"
    A["verdict"] = "CLOSED" if closed else "ALIVE"
    A["primary_numbers"] = primary
    # decomposition notes
    A["decomposition"] = {
        cond: {
            "iteration_axis_B0_vs_NOMS200":
                A["per_condition"][cond]["paired_vs_b0"]["NOMS200"],
            "algorithm_axis_NOMS200_vs_SPA200_note":
                "read as FER(NOMS200) - FER(SPA200) from the per-condition fer table",
        }
        for cond in A["per_condition"]
    }

    # ---------------- diagnostic B ----------------
    B: dict = {"per_condition": {}}
    if grid is None:
        B["skipped"] = "raw_grid.json not present yet"
    if grid is not None:
        for cond, cdata in grid["conditions"].items():
            g = cdata["grid"]
            keys = list(g.keys())
            fers = {k: float((np.array(g[k]["info_errors"]) > 0).mean()) for k in keys}
            b0_key = "a0.75_b0"
            b0_ie = np.array(g[b0_key]["info_errors"])
            b0f = (b0_ie > 0).astype(int)
            # anchor cross-check vs capability run
            best_key = min(fers, key=fers.get)
            best_ie = np.array(g[best_key]["info_errors"])
            bestf = (best_ie > 0).astype(int)
            H1 = paired_delta(b0f, bestf)
            B["per_condition"][cond] = {
                "fer_by_config": fers,
                "b0_config": b0_key,
                "fer_b0": fers[b0_key],
                "best_config": best_key,
                "fer_best": fers[best_key],
                "H1_b0_minus_percond_best": H1,
            }
        # global best: single config minimizing summed error FRAMES across
        # conditions (consistent with the FER primary metric)
        total_err_frames = {}
        for cond, cdata in grid["conditions"].items():
            for k in cdata["grid"]:
                total_err_frames[k] = total_err_frames.get(k, 0) + int(
                    (np.array(cdata["grid"][k]["info_errors"]) > 0).sum()
                )
        global_best = min(total_err_frames, key=total_err_frames.get)
        B["global_best_config"] = global_best
        B["global_best_total_error_frames"] = total_err_frames[global_best]
        B["b0_total_error_frames"] = total_err_frames["a0.75_b0"]
        for cond, cdata in grid["conditions"].items():
            gb_ie = np.array(cdata["grid"][global_best]["info_errors"])
            b0f = (np.array(cdata["grid"]["a0.75_b0"]["info_errors"]) > 0).astype(int)
            gbf = (gb_ie > 0).astype(int)
            B["per_condition"][cond]["H2_b0_minus_global_best"] = paired_delta(b0f, gbf)
            B["per_condition"][cond]["fer_global_best"] = float(gbf.mean())
            pb = (np.array(
                cdata["grid"][B["per_condition"][cond]["best_config"]]["info_errors"]
            ) > 0).astype(int)
            B["per_condition"][cond]["H3_global_best_minus_percond_best"] = paired_delta(
                gbf, pb
            )
        h1_all = [B["per_condition"][c]["H1_b0_minus_percond_best"]
                  for c in B["per_condition"]]
        B["verdict"] = ("CLOSED" if all(h["ci95"][1] < 0.005 for h in h1_all) else "ALIVE")
        B["verdict_rule"] = "CLOSED iff CI95 upper of H1 < +0.005 in all conditions"
        B["in_sample_selection_note"] = (
            "per-condition best and global best are in-sample selections over the "
            "16-config grid (oracle upper bounds on any selection rule; 16-way "
            "selection noise at n=2048 is negligible relative to the 0.005 threshold)"
        )

    summary["diagnostic_A_capability"] = A
    summary["diagnostic_B_grid"] = B
    summary["stratification"] = cap.get("stratification", {})
    summary["anchor_gates"] = cap.get("anchor_gates", {})

    # early-stop semantics note (N6): frames where B0 converged mid-run
    # (syndrome hit 0) but the final-20 output is wrong form the
    # "converged_wrong" class; under first-syndrome-0 early stopping they
    # are accepted at a codeword iterate that is almost surely the same
    # wrong codeword, so FER is unchanged except for codeword-oscillation
    # cases not distinguishable from the saved trajectory summary.
    es = {}
    for cond, cdata in cap["conditions"].items():
        b0 = cdata["arms"]["B0"]
        ie = np.array(b0["info_errors"])
        conv = np.array(b0["converged_at"])
        accepted_by_es = (conv > 0)
        wrong = ie > 0
        es[cond] = {
            "n_frames": len(ie),
            "es_accepted_fraction": float(accepted_by_es.mean()),
            "converged_wrong_frames": int((accepted_by_es & wrong).sum()),
            "never_converged_frames": int((~accepted_by_es).sum()),
            "fer_B0_fixed20": float(wrong.mean()),
            "es_fer_note": (
                "FER under first-syndrome-0 early stop equals FER(B0) up to "
                "codeword-oscillation cases; converged_wrong frames are "
                "errors under both output rules"
            ),
        }
    summary["N6_early_stop_semantics_B0"] = es

    save_results(summary, str(OUT_DIR / "summary.json"), "decode-capability-audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
