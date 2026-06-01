#!/usr/bin/env python3
"""系数调优 — 反推自适应公式系数使Ch4载波同步方案实际可用

问题诊断:
  当前系数下，20dB SNR (gamma_bar=100), h=0.3-0.8:
  - FOE: N_opt = 80/(100*h^2) 总是 <256 → clip到floor=256, 无法匹配fixed=1024
  - VV:  M_opt ~22 vs fixed=64 (太短, 更大噪声)
  - DPLL: B_L > fixed (更多噪声穿透)
  结论: 自适应在全部6场景比fixed差

方法:
  1. 从fixed参数反推所需系数
  2. 系统扫描系数倍率
  3. 最优系数集合上跑完整MVE

复用 sim_direction_a.py 的信号模型和全部原语。
"""

import numpy as np
from scipy.stats import gamma as gamma_dist
import sys, os, time

# 直接import原仿样的参数和原语
SIM_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SIM_DIR)

from sim_direction_a import (
    T_S, R_SYM, LASER_LW, F_RESIDUAL, TURB, BLOCK,
    DOPPLER_HIGH, DOPPLER_LOW, FIXED_CFG,
    gg_block, qpsk_mod, qpsk_demod, awgn, ber, resolve_qpsk, amp_limit,
    doppler_phase, fft_foe, dpll_track, vv_cpr,
    carrier_recovery_fixed,
)

np.random.seed(42)

# ═══════════════════════════════════════════════════════════════
# Step 0: 反推系数 — 从fixed参数反算每个公式需要的系数
# ═══════════════════════════════════════════════════════════════
def reverse_engineer_coefficients():
    """在典型工作点反推各公式系数, 使adaptive参数匹配fixed baseline"""
    print("=" * 70)
    print("STEP 0: 反推系数 — 从fixed参数反算公式系数")
    print("=" * 70)

    gamma_bar_db = 20
    gamma_bar = 10 ** (gamma_bar_db / 10)  # 100

    # 固定基准值
    N_fixed = 1024
    M_fixed = 64
    wn_fixed = 8e6  # omega_n fixed
    B_L_fixed = wn_fixed * 0.53  # ~8.48 MHz

    print(f"\nFixed baseline: N={N_fixed}, M={M_fixed}, omega_n={wn_fixed/1e6:.1f} MHz, B_L={B_L_fixed/1e6:.2f} MHz")
    print(f"gamma_bar = {gamma_bar}")

    # 典型h值 (强湍流中位数 ~0.5, 10th percentile ~0.2)
    h_points = [0.2, 0.3, 0.5, 0.8, 1.0]
    print(f"\n{'h':>6s} | {'C_foe (need)':>14s} | {'K_M (need)':>12s} | {'B0 (need)':>14s}")
    print("-" * 55)

    foe_coeffs = []
    km_coeffs = []
    b0_coeffs = []

    for h in h_points:
        gamma = gamma_bar * h

        # FOE: N_opt = C_foe / (gamma_bar * h^2) = N_fixed
        # => C_foe = N_fixed * gamma_bar * h^2
        C_foe = N_fixed * gamma_bar * h ** 2
        foe_coeffs.append(C_foe)

        # VV: M_opt = K_M * gamma^{-0.2} * (df*Ts)^{-0.4} = M_fixed
        # => K_M = M_fixed * gamma^{0.2} * (df*Ts)^{0.4}
        df_norm = F_RESIDUAL * T_S
        K_M_need = M_fixed * (gamma ** 0.2) * (df_norm ** 0.4)
        km_coeffs.append(K_M_need)

        # DPLL: B_L = B0 * h = B_L_fixed
        # => B0 = B_L_fixed / h
        B0_need = B_L_fixed / h
        b0_coeffs.append(B0_need)

        print(f"{h:6.2f} | {C_foe:14.1f} | {K_M_need:12.4f} | {B0_need/1e6:14.2f} MHz")

    print(f"\n总结 (匹配fixed参数所需的系数):")
    print(f"  FOE:  C_foe 原始=80, 反推范围={min(foe_coeffs):.0f}~{max(foe_coeffs):.0f}")
    print(f"        倍率范围: {min(foe_coeffs)/80:.0f}x ~ {max(foe_coeffs)/80:.0f}x")
    print(f"  VV:   K_M 原始={(3/4)**0.2:.4f}, 反推范围={min(km_coeffs):.4f}~{max(km_coeffs):.4f}")
    print(f"        倍率范围: {min(km_coeffs)/(3/4)**0.2:.1f}x ~ {max(km_coeffs)/(3/4)**0.5:.1f}x")
    print(f"  DPLL: B0 原始={np.sqrt(np.pi * LASER_LW * gamma_bar / T_S)/1e6:.2f} MHz, 反推范围={min(b0_coeffs)/1e6:.2f}~{max(b0_coeffs)/1e6:.2f} MHz")

    # 推荐起始点: h=0.5 (强湍流典型值)
    h_ref = 0.5
    gamma_ref = gamma_bar * h_ref
    C_foe_ref = N_fixed * gamma_bar * h_ref ** 2
    df_norm = F_RESIDUAL * T_S
    K_M_ref = M_fixed * (gamma_ref ** 0.2) * (df_norm ** 0.4)
    B0_ref = B_L_fixed / h_ref

    print(f"\n推荐参考点 (h={h_ref}):")
    print(f"  C_foe = {C_foe_ref:.0f} (原始80的 {C_foe_ref/80:.0f}x)")
    print(f"  K_M   = {K_M_ref:.4f} (原始{(3/4)**0.2:.4f}的 {K_M_ref/(3/4)**0.2:.1f}x)")
    print(f"  B0    = {B0_ref/1e6:.2f} MHz (原始{np.sqrt(np.pi * LASER_LW * gamma_bar / T_S)/1e6:.2f} MHz的 {B0_ref/np.sqrt(np.pi * LASER_LW * gamma_bar / T_S):.2f}x)")

    return {
        'C_foe_ref': C_foe_ref,
        'K_M_ref': K_M_ref,
        'B0_ref': B0_ref,
        'foe_coeffs': foe_coeffs,
        'km_coeffs': km_coeffs,
        'b0_coeffs': b0_coeffs,
    }


# ═══════════════════════════════════════════════════════════════
# 可调系数版adaptive_params
# ═══════════════════════════════════════════════════════════════
def adaptive_params_tuned(h_est, gamma_bar_db, C_foe, K_M, B0):
    """可调系数的自适应参数计算

    FOE:  N_opt = C_foe / (gamma_bar * h^2)     原始: C_foe=80
    VV:   M_opt = K_M * gamma^{-1/5} * (df*Ts)^{-2/5}  原始: K_M=(3/4)^0.2≈0.944
    DPLL: B_L = B0 * h                           原始: B0=sqrt(pi*LW*gamma_bar/Ts)
    """
    gamma_bar = 10 ** (gamma_bar_db / 10)
    h_safe = max(h_est, 0.001)
    gamma = gamma_bar * h_safe

    # FOE
    N_fft = int(np.clip(C_foe / (gamma_bar * h_safe ** 2 + 1e-10), 256, 8192))
    N_fft = int(2 ** np.ceil(np.log2(N_fft)))

    # VV
    df_norm = F_RESIDUAL * T_S
    M_vv = int(np.clip(K_M * gamma ** (-0.2) * df_norm ** (-0.4), 16, 256))
    M_vv = max(8, M_vv | 1) - 1

    # DPLL
    B_L = np.clip(B0 * h_safe, 0.5e6, 20e6)
    omega_n = B_L / 0.53  # omega_n = B_L / 0.53, since B_L = 0.53*omega_n when zeta=sqrt(2)/2

    return N_fft, M_vv, omega_n


def carrier_recovery_tuned(rx, h_est, gamma_bar_db, C_foe, K_M, B0, h_foe=None):
    """使用调优系数的自适应载波恢复"""
    if h_foe is None:
        h_foe = h_est
    N_foe, M_vv, omega_n = adaptive_params_tuned(h_foe, gamma_bar_db, C_foe, K_M, B0)

    fo_est = fft_foe(rx, N_fft=N_foe)
    rx_comp = rx * np.exp(-1j * fo_est * np.arange(len(rx)))
    rx_pll, _ = dpll_track(rx_comp, omega_n=omega_n, zeta=FIXED_CFG['zeta'])
    rx_cpr, _ = vv_cpr(rx_pll, Nw=M_vv)
    return rx_cpr


# ═══════════════════════════════════════════════════════════════
# Step 1: 系数扫描 — 只测强湍流低仰角(最困难场景)
# ═══════════════════════════════════════════════════════════════
def run_single_trial(Ns, turb_name, f_dot, gamma_bar_db, C_foe, K_M, B0, adaptive=True):
    """单次试验, 返回BER"""
    a, b = TURB[turb_name]
    bits = np.random.randint(0, 2, Ns * 2)
    tx = qpsk_mod(bits)

    h = gg_block(Ns, a, b)
    n_blocks = len(h) // BLOCK
    h_blocks = np.array([np.median(h[i * BLOCK:(i + 1) * BLOCK]) for i in range(n_blocks)])
    h_est = np.median(h_blocks)
    h_foe = np.percentile(h_blocks, 10)

    gamma_bar_lin = 10 ** (gamma_bar_db / 10)
    phi = doppler_phase(Ns, f_res=F_RESIDUAL, f_dot=f_dot)
    carrier = np.exp(1j * phi)

    signal = tx * np.sqrt(h) * carrier
    noise_var = 1.0 / (2 * gamma_bar_lin)
    noise = np.sqrt(noise_var) * (np.random.randn(Ns) + 1j * np.random.randn(Ns))
    rx = signal + noise

    rx_mmse = rx * np.sqrt(h) / (h + 1 / gamma_bar_lin)
    rx_mmse = amp_limit(rx_mmse, 3.0)

    if adaptive:
        rx_rec = carrier_recovery_tuned(rx_mmse, h_est, gamma_bar_db, C_foe, K_M, B0, h_foe=h_foe)
    else:
        rx_rec = carrier_recovery_fixed(rx_mmse)

    return resolve_qpsk(rx_rec, bits)


def sweep_coefficients():
    """系统扫描系数组合"""
    print("\n" + "=" * 70)
    print("STEP 1: 系数扫描 — 强湍流低仰角, SNR=20dB")
    print("=" * 70)

    Ns = 5000
    n_trials = 20
    gamma_bar_db = 20
    turb = 'strong'
    f_dot = DOPPLER_HIGH

    # 先测fixed baseline
    fixed_bers = []
    for t in range(n_trials):
        np.random.seed(500 + t)
        fixed_bers.append(run_single_trial(Ns, turb, f_dot, gamma_bar_db, 0, 0, 0, adaptive=False))
    fixed_mean = np.mean(fixed_bers)
    print(f"\nFixed baseline BER = {fixed_mean:.6f} ({n_trials} trials avg)")

    # FOE系数扫描: 80 * ratio
    foe_ratios = [1, 5, 10, 20, 50, 100, 200, 320, 500]
    # VV系数扫描: original_KM * ratio
    orig_KM = (3 / 4) ** 0.2
    km_ratios = [1, 2, 5, 10, 20, 50, 100]
    # DPLL B0: 从fixed反推的B0 (h=0.5时匹配fixed)
    gamma_bar = 10 ** (gamma_bar_db / 10)
    B0_original = np.sqrt(np.pi * LASER_LW * gamma_bar / T_S)
    # 固定B0到几个合理值: 原始, /2, 匹配fixed@h=0.5, 匹配fixed@h=0.3
    B_L_fixed = FIXED_CFG['omega_n'] * 0.53
    B0_values = {
        'original': B0_original,
        'match_h0.5': B_L_fixed / 0.5,
        'match_h0.3': B_L_fixed / 0.3,
        'match_h0.8': B_L_fixed / 0.8,
        'half_orig': B0_original / 2,
        'quarter_orig': B0_original / 4,
    }

    print(f"\n原始系数: C_foe=80, K_M={orig_KM:.4f}, B0={B0_original/1e6:.2f} MHz")
    print(f"Fixed B_L = {B_L_fixed/1e6:.2f} MHz")
    print(f"\nB0候选值:")
    for name, b0 in B0_values.items():
        print(f"  {name:15s}: {b0/1e6:.2f} MHz")

    # 三维扫描: FOE x VV x DPLL (先做粗扫)
    results = []
    total = len(foe_ratios) * len(km_ratios) * len(B0_values)
    count = 0

    print(f"\n扫描 {len(foe_ratios)} FOE x {len(km_ratios)} VV x {len(B0_values)} DPLL = {total} 组合")
    print(f"每组 {n_trials} trials x {Ns} symbols")
    print(f"{'C_foe':>10s} {'KM_ratio':>10s} {'B0_name':>15s} | {'BER':>10s} {'Gain_dB':>10s} {'N_typ':>6s} {'M_typ':>6s} {'BL_typ':>8s}")
    print("-" * 85)

    best_gain = -999
    best_config = None

    for foe_r in foe_ratios:
        C_foe = 80 * foe_r
        for km_r in km_ratios:
            K_M = orig_KM * km_r
            for b0_name, B0 in B0_values.items():
                count += 1

                bers = []
                for t in range(n_trials):
                    np.random.seed(500 + t)
                    bers.append(run_single_trial(Ns, turb, f_dot, gamma_bar_db, C_foe, K_M, B0, adaptive=True))

                mean_ber = np.mean(bers)
                if fixed_mean > 0 and mean_ber > 0 and mean_ber < fixed_mean:
                    gain_db = 10 * np.log10(fixed_mean / mean_ber)
                else:
                    gain_db = 0.0

                # 算典型参数 (h=0.5)
                h_typ = 0.5
                N_typ, M_typ, wn_typ = adaptive_params_tuned(h_typ, gamma_bar_db, C_foe, K_M, B0)
                BL_typ = wn_typ * 0.53 / 1e6

                results.append({
                    'C_foe': C_foe, 'foe_ratio': foe_r,
                    'K_M': K_M, 'km_ratio': km_r,
                    'B0': B0, 'b0_name': b0_name,
                    'ber': mean_ber, 'gain_db': gain_db,
                    'N_typ': N_typ, 'M_typ': M_typ, 'BL_typ': BL_typ,
                })

                if gain_db > best_gain:
                    best_gain = gain_db
                    best_config = results[-1]

                # 只打印有增益或接近的
                if gain_db > -0.5 or foe_r <= 50:
                    marker = " ***" if gain_db > 0.5 else (" **" if gain_db > 0 else "")
                    print(f"{C_foe:10d} {km_r:10.1f} {b0_name:>15s} | {mean_ber:10.6f} {gain_db:+10.3f} {N_typ:6d} {M_typ:6d} {BL_typ:8.2f}{marker}")

    print(f"\n扫描完成: {count} 组合")
    print(f"\n最佳配置 (强湍流低仰角):")
    bc = best_config
    print(f"  C_foe={bc['C_foe']} (原始80的 {bc['foe_ratio']}x)")
    print(f"  K_M={bc['K_M']:.4f} (原始{orig_KM:.4f}的 {bc['km_ratio']}x)")
    print(f"  B0={bc['B0']/1e6:.2f} MHz ({bc['b0_name']})")
    print(f"  BER={bc['ber']:.6f}  Gain={bc['gain_db']:+.3f} dB")
    print(f"  典型参数 (h=0.5): N={bc['N_typ']}, M={bc['M_typ']}, B_L={bc['BL_typ']:.2f} MHz")

    # 找出所有正增益的组合
    positive = sorted([r for r in results if r['gain_db'] > 0], key=lambda x: -x['gain_db'])
    if positive:
        print(f"\n正增益组合 ({len(positive)}/{len(results)}):")
        for r in positive[:10]:
            print(f"  C_foe={r['C_foe']:6d} ({r['foe_ratio']:3d}x)  K_M*r={r['km_ratio']:5.1f}x  B0={r['b0_name']:15s}  "
                  f"Gain={r['gain_db']:+.3f} dB  N={r['N_typ']} M={r['M_typ']} BL={r['BL_typ']:.1f}MHz")
    else:
        print("\n没有任何组合获得正增益!")

    return results, best_config


# ═══════════════════════════════════════════════════════════════
# Step 2: 最优系数精细扫描 (围绕最佳粗扫结果)
# ═══════════════════════════════════════════════════════════════
def fine_sweep(best_config):
    """围绕最佳粗扫结果做精细扫描"""
    print("\n" + "=" * 70)
    print("STEP 2: 精细扫描 — 围绕最佳粗扫结果")
    print("=" * 70)

    Ns = 5000
    n_trials = 30
    gamma_bar_db = 20
    turb = 'strong'
    f_dot = DOPPLER_HIGH

    # fixed baseline
    fixed_bers = []
    for t in range(n_trials):
        np.random.seed(500 + t)
        fixed_bers.append(run_single_trial(Ns, turb, f_dot, gamma_bar_db, 0, 0, 0, adaptive=False))
    fixed_mean = np.mean(fixed_bers)
    print(f"Fixed baseline BER = {fixed_mean:.6f}")

    orig_KM = (3 / 4) ** 0.2

    # 围绕best fine-tune
    base_foe = best_config['C_foe']
    base_km_r = best_config['km_ratio']
    base_b0 = best_config['B0']
    base_b0_name = best_config['b0_name']

    # FOE: 0.5x ~ 2x best
    foe_ratios = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0, 4.0]
    # KM: 0.5x ~ 3x best
    km_mults = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0]

    best_fine = None
    best_fine_gain = -999

    print(f"\n精细扫描基点: C_foe={base_foe}, K_M*r={base_km_r:.1f}, B0={base_b0_name}")
    print(f"{'foe_mult':>10s} {'km_mult':>10s} | {'BER':>10s} {'Gain_dB':>10s}")
    print("-" * 50)

    fine_results = []
    for fm in foe_ratios:
        C_foe = int(base_foe * fm)
        if C_foe < 80:
            C_foe = 80
        for km_m in km_mults:
            K_M = orig_KM * base_km_r * km_m

            bers = []
            for t in range(n_trials):
                np.random.seed(500 + t)
                bers.append(run_single_trial(Ns, turb, f_dot, gamma_bar_db, C_foe, K_M, base_b0, adaptive=True))

            mean_ber = np.mean(bers)
            if fixed_mean > 0 and mean_ber > 0 and mean_ber < fixed_mean:
                gain_db = 10 * np.log10(fixed_mean / mean_ber)
            else:
                gain_db = 0.0

            fine_results.append({
                'C_foe': C_foe, 'K_M': K_M, 'B0': base_b0,
                'ber': mean_ber, 'gain_db': gain_db,
                'foe_mult': fm, 'km_mult': km_m,
            })

            if gain_db > best_fine_gain:
                best_fine_gain = gain_db
                best_fine = fine_results[-1]

            marker = " ***" if gain_db > 0.5 else ""
            print(f"{fm:10.2f} {km_m:10.2f} | {mean_ber:10.6f} {gain_db:+10.3f}{marker}")

    print(f"\n精细扫描最佳:")
    bf = best_fine
    print(f"  C_foe={bf['C_foe']}, K_M={bf['K_M']:.4f}, B0={base_b0/1e6:.2f} MHz")
    print(f"  BER={bf['ber']:.6f}, Gain={bf['gain_db']:+.3f} dB")

    return best_fine


# ═══════════════════════════════════════════════════════════════
# Step 3: 完整MVE — 6场景 x 30次 x 10000符号
# ═══════════════════════════════════════════════════════════════
def run_full_mve(C_foe, K_M, B0, label="tuned"):
    """使用指定系数跑完整6场景MVE"""
    print("\n" + "=" * 70)
    print(f"STEP 3: 完整MVE — 系数: C_foe={C_foe}, K_M={K_M:.4f}, B0={B0/1e6:.2f} MHz")
    print("=" * 70)

    Ns = 10000
    n_trials = 30
    gamma_bar_db = 20

    scenarios = []
    for turb in ['weak', 'moderate', 'strong']:
        for elev, f_dot in [('low', DOPPLER_HIGH), ('high', DOPPLER_LOW)]:
            scenarios.append((turb, elev, f_dot))

    results = {}
    for turb, elev, f_dot in scenarios:
        scenario_label = f"{turb}_{elev}"
        print(f"\n  Scenario: {scenario_label} (f_dot={f_dot / 1e6:.0f} MHz/s)")

        bers_fixed = []
        bers_adapt = []
        for trial in range(n_trials):
            np.random.seed(42 + trial)
            bf = run_single_trial(Ns, turb, f_dot, gamma_bar_db, 0, 0, 0, adaptive=False)
            bers_fixed.append(bf)

            np.random.seed(42 + trial)
            ba = run_single_trial(Ns, turb, f_dot, gamma_bar_db, C_foe, K_M, B0, adaptive=True)
            bers_adapt.append(ba)

        mean_f = np.mean(bers_fixed)
        mean_a = np.mean(bers_adapt)
        if mean_f > 0 and mean_a > 0 and mean_a < mean_f:
            gain_db = 10 * np.log10(mean_f / mean_a)
        else:
            gain_db = 0.0

        status = "PASS" if gain_db > 0.5 else ("WEAK" if gain_db > 0 else "FAIL")
        results[scenario_label] = {
            'fixed_ber': mean_f,
            'adapt_ber': mean_a,
            'gain_db': gain_db,
        }
        print(f"    Fixed: {mean_f:.6f}  Adapt: {mean_a:.6f}  Gain: {gain_db:+.3f} dB [{status}]")

    # 汇总
    print(f"\n{'='*70}")
    print("MVE 汇总")
    print(f"{'='*70}")
    print(f"{'Scenario':>20s} | {'Fixed BER':>12s} | {'Adapt BER':>12s} | {'Gain (dB)':>10s} | {'Status':>8s}")
    print("-" * 72)

    n_pass = 0
    n_positive = 0
    for label, r in results.items():
        status = "PASS" if r['gain_db'] > 0.5 else ("WEAK" if r['gain_db'] > 0 else "FAIL")
        if r['gain_db'] > 0.5:
            n_pass += 1
        if r['gain_db'] > 0:
            n_positive += 1
        print(f"{label:>20s} | {r['fixed_ber']:12.6f} | {r['adapt_ber']:12.6f} | {r['gain_db']:+10.3f} | {status:>8s}")

    print(f"\n正增益: {n_positive}/6")
    print(f"≥0.5dB: {n_pass}/6")

    return results


# ═══════════════════════════════════════════════════════════════
# Step 4: 多湍流级别验证 (确保系数不只是对强湍流有效)
# ═══════════════════════════════════════════════════════════════
def cross_turbulence_check(C_foe, K_M, B0):
    """检查系数在不同湍流级别下的表现"""
    print("\n" + "=" * 70)
    print("STEP 4: 跨湍流级别验证")
    print("=" * 70)

    Ns = 5000
    n_trials = 20
    gamma_bar_db = 20

    print(f"\n{'Turbulence':>12s} {'Elevation':>10s} | {'Fixed':>10s} {'Adapt':>10s} {'Gain_dB':>10s} {'N_typ':>6s} {'M_typ':>6s} {'BL_typ':>8s}")
    print("-" * 80)

    for turb in ['weak', 'moderate', 'strong']:
        a, b = TURB[turb]
        for elev, f_dot in [('low', DOPPLER_HIGH), ('high', DOPPLER_LOW)]:
            bers_f, bers_a = [], []
            for t in range(n_trials):
                np.random.seed(700 + t)
                bers_f.append(run_single_trial(Ns, turb, f_dot, gamma_bar_db, 0, 0, 0, adaptive=False))
                np.random.seed(700 + t)
                bers_a.append(run_single_trial(Ns, turb, f_dot, gamma_bar_db, C_foe, K_M, B0, adaptive=True))

            mf, ma = np.mean(bers_f), np.mean(bers_a)
            gain = 10 * np.log10(mf / ma) if mf > 0 and ma > 0 and ma < mf else 0.0

            # 该湍流下的典型h值
            h_med = a / (a + b)  # GG中位数近似
            h_typ = max(h_med, 0.1)
            N_typ, M_typ, wn_typ = adaptive_params_tuned(h_typ, gamma_bar_db, C_foe, K_M, B0)

            print(f"{turb:>12s} {elev:>10s} | {mf:10.6f} {ma:10.6f} {gain:+10.3f} {N_typ:6d} {M_typ:6d} {wn_typ*1.06/1e6:8.2f}")


# ═══════════════════════════════════════════════════════════════
# 也测一下"per-component"策略: 各公式独立调到最优
# ═══════════════════════════════════════════════════════════════
def per_component_analysis():
    """分析各组件单独调优的效果"""
    print("\n" + "=" * 70)
    print("STEP 0b: 逐组件分析 — 各公式独立对BER的影响")
    print("=" * 70)

    Ns = 5000
    n_trials = 20
    gamma_bar_db = 20
    turb = 'strong'
    f_dot = DOPPLER_HIGH

    # fixed baseline
    fixed_bers = []
    for t in range(n_trials):
        np.random.seed(500 + t)
        fixed_bers.append(run_single_trial(Ns, turb, f_dot, gamma_bar_db, 0, 0, 0, adaptive=False))
    fixed_mean = np.mean(fixed_bers)
    print(f"Fixed baseline BER = {fixed_mean:.6f}")

    # 原始adaptive
    orig_KM = (3 / 4) ** 0.2
    gamma_bar = 10 ** (gamma_bar_db / 10)
    B0_orig = np.sqrt(np.pi * LASER_LW * gamma_bar / T_S)

    orig_bers = []
    for t in range(n_trials):
        np.random.seed(500 + t)
        orig_bers.append(run_single_trial(Ns, turb, f_dot, gamma_bar_db, 80, orig_KM, B0_orig, adaptive=True))
    orig_mean = np.mean(orig_bers)
    orig_gain = 10 * np.log10(fixed_mean / orig_mean) if orig_mean < fixed_mean else 0
    print(f"Original adaptive   BER = {orig_mean:.6f}  Gain = {orig_gain:+.3f} dB")

    # 只调FOE (保持VV和DPLL fixed)
    # 固定VV=DPLL意味着在carrier_recovery_tuned中只靠adaptive_params_tuned的结果
    # 但我们需要一个只改FOE的版本
    a, b = TURB[turb]

    print(f"\n{'Config':>35s} | {'BER':>10s} {'Gain_dB':>10s}")
    print("-" * 60)

    configs = [
        ('Fixed baseline', 0, 0, 0, False),
        ('Original (80, 0.94, orig B0)', 80, orig_KM, B0_orig, True),
        ('FOE x320 only (VV/DPLL orig)', 25600, orig_KM, B0_orig, True),
        ('FOE x320 + VV x50', 25600, orig_KM * 50, B0_orig, True),
        ('FOE x320 + B0 match h0.5', 25600, orig_KM, FIXED_CFG['omega_n'] * 0.53 / 0.5, True),
        ('FOE x320 + VV x50 + B0 h0.5', 25600, orig_KM * 50, FIXED_CFG['omega_n'] * 0.53 / 0.5, True),
        ('FOE x100', 8000, orig_KM, B0_orig, True),
        ('FOE x100 + VV x20', 8000, orig_KM * 20, B0_orig, True),
        ('FOE x100 + B0/4', 8000, orig_KM, B0_orig / 4, True),
        ('FOE x100 + VV x20 + B0/4', 8000, orig_KM * 20, B0_orig / 4, True),
        ('FOE x500 (40000)', 40000, orig_KM, B0_orig, True),
        ('FOE x500 + VV x100 + B0/4', 40000, orig_KM * 100, B0_orig / 4, True),
    ]

    for name, cf, km, b0, use_adapt in configs:
        bers = []
        for t in range(n_trials):
            np.random.seed(500 + t)
            bers.append(run_single_trial(Ns, turb, f_dot, gamma_bar_db,
                                         cf, km, b0, adaptive=use_adapt))

        mean_ber = np.mean(bers)
        gain = 10 * np.log10(fixed_mean / mean_ber) if mean_ber < fixed_mean and mean_ber > 0 else 0.0
        marker = " ***" if gain > 0.5 else ""
        print(f"{name:>35s} | {mean_ber:10.6f} {gain:+10.3f}{marker}")


# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    t0 = time.time()

    print("=" * 70)
    print("Ch4 自适应载波同步 — 系数调优实验")
    print("=" * 70)

    # Step 0: 反推系数
    coeff_info = reverse_engineer_coefficients()

    # Step 0b: 逐组件分析
    per_component_analysis()

    # Step 1: 粗扫
    sweep_results, best_coarse = sweep_coefficients()

    if best_coarse is None or best_coarse['gain_db'] <= -1.0:
        print("\n粗扫未找到有效配置, 尝试极端系数...")
        # 尝试更极端的组合
        orig_KM = (3 / 4) ** 0.2
        gamma_bar = 10 ** (20 / 10)
        B0_orig = np.sqrt(np.pi * LASER_LW * gamma_bar / T_S)

        extreme_configs = [
            (25600, orig_KM * 50, B0_orig / 4, "extreme1"),
            (25600, orig_KM * 100, B0_orig / 8, "extreme2"),
            (40000, orig_KM * 100, B0_orig / 4, "extreme3"),
            (40000, orig_KM * 50, FIXED_CFG['omega_n'] * 0.53 / 0.3, "extreme4"),
        ]

        Ns, n_trials = 5000, 20
        turb, f_dot, gamma_bar_db = 'strong', DOPPLER_HIGH, 20
        fixed_bers = []
        for t in range(n_trials):
            np.random.seed(500 + t)
            fixed_bers.append(run_single_trial(Ns, turb, f_dot, gamma_bar_db, 0, 0, 0, adaptive=False))
        fixed_mean = np.mean(fixed_bers)

        for cf, km, b0, name in extreme_configs:
            bers = []
            for t in range(n_trials):
                np.random.seed(500 + t)
                bers.append(run_single_trial(Ns, turb, f_dot, gamma_bar_db, cf, km, b0, adaptive=True))
            mb = np.mean(bers)
            g = 10 * np.log10(fixed_mean / mb) if mb < fixed_mean and mb > 0 else 0
            print(f"  {name}: C_foe={cf}, K_M={km:.4f}, B0={b0/1e6:.2f}MHz -> BER={mb:.6f} Gain={g:+.3f}dB")
            if g > best_coarse['gain_db']:
                best_coarse = {
                    'C_foe': cf, 'K_M': km, 'B0': b0,
                    'ber': mb, 'gain_db': g,
                    'foe_ratio': cf // 80, 'km_ratio': km / orig_KM,
                    'b0_name': name, 'N_typ': 0, 'M_typ': 0, 'BL_typ': 0,
                }

    # Step 2: 精细扫描
    best_fine = fine_sweep(best_coarse)

    # Step 3: 完整MVE
    mve_results = run_full_mve(best_fine['C_foe'], best_fine['K_M'], best_fine['B0'])

    # Step 4: 跨湍流验证
    cross_turbulence_check(best_fine['C_foe'], best_fine['K_M'], best_fine['B0'])

    # 最终结论
    dt = time.time() - t0
    print("\n" + "=" * 70)
    print("最终结论")
    print("=" * 70)

    n_pass = sum(1 for r in mve_results.values() if r['gain_db'] > 0.5)
    n_positive = sum(1 for r in mve_results.values() if r['gain_db'] > 0)
    max_gain = max(r['gain_db'] for r in mve_results.values())

    print(f"\n最优系数集:")
    print(f"  C_foe = {best_fine['C_foe']} (原始80的 {best_fine['C_foe']/80:.0f}x)")
    print(f"  K_M   = {best_fine['K_M']:.4f} (原始{(3/4)**0.2:.4f}的 {best_fine['K_M']/(3/4)**0.2:.1f}x)")
    print(f"  B0    = {best_fine['B0']/1e6:.2f} MHz")

    print(f"\nMVE结果:")
    print(f"  正增益场景: {n_positive}/6")
    print(f"  ≥0.5dB场景: {n_pass}/6")
    print(f"  最大增益:   {max_gain:+.3f} dB")

    if n_pass >= 4:
        print(f"\n  判定: 系数调优可以拯救自适应方案")
        print(f"  系数偏离原始理论值 {best_fine['C_foe']/80:.0f}x / {best_fine['K_M']/(3/4)**0.2:.1f}x,")
        print(f"  但自适应框架本身(结构+clip bounds)是合理的")
    elif n_positive >= 3:
        print(f"\n  判定: 系数调优部分有效, 但增益有限")
        print(f"  可能需要同时调整clip bounds或公式结构")
    else:
        print(f"\n  判定: 系数调优无法拯救自适应方案")
        print(f"  问题不在系数而在公式结构本身(如h^{-2}阈值行为)")
        print(f"  建议: 重新设计自适应策略, 如基于信道估计的分段策略")

    print(f"\n总耗时: {dt:.1f}s")
    print("=" * 70)
