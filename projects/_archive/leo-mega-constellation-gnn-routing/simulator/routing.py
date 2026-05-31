"""Routing algorithms: Dijkstra shortest path."""
import heapq
import numpy as np


def dijkstra(adj, source, N):
    """Single-source shortest paths.

    adj: adjacency list, adj[u] = [(v, weight), ...]
    Returns (dist, parent) arrays of length N.
    """
    dist = np.full(N, np.inf)
    parent = np.full(N, -1, dtype=np.int32)
    dist[source] = 0.0
    pq = [(0.0, source)]
    visited = np.zeros(N, dtype=bool)

    while pq:
        d, u = heapq.heappop(pq)
        if visited[u]:
            continue
        visited[u] = True
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, parent


def dijkstra_all_pairs(adj, N):
    """All-pairs shortest paths via Dijkstra.
    Returns (dist_matrix, next_hop_matrix).
    next_hop[i][j] = first node on shortest path from i to j.
    """
    dist_matrix = np.full((N, N), np.inf)
    next_hop = np.full((N, N), -1, dtype=np.int32)

    for src in range(N):
        dist, parent = dijkstra(adj, src, N)
        dist_matrix[src] = dist
        # Trace next_hop from parent
        for dst in range(N):
            if dst == src or parent[dst] < 0:
                continue
            cur = dst
            while parent[cur] != src:
                cur = parent[cur]
            next_hop[src, dst] = cur

    return dist_matrix, next_hop


def compute_delay_metrics(dist_matrix, flows):
    """Compute routing metrics from distance matrix and flow list.

    flows: (n_flows, 2) array of (src, dst) pairs.
    Returns dict with mean_delay, p95_delay, max_delay in same unit as dist.
    """
    delays = dist_matrix[flows[:, 0], flows[:, 1]]
    finite = delays[np.isfinite(delays)]
    if len(finite) == 0:
        return dict(mean_delay=np.inf, p95_delay=np.inf, max_delay=np.inf,
                    unreachable=len(delays))
    return dict(
        mean_delay=np.mean(finite),
        p95_delay=np.percentile(finite, 95),
        max_delay=np.max(finite),
        unreachable=int(np.sum(~np.isfinite(delays))),
    )
