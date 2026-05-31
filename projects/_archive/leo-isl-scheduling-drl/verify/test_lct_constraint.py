"""Test N_LCT terminal constraint impact on B1 throughput.

Compares: unlimited ISLs / N_LCT=4 / N_LCT=2 at full scale (1584 sats).
Key question: does the terminal constraint create enough room for DRL to improve?
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from baselines.grid_fixed import GridFixedBaseline


def test_lct(n_planes, spp, label, episode_steps=20):
    n_sats = n_planes * spp
    print(f"\n{'='*60}")
    print(f"  {label}: {n_planes}×{spp}={n_sats} sats, {episode_steps} steps")
    print(f"{'='*60}")

    configs = [
        ("unlimited", None),
        ("N_LCT=4", 4),
        ("N_LCT=3", 3),
        ("N_LCT=2", 2),
    ]

    results = {}
    for name, n_lct in configs:
        b = GridFixedBaseline(
            n_planes=n_planes, sats_per_plane=spp,
            episode_steps=episode_steps, seed=42,
            n_lct=n_lct,
        )
        topo = b.topology_summary()
        print(f"\n  --- {name} ---")
        print(f"  Topology: {topo['total_edges']} edges, "
              f"{topo['intra_edges']} intra + {topo['inter_edges']} inter, "
              f"{topo['edges_per_sat']:.1f} edges/sat")

        t0 = time.time()
        m, total_r = b.run_episode(verbose=True)
        elapsed = time.time() - t0

        delivered = m.get('total_delivered', 0)
        demanded = m.get('total_demanded', 0)
        tput = delivered / demanded if demanded > 0 else 0
        blocking = 1 - tput

        print(f"  Result: M1={tput:.4f} M4={blocking:.4f} "
              f"delivered={delivered:.1f} demanded={demanded:.1f} "
              f"M5={m.get('M5_fairness', 0):.4f} "
              f"avg_reward={m.get('avg_reward', 0):.4f} "
              f"time={elapsed:.1f}s")

        results[name] = {
            'tput': tput, 'blocking': blocking, 'time': elapsed,
            'edges': topo['total_edges'],
            'edges_per_sat': topo['edges_per_sat'],
            'M1': tput, 'M4': blocking, 'M5': m.get('M5_fairness', 0),
        }

    # Summary comparison
    print(f"\n{'='*60}")
    print(f"  SUMMARY: N_LCT Constraint Impact")
    print(f"{'='*60}")
    print(f"  {'Config':<12} {'Edges':>6} {'E/Sat':>6} {'M1':>8} {'M4':>8} {'M5':>8} {'Time':>6}")
    for name, r in results.items():
        print(f"  {name:<12} {r['edges']:>6} {r['edges_per_sat']:>6.1f} "
              f"{r['M1']:>8.4f} {r['M4']:>8.4f} {r['M5']:>8.4f} {r['time']:>5.1f}s")

    # DRL opportunity: gap between unlimited and constrained
    if 'unlimited' in results and 'N_LCT=4' in results:
        gap = results['unlimited']['M1'] - results['N_LCT=4']['M1']
        print(f"\n  DRL opportunity (N_LCT=4): {gap:.4f} throughput gap to close")
    if 'unlimited' in results and 'N_LCT=2' in results:
        gap = results['unlimited']['M1'] - results['N_LCT=2']['M1']
        print(f"  DRL opportunity (N_LCT=2): {gap:.4f} throughput gap to close")

    return results


if __name__ == "__main__":
    # Small scale sanity check
    test_lct(24, 8, "Small scale", episode_steps=10)

    # Full scale
    test_lct(24, 66, "Full scale (Starlink Phase I)", episode_steps=20)
