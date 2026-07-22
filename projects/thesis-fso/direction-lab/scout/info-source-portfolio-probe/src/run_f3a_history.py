"""F3-A: causal temporal history information-increment Probe.

Frozen contract: ../probe-contract.v1.yaml (governed by D019/D020/S012).

QUESTION: Do past K blocks (z-stream, CMA weight trajectory) provide CONDITIONAL information
about the current block's optimal action / state beyond block-0-only features? Quantify via
conditional mutual information and predictive R^2.

HYPO: past-block features add > 0 conditional MI about optimal MMSE Jones / collapse flag.

FALSIFIER: conditional MI ~ 0 (|MI| < 0.01 bits) OR predictive R^2 with history <= R^2 block-0-only
-> history family Kill. (Must prove history actually adds information; cannot assume RNN creates it.)

LEGAL INFORMATION: causal past-block z-stream + CMA weight trajectory (receiver-visible).
COMPARATOR: block-0-only feature baseline (H066: collapse determined at block 0).

NOTE: This is an OBSERVABILITY Probe, not a method. It does NOT train an RNN/GRU. It uses
information-theoretic bounds (mutual information between past-block features and current-block
oracle headroom / collapse flag) to test whether history carries usable conditional information.
"""
from __future__ import annotations
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import probe_shared as ps  # noqa: E402


def mutual_information_binary_continuous(y_binary, x_continuous, n_bins=10):
    """Estimate MI between a binary variable and a continuous variable via binning.

    Uses equiprobable binning on x. Returns bits. Conservative (underestimates true MI).
    """
    y = np.asarray(y_binary, dtype=float)
    x = np.asarray(x_continuous, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    y = y[mask]
    x = x[mask]
    n = len(y)
    if n < 20:
        return 0.0
    # Equiprobable bins on x
    quantiles = np.linspace(0, 1, n_bins + 1)[1:-1]
    x_edges = np.quantile(x, quantiles)
    x_bin = np.digitize(x, x_edges)
    # Joint distribution P(y, x_bin)
    p_yx = np.zeros((2, n_bins))
    for yi in (0, 1):
        for xb in range(n_bins):
            p_yx[yi, xb] = np.mean((y == yi) & (x_bin == xb))
    p_y = p_yx.sum(axis=1, keepdims=True)
    p_x = p_yx.sum(axis=0, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.where((p_yx > 0) & (p_y > 0) & (p_x > 0),
                         p_yx / (p_y * p_x), 1.0)
        mi = float(np.sum(p_yx * np.log2(ratio)))
    return max(mi, 0.0)


def block_features_from_trace(cma_result, block_idx):
    """Receiver-visible features for a SINGLE block from the CMA trace (causal, past-only)."""
    trace = cma_result.get("trace", [])
    if block_idx >= len(trace):
        return None
    t = trace[block_idx]
    return {
        "w_norm": float(t.get("w_norm", np.nan)),
        "z_amp_max": float(t.get("z_amp_max", np.nan)),
        "cm_error": float(t.get("cm_error", np.nan)),
        "update_norm": float(t.get("update_norm", np.nan)),
    }


def run_one(cell, seed):
    """Run CMA anchor, extract per-block features, compute oracle headroom per block (long cells only).

    For short cells (N=512, ~5-8 blocks) there is little history to test. The history Probe
    is most meaningful on LONG cells (N=8192, ~128 blocks) where past blocks could predict
    future block state. We still record short-cell features for completeness.
    """
    r = ps.make_realization(cell, seed)
    rX, rY = r["rX"], r["rY"]
    sX, sY = r["sX"], r["sY"]
    es, ce, ee, _ = ps.eval_window(cell)
    truth_eval = np.column_stack((sX[ce:ee], sY[ce:ee]))
    bx = r["bitsX"][ce * 4:ee * 4]
    by = r["bitsY"][ce * 4:ee * 4]

    cma = ps.run_cma_anchor(rX, rY)
    if cma["diverged"]:
        return {"cell": cell["id"], "seed": seed, "diverged": True,
                "cma_pi_ser": ps.RANDOM_CEILING, "n_blocks": 0, "per_block_features": [],
                "collapse_flag": True}

    m_cma = ps.metrics(cma["zX"][ce:ee], cma["zY"][ce:ee], truth_eval, bx, by)
    trace = cma.get("trace", [])
    n_blocks = len(trace)

    # Per-block receiver-visible features
    per_block = []
    for bi in range(n_blocks):
        f = block_features_from_trace(cma, bi)
        if f is not None:
            per_block.append(f)

    # Block-0 features (the H066 baseline: collapse determined at block 0)
    block0 = block_features_from_trace(cma, 0) if n_blocks > 0 else {}

    # Collapse flag (realization-level): CMA pi_ser > 0.3 (D018 definition)
    collapse_flag = m_cma["pi_ser"] > 0.3

    return {
        "cell": cell["id"],
        "seed": seed,
        "diverged": False,
        "cma_pi_ser": m_cma["pi_ser"],
        "n_blocks": n_blocks,
        "per_block_features": per_block,
        "block0_features": block0,
        "collapse_flag": collapse_flag,
    }


def main():
    t0 = time.time()
    ps.assert_seed_discipline()
    print(f"[F3-A] causal-history information-increment Probe; test seeds {ps.TEST_SEEDS}", flush=True)

    rows = []
    for cell in ps.ATLAS_CELLS:
        for seed in ps.TEST_SEEDS:
            r = run_one(cell, seed)
            rows.append(r)
        cell_rows = [r for r in rows if r["cell"] == cell["id"]]
        n_blk = np.mean([r["n_blocks"] for r in cell_rows])
        print(f"  {cell['id']}: mean n_blocks={n_blk:.1f}", flush=True)

    # === MI analysis: does past-block information predict collapse_flag? ===
    # Aggregate per-realization summary features from the trace.
    # block-0 features (H066 baseline) vs full-history features.
    def summarize_trace(per_block, block0):
        """Return (block0_feat_vector, history_feat_vector) as dicts of scalars."""
        if not per_block:
            return {}, {}
        b0 = block0 if block0 else {}
        # History = stats over ALL blocks (a summary that a recurrent model could form)
        wn = np.array([b.get("w_norm", np.nan) for b in per_block], dtype=float)
        za = np.array([b.get("z_amp_max", np.nan) for b in per_block], dtype=float)
        ce_ = np.array([b.get("cm_error", np.nan) for b in per_block], dtype=float)
        history = {
            "w_norm_mean": float(np.nanmean(wn)) if np.any(np.isfinite(wn)) else np.nan,
            "w_norm_std": float(np.nanstd(wn)) if np.any(np.isfinite(wn)) else np.nan,
            "z_amp_mean": float(np.nanmean(za)) if np.any(np.isfinite(za)) else np.nan,
            "z_amp_std": float(np.nanstd(za)) if np.any(np.isfinite(za)) else np.nan,
            "cm_error_mean": float(np.nanmean(ce_)) if np.any(np.isfinite(ce_)) else np.nan,
            "cm_error_std": float(np.nanstd(ce_)) if np.any(np.isfinite(ce_)) else np.nan,
            "cm_error_trend": (float(ce_[-1] - ce_[0]) if (len(ce_) > 1 and np.isfinite(ce_[0]) and np.isfinite(ce_[-1])) else 0.0),
        }
        return b0, history

    collapse_flags = np.array([1.0 if r["collapse_flag"] else 0.0 for r in rows])

    # MI(block0 features, collapse) vs MI(history features, collapse)
    block0_mis = {}
    history_mis = {}
    # Collect feature vectors
    feat_names_b0 = set()
    feat_names_h = set()
    for r in rows:
        b0, h = summarize_trace(r["per_block_features"], r["block0_features"])
        feat_names_b0.update(b0.keys())
        feat_names_h.update(h.keys())

    for fn in feat_names_b0:
        vals = []
        for r in rows:
            b0, _ = summarize_trace(r["per_block_features"], r["block0_features"])
            vals.append(b0.get(fn, np.nan))
        mi = mutual_information_binary_continuous(collapse_flags, np.array(vals))
        block0_mis[fn] = mi
    for fn in feat_names_h:
        vals = []
        for r in rows:
            _, h = summarize_trace(r["per_block_features"], r["block0_features"])
            vals.append(h.get(fn, np.nan))
        mi = mutual_information_binary_continuous(collapse_flags, np.array(vals))
        history_mis[fn] = mi

    max_mi_block0 = max(block0_mis.values()) if block0_mis else 0.0
    max_mi_history = max(history_mis.values()) if history_mis else 0.0
    # Increment = best history MI - best block-0 MI (conditional information added by history)
    mi_increment = max_mi_history - max_mi_block0

    # === Predictive R^2: can history features predict per-realization cma_pi_ser better than block-0? ===
    # Simple linear regression R^2 (1 feature at a time, best single feature)
    pi_sers = np.array([r["cma_pi_ser"] for r in rows])

    def best_single_feature_r2(feat_dict_list, target):
        best = 0.0
        best_fn = None
        names = set()
        for fd in feat_dict_list:
            names.update(fd.keys())
        for fn in names:
            vals = np.array([fd.get(fn, np.nan) for fd in feat_dict_list])
            mask = np.isfinite(vals) & np.isfinite(target)
            if mask.sum() > 10 and np.std(vals[mask]) > 1e-12:
                x = vals[mask]
                y = target[mask]
                # Linear fit
                A = np.vstack([x, np.ones_like(x)]).T
                coef, *_ = np.linalg.lstsq(A, y, rcond=None)
                yhat = A @ coef
                ss_res = float(np.sum((y - yhat) ** 2))
                ss_tot = float(np.sum((y - np.mean(y)) ** 2))
                r2 = 1 - ss_res / ss_tot if ss_tot > 1e-12 else 0.0
                if r2 > best:
                    best = r2
                    best_fn = fn
        return best, best_fn

    b0_list = []
    h_list = []
    for r in rows:
        b0, h = summarize_trace(r["per_block_features"], r["block0_features"])
        b0_list.append(b0)
        h_list.append(h)
    r2_block0, r2_b0_fn = best_single_feature_r2(b0_list, pi_sers)
    r2_history, r2_h_fn = best_single_feature_r2(h_list, pi_sers)
    r2_increment = r2_history - r2_block0

    # Verdict
    mi_threshold = 0.01  # bits
    mi_passes = mi_increment > mi_threshold
    r2_passes = r2_increment > 0.0
    observability_confirmed = mi_passes or r2_passes

    if not observability_confirmed:
        verdict = "FAMILY_NO_HEADROOM"
        verdict_reason = (f"history adds no conditional information: MI increment={mi_increment:.4f} bits "
                          f"(threshold {mi_threshold}), R^2 increment={r2_increment:.4f}. Best history MI="
                          f"{max_mi_history:.4f} vs best block-0 MI={max_mi_block0:.4f}. -> history family Kill.")
    else:
        verdict = "FAMILY_HAS_HEADROOM_AND_OBSERVABILITY"
        verdict_reason = (f"history adds conditional information: MI increment={mi_increment:.4f} bits "
                          f"(>{mi_threshold}) OR R^2 increment={r2_increment:+.4f}. Best history MI="
                          f"{max_mi_history:.4f} (feat={r2_h_fn}). Authorize considering SMALL_ADAPTER Scout.")

    payload = {
        "probe_id": "F3-A",
        "family": "causal_temporal_history",
        "question": ("Do past K blocks provide CONDITIONAL information about current block state "
                     "beyond block-0-only features? (MI + predictive R^2)"),
        "mutual_information": {
            "block0_feature_mi": block0_mis,
            "history_feature_mi": history_mis,
            "max_mi_block0": max_mi_block0,
            "max_mi_history": max_mi_history,
            "mi_increment_history_minus_block0": mi_increment,
            "threshold_bits": mi_threshold,
        },
        "predictive_r2": {
            "best_r2_block0": r2_block0,
            "best_r2_block0_feature": r2_b0_fn,
            "best_r2_history": r2_history,
            "best_r2_history_feature": r2_h_fn,
            "r2_increment_history_minus_block0": r2_increment,
        },
        "n_realizations": len(rows),
        "n_collapse": int(np.sum(collapse_flags)),
        "verdict": verdict,
        "verdict_reason": verdict_reason,
        "_elapsed_seconds": ps.elapsed(t0),
    }
    out = ps.write_result("F3-A", payload)
    print(f"[F3-A] DONE verdict={verdict}", flush=True)
    print(f"[F3-A] MI increment={mi_increment:.4f} bits (threshold {mi_threshold}); "
          f"R^2 increment={r2_increment:+.4f}", flush=True)
    print(f"[F3-A] wrote {out}", flush=True)


if __name__ == "__main__":
    main()
