#!/usr/bin/env python3
"""E08 + E09: Ablation experiments (evaluation-time, no retraining).

E08: fault_rate in {0, 0.05, 0.08, 0.10, 0.15} — verify fault activation
E09: n_popular in {0, 3, 5, 10} — verify traffic uniformity effect

Run from project root:
    cd /mnt/d/code/study/research-protocol
    ~/.venvs/torch/bin/python -u projects/leo-congestion-routing/run_e08_e09.py
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
from simulator.train import evaluate

RESULTS_DIR = Path(__file__).resolve().parent / "simulator" / "results"

BASE_CFG = dict(
    total_episodes=800, n_seeds=1, n_eval=50, device="cuda",
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
        print("ERROR: No ppo_best.pt. Run E01-v2 first.")
        return

    # ── E08: Fault rate ablation ────────────────────────────────────────
    print(f"\n{'='*60}")
    print("  E08: Fault Rate Ablation")
    print(f"{'='*60}")
    fault_rates = [0.0, 0.05, 0.08, 0.10, 0.15]
    e08_results = []

    for fr in fault_rates:
        cfg = SimConfig(failure_rate=fr, **BASE_CFG)
        print(f"\n  fault_rate={fr:.0%}")
        gnn_res = _eval_gnn(best_ckpt, cfg)
        ecmp_res = run_ecmp(RoutingEnv(cfg), n_eval=cfg.n_eval)
        r = gnn_res["mean"] / ecmp_res["mean"]
        print(f"    GNN={gnn_res['mean']:.4f}  ECMP={ecmp_res['mean']:.4f}  "
              f"GNN/ECMP={r:.4f}  {'GNN wins' if r < 1.0 else 'ECMP wins'}")
        e08_results.append({
            "fault_rate": fr,
            "gnn_mlu": gnn_res["mean"],
            "ecmp_mlu": ecmp_res["mean"],
            "gnn_ecmp_ratio": r,
        })

    # ── E09: Traffic uniformity ablation ────────────────────────────────
    print(f"\n{'='*60}")
    print("  E09: Traffic Uniformity Ablation")
    print(f"{'='*60}")
    # Vary hotspot destination count (n_popular) and heavy flow count
    traffic_configs = [
        {"n_popular": 0, "n_heavy": 0, "label": "uniform (no hotspot, no heavy)"},
        {"n_popular": 3, "n_heavy": 5, "label": "moderate (3 hotspot, 5 heavy)"},
        {"n_popular": 3, "n_heavy": 10, "label": "default (3 hotspot, 10 heavy)"},
        {"n_popular": 5, "n_heavy": 15, "label": "high (5 hotspot, 15 heavy)"},
    ]
    e09_results = []

    for tc in traffic_configs:
        cfg = SimConfig(
            n_popular=tc["n_popular"], n_heavy=tc["n_heavy"],
            failure_rate=0.08, **BASE_CFG,
        )
        print(f"\n  {tc['label']}")
        gnn_res = _eval_gnn(best_ckpt, cfg)
        ecmp_res = run_ecmp(RoutingEnv(cfg), n_eval=cfg.n_eval)
        r = gnn_res["mean"] / ecmp_res["mean"]
        print(f"    GNN={gnn_res['mean']:.4f}  ECMP={ecmp_res['mean']:.4f}  "
              f"GNN/ECMP={r:.4f}  {'GNN wins' if r < 1.0 else 'ECMP wins'}")
        e09_results.append({
            "label": tc["label"],
            "n_popular": tc["n_popular"],
            "n_heavy": tc["n_heavy"],
            "gnn_mlu": gnn_res["mean"],
            "ecmp_mlu": ecmp_res["mean"],
            "gnn_ecmp_ratio": r,
        })

    # ── Summary ─────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("  Ablation Summary")
    print(f"{'='*60}")
    print(f"\n  E08 Fault Rate:")
    for r in e08_results:
        marker = " <-- crossover" if abs(r["gnn_ecmp_ratio"] - 1.0) < 0.02 else ""
        print(f"    {r['fault_rate']:.0%}: GNN/ECMP={r['gnn_ecmp_ratio']:.4f}{marker}")

    print(f"\n  E09 Traffic Uniformity:")
    for r in e09_results:
        print(f"    {r['label']}: GNN/ECMP={r['gnn_ecmp_ratio']:.4f}")

    results = {
        "e08_fault_rate": e08_results,
        "e09_traffic_uniformity": e09_results,
        "elapsed_seconds": time.time() - t0,
    }
    print(f"\nTotal time: {(time.time()-t0)/60:.1f} min")

    out = RESULTS_DIR / "e08_e09_results.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved to {out}")


if __name__ == "__main__":
    main()
