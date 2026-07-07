"""参数溯源系统 — 所有仿真参数的唯一真相源

架构:
  params.py (唯一真相源, 零依赖除了 pydantic + numpy)
      ↑
  common.py (从 params 导入, 重新导出常量 + 函数逻辑不变)
      ↑
  experiments/*.py / tests/ (从 common import, 零修改)

使用:
  from params import SimulationConfig
  cfg = SimulationConfig()
  cfg.system.R_SYM  # 2.5e9
"""

from enum import Enum
from typing import Optional, Dict, Any, List, Tuple

import numpy as np
from pydantic import BaseModel, Field, ConfigDict


# ─── 枚举 ─────────────────────────────────────────────────────

class SourceType(str, Enum):
    literature = "literature"
    derived = "derived"
    typical = "typical"
    measured = "measured"
    assumption = "assumption"
    sweep_optimal = "sweep_optimal"
    regression = "regression"


class AuditFlag(str, Enum):
    OK = "OK"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    DEAD = "DEAD"


# ─── 参数模型 ─────────────────────────────────────────────────

class SystemParams(BaseModel):
    R_SYM: float = Field(
        2.5e9,
        description="符号率 (Gsps)",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "Zhao 2025 (doi:10.1109/JLT.2025.xxx)",
            "symbol": "R_SYM",
            "unit": "sym/s",
            "audit_flag": AuditFlag.OK,
            "spec_ref": "SPEC.md §1.3",
        },
    )
    T_S: float = Field(
        1 / 2.5e9,
        description="符号周期",
        json_schema_extra={
            "source_type": SourceType.derived,
            "source": "T_S = 1 / R_SYM",
            "symbol": "T_S",
            "unit": "s",
            "audit_flag": AuditFlag.OK,
            "derived_from": ["R_SYM"],
        },
    )
    F_CARRIER: float = Field(
        1.55e14,
        description="光载波频率 (1550 nm)",
        json_schema_extra={
            "source_type": SourceType.typical,
            "source": "C-band 标准波长 1550 nm",
            "symbol": "f_c",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
        },
    )
    LASER_LW: float = Field(
        10e3,
        description="激光线宽（单端激光器，全场景统一真相源）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "Valjus sat.1553 (doi:10.1002/sat.1553) §4.2 L438：星地 FSO ECL 典型 0.1-1MHz@28GBaud (ΔνTs≈10⁻⁶-10⁻⁵)；单载波 2.5GBaud 配 ECL (1-100kHz) 是典型。10kHz@2.5GBaud → ΔνTs=2.51e-5 落在该区间低端",
            "symbol": "Δν",
            "unit": "Hz",
            "audit_flag": AuditFlag.WARNING,
            "note": "D-007: 全场景（AWGN + 湍流）线宽单一真相源。Valjus sat.1553 §4.2 L438 (papers/doi/10.1002_sat.1553/content.md)",
        },
    )

    model_config = ConfigDict(frozen=True)


class TurbulenceParams(BaseModel):
    turb_weak_alpha: float = Field(
        4.0,
        description="弱湍流 GG α",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "夜间/高仰角场景典型值",
            "symbol": "α (weak)",
            "audit_flag": AuditFlag.WARNING,
        },
    )
    turb_weak_beta: float = Field(
        3.0,
        description="弱湍流 GG β",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "同 α(weak)",
            "symbol": "β (weak)",
            "audit_flag": AuditFlag.WARNING,
        },
    )
    turb_moderate_alpha: float = Field(
        2.5,
        description="中等湍流 GG α",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "白天/中仰角场景",
            "symbol": "α (moderate)",
            "audit_flag": AuditFlag.WARNING,
        },
    )
    turb_moderate_beta: float = Field(
        1.8,
        description="中等湍流 GG β",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "同 α(moderate)",
            "symbol": "β (moderate)",
            "audit_flag": AuditFlag.WARNING,
        },
    )
    turb_strong_alpha: float = Field(
        1.5,
        description="强湍流 GG α",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "低仰角/恶劣天气场景",
            "symbol": "α (strong)",
            "audit_flag": AuditFlag.WARNING,
        },
    )
    turb_strong_beta: float = Field(
        0.8,
        description="强湍流 GG β",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "同 α(strong)",
            "symbol": "β (strong)",
            "audit_flag": AuditFlag.WARNING,
        },
    )
    # --- 上行(地面→卫星)湍流场景 (sat.1553 Valjus 2025 综述 Table 1) ---
    # 设计选择: sat.1553 给 Rytov 方差 σ²_R=0.15(上行弱)/0.25(上行强), 远大于下行 0.029
    # (大气湍流主要在低空, 上行信号发射即受扰). 严格 σ²_R→α/β 映射是另一研究方向,
    # 此处务实选两组比现有 strong(α1.5/β0.8)更极端的 α/β 代表对应强度区间.
    turb_uplink_moderate_alpha: float = Field(
        1.2,
        description="上行中湍流 GG α (比 strong 略强, 对应 σ²_R≈0.15)",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "设计选择: 参考 sat.1553 上行 σ²_R=0.15, 选对应强度区间 Gamma-Gamma α/β",
            "symbol": "α (uplink_moderate)",
            "audit_flag": AuditFlag.WARNING,
        },
    )
    turb_uplink_moderate_beta: float = Field(
        0.9,
        description="上行中湍流 GG β (比 strong 略强)",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "设计选择: 参考 sat.1553 上行 σ²_R=0.15, 选对应强度区间 Gamma-Gamma α/β",
            "symbol": "β (uplink_moderate)",
            "audit_flag": AuditFlag.WARNING,
        },
    )
    turb_uplink_strong_alpha: float = Field(
        1.0,
        description="上行强湍流 GG α (明显比 strong 强, 接近 deep fade, 对应 σ²_R≈0.25)",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "设计选择: 参考 sat.1553 上行 σ²_R=0.25, 选对应强度区间 Gamma-Gamma α/β",
            "symbol": "α (uplink_strong)",
            "audit_flag": AuditFlag.WARNING,
        },
    )
    turb_uplink_strong_beta: float = Field(
        0.7,
        description="上行强湍流 GG β (明显比 strong 强, 接近 deep fade)",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "设计选择: 参考 sat.1553 上行 σ²_R=0.25, 选对应强度区间 Gamma-Gamma α/β",
            "symbol": "β (uplink_strong)",
            "audit_flag": AuditFlag.WARNING,
        },
    )

    model_config = ConfigDict(frozen=True)

    def as_dict(self) -> Dict[str, Tuple[float, float]]:
        return {
            "weak": (self.turb_weak_alpha, self.turb_weak_beta),
            "moderate": (self.turb_moderate_alpha, self.turb_moderate_beta),
            "strong": (self.turb_strong_alpha, self.turb_strong_beta),
            # 上行场景 (设计选择, 参考 sat.1553 上行 σ²_R=0.15/0.25)
            "uplink_moderate": (self.turb_uplink_moderate_alpha, self.turb_uplink_moderate_beta),
            "uplink_strong": (self.turb_uplink_strong_alpha, self.turb_uplink_strong_beta),
        }


class DopplerParams(BaseModel):
    DOPPLER_HIGH: float = Field(
        150e6,
        description="高多普勒变化率 (LEO 500km)",
        json_schema_extra={
            "source_type": SourceType.derived,
            "source": "LEO 500km 轨道速度 ~7.6 km/s 仰角变化率推导",
            "symbol": "f_dot",
            "unit": "Hz/s",
            "audit_flag": AuditFlag.WARNING,
        },
    )
    DOPPLER_LOW: float = Field(
        30e6,
        description="低多普勒变化率",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "无来源",
            "symbol": "f_dot (low)",
            "unit": "Hz/s",
            "audit_flag": AuditFlag.WARNING,
        },
    )
    F_RESIDUAL: float = Field(
        1e6,
        description="残余频偏 (FOE 粗补偿后)",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "FOE 补偿后残余, Δf ≈ 1/(4·N_fft·T_S) ≈ 0.98 MHz",
            "symbol": "f_res",
            "unit": "Hz",
            "audit_flag": AuditFlag.WARNING,
        },
    )

    model_config = ConfigDict(frozen=True)


class KFQParams(BaseModel):
    sigma2_turb: float = Field(
        ...,
        description="湍流引起的相位噪声方差",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "NO VERIFIED SOURCE",
            "symbol": "σ²_turb",
            "audit_flag": AuditFlag.CRITICAL,
            "impact": "直接控制 KF Q[0,0], 量级偏离则所有 KF 结论可能失效",
        },
    )
    kappa: float = Field(
        ...,
        description="kappa 参数 (design_Q 中未使用, 死参数)",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "NO VERIFIED SOURCE",
            "symbol": "κ",
            "audit_flag": AuditFlag.DEAD,
            "note": "定义于 Q_TURB_PARAMS 但 design_Q() 从未使用",
        },
    )

    model_config = ConfigDict(frozen=True)


class KFParams(BaseModel):
    sigma2_laser: float = Field(
        2 * np.pi * 10e3 * (1 / 2.5e9),
        description="激光相位噪声方差 = 2π·Δν·T_S",
        json_schema_extra={
            "source_type": SourceType.derived,
            "source": "标准激光相位噪声模型 σ²_laser = 2π·Δν·T_S (Viterbi 1963)",
            "symbol": "σ²_laser",
            "audit_flag": AuditFlag.OK,
            "derived_from": ["LASER_LW", "T_S"],
        },
    )
    Q_fine_df: float = Field(
        (50e3) ** 2,
        description="KF Q[1,1] 覆盖值 (覆盖 design_Q 计算)",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "NO VERIFIED SOURCE — SPEC 未记录此覆盖行为",
            "symbol": "Q_fine_df",
            "unit": "(Hz)²",
            "audit_flag": AuditFlag.CRITICAL,
            "impact": "在 kf_*_recovery 中覆盖 design_Q() 的 Q[1,1]",
        },
    )
    P_init_phase: float = Field(
        (np.pi / 4) ** 2,
        description="KF 初始相位不确定性",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "π/4 对应 QPSK 星座间距的一半",
            "symbol": "P_init[0,0]",
            "audit_flag": AuditFlag.WARNING,
        },
    )
    P_init_freq: float = Field(
        (2 * np.pi * 100e3) ** 2,
        description="KF 初始频偏不确定性 (±100 kHz)",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "假设 ±100 kHz 初始频偏",
            "symbol": "P_init[1,1]",
            "audit_flag": AuditFlag.WARNING,
        },
    )
    alpha_ema: float = Field(
        0.5,
        description="导频 h 估计 EMA 平滑系数",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "默认值 0.5",
            "symbol": "α_ema",
            "audit_flag": AuditFlag.WARNING,
        },
    )
    q_params_weak: KFQParams = Field(
        default_factory=lambda: KFQParams(sigma2_turb=1e-6, kappa=1.56e-6)
    )
    q_params_moderate: KFQParams = Field(
        default_factory=lambda: KFQParams(sigma2_turb=1e-4, kappa=9.80e-5)
    )
    q_params_strong: KFQParams = Field(
        default_factory=lambda: KFQParams(sigma2_turb=1e-3, kappa=3.79e-4)
    )

    model_config = ConfigDict(frozen=True)

    def get_q_params(self, turb_name: str) -> KFQParams:
        mapping = {
            "weak": self.q_params_weak,
            "moderate": self.q_params_moderate,
            "strong": self.q_params_strong,
        }
        return mapping[turb_name]


class DPLLParams(BaseModel):
    omega_n_default: float = Field(
        8e6,
        description="DPLL 默认自然频率",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "默认值, 非最优",
            "symbol": "ω_n",
            "unit": "Hz",
            "audit_flag": AuditFlag.WARNING,
        },
    )
    omega_n_optimal: float = Field(
        20e6,
        description="DPLL 最优自然频率 (D1 搜索结果)",
        json_schema_extra={
            "source_type": SourceType.sweep_optimal,
            "source": "sim_kf_stress_D1_D2.py 序贯搜索最优值",
            "symbol": "ω_n*",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
        },
    )
    zeta: float = Field(
        np.sqrt(2) / 2,
        description="DPLL 阻尼系数 (Butterworth)",
        json_schema_extra={
            "source_type": SourceType.derived,
            "source": "二阶环路 Butterworth 响应: ζ = √2/2",
            "symbol": "ζ",
            "audit_flag": AuditFlag.OK,
        },
    )

    model_config = ConfigDict(frozen=True)


class FOEParams(BaseModel):
    N_fft_default: int = Field(
        1024,
        description="默认 FFT 窗长度",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "默认值",
            "symbol": "N_fft",
            "audit_flag": AuditFlag.WARNING,
        },
    )
    N_fft_optimal_strong: int = Field(
        2048,
        description="强湍流最优 N_fft",
        json_schema_extra={
            "source_type": SourceType.sweep_optimal,
            "source": "D1 序贯搜索",
            "audit_flag": AuditFlag.OK,
        },
    )
    nfft_zp: int = Field(
        8192,
        description="FFT 零填充点数 (插值精度)",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "默认值 (8x 零填充)",
            "audit_flag": AuditFlag.WARNING,
        },
    )

    model_config = ConfigDict(frozen=True)


class VVParams(BaseModel):
    M_vv_default: int = Field(
        64,
        description="默认 VV 滑动窗长度",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "默认值, 非最优",
            "symbol": "N_w",
            "audit_flag": AuditFlag.WARNING,
        },
    )
    M_vv_optimal: int = Field(
        256,
        description="最优 VV 滑动窗长度",
        json_schema_extra={
            "source_type": SourceType.sweep_optimal,
            "source": "D1 序贯搜索",
            "audit_flag": AuditFlag.OK,
        },
    )

    model_config = ConfigDict(frozen=True)


class BPSParams(BaseModel):
    B_default: int = Field(
        32,
        description="默认 BPS 测试相位数",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "默认值",
            "symbol": "B",
            "audit_flag": AuditFlag.WARNING,
        },
    )
    Nw_default: int = Field(
        61,
        description="默认 BPS 滑动窗长度",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "默认值",
            "symbol": "N_w (BPS)",
            "audit_flag": AuditFlag.WARNING,
        },
    )

    model_config = ConfigDict(frozen=True)


class ExperimentParams(BaseModel):
    BLOCK: int = Field(
        100,
        description="信道块大小 (块内 h 恒定)",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "NO VERIFIED SOURCE",
            "symbol": "N_block",
            "unit": "symbols",
            "audit_flag": AuditFlag.WARNING,
        },
    )
    GAMMA_BAR_DEFAULT: float = Field(
        100.0,
        description="默认平均 SNR (20 dB)",
        json_schema_extra={
            "source_type": SourceType.typical,
            "source": "FSO 系统设计典型工作点 20 dB",
            "symbol": "γ̄",
            "audit_flag": AuditFlag.OK,
        },
    )

    model_config = ConfigDict(frozen=True)


class B11Params(BaseModel):
    """B11 NDA-ML STO+CPE 参数族 (10.1109/LPT.2024.3523478)

    用于 Step 4a 维度 D (CPE/FOE 链) MVE 评估。

    **D-007 (2026-07-07) 变更**：CLW/BAUD_RATE/PN_VARIANCE 三字段标 DEAD。
    原因：D002 已把 B11 重定位为"理论参考不对标 baseline"，我们方法重定义为单载波
    时域 NDA-ML。AWGN 场景作为"NDA-ML vs DA ML"对比（都是我们自己的单载波方法），
    理应用单载波参数（SystemParams.LASER_LW=10kHz @ R_SYM=2.5GBaud），不应继续用
    B11 的 OFDM 场景参数（500kHz @ 25GBaud）。三字段保留供 explore/ 历史探针 import
    不破（_ber_oracle_upperbound/_crb_lower_bound 读 cfg.b11.M0_POWER 等），但线宽类
    字段不再作为仿真真相源——仿真真相源统一为 SystemParams.LASER_LW 单字段。
    M0_POWER/HD_FEC_THRESHOLD/DFT_SIZE/CP_LEN 与线宽无关，保持 active。"""
    CLW: float = Field(
        500e3,
        description="combined laser linewidth (收发两端线宽之和) — B11 论文原始 OFDM 场景值",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B11 (10.1109/LPT.2024.3523478) 行 143/155：combined laser linewidth 扫至 500 kHz",
            "symbol": "Δν_CLW",
            "unit": "Hz",
            "audit_flag": AuditFlag.DEAD,
            "note": "D-007: B11 OFDM 原始场景参数，Formal 仿真已改用 SystemParams.LASER_LW (单载波 10kHz)。仅供 explore/ 历史探针 import，不作为仿真真相源",
        },
    )
    HD_FEC_THRESHOLD: float = Field(
        7e-2,
        description="7% HD-FEC overhead 对应 BER 阈值",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B11 行 181/191：7% HD-FEC threshold (BER=3.8e-3 软判决 7% 开销)",
            "symbol": "BER_HD-FEC",
            "audit_flag": AuditFlag.OK,
        },
    )
    BAUD_RATE: float = Field(
        25e9,
        description="波特率 25 GBaud — B11 论文原始 OFDM 场景值",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B11 行 143/155：25 GBaud",
            "symbol": "R_B",
            "unit": "sym/s",
            "audit_flag": AuditFlag.DEAD,
            "note": "D-007: B11 OFDM 原始场景参数，Formal 仿真已改用 SystemParams.R_SYM (单载波 2.5GBaud)。仅供 explore/ 历史探针 import",
        },
    )
    DFT_SIZE: int = Field(
        256,
        description="DFT 窗长度",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B11 行 155：DFT size N=256",
            "symbol": "N_DFT",
            "audit_flag": AuditFlag.OK,
        },
    )
    CP_LEN: int = Field(
        32,
        description="循环前缀长度",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B11 行 155：CP=32 sample",
            "symbol": "N_CP",
            "unit": "sample",
            "audit_flag": AuditFlag.OK,
        },
    )
    M0_POWER: int = Field(
        8,
        description="(8,8)-16APSK 升 M₀ 次幂去调制阶数",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B11 行 75-77：(8,8)-16APSK 升 M₀=8 次幂去调制, M₀=K·M₀/M=M₀ 对 K=2 M=16 M₀=8",
            "symbol": "M₀",
            "audit_flag": AuditFlag.OK,
        },
    )
    SNR_WORKING_POINT: float = Field(
        15.0,
        description="相位跟踪工作点 SNR",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B11 Fig.3 行 143：15 dB SNR 相位跟踪工作点",
            "symbol": "SNR",
            "unit": "dB",
            "audit_flag": AuditFlag.OK,
        },
    )
    PN_VARIANCE: float = Field(
        2 * np.pi * 500e3 * (1 / 25e9),
        description="Wiener 激光相位噪声方差 = 2π·Δν_CLW·T_S — B11 论文原始 OFDM 场景值",
        json_schema_extra={
            "source_type": SourceType.derived,
            "source": "B11 行 51：σp²=2πΔνTs Wiener laser phase noise",
            "symbol": "σ²_p",
            "unit": "rad²",
            "audit_flag": AuditFlag.DEAD,
            "derived_from": ["CLW", "T_S"],
            "note": "D-007: B11 OFDM 原始场景参数 (2π·500kHz·40ps=1.26e-4)。Formal 仿真已改用 2π·SystemParams.LASER_LW·T_S (2π·10kHz·400ps=2.51e-5)。仅供 explore/ 历史探针 import",
        },
    )

    model_config = ConfigDict(frozen=True)


class B7Params(BaseModel):
    """B7 Gardner TED FOE 参数族 (B7 OFC 2026)

    注意: B7 论文是 OFC 2026 会议, 其 Doppler range 0-23 GHz 来自地面 fiber 场景。
    B7 主线任务即"搬星地", 故部分参数为"原 paper 声明 + 星地迁移待验证"。"""
    DOPPLER_RANGE: float = Field(
        23e9,
        description="Doppler 频偏范围 (0-23 GHz)",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026：Doppler range 0-23 GHz",
            "symbol": "Δf_max",
            "unit": "Hz",
            "audit_flag": AuditFlag.WARNING,
            "note": "原 paper 为 fiber 场景声明值, 星地迁移待验证",
        },
    )
    LEO_DOPPLER_RATE: float = Field(
        30e3,
        description="LEO Doppler 变化率上界",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "Paillier 2020 JLT / IEEE sat.1553：LEO Doppler rate ~30 kHz/s（保守上界）",
            "symbol": "dḟ",
            "unit": "Hz/s",
            "audit_flag": AuditFlag.WARNING,
            "note": "Paillier/sat.1553 为 ISL/feeder 场景值, 星地场景可能不同",
        },
    )
    OSNR_WORKING_POINT: float = Field(
        10.0,
        description="OSNR 工作点",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026：OSNR 10 dB 工作点",
            "symbol": "OSNR",
            "unit": "dB",
            "audit_flag": AuditFlag.OK,
        },
    )
    GARDNER_SPS: int = Field(
        2,
        description="Gardner TED 每符号采样数",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "Gardner 1986 paper：每符号 2 采样（经典配置）",
            "symbol": "SPS",
            "audit_flag": AuditFlag.OK,
        },
    )
    GARDNER_GAIN: float = Field(
        0.01,
        description="Gardner TED 环路增益",
        json_schema_extra={
            "source_type": SourceType.typical,
            "source": "Gardner TED loop gain 典型值 0.01（不要求精确，MVE 阶段）",
            "symbol": "K_p",
            "audit_flag": AuditFlag.WARNING,
            "note": "典型值而非文献精确值, MVE 阶段近似",
        },
    )
    PSA_PILOT_SPACING: int = Field(
        32,
        description="PSA FOE pilot 间距",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "PSA FOE pilot 间距假设 32 符号（DVB-S2 标准 pilot pattern 近似，B7 未明确给）",
            "symbol": "N_p",
            "unit": "symbol",
            "audit_flag": AuditFlag.WARNING,
            "note": "B7 未明确给出, 用 DVB-S2 标准 pilot pattern 近似",
        },
    )

    model_config = ConfigDict(frozen=True)


class B3Params(BaseModel):
    """B3 子系统协同联合估计参数族 — 架构未决占位（B3 多孔径阵列 vs 单链路未拍板）。
    待对话 3 B3 架构决策后补全。"""
    NUM_BRANCHES_DIVERSITY: int = Field(
        4,
        description="4 支路分集配置（jphot+oe A1 已做联合）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "jphot+oe A1：4 支路地面 FSO 分集",
            "symbol": "N_branch",
            "audit_flag": AuditFlag.WARNING,
            "note": "架构未决，单链路 vs 多孔径阵列待对话 3 拍板",
        },
    )

    model_config = ConfigDict(frozen=True)


# ─── 聚合配置 ─────────────────────────────────────────────────

class SimulationConfig(BaseModel):
    system: SystemParams = Field(default_factory=SystemParams)
    turbulence: TurbulenceParams = Field(default_factory=TurbulenceParams)
    doppler: DopplerParams = Field(default_factory=DopplerParams)
    kf: KFParams = Field(default_factory=KFParams)
    dpll: DPLLParams = Field(default_factory=DPLLParams)
    foe: FOEParams = Field(default_factory=FOEParams)
    vv: VVParams = Field(default_factory=VVParams)
    bps: BPSParams = Field(default_factory=BPSParams)
    experiment: ExperimentParams = Field(default_factory=ExperimentParams)
    b11: B11Params = Field(default_factory=B11Params)
    b7: B7Params = Field(default_factory=B7Params)
    b3: B3Params = Field(default_factory=B3Params)

    model_config = ConfigDict(frozen=True)

    def get_turb_dict(self) -> Dict[str, Tuple[float, float]]:
        """兼容 common.py 的 TURB 格式"""
        return self.turbulence.as_dict()

    def get_fixed_cfg(self) -> Dict[str, Any]:
        """兼容 common.py 的 FIXED_CFG 格式"""
        return {
            "N_fft": int(self.foe.N_fft_default),
            "M_vv": self.vv.M_vv_default,
            "omega_n": self.dpll.omega_n_default,
            "zeta": self.dpll.zeta,
        }

    def get_fixed_cfg_optimal(self) -> Dict[str, Dict[str, Any]]:
        """兼容 common.py 的 FIXED_CFG_OPTIMAL 格式"""
        base = {
            "N_fft": int(self.foe.N_fft_default),
            "M_vv": self.vv.M_vv_optimal,
            "omega_n": self.dpll.omega_n_optimal,
            "zeta": self.dpll.zeta,
        }
        strong = {**base, "N_fft": self.foe.N_fft_optimal_strong}
        return {"weak": dict(base), "moderate": dict(base), "strong": strong}

    def get_q_turb_params(self) -> Dict[str, Dict[str, float]]:
        """兼容 common.py 的 Q_TURB_PARAMS 格式"""
        return {
            "weak": {"sigma2_turb": self.kf.q_params_weak.sigma2_turb,
                     "kappa": self.kf.q_params_weak.kappa},
            "moderate": {"sigma2_turb": self.kf.q_params_moderate.sigma2_turb,
                         "kappa": self.kf.q_params_moderate.kappa},
            "strong": {"sigma2_turb": self.kf.q_params_strong.sigma2_turb,
                       "kappa": self.kf.q_params_strong.kappa},
        }

    def design_Q(self, turb_name: str = 'strong',
                 f_dot: Optional[float] = None) -> np.ndarray:
        """替代 common.py 的 design_Q()"""
        if f_dot is None:
            f_dot = self.doppler.DOPPLER_HIGH
        q_params = self.kf.get_q_params(turb_name)
        sigma2_turb = q_params.sigma2_turb
        sigma2_df = (f_dot * self.system.T_S) ** 2 / 3
        sigma2_phi = self.kf.sigma2_laser + sigma2_turb
        return np.diag([sigma2_phi, sigma2_df])


# ─── 审计工具 ─────────────────────────────────────────────────

def audit_params(config: Optional[SimulationConfig] = None) -> Dict[str, Any]:
    """参数审计: 缺来源、死参数、覆盖未记录"""
    if config is None:
        config = SimulationConfig()

    result = {
        "summary": {"total": 0, "ok": 0, "warning": 0, "critical": 0, "dead": 0},
        "critical": [],
        "dead": [],
        "warnings": [],
    }

    def _audit_model(model: BaseModel, prefix: str = ""):
        for name, field_info in model.model_fields.items():
            val = getattr(model, name)
            extra = field_info.json_schema_extra or {}

            if isinstance(val, BaseModel):
                _audit_model(val, f"{prefix}{name}.")
                continue

            result["summary"]["total"] += 1
            flag = extra.get("audit_flag", AuditFlag.OK)
            flag_key = flag.value.lower() if isinstance(flag, AuditFlag) else str(flag).lower()
            if flag_key in result["summary"]:
                result["summary"][flag_key] += 1

            entry = {
                "param": f"{prefix}{name}",
                "value": repr(val),
                "source_type": str(extra.get("source_type", "unknown")),
                "source": extra.get("source", ""),
            }

            if flag == AuditFlag.CRITICAL:
                result["critical"].append(entry)
            elif flag == AuditFlag.DEAD:
                result["dead"].append(entry)
            elif flag == AuditFlag.WARNING:
                result["warnings"].append(entry)

    _audit_model(config)
    return result


def generate_audit_report(config: Optional[SimulationConfig] = None) -> str:
    """生成参数审计报告"""
    if config is None:
        config = SimulationConfig()

    audited = audit_params(config)
    lines = ["# 参数审计报告\n"]
    s = audited["summary"]
    lines.append(f"## 汇总: {s['critical']} CRITICAL, {s['dead']} DEAD, "
                 f"{s['warning']} WARNING, {s['ok']} OK\n")

    if audited["critical"]:
        lines.append("### CRITICAL\n")
        for e in audited["critical"]:
            lines.append(f"- **{e['param']}** = `{e['value']}`")
            lines.append(f"  - 来源: {e['source']}\n")

    if audited["dead"]:
        lines.append("### DEAD\n")
        for e in audited["dead"]:
            lines.append(f"- **{e['param']}** = `{e['value']}`\n")

    if audited["warnings"]:
        lines.append("### WARNING\n")
        for e in audited["warnings"]:
            lines.append(f"- **{e['param']}** = `{e['value']}` — {e['source']}")

    return "\n".join(lines)


if __name__ == "__main__":
    cfg = SimulationConfig()
    report = generate_audit_report(cfg)
    print(report)
