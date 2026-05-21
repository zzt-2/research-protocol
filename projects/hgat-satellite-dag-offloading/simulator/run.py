"""实验编排入口 — CLI + 模型注册表 + 多模型 x 多种子 + wandb。

用法:
    python run.py --model hgat --episodes 500 --seeds 42 123 456
    python run.py --model all   # 全部模型 + baselines
    python run.py --baselines-only
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch

from baselines import BaselineSuite, GreedySPTBaseline, RandomBaseline
from config import SimConfig
from env import SatelliteDAGEnv
from models_hgat import HGATActorCritic
from models_homo import GCNActorCritic, GraphSAGEActorCritic, MLPActorCritic
from ppo import EarlyStopping, PPO, RewardNormalizer, RolloutBuffer

try:
    import wandb
    _WANDB = bool(wandb.api.api_key) if hasattr(wandb, "api") else False
except Exception:
    wandb = None
    _WANDB = False

MODEL_REGISTRY = {
    "hgat": HGATActorCritic,
    "graphsage": GraphSAGEActorCritic,
    "gcn": GCNActorCritic,
    "mlp": MLPActorCritic,
}

BASELINE_REGISTRY = {
    "random": RandomBaseline(),
    "greedy": GreedySPTBaseline(),
}

# Per-model hyperparameter overrides (homo models need gentler training)
MODEL_HYPERPARAMS = {
    "graphsage": {"lr": 5e-5, "kl_threshold": 1.0, "ppo_epochs": 2},
    "gcn": {"lr": 5e-5, "kl_threshold": 1.0, "ppo_epochs": 2},
    "mlp": {"lr": 5e-5, "kl_threshold": 1.0, "ppo_epochs": 2},
}


def _make_model(name: str, config: SimConfig, n_actions: int, device: str):
    return MODEL_REGISTRY[name](config, n_actions).to(device)


def train_one(model_name: str, seed: int, config: SimConfig,
              n_episodes: int, device: str, results_dir: Path) -> dict:
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    env = SatelliteDAGEnv(config, seed=seed)
    n_actions = env.action_space.n
    model = _make_model(model_name, config, n_actions, device)

    if _WANDB:
        wandb.init(project="hgat-satellite-dag", name=f"{model_name}_seed{seed}",
                   config={"model": model_name, "seed": seed, "episodes": n_episodes},
                   reinit=True)

    overrides = MODEL_HYPERPARAMS.get(model_name, {})
    lr = overrides.get("lr", config.ppo_lr)
    kl_threshold = overrides.get("kl_threshold", config.early_stop_kl_threshold)
    ppo_epochs = overrides.get("ppo_epochs", config.ppo_epochs)

    ppo = PPO(model, lr=lr, clip_eps=config.ppo_clip,
              gamma=config.ppo_gamma, gae_lambda=config.ppo_gae_lambda,
              epochs=ppo_epochs, batch_size=config.ppo_batch,
              entropy_coef=config.ppo_entropy_coef, device=device)
    rnorm = RewardNormalizer()
    es = EarlyStopping(patience=config.early_stop_patience,
                       kl_threshold=kl_threshold)
    if overrides:
        print(f"  [Override] lr={lr:.0e}, kl_threshold={kl_threshold}")

    episode_rewards: list[float] = []
    all_metrics: list[dict] = []
    best_reward = -float("inf")

    for ep in range(n_episodes):
        obs, info = env.reset(seed=seed + ep)
        buf = RolloutBuffer()
        done, ep_reward = False, 0.0

        while not done:
            mask = info["action_mask"]
            action, lp, v, _ = model.get_action(obs, mask)
            next_obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            buf.add(obs, action, lp, reward, done, v, mask)
            obs = next_obs
            ep_reward += reward

        episode_rewards.append(ep_reward)

        # Skip cross-episode reward normalization — PPO advantage normalization is sufficient
        # Cross-episode normalizer fails on bimodal reward distributions (good:-35 vs bad:-267K)
        with torch.no_grad():
            _, last_val = model(obs)
            last_val = last_val if isinstance(last_val, float) else last_val.item()
        buf.compute_returns_and_advantages(last_val, config.ppo_gamma, config.ppo_gae_lambda)
        metrics = ppo.update(buf)
        metrics["episode"] = ep
        metrics["episode_reward"] = ep_reward
        all_metrics.append(metrics)

        if _WANDB and wandb.run is not None:
            wandb.log({"train/episode_reward": ep_reward, "train/episode": ep}, commit=False)

        # Save best model
        if ep_reward > best_reward:
            best_reward = ep_reward
            ppo.save(str(results_dir / f"{model_name}_seed{seed}_best.pt"), rnorm)

        if es.step(ep_reward, metrics["kl_approx"]):
            print(f"  [EarlyStop] episode {ep+1}")
            break

        if (ep + 1) % 50 == 0:
            recent = episode_rewards[-50:]
            print(f"  [{model_name}] seed={seed} ep={ep+1}/{n_episodes} "
                  f"reward(last50)={np.mean(recent):.2f}")

    # Final save
    ppo.save(str(results_dir / f"{model_name}_seed{seed}_final.pt"), rnorm)

    results = {"model": model_name, "seed": seed,
               "episode_rewards": episode_rewards, "n_episodes": len(episode_rewards)}
    out = results_dir / f"{model_name}_seed{seed}.json"
    with open(out, "w") as f:
        json.dump(results, f)

    if _WANDB and wandb.run is not None:
        wandb.finish()

    return results


def evaluate_baselines(config: SimConfig, n_episodes: int,
                       seeds: list[int], results_dir: Path) -> dict:
    env = SatelliteDAGEnv(config)
    suite = BaselineSuite()
    for bl in BASELINE_REGISTRY.values():
        suite.register(bl)
    results = suite.run_all(env, n_episodes=n_episodes, seeds=seeds)
    suite.verify_ranking(results, expected_order=["greedy", "random"])
    suite.save(results, str(results_dir / "baseline_summary.json"))
    return results


def collect_summary(results_dir: Path) -> dict:
    summary = {}
    for f in sorted(results_dir.glob("*_seed*.json")):
        with open(f) as fh:
            data = json.load(fh)
        rewards = data.get("episode_rewards", [])
        summary[f.stem] = {"model": data.get("model", f.stem), "seed": data.get("seed"),
                           "n_episodes": data.get("n_episodes"),
                           "mean_reward": float(np.mean(rewards)) if rewards else None}
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="all",
                        choices=list(MODEL_REGISTRY.keys()) + ["all", "random", "greedy"])
    parser.add_argument("--seeds", type=int, nargs="+", default=[42, 123, 456])
    parser.add_argument("--episodes", type=int, default=500)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--output-dir", default="results")
    parser.add_argument("--baselines-only", action="store_true")
    args = parser.parse_args()

    config = SimConfig()
    results_dir = Path(args.output_dir)
    results_dir.mkdir(exist_ok=True, parents=True)

    models = [] if args.baselines_only else (
        list(MODEL_REGISTRY.keys()) if args.model == "all"
        else ([args.model] if args.model in MODEL_REGISTRY else []))

    print(f"Models: {models or '(baselines only)'} | Seeds: {args.seeds} | "
          f"Ep: {args.episodes} | Device: {args.device}")
    t0 = time.time()

    for model_name in models:
        for seed in args.seeds:
            print(f"\n{'='*50}\nTrain: {model_name} seed={seed}\n{'='*50}")
            train_one(model_name, seed, config, args.episodes, args.device, results_dir)

    if BASELINE_REGISTRY and (args.baselines_only or args.model == "all"
                               or args.model in BASELINE_REGISTRY):
        print(f"\n{'='*50}\nBaseline Evaluation\n{'='*50}")
        evaluate_baselines(config, args.episodes, args.seeds, results_dir)

    summary = collect_summary(results_dir)
    with open(results_dir / "results_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nTotal: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
