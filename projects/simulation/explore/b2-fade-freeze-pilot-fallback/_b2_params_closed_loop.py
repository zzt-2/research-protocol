"""B2-Q2 闭环版参数（阶段 1.5 步骤 2，救援路线 D003）.

真相源（TL-26 参数溯源，每个参数标来源）:
- 激光线宽/符号率: 继承 D-007 SystemParams.LASER_LW=10kHz / R_SYM=2.5GBaud（全场景统一）
- Wiener PN σ²_pN: 2π·LASER_LW·T_S = 2.51e-5（派生量）
- GG α/β: 继承 step4a params.py GammaGammaParams（weak α4/β3, moderate α2.5/β1.8, strong α1.5/β0.8）
- pilot 配置: 继承 step4a DA_PILOT_SPACING=4 / 真符号 pilot / 25% overhead
- fade 阈值 γ_th: 前馈版 sandbox 实测 ρ_fade=0.15 反推（_rho_fade_measure.json）
- DPLL 环路参数: 继承 params.py DPLLParams（omega_n=8e6, zeta=√2/2 Butterworth）
- power_boost_factor: β=2.0（3dB），来源 DVB-S2 pilot boosting + 物理量级核算最优（见 _fair_comparison_closed_loop.md §1.2）

⚠️ [79] Matsuda 全文付费墙不可得（仅摘要），数值参数无法从 [79] 提取。
   [79] 仅作机制定性背书（功率 gate freeze），数值参数用通用经典来源。
"""
import numpy as np
import os, sys

# 从 common 导入（TL-13 共用信道 + params 真相源）
_SIM_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)

from common._config import T_S, LASER_LW, R_SYM, TURB, DOPPLER_HIGH  # 真相源（继承，TL-13）
from params import SimulationConfig  # DPLLParams 来源

# === 继承（不自建，从 common._config / params.py 导入）===
SIGMA2_PN = 2 * np.pi * LASER_LW * T_S   # 2.51e-5（派生，Wiener PN 单值）

# GG α/β（fade 三档，从 common._config.TURB 读，跟 step4a / 前馈版一致）
TURB_LEVELS = ['weak', 'moderate', 'strong']
GG_ALPHA_BETA = {lvl: TURB[lvl] for lvl in TURB_LEVELS}

# === step4a 继承（pilot 配置）===
DA_PILOT_SPACING = 4                      # 继承 step4a
PILOT_OVERHEAD_DB_FULL = 10.0 * np.log10(4 / 3)  # 1.249 dB（全帧，step4a 口径）

# === B2-Q2 闭环版特有（fade 门控 + 闭环 + power-boost）===

# fade 阈值 γ_th（前馈版 sandbox 实测 ρ_fade=0.15 反推，_rho_fade_measure.json）
RHO_FADE = 0.15                           # 前馈版实测，闭环版复用（功率分布不变）

# DPLL 环路参数（继承 params.py DPLLParams，不拍）
_cfg = SimulationConfig()
DPLL_OMEGA_N = _cfg.dpll.omega_n_default  # 8e6 Hz, params.py WARNING assumption
DPLL_ZETA = _cfg.dpll.zeta                # √2/2, params.py derived Butterworth

# power-boost factor（救援版核心新参数）
# 来源: DVB-S2 EN 302 307 pilot power boosting（标准用 2.5dB pilot symbols）+ 物理量级核算最优 β≈2-3
# （见 _fair_comparison_closed_loop.md §1.2 理论预期表：β=2 fade 块内净 +1.07dB, overhead 仅 +0.16dB）
# 强度: assumption + sweep_optimal（sandbox 扫 β ∈ {1, 2, 3} 验证最优）
POWER_BOOST_FACTOR_DEFAULT = 2.0          # 3dB boost（β=2）
POWER_BOOST_SWEEP = [1.0, 2.0, 3.0]       # 扫参（β=1 对照前馈版 / β=2 主选 / β=3 验证边际）

# === 块结构（继承 step4a）===
N_DFT = 256                               # 逐块恢复块大小
CH_BLOCK = 100                            # 信道 h 恒定块
N_BLOCKS = 400                            # 每点块数（400×256=102400 ≥ 1e5）
HDFEC = 3.8e-3                            # 7% HD-FEC 阈值

# === OSNR 扫描（继承 step4a）===
SNR_TURB = [5.0, 10.0, 15.0, 20.0, 22.0, 24.0, 26.0]

# === Doppler（继承 step4a / 前馈版）===
DOPPLER = 1.5e8                           # 150MHz LEO Doppler（_sandbox_results.json meta）

# === 估计器选择（闭环版）===
BLIND_ESTIMATOR_NONFADE = 'blind_dpll'    # 非 fade 期 blind 二阶 DPLL（闭环 tracking loop）
PILOT_ESTIMATOR_FADE = 'pilot_dpll_boost' # fade 期 pilot 二阶 DPLL + power-boost

# === 动态恢复度量修复（n_recover v2，见 _architecture_decision_closed_loop.md §4）===
N_RECOVER_BAND = 0.30                     # 稳态带 ±30%（修前馈版 ±10% 退化）
N_RECOVER_STEADY_WINDOW = 20              # 滑窗均值长度（平滑离散 BER 抖动）
N_RECOVER_CONSECUTIVE = 3                 # 连续 N 块在稳态带算恢复（与前馈版一致）
