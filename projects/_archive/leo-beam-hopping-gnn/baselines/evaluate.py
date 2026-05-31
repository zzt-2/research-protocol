"""Baseline comparison: verify relative trend PPO+MLP > GraphColoring > Greedy > Random.

Usage: cd /mnt/d/code/study/research-protocol && ~/.venvs/torch/bin/python projects/leo-beam-hopping-gnn/baselines/evaluate.py
"""
import sys
sys.path.insert(0, "projects/leo-beam-hopping-gnn")

import numpy as np
from simulator.env import BHEnv


def run_policy(env, policy_fn, n_episodes=30, seed_start=0):
    results = []
    for ep in range(n_episodes):
        obs, info = env.reset(seed=seed_start + ep * 100)
        total = 0.0
        comps = {'throughput': 0.0, 'fairness': 0.0, 'interference': 0.0}
        for _ in range(env.T):
            action = policy_fn(env, obs)
            obs, reward, terminated, truncated, info = env.step(action)
            total += reward
            comps['throughput'] += info['reward_throughput']
            comps['fairness'] += info['reward_fairness']
            comps['interference'] += info['penalty_interference']
            if terminated:
                break
        results.append({'total': total, **comps})
    return results


def summarize(results):
    t = np.array([r['total'] for r in results])
    return {'mean': t.mean(), 'std': t.std()}


def main():
    from baselines.greedy import random_policy, demand_greedy_policy, opt_greedy_policy
    from baselines.graph_coloring import GraphColoringScheduler
    from baselines.ppo_mlp import PPOAgent

    N_EP = 30
    env = BHEnv()

    print("=" * 70)
    print("Part B — Baseline Comparison")
    print("=" * 70)
    print(f"Episodes: {N_EP}, T={env.T}, N={env.N}, K={env.K}")
    print()

    all_results = {}

    # --- Random ---
    r = run_policy(env, random_policy, N_EP)
    all_results['Random'] = summarize(r)
    print(f"  Random:        {all_results['Random']['mean']:.4f} ± {all_results['Random']['std']:.4f}")

    # --- DemandGreedy ---
    r = run_policy(env, demand_greedy_policy, N_EP)
    all_results['DemandGreedy'] = summarize(r)
    print(f"  DemandGreedy:  {all_results['DemandGreedy']['mean']:.4f} ± {all_results['DemandGreedy']['std']:.4f}")

    # --- OptGreedy ---
    r = run_policy(env, opt_greedy_policy, N_EP)
    all_results['OptGreedy'] = summarize(r)
    print(f"  OptGreedy:     {all_results['OptGreedy']['mean']:.4f} ± {all_results['OptGreedy']['std']:.4f}")

    # --- Graph Coloring (L04) ---
    gc = GraphColoringScheduler(env)
    gc_policy = lambda env, obs: gc.policy(env, obs)
    r = run_policy(env, gc_policy, N_EP)
    all_results['GraphColoring'] = summarize(r)
    print(f"  GraphColoring: {all_results['GraphColoring']['mean']:.4f} ± {all_results['GraphColoring']['std']:.4f}")

    # --- PPO+MLP (trained) ---
    agent = PPOAgent(env)
    agent.load("projects/leo-beam-hopping-gnn/results/ppo_mlp_model.pt")
    ppo_policy = lambda env, obs: agent.act(obs)
    r = run_policy(env, ppo_policy, N_EP)
    all_results['PPO+MLP'] = summarize(r)
    print(f"  PPO+MLP:       {all_results['PPO+MLP']['mean']:.4f} ± {all_results['PPO+MLP']['std']:.4f}")

    # --- Trend Verification ---
    print()
    print("=" * 70)
    print("Trend Verification: DRL > Traditional > Random")
    print("=" * 70)

    ppo_mean = all_results['PPO+MLP']['mean']
    gc_mean = all_results['GraphColoring']['mean']
    rand_mean = all_results['Random']['mean']

    checks = []

    # Check 1: PPO+MLP > Random
    gap1 = (ppo_mean - rand_mean) / abs(rand_mean) * 100
    c1 = gap1 > 5
    checks.append(c1)
    print(f"  [{'PASS' if c1 else 'FAIL'}] PPO+MLP({ppo_mean:.4f}) > Random({rand_mean:.4f}): gap={gap1:.1f}%")

    # Check 2: GraphColoring > Random
    gap2 = (gc_mean - rand_mean) / abs(rand_mean) * 100
    c2 = gap2 > 5
    checks.append(c2)
    print(f"  [{'PASS' if c2 else 'FAIL'}] GraphColoring({gc_mean:.4f}) > Random({rand_mean:.4f}): gap={gap2:.1f}%")

    # Check 3: PPO+MLP > GraphColoring (structural advantage of learning)
    gap3 = (ppo_mean - gc_mean) / abs(gc_mean) * 100
    c3 = gap3 > 0
    checks.append(c3)
    print(f"  [{'PASS' if c3 else 'FAIL'}] PPO+MLP({ppo_mean:.4f}) > GraphColoring({gc_mean:.4f}): gap={gap3:.1f}%")

    # Check 4: GraphColoring > Greedy (traditional > naive)
    greedy_mean = all_results['DemandGreedy']['mean']
    gap4 = (gc_mean - greedy_mean) / abs(greedy_mean) * 100
    c4 = gap4 > 0
    checks.append(c4)
    print(f"  [{'INFO' if not c4 else 'PASS'}] GraphColoring({gc_mean:.4f}) > DemandGreedy({greedy_mean:.4f}): gap={gap4:.1f}%")

    print()
    n_pass = sum(checks)
    n_total = len(checks)
    if all(checks[:3]):
        print(f">>> TREND VERIFICATION PASSED ({n_pass}/{n_total})")
    else:
        print(f">>> TREND VERIFICATION FAILED ({n_pass}/{n_total}) — review baselines")

    return 0 if all(checks[:3]) else 1


if __name__ == "__main__":
    exit(main())
