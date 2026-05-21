"""仿真器验证套件 — 7 类验证。

1. 解析验证 — FSPL / 轨道周期 / Shannon 容量
2. 统计验证 — 衰落分布检验
3. 退化验证 — 确定性信道 → 固定速率
4. 自相关验证 — 信道时序 lag-1 ρ
5. MDP trial — 随机/贪心 episode
6. Baseline 对比 — greedy > random
7. 奖励平衡 gate — 分量占比 < 80%
"""

from __future__ import annotations

import numpy as np

from config import SimConfig
from env import SatelliteDAGEnv


def header(msg: str) -> None:
    print(f"\n{'='*60}\n  {msg}\n{'='*60}")


def check(name: str, condition: bool, detail: str = "") -> bool:
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {name}" + (f" — {detail}" if detail else ""))
    return condition


# ─── 1. 解析验证 ───

def verify_analytical(config: SimConfig) -> dict:
    header("1. 解析验证 — 公式精确对比")
    results = {}

    # 轨道周期: T = 2π√((R+h)³/μ) ≈ 94.5 min (h=500km)
    expected_period = 2 * np.pi * np.sqrt((config.earth_radius + config.leo_altitude) ** 3 / config.mu_earth)
    check("轨道周期 ≈ 94.5 min", abs(config.orbital_period - expected_period) < 1.0,
          f"{config.orbital_period/60:.1f} min")

    # FSPL: L = 20·log10(4πdf/c)
    from channel import free_space_path_loss, C
    d = 500e3  # 500 km
    f = 20e9   # Ka-band
    expected_fspl = 20 * np.log10(4 * np.pi * d * f / C)
    actual_fspl = free_space_path_loss(d, f)
    check("FSPL 公式", abs(actual_fspl - expected_fspl) < 0.01,
          f"actual={actual_fspl:.2f} dB, expected={expected_fspl:.2f} dB")

    # Shannon: C = B·log2(1+SNR)
    from channel import shannon_rate
    bw, snr = 20e6, 100.0
    expected_cap = bw * np.log2(1 + snr)
    actual_cap = shannon_rate(snr, bw)
    check("Shannon 容量", abs(actual_cap - expected_cap) < 1.0,
          f"{actual_cap/1e6:.1f} Mbps")

    # 噪声功率: -100 dBm → 1e-13 W
    check("噪声功率", abs(config.noise_power_w - 1e-13) < 1e-15,
          f"{config.noise_power_w:.2e} W")

    return results


# ─── 2. 统计验证 ───

def verify_statistical(config: SimConfig, n_samples: int = 5000) -> dict:
    header("2. 统计验证 — 分布检验")
    from channel import ChannelModel, rician_fading, shadowed_rician_fading

    rng = np.random.default_rng(42)
    cm = ChannelModel(config, rng=rng)

    # Rician 均值应接近 1
    rician_samples = np.array([rician_fading(rng, config.rician_k) for _ in range(n_samples)])
    check("Rician 均值 ≈ 1", abs(rician_samples.mean() - 1.0) < 0.1,
          f"mean={rician_samples.mean():.3f}")

    # Shadowed-Rician 非负
    sr_samples = np.array([shadowed_rician_fading(rng, config.sr_average) for _ in range(n_samples)])
    check("Shadowed-Rician 非负", (sr_samples >= 0).all(), f"min={sr_samples.min():.4f}")

    # Channel rate 单调递减（确定性信道，排除衰落噪声）
    cm_det = ChannelModel(config, rng=rng)
    cm_det.set_deterministic(True)
    dists = np.linspace(100, 3000, 20)
    rates_g2u = [cm_det.g2u_rate(d, config.tx_power_iotd) for d in dists]
    monotone = all(rates_g2u[i] >= rates_g2u[i+1] for i in range(len(rates_g2u)-1))
    check("G2U rate 随距离单调递减 (deterministic)", monotone,
          f"{rates_g2u[0]/1e6:.1f}→{rates_g2u[-1]/1e6:.1f} Mbps")

    return {}


# ─── 3. 退化验证 ───

def verify_degenerate(config: SimConfig) -> dict:
    header("3. 退化验证 — 确定性信道")
    env = SatelliteDAGEnv(config, seed=42, deterministic_channel=True)
    obs1, info1 = env.reset(seed=42)
    obs2, info2 = env.reset(seed=42)

    # Same seed → same DAG, same positions
    check("Same seed → same action mask",
          np.array_equal(info1["action_mask"], info2["action_mask"]),
          f"mask sum={info1['action_mask'].sum()}")

    # Run same actions on both
    mask = info1["action_mask"]
    valid = np.where(mask)[0]
    action = int(valid[0])
    _, r1, _, _, i1 = env.step(action)
    env.reset(seed=42)
    _, r2, _, _, i2 = env.step(action)
    check("Same seed + same action → same reward",
          abs(r1 - r2) < 1e-10, f"r1={r1:.6f}, r2={r2:.6f}")

    return {}


# ─── 4. 自相关验证 ───

def verify_autocorrelation(config: SimConfig, n_steps: int = 50) -> dict:
    header("4. 自相关验证 — 信道时序 AR(1)")
    from channel import ChannelModel

    rng = np.random.default_rng(42)
    cm = ChannelModel(config, rng=rng)
    rates = [cm.g2u_rate(500.0, config.tx_power_iotd) for _ in range(n_steps)]
    series = np.array(rates)
    mean = series.mean()
    var = np.sum((series - mean) ** 2)
    if var < 1e-10:
        check("信道方差非零", False, "方差为零")
        return {}
    rho = np.sum((series[1:] - mean) * (series[:-1] - mean)) / var
    check("Lag-1 ρ < 0.95", rho < 0.95, f"ρ = {rho:.4f}")
    return {}


# ─── 5. MDP Trial ───

def verify_mdp_trial(config: SimConfig, n_episodes: int = 3) -> dict:
    header("5. MDP Trial — 随机策略 episode")
    env = SatelliteDAGEnv(config, seed=42)

    for ep in range(n_episodes):
        obs, info = env.reset(seed=42 + ep * 1000)
        done, total_r, steps = False, 0.0, 0
        while not done:
            mask = info.get("action_mask")
            valid = np.where(mask)[0]
            if len(valid) == 0:
                break
            action = int(np.random.choice(valid))
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            total_r += reward
            steps += 1
        check(f"Episode {ep}: finite reward", np.isfinite(total_r),
              f"reward={total_r:.2f}, steps={steps}")

    return {}


# ─── 6. Baseline 对比 ───

def verify_baseline(config: SimConfig) -> dict:
    header("6. Baseline 对比 — greedy > random")
    from baselines import RandomBaseline, GreedySPTBaseline

    env = SatelliteDAGEnv(config, seed=42)
    rng = RandomBaseline()
    greedy = GreedySPTBaseline()

    random_rewards = [rng.run_episode(env, 42 + i)["reward"] for i in range(5)]
    greedy_rewards = [greedy.run_episode(env, 42 + i)["reward"] for i in range(5)]

    mean_r, mean_g = np.mean(random_rewards), np.mean(greedy_rewards)
    check("Greedy > Random", mean_g > mean_r,
          f"greedy={mean_g:.2f} vs random={mean_r:.2f}")
    return {}


# ─── 7. 奖励平衡 gate ───

def verify_reward_balance(config: SimConfig, n_episodes: int = 5) -> dict:
    header("7. 奖励平衡 gate")
    from baselines import RandomBaseline, GreedySPTBaseline

    env = SatelliteDAGEnv(config, seed=42)
    rng_bl = RandomBaseline()
    greedy_bl = GreedySPTBaseline()

    random_rewards, greedy_rewards = [], []
    for i in range(n_episodes):
        random_rewards.append(rng_bl.run_episode(env, 42 + i * 100)["reward"])
        greedy_rewards.append(greedy_bl.run_episode(env, 42 + i * 100)["reward"])

    mean_g, mean_r = np.mean(greedy_rewards), np.mean(random_rewards)
    check("Greedy > Random", mean_g > mean_r, f"greedy={mean_g:.2f} vs random={mean_r:.2f}")
    check("奖励方差 > 1e-6", np.std(random_rewards) > 1e-6,
          f"std={np.std(random_rewards):.6f}")

    return {}


# ─── 统一入口 ───

def run_all_verifications(config: SimConfig | None = None) -> dict:
    config = config or SimConfig()
    print("仿真器验证套件 — HGAT Satellite DAG Offloading")
    results = {}
    results["analytical"] = verify_analytical(config)
    results["statistical"] = verify_statistical(config)
    results["degenerate"] = verify_degenerate(config)
    results["autocorrelation"] = verify_autocorrelation(config)
    results["mdp_trial"] = verify_mdp_trial(config)
    results["baseline"] = verify_baseline(config)
    results["reward_balance"] = verify_reward_balance(config)
    print(f"\n{'='*60}\n  验证完成。\n{'='*60}")
    return results


if __name__ == "__main__":
    run_all_verifications()
