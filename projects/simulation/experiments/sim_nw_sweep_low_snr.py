#!/usr/bin/env python3
"""Nw 扫参实验 — 低 SNR 漂移验证

在 10 dB 和 15 dB SNR 下重跑 Nw 扫参，验证转折点是否随 SNR 漂移。

参数空间：
  SNR: [10, 15] dB (gamma_bar = [10, 31.6])
  Nw: [16, 32, 64, 128, 256, 512, 1024]
  方法: VV (vv_cpr), BPS (bps_cpr)
  湍流: weak, moderate, strong
  种子: 10 个 (range(1000, 1010))
  符号数: 50000
  Doppler: DOPPLER_HIGH

输出：
  - results/nw_sweep_low_snr.json
  - 毕设/写作材料/figures/nw_sweep_low_snr.pdf
"""

import sys, os
import json
import time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import (
    DOPPLER_HIGH,
    generate_shared_realization, equalize_oracle, fft_foe,
    vv_cpr, bps_cpr, resolve_qpsk,
)

# ── 实验参数 ─────────────────────────────────────────────────
SNR_POINTS_DB = [10, 15]
GAMMA_BAR_MAP = {10: 10.0, 15: 10**(15/10)}  # linear gamma_bar

NW_VALUES = [16, 32, 64, 128, 256, 512, 1024]
TURB_LEVELS = ['weak', 'moderate', 'strong']
METHODS = ['VV', 'BPS']
SEEDS = list(range(1000, 1010))
NS = 50000
F_DOT = DOPPLER_HIGH
BER_FLOOR = 1e-7
FAIL_THRESH = 0.10  # BER > 10% 视为失败

# ── 路径 ─────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_JSON = os.path.join(BASE, 'results', 'nw_sweep_low_snr.json')
# BASE = projects/simulation/ -> research-protocol/ is 2 levels up
PROJECT_ROOT = os.path.dirname(os.path.dirname(BASE))
OUT_PDF_THESIS = os.path.join(
    PROJECT_ROOT, '毕设', '写作材料', 'figures', 'nw_sweep_low_snr.pdf',
)

# ── 单次试验 ────────────────────────────────────────────────
def run_single_trial(nw, method, turb, gamma_bar, seed):
    """运行单次试验，返回 BER"""
    shared = generate_shared_realization(NS, gamma_bar, turb, F_DOT, seed=seed)
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

    total = (len(SNR_POINTS_DB) * len(TURB_LEVELS) * len(METHODS)
             * len(NW_VALUES) * len(SEEDS))
    done = 0

    for snr_db in SNR_POINTS_DB:
        gamma_bar = GAMMA_BAR_MAP[snr_db]
        snr_key = str(snr_db)
        results[snr_key] = {}

        for turb in TURB_LEVELS:
            results[snr_key][turb] = {}
            for method in METHODS:
                results[snr_key][turb][method] = {}
                for nw in NW_VALUES:
                    ber_list = []
                    for sd in SEEDS:
                        ber = run_single_trial(nw, method, turb, gamma_bar, sd)
                        ber_list.append(ber)
                        done += 1
                        if done % 50 == 0 or done == total:
                            elapsed = time.time() - t0
                            print(f"[{done}/{total}] SNR={snr_db}dB turb={turb} "
                                  f"method={method} Nw={nw} seed={sd} "
                                  f"BER={ber:.2e}  ({elapsed:.1f}s)")

                    ber_arr = np.array(ber_list)
                    results[snr_key][turb][method][str(nw)] = {
                        'ber_mean': float(np.mean(ber_arr)),
                        'ber_std': float(np.std(ber_arr)),
                        'ber_values': [float(b) for b in ber_arr],
                        'fail_rate': float(np.mean(ber_arr > FAIL_THRESH)),
                    }

    elapsed = time.time() - t0
    print(f"\nDone in {elapsed:.1f}s ({total} trials)")

    # ── 保存 JSON ────────────────────────────────────────────
    payload = {
        'meta': {
            'snr_points': SNR_POINTS_DB,
            'nw_values': NW_VALUES,
            'turb_levels': TURB_LEVELS,
            'methods': METHODS,
            'seeds': [SEEDS[0], SEEDS[-1] + 1],
            'Ns': NS,
        },
        'results': results,
    }
    with open(OUT_JSON, 'w') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"JSON saved: {OUT_JSON}")

    # ── 绘图 ─────────────────────────────────────────────────
    plot_results(results)


def plot_results(results):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    turb_labels = {'weak': 'Weak Turbulence', 'moderate': 'Moderate Turbulence',
                   'strong': 'Strong Turbulence'}

    fig, axes = plt.subplots(2, 3, figsize=(14, 8), sharey=True)

    for row_idx, snr_db in enumerate(SNR_POINTS_DB):
        snr_key = str(snr_db)
        for col_idx, turb in enumerate(TURB_LEVELS):
            ax = axes[row_idx, col_idx]
            nw_arr = np.array(NW_VALUES)

            for method, marker, color in [('VV', 'o-', '#1f77b4'),
                                           ('BPS', 's--', '#ff7f0e')]:
                bers = [results[snr_key][turb][method][str(nw)]['ber_mean']
                        for nw in NW_VALUES]
                ax.loglog(nw_arr, bers, marker, label=method, color=color,
                          markersize=5, linewidth=1.5)

                # annotate turning point: smallest Nw where BER < 1e-3
                # (use 1e-3 instead of 1e-4 since low SNR may not reach 1e-4)
                for i, ber in enumerate(bers):
                    if ber < 1e-3:
                        ax.annotate(f'Nw={NW_VALUES[i]}',
                                    xy=(nw_arr[i], ber),
                                    xytext=(5, -15), textcoords='offset points',
                                    fontsize=7, color=color)
                        break

            ax.set_xlabel('Window Size Nw')
            ax.grid(True, which='both', alpha=0.3)
            ax.set_xlim(10, 1200)

            if col_idx == 0:
                ax.set_ylabel(f'SNR = {snr_db} dB\nMean BER')
            ax.set_title(turb_labels.get(turb, turb))

    axes[0, 0].legend(loc='upper right')

    fig.suptitle('VV vs BPS Carrier Recovery -- Nw Sweep at Low SNR\n'
                 '(50k symbols, 10 seeds)',
                 fontsize=11, y=1.02)
    fig.tight_layout()

    d = os.path.dirname(OUT_PDF_THESIS)
    if d:
        os.makedirs(d, exist_ok=True)
    fig.savefig(OUT_PDF_THESIS, bbox_inches='tight', dpi=300)
    print(f"PDF saved: {OUT_PDF_THESIS}")

    plt.close(fig)


if __name__ == '__main__':
    main()
