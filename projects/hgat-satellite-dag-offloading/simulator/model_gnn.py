"""BaseActorCritic 抽象基类 — GNN actor-critic 接口模板。

子类只需实现 _encode(data) -> Tensor，forward / get_action / evaluate_actions 由基类处理。
设计要点:
  - encode (单样本) vs encode_batch (PPO 更新批处理) 分离
  - policy / value head 共享编码器
  - action masking 用 _MASK_VALUE 常量
  - get_action 加 @torch.no_grad()
"""

from abc import abstractmethod

import numpy as np
import torch
import torch.nn as nn
from torch import Tensor
from torch.distributions import Categorical
from torch_geometric.data import HeteroData

_MASK_VALUE: float = -1e8


def apply_mask(logits: Tensor, mask) -> Tensor:
    """将无效动作的 logit 置为大负数。"""
    mask_t = torch.as_tensor(mask, dtype=torch.bool, device=logits.device)
    return logits.masked_fill(~mask_t, _MASK_VALUE)


class BaseActorCritic(nn.Module):
    """GNN actor-critic 接口，适配 PPO 训练循环。

    子类必须实现 forward(obs) -> (logits, value)。
    get_action / evaluate_actions 提供默认实现。
    """

    def __init__(self, hidden_dim: int, n_actions: int) -> None:
        super().__init__()
        self.hidden_dim = hidden_dim
        self.n_actions = n_actions

    @abstractmethod
    def forward(self, obs: HeteroData) -> tuple[Tensor, Tensor]:
        """Return (action_logits [n_actions], value_scalar)."""
        ...

    @torch.no_grad()
    def get_action(self, obs: HeteroData, action_mask) -> tuple[int, float, float, float]:
        """Sample one action. Returns (action, log_prob, value, entropy)."""
        logits, value = self.forward(obs)
        logits = apply_mask(logits, action_mask)
        dist = Categorical(logits=logits)
        action = dist.sample()
        return (action.item(), dist.log_prob(action).item(),
                value.item(), dist.entropy().item())

    def evaluate_actions(self, obs_list: list, actions: Tensor,
                         action_masks: Tensor) -> tuple[Tensor, Tensor, Tensor]:
        """Re-evaluate actions under the current policy. Returns (log_probs, values, entropy)."""
        log_probs, values, entropies = [], [], []
        for i, obs in enumerate(obs_list):
            logits, value = self.forward(obs)
            logits = apply_mask(logits, action_masks[i])
            dist = Categorical(logits=logits)
            log_probs.append(dist.log_prob(actions[i]))
            values.append(value.squeeze())
            entropies.append(dist.entropy())
        return torch.stack(log_probs), torch.stack(values), torch.stack(entropies)

    def forward_batch(self, obs_list: list) -> Tensor:
        """Batch forward for DQN: (B, n_actions). Default:逐样本 forward."""
        q_batch = []
        for obs in obs_list:
            logits, _ = self.forward(obs)
            q_batch.append(logits)
        return torch.stack(q_batch)
