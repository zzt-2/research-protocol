"""Baseline 统一评估框架 — 抽象基类 + 多 episode x 多 seed + 趋势验证。

CUSTOMIZE 标记: 搜索 "# --- CUSTOMIZE ---" 找到所有需要定制的位置。
"""
from __future__ import annotations

import json
import math
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import numpy as np


class Baseline(ABC):
    """Baseline 策略接口。子类实现 name 属性和 run_episode 方法。"""
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def run_episode(self, env, seed: int) -> dict[str, Any]:
        """执行一个 episode，返回至少包含 'reward' 键的字典。"""
        ...


class RandomBaseline(Baseline):
    """均匀随机策略。"""
    @property
    def name(self) -> str:
        return "random"

    def run_episode(self, env, seed: int) -> dict[str, Any]:
        obs, info = env.reset(seed=seed)
        total_reward, steps, done = 0.0, 0, False
        while not done:
            # --- CUSTOMIZE: action masking 时改为从 info 中取合法动作 ---
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
            steps += 1
            done = terminated or truncated
        return {"reward": total_reward, "steps": steps}


class GreedyBaseline(Baseline):
    """贪心策略。需要定制 _greedy_action。"""
    @property
    def name(self) -> str:
        return "greedy"

    def run_episode(self, env, seed: int) -> dict[str, Any]:
        obs, info = env.reset(seed=seed)
        total_reward, steps, done = 0.0, 0, False
        while not done:
            action = self._greedy_action(env, obs, info)  # --- CUSTOMIZE ---
            obs, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
            steps += 1
            done = terminated or truncated
        return {"reward": total_reward, "steps": steps}

    def _greedy_action(self, env, obs, info) -> Any:
        """--- CUSTOMIZE: 替换为你的贪心启发式。默认降级为随机。---"""
        return env.action_space.sample()


class BaselineSuite:
    """注册 + 统一执行 + 趋势验证。

    用法: suite.register(RandomBaseline()); results = suite.run_all(env); suite.verify_ranking(...)
    """
    def __init__(self) -> None:
        self._baselines: dict[str, Baseline] = {}

    def register(self, baseline: Baseline) -> None:
        self._baselines[baseline.name] = baseline

    @property
    def names(self) -> list[str]:
        return list(self._baselines.keys())

    def run_all(self, env, n_episodes: int = 30,
                seeds: list[int] | None = None) -> dict[str, dict[str, Any]]:
        """N episode x M seed 评估，返回 {name: {episodes, summary}}。"""
        if seeds is None:
            seeds = [42, 43, 44]
        all_results: dict[str, dict[str, Any]] = {}
        for name, bl in self._baselines.items():
            print(f"\n{'='*50}\nBaseline: {name}\n{'='*50}")
            episode_data: list[dict] = []
            for seed in seeds:
                for ep in range(n_episodes):
                    ep_seed = seed + ep * 100
                    metrics = bl.run_episode(env, ep_seed)
                    metrics["seed"] = ep_seed
                    episode_data.append(metrics)
            summary = _summarize(episode_data)
            all_results[name] = {"episodes": episode_data, "summary": summary}
            s = summary
            print(f"  reward: {s['reward_mean']:.4f} +/- {s['reward_std']:.4f} "
                  f"95%CI [{s['reward_ci_lo']:.4f}, {s['reward_ci_hi']:.4f}]")
        return all_results

    def verify_ranking(self, results: dict[str, dict[str, Any]],
                       expected_order: list[str], min_gap_pct: float = 5.0) -> bool:
        """验证排名趋势。相邻对前>后为 PASS，gap<min_gap_pct 降级 ≈，反转则 FAIL。"""
        print(f"\n{'='*50}\nTrend Verification\n{'='*50}")
        means = {n: results[n]["summary"]["reward_mean"]
                 for n in expected_order if n in results}
        if len(means) < 2:
            print("  [WARN] <2 baselines"); return False

        ordered, checks = list(means.keys()), []
        for i in range(len(ordered) - 1):
            a, b = ordered[i], ordered[i + 1]
            gap = (means[a] - means[b]) / abs(means[b]) * 100 if means[b] != 0 else 0.0
            if gap > min_gap_pct:
                status = "PASS"; checks.append(True)
            elif gap > 0:
                status = f"~ gap={gap:.1f}%"; checks.append(True)
            else:
                status = "FAIL"; checks.append(False)
            print(f"  [{status}] {a}({means[a]:.4f}) > {b}({means[b]:.4f})")

        core_pass = means[ordered[0]] > means[ordered[-1]]
        print(f"  >>> {'PASSED' if core_pass else 'FAILED'} ({sum(checks)}/{len(checks)})")
        return core_pass

    def save(self, results: dict[str, dict[str, Any]], path: str) -> None:
        """保存 summary 到 JSON（与 run.py 格式兼容）。"""
        Path(path).parent.mkdir(exist_ok=True, parents=True)
        out = {n: {"summary": d["summary"]} for n, d in results.items()}
        with open(path, "w") as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
        print(f"Saved: {path}")


def _summarize(episodes: list[dict]) -> dict[str, float]:
    rewards = np.array([ep["reward"] for ep in episodes])
    n = len(rewards)
    mean, std = float(rewards.mean()), float(rewards.std())
    ci = 1.96 * std / math.sqrt(n) if n else 0.0
    return {"reward_mean": mean, "reward_std": std,
            "reward_min": float(rewards.min()), "reward_max": float(rewards.max()),
            "reward_ci_lo": mean - ci, "reward_ci_hi": mean + ci, "n_episodes": n}
