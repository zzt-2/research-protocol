"""run_checkpoint.py - Part A-checkpoint: MDP trial run with reward decomposition.

Runs one episode each with random and greedy policy, decomposes reward,
and checks quality gates from gw-experiment.md Part A-checkpoint.
"""

import sys
import numpy as np

from environment import SatelliteDAGEnv
from config import (
    REWARD_ETA_T, REWARD_ETA_E,
    REWARD_LAMBDA_1, REWARD_LAMBDA_2, REWARD_LAMBDA_3,
)


def run_and_decompose(env, policy="random"):
    """Run one episode, return result dict with reward decomposition."""
    if policy == "random":
        result = env.run_random_episode()
    else:
        result = env.run_greedy_episode()
    return result


def print_decomposition(label, result):
    """Print formatted decomposition table."""
    d = result["decomposition"]
    total_abs = abs(d["total"])

    components = [
        ("eta_t * T_norm", REWARD_ETA_T * d["T_norm"]),
        ("eta_e * E_norm", REWARD_ETA_E * d["E_norm"]),
        ("lambda1 * Phi1", REWARD_LAMBDA_1 * d["Phi1"]),
        ("lambda2 * Phi2", REWARD_LAMBDA_2 * d["Phi2"]),
        ("lambda3 * Phi3", REWARD_LAMBDA_3 * d["Phi3"]),
    ]

    print(f"--- {label} ---")
    print(f"Total reward: {d['total']:.4f}")
    print("| Component        | Value    | % of Total |")
    print("|------------------|----------|------------|")
    for name, val in components:
        pct = abs(val) / total_abs * 100 if total_abs > 0 else 0.0
        print(f"| {name:<16} | {val:>8.4f} | {pct:>8.1f}%   |")
    print()
    return components


def check_quality_gates(random_result, greedy_result, greedy_components):
    """Check quality gates and return number of failures."""
    d_greedy = greedy_result["decomposition"]
    total_abs = abs(d_greedy["total"])
    failures = 0

    # Gate 1: No single term > 95% of total absolute reward (greedy)
    max_pct = 0.0
    for name, val in greedy_components:
        pct = abs(val) / total_abs * 100 if total_abs > 0 else 0.0
        max_pct = max(max_pct, pct)
    gate1_pass = max_pct < 95.0
    status1 = "PASS" if gate1_pass else "FAIL"
    print(f"[{status1}] No single term > 95% (greedy): max={max_pct:.1f}%")
    if not gate1_pass:
        failures += 1

    # Gate 2: Greedy vs random gap > 10%
    r_random = random_result["decomposition"]["total"]
    r_greedy = d_greedy["total"]
    # Both should be negative; greedy should be less negative (better)
    gap = abs(r_random - r_greedy) / max(abs(r_random), 1e-9) * 100
    gate2_pass = gap > 10.0
    status2 = "PASS" if gate2_pass else "FAIL"
    print(f"[{status2}] Greedy vs Random gap > 10%: greedy={r_greedy:.4f}, "
          f"random={r_random:.4f}, gap={gap:.1f}%")
    if not gate2_pass:
        failures += 1

    # Gate 3: Key metrics differ between policies
    d_random = random_result["decomposition"]
    metrics_differ = (
        abs(d_random["T_norm"] - d_greedy["T_norm"]) > 1e-6
        or abs(d_random["E_norm"] - d_greedy["E_norm"]) > 1e-6
        or abs(d_random["Phi1"] - d_greedy["Phi1"]) > 1e-6
    )
    status3 = "PASS" if metrics_differ else "FAIL"
    print(f"[{status3}] Key metrics differ: "
          f"T_norm(r={d_random['T_norm']:.4f}, g={d_greedy['T_norm']:.4f}), "
          f"E_norm(r={d_random['E_norm']:.4f}, g={d_greedy['E_norm']:.4f}), "
          f"Phi1(r={d_random['Phi1']:.4f}, g={d_greedy['Phi1']:.4f})")
    if not metrics_differ:
        failures += 1

    return failures


def main():
    print("=== Part A-checkpoint: MDP Trial Run ===\n")

    env = SatelliteDAGEnv(seed=42)

    # Random policy
    random_result = run_and_decompose(env, "random")
    random_components = print_decomposition("Random Policy", random_result)

    # Greedy policy
    greedy_result = run_and_decompose(env, "greedy")
    greedy_components = print_decomposition("Greedy Policy", greedy_result)

    # Quality gates
    print("--- Quality Gates ---")
    failures = check_quality_gates(random_result, greedy_result, greedy_components)
    print(f"\nGates: {3 - failures}/3 passed")

    return failures == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
