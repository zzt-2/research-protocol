#!/usr/bin/env python3
"""
MVE: GNN Size Generalization for Walker-Delta Routing

Hypothesis: A GNN trained on small Walker-Delta constellation can zero-shot
generalize to larger constellations for weighted shortest-path routing.

Setup:
  Small  (train): 8x12 = 96 nodes
  Medium (test):  16x24 = 384 nodes (4x)
  Large  (test):  32x48 = 1536 nodes (16x)

Task: Predict weighted-shortest-path next-hop direction (4-class)
  - Each node has 4 neighbors (toroidal grid): +row, -row, +col, -col
  - Random edge weights per sample, uniform [0.5, 2.0]
  - Dijkstra provides ground truth

Features per node (dim=10):
  [r_norm, c_norm, dest_r_norm, dest_c_norm, is_source, is_dest,
   w_+row, w_-row, w_+col, w_-col]

Model: 3-layer GAT, 64 hidden, 4 heads

Pass criteria:
  - Same-scale accuracy >= 80% (model learns the task)
  - Cross-scale retention >= 70% (4x) and >= 60% (16x)

Verdict:
  PASS   — both criteria met, generalization confirmed
  PARTIAL — retention 50-70%, needs techniques
  FAIL   — retention < 50% or same-scale < 80%
"""

import time, random, heapq
import numpy as np
import torch
import torch.nn.functional as F
from torch_geometric.nn import GATConv
from torch_geometric.data import Data
from torch_geometric.loader import DataLoader

# ===================== Config =====================
SEED = 42
SCALES = {'small': (8, 12), 'medium': (16, 24), 'large': (32, 48)}
N_TRAIN, N_TEST = 3000, 500
EPOCHS = 50
HIDDEN = 64
LAYERS = 3
HEADS = 4
LR = 1e-3
W_LO, W_HI = 0.5, 2.0
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# ===================== Graph =====================
# 4 directions: +row(south), -row(north), +col(east), -col(west)
DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def make_grid(nR, nC):
    """Toroidal grid edge_index. Each node has degree 4."""
    E = []
    for i in range(nR):
        for j in range(nC):
            u = i * nC + j
            for dr, dc in DIRS:
                v = ((i + dr) % nR) * nC + (j + dc) % nC
                E.append([u, v])
    return torch.tensor(E, dtype=torch.long).t().contiguous()


# ===================== Dijkstra =====================

def dijkstra(dest, nR, nC, W):
    """Weighted Dijkstra from dest -> next_hop direction per node."""
    N = nR * nC
    dist = [1e18] * N
    dist[dest] = 0.0
    parent = [-1] * N
    pq = [(0.0, dest)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        r, c = divmod(u, nC)
        for dr, dc in DIRS:
            v = ((r + dr) % nR) * nC + (c + dc) % nC
            nd = d + W[u][v]
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(pq, (nd, v))

    nh = [-1] * N
    for u in range(N):
        if parent[u] < 0:
            continue
        r, c = divmod(u, nC)
        for di, (dr, dc) in enumerate(DIRS):
            if ((r + dr) % nR) * nC + (c + dc) % nC == parent[u]:
                nh[u] = di
                break
    return dist, nh


# ===================== Sample =====================

def make_sample(nR, nC, ei):
    """Generate one (source, dest, random weights) sample."""
    N = nR * nC
    # Random edge weights
    W = [[0.0] * N for _ in range(N)]
    for k in range(ei.size(1)):
        u, v = ei[0, k].item(), ei[1, k].item()
        W[u][v] = random.uniform(W_LO, W_HI)
    # Random src/dst
    src, dst = random.sample(range(N), 2)
    dist_list, nh = dijkstra(dst, nR, nC, W)
    # Features: [r/Nr, c/Nc, dr/Nr, dc/Nc, is_src, is_dst, w0, w1, w2, w3]
    dst_r, dst_c = divmod(dst, nC)
    x = torch.zeros(N, 10)
    y = torch.full((N,), -1, dtype=torch.long)
    for u in range(N):
        r, c = divmod(u, nC)
        x[u, 0] = r / nR
        x[u, 1] = c / nC
        x[u, 2] = dst_r / nR
        x[u, 3] = dst_c / nC
        x[u, 4] = float(u == src)
        x[u, 5] = float(u == dst)
        for di, (dr, dc) in enumerate(DIRS):
            nb = ((r + dr) % nR) * nC + (c + dc) % nC
            x[u, 6 + di] = W[u][nb] / W_HI
        if nh[u] >= 0:
            y[u] = nh[u]
    return Data(x=x, edge_index=ei, y=y)


# ===================== Dataset =====================

def gen_dataset(nR, nC, n_samples):
    ei = make_grid(nR, nC)
    return [make_sample(nR, nC, ei) for _ in range(n_samples)]


# ===================== Model =====================

class RoutingGNN(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = GATConv(10, HIDDEN // HEADS, heads=HEADS)
        self.convs = torch.nn.ModuleList([
            GATConv(HIDDEN, HIDDEN // HEADS, heads=HEADS)
            for _ in range(LAYERS - 1)
        ])
        self.head = torch.nn.Linear(HIDDEN, 4)

    def forward(self, data):
        x = self.conv1(data.x, data.edge_index).relu()
        for conv in self.convs:
            x = conv(x, data.edge_index).relu()
        return self.head(x)


# ===================== Train / Eval =====================

def train_epoch(model, loader, opt):
    model.train()
    tot = cor = 0
    for d in loader:
        d = d.to(DEVICE)
        opt.zero_grad()
        out = model(d)
        mask = d.y >= 0
        loss = F.cross_entropy(out[mask], d.y[mask])
        loss.backward()
        opt.step()
        tot += mask.sum().item()
        cor += (out[mask].argmax(-1) == d.y[mask]).sum().item()
    return cor / max(tot, 1)


@torch.no_grad()
def accuracy(model, loader):
    model.eval()
    tot = cor = 0
    for d in loader:
        d = d.to(DEVICE)
        out = model(d)
        mask = d.y >= 0
        tot += mask.sum().item()
        cor += (out[mask].argmax(-1) == d.y[mask]).sum().item()
    return cor / max(tot, 1)


# ===================== Path Tracing =====================

@torch.no_grad()
def path_stretch(model, nR, nC, ei, n_samples=200):
    """Trace predicted paths, compute stretch = predicted_cost / dijkstra_cost."""
    model.eval()
    N = nR * nC
    stretches = []
    failures = 0

    for _ in range(n_samples):
        W = [[0.0] * N for _ in range(N)]
        for k in range(ei.size(1)):
            u, v = ei[0, k].item(), ei[1, k].item()
            W[u][v] = random.uniform(W_LO, W_HI)
        src, dst = random.sample(range(N), 2)
        dist_list, _ = dijkstra(dst, nR, nC, W)
        opt_cost = dist_list[src]

        # Build features for model
        dst_r, dst_c = divmod(dst, nC)
        x = torch.zeros(1, N, 10)
        for u in range(N):
            r, c = divmod(u, nC)
            x[0, u] = torch.tensor([
                r / nR, c / nC, dst_r / nR, dst_c / nC,
                float(u == src), float(u == dst),
                W[u][((r + 1) % nR) * nC + c] / W_HI,
                W[u][((r - 1) % nR) * nC + c] / W_HI,
                W[u][r * nC + (c + 1) % nC] / W_HI,
                W[u][r * nC + (c - 1) % nC] / W_HI,
            ])

        data = Data(x=x.squeeze(0), edge_index=ei, y=torch.zeros(N, dtype=torch.long))
        data = data.to(DEVICE)
        dirs = model(data).argmax(-1).cpu().numpy()

        # Trace path
        cur = src
        cost = 0.0
        visited = {cur}
        reached = False
        for _ in range(N * 2):
            if cur == dst:
                reached = True
                break
            d = dirs[cur]
            r, c = divmod(cur, nC)
            dr, dc = DIRS[d]
            nxt = ((r + dr) % nR) * nC + (c + dc) % nC
            cost += W[cur][nxt]
            if nxt in visited:
                break
            visited.add(nxt)
            cur = nxt

        if reached and opt_cost > 0:
            stretches.append(cost / opt_cost)
        else:
            failures += 1

    avg_stretch = np.mean(stretches) if stretches else float('inf')
    success_rate = 1 - failures / n_samples
    return avg_stretch, success_rate


# ===================== Main =====================

def main():
    random.seed(SEED)
    torch.manual_seed(SEED)
    np.random.seed(SEED)

    print("=" * 60)
    print("MVE: GNN Size Generalization for Walker-Delta Routing")
    print("=" * 60)

    sr, sc = SCALES['small']
    mr, mc = SCALES['medium']
    lr, lc = SCALES['large']
    print(f"  Small (train): {sr}x{sc} = {sr * sc} nodes")
    print(f"  Medium (test): {mr}x{mc} = {mr * mc} nodes (4x)")
    print(f"  Large  (test): {lr}x{lc} = {lr * lc} nodes (16x)")
    print(f"  Device: {DEVICE}")

    # ---- Data ----
    print("\n[1] Generating data...")
    t0 = time.time()
    train_data = gen_dataset(sr, sc, N_TRAIN)
    print(f"  Train {N_TRAIN} samples: {time.time() - t0:.1f}s")

    t0 = time.time()
    test_s = gen_dataset(sr, sc, N_TEST)
    test_m = gen_dataset(mr, mc, N_TEST)
    test_l = gen_dataset(lr, lc, N_TEST)
    print(f"  Test {N_TEST * 3} samples: {time.time() - t0:.1f}s")

    bs = 32
    train_loader = DataLoader(train_data, batch_size=bs, shuffle=True)
    ts_loader = DataLoader(test_s, batch_size=bs * 2)
    tm_loader = DataLoader(test_m, batch_size=bs)
    tl_loader = DataLoader(test_l, batch_size=bs // 2)

    # ---- Train ----
    print(f"\n[2] Training (GAT x{LAYERS}, h={HIDDEN}, heads={HEADS})...")
    model = RoutingGNN().to(DEVICE)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"  Parameters: {n_params:,}")
    opt = torch.optim.Adam(model.parameters(), lr=LR)

    t0 = time.time()
    for ep in range(1, EPOCHS + 1):
        acc = train_epoch(model, train_loader, opt)
        if ep == 1 or ep % 10 == 0 or ep == EPOCHS:
            print(f"  Epoch {ep:3d}: train_acc = {acc:.4f}")
    print(f"  Training time: {time.time() - t0:.1f}s")

    # ---- Evaluate accuracy ----
    print(f"\n[3] Direction accuracy:")
    a_s = accuracy(model, ts_loader)
    a_m = accuracy(model, tm_loader)
    a_l = accuracy(model, tl_loader)
    r_m = a_m / max(a_s, 1e-6)
    r_l = a_l / max(a_s, 1e-6)

    print(f"  Same-scale ({sr * sc:4d}): {a_s:.4f} ({a_s * 100:.1f}%)")
    print(f"  Cross-4x   ({mr * mc:4d}): {a_m:.4f} ({a_m * 100:.1f}%)  retention = {r_m:.1%}")
    print(f"  Cross-16x  ({lr * lc:4d}): {a_l:.4f} ({a_l * 100:.1f}%)  retention = {r_l:.1%}")
    print(f"  Random baseline: 25.0%")

    # ---- Evaluate path stretch ----
    print(f"\n[4] Path quality (stretch = predicted_cost / dijkstra_cost):")
    ei_s = make_grid(sr, sc)
    ei_m = make_grid(mr, mc)
    ei_l = make_grid(lr, lc)

    for name, ei_tmp, nR, nC in [("Same-scale", ei_s, sr, sc),
                                   ("Cross-4x", ei_m, mr, mc),
                                   ("Cross-16x", ei_l, lr, lc)]:
        avg_stretch, success = path_stretch(model, nR, nC, ei_tmp, n_samples=200)
        print(f"  {name:12s}: stretch = {avg_stretch:.3f}, success = {success:.1%}")

    # ---- Verdict ----
    print(f"\n[5] Verdict:")
    if a_s < 0.80:
        print("  FAIL: Same-scale accuracy < 80% - model cannot learn the task")
        result = "FAIL_LEARN"
    elif r_m >= 0.70 and r_l >= 0.60:
        print("  PASS: Cross-scale generalization confirmed")
        print("  -> GNN routing model transfers across Walker-Delta scales")
        result = "PASS"
    elif r_m >= 0.50:
        print("  PARTIAL: Generalization exists but significant degradation")
        print("  -> Needs techniques: deeper GNN, position encoding, etc.")
        result = "PARTIAL"
    else:
        print("  FAIL: GNN cannot generalize across scales")
        print("  -> Fundamental barrier - reconsider direction")
        result = "FAIL"

    print("=" * 60)
    return result


if __name__ == '__main__':
    main()
