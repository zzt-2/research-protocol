#!/usr/bin/env python3
"""Ch4 KF载波同步公平性验证 — 6组对照实验

验证原始 KF 仿真中的 5 个不公平因素：
1. KF 使用真实 h（oracle CSI），基线使用估计 h
2. KF 知道湍流等级（oracle），基线不知道
3. KF 使用 FOE N=4096，基线使用 N=1024
4. Q 参数经过网格搜索（在测试数据上调优）
5. 自适应 DPLL 基线实现有缺陷

实验设计：
A: 公平 FOE 对比（Fixed 用 N=4096）
B: KF 用估计 h（移除 oracle CSI）
C: KF 用估计湍流（移除 oracle 湍流）
D: 完全公平对比（Fixed N=4096 vs KF 估计h+估计湍流）
E: Oracle 上界（完美载波同步）
F: KF 用 N=1024（隔离 KF 跟踪贡献）

基于 sim_ch4_kf_carrier_sync.py，不修改原始文件。
"""

import numpy as np
from scipy.stats import gamma as gamma_dist
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, time, json

OUT = os.path.dirname(os.path.abspath(__file__))
np.random.seed(42)
plt.rcParams.update({'font.size': 10, 'figure.dpi': 150})

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
# 基础原语（复用 sim_direction_a.py）
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
# 基线载波恢复（复用 sim_direction_a.py）
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

def adaptive_params(h_est, gamma_bar_db=20, f_dot=DOPPLER_HIGH):
    gamma_bar = 10**(gamma_bar_db / 10)
    h_safe = max(h_est, 0.001)
    gamma = gamma_bar * h_safe
    N_fft = int(np.clip(80 * gamma_bar / (gamma**2 + 1e-10), 256, 8192))
    N_fft = int(2**np.ceil(np.log2(N_fft)))
    K_M = (3/4)**0.2
    df_norm = F_RESIDUAL * T_S
    M_vv = int(np.clip(K_M * gamma**(-0.2) * df_norm**(-0.4), 16, 256))
    M_vv = max(8, M_vv | 1) - 1
    B0 = np.sqrt(np.pi * LASER_LW * gamma_bar / T_S)
    B_L = np.clip(B0 * h_safe, 0.5e6, 20e6)
    omega_n = B_L / 0.53  # omega_n = B_L / 0.53, since B_L = 0.53*omega_n when zeta=sqrt(2)/2
    return N_fft, M_vv, omega_n

def carrier_recovery_fixed(rx, cfg=FIXED_CFG):
    fo_est = fft_foe(rx, N_fft=cfg['N_fft'])
    rx_comp = rx * np.exp(-1j * fo_est * np.arange(len(rx)))
    rx_pll, _ = dpll_track(rx_comp, omega_n=cfg['omega_n'], zeta=cfg['zeta'])
    rx_cpr, _ = vv_cpr(rx_pll, Nw=cfg['M_vv'])
    return rx_cpr

def carrier_recovery_adaptive(rx, h_est, gamma_bar_db=20, f_dot=DOPPLER_HIGH, h_foe=None):
    if h_foe is None:
        h_foe = h_est
    N_foe, M_vv, omega_n = adaptive_params(h_foe, gamma_bar_db, f_dot)
    fo_est = fft_foe(rx, N_fft=N_foe)
    rx_comp = rx * np.exp(-1j * fo_est * np.arange(len(rx)))
    rx_pll, _ = dpll_track(rx_comp, omega_n=omega_n, zeta=FIXED_CFG['zeta'])
    rx_cpr, _ = vv_cpr(rx_pll, Nw=M_vv)
    return rx_cpr

# ═══════════════════════════════════════════════════════════════
# KF Q矩阵设计（湍流感知）
# ═══════════════════════════════════════════════════════════════
# GG分布矩: E[h]=1, Var[h] = 1/alpha + 1/beta + 1/(alpha*beta)
# 激光相位噪声: sigma2_L = 2*pi*Delta_nu_L*T_s
# Doppler率不确定性: sigma2_df = (f_dot_max * T_s)^2 / 3
# 湍流相位噪声: sigma2_turb = kappa * Var[h]（标定系数）

# 通过网格搜索标定的湍流相位噪声参数
# sigma2_turb = kappa * Var[h]，kappa 需仿真标定
# 初始估计基于物理近似，后续通过Q_grid_search优化
SIGMA2_LASER = 2 * np.pi * LASER_LW * T_S  # ~2.51e-5 rad²

SIGMA2_DF_HIGH = (DOPPLER_HIGH * T_S)**2 / 3  # ~1.2e-3 Hz²
SIGMA2_DF_LOW  = (DOPPLER_LOW * T_S)**2 / 3

# Q矩阵设计参数（分湍流强度）
# sigma2_turb 基于GG矩 + 耦合系数的物理先验
Q_TURB_PARAMS = {
    'weak':     {'sigma2_turb': 1e-6,  'kappa': 1.56e-6},
    'moderate': {'sigma2_turb': 1e-4,  'kappa': 9.80e-5},
    'strong':   {'sigma2_turb': 1e-3,  'kappa': 3.79e-4},
}

def design_Q(turb_name='strong', f_dot=DOPPLER_HIGH):
    """设计湍流感知Q矩阵

    Q = diag(sigma2_phi, sigma2_df)
    sigma2_phi = sigma2_laser + sigma2_turb(turbulence)
    sigma2_df = (f_dot * T_s)^2 / 3
    """
    sigma2_turb = Q_TURB_PARAMS[turb_name]['sigma2_turb']
    sigma2_df = (f_dot * T_S)**2 / 3

    sigma2_phi = SIGMA2_LASER + sigma2_turb
    Q = np.diag([sigma2_phi, sigma2_df])
    return Q

def gg_var_h(alpha, beta):
    """GG分布方差 Var[h] = 1/alpha + 1/beta + 1/(alpha*beta)"""
    return 1/alpha + 1/beta + 1/(alpha*beta)

# ═══════════════════════════════════════════════════════════════
# 2状态 Kalman 滤波统一载波同步
# ═══════════════════════════════════════════════════════════════
def kf_unified(rx_block, h_block, gamma_bar, Q, phi_init=None, df_init=0.0,
               return_debug=False):
    """2状态KF统一载波同步（单块内运行）

    状态向量: x = [phi, Delta_f]^T
    状态转移: x[k+1] = F*x[k] + w[k]
    观测: z[k] = phi[k] + v[k]（判决导引）

    Args:
        rx_block: 接收信号（块内，已做MMSE均衡+FOE粗补偿）
        h_block: 该块的信道增益（标量）
        gamma_bar: 平均SNR（线性值）
        Q: 过程噪声协方差 2x2
        phi_init: 初始相位（可选，None则从信号估计）
        df_init: 初始频偏（rad/s，默认0，FOE已粗补偿）
        return_debug: 是否返回调试信息

    Returns:
        phi_est: 相位估计序列
        df_est: 频偏估计序列（最后一个值）
        debug_info: 可选调试信息
    """
    N = len(rx_block)
    F = np.array([[1.0, T_S],
                  [0.0, 1.0]])
    H = np.array([[1.0, 0.0]])

    # 初始相位：从第一个符号估计（如果未提供）
    if phi_init is None:
        if N >= 16:
            _, pe_vv = vv_cpr(rx_block, Nw=min(N, 16))
            phi_init = pe_vv[0]
        else:
            phi_init = np.angle(rx_block[0]**4) / 4

    # 初始频偏：FOE已粗补偿，残余很小
    x = np.array([phi_init, df_init])
    # P0：相位不确定度 ±π/4，频偏残余不确定度 ±100kHz（FOE精度量级）
    P = np.diag([(np.pi/4)**2, (2*np.pi*100e3)**2])

    phi_est = np.zeros(N)
    df_est = np.zeros(N)

    if return_debug:
        K_history = np.zeros(N)
        R_history = np.zeros(N)
        innov_history = np.zeros(N)

    for k in range(N):
        # === 预测步 ===
        x_pred = F @ x
        P_pred = F @ P @ F.T + Q

        # === 观测步（判决导引）===
        # 用预测相位做硬判决
        rx_rotated = rx_block[k] * np.exp(-1j * x_pred[0])
        s_hat = ((np.sign(np.real(rx_rotated))) + 1j * (np.sign(np.imag(rx_rotated)))) / np.sqrt(2)

        # 去调制后提取相位
        y = rx_block[k] * np.conj(s_hat)
        z_obs = np.angle(y)

        # 残差（处理相位缠绕）
        innov = z_obs - x_pred[0]
        # 缠绕到 [-pi, pi]
        innov = (innov + np.pi) % (2*np.pi) - np.pi

        # R矩阵：瞬时SNR驱动
        R = 1.0 / (2 * gamma_bar * h_block)

        # === 更新步 ===
        S = H @ P_pred @ H.T + R  # 标量
        K = P_pred @ H.T / S      # 2x1

        x = x_pred + K.flatten() * innov
        # 缠绕相位到 [-pi, pi]
        x[0] = (x[0] + np.pi) % (2*np.pi) - np.pi

        P = (np.eye(2) - K @ H) @ P_pred

        phi_est[k] = x[0]
        df_est[k] = x[1]

        if return_debug:
            K_history[k] = K[0, 0]
            R_history[k] = R
            innov_history[k] = innov

    if return_debug:
        return phi_est, df_est[-1], {'K': K_history, 'R': R_history, 'innov': innov_history}
    return phi_est, df_est[-1]

def kf_carrier_recovery(rx, h, gamma_bar, turb_name='strong', f_dot=DOPPLER_HIGH):
    """KF载波恢复：帧级FOE粗补偿 + 块级KF精跟踪

    Step 1: FFT-FOE 在完整帧上估计并补偿粗频偏
    Step 2: 每 GG 块内运行 2 状态 KF 精细跟踪残余频偏+相位噪声
    """
    N = len(rx)
    k = np.arange(N)

    # Step 1: 帧级 FFT-FOE 粗补偿
    fo_est = fft_foe(rx, N_fft=min(N, 4096), nfft_zp=8192)
    rx_foc = rx * np.exp(-1j * fo_est * k)  # frequency-offset compensated

    # Step 2: 块级 KF 精跟踪
    n_blocks = N // BLOCK
    Q = design_Q(turb_name, f_dot)
    # FOE已补偿大部分频偏，残余频偏动态大幅降低
    Q_fine = Q.copy()
    Q_fine[1, 1] = (50e3 * T_S)**2  # 残余频偏不确定性 ~50kHz

    phi_full = np.zeros(N)
    prev_df = 0.0  # 块间传递频偏估计

    for i in range(n_blocks):
        s, e = i*BLOCK, (i+1)*BLOCK
        h_val = h[s]

        # 用前一块的相位估计作为初始值（连续性）
        phi_init = phi_full[s-1] if i > 0 else None
        phi_est, df_est = kf_unified(rx_foc[s:e], h_val, gamma_bar, Q_fine,
                                      phi_init=phi_init, df_init=prev_df)
        phi_full[s:e] = phi_est
        prev_df = df_est

    # 剩余符号
    rem = N % BLOCK
    if rem > 0:
        s = n_blocks * BLOCK
        h_val = h[s]
        phi_init = phi_full[s-1] if n_blocks > 0 else None
        phi_est, _ = kf_unified(rx_foc[s:], h_val, gamma_bar, Q_fine,
                                 phi_init=phi_init, df_init=prev_df)
        phi_full[s:] = phi_est

    # 总补偿 = FOE粗补偿 + KF精补偿
    return rx_foc * np.exp(-1j * phi_full)

# ═══════════════════════════════════════════════════════════════
# 信号生成（复用框架）
# ═══════════════════════════════════════════════════════════════
def generate_signal(Ns, turb_name, f_dot, gamma_bar_db):
    """生成完整信号（返回 rx, rx_comp, bits, h, phi_true）"""
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

    # MMSE均衡
    rx_comp = rx * np.sqrt(h) / (h + 1/gamma_bar)
    rx_comp = amp_limit(rx_comp, 3.0)

    return rx_comp, bits, h, phi

# ═══════════════════════════════════════════════════════════════
# 实验 1：KF vs 基线 BER 对比
# ═══════════════════════════════════════════════════════════════
def run_comparison(Ns=10000, n_trials=50, gamma_bar_db=20):
    """KF vs 基线对比：3湍流 × 低仰角"""
    schemes = ['Fixed', 'Adaptive DPLL', 'KF (turb-aware)']
    turb_list = ['weak', 'moderate', 'strong']
    f_dot = DOPPLER_HIGH
    gamma_bar = 10**(gamma_bar_db / 10)

    results = {}
    for turb in turb_list:
        print(f"\n  Turbulence: {turb}")
        bers = {s: [] for s in schemes}

        for t in range(n_trials):
            np.random.seed(42 + t)
            rx_comp, bits, h, phi_true = generate_signal(Ns, turb, f_dot, gamma_bar_db)

            # 信道估计（帧级）
            n_blocks = Ns // BLOCK
            h_blocks = np.array([np.median(h[i*BLOCK:(i+1)*BLOCK]) for i in range(n_blocks)])
            h_est = np.median(h_blocks)
            h_foe = np.percentile(h_blocks, 10)

            # 方案1: 固定参数
            rx_fixed = carrier_recovery_fixed(rx_comp)
            bers['Fixed'].append(resolve_qpsk(rx_fixed, bits))

            # 方案2: 自适应DPLL（+4.8dB基线）
            np.random.seed(42 + t)
            _, bits2, h2, _ = generate_signal(Ns, turb, f_dot, gamma_bar_db)
            rx_adapt = carrier_recovery_adaptive(rx_comp, h_est, gamma_bar_db, f_dot, h_foe=h_foe)
            bers['Adaptive DPLL'].append(resolve_qpsk(rx_adapt, bits))

            # 方案3: KF湍流感知
            rx_kf = kf_carrier_recovery(rx_comp, h, gamma_bar, turb, f_dot)
            bers['KF (turb-aware)'].append(resolve_qpsk(rx_kf, bits))

        for s in schemes:
            mean_ber = np.mean(bers[s])
            print(f"    {s:20s}: BER={mean_ber:.6f}")
        results[turb] = {s: np.mean(bers[s]) for s in schemes}

    return results

def plot_comparison(results):
    """绘制BER对比柱状图"""
    turb_list = ['weak', 'moderate', 'strong']
    schemes = ['Fixed', 'Adaptive DPLL', 'KF (turb-aware)']
    colors = ['steelblue', 'coral', '#2ecc71']

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(turb_list))
    w = 0.25

    for i, s in enumerate(schemes):
        vals = [results[t][s] for t in turb_list]
        ax.bar(x + i*w - w, vals, w, label=s, color=colors[i])

    ax.set_xticks(x)
    ax.set_xticklabels([t.capitalize() for t in turb_list])
    ax.set_ylabel('BER')
    ax.set_title('Carrier Sync Comparison: KF vs Baselines')
    ax.legend()
    ax.set_yscale('log')
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(f'{OUT}/fig_kf_vs_baselines.pdf')
    plt.close()

# ═══════════════════════════════════════════════════════════════
# 实验 2：SNR扫描 BER 曲线
# ═══════════════════════════════════════════════════════════════
def run_snr_sweep(n_trials=30):
    """SNR扫描：3湍流 × KF/Adaptive/Fixed"""
    snrs = np.arange(10, 32, 2)
    turb_list = ['weak', 'moderate', 'strong']
    f_dot = DOPPLER_HIGH
    Ns = 10000

    sweep_data = {}
    for turb in turb_list:
        print(f"\n  SNR sweep: {turb}")
        gamma_bar_at_snr = {s: 10**(s/10) for s in snrs}

        bers = {'Fixed': [], 'Adaptive DPLL': [], 'KF (turb-aware)': []}
        for snr in snrs:
            gamma_bar = gamma_bar_at_snr[snr]
            bf, ba, bk = [], [], []
            for t in range(n_trials):
                np.random.seed(100 + t)
                rx_comp, bits, h, _ = generate_signal(Ns, turb, f_dot, snr)

                n_blocks = Ns // BLOCK
                h_blocks = np.array([np.median(h[i*BLOCK:(i+1)*BLOCK]) for i in range(n_blocks)])
                h_est = np.median(h_blocks)
                h_foe = np.percentile(h_blocks, 10)

                bf.append(resolve_qpsk(carrier_recovery_fixed(rx_comp), bits))
                ba.append(resolve_qpsk(carrier_recovery_adaptive(rx_comp, h_est, snr, f_dot, h_foe=h_foe), bits))
                bk.append(resolve_qpsk(kf_carrier_recovery(rx_comp, h, gamma_bar, turb, f_dot), bits))

            bers['Fixed'].append(np.mean(bf))
            bers['Adaptive DPLL'].append(np.mean(ba))
            bers['KF (turb-aware)'].append(np.mean(bk))
            print(f"    SNR={snr}dB: F={np.mean(bf):.5f} A={np.mean(ba):.5f} KF={np.mean(bk):.5f}")

        sweep_data[turb] = {'snrs': list(snrs), **bers}

    # 绘图
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    colors = {'Fixed': 'steelblue', 'Adaptive DPLL': 'coral', 'KF (turb-aware)': '#2ecc71'}
    markers = {'Fixed': 's', 'Adaptive DPLL': '^', 'KF (turb-aware)': 'o'}

    for ax, turb in zip(axes, turb_list):
        d = sweep_data[turb]
        for s in ['Fixed', 'Adaptive DPLL', 'KF (turb-aware)']:
            ax.semilogy(d['snrs'], d[s], f'{markers[s]}-', color=colors[s], label=s, ms=5)
        ax.set_xlabel('SNR (dB)')
        ax.set_ylabel('BER')
        ax.set_title(f'{turb.capitalize()} turbulence')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim(1e-4, 1)

    plt.suptitle('BER vs SNR: KF vs Baselines (f_dot=150 MHz/s)')
    plt.tight_layout()
    plt.savefig(f'{OUT}/fig_kf_snr_sweep.pdf')
    plt.close()

    return sweep_data

# ═══════════════════════════════════════════════════════════════
# 实验 3：Q矩阵消融
# ═══════════════════════════════════════════════════════════════
def run_q_ablation(Ns=10000, n_trials=30, gamma_bar_db=20):
    """Q矩阵设计消融：固定Q / 分湍流Q / 在线自适应Q"""
    turb = 'strong'
    f_dot = DOPPLER_HIGH
    gamma_bar = 10**(gamma_bar_db / 10)

    # 三种Q设计
    Q_fixed = np.diag([SIGMA2_LASER + 1e-5, SIGMA2_DF_HIGH])  # 不分湍流
    Q_turb = design_Q('strong', f_dot)  # 分湍流强度

    modes = {
        'Q fixed (universal)': Q_fixed,
        'Q turb-aware (strong)': Q_turb,
        'Q online (h-adaptive)': None,  # 在线更新
    }

    results = {}
    for mode_name, Q_mode in modes.items():
        bers = []
        for t in range(n_trials):
            np.random.seed(200 + t)
            rx_comp, bits, h, _ = generate_signal(Ns, turb, f_dot, gamma_bar_db)

            # FOE粗补偿（与kf_carrier_recovery一致）
            fo_est = fft_foe(rx_comp, N_fft=min(Ns, 4096), nfft_zp=8192)
            rx_foc = rx_comp * np.exp(-1j * fo_est * np.arange(Ns))

            n_blocks = Ns // BLOCK
            phi_full = np.zeros(Ns)
            prev_df = 0.0

            for i in range(n_blocks):
                s, e = i*BLOCK, (i+1)*BLOCK
                h_val = h[s]

                if Q_mode is None:
                    h_safe = max(h_val, 0.01)
                    sigma2_turb_online = Q_TURB_PARAMS['strong']['kappa'] * (1.0/h_safe)
                    Q_online = np.diag([SIGMA2_LASER + sigma2_turb_online, (50e3*T_S)**2])
                    phi_init = phi_full[s-1] if i > 0 else None
                    phi_est, prev_df = kf_unified(rx_foc[s:e], h_val, gamma_bar, Q_online,
                                                   phi_init=phi_init, df_init=prev_df)
                else:
                    Q_fine = Q_mode.copy()
                    Q_fine[1, 1] = (50e3*T_S)**2
                    phi_init = phi_full[s-1] if i > 0 else None
                    phi_est, prev_df = kf_unified(rx_foc[s:e], h_val, gamma_bar, Q_fine,
                                                   phi_init=phi_init, df_init=prev_df)

                phi_full[s:e] = phi_est

            rx_rec = rx_comp * np.exp(-1j * phi_full)
            bers.append(resolve_qpsk(rx_rec, bits))

        mean_ber = np.mean(bers)
        results[mode_name] = mean_ber
        print(f"  {mode_name:30s}: BER={mean_ber:.6f}")

    # 绘图
    fig, ax = plt.subplots(figsize=(8, 5))
    names = list(results.keys())
    vals = list(results.values())
    colors_q = ['#e74c3c', '#2ecc71', '#3498db']
    bars = ax.bar(range(len(names)), vals, color=colors_q)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=15, ha='right', fontsize=9)
    ax.set_ylabel('BER')
    ax.set_title('Q Matrix Ablation (Strong Turbulence, SNR=20dB)')
    ax.grid(True, alpha=0.3, axis='y')
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f'{v:.5f}', ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plt.savefig(f'{OUT}/fig_kf_q_ablation.pdf')
    plt.close()

    return results

# ═══════════════════════════════════════════════════════════════
# 实验 4：KF跟踪轨迹可视化
# ═══════════════════════════════════════════════════════════════
def plot_tracking_trace(Ns=1000, gamma_bar_db=20, turb_name='strong'):
    """展示KF跟踪轨迹：相位/频偏估计 vs 真值"""
    f_dot = DOPPLER_HIGH
    gamma_bar = 10**(gamma_bar_db / 10)

    np.random.seed(42)
    rx_comp, bits, h, phi_true = generate_signal(Ns, turb_name, f_dot, gamma_bar_db)

    Q = design_Q(turb_name, f_dot)

    # 运行KF（块模式）
    n_blocks = Ns // BLOCK
    phi_est_full = np.zeros(Ns)
    df_est_full = np.zeros(Ns)
    K_full = np.zeros(Ns)
    R_full = np.zeros(Ns)

    for i in range(n_blocks):
        s, e = i*BLOCK, (i+1)*BLOCK
        phi_est, _, debug = kf_unified(rx_comp[s:e], h[s], gamma_bar, Q, return_debug=True)
        phi_est_full[s:e] = phi_est
        df_est_full[s:e] = debug.get('df_est', np.zeros(BLOCK))
        K_full[s:e] = debug['K']
        R_full[s:e] = debug['R']

    # 相位解缠用于绘图
    phi_true_unwrap = np.unwrap(phi_true)
    phi_est_unwrap = np.unwrap(phi_est_full)

    k = np.arange(Ns)

    fig, axes = plt.subplots(3, 1, figsize=(14, 10))

    # 相位跟踪
    axes[0].plot(k, phi_true_unwrap, 'b-', label='True φ', alpha=0.7)
    axes[0].plot(k, phi_est_unwrap, 'r--', label='KF est φ', alpha=0.8)
    # 标记块边界
    for i in range(1, n_blocks):
        axes[0].axvline(i*BLOCK, color='gray', ls=':', alpha=0.3)
    axes[0].set_ylabel('Phase (rad)')
    axes[0].set_title(f'KF Tracking: {turb_name.capitalize()} turbulence, SNR={gamma_bar_db}dB')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # 相位误差
    phase_err = phi_est_unwrap - phi_true_unwrap
    axes[1].plot(k, phase_err, 'g-', alpha=0.7)
    axes[1].axhline(0, color='k', ls='-', alpha=0.3)
    for i in range(1, n_blocks):
        axes[1].axvline(i*BLOCK, color='gray', ls=':', alpha=0.3)
    axes[1].set_ylabel('Phase Error (rad)')
    axes[1].set_title(f'Phase Error (RMSE={np.sqrt(np.mean(phase_err**2)):.4f} rad)')
    axes[1].grid(True, alpha=0.3)

    # Kalman增益和R
    ax2 = axes[2]
    ax2.plot(k, K_full, 'm-', label='K_φ (Kalman gain)', alpha=0.7)
    ax2.set_ylabel('Kalman Gain K_φ')
    ax2.legend(loc='upper left')
    ax2.grid(True, alpha=0.3)

    ax2b = ax2.twinx()
    ax2b.plot(k, R_full, 'c-', label='R (obs noise)', alpha=0.5)
    ax2b.set_ylabel('R (rad²)')
    ax2b.legend(loc='upper right')
    for i in range(1, n_blocks):
        axes[2].axvline(i*BLOCK, color='gray', ls=':', alpha=0.3)
    axes[2].set_xlabel('Symbol index')
    axes[2].set_title('Kalman Gain & Observation Noise (R ∝ 1/h)')

    plt.tight_layout()
    plt.savefig(f'{OUT}/fig_kf_tracking_{turb_name}.pdf')
    plt.close()

    return {'phase_rmse': np.sqrt(np.mean(phase_err**2))}

# ═══════════════════════════════════════════════════════════════
# 实验 5：Q矩阵网格搜索（标定 sigma2_turb）
# ═══════════════════════════════════════════════════════════════
def q_grid_search(turb_name='strong', Ns=5000, n_trials=20, gamma_bar_db=20):
    """网格搜索最优 sigma2_turb"""
    f_dot = DOPPLER_HIGH
    gamma_bar = 10**(gamma_bar_db / 10)

    sigma2_turb_candidates = np.logspace(-7, -1, 20)
    bers = []

    for s2t in sigma2_turb_candidates:
        Q = np.diag([SIGMA2_LASER + s2t, SIGMA2_DF_HIGH])
        trial_bers = []
        for t in range(n_trials):
            np.random.seed(500 + t)
            rx_comp, bits, h, _ = generate_signal(Ns, turb_name, f_dot, gamma_bar_db)

            n_blocks = Ns // BLOCK
            phi_full = np.zeros(Ns)
            for i in range(n_blocks):
                s, e = i*BLOCK, (i+1)*BLOCK
                phi_est, _ = kf_unified(rx_comp[s:e], h[s], gamma_bar, Q)
                phi_full[s:e] = phi_est

            rx_rec = rx_comp * np.exp(-1j * phi_full)
            trial_bers.append(resolve_qpsk(rx_rec, bits))

        mean_ber = np.mean(trial_bers)
        bers.append(mean_ber)

    best_idx = np.argmin(bers)
    best_s2t = sigma2_turb_candidates[best_idx]
    print(f"\n  Q Grid Search ({turb_name}):")
    print(f"    Best sigma2_turb = {best_s2t:.2e}  BER = {bers[best_idx]:.6f}")

    # 绘图
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.semilogx(sigma2_turb_candidates, bers, 'b-o', ms=4)
    ax.axvline(best_s2t, color='r', ls='--', label=f'Best σ²_turb={best_s2t:.1e}')
    ax.set_xlabel('σ²_turb (rad²/symbol)')
    ax.set_ylabel('BER')
    ax.set_title(f'Q Matrix Grid Search ({turb_name.capitalize()} turbulence, SNR={gamma_bar_db}dB)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{OUT}/fig_kf_q_grid_{turb_name}.pdf')
    plt.close()

    return {'sigma2_turb_candidates': list(sigma2_turb_candidates),
            'bers': bers, 'best_sigma2_turb': best_s2t}

# ═══════════════════════════════════════════════════════════════
# 公平性验证：辅助函数
# ═══════════════════════════════════════════════════════════════
def estimate_h_for_blocks(h, Ns):
    """从 h 序列中提取帧级信道估计（与基线相同的方法）"""
    n_blocks = Ns // BLOCK
    h_blocks = np.array([np.median(h[i*BLOCK:(i+1)*BLOCK]) for i in range(n_blocks)])
    h_est = np.median(h_blocks)
    h_foe = np.percentile(h_blocks, 10)
    return h_est, h_foe

def estimate_turbulence_from_h(h):
    """从 h 统计量估计湍流等级

    GG 分布方差: Var[h] = 1/a + 1/b + 1/(a*b)
      weak     (4,3): 0.583
      moderate (2.5,1.8): 0.956
      strong   (1.5,0.8): 1.972
    """
    var_h = np.var(h)
    if var_h < 0.75:
        return 'weak'
    elif var_h < 1.5:
        return 'moderate'
    else:
        return 'strong'

def kf_carrier_recovery_est_h(rx, h_est_frame, gamma_bar, turb_name='strong', f_dot=DOPPLER_HIGH):
    """KF载波恢复：使用帧级估计 h（非 oracle per-block h）

    与 kf_carrier_recovery 的区别：
    - h_val 使用帧级估计值 h_est_frame（标量），而非每个 block 的真实 h[s]
    - 其余逻辑完全一致
    """
    N = len(rx)
    k = np.arange(N)

    # Step 1: 帧级 FFT-FOE 粗补偿
    fo_est = fft_foe(rx, N_fft=min(N, 4096), nfft_zp=8192)
    rx_foc = rx * np.exp(-1j * fo_est * k)

    # Step 2: 块级 KF 精跟踪
    n_blocks = N // BLOCK
    Q = design_Q(turb_name, f_dot)
    Q_fine = Q.copy()
    Q_fine[1, 1] = (50e3 * T_S)**2

    phi_full = np.zeros(N)
    prev_df = 0.0

    for i in range(n_blocks):
        s, e = i*BLOCK, (i+1)*BLOCK
        # 使用帧级估计 h（与基线相同），而非真实 h[s]
        h_val = max(h_est_frame, 0.01)

        phi_init = phi_full[s-1] if i > 0 else None
        phi_est, df_est = kf_unified(rx_foc[s:e], h_val, gamma_bar, Q_fine,
                                      phi_init=phi_init, df_init=prev_df)
        phi_full[s:e] = phi_est
        prev_df = df_est

    rem = N % BLOCK
    if rem > 0:
        s = n_blocks * BLOCK
        h_val = max(h_est_frame, 0.01)
        phi_init = phi_full[s-1] if n_blocks > 0 else None
        phi_est, _ = kf_unified(rx_foc[s:], h_val, gamma_bar, Q_fine,
                                 phi_init=phi_init, df_init=prev_df)
        phi_full[s:] = phi_est

    return rx_foc * np.exp(-1j * phi_full)

def kf_carrier_recovery_est_turb(rx, h, gamma_bar, f_dot=DOPPLER_HIGH):
    """KF载波恢复：使用估计湍流等级（非 oracle）"""
    N = len(rx)
    k = np.arange(N)

    # 估计湍流等级
    turb_est = estimate_turbulence_from_h(h)

    fo_est = fft_foe(rx, N_fft=min(N, 4096), nfft_zp=8192)
    rx_foc = rx * np.exp(-1j * fo_est * k)

    n_blocks = N // BLOCK
    Q = design_Q(turb_est, f_dot)
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

def kf_carrier_recovery_fully_fair(rx, h_est_frame, h, gamma_bar, f_dot=DOPPLER_HIGH):
    """KF载波恢复：完全公平（估计 h + 估计湍流 + N=4096 FOE）"""
    N = len(rx)
    k = np.arange(N)

    turb_est = estimate_turbulence_from_h(h)

    fo_est = fft_foe(rx, N_fft=min(N, 4096), nfft_zp=8192)
    rx_foc = rx * np.exp(-1j * fo_est * k)

    n_blocks = N // BLOCK
    Q = design_Q(turb_est, f_dot)
    Q_fine = Q.copy()
    Q_fine[1, 1] = (50e3 * T_S)**2

    phi_full = np.zeros(N)
    prev_df = 0.0

    for i in range(n_blocks):
        s, e = i*BLOCK, (i+1)*BLOCK
        h_val = max(h_est_frame, 0.01)
        phi_init = phi_full[s-1] if i > 0 else None
        phi_est, df_est = kf_unified(rx_foc[s:e], h_val, gamma_bar, Q_fine,
                                      phi_init=phi_init, df_init=prev_df)
        phi_full[s:e] = phi_est
        prev_df = df_est

    rem = N % BLOCK
    if rem > 0:
        s = n_blocks * BLOCK
        h_val = max(h_est_frame, 0.01)
        phi_init = phi_full[s-1] if n_blocks > 0 else None
        phi_est, _ = kf_unified(rx_foc[s:], h_val, gamma_bar, Q_fine,
                                 phi_init=phi_init, df_init=prev_df)
        phi_full[s:] = phi_est

    return rx_foc * np.exp(-1j * phi_full)

def kf_carrier_recovery_n1024(rx, h, gamma_bar, turb_name='strong', f_dot=DOPPLER_HIGH):
    """KF载波恢复：FOE 用 N=1024（与基线相同），隔离 KF 跟踪贡献"""
    N = len(rx)
    k = np.arange(N)

    # FOE 用 N=1024（与基线相同）
    fo_est = fft_foe(rx, N_fft=min(N, 1024), nfft_zp=8192)
    rx_foc = rx * np.exp(-1j * fo_est * k)

    n_blocks = N // BLOCK
    Q = design_Q(turb_name, f_dot)
    Q_fine = Q.copy()
    # 残余频偏更大（因为 FOE 精度降低），使用原始 Q_fine 的频偏不确定性
    Q_fine[1, 1] = (200e3 * T_S)**2  # N=1024 时残余频偏约 200kHz

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

def carrier_recovery_fixed_n4096(rx):
    """Fixed 基线但 FOE 用 N=4096（与 KF 相同）"""
    cfg = FIXED_CFG.copy()
    cfg['N_fft'] = 4096
    return carrier_recovery_fixed(rx, cfg=cfg)

def oracle_perfect_sync(rx_comp, phi_true):
    """完美载波同步：直接用真实相位补偿"""
    return rx_comp * np.exp(-1j * phi_true)


# ═══════════════════════════════════════════════════════════════
# 公平性验证主程序
# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    t0 = time.time()
    Ns = 10000
    N_TRIALS = 30
    GAMMA_DB = 20
    F_DOT = DOPPLER_HIGH
    GAMMA_BAR = 10**(GAMMA_DB / 10)
    TURB_LIST = ['weak', 'moderate', 'strong']

    print("=" * 70)
    print("KF Carrier Sync Fairness Verification")
    print(f"  Ns={Ns}, trials={N_TRIALS}, SNR={GAMMA_DB}dB, f_dot={F_DOT/1e6:.0f}MHz/s")
    print("=" * 70)

    # Storage for all results
    all_ber = {}
    for label in ['Fixed N=1024', 'Fixed N=4096', 'KF oracle',
                   'KF est-h', 'KF est-turb', 'KF fully fair',
                   'Oracle perfect', 'KF N=1024']:
        all_ber[label] = {t: [] for t in TURB_LIST}

    # Turbulence estimation accuracy tracking
    turb_est_correct = {t: 0 for t in TURB_LIST}

    for turb in TURB_LIST:
        print(f"\n--- Turbulence: {turb} ---")
        for trial in range(N_TRIALS):
            np.random.seed(42 + trial)
            rx_comp, bits, h, phi_true = generate_signal(Ns, turb, F_DOT, GAMMA_DB)

            # 信道估计（与基线相同方法）
            h_est, h_foe = estimate_h_for_blocks(h, Ns)

            # 湍流估计
            turb_est = estimate_turbulence_from_h(h)
            if turb_est == turb:
                turb_est_correct[turb] += 1

            # ---- Reference: Fixed N=1024 (original baseline) ----
            rx_fixed = carrier_recovery_fixed(rx_comp)
            all_ber['Fixed N=1024'][turb].append(resolve_qpsk(rx_fixed, bits))

            # ---- Exp A: Fixed N=4096 ----
            rx_fixed_4096 = carrier_recovery_fixed_n4096(rx_comp)
            all_ber['Fixed N=4096'][turb].append(resolve_qpsk(rx_fixed_4096, bits))

            # ---- Original KF oracle (true h + known turb + N=4096) ----
            rx_kf_oracle = kf_carrier_recovery(rx_comp, h, GAMMA_BAR, turb, F_DOT)
            all_ber['KF oracle'][turb].append(resolve_qpsk(rx_kf_oracle, bits))

            # ---- Exp B: KF with estimated h ----
            rx_kf_esth = kf_carrier_recovery_est_h(rx_comp, h_est, GAMMA_BAR, turb, F_DOT)
            all_ber['KF est-h'][turb].append(resolve_qpsk(rx_kf_esth, bits))

            # ---- Exp C: KF with estimated turbulence ----
            rx_kf_estturb = kf_carrier_recovery_est_turb(rx_comp, h, GAMMA_BAR, F_DOT)
            all_ber['KF est-turb'][turb].append(resolve_qpsk(rx_kf_estturb, bits))

            # ---- Exp D: KF fully fair (est h + est turb) ----
            rx_kf_fair = kf_carrier_recovery_fully_fair(rx_comp, h_est, h, GAMMA_BAR, F_DOT)
            all_ber['KF fully fair'][turb].append(resolve_qpsk(rx_kf_fair, bits))

            # ---- Exp E: Oracle perfect sync ----
            rx_oracle = oracle_perfect_sync(rx_comp, phi_true)
            all_ber['Oracle perfect'][turb].append(resolve_qpsk(rx_oracle, bits))

            # ---- Exp F: KF with N=1024 ----
            rx_kf_n1024 = kf_carrier_recovery_n1024(rx_comp, h, GAMMA_BAR, turb, F_DOT)
            all_ber['KF N=1024'][turb].append(resolve_qpsk(rx_kf_n1024, bits))

        # Print per-turbulence results
        print(f"  Turbulence estimation accuracy: {turb_est_correct[turb]}/{N_TRIALS}")
        for label in all_ber:
            mean_b = np.mean(all_ber[label][turb])
            print(f"    {label:20s}: BER={mean_b:.6f}")

    # ═══════════════════════════════════════════════════════════
    # Summary Table
    # ═══════════════════════════════════════════════════════════
    dt = time.time() - t0
    print(f"\n{'=' * 70}")
    print(f"EXPERIMENT SUMMARY ({dt:.1f}s)")
    print(f"{'=' * 70}")

    header = f"{'':20s} | {'Weak':>10s} | {'Moderate':>10s} | {'Strong':>10s}"
    sep = "-" * 20 + "-+-" + "-".join(["-" * 10] * 3)
    print(header)
    print(sep)

    mean_results = {}
    for label in all_ber:
        vals = [np.mean(all_ber[label][t]) for t in TURB_LIST]
        mean_results[label] = {t: v for t, v in zip(TURB_LIST, vals)}
        row = f"{label:20s} | {vals[0]:10.6f} | {vals[1]:10.6f} | {vals[2]:10.6f}"
        tag = ""
        if label == 'Fixed N=4096': tag = "  [Exp A]"
        elif label == 'KF est-h': tag = "  [Exp B]"
        elif label == 'KF est-turb': tag = "  [Exp C]"
        elif label == 'KF fully fair': tag = "  [Exp D]"
        elif label == 'Oracle perfect': tag = "  [Exp E]"
        elif label == 'KF N=1024': tag = "  [Exp F]"
        print(row + tag)

    # Gain Analysis
    print(f"\n{'=' * 70}")
    print("GAIN ANALYSIS (dB)")
    print(f"{'=' * 70}")

    # Gain: KF fully fair vs Fixed N=4096
    print("\nKF fully fair vs Fixed(N=4096):")
    for turb in TURB_LIST:
        fair_ber = mean_results['KF fully fair'][turb]
        fix4096_ber = mean_results['Fixed N=4096'][turb]
        if fair_ber > 0 and fix4096_ber > 0:
            gain = 10 * np.log10(fix4096_ber / fair_ber)
        else:
            gain = 0.0
        print(f"  {turb:10s}: {gain:+.1f} dB")

    # Gain: KF oracle vs Oracle perfect (gap to theoretical optimum)
    print("\nKF oracle vs Oracle perfect (gap to optimum):")
    for turb in TURB_LIST:
        kf_ber = mean_results['KF oracle'][turb]
        oracle_ber = mean_results['Oracle perfect'][turb]
        if kf_ber > 0 and oracle_ber > 0:
            gap = 10 * np.log10(kf_ber / oracle_ber)
        else:
            gap = 0.0
        print(f"  {turb:10s}: gap={gap:.1f} dB")

    # Decomposition of the original gain claim
    print(f"\n{'=' * 70}")
    print("DECOMPOSITION OF ORIGINAL GAIN (KF oracle vs Fixed N=1024):")
    print(f"{'=' * 70}")
    for turb in TURB_LIST:
        kf_oracle = mean_results['KF oracle'][turb]
        fix1024 = mean_results['Fixed N=1024'][turb]
        fix4096 = mean_results['Fixed N=4096'][turb]
        kf_fair = mean_results['KF fully fair'][turb]
        kf_n1024 = mean_results['KF N=1024'][turb]
        kf_estturb = mean_results['KF est-turb'][turb]

        def db_ratio(a, b):
            if a > 0 and b > 0: return 10 * np.log10(a / b)
            return 0.0

        total_gain = db_ratio(fix1024, kf_oracle)
        # Component 1: FOE window size (Fixed N=1024 -> Fixed N=4096)
        foe_contrib = db_ratio(fix1024, fix4096)
        # Component 2: Oracle h advantage (KF fully fair -> KF oracle)
        # Positive = oracle h helps KF
        oracle_h_contrib = db_ratio(kf_fair, kf_oracle)
        # Component 3: Oracle turbulence advantage (KF est-turb -> KF oracle)
        oracle_turb_contrib = db_ratio(kf_estturb, kf_oracle)
        # Component 4: Pure KF tracking (Fixed 4096 -> KF fully fair)
        # This is the genuine KF contribution with all oracle removed
        pure_kf_vs_fair = db_ratio(fix4096, kf_fair)
        # Component 5: Pure KF tracking at same FOE (Fixed 1024 -> KF N=1024)
        pure_kf_vs_n1024 = db_ratio(fix1024, kf_n1024)

        print(f"\n  {turb.upper()}:")
        print(f"    Total original gain (KF oracle vs Fixed N=1024): {total_gain:+.1f} dB")
        print(f"      FOE window N=4096 vs N=1024:    {foe_contrib:+.1f} dB  (Exp A)")
        print(f"      Oracle h advantage:              {oracle_h_contrib:+.1f} dB  (Exp B)")
        print(f"      Oracle turbulence advantage:     {oracle_turb_contrib:+.1f} dB  (Exp C)")
        print(f"      Pure KF (Fixed4096 vs KF-fair):  {pure_kf_vs_fair:+.1f} dB  (Exp D)")
        print(f"      Pure KF (Fixed1024 vs KF N1024): {pure_kf_vs_n1024:+.1f} dB  (Exp F)")

    # Turbulence estimation accuracy
    print(f"\n{'=' * 70}")
    print("TURBULENCE ESTIMATION ACCURACY:")
    print(f"{'=' * 70}")
    for turb in TURB_LIST:
        acc = turb_est_correct[turb] / N_TRIALS * 100
        print(f"  {turb:10s}: {acc:.0f}% ({turb_est_correct[turb]}/{N_TRIALS})")

    # Save results
    save_data = {}
    for label in all_ber:
        save_data[label] = {t: np.mean(all_ber[label][t]) for t in TURB_LIST}
    with open(f'{OUT}/kf_verification_results.json', 'w') as f:
        json.dump(save_data, f, indent=2, default=str)
    print(f"\nResults saved to {OUT}/kf_verification_results.json")
    print(f"Total time: {dt:.1f}s")
    print("=" * 70)
