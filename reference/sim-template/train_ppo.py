"""PPO 训练模板 — 通用 on-policy 训练循环。

取自: projects/hgat-satellite-dag-offloading/simulator/ppo.py + train.py
核心设计思想:
  - RolloutBuffer 支持 GAE(λ) + mini-batch 迭代，obs 保留为 list（兼容 HeteroData）
  - RewardNormalizer: Welford 在线算法，running mean/var，clip [-5, 5]
  - PPO 核心: gradient clipping + advantage normalization + linear LR decay + entropy bonus + clip_range
  - save/load 支持 resume（model + optimizer + normalizer + step_count）
  - wandb 集成骨架（条件导入）
  - Early stopping 骨架（reward plateau + KL 散度双条件）

CUSTOMIZE 标记: 搜索 "# --- CUSTOMIZE ---" 找到所有需要定制的位置。
"""

from __future__ import annotations

from typing import Generator

import numpy as np
import torch
import torch.nn as nn
from torch import Tensor
from torch.distributions import Categorical

# --- CUSTOMIZE: wandb 条件导入 ---
# 如果可用就自动 log，不影响无 wandb 的环境
try:
    import wandb
    _WANDB = True
except ImportError:
    wandb = None  # type: ignore[assignment]
    _WANDB = False


# ---------------------------------------------------------------------------
# RolloutBuffer — on-policy 转移存储，支持 GAE(λ) + mini-batch
# ---------------------------------------------------------------------------

class RolloutBuffer:
    """On-policy buffer for PPO transitions.

    Observations 保留为 Python list，以兼容无法 stack 的自定义类型
    （如 torch_geometric HeteroData）。其余字段在计算 GAE 时转为 Tensor。
    """

    def __init__(self) -> None:
        self.obs: list = []           # --- CUSTOMIZE: 替换为你的 obs 类型 ---
        self.actions: list[int] = []
        self.log_probs: list[float] = []
        self.rewards: list[float] = []
        self.dones: list[bool] = []
        self.values: list[float] = []
        self.action_masks: list[np.ndarray] = []

        # GAE 计算后填充
        self.returns: Tensor | None = None
        self.advantages: Tensor | None = None

    def add(
        self,
        obs,
        action: int,
        log_prob: float,
        reward: float,
        done: bool,
        value: float,
        action_mask: np.ndarray,
    ) -> None:
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

    def compute_returns_and_advantages(self, last_value: float, gamma: float, gae_lambda: float) -> None:
        """GAE(λ) advantage estimation.

        δ_t = r_t + γ · V(s_{t+1}) · (1 − d_t) − V(s_t)
        A_t = Σ_{l≥0} (γλ)^l · δ_{t+l}
        """
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

    def get_batches(
        self, batch_size: int
    ) -> Generator[tuple[list, Tensor, Tensor, Tensor, Tensor, Tensor], None, None]:
        """Yield shuffled mini-batches from the buffer."""
        n = self.size
        indices = np.arange(n)
        np.random.shuffle(indices)

        actions_t = torch.tensor(self.actions, dtype=torch.long)
        old_log_probs_t = torch.tensor(self.log_probs, dtype=torch.float32)
        masks_t = torch.tensor(np.stack(self.action_masks), dtype=torch.bool)

        for start in range(0, n, batch_size):
            idx = indices[start : start + batch_size]
            yield (
                [self.obs[i] for i in idx],
                actions_t[idx],
                old_log_probs_t[idx],
                self.returns[idx],
                self.advantages[idx],
                masks_t[idx],
            )


# ---------------------------------------------------------------------------
# RewardNormalizer — Welford 在线算法
# ---------------------------------------------------------------------------

class RewardNormalizer:
    """Running Z-score normalization for rewards (Welford 在线算法).

    维护 running mean/var，输出 clip 到 [-clip, +clip]。
    支持 state_dict 以便 save/load。
    """

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
        m2 = (self._var * self._count + batch_var * n
              + delta ** 2 * self._count * n / total)
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
# PPO 算法
# ---------------------------------------------------------------------------

class PPO:
    """Proximal Policy Optimization with clipped surrogate objective.

    设计要点:
      - gradient clipping (max_grad_norm)
      - advantage normalization (全 rollout 标准化)
      - linear LR decay (按 update 次数线性衰减)
      - entropy coefficient
      - clip_range (PPO 核心 clip)
    """

    def __init__(
        self,
        model: nn.Module,
        lr: float = 3e-4,
        clip_eps: float = 0.2,
        gamma: float = 0.99,
        gae_lambda: float = 0.95,
        epochs: int = 4,
        batch_size: int = 64,
        max_grad_norm: float = 0.5,
        entropy_coef: float = 0.01,
        device: str = "cpu",
        # --- CUSTOMIZE: 总训练步数，用于 LR decay 计算 ---
        total_training_steps: int = 1_000_000,
    ) -> None:
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

    # ------------------------------------------------------------------
    # PPO update（需配合 RolloutBuffer 使用）
    # ------------------------------------------------------------------

    def update(self, buffer: RolloutBuffer) -> dict:
        """Run PPO clipped update over the buffer.  Returns metrics dict."""
        self.model.train()

        # Normalise advantages across the full rollout
        advantages = buffer.advantages
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        buffer.advantages = advantages.to(self.device)

        epoch_metrics: dict[str, list[float]] = {
            "policy_loss": [], "value_loss": [], "entropy": [], "kl_approx": [],
        }

        for _epoch in range(self.epochs):
            for obs_batch, actions, old_log_probs, returns, adv_batch, masks in (
                buffer.get_batches(self.batch_size)
            ):
                actions = actions.to(self.device)
                old_log_probs = old_log_probs.to(self.device)
                returns = returns.to(self.device)
                adv_batch = adv_batch.to(self.device)
                masks = masks.to(self.device)

                # --- CUSTOMIZE: 替换 evaluate_actions 为你的 model 前向逻辑 ---
                # 期望返回 (log_probs, values, entropy) 三个 Tensor
                log_probs, values, entropy = self.model.evaluate_actions(
                    obs_batch, actions, masks
                )

                # ---- Policy loss (clipped surrogate) ----
                ratio = torch.exp(log_probs - old_log_probs)
                surr1 = ratio * adv_batch
                surr2 = torch.clamp(ratio, 1.0 - self.clip_eps, 1.0 + self.clip_eps) * adv_batch
                policy_loss = -torch.min(surr1, surr2).mean()

                # ---- Value loss ----
                value_loss = 0.5 * ((values - returns) ** 2).mean()

                # ---- Entropy bonus ----
                entropy_loss = entropy.mean()

                # ---- Total loss ----
                loss = policy_loss + 0.5 * value_loss - self.entropy_coef * entropy_loss

                self.optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(self.model.parameters(), self.max_grad_norm)
                self.optimizer.step()

                kl = (old_log_probs - log_probs).mean().item()

                epoch_metrics["policy_loss"].append(policy_loss.item())
                epoch_metrics["value_loss"].append(value_loss.item())
                epoch_metrics["entropy"].append(entropy_loss.item())
                epoch_metrics["kl_approx"].append(kl)

        self._total_updates += 1
        self._decay_lr()

        metrics = {k: float(np.mean(v)) for k, v in epoch_metrics.items()}

        # --- CUSTOMIZE: wandb log ---
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

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _decay_lr(self) -> None:
        """Linear LR decay based on total update count."""
        factor = max(1.0 - self._total_updates / self._total_training_steps, 0.0)
        for pg in self.optimizer.param_groups:
            pg["lr"] = self._lr * factor

    def save(self, path: str, reward_normalizer: RewardNormalizer | None = None) -> None:
        """保存 checkpoint，包含 model + optimizer + normalizer + step_count。"""
        ckpt: dict = {
            "model": self.model.state_dict(),
            "optimizer": self.optimizer.state_dict(),
            "total_updates": self._total_updates,
        }
        if reward_normalizer is not None:
            ckpt["reward_normalizer"] = reward_normalizer.state_dict()
        torch.save(ckpt, path)

    def load(self, path: str, reward_normalizer: RewardNormalizer | None = None) -> None:
        """加载 checkpoint，恢复训练状态。"""
        ckpt = torch.load(path, map_location=self.device, weights_only=False)
        self.model.load_state_dict(ckpt["model"])
        self.optimizer.load_state_dict(ckpt["optimizer"])
        self._total_updates = ckpt.get("total_updates", 0)
        if reward_normalizer is not None and "reward_normalizer" in ckpt:
            reward_normalizer.load_state_dict(ckpt["reward_normalizer"])


# ---------------------------------------------------------------------------
# Early Stopping — reward plateau + KL 散度双条件
# ---------------------------------------------------------------------------

class EarlyStopping:
    """基于 reward plateau + KL 散度的 early stopping。

    两个条件满足任一即触发停止:
      1. reward plateau: 最近 patience 次 update 的 mean reward 没有超过历史 best
      2. KL 散度: 近期平均 KL 超过阈值（策略更新过大）
    """

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
        """返回 True 表示应该停止训练。"""
        self._recent_kl.append(mean_kl)
        if len(self._recent_kl) > 5:
            self._recent_kl = self._recent_kl[-5:]

        # 条件 2: KL 过大
        if len(self._recent_kl) >= 3:
            avg_kl = float(np.mean(self._recent_kl))
            if avg_kl > self.kl_threshold:
                print(f"  [EarlyStop] KL 散度过大: avg_kl={avg_kl:.4f} > {self.kl_threshold}")
                return True

        # 条件 1: reward plateau
        if mean_reward > self._best_reward + self.min_improvement:
            self._best_reward = mean_reward
            self._wait = 0
        else:
            self._wait += 1
            if self._wait >= self.patience:
                print(f"  [EarlyStop] Reward plateau: {self.patience} updates 无改善")
                return True

        return False


# ---------------------------------------------------------------------------
# 训练循环骨架
# ---------------------------------------------------------------------------

def train(
    env,
    model: nn.Module,
    n_episodes: int = 500,
    update_interval: int = 10,
    seed: int = 42,
    device: str = "cpu",
    results_dir: str = "results",
    # --- CUSTOMIZE: PPO 超参数 ---
    lr: float = 3e-4,
    entropy_coef: float = 0.01,
    clip_eps: float = 0.2,
    gamma: float = 0.99,
    gae_lambda: float = 0.95,
    epochs: int = 4,
    batch_size: int = 64,
    max_grad_norm: float = 0.5,
    # --- Early stopping ---
    early_stop_patience: int = 50,
    early_stop_kl_threshold: float = 0.15,
) -> dict:
    """PPO 训练主循环。

    --- CUSTOMIZE: 根据你的 env/model 调整 obs/action 处理逻辑 ---
    """
    import json
    from pathlib import Path

    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    results_path = Path(results_dir)
    results_path.mkdir(exist_ok=True, parents=True)

    ppo = PPO(
        model, lr=lr, clip_eps=clip_eps, gamma=gamma, gae_lambda=gae_lambda,
        epochs=epochs, batch_size=batch_size, max_grad_norm=max_grad_norm,
        entropy_coef=entropy_coef, device=device,
    )
    reward_normalizer = RewardNormalizer()
    early_stopper = EarlyStopping(patience=early_stop_patience, kl_threshold=early_stop_kl_threshold)

    episode_rewards: list[float] = []
    all_metrics: list[dict] = []
    buf = RolloutBuffer()  # 只创建一次，跨 episode 累积

    for ep in range(n_episodes):
        obs, info = env.reset()
        done = False
        ep_reward = 0.0

        while not done:
            action_mask = info["action_mask"]
            # --- CUSTOMIZE: 替换为你的 model 推理接口 ---
            action, log_prob, value = model.get_action(obs, action_mask)
            next_obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

            buf.add(obs, action, log_prob, reward, done, value, action_mask)
            obs = next_obs
            ep_reward += reward

        episode_rewards.append(ep_reward)

        # 每 update_interval 个 episode 更新一次
        if (ep + 1) % update_interval == 0:
            buf.rewards = reward_normalizer.update_and_normalize(buf.rewards)

            with torch.no_grad():
                # --- CUSTOMIZE: 获取 bootstrap value ---
                _, last_val = model(obs)
                last_val = last_val.squeeze().item()
            buf.compute_returns_and_advantages(last_val, gamma, gae_lambda)

            metrics = ppo.update(buf)
            metrics["episode"] = ep
            metrics["episode_reward"] = float(np.mean(episode_rewards[-update_interval:]))
            all_metrics.append(metrics)

            buf = RolloutBuffer()  # 清空 buffer

            # Early stopping 检查
            should_stop = early_stopper.step(metrics["episode_reward"], metrics["kl_approx"])
            if should_stop:
                print(f"  [EarlyStop] 在 episode {ep+1} 触发停止")
                break

        # 定期打印进度
        if (ep + 1) % 50 == 0:
            recent = episode_rewards[-50:]
            mean_r = np.mean(recent)
            last_m = all_metrics[-1] if all_metrics else {}
            print(f"  ep={ep+1}/{n_episodes} reward(last50)={mean_r:.2f} "
                  f"ploss={last_m.get('policy_loss', 0):.4f} "
                  f"ent={last_m.get('entropy', 0):.4f}")

            # --- CUSTOMIZE: wandb log ---
            if _WANDB and wandb.run is not None:
                wandb.log({
                    "train/episode_reward_mean50": mean_r,
                    "train/episode": ep + 1,
                })

    # 保存结果
    results = {
        "episode_rewards": episode_rewards,
        "n_episodes": n_episodes,
        "seed": seed,
    }
    out = results_path / f"ppo_seed{seed}.json"
    with open(out, "w") as f:
        json.dump(results, f)
    ppo.save(str(results_path / f"ppo_seed{seed}.pt"), reward_normalizer)

    return results
