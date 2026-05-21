#!/usr/bin/env python3
"""Complexity benchmark: parameter count, inference latency, theoretical O().

Measures GNN, MLP, and ECMP across multiple constellation scales.
Supports the "Online Fault-Resilient Per-Flow Routing" positioning by
quantifying that GNN routing is fast enough for online deployment.
"""

import json
import sys
import time
from collections import defaultdict, deque
from pathlib import Path

import numpy as np
import torch

_PROJECT = Path(__file__).resolve().parent.parent
if str(_PROJECT) not in sys.path:
    sys.path.insert(0, str(_PROJECT))

from simulator.config import SimConfig
from simulator.env import RoutingEnv
from simulator.model import RoutingActorCritic
from baselines.mlp import MLPActorCritic
from baselines.ecmp import _all_shortest_paths_bfs


def count_params(model: torch.nn.Module) -> dict:
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    return {"total": total, "trainable": trainable}


def bench_gnn_latency(model: torch.nn.Module, env: RoutingEnv,
                      n_warmup: int = 50, n_iters: int = 1000) -> dict:
    """Benchmark GNN inference: encode obs + select action."""
    obs, _ = env.reset(seed=42)

    # Warmup
    for _ in range(n_warmup):
        model.get_action(obs, deterministic=True)

    # Measure
    times = []
    for _ in range(n_iters):
        env.reset(seed=np.random.randint(0, 2**31))
        obs, _ = env.reset(seed=np.random.randint(0, 2**31))
        torch.cuda.synchronize() if torch.cuda.is_available() else None
        t0 = time.perf_counter()
        model.get_action(obs, deterministic=True)
        times.append(time.perf_counter() - t0)

    arr = np.array(times)
    return {
        "mean_ms": float(arr.mean() * 1000),
        "std_ms": float(arr.std() * 1000),
        "median_ms": float(np.median(arr) * 1000),
        "p95_ms": float(np.percentile(arr, 95) * 1000),
        "n_iters": n_iters,
    }


def bench_mlp_latency(model: torch.nn.Module, env: RoutingEnv,
                      n_warmup: int = 50, n_iters: int = 1000) -> dict:
    """Benchmark MLP inference."""
    obs, _ = env.reset(seed=42)
    sample_obs = env.reset(seed=0)[0]

    for _ in range(n_warmup):
        model.get_action(sample_obs, deterministic=True)

    times = []
    for _ in range(n_iters):
        obs, _ = env.reset(seed=np.random.randint(0, 2**31))
        t0 = time.perf_counter()
        model.get_action(obs, deterministic=True)
        times.append(time.perf_counter() - t0)

    arr = np.array(times)
    return {
        "mean_ms": float(arr.mean() * 1000),
        "std_ms": float(arr.std() * 1000),
        "median_ms": float(np.median(arr) * 1000),
        "p95_ms": float(np.percentile(arr, 95) * 1000),
        "n_iters": n_iters,
    }


def bench_ecmp_latency(env: RoutingEnv, n_iters: int = 200) -> dict:
    """Benchmark ECMP: BFS all-shortest-paths for all flows in one episode."""
    times = []
    n_paths_list = []

    for i in range(n_iters):
        env.reset(seed=100000 + i)
        graph = env._routing_graph
        flows = env._flows

        t0 = time.perf_counter()
        for src, dst, _ in flows:
            paths = _all_shortest_paths_bfs(graph, src, dst)
            n_paths_list.append(len(paths))
        times.append(time.perf_counter() - t0)

    arr = np.array(times)
    n_flows = len(env._flows)
    return {
        "total_ms": float(arr.mean() * 1000),
        "per_flow_ms": float(arr.mean() * 1000 / n_flows),
        "std_ms": float(arr.std() * 1000),
        "median_ms": float(np.median(arr) * 1000),
        "n_iters": n_iters,
        "n_flows": n_flows,
        "n_paths_mean": float(np.mean(n_paths_list)),
        "n_paths_max": int(np.max(n_paths_list)),
    }


def bench_fault_response(env: RoutingEnv, gnn_model: torch.nn.Module,
                         n_iters: int = 100) -> dict:
    """Benchmark fault response: ECMP recompute vs GNN forward pass.

    Simulates a topology change (link failure) and measures:
    - ECMP: time to recompute all shortest paths on new topology
    - GNN: time for one forward pass (same as normal routing, fault-aware by design)
    """
    ecmp_times = []
    gnn_times = []

    for i in range(n_iters):
        obs, _ = env.reset(seed=200000 + i)

        # ECMP: recompute all paths on current (faulty) topology
        graph = env._routing_graph
        flows = env._flows
        t0 = time.perf_counter()
        for src, dst, _ in flows:
            _all_shortest_paths_bfs(graph, src, dst)
        ecmp_times.append(time.perf_counter() - t0)

        # GNN: one forward pass (fault info already in edge features)
        torch.cuda.synchronize() if torch.cuda.is_available() else None
        t0 = time.perf_counter()
        gnn_model.get_action(obs, deterministic=True)
        gnn_times.append(time.perf_counter() - t0)

    ecmp_arr = np.array(ecmp_times)
    gnn_arr = np.array(gnn_times)
    return {
        "ecmp_recompute_ms": float(ecmp_arr.mean() * 1000),
        "ecmp_per_flow_ms": float(ecmp_arr.mean() * 1000 / len(flows)),
        "gnn_forward_ms": float(gnn_arr.mean() * 1000),
        "speedup": float(ecmp_arr.mean() / gnn_arr.mean()) if gnn_arr.mean() > 0 else float("inf"),
        "n_iters": n_iters,
    }


def theoretical_complexity(config: SimConfig) -> dict:
    """Document theoretical complexity for each method."""
    N = config.n_nodes
    E = N * 4  # Walker delta 4-regular, undirected edges = 2*4*N/2 = 4N
    d = config.hidden_dim
    H = config.n_heads
    L = config.n_layers
    K = config.k_paths
    F = config.n_flows

    return {
        "ECMP": {
            "per_query": f"O(E + N) BFS = O({E} + {N})",
            "all_flows": f"O(F * (E + N)) = O({F} * {E + N})",
            "note": "Must recompute on topology change",
        },
        "GNN": {
            "encoding": f"O(L * (E*d^2 + N*d)) = O({L} * ({E}*{d}^2 + {N}*{d}))",
            "scoring": f"O(K * path_len * d) per flow",
            "per_flow": f"GNN encode once + O(K*d) scoring",
            "all_flows": f"O(L*E*d^2 + F*K*d) = encode once, score {F} flows",
            "note": "Encode once per topology snapshot, score each flow independently",
        },
        "MLP": {
            "per_flow": f"O(d^2) = O({d}^2) for 2-layer MLP",
            "all_flows": f"O(F * d^2) = O({F} * {d}^2)",
            "note": "No graph encoding, local features only",
        },
        "params": {
            "N": N, "E": E, "d": d, "H": H, "L": L, "K": K, "F": F,
        },
    }


def run_benchmark() -> dict:
    """Run full complexity benchmark across multiple scales."""
    scales = [
        {"name": "48 nodes (0.7x)", "planes": 4, "sats": 12},
        {"name": "66 nodes (1x, train)", "planes": 6, "sats": 11},
        {"name": "288 nodes (4.4x)", "planes": 12, "sats": 24},
    ]

    results = {}
    # CPU for fair comparison (ECMP is pure CPU; same device = apples-to-apples)
    device = "cpu"
    print(f"Device: {device}")

    for scale in scales:
        name = scale["name"]
        print(f"\n{'='*60}")
        print(f"Benchmarking: {name}")
        print(f"{'='*60}")

        config = SimConfig(n_planes=scale["planes"], sats_per_plane=scale["sats"])
        env = RoutingEnv(config)
        obs, _ = env.reset(seed=42)

        # --- Parameter counts ---
        gnn = RoutingActorCritic(
            node_dim=config.node_feat_dim,
            edge_dim=config.edge_feat_dim,
            hidden_dim=config.hidden_dim,
            n_layers=config.n_layers,
            n_heads=config.n_heads,
            k_paths=config.k_paths,
        ).to(device)

        mlp_feat_dim = obs["mlp_feat"].shape[0]
        mlp = MLPActorCritic(
            mlp_feat_dim=mlp_feat_dim,
            k_paths=config.k_paths,
            hidden=config.hidden_dim,
        ).to(device)

        gnn_params = count_params(gnn)
        mlp_params = count_params(mlp)

        print(f"  GNN params: {gnn_params['total']:,}")
        print(f"  MLP params: {mlp_params['total']:,}")

        # --- Latency benchmarks ---
        print(f"  Benchmarking GNN latency...")
        gnn_lat = bench_gnn_latency(gnn, env, n_warmup=50, n_iters=500)

        print(f"  Benchmarking MLP latency...")
        mlp_lat = bench_mlp_latency(mlp, env, n_warmup=50, n_iters=500)

        print(f"  Benchmarking ECMP latency...")
        ecmp_lat = bench_ecmp_latency(env, n_iters=200)

        print(f"  Benchmarking fault response...")
        fault_resp = bench_fault_response(env, gnn, n_iters=100)

        # --- Theoretical complexity ---
        theory = theoretical_complexity(config)

        results[name] = {
            "n_nodes": config.n_nodes,
            "n_edges": config.n_nodes * 4,
            "gnn_params": gnn_params,
            "mlp_params": mlp_params,
            "gnn_latency": gnn_lat,
            "mlp_latency": mlp_lat,
            "ecmp_latency": ecmp_lat,
            "fault_response": fault_resp,
            "theoretical": theory,
        }

        print(f"\n  Results for {name}:")
        print(f"    GNN inference: {gnn_lat['median_ms']:.3f} ms (median)")
        print(f"    MLP inference: {mlp_lat['median_ms']:.3f} ms (median)")
        print(f"    ECMP all-flows: {ecmp_lat['total_ms']:.3f} ms")
        print(f"    Fault response: ECMP={fault_resp['ecmp_recompute_ms']:.3f}ms, "
              f"GNN={fault_resp['gnn_forward_ms']:.3f}ms, "
              f"speedup={fault_resp['speedup']:.1f}x")

    # --- Summary ---
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for name, r in results.items():
        print(f"\n{name} ({r['n_nodes']} nodes):")
        print(f"  Params: GNN={r['gnn_params']['total']:,}, MLP={r['mlp_params']['total']:,}")
        print(f"  Latency: GNN={r['gnn_latency']['median_ms']:.3f}ms, "
              f"MLP={r['mlp_latency']['median_ms']:.3f}ms, "
              f"ECMP={r['ecmp_latency']['per_flow_ms']:.3f}ms/flow")

    return results


if __name__ == "__main__":
    results = run_benchmark()

    out_path = Path(__file__).resolve().parent / "results" / "complexity_report.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")
