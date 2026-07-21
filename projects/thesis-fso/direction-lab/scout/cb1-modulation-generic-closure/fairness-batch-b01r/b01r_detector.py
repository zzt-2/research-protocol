"""B01-R detector module: 4-category label audit + real detector metrics.

Fixes audit findings:
  #2: C05 score was -min(z2_ratio), unrelated to tuned params.
      → We compute scores from BOTH (a) min-z2-ratio baseline (zero-param)
        AND (b) the CUSUM/threshold detector's real alert output.
  #7: Single-class AUROC was misreported as 0.5.
      → We return AUROC = None / "NA/UNDEFINED" for single-class cells.
  #8: PR-AUC, recall@5%FPR, false-alarm, degradation onset, warning
      lead time, Brier/ECE were never computed.
      → We compute all of them per cell.
  #9: oracle_pi_ser > 0.3 conflated AWGN-dominated with inner-ring collapse.
      → 4-category label audit (inner-ring/recoverable, AWGN-dominated,
        healthy, ambiguous).

This module is purely evaluative (no ML, no online use of oracle). Oracle
information is used ONLY for label assignment, never as a detector input.
"""

from __future__ import annotations

from typing import Any

import numpy as np


# =============================================================================
# 4-category label audit
# =============================================================================

def assign_label_4cat(
    *,
    nearest_pi_ser: float,
    oracle_pi_ser: float,
    mean_z2_ratio: float,
    min_z2_ratio: float,
    mde: float = 0.005,
    collapse_z2_ratio_threshold: float = 0.3,
    healthy_pi_ser_threshold: float = 0.1,
    recoverable_oracle_pi_ser_threshold: float = 0.1,
    awgn_oracle_gap_threshold: float = 0.05,
) -> str:
    """Assign one of 4 labels to a seed's trajectory.

    Labels:
      - "inner_ring_recoverable_collapse": z2_ratio low (trajectory collapsed
        to inner ring) AND oracle affine recovers it (oracle_pi_ser low).
        This is the target label for a collapse detector.
      - "awgn_dominated_error": oracle does not help
        (nearest - oracle < awgn_oracle_gap_threshold) but nearest is high.
        Typical for low SNR; NOT a collapse signature.
      - "healthy": nearest_pi_ser < healthy threshold.
      - "ambiguous": none of the above cleanly applies.

    Oracle is used ONLY for label assignment, not as a detector input.
    """
    if nearest_pi_ser < healthy_pi_ser_threshold:
        return "healthy"
    oracle_gap = nearest_pi_ser - oracle_pi_ser
    is_recoverable = oracle_pi_ser < recoverable_oracle_pi_ser_threshold
    is_inner_ring = (
        min_z2_ratio < collapse_z2_ratio_threshold
        or mean_z2_ratio < collapse_z2_ratio_threshold
    )
    if is_inner_ring and is_recoverable and oracle_gap > mde:
        return "inner_ring_recoverable_collapse"
    if oracle_gap < awgn_oracle_gap_threshold and nearest_pi_ser >= healthy_pi_ser_threshold:
        return "awgn_dominated_error"
    return "ambiguous"


def collapse_label_for_auroc(label_4cat: str) -> int | None:
    """Map 4-category label to binary collapse indicator for AUROC.

    Returns:
      1 if inner_ring_recoverable_collapse (positive).
      0 if healthy (negative).
      None if awgn_dominated_error or ambiguous (excluded from AUROC).
    """
    if label_4cat == "inner_ring_recoverable_collapse":
        return 1
    if label_4cat == "healthy":
        return 0
    return None  # AWGN-dominated / ambiguous excluded


# =============================================================================
# min-z2-ratio scoring baseline (zero-parameter, honest lower bound)
# =============================================================================

def min_z2_ratio_score(trace: list[dict[str, Any]], *, R2: float = 1.32, warmup: int = 2) -> float:
    """Zero-parameter scoring baseline: -min(z2_ratio) after warmup.

    Higher score = more collapse-like. This is the BARE heuristic; the
    parameterised C05 detector should beat this if its parameters matter.

    Accepts traces that carry EITHER `z2_over_R2_ratio` directly OR only
    `output_power` (from which ratio is derived as output_power/(2*R2)).
    This matches the C05 detector and degradation_onset_block behavior;
    the previous version silently returned NaN for anchor traces (which
    only carry output_power), which mechanically broke the adjudicator.
    """
    ratios = []
    for i, t in enumerate(trace):
        if i < warmup:
            continue
        r = t.get("z2_over_R2_ratio")
        if r is None or (isinstance(r, float) and np.isnan(r)):
            op = t.get("output_power")
            if op is None or (isinstance(op, float) and np.isnan(op)):
                continue  # skip missing
            else:
                r = float(op) / (2.0 * R2) if R2 > 0 else float("nan")
                if np.isnan(r):
                    continue
        ratios.append(float(r))
    if not ratios:
        return float("nan")
    return -float(np.min(ratios))


# =============================================================================
# CUSUM/threshold detector — REAL alert-based scoring (fixes finding #2)
# =============================================================================

def c05_alert_score(
    trace: list[dict[str, Any]],
    *,
    z2_ratio_threshold: float,
    cusum_drift: float,
    cusum_threshold: float = 3.0,
    R2: float = 1.32,
    warmup: int = 2,
) -> dict[str, Any]:
    """Run CUSUM/threshold detector on trace; return REAL alert-based outputs.

    Score = -first_block_where_alert_fires (earlier alert = higher score).
    If no alert fires, score = -inf (worst).
    This is structurally tied to the tuned (threshold, drift) parameters
    (unlike -min(z2_ratio) which is parameter-independent).
    """
    ratios: list[float] = []
    for t in trace:
        if "z2_over_R2_ratio" in t and not np.isnan(t.get("z2_over_R2_ratio", float("nan"))):
            ratios.append(float(t["z2_over_R2_ratio"]))
        elif "output_power" in t and not np.isnan(t.get("output_power", float("nan"))):
            op = float(t["output_power"])
            ratios.append(op / (2.0 * R2) if R2 > 0 else float("nan"))
        else:
            ratios.append(float("nan"))
    ratios_arr = np.array(ratios)
    if len(ratios_arr) == 0 or np.all(np.isnan(ratios_arr)):
        return {
            "score": float("-inf"),
            "alerts": [],
            "first_alert_block": None,
            "n_alerts": 0,
            "alert_any": 0,
        }
    warmup_ratios = ratios_arr[:warmup]
    valid_warmup = warmup_ratios[~np.isnan(warmup_ratios)]
    baseline = float(np.median(valid_warmup)) if len(valid_warmup) else 1.0

    cusum_stat = 0.0
    alerts: list[dict[str, Any]] = []
    first_alert_block: int | None = None
    n_alerts = 0
    for i, ratio in enumerate(ratios_arr):
        if np.isnan(ratio):
            alerts.append({"block": i, "alert": 0, "threshold_alert": 0, "cusum_alert": 0,
                           "z2_ratio": float("nan"), "cusum_stat": float(cusum_stat)})
            continue
        # WARMUP GUARD: blocks before `warmup` are used only to estimate the
        # baseline; they MUST NOT emit alerts. Previously the detector could
        # fire at block 0 or 1 (during warmup), which made lead_time =
        # onset(2) - alert(0) look like "+2 blocks lead" when it was just a
        # warmup口径 misalignment.
        if i < warmup:
            cusum_stat = max(0.0, cusum_stat + (baseline - ratio) - cusum_drift)
            alerts.append({"block": i, "alert": 0, "threshold_alert": 0, "cusum_alert": 0,
                           "z2_ratio": float(ratio), "cusum_stat": float(cusum_stat),
                           "in_warmup": True})
            continue
        threshold_alert = 1 if ratio < z2_ratio_threshold else 0
        cusum_stat = max(0.0, cusum_stat + (baseline - ratio) - cusum_drift)
        cusum_alert = 1 if cusum_stat >= cusum_threshold else 0
        alert = 1 if (threshold_alert or cusum_alert) else 0
        alerts.append({"block": i, "alert": int(alert),
                       "threshold_alert": int(threshold_alert),
                       "cusum_alert": int(cusum_alert),
                       "z2_ratio": float(ratio), "cusum_stat": float(cusum_stat)})
        if alert:
            n_alerts += 1
            if first_alert_block is None:
                first_alert_block = i
    # Score: earlier alert = higher score (rank by earliness).
    # No alert → -inf (worst rank).
    score = -float(first_alert_block) if first_alert_block is not None else float("-inf")
    return {
        "score": score,
        "alerts": alerts,
        "first_alert_block": first_alert_block,
        "n_alerts": int(n_alerts),
        "alert_any": int(n_alerts > 0),
        "baseline": baseline,
    }


# =============================================================================
# Degradation onset (oracle-side reference for lead time)
# =============================================================================

def degradation_onset_block(
    trace: list[dict[str, Any]],
    *,
    R2: float = 1.32,
    collapse_z2_ratio_threshold: float = 0.5,
    sustained_blocks: int = 2,
    warmup: int = 2,
) -> int | None:
    """DERIVED_HERE: first block where z2_ratio drops below
    collapse_z2_ratio_threshold and stays below for `sustained_blocks`
    consecutive blocks.

    This is the "true" collapse onset (used as reference for warning lead
    time). Returns None if no such onset exists (healthy seed).

    Accepts traces that carry EITHER `z2_over_R2_ratio` directly OR only
    `output_power` (from which ratio is derived as output_power/(2*R2)).
    """
    ratios = []
    for t in trace:
        r = t.get("z2_over_R2_ratio")
        if r is None or (isinstance(r, float) and np.isnan(r)):
            op = t.get("output_power")
            if op is None or (isinstance(op, float) and np.isnan(op)):
                r = float("inf")  # treat missing as "high" (not collapsed)
            else:
                r = float(op) / (2.0 * R2) if R2 > 0 else float("inf")
        ratios.append(float(r))
    run = 0
    for i, r in enumerate(ratios):
        if i < warmup:
            continue
        if r < collapse_z2_ratio_threshold:
            run += 1
            if run >= sustained_blocks:
                return i - run + 1  # first block of the sustained run
        else:
            run = 0
    return None


# =============================================================================
# AUROC / PR-AUC / recall@5%FPR (with proper single-class handling)
# =============================================================================

def auroc_or_none(scores: list[float], labels: list[int]) -> float | None:
    """AUROC via Mann-Whitney U. Returns None if single-class (fixes #7)."""
    s = np.asarray(scores, dtype=float)
    l = np.asarray(labels, dtype=int)
    n_pos = int(np.sum(l == 1))
    n_neg = int(np.sum(l == 0))
    if n_pos == 0 or n_neg == 0:
        return None  # single-class → undefined
    finite = np.isfinite(s)
    if not finite.all():
        # rank -inf as lowest; this is fine for Mann-Whitney.
        s_filled = np.where(finite, s, -1e18)
    else:
        s_filled = s
    order = np.argsort(s_filled)
    ranks = np.empty_like(order, dtype=float)
    ranks[order] = np.arange(1, len(s_filled) + 1)
    # tie handling via average ranks
    sorted_scores = s_filled[order]
    i = 0
    while i < len(sorted_scores):
        j = i
        while j + 1 < len(sorted_scores) and sorted_scores[j + 1] == sorted_scores[i]:
            j += 1
        if j > i:
            avg = (i + 1 + j + 1) / 2.0
            ranks[order[i:j + 1]] = avg
        i = j + 1
    sum_pos = float(np.sum(ranks[l == 1]))
    u = sum_pos - n_pos * (n_pos + 1) / 2.0
    return u / (n_pos * n_neg)


def pr_auc_or_none(scores: list[float], labels: list[int]) -> float | None:
    """Area under precision-recall curve. None if no positives."""
    s = np.asarray(scores, dtype=float)
    l = np.asarray(labels, dtype=int)
    n_pos = int(np.sum(l == 1))
    n_neg = int(np.sum(l == 0))
    if n_pos == 0 or n_neg == 0:
        return None
    finite = np.isfinite(s)
    s_filled = np.where(finite, s, -1e18)
    order = np.argsort(-s_filled)  # high score first
    tp = 0
    fp = 0
    recalls: list[float] = [0.0]
    precisions: list[float] = [1.0]
    for idx in order:
        if l[idx] == 1:
            tp += 1
        else:
            fp += 1
        recall = tp / n_pos
        precision = tp / (tp + fp)
        recalls.append(recall)
        precisions.append(precision)
    # Step-wise integration (monotonic decreasing recall).
    area = 0.0
    for i in range(1, len(recalls)):
        area += (recalls[i] - recalls[i - 1]) * precisions[i]
    return float(area)


def recall_at_fpr(scores: list[float], labels: list[int], *, fpr: float = 0.05) -> tuple[float | None, float | None, int | None]:
    """Recall at a target FPR. Returns (recall, actual_fpr_achieved, fp_budget).

    HONESTY FIX (BUG 3): with small n_neg, a target 5% FPR cannot actually
    be achieved. The smallest nonzero FPR is 1/n_neg. Previously this fn
    silently used floor(0.05*n_neg)=0 for n_neg<20 and returned recall at
    0 FPR (or with the off-by-one in `>` returned at ~1/n_neg).

    Now it returns a tuple: (recall_at_smallest_achievable_nonzero_fpr,
    actual_fpr = fp_budget/n_neg, fp_budget). Caller must report the
    ACTUAL fpr, not the nominal target. If fp_budget=0 (target FPR would
    require 0 false positives but we want nonzero), we report recall at 0
    FPR and actual_fpr=0.0, and the caller must note "0% FPR achieved;
    5% not resolvable with n_neg={}".

    None for all if single-class.
    """
    s = np.asarray(scores, dtype=float)
    l = np.asarray(labels, dtype=int)
    n_pos = int(np.sum(l == 1))
    n_neg = int(np.sum(l == 0))
    if n_pos == 0 or n_neg == 0:
        return None, None, None
    finite = np.isfinite(s)
    s_filled = np.where(finite, s, -1e18)
    order = np.argsort(-s_filled)
    # Budget: largest integer k such that k/n_neg <= target fpr.
    # If target fpr * n_neg < 1 (i.e. n_neg < 1/fpr), the smallest nonzero
    # achievable FPR is 1/n_neg; we use k=1 and flag it.
    k_target = int(np.floor(fpr * n_neg))
    if k_target < 1:
        # Cannot honor target fpr; use smallest nonzero (k=1).
        fp_budget = 1
        actual_fpr = 1.0 / n_neg
    else:
        fp_budget = k_target
        actual_fpr = fp_budget / n_neg
    fp_count = 0
    tp_count = 0
    for idx in order:
        if l[idx] == 1:
            tp_count += 1
        else:
            fp_count += 1
            if fp_count > fp_budget:
                break
    return float(tp_count / n_pos), float(actual_fpr), int(fp_budget)


def false_alarm_rate(scores: list[float], labels: list[int], *, threshold_rank: int = 1) -> float | None:
    """False-alarm rate when declaring top `threshold_rank` seeds as positive.

    None if no negatives.
    """
    s = np.asarray(scores, dtype=float)
    l = np.asarray(labels, dtype=int)
    n_neg = int(np.sum(l == 0))
    if n_neg == 0:
        return None
    finite = np.isfinite(s)
    s_filled = np.where(finite, s, -1e18)
    order = np.argsort(-s_filled)
    top = order[:threshold_rank]
    n_false = int(np.sum(l[top] == 0))
    return float(n_false / n_neg)


def brier_score(probs: list[float], labels: list[int]) -> float:
    """Mean squared error between predicted probabilities and binary labels."""
    p = np.asarray(probs, dtype=float)
    y = np.asarray(labels, dtype=int)
    return float(np.mean((p - y) ** 2))


def expected_calibration_error(probs: list[float], labels: list[int], *, n_bins: int = 5) -> float:
    """ECE with uniform-width bins over [0, 1]."""
    p = np.asarray(probs, dtype=float)
    y = np.asarray(labels, dtype=int)
    bins = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    n = len(p)
    if n == 0:
        return float("nan")
    for i in range(n_bins):
        # Build mask explicitly to avoid Python operator precedence on the boundary.
        if i < n_bins - 1:
            mask = (p >= bins[i]) & (p < bins[i + 1])
        else:
            mask = (p >= bins[i]) & (p <= bins[i + 1])
        if mask.sum() == 0:
            continue
        acc = float(y[mask].mean())
        conf = float(p[mask].mean())
        ece += (mask.sum() / n) * abs(acc - conf)
    return float(ece)


def detector_score_to_prob(score: float, *, score_scale: float = 1.0) -> float:
    """Map a detector score to a pseudo-probability for Brier/ECE.

    Uses a logistic transform with scale `score_scale`. This is a crude
    calibration; if Brier/ECE look bad we report them and explicitly DROP
    any calibration claim.
    """
    if not np.isfinite(score):
        return 0.0
    z = score / max(score_scale, 1e-12)
    # Clip to avoid overflow in exp (stable sigmoid).
    z = float(np.clip(z, -50.0, 50.0))
    return float(1.0 / (1.0 + np.exp(-z)))


__all__ = [
    "assign_label_4cat",
    "collapse_label_for_auroc",
    "min_z2_ratio_score",
    "c05_alert_score",
    "degradation_onset_block",
    "auroc_or_none",
    "pr_auc_or_none",
    "recall_at_fpr",
    "false_alarm_rate",
    "brier_score",
    "expected_calibration_error",
    "detector_score_to_prob",
]
