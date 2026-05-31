"""Evaluate Phase A supervised policy vs B1 baseline at 24x20 scale."""

import sys
import os
import torch
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from simulator.environment import ISLEnvironment
from simulator.discrete_wrapper import obs_to_data
from simulator.model_gat import GATv2Backbone, SupervisedGNN
from baselines.grid_fixed import GridFixedBaseline
from simulator import config


def evaluate_supervised_policy(
    checkpoint_path="results/phase_a_24x20/phase_a_best.pt",
    n_planes=24,
    sats_per_plane=20,
    n_episodes=5,
    device="cpu",
):
    env = ISLEnvironment(n_planes=n_planes, sats_per_plane=sats_per_plane)

    # Load model
    bb = GATv2Backbone()
    model = SupervisedGNN(bb)
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    model.load_state_dict(ckpt["full"])
    model.to(device)
    model.eval()

    # Supervised policy
    def policy_fn(obs):
        data = obs_to_data(obs).to(device)
        return model.predict_scores(data)

    # Run episodes
    all_metrics = []
    for ep in range(n_episodes):
        metrics, reward = env.run_episode(policy_fn)
        all_metrics.append(metrics)
        print(f"  Episode {ep+1}: M1={metrics['M1_throughput']:.4f} "
              f"M3={metrics['M3_switch_rate']:.4f} "
              f"reward={reward:.4f}")

    avg = {k: np.mean([m[k] for m in all_metrics]) for k in all_metrics[0]}
    return avg


def main():
    print("=" * 60)
    print("Evaluation: Phase A Supervised vs B1 Grid/Fixed")
    print(f"Scale: 24x20={config.N_PLANES}x20={24*20} sats")
    print("=" * 60)

    # B1 Baseline
    print("\nB1 Grid/Fixed:")
    b1 = GridFixedBaseline(n_planes=24, sats_per_plane=20)
    b1_metrics, b1_reward = b1.run_episode()
    print(f"  M1={b1_metrics['M1_throughput']:.4f} "
          f"M3={b1_metrics['M3_switch_rate']:.4f} "
          f"reward={b1_reward:.4f}")

    # Phase A
    print("\nPhase A (Supervised):")
    phase_a_metrics = evaluate_supervised_policy(n_episodes=5)

    # Comparison
    print("\n" + "=" * 60)
    print("Comparison:")
    print(f"  {'Method':<20} {'M1_tput':>10} {'M3_switch':>10} {'M5_fair':>10}")
    print(f"  {'B1 Grid/Fixed':<20} {b1_metrics['M1_throughput']:>10.4f} "
          f"{b1_metrics['M3_switch_rate']:>10.4f} "
          f"{b1_metrics['M5_fairness']:>10.4f}")
    print(f"  {'Phase A Supervised':<20} {phase_a_metrics['M1_throughput']:>10.4f} "
          f"{phase_a_metrics['M3_switch_rate']:>10.4f} "
          f"{phase_a_metrics['M5_fairness']:>10.4f}")
    print("=" * 60)


if __name__ == "__main__":
    main()
