"""End-to-end pipeline: ILP dataset -> Phase A (supervised) -> Phase B (discrete RL) -> evaluation.

Usage:
    python run_pipeline.py [--n_planes 24] [--sats_per_plane 20] [--n_snapshots 500] [--device cuda]
"""

import argparse
import os
import sys
import json
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from simulator.generate_dataset import generate_supervised_dataset
from simulator.train_supervised import train_supervised
from simulator.train_ppo_discrete import train_ppo_discrete, evaluate_model
from simulator.environment import ISLEnvironment
from simulator.discrete_wrapper import DiscreteActionWrapper, obs_to_data
from simulator.model_gat import GATv2Backbone, SupervisedGNN, DiscreteRLGNN
import torch
import numpy as np


def main():
    parser = argparse.ArgumentParser(description="ISL scheduling: supervised + discrete RL pipeline")
    parser.add_argument("--n_planes", type=int, default=24)
    parser.add_argument("--sats_per_plane", type=int, default=20)
    parser.add_argument("--n_snapshots", type=int, default=500)
    parser.add_argument("--device", type=str, default="cpu")
    parser.add_argument("--skip_dataset", action="store_true", help="Skip dataset generation if exists")
    args = parser.parse_args()

    results_dir = "results/pipeline"
    dataset_dir = "data/ilp_dataset"
    os.makedirs(results_dir, exist_ok=True)

    t0 = time.time()

    # === Phase 0: Dataset Generation ===
    print("=" * 60)
    print("Phase 0: Generating ILP dataset")
    print("=" * 60)
    if args.skip_dataset and os.path.exists(dataset_dir):
        print(f"Skipping, using existing dataset at {dataset_dir}")
    else:
        dataset_stats = generate_supervised_dataset(
            n_planes=args.n_planes,
            sats_per_plane=args.sats_per_plane,
            n_snapshots=args.n_snapshots,
            output_dir=dataset_dir,
        )
        print(f"Dataset: {dataset_stats}")

    # === Phase A: Supervised Pretraining ===
    print("\n" + "=" * 60)
    print("Phase A: Supervised pretraining")
    print("=" * 60)
    phase_a_dir = os.path.join(results_dir, "phase_a")
    phase_a_result = train_supervised(
        dataset_dir=dataset_dir,
        device=args.device,
        output_dir=phase_a_dir,
    )
    print(f"Phase A result: acc={phase_a_result.get('best_test_accuracy', 'N/A')}, "
          f"F1={phase_a_result.get('best_test_f1', 'N/A')}")

    # === Phase B: Discrete RL Fine-tuning ===
    print("\n" + "=" * 60)
    print("Phase B: Discrete RL fine-tuning")
    print("=" * 60)
    phase_b_dir = os.path.join(results_dir, "phase_b")
    phase_b_result = train_ppo_discrete(
        phase_a_checkpoint=os.path.join(phase_a_dir, "phase_a_best.pt"),
        n_planes=args.n_planes,
        sats_per_plane=args.sats_per_plane,
        device=args.device,
        results_dir=phase_b_dir,
    )
    print(f"Phase B result: best_reward={phase_b_result.get('best_reward', 'N/A')}")

    # === Evaluation: Compare vs Baselines ===
    print("\n" + "=" * 60)
    print("Evaluation: Phase A vs Phase B vs B1 (Grid/Fixed)")
    print("=" * 60)

    env = ISLEnvironment(n_planes=args.n_planes, sats_per_plane=args.sats_per_plane)

    # Load best Phase B model
    bb = GATv2Backbone()
    drl_model = DiscreteRLGNN(bb)
    ckpt_b = torch.load(os.path.join(phase_b_dir, "phase_b_best.pt"), map_location=args.device, weights_only=False)
    drl_model.load_state_dict(ckpt_b['model_state_dict'])
    drl_model.to(args.device)
    drl_model.eval()

    # Evaluate Phase B
    phase_b_metrics = evaluate_model(env, drl_model, n_episodes=5, device=args.device)
    print(f"Phase B: M1={phase_b_metrics.get('M1_throughput', 'N/A'):.4f}")

    # Load best Phase A model (supervised only, no RL)
    bb_a = GATv2Backbone()
    sg_model = SupervisedGNN(bb_a)
    ckpt_a = torch.load(os.path.join(phase_a_dir, "phase_a_best.pt"), map_location=args.device, weights_only=False)
    sg_model.load_state_dict(ckpt_a['full'])
    sg_model.to(args.device)
    sg_model.eval()

    # Evaluate Phase A (supervised policy via wrapper)
    def supervised_policy(obs):
        data = obs_to_data(obs).to(args.device)
        return sg_model.predict_scores(data)

    env2 = ISLEnvironment(n_planes=args.n_planes, sats_per_plane=args.sats_per_plane)
    phase_a_metrics, _ = env2.run_episode(supervised_policy)
    print(f"Phase A: M1={phase_a_metrics.get('M1_throughput', 'N/A'):.4f}")

    # B1 Baseline (Grid/Fixed)
    from baselines.grid_fixed import GridFixedBaseline
    b1 = GridFixedBaseline(n_planes=args.n_planes, sats_per_plane=args.sats_per_plane)
    b1_metrics, b1_reward = b1.run_episode()
    print(f"B1 Grid: M1={b1_metrics.get('M1_throughput', 'N/A'):.4f}")

    # Summary
    total_time = time.time() - t0
    summary = {
        'total_time_sec': total_time,
        'config': {'n_planes': args.n_planes, 'sats_per_plane': args.sats_per_plane},
        'phase_a': phase_a_result,
        'phase_b': phase_b_result,
        'evaluation': {
            'phase_b_M1': phase_b_metrics.get('M1_throughput'),
            'phase_a_M1': phase_a_metrics.get('M1_throughput'),
            'b1_M1': b1_metrics.get('M1_throughput'),
        }
    }

    summary_path = os.path.join(results_dir, "pipeline_summary.json")
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2, default=str)

    print("\n" + "=" * 60)
    print(f"Pipeline complete in {total_time:.1f}s")
    print(f"Summary saved to {summary_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
