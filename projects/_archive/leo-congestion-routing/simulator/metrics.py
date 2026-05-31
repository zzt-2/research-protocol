"""Evaluation metrics for LEO congestion-aware routing.

M1: MLU  — Maximum Link Utilization (already existed)
M2: CV   — Coefficient of Variation of link utilization
M3: Overflow Ratio — fraction of edges exceeding capacity
M4: Generalization Gap — MLU_test / MLU_train ratio
M5: Convergence Speed — episodes needed for stable MLU
"""

from __future__ import annotations

import numpy as np


def compute_episode_metrics(
    link_load: dict[tuple[int, int], float],
    capacity: float,
    n_total_edges: int,
    final_mlu: float | None = None,
    avg_delay_ms: float = 0.0,
    max_delay_ms: float = 0.0,
) -> dict[str, float]:
    """Compute all per-episode metrics from raw link load data.

    Args:
        link_load: Mapping (u, v) -> accumulated load (Gbps) for each
            directed edge.  Undirected edges appear twice as (u,v) and (v,u).
        capacity: Uniform link capacity in Gbps.
        n_total_edges: Total number of directed edges |E| in the topology.
        final_mlu: Pre-computed MLU if available; computed from link_load
            otherwise.
        avg_delay_ms: Average E2E propagation delay across all flows (ms).
        max_delay_ms: Maximum E2E propagation delay across all flows (ms).

    Returns:
        Dict with keys: mlu, cv, overflow_ratio, mean_util, std_util,
        avg_delay_ms, max_delay_ms.
    """
    loads = np.array(list(link_load.values()), dtype=np.float64) if link_load else np.array([0.0])

    # Per-link utilization array
    utils = loads / capacity if capacity > 0 else np.zeros_like(loads)

    # M1: MLU
    mlu = final_mlu if final_mlu is not None else float(np.max(utils))

    # M2: CV = std(util) / mean(util), lower is better
    mean_util = float(np.mean(utils))
    std_util = float(np.std(utils))
    cv = std_util / mean_util if mean_util > 0 else 0.0

    # M3: Overflow Ratio = count(load > capacity) / |E|
    overflow_count = int(np.sum(loads > capacity))
    overflow_ratio = overflow_count / n_total_edges if n_total_edges > 0 else 0.0

    return {
        "mlu": mlu,
        "cv": cv,
        "overflow_ratio": overflow_ratio,
        "mean_util": mean_util,
        "std_util": std_util,
        "avg_delay_ms": avg_delay_ms,
        "max_delay_ms": max_delay_ms,
    }


def aggregate_metrics(episode_metrics: list[dict[str, float]]) -> dict[str, float]:
    """Aggregate per-episode metrics into mean and std summaries.

    Args:
        episode_metrics: List of dicts returned by compute_episode_metrics.

    Returns:
        Dict with keys like {metric}_mean and {metric}_std for mlu, cv,
        overflow_ratio, plus n_episodes.
    """
    if not episode_metrics:
        return {}

    keys = ["mlu", "cv", "overflow_ratio", "mean_util", "std_util", "avg_delay_ms", "max_delay_ms"]
    result: dict[str, float] = {"n_episodes": float(len(episode_metrics))}

    for key in keys:
        vals = [m[key] for m in episode_metrics]
        result[f"{key}_mean"] = float(np.mean(vals))
        result[f"{key}_std"] = float(np.std(vals))

    return result


def compute_convergence_speed(
    episode_mlus: list[float],
    window: int = 50,
    threshold: float = 0.01,
) -> int:
    """M5: Convergence Speed — first episode where the rolling variance of
    MLU over the last *window* episodes drops below *threshold*.

    Args:
        episode_mlus: MLU values indexed by episode number (0-based).
        window: Number of trailing episodes to consider.
        threshold: Variance threshold for "stable".

    Returns:
        Episode index (0-based) at which convergence is achieved.
        Returns -1 if convergence was never reached.
    """
    if len(episode_mlus) < window:
        return -1

    arr = np.array(episode_mlus, dtype=np.float64)
    for i in range(window - 1, len(arr)):
        var = float(np.var(arr[i - window + 1 : i + 1]))
        if var < threshold:
            return i
    return -1


def compute_generalization_gap(
    mlu_train_mean: float,
    mlu_test_mean: float,
) -> float:
    """M4: Generalization Gap — MLU_test / MLU_train.

    A value close to 1.0 indicates good generalization.  Values > 1.0
    mean the model performs worse on test scenarios; values < 1.0
    mean it performs better on test (which may indicate underfitting or
    an easier test distribution).

    Args:
        mlu_train_mean: Mean MLU on training episodes.
        mlu_test_mean: Mean MLU on held-out evaluation episodes.

    Returns:
        Ratio mlu_test_mean / mlu_train_mean.  Returns float('nan')
        if mlu_train_mean is 0.
    """
    if mlu_train_mean == 0:
        return float("nan")
    return mlu_test_mean / mlu_train_mean
