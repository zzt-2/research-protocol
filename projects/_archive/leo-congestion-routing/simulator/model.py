"""GNN Actor-Critic for LEO congestion-aware routing with discrete K-path action space.

Architecture:
  - GATEncoder: shared GNN backbone (GATConv + LayerNorm + residual)
  - PathScoringHead: actor head, scores K candidate paths → Categorical
  - ValueHead: critic head, src_emb ∥ dst_emb → scalar value

Action space: discrete selection from K candidate paths.
Policy: Categorical distribution over K path scores.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor
from torch.distributions import Categorical
from torch_geometric.nn import GATConv


class GATEncoder(nn.Module):
    """GAT encoder: node_feat + edge_feat -> per-node embedding.

    Architecture: Input projection -> n_layers x (GATConv + LayerNorm + ELU + Residual).
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
        h = self.in_proj(x)
        for conv, norm in zip(self.convs, self.norms):
            out = conv(h, edge_index, edge_attr=edge_attr)
            out = norm(out)
            h = F.elu(out) + h
        return h


class PathScoringHead(nn.Module):
    """Score K candidate paths using node embeddings.

    For each path: mean(node_emb[path_nodes]) -> MLP -> scalar score.
    K scores form Categorical logits. Invalid paths get -1e9 mask.
    """

    def __init__(self, hidden_dim: int) -> None:
        super().__init__()
        self.mlp = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
        )

    def forward(
        self, node_emb: Tensor, paths: list[list[int]], n_valid: int, K: int,
    ) -> Tensor:
        """Score candidate paths.

        Args:
            node_emb: Node embeddings (N, hidden_dim).
            paths: List of K candidate paths (each a list of node ids).
            n_valid: Number of valid paths (< K if some paths unavailable).
            K: Maximum number of candidate paths.

        Returns:
            Logits (K,) for Categorical distribution.
        """
        scores = []
        for i, path in enumerate(paths):
            if i >= n_valid:
                break
            idx = torch.tensor(path, dtype=torch.long, device=node_emb.device)
            path_emb = node_emb[idx].mean(dim=0)
            scores.append(self.mlp(path_emb).squeeze())

        # Pad invalid actions with large negative score
        while len(scores) < K:
            scores.append(torch.tensor(-1e9, dtype=torch.float32, device=node_emb.device))

        return torch.stack(scores[:K])


class RoutingActorCritic(nn.Module):
    """GNN routing model with discrete K-path action space.

    Architecture:
      - GATEncoder: shared backbone, node/edge features -> node embeddings
      - PathScoringHead: actor head, scores K paths -> Categorical logits
      - ValueHead: critic head, src_emb ∥ dst_emb -> scalar value

    Action: discrete selection from K candidate paths.
    Policy: Categorical distribution.
    """

    def __init__(
        self,
        node_dim: int = 7,
        edge_dim: int = 4,
        hidden_dim: int = 64,
        n_layers: int = 2,
        n_heads: int = 4,
        k_paths: int = 4,
    ) -> None:
        super().__init__()
        self.K = k_paths
        self.encoder = GATEncoder(node_dim, edge_dim, hidden_dim, n_layers, n_heads)
        self.actor = PathScoringHead(hidden_dim)
        self.critic = nn.Sequential(
            nn.Linear(hidden_dim * 2, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
        )

    def _encode_obs(self, obs: dict) -> tuple[Tensor, Tensor]:
        """Encode dict observation to node embeddings and value."""
        dev = self.device
        x = torch.as_tensor(obs["node_feat"], dtype=torch.float32, device=dev)
        ei = torch.as_tensor(obs["edge_index"], dtype=torch.long, device=dev)
        ea = torch.as_tensor(obs["edge_feat"], dtype=torch.float32, device=dev)

        node_emb = self.encoder(x, ei, ea)  # (N, hidden_dim)

        src, dst, _ = obs["flow"]
        paths = obs["paths"]
        n_valid = obs["n_valid"]

        logits = self.actor(node_emb, paths, n_valid, self.K)
        value = self.critic(torch.cat([node_emb[src], node_emb[dst]])).squeeze()

        return logits, value

    @torch.no_grad()
    def get_action(
        self, obs: dict, deterministic: bool = False,
    ) -> tuple[Tensor, Tensor, Tensor]:
        """Sample an action from the current policy.

        Returns:
            (action, log_prob, value) where action is scalar int,
            log_prob and value are scalars.
        """
        logits, value = self._encode_obs(obs)

        if deterministic:
            action = logits.argmax()
            log_prob = torch.tensor(0.0, device=logits.device)
        else:
            dist = Categorical(logits=logits)
            action = dist.sample()
            log_prob = dist.log_prob(action)

        return action, log_prob, value

    def evaluate_actions(
        self, obs_list: list[dict], actions: Tensor,
    ) -> tuple[Tensor, Tensor, Tensor]:
        """Re-evaluate actions for PPO update.

        Args:
            obs_list: List of dict observations (length B).
            actions: Previously sampled actions (B,) int tensor.

        Returns:
            (log_probs, values, entropies) each of shape (B,).
        """
        log_probs: list[Tensor] = []
        values: list[Tensor] = []
        entropies: list[Tensor] = []

        for i, obs in enumerate(obs_list):
            logits, value = self._encode_obs(obs)
            dist = Categorical(logits=logits)
            log_probs.append(dist.log_prob(actions[i]))
            values.append(value.squeeze())
            entropies.append(dist.entropy())

        return torch.stack(log_probs), torch.stack(values), torch.stack(entropies)

    @property
    def device(self) -> torch.device:
        return next(self.parameters()).device
