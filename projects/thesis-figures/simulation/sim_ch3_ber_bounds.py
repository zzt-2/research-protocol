#!/usr/bin/env python3
"""Ch3 方向验证：GG 湍流 + 高斯相位误差联合下 QPSK BER 蒙特卡洛仿真
   验证目标：
   1. BER floor = 2Q(π/(4σ_φ))（高 SNR 渐近界）
   2. 平均 BER over GG fading + Gaussian phase error
   3. 不同湍流强度和相位误差方差的 BER 曲线
"""

import numpy as np
from scipy.stats import gamma as gamma_dist
from scipy.special import erfc
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

OUT = os.path.dirname(os.path.abspath(__file__))
np.random.seed(42)
plt.rcParams.update({'font.size': 11, 'figure.dpi': 150, 'font.family': 'serif'})

# ─── 参数 ──────────────────────────────────────────────────
TURB = {
    'weak':     (4.0, 3.0),
    'moderate': (2.5, 1.8),
    'strong':   (1.5, 0.8),
}
SIGMA_PHI_DEG = [2, 5, 10, 15]  # 相位误差标准差（度）
SNR_DB = np.arange(0, 41, 2)    # 平均 SNR (dB)
N_SYM = 500_000                  # 每个条件的仿真符号数

# ─── 基础函数 ──────────────────────────────────────────────
def gg_channel(N, alpha, beta):
    """Gamma-Gamma 信道增益 h"""
    X = gamma_dist.rvs(alpha, scale=1/alpha, size=N)
    Y = gamma_dist.rvs(beta,  scale=1/beta,  size=N)
    return X * Y  # E[h] = 1

def q_func(x):
    """Q 函数"""
    return 0.5 * erfc(x / np.sqrt(2))

def ber_qpsk_awgn(snr_lin):
    """AWGN 下 QPSK 理论 BER（无相位误差，无衰落）"""
    return q_func(np.sqrt(2 * snr_lin))

def ber_floor_theory(sigma_phi):
    """高 SNR BER floor: P(|φ| > π/4) = 2Q(π/(4σ_φ))"""
    return 2 * q_func(np.pi / (4 * sigma_phi))

def ber_qpsk_conditional(gamma, phi):
    """条件 BER: QPSK 在瞬时 SNR=γ 和相位误差=φ 下的 BER

    Gray-coded QPSK, 判决域为 ±π/4 象限:
    P_b ≈ Q(√(2γ) cos(φ+π/4)) + Q(√(2γ) cos(φ-π/4))
    """
    sqrt2g = np.sqrt(2 * np.maximum(gamma, 0))
    c1 = np.cos(phi + np.pi/4)
    c2 = np.cos(phi - np.pi/4)
    # 当 cos 值为负时 Q 值很大，对应相位误差严重时判决错误
    p = q_func(sqrt2g * c1) + q_func(sqrt2g * c2)
    return np.clip(p, 0, 1)

# ─── 蒙特卡洛仿真 ──────────────────────────────────────────
def mc_ber(avg_snr_db, alpha, beta, sigma_phi, N=N_SYM):
    """蒙特卡洛仿真: GG + Gaussian phase error + QPSK BER"""
    snr_lin = 10 ** (avg_snr_db / 10)
    h = gg_channel(N, alpha, beta)       # 信道增益
    phi = np.random.normal(0, sigma_phi, N)  # 相位误差
    gamma = snr_lin * h ** 2             # 瞬时 SNR
    ber = np.mean(ber_qpsk_conditional(gamma, phi))
    return ber

def ber_gg_only(avg_snr_db, alpha, beta, N=N_SYM):
    """仅 GG 衰落（无相位误差）的 BER，作为基准"""
    snr_lin = 10 ** (avg_snr_db / 10)
    h = gg_channel(N, alpha, beta)
    gamma = snr_lin * h ** 2
    return np.mean(ber_qpsk_awgn(gamma))

# ─── 实验 1：BER floor 验证 ────────────────────────────────
def experiment_ber_floor():
    """验证 BER floor = 2Q(π/(4σ_φ))"""
    print("="*60)
    print("实验 1: BER floor 验证")
    print("="*60)

    alpha, beta = TURB['moderate']
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))

    # 无相位误差基准
    ber_no_phase = [ber_gg_only(s, alpha, beta) for s in SNR_DB]
    ax.semilogy(SNR_DB, ber_no_phase, 'k--', linewidth=2, label='GG only (no phase error)')

    colors = plt.cm.tab10(np.linspace(0, 0.6, len(SIGMA_PHI_DEG)))
    for i, sigma_deg in enumerate(SIGMA_PHI_DEG):
        sigma_rad = np.radians(sigma_deg)
        ber_mc = [mc_ber(s, alpha, beta, sigma_rad) for s in SNR_DB]
        floor = ber_floor_theory(sigma_rad)

        ax.semilogy(SNR_DB, ber_mc, 'o-', color=colors[i], markersize=3,
                    label=f'MC: σ_φ = {sigma_deg}°')
        ax.axhline(y=floor, color=colors[i], linestyle=':', alpha=0.7,
                   label=f'Floor: 2Q(π/4σ_φ) = {floor:.2e}')

        # 找到 MC BER 接近 floor 的点
        ber_arr = np.array(ber_mc)
        floor_arr = np.full_like(ber_arr, floor)
        ratio = ber_arr / floor_arr
        converge_idx = np.where(ratio < 1.1)[0]
        if len(converge_idx) > 0:
            conv_snr = SNR_DB[converge_idx[0]]
            print(f"  σ_φ = {sigma_deg}°: floor = {floor:.2e}, MC converges at SNR ≥ {conv_snr} dB")
        else:
            print(f"  σ_φ = {sigma_deg}°: floor = {floor:.2e}, not yet converged at 40 dB")

    ax.set_xlabel('Average SNR (dB)')
    ax.set_ylabel('Average BER')
    ax.set_title('QPSK BER: GG Fading + Gaussian Phase Error\n(moderate turbulence: α=2.5, β=1.8)')
    ax.set_ylim([1e-7, 1])
    ax.set_xlim([0, 40])
    ax.legend(fontsize=8, ncol=2, loc='lower left')
    ax.grid(True, which='both', alpha=0.3)
    plt.tight_layout()
    path = os.path.join(OUT, 'fig_ch3_ber_floor.png')
    plt.savefig(path)
    print(f"  → {path}")
    plt.close()

# ─── 实验 2：不同湍流强度 ──────────────────────────────────
def experiment_turbulence():
    """不同湍流强度下的 BER（固定相位误差）"""
    print("\n" + "="*60)
    print("实验 2: 不同湍流强度下的 BER")
    print("="*60)

    sigma_deg = 10  # 固定 10° 相位误差
    sigma_rad = np.radians(sigma_deg)

    fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))

    for i, (tname, (alpha, beta)) in enumerate(TURB.items()):
        ax = axes[i]
        # 无相位误差
        ber_no = [ber_gg_only(s, alpha, beta) for s in SNR_DB]
        ax.semilogy(SNR_DB, ber_no, 'b--', linewidth=2, label='GG only')

        # 有相位误差
        ber_with = [mc_ber(s, alpha, beta, sigma_rad) for s in SNR_DB]
        ax.semilogy(SNR_DB, ber_with, 'r-', linewidth=2, label=f'GG + σ_φ={sigma_deg}°')

        # BER floor
        floor = ber_floor_theory(sigma_rad)
        ax.axhline(y=floor, color='gray', linestyle=':', label=f'Floor = {floor:.2e}')

        ax.set_xlabel('SNR (dB)')
        ax.set_ylabel('BER')
        ax.set_title(f'{tname} turbulence\n(α={alpha}, β={beta})')
        ax.set_ylim([1e-6, 1])
        ax.grid(True, which='both', alpha=0.3)
        ax.legend(fontsize=9)

        # 计算 floor 处的 SNR 惩罚
        # 找到无相位误差时 BER = floor 的 SNR
        ber_no_arr = np.array(ber_no)
        idx = np.where(ber_no_arr <= floor)[0]
        if len(idx) > 0:
            penalty = SNR_DB[idx[0]] - 0  # 近似惩罚
            print(f"  {tname}: BER floor reached, SNR penalty ≈ {SNR_DB[idx[0]]} dB")
        else:
            print(f"  {tname}: BER floor below simulation range")

    plt.tight_layout()
    path = os.path.join(OUT, 'fig_ch3_ber_turbulence.png')
    plt.savefig(path)
    print(f"  → {path}")
    plt.close()

# ─── 实验 3：BER floor vs σ_φ 关系 ─────────────────────────
def experiment_floor_vs_sigma():
    """BER floor 随 σ_φ 的变化"""
    print("\n" + "="*60)
    print("实验 3: BER floor vs σ_φ")
    print("="*60)

    sigma_deg_arr = np.arange(1, 30, 0.5)
    sigma_rad_arr = np.radians(sigma_deg_arr)
    floor_theory = [ber_floor_theory(s) for s in sigma_rad_arr]

    # MC 验证（高 SNR = 40 dB）
    alpha, beta = TURB['moderate']
    floor_mc = [mc_ber(40, alpha, beta, s) for s in sigma_rad_arr]

    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    ax.semilogy(sigma_deg_arr, floor_theory, 'b-', linewidth=2, label='Theory: 2Q(π/4σ_φ)')
    ax.semilogy(sigma_deg_arr, floor_mc, 'ro', markersize=4, label='MC (SNR=40 dB)')
    ax.set_xlabel('Phase error std σ_φ (degrees)')
    ax.set_ylabel('BER floor')
    ax.set_title('BER Floor vs Phase Error Std (QPSK)')
    ax.set_ylim([1e-8, 1])
    ax.grid(True, which='both', alpha=0.3)
    ax.legend()

    # 标注关键设计点
    for sd in [5, 10, 15]:
        f = ber_floor_theory(np.radians(sd))
        ax.axvline(x=sd, color='gray', linestyle=':', alpha=0.5)
        ax.annotate(f'σ_φ={sd}°\nfloor={f:.1e}', xy=(sd, f),
                   fontsize=8, ha='left', va='top')

    plt.tight_layout()
    path = os.path.join(OUT, 'fig_ch3_floor_vs_sigma.png')
    plt.savefig(path)
    print(f"  → {path}")
    plt.close()

    # 关键数值表
    print("\n  关键数值:")
    print(f"  {'σ_φ (deg)':>10} {'BER floor':>12} {'MC@40dB':>12}")
    for sd in [2, 5, 8, 10, 12, 15, 20]:
        sr = np.radians(sd)
        ft = ber_floor_theory(sr)
        mc = mc_ber(40, alpha, beta, sr)
        print(f"  {sd:>10} {ft:>12.2e} {mc:>12.2e}")

# ─── 实验 4：无衰落基准验证 BER floor 公式 ────────────────
def experiment_awgn_floor():
    """AWGN only（无衰落）直接验证 BER floor = 2Q(π/(4σ_φ))"""
    print("\n" + "="*60)
    print("实验 4: AWGN 无衰落基准 — 直接验证 BER floor")
    print("="*60)

    snr_high = np.arange(10, 61, 2)  # 高 SNR 范围

    fig, ax = plt.subplots(1, 1, figsize=(8, 5))

    # AWGN only, no phase error
    ber_awgn = [ber_qpsk_awgn(10**(s/10)) for s in snr_high]
    ax.semilogy(snr_high, ber_awgn, 'k--', linewidth=2, label='AWGN only')

    colors = plt.cm.tab10(np.linspace(0, 0.6, len(SIGMA_PHI_DEG)))
    for i, sigma_deg in enumerate(SIGMA_PHI_DEG):
        sigma_rad = np.radians(sigma_deg)
        ber_mc = []
        for s in snr_high:
            snr_lin = 10 ** (s / 10)
            phi = np.random.normal(0, sigma_rad, N_SYM)
            # AWGN: γ = SNR（固定）
            ber = np.mean(ber_qpsk_conditional(np.full(N_SYM, snr_lin), phi))
            ber_mc.append(ber)

        floor = ber_floor_theory(sigma_rad)
        ax.semilogy(snr_high, ber_mc, 'o-', color=colors[i], markersize=3,
                    label=f'MC: σ_φ = {sigma_deg}°')
        ax.axhline(y=floor, color=colors[i], linestyle=':', alpha=0.7,
                   label=f'Floor = {floor:.2e}')

        # 找收敛点
        ber_arr = np.array(ber_mc)
        floor_arr = np.full_like(ber_arr, floor)
        mask = ber_arr > 0
        ratio = ber_arr[mask] / floor_arr[mask]
        converge_idx = np.where(ratio < 1.05)[0]  # 5% 以内
        if len(converge_idx) > 0:
            conv_snr = snr_high[mask][converge_idx[0]]
            print(f"  σ_φ = {sigma_deg}°: floor = {floor:.2e}, converged at SNR ≥ {conv_snr} dB ✓")
        else:
            print(f"  σ_φ = {sigma_deg}°: floor = {floor:.2e}, not converged at 60 dB")

    ax.set_xlabel('SNR (dB)')
    ax.set_ylabel('BER')
    ax.set_title('AWGN + Gaussian Phase Error (no fading)\nDirect BER floor verification')
    ax.set_ylim([1e-8, 1])
    ax.set_xlim([10, 60])
    ax.legend(fontsize=8, ncol=2, loc='lower left')
    ax.grid(True, which='both', alpha=0.3)
    plt.tight_layout()
    path = os.path.join(OUT, 'fig_ch3_ber_awgn_floor.png')
    plt.savefig(path)
    print(f"  → {path}")
    plt.close()

# ─── 主函数 ────────────────────────────────────────────────
if __name__ == '__main__':
    print("Ch3 BER 闭合界蒙特卡洛验证")
    print(f"仿真符号数: {N_SYM:,}")
    print(f"SNR 范围: {SNR_DB[0]}~{SNR_DB[-1]} dB")

    experiment_ber_floor()
    experiment_turbulence()
    experiment_floor_vs_sigma()
    experiment_awgn_floor()

    print("\n" + "="*60)
    print("全部实验完成")
    print("="*60)
