"""C1: GNN + Dueling DDQN for LEO satellite handover (minimal first version).

Per-UE bipartite graph (1 UE + top-K=6 sats) + MPNN-E encoder + decomposed Q.
Quick sanity check: 10 episodes training, 3 seeds evaluation.
No pretrain phase for v1 — pure end-to-end.
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

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

import config as cfg
from simulator.environment import LEOSatHandoverEnv

# ── CLI arguments ─────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser()
parser.add_argument('--name', default='c1', help='Experiment name (output file)')
parser.add_argument('--gnn_lr', type=float, default=1e-3)
parser.add_argument('--drl_lr', type=float, default=1e-3)
parser.add_argument('--eps_decay', type=int, default=5)
parser.add_argument('--target_update', type=int, default=500)
parser.add_argument('--episodes', type=int, default=50)
parser.add_argument('--buffer', type=int, default=50_000)
parser.add_argument('--batch', type=int, default=128)
parser.add_argument('--grad_clip', type=float, default=1.0)
parser.add_argument('--K', type=int, default=6)
parser.add_argument('--hidden', type=int, default=32)
parser.add_argument('--gnn_out', type=int, default=64)
parser.add_argument('--T', type=int, default=2)
parser.add_argument('--no_orbit', action='store_true', help='Disable orbit_phase feature')
parser.add_argument('--num_ues', type=int, default=cfg.NUM_UES, help='Number of UEs')
parser.add_argument('--sat_capacity', type=int, default=cfg.SAT_CAPACITY, help='Satellite capacity')
parser.add_argument('--train_seed', type=int, default=42, help='Training random seed')
args = parser.parse_args()

K = args.K
HIDDEN_DIM = args.hidden
GNN_OUT = args.gnn_out
T_GNN = args.T
GNN_LR = args.gnn_lr
DRL_LR = args.drl_lr
GAMMA = 0.99
EPS_START = 0.5
EPS_END = 0.05
EPS_DECAY = args.eps_decay
BUFFER_SIZE = args.buffer
BATCH_SIZE = args.batch
TARGET_UPDATE = args.target_update
NUM_TRAIN_EP = args.episodes
NUM_EVAL_SEEDS = 3
GRAD_CLIP = args.grad_clip
EXP_NAME = args.name

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ── Graph Builder ─────────────────────────────────────────────────────────────
class GraphBuilder:
    """Build per-UE bipartite graph from flat observation."""

    def __init__(self):
        self.K = K
        self.N = cfg.NUM_SATS

    def build(self, obs_ue, step, prev_sat, was_blocked=False):
        """Parse flat obs into structured graph data for one UE.

        Flat obs layout: [sinr_norm(N), elev_norm(N), load_norm(N), is_current(N), t_conn(1)]
        Returns: (ue_feat, sat_feats, edge_feats, valid_mask, top_k_indices)
        """
        N = self.N
        sinr = obs_ue[0:N]
        elev = obs_ue[N:2 * N]
        load = obs_ue[2 * N:3 * N]     # 1 - connections/capacity
        is_cur = obs_ue[3 * N:4 * N]
        t_conn = obs_ue[4 * N]

        # Top-K by elevation (elev=0 for non-visible)
        visible = np.where(elev > 0)[0]
        top_k_idx = np.zeros(self.K, dtype=int)
        valid = np.zeros(self.K, dtype=bool)

        if len(visible) > 0:
            order = visible[np.argsort(-elev[visible])]
            sel = order[:self.K]
            top_k_idx[:len(sel)] = sel
            valid[:len(sel)] = True

        # UE features: [t_conn, sinr_serving, load_serving, is_blocked]
        cur = int(prev_sat) if prev_sat >= 0 else 0
        ue_feat = np.array([
            t_conn,
            sinr[cur] if prev_sat >= 0 else 0.0,
            load[cur] if prev_sat >= 0 else 0.0,
            1.0 if was_blocked else 0.0,
        ], dtype=np.float32)

        sat_feats = np.zeros((self.K, 2), dtype=np.float32)
        edge_feats = np.zeros((self.K, 3), dtype=np.float32)

        for ki in range(self.K):
            if not valid[ki]:
                continue
            si = top_k_idx[ki]
            sat_feats[ki, 0] = 1.0 - load[si]   # connections/capacity
            sat_feats[ki, 1] = _orbit_phase(si, step)
            edge_feats[ki] = [sinr[si], elev[si], is_cur[si]]

        return ue_feat, sat_feats, edge_feats, valid, top_k_idx


def _orbit_phase(sat_idx, step):
    if args.no_orbit:
        return 0.5
    sat_in_plane = sat_idx % cfg.SATS_PER_PLANE
    base = sat_in_plane / cfg.SATS_PER_PLANE
    t_frac = (step * cfg.DT_S) / cfg.ORBIT_PERIOD_S
    return (t_frac + base) % 1.0


# ── GNN Encoder (MPNN-E) ─────────────────────────────────────────────────────
class MPNNEncoder(nn.Module):
    """Edge-conditioned MPNN for per-UE bipartite subgraph (1 UE + K sats)."""

    def __init__(self):
        super().__init__()
        H = HIDDEN_DIM
        self.ue_proj = nn.Linear(4, H)
        self.sat_proj = nn.Linear(2, H)

        msg_in = H * 2 + 3  # [h_ue || h_sat || edge]
        self.msg_u2s = nn.Sequential(nn.Linear(msg_in, H), nn.ReLU())
        self.msg_s2u = nn.Sequential(nn.Linear(msg_in, H), nn.ReLU())
        self.upd_sat = nn.Sequential(nn.Linear(H * 2, H), nn.ReLU())
        self.upd_ue = nn.Sequential(nn.Linear(H * 2, H), nn.ReLU())

        self.ln_s = nn.LayerNorm(H)
        self.ln_u = nn.LayerNorm(H)

        self.ue_out = nn.Linear(H, GNN_OUT)
        self.sat_out = nn.Linear(H, GNN_OUT)

    def forward(self, ue_x, sat_x, edge_x, mask):
        """
        ue_x: (B,4)  sat_x: (B,K,2)  edge_x: (B,K,3)  mask: (B,K) bool
        Returns: h_ue (B, GNN_OUT), h_sat (B, K, GNN_OUT)
        """
        B, K_, _ = sat_x.shape
        h_u = self.ue_proj(ue_x)
        h_s = self.sat_proj(sat_x)
        mf = mask.unsqueeze(-1).float()

        for _ in range(T_GNN):
            hu = h_u.unsqueeze(1).expand(-1, K_, -1)

            # UE → Sat
            m = self.msg_u2s(torch.cat([hu, h_s, edge_x], -1))
            h_s = self.ln_s(h_s + self.upd_sat(torch.cat([h_s, m], -1)))
            h_s = h_s * mf

            # Sat → UE
            m = self.msg_s2u(torch.cat([h_s, hu, edge_x], -1))
            agg = (m * mf).sum(1) / mf.sum(1).clamp(min=1)
            h_u = self.ln_u(h_u + self.upd_ue(torch.cat([h_u, agg], -1)))

        return self.ue_out(h_u), self.sat_out(h_s)


# ── Decomposed Dueling Q ─────────────────────────────────────────────────────
class GNNQNetwork(nn.Module):
    """GNN encoder + V(h_ue) + A(h_ue, h_sat, edge) - mean(A)."""

    def __init__(self):
        super().__init__()
        self.gnn = MPNNEncoder()
        self.v_net = nn.Sequential(
            nn.Linear(GNN_OUT, GNN_OUT), nn.ReLU(), nn.Linear(GNN_OUT, 1))
        self.a_net = nn.Sequential(
            nn.Linear(GNN_OUT * 2 + 3, GNN_OUT), nn.ReLU(), nn.Linear(GNN_OUT, 1))

    def forward(self, ue_x, sat_x, edge_x, mask):
        """Returns Q: (B, K)"""
        h_u, h_s = self.gnn(ue_x, sat_x, edge_x, mask)
        v = self.v_net(h_u)
        hu = h_u.unsqueeze(1).expand_as(h_s)
        a = self.a_net(torch.cat([hu, h_s, edge_x], -1)).squeeze(-1)
        mf = mask.float()
        a_mean = (a * mf).sum(1, keepdim=True) / mf.sum(1, keepdim=True).clamp(min=1)
        q = v + a - a_mean
        return q.masked_fill(~mask, float('-inf'))


# ── Replay Buffer ─────────────────────────────────────────────────────────────
class Buf:
    def __init__(self, cap):
        self.d = deque(maxlen=cap)

    def push(self, ue, sa, ed, mk, a, r, nue, nsa, ned, nmk, dn):
        self.d.append((ue, sa, ed, mk, a, r, nue, nsa, ned, nmk, dn))

    def sample(self, bs):
        idx = np.random.choice(len(self.d), bs, replace=False)
        b = [self.d[i] for i in idx]
        return tuple(
            np.stack([x[i] for x in b]) if i != 4 else np.array([x[i] for x in b], dtype=np.int64)
            for i in range(11)
        )

    def __len__(self):
        return len(self.d)


# ── Episode runner ────────────────────────────────────────────────────────────
def run_ep(env, net, gb, eps, seed):
    obs = env.reset(seed=seed)
    prev = np.full(env.num_ues, -1, dtype=int)
    blk = np.zeros(env.num_ues, dtype=bool)
    trans = []
    total_r = 0.0
    done = False

    while not done:
        step_num = env._step
        graphs = [gb.build(obs[u], step_num, prev[u], blk[u]) for u in range(env.num_ues)]

        ue_x = torch.FloatTensor(np.stack([g[0] for g in graphs])).to(DEVICE)
        sa_x = torch.FloatTensor(np.stack([g[1] for g in graphs])).to(DEVICE)
        ed_x = torch.FloatTensor(np.stack([g[2] for g in graphs])).to(DEVICE)
        mk = torch.BoolTensor(np.stack([g[3] for g in graphs])).to(DEVICE)
        topk = [g[4] for g in graphs]

        with torch.no_grad():
            q = net(ue_x, sa_x, ed_x, mk)

        g_act = np.zeros(env.num_ues, dtype=int)
        l_act = np.zeros(env.num_ues, dtype=int)
        for u in range(env.num_ues):
            vk = np.where(graphs[u][3])[0]
            if len(vk) == 0:
                continue
            if np.random.random() < eps:
                la = np.random.choice(vk)
            else:
                la = int(q[u].argmax().item())
            l_act[u] = la
            g_act[u] = topk[u][la]

        nxt_obs, rews, done, info = env.step(g_act)
        nxt_blk = info['throughput_bps'] == 0

        nxt_step = env._step
        for u in range(env.num_ues):
            ng = gb.build(nxt_obs[u], nxt_step, g_act[u], nxt_blk[u])
            trans.append((
                graphs[u][0], graphs[u][1], graphs[u][2], graphs[u][3],
                l_act[u], rews[u],
                ng[0], ng[1], ng[2], ng[3],
                done,
            ))

        total_r += float(rews.sum())
        obs = nxt_obs
        prev = g_act.copy()
        blk = nxt_blk.copy()

    return trans, total_r


# ── Detailed Evaluation ───────────────────────────────────────────────────────
def evaluate(env, net, gb, seed):
    """Greedy evaluation returning detailed metrics."""
    net.eval()
    obs = env.reset(seed=seed)
    prev = np.full(env.num_ues, -1, dtype=int)
    blk = np.zeros(env.num_ues, dtype=bool)
    total_r = 0.0
    ho_count = 0
    blk_steps = 0
    step_count = 0
    ue_throughput = np.zeros(env.num_ues)
    sat_history = {u: [] for u in range(env.num_ues)}
    pp_count = 0
    done = False

    while not done:
        graphs = [gb.build(obs[u], env._step, prev[u], blk[u]) for u in range(env.num_ues)]
        ue_x = torch.FloatTensor(np.stack([g[0] for g in graphs])).to(DEVICE)
        sa_x = torch.FloatTensor(np.stack([g[1] for g in graphs])).to(DEVICE)
        ed_x = torch.FloatTensor(np.stack([g[2] for g in graphs])).to(DEVICE)
        mk = torch.BoolTensor(np.stack([g[3] for g in graphs])).to(DEVICE)

        with torch.no_grad():
            q = net(ue_x, sa_x, ed_x, mk)

        g_act = np.zeros(env.num_ues, dtype=int)
        for u in range(env.num_ues):
            vk = np.where(graphs[u][3])[0]
            if len(vk) == 0:
                continue
            la = int(q[u].argmax().item())
            g_act[u] = graphs[u][4][la]

        nxt_obs, rews, done, info = env.step(g_act)
        total_r += float(rews.sum())
        ho_count += int(info['handover_count'])
        blk_steps += float(info['blocking_rate'])
        ue_throughput += info['throughput_bps']
        step_count += 1

        # Ping-pong detection: UE returns to recently-used satellite
        for u in range(env.num_ues):
            if prev[u] != -1 and g_act[u] != prev[u]:
                if g_act[u] in sat_history[u][-3:]:
                    pp_count += 1
            sat_history[u].append(int(g_act[u]))
            if len(sat_history[u]) > 5:
                sat_history[u].pop(0)

        obs = nxt_obs
        prev = g_act.copy()
        blk = (info['throughput_bps'] == 0)

    # Jain's fairness index on per-UE cumulative throughput
    jain = float(np.sum(ue_throughput) ** 2 /
                 (env.num_ues * np.sum(ue_throughput ** 2) + 1e-12))

    net.train()
    return {
        'reward': float(total_r),
        'mean_blocking_rate': blk_steps / step_count,
        'total_handovers': ho_count,
        'mean_throughput_mbps': float(ue_throughput.mean() / step_count / 1e6),
        'jain_fairness': jain,
        'steps': step_count,
        'ping_pong_rate': float(pp_count / max(ho_count, 1)),
    }


# ── Training ──────────────────────────────────────────────────────────────────
def main():
    print(f"Device: {DEVICE}")
    torch.manual_seed(args.train_seed)
    np.random.seed(args.train_seed)
    env = LEOSatHandoverEnv(num_ues=args.num_ues, sat_capacity=args.sat_capacity, seed=args.train_seed)
    gb = GraphBuilder()

    net = GNNQNetwork().to(DEVICE)
    tgt = GNNQNetwork().to(DEVICE)
    tgt.load_state_dict(net.state_dict())
    tgt.eval()

    opt = torch.optim.Adam([
        {'params': net.gnn.parameters(), 'lr': GNN_LR},
        {'params': list(net.v_net.parameters()) + list(net.a_net.parameters()), 'lr': DRL_LR},
    ])
    buf = Buf(BUFFER_SIZE)

    n_param = sum(p.numel() for p in net.parameters())
    print(f"Parameters: {n_param:,}")
    print(f"K={K}, hidden={HIDDEN_DIM}, out={GNN_OUT}, T={T_GNN}")
    print(f"Train: {NUM_TRAIN_EP} episodes, eval: {NUM_EVAL_SEEDS} seeds\n")

    total_steps = 0
    r_log, l_log = [], []
    t0 = time.time()

    for ep in range(NUM_TRAIN_EP):
        eps = EPS_END + (EPS_START - EPS_END) * np.exp(-ep / EPS_DECAY)
        trans, ep_r = run_ep(env, net, gb, eps, seed=args.train_seed + ep)
        r_log.append(ep_r)

        for t in trans:
            buf.push(*t)

        ep_loss, n_upd = 0.0, 0
        if len(buf) >= BATCH_SIZE:
            for _ in range(max(1, len(trans) // BATCH_SIZE)):
                b = buf.sample(BATCH_SIZE)
                # b: (ue, sa, ed, mk, act, r, nue, nsa, ned, nmk, done)
                _to = lambda i: torch.from_numpy(b[i]).to(DEVICE) if i != 4 \
                    else torch.LongTensor(b[i]).unsqueeze(1).to(DEVICE)

                ue_t, sa_t, ed_t, mk_t = _to(0), _to(1), _to(2), torch.BoolTensor(b[3]).to(DEVICE)
                a_t, r_t = _to(4), _to(5)
                dn_t = torch.from_numpy(b[10].astype(np.float32)).to(DEVICE)
                nue_t, nsa_t, ned_t = _to(6), _to(7), _to(8)
                nmk_t = torch.BoolTensor(b[9]).to(DEVICE)

                q_val = net(ue_t, sa_t, ed_t, mk_t).gather(1, a_t).squeeze(1)
                with torch.no_grad():
                    nq_on = net(nue_t, nsa_t, ned_t, nmk_t)
                    n_a = nq_on.argmax(1, keepdim=True)
                    nq_tgt = tgt(nue_t, nsa_t, ned_t, nmk_t).gather(1, n_a).squeeze(1)
                    tgt_q = r_t + GAMMA * nq_tgt * (1 - dn_t)

                loss = nn.SmoothL1Loss()(q_val, tgt_q)
                opt.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(net.parameters(), GRAD_CLIP)
                opt.step()

                ep_loss += loss.item()
                n_upd += 1
                total_steps += 1
                if total_steps % TARGET_UPDATE == 0:
                    tgt.load_state_dict(net.state_dict())

        avg_l = ep_loss / max(n_upd, 1)
        l_log.append(avg_l)
        print(f"  ep {ep + 1:2d}/{NUM_TRAIN_EP} | r={ep_r:8.0f} | eps={eps:.3f} "
              f"| loss={avg_l:.4f} | buf={len(buf)}")

    dt = time.time() - t0
    print(f"\nTraining done in {dt:.1f}s")

    # Eval
    ev = []
    for s in [100, 200, 300][:NUM_EVAL_SEEDS]:
        eenv = LEOSatHandoverEnv(num_ues=args.num_ues, sat_capacity=args.sat_capacity, seed=s)
        m = evaluate(eenv, net, gb, s)
        m['seed'] = s
        ev.append(m)
        print(f"  eval seed={s}: reward={m['reward']:.0f} | blk={m['mean_blocking_rate']:.4f} "
              f"| HO={m['total_handovers']} | tput={m['mean_throughput_mbps']:.1f}Mbps "
              f"| jain={m['jain_fairness']:.3f}")

    # Save
    res = {
        'train': {
            'rewards': [float(x) for x in r_log],
            'losses': [float(x) for x in l_log],
            'time_s': round(dt, 1),
            'num_params': n_param,
        },
        'eval': ev,
        'config': {'K': K, 'hidden': HIDDEN_DIM, 'out': GNN_OUT, 'T': T_GNN,
                    'gnn_lr': GNN_LR, 'drl_lr': DRL_LR, 'gamma': GAMMA,
                    'eps_decay': EPS_DECAY, 'target_update': TARGET_UPDATE,
                    'episodes': NUM_TRAIN_EP, 'name': EXP_NAME,
                    'num_ues': args.num_ues, 'sat_capacity': args.sat_capacity,
                    'train_seed': args.train_seed},
    }
    out = PROJECT_ROOT / 'results' / f'{EXP_NAME}_s{args.train_seed}_results.json'
    out.parent.mkdir(exist_ok=True)
    with open(out, 'w') as f:
        json.dump(res, f, indent=2)

    # Save model checkpoint
    ckpt = PROJECT_ROOT / 'results' / f'{EXP_NAME}_s{args.train_seed}_model.pt'
    torch.save({'net': net.state_dict(), 'config': res['config']}, ckpt)
    print(f"Model saved to {ckpt}")

    # Summary
    rewards = [e['reward'] for e in ev]
    blks = [e['mean_blocking_rate'] for e in ev]
    hos = [e['total_handovers'] for e in ev]
    jains = [e['jain_fairness'] for e in ev]
    print(f"\n{'=' * 60}")
    print(f"C1 GNN+DDQN Summary")
    print(f"{'=' * 60}")
    print(f"  Params:     {n_param:,}")
    print(f"  Train:      {NUM_TRAIN_EP} ep, {dt:.1f}s")
    print(f"  Last-5 avg reward: {np.mean(r_log[-5:]):.0f}")
    print(f"  Eval ({NUM_EVAL_SEEDS} seeds):")
    print(f"    Reward:    {np.mean(rewards):.0f} +/- {np.std(rewards):.0f}")
    print(f"    Blocking:  {np.mean(blks):.4f}")
    print(f"    Handover:  {np.mean(hos):.0f}")
    print(f"    Jain's F:  {np.mean(jains):.3f}")


if __name__ == '__main__':
    main()
