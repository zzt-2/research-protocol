#!/usr/bin/env python3
"""湍流 FSO 载波同步仿真 — 公共基础设施

规格文档: SPEC.md（唯一真相源）

所有仿真脚本从此模块导入，确保：
1. 信号模型一致（TL-01）
2. 信道实现共享（TL-13）
3. KF 实现正确（TL-09: P 矩阵跨块传递）
4. 评估方法统一（默认 resolve_qpsk，因 VV/DPLL 有 π/2 模糊）

注意：VV/DPLL 使用 4 次方鉴相器，输出有 π/4 偏移 + π/2 模糊。
resolve_qpsk 通过试 8 个旋转解决此问题，是这些方法的必要配套。
ber_count 仅适用于 KF pilot（不做 4 次方，无相位模糊）。

使用方式：
  from common import *
"""

import numpy as np
from scipy.stats import gamma as gamma_dist
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, json, time, hashlib, subprocess, datetime

OUT = os.path.dirname(os.path.abspath(__file__))

# ═══════════════════════════════════════════════════════════════
# 系统参数（与 sim_ch4_kf_pilot_h.py 一致）
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

FIXED_CFG_OPTIMAL = {
    'weak':     {'N_fft': 1024, 'M_vv': 256, 'omega_n': 20e6, 'zeta': np.sqrt(2)/2},
    'moderate': {'N_fft': 1024, 'M_vv': 256, 'omega_n': 20e6, 'zeta': np.sqrt(2)/2},
    'strong':   {'N_fft': 2048, 'M_vv': 256, 'omega_n': 20e6, 'zeta': np.sqrt(2)/2},
}

GAMMA_BAR_DEFAULT = 100  # 20 dB

DEF_B_BPS = 32
DEF_NW_BPS = 61

# ═══════════════════════════════════════════════════════════════
# 信号原语
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

def ber_count(tx_bits, rx):
    return np.mean(tx_bits != qpsk_demod(rx))

def resolve_qpsk(rx, tx_bits):
    best = 1.0
    for r in np.arange(0, 2*np.pi, np.pi/4):
        b = ber_count(tx_bits, rx * np.exp(-1j*r))
        if b < best: best = b
    return best

def qam16_mod(bits):
    """16-QAM modulation: 4 bits/symbol, avg power normalized to 1.
    Gray mapping: 00→-3, 01→-1, 11→+1, 10→+3 per axis.
    """
    ns = len(bits) // 4
    bits = bits[:ns*4]
    bi = 2*bits[0::4] + bits[1::4]  # 2-bit I index
    bq = 2*bits[2::4] + bits[3::4]  # 2-bit Q index
    # Gray decode: 00→-3, 01→-1, 11→+1, 10→+3
    gray_map = np.array([-3, -1, +3, +1])
    si = gray_map[bi]
    sq = gray_map[bq]
    # Normalize: E[|s|²] = (9+1+1+9)/4 * 2 = 10, so divide by sqrt(10)
    return (si + 1j * sq) / np.sqrt(10)

def qam16_demod(s):
    """16-QAM demodulation with Gray mapping."""
    s = s * np.sqrt(10)  # undo normalization
    si = np.real(s)
    sq = np.imag(s)
    # Slice to {-3, -1, +1, +3}
    di = np.clip(np.round((si + 3) / 2) * 2 - 3, -3, 3).astype(int)
    dq = np.clip(np.round((sq + 3) / 2) * 2 - 3, -3, 3).astype(int)
    # Gray encode: -3→00, -1→01, +1→11, +3→10
    gray_enc = {-3: (0,0), -1: (0,1), 1: (1,1), 3: (1,0)}
    ns = len(s)
    bits = np.zeros(4*ns, dtype=int)
    for k in range(ns):
        b0, b1 = gray_enc.get(int(di[k]), (0,0))
        b2, b3 = gray_enc.get(int(dq[k]), (0,0))
        bits[4*k]   = b0
        bits[4*k+1] = b1
        bits[4*k+2] = b2
        bits[4*k+3] = b3
    return bits

def ber_count_qam16(tx_bits, rx):
    return np.mean(tx_bits != qam16_demod(rx))

def resolve_qam16(rx, tx_bits):
    """QAM16 resolve: try 8 π/4 rotations, pick lowest BER."""
    best = 1.0
    for r in np.arange(0, 2*np.pi, np.pi/4):
        b = ber_count_qam16(tx_bits, rx * np.exp(-1j*r))
        if b < best: best = b
    return best

def dpll_track_dd(rx, omega_n=8e6, zeta=np.sqrt(2)/2, mod='qpsk'):
    """DD (decision-directed) DPLL for QPSK and 16-QAM.
    Uses hard decision to remove modulation instead of 4th-power."""
    wT = min(omega_n * T_S, 0.5)
    c1 = 2 * zeta * wT
    c2 = wT**2
    N = len(rx)
    phi_est = np.zeros(N)
    integrator = 0.0
    vco_phase = 0.0
    for k in range(N):
        rotated = rx[k] * np.exp(-1j * vco_phase)
        # DD: hard decision
        if mod == 'qpsk':
            dec = (np.sign(np.real(rotated)) + 1j * np.sign(np.imag(rotated))) / np.sqrt(2)
        else:  # qam16
            s = rotated * np.sqrt(10)
            di = np.clip(np.round((np.real(s)+3)/2)*2-3, -3, 3)
            dq = np.clip(np.round((np.imag(s)+3)/2)*2-3, -3, 3)
            dec = (di + 1j * dq) / np.sqrt(10)
        # Phase error from decision
        pd_out = np.angle(rx[k] * np.exp(-1j * vco_phase) * np.conj(dec))
        integrator += c2 * pd_out
        freq_out = c1 * pd_out + integrator
        vco_phase += freq_out
        phi_est[k] = vco_phase
    return rx * np.exp(-1j * phi_est), phi_est

def ber_eval(tx_bits, rx, mode='direct'):
    """统一 BER 评估。

    mode='direct' (默认): 直接解调 ber_count — 公平，无 oracle
    mode='oracle': resolve_qpsk — 用 TX bits 选最优旋转（oracle 方法）
    """
    if mode == 'direct':
        return ber_count(tx_bits, rx)
    elif mode == 'oracle':
        return resolve_qpsk(rx, tx_bits)
    else:
        raise ValueError(f"Unknown mode: {mode}")

def amp_limit(rx, thresh=3.0):
    amp = np.abs(rx)
    mask = amp > thresh
    out = rx.copy()
    out[mask] = rx[mask] / amp[mask] * thresh
    return out

def hard_decision(z, mod='qpsk'):
    """Hard decision for QPSK or 16-QAM. Works with scalars and arrays."""
    if mod == 'qpsk':
        return (np.sign(np.real(z)) + 1j * np.sign(np.imag(z))) / np.sqrt(2)
    s = z * np.sqrt(10)
    di = np.clip(np.round((np.real(s) + 3) / 2) * 2 - 3, -3, 3)
    dq = np.clip(np.round((np.imag(s) + 3) / 2) * 2 - 3, -3, 3)
    return (di + 1j * dq) / np.sqrt(10)


def doppler_phase(N, f_res=F_RESIDUAL, f_dot=DOPPLER_HIGH, lw=LASER_LW):
    k = np.arange(N)
    phi_fo = 2 * np.pi * f_res * k * T_S
    phi_dot = np.pi * f_dot * (k * T_S)**2
    phi_laser = np.sqrt(2 * np.pi * lw * T_S) * np.cumsum(np.random.randn(N))
    return phi_fo + phi_dot + phi_laser

# ═══════════════════════════════════════════════════════════════
# 载波恢复基线
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
    pe = np.unwrap(np.angle(avg)) / M
    return rx * np.exp(-1j * pe), pe

def bps_cpr(rx, B=DEF_B_BPS, Nw=DEF_NW_BPS, mod='qpsk'):
    """Blind Phase Search (Pfau 2009, JLT)

    B 个测试相位，Nw 符号滑动窗口平均距离度量。
    使用 M=4 相位模糊展开解决 QPSK 模糊。
    mod: 'qpsk' or 'qam16' decision function.
    """
    N = len(rx)
    phases = 2 * np.pi * np.arange(B) / B

    # 向量化计算所有测试相位的距离度量
    rotated = rx[np.newaxis, :] * np.exp(-1j * phases[:, np.newaxis])
    dec = hard_decision(rotated, mod=mod)
    dist = np.abs(rotated - dec)**2
    metrics = dist / (np.abs(dec)**2 + 1e-10) if mod != 'qpsk' else dist

    # 滑动窗口平均
    ker = np.ones(Nw) / Nw
    for b in range(B):
        metrics[b] = np.convolve(metrics[b], ker, mode='same')

    best_b = np.argmin(metrics, axis=0)
    pe_raw = phases[best_b]

    # M=4 相位模糊展开：乘 4 → unwrap 2π 跳变 → 除 4
    pe = np.unwrap(4 * pe_raw) / 4

    return rx * np.exp(-1j * pe), pe

def carrier_recovery_fixed(rx, cfg=None):
    if cfg is None:
        cfg = FIXED_CFG
    fo_est = fft_foe(rx, N_fft=cfg['N_fft'])
    rx_comp = rx * np.exp(-1j * fo_est * np.arange(len(rx)))
    rx_pll, _ = dpll_track(rx_comp, omega_n=cfg['omega_n'], zeta=cfg['zeta'])
    rx_cpr, _ = vv_cpr(rx_pll, Nw=cfg['M_vv'])
    return rx_cpr

# ═══════════════════════════════════════════════════════════════
# Kalman 滤波器
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

def kf_unified(rx_block, h_block, gamma_bar, Q, phi_init=None,
               df_init=0.0, P_init=None, mod='qpsk'):
    """2状态KF（单块），P 跨块传递（TL-09）"""
    N = len(rx_block)
    F = np.array([[1.0, T_S], [0.0, 1.0]])
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
        s_hat = hard_decision(rx_rotated, mod=mod)
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
PILOT_PATTERN = np.array([
    ( 1 + 1j) / np.sqrt(2),
    ( 1 - 1j) / np.sqrt(2),
    (-1 + 1j) / np.sqrt(2),
    (-1 - 1j) / np.sqrt(2),
])

def get_pilots(n_pilots):
    return PILOT_PATTERN[np.arange(n_pilots) % len(PILOT_PATTERN)]

# ═══════════════════════════════════════════════════════════════
# [TL-13 修复] 共享信道生成
# ═══════════════════════════════════════════════════════════════
def generate_shared_realization(Ns, gamma_bar, turb_name, f_dot, seed=42):
    """
    生成单次信道/噪声/相位实现，所有方案共享。

    Returns:
        dict: rx_raw, bits, tx, h, h_blocks, h_med, phi,
              Ns, gamma_bar, turb_name, f_dot
    """
    np.random.seed(seed)
    a, b = TURB[turb_name]

    bits = np.random.randint(0, 2, Ns * 2)
    tx = qpsk_mod(bits)

    h = gg_block(Ns, a, b)
    n_blocks = Ns // BLOCK
    h_blocks = np.array([h[i * BLOCK] for i in range(n_blocks)])
    h_med = np.median(h_blocks)

    phi = doppler_phase(Ns, f_res=F_RESIDUAL, f_dot=f_dot)
    carrier = np.exp(1j * phi)

    signal = tx * np.sqrt(h) * carrier
    noise_var = 1.0 / (2 * gamma_bar)
    noise = np.sqrt(noise_var) * (np.random.randn(Ns) + 1j*np.random.randn(Ns))
    rx_raw = signal + noise

    return {
        'rx_raw': rx_raw, 'bits': bits, 'tx': tx,
        'h': h, 'h_blocks': h_blocks, 'h_med': h_med, 'phi': phi,
        'Ns': Ns, 'gamma_bar': gamma_bar,
        'turb_name': turb_name, 'f_dot': f_dot,
    }


def insert_pilots(shared, n_pilots_per_block=5):
    """
    在共享实现上插入导频。不重新生成信道/噪声/相位。

    返回 pilot 版本的 rx_raw、导频/数据索引、数据比特。
    """
    rx_raw = shared['rx_raw']
    tx = shared['tx'].copy()
    bits = shared['bits']
    h = shared['h']
    phi = shared['phi']
    gamma_bar = shared['gamma_bar']
    Ns = shared['Ns']
    n_blocks = Ns // BLOCK

    known_pilots = get_pilots(n_pilots_per_block)
    pilot_indices = []
    data_indices = []

    for b in range(n_blocks):
        base = b * BLOCK
        for p in range(n_pilots_per_block):
            idx = base + p
            tx[idx] = known_pilots[p % len(known_pilots)]
            pilot_indices.append(idx)
        for d in range(n_pilots_per_block, BLOCK):
            data_indices.append(base + d)

    pilot_indices = np.array(pilot_indices)
    data_indices = np.array(data_indices)

    # 重建 rx（替换导频位置的发符号，噪声/信道/相位不变）
    carrier = np.exp(1j * phi)
    noise = rx_raw - shared['tx'] * np.sqrt(h) * carrier
    signal_pilot = tx * np.sqrt(h) * carrier
    rx_pilot = signal_pilot + noise

    # 数据比特
    data_bits = np.zeros(len(data_indices) * 2, dtype=int)
    for i, idx in enumerate(data_indices):
        data_bits[2*i] = bits[2*idx]
        data_bits[2*i+1] = bits[2*idx+1]

    return rx_pilot, pilot_indices, data_indices, data_bits


def mmse_equalize(rx, h, gamma_bar):
    """MMSE 均衡，h 可为标量或向量"""
    return rx * np.sqrt(h) / (h + 1/gamma_bar)


def equalize_oracle(shared):
    """oracle h 均衡"""
    return amp_limit(mmse_equalize(shared['rx_raw'], shared['h'], shared['gamma_bar']), 3.0)

def equalize_hmed(shared):
    """h_med 均衡（公平）"""
    return amp_limit(mmse_equalize(shared['rx_raw'], shared['h_med'], shared['gamma_bar']), 3.0)

# ═══════════════════════════════════════════════════════════════
# KF 载波恢复变体
# ═══════════════════════════════════════════════════════════════
def kf_oracle_recovery(rx, h, gamma_bar, turb_name, f_dot=DOPPLER_HIGH,
                       Q_fine_df=(50e3)**2, mod='qpsk'):
    """KF oracle-h：逐块真实 h"""
    N = len(rx)
    k = np.arange(N)
    fo_est = fft_foe(rx, N_fft=min(N, 4096), nfft_zp=8192)
    rx_foc = rx * np.exp(-1j * fo_est * k)

    n_blocks = N // BLOCK
    Q = design_Q(turb_name, f_dot)
    Q_fine = Q.copy()
    Q_fine[1, 1] = Q_fine_df * T_S**2

    phi_full = np.zeros(N)
    prev_df = 0.0
    prev_P = None

    for i in range(n_blocks):
        s, e = i*BLOCK, (i+1)*BLOCK
        h_val = h[s]
        phi_init = phi_full[s-1] if i > 0 else None
        phi_est, df_est, P_final = kf_unified(
            rx_foc[s:e], h_val, gamma_bar, Q_fine,
            phi_init=phi_init, df_init=prev_df, P_init=prev_P, mod=mod)
        phi_full[s:e] = phi_est
        prev_df = df_est
        prev_P = P_final

    return rx_foc * np.exp(-1j * phi_full)


def kf_frame_h_recovery(rx, h_med, gamma_bar, turb_name, f_dot=DOPPLER_HIGH,
                        Q_fine_df=(50e3)**2, mod='qpsk'):
    """KF frame-level h"""
    N = len(rx)
    k = np.arange(N)
    fo_est = fft_foe(rx, N_fft=min(N, 4096), nfft_zp=8192)
    rx_foc = rx * np.exp(-1j * fo_est * k)

    n_blocks = N // BLOCK
    Q = design_Q(turb_name, f_dot)
    Q_fine = Q.copy()
    Q_fine[1, 1] = Q_fine_df * T_S**2

    h_val = max(h_med, 0.01)
    phi_full = np.zeros(N)
    prev_df = 0.0
    prev_P = None

    for i in range(n_blocks):
        s, e = i*BLOCK, (i+1)*BLOCK
        phi_init = phi_full[s-1] if i > 0 else None
        phi_est, df_est, P_final = kf_unified(
            rx_foc[s:e], h_val, gamma_bar, Q_fine,
            phi_init=phi_init, df_init=prev_df, P_init=prev_P, mod=mod)
        phi_full[s:e] = phi_est
        prev_df = df_est
        prev_P = P_final

    return rx_foc * np.exp(-1j * phi_full)


def kf_pilot_recovery(rx, gamma_bar, turb_name, n_pilots, h_med,
                      f_dot=DOPPLER_HIGH, block_size=BLOCK,
                      alpha_ema=0.5, Q_fine_df=(50e3)**2, mod='qpsk'):
    """导频辅助 KF 载波恢复"""
    N = len(rx)
    k = np.arange(N)
    fo_est = fft_foe(rx, N_fft=min(N, 4096), nfft_zp=8192)
    rx_foc = rx * np.exp(-1j * fo_est * k)

    n_blocks = N // block_size
    Q = design_Q(turb_name, f_dot)
    Q_fine = Q.copy()
    Q_fine[1, 1] = Q_fine_df * T_S**2

    F_mat = np.array([[1.0, T_S], [0.0, 1.0]])
    H_mat = np.array([[1.0, 0.0]])

    x = np.array([0.0, 0.0])
    P = np.diag([(np.pi/4)**2, (2*np.pi*100e3)**2])

    h_est = max(h_med, 0.01)
    h_est_prev = h_est
    h_est_per_block = np.zeros(n_blocks)

    corrected = np.zeros(N, dtype=complex)
    known_pilots = get_pilots(n_pilots)

    for b in range(n_blocks):
        start = b * block_size
        end = start + block_size
        pilot_end = start + n_pilots

        # 阶段1: 导频
        for k_idx in range(start, pilot_end):
            x_pred = F_mat @ x
            P_pred = F_mat @ P @ F_mat.T + Q_fine
            R_val = 1.0 / (2 * gamma_bar * max(h_est, 0.01))
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

        # 阶段2: 估计 h
        pilot_residuals = corrected[start:pilot_end]
        s_pilots = known_pilots[:n_pilots]
        h_est_raw = abs(np.mean(pilot_residuals * np.conj(s_pilots)))**2
        h_est = alpha_ema * h_est_raw + (1 - alpha_ema) * h_est_prev
        h_est = max(h_est, 0.01)
        h_est_prev = h_est
        h_est_per_block[b] = h_est

        # 阶段3: 数据（判决导引）
        for k_idx in range(pilot_end, end):
            R_val = 1.0 / (2 * gamma_bar * max(h_est, 0.01))
            x_pred = F_mat @ x
            P_pred = F_mat @ P @ F_mat.T + Q_fine
            rx_rotated = rx_foc[k_idx] * np.exp(-1j * x_pred[0])
            s_hat = hard_decision(rx_rotated, mod=mod)
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

    # 剩余符号
    rem_start = n_blocks * block_size
    if rem_start < N:
        for k_idx in range(rem_start, N):
            R_val = 1.0 / (2 * gamma_bar * max(h_est, 0.01))
            x_pred = F_mat @ x
            P_pred = F_mat @ P @ F_mat.T + Q_fine
            rx_rotated = rx_foc[k_idx] * np.exp(-1j * x_pred[0])
            s_hat = hard_decision(rx_rotated, mod=mod)
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
# 便捷函数：在共享实现上跑各方案
# ═══════════════════════════════════════════════════════════════
def run_fixed(shared, eq_mode='oracle'):
    """Fixed 基线（FOE+DPLL+VV）"""
    if eq_mode == 'oracle':
        rx_eq = equalize_oracle(shared)
    else:
        rx_eq = equalize_hmed(shared)
    return carrier_recovery_fixed(rx_eq)


def run_kf_oracle(shared, eq_mode='oracle', **kf_kwargs):
    """KF oracle-h"""
    if eq_mode == 'oracle':
        rx_eq = equalize_oracle(shared)
    else:
        rx_eq = equalize_hmed(shared)
    return kf_oracle_recovery(rx_eq, shared['h'], shared['gamma_bar'],
                              shared['turb_name'], shared['f_dot'], **kf_kwargs)


def run_kf_frame_h(shared, eq_mode='oracle', **kf_kwargs):
    """KF frame-level h"""
    if eq_mode == 'oracle':
        rx_eq = equalize_oracle(shared)
    else:
        rx_eq = equalize_hmed(shared)
    return kf_frame_h_recovery(rx_eq, shared['h_med'], shared['gamma_bar'],
                               shared['turb_name'], shared['f_dot'], **kf_kwargs)


def run_kf_pilot(shared, n_pilots=5, eq_mode='oracle', **kf_kwargs):
    """KF pilot-h（导频辅助）"""
    rx_pilot, pilot_idx, data_idx, data_bits = insert_pilots(shared, n_pilots)
    if eq_mode == 'oracle':
        rx_eq = amp_limit(mmse_equalize(rx_pilot, shared['h'], shared['gamma_bar']), 3.0)
    else:
        rx_eq = amp_limit(mmse_equalize(rx_pilot, shared['h_med'], shared['gamma_bar']), 3.0)
    corrected, h_est = kf_pilot_recovery(
        rx_eq, shared['gamma_bar'], shared['turb_name'], n_pilots,
        shared['h_med'], shared['f_dot'], **kf_kwargs)
    return corrected, data_idx, data_bits, h_est


def run_bps(shared, eq_mode='oracle'):
    """BPS 载波恢复（FOE + BPS）"""
    if eq_mode == 'oracle':
        rx_eq = equalize_oracle(shared)
    else:
        rx_eq = equalize_hmed(shared)
    fo_est = fft_foe(rx_eq)
    k = np.arange(len(rx_eq))
    rx_foc = rx_eq * np.exp(-1j * fo_est * k)
    rx_cpr, _ = bps_cpr(rx_foc)
    return rx_cpr


# ═══════════════════════════════════════════════════════════════
# 辅助
# ═══════════════════════════════════════════════════════════════
def db_ratio(a, b):
    if a > 0 and b > 0:
        return 10 * np.log10(a / b)
    return 0.0

def run_trial_shared(Ns, gamma_bar, turb_name, f_dot, seed,
                     schemes=None, n_pilots=5, eq_mode='oracle',
                     eval_mode='oracle'):
    """
    单次试验：共享信道，多方案对比。

    schemes: list of 'fixed', 'kf_oracle', 'kf_frame', 'kf_pilot'
    eval_mode: 'direct' (ber_count, 公平) 或 'oracle' (resolve_qpsk)
    Returns: dict {scheme: BER}
    """
    if schemes is None:
        schemes = ['fixed', 'kf_oracle', 'kf_frame', 'kf_pilot']

    shared = generate_shared_realization(Ns, gamma_bar, turb_name, f_dot, seed)
    results = {}

    if 'fixed' in schemes:
        rx_fixed = run_fixed(shared, eq_mode)
        results['fixed'] = ber_eval(shared['bits'], rx_fixed, mode=eval_mode)

    if 'kf_oracle' in schemes:
        rx_kf_or = run_kf_oracle(shared, eq_mode)
        results['kf_oracle'] = ber_eval(shared['bits'], rx_kf_or, mode=eval_mode)

    if 'kf_frame' in schemes:
        rx_kf_fr = run_kf_frame_h(shared, eq_mode)
        results['kf_frame'] = ber_eval(shared['bits'], rx_kf_fr, mode=eval_mode)

    if 'kf_pilot' in schemes:
        corrected, data_idx, data_bits, _ = run_kf_pilot(shared, n_pilots, eq_mode)
        results['kf_pilot'] = ber_eval(data_bits, corrected[data_idx], mode=eval_mode)

    if 'bps' in schemes:
        rx_bps = run_bps(shared, eq_mode)
        results['bps'] = ber_eval(shared['bits'], rx_bps, mode=eval_mode)

    return results


def save_results(data, filepath, script_name):
    """保存结果 JSON 并自动注入元数据（TL-25 rule 6）。

    Args:
        data: 要保存的 dict（会被原地修改，加入 _meta 键）
        filepath: 输出路径（如 'results/sweep.json'）
        script_name: 脚本名（如 'multi_seed_sweep'）
    """
    with open(__file__, 'rb') as f:
        chash = hashlib.md5(f.read()).hexdigest()[:8]
    try:
        commit = subprocess.run(
            ['git', 'rev-parse', '--short', 'HEAD'],
            capture_output=True, text=True, cwd=os.path.dirname(__file__)
        ).stdout.strip()
    except Exception:
        commit = 'unknown'
    data['_meta'] = {
        'script': script_name,
        'common_md5': chash,
        'git_commit': commit,
        'timestamp': datetime.datetime.now().isoformat(timespec='seconds'),
    }
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Results saved to {filepath} [common@{chash}, git@{commit}]")
