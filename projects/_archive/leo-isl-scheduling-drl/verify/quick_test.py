"""Quick Test: 24×20 small-scale training (Execute Step 1).

Verifies that GAT-PPO training converges on small constellation.
Compares with B1 (+Grid/Fixed) baseline on same scale.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import numpy as np
from simulator.environment import ISLEnvironment
from simulator.model_gat import GATv2ActorCritic
from simulator.train import train, evaluate, obs_to_data
from baselines.grid_fixed import GridFixedBaseline


def run_b1_baseline(n_planes=24, sats_per_plane=20, n_episodes=5):
    """Run B1 (+Grid/Fixed) baseline on small scale."""
    rewards = []
    m1s = []
    for i in range(n_episodes):
        baseline = GridFixedBaseline(n_planes=n_planes, sats_per_plane=sats_per_plane,
                                     seed=100 + i, n_lct=3)
        metrics, total_reward = baseline.run_episode()
        rewards.append(total_reward)
        m1s.append(metrics.get("M1", metrics.get("throughput", 0)))

    print(f"\n[B1 Baseline] reward={np.mean(rewards):.4f}±{np.std(rewards):.4f} "
          f"M1={np.mean(m1s):.4f} ({n_episodes} episodes)")
    return np.mean(rewards), np.mean(m1s)


def main():
    print("=" * 60)
    print("Quick Test: 24×20 (480 sats) GAT-PPO Training")
    print("=" * 60)

    n_planes, sats_per_plane = 24, 20

    # B1 baseline first
    print("\n--- B1 Baseline ---")
    b1_reward, b1_m1 = run_b1_baseline(n_planes, sats_per_plane)

    # Train GAT-PPO
    print("\n--- GAT-PPO Training ---")
    env = ISLEnvironment(n_planes=n_planes, sats_per_plane=sats_per_plane)
    model = GATv2ActorCritic(node_dim=6, edge_dim=7, hidden_dim=64, n_heads=4, n_layers=3)

    results = train(
        env, model,
        n_episodes=200,
        update_interval=5,
        seed=42,
        device="cpu",
        results_dir=str(ROOT / "results" / "quick_test"),
        lr=3e-4,
        entropy_coef=0.01,
        clip_eps=0.2,
        gamma=0.99,
        gae_lambda=0.95,
        ppo_epochs=4,
        batch_size=32,
        max_grad_norm=0.5,
        early_stop_patience=30,
        total_training_steps=500,
    )

    n_trained = results["n_episodes"]
    rewards = results["episode_rewards"]

    print(f"\n--- Training Summary ---")
    print(f"Episodes: {n_trained}")
    print(f"Final 50 ep reward: {np.mean(rewards[-50:]):.4f}")
    print(f"Best reward: {results['best_reward']:.4f}")

    # Evaluate deterministic
    print("\n--- Deterministic Evaluation ---")
    eval_metrics = evaluate(env, model, n_episodes=5, seed=200, device="cpu")
    for k, v in eval_metrics.items():
        print(f"  {k}: {v:.4f}")

    # Compare
    dqn_m1 = eval_metrics.get("M1", eval_metrics.get("throughput", 0))
    print(f"\n--- Comparison ---")
    print(f"  B1 M1:      {b1_m1:.4f}")
    print(f"  GAT-PPO M1: {dqn_m1:.4f}")
    gap = dqn_m1 - b1_m1
    print(f"  Gap:        {gap:+.4f} ({'GAT-PPO wins' if gap > 0 else 'B1 wins'})")

    # Signal check
    if np.mean(rewards[-50:]) > np.mean(rewards[:10]):
        print("\n[SIGNAL] Training reward improving — direction correct")
    else:
        print("\n[WARNING] Training reward not improving — check data flow")

    return results, eval_metrics, b1_m1


if __name__ == "__main__":
    main()
