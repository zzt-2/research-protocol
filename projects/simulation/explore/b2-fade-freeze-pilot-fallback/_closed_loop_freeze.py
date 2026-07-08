"""B2-Q2 闭环 freeze 实现（阶段 1.5 步骤 2，救援路线 D003 核心）.

[79] 式闭环 hold：block 级闭式相位估计 + 跨块 PI 环路平滑 + 功率阈值 gate + fade hold.

设计（C6 公式核对后修正）:
  - 鉴相器: block 级闭式估计（nda_ml M₀=8 升幂 / da_ml pilot 线性回归），不是逐符号 DPLL
    理由: (8,8)-16APSK 的 DD/升幂鉴相在高 BER 不稳，闭式估计更稳健
  - 闭环价值: 跨块 PI 环路平滑（integrator + vco_phase 状态传递）
  - [79] hold: fade 期冻结环路状态，fade 结束后环路从 hold 状态平滑收敛（有惯性）
  - 前馈版砍掉了跨块平滑 → 每块独立 → 无恢复动力学

V3 祖师爷（_B2-deep-fade-freeze-increment.md:33）:
  [79] 闭环 freeze = 环路滤波器 hold 状态 + 恢复重新收敛.
  本模块: PI 环路 hold (integrator, vco_phase) + 恢复从 hold 状态收敛.

D006 不撞（_architecture_decision_closed_loop.md §2）:
  - 闭式估计估载波相位 φ（nda_ml M₀=8 / da_ml pilot），不估湍流相位 φ_T
  - PI 环路 TF 固定（c1/c2 由 omega_n/zeta 预设），不感知湍流
  - 门控用信号功率 P < γ_th，不用相位

守 INVARIANT 14: explore 私有，不修改 common/_recovery.py.
"""
import numpy as np


class ClosedLoopPhaseTracker:
    """跨块 PI 环路平滑 + fade 期 hold（[79] 式闭环 freeze）.

    工作方式:
      1. 每块由外部闭式估计器给出 (phi_est, omega_est)（nda_ml / da_ml）
      2. 本类用 PI 环路滤波器平滑跨块估计:
         - 误差 e = phi_est - vco_phase
         - integrator += c2 * e
         - vco_phase = c1 * e + integrator + phi_est（一阶跟踪 + 积分抗漂移）
      3. fade 期 hold: 冻结 (integrator, vco_phase)，不更新
      4. fade 结束: 环路从 hold 状态恢复，对新闭式估计平滑收敛

    跨块状态（[79] hold 的核心，前馈版砍掉了）:
        integrator: 积分器状态（频率/相位漂移记忆）
        vco_phase: 当前平滑相位（相位记忆）
    """

    def __init__(self, alpha=0.3, beta=0.05):
        """PI 环路平滑器.

        Parameters
        ----------
        alpha : float
            比例增益（当前块估计的权重，0-1）。大=快跟新块，小=多平滑。
        beta : float
            积分增益（抗漂移）。小=慢积分稳，大=快消偏差但可能振荡。

        参数来源: PI 滤波器经典设计（alpha 控制带宽，beta 控制积分）.
        alpha=0.3 对应约 3 块时间常数（1/0.3≈3），即 fade 后约 3 块收敛到新估计.
        beta=0.05 慢积分消除残余偏差（前馈版无此项 → 每块独立无记忆）.
        """
        self.alpha = alpha
        self.beta = beta
        self.integrator = 0.0
        self.vco_phase = 0.0
        self.has_locked = False

    def update(self, phi_est, omega_est=0.0):
        """用新块闭式估计更新环路状态（非 fade 期调用）.

        Returns 平滑后的相位（用于补偿当前块）.
        """
        # 相位误差（解卷绕）
        e = np.angle(np.exp(1j * (phi_est - self.vco_phase)))
        # PI 环路更新
        self.integrator += self.beta * e
        self.vco_phase = phi_est * self.alpha + self.vco_phase * (1 - self.alpha) + self.integrator
        self.has_locked = True
        return self.vco_phase

    def hold(self):
        """完全 hold（方案 A fade 期）。冻结环路状态，返回 hold 的相位."""
        return self.vco_phase

    def compensate_block(self, rx_block, phi_comp):
        """用给定相位补偿块（hold 或 update 返回的相位）."""
        k = np.arange(len(rx_block))
        # omega 假设 0（块内常相位），纯 phi 补偿
        return rx_block * np.exp(-1j * phi_comp)

    def reset(self):
        """重置环路状态（新测试点）."""
        self.integrator = 0.0
        self.vco_phase = 0.0
        self.has_locked = False


def compute_n_recover_v2(per_block_ber, fade_state, steady_window=20, band=0.30,
                         consecutive=3):
    """动态恢复时间 N_recover v2（修前馈版退化）.

    前馈版退化（_architecture_decision_closed_loop.md §4.1）:
      ±10% 稳态带在高 SNR 太窄 → 命中 fallback → n_recover 与 BER 无关

    v2 修复:
      1. band 从 10% 放宽到 30%（容纳离散 BER 抖动）
      2. 滑窗均值（window=20 块）代替逐块判据
      3. 恢复 = 滑窗均值连续落入稳态带
    """
    n = len(fade_state)
    if n == 0:
        return []
    nonfade_idx = [i for i in range(n) if not fade_state[i] and i >= steady_window]
    if not nonfade_idx:
        return []
    steady_ber = float(np.mean([per_block_ber[i] for i in nonfade_idx]))
    if steady_ber <= 0:
        return []
    threshold_hi = steady_ber * (1 + band)
    threshold_lo = steady_ber * (1 - band)

    transitions = []
    for i in range(1, n):
        if fade_state[i - 1] == 1 and fade_state[i] == 0:
            transitions.append(i)

    n_recover_list = []
    for trans_idx in transitions:
        recover_count = 0
        end_j = n - 1
        for j in range(trans_idx, n):
            if fade_state[j] == 1:
                end_j = j - 1
                break
            win_start = max(trans_idx, j - steady_window + 1)
            win_ber = float(np.mean(per_block_ber[win_start:j + 1]))
            if threshold_lo <= win_ber <= threshold_hi:
                recover_count += 1
                if recover_count >= consecutive:
                    end_j = j
                    break
            else:
                recover_count = 0
            end_j = j
        n_recover = end_j - trans_idx + 1
        n_recover_list.append({
            'fade_end_block': trans_idx,
            'n_recover_blocks': int(n_recover),
            'n_recover_symbols': int(n_recover * 256),
        })
    return n_recover_list
