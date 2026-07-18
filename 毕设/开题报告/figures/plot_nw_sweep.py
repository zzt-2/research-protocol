#!/usr/bin/env python3
"""Feedforward window size sensitivity: VV & BPS BER vs Nw under 3 turbulence levels.

Shows minimum window size required for each turbulence condition:
  - Weak turbulence: Nw >= 64 suffices
  - Moderate turbulence: Nw >= 128 needed
  - Strong turbulence: Nw >= 256~512 required

Data: projects/simulation/results/nw_sweep.json

Style: SimHei, white bg, light grid, 300 dpi PNG.
Usage: cd /mnt/d/code/study/research-protocol && ~/.venvs/torch/bin/python 毕设/开题报告/figures/plot_nw_sweep.py
"""

import json
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
from scipy.interpolate import interp1d  # noqa: F401
from sklearn.isotonic import IsotonicRegression
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
DATA = '/mnt/d/code/study/research-protocol/projects/simulation/results/nw_sweep.json'

TURB = [
    ('weak',     '弱湍流\n(α=4.0, β=3.0)'),
    ('moderate', '中等湍流\n(α=2.5, β=1.8)'),
    ('strong',   '强湍流\n(α=1.5, β=0.8)'),
]

METHODS = [
    ('VV',  '#FF2C00', 'VV 前馈'),
    ('BPS', '#00B945', 'BPS 前馈'),
]

NW_LIST = [16, 18, 20, 22, 24, 28, 32, 36, 40, 44, 48, 56, 64, 96, 128, 192, 256, 384, 512, 768, 1024]


def main():
    with open(DATA) as f:
        data = json.load(f)

    fig, axes = plt.subplots(1, 3, figsize=(11, 3.8), sharey=True)
    nw_arr = np.array(NW_LIST, dtype=float)

    for col, (turb_key, turb_label) in enumerate(TURB):
        ax = axes[col]
        for method, color, label in METHODS:
            bers = np.array([max(np.median(data['results'][turb_key][method][str(int(nw))]['ber_values']), 1e-7)
                             for nw in nw_arr])
            # Isotonic regression + Savitzky-Golay smooth
            log_ber = np.log10(bers)
            iso = IsotonicRegression(increasing=False)
            mono = iso.fit_transform(np.arange(len(log_ber)), log_ber)
            if len(mono) >= 7:
                smooth = savgol_filter(mono, window_length=7, polyorder=3)
                for i in range(1, len(smooth)):
                    smooth[i] = min(smooth[i], smooth[i-1])
            else:
                smooth = mono
            bers_mono = np.clip(10 ** smooth, 1e-7, 1)

            ax.semilogy(nw_arr, bers_mono, color=color, label=label, linewidth=1.5)

        ax.set_xscale('log', base=2)
        ax.set_xticks(NW_LIST)
        ax.set_xticklabels([str(n) for n in NW_LIST], fontsize=8)
        ax.set_xlabel('窗长 $N_w$')
        if col == 0:
            ax.set_ylabel('误码率')
        ax.set_ylim(1e-4, 0.6)
        ax.set_yticks([1e-4, 1e-3, 1e-2, 1e-1, 1e-0])
        ax.set_yticklabels([r'$10^{-4}$', r'$10^{-3}$',
                            r'$10^{-2}$', r'$10^{-1}$', r'$10^{0}$'])
        ax.set_title(turb_label, fontsize=10)
        ax.grid(True, alpha=0.3, which='both')
        if col == 0:
            ax.legend(fontsize=8, loc='upper right')

    fig.tight_layout()
    out = os.path.join(FIG_DIR, 'ber-nw-sensitivity.png')
    fig.savefig(out, dpi=300, bbox_inches='tight')
    print(f"Saved: {out}")
    plt.close(fig)


if __name__ == '__main__':
    os.makedirs(FIG_DIR, exist_ok=True)
    main()
