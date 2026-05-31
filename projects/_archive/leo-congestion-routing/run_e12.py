#!/usr/bin/env python3
"""E12: Fault mode comparison — random vs regional vs cascading.

Evaluation-time ablation (no retraining). Tests GNN robustness across
different failure patterns at the same 8% failure rate.

Run from project root:
    cd /mnt/d/code/study/research-protocol
    ~/.venvs/torch/bin/python -u projects/leo-congestion-routing/run_e12.py
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
from simulator.train import evaluate

RESULTS_DIR = Path(__file__).resolve().parent / "simulator" / "results"

BASE_CFG = dict(
    total_episodes=800, n_seeds=1, n_eval=100, device="cuda",
    entropy_coef=0.02, early_stop_patience=80,
)


def _eval_gnn(ckpt_path: Path, cfg: SimConfig) -> dict:
    env = RoutingEnv(cfg)
    model = RoutingActorCritic(
        cfg.node_feat_dim, cfg.edge_feat_dim, cfg.hidden_dim,
        cfg.n_layers, cfg.n_heads, cfg.k_paths,
    ).to(cfg.device)
    ckpt = torch.load(str(ckpt_path), map_location=cfg.device, weights_only=False)
    model.load_state_dict(ckpt["model"])
    return evaluate(model, env, n_eval=cfg.n_eval, device=cfg.device)


def main() -> None:
    t0 = time.time()
    best_ckpt = RESULTS_DIR / "ppo_best.pt"
    if not best_ckpt.exists():
        print("ERROR: No ppo_best.pt. Run E01 first.")
        return

    # ── E12: Fault mode comparison ─────────────────────────────────────
    print(f"\n{'='*60}")
    print("  E12: Fault Mode Comparison (random / regional / cascading)")
    print(f"{'='*60}")

    modes = ["random", "regional", "cascading"]
    fault_rates = [0.05, 0.08, 0.10, 0.15]
    e12_results = []

    for mode in modes:
        for fr in fault_rates:
            cfg = SimConfig(failure_mode=mode, failure_rate=fr, **BASE_CFG)
            print(f"\n  mode={mode}  fault_rate={fr:.0%}")

            gnn_res = _eval_gnn(best_ckpt, cfg)
            ecmp_res = run_ecmp(RoutingEnv(cfg), n_eval=cfg.n_eval)
            gnn_ecmp_r = gnn_res["mean"] / ecmp_res["mean"]

            # Also run MLP for alt-exclusion (takes SimConfig, not RoutingEnv)
            mlp_res = run_mlp(env_config=cfg, n_eval=cfg.n_eval)
            gnn_mlp_r = gnn_res["mean"] / mlp_res["mean"]

            print(f"    GNN={gnn_res['mean']:.4f}  ECMP={ecmp_res['mean']:.4f}  "
                  f"MLP={mlp_res['mean']:.4f}")
            print(f"    GNN/ECMP={gnn_ecmp_r:.4f}  GNN/MLP={gnn_mlp_r:.4f}  "
                  f"{'PASS' if gnn_ecmp_r < 1.0 else 'FAIL'}")

            e12_results.append({
                "mode": mode,
                "fault_rate": fr,
                "gnn_mlu": gnn_res["mean"],
                "gnn_std": gnn_res.get("std", 0.0),
                "ecmp_mlu": ecmp_res["mean"],
                "mlp_mlu": mlp_res["mean"],
                "gnn_ecmp_ratio": gnn_ecmp_r,
                "gnn_mlp_ratio": gnn_mlp_r,
            })

    # ── Summary ─────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("  E12 Summary")
    print(f"{'='*60}")
    print(f"\n  {'Mode':<12} {'Rate':>6} {'GNN':>8} {'ECMP':>8} {'MLP':>8} "
          f"{'G/ECMP':>8} {'G/MLP':>8} {'Verdict':>8}")
    print("  " + "-" * 70)

    for r in e12_results:
        verdict = "GNN wins" if r["gnn_ecmp_ratio"] < 1.0 else "ECMP wins"
        print(f"  {r['mode']:<12} {r['fault_rate']:>5.0%} {r['gnn_mlu']:>8.4f} "
              f"{r['ecmp_mlu']:>8.4f} {r['mlp_mlu']:>8.4f} "
              f"{r['gnn_ecmp_ratio']:>8.4f} {r['gnn_mlp_ratio']:>8.4f} {verdict:>8}")

    results = {
        "experiment": "E12_fault_mode_comparison",
        "e12_results": e12_results,
        "elapsed_seconds": time.time() - t0,
    }
    print(f"\nTotal time: {(time.time()-t0)/60:.1f} min")

    out = RESULTS_DIR / "e12_fault_mode_results.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved to {out}")


if __name__ == "__main__":
    main()
