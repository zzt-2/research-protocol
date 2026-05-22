"""C6 ablation: B2 Dueling DDQN with top-K compressed obs (no GNN).

Isolates top-K contribution vs GNN contribution.
Same top-K=6 candidates as C1, same action space (K), flat MLP instead of GNN.
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

parser = argparse.ArgumentParser()
parser.add_argument('--name', default='C6', help='Experiment name')
parser.add_argument('--num_ues', type=int, default=cfg.NUM_UES)
parser.add_argument('--sat_capacity', type=int, default=cfg.SAT_CAPACITY)
parser.add_argument('--episodes', type=int, default=50)
parser.add_argument('--K', type=int, default=6)
parser.add_argument('--buffer', type=int, default=50_000)
parser.add_argument('--eps_decay', type=int, default=20)
args = parser.parse_args()

K = args.K
FLAT_DIM = 4 + K * 5   # ue_feat(4) + K × [sinr, elev, load, orbit, is_cur]
LR = 1e-3
GAMMA = 0.99
EPS_START, EPS_END = 0.5, 0.05
EPS_DECAY = args.eps_decay
BUFFER_SIZE = args.buffer
BATCH_SIZE = 128
TARGET_UPDATE = 3000
NUM_EP = args.episodes
HIDDEN = (128, 64)
GRAD_CLIP = 1.0
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def _orbit_phase(sat_idx, step):
    sat_in_plane = sat_idx % cfg.SATS_PER_PLANE
    return ((step * cfg.DT_S) / cfg.ORBIT_PERIOD_S + sat_in_plane / cfg.SATS_PER_PLANE) % 1.0


def build_flat_obs(obs_ue, step, prev_sat, was_blocked):
    """Build flat top-K observation from env flat obs."""
    N = cfg.NUM_SATS
    sinr = obs_ue[0:N]
    elev = obs_ue[N:2 * N]
    load = obs_ue[2 * N:3 * N]
    is_cur = obs_ue[3 * N:4 * N]
    t_conn = obs_ue[4 * N]

    visible = np.where(elev > 0)[0]
    top_k_idx = np.zeros(K, dtype=int)
    valid = np.zeros(K, dtype=bool)
    if len(visible) > 0:
        order = visible[np.argsort(-elev[visible])]
        sel = order[:K]
        top_k_idx[:len(sel)] = sel
        valid[:len(sel)] = True

    cur = int(prev_sat) if prev_sat >= 0 else 0
    ue_feat = np.array([t_conn, sinr[cur] if prev_sat >= 0 else 0.0,
                         load[cur] if prev_sat >= 0 else 0.0,
                         1.0 if was_blocked else 0.0], dtype=np.float32)

    cand_feat = np.zeros((K, 5), dtype=np.float32)
    for ki in range(K):
        if not valid[ki]:
            continue
        si = top_k_idx[ki]
        cand_feat[ki] = [sinr[si], elev[si], 1.0 - load[si], _orbit_phase(si, step), is_cur[si]]

    flat = np.concatenate([ue_feat, cand_feat.flatten()])
    return flat, valid, top_k_idx


class DuelingNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.shared = nn.Sequential(
            nn.Linear(FLAT_DIM, HIDDEN[0]), nn.ReLU(),
            nn.Linear(HIDDEN[0], HIDDEN[1]), nn.ReLU())
        self.v_stream = nn.Linear(HIDDEN[1], 1)
        self.a_stream = nn.Linear(HIDDEN[1], K)

    def forward(self, x, mask):
        f = self.shared(x)
        v = self.v_stream(f)
        a = self.a_stream(f)
        mf = mask.float()
        a_mean = (a * mf).sum(1, keepdim=True) / mf.sum(1, keepdim=True).clamp(min=1)
        q = v + a - a_mean
        return q.masked_fill(~mask, float('-inf'))


class Buf:
    def __init__(self, cap):
        self.d = deque(maxlen=cap)

    def push(self, s, a, r, ns, d, mk, nmk):
        self.d.append((s, a, r, ns, d, mk, nmk))

    def sample(self, bs):
        idx = np.random.choice(len(self.d), bs, replace=False)
        b = [self.d[i] for i in idx]
        s = np.stack([x[0] for x in b])
        a = np.array([x[1] for x in b], dtype=np.int64)
        r = np.array([x[2] for x in b], dtype=np.float32)
        ns = np.stack([x[3] for x in b])
        d = np.array([x[4] for x in b], dtype=np.float32)
        mk = np.stack([x[5] for x in b])
        nmk = np.stack([x[6] for x in b])
        return s, a, r, ns, d, mk, nmk

    def __len__(self):
        return len(self.d)


def run_ep(env, net, eps, seed):
    obs = env.reset(seed=seed)
    prev = np.full(env.num_ues, -1, dtype=int)
    blk = np.zeros(env.num_ues, dtype=bool)
    trans = []
    total_r = 0.0
    done = False
    while not done:
        step_n = env._step
        flats, masks, topks = [], [], []
        for u in range(env.num_ues):
            f, mk, tk = build_flat_obs(obs[u], step_n, prev[u], blk[u])
            flats.append(f)
            masks.append(mk)
            topks.append(tk)

        f_t = torch.FloatTensor(np.stack(flats)).to(DEVICE)
        mk_t = torch.BoolTensor(np.stack(masks)).to(DEVICE)
        with torch.no_grad():
            q = net(f_t, mk_t)

        g_act = np.zeros(env.num_ues, dtype=int)
        l_act = np.zeros(env.num_ues, dtype=int)
        for u in range(env.num_ues):
            vk = np.where(masks[u])[0]
            if len(vk) == 0:
                continue
            if np.random.random() < eps:
                la = np.random.choice(vk)
            else:
                la = int(q[u].argmax().item())
            l_act[u] = la
            g_act[u] = topks[u][la]

        nxt_obs, rews, done, info = env.step(g_act)
        nxt_blk = info['throughput_bps'] == 0
        nxt_step = env._step

        for u in range(env.num_ues):
            nf, nmk, _ = build_flat_obs(nxt_obs[u], nxt_step, g_act[u], nxt_blk[u])
            trans.append((flats[u], l_act[u], rews[u], nf, done, masks[u], nmk))

        total_r += float(rews.sum())
        obs = nxt_obs
        prev = g_act.copy()
        blk = nxt_blk.copy()
    return trans, total_r


def evaluate(env, net, seed):
    net.eval()
    obs = env.reset(seed=seed)
    prev = np.full(env.num_ues, -1, dtype=int)
    blk = np.zeros(env.num_ues, dtype=bool)
    total_r = 0.0
    ho = 0
    blk_s = 0.0
    steps = 0
    ue_throughput = np.zeros(env.num_ues)
    done = False
    while not done:
        flats, masks, topks = [], [], []
        for u in range(env.num_ues):
            f, mk, tk = build_flat_obs(obs[u], env._step, prev[u], blk[u])
            flats.append(f); masks.append(mk); topks.append(tk)
        f_t = torch.FloatTensor(np.stack(flats)).to(DEVICE)
        mk_t = torch.BoolTensor(np.stack(masks)).to(DEVICE)
        with torch.no_grad():
            q = net(f_t, mk_t)
        g_act = np.zeros(env.num_ues, dtype=int)
        for u in range(env.num_ues):
            vk = np.where(masks[u])[0]
            if len(vk) == 0:
                continue
            g_act[u] = topks[u][int(q[u].argmax().item())]
        obs, rews, done, info = env.step(g_act)
        total_r += float(rews.sum())
        ho += int(info['handover_count'])
        blk_s += float(info['blocking_rate'])
        ue_throughput += info['throughput_bps']
        steps += 1
        prev = g_act.copy()
        blk = info['throughput_bps'] == 0
    jain = float(np.sum(ue_throughput) ** 2 /
                 (env.num_ues * np.sum(ue_throughput ** 2) + 1e-12))
    net.train()
    return {'reward': total_r, 'blocking': blk_s / steps, 'handovers': ho,
            'jain_fairness': jain}


def main():
    print(f"Device: {DEVICE} | obs_dim={FLAT_DIM} | K={K} | UEs={args.num_ues} | cap={args.sat_capacity}")
    env = LEOSatHandoverEnv(num_ues=args.num_ues, sat_capacity=args.sat_capacity, seed=42)
    net = DuelingNet().to(DEVICE)
    tgt = DuelingNet().to(DEVICE)
    tgt.load_state_dict(net.state_dict()); tgt.eval()
    opt = torch.optim.Adam(net.parameters(), lr=LR)
    buf = Buf(BUFFER_SIZE)
    n_param = sum(p.numel() for p in net.parameters())
    print(f"Params: {n_param:,} | {NUM_EP} episodes\n")

    total_steps = 0
    r_log, l_log = [], []
    t0 = time.time()

    for ep in range(NUM_EP):
        eps = EPS_END + (EPS_START - EPS_END) * np.exp(-ep / EPS_DECAY)
        trans, ep_r = run_ep(env, net, eps, seed=42)
        r_log.append(ep_r)
        for t in trans:
            buf.push(*t)

        ep_loss, n_upd = 0.0, 0
        if len(buf) >= BATCH_SIZE:
            for _ in range(max(1, len(trans) // BATCH_SIZE)):
                s, a, r, ns, d, mk, nmk = buf.sample(BATCH_SIZE)
                s_t = torch.FloatTensor(s).to(DEVICE)
                a_t = torch.LongTensor(a).unsqueeze(1).to(DEVICE)
                r_t = torch.FloatTensor(r).to(DEVICE)
                ns_t = torch.FloatTensor(ns).to(DEVICE)
                d_t = torch.FloatTensor(d).to(DEVICE)
                mk_t = torch.BoolTensor(mk).to(DEVICE)
                nmk_t = torch.BoolTensor(nmk).to(DEVICE)

                q = net(s_t, mk_t).gather(1, a_t).squeeze(1)
                with torch.no_grad():
                    nq = net(ns_t, nmk_t)
                    na = nq.argmax(1, keepdim=True)
                    nq_tgt = tgt(ns_t, nmk_t).gather(1, na).squeeze(1)
                    tgt_q = r_t + GAMMA * nq_tgt * (1 - d_t)
                loss = nn.SmoothL1Loss()(q, tgt_q)
                opt.zero_grad(); loss.backward()
                nn.utils.clip_grad_norm_(net.parameters(), GRAD_CLIP)
                opt.step()
                ep_loss += loss.item(); n_upd += 1; total_steps += 1
                if total_steps % TARGET_UPDATE == 0:
                    tgt.load_state_dict(net.state_dict())

        l_log.append(ep_loss / max(n_upd, 1))
        print(f"  ep {ep+1:2d}/{NUM_EP} | r={ep_r:8.0f} | eps={eps:.3f} "
              f"| loss={l_log[-1]:.4f} | buf={len(buf)}")

    dt = time.time() - t0
    print(f"\nTraining done in {dt:.1f}s")

    # Eval
    net.eval()
    ev = []
    for s in [100, 200, 300]:
        eenv = LEOSatHandoverEnv(num_ues=args.num_ues, sat_capacity=args.sat_capacity, seed=s)
        m = evaluate(eenv, net, s)
        m['seed'] = s
        ev.append(m)
        print(f"  eval seed={s}: reward={m['reward']:.0f} | blk={m['blocking']:.4f} | HO={m['handovers']}")

    res = {'train': {'rewards': [float(x) for x in r_log], 'losses': [float(x) for x in l_log],
                      'time_s': round(dt, 1), 'num_params': n_param},
           'eval': ev, 'config': {'K': K, 'flat_dim': FLAT_DIM, 'hidden': HIDDEN,
                                   'target_update': TARGET_UPDATE, 'eps_decay': EPS_DECAY,
                                   'num_ues': args.num_ues, 'sat_capacity': args.sat_capacity,
                                   'name': args.name}}
    out = PROJECT_ROOT / 'results' / f'{args.name}_results.json'
    out.parent.mkdir(exist_ok=True)
    with open(out, 'w') as f:
        json.dump(res, f, indent=2)
    # Save model checkpoint
    ckpt = PROJECT_ROOT / 'results' / f'{args.name}_model.pt'
    torch.save({'net': net.state_dict(), 'config': res['config']}, ckpt)
    print(f"Model saved to {ckpt}")
    print(f"\n{'='*50}\n{args.name} B2+topK Summary\n{'='*50}")
    print(f"  Params: {n_param:,} | Train: {NUM_EP}ep, {dt:.1f}s")
    print(f"  Last-5 avg: {np.mean(r_log[-5:]):.0f}")
    print(f"  Eval reward: {np.mean([e['reward'] for e in ev]):.0f}")
    print(f"  Eval blocking: {np.mean([e['blocking'] for e in ev]):.4f}")


if __name__ == '__main__':
    main()
