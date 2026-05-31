"""Ablation study: train MatchingGAT variants with one component removed at a time.

Usage:
    cd projects/nfv-sfc-vne
    python verify/run_ablation.py --epochs 5 --vnr 500
"""
import sys
import os
import time
import argparse

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIRNE_ROOT = os.path.join(PROJECT_ROOT, 'Virne')
sys.path.insert(0, VIRNE_ROOT)
sys.path.insert(0, PROJECT_ROOT)

import verify.run_sfc_baselines as bl
build_config = bl.build_config
train_baseline = bl.train_baseline

ABLATION_SOLVERS = [
    ('sfc_ppo_matching_gat', 'Full Model'),
    ('sfc_ppo_ablation_no_sfc_pe', 'w/o SFC PE'),
    ('sfc_ppo_ablation_no_cross_attn', 'w/o Cross-Attn'),
    ('sfc_ppo_ablation_no_edge_attr', 'w/o Edge Attr'),
]


def main():
    parser = argparse.ArgumentParser(description='Ablation study')
    parser.add_argument('--epochs', type=int, default=5)
    parser.add_argument('--vnr', type=int, default=500)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--gpu', type=int, default=0)
    parser.add_argument('--skip-full', action='store_true',
                        help='Skip full model (already trained)')
    args = parser.parse_args()

    results = []
    for solver_name, label in ABLATION_SOLVERS:
        if args.skip_full and solver_name == 'sfc_ppo_matching_gat':
            print(f"\n[SKIP] {label} ({solver_name})")
            continue

        print(f"\n{'#' * 60}")
        print(f"# Ablation: {label} ({solver_name})")
        print(f"{'#' * 60}")
        config = build_config(
            num_v_nets=args.vnr, seed=args.seed,
            solver_name=solver_name, num_epochs=args.epochs,
            use_cuda=True, gpu_id=args.gpu,
        )
        result = train_baseline(config)
        result['label'] = label
        results.append(result)

    # Summary table
    print(f"\n{'=' * 60}")
    print(f"ABLATION SUMMARY ({args.epochs} epochs, {args.vnr} VNRs/epoch)")
    print(f"{'=' * 60}")
    print(f"{'Variant':<25} {'AC':>8} {'R2C':>8} {'Time':>8}")
    print(f"{'-' * 25} {'-' * 8} {'-' * 8} {'-' * 8}")
    for r in results:
        print(f"{r['label']:<25} {r['ac']:>8.4f} {r['r2c']:>8.4f} {r['elapsed']/60:>7.1f}m")

    # Save summary
    results_dir = os.path.join(PROJECT_ROOT, 'results')
    os.makedirs(results_dir, exist_ok=True)
    summary_file = os.path.join(results_dir, 'ablation_summary.txt')
    with open(summary_file, 'w') as f:
        f.write(f"Ablation Study ({args.epochs} epochs, {args.vnr} VNRs/epoch)\n")
        f.write(f"{'Variant':<25} {'AC':>8} {'R2C':>8} {'Time':>8}\n")
        for r in results:
            f.write(f"{r['label']:<25} {r['ac']:>8.4f} {r['r2c']:>8.4f} {r['elapsed']/60:>7.1f}m\n")
    print(f"\nSummary saved to {summary_file}")


if __name__ == '__main__':
    main()
