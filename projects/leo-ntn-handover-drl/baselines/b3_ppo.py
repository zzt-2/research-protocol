"""B3 Baseline: PPO for LEO satellite handover.

Shared ActorCritic with 3-layer MLP (256-256-128, tanh).
Parameter sharing across all UEs. Action masking for invisible satellites.
GAE advantage estimation with clipped surrogate objective.

Trains for NUM_EPISODES, evaluates with deterministic policy across
NUM_EVAL_SEEDS, saves metrics to results/b3_ppo_results.json.
"""

import json
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import config as cfg
from simulator.environment import LEOSatHandoverEnv

# ── Hyperparameters (from config.py) ──────────────────────────────────────────
LR = cfg.PPO_LR
GAMMA = cfg.PPO_GAMMA
GAE_LAMBDA = cfg.PPO_GAE_LAMBDA
CLIP_EPS = cfg.PPO_CLIP_EPS
ENTROPY_COEF = cfg.PPO_ENTROPY_COEF
VALUE_COEF = cfg.PPO_VALUE_COEF
PPO_EPOCHS = cfg.PPO_UPDATE_EPOCHS
MINIBATCH_SIZE = cfg.PPO_MINIBATCH_SIZE
ROLLOUT_STEPS = cfg.PPO_ROLLOUT_STEPS
HIDDEN = cfg.PPO_HIDDEN  # (256, 256, 128)
NUM_EPISODES = cfg.NUM_EPISODES
NUM_EVAL_SEEDS = cfg.NUM_EVAL_SEEDS
NUM_UES = cfg.NUM_UES
MAX_GRAD_NORM = 0.5

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ── Actor-Critic Network ─────────────────────────────────────────────────────
class ActorCritic(nn.Module):
    """Shared backbone (first two layers) with separate actor/critic heads.

    Architecture:
        Backbone: obs_dim → 256 → 256 (tanh)
        Actor head: 256 → 128 → num_sats (tanh activations)
        Critic head: 256 → 128 → 1 (tanh activations)
    """

    def __init__(self, obs_dim: int, num_sats: int):
        super().__init__()
        # Shared backbone
        self.backbone = nn.Sequential(
            nn.Linear(obs_dim, HIDDEN[0]),
            nn.Tanh(),
            nn.Linear(HIDDEN[0], HIDDEN[1]),
            nn.Tanh(),
        )
        # Actor head
        self.actor = nn.Sequential(
            nn.Linear(HIDDEN[1], HIDDEN[2]),
            nn.Tanh(),
            nn.Linear(HIDDEN[2], num_sats),
        )
        # Critic head
        self.critic = nn.Sequential(
            nn.Linear(HIDDEN[1], HIDDEN[2]),
            nn.Tanh(),
            nn.Linear(HIDDEN[2], 1),
        )

    def forward(self, obs: torch.Tensor, valid_mask: torch.Tensor):
        """Return masked logits, action probabilities, and value estimate.

        Parameters
        ----------
        obs : (batch, obs_dim)
        valid_mask : (batch, num_sats) bool

        Returns
        -------
        logits, probs, value
        """
        features = self.backbone(obs)
        logits = self.actor(features)

        # Mask invalid actions by setting logits to -inf
        masked_logits = logits.masked_fill(~valid_mask, float("-inf"))

        # For UEs with no visible satellites, fall back to uniform distribution
        no_valid = ~valid_mask.any(dim=-1, keepdim=True)
        safe_logits = torch.where(
            no_valid.expand_as(masked_logits),
            torch.zeros_like(masked_logits),
            masked_logits,
        )
        probs = torch.softmax(safe_logits, dim=-1)
        value = self.critic(features).squeeze(-1)
        return logits, probs, value

    def get_action(self, obs: torch.Tensor, valid_mask: torch.Tensor, deterministic: bool = False):
        """Select actions. Returns (action, log_prob, value), all detached."""
        _, probs, value = self.forward(obs, valid_mask)
        if deterministic:
            action = probs.argmax(dim=-1)
            log_prob = torch.zeros(obs.shape[0], device=obs.device)
        else:
            dist = Categorical(probs=probs)
            action = dist.sample()
            log_prob = dist.log_prob(action)
        return action.detach(), log_prob.detach(), value.detach()

    def evaluate_actions(self, obs: torch.Tensor, actions: torch.Tensor, valid_masks: torch.Tensor):
        """Re-evaluate log_prob, value, and entropy for given (obs, action) pairs."""
        _, probs, value = self.forward(obs, valid_masks)
        dist = Categorical(probs=probs)
        log_prob = dist.log_prob(actions)
        entropy = dist.entropy().mean()
        # Clamp to prevent NaN from edge cases
        log_prob = torch.clamp(log_prob, min=-20.0)
        return log_prob, value, entropy


# ── Rollout Buffer ────────────────────────────────────────────────────────────
class RolloutBuffer:
    """Stores per-UE transitions and computes GAE advantages."""

    def __init__(self):
        self.clear()

    def push(self, obs, action, log_prob, reward, value, valid_mask, done):
        self.obs_list.append(obs)
        self.actions.append(action)
        self.log_probs.append(log_prob)
        self.rewards.append(reward)
        self.values.append(value)
        self.valid_masks.append(valid_mask)
        self.dones.append(done)

    def clear(self):
        self.obs_list = []
        self.actions = []
        self.log_probs = []
        self.rewards = []
        self.values = []
        self.valid_masks = []
        self.dones = []

    def __len__(self):
        return len(self.rewards)

    def compute_gae(self, last_value: float, last_done: float):
        """Compute GAE advantages and discounted returns."""
        rewards = np.array(self.rewards, dtype=np.float32)
        values = np.array(self.values, dtype=np.float32)
        dones = np.array(self.dones, dtype=np.float32)

        advantages = np.zeros_like(rewards)
        last_gae = 0.0
        for t in reversed(range(len(rewards))):
            if t == len(rewards) - 1:
                next_value = last_value
                next_done = last_done
            else:
                next_value = values[t + 1]
                next_done = dones[t + 1]
            delta = rewards[t] + GAMMA * next_value * (1.0 - next_done) - values[t]
            last_gae = delta + GAMMA * GAE_LAMBDA * (1.0 - next_done) * last_gae
            advantages[t] = last_gae

        returns = advantages + values
        return advantages, returns


# ── PPO Update ────────────────────────────────────────────────────────────────
def ppo_update(model, optimizer, buffer, last_value, last_done):
    """Run PPO update on collected rollout data. Returns (policy_loss, value_loss, entropy)."""
    if len(buffer) == 0:
        return 0.0, 0.0, 0.0

    advantages, returns = buffer.compute_gae(last_value, last_done)

    # Normalize advantages for stability
    if len(advantages) > 1:
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

    obs_arr = np.array(buffer.obs_list, dtype=np.float32)
    actions_arr = np.array(buffer.actions, dtype=np.int64)
    old_log_probs_arr = np.array(buffer.log_probs, dtype=np.float32)
    valid_masks_arr = np.array(buffer.valid_masks, dtype=np.bool_)
    returns_arr = returns.astype(np.float32)
    advantages_arr = advantages.astype(np.float32)

    dataset_size = len(obs_arr)
    mb_size = min(MINIBATCH_SIZE, dataset_size)

    total_policy_loss = 0.0
    total_value_loss = 0.0
    total_entropy = 0.0
    num_updates = 0

    for _ in range(PPO_EPOCHS):
        indices = np.arange(dataset_size)
        np.random.shuffle(indices)

        for start in range(0, dataset_size, mb_size):
            mb_idx = indices[start : start + mb_size]

            mb_obs = torch.from_numpy(obs_arr[mb_idx]).to(DEVICE)
            mb_actions = torch.from_numpy(actions_arr[mb_idx]).to(DEVICE)
            mb_old_logp = torch.from_numpy(old_log_probs_arr[mb_idx]).to(DEVICE)
            mb_valid = torch.from_numpy(valid_masks_arr[mb_idx]).to(DEVICE)
            mb_returns = torch.from_numpy(returns_arr[mb_idx]).to(DEVICE)
            mb_advantages = torch.from_numpy(advantages_arr[mb_idx]).to(DEVICE)

            new_log_prob, value_pred, entropy = model.evaluate_actions(
                mb_obs, mb_actions, mb_valid
            )

            # Clipped surrogate objective
            ratio = torch.exp(new_log_prob - mb_old_logp)
            surr1 = ratio * mb_advantages
            surr2 = torch.clamp(ratio, 1.0 - CLIP_EPS, 1.0 + CLIP_EPS) * mb_advantages
            policy_loss = -torch.min(surr1, surr2).mean()

            # Value loss (MSE)
            value_loss = nn.MSELoss()(value_pred, mb_returns)

            # Entropy bonus (maximize entropy → minimize negative entropy)
            entropy_loss = -entropy

            loss = policy_loss + VALUE_COEF * value_loss + ENTROPY_COEF * entropy_loss

            optimizer.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), MAX_GRAD_NORM)
            optimizer.step()

            total_policy_loss += policy_loss.item()
            total_value_loss += value_loss.item()
            total_entropy += entropy.item()
            num_updates += 1

    avg_policy_loss = total_policy_loss / max(num_updates, 1)
    avg_value_loss = total_value_loss / max(num_updates, 1)
    avg_entropy = total_entropy / max(num_updates, 1)
    return avg_policy_loss, avg_value_loss, avg_entropy


# ── Training ──────────────────────────────────────────────────────────────────
def train(env: LEOSatHandoverEnv, seed: int):
    """Train PPO agent. Returns (model, episode_rewards, update_log)."""
    torch.manual_seed(seed)
    np.random.seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    obs_dim = env.obs_dim
    num_sats = env.num_sats
    num_ues = env.num_ues

    model = ActorCritic(obs_dim, num_sats).to(DEVICE)
    optimizer = optim.Adam(model.parameters(), lr=LR)
    buffer = RolloutBuffer()

    episode_rewards = []
    update_log = []  # (update_idx, avg_reward, policy_loss, value_loss, entropy)
    global_update = 0

    for ep in range(NUM_EPISODES):
        obs = env.reset(seed=seed + ep)
        ep_reward = 0.0
        ep_steps = 0
        done = False

        while not done:
            # Build batch of all UE observations and valid action masks
            obs_batch = torch.from_numpy(obs).float().to(DEVICE)
            valid_batch = torch.from_numpy(env.get_valid_actions()).to(DEVICE)

            with torch.no_grad():
                actions_t, log_probs_t, values_t = model.get_action(obs_batch, valid_batch)

            actions_np = actions_t.cpu().numpy()
            next_obs, rewards, done, info = env.step(actions_np)

            # Store per-UE transitions
            for ue in range(num_ues):
                buffer.push(
                    obs[ue],
                    actions_np[ue],
                    log_probs_t[ue].item(),
                    rewards[ue],
                    values_t[ue].item(),
                    valid_batch[ue].cpu().numpy(),
                    float(done),
                )

            ep_reward += rewards.sum()
            ep_steps += 1
            obs = next_obs

            # PPO update when enough transitions collected
            if len(buffer) >= ROLLOUT_STEPS or done:
                # Bootstrap value for non-terminal states
                if not done:
                    next_obs_t = torch.from_numpy(obs).float().to(DEVICE)
                    next_valid_t = torch.from_numpy(env.get_valid_actions()).to(DEVICE)
                    with torch.no_grad():
                        _, _, next_val = model(next_obs_t, next_valid_t)
                    last_value = next_val.mean().item()
                    last_done = 0.0
                else:
                    last_value = 0.0
                    last_done = 1.0

                p_loss, v_loss, ent = ppo_update(model, optimizer, buffer, last_value, last_done)
                buffer.clear()

                # Compute avg reward over the last batch of transitions
                recent_rewards = rewards
                avg_r = float(recent_rewards.mean())
                update_log.append((global_update, avg_r, p_loss, v_loss, ent))

                if (global_update + 1) % 5 == 0:
                    print(
                        f"  update {global_update+1:4d} | "
                        f"avg_reward={avg_r:.4f} | "
                        f"p_loss={p_loss:.4f} | "
                        f"v_loss={v_loss:.4f} | "
                        f"entropy={ent:.4f}"
                    )
                global_update += 1

        episode_rewards.append(ep_reward / max(ep_steps, 1))

        if (ep + 1) % 10 == 0:
            recent = episode_rewards[-10:]
            print(
                f"  ep {ep+1:3d}/{NUM_EPISODES} | "
                f"avg_step_reward={np.mean(recent):.4f} | "
                f"updates={global_update}"
            )

    return model, episode_rewards, update_log


# ── Evaluation (deterministic) ────────────────────────────────────────────────
def evaluate(env: LEOSatHandoverEnv, model: ActorCritic, seed: int) -> dict:
    """Run one episode with deterministic (argmax) policy. Return metrics."""
    obs = env.reset(seed=seed)
    step_rewards = []
    blocking_rates = []
    handover_counts = []
    throughputs = []
    ue_throughput = np.zeros(env.num_ues)

    done = False
    while not done:
        obs_t = torch.from_numpy(obs).float().to(DEVICE)
        valid_t = torch.from_numpy(env.get_valid_actions()).to(DEVICE)

        with torch.no_grad():
            actions_t, _, _ = model.get_action(obs_t, valid_t, deterministic=True)

        actions_np = actions_t.cpu().numpy()
        obs, rewards, done, info = env.step(actions_np)

        step_rewards.append(float(rewards.mean()))
        blocking_rates.append(float(info["blocking_rate"]))
        handover_counts.append(int(info["handover_count"]))
        throughputs.append(float(info["total_throughput_bps"]))
        ue_throughput += info['throughput_bps']

    jain = float(np.sum(ue_throughput) ** 2 /
                 (env.num_ues * np.sum(ue_throughput ** 2) + 1e-12))
    return {
        "mean_step_reward": float(np.mean(step_rewards)),
        "mean_throughput_bps": float(np.mean(throughputs)),
        "mean_blocking_rate": float(np.mean(blocking_rates)),
        "total_handover_count": int(np.sum(handover_counts)),
        "jain_fairness": jain,
    }


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print(f"Device: {DEVICE}")
    print(f"Config: episodes={NUM_EPISODES}, rollout_steps={ROLLOUT_STEPS}, "
          f"epochs={PPO_EPOCHS}, minibatch={MINIBATCH_SIZE}")
    print(f"        lr={LR}, gamma={GAMMA}, gae_lambda={GAE_LAMBDA}, clip_eps={CLIP_EPS}")
    print(f"        entropy_coef={ENTROPY_COEF}, value_coef={VALUE_COEF}")
    print(f"        hidden={HIDDEN}, num_ues={NUM_UES}")
    print()

    results = {"seeds": [], "summary": {}}
    all_eval_metrics = []

    # Training seed
    train_seed = 42

    print(f"{'='*60}")
    print(f"Training B3 PPO — seed={train_seed}")
    print(f"{'='*60}")

    env = LEOSatHandoverEnv(num_ues=NUM_UES, seed=train_seed)
    t0 = time.time()
    model, ep_rewards, update_log = train(env, train_seed)
    train_time = time.time() - t0
    print(f"Training completed in {train_time:.1f}s")

    # Evaluate on multiple seeds with deterministic policy
    eval_seeds = [100 + i for i in range(NUM_EVAL_SEEDS)]
    for eval_seed in eval_seeds:
        eval_env = LEOSatHandoverEnv(num_ues=NUM_UES, seed=eval_seed)
        metrics = evaluate(eval_env, model, seed=eval_seed)
        metrics["train_seed"] = train_seed
        metrics["eval_seed"] = eval_seed
        metrics["train_time_s"] = round(train_time, 1)
        metrics["num_episodes"] = NUM_EPISODES
        metrics["total_updates"] = len(update_log)
        results["seeds"].append(metrics)
        all_eval_metrics.append(metrics)

        print(
            f"  Eval seed={eval_seed}: reward={metrics['mean_step_reward']:.4f} | "
            f"tput={metrics['mean_throughput_bps']:.0f} | "
            f"blk={metrics['mean_blocking_rate']:.4f} | "
            f"HO={metrics['total_handover_count']}"
        )

    # Aggregate
    rewards_list = [m["mean_step_reward"] for m in all_eval_metrics]
    tputs = [m["mean_throughput_bps"] for m in all_eval_metrics]
    blks = [m["mean_blocking_rate"] for m in all_eval_metrics]
    hos = [m["total_handover_count"] for m in all_eval_metrics]

    results["summary"] = {
        "mean_step_reward": float(np.mean(rewards_list)),
        "std_step_reward": float(np.std(rewards_list)),
        "mean_throughput_bps": float(np.mean(tputs)),
        "std_throughput_bps": float(np.std(tputs)),
        "mean_blocking_rate": float(np.mean(blks)),
        "std_blocking_rate": float(np.std(blks)),
        "mean_handover_count": float(np.mean(hos)),
        "std_handover_count": float(np.std(hos)),
        "train_reward_final_10": float(np.mean(ep_rewards[-10:])),
        "train_time_s": round(train_time, 1),
    }

    s = results["summary"]
    print(f"\n{'='*60}")
    print(f"B3 PPO Summary ({NUM_EVAL_SEEDS} eval seeds)")
    print(f"{'='*60}")
    print(f"  Step Reward : {s['mean_step_reward']:.4f} +/- {s['std_step_reward']:.4f}")
    print(f"  Throughput  : {s['mean_throughput_bps']:.0f} +/- {s['std_throughput_bps']:.0f} bps")
    print(f"  Blocking    : {s['mean_blocking_rate']:.4f} +/- {s['std_blocking_rate']:.4f}")
    print(f"  Handovers   : {s['mean_handover_count']:.1f} +/- {s['std_handover_count']:.1f}")
    print(f"  Train reward (last 10 eps avg): {s['train_reward_final_10']:.4f}")

    # Save results
    results_dir = PROJECT_ROOT / "results"
    results_dir.mkdir(exist_ok=True)
    out_path = results_dir / "b3_ppo_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
