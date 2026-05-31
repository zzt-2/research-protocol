"""Quick test: supervised training on small scale, zero-shot evaluation on 720 stars.

Verifies GNN + Orbital PE size generalization for Walker-Delta routing.
Uses Dijkstra labels for training (not RL — that's for full experiments).
"""
import sys, os, time
import numpy as np
import torch
import torch.nn.functional as F
from torch_geometric.loader import DataLoader

sys.path.insert(0, os.path.dirname(__file__))

from config import CONFIGS, TRAIN_CONFIGS, TARGET_CONFIG, GNN_LAYERS, GNN_HIDDEN, GNN_HEADS, PE_DIM
from constellation import WalkerDelta
from snapshot import build_snapshot, get_orbital_pe_tensors, snapshot_to_pyg
from topology import build_adjacency
from routing import dijkstra_all_pairs
from models import RoutingGNN

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
N_TRAIN_SNAPSHOTS = 20
N_TEST_SNAPSHOTS = 3
EPOCHS = 150
LR = 1e-3
BATCH_SIZE = 64


def dijkstra_to_direction_labels(walker, next_hop_matrix):
    """Convert Dijkstra next-hop table to 4-direction labels.

    Returns (N, N) int array: labels[u][d] = direction 0-3, or -1.
    """
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


def generate_routing_dataset(walker, n_snapshots, rng):
    """Generate supervised training data: one PyG Data per (snapshot, destination)."""
    dataset = []
    plane_ids, sat_ids, P, S = get_orbital_pe_tensors(walker)

    for _ in range(n_snapshots):
        t = rng.uniform(0, walker.period)
        snap = build_snapshot(walker, t)

        adj = build_adjacency(walker.N, snap['edge_index'], snap['edge_delay'])
        dist_mat, next_hop = dijkstra_all_pairs(adj, walker.N)
        dir_labels = dijkstra_to_direction_labels(walker, next_hop)

        for d in range(walker.N):
            data = snapshot_to_pyg(snap, d, plane_ids, sat_ids, P, S, pe_dim=32)
            data.y = torch.tensor(dir_labels[:, d], dtype=torch.long)
            dataset.append(data)

    return dataset


def train_epoch(model, loader, opt, device):
    model.train()
    total_loss = 0
    correct = 0
    total = 0

    for batch in loader:
        batch = batch.to(device)
        opt.zero_grad()

        logits = model(batch)
        label_mask = batch.y >= 0
        if label_mask.sum() == 0:
            continue

        # Mask unavailable directions
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


@torch.no_grad()
def evaluate(model, loader, device):
    model.eval()
    correct = 0
    total = 0

    for batch in loader:
        batch = batch.to(device)
        logits = model(batch)
        label_mask = batch.y >= 0
        masked_logits = logits.clone()
        masked_logits[~batch.dir_mask] = float('-inf')
        has_valid = batch.dir_mask.any(dim=-1) & label_mask
        if has_valid.sum() == 0:
            continue

        preds = masked_logits[has_valid].argmax(dim=-1)
        correct += (preds == batch.y[has_valid]).sum().item()
        total += has_valid.sum().item()

    return correct / max(total, 1)


def trace_path(preds, walker, snap, src, dst):
    """Trace path using predicted directions. Returns (delay_ms, success)."""
    S, P = walker.S, walker.P

    neighbor_map = {}
    for e in range(snap['edge_index'].shape[1]):
        u, v = int(snap['edge_index'][0, e]), int(snap['edge_index'][1, e])
        sp, sk = divmod(u, S)
        dp, dk = divmod(v, S)
        if sp == dp:
            d = 0 if dk == (sk + 1) % S else 1
        else:
            d = 2 if dp == (sp + 1) % P else 3
        neighbor_map[(u, d)] = (v, snap['edge_delay'][e])

    cur, delay, visited = src, 0.0, {src}
    for _ in range(walker.N * 2):
        if cur == dst:
            return delay, True
        d = preds[cur]
        if (cur, d) not in neighbor_map:
            return float('inf'), False
        nxt, hop_delay = neighbor_map[(cur, d)]
        delay += hop_delay
        if nxt in visited:
            return float('inf'), False
        visited.add(nxt)
        cur = nxt
    return float('inf'), False


@torch.no_grad()
def evaluate_path_quality(model, walker, snap, n_flows=200, rng=None):
    """Path quality: stretch vs Dijkstra, success rate."""
    if rng is None:
        rng = np.random.default_rng()
    model.eval()
    device = next(model.parameters()).device
    plane_ids, sat_ids, P, S = get_orbital_pe_tensors(walker)

    adj = build_adjacency(walker.N, snap['edge_index'], snap['edge_delay'])
    dist_mat, _ = dijkstra_all_pairs(adj, walker.N)

    flows = rng.integers(0, walker.N, size=(n_flows, 2))
    for i in range(n_flows):
        while flows[i, 0] == flows[i, 1]:
            flows[i, 1] = rng.integers(0, walker.N)

    stretches, gnn_delays, djk_delays = [], [], []
    failures = 0

    for src, dst in flows:
        data = snapshot_to_pyg(snap, int(dst), plane_ids, sat_ids, P, S, pe_dim=32)
        data = data.to(device)
        logits = model(data)
        masked = logits.clone()
        masked[~data.dir_mask] = float('-inf')
        preds = masked.argmax(dim=-1).cpu().numpy()

        gnn_d, ok = trace_path(preds, walker, snap, int(src), int(dst))
        djk_d = dist_mat[src, dst]

        if ok and np.isfinite(djk_d) and djk_d > 0:
            stretches.append(gnn_d / djk_d)
            gnn_delays.append(gnn_d)
            djk_delays.append(djk_d)
        else:
            failures += 1

    return dict(
        mean_stretch=np.mean(stretches) if stretches else float('inf'),
        p95_stretch=np.percentile(stretches, 95) if stretches else float('inf'),
        mean_gnn_delay=np.mean(gnn_delays) if gnn_delays else float('inf'),
        mean_dijkstra_delay=np.mean(djk_delays) if djk_delays else float('inf'),
        success_rate=1.0 - failures / n_flows,
    )


def main():
    print("=" * 60)
    print("QUICK TEST: GNN + Orbital PE Size Generalization")
    print("=" * 60)
    print(f"Device: {DEVICE}")

    rng = np.random.default_rng(42)
    torch.manual_seed(42)

    # --- Training data ---
    print("\n[1] Generating training data (multi-scale)...")
    t0 = time.time()
    all_train = []
    for cfg_name in TRAIN_CONFIGS:
        cfg = CONFIGS[cfg_name]
        walker = WalkerDelta(cfg['P'], cfg['S'], cfg['F'], cfg['alt'], cfg['inc'])
        data = generate_routing_dataset(walker, N_TRAIN_SNAPSHOTS, rng)
        print(f"  {cfg_name} ({walker.N} nodes): {len(data)} samples "
              f"from {N_TRAIN_SNAPSHOTS} snapshots")
        all_train.extend(data)
    print(f"  Total: {len(all_train)} samples ({time.time()-t0:.1f}s)")

    # --- Test data ---
    print("\n[2] Generating test data...")
    test_data = {}
    eval_configs = ['train_66', 'train_100', 'train_200', TARGET_CONFIG]
    for cfg_name in eval_configs:
        cfg = CONFIGS[cfg_name]
        walker = WalkerDelta(cfg['P'], cfg['S'], cfg['F'], cfg['alt'], cfg['inc'])
        data = generate_routing_dataset(walker, N_TEST_SNAPSHOTS, rng)
        test_data[cfg_name] = data
        print(f"  {cfg_name}: {len(data)} test samples")

    # --- Train ---
    print(f"\n[3] Training (GAT x{GNN_LAYERS}, h={GNN_HIDDEN}, heads={GNN_HEADS}, PE={PE_DIM})...")
    model = RoutingGNN(node_dim=65, edge_dim=2, hidden=128,
                        n_layers=3, heads=GNN_HEADS).to(DEVICE)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"  Parameters: {n_params:,}")

    opt = torch.optim.Adam(model.parameters(), lr=LR)
    train_loader = DataLoader(all_train, batch_size=BATCH_SIZE, shuffle=True)

    t0 = time.time()
    for ep in range(1, EPOCHS + 1):
        loss, acc = train_epoch(model, train_loader, opt, DEVICE)
        if ep == 1 or ep % 10 == 0 or ep == EPOCHS:
            print(f"  Epoch {ep:3d}: loss={loss:.4f}, acc={acc:.4f}")
    print(f"  Training: {time.time()-t0:.1f}s")

    # --- Direction accuracy ---
    print(f"\n[4] Direction accuracy:")
    results = {}
    for cfg_name in eval_configs:
        loader = DataLoader(test_data[cfg_name], batch_size=BATCH_SIZE * 2)
        acc = evaluate(model, loader, DEVICE)
        results[cfg_name] = acc
        tag = "TRAIN" if cfg_name in TRAIN_CONFIGS else "TARGET"
        print(f"  {cfg_name:16s}: {acc:.4f} ({acc*100:.1f}%) [{tag}]")

    train_accs = [results[c] for c in TRAIN_CONFIGS]
    avg_train = np.mean(train_accs)
    target_acc = results[TARGET_CONFIG]
    retention = target_acc / avg_train if avg_train > 0 else 0
    print(f"\n  Avg train: {avg_train:.4f} | Target: {target_acc:.4f} | Retention: {retention:.1%}")

    # --- Path quality ---
    print(f"\n[5] Path quality:")
    for cfg_name in ['train_100', TARGET_CONFIG]:
        cfg = CONFIGS[cfg_name]
        walker = WalkerDelta(cfg['P'], cfg['S'], cfg['F'], cfg['alt'], cfg['inc'])
        t = rng.uniform(0, walker.period)
        snap = build_snapshot(walker, t)
        pq = evaluate_path_quality(model, walker, snap, n_flows=300, rng=rng)
        print(f"  {cfg_name}: stretch={pq['mean_stretch']:.3f}, "
              f"P95={pq['p95_stretch']:.3f}, success={pq['success_rate']:.1%}, "
              f"GNN={pq['mean_gnn_delay']:.1f}ms, Dijkstra={pq['mean_dijkstra_delay']:.1f}ms")

    # --- Verdict ---
    print(f"\n[6] Verdict:")
    if avg_train < 0.70:
        print(f"  FAIL: Train acc {avg_train:.1%} < 70% — cannot learn routing")
    elif retention >= 0.80:
        print(f"  PASS: Retention {retention:.1%} >= 80% — size generalization confirmed")
    elif retention >= 0.60:
        print(f"  PARTIAL: Retention {retention:.1%}")
    else:
        print(f"  FAIL: Retention {retention:.1%} < 60%")
    print("=" * 60)


if __name__ == '__main__':
    main()
