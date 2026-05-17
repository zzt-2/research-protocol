#!/usr/bin/env python3
"""E02 + E03: Scenario ablation experiments (evaluation-time, no retraining).

E02: failure_rate=0 — verify fault is the activation condition for GNN advantage
E03: surge_factor=20 — test extreme congestion adaptation

Uses trained GNN model from E01-v2. MLP trained fresh on default config.

Run from project root:
    cd /mnt/d/code/study/research-protocol
    ~/.venvs/torch/bin/python -u projects/leo-congestion-routing/run_e02_e03.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))

from baselines.ecmp import run_ecmp
from baselines.mlp import MLPActorCritic, _train_mlp
from simulator.config import SimConfig
from simulator.env import RoutingEnv
from simulator.model import RoutingActorCritic
from simulator.train import evaluate

RESULTS_DIR = Path(__file__).resolve().parent / "simulator" / "results"
RESULTS_DIR.mkdir(exist_ok=True, parents=True)

# Default config (same as E01-v2 training)
CFG_DEFAULT = SimConfig(
    total_episodes=800, n_seeds=1, n_eval=50, device="cuda",
    entropy_coef=0.02, early_stop_patience=80,
)

# E02: no fault
CFG_NOFAULT = SimConfig(
    total_episodes=800, n_seeds=1, n_eval=50, device="cuda",
    failure_rate=0.0, entropy_coef=0.02, early_stop_patience=80,
)

# E03: extreme surge
CFG_SURGE = SimConfig(
    total_episodes=800, n_seeds=1, n_eval=50, device="cuda",
    surge_factor=20.0, entropy_coef=0.02, early_stop_patience=80,
)


def _eval_gnn(ckpt_path: Path, cfg: SimConfig, device: str = "cuda") -> dict:
    """Evaluate best GNN checkpoint on given config."""
    env = RoutingEnv(cfg)
    model = RoutingActorCritic(
        cfg.node_feat_dim, cfg.edge_feat_dim, cfg.hidden_dim,
        cfg.n_layers, cfg.n_heads, cfg.k_paths,
    ).to(device)
    ckpt = torch.load(str(ckpt_path), map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model"])
    return evaluate(model, env, n_eval=cfg.n_eval, device=device)


def _train_and_eval_mlp(cfg: SimConfig, n_episodes: int = 300) -> dict:
    """Train MLP on default config, evaluate on given config."""
    # Train on default topology
    train_env = RoutingEnv(CFG_DEFAULT, seed=0)
    sample_obs, _ = train_env.reset(seed=0)
    mlp_feat_dim = sample_obs["mlp_feat"].shape[0]
    model = MLPActorCritic(mlp_feat_dim=mlp_feat_dim, k_paths=cfg.k_paths)
    print(f"  [MLP] Training on default config (300ep)...")
    _train_mlp(train_env, model, n_episodes=n_episodes, seed=0)

    # Evaluate on target config
    eval_env = RoutingEnv(cfg)
    mlus: list[float] = []
    for i in range(cfg.n_eval):
        obs, info = eval_env.reset(seed=300000 + i)
        done = False
        while not done:
            action, _, _ = model.get_action(obs, deterministic=True)
            obs, _, terminated, truncated, info = eval_env.step(action.item())
            done = terminated or truncated
        mlus.append(info.get("final_mlu", info["mlu"]))
    result = {"mean": float(np.mean(mlus)), "std": float(np.std(mlus))}
    print(f"  [MLP] Eval: MLU = {result['mean']:.4f} +/- {result['std']:.4f}")
    return result


def main() -> None:
    t0 = time.time()
    best_ckpt = RESULTS_DIR / "ppo_best.pt"
    if not best_ckpt.exists():
        print("ERROR: No ppo_best.pt found. Run E01-v2 first.")
        return

    scenarios = [
        ("E02_nofault", CFG_NOFAULT, "failure_rate=0%"),
        ("E03_surge", CFG_SURGE, "surge_factor=20"),
    ]
    all_results: dict = {}

    for name, cfg, desc in scenarios:
        print(f"\n{'='*60}")
        print(f"  {name}: {desc}")
        print(f"{'='*60}")

        # GNN (zero-shot from E01-v2 trained model)
        print(f"  [GNN] Evaluating trained model on {desc}...")
        gnn_res = _eval_gnn(best_ckpt, cfg)
        gnn_res["scenario"] = desc

        # ECMP
        print(f"  [ECMP] Running on {desc}...")
        ecmp_res = run_ecmp(RoutingEnv(cfg), n_eval=cfg.n_eval)

        # MLP (trained on default, eval on target)
        mlp_res = _train_and_eval_mlp(cfg)

        # Summary
        r_ecmp = gnn_res["mean"] / ecmp_res["mean"]
        r_mlp = gnn_res["mean"] / mlp_res["mean"]
        print(f"\n  {name} Summary:")
        print(f"    GNN:  {gnn_res['mean']:.4f}")
        print(f"    ECMP: {ecmp_res['mean']:.4f}")
        print(f"    MLP:  {mlp_res['mean']:.4f}")
        print(f"    GNN/ECMP = {r_ecmp:.4f}")
        print(f"    GNN/MLP  = {r_mlp:.4f}")

        all_results[name] = {
            "gnn": gnn_res,
            "ecmp": ecmp_res,
            "mlp": mlp_res,
            "ratios": {"gnn_ecmp": r_ecmp, "gnn_mlp": r_mlp},
            "config_desc": desc,
        }

    # Compare with E01-v2 default
    print(f"\n{'='*60}")
    print("  Cross-scenario comparison")
    print(f"{'='*60}")
    e01v2_path = RESULTS_DIR / "e01_v2_results.json"
    if e01v2_path.exists():
        with open(e01v2_path) as f:
            e01v2 = json.load(f)
        print(f"  E01-v2 (default):   GNN/ECMP={e01v2['ratios']['gnn_ecmp']:.4f}, "
              f"GNN/MLP={e01v2['ratios']['gnn_mlp']:.4f}")
    for name, res in all_results.items():
        print(f"  {name}: GNN/ECMP={res['ratios']['gnn_ecmp']:.4f}, "
              f"GNN/MLP={res['ratios']['gnn_mlp']:.4f}")

    all_results["elapsed_seconds"] = time.time() - t0
    print(f"\nTotal time: {(time.time()-t0)/60:.1f} min")

    out = RESULTS_DIR / "e02_e03_results.json"
    with open(out, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"Saved to {out}")


if __name__ == "__main__":
    main()
