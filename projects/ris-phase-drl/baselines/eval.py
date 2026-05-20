"""Deterministic evaluation of trained DRL policies (no exploration noise)."""

from __future__ import annotations

import argparse
import os
import sys
import numpy as np

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _PROJECT_ROOT)

from simulator.config import SimConfig
from simulator.env import RISPhaseEnv
from baselines.td3 import TD3Agent
from baselines.sac import SACAgent
from baselines.ddpg import DDPGAgent
from baselines.pso import PSOOptimizer
from baselines.simple import RandomPolicy, FixedPolicy
from baselines.networks import Critic
from baselines.ccan import CCANActor, CCANCritic
from baselines.train import _pso_fitness


def eval_drl(agent, env: RISPhaseEnv, cfg: SimConfig, n_episodes: int = 50,
             seed_base: int = 0) -> tuple[float, float, float]:
    rewards = []
    for ep in range(n_episodes):
        obs, info = env.reset(seed=seed_base + ep)
        ep_reward = 0.0
        for t in range(cfg.episode_len):
            action = agent.select_action(obs)  # deterministic, no noise
            obs, reward, terminated, truncated, info = env.step(action)
            ep_reward += reward
            if terminated:
                break
        rewards.append(ep_reward)
    arr = np.array(rewards)
    return float(np.mean(arr)), float(np.std(arr)), float(np.max(arr))


def eval_pso(env: RISPhaseEnv, cfg: SimConfig, n_episodes: int = 50,
             seed_base: int = 0, n_particles: int = 30) -> tuple[float, float, float]:
    pso = PSOOptimizer(N=cfg.N, n_particles=n_particles)
    rewards = []
    for ep in range(n_episodes):
        obs, info = env.reset(seed=seed_base + ep)
        pso.initialize()
        ep_reward = 0.0
        for t in range(cfg.episode_len):
            def fitness_fn(phases):
                return _pso_fitness(phases, env.H1, env.H2, cfg)
            action = pso.step(fitness_fn)
            obs, reward, terminated, truncated, info = env.step(action)
            ep_reward += reward
            if terminated:
                break
        rewards.append(ep_reward)
    arr = np.array(rewards)
    return float(np.mean(arr)), float(np.std(arr)), float(np.max(arr))


def eval_simple(policy, env: RISPhaseEnv, cfg: SimConfig, n_episodes: int = 50,
                seed_base: int = 0) -> tuple[float, float, float]:
    rewards = []
    for ep in range(n_episodes):
        obs, info = env.reset(seed=seed_base + ep)
        ep_reward = 0.0
        for t in range(cfg.episode_len):
            action = policy.select_action(obs)
            obs, reward, terminated, truncated, info = env.step(action)
            ep_reward += reward
            if terminated:
                break
        rewards.append(ep_reward)
    arr = np.array(rewards)
    return float(np.mean(arr)), float(np.std(arr)), float(np.max(arr))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--algo", required=True,
                        choices=["td3", "sac", "ddpg", "pso", "random", "fixed",
                                 "ccan_td3"])
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--N", type=int, default=100)
    parser.add_argument("--M", type=int, default=8)
    parser.add_argument("--K", type=int, default=4)
    parser.add_argument("--eval-episodes", type=int, default=50)
    parser.add_argument("--device", type=str, default="cuda")
    parser.add_argument("--hidden", type=int, nargs="+", default=[400, 300])
    parser.add_argument("--model-path", type=str, default=None)
    parser.add_argument("--ablation", type=str, default=None,
                        choices=["a1", "a2", "a3"])
    args = parser.parse_args()

    cfg = SimConfig(N=args.N, M=args.M, K=args.K, episode_len=50,
                    hidden_dims=tuple(args.hidden), device=args.device)
    env = RISPhaseEnv(cfg)
    hidden = tuple(args.hidden)

    eval_seed_base = 10000 + args.seed * 1000  # different seeds from training

    if args.algo == "ccan_td3":
        algo_tag = "ccan_td3" + (f"_{args.ablation}" if args.ablation else "")
        if args.model_path:
            model_path = args.model_path
        else:
            ckpt_dir = os.path.join(
                _PROJECT_ROOT, "results", "checkpoints",
                f"{algo_tag}_N{args.N}_seed{args.seed}"
            )
            model_path = os.path.join(ckpt_dir, "best_model.pt")

        if not os.path.exists(model_path):
            print(f"Model not found: {model_path}")
            return

        ablation_flags = dict(use_attention=True, use_sharing=True, use_encoder=True)
        critic_ablation = dict(use_attention=True, use_encoder=True)
        if args.ablation == "a1":
            ablation_flags["use_attention"] = False
            critic_ablation["use_attention"] = False
        elif args.ablation == "a2":
            ablation_flags["use_sharing"] = False
        elif args.ablation == "a3":
            ablation_flags["use_encoder"] = False
            critic_ablation["use_encoder"] = False

        ccan_actor = CCANActor(cfg.obs_dim, cfg.N, args.N, args.M, args.K,
                               **ablation_flags)
        ccan_critic = CCANCritic(cfg.obs_dim, cfg.N, args.N, args.M, args.K,
                                 hidden=hidden, **critic_ablation)
        agent = TD3Agent(cfg.obs_dim, cfg.N, hidden, device=args.device,
                         actor=ccan_actor, critic=ccan_critic)
        agent.load(model_path)
        avg, std, best = eval_drl(agent, env, cfg, args.eval_episodes, eval_seed_base)
        print(f"[{algo_tag}] seed={args.seed} | avg={avg:.2f} +/- {std:.2f} | best={best:.2f}")

    elif args.algo in ("td3", "sac", "ddpg"):
        # Find best model path
        if args.model_path:
            model_path = args.model_path
        else:
            ckpt_dir = os.path.join(
                _PROJECT_ROOT, "results", "checkpoints",
                f"{args.algo}_N{args.N}_seed{args.seed}"
            )
            model_path = os.path.join(ckpt_dir, "best_model.pt")

        if not os.path.exists(model_path):
            print(f"Model not found: {model_path}")
            return

        if args.algo == "td3":
            agent = TD3Agent(cfg.obs_dim, cfg.N, hidden, device=args.device)
        elif args.algo == "sac":
            agent = SACAgent(cfg.obs_dim, cfg.N, hidden, device=args.device)
        else:
            agent = DDPGAgent(cfg.obs_dim, cfg.N, hidden, device=args.device)

        agent.load(model_path)
        avg, std, best = eval_drl(agent, env, cfg, args.eval_episodes, eval_seed_base)
        print(f"[{args.algo}] seed={args.seed} | avg={avg:.2f} +/- {std:.2f} | best={best:.2f}")

    elif args.algo == "pso":
        avg, std, best = eval_pso(env, cfg, args.eval_episodes, eval_seed_base)
        print(f"[pso] seed={args.seed} | avg={avg:.2f} +/- {std:.2f} | best={best:.2f}")

    elif args.algo == "random":
        policy = RandomPolicy(args.N)
        avg, std, best = eval_simple(policy, env, cfg, args.eval_episodes, eval_seed_base)
        print(f"[random] seed={args.seed} | avg={avg:.2f} +/- {std:.2f} | best={best:.2f}")

    elif args.algo == "fixed":
        policy = FixedPolicy(args.N)
        avg, std, best = eval_simple(policy, env, cfg, args.eval_episodes, eval_seed_base)
        print(f"[fixed] seed={args.seed} | avg={avg:.2f} +/- {std:.2f} | best={best:.2f}")


if __name__ == "__main__":
    main()
