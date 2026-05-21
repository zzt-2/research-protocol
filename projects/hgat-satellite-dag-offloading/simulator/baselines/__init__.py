"""Baseline 策略 — Random + Greedy(SPT) + BaselineSuite 评估框架。"""

from __future__ import annotations

import json
import math
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import numpy as np


class Baseline(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def run_episode(self, env, seed: int) -> dict[str, Any]: ...


class RandomBaseline(Baseline):
    @property
    def name(self) -> str:
        return "random"

    def run_episode(self, env, seed: int) -> dict[str, Any]:
        obs, info = env.reset(seed=seed)
        total_reward, steps, done = 0.0, 0, False
        while not done:
            mask = info.get("action_mask")
            valid = np.where(mask)[0] if mask is not None else None
            if valid is not None and len(valid) == 0:
                break
            action = int(np.random.choice(valid)) if valid is not None else env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
            steps += 1
            done = terminated or truncated
        return {"reward": total_reward, "steps": steps}


class GreedySPTBaseline(Baseline):
    """Shortest Processing Time first: 选 (ready_task, node) pair 中 compute+transfer 最短的。"""

    @property
    def name(self) -> str:
        return "greedy_spt"

    def run_episode(self, env, seed: int) -> dict[str, Any]:
        obs, info = env.reset(seed=seed)
        total_reward, steps, done = 0.0, 0, False
        while not done:
            mask = info.get("action_mask")
            if mask is None or not mask.any():
                break
            action = self._greedy_action(env, mask)
            if action is None:
                break
            obs, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
            steps += 1
            done = terminated or truncated
        return {"reward": total_reward, "steps": steps}

    def _greedy_action(self, env, mask: np.ndarray) -> int | None:
        ready = env._get_ready_tasks()
        best_action, best_time = None, float("inf")
        for task_id in ready:
            task = env._all_tasks[task_id]
            for node_id in range(env.n_nodes):
                act = task_id * env.n_nodes + node_id
                if not mask[act]:
                    continue
                freq = env._get_node_freq(node_id)
                ct = task.cycles / freq
                tt = 0.0
                for pred_id in task.predecessors:
                    pn = int(env._task_nodes[pred_id])
                    if pn != node_id:
                        rate = env._get_link_rate(pn, node_id)
                        tt += env._all_tasks[pred_id].output_data / rate
                if not task.predecessors and node_id != task.owning_iotd:
                    rate = env._get_link_rate(task.owning_iotd, node_id)
                    tt += task.input_data / rate
                if ct + tt < best_time:
                    best_time = ct + tt
                    best_action = act
        return best_action


class BaselineSuite:
    def __init__(self) -> None:
        self._baselines: dict[str, Baseline] = {}

    def register(self, baseline: Baseline) -> None:
        self._baselines[baseline.name] = baseline

    @property
    def names(self) -> list[str]:
        return list(self._baselines.keys())

    def run_all(self, env, n_episodes: int = 30,
                seeds: list[int] | None = None) -> dict[str, dict[str, Any]]:
        if seeds is None:
            seeds = [42, 43, 44]
        all_results: dict[str, dict[str, Any]] = {}
        for name, bl in self._baselines.items():
            print(f"\nBaseline: {name}")
            episode_data: list[dict] = []
            for seed in seeds:
                for ep in range(n_episodes):
                    metrics = bl.run_episode(env, seed=seed + ep * 100)
                    metrics["seed"] = seed
                    episode_data.append(metrics)
            summary = _summarize(episode_data)
            all_results[name] = {"episodes": episode_data, "summary": summary}
            print(f"  reward: {summary['reward_mean']:.4f} +/- {summary['reward_std']:.4f}")
        return all_results

    def verify_ranking(self, results: dict[str, dict], expected_order: list[str],
                       min_gap_pct: float = 5.0) -> bool:
        means = {n: results[n]["summary"]["reward_mean"]
                 for n in expected_order if n in results}
        if len(means) < 2:
            return False
        ordered = list(means.keys())
        all_pass = True
        for i in range(len(ordered) - 1):
            a, b = ordered[i], ordered[i + 1]
            gap = (means[a] - means[b]) / abs(means[b]) * 100 if means[b] != 0 else 0.0
            status = "PASS" if gap > min_gap_pct else ("~" if gap > 0 else "FAIL")
            if gap <= 0:
                all_pass = False
            print(f"  [{status}] {a}({means[a]:.4f}) > {b}({means[b]:.4f})")
        return all_pass

    def save(self, results: dict, path: str) -> None:
        Path(path).parent.mkdir(exist_ok=True, parents=True)
        out = {n: {"summary": d["summary"]} for n, d in results.items()}
        with open(path, "w") as f:
            json.dump(out, f, indent=2, ensure_ascii=False)


def _summarize(episodes: list[dict]) -> dict[str, float]:
    rewards = np.array([ep["reward"] for ep in episodes])
    n = len(rewards)
    mean, std = float(rewards.mean()), float(rewards.std())
    ci = 1.96 * std / math.sqrt(n) if n else 0.0
    return {"reward_mean": mean, "reward_std": std,
            "reward_min": float(rewards.min()), "reward_max": float(rewards.max()),
            "reward_ci_lo": mean - ci, "reward_ci_hi": mean + ci, "n_episodes": n}
