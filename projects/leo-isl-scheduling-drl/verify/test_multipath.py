"""Quick test: single-path vs multi-path routing on B1 baseline.

Tests at two scales:
  1. Small (24×8=192): fast sanity check
  2. Full (24×66=1584): real comparison
"""

import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from baselines.grid_fixed import GridFixedBaseline


def test_scale(n_planes, spp, label, episode_steps=20, k_paths=4):
    n_sats = n_planes * spp
    print(f"\n{'='*60}")
    print(f"  {label}: {n_planes}×{spp}={n_sats} sats, {episode_steps} steps")
    print(f"{'='*60}")

    results = {}
    for mode, mp in [("single-path", False), (f"k={k_paths} multi-path", True)]:
        print(f"\n  --- {mode} ---")
        b = GridFixedBaseline(
            n_planes=n_planes, sats_per_plane=spp,
            episode_steps=episode_steps, seed=42,
            multipath=mp, k_paths=k_paths,
        )

        t0 = time.time()
        m, total_r = b.run_episode(verbose=True)
        elapsed = time.time() - t0

        delivered = m.get('total_delivered', 0)
        demanded = m.get('total_demanded', 0)
        tput = delivered / demanded if demanded > 0 else 0
        blocking = 1 - tput

        print(f"  Result: tput={tput:.4f} blocking={blocking:.4f} "
              f"delivered={delivered:.1f} demanded={demanded:.1f} "
              f"time={elapsed:.1f}s")
        results[mode] = {
            'tput': tput, 'blocking': blocking,
            'delivered': delivered, 'demanded': demanded,
            'time': elapsed,
        }

    # Compare
    sp = results["single-path"]
    mp_key = f"k={k_paths} multi-path"
    mp = results[mp_key]
    improvement = (mp['tput'] - sp['tput']) / sp['tput'] * 100 if sp['tput'] > 0 else 0
    print(f"\n  >>> Improvement: {improvement:+.1f}% "
          f"({sp['tput']:.4f} -> {mp['tput']:.4f})")
    return results


if __name__ == "__main__":
    # Quick sanity check at small scale
    test_scale(24, 8, "Small scale", episode_steps=10, k_paths=4)

    # Full scale comparison — uses k=3 for speed
    test_scale(24, 66, "Full scale (Starlink Phase I)", episode_steps=20, k_paths=3)
