"""run_mve.py - Execute MVE: HGAT vs GraphSAGE across 5 seeds."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import torch
from env import SatelliteDAGEnv
from models import HGATEncoder, GraphSAGEEncoder, ActorCritic
from train import train

SEEDS = [42, 123, 456, 789, 1024]
N_EPISODES = 500
EVAL_LAST = 50  # average over last N episodes


def run_encoder(name, EncoderCls, build_attr, seeds=SEEDS):
    results = {}
    for seed in seeds:
        torch.manual_seed(seed)
        np.random.seed(seed)
        env = SatelliteDAGEnv(seed=seed)
        encoder = EncoderCls()
        model = ActorCritic(encoder, n_actions=5)
        build_fn = getattr(env, build_attr)
        costs = train(env, model, build_fn, n_episodes=N_EPISODES, seed=seed)
        final_avg = np.mean(costs[-EVAL_LAST:])
        results[seed] = {"final_avg": final_avg, "costs": costs}
        n_params = sum(p.numel() for p in model.parameters())
        print(f"  [{name}] seed={seed}: final_avg_cost={final_avg:.4f}, params={n_params}")
    return results


def main():
    print("=" * 60)
    print("MVE: HGAT vs GraphSAGE for Satellite Edge DAG Offloading")
    print("=" * 60)

    print("\n--- HGAT Encoder ---")
    hgat_results = run_encoder("HGAT", HGATEncoder, "build_hetero")

    print("\n--- GraphSAGE Encoder ---")
    sage_results = run_encoder("GraphSAGE", GraphSAGEEncoder, "build_homo")

    # Compare
    print("\n" + "=" * 60)
    print("COMPARISON (lower cost = better)")
    print("-" * 60)
    print(f"{'Seed':<8} {'HGAT':<12} {'GraphSAGE':<12} {'Improvement':<12}")
    print("-" * 60)

    improvements = []
    for seed in SEEDS:
        h = hgat_results[seed]["final_avg"]
        s = sage_results[seed]["final_avg"]
        imp = (s - h) / s * 100  # positive = HGAT better
        improvements.append(imp)
        print(f"{seed:<8} {h:<12.4f} {s:<12.4f} {imp:>+8.2f}%")

    n_better = sum(1 for imp in improvements if imp > 0)
    n_sig_better = sum(1 for imp in improvements if imp >= 5.0)
    avg_imp = np.mean(improvements)

    print("-" * 60)
    print(f"Avg improvement: {avg_imp:+.2f}%")
    print(f"HGAT better in {n_better}/5 seeds, >=5% in {n_sig_better}/5 seeds")

    # Verdict
    if n_sig_better >= 3:
        verdict = "PASS"
    elif n_better >= 2 and avg_imp >= 3.0:
        verdict = "MARGINAL"
    else:
        verdict = "FAIL"

    print(f"\nVERDICT: {verdict}")
    print("=" * 60)

    # Save results
    import json
    out = {
        "verdict": verdict,
        "hgat": {str(k): v["final_avg"] for k, v in hgat_results.items()},
        "graphSAGE": {str(k): v["final_avg"] for k, v in sage_results.items()},
        "improvements": improvements,
        "avg_improvement": avg_imp,
    }
    with open(os.path.join(os.path.dirname(__file__), "mve_results.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"Results saved to mve/mve_results.json")


if __name__ == "__main__":
    main()
