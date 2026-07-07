# -*- coding: utf-8 -*-
"""B11 / 实验参数集中管理 (Formal 正式仿真器, TL-26 溯源).

每个参数标溯源 (B11 论文行号 / params.py / design.md §3). 从 design.md §3 参数表抄,
对齐 MVE (`_time_domain_crlb.py`) 以保证 §4.5 MVE 一致性验证可复现.

溯源说明:
- "B11 行 X" 指 B11 论文 (10.1109_LPT.2024.3523478) 源码行号, 与 MVE `_time_domain_crlb.py`
  注释中的行号引用一致 (MVE 已验证这些 B11 参数).
- params.py 是本仓库参数真相源 (T_S/BLOCK/DOPPLER via SimulationConfig), 此处 re-export.
"""
import os
import sys

import numpy as np

# 从 simulation 根导入 params (TL-13 共用同一参数真相源)
_SIM_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)

from params import SimulationConfig  # noqa: E402

_CFG = SimulationConfig()


# =============================================================================
# 信号 / 调制参数 (design.md §3.1)
# =============================================================================
N_DFT = 256            # B11 行 155 DFT size (= 逐块恢复块大小). MVE _time_domain_crlb.py:118.
M0 = 8                 # (8,8)-16APSK 升 M0=8 次幂 (B11 行 75-77, params B11Params.M0_POWER).
BITS_PER_SYM = 4       # (8,8)-16APSK: 4 bit/symbol.
BLOCK_SIZE_RESOLVE = 256   # resolve_m16apsk_blockwise block_size (守 D003 修复约定).
CH_BLOCK = _CFG.experiment.BLOCK    # 信道 h 估计块大小 (params ExperimentParams.BLOCK=100, h 块内恒定).

# =============================================================================
# 信道参数 (design.md §3.2, B11 行 143/155)
# =============================================================================
CLW_B11 = 500e3        # B11 行 143/155 combined linewidth (AWGN 场景 awgn_wiener_channel 用).
BAUD_B11 = 25e9        # B11 行 143/155 符号率 (不同于 system.R_SYM=2.5e9, B11 场景专用).
T_S_B11 = 1.0 / BAUD_B11   # derived = 1/BAUD_B11 = 40 ps (B11 场景符号周期).
# Wiener PN 每符号方差 σ²_p = 2π·Δν_CLW·T_S (Viterbi 1963 标准激光相位噪声模型,
# B11 行 51, MVE _time_domain_crlb.py:131).
SIGMA2_P_B11 = 2 * np.pi * CLW_B11 * T_S_B11

# 系统 T_S (信道 generate_shared_realization_apsk 用此, params SystemParams).
T_S_GLOBAL = 1.0 / _CFG.system.R_SYM    # = 4e-10 s (=1/2.5e9), 与 common._config T_S 一致

# Doppler / CFO (params DopplerParams, 湍流信道 generate_shared_realization_apsk 注入)
DOPPLER_HIGH = _CFG.doppler.DOPPLER_HIGH    # 150e6 Hz/s (LEO 500km 推导, SPEC §1.3)
F_RESIDUAL = _CFG.doppler.F_RESIDUAL        # 1e6 Hz (FOE 补偿后残余, design.md §3.2)


# =============================================================================
# 评估参数 (design.md §3.4)
# =============================================================================
HDFEC = 3.8e-3         # 7% HD-FEC threshold BER (B11 行 181/191).
DA_PILOT_SPACING = 4   # DA-ML pilot 间距: 每 4 符号 1 pilot = 25% overhead (D-S5-01 + B11).
# pilot overhead 总能量代价 (spacing=4): 10·log10(4/3) = 1.249 dB.
# derived: 相同信息吞吐量下 DA 多发 1/spacing pilot → 总能量代价 10·log10(spacing/(spacing-1)).
PILOT_OVERHEAD_DB = 10.0 * np.log10(DA_PILOT_SPACING / (DA_PILOT_SPACING - 1))


# =============================================================================
# 湍流等级 (design.md §3.3, Gamma-Gamma α/β; SPEC §1.4)
# =============================================================================
# 注: TURB_LEVELS 仅含下行 weak/moderate/strong — consistency_check 遍历此列表与 MVE 对照
# (MVE 只有这三档), 不得加入上行档 (否则 MVE 对照 KeyError). 上行档单独 UPLINK_LEVELS.
TURB_LEVELS = ['weak', 'moderate', 'strong']
# 从 _CFG 取 (params TurbulenceParams, 与 common._config TURB 同源)
TURB_ALPHA_BETA = {
    'weak': (_CFG.turbulence.turb_weak_alpha, _CFG.turbulence.turb_weak_beta),         # (4.0, 3.0)
    'moderate': (_CFG.turbulence.turb_moderate_alpha, _CFG.turbulence.turb_moderate_beta),  # (2.5, 1.8)
    'strong': (_CFG.turbulence.turb_strong_alpha, _CFG.turbulence.turb_strong_beta),   # (1.5, 0.8)
}

# --- 上行(地面→卫星)湍流场景 (sat.1553 Valjus 2025 综述 Table 1) ---
# 设计选择: 参考 sat.1553 上行 Rytov 方差 σ²_R=0.15(上行弱)/0.25(上行强), 远大于下行 0.029.
# 大气湍流主要在低空, 上行信号发射即受扰. 严格 σ²_R→α/β 映射是另一研究方向, 此处务实选
# 两组比现有 strong(α1.5/β0.8)更极端的 α/β 代表对应强度区间. 新增档, 不改 TURB_LEVELS.
# 信道 generate_shared_realization_apsk 经 common.TURB 自动识别 (params.get_turb_dict 已含).
UPLINK_LEVELS = ['uplink_moderate', 'uplink_strong']
UPLINK_ALPHA_BETA = {
    'uplink_moderate': (_CFG.turbulence.turb_uplink_moderate_alpha,   # (1.2, 0.9) ≈ σ²_R 0.15
                        _CFG.turbulence.turb_uplink_moderate_beta),
    'uplink_strong': (_CFG.turbulence.turb_uplink_strong_alpha,       # (1.0, 0.7) ≈ σ²_R 0.25, deep fade
                      _CFG.turbulence.turb_uplink_strong_beta),
}


# =============================================================================
# 实验矩阵 (design.md §5.1, 与 MVE 一致以保证 §4.5 复现)
# =============================================================================
N_BLOCKS = 400                         # 400×256 = 102400 ≥ 1e5 (FR-21, MVE 同).
N_SYM_PER_POINT = N_BLOCKS * N_DFT     # 102400
SNR_AWGN_DB = [5.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0]   # design.md §3.4 / MVE.
SNR_TURB_DB = [5.0, 10.0, 15.0, 20.0, 22.0, 24.0, 26.0]         # 扩至 26dB 覆盖 HD-FEC 交叉点.

# SEED: 必须与 MVE (`sc_nda_ml_mve.py`) 一致以保证 §4.5 一致性验证.
# (任务 brief 写 "seed=42" 是泛指; 实际 MVE 用 SEED_AWGN/SEED_TURB0, 此处守 MVE 种子.)
SEED_AWGN = 20240701      # MVE sc_nda_ml_mve.py:53 (AWGN 场景 base seed).
SEED_TURB0 = 2000         # MVE sc_nda_ml_mve.py:54 (湍流场景 per-block seed base).


def all_traced_params_summary():
    """返回溯源参数摘要 dict (供 results meta 记录, TL-26 审计)."""
    return {
        'N_DFT': (N_DFT, 'B11 行 155'),
        'M0': (M0, 'B11 行 75-77'),
        'BITS_PER_SYM': (BITS_PER_SYM, '(8,8)-16APSK'),
        'CLW_B11': (CLW_B11, 'B11 行 143/155'),
        'BAUD_B11': (BAUD_B11, 'B11 行 143/155'),
        'SIGMA2_P_B11': (SIGMA2_P_B11, 'derived 2π·CLW·T_S (Viterbi 1963, B11 行 51)'),
        'HDFEC': (HDFEC, 'B11 行 181/191'),
        'DA_PILOT_SPACING': (DA_PILOT_SPACING, 'D-S5-01 + B11'),
        'PILOT_OVERHEAD_DB': (PILOT_OVERHEAD_DB, 'derived 10·log10(4/3)'),
        'TURB_ALPHA_BETA': ({k: v for k, v in TURB_ALPHA_BETA.items()}, 'SPEC §1.4'),
        'N_BLOCKS': (N_BLOCKS, 'FR-21 N≥1e5'),
        'SEED_AWGN': (SEED_AWGN, 'MVE sc_nda_ml_mve.py:53'),
        'SEED_TURB0': (SEED_TURB0, 'MVE sc_nda_ml_mve.py:54'),
    }
