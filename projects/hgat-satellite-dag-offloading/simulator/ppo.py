"""PPO backbone for satellite DAG task offloading.

Works with any GNN encoder that implements BaseActorCritic.
Action space is flat Discrete(n_tasks * n_nodes) with per-step action masking.
"""

from abc import ABC, abstractmethod
from typing import Generator

import numpy as np
import torch
import torch.nn as nn
from torch import Tensor
from torch.distributions import Categorical
from torch_geometric.data import HeteroData

from config import (
    PPO_LR,
    PPO_BATCH,
    PPO_CLIP,
    PPO_GAE_LAMBDA,
    PPO_GAMMA,
    PPO_EPOCHS,
    PPO_MAX_GRAD_NORM,
    PPO_ENTROPY_COEF,
)

# Invalid-logit sentinel applied before softmax
_MASK_VALUE = -1e8


# ---------------------------------------------------------------------------
# Rollout buffer — stores variable-shape HeteroData as plain lists
# ---------------------------------------------------------------------------

class RolloutBuffer:
    """On-policy buffer for PPO transitions.

    Observations (HeteroData) are kept as a Python list since they cannot be
    stacked into a single tensor.  All other fields are 1-D tensors of length
    ``n_steps``.
    """

    def __init__(self) -> None:
        self.obs: list[HeteroData] = []
        self.actions: list[int] = []
        self.log_probs: list[float] = []
        self.rewards: list[float] = []
        self.dones: list[bool] = []
        self.values: list[float] = []
        self.action_masks: list[np.ndarray] = []

        # Filled by compute_returns_and_advantages
        self.returns: Tensor | None = None
        self.advantages: Tensor | None = None

    def add(
        self,
        obs: HeteroData,
        action: int,
        log_prob: float,
        reward: float,
        done: bool,
        value: float,
        action_mask: np.ndarray,
    ) -> None:
        self.obs.append(obs)
        self.actions.append(action)
        self.log_probs.append(log_prob)
        self.rewards.append(reward)
        self.dones.append(done)
        self.values.append(value)
        self.action_masks.append(action_mask)

    @property
    def size(self) -> int:
        return len(self.obs)

    # ------------------------------------------------------------------
    # GAE(λ) advantage estimation
    # ------------------------------------------------------------------

    def compute_returns_and_advantages(self, last_value: float) -> None:
        """Compute returns and GAE advantages given V(s_{T+1}).

        δ_t = r_t + γ · V(s_{t+1}) · (1 − d_t) − V(s_t)
        A_t = Σ_{l≥0} (γλ)^l · δ_{t+l}
        """
        n = self.size
        rewards = torch.tensor(self.rewards, dtype=torch.float32)
        values = torch.tensor(self.values, dtype=torch.float32)
        dones = torch.tensor(self.dones, dtype=torch.float32)

        # Append bootstrap value for t = n
        values = torch.cat([values, torch.tensor([last_value])])

        advantages = torch.zeros(n, dtype=torch.float32)
        last_gae = 0.0
        for t in reversed(range(n)):
            delta = rewards[t] + PPO_GAMMA * values[t + 1] * (1.0 - dones[t]) - values[t]
            last_gae = delta + PPO_GAMMA * PPO_GAE_LAMBDA * (1.0 - dones[t]) * last_gae
            advantages[t] = last_gae

        self.returns = advantages + values[:n]
        self.advantages = advantages

    # ------------------------------------------------------------------
    # Mini-batch iterator
    # ------------------------------------------------------------------

    def get_batches(
        self, batch_size: int
    ) -> Generator[
        tuple[
            list[HeteroData],  # obs sub-list
            Tensor,            # actions
            Tensor,            # old log probs
            Tensor,            # returns
            Tensor,            # advantages
            Tensor,            # action masks
        ],
        None,
        None,
    ]:
        """Yield shuffled mini-batches from the buffer."""
        n = self.size
        indices = np.arange(n)
        np.random.shuffle(indices)

        actions_t = torch.tensor(self.actions, dtype=torch.long)
        old_log_probs_t = torch.tensor(self.log_probs, dtype=torch.float32)
        masks_t = torch.tensor(np.stack(self.action_masks), dtype=torch.bool)

        for start in range(0, n, batch_size):
            idx = indices[start : start + batch_size]
            yield (
                [self.obs[i] for i in idx],
                actions_t[idx],
                old_log_probs_t[idx],
                self.returns[idx],
                self.advantages[idx],
                masks_t[idx],
            )


# ---------------------------------------------------------------------------
# Abstract actor-critic interface
# ---------------------------------------------------------------------------

class BaseActorCritic(nn.Module, ABC):
    """Interface every GNN encoder must implement.

    Subclasses take a HeteroData observation and produce action logits
    (size = action_space.n) and a scalar state value.
    """

    @abstractmethod
    def forward(self, obs: HeteroData) -> tuple[Tensor, Tensor]:
        """Return (action_logits [n_actions], value_scalar)."""
        ...

    @torch.no_grad()
    def get_action(
        self, obs: HeteroData, action_mask: np.ndarray
    ) -> tuple[int, float, float, float]:
        """Sample one action.  Returns (action, log_prob, value, entropy)."""
        logits, value = self.forward(obs)
        logits = _apply_mask(logits, action_mask)
        dist = Categorical(logits=logits)
        action = dist.sample()
        return (
            action.item(),
            dist.log_prob(action).item(),
            value.item(),
            dist.entropy().item(),
        )

    def evaluate_actions(
        self,
        obs_list: list[HeteroData],
        actions: Tensor,
        action_masks: Tensor,
    ) -> tuple[Tensor, Tensor, Tensor]:
        """Re-evaluate actions under the current policy.  Returns (log_probs, values, entropy)."""
        log_probs_list: list[Tensor] = []
        values_list: list[Tensor] = []
        entropy_list: list[Tensor] = []

        for i, obs in enumerate(obs_list):
            logits, value = self.forward(obs)
            logits = _apply_mask(logits, action_masks[i])
            dist = Categorical(logits=logits)
            log_probs_list.append(dist.log_prob(actions[i]))
            values_list.append(value.squeeze())
            entropy_list.append(dist.entropy())

        return (
            torch.stack(log_probs_list),
            torch.stack(values_list),
            torch.stack(entropy_list),
        )


def _apply_mask(logits: Tensor, mask: np.ndarray | Tensor) -> Tensor:
    """Set invalid action logits to a large negative value."""
    mask_t = torch.as_tensor(mask, dtype=torch.bool, device=logits.device)
    return logits.masked_fill(~mask_t, _MASK_VALUE)


# ---------------------------------------------------------------------------
# PPO algorithm
# ---------------------------------------------------------------------------

class PPO:
    """Proximal Policy Optimization with clipped surrogate objective.

    Designed for single-env on-policy collection followed by multiple
    gradient epochs over the rollout buffer.
    """

    def __init__(
        self,
        model: BaseActorCritic,
        lr: float = PPO_LR,
        clip_eps: float = PPO_CLIP,
        gamma: float = PPO_GAMMA,
        gae_lambda: float = PPO_GAE_LAMBDA,
        epochs: int = PPO_EPOCHS,
        batch_size: int = PPO_BATCH,
        max_grad_norm: float = PPO_MAX_GRAD_NORM,
        entropy_coef: float = PPO_ENTROPY_COEF,
        device: str = "cpu",
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

        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        self._lr = lr
        self._total_updates = 0

    # ------------------------------------------------------------------
    # Rollout collection
    # ------------------------------------------------------------------

    @torch.no_grad()
    def collect_rollout(self, env, n_steps: int) -> RolloutBuffer:
        """Run *env* for *n_steps* and return a filled buffer.

        Handles automatic environment resets on termination.  The bootstrap
        value for the final step is computed from the last observation.
        """
        buffer = RolloutBuffer()
        self.model.eval()

        obs, info = env.reset()
        for _ in range(n_steps):
            action_mask = info["action_mask"]
            action, log_prob, value, _ = self.model.get_action(obs, action_mask)

            next_obs, reward, terminated, truncated, info = env.step(action)
            buffer.add(obs, action, log_prob, reward, terminated, value, action_mask)

            obs = next_obs
            # Gymnasium auto-resets on termination; info from step() already
            # contains the new episode's action mask after auto-reset, but we
            # rely on the returned obs directly which is the new-episode obs.

        # Bootstrap value for the last observation (needed by GAE)
        _, _, last_value, _ = self.model.get_action(obs, info["action_mask"])
        buffer.compute_returns_and_advantages(last_value)

        return buffer

    # ------------------------------------------------------------------
    # PPO update
    # ------------------------------------------------------------------

    def update(self, buffer: RolloutBuffer) -> dict:
        """Run PPO clipped update over the buffer.  Returns metrics dict."""
        self.model.train()

        # Normalise advantages across the full rollout (stable baseline trick)
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
            for obs_batch, actions, old_log_probs, returns, adv_batch, masks in (
                buffer.get_batches(self.batch_size)
            ):
                actions = actions.to(self.device)
                old_log_probs = old_log_probs.to(self.device)
                returns = returns.to(self.device)
                adv_batch = adv_batch.to(self.device)
                masks = masks.to(self.device)

                log_probs, values, entropy = self.model.evaluate_actions(
                    obs_batch, actions, masks
                )

                # ---- Policy loss (clipped surrogate) ----
                ratio = torch.exp(log_probs - old_log_probs)
                surr1 = ratio * adv_batch
                surr2 = torch.clamp(ratio, 1.0 - self.clip_eps, 1.0 + self.clip_eps) * adv_batch
                policy_loss = -torch.min(surr1, surr2).mean()

                # ---- Value loss ----
                value_loss = 0.5 * ((values - returns) ** 2).mean()

                # ---- Entropy bonus ----
                entropy_loss = entropy.mean()

                # ---- Total loss ----
                loss = policy_loss + 0.5 * value_loss - self.entropy_coef * entropy_loss

                self.optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(self.model.parameters(), self.max_grad_norm)
                self.optimizer.step()

                # Approximate KL for monitoring
                kl = (old_log_probs - log_probs).mean().item()

                epoch_metrics["policy_loss"].append(policy_loss.item())
                epoch_metrics["value_loss"].append(value_loss.item())
                epoch_metrics["entropy"].append(entropy_loss.item())
                epoch_metrics["kl_approx"].append(kl)

        self._total_updates += 1
        # Linear learning-rate decay
        self._decay_lr()

        return {k: float(np.mean(v)) for k, v in epoch_metrics.items()}

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _decay_lr(self) -> None:
        """Optional linear LR decay (call after each update)."""
        # Hard-cap at 1M updates to avoid lr going negative
        factor = max(1.0 - self._total_updates / 1_000_000, 0.0)
        for pg in self.optimizer.param_groups:
            pg["lr"] = self._lr * factor

    def save(self, path: str) -> None:
        torch.save(
            {
                "model": self.model.state_dict(),
                "optimizer": self.optimizer.state_dict(),
                "total_updates": self._total_updates,
            },
            path,
        )

    def load(self, path: str) -> None:
        ckpt = torch.load(path, map_location=self.device, weights_only=False)
        self.model.load_state_dict(ckpt["model"])
        self.optimizer.load_state_dict(ckpt["optimizer"])
        self._total_updates = ckpt.get("total_updates", 0)
