#!/usr/bin/env python3
"""E01-v2 re-run: 800ep + entropy_coef=0.02 to fix seed sensitivity.

Addresses D17 analysis: seed 0 undertrained, entropy too low for exploration.

Run from project root:
    cd /mnt/d/code/study/research-protocol
    ~/.venvs/torch/bin/python -u projects/leo-congestion-routing/run_e01_v2.py
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
from baselines.mlp import run_mlp
from simulator.config import SimConfig
from simulator.env import RoutingEnv
from simulator.model import RoutingActorCritic
from simulator.train import evaluate, train

RESULTS_DIR = Path(__file__).resolve().parent / "simulator" / "results"
RESULTS_DIR.mkdir(exist_ok=True, parents=True)


def main() -> None:
    t0 = time.time()

    # Key changes from E01: more episodes + higher entropy for exploration
    cfg = SimConfig(
        total_episodes=800,
        n_seeds=3,
        n_eval=50,
        device="cuda",
        entropy_coef=0.02,       # was 0.01 — encourage more exploration
        early_stop_patience=80,  # was 50 — give more room for recovery
    )

    print(f"E01-v2 config: {cfg.n_seeds} seeds x {cfg.total_episodes}ep, "
          f"entropy_coef={cfg.entropy_coef}, early_stop={cfg.early_stop_patience}")

    # ── ECMP (deterministic) ────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("  ECMP Baseline")
    print(f"{'='*60}")
    ecmp_res = run_ecmp(RoutingEnv(cfg), n_eval=cfg.n_eval)
    print(f"ECMP: MLU = {ecmp_res['mean']:.4f} +/- {ecmp_res['std']:.4f}")

    # ── GNN (3 seeds x 800ep) ──────────────────────────────────────────
    gnn_eval: list[dict] = []
    for seed in range(cfg.n_seeds):
        print(f"\n{'='*60}")
        print(f"  GNN seed {seed}/{cfg.n_seeds}")
        print(f"{'='*60}")
        train(cfg, seed=seed)

        env = RoutingEnv(cfg, seed=seed)
        model = RoutingActorCritic(
            cfg.node_feat_dim, cfg.edge_feat_dim, cfg.hidden_dim,
            cfg.n_layers, cfg.n_heads, cfg.k_paths,
        ).to(cfg.device)

        ckpt = torch.load(
            str(RESULTS_DIR / "ppo_best.pt"),
            map_location=cfg.device, weights_only=False,
        )
        model.load_state_dict(ckpt["model"])

        ev = evaluate(model, env, n_eval=cfg.n_eval, device=cfg.device)
        ev["seed"] = seed
        gnn_eval.append(ev)

    # ── MLP (3 seeds x 800ep, same as GNN) ────────────────────────────────
    print(f"\n{'='*60}")
    print("  MLP Baseline")
    print(f"{'='*60}")
    mlp_eval: list[dict] = []
    for seed in range(cfg.n_seeds):
        mr = run_mlp(cfg, n_eval=cfg.n_eval, seed=seed, n_episodes=cfg.total_episodes)
        mlp_eval.append(mr)

    # ── Summary ─────────────────────────────────────────────────────────
    gnn_m = float(np.mean([r["mean"] for r in gnn_eval]))
    gnn_s = float(np.std([r["mean"] for r in gnn_eval]))
    ecmp_m = ecmp_res["mean"]
    mlp_m = float(np.mean([r["mean"] for r in mlp_eval]))
    mlp_s = float(np.std([r["mean"] for r in mlp_eval]))

    r_ecmp = gnn_m / ecmp_m
    r_mlp = gnn_m / mlp_m
    c_ecmp = "PASS" if r_ecmp <= 0.90 else "FAIL"
    c_mlp = "PASS" if r_mlp <= 0.85 else "FAIL"

    print(f"\n{'='*60}")
    print("  E01-v2 RESULTS (800ep, entropy=0.02)")
    print(f"{'='*60}")
    print(f"GNN:  MLU = {gnn_m:.4f} +/- {gnn_s:.4f}")
    print(f"ECMP: MLU = {ecmp_m:.4f} +/- {ecmp_res['std']:.4f}")
    print(f"MLP:  MLU = {mlp_m:.4f} +/- {mlp_s:.4f}")
    print(f"GNN/ECMP = {r_ecmp:.4f}  [{c_ecmp}] (target <= 0.90)")
    print(f"GNN/MLP  = {r_mlp:.4f}  [{c_mlp}] (target <= 0.85)")
    print(f"Total time: {(time.time() - t0)/60:.1f} min")

    # Compare with E01 original
    e01_path = RESULTS_DIR / "e01_results.json"
    if e01_path.exists():
        with open(e01_path) as f:
            e01 = json.load(f)
        old_r = e01["ratios"]
        print(f"\nE01 original: GNN/ECMP={old_r['gnn_ecmp']:.4f}, GNN/MLP={old_r['gnn_mlp']:.4f}")
        print(f"E01-v2 delta: ECMP {r_ecmp - old_r['gnn_ecmp']:+.4f}, MLP {r_mlp - old_r['gnn_mlp']:+.4f}")

    e01v2 = {
        "gnn": {"mean": gnn_m, "std": gnn_s, "seeds": gnn_eval},
        "ecmp": ecmp_res,
        "mlp": {"mean": mlp_m, "std": mlp_s, "seeds": mlp_eval},
        "ratios": {"gnn_ecmp": r_ecmp, "gnn_mlp": r_mlp},
        "criteria": {"gnn_ecmp_le_0.90": c_ecmp, "gnn_mlp_le_0.85": c_mlp},
        "config": {"total_episodes": cfg.total_episodes, "entropy_coef": cfg.entropy_coef},
        "elapsed_seconds": time.time() - t0,
    }
    out = RESULTS_DIR / "e01_v2_results.json"
    with open(out, "w") as f:
        json.dump(e01v2, f, indent=2)
    print(f"\nSaved to {out}")


if __name__ == "__main__":
    main()
