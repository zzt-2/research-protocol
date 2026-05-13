"""Training loop for satellite DAG task offloading.

Usage:
    python train.py --model hgat --episodes 500 --seeds 42 123 456
    python train.py --model all   # run all 5 methods
"""

import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch

from config import N_TASKS, PPO_LR, PPO_ENTROPY_COEF
from environment import SatelliteDAGEnv
from ppo import PPO, RolloutBuffer


class RewardNormalizer:
    """Running Z-score normalization for rewards (standard PPO trick)."""

    def __init__(self, clip: float = 5.0, eps: float = 1e-8):
        self._mean = 0.0
        self._var = 1.0
        self._count = 1e-4
        self._clip = clip
        self._eps = eps

    def update_and_normalize(self, rewards: list[float]) -> list[float]:
        arr = np.array(rewards, dtype=np.float64)
        batch_mean = arr.mean()
        batch_var = arr.var()
        n = len(rewards)
        delta = batch_mean - self._mean
        total = self._count + n
        self._mean += delta * n / total
        m2 = (self._var * self._count + batch_var * n
              + delta ** 2 * self._count * n / total)
        self._var = m2 / total + self._eps
        self._count = total
        std = np.sqrt(self._var)
        normed = (arr - self._mean) / std
        return np.clip(normed, -self._clip, self._clip).tolist()


def _make_model(model_type: str, device: str):
    if model_type == "hgat":
        from models_hgat import HGATActorCritic
        return HGATActorCritic().to(device)
    if model_type == "graphsage":
        from models_homo import GraphSAGEActorCritic
        return GraphSAGEActorCritic().to(device)
    if model_type == "gcn":
        from models_homo import GCNActorCritic
        return GCNActorCritic().to(device)
    if model_type == "mlp":
        from models_homo import MLPActorCritic
        return MLPActorCritic().to(device)
    raise ValueError(f"Unknown model: {model_type}")


def train_drl(model_type: str, n_episodes: int, seed: int,
              device: str, results_dir: Path, update_interval: int = 10,
              lr: float = PPO_LR, entropy_coef: float = PPO_ENTROPY_COEF):
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    model = _make_model(model_type, device)
    ppo = PPO(model, lr=lr, entropy_coef=entropy_coef, device=device)
    env = SatelliteDAGEnv(seed=seed)

    episode_rewards = []
    all_metrics = []
    buf = RolloutBuffer()
    reward_normalizer = RewardNormalizer()

    for ep in range(n_episodes):
        obs, info = env.reset()
        done = False
        ep_reward = 0.0

        while not done:
            action_mask = info["action_mask"]
            action, log_prob, value, _ = model.get_action(obs, action_mask)
            next_obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

            buf.add(obs, action, log_prob, reward, done, value, action_mask)
            obs = next_obs
            ep_reward += reward

        episode_rewards.append(ep_reward)

        # Update every update_interval episodes
        if (ep + 1) % update_interval == 0:
            # Normalize rewards using running statistics before GAE
            buf.rewards = reward_normalizer.update_and_normalize(buf.rewards)

            with torch.no_grad():
                _, last_val = model(obs)
                last_val = last_val.squeeze().item()
            buf.compute_returns_and_advantages(last_val)

            metrics = ppo.update(buf)
            metrics["episode"] = ep
            metrics["episode_reward"] = np.mean(episode_rewards[-update_interval:])
            all_metrics.append(metrics)
            buf = RolloutBuffer()

        if (ep + 1) % 50 == 0:
            recent = episode_rewards[-50:]
            mean_r = np.mean(recent)
            last_m = all_metrics[-1] if all_metrics else {}
            print(f"  [{model_type}] seed={seed} ep={ep+1}/{n_episodes} "
                  f"reward(last50)={mean_r:.2f} "
                  f"ploss={last_m.get('policy_loss', 0):.4f} "
                  f"ent={last_m.get('entropy', 0):.4f}")
    results = {
        "model": model_type, "seed": seed,
        "episode_rewards": episode_rewards,
        "n_episodes": n_episodes,
    }
    out = results_dir / f"{model_type}_seed{seed}.json"
    with open(out, "w") as f:
        json.dump(results, f)

    ppo.save(str(results_dir / f"{model_type}_seed{seed}.pt"))
    return results


def evaluate_baseline(baseline_type: str, n_episodes: int, seed: int,
                      results_dir: Path):
    np.random.seed(seed)
    env = SatelliteDAGEnv(seed=seed)

    episode_rewards = []
    for ep in range(n_episodes):
        env.reset()
        if baseline_type == "random":
            r = env.run_random_episode()
        else:
            r = env.run_greedy_episode()
        # run_*_episode returns dict with 'total_reward' key
        episode_rewards.append(r if isinstance(r, (int, float)) else r["total_reward"])

        if (ep + 1) % 100 == 0:
            mean_r = np.mean(episode_rewards[-100:])
            print(f"  [{baseline_type}] seed={seed} ep={ep+1}/{n_episodes} "
                  f"reward(last100)={mean_r:.2f}")

    results = {
        "model": baseline_type, "seed": seed,
        "episode_rewards": episode_rewards,
        "n_episodes": n_episodes,
    }
    out = results_dir / f"{baseline_type}_seed{seed}.json"
    with open(out, "w") as f:
        json.dump(results, f)
    return results


def plot_learning_curves(results_dir: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    result_files = sorted(results_dir.glob("*_seed*.json"))
    model_rewards = {}
    for f in result_files:
        with open(f) as fh:
            data = json.load(fh)
        model_rewards.setdefault(data["model"], []).append(data["episode_rewards"])

    if not model_rewards:
        print("No result files found for plotting.")
        return

    colors = {
        "hgat": "#e74c3c", "graphsage": "#3498db", "gcn": "#2ecc71",
        "random": "#95a5a6", "greedy": "#f39c12",
    }
    fig, ax = plt.subplots(figsize=(10, 6))
    for model in ["hgat", "graphsage", "gcn", "greedy", "random"]:
        if model not in model_rewards:
            continue
        arr = np.array(model_rewards[model])
        mean = arr.mean(axis=0)
        std = arr.std(axis=0)
        ep = np.arange(len(mean))
        ax.plot(ep, mean, label=model.upper(), color=colors[model], linewidth=1.5)
        ax.fill_between(ep, mean - std, mean + std, color=colors[model], alpha=0.15)

    ax.set_xlabel("Episode")
    ax.set_ylabel("Total Reward")
    ax.set_title("Learning Curves — Satellite DAG Task Offloading")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(results_dir / "learning_curves.png", dpi=150)
    plt.close(fig)
    print(f"Plot saved to {results_dir / 'learning_curves.png'}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True,
                        choices=["hgat", "graphsage", "gcn", "mlp", "random", "greedy", "all"])
    parser.add_argument("--episodes", type=int, default=500)
    parser.add_argument("--seeds", type=int, nargs="+", default=[42, 123, 456])
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--output-dir", default="results")
    parser.add_argument("--update-interval", type=int, default=10,
                        help="Accumulate N episodes before PPO update")
    parser.add_argument("--lr", type=float, default=PPO_LR,
                        help="PPO learning rate")
    parser.add_argument("--entropy", type=float, default=PPO_ENTROPY_COEF,
                        help="PPO entropy coefficient")
    args = parser.parse_args()

    results_dir = Path(args.output_dir)
    results_dir.mkdir(exist_ok=True, parents=True)

    models = (["hgat", "graphsage", "gcn", "mlp", "random", "greedy"]
              if args.model == "all" else [args.model])

    print(f"Models: {models} | Episodes: {args.episodes} | "
          f"Seeds: {args.seeds} | Device: {args.device}")

    t0 = time.time()
    for m in models:
        for seed in args.seeds:
            print(f"\n--- {m} seed={seed} ---")
            if m in ("random", "greedy"):
                evaluate_baseline(m, args.episodes, seed, results_dir)
            else:
                train_drl(m, args.episodes, seed, args.device, results_dir,
                          args.update_interval, args.lr, args.entropy)

    plot_learning_curves(results_dir)
    print(f"\nTotal: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
