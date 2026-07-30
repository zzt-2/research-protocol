# -*- coding: utf-8 -*-
"""P03 (T031) Phase A — uniform-precision baseline Pareto sweep.

For each frozen bitwidth (W,F) in {(6,4),(8,6),(10,8),(12,10),(14,12),(16,14)}
plus the float-bypass reference (64,40), evaluate decide_fp on dev seeds 0-9
across the anchor gain-bearing grid weak/moderate/strong x range(5,26,2) dB.

Per (scene, gamma, seed, bitwidth) cell we record:
  - decision_agreement_vs_float : fraction of windows where decide_fp(W,F) ==
                                  decide_fp(64,40) [== A.decide at bypass]
  - wrong_branch_regret_dB      : 10*log10(fp_selected_errors / float_selected_errors)
                                  paired per seed (>= 0; fp can only do worse
                                  because branch outputs are frozen).
  - overflow_rate               : fraction of windows where any datapath
                                  register saturated (block-float or mean_pwr).
  - op_bit_proxy / storage_bit_proxy : deterministic resource proxies (no
                                  synthesis; labelled proxy).

All bitwidths share ONE channel pass per (scene, gamma, seed) via
extra_selector, so the comparison is paired and channel-identical.

Discipline: only the selector CONTROL PATH is touched. Branch outputs (DA/NDA
common-768 errors) are the FROZEN per-window errors from run_case_multidelta;
this script never recomputes BER. delta=0 only (P03 is a bitwidth problem).
"""
import os
import sys
import json
import time
import argparse
from datetime import datetime, timezone

import numpy as np
from scipy import stats

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
sys.path[:0] = [_SIM_ROOT, os.path.join(_SIM_ROOT, 'simulator'), _HERE]

from _p01_cpr_snr_mismatch_probe import run_case_multidelta, N_WINDOWS  # noqa: E402
from _p03_fixed_point import decide_fp, selector_resource_proxy, block_float_normalise  # noqa: E402
from common import save_results  # noqa: E402

# ---- frozen bitwidth ladder (F = W - 2; 2 integer bits cover [0,4) mantissa) ----
BITWIDTHS = [(6, 4), (8, 6), (10, 8), (12, 10), (14, 12), (16, 14)]
FLOAT_BYPASS = (64, 40)

SCENES = ("weak", "moderate", "strong")
SNR_DB = tuple(map(float, range(5, 26, 2)))   # 5..25 dB step 2 (anchor grid)
DEV_SEEDS = list(range(10))                   # dev = anchor subset 0-9

OUT_DIR = os.path.join(_SIM_ROOT, "results", "p03_fixed_point_codesign")


def ci_t(data):
    a = np.asarray(data, dtype=float)
    n = len(a)
    mean = float(np.mean(a))
    std = float(np.std(a, ddof=1)) if n > 1 else 0.0
    hw = float(stats.t.ppf(0.975, n - 1)) * std / np.sqrt(n) if n > 1 else 0.0
    return mean, std, hw, mean - hw, mean + hw


def make_overflow_counting_decide(W, F):
    """Wrap decide_fp to also count per-window saturation events.

    We re-derive the block-float overflow flag from raw (cheap: just one pass
    over |raw|^2) so the regret/agreement loop stays on the fast probe path.
    The flag is recorded in a closure-captured list aligned to window index b.
    """
    state = {"overflow_flags": []}

    def fn(raw, gamma_db, gamma_lin, b):
        # cheap overflow pre-check: block-float normalise on |raw|^2 to see if
        # any register saturated. This mirrors decide_fp's internal datapath.
        pwr = np.abs(np.asarray(raw, dtype=np.complex128)) ** 2
        bf = block_float_normalise(pwr, W, F)
        of = bool(bf["overflow"]) if isinstance(bf["overflow"], list) else bool(bf["overflow"])
        # also flag mean_pwr saturation explicitly
        # (block_float_normalise already records it in overflow list)
        choice = decide_fp(raw, gamma_db, gamma_lin, W, F)
        # ensure state list length tracks b
        if len(state["overflow_flags"]) <= b:
            state["overflow_flags"].extend([False] * (b + 1 - len(state["overflow_flags"])))
        state["overflow_flags"][b] = of
        return choice

    fn.state = state
    return fn


def run_uniform_scan(seeds, tag, scenes=SCENES, snr_db=SNR_DB, bitwidths=BITWIDTHS):
    """Run the uniform bitwidth sweep; return raw_rows + per-cell aggregates.

    All bitwidths (+ float bypass) are evaluated in ONE channel pass per
    (scene, gamma, seed) via extra_selector — paired and channel-identical.
    """
    t0 = time.time()
    raw_rows = []
    total_cells = len(scenes) * len(snr_db) * len(seeds)
    done = 0
    for scene in scenes:
        for snr in snr_db:
            for seed in seeds:
                # Build extra_selector specs for ALL bitwidths + bypass.
                # bypass is the float reference (must match A.decide byte-exact).
                specs = {}
                fn_states = {}
                for (W, F) in bitwidths + [FLOAT_BYPASS]:
                    fn = make_overflow_counting_decide(W, F)
                    specs[f"fp_{W}_{F}"] = {"fn": fn, "needs_pilot": False,
                                            "needs_reset": False}
                    fn_states[(W, F)] = fn.state
                md = run_case_multidelta(scene, snr, seed, deltas=(0.0,),
                                         extra_selector=specs)
                base = md["base"]
                pw_da = base["per_window_da_err"]
                pw_nda = base["per_window_nda_err"]
                nda_common = base["fixed_nda_errors"]
                n_win = base["n_windows"]
                # float bypass selected errors (paired reference)
                bypass_key = f"fp_{FLOAT_BYPASS[0]}_{FLOAT_BYPASS[1]}"
                bypass_choices = md["per_delta_extra"][bypass_key][0.0]["choices"]
                bypass_sel = md["per_delta_extra"][bypass_key][0.0]["selected_errors"]
                for (W, F) in bitwidths + [FLOAT_BYPASS]:
                    key = f"fp_{W}_{F}"
                    pe = md["per_delta_extra"][key][0.0]
                    ch = pe["choices"]
                    fp_sel = pe["selected_errors"]
                    n_da = pe["n_select_da"]
                    n_nda = pe["n_select_nda"]
                    # agreement vs float bypass (per-window)
                    agree = sum(1 for a, b in zip(bypass_choices, ch) if a == b)
                    agree_rate = agree / n_win
                    # overflow rate (per-window saturation)
                    of_flags = fn_states[(W, F)]["overflow_flags"]
                    of_count = int(sum(1 for x in of_flags if x))
                    of_rate = of_count / n_win
                    # wrong-branch regret = errors fp paid that bypass did NOT.
                    # Per-window paired: sum over windows where fp != bypass of
                    # (fp_err - bypass_err) for that window.
                    regret_err = 0
                    for i in range(n_win):
                        if ch[i] != bypass_choices[i]:
                            fp_e = int(pw_da[i]) if ch[i] == "da" else int(pw_nda[i])
                            bp_e = int(pw_da[i]) if bypass_choices[i] == "da" else int(pw_nda[i])
                            regret_err += (fp_e - bp_e)
                    # dB regret vs bypass (>= 0). Use 10log10(fp_sel/bypass_sel).
                    if bypass_sel > 0 and fp_sel > 0:
                        regret_db = 10.0 * np.log10(fp_sel / bypass_sel)
                    elif fp_sel > 0:
                        regret_db = float("inf")
                    else:
                        regret_db = 0.0
                    # also vs per-block oracle (lower bound): how far from ideal
                    oracle_sel = int(sum(min(int(pw_da[i]), int(pw_nda[i])) for i in range(n_win)))
                    raw_rows.append({
                        "tag": tag, "scene": scene, "gamma_true_db": float(snr),
                        "seed_index": int(seed), "W": int(W), "F": int(F),
                        "bitwidth": f"({W},{F})",
                        "n_windows": int(n_win),
                        "fixed_nda_errors_common768": int(nda_common),
                        "fp_selected_errors": int(fp_sel),
                        "bypass_selected_errors": int(bypass_sel),
                        "oracle_selected_errors": int(oracle_sel),
                        "n_select_da": int(n_da), "n_select_nda": int(n_nda),
                        "decision_agreement_vs_float": float(agree_rate),
                        "wrong_branch_regret_errors": int(regret_err),
                        "wrong_branch_regret_db": float(regret_db),
                        "overflow_rate": float(of_rate),
                        "overflow_count": int(of_count),
                    })
                done += 1
            el = time.time() - t0
            print(f"  [{tag}] {scene}@{snr:.0f}dB done "
                  f"({done}/{total_cells} seed-cells, {el:.0f}s)", flush=True)
    return raw_rows


def aggregate_uniform(raw_rows, bitwidths=BITWIDTHS):
    """Per (bitwidth) pooled over all (scene, gamma, seed); plus per-cell.

    Pools wrong_branch_regret_db and decision_agreement over the dev grid.
    """
    aggs = []
    for (W, F) in bitwidths + [FLOAT_BYPASS]:
        sub = [r for r in raw_rows if r["W"] == W and r["F"] == F]
        if not sub:
            continue
        regrets = [r["wrong_branch_regret_db"] for r in sub
                   if r["wrong_branch_regret_db"] != float("inf")]
        agrees = [r["decision_agreement_vs_float"] for r in sub]
        overflows = [r["overflow_rate"] for r in sub]
        m_r, s_r, _, lo_r, hi_r = ci_t(regrets) if regrets else (float("nan"),)*5
        m_a, s_a, _, lo_a, hi_a = ci_t(agrees)
        m_o, s_o, _, lo_o, hi_o = ci_t(overflows)
        # resource proxy (deterministic, same for every window at this W,F)
        rp = selector_resource_proxy(W, F, n=256)
        # count cells with ANY regret > 0 (decision flips causing extra errors)
        n_flip_cells = int(sum(1 for r in sub if r["wrong_branch_regret_errors"] > 0))
        aggs.append({
            "W": int(W), "F": int(F), "bitwidth": f"({W},{F})",
            "n_cells": int(len(sub)),
            "regret_db_mean": float(m_r), "regret_db_std": float(s_r),
            "regret_db_ci95": [float(lo_r), float(hi_r)],
            "decision_agreement_mean": float(m_a),
            "decision_agreement_ci95": [float(lo_a), float(hi_a)],
            "overflow_rate_mean": float(m_o), "overflow_rate_ci95": [float(lo_o), float(hi_o)],
            "n_cells_with_regret": n_flip_cells,
            "op_bit_proxy": int(rp["op_bit_proxy"]),
            "storage_bit_proxy": int(rp["storage_bit_proxy"]),
            "W_acc": int(rp["W_acc"]),
            "max_regret_db": float(max(regrets)) if regrets else 0.0,
        })
    return aggs


def per_cell_aggregate(raw_rows, bitwidths=BITWIDTHS):
    """Per (scene, gamma, bitwidth) — for the tension diagnosis."""
    out = []
    for scene in SCENES:
        for snr in SNR_DB:
            for (W, F) in bitwidths + [FLOAT_BYPASS]:
                sub = [r for r in raw_rows if r["scene"] == scene
                       and abs(r["gamma_true_db"] - snr) < 1e-9
                       and r["W"] == W and r["F"] == F]
                if not sub:
                    continue
                regrets = [r["wrong_branch_regret_db"] for r in sub
                           if r["wrong_branch_regret_db"] != float("inf")]
                agrees = [r["decision_agreement_vs_float"] for r in sub]
                overflows = [r["overflow_rate"] for r in sub]
                m_r = float(np.mean(regrets)) if regrets else float("nan")
                out.append({
                    "scene": scene, "gamma_true_db": float(snr),
                    "W": int(W), "F": int(F),
                    "regret_db_mean": m_r,
                    "decision_agreement_mean": float(np.mean(agrees)),
                    "overflow_rate_mean": float(np.mean(overflows)),
                    "n_seeds": int(len(sub)),
                })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="dev")
    ap.add_argument("--seeds", type=int, nargs="+", default=DEV_SEEDS)
    ap.add_argument("--out", default=os.path.join(OUT_DIR, "phaseA_uniform.json"))
    a = ap.parse_args()
    os.makedirs(OUT_DIR, exist_ok=True)

    t0 = time.time()
    print(f"Phase A uniform sweep [{a.tag}] seeds={a.seeds} "
          f"bitwidths={BITWIDTHS} + bypass{FLOAT_BYPASS}\n"
          f"  grid: {SCENES} x {SNR_DB} = {len(SCENES)*len(SNR_DB)} cells x "
          f"{len(a.seeds)} seeds = {len(SCENES)*len(SNR_DB)*len(a.seeds)} "
          f"seed-cells, all bitwidths in ONE channel pass each")
    raw_rows = run_uniform_scan(a.seeds, a.tag)
    aggregates = aggregate_uniform(raw_rows)
    per_cell = per_cell_aggregate(raw_rows)
    elapsed = time.time() - t0

    # ---- print the Pareto table ----
    print(f"\n{'='*100}")
    print(f"Phase A uniform-precision Pareto [{a.tag}] (pooled over "
          f"{len(SCENES)*len(SNR_DB)*len(a.seeds)} seed-cells)")
    print(f"{'-'*100}")
    print(f"{'bitwidth':<10}{'agree%':>8}{'regret_dB':>11}{'[CI95]':>16}"
          f"{'overflow%':>11}{'op×bit':>9}{'storage':>9}{'W_acc':>7}")
    print(f"{'-'*100}")
    for ag in aggregates:
        ci = ag["regret_db_ci95"]
        print(f"{ag['bitwidth']:<10}{ag['decision_agreement_mean']*100:>7.3f}%"
              f"{ag['regret_db_mean']:>+10.4f}[{ci[0]:+.3f},{ci[1]:+.3f}]"
              f"{ag['overflow_rate_mean']*100:>10.3f}%"
              f"{ag['op_bit_proxy']:>9}{ag['storage_bit_proxy']:>9}"
              f"{ag['W_acc']:>7}")
    print(f"{'='*100}")

    out = {
        "package": "P03",
        "task": "T031-p03-fixed-point-resource-codesign",
        "phase": "A_uniform_baseline",
        "tag": a.tag,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "bitwidths": [list(bw) for bw in BITWIDTHS],
        "float_bypass": list(FLOAT_BYPASS),
        "scenes": list(SCENES), "snr_db": list(SNR_DB),
        "dev_seeds": list(a.seeds), "deltas": [0.0],
        "resource_proxy_note": (
            "op_bit_proxy and storage_bit_proxy are DETERMINISTIC operand-bit / "
            "register-bit sums. NO real synthesis, LUT, DSP, power, or area "
            "measurement was performed."
        ),
        "aggregates": aggregates,
        "per_cell": per_cell,
        "raw_rows": raw_rows,
        "elapsed_s": float(elapsed),
    }
    save_results(out, a.out, os.path.basename(__file__))
    print(f"[saved] {a.out} ({elapsed:.0f}s)")


if __name__ == "__main__":
    main()
