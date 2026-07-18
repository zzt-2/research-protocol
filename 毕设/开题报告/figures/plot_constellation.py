#!/usr/bin/env python3
"""Constellation diagram: VV vs DPLL during normal vs deep-fade periods.

2x2 layout:
  Top row:    normal signal  → both methods show clean QPSK
  Bottom row: deep fade      → VV scatters, DPLL stays clean

Uses moderate turbulence (alpha=2.5, beta=1.8) for clear contrast.
Signal is normalized by h so the figure shows phase estimation quality,
not amplitude variation.

Style: SimHei, white bg, light grid, no title, 300 dpi PNG.
Usage: ~/.venvs/torch/bin/python plot_constellation.py
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
N = 10000
B_s = 300
SNR_db = 20
SNR_lin = 10 ** (SNR_db / 10)
M = 64


def block_fading_channel(N, B_s, alpha, beta, rng):
    N_blocks = N // B_s
    h = np.empty(N)
    for i in range(N_blocks):
        X = rng.gamma(alpha, 1.0 / alpha)
        Y = rng.gamma(beta, 1.0 / beta)
        h[i * B_s:(i + 1) * B_s] = X * Y
    return h


def run_tracking(h, N, SNR_lin, rng):
    delta_f = 5e-4
    sigma_pn = 0.008
    theta = delta_f * np.arange(N) + np.cumsum(rng.normal(0, sigma_pn, N))

    s = np.exp(1j * (np.pi / 4 + np.pi / 2 * rng.integers(0, 4, N)))
    n = (rng.standard_normal(N) + 1j * rng.standard_normal(N)) / np.sqrt(2 * SNR_lin)
    r = h * s * np.exp(1j * theta) + n

    # VV (matching common.py: unwrap before divide)
    r4 = r ** 4
    ker = np.ones(M) / M
    avg = np.convolve(r4, ker, mode='same')
    theta_vv = np.unwrap(np.angle(avg)) / 4.0

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

    return theta_vv, theta_pll, r, s


def find_blocks(h, B_s, N_blocks):
    """Find a deep-fade block and a normal block."""
    vals = [h[i * B_s] for i in range(N_blocks)]

    # Deep fade: h in [0.15, 0.4]
    deep_idx = None
    for i in range(N_blocks):
        if 0.15 < vals[i] < 0.4 and i * B_s > M:
            deep_idx = i
            break
    if deep_idx is None:
        dists = [(abs(vals[i] - 0.25), i) for i in range(N_blocks)]
        dists.sort()
        deep_idx = dists[0][1]

    # Normal: h > 0.7, far from deep fade
    normal_idx = None
    for i in range(N_blocks):
        if vals[i] > 0.7 and abs(i - deep_idx) > 2 and i * B_s > M:
            normal_idx = i
            break
    if normal_idx is None:
        normal_idx = max(1, deep_idx - 3)

    return normal_idx, deep_idx, vals[normal_idx], vals[deep_idx]


def align_block_to_qpsk(data):
    """Resolve VV π/2 ambiguity via 4th power: ideal QPSK at π/4 → z4 = -1 (angle π)."""
    valid = data[~np.isnan(data)]
    if len(valid) < 10:
        return data
    mean_z4 = np.mean(valid ** 4)
    rotation = (np.pi - np.angle(mean_z4)) / 4
    return data * np.exp(1j * rotation)


# ── Search for a good seed ──
best_seed = None
best_h = float('inf')
for seed in range(2024, 3000):
    rng = np.random.default_rng(seed)
    h_test = block_fading_channel(N, B_s, 2.5, 1.8, rng)
    vals = [h_test[i * B_s] for i in range(N // B_s)]
    for i, v in enumerate(vals):
        if 0.15 < v < 0.35 and i * B_s > M + B_s:
            if v < best_h:
                best_h = v
                best_seed = seed
            break

if best_seed is None:
    best_seed = 2024

print(f"Using seed={best_seed}")

# ── Generate data ──
rng1 = np.random.default_rng(seed=best_seed)
h = block_fading_channel(N, B_s, 2.5, 1.8, rng1)

rng2 = np.random.default_rng(seed=3000)
theta_vv, theta_pll, r, s = run_tracking(h, N, SNR_lin, rng2)

N_blocks = N // B_s
normal_idx, deep_idx, h_normal, h_deep = find_blocks(h, B_s, N_blocks)
print(f"Normal block: #{normal_idx}, h={h_normal:.3f}")
print(f"Deep block:   #{deep_idx}, h={h_deep:.3f}")

# Compensated + normalized by h
comp_vv_raw = r * np.exp(-1j * theta_vv) / h
comp_pll = r * np.exp(-1j * theta_pll) / h

# Slices
normal_sl = slice(normal_idx * B_s, (normal_idx + 1) * B_s)
deep_sl = slice(deep_idx * B_s, (deep_idx + 1) * B_s)

# Align VV blocks
comp_vv = comp_vv_raw.copy()
comp_vv[normal_sl] = align_block_to_qpsk(comp_vv_raw[normal_sl])
comp_vv[deep_sl] = align_block_to_qpsk(comp_vv_raw[deep_sl])

# ── Plot ──
fig, axes = plt.subplots(2, 2, figsize=(7, 7),
                         gridspec_kw={'hspace': 0.45, 'wspace': 0.35})

configs = [
    (0, 0, comp_vv[normal_sl],  'VV 前馈 — 正常信号'),
    (0, 1, comp_pll[normal_sl], 'DPLL 反馈 — 正常信号'),
    (1, 0, comp_vv[deep_sl],    'VV 前馈 — 深衰落'),
    (1, 1, comp_pll[deep_sl],   'DPLL 反馈 — 深衰落'),
]

for row, col, data, title in configs:
    ax = axes[row, col]
    valid = ~np.isnan(data)
    d = data[valid]
    ax.scatter(d.real, d.imag, s=3, alpha=0.5,
               c='#0C5DA5', edgecolors='none', zorder=2)

    ax.set_xlim(-2.0, 2.0)
    ax.set_ylim(-2.0, 2.0)
    ax.set_aspect('equal')
    ax.set_xlabel('$I$')
    ax.set_ylabel('$Q$' if col == 0 else '')
    ax.set_title(title, fontsize=10)
    ax.grid(True, alpha=0.25)
    ax.axhline(0, color='gray', lw=0.5, alpha=0.3)
    ax.axvline(0, color='gray', lw=0.5, alpha=0.3)

fig.tight_layout()
out = os.path.join(OUT_DIR, 'constellation-vv-vs-dpll.png')
fig.savefig(out, dpi=300, bbox_inches='tight')
print(f"Saved: {out}")
plt.close(fig)
