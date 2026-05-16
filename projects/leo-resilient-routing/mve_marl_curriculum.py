"""
MVE-3: MARL + Curriculum Learning + Proactive Pre-routing
for LEO Fault-Resilient Routing

Part A: Does progressive fault complexity training (curriculum) improve
        MARL routing performance vs direct training on hard faults?
Part B: Does proactive pre-routing (predict ISL failure) reduce
        transition packet loss vs reactive-only handling?

Environment: 6x10 = 60 node grid (Walker delta proxy)
Agent: Shared-parameter DQN (each node = agent instance, shared network)
"""

import numpy as np
import torch
import torch.nn as nn
from collections import deque
import random
import json
import sys
import time

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ==================== Grid Environment ====================

class GridEnv:
    """Grid topology routing with link failures."""

    def __init__(self, rows=6, cols=10):
        self.rows, self.cols = rows, cols
        self.N = rows * cols
        self.base_adj = {}
        for r in range(rows):
            for c in range(cols):
                n = r * cols + c
                nbrs = {}
                if r > 0:     nbrs[0] = (r - 1) * cols + c       # North
                if r < rows - 1: nbrs[1] = (r + 1) * cols + c     # South
                if c < cols - 1: nbrs[2] = r * cols + (c + 1)     # East
                if c > 0:     nbrs[3] = r * cols + (c - 1)        # West
                self.base_adj[n] = nbrs

    # --- fault generation ---

    def _bfs_connected(self, link_up):
        adj = {n: [] for n in range(self.N)}
        for (a, b), up in link_up.items():
            if up:
                adj[a].append(b)
        visited = {0}
        q = deque([0])
        while q:
            n = q.popleft()
            for nb in adj[n]:
                if nb not in visited:
                    visited.add(nb)
                    q.append(nb)
        return len(visited) == self.N

    def gen_faults(self, level, rng=None):
        """Generate fault config. level 0-4."""
        if rng is None:
            rng = random
        if level == 0:
            return []
        n_faults = [0, 2, 5, 8, 12][level]
        correlated = level >= 3

        all_links = [(n, d) for n, nbrs in self.base_adj.items() for d in nbrs]
        rng.shuffle(all_links)

        link_up = {
            (n, nb): True
            for n, nbrs in self.base_adj.items()
            for d, nb in nbrs.items()
        }
        faults = []

        for i in range(min(n_faults * 4, len(all_links))):
            if len(faults) >= n_faults:
                break

            if correlated and faults and rng.random() < 0.5:
                prev_n = faults[-1][0]
                cands = [
                    (prev_n, d)
                    for d in self.base_adj[prev_n]
                    if (prev_n, d) not in faults
                ]
                if cands:
                    n, d = rng.choice(cands)
                else:
                    n, d = all_links[i]
            else:
                n, d = all_links[i]

            if d not in self.base_adj[n]:
                continue
            nb = self.base_adj[n][d]

            link_up[(n, nb)] = False
            link_up[(nb, n)] = False
            if self._bfs_connected(link_up):
                faults.append((n, d))
            else:
                link_up[(n, nb)] = True
                link_up[(nb, n)] = True

        return faults

    # --- episode control ---

    def reset(self, n_flows=20, fault_links=None, rng=None):
        if rng is None:
            rng = random
        self.link_up = {}
        for n, nbrs in self.base_adj.items():
            for d, nb in nbrs.items():
                self.link_up[(n, nb)] = True

        if fault_links:
            for n, d in fault_links:
                if d in self.base_adj[n]:
                    nb = self.base_adj[n][d]
                    self.link_up[(n, nb)] = False
                    self.link_up[(nb, n)] = False

        self.queues = {n: deque() for n in range(self.N)}
        self.pkt_info = []
        nodes = list(range(self.N))
        for i in range(n_flows):
            src, dst = rng.sample(nodes, 2)
            self.queues[src].append(
                {"id": i, "dst": dst, "ttl": 40, "hops": 0}
            )
            self.pkt_info.append({"delivered": False, "dropped": False, "hops": 0})

        self.step_count = 0
        self.done = False
        self.n_flows = n_flows
        return self._get_obs()

    def _get_obs(self):
        """(N, 7) float32: [queue_util, 4xlink_status, dx, dy]"""
        obs = np.zeros((self.N, 7), dtype=np.float32)
        for n in range(self.N):
            obs[n, 0] = len(self.queues[n]) / 20.0
            for d in range(4):
                if d in self.base_adj[n]:
                    nb = self.base_adj[n][d]
                    obs[n, 1 + d] = 1.0 if self.link_up.get((n, nb), False) else 0.0
                else:
                    obs[n, 1 + d] = -1.0
            if self.queues[n]:
                pkt = self.queues[n][0]
                dr = pkt["dst"] // self.cols - n // self.cols
                dc = pkt["dst"] % self.cols - n % self.cols
                obs[n, 5] = dc / max(self.cols - 1, 1)
                obs[n, 6] = dr / max(self.rows - 1, 1)
        return obs

    def get_valid_mask(self):
        mask = np.zeros((self.N, 4), dtype=bool)
        for n in range(self.N):
            for d in range(4):
                if d in self.base_adj[n]:
                    nb = self.base_adj[n][d]
                    if self.link_up.get((n, nb), False):
                        mask[n, d] = True
        return mask

    def has_packets(self):
        return np.array([len(self.queues[n]) > 0 for n in range(self.N)])

    def step(self, actions):
        """actions: (N,) int array, -1 = no-op."""
        if self.done:
            return self._get_obs(), 0.0, True, {}

        self.step_count += 1
        step_del = step_drop = 0
        transfers = {}

        for n in range(self.N):
            if not self.queues[n]:
                continue
            a = actions[n]
            valid = [
                d
                for d in range(4)
                if d in self.base_adj[n]
                and self.link_up.get((n, self.base_adj[n][d]), False)
            ]
            if not valid:
                continue
            if a not in valid:
                a = random.choice(valid)

            nb = self.base_adj[n][a]
            pkt = self.queues[n].popleft()
            pkt["hops"] += 1
            pkt["ttl"] -= 1

            if nb == pkt["dst"]:
                step_del += 1
                self.pkt_info[pkt["id"]]["delivered"] = True
                self.pkt_info[pkt["id"]]["hops"] = pkt["hops"]
            elif pkt["ttl"] <= 0 or pkt["hops"] >= 60:
                step_drop += 1
                self.pkt_info[pkt["id"]]["dropped"] = True
            else:
                transfers.setdefault(nb, []).append(pkt)

        for n, pkts in transfers.items():
            for p in pkts:
                if len(self.queues[n]) < 20:
                    self.queues[n].append(p)
                else:
                    step_drop += 1
                    self.pkt_info[p["id"]]["dropped"] = True

        total_q = sum(len(q) for q in self.queues.values())
        reward = step_del * 1.0 - step_drop * 0.5 - total_q * 0.001

        n_fin = sum(
            1 for p in self.pkt_info if p["delivered"] or p["dropped"]
        )
        self.done = n_fin >= self.n_flows or self.step_count >= 80

        info = {
            "delivered": sum(1 for p in self.pkt_info if p["delivered"]),
            "dropped": sum(1 for p in self.pkt_info if p["dropped"]),
            "total": self.n_flows,
            "avg_hops": np.mean(
                [p["hops"] for p in self.pkt_info if p["delivered"]] or [0]
            ),
            "step": self.step_count,
        }
        return self._get_obs(), reward, self.done, info


# ==================== DQN Agent ====================

class DQN(nn.Module):
    def __init__(self, state_dim=7, n_actions=4, hidden=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, 32),
            nn.ReLU(),
            nn.Linear(32, n_actions),
        )

    def forward(self, x):
        return self.net(x)


class Agent:
    def __init__(self, lr=0.001, gamma=0.95, eps_start=1.0):
        self.policy_net = DQN().to(DEVICE)
        self.target_net = DQN().to(DEVICE)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.optimizer = torch.optim.Adam(self.policy_net.parameters(), lr=lr)
        self.gamma = gamma
        self.eps = eps_start
        self.eps_min = 0.05
        self.eps_decay = 0.995
        self.buf = deque(maxlen=10000)
        self.train_count = 0

    def act_batch(self, obs, valid_mask, has_pkt):
        N = obs.shape[0]
        actions = np.full(N, -1, dtype=int)
        active = np.where(has_pkt)[0]
        if len(active) == 0:
            return actions

        active_obs = torch.FloatTensor(obs[active]).to(DEVICE)
        with torch.no_grad():
            q = self.policy_net(active_obs).cpu().numpy()

        for i, n in enumerate(active):
            valid = np.where(valid_mask[n])[0]
            if len(valid) == 0:
                continue
            if random.random() < self.eps:
                actions[n] = random.choice(valid)
            else:
                q_masked = np.full(4, -1e9)
                q_masked[valid] = q[i, valid]
                actions[n] = int(np.argmax(q_masked))
        return actions

    def store(self, obs, actions, reward, next_obs, done, valid_mask, has_pkt):
        for n in range(len(actions)):
            if actions[n] >= 0 and has_pkt[n]:
                self.buf.append(
                    (
                        obs[n].copy(),
                        actions[n],
                        reward,
                        next_obs[n].copy(),
                        done,
                        valid_mask[n].copy(),
                    )
                )

    def learn(self, batch_size=64):
        if len(self.buf) < batch_size:
            return 0.0
        batch = random.sample(self.buf, batch_size)
        s, a, r, s2, d, v = zip(*batch)

        sv = torch.FloatTensor(np.array(s)).to(DEVICE)
        av = torch.LongTensor(a).to(DEVICE)
        rv = torch.FloatTensor(r).to(DEVICE)
        s2v = torch.FloatTensor(np.array(s2)).to(DEVICE)
        dv = torch.FloatTensor(d).to(DEVICE).float()

        q_curr = self.policy_net(sv).gather(1, av.unsqueeze(1)).squeeze(1)
        with torch.no_grad():
            q_next = self.target_net(s2v)
            vm = torch.FloatTensor(np.array(v)).to(DEVICE)
            q_next = q_next.masked_fill(~vm.bool(), -1e9)
            q_target = rv + self.gamma * q_next.max(1)[0] * (1 - dv)

        loss = nn.MSELoss()(q_curr, q_target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.train_count += 1
        if self.train_count % 200 == 0:
            self.target_net.load_state_dict(self.policy_net.state_dict())
        return loss.item()

    def decay_eps(self):
        self.eps = max(self.eps_min, self.eps * self.eps_decay)


# ==================== Training ====================

def train_one_ep(env, agent, fault_level, seed=None):
    rng = random.Random(seed) if seed else random
    faults = env.gen_faults(fault_level, rng)
    obs = env.reset(n_flows=20, fault_links=faults, rng=rng)
    total_r = 0
    while not env.done:
        valid = env.get_valid_mask()
        has_pkt = env.has_packets()
        actions = agent.act_batch(obs, valid, has_pkt)
        next_obs, r, done, info = env.step(actions)
        agent.store(obs, actions, r, next_obs, done, valid, has_pkt)
        agent.learn()
        total_r += r
        obs = next_obs
    agent.decay_eps()
    return total_r, info


def train_curriculum(env, total_eps=1500):
    agent = Agent()
    # L0:0faults(300) -> L1:2faults(350) -> L2:5faults(400) -> L3:8faults+corr(450)
    stages = [(0, 300), (1, 350), (2, 400), (3, 450)]
    rewards_log = []
    for level, n_ep in stages:
        for i in range(n_ep):
            r, info = train_one_ep(env, agent, level)
            rewards_log.append(r)
            if (i + 1) % 100 == 0:
                print(
                    f"  Curriculum L{level} [{i+1}/{n_ep}] "
                    f"r100={np.mean(rewards_log[-100:]):.2f} "
                    f"del={info['delivered']}/{info['total']} "
                    f"eps={agent.eps:.3f}"
                )
    return agent, rewards_log


def train_direct(env, total_eps=1500):
    agent = Agent()
    rewards_log = []
    for i in range(total_eps):
        r, info = train_one_ep(env, agent, 3)
        rewards_log.append(r)
        if (i + 1) % 100 == 0:
            print(
                f"  Direct [{i+1}/{total_eps}] "
                f"r100={np.mean(rewards_log[-100:]):.2f} "
                f"del={info['delivered']}/{info['total']} "
                f"eps={agent.eps:.3f}"
            )
    return agent, rewards_log


# ==================== Evaluation ====================

def gen_test_scenarios(env, n_per=5):
    rng = random.Random(12345)
    scenarios = {}
    scenarios["easy_2f"] = [env.gen_faults(1, rng) for _ in range(n_per)]
    scenarios["med_5f"] = [env.gen_faults(2, rng) for _ in range(n_per)]
    scenarios["hard_8f"] = [env.gen_faults(3, rng) for _ in range(n_per)]
    scenarios["vhard_12f"] = [env.gen_faults(4, rng) for _ in range(n_per)]

    cor = []
    for _ in range(n_per):
        r, c = rng.randint(1, env.rows - 2), rng.randint(1, env.cols - 2)
        node = r * env.cols + c
        fl = [(node, d) for d in list(env.base_adj[node].keys())[:3]]
        cor.append(fl)
    scenarios["correlated"] = cor
    return scenarios


def evaluate(env, agent, scenarios, n_eps_per=5):
    agent.eps = 0.0
    rng = random.Random(99999)
    results = {}
    for name, fault_list in scenarios.items():
        deliveries, drops = [], []
        for faults in fault_list:
            for _ in range(n_eps_per):
                obs = env.reset(n_flows=20, fault_links=faults, rng=rng)
                while not env.done:
                    valid = env.get_valid_mask()
                    has_pkt = env.has_packets()
                    actions = agent.act_batch(obs, valid, has_pkt)
                    obs, _, done, info = env.step(actions)
                deliveries.append(info["delivered"] / info["total"])
                drops.append(info["dropped"] / info["total"])
        results[name] = {
            "delivery": np.mean(deliveries),
            "drop": np.mean(drops),
        }
    return results


# ==================== Part B: Proactive Pre-routing ====================

def greedy_route(env, valid_mask):
    actions = np.full(env.N, -1, dtype=int)
    for n in range(env.N):
        if not env.queues[n]:
            continue
        pkt = env.queues[n][0]
        dst = pkt["dst"]
        dr, dc = dst // env.cols, dst % env.cols
        best_d, best_dist = -1, float("inf")
        for d in range(4):
            if not valid_mask[n, d]:
                continue
            nb = env.base_adj[n][d]
            nr, nc = nb // env.cols, nb % env.cols
            dist = abs(nr - dr) + abs(nc - dc)
            if dist < best_dist:
                best_dist = dist
                best_d = d
        if best_d >= 0:
            actions[n] = best_d
        else:
            valid_ds = np.where(valid_mask[n])[0]
            if len(valid_ds) > 0:
                actions[n] = valid_ds[0]
    return actions


def proactive_test(env, n_trials=40, warning_steps=3):
    rng = random.Random(54321)
    results = {"proactive": [], "reactive": []}

    for trial in range(n_trials):
        r, c = rng.randint(0, env.rows - 1), rng.randint(0, env.cols - 1)
        node = r * env.cols + c
        dirs = list(env.base_adj[node].keys())
        sched_dir = rng.choice(dirs) if dirs else 0
        base_faults = env.gen_faults(1, rng)

        for mode in ["proactive", "reactive"]:
            obs = env.reset(n_flows=20, fault_links=base_faults, rng=rng)

            for step in range(80):
                if env.done:
                    break

                # Proactive: start avoiding scheduled link early
                if mode == "proactive" and step >= (10 - warning_steps):
                    if sched_dir in env.base_adj[node]:
                        nb = env.base_adj[node][sched_dir]
                        env.link_up[(node, nb)] = False
                        env.link_up[(nb, node)] = False

                # Actual failure at step 10
                if step == 10 and sched_dir in env.base_adj[node]:
                    nb = env.base_adj[node][sched_dir]
                    env.link_up[(node, nb)] = False
                    env.link_up[(nb, node)] = False

                valid = env.get_valid_mask()
                actions = greedy_route(env, valid)
                obs, _, _, info = env.step(actions)

            results[mode].append(info["delivered"] / info["total"])

    return results


# ==================== Main ====================

def main():
    t0 = time.time()
    print("=" * 60)
    print("MVE-3: MARL + Curriculum Learning + Proactive Pre-routing")
    print(f"Network: 6x10 = 60 nodes | Device: {DEVICE}")
    print("=" * 60)

    env = GridEnv(rows=6, cols=10)

    # ---- Part A ----
    print("\n[Part A] Curriculum vs Direct Training\n")
    print("--- Curriculum (L0 300 -> L1 350 -> L2 400 -> L3 450) ---")
    curr_agent, _ = train_curriculum(env, 1500)

    print("\n--- Direct (1500 eps on L3 = 8 faults + correlated) ---")
    direct_agent, _ = train_direct(env, 1500)

    print("\n--- Evaluation on Test Scenarios ---")
    test_sc = gen_test_scenarios(env)
    curr_res = evaluate(env, curr_agent, test_sc)
    direct_res = evaluate(env, direct_agent, test_sc)

    print(f"\n{'Scenario':<16} {'Curriculum':>10} {'Direct':>10} {'Delta':>8}")
    print("-" * 46)
    for name in test_sc:
        c = curr_res[name]["delivery"]
        d = direct_res[name]["delivery"]
        print(f"{name:<16} {c:>9.1%} {d:>9.1%} {c-d:>+7.1%}")

    c_avg = np.mean([curr_res[k]["delivery"] for k in test_sc])
    d_avg = np.mean([direct_res[k]["delivery"] for k in test_sc])
    delta_a = c_avg - d_avg
    print(f"{'AVERAGE':<16} {c_avg:>9.1%} {d_avg:>9.1%} {delta_a:>+7.1%}")

    if delta_a >= 0.05:
        part_a_verdict = "PASS"
    elif delta_a >= 0.02:
        part_a_verdict = "CONDITIONAL"
    else:
        part_a_verdict = "FAIL"
    print(f"\nPart A verdict: {part_a_verdict} (delta={delta_a:+.1%})")

    # ---- Part B ----
    print(f"\n[Part B] Proactive vs Reactive Pre-routing\n")
    part_b = proactive_test(env, n_trials=40, warning_steps=3)

    pro = np.mean(part_b["proactive"])
    rea = np.mean(part_b["reactive"])
    delta_b = pro - rea

    print(f"Proactive: {pro:.1%} | Reactive: {rea:.1%} | Delta: {delta_b:+.1%}")

    if delta_b >= 0.05:
        part_b_verdict = "PASS"
    elif delta_b >= 0.02:
        part_b_verdict = "CONDITIONAL"
    else:
        part_b_verdict = "FAIL"
    print(f"Part B verdict: {part_b_verdict} (delta={delta_b:+.1%})")

    # ---- Overall ----
    print("\n" + "=" * 60)
    if part_a_verdict == "PASS" and part_b_verdict == "PASS":
        overall = "PASS"
    elif part_a_verdict in ("PASS", "CONDITIONAL") or part_b_verdict in (
        "PASS",
        "CONDITIONAL",
    ):
        overall = "CONDITIONAL"
    else:
        overall = "FAIL"
    print(f"OVERALL: {overall}")
    print(f"  Part A (Curriculum): {part_a_verdict} ({delta_a:+.1%})")
    print(f"  Part B (Proactive):  {part_b_verdict} ({delta_b:+.1%})")

    elapsed = time.time() - t0
    print(f"\nTime: {elapsed:.0f}s")

    # Save
    out = {
        "part_a": {
            "curriculum_avg": float(c_avg),
            "direct_avg": float(d_avg),
            "delta": float(delta_a),
            "verdict": part_a_verdict,
            "per_scenario": {
                k: {
                    "curr": float(curr_res[k]["delivery"]),
                    "direct": float(direct_res[k]["delivery"]),
                }
                for k in test_sc
            },
        },
        "part_b": {
            "proactive": float(pro),
            "reactive": float(rea),
            "delta": float(delta_b),
            "verdict": part_b_verdict,
        },
        "overall": overall,
        "elapsed_s": elapsed,
    }
    outfile = "mve3_results.json"
    with open(outfile, "w") as f:
        json.dump(out, f, indent=2)
    print(f"Results saved to {outfile}")


if __name__ == "__main__":
    main()
