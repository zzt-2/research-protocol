#!/usr/bin/env python3
"""E05 + E06: Full-scale generalization experiments.

E05: 66→288 nodes (4.4× scale, 24 planes × 12 sats)
E06: 66→720 nodes (10.9× scale, 36 planes × 20 sats)

Uses trained GNN model from E01-v2. MLP trained on 66-node default config.

Run from project root:
    cd /mnt/d/code/study/research-protocol
    ~/.venvs/torch/bin/python -u projects/leo-congestion-routing/run_e05_e06.py
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

# Default 66-node config for MLP training reference
CFG_66 = SimConfig(
    total_episodes=800, n_seeds=1, n_eval=50, device="cuda",
    entropy_coef=0.02, early_stop_patience=80,
)

# E05: 288 nodes (4.4× scale) — scale flows proportionally
CFG_288 = SimConfig.from_n_nodes(
    288,
    n_flows=175, n_heavy=44,                 # scaled from 40/10
    total_episodes=800, n_seeds=1, n_eval=50, device="cuda",
    entropy_coef=0.02, early_stop_patience=80,
)

# E06: 720 nodes (10.9× scale) — cap flows at 200 for tractability
CFG_720 = SimConfig.from_n_nodes(
    720,
    n_flows=200, n_heavy=50,                 # scaled but capped
    total_episodes=800, n_seeds=1, n_eval=50, device="cuda",
    entropy_coef=0.02, early_stop_patience=80,
)


def _eval_gnn(ckpt_path: Path, cfg: SimConfig) -> dict:
    """Evaluate best GNN checkpoint on given config."""
    env = RoutingEnv(cfg)
    model = RoutingActorCritic(
        cfg.node_feat_dim, cfg.edge_feat_dim, cfg.hidden_dim,
        cfg.n_layers, cfg.n_heads, cfg.k_paths,
    ).to(cfg.device)
    ckpt = torch.load(str(ckpt_path), map_location=cfg.device, weights_only=False)
    model.load_state_dict(ckpt["model"])
    return evaluate(model, env, n_eval=cfg.n_eval, device=cfg.device)


def _train_mlp_on_default() -> MLPActorCritic:
    """Train MLP on 66-node default config, return model."""
    env = RoutingEnv(CFG_66, seed=0)
    sample_obs, _ = env.reset(seed=0)
    mlp_feat_dim = sample_obs["mlp_feat"].shape[0]
    model = MLPActorCritic(mlp_feat_dim=mlp_feat_dim, k_paths=CFG_66.k_paths)
    print("[MLP-66] Training on 66-node (300ep)...")
    _train_mlp(env, model, n_episodes=300, seed=0)
    return model


def _eval_mlp_on(model: MLPActorCritic, cfg: SimConfig, n_eval: int = 50) -> dict:
    """Evaluate saved MLP model on given config."""
    env = RoutingEnv(cfg)
    mlus: list[float] = []
    for i in range(n_eval):
        obs, info = env.reset(seed=500000 + i)
        done = False
        while not done:
            action, _, _ = model.get_action(obs, deterministic=True)
            obs, _, terminated, truncated, info = env.step(action.item())
            done = terminated or truncated
        mlus.append(info.get("final_mlu", info["mlu"]))
    result = {"mean": float(np.mean(mlus)), "std": float(np.std(mlus))}
    print(f"  [MLP] Eval: MLU = {result['mean']:.4f} +/- {result['std']:.4f}")
    return result


def main() -> None:
    t0 = time.time()
    best_ckpt = RESULTS_DIR / "ppo_best.pt"
    if not best_ckpt.exists():
        print("ERROR: No ppo_best.pt. Run E01-v2 first.")
        return

    # Train MLP once on 66-node
    mlp_model = _train_mlp_on_default()

    scenarios = [
        ("E05_288", CFG_288, "288 nodes (24x12, 4.4x scale)"),
        ("E06_720", CFG_720, "720 nodes (36x20, 10.9x scale)"),
    ]
    all_results: dict = {}

    for name, cfg, desc in scenarios:
        print(f"\n{'='*60}")
        print(f"  {name}: {desc}")
        print(f"  n_nodes={cfg.n_nodes}, n_flows={cfg.n_flows}")
        print(f"{'='*60}")

        # GNN zero-shot
        print(f"  [GNN] Zero-shot eval...")
        gnn_res = _eval_gnn(best_ckpt, cfg)

        # ECMP
        print(f"  [ECMP] Running...")
        ecmp_res = run_ecmp(RoutingEnv(cfg), n_eval=cfg.n_eval)

        # MLP zero-shot
        print(f"  [MLP] Zero-shot eval...")
        mlp_res = _eval_mlp_on(mlp_model, cfg, n_eval=cfg.n_eval)

        # Summary
        r_ecmp = gnn_res["mean"] / ecmp_res["mean"]
        r_mlp = gnn_res["mean"] / mlp_res["mean"]
        gen_gap = r_ecmp  # generalization gap: GNN_MLU / ECMP_MLU on target scale

        print(f"\n  {name} Summary:")
        print(f"    GNN:  {gnn_res['mean']:.4f} +/- {gnn_res['std']:.4f}")
        print(f"    ECMP: {ecmp_res['mean']:.4f} +/- {ecmp_res['std']:.4f}")
        print(f"    MLP:  {mlp_res['mean']:.4f} +/- {mlp_res['std']:.4f}")
        print(f"    GNN/ECMP = {r_ecmp:.4f}  {'PASS' if r_ecmp <= 1.10 else 'FAIL'} (target <= 1.10)")
        print(f"    GNN/MLP  = {r_mlp:.4f}")
        print(f"    MLP/ECMP = {mlp_res['mean']/ecmp_res['mean']:.4f}  (MLP collapse if > 1.10)")

        all_results[name] = {
            "gnn": gnn_res,
            "ecmp": ecmp_res,
            "mlp": mlp_res,
            "ratios": {"gnn_ecmp": r_ecmp, "gnn_mlp": r_mlp},
            "generalization_gap": gen_gap,
            "config_desc": desc,
            "n_nodes": cfg.n_nodes,
            "scale_factor": cfg.n_nodes / 66,
        }

    # Cross-scale summary
    print(f"\n{'='*60}")
    print("  Cross-scale generalization summary")
    print(f"{'='*60}")
    print(f"  {'Scale':<12} {'Nodes':<8} {'GNN/ECMP':<12} {'GNN/MLP':<12} {'MLP/ECMP':<12} {'Gen PASS'}")
    # Include E04 data
    e04_path = RESULTS_DIR / "e04_quick_results.json"
    if e04_path.exists():
        with open(e04_path) as f:
            e04 = json.load(f)
        s = e04["summary"]
        print(f"  {'0.7x (E04)':<12} {'48':<8} {s['gnn_over_ecmp']:<12.4f} "
              f"{s['gnn_over_mlp_zeroshot']:<12.4f} "
              f"{'—':<12} {'YES' if s['gnn_over_ecmp'] <= 1.10 else 'NO'}")
    for name, res in all_results.items():
        sf = res["scale_factor"]
        r = res["ratios"]
        mlp_ecmp = res["mlp"]["mean"] / res["ecmp"]["mean"]
        gen_pass = "YES" if r["gnn_ecmp"] <= 1.10 else "NO"
        print(f"  {sf:.1f}x ({name[:6]})  {res['n_nodes']:<8} {r['gnn_ecmp']:<12.4f} "
              f"{r['gnn_mlp']:<12.4f} {mlp_ecmp:<12.4f} {gen_pass}")

    all_results["elapsed_seconds"] = time.time() - t0
    print(f"\nTotal time: {(time.time()-t0)/60:.1f} min")

    out = RESULTS_DIR / "e05_e06_results.json"
    with open(out, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"Saved to {out}")


if __name__ == "__main__":
    main()
