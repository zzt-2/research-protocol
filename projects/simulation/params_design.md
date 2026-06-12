# params.py 参数溯源系统 — 完整设计方案

> 创建: 2026-06-12 | 状态: 设计稿
> 前置审计: A1 参数审计 + B3 溯源追踪
> 设计原则: 参数必须有来源且单一真相源

---

## 1. params.py 完整设计

### 1.1 架构概览

```
params.py (唯一真相源)
├── 枚举定义: SourceType, AuditFlag
├── SystemParams      — 系统/物理参数
├── TurbulenceParams  — Gamma-Gamma 湍流模型参数
├── DopplerParams     — 多普勒/频偏参数
├── KFParams          — Kalman 滤波器参数 (per-turbulence)
├── FixedCfgParams    — Fixed 基线参数
├── BPSParams         — BPS 算法参数
├── DPLLParams        — DPLL 环路参数
├── ExperimentParams  — 实验编排参数
└── SimulationConfig  — 聚合配置 + 审计 + SPEC 生成
```

### 1.2 枚举定义

```python
from enum import Enum
from typing import Optional, Dict, Any, List, Tuple
from pydantic import BaseModel, Field
import numpy as np


class SourceType(str, Enum):
    """参数来源类型"""
    literature = "literature"      # 文献引用（论文/标准）
    derived = "derived"            # 从其他参数推导
    typical = "typical"            # 行业典型值（无特定文献）
    measured = "measured"          # 实测数据
    assumption = "assumption"      # 未验证假设
    sweep_optimal = "sweep_optimal" # 扫参获得的最优值
    regression = "regression"      # 与已知结果回归匹配


class AuditFlag(str, Enum):
    """审计级别"""
    OK = "OK"                      # 来源完整，已验证
    WARNING = "WARNING"            # 来源不完整，需补充
    CRITICAL = "CRITICAL"          # 无来源或来源不可靠，影响核心结论
    DEAD = "DEAD"                  # 已定义但从未使用
```

### 1.3 完整参数模型定义

#### SystemParams — 系统物理参数

```python
class SystemParams(BaseModel):
    """系统级物理参数 — 锁定，不可随意修改"""

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
        1 / 2.5e9,  # 400e-12
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
        1.55e14,  # 1550 nm
        description="光载波频率",
        json_schema_extra={
            "source_type": SourceType.typical,
            "source": "C-band 标准波长 1550 nm",
            "symbol": "f_c",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
            "note": "SPEC 记为 1.95e14 Hz (实际是 193.1 THz 光通信标准频率)，common.py 用 1.55e14 Hz 对应 λ=c/f。两者量级一致，不影响仿真（F_CARRIER 当前未被使用）",
        },
    )

    LASER_LW: float = Field(
        10e3,
        description="激光线宽",
        json_schema_extra={
            "source_type": SourceType.typical,
            "source": "窄线宽外腔式半导体激光器典型值 (1-100 kHz 范围，10 kHz 为常用设计值)",
            "symbol": "Δν",
            "unit": "Hz",
            "audit_flag": AuditFlag.WARNING,
            "note": "无特定文献引用，需确认与实验系统一致",
        },
    )

    model_config = ConfigDict(frozen=True)  # 参数不可运行时修改（Pydantic v2）
```

#### TurbulenceParams — 湍流模型参数

```python
class TurbulenceParams(BaseModel):
    """Gamma-Gamma 湍流分布参数"""

    # --- 弱湍流 ---
    turb_weak_alpha: float = Field(
        4.0,
        description="弱湍流 Gamma-Gamma α 参数",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "夜间/高仰角场景典型值，与多数 FSO 文献一致",
            "symbol": "α (weak)",
            "audit_flag": AuditFlag.WARNING,
            "note": "SPEC 未给出具体文献；需从 Rytov 方差反推确认",
        },
    )
    turb_weak_beta: float = Field(
        3.0,
        description="弱湍流 Gamma-Gamma β 参数",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "同 α(weak)",
            "symbol": "β (weak)",
            "audit_flag": AuditFlag.WARNING,
            "note": "α > β 时物理上对应弱湍流，值合理",
        },
    )

    # --- 中等湍流 ---
    turb_moderate_alpha: float = Field(
        2.5,
        description="中等湍流 Gamma-Gamma α 参数",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "白天/中仰角场景",
            "symbol": "α (moderate)",
            "audit_flag": AuditFlag.WARNING,
            "note": "SPEC 未给出具体文献",
        },
    )
    turb_moderate_beta: float = Field(
        1.8,
        description="中等湍流 Gamma-Gamma β 参数",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "同 α(moderate)",
            "symbol": "β (moderate)",
            "audit_flag": AuditFlag.WARNING,
            "note": "α=2.5, β=1.8，闪烁指数 SI ≈ 1/α + 1/β ≈ 0.77，属于中等湍流范围",
        },
    )

    # --- 强湍流 ---
    turb_strong_alpha: float = Field(
        1.5,
        description="强湍流 Gamma-Gamma α 参数",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "低仰角/恶劣天气场景",
            "symbol": "α (strong)",
            "audit_flag": AuditFlag.WARNING,
            "note": "α 接近 1 表示极强湍流",
        },
    )
    turb_strong_beta: float = Field(
        0.8,
        description="强湍流 Gamma-Gamma β 参数",
        json_schema_extra={
            "source_type": SourceType.literature,
            "source": "同 α(strong)",
            "symbol": "β (strong)",
            "audit_flag": AuditFlag.WARNING,
            "note": "β < 1 时方差发散，这是强闪烁的特征",
        },
    )

    class Config:
        frozen = True

    def as_dict(self) -> Dict[str, Tuple[float, float]]:
        """返回 TURB 格式的 {(name): (alpha, beta)}"""
        return {
            "weak": (self.turb_weak_alpha, self.turb_weak_beta),
            "moderate": (self.turb_moderate_alpha, self.turb_moderate_beta),
            "strong": (self.turb_strong_alpha, self.turb_strong_beta),
        }
```

#### DopplerParams — 多普勒/频偏参数

```python
class DopplerParams(BaseModel):
    """多普勒效应与残余频偏参数"""

    DOPPLER_HIGH: float = Field(
        150e6,
        description="高多普勒变化率（LEO 500km 场景）",
        json_schema_extra={
            "source_type": SourceType.derived,
            "source": "LEO 500km 轨道速度 ~7.6 km/s，仰角变化率推导",
            "symbol": "f_dot",
            "unit": "Hz/s",
            "audit_flag": AuditFlag.WARNING,
            "note": "SPEC 声称 LEO 500km 但未给推导细节。典型 LEO 场景 f_dot 在 50-300 MHz/s 范围，150 MHz/s 合理",
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
            "note": "用于场景对比但从未在已发布实验中使用",
        },
    )

    F_RESIDUAL: float = Field(
        1e6,
        description="残余频偏（FOE 粗补偿后）",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "无分析依据",
            "symbol": "f_res",
            "unit": "Hz",
            "audit_flag": AuditFlag.WARNING,
            "note": "假设 FOE 补偿后残余 1 MHz。应从 FFT-FOE 精度分析推导：Δf ≈ 1/(4·N_fft·T_S)，N_fft=1024 → Δf ≈ 0.98 MHz。当前值与此一致，但未显式记录推导",
        },
    )

    class Config:
        frozen = True
```

#### KFParams — Kalman 滤波器参数（最关键）

```python
class KFQParams(BaseModel):
    """单个湍流等级的 KF Q 矩阵参数"""

    sigma2_turb: float = Field(
        ...,  # 必填，per-turbulence 设不同值
        description="湍流引起的相位噪声方差",
        json_schema_extra={
            "source_type": SourceType.assumption,  # 全部三个值都是假设
            "source": "NO VERIFIED SOURCE",
            "symbol": "σ²_turb",
            "audit_flag": AuditFlag.CRITICAL,
            "impact": "此参数直接控制 KF Q[0,0]。如果量级偏离真实湍流相位噪声，所有 KF 结论可能失效",
            "derivation_hint": "可从 Gamma-Gamma 相位结构函数推导：σ²_φ(t) = 2.91·k²·C²_n·L·t^{5/3}（Rytov 理论），或从闪烁指数 SI 反推等效相位方差",
        },
    )

    kappa: float = Field(
        ...,  # 必填
        description="kappa 参数（design_Q 中未使用）",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "NO VERIFIED SOURCE",
            "symbol": "κ",
            "audit_flag": AuditFlag.DEAD,
            "note": "定义于 Q_TURB_PARAMS 但 design_Q() 从未使用此值。死参数",
        },
    )


class KFParams(BaseModel):
    """Kalman 滤波器参数集合"""

    # --- 激光相位噪声（推导量，有严格公式） ---
    sigma2_laser: float = Field(
        2 * np.pi * 10e3 * (1 / 2.5e9),  # = 2π·Δν·T_S
        description="激光相位噪声方差 = 2π·Δν·T_S",
        json_schema_extra={
            "source_type": SourceType.derived,
            "source": "标准激光相位噪声模型：σ²_laser = 2π·Δν·T_S (Viterbi 1963)",
            "symbol": "σ²_laser",
            "audit_flag": AuditFlag.OK,
            "derived_from": ["LASER_LW", "T_S"],
            "equation": "σ²_laser = 2π·Δν·T_S",
        },
    )

    # --- Q_fine_df 覆盖参数（最关键的隐藏参数） ---
    Q_fine_df: float = Field(
        (50e3) ** 2,  # 2.5e9
        description="KF 恢复函数中 Q[1,1] 的覆盖值（覆盖 design_Q 计算）",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "NO VERIFIED SOURCE — SPEC 未记录此覆盖行为",
            "symbol": "Q_fine_df",
            "unit": "(Hz)²",
            "audit_flag": AuditFlag.CRITICAL,
            "impact": "在 kf_oracle_recovery, kf_frame_h_recovery, kf_pilot_recovery 中覆盖 design_Q() 计算的 Q[1,1]。SPEC §2 和 test_common.py T7 都未记录此覆盖。实际效果：Q[1,1] = Q_fine_df * T_S²",
            "note": "B1 消融实验已证明 Q[1,1] 在 50x 范围内对 BER 无影响（'哑参数'），但覆盖行为本身必须显式记录",
        },
    )

    # --- P_init 初始协方差 ---
    P_init_phase: float = Field(
        (np.pi / 4) ** 2,
        description="KF 初始相位不确定性",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "NO VERIFIED SOURCE",
            "symbol": "P_init[0,0]",
            "audit_flag": AuditFlag.WARNING,
            "note": "B3 消融实验已验证 P_init 不影响稳态（KF 在导频处快速收敛），但初始值应有物理意义",
        },
    )

    P_init_freq: float = Field(
        (2 * np.pi * 100e3) ** 2,
        description="KF 初始频偏不确定性（假设 ±100 kHz 初始频偏）",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "NO VERIFIED SOURCE",
            "symbol": "P_init[1,1]",
            "audit_flag": AuditFlag.WARNING,
            "note": "假设初始频偏不确定性 ±100 kHz，但无分析依据。B3 已验证不影响稳态",
        },
    )

    # --- EMA 平滑系数 ---
    alpha_ema: float = Field(
        0.5,
        description="导频 h 估计 EMA 平滑系数",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "默认值 0.5",
            "symbol": "α_ema",
            "audit_flag": AuditFlag.WARNING,
            "note": "未做敏感性分析",
        },
    )

    # --- Per-turbulence Q 参数 ---
    q_params_weak: KFQParams = Field(
        default_factory=lambda: KFQParams(
            sigma2_turb=1e-6,
            kappa=1.56e-6,
        )
    )
    q_params_moderate: KFQParams = Field(
        default_factory=lambda: KFQParams(
            sigma2_turb=1e-4,
            kappa=9.80e-5,
        )
    )
    q_params_strong: KFQParams = Field(
        default_factory=lambda: KFQParams(
            sigma2_turb=1e-3,
            kappa=3.79e-4,
        )
    )

    class Config:
        frozen = True

    def get_q_params(self, turb_name: str) -> KFQParams:
        mapping = {
            "weak": self.q_params_weak,
            "moderate": self.q_params_moderate,
            "strong": self.q_params_strong,
        }
        return mapping[turb_name]
```

#### DPLLParams — DPLL 环路参数

```python
class DPLLParams(BaseModel):
    """DPLL 二阶环路参数"""

    omega_n_default: float = Field(
        8e6,
        description="DPLL 默认自然频率",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "默认值，非最优",
            "symbol": "ω_n",
            "unit": "Hz",
            "audit_flag": AuditFlag.WARNING,
            "note": "FIXED_CFG 的默认值，非最优。FIXED_CFG_OPTIMAL 用 20e6",
        },
    )

    omega_n_optimal: float = Field(
        20e6,
        description="DPLL 最优自然频率（D1 序贯搜索结果）",
        json_schema_extra={
            "source_type": SourceType.sweep_optimal,
            "source": "sim_kf_stress_D1_D2.py 序贯搜索最优值",
            "symbol": "ω_n*",
            "unit": "Hz",
            "audit_flag": AuditFlag.OK,
            "note": "所有湍流等级统一 20 MHz",
        },
    )

    zeta: float = Field(
        np.sqrt(2) / 2,
        description="DPLL 阻尼系数（Butterworth 最平坦响应）",
        json_schema_extra={
            "source_type": SourceType.derived,
            "source": "二阶环路 Butterworth 响应条件：ζ = √2/2",
            "symbol": "ζ",
            "audit_flag": AuditFlag.OK,
            "note": "经典数字通信教科书值",
        },
    )

    class Config:
        frozen = True
```

#### FOEParams — FFT-FOE 参数

```python
class FOEParams(BaseModel):
    """FFT 频偏估计参数"""

    N_fft_default: float = Field(
        1024,
        description="默认 FFT 窗长度",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "默认值",
            "symbol": "N_fft",
            "audit_flag": AuditFlag.WARNING,
            "note": "决定 FOE 精度和延迟。N_fft=1024 对应 1024·T_S ≈ 410 ns 观测窗",
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
        description="FFT 零填充点数（插值精度）",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "默认值",
            "audit_flag": AuditFlag.WARNING,
            "note": "8x 零填充，频率分辨率 = 1/(8192·T_S)。未做敏感性分析",
        },
    )

    class Config:
        frozen = True
```

#### VVParams — Viterbi-Viterbi CPR 参数

```python
class VVParams(BaseModel):
    """VV CPR 参数"""

    M_vv_default: int = Field(
        64,
        description="默认 VV 滑动窗长度",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "默认值",
            "symbol": "N_w",
            "audit_flag": AuditFlag.WARNING,
            "note": "窗长 64 对应 64·T_S ≈ 25.6 ns。非最优",
        },
    )

    M_vv_optimal: int = Field(
        256,
        description="最优 VV 滑动窗长度",
        json_schema_extra={
            "source_type": SourceType.sweep_optimal,
            "source": "D1 序贯搜索",
            "audit_flag": AuditFlag.OK,
            "note": "所有湍流等级统一 Nw=256",
        },
    )

    class Config:
        frozen = True
```

#### BPSParams — BPS 盲相位搜索参数

```python
class BPSParams(BaseModel):
    """BPS (Pfau 2009) 参数"""

    B_default: int = Field(
        32,
        description="默认测试相位数",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "默认值，无来源",
            "symbol": "B",
            "audit_flag": AuditFlag.WARNING,
            "note": "Pfau 2009 原文建议 B=32-64（QPSK），需确认",
        },
    )

    Nw_default: int = Field(
        61,
        description="默认滑动窗长度",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "默认值，无来源",
            "symbol": "N_w (BPS)",
            "audit_flag": AuditFlag.WARNING,
            "note": "Pfau 2009 原文建议 Nw 取决于激光线宽和 SNR。61 可能是经验值",
        },
    )

    class Config:
        frozen = True
```

#### ExperimentParams — 实验编排参数

```python
class ExperimentParams(BaseModel):
    """实验编排参数"""

    BLOCK: int = Field(
        100,
        description="信道块大小（块内 h 恒定）",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "NO VERIFIED SOURCE",
            "symbol": "N_block",
            "unit": "symbols",
            "audit_flag": AuditFlag.WARNING,
            "note": "SPEC 声称'相干时间~2-10ms >> 100·T_S'，但 100·T_S = 40 ns，远小于 ms 量级相干时间。C4 实验显示 BLOCK=20 在强湍流下更优（1.74x），暗示 BLOCK=100 可能过大",
            "derivation_hint": "应从湍流相干时间推导：τ_c ~ ρ_0/v_perp（Fried 参数/横向风速）。若 τ_c >> N_block·T_S 则块内 h 恒定假设成立",
        },
    )

    GAMMA_BAR_DEFAULT: float = Field(
        100.0,
        description="默认平均 SNR（20 dB）",
        json_schema_extra={
            "source_type": SourceType.typical,
            "source": "FSO 系统设计典型工作点 20 dB",
            "symbol": "γ̄",
            "audit_flag": AuditFlag.OK,
            "note": "所有已发布实验基于此单点",
        },
    )

    N_PILOTS_PER_BLOCK: int = Field(
        5,
        description="每块导频数（5/100 = 5% 开销）",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "默认值",
            "audit_flag": AuditFlag.OK,
            "note": "B4 消融实验已验证 5% near-optimal（net BER 与最优值之比 <1.5x）",
        },
    )

    AMP_LIMIT_THRESH: float = Field(
        3.0,
        description="幅度限幅阈值",
        json_schema_extra={
            "source_type": SourceType.assumption,
            "source": "默认值",
            "audit_flag": AuditFlag.WARNING,
            "note": "防止深衰落块噪声放大，但阈值无理论推导",
        },
    )

    class Config:
        frozen = True
```

#### SimulationConfig — 聚合配置

```python
class SimulationConfig(BaseModel):
    """仿真完整配置 — 所有参数的聚合入口"""

    system: SystemParams = Field(default_factory=SystemParams)
    turbulence: TurbulenceParams = Field(default_factory=TurbulenceParams)
    doppler: DopplerParams = Field(default_factory=DopplerParams)
    kf: KFParams = Field(default_factory=KFParams)
    dpll: DPLLParams = Field(default_factory=DPLLParams)
    foe: FOEParams = Field(default_factory=FOEParams)
    vv: VVParams = Field(default_factory=VVParams)
    bps: BPSParams = Field(default_factory=BPSParams)
    experiment: ExperimentParams = Field(default_factory=ExperimentParams)

    class Config:
        frozen = True

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
        strong = {
            **base,
            "N_fft": self.foe.N_fft_optimal_strong,
        }
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

    def design_Q(self, turb_name: str, f_dot: Optional[float] = None) -> np.ndarray:
        """替代 common.py 的 design_Q()"""
        if f_dot is None:
            f_dot = self.doppler.DOPPLER_HIGH
        q_params = self.kf.get_q_params(turb_name)
        sigma2_turb = q_params.sigma2_turb
        sigma2_df = (f_dot * self.system.T_S) ** 2 / 3
        sigma2_phi = self.kf.sigma2_laser + sigma2_turb
        return np.diag([sigma2_phi, sigma2_df])
```

---

## 2. 来源补全方案

### 2.1 参数状态汇总（41 参数逐个处理）

| # | 参数 | 当前状态 | 行动 | 新来源 | 新审计 |
|---|------|---------|------|--------|--------|
| 1 | R_SYM | OK | 保持 | Zhao 2025 | OK |
| 2 | T_S | OK | 保持 | T_S=1/R_SYM | OK |
| 3 | F_CARRIER | OK | 保持 | C-band 标准 | OK |
| 4 | LASER_LW | typical | 补文献 | 需查窄线宽激光器论文 | WARNING→OK |
| 5 | turb α/β (×3) | typical | 补文献 | 需从 Rytov 方差/Cn² 反推或引用 Andrews&Phillips | WARNING→OK |
| 6 | DOPPLER_HIGH | 部分推导 | 补推导 | 从轨道力学公式推导 | WARNING→OK |
| 7 | DOPPLER_LOW | assumption | 标记 | 保留 assumption | WARNING |
| 8 | F_RESIDUAL | assumption | 补推导 | 从 FFT-FOE 精度公式推导 | WARNING→OK |
| 9 | **sigma2_turb (×3)** | **CRITICAL** | **必须推导** | 见 2.2 节 | CRITICAL→OK/WARNING |
| 10 | **kappa (×3)** | **DEAD** | **移除** | N/A | DEAD→移除 |
| 11 | **Q_fine_df** | **CRITICAL** | **显式记录** | 标记为 assumption+记录覆盖行为 | CRITICAL→WARNING |
| 12 | P_init_phase | assumption | 标注 | π/4 对应 QPSK 星座间距的一半 | WARNING |
| 13 | P_init_freq | assumption | 标注 | 假设 ±100 kHz FOE 残余 | WARNING |
| 14 | alpha_ema | assumption | 标注 | 0.5 默认 | WARNING |
| 15 | omega_n_default | assumption | 标注 | 非最优，仅默认 | WARNING |
| 16 | omega_n_optimal | sweep | 保持 | D1 序贯搜索 | OK |
| 17 | zeta | OK | 保持 | Butterworth 条件 | OK |
| 18 | N_fft | assumption | 补推导 | FOE 精度公式 | WARNING→OK |
| 19 | N_fft_optimal_strong | sweep | 保持 | D1 搜索 | OK |
| 20 | nfft_zp | assumption | 标注 | 8x 零填充 | WARNING |
| 21 | M_vv_default | assumption | 标注 | 非最优 | WARNING |
| 22 | M_vv_optimal | sweep | 保持 | D1 搜索 | OK |
| 23 | DEF_B_BPS | assumption | 补文献 | Pfau 2009 JLT | WARNING→OK |
| 24 | DEF_NW_BPS | assumption | 补文献 | Pfau 2009 JLT | WARNING→OK |
| 25 | BLOCK | assumption | 补推导 | 从相干时间推导 | WARNING→OK |
| 26 | GAMMA_BAR_DEFAULT | typical | 保持 | 20 dB 典型值 | OK |
| 27 | N_PILOTS_PER_BLOCK | assumption | 保持 | B4 验证 OK | OK |
| 28 | AMP_LIMIT_THRESH | assumption | 标注 | 无推导 | WARNING |
| 29 | SIGMA2_LASER | OK | 保持 | 2πΔνT_S | OK |
| 30 | F_CARRIER | OK | 保持 | C-band | OK |

### 2.2 sigma2_turb 推导方案（最关键）

sigma2_turb 表示湍流引起的相位噪声方差，是 KF Q[0,0] 的核心分量。

**推导路径 1：Rytov 理论（推荐）**

湍流相位结构函数：
```
D_φ(τ) = E[(φ(t+τ) - φ(t))²] = 2.91 · k² · C²_n · L · (v_⊥·τ)^{5/3}
```

其中：
- k = 2π/λ（波数）
- C²_n = 大气折射率结构常数
- L = 传播距离
- v_⊥ = 横向风速

σ²_turb ≈ D_φ(T_S)（符号间隔内的相位方差）

对于弱湍流（C²_n ~ 10⁻¹⁷ m⁻²/³），σ²_turb 应在 10⁻⁸ ~ 10⁻⁶ 量级。
对于强湍流（C²_n ~ 10⁻¹³ m⁻²/³），σ²_turb 应在 10⁻⁴ ~ 10⁻² 量级。

**验证标准**：推导出的 σ²_turb 应与当前使用的 1e-6/1e-4/1e-3 在同一量级（±1 个数量级）。偏离超过 1 个数量级则需要重新评估所有 KF 结论。

**推导路径 2：Gamma-Gamma 闪烁指数反推**

闪烁指数 SI = 1/α + 1/β（Gamma-Gamma 分布），与 σ²_turb 存在经验关系。可通过仿真标定。

**执行计划**：
1. 查 Andrews & Phillips "Laser Beam Propagation through Random Media"（标准参考书）获取相位结构函数公式
2. 代入系统参数（λ=1550nm, L~500km, v_⊥~典型值）计算三个量级
3. 与当前值比对，记录差异
4. 若差异 >1 个数量级，触发红旗：所有 KF 结论需重验

### 2.3 Q_fine_df 覆盖行为的设计决策

**决策记录**（此决策应写入 SPEC.md）：

> **D-C2-01: Q_fine_df 覆盖行为**
>
> **背景**: kf_oracle_recovery, kf_frame_h_recovery, kf_pilot_recovery 三个函数中，调用 design_Q() 后立即用 `Q_fine[1,1] = Q_fine_df * T_S²` 覆盖 Q[1,1]。这意味着 design_Q() 中 `sigma2_df = (f_dot * T_S)²/3` 的计算结果被完全忽略。
>
> **决策**:
> - 方案 A（推荐）: 移除覆盖，让 design_Q() 的物理推导值生效。B1 已证明 Q[1,1] 在 50x 范围内不影响 BER，所以覆盖无实际效果，但保留物理推导更自洽。
> - 方案 B: 保留覆盖但显式记录为 KFParams.Q_fine_df，在 SPEC 中记录覆盖行为和原因。
>
> **选择**: 迁移初期选方案 B（不改变行为），后续分析 sigma2_turb 时一并审查 Q[1,1] 是否需要调整。

---

## 3. 死参数处理方案

### 3.1 kappa — 确认死参数

**证据**：
- `Q_TURB_PARAMS` 中每个湍流等级都定义了 `kappa`
- `design_Q()` 函数只使用 `sigma2_turb`，从未读取 `kappa`
- 全项目 grep 确认 `kappa` 仅出现在定义处和测试断言中

**处理**：
1. params.py 的 KFQParams 中 kappa 字段标记为 `AuditFlag.DEAD`
2. SimulationConfig.get_q_turb_params() 保留 kappa 键（兼容性），但标注为 deprecated
3. test_common.py 的 `test_q_turb_params_keys` 断言 `'kappa' in Q_TURB_PARAMS` 改为警告而非失败
4. 下一次 SPEC 大修订时移除 kappa

### 3.2 死参数自动检测

params.py 内建检测函数：

```python
def detect_dead_params(config: SimulationConfig) -> List[str]:
    """通过 AST 分析检测从未使用的参数。

    策略：读取 params.py 的所有 Field 名称，grep 整个项目中
    除 params.py 本身外的使用情况。未使用的是死参数候选。
    """
    import ast
    import pathlib

    params_file = pathlib.Path(__file__)
    tree = ast.parse(params_file.read_text())

    # 提取所有 Field 名称
    field_names = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.ClassDef,)):
            for item in node.body:
                if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                    field_names.add(item.target.id)

    # 在项目中搜索使用
    project_dir = params_file.parent
    dead = []
    for name in field_names:
        found = False
        for py_file in project_dir.rglob("*.py"):
            if py_file == params_file:
                continue
            content = py_file.read_text()
            if name in content:
                found = True
                break
        if not found:
            dead.append(name)

    return dead
```

### 3.3 F_CARRIER — 半死参数

F_CARRIER 定义但仅在测试中引用，不在仿真逻辑中使用（载波频率不影响离散时间基带仿真）。保留但标注。

---

## 4. SPEC 自动生成设计

### 4.1 核心函数

```python
def generate_spec_md(config: SimulationConfig) -> str:
    """从 SimulationConfig 生成 SPEC.md 参数表格。

    确保代码和文档永远一致：SPEC.md 的参数表从此函数生成，
    不允许手动编辑参数表。
    """
    lines = []
    lines.append("# 系统参数（自动生成自 params.py）\n")
    lines.append("> 生成时间: " + _timestamp() + "\n")
    lines.append("> 参数定义: params.py（唯一真相源）\n\n")

    # 系统参数表
    lines.append("## 系统参数\n")
    lines.append("| 参数 | 符号 | 值 | 单位 | 来源类型 | 来源 | 审计 |\n")
    lines.append("|------|------|-----|------|---------|------|------|\n")

    for field_name, field_info in config.system.model_fields.items():
        extra = field_info.json_schema_extra or {}
        val = getattr(config.system, field_name)
        lines.append(_param_row(field_name, val, extra))

    # ... 其他分组同理 ...

    return "\n".join(lines)


def _param_row(name: str, val, extra: dict) -> str:
    """生成单行参数表"""
    symbol = extra.get("symbol", "")
    unit = extra.get("unit", "")
    source_type = extra.get("source_type", "")
    source = extra.get("source", "")
    audit = extra.get("audit_flag", "")
    return f"| `{name}` | {symbol} | `{val}` | {unit} | {source_type} | {source} | {audit} |"


def generate_audit_report(config: SimulationConfig) -> str:
    """生成参数审计报告"""
    lines = ["# 参数审计报告\n"]
    critical = []
    dead = []
    warning = []

    def _walk(model: BaseModel, prefix: str = ""):
        for name, field_info in model.model_fields.items():
            extra = field_info.json_schema_extra or {}
            flag = extra.get("audit_flag", "OK")
            full_name = f"{prefix}{name}" if prefix else name
            entry = {
                "name": full_name,
                "value": getattr(model, name),
                "source_type": extra.get("source_type", ""),
                "source": extra.get("source", ""),
                "impact": extra.get("impact", ""),
            }
            if flag == AuditFlag.CRITICAL:
                critical.append(entry)
            elif flag == AuditFlag.DEAD:
                dead.append(entry)
            elif flag == AuditFlag.WARNING:
                warning.append(entry)

    _walk(config.system, "system.")
    _walk(config.turbulence, "turbulence.")
    _walk(config.doppler, "doppler.")
    _walk(config.kf, "kf.")
    _walk(config.dpll, "dpll.")
    _walk(config.foe, "foe.")
    _walk(config.vv, "vv.")
    _walk(config.bps, "bps.")
    _walk(config.experiment, "experiment.")

    lines.append(f"## 汇总: {len(critical)} CRITICAL, {len(dead)} DEAD, {len(warning)} WARNING\n")

    if critical:
        lines.append("### CRITICAL\n")
        for e in critical:
            lines.append(f"- **{e['name']}** = `{e['value']}`")
            lines.append(f"  - 来源: {e['source']}")
            if e['impact']:
                lines.append(f"  - 影响: {e['impact']}")
            lines.append("")

    if dead:
        lines.append("### DEAD\n")
        for e in dead:
            lines.append(f"- **{e['name']}** = `{e['value']}`")
            lines.append("")

    if warning:
        lines.append("### WARNING\n")
        for e in warning:
            lines.append(f"- **{e['name']}** = `{e['value']}` — {e['source']}")
            lines.append("")

    return "\n".join(lines)
```

### 4.2 一致性保障机制

```python
def assert_spec_consistency(config: SimulationConfig, spec_path: str):
    """断言 params.py 与 SPEC.md 参数表一致。

    在测试中调用，CI 中强制执行。
    """
    import re
    spec_content = Path(spec_path).read_text()
    # 从 SPEC 提取参数值
    for field_name, field_info in config.system.model_fields.items():
        val = getattr(config.system, field_name)
        # 在 SPEC 中查找对应行
        pattern = rf"`{field_name}`.*?`([^`]+)`"
        match = re.search(pattern, spec_content)
        if match:
            spec_val = match.group(1)
            # 数值比较（容差处理）
            assert _values_match(val, spec_val), \
                f"参数 {field_name}: params.py={val}, SPEC={spec_val}"
```

---

## 5. 与 common.py 的集成方案

### 5.1 迁移策略

params.py 作为新的唯一真相源，common.py 作为向后兼容垫片。

**Phase 1（本次实现）**:
- params.py 定义所有参数模型
- common.py 从 params.py 导入参数，重新导出为模块级常量
- 所有现有 `from common import *` 调用无需修改

**Phase 2（后续）**:
- 逐步将实验脚本改为从 params.py 直接导入 SimulationConfig
- common.py 中的常量导出标记为 deprecated

### 5.2 common.py 垫片设计

```python
# common.py 顶部（Phase 1 改造后）

from params import SimulationConfig

# 唯一配置实例
_CFG = SimulationConfig()

# 向后兼容：导出为模块级常量
R_SYM = _CFG.system.R_SYM
T_S = _CFG.system.T_S
F_CARRIER = _CFG.system.F_CARRIER
LASER_LW = _CFG.system.LASER_LW

TURB = _CFG.get_turb_dict()
BLOCK = _CFG.experiment.BLOCK

DOPPLER_HIGH = _CFG.doppler.DOPPLER_HIGH
DOPPLER_LOW = _CFG.doppler.DOPPLER_LOW
F_RESIDUAL = _CFG.doppler.F_RESIDUAL

FIXED_CFG = _CFG.get_fixed_cfg()
FIXED_CFG_OPTIMAL = _CFG.get_fixed_cfg_optimal()

GAMMA_BAR_DEFAULT = _CFG.experiment.GAMMA_BAR_DEFAULT

DEF_B_BPS = _CFG.bps.B_default
DEF_NW_BPS = _CFG.bps.Nw_default

SIGMA2_LASER = _CFG.kf.sigma2_laser
Q_TURB_PARAMS = _CFG.get_q_turb_params()
```

### 5.3 模块间依赖关系

```
params.py (零依赖，只依赖 pydantic + numpy)
    ↑
common.py (从 params 导入，重新导出常量 + 函数逻辑不变)
    ↑
experiments/*.py (从 common import，零修改)
tests/test_common.py (从 common import，零修改)
```

---

## 6. 审计工具设计

### 6.1 audit_params() 函数

```python
def audit_params(config: Optional[SimulationConfig] = None) -> Dict[str, Any]:
    """参数审计：缺来源、死参数、覆盖未记录。

    Returns:
        {
            "summary": {"total": N, "ok": N, "warning": N, "critical": N, "dead": N},
            "critical": [...],
            "dead": [...],
            "warnings": [...],
            "unrecorded_overrides": [...],
        }
    """
    if config is None:
        config = SimulationConfig()

    result = {
        "summary": {"total": 0, "ok": 0, "warning": 0, "critical": 0, "dead": 0},
        "critical": [],
        "dead": [],
        "warnings": [],
        "unrecorded_overrides": [],
    }

    def _audit_model(model: BaseModel, prefix: str = ""):
        for name, field_info in model.model_fields.items():
            val = getattr(model, name)
            extra = field_info.json_schema_extra or {}

            # 跳过嵌套模型
            if isinstance(val, BaseModel):
                _audit_model(val, f"{prefix}{name}.")
                continue

            result["summary"]["total"] += 1
            flag = extra.get("audit_flag", AuditFlag.OK)
            result["summary"][flag.value.lower()] += 1

            entry = {
                "param": f"{prefix}{name}",
                "value": repr(val),
                "source_type": extra.get("source_type", "unknown"),
                "source": extra.get("source", ""),
            }

            if flag == AuditFlag.CRITICAL:
                result["critical"].append(entry)
            elif flag == AuditFlag.DEAD:
                result["dead"].append(entry)
            elif flag == AuditFlag.WARNING:
                result["warnings"].append(entry)

    _audit_model(config)

    # 检测覆盖未记录
    result["unrecorded_overrides"] = _detect_overrides(config)

    return result


def _detect_overrides(config: SimulationConfig) -> List[Dict]:
    """检测函数参数中覆盖 config 值的情况。

    例如 kf_oracle_recovery 的 Q_fine_df 参数覆盖了 design_Q 的计算。
    """
    overrides = []
    # Q_fine_df 覆盖 design_Q 的 sigma2_df 计算
    overrides.append({
        "param": "kf.Q_fine_df",
        "overrides": "design_Q() -> Q[1,1] = sigma2_df",
        "locations": [
            "kf_oracle_recovery(Q_fine_df=...)",
            "kf_frame_h_recovery(Q_fine_df=...)",
            "kf_pilot_recovery(Q_fine_df=...)",
        ],
        "recorded_in_spec": False,
    })
    return overrides
```

### 6.2 测试集成

```python
# tests/test_params.py

class TestParamAudit:
    """参数溯源审计测试"""

    def test_no_critical_params(self):
        """不应有 CRITICAL 级别参数（CI 门控）"""
        report = audit_params()
        assert len(report["critical"]) == 0, (
            f"存在 {len(report['critical'])} 个 CRITICAL 参数:\n" +
            "\n".join(f"  - {p['param']}: {p['source']}" for p in report["critical"])
        )

    def test_no_dead_params(self):
        """不应有 DEAD 参数"""
        report = audit_params()
        assert len(report["dead"]) == 0, (
            f"存在 {len(report['dead'])} 个死参数:\n" +
            "\n".join(f"  - {p['param']}" for p in report["dead"])
        )

    def test_all_params_have_source(self):
        """所有参数必须有 source 字段"""
        config = SimulationConfig()
        missing = []
        def _check(model, prefix=""):
            for name, fi in model.model_fields.items():
                val = getattr(model, name)
                if isinstance(val, BaseModel):
                    _check(val, f"{prefix}{name}.")
                    continue
                extra = fi.json_schema_extra or {}
                if not extra.get("source"):
                    missing.append(f"{prefix}{name}")
        _check(config)
        assert len(missing) == 0, f"以下参数缺 source: {missing}"

    def test_spec_consistency(self):
        """params.py 与 SPEC.md 参数值一致"""
        config = SimulationConfig()
        assert_spec_consistency(config, "SPEC.md")

    def test_frozen_config(self):
        """配置不可运行时修改"""
        config = SimulationConfig()
        with pytest.raises(Exception):  # ValidationError
            config.system.R_SYM = 3e9
```

**CI 门控策略**:
- `test_no_critical_params`: 初期允许失败（sigma2_turb 仍为 CRITICAL），设为 `@pytest.mark.xfail`
- `test_no_dead_params`: 初期允许失败（kappa 仍为 DEAD），设为 `@pytest.mark.xfail`
- 来源补全后移除 xfail

---

## 7. 迁移步骤（具体可执行）

### Step 1: 创建 params.py（~300 行）

1. 创建 `projects/simulation/params.py`
2. 实现所有 Pydantic 模型（SourceType, AuditFlag, SystemParams, ..., SimulationConfig）
3. 实现 `design_Q()` 方法
4. 实现 `audit_params()` 和 `generate_spec_md()`
5. 验证：`python -c "from params import SimulationConfig; c = SimulationConfig(); print(audit_params(c))"`

### Step 2: 改造 common.py 垫片（~20 行修改）

1. common.py 顶部添加 `from params import SimulationConfig` 和 `_CFG = SimulationConfig()`
2. 替换所有硬编码常量为 `_CFG.xxx` 导出
3. 保留所有函数实现不变（函数内引用模块级常量自动生效）
4. 验证：`python -c "from common import R_SYM; print(R_SYM)"` 输出不变

### Step 3: 验证测试套件通过

1. `python -m pytest tests/test_common.py -v` 全部通过
2. 无导入错误：所有 21 个实验脚本的 import 链不受影响
3. 参数值不变：T7 参数一致性测试逐项通过

### Step 4: 添加 params 审计测试

1. 创建 `tests/test_params.py`
2. 实现 TestParamAudit 中的所有测试
3. CRITICAL/DEAD 测试用 `@pytest.mark.xfail` 标记
4. 验证：`python -m pytest tests/test_params.py -v`

### Step 5: SPEC.md 参数表更新

1. 运行 `generate_spec_md()` 生成新参数表
2. 替换 SPEC.md §1.3 和 §2 的参数表
3. 添加来源类型和审计级别列
4. SPEC.md 其他内容（信号模型、评估方法、已验证事实）不变

### Step 6: sigma2_turb 推导（独立子任务）

1. 查阅 Andrews & Phillips 获取相位结构函数
2. 代入系统参数计算三个等级的 sigma2_turb
3. 与当前值 (1e-6, 1e-4, 1e-3) 比对
4. 更新 params.py 的 source 和 audit_flag
5. 若差异 >1 个数量级，触发红旗报告

### Step 7: 清理

1. kappa 标记 deprecated
2. Q_fine_df 覆盖行为写入 SPEC.md 决策记录
3. 运行完整测试确认无回归

---

## 附录 A: 参数编号索引

| ID | 名称 | 域 | 模型 | 审计 |
|----|------|----|------|------|
| P-01 | R_SYM | system | SystemParams.R_SYM | OK |
| P-02 | T_S | system | SystemParams.T_S | OK |
| P-03 | F_CARRIER | system | SystemParams.F_CARRIER | OK |
| P-04 | LASER_LW | system | SystemParams.LASER_LW | WARNING |
| P-05 | turb_weak_alpha | turbulence | TurbulenceParams.turb_weak_alpha | WARNING |
| P-06 | turb_weak_beta | turbulence | TurbulenceParams.turb_weak_beta | WARNING |
| P-07 | turb_moderate_alpha | turbulence | TurbulenceParams.turb_moderate_alpha | WARNING |
| P-08 | turb_moderate_beta | turbulence | TurbulenceParams.turb_moderate_beta | WARNING |
| P-09 | turb_strong_alpha | turbulence | TurbulenceParams.turb_strong_alpha | WARNING |
| P-10 | turb_strong_beta | turbulence | TurbulenceParams.turb_strong_beta | WARNING |
| P-11 | DOPPLER_HIGH | doppler | DopplerParams.DOPPLER_HIGH | WARNING |
| P-12 | DOPPLER_LOW | doppler | DopplerParams.DOPPLER_LOW | WARNING |
| P-13 | F_RESIDUAL | doppler | DopplerParams.F_RESIDUAL | WARNING |
| P-14 | sigma2_laser | kf | KFParams.sigma2_laser | OK |
| P-15 | sigma2_turb_weak | kf | KFParams.q_params_weak.sigma2_turb | **CRITICAL** |
| P-16 | sigma2_turb_moderate | kf | KFParams.q_params_moderate.sigma2_turb | **CRITICAL** |
| P-17 | sigma2_turb_strong | kf | KFParams.q_params_strong.sigma2_turb | **CRITICAL** |
| P-18 | kappa_weak | kf | KFParams.q_params_weak.kappa | **DEAD** |
| P-19 | kappa_moderate | kf | KFParams.q_params_moderate.kappa | **DEAD** |
| P-20 | kappa_strong | kf | KFParams.q_params_strong.kappa | **DEAD** |
| P-21 | Q_fine_df | kf | KFParams.Q_fine_df | **CRITICAL** |
| P-22 | P_init_phase | kf | KFParams.P_init_phase | WARNING |
| P-23 | P_init_freq | kf | KFParams.P_init_freq | WARNING |
| P-24 | alpha_ema | kf | KFParams.alpha_ema | WARNING |
| P-25 | omega_n_default | dpll | DPLLParams.omega_n_default | WARNING |
| P-26 | omega_n_optimal | dpll | DPLLParams.omega_n_optimal | OK |
| P-27 | zeta | dpll | DPLLParams.zeta | OK |
| P-28 | N_fft_default | foe | FOEParams.N_fft_default | WARNING |
| P-29 | N_fft_optimal_strong | foe | FOEParams.N_fft_optimal_strong | OK |
| P-30 | nfft_zp | foe | FOEParams.nfft_zp | WARNING |
| P-31 | M_vv_default | vv | VVParams.M_vv_default | WARNING |
| P-32 | M_vv_optimal | vv | VVParams.M_vv_optimal | OK |
| P-33 | B_default | bps | BPSParams.B_default | WARNING |
| P-34 | Nw_default | bps | BPSParams.Nw_default | WARNING |
| P-35 | BLOCK | experiment | ExperimentParams.BLOCK | WARNING |
| P-36 | GAMMA_BAR_DEFAULT | experiment | ExperimentParams.GAMMA_BAR_DEFAULT | OK |
| P-37 | N_PILOTS_PER_BLOCK | experiment | ExperimentParams.N_PILOTS_PER_BLOCK | OK |
| P-38 | AMP_LIMIT_THRESH | experiment | ExperimentParams.AMP_LIMIT_THRESH | WARNING |

**汇总**: 8 OK, 23 WARNING, 4 CRITICAL, 3 DEAD

---

## 附录 B: 设计决策记录

| ID | 决策 | 选择 | 理由 | 日期 |
|----|------|------|------|------|
| D-C2-01 | Q_fine_df 覆盖 | Phase B: 保留但记录 | B1 证明无影响，不改行为 | 2026-06-12 |
| D-C2-02 | kappa 处理 | 保留但标 DEAD+deprecated | 兼容性，下版移除 | 2026-06-12 |
| D-C2-03 | 垫片策略 | common.py 从 params 导出 | 零修改 21 个实验脚本 | 2026-06-12 |
| D-C2-04 | frozen=True | 所有模型不可变 | 防止运行时意外修改参数 | 2026-06-12 |
| D-C2-05 | sigma2_turb 行动 | 推导后再改值 | 先建立推导框架，再确认值是否正确 | 2026-06-12 |
