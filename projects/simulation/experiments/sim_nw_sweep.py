#!/usr/bin/env python3
"""Nw 扫参实验：VV 和 BPS 在不同湍流下的窗口大小敏感性

参数空间：
  Nw: [16, 32, 64, 128, 256, 512, 1024]
  方法: VV (vv_cpr), BPS (bps_cpr)
  湍流: weak, moderate, strong
  种子: 10 个 (range(1000, 1010))
  符号数: 50000
  SNR: 20 dB (gamma_bar=100)
  Doppler: DOPPLER_HIGH

输出：
  - results/nw_sweep.json
  - figures/nw_sweep.pdf
  - 毕设/写作材料/figures/nw_sweep.pdf
"""

import sys, os
import json
import time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import (
    GAMMA_BAR_DEFAULT, DOPPLER_HIGH,
    generate_shared_realization, equalize_oracle, fft_foe,
    vv_cpr, bps_cpr, resolve_qpsk,
)

# ── 实验参数 ─────────────────────────────────────────────────
NW_VALUES = [16, 32, 64, 128, 256, 512, 1024]
TURB_LEVELS = ['weak', 'moderate', 'strong']
METHODS = ['VV', 'BPS']
SEEDS = list(range(1000, 1010))
NS = 50000
GAMMA_BAR = GAMMA_BAR_DEFAULT
F_DOT = DOPPLER_HIGH
BER_FLOOR = 1e-7
FAIL_THRESH = 0.10  # BER > 10% 视为失败

# ── 路径 ─────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_JSON = os.path.join(BASE, 'results', 'nw_sweep.json')
OUT_PDF_FIG = os.path.join(BASE, 'figures', 'nw_sweep.pdf')
OUT_PDF_THESIS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(BASE))),
    '毕设', '写作材料', 'figures', 'nw_sweep.pdf',
)

# ── 单次试验 ────────────────────────────────────────────────
def run_single_trial(nw, method, turb, seed):
    """运行单次试验，返回 BER"""
    shared = generate_shared_realization(NS, GAMMA_BAR, turb, F_DOT, seed=seed)
    rx_eq = equalize_oracle(shared)
    fo_est = fft_foe(rx_eq, N_fft=1024)
    rx_foc = rx_eq * np.exp(-1j * fo_est * np.arange(NS))

    if method == 'VV':
        rx_cpr, _ = vv_cpr(rx_foc, Nw=nw)
    else:
        rx_cpr, _ = bps_cpr(rx_foc, Nw=nw)

    ber = resolve_qpsk(rx_cpr, shared['bits'])
    return max(ber, BER_FLOOR)


# ── 主循环 ───────────────────────────────────────────────────
def main():
    t0 = time.time()
    results = {}

    total = len(TURB_LEVELS) * len(METHODS) * len(NW_VALUES) * len(SEEDS)
    done = 0

    for turb in TURB_LEVELS:
        results[turb] = {}
        for method in METHODS:
            results[turb][method] = {}
            for nw in NW_VALUES:
                ber_list = []
                for sd in SEEDS:
                    ber = run_single_trial(nw, method, turb, sd)
                    ber_list.append(ber)
                    done += 1
                    if done % 50 == 0 or done == total:
                        elapsed = time.time() - t0
                        print(f"[{done}/{total}] turb={turb} method={method} "
                              f"Nw={nw} seed={sd} BER={ber:.2e}  "
                              f"({elapsed:.1f}s)")

                ber_arr = np.array(ber_list)
                results[turb][method][str(nw)] = {
                    'ber_mean': float(np.mean(ber_arr)),
                    'ber_std': float(np.std(ber_arr)),
                    'ber_values': [float(b) for b in ber_arr],
                    'fail_rate': float(np.mean(ber_arr > FAIL_THRESH)),
                }

    elapsed = time.time() - t0
    print(f"\nDone in {elapsed:.1f}s ({total} trials)")

    # ── 保存 JSON ────────────────────────────────────────────
    with open(OUT_JSON, 'w') as f:
        json.dump({'results': results}, f, indent=2, ensure_ascii=False)
    print(f"JSON saved: {OUT_JSON}")

    # ── 绘图 ─────────────────────────────────────────────────
    plot_results(results)


def plot_results(results):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), sharey=True)
    turb_labels = {'weak': 'Weak Turbulence', 'moderate': 'Moderate Turbulence',
                   'strong': 'Strong Turbulence'}

    for idx, turb in enumerate(TURB_LEVELS):
        ax = axes[idx]
        nw_arr = np.array(NW_VALUES)

        for method, marker, color in [('VV', 'o-', '#1f77b4'),
                                       ('BPS', 's--', '#ff7f0e')]:
            bers = [results[turb][method][str(nw)]['ber_mean'] for nw in NW_VALUES]
            ax.loglog(nw_arr, bers, marker, label=method, color=color,
                      markersize=6, linewidth=1.5)

            # annotate turning point: smallest Nw with BER < 1e-4
            for i, ber in enumerate(bers):
                if ber < 1e-4:
                    ax.annotate(f'Nw={NW_VALUES[i]}',
                                xy=(nw_arr[i], ber),
                                xytext=(5, -15), textcoords='offset points',
                                fontsize=7, color=color)
                    break

        ax.set_xlabel('Window Size Nw')
        ax.set_title(turb_labels.get(turb, turb))
        ax.grid(True, which='both', alpha=0.3)
        ax.set_xlim(10, 1200)

    axes[0].set_ylabel('Mean BER')
    axes[0].legend(loc='upper right')

    fig.suptitle('VV vs BPS Carrier Recovery -- Window Size Nw Sweep\n'
                 '(SNR=20 dB, 50k symbols, 10 seeds)',
                 fontsize=11, y=1.02)
    fig.tight_layout()

    for path in [OUT_PDF_FIG, OUT_PDF_THESIS]:
        d = os.path.dirname(path)
        if d:
            os.makedirs(d, exist_ok=True)
        fig.savefig(path, bbox_inches='tight', dpi=300)
        print(f"PDF saved: {path}")

    plt.close(fig)


if __name__ == '__main__':
    main()
