"""HGAT (Heterogeneous Graph Attention) encoder for satellite DAG task offloading.

Per-type linear projections → HeteroConv(GATConv) + LayerNorm + ReLU → bilinear policy + mean-pool value。

Policy head: bilinear scoring — task_emb @ node_emb.T → [n_tasks × n_nodes] logits。
This preserves per-node information instead of losing it to mean-pool.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor
from torch_geometric.data import HeteroData
from torch_geometric.nn import GATConv, HeteroConv

from config import SimConfig
from model_gnn import BaseActorCritic, _MASK_VALUE

NODE_FEAT_DIMS = {"task": 8, "iotd": 4, "uav": 5, "leo": 5, "cs": 2}
NODE_TYPES = ["task", "iotd", "uav", "leo", "cs"]
COMPUTE_NODE_TYPES = ["iotd", "uav", "leo", "cs"]
EDGE_TYPES = [
    ("task", "dep", "task"),
    ("task", "to_iotd", "iotd"),
    ("task", "to_uav", "uav"),
    ("task", "to_leo", "leo"),
    ("task", "to_cs", "cs"),
]
_EMPTY_EDGE = torch.tensor([[], []], dtype=torch.long)


class HGATActorCritic(BaseActorCritic):
    """Heterogeneous GAT encoder + bilinear policy + PPO actor-critic heads."""

    def __init__(self, config: SimConfig, n_actions: int) -> None:
        super().__init__(config.hgat_hidden, n_actions)
        assert n_actions == config.total_tasks * config.n_nodes

        hidden = config.hgat_hidden
        heads = config.hgat_heads
        n_layers = config.hgat_layers
        head_dim = hidden // heads

        self.input_proj = nn.ModuleDict({
            ntype: nn.Linear(NODE_FEAT_DIMS[ntype], hidden) for ntype in NODE_TYPES
        })

        self.conv_layers = nn.ModuleList()
        self.norm_layers = nn.ModuleList()
        for _ in range(n_layers):
            conv_dict = {}
            for etype in EDGE_TYPES:
                src_type, _, dst_type = etype
                conv_dict[etype] = GATConv(
                    in_channels=(hidden, hidden), out_channels=head_dim,
                    heads=heads, add_self_loops=(src_type == dst_type),
                )
            self.conv_layers.append(HeteroConv(conv_dict, aggr="sum"))
            self.norm_layers.append(nn.ModuleDict({
                ntype: nn.LayerNorm(hidden) for ntype in NODE_TYPES
            }))

        # Bilinear policy: task_proj(task_embs) @ node_proj(node_embs).T
        self.task_proj = nn.Linear(hidden, hidden)
        self.node_proj = nn.Linear(hidden, hidden)

        # Value: mean pool + MLP
        self.value_head = nn.Sequential(
            nn.Linear(hidden, hidden), nn.ReLU(), nn.Linear(hidden, 1),
        )

    def _ensure_all_edge_types(self, edge_index_dict: dict, device: torch.device) -> dict:
        for etype in EDGE_TYPES:
            if etype not in edge_index_dict:
                edge_index_dict[etype] = _EMPTY_EDGE.to(device)
        return edge_index_dict

    def _encode_dict(self, obs: HeteroData) -> dict[str, Tensor]:
        """Run GNN and return per-type node embeddings."""
        device = next(self.parameters()).device
        obs = obs.to(device)
        x_dict = {ntype: self.input_proj[ntype](obs[ntype].x) for ntype in NODE_TYPES}

        edge_index_dict = {}
        for etype in EDGE_TYPES:
            if hasattr(obs[etype[0], etype[1], etype[2]], "edge_index"):
                edge_index_dict[etype] = obs[etype[0], etype[1], etype[2]].edge_index
        edge_index_dict = self._ensure_all_edge_types(edge_index_dict, device)

        for conv, norms in zip(self.conv_layers, self.norm_layers):
            out_dict = conv(x_dict, edge_index_dict)
            new_x_dict = {}
            for ntype in NODE_TYPES:
                if ntype in out_dict and out_dict[ntype].numel() > 0:
                    new_x_dict[ntype] = F.relu(norms[ntype](out_dict[ntype]))
                else:
                    new_x_dict[ntype] = x_dict[ntype]
            x_dict = new_x_dict

        return x_dict

    def forward(self, obs: HeteroData) -> tuple[Tensor, Tensor]:
        x_dict = self._encode_dict(obs)

        # Policy: bilinear scoring
        task_embs = self.task_proj(x_dict["task"])                           # [n_tasks, H]
        node_parts = [x_dict[t] for t in COMPUTE_NODE_TYPES]
        node_embs = self.node_proj(torch.cat(node_parts, dim=0))             # [n_nodes, H]
        logits = (task_embs @ node_embs.T).flatten()                         # [n_tasks * n_nodes]

        # Value: mean pool over all node types
        embeddings = [x_dict[nt].mean(dim=0) for nt in NODE_TYPES
                      if nt in x_dict and x_dict[nt].numel() > 0]
        global_emb = torch.stack(embeddings).mean(dim=0)
        value = self.value_head(global_emb).squeeze(-1)

        return logits, value
