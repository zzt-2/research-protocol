"""PPO 训练引擎 — wandb 集成 + early stopping + LR decay + reward normalizer。

核心设计:
  - RolloutBuffer: GAE(λ) + mini-batch，obs 保留 list（兼容 HeteroData）
  - RewardNormalizer: Welford 在线算法，save/load 支持
  - PPO 核心: grad clip + advantage norm + linear LR decay + entropy bonus
  - EarlyStopping: reward plateau + KL 散度双条件
  - save/load: model + optimizer + normalizer + step_count，支持 resume
"""

from __future__ import annotations

from typing import Generator

import numpy as np
import torch
import torch.nn as nn
from torch import Tensor

try:
    import wandb
    _WANDB = True
except ImportError:
    wandb = None
    _WANDB = False


# ---------------------------------------------------------------------------
# RolloutBuffer
# ---------------------------------------------------------------------------

class RolloutBuffer:
    """On-policy buffer. Observations kept as list for HeteroData compatibility."""

    def __init__(self) -> None:
        self.obs: list = []
        self.actions: list[int] = []
        self.log_probs: list[float] = []
        self.rewards: list[float] = []
        self.dones: list[bool] = []
        self.values: list[float] = []
        self.action_masks: list[np.ndarray] = []
        self.returns: Tensor | None = None
        self.advantages: Tensor | None = None

    def add(self, obs, action: int, log_prob: float, reward: float,
            done: bool, value: float, action_mask: np.ndarray) -> None:
        self.obs.append(obs)
        self.actions.append(action)
        self.log_probs.append(log_prob)
        self.rewards.append(reward)
        self.dones.append(done)
        self.values.append(value)
        self.action_masks.append(action_mask)

    @property
    def size(self) -> int:
        return len(self.obs)

    def compute_returns_and_advantages(self, last_value: float,
                                        gamma: float, gae_lambda: float) -> None:
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

    def get_batches(self, batch_size: int):
        n = self.size
        indices = np.arange(n)
        np.random.shuffle(indices)
        actions_t = torch.tensor(self.actions, dtype=torch.long)
        old_lp_t = torch.tensor(self.log_probs, dtype=torch.float32)
        masks_t = torch.tensor(np.stack(self.action_masks), dtype=torch.bool)

        for start in range(0, n, batch_size):
            idx = indices[start:start + batch_size]
            yield ([self.obs[i] for i in idx], actions_t[idx], old_lp_t[idx],
                   self.returns[idx], self.advantages[idx], masks_t[idx])


# ---------------------------------------------------------------------------
# RewardNormalizer — Welford 在线
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
        n = len(rewards)
        if n == 0:
            return []
        batch_mean, batch_var = arr.mean(), arr.var()
        delta = batch_mean - self._mean
        total = self._count + n
        self._mean += delta * n / total
        m2 = (self._var * self._count + batch_var * n
              + delta ** 2 * self._count * n / total)
        self._var = m2 / total + self._eps
        self._count = total
        std = np.sqrt(self._var)
        return np.clip((arr - self._mean) / std, -self._clip, self._clip).tolist()

    def state_dict(self) -> dict:
        return {"mean": self._mean, "var": self._var, "count": self._count}

    def load_state_dict(self, d: dict) -> None:
        self._mean, self._var, self._count = d["mean"], d["var"], d["count"]


# ---------------------------------------------------------------------------
# EarlyStopping
# ---------------------------------------------------------------------------

class EarlyStopping:
    def __init__(self, patience: int = 50, kl_threshold: float = 0.15) -> None:
        self.patience = patience
        self.kl_threshold = kl_threshold
        self._best_reward = -float("inf")
        self._wait = 0
        self._recent_kl: list[float] = []

    def step(self, mean_reward: float, mean_kl: float) -> bool:
        """Returns True if training should stop."""
        self._recent_kl.append(mean_kl)
        if len(self._recent_kl) > 5:
            self._recent_kl = self._recent_kl[-5:]

        if len(self._recent_kl) >= 3:
            avg_kl = float(np.mean(self._recent_kl))
            if avg_kl > self.kl_threshold:
                print(f"  [EarlyStop] KL 过大: avg_kl={avg_kl:.4f} > {self.kl_threshold}")
                return True

        if mean_reward > self._best_reward:
            self._best_reward = mean_reward
            self._wait = 0
        else:
            self._wait += 1
            if self._wait >= self.patience:
                print(f"  [EarlyStop] Reward plateau: {self.patience} updates 无改善")
                return True
        return False


# ---------------------------------------------------------------------------
# PPO 算法
# ---------------------------------------------------------------------------

class PPO:
    def __init__(self, model: nn.Module, lr: float = 3e-4,
                 clip_eps: float = 0.2, gamma: float = 0.99,
                 gae_lambda: float = 0.95, epochs: int = 4,
                 batch_size: int = 64, max_grad_norm: float = 0.5,
                 entropy_coef: float = 0.01, device: str = "cpu",
                 total_training_steps: int = 1_000_000) -> None:
        self.model = model.to(device)
        self.device = device
        self.clip_eps = clip_eps
        self.gamma = gamma
        self.gae_lambda = gae_lambda
        self.epochs = epochs
        self.batch_size = batch_size
        self.max_grad_norm = max_grad_norm
        self.entropy_coef = entropy_coef
        self._lr = lr
        self._total_updates = 0
        self._total_training_steps = total_training_steps
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)

    def update(self, buffer: RolloutBuffer) -> dict:
        self.model.train()
        advantages = buffer.advantages
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        buffer.advantages = advantages.to(self.device)

        epoch_metrics: dict[str, list[float]] = {
            "policy_loss": [], "value_loss": [], "entropy": [], "kl_approx": [],
        }

        for _ in range(self.epochs):
            for obs_batch, actions, old_lp, returns, adv_batch, masks in buffer.get_batches(self.batch_size):
                actions = actions.to(self.device)
                old_lp = old_lp.to(self.device)
                returns = returns.to(self.device)
                adv_batch = adv_batch.to(self.device)
                masks = masks.to(self.device)

                log_probs, values, entropy = self.model.evaluate_actions(obs_batch, actions, masks)

                ratio = torch.exp(log_probs - old_lp)
                surr1 = ratio * adv_batch
                surr2 = torch.clamp(ratio, 1.0 - self.clip_eps, 1.0 + self.clip_eps) * adv_batch
                policy_loss = -torch.min(surr1, surr2).mean()
                value_loss = 0.5 * ((values - returns) ** 2).mean()
                entropy_loss = entropy.mean()

                loss = policy_loss + 0.5 * value_loss - self.entropy_coef * entropy_loss

                self.optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(self.model.parameters(), self.max_grad_norm)
                self.optimizer.step()

                kl = (old_lp - log_probs).mean().item()
                epoch_metrics["policy_loss"].append(policy_loss.item())
                epoch_metrics["value_loss"].append(value_loss.item())
                epoch_metrics["entropy"].append(entropy.mean().item())
                epoch_metrics["kl_approx"].append(kl)

        self._total_updates += 1
        self._decay_lr()

        metrics = {k: float(np.mean(v)) for k, v in epoch_metrics.items()}

        if _WANDB and wandb.run is not None:
            wandb.log({
                "ppo/policy_loss": metrics["policy_loss"],
                "ppo/value_loss": metrics["value_loss"],
                "ppo/entropy": metrics["entropy"],
                "ppo/kl_approx": metrics["kl_approx"],
                "ppo/lr": self.optimizer.param_groups[0]["lr"],
                "ppo/update": self._total_updates,
            })
        return metrics

    def _decay_lr(self) -> None:
        factor = max(1.0 - self._total_updates / self._total_training_steps, 0.0)
        for pg in self.optimizer.param_groups:
            pg["lr"] = self._lr * factor

    def save(self, path: str, reward_normalizer: RewardNormalizer | None = None) -> None:
        ckpt: dict = {
            "model": self.model.state_dict(),
            "optimizer": self.optimizer.state_dict(),
            "total_updates": self._total_updates,
        }
        if reward_normalizer is not None:
            ckpt["reward_normalizer"] = reward_normalizer.state_dict()
        torch.save(ckpt, path)

    def load(self, path: str, reward_normalizer: RewardNormalizer | None = None) -> None:
        ckpt = torch.load(path, map_location=self.device, weights_only=False)
        self.model.load_state_dict(ckpt["model"])
        self.optimizer.load_state_dict(ckpt["optimizer"])
        self._total_updates = ckpt.get("total_updates", 0)
        if reward_normalizer is not None and "reward_normalizer" in ckpt:
            reward_normalizer.load_state_dict(ckpt["reward_normalizer"])
