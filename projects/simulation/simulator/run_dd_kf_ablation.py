# -*- coding: utf-8 -*-
"""per-symbol DD-KF 消融 (FR-18 反转验证, 强 KF): per-block CPE 初始化 + per-symbol decision-directed Kalman.

回答用户最担心的问题 (§2.1): common/_kf.py:kf_unified 是更强的 **per-symbol DD-KF**
(每符号 hard_decision 决策反馈), 比 run_kf_ablation.py 的 per-block 相位序列 KF 更激进.
用户担心: 更强的 per-symbol DD-KF 会不会让 DA ML 在 high SNR 反超 NDA-ML?

本消融测这个口子 (per-block KF 消融 delta ∈ ±0.002 dB 不反转, 但更强的 per-symbol DD-KF 没测过).

设计 (§2.1 公平对照 + §2.3 纪律):
  4 配置: NDA / DA / NDA+DD-KF / DA+DD-KF, 2×2 (方法 × 是否 per-symbol DD-KF).
  DD-KF 对称施加: NDA+DD-KF 和 DA+DD-KF 用 **同一 DD-KF 参数** (Q per 场景, R 公式同).
  **不改 common/_kf.py 核心** (§2.3 纪律 2, 守 TL-13): m16apsk 判决在脚本内 (选项 A).

两阶段架构 (§2.1 DD-KF 接入方式):
  Stage 1: per-block CPE 初始化 (复用主实验 nda_ml_recovery/da_ml_recovery), 得每块初始相位 φ̂_block.
           - NDA: nda_ml_recovery(assume_df_zero=True) → φ_nda[b] ∈ [-π/8,π/8] (有 M₀=8 模糊)
           - DA:  da_ml_recovery → (φ_da[b]=intercept, df_da[b]=slope) (无模糊, pilot 已知)
  Stage 2: per-symbol DD-KF 跟踪 (块内 256 符号, 复制 kf_unified 逻辑改 m16apsk 判决).
           - 状态 x=[φ, df], F=[[1, T_S_sym],[0,1]] (per-symbol 时间步, T_S_sym 同信道)
           - 观测 z_k = angle(rx[k] · conj(s_hat)), s_hat = hard_decision_m16apsk(rx[k]·exp(-j·x_pred[0]))
           - 测量噪声 R = 1/(2·γ_bar·h_b) (per-symbol, 同 kf_unified 公式)
           - 过程噪声 Q_sym: design_Q 同湍流等级 (AWGN 用 SIGMA2_P_B11 per-symbol)
  跨块: P 矩阵从块尾传下一块头 (TL-09), φ_init 用上一块末尾 φ (连续性).
  再施加: rc_ddkf[k] = rx_raw[k] · exp(-j·x[0]) (per-symbol 相位补偿, DD-KF 直出).
  resolve + demod + BER (NDA 用 resolve_m16apsk_blockwise 解 M₀ 模糊; DA 直接 demod data 位置).

m16apsk 适配 (§2.1 选项 A, 不改 common/_kf.py):
  hard_decision_m16apsk(z): 用 m16apsk 星座点 (_M16APSK_SYM, 16 点最近邻) 判定, 返回最近邻星座点.
  kf_unified_dd_apsk(rx_block, h_b, gamma_bar, Q_sym, phi_init, df_init, P_init):
    复制 kf_unified 逻辑 (_kf.py:40-65), 把 hard_decision(mod='qpsk') 改为 hard_decision_m16apsk.

公平性 (§2.3 纪律 1):
  - NDA+DD-KF 和 DA+DD-KF 同 Q_sym (per 场景), 同 DD-KF 结构 (2 状态 per-symbol), 同 R 公式.
  - DA 在 pilot 位置用真 pilot 符号 (genie, 同主实验 DA pilot 设置), data 位置 decision-directed.
    — 这对 DA 是天然优势 (pilot 锚定), 但 DD-KF 对称施加, 反转风险反映 DD-KF 是否放大此差异.
  - 不给某方法调优 DD-KF. DD-KF 是"对称施加的 per-symbol decision-directed 跟踪层".

反转判定 (§2.1, §2.2):
  gain_no_kf = 主实验 fair gain @ HD-FEC (NDA vs DA, 从 _fair_gain_summary.json 读基准)
  gain_dd_kf = 消融 fair gain @ HD-FEC (NDA+DD-KF vs DA+DD-KF)
  delta = gain_dd_kf − gain_no_kf (负 = DD-KF 让 NDA 优势缩小 = 反转风险信号)
  high-SNR (≥16dB) 逐点查 DA+DD-KF 是否反超 NDA+DD-KF.

种子 (§2.3 纪律 3): 5 seed, 第 0 seed = MVE seed (SEED_AWGN/SEED_TURB0). 与主实验/per-block KF 消融完全一致.

运行: cd projects/simulation && python simulator/run_dd_kf_ablation.py
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

# 核心算法全从 common/ 导入 (守 TL-13, 不准 import explore/, 不改 common/_kf.py 核心)
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
# KF Q 矩阵设计 (common/_kf.py 公开 API design_Q, 不改其源码)
from common import design_Q as _kf_design_Q  # noqa: E402
# m16apsk 星座点 (用于 hard_decision_m16apsk 最近邻判定)
from common._modulation import _M16APSK_SYM  # noqa: E402

# --- 输出目录 ---
OUT_DIR = os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_dd_kf_ablation')
os.makedirs(OUT_DIR, exist_ok=True)

N_SEEDS = 5
T05_4 = float(stats.t.ppf(0.975, 4))   # 2.7764
SCENES = ['awgn', 'weak', 'moderate', 'strong']
TURB_LEVELS = ['weak', 'moderate', 'strong']

# per-symbol 时间步: AWGN 用 B11 T_S_B11 (40ps), 湍流用 system T_S_GLOBAL (400ps) — 与各自信道生成一致.
T_SYM_AWGN = P.T_S_B11
T_SYM_TURB = P.T_S_GLOBAL


# =============================================================================
# 种子 (与主实验/per-block KF 消融完全一致, §2.3 纪律 3)
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
# §2.1 选项 A: m16apsk 判决函数 (不污染 common)
# =============================================================================
def hard_decision_m16apsk(z):
    """(8,8)-16APSK 最近邻硬判决 (标量或向量).

    用 _M16APSK_SYM (16 点星座) 欧氏最近邻判定, 返回最近邻星座点 (复数).
    验证 (§2.3 步骤 2): 对无噪声 tx 符号应返回自身 — main() 内有自检.
    与 common/_modulation.py:hard_decision(mod='m16apsk') 等价 (但 common 那个未实现, 这里独立写).
    """
    z = np.asarray(z, dtype=complex)
    if z.ndim == 0:
        d = np.abs(z - _M16APSK_SYM) ** 2
        return complex(_M16APSK_SYM[int(np.argmin(d))])
    # 向量化
    d = np.abs(z[:, np.newaxis] - _M16APSK_SYM[np.newaxis, :]) ** 2
    idx = np.argmin(d, axis=1)
    return _M16APSK_SYM[idx]


# =============================================================================
# §2.1 选项 A: kf_unified_dd_apsk (复制 kf_unified, 改 m16apsk 判决, 不改 common/_kf.py)
# =============================================================================
def kf_unified_dd_apsk(rx_block, h_b, gamma_bar, Q_sym, T_sym,
                       phi_init=None, df_init=0.0, P_init=None,
                       pilot_idx=None, pilot_sym=None):
    """per-symbol DD-KF, m16apsk 判决 (复制 common/_kf.py:kf_unified 改 hard_decision).

    状态 x=[φ, df], F=[[1, T_sym],[0,1]], H=[[1,0]] (per-symbol 时间步).
    观测 z_k = angle(rx[k] · conj(s_hat)):
      - DA pilot 位置: s_hat = pilot_sym (genie 已知)
      - 其他位置: s_hat = hard_decision_m16apsk(rx[k] · exp(-j·x_pred[0])) (decision-directed)
    测量噪声 R = 1/(2·γ_bar·h_b) (per-symbol, 同 kf_unified).

    P 跨块传递 (TL-09): 返回 P_final 供下一块 P_init.
    返回 (rx_compensated, phi_full, df_final, P_final).
    """
    N = len(rx_block)
    F = np.array([[1.0, T_sym], [0.0, 1.0]])
    H = np.array([[1.0, 0.0]])

    if phi_init is None:
        phi_init = np.angle(rx_block[0] ** P.M0) / P.M0  # 兜底升幂估初相

    x = np.array([float(phi_init), float(df_init)])
    if P_init is not None:
        P_cov = np.asarray(P_init, dtype=float).copy()
    else:
        P_cov = np.diag([(np.pi / 4) ** 2, (2 * np.pi * 100e3) ** 2])

    # DA pilot 索引集 (set for O(1) lookup)
    pilot_set = set()
    if pilot_idx is not None and pilot_sym is not None:
        pilot_idx = np.atleast_1d(np.asarray(pilot_idx))
        pilot_sym = np.atleast_1d(np.asarray(pilot_sym, dtype=complex))
        pilot_set = {int(i): complex(s) for i, s in zip(pilot_idx, pilot_sym)}

    R = 1.0 / (2.0 * gamma_bar * max(float(h_b), 1e-6))
    rx_comp = np.zeros(N, dtype=complex)
    phi_full = np.zeros(N)

    for k in range(N):
        x_pred = F @ x
        P_pred = F @ P_cov @ F.T + Q_sym

        if k in pilot_set:
            # DA pilot 位置: genie 已知符号 (不决策错误传播)
            s_hat = pilot_set[k]
        else:
            # decision-directed: m16apsk 最近邻硬判决
            rx_rotated = rx_block[k] * np.exp(-1j * x_pred[0])
            s_hat = hard_decision_m16apsk(rx_rotated)

        y = rx_block[k] * np.conj(s_hat)
        z_obs = float(np.angle(y))

        innov = z_obs - x_pred[0]
        innov = (innov + np.pi) % (2.0 * np.pi) - np.pi

        S = float((H @ P_pred @ H.T)[0, 0] + R)
        K = P_pred @ H.T.flatten() / S

        x = x_pred + K * innov
        x[0] = (x[0] + np.pi) % (2.0 * np.pi) - np.pi

        P_cov = (np.eye(2) - np.outer(K, H[0])) @ P_pred
        phi_full[k] = x[0]
        rx_comp[k] = rx_block[k] * np.exp(-1j * x[0])

    return rx_comp, phi_full, float(x[1]), P_cov


def make_Q_sym(turb_name_or_awgn):
    """构造 per-symbol DD-KF 过程噪声 Q_sym (per-symbol 时间步).

    AWGN: sigma2_phi = SIGMA2_P_B11 (B11 线宽 500kHz, 匹配实际 AWGN 信道 PN per-symbol), 无 turbulence/df.
    湍流: design_Q(turb_name, DOPPLER_HIGH) 直接用 (per-symbol, 同 common/_kf.py).
    公平 (§2.3 纪律 1): NDA+DD-KF 和 DA+DD-KF 同 Q_sym.
    """
    if turb_name_or_awgn == 'awgn':
        # AWGN 信道只有 Wiener PN (SIGMA2_P_B11 per-symbol), 无 turbulence, 无 Doppler (df=0).
        # df 漂移给极小值 (AWGN 真 df=0, 但留小窗让 DD-KF 不僵化).
        sigma2_phi_sym = P.SIGMA2_P_B11
        sigma2_df_sym = (10e3 * T_SYM_AWGN) ** 2 * 0.1  # 极小 df 漂移
        return np.diag([sigma2_phi_sym, sigma2_df_sym])
    # 湍流: 用 common/_kf.py design_Q (同湍流等级 + 同 f_dot, §2.3 纪律 1)
    return _kf_design_Q(turb_name_or_awgn, P.DOPPLER_HIGH)


# =============================================================================
# AWGN: per-block CPE 初始化 + (可选) per-symbol DD-KF 跟踪, 一个 seed 一 SNR 点.
# =============================================================================
def run_awgn_point_ddkf(snr_db, seed_base):
    """AWGN 单 SNR 点, 单 seed_base. 返回 4 配置 BER.

    复用主实验 seed 派生 (per-SNR seed = seed_base + int(snr*1000), bits seed = seed+7).
    """
    N_sym = P.N_BLOCKS * P.N_DFT
    seed = seed_base + int(snr_db * 1000)
    rng = np.random.default_rng(seed + 7)
    bits = rng.integers(0, 2, N_sym * P.BITS_PER_SYM)
    tx = m16apsk_mod(bits)
    rx, phi_true = S.awgn_wiener_channel(tx, snr_db, seed)

    n_blk = P.N_BLOCKS
    Ns = P.N_DFT
    L = n_blk * Ns
    tb = bits[:L * P.BITS_PER_SYM]
    gamma_lin = 10.0 ** (snr_db / 10.0)

    # --- NDA per-block CPE 初始化 (复用主实验 ber_nda_awgn 内部逻辑) ---
    rc_nda_nokf = np.zeros(L, dtype=complex)
    phi_nda_blk = np.zeros(n_blk)
    for b in range(n_blk):
        seg = rx[b * Ns:(b + 1) * Ns]
        rc, _, phi_est, _ = nda_ml_recovery(seg, P.M0, mod='m16apsk', assume_df_zero=True)
        rc_nda_nokf[b * Ns:(b + 1) * Ns] = rc
        phi_nda_blk[b] = phi_est
    # no-KF BER (resolve M₀ 模糊 per-block, 与主实验一致)
    resolved_nda = resolve_m16apsk_blockwise(rc_nda_nokf, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    ne_nda_nokf = int(np.sum(tb != m16apsk_demod(resolved_nda)))
    nb_nda = len(tb)

    # --- DA per-block CPE 初始化 (复用主实验 ber_da_awgn 内部逻辑) ---
    tx_sym = m16apsk_mod(tb)
    pilot_idx_local = np.arange(0, Ns, P.DA_PILOT_SPACING)
    is_data = np.ones(Ns, dtype=bool)
    is_data[pilot_idx_local] = False
    rc_da_nokf = np.zeros(L, dtype=complex)
    phi_da_blk = np.zeros(n_blk)
    df_da_blk = np.zeros(n_blk)
    for b in range(n_blk):
        s_blk = slice(b * Ns, (b + 1) * Ns)
        p_sym = tx_sym[b * Ns + pilot_idx_local]
        rc, phi_est, df_est = da_ml_recovery(rx[s_blk], pilot_idx=pilot_idx_local,
                                             pilot_sym=p_sym, mod='m16apsk')
        rc_da_nokf[s_blk] = rc
        phi_da_blk[b] = phi_est
        df_da_blk[b] = df_est
    # no-KF BER (data 位置)
    demod_da = m16apsk_demod(rc_da_nokf)
    tb_arr = tb.reshape(L, P.BITS_PER_SYM)
    dm_arr = demod_da.reshape(L, P.BITS_PER_SYM)
    is_data_sym = np.zeros(L, dtype=bool)
    for b in range(n_blk):
        is_data_sym[b * Ns:(b + 1) * Ns] = is_data
    ne_da_nokf = int(np.sum(tb_arr[is_data_sym] != dm_arr[is_data_sym]))
    nb_da = int(np.sum(is_data_sym) * P.BITS_PER_SYM)

    # --- AWGN h≡1 (无 fading), DD-KF R 用 h=1 ---
    h_blk = 1.0
    Q_sym = make_Q_sym('awgn')

    # --- NDA+DD-KF: per-block CPE 初始化 φ + per-symbol DD-KF 跟踪 (P 跨块传递) ---
    rc_nda_ddkf = np.zeros(L, dtype=complex)
    P_cov = None
    for b in range(n_blk):
        s_blk = slice(b * Ns, (b + 1) * Ns)
        seg = rx[s_blk]
        phi_init = float(phi_nda_blk[b]) if b == 0 else float(rc_phi_last)
        df_init = 0.0  # AWGN 真 df=0
        rc_b, phi_b, _, P_cov = kf_unified_dd_apsk(
            seg, h_blk, gamma_lin, Q_sym, T_SYM_AWGN,
            phi_init=phi_init, df_init=df_init, P_init=(P_cov if b > 0 else None),
            pilot_idx=None, pilot_sym=None)
        rc_nda_ddkf[s_blk] = rc_b
        rc_phi_last = float(phi_b[-1])
    resolved_nda_ddkf = resolve_m16apsk_blockwise(rc_nda_ddkf, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    ne_nda_ddkf = int(np.sum(tb != m16apsk_demod(resolved_nda_ddkf)))

    # --- DA+DD-KF: per-block CPE 初始化 φ/df + per-symbol DD-KF 跟踪 (pilot 位置 genie) ---
    rc_da_ddkf = np.zeros(L, dtype=complex)
    P_cov = None
    for b in range(n_blk):
        s_blk = slice(b * Ns, (b + 1) * Ns)
        seg = rx[s_blk]
        p_sym = tx_sym[b * Ns + pilot_idx_local]
        phi_init = float(phi_da_blk[b]) if b == 0 else float(rc_phi_last)
        df_init = float(df_da_blk[b]) if b == 0 else 0.0
        rc_b, phi_b, _, P_cov = kf_unified_dd_apsk(
            seg, h_blk, gamma_lin, Q_sym, T_SYM_AWGN,
            phi_init=phi_init, df_init=df_init, P_init=(P_cov if b > 0 else None),
            pilot_idx=pilot_idx_local, pilot_sym=p_sym)
        rc_da_ddkf[s_blk] = rc_b
        rc_phi_last = float(phi_b[-1])
    demod_da_ddkf = m16apsk_demod(rc_da_ddkf)
    dm_arr_ddkf = demod_da_ddkf.reshape(L, P.BITS_PER_SYM)
    ne_da_ddkf = int(np.sum(tb_arr[is_data_sym] != dm_arr_ddkf[is_data_sym]))

    return {
        'snr_db': float(snr_db),
        'nda_ber_nokf': ne_nda_nokf / nb_nda,
        'da_ber_nokf': ne_da_nokf / nb_da,
        'nda_ber_ddkf': ne_nda_ddkf / nb_nda,
        'da_ber_ddkf': ne_da_ddkf / nb_da,
    }


# =============================================================================
# 湍流: per-block CPE 初始化 + per-symbol DD-KF 跟踪, 一个 seed 一 SNR 点.
# 复用主实验 run_turb 内部逻辑 (per-block h 估计 + 两阶段 FOE).
# =============================================================================
def run_turb_point_ddkf(turb_name, gamma_db, seed0):
    """湍流单 γ 点, 单 seed0. 返回 4 配置 BER. 复用主实验 per-block 结构."""
    cfg = SimulationConfig()
    Ns = P.N_DFT
    gamma_lin = 10 ** (gamma_db / 10)
    ne_nda_nokf = ne_da_nokf = 0
    ne_nda_ddkf = ne_da_ddkf = 0
    nb_nda = nb_da = 0

    pilot_idx_local = np.arange(0, Ns, P.DA_PILOT_SPACING)
    is_data = np.ones(Ns, dtype=bool)
    is_data[pilot_idx_local] = False
    n_blocks = P.N_BLOCKS
    Q_sym = make_Q_sym(turb_name)

    # DD-KF 状态跨块连续: P 跨块传递, φ/df 用上块尾初始化下块头
    P_cov_nda = None
    P_cov_da = None
    phi_last_nda = None
    phi_last_da = None

    for b in range(n_blocks):
        r = generate_shared_realization_apsk(
            Ns, gamma_lin, turb_name, cfg.doppler.DOPPLER_HIGH,
            mod='m16apsk', seed=seed0 + b)
        rx_raw = r['rx_raw']
        bits = r['bits']
        tx_sym = r['tx']
        # 幅度处理 (修复 D2): per-block h — NDA blind / DA pilot 各自估计
        h_blind = S.estimate_h_blind_perblock(rx_raw, gamma_lin)
        rx_blind = amp_limit(mmse_equalize(rx_raw, h_blind, gamma_lin), 3.0)
        h_pilot = S.estimate_h_pilot_perblock(rx_raw, tx_sym, gamma_lin)
        rx_pilot = amp_limit(mmse_equalize(rx_raw, h_pilot, gamma_lin), 3.0)
        tb = bits[:Ns * P.BITS_PER_SYM]
        tb_arr = tb.reshape(Ns, P.BITS_PER_SYM)

        # --- NDA per-block CPE 初始化 (复用主实验 ber_nda_turb 两阶段逻辑) ---
        omega_est = S.fft_foe_m0_omega(rx_blind, P.M0)
        k = np.arange(Ns)
        seg_foe = rx_blind * np.exp(-1j * omega_est * k)
        rc_nda_nokf_b, _, phi_nda_b, _ = nda_ml_recovery(seg_foe, P.M0, mod='m16apsk', assume_df_zero=True)
        # no-KF BER
        resolved = resolve_m16apsk_blockwise(rc_nda_nokf_b, tb, block_size=P.BLOCK_SIZE_RESOLVE)
        ne_nda_nokf += int(np.sum(tb != m16apsk_demod(resolved)))
        nb_nda += len(tb)

        # --- DA per-block CPE 初始化 (复用主实验 ber_da_turb/ber_da_awgn 逻辑) ---
        p_sym = tx_sym[pilot_idx_local]
        rc_da_nokf_b, phi_da_b, df_da_b = da_ml_recovery(
            rx_pilot, pilot_idx=pilot_idx_local, pilot_sym=p_sym, mod='m16apsk')
        # no-KF BER (data 位置)
        demod_da = m16apsk_demod(rc_da_nokf_b)
        dm_arr = demod_da.reshape(Ns, P.BITS_PER_SYM)
        ne_da_nokf += int(np.sum(tb_arr[is_data] != dm_arr[is_data]))
        nb_da += int(np.sum(is_data) * P.BITS_PER_SYM)

        # --- NDA+DD-KF: per-block CPE 初始化 + per-symbol DD-KF (P 跨块) ---
        h_b_nda = max(float(np.mean(h_blind)), 1e-6)
        phi_init_nda = float(phi_nda_b) if b == 0 else float(phi_last_nda)
        rc_nda_ddkf_b, phi_nda_full, _, P_cov_nda = kf_unified_dd_apsk(
            seg_foe, h_b_nda, gamma_lin, Q_sym, T_SYM_TURB,
            phi_init=phi_init_nda, df_init=0.0,
            P_init=(P_cov_nda if b > 0 else None),
            pilot_idx=None, pilot_sym=None)
        phi_last_nda = float(phi_nda_full[-1])
        resolved_ddkf = resolve_m16apsk_blockwise(rc_nda_ddkf_b, tb, block_size=P.BLOCK_SIZE_RESOLVE)
        ne_nda_ddkf += int(np.sum(tb != m16apsk_demod(resolved_ddkf)))

        # --- DA+DD-KF: per-block CPE 初始化 + per-symbol DD-KF (pilot genie) ---
        h_b_da = max(float(np.mean(h_pilot)), 1e-6)
        phi_init_da = float(phi_da_b) if b == 0 else float(phi_last_da)
        rc_da_ddkf_b, phi_da_full, _, P_cov_da = kf_unified_dd_apsk(
            rx_pilot, h_b_da, gamma_lin, Q_sym, T_SYM_TURB,
            phi_init=phi_init_da, df_init=float(df_da_b),
            P_init=(P_cov_da if b > 0 else None),
            pilot_idx=pilot_idx_local, pilot_sym=p_sym)
        phi_last_da = float(phi_da_full[-1])
        demod_da_ddkf = m16apsk_demod(rc_da_ddkf_b)
        dm_arr_ddkf = demod_da_ddkf.reshape(Ns, P.BITS_PER_SYM)
        ne_da_ddkf += int(np.sum(tb_arr[is_data] != dm_arr_ddkf[is_data]))

    return {
        'snr_db': float(gamma_db),
        'nda_ber_nokf': ne_nda_nokf / nb_nda,
        'da_ber_nokf': ne_da_nokf / nb_da,
        'nda_ber_ddkf': ne_nda_ddkf / nb_nda,
        'da_ber_ddkf': ne_da_ddkf / nb_da,
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
            raw['awgn'][i] = [run_awgn_point_ddkf(snr, seed_base_awgn(i)) for snr in P.SNR_AWGN_DB]
            print(f"   done {len(raw['awgn'][i])} SNR 点")
        for turb in TURB_LEVELS:
            if turb in scenes_to_run:
                print(f"\n#### {turb} seed {i} (seed0={seed0_turb(i)}) ####")
                raw[turb][i] = [run_turb_point_ddkf(turb, g, seed0_turb(i)) for g in P.SNR_TURB_DB]
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
            for cfg_name in ['nda_ber_nokf', 'da_ber_nokf', 'nda_ber_ddkf', 'da_ber_ddkf']:
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
    nda_key/da_key ∈ {'nokf','ddkf'} (映射到 *_ber_mean)."""
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
    """逐 high-SNR 点查 DD-KF 引起的排序变化.

    真正的反转是: DD-KF 改变了 NDA vs DA 的排序 (no-KF 时 NDA 赢/平, +DD-KF 后 DA 赢).
    此处报两层: (a) raw BER 排序, (b) DD-KF 是否改变排序 (reversal_induced_by_ddkf).
    """
    out = []
    for p in summary_points:
        if p['snr_db'] < high_snr_thresh:
            continue
        nda_ddkf = p['nda_ber_ddkf_mean']
        da_ddkf = p['da_ber_ddkf_mean']
        nda_nokf = p['nda_ber_nokf_mean']
        da_nokf = p['da_ber_nokf_mean']
        da_lower_ddkf = bool(da_ddkf < nda_ddkf)
        da_lower_nokf = bool(da_nokf < nda_nokf)
        reversal_induced_by_ddkf = bool((not da_lower_nokf) and da_lower_ddkf)
        out.append({
            'snr_db': p['snr_db'],
            'nda_ddkf_mean': nda_ddkf, 'da_ddkf_mean': da_ddkf,
            'da_ddkf_lower_than_nda_ddkf': da_lower_ddkf,
            'ratio_ddkf': float(da_ddkf / nda_ddkf) if nda_ddkf > 0 else None,
            'nda_nokf_mean': nda_nokf, 'da_nokf_mean': da_nokf,
            'da_nokf_lower_than_nda_nokf': da_lower_nokf,
            'reversal_induced_by_ddkf': reversal_induced_by_ddkf,
        })
    return out


def reversal_judgment(summary, scenes_to_run):
    """反转判定 per 场景: gain_no_kf vs gain_dd_kf vs delta + high-SNR 反超."""
    out = {}
    for sc in scenes_to_run:
        pts = summary[sc]['points']
        fg_nokf = fair_gain_for_config(pts, 'nokf', 'nokf')
        fg_ddkf = fair_gain_for_config(pts, 'ddkf', 'ddkf')
        g_nokf = fg_nokf['gain_nda_vs_da_fair_db']
        g_ddkf = fg_ddkf['gain_nda_vs_da_fair_db']
        delta = (g_ddkf - g_nokf) if (g_ddkf is not None and g_nokf is not None) else None
        hs = per_point_high_snr_reversal(pts)
        any_da_ddkf_reversal = any(p['reversal_induced_by_ddkf'] for p in hs)
        any_da_ddkf_raw_lower = any(p['da_ddkf_lower_than_nda_ddkf'] for p in hs)
        out[sc] = {
            'gain_no_kf_db': g_nokf,
            'gain_dd_kf_db': g_ddkf,
            'gain_delta_db': delta,
            'hdfec_reachable_nokf': fg_nokf['hdfec_reachable'],
            'hdfec_reachable_ddkf': fg_ddkf['hdfec_reachable'],
            'high_snr_points': hs,
            'any_ddkf_induced_reversal_high_snr': any_da_ddkf_reversal,
            'any_da_ddkf_raw_ber_lower_high_snr': any_da_ddkf_raw_lower,
            'fair_gain_no_kf_full': {k: fg_nokf[k] for k in
                                     ['snr_nda_tot_at_hdfec', 'snr_da_tot_at_hdfec',
                                      'gain_nda_vs_da_fair_db', 'fair_gain_high_snr_db',
                                      'fair_gain_mean_db', 'min_nda_ber']},
            'fair_gain_dd_kf_full': {k: fg_ddkf[k] for k in
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
        nda_ddkf = [p['nda_ber_ddkf_mean'] for p in pts]
        da_ddkf = [p['da_ber_ddkf_mean'] for p in pts]
        ax.semilogy(gts, nda_nokf, 'o-', color='C0', label='NDA-ML (no KF)', lw=1.6)
        ax.semilogy(gts, da_nokf, 's-', color='C1', label='DA ML (no KF)', lw=1.6)
        ax.semilogy(gts, nda_ddkf, 'o--', color='C0', label='NDA-ML + DD-KF', lw=1.8)
        ax.semilogy(gts, da_ddkf, 's--', color='C1', label='DA ML + DD-KF', lw=1.8)
        ax.axhline(P.HDFEC, color='k', ls=':', label='HD-FEC 3.8e-3')
        r = reversal[sc]
        g_nokf = r['gain_no_kf_db']
        g_ddkf = r['gain_dd_kf_db']
        ttl = f"{titles[sc]}\ngain@HDFEC: noKF={g_nokf}, +DDKF={g_ddkf}" if (g_nokf is not None and g_ddkf is not None) else \
              f"{titles[sc]}\ngain noKF={g_nokf}, +DDKF={g_ddkf}"
        ax.set_title(ttl, fontsize=9.5)
        ax.set_xlabel(r'$\gamma_{tot}$ (dB)')
        ax.set_ylabel('BER')
        ax.grid(True, which='both', alpha=0.3)
        ax.legend(fontsize=7, loc='best')
        ax.set_ylim(bottom=1e-4)
    fig.suptitle('per-symbol DD-KF 消融 (FR-18 反转验证, 强 KF): NDA/DA × {no KF, +DD-KF} (5 seed 均值)',
                 fontsize=12, y=1.01)
    fig.tight_layout()
    png = os.path.join(OUT_DIR, '_dd_kf_ablation_curves.png')
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
# m16apsk 判决自检 (§2.3 步骤 2: 对无噪声 tx 应返回自身)
# =============================================================================
def selfcheck_hard_decision():
    rng = np.random.default_rng(0)
    bits = rng.integers(0, 2, 16 * P.BITS_PER_SYM)
    tx = m16apsk_mod(bits)
    s_hat = hard_decision_m16apsk(tx)
    err = float(np.max(np.abs(s_hat - tx)))
    return err < 1e-12, err


# =============================================================================
# 主
# =============================================================================
def main():
    t0 = time.time()
    main_json_path = os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_main',
                                  '_main_experiment_5seed.json')

    print("=" * 100)
    print("per-symbol DD-KF 消融 (FR-18 反转验证, 强 KF): NDA/DA × {no KF, +DD-KF}, 5 seed × 4 场景")
    print("DD-KF 架构: per-block CPE 初始化 + per-symbol decision-directed Kalman (m16apsk 判决)")
    print("适配方式: 选项 A (脚本内 hard_decision_m16apsk + kf_unified_dd_apsk, 不改 common/_kf.py)")
    print("公平: NDA+DD-KF 和 DA+DD-KF 同 Q_sym (per 场景), 同 R 公式 (R=1/(2γh_b), per-symbol)")
    print(f"  AWGN T_sym={T_SYM_AWGN:.2e}s (B11 T_S); 湍流 T_sym={T_SYM_TURB:.2e}s (sys T_S)")

    # --- §2.3 步骤 2: m16apsk 判决自检 ---
    ok, err = selfcheck_hard_decision()
    print(f"  hard_decision_m16apsk 自检 (无噪声 tx→自身): {'PASS ✅' if ok else 'FAIL ❌'} (max err={err:.2e})")
    if not ok:
        print("  [警告] m16apsk 判决异常, 继续 (但需查)")

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

    # --- 落盘 _dd_kf_ablation_5seed.json ---
    out = {
        'meta': {
            'task': 'per-symbol DD-KF 消融 (FR-18 反转验证, 强 KF)',
            'metric': 'BER (4 配置) + fair gain @ HD-FEC (no-KF vs +DD-KF) + 反转指标',
            'n_seeds': N_SEEDS,
            'seed_strategy': {
                'awgn': 'seed_base_i = SEED_AWGN + i (per-SNR seed=seed_base+int(snr*1000))',
                'turbulence': 'seed0_i = SEED_TURB0 + i*N_BLOCKS (5 seed 块范围互斥)',
                'note': 'seed 0 = MVE seed (可复现); 与主实验/per-block KF 消融完全一致',
            },
            'scenes': scenes_to_run,
            'configs': ['NDA (no KF)', 'DA (no KF)', 'NDA+DD-KF', 'DA+DD-KF'],
            'ddkf_architecture': 'per-block CPE 初始化 (复用主实验 nda_ml/da_ml_recovery) + '
                                 'per-symbol decision-directed Kalman 跟踪 (复制 kf_unified 改 m16apsk 判决)',
            'ddkf_state': 'x=[φ, df], F=[[1, T_sym],[0,1]], H=[[1,0]] (per-symbol 时间步)',
            'ddkf_observation': 'z_k = angle(rx[k]·conj(s_hat)); s_hat = pilot_sym (DA pilot 位置 genie) '
                                '或 hard_decision_m16apsk (decision-directed, m16apsk 最近邻)',
            'ddkf_R': 'R = 1/(2·γ_bar·h_b), per-symbol, 同 kf_unified 公式; h_b 用各法自估 (NDA blind / DA pilot)',
            'ddkf_Q': 'AWGN: sigma2_phi=SIGMA2_P_B11 per-symbol (匹配实际信道 PN), df≈0; '
                      '湍流: design_Q(turb, DOPPLER_HIGH) per-symbol (同 common/_kf.py, 同湍流等级同 f_dot)',
            'cross_block_P_transfer': 'P 矩阵从块尾传下一块头 (TL-09); φ/df 用上块尾初始化下块头',
            'fairness': 'NDA+DD-KF 和 DA+DD-KF 同 Q_sym 同结构 (§2.3 纪律 1), 不给某方法调优 DD-KF',
            'reapply': 'rc_ddkf[k] = rx_raw[k]·exp(-j·x[0]) (per-symbol 相位补偿, DD-KF 直出)',
            'M0_ambiguity_resolve': 'NDA: resolve_m16apsk_blockwise (tx_bits, 同主实验) 解 M0=8 模糊; '
                                    'DA: pilot 已知无模糊',
            'sc_simulator_unchanged': True,
            'common_kf_unchanged': True,
            'M_APSK_ddkf_adaptation': '选项 A: 脚本内 hard_decision_m16apsk (最近邻) + kf_unified_dd_apsk '
                                       '(复制 kf_unified 改 hard_decision), 不改 common/_kf.py 核心 (守 TL-13)',
            'M0': P.M0, 'pilot_spacing': P.DA_PILOT_SPACING,
            'pilot_overhead_db': float(P.PILOT_OVERHEAD_DB), 'hdfec': P.HDFEC,
            'N_per_point': P.N_SYM_PER_POINT, 'N_blocks': P.N_BLOCKS,
            'seed_awgn_mve': P.SEED_AWGN, 'seed_turb0_mve': P.SEED_TURB0,
            'python': sys.executable, 'numpy_version': np.__version__,
            'hard_decision_selfcheck': {'pass': bool(ok), 'max_err': float(err)},
            'elapsed_sec': float(elapsed),
        },
        'seed0_reproducibility_vs_main': to_jsonable(repro),
        'summary': to_jsonable(summary),
        'reversal_analysis': to_jsonable(reversal),
        'ber_curves_png': png_path,
    }
    out_json = os.path.join(OUT_DIR, '_dd_kf_ablation_5seed.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(out), f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {out_json}")
    print(f"[保存] {png_path}")

    # --- 落盘 _dd_kf_ablation_summary.json (精简反转判定) ---
    fair_summary = {'meta': {
        'task': 'FR-18 反转验证汇总 (per-symbol DD-KF 消融, 强 KF)',
        'gain_definition': 'fair_gain@HD-FEC = (DA γ_tot @ HD-FEC) − (NDA γ_tot @ HD-FEC); 正=NDA赢',
        'reversal_criterion': 'gain_delta<0 或 high-SNR DA+DD-KF 反超 NDA+DD-KF → 反转风险信号',
        'note_no_kf_baseline': 'gain_no_kf 取自本消融 seed0 可复现的 no-KF 配置 (与主实验一致)',
        'vs_per_block_kf': 'per-block KF 消融 delta ∈ ±0.002 dB (run_kf_ablation.py, 不反转); '
                           '本 DD-KF 是更强 per-symbol decision-directed, 回答用户最担心的口子',
    }, 'reversal_per_scene': {}}
    for sc in scenes_to_run:
        r = reversal[sc]
        g_nokf = r['gain_no_kf_db']
        g_ddkf = r['gain_dd_kf_db']
        delta = r['gain_delta_db']
        ddkf_induced = r['any_ddkf_induced_reversal_high_snr']
        raw_lower = r['any_da_ddkf_raw_ber_lower_high_snr']
        # 反转 flag (主判据 = fair-gain delta; 辅 = DD-KF 引起的 raw-BER 排序变化)
        reversal_flag = (delta is not None and delta < -0.1) or ddkf_induced
        # 定性 (fair-gain 为主, raw-BER DD-KF-排序变化为辅)
        if delta is None:
            verdict = 'HD-FEC 不可达 (无法算 gain@HD-FEC); high-SNR DD-KF 排序变化: ' + \
                      ('有 (DD-KF 引起 DA 反超)' if ddkf_induced else '无')
        elif delta < -0.1 and ddkf_induced:
            verdict = '反转 (fair-gain 显著缩小 + high-SNR DD-KF 引起 DA 反超)'
        elif delta < -0.1:
            verdict = '反转风险 (fair-gain 显著缩小, high-SNR 排序未变)'
        elif ddkf_induced:
            verdict = '局部反转 (high-SNR DD-KF 引起 raw-BER DA 反超, fair-gain@HD-FEC 未全翻)'
        elif delta < -0.02:
            verdict = '轻微缩小 (DD-KF 让 NDA fair-gain 略减, 未反转)'
        else:
            verdict = '不反转 (DD-KF 后 NDA fair-gain 稳定)'
        fair_summary['reversal_per_scene'][sc] = {
            'gain_no_kf_db': g_nokf, 'gain_dd_kf_db': g_ddkf, 'gain_delta_db': delta,
            'hdfec_reachable_nokf': r['hdfec_reachable_nokf'],
            'hdfec_reachable_ddkf': r['hdfec_reachable_ddkf'],
            'any_ddkf_induced_reversal_high_snr': ddkf_induced,
            'any_da_ddkf_raw_ber_lower_high_snr': raw_lower,
            'reversal_flag': bool(reversal_flag),
            'verdict': verdict,
            'high_snr_reversal_points': r['high_snr_points'],
        }
    fair_json = os.path.join(OUT_DIR, '_dd_kf_ablation_summary.json')
    with open(fair_json, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(fair_summary), f, indent=2, ensure_ascii=False)
    print(f"[保存] {fair_json}")

    # --- 控制台汇总 ---
    print("\n" + "=" * 100)
    print("反转判定 (FR-18, 强 KF): gain_no_kf vs gain_dd_kf vs delta (fair-gain @ HD-FEC, γ_tot 坐标)")
    print(f"{'场景':>10} {'gain_noKF':>12} {'gain_+DDKF':>12} {'delta':>10} {'DDKF引起raw反超':>16} {'verdict'}")
    for sc in scenes_to_run:
        r = reversal[sc]
        g_nokf = r['gain_no_kf_db']; g_ddkf = r['gain_dd_kf_db']; delta = r['gain_delta_db']
        ddkf_ind = r['any_ddkf_induced_reversal_high_snr']
        v = fair_summary['reversal_per_scene'][sc]['verdict']
        def fmt(x):
            return f'{x:+.4f}' if isinstance(x, float) else str(x)
        print(f"{sc:>10} {fmt(g_nokf):>12} {fmt(g_ddkf):>12} {fmt(delta):>10} {str(ddkf_ind):>16} {v}")
    print(f"\n[总耗时] {elapsed:.1f} s (含 5 seed × {len(scenes_to_run)} 场景 × 4 配置)")


if __name__ == '__main__':
    main()
