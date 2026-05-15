"""Parameter sweep: N_LCT=3 gap robustness across traffic / range / GS count.

Quick 9-config grid: demand x Z_MAX, plus 3 GS variants.
Each config: 10 steps, 24x66=1584 sats, single-path routing.
Reports M1 gap between unlimited and N_LCT=3.
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from baselines.grid_fixed import GridFixedBaseline
from simulator import config


def run_config(n_lct, demand, z_max, n_gs, episode_steps=10, seed=42):
    """Run B1 with given params, return M1."""
    # Temporarily override config
    orig_z_max = config.Z_MAX
    orig_n_gs = config.N_GS
    config.Z_MAX = z_max
    config.N_GS = n_gs

    try:
        b = GridFixedBaseline(
            n_planes=24, sats_per_plane=66,
            episode_steps=episode_steps, seed=seed,
            n_lct=n_lct,
        )
        m, _ = b.run_episode(verbose=False)
    finally:
        config.Z_MAX = orig_z_max
        config.N_GS = orig_n_gs

    delivered = m.get('total_delivered', 0)
    demanded = m.get('total_demanded', 0)
    m1 = delivered / demanded if demanded > 0 else 0
    topo = b.topology_summary()
    return m1, topo['total_edges'], topo['edges_per_sat']


def main():
    demands = [5.0, 10.0, 20.0]
    z_maxes = [2000.0, 3000.0, 5000.0]
    n_gs_list = [50, 100, 200]

    print("=" * 80)
    print("  Parameter Sweep: N_LCT=3 gap robustness")
    print("  Grid: demand x Z_MAX (9 configs) + N_GS sensitivity (3 configs)")
    print("=" * 80)

    # --- Grid 1: demand x Z_MAX ---
    print(f"\n{'='*80}")
    print(f"  Grid: demand(gbps) x Z_MAX(km), N_GS=100, N_LCT=3, 10 steps")
    print(f"{'='*80}")

    results_grid = {}
    print(f"\n  {'demand\\Z_MAX':>14} | {'Z=2000km':>20} | {'Z=3000km':>20} | {'Z=5000km':>20}")
    print(f"  {'-'*14}-+-{'-'*20}-+-{'-'*20}-+-{'-'*20}")

    for demand in demands:
        row_unlimited = []
        row_lct3 = []
        row_gap = []

        for z_max in z_maxes:
            # Patch traffic base demand
            from simulator import traffic as traffic_mod
            orig_gen = traffic_mod.TrafficGenerator.generate

            def patched_gen(self, sat_lat, sat_lon, sat_alt, _demand=demand):
                return orig_gen(self, sat_lat, sat_lon, sat_alt, base_demand_gbps=_demand)

            traffic_mod.TrafficGenerator.generate = patched_gen

            try:
                m1_u, edges_u, eps_u = run_config(None, demand, z_max, 100)
                m1_3, edges_3, eps_3 = run_config(3, demand, z_max, 100)
            finally:
                traffic_mod.TrafficGenerator.generate = orig_gen

            gap = m1_u - m1_3
            row_unlimited.append(m1_u)
            row_lct3.append(m1_3)
            row_gap.append(gap)
            results_grid[(demand, z_max)] = {
                'm1_unlimited': m1_u, 'm1_lct3': m1_3,
                'gap': gap, 'edges_u': edges_u, 'edges_3': edges_3,
            }

        print(f"  d={demand:.0f}G unlimited |", end="")
        for v in row_unlimited:
            print(f" {v:>8.4f}          |", end="")
        print()
        print(f"  d={demand:.0f}G N_LCT=3   |", end="")
        for v in row_lct3:
            print(f" {v:>8.4f}          |", end="")
        print()
        print(f"  d={demand:.0f}G gap       |", end="")
        for v in row_gap:
            print(f" {v:>+8.4f} ({'OK' if v > 0.05 else '??':>2})   |", end="")
        print()
        print(f"  {'-'*14}-+-{'-'*20}-+-{'-'*20}-+-{'-'*20}")

    # --- Grid 2: N_GS sensitivity (fixed demand=10, Z_MAX=3000) ---
    print(f"\n{'='*80}")
    print(f"  N_GS sensitivity: demand=10Gbps, Z_MAX=3000km, N_LCT=3, 10 steps")
    print(f"{'='*80}")
    print(f"  {'N_GS':>6} | {'unlimited':>10} | {'N_LCT=3':>10} | {'gap':>10} | {'edges_3':>8} | {'e/sat':>6}")
    print(f"  {'-'*6}-+-{'-'*10}-+-{'-'*10}-+-{'-'*10}-+-{'-'*8}-+-{'-'*6}")

    for n_gs in n_gs_list:
        m1_u, edges_u, eps_u = run_config(None, 10.0, 3000.0, n_gs)
        m1_3, edges_3, eps_3 = run_config(3, 10.0, 3000.0, n_gs)
        gap = m1_u - m1_3
        print(f"  {n_gs:>6} | {m1_u:>10.4f} | {m1_3:>10.4f} | {gap:>+10.4f} | {edges_3:>8} | {eps_3:>6.1f}")

    # --- Summary ---
    print(f"\n{'='*80}")
    print(f"  RECOMMENDATION")
    print(f"{'='*80}")

    # Find config with best gap
    best_key = max(results_grid, key=lambda k: results_grid[k]['gap'])
    best = results_grid[best_key]
    print(f"  Best gap: demand={best_key[0]}Gbps, Z_MAX={best_key[1]}km")
    print(f"    unlimited={best['m1_unlimited']:.4f}, N_LCT=3={best['m1_lct3']:.4f}, gap={best['gap']:.4f}")

    # Count configs with gap > 5%
    good_configs = sum(1 for v in results_grid.values() if v['gap'] > 0.05)
    print(f"  Configs with gap > 5%: {good_configs}/{len(results_grid)}")

    avg_gap = np.mean([v['gap'] for v in results_grid.values()])
    print(f"  Average gap across all configs: {avg_gap:.4f}")


if __name__ == "__main__":
    t0 = time.time()
    main()
    print(f"\nTotal sweep time: {time.time() - t0:.1f}s")
