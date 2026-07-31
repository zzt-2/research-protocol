# -*- coding: utf-8 -*-
"""P07 (family F) Phase B/C — conventional AGC + method factory (BATCHED + MP).

ONLY run because Phase A established the problem (fixed-gain regret
+0.91~+1.03 dB across 6/8/10 bit, 14-15/15 cells pass).

Phase B: conventional AGCs (causal RMS / peak-hold / log-domain).
Phase C: 4 mechanism-distinct candidates (dual-tc / clipping-aware /
robust-pct / hysteretic).

Strategy (single MP pass per seed-set):
  1. dev-tune: for each AGC family, evaluate ALL its dev configs on the dev
     grid (weak/strong x 5 SNR x dev seeds 0-4), pick best params per bitwidth.
  2. held-out: evaluate the best config of EVERY family (conventional +
     candidate) on the held-out grid (3 scenes x 5 SNR x seeds 30-34), paired
     with ideal-float reference in the SAME channel pass.

Both passes use _p07_batch.eval_cell_agc (one channel-gen per cell, all AGC
families on identical channel). paired_regret_dB = 10log10(sel/ideal_sel).

Frozen (FROZEN_CONTRACT §5,§6): dev seeds 0-4, held-out 30-34, dev-tune only
on dev, MDE=0.15, METHOD_SIGNAL needs ALL checks + cross-bitwidth consistent.
"""
import os
import sys
import json
import time
import itertools
from multiprocessing import Pool

import numpy as np
from scipy import stats

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
sys.path[:0] = [_SIM_ROOT, os.path.join(_SIM_ROOT, 'simulator'), _HERE]

import _p07_adapters as AD  # noqa: E402
import _p07_batch as BATCH  # noqa: E402
from common import save_results  # noqa: E402

SCENES = ("weak", "moderate", "strong")
SNR_DB = (5.0, 9.0, 13.0, 17.0, 21.0)
DEV_SEEDS = (0, 1, 2)
HELDOUT_SEEDS = (30, 31, 32, 33, 34)
BITWIDTHS = AD.BITWIDTHS
MDE = 0.15
N_WORKERS = min(24, os.cpu_count() or 8)
FS = AD.FS

OUT_DIR = os.path.join(_SIM_ROOT, "results", "p07_agc_adc_dynamic_range")
DEV_SCENES = ("weak", "strong")   # dev-tune on representative subset
DEV_SNR = (5.0, 13.0, 21.0)       # dev-tune SNR subset (3 points spanning low/high)

# Conventional AGC dev search — 3 diverse configs per family (frozen, FAIR budget).
CONV_SEARCH = {
    "causal_rms": [{"target_rms": 0.2, "lam": 0.9},
                   {"target_rms": 0.3, "lam": 0.9},
                   {"target_rms": 0.4, "lam": 0.9}],
    "peak_hold": [{"target_peak": 0.6, "release": 0.95},
                  {"target_peak": 0.8, "release": 0.95},
                  {"target_peak": 0.9, "release": 0.95}],
    "log_domain": [{"target_rms": 0.2, "lam": 0.9},
                   {"target_rms": 0.3, "lam": 0.9},
                   {"target_rms": 0.4, "lam": 0.9}],
}
# Candidate dev search — 3 diverse configs per family (frozen, mechanism-spanning).
CAND_SEARCH = {
    "dual_tc": [{"target_rms": 0.3, "lam_attack": 0.5, "lam_release": 0.95},
                {"target_rms": 0.3, "lam_attack": 0.3, "lam_release": 0.97},
                {"target_rms": 0.4, "lam_attack": 0.5, "lam_release": 0.97}],
    "clipping_aware": [{"target_rms": 0.3, "lam": 0.9, "rail_frac_thresh": 0.02, "backoff": 0.5},
                       {"target_rms": 0.3, "lam": 0.9, "rail_frac_thresh": 0.05, "backoff": 0.7},
                       {"target_rms": 0.4, "lam": 0.95, "rail_frac_thresh": 0.02, "backoff": 0.5}],
    "robust_pct": [{"target_pct": 0.3, "percentile": 60, "lam": 0.9},
                   {"target_pct": 0.3, "percentile": 75, "lam": 0.9},
                   {"target_pct": 0.3, "percentile": 90, "lam": 0.9}],
    "hysteretic": [{"high_gain": 2.0, "low_gain": 0.5, "rms_hi": 0.4, "rms_lo": 0.2, "hyst_lo": 2, "hyst_hi": 2},
                   {"high_gain": 1.5, "low_gain": 0.4, "rms_hi": 0.35, "rms_lo": 0.15, "hyst_lo": 2, "hyst_hi": 2},
                   {"high_gain": 2.0, "low_gain": 0.4, "rms_hi": 0.35, "rms_lo": 0.2, "hyst_lo": 2, "hyst_hi": 2}],
}
CONV_CLS = AD.CONVENTIONAL_AGCS
CAND_CLS = AD.CANDIDATE_AGCS


def _to_jsonable(o):
    """Recursively convert numpy scalar types to plain Python for JSON."""
    import numpy as _np
    if isinstance(o, dict):
        return {k: _to_jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_to_jsonable(x) for x in o]
    if isinstance(o, _np.generic):
        return o.item()
    return o


def ci_t(data):
    a = np.asarray(data, dtype=float)
    n = len(a)
    mean = float(np.mean(a)) if n else float("nan")
    std = float(np.std(a, ddof=1)) if n > 1 else 0.0
    hw = float(stats.t.ppf(0.975, n - 1)) * std / np.sqrt(n) if n > 1 else 0.0
    return {"mean": mean, "std": std, "hw": hw, "ci_lo": mean - hw, "ci_hi": mean + hw, "n": n}


# ---- worker: tune all families on one dev cell ----
def _dev_worker(args):
    """Evaluate ALL dev configs of ALL families (conv + cand) on one dev cell,
    across all bitwidths. Returns {family|params_str|W: regret}."""
    scene, g, seed = args
    out = {}
    for W in BITWIDTHS:
        # build specs: every (family, params) pair as its own AGC
        specs = []
        for fam, search in {**CONV_SEARCH, **CAND_SEARCH}.items():
            cls = CONV_CLS[fam] if fam in CONV_CLS else CAND_CLS[fam]
            for params in search:
                tag = f"{fam}|{json.dumps(params, sort_keys=True)}|W{W}"
                specs.append((tag, (lambda c=cls, p=params: c(**p))))
        res = BATCH.eval_cell_agc(scene, g, seed, specs, W, FS)
        # ideal-float ref
        idl = BATCH.eval_cell_fixed_gains(
            scene, g, seed,
            [{"gain": 1.0, "W": AD.FLOAT_BYPASS_W, "fs": AD.FLOAT_BYPASS_FS,
              "tag": "ideal_float"}])["ideal_float"]
        idl_sel = idl["selected_errors"]
        for tag, r in res.items():
            sel = r["selected_errors"]
            regret = 10.0 * np.log10(sel / idl_sel) if idl_sel > 0 else 0.0
            out[tag] = {"regret": float(regret),
                        "selected_errors": int(sel),
                        "ideal_sel": int(idl_sel),
                        "scene": scene, "g": float(g), "seed": int(seed), "W": int(W)}
    return out


def _heldout_worker(args):
    """Evaluate the best config of every family on one held-out cell, paired
    with ideal-float in the same channel. best_params passed in."""
    scene, g, seed, best_params_by_fam = args
    out = {}
    for W in BITWIDTHS:
        specs = []
        for fam in list(CONV_SEARCH) + list(CAND_SEARCH):
            params = best_params_by_fam[fam][str(W)]
            cls = CONV_CLS[fam] if fam in CONV_CLS else CAND_CLS[fam]
            tag = f"{fam}|W{W}"
            specs.append((tag, (lambda c=cls, p=params: c(**p))))
        res = BATCH.eval_cell_agc(scene, g, seed, specs, W, FS)
        idl = BATCH.eval_cell_fixed_gains(
            scene, g, seed,
            [{"gain": 1.0, "W": AD.FLOAT_BYPASS_W, "fs": AD.FLOAT_BYPASS_FS,
              "tag": "ideal_float"}])["ideal_float"]
        idl_sel = idl["selected_errors"]
        for tag, r in res.items():
            sel = r["selected_errors"]
            regret = 10.0 * np.log10(sel / idl_sel) if idl_sel > 0 else 0.0
            out[f"{tag}|{scene}|{g:g}|{seed}"] = {
                "regret": float(regret), "selected_errors": int(sel),
                "ideal_sel": int(idl_sel), "clipping": float(r["mean_clipping_rate"]),
                "scene": scene, "g": float(g), "seed": int(seed),
                "fam": tag.split("|")[0], "W": int(W)}
    return out


def main():
    t0 = time.time()
    # ---- Phase B/C dev-tune (MP) ----
    dev_tasks = [(sc, g, seed)
                 for sc in DEV_SCENES for g in DEV_SNR for seed in DEV_SEEDS]
    print(f"Phase B/C dev-tune: {len(dev_tasks)} cells x "
          f"({len(CONV_SEARCH)+len(CAND_SEARCH)} families x dev configs) ...", flush=True)
    dev_results = {}
    with Pool(N_WORKERS) as pool:
        for i, res in enumerate(pool.imap_unordered(_dev_worker, dev_tasks)):
            for k, v in res.items():
                dev_results.setdefault(k, []).append(v)
            if (i + 1) % 10 == 0:
                print(f"  dev {i+1}/{len(dev_tasks)} ({round(time.time()-t0,1)}s)", flush=True)
    print(f"  dev-tune done ({round(time.time()-t0,1)}s)", flush=True)

    # pick best params per family per bitwidth (min mean regret on dev)
    best_params = {}
    for fam in list(CONV_SEARCH) + list(CAND_SEARCH):
        best_params[fam] = {}
        for W in BITWIDTHS:
            best_p = None
            best_mean = float("inf")
            for params in ({**CONV_SEARCH, **CAND_SEARCH})[fam]:
                tag = f"{fam}|{json.dumps(params, sort_keys=True)}|W{W}"
                regrets = [r["regret"] for r in dev_results.get(tag, [])]
                m = float(np.mean(regrets)) if regrets else float("inf")
                if m < best_mean:
                    best_mean = m
                    best_p = params
            best_params[fam][str(W)] = best_p
    print(f"  best params selected ({round(time.time()-t0,1)}s)", flush=True)

    # ---- held-out eval (MP) ----
    held_tasks = [(sc, g, seed, best_params)
                  for sc in SCENES for g in SNR_DB for seed in HELDOUT_SEEDS]
    print(f"Phase B/C held-out: {len(held_tasks)} cells ...", flush=True)
    heldout = {}
    with Pool(N_WORKERS) as pool:
        for i, res in enumerate(pool.imap_unordered(_heldout_worker, held_tasks)):
            heldout.update(res)
            if (i + 1) % 10 == 0:
                print(f"  heldout {i+1}/{len(held_tasks)} ({round(time.time()-t0,1)}s)", flush=True)
    print(f"  held-out done ({round(time.time()-t0,1)}s)", flush=True)

    # aggregate: per-family per-bitwidth pooled regret on held-out
    agg = {}
    for fam in list(CONV_SEARCH) + list(CAND_SEARCH):
        for W in BITWIDTHS:
            rows = [v for k, v in heldout.items()
                    if v["fam"] == fam and v["W"] == W]
            agg[f"{fam}|W{W}"] = ci_t([r["regret"] for r in rows])

    # strongest conventional per bitwidth
    strongest_conv = {}
    for W in BITWIDTHS:
        cands = {f: agg[f"{f}|W{W}"]["mean"] for f in CONV_SEARCH}
        best = min(cands, key=cands.get)
        strongest_conv[f"W{W}"] = {"name": best, "regret_ci": agg[f"{best}|W{W}"]}

    # Phase B gate: strongest conv recovers regret < MDE across bitwidths
    conv_resolves = all(strongest_conv[f"W{W}"]["regret_ci"]["mean"] < MDE
                        for W in BITWIDTHS)

    # Phase C: paired delta (cand - strongest-conv) per cell; positive => cand better
    cand_agg = {}
    signal_checks = {}
    for W in BITWIDTHS:
        sname = strongest_conv[f"W{W}"]["name"]
        conv_by_cell = {(v["scene"], v["g"], v["seed"]): v["regret"]
                        for k, v in heldout.items()
                        if v["fam"] == sname and v["W"] == W}
        for fam in CAND_SEARCH:
            deltas = []
            for k, v in heldout.items():
                if v["fam"] == fam and v["W"] == W:
                    key = (v["scene"], v["g"], v["seed"])
                    if key in conv_by_cell:
                        deltas.append(conv_by_cell[key] - v["regret"])
            ci = ci_t(deltas)
            cand_agg[f"{fam}|W{W}"] = ci
            signal_checks[f"{fam}|W{W}"] = {
                "beats_conv_mean_ge_mde": ci["mean"] >= MDE,
                "ci_lo_gt_0": ci["ci_lo"] > 0}

    best_cand_per_W = {}
    for W in BITWIDTHS:
        cands = {f: cand_agg[f"{f}|W{W}"]["mean"] for f in CAND_SEARCH}
        best = max(cands, key=cands.get)
        best_cand_per_W[f"W{W}"] = {"name": best, "delta_ci": cand_agg[f"{best}|W{W}"]}
    cross_consistent = all(
        best_cand_per_W[f"W{W}"]["delta_ci"]["mean"] >= MDE
        and best_cand_per_W[f"W{W}"]["delta_ci"]["ci_lo"] > 0
        for W in BITWIDTHS)

    # terminal verdict
    if conv_resolves:
        verdict = "PROBLEM_RESOLVED_BY_CONVENTIONAL_AGC"
    elif cross_consistent:
        verdict = "DIAGNOSTIC_METHOD_SIGNAL"
    else:
        verdict = "NO_DIAGNOSTIC_METHOD_SIGNAL"

    out = {
        "package": "P07", "family": "F_AGC_ADC_DYNAMIC_RANGE_UNDER_GG",
        "phase": "BC",
        "frozen": {"MDE": MDE, "bitwidths": list(BITWIDTHS),
                   "dev_seeds": list(DEV_SEEDS),
                   "heldout_seeds": list(HELDOUT_SEEDS),
                   "dev_snr_grid": list(SNR_DB), "fs": FS,
                   "n_workers": N_WORKERS},
        "phase_B_conventional_agg": agg,
        "phase_B_strongest_conv_per_bitwidth": strongest_conv,
        "phase_B_conv_resolves": conv_resolves,
        "phase_B_best_params": {f: best_params[f] for f in CONV_SEARCH},
        "phase_C_candidate_delta_agg": cand_agg,
        "phase_C_signal_checks": signal_checks,
        "phase_C_best_candidate_per_bitwidth": best_cand_per_W,
        "phase_C_best_params": {f: best_params[f] for f in CAND_SEARCH},
        "phase_C_cross_consistent": cross_consistent,
        "heldout_rows": list(heldout.values()),
        "dev_best_per_family": {f: best_params[f] for f in list(CONV_SEARCH)+list(CAND_SEARCH)},
        "terminal_verdict": verdict,
        "elapsed_s": round(time.time() - t0, 1),
    }
    os.makedirs(OUT_DIR, exist_ok=True)
    out = _to_jsonable(out)
    save_results(out, os.path.join(OUT_DIR, "p07_phaseBC.json"), "_p07_phaseBC.py")
    summary = {
        "terminal_verdict": verdict,
        "phase_B_conv_resolves": conv_resolves,
        "phase_B_strongest_conv": {str(W): strongest_conv[f"W{W}"] for W in BITWIDTHS},
        "phase_C_cross_consistent": cross_consistent,
        "phase_C_best_candidate": {str(W): best_cand_per_W[f"W{W}"] for W in BITWIDTHS},
        "elapsed_s": out["elapsed_s"],
    }
    print(json.dumps(summary, indent=2, default=str))
    return out


if __name__ == "__main__":
    main()
