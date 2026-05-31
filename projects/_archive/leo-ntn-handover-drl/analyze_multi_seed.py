#!/usr/bin/env python3
"""Analyze multi-seed experiment results and produce summary tables."""

import json
from pathlib import Path
import numpy as np

RESULTS_DIR = Path(__file__).resolve().parent / 'results'

EXPERIMENTS = [
    ('E4-20', 'GNN', 20, 10),
    ('C6-20', 'MLP', 20, 10),
    ('E4-50-c15', 'GNN', 50, 15),
    ('C6-50-c15', 'MLP', 50, 15),
    ('E4-100-c25', 'GNN', 100, 25),
    ('C6-100-c25', 'MLP', 100, 25),
    ('E4-30', 'GNN', 30, 12),
    ('C6-30', 'MLP', 30, 12),
    ('E4-40', 'GNN', 40, 14),
    ('C6-40', 'MLP', 40, 14),
]

SEEDS = [1, 2, 3]
EVAL_KEYS = ['reward', 'mean_blocking_rate', 'total_handovers',
             'mean_throughput_mbps', 'jain_fairness', 'ping_pong_rate']


def load_results():
    """Load all multi-seed results."""
    data = {}
    for exp_name, method, n_ues, cap in EXPERIMENTS:
        seeds_data = []
        for seed in SEEDS:
            f = RESULTS_DIR / f'{exp_name}_s{seed}_results.json'
            if f.exists():
                d = json.load(open(f))
                seeds_data.append({'train_seed': seed, 'eval': d.get('eval', [])})
        if seeds_data:
            data[exp_name] = {
                'method': method,
                'num_ues': n_ues,
                'sat_capacity': cap,
                'seeds': seeds_data,
            }
    return data


def aggregate(data):
    """Aggregate across training seeds and eval seeds."""
    rows = []
    for exp_name, info in data.items():
        all_evals = []
        for sd in info['seeds']:
            all_evals.extend(sd['eval'])

        if not all_evals:
            continue

        row = {
            'experiment': exp_name,
            'method': info['method'],
            'num_ues': info['num_ues'],
            'sat_capacity': info['sat_capacity'],
            'n_train_seeds': len(info['seeds']),
            'n_eval_seeds': len(all_evals),
        }

        for key in EVAL_KEYS:
            vals = [e[key] for e in all_evals if key in e and e[key] is not None]
            if vals:
                row[f'{key}_mean'] = float(np.mean(vals))
                row[f'{key}_std'] = float(np.std(vals))
            else:
                row[f'{key}_mean'] = None
                row[f'{key}_std'] = None

        rows.append(row)
    return rows


def print_comparison_table(rows):
    """Print formatted comparison table grouped by UE count."""
    print("=" * 100)
    print(f"{'Experiment':<15} {'Method':<6} {'UE':>3} {'Reward':>12} {'Block%':>8} "
          f"{'HO':>8} {'Tput(Mbps)':>12} {'Jain':>6} {'PP-rate':>8}")
    print("-" * 100)

    for r in rows:
        reward = f"{r['reward_mean']:.0f}±{r['reward_std']:.0f}" if r.get('reward_mean') is not None else "N/A"
        blk = f"{r['mean_blocking_rate_mean']*100:.2f}" if r.get('mean_blocking_rate_mean') is not None else "N/A"
        ho = f"{r['total_handovers_mean']:.0f}" if r.get('total_handovers_mean') is not None else "N/A"
        tput = f"{r['mean_throughput_mbps_mean']:.1f}" if r.get('mean_throughput_mbps_mean') is not None else "N/A"
        jain = f"{r['jain_fairness_mean']:.3f}" if r.get('jain_fairness_mean') is not None else "N/A"
        pp = f"{r['ping_pong_rate_mean']:.3f}" if r.get('ping_pong_rate_mean') is not None else "N/A"

        print(f"{r['experiment']:<15} {r['method']:<6} {r['num_ues']:>3} {reward:>12} {blk:>8} "
              f"{ho:>8} {tput:>12} {jain:>6} {pp:>8}")

    print("=" * 100)


def print_gnn_advantage(rows):
    """Print GNN vs MLP advantage by UE count."""
    print("\n" + "=" * 60)
    print("GNN vs MLP Advantage (multi-seed)")
    print("=" * 60)

    for n_ues in [20, 30, 40, 50, 100]:
        gnn_rows = [r for r in rows if r['num_ues'] == n_ues and r['method'] == 'GNN']
        mlp_rows = [r for r in rows if r['num_ues'] == n_ues and r['method'] == 'MLP']

        if not gnn_rows or not mlp_rows:
            continue

        g = gnn_rows[0]
        m = mlp_rows[0]

        if g.get('reward_mean') and m.get('reward_mean'):
            gap = (g['reward_mean'] - m['reward_mean']) / abs(m['reward_mean']) * 100
            print(f"  {n_ues:>3} UE: GNN {g['reward_mean']:.0f} vs MLP {m['reward_mean']:.0f} → {gap:+.1f}%")

    print("=" * 60)


def main():
    data = load_results()
    if not data:
        print("No multi-seed results found yet. Run run_multi_seed.py first.")
        return

    print(f"Loaded {len(data)} experiments")
    rows = aggregate(data)
    print_comparison_table(rows)
    print_gnn_advantage(rows)

    # Save as JSON for further use
    out = RESULTS_DIR / 'analysis_summary.json'
    with open(out, 'w') as f:
        json.dump(rows, f, indent=2)
    print(f"\nSaved to {out}")


if __name__ == '__main__':
    main()
