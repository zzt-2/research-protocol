"""F1 quick verification: 100ep GNN training with surge_factor=1.0 (no surge).

Compares GNN vs ECMP/SP baselines under the same no-surge config.
Saves results to results/f1_quick_test.json.
"""
import sys
import os
import json
import time
import shutil

ROOT = "/mnt/d/code/study/research-protocol"
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "projects", "leo-congestion-routing"))

import numpy as np
import torch

from simulator.config import SimConfig
from simulator.train import train, evaluate
from simulator.model import RoutingActorCritic
from simulator.env import RoutingEnv
from baselines.ecmp import run_ecmp
from baselines.sp import run_sp

RESULTS_DIR = "projects/leo-congestion-routing/simulator/results"
CKPT_PATH = os.path.join(RESULTS_DIR, "ppo_best.pt")
CKPT_BACKUP = os.path.join(RESULTS_DIR, "ppo_best_surge5_backup.pt")

# Backup existing checkpoint (trained with surge=5.0)
if os.path.exists(CKPT_PATH) and not os.path.exists(CKPT_BACKUP):
    shutil.copy2(CKPT_PATH, CKPT_BACKUP)
    print(f"Backed up existing checkpoint to {CKPT_BACKUP}")

# Config: surge=1.0 (default), 100ep quick test
cfg = SimConfig(total_episodes=100, n_seeds=1)
print(f"Config: {cfg.n_nodes} nodes, surge={cfg.surge_factor}, {cfg.total_episodes} eps")
print(f"Fault rate: {cfg.failure_rate}, K={cfg.k_paths}")
print()

# --- 1. Train GNN (100ep) ---
t0 = time.time()
result = train(cfg, seed=0)
train_time = time.time() - t0
print(f"\nTrain: {result['n_episodes']} eps in {train_time:.1f}s")
print(f"Best reward: {result['best_reward']:.4f}")

# --- 2. Evaluate GNN ---
env = RoutingEnv(cfg, seed=0)
model = RoutingActorCritic(
    node_dim=cfg.node_feat_dim,
    edge_dim=cfg.edge_feat_dim,
    hidden_dim=cfg.hidden_dim,
    n_layers=cfg.n_layers,
    n_heads=cfg.n_heads,
    n_edges=env._E,
).to(cfg.device)

if os.path.exists(CKPT_PATH):
    ckpt = torch.load(CKPT_PATH, map_location=cfg.device, weights_only=False)
    model.load_state_dict(ckpt["model"])
    print(f"Loaded best checkpoint from ep {ckpt.get('episode', '?')}")
else:
    print("WARNING: No checkpoint found, using final model")

gnn_result = evaluate(model, env, n_eval=50, device=cfg.device)
print(f"\nGNN MLU:  {gnn_result['mean']:.4f} +/- {gnn_result['std']:.4f}")

# --- 3. Evaluate baselines (same surge=1.0 config) ---
env_ecmp = RoutingEnv(cfg)
ecmp_result = run_ecmp(env_ecmp, n_eval=50)
print(f"ECMP MLU: {ecmp_result['mean']:.4f} +/- {ecmp_result['std']:.4f}")

env_sp = RoutingEnv(cfg)
sp_result = run_sp(env_sp, n_eval=50)
print(f"SP MLU:   {sp_result['mean']:.4f} +/- {sp_result['std']:.4f}")

# --- 4. Compare ---
ratio_ecmp = gnn_result["mean"] / ecmp_result["mean"]
ratio_sp = gnn_result["mean"] / sp_result["mean"]

print(f"\n{'='*60}")
print(f"F1 Quick Test (surge={cfg.surge_factor}, 100ep, seed=0)")
print(f"  GNN/ECMP = {ratio_ecmp:.4f}  ({'PASS' if ratio_ecmp < 0.90 else 'MARGINAL/FAIL'} — target < 0.90)")
print(f"  GNN/SP   = {ratio_sp:.4f}")
print(f"")
print(f"  Old results (surge=5.0, 800ep, 3 seeds):")
print(f"    ECMP MLU=1.97, GNN/ECMP=0.818 (PASS)")
print(f"{'='*60}")

# Save results
output = {
    "test": "F1_quick_surge1.0",
    "config": {
        "surge_factor": cfg.surge_factor,
        "total_episodes": cfg.total_episodes,
        "failure_rate": cfg.failure_rate,
        "n_nodes": cfg.n_nodes,
    },
    "gnn": gnn_result,
    "ecmp": ecmp_result,
    "sp": sp_result,
    "gnn_ecmp_ratio": ratio_ecmp,
    "gnn_sp_ratio": ratio_sp,
    "train_time_s": train_time,
    "train_best_reward": result["best_reward"],
}
out_path = os.path.join(RESULTS_DIR, "f1_quick_test.json")
with open(out_path, "w") as f:
    json.dump(output, f, indent=2)
print(f"\nResults saved to {out_path}")
