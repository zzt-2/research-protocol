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
    """B7 Gardner TED FOE 参数族 (B7 OFC 2026, ofc.2026.w2a.62)

    场景参数跟 NDA-ML (SystemParams) 不统一——B7 锚论文工作点在 25GBaud/1.8kHz，
    0.6dB 增量在此场景实测。复现 B7 锚方法必须用 B7 场景参数。
    跨候选可比性通过 fair gain 维度统一（都报 HD-FEC），不通过场景参数统一。
    用户决策：2026-07-08 对话 4，B7 用锚论文原参数。

    所有 literature 字段 source 精确到 content.md 行号（FR-26 V6 读原文数值）。
    """

    # === 锚论文场景参数（content.md 行号溯源，FR-26 V6）===
    R_SYM_B7: float = Field(
        25e9,
        description="符号率 25 GBaud（B7 锚论文场景，跟 NDA-ML 2.5GBaud 不统一）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026 content.md L21/L25/L47「25-Gbaud DP-QPSK」",
            "symbol": "R_SYM_B7",
            "unit": "sym/s",
            "audit_flag": AuditFlag.OK,
            "note": "用户决策（2026-07-08）：B7 用锚论文原参数，不跟 NDA-ML 统一。复现 B7 0.6dB 增量必须用 25GBaud",
        },
    )
    LASER_LW_B7: float = Field(
        1800.0,
        description="激光线宽 1.8 kHz（NL-FT-DFB 激光器 Lorentzian 线宽，B7 锚论文场景）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026 content.md L47「Lorentzian linewidth of 1.8 kHz」",
            "symbol": "Δν_B7",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
            "note": "跟 NDA-ML LASER_LW=10kHz 不统一（B7 锚论文场景）",
        },
    )
    ROLL_OFF: float = Field(
        0.1,
        description="RRC 成型 roll-off 0.1",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026 content.md L47「roll-off factor is set to 0.1」",
            "symbol": "α_RRC",
            "audit_flag": AuditFlag.OK,
        },
    )
    RX_BW_GHZ: float = Field(
        36.75e9,
        description="接收电带宽 36.75 GHz",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026 content.md L47/L49「receiver bandwidth of 36.75 GHz」",
            "symbol": "BW_RX",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
        },
    )
    SPS_RX: float = Field(
        2.94,
        description="接收采样率 2.94 sps（FOE 前降采样到 2 sps）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026 content.md L47/L49「sampling rate of 2.94 sps, downsampled to 2 sps before entering the FOE algorithms」",
            "symbol": "sps",
            "unit": "sample/sym",
            "audit_flag": AuditFlag.OK,
        },
    )

    # === Doppler 扫频参数 ===
    DOPPLER_RANGE: float = Field(
        23e9,
        description="Doppler 频偏扫描范围上限（0-23 GHz）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026 content.md L49「scan range is set to 0 GHz–23 GHz and the interval is 1 GHz」",
            "symbol": "Δf_max",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
        },
    )
    DOPPLER_INTERVAL: float = Field(
        1e9,
        description="Doppler 扫频间隔 1 GHz",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026 content.md L49「interval is 1 GHz」",
            "symbol": "Δf_step",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
        },
    )
    LEO_DOPPLER_EXCURSION: float = Field(
        100e6,
        description="LEO Doppler 频偏幅度 ±100 MHz（三角波模拟参数）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026 content.md L47「periodic frequency excursion of ±100 MHz at a variation rate of 1 GHz/s」",
            "symbol": "Δf_LEO",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
            "note": "原 LEO_DOPPLER_RATE=30e3 错误，B7 原文给的是 ±100MHz@1GHz/s",
        },
    )
    LEO_DOPPLER_RATE: float = Field(
        1e9,
        description="LEO Doppler 变化率 1 GHz/s（三角波斜率）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026 content.md L47「variation rate of 1 GHz/s」",
            "symbol": "ḟ_LEO",
            "unit": "Hz/s",
            "audit_flag": AuditFlag.OK,
        },
    )

    # === 工作点参数 ===
    OSNR_WORKING_POINT_LOW: float = Field(
        10.0,
        description="OSNR 低 SNR 极限工作点 10 dB（B7 可解调，PSA FOE 失败）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026 content.md L21/L69「OSNR of 10 dB, which is where conventional algorithms fail」",
            "symbol": "OSNR_low",
            "unit": "dB",
            "audit_flag": AuditFlag.OK,
        },
    )
    OSNR_WORKING_POINT_MAIN: float = Field(
        17.0,
        description="OSNR 主测点 17 dB（poster Fig.3a 主测条件）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026 content.md L49「under an OSNR of 17 dB」",
            "symbol": "OSNR_main",
            "unit": "dB",
            "audit_flag": AuditFlag.OK,
        },
    )

    # === Gardner TED 参数 ===
    GARDNER_SPS: int = Field(
        2,
        description="Gardner TED 每符号采样数（FOE 前降采样后）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026 content.md L47「downsampled to 2 sps before entering the FOE algorithms」+ Gardner 1986 经典配置",
            "symbol": "SPS",
            "audit_flag": AuditFlag.OK,
        },
    )
    GARDNER_GAIN: float = Field(
        0.01,
        description="Gardner TED 环路增益（典型值，MVE 阶段近似）",
        json_schema_extra={
            "source_type": SourceType.typical,
            "source": "Gardner TED loop gain 典型值（B7 锚论文未明确给精确值）",
            "symbol": "K_p",
            "audit_flag": AuditFlag.WARNING,
            "note": "典型值而非文献精确值，MVE 阶段近似",
        },
    )

    # === FEC 阈值（跨候选可比，跟 NDA-ML 对齐）===
    HD_FEC_THRESHOLD: float = Field(
        3.8e-3,
        description="7% HD-FEC BER 阈值（跨候选主判据，跟 NDA-ML 对齐）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B11 行 181/191（跟 NDA-ML 共用 FEC 阈值定义）+ B7 content.md 用 BER 2e-2（本字段是跨候选主判据补充）",
            "symbol": "BER_HD-FEC",
            "audit_flag": AuditFlag.OK,
            "note": "B7 锚论文用 BER 2e-2，本字段为跨候选可比补充（0.4 双工作点决策）",
        },
    )
    BER_SENSITIVITY_THRESHOLD: float = Field(
        2e-2,
        description="BER 2e-2 锚论文一致性校验工作点（receiver sensitivity）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B7 OFC 2026 content.md L21/L65/L69「receiver sensitivity by 0.6 dB at a BER of 2×10⁻²」",
            "symbol": "BER_sens",
            "audit_flag": AuditFlag.OK,
            "note": "锚论文一致性校验用，B7 实测 0.6dB @ 此工作点",
        },
    )

    model_config = ConfigDict(frozen=True)


class B5Params(BaseModel):
    """B5 LEO Doppler 短时谱 FOE 参数族 (B5 锚 optcom.2024.130981)

    场景参数跟 NDA-ML (SystemParams) 部分一致（2.5GBaud 巧合）但线宽/调制不同。
    复现 B5 锚方法必须用 B5 场景参数。
    跨候选可比性通过 fair gain 维度统一（都报 BER 1e-3 + HD-FEC），不通过场景参数统一。
    用户决策：2026-07-08 对话 2，B5 用锚论文原参数（跟 B7 同模式）。

    所有 literature 字段 source 精确到 content.md 行号（FR-26 V6 读原文数值）。
    来源: S003 阶段 0.5 B5Params 草稿（_b5_params_draft.md），sandbox 对话 3 落盘。
    """

    # === 锚论文场景参数（content.md 行号溯源，FR-26 V6）===

    R_SYM_B5: float = Field(
        2.5e9,
        description="符号率 2.5 GBaud（B5 锚论文场景，跟 NDA-ML 2.5GBaud 一致）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 optcom.2024.130981 content.md L23/L47/L89/L91/L93/L109/L167「2.5-GBaud PM-QPSK」",
            "symbol": "R_SYM_B5",
            "unit": "sym/s",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚论文场景。跟 NDA-ML R_SYM=2.5e9 一致（巧合），跟 B7 R_SYM_B7=25e9 不一致",
        },
    )

    T_S_B5: float = Field(
        1 / 2.5e9,
        description="符号周期（derived from R_SYM_B5）",
        json_schema_extra={
            "source_type": SourceType.derived,
            "source": "T_S_B5 = 1 / R_SYM_B5",
            "symbol": "T_S_B5",
            "unit": "s",
            "audit_flag": AuditFlag.OK,
            "derived_from": ["R_SYM_B5"],
        },
    )

    F_CARRIER_B5: float = Field(
        1.934e14,
        description="光载波频率（1550 nm，B5 锚波长 1550.32nm）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L23「1550-nm wavelength」+ L93「wavelength... 1550.32 nm」",
            "symbol": "F_CARRIER_B5",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚 1550.32nm（TTX1995 激光），换算频率 c/λ",
        },
    )

    LASER_LW_B5: float = Field(
        20e3,
        description="激光线宽 20 kHz（TTX1995 激光器，B5 锚论文场景）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L93「linewidth of... 20 KHz」（TTX1995）",
            "symbol": "Δν_B5",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
            "note": "跟 NDA-ML LASER_LW=10kHz 不一致（B5 锚 20kHz），跟 B7 LASER_LW_B7=1800Hz 不一致。三个候选线宽各异——各自锚论文场景",
        },
    )

    MODULATION_B5: str = Field(
        "pm-qpsk",
        description="调制格式 PM-QPSK（B5 锚论文场景）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L23/L47/L89/L91/L93「PM-QPSK」",
            "symbol": "MOD_B5",
            "unit": "-",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚 PM-QPSK。跟 NDA-ML 16-APSK / B7 DP-QPSK 不同",
        },
    )

    ORBIT_ALT_B5: float = Field(
        600e3,
        description="LEO 轨道高度 600 km（NEO 卫星，B5 锚建模自 Ref [6] Shoji）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L143「NEO satellite orbit altitude at 600 km」（建模自 Ref [6] Shoji JLT 2012 OIPLL）",
            "symbol": "h_B5",
            "unit": "m",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚 NEO 600km 轨道。Doppler ±4.5GHz + 56MHz/s 变化率均基于此轨道",
        },
    )

    # === B5 核心算法参数（B5 锚特有，short_time_spectrum_foe 用）===

    DOPPLER_RANGE_B5: float = Field(
        4.5e9,
        description="Doppler 频偏范围 ±4.5 GHz（B5 捕获范围，覆盖 LEO Doppler 全量程）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L23（abstract，两次）/ L29（intro）/ L47（intro）/ L143（experiment）/ L149（results）五处一致",
            "symbol": "Δf_Doppler_B5",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
            "note": "B5 核心范围优势。conclusion L167 不含此数字。vs 传统 ±312.5MHz = 15× 范围扩展",
        },
    )

    DOPPLER_RATE_B5: float = Field(
        56e6,
        description="Doppler 变化率最大 56 MHz/s（NEO 600km 过顶）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L147「the maximum rate of change reaches 56 MHz/s」",
            "symbol": "df_Doppler_B5",
            "unit": "Hz/s",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚 NEO 600km 过顶最大变化率。B5 跟踪能力指标",
        },
    )

    ALPHA_B5: float = Field(
        6e8,
        description="系数 α=6×10⁸（正负功率谱面积比转频偏估计的转换系数，B5 锚式 2）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L85「the value of α is 6 × 10⁸」",
            "symbol": "α_B5",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
            "note": "B5 核心算法参数。影响收敛速度（L87 too large → 残频抖动大）。short_time_spectrum_foe 必须用此值",
        },
    )

    FFT_BLOCKS_B5: int = Field(
        1024,
        description="均值滤波 FFT 组数 1024（M 组 FFT 数据均值滤波）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L87「1024 sets of 16-point FFT data for mean filtering」",
            "symbol": "M_B5",
            "unit": "blocks",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚均值滤波组数。跟 FFT_POINTS_B5=16 组合",
        },
    )

    FFT_POINTS_B5: int = Field(
        16,
        description="FFT 点数 16（每块 16 点 FFT，2 的幂次）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L87「16-point FFT」+ L141「16 points」",
            "symbol": "N_FFT_B5",
            "unit": "samples",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚 FFT 点数。块长 16 点 = 6.4ns（@2.5GBaud），远短于湍流相干时间 ~1ms（0.3b 验证 2 依据）",
        },
    )

    # === B5 残频/性能指标（锚论文报告值，sandbox 验证目标）===

    RESIDUAL_FREQ_COARSE_STD_B5: float = Field(
        140e6,
        description="粗补偿后残频标准差 σ<140 MHz（B5 锚报告值，sandbox 验证目标）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L23/L47「standard deviation... less than 140 MHz」",
            "symbol": "σ_res_coarse_B5",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚报告值。sandbox 路径 C 验证目标（湍流下前馈归一化后是否仍 <140MHz）",
        },
    )

    RESIDUAL_FREQ_COARSE_MAX_B5: float = Field(
        250e6,
        description="粗补偿后残频最大值 250 MHz（含激光 250MHz 抖动 + 算法误差）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L149/L167「maximum value... is 250 MHz... laser will have a 250 MHz frequency jitter, and secondly, the algorithmic compensation has errors」",
            "symbol": "res_max_B5",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚诚实标注：250MHz 含激光抖动非纯算法误差。湍流场景需重测",
        },
    )

    RESIDUAL_FREQ_FINE_B5: float = Field(
        5e6,
        description="精确补偿后残频 <5 MHz（B5 锚报告值，精确补偿级）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L149「residual frequency offset... approximately less than 5 MHz [20]」（引 [20] Liu 2023 PADE 精补偿）",
            "symbol": "res_fine_B5",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚精确补偿残频。属后续 DSP（PADE），非 B5 短时谱粗估任务",
        },
    )

    PRECISE_RANGE_B5: float = Field(
        312.5e6,
        description="精估范围 ±312.5 MHz（=B/8=2.5Gbaud/8，传统 FOE 标准范围）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L57/L95/L149/L167「[−B/8, +B/8]... [−312.5MHz, +312.5MHz]」",
            "symbol": "Δf_precise_B5",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
            "note": "B5 粗估任务边界 = 残频落此范围即完成任务。跟 [60] Leven 公式 27 Δfm=fs/8N 同族（N=1）",
        },
    )

    BER_TARGET_B5: float = Field(
        1e-3,
        description="BER 工作点 1e-3（B5 锚 + sat.1553 + [60] Leven 三者一致，主工作点）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L149「BER of 1 × 10⁻³」+ sat.1553 L353 + [60] Leven L121",
            "symbol": "BER_B5",
            "unit": "-",
            "audit_flag": AuditFlag.OK,
            "note": "主工作点。跨候选可比另报 HD-FEC 3.8e-3（0.4.3 决策）",
        },
    )

    RX_SENSITIVITY_DBM_B5: float = Field(
        -48.0,
        description="BER 1e-3 接收灵敏度 −48 dBm（B5 锚报告值）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L149「BER of 1 × 10⁻³ can be obtained at a receiver sensitivity of −48 dBm」",
            "symbol": "P_rx_B5",
            "unit": "dBm",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚接收灵敏度。测试区间 −51~−10 dBm（L93/L127），最优光功率 −25 dBm（L93 ATT2）",
        },
    )

    # === 硬件/采样参数（B5 锚 FPGA 实验配置）===

    ADC_RATE_B5: float = Field(
        5e9,
        description="ADC 采样率 5 GSa/s（B5 锚 FPGA 实验）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L93「sampling rate of 5 GSa/s」",
            "symbol": "f_s_ADC_B5",
            "unit": "samples/s",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚 ADC 采样率。8bit 分辨率（L93）",
        },
    )

    FPGA_CLOCK_B5: float = Field(
        312.5e6,
        description="FPGA DSP 核时钟 312.5 MHz（B5 锚 Intel Arria 10）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L95「DSP core driven by a 312.5 MHz clock frequency」",
            "symbol": "f_FPGA_B5",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚 FPGA 时钟。Intel Arria 10（L93/L95）",
        },
    )

    CYCLE_PERIOD_B5: float = Field(
        3.0,
        description="3s 循环周期（B5 锚外层迭代重估周期，前馈开环）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "B5 锚 content.md L93「The process cycles every 3 s」",
            "symbol": "T_cycle_B5",
            "unit": "s",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚外层迭代重估周期。3s 周期重估是前馈重复执行（0.3a 确认），非闭环 TF",
        },
    )

    # === FEC 阈值（跨候选可比，跟 B7/NDA-ML 对齐）===

    HD_FEC_THRESHOLD_B5: float = Field(
        3.8e-3,
        description="7% HD-FEC BER 阈值（跨候选可比补充工作点，0.4.3 决策）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "sat.1553 L440 + D005 会议门槛 + 跨候选统一叙事（B7Params HD_FEC_THRESHOLD 同源）",
            "symbol": "BER_HD-FEC_B5",
            "unit": "-",
            "audit_flag": AuditFlag.OK,
            "note": "B5 锚论文用 BER 1e-3，本字段为跨候选可比补充（0.4.3 双工作点决策）",
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


class GGTimeParams(BaseModel):
    """Gamma-Gamma 时间域衰落模型参数族 (Q-CMA-FADE Step A, FR-20 前置门控)

    现有 ``gg_block`` 块间独立（无时间动力学），本参数族支撑时间相关 GG 包络
    生成器 ``common/_gg_time.py::gg_time_envelope``——块内恒定物理成立
    (τ_c ≫ 符号周期)，块间用 AR(1) 相关 (相干时间 τ_c 控制)。

    物理基础（全标来源，FR-20）:
    - f_G 公式: Greenwood 1977 JOSA 67(3):390-393 + Andrews&Phillips 2005
    - τ_c = 1/(2π·f_G): Conan 1995 JOSA A 12(7):1559 + Andrews 2005 §12
      (注: τ_c 是强度闪烁相干时间，非 AO 相位校正时间常数 0.314·r₀/V)
    - τ_c 典型 1-100 ms: sat.1553:167 (>1ms) + s24248036:872 (1-100ms)
    - 强度功率谱高频 f⁻¹¹ᐟ³: Tatarskii 1971 / Clifford 1971 / Ishimaru 1972
      (已由 formulas-master F24/F25 Kolmogorov 谱覆盖，此处不重复)

    所有 literature 字段 source 标精确文献（含行号）。
    来源: 2026-07-11 Step A 实施（GG 时间域衰落模型 FR-20 前置门控）。
    """

    # === Greenwood 频率 (湍流时间尺度) ===
    GREENWOOD_FREQ_DEFAULT: float = Field(
        100.0,
        description="Greenwood 频率默认值 100 Hz（中湍流典型，星地 LEO）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "arxiv 2208.00836 content.md L51「60 Hz to 1 kHz depending on environment」+ Greenwood 1977 JOSA 67(3):390 公式推导 + 外部教材交叉验证（Andrews&Phillips 2005 Ch.10-12, Tyson 2011 Ch.8）。典型星地链路 10-1000 Hz",
            "symbol": "f_G",
            "unit": "Hz",
            "audit_flag": AuditFlag.WARNING,
            "note": "仅 1 篇本地论文(arxiv 2208.00836)给数值范围；f_G 严格公式依赖 Cn²(h)·V(h) 路径积分，本字段取中湍流代表值 100Hz，实际应扫描",
        },
    )
    GREENWOOD_FREQ_SWEEP: tuple = Field(
        default_factory=lambda: (30.0, 100.0, 300.0, 1000.0),
        description="f_G 扫描档（守 C1 扫描非单点）。30Hz 弱湍 / 100Hz 中湍 / 300Hz 中强 / 1000Hz 强湍",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "arxiv 2208.00836:51 范围 60-1000Hz + Greenwood 1977 公式量级",
            "symbol": "f_G(sweep)",
            "unit": "Hz",
            "audit_flag": AuditFlag.WARNING,
        },
    )

    # === 相干时间 ===
    TAU_C_COEFF: float = Field(
        1.0 / (2 * np.pi),
        description="τ_c = TAU_C_COEFF / f_G 的系数 1/(2π)（强度闪烁相干时间，Conan 1995）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "Conan, Rousset & Madec 1995 JOSA A 12(7):1559 时间功率谱转折频率 ~2π·f_G + Andrews&Phillips 2005 §12。注: AO 相位校正用 0.314·r₀/V（Roddier 1999），本字段是强度闪烁 τ_c 非相位 τ₀",
            "symbol": "c_τ",
            "unit": "-",
            "audit_flag": AuditFlag.OK,
            "note": "系数 1/(2π) 是强度闪烁谱转折定义，与 AO 的 0.214/f_G 不同（后者是相位校正带宽特定定义）",
        },
    )

    # === 横风速度（f_G 公式输入）===
    WIND_SPEED_GROUND: float = Field(
        10.0,
        description="地面横风典型速度 10 m/s（f_G 公式 V(h) 剖面的地面代表值）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "papers/doi/10.3390_photonics10121312/content.md L566（Paillier 全数字 OPLL，地面风 0-43 m/s，强湍场景图用 5/60 m/s 对比）+ Bufton 风模型",
            "symbol": "V_g",
            "unit": "m/s",
            "audit_flag": AuditFlag.WARNING,
            "note": "仅地面风；LEO 卫星视运动对湍流层横扫的贡献由仰角定，本字段不含（需仰角几何，留作后续精确化）",
        },
    )

    # === Cn² 结构常数地面值（f_G/H-V 剖面输入，与 TurbulenceParams 的 α,β 互补）===
    CN2_GROUND_WEAK: float = Field(
        1e-15,
        description="弱湍流地面 Cn²(0) = 1×10⁻¹⁵ m⁻²ᐟ³（Hufnagel-Valley 剖面地面值）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "papers/doi/10.3390_photonics10121312/content.md L560（H-V 剖面 C0 弱 1e-15 / 中 5e-14 / 强 1e-13）",
            "symbol": "C_n²(0)_weak",
            "unit": "m^{-2/3}",
            "audit_flag": AuditFlag.OK,
        },
    )
    CN2_GROUND_MODERATE: float = Field(
        5e-14,
        description="中等湍流地面 Cn²(0) = 5×10⁻¹⁴ m⁻²ᐟ³",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "papers/doi/10.3390_photonics10121312/content.md L560",
            "symbol": "C_n²(0)_mod",
            "unit": "m^{-2/3}",
            "audit_flag": AuditFlag.OK,
        },
    )
    CN2_GROUND_STRONG: float = Field(
        1e-13,
        description="强湍流地面 Cn²(0) = 1×10⁻¹³ m⁻²ᐟ³",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "papers/doi/10.3390_photonics10121312/content.md L560",
            "symbol": "C_n²(0)_strong",
            "unit": "m^{-2/3}",
            "audit_flag": AuditFlag.OK,
        },
    )

    # === AR(1) 生成方法参数 ===
    AR1_METHOD: str = Field(
        "gar",
        description="时间相关 GG 生成方法: 'gar'（默认，精确 Gamma 边缘，分位数匹配畸变 log-ACF 略低<2%）/ 'lognormal'（对数域 AR(1) log-ACF=ρ 精确，但强湍边缘近似偏差大 KS~0.15）",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "MVE 阶段务实选择。gar: 标准正态 AR(1)+分位数映射到精确 Gamma 边缘(KS<0.006 全湍流档)，但非线性映射使 log-ACF 略低于 ρ(高 ρ 区<2%)。lognormal: 对 log(X) 平稳 AR(1)，log-ACF[lag]=ρ 精确(匹配 Conan τ_c 定义)，但边缘矩匹配在强湍(β<1)偏差大(weak KS=0.046/mod 0.074/strong 0.149)",
            "audit_flag": AuditFlag.WARNING,
            "note": "默认 gar（边缘精确，跨湍流强度稳健）；lognormal 适弱中湍且需 log-ACF 精确时。验证见 gg_time_validation.json edge_check_independent",
        },
    )

    # === τ_c 本地校验锚点（sat.1553/s24248036，供验证脚本对比）===
    TAU_C_LITERATURE_LOWER_MS: float = Field(
        1.0,
        description="文献 τ_c 下限 1 ms（sat.1553 自述 >1ms）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "papers/doi/10.1002_sat.1553/content.md L167「coherence time of more than 1 ms」",
            "symbol": "τ_c,min",
            "unit": "ms",
            "audit_flag": AuditFlag.OK,
        },
    )
    TAU_C_LITERATURE_UPPER_MS: float = Field(
        100.0,
        description="文献 τ_c 上限 100 ms（s24248036 综述 1-100ms 范围上端）",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "papers/doi/10.3390_s24248036/content.md L872「coherence time ... ranging from 1 to 100 ms」",
            "symbol": "τ_c,max",
            "unit": "ms",
            "audit_flag": AuditFlag.OK,
        },
    )

    model_config = ConfigDict(frozen=True)

    def tau_c_from_fg(self, f_g: float) -> float:
        """τ_c = 1/(2π·f_G)（Conan 1995 强度闪烁相干时间）。

        返回秒。f_G=100Hz → τ_c=1.59ms。
        """
        return self.TAU_C_COEFF / f_g

    def rho_block(self, f_g: float, block: int, t_s: float) -> float:
        """块间 AR(1) 相关系数 ρ = exp(-Δt/τ_c)，Δt = block·T_S（块时长）。

        ρ 越接近 1 块间越相关（τ_c 大 / f_G 小 → 慢变 → 高相关）。
        """
        tau_c = self.tau_c_from_fg(f_g)
        dt = block * t_s
        return float(np.exp(-dt / tau_c))


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
    gg_time: GGTimeParams = Field(default_factory=GGTimeParams)

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
