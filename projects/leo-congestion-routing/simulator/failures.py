"""Link failure injector for LEO constellation topology.

Supports random independent and regional failure modes.
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
        """Remove all edges around a randomly chosen node (regional outage)."""
        cfg = self._config
        n_nodes = cfg.n_nodes
        n_regional = max(1, int(n_nodes * 0.1))
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
