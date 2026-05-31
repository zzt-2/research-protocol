"""LA-DDQN: Load-Attention Dueling Double DQN for LEO satellite handover.

Quick validation: 30 episodes, 2 eval seeds.
Architecture: Top-K(8) preprocessing → DLA cross-attention → Dueling Q.
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

# ── Hyperparameters ────────────────────────────────────────────────────────────
K = 8                   # top-K candidates
FEAT_DIM = 4            # [sinr_norm, load_actual, elev_norm, is_svc]
D_ATTN = 64             # attention dimension
HIDDEN = (256, 128)
LR = 1e-3
GAMMA = 0.99
EPS_START = 1.0
EPS_END = 0.01
EPS_DECAY_EP = 20       # linear decay over this many episodes
BUFFER_SIZE = 100_000
BATCH_SIZE = 256
TARGET_UPDATE = 1000
QUICK_EPISODES = 100
EVAL_SEEDS = [100, 200, 300]

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
NUM_UES = cfg.NUM_UES
NUM_SATS = cfg.NUM_PLANES * cfg.SATS_PER_PLANE


# ── Top-K Preprocessor ─────────────────────────────────────────────────────────
def topk_preprocess(flat_obs):
    """Extract top-K candidates from flat observation.

    flat_obs: (obs_dim,) = [sinr(N), avail(N), elev(N), is_current(N), t_conn(1)]
    avail = 1 - load/capacity (higher = more available)

    Returns: candidates(K,4), load_stats(4,), sat_indices(K,), valid(K,)
    """
    sinr = flat_obs[:NUM_SATS]
    elev = flat_obs[NUM_SATS:2 * NUM_SATS]
    avail = flat_obs[2 * NUM_SATS:3 * NUM_SATS]   # avail_norm = 1 - load/cap
    is_cur = flat_obs[3 * NUM_SATS:4 * NUM_SATS]

    load_actual = 1.0 - avail
    visible = elev > 1e-6

    if not visible.any():
        z_cands = np.zeros((K, FEAT_DIM), dtype=np.float32)
        z_stats = np.zeros(4, dtype=np.float32)
        z_idx = np.zeros(K, dtype=np.int64)
        z_valid = np.zeros(K, dtype=bool)
        return z_cands, z_stats, z_idx, z_valid

    score = sinr + elev
    cur_idx = int(np.argmax(is_cur)) if is_cur.any() else -1

    vis_idx = np.where(visible)[0]
    sorted_idx = vis_idx[np.argsort(-score[vis_idx])]

    selected = []
    if cur_idx >= 0 and visible[cur_idx]:
        selected.append(cur_idx)
    for idx in sorted_idx:
        if idx not in selected:
            selected.append(idx)
        if len(selected) >= K:
            break
    while len(selected) < K:
        selected.append(0)

    sat_indices = np.array(selected[:K], dtype=np.int64)

    candidates = np.zeros((K, FEAT_DIM), dtype=np.float32)
    valid = np.zeros(K, dtype=bool)
    for i, si in enumerate(sat_indices):
        candidates[i] = [sinr[si], load_actual[si], elev[si], is_cur[si]]
        valid[i] = visible[si]

    vis_loads = load_actual[visible]
    load_stats = np.array([
        vis_loads.mean(),
        vis_loads.max(),
        vis_loads.std() if len(vis_loads) > 1 else 0.0,
        float(is_cur[visible].any()),
    ], dtype=np.float32)

    return candidates, load_stats, sat_indices, valid


# ── DLA Module ─────────────────────────────────────────────────────────────────
class DLAModule(nn.Module):
    """Load-Driven Attention: cross-attention with load stats as query."""

    def __init__(self, feat_dim=FEAT_DIM, d=D_ATTN):
        super().__init__()
        self.W_q = nn.Linear(4, d)
        self.W_k = nn.Linear(feat_dim, d)
        self.W_v = nn.Linear(feat_dim, d)
        self.scale = d ** 0.5

    def forward(self, candidates, load_stats):
        q = self.W_q(load_stats).unsqueeze(1)
        k = self.W_k(candidates)
        v = self.W_v(candidates)
        attn = torch.softmax(q @ k.transpose(-2, -1) / self.scale, dim=-1)
        ctx = (attn @ v).squeeze(1)
        return ctx, attn.squeeze(1)


class LADDQNNetwork(nn.Module):
    """LA-DDQN: DLA cross-attention → FC → Dueling Q."""

    def __init__(self, feat_dim=FEAT_DIM, k=K, d=D_ATTN, hidden=HIDDEN):
        super().__init__()
        self.k = k
        self.dla = DLAModule(feat_dim, d)
        self.shared = nn.Sequential(
            nn.Linear(feat_dim + d, hidden[0]),
            nn.ReLU(),
            nn.Linear(hidden[0], hidden[1]),
            nn.ReLU(),
        )
        self.value_stream = nn.Linear(hidden[1], 1)
        self.advantage_stream = nn.Linear(hidden[1], 1)

    def forward(self, candidates, load_stats):
        ctx, _ = self.dla(candidates, load_stats)
        ctx_exp = ctx.unsqueeze(1).expand(-1, self.k, -1)
        fused = torch.cat([candidates, ctx_exp], dim=-1)
        h = self.shared(fused)
        value = self.value_stream(h.mean(dim=1))
        advantage = self.advantage_stream(h).squeeze(-1)
        return value + advantage - advantage.mean(dim=-1, keepdim=True)

    def forward_with_attn(self, candidates, load_stats):
        ctx, attn_w = self.dla(candidates, load_stats)
        ctx_exp = ctx.unsqueeze(1).expand(-1, self.k, -1)
        fused = torch.cat([candidates, ctx_exp], dim=-1)
        h = self.shared(fused)
        value = self.value_stream(h.mean(dim=1))
        advantage = self.advantage_stream(h).squeeze(-1)
        q = value + advantage - advantage.mean(dim=-1, keepdim=True)
        return q, attn_w


# ── Replay Buffer ──────────────────────────────────────────────────────────────
class LAReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    def push(self, cands, lstats, act_k, reward,
             next_cands, next_lstats, next_valid, done):
        self.buffer.append((cands, lstats, act_k, reward,
                            next_cands, next_lstats, next_valid, done))

    def sample(self, batch_size):
        idx = np.random.choice(len(self.buffer), batch_size, replace=False)
        batch = [self.buffer[i] for i in idx]
        return (
            np.array([b[0] for b in batch], dtype=np.float32),
            np.array([b[1] for b in batch], dtype=np.float32),
            np.array([b[2] for b in batch], dtype=np.int64),
            np.array([b[3] for b in batch], dtype=np.float32),
            np.array([b[4] for b in batch], dtype=np.float32),
            np.array([b[5] for b in batch], dtype=np.float32),
            np.array([b[6] for b in batch], dtype=bool),
            np.array([b[7] for b in batch], dtype=np.float32),
        )

    def __len__(self):
        return len(self.buffer)


# ── Episode runner ─────────────────────────────────────────────────────────────
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


# ── Training ───────────────────────────────────────────────────────────────────
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

        if (ep + 1) % 5 == 0:
            recent = episode_rewards[-5:]
            print(f"  ep {ep + 1:3d}/{num_episodes} | "
                  f"avg_reward={np.mean(recent):.1f} | "
                  f"eps={eps:.3f} | "
                  f"loss={avg_loss:.4f} | "
                  f"buf={len(buffer)}")

    return episode_rewards, episode_losses


# ── Evaluation ─────────────────────────────────────────────────────────────────
def evaluate(env, network, seed):
    network.eval()
    obs = env.reset(seed=seed)
    throughputs, blockings = [], []
    ho_count = 0
    ue_throughput = np.zeros(env.num_ues)
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
        ue_throughput += info['throughput_bps']

    jain = float(np.sum(ue_throughput) ** 2 /
                 (env.num_ues * np.sum(ue_throughput ** 2) + 1e-12))
    network.train()
    return {
        'mean_throughput_bps': float(np.mean(throughputs)),
        'mean_blocking_rate': float(np.mean(blockings)),
        'total_handover_count': ho_count,
        'jain_fairness': jain,
    }


# ── Attention visualization (debug) ────────────────────────────────────────────
def debug_attention(env, network, seed=42):
    """Print attention weights for one step to verify DLA behavior."""
    network.eval()
    obs = env.reset(seed=seed)
    valid_mask = env.get_valid_actions()

    ue = 0
    cands, lstats, sat_idx, valid_k = topk_preprocess(obs[ue])
    cands_t = torch.FloatTensor(cands).unsqueeze(0).to(DEVICE)
    lstats_t = torch.FloatTensor(lstats).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        q, attn_w = network.forward_with_attn(cands_t, lstats_t)
        q = q.squeeze(0).cpu().numpy()
        attn_w = attn_w.squeeze(0).cpu().numpy()

    print("\n  DLA Attention weights (UE 0):")
    print(f"  load_stats: avg={lstats[0]:.3f} max={lstats[1]:.3f} std={lstats[2]:.3f} has_svc={lstats[3]:.0f}")
    print(f"  {'idx':>3} {'sat':>4} {'sinr':>6} {'load':>6} {'elev':>6} {'svc':>4} {'valid':>5} {'attn':>6} {'Q':>7}")
    for i in range(K):
        print(f"  {i:3d} {sat_idx[i]:4d} {cands[i,0]:6.3f} {cands[i,1]:6.3f} "
              f"{cands[i,2]:6.3f} {cands[i,3]:4.0f} {str(valid_k[i]):>5} "
              f"{attn_w[i]:6.3f} {q[i]:7.3f}")

    network.train()


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    print(f"Device: {DEVICE}")
    env = LEOSatHandoverEnv(num_ues=NUM_UES, seed=42)
    print(f"obs_dim={env.obs_dim}, num_sats={env.num_sats}, K={K}, feat_dim={FEAT_DIM}")
    print(f"Quick run: {QUICK_EPISODES} episodes, {EVAL_SEEDS} eval seeds\n")

    torch.manual_seed(42)
    np.random.seed(42)

    network = LADDQNNetwork().to(DEVICE)
    target_net = LADDQNNetwork().to(DEVICE)
    target_net.load_state_dict(network.state_dict())
    target_net.eval()

    n_params = sum(p.numel() for p in network.parameters())
    print(f"Network params: {n_params:,}\n")

    optimizer = optim.Adam(network.parameters(), lr=LR)
    buffer = LAReplayBuffer(BUFFER_SIZE)

    # Debug attention before training
    print("Before training:")
    debug_attention(env, network)

    # Train
    t0 = time.time()
    rewards, losses = train(env, network, target_net, optimizer, buffer,
                            QUICK_EPISODES, seed=42)
    train_time = time.time() - t0
    print(f"\nTraining completed in {train_time:.1f}s")

    # Debug attention after training
    print("\nAfter training:")
    debug_attention(env, network)

    # Eval
    print("\nEvaluation:")
    eval_results = []
    for seed in EVAL_SEEDS:
        eval_env = LEOSatHandoverEnv(num_ues=NUM_UES, seed=seed)
        metrics = evaluate(eval_env, network, seed=seed)
        metrics['eval_seed'] = seed
        eval_results.append(metrics)
        print(f"  seed={seed}: tput={metrics['mean_throughput_bps']:.0f} bps | "
              f"blk={metrics['mean_blocking_rate']:.4f} | "
              f"HO={metrics['total_handover_count']}")

    # Compare with B2 baseline (from baseline_report.md)
    print(f"\n{'=' * 60}")
    print("Quick Comparison (B2 baseline from baseline_report.md):")
    print(f"  B2 DDQN:  episode reward 3345-4241 (5 ep validation)")
    print(f"  LA-DDQN:  last-5 avg reward = {np.mean(rewards[-5:]):.1f}")
    print(f"  B1 HHS:   blk=37.4%, HO=877")
    print(f"  B4 Random: blk=0.02%, HO=8435")
    avg_blk = np.mean([m['mean_blocking_rate'] for m in eval_results])
    avg_ho = np.mean([m['total_handover_count'] for m in eval_results])
    print(f"  LA-DDQN:  blk={avg_blk:.4f}, HO={avg_ho:.0f}")

    # Save
    results = {
        'method': 'LA-DDQN (quick validation)',
        'train': {
            'episode_rewards': [float(r) for r in rewards],
            'episode_losses': [float(l) for l in losses],
            'train_time_s': round(train_time, 1),
            'last5_avg_reward': float(np.mean(rewards[-5:])),
        },
        'eval': eval_results,
        'config': {
            'K': K, 'feat_dim': FEAT_DIM, 'd_attn': D_ATTN,
            'hidden': HIDDEN, 'num_params': n_params,
            'episodes': QUICK_EPISODES, 'lr': LR, 'gamma': GAMMA,
        },
    }
    results_dir = PROJECT_ROOT / 'results'
    results_dir.mkdir(exist_ok=True)
    out_path = results_dir / 'la_ddqn_quick.json'
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")


if __name__ == '__main__':
    main()
