# -*- coding: utf-8 -*-
"""P07-R — Phase B (conventional comparators) + Phase C (candidates), fresh held-out.

Only run if Phase A establishes the problem (D046 terminal-state gate).

Frozen BEFORE reading B/C results (FROZEN_CONTRACT §5,§6; D046):
  - Strongest conventional comparator = corrected gain-aware causal-RMS AGC.
  - held-out seeds 500-519 (20 seeds, FRESH, disjoint from dev 300-309 and all
    campaign history 0-99/200-239).
  - MDE = 0.15 dB; METHOD_SIGNAL requires candidate strictly beats strongest
    conventional on held-out, gap >= MDE, paired CI not crossing 0, direction
    consistent across bitwidths/rho, ablation supports the mechanism.

Conventional AGCs (corrected, gain-aware): causal_rms / attack_release / log_domain.
Candidates (max 3, mechanism-distinct): censored_moment / upper_quantile / two_range_pga.
Cheap alternatives: dev-tuned fixed gain + de-gain; two-level gain hysteresis.
Oracle per-block gain: headroom/Kill bound ONLY (TL-32/FR-25), never a Go gate.

Terminal verdict (D046 §VII):
  A problem_absent_after_gain_calibration
  B problem_resolved_by_corrected_conventional_agc
  C problem survives + oracle headroom -> candidate construction
  D execution_invalid
"""
import os
import sys
import json
import time
from multiprocessing import Pool

import numpy as np
from scipy import stats

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
sys.path[:0] = [_SIM_ROOT, os.path.join(_SIM_ROOT, 'simulator'), _HERE]

import p07r_adapters as AD  # noqa: E402
import p07r_runner as R  # noqa: E402
from common import save_results  # noqa: E402

SCENES = ("weak", "moderate", "strong")
SNR_DB = (5.0, 9.0, 13.0, 17.0, 21.0)
HELDOUT_SEEDS = tuple(range(500, 520))
BITWIDTHS = AD.BITWIDTHS
F_G_LEVELS = R.F_G_LEVELS
MDE = 0.15
N_WORKERS = min(24, os.cpu_count() or 8)

OUT_DIR = os.path.join(_SIM_ROOT, "results", "p07r_agc_adc_repair")
OUT_BC = os.path.join(OUT_DIR, "p07r_phaseBC_heldout.json")

# Pre-registered 3-config dev sets per family (FROZEN a priori).
CONV_CONFIGS = {
    "causal_rms": [dict(target_rms=t, lam=l) for t in (0.2, 0.3, 0.4) for l in (0.8, 0.9, 0.95)][:3],
    "attack_release": [dict(target_peak=t, attack=a, release=r)
                       for t in (0.6, 0.8, 1.0) for a in (0.3, 0.5) for r in (0.9, 0.95)][:3],
    "log_domain": [dict(target_rms=t, lam=l) for t in (0.2, 0.3, 0.4) for l in (0.8, 0.9, 0.95)][:3],
}
CAND_CONFIGS = {
    "censored_moment": [dict(target_rms=t, lam=l) for t in (0.2, 0.3, 0.4) for l in (0.8, 0.9, 0.95)][:3],
    "upper_quantile": [dict(target_quantile=q, target_frac_fs=f, lam=l)
                       for q in (0.95, 0.99) for f in (0.6, 0.8) for l in (0.9,)][:3],
    "two_range_pga": [dict(high_gain=h, low_gain=lo, q_hi=qh, q_lo=ql)
                      for h in (1.5, 2.0) for lo in (0.5, 0.75) for qh in (0.4, 0.5) for ql in (0.2, 0.3)][:3],
}


def ci_t(data):
    a = np.asarray(data, dtype=float)
    n = len(a)
    mean = float(np.mean(a)) if n else float("nan")
    std = float(np.std(a, ddof=1)) if n > 1 else 0.0
    hw = float(stats.t.ppf(0.975, n - 1)) * std / np.sqrt(n) if n > 1 else 0.0
    return {"mean": mean, "std": std, "hw": hw, "ci_lo": mean - hw,
            "ci_hi": mean + hw, "n": n}


def _eval_agc_set(wins, gamma_db, agc_factory_list, W, fs=AD.FS, decomp="full_adc"):
    """Evaluate a list of (tag, factory) AGCs on one shared trajectory."""
    out = {}
    for tag, fac in agc_factory_list:
        agc = fac()
        out[tag] = R.eval_cell_agc(wins, gamma_db, agc, fs, W, decomp=decomp)
    return out


def _worker_bc(args):
    """One held-out cell: eval ideal_float + strongest-conv + candidates + oracle."""
    scene, g, fG, seed, best_conv_tags, best_cand_tags, dev_gains = args
    wins, _ = R.make_trajectory(scene, g, fG, seed)
    gl_true = 10.0 ** (g / 10.0)
    rows = []
    # ideal_float reference (scale_only g=1)
    cfg_idl = [{"gain": 1.0, "W": AD.FLOAT_BYPASS_W, "fs": AD.FLOAT_BYPASS_FS,
                "decomp": "scale_only", "tag": "ideal_float"}]
    idl = R.eval_cell_fixed_gains(wins, g, cfg_idl)["ideal_float"]["selected_errors"]
    # dev-tuned fixed gain (cheap alternative) per W
    for W in BITWIDTHS:
        # oracle per-block gain (headroom/Kill bound ONLY): picks g minimizing
        # per-window errors from the PAST (causal, receiver-visible via past errs)
        # implemented as: best fixed gain chosen with full hindsight -> upper bound
        # NOT used as Go gate (TL-32). We compute it as a headroom reference.
        oracle_g = _oracle_perblock_gain(wins, g, W)
        # build AGC set: strongest conv + candidates + fixed(dev) + oracle
        agcs = []
        for name, cfg in best_conv_tags.items():
            cls = AD.CONVENTIONAL_AGCS[name]
            agcs.append((f"conv_{name}", lambda c=cfg, k=cls: k(**c)))
        for name, cfg in best_cand_tags.items():
            cls = AD.CANDIDATE_AGCS[name]
            agcs.append((f"cand_{name}", lambda c=cfg, k=cls: k(**c)))
        agcs.append((f"fixed_dev_{dev_gains[W]:g}",
                     lambda gg=dev_gains[W]: AD.FixedGainAGC(gain=gg)))
        agcs.append(("oracle_perblock",
                     lambda og=oracle_g: AD.FixedGainAGC(gain=og)))
        res = _eval_agc_set(wins, g, agcs, W)
        for tag, r in res.items():
            sel = r["selected_errors"]
            regret = 10.0 * np.log10(sel / idl) if idl > 0 else 0.0
            rows.append({"scene": scene, "gamma_true_db": float(g), "f_G": float(fG),
                         "seed": int(seed), "W": int(W), "tag": tag,
                         "selected_errors": int(sel),
                         "ideal_float_selected_errors": int(idl),
                         "clipping_rate": float(r["mean_clipping_rate"]),
                         "mean_gain": float(r["mean_gain"]),
                         "paired_regret_dB": float(regret)})
    return rows


def _oracle_perblock_gain(wins, gamma_db, W, fs=AD.FS):
    """Oracle per-block gain: the fixed gain (from ladder) minimizing total
    selected_errors over the trajectory WITH FULL HINDSIGHT. Headroom/Kill bound
    ONLY — never enters a deployable decide (TL-32/FR-25).

    NOTE: this is a per-TRAJECTORY best fixed gain (upper bound on what any
    causal AGC could achieve with perfect future knowledge). It is NOT a per-
    sample/per-block oracle; it is the strongest Kill reference.
    """
    best_g, best_sel = 1.0, None
    for g in AD.FIXED_GAIN_LADDER:
        cfgs = [{"gain": g, "W": W, "fs": fs, "decomp": "full_adc", "tag": "x"}]
        sel = R.eval_cell_fixed_gains(wins, gamma_db, cfgs)["x"]["selected_errors"]
        if best_sel is None or sel < best_sel:
            best_sel, best_g = sel, g
    return best_g


def run_phaseBC(best_conv_tags, best_cand_tags, dev_gains):
    t0 = time.time()
    tasks = [(sc, g, fG, seed, best_conv_tags, best_cand_tags, dev_gains)
             for fG in F_G_LEVELS for sc in SCENES for g in SNR_DB for seed in HELDOUT_SEEDS]
    print(f"Phase B/C held-out (MP): {len(tasks)} cells, {N_WORKERS} workers ...", flush=True)
    raw = []
    with Pool(N_WORKERS) as pool:
        for i, rows in enumerate(pool.imap_unordered(_worker_bc, tasks)):
            raw.extend(rows)
            if (i + 1) % 30 == 0:
                print(f"  {i+1}/{len(tasks)} cells ({round(time.time()-t0,1)}s)", flush=True)
    print(f"  all done ({round(time.time()-t0,1)}s)", flush=True)
    return {"raw_rows": raw, "elapsed_s": round(time.time() - t0, 1)}


def main(best_conv_tags, best_cand_tags, dev_gains):
    """best_conv_tags/best_cand_tags/dev_gains come from dev-tuning (phaseA/devBC).
    For now this is invoked with pre-registered defaults if no dev tuning ran."""
    os.makedirs(OUT_DIR, exist_ok=True)
    bc = run_phaseBC(best_conv_tags, best_cand_tags, dev_gains)
    out = {"package": "P07-R", "phase": "BC_heldout",
           "frozen": {"MDE": MDE, "heldout_seeds": list(HELDOUT_SEEDS),
                      "snr_grid": list(SNR_DB), "f_G_levels": list(F_G_LEVELS),
                      "bitwidths": list(BITWIDTHS)},
           "best_conv_tags": best_conv_tags, "best_cand_tags": best_cand_tags,
           "dev_gains": dev_gains, **bc}
    save_results(out, OUT_BC, os.path.basename(__file__))
    print(f"Saved -> {OUT_BC}")
    return out


if __name__ == "__main__":
    # default: use pre-registered first config of each family (dev-tuning hook)
    bct = {k: v[0] for k, v in CONV_CONFIGS.items()}
    bca = {k: v[0] for k, v in CAND_CONFIGS.items()}
    dg = {W: 0.75 for W in BITWIDTHS}
    main(bct, bca, dg)
