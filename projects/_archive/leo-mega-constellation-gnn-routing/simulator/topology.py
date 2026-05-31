"""+Grid ISL topology with dynamic disconnect."""
import numpy as np
from config import ISL_MAX_DISTANCE


def build_plus_grid_edges(P, S):
    """Build +Grid edge list for Walker-Delta.

    +Grid: each sat has 4 ISLs — 2 intra-orbit (k±1 in same plane)
    + 2 inter-orbit (same k in adjacent planes).
    Returns edge pairs as (2, E) unique undirected edges.
    """
    edge_set = set()
    for p in range(P):
        for k in range(S):
            idx = p * S + k
            # Intra-orbit
            edge_set.add((idx, p * S + (k + 1) % S))
            # Inter-orbit (same index in next plane)
            edge_set.add((idx, ((p + 1) % P) * S + k))
    # Sort for determinism
    edges = sorted(edge_set)
    return np.array(edges, dtype=np.int64).T  # (2, E)


def compute_distances(positions, edge_index):
    """Euclidean distances for all edges. Returns (E,) in km."""
    diff = positions[edge_index[0]] - positions[edge_index[1]]
    return np.sqrt((diff ** 2).sum(axis=-1))


def filter_by_distance(edge_index, distances, max_dist=ISL_MAX_DISTANCE):
    """Remove edges exceeding max distance (ISL disconnect).
    Returns (filtered_edge_index, filtered_distances, disconnect_mask)."""
    mask = distances <= max_dist
    return edge_index[:, mask], distances[mask], mask


def build_adjacency(N, edge_index, weights=None):
    """Build weighted adjacency list for routing.
    adj[u] = [(v, weight), ...]. Default weight = 1.0."""
    adj = [[] for _ in range(N)]
    for e in range(edge_index.shape[1]):
        u, v = int(edge_index[0, e]), int(edge_index[1, e])
        w = float(weights[e]) if weights is not None else 1.0
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj
