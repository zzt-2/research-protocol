#!/usr/bin/env python3
"""Multi-seed training runs for Ch2 experiments."""

import argparse
import json
import subprocess
import sys
from pathlib import Path

PYTHON = str(Path.home() / '.venvs/torch/bin/python')
PROJECT = Path(__file__).resolve().parent

EXPERIMENTS = [
    # (name, script, num_ues, sat_capacity, extra_args)
    ('E4-20-d20', 'c_gnn_ddqn.py', 20, 10, '--eps_decay 20'),
    ('C6-20-d20', 'b2_topk.py', 20, 10, '--eps_decay 20'),
    ('E4-50-c15-d20', 'c_gnn_ddqn.py', 50, 15, '--eps_decay 20'),
    ('C6-50-c15-d20', 'b2_topk.py', 50, 15, '--eps_decay 20'),
]


def run_one(name, script, num_ues, sat_capacity, extra_args, seed):
    """Run a single experiment and return the result dict."""
    cmd = [
        PYTHON, str(PROJECT / script),
        '--name', name,
        '--num_ues', str(num_ues),
        '--sat_capacity', str(sat_capacity),
        '--train_seed', str(seed),
    ]
    if extra_args:
        cmd.extend(extra_args.split())

    print(f"\n{'='*60}")
    print(f"Running: {name} seed={seed}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}")

    result = subprocess.run(cmd, cwd=str(PROJECT), capture_output=False)
    if result.returncode != 0:
        print(f"FAILED: {name} seed={seed} (exit code {result.returncode})")
        return None

    # Load the output file
    result_file = PROJECT / 'results' / f'{name}_s{seed}_results.json'
    if not result_file.exists():
        print(f"WARNING: result file not found: {result_file}")
        return None

    with open(result_file) as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seeds', default='1,2,3', help='Comma-separated seeds')
    parser.add_argument('--experiments', default=None,
                        help='Comma-separated experiment names (default: all)')
    args = parser.parse_args()

    seeds = [int(s) for s in args.seeds.split(',')]
    exps = EXPERIMENTS
    if args.experiments:
        names = set(args.experiments.split(','))
        exps = [e for e in EXPERIMENTS if e[0] in names]

    all_results = {}
    for name, script, num_ues, sat_capacity, extra_args in exps:
        for seed in seeds:
            res = run_one(name, script, num_ues, sat_capacity, extra_args, seed)
            key = f"{name}_s{seed}"
            if res:
                all_results[key] = {
                    'experiment': name,
                    'seed': seed,
                    'script': script,
                    'num_ues': num_ues,
                    'sat_capacity': sat_capacity,
                    'eval': res.get('eval', []),
                    'config': res.get('config', {}),
                }
                # Print summary
                ev = res.get('eval', [])
                if ev:
                    avg_r = sum(e.get('reward', 0) for e in ev) / len(ev)
                    avg_blk = sum(e.get('blocking', e.get('mean_blocking_rate', 0)) for e in ev) / len(ev)
                    avg_tput = sum(e.get('mean_throughput_mbps', 0) for e in ev) / len(ev)
                    print(f"  -> {key}: reward={avg_r:.0f} | blk={avg_blk:.4f} | tput={avg_tput:.1f}Mbps")

    # Save summary
    summary_file = PROJECT / 'results' / 'multi_seed_summary.json'
    summary_file.parent.mkdir(exist_ok=True)
    with open(summary_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nSummary saved to {summary_file}")
    print(f"Total runs: {len(all_results)}")


if __name__ == '__main__':
    main()
