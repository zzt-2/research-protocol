#!/usr/bin/env python3
"""Ch4 系统性分析仿真 — Gamma-Gamma 湍流下载波同步方法对比

对比方法：FOE+VV / FOE+BPS / FOE+DPLL / FOE+DPLL+VV
实验：
  Exp1: BER vs 平均SNR（三档湍流 + AWGN参考）
  Exp2: BER vs FOE 窗口长度 N_fft
  Exp3: BER vs VV 窗口 M_vv / DPLL 带宽 B_L
  Exp4: 湍流强度综合对比（固定 SNR）

关键设计原则（thesis-lessons.md）：
  - TL-13: 所有方法共用同一信道/噪声/相位实现
  - TL-11: 公平性分层审查
  - MMSE 均衡使用真实 h（20dB 下影响可忽略，S022 阶段十一验证）
"""

import numpy as np
from scipy.stats import gamma as gamma_dist
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, time

OUT = os.path.dirname(os.path.abspath(__file__))
plt.rcParams.update({'font.size': 10, 'figure.dpi': 150})

# ═══════════════════════════════════════════════════════════════
# 系统参数 (Zhao 2025)
# ═══════════════════════════════════════════════════════════════
R_SYM = 2.5e9           # 符号率 (Gsps)
T_S = 1 / R_SYM         # 符号周期 (s)
LASER_LW = 10e3         # 激光线宽 (Hz)
TURB = {
    'weak':     (4.0, 3.0),
    'moderate': (2.5, 1.8),
    'strong':   (1.5, 0.8),
}
BLOCK = 100              # 块衰落大小 (符号)
F_DOT = 150e6            # 多普勒变化率 (Hz/s)
F_RES = 1e6              # 预补偿后残余频偏 (Hz)
ZETA = np.sqrt(2) / 2    # DPLL 阻尼系数

# 默认参数 (Zhao 2025 配置)
DEF_NFFT = 1024
DEF_MVV = 64
DEF_B_BPS = 32
DEF_NW_BPS = 61
DEF_WN = 8e6             # DPLL 自然频率 (rad/s)

# ═══════════════════════════════════════════════════════════════
# 基础原语
# ═══════════════════════════════════════════════════════════════
def gg_block(N, a, b, bs=BLOCK):
    """GG 块衰落信道"""
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
    """解决 π/2 相位模糊"""
    best = 1.0
    for r in np.arange(0, 2*np.pi, np.pi/4):
        b = ber_count(tx_bits, rx * np.exp(-1j*r))
        if b < best:
            best = b
    return best

def amp_limit(rx, thresh=3.0):
    amp = np.abs(rx)
    mask = amp > thresh
    out = rx.copy()
    out[mask] = rx[mask] / amp[mask] * thresh
    return out

def doppler_phase(N):
    """Doppler 时变 + 激光相位噪声"""
    k = np.arange(N)
    phi_fo = 2 * np.pi * F_RES * k * T_S
    phi_dot = np.pi * F_DOT * (k * T_S)**2
    phi_laser = np.sqrt(2 * np.pi * LASER_LW * T_S) * np.cumsum(np.random.randn(N))
    return phi_fo + phi_dot + phi_laser

# ═══════════════════════════════════════════════════════════════
# 载波恢复算法
# ═══════════════════════════════════════════════════════════════

def fft_foe(rx, N_fft=DEF_NFFT, nfft_zp=8192):
    """FFT 频偏估计（4 次方法）"""
    N_fft = min(N_fft, len(rx))
    seg = rx[:N_fft]
    r4 = seg**4
    win = np.hanning(N_fft)
    R4 = np.fft.fftshift(np.fft.fft(r4 * win, n=nfft_zp))
    freqs = np.fft.fftshift(np.fft.fftfreq(nfft_zp, d=1))
    idx = np.argmax(np.abs(R4))
    if 1 <= idx < len(R4) - 1:
        av, bv, gv = np.abs(R4[idx-1]), np.abs(R4[idx]), np.abs(R4[idx+1])
        denom = av - 2*bv + gv
        if bv > av and abs(denom) > 1e-10:
            p = 0.5 * (av - gv) / denom
            f_est = freqs[idx] + p * (freqs[1] - freqs[0])
        else:
            f_est = freqs[idx]
    else:
        f_est = freqs[idx]
    return 2 * np.pi * f_est / 4  # rad/symbol

def _sequential_unwrap(pe_raw, M=4):
    """顺序相位跟踪：每步选离上一步最近的候选（mod π/M）"""
    N = len(pe_raw)
    pe = np.zeros(N)
    pe[0] = pe_raw[0]
    for k in range(1, N):
        candidates = pe_raw[k] + np.arange(-3, 4) * (np.pi / M)
        diffs = np.abs(np.angle(np.exp(1j * (candidates - pe[k-1]))))
        pe[k] = candidates[np.argmin(diffs)]
    return pe

def vv_cpr(rx, Nw=DEF_MVV):
    """Viterbi-Viterbi 载波相位恢复 (M=4)

    4 次方去调制 → 滑动窗口平均 → 标准 phase unwrap。
    注：VV 在强湍流深衰落中有相位滑动风险，这是前馈方法的已知局限。
    """
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

def bps_cpr(rx, B=DEF_B_BPS, Nw=DEF_NW_BPS):
    """Blind Phase Search (Pfau 2009, JLT)

    B 个测试相位，Nw 符号滑动窗口平均距离度量。
    使用顺序相位跟踪解决 M=4 模糊。
    """
    N = len(rx)
    phases = 2 * np.pi * np.arange(B) / B

    # 向量化计算所有测试相位的距离度量
    rotated = rx[np.newaxis, :] * np.exp(-1j * phases[:, np.newaxis])
    dec = (np.sign(np.real(rotated)) + 1j * np.sign(np.imag(rotated))) / np.sqrt(2)
    metrics = np.abs(rotated - dec)**2

    # 滑动窗口平均
    ker = np.ones(Nw) / Nw
    for b in range(B):
        metrics[b] = np.convolve(metrics[b], ker, mode='same')

    best_b = np.argmin(metrics, axis=0)
    pe_raw = phases[best_b]

    # M=4 相位模糊展开：乘 4 → unwrap 2π 跳变 → 除 4
    pe = np.unwrap(4 * pe_raw) / 4

    return rx * np.exp(-1j * pe), pe

def dpll_track(rx, omega_n=DEF_WN, zeta=ZETA):
    """二阶 DPLL"""
    wT = min(omega_n * T_S, 0.5)
    c1 = 2 * zeta * wT
    c2 = wT**2
    N = len(rx)
    phi_est = np.zeros(N)
    integrator = 0.0
    vco_phase = 0.0
    for k in range(N):
        mixed = rx[k] * np.exp(-1j * vco_phase)
        pd_out = np.angle(mixed**4) / 4
        integrator += c2 * pd_out
        vco_phase += c1 * pd_out + integrator
        phi_est[k] = vco_phase
    return rx * np.exp(-1j * phi_est), phi_est

def apply_foe(rx, N_fft):
    """FOE 频偏补偿"""
    fo = fft_foe(rx, N_fft)
    return rx * np.exp(-1j * fo * np.arange(len(rx)))

# ═══════════════════════════════════════════════════════════════
# 共用信号生成（公平性保证）
# ═══════════════════════════════════════════════════════════════

def generate_signal(Ns, turb_name, gamma_bar_db, seed):
    """生成共用信号 — 所有方法处理同一 rx_eq。

    信号模型: r[k] = √h[k]·s[k]·exp(jφ[k]) + n[k]
    相干检测约定: 瞬时 SNR γ = γ̄·h
    MMSE 均衡使用真实 h（公平：所有方法获得相同预处理）
    """
    np.random.seed(seed)
    a, b = TURB[turb_name]
    gamma_bar = 10**(gamma_bar_db / 10)

    bits = np.random.randint(0, 2, 2*Ns)
    tx = qpsk_mod(bits)
    h = gg_block(Ns, a, b)
    phi = doppler_phase(Ns)

    rx = tx * np.sqrt(h) * np.exp(1j * phi) + \
         np.sqrt(1/(2*gamma_bar)) * (np.random.randn(Ns) + 1j*np.random.randn(Ns))

    # MMSE 均衡: rx_eq = r · √h / (h + 1/γ̄)
    rx_eq = rx * np.sqrt(h) / (h + 1/gamma_bar)
    return amp_limit(rx_eq, 3.0), bits

def generate_signal_awgn(Ns, gamma_bar_db, seed):
    """AWGN 参考信号（无湍流）"""
    np.random.seed(seed)
    gamma_bar = 10**(gamma_bar_db / 10)

    bits = np.random.randint(0, 2, 2*Ns)
    tx = qpsk_mod(bits)
    phi = doppler_phase(Ns)

    rx = tx * np.exp(1j * phi) + \
         np.sqrt(1/(2*gamma_bar)) * (np.random.randn(Ns) + 1j*np.random.randn(Ns))
    return rx, bits

# ═══════════════════════════════════════════════════════════════
# 载波同步链
# ═══════════════════════════════════════════════════════════════

def chain_foe_vv(rx, N_fft=DEF_NFFT, M_vv=DEF_MVV):
    rx_fo = apply_foe(rx, N_fft)
    out, _ = vv_cpr(rx_fo, M_vv)
    return out

def chain_foe_bps(rx, N_fft=DEF_NFFT, B=DEF_B_BPS, Nw=DEF_NW_BPS):
    rx_fo = apply_foe(rx, N_fft)
    out, _ = bps_cpr(rx_fo, B, Nw)
    return out

def chain_foe_dpll(rx, N_fft=DEF_NFFT, omega_n=DEF_WN):
    rx_fo = apply_foe(rx, N_fft)
    out, _ = dpll_track(rx_fo, omega_n)
    return out

def chain_foe_dpll_vv(rx, N_fft=DEF_NFFT, M_vv=DEF_MVV, omega_n=DEF_WN):
    rx_fo = apply_foe(rx, N_fft)
    tmp, _ = dpll_track(rx_fo, omega_n)
    out, _ = vv_cpr(tmp, M_vv)
    return out

METHODS = {
    'FOE+VV':      chain_foe_vv,
    'FOE+BPS':     chain_foe_bps,
    'FOE+DPLL':    chain_foe_dpll,
    'FOE+DPLL+VV': chain_foe_dpll_vv,
}

METHOD_STYLE = {
    'FOE+VV':      {'color': 'blue',   'marker': 'o', 'ls': '-'},
    'FOE+BPS':     {'color': 'green',  'marker': 's', 'ls': '-'},
    'FOE+DPLL':    {'color': 'red',    'marker': '^', 'ls': '-'},
    'FOE+DPLL+VV': {'color': 'purple', 'marker': 'D', 'ls': '-'},
}

TURB_STYLE = {
    'weak':     {'color': '#2ecc71', 'label': 'Weak ($\\alpha$=4.0, $\\beta$=3.0)'},
    'moderate': {'color': '#e67e22', 'label': 'Moderate ($\\alpha$=2.5, $\\beta$=1.8)'},
    'strong':   {'color': '#e74c3c', 'label': 'Strong ($\\alpha$=1.5, $\\beta$=0.8)'},
}

def run_method(name, rx, bits, **kwargs):
    rx_rec = METHODS[name](rx, **kwargs)
    return resolve_qpsk(rx_rec, bits)

# ═══════════════════════════════════════════════════════════════
# Exp1: BER vs 平均 SNR
# ═══════════════════════════════════════════════════════════════

def exp1_ber_vs_snr(Ns=10000, n_trials=50):
    snrs = np.arange(5, 31, 2.5)
    conditions = ['weak', 'moderate', 'strong']

    results = {}
    for cond in conditions:
        print(f"\n  {cond}")
        results[cond] = {m: [] for m in METHODS}
        for snr in snrs:
            bers = {m: [] for m in METHODS}
            for t in range(n_trials):
                rx, bits = generate_signal(Ns, cond, snr, seed=1000+t)
                for m in METHODS:
                    bers[m].append(run_method(m, rx, bits))
            for m in METHODS:
                results[cond][m].append(np.mean(bers[m]))
            v = ', '.join(f"{m}={results[cond][m][-1]:.4e}" for m in METHODS)
            print(f"    SNR={snr:5.1f}dB: {v}")

    # AWGN 参考（仅 FOE+VV）
    print("\n  AWGN reference")
    results['awgn'] = []
    for snr in snrs:
        bers = []
        for t in range(n_trials):
            rx, bits = generate_signal_awgn(Ns, snr, seed=1000+t)
            bers.append(run_method('FOE+VV', rx, bits))
        results['awgn'].append(np.mean(bers))
        print(f"    SNR={snr:5.1f}dB: BER={results['awgn'][-1]:.4e}")

    # 绘图: 3 子图
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    for ax, cond in zip(axes, conditions):
        # AWGN 参考线
        ax.semilogy(snrs, results['awgn'], 'k--', alpha=0.4, label='AWGN ref', lw=1)
        for m in METHODS:
            s = METHOD_STYLE[m]
            ax.semilogy(snrs, results[cond][m], color=s['color'], marker=s['marker'],
                       ls=s['ls'], label=m, ms=4, lw=1.2)
        ax.set_xlabel('$\\bar{\\gamma}$ (dB)')
        ax.set_ylabel('BER')
        ax.set_title(f'{cond.capitalize()} turbulence')
        ax.legend(fontsize=7, loc='lower left')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(1e-5, 1)
        ax.set_xlim(5, 30)

    plt.suptitle('BER vs Average SNR under Gamma-Gamma Turbulence')
    plt.tight_layout()
    plt.savefig(f'{OUT}/fig_ch4_ber_vs_snr.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n  -> fig_ch4_ber_vs_snr.png")
    return results

# ═══════════════════════════════════════════════════════════════
# Exp2: BER vs FOE 窗口长度
# ═══════════════════════════════════════════════════════════════

def exp2_foe_window(Ns=10000, n_trials=30, gamma_bar_db=20):
    nfft_vals = [128, 256, 512, 1024, 2048, 4096]
    conditions = ['weak', 'moderate', 'strong']

    results = {}
    for cond in conditions:
        print(f"\n  {cond}")
        results[cond] = {m: [] for m in METHODS}
        for Nf in nfft_vals:
            bers = {m: [] for m in METHODS}
            for t in range(n_trials):
                rx, bits = generate_signal(Ns, cond, gamma_bar_db, seed=2000+t)
                for m in METHODS:
                    bers[m].append(run_method(m, rx, bits, N_fft=Nf))
            for m in METHODS:
                results[cond][m].append(np.mean(bers[m]))
            v = ', '.join(f"{m}={results[cond][m][-1]:.4e}" for m in METHODS)
            print(f"    N_fft={Nf:5d}: {v}")

    # 绘图: 3 子图
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    for ax, cond in zip(axes, conditions):
        for m in METHODS:
            s = METHOD_STYLE[m]
            ax.semilogy(nfft_vals, results[cond][m], color=s['color'], marker=s['marker'],
                       ls=s['ls'], label=m, ms=6, lw=1.2)
        ax.set_xlabel('FOE Window $N_{FFT}$')
        ax.set_ylabel('BER')
        ax.set_title(f'{cond.capitalize()} turbulence, $\\bar{{\\gamma}}$={gamma_bar_db}dB')
        ax.legend(fontsize=7)
        ax.grid(True, alpha=0.3)
        ax.set_xscale('log', base=2)
        ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())

    plt.suptitle('BER vs FOE Window Length')
    plt.tight_layout()
    plt.savefig(f'{OUT}/fig_ch4_foe_window.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n  -> fig_ch4_foe_window.png")
    return results

# ═══════════════════════════════════════════════════════════════
# Exp3: BER vs CPR 参数
# ═══════════════════════════════════════════════════════════════

def exp3_cpr_params(Ns=10000, n_trials=30, gamma_bar_db=20):
    conditions = ['weak', 'moderate', 'strong']

    # 3a: VV 窗口扫描
    mvv_vals = [8, 16, 32, 64, 128, 256]
    vv_results = {}
    for cond in conditions:
        print(f"\n  VV sweep, {cond}")
        vv_results[cond] = []
        for Mv in mvv_vals:
            bers = []
            for t in range(n_trials):
                rx, bits = generate_signal(Ns, cond, gamma_bar_db, seed=3000+t)
                bers.append(run_method('FOE+VV', rx, bits, M_vv=Mv))
            vv_results[cond].append(np.mean(bers))
            print(f"    M_vv={Mv:4d}: BER={vv_results[cond][-1]:.4e}")

    # 3b: DPLL 带宽扫描
    bl_mhz = [0.5, 1, 2, 4, 8, 16, 32]
    wn_vals = [bl * 1e6 * 1.06 for bl in bl_mhz]  # B_L → omega_n
    dpll_results = {}
    for cond in conditions:
        print(f"\n  DPLL sweep, {cond}")
        dpll_results[cond] = []
        for wn in wn_vals:
            bers = []
            for t in range(n_trials):
                rx, bits = generate_signal(Ns, cond, gamma_bar_db, seed=3000+t)
                bers.append(run_method('FOE+DPLL', rx, bits, omega_n=wn))
            dpll_results[cond].append(np.mean(bers))
            print(f"    B_L={wn/1.06/1e6:5.1f}MHz: BER={dpll_results[cond][-1]:.4e}")

    # 3c: BPS 窗口扫描
    nw_bps_vals = [11, 21, 41, 61, 81, 121]
    bps_results = {}
    for cond in conditions:
        print(f"\n  BPS sweep, {cond}")
        bps_results[cond] = []
        for Nw in nw_bps_vals:
            bers = []
            for t in range(n_trials):
                rx, bits = generate_signal(Ns, cond, gamma_bar_db, seed=3000+t)
                bers.append(run_method('FOE+BPS', rx, bits, Nw=Nw))
            bps_results[cond].append(np.mean(bers))
            print(f"    Nw={Nw:4d}: BER={bps_results[cond][-1]:.4e}")

    # 绘图: 3 子图 (VV / DPLL / BPS)
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # VV
    ax = axes[0]
    for cond in conditions:
        ts = TURB_STYLE[cond]
        ax.semilogy(mvv_vals, vv_results[cond], color=ts['color'], marker='o',
                   label=ts['label'], ms=5, lw=1.2)
    ax.axvline(DEF_MVV, color='gray', ls=':', alpha=0.5, label=f'Default ({DEF_MVV})')
    ax.set_xlabel('VV Window $M_{VV}$')
    ax.set_ylabel('BER')
    ax.set_title('FOE+VV: BER vs Window Length')
    ax.legend(fontsize=6)
    ax.grid(True, alpha=0.3)

    # DPLL
    ax = axes[1]
    for cond in conditions:
        ts = TURB_STYLE[cond]
        ax.semilogy(bl_mhz, dpll_results[cond], color=ts['color'], marker='s',
                   label=ts['label'], ms=5, lw=1.2)
    ax.axvline(DEF_WN/1.06/1e6, color='gray', ls=':', alpha=0.5,
              label=f'Default ({DEF_WN/1.06/1e6:.1f}MHz)')
    ax.set_xlabel('DPLL Bandwidth $B_L$ (MHz)')
    ax.set_ylabel('BER')
    ax.set_title('FOE+DPLL: BER vs Loop Bandwidth')
    ax.legend(fontsize=6)
    ax.grid(True, alpha=0.3)

    # BPS
    ax = axes[2]
    for cond in conditions:
        ts = TURB_STYLE[cond]
        ax.semilogy(nw_bps_vals, bps_results[cond], color=ts['color'], marker='D',
                   label=ts['label'], ms=5, lw=1.2)
    ax.axvline(DEF_NW_BPS, color='gray', ls=':', alpha=0.5, label=f'Default ({DEF_NW_BPS})')
    ax.set_xlabel('BPS Window $N_w$')
    ax.set_ylabel('BER')
    ax.set_title('FOE+BPS: BER vs Averaging Window')
    ax.legend(fontsize=6)
    ax.grid(True, alpha=0.3)

    plt.suptitle(f'CPR Parameter Sensitivity, $\\bar{{\\gamma}}$={gamma_bar_db}dB')
    plt.tight_layout()
    plt.savefig(f'{OUT}/fig_ch4_cpr_params.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n  -> fig_ch4_cpr_params.png")
    return vv_results, dpll_results, bps_results

# ═══════════════════════════════════════════════════════════════
# Exp4: 湍流强度综合对比
# ═══════════════════════════════════════════════════════════════

def exp4_turbulence_summary(Ns=10000, n_trials=50, gamma_bar_db=20):
    conditions = ['weak', 'moderate', 'strong']

    results = {}
    for cond in conditions:
        print(f"\n  {cond}")
        results[cond] = {}
        for m in METHODS:
            bers = []
            for t in range(n_trials):
                rx, bits = generate_signal(Ns, cond, gamma_bar_db, seed=4000+t)
                bers.append(run_method(m, rx, bits))
            results[cond][m] = np.mean(bers)
            print(f"    {m:15s}: BER={results[cond][m]:.4e}")

    # 绘图: 分组柱状图
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(conditions))
    w = 0.18
    for i, m in enumerate(METHODS):
        vals = [results[cond][m] for cond in conditions]
        s = METHOD_STYLE[m]
        ax.bar(x + i*w - 1.5*w, vals, w, label=m, color=s['color'], alpha=0.85)

    ax.set_xticks(x)
    ax.set_xticklabels([c.capitalize() for c in conditions])
    ax.set_ylabel('BER')
    ax.set_title(f'Carrier Sync Comparison at $\\bar{{\\gamma}}$={gamma_bar_db}dB')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_yscale('log')
    ax.set_ylim(1e-5, 1)

    plt.tight_layout()
    plt.savefig(f'{OUT}/fig_ch4_turbulence_summary.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n  -> fig_ch4_turbulence_summary.png")
    return results

# ═══════════════════════════════════════════════════════════════
# 主程序
# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    t0 = time.time()
    print("="*60)
    print("Ch4 Systematic Analysis — Carrier Sync under GG Turbulence")
    print(f"Output: {OUT}")
    print("="*60)

    print("\n[1/4] Exp1: BER vs SNR (this takes a few minutes)...")
    exp1 = exp1_ber_vs_snr()

    print("\n[2/4] Exp2: BER vs FOE window...")
    exp2 = exp2_foe_window()

    print("\n[3/4] Exp3: BER vs CPR parameters...")
    exp3 = exp3_cpr_params()

    print("\n[4/4] Exp4: Turbulence summary...")
    exp4 = exp4_turbulence_summary()

    dt = time.time() - t0
    print(f"\n{'='*60}")
    print(f"Done! {dt:.1f}s")
    print(f"Figures saved to: {OUT}/")
    print("  fig_ch4_ber_vs_snr.png")
    print("  fig_ch4_foe_window.png")
    print("  fig_ch4_cpr_params.png")
    print("  fig_ch4_turbulence_summary.png")
    print("="*60)
