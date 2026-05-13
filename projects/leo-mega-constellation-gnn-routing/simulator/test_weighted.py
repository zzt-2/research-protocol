"""Quick test: GNN-weighted Dijkstra vs greedy inference.

Loads pretrained model, compares greedy path tracing vs weighted Dijkstra.
"""
import sys
import os
import time
import numpy as np
import torch

sys.path.insert(0, os.path.dirname(__file__))

from config import CONFIGS, TRAIN_CONFIGS, TARGET_CONFIG, PE_DIM
from models import RoutingActorCritic
from env import RoutingEnv

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
PRETRAINED = os.path.join(os.path.dirname(__file__), 'pretrained.pt')


@torch.no_grad()
def evaluate_both(model, config_name, n_episodes=20, n_flows=200, seed=123):
    env = RoutingEnv([config_name], n_sources=n_flows, pe_dim=PE_DIM, seed=seed)
    model.eval()

    greedy_sr, greedy_st, weighted_sr, weighted_st = [], [], [], []

    for _ in range(n_episodes):
        ep = env.reset()
        data = ep['data'].to(DEVICE)
        logits, _ = model(data)
        masked = logits.clone()
        masked[~data.dir_mask] = -1e8

        # Greedy
        dirs = masked.argmax(dim=-1).cpu().numpy()
        _, info_g = RoutingEnv.evaluate_directions(ep, dirs)
        greedy_sr.append(info_g['success_rate'])
        if info_g['mean_stretch'] < float('inf'):
            greedy_st.append(info_g['mean_stretch'])

        # Weighted Dijkstra
        logits_np = masked.cpu().numpy()
        _, info_w = RoutingEnv.evaluate_weighted(ep, logits_np)
        weighted_sr.append(info_w['success_rate'])
        if info_w['mean_stretch'] < float('inf'):
            weighted_st.append(info_w['mean_stretch'])

    return dict(
        greedy_sr=np.mean(greedy_sr), greedy_st=np.mean(greedy_st) if greedy_st else float('inf'),
        weighted_sr=np.mean(weighted_sr), weighted_st=np.mean(weighted_st) if weighted_st else float('inf'),
    )


def main():
    print("=" * 60)
    print("GREEDY vs GNN-WEIGHTED DIJKSTRA")
    print("=" * 60)
    print(f"Device: {DEVICE}")

    node_dim = 1 + PE_DIM * 2
    model = RoutingActorCritic(node_dim=node_dim, edge_dim=2, hidden=128,
                                n_layers=3, heads=4).to(DEVICE)
    state = torch.load(PRETRAINED, map_location=DEVICE, weights_only=True)
    model.load_state_dict(state)
    print(f"Loaded: {PRETRAINED}\n")

    print(f"{'Config':16s} | {'Greedy SR':>9s} {'Stretch':>7s} | {'Weighted SR':>11s} {'Stretch':>7s}")
    print("-" * 60)

    for cfg in TRAIN_CONFIGS + [TARGET_CONFIG]:
        r = evaluate_both(model, cfg, n_episodes=20, n_flows=300)
        tag = "TRAIN" if cfg in TRAIN_CONFIGS else "TARGET"
        print(f"{cfg:16s} | {r['greedy_sr']:8.1%} {r['greedy_st']:7.3f} | "
              f"{r['weighted_sr']:10.1%} {r['weighted_st']:7.3f}  [{tag}]")

    print("=" * 60)


if __name__ == '__main__':
    main()
