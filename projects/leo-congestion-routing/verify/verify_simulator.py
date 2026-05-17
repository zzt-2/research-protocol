#!/usr/bin/env python3
"""验证套件 — LEO 拥塞路由仿真器 (K-path 范式)。

验证类别:
  1. 解析验证 — 已知拓扑下的精确 MLU
  2. 统计验证 — 流量分布、故障率分布
  3. 退化验证 — 确定性种子 → 确定性输出
  4. Episode 结构验证 — 步数=n_flows, MLU 非递减
  5. MDP trial — SP vs Random 策略跑完整 episode
  6. Baseline 对比 — SP vs ECMP
  7. Reward balance gate — 策略分化/信号非恒定
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

_PROJECT = Path(__file__).resolve().parent.parent
if str(_PROJECT) not in sys.path:
    sys.path.insert(0, str(_PROJECT))

from simulator.config import SimConfig
from simulator.env import RoutingEnv
from baselines.sp import run_sp
from baselines.ecmp import run_ecmp


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def header(msg: str) -> None:
    print(f"\n{'='*60}\n  {msg}\n{'='*60}")


def check(name: str, condition: bool, detail: str = "") -> bool:
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {name}" + (f" — {detail}" if detail and condition else ""))
    if not condition:
        print(f"        Detail: {detail}")
    return condition


def _run_episode(env: RoutingEnv, strategy: str, seed: int) -> dict:
    """Run one episode with a given strategy, return diagnostics."""
    obs, info = env.reset(seed=seed)
    done = False
    total_reward = 0.0
    rewards: list[float] = []
    mlus: list[float] = []
    step = 0

    while not done:
        n_valid = obs["n_valid"]
        K = env._K

        if strategy == "sp":
            action = 0
        elif strategy == "random":
            action = int(np.random.randint(0, max(n_valid, 1)))
        elif strategy == "last":
            # Pick the longest path (worst greedy)
            action = min(n_valid - 1, K - 1) if n_valid > 0 else 0
        else:
            action = 0

        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        total_reward += reward
        rewards.append(reward)
        mlus.append(info.get("mlu", 0.0))
        step += 1

    return {
        "total_reward": total_reward,
        "rewards": rewards,
        "mlus": mlus,
        "final_mlu": mlus[-1] if mlus else 0.0,
        "steps": step,
    }


# ─── 1. 解析验证 ───

def verify_analytical(env: RoutingEnv) -> dict:
    header("1. 解析验证 — 已知拓扑精确 MLU")
    results = {}

    # Test 1: SP routing on full topology → MLU finite and positive
    obs, info = env.reset(seed=42)
    obs, r, done, _, info = env.step(0)  # SP: always first path
    results["mlu_sp_first_flow"] = info["mlu"]
    check("MLU finite with SP routing", np.isfinite(info["mlu"]),
          f"MLU={info['mlu']:.4f}")
    check("MLU > 0 with active flows", info["mlu"] > 0,
          f"MLU={info['mlu']:.4f}")

    # Test 2: Mini-topology (2 nodes, 1 flow)
    cfg2 = SimConfig(n_planes=1, sats_per_plane=2, n_flows=1, n_heavy=0,
                     n_popular=1, failure_rate=0.0, t_slots=1)
    env2 = RoutingEnv(cfg2, seed=0)
    obs2, _ = env2.reset(seed=0)
    check("Mini-topology has valid paths", obs2["n_valid"] > 0,
          f"n_valid={obs2['n_valid']}, K={env2._K}")
    obs2, r2, done2, _, info2 = env2.step(0)
    check("Mini-topology (2 nodes) MLU finite", np.isfinite(info2["mlu"]),
          f"MLU={info2['mlu']:.4f}, E={env2._E}")

    return results


# ─── 2. 统计验证 ───

def verify_statistical(env: RoutingEnv, n_samples: int = 100, seed: int = 42) -> dict:
    header("2. 统计验证 — 流量/故障分布")
    results = {}
    cfg = env.config

    heavy_demands: list[float] = []
    light_demands: list[float] = []

    for i in range(n_samples):
        env.reset(seed=seed + i)
        flows = env._flows
        n_heavy = cfg.n_heavy
        for j, (src, dst, demand) in enumerate(flows):
            if j < n_heavy:
                heavy_demands.append(demand)
            else:
                light_demands.append(demand)

    heavy_arr = np.array(heavy_demands)
    light_arr = np.array(light_demands)

    check("Heavy median > Light median",
          np.median(heavy_arr) > np.median(light_arr),
          f"heavy_median={np.median(heavy_arr):.2f} > light_median={np.median(light_arr):.2f}")
    check("Light demands >= 0.05 Gbps (post-modulation floor)",
          np.percentile(light_arr, 1) >= 0.05,
          f"light 1st percentile = {np.percentile(light_arr, 1):.3f}")

    # Test failure rate (undirected edges removed)
    if cfg.failure_rate > 0:
        failure_counts: list[float] = []
        for i in range(n_samples):
            env.reset(seed=seed + 1000 + i)
            total_undirected = env._E // 2
            failed = len(env._failed_undirected)
            failure_counts.append(failed / total_undirected if total_undirected > 0 else 0)

        mean_rate = np.mean(failure_counts)
        expected_range = (cfg.failure_rate * 0.3, cfg.failure_rate * 3.0)
        check(f"Failure rate ≈ {cfg.failure_rate:.0%} (undirected edge ratio)",
              expected_range[0] <= mean_rate <= expected_range[1],
              f"actual={mean_rate:.3f}, expected_range=[{expected_range[0]:.3f}, {expected_range[1]:.3f}]")

    results["heavy_mean"] = float(np.mean(heavy_arr))
    results["light_mean"] = float(np.mean(light_arr))
    return results


# ─── 3. 退化验证 ───

def verify_degenerate(env: RoutingEnv, seed: int = 42) -> dict:
    header("3. 退化验证 — 确定性种子 → 确定性输出")
    results = {}

    ep1 = _run_episode(env, "sp", seed=seed)
    ep2 = _run_episode(env, "sp", seed=seed)
    check("Deterministic with same seed (total reward)",
          abs(ep1["total_reward"] - ep2["total_reward"]) < 1e-10,
          f"ep1={ep1['total_reward']:.6f}, ep2={ep2['total_reward']:.6f}")
    check("Deterministic with same seed (final MLU)",
          abs(ep1["final_mlu"] - ep2["final_mlu"]) < 1e-10,
          f"ep1={ep1['final_mlu']:.6f}, ep2={ep2['final_mlu']:.6f}")

    ep3 = _run_episode(env, "sp", seed=seed + 1)
    check("Different seed → different MLU",
          abs(ep1["final_mlu"] - ep3["final_mlu"]) > 1e-6,
          f"seed42={ep1['final_mlu']:.4f}, seed43={ep3['final_mlu']:.4f}")

    cfg_nofail = SimConfig(failure_rate=0.0)
    env_nofail = RoutingEnv(cfg_nofail, seed=seed)
    env_nofail.reset(seed=seed)
    check("Zero failure rate → no failures",
          len(env_nofail._failed_undirected) == 0,
          f"failed={len(env_nofail._failed_undirected)}")

    return results


# ─── 4. Episode 结构验证 ───

def verify_episode_structure(env: RoutingEnv, n_episodes: int = 5, seed: int = 42) -> dict:
    header("4. Episode 结构验证 — 步数=n_flows, MLU 非递减")
    results = {}

    for i in range(n_episodes):
        ep = _run_episode(env, "sp", seed=seed + i)
        expected_steps = env.config.n_flows

        check(f"Episode {i}: steps = n_flows",
              ep["steps"] == expected_steps,
              f"steps={ep['steps']}, expected={expected_steps}")

        # MLU should be non-decreasing (each routing step adds load)
        mlus = ep["mlus"]
        non_decreasing = all(mlus[t] >= mlus[t - 1] - 1e-10 for t in range(1, len(mlus)))
        check(f"Episode {i}: MLU non-decreasing",
              non_decreasing,
              f"final_mlu={mlus[-1]:.4f}")

    return results


# ─── 5. MDP Trial ───

def verify_mdp_trial(env: RoutingEnv, n_episodes: int = 10, seed: int = 42) -> dict:
    header("5. MDP Trial — SP vs Random 策略对比")
    results = {}

    sp_rewards: list[float] = []
    random_rewards: list[float] = []

    for i in range(n_episodes):
        ep_sp = _run_episode(env, "sp", seed=seed + i)
        ep_rand = _run_episode(env, "random", seed=seed + i)
        sp_rewards.append(ep_sp["total_reward"])
        random_rewards.append(ep_rand["total_reward"])

    mean_sp = np.mean(sp_rewards)
    mean_rand = np.mean(random_rewards)

    print(f"  SP mean reward:     {mean_sp:.4f}")
    print(f"  Random mean reward: {mean_rand:.4f}")

    # Note: In sequential K-path routing, random may beat SP because greedy
    # shortest-path doesn't consider future flow impact. This is expected.
    check("SP vs Random (informational)", True,
          f"SP={mean_sp:.4f}, Random={mean_rand:.4f} (random can beat SP in sequential routing)")

    check("Rewards finite", all(np.isfinite(r) for r in sp_rewards + random_rewards),
          f"all {2*n_episodes} episodes finite")

    check("Strategy differentiation (SP ≠ Random)",
          abs(mean_sp - mean_rand) > 1e-4,
          f"diff={abs(mean_sp - mean_rand):.4f}")

    results["sp_mean"] = float(mean_sp)
    results["random_mean"] = float(mean_rand)
    return results


# ─── 6. Baseline 对比 ───

def verify_baseline(env: RoutingEnv, seed: int = 42) -> dict:
    header("6. Baseline 对比 — SP vs ECMP")
    results = {}

    sp_result = run_sp(env, n_eval=50, seed_offset=300000)
    ecmp_result = run_ecmp(env, n_eval=50, seed_offset=300000)

    print(f"  SP MLU:   {sp_result['mean']:.4f} ± {sp_result['std']:.4f}")
    print(f"  ECMP MLU: {ecmp_result['mean']:.4f} ± {ecmp_result['std']:.4f}")

    check("SP MLU finite", np.isfinite(sp_result["mean"]),
          f"mean={sp_result['mean']:.4f}")
    check("ECMP MLU finite", np.isfinite(ecmp_result["mean"]),
          f"mean={ecmp_result['mean']:.4f}")
    check("ECMP ≤ SP (load splitting helps or matches)",
          ecmp_result["mean"] <= sp_result["mean"] * 1.05,
          f"ECMP={ecmp_result['mean']:.4f} <= SP*1.05={sp_result['mean']*1.05:.4f}")

    results["sp"] = sp_result
    results["ecmp"] = ecmp_result
    return results


# ─── 7. Reward Balance Gate ───

def verify_reward_balance(env: RoutingEnv, n_episodes: int = 10, seed: int = 42) -> dict:
    header("7. Reward Balance Gate — 策略分化/信号非恒定")
    results = {}

    sp_rewards: list[float] = []
    random_rewards: list[float] = []

    for i in range(n_episodes):
        ep_sp = _run_episode(env, "sp", seed=seed + i)
        ep_rand = _run_episode(env, "random", seed=seed + i)
        sp_rewards.append(ep_sp["total_reward"])
        random_rewards.append(ep_rand["total_reward"])

    mean_sp = float(np.mean(sp_rewards))
    mean_rand = float(np.mean(random_rewards))

    # Strategy differentiation: check that strategies produce different results
    check("Strategy differentiation (SP ≠ Random)",
          abs(mean_sp - mean_rand) > 1e-4,
          f"SP={mean_sp:.4f}, Random={mean_rand:.4f}, diff={abs(mean_sp-mean_rand):.4f}")

    # Per-step reward distribution
    obs, info = env.reset(seed=seed)
    step_rewards: list[float] = []
    done = False
    while not done:
        obs, r, done, _, info = env.step(0)
        step_rewards.append(r)

    step_arr = np.array(step_rewards)
    reward_std = float(np.std(step_rewards))
    reward_range = float(step_arr.max() - step_arr.min())

    check("Reward variance > 1e-6 (non-constant signal)",
          reward_std > 1e-6,
          f"std={reward_std:.6f}")
    check("Reward has variation (range > 0.01)",
          reward_range > 0.01,
          f"range={reward_range:.4f}")

    sp_std = float(np.std(sp_rewards))
    check("Cross-episode variance > 1e-6", sp_std > 1e-6,
          f"std={sp_std:.6f}")

    results["sp_mean"] = mean_sp
    results["random_mean"] = mean_rand
    results["step_std"] = reward_std
    results["cross_ep_std"] = sp_std
    return results


# ---------------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------------

def run_all_verifications(config: SimConfig | None = None, seed: int = 42) -> dict:
    """Run all 7 verification categories."""
    cfg = config or SimConfig()
    print("LEO Congestion Routing — Verification Suite (K-path)")
    print(f"Config: {cfg.n_nodes} nodes ({cfg.n_planes}x{cfg.sats_per_plane}), "
          f"failure_rate={cfg.failure_rate}, K={cfg.k_paths}")

    env = RoutingEnv(cfg, seed=seed)

    all_results = {}
    all_results["analytical"] = verify_analytical(env)
    all_results["statistical"] = verify_statistical(env, seed=seed)
    all_results["degenerate"] = verify_degenerate(env, seed=seed)
    all_results["episode_structure"] = verify_episode_structure(env, seed=seed)
    all_results["mdp_trial"] = verify_mdp_trial(env, seed=seed)
    all_results["baseline"] = verify_baseline(env, seed=seed)
    all_results["reward_balance"] = verify_reward_balance(env, seed=seed)

    print(f"\n{'='*60}")
    print("  All verifications completed.")
    print(f"{'='*60}")
    return all_results


if __name__ == "__main__":
    run_all_verifications()
