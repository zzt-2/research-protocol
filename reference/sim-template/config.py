"""Config dataclass 模板 — 取自 leo-beam-hopping-gnn 项目。

最佳实践：
- @dataclass + __post_init__ 计算派生量，避免运行时重复计算
- 所有参数有默认值 → 单行 config = SimConfig() 即可跑通
- 文献溯源用行内注释 (Ref: 来源) 追踪每个参数出处
"""
import numpy as np
from dataclasses import dataclass


@dataclass
class SimConfig:
    # === 物理常数 ===
    c: float = 3e8                        # 光速 m/s

    # --- CUSTOMIZE --- 星座参数
    orbit_height_km: float = 550.0        # 轨道高度 (Ref: 根据具体星座)
    earth_radius_km: float = 6371.0       # 地球半径，一般不改

    # --- CUSTOMIZE --- 信道参数
    frequency_hz: float = 11.45e9         # 载频 (Ref: 频段论文)
    bandwidth_hz: float = 30e6            # 带宽 (Ref: 频谱分配)
    p_max_dbm: float = 40.0              # 最大发射功率 dBm (Ref: 链路预算)
    noise_power_dbm: float = -97.0       # 噪声功率 dBm (Ref: 接收机灵敏度)

    # --- CUSTOMIZE --- 流量参数
    demand_min_mbps: float = 20.0         # 最小需求 Mbps
    demand_max_mbps: float = 700.0        # 最大需求 Mbps (Ref: 流量模型论文)

    # --- CUSTOMIZE --- 奖励权重（用户确认后再冻结）
    # 映射关系：reward_alpha → reward.py w_throughput, reward_beta → w_fairness,
    #           reward_gamma → w_penalty
    reward_alpha: float = 0.6             # 吞吐量权重  (→ RewardCalculator.w_throughput)
    reward_beta: float = 0.3              # 公平性权重  (→ RewardCalculator.w_fairness)
    reward_gamma: float = 0.1             # 干扰惩罚权重 (→ RewardCalculator.w_penalty)
    sinr_max_db: float = 22.0            # log-capacity 归一化上界 dB (→ RewardCalculator.sinr_max_db)

    # --- CUSTOMIZE --- 训练/episode 参数
    t_slots: int = 20                     # 每个 episode 时隙数
    n_beams: int = 19                     # 波束/用户数量
    n_entities: int = 19                  # 实体数量（默认与 n_beams 相同，多 IoTD 场景可不同）
    device: str = "cuda"                  # 训练设备
    seed: int = 42                        # 全局随机种子
    total_episodes: int = 1000            # 总训练 episode 数

    # === 派生量（__post_init__ 自动计算，不要手动设）===
    wavelength_m: float = 0.0
    p_max_linear: float = 0.0
    noise_power_linear: float = 0.0
    slant_range_km: float = 0.0

    def __post_init__(self):
        # --- 范围校验（先于派生量计算，避免 sqrt 负值等数值问题）---
        assert 0 < self.orbit_height_km <= 36000, "轨道高度应在 LEO/MEO 范围"
        assert self.frequency_hz > 0, "载频必须为正"
        assert self.p_max_dbm > self.noise_power_dbm, "发射功率应大于噪声功率"
        assert self.bandwidth_hz > 0, "带宽必须为正"
        assert self.t_slots > 0, "episode 时隙数必须为正"
        assert self.n_beams > 0, "波束数必须为正"
        assert self.n_entities > 0, "实体数必须为正"
        assert self.total_episodes > 0, "总 episode 数必须为正"
        assert self.device in ("cpu", "cuda"), "device 必须为 'cpu' 或 'cuda'"
        assert abs(self.reward_alpha + self.reward_beta + self.reward_gamma - 1.0) < 0.05, \
            "奖励权重之和应接近 1.0"

        # 派生物理量
        self.wavelength_m = self.c / self.frequency_hz
        self.p_max_linear = 10 ** (self.p_max_dbm / 10) / 1000    # dBm → W
        self.noise_power_linear = 10 ** (self.noise_power_dbm / 10) / 1000

        # 星下点到地面最大斜距（几何近似）
        r = self.earth_radius_km
        self.slant_range_km = np.sqrt((r + self.orbit_height_km) ** 2 - r ** 2)
