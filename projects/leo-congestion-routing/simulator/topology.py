"""Walker delta constellation topology generator.

Builds directed graph, PyG-format edge_index, and initial edge features.
Extended from mve_env.py build_topology().
"""

from dataclasses import dataclass

import networkx as nx
import numpy as np

from .config import SimConfig


@dataclass
class TopologyData:
    graph: nx.DiGraph
    edge_index: np.ndarray       # shape (2, E), int64
    edge_features: np.ndarray    # shape (E, 4), float32
    adj: dict[int, list[int]]
    n_edges: int


def build_walker_delta(config: SimConfig) -> TopologyData:
    """Build Walker delta constellation topology.

    Node id: plane * sats_per_plane + sat_index
    Intra-plane ISLs (etype=0): ring within each orbital plane.
    Inter-plane ISLs (etype=1): between adjacent planes at same sat index.
    Polar gap handling deferred to failures.py.
    """
    P, S = config.n_planes, config.sats_per_plane
    G = nx.DiGraph()

    for p in range(P):
        for s in range(S):
            G.add_node(p * S + s)

    # Intra-plane ring ISLs (directed both ways)
    for p in range(P):
        for s in range(S):
            u = p * S + s
            v = p * S + (s + 1) % S
            G.add_edge(u, v, etype=0, capacity_norm=1.0, distance_km=1.0)
            G.add_edge(v, u, etype=0, capacity_norm=1.0, distance_km=1.0)

    # Inter-plane ISLs (directed both ways)
    for p in range(P):
        for s in range(S):
            u = p * S + s
            v = ((p + 1) % P) * S + s
            G.add_edge(u, v, etype=1, capacity_norm=1.0, distance_km=1.0)
            G.add_edge(v, u, etype=1, capacity_norm=1.0, distance_km=1.0)

    return _graph_to_topology_data(G, config)


def _graph_to_topology_data(
    G: nx.DiGraph, config: SimConfig
) -> TopologyData:
    """Convert nx.DiGraph to TopologyData with edge_index and features."""
    adj: dict[int, list[int]] = {n: sorted(G.successors(n)) for n in G.nodes()}

    srcs, dsts = [], []
    feat_rows: list[list[float]] = []

    for u, v, d in G.edges(data=True):
        srcs.append(u)
        dsts.append(v)
        # [capacity_norm, edge_type, distance_km, 0.0 (is_failed)]
        feat_rows.append([
            d.get("capacity_norm", 1.0),
            float(d.get("etype", 0)),
            d.get("distance_km", 1.0),
            0.0,
        ])

    edge_index = np.array([srcs, dsts], dtype=np.int64)
    edge_features = np.array(feat_rows, dtype=np.float32)
    n_edges = len(srcs)

    return TopologyData(
        graph=G,
        edge_index=edge_index,
        edge_features=edge_features,
        adj=adj,
        n_edges=n_edges,
    )
