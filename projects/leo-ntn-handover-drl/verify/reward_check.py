"""MDP checkpoint: reward decomposition for random vs greedy strategies.

Runs 1 episode each and checks:
- No single reward item > 95% of total (F5 prevention)
- Greedy vs random total reward gap > 10%
"""

import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from simulator.environment import LEOSatHandoverEnv
from config import REWARD_DOMINATION_THRESHOLD


def run_episode(env, strategy: str, seed: int) -> dict:
    """Run one episode with given strategy. Returns metrics."""
    obs = env.reset(seed=seed)
    total_rewards = []
    decomp_accum = {"throughput_abs": 0, "load_abs": 0, "blocked_abs": 0, "handover_abs": 0}
    done = False

    while not done:
        valid = env.get_valid_actions()
        actions = np.zeros(env.num_ues, dtype=int)

        if strategy == "random":
            for ue in range(env.num_ues):
                v = np.where(valid[ue])[0]
                actions[ue] = np.random.choice(v) if len(v) > 0 else 0

        elif strategy == "greedy":
            # Greedy: each UE picks highest SINR visible satellite
            obs_full = env._get_obs()
            for ue in range(env.num_ues):
                sinr = obs_full[ue, :env.num_sats]  # first N features are SINR
                sinr[~valid[ue]] = -1
                v = np.where(valid[ue])[0]
                actions[ue] = v[sinr[v].argmax()] if len(v) > 0 else 0

        obs, rewards, done, info = env.step(actions)
        total_rewards.append(rewards.mean())

        rd = info["reward_decomposition"]
        for k in decomp_accum:
            decomp_accum[k] += rd.get(k, 0)

    n_steps = len(total_rewards)
    decomp_pct = {}
    total_abs = sum(decomp_accum.values()) + 1e-12
    for k, v in decomp_accum.items():
        decomp_pct[k.replace("_abs", "_pct")] = v / total_abs * 100

    return {
        "strategy": strategy,
        "seed": seed,
        "mean_reward": float(np.mean(total_rewards)),
        "total_reward": float(np.sum(total_rewards)),
        "decomposition_pct": decomp_pct,
        "steps": n_steps,
    }


def main():
    print("=== MDP Checkpoint: Reward Decomposition ===\n")
    env = LEOSatHandoverEnv(num_ues=15, seed=42)

    for strategy in ["random", "greedy"]:
        print(f"--- {strategy.upper()} strategy (seed=42) ---")
        result = run_episode(env, strategy, seed=42)
        dp = result["decomposition_pct"]
        print(f"  Mean reward: {result['mean_reward']:.4f}")
        print(f"  Steps: {result['steps']}")
        print(f"  Reward decomposition (% of |reward|):")
        print(f"    Throughput: {dp['throughput_pct']:.1f}%")
        print(f"    Load:       {dp['load_pct']:.1f}%")
        print(f"    Blocked:    {dp['blocked_pct']:.1f}%")
        print(f"    Handover:   {dp['handover_pct']:.1f}%")

        # Check domination
        for k, v in dp.items():
            if v > REWARD_DOMINATION_THRESHOLD * 100:
                print(f"  [FAIL] {k} dominates at {v:.1f}% (>{REWARD_DOMINATION_THRESHOLD*100:.0f}%)")
                print("  >>> STOP: Fix reward function before training DRL <<<")
                return False
        print(f"  [PASS] No single item >{REWARD_DOMINATION_THRESHOLD*100:.0f}%")

    # Strategy differentiation check
    random_r = run_episode(env, "random", seed=42)["total_reward"]
    greedy_r = run_episode(env, "greedy", seed=42)["total_reward"]
    gap = abs(greedy_r - random_r) / (abs(random_r) + 1e-12) * 100
    print(f"\nStrategy differentiation: random={random_r:.2f} greedy={greedy_r:.2f} gap={gap:.1f}%")
    if gap > 10:
        print("  [PASS] Greedy vs random gap > 10%")
    else:
        print("  [WARN] Gap < 10%, reward function may lack discrimination")

    print("\n=== MDP Checkpoint Complete ===")
    return True


if __name__ == "__main__":
    main()
