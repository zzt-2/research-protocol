"""Walker-Delta constellation topology with latitude-based polar gap.

Builds directed graph, PyG-format edge_index, and initial edge features.
Polar gap: inter-plane ISLs disabled when either endpoint's latitude
exceeds polar_gap_lat threshold (Iridium-like antenna tracking limit).
"""
from dataclasses import dataclass

import networkx as nx
import numpy as np

from .config import SimConfig
from .constellation import WalkerDelta


@dataclass
class TopologyData:
    graph: nx.DiGraph
    edge_index: np.ndarray       # shape (2, E), int64
    edge_features: np.ndarray    # shape (E, 4), float32
    adj: dict[int, list[int]]
    n_edges: int
    degree: np.ndarray           # shape (N,), undirected degree per node
    lats: np.ndarray             # shape (N,), latitude in degrees


def build_walker_delta(config: SimConfig, t: float = 0.0) -> TopologyData:
    """Build Walker-Delta constellation topology with polar gap.

    Steps:
      1. Compute satellite positions via orbital mechanics
      2. Build full +Grid (intra-plane ring + inter-plane links)
      3. Remove inter-plane ISLs where either endpoint exceeds polar_gap_lat
      4. Build directed graph with real distances
    """
    P, S = config.n_planes, config.sats_per_plane
    N = P * S

    # Orbital mechanics
    wd = WalkerDelta(P, S, F=config.walker_delta_F,
                     alt=config.altitude_km, inc=config.inclination_deg)
    pos = wd.positions(t=t)
    lats = wd.latitudes(t=t)

    G = nx.DiGraph()
    for n in range(N):
        G.add_node(n)

    # Intra-plane ring ISLs (always present, directed both ways)
    for p in range(P):
        for s in range(S):
            u = p * S + s
            v = p * S + (s + 1) % S
            dist = float(np.linalg.norm(pos[u] - pos[v]))
            G.add_edge(u, v, etype=0, capacity_norm=1.0, distance_km=dist)
            G.add_edge(v, u, etype=0, capacity_norm=1.0, distance_km=dist)

    # Inter-plane ISLs (disabled at polar latitudes)
    gap_lat = config.polar_gap_lat
    for p in range(P):
        for s in range(S):
            u = p * S + s
            v = ((p + 1) % P) * S + s
            # Polar gap: skip if either endpoint above threshold
            if abs(lats[u]) >= gap_lat or abs(lats[v]) >= gap_lat:
                continue
            dist = float(np.linalg.norm(pos[u] - pos[v]))
            G.add_edge(u, v, etype=1, capacity_norm=1.0, distance_km=dist)
            G.add_edge(v, u, etype=1, capacity_norm=1.0, distance_km=dist)

    return _graph_to_topology_data(G, config, pos, lats)


def _graph_to_topology_data(
    G: nx.DiGraph, config: SimConfig,
    pos: np.ndarray, lats: np.ndarray,
) -> TopologyData:
    """Convert nx.DiGraph to TopologyData with edge_index and features."""
    adj: dict[int, list[int]] = {n: sorted(G.successors(n)) for n in G.nodes()}

    srcs, dsts = [], []
    feat_rows: list[list[float]] = []

    for u, v, d in G.edges(data=True):
        srcs.append(u)
        dsts.append(v)
        feat_rows.append([
            d.get("capacity_norm", 1.0),
            float(d.get("etype", 0)),
            d.get("distance_km", 1.0),
            0.0,
        ])

    edge_index = np.array([srcs, dsts], dtype=np.int64)
    edge_features = np.array(feat_rows, dtype=np.float32)

    # Compute undirected degree for each node
    undirected = nx.Graph()
    undirected.add_nodes_from(G.nodes())
    for u, v in G.edges():
        undirected.add_edge(u, v)
    degree = np.array([undirected.degree(n) for n in range(config.n_nodes)], dtype=np.int32)

    return TopologyData(
        graph=G,
        edge_index=edge_index,
        edge_features=edge_features,
        adj=adj,
        n_edges=len(srcs),
        degree=degree,
        lats=lats.astype(np.float32),
    )
