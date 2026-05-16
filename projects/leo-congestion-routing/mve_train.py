#!/usr/bin/env python3
"""MVE: GNN vs MLP for congestion-aware routing in LEO satellite networks.

Hypothesis: Under non-uniform traffic, GNN message passing over link load info
achieves >=10% lower MLU than MLP with only local (1-hop) load info.

Pass:  GNN MLU <= 0.9 * MLP MLU  → Go
Fail:  GNN MLU > 0.95 * MLP MLU  → Kill
"""

import sys
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Categorical
from torch_geometric.nn import GATConv

from mve_env import Config, RoutingEnv, eval_baseline


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class GNNActorCritic(nn.Module):
    """GAT-based actor-critic: aggregates global load info via message passing."""

    def __init__(self, cfg, hidden=32, heads=4):
        super().__init__()
        self.K = cfg.k_paths
        h_dim = hidden * heads

        self.conv1 = GATConv(5, hidden, heads=heads, edge_dim=2)
        self.conv2 = GATConv(h_dim, hidden, heads=heads, edge_dim=2)

        self.path_head = nn.Sequential(
            nn.Linear(h_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
        )
        self.value_head = nn.Sequential(
            nn.Linear(h_dim * 2, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
        )

    def forward(self, obs):
        x = torch.as_tensor(obs["node_feat"], dtype=torch.float32)
        ei = torch.as_tensor(obs["edge_index"], dtype=torch.long)
        ea = torch.as_tensor(obs["edge_feat"], dtype=torch.float32)

        h = F.elu(self.conv1(x, ei, ea))
        h = F.elu(self.conv2(h, ei, ea))

        src, dst, _ = obs["flow"]
        paths = obs["paths"]
        n_valid = obs["n_valid"]

        # Score each candidate path using node embeddings along the path
        scores = []
        for path in paths:
            idx = torch.tensor(path, dtype=torch.long)
            path_emb = h[idx].mean(dim=0)
            scores.append(self.path_head(path_emb).squeeze())

        # Pad invalid actions with large negative score
        while len(scores) < self.K:
            scores.append(torch.tensor(-1e9, dtype=torch.float32))

        logits = torch.stack(scores[:self.K])

        # Critic: value from src + dst embeddings
        value = self.value_head(torch.cat([h[src], h[dst]])).squeeze()
        return logits, value


class MLPActorCritic(nn.Module):
    """MLP actor-critic: uses only local (1-hop) load information."""

    def __init__(self, cfg, hidden=128):
        super().__init__()
        self.K = cfg.k_paths
        # Input: src_feat(5) + dst_feat(5) + src_nbr_loads(4) + dst_nbr_loads(4)
        #        + demand(1) + path_lens(K) = 19 + K
        inp = 5 + 5 + 4 + 4 + 1 + self.K

        self.backbone = nn.Sequential(
            nn.Linear(inp, hidden),
            nn.ReLU(),
            nn.Linear(hidden, hidden),
            nn.ReLU(),
        )
        self.actor = nn.Linear(hidden, self.K)
        self.critic = nn.Linear(hidden, 1)

    def forward(self, obs):
        x = torch.as_tensor(obs["mlp_feat"], dtype=torch.float32)
        h = self.backbone(x)

        logits = self.actor(h)

        # Mask invalid actions
        n_valid = obs["n_valid"]
        mask = torch.full_like(logits, -1e9)
        mask[:n_valid] = logits[:n_valid]

        value = self.critic(h).squeeze()
        return mask, value


# ---------------------------------------------------------------------------
# PPO
# ---------------------------------------------------------------------------

def compute_gae(rewards, values, gamma=0.99, lam=0.95):
    """Generalized Advantage Estimation."""
    n = len(rewards)
    advantages = np.zeros(n, dtype=np.float32)
    returns = np.zeros(n, dtype=np.float32)

    gae = 0.0
    for t in reversed(range(n)):
        if t == n - 1:
            delta = rewards[t] - values[t]
        else:
            delta = rewards[t] + gamma * values[t + 1] - values[t]
        gae = delta + gamma * lam * gae
        advantages[t] = gae
        returns[t] = gae + values[t]

    # Normalize
    adv_std = advantages.std()
    if adv_std > 1e-8:
        advantages = (advantages - advantages.mean()) / adv_std

    return advantages, returns


def collect_rollout(model, env, seed):
    """Collect one episode of experience."""
    obs_list, actions, rewards, values, logprobs = [], [], [], [], []

    obs, _ = env.reset(seed=seed)
    done = False
    while not done:
        with torch.no_grad():
            logits, value = model(obs)
            dist = Categorical(logits=logits)
            action = dist.sample()
            logprob = dist.log_prob(action).item()

        next_obs, reward, terminated, truncated, info = env.step(action.item())
        obs_list.append(obs)
        actions.append(action.item())
        rewards.append(reward)
        values.append(value.item())
        logprobs.append(logprob)

        obs = next_obs
        done = terminated or truncated

    advantages, returns = compute_gae(rewards, values)
    return obs_list, actions, rewards, values, logprobs, advantages, returns, info


def ppo_update(model, optimizer, obs_list, actions, logprobs, advantages, returns,
               n_epochs=4, clip_eps=0.2, entropy_coeff=0.01):
    """PPO clipped surrogate update."""
    for _ in range(n_epochs):
        for t in range(len(obs_list)):
            logits, value = model(obs_list[t])
            dist = Categorical(logits=logits)
            new_logprob = dist.log_prob(torch.tensor(actions[t]))
            entropy = dist.entropy()

            ratio = (new_logprob - logprobs[t]).exp()
            adv = torch.tensor(advantages[t], dtype=torch.float32)
            ret = torch.tensor(returns[t], dtype=torch.float32)

            surr1 = ratio * adv
            surr2 = torch.clamp(ratio, 1 - clip_eps, 1 + clip_eps) * adv
            actor_loss = -torch.min(surr1, surr2)

            critic_loss = F.mse_loss(value, ret)

            loss = actor_loss + 0.5 * critic_loss - entropy_coeff * entropy

            optimizer.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()


# ---------------------------------------------------------------------------
# Training & Evaluation
# ---------------------------------------------------------------------------

def train(model, cfg, n_episodes=300, seed=0, lr=3e-4):
    """Train model with PPO, return per-episode final MLU."""
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    env = RoutingEnv(cfg)
    mlus = []

    for ep in range(n_episodes):
        (obs_list, actions, rewards, values, logprobs,
         advantages, returns, info) = collect_rollout(model, env, seed=seed * 10000 + ep)

        ppo_update(model, optimizer, obs_list, actions, logprobs,
                   advantages, returns)

        final_mlu = info.get("final_mlu", info["mlu"])
        mlus.append(final_mlu)

        if (ep + 1) % 50 == 0:
            recent = mlus[-50:]
            print(f"  Ep {ep+1:4d}: MLU = {np.mean(recent):.4f} ± {np.std(recent):.4f}")

    return mlus


def evaluate(model, cfg, n_eval=20, seed_offset=200000):
    """Evaluate trained model (greedy policy) on fresh scenarios."""
    env = RoutingEnv(cfg)
    mlus = []

    for i in range(n_eval):
        obs, _ = env.reset(seed=seed_offset + i)
        done = False
        while not done:
            with torch.no_grad():
                logits, _ = model(obs)
                action = logits.argmax().item()
            obs, _, terminated, truncated, info = env.step(action)
            done = terminated or truncated
        mlus.append(info.get("final_mlu", info["mlu"]))

    return np.mean(mlus), np.std(mlus)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    cfg = Config()
    n_seeds = 3
    n_episodes = 300
    n_eval = 20

    print("=" * 60)
    print("MVE: GNN vs MLP for Congestion-Aware LEO Routing")
    print("=" * 60)
    print(f"Topology: Walker delta {cfg.n_planes}x{cfg.n_sats} = {cfg.n_nodes} nodes")
    print(f"Flows: {cfg.n_flows} ({cfg.n_heavy} heavy + {cfg.n_flows - cfg.n_heavy} light)")
    print(f"Capacity: {cfg.capacity} Gbps/link, K={cfg.k_paths} candidate paths")
    print()

    # 1. Baselines
    print("--- Baselines ---")
    sp_mean, sp_std = eval_baseline(cfg, "sp", n_eval=n_eval, seed_offset=100000)
    ecmp_mean, ecmp_std = eval_baseline(cfg, "ecmp", n_eval=n_eval, seed_offset=100000)
    print(f"Shortest-path: MLU = {sp_mean:.4f} ± {sp_std:.4f}")
    print(f"ECMP:          MLU = {ecmp_mean:.4f} ± {ecmp_std:.4f}")
    print()

    # 2. GNN training
    print("--- GNN Training ---")
    gnn_evals = []
    for seed in range(n_seeds):
        print(f"[Seed {seed}]")
        model = GNNActorCritic(cfg)
        train(model, cfg, n_episodes=n_episodes, seed=seed)
        mean, std = evaluate(model, cfg, n_eval=n_eval, seed_offset=200000 + seed * 1000)
        gnn_evals.append(mean)
        print(f"  → Eval: {mean:.4f} ± {std:.4f}")
    print()

    # 3. MLP training
    print("--- MLP Training ---")
    mlp_evals = []
    for seed in range(n_seeds):
        print(f"[Seed {seed}]")
        model = MLPActorCritic(cfg)
        train(model, cfg, n_episodes=n_episodes, seed=seed)
        mean, std = evaluate(model, cfg, n_eval=n_eval, seed_offset=300000 + seed * 1000)
        mlp_evals.append(mean)
        print(f"  → Eval: {mean:.4f} ± {std:.4f}")
    print()

    # 4. Verdict
    print("=" * 60)
    print("VERDICT")
    print("=" * 60)
    gnn_avg = np.mean(gnn_evals)
    gnn_std = np.std(gnn_evals)
    mlp_avg = np.mean(mlp_evals)
    mlp_std = np.std(mlp_evals)
    ratio = gnn_avg / mlp_avg if mlp_avg > 0 else float("inf")

    print(f"GNN  MLU: {gnn_avg:.4f} ± {gnn_std:.4f}")
    print(f"MLP  MLU: {mlp_avg:.4f} ± {mlp_std:.4f}")
    print(f"SP   MLU: {sp_mean:.4f}")
    print(f"ECMP MLU: {ecmp_mean:.4f}")
    print(f"GNN/MLP ratio: {ratio:.4f}")
    print()

    if ratio <= 0.90:
        print("PASS: GNN achieves >=10% lower MLU → GO")
    elif ratio > 0.95:
        print("FAIL: GNN has no significant advantage → KILL (archive project)")
    else:
        print("CONDITIONAL: GNN advantage marginal (5-10%) → investigate further")


if __name__ == "__main__":
    main()
