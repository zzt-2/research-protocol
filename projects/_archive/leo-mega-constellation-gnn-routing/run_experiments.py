#!/usr/bin/env python3
"""Ch1 batch experiment runner — multi-seed + multi-experiment.

Experiments:
  full:      Full architecture (PE + multi-scale), eval on target_720
  A1:        No PE (zero vectors), multi-scale training
  A2:        PE ON, single-scale (train_100 only)
  A3:        No PE + single-scale (train_100 only)
  same:      Full architecture, train+eval on 720 (same-scale control)
  random_pe: Random PE (same dim, random init), multi-scale training

Usage:
    cd /mnt/d/code/study/research-protocol
    ~/.venvs/torch/bin/python -u projects/leo-mega-constellation-gnn-routing/run_experiments.py --seeds 123 42 0 --experiments full A1 A2 A3 same random_pe
    ~/.venvs/torch/bin/python -u projects/leo-mega-constellation-gnn-routing/run_experiments.py --seeds 123 --experiments full  # single quick test
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from torch_geometric.loader import DataLoader

sys.path.insert(0, str(Path(__file__).resolve().parent / "simulator"))

from config import CONFIGS, TRAIN_CONFIGS, TARGET_CONFIG, PE_DIM, GNN_HEADS
from constellation import WalkerDelta
from snapshot import build_snapshot, get_orbital_pe_tensors, snapshot_to_pyg
from topology import build_adjacency
from routing import dijkstra_all_pairs, dijkstra
from models import RoutingActorCritic
from env import _build_neighbor_map

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Fixed hyperparameters (same as original experiments)
LAYERS, HIDDEN, EPOCHS, LR, BATCH_SIZE = 3, 128, 150, 1e-3, 64
N_TRAIN_SNAPSHOTS = 20
EVAL_SNAPSHOTS, EVAL_TMS, EVAL_FLOWS = 10, 5, 100

RESULTS_DIR = Path(__file__).resolve().parent / "simulator" / "results"
RESULTS_DIR.mkdir(exist_ok=True, parents=True)


def dijkstra_to_direction_labels(walker, next_hop_matrix):
    N, S, P = walker.N, walker.S, walker.P
    labels = np.full((N, N), -1, dtype=np.int64)
    for u in range(N):
        for d in range(N):
            if u == d or next_hop_matrix[u, d] < 0:
                continue
            nh = next_hop_matrix[u, d]
            sp, sk = divmod(u, S)
            dp, dk = divmod(nh, S)
            if sp == dp:
                labels[u, d] = 0 if dk == (sk + 1) % S else 1
            else:
                labels[u, d] = 2 if dp == (sp + 1) % P else 3
    return labels


def generate_dataset(walker, n_snapshots, rng, use_pe=True, random_pe=False, pe_rng=None):
    """Generate training dataset.

    Args:
        use_pe: If False, zero out PE dimensions.
        random_pe: If True, use random PE instead of orbital PE.
        pe_rng: Separate RNG for random PE generation (ensures same PE across experiments).
    """
    dataset = []
    plane_ids, sat_ids, P, S = get_orbital_pe_tensors(walker)
    N = walker.N

    for _ in range(n_snapshots):
        t = rng.uniform(0, walker.period)
        snap = build_snapshot(walker, t)
        adj = build_adjacency(walker.N, snap["edge_index"], snap["edge_delay"])
        _, next_hop = dijkstra_all_pairs(adj, walker.N)
        dir_labels = dijkstra_to_direction_labels(walker, next_hop)

        for d in range(N):
            data = snapshot_to_pyg(snap, d, plane_ids, sat_ids, P, S, PE_DIM)
            if random_pe:
                data.x = torch.cat(
                    [data.x[:, :1],
                     torch.randn(N, PE_DIM * 2, generator=torch.Generator().manual_seed(pe_rng.integers(0, 2**31)))],
                    dim=-1,
                )
            elif not use_pe:
                data.x = torch.cat([data.x[:, :1], torch.zeros(N, PE_DIM * 2)], dim=-1)
            data.y = torch.tensor(dir_labels[:, d], dtype=torch.long)
            dataset.append(data)
    return dataset


def _mask_pe(data, use_pe, random_pe, pe_rng, device):
    """Apply PE masking/randomization on the correct device."""
    if random_pe:
        N = data.x.shape[0]
        data.x = torch.cat(
            [data.x[:, :1],
             torch.randn(N, PE_DIM * 2, generator=torch.Generator().manual_seed(pe_rng.integers(0, 2**31)),
                          device=device)],
            dim=-1,
        )
    elif not use_pe:
        data.x = torch.cat([data.x[:, :1], torch.zeros(data.x.shape[0], PE_DIM * 2, device=device)], dim=-1)


def train_model(dataset, seed):
    """Train RoutingActorCritic on given dataset."""
    torch.manual_seed(seed)
    node_dim = 1 + PE_DIM * 2
    model = RoutingActorCritic(
        node_dim=node_dim, edge_dim=2, hidden=HIDDEN,
        n_layers=LAYERS, heads=GNN_HEADS,
    ).to(DEVICE)
    opt = torch.optim.Adam(model.parameters(), lr=LR)
    loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True,
                        generator=torch.Generator().manual_seed(seed))

    history = []
    for ep in range(1, EPOCHS + 1):
        model.train()
        total_loss, correct, total = 0, 0, 0
        for batch in loader:
            batch = batch.to(DEVICE)
            opt.zero_grad()
            logits, _ = model(batch)
            label_mask = batch.y >= 0
            masked_logits = logits.clone()
            masked_logits[~batch.dir_mask] = float("-inf")
            has_valid = batch.dir_mask.any(dim=-1) & label_mask
            if has_valid.sum() == 0:
                continue
            loss = F.cross_entropy(masked_logits[has_valid], batch.y[has_valid])
            loss.backward()
            opt.step()
            total_loss += loss.item() * has_valid.sum().item()
            preds = masked_logits[has_valid].argmax(dim=-1)
            correct += (preds == batch.y[has_valid]).sum().item()
            total += has_valid.sum().item()
        history.append(dict(
            epoch=ep,
            loss=total_loss / max(total, 1),
            accuracy=correct / max(total, 1),
        ))

    return model, history


@torch.no_grad()
def eval_weighted_dijkstra(model, config_name, use_pe=True, random_pe=False,
                           pe_rng=None, seed=123):
    """Evaluate model with weighted Dijkstra on target config."""
    rng = np.random.default_rng(seed)
    cfg = CONFIGS[config_name]
    walker = WalkerDelta(cfg["P"], cfg["S"], cfg["F"], cfg["alt"], cfg["inc"])
    plane_ids, sat_ids, P, S = get_orbital_pe_tensors(walker)
    N = walker.N
    model.eval()

    all_stretches = []
    all_gnn_delays = []
    all_djk_delays = []
    edge_load = {}
    total_inference_ms = 0.0

    for snap_i in range(EVAL_SNAPSHOTS):
        t = rng.uniform(0, walker.period)
        snap = build_snapshot(walker, t)
        adj_djk = build_adjacency(N, snap["edge_index"], snap["edge_delay"])
        dist_mat, _ = dijkstra_all_pairs(adj_djk, N)
        nmap = _build_neighbor_map(snap, walker.S, walker.P)

        for tm_i in range(EVAL_TMS):
            dest = int(rng.integers(0, N))
            data = snapshot_to_pyg(snap, dest, plane_ids, sat_ids, P, S, PE_DIM).to(DEVICE)
            _mask_pe(data, use_pe, random_pe, pe_rng, DEVICE)

            t_inf = time.perf_counter()
            logits, _ = model(data)
            torch.cuda.synchronize()
            total_inference_ms += (time.perf_counter() - t_inf) * 1000
            logits_np = logits.cpu().numpy()

            best_logit = np.max(logits_np, axis=-1)
            adj_w = [[] for _ in range(N)]
            edge_dir = {}
            for (u, d), (v, delay) in nmap.items():
                edge_dir[(u, v)] = d
                penalty = max(0.0, best_logit[u] - logits_np[u, d])
                adj_w[u].append((v, delay + penalty))

            candidates = np.array([i for i in range(N) if i != dest])
            n_src = min(EVAL_FLOWS, len(candidates))
            sources = rng.choice(candidates, size=n_src, replace=False)

            for src in sources:
                src = int(src)
                dist_w, parent = dijkstra(adj_w, src, N)
                if dist_w[dest] == np.inf or parent[dest] < 0:
                    continue
                cur, path = dest, []
                while cur != src and cur >= 0:
                    path.append(cur)
                    cur = parent[cur]
                if cur != src:
                    continue
                path.append(src)
                path.reverse()

                actual_delay = 0.0
                valid = True
                for i in range(len(path) - 1):
                    u, v = path[i], path[i + 1]
                    if (u, v) not in edge_dir:
                        valid = False
                        break
                    _, hop_delay = nmap[(u, edge_dir[(u, v)])]
                    actual_delay += hop_delay
                    edge_load[(u, v)] = edge_load.get((u, v), 0) + 1
                if not valid:
                    continue

                djk_delay = dist_mat[src, dest]
                if np.isfinite(djk_delay) and djk_delay > 0:
                    all_stretches.append(actual_delay / djk_delay)
                    all_gnn_delays.append(actual_delay)
                    all_djk_delays.append(djk_delay)

    stretches = np.array(all_stretches)
    n_attempted = EVAL_SNAPSHOTS * EVAL_TMS * EVAL_FLOWS

    loads = np.array(list(edge_load.values()), dtype=np.float64) if edge_load else np.array([0.0])

    return dict(
        n_flows=len(stretches),
        success_rate=len(stretches) / n_attempted if n_attempted else 0,
        mean_stretch=float(np.mean(stretches)) if len(stretches) else float("inf"),
        median_stretch=float(np.median(stretches)) if len(stretches) else float("inf"),
        p95_stretch=float(np.percentile(stretches, 95)) if len(stretches) else float("inf"),
        le12=float(np.mean(stretches <= 1.2) * 100) if len(stretches) else 0,
        le15=float(np.mean(stretches <= 1.5) * 100) if len(stretches) else 0,
        mean_gnn_delay=float(np.mean(all_gnn_delays)) if all_gnn_delays else float("inf"),
        mean_djk_delay=float(np.mean(all_djk_delays)) if all_djk_delays else float("inf"),
        link_util_mean=float(np.mean(loads)),
        link_util_max=float(np.max(loads)),
        link_util_std=float(np.std(loads)),
        inference_time_ms=total_inference_ms,
        per_flow_stretches=[float(s) for s in all_stretches],
    )


def run_experiment(experiment: str, seed: int) -> dict:
    """Run a single experiment with a single seed."""
    use_pe = experiment not in ("A1", "A3")
    random_pe = experiment == "random_pe"
    use_pe = False if random_pe else use_pe  # random_pe replaces orbital PE

    if experiment == "same":
        train_configs = [TARGET_CONFIG]
    elif experiment in ("A2", "A3"):
        train_configs = ["train_100"]
    else:
        train_configs = list(TRAIN_CONFIGS)

    rng = np.random.default_rng(seed)
    pe_rng = np.random.default_rng(seed + 10000) if random_pe else None

    # Generate training data
    t0 = time.time()
    all_train = []
    for cfg_name in train_configs:
        cfg = CONFIGS[cfg_name]
        walker = WalkerDelta(cfg["P"], cfg["S"], cfg["F"], cfg["alt"], cfg["inc"])
        data = generate_dataset(walker, N_TRAIN_SNAPSHOTS, rng,
                                use_pe=use_pe, random_pe=random_pe, pe_rng=pe_rng)
        print(f"    {cfg_name} ({walker.N} nodes): {len(data)} samples")
        all_train.extend(data)
    data_gen_time = time.time() - t0

    # Train
    t0 = time.time()
    model, history = train_model(all_train, seed)
    train_time = time.time() - t0
    final = history[-1]
    print(f"    Train: loss={final['loss']:.4f}, acc={final['accuracy']:.4f} ({train_time:.1f}s)")

    # Evaluate on target_720
    t0 = time.time()
    results = eval_weighted_dijkstra(
        model, TARGET_CONFIG,
        use_pe=use_pe, random_pe=random_pe, pe_rng=pe_rng,
        seed=123,  # fixed eval seed for all training seeds
    )
    eval_time = time.time() - t0

    results["experiment"] = experiment
    results["train_seed"] = seed
    results["eval_seed"] = 123
    results["train_configs"] = train_configs
    results["use_pe"] = use_pe and not random_pe
    results["random_pe"] = random_pe
    results["train_loss"] = final["loss"]
    results["train_accuracy"] = final["accuracy"]
    results["data_gen_time_s"] = data_gen_time
    results["train_time_s"] = train_time
    results["eval_time_s"] = eval_time
    results["loss_history"] = history

    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, nargs="+", default=[123, 42, 0])
    parser.add_argument("--experiments", nargs="+",
                        default=["full", "A1", "A2", "A3", "same", "random_pe"],
                        choices=["full", "A1", "A2", "A3", "same", "random_pe"])
    args = parser.parse_args()

    print("=" * 60)
    print("Ch1 MULTI-SEED EXPERIMENT SUITE")
    print("=" * 60)
    print(f"Device: {DEVICE}")
    print(f"Seeds: {args.seeds}")
    print(f"Experiments: {args.experiments}")
    print(f"Total runs: {len(args.seeds) * len(args.experiments)}")
    print(f"Results: {RESULTS_DIR}")
    print()

    all_results = {}
    total_runs = len(args.seeds) * len(args.experiments)
    completed = 0
    t_total = time.time()

    for experiment in args.experiments:
        exp_results = []
        for seed in args.seeds:
            completed += 1
            print(f"[{completed}/{total_runs}] {experiment} seed={seed}")
            t0 = time.time()

            result = run_experiment(experiment, seed)
            result["total_time_s"] = time.time() - t0
            exp_results.append(result)

            print(f"    stretch={result['mean_stretch']:.3f}  "
                  f"median={result['median_stretch']:.3f}  "
                  f"P95={result['p95_stretch']:.3f}  "
                  f"<=1.2x={result['le12']:.1f}%  "
                  f"<=1.5x={result['le15']:.1f}%  "
                  f"delay={result['mean_gnn_delay']:.2f}ms  "
                  f"t={result['total_time_s']:.0f}s")
            print()

        # Aggregate
        stretches = [r["mean_stretch"] for r in exp_results]
        delays = [r["mean_gnn_delay"] for r in exp_results]
        le12s = [r["le12"] for r in exp_results]
        all_results[experiment] = {
            "seeds": args.seeds,
            "mean_stretch": dict(mean=float(np.mean(stretches)),
                                 std=float(np.std(stretches)),
                                 values=stretches),
            "mean_delay": dict(mean=float(np.mean(delays)),
                               std=float(np.std(delays)),
                               values=delays),
            "le12": dict(mean=float(np.mean(le12s)),
                         std=float(np.std(le12s)),
                         values=le12s),
            "per_seed_results": exp_results,
        }

    # Summary table
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"{'Experiment':<12} {'Stretch':>10} {'±std':>8} {'Delay(ms)':>10} {'±std':>8} {'<=1.2x':>8}")
    print("-" * 60)
    for exp, data in all_results.items():
        s = data["mean_stretch"]
        d = data["mean_delay"]
        l = data["le12"]
        print(f"{exp:<12} {s['mean']:>10.3f} {s['std']:>8.3f} {d['mean']:>10.2f} {d['std']:>8.2f} {l['mean']:>7.1f}%")
    print()

    # Retention rate (same/cross, consistent with 06_formulas §7)
    if "full" in all_results and "same" in all_results:
        full_delay = all_results["full"]["mean_delay"]["mean"]
        same_delay = all_results["same"]["mean_delay"]["mean"]
        retention = same_delay / full_delay if full_delay > 0 else 0
        print(f"Delay retention (same/cross): {retention:.3f} ({retention*100:.1f}%)")

    elapsed = time.time() - t_total
    all_results["_meta"] = dict(
        total_time_s=elapsed,
        seeds=args.seeds,
        experiments=args.experiments,
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
    )
    print(f"Total: {elapsed:.0f}s ({elapsed/60:.1f} min)")

    # Save
    out_path = RESULTS_DIR / "ch1_multi_seed_results.json"
    with open(out_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
