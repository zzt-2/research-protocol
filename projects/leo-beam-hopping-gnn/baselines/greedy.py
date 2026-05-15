"""Greedy baselines: Random, DemandGreedy, OptGreedy (C(N,K) enumeration)."""
import sys
sys.path.insert(0, "projects/leo-beam-hopping-gnn")

import numpy as np
from itertools import combinations
from simulator.channel import compute_sinr
from simulator.env import BHEnv


def random_policy(env, obs):
    return env._rng.standard_normal(env.N)


def demand_greedy_policy(env, obs):
    dq = obs[:, 0] * env.config.demand_max_mbps + obs[:, 1] * env.config.queue_capacity_mbps
    return dq.astype(np.float64)


def opt_greedy_policy(env, obs):
    """Enumerate C(N,K), pick best immediate served throughput (per-slot optimal)."""
    total_demand = env.demands + env.queues
    best_served, best_active = -1.0, None
    for combo in combinations(range(env.N), env.K):
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


def run_baseline(policy_fn, n_episodes=30, seed_start=0):
    env = BHEnv()
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
    N_EP = 30
    print("=== Greedy Baselines ===")
    for name, fn in [("Random", random_policy),
                     ("DemandGreedy", demand_greedy_policy),
                     ("OptGreedy", opt_greedy_policy)]:
        results = run_baseline(fn, n_episodes=N_EP)
        summarize(results, name)
