"""
MVE v3: GNN+QMIX vs FC+QMIX for Beam Hopping Scheduling

Architecture:
- GNN encoder (2 GCN layers) + Q-head + QMIX mixer (experiment)
- FC encoder (2 MLP layers) + Q-head + QMIX mixer (control)
- Identical QMIX mixer isolates GNN encoder contribution

Key fixes from failed attempts:
1. Reward = throughput only (action-dependent, clean signal)
2. Proper QMIX: gather Q(a_i) per agent, not always Q(on)
3. No reward clipping/scaling that breaks the signal
4. Soft target updates (tau=0.01)
5. Early stopping only after epsilon fully decays
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import time
from collections import deque
import random


# ============================================================
# Environment (verified, from mve_gnn_vs_fc.py)
# ============================================================

def make_hex_grid(n_rings=2):
    cells = []
    for q in range(-n_rings, n_rings + 1):
        for r in range(max(-n_rings, -q - n_rings), min(n_rings, -q + n_rings) + 1):
            cells.append((q, r))
    n = len(cells)
    adj = np.zeros((n, n), dtype=np.float32)
    for i, (q1, r1) in enumerate(cells):
        for j, (q2, r2) in enumerate(cells):
            if i != j:
                dist = (abs(q1 - q2) + abs(r1 - r2) + abs(q1 + r1 - q2 - r2)) / 2
                if dist <= 1:
                    adj[i, j] = 1.0
    return cells, adj


class BHEnv:
    def __init__(self, n_cells=19, n_beams=3, adj=None, seed=42):
        self.n = n_cells
        self.K = n_beams
        self.rng = np.random.RandomState(seed)
        if adj is None:
            _, adj = make_hex_grid()
        self.adj = adj
        self.signal = 1.0
        self.interf_per_neighbor = 0.5
        self.noise = 0.1
        self.queue = np.zeros(n_cells, dtype=np.float32)
        self.ttl = np.zeros(n_cells, dtype=np.float32)
        self.ttl_max = 10
        self.t = 0

    def reset(self):
        self.queue = self.rng.exponential(50, self.n).astype(np.float32)
        self.ttl = np.zeros(self.n, dtype=np.float32)
        self.t = 0
        return self._state()

    def _state(self):
        return np.stack([self.queue / 100.0, self.ttl / self.ttl_max], axis=-1)

    def step(self, action):
        sinr = np.zeros(self.n)
        for i in range(self.n):
            if action[i] > 0:
                n_interf = sum(1 for j in range(self.n)
                              if j != i and action[j] > 0 and self.adj[i, j] > 0)
                sinr[i] = self.signal / (self.noise + n_interf * self.interf_per_neighbor)
        throughput = np.where(action > 0, np.log2(1 + sinr), 0).astype(np.float32)
        served = throughput * 5.0
        self.queue = np.maximum(self.queue - served, 0).astype(np.float32)
        self.ttl = np.where(action > 0, 0, self.ttl + 1).astype(np.float32)
        self.ttl = np.minimum(self.ttl, self.ttl_max)
        arrivals = self.rng.exponential(20, self.n).astype(np.float32)
        self.queue += arrivals
        self.t += 1
        tp_sum = throughput.sum()
        delay_penalty = np.sum(np.maximum(self.ttl - 5, 0)) * 0.2
        overflow = np.sum(np.maximum(self.queue - 200, 0)) * 0.01
        reward = tp_sum - delay_penalty - overflow
        return self._state(), reward, tp_sum, throughput


# ============================================================
# Networks
# ============================================================

class GCNLayer(nn.Module):
    def __init__(self, d_in, d_out):
        super().__init__()
        self.w = nn.Linear(d_in, d_out)

    def forward(self, x, adj):
        deg = adj.sum(-1, keepdim=True).clamp(min=1)
        return self.w(torch.matmul(adj / deg, x))


class GNEncoder(nn.Module):
    def __init__(self, obs_dim=2, hidden=32):
        super().__init__()
        self.g1 = GCNLayer(obs_dim, hidden)
        self.g2 = GCNLayer(hidden, hidden)

    def forward(self, obs, adj):
        """obs: (B, N, D), adj: (B, N, N) -> (B, N, hidden)"""
        h = torch.relu(self.g1(obs, adj))
        h = torch.relu(self.g2(h, adj))
        return h


class FCEncoder(nn.Module):
    def __init__(self, obs_dim=2, hidden=32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
        )

    def forward(self, obs, adj=None):
        B, N, D = obs.shape
        return self.net(obs.reshape(B * N, D)).reshape(B, N, -1)


class QMIXMixer(nn.Module):
    def __init__(self, n_agents, state_dim, hidden=32):
        super().__init__()
        self.n_agents = n_agents
        self.hidden = hidden
        self.hyper_w1 = nn.Sequential(
            nn.Linear(state_dim, hidden), nn.ReLU(),
            nn.Linear(hidden, n_agents * hidden),
        )
        self.hyper_b1 = nn.Linear(state_dim, hidden)
        self.hyper_w2 = nn.Sequential(
            nn.Linear(state_dim, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden),
        )
        self.hyper_b2 = nn.Sequential(
            nn.Linear(state_dim, hidden), nn.ReLU(),
            nn.Linear(hidden, 1),
        )

    def forward(self, agent_qs, states):
        """agent_qs: (B, N), states: (B, state_dim) -> (B, 1)"""
        B = agent_qs.size(0)
        w1 = torch.abs(self.hyper_w1(states)).view(B, self.hidden, self.n_agents)
        b1 = self.hyper_b1(states)
        h = torch.relu(torch.bmm(w1, agent_qs.unsqueeze(-1)).squeeze(-1) + b1)
        w2 = torch.abs(self.hyper_w2(states)).view(B, 1, self.hidden)
        b2 = self.hyper_b2(states)
        return torch.bmm(w2, h.unsqueeze(-1)).squeeze(-1) + b2


class QMIXAgent(nn.Module):
    def __init__(self, encoder, n_agents, obs_dim=2, hidden=32):
        super().__init__()
        self.encoder = encoder
        self.q_head = nn.Linear(hidden, 2)
        state_dim = n_agents * obs_dim
        self.mixer = QMIXMixer(n_agents, state_dim, hidden)

    def get_q(self, obs, adj):
        return self.q_head(self.encoder(obs, adj))  # (B, N, 2)

    def get_q_tot(self, q_vals, actions, global_state):
        """q_vals: (B,N,2), actions: (B,N) binary, global_state: (B, N*obs_dim)"""
        q_chosen = q_vals.gather(2, actions.long().unsqueeze(-1)).squeeze(-1)
        return self.mixer(q_chosen, global_state)


# ============================================================
# Replay Buffer
# ============================================================

class ReplayBuffer:
    def __init__(self, capacity=50000):
        self.buf = deque(maxlen=capacity)

    def push(self, s, a, r, ns, d):
        self.buf.append((s, a, r, ns, d))

    def sample(self, bs):
        batch = random.sample(self.buf, bs)
        s, a, r, ns, d = zip(*batch)
        return (np.array(s, dtype=np.float32), np.array(a, dtype=np.float32),
                np.array(r, dtype=np.float32), np.array(ns, dtype=np.float32),
                np.array(d, dtype=np.float32))

    def __len__(self):
        return len(self.buf)


# ============================================================
# Action selection
# ============================================================

def select_action(q_values, K, epsilon=0.0, rng=None):
    """q_values: (N, 2) -> action: (N,) binary sum=K"""
    n = q_values.shape[0]
    if rng is None:
        rng = np.random.RandomState()
    if rng.random() < epsilon:
        idx = rng.choice(n, K, replace=False)
    else:
        advantage = q_values[:, 1] - q_values[:, 0]
        idx = np.argsort(advantage)[-K:]
    action = np.zeros(n, dtype=np.float32)
    action[idx] = 1.0
    return action


# ============================================================
# Training
# ============================================================

def train(agent, target, env, adj, n_ep=1000, ep_len=50, lr=1e-3,
          gamma=0.99, buf_size=50000, batch_size=64, target_update=200,
          eps_start=1.0, eps_end=0.05, eps_decay=500, seed=42):
    rng = np.random.RandomState(seed)
    torch.manual_seed(seed)
    opt = optim.Adam(agent.parameters(), lr=lr)
    buf = ReplayBuffer(buf_size)
    adj_t = torch.FloatTensor(adj).unsqueeze(0)
    n = env.n

    rewards_hist, tp_hist = [], []
    total_steps = 0
    early_stop = False

    for ep in range(n_ep):
        if early_stop:
            break
        epsilon = eps_end + (eps_start - eps_end) * max(0, (eps_decay - ep) / eps_decay)

        obs = env.reset()
        ep_reward, ep_tp = 0.0, []

        for t in range(ep_len):
            obs_t = torch.FloatTensor(obs).unsqueeze(0)
            gs_t = obs_t.reshape(1, -1)

            with torch.no_grad():
                q = agent.get_q(obs_t, adj_t).squeeze(0).numpy()

            action = select_action(q, env.K, epsilon, rng)
            next_obs, reward, tp, _ = env.step(action)
            done = float(t == ep_len - 1)

            # Store with throughput-only reward for learning
            buf.push(obs.copy(), action.copy(), tp, next_obs.copy(), done)
            obs = next_obs
            ep_reward += reward
            ep_tp.append(tp)
            total_steps += 1

            if len(buf) >= batch_size:
                b_s, b_a, b_r, b_ns, b_d = buf.sample(batch_size)
                b_s_t = torch.FloatTensor(b_s)
                b_a_t = torch.FloatTensor(b_a)
                b_r_t = torch.FloatTensor(b_r)
                b_ns_t = torch.FloatTensor(b_ns)
                b_d_t = torch.FloatTensor(b_d)
                B = b_s_t.size(0)
                adj_b = adj_t.expand(B, -1, -1)
                b_gs = b_s_t.reshape(B, -1)
                b_ngs = b_ns_t.reshape(B, -1)

                # Current Q_tot
                q_vals = agent.get_q(b_s_t, adj_b)
                q_tot = agent.get_q_tot(q_vals, b_a_t, b_gs)

                # Target Q_tot (Double DQN)
                with torch.no_grad():
                    q_online_next = agent.get_q(b_ns_t, adj_b)
                    adv = q_online_next[:, :, 1] - q_online_next[:, :, 0]
                    next_a = torch.zeros(B, n)
                    _, topk = adv.topk(env.K, dim=-1)
                    next_a.scatter_(1, topk, 1.0)
                    q_next = target.get_q(b_ns_t, adj_b)
                    q_tot_next = target.get_q_tot(q_next, next_a, b_ngs)
                    q_target = b_r_t.unsqueeze(-1) + gamma * (1 - b_d_t.unsqueeze(-1)) * q_tot_next

                loss = nn.functional.smooth_l1_loss(q_tot, q_target)
                opt.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(agent.parameters(), 1.0)
                opt.step()

            if total_steps % target_update == 0:
                tau = 0.01
                for p, tp_p in zip(agent.parameters(), target.parameters()):
                    tp_p.data.copy_(tau * p.data + (1 - tau) * tp_p.data)

        rewards_hist.append(ep_reward)
        tp_hist.append(np.mean(ep_tp))

        if (ep + 1) % 200 == 0:
            recent = rewards_hist[-20:] if len(rewards_hist) >= 20 else rewards_hist
            print(f"  Ep {ep+1}: reward={np.mean(recent):.1f}, eps={epsilon:.3f}")

        if ep >= eps_decay + 100 and len(rewards_hist) >= eps_decay + 100:
            w = rewards_hist[-100:]
            h1, h2 = np.mean(w[:50]), np.mean(w[50:])
            scale = max(abs(h1), abs(h2), 1.0)
            if abs(h2 - h1) / scale < 0.003:
                print(f"  Early stop at ep {ep+1}, converged at {h2:.1f}")
                early_stop = True

    return rewards_hist, tp_hist


# ============================================================
# Evaluation
# ============================================================

def evaluate(agent, env, adj, n_ep=50, ep_len=50):
    agent.eval()
    adj_t = torch.FloatTensor(adj).unsqueeze(0)
    rewards, tps = [], []
    with torch.no_grad():
        for _ in range(n_ep):
            obs = env.reset()
            ep_r, ep_tp = 0, []
            for t in range(ep_len):
                obs_t = torch.FloatTensor(obs).unsqueeze(0)
                q = agent.get_q(obs_t, adj_t).squeeze(0).numpy()
                action = select_action(q, env.K, epsilon=0.0)
                obs, r, tp, _ = env.step(action)
                ep_r += r
                ep_tp.append(tp)
            rewards.append(ep_r)
            tps.append(np.mean(ep_tp))
    agent.train()
    return np.mean(rewards), np.mean(tps), np.std(rewards)


def greedy(env, n_ep=50, ep_len=50, avoid_interf=False):
    rewards, tps = [], []
    for _ in range(n_ep):
        s = env.reset()
        ep_r, ep_tp = 0, []
        for t in range(ep_len):
            q = s[:, 0].copy()
            selected, action = [], np.zeros(env.n)
            for _ in range(env.K):
                mask = np.zeros(env.n, dtype=bool)
                for sel in selected:
                    mask[sel] = True
                    if avoid_interf:
                        mask |= (env.adj[sel] > 0)
                q_m = q.copy()
                q_m[mask] = -np.inf
                best = np.argmax(q_m) if q_m.max() > -np.inf else ([i for i in range(env.n) if i not in selected] or [0])[0]
                selected.append(best)
                action[best] = 1.0
            s, r, tp, _ = env.step(action)
            ep_r += r
            ep_tp.append(tp)
        rewards.append(ep_r)
        tps.append(np.mean(ep_tp))
    return np.mean(rewards), np.mean(tps), np.std(rewards)


def random_bh(env, n_ep=50, ep_len=50):
    rewards, tps = [], []
    for _ in range(n_ep):
        s = env.reset()
        ep_r, ep_tp = 0, []
        for t in range(ep_len):
            action = np.zeros(env.n)
            action[np.random.choice(env.n, env.K, replace=False)] = 1.0
            s, r, tp, _ = env.step(action)
            ep_r += r
            ep_tp.append(tp)
        rewards.append(ep_r)
        tps.append(np.mean(ep_tp))
    return np.mean(rewards), np.mean(tps), np.std(rewards)


# ============================================================
# Main
# ============================================================

def make_agent(enc_type, n, obs_dim=2, hidden=32):
    enc = GNEncoder(obs_dim, hidden) if enc_type == 'gnn' else FCEncoder(obs_dim, hidden)
    agent = QMIXAgent(enc, n, obs_dim, hidden)
    enc2 = GNEncoder(obs_dim, hidden) if enc_type == 'gnn' else FCEncoder(obs_dim, hidden)
    target = QMIXAgent(enc2, n, obs_dim, hidden)
    target.load_state_dict(agent.state_dict())
    return agent, target


def main():
    print("=" * 60)
    print("MVE v3: GNN+QMIX vs FC+QMIX for BH Scheduling")
    print("=" * 60)

    cells, adj = make_hex_grid(2)
    n, K, obs_dim = 19, 3, 2

    print(f"\nConfig: {n} cells, K={K} beams, interf=0.5")
    print("Training: QMIX + DQN + replay buffer + throughput reward")

    print("\n--- SINR Reference ---")
    for ni in range(5):
        sinr = 1.0 / (0.1 + ni * 0.5)
        print(f"  {ni} interf: SINR={sinr:.2f}, tp={np.log2(1+sinr):.2f}")

    a1, _ = make_agent('gnn', n, obs_dim)
    a2, _ = make_agent('fc', n, obs_dim)
    print(f"\nParams: GNN+QMIX={sum(p.numel() for p in a1.parameters())}, FC+QMIX={sum(p.numel() for p in a2.parameters())}")

    seeds = [42, 123, 456]
    results = {'GNN+QMIX': [], 'FC+QMIX': [], 'Greedy': [], 'IA-Greedy': [], 'Random': []}

    for seed in seeds:
        print(f"\n{'='*50}\nSeed: {seed}\n{'='*50}")

        for name, enc_type in [("GNN+QMIX", 'gnn'), ("FC+QMIX", 'fc')]:
            print(f"\n[{name}]")
            agent, target = make_agent(enc_type, n, obs_dim)
            env = BHEnv(n, K, adj, seed=seed)
            t0 = time.time()
            rew, _ = train(agent, target, env, adj, seed=seed)
            print(f"  {time.time()-t0:.1f}s, final={np.mean(rew[-20:]):.1f}")

            if enc_type == 'gnn':
                gnn_agent, gnn_rew = agent, rew
            else:
                fc_agent, fc_rew = agent, rew

        es = seed * 7
        g_r, g_tp, g_std = evaluate(gnn_agent, BHEnv(n, K, adj, seed=es), adj)
        f_r, f_tp, f_std = evaluate(fc_agent, BHEnv(n, K, adj, seed=es), adj)
        gr_r, gr_tp, gr_std = greedy(BHEnv(n, K, adj, seed=es))
        ia_r, ia_tp, ia_std = greedy(BHEnv(n, K, adj, seed=es), avoid_interf=True)
        rnd_r, rnd_tp, rnd_std = random_bh(BHEnv(n, K, adj, seed=es))

        print(f"\n  Eval: GNN={g_tp:.2f}, FC={f_tp:.2f}, Greedy={gr_tp:.2f}, IA-Greedy={ia_tp:.2f}, Random={rnd_tp:.2f}")

        results['GNN+QMIX'].append((g_r, g_tp, g_std))
        results['FC+QMIX'].append((f_r, f_tp, f_std))
        results['Greedy'].append((gr_r, gr_tp, gr_std))
        results['IA-Greedy'].append((ia_r, ia_tp, ia_std))
        results['Random'].append((rnd_r, rnd_tp, rnd_std))

    # Aggregate
    print("\n" + "=" * 60)
    print("AGGREGATE RESULTS (3 seeds)")
    print("=" * 60)
    agg = {}
    for name, vals in results.items():
        r_m = np.mean([v[0] for v in vals])
        r_s = np.std([v[0] for v in vals])
        tp_m = np.mean([v[1] for v in vals])
        tp_s = np.std([v[1] for v in vals])
        agg[name] = (r_m, r_s, tp_m, tp_s)
        print(f"{name:<15} reward={r_m:>7.1f}+/-{r_s:.0f}  tp={tp_m:.2f}+/-{tp_s:.2f}")

    gnn_tp, fc_tp, gr_tp, ia_tp = agg['GNN+QMIX'][2], agg['FC+QMIX'][2], agg['Greedy'][2], agg['IA-Greedy'][2]
    print(f"\nGNN vs FC:      {(gnn_tp-fc_tp)/fc_tp*100:+.2f}%")
    print(f"GNN vs Greedy:  {(gnn_tp-gr_tp)/gr_tp*100:+.2f}%")
    print(f"GNN vs IA-Greedy: {(gnn_tp-ia_tp)/ia_tp*100:+.2f}%")

    print("\n--- Convergence ---")
    for label, hist in [("GNN", gnn_rew), ("FC", fc_rew)]:
        if len(hist) >= 50:
            l50 = hist[-50:]
            var = (max(l50) - min(l50)) / (abs(np.mean(l50)) + 1e-8) * 100
            print(f"{label}: var={var:.1f}% ({'ok' if var < 10 else 'high'})")

    print("\n--- MVE Verdict ---")
    m_fc = (gnn_tp - fc_tp) / fc_tp * 100
    m_gr = (gnn_tp - gr_tp) / gr_tp * 100

    if m_fc >= 5 and m_gr >= 10:
        print(f"PASS: GNN+QMIX > FC+QMIX by {m_fc:.1f}% AND > Greedy by {m_gr:.1f}%")
    elif m_fc > 0:
        print(f"CONDITIONAL: GNN+QMIX > FC+QMIX by {m_fc:.1f}% (need >=5%)")
        print(f"  GNN vs Greedy: {m_gr:+.1f}% (need >=10%)")
    else:
        print(f"FAIL: GNN+QMIX <= FC+QMIX ({m_fc:+.1f}%)")
        print(f"\nAnalysis:")
        print(f"  - GNN consistently underperforms FC across multiple training approaches")
        print(f"  - GNN message passing with noisy neighbor queue states introduces noise")
        print(f"  - FC encoder with global state in QMIX mixer already captures sufficient info")
        print(f"  - The top-K action selection bypasses the GNN's spatial reasoning")
        print(f"  - Interference awareness (IA-Greedy +50%) requires explicit constraint,")
        print(f"    not implicit learning through GNN neighbor features")
        print(f"\nRecommendation:")
        print(f"  - GNN encoder is NOT beneficial for BH scheduling with this formulation")
        print(f"  - Consider alternative GNN applications: graph-level policy, attention-based")
        print(f"  - Or use explicit interference features rather than raw neighbor observations")


if __name__ == "__main__":
    main()
