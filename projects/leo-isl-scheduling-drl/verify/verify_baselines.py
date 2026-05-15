"""Verification for B1 (+Grid/Fixed) baseline.

Checks:
  1. Topology construction (edge counts, per-sat degree)
  2. Episode run (no crashes, metrics reasonable)
  3. M3 switch_rate = 0 (fixed topology)
  4. M1 throughput > 0
  5. Compare with random/greedy from Part A-checkpoint
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np

N_PLANES = 24
SATS_PER_PLANE = 8

from baselines.grid_fixed import GridFixedBaseline
from simulator.environment import ISLEnvironment
from simulator import config


def header(msg):
    print(f"\n{'='*60}\n  {msg}\n{'='*60}")


def check(label, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    suffix = f" — {detail}" if detail else ""
    print(f"  [{status}] {label}{suffix}")
    if not condition:
        raise AssertionError(f"FAILED: {label}")


def test_topology():
    header("B1 Topology Construction")
    b = GridFixedBaseline(n_planes=N_PLANES, sats_per_plane=SATS_PER_PLANE,
                          episode_steps=5)
    info = b.topology_summary()
    print(f"  Total sats: {b.n_sats}")
    print(f"  Intra-plane edges: {info['intra_edges']}")
    print(f"  Inter-plane edges: {info['inter_edges']}")
    print(f"  Total edges: {info['total_edges']}")
    print(f"  Avg edges/sat: {info['edges_per_sat']:.2f}")

    # Intra-plane: each plane has SPP edges (ring), total = P * SPP
    expected_intra = N_PLANES * SATS_PER_PLANE
    check("Intra-plane edges", info['intra_edges'] == expected_intra,
          f"{info['intra_edges']} == {expected_intra}")

    # Inter-plane: each sat contributes up to 2 inter edges, but deduplicated
    # Total should be roughly n_sats * 2 (each sat finds 2 nearest in next plane)
    # But deduplication reduces count since (i,j) == (j,i) for different plane pairs
    check("Inter-plane edges > 0", info['inter_edges'] > 0)
    check("Total edges > intra only", info['total_edges'] > expected_intra)

    # Each sat should have ~4 edges (2 intra + ~2 inter)
    check("Avg edges/sat ~ 4", 3.0 <= info['edges_per_sat'] <= 5.0,
          f"{info['edges_per_sat']:.2f}")

    return b


def test_episode():
    header("B1 Episode Run (24×8, 50 steps)")
    b = GridFixedBaseline(n_planes=N_PLANES, sats_per_plane=SATS_PER_PLANE,
                          episode_steps=50)
    metrics, total_reward = b.run_episode(verbose=True)

    print(f"\n  Metrics:")
    for k, v in metrics.items():
        if isinstance(v, float):
            print(f"    {k}: {v:.4f}")
        else:
            print(f"    {k}: {v}")

    check("M1 throughput > 0", metrics['M1_throughput'] > 0,
          f"{metrics['M1_throughput']:.4f}")
    check("M3 switch_rate = 0", metrics['M3_switch_rate'] == 0,
          "fixed topology has no switching")
    check("M4 blocking_rate < 1", metrics['M4_blocking_rate'] < 1.0,
          f"{metrics['M4_blocking_rate']:.4f}")
    check("M5 fairness > 0", metrics['M5_fairness'] > 0,
          f"{metrics['M5_fairness']:.4f}")
    check("Avg reward > 0", metrics['avg_reward'] > 0,
          f"{metrics['avg_reward']:.4f}")

    return metrics


def test_vs_dynamic():
    header("B1 (Fixed) vs Random/Greedy (Dynamic)")

    np32 = N_PLANES
    spp = SATS_PER_PLANE
    steps = 20

    # B1 fixed
    b1 = GridFixedBaseline(n_planes=np32, sats_per_plane=spp, episode_steps=steps)
    b1_m, b1_r = b1.run_episode()

    # Random policy
    env = ISLEnvironment(n_planes=np32, sats_per_plane=spp, episode_steps=steps)
    def random_policy(obs):
        return env.rng.random(obs['n_candidates'])
    rand_m, rand_r = env.run_episode(random_policy)

    # Greedy policy (always select all)
    def greedy_policy(obs):
        return np.ones(obs['n_candidates'])
    env2 = ISLEnvironment(n_planes=np32, sats_per_plane=spp, episode_steps=steps)
    greed_m, greed_r = env2.run_episode(greedy_policy)

    print(f"  {'Strategy':<15} {'M1_tput':>8} {'M3_switch':>10} {'M4_block':>9} {'M5_fair':>8} {'Avg_rwd':>8}")
    print(f"  {'-'*15} {'-'*8} {'-'*10} {'-'*9} {'-'*8} {'-'*8}")
    for name, m in [("B1 Fixed", b1_m), ("Random", rand_m), ("Greedy", greed_m)]:
        print(f"  {name:<15} {m['M1_throughput']:>8.4f} {m['M3_switch_rate']:>10.4f} "
              f"{m['M4_blocking_rate']:>9.4f} {m['M5_fairness']:>8.4f} {m['avg_reward']:>8.4f}")

    # B1 should outperform random (fixed grid is a reasonable baseline)
    check("B1 throughput > Random", b1_m['M1_throughput'] > rand_m['M1_throughput'],
          f"{b1_m['M1_throughput']:.4f} vs {rand_m['M1_throughput']:.4f}")

    # B1 should have zero switching
    check("B1 switch=0 < Random switch", b1_m['M3_switch_rate'] < rand_m['M3_switch_rate'])

    # Trend: Fixed > Random is the baseline floor
    print(f"\n  Relative improvement B1 vs Random: "
          f"+{(b1_m['M1_throughput']/max(rand_m['M1_throughput'],1e-6)-1)*100:.1f}% throughput")


if __name__ == '__main__':
    print("B1 (+Grid/Fixed) Baseline Verification")
    print(f"Constellation: {N_PLANES} planes × {SATS_PER_PLANE} sats = {N_PLANES*SATS_PER_PLANE}")

    b = test_topology()
    test_episode()
    test_vs_dynamic()

    header("ALL CHECKS PASSED")
