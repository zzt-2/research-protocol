"""Reward calculator — 多目标加权奖励，per-objective 归一化 + domination 检查。

从 environment.py 提取，与 K2/M01 eq.52 奖励结构对齐：
  R_episode = -(η_t · T_norm + η_e · E_norm + λ₁·Φ₁ + λ₂·Φ₂ + λ₃·Φ₃)

归一化策略：
  - T_norm = 总完成延迟 / Σ deadline（相对截止时间比例）
  - E_norm = 总能耗 / E_max（IoTD 本地全量计算的能耗上界）
  - Φ₁ = 平均违约程度（按子任务数归一化，防止多 IoTD 累积主导）
  - Φ₂/Φ₃ = 资源溢出（按节点数归一化）
"""

from __future__ import annotations

import warnings

import numpy as np

from config import SimConfig


class RewardCalculator:
    def __init__(self, config: SimConfig):
        self.cfg = config
        self.domination_threshold = config.reward_domination_threshold

        # Pre-compute E_max (worst case: all tasks on IoTD locally)
        # E_max = Σ (κ_iotd · f_iotd² · cycles_i) per task
        # Computed per-episode in setup() since task cycles vary
        self._e_max: float = 0.0
        self._mean_deadline: float = 1.0

    def setup(self, task_cycles: list[float], task_deadlines: list[float]) -> None:
        """Pre-compute normalization constants for this episode."""
        c = self.cfg
        self._e_max = c.kappa_iotd * c.freq_iotd ** 2 * sum(task_cycles)
        self._mean_deadline = float(np.mean(task_deadlines)) if task_deadlines else 1.0

    def compute_step_reward(
        self,
        compute_time: float,
        transfer_time: float,
        compute_energy: float,
        transfer_energy: float,
    ) -> tuple[float, dict[str, float]]:
        """Per-step reward for assigning a single task.

        Returns (reward, decomposition_dict).
        """
        md = self._mean_deadline
        t_raw = (compute_time + transfer_time) / md if md > 0 else 0.0
        e_raw = (compute_energy + transfer_energy) / self._e_max if self._e_max > 0 else 0.0

        t_norm = np.log1p(t_raw)
        e_norm = np.log1p(e_raw)

        r_t = self.cfg.reward_eta_t * t_norm
        r_e = self.cfg.reward_eta_e * e_norm
        r_step = -(r_t + r_e)

        decomp = {"latency": r_t, "energy": r_e}
        return r_step, decomp

    def compute_episode_penalty(
        self,
        task_completion_times: np.ndarray,
        task_deadlines: np.ndarray,
        node_available: np.ndarray,
        n_tasks: int,
        uav_start: int,
        n_uav: int,
        leo_start: int,
        n_leo: int,
    ) -> tuple[float, dict[str, float]]:
        """Episode-end penalty for deadline/resource violations.

        Returns (penalty, decomposition_dict).
        """
        c = self.cfg
        md = self._mean_deadline

        # Φ₁: deadline violation
        phi1 = 0.0
        for i in range(n_tasks):
            if task_completion_times[i] > task_deadlines[i]:
                phi1 += (task_completion_times[i] - task_deadlines[i]) / task_deadlines[i]
        phi1 /= n_tasks

        # Φ₂: UAV compute resource overflow
        phi2 = 0.0
        for u in range(n_uav):
            phi2 += max(0.0, node_available[uav_start + u] / md - 1.0)
        phi2 /= n_uav

        # Φ₃: LEO compute resource overflow
        phi3 = 0.0
        for l in range(n_leo):
            phi3 += max(0.0, node_available[leo_start + l] / md - 1.0)
        phi3 /= n_leo

        p1 = c.reward_lambda_1 * np.log1p(phi1)
        p2 = c.reward_lambda_2 * np.log1p(phi2)
        p3 = c.reward_lambda_3 * np.log1p(phi3)
        penalty = -(p1 + p2 + p3)

        decomp = {"penalty_deadline": p1, "penalty_uav": p2, "penalty_leo": p3}
        return penalty, decomp

    def check_domination(self, decomp: dict[str, float]) -> bool:
        """Check if any single component dominates (>threshold of total).

        Returns True if balanced (no domination), False if imbalanced.
        """
        abs_vals = {k: abs(v) for k, v in decomp.items() if abs(v) > 1e-12}
        total = sum(abs_vals.values())
        if total < 1e-12:
            return True

        balanced = True
        for name, val in abs_vals.items():
            pct = val / total
            if pct > self.domination_threshold:
                warnings.warn(
                    f"Reward domination: {name} = {pct*100:.1f}% "
                    f"> {self.domination_threshold*100:.0f}%",
                    RuntimeWarning, stacklevel=2,
                )
                balanced = False
        return balanced
