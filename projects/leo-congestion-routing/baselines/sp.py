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


def run_sp(
    env: RoutingEnv,
    n_eval: int = 50,
    seed_offset: int = 200000,
) -> dict[str, float]:
    """Evaluate shortest-path routing baseline.

    Always selects action=0 (first candidate path, which is the shortest).

    Returns:
        {"mean": mean MLU, "std": std MLU} across episodes.
    """
    mlus: list[float] = []

    for i in range(n_eval):
        obs, info = env.reset(seed=seed_offset + i)
        done = False
        while not done:
            obs, reward, terminated, truncated, info = env.step(0)
            done = terminated or truncated
        mlus.append(info.get("final_mlu", info["mlu"]))

    return {"mean": float(np.mean(mlus)), "std": float(np.std(mlus))}


if __name__ == "__main__":
    config = SimConfig()
    env = RoutingEnv(config)
    result = run_sp(env)
    print(f"Shortest-Path: MLU = {result['mean']:.4f} +/- {result['std']:.4f}")
