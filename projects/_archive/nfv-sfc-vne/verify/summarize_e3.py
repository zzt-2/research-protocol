"""Summarize E3 ablation results."""
import sys
import os
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(PROJECT_ROOT, 'results')

ABLATION_INFO = [
    ('sfc_ppo_matching_gat',              'Full Model'),
    ('sfc_ppo_ablation_no_sfc_pe',        'w/o SFC PE (A1)'),
    ('sfc_ppo_ablation_no_cross_attn',    'w/o Cross-Attn (A2)'),
    ('sfc_ppo_ablation_no_edge_attr',     'w/o Edge Attr (A3)'),
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
    print("=" * 75)
    print("E3: Ablation Study — MatchingGAT components on WX100, 30ep, 3 seeds")
    print("=" * 75)

    all_results = {}
    for solver, label in ABLATION_INFO:
        seeds_data = []
        for seed in SEEDS:
            d = read_result(solver, seed)
            if d:
                seeds_data.append({
                    'seed': seed,
                    'r2c': float(d.get('r2c', 0)),
                    'ac': float(d.get('ac', 0)),
                })
        all_results[solver] = {'label': label, 'seeds': seeds_data}

    # Print table
    print(f"\n{'Variant':<30} {'R2C (mean±std)':>16} {'AC (mean±std)':>16} {'Seeds':>6}")
    print("-" * 75)

    full_r2c = None
    for solver, label in ABLATION_INFO:
        data = all_results[solver]
        seeds_data = data['seeds']
        n = len(seeds_data)

        if n == 0:
            print(f"{label:<30} {'—':>16} {'—':>16} {'0/3':>6}")
            continue

        r2cs = [s['r2c'] for s in seeds_data]
        acs = [s['ac'] for s in seeds_data]

        if n >= 2:
            r2c_str = f"{np.mean(r2cs):.4f}±{np.std(r2cs):.4f}"
            ac_str = f"{np.mean(acs):.4f}±{np.std(acs):.4f}"
        else:
            r2c_str = f"{r2cs[0]:.4f}"
            ac_str = f"{acs[0]:.4f}"

        print(f"{label:<30} {r2c_str:>16} {ac_str:>16} {f'{n}/3':>6}")

        if solver == 'sfc_ppo_matching_gat':
            full_r2c = np.mean(r2cs)

    # Component contribution analysis
    if full_r2c is not None:
        print(f"\n{'=' * 75}")
        print(f"Component Contribution (Full Model R2C = {full_r2c:.4f})")
        print(f"{'=' * 75}")

        for solver, label in ABLATION_INFO[1:]:  # Skip full model
            data = all_results[solver]
            seeds_data = data['seeds']
            if not seeds_data:
                continue
            ablation_r2c = np.mean([s['r2c'] for s in seeds_data])
            drop = full_r2c - ablation_r2c
            pct = (drop / full_r2c) * 100
            status = "✅ ≥1.5%" if pct >= 1.5 else "⚠️ <1.5%"
            print(f"  {label:<30}: ΔR2C = {drop:+.4f} ({pct:+.1f}%) {status}")

    # Completeness
    print(f"\n{'=' * 75}")
    missing = []
    for solver, label in ABLATION_INFO:
        for seed in SEEDS:
            if not read_result(solver, seed):
                missing.append(f"{label} seed={seed}")
    if missing:
        print(f"⚠ Missing {len(missing)} results")
        for m in missing:
            print(f"  - {m}")
    else:
        print("✅ All ablation results complete (4 variants × 3 seeds)")


if __name__ == '__main__':
    main()
