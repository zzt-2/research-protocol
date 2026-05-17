#!/usr/bin/env python3
"""Shortest-Path baseline: hop-count weights (all 1.0) for every step."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

# Ensure simulator package is importable
_PROJECT = Path(__file__).resolve().parent.parent
if str(_PROJECT) not in sys.path:
    sys.path.insert(0, str(_PROJECT))

from simulator.config import SimConfig
from simulator.env import RoutingEnv


def run_sp(
    env: RoutingEnv,
    n_eval: int = 50,
    seed_offset: int = 200000,
) -> dict[str, float]:
    """Evaluate shortest-path (hop-count) routing baseline.

    Each step uses uniform weight 1.0 for all edges, which is equivalent
    to standard Dijkstra shortest-path routing.

    Args:
        env: RoutingEnv instance.
        n_eval: Number of evaluation episodes.
        seed_offset: Base seed for evaluation RNG.

    Returns:
        {"mean": mean MLU, "std": std MLU} across episodes.
    """
    action = np.ones(env._E, dtype=np.float32)
    mlus: list[float] = []

    for i in range(n_eval):
        obs, info = env.reset(seed=seed_offset + i)
        done = False
        step_mlus: list[float] = []
        while not done:
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            step_mlus.append(info["mlu"])
        mlus.append(float(np.mean(step_mlus)))

    return {"mean": float(np.mean(mlus)), "std": float(np.std(mlus))}


if __name__ == "__main__":
    config = SimConfig()
    env = RoutingEnv(config)
    result = run_sp(env)
    print(f"Shortest-Path: MLU = {result['mean']:.4f} +/- {result['std']:.4f}")
