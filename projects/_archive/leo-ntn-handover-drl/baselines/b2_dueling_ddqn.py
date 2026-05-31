"""B2 Baseline: Dueling Double DQN for LEO satellite handover.

Dueling architecture (L02 corrected):
  Q(s,a) = V(s) + A(s,a) - mean(A(s,·))
  Shared backbone: obs_dim -> 256 -> 128, then split into V and A streams.

Double DQN: online network selects action (argmax Q_online),
target network evaluates Q_target.

Parameter sharing: one network serves all 15 UEs.
Action masking: only visible satellites are selectable.
"""

import argparse
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

parser = argparse.ArgumentParser()
parser.add_argument('--name', default='b2_ddqn', help='Experiment name')
parser.add_argument('--num_ues', type=int, default=cfg.NUM_UES)
parser.add_argument('--sat_capacity', type=int, default=cfg.SAT_CAPACITY)
parser.add_argument('--episodes', type=int, default=cfg.NUM_EPISODES)
args = parser.parse_args()

# ── Hyperparameters (from config.py) ───────────────────────────────────────────
LR = cfg.DDQN_LR                    # 1e-3
GAMMA = cfg.DDQN_GAMMA              # 0.99
EPS_START = cfg.DDQN_EPS_START      # 0.2
EPS_END = cfg.DDQN_EPS_END          # 0.01
EPS_DECAY = cfg.DDQN_EPS_DECAY      # 300 (exponential decay rate)
BUFFER_SIZE = cfg.DDQN_BUFFER_SIZE   # 200_000
BATCH_SIZE = cfg.DDQN_BATCH_SIZE     # 256
TARGET_UPDATE = cfg.DDQN_TARGET_UPDATE  # 1000 steps
HIDDEN = cfg.DDQN_HIDDEN            # (256, 128)
NUM_EPISODES = args.episodes
NUM_EVAL_SEEDS = cfg.NUM_EVAL_SEEDS # 5
NUM_UES = args.num_ues

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ── Replay Buffer ──────────────────────────────────────────────────────────────
class ReplayBuffer:
    """Uniform replay buffer for (s, a, r, s', done) transitions."""

    def __init__(self, capacity: int):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size: int):
        indices = np.random.choice(len(self.buffer), batch_size, replace=False)
        batch = [self.buffer[i] for i in indices]
        states, actions, rewards, next_states, dones = zip(*batch)
        return (
            np.array(states, dtype=np.float32),
            np.array(actions, dtype=np.int64),
            np.array(rewards, dtype=np.float32),
            np.array(next_states, dtype=np.float32),
            np.array(dones, dtype=np.float32),
        )

    def __len__(self):
        return len(self.buffer)


# ── Dueling Network ───────────────────────────────────────────────────────────
class DuelingQNetwork(nn.Module):
    """Dueling architecture with shared backbone splitting into V and A streams.

    Backbone: Linear(obs_dim, 256) -> ReLU -> Linear(256, 128) -> ReLU
    V stream:  Linear(128, 1)
    A stream:  Linear(128, num_actions)
    """

    def __init__(self, obs_dim: int, num_actions: int):
        super().__init__()
        self.shared = nn.Sequential(
            nn.Linear(obs_dim, HIDDEN[0]),
            nn.ReLU(),
            nn.Linear(HIDDEN[0], HIDDEN[1]),
            nn.ReLU(),
        )
        self.value_stream = nn.Linear(HIDDEN[1], 1)
        self.advantage_stream = nn.Linear(HIDDEN[1], num_actions)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        features = self.shared(x)
        value = self.value_stream(features)
        advantage = self.advantage_stream(features)
        return value + advantage - advantage.mean(dim=-1, keepdim=True)


# ── Episode runner ─────────────────────────────────────────────────────────────
def run_episode(env, network, eps, seed):
    """Run one full episode, collecting transitions from all UEs.

    Returns (transitions_list, episode_reward_sum).
    episode_reward_sum = sum of all per-UE rewards across all steps.
    """
    obs = env.reset(seed=seed)
    all_transitions = []
    episode_reward = 0.0
    done = False

    while not done:
        valid = env.get_valid_actions()  # (num_ues, num_sats) bool
        actions = np.zeros(env.num_ues, dtype=int)

        for ue in range(env.num_ues):
            state = torch.FloatTensor(obs[ue]).unsqueeze(0).to(DEVICE)
            with torch.no_grad():
                q = network(state).squeeze(0).cpu().numpy()
            # Mask invalid actions
            q[~valid[ue]] = -float('inf')

            if np.random.random() < eps:
                v = np.where(valid[ue])[0]
                actions[ue] = np.random.choice(v) if len(v) > 0 else 0
            else:
                actions[ue] = int(q.argmax())

        next_obs, rewards, done, info = env.step(actions)

        for ue in range(env.num_ues):
            all_transitions.append(
                (obs[ue].copy(), actions[ue], rewards[ue], next_obs[ue].copy(), done)
            )

        episode_reward += float(rewards.sum())
        obs = next_obs

    return all_transitions, episode_reward


# ── Training ───────────────────────────────────────────────────────────────────
def train(env, network, target_net, optimizer, buffer, seed):
    """Train for NUM_EPISODES, return (episode_rewards, episode_losses)."""
    total_steps = 0
    episode_rewards = []
    episode_losses = []

    for ep in range(NUM_EPISODES):
        # Exponential epsilon decay
        eps = EPS_END + (EPS_START - EPS_END) * np.exp(-1.0 * ep / EPS_DECAY)

        transitions, ep_reward = run_episode(env, network, eps, seed=seed)
        episode_rewards.append(ep_reward)

        # Push all transitions into buffer (parameter sharing across UEs)
        for s, a, r, s_next, d in transitions:
            buffer.push(s, a, r, s_next, d)

        # Learning step: sample and update
        ep_loss = 0.0
        num_updates = 0
        if len(buffer) >= BATCH_SIZE:
            # Multiple updates per episode to keep learning rate adequate
            num_transitions = len(transitions)
            # One update per BATCH_SIZE transitions collected this episode
            n_updates = max(1, num_transitions // BATCH_SIZE)
            for _ in range(n_updates):
                b_s, b_a, b_r, b_ns, b_d = buffer.sample(BATCH_SIZE)

                b_s_t = torch.FloatTensor(b_s).to(DEVICE)
                b_a_t = torch.LongTensor(b_a).unsqueeze(1).to(DEVICE)
                b_r_t = torch.FloatTensor(b_r).to(DEVICE)
                b_ns_t = torch.FloatTensor(b_ns).to(DEVICE)
                b_d_t = torch.FloatTensor(b_d).to(DEVICE)

                # Current Q values
                q_values = network(b_s_t).gather(1, b_a_t).squeeze(1)

                # Double DQN: online selects action, target evaluates
                with torch.no_grad():
                    next_q_online = network(b_ns_t)
                    next_actions = next_q_online.argmax(dim=1, keepdim=True)
                    next_q_target = target_net(b_ns_t).gather(1, next_actions).squeeze(1)
                    target_q = b_r_t + GAMMA * next_q_target * (1.0 - b_d_t)

                loss = nn.SmoothL1Loss()(q_values, target_q)
                optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(network.parameters(), 10.0)
                optimizer.step()

                ep_loss += loss.item()
                num_updates += 1
                total_steps += 1

                # Target network sync
                if total_steps % TARGET_UPDATE == 0:
                    target_net.load_state_dict(network.state_dict())

        avg_loss = ep_loss / max(num_updates, 1)
        episode_losses.append(avg_loss)

        if (ep + 1) % 10 == 0:
            recent = episode_rewards[-10:]
            recent_loss = episode_losses[-10:]
            print(
                f"  ep {ep+1:3d}/{NUM_EPISODES} | "
                f"avg_reward={np.mean(recent):.1f} | "
                f"eps={eps:.3f} | "
                f"avg_loss={np.mean(recent_loss):.4f} | "
                f"buf={len(buffer)}"
            )

    return episode_rewards, episode_losses


# ── Evaluation (greedy) ───────────────────────────────────────────────────────
def evaluate(env, network, seed):
    """Run one episode with eps=0 (greedy), return metrics dict."""
    network.eval()
    transitions, ep_reward = run_episode(env, network, eps=0.0, seed=seed)

    # Also collect detailed info for metrics
    obs = env.reset(seed=seed)
    throughputs = []
    blocking_rates = []
    handover_count = 0
    ue_throughput = np.zeros(env.num_ues)
    done = False

    while not done:
        valid = env.get_valid_actions()
        actions = np.zeros(env.num_ues, dtype=int)
        for ue in range(env.num_ues):
            state = torch.FloatTensor(obs[ue]).unsqueeze(0).to(DEVICE)
            with torch.no_grad():
                q = network(state).squeeze(0).cpu().numpy()
            q[~valid[ue]] = -float('inf')
            actions[ue] = int(q.argmax())

        obs, rewards, done, info = env.step(actions)
        throughputs.append(float(info['total_throughput_bps']))
        blocking_rates.append(float(info['blocking_rate']))
        handover_count += int(info['handover_count'])
        ue_throughput += info['throughput_bps']

    jain = float(np.sum(ue_throughput) ** 2 /
                 (env.num_ues * np.sum(ue_throughput ** 2) + 1e-12))
    network.train()
    return {
        'episode_reward': float(ep_reward),
        'mean_throughput_bps': float(np.mean(throughputs)),
        'mean_blocking_rate': float(np.mean(blocking_rates)),
        'total_handover_count': handover_count,
        'jain_fairness': jain,
    }


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    print(f"Device: {DEVICE}")
    env = LEOSatHandoverEnv(num_ues=NUM_UES, sat_capacity=args.sat_capacity, seed=42)
    obs_dim = env.obs_dim      # 1585
    num_actions = env.num_sats # 396

    print(f"obs_dim={obs_dim}, num_actions={num_actions}, num_ues={NUM_UES}")
    print(f"num_steps={env.num_steps}, episodes={NUM_EPISODES}")
    print(f"hidden={HIDDEN}, buffer={BUFFER_SIZE}, batch={BATCH_SIZE}")
    print()

    # Initialize networks
    torch.manual_seed(42)
    np.random.seed(42)
    network = DuelingQNetwork(obs_dim, num_actions).to(DEVICE)
    target_net = DuelingQNetwork(obs_dim, num_actions).to(DEVICE)
    target_net.load_state_dict(network.state_dict())
    target_net.eval()

    optimizer = optim.Adam(network.parameters(), lr=LR)
    buffer = ReplayBuffer(BUFFER_SIZE)

    # Train
    t0 = time.time()
    episode_rewards, episode_losses = train(
        env, network, target_net, optimizer, buffer, seed=42
    )
    train_time = time.time() - t0
    print(f"\nTraining completed in {train_time:.1f}s")

    # Evaluate on 5 seeds
    eval_results = []
    eval_seeds = [100, 200, 300, 400, 500]
    for i, eseed in enumerate(eval_seeds[:NUM_EVAL_SEEDS]):
        eval_env = LEOSatHandoverEnv(num_ues=NUM_UES, sat_capacity=args.sat_capacity, seed=eseed)
        metrics = evaluate(eval_env, network, seed=eseed)
        metrics['eval_seed'] = eseed
        eval_results.append(metrics)
        print(
            f"  eval seed={eseed}: reward={metrics['episode_reward']:.1f} | "
            f"tput={metrics['mean_throughput_bps']:.0f} | "
            f"blk={metrics['mean_blocking_rate']:.4f} | "
            f"HO={metrics['total_handover_count']}"
        )

    # Aggregate
    eval_rewards = [m['episode_reward'] for m in eval_results]
    eval_tputs = [m['mean_throughput_bps'] for m in eval_results]
    eval_blks = [m['mean_blocking_rate'] for m in eval_results]
    eval_hos = [m['total_handover_count'] for m in eval_results]

    results = {
        'train': {
            'episode_rewards': [float(r) for r in episode_rewards],
            'episode_losses': [float(l) for l in episode_losses],
            'train_time_s': round(train_time, 1),
            'final_reward': float(episode_rewards[-1]),
            'last10_avg_reward': float(np.mean(episode_rewards[-10:])),
        },
        'eval': {
            'seeds': eval_results,
            'mean_reward': float(np.mean(eval_rewards)),
            'std_reward': float(np.std(eval_rewards)),
            'mean_throughput_bps': float(np.mean(eval_tputs)),
            'mean_blocking_rate': float(np.mean(eval_blks)),
            'mean_handover_count': float(np.mean(eval_hos)),
        },
        'config': {
            'num_ues': NUM_UES,
            'obs_dim': obs_dim,
            'num_actions': num_actions,
            'num_episodes': NUM_EPISODES,
            'hidden': HIDDEN,
            'lr': LR,
            'gamma': GAMMA,
            'eps_start': EPS_START,
            'eps_end': EPS_END,
            'eps_decay': EPS_DECAY,
            'buffer_size': BUFFER_SIZE,
            'batch_size': BATCH_SIZE,
            'target_update': TARGET_UPDATE,
        },
    }

    # Save
    results_dir = PROJECT_ROOT / 'results'
    results_dir.mkdir(exist_ok=True)
    out_path = results_dir / f'{args.name}_results.json'
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")

    # Summary
    print(f"\n{'='*60}")
    print("B2 Dueling DDQN Summary")
    print(f"{'='*60}")
    print(f"  Train: {NUM_EPISODES} episodes, {train_time:.1f}s")
    print(f"  Last-10 avg reward: {results['train']['last10_avg_reward']:.1f}")
    print(f"  Eval ({NUM_EVAL_SEEDS} seeds):")
    print(f"    Reward:   {np.mean(eval_rewards):.1f} +/- {np.std(eval_rewards):.1f}")
    print(f"    Blocking: {np.mean(eval_blks):.4f}")
    print(f"    Handover: {np.mean(eval_hos):.1f}")


if __name__ == '__main__':
    main()
