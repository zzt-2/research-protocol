#!/usr/bin/env python3
"""Generate training curves for GNN and MLP (800ep, surge=1.0).

Produces training_curves_v2.json with per-episode MLU for both methods.
Used for paper Figure: convergence comparison.
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
from simulator.train import train as gnn_train
from baselines.mlp import _train_mlp, MLPActorCritic
from simulator.env import RoutingEnv


def run() -> dict:
    cfg = SimConfig(total_episodes=800, device="cuda" if torch.cuda.is_available() else "cpu")
    print(f"Config: {cfg.n_nodes} nodes, {cfg.total_episodes} eps, surge={cfg.surge_factor}")
    print(f"Device: {cfg.device}")

    results = {}

    # --- GNN training ---
    print(f"\n{'='*60}")
    print("Training GNN (800 episodes)...")
    print(f"{'='*60}")
    t0 = time.time()
    gnn_result = gnn_train(cfg, seed=42)
    gnn_time = time.time() - t0
    print(f"GNN training: {gnn_time:.1f}s, {len(gnn_result['episode_mlus'])} episodes")
    results["gnn"] = {
        "episode_mlus": gnn_result["episode_mlus"],
        "n_episodes": len(gnn_result["episode_mlus"]),
        "elapsed_s": gnn_time,
        "final_mlu_mean50": float(np.mean(gnn_result["episode_mlus"][-50:])),
    }

    # --- MLP training ---
    print(f"\n{'='*60}")
    print("Training MLP (800 episodes)...")
    print(f"{'='*60}")
    env = RoutingEnv(cfg, seed=42)
    sample_obs, _ = env.reset(seed=0)
    mlp_feat_dim = sample_obs["mlp_feat"].shape[0]
    mlp_model = MLPActorCritic(mlp_feat_dim=mlp_feat_dim, k_paths=cfg.k_paths, hidden=cfg.hidden_dim)

    t0 = time.time()
    mlp_mlus = _train_mlp(
        env, mlp_model,
        n_episodes=800,
        lr=cfg.lr,
        clip_eps=cfg.clip_eps,
        gamma=cfg.gamma,
        gae_lambda=cfg.gae_lambda,
        ppo_epochs=cfg.n_epochs,
        batch_size=cfg.batch_size,
        max_grad_norm=cfg.max_grad_norm,
        entropy_coef=cfg.entropy_coef,
        update_interval=cfg.update_interval,
        early_stop_patience=cfg.early_stop_patience,
        seed=42,
    )
    mlp_time = time.time() - t0
    print(f"MLP training: {mlp_time:.1f}s, {len(mlp_mlus)} episodes")
    results["mlp"] = {
        "episode_mlus": mlp_mlus,
        "n_episodes": len(mlp_mlus),
        "elapsed_s": mlp_time,
        "final_mlu_mean50": float(np.mean(mlp_mlus[-50:])),
    }

    # --- Summary ---
    gnn_final = results["gnn"]["final_mlu_mean50"]
    mlp_final = results["mlp"]["final_mlu_mean50"]
    print(f"\n{'='*60}")
    print(f"GNN final MLU (last 50): {gnn_final:.4f}")
    print(f"MLP final MLU (last 50): {mlp_final:.4f}")
    print(f"GNN/MLP ratio: {gnn_final/mlp_final:.4f}")
    print(f"GNN training time: {gnn_time:.1f}s")
    print(f"MLP training time: {mlp_time:.1f}s")
    print(f"{'='*60}")

    return results


if __name__ == "__main__":
    results = run()
    out_path = Path(__file__).resolve().parent / "results" / "training_curves_v2.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved to {out_path}")
