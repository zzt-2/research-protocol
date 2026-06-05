#!/usr/bin/env python3
"""Generate 3 basic result figures for Chapter 3 of kaiti report.

Figures:
  1. gg-pdf-three-turbulence.png  — GG PDF, weak/moderate/strong
  2. block-fading-waveform.png    — Block fading channel realization
  3. ber-snr-gg-fading.png        — QPSK BER over GG fading (Monte Carlo)

Style: SimHei, white bg, light grid, no title, 300 dpi PNG.
       Matches plot_kaiti_figures.py conventions exactly.

GG parameters from kaiti-report.md Table 3-1:
  weak:     alpha=4.0, beta=3.0
  moderate: alpha=2.5, beta=1.8
  strong:   alpha=1.5, beta=0.8

Usage: ~/.venvs/torch/bin/python plot_ch3_basic_figures.py
"""

import numpy as np
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
from scipy.special import gamma as Gamma_func
from scipy.special import kv as bessel_kv
from scipy.special import erfc

# ── Style (matching plot_kaiti_figures.py) ──────────────────────────
_FONT_PATH = "/mnt/c/Windows/Fonts/simhei.ttf"
if os.path.exists(_FONT_PATH):
    fontManager.addfont(_FONT_PATH)
plt.rcParams["font.sans-serif"] = ["SimHei"] + plt.rcParams["font.sans-serif"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'legend.fontsize': 10,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
})

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'png')

# GG parameters from kaiti-report.md Table 3-1
TURB = [
    # (key, alpha, beta, color, label)
    ('weak',     4.0, 3.0, '#0C5DA5', '弱湍流 ($\\alpha$=4.0, $\\beta$=3.0)'),
    ('moderate', 2.5, 1.8, '#FF2C00', '中等湍流 ($\\alpha$=2.5, $\\beta$=1.8)'),
    ('strong',   1.5, 0.8, '#00B945', '强湍流 ($\\alpha$=1.5, $\\beta$=0.8)'),
]


# =====================================================================
# Fig 1: Gamma-Gamma PDF
# =====================================================================
def gg_pdf(h, alpha, beta):
    coeff = 2 * (alpha * beta)**((alpha + beta) / 2) \
            / (Gamma_func(alpha) * Gamma_func(beta))
    return np.real(
        coeff * h**((alpha + beta) / 2 - 1)
        * bessel_kv(abs(alpha - beta), 2 * np.sqrt(alpha * beta * h))
    )


def fig_gg_pdf():
    print("  [1/3] GG概率密度曲线 ...")
    h = np.linspace(0.001, 3.0, 2000)

    fig, ax = plt.subplots(figsize=(5, 3.5))
    for _, alpha, beta, color, label in TURB:
        ax.plot(h, gg_pdf(h, alpha, beta),
                color=color, label=label, linewidth=1.5)

    ax.set_xlabel('归一化辐照度 $h$')
    ax.set_ylabel('概率密度')
    ax.set_xlim(0, 3)
    ax.set_ylim(bottom=0)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3, which='both')
    fig.tight_layout()

    out = os.path.join(OUT_DIR, 'gg-pdf-three-turbulence.png')
    fig.savefig(out, dpi=300, bbox_inches='tight')
    print(f"  -> {out}")
    plt.close(fig)


# =====================================================================
# Fig 2: Block fading waveform
# =====================================================================
def fig_block_fading():
    print("  [2/3] 块衰落信道波形 ...")
    np.random.seed(42)

    B_s = 100       # symbols per block
    N_blocks = 80
    N_total = B_s * N_blocks
    alpha, beta = 2.5, 1.8   # moderate turbulence

    h = np.empty(N_total)
    for i in range(N_blocks):
        X = np.random.gamma(alpha, 1 / alpha)
        Y = np.random.gamma(beta, 1 / beta)
        h[i * B_s : (i + 1) * B_s] = X * Y

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.step(np.arange(N_total), h, color='#0C5DA5', linewidth=0.8, where='mid')

    deep_threshold = 0.3
    for i in range(N_blocks):
        if h[i * B_s] < deep_threshold:
            ax.axvspan(i * B_s, (i + 1) * B_s,
                       alpha=0.15, color='#FF2C00', zorder=0)

    ax.axhline(y=deep_threshold, color='#FF2C00', linestyle='--',
               linewidth=0.8, alpha=0.6, label='深衰落阈值')
    ax.set_xlabel('符号索引')
    ax.set_ylabel('信道增益 $h$')
    ax.set_xlim(0, N_total)
    ax.set_ylim(bottom=0)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3, which='both')
    fig.tight_layout()

    out = os.path.join(OUT_DIR, 'block-fading-waveform.png')
    fig.savefig(out, dpi=300, bbox_inches='tight')
    print(f"  -> {out}")
    plt.close(fig)


# =====================================================================
# Fig 3: BER-SNR (Monte Carlo — no quad integration)
# =====================================================================
def fig_ber_snr():
    print("  [3/3] BER-SNR曲线 (蒙特卡洛, N=2M/档) ...")

    N = 2_000_000
    snr_db = np.arange(0, 31, 0.5)
    snr_lin = 10.0 ** (snr_db / 10.0)

    fig, ax = plt.subplots(figsize=(5, 3.5))

    # AWGN baseline (h=1)
    ber_awgn = 0.5 * erfc(np.sqrt(snr_lin))
    ax.semilogy(snr_db, np.clip(ber_awgn, 1e-8, 1),
                'k--', label='AWGN', linewidth=1.2, alpha=0.7)

    for key, alpha, beta, color, label in TURB:
        rng = np.random.default_rng(seed=12345 + hash(key) % 10000)
        # Sample h from GG: h = X*Y, X~Gamma(a,1/a), Y~Gamma(b,1/b)
        X = rng.gamma(alpha, 1 / alpha, N)
        Y = rng.gamma(beta, 1 / beta, N)
        h_sq = (X * Y) ** 2          # pre-compute h²

        bers = np.empty(len(snr_lin))
        for j, snr in enumerate(snr_lin):
            bers[j] = np.mean(0.5 * erfc(np.sqrt(snr * h_sq)))

        ax.semilogy(snr_db, np.clip(bers, 1e-8, 1),
                    color=color, label=label, linewidth=1.5)

    ax.set_xlabel('$E_b/N_0$/dB')
    ax.set_ylabel('误码率')
    ax.set_ylim(1e-6, 1)
    ax.set_yticks([1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1e0])
    ax.set_yticklabels([r'$10^{-5}$', r'$10^{-4}$', r'$10^{-3}$',
                        r'$10^{-2}$', r'$10^{-1}$', r'$10^{0}$'])
    ax.set_xlim(0, 30)
    ax.legend(fontsize=9, loc='upper left')
    ax.grid(True, alpha=0.3, which='both')
    fig.tight_layout()

    out = os.path.join(OUT_DIR, 'ber-snr-gg-fading.png')
    fig.savefig(out, dpi=300, bbox_inches='tight')
    print(f"  -> {out}")
    plt.close(fig)


# =====================================================================
if __name__ == '__main__':
    print("=" * 50)
    print("第三章基础结果图 (SimHei 中文风格)")
    print("=" * 50)
    os.makedirs(OUT_DIR, exist_ok=True)
    fig_gg_pdf()
    fig_block_fading()
    fig_ber_snr()
    print("\nDone.")
