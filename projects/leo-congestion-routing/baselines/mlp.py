#!/usr/bin/env python3
"""MLP ablation baseline: K-path discrete selection with local features only.

Uses mlp_feat (src/dst node features + 1-hop loads + path lengths) instead of
GNN message passing. Same Categorical policy over K paths as GNN model.
Trained with self-contained PPO loop (matching MVE MLPActorCritic).
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


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------


class MLPActorCritic(nn.Module):
    """MLP actor-critic: local features only, no message passing.

    Uses mlp_feat from env obs: src_feat(6) + dst_feat(6) + src_nbr(4) +
    dst_nbr(4) + demand(1) + path_lens(K) = 21 + K dimensions.
    """

    def __init__(self, mlp_feat_dim: int, k_paths: int = 4, hidden: int = 128) -> None:
        super().__init__()
        self.K = k_paths
        self.backbone = nn.Sequential(
            nn.Linear(mlp_feat_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, hidden),
            nn.ReLU(),
        )
        self.actor = nn.Linear(hidden, k_paths)
        self.critic = nn.Linear(hidden, 1)

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
# PPO training (minimal inline version)
# ---------------------------------------------------------------------------


def _compute_gae(rewards, values, dones, gamma=0.99, lam=0.95):
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


def _train_mlp(env, model, n_episodes=300, lr=3e-4, seed=0):
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    rng = np.random.default_rng(seed)
    episode_mlus: list[float] = []

    for ep in range(n_episodes):
        obs_list, actions, rewards, values, logprobs, dones = [], [], [], [], [], []
        obs, info = env.reset(seed=int(rng.integers(0, 2**31)))
        done = False
        last_info = info

        while not done:
            action, log_prob, value = model.get_action(obs)
            obs, reward, terminated, truncated, info = env.step(action.item())
            done = terminated or truncated
            obs_list.append(obs)
            actions.append(action.item())
            rewards.append(reward)
            values.append(value.item())
            logprobs.append(log_prob.item())
            dones.append(done)
            last_info = info

        advantages, returns = _compute_gae(rewards, values, dones)
        actions_t = torch.tensor(actions, dtype=torch.long)
        old_lp = torch.tensor(logprobs, dtype=torch.float32)
        adv_t = torch.tensor(advantages, dtype=torch.float32)
        ret_t = torch.tensor(returns, dtype=torch.float32)

        for _ in range(4):
            new_lp, vals, ent = model.evaluate_actions(obs_list, actions_t)
            ratio = (new_lp - old_lp).exp()
            surr1 = ratio * adv_t
            surr2 = torch.clamp(ratio, 0.8, 1.2) * adv_t
            loss = -torch.min(surr1, surr2).mean() + 0.5 * F.mse_loss(vals, ret_t) - 0.01 * ent.mean()
            optimizer.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

        episode_mlus.append(last_info.get("final_mlu", last_info["mlu"]))
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
    """Train MLP baseline and evaluate."""
    config = env_config or SimConfig()
    env = RoutingEnv(config, seed=seed)

    # Compute mlp_feat dimension from a sample obs
    sample_obs, _ = env.reset(seed=0)
    mlp_feat_dim = sample_obs["mlp_feat"].shape[0]

    model = MLPActorCritic(mlp_feat_dim=mlp_feat_dim, k_paths=config.k_paths)

    print(f"[MLP seed={seed}] Training for {n_episodes} episodes...")
    _train_mlp(env, model, n_episodes=n_episodes, seed=seed)

    # Evaluate with greedy policy
    mlus: list[float] = []
    for i in range(n_eval):
        obs, info = env.reset(seed=seed_offset + i)
        done = False
        while not done:
            action, _, _ = model.get_action(obs, deterministic=True)
            obs, _, terminated, truncated, info = env.step(action.item())
            done = terminated or truncated
        mlus.append(info.get("final_mlu", info["mlu"]))

    result = {"mean": float(np.mean(mlus)), "std": float(np.std(mlus))}
    print(f"[MLP seed={seed}] Eval: MLU = {result['mean']:.4f} +/- {result['std']:.4f}")
    return result


if __name__ == "__main__":
    config = SimConfig()
    result = run_mlp(config, n_eval=50, n_episodes=300)
    print(f"\nMLP Baseline: MLU = {result['mean']:.4f} +/- {result['std']:.4f}")
