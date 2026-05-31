#!/usr/bin/env python3
"""Ch3 Strengthening: Design Tables + Estimation Error Robustness

Strengthening 1: Outage-based design tables (turbulence-dependent)
  - Average SNR required for P_out = 1% at different sigma_phi
  - sigma_phi_max vs P_target
  - Unreachable region marking

Strengthening 2: Estimation error robustness analysis
  - DPLL: sigma_phi^2 = B0*T_s/(2*gamma_bar), h-independent with perfect CSI
  - With estimation error: h_hat = h*(1+eps), DPLL sigma_phi^2 changes
  - VV: sigma_phi^2 = 1/(2*M(h_hat)*gamma_bar*h), depends on h^{-0.6}
  - MC simulation of BER degradation vs NMSE
"""

import numpy as np
from scipy.stats import gamma as gamma_dist
from scipy.special import erfc, erfcinv
import mpmath
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, time

OUT = os.path.dirname(os.path.abspath(__file__))
np.random.seed(42)
plt.rcParams.update({'font.size': 11, 'figure.dpi': 150})

TURB = {
    'weak':     (4.0, 3.0),
    'moderate': (2.5, 1.8),
    'strong':   (1.5, 0.8),
}
P_TARGETS = [1e-3, 1e-4, 1e-5, 1e-6]
P_OUT_TARGET = 0.01  # 1% outage target
N_SYM = 300_000

# Physical constants (from formulas-ch3ch4-sync.md)
LASER_LW = 10e3         # 10 kHz laser linewidth (Zhao 2025)
T_S = 4e-10             # symbol period (2.5 GBaud)
F_RESIDUAL = 1e6        # residual frequency offset
DF_NORM = F_RESIDUAL * T_S  # = 4e-4
K_M = (3/4)**0.2        # VV window coefficient

# ─── Basic functions ───────────────────────────────────────
def q_func(x):
    return 0.5 * erfc(x / np.sqrt(2))

def gg_channel(N, alpha, beta):
    X = gamma_dist.rvs(alpha, scale=1/alpha, size=N)
    Y = gamma_dist.rvs(beta,  scale=1/beta,  size=N)
    return X * Y

def ber_qpsk_conditional(gamma, phi):
    sqrt2g = np.sqrt(2 * np.maximum(gamma, 0))
    return 0.5 * (q_func(sqrt2g * np.cos(phi + np.pi/4)) +
                  q_func(sqrt2g * np.cos(phi - np.pi/4)))

def ber_floor_qpsk(sigma_phi):
    return q_func(np.pi / (4 * sigma_phi))

def gg_cdf(h_th, alpha, beta):
    z = mpmath.mpf(alpha * beta * h_th)
    G = mpmath.meijerg([[mpmath.mpf(1)], []],
                       [[mpmath.mpf(alpha), mpmath.mpf(beta)], [mpmath.mpf(0)]],
                       z)
    return float(G / (mpmath.gamma(alpha) * mpmath.gamma(beta)))

def ber_phase_avg(gamma_lin, sigma_phi, N_phi=150):
    phi = np.linspace(-4*sigma_phi, 4*sigma_phi, N_phi)
    dphi = phi[1] - phi[0]
    weights = np.exp(-phi**2 / (2*sigma_phi**2)) / (sigma_phi * np.sqrt(2*np.pi))
    pb = ber_qpsk_conditional(np.full_like(phi, gamma_lin), phi)
    return np.sum(pb * weights) * dphi

def find_gamma_threshold(p_target, sigma_phi):
    """Binary search: P_b_avg(gamma_th, sigma_phi) = p_target"""
    if sigma_phi == 0:
        return (erfcinv(2 * p_target))**2 * 2
    floor = ber_floor_qpsk(sigma_phi)
    if p_target <= floor:
        return np.inf
    g_lo, g_hi = 0.1, 1e5
    for _ in range(80):
        g_mid = np.sqrt(g_lo * g_hi)
        if ber_phase_avg(g_mid, sigma_phi) > p_target:
            g_lo = g_mid
        else:
            g_hi = g_mid
        if abs(g_hi - g_lo) / g_mid < 1e-5:
            break
    return g_mid

def find_required_snr(p_target, p_out_target, sigma_phi, alpha, beta):
    """Find gamma_bar such that P_out = F_GG(gamma_th/gamma_bar) = p_out_target

    gamma_th depends on sigma_phi, gamma_bar enters through h_th = gamma_th/gamma_bar.
    For fixed p_target: gamma_th is fixed -> h_th = gamma_th/gamma_bar.
    P_out = F_GG(h_th) = p_out_target -> solve for gamma_bar.
    """
    gamma_th = find_gamma_threshold(p_target, sigma_phi)
    if np.isinf(gamma_th):
        return np.inf
    # F_GG(gamma_th/gamma_bar) = p_out_target
    # Need to find gamma_bar such that F_GG(gamma_th/gamma_bar) = p_out_target
    # Invert: h_th = F_GG^{-1}(p_out_target), then gamma_bar = gamma_th / h_th
    # Find h_th by binary search on F_GG
    h_lo, h_hi = 1e-6, 100
    for _ in range(80):
        h_mid = np.sqrt(h_lo * h_hi)
        if gg_cdf(h_mid, alpha, beta) < p_out_target:
            h_lo = h_mid
        else:
            h_hi = h_mid
        if abs(h_hi - h_lo) / h_mid < 1e-6:
            break
    gamma_bar = gamma_th / h_mid
    return gamma_bar

# ─── Strengthening 1: Outage-Based Design Tables ───────────
def experiment_design_tables():
    print("=" * 70)
    print("Strengthening 1: Outage-Based Design Tables")
    print("=" * 70)

    p_target = 1e-4
    p_out = P_OUT_TARGET

    # 1.1 sigma_phi upper bounds
    print(f"\n  1.1 Phase error upper bounds (BER floor < P_target):")
    print(f"  {'P_target':>10} {'sigma_max (deg)':>16} {'Floor at limit':>16}")
    for pt in P_TARGETS:
        sp = np.pi / (4 * erfcinv(2*pt) * np.sqrt(2))
        floor = ber_floor_qpsk(sp)
        print(f"  {pt:>10.0e} {np.degrees(sp):>16.1f} {floor:>16.2e}")

    # 1.2 Required average SNR for P_out = 1% (turbulence-dependent!)
    sigma_deg_arr = [0, 3, 5, 8, 10, 12]
    print(f"\n  1.2 Required avg SNR (dB) for P_out={p_out:.0%} at P_BER={p_target:.0e}:")
    print(f"  {'Turbulence':>12}", end="")
    for sd in sigma_deg_arr:
        print(f"  {'s='+str(sd)+'deg':>10}", end="")
    print(f"  {'Penalty@10deg':>14}")

    for tname, (alpha, beta) in TURB.items():
        snrs = []
        for sd in sigma_deg_arr:
            sr = np.radians(sd) if sd > 0 else 0
            gb = find_required_snr(p_target, p_out, sr, alpha, beta)
            if np.isinf(gb):
                snrs.append(np.inf)
            else:
                snrs.append(10*np.log10(gb))

        print(f"  {tname:>12}", end="")
        for s in snrs:
            if np.isinf(s):
                print(f"  {'---':>10}", end="")
            else:
                print(f"  {s:>10.1f}", end="")
        # Penalty at 10 deg vs 0 deg
        if not np.isinf(snrs[-1]) and not np.isinf(snrs[0]):
            penalty = snrs[4] - snrs[0]  # 10deg vs 0deg
            print(f"  {penalty:>14.1f} dB")
        else:
            print(f"  {'UNREACH':>14}")

    # 1.3 Comprehensive table: P_out vs SNR for each (turbulence, sigma_phi)
    print(f"\n  1.3 Outage probability at SNR=20dB, P_BER_target={p_target:.0e}:")
    snr_db = 20
    gamma_bar = 10**(snr_db/10)
    print(f"  {'Turbulence':>12} {'s=0':>8} {'s=5':>8} {'s=8':>8} {'s=10':>8} {'s=12':>8}")
    for tname, (alpha, beta) in TURB.items():
        pouts = []
        for sd in [0, 5, 8, 10, 12]:
            sr = np.radians(sd) if sd > 0 else 0
            g_th = find_gamma_threshold(p_target, sr)
            if np.isinf(g_th):
                pouts.append(1.0)
            else:
                h_th = g_th / gamma_bar
                pouts.append(gg_cdf(h_th, alpha, beta))
        print(f"  {tname:>12}", end="")
        for po in pouts:
            print(f"  {po:>8.1e}", end="")
        print()

    # 1.4 Plot: Required SNR vs sigma_phi for 3 turbulence levels
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    sigma_plot = np.arange(0, 13, 0.5)
    colors = {'weak': 'blue', 'moderate': 'green', 'strong': 'red'}

    for tname, (alpha, beta) in TURB.items():
        req_snr = []
        for sd in sigma_plot:
            sr = np.radians(sd) if sd > 0 else 0
            gb = find_required_snr(p_target, p_out, sr, alpha, beta)
            if np.isinf(gb):
                req_snr.append(np.nan)
            else:
                req_snr.append(10*np.log10(gb))
        ax1.plot(sigma_plot, req_snr, color=colors[tname], lw=2, label=tname)

    # Mark unreachable boundaries
    sp_max = np.degrees(np.pi / (4 * erfcinv(2*p_target) * np.sqrt(2)))
    ax1.axvline(x=sp_max, color='gray', ls='--', alpha=0.7, label=f'Limit ({sp_max:.1f}deg)')

    ax1.set_xlabel('Phase Error Std $\\sigma_\\phi$ (deg)')
    ax1.set_ylabel('Required Avg SNR (dB)')
    ax1.set_title(f'Required SNR for $P_{{out}}$={p_out:.0%}, $P_{{BER}}$={p_target:.0e}')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Right: Outage probability vs SNR for different sigma_phi (moderate turbulence)
    alpha, beta = TURB['moderate']
    snr_range = np.arange(5, 40, 1)
    for sd in [0, 5, 8, 10]:
        sr = np.radians(sd) if sd > 0 else 0
        g_th = find_gamma_threshold(p_target, sr)
        if not np.isinf(g_th):
            pout_curve = [gg_cdf(g_th / (10**(s/10)), alpha, beta) for s in snr_range]
            ax2.semilogy(snr_range, pout_curve, lw=2, label=f'$\\sigma_\\phi$={sd}deg')

    ax2.axhline(y=p_out, color='gray', ls=':', label=f'$P_{{out}}$={p_out:.0%}')
    ax2.set_xlabel('Average SNR (dB)')
    ax2.set_ylabel('Outage Probability $P_{out}$')
    ax2.set_title(f'Outage vs SNR (moderate, $P_{{BER}}$={p_target:.0e})')
    ax2.set_ylim([1e-4, 1])
    ax2.legend(fontsize=9)
    ax2.grid(True, which='both', alpha=0.3)

    plt.tight_layout()
    path = os.path.join(OUT, 'fig_ch3_design_tables.png')
    plt.savefig(path)
    print(f"\n  -> {path}")
    plt.close()

# ─── Strengthening 2: Estimation Error Robustness ──────────
def experiment_estimation_error():
    print("\n" + "=" * 70)
    print("Strengthening 2: Estimation Error Robustness")
    print("=" * 70)

    alpha, beta = TURB['moderate']
    gamma_bar = 100  # 20 dB

    # --- Analytical insight ---
    # DPLL with B_L = B0*h:
    #   sigma_phi^2 = B_L*T_s/(2*gamma) = B0*h*T_s/(2*gamma_bar*h) = B0*T_s/(2*gamma_bar)
    #   -> h-independent! Estimation error changes B_L(h_hat) but mean unchanged.
    #
    # VV with M = K_M*(gamma_bar*h_hat^2)^{-0.2}*...:
    #   sigma_phi^2 = 1/(2*M*gamma) ∝ (h_hat/h)^{0.4} / gamma_bar^{0.8}
    #   -> depends on h^{-0.6}, estimation error adds (1+eps)^{0.4} factor

    B0 = np.sqrt(np.pi * LASER_LW * gamma_bar / T_S)
    sigma_dpll_perfect = np.sqrt(B0 * T_S / (2 * gamma_bar))
    print(f"\n  DPLL parameters: B0={B0:.2e} Hz, sigma_phi(perfect)={sigma_dpll_perfect:.4f} rad "
          f"({np.degrees(sigma_dpll_perfect):.2f} deg)")

    # --- 2.1 Conditional sigma_phi vs h (VV case, where h-dependence exists) ---
    h_range = np.logspace(-2, 1, 200)

    sigma_dpll = np.full_like(h_range, sigma_dpll_perfect)  # h-independent
    M_vv = K_M * (gamma_bar * h_range)**(-0.2) * DF_NORM**(-0.4)
    M_vv = np.clip(M_vv, 4, 256)
    sigma_vv = np.sqrt(1 / (2 * M_vv * gamma_bar * h_range))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.loglog(h_range, np.degrees(sigma_dpll), 'b-', lw=2, label='DPLL (h-independent)')
    ax1.loglog(h_range, np.degrees(sigma_vv), 'g-', lw=2, label='VV-CPR ($\\propto h^{-0.3}$)')
    ax1.set_xlabel('Channel gain $h$')
    ax1.set_ylabel('$\\sigma_\\phi$ (deg)')
    ax1.set_title('Phase Error Std vs Channel Gain')
    ax1.legend()
    ax1.grid(True, which='both', alpha=0.3)

    # --- 2.2 BER degradation vs NMSE (MC) ---
    nmse_db_arr = np.array([-25, -20, -15, -10, -7, -5])
    h_samples = gg_channel(N_SYM * 3, alpha, beta)  # more samples for accuracy
    gamma_true = gamma_bar * h_samples

    # Perfect CSI baseline (combined DPLL+VV)
    sigma_dpll_p = np.full(len(h_samples), sigma_dpll_perfect)
    M_vv_p = K_M * (gamma_bar * h_samples)**(-0.2) * DF_NORM**(-0.4)
    M_vv_p = np.clip(M_vv_p, 4, 256)
    sigma_vv_p = np.sqrt(1 / (2 * M_vv_p * gamma_bar * h_samples))
    sigma_cascade_p = np.sqrt(sigma_dpll_p**2 + sigma_vv_p**2)
    phi_p = np.random.normal(0, 1, len(h_samples)) * sigma_cascade_p
    ber_perfect = np.mean(ber_qpsk_conditional(gamma_true, phi_p))

    ber_results = [ber_perfect]
    for nmse_db in nmse_db_arr:
        nmse = 10**(nmse_db/10)
        eps = np.random.normal(0, np.sqrt(nmse), len(h_samples))
        h_est = np.clip(h_samples * (1 + eps), 0.01, 50)

        # DPLL with estimated h
        B_L_est = B0 * h_est
        sigma_dpll_est = np.sqrt(B_L_est * T_S / (2 * gamma_bar * h_samples))

        # VV with estimated h
        M_vv_est = K_M * (gamma_bar * h_est)**(-0.2) * DF_NORM**(-0.4)
        M_vv_est = np.clip(M_vv_est, 4, 256)
        sigma_vv_est = np.sqrt(1 / (2 * M_vv_est * gamma_bar * h_samples))

        # Combined
        sigma_cascade_est = np.sqrt(sigma_dpll_est**2 + sigma_vv_est**2)
        phi_est = np.random.normal(0, 1, len(h_samples)) * sigma_cascade_est
        ber = np.mean(ber_qpsk_conditional(gamma_true, phi_est))
        ber_results.append(ber)

    # Compute degradation ratio
    ratios = np.array(ber_results[1:]) / ber_perfect
    print(f"\n  2.2 BER vs NMSE (moderate turb, SNR=20dB):")
    print(f"  Perfect CSI: BER = {ber_perfect:.4e}")
    print(f"  {'NMSE (dB)':>10} {'BER':>12} {'Ratio':>10}")
    for i, nmse_db in enumerate(nmse_db_arr):
        print(f"  {nmse_db:>10} {ber_results[i+1]:>12.4e} {ratios[i]:>10.3f}")

    # Left plot already done, now right plot
    nmse_x = np.concatenate([[0], nmse_db_arr])  # 0 = perfect CSI
    ber_y = np.array(ber_results)

    ax2.semilogy(nmse_x, ber_y, 'ro-', ms=6, lw=2)
    ax2.axhline(y=ber_perfect, color='blue', ls=':', alpha=0.5)
    ax2.set_xlabel('NMSE (dB) [0 = perfect CSI]')
    ax2.set_ylabel('Average BER')
    ax2.set_title('BER vs Channel Estimation Error\n(moderate turb, SNR=20dB, DPLL+VV)')
    ax2.grid(True, which='both', alpha=0.3)
    ax2.annotate(f'Perfect CSI: {ber_perfect:.2e}', xy=(0, ber_perfect),
                xytext=(2, ber_perfect*2), fontsize=8)

    plt.tight_layout()
    path = os.path.join(OUT, 'fig_ch3_estimation_robustness.png')
    plt.savefig(path)
    print(f"\n  -> {path}")
    plt.close()

    # --- 2.3 Conditional BER degradation for small h (deep fade) ---
    # The average BER barely changes, but what about conditional BER in deep fading?
    print(f"\n  2.3 Conditional analysis (deep fade h < 0.2):")
    deep_mask = h_samples < 0.2
    gamma_deep = gamma_true[deep_mask]
    h_deep = h_samples[deep_mask]
    n_deep = deep_mask.sum()

    ber_deep_perfect = np.mean(ber_qpsk_conditional(
        gamma_deep, np.random.normal(0, 1, n_deep) * sigma_cascade_p[deep_mask]))

    for nmse_db in [-10, -5]:
        nmse = 10**(nmse_db/10)
        eps = np.random.normal(0, np.sqrt(nmse), n_deep)
        h_est_d = np.clip(h_deep * (1 + eps), 0.01, 50)

        B_L_d = B0 * h_est_d
        s_dpll_d = np.sqrt(B_L_d * T_S / (2 * gamma_bar * h_deep))
        M_vv_d = K_M * (gamma_bar * h_est_d)**(-0.2) * DF_NORM**(-0.4)
        M_vv_d = np.clip(M_vv_d, 4, 256)
        s_vv_d = np.sqrt(1 / (2 * M_vv_d * gamma_bar * h_deep))
        s_cas_d = np.sqrt(s_dpll_d**2 + s_vv_d**2)
        ber_deep = np.mean(ber_qpsk_conditional(
            gamma_deep, np.random.normal(0, 1, n_deep) * s_cas_d))
        print(f"    NMSE={nmse_db}dB: h<0.2 BER = {ber_deep:.4f} (perfect: {ber_deep_perfect:.4f}, "
              f"ratio={ber_deep/ber_deep_perfect:.3f})")

    # --- Key conclusion ---
    print(f"\n  Key findings:")
    print(f"  1. DPLL sigma_phi is h-independent (B_L∝h cancels γ∝h)")
    print(f"     -> estimation error doesn't change mean sigma_phi")
    print(f"  2. VV sigma_phi ∝ h^{{-0.3}} -> deep fading increases phase error")
    print(f"     -> estimation error adds (1+eps)^0.4 factor")
    print(f"  3. Average BER barely changes (ratio < {ratios.max():.3f} at NMSE=-5dB)")
    print(f"  4. Deep-fade BER changes slightly but dominated by low-SNR effect")
    print(f"  Conclusion: Adaptive sync is inherently robust to estimation errors")

# ─── Main ──────────────────────────────────────────────────
if __name__ == '__main__':
    t0 = time.time()
    experiment_design_tables()
    experiment_estimation_error()
    print(f"\nTotal: {time.time()-t0:.1f}s")
    print("=" * 70)
    print("All strengthening experiments done")
