#!/usr/bin/env python3
"""MVE Environment: Walker delta LEO topology + non-uniform traffic routing."""

import numpy as np
import networkx as nx
from dataclasses import dataclass


@dataclass
class Config:
    n_planes: int = 6
    n_sats: int = 4          # per plane → 24 total
    capacity: float = 10.0   # Gbps per ISL (full duplex)
    n_flows: int = 20
    n_heavy: int = 5         # heavy hitters
    heavy_demand: tuple = (3.0, 5.0)  # Gbps
    light_demand: tuple = (0.1, 1.0)
    k_paths: int = 4         # candidate paths per flow
    n_popular: int = 3       # hotspot destinations

    @property
    def n_nodes(self):
        return self.n_planes * self.n_sats


def build_topology(cfg):
    """Walker delta constellation → networkx graph + PyG-style edge_index."""
    G = nx.Graph()
    S, P = cfg.n_sats, cfg.n_planes

    for p in range(P):
        for s in range(S):
            G.add_node(p * S + s)

    # Intra-plane ring ISLs
    for p in range(P):
        for s in range(S):
            u, v = p * S + s, p * S + (s + 1) % S
            if not G.has_edge(u, v):
                G.add_edge(u, v, etype=0)

    # Inter-plane ISLs
    for p in range(P):
        for s in range(S):
            u, v = p * S + s, ((p + 1) % P) * S + s
            if not G.has_edge(u, v):
                G.add_edge(u, v, etype=1)

    # Directed edge_index for PyG [2, 2*E]
    srcs, dsts, types = [], [], []
    for u, v, d in G.edges(data=True):
        srcs += [u, v]
        dsts += [v, u]
        types += [d['etype'], d['etype']]

    adj = {n: sorted(G.neighbors(n)) for n in G.nodes()}
    edge_index = np.array([srcs, dsts], dtype=np.int64)
    edge_types = np.array(types, dtype=np.float32)

    return G, adj, edge_index, edge_types


class RoutingEnv:
    """Sequential flow routing: route flows one-by-one, minimize MLU."""

    def __init__(self, cfg=None):
        self.cfg = cfg or Config()
        self.G, self.adj, self.edge_index, self.edge_types = build_topology(self.cfg)
        self.N = self.cfg.n_nodes
        self.K = self.cfg.k_paths
        self._path_cache = {}
        self._init_state()

    def _init_state(self):
        self.link_load = {}
        for u, v in zip(self.edge_index[0], self.edge_index[1]):
            self.link_load[(int(u), int(v))] = 0.0
        self.flows = []
        self.step_idx = 0

    def _get_paths(self, src, dst):
        key = (src, dst)
        if key not in self._path_cache:
            try:
                gen = nx.shortest_simple_paths(self.G, src, dst)
                self._path_cache[key] = [p for _, p in zip(range(self.K), gen)]
            except nx.NetworkXNoPath:
                self._path_cache[key] = []
        return self._path_cache[key]

    def _generate_flows(self, rng):
        flows = []
        N = self.N
        popular = rng.choice(N, self.cfg.n_popular, replace=False).tolist()

        # Heavy flows → popular destinations (hotspot)
        for _ in range(self.cfg.n_heavy):
            dst = int(rng.choice(popular))
            src = int(rng.integers(0, N))
            while src == dst:
                src = int(rng.integers(0, N))
            demand = float(rng.uniform(*self.cfg.heavy_demand))
            flows.append((src, dst, demand))

        # Light flows → random pairs
        pairs = [(i, j) for i in range(N) for j in range(N) if i != j]
        for _ in range(self.cfg.n_flows - self.cfg.n_heavy):
            src, dst = pairs[int(rng.integers(0, len(pairs)))]
            demand = float(rng.uniform(*self.cfg.light_demand))
            flows.append((src, dst, demand))

        rng.shuffle(flows)
        return flows

    def _node_features(self):
        """Per-node: [in_load_norm, out_load_norm, is_src, is_dst, demand_norm]"""
        feat = np.zeros((self.N, 5), dtype=np.float32)
        for i in range(self.N):
            for n in self.adj[i]:
                feat[i, 0] += self.link_load.get((n, i), 0.0)
                feat[i, 1] += self.link_load.get((i, n), 0.0)
        feat[:, :2] /= self.cfg.capacity

        if self.step_idx < len(self.flows):
            src, dst, demand = self.flows[self.step_idx]
            feat[src, 2] = 1.0
            feat[dst, 3] = 1.0
            feat[src, 4] = demand / self.cfg.capacity
            feat[dst, 4] = demand / self.cfg.capacity
        return feat

    def _edge_features(self):
        """Per-directed-edge: [utilization, edge_type]"""
        feat = np.zeros((len(self.edge_types), 2), dtype=np.float32)
        for i, (u, v) in enumerate(zip(self.edge_index[0], self.edge_index[1])):
            feat[i, 0] = self.link_load.get((int(u), int(v)), 0.0) / self.cfg.capacity
            feat[i, 1] = self.edge_types[i]
        return feat

    def _mlp_features(self):
        """Local features for MLP: src + dst + 1-hop neighbor loads + path lengths."""
        if self.step_idx >= len(self.flows):
            return np.zeros(5 + 5 + 4 + 4 + 1 + self.K, dtype=np.float32)

        src, dst, demand = self.flows[self.step_idx]
        nf = self._node_features()

        src_feat = nf[src]
        dst_feat = nf[dst]

        # 1-hop neighbor outgoing loads (padded to 4)
        src_nbr_loads = np.zeros(4, dtype=np.float32)
        for i, n in enumerate(self.adj[src][:4]):
            src_nbr_loads[i] = nf[n, 1]

        dst_nbr_loads = np.zeros(4, dtype=np.float32)
        for i, n in enumerate(self.adj[dst][:4]):
            dst_nbr_loads[i] = nf[n, 1]

        # Path lengths
        paths = self._get_paths(src, dst)
        path_lens = np.zeros(self.K, dtype=np.float32)
        for i, p in enumerate(paths):
            path_lens[i] = len(p)

        demand_norm = np.array([demand / self.cfg.capacity], dtype=np.float32)
        return np.concatenate([src_feat, dst_feat, src_nbr_loads, dst_nbr_loads,
                               demand_norm, path_lens])

    def _get_mlu(self):
        if not self.link_load:
            return 0.0
        return max(self.link_load.values()) / self.cfg.capacity

    def _get_obs(self):
        paths = []
        src, dst, demand = 0, 0, 0.0
        if self.step_idx < len(self.flows):
            src, dst, demand = self.flows[self.step_idx]
            paths = self._get_paths(src, dst)

        return {
            "node_feat": self._node_features(),
            "edge_index": self.edge_index,
            "edge_feat": self._edge_features(),
            "mlp_feat": self._mlp_features(),
            "flow": (src, dst, demand),
            "paths": paths,
            "n_valid": len(paths),
        }

    def reset(self, seed=None):
        self._init_state()
        rng = np.random.default_rng(seed)
        self.flows = self._generate_flows(rng)
        return self._get_obs(), {}

    def step(self, action):
        src, dst, demand = self.flows[self.step_idx]
        paths = self._get_paths(src, dst)

        mlu_before = self._get_mlu()

        # Route along selected path
        a = min(action, len(paths) - 1)
        path = paths[a]
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            self.link_load[(u, v)] += demand
            self.link_load[(v, u)] += demand

        mlu_after = self._get_mlu()
        reward = -(mlu_after - mlu_before)

        self.step_idx += 1
        terminated = self.step_idx >= len(self.flows)

        info = {"mlu": mlu_after}
        if terminated:
            info["final_mlu"] = mlu_after

        return self._get_obs(), reward, terminated, False, info


def eval_baseline(cfg, strategy="sp", n_eval=20, seed_offset=100000):
    """Evaluate shortest-path or ECMP baseline."""
    mlus = []
    for i in range(n_eval):
        env = RoutingEnv(cfg)
        obs, _ = env.reset(seed=seed_offset + i)
        for t in range(len(env.flows)):
            paths = obs["paths"]
            if not paths:
                break
            if strategy == "sp":
                a = 0
            else:  # ecmp
                min_len = min(len(p) for p in paths)
                equal = [j for j, p in enumerate(paths) if len(p) == min_len]
                a = equal[t % len(equal)] if equal else 0
            obs, _, done, _, info = env.step(a)
            if done:
                break
        mlus.append(info.get("final_mlu", info["mlu"]))
    return np.mean(mlus), np.std(mlus)
