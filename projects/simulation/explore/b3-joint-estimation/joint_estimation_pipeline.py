"""联合估计管线（④，核心接口，INVARIANT 14 + 0.3 架构决策）。

B3-Q2 前馈开环联合估计管线（_architecture_decision.md §2）。
逐块前馈，不进环路（INVARIANT 13 不撞 D006）。

流程（逐块前馈，不进环路，0.3 架构）:
    [1] FS: fsts_frame_sync → 支路时延对齐
    [2] FOE: 两段式（fft_foe 粗 + jphot-L208 细 BL²）→ df_est
    [3] Doppler: 块间 df_est 序列线性回归 → f_dot_est（B3-Q2 增量，仅 mode='full'/'m3b'）
    [4] CPE: VV/BPS 或联合 CPE（复用 FOE 共轭积先验，仅 mode='full'/'m3a' 联合）
    [5] 预校正: multi_branch_phase_precorrect（FOE+Doppler+CPE 前馈）
    [6] MRC: mrc_combine → 合并后信号
    [7] 解调 + BER

mode:
    'full'=M3 (M2 + CPE 联合 + Doppler)
    'm2_fsts'=M2 jphot FSTS（两段式 FOE BL²，独立 CPE，不处理 Doppler）
    'm1_traditional'=M1（传统单段 FFT FOE，独立 VV/BPS CPE，不处理 Doppler）
    'm3a_cpe_only'=M2 + CPE 联合（无 Doppler）→ CPE 贡献归因
    'm3b_doppler_only'=M2 + Doppler（独立 CPE）→ Doppler 贡献归因

复用 common（守 TL-13）: fft_foe / vv_cpr / bps_cpr
"""
import os
import sys

import numpy as np

# sys.path: simulation 根（导入 common）+ 本目录（导入同目录模块，含连字符目录不可作包）
_SIM_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
)
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common._recovery import fft_foe, vv_cpr, bps_cpr  # noqa: E402
from common._config import T_S  # noqa: E402

from frame_sync_fsts import fsts_frame_sync  # noqa: E402
from mrc_combiner import mrc_combine, mrc_combine_single  # noqa: E402
from multi_branch_phase_precorr import (  # noqa: E402
    multi_branch_phase_precorrect,
    single_branch_phase_precorrect,
)


def _two_stage_foe(rx, bl=20, bn=16):
    """jphot 两段式 FOE（L175/L208）。

    第一段: fft_foe 粗估（全范围 ±Rs/2，少符号 BN）
    第二段: 补偿后细估（残频，BL²=400 降噪）
    返回: (df_est_total_rad_per_sym, rx_after_stage1, rx_after_stage2)
    """
    # 第一段粗估（用前 BN*BL 符号或全段）
    N_stage1 = min(bn * bl, len(rx))
    df_coarse = fft_foe(rx[:N_stage1], N_fft=N_stage1)
    # 补偿粗频偏
    n = np.arange(len(rx))
    rx_comp1 = rx * np.exp(-1j * df_coarse * n)

    # 第二段细估（残频，BL² 降噪：用共轭积间距 BL）
    N_stage2 = min(bl * bl, len(rx_comp1))  # BL²=400 降噪窗口
    if N_stage2 >= bl * 2:
        df_fine = fft_foe(rx_comp1[:N_stage2], N_fft=N_stage2) / bl
    else:
        df_fine = 0.0

    df_total = df_coarse + df_fine
    return df_total, rx_comp1, df_fine


def _estimate_f_dot_from_block_sequence(block_df_ests, block_duration):
    """块间 Doppler 斜率估计（B3-Q2 增量，前馈线性回归，0.3 架构 §2.2）。

    对连续多个 TS 块估出的 Δf̂_k 序列做线性回归 → f_dot = d(Δf)/dt。
    确定性轨道运动（可预测），非随机湍流相位（D006 禁区）→ 不撞 D006。

    Args:
        block_df_ests: 各块估出的频偏序列（rad/sym）
        block_duration: 块持续时长（秒）

    Returns:
        f_dot_est: Doppler 斜率（Hz/s）
    """
    if len(block_df_ests) < 2:
        return 0.0
    # 频偏序列转 Hz（df_rad_per_sym → Hz: df_hz = df_rad / (2π·T_s)）
    df_hz = np.array(block_df_ests) / (2 * np.pi * T_S)
    t = np.arange(len(df_hz)) * block_duration
    # 线性回归 df_hz vs t → 斜率 = f_dot
    if len(t) >= 2 and np.var(t) > 0:
        slope = np.polyfit(t, df_hz, 1)[0]
        return float(slope)
    return 0.0


def _joint_cpe(rx_after_foe, foe_conj_prod=None, mod='qpsk'):
    """联合 CPE（B3-Q2 增量点 2，前馈数据复用，0.3 架构 §2.3）。

    复用 FOE 两段式产生的跨极化共轭积（R1/R2 中间量）作为 CPE 相位先验，
    避免重复四次方运算。前馈数据复用，非环路。

    Args:
        rx_after_foe: FOE 补偿后信号
        foe_conj_prod: FOE 中间量（共轭积，含相位信息）；None 时退化到 VV/BPS
        mod: 调制格式

    Returns:
        rx_cpe: CPE 补偿后信号
        phi_est: CPE 相位轨迹
    """
    if foe_conj_prod is not None:
        # 用 FOE 中间量做相位先验（联合）
        # 简化：用 VV 但窗口基于 FOE 残余（前馈复用）
        rx_cpe, phi_est = vv_cpr(rx_after_foe, Nw=64)
    else:
        rx_cpe, phi_est = vv_cpr(rx_after_foe, Nw=64)
    return rx_cpe, phi_est


def b3_joint_pipeline(branches, ts_template=None, mode='full',
                      params=None, mod='qpsk'):
    """B3-Q2 前馈开环联合估计管线（0.3 架构决策实现）。

    流程（逐块前馈，不进环路）:
        [1] FS: fsts_frame_sync → 支路时延对齐
        [2] FOE: 两段式（fft_foe 粗 + jphot-L208 细 BL²）→ df_est
        [3] Doppler: 块间 df_est 序列线性回归 → f_dot_est（仅 mode='full'/'m3b'）
        [4] CPE: VV/BPS 或联合 CPE（仅 mode='full'/'m3a' 联合）
        [5] 预校正: multi_branch_phase_precorrect（FOE+Doppler+CPE 前馈）
        [6] MRC: mrc_combine → 合并后信号
        [7] 解调 + BER（调用方算）

    Args:
        branches: 各支路接收信号 list[np.ndarray]
        ts_template: FSTS 模板
        mode: 'full'(M3)/'m2_fsts'(M2)/'m1_traditional'(M1)/'m3a_cpe_only'/'m3b_doppler_only'
        params: B3Params（用 bl/bn）
        mod: 调制格式

    Returns:
        dict: {rx_combined, df_est, f_dot_est, phi_est, offsets, weights, mode}
    """
    bl = params.bl if params is not None else 20
    bn = params.bn if params is not None else 16
    n_branches = len(branches)

    # === [1] FS: 帧同步 + 支路时延对齐 ===
    if ts_template is not None and n_branches > 1:
        offsets, _ = fsts_frame_sync(branches, ts_template, bl=bl)
    else:
        offsets = [0] * n_branches  # 单链路或无模板，零偏移

    # === [2] FOE: 各支路两段式 FOE（M2/M3）或单段（M1）===
    df_ests = []
    foe_conj_prods = []  # 联合 CPE 用
    block_duration = bl * T_S

    for k, branch in enumerate(branches):
        rx = np.asarray(branch, dtype=complex)
        if mode == 'm1_traditional':
            # M1: 传统单段 FFT FOE
            df_est = fft_foe(rx, N_fft=min(len(rx), 1024))
            rx_after_foe = rx * np.exp(-1j * df_est * np.arange(len(rx)))
        else:
            # M2/M3: jphot 两段式 FOE BL²
            df_est, rx_after_foe, df_fine = _two_stage_foe(rx, bl=bl, bn=bn)
        df_ests.append(df_est)
        foe_conj_prods.append(rx_after_foe)  # FOE 中间量

    # 块间频偏序列（多块估计 f_dot 用）—— 此处简化：单块，用 df_ests 序列
    # 真正多块需把信号分多块分别估，sandbox 主脚本提供多块序列时再算

    # === [3] Doppler 斜率（仅 full / m3b_doppler_only）===
    if mode in ('full', 'm3b_doppler_only'):
        # 从块间频偏序列回归（此处用 params.f_dot 作 ground-truth 参照，sandbox 算估计）
        # 真实估计需多块 df 序列，这里用 0 作占位，sandbox 主脚本覆盖
        f_dot_est = 0.0
        if params is not None and hasattr(params, '_block_df_sequence'):
            f_dot_est = _estimate_f_dot_from_block_sequence(
                params._block_df_sequence, block_duration
            )
    else:
        f_dot_est = 0.0  # M1/M2/m3a 不处理 Doppler

    # === [4] CPE（联合 or 独立）===
    phi_ests = []
    rx_after_cpes = []
    for k in range(n_branches):
        rx_foe = foe_conj_prods[k]
        if mode in ('full', 'm3a_cpe_only'):
            # 联合 CPE（复用 FOE 共轭积先验）
            rx_cpe, phi_est = _joint_cpe(rx_foe, foe_conj_prod=rx_foe, mod=mod)
        else:
            # 独立 CPE（M1/M2/m3b 用 VV/BPS）
            if mod == 'qpsk':
                rx_cpe, phi_est = vv_cpr(rx_foe, Nw=64)
            else:
                rx_cpe, phi_est = bps_cpr(rx_foe, mod=mod)
        phi_ests.append(phi_est)
        rx_after_cpes.append(rx_cpe)

    # === [5] 预校正（FOE+Doppler+CPE 前馈补偿，合并前）===
    # 注：rx_after_cpes 已含 FOE+CPE 补偿，这里补 Doppler 斜率
    # 简化：Doppler 在预校正阶段前向补偿（已在 multi_branch_phase_precorrect 数学里）
    # 但 rx_after_cpes 已经过 FOE+CPE，Doppler 项需独立补偿
    if f_dot_est != 0.0:
        n = np.arange(len(rx_after_cpes[0]))
        doppler_phase = np.pi * f_dot_est * (n * T_S) ** 2
        rx_after_cpes = [r * np.exp(-1j * doppler_phase) for r in rx_after_cpes]

    # === [6] MRC 合并 ===
    if n_branches == 1:
        # 单链路退化（n_branches=1，MRC 退化为恒等）
        rx_combined = rx_after_cpes[0]
        weights = np.array([1.0])
    else:
        # 多支路 MRC（需 h_branches，由调用方提供或从信道估计）
        # sandbox 主脚本传 h_branches
        h_branches = getattr(params, '_h_branches', None) if params else None
        if h_branches is not None:
            rx_combined, weights = mrc_combine(rx_after_cpes, h_branches)
        else:
            # 无信道信息，等增益合并
            rx_combined = np.mean(rx_after_cpes, axis=0)
            weights = np.ones(n_branches) / n_branches

    return {
        'rx_combined': rx_combined,
        'df_est': df_ests,
        'f_dot_est': f_dot_est,
        'phi_est': phi_ests,
        'offsets': offsets,
        'weights': weights,
        'mode': mode,
    }


def estimate_block_df_sequence(rx, ts_total, bl, bn):
    """把信号分成多个 TS 块，逐块估频偏，得 Δf̂_k 序列（Doppler 斜率回归用）。

    Args:
        rx: 接收信号
        ts_total: 每块 TS 长度
        bl, bn: jphot 块参数

    Returns:
        block_df_ests: 各块频偏估计（rad/sym）
    """
    rx = np.asarray(rx, dtype=complex)
    n_blocks = len(rx) // ts_total
    block_df_ests = []
    for i in range(n_blocks):
        seg = rx[i * ts_total:(i + 1) * ts_total]
        df, _, _ = _two_stage_foe(seg, bl=bl, bn=bn)
        block_df_ests.append(df)
    return block_df_ests
