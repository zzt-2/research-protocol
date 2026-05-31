#!/usr/bin/env python3
"""Comprehensive evaluation: E02-E08 with surge=1.0, using E01-v3 checkpoints.

Evaluates the 3-seed GNN model (trained on 66 nodes, surge=1.0) across:
- E02: no fault (fault_rate=0)
- E03-variant: surge=5.0 robustness (model trained w/o surge)
- E04: 48 nodes (0.7x)
- E05: 288 nodes (4.4x)
- E06: 720 nodes (10.9x)
- E08: fault rate ablation (0/5/8/10/15%)

All evaluations include ECMP/SP baselines + M1-M5 metrics.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

PROJECT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT))

from baselines.ecmp import run_ecmp
from baselines.sp import run_sp
from simulator.config import SimConfig
from simulator.env import RoutingEnv
from simulator.model import RoutingActorCritic
from simulator.train import evaluate

RESULTS_DIR = PROJECT / "simulator" / "results"
SEED_CKPTS = [
    RESULTS_DIR / f"ppo_seed{s}.pt" for s in range(3)
]

# Verify checkpoints exist
for p in SEED_CKPTS:
    assert p.exists(), f"Missing checkpoint: {p}"

BASE_CFG = dict(
    total_episodes=800,
    n_seeds=3,
    n_eval=50,
    device="cuda",
    entropy_coef=0.02,
    early_stop_patience=80,
)


def make_cfg(**overrides) -> SimConfig:
    """Create config with base settings + overrides."""
    params = {**BASE_CFG, **overrides}
    return SimConfig(**params)


def load_model(cfg: SimConfig, ckpt_path: Path) -> RoutingActorCritic:
    """Load a trained model from checkpoint."""
    model = RoutingActorCritic(
        node_dim=cfg.node_feat_dim,
        edge_dim=cfg.edge_feat_dim,
        hidden_dim=cfg.hidden_dim,
        n_layers=cfg.n_layers,
        n_heads=cfg.n_heads,
        k_paths=cfg.k_paths,
    ).to(cfg.device)
    ckpt = torch.load(str(ckpt_path), map_location=cfg.device, weights_only=False)
    model.load_state_dict(ckpt["model"])
    return model


def eval_gnn_3seeds(eval_cfg: SimConfig) -> dict:
    """Evaluate GNN across 3 seeds on the given config."""
    results = []
    for seed, ckpt_path in enumerate(SEED_CKPTS):
        env = RoutingEnv(eval_cfg, seed=seed)
        # Use training cfg for model arch (must match checkpoint)
        train_cfg = make_cfg()
        model = load_model(train_cfg, ckpt_path)
        ev = evaluate(model, env, n_eval=eval_cfg.n_eval, device=eval_cfg.device)
        ev["seed"] = seed
        results.append(ev)

    means = [r["mean"] for r in results]
    return {
        "mean": float(np.mean(means)),
        "std": float(np.std(means)),
        "seeds": results,
    }


def run_experiment(name: str, eval_cfg: SimConfig) -> dict:
    """Run one experiment: GNN 3 seeds + ECMP + SP baselines."""
    t0 = time.time()
    print(f"\n{'='*60}")
    print(f"  {name}: {eval_cfg.n_nodes} nodes, fault={eval_cfg.failure_rate:.0%}, "
          f"surge={eval_cfg.surge_factor}")
    print(f"{'='*60}")

    # GNN
    gnn = eval_gnn_3seeds(eval_cfg)
    print(f"  GNN:  MLU = {gnn['mean']:.4f} +/- {gnn['std']:.4f}")

    # ECMP
    env_ecmp = RoutingEnv(eval_cfg)
    ecmp = run_ecmp(env_ecmp, n_eval=eval_cfg.n_eval)
    print(f"  ECMP: MLU = {ecmp['mean']:.4f} +/- {ecmp['std']:.4f}")

    # SP
    env_sp = RoutingEnv(eval_cfg)
    sp = run_sp(env_sp, n_eval=eval_cfg.n_eval)
    print(f"  SP:   MLU = {sp['mean']:.4f} +/- {sp['std']:.4f}")

    # Ratios
    r_ecmp = gnn["mean"] / ecmp["mean"]
    r_sp = gnn["mean"] / sp["mean"]
    elapsed = time.time() - t0

    print(f"  GNN/ECMP = {r_ecmp:.4f}  GNN/SP = {r_sp:.4f}  ({elapsed:.0f}s)")

    return {
        "gnn": gnn,
        "ecmp": ecmp,
        "sp": sp,
        "gnn_ecmp_ratio": r_ecmp,
        "gnn_sp_ratio": r_sp,
        "config": {
            "n_nodes": eval_cfg.n_nodes,
            "n_planes": eval_cfg.n_planes,
            "sats_per_plane": eval_cfg.sats_per_plane,
            "failure_rate": eval_cfg.failure_rate,
            "surge_factor": eval_cfg.surge_factor,
        },
        "elapsed_s": elapsed,
    }


def main() -> None:
    t0 = time.time()
    all_results = {}

    # ── E02: No fault ──────────────────────────────────────────────────
    all_results["E02_no_fault"] = run_experiment(
        "E02 No Fault", make_cfg(failure_rate=0.0)
    )

    # ── E03-variant: Surge robustness (model trained w/o surge) ────────
    all_results["E03_surge5"] = run_experiment(
        "E03 Surge=5 (robustness)", make_cfg(surge_factor=5.0)
    )

    # ── E04: 48 nodes (0.7x) ──────────────────────────────────────────
    all_results["E04_48nodes"] = run_experiment(
        "E04 Generalization 48 nodes", make_cfg(n_planes=4, sats_per_plane=12)
    )

    # ── E05: 288 nodes (4.4x) ─────────────────────────────────────────
    all_results["E05_288nodes"] = run_experiment(
        "E05 Generalization 288 nodes", make_cfg(n_planes=12, sats_per_plane=24)
    )

    # ── E06: 720 nodes (10.9x) ────────────────────────────────────────
    all_results["E06_720nodes"] = run_experiment(
        "E06 Generalization 720 nodes", make_cfg(n_planes=36, sats_per_plane=20)
    )

    # ── E08: Fault rate ablation ───────────────────────────────────────
    fault_rates = [0.0, 0.05, 0.08, 0.10, 0.15]
    e08_results = []
    for fr in fault_rates:
        r = run_experiment(f"E08 Fault={fr:.0%}", make_cfg(failure_rate=fr))
        r["fault_rate"] = fr
        e08_results.append(r)
    all_results["E08_fault_ablation"] = e08_results

    # ── Summary ────────────────────────────────────────────────────────
    elapsed_total = time.time() - t0
    print(f"\n{'='*60}")
    print(f"  COMPREHENSIVE EVALUATION SUMMARY (surge=1.0 training)")
    print(f"{'='*60}")

    # E01-v3 reference
    e01v3 = json.loads((RESULTS_DIR / "e01_v2_results.json").read_text())
    e01_gnn = e01v3["gnn"]["mean"]
    e01_ecmp = e01v3["ecmp"]["mean"]
    print(f"\n  E01-v3 (66 nodes, 8% fault, surge=1.0):")
    print(f"    GNN={e01_gnn:.4f}  ECMP={e01_ecmp:.4f}  GNN/ECMP={e01_gnn/e01_ecmp:.4f}")

    # Key comparisons
    for name in ["E02_no_fault", "E03_surge5", "E04_48nodes", "E05_288nodes", "E06_720nodes"]:
        r = all_results[name]
        print(f"\n  {name}: GNN/ECMP={r['gnn_ecmp_ratio']:.4f}  "
              f"(GNN={r['gnn']['mean']:.4f}, ECMP={r['ecmp']['mean']:.4f})")

    print(f"\n  E08 Fault Rate Ablation:")
    for r in e08_results:
        print(f"    fault={r['fault_rate']:.0%}: GNN/ECMP={r['gnn_ecmp_ratio']:.4f}")

    print(f"\n  Total time: {elapsed_total/60:.1f} min")

    # Save
    out = RESULTS_DIR / "batch_eval_results.json"
    with open(out, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\n  Saved to {out}")


if __name__ == "__main__":
    main()
