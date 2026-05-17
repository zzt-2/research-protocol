"""Gymnasium routing environment for LEO constellation congestion-aware GNN routing.

GNN outputs per-edge continuous weights -> weighted shortest-path routes all flows
simultaneously -> minimize MLU. Failed edges remain in edge_index with is_failed=1.0
so model parameter dimensions stay fixed.
"""

from __future__ import annotations

from collections import defaultdict

import gymnasium as gym
import networkx as nx
import numpy as np
import torch
from gymnasium import spaces
from torch_geometric.data import Data

from .config import SimConfig
from .failures import FailureInjector
from .topology import TopologyData, build_walker_delta
from .traffic import TrafficGenerator


class RoutingEnv(gym.Env):
    """GNN-based congestion-aware routing on Walker delta LEO constellation.

    Episode: t_slots steps. Each step: GNN predicts edge weights -> weighted SP
    routes all flows simultaneously -> compute MLU -> reward = -MLU.
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

        # Remap base features from topology layout [cap_norm, etype, dist_km, 0.0]
        # to spec layout [utilization(0.0), edge_type, is_failed(0.0), capacity_norm]
        raw = self._base_topo.edge_features  # (E, 4)
        self._edge_features_base = np.zeros_like(raw)
        self._edge_features_base[:, 0] = 0.0                       # utilization (filled at runtime)
        self._edge_features_base[:, 1] = raw[:, 1]                 # edge_type (intra=0 / inter=1)
        self._edge_features_base[:, 2] = 0.0                       # is_failed (filled at reset)
        self._edge_features_base[:, 3] = raw[:, 0]                 # capacity_norm (1.0)

        # Map (u, v) -> row index in edge_index for fast lookup
        self._edge_to_idx: dict[tuple[int, int], int] = {}
        for i in range(self._E):
            u = int(self._edge_index[0, i])
            v = int(self._edge_index[1, i])
            self._edge_to_idx[(u, v)] = i

        # Max degree for normalization
        self._max_degree: int = max(
            len(list(self._base_nx.successors(n))) + len(list(self._base_nx.predecessors(n)))
            for n in self._base_nx.nodes()
        )

        # Sub-modules
        self._traffic_gen = TrafficGenerator(self.config)
        self._failure_injector = FailureInjector(self.config)

        # Action/observation spaces
        self.action_space = spaces.Box(
            low=0.0, high=float("inf"), shape=(self._E,), dtype=np.float32,
        )
        self.observation_space = spaces.Dict({
            "x": spaces.Box(low=-1.0, high=10.0, shape=(self._N, 6), dtype=np.float32),
            "edge_index": spaces.Box(low=0, high=self._N - 1, shape=(2, self._E), dtype=np.int64),
            "edge_attr": spaces.Box(low=-1.0, high=10.0, shape=(self._E, 4), dtype=np.float32),
        })

        # Internal RNG (separate from gymnasium's np_random)
        self._rng: np.random.Generator = np.random.default_rng(seed)

        # Episode state (set in reset)
        self._t: int = 0
        self._failed_edges: set[tuple[int, int]] = set()
        self._flows: list[tuple[int, int, float]] = []
        self._link_load: dict[tuple[int, int], float] = defaultdict(float)
        self._current_edge_feat: np.ndarray = np.empty((0, 4), dtype=np.float32)
        self._popular_dests: list[int] = []

    # ------------------------------------------------------------------
    # Gymnasium API
    # ------------------------------------------------------------------

    def reset(
        self, seed: int | None = None, options: dict | None = None,
    ) -> tuple[Data, dict]:
        super().reset(seed=seed)
        if seed is not None:
            self._rng = np.random.default_rng(seed)

        self._t = 0
        self._link_load = defaultdict(float)

        # Inject failures on a fresh copy of base topology
        _, self._failed_edges = self._failure_injector.inject(
            self._base_nx, self._rng,
        )

        # Build edge features with is_failed column set
        self._current_edge_feat = self._edge_features_base.copy()
        for u, v in self._failed_edges:
            if (u, v) in self._edge_to_idx:
                idx = self._edge_to_idx[(u, v)]
                self._current_edge_feat[idx, 2] = 1.0  # is_failed

        # Reset traffic generator hotspot cache so popular dests vary per episode
        self._traffic_gen._popular = None
        self._flows = self._traffic_gen.generate(self._rng, t=0)
        self._popular_dests = self._traffic_gen._popular or []

        obs = self._build_obs()
        info = self._get_info()
        return obs, info

    def step(
        self, action: np.ndarray,
    ) -> tuple[Data, float, bool, bool, dict]:
        action = np.asarray(action, dtype=np.float64).ravel()
        assert action.shape == (self._E,), f"action shape {action.shape}, expected ({self._E},)"

        # 1. Build weighted graph from action
        weighted_graph = self._build_weighted_graph(action)

        # 2. Route all flows simultaneously
        link_load, mlu, n_overflow = self._route_flows(weighted_graph, self._flows)
        self._link_load = link_load

        # 3. Reward
        reward = -mlu

        # 4. Advance time
        self._t += 1
        terminated = self._t >= self.config.t_slots

        # 5. Generate new traffic for next step (or empty if terminated)
        if not terminated:
            self._flows = self._traffic_gen.generate(self._rng, t=self._t)

        # 6. Build observation with updated loads
        obs = self._build_obs()
        info = self._get_info()
        info["mlu"] = mlu
        info["n_overflow"] = n_overflow
        info["reward_decomp"] = {"mlu": -mlu}
        info["step"] = self._t

        return obs, float(reward), terminated, False, info

    # ------------------------------------------------------------------
    # Internal: routing
    # ------------------------------------------------------------------

    def _build_weighted_graph(self, action: np.ndarray) -> nx.DiGraph:
        """Create nx.DiGraph with action weights; failed edges get weight=1e9."""
        G = nx.DiGraph()
        G.add_nodes_from(range(self._N))

        for i in range(self._E):
            u = int(self._edge_index[0, i])
            v = int(self._edge_index[1, i])
            is_failed = (u, v) in self._failed_edges
            w = 1e9 if is_failed else float(action[i])
            G.add_edge(u, v, weight=w)

        return G

    def _route_flows(
        self, G: nx.DiGraph, flows: list[tuple[int, int, float]],
    ) -> tuple[dict[tuple[int, int], float], float, int]:
        """Simultaneously route all flows via weighted shortest path.

        Returns:
            link_load: dict mapping directed edge -> total demand routed through it.
            mlu: max link utilization (max_load / capacity).
            n_overflow: number of unreachable flows.
        """
        link_load: dict[tuple[int, int], float] = defaultdict(float)
        n_overflow = 0

        for src, dst, demand in flows:
            try:
                path = nx.shortest_path(G, src, dst, weight="weight")
                for i in range(len(path) - 1):
                    link_load[(path[i], path[i + 1])] += demand
            except nx.NetworkXNoPath:
                n_overflow += 1

        max_load = max(link_load.values()) if link_load else 0.0
        mlu = max_load / self._capacity if self._capacity > 0 else 0.0
        return link_load, mlu, n_overflow

    # ------------------------------------------------------------------
    # Internal: observation
    # ------------------------------------------------------------------

    def _build_obs(self) -> Data:
        """Build PyG Data observation."""
        node_feat = self._node_features()      # (N, 6)
        edge_feat = self._edge_features()       # (E, 4)

        return Data(
            x=torch.from_numpy(node_feat),
            edge_index=torch.from_numpy(self._edge_index.copy()),
            edge_attr=torch.from_numpy(edge_feat),
        )

    def _node_features(self) -> np.ndarray:
        """Compute (N, 6) node features.

        Columns: [in_load_norm, out_load_norm, demand_as_src_norm,
                  demand_as_dst_norm, is_hotspot, degree_norm]
        """
        feat = np.zeros((self._N, 6), dtype=np.float32)
        cap = self._capacity

        # in_load / out_load from link_load
        for (u, v), load in self._link_load.items():
            feat[v, 0] += load / cap  # in_load
            feat[u, 1] += load / cap  # out_load

        # Demand aggregation from current flows
        demand_as_src = np.zeros(self._N, dtype=np.float64)
        demand_as_dst = np.zeros(self._N, dtype=np.float64)
        for src, dst, demand in self._flows:
            demand_as_src[src] += demand
            demand_as_dst[dst] += demand
        feat[:, 2] = (demand_as_src / cap).astype(np.float32)
        feat[:, 3] = (demand_as_dst / cap).astype(np.float32)

        # Hotspot destinations
        for node_id in self._popular_dests:
            feat[node_id, 4] = 1.0

        # Degree normalization
        for n in range(self._N):
            deg = len(list(self._base_nx.successors(n))) + len(
                list(self._base_nx.predecessors(n))
            )
            feat[n, 5] = deg / self._max_degree if self._max_degree > 0 else 0.0

        return feat

    def _edge_features(self) -> np.ndarray:
        """Compute (E, 4) edge features with updated utilization.

        Columns: [utilization, edge_type, is_failed, capacity_norm]
        Only utilization (col 0) changes per step; cols 1-3 are static from reset.
        """
        feat = self._current_edge_feat.copy()
        cap = self._capacity

        for i in range(self._E):
            u = int(self._edge_index[0, i])
            v = int(self._edge_index[1, i])
            load = self._link_load.get((u, v), 0.0)
            feat[i, 0] = load / cap if cap > 0 else 0.0  # utilization

        return feat.astype(np.float32)

    def _get_info(self) -> dict:
        return {
            "step": self._t,
            "n_flows": len(self._flows),
            "n_failed": len(self._failed_edges),
        }
