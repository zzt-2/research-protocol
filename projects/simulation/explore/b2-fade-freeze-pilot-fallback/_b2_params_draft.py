"""B2-Q2 双模切换参数（sandbox 阶段 1 用，草稿落盘）.

真相源（每项标 source + 读原文数值，守 TL-26 / FR-26 / FR-20）:
- 激光线宽 LASER_LW: 继承 D-007 SystemParams.LASER_LW=10kHz @ R_SYM=2.5GBaud（全场景统一）
- Wiener PN σ²_pN: 2π·LASER_LW·T_S = 2.51e-5（派生量，不是独立参数）
- GG α/β: 继承 step4a TurbulenceParams（weak α4/β3, moderate α2.5/β1.8, strong α1.5/β0.8）
  · source 标注（params.py:97-156）：'夜间/高仰角场景典型值' 等 = 设计选择典型值，audit_flag=WARNING
  · 不是 sat.1553 scenario 定义（阶段 0.5 悬而未决 #3 答案）
  · B2-Q2 sandbox 复现 step4a 配置（继承相同 α/β），不改 α/β
- pilot 配置: 继承 step4a DA_PILOT_SPACING=4 / 真符号 pilot / 25% overhead
- fade 阈值 γ_th: sandbox 实测 rx 功率分布后定扫参范围 [γ̄−3σ, γ̄−1σ]（不拍脑袋，FR-20/TL-26）
- ρ_fade: sandbox 逐点实测（每 OSNR × 湍流档，不预设）

⚠️ 命名澄清（阶段 0.1 子 agent 发现，阶段 0.5 制度化）:
- σ²_pN（Wiener PN）是单值 2.51e-5，不是 fade 三档
- GG α/β 是 fade 统计参数，不是相位噪声
- 禁用 'σp² 三档' 表述（混淆两个物理量）
- sat.1553 σp²=0.25 是 Rytov 方差 σ²_R，跟 Wiener PN σ²_pN=2.51e-5 不同物理量

⚠️ 阶段 0.5 草稿 import 修正（主线 sandbox 前核查发现）:
- params.py 无 GammaGammaParams 类（阶段 0.5 草稿误写）
- α/β 在 TurbulenceParams 子类，经 SimulationConfig.get_turb_dict() 聚合到 common._config.TURB
- 正确 import: from common._config import TURB（或 from params import SimulationConfig）

架构约束（阶段 0.3 前馈化 INVARIANT 级，不撞 D006）:
- 4 估计器全部前馈闭式（_recovery.py 核查：da_ml L136 线性回归 / nda_ml L171 mean-angle / psa_foe L435 差分最小二乘 / fft_foe L37 4次幂峰值）
- fade 检测用开环功率阈值 γ_th（不闭环，不用误差驱动）
- 模式切换是 switch 不是 feedback
- 补偿一次性（无跨块迭代）
"""
import os
import sys
import numpy as np

# import 路径对齐 step4a 锚脚本（_time_domain_crlb.py:97-112）
_SIM_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)

from common._config import TURB, BLOCK as CH_BLOCK, LASER_LW, R_SYM, T_S, DOPPLER_HIGH
from params import SimulationConfig


# =============================================================================
# 继承常量（不自建，从 common._config / params 单字段读，守 TL-13 共用 + D-007 单一真相源）
# =============================================================================
_cfg = SimulationConfig()

# 系统（D-007 统一：单载波 10kHz @ 2.5GBaud）
LASER_LW = LASER_LW                     # 10e3 Hz（common._config 透传）
R_SYM = R_SYM                           # 2.5e9 sym/s
T_S = T_S                               # 4e-10 s（派生 = 1/R_SYM）
SIGMA2_PN = 2 * np.pi * LASER_LW * T_S  # 2.51e-5（派生，Wiener PN 单值，2π·10kHz·4e-10）

# GG α/β（fade 三档，从 TURB dict 读，继承 step4a TurbulenceParams）
TURB_LEVELS = ['weak', 'moderate', 'strong']
GG_ALPHA_BETA = {lvl: TURB[lvl] for lvl in TURB_LEVELS}
# weak (4.0, 3.0) / moderate (2.5, 1.8) / strong (1.5, 0.8)

# pilot 配置（step4a 继承，spacing=4 真符号 pilot 25% overhead）
DA_PILOT_SPACING = 4
PILOT_OVERHEAD_DB_FULL = 10.0 * np.log10(DA_PILOT_SPACING / (DA_PILOT_SPACING - 1))  # 1.2494 dB（全帧）

# 块结构（继承 step4a）
N_DFT = 256                  # 逐块恢复块大小（= B11 DFT_SIZE）
CH_BLOCK = CH_BLOCK          # 信道 h 恒定块 = 100 符号（params ExperimentParams.BLOCK）
N_BLOCKS = 400               # 每点块数（400×256=102400 ≥ 1e5，守 FR-21）
HDFEC = 3.8e-3               # 7% HD-FEC 阈值 BER

# OSNR 扫描（继承 step4a 湍流扫描点）
SNR_TURB = [5.0, 10.0, 15.0, 20.0, 22.0, 24.0, 26.0]

# seed（继承 step4a）
SEED_TURB0 = 2000

# Doppler（继承 common._config，湍流场景用 DOPPLER_HIGH）
DOPPLER = DOPPLER_HIGH


# =============================================================================
# B2-Q2 特有参数（fade 门控，sandbox 实测后填）
# =============================================================================
# γ_th: fade 检测功率阈值。
# 物理依据（阶段 0.4 §3.3 + 阶段 0.5 §1.5）: 实测 rx 功率分布 P(|rx|²)，
#   算 γ̄=mean(P)，σ=std(P)，定扫参范围 [γ̄−3σ, γ̄−1σ]。
# sandbox 第一步（_gamma_th_sweep.py）实测后，从 sweep 结果选最优 γ_th 落到 GAMMA_TH。
# 这里不预设（FR-20/TL-26 禁拍参数）。
GAMMA_TH = None              # 待 sandbox 实测后定
GAMMA_TH_SWEEP_RANGE = None  # 待 sandbox 实测 rx 功率分布后定 [γ̄−3σ, γ̄−1σ]

# ρ_fade: fade 占空比 = P(mean(|rx_block|²) < γ_th)。
# B2-Q2 pilot overhead 摊薄（阶段 0.4 §3.2）: B2Q2_overhead ≈ ρ_fade × 1.249 dB。
# sandbox 逐点（OSNR × 湍流档 × γ_th）实测，不预设。
RHO_FADE = None              # 待 sandbox 实测（dict: {turb: {snr: {gamma_th: rho_fade}}})


# =============================================================================
# 估计器选择（阶段 0.3 前馈化 INVARIANT，4 估计器全前馈闭式）
# =============================================================================
# 方案 A 纯 blind freeze [79]：fft_foe_m0_omega + nda_ml（非 fade）+ freeze hold（fade）
# 方案 B 纯 pilot-aided：da_ml_recovery 全程
# 方案 C B2-Q2 双模切换：非 fade 期 fft_foe_m0_omega + nda_ml / fade 期 da_ml 或 psa_foe
#
# 注: fft_foe（_recovery.py:37）是 QPSK 专用 M=4 升幂，对 16-APSK 不适用。
#     step4a 湍流路径用的是脚本自带 fft_foe_m0_omega（升 M₀=8），sandbox 复用同一实现。
BLIND_ESTIMATOR_NONFADE = 'nda_ml'   # 非 fade 期（step4a 湍流路径同款，两阶段 fft_foe_m0_omega + nda_ml CPE）
PILOT_ESTIMATOR_FADE = 'da_ml'       # fade 期主选（step4a 锚，维度 C2 红线必测）
PILOT_ESTIMATOR_FADE_ALT = 'psa_foe' # fade 期备选（维度 C2 红线必测，B7 baseline）

M0 = 8  # (8,8)-16APSK 升 M₀=8 次幂（step4a 继承）


def print_params_summary():
    """打印参数摘要（sandbox 跑前 sanity check）."""
    print("=" * 80)
    print("B2-Q2 双模切换参数摘要（_b2_params_draft.py）")
    print("=" * 80)
    print(f"[系统] LASER_LW={LASER_LW/1e3:.0f}kHz  R_SYM={R_SYM/1e9:.1f}GBaud  T_S={T_S:.2e}s")
    print(f"       SIGMA2_PN(Wiener)={SIGMA2_PN:.3e}  (2π·LASER_LW·T_S, 派生单值)")
    print(f"[fade] GG α/β 三档（设计选择典型值, params.py audit WARNING）:")
    for lvl in TURB_LEVELS:
        a, b = GG_ALPHA_BETA[lvl]
        print(f"       {lvl:10s}: α={a}, β={b}")
    print(f"[pilot] spacing={DA_PILOT_SPACING}  overhead_full={PILOT_OVERHEAD_DB_FULL:.4f}dB (10·log10(4/3))")
    print(f"[block] N_DFT={N_DFT}  CH_BLOCK={CH_BLOCK}  N_BLOCKS={N_BLOCKS}  N/点={N_BLOCKS*N_DFT}")
    print(f"[snr]   SNR_TURB={SNR_TURB}")
    print(f"[B2-Q2] GAMMA_TH={GAMMA_TH} (待 sandbox 实测)  RHO_FADE={RHO_FADE} (待 sandbox 实测)")
    print(f"[est]   非fade={BLIND_ESTIMATOR_NONFADE}  fade主={PILOT_ESTIMATOR_FADE}  fade备={PILOT_ESTIMATOR_FADE_ALT}")
    print(f"[arch]  前馈化 INVARIANT（4 估计器全前馈闭式 + 开环 γ_th 门控，不撞 D006）")
    print("=" * 80)


if __name__ == '__main__':
    print_params_summary()
