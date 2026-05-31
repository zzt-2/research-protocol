"""Supervised pretraining for RoutingActorCritic using Dijkstra labels.

Generates (snapshot, destination) pairs with ground-truth direction labels,
trains the actor head + GAT backbone, saves weights for PPO fine-tuning.
"""
import sys
import os
import time
import numpy as np
import torch
import torch.nn.functional as F
from torch_geometric.loader import DataLoader

sys.path.insert(0, os.path.dirname(__file__))

from config import (
    CONFIGS, TRAIN_CONFIGS, TARGET_CONFIG,
    GNN_HEADS, PE_DIM,
)
from constellation import WalkerDelta
from snapshot import build_snapshot, get_orbital_pe_tensors, snapshot_to_pyg
from topology import build_adjacency
from routing import dijkstra_all_pairs
from models import RoutingActorCritic
from env import RoutingEnv

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

PRETRAIN_LAYERS = 3
PRETRAIN_HIDDEN = 128
EPOCHS = 150
LR = 1e-3
BATCH_SIZE = 64
N_SNAPSHOTS = 20
N_EVAL_SNAPSHOTS = 3


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


def generate_dataset(walker, n_snapshots, rng):
    dataset = []
    plane_ids, sat_ids, P, S = get_orbital_pe_tensors(walker)

    for _ in range(n_snapshots):
        t = rng.uniform(0, walker.period)
        snap = build_snapshot(walker, t)

        adj = build_adjacency(walker.N, snap['edge_index'], snap['edge_delay'])
        _, next_hop = dijkstra_all_pairs(adj, walker.N)
        dir_labels = dijkstra_to_direction_labels(walker, next_hop)

        for d in range(walker.N):
            data = snapshot_to_pyg(snap, d, plane_ids, sat_ids, P, S, PE_DIM)
            data.y = torch.tensor(dir_labels[:, d], dtype=torch.long)
            dataset.append(data)

    return dataset


def train_epoch(model, loader, opt, device):
    model.train()
    total_loss, correct, total = 0, 0, 0

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


@torch.no_grad()
def eval_accuracy(model, loader, device):
    model.eval()
    correct, total = 0, 0
    for batch in loader:
        batch = batch.to(device)
        logits, _ = model(batch)
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


@torch.no_grad()
def eval_path_quality(model, config_name, n_flows=300, seed=123):
    env = RoutingEnv([config_name], n_sources=n_flows, pe_dim=PE_DIM, seed=seed)
    model.eval()
    all_sr, all_st = [], []

    for _ in range(5):
        ep = env.reset()
        data = ep['data'].to(DEVICE)
        logits, _ = model(data)
        masked = logits.clone()
        masked[~data.dir_mask] = float('-inf')
        dirs = masked.argmax(dim=-1).cpu().numpy()
        _, info = RoutingEnv.evaluate_directions(ep, dirs)
        all_sr.append(info['success_rate'])
        if info['mean_stretch'] < float('inf'):
            all_st.append(info['mean_stretch'])

    return dict(
        success_rate=np.mean(all_sr),
        mean_stretch=np.mean(all_st) if all_st else float('inf'),
    )


def main():
    print("=" * 60)
    print("SUPERVISED PRETRAINING → PPO READY")
    print("=" * 60)
    print(f"Device: {DEVICE}")

    rng = np.random.default_rng(42)
    torch.manual_seed(42)

    # --- Generate data ---
    print("\n[1] Generating training data...")
    t0 = time.time()
    all_train = []
    for cfg_name in TRAIN_CONFIGS:
        cfg = CONFIGS[cfg_name]
        walker = WalkerDelta(cfg['P'], cfg['S'], cfg['F'], cfg['alt'], cfg['inc'])
        data = generate_dataset(walker, N_SNAPSHOTS, rng)
        print(f"  {cfg_name} ({walker.N} nodes): {len(data)} samples")
        all_train.extend(data)
    print(f"  Total: {len(all_train)} samples ({time.time()-t0:.1f}s)")

    # --- Test data ---
    print("\n[2] Generating test data...")
    test_data = {}
    eval_configs = TRAIN_CONFIGS + [TARGET_CONFIG]
    for cfg_name in eval_configs:
        cfg = CONFIGS[cfg_name]
        walker = WalkerDelta(cfg['P'], cfg['S'], cfg['F'], cfg['alt'], cfg['inc'])
        data = generate_dataset(walker, N_EVAL_SNAPSHOTS, rng)
        test_data[cfg_name] = data

    # --- Model ---
    node_dim = 1 + PE_DIM * 2  # is_dest + own_PE + dest_PE
    model = RoutingActorCritic(
        node_dim=node_dim, edge_dim=2, hidden=PRETRAIN_HIDDEN,
        n_layers=PRETRAIN_LAYERS, heads=GNN_HEADS,
    ).to(DEVICE)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"\n[3] Model: {PRETRAIN_LAYERS} GAT layers, h={PRETRAIN_HIDDEN}, "
          f"heads={GNN_HEADS}, params={n_params:,}")

    # --- Train ---
    opt = torch.optim.Adam(model.parameters(), lr=LR)
    train_loader = DataLoader(all_train, batch_size=BATCH_SIZE, shuffle=True)

    print(f"\n[4] Training {EPOCHS} epochs...")
    t0 = time.time()
    for ep in range(1, EPOCHS + 1):
        loss, acc = train_epoch(model, train_loader, opt, DEVICE)
        if ep == 1 or ep % 25 == 0 or ep == EPOCHS:
            print(f"  Epoch {ep:3d}: loss={loss:.4f}, acc={acc:.4f}")
    print(f"  Training: {time.time()-t0:.1f}s")

    # --- Direction accuracy ---
    print(f"\n[5] Direction accuracy:")
    results = {}
    for cfg_name in eval_configs:
        loader = DataLoader(test_data[cfg_name], batch_size=BATCH_SIZE * 2)
        acc = eval_accuracy(model, loader, DEVICE)
        results[cfg_name] = acc
        tag = "TRAIN" if cfg_name in TRAIN_CONFIGS else "TARGET"
        print(f"  {cfg_name:16s}: {acc:.4f} ({acc*100:.1f}%) [{tag}]")

    train_accs = [results[c] for c in TRAIN_CONFIGS]
    avg_train = np.mean(train_accs)
    target_acc = results[TARGET_CONFIG]
    retention = target_acc / avg_train if avg_train > 0 else 0
    print(f"\n  Avg train: {avg_train:.4f} | Target: {target_acc:.4f} | Retention: {retention:.1%}")

    # --- Path quality ---
    print(f"\n[6] Path quality:")
    for cfg_name in ['train_100', TARGET_CONFIG]:
        pq = eval_path_quality(model, cfg_name)
        print(f"  {cfg_name:16s}: success={pq['success_rate']:.1%}, "
              f"stretch={pq['mean_stretch']:.3f}")

    # --- Save ---
    save_path = os.path.join(os.path.dirname(__file__), 'pretrained.pt')
    torch.save(model.state_dict(), save_path)
    print(f"\n[7] Saved: {save_path}")

    # --- Verdict ---
    print(f"\n{'=' * 60}")
    if retention >= 0.80:
        print(f"  PASS: Retention {retention:.1%} >= 80%")
    elif retention >= 0.60:
        print(f"  PARTIAL: Retention {retention:.1%}")
    else:
        print(f"  LOW: Retention {retention:.1%}")
    print(f"  Ready for PPO fine-tuning: python train.py")
    print(f"{'=' * 60}")


if __name__ == '__main__':
    main()
