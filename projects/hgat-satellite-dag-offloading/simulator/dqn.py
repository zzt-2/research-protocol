"""DQN agent with MLP Q-network for satellite DAG task offloading.

Uses the same per-node-type projection + mean-pool architecture as PPO-MLP
for fair comparison. Only the RL algorithm differs (value-based vs policy-based).
"""

import random
from collections import deque

import numpy as np
import torch
import torch.nn as nn
from torch_geometric.data import HeteroData

from config import HGAT_HIDDEN

_IN_DIMS = {"task": 8, "iotd": 4, "uav": 5, "leo": 5, "cs": 2}
_NODE_TYPES = ["task", "iotd", "uav", "leo", "cs"]


class ReplayBuffer:
    def __init__(self, capacity: int = 50000):
        self.buf = deque(maxlen=capacity)

    def push(self, obs, action, reward, next_obs, done, mask, next_mask):
        self.buf.append((obs, action, reward, next_obs, done, mask, next_mask))

    def sample(self, batch_size: int):
        batch = random.sample(self.buf, batch_size)
        obs, actions, rewards, next_obs, dones, masks, next_masks = zip(*batch)
        return obs, actions, rewards, next_obs, dones, masks, next_masks

    def __len__(self):
        return len(self.buf)


class QNetwork(nn.Module):
    """MLP Q-network: proj → mean-pool → trunk → Q-values per action."""

    def __init__(self, hidden_dim: int = HGAT_HIDDEN, n_actions: int = 280):
        super().__init__()
        self.hidden_dim = hidden_dim

        self.proj = nn.ModuleDict({
            ntype: nn.Linear(_IN_DIMS[ntype], hidden_dim)
            for ntype in _NODE_TYPES
        })

        self.trunk = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
        )

        self.q_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, n_actions),
        )

    def _encode(self, obs: HeteroData) -> torch.Tensor:
        device = next(self.parameters()).device
        parts = [self.proj[ntype](obs[ntype].x.to(device)) for ntype in _NODE_TYPES]
        x = torch.cat(parts, dim=0).mean(dim=0)
        return self.trunk(x)

    def _encode_batch(self, obs_list: list[HeteroData]) -> torch.Tensor:
        embs = [self._encode(o) for o in obs_list]
        return torch.stack(embs)

    def forward(self, obs: HeteroData) -> torch.Tensor:
        return self.q_head(self._encode(obs))

    def forward_batch(self, obs_list: list[HeteroData]) -> torch.Tensor:
        """Return Q-values (B, n_actions) for a batch of observations."""
        return self.q_head(self._encode_batch(obs_list))


class DQNAgent:
    def __init__(
        self,
        n_actions: int = 280,
        hidden_dim: int = HGAT_HIDDEN,
        lr: float = 1e-3,
        gamma: float = 0.99,
        batch_size: int = 128,
        buffer_capacity: int = 50000,
        target_tau: float = 0.005,
        epsilon_start: float = 1.0,
        epsilon_end: float = 0.05,
        epsilon_decay: float = 0.997,
        max_grad_norm: float = 1.0,
        device: str = "cpu",
    ):
        self.n_actions = n_actions
        self.gamma = gamma
        self.batch_size = batch_size
        self.target_tau = target_tau
        self.epsilon = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.max_grad_norm = max_grad_norm
        self.device = device

        self.q_net = QNetwork(hidden_dim, n_actions).to(device)
        self.target_net = QNetwork(hidden_dim, n_actions).to(device)
        self.target_net.load_state_dict(self.q_net.state_dict())
        self.target_net.eval()

        self.optimizer = torch.optim.Adam(self.q_net.parameters(), lr=lr)
        self.buffer = ReplayBuffer(buffer_capacity)

        # Running reward stats for TD target normalization
        self._reward_mean = 0.0
        self._reward_var = 1.0
        self._reward_count = 1e-4

    def select_action(self, obs: HeteroData, action_mask: np.ndarray) -> int:
        if random.random() < self.epsilon:
            valid = np.where(action_mask)[0]
            return int(random.choice(valid))
        with torch.no_grad():
            q = self.q_net(obs)
            mask = torch.as_tensor(action_mask, dtype=torch.bool, device=q.device)
            q = q.masked_fill(~mask, -1e8)
            return int(q.argmax().item())

    def store(self, obs, action, reward, next_obs, done, mask, next_mask):
        # Update running reward stats
        delta = reward - self._reward_mean
        self._reward_count += 1
        self._reward_mean += delta / self._reward_count
        self._reward_var += delta * (reward - self._reward_mean)
        self.buffer.push(obs, action, reward, next_obs, done, mask, next_mask)

    def update(self) -> dict | None:
        if len(self.buffer) < self.batch_size:
            return None

        obs, actions, rewards, next_obs, dones, masks, next_masks = \
            self.buffer.sample(self.batch_size)

        self.q_net.train()

        actions_t = torch.tensor(actions, dtype=torch.long, device=self.device)
        rewards_t = torch.tensor(rewards, dtype=torch.float32, device=self.device)
        dones_t = torch.tensor(dones, dtype=torch.float32, device=self.device)

        # Normalize rewards using running stats
        r_std = max(np.sqrt(self._reward_var / self._reward_count), 1.0)
        rewards_norm = rewards_t / r_std

        # Current Q values (batched)
        q_all = self.q_net.forward_batch(obs)  # (B, n_actions)
        q_values = q_all.gather(1, actions_t.unsqueeze(1)).squeeze(1)  # (B,)

        # Target Q values (batched)
        with torch.no_grad():
            next_q_all = self.target_net.forward_batch(next_obs)  # (B, n_actions)
            for i, nm in enumerate(next_masks):
                nm_t = torch.as_tensor(nm, dtype=torch.bool, device=self.device)
                next_q_all[i] = next_q_all[i].masked_fill(~nm_t, -1e8)
            next_q_max = next_q_all.max(dim=1).values  # (B,)
            targets = rewards_norm + self.gamma * next_q_max * (1.0 - dones_t)

        # Huber loss (robust to large TD errors)
        loss = nn.functional.smooth_l1_loss(q_values, targets)

        self.optimizer.zero_grad()
        loss.backward()
        nn.utils.clip_grad_norm_(self.q_net.parameters(), self.max_grad_norm)
        self.optimizer.step()

        # Soft update target network
        for tp, sp in zip(self.target_net.parameters(), self.q_net.parameters()):
            tp.data.mul_(1.0 - self.target_tau)
            tp.data.add_(self.target_tau * sp.data)

        # Epsilon decay
        self.epsilon = max(self.epsilon_end, self.epsilon * self.epsilon_decay)

        return {"loss": loss.item(), "epsilon": self.epsilon}

    def save(self, path: str):
        torch.save({
            "q_net": self.q_net.state_dict(),
            "target_net": self.target_net.state_dict(),
            "optimizer": self.optimizer.state_dict(),
            "epsilon": self.epsilon,
        }, path)

    def load(self, path: str):
        ckpt = torch.load(path, map_location=self.device, weights_only=False)
        self.q_net.load_state_dict(ckpt["q_net"])
        self.target_net.load_state_dict(ckpt["target_net"])
        self.optimizer.load_state_dict(ckpt["optimizer"])
        self.epsilon = ckpt["epsilon"]
