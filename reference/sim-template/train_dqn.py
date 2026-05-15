"""DQN 训练模板 — off-policy value-based RL。

取自: projects/hgat-satellite-dag-offloading/simulator/dqn.py
核心设计思想:
  - ReplayBuffer: deque-based，支持 push/sample/__len__，预留优先采样骨架
  - soft target update (Polyak averaging, tau=0.005)
  - Huber loss (smooth_l1) — 对大 TD error 更鲁棒
  - gradient clipping + epsilon 线性衰减
  - running reward normalization (Welford)
  - save/load: model + target + optimizer + epsilon
  - wandb 集成骨架（条件导入）

CUSTOMIZE 标记: 搜索 "# --- CUSTOMIZE ---" 找到所有需要定制的位置。
"""

from __future__ import annotations

import random
from collections import deque
from typing import Any

import numpy as np
import torch
import torch.nn as nn

# 复用 train_ppo 中的 RewardNormalizer（Welford 在线算法），不在 DQN 中重写
from .train_ppo import RewardNormalizer
from .train_ppo import EarlyStopping

# --- CUSTOMIZE: wandb 条件导入 ---
try:
    import wandb
    _WANDB = True
except ImportError:
    wandb = None  # type: ignore[assignment]
    _WANDB = False


# ---------------------------------------------------------------------------
# ReplayBuffer — 经验回放
# ---------------------------------------------------------------------------

class ReplayBuffer:
    """标准经验回放缓冲区，预留优先采样骨架。

    --- CUSTOMIZE: 如需 prioritized experience replay，在 push 时计算 priority，
        在 sample 时按 priority 加权采样 ---
    """

    def __init__(self, capacity: int = 50000) -> None:
        self.buf: deque[tuple[Any, ...]] = deque(maxlen=capacity)
        self.capacity = capacity
        # --- CUSTOMIZE: 优先采样相关字段 ---
        # self.priorities = deque(maxlen=capacity)
        # self._alpha = 0.6   # priority exponent
        # self._beta = 0.4    # importance sampling exponent

    def push(
        self,
        obs: Any,
        action: int,
        reward: float,
        next_obs: Any,
        done: bool,
        mask: np.ndarray,
        next_mask: np.ndarray,
    ) -> None:
        """存储一条 transition。"""
        self.buf.append((obs, action, reward, next_obs, done, mask, next_mask))
        # --- CUSTOMIZE: 优先采样 priority ---
        # self.priorities.append(max_priority)

    def sample(self, batch_size: int) -> tuple[Any, ...]:
        """均匀随机采样一个 batch。"""
        batch = random.sample(self.buf, batch_size)
        return tuple(zip(*batch))  # type: ignore[return-value]

        # --- CUSTOMIZE: 优先采样实现 ---
        # probs = np.array(self.priorities) ** self._alpha
        # probs /= probs.sum()
        # indices = np.random.choice(len(self.buf), batch_size, p=probs)
        # batch = [self.buf[i] for i in indices]
        # ...

    def __len__(self) -> int:
        return len(self.buf)


# ---------------------------------------------------------------------------
# DQN Agent
# ---------------------------------------------------------------------------

class DQNAgent:
    """DQN agent with soft target update + Huber loss + gradient clipping。

    设计要点:
      - soft target update (Polyak averaging, tau): θ_target = τ·θ + (1-τ)·θ_target
      - Huber loss (smooth_l1): 对大 TD error 鲁棒
      - gradient clipping: 防止梯度爆炸
      - epsilon 线性衰减: 探索 → 利用
      - running reward normalization: Welford 在线统计
    """

    def __init__(
        self,
        q_net: nn.Module,
        n_actions: int,
        lr: float = 1e-3,
        gamma: float = 0.99,
        batch_size: int = 128,
        buffer_capacity: int = 50000,
        target_tau: float = 0.005,
        epsilon_start: float = 1.0,
        epsilon_end: float = 0.05,
        epsilon_decay_steps: int = 10000,
        max_grad_norm: float = 1.0,
        device: str = "cpu",
    ) -> None:
        self.n_actions = n_actions
        self.gamma = gamma
        self.batch_size = batch_size
        self.target_tau = target_tau
        self.epsilon = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay_steps = epsilon_decay_steps
        self.max_grad_norm = max_grad_norm
        self.device = device

        self.q_net = q_net.to(device)
        # --- CUSTOMIZE: 确保 target_net 和 q_net 结构完全一致 ---
        self.target_net = type(q_net)(**_get_init_kwargs(q_net)).to(device)
        self.target_net.load_state_dict(self.q_net.state_dict())
        self.target_net.eval()

        self.optimizer = torch.optim.Adam(self.q_net.parameters(), lr=lr)
        self.buffer = ReplayBuffer(buffer_capacity)
        self._total_steps = 0
        self.reward_normalizer = RewardNormalizer()  # 复用 train_ppo 的 Welford 实现

    def select_action(self, obs, action_mask: np.ndarray) -> int:
        """epsilon-greedy action selection with action masking。"""
        if random.random() < self.epsilon:
            valid = np.where(action_mask)[0]
            return int(random.choice(valid))
        with torch.no_grad():
            # --- CUSTOMIZE: 替换为你的 q_net 前向接口 ---
            q = self.q_net(obs)
            mask = torch.as_tensor(action_mask, dtype=torch.bool, device=q.device)
            q = q.masked_fill(~mask, -1e8)
            return int(q.argmax().item())

    def store(self, obs, action: int, reward: float, next_obs, done: bool,
              mask: np.ndarray, next_mask: np.ndarray) -> None:
        """存储 transition（reward normalization 在 update 时批量处理）。"""
        self.buffer.push(obs, action, reward, next_obs, done, mask, next_mask)

    def update(self) -> dict | None:
        """从 buffer 采样并更新 Q 网络。返回 metrics dict 或 None（buffer 不够时）。"""
        if len(self.buffer) < self.batch_size:
            return None

        obs, actions, rewards, next_obs, dones, masks, next_masks = \
            self.buffer.sample(self.batch_size)

        self.q_net.train()

        actions_t = torch.tensor(actions, dtype=torch.long, device=self.device)
        rewards_t = torch.tensor(rewards, dtype=torch.float32, device=self.device)
        dones_t = torch.tensor(dones, dtype=torch.float32, device=self.device)

        # Normalize rewards using RewardNormalizer (Welford)
        rewards_list = list(rewards)
        normed_rewards = self.reward_normalizer.update_and_normalize(rewards_list)
        rewards_norm = torch.tensor(normed_rewards, dtype=torch.float32, device=self.device)

        # --- CUSTOMIZE: 替换为你的 q_net batch 前向接口 ---
        # Current Q values
        q_all = self.q_net.forward_batch(obs)  # (B, n_actions)
        q_values = q_all.gather(1, actions_t.unsqueeze(1)).squeeze(1)  # (B,)

        # Target Q values
        with torch.no_grad():
            next_q_all = self.target_net.forward_batch(next_obs)  # (B, n_actions)
            for i, nm in enumerate(next_masks):
                nm_t = torch.as_tensor(nm, dtype=torch.bool, device=self.device)
                next_q_all[i] = next_q_all[i].masked_fill(~nm_t, -1e8)
            next_q_max = next_q_all.max(dim=1).values  # (B,)
            targets = rewards_norm + self.gamma * next_q_max * (1.0 - dones_t)

        # Huber loss (smooth_l1)
        loss = nn.functional.smooth_l1_loss(q_values, targets)

        self.optimizer.zero_grad()
        loss.backward()
        nn.utils.clip_grad_norm_(self.q_net.parameters(), self.max_grad_norm)
        self.optimizer.step()

        # Soft update target network (Polyak averaging)
        for tp, sp in zip(self.target_net.parameters(), self.q_net.parameters()):
            tp.data.mul_(1.0 - self.target_tau)
            tp.data.add_(self.target_tau * sp.data)

        # Epsilon 线性衰减
        self._total_steps += 1
        self.epsilon = max(
            self.epsilon_end,
            self.epsilon_start - (self.epsilon_start - self.epsilon_end)
            * self._total_steps / self.epsilon_decay_steps,
        )

        metrics = {"loss": loss.item(), "epsilon": self.epsilon}

        # --- CUSTOMIZE: wandb log ---
        if _WANDB and wandb.run is not None:
            wandb.log({
                "dqn/loss": metrics["loss"],
                "dqn/epsilon": metrics["epsilon"],
                "dqn/step": self._total_steps,
            })

        return metrics

    def save(self, path: str) -> None:
        """保存 checkpoint: model + target + optimizer + epsilon + normalizer。"""
        torch.save({
            "q_net": self.q_net.state_dict(),
            "target_net": self.target_net.state_dict(),
            "optimizer": self.optimizer.state_dict(),
            "epsilon": self.epsilon,
            "total_steps": self._total_steps,
            "reward_normalizer": self.reward_normalizer.state_dict(),
        }, path)

    def load(self, path: str) -> None:
        """加载 checkpoint，恢复训练状态。"""
        ckpt = torch.load(path, map_location=self.device, weights_only=False)
        self.q_net.load_state_dict(ckpt["q_net"])
        self.target_net.load_state_dict(ckpt["target_net"])
        self.optimizer.load_state_dict(ckpt["optimizer"])
        self.epsilon = ckpt["epsilon"]
        self._total_steps = ckpt.get("total_steps", 0)
        if "reward_normalizer" in ckpt:
            self.reward_normalizer.load_state_dict(ckpt["reward_normalizer"])


# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------

def _get_init_kwargs(module: nn.Module) -> dict:
    """尝试从 __init__ 参数中提取构造 kwargs（用于 clone target_net）。

    --- CUSTOMIZE: 如果你的 QNetwork 构造参数复杂，直接手动构造 target_net ---
    """
    import inspect
    sig = inspect.signature(type(module).__init__)
    params = list(sig.parameters.keys())[1:]  # skip 'self'
    kwargs = {}
    for p in params:
        if hasattr(module, p):
            kwargs[p] = getattr(module, p)
        elif f"_{p}" in module.__dict__:
            kwargs[p] = module.__dict__[f"_{p}"]
    return kwargs


# ---------------------------------------------------------------------------
# 训练循环骨架
# ---------------------------------------------------------------------------

def train(
    env,
    agent: DQNAgent,
    n_episodes: int = 500,
    seed: int = 42,
    results_dir: str = "results",
    # --- Early stopping ---
    early_stop_patience: int = 50,
    early_stop_kl_threshold: float = 0.15,
    # --- CUSTOMIZE: 其他超参数 ---
    warmup_steps: int = 1000,
    train_freq: int = 4,
) -> dict:
    """DQN 训练主循环。

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

    early_stopper = EarlyStopping(patience=early_stop_patience, kl_threshold=early_stop_kl_threshold)

    episode_rewards: list[float] = []
    all_metrics: list[dict] = []

    for ep in range(n_episodes):
        obs, info = env.reset()
        done = False
        ep_reward = 0.0
        step_count = 0

        while not done:
            action_mask = info.get("action_mask", np.ones(agent.n_actions, dtype=bool))
            action = agent.select_action(obs, action_mask)
            next_obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            next_mask = info.get("action_mask", np.ones(agent.n_actions, dtype=bool))

            agent.store(obs, action, reward, next_obs, done, action_mask, next_mask)

            # 每 train_freq 步训练一次（warmup 后）
            if step_count >= warmup_steps and step_count % train_freq == 0:
                metrics = agent.update()
                if metrics is not None:
                    all_metrics.append(metrics)

            obs = next_obs
            ep_reward += reward
            step_count += 1

        episode_rewards.append(ep_reward)

        # Early stopping 检查（基于滑动窗口均值）
        if len(episode_rewards) >= 50:
            window_mean = float(np.mean(episode_rewards[-50:]))
            last_kl = all_metrics[-1].get("loss", 0.0) if all_metrics else 0.0
            should_stop = early_stopper.step(window_mean, last_kl)
            if should_stop:
                print(f"  [EarlyStop] 在 episode {ep+1} 触发停止")
                break

        # 定期打印进度
        if (ep + 1) % 50 == 0:
            recent = episode_rewards[-50:]
            mean_r = np.mean(recent)
            eps = agent.epsilon
            buf_len = len(agent.buffer)
            print(f"  ep={ep+1}/{n_episodes} reward(last50)={mean_r:.2f} "
                  f"epsilon={eps:.4f} buffer={buf_len}")

            # --- CUSTOMIZE: wandb log ---
            if _WANDB and wandb.run is not None:
                wandb.log({
                    "train/episode_reward_mean50": mean_r,
                    "train/episode": ep + 1,
                    "train/epsilon": eps,
                })

    # 保存结果
    results = {
        "episode_rewards": episode_rewards,
        "n_episodes": n_episodes,
        "seed": seed,
    }
    out = results_path / f"dqn_seed{seed}.json"
    with open(out, "w") as f:
        json.dump(results, f)
    agent.save(str(results_path / f"dqn_seed{seed}.pt"))

    return results
