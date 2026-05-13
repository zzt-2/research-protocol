"""HGAT (Heterogeneous Graph Attention) encoder for satellite DAG task offloading.

Processes the HeteroData observation directly via HeteroConv-wrapped GATConv
layers, preserving heterogeneous structure rather than converting to homogeneous.
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor
from torch.distributions import Categorical
from torch_geometric.data import HeteroData
from torch_geometric.nn import GATConv, HeteroConv

from config import (
    EDGE_TYPES,
    HGAT_HEADS,
    HGAT_HIDDEN,
    HGAT_LAYERS,
    N_TASKS,
    NODE_TYPES,
)
from ppo import BaseActorCritic

# Per-node-type input feature dimensions (from environment._build_graph)
NODE_FEAT_DIMS = {"task": 8, "iotd": 4, "uav": 5, "leo": 5, "cs": 2}

# Total number of compute nodes: iotd(1) + uav(4) + leo(8) + cs(1) = 14
N_NODES = 14
N_ACTIONS = N_TASKS * N_NODES

# Sentinel value for masking invalid actions (matches ppo._MASK_VALUE)
_MASK_VALUE = -1e8

# Empty edge_index placeholder for missing edge types
_EMPTY_EDGE = torch.tensor([[], []], dtype=torch.long)


class HGATActorCritic(BaseActorCritic):
    """Heterogeneous Graph Attention Network for PPO actor-critic.

    Architecture:
      1. Per-type linear projections → shared hidden_dim
      2. HGAT_LAYERS × HeteroConv(GATConv per edge type) + LayerNorm + ReLU
      3. Mean pooling across all node types → graph embedding
      4. Separate policy / value MLP heads
    """

    def __init__(self, hidden_dim: int = HGAT_HIDDEN, n_heads: int = HGAT_HEADS,
                 n_layers: int = HGAT_LAYERS) -> None:
        super().__init__()
        self.hidden_dim = hidden_dim
        self.n_heads = n_heads
        self.n_layers = n_layers
        head_dim = hidden_dim // n_heads

        # --- 1. Per-type input projections ---
        self.input_proj = nn.ModuleDict({
            ntype: nn.Linear(NODE_FEAT_DIMS[ntype], hidden_dim)
            for ntype in NODE_TYPES
        })

        # --- 2. HeteroConv layers with LayerNorm ---
        self.conv_layers = nn.ModuleList()
        self.norm_layers = nn.ModuleList()
        for _ in range(n_layers):
            conv_dict = {}
            for etype in EDGE_TYPES:
                src_type, _, dst_type = etype
                # GATConv: in_channels (src) = hidden_dim, out_channels = head_dim
                conv_dict[etype] = GATConv(
                    in_channels=(hidden_dim, hidden_dim),
                    out_channels=head_dim,
                    heads=n_heads,
                    add_self_loops=(src_type == dst_type),
                )
            self.conv_layers.append(HeteroConv(conv_dict, aggr="sum"))
            # LayerNorm per destination node type
            self.norm_layers.append(nn.ModuleDict({
                ntype: nn.LayerNorm(hidden_dim)
                for ntype in NODE_TYPES
            }))

        # --- 3. Policy head: hidden_dim → N_ACTIONS ---
        self.policy_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, N_ACTIONS),
        )

        # --- 4. Value head: hidden_dim → 1 ---
        self.value_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

    def _ensure_all_edge_types(self, x_dict: dict, edge_index_dict: dict, device: torch.device) -> dict:
        """Fill missing edge types with empty edge_index so HeteroConv sees all keys."""
        for etype in EDGE_TYPES:
            if etype not in edge_index_dict:
                edge_index_dict[etype] = _EMPTY_EDGE.to(device)
        return edge_index_dict

    def _encode(self, obs: HeteroData) -> Tensor:
        """Run HGAT encoder and return a graph-level embedding (hidden_dim,)."""
        device = next(self.parameters()).device
        obs = obs.to(device)
        # Project each node type into shared hidden space
        x_dict = {
            ntype: self.input_proj[ntype](obs[ntype].x)
            for ntype in NODE_TYPES
        }

        # Collect edge indices, filling missing types with empty tensors
        edge_index_dict = {}
        for etype in EDGE_TYPES:
            if hasattr(obs[etype[0], etype[1], etype[2]], "edge_index"):
                edge_index_dict[etype] = obs[etype[0], etype[1], etype[2]].edge_index
        edge_index_dict = self._ensure_all_edge_types(x_dict, edge_index_dict, device)

        # Message-passing layers
        for i, (conv, norms) in enumerate(zip(self.conv_layers, self.norm_layers)):
            out_dict = conv(x_dict, edge_index_dict)
            # Apply LayerNorm + ReLU per node type; missing types get zeros
            new_x_dict = {}
            for ntype in NODE_TYPES:
                if ntype in out_dict and out_dict[ntype].numel() > 0:
                    new_x_dict[ntype] = F.relu(norms[ntype](out_dict[ntype]))
                else:
                    # Node type had no incoming messages — keep previous embedding
                    new_x_dict[ntype] = x_dict[ntype]
            x_dict = new_x_dict

        # --- Global mean pooling across all node types ---
        embeddings = []
        for ntype in NODE_TYPES:
            if ntype in x_dict and x_dict[ntype].numel() > 0:
                embeddings.append(x_dict[ntype].mean(dim=0))
        graph_emb = torch.stack(embeddings).mean(dim=0)
        return graph_emb

    def forward(self, obs: HeteroData) -> tuple[Tensor, Tensor]:
        """Return (action_logits [N_ACTIONS], value_scalar)."""
        graph_emb = self._encode(obs)
        logits = self.policy_head(graph_emb)
        value = self.value_head(graph_emb)
        return logits, value.squeeze(-1)

    @torch.no_grad()
    def get_action(
        self, obs: HeteroData, action_mask: np.ndarray
    ) -> tuple[int, float, float, float]:
        """Sample one action. Returns (action, log_prob, value, entropy)."""
        logits, value = self.forward(obs)
        mask = torch.as_tensor(action_mask, dtype=torch.bool, device=logits.device)
        logits = logits.masked_fill(~mask, _MASK_VALUE)
        dist = Categorical(logits=logits)
        action = dist.sample()
        return (
            action.item(),
            dist.log_prob(action).item(),
            value.item(),
            dist.entropy().item(),
        )

    def evaluate_actions(
        self,
        obs_list: list[HeteroData],
        actions: Tensor,
        action_masks: Tensor,
    ) -> tuple[Tensor, Tensor, Tensor]:
        """Re-evaluate actions under the current policy.

        Returns (log_probs, values, entropy), each shape (batch,).
        """
        log_probs_list: list[Tensor] = []
        values_list: list[Tensor] = []
        entropy_list: list[Tensor] = []

        for i, obs in enumerate(obs_list):
            logits, value = self.forward(obs)
            mask = action_masks[i]
            logits = logits.masked_fill(~mask.to(dtype=torch.bool, device=logits.device),
                                        _MASK_VALUE)
            dist = Categorical(logits=logits)
            log_probs_list.append(dist.log_prob(actions[i]))
            values_list.append(value.squeeze())
            entropy_list.append(dist.entropy())

        return (
            torch.stack(log_probs_list),
            torch.stack(values_list),
            torch.stack(entropy_list),
        )
