"""
MVE v2: GNN vs FC for Beam Hopping Scheduling
Simplified interference model: direct SINR-based throughput with proper regime.

Key design:
- 19-cell hex grid, K=3 beams
- SINR = signal / (noise + sum of interference from co-illuminated neighbors)
- Interference proportional to 1/distance^2 for simplicity
- Environment tuned so interference-limited regime holds
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import time


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

        # Channel: signal=1.0, interference from neighbor=0.5, noise=0.1
        # SINR = 1.0 / (0.1 + 0.5 * num_coilluminated_neighbors)
        self.signal = 1.0
        self.interf_per_neighbor = 0.5
        self.noise = 0.1

        # Queue state
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
        """action: (n,) binary, sum=K"""
        # SINR for each illuminated cell
        sinr = np.zeros(self.n)
        for i in range(self.n):
            if action[i] > 0:
                n_interf_neighbors = sum(1 for j in range(self.n)
                                        if j != i and action[j] > 0 and self.adj[i, j] > 0)
                sinr[i] = self.signal / (self.noise + n_interf_neighbors * self.interf_per_neighbor)

        # Throughput = log2(1+SINR) for illuminated cells
        throughput = np.where(action > 0, np.log2(1 + sinr), 0).astype(np.float32)

        # Serve queue
        served = throughput * 5.0  # scale factor
        self.queue = np.maximum(self.queue - served, 0).astype(np.float32)

        # TTL for unserved
        self.ttl = np.where(action > 0, 0, self.ttl + 1).astype(np.float32)
        self.ttl = np.minimum(self.ttl, self.ttl_max)

        # New arrivals
        arrivals = self.rng.exponential(20, self.n).astype(np.float32)
        self.queue += arrivals
        self.t += 1

        # Reward
        tp_sum = throughput.sum()
        delay_penalty = np.sum(np.maximum(self.ttl - 5, 0)) * 0.2
        overflow = np.sum(np.maximum(self.queue - 200, 0)) * 0.01
        reward = tp_sum - delay_penalty - overflow

        return self._state(), reward, tp_sum, throughput


class GCNLayer(nn.Module):
    def __init__(self, d_in, d_out):
        super().__init__()
        self.w = nn.Linear(d_in, d_out)

    def forward(self, x, adj):
        deg = adj.sum(-1, keepdim=True).clamp(min=1)
        adj_n = adj / deg
        return self.w(torch.matmul(adj_n, x))


class GNNPolicy(nn.Module):
    def __init__(self, n, d=2, h=32):
        super().__init__()
        self.g1 = GCNLayer(d, h)
        self.g2 = GCNLayer(h, h)
        self.head = nn.Linear(h, 1)

    def forward(self, s, adj):
        h = torch.relu(self.g1(s, adj))
        h = torch.relu(self.g2(h, adj))
        return self.head(h).squeeze(-1)


class FCPolicy(nn.Module):
    def __init__(self, n, d=2, h=32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n * d, h), nn.ReLU(),
            nn.Linear(h, h), nn.ReLU(),
            nn.Linear(h, n),
        )

    def forward(self, s, adj=None):
        return self.net(s.flatten(1))


def act(policy, state, adj, K, explore=True):
    scores = policy(state, adj)
    if explore and policy.training:
        scores = scores + (-torch.log(-torch.log(torch.rand_like(scores) + 1e-8) + 1e-8)) * 0.5
    action = torch.zeros_like(scores)
    _, idx = scores.topk(K, -1)
    action.scatter_(-1, idx, 1.0)
    return action, scores


def train(policy, env, adj_t, n_ep=500, ep_len=50, lr=3e-4):
    opt = optim.Adam(policy.parameters(), lr=lr)
    rewards_hist = []
    tp_hist = []

    for ep in range(n_ep):
        s = env.reset()
        ep_r, ep_tp, log_probs = 0, [], []

        for t in range(ep_len):
            s_t = torch.FloatTensor(s).unsqueeze(0)
            a, scores = act(policy, s_t, adj_t, env.K, explore=True)
            log_p = (torch.log_softmax(scores, -1) * a).sum()
            s, r, tp, _ = env.step(a.squeeze().numpy())

            ep_r += r
            ep_tp.append(tp)
            log_probs.append(log_p)

        R = sum([r * (0.99 ** i) for i, r in enumerate([env.step(act(policy, torch.FloatTensor(s).unsqueeze(0), adj_t, env.K)[0].squeeze().numpy())[1] for _ in range(1)])])
        baseline = np.mean(rewards_hist[-20:]) if len(rewards_hist) >= 20 else 0
        advantage = ep_r - baseline

        loss = -sum(log_probs) * advantage / len(log_probs)
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(policy.parameters(), 1.0)
        opt.step()

        rewards_hist.append(ep_r)
        tp_hist.append(np.mean(ep_tp))

    return rewards_hist, tp_hist


def evaluate(policy, env, adj_t, n_ep=50, ep_len=50):
    policy.eval()
    rewards, tps = [], []
    with torch.no_grad():
        for _ in range(n_ep):
            s = env.reset()
            ep_r, ep_tp = 0, []
            for t in range(ep_len):
                s_t = torch.FloatTensor(s).unsqueeze(0)
                a, _ = act(policy, s_t, adj_t, env.K, explore=False)
                s, r, tp, _ = env.step(a.squeeze().numpy())
                ep_r += r
                ep_tp.append(tp)
            rewards.append(ep_r)
            tps.append(np.mean(ep_tp))
    policy.train()
    return np.mean(rewards), np.mean(tps), np.std(rewards)


def greedy(env, n_ep=50, ep_len=50, avoid_interf=False):
    rewards, tps = [], []
    for _ in range(n_ep):
        s = env.reset()
        ep_r, ep_tp = 0, []
        for t in range(ep_len):
            q = s[:, 0].copy()
            selected = []
            action = np.zeros(env.n)

            for _ in range(env.K):
                mask = np.zeros(env.n, dtype=bool)
                for sel in selected:
                    mask[sel] = True
                    if avoid_interf:
                        mask |= (env.adj[sel] > 0)
                q_m = q.copy()
                q_m[mask] = -np.inf
                if q_m.max() <= -np.inf:
                    # fallback: pick any unselected
                    remaining = [i for i in range(env.n) if i not in selected]
                    best = remaining[0] if remaining else 0
                else:
                    best = np.argmax(q_m)
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
            chosen = np.random.choice(env.n, env.K, replace=False)
            action[chosen] = 1.0
            s, r, tp, _ = env.step(action)
            ep_r += r
            ep_tp.append(tp)
        rewards.append(ep_r)
        tps.append(np.mean(ep_tp))
    return np.mean(rewards), np.mean(tps), np.std(rewards)


def main():
    print("=" * 60)
    print("MVE v2: GNN vs FC for BH Scheduling")
    print("=" * 60)

    cells, adj = make_hex_grid(2)
    adj_t = torch.FloatTensor(adj).unsqueeze(0)
    n = 19
    K = 3

    print(f"\nConfig: {n} cells, K={K} beams, interf_per_neighbor=0.5")

    # SINR examples
    print("\n--- SINR Analysis ---")
    for n_interf in range(5):
        sinr = 1.0 / (0.1 + n_interf * 0.5)
        tp = np.log2(1 + sinr)
        print(f"  {n_interf} interfering neighbors: SINR={sinr:.2f}, throughput={tp:.2f} bits/s/Hz")

    # Count params
    gnn = GNNPolicy(n, d=2, h=32)
    fc = FCPolicy(n, d=2, h=32)
    print(f"\nParams: GNN={sum(p.numel() for p in gnn.parameters())}, FC={sum(p.numel() for p in fc.parameters())}")

    # Run multiple seeds for statistical significance
    seeds = [42, 123, 456]
    results = {'GNN': [], 'FC': [], 'Greedy': [], 'IA-Greedy': [], 'Random': []}

    for seed in seeds:
        print(f"\n{'='*40}")
        print(f"Seed: {seed}")
        print(f"{'='*40}")

        # Train GNN
        gnn = GNNPolicy(n, d=2, h=32)
        env_g = BHEnv(n, K, adj, seed=seed)
        t0 = time.time()
        gnn_r, gnn_tp = train(gnn, env_g, adj_t, n_ep=500, ep_len=50)
        print(f"GNN train: {time.time()-t0:.1f}s, final reward={np.mean(gnn_r[-20:]):.1f}")

        # Train FC
        fc = FCPolicy(n, d=2, h=32)
        env_f = BHEnv(n, K, adj, seed=seed)
        t0 = time.time()
        fc_r, fc_tp = train(fc, env_f, adj_t, n_ep=500, ep_len=50)
        print(f"FC train:  {time.time()-t0:.1f}s, final reward={np.mean(fc_r[-20:]):.1f}")

        # Evaluate
        env_e = BHEnv(n, K, adj, seed=seed*7)
        g_r, g_tp, g_std = evaluate(gnn, env_e, adj_t)
        f_r, f_tp, f_std = evaluate(fc, env_e, adj_t)

        env_b = BHEnv(n, K, adj, seed=seed*7)
        gr_r, gr_tp, gr_std = greedy(env_b)
        env_b2 = BHEnv(n, K, adj, seed=seed*7)
        ia_r, ia_tp, ia_std = greedy(env_b2, avoid_interf=True)
        env_b3 = BHEnv(n, K, adj, seed=seed*7)
        rnd_r, rnd_tp, rnd_std = random_bh(env_b3)

        print(f"\nEval: GNN={g_tp:.2f}±{g_std:.1f}, FC={f_tp:.2f}±{f_std:.1f}, "
              f"Greedy={gr_tp:.2f}±{gr_std:.1f}, IA-Greedy={ia_tp:.2f}±{ia_std:.1f}, Random={rnd_tp:.2f}±{rnd_std:.1f}")

        results['GNN'].append((g_r, g_tp, g_std))
        results['FC'].append((f_r, f_tp, f_std))
        results['Greedy'].append((gr_r, gr_tp, gr_std))
        results['IA-Greedy'].append((ia_r, ia_tp, ia_std))
        results['Random'].append((rnd_r, rnd_tp, rnd_std))

    # Aggregate
    print("\n" + "=" * 60)
    print("AGGREGATE RESULTS (3 seeds)")
    print("=" * 60)
    print(f"{'Method':<15} {'Reward':>10} {'±':>3} {'Throughput':>12} {'±':>3}")
    print("-" * 50)
    agg = {}
    for name, vals in results.items():
        r_mean = np.mean([v[0] for v in vals])
        r_std = np.std([v[0] for v in vals])
        tp_mean = np.mean([v[1] for v in vals])
        tp_std = np.std([v[1] for v in vals])
        agg[name] = (r_mean, r_std, tp_mean, tp_std)
        print(f"{name:<15} {r_mean:>10.1f} {'±':>3}{r_std:.0f} {tp_mean:>12.2f} {'±':>3}{tp_std:.2f}")

    # Key comparisons
    gnn_tp = agg['GNN'][2]
    fc_tp = agg['FC'][2]
    gr_tp = agg['Greedy'][2]
    ia_tp = agg['IA-Greedy'][2]

    print(f"\nGNN vs FC:        {(gnn_tp-fc_tp)/fc_tp*100:+.2f}%")
    print(f"GNN vs Greedy:    {(gnn_tp-gr_tp)/gr_tp*100:+.2f}%")
    print(f"GNN vs IA-Greedy: {(gnn_tp-ia_tp)/ia_tp*100:+.2f}%")
    print(f"IA-Greedy vs Greedy: {(ia_tp-gr_tp)/gr_tp*100:+.2f}%  (env interference sensitivity)")

    print("\n--- MVE Verdict ---")
    margin_vs_fc = (gnn_tp - fc_tp) / fc_tp * 100
    margin_vs_greedy = (gnn_tp - gr_tp) / gr_tp * 100

    if margin_vs_fc >= 5 and margin_vs_greedy >= 10:
        print(f"PASS: GNN > FC by {margin_vs_fc:.1f}% AND GNN > Greedy by {margin_vs_greedy:.1f}%")
    elif margin_vs_fc > 0 or margin_vs_greedy > 0:
        print(f"CONDITIONAL: GNN shows positive signal but below threshold")
        print(f"  GNN > FC: {margin_vs_fc:+.1f}%, GNN > Greedy: {margin_vs_greedy:+.1f}%")
    else:
        print(f"FAIL: GNN not better than FC or Greedy")


if __name__ == "__main__":
    main()
