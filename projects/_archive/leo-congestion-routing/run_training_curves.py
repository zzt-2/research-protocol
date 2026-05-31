#!/usr/bin/env python3
"""Training curves: per-episode MLU for GNN and MLP.

Run from project root:
    cd /mnt/d/code/study/research-protocol
    ~/.venvs/torch/bin/python -u projects/leo-congestion-routing/run_training_curves.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))

from baselines.mlp import MLPActorCritic, _train_mlp
from simulator.config import SimConfig
from simulator.env import RoutingEnv
from simulator.model import RoutingActorCritic
from simulator.train import evaluate, train

RESULTS_DIR = Path(__file__).resolve().parent / "simulator" / "results"
RESULTS_DIR.mkdir(exist_ok=True, parents=True)


def main() -> None:
    t0 = time.time()

    cfg = SimConfig(
        total_episodes=500,
        n_seeds=1,
        n_eval=50,
        device="cuda",
        entropy_coef=0.02,
        early_stop_patience=80,
    )

    # ── GNN training curve ──────────────────────────────────────────────
    print("=" * 60)
    print("  GNN Training (1 seed × 500ep)")
    print("=" * 60)
    gnn_result = train(cfg, seed=0)

    # Evaluate final GNN model
    env = RoutingEnv(cfg, seed=0)
    model = RoutingActorCritic(
        cfg.node_feat_dim, cfg.edge_feat_dim, cfg.hidden_dim,
        cfg.n_layers, cfg.n_heads, cfg.k_paths,
    ).to(cfg.device)
    ckpt = torch.load(
        str(RESULTS_DIR / "ppo_best.pt"),
        map_location=cfg.device, weights_only=False,
    )
    model.load_state_dict(ckpt["model"])
    gnn_eval = evaluate(model, env, n_eval=50, device=cfg.device)

    # ── MLP training curve ──────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  MLP Training (1 seed × 300ep)")
    print("=" * 60)
    env_mlp = RoutingEnv(cfg, seed=0)
    sample_obs, _ = env_mlp.reset(seed=0)
    mlp_feat_dim = sample_obs["mlp_feat"].shape[0]
    mlp_model = MLPActorCritic(mlp_feat_dim=mlp_feat_dim, k_paths=cfg.k_paths)

    mlp_episode_mlus = _train_mlp(env_mlp, mlp_model, n_episodes=300, seed=0)

    # Evaluate final MLP model
    mlp_mlus: list[float] = []
    for i in range(50):
        obs, info = env_mlp.reset(seed=300000 + i)
        done = False
        while not done:
            action, _, _ = mlp_model.get_action(obs, deterministic=True)
            obs, _, terminated, truncated, info = env_mlp.step(action.item())
            done = terminated or truncated
        mlp_mlus.append(info.get("final_mlu", info["mlu"]))

    # ── Save ────────────────────────────────────────────────────────────
    output = {
        "gnn": {
            "episode_mlus": gnn_result["episode_mlus"],
            "episode_rewards": gnn_result["episode_rewards"],
            "eval_mean": gnn_eval["mean"],
            "eval_std": gnn_eval["std"],
            "n_episodes": gnn_result["n_episodes"],
        },
        "mlp": {
            "episode_mlus": mlp_episode_mlus,
            "eval_mean": float(np.mean(mlp_mlus)),
            "eval_std": float(np.std(mlp_mlus)),
            "n_episodes": len(mlp_episode_mlus),
        },
        "elapsed_seconds": time.time() - t0,
    }

    out_path = RESULTS_DIR / "training_curves.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved to {out_path}")
    print(f"Total time: {(time.time() - t0)/60:.1f} min")


if __name__ == "__main__":
    main()
