"""Homogeneous GNN encoders (GraphSAGE / GCN) with Actor-Critic heads.

Converts the heterogeneous HeteroData observation to a flat homogeneous graph,
then applies standard message-passing GNN layers.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Categorical
from torch_geometric.data import Data, HeteroData
from torch_geometric.nn import GCNConv, SAGEConv

from config import HGAT_HIDDEN, N_TASKS, N_UAV, N_LEO

# Node-type feature dimensions (must match environment.py _build_graph)
_IN_DIMS = {"task": 8, "iotd": 4, "uav": 5, "leo": 5, "cs": 2}

# Canonical node order in the homogeneous graph
_NODE_TYPES = ["task", "iotd", "uav", "leo", "cs"]

# Edge types present in the environment's _build_graph output
_HETERO_EDGE_TYPES = [
    ("task", "dep", "task"),
    ("task", "to_iotd", "iotd"),
    ("task", "to_uav", "uav"),
    ("task", "to_leo", "leo"),
    ("task", "to_cs", "cs"),
]


def _node_offsets(data: HeteroData) -> dict[str, int]:
    """Compute global index offset for each node type."""
    offsets = {}
    offset = 0
    for ntype in _NODE_TYPES:
        offsets[ntype] = offset
        x = data[ntype].x
        offset += x.size(0) if x is not None else 0
    return offsets


def hetero_to_homo(data: HeteroData, proj_layers: dict[str, nn.Linear]) -> Data:
    """Convert HeteroData to homogeneous PyG Data.

    Each node type's features are projected to a common dimension via the
    corresponding linear layer in *proj_layers*.  Nodes are concatenated in
    canonical order: task, iotd, uav, leo, cs.  All heterogeneous edges are
    remapped to a single edge_index.

    Args:
        data: Heterogeneous observation from the environment.
        proj_layers: Mapping node-type name -> Linear(in_dim, hidden_dim).

    Returns:
        Homogeneous Data with x (total_nodes x hidden_dim) and edge_index.
    """
    offsets = _node_offsets(data)

    # Project and concatenate node features
    x_parts = []
    for ntype in _NODE_TYPES:
        feat = data[ntype].x  # (N_i, in_dim_i)
        x_parts.append(proj_layers[ntype](feat))
    x = torch.cat(x_parts, dim=0)  # (34, hidden_dim)

    # Remap edges
    edge_rows = []
    for src_type, rel_type, dst_type in _HETERO_EDGE_TYPES:
        key = (src_type, rel_type, dst_type)
        ei = data.edge_index_dict.get(key)
        if ei is None or ei.numel() == 0:
            continue
        src_offset = offsets[src_type]
        dst_offset = offsets[dst_type]
        remapped = torch.stack([
            ei[0] + src_offset,
            ei[1] + dst_offset,
        ])
        edge_rows.append(remapped)

    if edge_rows:
        edge_index = torch.cat(edge_rows, dim=1)
    else:
        # 不会出现，但防御性处理
        edge_index = torch.empty(2, 0, dtype=torch.long, device=x.device)

    return Data(x=x, edge_index=edge_index)


def _batch_hetero_to_homo(
    obs_list: list[HeteroData],
    proj_layers: dict[str, nn.Linear],
) -> Data:
    """Batch-convert a list of HeteroData into a single disconnected-graph Data.

    Each observation is converted independently then merged into one large
    graph where observations form disconnected components.  A *batch* vector
    is added so that global pooling can be done per-observation.
    """
    data_list = [hetero_to_homo(o, proj_layers) for o in obs_list]
    # 手动拼 batch，避免 to_data_list 反弹开销
    xs, eis, batch_vec = [], [], []
    ptr = 0
    for i, d in enumerate(data_list):
        xs.append(d.x)
        if d.edge_index.numel() > 0:
            eis.append(d.edge_index + ptr)
        batch_vec.append(torch.full((d.x.size(0),), i, dtype=torch.long, device=d.x.device))
        ptr += d.x.size(0)
    x = torch.cat(xs, dim=0)
    edge_index = torch.cat(eis, dim=1) if eis else torch.empty(2, 0, dtype=torch.long, device=x.device)
    batch = torch.cat(batch_vec, dim=0)
    return Data(x=x, edge_index=edge_index, batch=batch)


class _HomoActorCritic(nn.Module):
    """Shared backbone for homogeneous GNN actor-critics.

    Subclasses supply *conv_fn* to choose the message-passing layer
    (SAGEConv / GCNConv).
    """

    # Subclass sets this to SAGEConv or GCNConv
    _conv_cls = None

    def __init__(self, hidden_dim: int = HGAT_HIDDEN, n_actions: int = 280,
                 n_gnn_layers: int = 2):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.n_actions = n_actions

        # Per-node-type projection: raw features -> hidden_dim
        self.proj = nn.ModuleDict({
            ntype: nn.Linear(_IN_DIMS[ntype], hidden_dim)
            for ntype in _NODE_TYPES
        })

        # GNN layers
        self.convs = nn.ModuleList()
        for _ in range(n_gnn_layers):
            self.convs.append(self._conv_cls(hidden_dim, hidden_dim))

        # Policy head
        self.policy = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, n_actions),
        )

        # Value head
        self.value = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _proj_layers(self) -> dict[str, nn.Linear]:
        return {ntype: self.proj[ntype] for ntype in _NODE_TYPES}

    def _encode_single(self, obs: HeteroData) -> torch.Tensor:
        """Run GNN on one observation, return graph embedding (hidden_dim,)."""
        device = next(self.parameters()).device
        homo = hetero_to_homo(obs.to(device), self._proj_layers())
        x, ei = homo.x, homo.edge_index
        for conv in self.convs:
            x = conv(x, ei)
            x = F.relu(x)
        return x.mean(dim=0)

    def _encode_batch(self, obs_list: list[HeteroData]) -> torch.Tensor:
        """Run GNN on a batch, return per-obs graph embeddings (B, hidden_dim)."""
        device = next(self.parameters()).device
        obs_on_device = [o.to(device) for o in obs_list]
        homo = _batch_hetero_to_homo(obs_on_device, self._proj_layers())
        x, ei = homo.x, homo.edge_index
        for conv in self.convs:
            x = conv(x, ei)
            x = F.relu(x)
        # Mean-pool per observation
        batch = homo.batch
        out = torch.zeros(batch.max().item() + 1, self.hidden_dim, device=x.device)
        count = torch.zeros(batch.max().item() + 1, 1, device=x.device)
        out.scatter_add_(0, batch.unsqueeze(1).expand_as(x), x)
        count.scatter_add_(0, batch.unsqueeze(1), torch.ones_like(x[:, :1]))
        out = out / count.clamp(min=1)
        return out

    # ------------------------------------------------------------------
    # Public API (matches BaseActorCritic contract)
    # ------------------------------------------------------------------

    def forward(self, obs: HeteroData):
        """Return (logits, value) for a single observation.

        Args:
            obs: HeteroData from the environment.

        Returns:
            logits: (n_actions,) unnormalized action preferences.
            value:  scalar state-value estimate.
        """
        emb = self._encode_single(obs)
        return self.policy(emb), self.value(emb).squeeze(-1)

    @torch.no_grad()
    def get_action(self, obs: HeteroData, action_mask: torch.Tensor):
        """Sample a single action, return action info for PPO buffer.

        Args:
            obs: HeteroData observation.
            action_mask: boolean tensor (n_actions,).

        Returns:
            action:     int
            log_prob:   float tensor (scalar)
            value:      float tensor (scalar)
            entropy:    float tensor (scalar)
        """
        logits, value = self.forward(obs)
        mask = torch.as_tensor(action_mask, dtype=torch.bool, device=logits.device)
        logits = logits.masked_fill(~mask, -1e8)
        dist = Categorical(logits=logits)
        action = dist.sample()
        return (
            action.item(),
            dist.log_prob(action),
            value,
            dist.entropy(),
        )

    def evaluate_actions(
        self,
        obs_list: list[HeteroData],
        actions: torch.Tensor,
        action_masks: torch.Tensor,
    ):
        """Evaluate log-prob, value, entropy for a batch of transitions.

        Used during PPO update.

        Args:
            obs_list:     list of HeteroData, length B.
            actions:      (B,) long tensor of taken actions.
            action_masks: (B, n_actions) boolean tensor.

        Returns:
            log_probs: (B,)
            values:    (B,)
            entropy:   (B,)
        """
        embs = self._encode_batch(obs_list)  # (B, hidden_dim)
        logits = self.policy(embs)            # (B, n_actions)
        values = self.value(embs).squeeze(-1) # (B,)

        logits = logits.masked_fill(~action_masks, -1e8)
        dist = Categorical(logits=logits)
        log_probs = dist.log_prob(actions)
        entropy = dist.entropy()

        return log_probs, values, entropy


class GraphSAGEActorCritic(_HomoActorCritic):
    """GraphSAGE encoder with PPO actor-critic heads."""
    _conv_cls = SAGEConv

    def __init__(self, hidden_dim: int = HGAT_HIDDEN, n_actions: int = 280,
                 n_gnn_layers: int = 2):
        super().__init__(hidden_dim=hidden_dim, n_actions=n_actions,
                         n_gnn_layers=n_gnn_layers)


class GCNActorCritic(_HomoActorCritic):
    """GCN encoder with PPO actor-critic heads."""
    _conv_cls = GCNConv

    def __init__(self, hidden_dim: int = HGAT_HIDDEN, n_actions: int = 280,
                 n_gnn_layers: int = 2):
        super().__init__(hidden_dim=hidden_dim, n_actions=n_actions,
                         n_gnn_layers=n_gnn_layers)


class MLPActorCritic(nn.Module):
    """No-GNN baseline: project + mean-pool + FC, same interface as GNN models.

    Keeps per-node-type projection layers (matching GNN models), but replaces
    message-passing with a 2-layer MLP over the pooled graph embedding.
    """

    def __init__(self, hidden_dim: int = HGAT_HIDDEN, n_actions: int = 280):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.n_actions = n_actions

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

        self.policy = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, n_actions),
        )

        self.value = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

    def _encode_single(self, obs: HeteroData) -> torch.Tensor:
        device = next(self.parameters()).device
        parts = [self.proj[ntype](obs[ntype].x.to(device)) for ntype in _NODE_TYPES]
        x = torch.cat(parts, dim=0).mean(dim=0)  # (hidden_dim,)
        return self.trunk(x)

    def _encode_batch(self, obs_list: list[HeteroData]) -> torch.Tensor:
        embs = [self._encode_single(o) for o in obs_list]
        return torch.stack(embs)  # (B, hidden_dim)

    def forward(self, obs: HeteroData):
        emb = self._encode_single(obs)
        return self.policy(emb), self.value(emb).squeeze(-1)

    @torch.no_grad()
    def get_action(self, obs: HeteroData, action_mask):
        logits, value = self.forward(obs)
        mask = torch.as_tensor(action_mask, dtype=torch.bool, device=logits.device)
        logits = logits.masked_fill(~mask, -1e8)
        dist = Categorical(logits=logits)
        action = dist.sample()
        return action.item(), dist.log_prob(action), value, dist.entropy()

    def evaluate_actions(self, obs_list: list[HeteroData], actions: torch.Tensor,
                         action_masks: torch.Tensor):
        embs = self._encode_batch(obs_list)
        logits = self.policy(embs)
        values = self.value(embs).squeeze(-1)
        logits = logits.masked_fill(~action_masks, -1e8)
        dist = Categorical(logits=logits)
        return dist.log_prob(actions), values, dist.entropy()
