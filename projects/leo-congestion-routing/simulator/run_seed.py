"""Single-seed training + evaluation runner for LEO congestion-aware routing."""
import sys
import os

# Add project root so relative paths in train.py resolve correctly
ROOT = "/mnt/d/code/study/research-protocol"
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "projects", "leo-congestion-routing"))

import json
from pathlib import Path

import numpy as np
import torch

from simulator.config import SimConfig
from simulator.train import train, evaluate
from simulator.model import RoutingActorCritic
from simulator.env import RoutingEnv

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 0

cfg = SimConfig(total_episodes=500, n_seeds=1)
print(f"Config: {cfg.n_nodes} nodes, {cfg.total_episodes} eps, seed={SEED}, device={cfg.device}")

# Train
result = train(cfg, seed=SEED)

# Evaluate best model
env = RoutingEnv(cfg, seed=SEED)
model = RoutingActorCritic(
    node_dim=cfg.node_feat_dim,
    edge_dim=cfg.edge_feat_dim,
    hidden_dim=cfg.hidden_dim,
    n_layers=cfg.n_layers,
    n_heads=cfg.n_heads,
    n_edges=env._E,
).to(cfg.device)

results_dir = Path("projects/leo-congestion-routing/simulator/results")
ckpt_path = results_dir / "ppo_best.pt"
if ckpt_path.exists():
    ckpt = torch.load(str(ckpt_path), map_location=cfg.device, weights_only=False)
    model.load_state_dict(ckpt["model"])
    print(f"Loaded best checkpoint")
else:
    print("WARNING: No best checkpoint, using final model")

eval_result = evaluate(model, env, n_eval=50, device=cfg.device)
eval_result["seed"] = SEED
eval_result["train_best_reward"] = result["best_reward"]
eval_result["train_n_episodes"] = result["n_episodes"]
eval_result["train_elapsed"] = result["elapsed_seconds"]

# Save eval result
eval_path = results_dir / f"eval_seed{SEED}.json"
with open(eval_path, "w") as f:
    json.dump(eval_result, f, indent=2)

# Reference baselines
ECMP_MLU = 1.9664
SP_MLU = 2.3674
MLP_MLU = 2.5249

# Summary
print(f"\n{'='*60}")
print(f"Seed {SEED} Summary:")
print(f"  Train: {result['n_episodes']} eps in {result['elapsed_seconds']:.1f}s")
print(f"  Best reward: {result['best_reward']:.4f}")
print(f"  Eval MLU: {eval_result['mean']:.4f} +/- {eval_result['std']:.4f}")
print(f"  GNN/ECMP: {eval_result['mean']/ECMP_MLU:.4f}")
print(f"  GNN/MLP:  {eval_result['mean']/MLP_MLU:.4f}")
print(f"  GNN/SP:   {eval_result['mean']/SP_MLU:.4f}")
print(f"{'='*60}")
