"""Detailed stretch distribution for weighted Dijkstra."""
import sys, os
import numpy as np
import torch

sys.path.insert(0, os.path.dirname(__file__))

from config import CONFIGS, TRAIN_CONFIGS, TARGET_CONFIG, PE_DIM
from models import RoutingActorCritic
from env import RoutingEnv

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
PRETRAINED = os.path.join(os.path.dirname(__file__), 'pretrained.pt')


@torch.no_grad()
def detailed_eval(model, config_name, n_episodes=20, n_flows=100, seed=123):
    env = RoutingEnv([config_name], n_sources=n_flows, pe_dim=PE_DIM, seed=seed)
    model.eval()

    all_stretches = []
    ep_stretches = []

    for ei in range(n_episodes):
        ep = env.reset()
        data = ep['data'].to(DEVICE)
        logits, _ = model(data)
        masked = logits.clone()
        masked[~data.dir_mask] = -1e8
        logits_np = masked.cpu().numpy()

        _, info = RoutingEnv.evaluate_weighted(ep, logits_np)
        ep_mean = info['mean_stretch'] if info['mean_stretch'] < float('inf') else None
        if ep_mean is not None:
            ep_stretches.append(ep_mean)

        # Also compute per-flow stretches manually
        from routing import dijkstra
        nmap = ep['neighbor_map']
        N = ep['N']
        dest = ep['dest']
        dist_mat = ep['dist_mat']
        best_logit = np.max(logits_np, axis=-1)

        adj = [[] for _ in range(N)]
        edge_dir = {}
        for (u, d), (v, delay) in nmap.items():
            edge_dir[(u, v)] = d
            penalty = max(0.0, best_logit[u] - logits_np[u, d])
            adj[u].append((v, delay + penalty))

        for src in ep['sources']:
            src = int(src)
            dist_w, parent = dijkstra(adj, src, N)
            if dist_w[dest] == np.inf or parent[dest] < 0:
                continue
            cur, path = dest, []
            while cur != src and cur >= 0:
                path.append(cur)
                cur = parent[cur]
            if cur != src:
                continue
            path.append(src)
            path.reverse()

            actual_delay = 0.0
            ok = True
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                if (u, v) not in edge_dir:
                    ok = False
                    break
                _, hd = nmap[(u, edge_dir[(u, v)])]
                actual_delay += hd
            if not ok:
                continue

            djk_delay = dist_mat[src, dest]
            if np.isfinite(djk_delay) and djk_delay > 0:
                all_stretches.append(actual_delay / djk_delay)

    arr = np.array(all_stretches)
    print(f"\n{config_name} ({len(arr)} successful flows):")
    print(f"  Mean: {arr.mean():.4f}  Median: {np.median(arr):.4f}  "
          f"P95: {np.percentile(arr, 95):.4f}  Max: {arr.max():.4f}")
    print(f"  >1.5: {(arr > 1.5).sum()} ({(arr>1.5).mean():.1%})  "
          f">2.0: {(arr > 2.0).sum()} ({(arr>2.0).mean():.1%})  "
          f">3.0: {(arr > 3.0).sum()} ({(arr>3.0).mean():.1%})")


def main():
    node_dim = 1 + PE_DIM * 2
    model = RoutingActorCritic(node_dim=node_dim, edge_dim=2, hidden=128,
                                n_layers=3, heads=4).to(DEVICE)
    state = torch.load(PRETRAINED, map_location=DEVICE, weights_only=True)
    model.load_state_dict(state)
    print(f"Loaded pretrained ({DEVICE})")

    for cfg in TRAIN_CONFIGS + [TARGET_CONFIG]:
        detailed_eval(model, cfg)


if __name__ == '__main__':
    main()
