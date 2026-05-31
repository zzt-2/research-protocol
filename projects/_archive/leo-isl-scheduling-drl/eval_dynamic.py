"""Evaluate GNN vs Grid under link failures.

Compares:
  1. Grid baseline (no failure) — reference ceiling
  2. Grid baseline (with failure) — static topology can't adapt
  3. Phase A GNN (with failure) — LCT auto-fills alternatives
  4. Phase B GNN (with failure) — RL fine-tuned adaptation

Usage:
  python eval_dynamic.py [--failure-prob 0.05] [--seeds 42 100 200] [--quick]
  python eval_dynamic.py --phase-b-ckpt results/phase_b_dynamic/phase_b_best.pt
"""

import argparse
import sys
import os
import time

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from simulator.environment import ISLEnvironment
from simulator.model_gat import GATv2Backbone, SupervisedGNN, DiscreteRLGNN, load_backbone_with_padding
from simulator.discrete_wrapper import DiscreteActionWrapper, obs_to_data
from simulator.generate_dataset import build_grid_topology
from baselines.grid_fixed import GridFixedBaseline
from simulator import config


def run_gnn_episode(env, model, device="cpu", verbose=False, preactivated=False):
    """Run one episode with pretrained GNN policy under failures.

    If preactivated=True, assumes env is already reset and grid edges are active.
    """
    if not preactivated:
        obs, _ = env.reset()
    else:
        obs = env._build_obs()
    model.eval()
    total_reward = 0.0

    for step in range(env.episode_steps):
        data = obs_to_data(obs).to(device)
        with torch.no_grad():
            scores = model.predict_scores(data)
        obs, reward, terminated, truncated, info = env.step(scores)
        total_reward += reward
        if verbose and step % 10 == 0:
            rd = info["reward_dict"]
            print(f"  Step {step}: reward={reward:.4f} R_tput={rd['R_tput']:.3f} "
                  f"n_active={info['n_active']} n_failed={len(env._failed_edges)}")
        if terminated:
            break

    return env.metrics.compute(), total_reward


def run_phase_b_episode(env, model, device="cpu", verbose=False, preactivated=False):
    """Run one episode with Phase B DiscreteRLGNN under failures."""
    if not preactivated:
        obs, _ = env.reset()
    else:
        obs = env._build_obs()
    model.eval()
    wrapper = DiscreteActionWrapper(env, model, device=device)
    total_reward = 0.0

    for step in range(env.episode_steps):
        data = obs_to_data(obs).to(device)
        with torch.no_grad():
            actions, _, _ = model.get_action(data, deterministic=True)
        obs, reward, terminated, truncated, info = wrapper.step(actions.cpu().numpy())
        total_reward += reward
        if verbose and step % 10 == 0:
            rd = info["reward_dict"]
            print(f"  Step {step}: reward={reward:.4f} R_tput={rd['R_tput']:.3f} "
                  f"n_active={info['n_active']} n_failed={len(env._failed_edges)}")
        if terminated:
            break

    return env.metrics.compute(), total_reward


def run_grid_episode(baseline, verbose=False):
    """Run one episode with grid baseline."""
    return baseline.run_episode(verbose=verbose)


def main():
    parser = argparse.ArgumentParser(description="Dynamic scenario evaluation")
    parser.add_argument("--phase-a-ckpt", default="results/phase_a_grid_24x20/phase_a_best.pt")
    parser.add_argument("--n-planes", type=int, default=24)
    parser.add_argument("--sats-per-plane", type=int, default=20)
    parser.add_argument("--failure-prob", type=float, default=0.03)
    parser.add_argument("--failure-dur-min", type=int, default=2)
    parser.add_argument("--failure-dur-max", type=int, default=5)
    parser.add_argument("--seeds", type=int, nargs="+", default=[42, 100, 200])
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--quick", action="store_true", help="1 episode per seed, 10 steps")
    parser.add_argument("--phase-b-ckpt", default=None, help="Phase B checkpoint for evaluation")
    args = parser.parse_args()

    n_episodes = 1 if args.quick else 5
    episode_steps = 10 if args.quick else config.EPISODE_STEPS

    # Load Phase A model (with 7→8 dim padding)
    device = torch.device(args.device)

    if os.path.exists(args.phase_a_ckpt):
        backbone = load_backbone_with_padding(args.phase_a_ckpt, device=str(device))
        print(f"Loaded Phase A from {args.phase_a_ckpt}")
    else:
        print(f"WARNING: {args.phase_a_ckpt} not found, using random weights")
        backbone = GATv2Backbone()
    model = SupervisedGNN(backbone)

    model = model.to(device)
    model.eval()

    # Load Phase B model if provided
    phase_b_model = None
    if args.phase_b_ckpt and os.path.exists(args.phase_b_ckpt):
        backbone_b = load_backbone_with_padding(args.phase_a_ckpt, device=str(device))
        phase_b_model = DiscreteRLGNN(backbone_b).to(device)
        ckpt_b = torch.load(args.phase_b_ckpt, map_location=device, weights_only=False)
        phase_b_model.load_state_dict(ckpt_b["model"])
        phase_b_model.eval()
        print(f"Loaded Phase B from {args.phase_b_ckpt}")

    results = {"grid_no_fail": [], "grid_fail": [], "gnn_fail": []}
    if phase_b_model:
        results["gnn_phase_b"] = []

    for seed in args.seeds:
        print(f"\n--- Seed {seed} ---")

        # 1. Grid no failure (reference)
        b_ref = GridFixedBaseline(
            n_planes=args.n_planes, sats_per_plane=args.sats_per_plane,
            n_lct=config.N_LCT, seed=seed,
            failure_prob=0.0, episode_steps=episode_steps,
        )
        m_ref, r_ref = run_grid_episode(b_ref)
        results["grid_no_fail"].append(m_ref)
        print(f"  Grid (no fail): M1={m_ref['M1_throughput']:.4f} M3={m_ref['M3_switch_rate']:.4f}")

        # 2. Grid with failure
        b_fail = GridFixedBaseline(
            n_planes=args.n_planes, sats_per_plane=args.sats_per_plane,
            n_lct=config.N_LCT, seed=seed,
            failure_prob=args.failure_prob,
            failure_duration_min=args.failure_dur_min,
            failure_duration_max=args.failure_dur_max,
            episode_steps=episode_steps,
        )
        m_gf, r_gf = run_grid_episode(b_fail)
        results["grid_fail"].append(m_gf)
        print(f"  Grid (fail):    M1={m_gf['M1_throughput']:.4f} M3={m_gf['M3_switch_rate']:.4f}")

        # 3. GNN with failure
        env = ISLEnvironment(
            n_planes=args.n_planes, sats_per_plane=args.sats_per_plane,
            seed=seed,
            failure_prob=args.failure_prob,
            failure_duration_min=args.failure_dur_min,
            failure_duration_max=args.failure_dur_max,
            episode_steps=episode_steps,
        )
        # Pre-activate grid edges for warm start (same as Phase A eval)
        obs, _ = env.reset()
        grid_edges = build_grid_topology(env)
        env.set_isl_configuration(set(grid_edges.keys()))

        m_nn, r_nn = run_gnn_episode(env, model, device=device, preactivated=True)
        results["gnn_fail"].append(m_nn)
        print(f"  GNN  (fail):    M1={m_nn['M1_throughput']:.4f} M3={m_nn['M3_switch_rate']:.4f}")

        # 4. Phase B GNN with failure
        if phase_b_model:
            env_b = ISLEnvironment(
                n_planes=args.n_planes, sats_per_plane=args.sats_per_plane,
                seed=seed,
                failure_prob=args.failure_prob,
                failure_duration_min=args.failure_dur_min,
                failure_duration_max=args.failure_dur_max,
                episode_steps=episode_steps,
            )
            obs_b, _ = env_b.reset()
            grid_edges_b = build_grid_topology(env_b)
            env_b.set_isl_configuration(set(grid_edges_b.keys()))
            m_pb, r_pb = run_phase_b_episode(env_b, phase_b_model, device=device, preactivated=True)
            results["gnn_phase_b"].append(m_pb)
            print(f"  PhaseB(fail):   M1={m_pb['M1_throughput']:.4f} M3={m_pb['M3_switch_rate']:.4f}")

    # Summary
    print("\n" + "=" * 60)
    print(f"Results: {args.n_planes}x{args.sats_per_plane}, "
          f"failure_prob={args.failure_prob}, seeds={args.seeds}")
    print("=" * 60)

    for name, data in results.items():
        m1 = [m["M1_throughput"] for m in data]
        m3 = [m["M3_switch_rate"] for m in data]
        print(f"  {name:16s}: M1={np.mean(m1):.4f}+-{np.std(m1):.4f}  M3={np.mean(m3):.4f}")

    # GNN advantage under failures
    gnn_m1 = np.mean([m["M1_throughput"] for m in results["gnn_fail"]])
    grid_m1 = np.mean([m["M1_throughput"] for m in results["grid_fail"]])
    if grid_m1 > 0:
        ratio = gnn_m1 / grid_m1
        print(f"\n  GNN/Grid ratio under failures: {ratio:.3f}")


if __name__ == "__main__":
    main()
