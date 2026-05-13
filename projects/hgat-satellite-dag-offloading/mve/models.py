"""models.py - HGAT and GraphSAGE encoders with Actor-Critic head."""
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import HANConv, SAGEConv

METADATA = (
    ["task", "iotd", "uav", "leo", "cs"],
    [
        ("task", "dep", "task"),
        ("task", "to_iotd", "iotd"),
        ("task", "to_uav", "uav"),
        ("task", "to_leo", "leo"),
        ("task", "to_cs", "cs"),
    ],
)


class HGATEncoder(nn.Module):
    def __init__(self, hidden=16, heads=4, n_layers=2, out_dim=64):
        super().__init__()
        self.node_types = METADATA[0]
        in_ch = {"task": 5, "iotd": 4, "uav": 4, "leo": 4, "cs": 4}
        self.convs = nn.ModuleList()
        for i in range(n_layers):
            self.convs.append(
                HANConv(
                    in_channels=in_ch if i == 0 else hidden,
                    out_channels=hidden,
                    metadata=METADATA,
                    heads=heads,
                )
            )
        self.proj = nn.Linear(hidden * len(self.node_types), out_dim)
        self.out_dim = out_dim

    def forward(self, g):
        x_dict = {k: v.clone() for k, v in g.x_dict.items()}
        ei_dict = g.edge_index_dict
        for conv in self.convs:
            x_dict = conv(x_dict, ei_dict)
            x_dict = {k: F.elu(v) for k, v in x_dict.items()}
        pooled = [x_dict[nt].mean(dim=0) for nt in self.node_types if nt in x_dict and x_dict[nt].numel() > 0]
        return self.proj(torch.cat(pooled))


class GraphSAGEEncoder(nn.Module):
    def __init__(self, in_dim=9, hidden=64, n_layers=2, out_dim=64):
        super().__init__()
        self.convs = nn.ModuleList()
        self.convs.append(SAGEConv(in_dim, hidden))
        for _ in range(n_layers - 1):
            self.convs.append(SAGEConv(hidden, hidden))
        self.proj = nn.Linear(hidden, out_dim)
        self.out_dim = out_dim

    def forward(self, g):
        x, ei = g.x, g.edge_index
        for conv in self.convs:
            x = F.elu(conv(x, ei))
        return self.proj(x.mean(dim=0))


class ActorCritic(nn.Module):
    def __init__(self, encoder, n_actions=5):
        super().__init__()
        self.encoder = encoder
        self.actor = nn.Sequential(nn.Linear(encoder.out_dim, 64), nn.ELU(), nn.Linear(64, n_actions))
        self.critic = nn.Sequential(nn.Linear(encoder.out_dim, 64), nn.ELU(), nn.Linear(64, 1))

    def forward(self, g):
        emb = self.encoder(g)
        return self.actor(emb), self.critic(emb)
