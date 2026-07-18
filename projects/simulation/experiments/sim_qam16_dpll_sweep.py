#!/usr/bin/env python3
"""16-QAM DPLL ω_n sweep + SNR curves — Ch4 创新点(2) 扩展实验

将现有 QPSK 仿真迁移至 16-QAM，回答三个问题:
1. DPLL ω_n 最优值是否因调制改变？
2. 16-QAM 的绝对 BER 性能如何？
3. 与 QPSK 相比，16-QAM 对 ω_n 的敏感度是否不同？

TL-25 checklist:
1. 共享信道: np.random.seed() 全局控制 (TL-13 fix) [确认]
2. 重生信道: 不适用（不改物理参数） [确认]
3. 从 common.py 导入: qam16_mod/demod/dpll_track_dd/resolve_qam16 [确认]
4. 基线已优化: FIXED_CFG_OPTIMAL [确认]
5. 先写理论预期: 见下方
6. 输出含元数据: JSON [确认]

理论预期（TL-20）:
- 16-QAM 需要 DD 鉴相器（VV/BPS 的 4 次方/sign() 不兼容）
- 16-QAM 需要更高 SNR 才能达到与 QPSK 相近的 BER
- ω_n 最优值可能与 QPSK 相近（跟踪需求相同，但噪声容忍度不同）
- 量化锚点:
  - weak 20dB BER 应在 1e-3~1e-2 量级
  - strong 15dB BER 应在 0.1~0.3 量级
  - ω_n=20MHz 应接近最优（与 QPSK 一致则强化固定参数结论）

FOE 方案: Oracle FOE（FFT 4th-power 不兼容 16-QAM）
CPR 方案: DPLL(DD) — 唯一兼容 16-QAM 的 CPR 方法
"""

import sys, os, json, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import (
    TURB, BLOCK, T_S, R_SYM, F_RESIDUAL, DOPPLER_HIGH, FIXED_CFG_OPTIMAL,
    gg_block, doppler_phase, qam16_mod, qam16_demod,
    dpll_track_dd, resolve_qam16, amp_limit, mmse_equalize, db_ratio,
    save_results,
)

# ═══════════════════════════════════════════════════════════════
# Config
# ═══════════════════════════════════════════════════════════════
OMEGA_N_VALUES = [2e6, 5e6, 10e6, 20e6, 50e6, 100e6]
TURB_LEVELS = ['weak', 'moderate', 'strong']
SNR_DB = [10, 15, 20, 25, 30]
N_SEEDS = 10
SEEDS = list(range(1000, 1000 + N_SEEDS))
NS = 50000
F_DOT = DOPPLER_HIGH
BER_FLOOR = 1e-7

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ═══════════════════════════════════════════════════════════════
# Signal generation (TL-13 compliant: global seed)
# ═══════════════════════════════════════════════════════════════

def generate_qam16_signal(Ns, gamma_bar, turb_name, f_dot, seed=42):
    """Generate 16-QAM signal. Global np.random.seed for channel sharing."""
    np.random.seed(seed)
    alpha, beta = TURB[turb_name]

    bits = np.random.randint(0, 2, size=4 * Ns)
    tx = qam16_mod(bits)

    h_per_sym = gg_block(Ns, alpha, beta, BLOCK)[:Ns]
    phi = doppler_phase(Ns, f_res=F_RESIDUAL, f_dot=f_dot)

    noise_var = 1.0 / (2 * gamma_bar)
    noise = np.sqrt(noise_var) * (np.random.randn(Ns) + 1j * np.random.randn(Ns))
    rx_raw = np.sqrt(h_per_sym) * tx * np.exp(1j * phi) + noise

    return {
        'bits': bits, 'tx': tx, 'rx_raw': rx_raw,
        'h': h_per_sym, 'phi': phi,
        'gamma_bar': gamma_bar, 'turb_name': turb_name,
    }


# ═══════════════════════════════════════════════════════════════
# Carrier recovery
# ═══════════════════════════════════════════════════════════════

def run_dpll_dd_qam16(rx_eq, bits, omega_n):
    """Oracle FOE + DD-DPLL for 16-QAM."""
    N = len(rx_eq)
    phi_fo = 2 * np.pi * F_RESIDUAL * np.arange(N) * T_S
    rx_foc = rx_eq * np.exp(-1j * phi_fo)
    rx_out, _ = dpll_track_dd(rx_foc, omega_n=omega_n, mod='qam16')
    return resolve_qam16(rx_out, bits)


# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════

def main():
    t0 = time.time()
    print("=" * 70)
    print("16-QAM DPLL ω_n Sweep + SNR Curves")
    print(f"  ω_n: {[int(o/1e6) for o in OMEGA_N_VALUES]} MHz")
    print(f"  SNR: {SNR_DB} dB")
    print(f"  Seeds: {N_SEEDS}")
    print("=" * 70)

    results_omega = {}  # omega sweep: {snr: {turb: {omega: {mean, values}}}}
    results_snr = {}    # snr curve at optimal: {turb: {snr: {mean, values}}}

    total = len(SNR_DB) * len(TURB_LEVELS) * len(OMEGA_N_VALUES) * N_SEEDS
    done = 0

    for snr_db in SNR_DB:
        gamma_bar = 10 ** (snr_db / 10)
        results_omega[str(snr_db)] = {}

        for turb in TURB_LEVELS:
            results_omega[str(snr_db)][turb] = {}

            for omega_n in OMEGA_N_VALUES:
                bers = []
                for sd in SEEDS:
                    shared = generate_qam16_signal(NS, gamma_bar, turb, F_DOT, seed=sd)
                    rx_eq = amp_limit(mmse_equalize(shared['rx_raw'], shared['h'], gamma_bar), 3.0)
                    ber = run_dpll_dd_qam16(rx_eq, shared['bits'], omega_n)
                    bers.append(max(ber, BER_FLOOR))
                    done += 1

                mean_ber = float(np.mean(bers))
                results_omega[str(snr_db)][turb][str(int(omega_n))] = {
                    'ber_mean': mean_ber,
                    'ber_std': float(np.std(bers)),
                    'ber_values': [float(b) for b in bers],
                }

                if done % 100 == 0 or done == total:
                    elapsed = time.time() - t0
                    print(f"[{done}/{total}] SNR={snr_db}dB {turb} "
                          f"ω_n={omega_n/1e6:.0f}MHz BER={mean_ber:.2e} ({elapsed:.0f}s)")

    # ── Extract SNR curves at ω_n=20MHz ──
    print(f"\n{'='*70}")
    print("SNR Curves (ω_n=20MHz)")
    print(f"{'='*70}")

    optimal_omega = 20e6
    for turb in TURB_LEVELS:
        results_snr[turb] = {}
        print(f"\n--- {turb} ---")
        for snr_db in SNR_DB:
            d = results_omega[str(snr_db)][turb].get(str(int(optimal_omega)), {})
            mean_ber = d.get('ber_mean', 1.0)
            results_snr[turb][str(snr_db)] = d
            print(f"  SNR={snr_db:>2}dB: BER={mean_ber:.2e}")

    # ── Find optimal ω_n per condition ──
    print(f"\n{'='*70}")
    print("OPTIMAL ω_n PER CONDITION")
    print(f"{'='*70}")
    print(f"{'Turb':<10} {'SNR':>5} | {'Best ω_n':>10} {'BER':>10} | {'QPSK best':>10} {'Same?':>6}")
    print("-" * 65)

    # Load QPSK data for comparison
    qpsk_path = os.path.join(OUT, 'results', 'dpll_omega_sweep.json')
    qpsk_data = None
    if os.path.exists(qpsk_path):
        with open(qpsk_path) as f:
            qpsk_data = json.load(f)

    for turb in TURB_LEVELS:
        for snr_db in SNR_DB:
            cond = results_omega[str(snr_db)][turb]
            best_omega = min(cond, key=lambda o: cond[o]['ber_mean'])
            best_ber = cond[best_omega]['ber_mean']

            qpsk_best = "N/A"
            same = "?"
            if qpsk_data and str(snr_db) in qpsk_data.get('results', {}):
                qpsk_cond = qpsk_data['results'][str(snr_db)].get(turb, {})
                if qpsk_cond:
                    qpsk_best_o = min(qpsk_cond, key=lambda o: qpsk_cond[o]['ber_mean'])
                    qpsk_best = f"{int(qpsk_best_o)/1e6:.0f}MHz"
                    same = "YES" if best_omega == qpsk_best_o else "no"

            print(f"{turb:<10} {snr_db:>5} | "
                  f"{int(best_omega)/1e6:>8.0f}MHz {best_ber:>10.2e} | "
                  f"{qpsk_best:>10} {same:>6}")

    # ── Save JSON ──
    output = {
        'omega_sweep': results_omega,
        'snr_curves': results_snr,
        'meta': {
            'modulation': '16-QAM',
            'omega_n_values': [int(o) for o in OMEGA_N_VALUES],
            'turb_levels': TURB_LEVELS,
            'snr_points': SNR_DB,
            'seeds': SEEDS,
            'Ns': NS,
            'foe_method': 'oracle',
            'cpr_method': 'DPLL_DD',
            'note': '16-QAM DPLL omega_n sweep + SNR curves at omega_n=20MHz',
        }
    }

    out_path = os.path.join(OUT, 'results', 'qam16_dpll_omega_sweep.json')
    save_results(output, out_path, 'sim_qam16_dpll_sweep')

    elapsed = time.time() - t0
    print(f"\nTotal time: {elapsed:.1f}s")


if __name__ == '__main__':
    main()
