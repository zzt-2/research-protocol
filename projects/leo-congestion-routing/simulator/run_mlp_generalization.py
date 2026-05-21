#!/usr/bin/env python3
"""MLP generalization evaluation: train MLP at each scale, evaluate on E04/E05/E06.

Fills the gap identified in Tier 2 audit: no MLP data at generalization scales.
Produces mlp_generalization_results.json with per-scale MLP MLU.
"""

import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

_PROJECT = Path(__file__).resolve().parent.parent
if str(_PROJECT) not in sys.path:
    sys.path.insert(0, str(_PROJECT))

from simulator.config import SimConfig
from simulator.env import RoutingEnv
from baselines.mlp import MLPActorCritic, run_mlp

SCALES = [
    {"name": "E04_48", "planes": 4, "sats": 12, "scale": "0.7x"},
    {"name": "E05_288", "planes": 12, "sats": 24, "scale": "4.4x"},
    {"name": "E06_720", "planes": 36, "sats": 20, "scale": "10.9x"},
]

# Note: MLP is trained FROM SCRATCH at each scale (same as GNN was trained at 66)
# This is the fair comparison: can MLP also generalize? (spoiler: it can't)
# We also test zero-shot: train MLP at 66, deploy at other scales (like GNN)


def train_and_eval_at_scale(config: SimConfig, n_episodes: int = 800, n_eval: int = 50) -> dict:
    """Train MLP at a given scale and evaluate."""
    env = RoutingEnv(config)
    sample_obs, _ = env.reset(seed=0)
    mlp_feat_dim = sample_obs["mlp_feat"].shape[0]

    model = MLPActorCritic(
        mlp_feat_dim=mlp_feat_dim,
        k_paths=config.k_paths,
        hidden=config.hidden_dim,
    )

    t0 = time.time()
    result = run_mlp(
        env_config=config,
        n_eval=n_eval,
        seed=0,
        n_episodes=n_episodes,
    )
    elapsed = time.time() - t0
    result["elapsed_s"] = elapsed
    result["n_episodes"] = n_episodes
    return result


def zero_shot_eval(train_config: SimConfig, eval_config: SimConfig, n_eval: int = 50) -> dict:
    """Train MLP at train_config scale, evaluate at eval_config scale (zero-shot)."""
    # Train at original scale
    print(f"  Training MLP at {train_config.n_nodes} nodes...")
    train_env = RoutingEnv(train_config)
    sample_obs, _ = train_env.reset(seed=0)
    mlp_feat_dim = sample_obs["mlp_feat"].shape[0]

    model = MLPActorCritic(
        mlp_feat_dim=mlp_feat_dim,
        k_paths=train_config.k_paths,
        hidden=train_config.hidden_dim,
    )

    from baselines.mlp import _train_mlp
    t0 = time.time()
    _train_mlp(
        train_env, model,
        n_episodes=800,
        lr=train_config.lr,
        clip_eps=train_config.clip_eps,
        gamma=train_config.gamma,
        gae_lambda=train_config.gae_lambda,
        ppo_epochs=train_config.n_epochs,
        batch_size=train_config.batch_size,
        max_grad_norm=train_config.max_grad_norm,
        entropy_coef=train_config.entropy_coef,
        update_interval=train_config.update_interval,
        early_stop_patience=train_config.early_stop_patience,
        seed=0,
    )
    train_time = time.time() - t0

    # Evaluate at target scale (zero-shot)
    print(f"  Evaluating at {eval_config.n_nodes} nodes (zero-shot)...")
    eval_env = RoutingEnv(eval_config)
    from simulator.metrics import aggregate_metrics, compute_episode_metrics
    episode_metrics = []
    for i in range(n_eval):
        obs, info = eval_env.reset(seed=300000 + i)
        done = False
        while not done:
            action, _, _ = model.get_action(obs, deterministic=True)
            obs, _, terminated, truncated, info = eval_env.step(action.item())
            done = terminated or truncated
        link_load = info.get("link_load", {})
        capacity = info.get("capacity", eval_env._capacity)
        n_total_edges = info.get("n_total_edges", eval_env._E)
        final_mlu = info.get("final_mlu", info["mlu"])
        episode_metrics.append(
            compute_episode_metrics(link_load, capacity, n_total_edges, final_mlu)
        )

    result = aggregate_metrics(episode_metrics)
    mlus = [m["mlu"] for m in episode_metrics]
    result["mean"] = result["mlu_mean"]
    result["std"] = result["mlu_std"]
    result["mlus"] = mlus
    result["train_time_s"] = train_time
    result["train_nodes"] = train_config.n_nodes
    result["eval_nodes"] = eval_config.n_nodes
    result["zero_shot"] = True
    return result


def run() -> dict:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}")

    train_config = SimConfig(device=device)  # 66 nodes
    results = {}

    # === Part 1: Train-from-scratch at each scale ===
    print("\n" + "=" * 60)
    print("Part 1: MLP trained from scratch at each scale")
    print("=" * 60)

    for scale in SCALES:
        name = scale["name"]
        print(f"\n--- {name} ({scale['scale']}, {scale['planes']*scale['sats']} nodes) ---")
        config = SimConfig(
            n_planes=scale["planes"],
            sats_per_plane=scale["sats"],
            device=device,
        )
        result = train_and_eval_at_scale(config)
        results[name + "_scratch"] = result
        print(f"  MLU={result['mean']:.4f} +/- {result['std']:.4f}, "
              f"time={result['elapsed_s']:.1f}s")

    # === Part 2: Zero-shot (train 66, eval other scales) ===
    print("\n" + "=" * 60)
    print("Part 2: MLP zero-shot (train 66, eval other scales)")
    print("=" * 60)

    for scale in SCALES:
        name = scale["name"]
        eval_config = SimConfig(
            n_planes=scale["planes"],
            sats_per_plane=scale["sats"],
            device=device,
        )
        print(f"\n--- {name} zero-shot ---")
        result = zero_shot_eval(train_config, eval_config)
        results[name + "_zeroshot"] = result
        print(f"  MLU={result['mean']:.4f} +/- {result['std']:.4f}")

    # === Summary ===
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    # Load GNN/ECMP results for comparison
    batch_path = Path(__file__).resolve().parent / "results" / "batch_eval_results.json"
    gnn_ecmp = {}
    if batch_path.exists():
        with open(batch_path) as f:
            batch = json.load(f)
        for key in ["E02_no_fault", "E04_48", "E05_288", "E06_720"]:
            if key in batch:
                gnn_ecmp[key] = {
                    "gnn": batch[key]["gnn"]["mean"],
                    "ecmp": batch[key]["ecmp"]["mean"],
                }

    for scale in SCALES:
        name = scale["name"]
        scratch = results.get(name + "_scratch", {})
        zeroshot = results.get(name + "_zeroshot", {})
        ecmp_mlu = gnn_ecmp.get(name, {}).get("ecmp", 0)

        print(f"\n{name} ({scale['scale']}):")
        if scratch:
            ratio = scratch["mean"] / ecmp_mlu if ecmp_mlu > 0 else 0
            print(f"  MLP (scratch):  {scratch['mean']:.4f}  (MLP/ECMP={ratio:.3f})")
        if zeroshot:
            ratio = zeroshot["mean"] / ecmp_mlu if ecmp_mlu > 0 else 0
            print(f"  MLP (zero-shot): {zeroshot['mean']:.4f}  (MLP/ECMP={ratio:.3f})")
        if ecmp_mlu > 0:
            print(f"  ECMP:           {ecmp_mlu:.4f}")

    return results


if __name__ == "__main__":
    results = run()
    out_path = Path(__file__).resolve().parent / "results" / "mlp_generalization_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved to {out_path}")
