#!/usr/bin/env python3
"""E10 + E11: Architecture ablation — GNN layers and attention heads.

E10: n_layers in {1, 2, 3} (default=2)
E11: n_heads  in {2, 4, 8} (default=4)

Each config: 1 seed x 800ep training + 50 eval episodes. Checkpoints saved separately.

Run from project root:
    cd /mnt/d/code/study/research-protocol
    ~/.venvs/torch/bin/python -u projects/leo-congestion-routing/run_e10_e11.py
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
from simulator.config import SimConfig
from simulator.env import RoutingEnv
from simulator.model import RoutingActorCritic
from simulator.train import evaluate, train

RESULTS_DIR = Path(__file__).resolve().parent / "simulator" / "results"
RESULTS_DIR.mkdir(exist_ok=True, parents=True)


def run_single_config(
    n_layers: int = 2,
    n_heads: int = 4,
    n_episodes: int = 800,
    n_eval: int = 50,
    tag: str = "",
) -> dict:
    """Train and evaluate a single architecture config."""
    cfg = SimConfig(
        n_layers=n_layers,
        n_heads=n_heads,
        total_episodes=n_episodes,
        n_seeds=1,
        n_eval=n_eval,
        device="cuda",
        entropy_coef=0.02,
        early_stop_patience=80,
    )

    t0 = time.time()
    print(f"\n{'='*60}")
    print(f"  {tag}: layers={n_layers}, heads={n_heads}")
    print(f"{'='*60}")

    # Train
    train_result = train(cfg, seed=0)

    # Save checkpoint with unique name to avoid overwriting E01-v3
    src = RESULTS_DIR / "ppo_best.pt"
    dst = RESULTS_DIR / f"ppo_{tag}.pt"
    if src.exists():
        import shutil
        shutil.copy2(src, dst)

    # Load best model
    env = RoutingEnv(cfg, seed=0)
    model = RoutingActorCritic(
        cfg.node_feat_dim, cfg.edge_feat_dim, cfg.hidden_dim,
        cfg.n_layers, cfg.n_heads, cfg.k_paths,
    ).to(cfg.device)
    ckpt = torch.load(
        str(src),
        map_location=cfg.device, weights_only=False,
    )
    model.load_state_dict(ckpt["model"])

    # Evaluate
    eval_result = evaluate(model, env, n_eval=n_eval, device=cfg.device)
    elapsed = time.time() - t0

    result = {
        "n_layers": n_layers,
        "n_heads": n_heads,
        "eval_mean": eval_result["mean"],
        "eval_std": eval_result["std"],
        "train_episodes": train_result["n_episodes"],
        "train_episode_mlus": train_result.get("episode_mlus", []),
        "elapsed_seconds": elapsed,
        "ckpt_path": str(dst),
    }
    print(f"  -> MLU = {eval_result['mean']:.4f} +/- {eval_result['std']:.4f} "
          f"({elapsed/60:.1f} min, {train_result['n_episodes']} ep)")
    return result


def main() -> None:
    t0 = time.time()

    # ECMP baseline (shared)
    cfg_base = SimConfig(device="cuda")
    env = RoutingEnv(cfg_base, seed=0)
    ecmp_res = run_ecmp(env, n_eval=50)
    print(f"ECMP baseline: MLU = {ecmp_res['mean']:.4f} ± {ecmp_res['std']:.4f}")

    # ═══════════════════════════════════════════════════════════════════
    # E10: GNN layers ablation {1, 2, 3}
    # ═══════════════════════════════════════════════════════════════════
    e10_results = []
    for nl in [1, 2, 3]:
        r = run_single_config(n_layers=nl, n_heads=4, tag=f"E10-L{nl}")
        r["gnn_ecmp_ratio"] = r["eval_mean"] / ecmp_res["mean"]
        e10_results.append(r)

    # ═══════════════════════════════════════════════════════════════════
    # E11: Attention heads ablation {2, 4, 8}
    # ═══════════════════════════════════════════════════════════════════
    e11_results = []
    for nh in [2, 4, 8]:
        r = run_single_config(n_layers=2, n_heads=nh, tag=f"E11-H{nh}")
        r["gnn_ecmp_ratio"] = r["eval_mean"] / ecmp_res["mean"]
        e11_results.append(r)

    # ── Save ────────────────────────────────────────────────────────────
    output = {
        "e10_layers": e10_results,
        "e11_heads": e11_results,
        "ecmp_baseline": ecmp_res,
        "elapsed_seconds": time.time() - t0,
    }

    out_path = RESULTS_DIR / "e10_e11_results.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    # ── Summary ─────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("  E10/E11 SUMMARY")
    print(f"{'='*60}")
    print(f"ECMP: MLU = {ecmp_res['mean']:.4f}")
    print("\nE10 — GNN Layers:")
    for r in e10_results:
        print(f"  L{r['n_layers']}: MLU = {r['eval_mean']:.4f}  "
              f"GNN/ECMP = {r['gnn_ecmp_ratio']:.4f}")
    print("\nE11 — Attention Heads:")
    for r in e11_results:
        print(f"  H{r['n_heads']}: MLU = {r['eval_mean']:.4f}  "
              f"GNN/ECMP = {r['gnn_ecmp_ratio']:.4f}")
    print(f"\nTotal time: {(time.time() - t0)/60:.1f} min")
    print(f"Saved to {out_path}")

    # Restore E01-v3 default checkpoint (L2_H4 was trained last, overwrite ppo_best)
    default_bak = RESULTS_DIR / "ppo_E10-L2.pt"
    if default_bak.exists():
        import shutil
        shutil.copy2(default_bak, RESULTS_DIR / "ppo_best.pt")
        print("Restored ppo_best.pt from E10-L2 (default config)")


if __name__ == "__main__":
    main()
