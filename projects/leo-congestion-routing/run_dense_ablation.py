#!/usr/bin/env python3
"""Dense ablation sweeps: granular fault rates + traffic patterns.

Uses the E01-v2 trained model (66 nodes, seed 0) for zero-shot evaluation.
No retraining needed — just evaluate under varied conditions.

Run from project root:
    cd /mnt/d/code/study/research-protocol
    ~/.venvs/torch/bin/python -u projects/leo-congestion-routing/run_dense_ablation.py
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

RESULTS_DIR = Path(__file__).resolve().parent / "simulator" / "results"


def load_gnn_model(cfg: SimConfig) -> RoutingActorCritic:
    model = RoutingActorCritic(
        cfg.node_feat_dim, cfg.edge_feat_dim, cfg.hidden_dim,
        cfg.n_layers, cfg.n_heads, cfg.k_paths,
    ).to(cfg.device)
    ckpt = torch.load(
        str(RESULTS_DIR / "ppo_best.pt"),
        map_location=cfg.device, weights_only=False,
    )
    model.load_state_dict(ckpt["model"])
    model.eval()
    return model


def eval_gnn(model, cfg, n_eval=50, seed_offset=0) -> dict:
    env = RoutingEnv(cfg, seed=0)
    mlus = []
    for i in range(n_eval):
        obs, info = env.reset(seed=seed_offset + i)
        done = False
        while not done:
            action, _, _ = model.get_action(obs, deterministic=True)
            obs, _, terminated, truncated, info = env.step(action.item())
            done = terminated or truncated
        mlus.append(info.get("final_mlu", info["mlu"]))
    return {"mean": float(np.mean(mlus)), "std": float(np.std(mlus)), "mlus": mlus}


def eval_ecmp(cfg, n_eval=50, seed_offset=0) -> dict:
    env = RoutingEnv(cfg, seed=0)
    return run_ecmp(env, n_eval=n_eval)


def main() -> None:
    t0 = time.time()

    base_cfg = SimConfig(device="cuda")
    model = load_gnn_model(base_cfg)

    # ═══════════════════════════════════════════════════════════════════
    # A. Dense fault rate sweep: 0, 2, 4, 6, 8, 10, 12, 15 (%)
    # ═══════════════════════════════════════════════════════════════════
    fault_rates = [0.0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.15]
    fault_results = []

    print("=" * 60)
    print("  Dense Fault Rate Sweep (8 points)")
    print("=" * 60)

    for fr in fault_rates:
        cfg = SimConfig(failure_rate=fr, device="cuda")
        gnn_res = eval_gnn(model, cfg, n_eval=50, seed_offset=100000)
        ecmp_res = eval_ecmp(cfg, n_eval=50, seed_offset=100000)
        ratio = gnn_res["mean"] / ecmp_res["mean"]
        fault_results.append({
            "fault_rate": fr,
            "fault_rate_pct": fr * 100,
            "gnn_mlu": gnn_res["mean"],
            "gnn_std": gnn_res["std"],
            "ecmp_mlu": ecmp_res["mean"],
            "ecmp_std": ecmp_res["std"],
            "gnn_ecmp_ratio": ratio,
        })
        print(f"  fault={fr*100:5.1f}%: GNN={gnn_res['mean']:.4f} "
              f"ECMP={ecmp_res['mean']:.4f} ratio={ratio:.4f}")

    # ═══════════════════════════════════════════════════════════════════
    # B. Dense traffic pattern sweep
    # ═══════════════════════════════════════════════════════════════════
    traffic_configs = [
        {"n_heavy": 0, "n_popular": 0, "label": "uniform"},
        {"n_heavy": 3, "n_popular": 1, "label": "light"},
        {"n_heavy": 5, "n_popular": 2, "label": "moderate-light"},
        {"n_heavy": 8, "n_popular": 3, "label": "moderate"},
        {"n_heavy": 10, "n_popular": 3, "label": "default"},
        {"n_heavy": 13, "n_popular": 4, "label": "moderate-heavy"},
        {"n_heavy": 15, "n_popular": 5, "label": "heavy"},
        {"n_heavy": 20, "n_popular": 6, "label": "very-heavy"},
    ]
    traffic_results = []

    print("\n" + "=" * 60)
    print("  Dense Traffic Pattern Sweep (8 points)")
    print("=" * 60)

    for tc in traffic_configs:
        cfg = SimConfig(n_heavy=tc["n_heavy"], n_popular=tc["n_popular"], device="cuda")
        gnn_res = eval_gnn(model, cfg, n_eval=50, seed_offset=200000)
        ecmp_res = eval_ecmp(cfg, n_eval=50, seed_offset=200000)
        ratio = gnn_res["mean"] / ecmp_res["mean"]
        traffic_results.append({
            "label": tc["label"],
            "n_heavy": tc["n_heavy"],
            "n_popular": tc["n_popular"],
            "gnn_mlu": gnn_res["mean"],
            "gnn_std": gnn_res["std"],
            "ecmp_mlu": ecmp_res["mean"],
            "ecmp_std": ecmp_res["std"],
            "gnn_ecmp_ratio": ratio,
        })
        print(f"  {tc['label']:18s}: GNN={gnn_res['mean']:.4f} "
              f"ECMP={ecmp_res['mean']:.4f} ratio={ratio:.4f}")

    # ═══════════════════════════════════════════════════════════════════
    # C. Dense scale sweep: add intermediate constellation sizes
    # ═══════════════════════════════════════════════════════════════════
    scale_configs = [
        {"planes": 4, "sats": 12, "label": "48 (0.7×)"},
        {"planes": 6, "sats": 11, "label": "66 (1.0×, train)"},
        {"planes": 8, "sats": 12, "label": "96 (1.5×)"},
        {"planes": 12, "sats": 12, "label": "144 (2.2×)"},
        {"planes": 12, "sats": 24, "label": "288 (4.4×)"},
        {"planes": 20, "sats": 24, "label": "480 (7.3×)"},
        {"planes": 36, "sats": 20, "label": "720 (10.9×)"},
    ]
    scale_results = []

    print("\n" + "=" * 60)
    print("  Dense Scale Sweep (7 points)")
    print("=" * 60)

    for sc in scale_configs:
        n_nodes = sc["planes"] * sc["sats"]
        scale_f = n_nodes / 66.0
        cfg = SimConfig(
            n_planes=sc["planes"], sats_per_plane=sc["sats"],
            n_flows=max(10, int(n_nodes * 0.6)),
            device="cuda",
        )
        gnn_res = eval_gnn(model, cfg, n_eval=30, seed_offset=400000)
        ecmp_res = eval_ecmp(cfg, n_eval=30, seed_offset=400000)
        ratio = gnn_res["mean"] / ecmp_res["mean"]
        scale_results.append({
            "label": sc["label"],
            "n_nodes": n_nodes,
            "n_planes": sc["planes"],
            "sats_per_plane": sc["sats"],
            "scale_factor": scale_f,
            "gnn_mlu": gnn_res["mean"],
            "gnn_std": gnn_res["std"],
            "ecmp_mlu": ecmp_res["mean"],
            "ecmp_std": ecmp_res["std"],
            "gnn_ecmp_ratio": ratio,
        })
        print(f"  {sc['label']:20s}: GNN={gnn_res['mean']:.4f} "
              f"ECMP={ecmp_res['mean']:.4f} ratio={ratio:.4f}")

    # ── Save ────────────────────────────────────────────────────────────
    output = {
        "fault_rate_sweep": fault_results,
        "traffic_sweep": traffic_results,
        "scale_sweep": scale_results,
        "elapsed_seconds": time.time() - t0,
    }

    out_path = RESULTS_DIR / "dense_ablation_results.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved to {out_path}")
    print(f"Total time: {(time.time() - t0)/60:.1f} min")


if __name__ == "__main__":
    main()
