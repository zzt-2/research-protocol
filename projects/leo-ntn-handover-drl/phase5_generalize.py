"""Phase 5: Size Generalization evaluation.

Load models trained at 20 UE cap=25, evaluate at 50/100 UE cap=25 without retraining.
Self-contained to avoid argparse conflicts with training scripts.
"""

import json
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

import config as cfg
from simulator.environment import LEOSatHandoverEnv

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
K = 6
GNN_OUT = 64
HIDDEN_DIM = 32
T_GNN = 2


# ── GNN Architecture (copied from c_gnn_ddqn.py) ───────────────────────────
class MPNNEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        H = HIDDEN_DIM
        self.ue_proj = nn.Linear(4, H)
        self.sat_proj = nn.Linear(2, H)
        msg_in = H * 2 + 3
        self.msg_u2s = nn.Sequential(nn.Linear(msg_in, H), nn.ReLU())
        self.msg_s2u = nn.Sequential(nn.Linear(msg_in, H), nn.ReLU())
        self.upd_sat = nn.Sequential(nn.Linear(H * 2, H), nn.ReLU())
        self.upd_ue = nn.Sequential(nn.Linear(H * 2, H), nn.ReLU())
        self.ln_s = nn.LayerNorm(H)
        self.ln_u = nn.LayerNorm(H)
        self.ue_out = nn.Linear(H, GNN_OUT)
        self.sat_out = nn.Linear(H, GNN_OUT)

    def forward(self, ue_x, sat_x, edge_x, mask):
        B, K_, _ = sat_x.shape
        h_u = self.ue_proj(ue_x)
        h_s = self.sat_proj(sat_x)
        mf = mask.unsqueeze(-1).float()
        for _ in range(T_GNN):
            hu = h_u.unsqueeze(1).expand(-1, K_, -1)
            m = self.msg_u2s(torch.cat([hu, h_s, edge_x], -1))
            h_s = self.ln_s(h_s + self.upd_sat(torch.cat([h_s, m], -1)))
            h_s = h_s * mf
            m = self.msg_s2u(torch.cat([h_s, hu, edge_x], -1))
            agg = (m * mf).sum(1) / mf.sum(1).clamp(min=1)
            h_u = self.ln_u(h_u + self.upd_ue(torch.cat([h_u, agg], -1)))
        return self.ue_out(h_u), self.sat_out(h_s)


class GNNQNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.gnn = MPNNEncoder()
        self.v_net = nn.Sequential(
            nn.Linear(GNN_OUT, GNN_OUT), nn.ReLU(), nn.Linear(GNN_OUT, 1))
        self.a_net = nn.Sequential(
            nn.Linear(GNN_OUT * 2 + 3, GNN_OUT), nn.ReLU(), nn.Linear(GNN_OUT, 1))

    def forward(self, ue_x, sat_x, edge_x, mask):
        h_u, h_s = self.gnn(ue_x, sat_x, edge_x, mask)
        v = self.v_net(h_u)
        hu = h_u.unsqueeze(1).expand_as(h_s)
        a = self.a_net(torch.cat([hu, h_s, edge_x], -1)).squeeze(-1)
        mf = mask.float()
        a_mean = (a * mf).sum(1, keepdim=True) / mf.sum(1, keepdim=True).clamp(min=1)
        q = v + a - a_mean
        return q.masked_fill(~mask, float('-inf'))


# ── MLP Architecture (copied from b2_topk.py) ───────────────────────────────
FLAT_DIM = 4 + K * 5


class DuelingNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.shared = nn.Sequential(
            nn.Linear(FLAT_DIM, 128), nn.ReLU(),
            nn.Linear(128, 64), nn.ReLU())
        self.v_stream = nn.Linear(64, 1)
        self.a_stream = nn.Linear(64, K)

    def forward(self, x, mask):
        f = self.shared(x)
        v = self.v_stream(f)
        a = self.a_stream(f)
        mf = mask.float()
        a_mean = (a * mf).sum(1, keepdim=True) / mf.sum(1, keepdim=True).clamp(min=1)
        q = v + a - a_mean
        return q.masked_fill(~mask, float('-inf'))


# ── Shared helpers ──────────────────────────────────────────────────────────
def _orbit_phase(sat_idx, step):
    sat_in_plane = sat_idx % cfg.SATS_PER_PLANE
    return ((step * cfg.DT_S) / cfg.ORBIT_PERIOD_S + sat_in_plane / cfg.SATS_PER_PLANE) % 1.0


def build_graph(obs_ue, step, prev_sat, was_blocked):
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

    sat_feats = np.zeros((K, 2), dtype=np.float32)
    edge_feats = np.zeros((K, 3), dtype=np.float32)
    for ki in range(K):
        if not valid[ki]:
            continue
        si = top_k_idx[ki]
        sat_feats[ki, 0] = 1.0 - load[si]
        sat_feats[ki, 1] = _orbit_phase(si, step)
        edge_feats[ki] = [sinr[si], elev[si], is_cur[si]]

    return ue_feat, sat_feats, edge_feats, valid, top_k_idx


def build_flat(obs_ue, step, prev_sat, was_blocked):
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
    return np.concatenate([ue_feat, cand_feat.flatten()]), valid, top_k_idx


# ── Evaluators ──────────────────────────────────────────────────────────────
def eval_gnn(env, net, seed):
    net.eval()
    obs = env.reset(seed=seed)
    prev = np.full(env.num_ues, -1, dtype=int)
    blk = np.zeros(env.num_ues, dtype=bool)
    total_r, ho, blk_s, steps = 0.0, 0, 0.0, 0
    ue_throughput = np.zeros(env.num_ues)
    done = False
    while not done:
        graphs = [build_graph(obs[u], env._step, prev[u], blk[u]) for u in range(env.num_ues)]
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
            g_act[u] = graphs[u][4][int(q[u].argmax().item())]
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


def eval_mlp(env, net, seed):
    net.eval()
    obs = env.reset(seed=seed)
    prev = np.full(env.num_ues, -1, dtype=int)
    blk = np.zeros(env.num_ues, dtype=bool)
    total_r, ho, blk_s, steps = 0.0, 0, 0.0, 0
    ue_throughput = np.zeros(env.num_ues)
    done = False
    while not done:
        flats, masks, topks = [], [], []
        for u in range(env.num_ues):
            f, mk, tk = build_flat(obs[u], env._step, prev[u], blk[u])
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


# ── Main ────────────────────────────────────────────────────────────────────
def main():
    gnn_path = PROJECT_ROOT / 'results' / 'E4-20-c25_model.pt'
    mlp_path = PROJECT_ROOT / 'results' / 'C6-20-c25_model.pt'
    eval_ues = [50, 100]
    sat_cap = 25
    seeds = [100, 200, 300]

    print("=" * 70)
    print("Phase 5: Size Generalization — 20UE trained → 50/100UE eval")
    print("=" * 70)

    # Load GNN
    gnn_ckpt = torch.load(gnn_path, map_location=DEVICE, weights_only=False)
    gnn_net = GNNQNetwork().to(DEVICE)
    gnn_net.load_state_dict(gnn_ckpt['net'])
    gnn_net.eval()
    print(f"GNN model loaded from {gnn_path}")

    # Load MLP
    mlp_ckpt = torch.load(mlp_path, map_location=DEVICE, weights_only=False)
    mlp_net = DuelingNet().to(DEVICE)
    mlp_net.load_state_dict(mlp_ckpt['net'])
    mlp_net.eval()
    print(f"MLP model loaded from {mlp_path}")

    gnn_results, mlp_results = [], []
    for n_ues in eval_ues:
        print(f"\n--- {n_ues} UE, cap={sat_cap} ---")
        g_eps, m_eps = [], []
        for s in seeds:
            env = LEOSatHandoverEnv(num_ues=n_ues, sat_capacity=sat_cap, seed=s)
            gm = eval_gnn(env, gnn_net, s)
            gm['seed'] = s; gm['num_ues'] = n_ues
            g_eps.append(gm)

            env2 = LEOSatHandoverEnv(num_ues=n_ues, sat_capacity=sat_cap, seed=s)
            mm = eval_mlp(env2, mlp_net, s)
            mm['seed'] = s; mm['num_ues'] = n_ues
            m_eps.append(mm)

            print(f"  seed={s}: GNN r={gm['reward']:.0f} blk={gm['blocking']:.4f} | "
                  f"MLP r={mm['reward']:.0f} blk={mm['blocking']:.4f}")

        gnn_results.append({
            'num_ues': n_ues,
            'reward_mean': float(np.mean([e['reward'] for e in g_eps])),
            'reward_std': float(np.std([e['reward'] for e in g_eps])),
            'blocking_mean': float(np.mean([e['blocking'] for e in g_eps])),
            'handover_mean': float(np.mean([e['handovers'] for e in g_eps])),
        })
        mlp_results.append({
            'num_ues': n_ues,
            'reward_mean': float(np.mean([e['reward'] for e in m_eps])),
            'reward_std': float(np.std([e['reward'] for e in m_eps])),
            'blocking_mean': float(np.mean([e['blocking'] for e in m_eps])),
            'handover_mean': float(np.mean([e['handovers'] for e in m_eps])),
        })

    # Summary
    print(f"\n{'=' * 70}")
    print("Size Generalization Summary (trained 20UE → eval N UE)")
    print(f"{'=' * 70}")
    print(f"{'UEs':>6} | {'GNN reward':>12} {'GNN blk':>10} | {'MLP reward':>12} {'MLP blk':>10} | {'Gap':>8}")
    print("-" * 75)
    for g, m in zip(gnn_results, mlp_results):
        n = g['num_ues']
        gap = (g['reward_mean'] - m['reward_mean']) / abs(m['reward_mean']) * 100 if m['reward_mean'] != 0 else 0
        print(f"{n:>6} | {g['reward_mean']:>12.0f} {g['blocking_mean']:>10.4f} | "
              f"{m['reward_mean']:>12.0f} {m['blocking_mean']:>10.4f} | {gap:>+7.1f}%")

    # Save
    out = PROJECT_ROOT / 'results' / 'phase5_generalize.json'
    with open(out, 'w') as f:
        json.dump({'gnn': gnn_results, 'mlp': mlp_results,
                    'train_ues': 20, 'eval_ues': eval_ues, 'sat_capacity': sat_cap}, f, indent=2)
    print(f"\nSaved to {out}")


if __name__ == '__main__':
    main()
