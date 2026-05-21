"""Summarize E1 experiment results into comparison table."""
import sys
import os
import re
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(PROJECT_ROOT, 'results')

# Solver display order and labels
SOLVER_INFO = [
    ('grc_rank',              'B1: GRC'),
    ('sfc_pg_mlp',            'B3: PG-MLP'),
    ('sfc_ppo_dual_gcn',      'B5: DualGCN'),
    ('sfc_ppo_dual_gat+',     'B2: DualGAT+'),
    ('sfc_ppo_matching_gat',  'Ours: MatchingGAT'),
]

SEEDS = [0, 1, 2]


def read_result(solver, seed):
    path = os.path.join(RESULTS_DIR, f'{solver}_seed{seed}.txt')
    if not os.path.exists(path):
        return None
    data = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if ':' in line:
                k, v = line.split(':', 1)
                data[k.strip()] = v.strip()
    return data


def main():
    print("=" * 80)
    print("E1 Main Comparison: MatchingGAT vs B1-B5, WX100, 30ep, 3 seeds")
    print("=" * 80)

    all_results = {}
    for solver, label in SOLVER_INFO:
        seeds_data = []
        for seed in SEEDS:
            d = read_result(solver, seed)
            if d:
                seeds_data.append({
                    'seed': seed,
                    'ac': float(d.get('ac', 0)),
                    'r2c': float(d.get('r2c', 0)),
                    'elapsed': float(d.get('elapsed', 0)),
                })
        all_results[solver] = {'label': label, 'seeds': seeds_data}

    # Print table
    print(f"\n{'Solver':<28} {'AC (mean±std)':>16} {'R2C (mean±std)':>16} {'Seeds':>6} {'Time/seed':>10}")
    print("-" * 80)

    for solver, label in SOLVER_INFO:
        data = all_results[solver]
        seeds_data = data['seeds']
        n = len(seeds_data)

        if n == 0:
            print(f"{label:<28} {'—':>16} {'—':>16} {'0/3':>6} {'—':>10}")
            continue

        acs = [s['ac'] for s in seeds_data]
        r2cs = [s['r2c'] for s in seeds_data]
        times = [s['elapsed'] / 60 for s in seeds_data]

        if n >= 2:
            ac_str = f"{np.mean(acs):.4f}±{np.std(acs):.4f}"
            r2c_str = f"{np.mean(r2cs):.4f}±{np.std(r2cs):.4f}"
        else:
            ac_str = f"{acs[0]:.4f}"
            r2c_str = f"{r2cs[0]:.4f}"

        time_str = f"{np.mean(times):.1f}min"
        print(f"{label:<28} {ac_str:>16} {r2c_str:>16} {f'{n}/3':>6} {time_str:>10}")

    # R2C improvement over DualGAT+
    print("\n" + "=" * 80)
    print("R2C Improvement over B2 (PPO-DualGAT+)")
    print("=" * 80)

    dualgat_data = all_results['sfc_ppo_dual_gat+']['seeds']
    if dualgat_data:
        dualgat_r2c = np.mean([s['r2c'] for s in dualgat_data])
        print(f"\nDualGAT+ mean R2C: {dualgat_r2c:.4f}")

        for solver, label in SOLVER_INFO:
            if solver == 'sfc_ppo_dual_gat+':
                continue
            data = all_results[solver]['seeds']
            if not data:
                continue
            mean_r2c = np.mean([s['r2c'] for s in data])
            diff = mean_r2c - dualgat_r2c
            pct = (diff / dualgat_r2c) * 100
            marker = ""
            if solver == 'sfc_ppo_matching_gat':
                if pct >= 5.0:
                    marker = " ✅ PASS (≥5%)"
                elif pct >= 3.0:
                    marker = " ⚠️ MARGINAL (3-5%)"
                else:
                    marker = " ❌ FAIL (<3%)"
            print(f"  {label:<28}: {mean_r2c:.4f} ({diff:+.4f}, {pct:+.1f}%){marker}")

    # Check completeness
    print("\n" + "=" * 80)
    print("Completeness Check")
    print("=" * 80)
    missing = []
    for solver, label in SOLVER_INFO:
        for seed in SEEDS:
            if not read_result(solver, seed):
                missing.append(f"{label} seed={seed}")
    if missing:
        print(f"\n⚠ Missing {len(missing)} results:")
        for m in missing:
            print(f"  - {m}")
    else:
        print("\n✅ All results complete (5 solvers × 3 seeds)")


if __name__ == '__main__':
    main()
