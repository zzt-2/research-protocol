#!/usr/bin/env python3
"""Ch4 KF载波同步 — 逐块判决导引h估计实验

测试 KF 载波同步在逐块 DD (decision-directed) h 估计下的性能，
对比 oracle h（上界）和帧级 h（下界），分离 h 估计精度的影响。

实验设计：
  1. Fixed N=1024        — 基线
  2. KF frame-level h    — 帧级 h_est（已知较差）
  3. KF per-block DD h   — 逐块判决导引 h 估计（新实验）
  4. KF oracle h         — 逐块真实 h（上界参考）

自包含脚本，不修改任何已有文件。
基于 sim_ch4_kf_verification.py 的函数复写。
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
# 系统参数（与 sim_direction_a.py 一致）
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

# ═══════════════════════════════════════════════════════════════
# 基础原语（复写自 sim_ch4_kf_verification.py）
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
# 基线载波恢复（复写）
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

def carrier_recovery_fixed(rx, cfg=FIXED_CFG):
    fo_est = fft_foe(rx, N_fft=cfg['N_fft'])
    rx_comp = rx * np.exp(-1j * fo_est * np.arange(len(rx)))
    rx_pll, _ = dpll_track(rx_comp, omega_n=cfg['omega_n'], zeta=cfg['zeta'])
    rx_cpr, _ = vv_cpr(rx_pll, Nw=cfg['M_vv'])
    return rx_cpr

# ═══════════════════════════════════════════════════════════════
# KF 相关（复写）
# ═══════════════════════════════════════════════════════════════
SIGMA2_LASER = 2 * np.pi * LASER_LW * T_S

SIGMA2_DF_HIGH = (DOPPLER_HIGH * T_S)**2 / 3

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

def kf_unified(rx_block, h_block, gamma_bar, Q, phi_init=None, df_init=0.0):
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

    return phi_est, x[1]

# ═══════════════════════════════════════════════════════════════
# 信号生成（复写）
# ═══════════════════════════════════════════════════════════════
def generate_signal(Ns, turb_name, f_dot, gamma_bar_db):
    a, b = TURB[turb_name]
    gamma_bar = 10**(gamma_bar_db / 10)

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

# ═══════════════════════════════════════════════════════════════
# KF oracle h 载波恢复（复写）
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

    for i in range(n_blocks):
        s, e = i*BLOCK, (i+1)*BLOCK
        h_val = h[s]
        phi_init = phi_full[s-1] if i > 0 else None
        phi_est, df_est = kf_unified(rx_foc[s:e], h_val, gamma_bar, Q_fine,
                                      phi_init=phi_init, df_init=prev_df)
        phi_full[s:e] = phi_est
        prev_df = df_est

    rem = N % BLOCK
    if rem > 0:
        s = n_blocks * BLOCK
        h_val = h[s]
        phi_init = phi_full[s-1] if n_blocks > 0 else None
        phi_est, _ = kf_unified(rx_foc[s:], h_val, gamma_bar, Q_fine,
                                 phi_init=phi_init, df_init=prev_df)
        phi_full[s:] = phi_est

    return rx_foc * np.exp(-1j * phi_full)

# ═══════════════════════════════════════════════════════════════
# KF frame-level h 载波恢复（复写）
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
    h_val = max(h_est_frame, 0.01)

    for i in range(n_blocks):
        s, e = i*BLOCK, (i+1)*BLOCK
        phi_init = phi_full[s-1] if i > 0 else None
        phi_est, df_est = kf_unified(rx_foc[s:e], h_val, gamma_bar, Q_fine,
                                      phi_init=phi_init, df_init=prev_df)
        phi_full[s:e] = phi_est
        prev_df = df_est

    rem = N % BLOCK
    if rem > 0:
        s = n_blocks * BLOCK
        phi_init = phi_full[s-1] if n_blocks > 0 else None
        phi_est, _ = kf_unified(rx_foc[s:], h_val, gamma_bar, Q_fine,
                                 phi_init=phi_init, df_init=prev_df)
        phi_full[s:] = phi_est

    return rx_foc * np.exp(-1j * phi_full)

# ═══════════════════════════════════════════════════════════════
# 核心新函数：KF 逐块判决导引 h 估计载波恢复
# ═══════════════════════════════════════════════════════════════
WARMUP_BLOCKS = 3  # 前3块用帧级 h_med，之后切换到 DD h

def estimate_h_block_dd(rx_corrected, gamma_bar):
    """判决导引估计当前块的等效信道增益 h

    返回 (h_est, confidence):
    - h_est: 估计的 h
    - confidence: 判决置信度 [0,1]，用于混合策略
    """
    N = len(rx_corrected)
    # QPSK 判决
    s_hat = ((np.sign(np.real(rx_corrected))) + 1j * (np.sign(np.imag(rx_corrected)))) / np.sqrt(2)
    # 去调制后的残差
    residual = rx_corrected * np.conj(s_hat)
    mean_res = np.mean(residual)
    h_mmse_est = np.abs(mean_res)
    # 噪声方差估计
    noise_est = residual - mean_res
    noise_var = np.mean(np.abs(noise_est)**2)
    # 判决置信度：残差集中在正确星座点的程度
    # 理想 QPSK 判决正确时 residual ≈ constant + small noise
    # 判决错误时 residual 散布很大
    confidence = h_mmse_est**2 / (h_mmse_est**2 + noise_var + 1e-10)
    # SNR 估计
    if noise_var > 1e-10:
        snr_est = h_mmse_est**2 / noise_var
        h_est = snr_est / gamma_bar
    else:
        h_est = 1.0
    return max(h_est, 1e-4), float(confidence)

def kf_carrier_recovery_dd_h(rx, h_med_frame, gamma_bar, turb_name, f_dot=DOPPLER_HIGH):
    """KF载波恢复：逐块判决导引 h 估计

    流程：
    1. 帧级 FFT-FOE 粗补偿
    2. 逐块处理：
       - 用当前 h_est 设 R 矩阵，运行 KF
       - QPSK 判决得到 s_hat
       - DD 估计当前块 h（基于 SNR 估计）
       - 更新 h_est 供下一块使用
    3. 前 WARMUP_BLOCKS 块用帧级 h_med（避免初始发散）
    """
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
    h_dd_accum = max(h_med_frame, 0.01)  # DD 累积估计（warm-up 后才给 KF）
    h_med_safe = max(h_med_frame, 0.01)

    for i in range(n_blocks):
        s, e = i*BLOCK, (i+1)*BLOCK

        # Warm-up 块用帧级 h_med；之后用 DD 累积估计
        h_val = h_med_safe if i < WARMUP_BLOCKS else h_dd_accum

        phi_init = phi_full[s-1] if i > 0 else None
        phi_est, df_est = kf_unified(rx_foc[s:e], h_val, gamma_bar, Q_fine,
                                      phi_init=phi_init, df_init=prev_df)
        phi_full[s:e] = phi_est
        prev_df = df_est

        # DD h 估计：用 KF 补偿后的信号
        rx_corrected_block = rx_foc[s:e] * np.exp(-1j * phi_est)
        h_dd, confidence = estimate_h_block_dd(rx_corrected_block, gamma_bar)

        # 置信度加权：高置信度用 DD h，低置信度回退到帧级 h
        # confidence > 0.5 表示判决可靠，用 DD h
        # confidence <= 0.5 表示判决不可靠（深衰落或高噪声），用帧级 h
        h_dd_accum = confidence * h_dd + (1 - confidence) * h_med_safe

    rem = N % BLOCK
    if rem > 0:
        s = n_blocks * BLOCK
        phi_init = phi_full[s-1] if n_blocks > 0 else None
        phi_est, _ = kf_unified(rx_foc[s:], h_dd_accum, gamma_bar, Q_fine,
                                 phi_init=phi_init, df_init=prev_df)
        phi_full[s:] = phi_est

    return rx_foc * np.exp(-1j * phi_full)

# ═══════════════════════════════════════════════════════════════
# 辅助：帧级 h 估计
# ═══════════════════════════════════════════════════════════════
def estimate_h_frame(h, Ns):
    n_blocks = Ns // BLOCK
    h_blocks = np.array([np.median(h[i*BLOCK:(i+1)*BLOCK]) for i in range(n_blocks)])
    return np.median(h_blocks)

def diagnose_dd_h(rx_comp, h_true, h_med_frame, gamma_bar, turb_name, f_dot=DOPPLER_HIGH):
    """诊断 DD h 估计质量：比较 per-block h_true vs h_est(DD) vs h_med(frame)"""
    N = len(rx_comp)
    k = np.arange(N)

    fo_est = fft_foe(rx_comp, N_fft=min(N, 4096), nfft_zp=8192)
    rx_foc = rx_comp * np.exp(-1j * fo_est * k)

    n_blocks = N // BLOCK
    Q = design_Q(turb_name, f_dot)
    Q_fine = Q.copy()
    Q_fine[1, 1] = (50e3 * T_S)**2

    h_true_per_block = np.array([h_true[i*BLOCK] for i in range(n_blocks)])
    h_dd_per_block = np.zeros(n_blocks)
    h_dd_accum = max(h_med_frame, 0.01)
    h_med_safe = max(h_med_frame, 0.01)

    phi_full = np.zeros(N)
    prev_df = 0.0

    for i in range(n_blocks):
        s, e = i*BLOCK, (i+1)*BLOCK
        h_val = h_med_safe if i < WARMUP_BLOCKS else h_dd_accum

        phi_init = phi_full[s-1] if i > 0 else None
        phi_est, df_est = kf_unified(rx_foc[s:e], h_val, gamma_bar, Q_fine,
                                      phi_init=phi_init, df_init=prev_df)
        phi_full[s:e] = phi_est
        prev_df = df_est

        rx_corrected_block = rx_foc[s:e] * np.exp(-1j * phi_est)
        h_dd, confidence = estimate_h_block_dd(rx_corrected_block, gamma_bar)
        h_dd_per_block[i] = h_dd

        h_dd_accum = confidence * h_dd + (1 - confidence) * h_med_safe

    # 指标
    err_dd = np.mean(np.abs(h_dd_per_block - h_true_per_block)**2)
    err_frame = np.mean((h_med_safe - h_true_per_block)**2)
    corr_dd = np.corrcoef(h_dd_per_block, h_true_per_block)[0, 1]

    return {
        'h_true': h_true_per_block,
        'h_dd': h_dd_per_block,
        'h_frame': h_med_safe,
        'mse_dd': float(err_dd),
        'mse_frame': float(err_frame),
        'corr_dd': float(corr_dd),
    }

# ═══════════════════════════════════════════════════════════════
# 主实验
# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    t0 = time.time()
    Ns = 10000
    N_TRIALS = 30
    GAMMA_DB = 20
    F_DOT = DOPPLER_HIGH
    GAMMA_BAR = 10**(GAMMA_DB / 10)
    TURB_LIST = ['weak', 'moderate', 'strong']

    SCHEMES = ['Fixed N=1024', 'KF frame-h', 'KF DD-h', 'KF oracle-h']

    print("=" * 72)
    print("Ch4 KF Per-Block DD h Estimation Experiment")
    print(f"  Ns={Ns}, trials={N_TRIALS}, SNR={GAMMA_DB}dB, f_dot={F_DOT/1e6:.0f}MHz/s")
    print(f"  BLOCK={BLOCK}, WARMUP_BLOCKS={WARMUP_BLOCKS}")
    print("=" * 72)

    all_ber = {s: {t: [] for t in TURB_LIST} for s in SCHEMES}

    # DD h estimation quality diagnostics (single trial)
    dd_diagnostics = {}

    for turb in TURB_LIST:
        print(f"\n--- Turbulence: {turb} ---")
        for trial in range(N_TRIALS):
            np.random.seed(42 + trial)
            rx_comp, bits, h, phi_true = generate_signal(Ns, turb, F_DOT, GAMMA_DB)

            # 帧级 h 估计（基线方法）
            h_med = estimate_h_frame(h, Ns)

            # 1. Fixed N=1024
            rx_fixed = carrier_recovery_fixed(rx_comp)
            all_ber['Fixed N=1024'][turb].append(resolve_qpsk(rx_fixed, bits))

            # 2. KF frame-level h
            rx_kf_frame = kf_carrier_recovery_frame_h(rx_comp, h_med, GAMMA_BAR, turb, F_DOT)
            all_ber['KF frame-h'][turb].append(resolve_qpsk(rx_kf_frame, bits))

            # 3. KF per-block DD h (NEW)
            rx_kf_dd = kf_carrier_recovery_dd_h(rx_comp, h_med, GAMMA_BAR, turb, F_DOT)
            all_ber['KF DD-h'][turb].append(resolve_qpsk(rx_kf_dd, bits))

            # 4. KF oracle h (upper bound)
            rx_kf_oracle = kf_carrier_recovery_oracle(rx_comp, h, GAMMA_BAR, turb, F_DOT)
            all_ber['KF oracle-h'][turb].append(resolve_qpsk(rx_kf_oracle, bits))

            # Diagnostics on first trial: compare DD h estimate vs oracle h per block
            if trial == 0:
                dd_diag = diagnose_dd_h(rx_comp, h, h_med, GAMMA_BAR, turb)
                dd_diagnostics[turb] = dd_diag

        for s in SCHEMES:
            mean_b = np.mean(all_ber[s][turb])
            print(f"    {s:20s}: BER={mean_b:.6f}")

    # ═══════════════════════════════════════════════════════════
    # DD h Estimation Diagnostics
    # ═══════════════════════════════════════════════════════════
    print(f"\n{'=' * 72}")
    print("DD h ESTIMATION DIAGNOSTICS (trial 0)")
    print(f"{'=' * 72}")
    for turb in TURB_LIST:
        d = dd_diagnostics[turb]
        print(f"\n  {turb.upper()}:")
        print(f"    MSE(DD h vs true h):    {d['mse_dd']:.6f}")
        print(f"    MSE(frame h vs true h): {d['mse_frame']:.6f}")
        print(f"    Corr(DD h, true h):     {d['corr_dd']:.4f}")
        # Sample blocks: min, median, max of h_true
        h_true = d['h_true']
        h_dd = d['h_dd']
        for label, idx_fn in [('min h block', np.argmin), ('median h block', lambda x: np.argsort(x)[len(x)//2]),
                               ('max h block', np.argmax)]:
            idx = idx_fn(h_true)
            print(f"    {label:20s}: h_true={h_true[idx]:.4f}  h_dd={h_dd[idx]:.4f}  ratio={h_dd[idx]/max(h_true[idx],1e-6):.3f}")
        print(f"    frame h = {d['h_frame']:.4f}")
        print(f"    h_true range: [{h_true.min():.4f}, {h_true.max():.4f}], mean={h_true.mean():.4f}")
        print(f"    h_dd range:   [{h_dd.min():.4f}, {h_dd.max():.4f}], mean={h_dd.mean():.4f}")

    # ═══════════════════════════════════════════════════════════
    # Summary Table
    # ═══════════════════════════════════════════════════════════
    dt = time.time() - t0
    print(f"\n{'=' * 72}")
    print(f"SUMMARY ({dt:.1f}s)")
    print(f"{'=' * 72}")

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
    print(f"\n{'=' * 72}")
    print("GAIN ANALYSIS")
    print(f"{'=' * 72}")

    def db_ratio(a, b):
        if a > 0 and b > 0:
            return 10 * np.log10(a / b)
        return 0.0

    print("\nKF DD-h vs KF frame-h (DD estimation gain):")
    for turb in TURB_LIST:
        dd = mean_results['KF DD-h'][turb]
        fr = mean_results['KF frame-h'][turb]
        gain = db_ratio(fr, dd)
        print(f"  {turb:10s}: {gain:+.1f} dB")

    print("\nKF DD-h vs Fixed N=1024 (total KF gain with DD h):")
    for turb in TURB_LIST:
        dd = mean_results['KF DD-h'][turb]
        fix = mean_results['Fixed N=1024'][turb]
        gain = db_ratio(fix, dd)
        print(f"  {turb:10s}: {gain:+.1f} dB")

    print("\nKF DD-h vs KF oracle-h (gap to upper bound):")
    for turb in TURB_LIST:
        dd = mean_results['KF DD-h'][turb]
        ora = mean_results['KF oracle-h'][turb]
        gap = db_ratio(dd, ora)
        print(f"  {turb:10s}: gap={gap:.1f} dB")

    # ═══════════════════════════════════════════════════════════
    # Plot
    # ═══════════════════════════════════════════════════════════
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    colors = {
        'Fixed N=1024': 'steelblue',
        'KF frame-h':   'coral',
        'KF DD-h':      '#2ecc71',
        'KF oracle-h':  '#9b59b6',
    }

    bar_labels = ['Fixed', 'KF\nframe-h', 'KF\nDD-h', 'KF\noracle-h']
    scheme_keys = list(colors.keys())

    for ax, turb in zip(axes, TURB_LIST):
        vals = [mean_results[s][turb] for s in scheme_keys]
        x = np.arange(len(vals))
        bar_colors = [colors[s] for s in scheme_keys]

        bars = ax.bar(x, vals, color=bar_colors, width=0.6, edgecolor='white', linewidth=0.5)

        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.05,
                    f'{v:.5f}', ha='center', va='bottom', fontsize=7)

        ax.set_xticks(x)
        ax.set_xticklabels(bar_labels, fontsize=8)
        ax.set_ylabel('BER')
        ax.set_title(f'{turb.capitalize()} turbulence')
        ax.set_yscale('log')
        ax.set_ylim(ymax=max(vals) * 5)
        ax.grid(True, alpha=0.3, axis='y')

    fig.suptitle(f'KF Carrier Sync: Per-Block DD h Estimation (SNR={GAMMA_DB}dB, {N_TRIALS} trials)',
                 fontsize=11)
    plt.tight_layout()
    plt.savefig(f'{OUT}/fig_ch4_kf_perblock_h.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\nPlot saved to {OUT}/fig_ch4_kf_perblock_h.png")

    # Save JSON
    save_data = {}
    for s in SCHEMES:
        save_data[s] = {t: float(np.mean(all_ber[s][t])) for t in TURB_LIST}
        save_data[f'{s}_per_trial'] = {t: [float(x) for x in all_ber[s][t]] for t in TURB_LIST}
    # DD diagnostics
    for turb in TURB_LIST:
        d = dd_diagnostics[turb]
        save_data[f'diag_{turb}'] = {
            'mse_dd': d['mse_dd'],
            'mse_frame': d['mse_frame'],
            'corr_dd': d['corr_dd'],
            'h_true_sample': [float(x) for x in d['h_true'][:10]],
            'h_dd_sample': [float(x) for x in d['h_dd'][:10]],
        }

    with open(f'{OUT}/results_ch4_kf_perblock_h.json', 'w') as f:
        json.dump(save_data, f, indent=2)
    print(f"Results saved to {OUT}/results_ch4_kf_perblock_h.json")

    print(f"\nTotal time: {dt:.1f}s")
    print("=" * 72)
