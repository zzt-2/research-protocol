"""GRLR training: Vanilla Actor-Critic on 720-star constellation.

Trains GRLR model (6-node local graph GAT + AC) using on-policy policy gradient.
Per Table III: gamma=0.95, lr=5e-4, entropy_beta=0.1, Adam optimizer.
Reward: r_t = -d_k (negative hop delay) + arrival bonus / timeout penalty.
"""
import sys
import argparse
import numpy as np
import torch
import torch.nn.functional as F
from torch.distributions import Categorical

from config import CONFIGS, N_SNAPSHOTS, SNAPSHOT_INTERVAL
from constellation import WalkerDelta
from snapshot import build_snapshot
from topology import build_adjacency
from routing import dijkstra, dijkstra_all_pairs
from env import _build_neighbor_map
from grlr_model import GRLRModel, build_local_graphs

# GRLR Table III params
GAMMA = 0.95
LR = 5e-4
ENTROPY_BETA = 0.1
ARRIVAL_BONUS = 10.0
TIMEOUT_PENALTY = 50.0
MAX_HOPS = 80


def train(args):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")

    # Build 720-star constellation
    cfg = CONFIGS['target_720']
    walker = WalkerDelta(cfg['P'], cfg['S'], cfg['F'], cfg['alt'], cfg['inc'])
    print(f"Constellation: {walker.P}x{walker.S} = {walker.N} sats, alt={cfg['alt']}km")

    model = GRLRModel().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)
    print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")

    rng = np.random.default_rng(args.seed)
    torch.manual_seed(args.seed)

    best_reward = -float('inf')
    log_every = 50

    for ep in range(args.episodes):
        # Sample snapshot and source-dest pair
        t = rng.uniform(0, walker.period)
        snap = build_snapshot(walker, t)
        neighbor_map = _build_neighbor_map(snap, walker.S, walker.P)

        N = walker.N
        adj = build_adjacency(N, snap['edge_index'], snap['edge_delay'])
        dist_mat, _ = dijkstra_all_pairs(adj, N)

        # Sample n_routes source-dest pairs
        n_routes = 10  # GRLR: 10 iterations per episode
        srcs = rng.choice(N, size=n_routes, replace=False)
        dsts = rng.choice(N, size=n_routes, replace=False)

        ep_rewards = []
        ep_entropies = []
        ep_stretches = []

        for src, dst in zip(srcs, dsts):
            if src == dst:
                continue

            # Route one packet: collect trajectory
            log_probs, values, rewards, entropies = [], [], [], []
            cur = int(src)
            visited = {cur}
            total_delay = 0.0

            for hop in range(MAX_HOPS):
                if cur == dst:
                    break

                # Build local graph
                graph, valid_mask = build_local_graphs(
                    [cur], dst, snap, walker, neighbor_map)
                graph = graph.to(device)

                logits, value = model(graph)
                logits = logits.squeeze(0)  # (4,)
                value = value.squeeze(0)    # scalar

                # Mask invalid directions
                valid = valid_mask.squeeze(0).to(device)
                logits[~valid] = -1e9

                # Sample action
                dist = Categorical(logits=logits)
                action = dist.sample()

                log_probs.append(dist.log_prob(action))
                values.append(value)
                entropies.append(dist.entropy())

                # Check if action is valid
                if not valid[action.item()]:
                    rewards.append(-TIMEOUT_PENALTY / MAX_HOPS)
                    break

                # Execute action
                nb_key = (cur, action.item())
                if nb_key not in neighbor_map:
                    rewards.append(-TIMEOUT_PENALTY / MAX_HOPS)
                    break

                nxt, hop_delay = neighbor_map[nb_key]
                total_delay += hop_delay

                if nxt == dst:
                    rewards.append(-hop_delay + ARRIVAL_BONUS)
                elif nxt in visited:
                    rewards.append(-hop_delay - TIMEOUT_PENALTY / MAX_HOPS)
                    break
                else:
                    rewards.append(-hop_delay)

                visited.add(nxt)
                cur = nxt
            else:
                # Max hops exceeded — penalty on last stored transition
                rewards[-1] -= TIMEOUT_PENALTY

            # Compute returns
            returns = []
            R = 0.0
            for r in reversed(rewards):
                R = r + GAMMA * R
                returns.insert(0, R)
            returns = torch.tensor(returns, dtype=torch.float32, device=device)

            # Compute advantages
            values_t = torch.stack(values) if values else torch.tensor([])
            if len(values_t) > 0:
                # Bootstrap from last value if not terminal
                advantages = returns - values_t.detach()
            else:
                continue

            # Policy loss
            log_probs_t = torch.stack(log_probs)
            policy_loss = -(log_probs_t * advantages).mean()

            # Value loss
            value_loss = F.mse_loss(values_t, returns)

            # Entropy bonus
            entropy = torch.stack(entropies).mean()

            # Total loss
            loss = policy_loss + 0.5 * value_loss - ENTROPY_BETA * entropy

            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 0.5)
            optimizer.step()

            # Track metrics
            djk_delay = dist_mat[src, dst]
            if cur == dst and np.isfinite(djk_delay) and djk_delay > 0:
                ep_stretches.append(total_delay / djk_delay)
            ep_rewards.append(sum(rewards))
            ep_entropies.append(entropy.item())

        # Logging
        if (ep + 1) % log_every == 0:
            avg_r = np.mean(ep_rewards)
            avg_s = np.mean([s for s in ep_stretches if np.isfinite(s)])
            avg_e = np.mean(ep_entropies)
            best_reward = max(best_reward, avg_r)
            print(f"Ep {ep+1:4d} | reward {avg_r:8.2f} | "
                  f"stretch {avg_s:6.2f} | entropy {avg_e:4.3f} | "
                  f"best {best_reward:8.2f}")

        # Save best model
        if ep_rewards and np.mean(ep_rewards) > best_reward:
            best_reward = np.mean(ep_rewards)
            torch.save(model.state_dict(), args.output)
            print(f"  → Saved best model (reward={best_reward:.2f})")

    # Final save
    torch.save(model.state_dict(), args.output)
    print(f"Training done. Model saved to {args.output}")


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--episodes', type=int, default=2000)
    p.add_argument('--seed', type=int, default=42)
    p.add_argument('--output', default='grlr_trained.pt')
    args = p.parse_args()
    train(args)
