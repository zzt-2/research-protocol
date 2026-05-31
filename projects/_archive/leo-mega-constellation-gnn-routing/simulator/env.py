"""RL environment for LEO mega-constellation routing.

Uses precomputed PE via snapshot_to_pyg (same format as supervised training).
Episode = one (snapshot, destination) pair with sampled source nodes.
"""
import numpy as np
import torch

from config import CONFIGS
from constellation import WalkerDelta
from snapshot import build_snapshot, get_orbital_pe_tensors, snapshot_to_pyg
from topology import build_adjacency
from routing import dijkstra, dijkstra_all_pairs

class RoutingEnv:
    """Episode generator for PPO training."""

    def __init__(self, config_names, n_sources=30, pe_dim=16, seed=None):
        self.config_names = list(config_names)
        self.n_sources = n_sources
        self.pe_dim = pe_dim
        self.rng = np.random.default_rng(seed)

        self.walkers = {}
        self.pe_data = {}
        for name in self.config_names:
            cfg = CONFIGS[name]
            w = WalkerDelta(cfg['P'], cfg['S'], cfg['F'], cfg['alt'], cfg['inc'])
            self.walkers[name] = w
            self.pe_data[name] = get_orbital_pe_tensors(w)

    def reset(self):
        """Create a random episode. Returns dict with PyG data + eval context."""
        cfg_name = self.rng.choice(self.config_names)
        walker = self.walkers[cfg_name]
        plane_ids, sat_ids, P, S = self.pe_data[cfg_name]
        N = walker.N

        t = self.rng.uniform(0, walker.period)
        dest = int(self.rng.integers(0, N))
        snap = build_snapshot(walker, t)

        # PyG data with precomputed PE (same format as supervised)
        data = snapshot_to_pyg(snap, dest, plane_ids, sat_ids, P, S, self.pe_dim)

        # Dijkstra reference for reward computation
        adj = build_adjacency(N, snap['edge_index'], snap['edge_delay'])
        dist_mat, _ = dijkstra_all_pairs(adj, N)

        # Sample source nodes
        candidates = np.array([i for i in range(N) if i != dest])
        n_src = min(self.n_sources, len(candidates))
        sources = self.rng.choice(candidates, size=n_src, replace=False)

        neighbor_map = _build_neighbor_map(snap, walker.S, walker.P)

        return dict(
            data=data, dest=dest, sources=sources,
            dist_mat=dist_mat, neighbor_map=neighbor_map,
            N=N, cfg_name=cfg_name,
        )

    @staticmethod
    def evaluate_directions(ep, directions):
        """Evaluate per-node direction predictions. Returns (reward, info)."""
        dest = ep['dest']
        sources = ep['sources']
        dist_mat = ep['dist_mat']
        nmap = ep['neighbor_map']
        N = ep['N']

        stretches, gnn_delays, djk_delays = [], [], []
        n_success = 0
        for src in sources:
            gnn_d, ok = _trace(directions, int(src), dest, N, nmap)
            djk_d = dist_mat[src, dest]
            if ok and np.isfinite(djk_d) and djk_d > 0:
                stretches.append(gnn_d / djk_d)
                gnn_delays.append(gnn_d)
                djk_delays.append(djk_d)
                n_success += 1

        n_total = len(sources)
        success_rate = n_success / n_total if n_total else 0.0
        mean_stretch = np.mean(stretches) if stretches else float('inf')
        mean_gnn_delay = np.mean(gnn_delays) if gnn_delays else float('inf')
        mean_djk_delay = np.mean(djk_delays) if djk_delays else float('inf')

        if n_success > 0:
            reward = success_rate - 0.3 * max(mean_stretch - 1.0, 0.0)
        else:
            reward = -0.5

        info = dict(
            success_rate=success_rate,
            mean_stretch=mean_stretch,
            mean_gnn_delay=mean_gnn_delay,
            mean_djk_delay=mean_djk_delay,
            n_success=n_success,
            n_total=n_total,
            config=ep['cfg_name'],
        )
        return reward, info

    @staticmethod
    def evaluate_weighted(ep, logits_np):
        """GNN-weighted Dijkstra: softmax probs → edge weights → shortest path.

        For each node, softmax(logits) gives direction probabilities.
        weight(u,v) = delay(u,v) / (prob[u, dir_uv] + eps).
        High prob → low weight → preferred edge.

        Args:
            ep: episode dict from reset()
            logits_np: (N, 4) numpy array of direction logits
        Returns:
            (reward, info)
        """
        nmap = ep['neighbor_map']
        N = ep['N']
        dest = ep['dest']
        sources = ep['sources']
        dist_mat = ep['dist_mat']
        dir_mask = ep['data'].dir_mask.cpu().numpy()  # (N, 4) bool

        # Best logit per node (for relative penalty)
        best_logit = np.max(logits_np, axis=-1)  # (N,)

        # Build weighted adjacency: delay + alpha * relu(best - logit)
        # Preferred edge: logit=best → penalty=0 → weight=delay
        # Avoided edge: logit<<best → penalty=alpha*gap → weight=delay+penalty
        adj = [[] for _ in range(N)]
        edge_dir = {}
        for (u, d), (v, delay) in nmap.items():
            edge_dir[(u, v)] = d
            penalty = max(0.0, best_logit[u] - logits_np[u, d])
            w = delay + penalty
            adj[u].append((v, w))

        stretches, gnn_delays, djk_delays = [], [], []
        n_success = 0

        for src in sources:
            src = int(src)
            dist_w, parent = dijkstra(adj, src, N)
            if dist_w[dest] == np.inf or parent[dest] < 0:
                continue

            # Trace actual path delay
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
                stretches.append(actual_delay / djk_delay)
                gnn_delays.append(actual_delay)
                djk_delays.append(djk_delay)
                n_success += 1

        n_total = len(sources)
        success_rate = n_success / n_total if n_total else 0.0
        mean_stretch = np.mean(stretches) if stretches else float('inf')
        mean_gnn_delay = np.mean(gnn_delays) if gnn_delays else float('inf')
        mean_djk_delay = np.mean(djk_delays) if djk_delays else float('inf')

        if n_success > 0:
            reward = success_rate - 0.3 * max(mean_stretch - 1.0, 0.0)
        else:
            reward = -0.5

        info = dict(
            success_rate=success_rate,
            mean_stretch=mean_stretch,
            mean_gnn_delay=mean_gnn_delay,
            mean_djk_delay=mean_djk_delay,
            n_success=n_success,
            n_total=n_total,
            config=ep['cfg_name'],
        )
        return reward, info


OPPOSITE_DIR = {0: 1, 1: 0, 2: 3, 3: 2}


def _build_neighbor_map(snap, S, P):
    nmap = {}
    for e in range(snap['edge_index'].shape[1]):
        u, v = int(snap['edge_index'][0, e]), int(snap['edge_index'][1, e])
        sp, sk = divmod(u, S)
        dp, dk = divmod(v, S)
        if sp == dp:
            d = 0 if dk == (sk + 1) % S else 1
        else:
            d = 2 if dp == (sp + 1) % P else 3
        nmap[(u, d)] = (v, snap['edge_delay'][e])
        nmap[(v, OPPOSITE_DIR[d])] = (u, snap['edge_delay'][e])
    return nmap


def _trace(directions, src, dest, N, nmap):
    cur, delay, visited = src, 0.0, {src}
    for _ in range(N * 2):
        if cur == dest:
            return delay, True
        d = int(directions[cur])
        if (cur, d) not in nmap:
            return float('inf'), False
        nxt, hop_delay = nmap[(cur, d)]
        delay += hop_delay
        if nxt in visited:
            return float('inf'), False
        visited.add(nxt)
        cur = nxt
    return float('inf'), False
