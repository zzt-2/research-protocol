#!/usr/bin/env python3
"""
MVE: GNN vs MLP for Fault-Aware Load-Balanced Routing in LEO Constellation

Hypothesis: GNN message passing captures fault impact patterns on topology,
enabling better load-balanced routing under high fault rates.

Pass: GNN MLU <= MLP MLU * 0.95 at fault rate >= 10%
"""

import numpy as np
import heapq
import random
from collections import defaultdict

import torch
import torch.nn as nn
import torch.optim as optim

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

# ====== 1. Walker Constellation ======

class WalkerGraph:
    def __init__(self, n_planes=3, spp=6, phasing=1):
        self.n_planes = n_planes
        self.spp = spp
        self.N = n_planes * spp
        self.phasing = phasing
        self.adj = self._build_adj()
        self.edge_list = self._edge_list()

    def _nid(self, p, s):
        return p * self.spp + s

    def _build_adj(self):
        adj = defaultdict(set)
        for p in range(self.n_planes):
            for s in range(self.spp):
                n = self._nid(p, s)
                # Intra-plane ring
                adj[n].add(self._nid(p, (s + 1) % self.spp))
                adj[n].add(self._nid(p, (s - 1) % self.spp))
                # Inter-plane (+ phasing)
                pn = (p + 1) % self.n_planes
                sn = (s - self.phasing) % self.spp
                adj[n].add(self._nid(pn, sn))
                pp = (p - 1) % self.n_planes
                sp = (s + self.phasing) % self.spp
                adj[n].add(self._nid(pp, sp))
        return dict(adj)

    def _edge_list(self):
        edges = set()
        for u, nbrs in self.adj.items():
            for v in nbrs:
                if u < v:
                    edges.add((u, v))
        return sorted(edges)

    def adj_matrix(self, faults=frozenset()):
        A = np.zeros((self.N, self.N), dtype=np.float32)
        for u in range(self.N):
            if u in faults:
                continue
            for v in self.adj.get(u, []):
                if v not in faults:
                    A[u, v] = 1.0
        D = A.sum(1)
        D[D == 0] = 1.0
        Di = 1.0 / np.sqrt(D)
        return Di[:, None] * A * Di[None, :]


# ====== 2. Routing Utilities ======

def dijkstra(adj, src, dst, faults=frozenset(), weights=None):
    if src in faults or dst in faults:
        return None
    if src == dst:
        return [src]
    dist = {src: 0.0}
    prev = {}
    heap = [(0.0, src)]
    visited = set()
    while heap:
        d, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        if u == dst:
            path = []
            while u in prev:
                path.append(u)
                u = prev[u]
            path.append(src)
            return path[::-1]
        for v in adj.get(u, []):
            if v in faults or v in visited:
                continue
            w = (weights.get((u, v), 1.0) if weights else 1.0)
            nd = d + w
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
    return None


def k_shortest_paths(adj, src, dst, k=3, faults=frozenset()):
    paths = []
    banned = set()
    for _ in range(k):
        p = dijkstra_banned(adj, src, dst, faults, banned)
        if p is None:
            break
        paths.append(p)
        for i in range(len(p) - 1):
            banned.add((p[i], p[i + 1]))
            banned.add((p[i + 1], p[i]))
    return paths if paths else []


def dijkstra_banned(adj, src, dst, faults, banned):
    if src in faults or dst in faults:
        return None
    if src == dst:
        return [src]
    dist = {src: 0.0}
    prev = {}
    heap = [(0.0, src)]
    visited = set()
    while heap:
        d, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        if u == dst:
            path = []
            while u in prev:
                path.append(u)
                u = prev[u]
            path.append(src)
            return path[::-1]
        for v in adj.get(u, []):
            if v in faults or v in visited or (u, v) in banned:
                continue
            nd = d + 1.0
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
    return None


def oracle_routing(g, faults, flows, k=3):
    """Greedy load-balanced routing: assign paths minimizing max link util."""
    link_load = defaultdict(float)
    assignments = [None] * len(flows)

    all_paths = []
    for src, dst, _ in flows:
        ps = k_shortest_paths(g.adj, src, dst, k=k, faults=faults)
        all_paths.append(ps if ps else [None])

    order = sorted(range(len(flows)), key=lambda i: flows[i][2], reverse=True)
    for idx in order:
        best_p, best_ml = None, float('inf')
        for p in all_paths[idx]:
            if p is None:
                continue
            tmp = dict(link_load)
            for i in range(len(p) - 1):
                e = (min(p[i], p[i + 1]), max(p[i], p[i + 1]))
                tmp[e] = tmp.get(e, 0.0) + flows[idx][2]
            ml = max(tmp.values()) if tmp else 0.0
            if ml < best_ml:
                best_ml, best_p = ml, p
        assignments[idx] = best_p
        if best_p:
            for i in range(len(best_p) - 1):
                e = (min(best_p[i], best_p[i + 1]), max(best_p[i], best_p[i + 1]))
                link_load[e] += flows[idx][2]

    return assignments


def eval_routing(g, faults, flows, assignments):
    link_load = defaultdict(float)
    delivered = 0
    for (src, dst, demand), p in zip(flows, assignments):
        if p is not None:
            delivered += 1
            for i in range(len(p) - 1):
                e = (min(p[i], p[i + 1]), max(p[i], p[i + 1]))
                link_load[e] += demand
    loads = list(link_load.values())
    if not loads:
        return float('inf'), float('inf'), 0.0
    mlu = max(loads)
    mean_l = np.mean(loads)
    imbalance = mlu / max(mean_l, 1e-9)
    conn = delivered / len(flows)
    return mlu, imbalance, conn


# ====== 3. Features ======

def node_features(g, faults, mode='mlp'):
    N = g.N
    gamma = 0.5  # FCRMJ decay
    is_f = np.array([1.0 if i in faults else 0.0 for i in range(N)], dtype=np.float32)
    fd = np.zeros(N, dtype=np.float32)
    for f in faults:
        fd[f] = 1.0
        for nb in g.adj.get(f, []):
            fd[nb] = max(fd[nb], gamma)
    active = set(range(N)) - faults
    deg = np.zeros(N, dtype=np.float32)
    for u in active:
        deg[u] = sum(1 for v in g.adj.get(u, []) if v in active)
    plane = np.arange(N, dtype=np.float32) // g.spp / g.n_planes
    idx = np.arange(N, dtype=np.float32) % g.spp / g.spp
    if mode == 'mlp':
        return np.stack([is_f, deg, fd, plane, idx], axis=1)
    else:
        return np.stack([is_f, plane, idx], axis=1)


def fcrmj_weights(g, faults, gamma=0.5):
    """FCRMJ-style edge weights: penalize edges near fault nodes."""
    fd = defaultdict(float)
    for f in faults:
        fd[f] = 1.0
        for nb in g.adj.get(f, []):
            fd[nb] = max(fd[nb], gamma)
    ws = {}
    active = set(range(g.N)) - faults
    for u, v in g.edge_list:
        if u in active and v in active:
            w = 1.0 + fd[u] + fd[v]
            ws[(u, v)] = w
            ws[(v, u)] = w
    return ws


# ====== 4. Models ======

class GCNEncoder(nn.Module):
    def __init__(self, dim_in, dim_h=32):
        super().__init__()
        self.w1 = nn.Linear(dim_in, dim_h)
        self.w2 = nn.Linear(dim_h, dim_h)
        self.out = nn.Linear(dim_h, 1)

    def forward(self, x, adj):
        h = torch.relu(self.w1(adj @ x))
        h = torch.relu(self.w2(adj @ h))
        return self.out(h).squeeze(-1)


class MLPEncoder(nn.Module):
    def __init__(self, dim_in, dim_h=32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(dim_in, dim_h), nn.ReLU(),
            nn.Linear(dim_h, dim_h), nn.ReLU(),
            nn.Linear(dim_h, 1),
        )

    def forward(self, x, adj=None):
        return self.net(x).squeeze(-1)


def scores_to_weights(scores, g, faults):
    ws = {}
    active = set(range(g.N)) - faults
    s = scores.detach().numpy()
    for u, v in g.edge_list:
        if u in active and v in active:
            w = 1.0 + abs(s[u]) + abs(s[v])
            ws[(u, v)] = w
            ws[(v, u)] = w
    return ws


# ====== 5. Oracle targets ======

def oracle_targets(g, faults, flows):
    """Node usage count from oracle routing → target for supervised training."""
    assignments = oracle_routing(g, faults, flows)
    usage = np.zeros(g.N, dtype=np.float32)
    for p in assignments:
        if p:
            for n in p:
                usage[n] += 1
    # Mask fault nodes
    for f in faults:
        usage[f] = 0.0
    mx = usage.max()
    if mx > 0:
        usage /= mx
    return usage


# ====== 6. Main Experiment ======

def main():
    g = WalkerGraph(n_planes=6, spp=10, phasing=2)
    print(f"Graph: {g.N} nodes, {len(g.edge_list)} undirected edges")

    # Fixed traffic demands
    flows = []
    for _ in range(40):
        src, dst = random.sample(range(g.N), 2)
        demand = random.uniform(0.5, 2.0)
        flows.append((src, dst, demand))
    print(f"Flows: {len(flows)}")

    # Training: 0-3 faults (0-5% of 60)
    train_scenarios = []
    for _ in range(120):
        nf = random.choice([0, 1, 2, 3])
        faults = frozenset(random.sample(range(g.N), nf)) if nf else frozenset()
        train_scenarios.append(faults)

    # Test: 6-12 random (10-20%) + correlated (same orbit)
    test_random = []
    for _ in range(50):
        nf = random.choice([6, 8, 10, 12])
        test_random.append(frozenset(random.sample(range(g.N), nf)))

    test_correlated = []
    for _ in range(25):
        n_planes_fault = random.randint(1, 3)
        planes = random.sample(range(6), n_planes_fault)
        faults = set()
        for p in planes:
            n_sats = random.randint(2, 5)
            sats = random.sample(range(10), min(n_sats, 10))
            faults.update(p * 10 + s for s in sats)
        test_correlated.append(frozenset(faults))

    test_scenarios = test_random + test_correlated
    print(f"Train: {len(train_scenarios)}, Test: {len(test_scenarios)} (50 rand + 25 corr)")

    # Compute oracle targets for training
    print("\nComputing oracle targets...")
    train_data = []
    for faults in train_scenarios:
        feats_mlp = node_features(g, faults, 'mlp')
        feats_gnn = node_features(g, faults, 'gnn')
        adj_m = g.adj_matrix(faults)
        tgt = oracle_targets(g, faults, flows)
        train_data.append((feats_mlp, feats_gnn, adj_m, tgt, faults))

    # Train both models
    dim_mlp = train_data[0][0].shape[1]
    dim_gnn = train_data[0][1].shape[1]

    mlp = MLPEncoder(dim_mlp, dim_h=64)
    gnn = GCNEncoder(dim_gnn, dim_h=64)
    loss_fn = nn.MSELoss()

    N_EPOCHS = 300

    print("\nTraining MLP...")
    opt_mlp = optim.Adam(mlp.parameters(), lr=0.005)
    for epoch in range(N_EPOCHS):
        loss_sum = 0
        for feats, _, _, tgt, _ in train_data:
            x = torch.FloatTensor(feats)
            y = torch.FloatTensor(tgt)
            pred = mlp(x)
            loss = loss_fn(pred, y)
            opt_mlp.zero_grad()
            loss.backward()
            opt_mlp.step()
            loss_sum += loss.item()
        if (epoch + 1) % 75 == 0:
            print(f"  Epoch {epoch+1}: loss={loss_sum/len(train_data):.4f}")

    print("Training GNN...")
    opt_gnn = optim.Adam(gnn.parameters(), lr=0.005)
    for epoch in range(N_EPOCHS):
        loss_sum = 0
        for _, feats, adj_m, tgt, _ in train_data:
            x = torch.FloatTensor(feats)
            a = torch.FloatTensor(adj_m)
            y = torch.FloatTensor(tgt)
            pred = gnn(x, a)
            loss = loss_fn(pred, y)
            opt_gnn.zero_grad()
            loss.backward()
            opt_gnn.step()
            loss_sum += loss.item()
        if (epoch + 1) % 75 == 0:
            print(f"  Epoch {epoch+1}: loss={loss_sum/len(train_data):.4f}")

    # ====== Evaluate ======
    def evaluate_method(name, route_fn):
        results = {'mlu': [], 'imb': [], 'conn': []}
        for faults in test_scenarios:
            assignments = route_fn(g, faults, flows)
            mlu, imb, conn = eval_routing(g, faults, flows, assignments)
            results['mlu'].append(mlu)
            results['imb'].append(imb)
            results['conn'].append(conn)
        return {k: np.mean(v) for k, v in results.items()}

    # Method 1: Dijkstra (baseline)
    def route_dijkstra(g, faults, flows):
        return [dijkstra(g.adj, s, d, faults) for s, d, _ in flows]

    # Method 2: FCRMJ-style (hand-crafted fault domain weights)
    def route_fcrmj(g, faults, flows):
        ws = fcrmj_weights(g, faults)
        return [dijkstra(g.adj, s, d, faults, ws) for s, d, _ in flows]

    # Method 3: MLP-weighted Dijkstra
    def route_mlp(g, faults, flows):
        feats = node_features(g, faults, 'mlp')
        with torch.no_grad():
            scores = mlp(torch.FloatTensor(feats))
        ws = scores_to_weights(scores, g, faults)
        return [dijkstra(g.adj, s, d, faults, ws) for s, d, _ in flows]

    # Method 4: GNN-weighted Dijkstra
    def route_gnn(g, faults, flows):
        feats = node_features(g, faults, 'gnn')
        adj_m = g.adj_matrix(faults)
        with torch.no_grad():
            scores = gnn(torch.FloatTensor(feats), torch.FloatTensor(adj_m))
        ws = scores_to_weights(scores, g, faults)
        return [dijkstra(g.adj, s, d, faults, ws) for s, d, _ in flows]

    print("\n" + "=" * 60)
    print("RESULTS (averaged over all test scenarios)")
    print("=" * 60)

    methods = {
        'Dijkstra': route_dijkstra,
        'FCRMJ-style': route_fcrmj,
        'MLP': route_mlp,
        'GNN': route_gnn,
    }

    all_res = {}
    for name, fn in methods.items():
        res = evaluate_method(name, fn)
        all_res[name] = res
        print(f"{name:15s}  MLU={res['mlu']:.3f}  Imbalance={res['imb']:.3f}  Connectivity={res['conn']:.3f}")

    # ====== Breakdown by fault severity ======
    print("\n" + "=" * 60)
    print("BREAKDOWN BY FAULT RATE")
    print("=" * 60)

    for label, subset in [("Random 6-12 faults", test_random), ("Correlated (same orbit)", test_correlated)]:
        print(f"\n--- {label} ({len(subset)} scenarios) ---")
        for name, fn in methods.items():
            res = {'mlu': [], 'imb': [], 'conn': []}
            for faults in subset:
                assignments = fn(g, faults, flows)
                mlu, imb, conn = eval_routing(g, faults, flows, assignments)
                res['mlu'].append(mlu)
                res['imb'].append(imb)
                res['conn'].append(conn)
            m = {k: np.mean(v) for k, v in res.items()}
            print(f"  {name:15s}  MLU={m['mlu']:.3f}  Imbalance={m['imb']:.3f}  Connectivity={m['conn']:.3f}")

    # ====== Per-fault-count breakdown ======
    print("\n" + "=" * 60)
    print("PER FAULT COUNT")
    print("=" * 60)

    by_count = defaultdict(list)
    for s in test_scenarios:
        by_count[len(s)].append(s)

    for nf in sorted(by_count):
        subset = by_count[nf]
        fault_rate = nf / g.N * 100
        print(f"\n--- {nf} faults ({fault_rate:.1f}% fault rate, {len(subset)} scenarios) ---")
        for name, fn in methods.items():
            res = {'mlu': [], 'imb': [], 'conn': []}
            for faults in subset:
                assignments = fn(g, faults, flows)
                mlu, imb, conn = eval_routing(g, faults, flows, assignments)
                res['mlu'].append(mlu)
                res['imb'].append(imb)
                res['conn'].append(conn)
            m = {k: np.mean(v) for k, v in res.items()}
            print(f"  {name:15s}  MLU={m['mlu']:.3f}  Imbalance={m['imb']:.3f}  Connectivity={m['conn']:.3f}")

    # ====== Verdict ======
    print("\n" + "=" * 60)
    print("MVE VERDICT")
    print("=" * 60)

    # Aggregate high fault rate scenarios (>= 10%)
    high_fault = [s for s in test_scenarios if len(s) >= 6]  # 6/60 = 10%
    if high_fault:
        mlp_mlu, gnn_mlu = [], []
        for faults in high_fault:
            for name, fn, lst in [('MLP', route_mlp, mlp_mlu), ('GNN', route_gnn, gnn_mlu)]:
                assignments = fn(g, faults, flows)
                mlu, _, _ = eval_routing(g, faults, flows, assignments)
                lst.append(mlu)

        mlp_avg = np.mean(mlp_mlu)
        gnn_avg = np.mean(gnn_mlu)
        improvement = (mlp_avg - gnn_avg) / mlp_avg * 100 if mlp_avg > 0 else 0

        print(f"High fault rate scenarios (>= 11.1%):")
        print(f"  MLP avg MLU: {mlp_avg:.3f}")
        print(f"  GNN avg MLU: {gnn_avg:.3f}")
        print(f"  GNN improvement: {improvement:.1f}%")

        if gnn_avg <= mlp_avg * 0.95:
            print("  PASS: GNN >= 5% better than MLP at high fault rates")
        elif gnn_avg < mlp_avg:
            print(f"  PARTIAL: GNN better but only {improvement:.1f}% (< 5% threshold)")
        else:
            print("  FAIL: GNN not better than MLP")


if __name__ == '__main__':
    main()
