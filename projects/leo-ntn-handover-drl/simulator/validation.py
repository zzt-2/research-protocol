"""Simulator validation: analytical, statistical, degradation, autocorrelation checks.

Implements the 4-item validation checklist from groundwork.md Step 6.
"""

import sys
import numpy as np

from .orbit import WalkerConstellation, geodetic_to_ecef, compute_elevation, EARTH_RADIUS
from .channel import fspl_db, RainFadingModel, ChannelModel
from .env import LEOSatHandoverEnv

PASS = "PASS"
FAIL = "FAIL"
WARN = "WARN"


def validate_fspl():
    """Check 1: Analytical validation — FSPL matches formula at known distance."""
    freq = 20e9
    d_km = 1000.0  # 1000 km
    d_m = d_km * 1e3
    lam = 3e8 / freq
    expected = 20.0 * np.log10(4.0 * np.pi * d_m / lam)
    actual = fspl_db(d_km, freq)
    err = abs(actual - expected)
    status = PASS if err < 0.01 else FAIL
    return status, f"FSPL at {d_km}km: expected={expected:.2f}dB, actual={actual:.2f}dB, err={err:.4f}dB"


def validate_elevation():
    """Check 1b: Elevation angle for overhead satellite should be ~90°."""
    sat_pos = geodetic_to_ecef(0, 0, 550.0)  # directly above equator
    ue_pos = geodetic_to_ecef(0, 0, 0.0)
    elev = compute_elevation(sat_pos, ue_pos)
    status = PASS if abs(elev - 90.0) < 1.0 else FAIL
    return status, f"Elevation for overhead sat: {elev:.2f}° (expected ~90°)"


def validate_rain_statistics():
    """Check 2: Statistical validation — rain fading distribution."""
    model = RainFadingModel(num_sats=10, std_db=5.0, corr_length_s=30.0, dt_s=10.0, seed=42)
    model.reset(seed=42)
    samples = []
    for _ in range(5000):
        samples.append(model.step())
    samples = np.array(samples)  # (5000, 10)

    # Rain attenuation should be non-negative
    neg_ratio = (samples < 0).mean()
    # Mean should be close to theoretical mean of |N(0,σ)| = σ·√(2/π)
    theoretical_mean = 5.0 * np.sqrt(2.0 / np.pi)
    actual_mean = samples.mean()
    mean_err = abs(actual_mean - theoretical_mean) / theoretical_mean

    status = PASS if mean_err < 0.1 and neg_ratio < 0.01 else FAIL
    return (
        status,
        f"Rain atten: mean={actual_mean:.2f}dB (theory={theoretical_mean:.2f}dB, "
        f"err={mean_err:.1%}), neg_ratio={neg_ratio:.4f}",
    )


def validate_degradation():
    """Check 3: Degradation test — without rain, SNR should be deterministic."""
    # With rain
    env1 = LEOSatHandoverEnv(
        num_ues=5, rain_std_db=5.0, duration_s=100.0, dt_s=10.0, seed=42,
    )
    # Without rain (std=0)
    env2 = LEOSatHandoverEnv(
        num_ues=5, rain_std_db=0.0, duration_s=100.0, dt_s=10.0, seed=42,
    )

    rng = np.random.default_rng(0)
    actions_fn = lambda env: np.array([
        rng.choice(np.where(env._get_obs()[i]["visible_mask"])[0])
        if env._get_obs()[i]["visible_count"] > 0 else 0
        for i in range(env.num_ues)
    ])

    # Collect throughput with rain
    throughput_rain = []
    env1.reset(seed=42)
    for _ in range(env1.num_steps):
        obs = env1._get_obs()
        actions = actions_fn(env1)
        _, _, done, info = env1.step(actions)
        throughput_rain.append(info["total_throughput"])
        if done:
            break

    # Collect throughput without rain (same random actions)
    throughput_no_rain = []
    env2.reset(seed=42)
    rng2 = np.random.default_rng(0)
    for _ in range(env2.num_steps):
        obs = env2._get_obs()
        actions = np.array([
            rng2.choice(np.where(obs[i]["visible_mask"])[0])
            if obs[i]["visible_count"] > 0 else 0
            for i in range(env2.num_ues)
        ])
        _, _, done, info = env2.step(actions)
        throughput_no_rain.append(info["total_throughput"])
        if done:
            break

    t_rain = np.array(throughput_rain)
    t_norain = np.array(throughput_no_rain)

    # Without rain, same seed should give identical throughput (deterministic)
    # With rain, throughput should vary
    cv_rain = t_rain.std() / (t_rain.mean() + 1e-10)
    cv_norain = t_norain.std() / (t_norain.mean() + 1e-10)

    status = PASS if cv_rain > cv_norain * 1.5 else WARN
    return (
        status,
        f"CV with rain={cv_rain:.4f}, without rain={cv_norain:.4f} "
        f"(rain should add variability)",
    )


def validate_autocorrelation():
    """Check 4: Lag-1 autocorrelation warning — >0.95 triggers 'too smooth' warning."""
    env = LEOSatHandoverEnv(
        num_ues=5, rain_std_db=5.0, duration_s=600.0, dt_s=10.0, seed=42,
    )
    rng = np.random.default_rng(0)
    snr_series = []
    env.reset(seed=42)
    target_ue = 0

    for _ in range(env.num_steps):
        obs = env._get_obs()
        # Record max SNR for target UE
        visible = obs[target_ue]["visible_mask"]
        if visible.any():
            snr_series.append(obs[target_ue]["rates"][visible].max())
        else:
            snr_series.append(0.0)

        actions = np.array([
            rng.choice(np.where(obs[i]["visible_mask"])[0])
            if obs[i]["visible_count"] > 0 else 0
            for i in range(env.num_ues)
        ])
        _, _, done, _ = env.step(actions)
        if done:
            break

    snr = np.array(snr_series)
    # Lag-1 autocorrelation
    if len(snr) > 1 and snr.std() > 0:
        lag1 = np.corrcoef(snr[:-1], snr[1:])[0, 1]
    else:
        lag1 = 1.0

    if lag1 > 0.95:
        status = WARN
        msg = f"Lag-1 autocorrelation = {lag1:.4f} > 0.95 → TOO SMOOTH WARNING"
    else:
        status = PASS
        msg = f"Lag-1 autocorrelation = {lag1:.4f} (threshold=0.95) → OK"

    return status, msg


def run_all_validations():
    """Run all validation checks and print results."""
    checks = [
        ("FSPL analytical", validate_fspl),
        ("Elevation angle", validate_elevation),
        ("Rain statistics", validate_rain_statistics),
        ("Degradation test", validate_degradation),
        ("Autocorrelation", validate_autocorrelation),
    ]

    results = []
    all_pass = True
    for name, fn in checks:
        try:
            status, detail = fn()
        except Exception as e:
            status, detail = FAIL, str(e)
        results.append((name, status, detail))
        if status != PASS:
            all_pass = False
        print(f"  [{status}] {name}: {detail}")

    print()
    if all_pass:
        print("All validations passed.")
    else:
        print("Some checks failed or warned — review above.")
    return results


if __name__ == "__main__":
    print("=== LEO Satellite Handover Simulator Validation ===\n")
    run_all_validations()
