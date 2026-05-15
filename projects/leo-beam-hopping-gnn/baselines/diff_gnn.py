"""Differentiable GNN for Beam Hopping — supervised optimization without RL.

Core idea: GNN outputs per-beam scores → sigmoid relaxation → differentiable
reward (throughput + interference). Gradients flow directly from loss to GNN
parameters, avoiding RL's credit assignment problem.

Training: soft selection (sigmoid weights), temperature annealing.
Evaluation: hard top-K selection.
"""
import sys
sys.path.insert(0, "projects/leo-beam-hopping-gnn")

import argparse
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from simulator.env import BHEnv
from simulator.config import SimConfig
from baselines.ppo_gnn import GCNLayer, build_adjacency

# ---------------------------------------------------------------------------
# Hyperparameters
# ---------------------------------------------------------------------------
HIDDEN_DIM = 128
GNN_LAYERS = 2
LR = 1e-3
BATCH_EPISODES = 16
TRAIN_EPOCHS = 200
EVAL_EPISODES = 30
TAU_START = 2.0
TAU_END = 0.1
LAMBDA_INTERF = 1.0  # interference penalty multiplier (matched to env γ)
BASELINE_DECAY = 0.99  # running baseline EMA


# ---------------------------------------------------------------------------
# GNN Score Network
# ---------------------------------------------------------------------------
class BeamScoreNet(nn.Module):
    """GNN that outputs per-beam activation scores."""

    def __init__(self, obs_dim, hidden_dim, A_norm, n_layers=2):
        super().__init__()
        self.register_buffer('A_norm', A_norm)
        layers = []
        in_d = obs_dim
        for _ in range(n_layers):
            layers.append(GCNLayer(in_d, hidden_dim))
            layers.append(nn.ReLU())
            in_d = hidden_dim
        self.gnn = nn.Sequential(*layers) if False else None
        # Manual layer list for proper forward
        self.gcn_layers = nn.ModuleList()
        in_d = obs_dim
        for _ in range(n_layers):
            self.gcn_layers.append(GCNLayer(in_d, hidden_dim))
            in_d = hidden_dim
        self.head = nn.Linear(hidden_dim, 1)

    def forward(self, x, temperature=1.0):
        """
        x: (N, obs_dim) node features
        Returns: soft_weights (N,) in (0, 1)
        """
        h = x
        for layer in self.gcn_layers:
            h = torch.relu(layer(h, self.A_norm))
        scores = self.head(h).squeeze(-1)  # (N,)
        return torch.sigmoid(scores / temperature), scores


# ---------------------------------------------------------------------------
# Differentiable reward computation
# ---------------------------------------------------------------------------
def diff_reward(soft_weights, gain_matrix_t, demands, queues, fading, config):
    """Compute differentiable reward matching env's 3-component structure.

    Mirrors env.py step(): α·R_throughput + β·R_fairness - γ·P_interference.
    All components normalized to [0, 1] range for stable gradients.

    Returns:
        reward: scalar tensor (composite reward, higher is better)
        components: dict with individual terms for logging
    """
    eps = 1e-8
    w = soft_weights  # (N,)
    N = w.shape[0]

    # --- SINR computation (same physics as env) ---
    P = config.p_max_linear
    signal = w * P * torch.diag(gain_matrix_t) * fading  # (N,)
    weighted_gain = w.unsqueeze(0) * gain_matrix_t * P    # (N, N)
    interference_per_beam = weighted_gain.sum(dim=1) - w * P * torch.diag(gain_matrix_t)
    sinr = signal / (interference_per_beam + config.noise_power_linear)

    # --- Capacity ---
    capacity = config.bandwidth_hz * torch.log2(1.0 + sinr) / 1e6  # (N,) Mbps

    # --- Throughput reward (fraction of active demand served) ---
    total_demand = demands + queues
    served = torch.minimum(capacity, w * total_demand)  # (N,)
    active_demand = (w * total_demand).sum()
    r_throughput = served.sum() / (active_demand + eps)

    # --- Fairness reward (Jain-like on satisfaction, weighted by activation) ---
    satisfaction = served / (w * total_demand + eps)  # (N,)
    s_w = w * satisfaction
    s_w_sq = w * satisfaction ** 2
    w_sum = w.sum()
    r_fairness = s_w.sum() ** 2 / (w_sum * s_w_sq.sum() + eps)

    # --- Interference penalty (SINR deficit, matches env) ---
    sinr_thr = 10 ** (config.sinr_threshold_db / 10)
    deficit = torch.clamp(sinr_thr - sinr, min=0)
    p_interference = (w * deficit).sum() / (w_sum * sinr_thr + eps)

    # --- Composite reward (same weights as env) ---
    reward = (config.reward_alpha * r_throughput
              + config.reward_beta * r_fairness
              - config.reward_gamma * p_interference)

    components = {
        'throughput': r_throughput.item(),
        'fairness': r_fairness.item(),
        'interference': p_interference.item(),
        'reward': reward.item(),
    }
    return reward, components


# ---------------------------------------------------------------------------
# Training — REINFORCE with softmax scores
# ---------------------------------------------------------------------------
def train(config):
    env = BHEnv(config=config)
    N = env.N
    obs_dim = 4

    A_norm = build_adjacency(env)
    model = BeamScoreNet(obs_dim, HIDDEN_DIM, A_norm, GNN_LAYERS)
    optimizer = optim.Adam(model.parameters(), lr=LR)

    episode_rewards = []
    baseline = 0.0

    for epoch in range(TRAIN_EPOCHS):
        epoch_loss = 0.0
        epoch_env_r = 0.0
        epoch_logp = 0.0

        for ep in range(BATCH_EPISODES):
            obs, _ = env.reset(seed=epoch * BATCH_EPISODES + ep + 1)
            ep_loss = 0.0
            ep_env_r = 0.0

            for slot in range(env.T):
                obs_t = torch.from_numpy(obs).float()

                # GNN forward → raw scores
                _, scores = model(obs_t, temperature=1.0)  # scores unused for soft

                # Softmax log-probabilities (gradient signal for ALL beams)
                log_probs = torch.log_softmax(scores, dim=0)  # (N,)

                # Hard top-K selection for env step
                with torch.no_grad():
                    topk_idx = torch.topk(scores, env.K).indices
                action = scores.detach().numpy()
                obs, reward, terminated, truncated, info = env.step(action)

                # REINFORCE: log_prob of selected beams
                selected_logp = log_probs[topk_idx].sum()
                advantage = reward - baseline
                ep_loss += -advantage * selected_logp
                ep_env_r += reward

                if terminated:
                    break

            epoch_loss += ep_loss
            episode_rewards.append(ep_env_r)
            # Update baseline after each episode
            baseline = BASELINE_DECAY * baseline + (1 - BASELINE_DECAY) * ep_env_r

        # Backprop
        optimizer.zero_grad()
        total_loss = epoch_loss / BATCH_EPISODES
        total_loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()

        if (epoch + 1) % 20 == 0:
            recent = episode_rewards[-100:]
            avg_r = np.mean(recent)
            print(f"Epoch {epoch+1:3d} | loss={total_loss.item():.4f} | "
                  f"baseline={baseline:.4f} | env_r={avg_r:.4f}")

    return model, np.array(episode_rewards)


# ---------------------------------------------------------------------------
# Evaluation (hard top-K)
# ---------------------------------------------------------------------------
def evaluate(model, config, n_episodes=EVAL_EPISODES, seed_start=10000):
    env = BHEnv(config=config)
    results = []
    for ep in range(n_episodes):
        obs, _ = env.reset(seed=seed_start + ep * 13)
        total_r = 0.0
        tp_sum, fa_sum, intf_sum = 0.0, 0.0, 0.0
        for _ in range(env.T):
            obs_t = torch.from_numpy(obs).float()
            with torch.no_grad():
                _, scores = model(obs_t, temperature=0.1)
            action = scores.numpy()
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
    print(f"  [{name}] total={totals.mean():.4f}±{totals.std():.4f} "
          f"tp={tp.mean():.4f} fair={fa.mean():.4f} intf={intf.mean():.4f}")
    return totals


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--scale', default='medium', choices=['small', 'medium', 'large'])
    args = parser.parse_args()

    cfg = SimConfig.preset(args.scale)
    tag = f"N={cfg.n_beams}_K={cfg.k_active}"
    print("=" * 60)
    print(f"DiffGNN(REINFORCE) — Beam Hopping ({tag})")
    print(f"Epochs={TRAIN_EPOCHS}, Batch={BATCH_EPISODES}, LR={LR}")
    print("=" * 60)

    print(f"\nTraining ...")
    model, train_rewards = train(cfg)

    print(f"\nEvaluating for {EVAL_EPISODES} episodes ...")
    eval_results = evaluate(model, cfg)
    eval_totals = summarize(eval_results, f"DiffGNN({tag})")

    # Save
    model_path = f"projects/leo-beam-hopping-gnn/results/diff_gnn_{tag}_model.pt"
    torch.save({
        'model': model.state_dict(),
        'A_norm': model.A_norm,
        'config': {'scale': args.scale, 'n_beams': cfg.n_beams, 'k_active': cfg.k_active},
    }, model_path)
    print(f"\nModel saved to {model_path}")

    out_path = f"projects/leo-beam-hopping-gnn/results/diff_gnn_{tag}_training.npz"
    np.savez(out_path, episode_rewards=train_rewards,
             eval_mean=np.array([eval_totals.mean()]))
    print(f"Training curve saved to {out_path}")
    print("=" * 60)
