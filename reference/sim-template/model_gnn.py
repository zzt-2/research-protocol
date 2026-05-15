"""GNN Actor-Critic 模板 — PyG + PPO。

取自 projects/hgat-satellite-dag-offloading，提取核心设计：
  1. BaseActorCritic 抽象基类：forward / get_action / evaluate_actions 三件套
  2. GATEncoder 示例：GATConv + LayerNorm + 残差，支持 edge_dim
  3. 子类只需实现 _encode(data) -> Tensor，其余由基类处理

设计思想：
  - encode（单样本推理）vs encode_batch（PPO 更新批处理）分离
  - policy / value head 分离，共享编码器
  - action masking 用 _MASK_VALUE 常量，不修改分布参数
  - get_action 加 @torch.no_grad()，采样时不开计算图
"""

from abc import abstractmethod

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor
from torch.distributions import Categorical
from torch_geometric.data import Data
from torch_geometric.nn import GATConv, global_mean_pool

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

_MASK_VALUE: float = -1e8  # 无效动作的 logit 哨兵值


def _apply_mask(logits: Tensor, mask: Tensor) -> Tensor:
    """将无效动作的 logit 置为大负数，阻止被采样。"""
    return logits.masked_fill(~mask.to(dtype=torch.bool, device=logits.device), _MASK_VALUE)


# ===========================================================================
# 抽象基类 — 子类只需实现 _encode
# ===========================================================================

class BaseActorCritic(nn.Module):
    """GNN actor-critic 接口，适配 PPO 训练循环。

    子类必须实现 _encode(self, data) -> Tensor，返回图级嵌入 (hidden_dim,)。
    forward / get_action / evaluate_actions 的签名和返回类型固定不变。
    """

    def __init__(self, hidden_dim: int, n_actions: int) -> None:
        super().__init__()
        self.hidden_dim = hidden_dim
        self.n_actions = n_actions

        # --- CUSTOMIZE: policy / value head 结构可调整 ---
        self.policy_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, n_actions),
        )
        self.value_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

    # --- 子类必须实现 ---

    @abstractmethod
    def _encode(self, data: Data) -> Tensor:
        """编码观测为图级嵌入 (hidden_dim,)。"""
        raise NotImplementedError

    # --- 固定接口 ---

    def forward(self, data: Data) -> tuple[Tensor, Tensor]:
        """带梯度的前向传播，返回 (logits, value)。"""
        emb = self._encode(data)
        logits = self.policy_head(emb)
        value = self.value_head(emb).squeeze(-1)
        return logits, value

    @torch.no_grad()
    def get_action(
        self, data: Data, action_mask: Tensor, deterministic: bool = False,
    ) -> tuple[int, Tensor, Tensor]:
        """采样一个动作。@torch.no_grad() 避免采样时建计算图。

        Returns: (action, log_prob, value)
        """
        logits, value = self.forward(data)
        logits = _apply_mask(logits, action_mask)
        dist = Categorical(logits=logits)
        action = logits.argmax() if deterministic else dist.sample()
        return action.item(), dist.log_prob(action), value

    def evaluate_actions(
        self, data_list: list[Data], actions: Tensor, action_masks: Tensor,
    ) -> tuple[Tensor, Tensor, Tensor]:
        """PPO 更新时重新评估动作，返回 (log_probs, values, entropy)，各 shape (B,)。"""
        log_probs, values, entropies = [], [], []
        for i, data in enumerate(data_list):
            logits, value = self.forward(data)
            logits = _apply_mask(logits, action_masks[i])
            dist = Categorical(logits=logits)
            log_probs.append(dist.log_prob(actions[i]))
            values.append(value.squeeze())
            entropies.append(dist.entropy())
        return torch.stack(log_probs), torch.stack(values), torch.stack(entropies)

    def forward_batch(self, obs_list: list[Data]) -> Tensor:
        """批量前向传播，返回 (B, n_actions) Q 值矩阵（DQN 使用）。

        默认实现逐样本 forward 后 stack；若子类支持真正的 batch forward
        （如 PyG Batch），可重写此方法以提升效率。
        """
        q_batch: list[Tensor] = []
        for obs in obs_list:
            logits, _ = self.forward(obs)
            q_batch.append(logits)
        return torch.stack(q_batch)  # (B, n_actions)


# ===========================================================================
# GATEncoder — 同构图示例
# ===========================================================================

class GATEncoder(BaseActorCritic):
    """GAT 编码器 + PPO actor-critic 头。

    支持 PyG Data（同构图）。若需要 HeteroData，改用 HeteroConv 包装，
    并在 _encode 中按节点类型投影后送入异构卷积层 — 详见项目 models_hgat.py。

    Args:
        in_dim: 节点特征维度。
        hidden_dim: GNN 隐层维度。
        n_actions: 离散动作空间大小。
        n_layers: GATConv 层数。
        n_heads: 注意力头数。
        edge_dim: 边特征维度（None 表示不使用边特征）。
    """

    def __init__(
        self,
        in_dim: int = 16,
        hidden_dim: int = 64,
        n_actions: int = 10,
        n_layers: int = 2,
        n_heads: int = 4,
        edge_dim: int | None = None,
    ) -> None:
        super().__init__(hidden_dim, n_actions)
        assert hidden_dim % n_heads == 0, (
            f"hidden_dim ({hidden_dim}) 必须能被 n_heads ({n_heads}) 整除"
        )
        self.in_proj = nn.Linear(in_dim, hidden_dim)
        head_dim = hidden_dim // n_heads

        self.convs = nn.ModuleList()
        self.norms = nn.ModuleList()
        for _ in range(n_layers):
            self.convs.append(GATConv(
                (hidden_dim, hidden_dim), head_dim,
                heads=n_heads, edge_dim=edge_dim, add_self_loops=True,
            ))
            self.norms.append(nn.LayerNorm(hidden_dim))

    def _encode(self, data: Data) -> Tensor:
        """GAT 多层 + LayerNorm + 残差 → 全局均值池化 → 图嵌入。"""
        device = next(self.parameters()).device
        data = data.to(device)
        x: Tensor = self.in_proj(data.x)          # (N, hidden_dim)
        edge_index = data.edge_index
        edge_attr = getattr(data, "edge_attr", None)

        for conv, norm in zip(self.convs, self.norms):
            out = conv(x, edge_index, edge_attr=edge_attr)
            out = norm(out)
            x = F.relu(out) + x                    # 残差连接

        # --- CUSTOMIZE: 池化方式可改为 global_max_pool / attention pooling ---
        batch = getattr(data, "batch", None)
        if batch is None:
            # 单图：直接均值
            return x.mean(dim=0)
        return global_mean_pool(x, batch)          # (num_graphs, hidden_dim)
