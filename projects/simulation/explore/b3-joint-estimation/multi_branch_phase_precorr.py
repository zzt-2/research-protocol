"""多支路相位预校正（③，INVARIANT 14）。

各支路相位预校正（FOE + Doppler 斜率 + CPE 前馈补偿，合并前）。
jphot-L243: "diversity branch phase correction" 在 MRC 之前。

数学（§0.6.2 接口定义）:
    r_k_precorr = r_k * exp(-j*(2π·df·(n-offset_k)·Ts + π·f_dot·(n·Ts)^2 + phi_est[n]))

前馈开环（INVARIANT 13）: 用估计值前向补偿，不进环路。
"""
import os
import sys

import numpy as np

_SIM_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
)
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)

from common._config import T_S  # noqa: E402


def multi_branch_phase_precorrect(branches, offsets, df_est, f_dot_est,
                                  phi_est, ts=None):
    """各支路相位预校正（FOE + Doppler 斜率 + CPE 前馈补偿，合并前）。

    Args:
        branches: 各支路信号（FS 对齐后）
        offsets: 各支路时延偏移（来自 fsts_frame_sync）
        df_est: 块内频偏（两段式 FOE 输出，jphot-L175）
        f_dot_est: 块间 Doppler 斜率（B3-Q2 增量，前馈回归）
        phi_est: CPE 相位轨迹（VV/BPS 或联合 CPE 输出）
        ts: 符号周期 T_S（默认从 common 读）

    Returns:
        precorrected: 各支路预校正后信号（待 MRC 合并）
    数学: r_k_precorr = r_k * exp(-j*(2π·df·(n-offset_k)·Ts + π·f_dot·(n·Ts)^2 + phi_est[n]))
    """
    if ts is None:
        ts = T_S

    branches = [np.asarray(b, dtype=complex) for b in branches]
    phi_est = np.asarray(phi_est, dtype=float)

    precorrected = []
    for k, (branch, offset_k) in enumerate(zip(branches, offsets)):
        N = len(branch)
        n = np.arange(N)
        # FOE 线性相位（块内频偏）+ Doppler 二次相位（斜率）+ CPE 相位
        phase_foe = 2 * np.pi * df_est * (n - offset_k) * ts
        phase_dot = np.pi * f_dot_est * (n * ts) ** 2
        phase_cpe = phi_est[:N] if len(phi_est) >= N else np.resize(phi_est, N)

        total_phase = phase_foe + phase_dot + phase_cpe
        precorr = branch * np.exp(-1j * total_phase)
        precorrected.append(precorr)

    return precorrected


def single_branch_phase_precorrect(rx, df_est, f_dot_est, phi_est, ts=None):
    """单支路相位预校正（n_branches=1 退化接口）。"""
    if ts is None:
        ts = T_S
    rx = np.asarray(rx, dtype=complex)
    phi_est = np.asarray(phi_est, dtype=float)
    N = len(rx)
    n = np.arange(N)
    phase_foe = 2 * np.pi * df_est * n * ts
    phase_dot = np.pi * f_dot_est * (n * ts) ** 2
    phase_cpe = phi_est[:N] if len(phi_est) >= N else np.resize(phi_est, N)
    total_phase = phase_foe + phase_dot + phase_cpe
    return rx * np.exp(-1j * total_phase)
