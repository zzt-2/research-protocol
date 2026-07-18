#!/usr/bin/env python3
"""16-QAM NMSE turbulence sweep: test CE error impact on QAM modulation.

TL-25 checklist:
1. 共享信道: 使用 generate_shared_realization 获取 h/phi/noise [确认]
2. 重生信道: 不适用（不改物理参数） [确认]
3. 从 common.py 导入: qam16_mod/qam16_demod/dpll_track_dd [确认]
4. 基线已优化: 使用 FIXED_CFG_OPTIMAL [确认]
5. 先写理论预期: 见下方
6. 输出含元数据: save_results 保存 [确认]

理论预期（TL-20）:
- QPSK 免疫根因: W = sqrt(h)/(h+c) > 0 → sign() 判决对正缩放免疫
- 16-QAM 判决依赖幅度: h_est 误差引入缩放偏移导致判决边界偏移
- 预期: NMSE 0~-20dB 对 16-QAM BER 有渐进影响（NMSE 越差 BER 越高）
- 量化锚点:
  - NMSE=0dB 时退化可能 1-5dB（幅度判决对缩放敏感）
  - NMSE=-20dB 时退化 <0.5dB
  - 如果 NMSE=0dB 退化 <0.5dB → QAM 也不敏感，增强失败

FOE 方案: Oracle FOE（方案 C）— 用真实残余频偏补偿，聚焦 NMSE 对 CPR 的影响
CPR 方案: DPLL(DD) — DD 鉴相器对 QAM 兼容，VV/BPS 因 4 次方鉴相器不兼容不纳入
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import *
import json

# ═══════════════════════════════════════════════════════════════
# Config
# ═══════════════════════════════════════════════════════════════
TURB_LEVELS = ['weak', 'moderate', 'strong']
METHODS = ['DPLL_DD', 'DPLL_DD_oracle_h']  # DD-DPLL with noisy/oracle h

N_SEEDS = 10
SEEDS = list(range(1000, 1000 + N_SEEDS))
NS = 50000
F_DOT = DOPPLER_HIGH

# 16-QAM needs higher SNR than QPSK
SNR_DB = [10, 15, 20, 25, 30]
GAMMA_BARS = [10 ** (s / 10) for s in SNR_DB]

NMSE_DB = [-20, -10, -5, 0]

BER_FLOOR = 1e-7


# ═══════════════════════════════════════════════════════════════
# Noise model (same as QPSK sweep — multiplicative, Model A)
# ═══════════════════════════════════════════════════════════════

def noisy_h(h_true_blocks, nmse_db, rng):
    """Multiplicative noise: h_noisy = |h*(1+noise)|"""
    sigma = np.sqrt(10 ** (nmse_db / 10))
    n_real = rng.randn(len(h_true_blocks))
    n_imag = rng.randn(len(h_true_blocks))
    h_noisy = h_true_blocks * (1 + sigma * n_real + 1j * sigma * n_imag)
    return np.abs(h_noisy)


# ═══════════════════════════════════════════════════════════════
# Signal generation for 16-QAM
# ═══════════════════════════════════════════════════════════════

def generate_qam16_signal(Ns, gamma_bar, turb_name, f_dot, seed=42):
    """Generate 16-QAM signal with shared channel realization.

    TL-13 fix: use np.random.seed() for global RNG control so that
    gg_block() and doppler_phase() produce identical channels when
    called with the same seed (oracle vs NMSE loops share channel).
    Pattern matches generate_shared_realization() in common.py.
    """
    np.random.seed(seed)
    alpha, beta = TURB[turb_name]

    # Bits: 4 bits per QAM16 symbol
    bits = np.random.randint(0, 2, size=4 * Ns)
    tx = qam16_mod(bits)

    # Channel — gg_block and doppler_phase both use global RNG
    h_per_sym = gg_block(Ns, alpha, beta, BLOCK)[:Ns]
    h_block_vals = np.array([h_per_sym[i * BLOCK] for i in range(Ns // BLOCK)])
    phi = doppler_phase(Ns, f_res=F_RESIDUAL, f_dot=f_dot)

    # Received signal: r = sqrt(h) * tx * exp(j*phi) + n
    noise_var = 1.0 / (2 * gamma_bar)
    noise = np.sqrt(noise_var) * (np.random.randn(Ns) + 1j * np.random.randn(Ns))
    rx_raw = np.sqrt(h_per_sym) * tx * np.exp(1j * phi) + noise

    return {
        'bits': bits, 'tx': tx, 'rx_raw': rx_raw,
        'h': h_per_sym, 'h_blocks': h_block_vals,
        'phi': phi, 'gamma_bar': gamma_bar, 'turb_name': turb_name,
    }


# ═══════════════════════════════════════════════════════════════
# Carrier recovery for 16-QAM
# ═══════════════════════════════════════════════════════════════

def oracle_foe_compensate(rx, phi):
    """Oracle FOE: compensate true residual frequency offset."""
    # True FO phase: phi contains FO + Doppler + laser
    # We compensate only the FO component: phi_fo = 2*pi*f_res*k*T_s
    k = np.arange(len(rx))
    phi_fo = 2 * np.pi * F_RESIDUAL * k * T_S
    return rx * np.exp(-1j * phi_fo)


def run_dpll_dd(rx_eq, bits, use_oracle_h=False, shared=None, h_noisy_blocks=None, gamma_bar=None):
    """DD-DPLL carrier recovery for 16-QAM."""
    N = len(rx_eq)
    # Oracle FOE compensation
    phi_fo = 2 * np.pi * F_RESIDUAL * np.arange(N) * T_S
    rx_foc = rx_eq * np.exp(-1j * phi_fo)
    # DD-DPLL tracking
    rx_out, _ = dpll_track_dd(rx_foc, omega_n=20e6, mod='qam16')
    return resolve_qam16(rx_out, bits)


# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════

def main():
    t0 = time.time()
    print("=" * 70)
    print("16-QAM NMSE Turbulence Sweep")
    print("  Methods: DPLL(DD) with oracle FOE")
    print("  NMSE levels: " + str(NMSE_DB) + " dB")
    print("=" * 70)

    results = {}

    for turb_name in TURB_LEVELS:
        print(f"\n{'#'*70}")
        print(f"# TURBULENCE: {turb_name}  (a={TURB[turb_name][0]}, b={TURB[turb_name][1]})")
        print(f"{'#'*70}")
        results[turb_name] = {}

        for snr_db, gamma_bar in zip(SNR_DB, GAMMA_BARS):
            print(f"\n  SNR = {snr_db} dB, turb = {turb_name}")
            results[turb_name][snr_db] = {}

            # -- Oracle baselines (perfect h, no NMSE) --
            oracle_bers = []
            for sd in SEEDS:
                shared = generate_qam16_signal(NS, gamma_bar, turb_name, F_DOT, seed=sd)
                rx_eq_oracle = amp_limit(
                    mmse_equalize(shared['rx_raw'], shared['h'], gamma_bar), 3.0)
                ber = run_dpll_dd(rx_eq_oracle, shared['bits'])
                oracle_bers.append(ber)

            oracle_mean = max(float(np.mean(oracle_bers)), BER_FLOOR)
            results[turb_name][snr_db]['oracle'] = {
                'mean': oracle_mean,
                'values': [float(x) for x in oracle_bers]
            }
            print(f"    oracle DPLL(DD): BER={oracle_mean:.2e}")

            # -- NMSE sweep --
            for nmse_db in NMSE_DB:
                bers = []
                for sd in SEEDS:
                    shared = generate_qam16_signal(NS, gamma_bar, turb_name, F_DOT, seed=sd)
                    h_true_blocks = shared['h_blocks']
                    rng_noisy = np.random.RandomState(sd + 50000)
                    h_noisy_blocks = noisy_h(h_true_blocks, nmse_db, rng_noisy)

                    h_noisy_per_sym = np.repeat(h_noisy_blocks, BLOCK)[:NS]
                    rx_eq = amp_limit(
                        mmse_equalize(shared['rx_raw'], h_noisy_per_sym, gamma_bar), 3.0)

                    ber = run_dpll_dd(rx_eq, shared['bits'])
                    bers.append(ber)

                mean_ber = max(float(np.mean(bers)), BER_FLOOR)
                degrade = float(db_ratio(mean_ber, oracle_mean))

                results[turb_name][snr_db][nmse_db] = {
                    'mean': mean_ber,
                    'values': [float(x) for x in bers],
                    'degradation_dB': degrade,
                }
                print(f"    NMSE={nmse_db:>3d}dB: BER={mean_ber:.2e} (D={degrade:+.2f}dB)")

    # -- Compare with QPSK data --
    print(f"\n{'='*70}")
    print("COMPARISON WITH QPSK (from existing data)")
    print(f"{'='*70}")

    qpsk_path = os.path.join(OUT, 'results', 'nmse_turbulence_sweep.json')
    if os.path.exists(qpsk_path):
        with open(qpsk_path) as f:
            qpsk_data = json.load(f)
        print(f"\n{'Turb':<10} {'SNR':>5} {'NMSE':>5} | {'QAM16 D':>10} {'QPSK D':>10} {'QAM worse?':>10}")
        print("-" * 60)
        for turb_name in TURB_LEVELS:
            for snr_db in SNR_DB:
                for nmse_db in NMSE_DB:
                    qam = results[turb_name][snr_db].get(nmse_db, {})
                    qam_deg = qam.get('degradation_dB', None)

                    # QPSK degradation from existing data (Model A, DPLL method)
                    qpsk_deg = None
                    try:
                        qpsk_oracle = qpsk_data['results'][turb_name][str(snr_db)]['oracle']['DPLL']['mean']
                        qpsk_nmse = qpsk_data['results'][turb_name][str(snr_db)]['A'][str(nmse_db)]['DPLL']['mean']
                        qpsk_deg = float(db_ratio(qpsk_nmse, qpsk_oracle))
                    except (KeyError, TypeError):
                        pass

                    if qam_deg is not None:
                        worse = "YES" if (qpsk_deg is not None and qam_deg > (qpsk_deg + 0.3)) else "no"
                        qpsk_str = f"{qpsk_deg:+.2f}" if qpsk_deg is not None else "N/A"
                        print(f"{turb_name:<10} {snr_db:>5} {nmse_db:>5} | "
                              f"{qam_deg:>+10.2f} {qpsk_str:>10} {worse:>10}")

    # -- Degradation check --
    print(f"\n{'='*70}")
    print("DEGRADATION CHECK (target: QAM16 degradation > QPSK degradation)")
    print(f"{'='*70}")
    max_degrade = 0.0
    qam_worse_count = 0
    total_count = 0
    for turb_name in TURB_LEVELS:
        for snr_db in SNR_DB:
            oracle = results[turb_name][snr_db]['oracle']['mean']
            for nmse_db in NMSE_DB:
                d = results[turb_name][snr_db][nmse_db]['degradation_dB']
                max_degrade = max(max_degrade, d)
                total_count += 1
                if d > 0.5:
                    qam_worse_count += 1
    print(f"  Max degradation: {max_degrade:+.2f} dB")
    print(f"  Conditions with D > 0.5 dB: {qam_worse_count}/{total_count}")
    if qam_worse_count > 0:
        print("  ✓ QAM16 IS sensitive to NMSE — IP1 enhancement SUCCESSFUL")
    else:
        print("  ✗ QAM16 NOT sensitive to NMSE — IP1 enhancement FAILED")

    # --- Save JSON ---
    out_dir = os.path.join(OUT, 'results')
    os.makedirs(out_dir, exist_ok=True)
    json_path = os.path.join(out_dir, 'nmse_qam16_turbulence_sweep.json')
    with open(json_path, 'w') as f:
        json.dump({
            'results': results,
            'meta': {
                'N_seeds': N_SEEDS, 'seeds': SEEDS, 'Ns': NS,
                'snr_db': SNR_DB, 'gamma_bars': [float(g) for g in GAMMA_BARS],
                'nmse_levels_db': NMSE_DB,
                'modulation': '16-QAM',
                'foe_method': 'oracle',
                'cpr_method': 'DPLL_DD',
                'note': '16-QAM NMSE sweep: oracle FOE + DD-DPLL',
            }
        }, f, indent=2)
    print(f"\nJSON saved: {json_path}")

    elapsed = time.time() - t0
    print(f"\nTotal time: {elapsed:.1f}s")


if __name__ == '__main__':
    main()
