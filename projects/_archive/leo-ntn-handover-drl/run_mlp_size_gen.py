#!/usr/bin/env python3
"""MLP size generalization evaluation: load 20UE MLP models, evaluate on 50/100UE."""

import json
from pathlib import Path
import numpy as np
import torch

PROJECT = Path(__file__).resolve().parent
import sys
sys.path.insert(0, str(PROJECT))
sys.path.insert(0, str(PROJECT / 'simulator'))

from b2_topk import DuelingNet, evaluate, DEVICE, K
from simulator.environment import LEOSatHandoverEnv


def load_model(model_path):
    net = DuelingNet().to(DEVICE)
    ckpt = torch.load(model_path, map_location=DEVICE, weights_only=False)
    net.load_state_dict(ckpt['net'] if isinstance(ckpt, dict) and 'net' in ckpt else ckpt)
    net.eval()
    return net


def eval_size_gen(net, num_ues, sat_capacity, seeds):
    results = []
    for s in seeds:
        env = LEOSatHandoverEnv(num_ues=num_ues, sat_capacity=sat_capacity, seed=s)
        m = evaluate(env, net, s)
        results.append(m)
    avg = {k: np.mean([r[k] for r in results]) for k in results[0]}
    return avg, results


def main():
    seeds = [1, 2, 3]
    eval_seeds = [100, 200, 300]
    results_dir = PROJECT / 'results'

    all_results = {}

    for seed in seeds:
        model_path = results_dir / f'C6-20-d20_s{seed}_model.pt'
        if not model_path.exists():
            print(f"WARNING: model not found for seed {seed}, skipping")
            continue

        print(f"\nLoading MLP model: {model_path}")
        net = load_model(model_path)

        avg20, _ = eval_size_gen(net, 20, 10, eval_seeds)
        print(f"  20UE same-scale: reward={avg20['reward']:.0f} | blk={avg20['blocking']:.4f}")

        avg50, _ = eval_size_gen(net, 50, 15, eval_seeds)
        print(f"  20->50 size gen: reward={avg50['reward']:.0f} | blk={avg50['blocking']:.4f} | retention={avg50['reward']/avg20['reward']*100:.1f}%")

        avg100, _ = eval_size_gen(net, 100, 25, eval_seeds)
        print(f"  20->100 size gen: reward={avg100['reward']:.0f} | blk={avg100['blocking']:.4f} | retention={avg100['reward']/avg20['reward']*100:.1f}%")

        all_results[f'seed_{seed}'] = {
            'train_seed': seed,
            'same_20ue': avg20,
            'sizegen_50ue': avg50,
            'sizegen_100ue': avg100,
            'retention_50': avg50['reward'] / avg20['reward'] * 100,
            'retention_100': avg100['reward'] / avg20['reward'] * 100,
        }

    if all_results:
        print("\n" + "=" * 70)
        print("MLP Size Generalization Summary (eps_decay=20)")
        print("=" * 70)
        r50s = [v['retention_50'] for v in all_results.values()]
        r100s = [v['retention_100'] for v in all_results.values()]
        print(f"  Retention 20->50:  {np.mean(r50s):.1f}% ± {np.std(r50s):.1f}%")
        print(f"  Retention 20->100: {np.mean(r100s):.1f}% ± {np.std(r100s):.1f}%")

    out = results_dir / 'mlp_size_gen_d20_results.json'
    with open(out, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nSaved to {out}")


if __name__ == '__main__':
    main()
