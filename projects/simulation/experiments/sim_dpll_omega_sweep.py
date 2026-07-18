#!/usr/bin/env python3
"""DPLL omega_n 扫参实验：评估自然频率对 BER 的影响

参数空间：
  omega_n: [2e6, 5e6, 10e6, 20e6, 50e6, 100e6] rad/s
  湍流: weak, moderate, strong
  SNR: 10, 15, 20 dB
  种子: 10 个 (range(1000, 1010))
  符号数: 50000
  Doppler: DOPPLER_HIGH

链路: FOE (FFT 频偏估计) + DPLL (只调 omega_n, zeta=sqrt(2)/2)

理论预期（TL-20）：
  - omega_n 太小 (<5MHz): 跟踪不上频偏变化, BER 高
  - omega_n 太大 (>50MHz): 噪声带宽大, 相位估计方差大, BER 高
  - 最优值应在 10-50 MHz (U 型谷底)
  - 强湍流可能需要更大 omega_n

输出：
  - results/dpll_omega_sweep.json
  - 毕设/写作材料/figures/dpll_omega_sweep.pdf
"""

import sys, os
import json
import time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import (
    DOPPLER_HIGH,
    generate_shared_realization, equalize_oracle, fft_foe,
    dpll_track, resolve_qpsk,
)

# ── 实验参数 ─────────────────────────────────────────────────
OMEGA_N_VALUES = [2e6, 5e6, 10e6, 20e6, 50e6, 100e6]
TURB_LEVELS = ['weak', 'moderate', 'strong']
SNR_POINTS = [10, 15, 20]  # dB
SEEDS = list(range(1000, 1010))
NS = 50000
F_DOT = DOPPLER_HIGH
ZETA = np.sqrt(2) / 2
BER_FLOOR = 1e-7

# ── 路径 ─────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_JSON = os.path.join(BASE, 'results', 'dpll_omega_sweep.json')
OUT_PDF_THESIS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(BASE))),
    '毕设', '写作材料', 'figures', 'dpll_omega_sweep.pdf',
)

# ── 单次试验 ────────────────────────────────────────────────
def run_single_trial(omega_n, turb, gamma_bar, seed):
    """FOE + DPLL(omega_n) 单次试验"""
    shared = generate_shared_realization(NS, gamma_bar, turb, F_DOT, seed=seed)
    rx_eq = equalize_oracle(shared)
    fo_est = fft_foe(rx_eq, N_fft=1024)
    rx_foc = rx_eq * np.exp(-1j * fo_est * np.arange(NS))
    rx_out, _ = dpll_track(rx_foc, omega_n=omega_n, zeta=ZETA)
    ber = resolve_qpsk(rx_out, shared['bits'])
    return max(ber, BER_FLOOR)


# ── 主循环 ───────────────────────────────────────────────────
def main():
    t0 = time.time()
    results = {}

    total = len(SNR_POINTS) * len(TURB_LEVELS) * len(OMEGA_N_VALUES) * len(SEEDS)
    done = 0

    for snr_db in SNR_POINTS:
        gamma_bar = 10 ** (snr_db / 10)
        results[str(snr_db)] = {}

        for turb in TURB_LEVELS:
            results[str(snr_db)][turb] = {}

            for omega_n in OMEGA_N_VALUES:
                ber_list = []
                for sd in SEEDS:
                    ber = run_single_trial(omega_n, turb, gamma_bar, sd)
                    ber_list.append(ber)
                    done += 1
                    if done % 50 == 0 or done == total:
                        elapsed = time.time() - t0
                        print(f"[{done}/{total}] SNR={snr_db}dB turb={turb} "
                              f"omega_n={omega_n/1e6:.0f}MHz seed={sd} "
                              f"BER={ber:.2e}  ({elapsed:.1f}s)")

                ber_arr = np.array(ber_list)
                results[str(snr_db)][turb][str(int(omega_n))] = {
                    'ber_mean': float(np.mean(ber_arr)),
                    'ber_std': float(np.std(ber_arr)),
                    'ber_values': [float(b) for b in ber_arr],
                }

    elapsed = time.time() - t0
    print(f"\nDone in {elapsed:.1f}s ({total} trials)")

    # ── 保存 JSON ────────────────────────────────────────────
    meta = {
        'omega_n_values': [int(o) for o in OMEGA_N_VALUES],
        'turb_levels': TURB_LEVELS,
        'snr_points': SNR_POINTS,
        'seeds': SEEDS,
        'Ns': NS,
        'zeta': float(ZETA),
        'f_dot': float(F_DOT),
    }
    with open(OUT_JSON, 'w') as f:
        json.dump({'meta': meta, 'results': results}, f, indent=2,
                  ensure_ascii=False)
    print(f"JSON saved: {OUT_JSON}")

    # ── 绘图 ─────────────────────────────────────────────────
    plot_results(results, meta)


def plot_results(results, meta):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    omega_mhz = [o / 1e6 for o in OMEGA_N_VALUES]
    snr_colors = {10: '#d62728', 15: '#ff7f0e', 20: '#1f77b4'}
    snr_markers = {10: 'o--', 15: 's-.', 20: '^-'}
    turb_labels = {
        'weak': 'Weak Turbulence',
        'moderate': 'Moderate Turbulence',
        'strong': 'Strong Turbulence',
    }

    fig, axes = plt.subplots(3, 1, figsize=(8, 10), sharex=True)

    for row, turb in enumerate(TURB_LEVELS):
        ax = axes[row]

        for snr_db in SNR_POINTS:
            bers = [results[str(snr_db)][turb][str(int(o))]['ber_mean']
                    for o in OMEGA_N_VALUES]
            style = snr_markers[snr_db]
            color = snr_colors[snr_db]

            ax.loglog(omega_mhz, bers, style, label=f'SNR={snr_db} dB',
                      color=color, markersize=6, linewidth=1.5)

            # annotate optimal omega_n (minimum BER)
            best_idx = int(np.argmin(bers))
            ax.annotate(
                f'{omega_mhz[best_idx]:.0f} MHz\nBER={bers[best_idx]:.1e}',
                xy=(omega_mhz[best_idx], bers[best_idx]),
                xytext=(15, 10), textcoords='offset points',
                fontsize=7, color=color,
                arrowprops=dict(arrowstyle='->', color=color, lw=0.8),
            )

        ax.set_ylabel('Mean BER')
        ax.set_title(turb_labels.get(turb, turb))
        ax.grid(True, which='both', alpha=0.3)
        ax.legend(loc='best', fontsize=8)
        ax.set_xlim(1, 150)

    axes[-1].set_xlabel(r'$\omega_n$ (MHz)')

    fig.suptitle(r'DPLL Natural Frequency $\omega_n$ Sweep'
                 '\n(FOE + DPLL, 50k symbols, 10 seeds)',
                 fontsize=11, y=1.01)
    fig.tight_layout()

    d = os.path.dirname(OUT_PDF_THESIS)
    if d:
        os.makedirs(d, exist_ok=True)
    fig.savefig(OUT_PDF_THESIS, bbox_inches='tight', dpi=300)
    print(f"PDF saved: {OUT_PDF_THESIS}")

    plt.close(fig)


if __name__ == '__main__':
    main()
