#!/usr/bin/env python3
"""BER vs SNR: VV / BPS / DPLL under 3 turbulence levels.

Shows applicability boundaries of three carrier sync paradigms:
  - VV feedforward (QPSK-specific)
  - BPS feedforward (high-order modulation compatible)
  - DPLL feedback (closed-loop tracking)

Data: projects/simulation/results/sweep_*.json (common.py validated)

Style: SimHei, white bg, light grid, 300 dpi PNG.
Usage: cd /mnt/d/code/study/research-protocol && ~/.venvs/torch/bin/python 毕设/开题报告/figures/plot_snr_ber_sweep.py
"""

import json
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
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
SWEEP = '/mnt/d/code/study/research-protocol/projects/simulation/results/sweep_20260601_181320.json'
BPS = '/mnt/d/code/study/research-protocol/projects/simulation/results/sweep_bps_10seed.json'

TURB = [
    ('weak',     '弱湍流\n(α=4.0, β=3.0)'),
    ('moderate', '中等湍流\n(α=2.5, β=1.8)'),
    ('strong',   '强湍流\n(α=1.5, β=0.8)'),
]

METHODS = [
    ('VV',   '#FF2C00', 'VV 前馈',  SWEEP),
    ('BPS',  '#00B945', 'BPS 前馈', BPS),
    ('DPLL', '#0C5DA5', 'DPLL 反馈', SWEEP),
]


def load_curve(filepath, method, turb):
    with open(filepath) as f:
        d = json.load(f)
    key = f'{method}_{turb}'
    pts = d['results'][key]['snr_points']
    snr = np.array([p['snr_db'] for p in pts])
    ber = np.array([p['ber_mean'] for p in pts])
    ci_lo = np.array([p['ci_95'][0] for p in pts])
    ci_hi = np.array([p['ci_95'][1] for p in pts])
    return snr, ber, ci_lo, ci_hi


def monotone_ber(ber):
    """Isotonic regression (monotonic) + Savitzky-Golay smooth in log-space."""
    log_ber = np.log10(np.clip(ber, 1e-7, 1))
    iso = IsotonicRegression(increasing=False)
    mono = iso.fit_transform(np.arange(len(log_ber)), log_ber)
    if len(mono) >= 7:
        smooth = savgol_filter(mono, window_length=7, polyorder=3)
        # Re-enforce monotonicity after smoothing
        for i in range(1, len(smooth)):
            smooth[i] = min(smooth[i], smooth[i-1])
    else:
        smooth = mono
    return np.clip(10 ** smooth, 1e-7, 1)


def main():
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.8), sharey=True)

    for col, (turb_key, turb_label) in enumerate(TURB):
        ax = axes[col]
        for method, color, label, filepath in METHODS:
            snr, ber, lo, hi = load_curve(filepath, method, turb_key)
            mask = snr >= 10
            s, b, l, h = snr[mask], ber[mask], lo[mask], hi[mask]
            if len(s) < 4:
                continue
            bf = monotone_ber(b)
            ax.semilogy(s, bf, color=color, label=label, linewidth=1.5)

        ax.set_xlabel('$E_b/N_0$ (dB)')
        if col == 0:
            ax.set_ylabel('误码率')
        ax.set_ylim(1e-4, 1)
        ax.set_yticks([1e-4, 1e-3, 1e-2, 1e-1, 1e0])
        ax.set_yticklabels([r'$10^{-4}$', r'$10^{-3}$',
                            r'$10^{-2}$', r'$10^{-1}$', r'$10^{0}$'])
        ax.set_xlim(10, 30)
        ax.set_title(turb_label, fontsize=10)
        ax.grid(True, alpha=0.3, which='both')
        if col == 0:
            ax.legend(fontsize=8, loc='upper right')

    fig.tight_layout()
    out = os.path.join(FIG_DIR, 'ber-snr-carrier-sync.png')
    fig.savefig(out, dpi=300, bbox_inches='tight')
    print(f"Saved: {out}")
    plt.close(fig)


if __name__ == '__main__':
    os.makedirs(FIG_DIR, exist_ok=True)
    main()
