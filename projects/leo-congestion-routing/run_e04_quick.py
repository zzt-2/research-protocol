#!/usr/bin/env python3
"""E04 quick generalization validation: 66-node trained model → 48-node zero-shot.

Tests whether GNN generalizes better than MLP to different topology sizes.

Run from project root:
    cd /mnt/d/code/study/research-protocol
    ~/.venvs/torch/bin/python -u projects/leo-congestion-routing/run_e04_quick.py
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
from baselines.mlp import MLPActorCritic, run_mlp, _train_mlp
from simulator.config import SimConfig
from simulator.env import RoutingEnv
from simulator.model import RoutingActorCritic
from simulator.train import evaluate

RESULTS_DIR = Path(__file__).resolve().parent / "simulator" / "results"
RESULTS_DIR.mkdir(exist_ok=True, parents=True)

# 48-node topology: 6 planes × 8 sats = 48
CFG_48 = SimConfig(n_planes=6, sats_per_plane=8, total_episodes=500, n_seeds=1, n_eval=50, device="cuda")
CFG_66 = SimConfig(total_episodes=500, n_seeds=3, n_eval=50, device="cuda")


def _train_and_save_mlp_66() -> MLPActorCritic:
    """Train MLP on 66-node topology and return the model."""
    env = RoutingEnv(CFG_66, seed=0)
    sample_obs, _ = env.reset(seed=0)
    mlp_feat_dim = sample_obs["mlp_feat"].shape[0]
    model = MLPActorCritic(mlp_feat_dim=mlp_feat_dim, k_paths=CFG_66.k_paths)
    print("[MLP-66] Training on 66-node topology (300ep)...")
    _train_mlp(env, model, n_episodes=300, seed=0)
    return model


def _eval_mlp_on(model: MLPActorCritic, env: RoutingEnv, n_eval: int = 50) -> dict:
    """Evaluate saved MLP model on given env."""
    mlus: list[float] = []
    for i in range(n_eval):
        obs, info = env.reset(seed=400000 + i)
        done = False
        while not done:
            action, _, _ = model.get_action(obs, deterministic=True)
            obs, _, terminated, truncated, info = env.step(action.item())
            done = terminated or truncated
        mlus.append(info.get("final_mlu", info["mlu"]))
    result = {"mean": float(np.mean(mlus)), "std": float(np.std(mlus))}
    print(f"  MLU = {result['mean']:.4f} +/- {result['std']:.4f}")
    return result


def main() -> None:
    t0 = time.time()
    print(f"E04 Quick Generalization: 66-node → 48-node zero-shot")
    print(f"  48-node config: {CFG_48.n_planes}x{CFG_48.sats_per_plane} = {CFG_48.n_nodes} nodes")

    results: dict = {}

    # ── 1. ECMP on 48-node (deterministic, fast) ───────────────────────
    print(f"\n{'='*60}")
    print("  ECMP on 48-node")
    print(f"{'='*60}")
    env48 = RoutingEnv(CFG_48)
    ecmp_48 = run_ecmp(env48, n_eval=50)
    results["ecmp_48"] = ecmp_48

    # ── 2. GNN zero-shot: 66→48 ────────────────────────────────────────
    print(f"\n{'='*60}")
    print("  GNN zero-shot: 66-node → 48-node")
    print(f"{'='*60}")
    best_ckpt = RESULTS_DIR / "ppo_best.pt"
    if not best_ckpt.exists():
        # Try seed-specific checkpoints
        for s in range(3):
            alt = RESULTS_DIR / f"ppo_seed{s}.pt"
            if alt.exists():
                best_ckpt = alt
                break

    gnn_48_seeds = []
    for seed in range(3):
        # Try each seed's checkpoint
        ckpt_path = RESULTS_DIR / f"ppo_seed{seed}.pt"
        if not ckpt_path.exists():
            ckpt_path = best_ckpt

        env48_s = RoutingEnv(CFG_48, seed=seed)
        model = RoutingActorCritic(
            CFG_48.node_feat_dim, CFG_48.edge_feat_dim, CFG_48.hidden_dim,
            CFG_48.n_layers, CFG_48.n_heads, CFG_48.k_paths,
        ).to(CFG_48.device)

        ckpt = torch.load(str(ckpt_path), map_location=CFG_48.device, weights_only=False)
        model.load_state_dict(ckpt["model"])

        ev = evaluate(model, env48_s, n_eval=50, device=CFG_48.device)
        ev["source_seed"] = seed
        gnn_48_seeds.append(ev)
    results["gnn_48_zeroshot"] = gnn_48_seeds

    # ── 3. MLP zero-shot: 66→48 ────────────────────────────────────────
    print(f"\n{'='*60}")
    print("  MLP zero-shot: 66-node → 48-node")
    print(f"{'='*60}")
    mlp_66 = _train_and_save_mlp_66()
    env48_mlp = RoutingEnv(CFG_48)
    mlp_48_zeroshot = _eval_mlp_on(mlp_66, env48_mlp, n_eval=50)
    results["mlp_48_zeroshot"] = mlp_48_zeroshot

    # ── 4. MLP trained on 48-node (baseline for comparison) ────────────
    print(f"\n{'='*60}")
    print("  MLP trained on 48-node")
    print(f"{'='*60}")
    mlp_48_trained = run_mlp(CFG_48, n_eval=50, seed=0, n_episodes=300)
    results["mlp_48_trained"] = mlp_48_trained

    # ── Summary ─────────────────────────────────────────────────────────
    gnn_48_mean = float(np.mean([r["mean"] for r in gnn_48_seeds]))
    ecmp_48_mean = ecmp_48["mean"]
    mlp_48_zs_mean = mlp_48_zeroshot["mean"]
    mlp_48_tr_mean = mlp_48_trained["mean"]

    print(f"\n{'='*60}")
    print("  E04 RESULTS: 48-node generalization")
    print(f"{'='*60}")
    print(f"GNN zero-shot (66→48):  {gnn_48_mean:.4f}")
    print(f"MLP zero-shot (66→48):  {mlp_48_zs_mean:.4f}")
    print(f"MLP trained on 48:      {mlp_48_tr_mean:.4f}")
    print(f"ECMP on 48:             {ecmp_48_mean:.4f}")
    print(f"")
    print(f"GNN/ECMP = {gnn_48_mean/ecmp_48_mean:.4f}")
    print(f"GNN/MLP_zer shot = {gnn_48_mean/mlp_48_zs_mean:.4f}")
    print(f"MLP_zer shot/MLP_trained = {mlp_48_zs_mean/mlp_48_tr_mean:.4f} (MLP泛化退化)")
    print(f"Total time: {(time.time()-t0)/60:.1f} min")

    # Key metric: does GNN generalize better than MLP?
    gnn_generalizes = gnn_48_mean / ecmp_48_mean < 0.90
    mlp_collapses = mlp_48_zs_mean > ecmp_48_mean * 1.1
    print(f"\nGNN generalization (GNN/ECMP<0.90 on 48-node): {'YES' if gnn_generalizes else 'NO'}")
    print(f"MLP collapse (MLP_zer shot>ECMP*1.1): {'YES' if mlp_collapses else 'NO'}")

    if mlp_collapses and not (gnn_48_mean > ecmp_48_mean):
        print("\n>>> KEY FINDING: MLP collapses on unseen topology, GNN remains effective <<<")
        print(">>> This strengthens the case for message passing, mitigating GNN/MLP=0.86 on same-scale <<<")

    results["summary"] = {
        "gnn_48_mean": gnn_48_mean,
        "mlp_48_zeroshot_mean": mlp_48_zs_mean,
        "mlp_48_trained_mean": mlp_48_tr_mean,
        "ecmp_48_mean": ecmp_48_mean,
        "gnn_over_ecmp": gnn_48_mean / ecmp_48_mean,
        "gnn_over_mlp_zeroshot": gnn_48_mean / mlp_48_zs_mean,
        "mlp_zeroshot_over_trained": mlp_48_zs_mean / mlp_48_tr_mean,
    }
    results["elapsed_seconds"] = time.time() - t0

    out = RESULTS_DIR / "e04_quick_results.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved to {out}")


if __name__ == "__main__":
    main()
