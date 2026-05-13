"""PPO fine-tuning with GNN-weighted Dijkstra reward.

Loads pretrained RoutingActorCritic, fine-tunes with PPO using
weighted Dijkstra stretch as reward (dense signal).
"""
import sys
import os
import time
import numpy as np
import torch
import torch.nn.functional as F
from torch.distributions import Categorical

sys.path.insert(0, os.path.dirname(__file__))

from config import (
    CONFIGS, TRAIN_CONFIGS, TARGET_CONFIG,
    PE_DIM, PPO_LR,
)
from models import RoutingActorCritic
from env import RoutingEnv

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

AC_LAYERS = 3
AC_HIDDEN = 128
AC_HEADS = 4

N_ITERATIONS = 80
BATCH_SIZE = 32
PPO_EPOCHS = 3
PPO_CLIP = 0.2
ENTROPY_COEF = 0.01
VALUE_COEF = 0.5
MAX_GRAD_NORM = 0.5
EVAL_INTERVAL = 20
N_EVAL_EPISODES = 20

PRETRAINED_PATH = os.path.join(os.path.dirname(__file__), 'pretrained.pt')


def _mask_logits(logits, dir_mask):
    masked = logits.clone()
    masked[~dir_mask] = -1e8
    all_masked = ~dir_mask.any(dim=-1)
    if all_masked.any():
        masked[all_masked] = 0.0
    return masked


def collect_batch(env, model, batch_size, device):
    model.eval()
    batch = []
    for _ in range(batch_size):
        ep = env.reset()
        data = ep['data'].to(device)

        with torch.no_grad():
            logits, value = model(data)

        masked = _mask_logits(logits, data.dir_mask)
        dist = Categorical(logits=masked)
        actions = dist.sample()
        mean_log_prob = dist.log_prob(actions).mean()

        # Reward from weighted Dijkstra (dense signal)
        logits_np = masked.cpu().numpy()
        reward, info = RoutingEnv.evaluate_weighted(ep, logits_np)

        batch.append(dict(
            data=data,
            actions=actions.cpu(),
            log_prob_old=mean_log_prob.item(),
            value_old=value.item(),
            reward=reward, info=info,
        ))
    return batch


def ppo_update(model, optimizer, batch, device):
    model.train()

    rewards = torch.tensor([b['reward'] for b in batch], dtype=torch.float32, device=device)
    values_old = torch.tensor([b['value_old'] for b in batch], dtype=torch.float32, device=device)
    log_probs_old = torch.tensor([b['log_prob_old'] for b in batch], dtype=torch.float32, device=device)

    advantages = rewards - values_old
    advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

    total_pi, total_v, total_ent = 0.0, 0.0, 0.0

    for epoch in range(PPO_EPOCHS):
        indices = torch.randperm(len(batch), device=device)
        for idx in indices:
            ep = batch[idx.item()]
            data = ep['data']

            logits, value = model(data)
            masked = _mask_logits(logits, data.dir_mask)

            dist = Categorical(logits=masked)
            log_prob_new = dist.log_prob(ep['actions'].to(device)).mean()
            entropy = dist.entropy().mean()

            ratio = torch.exp(log_prob_new - log_probs_old[idx])
            adv = advantages[idx]

            surr1 = ratio * adv
            surr2 = torch.clamp(ratio, 1 - PPO_CLIP, 1 + PPO_CLIP) * adv
            pi_loss = -torch.min(surr1, surr2)
            v_loss = F.mse_loss(value, rewards[idx].detach())

            loss = pi_loss + VALUE_COEF * v_loss - ENTROPY_COEF * entropy

            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), MAX_GRAD_NORM)
            optimizer.step()

            total_pi += pi_loss.item()
            total_v += v_loss.item()
            total_ent += entropy.item()

    n = len(batch) * PPO_EPOCHS
    return dict(policy_loss=total_pi / n, value_loss=total_v / n, entropy=total_ent / n)


@torch.no_grad()
def evaluate(model, config_name, n_episodes=20, n_flows=100, seed=123):
    env = RoutingEnv([config_name], n_sources=n_flows, pe_dim=PE_DIM, seed=seed)
    model.eval()

    all_sr, all_stretch = [], []

    for _ in range(n_episodes):
        ep = env.reset()
        data = ep['data'].to(DEVICE)
        logits, _ = model(data)
        masked = _mask_logits(logits, data.dir_mask)
        logits_np = masked.cpu().numpy()

        _, info = RoutingEnv.evaluate_weighted(ep, logits_np)
        all_sr.append(info['success_rate'])
        if info['mean_stretch'] < float('inf'):
            all_stretch.append(info['mean_stretch'])

    return dict(
        success_rate=np.mean(all_sr),
        mean_stretch=np.mean(all_stretch) if all_stretch else float('inf'),
        config=config_name,
    )


def main():
    print("=" * 60)
    print("PPO + WEIGHTED DIJKSTRA FINE-TUNING")
    print("=" * 60)
    print(f"Device: {DEVICE}")

    env = RoutingEnv(TRAIN_CONFIGS, n_sources=30, pe_dim=PE_DIM, seed=42)

    node_dim = 1 + PE_DIM * 2
    model = RoutingActorCritic(
        node_dim=node_dim, edge_dim=2, hidden=AC_HIDDEN,
        n_layers=AC_LAYERS, heads=AC_HEADS,
    ).to(DEVICE)

    if os.path.exists(PRETRAINED_PATH):
        state = torch.load(PRETRAINED_PATH, map_location=DEVICE, weights_only=True)
        model.load_state_dict(state)
        print(f"Loaded pretrained: {PRETRAINED_PATH}")
    else:
        print(f"WARNING: No pretrained weights. Run pretrain.py first.")

    n_params = sum(p.numel() for p in model.parameters())
    print(f"Parameters: {n_params:,}")
    print(f"Loop: {N_ITERATIONS} iters x batch={BATCH_SIZE} x PPO={PPO_EPOCHS}")

    # Baseline
    print(f"\n--- Baseline (pretrained, no PPO) ---")
    for cfg in TRAIN_CONFIGS + [TARGET_CONFIG]:
        r = evaluate(model, cfg, n_episodes=N_EVAL_EPISODES, n_flows=200)
        tag = "TRAIN" if cfg in TRAIN_CONFIGS else "TARGET"
        print(f"  {cfg:16s}: success={r['success_rate']:.1%}  "
              f"stretch={r['mean_stretch']:.3f}  [{tag}]")
    print()

    optimizer = torch.optim.Adam(model.parameters(), lr=PPO_LR)
    t0 = time.time()

    for it in range(N_ITERATIONS):
        batch = collect_batch(env, model, BATCH_SIZE, DEVICE)
        metrics = ppo_update(model, optimizer, batch, DEVICE)

        mean_reward = np.mean([b['reward'] for b in batch])
        mean_sr = np.mean([b['info']['success_rate'] for b in batch])
        mean_st = np.mean([b['info']['mean_stretch']
                          if b['info']['mean_stretch'] < float('inf') else 5.0
                          for b in batch])

        if (it + 1) % 10 == 0 or it == 0:
            elapsed = time.time() - t0
            print(f"  Iter {it + 1:3d}: reward={mean_reward:+.3f}  "
                  f"success={mean_sr:.1%}  stretch={mean_st:.3f}  "
                  f"ent={metrics['entropy']:.4f}  t={elapsed:.0f}s")

        if (it + 1) % EVAL_INTERVAL == 0:
            print(f"\n  --- Eval @ iter {it + 1} ---")
            for cfg in TRAIN_CONFIGS + [TARGET_CONFIG]:
                r = evaluate(model, cfg, n_episodes=N_EVAL_EPISODES, n_flows=200)
                tag = "TRAIN" if cfg in TRAIN_CONFIGS else "TARGET"
                print(f"  {cfg:16s}: success={r['success_rate']:.1%}  "
                      f"stretch={r['mean_stretch']:.3f}  [{tag}]")
            print()

    # Final
    print("=" * 60)
    print("FINAL EVALUATION")
    print("=" * 60)
    for cfg in TRAIN_CONFIGS + [TARGET_CONFIG]:
        r = evaluate(model, cfg, n_episodes=50, n_flows=300)
        tag = "TRAIN" if cfg in TRAIN_CONFIGS else "TARGET"
        print(f"  {cfg:16s}: success={r['success_rate']:.1%}  "
              f"stretch={r['mean_stretch']:.3f}  [{tag}]")

    save_path = os.path.join(os.path.dirname(__file__), 'ppo_finetuned.pt')
    torch.save(model.state_dict(), save_path)
    print(f"\nSaved: {save_path}")
    print(f"Total: {time.time() - t0:.0f}s")
    print("=" * 60)


if __name__ == '__main__':
    main()
