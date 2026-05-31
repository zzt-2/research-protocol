"""GRLR evaluation: compare with Dijkstra and our method on 720-star.

Supports two inference modes:
  --mode greedy:  per-hop argmax (original GRLR)
  --mode weighted: GNN-weighted Dijkstra (fair comparison with our method)
"""
import argparse
import numpy as np
import torch

from config import CONFIGS
from constellation import WalkerDelta
from snapshot import build_snapshot
from topology import build_adjacency
from routing import dijkstra, dijkstra_all_pairs
from env import _build_neighbor_map
from grlr_model import GRLRModel, build_local_graphs

MAX_HOPS = 80


def eval_greedy(model, walker, snap, neighbor_map, dist_mat, pairs, device):
    """Per-hop argmax routing."""
    N = walker.N
    all_stretches, all_gnn, all_djk = [], [], []
    n_success, n_total = 0, 0

    for src, dst in pairs:
        if src == dst:
            continue
        n_total += 1
        cur, delay, visited, reached = int(src), 0.0, {int(src)}, False

        for _ in range(MAX_HOPS):
            if cur == dst:
                reached = True
                break
            graph, vmask = build_local_graphs([cur], dst, snap, walker, neighbor_map)
            graph = graph.to(device)
            with torch.no_grad():
                logits, _ = model(graph)
            logits = logits.squeeze(0).cpu()
            valid = vmask.squeeze(0)
            logits[~valid] = -1e9
            action = logits.argmax().item()
            nb_key = (cur, action)
            if nb_key not in neighbor_map:
                break
            nxt, hd = neighbor_map[nb_key]
            delay += hd
            if nxt in visited:
                break
            visited.add(nxt)
            cur = nxt

        djk = dist_mat[src, dst]
        if reached and np.isfinite(djk) and djk > 0:
            all_stretches.append(delay / djk)
            all_gnn.append(delay)
            all_djk.append(djk)
            n_success += 1

    return all_stretches, all_gnn, all_djk, n_success, n_total


def eval_weighted(model, walker, snap, neighbor_map, dist_mat, pairs, device):
    """GNN-weighted Dijkstra: logits → edge weights → shortest path."""
    N = walker.N

    # Collect unique destinations
    dests = set(int(d) for _, d in pairs if _ != d)

    all_stretches, all_gnn, all_djk = [], [], []
    n_success, n_total = 0, 0

    for dst in dests:
        # Get logits for ALL nodes toward this destination
        node_list = list(range(N))
        all_logits = np.zeros((N, 4), dtype=np.float32)
        batch_size = 64

        for start in range(0, N, batch_size):
            batch = node_list[start:start + batch_size]
            graph, vmask = build_local_graphs(batch, dst, snap, walker, neighbor_map)
            graph = graph.to(device)
            with torch.no_grad():
                logits, _ = model(graph)
            logits = logits.cpu().numpy()
            valid = vmask.numpy()
            logits[~valid] = -1e9
            for i, nid in enumerate(batch):
                all_logits[nid] = logits[i]

        # Build weighted adjacency: delay + relu(best_logit - logit)
        best_logit = np.max(all_logits, axis=-1)
        adj_w = [[] for _ in range(N)]
        edge_dir = {}
        for (u, d), (v, delay) in neighbor_map.items():
            edge_dir[(u, v)] = d
            penalty = max(0.0, best_logit[u] - all_logits[u, d])
            adj_w[u].append((v, delay + penalty))

        # Route all pairs for this destination
        for src, d in pairs:
            if int(d) != dst or int(src) == dst:
                continue
            n_total += 1
            src = int(src)
            dw, par = dijkstra(adj_w, src, N)
            if dw[dst] == np.inf or par[dst] < 0:
                continue

            cur, path = dst, []
            while cur != src and cur >= 0:
                path.append(cur)
                cur = par[cur]
            if cur != src:
                continue
            path.append(src)
            path.reverse()

            actual = 0.0
            ok = True
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                if (u, v) not in edge_dir:
                    ok = False
                    break
                _, hd = neighbor_map[(u, edge_dir[(u, v)])]
                actual += hd
            if not ok:
                continue

            djk = dist_mat[src, dst]
            if np.isfinite(djk) and djk > 0:
                all_stretches.append(actual / djk)
                all_gnn.append(actual)
                all_djk.append(djk)
                n_success += 1

    return all_stretches, all_gnn, all_djk, n_success, n_total


def evaluate(args):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    cfg = CONFIGS['target_720']
    walker = WalkerDelta(cfg['P'], cfg['S'], cfg['F'], cfg['alt'], cfg['inc'])
    N = walker.N
    print(f"Constellation: {walker.P}x{walker.S} = {N} sats, mode={args.mode}")

    model = GRLRModel().to(device)
    model.load_state_dict(torch.load(args.model, map_location=device))
    model.eval()

    rng = np.random.default_rng(args.seed)
    eval_fn = eval_greedy if args.mode == 'greedy' else eval_weighted

    all_s, all_g, all_d, tot_succ, tot_total = [], [], [], 0, 0

    for snap_idx in range(args.n_snapshots):
        t = rng.uniform(0, walker.period)
        snap = build_snapshot(walker, t)
        nmap = _build_neighbor_map(snap, walker.S, walker.P)
        adj = build_adjacency(N, snap['edge_index'], snap['edge_delay'])
        dist_mat, _ = dijkstra_all_pairs(adj, N)

        for tm_idx in range(args.n_flows):
            pairs = rng.choice(N, size=(args.n_flows_per_tm, 2), replace=True)
            s, g, d, ns, nt = eval_fn(model, walker, snap, nmap, dist_mat, pairs, device)
            all_s.extend(s)
            all_g.extend(g)
            all_d.extend(d)
            tot_succ += ns
            tot_total += nt

        print(f"  Snapshot {snap_idx+1}/{args.n_snapshots}: "
              f"{tot_succ}/{tot_total} success ({tot_succ/tot_total:.1%})")

    stretches = np.array(all_s)
    print(f"\n{'='*60}")
    print(f"GRLR Results ({args.mode}, {args.n_snapshots} snapshots, 720-star)")
    print(f"{'='*60}")
    print(f"Success rate:  {tot_succ/tot_total:.1%} ({tot_succ}/{tot_total})")
    if len(stretches) > 0:
        print(f"Mean stretch:  {stretches.mean():.3f}")
        print(f"Median stretch:{np.median(stretches):.3f}")
        print(f"P95 stretch:   {np.percentile(stretches, 95):.3f}")
        print(f"Optimality ≤1.2x: {(stretches <= 1.2).mean():.1%}")
        print(f"Optimality ≤1.5x: {(stretches <= 1.5).mean():.1%}")
        print(f"Delay (ms): GNN mean={np.mean(all_g):.2f}  Dijkstra mean={np.mean(all_d):.2f}")
    print(f"{'='*60}")

    np.save(args.output, dict(
        method=f'GRLR_{args.mode}', success_rate=tot_succ / tot_total,
        mean_stretch=float(stretches.mean()) if len(stretches) else float('inf'),
        median_stretch=float(np.median(stretches)) if len(stretches) else float('inf'),
        p95_stretch=float(np.percentile(stretches, 95)) if len(stretches) else float('inf'),
        optimality_1_2=float((stretches <= 1.2).mean()) if len(stretches) else 0.0,
    ))
    print(f"Saved to {args.output}")


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--model', default='grlr_trained.pt')
    p.add_argument('--mode', choices=['greedy', 'weighted'], default='weighted')
    p.add_argument('--n_snapshots', type=int, default=10)
    p.add_argument('--n_flows', type=int, default=5)
    p.add_argument('--n_flows_per_tm', type=int, default=50)
    p.add_argument('--seed', type=int, default=123)
    p.add_argument('--output', default='grlr_results.npy')
    args = p.parse_args()
    evaluate(args)
