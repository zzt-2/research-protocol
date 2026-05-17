#!/usr/bin/env python3
"""Equal-Cost Multi-Path baseline: split flow across all shortest paths."""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import networkx as nx
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
    """Evaluate ECMP routing baseline across all t_slots per episode.

    For each (src, dst) flow, find all equal-cost shortest paths (by hop count)
    and split demand evenly across them. Iterates through all time slots to
    handle time-varying traffic. Failures are static per episode (set at reset).

    Args:
        env: RoutingEnv instance.
        n_eval: Number of evaluation episodes.
        seed_offset: Base seed for evaluation RNG.

    Returns:
        {"mean": mean MLU, "std": std MLU} across episodes.
    """
    episode_mlus: list[float] = []

    for i in range(n_eval):
        env.reset(seed=seed_offset + i)

        # Failures are static per episode — build graph once
        G = nx.DiGraph()
        G.add_nodes_from(range(env._N))
        for idx in range(env._E):
            u = int(env._edge_index[0, idx])
            v = int(env._edge_index[1, idx])
            if (u, v) not in env._failed_edges:
                G.add_edge(u, v, weight=1.0)

        step_mlus: list[float] = []
        for t in range(env.config.t_slots):
            # Route current flows via ECMP
            link_load: dict[tuple[int, int], float] = defaultdict(float)
            for src, dst, demand in env._flows:
                try:
                    paths = list(nx.all_shortest_paths(G, src, dst, weight="weight"))
                    per_path = demand / len(paths)
                    for path in paths:
                        for j in range(len(path) - 1):
                            link_load[(path[j], path[j + 1])] += per_path
                except nx.NetworkXNoPath:
                    pass

            max_load = max(link_load.values()) if link_load else 0.0
            mlu = max_load / env._capacity if env._capacity > 0 else 0.0
            step_mlus.append(mlu)

            # Advance to next time step's traffic
            if t + 1 < env.config.t_slots:
                env._flows = env._traffic_gen.generate(env._rng, t=t + 1)

        episode_mlus.append(float(np.mean(step_mlus)))

    return {"mean": float(np.mean(episode_mlus)), "std": float(np.std(episode_mlus))}


if __name__ == "__main__":
    config = SimConfig()
    env = RoutingEnv(config)
    result = run_ecmp(env)
    print(f"ECMP: MLU = {result['mean']:.4f} +/- {result['std']:.4f}")
