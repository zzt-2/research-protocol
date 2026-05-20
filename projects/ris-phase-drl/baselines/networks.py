"""Shared neural network components and replay buffer."""

import numpy as np
import torch
import torch.nn as nn


class ReplayBuffer:
    """Standard off-policy replay buffer with numpy arrays."""

    def __init__(self, obs_dim: int, act_dim: int, max_size: int = 100000):
        self.obs_buf = np.zeros((max_size, obs_dim), dtype=np.float32)
        self.obs2_buf = np.zeros((max_size, obs_dim), dtype=np.float32)
        self.act_buf = np.zeros((max_size, act_dim), dtype=np.float32)
        self.rew_buf = np.zeros(max_size, dtype=np.float32)
        self.done_buf = np.zeros(max_size, dtype=np.float32)
        self.ptr = 0
        self.size = 0
        self.max_size = max_size

    def store(self, obs, act, rew, next_obs, done):
        self.obs_buf[self.ptr] = obs
        self.obs2_buf[self.ptr] = next_obs
        self.act_buf[self.ptr] = act
        self.rew_buf[self.ptr] = rew
        self.done_buf[self.ptr] = done
        self.ptr = (self.ptr + 1) % self.max_size
        self.size = min(self.size + 1, self.max_size)

    def sample_batch(self, batch_size: int = 256) -> dict[str, np.ndarray]:
        idxs = np.random.randint(0, self.size, size=batch_size)
        return dict(
            obs=self.obs_buf[idxs],
            obs2=self.obs2_buf[idxs],
            act=self.act_buf[idxs],
            rew=self.rew_buf[idxs],
            done=self.done_buf[idxs],
        )


class Actor(nn.Module):
    """MLP Actor outputting tanh-squashed actions in [-1, 1]."""

    def __init__(self, obs_dim: int, act_dim: int, hidden: tuple = (400, 300)):
        super().__init__()
        layers = []
        prev = obs_dim
        for h in hidden:
            layers += [nn.Linear(prev, h), nn.ReLU()]
            prev = h
        layers.append(nn.Linear(prev, act_dim))
        layers.append(nn.Tanh())
        self.net = nn.Sequential(*layers)

    def forward(self, obs: torch.Tensor) -> torch.Tensor:
        return self.net(obs)


class Critic(nn.Module):
    """Twin Q-networks for TD3/SAC. DDPG uses only q1."""

    def __init__(self, obs_dim: int, act_dim: int, hidden: tuple = (400, 300)):
        super().__init__()
        # Q1
        layers1 = []
        prev = obs_dim + act_dim
        for h in hidden:
            layers1 += [nn.Linear(prev, h), nn.ReLU()]
            prev = h
        layers1.append(nn.Linear(prev, 1))
        self.q1 = nn.Sequential(*layers1)
        # Q2 (same structure)
        layers2 = []
        prev = obs_dim + act_dim
        for h in hidden:
            layers2 += [nn.Linear(prev, h), nn.ReLU()]
            prev = h
        layers2.append(nn.Linear(prev, 1))
        self.q2 = nn.Sequential(*layers2)

    def forward(self, obs: torch.Tensor, act: torch.Tensor):
        x = torch.cat([obs, act], dim=-1)
        return self.q1(x), self.q2(x)

    def q1_forward(self, obs: torch.Tensor, act: torch.Tensor) -> torch.Tensor:
        x = torch.cat([obs, act], dim=-1)
        return self.q1(x)
