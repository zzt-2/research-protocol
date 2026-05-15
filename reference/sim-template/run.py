"""实验入口/编排模板 — CLI + 注册表 + 多模型 x 多种子调度 + 结果汇总。

MODEL_REGISTRY / BASELINE_REGISTRY 字典注册，--model all 遍历，--seeds 外层循环。
wandb 实验名: {model}_seed{N}。--eval-only / --baselines-only 控制模式。

CUSTOMIZE 标记: 搜索 "# --- CUSTOMIZE ---" 找到所有需要定制的位置。
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

import numpy as np
import torch

from .baselines.base import Baseline, BaselineSuite, RandomBaseline, GreedyBaseline
from .config import SimConfig
from .env import SimEnv

# --- CUSTOMIZE: 导入模型类 ---
# from .model_gnn import GATEncoder

# --- CUSTOMIZE: 注册模型（名字 -> 构造 callable）---
MODEL_REGISTRY: dict[str, Any] = {
    # "gnn": GATEncoder,
}

# --- CUSTOMIZE: 注册 Baseline ---
BASELINE_REGISTRY: dict[str, Baseline] = {
    "random": RandomBaseline(),
    "greedy": GreedyBaseline(),
}


def build_model(name: str, config: SimConfig, device: str) -> torch.nn.Module:
    if name not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model: {name!r}")
    # --- CUSTOMIZE: 调整构造参数（in_dim, n_actions 等）---
    return MODEL_REGISTRY[name]().to(device)


def train_one(model_name: str, seed: int, config: SimConfig,
              n_episodes: int, device: str, results_dir: Path) -> dict[str, Any]:
    """训练一个 (model, seed) 组合。--- CUSTOMIZE: 调整 train() 调用 ---"""
    from .train_ppo import train
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    env = SimEnv(config=config, seed=seed)
    model = build_model(model_name, config, device)

    # --- CUSTOMIZE: wandb ---
    # try: import wandb; wandb.init(project="your-project", name=f"{model_name}_seed{seed}")
    # except ImportError: pass

    results = train(env=env, model=model, n_episodes=n_episodes,
                    seed=seed, device=device, results_dir=str(results_dir))

    # --- CUSTOMIZE: wandb finish ---
    # try: import wandb; wandb.finish()
    # except ImportError: pass
    return results


def evaluate_baselines(config: SimConfig, n_episodes: int,
                       seeds: list[int], results_dir: Path) -> dict[str, Any]:
    """运行所有注册 baseline 并验证趋势。"""
    env = SimEnv(config=config)
    suite = BaselineSuite()
    for bl in BASELINE_REGISTRY.values():
        suite.register(bl)
    results = suite.run_all(env, n_episodes=n_episodes, seeds=seeds)
    # --- CUSTOMIZE: 调整 expected_order ---
    suite.verify_ranking(results, expected_order=list(BASELINE_REGISTRY.keys()))
    suite.save(results, str(results_dir / "baseline_summary.json"))
    return results


def collect_summary(results_dir: Path) -> dict[str, Any]:
    """汇总所有结果文件。"""
    summary: dict[str, Any] = {}
    for f in sorted(results_dir.glob("*_seed*.json")):
        with open(f) as fh:
            data = json.load(fh)
        rewards = data.get("episode_rewards", [])
        summary[f.stem] = {
            "model": data.get("model", f.stem), "seed": data.get("seed"),
            "n_episodes": data.get("n_episodes"),
            "mean_reward": float(np.mean(rewards)) if rewards else None,
        }
    return summary


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="实验编排 — 模型训练 + baseline 评估")
    p.add_argument("--model", default="all", help="模型名或 'all'")
    p.add_argument("--seeds", type=int, nargs="+", default=[42, 123, 456])
    p.add_argument("--episodes", type=int, default=500)
    p.add_argument("--config", default=None, help="SimConfig JSON 路径")
    p.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    p.add_argument("--output-dir", default="results")
    p.add_argument("--eval-only", action="store_true", help="仅评估已有模型")
    p.add_argument("--baselines-only", action="store_true", help="仅 baseline")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    config = SimConfig()
    if args.config:
        with open(args.config) as f:
            overrides = json.load(f)
        valid = {k: v for k, v in overrides.items() if hasattr(config, k)}
        config = SimConfig(**{k: valid.get(k, getattr(config, k))
                              for k in config.__dataclass_fields__})

    results_dir = Path(args.output_dir)
    results_dir.mkdir(exist_ok=True, parents=True)

    models = [] if args.baselines_only else (
        list(MODEL_REGISTRY.keys()) if args.model == "all" else [args.model])

    print(f"Models: {models or '(baselines only)'} | Seeds: {args.seeds} | "
          f"Ep: {args.episodes} | Device: {args.device}")
    t0 = time.time()

    for model_name in models:
        if model_name in BASELINE_REGISTRY:
            continue
        for seed in args.seeds:
            print(f"\n{'='*50}\nTrain: {model_name} seed={seed}\n{'='*50}")
            train_one(model_name, seed, config, args.episodes, args.device, results_dir)

    if BASELINE_REGISTRY and (args.baselines_only or args.model == "all" or not models):
        print(f"\n{'='*50}\nBaseline Evaluation\n{'='*50}")
        evaluate_baselines(config, args.episodes, args.seeds, results_dir)

    summary = collect_summary(results_dir)
    with open(results_dir / "results_summary.json", "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"\nSummary: {results_dir / 'results_summary.json'}")
    print(f"Total: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
