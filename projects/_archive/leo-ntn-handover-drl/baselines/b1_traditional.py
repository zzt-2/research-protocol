"""B1 Baseline: Traditional A3 / MVT handover rules for LEO satellite handover.

Implements two classic handover strategies:
- MVT (Maximum Visible Time): select the satellite with the highest rate
  (proxy for highest elevation / longest remaining visibility).
- A3 event (3GPP): hand over only when a neighbor satellite's signal exceeds
  the serving satellite's signal by an offset threshold.

Runs both strategies across multiple seeds and collects performance metrics.
"""

import json
import sys
from pathlib import Path

import numpy as np

# Ensure project root is importable
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from simulator.env import LEOSatHandoverEnv

SEEDS = [42, 43, 44, 45, 46]
A3_OFFSET = 0.0  # dB-equivalent offset in rate domain (0 = always hand over to better sat)


# ---------------------------------------------------------------------------
# Strategy implementations
# ---------------------------------------------------------------------------

def select_mvt(obs: dict, num_sats: int) -> np.ndarray:
    """MVT: each UE picks the visible satellite with the highest achievable rate."""
    actions = np.zeros(len(obs), dtype=int)
    for ue, o in obs.items():
        visible = o["visible_mask"]
        if visible.any():
            rates = o["rates"].copy()
            rates[~visible] = -np.inf
            actions[ue] = int(rates.argmax())
        else:
            # No visible satellite -- pick index 0 as fallback (will be blocked)
            actions[ue] = 0
    return actions


def select_a3(obs: dict, prev_sats: np.ndarray, num_sats: int,
              offset: float = A3_OFFSET) -> np.ndarray:
    """A3 event: hand over when a neighbor's rate > serving rate + offset.

    On the first step (prev_sat == -1), falls back to MVT selection.
    """
    actions = np.zeros(len(obs), dtype=int)
    for ue, o in obs.items():
        visible = o["visible_mask"]
        if not visible.any():
            actions[ue] = 0
            continue

        rates = o["rates"].copy()
        rates[~visible] = -np.inf

        prev = prev_sats[ue]
        if prev < 0:
            # No serving satellite yet -- pick best visible (MVT)
            actions[ue] = int(rates.argmax())
        else:
            current_rate = rates[prev]
            best_neighbor = int(rates.argmax())
            best_rate = rates[best_neighbor]
            if best_rate > current_rate + offset:
                actions[ue] = best_neighbor
            else:
                actions[ue] = prev
    return actions


# ---------------------------------------------------------------------------
# Episode runner
# ---------------------------------------------------------------------------

def run_episode(env: LEOSatHandoverEnv, seed: int, strategy: str) -> dict:
    """Run one full episode and return aggregated metrics."""
    obs = env.reset(seed=seed)
    prev_sats = np.full(env.num_ues, -1, dtype=int)

    total_throughputs = []
    blocking_rates = []
    handover_count = 0

    done = False
    while not done:
        if strategy == "mvt":
            actions = select_mvt(obs, env.num_sats)
        elif strategy == "a3":
            actions = select_a3(obs, prev_sats, env.num_sats)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

        obs, _rewards, done, info = env.step(actions)
        prev_sats = actions.copy()

        total_throughputs.append(float(info["total_throughput"]))
        blocking_rates.append(float(info["blocking_rate"]))
        handover_count += int(info["handover_count"])

    return {
        "seed": seed,
        "mean_throughput": float(np.mean(total_throughputs)),
        "mean_blocking_rate": float(np.mean(blocking_rates)),
        "total_handover_count": handover_count,
    }


# ---------------------------------------------------------------------------
# Main: run all seeds, collect and save results
# ---------------------------------------------------------------------------

def main():
    results = {}

    for strategy in ["mvt", "a3"]:
        print(f"\n{'='*60}")
        print(f"Strategy: {strategy.upper()}")
        print(f"{'='*60}")

        seed_results = []
        for seed in SEEDS:
            env = LEOSatHandoverEnv(num_ues=20, sat_capacity=5, seed=seed)
            metrics = run_episode(env, seed, strategy)
            seed_results.append(metrics)
            print(
                f"  seed={seed:3d} | "
                f"avg_tput={metrics['mean_throughput']:12.2f} | "
                f"avg_blk={metrics['mean_blocking_rate']:.4f} | "
                f"HO_count={metrics['total_handover_count']:5d}"
            )

        throughputs = [r["mean_throughput"] for r in seed_results]
        blockings = [r["mean_blocking_rate"] for r in seed_results]
        handovers = [r["total_handover_count"] for r in seed_results]

        summary = {
            "strategy": strategy,
            "seeds": seed_results,
            "summary": {
                "mean_throughput": float(np.mean(throughputs)),
                "std_throughput": float(np.std(throughputs)),
                "mean_blocking_rate": float(np.mean(blockings)),
                "std_blocking_rate": float(np.std(blockings)),
                "mean_handover_count": float(np.mean(handovers)),
                "std_handover_count": float(np.std(handovers)),
            },
        }
        results[strategy] = summary

        s = summary["summary"]
        print(f"\n  Summary ({len(SEEDS)} seeds):")
        print(f"    Throughput : {s['mean_throughput']:.2f} +/- {s['std_throughput']:.2f}")
        print(f"    Blocking   : {s['mean_blocking_rate']:.4f} +/- {s['std_blocking_rate']:.4f}")
        print(f"    Handovers  : {s['mean_handover_count']:.1f} +/- {s['std_handover_count']:.1f}")

    # Save results
    results_dir = PROJECT_ROOT / "results"
    results_dir.mkdir(exist_ok=True)
    out_path = results_dir / "b1_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
