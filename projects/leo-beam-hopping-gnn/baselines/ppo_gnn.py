"""PPO+GNN — main method for Beam Hopping with graph neural network encoder.

GNN captures spatial interference coupling between beams via GCN message passing.
Compared against PPO+MLP (flat encoder) to isolate GNN's contribution.
"""
import sys
sys.path.insert(0, "projects/leo-beam-hopping-gnn")

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from simulator.env import BHEnv
from baselines.ppo_mlp import RunningNormalizer, compute_gae

# ---------------------------------------------------------------------------
# Hyperparameters (same as PPO+MLP for fair comparison)
# ---------------------------------------------------------------------------
GAMMA = 0.99
GAE_LAMBDA = 0.95
CLIP_RATIO = 0.2
ENTROPY_COEF = 0.02
LR = 3e-4
PPO_EPOCHS = 4
MINI_BATCH = 64
BATCH_EPISODES = 10
TRAIN_UPDATES = 200
EVAL_EPISODES = 30
GCN_DIM1 = 128
GCN_DIM2 = 64


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------
def build_adjacency(env):
    """Build normalized adjacency from gain matrix for GCN."""
    gain = env.gain_matrix.copy()
    # Symmetric: A[i,j] = max(gain[i,j], gain[j,i])
    A = np.maximum(gain, gain.T)
    np.fill_diagonal(A, 0)
    # Normalize off-diagonal to [0, 1]
    off_max = A.max()
    if off_max > 0:
        A = A / off_max
    # Add self-loops with weight 1
    A_hat = A + np.eye(env.N)
    # D^(-1/2) A_hat D^(-1/2) normalization
    D = A_hat.sum(axis=1)
    D_inv_sqrt = np.diag(1.0 / np.sqrt(np.maximum(D, 1e-8)))
    A_norm = D_inv_sqrt @ A_hat @ D_inv_sqrt
    return torch.from_numpy(A_norm.astype(np.float32))


# ---------------------------------------------------------------------------
# GCN Layer
# ---------------------------------------------------------------------------
class GCNLayer(nn.Module):
    def __init__(self, in_dim, out_dim):
        super().__init__()
        self.W = nn.Parameter(torch.randn(in_dim, out_dim) * (2.0 / in_dim) ** 0.5)
        self.b = nn.Parameter(torch.zeros(out_dim))

    def forward(self, X, A_norm):
        """X: (batch, N, in_dim) or (N, in_dim), A_norm: (N, N)."""
        if X.dim() == 2:
            AX = A_norm @ X          # (N, in_dim)
            return AX @ self.W + self.b
        batch = X.size(0)
        A_exp = A_norm.unsqueeze(0).expand(batch, -1, -1)
        AX = torch.bmm(A_exp, X)     # (batch, N, in_dim)
        return AX @ self.W + self.b  # (batch, N, out_dim)


# ---------------------------------------------------------------------------
# Networks
# ---------------------------------------------------------------------------
class GNNActor(nn.Module):
    def __init__(self, n_beams, obs_dim, A_norm):
        super().__init__()
        self.register_buffer('A_norm', A_norm)
        self.gcn1 = GCNLayer(obs_dim, GCN_DIM1)
        self.gcn2 = GCNLayer(GCN_DIM1, GCN_DIM2)
        self.head = nn.Linear(GCN_DIM2, 1)
        self.log_std = nn.Parameter(torch.full((n_beams,), -1.0))

    def _encode(self, x):
        h = torch.relu(self.gcn1(x, self.A_norm))
        h = torch.relu(self.gcn2(h, self.A_norm))
        return self.head(h).squeeze(-1)  # (..., N)

    def forward(self, x):
        mean = self._encode(x)
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
        return self._encode(x)


class GNNCritic(nn.Module):
    def __init__(self, obs_dim, A_norm):
        super().__init__()
        self.register_buffer('A_norm', A_norm)
        self.gcn1 = GCNLayer(obs_dim, GCN_DIM1)
        self.gcn2 = GCNLayer(GCN_DIM1, GCN_DIM2)
        self.head = nn.Sequential(
            nn.Linear(GCN_DIM2, 128), nn.ReLU(),
            nn.Linear(128, 1),
        )

    def forward(self, x):
        h = torch.relu(self.gcn1(x, self.A_norm))
        h = torch.relu(self.gcn2(h, self.A_norm))
        h_pool = h.mean(dim=-2)  # global mean pool over nodes → (..., GCN_DIM2)
        return self.head(h_pool).squeeze(-1)


# ---------------------------------------------------------------------------
# PPO update (same logic as ppo_mlp, handles GNN batch shapes)
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
        o_norm = obs_norm.normalize(o_raw).reshape(env.N, 4)
        o_t = torch.from_numpy(o_norm).float().unsqueeze(0)  # (1, N, 4)
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
    return (np.array(obs_list), np.array(act_list),
            np.array(logp_list), np.array(rew_list), np.array(done_list))


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------
def train():
    env = BHEnv()
    N = env.N
    obs_dim = 4  # per-node features
    A_norm = build_adjacency(env)

    actor = GNNActor(N, obs_dim, A_norm)
    critic = GNNCritic(obs_dim, A_norm)
    opt_a = optim.Adam(actor.parameters(), lr=LR)
    opt_c = optim.Adam(critic.parameters(), lr=LR)
    obs_norm = RunningNormalizer(N * 4)

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
            obs_norm.update(obs_ep.reshape(-1, N * 4))

        episode_rewards.extend(update_rewards)

        batch_obs = np.concatenate(all_obs)     # (steps, N, 4)
        batch_act = np.concatenate(all_act)
        batch_logp = np.concatenate(all_logp)
        batch_rew = np.concatenate(all_rew)
        batch_done = np.concatenate(all_done)

        obs_t = torch.from_numpy(batch_obs).float()
        with torch.no_grad():
            values = critic(obs_t).numpy()

        advantages, returns = compute_gae(batch_rew, values, batch_done)

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
                  f"avg(last100)={avg:8.4f} | batch={np.mean(update_rewards):8.4f} | "
                  f"p_loss={a_loss:+.4f} v_loss={c_loss:.4f}")

    return actor, critic, obs_norm, np.array(episode_rewards)


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
            o_norm = obs_norm.normalize(obs.flatten()).reshape(env.N, 4)
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
        results.append({'total': total_r, 'throughput': tp_sum,
                        'fairness': fa_sum, 'interference': intf_sum})
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
    print("PPO+GNN — Beam Hopping (GCN encoder)")
    print(f"Batch={BATCH_EPISODES} eps/update, Updates={TRAIN_UPDATES}")
    print("=" * 60)

    print(f"\nTraining ...")
    actor, critic, obs_norm, train_rewards = train()

    print(f"\nEvaluating for {EVAL_EPISODES} episodes ...")
    eval_results = evaluate(actor, obs_norm)
    eval_totals = summarize(eval_results, "PPO+GNN")

    # Save
    model_path = "projects/leo-beam-hopping-gnn/results/ppo_gnn_model.pt"
    torch.save({
        'actor': actor.state_dict(),
        'A_norm': actor.A_norm,
        'obs_norm': obs_norm.state_dict(),
    }, model_path)
    print(f"\nModel saved to {model_path}")

    out_path = "projects/leo-beam-hopping-gnn/results/ppo_gnn_training.npz"
    np.savez(out_path, episode_rewards=train_rewards,
             eval_mean=np.array([eval_totals.mean()]))
    print(f"Training curve saved to {out_path}")
    print("=" * 60)
