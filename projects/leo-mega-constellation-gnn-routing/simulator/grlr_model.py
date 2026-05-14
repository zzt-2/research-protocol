"""GRLR baseline: 6-node local graph GAT + Actor-Critic.

Reproduces Zhang et al. TVT 2025 "GRLR: Routing With Graph Neural Network
and Reinforcement Learning for Mega LEO Satellite Constellations".

Architecture (per paper §III):
- Actor: GAT(1 layer, out=64) → LayerNorm → GlobalAddPool → FC(64→4)
- Critic: GAT(1 layer, out=32) → LayerNorm → GlobalAddPool → FC(32→1)
- Input: 6-node directed graph per routing decision
- Node features: [lat_norm, lon_norm, traffic_norm] = 3 dim
- Edge features: [delay_norm, dist_norm] = 2 dim
"""
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATConv
from torch_geometric.data import Data, Batch

from config import C_LIGHT


class GRLRModel(nn.Module):
    """Separate GAT feature extractors for Actor and Critic."""

    def __init__(self, node_dim=3, edge_dim=2, actor_hidden=64, critic_hidden=32):
        super().__init__()
        self.actor_gat = GATConv(node_dim, actor_hidden, heads=1, edge_dim=edge_dim)
        self.actor_norm = nn.LayerNorm(actor_hidden)
        self.actor_head = nn.Sequential(
            nn.Linear(actor_hidden, actor_hidden),
            nn.ReLU(),
            nn.Linear(actor_hidden, 4),
        )
        self.critic_gat = GATConv(node_dim, critic_hidden, heads=1, edge_dim=edge_dim)
        self.critic_norm = nn.LayerNorm(critic_hidden)
        self.critic_head = nn.Sequential(
            nn.Linear(critic_hidden, critic_hidden),
            nn.ReLU(),
            nn.Linear(critic_hidden, 1),
        )

    def forward(self, data):
        """Returns (logits (B,4), value (B,))."""
        a = F.leaky_relu(self.actor_gat(data.x, data.edge_index, data.edge_attr))
        a = self.actor_norm(a)
        a_pool = _global_add_pool(a, data)

        c = F.leaky_relu(self.critic_gat(data.x, data.edge_index, data.edge_attr))
        c = self.critic_norm(c)
        c_pool = _global_add_pool(c, data)

        logits = self.actor_head(a_pool)
        value = self.critic_head(c_pool).squeeze(-1)
        return logits, value


def _global_add_pool(x, data):
    if hasattr(data, 'batch') and data.batch is not None:
        from torch_geometric.nn import global_add_pool as gap
        return gap(x, data.batch)
    return x.sum(dim=0, keepdim=True)


def _eci_to_latlon(pos):
    """ECI → (lat_deg, lon_deg) approximation."""
    r = np.linalg.norm(pos, axis=1, keepdims=True).squeeze()
    lat = np.degrees(np.arcsin(pos[:, 2] / r))
    lon = np.degrees(np.arctan2(pos[:, 1], pos[:, 0]))
    return lat, lon


def build_local_graphs(current_indices, dest_idx, snap, walker, neighbor_map,
                       traffic=None):
    """Build batched 6-node local graphs for parallel routing decisions.

    6 nodes: [current, nb_intra_fwd, nb_intra_bwd, nb_inter_r, nb_inter_l, dest]
    Directed edges: current→neighbors, neighbors→dest, current→dest.

    Returns (Batched PyG Data, valid_mask (B,4) bool tensor).
    """
    S, P = walker.S, walker.P
    pos = snap['pos']
    lat, lon = _eci_to_latlon(pos)
    t_max = traffic.max() if traffic is not None else 1.0

    graphs, masks = [], []
    for cur in current_indices:
        cp, ck = divmod(int(cur), S)
        dp, dk = divmod(int(dest_idx), S)

        # 4 neighbors by direction
        nbs = [
            cp * S + (ck + 1) % S,     # 0: intra fwd
            cp * S + (ck - 1) % S,      # 1: intra bwd
            ((cp + 1) % P) * S + ck,    # 2: inter right
            ((cp - 1) % P) * S + ck,    # 3: inter left
        ]

        node_ids = [cur] + nbs + [dest_idx]
        # Node features: normalized lat, lon, traffic
        nx = np.array([
            [lat[i] / 90.0, lon[i] / 180.0, (traffic[i] if traffic is not None else 1.0) / t_max]
            for i in node_ids
        ], dtype=np.float32)

        edges, ea = [], []
        valid = [False] * 4

        # current(0) → neighbor(i+1) with ISL features
        for d, nb in enumerate(nbs):
            key = (cur, d)
            if key in neighbor_map:
                _, delay = neighbor_map[key]
                dist = float(np.linalg.norm(pos[cur] - pos[nb]))
                edges.append([0, d + 1])
                ea.append([delay / 50.0, dist / 6000.0])
                valid[d] = True

        # neighbor(i+1) → dest(5): geometric approximation
        for d, nb in enumerate(nbs):
            dist = float(np.linalg.norm(pos[nb] - pos[dest_idx]))
            dly = dist / C_LIGHT * 1000
            edges.append([d + 1, 5])
            ea.append([dly / 50.0, dist / 6000.0])

        # current(0) → dest(5)
        dist_cd = float(np.linalg.norm(pos[cur] - pos[dest_idx]))
        dly_cd = dist_cd / C_LIGHT * 1000
        edges.append([0, 5])
        ea.append([dly_cd / 50.0, dist_cd / 6000.0])

        if not edges:
            edges.append([0, 5])
            ea.append([0.0, 0.0])

        x = torch.tensor(nx, dtype=torch.float32)
        ei = torch.tensor(edges, dtype=torch.long).t().contiguous()
        eattr = torch.tensor(ea, dtype=torch.float32)

        graphs.append(Data(x=x, edge_index=ei, edge_attr=eattr))
        masks.append(valid)

    batched = Batch.from_data_list(graphs) if len(graphs) > 1 else graphs[0]
    mask = torch.tensor(masks, dtype=torch.bool)
    return batched, mask
