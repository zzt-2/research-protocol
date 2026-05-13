"""GNN model with Orbital Position Encoding for Walker-Delta routing."""
import math
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATConv


class OrbitalPE(nn.Module):
    """Sin/cos positional encoding based on orbital position.

    Encodes (plane_idx / P, sat_idx / S) at multiple frequencies.
    Output dim = pe_dim (must be divisible by 4).
    """
    def __init__(self, pe_dim=16):
        super().__init__()
        self.pe_dim = pe_dim
        self.n_freq = pe_dim // 4

    def forward(self, plane_ids, sat_ids, P, S):
        """
        Args:
            plane_ids: (N,) int tensor, plane index per node
            sat_ids: (N,) int tensor, sat index per node
            P: int, number of planes
            S: int, sats per plane
        Returns:
            (N, pe_dim) float tensor
        """
        p_norm = plane_ids.float() / P
        s_norm = sat_ids.float() / S
        pe_parts = []
        for i in range(self.n_freq):
            freq = 2 ** i * 2 * math.pi
            pe_parts.extend([
                torch.sin(freq * p_norm),
                torch.cos(freq * p_norm),
                torch.sin(freq * s_norm),
                torch.cos(freq * s_norm),
            ])
        return torch.stack(pe_parts, dim=-1)


class RoutingGNN(nn.Module):
    """GAT-based routing model with precomputed Orbital PE.

    Node input: [is_dest(1), own_PE(16), dest_PE(16)] = 33 dim (precomputed).
    Outputs per-node scores over 4 ISL directions.
    """
    def __init__(self, node_dim=33, edge_dim=2, hidden=64,
                 n_layers=2, heads=4, n_directions=4):
        super().__init__()
        self.convs = nn.ModuleList()
        self.convs.append(GATConv(node_dim, hidden // heads, heads=heads, edge_dim=edge_dim))
        for _ in range(n_layers - 1):
            self.convs.append(GATConv(hidden, hidden // heads, heads=heads, edge_dim=edge_dim))

        self.direction_head = nn.Sequential(
            nn.Linear(hidden, hidden),
            nn.ReLU(),
            nn.Linear(hidden, n_directions),
        )

    def forward(self, data):
        """Returns direction_scores: (N, 4) logits."""
        x = data.x
        for conv in self.convs:
            x = F.elu(conv(x, data.edge_index, data.edge_attr))
        return self.direction_head(x)


class RoutingGNNActorCritic(nn.Module):
    """GNN + Actor-Critic for PPO training.

    Actor: direction scores (N, 4)
    Critic: global value (1,)
    """
    def __init__(self, node_dim=1, edge_dim=2, pe_dim=16, hidden=64,
                 n_layers=2, heads=4, n_directions=4):
        super().__init__()
        self.pe = OrbitalPE(pe_dim)
        input_dim = node_dim + pe_dim

        self.convs = nn.ModuleList()
        self.convs.append(GATConv(input_dim, hidden // heads, heads=heads, edge_dim=edge_dim))
        for _ in range(n_layers - 1):
            self.convs.append(GATConv(hidden, hidden // heads, heads=heads, edge_dim=edge_dim))

        self.actor = nn.Sequential(
            nn.Linear(hidden, hidden),
            nn.ReLU(),
            nn.Linear(hidden, n_directions),
        )
        self.critic = nn.Sequential(
            nn.Linear(hidden, hidden),
            nn.ReLU(),
            nn.Linear(hidden, 1),
        )

    def forward(self, data, plane_ids, sat_ids, P, S):
        pe = self.pe(plane_ids, sat_ids, P, S)
        x = torch.cat([data.x, pe], dim=-1)

        for conv in self.convs:
            x = F.elu(conv(x, data.edge_index, data.edge_attr))

        action_logits = self.actor(x)       # (N, 4)
        value = self.critic(x).mean()       # scalar
        return action_logits, value
