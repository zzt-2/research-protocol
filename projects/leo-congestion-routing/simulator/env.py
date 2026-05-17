"""Gymnasium routing environment for LEO constellation congestion-aware GNN routing.

K-path sequential routing: each step routes one flow by selecting from K candidate
paths. Episode length = n_flows. Reward = -(MLU_after - MLU_before) per step.

Failed edges are physically removed from the routing graph (for path generation)
but kept in edge_index/edge_features with is_failed=1.0 (for GNN input).
"""

from __future__ import annotations

from collections import defaultdict

import gymnasium as gym
import networkx as nx
import numpy as np
from gymnasium import spaces

from .config import SimConfig
from .failures import FailureInjector
from .topology import TopologyData, build_walker_delta
from .traffic import TrafficGenerator


class RoutingEnv(gym.Env):
    """GNN-based congestion-aware routing on Walker delta LEO constellation.

    Episode: n_flows steps. Each step: select from K candidate paths for one flow.
    Action: int in [0, K) selecting which candidate path to use.
    Reward: -(MLU_after - MLU_before), encouraging each routing step to minimize MLU increase.
    """

    metadata = {"render_modes": []}

    def __init__(self, config: SimConfig | None = None, seed: int | None = None) -> None:
        super().__init__()
        self.config = config or SimConfig()

        # Base topology (built once, never mutated)
        self._base_topo: TopologyData = build_walker_delta(self.config)
        self._base_nx: nx.DiGraph = self._base_topo.graph
        self._edge_index: np.ndarray = self._base_topo.edge_index
        self._E: int = self._base_topo.n_edges
        self._N: int = self.config.n_nodes
        self._capacity: float = self.config.isl_capacity_gbps
        self._K: int = self.config.k_paths

        # Remap edge features from topology layout [cap_norm, etype, dist_km, 0.0]
        # to spec layout [utilization, edge_type, is_failed, capacity_norm]
        raw = self._base_topo.edge_features
        self._edge_features_base = np.zeros_like(raw)
        self._edge_features_base[:, 0] = 0.0       # utilization (filled at runtime)
        self._edge_features_base[:, 1] = raw[:, 1]  # edge_type (intra=0 / inter=1)
        self._edge_features_base[:, 2] = 0.0       # is_failed (filled at reset)
        self._edge_features_base[:, 3] = raw[:, 0]  # capacity_norm (1.0)

        # Map (u, v) -> row index in edge_index for fast lookup
        self._edge_to_idx: dict[tuple[int, int], int] = {}
        for i in range(self._E):
            u = int(self._edge_index[0, i])
            v = int(self._edge_index[1, i])
            self._edge_to_idx[(u, v)] = i

        # Sub-modules
        self._traffic_gen = TrafficGenerator(self.config)
        self._failure_injector = FailureInjector(self.config)

        # Action/observation spaces
        self.action_space = spaces.Discrete(self._K)

        # Internal RNG (separate from gymnasium's np_random)
        self._rng: np.random.Generator = np.random.default_rng(seed)

        # Episode state (set in reset)
        self._step_idx: int = 0
        self._failed_edges: set[tuple[int, int]] = set()
        self._failed_undirected: set[tuple[int, int]] = set()
        self._flows: list[tuple[int, int, float]] = []
        self._link_load: dict[tuple[int, int], float] = defaultdict(float)
        self._current_edge_feat: np.ndarray = np.empty((0, 4), dtype=np.float32)
        self._popular_dests: list[int] = []
        self._routing_graph: nx.Graph = nx.Graph()
        self._path_cache: dict[tuple[int, int], list[list[int]]] = {}
        self._adj: dict[int, list[int]] = {}

    # ------------------------------------------------------------------
    # Gymnasium API
    # ------------------------------------------------------------------

    def reset(
        self, seed: int | None = None, options: dict | None = None,
    ) -> tuple[dict, dict]:
        super().reset(seed=seed)
        if seed is not None:
            self._rng = np.random.default_rng(seed)

        self._step_idx = 0
        self._link_load = defaultdict(float)
        self._path_cache = {}

        # Inject failures on base DiGraph to get failed edge set
        _, self._failed_edges = self._failure_injector.inject(
            self._base_nx, self._rng,
        )

        # Convert failed directed edges to undirected set
        self._failed_undirected = set()
        for u, v in self._failed_edges:
            self._failed_undirected.add(tuple(sorted((u, v))))

        # Build undirected routing graph WITHOUT failed edges
        self._routing_graph = nx.Graph()
        self._routing_graph.add_nodes_from(range(self._N))
        seen: set[tuple[int, int]] = set()
        for i in range(self._E):
            u = int(self._edge_index[0, i])
            v = int(self._edge_index[1, i])
            key = tuple(sorted((u, v)))
            if key not in self._failed_undirected and key not in seen:
                self._routing_graph.add_edge(u, v)
                seen.add(key)

        # Adjacency from routing graph (for MLP features)
        self._adj = {
            n: sorted(self._routing_graph.neighbors(n))
            for n in self._routing_graph.nodes()
        }

        # Update edge features with is_failed flag
        self._current_edge_feat = self._edge_features_base.copy()
        for u, v in self._failed_edges:
            if (u, v) in self._edge_to_idx:
                idx = self._edge_to_idx[(u, v)]
                self._current_edge_feat[idx, 2] = 1.0

        # Reset traffic generator hotspot cache so popular dests vary per episode
        self._traffic_gen._popular = None
        self._flows = self._traffic_gen.generate(self._rng, t=0)
        self._popular_dests = self._traffic_gen._popular or []

        obs = self._build_obs()
        info = self._get_info()
        return obs, info

    def step(self, action: int) -> tuple[dict, float, bool, bool, dict]:
        src, dst, demand = self._flows[self._step_idx]
        paths = self._get_paths(src, dst)

        mlu_before = self._get_mlu()

        # Route along selected path
        if paths:
            a = min(action, len(paths) - 1)
            path = paths[a]
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                self._link_load[(u, v)] += demand
                self._link_load[(v, u)] += demand

        mlu_after = self._get_mlu()
        reward = -(mlu_after - mlu_before)

        self._step_idx += 1
        terminated = self._step_idx >= len(self._flows)

        obs = self._build_obs()
        info = self._get_info()
        info["mlu"] = mlu_after
        info["mlu_before"] = mlu_before
        info["reward_decomp"] = {"delta_mlu": reward}
        info["step"] = self._step_idx
        if terminated:
            info["final_mlu"] = mlu_after

        return obs, float(reward), terminated, False, info

    # ------------------------------------------------------------------
    # Path generation
    # ------------------------------------------------------------------

    def _get_paths(self, src: int, dst: int) -> list[list[int]]:
        """Generate K candidate paths using shortest_simple_paths."""
        key = (src, dst)
        if key not in self._path_cache:
            try:
                gen = nx.shortest_simple_paths(self._routing_graph, src, dst)
                self._path_cache[key] = [p for _, p in zip(range(self._K), gen)]
            except nx.NetworkXNoPath:
                self._path_cache[key] = []
        return self._path_cache[key]

    # ------------------------------------------------------------------
    # Observation
    # ------------------------------------------------------------------

    def _get_mlu(self) -> float:
        if not self._link_load:
            return 0.0
        return max(self._link_load.values()) / self._capacity

    def _node_features(self) -> np.ndarray:
        """Compute (N, 6) node features.

        Columns: [in_load_norm, out_load_norm, is_current_src,
                  is_current_dst, current_demand_norm, is_hotspot]
        """
        feat = np.zeros((self._N, 6), dtype=np.float32)
        cap = self._capacity

        # in_load / out_load from accumulated link_load
        for (u, v), load in self._link_load.items():
            feat[v, 0] += load / cap  # in_load
            feat[u, 1] += load / cap  # out_load

        # Current flow markers
        if self._step_idx < len(self._flows):
            src, dst, demand = self._flows[self._step_idx]
            feat[src, 2] = 1.0                    # is_current_src
            feat[dst, 3] = 1.0                    # is_current_dst
            feat[src, 4] = demand / cap            # current_demand at src
            feat[dst, 4] = demand / cap            # current_demand at dst

        # Hotspot destinations
        for node_id in self._popular_dests:
            feat[node_id, 5] = 1.0

        return feat

    def _edge_features(self) -> np.ndarray:
        """Compute (E, 4) edge features with updated utilization."""
        feat = self._current_edge_feat.copy()
        cap = self._capacity
        for i in range(self._E):
            u = int(self._edge_index[0, i])
            v = int(self._edge_index[1, i])
            load = self._link_load.get((u, v), 0.0)
            feat[i, 0] = load / cap if cap > 0 else 0.0
        return feat.astype(np.float32)

    def _mlp_features(self) -> np.ndarray:
        """Local features for MLP baseline: src + dst + 1-hop loads + path lengths."""
        K = self._K
        if self._step_idx >= len(self._flows):
            return np.zeros(6 + 6 + 4 + 4 + 1 + K, dtype=np.float32)

        src, dst, demand = self._flows[self._step_idx]
        nf = self._node_features()

        src_feat = nf[src]   # (6,)
        dst_feat = nf[dst]   # (6,)

        # 1-hop neighbor loads (padded to 4)
        src_nbr_loads = np.zeros(4, dtype=np.float32)
        for i, n in enumerate(self._adj.get(src, [])[:4]):
            src_nbr_loads[i] = nf[n, 1]  # out_load of neighbor

        dst_nbr_loads = np.zeros(4, dtype=np.float32)
        for i, n in enumerate(self._adj.get(dst, [])[:4]):
            dst_nbr_loads[i] = nf[n, 1]

        # Path lengths
        paths = self._get_paths(src, dst)
        path_lens = np.zeros(K, dtype=np.float32)
        for i, p in enumerate(paths):
            path_lens[i] = len(p)

        demand_norm = np.array([demand / self._capacity], dtype=np.float32)
        return np.concatenate([src_feat, dst_feat, src_nbr_loads, dst_nbr_loads,
                               demand_norm, path_lens])

    def _build_obs(self) -> dict:
        """Build observation dict."""
        paths: list[list[int]] = []
        src, dst, demand = 0, 0, 0.0
        if self._step_idx < len(self._flows):
            src, dst, demand = self._flows[self._step_idx]
            paths = self._get_paths(src, dst)

        return {
            "node_feat": self._node_features(),
            "edge_index": self._edge_index,
            "edge_feat": self._edge_features(),
            "mlp_feat": self._mlp_features(),
            "flow": (src, dst, demand),
            "paths": paths,
            "n_valid": len(paths),
        }

    def _get_info(self) -> dict:
        return {
            "step": self._step_idx,
            "n_flows": len(self._flows),
            "n_failed": len(self._failed_undirected),
        }
