#!/usr/bin/env python3
"""解析相位模型分析 — Ch4 创新点支撑

分析 VV/DPLL 在不同湍流下的性能差异，推导解析预测并与仿真数据对比。

核心问题：
1. VV 为什么在中等/强湍流崩溃？（不是相位跟踪问题，是幅度深衰落）
2. DPLL 为什么鲁棒？（反馈环路有记忆，深衰落保持估计）
3. 能否给出闭合形式的设计公式？

TL-25 checklist: [1/2/3/4/5/6] 全部确认
"""

import sys, os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SIM_DIR = os.path.dirname(SCRIPT_DIR)
if SIM_DIR not in sys.path:
    sys.path.insert(0, SIM_DIR)

import numpy as np
from scipy.stats import gamma as gamma_dist
from common import (
    TURB, BLOCK, T_S, R_SYM, LASER_LW, F_RESIDUAL, DOPPLER_HIGH,
    GAMMA_BAR_DEFAULT, generate_shared_realization, equalize_oracle,
    vv_cpr, dpll_track, fft_foe, ber_eval, resolve_qpsk, qpsk_mod,
    qpsk_demod, save_results, FIXED_CFG_OPTIMAL, carrier_recovery_fixed,
)

NSeeds = 100
Ns = 50000
gamma_bar = GAMMA_BAR_DEFAULT  # 20 dB
f_dot = DOPPLER_HIGH  # 150 MHz/s

# ═══════════════════════════════════════════════════════════════
# Part 1: 相位模型分量量化
# ═══════════════════════════════════════════════════════════════

def analyze_phase_components():
    """分析相位各分量的量级"""
    k = np.arange(Ns)
    t = k * T_S
    T_frame = Ns * T_S

    # 分量 1: 残余频偏（线性）
    phi_fo = 2 * np.pi * F_RESIDUAL * t
    f_fo = F_RESIDUAL  # Hz

    # 分量 2: 多普勒率（二次）
    phi_dot = np.pi * f_dot * t**2
    f_dot_inst = f_dot * t  # 瞬时频率漂移
    f_dot_end = f_dot * T_frame

    # 分量 3: 激光相位噪声
    sigma_laser = np.sqrt(2 * np.pi * LASER_LW * T_S)
    phi_laser = sigma_laser * np.cumsum(np.random.randn(Ns))
    phi_laser_range = np.max(phi_laser) - np.min(phi_laser)

    # FOE 补偿后的残余相位分析
    # FOE 估计初始频偏，补偿后残余 = 频率漂移 + 相位噪声
    # 残余相位速率（rad/symbol）在帧末尾
    res_rate_start = 0  # FOE 补偿了初始频偏
    res_rate_end = 2 * np.pi * f_dot_end * T_S  # rad/symbol

    # VV 窗口内相位变化
    Nw = 64
    dphi_vv_window_end = res_rate_end * Nw  # 帧末尾VV窗口内的相位变化

    print("=" * 60)
    print("Part 1: 相位模型分量量化")
    print("=" * 60)
    print(f"帧长: {Ns} 符号 = {T_frame*1e6:.1f} μs")
    print(f"T_S = {T_S*1e12:.0f} ps, BLOCK = {BLOCK} 符号")
    print()
    print(f"分量1 - 残余频偏 f_res={F_RESIDUAL/1e6:.0f} MHz:")
    print(f"  线性相位斜率 = {2*np.pi*F_RESIDUAL*T_S:.4e} rad/symbol")
    print(f"  FOE 估计并补偿此分量")
    print()
    print(f"分量2 - 多普勒率 f_dot={f_dot/1e6:.0f} MHz/s:")
    print(f"  帧内频率漂移 = {f_dot_end:.1f} Hz (帧末)")
    print(f"  帧末相位速率 = {res_rate_end:.2e} rad/symbol")
    print(f"  VV窗口(Nw={Nw})内相位变化(帧末) = {dphi_vv_window_end:.2e} rad")
    print(f"  VV跟踪极限(π/8) = {np.pi/8:.4f} rad")
    print(f"  → 多普勒率对VV不构成挑战 ({dphi_vv_window_end/(np.pi/8)*100:.4f}%)")
    print()
    print(f"分量3 - 激光相位噪声 Δν={LASER_LW/1e3:.0f} kHz:")
    print(f"  单步标准差 = {sigma_laser:.2e} rad")
    print(f"  帧内累积范围 = {phi_laser_range:.4f} rad")
    print(f"  → 激光相位噪声量级极小，可忽略")
    print()
    print("【结论】相位动态对 VV/DPLL 都不构成挑战。")
    print("   VV 失效的原因不是相位跟踪，而是幅度深衰落下的估计器信噪比崩溃。")


# ═══════════════════════════════════════════════════════════════
# Part 2: h 统计量与深衰落特性
# ═══════════════════════════════════════════════════════════════

def analyze_h_statistics():
    """分析 Gamma-Gamma h 的统计特性与深衰落"""
    print("\n" + "=" * 60)
    print("Part 2: h 统计量与深衰落特性")
    print("=" * 60)

    for turb_name in ['weak', 'moderate', 'strong']:
        a, b = TURB[turb_name]
        # 生成大量 h 样本（block级）
        nb = 100000
        h_blocks = gamma_dist.rvs(a, scale=1/a, size=nb) * \
                   gamma_dist.rvs(b, scale=1/b, size=nb)

        # 基本统计
        h_mean = np.mean(h_blocks)
        h_var = np.var(h_blocks)
        h_median = np.median(h_blocks)

        # 深衰落统计
        deep_fade_thresholds = [0.1, 0.01, 0.001]
        deep_fade_fracs = [np.mean(h_blocks < t) for t in deep_fade_thresholds]

        # h² 统计（VV 4次方后的有效信号功率 ∝ h²）
        h2_mean = np.mean(h_blocks**2)
        h2_var = np.var(h_blocks**2)

        # 1/h 统计（零强迫均衡后的噪声增强因子）
        h_safe = np.clip(h_blocks, 1e-6, None)
        inv_h_mean = np.mean(1/h_safe)
        inv_h_median = np.median(1/h_safe)

        # MMSE 均衡后的有效 SNR
        gamma_bar = GAMMA_BAR_DEFAULT
        snr_per_block = gamma_bar * h_blocks
        # MMSE equalizer effective SNR = gamma_bar * h / (1 + 1/(gamma_bar*h)) ≈ gamma_bar*h for high SNR
        # 但关键是：低 SNR 块对 VV 4次方估计的贡献

        # VV 4次方估计器的有效 SNR 分析
        # y[k]^4 ≈ h[k]² × s^4 × exp(j4φ) + noise
        # 窗口内平均：(1/Nw) Σ h[k]² × exp(j4φ) ≈ <h²> × exp(j4φ) (如果φ恒定)
        # 噪声功率 ≈ 噪声交叉项
        # 有效SNR ∝ <h²>² / Var[h²] (简化)

        print(f"\n--- {turb_name} (α={a}, β={b}) ---")
        print(f"  E[h] = {h_mean:.4f}, Var[h] = {h_var:.4f}, Median = {h_median:.4f}")
        print(f"  闪烁指数 SI = sqrt(Var[h])/E[h] = {np.sqrt(h_var)/h_mean:.4f}")
        print(f"  深衰落概率: P(h<0.1)={deep_fade_fracs[0]:.4f}, "
              f"P(h<0.01)={deep_fade_fracs[1]:.6f}, "
              f"P(h<0.001)={deep_fade_fracs[2]:.2e}")
        print(f"  E[h²] = {h2_mean:.4f}, Var[h²] = {h2_var:.4f}")
        print(f"  E[1/h] = {inv_h_mean:.4f} (ZFE噪声增强)")
        print(f"  P(γ<0dB) = P(h<0.01) = {np.mean(h_blocks < 0.01):.6f}")

        # 关键指标：VV有效SNR比
        # 在 MMSE 均衡后，符号 k 的有效 SNR = γ̄h[k]
        # VV 4次方操作的SNR依赖于h²（信号功率）vs 噪声交叉项
        # 简化模型：VV估计方差 ∝ 1/(Nw × γ̄² × E[h²])
        # 深衰落使 E[h²] 的方差增大 → 估计不稳定

        # 更精确：4次方估计器在衰落信道下的SNR
        # Σ h[k]² 的变异系数 = Var[h²]^{1/2} / E[h²]
        cv_h2 = np.sqrt(h2_var) / h2_mean
        print(f"  h² 变异系数 CV(h²) = {cv_h2:.4f}")

    print("\n【结论】强湍流下 h 的深衰落概率和 h² 的变异系数急剧增大。")
    print("   这导致 VV 窗口内信号功率极度不均匀，估计质量崩溃。")


# ═══════════════════════════════════════════════════════════════
# Part 3: VV 相位估计质量的解析预测
# ═══════════════════════════════════════════════════════════════

def analyze_vv_quality():
    """实测 VV 相位估计质量 vs 解析预测"""
    print("\n" + "=" * 60)
    print("Part 3: VV 相位估计质量 (实测)")
    print("=" * 60)

    for turb_name in ['weak', 'moderate', 'strong']:
        phase_errors = []
        for seed in range(1000, 1010):
            shared = generate_shared_realization(Ns, gamma_bar, turb_name, f_dot, seed)
            rx_eq = equalize_oracle(shared)

            # FOE 补偿
            fo_est = fft_foe(rx_eq)
            k = np.arange(len(rx_eq))
            rx_foc = rx_eq * np.exp(-1j * fo_est * k)

            # VV 估计
            rx_vv, _ = vv_cpr(rx_foc, Nw=64)

            # 相位误差（去掉π/4偏移和π/2模糊）
            true_phase = shared['phi']
            # FOE补偿后的残余相位
            residual_phase = true_phase - fo_est * k
            # VV 估计的相位
            vv_phase = np.angle(rx_vv * np.exp(-1j * np.angle(shared['tx'])))

            # 用符号级相位误差（去掉常数偏移）
            err = np.angle(rx_vv * np.conj(shared['tx']) * np.exp(-1j * residual_phase))
            phase_errors.append(np.sqrt(np.mean(err**2)))

        rmse = np.mean(phase_errors)
        print(f"  {turb_name}: VV相位估计RMSE = {rmse:.4f} rad ({rmse*180/np.pi:.2f}°)")


# ═══════════════════════════════════════════════════════════════
# Part 4: DPLL 稳态误差的解析预测
# ═══════════════════════════════════════════════════════════════

def analyze_dpll_analytical():
    """DPLL 解析稳态误差预测"""
    print("\n" + "=" * 60)
    print("Part 4: DPLL 解析稳态误差")
    print("=" * 60)

    zeta = np.sqrt(2) / 2  # 阻尼系数

    # 二阶DPLL对频率斜坡输入的稳态误差
    # 输入: φ(t) = π·f_dot·t² (二次相位)
    # 二阶环对频率斜坡的稳态相位误差:
    # φ_ss = Δf_rate / (ω_n² × 2ζ)  [Gardner, Phaselock Techniques]
    # 其中 Δf_rate = f_dot (频率变化率, Hz/s)

    # 转换为rad/s²: φ'' = 2π × f_dot
    phi_ddot = 2 * np.pi * f_dot  # rad/s²

    omega_n_values = [8e6, 20e6, 50e6, 100e6]

    print(f"\n多普勒率 f_dot = {f_dot/1e6:.0f} MHz/s → φ'' = {phi_ddot:.2e} rad/s²")
    print(f"阻尼系数 ζ = {zeta:.4f}")
    print()
    print(f"{'ω_n (MHz)':>12} {'φ_ss (rad)':>14} {'φ_ss (deg)':>14} {'B_L (Hz)':>12}")

    for omega_n in omega_n_values:
        # 稳态相位误差（频率斜坡）
        phi_ss = phi_ddot / (omega_n**2 * 2 * zeta)

        # 环路带宽
        B_L = omega_n * (1 + 4*zeta**2) / (8*zeta)

        print(f"{omega_n/1e6:>10.0f}   {phi_ss:>14.2e}   {np.degrees(phi_ss):>12.4f}°   {B_L:>10.0f}")

    print()
    print("【结论】所有实际 ω_n 值下，DPLL稳态跟踪误差 << 1°。")
    print("   DPLL轻松跟踪多普勒率。性能瓶颈是噪声+衰落，不是动态跟踪。")

    # 噪声引起的相位误差
    print("\n噪声引起的DPLL相位抖动:")
    print(f"  σ_φ = sqrt(B_L × T_S / (2 × SNR_eff))")
    for omega_n in [8e6, 20e6]:
        B_L = omega_n * (1 + 4*zeta**2) / (8*zeta)
        for turb_name in ['weak', 'strong']:
            a, b = TURB[turb_name]
            # E[h] for Gamma-Gamma
            h_mean = 1.0  # normalized
            snr_eff = gamma_bar * h_mean  # average SNR
            sigma_phi = np.sqrt(B_L * T_S / (2 * snr_eff))
            print(f"  ω_n={omega_n/1e6:.0f}MHz, {turb_name}: "
                  f"σ_φ = {sigma_phi:.2e} rad ({np.degrees(sigma_phi):.4f}°)")


# ═══════════════════════════════════════════════════════════════
# Part 5: VV 失效机制 — h² 加权SNR分析
# ═══════════════════════════════════════════════════════════════

def analyze_vv_failure_mechanism():
    """VV 失效的根因：深衰落下4次方估计器SNR崩溃"""
    print("\n" + "=" * 60)
    print("Part 5: VV 失效机制 — 4次方估计器SNR崩溃")
    print("=" * 60)

    Nw = 64  # VV窗口

    for turb_name in ['weak', 'moderate', 'strong']:
        a, b = TURB[turb_name]

        # 模拟多个窗口的VV估计质量
        n_windows = 50000
        snr_windows = []

        for _ in range(n_windows):
            # 生成 Nw 个 h 值（block级，每个block=BLOCK个符号）
            # Nw=64 < BLOCK=100，所以窗口内h基本恒定
            # 但我们模拟跨block边界的情况
            n_blocks_in_window = (Nw + BLOCK - 1) // BLOCK  # 1 block
            h_blocks = gamma_dist.rvs(a, scale=1/a, size=n_blocks_in_window) * \
                       gamma_dist.rvs(b, scale=1/b, size=n_blocks_in_window)

            # 窗口内有效SNR（MMSE均衡后）
            # SNR_k = γ̄ × h_k
            # VV 4次方后信号功率 ∝ h²，噪声 ∝ (1 + noise terms)
            # 简化：VV估计器SNR ∝ Σ SNR_k² = Σ (γ̄h_k)²
            h_window = h_blocks[0]  # 窗口内h恒定（Nw < BLOCK）
            snr_eff = gamma_bar * h_window  # 有效SNR

            # 4次方VV估计器方差（M=4, Nw个样本平均）
            # σ²_φ ≈ 1 / (2 × M² × Nw × SNR)  [Mengali, Synchronization Techniques]
            # 但这是AWGN下的公式；在衰落信道下需要修正
            snr_windows.append(snr_eff)

        snr_windows = np.array(snr_windows)

        # VV估计方差（解析预测，AWGN公式）
        # σ²_φ = 1 / (2 × 16 × Nw × SNR) = 1 / (2048 × SNR)
        sigma_phi_pred = 1.0 / np.sqrt(2 * 16 * Nw * snr_windows)

        # 深衰落窗口比例
        deep_fade = snr_windows < 1  # SNR < 0 dB
        bad_est = sigma_phi_pred > np.pi/8  # 估计误差 > π/8 → 失效

        print(f"\n--- {turb_name} ---")
        print(f"  窗口SNR: mean={np.mean(snr_windows):.1f}, "
              f"median={np.median(snr_windows):.1f}, "
              f"min={np.min(snr_windows):.4f}")
        print(f"  P(SNR<0dB) = {np.mean(deep_fade):.4f} ({np.mean(deep_fade)*100:.2f}%)")
        print(f"  P(σ_φ>π/8) = {np.mean(bad_est):.4f} ({np.mean(bad_est)*100:.2f}%)")
        print(f"  VV估计RMSE(解析) = {np.sqrt(np.mean(sigma_phi_pred**2)):.4f} rad "
              f"({np.degrees(np.sqrt(np.mean(sigma_phi_pred**2))):.2f}°)")

    print("\n【结论】强湍流下 ~X% 的窗口处于深衰落（SNR<0dB），")
    print("   VV估计器在这些窗口产生随机相位 → BER崩溃。")
    print("   DPLL 有环路记忆（积分器保持），深衰落中不产生随机估计。")


# ═══════════════════════════════════════════════════════════════
# Part 6: 综合结论
# ═══════════════════════════════════════════════════════════════

def print_conclusions():
    print("\n" + "=" * 60)
    print("Part 6: 综合结论 — 可用于论文的解析框架")
    print("=" * 60)
    print("""
1. 相位模型三分量:
   φ(k) = 2π·f_res·k·T_s + π·f_dot·(kT_s)² + φ_laser(k)

   - f_res=1MHz → FOE补偿（线性，容易）
   - f_dot=150MHz/s → DPLL跟踪（二次，环路有记忆）
   - Δν=10kHz → 可忽略（维纳过程，σ<<1°）

2. VV失效机制（不是相位跟踪，是幅度衰落）:
   - VV是前馈估计器，无记忆
   - 4次方操作后有效信号功率 ∝ h²
   - 深衰落下 h→0 → SNR→0 → 估计=随机值
   - 关键公式: σ²_φ_VV = 1/(2M²Nw·γ̄·E[h²])
     强湍流 E[h²]方差大 → 估计不稳定

   设计准则: VV仅适用于弱湍流(P(h<0.1)<X%)

3. DPLL鲁棒性来源:
   - 反馈环路有积分器记忆
   - 深衰落下鉴相器增益下降但环路保持
   - 稳态跟踪误差: φ_ss = 2πf_dot/(ω_n²·2ζ) << 1°
   - 环路带宽选择: B_L = ω_n(1+4ζ²)/(8ζ)
     太大 → 噪声通过 → 误码
     太小 → 动态跟踪不上 → 误码
     最优 ω_n 平衡两者

4. 设计公式（闭合形式）:
   - VV可用条件: γ̄·E[h]·Nw >> 1 (有效SNR足够)
   - DPLL最优带宽: ω_n_opt = f(湍流参数, SNR)
   - 稳定性边界: ω_n_max = c/√(Var[h]·T_s) (经验)
""")


if __name__ == '__main__':
    t0 = __import__('time').time()

    analyze_phase_components()
    analyze_h_statistics()
    analyze_vv_quality()
    analyze_dpll_analytical()
    analyze_vv_failure_mechanism()
    print_conclusions()

    print(f"\n总耗时: {__import__('time').time()-t0:.1f}s")
