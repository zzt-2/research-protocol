"""SimConfig dataclass — satellite-地面协同边缘计算 DAG 依赖任务卸载仿真器。

Sources: K2/M01 (TMC 2026) primary, K3/M06/M08/M09 supplementary.
所有参数有默认值 → config = SimConfig() 即可跑通。
"""

import math
from dataclasses import dataclass, field


@dataclass
class SimConfig:
    # === 网络拓扑 (K2/M01 Table III) ===
    n_iotd: int = 10                    # IoTD 数量
    n_uav: int = 4                      # UAV 数量
    n_leo: int = 8                      # LEO 卫星数量
    n_cs: int = 1                       # Cloud Server 数量
    area_size: float = 1000.0           # 区域大小 (m), 1 km × 1 km

    # === 轨道参数 ===
    leo_altitude: float = 500e3         # LEO 轨道高度 (m) (Ref: K2/M01)
    leo_planes: int = 2                 # 轨道面数 (2×4 配置)
    leo_inclination: float = 53.0       # 轨道倾角 (deg) (Ref: K2/M01)
    leo_min_elevation: float = 10.0     # 最小仰角 (deg) (Ref: M08)
    earth_radius: float = 6371e3        # 地球半径 (m)
    mu_earth: float = 3.986004418e14    # 地球引力常数 (m³/s²)

    # === 计算能力 (K2/M01 Table III) ===
    freq_iotd: float = 0.8e9            # IoTD CPU 频率 (Hz)
    freq_uav: float = 3.0e9             # UAV CPU 频率 (Hz)
    freq_leo_range: tuple[float, float] = (4.0e9, 5.0e9)  # LEO 均匀采样
    freq_cs: float = 10.0e9             # CS CPU 频率 (Hz)

    # === 能耗系数 κ (K2/M01 Table III) ===
    kappa_iotd: float = 5e-27           # VERIFY: IoTD κ_D = 5×10⁻²⁷，比其他节点高 50×
    kappa_uav: float = 1e-28            # κ_U = 10⁻²⁸
    kappa_leo: float = 1e-28            # κ_L = 10⁻²⁸
    kappa_cs: float = 1e-28             # κ_C = 10⁻²⁸

    # === 发射功率 (K2/M01 Table III) ===
    tx_power_iotd: float = 1.0          # Watts
    tx_power_uav: float = 2.0
    tx_power_leo: float = 5.0
    tx_power_cs: float = 5.0

    # === 信道参数 (K2/M01 §II-C + Table III/IV) ===
    bw_g2u: float = 20e6                # IoTD-UAV 带宽 (Hz)
    bw_g2s: float = 15e6                # IoTD-LEO 带宽 (Hz)
    bw_u2s: float = 15e6                # UAV-LEO 带宽 (Hz)
    bw_isl: float = 1e9                 # LEO-LEO ISL 带宽 (Hz)
    bw_l2c: float = 1e9                 # LEO-CS 带宽 (Hz)
    noise_power_dbm: float = -100.0     # VERIFY: 这是总功率 dBm，非 PSD dBm/Hz
    rician_k: float = 2.0               # Rician K 因子 (Ref: 3GPP TR 38.811)
    antenna_gain: float = 1.0           # G_P
    bw_alloc_factor: float = 2.0        # ζ_B
    sr_condition: str = "average"       # Shadowed-Rician 条件: light/average/heavy

    # Shadowed-Rician 参数 (K2/M01 Table IV)
    sr_light: dict = field(default_factory=lambda: {"b0": 0.879, "m": 10.13, "Omega": 0.001})
    sr_average: dict = field(default_factory=lambda: {"b0": 0.252, "m": 5.21, "Omega": 0.004})
    sr_heavy: dict = field(default_factory=lambda: {"b0": 0.146, "m": 1.75, "Omega": 0.025})

    # 固定速率链路
    rate_cs_wired: float = 1e9          # CS 有线链路 1 Gbps

    # === DAG 参数 (K2/M01 §V + M06 Table VI) ===
    n_tasks: int = 20                   # 每个IoTD的DAG子任务数 J
    task_input_range: tuple[float, float] = (0.8e6, 4.0e6)    # bytes [0.8 MB, 4 MB]
    task_output_range: tuple[float, float] = (0.4e6, 1.0e6)   # bytes [0.4 MB, 1 MB]
    task_cycles_range: tuple[float, float] = (1.0e9, 3.0e9)   # cycles [1, 3] Gcycles
    task_deadline_range: tuple[float, float] = (50.0, 60.0)    # seconds
    daggen_fat: float = 0.6
    daggen_density: float = 0.4
    daggen_regular: float = 0.9
    daggen_jump: int = 1

    # === HGAT 架构 (M09 + M06) ===
    hgat_layers: int = 2
    hgat_heads: int = 4
    hgat_hidden: int = 64

    # === PPO 训练超参 (K2/M01 Table III, sweep 验证 2026-05-12) ===
    ppo_lr: float = 3e-4
    ppo_batch: int = 128
    ppo_clip: float = 0.2
    ppo_gae_lambda: float = 0.95
    ppo_gamma: float = 0.99
    ppo_epochs: int = 4
    ppo_max_grad_norm: float = 0.5
    ppo_entropy_coef: float = 0.01

    # === 奖励权重 (D009 + checkpoint 验证) ===
    # VERIFY: η_t=5.0 因为 T_norm << E_norm（快速节点延迟小），需放大匹配量级
    reward_eta_t: float = 5.0           # 延迟权重
    reward_eta_e: float = 0.5           # 能耗权重
    reward_lambda_1: float = 10.0       # 截止时间违约惩罚
    reward_lambda_2: float = 5.0        # UAV 计算资源溢出惩罚
    reward_lambda_3: float = 5.0        # LEO 计算资源溢出惩罚
    reward_domination_threshold: float = 0.80  # 单项占比警告阈值 (Ref: code-quality.md C1)

    # === UAV 约束 (K2/M01 Table III, 固定位置) ===
    uav_height_range: tuple[float, float] = (40.0, 60.0)  # m AGL

    # === 训练参数 ===
    total_episodes: int = 500
    update_interval: int = 10
    early_stop_patience: int = 100
    early_stop_kl_threshold: float = 0.15
    device: str = "cuda"
    seed: int = 42

    # === 派生量（__post_init__ 自动计算）===
    noise_power_w: float = 0.0
    total_tasks: int = 0
    n_nodes: int = 0
    uav_start: int = 0
    leo_start: int = 0
    cs_node: int = 0
    sats_per_plane: int = 0
    semi_major_axis: float = 0.0
    orbital_period: float = 0.0
    mean_motion: float = 0.0

    def __post_init__(self):
        c = self
        # 范围校验
        assert c.n_iotd > 0
        assert c.n_uav > 0
        assert c.n_leo > 0 and c.n_leo % c.leo_planes == 0, \
            f"n_leo ({c.n_leo}) 必须能被 leo_planes ({c.leo_planes}) 整除"
        assert c.area_size > 0
        assert c.freq_iotd > 0 and c.freq_uav > 0 and c.freq_cs > 0
        assert c.freq_leo_range[0] > 0 and c.freq_leo_range[1] >= c.freq_leo_range[0]
        assert c.n_tasks >= 2, "DAG 至少需要 2 个子任务"
        assert 0 < c.reward_eta_t and 0 < c.reward_eta_e
        assert 0 < c.reward_domination_threshold <= 1.0
        assert c.device in ("cpu", "cuda")

        # 派生物理量
        self.noise_power_w = math.pow(10, (c.noise_power_dbm - 30) / 10)

        # 节点布局
        self.uav_start = c.n_iotd
        self.leo_start = c.n_iotd + c.n_uav
        self.cs_node = c.n_iotd + c.n_uav + c.n_leo
        self.n_nodes = self.cs_node + 1
        self.total_tasks = c.n_iotd * c.n_tasks

        # 轨道派生量
        self.sats_per_plane = c.n_leo // c.leo_planes
        self.semi_major_axis = c.earth_radius + c.leo_altitude
        self.orbital_period = 2.0 * math.pi * math.sqrt(self.semi_major_axis ** 3 / c.mu_earth)
        self.mean_motion = 2.0 * math.pi / self.orbital_period
