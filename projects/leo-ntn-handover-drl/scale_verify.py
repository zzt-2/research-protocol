"""Phase 1: Verify simulator behavior at different UE scales.

Collects baseline statistics for 20/50/100 UE with different sat_capacity values.
Uses random policy (pick random visible satellite) to measure natural load competition.
"""

import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from simulator.environment import LEOSatHandoverEnv


def run_random_episode(env, seed):
    obs = env.reset(seed=seed)
    total_blk = 0.0
    total_ho = 0
    steps = 0
    vis_counts = []
    max_loads_per_step = []
    done = False

    while not done:
        # Count visible sats per UE from obs
        N = env.num_sats
        for u in range(env.num_ues):
            elev = obs[u, N:2*N]
            vis_counts.append(int((elev > 0).sum()))

        # Random action: pick random visible sat per UE
        actions = np.zeros(env.num_ues, dtype=int)
        sat_pos = env.constellation.get_positions(env._step)
        from simulator.orbit import compute_visibility
        for u in range(env.num_ues):
            vis = compute_visibility(sat_pos, env.ue_positions[u], env.min_elev)
            vis_idx = np.where(vis)[0]
            if len(vis_idx) > 0:
                actions[u] = np.random.choice(vis_idx)
            else:
                actions[u] = 0  # fallback

        obs, rewards, done, info = env.step(actions)
        total_blk += float(info['blocking_rate'])
        total_ho += int(info['handover_count'])
        steps += 1

        # Track satellite load distribution
        load_per_sat = np.zeros(env.num_sats, dtype=int)
        for u in range(env.num_ues):
            if not (info['throughput_bps'][u] == 0):
                load_per_sat[actions[u]] += 1
        active = load_per_sat[load_per_sat > 0]
        if len(active) > 0:
            max_loads_per_step.append(int(active.max()))

    return {
        'blocking_rate': total_blk / steps,
        'handovers': total_ho,
        'steps': steps,
        'vis_mean': np.mean(vis_counts),
        'vis_max': np.max(vis_counts),
        'vis_min': np.min(vis_counts),
        'vis_std': np.std(vis_counts),
        'max_load_mean': np.mean(max_loads_per_step) if max_loads_per_step else 0,
        'max_load_max': np.max(max_loads_per_step) if max_loads_per_step else 0,
    }


def main():
    print("=" * 70)
    print("Phase 1: Simulator Scale Verification")
    print("=" * 70)

    configs = [
        (20, 10), (20, 5), (20, 3),
        (50, 10), (50, 5), (50, 3),
        (100, 10), (100, 5), (100, 3),
    ]

    results = {}
    for num_ues, sat_cap in configs:
        key = f"UE{num_ues}_cap{sat_cap}"
        print(f"\n--- {key} ---")
        env = LEOSatHandoverEnv(num_ues=num_ues, sat_capacity=sat_cap)
        print(f"  Sats: {env.num_sats}, Steps: {env.num_steps}, Obs dim: {env.obs_dim}")

        eps = []
        for seed in range(10):
            r = run_random_episode(env, seed=seed + 100)
            eps.append(r)

        # Aggregate
        agg = {k: np.mean([e[k] for e in eps]) for k in eps[0]}
        agg_std = {k: np.std([e[k] for e in eps]) for k in eps[0]}
        results[key] = {'mean': agg, 'std': agg_std, 'raw': eps}

        print(f"  Blocking: {agg['blocking_rate']:.4f} ± {agg_std['blocking_rate']:.4f}")
        print(f"  Visible sats: {agg['vis_mean']:.1f} ± {agg['vis_std']:.1f} "
              f"(max={agg['vis_max']:.0f}, min={agg['vis_min']:.0f})")
        print(f"  Max sat load: {agg['max_load_mean']:.1f} (peak={agg['max_load_max']:.0f})")
        print(f"  Handovers: {agg['handovers']:.0f}")

    # Summary table
    print(f"\n{'=' * 70}")
    print("Summary: Blocking Rate by (UE, capacity)")
    print(f"{'=' * 70}")
    print(f"{'Config':<20} {'Blocking':>10} {'Vis Mean':>10} {'Max Load':>10}")
    print("-" * 50)
    for key in results:
        m = results[key]['mean']
        print(f"{key:<20} {m['blocking_rate']:>10.4f} {m['vis_mean']:>10.1f} {m['max_load_mean']:>10.1f}")

    # Save
    import json
    out = PROJECT_ROOT / 'results' / 'phase1_scale_verify.json'
    out.parent.mkdir(exist_ok=True)
    serializable = {}
    for k, v in results.items():
        serializable[k] = {
            'mean': {kk: float(vv) for kk, vv in v['mean'].items()},
            'std': {kk: float(vv) for kk, vv in v['std'].items()},
        }
    with open(out, 'w') as f:
        json.dump(serializable, f, indent=2)
    print(f"\nSaved to {out}")


if __name__ == '__main__':
    main()
