#!/usr/bin/env python3
"""Ch3: GG + Gaussian Phase Error + QPSK 平均 BER 闭合解推导与验证

推导方法：Petkovic 2023 Fourier 级数法，GG 特例 (Málaga ρ=0)
核心公式:
  P_b = 3/8 - Σ_{n=1}^{N} (b_n^GG / n) exp(-n²σ_φ²/2) sin(nπ/4)

  b_n^GG = n / (2π Γ(α)Γ(β)) × G_{2,3}^{3,1}(αβ/γ̄ | 1-n/2, 1+n/2; α, β, 0)

SNR 模型: γ = γ̄ · h（相干检测，SNR ∝ 辐照度）
BER floor: Q(π/(4σ_φ))（标准 BER 定义，P_b = P_s/2）
"""

import numpy as np
from scipy.stats import gamma as gamma_dist
from scipy.special import erfc, erfcinv, gamma as gamma_func
import mpmath
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, time

OUT = os.path.dirname(os.path.abspath(__file__))
np.random.seed(42)
plt.rcParams.update({'font.size': 11, 'figure.dpi': 150, 'font.family': 'serif'})

# ─── 参数 ──────────────────────────────────────────────────
TURB = {
    'weak':     (4.0, 3.0),
    'moderate': (2.5, 1.8),
    'strong':   (1.5, 0.8),
}
SIGMA_PHI_DEG = [5, 10, 15]
SNR_DB = np.arange(0, 41, 2)
N_SYM = 500_000

# ─── 基础函数 ──────────────────────────────────────────────
def q_func(x):
    return 0.5 * erfc(x / np.sqrt(2))

def gg_channel(N, alpha, beta):
    X = gamma_dist.rvs(alpha, scale=1/alpha, size=N)
    Y = gamma_dist.rvs(beta,  scale=1/beta,  size=N)
    return X * Y

def ber_qpsk_conditional(gamma, phi):
    """QPSK 条件 BER (Gray coding, P_b = P_s/2)"""
    sqrt2g = np.sqrt(2 * np.maximum(gamma, 0))
    return 0.5 * (q_func(sqrt2g * np.cos(phi + np.pi/4)) +
                  q_func(sqrt2g * np.cos(phi - np.pi/4)))

def ber_floor_qpsk(sigma_phi):
    """BER floor = Q(π/(4σ_φ))"""
    return q_func(np.pi / (4 * sigma_phi))

# ─── Meijer-G 计算 ─────────────────────────────────────────
def bn_gg(n, alpha, beta, gamma_bar):
    """GG 信道的 Fourier 系数 b_n (Petkovic 2023 Eq.19)

    b_n^GG = n / (2π Γ(α)Γ(β)) × G_{2,3}^{3,1}(αβ/γ̄ | 1-n/2, 1+n/2; α, β, 0)
    """
    z = mpmath.mpf(alpha * beta) / mpmath.mpf(gamma_bar)
    # Meijer-G 参数: a_s = [1-n/2, 1+n/2], b_s = [α, β, 0]
    a_s = [1 - mpmath.mpf(n)/2, 1 + mpmath.mpf(n)/2]
    b_s = [mpmath.mpf(alpha), mpmath.mpf(beta), mpmath.mpf(0)]
    G = mpmath.meijerg([a_s[:0], a_s[0:]],  # m=0, n=2 → a_1...a_n=[], b_1...b_m=[]
                       [[], a_s],             # 实际上 meijerg 参数格式需要调整
                       # mpmath.meijerg([[a_n], [a_m]], [[b_n], [b_m]], z)
                       )
    # 正确的 mpmath.meijerg 调用格式:
    # meijerg([[a_1,...,a_n], [a_{n+1},...,a_p]], [[b_1,...,b_m], [b_{m+1},...,b_q]], z)
    # G_{p,q}^{m,n}: n 个上参数在 "an" 列表, m 个下参数在 "bm" 列表
    # 这里 G_{2,3}^{3,1}: n=1, m=3, p=2, q=3
    # an = [1-n/2] (前 n=1 个上参数)
    # aother = [1+n/2] (剩余 p-n=1 个上参数)
    # bm = [α, β, 0] (前 m=3 个下参数)
    # bother = [] (剩余 q-m=0 个下参数)
    return None  # placeholder, will fix below

def bn_gg_v2(n, alpha, beta, gamma_bar):
    """GG 信道的 Fourier 系数 b_n

    G_{2,3}^{3,1}(z | 1-n/2, 1+n/2; α, β, 0)
    mpmath: meijerg([[an], [ap]], [[bm], [bq]], z)
      an = [1-n/2]         (n=1 个上参数)
      ap = [1+n/2]         (p-n=1 个上参数)
      bm = [α, β, 0]      (m=3 个下参数)
      bq = []              (q-m=0 个下参数)
    """
    z = mpmath.mpf(alpha * beta) / mpmath.mpf(gamma_bar)
    an = [1 - mpmath.mpf(n)/2]
    ap = [1 + mpmath.mpf(n)/2]
    bm = [mpmath.mpf(alpha), mpmath.mpf(beta), mpmath.mpf(0)]
    bq = []
    G = mpmath.meijerg([an, ap], [bm, bq], z)
    coeff = mpmath.mpf(n) / (2 * mpmath.pi * mpmath.gamma(alpha) * mpmath.gamma(beta))
    return float(coeff * G)

# ─── 闭合解 BER 计算 ───────────────────────────────────────
def ber_closed_form(gamma_bar_db, alpha, beta, sigma_phi, N_terms=30):
    """Fourier 级数闭合解 (P_s/2 近似): 平均 BER

    P_b = 3/8 - Σ (b_n/n) exp(-n²σ²/2) sin(nπ/4)
    """
    gamma_bar = 10 ** (gamma_bar_db / 10)
    sigma_sq_half = sigma_phi ** 2 / 2

    total = 0.0
    for n in range(1, N_terms + 1):
        sin_val = np.sin(n * np.pi / 4)
        if abs(sin_val) < 1e-15:
            continue
        bn = bn_gg_v2(n, alpha, beta, gamma_bar)
        gauss_atten = np.exp(-n**2 * sigma_sq_half)
        total += bn / n * gauss_atten * sin_val

    return 3.0/8 - total

def ber_exact(gamma_bar_db, alpha, beta, sigma_phi, N_terms=30):
    """精确 BER (I/Q 通道分别积分)

    P_b = 1/2 - 2 Σ (b_n/n) exp(-n²σ²/2) sin(nπ/2) cos(nπ/4)

    推导: P_I = P(Q error) = 1 - ∫_{-3π/4}^{π/4} f_total(ψ) dψ
    P_b = (P_I + P_Q)/2 = P_I (对称性)
    """
    gamma_bar = 10 ** (gamma_bar_db / 10)
    sigma_sq_half = sigma_phi ** 2 / 2

    total = 0.0
    for n in range(1, N_terms + 1):
        sin_cos = np.sin(n * np.pi / 2) * np.cos(n * np.pi / 4)
        if abs(sin_cos) < 1e-15:
            continue
        bn = bn_gg_v2(n, alpha, beta, gamma_bar)
        gauss_atten = np.exp(-n**2 * sigma_sq_half)
        total += bn / n * gauss_atten * sin_cos

    return 0.5 - 2 * total

def ber_floor_series(sigma_phi, N_terms=50):
    """BER floor via Fourier series (b_n → 1/π at high SNR)"""
    sigma_sq_half = sigma_phi ** 2 / 2
    total = 0.0
    for n in range(1, N_terms + 1):
        sin_val = np.sin(n * np.pi / 4)
        if abs(sin_val) < 1e-15:
            continue
        total += np.exp(-n**2 * sigma_sq_half) * sin_val / n
    return 3.0/8 - total / np.pi

# ─── 中断概率 ─────────────────────────────────────────────
def gg_cdf(h_th, alpha, beta):
    """GG 分布 CDF: F_GG(h) = Meijer-G 闭合形式"""
    z = mpmath.mpf(alpha * beta * h_th)
    # G_{1,3}^{2,1}(z | 1; α, β, 0)
    # meijerg: an=[1], ap=[], bm=[α,β], bq=[0]
    G = mpmath.meijerg([[mpmath.mpf(1)], []],
                       [[mpmath.mpf(alpha), mpmath.mpf(beta)], [mpmath.mpf(0)]],
                       z)
    return float(G / (mpmath.gamma(alpha) * mpmath.gamma(beta)))

def ber_phase_avg(gamma_lin, sigma_phi, N_phi=200):
    """相位平均 BER: E_φ[P_b(γ,φ)]"""
    phi = np.linspace(-4*sigma_phi, 4*sigma_phi, N_phi)
    dphi = phi[1] - phi[0]
    weights = np.exp(-phi**2 / (2*sigma_phi**2)) / (sigma_phi * np.sqrt(2*np.pi))
    pb = ber_qpsk_conditional(np.full_like(phi, gamma_lin), phi)
    return np.sum(pb * weights) * dphi

def find_threshold_snr(p_target, sigma_phi, gamma_range=np.logspace(-1, 4, 1000)):
    """二分查找阈值 SNR: P_b_avg(γ_th) = P_target"""
    g_lo, g_hi = gamma_range[0], gamma_range[-1]
    floor = ber_floor_qpsk(sigma_phi)
    if p_target <= floor:
        return np.inf
    for _ in range(100):
        g_mid = np.sqrt(g_lo * g_hi)
        pb = ber_phase_avg(g_mid, sigma_phi)
        if pb > p_target:
            g_lo = g_mid
        else:
            g_hi = g_mid
        if abs(g_hi - g_lo) / g_mid < 1e-6:
            break
    return g_mid

def outage_probability(gamma_bar_db, alpha, beta, sigma_phi, p_target=1e-3):
    """中断概率: P_out = P(BER > P_target) = F_GG(γ_th / γ̄)"""
    gamma_bar = 10 ** (gamma_bar_db / 10)
    gamma_th = find_threshold_snr(p_target, sigma_phi)
    if np.isinf(gamma_th):
        return 1.0
    h_th = gamma_th / gamma_bar
    if h_th > 100:
        return 1.0
    return gg_cdf(h_th, alpha, beta)

# ─── MC 仿真 ───────────────────────────────────────────────
def mc_ber_linear(avg_snr_db, alpha, beta, sigma_phi, N=N_SYM):
    """MC 仿真 (γ = γ̄·h, 相干检测模型)"""
    snr_lin = 10 ** (avg_snr_db / 10)
    h = gg_channel(N, alpha, beta)
    gamma = snr_lin * h           # γ = γ̄·h (NOT h²)
    phi = np.random.normal(0, sigma_phi, N)
    return np.mean(ber_qpsk_conditional(gamma, phi))

# ─── 实验 1: BER 曲线对比 (闭合解 vs MC) ───────────────────
def experiment_ber_curves():
    print("=" * 60)
    print("实验 1: 闭合解 vs MC BER 曲线")
    print("=" * 60)

    alpha, beta = TURB['moderate']
    sigma_rad = np.radians(10)

    fig, ax = plt.subplots(1, 1, figsize=(9, 6))

    # 无相位误差基准
    mc_no_phase = []
    for s in SNR_DB:
        snr_lin = 10 ** (s / 10)
        h = gg_channel(N_SYM, alpha, beta)
        gamma = snr_lin * h
        mc_no_phase.append(np.mean(q_func(np.sqrt(2 * gamma))))
    ax.semilogy(SNR_DB, mc_no_phase, 'k--', lw=2, label='MC: GG only (no phase error)')

    # 有相位误差: 闭合解 vs MC
    ber_theory = []
    ber_mc = []
    for s in SNR_DB:
        t = ber_exact(s, alpha, beta, sigma_rad, N_terms=20)
        m = mc_ber_linear(s, alpha, beta, sigma_rad)
        ber_theory.append(max(t, 1e-12))
        ber_mc.append(max(m, 1e-12))

    floor_q = ber_floor_qpsk(sigma_rad)
    floor_series = ber_floor_series(sigma_rad)

    ax.semilogy(SNR_DB, ber_theory, 'b-', lw=2,
                label=f'Theory (exact I/Q): σ_φ=10°')
    ax.semilogy(SNR_DB, ber_mc, 'ro', ms=4,
                label=f'MC: σ_φ=10°')
    ax.axhline(y=floor_q, color='green', ls=':', lw=1.5,
               label=f'Floor Q(π/4σ_φ) = {floor_q:.2e}')
    ax.axhline(y=floor_series, color='blue', ls='-.', lw=1,
               label=f'Floor (series) = {floor_series:.2e}')

    # 误差分析
    ber_t = np.array(ber_theory)
    ber_m = np.array(ber_mc)
    valid = (ber_m > 1e-8) & (ber_t > 1e-8)
    if np.any(valid):
        ratios = ber_t[valid] / ber_m[valid]
        print(f"  Theory/MC ratio: min={ratios.min():.3f}, max={ratios.max():.3f}, "
              f"median={np.median(ratios):.3f}")
        abs_err = np.abs(ber_t[valid] - ber_m[valid]) / ber_m[valid]
        print(f"  Relative error: median={np.median(abs_err)*100:.1f}%, "
              f"max={abs_err.max()*100:.1f}%")

    ax.set_xlabel('Average SNR $\\bar{\\gamma}$ (dB)')
    ax.set_ylabel('Average BER $\\bar{P}_b$')
    ax.set_title(f'QPSK BER: GG Fading + Gaussian Phase Error\n'
                 f'(moderate: α={alpha}, β={beta}, σ_φ=10°)')
    ax.set_ylim([1e-7, 1])
    ax.set_xlim([0, 40])
    ax.legend(fontsize=9, loc='lower left')
    ax.grid(True, which='both', alpha=0.3)
    plt.tight_layout()
    path = os.path.join(OUT, 'fig_ch3_closed_form_vs_mc.png')
    plt.savefig(path)
    print(f"  → {path}")
    plt.close()

# ─── 实验 2: 不同 σ_φ 的 BER floor 验证 ────────────────────
def experiment_ber_floor():
    print("\n" + "=" * 60)
    print("实验 2: BER floor 验证")
    print("=" * 60)

    alpha, beta = TURB['moderate']
    sigma_deg_arr = [2, 5, 8, 10, 12, 15, 20]

    print(f"\n  {'σ_φ (deg)':>10} {'Q(π/4σ_φ)':>12} {'Series':>12} {'MC@40dB':>12}")
    print("  " + "-" * 50)

    for sd in sigma_deg_arr:
        sr = np.radians(sd)
        floor_q = ber_floor_qpsk(sr)
        floor_s = ber_floor_series(sr, N_terms=60)
        mc = mc_ber_linear(40, alpha, beta, sr)
        print(f"  {sd:>10} {floor_q:>12.2e} {floor_s:>12.2e} {mc:>12.2e}")

# ─── 实验 3: 不同湍流强度 ──────────────────────────────────
def experiment_turbulence():
    print("\n" + "=" * 60)
    print("实验 3: 不同湍流强度")
    print("=" * 60)

    sigma_rad = np.radians(10)

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    for i, (tname, (alpha, beta)) in enumerate(TURB.items()):
        ax = axes[i]
        ber_theory = []
        ber_mc = []
        for s in SNR_DB:
            t = ber_exact(s, alpha, beta, sigma_rad, N_terms=20)
            m = mc_ber_linear(s, alpha, beta, sigma_rad)
            ber_theory.append(max(t, 1e-12))
            ber_mc.append(max(m, 1e-12))

        floor_q = ber_floor_qpsk(sigma_rad)

        ax.semilogy(SNR_DB, ber_theory, 'b-', lw=2, label='Theory (Fourier)')
        ax.semilogy(SNR_DB, ber_mc, 'ro', ms=3, label='MC')
        ax.axhline(y=floor_q, color='green', ls=':', label=f'Floor = {floor_q:.2e}')

        ax.set_xlabel('SNR (dB)')
        ax.set_ylabel('BER')
        ax.set_title(f'{tname} turbulence\n(α={alpha}, β={beta})')
        ax.set_ylim([1e-7, 1])
        ax.grid(True, which='both', alpha=0.3)
        ax.legend(fontsize=8)

    plt.tight_layout()
    path = os.path.join(OUT, 'fig_ch3_turbulence_closed.png')
    plt.savefig(path)
    print(f"  → {path}")
    plt.close()

# ─── 实验 4: 系数 b_n 行为分析 ──────────────────────────────
def experiment_bn_analysis():
    print("\n" + "=" * 60)
    print("实验 4: b_n^GG 系数行为分析")
    print("=" * 60)

    alpha, beta = TURB['moderate']

    for snr_db in [0, 10, 20, 30, 40]:
        gamma_bar = 10 ** (snr_db / 10)
        print(f"\n  SNR = {snr_db} dB:")
        print(f"  {'n':>4} {'b_n':>12} {'n/2πΓ(α)Γ(β)':>15} {'b_n limit':>12}")
        for n in [1, 2, 3, 5, 10]:
            bn = bn_gg_v2(n, alpha, beta, gamma_bar)
            print(f"  {n:>4} {bn:>12.6f} {'':>15} {1/np.pi:>12.6f}")

# ─── 实验 5: 精确 BER vs P_s/2 近似 ────────────────────────
def experiment_exact_vs_approx():
    print("\n" + "=" * 60)
    print("实验 5: 精确 BER vs P_s/2 近似对比")
    print("=" * 60)

    alpha, beta = TURB['moderate']
    sigma_rad = np.radians(10)

    ber_approx = []
    ber_exact_arr = []
    ber_mc = []
    for s in SNR_DB:
        ba = ber_closed_form(s, alpha, beta, sigma_rad, N_terms=20)
        be = ber_exact(s, alpha, beta, sigma_rad, N_terms=20)
        m = mc_ber_linear(s, alpha, beta, sigma_rad)
        ber_approx.append(max(ba, 1e-12))
        ber_exact_arr.append(max(be, 1e-12))
        ber_mc.append(max(m, 1e-12))

    floor_q = ber_floor_qpsk(sigma_rad)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # 左图: BER 曲线
    ax1.semilogy(SNR_DB, ber_approx, 'b--', lw=2, label='P_s/2 近似')
    ax1.semilogy(SNR_DB, ber_exact_arr, 'g-', lw=2, label='精确 BER (I/Q 积分)')
    ax1.semilogy(SNR_DB, ber_mc, 'ro', ms=3, label='MC')
    ax1.axhline(y=floor_q, color='gray', ls=':', label=f'Floor = {floor_q:.2e}')
    ax1.set_xlabel('SNR (dB)')
    ax1.set_ylabel('BER')
    ax1.set_title(f'Exact vs Approx BER\n(α={alpha}, β={beta}, σ_φ=10°)')
    ax1.set_ylim([1e-7, 1])
    ax1.legend(fontsize=9)
    ax1.grid(True, which='both', alpha=0.3)

    # 右图: 相对误差
    ba = np.array(ber_approx)
    be = np.array(ber_exact_arr)
    bm = np.array(ber_mc)
    valid = (bm > 1e-8) & (be > 1e-8)
    err_approx = np.abs(ba[valid] - bm[valid]) / bm[valid] * 100
    err_exact = np.abs(be[valid] - bm[valid]) / bm[valid] * 100
    snr_valid = SNR_DB[valid]

    ax2.plot(snr_valid, err_approx, 'b--o', ms=3, label='P_s/2 近似误差')
    ax2.plot(snr_valid, err_exact, 'g-^', ms=3, label='精确 BER 误差')
    ax2.set_xlabel('SNR (dB)')
    ax2.set_ylabel('Relative Error (%)')
    ax2.set_title('Relative Error vs MC')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim([0, max(err_approx.max(), err_exact.max()) * 1.2])

    plt.tight_layout()
    path = os.path.join(OUT, 'fig_ch3_exact_vs_approx.png')
    plt.savefig(path)
    print(f"  → {path}")
    plt.close()

    print(f"  P_s/2 近似: median={np.median(err_approx):.1f}%, max={err_approx.max():.1f}%")
    print(f"  精确 BER:   median={np.median(err_exact):.1f}%, max={err_exact.max():.1f}%")

# ─── 实验 6: 中断概率 ─────────────────────────────────────
def experiment_outage():
    print("\n" + "=" * 60)
    print("实验 6: 中断概率")
    print("=" * 60)

    alpha, beta = TURB['moderate']
    sigma_deg_arr = [0, 5, 10, 15]
    p_target = 1e-3
    snr_range = np.arange(0, 51, 2)

    # MC 验证中断概率
    print(f"\n  目标 BER = {p_target:.0e}")
    print(f"  {'σ_φ (deg)':>10} {'γ_th (dB)':>10} {'理论':>12}")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    for sd in sigma_deg_arr:
        sr = np.radians(sd) if sd > 0 else 0

        # 阈值 SNR
        if sr > 0:
            gamma_th = find_threshold_snr(p_target, sr)
        else:
            # 无相位误差: P_b = Q(sqrt(gamma)), gamma_th = [Q^{-1}(P_target)]^2
            gamma_th = (erfcinv(2 * p_target))**2 * 2

        # 理论中断概率
        pout_theory = []
        for s in snr_range:
            gamma_bar = 10 ** (s / 10)
            if np.isinf(gamma_th):
                pout_theory.append(1.0)
            else:
                h_th = gamma_th / gamma_bar
                pout_theory.append(gg_cdf(h_th, alpha, beta))

        th_db = 10 * np.log10(gamma_th) if not np.isinf(gamma_th) else float('inf')
        ax1.semilogy(snr_range, pout_theory, lw=2,
                     label=f'σ_φ={sd}° (γ_th={th_db:.1f}dB)')

        # 关键数值
        for s_idx, s in enumerate(snr_range):
            if pout_theory[s_idx] < 0.01:
                print(f"  {sd:>10} {th_db:>10.1f} P_out={pout_theory[s_idx]:.2e} @ {s}dB")
                break

    ax1.set_xlabel('Average SNR $\\bar{\\gamma}$ (dB)')
    ax1.set_ylabel('Outage Probability $P_{out}$')
    ax1.set_title(f'Outage Probability (P_target = {p_target:.0e})\n(moderate: α={alpha}, β={beta})')
    ax1.set_ylim([1e-4, 1])
    ax1.legend(fontsize=9)
    ax1.grid(True, which='both', alpha=0.3)

    # 右图: 不同湍流的中断概率 (固定 σ_φ=10°)
    sigma_rad = np.radians(10)
    gamma_th_fixed = find_threshold_snr(p_target, sigma_rad)
    th_db_fixed = 10 * np.log10(gamma_th_fixed)

    for tname, (a, b) in TURB.items():
        pout = [gg_cdf(gamma_th_fixed / (10**(s/10)), a, b) for s in snr_range]
        ax2.semilogy(snr_range, pout, lw=2, label=f'{tname} (α={a}, β={b})')

    ax2.set_xlabel('Average SNR (dB)')
    ax2.set_ylabel('Outage Probability')
    ax2.set_title(f'Outage vs Turbulence\n(σ_φ=10°, γ_th={th_db_fixed:.1f}dB)')
    ax2.set_ylim([1e-4, 1])
    ax2.legend(fontsize=9)
    ax2.grid(True, which='both', alpha=0.3)

    plt.tight_layout()
    path = os.path.join(OUT, 'fig_ch3_outage.png')
    plt.savefig(path)
    print(f"  → {path}")
    plt.close()

# ─── 主函数 ────────────────────────────────────────────────
if __name__ == '__main__':
    print("Ch3: GG + Gaussian Phase Error + QPSK BER 闭合解验证")
    print(f"SNR 模型: γ = γ̄·h (相干检测)")
    print(f"BER floor: Q(π/(4σ_φ))")
    print()

    t0 = time.time()
    experiment_bn_analysis()
    experiment_ber_floor()
    experiment_ber_curves()
    experiment_turbulence()
    experiment_exact_vs_approx()
    experiment_outage()

    print(f"\n总耗时: {time.time()-t0:.1f}s")
    print("=" * 60)
    print("全部实验完成")
    print("=" * 60)
