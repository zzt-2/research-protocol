#!/usr/bin/env python3
"""Phase tracking comparison: VV feedforward vs DPLL feedback under GG turbulence.

Redesigned: zoom into a deep-fade event so the contrast is visible.

Three columns: weak / moderate / strong turbulence.
Top row: channel gain h(t) in the zoom window, deep-fade block shaded.
Bottom row: smoothed phase estimation error for VV and DPLL.

Key story: VV spikes during deep fades (no averaging memory),
           DPLL coasts through (loop filter memory).

Style: SimHei, white bg, light grid, no title, 300 dpi PNG.
Usage: ~/.venvs/torch/bin/python plot_phase_tracking.py
"""

import numpy as np
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager

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
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
})

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'png')

# ── Parameters ──
N = 3000
B_s = 100
SNR_db = 20
SNR_lin = 10 ** (SNR_db / 10)
SMOOTH = 20          # running-mean window for phase error

TURB = [
    ('弱湍流\n(α=4.0, β=3.0)', 4.0, 3.0),
    ('中等湍流\n(α=2.5, β=1.8)', 2.5, 1.8),
    ('强湍流\n(α=1.5, β=0.8)', 1.5, 0.8),
]


def block_fading_channel(N, B_s, alpha, beta, rng):
    N_blocks = N // B_s
    h = np.empty(N)
    for i in range(N_blocks):
        X = rng.gamma(alpha, 1.0 / alpha)
        Y = rng.gamma(beta, 1.0 / beta)
        h[i * B_s:(i + 1) * B_s] = X * Y
    return h


def find_zoom_range(h, B_s, window=500):
    """Find a window centered on the deepest fade block."""
    N_blocks = len(h) // B_s
    block_vals = [h[i * B_s] for i in range(N_blocks)]
    worst = int(np.argmin(block_vals))
    center = (worst + 0.5) * B_s
    half = window // 2
    start = max(0, int(center - half))
    end = min(len(h), start + window)
    start = max(0, end - window)
    return start, end


def run_tracking(h, N, SNR_lin, rng):
    delta_f = 5e-4
    sigma_pn = 0.008
    theta = delta_f * np.arange(N) + np.cumsum(rng.normal(0, sigma_pn, N))

    s = np.exp(1j * (np.pi / 4 + np.pi / 2 * rng.integers(0, 4, N)))
    n = (rng.standard_normal(N) + 1j * rng.standard_normal(N)) / np.sqrt(2 * SNR_lin)
    r = h * s * np.exp(1j * theta) + n

    # VV (M = 64)
    M = 64
    theta_vv = np.full(N, np.nan)
    for k in range(M - 1, N):
        z4 = r[k - M + 1:k + 1] ** 4
        theta_vv[k] = np.angle(np.mean(z4)) / 4.0

    # DPLL (2nd order)
    zeta = 1.0 / np.sqrt(2)
    wn = 0.02
    K1 = 2 * zeta * wn
    K2 = wn ** 2
    theta_pll = np.zeros(N)
    acc = 0.0
    for k in range(1, N):
        x = r[k] * np.exp(-1j * theta_pll[k - 1])
        s_hat = np.exp(1j * (np.pi / 4 * np.round(np.angle(x) / (np.pi / 4))))
        e = np.angle(x * np.conj(s_hat))
        acc += K2 * e
        theta_pll[k] = theta_pll[k - 1] + K1 * e + acc

    def wrap(e):
        return e - np.round(e / (np.pi / 2)) * (np.pi / 2)

    err_vv = np.abs(wrap(theta_vv - theta))
    err_pll = np.abs(wrap(theta_pll - theta))

    # Running mean for smoother curves
    kernel = np.ones(SMOOTH) / SMOOTH
    err_vv_s = np.convolve(np.nan_to_num(err_vv), kernel, mode='same')
    err_pll_s = np.convolve(err_pll, kernel, mode='same')

    return err_vv_s, err_pll_s


# ── Generate figure ──
fig, axes = plt.subplots(2, 3, figsize=(9.5, 5), sharex=True,
                         gridspec_kw={'height_ratios': [0.6, 1], 'hspace': 0.15})

DEEP = 0.3
ZOOM = 500

for col, (label, alpha, beta) in enumerate(TURB):
    rng = np.random.default_rng(seed=2024 + col)
    h = block_fading_channel(N, B_s, alpha, beta, rng)

    rng2 = np.random.default_rng(seed=3000 + col)
    err_vv, err_pll = run_tracking(h, N, SNR_lin, rng2)

    s, e = find_zoom_range(h, B_s, ZOOM)
    t_zoom = np.arange(s, e)
    h_zoom = h[s:e]
    vv_zoom = err_vv[s:e]
    pll_zoom = err_pll[s:e]

    # Top row: channel gain (zoomed)
    ax_h = axes[0, col]
    ax_h.step(t_zoom, h_zoom, color='#0C5DA5', linewidth=1.0, where='mid')
    for i in range(N // B_s):
        bs, be = i * B_s, (i + 1) * B_s
        if bs >= e or be <= s:
            continue
        if h[bs] < DEEP:
            ax_h.axvspan(max(bs, s), min(be, e), alpha=0.18, color='#FF2C00', zorder=0)
    ax_h.axhline(DEEP, color='#FF2C00', ls='--', lw=0.7, alpha=0.5)
    ax_h.set_ylim(0, 2.5)
    ax_h.set_ylabel('信道增益 $h$' if col == 0 else '')
    ax_h.set_title(label, fontsize=10)
    ax_h.grid(True, alpha=0.3)

    # Bottom row: phase error (zoomed + smoothed)
    ax_e = axes[1, col]
    for i in range(N // B_s):
        bs, be = i * B_s, (i + 1) * B_s
        if bs >= e or be <= s:
            continue
        if h[bs] < DEEP:
            ax_e.axvspan(max(bs, s), min(be, e), alpha=0.10, color='#FF2C00', zorder=0)
    ax_e.plot(t_zoom, vv_zoom, color='#FF2C00', alpha=0.75, lw=1.2, label='VV 前馈')
    ax_e.plot(t_zoom, pll_zoom, color='#0C5DA5', alpha=0.85, lw=1.2, label='DPLL 反馈')
    ax_e.set_ylim(0, 0.5)
    ax_e.set_xlabel('符号索引')
    ax_e.set_ylabel('相位误差 (rad)' if col == 0 else '')
    ax_e.grid(True, alpha=0.3)
    if col == 0:
        ax_e.legend(fontsize=9, loc='upper right')

fig.tight_layout()
out = os.path.join(OUT_DIR, 'phase-tracking-vv-vs-dpll.png')
fig.savefig(out, dpi=300, bbox_inches='tight')
print(f"Saved: {out}")
plt.close(fig)
