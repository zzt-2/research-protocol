"""Link failure injector for LEO constellation topology.

Supports random independent, regional, and cascading failure modes.
Extended from mve_env.py RoutingEnv66.reset().
"""

from __future__ import annotations

from copy import deepcopy

import networkx as nx
import numpy as np

from .config import SimConfig


class FailureInjector:
    def __init__(self, config: SimConfig) -> None:
        self._config = config

    def inject(
        self,
        graph: nx.DiGraph,
        rng: np.random.Generator,
    ) -> tuple[nx.DiGraph, set[tuple[int, int]]]:
        """Inject link failures into a copy of the graph.

        Returns:
            Modified graph copy and set of failed directed edge tuples.
        """
        cfg = self._config
        G = deepcopy(graph)
        failed: set[tuple[int, int]] = set()

        if cfg.failure_rate <= 0:
            return G, failed

        if cfg.failure_mode == "random":
            failed = self._inject_random(G, rng)
        elif cfg.failure_mode == "regional":
            failed = self._inject_regional(G, rng)
        elif cfg.failure_mode == "cascading":
            failed = self._inject_cascading(G, rng)

        return G, failed

    def _inject_random(
        self, G: nx.DiGraph, rng: np.random.Generator
    ) -> set[tuple[int, int]]:
        """Remove random undirected edges at failure_rate proportion."""
        cfg = self._config
        undirected_edges = list({tuple(sorted(e)) for e in G.edges()})
        n_to_remove = max(1, int(len(undirected_edges) * cfg.failure_rate))
        chosen = rng.choice(len(undirected_edges), size=n_to_remove, replace=False)

        failed: set[tuple[int, int]] = set()
        for idx in chosen:
            u, v = undirected_edges[idx]
            if G.has_edge(u, v):
                G.remove_edge(u, v)
                failed.add((u, v))
            if G.has_edge(v, u):
                G.remove_edge(v, u)
                failed.add((v, u))
        return failed

    def _inject_regional(
        self, G: nx.DiGraph, rng: np.random.Generator
    ) -> set[tuple[int, int]]:
        """Remove all edges around randomly chosen nodes (regional outage).

        Number of center nodes scales with failure_rate.
        """
        cfg = self._config
        n_nodes = cfg.n_nodes
        n_regional = max(1, int(n_nodes * cfg.failure_rate))
        centers = rng.choice(n_nodes, size=n_regional, replace=False)

        failed: set[tuple[int, int]] = set()
        for center in centers:
            neighbors = list(G.neighbors(center))
            for nb in neighbors:
                if G.has_edge(center, nb):
                    G.remove_edge(center, nb)
                    failed.add((center, nb))
                if G.has_edge(nb, center):
                    G.remove_edge(nb, center)
                    failed.add((nb, center))
        return failed

    def _inject_cascading(
        self, G: nx.DiGraph, rng: np.random.Generator
    ) -> set[tuple[int, int]]:
        """Cascading failure: initial random failures propagate to neighbors.

        Initial failures at half the normal rate, then each failed edge's
        adjacent edges fail with probability cascade_prob (0.5). Propagation
        runs for up to max_rounds (3) iterations.
        """
        cfg = self._config
        cascade_prob = 0.5
        max_rounds = 3
        initial_rate = cfg.failure_rate * 0.5

        # Phase 1: seed failures (fewer than pure random)
        undirected_edges = list({tuple(sorted(e)) for e in G.edges()})
        n_seed = max(1, int(len(undirected_edges) * initial_rate))
        seed_idx = rng.choice(len(undirected_edges), size=n_seed, replace=False)

        failed: set[tuple[int, int]] = set()
        failed_undirected: set[tuple[int, int]] = set()

        for idx in seed_idx:
            u, v = undirected_edges[idx]
            for a, b in [(u, v), (v, u)]:
                if G.has_edge(a, b):
                    G.remove_edge(a, b)
                    failed.add((a, b))
            failed_undirected.add((u, v))

        # Phase 2: cascading propagation
        for _ in range(max_rounds):
            new_undirected: set[tuple[int, int]] = set()
            for u, v in failed_undirected:
                for node in (u, v):
                    for nb in list(G.neighbors(node)):
                        edge_key = tuple(sorted((node, nb)))
                        if edge_key not in failed_undirected and rng.random() < cascade_prob:
                            for a, b in [(node, nb), (nb, node)]:
                                if G.has_edge(a, b):
                                    G.remove_edge(a, b)
                                    failed.add((a, b))
                            new_undirected.add(edge_key)
            if not new_undirected:
                break
            failed_undirected |= new_undirected

        return failed


def rebuild_edge_structures(
    graph: nx.DiGraph,
    config: SimConfig,
) -> tuple[np.ndarray, np.ndarray, dict[int, list[int]]]:
    """Rebuild edge_index, edge_features, and adj from an nx.DiGraph.

    Used after failure injection to update PyG-format structures.
    """
    adj: dict[int, list[int]] = {n: sorted(graph.successors(n)) for n in graph.nodes()}

    srcs: list[int] = []
    dsts: list[int] = []
    feat_rows: list[list[float]] = []

    for u, v, d in graph.edges(data=True):
        srcs.append(u)
        dsts.append(v)
        feat_rows.append([
            d.get("capacity_norm", 1.0),
            float(d.get("etype", 0)),
            d.get("distance_km", 1.0),
            float(d.get("is_failed", 0.0)),
        ])

    edge_index = np.array([srcs, dsts], dtype=np.int64) if srcs else np.empty((2, 0), dtype=np.int64)
    edge_features = np.array(feat_rows, dtype=np.float32) if feat_rows else np.empty((0, 4), dtype=np.float32)

    return edge_index, edge_features, adj
