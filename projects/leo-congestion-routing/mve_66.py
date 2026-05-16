#!/usr/bin/env python3
"""MVE-2: 66-node Walker delta + 8% link failures.

Key question: Does GNN beat ECMP when link failures break equal-cost paths?
All methods evaluated on the SAME scenarios (same failures + same traffic).
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import networkx as nx
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Categorical

from mve_env import Config, RoutingEnv, build_topology
from mve_train import GNNActorCritic, MLPActorCritic, compute_gae


# ---------------------------------------------------------------------------
# Environment with link failures
# ---------------------------------------------------------------------------

class RoutingEnv66(RoutingEnv):
    """66-node env with random link failures per episode."""

    def __init__(self, cfg=None, failure_rate=0.08):
        super().__init__(cfg)
        self.failure_rate = failure_rate
        self._base_G = self.G.copy()

    def reset(self, seed=None):
        rng = np.random.default_rng(seed)

        # Restore base topology, then apply failures
        self.G = self._base_G.copy()
        edges = list(self.G.edges())
        n_fail = max(1, int(len(edges) * self.failure_rate))
        for idx in rng.choice(len(edges), n_fail, replace=False):
            self.G.remove_edge(*edges[idx])

        # Rebuild edge structures
        srcs, dsts, types = [], [], []
        for u, v, d in self.G.edges(data=True):
            srcs += [u, v]; dsts += [v, u]
            types += [d['etype'], d['etype']]
        self.edge_index = np.array([srcs, dsts], dtype=np.int64) if srcs else np.zeros((2, 0), dtype=np.int64)
        self.edge_types = np.array(types, dtype=np.float32) if types else np.zeros(0, dtype=np.float32)

        self.adj = {n: sorted(self.G.neighbors(n)) for n in self.G.nodes()}
        self._path_cache = {}

        # Reset link loads + generate flows
        self._init_state()
        self.flows = self._generate_flows(rng)
        return self._get_obs(), {}


# ---------------------------------------------------------------------------
# Training (reuses models from mve_train)
# ---------------------------------------------------------------------------

def train_model(model, cfg, n_episodes=100, seed=0, failure_rate=0.08, lr=3e-4):
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    env = RoutingEnv66(cfg, failure_rate=failure_rate)
    mlus = []

    for ep in range(n_episodes):
        # Collect rollout
        obs_list, actions, rewards, values, logprobs_list = [], [], [], [], []
        obs, _ = env.reset(seed=seed * 10000 + ep)
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
            logprobs_list.append(logprob)
            obs = next_obs
            done = terminated or truncated

        advantages, returns = compute_gae(rewards, values)

        # PPO update
        for _ in range(4):
            for t in range(len(obs_list)):
                logits_t, value_t = model(obs_list[t])
                dist_t = Categorical(logits=logits_t)
                new_lp = dist_t.log_prob(torch.tensor(actions[t]))
                entropy = dist_t.entropy()

                ratio = (new_lp - logprobs_list[t]).exp()
                adv = torch.tensor(advantages[t], dtype=torch.float32)
                ret = torch.tensor(returns[t], dtype=torch.float32)

                surr1 = ratio * adv
                surr2 = torch.clamp(ratio, 1 - 0.2, 1 + 0.2) * adv
                loss = -torch.min(surr1, surr2) + 0.5 * F.mse_loss(value_t, ret) - 0.01 * entropy

                optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                optimizer.step()

        final_mlu = info.get("final_mlu", info["mlu"])
        mlus.append(final_mlu)
        if (ep + 1) % 50 == 0:
            recent = mlus[-50:]
            print(f"  Ep {ep+1:4d}: MLU = {np.mean(recent):.4f} +/- {np.std(recent):.4f}")

    return mlus


# ---------------------------------------------------------------------------
# Fair evaluation: all methods on SAME scenarios
# ---------------------------------------------------------------------------

def _run_greedy(model, env, seed):
    """Run model with greedy policy, return final MLU."""
    obs, _ = env.reset(seed=seed)
    for t in range(len(env.flows)):
        if obs["n_valid"] == 0:
            return None  # unreachable flow
        with torch.no_grad():
            logits, _ = model(obs)
            a = logits.argmax().item()
        obs, _, done, _, info = env.step(a)
        if done:
            break
    return info.get("final_mlu", info["mlu"])


def _run_sp(env, seed):
    obs, _ = env.reset(seed=seed)
    for t in range(len(env.flows)):
        if obs["n_valid"] == 0:
            return None
        obs, _, done, _, info = env.step(0)
        if done:
            break
    return info.get("final_mlu", info["mlu"])


def _run_ecmp(env, seed):
    obs, _ = env.reset(seed=seed)
    for t in range(len(env.flows)):
        paths = obs["paths"]
        if not paths:
            return None
        min_len = min(len(p) for p in paths)
        equal = [j for j, p in enumerate(paths) if len(p) == min_len]
        a = equal[t % len(equal)] if equal else 0
        obs, _, done, _, info = env.step(a)
        if done:
            break
    return info.get("final_mlu", info["mlu"])


def eval_fair(cfg, gnn_model, mlp_model, n_eval=20, seed_offset=500000, failure_rate=0.08):
    """Evaluate ALL methods on the SAME failure patterns + traffic."""
    results = {"gnn": [], "mlp": [], "sp": [], "ecmp": []}

    for i in range(n_eval):
        seed = seed_offset + i

        # Each method gets its own env but same seed → same failures + traffic
        gnn_mlu = _run_greedy(gnn_model, RoutingEnv66(cfg, failure_rate), seed)
        mlp_mlu = _run_greedy(mlp_model, RoutingEnv66(cfg, failure_rate), seed)
        sp_mlu = _run_sp(RoutingEnv66(cfg, failure_rate), seed)
        ecmp_mlu = _run_ecmp(RoutingEnv66(cfg, failure_rate), seed)

        # Only count scenarios where all methods could route
        if all(v is not None for v in [gnn_mlu, mlp_mlu, sp_mlu, ecmp_mlu]):
            results["gnn"].append(gnn_mlu)
            results["mlp"].append(mlp_mlu)
            results["sp"].append(sp_mlu)
            results["ecmp"].append(ecmp_mlu)

    return {k: (np.mean(v), np.std(v)) for k, v in results.items() if v}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    cfg = Config(n_planes=6, n_sats=11, n_flows=40, n_heavy=10)
    failure_rate = 0.08
    n_seeds = 2
    n_episodes = 150
    n_eval = 20

    print("=" * 60)
    print("MVE-2: 66 nodes + link failures")
    print("=" * 60)
    print(f"Topology: Walker {cfg.n_planes}x{cfg.n_sats} = {cfg.n_nodes} nodes")
    print(f"Link failures: {failure_rate*100:.0f}% per episode")
    print(f"Flows: {cfg.n_flows} ({cfg.n_heavy} heavy + {cfg.n_flows - cfg.n_heavy} light)")
    print()

    # Also run 24-node without failures for reference
    print("--- 24-node reference (no failures) ---")
    cfg24 = Config()
    from mve_env import eval_baseline
    sp24, _ = eval_baseline(cfg24, "sp", n_eval=n_eval, seed_offset=500000)
    ecmp24, _ = eval_baseline(cfg24, "ecmp", n_eval=n_eval, seed_offset=500000)
    print(f"SP:   {sp24:.4f}")
    print(f"ECMP: {ecmp24:.4f}")
    print()

    # 66-node baselines (with failures)
    print("--- 66-node baselines (with failures) ---")
    sp_mlus, ecmp_mlus = [], []
    for i in range(n_eval):
        seed = 600000 + i
        sp_m = _run_sp(RoutingEnv66(cfg, failure_rate), seed)
        ecmp_m = _run_ecmp(RoutingEnv66(cfg, failure_rate), seed)
        if sp_m is not None: sp_mlus.append(sp_m)
        if ecmp_m is not None: ecmp_mlus.append(ecmp_m)
    print(f"SP:   {np.mean(sp_mlus):.4f} +/- {np.std(sp_mlus):.4f}")
    print(f"ECMP: {np.mean(ecmp_mlus):.4f} +/- {np.std(ecmp_mlus):.4f}")
    print()

    # GNN training
    print("--- GNN Training (66-node + failures) ---")
    gnn_models = []
    for seed in range(n_seeds):
        print(f"[Seed {seed}]")
        model = GNNActorCritic(cfg)
        train_model(model, cfg, n_episodes=n_episodes, seed=seed, failure_rate=failure_rate)
        gnn_models.append(model)
    print()

    # MLP training
    print("--- MLP Training (66-node + failures) ---")
    mlp_models = []
    for seed in range(n_seeds):
        print(f"[Seed {seed}]")
        model = MLPActorCritic(cfg)
        train_model(model, cfg, n_episodes=n_episodes, seed=seed, failure_rate=failure_rate)
        mlp_models.append(model)
    print()

    # Fair evaluation: best GNN vs best MLP vs baselines
    print("=" * 60)
    print("FAIR COMPARISON (same scenarios)")
    print("=" * 60)

    best_gnn = min(gnn_models, key=lambda m: _quick_eval(m, cfg, failure_rate))
    best_mlp = min(mlp_models, key=lambda m: _quick_eval(m, cfg, failure_rate))

    results = eval_fair(cfg, best_gnn, best_mlp, n_eval=n_eval, seed_offset=700000,
                        failure_rate=failure_rate)

    print(f"GNN:  {results['gnn'][0]:.4f} +/- {results['gnn'][1]:.4f}")
    print(f"MLP:  {results['mlp'][0]:.4f} +/- {results['mlp'][1]:.4f}")
    print(f"SP:   {results['sp'][0]:.4f} +/- {results['sp'][1]:.4f}")
    print(f"ECMP: {results['ecmp'][0]:.4f} +/- {results['ecmp'][1]:.4f}")

    gnn_m = results["gnn"][0]
    mlp_m = results["mlp"][0]
    ecmp_m = results["ecmp"][0]
    sp_m = results["sp"][0]

    print()
    print(f"GNN/MLP:  {gnn_m/mlp_m:.4f}")
    print(f"GNN/ECMP: {gnn_m/ecmp_m:.4f}")
    print(f"GNN/SP:   {gnn_m/sp_m:.4f}")

    print()
    if gnn_m / ecmp_m <= 0.95:
        print("RESULT: GNN beats ECMP → direction validated")
    elif gnn_m / ecmp_m > 1.05:
        print("RESULT: ECMP beats GNN → direction should be archived")
    else:
        print("RESULT: GNN ≈ ECMP → inconclusive")


def _quick_eval(model, cfg, failure_rate, n=5):
    """Quick eval to select best model per seed."""
    env = RoutingEnv66(cfg, failure_rate)
    mlus = []
    for i in range(n):
        obs, _ = env.reset(seed=800000 + i)
        done = False
        while not done:
            if obs["n_valid"] == 0:
                break
            with torch.no_grad():
                logits, _ = model(obs)
                a = logits.argmax().item()
            obs, _, done, _, info = env.step(a)
        if done:
            mlus.append(info.get("final_mlu", info["mlu"]))
    return np.mean(mlus) if mlus else float("inf")


if __name__ == "__main__":
    main()
