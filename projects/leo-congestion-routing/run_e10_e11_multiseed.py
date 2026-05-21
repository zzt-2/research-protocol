#!/usr/bin/env python3
"""E10 + E11: Multi-seed architecture ablation (3 seeds per config).

E10: n_layers in {1, 2, 3} (default=2)
E11: n_heads  in {2, 4, 8} (default=4)

Each config: 3 seeds x 800ep training + 50 eval episodes.

Run from project root:
    cd /mnt/d/code/study/research-protocol
    ~/.venvs/torch/bin/python -u projects/leo-congestion-routing/run_e10_e11_multiseed.py
"""
from __future__ import annotations

import json
import shutil
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))

from baselines.ecmp import run_ecmp
from simulator.config import SimConfig
from simulator.env import RoutingEnv
from simulator.model import RoutingActorCritic
from simulator.train import evaluate, train

RESULTS_DIR = Path(__file__).resolve().parent / "simulator" / "results"
RESULTS_DIR.mkdir(exist_ok=True, parents=True)

SEEDS = [0, 1, 2]


def run_single_seed(
    n_layers: int,
    n_heads: int,
    seed: int,
    tag: str,
    n_episodes: int = 800,
    n_eval: int = 50,
) -> dict:
    cfg = SimConfig(
        n_layers=n_layers,
        n_heads=n_heads,
        total_episodes=n_episodes,
        n_seeds=1,
        n_eval=n_eval,
        device="cuda",
        entropy_coef=0.02,
        early_stop_patience=80,
        seed=seed,
    )

    # Back up existing ppo_best.pt so training starts fresh
    best_ckpt = RESULTS_DIR / "ppo_best.pt"
    backup_ckpt = RESULTS_DIR / "ppo_best_backup.pt"
    if best_ckpt.exists():
        shutil.move(str(best_ckpt), str(backup_ckpt))

    train_result = train(cfg, seed=seed)

    # Save new checkpoint with unique name
    src = RESULTS_DIR / "ppo_best.pt"
    dst = RESULTS_DIR / f"ppo_{tag}_s{seed}.pt"
    if src.exists():
        shutil.copy2(src, dst)

    # Evaluate
    env = RoutingEnv(cfg, seed=seed)
    model = RoutingActorCritic(
        cfg.node_feat_dim, cfg.edge_feat_dim, cfg.hidden_dim,
        cfg.n_layers, cfg.n_heads, cfg.k_paths,
    ).to(cfg.device)
    ckpt = torch.load(str(src), map_location=cfg.device, weights_only=False)
    model.load_state_dict(ckpt["model"])
    eval_result = evaluate(model, env, n_eval=n_eval, device=cfg.device)

    return {
        "seed": seed,
        "eval_mean": eval_result["mean"],
        "eval_std": eval_result["std"],
        "train_episodes": train_result["n_episodes"],
    }


def run_multiseed_config(n_layers: int, n_heads: int, tag: str) -> dict:
    print(f"\n  {tag}: layers={n_layers}, heads={n_heads}, seeds={SEEDS}")
    seed_results = []
    for s in SEEDS:
        t0 = time.time()
        r = run_single_seed(n_layers, n_heads, s, tag)
        elapsed = time.time() - t0
        print(f"    seed={s}: MLU={r['eval_mean']:.4f} ({elapsed/60:.1f} min)")
        seed_results.append(r)

    means = [r["eval_mean"] for r in seed_results]
    return {
        "n_layers": n_layers,
        "n_heads": n_heads,
        "seeds": seed_results,
        "mean_across_seeds": float(np.mean(means)),
        "std_across_seeds": float(np.std(means)),
    }


def main() -> None:
    t0 = time.time()

    # ECMP baseline (multi-seed)
    ecmp_mlus = []
    for s in SEEDS:
        cfg = SimConfig(device="cuda", seed=s)
        env = RoutingEnv(cfg, seed=s)
        ecmp_res = run_ecmp(env, n_eval=50)
        ecmp_mlus.append(ecmp_res["mean"])
    ecmp_mean = float(np.mean(ecmp_mlus))
    ecmp_std = float(np.std(ecmp_mlus))
    print(f"ECMP baseline: MLU = {ecmp_mean:.4f} ± {ecmp_std:.4f} (3 seeds)")

    # E10: GNN layers
    print(f"\n{'='*60}")
    print("  E10: GNN Layers Ablation (3 seeds)")
    print(f"{'='*60}")
    e10_results = []
    for nl in [1, 2, 3]:
        r = run_multiseed_config(n_layers=nl, n_heads=4, tag=f"E10-L{nl}")
        r["gnn_ecmp_ratio"] = r["mean_across_seeds"] / ecmp_mean
        e10_results.append(r)

    # E11: Attention heads
    print(f"\n{'='*60}")
    print("  E11: Attention Heads Ablation (3 seeds)")
    print(f"{'='*60}")
    e11_results = []
    for nh in [2, 4, 8]:
        r = run_multiseed_config(n_layers=2, n_heads=nh, tag=f"E11-H{nh}")
        r["gnn_ecmp_ratio"] = r["mean_across_seeds"] / ecmp_mean
        e11_results.append(r)

    # Save
    output = {
        "experiment": "E10_E11_multiseed",
        "seeds": SEEDS,
        "e10_layers": e10_results,
        "e11_heads": e11_results,
        "ecmp_baseline": {"mean": ecmp_mean, "std": ecmp_std, "per_seed": ecmp_mlus},
        "elapsed_seconds": time.time() - t0,
    }
    out_path = RESULTS_DIR / "e10_e11_multiseed_results.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    # Summary
    print(f"\n{'='*60}")
    print("  E10/E11 MULTI-SEED SUMMARY")
    print(f"{'='*60}")
    print(f"ECMP: MLU = {ecmp_mean:.4f} ± {ecmp_std:.4f}")
    print("\nE10 — GNN Layers:")
    for r in e10_results:
        print(f"  L{r['n_layers']}: MLU = {r['mean_across_seeds']:.4f} ± {r['std_across_seeds']:.4f}  "
              f"GNN/ECMP = {r['gnn_ecmp_ratio']:.4f}")
    print("\nE11 — Attention Heads:")
    for r in e11_results:
        print(f"  H{r['n_heads']}: MLU = {r['mean_across_seeds']:.4f} ± {r['std_across_seeds']:.4f}  "
              f"GNN/ECMP = {r['gnn_ecmp_ratio']:.4f}")
    print(f"\nTotal time: {(time.time() - t0)/60:.1f} min")
    print(f"Saved to {out_path}")

    # Restore original checkpoint
    backup_ckpt = RESULTS_DIR / "ppo_best_backup.pt"
    if backup_ckpt.exists():
        shutil.copy2(backup_ckpt, RESULTS_DIR / "ppo_best.pt")
        backup_ckpt.unlink()
        print("Restored original ppo_best.pt")


if __name__ == "__main__":
    main()
