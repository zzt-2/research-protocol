"""Generate supervised dataset from B1 grid topology labels.

At 24×20 scale, the grid topology IS the route-aware optimal (D024, D029):
  - Perfect 4-regular graph, all 960 edges survive at every time step
  - N_LCT=4 blocks all single-edge swaps (every satellite at capacity)
  - Greedy route-aware search is infeasible (146ms/route × 2600 trials/round)
  - D024: random swaps improve ≤0.0015 (noise level)

Direction 3 (fair comparison): GNN learns to reproduce grid topology,
validating the architecture and training pipeline.

Output format matches previous datasets — train_supervised.py works unchanged.
"""

import os
import json
import numpy as np
import torch
from torch_geometric.data import Data
from collections import defaultdict

from . import config
from .environment import ISLEnvironment


def build_grid_topology(env, n_lct=None):
    """Build B1 +Grid topology at t=0, pruned to n_lct edges per satellite."""
    n_lct = n_lct or config.N_LCT
    positions = env.orbit.propagate(0)
    n_planes = env.orbit.n_planes
    spp = env.orbit.sats_per_plane

    def sat_id(p, s):
        return p * spp + s

    edges = {}

    # Intra-plane: adjacent neighbors (wrapping)
    for p in range(n_planes):
        for s in range(spp):
            i = sat_id(p, s)
            j = sat_id(p, (s + 1) % spp)
            edges[(min(i, j), max(i, j))] = 'intra'

    # Inter-plane: 2 nearest in each adjacent plane
    for p in range(n_planes):
        p_next = (p + 1) % n_planes
        for s in range(spp):
            i = sat_id(p, s)
            candidates = []
            for s2 in range(spp):
                j = sat_id(p_next, s2)
                d = np.linalg.norm(positions[i] - positions[j])
                if d < config.Z_MAX:
                    candidates.append((d, j))
            candidates.sort()
            for k in range(min(2, len(candidates))):
                j = candidates[k][1]
                key = (min(i, j), max(i, j))
                if key not in edges:
                    edges[key] = 'inter'

    # Prune to n_lct per satellite (keep shortest)
    sat_edges = defaultdict(list)
    for (i, j), etype in edges.items():
        d = np.linalg.norm(positions[i] - positions[j])
        sat_edges[i].append((d, (i, j)))
        sat_edges[j].append((d, (i, j)))

    keep = set()
    for sat, elist in sat_edges.items():
        elist.sort()
        for _, key in elist[:n_lct]:
            keep.add(key)

    return {k: v for k, v in edges.items() if k in keep}


def generate_grid_dataset(
    n_planes=24,
    sats_per_plane=20,
    n_snapshots=500,
    tau_sample=50.0,
    seed=42,
    output_dir=None,
):
    """Generate dataset with B1 grid topology as labels.

    For each time snapshot, the label is the grid topology filtered to
    currently valid candidates.  This produces clean, expert-level labels
    for the GNN to learn.

    Args:
        n_snapshots: number of time snapshots
        tau_sample: time gap between snapshots (seconds)
        seed: random seed
        output_dir: output directory (auto-generated if None)
    """
    if output_dir is None:
        output_dir = f"data/grid_dataset_{n_planes}x{sats_per_plane}"
    os.makedirs(output_dir, exist_ok=True)

    env = ISLEnvironment(n_planes=n_planes, sats_per_plane=sats_per_plane, seed=seed)
    grid_edges = build_grid_topology(env)
    grid_set = set(grid_edges.keys())

    print(f"Grid topology: {len(grid_edges)} edges "
          f"({sum(1 for v in grid_edges.values() if v == 'intra')} intra + "
          f"{sum(1 for v in grid_edges.values() if v == 'inter')} inter)")

    all_stats = []

    for idx in range(n_snapshots):
        t = idx * tau_sample

        # Setup env state at time t
        env._t = t
        env._positions = env.orbit.propagate(t)
        env._candidate_edges = env.vis.compute(env._positions)
        lat, lon, alt = env.orbit.eci_to_lla(env._positions, t)
        env._flows = env.traffic.generate(lat, lon, alt)

        # Filter grid edges to current candidates
        cand_set = {(min(i, j), max(i, j)) for i, j, _ in env._candidate_edges}
        active_grid = {e for e in grid_set if e in cand_set}

        # Set topology and build obs
        env.set_isl_configuration(active_grid)
        obs = env._build_obs()

        # Build PyG Data
        node_feat = torch.tensor(obs['node_features'], dtype=torch.float32)
        edge_feat = torch.tensor(obs['edge_features'], dtype=torch.float32)

        edge_list = obs['candidate_edges']
        if edge_list:
            edge_index = torch.tensor(
                [[i, j] for i, j, _ in edge_list], dtype=torch.long
            ).t().contiguous()
        else:
            edge_index = torch.zeros((2, 0), dtype=torch.long)

        # Binary labels: 1 if grid edge, 0 otherwise
        edge_labels = torch.zeros(len(edge_list), dtype=torch.float32)
        for idx_e, (i, j, _) in enumerate(edge_list):
            key = (min(i, j), max(i, j))
            if key in active_grid:
                edge_labels[idx_e] = 1.0

        # Traffic-weighted edge weights
        n = env.n_sats
        supply = np.zeros(n)
        demand = np.zeros(n)
        for src, dst, dem in env._flows:
            if 0 <= src < n and 0 <= dst < n:
                supply[src] += dem
                demand[dst] += dem
        edge_weights = torch.tensor(
            [supply[i] + supply[j] + demand[i] + demand[j]
             for i, j, _ in edge_list],
            dtype=torch.float32,
        )

        data = Data(
            x=node_feat,
            edge_index=edge_index,
            edge_attr=edge_feat,
            edge_labels=edge_labels,
            edge_weights=edge_weights,
            n_sats=env.n_sats,
            snapshot_idx=idx,
            time=t,
        )
        torch.save(data, os.path.join(output_dir, f"snapshot_{idx:04d}.pt"))

        n_selected = int(edge_labels.sum().item())
        all_stats.append({
            'idx': idx,
            'time': t,
            'n_candidates': len(edge_list),
            'n_selected': n_selected,
            'n_grid_surviving': len(active_grid),
        })

        if (idx + 1) % 100 == 0:
            print(f"  Generated {idx+1}/{n_snapshots} snapshots")

    # Save manifest
    manifest = {
        'method': 'grid_topology',
        'n_snapshots': n_snapshots,
        'n_planes': n_planes,
        'sats_per_plane': sats_per_plane,
        'n_lct': config.N_LCT,
        'tau_sample': tau_sample,
        'grid_edges_total': len(grid_set),
        'stats': all_stats,
    }
    with open(os.path.join(output_dir, 'manifest.json'), 'w') as f:
        json.dump(manifest, f, indent=2)

    result = {
        'n_snapshots': n_snapshots,
        'avg_candidates': float(np.mean([s['n_candidates'] for s in all_stats])),
        'avg_selected': float(np.mean([s['n_selected'] for s in all_stats])),
        'avg_grid_surviving': float(np.mean([s['n_grid_surviving'] for s in all_stats])),
        'output_dir': output_dir,
    }
    print(f"Grid dataset generated: {result}")
    return result


def load_dataset(dataset_dir, train_ratio=0.8):
    """Load dataset from directory.

    Returns:
        train_data: list of PyG Data
        test_data: list of PyG Data
    """
    with open(os.path.join(dataset_dir, 'manifest.json')) as f:
        manifest = json.load(f)

    all_data = []
    for s in manifest['stats']:
        path = os.path.join(dataset_dir, f"snapshot_{s['idx']:04d}.pt")
        if os.path.exists(path) and s['n_candidates'] > 0:
            all_data.append(torch.load(path, weights_only=False))

    split = int(len(all_data) * train_ratio)
    return all_data[:split], all_data[split:]


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Generate grid topology dataset')
    parser.add_argument('--n-planes', type=int, default=24)
    parser.add_argument('--sats-per-plane', type=int, default=20)
    parser.add_argument('--n-snapshots', type=int, default=500)
    parser.add_argument('--tau-sample', type=float, default=50.0)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--output-dir', type=str, default=None)
    args = parser.parse_args()

    generate_grid_dataset(
        n_planes=args.n_planes,
        sats_per_plane=args.sats_per_plane,
        n_snapshots=args.n_snapshots,
        tau_sample=args.tau_sample,
        seed=args.seed,
        output_dir=args.output_dir,
    )
