#!/usr/bin/env python3
"""DPLL loop bandwidth sensitivity: BER vs ω_n under 3 turbulence × 3 SNR levels.

Shows feedback stability boundary:
  - Weak turbulence: ω_n up to 50M stable, 100M diverges
  - Moderate: ω_n > 20M starts degrading
  - Strong: ω_n > 10M loses lock

Data: projects/simulation/results/dpll_omega_sweep.json

Style: SimHei, white bg, light grid, 300 dpi PNG.
Usage: cd /mnt/d/code/study/research-protocol && ~/.venvs/torch/bin/python 毕设/开题报告/figures/plot_dpll_omega_sweep.py
"""

import json
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
from scipy.interpolate import interp1d  # noqa: F401
from scipy.signal import savgol_filter

# ── Style ──
_FONT_PATH = "/mnt/c/Windows/Fonts/simhei.ttf"
if os.path.exists(_FONT_PATH):
    fontManager.addfont(_FONT_PATH)
plt.rcParams["font.sans-serif"] = ["SimHei"] + plt.rcParams["font.sans-serif"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'legend.fontsize': 9,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
})

FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'png')
DATA = '/mnt/d/code/study/research-protocol/projects/simulation/results/dpll_omega_sweep.json'

TURB = [
    ('weak',     '弱湍流\n(α=4.0, β=3.0)'),
    ('moderate', '中等湍流\n(α=2.5, β=1.8)'),
    ('strong',   '强湍流\n(α=1.5, β=0.8)'),
]

SNR_CONFIGS = [
    ('10', '#0C5DA5', '$E_b/N_0$=10 dB', 'o-'),
    ('15', '#FF9500', '$E_b/N_0$=15 dB', 's--'),
    ('20', '#8E44AD', '$E_b/N_0$=20 dB', '^-.'),
]

OMEGA_LIST = [2e6, 3e6, 5e6, 7e6, 10e6, 15e6, 20e6, 30e6, 50e6, 70e6, 100e6]
OMEGA_LABELS = ['2', '3', '5', '7', '10', '15', '20', '30', '50', '70', '100']


def main():
    with open(DATA) as f:
        data = json.load(f)

    fig, axes = plt.subplots(1, 3, figsize=(11, 3.8), sharey=True)
    omega_arr = np.array(OMEGA_LIST, dtype=float)

    for col, (turb_key, turb_label) in enumerate(TURB):
        ax = axes[col]
        for snr_key, color, label, _marker in [
            ('10', '#0C5DA5', '$E_b/N_0$=10 dB', 'o'),
            ('15', '#FF9500', '$E_b/N_0$=15 dB', 's'),
            ('20', '#8E44AD', '$E_b/N_0$=20 dB', '^'),
        ]:
            bers = np.array([max(np.median(data['results'][snr_key][turb_key][str(int(om))]['ber_values']), 1e-7)
                             for om in omega_arr])
            # Savitzky-Golay smooth in log-space (no monotonicity — U-shape)
            log_ber = np.log10(bers)
            if len(log_ber) >= 7:
                smooth = savgol_filter(log_ber, window_length=7, polyorder=3)
                bers_smooth = np.clip(10 ** smooth, 1e-7, 1)
            else:
                bers_smooth = bers

            ax.semilogy(omega_arr, bers_smooth, color=color, label=label, linewidth=1.5)

        ax.set_xscale('log', base=10)
        ax.set_xticks(OMEGA_LIST)
        ax.set_xticklabels(OMEGA_LABELS, fontsize=8)
        ax.set_xlabel('环路带宽 $\\omega_n$ (rad/s)')
        if col == 0:
            ax.set_ylabel('误码率')
        ax.set_ylim(1e-4, 0.6)
        ax.set_yticks([1e-4, 1e-3, 1e-2, 1e-1, 1e-0])
        ax.set_yticklabels([r'$10^{-4}$', r'$10^{-3}$',
                            r'$10^{-2}$', r'$10^{-1}$', r'$10^{0}$'])
        ax.set_title(turb_label, fontsize=10)
        ax.grid(True, alpha=0.3, which='both')
        if col == 0:
            ax.legend(fontsize=8, loc='upper left')

    fig.tight_layout()
    out = os.path.join(FIG_DIR, 'ber-dpll-omega-sensitivity.png')
    fig.savefig(out, dpi=300, bbox_inches='tight')
    print(f"Saved: {out}")
    plt.close(fig)


if __name__ == '__main__':
    os.makedirs(FIG_DIR, exist_ok=True)
    main()
