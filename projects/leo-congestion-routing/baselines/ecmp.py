#!/usr/bin/env python3
"""ECMP baseline: round-robin among equal-cost shortest candidate paths."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

_PROJECT = Path(__file__).resolve().parent.parent
if str(_PROJECT) not in sys.path:
    sys.path.insert(0, str(_PROJECT))

from simulator.config import SimConfig
from simulator.env import RoutingEnv


def run_ecmp(
    env: RoutingEnv,
    n_eval: int = 50,
    seed_offset: int = 200000,
) -> dict[str, float]:
    """Evaluate ECMP routing baseline (sequential K-path variant).

    For each flow: from K candidate paths, find equal-cost shortest paths
    and round-robin among them. This matches the K-path sequential paradigm
    where each flow is routed along a single path.

    Returns:
        {"mean": mean MLU, "std": std MLU} across episodes.
    """
    mlus: list[float] = []

    for i in range(n_eval):
        obs, info = env.reset(seed=seed_offset + i)
        step_idx = 0
        done = False
        while not done:
            paths = obs["paths"]
            n_valid = obs["n_valid"]
            if n_valid == 0:
                action = 0
            else:
                min_len = min(len(p) for p in paths[:n_valid])
                equal = [j for j, p in enumerate(paths[:n_valid]) if len(p) == min_len]
                action = equal[step_idx % len(equal)] if equal else 0
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            step_idx += 1
        mlus.append(info.get("final_mlu", info["mlu"]))

    return {"mean": float(np.mean(mlus)), "std": float(np.std(mlus))}


if __name__ == "__main__":
    config = SimConfig()
    env = RoutingEnv(config)
    result = run_ecmp(env)
    print(f"ECMP: MLU = {result['mean']:.4f} +/- {result['std']:.4f}")
