"""Smoke test: verify constellation physics, ISL distances, Dijkstra routing."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
from config import CONFIGS, TRAIN_CONFIGS, TARGET_CONFIG, C_LIGHT, ISL_MAX_DISTANCE
from constellation import WalkerDelta
from topology import build_plus_grid_edges, compute_distances, filter_by_distance, build_adjacency
from channel import isl_capacity, isl_delay_ms
from traffic import generate_traffic, sample_flows
from routing import dijkstra_all_pairs, compute_delay_metrics


def test_config(name, cfg):
    print(f"\n{'='*60}")
    print(f"Config: {name} — P={cfg['P']}, S={cfg['S']}, N={cfg['P']*cfg['S']}")
    print(f"{'='*60}")

    const = WalkerDelta(cfg['P'], cfg['S'], cfg['F'], cfg['alt'], cfg['inc'])
    print(f"  Orbital period: {const.period:.1f}s ({const.period/60:.1f} min)")

    # Positions at t=0
    pos = const.positions(t=0)
    print(f"  Positions shape: {pos.shape}")
    assert pos.shape == (const.N, 3)

    # Verify all at correct altitude
    radii = np.sqrt((pos ** 2).sum(axis=1))
    print(f"  Orbital radius: mean={radii.mean():.1f} km (expected {const.r:.1f})")
    assert np.allclose(radii, const.r, atol=1.0)

    # +Grid topology
    edge_idx = build_plus_grid_edges(cfg['P'], cfg['S'])
    n_edges = edge_idx.shape[1]
    expected_full = cfg['P'] * cfg['S'] * 2  # P*S intra + P*S inter
    print(f"  +Grid edges: {n_edges} (expected {expected_full} before disconnect)")

    # ISL distances
    dists = compute_distances(pos, edge_idx)
    print(f"  ISL distances (km):")
    print(f"    min={dists.min():.0f}, max={dists.max():.0f}, mean={dists.mean():.0f}")

    # Classify intra vs inter-orbit
    p0 = edge_idx[0] // cfg['S']
    p1 = edge_idx[1] // cfg['S']
    intra_mask = p0 == p1
    inter_mask = ~intra_mask
    if intra_mask.any():
        print(f"    Intra-orbit: mean={dists[intra_mask].mean():.0f}, "
              f"min={dists[intra_mask].min():.0f}, max={dists[intra_mask].max():.0f}")
    if inter_mask.any():
        print(f"    Inter-orbit: mean={dists[inter_mask].mean():.0f}, "
              f"min={dists[inter_mask].min():.0f}, max={dists[inter_mask].max():.0f}")

    # Apply disconnect
    filt_idx, filt_dist, keep_mask = filter_by_distance(edge_idx, dists)
    n_disconnected = n_edges - filt_idx.shape[1]
    print(f"  ISL disconnects: {n_disconnected}/{n_edges} "
          f"({100*n_disconnected/n_edges:.1f}% exceed {ISL_MAX_DISTANCE:.0f} km)")

    if n_disconnected > 0:
        disc_dists = dists[~keep_mask]
        print(f"    Disconnected distances: {disc_dists.min():.0f}-{disc_dists.max():.0f} km")

    # Channel
    cap = isl_capacity(filt_dist)
    delay = isl_delay_ms(filt_dist)
    print(f"  ISL capacity: mean={cap.mean()/1e9:.1f} Gbps, min={cap.min()/1e9:.1f} Gbps")
    print(f"  ISL delay: mean={delay.mean():.2f} ms, max={delay.max():.2f} ms")

    # Connectivity check
    adj = build_adjacency(const.N, filt_idx)
    degrees = [len(adj[i]) for i in range(const.N)]
    isolated = sum(1 for d in degrees if d == 0)
    min_deg = min(degrees)
    max_deg = max(degrees)
    print(f"  Node degrees: min={min_deg}, max={max_deg}, isolated={isolated}")
    if isolated > 0:
        print(f"    ⚠️  {isolated} isolated nodes — topology is disconnected!")

    # Traffic + Dijkstra (only if graph is connected enough)
    if isolated == 0:
        rng = np.random.default_rng(42)
        tm = generate_traffic(const.N, 'hotspot', total_demand=100.0, rng=rng)
        flows = sample_flows(tm, 500, rng=rng)

        # Dijkstra with ISL delay as weight
        adj_weighted = build_adjacency(const.N, filt_idx, delay)
        print(f"\n  Running Dijkstra all-pairs (N={const.N})...")
        dist_mat, next_hop = dijkstra_all_pairs(adj_weighted, const.N)
        metrics = compute_delay_metrics(dist_mat, flows)
        print(f"  Dijkstra routing (delay in ms):")
        print(f"    Mean={metrics['mean_delay']:.2f}, P95={metrics['p95_delay']:.2f}, "
              f"Max={metrics['max_delay']:.2f}")
        print(f"    Unreachable flows: {metrics['unreachable']}")
    else:
        print(f"  ⏭ Skipping Dijkstra (disconnected topology)")

    return dict(name=name, N=const.N, n_edges=n_edges, n_disconnected=n_disconnected,
                isolated=isolated, intra_mean=dists[intra_mask].mean() if intra_mask.any() else 0,
                inter_mean=dists[inter_mask].mean() if inter_mask.any() else 0)


def main():
    print("SMOKE TEST: Walker-Delta Constellation + ISL + Dijkstra")
    print("=" * 60)

    results = []
    for name in list(CONFIGS.keys()):
        r = test_config(name, CONFIGS[name])
        results.append(r)

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"{'Config':<16} {'N':>5} {'Edges':>7} {'Disc%':>7} {'Isolated':>9} "
          f"{'Intra(km)':>10} {'Inter(km)':>10}")
    for r in results:
        disc_pct = 100 * r['n_disconnected'] / r['n_edges'] if r['n_edges'] > 0 else 0
        print(f"{r['name']:<16} {r['N']:>5} {r['n_edges']:>7} {disc_pct:>6.1f}% "
              f"{r['isolated']:>9} {r['intra_mean']:>10.0f} {r['inter_mean']:>10.0f}")

    print("\n✅ Smoke test complete.")


if __name__ == '__main__':
    main()
