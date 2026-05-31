#!/usr/bin/env python3
"""Ch4 KF载波同步 — 导频辅助逐块h估计实验

测试 KF 载波同步在导频辅助(per-block pilot h estimation)下的性能，
对比 oracle h（上界）、帧级 h（下界）和 DD-h（判决导引）。

核心思想：
  DD 判决导引在深衰落块发生正向反馈崩溃（判决错误 -> h 高估 -> KF 发散）。
  导频符号已知，不依赖判决，无反馈循环。

导频模式：
  每块 100 符号，前 P 个为导频（已知 QPSK），后 (100-P) 个为数据。
  测试 5%/10%/20% 三种导频开销。

BER 只统计数据符号，不统计导频符号。

自包含脚本，不修改任何已有文件。
"""

import numpy as np
from scipy.stats import gamma as gamma_dist
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, time, json

OUT = os.path.dirname(os.path.abspath(__file__))
np.random.seed(42)
plt.rcParams.update({'font.size': 9, 'figure.dpi': 120})

# ═══════════════════════════════════════════════════════════════
# 系统参数
# ═══════════════════════════════════════════════════════════════
R_SYM = 2.5e9
T_S = 1 / R_SYM
F_CARRIER = 1.55e14
LASER_LW = 10e3

TURB = {
    'weak':     (4.0, 3.0),
    'moderate': (2.5, 1.8),
    'strong':   (1.5, 0.8),
}
BLOCK = 100

DOPPLER_HIGH = 150e6
DOPPLER_LOW  = 30e6
F_RESIDUAL   = 1e6

FIXED_CFG = {
    'N_fft': 1024,
    'M_vv': 64,
    'omega_n': 8e6,
    'zeta': np.sqrt(2)/2,
}

GAMMA_BAR = 100  # SNR=20dB

# ═══════════════════════════════════════════════════════════════
# 基础原语
# ═══════════════════════════════════════════════════════════════
def gg_block(N, a, b, bs=BLOCK):
    nb = (N + bs - 1) // bs
    return np.repeat(
        gamma_dist.rvs(a, scale=1/a, size=nb) *
        gamma_dist.rvs(b, scale=1/b, size=nb),
        bs)[:N]

def qpsk_mod(bits):
    return ((2*bits[0::2]-1) + 1j*(2*bits[1::2]-1)) / np.sqrt(2)

def qpsk_demod(s):
    b = np.zeros(2*len(s), dtype=int)
    b[0::2] = (np.real(s) > 0).astype(int)
    b[1::2] = (np.imag(s) > 0).astype(int)
    return b

def ber(tx_bits, rx):
    return np.mean(tx_bits != qpsk_demod(rx))

def resolve_qpsk(rx, tx_bits):
    best = 1.0
    for r in np.arange(0, 2*np.pi, np.pi/4):
        b = ber(tx_bits, rx * np.exp(-1j*r))
        if b < best: best = b
    return best

def amp_limit(rx, thresh=3.0):
    amp = np.abs(rx)
    mask = amp > thresh
    out = rx.copy()
    out[mask] = rx[mask] / amp[mask] * thresh
    return out

def doppler_phase(N, f_res=F_RESIDUAL, f_dot=DOPPLER_HIGH, lw=LASER_LW):
    k = np.arange(N)
    phi_fo = 2 * np.pi * f_res * k * T_S
    phi_dot = np.pi * f_dot * (k * T_S)**2
    phi_laser = np.sqrt(2 * np.pi * lw * T_S) * np.cumsum(np.random.randn(N))
    return phi_fo + phi_dot + phi_laser

# ═══════════════════════════════════════════════════════════════
# 基线载波恢复
# ═══════════════════════════════════════════════════════════════
def fft_foe(rx, N_fft=1024, nfft_zp=8192):
    N_fft = min(N_fft, len(rx))
    seg = rx[:N_fft]
    r4 = seg**4
    win = np.hanning(N_fft)
    r4w = r4 * win
    R4 = np.fft.fftshift(np.fft.fft(r4w, n=nfft_zp))
    freqs = np.fft.fftshift(np.fft.fftfreq(nfft_zp, d=1))
    idx = np.argmax(np.abs(R4))
    if 1 <= idx < len(R4) - 1:
        a_v, b_v, g_v = np.abs(R4[idx-1]), np.abs(R4[idx]), np.abs(R4[idx+1])
        if b_v - a_v > 0 and b_v + a_v - 2*g_v != 0:
            p = 0.5 * (a_v - g_v) / (a_v - 2*b_v + g_v)
            f_est_norm = (freqs[idx] + p * (freqs[1] - freqs[0]))
        else:
            f_est_norm = freqs[idx]
    else:
        f_est_norm = freqs[idx]
    f_est_norm /= 4
    return 2 * np.pi * f_est_norm

def dpll_track(rx, omega_n=8e6, zeta=np.sqrt(2)/2):
    wT = min(omega_n * T_S, 0.5)
    c1 = 2 * zeta * wT
    c2 = wT**2
    N = len(rx)
    phi_est = np.zeros(N)
    integrator = 0.0
    vco_phase = 0.0
    for k in range(N):
        mixed = rx[k] * np.exp(-1j * vco_phase)
        m4 = mixed**4
        pd_out = np.angle(m4) / 4
        integrator += c2 * pd_out
        freq_out = c1 * pd_out + integrator
        vco_phase += freq_out
        phi_est[k] = vco_phase
    return rx * np.exp(-1j * phi_est), phi_est

def vv_cpr(rx, Nw=64):
    M = 4
    raised = rx**M
    amp = np.abs(raised)
    mask = amp > 1e8
    if np.any(mask):
        raised[mask] = raised[mask] / amp[mask] * 1e8
    ker = np.ones(Nw) / Nw
    avg = np.convolve(raised, ker, mode='same')
    pe = np.unwrap(np.angle(avg) * M) / M
    return rx * np.exp(-1j * pe), pe

def carrier_recovery_fixed(rx, cfg=FIXED_CFG):
    fo_est = fft_foe(rx, N_fft=cfg['N_fft'])
    rx_comp = rx * np.exp(-1j * fo_est * np.arange(len(rx)))
    rx_pll, _ = dpll_track(rx_comp, omega_n=cfg['omega_n'], zeta=cfg['zeta'])
    rx_cpr, _ = vv_cpr(rx_pll, Nw=cfg['M_vv'])
    return rx_cpr

# ═══════════════════════════════════════════════════════════════
# KF 相关
# ═══════════════════════════════════════════════════════════════
SIGMA2_LASER = 2 * np.pi * LASER_LW * T_S

Q_TURB_PARAMS = {
    'weak':     {'sigma2_turb': 1e-6,  'kappa': 1.56e-6},
    'moderate': {'sigma2_turb': 1e-4,  'kappa': 9.80e-5},
    'strong':   {'sigma2_turb': 1e-3,  'kappa': 3.79e-4},
}

def design_Q(turb_name='strong', f_dot=DOPPLER_HIGH):
    sigma2_turb = Q_TURB_PARAMS[turb_name]['sigma2_turb']
    sigma2_df = (f_dot * T_S)**2 / 3
    sigma2_phi = SIGMA2_LASER + sigma2_turb
    Q = np.diag([sigma2_phi, sigma2_df])
    return Q

def kf_unified(rx_block, h_block, gamma_bar, Q, phi_init=None, df_init=0.0, P_init=None):
    """2状态KF统一载波同步（单块内运行）"""
    N = len(rx_block)
    F = np.array([[1.0, T_S],
                  [0.0, 1.0]])
    H = np.array([[1.0, 0.0]])

    if phi_init is None:
        if N >= 16:
            _, pe_vv = vv_cpr(rx_block, Nw=min(N, 16))
            phi_init = pe_vv[0]
        else:
            phi_init = np.angle(rx_block[0]**4) / 4

    x = np.array([phi_init, df_init])
    if P_init is not None:
        P = P_init.copy()
    else:
        P = np.diag([(np.pi/4)**2, (2*np.pi*100e3)**2])

    phi_est = np.zeros(N)

    for k in range(N):
        x_pred = F @ x
        P_pred = F @ P @ F.T + Q

        rx_rotated = rx_block[k] * np.exp(-1j * x_pred[0])
        s_hat = ((np.sign(np.real(rx_rotated))) + 1j * (np.sign(np.imag(rx_rotated)))) / np.sqrt(2)

        y = rx_block[k] * np.conj(s_hat)
        z_obs = np.angle(y)

        innov = z_obs - x_pred[0]
        innov = (innov + np.pi) % (2*np.pi) - np.pi

        R = 1.0 / (2 * gamma_bar * h_block)

        S = H @ P_pred @ H.T + R
        K = P_pred @ H.T / S

        x = x_pred + K.flatten() * innov
        x[0] = (x[0] + np.pi) % (2*np.pi) - np.pi

        P = (np.eye(2) - K @ H) @ P_pred

        phi_est[k] = x[0]

    return phi_est, x[1], P

# ═══════════════════════════════════════════════════════════════
# 导频图案
# ═══════════════════════════════════════════════════════════════
# 交替 QPSK 符号，避免直流偏置
# 4 种导频符号循环: (1+1j), (1-1j), (-1+1j), (-1-1j) / sqrt(2)
PILOT_PATTERN = np.array([
    ( 1 + 1j) / np.sqrt(2),
    ( 1 - 1j) / np.sqrt(2),
    (-1 + 1j) / np.sqrt(2),
    (-1 - 1j) / np.sqrt(2),
])

def get_pilots(n_pilots):
    """获取 n_pilots 个导频符号（循环图案）"""
    return PILOT_PATTERN[np.arange(n_pilots) % len(PILOT_PATTERN)]

# ═══════════════════════════════════════════════════════════════
# 含导频的信号生成
# ═══════════════════════════════════════════════════════════════
def generate_frame_with_pilots(N_total, gamma_bar, turb_name, f_dot, n_pilots_per_block=10):
    """生成含导频的帧信号

    每块: n_pilots 个导频 + (BLOCK - n_pilots) 个数据
    信道 h 按块生成（块内恒定）

    Returns:
        rx_comp: MMSE均衡后的接收信号
        data_bits: 数据符号对应的发送比特（只含数据部分）
        data_indices: 数据符号在帧中的索引
        pilot_indices: 导频符号在帧中的索引
        h: 信道增益序列（per symbol）
        h_blocks: per-block h（标量，每块一个）
        h_med: 帧级 h 中位数
    """
    a, b = TURB[turb_name]
    n_blocks = N_total // BLOCK
    assert N_total == n_blocks * BLOCK, "N_total must be multiple of BLOCK"

    # 生成所有导频符号
    pilots_all = get_pilots(n_pilots_per_block)

    # 生成数据比特（每块 (BLOCK - n_pilots) 个数据符号 = 2*(BLOCK-n_pilots) 比特）
    n_data_per_block = BLOCK - n_pilots_per_block
    total_data_syms = n_blocks * n_data_per_block
    data_bits = np.random.randint(0, 2, total_data_syms * 2)
    data_syms = qpsk_mod(data_bits)

    # 组装完整帧
    tx_frame = np.zeros(N_total, dtype=complex)
    data_idx = 0  # 数据符号指针
    data_indices = []
    pilot_indices = []

    for b_idx in range(n_blocks):
        base = b_idx * BLOCK
        # 导频段
        for p in range(n_pilots_per_block):
            idx = base + p
            tx_frame[idx] = pilots_all[p]
            pilot_indices.append(idx)
        # 数据段
        for d in range(n_data_per_block):
            idx = base + n_pilots_per_block + d
            tx_frame[idx] = data_syms[data_idx]
            data_idx += 1
            data_indices.append(idx)

    data_indices = np.array(data_indices)
    pilot_indices = np.array(pilot_indices)

    # 信道: 按块生成，块内恒定
    h_raw = gg_block(N_total, a, b)
    # 提取 per-block h
    h_blocks = np.array([h_raw[b_idx * BLOCK] for b_idx in range(n_blocks)])
    h = h_raw.copy()

    # 载波相位
    phi = doppler_phase(N_total, f_res=F_RESIDUAL, f_dot=f_dot)
    carrier = np.exp(1j * phi)

    # 通过信道
    signal = tx_frame * np.sqrt(h) * carrier
    noise_var = 1.0 / (2 * gamma_bar)
    noise = np.sqrt(noise_var) * (np.random.randn(N_total) + 1j*np.random.randn(N_total))
    rx = signal + noise

    # MMSE均衡
    rx_comp = rx * np.sqrt(h) / (h + 1/gamma_bar)
    rx_comp = amp_limit(rx_comp, 3.0)

    # 帧级 h 中位数
    h_med = np.median(h_blocks)

    return rx_comp, data_bits, data_indices, pilot_indices, h, h_blocks, h_med

# ═══════════════════════════════════════════════════════════════
# KF oracle-h 载波恢复（上界参考）
# ═══════════════════════════════════════════════════════════════
def kf_carrier_recovery_oracle(rx, h, gamma_bar, turb_name, f_dot=DOPPLER_HIGH):
    """KF载波恢复：oracle h（逐块真实h）"""
    N = len(rx)
    k = np.arange(N)

    fo_est = fft_foe(rx, N_fft=min(N, 4096), nfft_zp=8192)
    rx_foc = rx * np.exp(-1j * fo_est * k)

    n_blocks = N // BLOCK
    Q = design_Q(turb_name, f_dot)
    Q_fine = Q.copy()
    Q_fine[1, 1] = (50e3 * T_S)**2

    phi_full = np.zeros(N)
    prev_df = 0.0
    prev_P = None

    for i in range(n_blocks):
        s, e = i*BLOCK, (i+1)*BLOCK
        h_val = h[s]
        phi_init = phi_full[s-1] if i > 0 else None
        phi_est, df_est, P_final = kf_unified(rx_foc[s:e], h_val, gamma_bar, Q_fine,
                                      phi_init=phi_init, df_init=prev_df, P_init=prev_P)
        phi_full[s:e] = phi_est
        prev_df = df_est
        prev_P = P_final

    rem = N % BLOCK
    if rem > 0:
        s = n_blocks * BLOCK
        h_val = h[s]
        phi_init = phi_full[s-1] if n_blocks > 0 else None
        phi_est, _, _ = kf_unified(rx_foc[s:], h_val, gamma_bar, Q_fine,
                                 phi_init=phi_init, df_init=prev_df, P_init=prev_P)
        phi_full[s:] = phi_est

    return rx_foc * np.exp(-1j * phi_full)

# ═══════════════════════════════════════════════════════════════
# KF frame-level h 载波恢复（下界参考）
# ═══════════════════════════════════════════════════════════════
def kf_carrier_recovery_frame_h(rx, h_est_frame, gamma_bar, turb_name, f_dot=DOPPLER_HIGH):
    """KF载波恢复：帧级 h_est（标量，所有块共用）"""
    N = len(rx)
    k = np.arange(N)

    fo_est = fft_foe(rx, N_fft=min(N, 4096), nfft_zp=8192)
    rx_foc = rx * np.exp(-1j * fo_est * k)

    n_blocks = N // BLOCK
    Q = design_Q(turb_name, f_dot)
    Q_fine = Q.copy()
    Q_fine[1, 1] = (50e3 * T_S)**2

    phi_full = np.zeros(N)
    prev_df = 0.0
    prev_P = None
    h_val = max(h_est_frame, 0.01)

    for i in range(n_blocks):
        s, e = i*BLOCK, (i+1)*BLOCK
        phi_init = phi_full[s-1] if i > 0 else None
        phi_est, df_est, P_final = kf_unified(rx_foc[s:e], h_val, gamma_bar, Q_fine,
                                      phi_init=phi_init, df_init=prev_df, P_init=prev_P)
        phi_full[s:e] = phi_est
        prev_df = df_est
        prev_P = P_final

    rem = N % BLOCK
    if rem > 0:
        s = n_blocks * BLOCK
        phi_init = phi_full[s-1] if n_blocks > 0 else None
        phi_est, _, _ = kf_unified(rx_foc[s:], h_val, gamma_bar, Q_fine,
                                 phi_init=phi_init, df_init=prev_df, P_init=prev_P)
        phi_full[s:] = phi_est

    return rx_foc * np.exp(-1j * phi_full)

# ═══════════════════════════════════════════════════════════════
# 核心新函数：导频辅助 KF 载波恢复
# ═══════════════════════════════════════════════════════════════
def kf_pilot_recovery(rx, gamma_bar, turb_name, n_pilots, h_med,
                      f_dot=DOPPLER_HIGH, block_size=BLOCK, alpha_ema=0.5):
    """导频辅助 KF 载波恢复

    每块:
      1. 前 n_pilots 个已知导频: 用上一块 h_est 设 R, KF 正常更新
      2. 从导频残余估计当前块 h
      3. 后 (block_size - n_pilots) 个数据符号: 用新 h_est 设 R, KF 判决导引

    Args:
        rx: 接收信号（已做 MMSE 均衡）
        gamma_bar: 平均SNR
        turb_name: 湍流等级
        n_pilots: 每块导频数
        h_med: 帧级 h 中位数（初始化用）
        f_dot: 多普勒率
        block_size: 块大小
        alpha_ema: h 平滑系数

    Returns:
        corrected: 相位补偿后的信号
        h_est_per_block: 每块估计的 h（用于诊断）
    """
    N = len(rx)
    k = np.arange(N)

    # 帧级 FFT-FOE 粗补偿
    fo_est = fft_foe(rx, N_fft=min(N, 4096), nfft_zp=8192)
    rx_foc = rx * np.exp(-1j * fo_est * k)

    n_blocks = N // block_size
    Q = design_Q(turb_name, f_dot)
    Q_fine = Q.copy()
    Q_fine[1, 1] = (50e3 * T_S)**2

    # KF 状态
    F_mat = np.array([[1.0, T_S],
                      [0.0, 1.0]])
    H_mat = np.array([[1.0, 0.0]])

    # 初始化
    x = np.array([0.0, 0.0])
    P = np.diag([(np.pi/4)**2, (2*np.pi*100e3)**2])
    initialized = False

    h_est = max(h_med, 0.01)  # 初始用帧级中位数
    h_est_prev = h_est
    h_est_per_block = np.zeros(n_blocks)

    corrected = np.zeros(N, dtype=complex)
    known_pilots = get_pilots(n_pilots)

    for b in range(n_blocks):
        start = b * block_size
        end = start + block_size

        # === 阶段1: 处理导频（已知符号） ===
        pilot_end = start + n_pilots
        for k_idx in range(start, pilot_end):
            # 预测
            x_pred = F_mat @ x
            P_pred = F_mat @ P @ F_mat.T + Q_fine

            # R 用上一块的 h_est
            R_val = 1.0 / (2 * gamma_bar * max(h_est, 0.01))

            # 已知导频符号 -> 精确观测
            s_p = known_pilots[k_idx - start]
            y = rx_foc[k_idx] * np.conj(s_p)
            z_obs = np.angle(y)

            innov = z_obs - x_pred[0]
            innov = (innov + np.pi) % (2*np.pi) - np.pi

            S = H_mat @ P_pred @ H_mat.T + R_val
            K_gain = P_pred @ H_mat.T / S

            x = x_pred + K_gain.flatten() * innov
            x[0] = (x[0] + np.pi) % (2*np.pi) - np.pi
            P = (np.eye(2) - K_gain @ H_mat) @ P_pred

            corrected[k_idx] = rx_foc[k_idx] * np.exp(-1j * x[0])

        # === 阶段2: 从导频残余估计 h ===
        pilot_residuals = corrected[start:pilot_end]
        s_pilots = known_pilots[:n_pilots]
        h_est_raw = abs(np.mean(pilot_residuals * np.conj(s_pilots)))**2
        h_est = alpha_ema * h_est_raw + (1 - alpha_ema) * h_est_prev
        h_est = max(h_est, 0.01)
        h_est_prev = h_est
        h_est_per_block[b] = h_est

        # === 阶段3: 处理数据符号（判决导引） ===
        for k_idx in range(pilot_end, end):
            # R 用当前块估计的 h
            R_val = 1.0 / (2 * gamma_bar * max(h_est, 0.01))

            # 预测
            x_pred = F_mat @ x
            P_pred = F_mat @ P @ F_mat.T + Q_fine

            # 判决导引
            rx_rotated = rx_foc[k_idx] * np.exp(-1j * x_pred[0])
            s_hat = ((np.sign(np.real(rx_rotated))) + 1j * (np.sign(np.imag(rx_rotated)))) / np.sqrt(2)

            y = rx_foc[k_idx] * np.conj(s_hat)
            z_obs = np.angle(y)

            innov = z_obs - x_pred[0]
            innov = (innov + np.pi) % (2*np.pi) - np.pi

            S = H_mat @ P_pred @ H_mat.T + R_val
            K_gain = P_pred @ H_mat.T / S

            x = x_pred + K_gain.flatten() * innov
            x[0] = (x[0] + np.pi) % (2*np.pi) - np.pi
            P = (np.eye(2) - K_gain @ H_mat) @ P_pred

            corrected[k_idx] = rx_foc[k_idx] * np.exp(-1j * x[0])

    # 处理剩余符号
    rem_start = n_blocks * block_size
    if rem_start < N:
        for k_idx in range(rem_start, N):
            R_val = 1.0 / (2 * gamma_bar * max(h_est, 0.01))
            x_pred = F_mat @ x
            P_pred = F_mat @ P @ F_mat.T + Q_fine
            rx_rotated = rx_foc[k_idx] * np.exp(-1j * x_pred[0])
            s_hat = ((np.sign(np.real(rx_rotated))) + 1j * (np.sign(np.imag(rx_rotated)))) / np.sqrt(2)
            y = rx_foc[k_idx] * np.conj(s_hat)
            z_obs = np.angle(y)
            innov = z_obs - x_pred[0]
            innov = (innov + np.pi) % (2*np.pi) - np.pi
            S = H_mat @ P_pred @ H_mat.T + R_val
            K_gain = P_pred @ H_mat.T / S
            x = x_pred + K_gain.flatten() * innov
            x[0] = (x[0] + np.pi) % (2*np.pi) - np.pi
            P = (np.eye(2) - K_gain @ H_mat) @ P_pred
            corrected[k_idx] = rx_foc[k_idx] * np.exp(-1j * x[0])

    return corrected, h_est_per_block

# ═══════════════════════════════════════════════════════════════
# 辅助：帧级 h 估计（无导频场景用）
# ═══════════════════════════════════════════════════════════════
def generate_signal_no_pilots(Ns, gamma_bar, turb_name, f_dot):
    """生成无导频信号（用于 Fixed 和 KF frame-h / oracle-h 基线）"""
    a, b = TURB[turb_name]
    bits = np.random.randint(0, 2, Ns*2)
    tx = qpsk_mod(bits)
    h = gg_block(Ns, a, b)
    phi = doppler_phase(Ns, f_res=F_RESIDUAL, f_dot=f_dot)
    carrier = np.exp(1j * phi)
    signal = tx * np.sqrt(h) * carrier
    noise_var = 1.0 / (2 * gamma_bar)
    noise = np.sqrt(noise_var) * (np.random.randn(Ns) + 1j*np.random.randn(Ns))
    rx = signal + noise
    rx_comp = rx * np.sqrt(h) / (h + 1/gamma_bar)
    rx_comp = amp_limit(rx_comp, 3.0)
    return rx_comp, bits, h, phi

def estimate_h_frame(h, Ns):
    n_blocks = Ns // BLOCK
    h_blocks = np.array([np.median(h[i*BLOCK:(i+1)*BLOCK]) for i in range(n_blocks)])
    return np.median(h_blocks)

# ═══════════════════════════════════════════════════════════════
# MMSE 均衡公平性实验 — 原始信号生成（不做均衡）
# ═══════════════════════════════════════════════════════════════
def generate_raw_signal_np(Ns, gamma_bar, turb_name, f_dot):
    """生成无导频原始信号（不做MMSE均衡），用于公平性实验

    Returns:
        rx_raw: 原始接收信号（未均衡）
        bits: 发送比特
        h: 信道增益序列
        h_blocks: per-block h
        h_med: 帧级 h 中位数
    """
    a, b = TURB[turb_name]
    n_blocks = Ns // BLOCK
    bits = np.random.randint(0, 2, Ns * 2)
    tx = qpsk_mod(bits)
    h = gg_block(Ns, a, b)
    h_blocks = np.array([h[i * BLOCK] for i in range(n_blocks)])
    h_med = np.median(h_blocks)

    carrier = np.exp(1j * doppler_phase(Ns, f_res=F_RESIDUAL, f_dot=f_dot))
    signal = tx * np.sqrt(h) * carrier
    noise_var = 1.0 / (2 * gamma_bar)
    noise = np.sqrt(noise_var) * (np.random.randn(Ns) + 1j * np.random.randn(Ns))
    rx_raw = signal + noise

    return rx_raw, bits, h, h_blocks, h_med


def generate_raw_signal_pilot(Ns, gamma_bar, turb_name, f_dot, n_pilots_per_block=10):
    """生成含导频原始信号（不做MMSE均衡），用于公平性实验

    Returns:
        rx_raw: 原始接收信号（未均衡）
        data_bits: 数据符号对应的发送比特
        data_indices: 数据符号索引
        pilot_indices: 导频符号索引
        h: 信道增益序列
        h_blocks: per-block h
        h_med: 帧级 h 中位数
    """
    a, b = TURB[turb_name]
    n_blocks = Ns // BLOCK
    assert Ns == n_blocks * BLOCK

    pilots_all = get_pilots(n_pilots_per_block)
    n_data_per_block = BLOCK - n_pilots_per_block
    total_data_syms = n_blocks * n_data_per_block
    data_bits = np.random.randint(0, 2, total_data_syms * 2)
    data_syms = qpsk_mod(data_bits)

    tx_frame = np.zeros(Ns, dtype=complex)
    data_idx = 0
    data_indices = []
    pilot_indices = []

    for b_idx in range(n_blocks):
        base = b_idx * BLOCK
        for p in range(n_pilots_per_block):
            idx = base + p
            tx_frame[idx] = pilots_all[p]
            pilot_indices.append(idx)
        for d in range(n_data_per_block):
            idx = base + n_pilots_per_block + d
            tx_frame[idx] = data_syms[data_idx]
            data_idx += 1
            data_indices.append(idx)

    data_indices = np.array(data_indices)
    pilot_indices = np.array(pilot_indices)

    h = gg_block(Ns, a, b)
    h_blocks = np.array([h[b_idx * BLOCK] for b_idx in range(n_blocks)])
    h_med = np.median(h_blocks)

    carrier = np.exp(1j * doppler_phase(Ns, f_res=F_RESIDUAL, f_dot=f_dot))
    signal = tx_frame * np.sqrt(h) * carrier
    noise_var = 1.0 / (2 * gamma_bar)
    noise = np.sqrt(noise_var) * (np.random.randn(Ns) + 1j * np.random.randn(Ns))
    rx_raw = signal + noise

    return rx_raw, data_bits, data_indices, pilot_indices, h, h_blocks, h_med


def mmse_equalize(rx, h_eq, gamma_bar):
    """MMSE均衡：h_eq 可以是标量或向量"""
    return rx * np.sqrt(h_eq) / (h_eq + 1 / gamma_bar)


# ═══════════════════════════════════════════════════════════════
# 主实验
# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    t0 = time.time()
    Ns = 10000  # 100 blocks * 100 symbols
    N_TRIALS = 30
    GAMMA_DB = 20
    F_DOT = DOPPLER_HIGH
    TURB_LIST = ['weak', 'moderate', 'strong']

    PILOT_CONFIGS = {
        'KF pilot 5%':  5,
        'KF pilot 10%': 10,
        'KF pilot 20%': 20,
    }

    # 所有方案（按输出顺序）
    SCHEMES = ['Fixed N=1024', 'KF frame-h', 'KF pilot 5%', 'KF pilot 10%', 'KF pilot 20%', 'KF oracle-h']

    print("=" * 80)
    print("Ch4 KF Pilot-Aided Per-Block h Estimation Experiment")
    print(f"  Ns={Ns}, trials={N_TRIALS}, SNR={GAMMA_DB}dB, f_dot={F_DOT/1e6:.0f}MHz/s")
    print(f"  BLOCK={BLOCK}, Pilot overheads: 5%/10%/20%")
    print(f"  BER counts DATA symbols only (pilots excluded)")
    print("=" * 80)

    all_ber = {s: {t: [] for t in TURB_LIST} for s in SCHEMES}
    # h estimation diagnostics (single trial, strong turbulence, 10% pilots)
    h_diag_true = None
    h_diag_est = None

    for turb in TURB_LIST:
        print(f"\n--- Turbulence: {turb} ---")
        for trial in range(N_TRIALS):
            trial_seed = 42 + trial

            # --- 无导频基线方案（共用同一信道实现） ---
            np.random.seed(trial_seed)
            rx_comp_np, bits_np, h_np, phi_np = generate_signal_no_pilots(
                Ns, GAMMA_BAR, turb, F_DOT)

            # 1. Fixed N=1024
            rx_fixed = carrier_recovery_fixed(rx_comp_np)
            all_ber['Fixed N=1024'][turb].append(resolve_qpsk(rx_fixed, bits_np))

            # 2. KF frame-level h
            h_med = estimate_h_frame(h_np, Ns)
            rx_kf_frame = kf_carrier_recovery_frame_h(rx_comp_np, h_med, GAMMA_BAR, turb, F_DOT)
            all_ber['KF frame-h'][turb].append(resolve_qpsk(rx_kf_frame, bits_np))

            # 3. KF oracle h
            rx_kf_oracle = kf_carrier_recovery_oracle(rx_comp_np, h_np, GAMMA_BAR, turb, F_DOT)
            all_ber['KF oracle-h'][turb].append(resolve_qpsk(rx_kf_oracle, bits_np))

            # --- 导频方案（每种开销独立生成含导频帧） ---
            for scheme_name, n_pilots in PILOT_CONFIGS.items():
                np.random.seed(trial_seed)
                rx_comp_p, data_bits_p, data_idx_p, pilot_idx_p, h_p, h_blocks_p, h_med_p = \
                    generate_frame_with_pilots(Ns, GAMMA_BAR, turb, F_DOT, n_pilots)

                rx_corrected, h_est_blocks = kf_pilot_recovery(
                    rx_comp_p, GAMMA_BAR, turb, n_pilots, h_med_p, F_DOT)

                # BER 只统计数据符号
                rx_data = rx_corrected[data_idx_p]
                data_ber = resolve_qpsk(rx_data, data_bits_p)
                all_ber[scheme_name][turb].append(data_ber)

                # 诊断：强湍流 + 10% 导频 + 第一次 trial
                if turb == 'strong' and n_pilots == 10 and trial == 0:
                    h_diag_true = h_blocks_p.copy()
                    h_diag_est = h_est_blocks.copy()

        for s in SCHEMES:
            mean_b = np.mean(all_ber[s][turb])
            print(f"    {s:20s}: BER={mean_b:.6f}")

    # ═══════════════════════════════════════════════════════════
    # Summary Table
    # ═══════════════════════════════════════════════════════════
    dt = time.time() - t0
    print(f"\n{'=' * 80}")
    print(f"SUMMARY ({dt:.1f}s)")
    print(f"{'=' * 80}")

    header = f"{'':20s} | {'Weak':>10s} | {'Moderate':>10s} | {'Strong':>10s}"
    sep = "-" * 20 + "-+-" + "-".join(["-" * 10] * 3)
    print(header)
    print(sep)

    mean_results = {}
    for s in SCHEMES:
        vals = [np.mean(all_ber[s][t]) for t in TURB_LIST]
        mean_results[s] = {t: v for t, v in zip(TURB_LIST, vals)}
        print(f"{s:20s} | {vals[0]:10.6f} | {vals[1]:10.6f} | {vals[2]:10.6f}")

    # Gain analysis
    def db_ratio(a, b):
        if a > 0 and b > 0:
            return 10 * np.log10(a / b)
        return 0.0

    print(f"\n{'=' * 80}")
    print("GAIN ANALYSIS")
    print(f"{'=' * 80}")

    for pilot_scheme in ['KF pilot 5%', 'KF pilot 10%', 'KF pilot 20%']:
        print(f"\n{pilot_scheme} vs baselines:")
        for turb in TURB_LIST:
            pilot_ber = mean_results[pilot_scheme][turb]
            frame_ber = mean_results['KF frame-h'][turb]
            oracle_ber = mean_results['KF oracle-h'][turb]
            fixed_ber = mean_results['Fixed N=1024'][turb]
            print(f"  {turb:10s}: vs Fixed={db_ratio(fixed_ber, pilot_ber):+.1f}dB  "
                  f"vs frame-h={db_ratio(frame_ber, pilot_ber):+.1f}dB  "
                  f"gap to oracle={db_ratio(pilot_ber, oracle_ber):.1f}dB")

    # ═══════════════════════════════════════════════════════════
    # Plot
    # ═══════════════════════════════════════════════════════════
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # --- 左图: BER 柱状图 ---
    colors = {
        'Fixed N=1024':  'steelblue',
        'KF frame-h':    'coral',
        'KF pilot 5%':   '#27ae60',
        'KF pilot 10%':  '#2ecc71',
        'KF pilot 20%':  '#1abc9c',
        'KF oracle-h':   '#9b59b6',
    }
    bar_labels = ['Fixed', 'KF\nframe-h', 'Pilot\n5%', 'Pilot\n10%', 'Pilot\n20%', 'KF\noracle-h']
    scheme_keys = list(colors.keys())

    ax0 = axes[0]
    n_schemes = len(scheme_keys)
    n_turbs = len(TURB_LIST)
    group_width = 0.8
    bar_width = group_width / n_schemes

    for ti, turb in enumerate(TURB_LIST):
        group_center = ti
        for si, s in enumerate(scheme_keys):
            x_pos = group_center - group_width/2 + (si + 0.5) * bar_width
            val = mean_results[s][turb]
            ax0.bar(x_pos, val, width=bar_width*0.9, color=colors[s],
                    edgecolor='white', linewidth=0.3)

    # 图例
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=colors[s], label=s) for s in scheme_keys]
    ax0.legend(handles=legend_elements, fontsize=7, loc='upper left')

    ax0.set_xticks(range(n_turbs))
    ax0.set_xticklabels([t.capitalize() for t in TURB_LIST])
    ax0.set_ylabel('BER')
    ax0.set_title('BER by Turbulence & Scheme')
    ax0.set_yscale('log')
    ax0.grid(True, alpha=0.3, axis='y')

    # 在每个湍流组上方标注最佳导频方案的 BER
    for ti, turb in enumerate(TURB_LIST):
        best_pilot = min(mean_results[s][turb] for s in ['KF pilot 5%', 'KF pilot 10%', 'KF pilot 20%'])
        oracle_ber = mean_results['KF oracle-h'][turb]
        ax0.text(ti, best_pilot * 0.5, f'{best_pilot:.4f}', ha='center', va='top', fontsize=7, color='green')

    # --- 右图: h 估计质量 scatter (strong turb, 10% pilots, trial 0) ---
    ax1 = axes[1]
    if h_diag_true is not None and h_diag_est is not None:
        ax1.scatter(h_diag_true, h_diag_est, alpha=0.6, s=20, color='#2ecc71', edgecolors='gray', linewidth=0.3)
        # 对角线参考
        lim_min = min(h_diag_true.min(), h_diag_est.min()) * 0.8
        lim_max = max(h_diag_true.max(), h_diag_est.max()) * 1.2
        ax1.plot([lim_min, lim_max], [lim_min, lim_max], 'k--', alpha=0.3, label='y=x')
        ax1.set_xlabel('h_true (per block)')
        ax1.set_ylabel('h_est (pilot-aided)')
        ax1.set_title('h Estimation: Pilot 10% (Strong turb, trial 0)')
        ax1.legend(fontsize=8)
        ax1.grid(True, alpha=0.3)
        # 相关系数
        corr = np.corrcoef(h_diag_true, h_diag_est)[0, 1]
        mse = np.mean((h_diag_true - h_diag_est)**2)
        ax1.text(0.05, 0.95, f'corr={corr:.3f}\nMSE={mse:.4f}',
                 transform=ax1.transAxes, va='top', fontsize=8,
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    fig.suptitle(f'KF Carrier Sync: Pilot-Aided h Estimation (SNR={GAMMA_DB}dB, {N_TRIALS} trials)',
                 fontsize=11)
    plt.tight_layout()
    plt.savefig(f'{OUT}/fig_ch4_kf_pilot_h.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\nPlot saved to {OUT}/fig_ch4_kf_pilot_h.png")

    # ═══════════════════════════════════════════════════════════
    # Save JSON
    # ═══════════════════════════════════════════════════════════
    save_data = {}
    for s in SCHEMES:
        save_data[s] = {t: float(np.mean(all_ber[s][t])) for t in TURB_LIST}
        save_data[f'{s}_per_trial'] = {t: [float(x) for x in all_ber[s][t]] for t in TURB_LIST}

    # h diagnostics
    if h_diag_true is not None:
        save_data['h_diag'] = {
            'h_true': [float(x) for x in h_diag_true],
            'h_est':  [float(x) for x in h_diag_est],
            'corr':   float(np.corrcoef(h_diag_true, h_diag_est)[0, 1]),
            'mse':    float(np.mean((h_diag_true - h_diag_est)**2)),
        }

    save_data['config'] = {
        'Ns': Ns,
        'n_trials': N_TRIALS,
        'gamma_db': GAMMA_DB,
        'f_dot': F_DOT,
        'block_size': BLOCK,
        'pilot_configs': {k: v for k, v in PILOT_CONFIGS.items()},
    }

    with open(f'{OUT}/results_ch4_kf_pilot_h.json', 'w') as f:
        json.dump(save_data, f, indent=2)
    print(f"Results saved to {OUT}/results_ch4_kf_pilot_h.json")

    print(f"\nTotal time: {dt:.1f}s")
    print("=" * 80)

    # ═════════════════════════════════════════════════════════════
    # MMSE 均衡公平性实验
    # ═════════════════════════════════════════════════════════════
    print("\n" + "=" * 80)
    print("MMSE EQUALIZATION FAIRNESS EXPERIMENT")
    print("  All schemes use SAME channel realization per trial.")
    print("  Fair configs use h_med for equalization (no oracle advantage).")
    print("=" * 80)

    FAIR_SCHEMES = ['Fixed fair', 'KF pilot fair', 'KF oracle R-only', 'KF oracle upper']
    fair_ber = {s: {t: [] for t in TURB_LIST} for s in FAIR_SCHEMES}

    t1 = time.time()

    for turb in TURB_LIST:
        print(f"\n--- Fairness Exp | Turbulence: {turb} ---")
        for trial in range(N_TRIALS):
            trial_seed = 42 + trial

            # --- 无导频原始信号（Fixed / oracle 用）---
            np.random.seed(trial_seed)
            rx_raw_np, bits_np, h_np, h_blocks_np, h_med_np = generate_raw_signal_np(
                Ns, GAMMA_BAR, turb, F_DOT)

            # --- 有导频原始信号（pilot 用）---
            np.random.seed(trial_seed)
            rx_raw_p, data_bits_p, data_idx_p, pilot_idx_p, h_p, h_blocks_p, h_med_p = \
                generate_raw_signal_pilot(Ns, GAMMA_BAR, turb, F_DOT, n_pilots_per_block=10)

            # --- Fixed fair: h_med 均衡 + 标准载波恢复 (VV+DPLL) ---
            rx_eq_fixed = mmse_equalize(rx_raw_np, h_med_np, GAMMA_BAR)
            rx_fixed = carrier_recovery_fixed(amp_limit(rx_eq_fixed, 3.0))
            fair_ber['Fixed fair'][turb].append(resolve_qpsk(rx_fixed, bits_np))

            # --- KF pilot fair: h_med 均衡 + pilot KF (pilot-estimated h for R) ---
            rx_eq_pilot = mmse_equalize(rx_raw_p, h_med_p, GAMMA_BAR)
            rx_corrected_p, _ = kf_pilot_recovery(
                amp_limit(rx_eq_pilot, 3.0), GAMMA_BAR, turb, 10, h_med_p, F_DOT)
            fair_ber['KF pilot fair'][turb].append(
                resolve_qpsk(rx_corrected_p[data_idx_p], data_bits_p))

            # --- KF oracle R-only: h_med 均衡 + oracle h for R matrix ---
            rx_eq_or = mmse_equalize(rx_raw_np, h_med_np, GAMMA_BAR)
            rx_oracle_r = kf_carrier_recovery_oracle(
                amp_limit(rx_eq_or, 3.0), h_np, GAMMA_BAR, turb, F_DOT)
            fair_ber['KF oracle R-only'][turb].append(resolve_qpsk(rx_oracle_r, bits_np))

            # --- KF oracle upper: true h 均衡 + oracle R (理论上界) ---
            rx_eq_upper = mmse_equalize(rx_raw_np, h_np, GAMMA_BAR)
            rx_oracle_upper = kf_carrier_recovery_oracle(
                amp_limit(rx_eq_upper, 3.0), h_np, GAMMA_BAR, turb, F_DOT)
            fair_ber['KF oracle upper'][turb].append(resolve_qpsk(rx_oracle_upper, bits_np))

        for s in FAIR_SCHEMES:
            mean_b = np.mean(fair_ber[s][turb])
            print(f"    {s:20s}: BER={mean_b:.6f}")

    dt_fair = time.time() - t1

    # ═════════════════════════════════════════════════════════════
    # Fairness Summary Tables
    # ═════════════════════════════════════════════════════════════
    print(f"\n{'=' * 80}")
    print(f"FAIRNESS SUMMARY ({dt_fair:.1f}s)")
    print(f"{'=' * 80}")

    # Table 1: Oracle equalization (existing results, for reference)
    print("\nTable 1: Oracle Equalization (existing results)")
    header = f"{'':20s} | {'Weak':>10s} | {'Moderate':>10s} | {'Strong':>10s}"
    sep = "-" * 20 + "-+-" + "-".join(["-" * 10] * 3)
    print(header)
    print(sep)
    for s in ['Fixed N=1024', 'KF pilot 10%', 'KF oracle-h']:
        vals = [np.mean(all_ber[s][t]) for t in TURB_LIST]
        print(f"{s:20s} | {vals[0]:10.6f} | {vals[1]:10.6f} | {vals[2]:10.6f}")

    # Table 2: h_med equalization (new results)
    print("\nTable 2: h_med Equalization (fair comparison)")
    print(header)
    print(sep)
    fair_mean = {}
    for s in FAIR_SCHEMES:
        vals = [np.mean(fair_ber[s][t]) for t in TURB_LIST]
        fair_mean[s] = {t: v for t, v in zip(TURB_LIST, vals)}
        print(f"{s:20s} | {vals[0]:10.6f} | {vals[1]:10.6f} | {vals[2]:10.6f}")

    # Table 3: Gain analysis (h_med equalization)
    print(f"\n{'=' * 80}")
    print("GAIN ANALYSIS (h_med equalization)")
    print(f"{'=' * 80}")
    for turb in TURB_LIST:
        pilot_ber = fair_mean['KF pilot fair'][turb]
        fixed_ber = fair_mean['Fixed fair'][turb]
        oracle_r_ber = fair_mean['KF oracle R-only'][turb]
        upper_ber = fair_mean['KF oracle upper'][turb]
        gain_vs_fixed = db_ratio(fixed_ber, pilot_ber)
        gain_oracle_r = db_ratio(oracle_r_ber, pilot_ber)
        gap_to_upper = db_ratio(pilot_ber, upper_ber)
        print(f"  {turb:10s}: pilot vs Fixed={gain_vs_fixed:+.1f}dB  "
              f"pilot vs oracle-R={gain_oracle_r:+.1f}dB  "
              f"gap to upper={gap_to_upper:.1f}dB")

    # ═════════════════════════════════════════════════════════════
    # Fairness Plot
    # ═════════════════════════════════════════════════════════════
    fig2, axes2 = plt.subplots(1, 2, figsize=(14, 5))

    # --- 左图: 公平性对比柱状图 ---
    fair_colors = {
        'Fixed fair':        'steelblue',
        'KF pilot fair':     '#2ecc71',
        'KF oracle R-only':  '#e67e22',
        'KF oracle upper':   '#9b59b6',
    }
    fair_bar_labels = list(fair_colors.keys())

    ax_f0 = axes2[0]
    n_fair = len(fair_bar_labels)
    group_width = 0.8
    bar_width = group_width / n_fair

    for ti, turb in enumerate(TURB_LIST):
        group_center = ti
        for si, s in enumerate(fair_bar_labels):
            x_pos = group_center - group_width / 2 + (si + 0.5) * bar_width
            val = fair_mean[s][turb]
            ax_f0.bar(x_pos, val, width=bar_width * 0.9, color=fair_colors[s],
                      edgecolor='white', linewidth=0.3)

    from matplotlib.patches import Patch
    legend_fair = [Patch(facecolor=fair_colors[s], label=s) for s in fair_bar_labels]
    ax_f0.legend(handles=legend_fair, fontsize=7, loc='upper left')
    ax_f0.set_xticks(range(len(TURB_LIST)))
    ax_f0.set_xticklabels([t.capitalize() for t in TURB_LIST])
    ax_f0.set_ylabel('BER')
    ax_f0.set_title('Fair Comparison (h_med equalization)')
    ax_f0.set_yscale('log')
    ax_f0.grid(True, alpha=0.3, axis='y')

    # --- 右图: Oracle vs Fair 对比 ---
    ax_f1 = axes2[1]
    compare_pairs = [
        ('Fixed N=1024', 'Fixed fair', 'Fixed'),
        ('KF pilot 10%', 'KF pilot fair', 'KF pilot'),
        ('KF oracle-h', 'KF oracle upper', 'KF oracle'),
    ]
    x_pos_arr = np.arange(len(TURB_LIST))
    width_c = 0.3
    for pi, (oracle_key, fair_key, label) in enumerate(compare_pairs):
        oracle_vals = [np.mean(all_ber[oracle_key][t]) for t in TURB_LIST]
        fair_vals = [fair_mean[fair_key][t] for t in TURB_LIST]
        offset = (pi - 1) * width_c * 2
        ax_f1.bar(x_pos_arr + offset - width_c / 2, oracle_vals, width_c,
                  alpha=0.7, color=['steelblue', '#2ecc71', '#9b59b6'][pi],
                  label=f'{label} (oracle eq)')
        ax_f1.bar(x_pos_arr + offset + width_c / 2, fair_vals, width_c,
                  alpha=0.7, color=['steelblue', '#2ecc71', '#9b59b6'][pi],
                  hatch='//', label=f'{label} (h_med eq)')

    ax_f1.set_xticks(x_pos_arr)
    ax_f1.set_xticklabels([t.capitalize() for t in TURB_LIST])
    ax_f1.set_ylabel('BER')
    ax_f1.set_title('Oracle vs h_med Equalization')
    ax_f1.set_yscale('log')
    ax_f1.legend(fontsize=6, ncol=2)
    ax_f1.grid(True, alpha=0.3, axis='y')

    fig2.suptitle(f'MMSE Equalization Fairness (SNR={GAMMA_DB}dB, {N_TRIALS} trials)',
                  fontsize=11)
    plt.tight_layout()
    plt.savefig(f'{OUT}/fig_ch4_fairness.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\nFairness plot saved to {OUT}/fig_ch4_fairness.png")

    # Save fairness results
    fair_save = {'config': {'equalization': 'fairness_experiment'}}
    for s in FAIR_SCHEMES:
        fair_save[s] = {t: float(np.mean(fair_ber[s][t])) for t in TURB_LIST}
        fair_save[f'{s}_per_trial'] = {t: [float(x) for x in fair_ber[s][t]] for t in TURB_LIST}
    with open(f'{OUT}/results_ch4_fairness.json', 'w') as f:
        json.dump(fair_save, f, indent=2)
    print(f"Fairness results saved to {OUT}/results_ch4_fairness.json")

    print(f"\nFairness experiment time: {dt_fair:.1f}s")
    print(f"Total script time: {time.time() - t0:.1f}s")
    print("=" * 80)
