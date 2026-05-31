"""PPO+MLP baseline for Beam Hopping environment.

Fixed: batch collection (10 eps/update), obs normalization, 2000 episodes.
"""
import sys
sys.path.insert(0, "projects/leo-beam-hopping-gnn")

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from simulator.env import BHEnv

# ---------------------------------------------------------------------------
# Hyperparameters
# ---------------------------------------------------------------------------
GAMMA = 0.99
GAE_LAMBDA = 0.95
CLIP_RATIO = 0.2
ENTROPY_COEF = 0.02
LR = 3e-4
PPO_EPOCHS = 4
MINI_BATCH = 64
BATCH_EPISODES = 10       # collect 10 eps before each update
TRAIN_UPDATES = 200       # 200 updates × 10 eps = 2000 episodes
HIDDEN = 128
EVAL_EPISODES = 30


# ---------------------------------------------------------------------------
# Observation normalization
# ---------------------------------------------------------------------------
class RunningNormalizer:
    def __init__(self, dim):
        self.mean = np.zeros(dim, dtype=np.float32)
        self.var = np.ones(dim, dtype=np.float32)
        self.count = 1e-4

    def update(self, x):
        batch_mean = x.mean(axis=0)
        batch_var = x.var(axis=0)
        batch_count = x.shape[0]
        delta = batch_mean - self.mean
        total = self.count + batch_count
        self.mean += delta * batch_count / total
        m2 = self.var * self.count + batch_var * batch_count + delta**2 * self.count * batch_count / total
        self.var = m2 / total
        self.count = total

    def normalize(self, x):
        return (x - self.mean) / (np.sqrt(self.var) + 1e-8)

    def state_dict(self):
        return {'mean': self.mean.copy(), 'var': self.var.copy(), 'count': self.count}

    def load_state_dict(self, d):
        self.mean = d['mean']
        self.var = d['var']
        self.count = d['count']


# ---------------------------------------------------------------------------
# Networks
# ---------------------------------------------------------------------------
def _orthogonal_init(module):
    if isinstance(module, nn.Linear):
        nn.init.orthogonal_(module.weight)
        nn.init.zeros_(module.bias)


class Actor(nn.Module):
    def __init__(self, obs_dim, act_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, HIDDEN), nn.Tanh(),
            nn.Linear(HIDDEN, HIDDEN), nn.Tanh(),
            nn.Linear(HIDDEN, act_dim),
        )
        self.log_std = nn.Parameter(torch.full((act_dim,), -1.0))
        self.net.apply(_orthogonal_init)

    def forward(self, x):
        mean = self.net(x)
        std = torch.exp(self.log_std.clamp(-5, 2))
        return mean, std

    def get_dist(self, x):
        mean, std = self.forward(x)
        return torch.distributions.Normal(mean, std)

    def sample(self, x):
        dist = self.get_dist(x)
        action = dist.sample()
        log_prob = dist.log_prob(action).sum(-1)
        return action, log_prob

    def deterministic(self, x):
        mean, _ = self.forward(x)
        return mean


class Critic(nn.Module):
    def __init__(self, obs_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, HIDDEN), nn.Tanh(),
            nn.Linear(HIDDEN, HIDDEN), nn.Tanh(),
            nn.Linear(HIDDEN, 1),
        )
        self.net.apply(_orthogonal_init)

    def forward(self, x):
        return self.net(x).squeeze(-1)


# ---------------------------------------------------------------------------
# GAE
# ---------------------------------------------------------------------------
def compute_gae(rewards, values, dones, gamma=GAMMA, lam=GAE_LAMBDA):
    T = len(rewards)
    advantages = np.zeros(T, dtype=np.float32)
    returns = np.zeros(T, dtype=np.float32)
    gae = 0.0
    next_value = 0.0
    for t in reversed(range(T)):
        if dones[t]:
            delta = rewards[t] - values[t]
            gae = delta
        else:
            delta = rewards[t] + gamma * next_value - values[t]
            gae = delta + gamma * lam * gae
        advantages[t] = gae
        returns[t] = gae + values[t]
        next_value = values[t]
    return advantages, returns


# ---------------------------------------------------------------------------
# PPO update
# ---------------------------------------------------------------------------
def ppo_update(actor, critic, opt_a, opt_c,
               obs_b, act_b, old_logp_b, ret_b, adv_b):
    adv_b = (adv_b - adv_b.mean()) / (adv_b.std() + 1e-8)
    bs = obs_b.shape[0]
    mb_size = min(MINI_BATCH, bs)

    for _ in range(PPO_EPOCHS):
        indices = torch.randperm(bs)
        for start in range(0, bs, mb_size):
            idx = indices[start:start + mb_size]
            b_obs, b_act, b_old_lp = obs_b[idx], act_b[idx], old_logp_b[idx]
            b_ret, b_adv = ret_b[idx], adv_b[idx]

            dist = actor.get_dist(b_obs)
            new_logp = dist.log_prob(b_act).sum(-1)
            ratio = torch.exp(new_logp - b_old_lp)
            surr1 = ratio * b_adv
            surr2 = torch.clamp(ratio, 1 - CLIP_RATIO, 1 + CLIP_RATIO) * b_adv
            entropy = dist.entropy().sum(-1).mean()
            actor_loss = -torch.min(surr1, surr2).mean() - ENTROPY_COEF * entropy

            opt_a.zero_grad()
            actor_loss.backward()
            nn.utils.clip_grad_norm_(actor.parameters(), 0.5)
            opt_a.step()

            val = critic(b_obs)
            critic_loss = nn.functional.mse_loss(val, b_ret)
            opt_c.zero_grad()
            critic_loss.backward()
            nn.utils.clip_grad_norm_(critic.parameters(), 0.5)
            opt_c.step()

    return actor_loss.item(), critic_loss.item()


# ---------------------------------------------------------------------------
# Episode collection
# ---------------------------------------------------------------------------
def collect_episode(env, actor, obs_norm, seed):
    obs_list, act_list, logp_list, rew_list, done_list = [], [], [], [], []
    obs, _ = env.reset(seed=seed)
    for _ in range(env.T):
        o_raw = obs.flatten()
        o_norm = obs_norm.normalize(o_raw)
        o_t = torch.from_numpy(o_norm).float().unsqueeze(0)
        with torch.no_grad():
            a, lp = actor.sample(o_t)
        action = a.squeeze(0).numpy()
        obs_next, reward, terminated, truncated, info = env.step(action)
        obs_list.append(o_norm)
        act_list.append(action)
        logp_list.append(lp.item())
        rew_list.append(reward)
        done_list.append(terminated)
        obs = obs_next
        if terminated:
            break
    # Update normalizer with raw obs from this episode
    raw_obs = np.array([obs_list[i] for i in range(len(obs_list))])  # already normalized
    return (np.array(obs_list), np.array(act_list),
            np.array(logp_list), np.array(rew_list), np.array(done_list))


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------
def train():
    env = BHEnv()
    N = env.N
    obs_dim = N * 4
    act_dim = N

    actor = Actor(obs_dim, act_dim)
    critic = Critic(obs_dim)
    opt_a = optim.Adam(actor.parameters(), lr=LR)
    opt_c = optim.Adam(critic.parameters(), lr=LR)
    obs_norm = RunningNormalizer(obs_dim)

    episode_rewards = []
    global_ep = 0

    for update in range(1, TRAIN_UPDATES + 1):
        all_obs, all_act, all_logp, all_rew, all_done = [], [], [], [], []
        update_rewards = []

        for _ in range(BATCH_EPISODES):
            global_ep += 1
            ep_data = collect_episode(env, actor, obs_norm, seed=global_ep * 7)
            obs_ep, act_ep, logp_ep, rew_ep, done_ep = ep_data
            all_obs.append(obs_ep)
            all_act.append(act_ep)
            all_logp.append(logp_ep)
            all_rew.append(rew_ep)
            all_done.append(done_ep)
            update_rewards.append(rew_ep.sum())

            # Update obs normalizer with raw obs
            obs_norm.update(obs_ep)

        episode_rewards.extend(update_rewards)

        # Concatenate batch
        batch_obs = np.concatenate(all_obs)
        batch_act = np.concatenate(all_act)
        batch_logp = np.concatenate(all_logp)
        batch_rew = np.concatenate(all_rew)
        batch_done = np.concatenate(all_done)

        # Compute values
        obs_t = torch.from_numpy(batch_obs).float()
        with torch.no_grad():
            values = critic(obs_t).numpy()

        advantages, returns = compute_gae(batch_rew, values, batch_done)

        # PPO update
        a_loss, c_loss = ppo_update(
            actor, critic, opt_a, opt_c,
            obs_t,
            torch.from_numpy(batch_act).float(),
            torch.from_numpy(batch_logp).float(),
            torch.from_numpy(returns).float(),
            torch.from_numpy(advantages).float(),
        )

        if update % 20 == 0:
            recent = episode_rewards[-100:]
            avg = np.mean(recent)
            print(f"Update {update:3d} | ep={global_ep:4d} | "
                  f"avg_reward(last100)={avg:8.4f} | "
                  f"batch_mean={np.mean(update_rewards):8.4f} | "
                  f"p_loss={a_loss:+.4f} v_loss={c_loss:.4f}")

    return actor, critic, obs_norm, np.array(episode_rewards)


# ---------------------------------------------------------------------------
# PPOAgent wrapper (for evaluate.py compatibility)
# ---------------------------------------------------------------------------
class PPOAgent:
    def __init__(self, env=None, obs_dim=None, act_dim=None):
        if env is not None:
            self.obs_dim = env.N * 4
            self.act_dim = env.N
        else:
            self.obs_dim = obs_dim or 76
            self.act_dim = act_dim or 19
        self.actor = Actor(self.obs_dim, self.act_dim)
        self.obs_norm = RunningNormalizer(self.obs_dim)

    def act(self, obs):
        """Deterministic action for evaluation. Signature: act(obs) -> action."""
        o_norm = self.obs_norm.normalize(obs.flatten())
        o_t = torch.from_numpy(o_norm).float().unsqueeze(0)
        with torch.no_grad():
            action = self.actor.deterministic(o_t).squeeze(0).numpy()
        return action

    def save(self, path):
        torch.save({
            'actor': self.actor.state_dict(),
            'obs_norm': self.obs_norm.state_dict(),
        }, path)

    def load(self, path):
        ckpt = torch.load(path, weights_only=False)
        self.actor.load_state_dict(ckpt['actor'])
        self.obs_norm.load_state_dict(ckpt['obs_norm'])


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------
def evaluate(actor, obs_norm, n_episodes=EVAL_EPISODES, seed_start=10000):
    env = BHEnv()
    results = []
    for ep in range(n_episodes):
        obs, _ = env.reset(seed=seed_start + ep * 13)
        total_r = 0.0
        tp_sum, fa_sum, intf_sum = 0.0, 0.0, 0.0
        for _ in range(env.T):
            o_norm = obs_norm.normalize(obs.flatten())
            o_t = torch.from_numpy(o_norm).float().unsqueeze(0)
            with torch.no_grad():
                action = actor.deterministic(o_t).squeeze(0).numpy()
            obs, reward, terminated, truncated, info = env.step(action)
            total_r += reward
            tp_sum += info['reward_throughput']
            fa_sum += info['reward_fairness']
            intf_sum += info['penalty_interference']
            if terminated:
                break
        results.append({
            'total': total_r,
            'throughput': tp_sum,
            'fairness': fa_sum,
            'interference': intf_sum,
        })
    return results


def summarize(results, name=""):
    totals = np.array([r['total'] for r in results])
    tp = np.array([r['throughput'] for r in results])
    fa = np.array([r['fairness'] for r in results])
    intf = np.array([r['interference'] for r in results])
    print(f"  [{name}] total={totals.mean():.4f}+/-{totals.std():.4f} "
          f"tp={tp.mean():.4f} fair={fa.mean():.4f} intf={intf.mean():.4f}")
    return totals


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("PPO+MLP Baseline for Beam Hopping (v2 — batch training)")
    print(f"Batch={BATCH_EPISODES} eps/update, Updates={TRAIN_UPDATES}, "
          f"Total eps={BATCH_EPISODES * TRAIN_UPDATES}")
    print("=" * 60)

    print(f"\nTraining ...")
    actor, critic, obs_norm, train_rewards = train()

    print(f"\nEvaluating trained policy for {EVAL_EPISODES} episodes ...")
    eval_results = evaluate(actor, obs_norm)
    eval_totals = summarize(eval_results, "PPO+MLP trained")

    # Save model for evaluate.py
    agent = PPOAgent(obs_dim=actor.net[0].in_features, act_dim=actor.log_std.shape[0])
    agent.actor = actor
    agent.obs_norm = obs_norm
    model_path = "projects/leo-beam-hopping-gnn/results/ppo_mlp_model.pt"
    agent.save(model_path)
    print(f"\nModel saved to {model_path}")

    # Save training curve
    out_path = "projects/leo-beam-hopping-gnn/results/ppo_mlp_training.npz"
    np.savez(out_path,
             episode_rewards=train_rewards,
             eval_mean=np.array([eval_totals.mean()]))
    print(f"Training curve saved to {out_path}")
    print("=" * 60)
