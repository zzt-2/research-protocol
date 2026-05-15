"""M6: Router — Dijkstra / k-shortest-paths + proportional congestion allocation.

Routes flow demands on the active ISL topology. Edge weight =
propagation delay (d/c) + hop delay (1 ms per hop) [L04].

Single-path mode (route): Dijkstra shortest path per flow.
Multi-path mode (route_multipath): Yen's k-shortest-paths, split demand
inversely proportional to path cost, then iterative congestion resolution.
"""

import numpy as np
import heapq
from collections import defaultdict
from . import config


class Router:
    def __init__(self, hop_delay=None):
        self.hop_delay = hop_delay if hop_delay is not None else config.HOP_DELAY

    def _build_graph(self, active_edges, edge_distances, edge_capacities):
        """Build adjacency, weights, and capacity dicts from edge lists."""
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
        return adj, cap

    # --- Single-path routing (original) ---

    def route(self, active_edges, edge_distances, edge_capacities, flows, n_sats):
        """Single-path Dijkstra routing with congestion resolution."""
        adj, cap = self._build_graph(active_edges, edge_distances, edge_capacities)
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
                link_loads[(path[k], path[k + 1])] += demand

        delivered = self._resolve_congestion(flow_paths, link_loads, cap)
        total_demand = sum(f[3] for f in flow_paths)

        return {
            'delivered': delivered,
            'total_demand': total_demand,
            'flow_details': flow_paths,
            'link_loads': dict(link_loads),
        }

    # --- Multi-path routing (k-shortest-paths + weighted splitting) ---

    def route_multipath(self, active_edges, edge_distances, edge_capacities,
                        flows, n_sats, k_paths=4):
        """Multi-path routing using Yen's k-shortest-paths.

        Finds k shortest paths per flow, splits demand inversely proportional
        to path cost, then applies iterative congestion resolution.
        """
        adj, cap = self._build_graph(active_edges, edge_distances, edge_capacities)
        link_loads = defaultdict(float)
        flow_paths = []
        total_demand = 0.0

        for src, dst, demand in flows:
            if src == dst:
                continue
            total_demand += demand
            paths = self._yen_k_shortest(src, dst, adj, n_sats, k=k_paths)
            if not paths:
                flow_paths.append((src, dst, 0, demand, []))
                continue

            # Split demand inversely proportional to cost
            inv_costs = [1.0 / p_cost for p_cost, _ in paths]
            total_inv = sum(inv_costs)
            for (p_cost, path), inv_c in zip(paths, inv_costs):
                frac = inv_c / total_inv
                split = demand * frac
                flow_paths.append((src, dst, split, demand, path))
                for k in range(len(path) - 1):
                    link_loads[(path[k], path[k + 1])] += split

        delivered = self._resolve_congestion(flow_paths, link_loads, cap)

        return {
            'delivered': delivered,
            'total_demand': total_demand,
            'flow_details': flow_paths,
            'link_loads': dict(link_loads),
        }

    # --- Congestion resolution (shared) ---

    @staticmethod
    def _resolve_congestion(flow_paths, link_loads, cap):
        """Iterative proportional reduction on overloaded links."""
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

        return sum(f[2] for f in flow_paths)

    # --- Path finding algorithms ---

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

    @staticmethod
    def _dijkstra_with_cost(src, dst, adj):
        """Dijkstra returning (cost, path) or None."""
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
                return d, _reconstruct(prev, dst)
            for v, w in adj.get(u, []):
                if v in visited:
                    continue
                nd = d + w
                if nd < dist.get(v, np.inf):
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(heap, (nd, v))
        return None

    def _yen_k_shortest(self, src, dst, adj, n_sats, k=4):
        """Yen's algorithm for k shortest loopless paths.

        Returns list of (cost, path) tuples sorted by cost.
        """
        first = self._dijkstra_with_cost(src, dst, adj)
        if first is None:
            return []

        shortest = [first]
        candidates = []

        for ki in range(1, k):
            prev_cost, prev_path = shortest[ki - 1]
            for i in range(len(prev_path) - 1):
                spur_node = prev_path[i]
                root_path = prev_path[:i + 1]
                root_cost = 0.0
                for r in range(len(root_path) - 1):
                    u, v = root_path[r], root_path[r + 1]
                    for nb, w in adj.get(u, []):
                        if nb == v:
                            root_cost += w
                            break

                # Remove edges that share root_path prefix
                blocked_edges = set()
                for cost_p, path_p in shortest:
                    if len(path_p) > i and path_p[:i + 1] == root_path:
                        blocked_edges.add((path_p[i], path_p[i + 1]))

                # Remove spur_node's predecessors in root_path (except last)
                blocked_nodes = set(root_path[:-1])

                spur_result = self._dijkstra_with_cost(
                    spur_node, dst, adj, blocked_edges, blocked_nodes)
                if spur_result is None:
                    continue

                spur_cost, spur_path = spur_result
                total_path = root_path[:-1] + spur_path
                total_cost = root_cost + spur_cost
                candidates.append((total_cost, total_path))

            if not candidates:
                break
            candidates.sort()
            shortest.append(candidates.pop(0))

        return shortest

    @staticmethod
    def _dijkstra_with_cost(src, dst, adj, blocked_edges=None, blocked_nodes=None):
        """Dijkstra with optional edge/node blocking for Yen's spur paths."""
        blocked_edges = blocked_edges or set()
        blocked_nodes = blocked_nodes or set()

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
                return d, _reconstruct(prev, dst)
            for v, w in adj.get(u, []):
                if v in visited:
                    continue
                if v in blocked_nodes and v != dst:
                    continue
                if (u, v) in blocked_edges:
                    continue
                nd = d + w
                if nd < dist.get(v, np.inf):
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(heap, (nd, v))
        return None


def _reconstruct(prev, dst):
    """Reconstruct path from prev dict."""
    path = []
    u = dst
    while u is not None:
        path.append(u)
        u = prev[u]
    path.reverse()
    return path
