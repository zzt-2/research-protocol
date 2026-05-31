"""MDP Trial Run — Reward Sanity Check (Part A-checkpoint).

Runs random vs greedy policies, checks:
1. No single reward component >95% of total absolute reward
2. Greedy vs random total reward gap >10%
"""
import sys
sys.path.insert(0, "projects/leo-beam-hopping-gnn")

import numpy as np
from simulator.env import BHEnv


def run_episode(env, policy_fn, seed=42):
    """Run one episode, return total reward and per-step decomposition."""
    obs, info = env.reset(seed=seed)
    total_reward = 0.0
    total_throughput = 0.0
    total_fairness = 0.0
    total_interference = 0.0

    for t in range(env.T):
        action = policy_fn(obs, env)
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        total_throughput += info['reward_throughput']
        total_fairness += info['reward_fairness']
        total_interference += info['penalty_interference']
        if terminated:
            break

    return {
        'total': total_reward,
        'throughput': total_throughput,
        'fairness': total_fairness,
        'interference': total_interference,
    }


def random_policy(obs, env):
    """Random action: N-dim random scores."""
    return env._rng.standard_normal(env.N)


def greedy_policy(obs, env):
    """Per-slot greedy: select K beams with highest (demand + queue)."""
    # obs shape (N, 4): [demand_norm, queue_norm, channel_gain_norm, interf_norm]
    demand_queue = obs[:, 0] * env.config.demand_max_mbps + obs[:, 1] * env.config.queue_capacity_mbps
    scores = demand_queue.astype(np.float64)
    return scores


def optimal_greedy_policy(obs, env):
    """Enumerate C(N,K) combinations, pick best immediate served throughput."""
    from itertools import combinations
    from simulator.channel import compute_sinr
    total_demand = env.demands + env.queues
    best_served, best_active = -1, None
    for combo in combinations(range(env.N), env.K):
        active = np.array(combo)
        sinr = compute_sinr(env.gain_matrix, active, env.config, env.fading)
        cap = env.config.bandwidth_hz * np.log2(1.0 + sinr) / 1e6
        served = np.minimum(cap, total_demand[active]).sum()
        if served > best_served:
            best_served, best_active = served, combo
    # Return scores that select best_active via top-K
    scores = np.full(env.N, -1e9)
    for i in best_active:
        scores[i] = 1.0
    return scores


def main():
    print("=" * 60)
    print("MDP Trial Run — Reward Sanity Check")
    print("=" * 60)

    env = BHEnv(seed=42)

    # --- Run multiple episodes for statistical robustness ---
    N_EPS = 30

    random_results = []
    greedy_results = []
    opt_greedy_results = []

    for ep in range(N_EPS):
        seed = ep * 100
        r = run_episode(env, random_policy, seed=seed)
        random_results.append(r)
        g = run_episode(env, greedy_policy, seed=seed)
        greedy_results.append(g)
        o = run_episode(env, optimal_greedy_policy, seed=seed)
        opt_greedy_results.append(o)

    # Aggregate
    rand_totals = np.array([r['total'] for r in random_results])
    greedy_totals = np.array([g['total'] for g in greedy_results])
    opt_totals = np.array([o['total'] for o in opt_greedy_results])

    rand_throughput = np.array([r['throughput'] for r in random_results])
    rand_fairness = np.array([r['fairness'] for r in random_results])
    rand_interf = np.array([r['interference'] for r in random_results])

    greedy_throughput = np.array([g['throughput'] for g in greedy_results])
    greedy_fairness = np.array([g['fairness'] for g in greedy_results])
    greedy_interf = np.array([g['interference'] for g in greedy_results])

    opt_throughput = np.array([o['throughput'] for o in opt_greedy_results])
    opt_fairness = np.array([o['fairness'] for o in opt_greedy_results])
    opt_interf = np.array([o['interference'] for o in opt_greedy_results])

    print(f"\nEpisodes: {N_EPS}, T={env.T} slots, N={env.N} beams, K={env.K} active")
    print(f"Reward weights: α={env.config.reward_alpha}, β={env.config.reward_beta}, γ={env.config.reward_gamma}")

    print(f"\n--- Random Policy ---")
    print(f"  Total reward:      {rand_totals.mean():.4f} ± {rand_totals.std():.4f}")
    print(f"  Throughput (α·R):  {rand_throughput.mean():.4f}")
    print(f"  Fairness (β·R):    {rand_fairness.mean():.4f}")
    print(f"  Interference (γ·P):{rand_interf.mean():.4f}")

    print(f"\n--- Greedy (highest demand) ---")
    print(f"  Total reward:      {greedy_totals.mean():.4f} ± {greedy_totals.std():.4f}")
    print(f"  Throughput (α·R):  {greedy_throughput.mean():.4f}")
    print(f"  Fairness (β·R):    {greedy_fairness.mean():.4f}")
    print(f"  Interference (γ·P):{greedy_interf.mean():.4f}")

    print(f"\n--- Optimal Greedy (C(N,K) enumeration) ---")
    print(f"  Total reward:      {opt_totals.mean():.4f} ± {opt_totals.std():.4f}")
    print(f"  Throughput (α·R):  {opt_throughput.mean():.4f}")
    print(f"  Fairness (β·R):    {opt_fairness.mean():.4f}")
    print(f"  Interference (γ·P):{opt_interf.mean():.4f}")

    # --- Reward Decomposition ---
    print(f"\n--- Reward Decomposition (per-slot averages) ---")
    for name, results in [("Random", random_results), ("OptGreedy", opt_greedy_results)]:
        r_t = np.array([r['throughput'] for r in results]) / env.T
        r_f = np.array([r['fairness'] for r in results]) / env.T
        r_i = np.array([r['interference'] for r in results]) / env.T
        # Weighted contributions
        c_t = env.config.reward_alpha * np.abs(r_t).mean()
        c_f = env.config.reward_beta * np.abs(r_f).mean()
        c_i = env.config.reward_gamma * np.abs(r_i).mean()
        total_abs = c_t + c_f + c_i
        if total_abs > 0:
            pct_t = c_t / total_abs * 100
            pct_f = c_f / total_abs * 100
            pct_i = c_i / total_abs * 100
        else:
            pct_t = pct_f = pct_i = 0
        print(f"  [{name}]")
        print(f"    α·throughput: {c_t:.4f} ({pct_t:.1f}%)")
        print(f"    β·fairness:   {c_f:.4f} ({pct_f:.1f}%)")
        print(f"    γ·interf:     {c_i:.4f} ({pct_i:.1f}%)")

    # --- Checks ---
    print(f"\n{'=' * 60}")
    print("CHECKS")
    print(f"{'=' * 60}")

    all_pass = True

    # Check 1: No single component >95%
    for name, results in [("Random", random_results), ("OptGreedy", opt_greedy_results)]:
        r_t = np.array([r['throughput'] for r in results])
        r_f = np.array([r['fairness'] for r in results])
        r_i = np.array([r['interference'] for r in results])
        c_t = env.config.reward_alpha * np.abs(r_t).mean()
        c_f = env.config.reward_beta * np.abs(r_f).mean()
        c_i = env.config.reward_gamma * np.abs(r_i).mean()
        total_abs = c_t + c_f + c_i
        max_pct = max(c_t, c_f, c_i) / total_abs * 100 if total_abs > 0 else 0
        passed = max_pct < 95
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_pass = False
        print(f"  [{status}] {name}: max component = {max_pct:.1f}% (< 95% threshold)")

    # Check 2: Optimal greedy vs Random gap >10%
    rand_mean = rand_totals.mean()
    opt_mean = opt_totals.mean()
    if rand_mean != 0:
        gap_pct = abs(opt_mean - rand_mean) / abs(rand_mean) * 100
    else:
        gap_pct = 0
    passed = gap_pct > 10
    status = "PASS" if passed else "FAIL"
    if not passed:
        all_pass = False
    print(f"  [{status}] Strategy gap: opt_greedy({opt_mean:.4f}) vs random({rand_mean:.4f}) = {gap_pct:.1f}% (> 10% threshold)")

    # Check 3: Reward values are reasonable (not NaN/Inf, not zero)
    finite_check = np.isfinite(rand_totals).all() and np.isfinite(opt_totals).all()
    nonzero_check = rand_totals.mean() != 0 and opt_totals.mean() != 0
    status = "PASS" if (finite_check and nonzero_check) else "FAIL"
    if not (finite_check and nonzero_check):
        all_pass = False
    print(f"  [{status}] Rewards finite and non-zero")

    print(f"\n{'=' * 60}")
    if all_pass:
        print(">>> ALL CHECKS PASSED — MDP trial run OK")
    else:
        print(">>> SOME CHECKS FAILED — review reward function")
    print(f"{'=' * 60}")

    return 0 if all_pass else 1


if __name__ == "__main__":
    exit(main())
