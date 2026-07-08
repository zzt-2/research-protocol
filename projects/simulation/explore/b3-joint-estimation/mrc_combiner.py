"""MRC 合并器（①，INVARIANT 14）。

jphot MRC（L101）:
- 共享 LO → 各支路合并后联合补偿（不需每支路独立 DSP）
- 最大比合并: combined = sum_k conj(h_k) * r_k / |h_k|^2（归一化 MRC）
- 合并前各支路需相位预校正（见 multi_branch_phase_precorr.py）

单支路退化: combined = r_0（n_branches=1 时 MRC 退化为恒等）。
"""
import numpy as np


def mrc_combine(branches, h_branches):
    """最大比合并（jphot-L101 共享 LO 合并后联合补偿）。

    Args:
        branches: 各支路复数信号 [r_1, r_2, ..., r_K]（已相位预校正）
        h_branches: 各支路信道增益 [h_1, h_2, ..., h_K]
    Returns:
        combined: MRC 合并后信号
        weights: 各支路合并权重（诊断用）
    数学: combined = sum_k conj(h_k) * r_k / |h_k|^2 （归一化 MRC）
    """
    branches = [np.asarray(b, dtype=complex) for b in branches]
    h_branches = [np.asarray(h, dtype=complex) for h in h_branches]

    K = len(branches)
    N = len(branches[0])

    combined = np.zeros(N, dtype=complex)
    weights = np.zeros(K)

    for k in range(K):
        h_k = h_branches[k]
        # 信道增益（GG 块衰落，取块内代表值；分支逐符号合并需逐符号 h）
        # 此处 h_k 是逐符号的（来自 generate_multi_aperture_realization）
        h_k_sym = h_k[:N] if len(h_k) >= N else np.resize(h_k, N)

        # MRC 权重 = conj(h) / |h|^2 = conj(h) * 1/|h|^2
        h_sq = np.abs(h_k_sym) ** 2
        # 避免除零
        h_sq = np.where(h_sq > 1e-12, h_sq, 1e-12)
        w_k = np.conj(h_k_sym) / h_sq
        combined += w_k * branches[k][:N]
        weights[k] = np.mean(np.abs(h_k_sym) ** 2)  # 诊断：平均信道功率

    # 归一化（MRC 后总功率归一）
    total_power = np.sum(weights)
    if total_power > 0:
        # 归一化合并增益，使合并后 SNR 合理
        # MRC 合并后 signal power ∝ sum |h|^2，归一化使期望 signal power = 1
        norm = np.sqrt(total_power)
        combined = combined / norm if norm > 0 else combined

    return combined, weights


def mrc_combine_single(rx, h):
    """单支路退化接口（n_branches=1，MRC 退化为信道均衡）。

    combined = conj(h) * rx / |h|^2 = rx / sqrt(h)（近似）
    """
    rx = np.asarray(rx, dtype=complex)
    h = np.asarray(h, dtype=complex)
    N = len(rx)
    h_sym = h[:N] if len(h) >= N else np.resize(h, N)
    h_sq = np.abs(h_sym) ** 2
    h_sq = np.where(h_sq > 1e-12, h_sq, 1e-12)
    combined = np.conj(h_sym) * rx / h_sq
    # 归一化
    norm = np.sqrt(np.mean(h_sq))
    return combined / norm if norm > 0 else combined
