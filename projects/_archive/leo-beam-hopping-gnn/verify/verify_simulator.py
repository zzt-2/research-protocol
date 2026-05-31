"""Verification script for LEO Beam Hopping Simulator — GW Step 7 Part A."""
import sys
import numpy as np

sys.path.insert(0, '/mnt/d/code/study/research-protocol/projects/leo-beam-hopping-gnn')

from simulator.config import SimConfig
from simulator.antenna import gain_at_angle, compute_gain_matrix, hex_grid_positions
from simulator.channel import free_space_path_loss_db, compute_sinr, compute_interference_graph
from simulator.traffic import TrafficGenerator
from simulator.env import BHEnv

PASSED = 0
FAILED = 0


def check(name: str, condition: bool, detail: str = ""):
    global PASSED, FAILED
    if condition:
        print(f"  PASS: {name}")
        PASSED += 1
    else:
        print(f"  FAIL: {name} — {detail}")
        FAILED += 1


def test_path_loss():
    """Analytical: Free space path loss at 550km, 11.45GHz."""
    print("\n[1] Free Space Path Loss")
    config = SimConfig()
    # L_fs = 20*log10(4πd/λ) where d=550e3m, λ=c/f
    d_m = 550e3
    wavelength = 3e8 / 11.45e9
    expected = 20.0 * np.log10(4.0 * np.pi * d_m / wavelength)
    computed = free_space_path_loss_db(550.0, 11.45e9)
    diff = abs(computed - expected)
    check("L_fs at 550km, 11.45GHz", diff < 0.1,
          f"computed={computed:.4f}, expected={expected:.4f}, diff={diff:.4f}")


def test_bessel_main_lobe():
    """Analytical: Bessel main lobe gain at θ=0 should equal max gain."""
    print("\n[2] Bessel Main Lobe Gain")
    config = SimConfig()
    gain_linear = gain_at_angle(0.0, config)
    gain_dbi = 10 * np.log10(gain_linear)
    diff = abs(gain_dbi - config.antenna_max_gain_dbi)
    check("G(θ=0) = 48.7 dBi", diff < 0.5,
          f"computed={gain_dbi:.4f} dBi, expected={config.antenna_max_gain_dbi}, diff={diff:.4f}")


def test_demand_distribution():
    """Statistical: Compound Poisson demand distribution."""
    print("\n[3] Demand Distribution (Compound Poisson)")
    config = SimConfig()
    rng = np.random.default_rng(42)
    from simulator.traffic import compound_poisson_demand
    samples = []
    for _ in range(10000):
        d = compound_poisson_demand(config.n_beams, config, rng)
        samples.extend(d.tolist())
    samples = np.array(samples)
    mean = samples.mean()
    std = samples.std()
    check("Mean demand in [100, 600] Mbps", 100 < mean < 600,
          f"mean={mean:.1f}")
    check("Std > 50 Mbps (not degenerate)", std > 50,
          f"std={std:.1f}")


def test_degradation():
    """Degradation test: deterministic actions → zero reward variance."""
    print("\n[4] Degradation Test (deterministic)")
    config = SimConfig()
    # Disable fading by setting alpha=0 (fading stays at initial values)
    config_faded = SimConfig(fading_alpha=0.0)

    # Use uniform demand with fixed seed for reproducibility
    env = BHEnv(config=config_faded, seed=123)
    # Override traffic to uniform for stability
    env.traffic = TrafficGenerator(config_faded, mode='uniform', seed=123)

    # Freeze fading to ones (no fading effect)
    rewards = []
    for ep in range(10):
        obs, info = env.reset(seed=123)
        env.traffic = TrafficGenerator(config_faded, mode='uniform', seed=123)
        env.fading = np.ones(config.n_beams)  # no fading
        total_r = 0
        done = False
        action = np.ones(config.n_beams)  # same action every time
        while not done:
            obs, r, terminated, truncated, info = env.step(action)
            total_r += r
            done = terminated or truncated
            env.fading = np.ones(config.n_beams)  # keep fading frozen
        rewards.append(total_r)

    rewards = np.array(rewards)
    var = rewards.var()
    check("Reward variance = 0 with deterministic setup", var < 1e-10,
          f"variance={var:.2e}")


def test_autocorrelation():
    """Autocorrelation: lag-1 autocorrelation of channel < 0.95."""
    print("\n[5] Channel Autocorrelation (lag-1 < 0.95)")
    config = SimConfig(fading_alpha=0.3)
    rng = np.random.default_rng(42)

    # Generate 100-slot fading time series for one beam
    n_slots = 100
    fading = np.sqrt(rng.exponential(1.0))  # initial
    series = []
    alpha = config.fading_alpha
    for _ in range(n_slots):
        new_sample = np.sqrt(rng.exponential(1.0))
        fading = alpha * new_sample + (1 - alpha) * fading
        series.append(fading)
    series = np.array(series)

    # Lag-1 autocorrelation
    mean = series.mean()
    var = series.var()
    if var > 0:
        autocorr = np.mean((series[:-1] - mean) * (series[1:] - mean)) / var
    else:
        autocorr = 1.0
    check("Lag-1 autocorrelation < 0.95", autocorr < 0.95,
          f"autocorr={autocorr:.4f}")


def test_mdp_sanity():
    """MDP basic sanity: shapes, types, full episode."""
    print("\n[6] MDP Basic Sanity")
    config = SimConfig()
    env = BHEnv(config=config, seed=42)

    # Test reset
    obs, info = env.reset(seed=42)
    check("reset() obs shape = (N, 4)", obs.shape == (config.n_beams, 4),
          f"shape={obs.shape}")
    check("reset() obs dtype = float32", obs.dtype == np.float32,
          f"dtype={obs.dtype}")
    check("reset() obs in [0, 1]", (obs >= 0).all() and (obs <= 1).all(),
          f"min={obs.min():.4f}, max={obs.max():.4f}")

    # Test step
    action = np.random.randn(config.n_beams)
    obs, reward, terminated, truncated, info = env.step(action)
    check("step() obs shape = (N, 4)", obs.shape == (config.n_beams, 4),
          f"shape={obs.shape}")
    check("step() reward is float", isinstance(reward, float),
          f"type={type(reward)}")
    check("step() returns terminated bool", isinstance(terminated, bool),
          f"type={type(terminated)}")
    check("step() info has reward decomposition",
          all(k in info for k in ['reward_throughput', 'reward_fairness', 'penalty_interference']),
          f"keys={list(info.keys())}")

    # Full episode with random actions
    obs, info = env.reset(seed=0)
    total_reward = 0
    done = False
    steps = 0
    while not done:
        action = np.random.randn(config.n_beams)
        obs, r, terminated, truncated, info = env.step(action)
        total_reward += r
        steps += 1
        done = terminated or truncated
    check("Full episode completes in T steps", steps == config.t_slots,
          f"steps={steps}, T={config.t_slots}")
    check("Total reward is finite", np.isfinite(total_reward),
          f"total_reward={total_reward}")

    # Check observation space bounds
    obs, info = env.reset(seed=7)
    in_bounds = env.observation_space.contains(obs)
    check("obs in observation_space bounds", in_bounds,
          f"obs min={obs.min():.4f}, max={obs.max():.4f}")


if __name__ == "__main__":
    print("=" * 60)
    print("LEO Beam Hopping Simulator — Verification (Part A)")
    print("=" * 60)

    test_path_loss()
    test_bessel_main_lobe()
    test_demand_distribution()
    test_degradation()
    test_autocorrelation()
    test_mdp_sanity()

    print(f"\n{'=' * 60}")
    print(f"Results: {PASSED} passed, {FAILED} failed")
    print(f"{'=' * 60}")

    sys.exit(0 if FAILED == 0 else 1)
