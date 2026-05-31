"""Quick test: REINFORCE with deterministic scores + noise exploration.

No PPO, no log_prob, no KL. Just:
1. Forward → deterministic scores (with prior biases)
2. Add Gaussian noise for exploration
3. REINFORCE gradient: -(G - baseline) * mean(scores[selected])

Goal: see if M1 can improve from prior baseline 0.0774.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import numpy as np
import torch
import torch.nn as nn
from collections import defaultdict

from simulator.environment import ISLEnvironment
from simulator.model_gat import GATv2ActorCritic
from simulator.train import obs_to_data
from simulator import config


def compute_selected_indices(scores, candidate_edges):
    """Replicate env._apply_lct: return set of selected edge indices."""
    scores = np.asarray(scores)
    sat_scores = defaultdict(list)
    for idx, (i, j, _) in enumerate(candidate_edges):
        s = float(scores[idx]) if idx < len(scores) else 0.0
        sat_scores[i].append((s, idx))
        sat_scores[j].append((s, idx))

    selected = set()
    for sat, edges in sat_scores.items():
        edges.sort(reverse=True)
        for k in range(min(config.N_LCT, len(edges))):
            selected.add(edges[k][1])
    return selected


def evaluate(model, env, device, seed=0):
    """Run deterministic eval episode, return metrics."""
    model.eval()

    def policy_fn(obs):
        data = obs_to_data(obs).to(device)
        with torch.no_grad():
            scores, _ = model(data)
        return scores.cpu().numpy()

    metrics, total_reward = env.run_episode(policy_fn)
    model.train()
    return metrics, total_reward


def run_reinforce(
    n_planes=24,
    sats_per_plane=20,
    n_episodes=20,
    lr=3e-5,
    gamma=0.99,
    noise_std=0.08,
    seed=42,
):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    env = ISLEnvironment(n_planes=n_planes, sats_per_plane=sats_per_plane, seed=seed)
    model = GATv2ActorCritic().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    print(f"N_sats={env.n_sats}, params={model.n_params:,}")

    # Baseline eval (prior only, no training)
    eval_env = ISLEnvironment(n_planes=n_planes, sats_per_plane=sats_per_plane, seed=seed + 9999)
    prior_metrics, prior_reward = evaluate(model, eval_env, device, seed=seed + 9999)
    print(f"\n[Prior baseline] M1={prior_metrics['M1_throughput']:.4f} "
          f"M3={prior_metrics['M3_switch_rate']:.4f} "
          f"reward={prior_reward:.3f}")

    baseline_reward = prior_reward  # running baseline

    for ep in range(n_episodes):
        # --- Collect episode ---
        obs, _ = env.reset(seed=seed + ep)
        trajectory = []
        episode_rewards = []

        for step in range(env.episode_steps):
            data = obs_to_data(obs).to(device)

            with torch.no_grad():
                scores, _ = model(data)

            # Exploration noise
            noisy = scores + torch.randn_like(scores) * noise_std
            noisy = noisy.clamp(0.0, 1.0)

            # Track selected edges
            selected_idx = compute_selected_indices(
                noisy.cpu().numpy(), obs["candidate_edges"]
            )

            obs, reward, done, _, info = env.step(noisy.cpu().numpy())
            episode_rewards.append(reward)
            trajectory.append((data, selected_idx))

            if done:
                break

        # --- Compute returns ---
        returns = []
        G = 0.0
        for r in reversed(episode_rewards):
            G = r + gamma * G
            returns.insert(0, G)
        returns_t = torch.tensor(returns, dtype=torch.float32)
        if len(returns_t) > 1:
            returns_t = (returns_t - returns_t.mean()) / (returns_t.std() + 1e-8)

        # --- REINFORCE update ---
        loss = torch.tensor(0.0, device=device)
        n_selected_total = 0
        for (data, sel_idx), G in zip(trajectory, returns_t):
            scores, _ = model(data)
            if sel_idx:
                idx_tensor = torch.tensor(sorted(sel_idx), device=device)
                selected_scores = scores[idx_tensor]
                loss = loss - G.to(device) * selected_scores.mean()
                n_selected_total += len(sel_idx)

        loss = loss / max(len(trajectory), 1)

        optimizer.zero_grad()
        loss.backward()
        grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()

        # Update baseline
        ep_reward = sum(episode_rewards)
        baseline_reward = 0.9 * baseline_reward + 0.1 * ep_reward

        # --- Eval every 5 episodes ---
        if (ep + 1) % 5 == 0 or ep == 0:
            eval_metrics, eval_reward = evaluate(
                model, eval_env, device, seed=seed + 9999
            )
            m1 = eval_metrics["M1_throughput"]
            m3 = eval_metrics["M3_switch_rate"]
            print(
                f"Ep {ep+1:3d}/{n_episodes}: "
                f"train_r={ep_reward:.3f} eval_M1={m1:.4f} "
                f"eval_r={eval_reward:.3f} M3={m3:.4f} "
                f"loss={loss.item():.4f} grad={grad_norm:.3f} "
                f"n_sel={n_selected_total//len(trajectory)}"
            )

    # Final eval
    final_metrics, final_reward = evaluate(model, eval_env, device, seed=seed + 9999)
    print(f"\n[Final] M1={final_metrics['M1_throughput']:.4f} "
          f"reward={final_reward:.3f}")
    print(f"[Prior] M1={prior_metrics['M1_throughput']:.4f} "
          f"reward={prior_reward:.3f}")
    delta = final_metrics["M1_throughput"] - prior_metrics["M1_throughput"]
    print(f"Delta M1: {delta:+.4f} ({delta/max(abs(prior_metrics['M1_throughput']),1e-6)*100:+.1f}%)")


if __name__ == "__main__":
    run_reinforce()
