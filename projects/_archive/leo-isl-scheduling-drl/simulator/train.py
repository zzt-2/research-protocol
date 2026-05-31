"""PPO training loop for ISL scheduling — continuous edge-score actions.

Adapted from reference/sim-template/train_ppo.py for continuous actions:
  - Buffer stores variable-length score arrays (ndarray) instead of int actions
  - No action masks (all candidate edges are valid)
  - Normal distribution instead of Categorical
  - obs dict → PyG Data conversion via obs_to_data()
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Generator

import numpy as np
import torch
import torch.nn as nn
from torch import Tensor
from torch_geometric.data import Data

try:
    import wandb
    _WANDB = True
except ImportError:
    wandb = None  # type: ignore[assignment]
    _WANDB = False


# ---------------------------------------------------------------------------
# obs → PyG Data conversion
# ---------------------------------------------------------------------------

def obs_to_data(obs: dict) -> Data:
    """Convert env observation dict to PyG Data object."""
    node_feat = torch.tensor(obs["node_features"], dtype=torch.float32)
    edge_feat = torch.tensor(obs["edge_features"], dtype=torch.float32)

    edges = obs["candidate_edges"]
    if len(edges) > 0:
        edge_index = torch.tensor(
            [[i, j] for i, j, _ in edges], dtype=torch.long,
        ).t().contiguous()
    else:
        edge_index = torch.zeros(2, 0, dtype=torch.long)

    return Data(x=node_feat, edge_index=edge_index, edge_attr=edge_feat)


# ---------------------------------------------------------------------------
# RolloutBuffer — continuous actions, variable-length score arrays
# ---------------------------------------------------------------------------

class ISLRolloutBuffer:
    def __init__(self) -> None:
        self.obs_list: list[dict] = []
        self.scores_list: list[np.ndarray] = []
        self.log_probs: list[float] = []
        self.rewards: list[float] = []
        self.dones: list[bool] = []
        self.values: list[float] = []

        self.returns: Tensor | None = None
        self.advantages: Tensor | None = None

    def add(
        self,
        obs: dict,
        scores: np.ndarray,
        log_prob: float,
        reward: float,
        done: bool,
        value: float,
    ) -> None:
        self.obs_list.append(obs)
        self.scores_list.append(scores)
        self.log_probs.append(log_prob)
        self.rewards.append(reward)
        self.dones.append(done)
        self.values.append(value)

    @property
    def size(self) -> int:
        return len(self.obs_list)

    def compute_returns_and_advantages(
        self, last_value: float, gamma: float, gae_lambda: float,
    ) -> None:
        n = self.size
        rewards = torch.tensor(self.rewards, dtype=torch.float32)
        values = torch.tensor(self.values, dtype=torch.float32)
        dones = torch.tensor(self.dones, dtype=torch.float32)
        values = torch.cat([values, torch.tensor([last_value])])

        advantages = torch.zeros(n, dtype=torch.float32)
        last_gae = 0.0
        for t in reversed(range(n)):
            delta = rewards[t] + gamma * values[t + 1] * (1.0 - dones[t]) - values[t]
            last_gae = delta + gamma * gae_lambda * (1.0 - dones[t]) * last_gae
            advantages[t] = last_gae

        self.returns = advantages + values[:n]
        self.advantages = advantages

    def get_mini_batches(
        self, batch_size: int,
    ) -> Generator[
        tuple[list[dict], list[np.ndarray], Tensor, Tensor, Tensor], None, None,
    ]:
        n = self.size
        indices = np.arange(n)
        np.random.shuffle(indices)

        old_log_probs_t = torch.tensor(self.log_probs, dtype=torch.float32)

        for start in range(0, n, batch_size):
            idx = indices[start : start + batch_size]
            yield (
                [self.obs_list[i] for i in idx],
                [self.scores_list[i] for i in idx],
                old_log_probs_t[idx],
                self.returns[idx],
                self.advantages[idx],
            )


# ---------------------------------------------------------------------------
# RewardNormalizer — Welford online
# ---------------------------------------------------------------------------

class RewardNormalizer:
    def __init__(self, clip: float = 5.0, eps: float = 1e-8) -> None:
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
        m2 = (
            self._var * self._count
            + batch_var * n
            + delta ** 2 * self._count * n / total
        )
        self._var = m2 / total + self._eps
        self._count = total
        std = np.sqrt(self._var)
        normed = (arr - self._mean) / std
        return np.clip(normed, -self._clip, self._clip).tolist()

    def state_dict(self) -> dict:
        return {"mean": self._mean, "var": self._var, "count": self._count}

    def load_state_dict(self, d: dict) -> None:
        self._mean = d["mean"]
        self._var = d["var"]
        self._count = d["count"]


# ---------------------------------------------------------------------------
# EarlyStopping — reward plateau + KL dual condition
# ---------------------------------------------------------------------------

class EarlyStopping:
    def __init__(
        self,
        patience: int = 20,
        kl_threshold: float = 0.15,
        min_improvement: float = 0.0,
    ) -> None:
        self.patience = patience
        self.kl_threshold = kl_threshold
        self.min_improvement = min_improvement
        self._best_reward = -float("inf")
        self._wait = 0
        self._recent_kl: list[float] = []

    def step(self, mean_reward: float, mean_kl: float) -> bool:
        self._recent_kl.append(mean_kl)
        if len(self._recent_kl) > 5:
            self._recent_kl = self._recent_kl[-5:]

        if len(self._recent_kl) >= 3:
            avg_kl = float(np.mean(self._recent_kl))
            if avg_kl > self.kl_threshold:
                print(f"  [EarlyStop] KL too large: avg_kl={avg_kl:.4f}")
                return True

        if mean_reward > self._best_reward + self.min_improvement:
            self._best_reward = mean_reward
            self._wait = 0
        else:
            self._wait += 1
            if self._wait >= self.patience:
                print(f"  [EarlyStop] Reward plateau: {self.patience} updates no improvement")
                return True

        return False


# ---------------------------------------------------------------------------
# Checkpoint helpers
# ---------------------------------------------------------------------------

def save_checkpoint(
    path: Path,
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    reward_normalizer: RewardNormalizer,
    total_updates: int,
    extra: dict | None = None,
) -> None:
    ckpt: dict = {
        "model": model.state_dict(),
        "optimizer": optimizer.state_dict(),
        "reward_normalizer": reward_normalizer.state_dict(),
        "total_updates": total_updates,
    }
    if extra:
        ckpt.update(extra)
    torch.save(ckpt, path)


def load_checkpoint(
    path: Path,
    model: nn.Module,
    optimizer: torch.optim.Optimizer | None = None,
    reward_normalizer: RewardNormalizer | None = None,
    device: str = "cpu",
) -> dict:
    ckpt = torch.load(path, map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model"])
    if optimizer and "optimizer" in ckpt:
        optimizer.load_state_dict(ckpt["optimizer"])
    if reward_normalizer and "reward_normalizer" in ckpt:
        reward_normalizer.load_state_dict(ckpt["reward_normalizer"])
    return ckpt


# ---------------------------------------------------------------------------
# Training loop
# ---------------------------------------------------------------------------

def train(
    env,
    model: nn.Module,
    n_episodes: int = 500,
    update_interval: int = 10,
    seed: int = 42,
    device: str = "cpu",
    results_dir: str = "results",
    # PPO hyperparams
    lr: float = 3e-4,
    entropy_coef: float = 0.01,
    clip_eps: float = 0.2,
    gamma: float = 0.99,
    gae_lambda: float = 0.95,
    ppo_epochs: int = 4,
    batch_size: int = 64,
    max_grad_norm: float = 0.5,
    total_training_steps: int = 10_000,
    # Early stopping
    early_stop_patience: int = 50,
    early_stop_kl_threshold: float = 0.15,
) -> dict:
    """PPO training for ISL scheduling with continuous edge-score actions."""
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    results_path = Path(results_dir)
    results_path.mkdir(exist_ok=True, parents=True)

    model = model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    reward_normalizer = RewardNormalizer()
    early_stopper = EarlyStopping(
        patience=early_stop_patience,
        kl_threshold=early_stop_kl_threshold,
    )

    episode_rewards: list[float] = []
    best_reward = -float("inf")
    total_updates = 0
    buf = ISLRolloutBuffer()

    for ep in range(n_episodes):
        obs, _ = env.reset(seed=seed + ep)
        done = False
        ep_reward = 0.0

        while not done:
            data = obs_to_data(obs)
            scores, log_prob, value = model.get_action(data)
            scores_np = scores.cpu().numpy()

            next_obs, reward, terminated, truncated, info = env.step(scores_np)
            done = terminated or truncated

            buf.add(obs, scores_np, log_prob.item(), reward, done, value.item())
            obs = next_obs
            ep_reward += reward

        episode_rewards.append(ep_reward)

        # PPO update every update_interval episodes
        if (ep + 1) % update_interval == 0:
            # Normalize rewards
            buf.rewards = reward_normalizer.update_and_normalize(buf.rewards)

            # Bootstrap value for last observation
            with torch.no_grad():
                last_data = obs_to_data(obs)
                _, last_val = model(last_data)
                last_val = last_val.squeeze().item()
            buf.compute_returns_and_advantages(last_val, gamma, gae_lambda)

            # Normalize advantages
            advs = buf.advantages
            advs = (advs - advs.mean()) / (advs.std() + 1e-8)
            buf.advantages = advs.to(device)

            # PPO epochs
            model.train()
            epoch_metrics: dict[str, list[float]] = {
                "policy_loss": [], "value_loss": [], "entropy": [], "kl": [],
            }

            for _epoch in range(ppo_epochs):
                for (
                    obs_batch, scores_batch, old_lps, returns, advs_batch,
                ) in buf.get_mini_batches(batch_size):
                    data_list = [obs_to_data(o) for o in obs_batch]
                    scores_t = [
                        torch.tensor(s, dtype=torch.float32) for s in scores_batch
                    ]

                    log_probs, values, entropies = model.evaluate_actions(
                        data_list, scores_t,
                    )

                    old_lps_dev = old_lps.to(device)
                    returns_dev = returns.to(device)
                    advs_dev = advs_batch.to(device)

                    # PPO clipped surrogate
                    ratio = torch.exp(log_probs - old_lps_dev)
                    surr1 = ratio * advs_dev
                    surr2 = (
                        torch.clamp(ratio, 1.0 - clip_eps, 1.0 + clip_eps)
                        * advs_dev
                    )
                    policy_loss = -torch.min(surr1, surr2).mean()

                    value_loss = 0.5 * ((values - returns_dev) ** 2).mean()
                    entropy_loss = entropies.mean()

                    loss = policy_loss + 0.5 * value_loss - entropy_coef * entropy_loss

                    optimizer.zero_grad()
                    loss.backward()
                    nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
                    optimizer.step()

                    kl = (old_lps_dev - log_probs).mean().item()
                    epoch_metrics["policy_loss"].append(policy_loss.item())
                    epoch_metrics["value_loss"].append(value_loss.item())
                    epoch_metrics["entropy"].append(entropy_loss.item())
                    epoch_metrics["kl"].append(kl)

            total_updates += 1

            # Linear LR decay
            factor = max(1.0 - total_updates / total_training_steps, 0.0)
            for pg in optimizer.param_groups:
                pg["lr"] = lr * factor

            metrics = {k: float(np.mean(v)) for k, v in epoch_metrics.items()}
            mean_reward = float(np.mean(episode_rewards[-update_interval:]))

            # Save best
            if mean_reward > best_reward:
                best_reward = mean_reward
                save_checkpoint(
                    results_path / "best_model.pt",
                    model, optimizer, reward_normalizer, total_updates,
                    extra={"best_reward": best_reward, "episode": ep + 1},
                )

            # Early stopping
            if early_stopper.step(mean_reward, metrics["kl"]):
                print(f"  [EarlyStop] Triggered at episode {ep + 1}")
                buf = ISLRolloutBuffer()
                break

            # Clear buffer
            buf = ISLRolloutBuffer()

            # Wandb log
            if _WANDB and wandb.run is not None:
                wandb.log({
                    "train/mean_reward": mean_reward,
                    "ppo/policy_loss": metrics["policy_loss"],
                    "ppo/value_loss": metrics["value_loss"],
                    "ppo/entropy": metrics["entropy"],
                    "ppo/kl": metrics["kl"],
                    "ppo/lr": optimizer.param_groups[0]["lr"],
                    "train/episode": ep + 1,
                })

        # Progress log
        if (ep + 1) % 50 == 0:
            recent = episode_rewards[-50:]
            mean_r = np.mean(recent)
            print(
                f"  ep={ep + 1}/{n_episodes} "
                f"reward(last50)={mean_r:.4f} "
                f"best={best_reward:.4f}"
            )

    # Final save
    save_checkpoint(
        results_path / f"final_seed{seed}.pt",
        model, optimizer, reward_normalizer, total_updates,
        extra={"episode": ep + 1},
    )

    results = {
        "episode_rewards": episode_rewards,
        "n_episodes": ep + 1,
        "seed": seed,
        "best_reward": best_reward,
    }
    with open(results_path / f"train_seed{seed}.json", "w") as f:
        json.dump(results, f, indent=2)

    return results


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------

def evaluate(
    env,
    model: nn.Module,
    n_episodes: int = 10,
    seed: int = 42,
    device: str = "cpu",
) -> dict:
    """Deterministic evaluation, returns averaged M1-M5 metrics."""
    model = model.to(device)
    model.eval()

    all_metrics: list[dict] = []
    total_rewards: list[float] = []

    for i in range(n_episodes):
        def policy_fn(obs: dict) -> np.ndarray:
            data = obs_to_data(obs)
            scores, _, _ = model.get_action(data, deterministic=True)
            return scores.cpu().numpy()

        metrics, total_reward = env.run_episode(policy_fn)
        all_metrics.append(metrics)
        total_rewards.append(total_reward)

    avg: dict[str, float] = {"total_reward": float(np.mean(total_rewards))}
    for key in all_metrics[0]:
        avg[key] = float(np.mean([m[key] for m in all_metrics]))

    return avg
