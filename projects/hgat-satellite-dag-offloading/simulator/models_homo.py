"""Homogeneous GNN encoders (GraphSAGE / GCN) with bilinear policy heads.

Converts HeteroData → flat homogeneous graph via per-type projection,
then applies standard message-passing GNN layers. Bilinear policy for fair
comparison with HGAT.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import Data, HeteroData
from torch_geometric.nn import GCNConv, SAGEConv

from config import SimConfig
from model_gnn import BaseActorCritic

_IN_DIMS = {"task": 8, "iotd": 4, "uav": 5, "leo": 5, "cs": 2}
_NODE_TYPES = ["task", "iotd", "uav", "leo", "cs"]
_COMPUTE_TYPES = ["iotd", "uav", "leo", "cs"]
_HETERO_EDGE_TYPES = [
    ("task", "dep", "task"),
    ("task", "to_iotd", "iotd"),
    ("task", "to_uav", "uav"),
    ("task", "to_leo", "leo"),
    ("task", "to_cs", "cs"),
]


def _node_offsets(data: HeteroData) -> dict[str, int]:
    offsets, offset = {}, 0
    for ntype in _NODE_TYPES:
        offsets[ntype] = offset
        x = data[ntype].x
        offset += x.size(0) if x is not None else 0
    return offsets


def hetero_to_homo(data: HeteroData, proj_layers: dict[str, nn.Linear]) -> Data:
    """Convert HeteroData to homogeneous PyG Data via per-type projection."""
    offsets = _node_offsets(data)
    x_parts = [proj_layers[ntype](data[ntype].x) for ntype in _NODE_TYPES]
    x = torch.cat(x_parts, dim=0)

    edge_rows = []
    for src_type, rel_type, dst_type in _HETERO_EDGE_TYPES:
        ei = data.edge_index_dict.get((src_type, rel_type, dst_type))
        if ei is None or ei.numel() == 0:
            continue
        edge_rows.append(torch.stack([ei[0] + offsets[src_type], ei[1] + offsets[dst_type]]))

    edge_index = torch.cat(edge_rows, dim=1) if edge_rows else torch.empty(2, 0, dtype=torch.long)
    return Data(x=x, edge_index=edge_index)


def _batch_hetero_to_homo(obs_list: list[HeteroData], proj_layers: dict[str, nn.Linear]) -> Data:
    """Batch-convert list of HeteroData into disconnected-graph Data."""
    xs, eis, batch_vec, ptr = [], [], [], 0
    for i, o in enumerate(obs_list):
        d = hetero_to_homo(o, proj_layers)
        xs.append(d.x)
        if d.edge_index.numel() > 0:
            eis.append(d.edge_index + ptr)
        batch_vec.append(torch.full((d.x.size(0),), i, dtype=torch.long, device=d.x.device))
        ptr += d.x.size(0)
    x = torch.cat(xs, dim=0)
    edge_index = torch.cat(eis, dim=1) if eis else torch.empty(2, 0, dtype=torch.long, device=x.device)
    return Data(x=x, edge_index=edge_index, batch=torch.cat(batch_vec))


class _HomoActorCritic(BaseActorCritic):
    _conv_cls = None

    def __init__(self, config: SimConfig, n_actions: int, n_gnn_layers: int = 2):
        hidden = config.hgat_hidden
        assert n_actions == config.total_tasks * config.n_nodes
        super().__init__(hidden, n_actions)

        self._n_tasks = config.total_tasks
        self._n_nodes = config.n_nodes
        self._node_type_sizes = {
            "task": config.total_tasks,
            "iotd": config.n_iotd,
            "uav": config.n_uav,
            "leo": config.n_leo,
            "cs": 1,
        }

        self.proj = nn.ModuleDict({ntype: nn.Linear(_IN_DIMS[ntype], hidden) for ntype in _NODE_TYPES})
        self.convs = nn.ModuleList([self._conv_cls(hidden, hidden) for _ in range(n_gnn_layers)])

        # Learnable type bias before GNN — gives message passing explicit type signal
        self.type_bias = nn.ParameterDict({
            ntype: nn.Parameter(torch.zeros(hidden)) for ntype in _NODE_TYPES
        })

        # Per-type output projection to recover type info after homo message passing
        self.type_proj = nn.ModuleDict({ntype: nn.Linear(hidden, hidden) for ntype in _NODE_TYPES})

        # Bilinear policy
        self.task_proj = nn.Linear(hidden, hidden)
        self.node_proj = nn.Linear(hidden, hidden)

        # Value head
        self.value_head = nn.Sequential(nn.Linear(hidden, hidden), nn.ReLU(), nn.Linear(hidden, 1))

    def _encode_single(self, obs: HeteroData) -> torch.Tensor:
        device = next(self.parameters()).device
        obs = obs.to(device)
        offsets, offset = {}, 0
        x_parts = []
        for ntype in _NODE_TYPES:
            projected = self.proj[ntype](obs[ntype].x) + self.type_bias[ntype]
            x_parts.append(projected)
            offsets[ntype] = offset
            offset += projected.size(0)
        x = torch.cat(x_parts, dim=0)

        edge_rows = []
        for src_type, rel_type, dst_type in _HETERO_EDGE_TYPES:
            ei = obs.edge_index_dict.get((src_type, rel_type, dst_type))
            if ei is None or ei.numel() == 0:
                continue
            edge_rows.append(torch.stack([ei[0] + offsets[src_type], ei[1] + offsets[dst_type]]))
        edge_index = torch.cat(edge_rows, dim=1) if edge_rows else torch.empty(2, 0, dtype=torch.long, device=device)

        for conv in self.convs:
            x = F.relu(conv(x, edge_index))
        return x

    def _encode_batch(self, obs_list: list[HeteroData]) -> torch.Tensor:
        device = next(self.parameters()).device
        xs, eis, batch_vec, ptr = [], [], [], 0
        for i, obs in enumerate(obs_list):
            obs = obs.to(device)
            offsets, off = {}, 0
            x_parts = []
            for ntype in _NODE_TYPES:
                projected = self.proj[ntype](obs[ntype].x) + self.type_bias[ntype]
                x_parts.append(projected)
                offsets[ntype] = off
                off += projected.size(0)
            x = torch.cat(x_parts, dim=0)
            xs.append(x)
            edge_rows = []
            for src_type, rel_type, dst_type in _HETERO_EDGE_TYPES:
                ei = obs.edge_index_dict.get((src_type, rel_type, dst_type))
                if ei is None or ei.numel() == 0:
                    continue
                edge_rows.append(torch.stack([ei[0] + offsets[src_type], ei[1] + offsets[dst_type]]))
            if edge_rows:
                eis.append(torch.cat(edge_rows, dim=1) + ptr)
            batch_vec.append(torch.full((x.size(0),), i, dtype=torch.long, device=device))
            ptr += x.size(0)
        x = torch.cat(xs, dim=0)
        edge_index = torch.cat(eis, dim=1) if eis else torch.empty(2, 0, dtype=torch.long, device=device)
        for conv in self.convs:
            x = F.relu(conv(x, edge_index))
        batch = torch.cat(batch_vec)
        out = torch.zeros(batch.max().item() + 1, self.hidden_dim, device=x.device)
        count = torch.zeros(batch.max().item() + 1, 1, device=x.device)
        out.scatter_add_(0, batch.unsqueeze(1).expand_as(x), x)
        count.scatter_add_(0, batch.unsqueeze(1), torch.ones_like(x[:, :1]))
        return out / count.clamp(min=1)

    def _split_homo_embs_single(self, homo_embs: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """Split flat homo embeddings into task_embs and compute_node_embs."""
        sizes = [self._node_type_sizes[t] for t in _NODE_TYPES]
        splits = torch.split(homo_embs, sizes)
        task_embs = splits[0]
        # compute nodes: iotd + uav + leo + cs
        node_embs = torch.cat(splits[1:], dim=0)
        return task_embs, node_embs

    def _split_homo_embs_batch(self, homo_embs: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """Split batched homo embeddings. homo_embs: [B, hidden]. Not applicable — need per-node."""
        raise NotImplementedError("Batch bilinear requires per-node splits")

    def forward(self, obs: HeteroData):
        homo_embs = self._encode_single(obs)
        # Apply per-type projection to recover type info after homo message passing
        sizes = [self._node_type_sizes[t] for t in _NODE_TYPES]
        splits = torch.split(homo_embs, sizes)
        typed_splits = [self.type_proj[t](s) for t, s in zip(_NODE_TYPES, splits)]
        task_embs = typed_splits[0]
        node_embs = torch.cat(typed_splits[1:], dim=0)

        # Bilinear policy
        logits = (self.task_proj(task_embs) @ self.node_proj(node_embs).T).flatten()

        # Value: mean pool
        global_emb = homo_embs.mean(dim=0)
        value = self.value_head(global_emb).squeeze(-1)

        return logits, value

    def evaluate_actions(self, obs_list, actions, action_masks):
        embs = self._encode_batch(obs_list)
        # For batch, we need per-node embs per graph — use single-obs forward
        log_probs, values, entropies = [], [], []
        from model_gnn import apply_mask
        from torch.distributions import Categorical
        for i, obs in enumerate(obs_list):
            logits, value = self.forward(obs)
            logits = apply_mask(logits, action_masks[i])
            dist = Categorical(logits=logits)
            log_probs.append(dist.log_prob(actions[i]))
            values.append(value.squeeze())
            entropies.append(dist.entropy())
        return torch.stack(log_probs), torch.stack(values), torch.stack(entropies)


class GraphSAGEActorCritic(_HomoActorCritic):
    _conv_cls = SAGEConv

    def __init__(self, config: SimConfig, n_actions: int, n_gnn_layers: int = 2):
        super().__init__(config, n_actions, n_gnn_layers)


class GCNActorCritic(_HomoActorCritic):
    _conv_cls = GCNConv

    def __init__(self, config: SimConfig, n_actions: int, n_gnn_layers: int = 2):
        super().__init__(config, n_actions, n_gnn_layers)


class MLPActorCritic(BaseActorCritic):
    """No-GNN baseline: project + bilinear scoring."""

    def __init__(self, config: SimConfig, n_actions: int):
        hidden = config.hgat_hidden
        assert n_actions == config.total_tasks * config.n_nodes
        super().__init__(hidden, n_actions)

        self._n_tasks = config.total_tasks
        self._n_nodes = config.n_nodes
        self._node_type_sizes = {
            "task": config.total_tasks,
            "iotd": config.n_iotd,
            "uav": config.n_uav,
            "leo": config.n_leo,
            "cs": 1,
        }

        self.proj = nn.ModuleDict({ntype: nn.Linear(_IN_DIMS[ntype], hidden) for ntype in _NODE_TYPES})
        self.trunk = nn.Sequential(nn.Linear(hidden, hidden), nn.ReLU(),
                                   nn.Linear(hidden, hidden), nn.ReLU())
        # Learnable type bias
        self.type_bias = nn.ParameterDict({
            ntype: nn.Parameter(torch.zeros(hidden)) for ntype in _NODE_TYPES
        })
        # Per-type output projection
        self.type_proj = nn.ModuleDict({ntype: nn.Linear(hidden, hidden) for ntype in _NODE_TYPES})
        self.task_proj = nn.Linear(hidden, hidden)
        self.node_proj = nn.Linear(hidden, hidden)
        self.value_head = nn.Sequential(nn.Linear(hidden, hidden), nn.ReLU(), nn.Linear(hidden, 1))

    def _encode_single(self, obs: HeteroData) -> torch.Tensor:
        device = next(self.parameters()).device
        parts = [self.trunk(self.proj[ntype](obs[ntype].x.to(device)) + self.type_bias[ntype])
                 for ntype in _NODE_TYPES]
        return torch.cat(parts, dim=0)

    def forward(self, obs: HeteroData):
        embs = self._encode_single(obs)
        # Per-type projection to recover type info
        sizes = [self._node_type_sizes[t] for t in _NODE_TYPES]
        splits = torch.split(embs, sizes)
        typed_splits = [self.type_proj[t](s) for t, s in zip(_NODE_TYPES, splits)]
        task_embs, node_embs = typed_splits[0], torch.cat(typed_splits[1:], dim=0)

        logits = (self.task_proj(task_embs) @ self.node_proj(node_embs).T).flatten()
        global_emb = embs.mean(dim=0)
        value = self.value_head(global_emb).squeeze(-1)
        return logits, value
