"""Debug: inspect weighted Dijkstra paths vs optimal."""
import sys, os
import numpy as np
import torch

sys.path.insert(0, os.path.dirname(__file__))

from config import CONFIGS, TRAIN_CONFIGS, PE_DIM
from models import RoutingActorCritic
from env import RoutingEnv
from topology import build_adjacency
from routing import dijkstra, dijkstra_all_pairs

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def debug_one(config_name):
    env = RoutingEnv([config_name], n_sources=10, pe_dim=PE_DIM, seed=42)
    node_dim = 1 + PE_DIM * 2
    model = RoutingActorCritic(node_dim=node_dim, edge_dim=2, hidden=128,
                                n_layers=3, heads=4).to(DEVICE)
    state = torch.load(os.path.join(os.path.dirname(__file__), 'pretrained.pt'),
                       map_location=DEVICE, weights_only=True)
    model.load_state_dict(state)
    model.eval()

    ep = env.reset()
    data = ep['data'].to(DEVICE)
    with torch.no_grad():
        logits, _ = model(data)

    masked = logits.clone()
    masked[~data.dir_mask] = -1e8
    logits_np = masked.cpu().numpy()
    dir_mask_np = data.dir_mask.cpu().numpy()
    nmap = ep['neighbor_map']
    N = ep['N']
    dest = ep['dest']

    # Pure Dijkstra on delay
    adj_delay = build_adjacency(N, ep['data'].edge_index.cpu().numpy().T if hasattr(ep['data'].edge_index, 'cpu') else ep['data'].edge_index.numpy().T,
                                np.zeros(ep['data'].edge_attr.shape[0]))  # dummy
    # Rebuild with actual delays
    adj_pure = [[] for _ in range(N)]
    edge_dir = {}
    for (u, d), (v, delay) in nmap.items():
        edge_dir[(u, v)] = d
        adj_pure[u].append((v, delay))

    # Weighted adjacency
    best_logit = np.max(logits_np, axis=-1)
    adj_weighted = [[] for _ in range(N)]
    for (u, d), (v, delay) in nmap.items():
        penalty = max(0.0, best_logit[u] - logits_np[u, d])
        w = delay + penalty
        adj_weighted[u].append((v, w))

    # Analyze a few flows
    print(f"\n{'='*60}")
    print(f"Config: {config_name} (N={N}, dest={dest})")
    print(f"{'='*60}")

    # Logit distribution
    pred_dirs = logits_np.argmax(axis=-1)
    correct_count = 0
    total_count = 0
    for u in range(N):
        if u == dest:
            continue
        # What direction should u take? Check all neighbors for path to dest
        dist_pure, parent_pure = dijkstra(adj_pure, u, N)
        if parent_pure[dest] < 0:
            continue
        # Trace optimal next hop
        cur = dest
        while parent_pure[cur] != u and parent_pure[cur] >= 0:
            cur = parent_pure[cur]
        if parent_pure[cur] == u:
            nh = cur
            if (u, nh) in edge_dir:
                optimal_dir = edge_dir[(u, nh)]
                total_count += 1
                if pred_dirs[u] == optimal_dir:
                    correct_count += 1

    acc = correct_count / max(total_count, 1)
    print(f"Next-hop direction accuracy: {acc:.4f} ({correct_count}/{total_count})")

    # Sample flows
    for i, src in enumerate(ep['sources'][:5]):
        src = int(src)

        # Pure Dijkstra
        dist_pure, parent_pure = dijkstra(adj_pure, src, N)
        pure_delay = dist_pure[dest]

        # Trace pure path
        path_pure = []
        cur = dest
        while cur != src and parent_pure[cur] >= 0:
            path_pure.append(cur)
            cur = parent_pure[cur]
        path_pure.append(src)
        path_pure.reverse()
        n_hops_pure = len(path_pure) - 1

        # Weighted Dijkstra
        dist_w, parent_w = dijkstra(adj_weighted, src, N)
        weighted_cost = dist_w[dest]

        # Trace weighted path (actual delay)
        cur = dest
        path_w = []
        while cur != src and parent_w[cur] >= 0:
            path_w.append(cur)
            cur = parent_w[cur]
        path_w.append(src)
        path_w.reverse()
        n_hops_w = len(path_w) - 1

        # Actual delay of weighted path
        actual_delay = 0.0
        for j in range(len(path_w) - 1):
            u, v = path_w[j], path_w[j+1]
            d = edge_dir.get((u, v), -1)
            if d >= 0:
                _, hop_d = nmap[(u, d)]
                actual_delay += hop_d

        stretch = actual_delay / pure_delay if pure_delay > 0 else float('inf')

        # Count wrong predictions on weighted path
        wrong_on_path = 0
        for j in range(len(path_w) - 1):
            u, v = path_w[j], path_w[j+1]
            if (u, v) in edge_dir:
                actual_d = edge_dir[(u, v)]
                if pred_dirs[u] != actual_d:
                    wrong_on_path += 1

        print(f"\n  Flow {src}→{dest}:")
        print(f"    Pure Dijkstra: {n_hops_pure} hops, delay={pure_delay:.1f}ms")
        print(f"    Weighted path: {n_hops_w} hops, actual_delay={actual_delay:.1f}ms, "
              f"weighted_cost={weighted_cost:.1f}, stretch={stretch:.3f}")
        print(f"    Wrong preds on weighted path: {wrong_on_path}/{n_hops_w}")


for cfg in ['train_100', 'target_720']:
    debug_one(cfg)
