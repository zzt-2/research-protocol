"""DDPG (Deep Deterministic Policy Gradient) agent."""

from __future__ import annotations

import copy
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from .networks import Actor, Critic


class DDPGAgent:
    """DDPG with single critic, OU-like Gaussian noise for exploration."""

    def __init__(
        self,
        obs_dim: int,
        act_dim: int,
        hidden: tuple = (400, 300),
        lr: float = 1e-3,
        tau: float = 1e-3,
        gamma: float = 0.99,
        device: str = "cuda",
    ):
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.act_dim = act_dim
        self.tau = tau
        self.gamma = gamma

        self.actor = Actor(obs_dim, act_dim, hidden).to(self.device)
        self.actor_target = copy.deepcopy(self.actor)
        self.actor_optimizer = torch.optim.Adam(self.actor.parameters(), lr=lr)

        self.critic = Critic(obs_dim, act_dim, hidden).to(self.device)
        self.critic_target = copy.deepcopy(self.critic)
        self.critic_optimizer = torch.optim.Adam(self.critic.parameters(), lr=lr)

        self.last_actor_loss = 0.0
        self.last_critic_loss = 0.0

    @torch.no_grad()
    def select_action(self, obs: np.ndarray) -> np.ndarray:
        obs_t = torch.FloatTensor(obs).unsqueeze(0).to(self.device)
        return self.actor(obs_t).cpu().numpy()[0]

    @torch.no_grad()
    def select_action_exploration(self, obs: np.ndarray, noise_std: float = 0.1) -> np.ndarray:
        action = self.select_action(obs)
        noise = np.random.normal(0, noise_std, size=self.act_dim)
        return np.clip(action + noise, -1.0, 1.0)

    def update(self, buffer, batch_size: int = 256):
        batch = buffer.sample_batch(batch_size)
        obs = torch.FloatTensor(batch["obs"]).to(self.device)
        obs2 = torch.FloatTensor(batch["obs2"]).to(self.device)
        act = torch.FloatTensor(batch["act"]).to(self.device)
        rew = torch.FloatTensor(batch["rew"]).unsqueeze(1).to(self.device)
        done = torch.FloatTensor(batch["done"]).unsqueeze(1).to(self.device)

        # --- Critic update ---
        with torch.no_grad():
            next_act = self.actor_target(obs2)
            q_target = rew + self.gamma * (1 - done) * self.critic_target.q1_forward(obs2, next_act)

        q1 = self.critic.q1_forward(obs, act)
        critic_loss = F.mse_loss(q1, q_target)
        self.last_critic_loss = critic_loss.item()

        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        nn.utils.clip_grad_norm_(self.critic.parameters(), 1.0)
        self.critic_optimizer.step()

        # --- Actor update ---
        actor_loss = -self.critic.q1_forward(obs, self.actor(obs)).mean()
        self.last_actor_loss = actor_loss.item()

        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        nn.utils.clip_grad_norm_(self.actor.parameters(), 1.0)
        self.actor_optimizer.step()

        # --- Soft update targets ---
        self._soft_update(self.critic, self.critic_target)
        self._soft_update(self.actor, self.actor_target)

    def _soft_update(self, source: nn.Module, target: nn.Module):
        for p, tp in zip(source.parameters(), target.parameters()):
            tp.data.copy_(self.tau * p.data + (1 - self.tau) * tp.data)

    def save(self, path: str):
        torch.save({
            "actor": self.actor.state_dict(),
            "actor_optimizer": self.actor_optimizer.state_dict(),
            "critic": self.critic.state_dict(),
            "critic_optimizer": self.critic_optimizer.state_dict(),
        }, path)

    def load(self, path: str):
        ckpt = torch.load(path, map_location=self.device, weights_only=True)
        self.actor.load_state_dict(ckpt["actor"])
        self.actor_optimizer.load_state_dict(ckpt["actor_optimizer"])
        self.critic.load_state_dict(ckpt["critic"])
        self.critic_optimizer.load_state_dict(ckpt["critic_optimizer"])
        for p, tp in zip(self.actor.parameters(), self.actor_target.parameters()):
            tp.data.copy_(p.data)
        for p, tp in zip(self.critic.parameters(), self.critic_target.parameters()):
            tp.data.copy_(p.data)
