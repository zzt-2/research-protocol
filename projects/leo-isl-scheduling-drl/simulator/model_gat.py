"""GATv2 Actor-Critic for ISL scheduling — continuous edge scores.

Architecture (optimized for speed):
  - Node projection: Linear(6, 64)
  - GATv2Conv × 3 layers (4-head, 64-dim, NO edge_dim) + LayerNorm + residual
    → ~4ms/layer on GPU (vs 67ms with edge_dim)
  - Edge decoder: concat(src_emb, dst_emb, edge_feat) (135,) → MLP → sigmoid
    → edge features enter at decoder, not in message passing
  - Critic: global_mean_pool (64,) → MLP 64→32→1
  - Exploration: Normal(scores, σ) with learnable log_std
  - Batched evaluate_actions via PyG Batch for efficient PPO updates
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor
from torch_geometric.data import Data, Batch
from torch_geometric.nn import GATv2Conv, global_mean_pool


class GATv2ActorCritic(nn.Module):
    def __init__(
        self,
        node_dim: int = 6,
        edge_dim: int = 8,
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

        # Node projection
        self.node_proj = nn.Linear(node_dim, hidden_dim)

        # GATv2 layers — no edge_dim for speed
        self.convs = nn.ModuleList()
        self.norms = nn.ModuleList()
        for _ in range(n_layers):
            self.convs.append(GATv2Conv(
                (hidden_dim, hidden_dim), head_dim,
                heads=n_heads, edge_dim=None,
                add_self_loops=True,
            ))
            self.norms.append(nn.LayerNorm(hidden_dim))

        # Edge decoder: concat(src_emb, dst_emb, edge_feat) → MLP → score
        self.edge_decoder = nn.Sequential(
            nn.Linear(2 * hidden_dim + edge_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
        )

        # Critic head
        self.critic_head = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
        )

        # Active ISL bias: favor maintaining active edges (edge_feat dim 2)
        # sigmoid(3.0) ≈ 0.95
        self.active_bias = nn.Parameter(torch.tensor(3.0))

        # Distance bias: prefer shorter edges (edge_feat dim 1 = distance/Z_MAX)
        # (1 - distance_norm) is 1.0 for zero distance, 0.0 for Z_MAX
        self.distance_bias = nn.Parameter(torch.tensor(2.0))

        # Learnable exploration noise (small std for stable top-K ranking)
        self.log_std = nn.Parameter(torch.tensor(-4.0))

    def _encode(self, x: Tensor, edge_index: Tensor) -> Tensor:
        """GATv2 message passing → node embeddings (N, hidden_dim)."""
        x = self.node_proj(x)

        for conv, norm in zip(self.convs, self.norms):
            residual = x
            out = conv(x, edge_index)
            out = norm(out)
            x = F.relu(out) + residual

        return x

    def _decode_edges(
        self, node_emb: Tensor, edge_index: Tensor, edge_attr: Tensor,
    ) -> Tensor:
        """Concat(src_emb, dst_emb, edge_feat) → MLP → raw logits (E,)."""
        src, dst = edge_index
        edge_input = torch.cat([node_emb[src], node_emb[dst], edge_attr], dim=-1)
        return self.edge_decoder(edge_input).squeeze(-1)

    def forward(self, data: Data) -> tuple[Tensor, Tensor]:
        """Returns (edge_scores ∈ [0,1] shape (E,), value scalar)."""
        device = next(self.parameters()).device
        data = data.to(device)

        node_emb = self._encode(data.x, data.edge_index)

        # Actor: MLP output + active bias + distance bias
        raw = self._decode_edges(node_emb, data.edge_index, data.edge_attr)
        raw = raw + self.active_bias * data.edge_attr[:, 2]  # keep active edges
        raw = raw + self.distance_bias * (1.0 - data.edge_attr[:, 1])  # prefer shorter
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
        """Sample edge scores. Returns (scores, log_prob, value)."""
        scores, value = self.forward(data)

        if deterministic:
            return scores, torch.zeros(1, device=scores.device), value

        std = torch.exp(self.log_std).clamp(max=0.5)
        dist = torch.distributions.Normal(scores, std.expand_as(scores))
        sampled = dist.sample().clamp(0.0, 1.0)
        log_prob = dist.log_prob(sampled).mean()

        return sampled, log_prob, value

    def evaluate_actions(
        self,
        data_list: list[Data],
        old_scores_list: list[Tensor],
    ) -> tuple[Tensor, Tensor, Tensor]:
        """Batched PPO re-evaluation using PyG Batch.

        Returns (log_probs, values, entropies) shape (B,).
        """
        device = next(self.parameters()).device

        # Batch all graphs into one disconnected graph
        batch_data = Batch.from_data_list(data_list).to(device)

        node_emb = self._encode(batch_data.x, batch_data.edge_index)
        raw = self._decode_edges(node_emb, batch_data.edge_index, batch_data.edge_attr)
        scores = torch.sigmoid(raw)

        # Critic
        graph_emb = global_mean_pool(node_emb, batch_data.batch)
        values = self.critic_head(graph_emb).squeeze(-1)  # (B,)

        # Distribution
        std = torch.exp(self.log_std).clamp(max=0.5)
        dist = torch.distributions.Normal(scores, std.expand_as(scores))

        # Concatenate old scores and compute log_prob for all edges
        old_all = torch.cat([s.to(device=device, dtype=torch.float32) for s in old_scores_list])
        log_prob_all = dist.log_prob(old_all)  # (E_total,)
        entropy_all = dist.entropy()  # (E_total,)

        # Split by graph and take mean per graph
        edge_batch = batch_data.batch[batch_data.edge_index[0]]
        edge_counts = torch.bincount(edge_batch, minlength=len(data_list))

        log_probs = []
        entropies = []
        offset = 0
        for count in edge_counts:
            c = int(count)
            log_probs.append(log_prob_all[offset : offset + c].mean())
            entropies.append(entropy_all[offset : offset + c].mean())
            offset += c

        return (
            torch.stack(log_probs),
            values,
            torch.stack(entropies),
        )

    @property
    def n_params(self) -> int:
        return sum(p.numel() for p in self.parameters())


# ---------------------------------------------------------------------------
# Refactored components: backbone, supervised head, discrete RL head
# ---------------------------------------------------------------------------

import numpy as np


class GATv2Backbone(nn.Module):
    """Shared GATv2 encoder for ISL edge-level tasks.

    Mirrors the encoder from GATv2ActorCritic but exposes encode/decode_edges
    as public methods.  The edge decoder has **no** active/distance bias —
    those are learned from ILP supervision instead.
    """

    def __init__(
        self,
        node_dim: int = 6,
        edge_dim: int = 8,
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

        # Node projection
        self.node_proj = nn.Linear(node_dim, hidden_dim)

        # GATv2 layers — no edge_dim for speed (same as GATv2ActorCritic)
        self.convs = nn.ModuleList()
        self.norms = nn.ModuleList()
        for _ in range(n_layers):
            self.convs.append(GATv2Conv(
                (hidden_dim, hidden_dim), head_dim,
                heads=n_heads, edge_dim=None,
                add_self_loops=True,
            ))
            self.norms.append(nn.LayerNorm(hidden_dim))

        # Edge decoder: no bias terms — raw scores only
        self.edge_decoder = nn.Sequential(
            nn.Linear(2 * hidden_dim + edge_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
        )

    def encode(self, data: Data) -> Tensor:
        """GATv2 message passing → node embeddings (N, hidden_dim)."""
        x = self.node_proj(data.x)
        edge_index = data.edge_index

        for conv, norm in zip(self.convs, self.norms):
            residual = x
            out = conv(x, edge_index)
            out = norm(out)
            x = F.relu(out) + residual

        return x

    def decode_edges(
        self,
        node_emb: Tensor,
        edge_index: Tensor,
        edge_attr: Tensor,
    ) -> Tensor:
        """Concat(src_emb, dst_emb, edge_feat) → MLP → raw scores (E,)."""
        src, dst = edge_index
        h = torch.cat([node_emb[src], node_emb[dst], edge_attr], dim=-1)
        return self.edge_decoder(h).squeeze(-1)


class SupervisedGNN(nn.Module):
    """Phase A: backbone + sigmoid edge classifier for ILP label prediction."""

    def __init__(self, backbone: GATv2Backbone) -> None:
        super().__init__()
        self.backbone = backbone

    def forward(self, data: Data) -> Tensor:
        """Returns edge probabilities (E,) in [0, 1]."""
        node_emb = self.backbone.encode(data)
        raw = self.backbone.decode_edges(node_emb, data.edge_index, data.edge_attr)
        return torch.sigmoid(raw)

    def predict_scores(self, data: Data) -> np.ndarray:
        """Returns edge scores (E,) as numpy for env.step(). No grad."""
        self.eval()
        with torch.no_grad():
            probs = self.forward(data)
        return probs.cpu().numpy()


class DiscreteRLGNN(nn.Module):
    """Phase B: pretrained backbone + 3-way discrete action head + critic.

    Actions per edge: AS-IS(0), FORCE-ON(1), FORCE-OFF(2).
    """

    def __init__(
        self,
        backbone: GATv2Backbone,
        node_dim: int = 6,
        edge_dim: int = 8,
        hidden_dim: int = 64,
    ) -> None:
        super().__init__()
        self.backbone = backbone
        self.hidden_dim = hidden_dim

        # 3-way action head per edge
        self.action_head = nn.Sequential(
            nn.Linear(2 * hidden_dim + edge_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 3),
        )

        # Initialize AS-IS bias: untrained model defaults to keeping backbone scores
        nn.init.zeros_(self.action_head[-1].weight)
        nn.init.zeros_(self.action_head[-1].bias)
        self.action_head[-1].bias.data[0] = 5.0  # strong AS-IS prior

        # Critic
        self.critic_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, 1),
        )

    def _get_edge_input(
        self,
        node_emb: Tensor,
        edge_index: Tensor,
        edge_attr: Tensor,
    ) -> Tensor:
        src, dst = edge_index
        return torch.cat([node_emb[src], node_emb[dst], edge_attr], dim=-1)

    def forward(self, data: Data) -> tuple[Tensor, Tensor]:
        """Returns (action_logits (E, 3), value scalar)."""
        node_emb = self.backbone.encode(data)
        h = self._get_edge_input(node_emb, data.edge_index, data.edge_attr)
        logits = self.action_head(h)  # (E, 3)
        value = self.critic_head(node_emb.mean(dim=0))  # scalar
        return logits, value

    def get_action(
        self,
        data: Data,
        deterministic: bool = False,
    ) -> tuple[Tensor, Tensor, Tensor]:
        """Sample discrete actions per edge.

        Returns:
            actions: (E,) int tensor in {0, 1, 2}
            log_prob: scalar
            value: scalar
        """
        logits, value = self.forward(data)
        dist = torch.distributions.Categorical(logits=logits)
        if deterministic:
            actions = logits.argmax(dim=-1)
        else:
            actions = dist.sample()
        log_prob = dist.log_prob(actions).sum()
        return actions, log_prob, value

    def evaluate_actions(
        self,
        data_list: list[Data],
        actions_list: list[Tensor],
    ) -> tuple[Tensor, Tensor, Tensor]:
        """Batched PPO re-evaluation.

        Returns:
            log_probs: (batch_size,) tensor
            values: (batch_size,) tensor
            entropies: (batch_size,) tensor
        """
        all_log_probs = []
        all_values = []
        all_entropies = []

        for data, actions in zip(data_list, actions_list):
            logits, value = self.forward(data)
            dist = torch.distributions.Categorical(logits=logits)
            log_prob = dist.log_prob(actions).sum()
            entropy = dist.entropy().sum()
            all_log_probs.append(log_prob)
            all_values.append(value.squeeze())
            all_entropies.append(entropy)

        return (
            torch.stack(all_log_probs),
            torch.stack(all_values),
            torch.stack(all_entropies),
        )

    def get_base_scores(self, data: Data) -> np.ndarray:
        """Get base scores from backbone's edge decoder (for DiscreteActionWrapper).

        Returns sigmoid scores (E,) as numpy.
        """
        self.eval()
        with torch.no_grad():
            node_emb = self.backbone.encode(data)
            raw = self.backbone.decode_edges(
                node_emb, data.edge_index, data.edge_attr,
            )
            scores = torch.sigmoid(raw)
        return scores.cpu().numpy()


def load_backbone_with_padding(checkpoint_path: str, device: str = "cpu") -> GATv2Backbone:
    """Load Phase A backbone, padding weights for edge_dim 7→8 if needed."""
    backbone = GATv2Backbone()
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)

    # Extract state dict
    if "model_state_dict" in ckpt:
        sd = ckpt["model_state_dict"]
    elif "backbone" in ckpt:
        sd = ckpt["backbone"]
    else:
        sd = ckpt

    # Check if padding is needed (old 7-dim → new 8-dim)
    decoder_key = "edge_decoder.0.weight"
    if decoder_key in sd and sd[decoder_key].shape[1] == 135:  # 2*64+7=135
        old_w = sd[decoder_key]
        new_w = torch.zeros(128, 136)  # 2*64+8=136
        new_w[:, :135] = old_w
        sd[decoder_key] = new_w

    backbone.load_state_dict(sd, strict=True)
    return backbone
