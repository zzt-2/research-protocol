"""M6: Router — Dijkstra shortest path + proportional congestion allocation.

Routes flow demands on the active ISL topology. Edge weight =
propagation delay (d/c) + hop delay (1 ms per hop) [L04].

Congestion handling: if total demand on an ISL exceeds its capacity,
all flows through that ISL are proportionally reduced. Iterates until
no overloaded links remain (max 10 rounds).
"""

import numpy as np
import heapq
from collections import defaultdict
from . import config


class Router:
    def __init__(self, hop_delay=None):
        self.hop_delay = hop_delay if hop_delay is not None else config.HOP_DELAY

    def route(self, active_edges, edge_distances, edge_capacities, flows, n_sats):
        """Route all flows on the active ISL topology.

        Args:
            active_edges: list of (i, j) tuples — each represents a bidirectional ISL.
            edge_distances: dict {(i,j): distance_km}.
            edge_capacities: dict {(i,j): capacity_gbps}.
            flows: list of (src_sat, dst_sat, demand_gbps) tuples.
            n_sats: number of satellites.

        Returns:
            dict with delivered, total_demand, flow_details, link_loads.
        """
        # Build adjacency
        adj = defaultdict(list)
        cap = {}
        for i, j in active_edges:
            d = edge_distances.get((i, j), edge_distances.get((j, i), 1000))
            w = d / config.C_LIGHT + self.hop_delay
            adj[i].append((j, w))
            adj[j].append((i, w))
            c = edge_capacities.get((i, j), edge_capacities.get((j, i), 0))
            cap[(i, j)] = c
            cap[(j, i)] = c

        # Find paths and accumulate loads
        link_loads = defaultdict(float)
        flow_paths = []

        for src, dst, demand in flows:
            if src == dst:
                continue
            path = self._dijkstra(src, dst, adj, n_sats)
            if path is None:
                flow_paths.append((src, dst, 0, demand, []))
                continue
            flow_paths.append((src, dst, demand, demand, path))
            for k in range(len(path) - 1):
                ek = (path[k], path[k + 1])
                link_loads[ek] += demand

        # Congestion resolution: iterative proportional reduction
        for _ in range(10):
            overloaded = False
            edge_ratio = {}
            for ek, load in link_loads.items():
                c = cap.get(ek, 0)
                if load > c > 0:
                    edge_ratio[ek] = c / load
                    overloaded = True
                elif c <= 0 and load > 0:
                    edge_ratio[ek] = 0.0
                    overloaded = True

            if not overloaded:
                break

            new_loads = defaultdict(float)
            for idx, (src, dst, delivered, demand, path) in enumerate(flow_paths):
                if not path:
                    continue
                min_ratio = min(
                    (edge_ratio.get((path[k], path[k + 1]), 1.0)
                     for k in range(len(path) - 1)),
                    default=1.0,
                )
                new_del = delivered * min_ratio
                flow_paths[idx] = (src, dst, new_del, demand, path)
                for k in range(len(path) - 1):
                    new_loads[(path[k], path[k + 1])] += new_del
            link_loads = new_loads

        delivered = sum(f[2] for f in flow_paths)
        total_demand = sum(f[3] for f in flow_paths)

        return {
            'delivered': delivered,
            'total_demand': total_demand,
            'flow_details': flow_paths,
            'link_loads': dict(link_loads),
        }

    @staticmethod
    def _dijkstra(src, dst, adj, n_sats):
        """Shortest-path Dijkstra. Returns list of node indices or None."""
        dist = {src: 0.0}
        prev = {src: None}
        heap = [(0.0, src)]
        visited = set()

        while heap:
            d, u = heapq.heappop(heap)
            if u in visited:
                continue
            visited.add(u)
            if u == dst:
                break
            for v, w in adj.get(u, []):
                if v in visited:
                    continue
                nd = d + w
                if nd < dist.get(v, np.inf):
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(heap, (nd, v))

        if dst not in prev:
            return None

        path = []
        u = dst
        while u is not None:
            path.append(u)
            u = prev[u]
        path.reverse()
        return path
