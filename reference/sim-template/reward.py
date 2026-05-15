"""Reward 模板 — 取自 leo-ntn-handover-drl 项目的 log-capacity 归一化模式。

最佳实践：
- log-capacity 归一化：r_norm = log₂(1+x) / log₂(1+x_max) ∈ [0,1]
  比线性归一化更适合 Shannon 容量，因为 SINR 跨度可达 40+ dB
- 每个目标独立方法 + 独立归一化，权重只在最终 combine 时乘
- domination threshold：单项目标占比 > 95% 时打印警告，提示检查权重平衡
- compute_reward 返回 (total, decomposition)，decomposition 含绝对值和百分比
"""
import warnings
import numpy as np
from numpy.typing import NDArray


class RewardCalculator:
    """多目标加权奖励，每项目标归一化到 [0, 1]。

    用法：
        rc = RewardCalculator(w_throughput=0.6, w_fairness=0.3, w_penalty=0.1)
        total, decomp = rc.compute_reward(sinr_db, served, demanded)
    """

    def __init__(
        self,
        w_throughput: float = 0.6,
        w_fairness: float = 0.3,
        w_penalty: float = 0.1,
        sinr_max_db: float = 22.0,        # log-capacity 归一化上界
        domination_threshold: float = 0.95,  # 单项占比警告阈值
    ):
        self.w_t = w_throughput
        self.w_f = w_fairness
        self.w_p = w_penalty
        self.sinr_max_db = sinr_max_db
        self.domination_threshold = domination_threshold

    # === 归一化工具 ===

    def _log_capacity_norm(self, sinr_db: float | NDArray) -> float | NDArray:
        """log-capacity 归一化：log₂(1+SINR) / log₂(1+SINR_max) ∈ [0, 1]。

        比 sinr/max_sinr 线性归一化更好：Shannon 容量对 SINR 是对数关系，
        线性归一化会让低 SINR 区间几乎为零、高 SINR 区间主导。
        """
        sinr_lin = np.maximum(10.0 ** (np.asarray(sinr_db, dtype=float) / 10.0), 0.0)
        cap = np.log2(1.0 + sinr_lin)
        cap_max = np.log2(1.0 + 10.0 ** (self.sinr_max_db / 10.0))
        return np.clip(cap / cap_max, 0.0, 1.0)

    # --- CUSTOMIZE --- 每个目标一个方法，内部归一化到 [0, 1]

    def _throughput_reward(self, served: NDArray, demanded: NDArray, sinr_db: float | NDArray | None = None) -> float:
        """吞吐量满足率：基于 log-capacity 归一化的 SINR 加权服务率。

        如果提供 sinr_db，则用 _log_capacity_norm 归一化 SINR 后作为权重；
        否则退化为简单的 served/demanded 比率。
        结果 clip 到 [0, 1]，防止超额服务时 > 1.0。
        """
        total = demanded.sum()
        if total <= 0:
            return 0.0
        if sinr_db is not None:
            # 用 log-capacity 归一化的 SINR 加权
            sinr_norm = self._log_capacity_norm(sinr_db)
            weighted_served = float(np.sum(served * sinr_norm))
            raw_ratio = weighted_served / total
        else:
            raw_ratio = float(served.sum() / total)
        return min(raw_ratio, 1.0)

    def _fairness_reward(self, served: NDArray, demanded: NDArray) -> float:
        """Jain's fairness index on satisfaction ratio。"""
        ratio = np.where(demanded > 0, served / demanded, 0.0)
        n = len(ratio)
        if n == 0 or ratio.sum() == 0:
            return 1.0
        return float(ratio.sum() ** 2 / (n * (ratio ** 2).sum()))

    def _penalty_term(self, violation: NDArray) -> float:
        """惩罚项归一化：越低越好。--- CUSTOMIZE --- 定义什么算违规。"""
        return float(np.mean(violation > 0))

    # === 主入口 ===

    def compute_reward(
        self,
        sinr_db: float | NDArray,
        served: NDArray,
        demanded: NDArray,
        violation: NDArray | None = None,
    ) -> tuple[float, dict[str, float]]:
        """计算加权奖励。

        Returns:
            (total_reward, decomposition_dict)
            decomposition 包含每项的绝对贡献和百分比。
        """
        r_t = self._throughput_reward(served, demanded, sinr_db)
        r_f = self._fairness_reward(served, demanded)
        r_p = self._penalty_term(violation) if violation is not None else 0.0

        # 加权求和（惩罚项减去）
        total = self.w_t * r_t + self.w_f * r_f - self.w_p * r_p

        # 分解：绝对贡献和百分比
        abs_t = abs(self.w_t * r_t)
        abs_f = abs(self.w_f * r_f)
        abs_p = abs(self.w_p * r_p)
        total_abs = abs_t + abs_f + abs_p + 1e-12  # 防除零

        decomp = {
            "throughput_abs": float(abs_t),
            "fairness_abs": float(abs_f),
            "penalty_abs": float(abs_p),
            "throughput_pct": float(abs_t / total_abs * 100),
            "fairness_pct": float(abs_f / total_abs * 100),
            "penalty_pct": float(abs_p / total_abs * 100),
        }

        # Domination threshold 检查
        for name, pct in [("throughput", decomp["throughput_pct"]),
                          ("fairness", decomp["fairness_pct"]),
                          ("penalty", decomp["penalty_pct"])]:
            if pct > self.domination_threshold * 100:
                warnings.warn(
                    f"Reward domination: {name} = {pct:.1f}% "
                    f">( {self.domination_threshold*100:.0f}%), check weights",
                    RuntimeWarning, stacklevel=2,
                )

        return float(total), decomp
