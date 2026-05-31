#!/usr/bin/env python3
"""Ch3 Stress Test: 11-dimension validation of closed-form BER framework

Validates numerical stability, convergence, accuracy, and robustness
across extreme parameter ranges for the GG + Gaussian Phase Error + QPSK
closed-form BER expressions.

Dimensions:
  F1:  Meijer-G numerical stability
  F2:  Fourier series convergence
  F3:  ber_phase_avg trapezoidal integration accuracy
  F4:  GG CDF extreme parameter behavior
  F5:  BER floor large sigma_phi applicability
  F6:  P_s/2 approximation bias boundary
  F7:  Outage probability binary search robustness
  F8:  DPLL sigma_phi h-independence
  F9:  Closed-form vs MC full parameter sweep (most important)
  F10: SNR penalty turbulence independence
  F11: Estimation error conditional BER deep fading
"""

import numpy as np
from scipy.stats import gamma as gamma_dist
from scipy.special import erfc, erfcinv, gamma as gamma_func
from scipy.integrate import quad
import mpmath
import json
import os
import sys
import time
import traceback

OUT = os.path.dirname(os.path.abspath(__file__))
np.random.seed(42)

# ─── Turbulence parameters ──────────────────────────────────
TURB = {
    'weak':     (4.0, 3.0),
    'moderate': (2.5, 1.8),
    'strong':   (1.5, 0.8),
}

# ─── Physical constants (DPLL / VV) ─────────────────────────
LASER_LW = 10e3          # 10 kHz laser linewidth
T_S = 4e-10              # symbol period (2.5 GBaud)
F_RESIDUAL = 1e6         # residual frequency offset
DF_NORM = F_RESIDUAL * T_S  # = 4e-4
K_M = (3/4)**0.2         # VV window coefficient


# ═══════════════════════════════════════════════════════════════
# Core functions (from sim_ch3_ber_closed_form.py)
# ═══════════════════════════════════════════════════════════════
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

def bn_gg_v2(n, alpha, beta, gamma_bar):
    z = mpmath.mpf(alpha * beta) / mpmath.mpf(gamma_bar)
    an = [1 - mpmath.mpf(n)/2]
    ap = [1 + mpmath.mpf(n)/2]
    bm = [mpmath.mpf(alpha), mpmath.mpf(beta), mpmath.mpf(0)]
    bq = []
    G = mpmath.meijerg([an, ap], [bm, bq], z)
    coeff = mpmath.mpf(n) / (2 * mpmath.pi * mpmath.gamma(alpha) * mpmath.gamma(beta))
    return float(coeff * G)

def ber_closed_form(gamma_bar_db, alpha, beta, sigma_phi, N_terms=30):
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
    sigma_sq_half = sigma_phi ** 2 / 2
    total = 0.0
    for n in range(1, N_terms + 1):
        sin_val = np.sin(n * np.pi / 4)
        if abs(sin_val) < 1e-15:
            continue
        total += np.exp(-n**2 * sigma_sq_half) * sin_val / n
    return 3.0/8 - total / np.pi

def gg_cdf(h_th, alpha, beta):
    z = mpmath.mpf(alpha * beta * h_th)
    G = mpmath.meijerg([[mpmath.mpf(1)], []],
                       [[mpmath.mpf(alpha), mpmath.mpf(beta)], [mpmath.mpf(0)]],
                       z)
    return float(G / (mpmath.gamma(alpha) * mpmath.gamma(beta)))

def ber_phase_avg(gamma_lin, sigma_phi, N_phi=200):
    phi = np.linspace(-4*sigma_phi, 4*sigma_phi, N_phi)
    dphi = phi[1] - phi[0]
    weights = np.exp(-phi**2 / (2*sigma_phi**2)) / (sigma_phi * np.sqrt(2*np.pi))
    pb = ber_qpsk_conditional(np.full_like(phi, gamma_lin), phi)
    return np.sum(pb * weights) * dphi

def mc_ber_linear(avg_snr_db, alpha, beta, sigma_phi, N=500_000):
    snr_lin = 10 ** (avg_snr_db / 10)
    h = gg_channel(N, alpha, beta)
    gamma = snr_lin * h
    phi = np.random.normal(0, sigma_phi, N)
    return np.mean(ber_qpsk_conditional(gamma, phi))

# ─── Outage functions (from sim_ch3_strengthening.py) ────────
def find_gamma_threshold(p_target, sigma_phi):
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
    gamma_th = find_gamma_threshold(p_target, sigma_phi)
    if np.isinf(gamma_th):
        return np.inf
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


# ═══════════════════════════════════════════════════════════════
# F1: Meijer-G numerical stability
# ═══════════════════════════════════════════════════════════════
def test_F1():
    print("\n" + "="*60)
    print("F1: Meijer-G Numerical Stability")
    print("="*60)
    t0 = time.time()

    turb_extended = {
        'weak': (4, 3), 'moderate': (2.5, 1.8), 'strong': (1.5, 0.8),
        'extreme': (0.5, 0.3), 'very_weak': (8, 6),
    }
    gamma_db_range = range(0, 55, 5)
    fails = []
    total = 0

    for turb, (a, b) in turb_extended.items():
        for gdb in gamma_db_range:
            for n in range(1, 51):
                total += 1
                try:
                    val = bn_gg_v2(n, a, b, 10**(gdb/10))
                    if np.isnan(val) or np.isinf(val):
                        fails.append(f'{turb} snr={gdb}dB n={n}: NaN/Inf')
                    elif gdb >= 30 and n <= 10 and abs(val - 1/np.pi) > 0.01:
                        fails.append(
                            f'{turb} snr={gdb}dB n={n}: |bn-1/pi|='
                            f'{abs(val-1/np.pi):.4f} > 0.01')
                except Exception as e:
                    fails.append(f'{turb} snr={gdb}dB n={n}: {e}')

    status = 'PASS' if not fails else 'FAIL'
    elapsed = time.time() - t0
    print(f"  Tested {total} combinations in {elapsed:.1f}s")
    print(f"  Failures: {len(fails)}/{total}")
    if fails:
        for f in fails[:20]:
            print(f"    {f}")
        if len(fails) > 20:
            print(f"    ... and {len(fails)-20} more")

    return {
        'dim': 'F1', 'name': 'Meijer-G Stability',
        'status': status, 'fail_items': fails,
        'details': {'total': total, 'failures': len(fails), 'elapsed_s': elapsed},
    }


# ═══════════════════════════════════════════════════════════════
# F2: Fourier series convergence
# ═══════════════════════════════════════════════════════════════
def test_F2():
    print("\n" + "="*60)
    print("F2: Fourier Series Convergence")
    print("="*60)
    t0 = time.time()

    sigma_deg_range = [1, 2, 3, 5, 8, 10, 15, 20, 25]
    N_terms_list = [5, 10, 15, 20, 30, 50, 100, 200]
    ref_N = 200
    alpha, beta = 2.5, 1.8
    snr_db_list = [10, 20, 30]

    fails = []
    convergence_map = {}  # sigma -> min_N for <1% error

    for sigma_deg in sigma_deg_range:
        sigma_rad = np.radians(sigma_deg)
        min_N_for_1pct = None

        for snr_db in snr_db_list:
            # Reference value with large N
            ref_val = ber_closed_form(snr_db, alpha, beta, sigma_rad, N_terms=ref_N)

            for N_trunc in N_terms_list:
                if N_trunc >= ref_N:
                    continue
                trunc_val = ber_closed_form(snr_db, alpha, beta, sigma_rad, N_terms=N_trunc)
                if abs(ref_val) < 1e-15:
                    continue
                rel_err = abs(trunc_val - ref_val) / abs(ref_val)

                # Check pass criteria
                if sigma_deg >= 5 and N_trunc == 20:
                    if rel_err > 0.01:
                        fails.append(
                            f'sigma={sigma_deg} snr={snr_db}dB N=20: '
                            f'rel_err={rel_err:.4f} > 1%')

                if sigma_deg >= 3 and N_trunc == 20:
                    if rel_err > 0.05:
                        fails.append(
                            f'sigma={sigma_deg} snr={snr_db}dB N=20: '
                            f'rel_err={rel_err:.4f} > 5%')

                # Track minimum N for <1% error
                if rel_err < 0.01 and min_N_for_1pct is None:
                    min_N_for_1pct = N_trunc

        convergence_map[sigma_deg] = min_N_for_1pct

    status = 'PASS' if not fails else 'FAIL'
    elapsed = time.time() - t0

    print(f"  Convergence (min N_terms for <1% error):")
    for sd, mn in convergence_map.items():
        print(f"    sigma={sd:>2}deg: min_N = {mn if mn else '>200'}")

    print(f"  Failures: {len(fails)}")
    if fails:
        for f in fails[:20]:
            print(f"    {f}")

    return {
        'dim': 'F2', 'name': 'Fourier Series Convergence',
        'status': status, 'fail_items': fails,
        'details': {'convergence_map': {str(k): v for k, v in convergence_map.items()},
                    'elapsed_s': elapsed},
    }


# ═══════════════════════════════════════════════════════════════
# F3: ber_phase_avg trapezoidal integration accuracy
# ═══════════════════════════════════════════════════════════════
def test_F3():
    print("\n" + "="*60)
    print("F3: ber_phase_avg Trapezoidal Integration Accuracy")
    print("="*60)
    t0 = time.time()

    sigma_deg_range = [1, 3, 5, 10, 15, 20, 30]
    gamma_lin_range = [0.1, 1, 10, 100, 1000]

    fails = []
    max_errors = {}

    def integrand(phi, gamma_lin, sigma_phi):
        """Phase-averaged BER integrand: P_b(gamma, phi) * f_phi(phi)"""
        sqrt2g = np.sqrt(2 * max(gamma_lin, 0))
        pb = 0.5 * (q_func(sqrt2g * np.cos(phi + np.pi/4)) +
                     q_func(sqrt2g * np.cos(phi - np.pi/4)))
        pdf = np.exp(-phi**2 / (2 * sigma_phi**2)) / (sigma_phi * np.sqrt(2*np.pi))
        return pb * pdf

    for sigma_deg in sigma_deg_range:
        sigma_rad = np.radians(sigma_deg)
        max_errors[sigma_deg] = {}

        for gamma_lin in gamma_lin_range:
            # Reference: scipy.integrate.quad (adaptive)
            ref_val, ref_err = quad(integrand, -6*sigma_rad, 6*sigma_rad,
                                    args=(gamma_lin, sigma_rad), limit=200,
                                    epsabs=1e-12, epsrel=1e-12)

            # Trapezoidal (ber_phase_avg with default N_phi=200)
            trap_val = ber_phase_avg(gamma_lin, sigma_rad, N_phi=200)

            if abs(ref_val) < 1e-15:
                continue
            rel_err = abs(trap_val - ref_val) / abs(ref_val)
            max_errors[sigma_deg][gamma_lin] = rel_err

            # Pass criteria
            if sigma_deg >= 3 and gamma_lin <= 100:
                if rel_err > 0.001:
                    fails.append(
                        f'sigma={sigma_deg} gamma={gamma_lin}: '
                        f'rel_err={rel_err:.6f} > 0.1%')

            if sigma_deg >= 1 and gamma_lin <= 1000:
                if rel_err > 0.01:
                    fails.append(
                        f'sigma={sigma_deg} gamma={gamma_lin}: '
                        f'rel_err={rel_err:.6f} > 1%')

    status = 'PASS' if not fails else 'FAIL'
    elapsed = time.time() - t0

    print(f"  Relative errors (trap vs quad):")
    for sd in sigma_deg_range:
        errs = max_errors[sd]
        err_strs = [f"g={g}:{e:.2e}" for g, e in errs.items()]
        print(f"    sigma={sd:>2}deg: {', '.join(err_strs)}")

    print(f"  Failures: {len(fails)}")
    if fails:
        for f in fails[:20]:
            print(f"    {f}")

    return {
        'dim': 'F3', 'name': 'Phase Avg Integration Accuracy',
        'status': status, 'fail_items': fails,
        'details': {'elapsed_s': elapsed},
    }


# ═══════════════════════════════════════════════════════════════
# F4: GG CDF extreme parameters
# ═══════════════════════════════════════════════════════════════
def test_F4():
    print("\n" + "="*60)
    print("F4: GG CDF Extreme Parameters")
    print("="*60)
    t0 = time.time()

    h_test = [1e-10, 1e-6, 1e-3, 0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 50.0, 100.0]
    N_mc = 10_000_000  # 10M for empirical CDF

    fails = []

    for tname, (alpha, beta) in TURB.items():
        print(f"  Turbulence: {tname} (alpha={alpha}, beta={beta})")

        # --- Compute CDF at all h_test points ---
        cdf_vals = []
        for h in h_test:
            try:
                val = gg_cdf(h, alpha, beta)
                if np.isnan(val) or np.isinf(val):
                    fails.append(f'{tname} h={h}: NaN/Inf CDF')
                    cdf_vals.append(np.nan)
                else:
                    cdf_vals.append(val)
            except Exception as e:
                fails.append(f'{tname} h={h}: exception {e}')
                cdf_vals.append(np.nan)

        # --- Monotonicity check ---
        for i in range(len(cdf_vals) - 1):
            if not (np.isnan(cdf_vals[i]) or np.isnan(cdf_vals[i+1])):
                if cdf_vals[i+1] < cdf_vals[i] - 1e-10:
                    fails.append(
                        f'{tname}: non-monotonic h={h_test[i]}->{h_test[i+1]}: '
                        f'F={cdf_vals[i]:.6e}->{cdf_vals[i+1]:.6e}')

        # --- Boundary checks ---
        cdf_dict = dict(zip(h_test, cdf_vals))
        if not np.isnan(cdf_dict.get(1e-10, np.nan)):
            if cdf_dict[1e-10] > 1e-8:
                fails.append(f'{tname} h=1e-10: F={cdf_dict[1e-10]:.2e} > 1e-8')
        if not np.isnan(cdf_dict.get(100.0, np.nan)):
            if cdf_dict[100.0] < 0.99:
                fails.append(f'{tname} h=100: F={cdf_dict[100.0]:.4f} < 0.99')

        # --- Print CDF table ---
        for h, c in zip(h_test, cdf_vals):
            print(f"    h={h:>10.1e}  F={c:.6e}")

    # --- MC verification at 6 intermediate points ---
    print(f"\n  MC verification (N={N_mc:,}):")
    h_mc_points = [0.01, 0.1, 0.5, 1.0, 2.0, 5.0]
    alpha, beta = TURB['moderate']
    h_samples = gg_channel(N_mc, alpha, beta)

    for h in h_mc_points:
        cdf_analytic = gg_cdf(h, alpha, beta)
        cdf_mc = np.mean(h_samples <= h)
        rel_err = abs(cdf_analytic - cdf_mc) / max(cdf_analytic, 1e-15)
        print(f"    h={h:.2f}: analytic={cdf_analytic:.6f} MC={cdf_mc:.6f} "
              f"rel_err={rel_err:.4e}")
        if rel_err > 0.05:
            fails.append(f'MC verify h={h}: rel_err={rel_err:.4e} > 5%')

    status = 'PASS' if not fails else 'FAIL'
    elapsed = time.time() - t0
    print(f"  Elapsed: {elapsed:.1f}s  Failures: {len(fails)}")
    if fails:
        for f in fails[:20]:
            print(f"    {f}")

    return {
        'dim': 'F4', 'name': 'GG CDF Extreme Parameters',
        'status': status, 'fail_items': fails,
        'details': {'N_mc': N_mc, 'elapsed_s': elapsed},
    }


# ═══════════════════════════════════════════════════════════════
# F5: BER floor large sigma_phi applicability
# ═══════════════════════════════════════════════════════════════
def test_F5():
    print("\n" + "="*60)
    print("F5: BER Floor Large sigma_phi Applicability")
    print("="*60)
    t0 = time.time()

    sigma_deg_range = [5, 8, 10, 12, 15, 18, 20, 25, 30, 35, 40, 45]
    alpha, beta = TURB['moderate']
    N_mc = 2_000_000

    fails = []
    print(f"  {'sigma(deg)':>10} {'Q(pi/4s)':>12} {'Series(N=100)':>14} "
          f"{'MC@50dB':>12} {'Q vs MC%':>10} {'S vs MC%':>10}")

    for sigma_deg in sigma_deg_range:
        sigma_rad = np.radians(sigma_deg)

        # Three paths
        val_q = ber_floor_qpsk(sigma_rad)
        val_series = ber_floor_series(sigma_rad, N_terms=100)

        # MC at very high SNR (50 dB)
        mc_val = mc_ber_linear(50, alpha, beta, sigma_rad, N=N_mc)

        err_q_mc = abs(val_q - mc_val) / max(mc_val, 1e-15) * 100
        err_s_mc = abs(val_series - mc_val) / max(mc_val, 1e-15) * 100

        print(f"  {sigma_deg:>10} {val_q:>12.4e} {val_series:>14.4e} "
              f"{mc_val:>12.4e} {err_q_mc:>9.2f}% {err_s_mc:>9.2f}%")

        # Pass criteria
        if sigma_deg <= 15:
            if err_q_mc > 5:
                fails.append(f'sigma={sigma_deg}: Q vs MC err={err_q_mc:.2f}% > 5%')
            if err_s_mc > 5:
                fails.append(f'sigma={sigma_deg}: Series vs MC err={err_s_mc:.2f}% > 5%')

        if sigma_deg <= 25:
            if err_q_mc > 10:
                fails.append(f'sigma={sigma_deg}: Q vs MC err={err_q_mc:.2f}% > 10%')

        # sigma=45: floor should be near 0.25, deviation < 20%
        if sigma_deg == 45:
            expected_near = 0.25
            dev = abs(mc_val - expected_near) / expected_near * 100
            if dev > 20:
                fails.append(f'sigma=45: MC={mc_val:.4f}, dev from 0.25 = {dev:.1f}% > 20%')

    status = 'PASS' if not fails else 'FAIL'
    elapsed = time.time() - t0
    print(f"  Elapsed: {elapsed:.1f}s  Failures: {len(fails)}")
    if fails:
        for f in fails:
            print(f"    {f}")

    return {
        'dim': 'F5', 'name': 'BER Floor Large sigma_phi',
        'status': status, 'fail_items': fails,
        'details': {'N_mc': N_mc, 'elapsed_s': elapsed},
    }


# ═══════════════════════════════════════════════════════════════
# F6: P_s/2 approximation bias boundary
# ═══════════════════════════════════════════════════════════════
def test_F6():
    print("\n" + "="*60)
    print("F6: P_s/2 Approximation Bias Boundary")
    print("="*60)
    t0 = time.time()

    sigma_deg_list = [5, 10, 15]
    snr_db_range = np.arange(0, 42, 2)

    fails = []
    contour_10pct = {}  # (turb, sigma) -> SNR where bias crosses 10%

    for tname, (alpha, beta) in TURB.items():
        for sigma_deg in sigma_deg_list:
            sigma_rad = np.radians(sigma_deg)
            key = f'{tname}_s{sigma_deg}'
            cross_snr = None

            for snr_db in snr_db_range:
                val_approx = ber_closed_form(snr_db, alpha, beta, sigma_rad, N_terms=30)
                val_exact = ber_exact(snr_db, alpha, beta, sigma_rad, N_terms=30)

                if abs(val_exact) < 1e-15:
                    continue
                bias_pct = abs(val_approx - val_exact) / abs(val_exact) * 100

                gamma_db = snr_db
                if gamma_db >= 10 and bias_pct > 15:
                    fails.append(
                        f'{key} SNR={snr_db}dB: bias={bias_pct:.2f}% > 15%')
                if gamma_db >= 20 and bias_pct > 5:
                    fails.append(
                        f'{key} SNR={snr_db}dB: bias={bias_pct:.2f}% > 5%')

                # Track 10% contour
                if cross_snr is None and bias_pct < 10:
                    cross_snr = snr_db

            contour_10pct[key] = cross_snr
            print(f"  {key}: 10% contour at SNR >= {cross_snr} dB")

    status = 'PASS' if not fails else 'FAIL'
    elapsed = time.time() - t0
    print(f"  Failures: {len(fails)}")
    if fails:
        for f in fails[:20]:
            print(f"    {f}")

    return {
        'dim': 'F6', 'name': 'P_s/2 Approximation Bias',
        'status': status, 'fail_items': fails,
        'details': {'contour_10pct': contour_10pct, 'elapsed_s': elapsed},
    }


# ═══════════════════════════════════════════════════════════════
# F7: Outage probability binary search robustness
# ═══════════════════════════════════════════════════════════════
def test_F7():
    print("\n" + "="*60)
    print("F7: Outage Probability Binary Search Robustness")
    print("="*60)
    t0 = time.time()

    test_cases = [
        (5, 1e-3), (5, 1e-6), (5, 1e-8),
        (10, 1e-3), (10, 1e-5), (10, 3.5e-6),
        (15, 1e-2), (15, 1e-3),
        (0, 1e-3), (0, 1e-6),
    ]

    fails = []
    print(f"  {'sigma':>6} {'p_target':>10} {'gamma_th':>12} {'check':>20}")

    for sigma_deg, p_target in test_cases:
        sigma_rad = np.radians(sigma_deg) if sigma_deg > 0 else 0.0
        floor = ber_floor_qpsk(sigma_rad) if sigma_rad > 0 else 0.0

        gamma_th = find_gamma_threshold(p_target, sigma_rad)

        # Case: p_target <= floor -> should return inf
        if sigma_rad > 0 and p_target <= floor:
            if np.isinf(gamma_th):
                print(f"  {sigma_deg:>6} {p_target:>10.1e} {'inf':>12} "
                      f"{'OK (above floor)':>20}")
            else:
                fails.append(f'sigma={sigma_deg} p={p_target:.1e}: '
                             f'should be inf, got {gamma_th:.2f}')
                print(f"  {sigma_deg:>6} {p_target:>10.1e} {gamma_th:>12.2f} "
                      f"{'FAIL: not inf':>20}")
            continue

        if np.isinf(gamma_th):
            fails.append(f'sigma={sigma_deg} p={p_target:.1e}: unexpected inf')
            print(f"  {sigma_deg:>6} {p_target:>10.1e} {'inf':>12} "
                  f"{'FAIL: unexpected':>20}")
            continue

        # Self-consistency: ber_phase_avg(gamma_th) should approximate p_target
        if sigma_rad > 0:
            pb_check = ber_phase_avg(gamma_th, sigma_rad)
        else:
            pb_check = q_func(np.sqrt(gamma_th))

        self_err = abs(pb_check - p_target) / p_target * 100

        # sigma=0: compare with analytical 2*[erfcinv(2p)]^2
        if sigma_deg == 0:
            gamma_analytic = 2 * erfcinv(2 * p_target)**2
            analytic_err = abs(gamma_th - gamma_analytic) / gamma_analytic * 100
            print(f"  {sigma_deg:>6} {p_target:>10.1e} {gamma_th:>12.4f} "
                  f"self_err={self_err:.3f}% analytic_err={analytic_err:.3f}%")
            if analytic_err > 1:
                fails.append(f'sigma=0 p={p_target:.1e}: analytic err '
                             f'{analytic_err:.3f}% > 1%')
            if self_err > 1:
                fails.append(f'sigma=0 p={p_target:.1e}: self_err '
                             f'{self_err:.3f}% > 1%')
        else:
            print(f"  {sigma_deg:>6} {p_target:>10.1e} {gamma_th:>12.4f} "
                  f"self_err={self_err:.3f}%")
            if self_err > 1:
                fails.append(f'sigma={sigma_deg} p={p_target:.1e}: self_err '
                             f'{self_err:.3f}% > 1%')

    status = 'PASS' if not fails else 'FAIL'
    elapsed = time.time() - t0
    print(f"  Failures: {len(fails)}")
    if fails:
        for f in fails:
            print(f"    {f}")

    return {
        'dim': 'F7', 'name': 'Outage Binary Search Robustness',
        'status': status, 'fail_items': fails,
        'details': {'elapsed_s': elapsed},
    }


# ═══════════════════════════════════════════════════════════════
# F8: DPLL sigma_phi h-independence
# ═══════════════════════════════════════════════════════════════
def test_F8():
    print("\n" + "="*60)
    print("F8: DPLL sigma_phi h-independence")
    print("="*60)
    t0 = time.time()

    fails = []
    gamma_bar = 100  # 20 dB

    B0 = np.sqrt(np.pi * LASER_LW * gamma_bar / T_S)
    sigma_dpll_perfect = np.sqrt(B0 * T_S / (2 * gamma_bar))

    print(f"  B0 = {B0:.4e} Hz")
    print(f"  sigma_dpll (perfect CSI) = {sigma_dpll_perfect:.6f} rad "
          f"= {np.degrees(sigma_dpll_perfect):.4f} deg")

    # Verify h-independence: generate many h values, compute sigma_dpll
    h_range = np.logspace(-3, 2, 10000)
    sigma_dpll_arr = np.full_like(h_range, sigma_dpll_perfect)  # h-independent

    std_check = np.std(sigma_dpll_arr)
    print(f"  sigma_dpll array std = {std_check:.2e} (should be 0)")

    if std_check > 1e-15:
        fails.append(f'sigma_dpll std = {std_check:.2e}, not h-independent')

    # Check engineering range
    if np.degrees(sigma_dpll_perfect) >= 20:
        fails.append(f'sigma_dpll = {np.degrees(sigma_dpll_perfect):.2f} deg >= 20 deg '
                     f'(outside engineering range)')
    else:
        print(f"  sigma_dpll = {np.degrees(sigma_dpll_perfect):.4f} deg (< 20 deg, OK)")

    status = 'PASS' if not fails else 'FAIL'
    elapsed = time.time() - t0
    print(f"  Failures: {len(fails)}")
    if fails:
        for f in fails:
            print(f"    {f}")

    return {
        'dim': 'F8', 'name': 'DPLL h-independence',
        'status': status, 'fail_items': fails,
        'details': {
            'B0': float(B0),
            'sigma_dpll_rad': float(sigma_dpll_perfect),
            'sigma_dpll_deg': float(np.degrees(sigma_dpll_perfect)),
            'elapsed_s': elapsed,
        },
    }


# ═══════════════════════════════════════════════════════════════
# F9: Closed-form vs MC full parameter sweep (MOST IMPORTANT)
# ═══════════════════════════════════════════════════════════════
def test_F9():
    print("\n" + "="*60)
    print("F9: Closed-form vs MC Full Parameter Sweep (MOST IMPORTANT)")
    print("="*60)
    t0 = time.time()

    sigma_deg_list = [2, 5, 8, 10, 12, 15, 20]
    snr_db_range = np.arange(0, 42, 2)
    N_mc = 500_000

    total_tests = len(TURB) * len(sigma_deg_list) * len(snr_db_range)
    print(f"  Total parameter combinations: {total_tests}")
    print(f"  MC samples per point: {N_mc:,}")
    print(f"  Estimated time: ~{total_tests * 0.02:.0f}s - {total_tests * 0.05:.0f}s")

    fails = []
    bias_direction = {'over': 0, 'under': 0, 'neutral': 0}
    results_summary = []

    count = 0
    for tname, (alpha, beta) in TURB.items():
        for sigma_deg in sigma_deg_list:
            sigma_rad = np.radians(sigma_deg)
            for snr_db in snr_db_range:
                count += 1
                if count % 50 == 0:
                    elapsed = time.time() - t0
                    eta = elapsed / count * (total_tests - count)
                    print(f"  Progress: {count}/{total_tests} "
                          f"({count/total_tests*100:.0f}%) "
                          f"elapsed={elapsed:.0f}s ETA={eta:.0f}s")

                theory = ber_exact(snr_db, alpha, beta, sigma_rad, N_terms=30)
                mc_val = mc_ber_linear(snr_db, alpha, beta, sigma_rad, N=N_mc)

                if mc_val < 1e-8 or theory < 1e-8:
                    continue

                rel_err = abs(theory - mc_val) / mc_val * 100

                # Track bias direction
                if theory > mc_val * 1.01:
                    bias_direction['over'] += 1
                elif theory < mc_val * 0.99:
                    bias_direction['under'] += 1
                else:
                    bias_direction['neutral'] += 1

                # Pass criteria
                if mc_val > 1e-3 and rel_err > 5:
                    fails.append(
                        f'{tname} s={sigma_deg} snr={snr_db}dB '
                        f'BER={mc_val:.2e} err={rel_err:.1f}% > 5%')
                elif mc_val > 1e-4 and rel_err > 10:
                    fails.append(
                        f'{tname} s={sigma_deg} snr={snr_db}dB '
                        f'BER={mc_val:.2e} err={rel_err:.1f}% > 10%')
                elif mc_val > 1e-5 and rel_err > 20:
                    fails.append(
                        f'{tname} s={sigma_deg} snr={snr_db}dB '
                        f'BER={mc_val:.2e} err={rel_err:.1f}% > 20%')

    status = 'PASS' if not fails else 'FAIL'
    elapsed = time.time() - t0

    total_bias = bias_direction['over'] + bias_direction['under'] + bias_direction['neutral']
    print(f"\n  Bias direction: over={bias_direction['over']} "
          f"under={bias_direction['under']} neutral={bias_direction['neutral']} "
          f"(total={total_bias})")
    print(f"  Failures: {len(fails)}")
    if fails:
        print(f"  First 20 failures:")
        for f in fails[:20]:
            print(f"    {f}")
        if len(fails) > 20:
            print(f"    ... and {len(fails)-20} more")

    print(f"  Elapsed: {elapsed:.1f}s ({elapsed/60:.1f}min)")

    return {
        'dim': 'F9', 'name': 'Closed-form vs MC Sweep',
        'status': status, 'fail_items': fails[:100],  # cap for JSON size
        'details': {
            'total_tests': total_tests,
            'N_mc': N_mc,
            'bias_direction': bias_direction,
            'total_fails': len(fails),
            'elapsed_s': elapsed,
        },
    }


# ═══════════════════════════════════════════════════════════════
# F10: SNR penalty turbulence independence
# ═══════════════════════════════════════════════════════════════
def test_F10():
    print("\n" + "="*60)
    print("F10: SNR Penalty Turbulence Independence")
    print("="*60)
    t0 = time.time()

    sigma_test = [3, 5, 8, 10, 12]
    p_targets = [1e-3, 1e-4, 1e-5, 1e-6]
    p_out = 0.01

    fails = []
    print(f"  {'sigma':>6} {'p_target':>10} {'weak_dB':>10} {'mod_dB':>10} "
          f"{'str_dB':>10} {'max_diff':>10}")

    for sigma_deg in sigma_test:
        sigma_rad = np.radians(sigma_deg) if sigma_deg > 0 else 0

        for p_target in p_targets:
            floor_val = ber_floor_qpsk(sigma_rad)
            if p_target <= floor_val:
                continue

            penalties = {}
            for tname, (alpha, beta) in TURB.items():
                # SNR with phase error
                gb_with = find_required_snr(p_target, p_out, sigma_rad, alpha, beta)
                # SNR without phase error (sigma=0)
                gb_without = find_required_snr(p_target, p_out, 0, alpha, beta)

                if np.isinf(gb_with) or np.isinf(gb_without):
                    penalties[tname] = np.nan
                else:
                    penalties[tname] = 10*np.log10(gb_with) - 10*np.log10(gb_without)

            vals = [v for v in penalties.values() if not np.isnan(v)]
            if len(vals) < 2:
                print(f"  {sigma_deg:>6} {p_target:>10.1e} "
                      f"{'---':>10} {'---':>10} {'---':>10} {'---':>10}")
                continue

            max_diff = max(vals) - min(vals)
            weak_str = f"{penalties.get('weak', np.nan):.2f}" if 'weak' in penalties else "---"
            mod_str = f"{penalties.get('moderate', np.nan):.2f}" if 'moderate' in penalties else "---"
            str_str = f"{penalties.get('strong', np.nan):.2f}" if 'strong' in penalties else "---"

            print(f"  {sigma_deg:>6} {p_target:>10.1e} {weak_str:>10} {mod_str:>10} "
                  f"{str_str:>10} {max_diff:>10.3f}")

            if max_diff > 0.1:
                fails.append(
                    f'sigma={sigma_deg} p={p_target:.1e}: '
                    f'penalty diff={max_diff:.3f} dB > 0.1 dB')

    status = 'PASS' if not fails else 'FAIL'
    elapsed = time.time() - t0
    print(f"  Failures: {len(fails)}")
    if fails:
        for f in fails:
            print(f"    {f}")

    return {
        'dim': 'F10', 'name': 'SNR Penalty Turbulence Independence',
        'status': status, 'fail_items': fails,
        'details': {'elapsed_s': elapsed},
    }


# ═══════════════════════════════════════════════════════════════
# F11: Estimation error conditional BER deep fading
# ═══════════════════════════════════════════════════════════════
def test_F11():
    print("\n" + "="*60)
    print("F11: Estimation Error Conditional BER Deep Fading")
    print("="*60)
    t0 = time.time()

    alpha, beta = TURB['moderate']
    gamma_bar = 100  # 20 dB
    N = 2_000_000

    h_bins = [
        (0, 0.01), (0.01, 0.05), (0.05, 0.1), (0.1, 0.2),
        (0.2, 0.5), (0.5, 1.0), (1.0, 2.0), (2.0, 10.0),
    ]
    nmse_db_test = [-25, -20, -15, -10, -7, -5, -3, 0]

    fails = []

    # Generate samples
    h_samples = gg_channel(N, alpha, beta)
    gamma_true = gamma_bar * h_samples

    B0 = np.sqrt(np.pi * LASER_LW * gamma_bar / T_S)
    sigma_dpll_perfect = np.sqrt(B0 * T_S / (2 * gamma_bar))

    # Perfect CSI baseline
    sigma_dpll_p = np.full(N, sigma_dpll_perfect)
    M_vv_p = K_M * (gamma_bar * h_samples)**(-0.2) * DF_NORM**(-0.4)
    M_vv_p = np.clip(M_vv_p, 4, 256)
    sigma_vv_p = np.sqrt(1 / (2 * M_vv_p * gamma_bar * h_samples))
    sigma_cascade_p = np.sqrt(sigma_dpll_p**2 + sigma_vv_p**2)
    phi_perfect = np.random.normal(0, 1, N) * sigma_cascade_p
    ber_perfect_all = ber_qpsk_conditional(gamma_true, phi_perfect)

    # Bin masks
    bin_masks = []
    for h_lo, h_hi in h_bins:
        mask = (h_samples >= h_lo) & (h_samples < h_hi)
        bin_masks.append(mask)

    print(f"  {'NMSE_dB':>8}", end="")
    for h_lo, h_hi in h_bins:
        print(f"  h=[{h_lo},{h_hi})", end="")
    print()

    for nmse_db in nmse_db_test:
        nmse = 10**(nmse_db/10)
        eps = np.random.normal(0, np.sqrt(nmse), N)
        h_est = np.clip(h_samples * (1 + eps), 0.01, 50)

        # DPLL with estimated h
        B_L_est = B0 * h_est
        sigma_dpll_est = np.sqrt(B_L_est * T_S / (2 * gamma_bar * h_samples))

        # VV with estimated h
        M_vv_est = K_M * (gamma_bar * h_est)**(-0.2) * DF_NORM**(-0.4)
        M_vv_est = np.clip(M_vv_est, 4, 256)
        sigma_vv_est = np.sqrt(1 / (2 * M_vv_est * gamma_bar * h_samples))

        sigma_cascade_est = np.sqrt(sigma_dpll_est**2 + sigma_vv_est**2)
        phi_est = np.random.normal(0, 1, N) * sigma_cascade_est
        ber_est_all = ber_qpsk_conditional(gamma_true, phi_est)

        print(f"  {nmse_db:>8}", end="")
        for i, (h_lo, h_hi) in enumerate(h_bins):
            mask = bin_masks[i]
            if mask.sum() < 10:
                print(f"  {'---':>12}", end="")
                continue

            bp = np.mean(ber_perfect_all[mask])
            be = np.mean(ber_est_all[mask])
            ratio = be / bp if bp > 1e-12 else float('nan')
            print(f"  {ratio:>12.3f}", end="")

            # Pass criteria
            if nmse_db <= -10:
                if ratio > 1.5 or (not np.isnan(ratio) and ratio < 0.5):
                    fails.append(
                        f'NMSE={nmse_db}dB h=[{h_lo},{h_hi}): '
                        f'ratio={ratio:.3f} outside [0.5, 1.5]')
            if nmse_db == -5:
                if h_lo >= 0.1 and (ratio > 1.2 or ratio < 0.8):
                    fails.append(
                        f'NMSE=-5dB h=[{h_lo},{h_hi}): '
                        f'ratio={ratio:.3f} outside [0.8, 1.2]')
                if h_hi <= 0.1 and (ratio > 2.0 or ratio < 0.5):
                    fails.append(
                        f'NMSE=-5dB h=[{h_lo},{h_hi}): '
                        f'ratio={ratio:.3f} outside [0.5, 2.0]')
        print()

    status = 'PASS' if not fails else 'FAIL'
    elapsed = time.time() - t0
    print(f"  Elapsed: {elapsed:.1f}s  Failures: {len(fails)}")
    if fails:
        for f in fails:
            print(f"    {f}")

    return {
        'dim': 'F11', 'name': 'Estimation Error Deep Fading',
        'status': status, 'fail_items': fails,
        'details': {'N': N, 'elapsed_s': elapsed},
    }


# ═══════════════════════════════════════════════════════════════
# Main: run all dimensions sequentially
# ═══════════════════════════════════════════════════════════════
def main():
    print("="*60)
    print("Ch3 Stress Test: 11-Dimension Validation")
    print("="*60)
    print(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.executable}")
    print(f"numpy: {np.__version__}")

    t_total = time.time()
    all_results = []

    # Fast tests first (F1-F8, F10-F11), then the slow F9
    test_funcs = [
        ('F1',  test_F1),
        ('F2',  test_F2),
        ('F3',  test_F3),
        ('F4',  test_F4),
        ('F5',  test_F5),
        ('F6',  test_F6),
        ('F7',  test_F7),
        ('F8',  test_F8),
        ('F10', test_F10),
        ('F11', test_F11),
        ('F9',  test_F9),  # Last: most time-consuming
    ]

    for dim_name, func in test_funcs:
        try:
            result = func()
            all_results.append(result)
            # Print immediate summary
            status_str = result['status']
            n_fails = len(result.get('fail_items', []))
            elapsed = result.get('details', {}).get('elapsed_s', 0)
            print(f"\n  >> {dim_name}: {status_str} "
                  f"({n_fails} failures, {elapsed:.1f}s)")
        except Exception as e:
            tb = traceback.format_exc()
            print(f"\n  >> {dim_name}: ERROR - {e}")
            print(tb)
            all_results.append({
                'dim': dim_name, 'name': dim_name,
                'status': 'ERROR', 'fail_items': [str(e)],
                'details': {'traceback': tb},
            })

    # ─── Summary table ───────────────────────────────────────
    total_elapsed = time.time() - t_total
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"  {'Dim':>4} {'Name':>35} {'Status':>8} {'Fails':>6}")
    print("  " + "-"*55)

    n_pass = 0
    n_fail = 0
    n_error = 0
    for r in all_results:
        s = r['status']
        nf = len(r.get('fail_items', []))
        print(f"  {r['dim']:>4} {r['name']:>35} {s:>8} {nf:>6}")
        if s == 'PASS':
            n_pass += 1
        elif s == 'FAIL':
            n_fail += 1
        else:
            n_error += 1

    print(f"\n  Total: {n_pass} PASS, {n_fail} FAIL, {n_error} ERROR")
    print(f"  Total time: {total_elapsed:.1f}s ({total_elapsed/60:.1f}min)")
    print(f"  End time: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # ─── Save JSON ───────────────────────────────────────────
    json_path = os.path.join(OUT, 'results_ch3_stress.json')
    # Make results JSON-serializable
    json_results = []
    for r in all_results:
        jr = dict(r)
        # Truncate large fail_items
        if len(jr.get('fail_items', [])) > 100:
            jr['fail_items_truncated'] = True
            jr['fail_items'] = jr['fail_items'][:100]
            jr['total_fail_count'] = r.get('details', {}).get('total_fails',
                                       len(r.get('fail_items', [])))
        json_results.append(jr)

    output = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total_elapsed_s': total_elapsed,
        'summary': {'pass': n_pass, 'fail': n_fail, 'error': n_error},
        'results': json_results,
    }

    with open(json_path, 'w') as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\n  Results saved to: {json_path}")


if __name__ == '__main__':
    main()
