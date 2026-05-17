"""GNN Actor-Critic for LEO congestion-aware routing with continuous action space.

Architecture:
  - GATEncoder: shared GNN backbone (GATConv + LayerNorm + residual)
  - EdgeWeightDecoder: actor head, per-edge positive weight prediction
  - ValueHead: critic head, global readout to scalar value

Action space: E-dimensional continuous vector (per-edge weights for weighted shortest path).
Policy: Gaussian (Normal distribution) with learned log_std.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor
from torch.distributions import Normal
from torch_geometric.data import Data
from torch_geometric.nn import GATConv


class GATEncoder(nn.Module):
    """GAT encoder: node_feat + edge_feat -> per-node embedding.

    Architecture: Input projection -> n_layers x (GATConv + LayerNorm + ReLU + Residual).
    Reference: L06 DTAR (GAT+LN+Residual), sim-template/model_gnn.py.

    Args:
        node_dim: Input node feature dimension.
        edge_dim: Input edge feature dimension.
        hidden_dim: GNN hidden dimension.
        n_layers: Number of GAT layers.
        n_heads: Number of attention heads per layer.
    """

    def __init__(
        self,
        node_dim: int,
        edge_dim: int,
        hidden_dim: int,
        n_layers: int,
        n_heads: int,
    ) -> None:
        super().__init__()
        assert hidden_dim % n_heads == 0, (
            f"hidden_dim ({hidden_dim}) must be divisible by n_heads ({n_heads})"
        )
        self.in_proj = nn.Linear(node_dim, hidden_dim)
        head_dim = hidden_dim // n_heads

        self.convs = nn.ModuleList()
        self.norms = nn.ModuleList()
        for _ in range(n_layers):
            self.convs.append(GATConv(
                (hidden_dim, hidden_dim), head_dim,
                heads=n_heads, edge_dim=edge_dim, add_self_loops=True,
            ))
            self.norms.append(nn.LayerNorm(hidden_dim))

    def forward(self, x: Tensor, edge_index: Tensor, edge_attr: Tensor | None = None) -> Tensor:
        """Encode node features through GAT layers.

        Args:
            x: Node features (N, node_dim).
            edge_index: Edge indices (2, E).
            edge_attr: Edge features (E, edge_dim) or None.

        Returns:
            Per-node embeddings (N, hidden_dim).
        """
        h = self.in_proj(x)
        for conv, norm in zip(self.convs, self.norms):
            out = conv(h, edge_index, edge_attr=edge_attr)
            out = norm(out)
            h = F.relu(out) + h
        return h


class EdgeWeightDecoder(nn.Module):
    """Per-edge weight decoder: node embeddings + edge features -> positive edge weights.

    For each directed edge (u,v): weight = MLP(emb_u || emb_v || edge_feat_uv).
    Output passed through softplus to ensure strictly positive weights (required by Dijkstra).

    Args:
        hidden_dim: Node embedding dimension.
        edge_dim: Edge feature dimension.
    """

    def __init__(self, hidden_dim: int, edge_dim: int) -> None:
        super().__init__()
        self.mlp = nn.Sequential(
            nn.Linear(hidden_dim * 2 + edge_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, node_emb: Tensor, edge_index: Tensor, edge_attr: Tensor) -> Tensor:
        """Predict per-edge positive weights.

        Args:
            node_emb: Node embeddings (N, hidden_dim).
            edge_index: Edge indices (2, E).
            edge_attr: Edge features (E, edge_dim).

        Returns:
            Positive edge weights (E,).
        """
        src, dst = edge_index[0], edge_index[1]
        edge_input = torch.cat([node_emb[src], node_emb[dst], edge_attr], dim=-1)
        raw = self.mlp(edge_input).squeeze(-1)
        return F.softplus(raw) + 1e-6


class RoutingActorCritic(nn.Module):
    """GNN routing model with continuous action space for LEO congestion-aware routing.

    Architecture:
      - GATEncoder: shared backbone, node/edge features -> node embeddings
      - EdgeWeightDecoder: actor head, per-edge weight prediction
      - ValueHead: critic head, global readout -> scalar value

    Action: E-dimensional continuous vector (edge weights for weighted shortest path routing).
    Policy: Gaussian (Normal distribution) with learned log_std.

    Args:
        node_dim: Node feature dimension.
        edge_dim: Edge feature dimension.
        hidden_dim: Hidden dimension for GNN and heads.
        n_layers: Number of GAT layers.
        n_heads: Number of attention heads per layer.
        n_edges: Number of directed edges (determines log_std parameter size).
    """

    def __init__(
        self,
        node_dim: int = 6,
        edge_dim: int = 4,
        hidden_dim: int = 64,
        n_layers: int = 2,
        n_heads: int = 4,
        n_edges: int = 264,
    ) -> None:
        super().__init__()
        self.encoder = GATEncoder(node_dim, edge_dim, hidden_dim, n_layers, n_heads)
        self.actor = EdgeWeightDecoder(hidden_dim, edge_dim)
        self.critic = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )
        self.log_std = nn.Parameter(torch.zeros(n_edges))

    def forward(self, data: Data) -> tuple[Tensor, Tensor]:
        """Forward pass with gradients.

        Args:
            data: PyG Data object with x, edge_index, edge_attr.

        Returns:
            (edge_weights_mean, value) where edge_weights_mean is (E,) and value is scalar.
        """
        data = data.to(self.device)
        node_emb = self.encoder(data.x, data.edge_index, data.edge_attr)
        weights_mean = self.actor(node_emb, data.edge_index, data.edge_attr)
        value = self.critic(node_emb.mean(dim=0)).squeeze(-1)
        return weights_mean, value

    @torch.no_grad()
    def get_action(
        self, data: Data, deterministic: bool = False,
    ) -> tuple[Tensor, Tensor, Tensor]:
        """Sample an action from the current policy.

        Args:
            data: PyG Data observation.
            deterministic: If True, return mean directly without sampling.

        Returns:
            (action, log_prob, value) where action is (E,), log_prob and value are scalars.
        """
        mean, value = self.forward(data)
        if deterministic:
            action = mean.clone()
            log_prob = torch.tensor(0.0, device=self.device)
        else:
            std = self.log_std.exp()
            dist = Normal(mean, std)
            action = dist.sample()
            action = torch.clamp(action, min=1e-6)  # Dijkstra requires positive weights
            action = torch.where(torch.isnan(action), mean, action)
            log_prob = dist.log_prob(action).sum()
        return action, log_prob, value

    def evaluate_actions(
        self, data_list: list[Data], actions: Tensor,
    ) -> tuple[Tensor, Tensor, Tensor]:
        """Re-evaluate actions for PPO update.

        Args:
            data_list: List of PyG Data observations (length B).
            actions: Previously sampled actions (B, E).

        Returns:
            (log_probs, values, entropies) each of shape (B,).
        """
        log_probs: list[Tensor] = []
        values: list[Tensor] = []
        entropies: list[Tensor] = []
        for i, data in enumerate(data_list):
            mean, value = self.forward(data)
            std = self.log_std.exp()
            dist = Normal(mean, std)
            log_probs.append(dist.log_prob(actions[i]).sum())
            values.append(value.squeeze())
            entropies.append(dist.entropy().sum())
        return torch.stack(log_probs), torch.stack(values), torch.stack(entropies)

    @property
    def device(self) -> torch.device:
        """Return the device of the first model parameter."""
        return next(self.parameters()).device
