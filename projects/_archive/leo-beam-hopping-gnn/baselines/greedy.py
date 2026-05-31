"""Greedy baselines: Random, DemandGreedy, OptGreedy, ApproxGreedy."""
import sys
sys.path.insert(0, "projects/leo-beam-hopping-gnn")

import numpy as np
from itertools import combinations
from math import comb
from simulator.channel import compute_sinr
from simulator.env import BHEnv
from simulator.config import SimConfig

MAX_COMBINATIONS = 1_000_000  # skip OptGreedy above this


def random_policy(env, obs):
    return env._rng.standard_normal(env.N)


def demand_greedy_policy(env, obs):
    dq = obs[:, 0] * env.config.demand_max_mbps + obs[:, 1] * env.config.queue_capacity_mbps
    return dq.astype(np.float64)


def opt_greedy_policy(env, obs):
    """Enumerate C(N,K), pick best immediate served throughput (per-slot optimal).

    Skipped when C(N,K) > MAX_COMBINATIONS (e.g. N>37).
    """
    n, k = env.N, env.K
    if comb(n, k) > MAX_COMBINATIONS:
        return approx_greedy_policy(env, obs)
    total_demand = env.demands + env.queues
    best_served, best_active = -1.0, None
    for combo in combinations(range(n), k):
        active = np.array(combo)
        sinr = compute_sinr(env.gain_matrix, active, env.config, env.fading)
        cap = env.config.bandwidth_hz * np.log2(1.0 + sinr) / 1e6
        served = np.minimum(cap, total_demand[active]).sum()
        if served > best_served:
            best_served, best_active = served, combo
    scores = np.full(env.N, -1e9)
    for i in best_active:
        scores[i] = 1.0
    return scores


def approx_greedy_policy(env, obs):
    """Greedy beam-by-beam selection maximizing marginal throughput.

    Scalable alternative to OptGreedy for large N. Each step picks the beam
    that maximizes total served throughput given already-selected beams.
    """
    total_demand = env.demands + env.queues
    selected = []
    remaining = set(range(env.N))

    for _ in range(env.K):
        best_beam, best_served = -1, -1.0
        for b in remaining:
            trial = selected + [b]
            active = np.array(trial)
            sinr = compute_sinr(env.gain_matrix, active, env.config, env.fading)
            cap = env.config.bandwidth_hz * np.log2(1.0 + sinr) / 1e6
            served = np.minimum(cap, total_demand[active]).sum()
            if served > best_served:
                best_served = served
                best_beam = b
        selected.append(best_beam)
        remaining.discard(best_beam)

    scores = np.full(env.N, -1e9)
    for i in selected:
        scores[i] = 1.0
    return scores


def run_episode(env, policy_fn, seed=42):
    obs, info = env.reset(seed=seed)
    total_reward = 0.0
    components = {'throughput': 0.0, 'fairness': 0.0, 'interference': 0.0}
    for _ in range(env.T):
        action = policy_fn(env, obs)
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        components['throughput'] += info['reward_throughput']
        components['fairness'] += info['reward_fairness']
        components['interference'] += info['penalty_interference']
        if terminated:
            break
    return {'total': total_reward, **components}


def run_baseline(policy_fn, n_episodes=30, seed_start=0, config=None):
    env = BHEnv(config=config)
    results = []
    for ep in range(n_episodes):
        r = run_episode(env, policy_fn, seed=seed_start + ep * 100)
        results.append(r)
    return results


def summarize(results, name=""):
    totals = np.array([r['total'] for r in results])
    tp = np.array([r['throughput'] for r in results])
    fa = np.array([r['fairness'] for r in results])
    intf = np.array([r['interference'] for r in results])
    print(f"  [{name}] total={totals.mean():.4f}±{totals.std():.4f} "
          f"tp={tp.mean():.4f} fair={fa.mean():.4f} intf={intf.mean():.4f}")
    return {'total_mean': totals.mean(), 'total_std': totals.std()}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--scale', default='small', choices=['small', 'medium', 'large'])
    args = parser.parse_args()

    cfg = SimConfig.preset(args.scale)
    N_EP = 30
    print(f"=== Greedy Baselines (N={cfg.n_beams}, K={cfg.k_active}) ===")
    for name, fn in [("Random", random_policy),
                     ("DemandGreedy", demand_greedy_policy),
                     ("ApproxGreedy", approx_greedy_policy),
                     ("OptGreedy", opt_greedy_policy)]:
        results = run_baseline(fn, n_episodes=N_EP, config=cfg)
        summarize(results, name)
