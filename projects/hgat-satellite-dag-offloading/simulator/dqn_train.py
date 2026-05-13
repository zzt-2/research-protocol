"""Training loop for DQN-MLP baseline.

Usage:
    python dqn_train.py --episodes 500 --seeds 42 123 456
"""

import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch

from dqn import DQNAgent
from environment import SatelliteDAGEnv


def train_dqn(n_episodes: int, seed: int, device: str, results_dir: Path,
              lr: float = 1e-3, target_update_interval: int = 10):
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    env = SatelliteDAGEnv(seed=seed)
    n_actions = env.action_space.n
    agent = DQNAgent(n_actions=n_actions, lr=lr, device=device)

    episode_rewards = []
    all_metrics = []
    step_count = 0
    update_freq = 10  # update every N steps, not every step

    for ep in range(n_episodes):
        obs, info = env.reset()
        done = False
        ep_reward = 0.0

        while not done:
            mask = info["action_mask"]
            action = agent.select_action(obs, mask)
            next_obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            next_mask = info["action_mask"]

            agent.store(obs, action, reward, next_obs, terminated, mask, next_mask)
            step_count += 1

            if step_count % update_freq == 0:
                metrics = agent.update()
                if metrics:
                    all_metrics.append(metrics)

            obs = next_obs
            ep_reward += reward

        episode_rewards.append(ep_reward)

        if (ep + 1) % 50 == 0:
            recent = episode_rewards[-50:]
            mean_r = np.mean(recent)
            last_m = all_metrics[-1] if all_metrics else {}
            print(f"  [dqn-mlp] seed={seed} ep={ep+1}/{n_episodes} "
                  f"reward(last50)={mean_r:.2f} "
                  f"eps={last_m.get('epsilon', 0):.4f} "
                  f"loss={last_m.get('loss', 0):.4f}")

    results = {
        "model": "dqn-mlp", "seed": seed,
        "episode_rewards": episode_rewards,
        "n_episodes": n_episodes,
    }
    out = results_dir / f"dqn-mlp_seed{seed}.json"
    with open(out, "w") as f:
        json.dump(results, f)

    agent.save(str(results_dir / f"dqn-mlp_seed{seed}.pt"))
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=500)
    parser.add_argument("--seeds", type=int, nargs="+", default=[42, 123, 456])
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--output-dir", default="results")
    parser.add_argument("--lr", type=float, default=1e-3)
    args = parser.parse_args()

    results_dir = Path(args.output_dir)
    results_dir.mkdir(exist_ok=True, parents=True)

    print(f"DQN-MLP | Episodes: {args.episodes} | Seeds: {args.seeds} | Device: {args.device}")

    t0 = time.time()
    for seed in args.seeds:
        print(f"\n--- dqn-mlp seed={seed} ---")
        train_dqn(args.episodes, seed, args.device, results_dir, args.lr)

    print(f"\nTotal: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
