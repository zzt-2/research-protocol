"""GATv2 Actor-Critic for ISL scheduling — continuous edge scores.

Architecture (from data-flow.md):
  - Node projection: Linear(6, 64)
  - Edge projection: Linear(7, 64)
  - GATv2Conv × 3 layers (4-head, 64-dim, edge_dim=64) + LayerNorm + residual
  - Actor (edge decoder): concat(src, dst) (128,) → MLP 128→64→32→1 → sigmoid
  - Critic: global_mean_pool (64,) → MLP 64→32→1
  - Exploration: Normal(scores, σ) with learnable log_std
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor
from torch_geometric.data import Data
from torch_geometric.nn import GATv2Conv, global_mean_pool


class GATv2ActorCritic(nn.Module):
    def __init__(
        self,
        node_dim: int = 6,
        edge_dim: int = 7,
        hidden_dim: int = 64,
        n_heads: int = 4,
        n_layers: int = 3,
    ) -> None:
        super().__init__()
        self.hidden_dim = hidden_dim
        self.node_dim = node_dim
        self.edge_dim = edge_dim

        head_dim = hidden_dim // n_heads
        assert hidden_dim % n_heads == 0

        # Input projections
        self.node_proj = nn.Linear(node_dim, hidden_dim)
        self.edge_proj = nn.Linear(edge_dim, hidden_dim)

        # GATv2 layers
        self.convs = nn.ModuleList()
        self.norms = nn.ModuleList()
        for _ in range(n_layers):
            self.convs.append(GATv2Conv(
                (hidden_dim, hidden_dim), head_dim,
                heads=n_heads, edge_dim=hidden_dim,
                add_self_loops=True,
            ))
            self.norms.append(nn.LayerNorm(hidden_dim))

        # Edge decoder (Actor)
        self.edge_decoder = nn.Sequential(
            nn.Linear(2 * hidden_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
        )

        # Critic head
        self.critic_head = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
        )

        # Learnable exploration noise
        self.log_std = nn.Parameter(torch.tensor(-2.0))

    def _encode(
        self, x: Tensor, edge_index: Tensor, edge_attr: Tensor,
    ) -> Tensor:
        """GATv2 message passing → node embeddings (N, hidden_dim)."""
        x = self.node_proj(x)
        edge_attr_proj = self.edge_proj(edge_attr)

        for conv, norm in zip(self.convs, self.norms):
            residual = x
            out = conv(x, edge_index, edge_attr=edge_attr_proj)
            out = norm(out)
            x = F.relu(out) + residual

        return x

    def _decode_edges(
        self, node_emb: Tensor, edge_index: Tensor,
    ) -> Tensor:
        """Concat(src, dst) → MLP → raw logits (E,)."""
        src, dst = edge_index
        edge_input = torch.cat([node_emb[src], node_emb[dst]], dim=-1)
        return self.edge_decoder(edge_input).squeeze(-1)

    def forward(self, data: Data) -> tuple[Tensor, Tensor]:
        """Returns (edge_scores ∈ [0,1] shape (E,), value scalar)."""
        device = next(self.parameters()).device
        data = data.to(device)

        node_emb = self._encode(data.x, data.edge_index, data.edge_attr)

        # Actor
        raw = self._decode_edges(node_emb, data.edge_index)
        edge_scores = torch.sigmoid(raw)

        # Critic
        batch = getattr(data, "batch", None)
        if batch is None:
            graph_emb = node_emb.mean(dim=0, keepdim=True)
        else:
            graph_emb = global_mean_pool(node_emb, batch)
        value = self.critic_head(graph_emb).squeeze()

        return edge_scores, value

    @torch.no_grad()
    def get_action(
        self, data: Data, deterministic: bool = False,
    ) -> tuple[Tensor, Tensor, Tensor]:
        """Sample edge scores. Returns (scores, log_prob, value).

        log_prob uses *mean* over edges (not sum) so PPO clip range
        is independent of candidate-edge count.
        """
        scores, value = self.forward(data)

        if deterministic:
            return scores, torch.zeros(1, device=scores.device), value

        std = torch.exp(self.log_std).clamp(max=0.5)
        dist = torch.distributions.Normal(scores, std.expand_as(scores))
        sampled = dist.sample().clamp(0.0, 1.0)
        # mean log_prob keeps magnitude stable across varying E
        log_prob = dist.log_prob(sampled).mean()

        return sampled, log_prob, value

    def evaluate_actions(
        self,
        data_list: list[Data],
        old_scores_list: list[Tensor],
    ) -> tuple[Tensor, Tensor, Tensor]:
        """PPO re-evaluation. Returns (log_probs, values, entropies) shape (B,)."""
        std = torch.exp(self.log_std).clamp(max=0.5)
        log_probs, values, entropies = [], [], []

        for data, old_scores in zip(data_list, old_scores_list):
            scores, value = self.forward(data)
            dist = torch.distributions.Normal(scores, std.expand_as(scores))
            old_t = old_scores.to(device=scores.device, dtype=scores.dtype)
            log_probs.append(dist.log_prob(old_t).mean())
            values.append(value.squeeze())
            entropies.append(dist.entropy().mean())

        return (
            torch.stack(log_probs),
            torch.stack(values),
            torch.stack(entropies),
        )

    @property
    def n_params(self) -> int:
        return sum(p.numel() for p in self.parameters())
