"""Channel-Conditioned Attention Network (CCAN) Actor + Critic for RIS phase optimization.

Architecture (per data-flow.md):
  Actor:
    1. Input: obs (B, 2600) → reshape (B, N, 2M+2K+2)
    2. Channel Encoder: Linear(26,64) → MultiHeadAttention(4,64) → FFN(64,128,64)
    3. Phase Decoder: Shared MLP (66→128→1) + tanh → action (B, N)

  Critic (Amendment 1):
    1. Own CCAN encoder → mean-pool → (B, d_model)
    2. concat(embed, action) → (B, d_model+N) → twin Q-heads

Ablation support:
  - A1 (w/o attention): skip attention layer, use per-element MLP only
  - A2 (w/o sharing): per-element independent decoders (no weight sharing)
  - A3 (w/o encoder): skip encoder entirely, raw features → decoder
"""

import torch
import torch.nn as nn


class CCANActor(nn.Module):
    def __init__(
        self,
        obs_dim: int,
        act_dim: int,
        N: int,
        M: int,
        K: int,
        d_model: int = 64,
        n_heads: int = 4,
        use_attention: bool = True,
        use_sharing: bool = True,
        use_encoder: bool = True,
    ):
        super().__init__()
        self.N = N
        self.M = M
        self.K = K
        self.d_model = d_model
        self.use_attention = use_attention
        self.use_sharing = use_sharing
        self.use_encoder = use_encoder

        self.elem_feat_dim = 2 * M + 2 * K + 2  # 26 for M=8, K=4
        assert obs_dim == 2 * N * M + 2 * N * K + 2 * N
        assert act_dim == N

        if use_encoder:
            self.input_proj = nn.Linear(self.elem_feat_dim, d_model)

            if use_attention:
                self.attention = nn.MultiheadAttention(
                    d_model, n_heads, batch_first=True
                )
                self.ln1 = nn.LayerNorm(d_model)

            self.ffn = nn.Sequential(
                nn.Linear(d_model, d_model * 2),
                nn.ReLU(),
                nn.Linear(d_model * 2, d_model),
            )
            self.ln2 = nn.LayerNorm(d_model)
            dec_input_dim = d_model + 2
        else:
            dec_input_dim = self.elem_feat_dim

        if use_sharing:
            self.decoder = nn.Sequential(
                nn.Linear(dec_input_dim, 128),
                nn.ReLU(),
                nn.Linear(128, 1),
                nn.Tanh(),
            )
        else:
            self.per_element_decoders = nn.ModuleList([
                nn.Sequential(
                    nn.Linear(dec_input_dim, 128),
                    nn.ReLU(),
                    nn.Linear(128, 1),
                    nn.Tanh(),
                )
                for _ in range(N)
            ])

    def _reshape_obs(self, obs: torch.Tensor) -> torch.Tensor:
        B = obs.shape[0]
        NM = self.N * self.M
        NK = self.N * self.K

        re_h1 = obs[:, :NM].reshape(B, self.N, self.M)
        im_h1 = obs[:, NM : 2 * NM].reshape(B, self.N, self.M)
        re_h2 = obs[:, 2 * NM : 2 * NM + NK].reshape(B, self.N, self.K)
        im_h2 = obs[:, 2 * NM + NK : 2 * NM + 2 * NK].reshape(B, self.N, self.K)
        cos_theta = obs[:, 2 * NM + 2 * NK : 2 * NM + 2 * NK + self.N].reshape(
            B, self.N, 1
        )
        sin_theta = obs[
            :, 2 * NM + 2 * NK + self.N : 2 * NM + 2 * NK + 2 * self.N
        ].reshape(B, self.N, 1)

        return torch.cat(
            [re_h1, im_h1, re_h2, im_h2, cos_theta, sin_theta], dim=-1
        )

    def forward(self, obs: torch.Tensor) -> torch.Tensor:
        x = self._reshape_obs(obs)  # (B, N, 26)
        cos_sin = x[:, :, -2:]  # (B, N, 2)

        if self.use_encoder:
            h = self.input_proj(x)  # (B, N, d_model)

            if self.use_attention:
                attn_out, _ = self.attention(h, h, h)
                h = self.ln1(h + attn_out)

            h = self.ln2(h + self.ffn(h))  # (B, N, d_model)
            dec_input = torch.cat([h, cos_sin], dim=-1)  # (B, N, d_model+2)
        else:
            dec_input = x  # (B, N, 26)

        if self.use_sharing:
            action = self.decoder(dec_input)  # (B, N, 1)
            return action.squeeze(-1)  # (B, N)
        else:
            actions = []
            for i in range(self.N):
                actions.append(self.per_element_decoders[i](dec_input[:, i, :]))
            return torch.cat(actions, dim=-1)  # (B, N)


class CCANCritic(nn.Module):
    """Channel-aware Twin Critic: own CCAN encoder + mean-pool + twin Q-heads.

    Amendment 1: replaces flat MLP Critic (2700→400 compression ratio 6.75:1).
    New input: d_model(64) + act_dim(N) = 164, compression 2.4:1.
    """

    def __init__(
        self,
        obs_dim: int,
        act_dim: int,
        N: int,
        M: int,
        K: int,
        d_model: int = 64,
        n_heads: int = 4,
        hidden: tuple = (400, 300),
        use_attention: bool = True,
        use_encoder: bool = True,
    ):
        super().__init__()
        self.N = N
        self.M = M
        self.K = K
        self.d_model = d_model
        self.use_attention = use_attention
        self.use_encoder = use_encoder
        self.elem_feat_dim = 2 * M + 2 * K + 2

        if use_encoder:
            self.input_proj = nn.Linear(self.elem_feat_dim, d_model)
            if use_attention:
                self.attention = nn.MultiheadAttention(
                    d_model, n_heads, batch_first=True
                )
                self.ln1 = nn.LayerNorm(d_model)
            self.ffn = nn.Sequential(
                nn.Linear(d_model, d_model * 2),
                nn.ReLU(),
                nn.Linear(d_model * 2, d_model),
            )
            self.ln2 = nn.LayerNorm(d_model)
            q_input_dim = d_model
        else:
            q_input_dim = self.elem_feat_dim

        q_input_dim += act_dim  # concat channel_embed + action

        self.q1 = nn.Sequential(
            nn.Linear(q_input_dim, hidden[0]),
            nn.ReLU(),
            nn.Linear(hidden[0], hidden[1]),
            nn.ReLU(),
            nn.Linear(hidden[1], 1),
        )
        self.q2 = nn.Sequential(
            nn.Linear(q_input_dim, hidden[0]),
            nn.ReLU(),
            nn.Linear(hidden[0], hidden[1]),
            nn.ReLU(),
            nn.Linear(hidden[1], 1),
        )

    def _reshape_obs(self, obs: torch.Tensor) -> torch.Tensor:
        B = obs.shape[0]
        NM = self.N * self.M
        NK = self.N * self.K
        re_h1 = obs[:, :NM].reshape(B, self.N, self.M)
        im_h1 = obs[:, NM : 2 * NM].reshape(B, self.N, self.M)
        re_h2 = obs[:, 2 * NM : 2 * NM + NK].reshape(B, self.N, self.K)
        im_h2 = obs[:, 2 * NM + NK : 2 * NM + 2 * NK].reshape(B, self.N, self.K)
        cos_theta = obs[
            :, 2 * NM + 2 * NK : 2 * NM + 2 * NK + self.N
        ].reshape(B, self.N, 1)
        sin_theta = obs[
            :, 2 * NM + 2 * NK + self.N : 2 * NM + 2 * NK + 2 * self.N
        ].reshape(B, self.N, 1)
        return torch.cat(
            [re_h1, im_h1, re_h2, im_h2, cos_theta, sin_theta], dim=-1
        )

    def _encode(self, obs: torch.Tensor) -> torch.Tensor:
        x = self._reshape_obs(obs)
        if self.use_encoder:
            h = self.input_proj(x)
            if self.use_attention:
                attn_out, _ = self.attention(h, h, h)
                h = self.ln1(h + attn_out)
            h = self.ln2(h + self.ffn(h))
            return h.mean(dim=1)  # (B, d_model)
        else:
            return x.mean(dim=1)  # (B, elem_feat_dim)

    def forward(self, obs: torch.Tensor, act: torch.Tensor):
        embed = self._encode(obs)
        x = torch.cat([embed, act], dim=-1)
        return self.q1(x), self.q2(x)

    def q1_forward(self, obs: torch.Tensor, act: torch.Tensor) -> torch.Tensor:
        embed = self._encode(obs)
        x = torch.cat([embed, act], dim=-1)
        return self.q1(x)
