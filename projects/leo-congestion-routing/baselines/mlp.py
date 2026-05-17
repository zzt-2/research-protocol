#!/usr/bin/env python3
"""MLP ablation baseline: same routing task as GNN but without message passing.

Architecture mirrors RoutingActorCritic (model.py) but replaces GATEncoder
with a per-node independent Linear projection (no GNN layers).
Trained with self-contained PPO loop.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor
from torch.distributions import Normal
from torch_geometric.data import Data

_PROJECT = Path(__file__).resolve().parent.parent
if str(_PROJECT) not in sys.path:
    sys.path.insert(0, str(_PROJECT))

from simulator.config import SimConfig
from simulator.env import RoutingEnv


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------


class MLPActorCritic(nn.Module):
    """MLP actor-critic: independent per-node projection, no message passing.

    Architecture:
      - Node encoder: Linear(node_dim, hidden) -> ReLU -> Linear(hidden, hidden)
      - Edge decoder: same EdgeWeightDecoder as model.py (MLP over emb_u || emb_v || edge_feat)
      - Critic: Linear(hidden, hidden) -> ReLU -> Linear(hidden, 1) on mean-pooled embeddings
      - Gaussian policy with learned log_std

    Args:
        node_dim: Node feature dimension (default 6).
        edge_dim: Edge feature dimension (default 4).
        hidden_dim: Hidden dimension.
        n_edges: Number of directed edges (for log_std parameter).
    """

    def __init__(
        self,
        node_dim: int = 6,
        edge_dim: int = 4,
        hidden_dim: int = 64,
        n_edges: int = 264,
    ) -> None:
        super().__init__()
        self.node_encoder = nn.Sequential(
            nn.Linear(node_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
        )
        self.edge_decoder = nn.Sequential(
            nn.Linear(hidden_dim * 2 + edge_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )
        self.critic = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )
        self.log_std = nn.Parameter(torch.zeros(n_edges))

    def forward(self, data: Data) -> tuple[Tensor, Tensor]:
        """Forward pass.

        Args:
            data: PyG Data with x, edge_index, edge_attr.

        Returns:
            (edge_weights_mean, value) — shapes (E,) and scalar.
        """
        data = data.to(self.device)
        h = self.node_encoder(data.x)  # (N, hidden) — no message passing

        # Edge weights: MLP(emb_u || emb_v || edge_feat) -> softplus
        src, dst = data.edge_index[0], data.edge_index[1]
        edge_input = torch.cat([h[src], h[dst], data.edge_attr], dim=-1)
        raw = self.edge_decoder(edge_input).squeeze(-1)
        weights_mean = F.softplus(raw) + 1e-6

        value = self.critic(h.mean(dim=0)).squeeze(-1)
        return weights_mean, value

    @torch.no_grad()
    def get_action(
        self, data: Data, deterministic: bool = False,
    ) -> tuple[Tensor, Tensor, Tensor]:
        """Sample action from Gaussian policy.

        Returns:
            (action, log_prob, value).
        """
        mean, value = self.forward(data)
        if deterministic:
            action = mean.clone()
            log_prob = torch.tensor(0.0, device=self.device)
        else:
            std = self.log_std.exp()
            dist = Normal(mean, std)
            action = dist.sample()
            action = torch.where(torch.isnan(action), mean, action)
            log_prob = dist.log_prob(action).sum()
        return action, log_prob, value

    def evaluate_actions(
        self, data_list: list[Data], actions: Tensor,
    ) -> tuple[Tensor, Tensor, Tensor]:
        """Re-evaluate actions for PPO update.

        Returns:
            (log_probs, values, entropies) — each shape (B,).
        """
        log_probs_list: list[Tensor] = []
        values_list: list[Tensor] = []
        entropies_list: list[Tensor] = []
        for i, data in enumerate(data_list):
            mean, value = self.forward(data)
            std = self.log_std.exp()
            dist = Normal(mean, std)
            log_probs_list.append(dist.log_prob(actions[i]).sum())
            values_list.append(value.squeeze())
            entropies_list.append(dist.entropy().sum())
        return (
            torch.stack(log_probs_list),
            torch.stack(values_list),
            torch.stack(entropies_list),
        )

    @property
    def device(self) -> torch.device:
        return next(self.parameters()).device


# ---------------------------------------------------------------------------
# Rollout buffer
# ---------------------------------------------------------------------------


class _RolloutBuffer:
    """Simple PPO rollout buffer."""

    def __init__(self) -> None:
        self.data_list: list[Data] = []
        self.actions: list[np.ndarray] = []
        self.log_probs: list[float] = []
        self.rewards: list[float] = []
        self.values: list[float] = []
        self.dones: list[bool] = []

    def push(
        self,
        data: Data,
        action: np.ndarray,
        log_prob: float,
        reward: float,
        value: float,
        done: bool,
    ) -> None:
        self.data_list.append(data)
        self.actions.append(action)
        self.log_probs.append(log_prob)
        self.rewards.append(reward)
        self.values.append(value)
        self.dones.append(done)

    def __len__(self) -> int:
        return len(self.rewards)


# ---------------------------------------------------------------------------
# PPO training
# ---------------------------------------------------------------------------


def _compute_gae(
    rewards: list[float],
    values: list[float],
    dones: list[bool],
    gamma: float = 0.99,
    lam: float = 0.95,
) -> tuple[np.ndarray, np.ndarray]:
    """Generalized Advantage Estimation."""
    n = len(rewards)
    advantages = np.zeros(n, dtype=np.float32)
    returns = np.zeros(n, dtype=np.float32)
    gae = 0.0
    for t in reversed(range(n)):
        if t == n - 1 or dones[t]:
            delta = rewards[t] - values[t]
            gae = delta
        else:
            delta = rewards[t] + gamma * values[t + 1] - values[t]
            gae = delta + gamma * lam * gae
        advantages[t] = gae
        returns[t] = gae + values[t]
    adv_std = advantages.std()
    if adv_std > 1e-8:
        advantages = (advantages - advantages.mean()) / adv_std
    return advantages, returns


def _ppo_update(
    model: MLPActorCritic,
    optimizer: torch.optim.Optimizer,
    buf: _RolloutBuffer,
    clip_eps: float = 0.2,
    entropy_coef: float = 0.01,
    value_coef: float = 0.5,
    max_grad_norm: float = 0.5,
    n_epochs: int = 4,
) -> None:
    """PPO clipped surrogate update over rollout buffer."""
    advantages, returns = _compute_gae(buf.rewards, buf.values, buf.dones)
    actions_t = torch.tensor(np.array(buf.actions), dtype=torch.float32)
    old_log_probs_t = torch.tensor(buf.log_probs, dtype=torch.float32)
    adv_t = torch.tensor(advantages, dtype=torch.float32)
    ret_t = torch.tensor(returns, dtype=torch.float32)

    for _ in range(n_epochs):
        log_probs, values, entropies = model.evaluate_actions(buf.data_list, actions_t)
        ratio = (log_probs - old_log_probs_t).exp()
        surr1 = ratio * adv_t
        surr2 = torch.clamp(ratio, 1 - clip_eps, 1 + clip_eps) * adv_t
        actor_loss = -torch.min(surr1, surr2).mean()
        critic_loss = F.mse_loss(values, ret_t)
        entropy_loss = -entropies.mean()

        loss = actor_loss + value_coef * critic_loss + entropy_coef * entropy_loss

        optimizer.zero_grad()
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
        optimizer.step()


def _train_mlp(
    env: RoutingEnv,
    model: MLPActorCritic,
    n_episodes: int = 300,
    lr: float = 3e-4,
    seed: int = 0,
    update_interval: int = 10,
) -> list[float]:
    """Train MLP baseline with PPO. Returns per-episode final MLU list."""
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    rng = np.random.default_rng(seed)
    episode_mlus: list[float] = []

    for ep in range(n_episodes):
        buf = _RolloutBuffer()
        obs, info = env.reset(seed=int(rng.integers(0, 2**31)))
        done = False
        last_info: dict = info

        while not done:
            action_tensor, log_prob, value = model.get_action(obs)
            action_np = action_tensor.cpu().numpy()
            # Clamp to positive — Dijkstra requires non-negative weights
            action_np = np.maximum(action_np, 1e-3)
            obs, reward, terminated, truncated, info = env.step(action_np)
            done = terminated or truncated
            buf.push(obs, action_np, log_prob.item(), reward, value.item(), done)
            last_info = info

        _ppo_update(model, optimizer, buf)
        episode_mlus.append(last_info.get("mlu", 0.0))

        if (ep + 1) % 50 == 0:
            recent = episode_mlus[-50:]
            print(f"  Ep {ep+1:4d}: MLU = {np.mean(recent):.4f} +/- {np.std(recent):.4f}")

    return episode_mlus


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def run_mlp(
    env_config: SimConfig | None = None,
    n_eval: int = 50,
    seed: int = 0,
    n_episodes: int = 300,
    seed_offset: int = 300000,
) -> dict[str, float]:
    """Train MLP baseline and evaluate.

    Args:
        env_config: SimConfig (uses defaults if None).
        n_eval: Number of evaluation episodes.
        seed: Training seed.
        n_episodes: PPO training episodes.
        seed_offset: Base seed for evaluation.

    Returns:
        {"mean": mean MLU, "std": std MLU} across evaluation episodes.
    """
    config = env_config or SimConfig()
    env = RoutingEnv(config, seed=seed)

    model = MLPActorCritic(
        node_dim=config.node_feat_dim,
        edge_dim=config.edge_feat_dim,
        hidden_dim=config.hidden_dim,
        n_edges=env._E,
    )

    print(f"[MLP seed={seed}] Training for {n_episodes} episodes...")
    _train_mlp(env, model, n_episodes=n_episodes, seed=seed)

    # Evaluate with deterministic policy
    mlus: list[float] = []
    for i in range(n_eval):
        obs, info = env.reset(seed=seed_offset + i)
        done = False
        step_mlus: list[float] = []
        while not done:
            action, _, _ = model.get_action(obs, deterministic=True)
            action_np = np.maximum(action.cpu().numpy(), 1e-3)
            obs, _, terminated, truncated, info = env.step(action_np)
            done = terminated or truncated
            step_mlus.append(info["mlu"])
        mlus.append(float(np.mean(step_mlus)))

    result = {"mean": float(np.mean(mlus)), "std": float(np.std(mlus))}
    print(f"[MLP seed={seed}] Eval: MLU = {result['mean']:.4f} +/- {result['std']:.4f}")
    return result


if __name__ == "__main__":
    config = SimConfig()
    result = run_mlp(config, n_eval=50, n_episodes=300)
    print(f"\nMLP Baseline: MLU = {result['mean']:.4f} +/- {result['std']:.4f}")
