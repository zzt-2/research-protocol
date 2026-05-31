"""Diagnostic: Can single-satellite ISL swaps improve M1 over the prior?

For each trial:
1. Run prior policy for full episode → baseline M1
2. Rerun same episode, but swap ONE satellite's ISL at ONE step
3. Compare M1

If any swap improves M1 → learning signal exists, method just needs to find it.
If no swap improves M1 → prior is near-optimal, no method can beat it.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import numpy as np
from collections import defaultdict

from simulator.environment import ISLEnvironment
from simulator.model_gat import GATv2ActorCritic
from simulator.train import obs_to_data
from simulator import config

import torch


def prior_policy(model, obs, device):
    """Deterministic prior policy: model scores without noise."""
    data = obs_to_data(obs).to(device)
    with torch.no_grad():
        scores, _ = model(data)
    return scores.cpu().numpy()


def apply_single_swap(scores, candidate_edges, sat_id, slot_idx, new_edge_idx, isl_state):
    """Swap one satellite's ISL: drop current active edge, select new one.

    Returns modified scores array.
    """
    scores = scores.copy()

    # Group edges by satellite
    sat_edges = defaultdict(list)
    for idx, (i, j, _) in enumerate(candidate_edges):
        sat_edges[i].append(idx)
        sat_edges[j].append(idx)

    if sat_id not in sat_edges:
        return scores

    # Find active edges for this satellite
    active_indices = []
    inactive_indices = []
    for idx in sat_edges[sat_id]:
        i, j, _ = candidate_edges[idx]
        key = (min(i, j), max(i, j))
        if isl_state.get(key, "inactive") == "active":
            active_indices.append(idx)
        else:
            inactive_indices.append(idx)

    if not active_indices or not inactive_indices:
        return scores

    # Drop the specified active edge (by slot index)
    drop_idx = active_indices[slot_idx % len(active_indices)]
    # Select the new edge
    add_idx = inactive_indices[new_edge_idx % len(inactive_indices)]

    scores[drop_idx] = 0.0
    scores[add_idx] = 1.0

    return scores


def run_swap_diagnostic(
    n_planes=24,
    sats_per_plane=20,
    n_trials=100,
    swap_step=5,
    seed=42,
):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    env = ISLEnvironment(n_planes=n_planes, sats_per_plane=sats_per_plane, seed=seed)
    model = GATv2ActorCritic().to(device)
    print(f"N_sats={env.n_sats}")

    # Baseline: full episode with prior
    def run_baseline(seed_val):
        env2 = ISLEnvironment(n_planes=n_planes, sats_per_plane=sats_per_plane, seed=seed_val)
        metrics, reward = env2.run_episode(
            lambda obs: prior_policy(model, obs, device)
        )
        return metrics, reward

    base_m, base_r = run_baseline(seed)
    print(f"\n[Baseline] M1={base_m['M1_throughput']:.4f} reward={base_r:.3f}")

    # Now try swaps
    rng = np.random.default_rng(seed + 100)
    improvements = 0
    degradations = 0
    neutral = 0
    best_delta = 0.0
    best_trial = -1
    deltas = []

    for trial in range(n_trials):
        trial_seed = seed + trial + 1000

        # Create two envs with same seed for fair comparison
        env_base = ISLEnvironment(n_planes=n_planes, sats_per_plane=sats_per_plane, seed=trial_seed)
        env_swap = ISLEnvironment(n_planes=n_planes, sats_per_plane=sats_per_plane, seed=trial_seed)

        # --- Run baseline episode ---
        obs_b, _ = env_base.reset(seed=trial_seed)
        base_trajectory = []  # (obs, scores, info)

        for step in range(env_base.episode_steps):
            scores = prior_policy(model, obs_b, device)
            obs_b, r, done, _, info = env_base.step(scores)
            base_trajectory.append((scores, info))
            if done:
                break

        base_metrics = env_base.metrics.compute()
        base_m1 = base_metrics["M1_throughput"]

        # --- Run swapped episode ---
        # Pick random satellite, slot, and swap target
        swap_sat = int(rng.integers(0, env_swap.n_sats))
        swap_slot = int(rng.integers(0, config.N_LCT))

        obs_s, _ = env_swap.reset(seed=trial_seed)

        for step in range(env_swap.episode_steps):
            scores = prior_policy(model, obs_s, device)

            # Apply swap at the designated step
            if step == swap_step:
                # Get number of inactive candidates for this sat
                sat_inactive = []
                for idx, (i, j, _) in enumerate(obs_s["candidate_edges"]):
                    key = (min(i, j), max(i, j))
                    state = env_swap._isl_state.get(key, "inactive")
                    if (i == swap_sat or j == swap_sat) and state != "active":
                        sat_inactive.append(idx)

                if sat_inactive:
                    new_edge = int(rng.choice(sat_inactive))
                    scores = apply_single_swap(
                        scores,
                        obs_s["candidate_edges"],
                        swap_sat,
                        swap_slot,
                        new_edge,
                        env_swap._isl_state,
                    )

            obs_s, r, done, _, info = env_swap.step(scores)
            if done:
                break

        swap_metrics = env_swap.metrics.compute()
        swap_m1 = swap_metrics["M1_throughput"]
        delta = swap_m1 - base_m1
        deltas.append(delta)

        if delta > 0.001:
            improvements += 1
            if delta > best_delta:
                best_delta = delta
                best_trial = trial
        elif delta < -0.001:
            degradations += 1
        else:
            neutral += 1

        if (trial + 1) % 20 == 0:
            print(f"  Trial {trial+1}/{n_trials}: "
                  f"improved={improvements} degraded={degradations} neutral={neutral} "
                  f"best_delta={best_delta:+.4f}")

    print(f"\n=== Results ({n_trials} trials) ===")
    print(f"Improved:   {improvements} ({improvements/n_trials*100:.0f}%)")
    print(f"Degraded:   {degradations} ({degradations/n_trials*100:.0f}%)")
    print(f"Neutral:    {neutral} ({neutral/n_trials*100:.0f}%)")
    print(f"Best delta: {best_delta:+.4f}")
    print(f"Mean delta: {np.mean(deltas):+.4f}")
    print(f"Std delta:  {np.std(deltas):.4f}")

    if improvements > 0:
        print(f"\nSignal EXISTS: {improvements}/{n_trials} swaps improved M1.")
        print(f"Best improvement: {best_delta:+.4f} (trial {best_trial})")
    else:
        print(f"\nNO SIGNAL: no single-satellite swap improved M1.")
        print("Prior may be near-optimal for this topology.")


if __name__ == "__main__":
    run_swap_diagnostic()
