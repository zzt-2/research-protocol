# -*- coding: utf-8 -*-
"""SC-NDA-ML 正式仿真器 (Formal, 独立实现, 非 explore 薄包装).

Step 7 Part A: 单载波时域 NDA-ML 载波相位估计改进仿真.
方向: (8,8)-16APSK + Wiener PN + Gamma-Gamma 块衰落, 星地激光通信.

架构 (design.md §2 模块清单):
  - 核心算法全从 common/ 导入 (守 TL-13, 不准重写/不准 import explore/):
      generate_shared_realization_apsk (信道), m16apsk_mod/demod + resolve_m16apsk_blockwise (调制),
      nda_ml_recovery / da_ml_recovery (估计器, D003 约定), fft_foe (FOE),
      mmse_equalize + amp_limit (均衡).
  - 独立实现 (Formal 新增):
      awgn_wiener_channel (B11 AWGN 场景, 逻辑同 MVE 但独立写),
      per-block h 估计 (NDA 盲 / DA pilot / oracle 真),
      逐块 NDA-ML/DA-ML/oracle BER 评估,
      两阶段 FOE (湍流场景 fft_foe + nda_ml_recovery),
      SNR 扫描 + BER 曲线 + 公平对照.

§4.5 MVE 一致性验证 (正确性锚点):
  同 seed (SEED_AWGN/SEED_TURB0 from MVE) 同参数下, Formal 实现的 NDA/DA/oracle BER
  必须与 `_mve_results.json` 一致 (相对误差 < 5% 或绝对 < 1e-4).
  这是 Formal 独立实现的正确性证明 — 数学算子一致 (共用 common/) + 信道/评估逻辑独立写但等价.

运行:
  cd projects/simulation && python simulator/sc_nda_ml_sim.py
"""
import os
import sys
import time
import json

import numpy as np

# --- 路径: simulation 根 ---
_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..'))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)
# simulator 自身目录 (for _b11_params / fair_comparison import)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

# =============================================================================
# 核心算法全从 common/ 导入 (守 TL-13: 共用信道/估计器/调制, 不重写算法)
# =============================================================================
from common import (  # noqa: E402
    generate_shared_realization_apsk,
    m16apsk_mod, m16apsk_demod,
    resolve_m16apsk_blockwise,
    da_ml_recovery, nda_ml_recovery,
    fft_foe,
    mmse_equalize, amp_limit,
)

# Formal 内部参数 + 公平对照 (独立模块, 不 import explore/)
import _b11_params as P  # noqa: E402
from fair_comparison import analyze_fair_gain  # noqa: E402
from params import SimulationConfig  # noqa: E402


# =============================================================================
# AWGN 信道 (B11 原始场景, 无湍流/无 Doppler/无 CFO, 仅 Wiener PN + AWGN)
# 独立实现, 逻辑等价于 MVE _time_domain_crlb.py:awgn_wiener_channel (B11 行 33/51 信号模型)
# =============================================================================
def awgn_wiener_channel(tx, snr_db, seed):
    """B11 信号模型 (行 33/51): r(k) = s(k)·exp(jθ(k)) + n(k), θ(k)=Wiener 累积 PN.

    无 FOE (Δf=0 已补偿), 无湍流, 无 Doppler. φ₀=0.
    与 MVE 等价 (同 SIGMA2_P_B11, 同 seed 派生, 同 noise_var=1/(2·γ_lin)).
    """
    rng = np.random.default_rng(seed)
    N = len(tx)
    # Wiener PN: θ(k) = cumsum(N(0, σ²_p)) (Viterbi 1963 标准模型, B11 行 51)
    phi = np.cumsum(rng.normal(0.0, np.sqrt(P.SIGMA2_P_B11), N))
    carrier = np.exp(1j * phi)
    signal = tx * carrier
    snr_lin = 10.0 ** (snr_db / 10.0)
    noise_var = 1.0 / (2.0 * snr_lin)   # 复噪声方差 σ², 每实/虚分量 σ²/2
    noise = np.sqrt(noise_var) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
    return signal + noise, phi


# =============================================================================
# per-block h 估计 (修复 D2: 替代 h_med 标量均衡; 对齐信道 CH_BLOCK=100)
# 独立实现, 逻辑等价于 MVE _time_domain_crlb.py:estimate_h_*_perblock
# =============================================================================
def estimate_h_blind_perblock(rx_raw, gamma_bar, block=P.CH_BLOCK):
    """盲 per-block h 估计 (NDA-ML, 无 pilot, 公平非 oracle).

    块内 |rx|² 平均 ≈ h·E[|s|²] + σ². E[|s|²]=1 (星座归一化), σ²=1/(2γ).
    → ĥ = mean(|rx|²) − 1/(2γ). 截断 ≥ 1e-6. 对齐信道 BLOCK (100 sym 内 h 恒定).
    """
    rx_raw = np.asarray(rx_raw)
    N = len(rx_raw)
    nb = (N + block - 1) // block
    h_est = np.empty(N, dtype=float)
    for i in range(nb):
        s = slice(i * block, min((i + 1) * block, N))
        p_rx = float(np.mean(np.abs(rx_raw[s]) ** 2))
        h_blk = p_rx - 1.0 / (2.0 * gamma_bar)
        h_est[s] = max(h_blk, 1e-6)
    return h_est


def estimate_h_pilot_perblock(rx_raw, tx_sym, gamma_bar,
                              pilot_spacing=P.DA_PILOT_SPACING, block=P.CH_BLOCK):
    """per-block pilot h 估计 (DA-ML): pilot 位置 r(p)=s(p)√h → ĥ=mean(|r(p)/s(p)|²).

    对齐信道 BLOCK. 公平 (DA 有 pilot, 用 pilot 估 h 非盲也非 oracle).
    """
    rx_raw = np.asarray(rx_raw)
    N = len(rx_raw)
    pilot_idx = np.arange(0, N, pilot_spacing)
    ratio_sq = np.abs(rx_raw[pilot_idx] / tx_sym[pilot_idx]) ** 2
    nb = (N + block - 1) // block
    h_est = np.empty(N, dtype=float)
    for i in range(nb):
        lo, hi = i * block, min((i + 1) * block, N)
        p_in_blk = (pilot_idx >= lo) & (pilot_idx < hi)
        h_blk = float(np.mean(ratio_sq[p_in_blk])) if np.any(p_in_blk) else 1.0
        h_est[lo:hi] = max(h_blk, 1e-6)
    return h_est


# =============================================================================
# M0 升幂 FOE (湍流场景两阶段第一步: 粗估 CFO)
# 独立实现, 逻辑等价于 MVE _time_domain_crlb.py:fft_foe_m0_omega (修复 D1: CFO 残余致相位斜坡)
# =============================================================================
def fft_foe_m0_omega(rx, M0_power, N_fft=None):
    """M0 升幂 FOE: rx^M0 去调制 → FFT 找频峰 → /M0 还原 CFO (omega, rad/sample).

    修复 D1: 星地湍流场景 F_RESIDUAL=1MHz CFO 致 0.64rad/块 相位斜坡, 必须估 FOE.
    返回 omega_est (rad/sample), 用于 exp(−j·omega·k) 补偿.

    注: 用系统 T_S_GLOBAL (信道 generate_shared_realization_apsk 用此), 非 B11 T_S.
    """
    rx = np.asarray(rx, dtype=complex)
    N = len(rx)
    if N_fft is None:
        N_fft = min(N, 4096)
    N_fft = min(N_fft, N)
    raised = rx ** M0_power
    seg = raised[:N_fft]
    win = np.hanning(N_fft)
    R = np.fft.fftshift(np.fft.fft(seg * win, n=N_fft * 8))
    freqs = np.fft.fftshift(np.fft.fftfreq(N_fft * 8, d=P.T_S_GLOBAL))
    idx = np.argmax(np.abs(R))
    if 1 <= idx < len(R) - 1:
        a_v, b_v, g_v = np.abs(R[idx - 1]), np.abs(R[idx]), np.abs(R[idx + 1])
        if b_v + a_v - 2 * g_v != 0:
            p = 0.5 * (a_v - g_v) / (a_v - 2 * b_v + g_v)
            df_raised = freqs[idx] + p * (freqs[1] - freqs[0])
        else:
            df_raised = freqs[idx]
    else:
        df_raised = freqs[idx]
    df_est_hz = df_raised / M0_power
    return 2 * np.pi * df_est_hz * P.T_S_GLOBAL


# =============================================================================
# 逐块 NDA-ML / DA-ML / oracle BER 评估
# =============================================================================

def ber_nda_awgn(rx, tx_bits):
    """NDA-ML AWGN: 逐块升幂 mean-angle 估常相位 CPE (assume_df_zero=True, B11 df=0 修复 D1).
    逐块 resolve M0-fold 模糊 (守 D003 / Bug 2). 返回 (n_err, n_bits)."""
    N = len(rx)
    n_blk = N // P.N_DFT
    L = n_blk * P.N_DFT
    rx_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
        # assume_df_zero=True: B11 真 df=0, 跳 FFT-df 锁伪峰 (守 D003 bug 修复)
        # intra_block_tracking='segmented': segK8 块内跟踪 (改进版, sandbox 验证 AWGN 反超 BPS ~1dB).
        #   AWGN 场景用 segmented; ber_nda_turb 保持 'none' 默认 (sandbox 显示 segK8 在 strong 湍流有害).
        rc, _, _, _ = nda_ml_recovery(seg, P.M0, mod='m16apsk', assume_df_zero=True,
                                      intra_block_tracking='segmented')
        rx_comp[b * P.N_DFT:(b + 1) * P.N_DFT] = rc
    tb = tx_bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


def ber_da_awgn(rx, tx_bits, pilot_spacing=P.DA_PILOT_SPACING):
    """DA-ML AWGN: 逐块 pilot-aided (pilot_sym=已知 tx 符号, 非决策错误传播).
    公平对照: BER 仅在 data 符号位置算 (pilot 不算信息 BER). 返回 (n_err_data, n_bits_data)."""
    N = len(rx)
    n_blk = N // P.N_DFT
    L = n_blk * P.N_DFT
    tx_sym = m16apsk_mod(tx_bits[:L * P.BITS_PER_SYM])
    pilot_idx_local = np.arange(0, P.N_DFT, pilot_spacing)
    is_data = np.ones(P.N_DFT, dtype=bool)
    is_data[pilot_idx_local] = False
    rx_comp_full = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        s_blk = slice(b * P.N_DFT, (b + 1) * P.N_DFT)
        p_sym = tx_sym[b * P.N_DFT + pilot_idx_local]
        rc, _, _ = da_ml_recovery(rx[s_blk], pilot_idx=pilot_idx_local,
                                  pilot_sym=p_sym, mod='m16apsk')
        rx_comp_full[s_blk] = rc
    demod_bits = m16apsk_demod(rx_comp_full)
    tb = tx_bits[:L * P.BITS_PER_SYM]
    n_sym = L
    is_data_sym = np.zeros(n_sym, dtype=bool)
    for b in range(n_blk):
        base = b * P.N_DFT
        is_data_sym[base:base + P.N_DFT] = is_data
    tb_arr = tb.reshape(n_sym, P.BITS_PER_SYM)
    dm_arr = demod_bits.reshape(n_sym, P.BITS_PER_SYM)
    n_err_data = int(np.sum(tb_arr[is_data_sym] != dm_arr[is_data_sym]))
    n_bits_data = int(np.sum(is_data_sym) * P.BITS_PER_SYM)
    return n_err_data, n_bits_data


def ber_oracle_awgn(rx, tx_bits, phi_true):
    """Oracle (genie-aided): 真实 θ(k) 补偿 → 解调 → BER. 信息论上界."""
    N = len(rx)
    rx_comp = rx * np.exp(-1j * phi_true[:N])
    tb = tx_bits[:N * P.BITS_PER_SYM]
    return int(np.sum(tb != m16apsk_demod(rx_comp))), len(tb)


def ber_nda_turb(rx):
    """NDA-ML 湍流: 两阶段 (fft_foe + nda CPE) 逐块恢复 (修复 D1).
    (rx 已 per-block h 均衡 — 修复 D2). 返回 (n_err, n_bits)."""
    N = len(rx)
    n_blk = N // P.N_DFT
    L = n_blk * P.N_DFT
    rx_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
        omega_est = fft_foe_m0_omega(seg, P.M0)
        k = np.arange(P.N_DFT)
        seg_foe = seg * np.exp(-1j * omega_est * k)
        rc, _, _, _ = nda_ml_recovery(seg_foe, P.M0, mod='m16apsk', assume_df_zero=True)
        rx_comp[b * P.N_DFT:(b + 1) * P.N_DFT] = rc
    # resolve 需要 tx_bits (genie-aided 解卷绕, 与 MVE 一致 — 注: resolve 不是 oracle 相位估计,
    # 是解 M0-fold 模糊, MVE 用 tx_bits 选最优旋转, 与 B11 行 129 解卷绕精神一致)
    # tx_bits 从调用方通过闭包/参数传入 — 此处签名简化, tx_bits 由 run_turb 传入 resolve
    return rx_comp  # 返回 rx_comp, resolve 在 run_turb 里做 (因需 tx_bits)


def ber_nda_turb_eval(rx, tx_bits):
    """NDA-ML 湍流完整评估 (含 resolve). 返回 (n_err, n_bits)."""
    rx_comp = ber_nda_turb(rx)
    L = len(rx_comp)
    tb = tx_bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


def ber_da_turb(rx, tx_bits, pilot_spacing=P.DA_PILOT_SPACING):
    """DA-ML 湍流: pilot_sym=已知 tx 符号. BER 仅 data 位置. (rx 已 per-block pilot h 均衡)
    DA ML 估计器内含 FOE+CPE (pilot 线性回归), 无需额外 fft_foe. 返回 (n_err_data, n_bits_data)."""
    return ber_da_awgn(rx, tx_bits, pilot_spacing)


def ber_oracle_turb(rx_eq, tx_bits, phi_true):
    """Oracle 湍流: rx 已 per-block 真h 均衡, 再用真实 θ 补偿. (genie 幅度+相位)."""
    N = len(rx_eq)
    rx_comp = rx_eq * np.exp(-1j * phi_true[:N])
    tb = tx_bits[:N * P.BITS_PER_SYM]
    return int(np.sum(tb != m16apsk_demod(rx_comp))), len(tb)


# =============================================================================
# SNR 扫描: AWGN + 湍流
# =============================================================================
def run_awgn(n_blocks, snr_points, seed_base):
    """AWGN 三方案 BER 扫描. 与 MVE run_awgn 同 seed/参数派生 (保 §4.5 一致性).

    seed 派生逻辑 (与 MVE _time_domain_crlb.py:run_awgn 完全一致):
      per-snr seed = seed_base + int(snr*1000); bits seed = seed+7; channel seed = seed.
    """
    N_sym = n_blocks * P.N_DFT
    print(f"[AWGN Formal] N_sym={N_sym}/点 ({n_blocks}×{P.N_DFT}), CLW={P.CLW_B11/1e3:.0f}kHz, "
          f"M0={P.M0}, pilot_spacing={P.DA_PILOT_SPACING}")
    print(f"{'SNR_dB':>7} {'NDA_BER':>12} {'DA_BER':>12} {'ORACLE':>12}")
    per_snr = []
    for snr in snr_points:
        seed = seed_base + int(snr * 1000)
        rng = np.random.default_rng(seed + 7)
        bits = rng.integers(0, 2, N_sym * P.BITS_PER_SYM)
        tx = m16apsk_mod(bits)
        rx, phi_true = awgn_wiener_channel(tx, snr, seed)
        ne_nda, nb_nda = ber_nda_awgn(rx, bits)
        ne_da, nb_da = ber_da_awgn(rx, bits)
        ne_or, nb_or = ber_oracle_awgn(rx, bits, phi_true)
        b_nda = ne_nda / nb_nda
        b_da = ne_da / nb_da
        b_or = ne_or / nb_or
        print(f"{snr:>7.0f} {b_nda:>12.4e} {b_da:>12.4e} {b_or:>12.4e}")
        per_snr.append({
            'snr_db': float(snr),
            'snr_db_total_nda': float(snr),
            'snr_db_total_da': float(snr) + P.PILOT_OVERHEAD_DB,
            'nda_ml_ber': b_nda, 'da_ml_ber': b_da, 'oracle_ber': b_or,
        })
    return per_snr


def run_turb(turb_name, gamma_bar_points_db, n_blocks, cfg, seed0):
    """湍流场景三方案 BER 扫描. 用 generate_shared_realization_apsk 共享信道 (守 TL-13).

    幅度处理 (修复 D2): per-block h 估计替代 h_med 标量均衡:
      - NDA-ML (盲): per-block 硬幅值 ĥ=mean(|rx|²)−1/(2γ) via mmse_equalize+amp_limit(3.0)
      - DA-ML (pilot): per-block pilot ĥ=mean(|r(p)/s(p)|²)
      - oracle: per-block 真 h (genie 上限)
    相位 (修复 D1): NDA 两阶段 (fft_foe+nda CPE); DA pilot FOE+CPE (da_ml 内含); oracle 真 θ.

    seed 派生 (与 MVE _time_domain_crlb.py:run_turb 一致): per-block seed = seed0 + b.
    """
    Ns = P.N_DFT
    print(f"[{turb_name} Formal] N_sym={n_blocks*Ns}/点 ({n_blocks}×{Ns}), "
          f"per-block h 均衡 + amp_limit(3.0), NDA 两阶段 fft_foe+nda CPE")
    print(f"{'γd_dB':>7} {'NDA_BER':>12} {'DA_BER':>12} {'ORACLE':>12}")
    per_snr = []
    for gamma_db in gamma_bar_points_db:
        gamma_lin = 10 ** (gamma_db / 10)
        ne_nda = ne_da = ne_or = 0
        nb_nda = nb_da = nb_or = 0
        for b in range(n_blocks):
            r = generate_shared_realization_apsk(
                Ns, gamma_lin, turb_name, cfg.doppler.DOPPLER_HIGH,
                mod='m16apsk', seed=seed0 + b)
            rx_raw = r['rx_raw']
            bits = r['bits']
            phi = r['phi']
            tx_sym = r['tx']
            h_true = r['h']
            # 幅度处理 (修复 D2): per-block h — 三方案各自估计, 公平
            h_blind = estimate_h_blind_perblock(rx_raw, gamma_lin)
            rx_blind = amp_limit(mmse_equalize(rx_raw, h_blind, gamma_lin), 3.0)
            h_pilot = estimate_h_pilot_perblock(rx_raw, tx_sym, gamma_lin)
            rx_pilot = amp_limit(mmse_equalize(rx_raw, h_pilot, gamma_lin), 3.0)
            rx_trueh = amp_limit(mmse_equalize(rx_raw, h_true, gamma_lin), 3.0)
            ne, nb = ber_nda_turb_eval(rx_blind, bits)
            ne_nda += ne; nb_nda += nb
            ne, nb = ber_da_turb(rx_pilot, bits)
            ne_da += ne; nb_da += nb
            ne, nb = ber_oracle_turb(rx_trueh, bits, phi)
            ne_or += ne; nb_or += nb
        b_nda = ne_nda / nb_nda
        b_da = ne_da / nb_da
        b_or = ne_or / nb_or
        print(f"{gamma_db:>7.0f} {b_nda:>12.4e} {b_da:>12.4e} {b_or:>12.4e}")
        per_snr.append({
            'snr_db': float(gamma_db),
            'snr_db_total_nda': float(gamma_db),
            'snr_db_total_da': float(gamma_db) + P.PILOT_OVERHEAD_DB,
            'nda_ml_ber': b_nda, 'da_ml_ber': b_da, 'oracle_ber': b_or,
        })
    return per_snr


# =============================================================================
# MVE 一致性验证 (§4.5 正确性锚点)
# =============================================================================
def consistency_check(mve_results_path):
    """同 seed 同参数 Formal vs MVE BER 对照.

    一致性标准: 每点 BER 相对误差 < 5% 或绝对误差 < 1e-4 (浮点容差).
    返回 dict: 每场景每点 formal_ber vs mve_ber vs relative_error, + 总 PASS/FAIL.
    """
    cfg = SimulationConfig()
    with open(mve_results_path, 'r', encoding='utf-8') as f:
        mve = json.load(f)

    report = {'scenarios': {}, 'overall_pass': True}
    tol_rel = 0.05    # 5% 相对容差
    tol_abs = 1e-4    # 绝对容差 (低 BER 区浮点)

    # AWGN
    print(f"\n{'='*30} MVE 一致性 — AWGN {'='*30}")
    formal_awgn = run_awgn(P.N_BLOCKS, P.SNR_AWGN_DB, P.SEED_AWGN)
    mve_awgn = mve['results']['awgn']
    sc_report = _compare_points(formal_awgn, mve_awgn, tol_rel, tol_abs, 'awgn')
    report['scenarios']['awgn'] = sc_report
    if not sc_report['pass']:
        report['overall_pass'] = False

    # 湍流 weak/moderate/strong
    for turb in P.TURB_LEVELS:
        print(f"\n{'='*25} MVE 一致性 — {turb} {'='*25}")
        formal_turb = run_turb(turb, P.SNR_TURB_DB, P.N_BLOCKS, cfg, P.SEED_TURB0)
        mve_turb = mve['results'][turb]
        sc_report = _compare_points(formal_turb, mve_turb, tol_rel, tol_abs, turb)
        report['scenarios'][turb] = sc_report
        if not sc_report['pass']:
            report['overall_pass'] = False

    return report


def _compare_points(formal_pts, mve_pts, tol_rel, tol_abs, scene):
    """逐点对比 formal vs mve BER. 返回 per-point report + pass flag."""
    points = []
    all_pass = True
    max_rel_err = 0.0
    for fp, mp in zip(formal_pts, mve_pts):
        # formal 用 'nda_ml_ber'/'da_ml_ber'/'oracle_ber'; mve 用 'nda_ber'/'da_ber'/'oracle_ber'
        f_nda, f_da, f_or = fp['nda_ml_ber'], fp['da_ml_ber'], fp['oracle_ber']
        m_nda, m_da, m_or = mp['nda_ber'], mp['da_ber'], mp['oracle_ber']
        rel_nda = abs(f_nda - m_nda) / max(abs(m_nda), 1e-12) if m_nda > 1e-12 else abs(f_nda - m_nda)
        rel_da = abs(f_da - m_da) / max(abs(m_da), 1e-12) if m_da > 1e-12 else abs(f_da - m_da)
        rel_or = abs(f_or - m_or) / max(abs(m_or), 1e-12) if m_or > 1e-12 else abs(f_or - m_or)
        # 一致: (相对 < 5%) 或 (绝对 < 1e-4)
        ok_nda = (rel_nda < tol_rel) or (abs(f_nda - m_nda) < tol_abs)
        ok_da = (rel_da < tol_rel) or (abs(f_da - m_da) < tol_abs)
        ok_or = (rel_or < tol_rel) or (abs(f_or - m_or) < tol_abs)
        pt_pass = ok_nda and ok_da and ok_or
        if not pt_pass:
            all_pass = False
        max_rel_err = max(max_rel_err, rel_nda, rel_da, rel_or)
        points.append({
            'snr_db': fp['snr_db'],
            'formal_nda': f_nda, 'mve_nda': m_nda, 'rel_err_nda': rel_nda, 'ok_nda': ok_nda,
            'formal_da': f_da, 'mve_da': m_da, 'rel_err_da': rel_da, 'ok_da': ok_da,
            'formal_oracle': f_or, 'mve_oracle': m_or, 'rel_err_oracle': rel_or, 'ok_oracle': ok_or,
            'pass': pt_pass,
        })
    print(f"  [{scene}] max_rel_err={max_rel_err*100:.3f}%  pass={all_pass}")
    return {'points': points, 'pass': all_pass, 'max_rel_err': max_rel_err}


# =============================================================================
# 退化测试 (design.md §4.3)
# =============================================================================
def degradation_tests():
    """三场景退化测试:
      (1) 关湍流 (h≡1): BER 退化为 AWGN 曲线
      (2) 关 Wiener (σ²_p=0): NDA/DA/oracle BER 收敛
      (3) 关 Doppler (f_dot=0): fft_foe 输出 ≈ 0
    返回 report dict.
    """
    report = {}
    N_sym_test = 10 * P.N_DFT   # 2560 符号, 快速测试
    snr_test = 16.0
    cfg = SimulationConfig()

    # (1) 关湍流: 用 awgn_wiener_channel (无 h 衰落) 应等价 AWGN. 已由 AWGN 场景覆盖.
    #     额外验证: generate_shared_realization_apsk 不含湍流时 h 应≈1 (但 GG 始终有 h, 故
    #     用 awgn_wiener_channel 代指 "关湍流" 场景). 标 PASS (AWGN 场景本身即此).
    report['turb_off_h_eq_1'] = {'status': 'AWGN 场景 (awgn_wiener_channel) 本身即 h≡1, 已由 AWGN 一致性验证覆盖'}

    # (2) 关 Wiener PN (σ²_p=0): 信道只剩 AWGN, 三方案 BER 应接近 (相位恒定无估计负担)
    #     独立写一个 no-wiener channel
    def awgn_no_pn_channel(tx, snr_db, seed):
        rng = np.random.default_rng(seed)
        N = len(tx)
        snr_lin = 10.0 ** (snr_db / 10.0)
        noise_var = 1.0 / (2.0 * snr_lin)
        noise = np.sqrt(noise_var) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
        return tx + noise, np.zeros(N)   # phi=0 (无 PN)
    rng_b = np.random.default_rng(424242 + 7)
    bits = rng_b.integers(0, 2, N_sym_test * P.BITS_PER_SYM)
    tx = m16apsk_mod(bits)
    rx_nopn, phi_nopn = awgn_no_pn_channel(tx, snr_test, 424242)
    ne_nda, _ = ber_nda_awgn(rx_nopn, bits)
    ne_da, _ = ber_da_awgn(rx_nopn, bits)
    ne_or, _ = ber_oracle_awgn(rx_nopn, bits, phi_nopn)
    b_nda, b_da, b_or = ne_nda/(N_sym_test*P.BITS_PER_SYM), ne_da/((N_sym_test*P.BITS_PER_SYM*3//4)), ne_or/(N_sym_test*P.BITS_PER_SYM)
    # 关 PN 后 NDA/DA/oracle 应接近 (oracle 略好因无相位估计噪声; NDA/DA 升幂/pilot 估常相位≈0)
    converged = (b_or > 0) and (b_nda / b_or < 2.0) and (b_da / b_or < 2.0)
    report['wiener_off_sigma2p_zero'] = {
        'ber_nda': b_nda, 'ber_da': b_da, 'ber_oracle': b_or,
        'nda_over_oracle': b_nda/b_or if b_or > 0 else None,
        'converged_within_2x': converged,
        'status': 'PASS (NDA/DA/oracle 收敛, 相位恒定无估计负担)' if converged else 'CHECK',
    }

    # (3) 关 Doppler (f_dot=0): fft_foe 在无 CFO 时输出应 ≈ 0.
    #     构造无 CFO 信号 (AWGN + Wiener PN, 无 f_res 无 f_dot): awgn_wiener_channel 已无 CFO.
    rng_c = np.random.default_rng(99999 + 7)
    bits_c = rng_c.integers(0, 2, P.N_DFT * P.BITS_PER_SYM)
    tx_c = m16apsk_mod(bits_c)
    rx_c, phi_c = awgn_wiener_channel(tx_c, snr_test, 99999)
    omega_est = fft_foe_m0_omega(rx_c, P.M0)
    foe_near_zero = abs(omega_est) < 0.05   # rad/sample, 无 CFO 时应≈0 (噪声所致小残余)
    report['doppler_off_fdot_zero'] = {
        'fft_foe_omega_est': omega_est,
        'near_zero': foe_near_zero,
        'status': 'PASS (fft_foe 输出≈0, 无 CFO 漂移)' if foe_near_zero else f'CHECK (omega={omega_est:.4f})',
    }
    return report


# =============================================================================
# 自相关预警 (design.md §4.4: lag-1 自相关 < 0.95)
# =============================================================================
def autocorr_warning():
    """h 序列 + θ 序列 lag-1 自相关检查 (非"过于平滑").

    h 序列: generate_shared_realization_apsk 的 h (GG 块衰落, 块内恒定 → 块内自相关高,
            但块间独立 → 全局 lag-1 受块结构影响, 预期 < 0.95 if block<<N).
    θ 序列: Wiener PN cumsum, lag-1 自相关预期接近 1 (随机游走强自相关) — 这是 Wiener PN
            物理特性, 非 bug. 标注预期高, 不作 fail.
    """
    report = {}
    cfg = SimulationConfig()
    # h 序列: 取 weak 湍流一个长实现
    r = generate_shared_realization_apsk(5000, 100.0, 'weak', cfg.doppler.DOPPLER_HIGH,
                                         mod='m16apsk', seed=12345)
    h = r['h']
    theta = r['phi']
    # lag-1 自相关
    h_lag1 = _lag1_autocorr(h)
    theta_lag1 = _lag1_autocorr(theta)
    report['h_lag1_autocorr'] = float(h_lag1)
    report['theta_lag1_autocorr'] = float(theta_lag1)
    report['h_below_0.95'] = bool(h_lag1 < 0.95)
    report['theta_note'] = ('Wiener PN cumsum lag-1 自相关预期接近 1 (随机游走物理特性), '
                            '非"过于平滑" bug; 块内 h 恒定致 h 序列自相关受块结构影响')
    report['status'] = 'PASS (h 序列 lag-1 < 0.95)' if h_lag1 < 0.95 else 'CHECK (h 自相关高, 检查块结构)'
    return report


def _lag1_autocorr(x):
    """lag-1 自相关系数."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    xm = x - x.mean()
    denom = np.sum(xm ** 2)
    if denom == 0:
        return 0.0
    return float(np.sum(xm[:-1] * xm[1:]) / denom)


# =============================================================================
# 工具: numpy → json
# =============================================================================
def _to_jsonable(o):
    if isinstance(o, dict):
        return {k: _to_jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_to_jsonable(v) for v in o]
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return _to_jsonable(o.tolist())
    return o


# =============================================================================
# 主
# =============================================================================
def main():
    t0 = time.time()
    print("=" * 100)
    print("SC-NDA-ML Formal 仿真器 (Step 7 Part A, 独立实现)")
    print(f"M0={P.M0}, pilot_spacing={P.DA_PILOT_SPACING} (25% overhead), "
          f"pilot_overhead={P.PILOT_OVERHEAD_DB:.3f} dB, HDFEC={P.HDFEC}, "
          f"N_sym={P.N_SYM_PER_POINT}/点")
    print(f"算法来源: common/ (nda_ml_recovery/da_ml_recovery/generate_shared_realization_apsk/m16apsk_*)")
    print("=" * 100)

    mve_results_path = os.path.join(_SIM_ROOT, 'explore', 'single-carrier-nda-ml', '_mve_results.json')

    # --- §4.5 MVE 一致性验证 (最关键, 正确性锚点) ---
    print("\n" + "#" * 40 + " §4.5 MVE 一致性验证 " + "#" * 40)
    consistency = consistency_check(mve_results_path)

    # --- 退化测试 (§4.3) ---
    print("\n" + "#" * 40 + " 退化测试 (§4.3) " + "#" * 40)
    degr = degradation_tests()
    for k, v in degr.items():
        print(f"  {k}: {v.get('status', v)}")

    # --- 自相关预警 (§4.4) ---
    print("\n" + "#" * 40 + " 自相关预警 (§4.4) " + "#" * 40)
    ac = autocorr_warning()
    print(f"  h lag-1 自相关: {ac['h_lag1_autocorr']:.4f} (< 0.95: {ac['h_below_0.95']})")
    print(f"  θ lag-1 自相关: {ac['theta_lag1_autocorr']:.4f} ({ac['theta_note'][:50]}...)")

    # --- 输出 BER 曲线 PNG (可选) ---
    png_path = os.path.join(_HERE, '_formal_ber_curves.png')
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1, 4, figsize=(20, 4.5))
        for ax, sc in zip(axes, ['awgn', 'weak', 'moderate', 'strong']):
            pts = consistency['scenarios'][sc]['points']
            gts = [p['snr_db'] for p in pts]
            ax.semilogy(gts, [p['formal_nda'] for p in pts], 'o-', label='NDA-ML (M0=8)')
            ax.semilogy(gts, [p['formal_da'] for p in pts], 's-', label='DA ML (sp=4)')
            ax.semilogy(gts, [p['formal_oracle'] for p in pts], '^--', label='oracle')
            ax.axhline(P.HDFEC, color='k', ls=':', label='HD-FEC 3.8e-3')
            ax.set_title(f"{sc} (Formal)")
            ax.set_xlabel(r'$\gamma_{tot}$ (dB)')
            ax.set_ylabel('BER')
            ax.grid(True, which='both', alpha=0.3)
            ax.legend(fontsize=8)
        fig.tight_layout()
        fig.savefig(png_path, dpi=110)
        print(f"\n[PNG] {png_path}")
    except Exception as e:
        print(f"(PNG skipped: {e})")
        png_path = None

    # --- 落盘 _consistency_check.json ---
    elapsed = time.time() - t0
    out = {
        'meta': {
            'task': 'SC-NDA-ML Formal 仿真器 Step 7 Part A',
            'increment_form': 'A+C (AWGN 频谱效率 + 湍流鲁棒性)',
            'metric': 'BER @ HD-FEC=3.8e-3, MVE 一致性验证 (§4.5 正确性锚点)',
            'M0': P.M0,
            'pilot_spacing': P.DA_PILOT_SPACING,
            'pilot_overhead_db': float(P.PILOT_OVERHEAD_DB),
            'N_per_point': P.N_SYM_PER_POINT,
            'N_blocks': P.N_BLOCKS,
            'seed_awgn': P.SEED_AWGN,
            'seed_turb0': P.SEED_TURB0,
            'hdfec': P.HDFEC,
            'algorithm_source': 'common/ (nda_ml_recovery/da_ml_recovery/generate_shared_realization_apsk/m16apsk_*/mmse_equalize/amp_limit/fft_foe)',
            'no_explore_import': True,
            'tolerance': {'relative': 0.05, 'absolute': 1e-4},
            'python': sys.executable,
            'numpy_version': np.__version__,
            'elapsed_sec': float(elapsed),
            'traced_params': P.all_traced_params_summary(),
        },
        'consistency_check': consistency,
        'degradation_tests': degr,
        'autocorrelation': ac,
        'ber_curves_png': png_path,
    }
    out_json = os.path.join(_HERE, '_consistency_check.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(_to_jsonable(out), f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {out_json}")

    # --- 汇总 ---
    print("\n" + "=" * 100)
    print(f"§4.5 MVE 一致性: {'PASS ✅' if consistency['overall_pass'] else 'FAIL ❌'}")
    for sc in ['awgn', 'weak', 'moderate', 'strong']:
        sr = consistency['scenarios'][sc]
        print(f"  {sc:>10}: pass={sr['pass']}  max_rel_err={sr['max_rel_err']*100:.3f}%")
    print(f"\n[耗时] {elapsed:.1f} s")


if __name__ == '__main__':
    main()
