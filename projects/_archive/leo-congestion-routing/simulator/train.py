"""PPO training loop for LEO congestion-aware routing (discrete K-path action space).

Key differences from continuous variant:
  - Buffer.actions: list[int] (discrete path selection)
  - Categorical distribution instead of Normal
  - No log_std parameter
  - actions_t dtype: long, shape (batch,)
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Generator

import numpy as np
import torch
import torch.nn as nn
from torch import Tensor

from .config import SimConfig
from .env import RoutingEnv
from .metrics import (
    aggregate_metrics,
    compute_convergence_speed,
    compute_episode_metrics,
    compute_generalization_gap,
)
from .model import RoutingActorCritic

# wandb conditional import
try:
    import wandb
    _WANDB = True
except ImportError:
    wandb = None  # type: ignore[assignment]
    _WANDB = False


# ---------------------------------------------------------------------------
# RolloutBuffer — on-policy buffer, discrete action space
# ---------------------------------------------------------------------------

class RolloutBuffer:
    """On-policy buffer for PPO with discrete actions."""

    def __init__(self) -> None:
        self.obs: list[dict] = []
        self.actions: list[int] = []
        self.log_probs: list[float] = []
        self.rewards: list[float] = []
        self.dones: list[bool] = []
        self.values: list[float] = []

        # Filled after GAE computation
        self.returns: Tensor | None = None
        self.advantages: Tensor | None = None

    def add(
        self,
        obs: dict,
        action: int,
        log_prob: float,
        reward: float,
        done: bool,
        value: float,
    ) -> None:
        self.obs.append(obs)
        self.actions.append(action)
        self.log_probs.append(log_prob)
        self.rewards.append(reward)
        self.dones.append(done)
        self.values.append(value)

    @property
    def size(self) -> int:
        return len(self.obs)

    def compute_returns_and_advantages(
        self, last_value: float, gamma: float, gae_lambda: float,
    ) -> None:
        """GAE(lambda) advantage estimation."""
        n = self.size
        rewards = torch.tensor(self.rewards, dtype=torch.float32)
        values = torch.tensor(self.values, dtype=torch.float32)
        dones = torch.tensor(self.dones, dtype=torch.float32)
        values = torch.cat([values, torch.tensor([last_value])])

        advantages = torch.zeros(n, dtype=torch.float32)
        last_gae = 0.0
        for t in reversed(range(n)):
            delta = rewards[t] + gamma * values[t + 1] * (1.0 - dones[t]) - values[t]
            last_gae = delta + gamma * gae_lambda * (1.0 - dones[t]) * last_gae
            advantages[t] = last_gae

        self.returns = advantages + values[:n]
        self.advantages = advantages

    def get_batches(
        self, batch_size: int,
    ) -> Generator[tuple[list[dict], Tensor, Tensor, Tensor, Tensor], None, None]:
        """Yield shuffled mini-batches.

        Returns:
            (obs_batch, actions, old_log_probs, returns, advantages)
        """
        n = self.size
        indices = np.arange(n)
        np.random.shuffle(indices)

        # Discrete: stack ints -> (N,) long tensor
        actions_t = torch.tensor(self.actions, dtype=torch.long)
        old_log_probs_t = torch.tensor(self.log_probs, dtype=torch.float32)

        for start in range(0, n, batch_size):
            idx = indices[start : start + batch_size]
            yield (
                [self.obs[i] for i in idx],
                actions_t[idx],
                old_log_probs_t[idx],
                self.returns[idx],
                self.advantages[idx],
            )


# ---------------------------------------------------------------------------
# RewardNormalizer — Welford online algorithm
# ---------------------------------------------------------------------------

class RewardNormalizer:
    """Running Z-score normalization for rewards."""

    def __init__(self, clip: float = 5.0, eps: float = 1e-8) -> None:
        self._mean = 0.0
        self._var = 1.0
        self._count = 1e-4
        self._clip = clip
        self._eps = eps

    def update_and_normalize(self, rewards: list[float]) -> list[float]:
        arr = np.array(rewards, dtype=np.float64)
        batch_mean = arr.mean()
        batch_var = arr.var()
        n = len(rewards)
        delta = batch_mean - self._mean
        total = self._count + n
        self._mean += delta * n / total
        m2 = (
            self._var * self._count
            + batch_var * n
            + delta ** 2 * self._count * n / total
        )
        self._var = m2 / total + self._eps
        self._count = total
        std = np.sqrt(self._var)
        normed = (arr - self._mean) / std
        return np.clip(normed, -self._clip, self._clip).tolist()

    def state_dict(self) -> dict:
        return {"mean": self._mean, "var": self._var, "count": self._count}

    def load_state_dict(self, d: dict) -> None:
        self._mean = d["mean"]
        self._var = d["var"]
        self._count = d["count"]


# ---------------------------------------------------------------------------
# PPO — discrete action space variant
# ---------------------------------------------------------------------------

class PPO:
    """Proximal Policy Optimization with clipped surrogate (discrete actions)."""

    def __init__(
        self,
        model: nn.Module,
        lr: float = 3e-4,
        clip_eps: float = 0.2,
        gamma: float = 0.99,
        gae_lambda: float = 0.95,
        epochs: int = 4,
        batch_size: int = 64,
        max_grad_norm: float = 0.5,
        entropy_coef: float = 0.01,
        device: str = "cpu",
        total_training_steps: int = 1_000_000,
    ) -> None:
        self.model = model.to(device)
        self.device = device
        self.clip_eps = clip_eps
        self.gamma = gamma
        self.gae_lambda = gae_lambda
        self.epochs = epochs
        self.batch_size = batch_size
        self.max_grad_norm = max_grad_norm
        self.entropy_coef = entropy_coef
        self._lr = lr
        self._total_updates = 0
        self._total_training_steps = total_training_steps

        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)

    def update(self, buffer: RolloutBuffer) -> dict:
        """Run PPO clipped update. Returns metrics dict."""
        self.model.train()

        # Normalize advantages across the full rollout
        advantages = buffer.advantages
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        buffer.advantages = advantages.to(self.device)

        epoch_metrics: dict[str, list[float]] = {
            "policy_loss": [],
            "value_loss": [],
            "entropy": [],
            "kl_approx": [],
        }

        for _epoch in range(self.epochs):
            for obs_batch, actions, old_log_probs, returns, adv_batch in (
                buffer.get_batches(self.batch_size)
            ):
                actions = actions.to(self.device)
                old_log_probs = old_log_probs.to(self.device)
                returns = returns.to(self.device)
                adv_batch = adv_batch.to(self.device)

                log_probs, values, entropy = self.model.evaluate_actions(
                    obs_batch, actions,
                )

                # Policy loss (clipped surrogate)
                ratio = torch.exp(log_probs - old_log_probs)
                surr1 = ratio * adv_batch
                surr2 = (
                    torch.clamp(ratio, 1.0 - self.clip_eps, 1.0 + self.clip_eps)
                    * adv_batch
                )
                policy_loss = -torch.min(surr1, surr2).mean()

                # Value loss
                value_loss = 0.5 * ((values - returns) ** 2).mean()

                # Entropy bonus
                entropy_loss = entropy.mean()

                # Total loss
                loss = policy_loss + 0.5 * value_loss - self.entropy_coef * entropy_loss

                self.optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(self.model.parameters(), self.max_grad_norm)
                self.optimizer.step()

                kl = (old_log_probs - log_probs).mean().item()

                epoch_metrics["policy_loss"].append(policy_loss.item())
                epoch_metrics["value_loss"].append(value_loss.item())
                epoch_metrics["entropy"].append(entropy_loss.item())
                epoch_metrics["kl_approx"].append(kl)

        self._total_updates += 1
        self._decay_lr()

        metrics = {k: float(np.mean(v)) for k, v in epoch_metrics.items()}

        if _WANDB and wandb.run is not None:
            wandb.log({
                "ppo/policy_loss": metrics["policy_loss"],
                "ppo/value_loss": metrics["value_loss"],
                "ppo/entropy": metrics["entropy"],
                "ppo/kl_approx": metrics["kl_approx"],
                "ppo/lr": self.optimizer.param_groups[0]["lr"],
                "ppo/update": self._total_updates,
            })

        return metrics

    def _decay_lr(self) -> None:
        """Linear LR decay based on total update count."""
        factor = max(1.0 - self._total_updates / self._total_training_steps, 0.0)
        for pg in self.optimizer.param_groups:
            pg["lr"] = self._lr * factor

    def save(
        self, path: str, reward_normalizer: RewardNormalizer | None = None,
    ) -> None:
        """Save checkpoint: model + optimizer + normalizer + step_count."""
        ckpt: dict = {
            "model": self.model.state_dict(),
            "optimizer": self.optimizer.state_dict(),
            "total_updates": self._total_updates,
        }
        if reward_normalizer is not None:
            ckpt["reward_normalizer"] = reward_normalizer.state_dict()
        torch.save(ckpt, path)

    def load(
        self, path: str, reward_normalizer: RewardNormalizer | None = None,
    ) -> None:
        """Load checkpoint, restore training state."""
        ckpt = torch.load(path, map_location=self.device, weights_only=False)
        self.model.load_state_dict(ckpt["model"])
        self.optimizer.load_state_dict(ckpt["optimizer"])
        self._total_updates = ckpt.get("total_updates", 0)
        if reward_normalizer is not None and "reward_normalizer" in ckpt:
            reward_normalizer.load_state_dict(ckpt["reward_normalizer"])


# ---------------------------------------------------------------------------
# Early Stopping — reward plateau + KL divergence
# ---------------------------------------------------------------------------

class EarlyStopping:
    """Dual-condition early stopping: reward plateau or excessive KL divergence."""

    def __init__(
        self,
        patience: int = 20,
        kl_threshold: float = 0.15,
        min_improvement: float = 0.0,
    ) -> None:
        self.patience = patience
        self.kl_threshold = kl_threshold
        self.min_improvement = min_improvement
        self._best_reward = -float("inf")
        self._wait = 0
        self._recent_kl: list[float] = []

    def step(self, mean_reward: float, mean_kl: float) -> bool:
        """Returns True if training should stop."""
        self._recent_kl.append(mean_kl)
        if len(self._recent_kl) > 5:
            self._recent_kl = self._recent_kl[-5:]

        # Condition 2: KL divergence too large
        if len(self._recent_kl) >= 3:
            avg_kl = float(np.mean(self._recent_kl))
            if avg_kl > self.kl_threshold:
                print(
                    f"  [EarlyStop] KL divergence too large: "
                    f"avg_kl={avg_kl:.4f} > {self.kl_threshold}"
                )
                return True

        # Condition 1: reward plateau
        if mean_reward > self._best_reward + self.min_improvement:
            self._best_reward = mean_reward
            self._wait = 0
        else:
            self._wait += 1
            if self._wait >= self.patience:
                print(
                    f"  [EarlyStop] Reward plateau: "
                    f"{self.patience} updates without improvement"
                )
                return True

        return False


# ---------------------------------------------------------------------------
# Training loop
# ---------------------------------------------------------------------------

def train(config: SimConfig | None = None, seed: int = 42) -> dict:
    """PPO training main loop for K-path LEO congestion-aware routing.

    Args:
        config: Simulation configuration. Uses defaults if None.
        seed: Random seed for reproducibility.

    Returns:
        dict with episode_rewards, best_reward, n_episodes, seed.
    """
    cfg = config or SimConfig()

    # Seed everything
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    # Build env and model
    env = RoutingEnv(cfg, seed=seed)
    model = RoutingActorCritic(
        node_dim=cfg.node_feat_dim,
        edge_dim=cfg.edge_feat_dim,
        hidden_dim=cfg.hidden_dim,
        n_layers=cfg.n_layers,
        n_heads=cfg.n_heads,
        k_paths=cfg.k_paths,
    ).to(cfg.device)

    ppo = PPO(
        model,
        lr=cfg.lr,
        clip_eps=cfg.clip_eps,
        gamma=cfg.gamma,
        gae_lambda=cfg.gae_lambda,
        epochs=cfg.n_epochs,
        batch_size=cfg.batch_size,
        max_grad_norm=cfg.max_grad_norm,
        entropy_coef=cfg.entropy_coef,
        device=cfg.device,
        total_training_steps=cfg.total_episodes,
    )
    reward_normalizer = RewardNormalizer()
    early_stopper = EarlyStopping(patience=cfg.early_stop_patience)

    results_dir = Path("projects/leo-congestion-routing/simulator/results")
    results_dir.mkdir(exist_ok=True, parents=True)

    episode_rewards: list[float] = []
    episode_mlus: list[float] = []
    all_metrics: list[dict] = []
    best_reward = -float("inf")
    buf = RolloutBuffer()

    t_start = time.time()

    for ep in range(cfg.total_episodes):
        obs, info = env.reset()
        done = False
        ep_reward = 0.0
        last_info = info

        while not done:
            action, log_prob, value = model.get_action(obs)
            action_int = action.item()

            next_obs, reward, terminated, truncated, info = env.step(action_int)
            done = terminated or truncated

            buf.add(
                obs,
                action_int,
                log_prob.item(),
                reward,
                done,
                value.item(),
            )
            obs = next_obs
            ep_reward += reward
            last_info = info

        episode_rewards.append(ep_reward)
        episode_mlus.append(last_info.get("final_mlu", last_info.get("mlu", 0.0)))

        # Periodic PPO update
        if (ep + 1) % cfg.update_interval == 0:
            # Normalize rewards
            buf.rewards = reward_normalizer.update_and_normalize(buf.rewards)

            # Bootstrap value for last obs
            with torch.no_grad():
                _, last_val = model._encode_obs(obs)
                last_val = last_val.squeeze().item()

            buf.compute_returns_and_advantages(last_val, cfg.gamma, cfg.gae_lambda)

            metrics = ppo.update(buf)
            metrics["episode"] = ep
            metrics["episode_reward"] = float(
                np.mean(episode_rewards[-cfg.update_interval:])
            )
            all_metrics.append(metrics)

            # Track best model
            if metrics["episode_reward"] > best_reward:
                best_reward = metrics["episode_reward"]
                ppo.save(
                    str(results_dir / "ppo_best.pt"),
                    reward_normalizer,
                )

            buf = RolloutBuffer()

            # Early stopping
            should_stop = early_stopper.step(
                metrics["episode_reward"], metrics["kl_approx"],
            )
            if should_stop:
                print(f"  [EarlyStop] Triggered at episode {ep + 1}")
                break

        # Progress logging
        if (ep + 1) % 50 == 0:
            recent = episode_rewards[-50:]
            mean_r = np.mean(recent)
            last_m = all_metrics[-1] if all_metrics else {}
            elapsed = time.time() - t_start
            print(
                f"  ep={ep + 1}/{cfg.total_episodes} "
                f"reward(last50)={mean_r:.4f} "
                f"ploss={last_m.get('policy_loss', 0):.4f} "
                f"ent={last_m.get('entropy', 0):.4f} "
                f"time={elapsed:.1f}s"
            )

            if _WANDB and wandb.run is not None:
                wandb.log({
                    "train/episode_reward_mean50": mean_r,
                    "train/episode": ep + 1,
                })

    # Save final results
    final_results = {
        "episode_rewards": episode_rewards,
        "episode_mlus": episode_mlus,
        "n_episodes": len(episode_rewards),
        "best_reward": best_reward,
        "seed": seed,
        "elapsed_seconds": time.time() - t_start,
    }
    out_path = results_dir / f"ppo_seed{seed}.json"
    with open(out_path, "w") as f:
        json.dump(final_results, f, indent=2)
    ppo.save(str(results_dir / f"ppo_seed{seed}.pt"), reward_normalizer)

    print(
        f"  [Train] seed={seed} done: {len(episode_rewards)} episodes, "
        f"best_reward={best_reward:.4f}"
    )
    return final_results


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------

def evaluate(
    model: RoutingActorCritic,
    env: RoutingEnv,
    n_eval: int = 50,
    seed_offset: int = 500000,
    device: str = "cpu",
) -> dict:
    """Evaluate trained model with greedy deterministic policy.

    Args:
        model: Trained RoutingActorCritic model.
        env: Routing environment.
        n_eval: Number of evaluation episodes.
        seed_offset: Base seed for evaluation episodes.
        device: Compute device.

    Returns:
        dict with per-metric mean/std (mlu, cv, overflow_ratio, mean_util)
        plus backward-compatible 'mean' and 'std' for MLU, and 'mlus' list.
    """
    model.eval()
    episode_metrics: list[dict] = []

    for i in range(n_eval):
        obs, _ = env.reset(seed=seed_offset + i)
        done = False
        while not done:
            action, _, _ = model.get_action(obs, deterministic=True)
            obs, _, terminated, truncated, info = env.step(action.item())
            done = terminated or truncated

        # Extract link-level data from final info
        link_load = info.get("link_load", {})
        capacity = info.get("capacity", env._capacity)
        n_total_edges = info.get("n_total_edges", env._E)
        final_mlu = info.get("final_mlu", info["mlu"])
        avg_delay_ms = info.get("avg_delay_ms", 0.0)
        max_delay_ms = info.get("max_delay_ms", 0.0)

        ep_m = compute_episode_metrics(
            link_load, capacity, n_total_edges, final_mlu,
            avg_delay_ms=avg_delay_ms, max_delay_ms=max_delay_ms,
        )
        episode_metrics.append(ep_m)

    aggregated = aggregate_metrics(episode_metrics)
    mlus = [m["mlu"] for m in episode_metrics]

    # Backward-compatible keys
    aggregated["mean"] = aggregated["mlu_mean"]
    aggregated["std"] = aggregated["mlu_std"]
    aggregated["mlus"] = mlus

    print(
        f"  [Eval] n={n_eval}, MLU={aggregated['mlu_mean']:.4f}+/-{aggregated['mlu_std']:.4f}, "
        f"CV={aggregated['cv_mean']:.4f}, "
        f"Overflow={aggregated['overflow_ratio_mean']:.4f}"
    )
    return aggregated


# ---------------------------------------------------------------------------
# Main entry: multi-seed training + evaluation
# ---------------------------------------------------------------------------

def main() -> None:
    """Multi-seed training and evaluation entry point."""
    cfg = SimConfig()

    if _WANDB:
        wandb.init(
            project="leo-congestion-routing",
            config=vars(cfg),
            name=f"ppo_kpath{cfg.k_paths}_{cfg.hidden_dim}h_{cfg.n_layers}l",
        )

    all_eval_results: list[dict] = []
    for seed in range(cfg.n_seeds):
        print(f"\n{'='*60}")
        print(f"  Training seed {seed}/{cfg.n_seeds}")
        print(f"{'='*60}")

        train_results = train(cfg, seed=seed)

        # Evaluate
        env = RoutingEnv(cfg, seed=seed)
        model = RoutingActorCritic(
            node_dim=cfg.node_feat_dim,
            edge_dim=cfg.edge_feat_dim,
            hidden_dim=cfg.hidden_dim,
            n_layers=cfg.n_layers,
            n_heads=cfg.n_heads,
            k_paths=cfg.k_paths,
        ).to(cfg.device)

        # Load best model
        results_dir = Path("projects/leo-congestion-routing/simulator/results")
        ckpt_path = results_dir / "ppo_best.pt"
        if ckpt_path.exists():
            ckpt = torch.load(
                str(ckpt_path), map_location=cfg.device, weights_only=False,
            )
            model.load_state_dict(ckpt["model"])
        else:
            print("  [Warning] No best checkpoint found, using final model")

        eval_result = evaluate(model, env, n_eval=cfg.n_eval, device=cfg.device)
        eval_result["seed"] = seed
        eval_result["train_best_reward"] = train_results["best_reward"]
        all_eval_results.append(eval_result)

    # Summary
    all_mlus = [r["mean"] for r in all_eval_results]
    print(f"\n{'='*60}")
    print(f"  Summary across {cfg.n_seeds} seeds")
    print(f"  MLU: {np.mean(all_mlus):.4f} +/- {np.std(all_mlus):.4f}")

    # Convergence speed (M5) from training MLUs
    conv_ep = compute_convergence_speed(episode_mlus)
    print(f"  Convergence (M5): ep={conv_ep}" if conv_ep >= 0 else "  Convergence (M5): not reached")

    for r in all_eval_results:
        print(
            f"    seed={r['seed']}: "
            f"MLU={r['mean']:.4f}+/-{r['std']:.4f}, "
            f"CV={r.get('cv_mean', 0):.4f}, "
            f"Overflow={r.get('overflow_ratio_mean', 0):.4f}"
        )
    print(f"{'='*60}")

    # Save summary
    results_dir = Path("projects/leo-congestion-routing/simulator/results")
    summary_path = results_dir / "eval_summary.json"
    summary = {
        "seeds": all_eval_results,
        "overall_mean": float(np.mean(all_mlus)),
        "overall_std": float(np.std(all_mlus)),
        "convergence_episode": conv_ep,
    }

    # Generalization gap (M4)
    train_mlu_mean = float(np.mean(episode_mlus)) if episode_mlus else 0.0
    test_mlu_mean = float(np.mean(all_mlus))
    gen_gap = compute_generalization_gap(train_mlu_mean, test_mlu_mean)
    summary["generalization_gap"] = gen_gap
    print(f"  Generalization Gap (M4): {gen_gap:.4f}")

    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    if _WANDB and wandb.run is not None:
        wandb.finish()


if __name__ == "__main__":
    main()
