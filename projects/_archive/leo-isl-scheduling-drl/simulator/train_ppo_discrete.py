"""Phase B: Discrete PPO fine-tuning on pretrained GATv2 backbone.

Loads backbone weights from Phase A supervised pretraining, then trains a
3-way discrete action head (AS-IS / FORCE-ON / FORCE-OFF) per candidate edge
using PPO with GAE advantage estimation.

Key design choices:
  - Backbone is frozen for the first `backbone_freeze_updates` update rounds
    to let the action head and critic stabilise before fine-tuning the encoder.
  - After unfreezing, a smaller learning rate is used for the full model.
  - PPO updates are done per-sample (each obs can have a different number of
    candidate edges) rather than mini-batching.
"""

import json
import os
import time
from typing import Any

import numpy as np
import torch
import torch.nn as nn

from .model_gat import GATv2Backbone, DiscreteRLGNN, load_backbone_with_padding
from .environment import ISLEnvironment
from .discrete_wrapper import DiscreteActionWrapper, obs_to_data
from .generate_dataset import build_grid_topology
from . import config


# ---------------------------------------------------------------------------
# Rollout buffer
# ---------------------------------------------------------------------------

class DiscreteRolloutBuffer:
    """Stores transitions for discrete-action PPO."""

    def __init__(self) -> None:
        self.obs_list: list[dict] = []
        self.actions_list: list[np.ndarray] = []
        self.log_probs: list[float] = []
        self.rewards: list[float] = []
        self.values: list[float] = []
        self.dones: list[bool] = []

        # Computed after calling compute_returns_and_advantages
        self.advantages: np.ndarray | None = None
        self.returns: np.ndarray | None = None

    def add(
        self,
        obs: dict,
        actions: np.ndarray,
        log_prob: float,
        reward: float,
        value: float,
        done: bool,
    ) -> None:
        self.obs_list.append(obs)
        self.actions_list.append(actions)
        self.log_probs.append(log_prob)
        self.rewards.append(reward)
        self.values.append(value)
        self.dones.append(done)

    def compute_returns_and_advantages(
        self,
        last_value: float,
        gamma: float,
        gae_lambda: float,
    ) -> None:
        """Compute GAE advantages and discounted returns."""
        n = len(self.rewards)
        self.advantages = np.zeros(n, dtype=np.float64)
        self.returns = np.zeros(n, dtype=np.float64)
        last_gae = 0.0

        for t in reversed(range(n)):
            if t == n - 1:
                next_value = last_value
            else:
                next_value = self.values[t + 1]
            next_non_terminal = 1.0 - float(self.dones[t])

            delta = (
                self.rewards[t] + gamma * next_value * next_non_terminal
                - self.values[t]
            )
            last_gae = delta + gamma * gae_lambda * next_non_terminal * last_gae
            self.advantages[t] = last_gae
            self.returns[t] = last_gae + self.values[t]

        # Normalise advantages (stabilises PPO)
        if n > 1:
            adv = self.advantages
            self.advantages = (adv - adv.mean()) / (adv.std() + 1e-8)

    def clear(self) -> None:
        self.obs_list.clear()
        self.actions_list.clear()
        self.log_probs.clear()
        self.rewards.clear()
        self.values.clear()
        self.dones.clear()
        self.advantages = None
        self.returns = None

    def __len__(self) -> int:
        return len(self.rewards)


# ---------------------------------------------------------------------------
# Evaluation helper
# ---------------------------------------------------------------------------

def evaluate_model(
    env: ISLEnvironment,
    model: DiscreteRLGNN,
    n_episodes: int = 5,
    device: str = "cpu",
    warm_start: bool = True,
) -> dict[str, float]:
    """Run episodes with deterministic policy, return averaged metrics."""
    wrapper = DiscreteActionWrapper(env, model, device=device)
    all_metrics: list[dict[str, float]] = []

    for ep in range(n_episodes):
        obs, _ = wrapper.reset(seed=9999 + ep)
        if warm_start:
            grid_edges = build_grid_topology(env)
            env.set_isl_configuration(set(grid_edges.keys()))
            obs = env._build_obs()
        done = False
        while not done:
            data = obs_to_data(obs).to(device)
            actions, _, _ = model.get_action(data, deterministic=True)
            obs, _reward, terminated, truncated, _info = wrapper.step(
                actions.cpu().numpy()
            )
            done = terminated or truncated
        metrics = env.metrics.compute()
        all_metrics.append(metrics)

    avg: dict[str, float] = {}
    for k in all_metrics[0]:
        avg[k] = float(np.mean([m[k] for m in all_metrics]))
    return avg


# ---------------------------------------------------------------------------
# Core training loop
# ---------------------------------------------------------------------------

def train_ppo_discrete(
    phase_a_checkpoint: str = "results/phase_a/phase_a_best.pt",
    n_planes: int = 24,
    sats_per_plane: int = 20,
    n_episodes: int = 200,
    update_interval: int = 5,
    lr: float = 1e-4,
    clip_eps: float = 0.2,
    gamma: float = 0.99,
    gae_lambda: float = 0.95,
    ppo_epochs: int = 4,
    entropy_coef: float = 0.05,
    value_coef: float = 0.5,
    max_grad_norm: float = 0.5,
    backbone_freeze_updates: int = 2,
    backbone_lr_scale: float = 0.1,
    device: str = "cpu",
    results_dir: str = "results/phase_b",
    seed: int = 42,
    failure_prob: float = 0.0,
    failure_duration_min: int = 2,
    failure_duration_max: int = 5,
    warm_start: bool = True,
) -> dict[str, Any]:
    """Phase B discrete PPO fine-tuning.

    Returns a summary dict with best reward, final metrics, and file paths.
    """
    torch.manual_seed(seed)
    np.random.seed(seed)

    os.makedirs(results_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # 1. Build model and load Phase A backbone (with 7→8 dim padding)
    # ------------------------------------------------------------------
    backbone = load_backbone_with_padding(phase_a_checkpoint, device=str(device))
    model = DiscreteRLGNN(backbone).to(device)
    print(f"[Phase B] Loaded backbone from {phase_a_checkpoint}")

    # ------------------------------------------------------------------
    # 2. Create environment + wrapper
    # ------------------------------------------------------------------
    env = ISLEnvironment(
        n_planes=n_planes,
        sats_per_plane=sats_per_plane,
        seed=seed,
        failure_prob=failure_prob,
        failure_duration_min=failure_duration_min,
        failure_duration_max=failure_duration_max,
    )
    wrapper = DiscreteActionWrapper(env, model, device=device)

    # ------------------------------------------------------------------
    # 3. Optimizer — initially only non-backbone params
    # ------------------------------------------------------------------
    def _head_params():
        return [p for p in model.parameters() if not _is_backbone(p)]

    def _is_backbone(p):
        return any(p is bp for bp in model.backbone.parameters())

    # Freeze backbone initially
    for param in model.backbone.parameters():
        param.requires_grad = False

    optimizer = torch.optim.Adam(_head_params(), lr=lr)

    # ------------------------------------------------------------------
    # 4. Training loop
    # ------------------------------------------------------------------
    buf = DiscreteRolloutBuffer()
    log_entries: list[dict] = []
    best_reward = -float("inf")
    update_count = 0
    backbone_unfrozen = False

    t_start = time.time()

    for ep in range(n_episodes):
        obs, _ = wrapper.reset(seed=seed + ep)
        if warm_start:
            grid_edges = build_grid_topology(env)
            env.set_isl_configuration(set(grid_edges.keys()))
            obs = env._build_obs()
        episode_reward = 0.0
        done = False

        while not done:
            data = obs_to_data(obs).to(device)
            actions, log_prob, value = model.get_action(data, deterministic=False)
            actions_np = actions.cpu().numpy()

            next_obs, reward, terminated, truncated, info = wrapper.step(actions_np)
            done = terminated or truncated

            buf.add(
                obs=obs,
                actions=actions_np,
                log_prob=log_prob.item(),
                reward=reward,
                value=value.item(),
                done=done,
            )
            episode_reward += reward
            obs = next_obs

        # --- PPO update every update_interval episodes ---
        if (ep + 1) % update_interval == 0 and len(buf) > 0:
            update_count += 1

            # Bootstrap last value
            with torch.no_grad():
                data_last = obs_to_data(obs).to(device)
                _, _, last_val = model.get_action(data_last, deterministic=True)
                last_value = last_val.item()

            buf.compute_returns_and_advantages(last_value, gamma, gae_lambda)

            # Optionally unfreeze backbone
            if (
                not backbone_unfrozen
                and update_count > backbone_freeze_updates
            ):
                for param in model.backbone.parameters():
                    param.requires_grad = True
                backbone_unfrozen = True
                # Rebuild optimizer with all params, smaller LR for backbone
                param_groups = [
                    {
                        "params": list(model.backbone.parameters()),
                        "lr": lr * backbone_lr_scale,
                    },
                    {
                        "params": [
                            p for p in model.parameters()
                            if not _is_backbone(p)
                        ],
                        "lr": lr,
                    },
                ]
                optimizer = torch.optim.Adam(param_groups)
                print(
                    f"[Phase B] Backbone unfrozen at update {update_count}, "
                    f"backbone_lr={lr * backbone_lr_scale:.2e}"
                )

            # PPO epochs
            for _ppo_ep in range(ppo_epochs):
                total_loss = torch.tensor(0.0, device=device)
                for i in range(len(buf)):
                    data_i = obs_to_data(buf.obs_list[i]).to(device)
                    actions_i = torch.tensor(
                        buf.actions_list[i], dtype=torch.long, device=device
                    )
                    old_lp = buf.log_probs[i]
                    adv = torch.tensor(
                        buf.advantages[i], dtype=torch.float32, device=device
                    )
                    ret = torch.tensor(
                        buf.returns[i], dtype=torch.float32, device=device
                    )

                    log_probs, values, entropies = model.evaluate_actions(
                        [data_i], [actions_i]
                    )
                    lp = log_probs[0]
                    val = values[0]
                    ent = entropies[0]

                    ratio = torch.exp(lp - old_lp)
                    surr1 = ratio * adv
                    surr2 = (
                        torch.clamp(ratio, 1.0 - clip_eps, 1.0 + clip_eps) * adv
                    )
                    policy_loss = -torch.min(surr1, surr2)

                    value_loss = value_coef * (val - ret).pow(2)
                    entropy_bonus = -entropy_coef * ent

                    total_loss = total_loss + policy_loss + value_loss + entropy_bonus

                optimizer.zero_grad()
                total_loss.backward()
                nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
                optimizer.step()

            # Logging
            avg_reward = episode_reward
            log_entries.append({
                "episode": ep + 1,
                "update": update_count,
                "episode_reward": avg_reward,
                "buffer_size": len(buf),
            })

            # Save best model
            if avg_reward > best_reward:
                best_reward = avg_reward
                torch.save(
                    {
                        "model": model.state_dict(),
                        "backbone": model.backbone.state_dict(),
                        "episode": ep + 1,
                        "reward": best_reward,
                    },
                    os.path.join(results_dir, "phase_b_best.pt"),
                )

            buf.clear()

        # Episode-level log (even when no update)
        if (ep + 1) % 20 == 0 or ep == 0:
            elapsed = time.time() - t_start
            print(
                f"[Phase B] Ep {ep + 1}/{n_episodes} | "
                f"reward={episode_reward:.4f} | "
                f"best={best_reward:.4f} | "
                f"updates={update_count} | "
                f"unfrozen={backbone_unfrozen} | "
                f"time={elapsed:.1f}s"
            )

    # ------------------------------------------------------------------
    # 5. Final evaluation
    # ------------------------------------------------------------------
    print("[Phase B] Running final evaluation ...")
    final_metrics = evaluate_model(env, model, n_episodes=5, device=device, warm_start=warm_start)
    elapsed = time.time() - t_start

    # Save final model
    torch.save(
        {
            "model": model.state_dict(),
            "backbone": model.backbone.state_dict(),
            "episode": n_episodes,
            "reward": best_reward,
            "final_metrics": final_metrics,
        },
        os.path.join(results_dir, "phase_b_final.pt"),
    )

    # Save training log
    log_path = os.path.join(results_dir, "phase_b_log.json")
    with open(log_path, "w") as f:
        json.dump(
            {
                "config": {
                    "n_planes": n_planes,
                    "sats_per_plane": sats_per_plane,
                    "n_episodes": n_episodes,
                    "update_interval": update_interval,
                    "lr": lr,
                    "clip_eps": clip_eps,
                    "gamma": gamma,
                    "gae_lambda": gae_lambda,
                    "ppo_epochs": ppo_epochs,
                    "entropy_coef": entropy_coef,
                    "value_coef": value_coef,
                    "max_grad_norm": max_grad_norm,
                    "backbone_freeze_updates": backbone_freeze_updates,
                    "backbone_lr_scale": backbone_lr_scale,
                    "seed": seed,
                    "failure_prob": failure_prob,
                    "warm_start": warm_start,
                },
                "log": log_entries,
                "best_reward": best_reward,
                "final_metrics": final_metrics,
                "total_time_s": elapsed,
            },
            f,
            indent=2,
        )

    print(
        f"[Phase B] Done in {elapsed:.1f}s | best_reward={best_reward:.4f} | "
        f"saved to {results_dir}"
    )

    return {
        "best_reward": best_reward,
        "final_metrics": final_metrics,
        "results_dir": results_dir,
        "total_time_s": elapsed,
    }


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Phase B: Discrete PPO fine-tuning")
    parser.add_argument(
        "--phase-a-ckpt",
        default="results/phase_a/phase_a_best.pt",
        help="Path to Phase A checkpoint",
    )
    parser.add_argument("--n-planes", type=int, default=config.N_PLANES)
    parser.add_argument("--sats-per-plane", type=int, default=config.SATS_PER_PLANE)
    parser.add_argument("--n-episodes", type=int, default=config.PHASE_B_EPISODES)
    parser.add_argument(
        "--update-interval", type=int, default=config.PHASE_B_UPDATE_INTERVAL
    )
    parser.add_argument("--lr", type=float, default=config.PHASE_B_LR)
    parser.add_argument("--clip-eps", type=float, default=config.PHASE_B_CLIP_EPS)
    parser.add_argument("--gamma", type=float, default=config.PHASE_B_GAMMA)
    parser.add_argument("--gae-lambda", type=float, default=config.PHASE_B_GAE_LAMBDA)
    parser.add_argument(
        "--ppo-epochs", type=int, default=config.PHASE_B_PPO_EPOCHS
    )
    parser.add_argument(
        "--entropy-coef", type=float, default=config.PHASE_B_ENTROPY_COEF
    )
    parser.add_argument(
        "--freeze-updates", type=int, default=config.PHASE_B_FREEZE_UPDATES
    )
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--results-dir", default="results/phase_b")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--failure-prob", type=float, default=config.FAILURE_PROB)
    parser.add_argument("--failure-dur-min", type=int, default=config.FAILURE_DURATION_MIN)
    parser.add_argument("--failure-dur-max", type=int, default=config.FAILURE_DURATION_MAX)
    parser.add_argument("--no-warm-start", action="store_true")
    args = parser.parse_args()

    train_ppo_discrete(
        phase_a_checkpoint=args.phase_a_ckpt,
        n_planes=args.n_planes,
        sats_per_plane=args.sats_per_plane,
        n_episodes=args.n_episodes,
        update_interval=args.update_interval,
        lr=args.lr,
        clip_eps=args.clip_eps,
        gamma=args.gamma,
        gae_lambda=args.gae_lambda,
        ppo_epochs=args.ppo_epochs,
        entropy_coef=args.entropy_coef,
        backbone_freeze_updates=args.freeze_updates,
        device=args.device,
        results_dir=args.results_dir,
        seed=args.seed,
        failure_prob=args.failure_prob,
        failure_duration_min=args.failure_dur_min,
        failure_duration_max=args.failure_dur_max,
        warm_start=not args.no_warm_start,
    )
