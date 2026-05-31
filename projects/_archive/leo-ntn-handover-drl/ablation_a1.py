"""A1 Ablation: Flat FC + Top-K (no attention).

Isolates DLA contribution: same input (candidates + load_stats),
but FC per satellite instead of cross-attention context.
"""

import json
import sys
import time
from collections import deque
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import config as cfg
from simulator.environment import LEOSatHandoverEnv
from la_ddqn import topk_preprocess, LAReplayBuffer

# ── Config ─────────────────────────────────────────────────────────────────────
K = 8
FEAT_DIM = 4
LOAD_DIM = 4
HIDDEN = (256, 128)
LR = 1e-3
GAMMA = 0.99
EPS_START = 1.0
EPS_END = 0.01
EPS_DECAY_EP = 20
BUFFER_SIZE = 100_000
BATCH_SIZE = 256
TARGET_UPDATE = 1000
NUM_EPISODES = 100
EVAL_SEEDS = [100, 200, 300]

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
NUM_UES = cfg.NUM_UES
NUM_SATS = cfg.NUM_PLANES * cfg.SATS_PER_PLANE


class FlatFCNetwork(nn.Module):
    """A1: FC per satellite (no attention), load_stats broadcast to each sat."""

    def __init__(self, feat_dim=FEAT_DIM, load_dim=LOAD_DIM, k=K, hidden=HIDDEN):
        super().__init__()
        self.k = k
        self.shared = nn.Sequential(
            nn.Linear(feat_dim + load_dim, hidden[0]),
            nn.ReLU(),
            nn.Linear(hidden[0], hidden[1]),
            nn.ReLU(),
        )
        self.value_stream = nn.Linear(hidden[1], 1)
        self.advantage_stream = nn.Linear(hidden[1], 1)

    def forward(self, candidates, load_stats):
        ls_exp = load_stats.unsqueeze(1).expand(-1, self.k, -1)
        x = torch.cat([candidates, ls_exp], dim=-1)
        h = self.shared(x)
        value = self.value_stream(h.mean(dim=1))
        advantage = self.advantage_stream(h).squeeze(-1)
        return value + advantage - advantage.mean(dim=-1, keepdim=True)


def run_episode(env, network, eps, seed):
    obs = env.reset(seed=seed)
    transitions = []
    episode_reward = 0.0
    done = False

    while not done:
        valid_mask = env.get_valid_actions()
        sat_actions = np.zeros(env.num_ues, dtype=int)
        ue_data = []

        for ue in range(env.num_ues):
            cands, lstats, sat_idx, valid_k = topk_preprocess(obs[ue])
            cands_t = torch.FloatTensor(cands).unsqueeze(0).to(DEVICE)
            lstats_t = torch.FloatTensor(lstats).unsqueeze(0).to(DEVICE)
            with torch.no_grad():
                q = network(cands_t, lstats_t).squeeze(0).cpu().numpy()
            q[~valid_k] = -float('inf')

            if np.random.random() < eps:
                v = np.where(valid_k)[0]
                act_k = np.random.choice(v) if len(v) > 0 else 0
            else:
                act_k = int(q.argmax())

            sat_actions[ue] = sat_idx[act_k]
            ue_data.append((cands, lstats, act_k))

        next_obs, rewards, done, info = env.step(sat_actions)

        for ue in range(env.num_ues):
            cands, lstats, act_k = ue_data[ue]
            next_cands, next_lstats, _, next_valid = topk_preprocess(next_obs[ue])
            transitions.append((cands, lstats, act_k, rewards[ue],
                                next_cands, next_lstats, next_valid, done))

        episode_reward += float(rewards.sum())
        obs = next_obs

    return transitions, episode_reward


def train(env, network, target_net, optimizer, buffer, num_episodes, seed):
    total_steps = 0
    episode_rewards = []
    episode_losses = []

    for ep in range(num_episodes):
        if ep < EPS_DECAY_EP:
            eps = EPS_START - (EPS_START - EPS_END) * ep / EPS_DECAY_EP
        else:
            eps = EPS_END

        transitions, ep_reward = run_episode(env, network, eps, seed=seed)
        episode_rewards.append(ep_reward)

        for t in transitions:
            buffer.push(*t)

        ep_loss = 0.0
        n_updates = 0
        if len(buffer) >= BATCH_SIZE:
            n_upd = max(1, len(transitions) // BATCH_SIZE)
            for _ in range(n_upd):
                c, ls, a, r, nc, nls, nv, d = buffer.sample(BATCH_SIZE)
                c_t = torch.FloatTensor(c).to(DEVICE)
                ls_t = torch.FloatTensor(ls).to(DEVICE)
                a_t = torch.LongTensor(a).unsqueeze(1).to(DEVICE)
                r_t = torch.FloatTensor(r).to(DEVICE)
                nc_t = torch.FloatTensor(nc).to(DEVICE)
                nls_t = torch.FloatTensor(nls).to(DEVICE)
                nv_t = torch.BoolTensor(nv).to(DEVICE)
                d_t = torch.FloatTensor(d).to(DEVICE)

                q_values = network(c_t, ls_t).gather(1, a_t).squeeze(1)

                with torch.no_grad():
                    next_q_online = network(nc_t, nls_t)
                    next_q_online[~nv_t] = -float('inf')
                    next_actions = next_q_online.argmax(dim=1, keepdim=True)
                    next_q_target = target_net(nc_t, nls_t).gather(1, next_actions).squeeze(1)
                    target_q = r_t + GAMMA * next_q_target * (1.0 - d_t)

                loss = nn.SmoothL1Loss()(q_values, target_q)
                optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(network.parameters(), 10.0)
                optimizer.step()

                ep_loss += loss.item()
                n_updates += 1
                total_steps += 1

                if total_steps % TARGET_UPDATE == 0:
                    target_net.load_state_dict(network.state_dict())

        avg_loss = ep_loss / max(n_updates, 1)
        episode_losses.append(avg_loss)

        if (ep + 1) % 10 == 0:
            recent = episode_rewards[-10:]
            print(f"  ep {ep + 1:3d}/{num_episodes} | "
                  f"avg_reward={np.mean(recent):.1f} | "
                  f"eps={eps:.3f} | "
                  f"loss={avg_loss:.4f} | "
                  f"buf={len(buffer)}")

    return episode_rewards, episode_losses


def evaluate(env, network, seed):
    network.eval()
    obs = env.reset(seed=seed)
    throughputs, blockings = [], []
    ho_count = 0
    done = False

    while not done:
        valid_mask = env.get_valid_actions()
        actions = np.zeros(env.num_ues, dtype=int)
        for ue in range(env.num_ues):
            cands, lstats, sat_idx, valid_k = topk_preprocess(obs[ue])
            cands_t = torch.FloatTensor(cands).unsqueeze(0).to(DEVICE)
            lstats_t = torch.FloatTensor(lstats).unsqueeze(0).to(DEVICE)
            with torch.no_grad():
                q = network(cands_t, lstats_t).squeeze(0).cpu().numpy()
            q[~valid_k] = -float('inf')
            actions[ue] = sat_idx[int(q.argmax())]

        obs, rewards, done, info = env.step(actions)
        throughputs.append(float(info['total_throughput_bps']))
        blockings.append(float(info['blocking_rate']))
        ho_count += int(info['handover_count'])

    network.train()
    return {
        'mean_throughput_bps': float(np.mean(throughputs)),
        'mean_blocking_rate': float(np.mean(blockings)),
        'total_handover_count': ho_count,
    }


def main():
    print(f"Device: {DEVICE}")
    print(f"A1 Ablation: Flat FC + Top-K (no attention)")
    env = LEOSatHandoverEnv(num_ues=NUM_UES, seed=42)
    print(f"K={K}, feat_dim={FEAT_DIM}, episodes={NUM_EPISODES}\n")

    torch.manual_seed(42)
    np.random.seed(42)

    network = FlatFCNetwork().to(DEVICE)
    target_net = FlatFCNetwork().to(DEVICE)
    target_net.load_state_dict(network.state_dict())
    target_net.eval()

    n_params = sum(p.numel() for p in network.parameters())
    print(f"Network params: {n_params:,}\n")

    optimizer = optim.Adam(network.parameters(), lr=LR)
    buffer = LAReplayBuffer(BUFFER_SIZE)

    t0 = time.time()
    rewards, losses = train(env, network, target_net, optimizer, buffer,
                            NUM_EPISODES, seed=42)
    train_time = time.time() - t0
    print(f"\nTraining completed in {train_time:.1f}s")

    print("\nEvaluation:")
    eval_results = []
    for seed in EVAL_SEEDS:
        eval_env = LEOSatHandoverEnv(num_ues=NUM_UES, seed=seed)
        metrics = evaluate(eval_env, network, seed=seed)
        metrics['eval_seed'] = seed
        eval_results.append(metrics)
        print(f"  seed={seed}: tput={metrics['mean_throughput_bps'] / 1e9:.2f} Gbps | "
              f"blk={metrics['mean_blocking_rate']:.4f} | "
              f"HO={metrics['total_handover_count']}")

    results = {
        'method': 'A1-FlatFC-TopK',
        'train': {
            'episode_rewards': [float(r) for r in rewards],
            'episode_losses': [float(l) for l in losses],
            'train_time_s': round(train_time, 1),
            'last10_avg_reward': float(np.mean(rewards[-10:])),
        },
        'eval': eval_results,
        'config': {
            'K': K, 'num_params': n_params,
            'episodes': NUM_EPISODES, 'lr': LR,
        },
    }
    results_dir = PROJECT_ROOT / 'results'
    results_dir.mkdir(exist_ok=True)
    out_path = results_dir / 'a1_flatfc_results.json'
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")


if __name__ == '__main__':
    main()
