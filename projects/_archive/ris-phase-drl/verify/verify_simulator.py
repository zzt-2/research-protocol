"""RIS Phase DRL Simulator Verification Suite.

7 verification categories:
  1. Analytical — formula-precise comparison
  2. Statistical — distribution checks
  3. Degenerate — simplified model sanity
  4. Autocorrelation — time-series AR(1) checks
  5. MDP Trial — random policy episodes
  6. Baseline comparison — Random vs Fixed(theta=0)
  7. Reward Balance Gate — single-component reward sanity
"""

from __future__ import annotations

import sys
import os

# Ensure simulator package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np

from simulator.config import SimConfig
from simulator.channel import ChannelGenerator
from simulator.beamforming import zf_beamforming
from simulator.reward import compute_sum_rate
from simulator.env import RISPhaseEnv


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


def lag1_autocorr(x: np.ndarray) -> float:
    """Compute lag-1 autocorrelation of a 1-D array."""
    if len(x) < 2:
        return 0.0
    mean = x.mean()
    var = np.sum((x - mean) ** 2)
    if var < 1e-15:
        return 0.0
    return float(np.sum((x[1:] - mean) * (x[:-1] - mean)) / var)


# ---------------------------------------------------------------------------
# 1. Analytical Verification
# ---------------------------------------------------------------------------

def verify_analytical(seed: int = 42) -> dict:
    """Formula-precise comparison: theta=0 manual cascade, alignment vs random, ZF null."""
    header("1. Analytical Verification")
    results = {}
    rng = np.random.default_rng(seed)
    cfg = SimConfig()

    # --- 1a. theta=0 manual cascade ---
    # theta=0 => action = -1 (since theta = (action+1)*pi, theta=0 when action=-1)
    # phase_shift = exp(j*0) = ones(N)
    # H_eff = H2^H @ diag(ones) @ H1 = H2^H @ H1
    gen = ChannelGenerator(cfg, rng=rng)
    H1, H2 = gen.generate()
    H_eff_manual = H2.conj().T @ H1  # (K, M)

    W_manual = zf_beamforming(H_eff_manual, cfg.tx_power_linear, cfg.K)
    sr_manual, sinrs_manual = compute_sum_rate(H_eff_manual, W_manual, cfg.noise_power_linear)

    # Now via env with action = -1 (theta=0)
    env = RISPhaseEnv(cfg)
    obs, info = env.reset(seed=seed)
    # Override channels to match (reset regenerates, but with same seed the channels should match)
    env.H1, env.H2 = H1, H2
    action_zero = -np.ones(cfg.N, dtype=np.float32)
    obs, reward, term, trunc, info_env = env.step(action_zero)

    sr_env = reward
    rel_err = abs(sr_manual - sr_env) / max(abs(sr_manual), 1e-12)
    check("theta=0 manual vs env (rel_err<5%)",
          rel_err < 0.05,
          f"manual={sr_manual:.6f}, env={sr_env:.6f}, rel_err={rel_err:.6f}")
    results["theta0_rel_err"] = rel_err

    # --- 1b. Alignment (theta=0) vs random phase shifts ---
    # theta=0 is a specific configuration; compare against random actions
    random_rewards = []
    for _ in range(20):
        obs, info = env.reset(seed=int(rng.integers(0, 2**31)))
        rand_act = rng.uniform(-1, 1, cfg.N).astype(np.float32)
        _, r, _, _, _ = env.step(rand_act)
        random_rewards.append(r)

    # theta=0 reward with a fresh channel
    obs, info = env.reset(seed=int(rng.integers(0, 2**31)))
    aligned_r = env.step(action_zero)[1]

    mean_rand = np.mean(random_rewards)
    # theta=0 should beat average random (not guaranteed for every seed,
    # but for Rician kappa=10dB the LoS alignment is strong)
    check("Aligned(theta=0) > mean(random)",
          aligned_r > mean_rand,
          f"aligned={aligned_r:.4f}, mean_random={mean_rand:.4f}")
    results["aligned_sr"] = aligned_r
    results["random_sr_mean"] = mean_rand

    # --- 1c. ZF zero-interference ---
    # With ZF, inter-user interference should be negligible
    rng2 = np.random.default_rng(seed + 100)
    gen2 = ChannelGenerator(cfg, rng=rng2)
    H1_2, H2_2 = gen2.generate()
    H_eff_2 = H2_2.conj().T @ H1_2
    W_2 = zf_beamforming(H_eff_2, cfg.tx_power_linear, cfg.K)
    link_gain = H_eff_2 @ W_2  # (K, K)
    off_diag = link_gain.copy()
    np.fill_diagonal(off_diag, 0)
    interference_power = float(np.sum(np.abs(off_diag) ** 2))
    check("ZF inter-user interference < 1e-6",
          interference_power < 1e-6,
          f"total interference power = {interference_power:.2e}")
    results["zf_interference"] = interference_power

    return results


# ---------------------------------------------------------------------------
# 2. Statistical Verification
# ---------------------------------------------------------------------------

def verify_statistical(seed: int = 42) -> dict:
    """Rician distribution check and block-fading independence."""
    header("2. Statistical Verification")
    results = {}
    cfg = SimConfig()

    # --- 2a. Rician E[|h|^2] ~ PL ---
    # For Rician with kappa: E[|h_los|^2] = kappa/(kappa+1), E[|h_nlos|^2] = 1/(kappa+1)
    # Total E[|h|^2] = PL (since both components scaled by sqrt(PL))
    # Generate many H1 and check average |h_ij|^2 ≈ pl_bs_ris_linear
    gen = ChannelGenerator(cfg)
    n_trials = 1000
    sq_magnitudes = []
    for _ in range(n_trials):
        gen.rng = np.random.default_rng(int(np.random.default_rng().integers(0, 2**31)))
        H1, _ = gen.generate()
        sq_magnitudes.append(np.mean(np.abs(H1) ** 2))

    mean_sq_mag = np.mean(sq_magnitudes)
    expected_pl = cfg.pl_bs_ris_linear
    rel_err = abs(mean_sq_mag - expected_pl) / expected_pl
    check("E[|h|^2] ~ PL_bs_ris (rel_err<10%)",
          rel_err < 0.10,
          f"measured={mean_sq_mag:.6e}, expected={expected_pl:.6e}, rel_err={rel_err:.4f}")
    results["rician_rel_err"] = rel_err

    # --- 2b. Block fading independence: lag-1 autocorr of first-reward across episodes ---
    first_rewards = []
    env = RISPhaseEnv(cfg)
    for i in range(100):
        obs, info = env.reset(seed=seed + i * 7)
        act = np.zeros(cfg.N, dtype=np.float32)  # fixed action
        _, r, _, _, _ = env.step(act)
        first_rewards.append(r)

    first_rewards = np.array(first_rewards)
    rho = lag1_autocorr(first_rewards)
    check("Block-fading independence: lag-1 rho < 0.3",
          abs(rho) < 0.3,
          f"lag-1 autocorr = {rho:.4f}")
    results["block_fading_rho"] = rho

    return results


# ---------------------------------------------------------------------------
# 3. Degenerate Verification
# ---------------------------------------------------------------------------

def verify_degenerate(seed: int = 42) -> dict:
    """Simplified model checks: pure-LoS, no-RIS, fixed-phase consistency."""
    header("3. Degenerate Verification")
    results = {}

    # --- 3a. kappa->inf (pure LoS): H1 variance should be near 0 ---
    cfg_pure = SimConfig(kappa_db=60.0)
    gen = ChannelGenerator(cfg_pure)
    H1_list = []
    for i in range(100):
        gen.rng = np.random.default_rng(seed + i)
        H1, _ = gen.generate()
        H1_list.append(H1)

    H1_stack = np.array(H1_list)  # (100, N, M)
    h1_var = float(np.var(H1_stack))
    check("Pure-LoS (kappa=60dB): H1 variance near 0",
          h1_var < 1e-6,
          f"variance = {h1_var:.2e}")
    results["pure_los_var"] = h1_var

    # --- 3b. H1=0 => no signal path => sum_rate = 0 ---
    cfg = SimConfig()
    env = RISPhaseEnv(cfg)
    obs, info = env.reset(seed=seed)
    env.H1 = np.zeros((cfg.N, cfg.M), dtype=complex)
    action = np.zeros(cfg.N, dtype=np.float32)
    _, r, _, _, info_env = env.step(action)
    check("H1=0 => sum_rate=0",
          abs(r) < 1e-10,
          f"reward = {r:.2e}")
    results["no_ris_reward"] = r

    # --- 3c. Same channel, same action => same result ---
    obs1, info1 = env.reset(seed=seed + 99)
    H1_saved, H2_saved = env.H1.copy(), env.H2.copy()
    action_fixed = np.zeros(cfg.N, dtype=np.float32)

    _, r1, _, _, _ = env.step(action_fixed)

    # Reset with same seed to get same channels, then apply same action
    obs2, info2 = env.reset(seed=seed + 99)
    _, r2, _, _, _ = env.step(action_fixed)

    check("Same channel + same action => same reward",
          abs(r1 - r2) < 1e-10,
          f"r1={r1:.6f}, r2={r2:.6f}")
    results["deterministic_consistency"] = abs(r1 - r2)

    return results


# ---------------------------------------------------------------------------
# 4. Autocorrelation Verification
# ---------------------------------------------------------------------------

def verify_autocorrelation(seed: int = 42) -> dict:
    """Episode-internal and episode-inter reward autocorrelation."""
    header("4. Autocorrelation Verification")
    results = {}
    cfg = SimConfig()
    env = RISPhaseEnv(cfg)
    rng = np.random.default_rng(seed)

    # --- 4a. Episode-internal lag-1 autocorr (random policy, 5 episodes) ---
    intra_rho_list = []
    for _ in range(5):
        obs, info = env.reset(seed=int(rng.integers(0, 2**31)))
        rewards = []
        done = False
        while not done:
            action = rng.uniform(-1, 1, cfg.N).astype(np.float32)
            obs, r, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            rewards.append(r)
        rho_ep = lag1_autocorr(np.array(rewards))
        intra_rho_list.append(rho_ep)

    mean_intra_rho = float(np.mean(intra_rho_list))
    check("Episode-internal lag-1 rho (should be moderate, < 0.95)",
          mean_intra_rho < 0.95,
          f"mean rho = {mean_intra_rho:.4f} (values: {[f'{r:.3f}' for r in intra_rho_list]})")
    results["intra_episode_rho"] = mean_intra_rho

    # --- 4b. Episode-inter lag-1 autocorr of first rewards ---
    first_rewards = []
    for i in range(50):
        obs, info = env.reset(seed=seed + i * 13)
        action = rng.uniform(-1, 1, cfg.N).astype(np.float32)
        _, r, _, _, _ = env.step(action)
        first_rewards.append(r)

    inter_rho = lag1_autocorr(np.array(first_rewards))
    check("Episode-inter lag-1 rho < 0.3",
          abs(inter_rho) < 0.3,
          f"inter-episode rho = {inter_rho:.4f}")
    results["inter_episode_rho"] = inter_rho

    return results


# ---------------------------------------------------------------------------
# 5. MDP Trial
# ---------------------------------------------------------------------------

def verify_mdp_trial(seed: int = 42) -> dict:
    """Random policy over 3 full episodes."""
    header("5. MDP Trial — Random Policy Episodes")
    results = {}
    cfg = SimConfig()
    env = RISPhaseEnv(cfg)
    rng = np.random.default_rng(seed)

    all_pass = True
    for ep in range(3):
        obs, info = env.reset(seed=int(rng.integers(0, 2**31)))
        rewards = []
        done = False
        while not done:
            action = rng.uniform(-1, 1, cfg.N).astype(np.float32)
            obs, r, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            rewards.append(r)

        arr = np.array(rewards)
        total = float(arr.sum())
        mean_r = float(arr.mean())
        std_r = float(arr.std())
        finite = bool(np.all(np.isfinite(arr)))
        positive = bool(total > 0)

        print(f"  Episode {ep}: steps={len(rewards)}, "
              f"total={total:.4f}, mean={mean_r:.4f}, std={std_r:.4f}")
        check(f"  Ep{ep} reward > 0", positive, f"total={total:.4f}")
        check(f"  Ep{ep} reward finite", finite, f"all rewards finite: {finite}")

        if not (positive and finite):
            all_pass = False

    check("MDP Trial overall", all_pass, "All episodes: reward>0 and finite")
    results["mdp_all_pass"] = all_pass
    return results


# ---------------------------------------------------------------------------
# 6. Baseline Comparison
# ---------------------------------------------------------------------------

def verify_baseline(seed: int = 42) -> dict:
    """Random policy vs Fixed(theta=0)."""
    header("6. Baseline Comparison — Random vs Fixed(theta=0)")
    results = {}
    cfg = SimConfig()
    env = RISPhaseEnv(cfg)
    rng = np.random.default_rng(seed)

    n_eps = 30

    # Random policy
    random_totals = []
    for i in range(n_eps):
        obs, info = env.reset(seed=seed + i)
        total = 0.0
        done = False
        while not done:
            action = rng.uniform(-1, 1, cfg.N).astype(np.float32)
            obs, r, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            total += r
        random_totals.append(total)

    # Fixed policy: theta=0 (action=-1)
    fixed_totals = []
    for i in range(n_eps):
        obs, info = env.reset(seed=seed + i)
        total = 0.0
        done = False
        action_fixed = -np.ones(cfg.N, dtype=np.float32)
        while not done:
            obs, r, terminated, truncated, info = env.step(action_fixed)
            done = terminated or truncated
            total += r
        fixed_totals.append(total)

    mean_random = float(np.mean(random_totals))
    mean_fixed = float(np.mean(fixed_totals))
    std_random = float(np.std(random_totals))
    std_fixed = float(np.std(fixed_totals))

    print(f"  Random:  mean={mean_random:.4f} ± {std_random:.4f}")
    print(f"  Fixed(θ=0): mean={mean_fixed:.4f} ± {std_fixed:.4f}")

    check("Random mean > 0", mean_random > 0,
          f"mean_random={mean_random:.4f}")
    check("Fixed(θ=0) mean > 0", mean_fixed > 0,
          f"mean_fixed={mean_fixed:.4f}")

    # Both should produce positive rewards (there is always a signal path)
    # Random may or may not beat fixed depending on Rician alignment
    results["random_mean"] = mean_random
    results["fixed_mean"] = mean_fixed
    return results


# ---------------------------------------------------------------------------
# 7. Reward Balance Gate
# ---------------------------------------------------------------------------

def verify_reward_balance(seed: int = 42) -> dict:
    """Single-component reward sanity checks."""
    header("7. Reward Balance Gate")
    results = {}
    cfg = SimConfig()
    env = RISPhaseEnv(cfg)
    rng = np.random.default_rng(seed)

    n_eps = 30
    random_rewards = []
    for i in range(n_eps):
        obs, info = env.reset(seed=seed + i)
        done = False
        ep_rewards = []
        while not done:
            action = rng.uniform(-1, 1, cfg.N).astype(np.float32)
            obs, r, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            ep_rewards.append(r)
        random_rewards.append(float(np.mean(ep_rewards)))

    random_arr = np.array(random_rewards)

    # (a) random reward > 0
    check("(a) Random reward > 0",
          float(np.mean(random_arr)) > 0,
          f"mean_reward={float(np.mean(random_arr)):.6f}")

    # (b) reward variance > 1e-6
    reward_std = float(np.std(random_arr))
    check("(b) Reward variance > 1e-6",
          reward_std > 1e-6,
          f"std={reward_std:.8f}")

    # (c) fixed(theta=0) vs random distinguishable
    fixed_rewards = []
    for i in range(n_eps):
        obs, info = env.reset(seed=seed + i)
        done = False
        ep_rewards = []
        action_fixed = -np.ones(cfg.N, dtype=np.float32)
        while not done:
            obs, r, terminated, truncated, info = env.step(action_fixed)
            done = terminated or truncated
            ep_rewards.append(r)
        fixed_rewards.append(float(np.mean(ep_rewards)))

    fixed_arr = np.array(fixed_rewards)
    mean_diff = abs(float(np.mean(random_arr)) - float(np.mean(fixed_arr)))
    combined_std = float(np.sqrt(np.var(random_arr) + np.var(fixed_arr)))
    separable = combined_std > 1e-10 and (mean_diff / combined_std) > 0.1
    check("(c) Fixed vs Random distinguishable",
          separable,
          f"mean_diff={mean_diff:.4f}, combined_std={combined_std:.4f}, "
          f"ratio={mean_diff/max(combined_std,1e-12):.4f}")

    results["random_mean"] = float(np.mean(random_arr))
    results["fixed_mean"] = float(np.mean(fixed_arr))
    results["random_std"] = reward_std
    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_all_verifications(seed: int = 42) -> dict:
    """Run all 7 verification categories."""
    print("RIS Phase DRL — Simulator Verification Suite")
    all_results = {}

    all_results["analytical"] = verify_analytical(seed)
    all_results["statistical"] = verify_statistical(seed)
    all_results["degenerate"] = verify_degenerate(seed)
    all_results["autocorrelation"] = verify_autocorrelation(seed)
    all_results["mdp_trial"] = verify_mdp_trial(seed)
    all_results["baseline"] = verify_baseline(seed)
    all_results["reward_balance"] = verify_reward_balance(seed)

    print(f"\n{'='*60}")
    print("  Verification complete.")
    print(f"{'='*60}")
    return all_results


if __name__ == "__main__":
    run_all_verifications(seed=42)
