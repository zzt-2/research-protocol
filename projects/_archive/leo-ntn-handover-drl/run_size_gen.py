#!/usr/bin/env python3
"""Size generalization evaluation: load 20UE models, evaluate on 50/100UE."""

import json
from pathlib import Path
import numpy as np
import torch

PYTHON = str(Path.home() / '.venvs/torch/bin/python')
PROJECT = Path(__file__).resolve().parent

# Must import after setting path
import sys
sys.path.insert(0, str(PROJECT))
sys.path.insert(0, str(PROJECT / 'simulator'))

from c_gnn_ddqn import GNNQNetwork, GraphBuilder, evaluate, DEVICE
from simulator.environment import LEOSatHandoverEnv


def load_model(model_path):
    net = GNNQNetwork().to(DEVICE)
    ckpt = torch.load(model_path, map_location=DEVICE, weights_only=False)
    net.load_state_dict(ckpt['net'] if isinstance(ckpt, dict) and 'net' in ckpt else ckpt)
    net.eval()
    return net


def eval_size_gen(net, gb, num_ues, sat_capacity, seeds):
    results = []
    for s in seeds:
        env = LEOSatHandoverEnv(num_ues=num_ues, sat_capacity=sat_capacity, seed=s)
        m = evaluate(env, net, gb, s)
        results.append(m)
    avg = {k: np.mean([r[k] for r in results]) for k in results[0]}
    return avg, results


def main():
    gb = GraphBuilder()
    seeds = [1, 2, 3]
    eval_seeds = [100, 200, 300]
    results_dir = PROJECT / 'results'

    all_results = {}

    for seed in seeds:
        model_path = results_dir / f'E4-20-d20_s{seed}_model.pt'
        if not model_path.exists():
            # fallback to old naming (no seed suffix)
            model_path = results_dir / f'E4-20-d20_model.pt'
        if not model_path.exists():
            print(f"WARNING: model not found for seed {seed}, skipping")
            continue

        print(f"\nLoading model: {model_path}")
        net = load_model(model_path)

        # Same-scale 20UE baseline
        avg20, _ = eval_size_gen(net, gb, 20, 10, eval_seeds)
        print(f"  20UE same-scale: reward={avg20['reward']:.0f} | blk={avg20['mean_blocking_rate']:.4f}")

        # Size gen 20->50
        avg50, raw50 = eval_size_gen(net, gb, 50, 15, eval_seeds)
        print(f"  20->50 size gen: reward={avg50['reward']:.0f} | blk={avg50['mean_blocking_rate']:.4f} | retention={avg50['reward']/avg20['reward']*100:.1f}%")

        # Size gen 20->100
        avg100, raw100 = eval_size_gen(net, gb, 100, 25, eval_seeds)
        print(f"  20->100 size gen: reward={avg100['reward']:.0f} | blk={avg100['mean_blocking_rate']:.4f} | retention={avg100['reward']/avg20['reward']*100:.1f}%")

        all_results[f'seed_{seed}'] = {
            'train_seed': seed,
            'same_20ue': avg20,
            'sizegen_50ue': avg50,
            'sizegen_100ue': avg100,
            'retention_50': avg50['reward'] / avg20['reward'] * 100,
            'retention_100': avg100['reward'] / avg20['reward'] * 100,
        }

    # Summary
    if all_results:
        print("\n" + "=" * 70)
        print("Size Generalization Summary (eps_decay=20)")
        print("=" * 70)
        r50s = [v['retention_50'] for v in all_results.values()]
        r100s = [v['retention_100'] for v in all_results.values()]
        print(f"  Retention 20->50:  {np.mean(r50s):.1f}% ± {np.std(r50s):.1f}%")
        print(f"  Retention 20->100: {np.mean(r100s):.1f}% ± {np.std(r100s):.1f}%")

    out = results_dir / 'size_gen_d20_results.json'
    with open(out, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nSaved to {out}")


if __name__ == '__main__':
    main()
