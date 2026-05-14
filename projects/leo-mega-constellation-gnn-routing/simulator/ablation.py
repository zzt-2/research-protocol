"""Ablation experiments for Execute Step 2.

A1: Remove Orbital PE (zero vectors, keep dims)
A2: Single-scale training (train_100 only)
A3: A1 + A2 combined
same: Same-scale (train+test on 720) with full architecture

Usage:
    python ablation.py A1
    python ablation.py A2
    python ablation.py A3
    python ablation.py same
"""
import sys
import os
import time
import argparse
import numpy as np
import torch
import torch.nn.functional as F
from torch_geometric.loader import DataLoader

sys.path.insert(0, os.path.dirname(__file__))

from config import CONFIGS, TRAIN_CONFIGS, TARGET_CONFIG, GNN_HEADS, PE_DIM
from constellation import WalkerDelta
from snapshot import build_snapshot, get_orbital_pe_tensors, snapshot_to_pyg
from topology import build_adjacency
from routing import dijkstra_all_pairs, dijkstra
from models import RoutingActorCritic
from env import _build_neighbor_map

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Same hyperparameters as main experiment
LAYERS, HIDDEN, EPOCHS, LR, BATCH_SIZE = 3, 128, 150, 1e-3, 64
N_TRAIN_SNAPSHOTS = 20

# Same evaluation protocol as D023: 10 snapshots × 5 TMs × 100 flows
EVAL_SNAPSHOTS, EVAL_TMS, EVAL_FLOWS, EVAL_SEED = 10, 5, 100, 123


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


def generate_dataset(walker, n_snapshots, rng, use_pe=True):
    dataset = []
    plane_ids, sat_ids, P, S = get_orbital_pe_tensors(walker)
    N = walker.N

    for _ in range(n_snapshots):
        t = rng.uniform(0, walker.period)
        snap = build_snapshot(walker, t)
        adj = build_adjacency(N, snap['edge_index'], snap['edge_delay'])
        _, next_hop = dijkstra_all_pairs(adj, N)
        dir_labels = dijkstra_to_direction_labels(walker, next_hop)
        for d in range(N):
            data = snapshot_to_pyg(snap, d, plane_ids, sat_ids, P, S, PE_DIM)
            if not use_pe:
                data.x = torch.cat([data.x[:, :1], torch.zeros(N, PE_DIM * 2)], dim=-1)
            data.y = torch.tensor(dir_labels[:, d], dtype=torch.long)
            dataset.append(data)
    return dataset


def train_epoch(model, loader, opt, device):
    model.train()
    total_loss, correct, total = 0.0, 0, 0
    for batch in loader:
        batch = batch.to(device)
        opt.zero_grad()
        logits, _ = model(batch)
        label_mask = batch.y >= 0
        if label_mask.sum() == 0:
            continue
        masked_logits = logits.clone()
        masked_logits[~batch.dir_mask] = float('-inf')
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
    return total_loss / max(total, 1), correct / max(total, 1)


def eval_weighted_dijkstra(model, config_name, use_pe=True,
                           n_snapshots=10, n_tms=5, n_flows=100, seed=123):
    """Weighted Dijkstra evaluation matching main experiment protocol (D023)."""
    rng = np.random.default_rng(seed)
    cfg = CONFIGS[config_name]
    walker = WalkerDelta(cfg['P'], cfg['S'], cfg['F'], cfg['alt'], cfg['inc'])
    plane_ids, sat_ids, P, S = get_orbital_pe_tensors(walker)
    N = walker.N
    model.eval()

    all_stretches = []
    all_gnn_delays = []
    all_djk_delays = []

    for snap_i in range(n_snapshots):
        t = rng.uniform(0, walker.period)
        snap = build_snapshot(walker, t)
        adj_djk = build_adjacency(N, snap['edge_index'], snap['edge_delay'])
        dist_mat, _ = dijkstra_all_pairs(adj_djk, N)
        nmap = _build_neighbor_map(snap, walker.S, walker.P)

        for tm_i in range(n_tms):
            dest = int(rng.integers(0, N))
            data = snapshot_to_pyg(snap, dest, plane_ids, sat_ids, P, S, PE_DIM)
            if not use_pe:
                data.x = torch.cat([data.x[:, :1], torch.zeros(N, PE_DIM * 2)], dim=-1)
            data = data.to(DEVICE)

            with torch.no_grad():
                logits, _ = model(data)
            logits_np = logits.cpu().numpy()

            # Build weighted adjacency: weight = delay + relu(best_logit - logit)
            best_logit = np.max(logits_np, axis=-1)
            adj_w = [[] for _ in range(N)]
            edge_dir = {}
            for (u, d), (v, delay) in nmap.items():
                edge_dir[(u, v)] = d
                penalty = max(0.0, best_logit[u] - logits_np[u, d])
                adj_w[u].append((v, delay + penalty))

            # Sample source nodes
            candidates = np.array([i for i in range(N) if i != dest])
            n_src = min(n_flows, len(candidates))
            sources = rng.choice(candidates, size=n_src, replace=False)

            for src in sources:
                src = int(src)
                dist_w, parent = dijkstra(adj_w, src, N)
                if dist_w[dest] == np.inf or parent[dest] < 0:
                    continue
                # Trace path for actual delay
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
                if not valid:
                    continue

                djk_delay = dist_mat[src, dest]
                if np.isfinite(djk_delay) and djk_delay > 0:
                    all_stretches.append(actual_delay / djk_delay)
                    all_gnn_delays.append(actual_delay)
                    all_djk_delays.append(djk_delay)

        if (snap_i + 1) % 5 == 0:
            print(f"    {snap_i + 1}/{n_snapshots} snapshots done, "
                  f"{len(all_stretches)} flows so far")

    stretches = np.array(all_stretches)
    n_attempted = n_snapshots * n_tms * n_flows
    return dict(
        n_flows=len(stretches),
        success_rate=len(stretches) / n_attempted if n_attempted else 0,
        mean_stretch=float(np.mean(stretches)) if len(stretches) else float('inf'),
        median_stretch=float(np.median(stretches)) if len(stretches) else float('inf'),
        p95_stretch=float(np.percentile(stretches, 95)) if len(stretches) else float('inf'),
        le12=float(np.mean(stretches <= 1.2) * 100) if len(stretches) else 0,
        le15=float(np.mean(stretches <= 1.5) * 100) if len(stretches) else 0,
        mean_gnn_delay=float(np.mean(all_gnn_delays)) if all_gnn_delays else float('inf'),
        mean_djk_delay=float(np.mean(all_djk_delays)) if all_djk_delays else float('inf'),
    )


def run_ablation(ablation_type):
    t_start = time.time()
    print("=" * 60)
    print(f"ABLATION: {ablation_type}")
    print("=" * 60)

    use_pe = ablation_type not in ('A1', 'A3')

    if ablation_type == 'same':
        train_configs = [TARGET_CONFIG]
    elif ablation_type in ('A2', 'A3'):
        train_configs = ['train_100']
    else:
        train_configs = list(TRAIN_CONFIGS)

    print(f"  PE: {'ON' if use_pe else 'OFF (zero vectors)'}")
    print(f"  Train configs: {train_configs}")
    print(f"  Eval config: {TARGET_CONFIG}")
    print(f"  Device: {DEVICE}")

    rng = np.random.default_rng(42)
    torch.manual_seed(42)

    # [1] Generate training data
    print(f"\n[1] Generating training data...")
    t0 = time.time()
    all_train = []
    for cfg_name in train_configs:
        cfg = CONFIGS[cfg_name]
        walker = WalkerDelta(cfg['P'], cfg['S'], cfg['F'], cfg['alt'], cfg['inc'])
        data = generate_dataset(walker, N_TRAIN_SNAPSHOTS, rng, use_pe=use_pe)
        print(f"  {cfg_name} ({walker.N} nodes): {len(data)} samples")
        all_train.extend(data)
    print(f"  Total: {len(all_train)} samples ({time.time()-t0:.1f}s)")

    # [2] Model (same architecture)
    node_dim = 1 + PE_DIM * 2
    model = RoutingActorCritic(
        node_dim=node_dim, edge_dim=2, hidden=HIDDEN,
        n_layers=LAYERS, heads=GNN_HEADS,
    ).to(DEVICE)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"\n[2] Model: params={n_params:,}")

    # [3] Train
    opt = torch.optim.Adam(model.parameters(), lr=LR)
    loader = DataLoader(all_train, batch_size=BATCH_SIZE, shuffle=True)
    print(f"\n[3] Training {EPOCHS} epochs...")
    t0 = time.time()
    final_loss, final_acc = 0, 0
    for ep in range(1, EPOCHS + 1):
        loss, acc = train_epoch(model, loader, opt, DEVICE)
        if ep == 1 or ep % 50 == 0 or ep == EPOCHS:
            print(f"  Epoch {ep:3d}: loss={loss:.4f}, acc={acc:.4f}")
        final_loss, final_acc = loss, acc
    print(f"  Final: loss={final_loss:.4f}, acc={final_acc:.4f} ({time.time()-t0:.1f}s)")

    # [4] Evaluate on 720-star target
    print(f"\n[4] Weighted Dijkstra evaluation on {TARGET_CONFIG}...")
    print(f"  Protocol: {EVAL_SNAPSHOTS} snapshots × {EVAL_TMS} TMs × {EVAL_FLOWS} flows")
    t0 = time.time()
    results = eval_weighted_dijkstra(
        model, TARGET_CONFIG, use_pe=use_pe,
        n_snapshots=EVAL_SNAPSHOTS, n_tms=EVAL_TMS,
        n_flows=EVAL_FLOWS, seed=EVAL_SEED,
    )
    print(f"  Evaluation time: {time.time()-t0:.1f}s")

    # Save model
    save_path = os.path.join(os.path.dirname(__file__), f'ablation_{ablation_type}.pt')
    torch.save(model.state_dict(), save_path)

    # Print results
    print(f"\n{'='*60}")
    print(f"  RESULTS — {ablation_type} → {TARGET_CONFIG}")
    print(f"{'='*60}")
    print(f"  Flows:          {results['n_flows']}")
    print(f"  Success rate:   {results['success_rate']:.1%}")
    print(f"  Mean stretch:   {results['mean_stretch']:.3f}")
    print(f"  Median stretch: {results['median_stretch']:.3f}")
    print(f"  P95 stretch:    {results['p95_stretch']:.3f}")
    print(f"  ≤1.2x optimal:  {results['le12']:.1f}%")
    print(f"  ≤1.5x optimal:  {results['le15']:.1f}%")
    print(f"  GNN delay:      {results['mean_gnn_delay']:.2f} ms")
    print(f"  Djk delay:      {results['mean_djk_delay']:.2f} ms")
    delay_overhead = (results['mean_gnn_delay'] / results['mean_djk_delay'] - 1) * 100
    print(f"  Delay overhead: {delay_overhead:.1f}%")
    print(f"  Total time:     {time.time()-t_start:.1f}s")
    print(f"  Model saved:    {save_path}")
    print(f"{'='*60}")

    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('type', choices=['A1', 'A2', 'A3', 'same'])
    args = parser.parse_args()
    run_ablation(args.type)


if __name__ == '__main__':
    main()
