#!/usr/bin/env python3
"""ECMP baseline: round-robin among ALL equal-cost shortest paths.

True ECMP enumerates every shortest path (by hop count) between src and dst
on the routing graph, then round-robins flows among them. This is NOT limited
to the K=4 candidate paths used by the GNN/MLP action space.
"""

from __future__ import annotations

import sys
from collections import defaultdict, deque
from pathlib import Path

import numpy as np

_PROJECT = Path(__file__).resolve().parent.parent
if str(_PROJECT) not in sys.path:
    sys.path.insert(0, str(_PROJECT))

from simulator.config import SimConfig
from simulator.env import RoutingEnv
from simulator.metrics import aggregate_metrics, compute_episode_metrics

SPEED_OF_LIGHT_KM_S = 299792.458  # km/s (free space)
CONGESTION_DELAY_CAP = 100.0      # must match env.py


def _all_shortest_paths_bfs(
    graph: "nx.Graph",  # noqa: F821
    src: int,
    dst: int,
) -> list[list[int]]:
    """Enumerate ALL shortest paths from src to dst using BFS.

    Returns every path of minimum hop count. Uses BFS to first find the
    shortest distance, then backtracks to enumerate all paths of that length.
    """
    if src == dst:
        return [[src]]

    # BFS to find shortest distance and build predecessor map
    # predecessors[v] = list of u where (u,v) is on a shortest path from src
    dist: dict[int, int] = {src: 0}
    predecessors: dict[int, list[int]] = defaultdict(list)
    queue: deque[int] = deque([src])
    found_dist: int | None = None

    while queue:
        u = queue.popleft()
        d = dist[u]

        # Stop exploring beyond shortest distance to dst
        if found_dist is not None and d >= found_dist:
            continue

        for v in graph.neighbors(u):
            if v not in dist:
                dist[v] = d + 1
                predecessors[v].append(u)
                queue.append(v)
                if v == dst:
                    found_dist = d + 1
            elif dist[v] == d + 1:
                # Another shortest-path predecessor
                predecessors[v].append(u)

    if found_dist is None:
        return []

    # Backtrack from dst to src to enumerate all shortest paths
    paths: list[list[int]] = []

    def _backtrack(node: int, path: list[int]) -> None:
        if node == src:
            paths.append(list(reversed(path)))
            return
        for pred in predecessors[node]:
            path.append(pred)
            _backtrack(pred, path)
            path.pop()

    _backtrack(dst, [dst])
    return paths


def _route_episode_ecmp(
    env: RoutingEnv,
    seed: int,
) -> tuple[float, dict, dict[tuple[int, int], float]]:
    """Route one episode using true ECMP.

    Uses env.reset() to generate the same topology/failures/traffic as other
    baselines, then routes all flows using externally-computed equal-cost paths.

    Returns:
        (final_mlu, stats, link_load) where stats includes equal-cost path
        count info, delay stats, and link_load is the per-edge load dict.
    """
    obs, info = env.reset(seed=seed)

    # Access env internals for the routing graph and flows
    routing_graph = env._routing_graph
    flows = env._flows
    capacity = env._capacity
    edge_distances = env._edge_distances

    # Accumulate link loads (same logic as env)
    link_load: dict[tuple[int, int], float] = defaultdict(float)

    # Cache for equal-cost paths: (src, dst) -> list of paths
    ecmp_cache: dict[tuple[int, int], list[list[int]]] = {}

    n_paths_per_flow: list[int] = []
    flow_delays: list[float] = []  # propagation delays in seconds
    step_idx = 0

    for src, dst, demand in flows:
        key = (src, dst)
        if key not in ecmp_cache:
            ecmp_cache[key] = _all_shortest_paths_bfs(routing_graph, src, dst)
        paths = ecmp_cache[key]

        n_paths = len(paths)
        n_paths_per_flow.append(n_paths)

        if paths:
            # Round-robin among all equal-cost paths
            path = paths[step_idx % n_paths]
            # Compute delay BEFORE updating loads (uses current congestion state)
            path_delay = 0.0
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                dist = edge_distances.get((u, v), 0.0)
                prop_delay = dist / SPEED_OF_LIGHT_KM_S
                util = link_load.get((u, v), 0.0) / capacity
                # M/M/1 queuing: delay_factor = 1/(1-util), capped for overload
                if util >= 1.0:
                    cong_factor = CONGESTION_DELAY_CAP
                else:
                    cong_factor = 1.0 / (1.0 - util)
                path_delay += prop_delay * cong_factor
            # Update loads
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                link_load[(u, v)] += demand
                link_load[(v, u)] += demand
            flow_delays.append(path_delay)
        else:
            flow_delays.append(0.0)

        step_idx += 1

    # Compute final MLU (same formula as env)
    if link_load:
        final_mlu = max(link_load.values()) / capacity
    else:
        final_mlu = 0.0

    # Delay stats (ms)
    delays_ms = [d * 1000.0 for d in flow_delays]
    avg_delay_ms = float(np.mean(delays_ms)) if delays_ms else 0.0
    max_delay_ms = float(np.max(delays_ms)) if delays_ms else 0.0

    stats = {
        "n_paths_min": min(n_paths_per_flow) if n_paths_per_flow else 0,
        "n_paths_mean": float(np.mean(n_paths_per_flow)) if n_paths_per_flow else 0.0,
        "n_paths_max": max(n_paths_per_flow) if n_paths_per_flow else 0,
        "n_flows": len(flows),
        "avg_delay_ms": avg_delay_ms,
        "max_delay_ms": max_delay_ms,
    }

    return final_mlu, stats, dict(link_load)


def run_ecmp(
    env: RoutingEnv,
    n_eval: int = 50,
    seed_offset: int = 200000,
) -> dict[str, float]:
    """Evaluate true ECMP routing baseline.

    For each flow: enumerate ALL shortest paths (by hop count) on the routing
    graph, then round-robin traffic among them. This gives true equal-cost
    multi-path, not limited to K=4 candidates.

    Returns:
        Aggregated metrics dict with mean/std for mlu, cv, overflow_ratio,
        plus backward-compatible 'mean' and 'std' for MLU.
    """
    episode_metrics: list[dict] = []

    for i in range(n_eval):
        final_mlu, stats, link_load = _route_episode_ecmp(env, seed=seed_offset + i)
        ep_m = compute_episode_metrics(
            link_load, env._capacity, env._E, final_mlu,
            avg_delay_ms=stats["avg_delay_ms"],
            max_delay_ms=stats["max_delay_ms"],
        )
        episode_metrics.append(ep_m)

    result = aggregate_metrics(episode_metrics)
    mlus = [m["mlu"] for m in episode_metrics]
    result["mean"] = result["mlu_mean"]
    result["std"] = result["mlu_std"]
    result["mlus"] = mlus
    return result


if __name__ == "__main__":
    config = SimConfig()
    env = RoutingEnv(config)

    # Quick analysis: equal-cost path counts on default topology
    print("=" * 60)
    print("True ECMP Analysis: Equal-cost shortest path enumeration")
    print("=" * 60)

    # Run one episode to get stats
    final_mlu, stats, _link_load = _route_episode_ecmp(env, seed=200000)
    print(f"\nSample episode (seed=200000):")
    print(f"  Flows: {stats['n_flows']}")
    print(f"  Equal-cost paths per flow: min={stats['n_paths_min']}, "
          f"mean={stats['n_paths_mean']:.1f}, max={stats['n_paths_max']}")
    print(f"  Final MLU: {final_mlu:.4f}")

    # Detailed distribution across multiple episodes
    print(f"\nAggregating over 50 episodes...")
    n_paths_all: list[int] = []
    mlus: list[float] = []
    for i in range(50):
        mlu, st, _ = _route_episode_ecmp(env, seed=200000 + i)
        mlus.append(mlu)
        # Sample a few flows per episode for distribution
        routing_graph = env._routing_graph
        flows = env._flows
        for src, dst, _ in flows[:5]:
            paths = _all_shortest_paths_bfs(routing_graph, src, dst)
            n_paths_all.append(len(paths))

    arr = np.array(n_paths_all)
    print(f"\nEqual-cost path distribution (sampled {len(n_paths_all)} flow pairs):")
    print(f"  Min: {arr.min()}, Max: {arr.max()}, "
          f"Mean: {arr.mean():.1f}, Median: {float(np.median(arr)):.0f}")
    unique, counts = np.unique(arr, return_counts=True)
    print(f"  Distribution:")
    for u, c in zip(unique, counts):
        pct = 100.0 * c / len(arr)
        print(f"    {u} paths: {c} times ({pct:.1f}%)")

    # Full evaluation
    print(f"\nRunning full ECMP evaluation (50 episodes)...")
    result = run_ecmp(env)
    print(f"\nTrue ECMP: MLU = {result['mean']:.4f} +/- {result['std']:.4f}")

    # Compare with K=4 limit info
    k4_count = sum(1 for n in n_paths_all if n <= 4)
    print(f"\nK=4 coverage: {k4_count}/{len(n_paths_all)} flows "
          f"({100.0 * k4_count / len(n_paths_all):.1f}%) would have all paths captured")
