# -*- coding: utf-8 -*-
"""跨块 KF 消融 (FR-18 反转验证): per-block CPE (复用主实验) + 跨块 KF 平滑.

回答 FR-18 预判核心问题: "加跨块 KF/CPE 跟踪后, DA ML high SNR 是否反超 NDA-ML?"

设计 (§2.1 公平对照 + §2.3 纪律):
  4 配置: NDA / DA / NDA+KF / DA+KF, 2×2 (方法 × 是否 KF).
  KF 对称施加: NDA+KF 和 DA+KF 用 **同一 KF 参数** (Q 矩阵 per 场景, R 用各自 h 估计).
  **不改 sc_nda_ml_sim.py 核心逻辑** (§2.3 纪律 2): 复用 common/ API + 主实验 per-block 逻辑.

两阶段架构 (§2.4 M-APSK KF 适配: "KF 只平滑相位序列不判定调制"):
  Stage 1: per-block CPE (复用主实验 nda_ml_recovery/da_ml_recovery), 得 per-block φ̂_b.
           - NDA: nda_ml_recovery(assume_df_zero=True) → φ_nda[b] ∈ [-π/8,π/8] (有 M₀=8 模糊)
           - DA:  da_ml_recovery → (φ_da[b]=intercept, df_da[b]=slope) (无模糊, pilot 已知)
  Stage 2: 跨块 KF 平滑 φ̂_b 序列 → φ_smoothed[b].
           - 状态 x=[φ, df], F=[[1, T_block],[0,1]], H=[[1,0]] (per-block 时间步 T_block=N_DFT·T_S)
           - 观测 z_b = φ̂_b (per-block CPE 相位); NDA 联合解 M₀ 模糊 (innovation search)
           - 测量噪声 R_b = 1/(2·γ·h_b·N_DFT) (mean-angle 估计方差 ∝ 1/(γhN); deep fade h↓→R↑→KF 信预测=邻居→平滑)
           - 过程噪声 Q_block: sigma2_phi · N_DFT (相位随机游走跨块累积), design_Q 同湍流等级
  再施加: rc_kf[b] = rc_main[b] · exp(-j·Δφ_b), Δφ_b = φ_smoothed[b] − φ̂_b (常相位微调, 保 DA 块内 freq ramp).
  resolve + demod + BER (NDA 用 resolve_m16apsk_blockwise 解 M₀ 模糊; DA 直接 demod data 位置).

公平性 (§2.3 纪律 1):
  - NDA+KF 和 DA+KF 同 Q (per 场景), 同 KF 结构 (2 状态), 同 R 公式 (R_b=1/(2γh_b·N_DFT), h_b 用各法自己估计).
  - 不给某方法调优 KF. KF 是"对称施加的跨块平滑层".

反转判定 (§2.1):
  gain_no_kf = 主实验 fair gain @ HD-FEC (NDA vs DA, 从 _main_experiment_5seed.json 读基准)
  gain_kf    = 消融 fair gain @ HD-FEC (NDA+KF vs DA+KF)
  delta = gain_kf − gain_no_kf (负 = KF 让 NDA 优势缩小 = 反转风险信号)
  high-SNR (≥16dB) 逐点查 DA+KF 是否反超 NDA+KF.

种子 (§2.3 纪律 3): 5 seed, 第 0 seed = MVE seed (SEED_AWGN/SEED_TURB0).
  AWGN: seed_base_i = SEED_AWGN + i
  湍流: seed0_i = SEED_TURB0 + i·N_BLOCKS (5 seed 块范围互斥)

运行: cd projects/simulation && python simulator/run_kf_ablation.py
"""
import os
import sys
import json
import time

import numpy as np

# --- 路径: simulation 根 ---
_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..'))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

# 核心算法全从 common/ 导入 (守 TL-13, 不准 import explore/, 不改 sc_nda_ml_sim.py 核心)
from common import (  # noqa: E402
    generate_shared_realization_apsk,
    m16apsk_mod, m16apsk_demod,
    resolve_m16apsk_blockwise,
    da_ml_recovery, nda_ml_recovery,
    mmse_equalize, amp_limit,
)
import _b11_params as P  # noqa: E402
from fair_comparison import analyze_fair_gain  # noqa: E402
from params import SimulationConfig  # noqa: E402
from scipy import stats  # noqa: E402

# 复用主实验的信道/估计辅助 (这些是 sc_nda_ml_sim.py 的公开 API 函数, 非核心改写)
import sc_nda_ml_sim as S  # noqa: E402
# KF Q 矩阵设计 (common/_kf.py 公开 API)
from common import design_Q as _kf_design_Q  # noqa: E402

# --- 输出目录 ---
OUT_DIR = os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_ablation')
os.makedirs(OUT_DIR, exist_ok=True)

N_SEEDS = 5
T05_4 = float(stats.t.ppf(0.975, 4))   # 2.7764
SCENES = ['awgn', 'weak', 'moderate', 'strong']
TURB_LEVELS = ['weak', 'moderate', 'strong']

# 跨块时间步: 一个 per-block CPE 块 (N_DFT=256 符号) 的持续时间.
# AWGN 用 B11 T_S_B11 (40ps), 湍流用 system T_S_GLOBAL (400ps) — 与各自信道生成一致.
T_BLOCK_AWGN = P.N_DFT * P.T_S_B11
T_BLOCK_TURB = P.N_DFT * P.T_S_GLOBAL


# =============================================================================
# 种子 (与主实验完全一致, §2.3 纪律 3)
# =============================================================================
def seed_base_awgn(i):
    return P.SEED_AWGN + i


def seed0_turb(i):
    return P.SEED_TURB0 + i * P.N_BLOCKS


def ci_t(data):
    a = np.asarray(data, dtype=float)
    n = len(a)
    mean = float(np.mean(a))
    std = float(np.std(a, ddof=1)) if n > 1 else 0.0
    if n > 1:
        hw = float(stats.t.ppf(0.975, n - 1)) * std / np.sqrt(n)
    else:
        hw = 0.0
    return mean, std, hw, mean - hw, mean + hw


# =============================================================================
# 跨块 KF 平滑 (核心: per-block 相位序列 → 跨块 KF, "只平滑相位不判定调制" §2.4)
# =============================================================================
def cross_block_kf(phi_obs, h_per_block, gamma_lin, Q_block, T_block,
                   has_ambiguity=False, M0=8):
    """跨块 KF 平滑 per-block 相位估计序列.

    状态 x=[φ, df], F=[[1, T_block],[0,1]], H=[[1,0]]. per-block 时间步.
    观测 z_b = phi_obs[b] (per-block CPE 相位).
    - has_ambiguity=True (NDA): 联合解 M₀-fold 模糊 (innovation 搜索选 m 使 |wrap(innov)| 最小).
    - has_ambiguity=False (DA): 直接用 phi_obs (pilot 已知, 无模糊).

    测量噪声 R_b = 1/(2·γ·h_b·N_DFT): mean-angle 估计方差 ∝ 1/(γhN).
    deep fade (h_b↓) → R↑ → KF 信时间预测 (邻居块) → 跨块平滑 (FR-18 机制).

    过程噪声 Q_block: 相位随机游走跨 N_DFT 符号累积 (sigma2_phi·N_DFT) + df 漂移.

    返回 (phi_smoothed, phi_resolved_used).
    """
    n_blk = len(phi_obs)
    F = np.array([[1.0, T_block], [0.0, 1.0]])
    H = np.array([[1.0, 0.0]])
    # 初始化: 用第一块观测 (NDA 取 principal value)
    x = np.array([float(phi_obs[0]), 0.0])
    P_cov = np.diag([1.0, 1.0])  # 较大初始不确定 (KF 会收敛)
    phi_smoothed = np.zeros(n_blk)
    phi_resolved = np.zeros(n_blk)
    for b in range(n_blk):
        if b == 0:
            x_pred = x.copy()
            P_pred = P_cov.copy()
        else:
            x_pred = F @ x
            P_pred = F @ P_cov @ F.T + Q_block
        # 测量噪声: per-block h 估计, deep fade → 大 R → 信预测
        h_b = max(float(h_per_block[b]), 1e-6)
        R = 1.0 / (2.0 * gamma_lin * h_b * P.N_DFT)
        if has_ambiguity:
            # 联合解 M₀-fold 模糊: 选 m 使 phi_obs[b]+2πm/M₀ 最接近 KF 预测
            best_innov = 1e18
            best_phi = float(phi_obs[b])
            for m in range(M0):
                phi_cand = float(phi_obs[b]) + 2.0 * np.pi * m / M0
                innov = phi_cand - x_pred[0]
                innov = (innov + np.pi) % (2.0 * np.pi) - np.pi
                if abs(innov) < best_innov:
                    best_innov = abs(innov)
                    best_phi = phi_cand
            z = best_phi
        else:
            z = float(phi_obs[b])
        phi_resolved[b] = z
        innov = z - x_pred[0]
        innov = (innov + np.pi) % (2.0 * np.pi) - np.pi
        S = float((H @ P_pred @ H.T)[0, 0] + R)
        K = (P_pred @ H.T.flatten() / S)
        x = x_pred + K * innov
        x[0] = (x[0] + np.pi) % (2.0 * np.pi) - np.pi
        P_cov = (np.eye(2) - np.outer(K, H[0])) @ P_pred
        phi_smoothed[b] = x[0]
    return phi_smoothed, phi_resolved


def make_Q_block(turb_name_or_awgn):
    """构造跨块 KF 过程噪声 Q_block (per-block 时间步).

    AWGN: sigma2_phi = SIGMA2_P_B11 (B11 线宽 500kHz, 匹配实际 AWGN 信道 PN), 无 turbulence/df.
    湍流: design_Q(turb_name, DOPPLER_HIGH) 给 per-symbol Q, 跨块 ×N_DFT.
    """
    if turb_name_or_awgn == 'awgn':
        # AWGN 信道只有 Wiener PN (SIGMA2_P_B11), 无 turbulence, 无 Doppler (df=0).
        # df 漂移给极小值 (AWGN 真 df=0, 但留小窗让 KF 不僵化).
        sigma2_phi_block = P.SIGMA2_P_B11 * P.N_DFT
        sigma2_df_block = (10e3 * T_BLOCK_AWGN) ** 2 * 0.1  # 极小 df 漂移
        return np.diag([sigma2_phi_block, sigma2_df_block])
    # 湍流: 用 common/_kf.py design_Q (同湍流等级 + 同 f_dot, §2.3 纪律 1)
    Q_per_sym = _kf_design_Q(turb_name_or_awgn, P.DOPPLER_HIGH)
    # per-symbol → per-block: 相位随机游走方差 ×N_DFT; df 漂移 ×N_DFT
    Q_block = np.diag([Q_per_sym[0, 0] * P.N_DFT, Q_per_sym[1, 1] * P.N_DFT])
    return Q_block


# =============================================================================
# AWGN: per-block CPE + (可选) 跨块 KF, 一个 seed 一 SNR 点.
# 复用主实验 awgn_wiener_channel + ber_nda_awgn/ber_da_awgn 的 per-block 内部逻辑,
# 但额外捕获 per-block φ_est + rc_comp 以施加 KF.
# =============================================================================
def run_awgn_point_kf(snr_db, seed_base):
    """AWGN 单 SNR 点, 单 seed_base. 返回 4 配置 BER + per-block 信息 (供 KF).

    复用主实验 seed 派生 (per-SNR seed = seed_base + int(snr*1000), bits seed = seed+7).
    """
    N_sym = P.N_BLOCKS * P.N_DFT
    seed = seed_base + int(snr_db * 1000)
    rng = np.random.default_rng(seed + 7)
    bits = rng.integers(0, 2, N_sym * P.BITS_PER_SYM)
    tx = m16apsk_mod(bits)
    rx, phi_true = S.awgn_wiener_channel(tx, snr_db, seed)

    n_blk = P.N_BLOCKS
    L = n_blk * P.N_DFT
    tb = bits[:L * P.BITS_PER_SYM]

    # --- NDA per-block CPE (复用主实验 ber_nda_awgn 内部逻辑) ---
    rc_nda = np.zeros(L, dtype=complex)
    phi_nda_blk = np.zeros(n_blk)
    for b in range(n_blk):
        seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
        rc, _, phi_est, _ = nda_ml_recovery(seg, P.M0, mod='m16apsk', assume_df_zero=True)
        rc_nda[b * P.N_DFT:(b + 1) * P.N_DFT] = rc
        phi_nda_blk[b] = phi_est
    # no-KF BER (resolve M₀ 模糊 per-block, 与主实验一致)
    resolved_nda = resolve_m16apsk_blockwise(rc_nda, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    ne_nda_nokf = int(np.sum(tb != m16apsk_demod(resolved_nda)))
    nb_nda = len(tb)

    # --- DA per-block CPE (复用主实验 ber_da_awgn 内部逻辑) ---
    tx_sym = m16apsk_mod(tb)
    pilot_idx_local = np.arange(0, P.N_DFT, P.DA_PILOT_SPACING)
    is_data = np.ones(P.N_DFT, dtype=bool)
    is_data[pilot_idx_local] = False
    rc_da = np.zeros(L, dtype=complex)
    phi_da_blk = np.zeros(n_blk)
    for b in range(n_blk):
        s_blk = slice(b * P.N_DFT, (b + 1) * P.N_DFT)
        p_sym = tx_sym[b * P.N_DFT + pilot_idx_local]
        rc, phi_est, _ = da_ml_recovery(rx[s_blk], pilot_idx=pilot_idx_local,
                                        pilot_sym=p_sym, mod='m16apsk')
        rc_da[s_blk] = rc
        phi_da_blk[b] = phi_est
    # no-KF BER (data 位置)
    demod_da = m16apsk_demod(rc_da)
    tb_arr = tb.reshape(L, P.BITS_PER_SYM)
    dm_arr = demod_da.reshape(L, P.BITS_PER_SYM)
    is_data_sym = np.zeros(L, dtype=bool)
    for b in range(n_blk):
        is_data_sym[b * P.N_DFT:(b + 1) * P.N_DFT] = is_data
    ne_da_nokf = int(np.sum(tb_arr[is_data_sym] != dm_arr[is_data_sym]))
    nb_da = int(np.sum(is_data_sym) * P.BITS_PER_SYM)

    # --- AWGN h≡1 (无 fading), KF R 用 h=1 ---
    h_blk = np.ones(n_blk)
    gamma_lin = 10.0 ** (snr_db / 10.0)
    Q_block = make_Q_block('awgn')

    # --- NDA+KF: 跨块 KF 平滑 φ_nda 序列 (联合解 M₀ 模糊) ---
    phi_smoothed_nda, phi_resolved_nda = cross_block_kf(
        phi_nda_blk, h_blk, gamma_lin, Q_block, T_BLOCK_AWGN,
        has_ambiguity=True, M0=P.M0)
    delta_nda = phi_smoothed_nda - phi_resolved_nda  # KF 常相位微调
    rc_nda_kf = rc_nda * np.exp(-1j * np.repeat(delta_nda, P.N_DFT))
    resolved_nda_kf = resolve_m16apsk_blockwise(rc_nda_kf, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    ne_nda_kf = int(np.sum(tb != m16apsk_demod(resolved_nda_kf)))

    # --- DA+KF: 跨块 KF 平滑 φ_da 序列 (无模糊) ---
    phi_smoothed_da, phi_resolved_da = cross_block_kf(
        phi_da_blk, h_blk, gamma_lin, Q_block, T_BLOCK_AWGN,
        has_ambiguity=False, M0=P.M0)
    delta_da = phi_smoothed_da - phi_resolved_da
    rc_da_kf = rc_da * np.exp(-1j * np.repeat(delta_da, P.N_DFT))
    demod_da_kf = m16apsk_demod(rc_da_kf)
    dm_arr_kf = demod_da_kf.reshape(L, P.BITS_PER_SYM)
    ne_da_kf = int(np.sum(tb_arr[is_data_sym] != dm_arr_kf[is_data_sym]))

    return {
        'snr_db': float(snr_db),
        'nda_ber_nokf': ne_nda_nokf / nb_nda,
        'da_ber_nokf': ne_da_nokf / nb_da,
        'nda_ber_kf': ne_nda_kf / nb_nda,
        'da_ber_kf': ne_da_kf / nb_da,
    }


# =============================================================================
# 湍流: per-block CPE + (可选) 跨块 KF, 一个 seed 一 SNR 点.
# 复用主实验 run_turb 内部逻辑 (per-block h 估计 + 两阶段 FOE), 额外捕获 per-block φ_est.
# =============================================================================
def run_turb_point_kf(turb_name, gamma_db, seed0):
    """湍流单 γ 点, 单 seed0. 返回 4 配置 BER. 复用主实验 per-block 结构."""
    cfg = SimulationConfig()
    Ns = P.N_DFT
    gamma_lin = 10 ** (gamma_db / 10)
    ne_nda_nokf = ne_da_nokf = 0
    ne_nda_kf = ne_da_kf = 0
    nb_nda = nb_da = 0

    # 收集所有块的 per-block φ_est + h_est (供跨块 KF; 注意跨块 KF 需要块序列连续)
    phi_nda_blk_all = []
    phi_da_blk_all = []
    h_blind_blk_all = []
    h_pilot_blk_all = []
    # 同时保存每块的 rc_comp + tx_bits 切片, 供 KF 后再施加 + resolve
    rc_nda_blk_all = []
    rc_da_blk_all = []
    tb_blk_all = []

    n_blocks = P.N_BLOCKS
    for b in range(n_blocks):
        r = generate_shared_realization_apsk(
            Ns, gamma_lin, turb_name, cfg.doppler.DOPPLER_HIGH,
            mod='m16apsk', seed=seed0 + b)
        rx_raw = r['rx_raw']
        bits = r['bits']
        phi = r['phi']
        tx_sym = r['tx']
        h_true = r['h']
        # 幅度处理 (修复 D2): per-block h — 三方案各自估计
        h_blind = S.estimate_h_blind_perblock(rx_raw, gamma_lin)
        rx_blind = amp_limit(mmse_equalize(rx_raw, h_blind, gamma_lin), 3.0)
        h_pilot = S.estimate_h_pilot_perblock(rx_raw, tx_sym, gamma_lin)
        rx_pilot = amp_limit(mmse_equalize(rx_raw, h_pilot, gamma_lin), 3.0)

        # --- NDA per-block CPE (复用主实验 ber_nda_turb 两阶段逻辑) ---
        omega_est = S.fft_foe_m0_omega(rx_blind, P.M0)
        k = np.arange(Ns)
        seg_foe = rx_blind * np.exp(-1j * omega_est * k)
        rc_nda_b, _, phi_nda_b, _ = nda_ml_recovery(seg_foe, P.M0, mod='m16apsk', assume_df_zero=True)
        # --- DA per-block CPE (复用主实验 ber_da_turb/ber_da_awgn 逻辑) ---
        pilot_idx_local = np.arange(0, Ns, P.DA_PILOT_SPACING)
        p_sym = tx_sym[pilot_idx_local]
        rc_da_b, phi_da_b, _ = da_ml_recovery(rx_pilot, pilot_idx=pilot_idx_local,
                                              pilot_sym=p_sym, mod='m16apsk')

        # per-block 代表 h (块中心值, 供 KF R)
        h_blind_blk_all.append(float(np.mean(h_blind)))
        h_pilot_blk_all.append(float(np.mean(h_pilot)))
        phi_nda_blk_all.append(float(phi_nda_b))
        phi_da_blk_all.append(float(phi_da_b))
        rc_nda_blk_all.append(rc_nda_b)
        rc_da_blk_all.append(rc_da_b)
        tb_blk_all.append(bits[:Ns * P.BITS_PER_SYM])

    phi_nda_blk_all = np.array(phi_nda_blk_all)
    phi_da_blk_all = np.array(phi_da_blk_all)
    h_blind_blk_all = np.array(h_blind_blk_all)
    h_pilot_blk_all = np.array(h_pilot_blk_all)
    Q_block = make_Q_block(turb_name)

    # --- 跨块 KF ---
    phi_sm_nda, phi_res_nda = cross_block_kf(
        phi_nda_blk_all, h_blind_blk_all, gamma_lin, Q_block, T_BLOCK_TURB,
        has_ambiguity=True, M0=P.M0)
    phi_sm_da, phi_res_da = cross_block_kf(
        phi_da_blk_all, h_pilot_blk_all, gamma_lin, Q_block, T_BLOCK_TURB,
        has_ambiguity=False, M0=P.M0)
    delta_nda = phi_sm_nda - phi_res_nda
    delta_da = phi_sm_da - phi_res_da

    pilot_idx_local = np.arange(0, Ns, P.DA_PILOT_SPACING)
    is_data = np.ones(Ns, dtype=bool)
    is_data[pilot_idx_local] = False

    for b in range(n_blocks):
        tb = tb_blk_all[b]
        # --- NDA no-KF: resolve M₀ 模糊 per-block ---
        resolved_nda = resolve_m16apsk_blockwise(rc_nda_blk_all[b], tb, block_size=P.BLOCK_SIZE_RESOLVE)
        ne_nda_nokf += int(np.sum(tb != m16apsk_demod(resolved_nda)))
        # --- NDA+KF ---
        rc_nda_kf_b = rc_nda_blk_all[b] * np.exp(-1j * delta_nda[b])
        resolved_nda_kf = resolve_m16apsk_blockwise(rc_nda_kf_b, tb, block_size=P.BLOCK_SIZE_RESOLVE)
        ne_nda_kf += int(np.sum(tb != m16apsk_demod(resolved_nda_kf)))
        nb_nda += len(tb)

        # --- DA no-KF: demod data 位置 ---
        demod_da = m16apsk_demod(rc_da_blk_all[b])
        tb_arr = tb.reshape(Ns, P.BITS_PER_SYM)
        dm_arr = demod_da.reshape(Ns, P.BITS_PER_SYM)
        ne_da_nokf += int(np.sum(tb_arr[is_data] != dm_arr[is_data]))
        # --- DA+KF ---
        rc_da_kf_b = rc_da_blk_all[b] * np.exp(-1j * delta_da[b])
        demod_da_kf = m16apsk_demod(rc_da_kf_b)
        dm_arr_kf = demod_da_kf.reshape(Ns, P.BITS_PER_SYM)
        ne_da_kf += int(np.sum(tb_arr[is_data] != dm_arr_kf[is_data]))
        nb_da += int(np.sum(is_data) * P.BITS_PER_SYM)

    return {
        'snr_db': float(gamma_db),
        'nda_ber_nokf': ne_nda_nokf / nb_nda,
        'da_ber_nokf': ne_da_nokf / nb_da,
        'nda_ber_kf': ne_nda_kf / nb_nda,
        'da_ber_kf': ne_da_kf / nb_da,
    }


# =============================================================================
# 跑全场景全 seed
# =============================================================================
def run_all(scenes_to_run):
    t0 = time.time()
    # raw[scene][seed_i] = list of per-SNR point dict (4 配置 BER)
    raw = {sc: {} for sc in scenes_to_run}
    for i in range(N_SEEDS):
        if 'awgn' in scenes_to_run:
            print(f"\n#### AWGN seed {i} (seed_base={seed_base_awgn(i)}) ####")
            raw['awgn'][i] = [run_awgn_point_kf(snr, seed_base_awgn(i)) for snr in P.SNR_AWGN_DB]
            print(f"   done {len(raw['awgn'][i])} SNR 点")
        for turb in TURB_LEVELS:
            if turb in scenes_to_run:
                print(f"\n#### {turb} seed {i} (seed0={seed0_turb(i)}) ####")
                raw[turb][i] = [run_turb_point_kf(turb, g, seed0_turb(i)) for g in P.SNR_TURB_DB]
                print(f"   done {len(raw[turb][i])} SNR 点")
    elapsed = time.time() - t0
    return raw, elapsed


# =============================================================================
# 聚合 + 反转指标
# =============================================================================
def aggregate(raw, scenes_to_run):
    summary = {}
    for sc in scenes_to_run:
        per_seed = raw[sc]
        snrs = [p['snr_db'] for p in per_seed[0]]
        points = []
        for j, snr in enumerate(snrs):
            entry = {'snr_db': float(snr)}
            for cfg_name in ['nda_ber_nokf', 'da_ber_nokf', 'nda_ber_kf', 'da_ber_kf']:
                vals = [per_seed[i][j][cfg_name] for i in range(N_SEEDS)]
                m, s, hw, lo, hi = ci_t(vals)
                entry[f'{cfg_name}_per_seed'] = [float(x) for x in vals]
                entry[f'{cfg_name}_mean'] = m
                entry[f'{cfg_name}_std'] = s
                entry[f'{cfg_name}_ci95'] = [lo, hi]
            points.append(entry)
        summary[sc] = {'snr_db': snrs, 'points': points}
    return summary


def fair_gain_for_config(summary_points, nda_key, da_key):
    """用 analyze_fair_gain 算 NDA(config) vs DA(config) fair gain @ HD-FEC.
    nda_key/da_key ∈ {'nokf','kf'} (映射到 *_ber_mean)."""
    per_snr = []
    for p in summary_points:
        per_snr.append({
            'snr_db': p['snr_db'],
            'nda_ml_ber': p[f'nda_ber_{nda_key}_mean'],
            'da_ml_ber': p[f'da_ber_{da_key}_mean'],
            'oracle_ber': p[f'nda_ber_{nda_key}_mean'],  # 占位 (fair_gain 不用 oracle 判 gain)
        })
    fg = analyze_fair_gain(per_snr, P.HDFEC, P.PILOT_OVERHEAD_DB)
    return fg


def per_point_high_snr_reversal(summary_points, high_snr_thresh=16.0):
    """逐 high-SNR 点查 KF 引起的排序变化.

    关键修正: AWGN high-SNR 下 DA raw BER 本就低于 NDA (主实验已知, 因无 pilot overhead 时
    DA pilot 估准), 故 "DA BER < NDA BER" 不是 KF 引起的反转. 真正的 FR-18 反转是:
      KF 改变了 NDA vs DA 的排序 (no-KF 时 NDA 赢 / 平, +KF 后 DA 赢) — 用 fair-gain 坐标.
    此处报两层: (a) raw BER 排序 (含 pre-existing), (b) KF 是否改变排序 (reversal_induced_by_kf).

    返回 list of dict.
    """
    out = []
    for p in summary_points:
        if p['snr_db'] < high_snr_thresh:
            continue
        nda_kf = p['nda_ber_kf_mean']
        da_kf = p['da_ber_kf_mean']
        nda_nokf = p['nda_ber_nokf_mean']
        da_nokf = p['da_ber_nokf_mean']
        da_lower_kf = bool(da_kf < nda_kf)
        da_lower_nokf = bool(da_nokf < nda_nokf)
        # KF 是否改变了 raw-BER 排序 (nokf 时 NDA≤DA 但 kf 时 DA<NDA)
        reversal_induced_by_kf = bool((not da_lower_nokf) and da_lower_kf)
        out.append({
            'snr_db': p['snr_db'],
            'nda_kf_mean': nda_kf, 'da_kf_mean': da_kf,
            'da_kf_lower_than_nda_kf': da_lower_kf,  # raw BER (含 pre-existing)
            'ratio_kf': float(da_kf / nda_kf) if nda_kf > 0 else None,
            'nda_nokf_mean': nda_nokf, 'da_nokf_mean': da_nokf,
            'da_nokf_lower_than_nda_nokf': da_lower_nokf,
            'reversal_induced_by_kf': reversal_induced_by_kf,  # KF 引起的排序变化 (真 FR-18 信号)
        })
    return out


def reversal_judgment(summary, scenes_to_run):
    """反转判定 per 场景: gain_no_kf vs gain_kf vs delta + high-SNR 反超."""
    out = {}
    for sc in scenes_to_run:
        pts = summary[sc]['points']
        fg_nokf = fair_gain_for_config(pts, 'nokf', 'nokf')
        fg_kf = fair_gain_for_config(pts, 'kf', 'kf')
        g_nokf = fg_nokf['gain_nda_vs_da_fair_db']
        g_kf = fg_kf['gain_nda_vs_da_fair_db']
        delta = (g_kf - g_nokf) if (g_kf is not None and g_nokf is not None) else None
        hs = per_point_high_snr_reversal(pts)
        any_da_kf_reversal = any(p['reversal_induced_by_kf'] for p in hs)
        any_da_kf_raw_lower = any(p['da_kf_lower_than_nda_kf'] for p in hs)
        out[sc] = {
            'gain_no_kf_db': g_nokf,
            'gain_kf_db': g_kf,
            'gain_delta_db': delta,
            'hdfec_reachable_nokf': fg_nokf['hdfec_reachable'],
            'hdfec_reachable_kf': fg_kf['hdfec_reachable'],
            'high_snr_points': hs,
            'any_kf_induced_reversal_high_snr': any_da_kf_reversal,
            'any_da_kf_raw_ber_lower_high_snr': any_da_kf_raw_lower,
            'fair_gain_no_kf_full': {k: fg_nokf[k] for k in
                                     ['snr_nda_tot_at_hdfec', 'snr_da_tot_at_hdfec',
                                      'gain_nda_vs_da_fair_db', 'fair_gain_high_snr_db',
                                      'fair_gain_mean_db', 'min_nda_ber']},
            'fair_gain_kf_full': {k: fg_kf[k] for k in
                                  ['snr_nda_tot_at_hdfec', 'snr_da_tot_at_hdfec',
                                   'gain_nda_vs_da_fair_db', 'fair_gain_high_snr_db',
                                   'fair_gain_mean_db', 'min_nda_ber']},
        }
    return out


def check_seed0_vs_main(raw, main_json_path, scenes_to_run):
    """§2.3 纪律 1: 第 0 seed NDA/DA (no-KF) BER 必须与主实验一致 (可复现性锚点).
    主实验 summary[scene].points[*].per_seed.nda_ml_ber[0] = seed 0 BER."""
    with open(main_json_path, 'r', encoding='utf-8') as f:
        main = json.load(f)
    report = {'pass': True, 'scenes': {}}
    for sc in scenes_to_run:
        main_pts = main['summary'][sc]['points']
        sc_pass = True
        max_rel = 0.0
        per_pt = []
        for j, mp in enumerate(main_pts):
            ours_nda = raw[sc][0][j]['nda_ber_nokf']
            ours_da = raw[sc][0][j]['da_ber_nokf']
            main_nda = mp['per_seed']['nda_ml_ber'][0]
            main_da = mp['per_seed']['da_ml_ber'][0]
            rel_nda = abs(ours_nda - main_nda) / max(abs(main_nda), 1e-12) if main_nda > 1e-12 else abs(ours_nda - main_nda)
            rel_da = abs(ours_da - main_da) / max(abs(main_da), 1e-12) if main_da > 1e-12 else abs(ours_da - main_da)
            ok = ((rel_nda < 0.05) or (abs(ours_nda - main_nda) < 1e-4)) and \
                 ((rel_da < 0.05) or (abs(ours_da - main_da) < 1e-4))
            max_rel = max(max_rel, rel_nda, rel_da)
            sc_pass = sc_pass and ok
            per_pt.append({'snr_db': mp['snr_db'], 'ok': ok,
                           'nda': [ours_nda, main_nda, rel_nda],
                           'da': [ours_da, main_da, rel_da]})
        report['scenes'][sc] = {'pass': sc_pass, 'max_rel_err': max_rel, 'points': per_pt}
        report['pass'] = report['pass'] and sc_pass
    return report


# =============================================================================
# 画图: BER 曲线 4 配置对比
# =============================================================================
def plot_curves(summary, reversal, scenes_to_run):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, len(scenes_to_run), figsize=(6 * len(scenes_to_run), 5.2),
                             squeeze=False)
    titles = {'awgn': 'AWGN', 'weak': 'weak (α4/β3)',
              'moderate': 'moderate (α2.5/β1.8)', 'strong': 'strong (α1.5/β0.8)'}
    for ax, sc in zip(axes[0], scenes_to_run):
        pts = summary[sc]['points']
        gts = [p['snr_db'] for p in pts]
        nda_nokf = [p['nda_ber_nokf_mean'] for p in pts]
        da_nokf = [p['da_ber_nokf_mean'] for p in pts]
        nda_kf = [p['nda_ber_kf_mean'] for p in pts]
        da_kf = [p['da_ber_kf_mean'] for p in pts]
        ax.semilogy(gts, nda_nokf, 'o-', color='C0', label='NDA-ML (no KF)', lw=1.6)
        ax.semilogy(gts, da_nokf, 's-', color='C1', label='DA ML (no KF)', lw=1.6)
        ax.semilogy(gts, nda_kf, 'o--', color='C0', label='NDA-ML + KF', lw=1.8)
        ax.semilogy(gts, da_kf, 's--', color='C1', label='DA ML + KF', lw=1.8)
        ax.axhline(P.HDFEC, color='k', ls=':', label='HD-FEC 3.8e-3')
        r = reversal[sc]
        g_nokf = r['gain_no_kf_db']
        g_kf = r['gain_kf_db']
        ttl = f"{titles[sc]}\ngain@HDFEC: noKF={g_nokf}, +KF={g_kf}" if (g_nokf is not None and g_kf is not None) else \
              f"{titles[sc]}\ngain noKF={g_nokf}, +KF={g_kf}"
        ax.set_title(ttl, fontsize=9.5)
        ax.set_xlabel(r'$\gamma_{tot}$ (dB)')
        ax.set_ylabel('BER')
        ax.grid(True, which='both', alpha=0.3)
        ax.legend(fontsize=7, loc='best')
        ax.set_ylim(bottom=1e-4)
    fig.suptitle('跨块 KF 消融 (FR-18 反转验证): NDA/DA × {no KF, +KF} (5 seed 均值)',
                 fontsize=12, y=1.01)
    fig.tight_layout()
    png = os.path.join(OUT_DIR, '_kf_ablation_curves.png')
    fig.savefig(png, dpi=120, bbox_inches='tight')
    return png


def to_jsonable(o):
    if isinstance(o, dict):
        return {k: to_jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [to_jsonable(v) for v in o]
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return to_jsonable(o.tolist())
    return o


# =============================================================================
# 主
# =============================================================================
def main():
    t0 = time.time()
    main_json_path = os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_main',
                                  '_main_experiment_5seed.json')

    print("=" * 100)
    print("跨块 KF 消融 (FR-18 反转验证): NDA/DA × {no KF, +KF}, 5 seed × 4 场景")
    print(f"KF 架构: per-block CPE (复用主实验) + 跨块 KF 平滑 (只平滑相位, 不判定调制)")
    print(f"公平: NDA+KF 和 DA+KF 同 Q (per 场景), 同 R 公式 (R=1/(2γh_b·N_DFT), h_b 各法自估)")
    print(f"  AWGN T_block={T_BLOCK_AWGN:.2e}s (B11 T_S); 湍流 T_block={T_BLOCK_TURB:.2e}s (sys T_S)")
    print("=" * 100)

    scenes_to_run = list(SCENES)
    raw, elapsed = run_all(scenes_to_run)

    # --- §2.3 纪律 1: seed 0 no-KF vs 主实验 (可复现性锚点) ---
    print("\n" + "#" * 30 + " seed 0 可复现性 (no-KF vs 主实验) " + "#" * 30)
    repro = check_seed0_vs_main(raw, main_json_path, scenes_to_run)
    for sc in scenes_to_run:
        sr = repro['scenes'][sc]
        print(f"  {sc:>10}: pass={sr['pass']}  max_rel_err={sr['max_rel_err']*100:.4f}%")
    print(f"  总体: {'PASS ✅' if repro['pass'] else 'FAIL ❌'}")

    summary = aggregate(raw, scenes_to_run)
    reversal = reversal_judgment(summary, scenes_to_run)

    png_path = plot_curves(summary, reversal, scenes_to_run)

    # --- 落盘 _kf_ablation_5seed.json ---
    out = {
        'meta': {
            'task': '跨块 KF 消融 (FR-18 反转验证)',
            'metric': 'BER (4 配置) + fair gain @ HD-FEC (no-KF vs +KF) + 反转指标',
            'n_seeds': N_SEEDS,
            'seed_strategy': {
                'awgn': 'seed_base_i = SEED_AWGN + i (per-SNR seed=seed_base+int(snr*1000))',
                'turbulence': 'seed0_i = SEED_TURB0 + i*N_BLOCKS (5 seed 块范围互斥)',
                'note': 'seed 0 = MVE seed (可复现); 与主实验完全一致',
            },
            'scenes': scenes_to_run,
            'configs': ['NDA (no KF)', 'DA (no KF)', 'NDA+KF', 'DA+KF'],
            'kf_architecture': 'per-block CPE (复用主实验 nda_ml/da_ml_recovery) + 跨块 KF 平滑 '
                               '(只平滑 per-block 相位序列, 不判定调制 — §2.4 M-APSK 适配)',
            'kf_state': 'x=[φ, df], F=[[1, T_block],[0,1]], H=[[1,0]] (per-block 时间步)',
            'kf_observation': 'z_b = per-block φ̂_b (NDA 联合解 M0=8 模糊 in innovation; DA 直接用 intercept)',
            'kf_R': 'R_b = 1/(2·γ·h_b·N_DFT), h_b 用各法自估 (NDA blind / DA pilot); '
                    'deep fade h_b↓→R↑→KF 信邻居→平滑 (FR-18 机制)',
            'kf_Q': 'AWGN: sigma2_phi=SIGMA2_P_B11·N_DFT (匹配实际信道 PN), df≈0; '
                    '湍流: design_Q(turb, DOPPLER_HIGH)·N_DFT (同湍流等级同 f_dot)',
            'fairness': 'NDA+KF 和 DA+KF 同 Q 同结构 (§2.3 纪律 1), 不给某方法调优 KF',
            'reapply': 'rc_kf[b] = rc_main[b]·exp(-j·Δφ_b), Δφ_b=φ_smoothed−φ̂_b (常相位微调, 保 DA 块内 freq ramp)',
            'M0_ambiguity_resolve': 'NDA: KF innovation 联合解 M0=8 模糊 + resolve_m16apsk_blockwise (tx_bits, 同主实验); '
                                    'DA: pilot 已知无模糊',
            'sc_simulator_unchanged': True,
            'M_APSK_kf_adaptation': '用"KF 只平滑相位序列不判定调制"方案 (kf_unified 的 hard_decision 不支持 m16apsk, '
                                     '故不用 per-symbol DD-KF, 改用 per-block 相位序列 KF)',
            'M0': P.M0, 'pilot_spacing': P.DA_PILOT_SPACING,
            'pilot_overhead_db': float(P.PILOT_OVERHEAD_DB), 'hdfec': P.HDFEC,
            'N_per_point': P.N_SYM_PER_POINT, 'N_blocks': P.N_BLOCKS,
            'seed_awgn_mve': P.SEED_AWGN, 'seed_turb0_mve': P.SEED_TURB0,
            'python': sys.executable, 'numpy_version': np.__version__,
            'elapsed_sec': float(elapsed),
        },
        'seed0_reproducibility_vs_main': to_jsonable(repro),
        'summary': to_jsonable(summary),
        'reversal_analysis': to_jsonable(reversal),
        'ber_curves_png': png_path,
    }
    out_json = os.path.join(OUT_DIR, '_kf_ablation_5seed.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(out), f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {out_json}")
    print(f"[保存] {png_path}")

    # --- 落盘 _kf_ablation_summary.json (精简反转判定) ---
    fair_summary = {'meta': {
        'task': 'FR-18 反转验证汇总 (跨块 KF 消融)',
        'gain_definition': 'fair_gain@HD-FEC = (DA γ_tot @ HD-FEC) − (NDA γ_tot @ HD-FEC); 正=NDA赢',
        'reversal_criterion': 'gain_delta<0 或 high-SNR DA+KF 反超 NDA+KF → 反转风险信号',
        'note_no_kf_baseline': 'gain_no_kf 取自本消融 seed0 可复现的 no-KF 配置 (与主实验一致), 非外部读入',
    }, 'reversal_per_scene': {}}
    for sc in scenes_to_run:
        r = reversal[sc]
        g_nokf = r['gain_no_kf_db']
        g_kf = r['gain_kf_db']
        delta = r['gain_delta_db']
        kf_induced = r['any_kf_induced_reversal_high_snr']
        raw_lower = r['any_da_kf_raw_ber_lower_high_snr']
        # 反转 flag (主判据 = fair-gain delta; 辅 = KF 引起的 raw-BER 排序变化)
        reversal_flag = (delta is not None and delta < -0.1) or kf_induced
        # 定性 (fair-gain 为主, raw-BER KF-排序变化为辅)
        if delta is None:
            verdict = 'HD-FEC 不可达 (无法算 gain@HD-FEC); high-SNR KF 排序变化: ' + \
                      ('有 (KF 引起 DA 反超)' if kf_induced else '无')
        elif delta < -0.1 and kf_induced:
            verdict = '反转 (fair-gain 显著缩小 + high-SNR KF 引起 DA 反超)'
        elif delta < -0.1:
            verdict = '反转风险 (fair-gain 显著缩小, high-SNR 排序未变)'
        elif kf_induced:
            verdict = '局部反转 (high-SNR KF 引起 raw-BER DA 反超, fair-gain@HD-FEC 未全翻)'
        elif delta < -0.02:
            verdict = '轻微缩小 (KF 让 NDA fair-gain 略减, 未反转)'
        else:
            verdict = '不反转 (KF 后 NDA fair-gain 稳定; AWGN high-SNR DA raw-BER 本就低于 NDA 属 pre-existing 非 KF 引起)'
        fair_summary['reversal_per_scene'][sc] = {
            'gain_no_kf_db': g_nokf, 'gain_kf_db': g_kf, 'gain_delta_db': delta,
            'hdfec_reachable_nokf': r['hdfec_reachable_nokf'],
            'hdfec_reachable_kf': r['hdfec_reachable_kf'],
            'any_kf_induced_reversal_high_snr': kf_induced,
            'any_da_kf_raw_ber_lower_high_snr': raw_lower,
            'reversal_flag': bool(reversal_flag),
            'verdict': verdict,
            'high_snr_reversal_points': r['high_snr_points'],
        }
    fair_json = os.path.join(OUT_DIR, '_kf_ablation_summary.json')
    with open(fair_json, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(fair_summary), f, indent=2, ensure_ascii=False)
    print(f"[保存] {fair_json}")

    # --- 控制台汇总 ---
    print("\n" + "=" * 100)
    print("反转判定 (FR-18): gain_no_kf vs gain_kf vs delta (fair-gain @ HD-FEC, γ_tot 坐标)")
    print(f"{'场景':>10} {'gain_noKF':>12} {'gain_+KF':>12} {'delta':>10} {'KF引起raw反超':>14} {'verdict'}")
    for sc in scenes_to_run:
        r = reversal[sc]
        g_nokf = r['gain_no_kf_db']; g_kf = r['gain_kf_db']; delta = r['gain_delta_db']
        kf_ind = r['any_kf_induced_reversal_high_snr']
        v = fair_summary['reversal_per_scene'][sc]['verdict']
        def fmt(x):
            return f'{x:+.4f}' if isinstance(x, float) else str(x)
        print(f"{sc:>10} {fmt(g_nokf):>12} {fmt(g_kf):>12} {fmt(delta):>10} {str(kf_ind):>14} {v}")
    print(f"\n[总耗时] {elapsed:.1f} s (含 5 seed × {len(scenes_to_run)} 场景 × 4 配置)")


if __name__ == '__main__':
    main()
