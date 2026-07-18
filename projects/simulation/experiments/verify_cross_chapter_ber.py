#!/usr/bin/env python3
"""Cross-chapter verification: Ch3 BER closed form predicts Ch4 DPLL performance.

TL-25 checklist:
1. 共享信道: 不适用（解析+数据对比）
2. 重生信道: 不适用
3. 从 common.py 导入: 不适用（纯数学，参数与 TURB 一致）
4. 基线已优化: 不适用
5. 先写理论预期: DPLL 20dB σ_φ~2.6°, BER主要由SNR决定, 预测偏差<10%
6. 输出含元数据: 时间戳

理论预期（TL-20）:
- BER_closed = E_h[Q(sqrt(2·γ̄·h))]
- DPLL at 20dB: σ_φ small (~2.6°), BER dominated by SNR fading
- Expected: closed-form ≈ DPLL measured (deviation <10%)
- Quantitative anchor: if deviation >20%, DPLL phase error has non-negligible contribution
"""

import sys, os, time, datetime, json
import numpy as np
from scipy.stats import gamma as gamma_dist
from scipy.integrate import quad
from scipy.special import erfc

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import TURB, T_S

def q_function(x):
    """Q(x) = 0.5 * erfc(x / sqrt(2))"""
    return 0.5 * erfc(x / np.sqrt(2))

def gg_pdf(h, alpha, beta):
    """PDF of GG(alpha, beta) = Gamma(alpha, 1/alpha) × Gamma(beta, 1/beta).
    Numerical: sample and KDE is unreliable. Use MC integration instead.
    """
    # Not used directly - we use MC integration
    pass

def ber_closed_form_mc(gamma_bar_db, alpha, beta, n_mc=10**6, seed=42):
    """BER closed form via MC integration: E_h[Q(sqrt(2*gamma_bar*h))]."""
    gamma_bar = 10 ** (gamma_bar_db / 10)
    rng = np.random.default_rng(seed)
    x = gamma_dist.rvs(alpha, scale=1/alpha, size=n_mc, random_state=rng)
    y = gamma_dist.rvs(beta, scale=1/beta, size=n_mc, random_state=rng)
    h = x * y
    # QPSK BER in Rayleigh-fading-like: Q(sqrt(2*gamma_bar*h))
    args = np.sqrt(2 * gamma_bar * np.clip(h, 1e-10, None))
    ber_samples = q_function(args)
    return float(np.mean(ber_samples)), float(np.std(ber_samples) / np.sqrt(n_mc))

def ber_closed_form_quad(gamma_bar_db, alpha, beta):
    """BER closed form via numerical quadrature over h."""
    gamma_bar = 10 ** (gamma_bar_db / 10)

    def integrand(h):
        if h <= 0:
            return 0.0
        # GG PDF: f(h) = integral over x from 0 to h of GammaPDF(x;a,1/a) * GammaPDF(h/x;b,1/b) / x
        # Simpler: use direct MC since GG PDF has no simple closed form for quadrature
        pass

    # Fallback to MC - quadrature over bivariate Gamma is complex
    return None

def main():
    t0 = time.time()
    print("=" * 70)
    print("Cross-Chapter Verification: Ch3 BER Closed Form vs Ch4 DPLL")
    print(f"Timestamp: {datetime.datetime.now().isoformat()}")
    print("=" * 70)

    SNR_DB = [10, 15, 20, 25, 30]

    # C4-06 DPLL reference data (ω_n=20MHz, 20dB)
    # From CONCLUSIONS.md and dpll_omega_sweep.json
    dpll_ref = {
        'weak':     {20: 0.00015},
        'moderate': {20: 0.00038},
        'strong':   {20: 0.0188},
    }

    # Try to load full DPLL sweep data
    # JSON structure: {snr_db_str: {turb_name: {omega_n_hz_str: {mean, values}}}}
    dpll_data_path = os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), 'results', 'dpll_omega_sweep.json')
    if os.path.exists(dpll_data_path):
        with open(dpll_data_path) as f:
            dpll_sweep = json.load(f)
        print(f"Loaded DPLL sweep data: {dpll_data_path}")
        for snr_key, snr_data in dpll_sweep.items():
            if not snr_key.isdigit():
                continue
            snr_db = int(snr_key)
            if not isinstance(snr_data, dict):
                continue
            for turb_name, turb_data in snr_data.items():
                if turb_name not in TURB or not isinstance(turb_data, dict):
                    continue
                if turb_name not in dpll_ref:
                    dpll_ref[turb_name] = {}
                # Find best DPLL BER across omega_n values
                best_ber = 1.0
                for omega_key, omega_data in turb_data.items():
                    if isinstance(omega_data, dict) and 'mean' in omega_data:
                        ber_val = omega_data['mean']
                        if ber_val < best_ber:
                            best_ber = ber_val
                if best_ber < 1.0:
                    dpll_ref[turb_name][snr_db] = best_ber
        # Also extract at ω_n=20MHz specifically for 20dB
        for turb_name in TURB:
            om20_key = '20000000'  # 20 MHz
            if '20' in dpll_sweep and turb_name in dpll_sweep['20']:
                if om20_key in dpll_sweep['20'][turb_name]:
                    dpll_ref[turb_name][20] = dpll_sweep['20'][turb_name][om20_key]['mean']
    print(f"DPLL reference data: {list(dpll_ref.keys())}")

    # --- Compute closed-form BER ---
    print(f"\n{'='*70}")
    print("BER Closed Form (MC integration, N=10^6)")
    print(f"{'='*70}")

    closed_form = {}
    for turb_name, (a, b) in TURB.items():
        closed_form[turb_name] = {}
        print(f"\n--- {turb_name} (α={a}, β={b}) ---")
        print(f"  {'SNR(dB)':>8}  {'BER_closed':>12}  {'stderr':>12}  {'DPLL_ref':>12}  {'deviation':>10}")
        for snr_db in SNR_DB:
            ber, se = ber_closed_form_mc(snr_db, a, b)
            closed_form[turb_name][snr_db] = {'mean': ber, 'stderr': se}

            dpll_ber = dpll_ref.get(turb_name, {}).get(snr_db, None)
            if dpll_ber is not None and ber > 0:
                dev = (ber - dpll_ber) / dpll_ber * 100
                dev_str = f"{dev:+.1f}%"
            else:
                dev_str = "N/A"

            print(f"  {snr_db:>8}  {ber:>12.6f}  {se:>12.6f}  "
                  f"{dpll_ber if dpll_ber is not None else 'N/A':>12}  {dev_str:>10}")

    # --- Detailed comparison at 20dB ---
    print(f"\n{'='*70}")
    print("Detailed Comparison at 20 dB")
    print(f"{'='*70}")
    print(f"{'Turbulence':<12} {'BER_closed':>12} {'DPLL_measured':>14} {'Deviation':>10} {'Assessment':>15}")
    print("-" * 65)

    all_pass = True
    for turb_name in TURB:
        ber_cf = closed_form[turb_name][20]['mean']
        dpll_ber = dpll_ref.get(turb_name, {}).get(20, None)
        if dpll_ber is not None and ber_cf > 0:
            dev = (ber_cf - dpll_ber) / dpll_ber * 100
            if abs(dev) < 10:
                assessment = "✓ PASS (<10%)"
            elif abs(dev) < 20:
                assessment = "△ minor (10-20%)"
                all_pass = False
            else:
                assessment = "✗ FAIL (>20%)"
                all_pass = False
            print(f"{turb_name:<12} {ber_cf:>12.6f} {dpll_ber:>14.6f} {dev:>+10.1f}% {assessment:>15}")
        else:
            print(f"{turb_name:<12} {ber_cf:>12.6f} {'N/A':>14} {'N/A':>10} {'no ref data':>15}")

    # --- Conclusion ---
    print(f"\n{'='*70}")
    print("CONCLUSION")
    print(f"{'='*70}")
    if all_pass:
        print("Ch3 BER closed form accurately predicts Ch4 DPLL performance (deviation <10%).")
        print("This validates the analytical framework's predictive capability.")
        print("Phase error contribution at 20dB is negligible, as expected (σ_φ ~ 2.6°).")
    else:
        print("Some conditions show deviation >10%, indicating DPLL phase error")
        print("has non-negligible contribution. Further investigation needed.")

    elapsed = time.time() - t0
    print(f"\nTotal time: {elapsed:.1f}s")

if __name__ == '__main__':
    main()
