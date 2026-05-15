"""B4 Baseline: Random satellite selection policy.

Each UE independently picks a random visible satellite at every decision step.
Serves as the lower-bound baseline for LEO handover performance comparison.
"""

import json
import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from simulator.environment import LEOSatHandoverEnv
import config as cfg

SEEDS = [42, 43, 44, 45, 46]


def select_random(valid_mask: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Each UE picks a random visible satellite."""
    num_ues = valid_mask.shape[0]
    actions = np.zeros(num_ues, dtype=int)
    for ue in range(num_ues):
        visible = np.where(valid_mask[ue])[0]
        actions[ue] = rng.choice(visible) if len(visible) > 0 else 0
    return actions


def run_episode(seed: int) -> dict:
    """Run one full episode with random policy. Returns aggregated metrics."""
    env = LEOSatHandoverEnv(num_ues=cfg.NUM_UES, seed=seed)
    rng = np.random.default_rng(seed)
    obs = env.reset(seed=seed)

    total_throughputs = []
    blocking_rates = []
    handover_count = 0
    done = False

    while not done:
        valid_mask = env.get_valid_actions()
        actions = select_random(valid_mask, rng)
        obs, _rewards, done, info = env.step(actions)

        total_throughputs.append(float(info["total_throughput_bps"]))
        blocking_rates.append(float(info["blocking_rate"]))
        handover_count += int(info["handover_count"])

    return {
        "seed": seed,
        "mean_throughput_mbps": float(np.mean(total_throughputs)) / 1e6,
        "mean_blocking_rate": float(np.mean(blocking_rates)),
        "total_handover_count": handover_count,
    }


def main():
    print("=" * 60)
    print("B4 Random Policy Baseline")
    print("=" * 60)

    seed_results = []
    for seed in SEEDS:
        metrics = run_episode(seed)
        seed_results.append(metrics)
        print(
            f"  seed={seed:3d} | "
            f"avg_tput={metrics['mean_throughput_mbps']:8.2f} Mbps | "
            f"avg_blk={metrics['mean_blocking_rate']:.4f} | "
            f"HO_count={metrics['total_handover_count']:5d}"
        )

    throughputs = [r["mean_throughput_mbps"] for r in seed_results]
    blockings = [r["mean_blocking_rate"] for r in seed_results]
    handovers = [r["total_handover_count"] for r in seed_results]

    summary = {
        "seeds": seed_results,
        "summary": {
            "mean_throughput_mbps": float(np.mean(throughputs)),
            "std_throughput_mbps": float(np.std(throughputs)),
            "mean_blocking_rate": float(np.mean(blockings)),
            "std_blocking_rate": float(np.std(blockings)),
            "mean_handover_count": float(np.mean(handovers)),
            "std_handover_count": float(np.std(handovers)),
        },
    }

    s = summary["summary"]
    print(f"\n  Summary ({len(SEEDS)} seeds):")
    print(f"    Throughput : {s['mean_throughput_mbps']:.2f} +/- {s['std_throughput_mbps']:.2f} Mbps")
    print(f"    Blocking   : {s['mean_blocking_rate']:.4f} +/- {s['std_blocking_rate']:.4f}")
    print(f"    Handovers  : {s['mean_handover_count']:.1f} +/- {s['std_handover_count']:.1f}")

    results_dir = PROJECT_ROOT / "results"
    results_dir.mkdir(exist_ok=True)
    out_path = results_dir / "b4_random_results.json"
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
