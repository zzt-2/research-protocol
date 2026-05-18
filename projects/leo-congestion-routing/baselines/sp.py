#!/usr/bin/env python3
"""Shortest-Path baseline: always select the first (shortest) candidate path."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

_PROJECT = Path(__file__).resolve().parent.parent
if str(_PROJECT) not in sys.path:
    sys.path.insert(0, str(_PROJECT))

from simulator.config import SimConfig
from simulator.env import RoutingEnv
from simulator.metrics import aggregate_metrics, compute_episode_metrics


def run_sp(
    env: RoutingEnv,
    n_eval: int = 50,
    seed_offset: int = 200000,
) -> dict[str, float]:
    """Evaluate shortest-path routing baseline.

    Always selects action=0 (first candidate path, which is the shortest).

    Returns:
        Aggregated metrics dict with mean/std for mlu, cv, overflow_ratio,
        plus backward-compatible 'mean' and 'std' for MLU.
    """
    episode_metrics: list[dict] = []

    for i in range(n_eval):
        obs, info = env.reset(seed=seed_offset + i)
        done = False
        while not done:
            obs, reward, terminated, truncated, info = env.step(0)
            done = terminated or truncated

        link_load = info.get("link_load", {})
        capacity = info.get("capacity", env._capacity)
        n_total_edges = info.get("n_total_edges", env._E)
        final_mlu = info.get("final_mlu", info["mlu"])
        episode_metrics.append(
            compute_episode_metrics(link_load, capacity, n_total_edges, final_mlu)
        )

    result = aggregate_metrics(episode_metrics)
    mlus = [m["mlu"] for m in episode_metrics]
    result["mean"] = result["mlu_mean"]
    result["std"] = result["mlu_std"]
    result["mlus"] = mlus
    return result


if __name__ == "__main__":
    config = SimConfig()
    env = RoutingEnv(config)
    result = run_sp(env)
    print(f"Shortest-Path: MLU = {result['mean']:.4f} +/- {result['std']:.4f}")
