"""Unified training entry point for all RIS phase-shift baselines.

Usage:
    python train.py --algo td3 --seed 0 --N 100 --M 8 --K 4
    python train.py --algo pso --seed 0
    python train.py --algo random --seed 0 --episodes 100
"""

from __future__ import annotations

import argparse
import os
import sys
from collections import deque

import numpy as np

# Add project root so `simulator` is importable
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _PROJECT_ROOT)

from simulator.config import SimConfig
from simulator.env import RISPhaseEnv
from simulator.beamforming import zf_beamforming
from simulator.reward import compute_sum_rate

from baselines.networks import ReplayBuffer, Critic
from baselines.td3 import TD3Agent
from baselines.sac import SACAgent
from baselines.ddpg import DDPGAgent
from baselines.pso import PSOOptimizer
from baselines.simple import RandomPolicy, FixedPolicy
from baselines.ccan import CCANActor, CCANCritic


# ---------------------------------------------------------------------------
# PSO fitness function (evaluates sum-rate without calling env.step)
# ---------------------------------------------------------------------------

def _pso_fitness(phases: np.ndarray, H1: np.ndarray, H2: np.ndarray,
                 cfg: SimConfig) -> np.ndarray:
    """Evaluate sum-rate for a batch of phase-shift vectors.

    Args:
        phases: (n_particles, N) in [-1, 1]
        H1: (N, M) complex channel
        H2: (N, K) complex channel
        cfg: SimConfig with tx_power_linear and noise_power_linear

    Returns:
        (n_particles,) sum-rate values
    """
    n = phases.shape[0]
    rates = np.empty(n, dtype=np.float32)
    theta_all = (phases + 1.0) * np.pi  # (n, N) in [0, 2pi)
    for i in range(n):
        phase_shift = np.exp(1j * theta_all[i])
        H_eff = H2.conj().T @ np.diag(phase_shift) @ H1  # (K, M)
        W = zf_beamforming(H_eff, cfg.tx_power_linear, cfg.K)
        r, _ = compute_sum_rate(H_eff, W, cfg.noise_power_linear)
        rates[i] = r
    return rates


# ---------------------------------------------------------------------------
# Training loops
# ---------------------------------------------------------------------------

def _train_drl(algo_name: str, agent, env: RISPhaseEnv, buffer: ReplayBuffer,
               n_episodes: int, batch_size: int, base_seed: int,
               use_wandb: bool, save_dir: str, cfg: SimConfig,
               no_early_stop: bool = False):
    """Generic DRL training loop (TD3/SAC/DDPG)."""
    import wandb

    if use_wandb:
        wandb.init(
            project="ris-phase-drl",
            name=f"{algo_name}_N{cfg.N}_seed{base_seed}",
            config={"algo": algo_name, "N": cfg.N, "M": cfg.M, "K": cfg.K,
                    "seed": base_seed},
        )

    best_reward = -np.inf
    recent_rewards: deque[float] = deque(maxlen=100)
    os.makedirs(save_dir, exist_ok=True)

    for ep in range(n_episodes):
        obs, info = env.reset(seed=base_seed + ep)
        ep_reward = 0.0

        for t in range(cfg.episode_len):
            action = agent.select_action_exploration(obs)
            next_obs, reward, terminated, truncated, info = env.step(action)
            buffer.store(obs, action, reward, next_obs, float(terminated))

            if buffer.size >= batch_size:
                agent.update(buffer, batch_size)

            obs = next_obs
            ep_reward += reward
            if terminated:
                break

        recent_rewards.append(ep_reward)

        log_data = {"episode_reward": ep_reward, "episode": ep}
        if buffer.size >= batch_size:
            log_data["actor_loss"] = agent.last_actor_loss
            log_data["critic_loss"] = agent.last_critic_loss

        if use_wandb:
            wandb.log(log_data)

        # Save best model
        if ep_reward > best_reward:
            best_reward = ep_reward
            agent.save(os.path.join(save_dir, "best_model.pt"))

        # Periodic checkpoint
        if (ep + 1) % 100 == 0:
            agent.save(os.path.join(save_dir, f"checkpoint_ep{ep+1}.pt"))
            avg = np.mean(recent_rewards)
            print(f"[{algo_name}] Ep {ep+1}/{n_episodes} | "
                  f"reward={ep_reward:.2f} | avg100={avg:.2f} | best={best_reward:.2f}")

        # Early stopping: 100-episode average change < 1%
        if not no_early_stop and len(recent_rewards) == 100:
            first_half = list(recent_rewards)[:50]
            second_half = list(recent_rewards)[50:]
            avg1 = np.mean(first_half)
            avg2 = np.mean(second_half)
            if avg1 > 0 and abs(avg2 - avg1) / max(abs(avg1), 1e-8) < 0.01:
                print(f"[{algo_name}] Early stopping at ep {ep+1} "
                      f"(avg change < 1% over 100 eps)")
                break

    # Save final model
    agent.save(os.path.join(save_dir, "final_model.pt"))
    final_avg = np.mean(recent_rewards) if recent_rewards else 0.0
    final_std = np.std(recent_rewards) if len(recent_rewards) > 1 else 0.0
    print(f"[{algo_name}] Done {len(recent_rewards)} eps | "
          f"avg={final_avg:.2f} +/- {final_std:.2f} | best={best_reward:.2f}")
    if use_wandb:
        wandb.finish()


def _train_pso(env: RISPhaseEnv, n_episodes: int, base_seed: int,
               use_wandb: bool, save_dir: str, cfg: SimConfig,
               n_particles: int = 30):
    """PSO training loop."""
    import wandb

    if use_wandb:
        wandb.init(
            project="ris-phase-drl",
            name=f"pso_N{cfg.N}_seed{base_seed}",
            config={"algo": "pso", "N": cfg.N, "M": cfg.M, "K": cfg.K,
                    "seed": base_seed, "n_particles": n_particles},
        )

    pso = PSOOptimizer(N=cfg.N, n_particles=n_particles)
    best_reward = -np.inf
    recent_rewards: deque[float] = deque(maxlen=100)
    os.makedirs(save_dir, exist_ok=True)

    for ep in range(n_episodes):
        obs, info = env.reset(seed=base_seed + ep)
        pso.initialize()
        ep_reward = 0.0

        for t in range(cfg.episode_len):
            # Fitness closure over current channels
            def fitness_fn(phases):
                return _pso_fitness(phases, env.H1, env.H2, cfg)

            action = pso.step(fitness_fn)
            obs, reward, terminated, truncated, info = env.step(action)
            ep_reward += reward
            if terminated:
                break

        recent_rewards.append(ep_reward)

        if use_wandb:
            wandb.log({"episode_reward": ep_reward, "episode": ep,
                        "pso_best_fitness": pso._global_best_fitness})

        if ep_reward > best_reward:
            best_reward = ep_reward

        if (ep + 1) % 10 == 0:
            avg = np.mean(recent_rewards)
            print(f"[PSO] Ep {ep+1}/{n_episodes} | "
                  f"reward={ep_reward:.2f} | avg={avg:.2f} | best={best_reward:.2f}")

        # Early stopping
        if len(recent_rewards) == 100:
            first_half = list(recent_rewards)[:50]
            second_half = list(recent_rewards)[50:]
            avg1 = np.mean(first_half)
            avg2 = np.mean(second_half)
            if avg1 > 0 and abs(avg2 - avg1) / max(abs(avg1), 1e-8) < 0.01:
                print(f"[PSO] Early stopping at ep {ep+1}")
                break

    if use_wandb:
        wandb.finish()


def _train_simple(policy, algo_name: str, env: RISPhaseEnv, n_episodes: int,
                  base_seed: int, use_wandb: bool, cfg: SimConfig):
    """Random / Fixed baseline loop."""
    import wandb

    if use_wandb:
        wandb.init(
            project="ris-phase-drl",
            name=f"{algo_name}_N{cfg.N}_seed{base_seed}",
            config={"algo": algo_name, "N": cfg.N, "M": cfg.M, "K": cfg.K,
                    "seed": base_seed},
        )

    rewards = []
    for ep in range(n_episodes):
        obs, info = env.reset(seed=base_seed + ep)
        ep_reward = 0.0

        for t in range(cfg.episode_len):
            action = policy.select_action(obs)
            obs, reward, terminated, truncated, info = env.step(action)
            ep_reward += reward
            if terminated:
                break

        rewards.append(ep_reward)
        if use_wandb:
            wandb.log({"episode_reward": ep_reward, "episode": ep})

        if (ep + 1) % 10 == 0:
            avg = np.mean(rewards[-10:])
            print(f"[{algo_name}] Ep {ep+1}/{n_episodes} | "
                  f"reward={ep_reward:.2f} | avg10={avg:.2f}")

    print(f"[{algo_name}] Final avg reward: {np.mean(rewards):.2f} "
          f"+/- {np.std(rewards):.2f}")
    if use_wandb:
        wandb.finish()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Train RIS phase-shift baselines")
    parser.add_argument("--algo", type=str, required=True,
                        choices=["td3", "sac", "ddpg", "pso", "random", "fixed",
                                 "ccan_td3", "ccan_sac"],
                        help="Algorithm to train")
    parser.add_argument("--ablation", type=str, default=None,
                        choices=["a1", "a2", "a3"],
                        help="CCAN ablation: a1=w/o attention, a2=w/o sharing, a3=w/o encoder")
    parser.add_argument("--no-early-stop", action="store_true",
                        help="Disable early stopping")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--N", type=int, default=100, help="RIS elements")
    parser.add_argument("--M", type=int, default=8, help="BS antennas")
    parser.add_argument("--K", type=int, default=4, help="Users")
    parser.add_argument("--episodes", type=int, default=3000)
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--gamma", type=float, default=0.99)
    parser.add_argument("--tau", type=float, default=1e-3)
    parser.add_argument("--hidden", type=int, nargs="+", default=[400, 300])
    parser.add_argument("--device", type=str, default="cuda")
    parser.add_argument("--no-wandb", action="store_true")
    parser.add_argument("--pso-particles", type=int, default=30)
    parser.add_argument("--buffer-size", type=int, default=100000)
    parser.add_argument("--save-dir", type=str, default=None,
                        help="Override checkpoint save directory")
    args = parser.parse_args()

    np.random.seed(args.seed)
    use_wandb = not args.no_wandb

    cfg = SimConfig(
        N=args.N, M=args.M, K=args.K,
        episode_len=50,
        total_episodes=args.episodes,
        buffer_size=args.buffer_size,
        batch_size=args.batch_size,
        lr=args.lr,
        gamma=args.gamma,
        tau=args.tau,
        hidden_dims=tuple(args.hidden),
        seed=args.seed,
        device=args.device,
    )

    env = RISPhaseEnv(cfg)

    # Save directory
    if args.save_dir:
        save_dir = args.save_dir
    else:
        save_dir = os.path.join(
            _PROJECT_ROOT, "results", "checkpoints",
            f"{args.algo}_N{args.N}_seed{args.seed}"
        )

    hidden = tuple(args.hidden)
    obs_dim = cfg.obs_dim
    act_dim = cfg.N

    if args.algo == "td3":
        agent = TD3Agent(obs_dim, act_dim, hidden, args.lr, args.tau, args.gamma,
                         device=args.device)
        buffer = ReplayBuffer(obs_dim, act_dim, args.buffer_size)
        _train_drl("td3", agent, env, buffer, args.episodes, args.batch_size,
                   args.seed, use_wandb, save_dir, cfg,
                   no_early_stop=args.no_early_stop)

    elif args.algo == "sac":
        agent = SACAgent(obs_dim, act_dim, hidden, args.lr, args.tau, args.gamma,
                         device=args.device)
        buffer = ReplayBuffer(obs_dim, act_dim, args.buffer_size)
        _train_drl("sac", agent, env, buffer, args.episodes, args.batch_size,
                   args.seed, use_wandb, save_dir, cfg,
                   no_early_stop=args.no_early_stop)

    elif args.algo == "ddpg":
        agent = DDPGAgent(obs_dim, act_dim, hidden, args.lr, args.tau, args.gamma,
                          device=args.device)
        buffer = ReplayBuffer(obs_dim, act_dim, args.buffer_size)
        _train_drl("ddpg", agent, env, buffer, args.episodes, args.batch_size,
                   args.seed, use_wandb, save_dir, cfg,
                   no_early_stop=args.no_early_stop)

    elif args.algo == "pso":
        _train_pso(env, args.episodes, args.seed, use_wandb, save_dir, cfg,
                   args.pso_particles)

    elif args.algo == "ccan_td3":
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

        ccan_actor = CCANActor(obs_dim, act_dim, args.N, args.M, args.K,
                               **ablation_flags)
        ccan_critic = CCANCritic(obs_dim, act_dim, args.N, args.M, args.K,
                                 hidden=hidden, **critic_ablation)
        agent = TD3Agent(obs_dim, act_dim, hidden, args.lr, args.tau, args.gamma,
                         device=args.device, actor=ccan_actor, critic=ccan_critic)
        buffer = ReplayBuffer(obs_dim, act_dim, args.buffer_size)
        _train_drl("ccan_td3" + (f"_{args.ablation}" if args.ablation else ""),
                   agent, env, buffer, args.episodes, args.batch_size,
                   args.seed, use_wandb, save_dir, cfg,
                   no_early_stop=args.no_early_stop)

    elif args.algo == "ccan_sac":
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

        ccan_actor = CCANActor(obs_dim, act_dim, args.N, args.M, args.K,
                               **ablation_flags)
        ccan_critic = CCANCritic(obs_dim, act_dim, args.N, args.M, args.K,
                                 hidden=hidden, **critic_ablation)
        agent = SACAgent(obs_dim, act_dim, hidden, args.lr, args.tau, args.gamma,
                         device=args.device, actor=ccan_actor, critic=ccan_critic)
        buffer = ReplayBuffer(obs_dim, act_dim, args.buffer_size)
        _train_drl("ccan_sac" + (f"_{args.ablation}" if args.ablation else ""),
                   agent, env, buffer, args.episodes, args.batch_size,
                   args.seed, use_wandb, save_dir, cfg,
                   no_early_stop=args.no_early_stop)

    elif args.algo == "random":
        policy = RandomPolicy(args.N)
        _train_simple(policy, "random", env, args.episodes, args.seed,
                      use_wandb, cfg)

    elif args.algo == "fixed":
        policy = FixedPolicy(args.N)
        _train_simple(policy, "fixed", env, args.episodes, args.seed,
                      use_wandb, cfg)


if __name__ == "__main__":
    main()
