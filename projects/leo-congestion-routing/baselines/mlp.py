#!/usr/bin/env python3
"""MLP ablation baseline: K-path discrete selection with local features only.

Uses mlp_feat (src/dst node features + 1-hop loads + path lengths) instead of
GNN message passing. Same Categorical policy over K paths as GNN model.

Fairness-matched to GNN PPO training (train.py):
  - Same PPO hyperparameters from SimConfig
  - Reward normalization (Welford, same as GNN)
  - Linear LR decay (same schedule as GNN)
  - Same clip_eps, entropy_coef, max_grad_norm, gamma, gae_lambda
  - Update-interval batching (every N episodes, not per-episode)
  - Early stopping with configurable patience
  - Hidden dim = 64 (same as GNN hidden_dim) — the only difference is
    the absence of message passing layers.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Categorical

_PROJECT = Path(__file__).resolve().parent.parent
if str(_PROJECT) not in sys.path:
    sys.path.insert(0, str(_PROJECT))

from simulator.config import SimConfig
from simulator.env import RoutingEnv
from simulator.metrics import aggregate_metrics, compute_episode_metrics


# ---------------------------------------------------------------------------
# Model — hidden=64 to match GNN hidden_dim, only difference is no msg passing
# ---------------------------------------------------------------------------


class MLPActorCritic(nn.Module):
    """MLP actor-critic: local features only, no message passing.

    Uses mlp_feat from env obs: src_feat(6) + dst_feat(6) + src_nbr(4) +
    dst_nbr(4) + demand(1) + path_lens(K) = 21 + K dimensions.

    Architecture mirrors GNN parameter budget:
      backbone: 2-layer MLP (input→64→64), same hidden as GNN
      actor:    64→K  (vs GNN PathScoringHead 64→32→1, applied K times)
      critic:   64→64→1 (mirrors GNN value head 128→64→1)
    """

    def __init__(self, mlp_feat_dim: int, k_paths: int = 4, hidden: int = 64) -> None:
        super().__init__()
        self.K = k_paths
        self.backbone = nn.Sequential(
            nn.Linear(mlp_feat_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, hidden),
            nn.ReLU(),
        )
        self.actor = nn.Linear(hidden, k_paths)
        # Critic mirrors GNN: concat(src_emb, dst_emb) → 2*hidden → hidden → 1
        # But MLP has no separate src/dst embeddings, so use hidden → hidden → 1
        self.critic = nn.Sequential(
            nn.Linear(hidden, hidden),
            nn.ReLU(),
            nn.Linear(hidden, 1),
        )

    def _forward(self, obs: dict) -> tuple[torch.Tensor, torch.Tensor]:
        x = torch.as_tensor(obs["mlp_feat"], dtype=torch.float32)
        h = self.backbone(x)
        logits = self.actor(h)
        # Mask invalid actions
        n_valid = obs["n_valid"]
        mask = torch.full_like(logits, -1e9)
        mask[:n_valid] = logits[:n_valid]
        value = self.critic(h).squeeze()
        return mask, value

    @torch.no_grad()
    def get_action(self, obs: dict, deterministic: bool = False):
        logits, value = self._forward(obs)
        if deterministic:
            action = logits.argmax()
            log_prob = torch.tensor(0.0)
        else:
            dist = Categorical(logits=logits)
            action = dist.sample()
            log_prob = dist.log_prob(action)
        return action, log_prob, value

    def evaluate_actions(self, obs_list: list[dict], actions: torch.Tensor):
        log_probs, values, entropies = [], [], []
        for i, obs in enumerate(obs_list):
            logits, value = self._forward(obs)
            dist = Categorical(logits=logits)
            log_probs.append(dist.log_prob(actions[i]))
            values.append(value.squeeze())
            entropies.append(dist.entropy())
        return torch.stack(log_probs), torch.stack(values), torch.stack(entropies)


# ---------------------------------------------------------------------------
# RewardNormalizer — Welford online (copied from train.py for self-containment)
# ---------------------------------------------------------------------------


class _RewardNormalizer:
    """Running Z-score normalization for rewards (same as train.py)."""

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


# ---------------------------------------------------------------------------
# PPO training — matched to train.py GNN PPO loop
# ---------------------------------------------------------------------------


def _train_mlp(
    env,
    model,
    n_episodes: int = 800,
    lr: float = 3e-4,
    clip_eps: float = 0.2,
    gamma: float = 0.99,
    gae_lambda: float = 0.95,
    ppo_epochs: int = 4,
    batch_size: int = 64,
    max_grad_norm: float = 0.5,
    entropy_coef: float = 0.01,
    update_interval: int = 10,
    early_stop_patience: int = 50,
    seed: int = 0,
):
    """Train MLP with PPO, matching GNN training loop in train.py.

    Key fairness matches:
      - Reward normalization (Welford, same as GNN)
      - Linear LR decay (same formula as train.py PPO._decay_lr)
      - Same clip_eps, entropy_coef, max_grad_norm
      - Update-interval batching (every update_interval episodes, not per-episode)
      - Early stopping with reward plateau detection
    """
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    rng = np.random.default_rng(seed)
    episode_mlus: list[float] = []
    episode_rewards: list[float] = []
    reward_normalizer = _RewardNormalizer()

    # Early stopping state
    best_reward = -float("inf")
    wait = 0

    # LR decay state
    total_updates = 0

    def _decay_lr() -> None:
        nonlocal total_updates
        factor = max(1.0 - total_updates / n_episodes, 0.0)
        for pg in optimizer.param_groups:
            pg["lr"] = lr * factor

    # Rollout buffer (resets every update_interval episodes)
    buf_obs: list[dict] = []
    buf_actions: list[int] = []
    buf_rewards: list[float] = []
    buf_values: list[float] = []
    buf_logprobs: list[float] = []
    buf_dones: list[bool] = []

    for ep in range(n_episodes):
        obs, info = env.reset(seed=int(rng.integers(0, 2**31)))
        done = False
        ep_reward = 0.0
        last_info = info

        while not done:
            action, log_prob, value = model.get_action(obs)
            next_obs, reward, terminated, truncated, info = env.step(action.item())
            done = terminated or truncated
            buf_obs.append(obs)
            buf_actions.append(action.item())
            buf_rewards.append(reward)
            buf_values.append(value.item())
            buf_logprobs.append(log_prob.item())
            buf_dones.append(done)
            ep_reward += reward
            last_info = info
            obs = next_obs

        episode_mlus.append(last_info.get("final_mlu", last_info["mlu"]))
        episode_rewards.append(ep_reward)

        # Periodic PPO update (same as train.py: every update_interval episodes)
        if (ep + 1) % update_interval == 0:
            # Normalize rewards (same as GNN)
            buf_rewards = reward_normalizer.update_and_normalize(buf_rewards)

            # Bootstrap value for last obs
            with torch.no_grad():
                _, last_val = model._forward(obs)
                last_val = last_val.squeeze().item()

            # GAE computation (same formula as train.py RolloutBuffer)
            n = len(buf_rewards)
            rewards_t = torch.tensor(buf_rewards, dtype=torch.float32)
            values_t = torch.tensor(buf_values, dtype=torch.float32)
            dones_t = torch.tensor(buf_dones, dtype=torch.float32)
            values_t = torch.cat([values_t, torch.tensor([last_val])])

            advantages = torch.zeros(n, dtype=torch.float32)
            last_gae = 0.0
            for t in reversed(range(n)):
                delta = rewards_t[t] + gamma * values_t[t + 1] * (1.0 - dones_t[t]) - values_t[t]
                last_gae = delta + gamma * gae_lambda * (1.0 - dones_t[t]) * last_gae
                advantages[t] = last_gae
            returns = advantages + values_t[:n]

            # Normalize advantages (same as train.py PPO.update)
            advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

            actions_t = torch.tensor(buf_actions, dtype=torch.long)
            old_lp = torch.tensor(buf_logprobs, dtype=torch.float32)

            # Mini-batch PPO update (same as train.py)
            indices = np.arange(n)
            np.random.shuffle(indices)
            for _epoch in range(ppo_epochs):
                for start in range(0, n, batch_size):
                    idx = indices[start : start + batch_size]
                    obs_batch = [buf_obs[i] for i in idx]
                    act_batch = actions_t[idx]
                    olp_batch = old_lp[idx]
                    adv_batch = advantages[idx]
                    ret_batch = returns[idx]

                    new_lp, vals, ent = model.evaluate_actions(obs_batch, act_batch)
                    ratio = (new_lp - olp_batch).exp()
                    surr1 = ratio * adv_batch
                    surr2 = (
                        torch.clamp(ratio, 1.0 - clip_eps, 1.0 + clip_eps)
                        * adv_batch
                    )
                    policy_loss = -torch.min(surr1, surr2).mean()
                    value_loss = 0.5 * ((vals - ret_batch) ** 2).mean()
                    entropy_loss = ent.mean()
                    loss = policy_loss + 0.5 * value_loss - entropy_coef * entropy_loss

                    optimizer.zero_grad()
                    loss.backward()
                    nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
                    optimizer.step()

            # LR decay (same schedule as train.py)
            total_updates += 1
            _decay_lr()

            # Early stopping (reward plateau)
            mean_reward = float(np.mean(episode_rewards[-update_interval:]))
            if mean_reward > best_reward:
                best_reward = mean_reward
                wait = 0
            else:
                wait += 1
                if wait >= early_stop_patience:
                    print(f"  [EarlyStop] Reward plateau at episode {ep + 1}")
                    break

            # Clear buffer
            buf_obs, buf_actions, buf_rewards = [], [], []
            buf_values, buf_logprobs, buf_dones = [], [], []

        # Progress logging (same cadence as train.py)
        if (ep + 1) % 50 == 0:
            recent = episode_mlus[-50:]
            print(
                f"  ep={ep + 1}/{n_episodes} "
                f"MLU(last50)={np.mean(recent):.4f} +/- {np.std(recent):.4f} "
                f"lr={optimizer.param_groups[0]['lr']:.6f}"
            )

    return episode_mlus


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def run_mlp(
    env_config: SimConfig | None = None,
    n_eval: int = 50,
    seed: int = 0,
    n_episodes: int = 800,
    seed_offset: int = 300000,
) -> dict[str, float]:
    """Train MLP baseline and evaluate.

    Default n_episodes=800 to match E01-v2 GNN training.
    PPO hyperparameters are read from SimConfig to ensure fair comparison.
    """
    config = env_config or SimConfig()
    env = RoutingEnv(config, seed=seed)

    # Compute mlp_feat dimension from a sample obs
    sample_obs, _ = env.reset(seed=0)
    mlp_feat_dim = sample_obs["mlp_feat"].shape[0]

    # hidden=64 to match GNN hidden_dim — the only architectural difference
    # is the absence of message passing layers
    model = MLPActorCritic(mlp_feat_dim=mlp_feat_dim, k_paths=config.k_paths, hidden=config.hidden_dim)

    print(f"[MLP seed={seed}] Training for {n_episodes} episodes (hidden={config.hidden_dim})...")
    _train_mlp(
        env,
        model,
        n_episodes=n_episodes,
        lr=config.lr,
        clip_eps=config.clip_eps,
        gamma=config.gamma,
        gae_lambda=config.gae_lambda,
        ppo_epochs=config.n_epochs,
        batch_size=config.batch_size,
        max_grad_norm=config.max_grad_norm,
        entropy_coef=config.entropy_coef,
        update_interval=config.update_interval,
        early_stop_patience=config.early_stop_patience,
        seed=seed,
    )

    # Evaluate with greedy policy
    episode_metrics: list[dict] = []
    for i in range(n_eval):
        obs, info = env.reset(seed=seed_offset + i)
        done = False
        while not done:
            action, _, _ = model.get_action(obs, deterministic=True)
            obs, _, terminated, truncated, info = env.step(action.item())
            done = terminated or truncated

        link_load = info.get("link_load", {})
        capacity = info.get("capacity", env._capacity)
        n_total_edges = info.get("n_total_edges", env._E)
        final_mlu = info.get("final_mlu", info["mlu"])
        episode_metrics.append(
            compute_episode_metrics(link_load, capacity, n_total_edges, final_mlu)
        )

    result = aggregate_metrics(episode_metrics)
    mlus = [m["mlu"] for m in episode_metrics]
    result["mean"] = result["mlu_mean"]
    result["std"] = result["mlu_std"]
    result["mlus"] = mlus
    print(
        f"[MLP seed={seed}] Eval: "
        f"MLU={result['mlu_mean']:.4f}+/-{result['mlu_std']:.4f}, "
        f"CV={result['cv_mean']:.4f}, "
        f"Overflow={result['overflow_ratio_mean']:.4f}"
    )
    return result


if __name__ == "__main__":
    config = SimConfig()
    result = run_mlp(config, n_eval=50, n_episodes=800)
    print(f"\nMLP Baseline: MLU = {result['mean']:.4f} +/- {result['std']:.4f}")
