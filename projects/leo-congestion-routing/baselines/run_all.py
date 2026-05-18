#!/usr/bin/env python3
"""Run all baselines (SP, ECMP, MLP) and print comparison table."""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT = Path(__file__).resolve().parent.parent
if str(_PROJECT) not in sys.path:
    sys.path.insert(0, str(_PROJECT))

from simulator.config import SimConfig
from simulator.env import RoutingEnv

from .ecmp import run_ecmp
from .mlp import run_mlp
from .sp import run_sp


def run_all_baselines(
    config: SimConfig | None = None,
    n_eval: int = 50,
    n_episodes: int = 800,
) -> dict[str, dict[str, float]]:
    """Run SP, ECMP, MLP baselines and return results.

    Args:
        config: SimConfig (defaults if None).
        n_eval: Evaluation episodes per baseline.
        n_episodes: PPO training episodes for MLP.

    Returns:
        {"sp": {...}, "ecmp": {...}, "mlp": {...}}
    """
    config = config or SimConfig()
    env = RoutingEnv(config)

    print("=" * 55)
    print("LEO Congestion-Aware Routing — Baseline Comparison")
    print("=" * 55)
    print(f"Topology: {config.n_planes}x{config.sats_per_plane} = {config.n_nodes} nodes")
    print(f"Flows: {config.n_flows}, Capacity: {config.isl_capacity_gbps} Gbps/link")
    print(f"Eval episodes: {n_eval}")
    print()

    print("[1/3] Shortest Path...")
    sp = run_sp(env, n_eval=n_eval)
    print(f"       SP: MLU={sp['mean']:.4f}+/-{sp['std']:.4f}, "
          f"CV={sp['cv_mean']:.4f}, Overflow={sp['overflow_ratio_mean']:.4f}\n")

    print("[2/3] ECMP...")
    ecmp = run_ecmp(env, n_eval=n_eval)
    print(f"       ECMP: MLU={ecmp['mean']:.4f}+/-{ecmp['std']:.4f}, "
          f"CV={ecmp['cv_mean']:.4f}, Overflow={ecmp['overflow_ratio_mean']:.4f}\n")

    print("[3/3] MLP (training required)...")
    mlp = run_mlp(config, n_eval=n_eval, n_episodes=n_episodes)
    print()

    # Comparison table
    print("-" * 75)
    print(f"{'Baseline':<12} {'MLU Mean':>10} {'MLU Std':>10} {'CV Mean':>10} "
          f"{'Overflow':>10} {'vs SP':>10}")
    print("-" * 75)
    for name, res in [("SP", sp), ("ECMP", ecmp), ("MLP", mlp)]:
        ratio = res["mean"] / sp["mean"] if sp["mean"] > 0 else float("nan")
        print(
            f"{name:<12} {res['mean']:>10.4f} {res['std']:>10.4f} "
            f"{res.get('cv_mean', 0):>10.4f} "
            f"{res.get('overflow_ratio_mean', 0):>10.4f} {ratio:>9.2%}"
        )
    print("-" * 75)

    return {"sp": sp, "ecmp": ecmp, "mlp": mlp}


if __name__ == "__main__":
    run_all_baselines()
