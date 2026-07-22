"""F1-A: channel-model prior oracle state headroom Probe.

Frozen contract: ../probe-contract.v1.yaml (governed by D019/D020/S012).

QUESTION: Under scoring-only conditions (per-block true Jones reconstructed from h, theta),
what macro PI-SER headroom does a model-based MMSE equalizer close over fixed-mu CMA mu=0.03?
Is receiver-visible observability plausible (does the gap correlate with any receiver-visible feature)?

HYPO: true-state MMSE closes >= 0.03 headroom on the collapse subset; the gap is not just noise.

FALSIFIER: oracle headroom < 0.03 macro PI-SER (8x below threshold like D018) -> model-prior family Kill.

LEGAL INFORMATION: per-block true Jones matrix (eval-truth h, theta) -> per-block MMSE.
This is a SCORING-ONLY Kill/headroom bound (FR-21). It is NOT a deployable method and NOT a Go
criterion (FR-25). It establishes the ceiling a model-based tracker COULD reach if it recovered
the Jones state perfectly.

OBSERVABILITY CHECK: correlate per-realization oracle headroom with receiver-visible features
(w_norm trajectory stats, z_amp trajectory stats, block-0 collapse flag). If |point-biserial r| < 0.1
for ALL features, flag OBSERVABILITY_UNCONFIRMED even if headroom passes — the information exists but
is not extractable from receiver-visible signals.
"""
from __future__ import annotations
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import probe_shared as ps  # noqa: E402


def receiver_visible_features(cma_result, cell, es, ce, ee):
    """Extract receiver-VISIBLE features (no sX/sY/h/theta). These test observability.

    Returns a dict of scalar features that a deployable tracker could in principle compute
    from the CMA output trace alone.
    """
    trace = cma_result.get("trace", [])
    if not trace:
        return {}
    w_norms = np.array([t.get("w_norm", np.nan) for t in trace], dtype=float)
    z_amps = np.array([t.get("z_amp_max", np.nan) for t in trace], dtype=float)
    cm_errs = np.array([t.get("cm_error", np.nan) for t in trace], dtype=float)
    feats = {
        "w_norm_final": float(w_norms[-1]) if len(w_norms) else float("nan"),
        "w_norm_mean": float(np.nanmean(w_norms)) if len(w_norms) else float("nan"),
        "w_norm_std": float(np.nanstd(w_norms)) if len(w_norms) else float("nan"),
        "z_amp_final": float(z_amps[-1]) if len(z_amps) else float("nan"),
        "z_amp_mean": float(np.nanmean(z_amps)) if len(z_amps) else float("nan"),
        "z_amp_std": float(np.nanstd(z_amps)) if len(z_amps) else float("nan"),
        "cm_error_mean": float(np.nanmean(cm_errs)) if len(cm_errs) else float("nan"),
        "cm_error_final": float(cm_errs[-1]) if len(cm_errs) else float("nan"),
    }
    return feats


def point_biserial(x, y_binary):
    """Point-biserial correlation between continuous x and binary y (0/1)."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y_binary, dtype=float)
    n = len(x)
    n1 = float(np.sum(y == 1))
    n0 = float(np.sum(y == 0))
    if n1 == 0 or n0 == 0:
        return 0.0
    m1 = float(np.mean(x[y == 1]))
    m0 = float(np.mean(x[y == 0]))
    sx = float(np.std(x, ddof=1)) if n > 1 else 0.0
    if sx < 1e-12:
        return 0.0
    return (m1 - m0) * np.sqrt(n1 * n0) / (sx * n)


def run_one(cell, seed):
    """Run CMA anchor + oracle MMSE on one (cell, seed) paired realization."""
    r = ps.make_realization(cell, seed)
    rX, rY = r["rX"], r["rY"]
    sX, sY = r["sX"], r["sY"]
    es, ce, ee, _ = ps.eval_window(cell)
    truth_eval = np.column_stack((sX[ce:ee], sY[ce:ee]))
    bx = r["bitsX"][ce * 4:ee * 4]
    by = r["bitsY"][ce * 4:ee * 4]

    # CMA anchor (fair fixed-mu = 0.03)
    cma = ps.run_cma_anchor(rX, rY)
    if cma["diverged"]:
        m_cma = {"pi_ser": ps.RANDOM_CEILING, "fixed_label_ser": ps.RANDOM_CEILING}
    else:
        m_cma = ps.metrics(cma["zX"][ce:ee], cma["zY"][ce:ee], truth_eval, bx, by)

    # Oracle MMSE (scoring-only Kill bound; uses true h, theta + TX-truth calibration)
    zXo, zYo = ps.mmse_equalize_oracle(rX, rY, r["h"], r["theta"], sX[es:ce], sY[es:ce], es, ce, ee)
    m_oracle = ps.metrics(zXo, zYo, truth_eval, bx, by)

    # Receiver-visible features (for observability check)
    feats = receiver_visible_features(cma, cell, es, ce, ee)

    return {
        "cma_pi_ser": m_cma["pi_ser"],
        "oracle_pi_ser": m_oracle["pi_ser"],
        "headroom": m_cma["pi_ser"] - m_oracle["pi_ser"],
        "cma_diverged": bool(cma["diverged"]),
        "features": feats,
    }


def main():
    t0 = time.time()
    ps.assert_seed_discipline()
    print(f"[F1-A] model-prior oracle headroom Probe; test seeds {ps.TEST_SEEDS}", flush=True)

    rows = []
    for cell in ps.ATLAS_CELLS:
        for seed in ps.TEST_SEEDS:
            r = run_one(cell, seed)
            r["cell"] = cell["id"]
            r["seed"] = seed
            rows.append(r)
        cell_rows = [r for r in rows if r["cell"] == cell["id"]]
        mean_cma = float(np.mean([r["cma_pi_ser"] for r in cell_rows]))
        mean_oracle = float(np.mean([r["oracle_pi_ser"] for r in cell_rows]))
        mean_hr = float(np.mean([r["headroom"] for r in cell_rows]))
        print(f"  {cell['id']}: cma={mean_cma:.4f} oracle={mean_oracle:.4f} headroom={mean_hr:+.4f}",
              flush=True)

    # Headroom aggregates
    macro_cma = ps.macro_aggregate(rows, "cma_pi_ser")
    macro_oracle = ps.macro_aggregate(rows, "oracle_pi_ser")
    macro_hr = ps.macro_aggregate(rows, "headroom")

    # Collapse subset (CMA pi_ser > 0.3, the D018 collapse definition)
    collapse_rows = [r for r in rows if r["cma_pi_ser"] > 0.3]
    macro_hr_collapse = None
    if collapse_rows:
        collapse_by_cell = {}
        for r in collapse_rows:
            collapse_by_cell.setdefault(r["cell"], []).append(r["headroom"])
        cell_means = [float(np.mean(v)) for v in collapse_by_cell.values()]
        macro_hr_collapse = {
            "macro": float(np.mean(cell_means)),
            "n_cells": len(cell_means),
            "n_realizations": len(collapse_rows),
        }

    # Observability check: correlate headroom with receiver-visible features
    # Use collapse flag (binary: cma_pi_ser > 0.3) as the prediction target
    feature_names = []
    for r in rows:
        feature_names = list(r["features"].keys())
        break
    obs_corrs = {}
    if feature_names and collapse_rows:
        # On the FULL set, correlate each feature with the per-realization headroom (continuous)
        all_hr = np.array([r["headroom"] for r in rows])
        for fn in feature_names:
            fv = np.array([r["features"].get(fn, np.nan) for r in rows])
            mask = np.isfinite(fv) & np.isfinite(all_hr)
            if mask.sum() > 5 and np.std(fv[mask]) > 1e-12:
                c = float(np.corrcoef(fv[mask], all_hr[mask])[0, 1])
            else:
                c = 0.0
            obs_corrs[fn] = c
    max_obs_corr = max((abs(v) for v in obs_corrs.values()), default=0.0)

    # Verdict
    macro_headroom = macro_hr["macro"]
    headroom_passes = macro_headroom >= ps.PRACTICAL_HEADROOM_MIN
    headroom_ci_above_zero = macro_hr["ci_lo"] > 0
    observability_confirmed = max_obs_corr >= 0.1

    if not headroom_passes:
        verdict = "FAMILY_NO_HEADROOM"
        verdict_reason = (f"macro oracle headroom {macro_headroom:.6f} < threshold "
                          f"{ps.PRACTICAL_HEADROOM_MIN} (8x below like D018) -> model-prior family Kill.")
    elif headroom_passes and not observability_confirmed:
        verdict = "FAMILY_HEADROOM_BUT_NOT_OBSERVABLE"
        verdict_reason = (f"headroom {macro_headroom:.6f} >= threshold but max receiver-visible "
                          f"correlation |r|={max_obs_corr:.4f} < 0.1 -> BOUNDARY result; information "
                          f"exists but not extractable from receiver-visible signals. Do NOT build full model.")
    else:
        verdict = "FAMILY_HAS_HEADROOM_AND_OBSERVABILITY"
        verdict_reason = (f"headroom {macro_headroom:.6f} >= threshold AND receiver-visible correlation "
                          f"|r|={max_obs_corr:.4f} >= 0.1 -> authorize considering SMALL_ADAPTER Scout (F1-B/C).")

    payload = {
        "probe_id": "F1-A",
        "family": "channel_model_prior",
        "question": ("Under scoring-only conditions, what macro PI-SER headroom does a model-based "
                     "MMSE equalizer close over fixed-mu CMA? Is receiver-visible observability plausible?"),
        "macro_cma_pi_ser": macro_cma,
        "macro_oracle_pi_ser": macro_oracle,
        "macro_headroom_over_cma": macro_hr,
        "macro_headroom_collapse_subset_only": macro_hr_collapse,
        "practical_threshold_headroom_min": ps.PRACTICAL_HEADROOM_MIN,
        "headroom_meets_threshold": headroom_passes,
        "observability": {
            "feature_correlations_with_headroom": obs_corrs,
            "max_abs_correlation": max_obs_corr,
            "observability_confirmed": observability_confirmed,
            "threshold": 0.1,
        },
        "n_realizations": len(rows),
        "verdict": verdict,
        "verdict_reason": verdict_reason,
        "_elapsed_seconds": ps.elapsed(t0),
    }
    out = ps.write_result("F1-A", payload)
    print(f"[F1-A] DONE verdict={verdict}", flush=True)
    print(f"[F1-A] macro headroom={macro_headroom:.6f} (threshold {ps.PRACTICAL_HEADROOM_MIN}); "
          f"max obs |r|={max_obs_corr:.4f}", flush=True)
    print(f"[F1-A] wrote {out}", flush=True)


if __name__ == "__main__":
    main()
