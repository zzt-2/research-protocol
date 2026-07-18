# -*- coding: utf-8 -*-
"""Fig 2 (main): BER vs SNR, 4 subplots (awgn/weak/moderate/strong).

每个子图 DA-ML / NDA-ML / oracle 三线, 30 seed 95% CI 带.
对标 Wang2024 Fig15-17 (多子图分组 + FEC 线). 全英文 (CCISP 直接用).

Usage:
    cd /d/code/study/research-protocol
    python projects/simulation/experiments/plot_fig2_ber_curves.py
"""
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Paths — 脚本在 experiments/, 数据在 results/, 图输出到 figures/ (分离原则)
# ---------------------------------------------------------------------------
_SIM_ROOT = Path(__file__).resolve().parents[1]  # projects/simulation/
DATA = _SIM_ROOT / 'results' / 'sc_nda_ml_main_30seed' / '_main_experiment_30seed.json'
FIG_DIR = _SIM_ROOT / 'figures'
OUT_PNG = FIG_DIR / 'fig2_ber_curves.png'
OUT_PDF = FIG_DIR / 'fig2_ber_curves.pdf'

# ---------------------------------------------------------------------------
# Style — 论文级默认 (用户本地微调配色/字号/线宽)
# ---------------------------------------------------------------------------
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 9,
    'axes.labelsize': 10,
    'axes.titlesize': 10,
    'legend.fontsize': 8,
    'xtick.labelsize': 8.5,
    'ytick.labelsize': 8.5,
    'axes.grid': True,
    'grid.alpha': 0.25,
    'grid.linestyle': '--',
    'lines.linewidth': 1.8,
    'savefig.dpi': 300,
})

# 方法配色 (色盲友好近似)
COLORS = {
    'da': '#D55E00',      # 橙红 — pilot-aided (主 baseline)
    'nda': '#0072B2',     # 蓝 — blind (主卖点)
    'oracle': '#009E73',  # 绿 — 上界
}
MARKERS = {'da': 's', 'nda': 'o', 'oracle': '^'}
LABELS = {
    'da': 'DA-ML (pilot-aided)',
    'nda': 'NDA-ML (blind, proposed)',
    'oracle': 'Oracle (lower bound)',
}
# 场景配置: (显示名, α/β 副标签) — 不标 σ²R (实证后非阻塞, 用 GG α/β 标注)
SCENES = [
    ('awgn',     '(a) AWGN\n(no turbulence)',       '—'),
    ('weak',     '(b) Weak turbulence',             r'$\alpha=4.0,\beta=3.0$'),
    ('moderate', '(c) Moderate turbulence',         r'$\alpha=2.5,\beta=1.8$'),
    ('strong',   '(d) Strong turbulence',           r'$\alpha=1.5,\beta=0.8$'),
]
HD_FEC = 3.8e-3  # HD-FEC 门限 (5/5 论文硬性画法)
BER_FLOOR = 1e-5  # log 轴下限


def load():
    with open(DATA, encoding='utf-8') as f:
        return json.load(f)


def extract(data, scene):
    """返回 (snrs, {method: (ber_mean, ci_lo, ci_hi)}) per scene."""
    pts = data['summary'][scene]['points']
    snrs = np.array([p['snr_db'] for p in pts])
    out = {}
    for m in ('da', 'nda', 'oracle'):
        key = f'{m}_ml_ber_mean' if m != 'oracle' else 'oracle_ber_mean'
        ci_key = f'{m}_ml_ber_ci95' if m != 'oracle' else 'oracle_ber_ci95'
        mean = np.array([p[key] for p in pts])
        ci = np.array([p[ci_key] for p in pts])  # shape (n,2)
        out[m] = (mean, ci[:, 0], ci[:, 1])
    return snrs, out


def plot():
    data = load()
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.2), sharey=True)

    for ax, (sc, title, sublabel) in zip(axes, SCENES):
        snrs, methods = extract(data, sc)

        for m in ('oracle', 'da', 'nda'):  # oracle 先画 (底层), da/nda 叠上
            mean, lo, hi = methods[m]
            mean = np.maximum(mean, BER_FLOOR)
            lo = np.maximum(lo, BER_FLOOR)
            hi = np.maximum(hi, BER_FLOOR)
            ax.semilogy(snrs, mean, color=COLORS[m], marker=MARKERS[m],
                        markersize=4.5, label=LABELS[m])
            ax.fill_between(snrs, lo, hi, color=COLORS[m], alpha=0.15)

        # HD-FEC 门限线 (硬性画法)
        ax.axhline(HD_FEC, color='k', ls=':', lw=1.0)
        # 只在第一个子图标 HD-FEC 文字 (避免重复)
        if sc == 'awgn':
            ax.text(snrs[-1], HD_FEC * 0.5, 'HD-FEC\n3.8e-3',
                    fontsize=6.5, ha='right', va='top', color='k')

        ax.set_title(title, fontsize=9)
        ax.set_xlabel(r'Received $\gamma_d$ (dB)')
        ax.set_xlim(snrs[0] - 0.5, snrs[-1] + 0.5)
        ax.set_ylim(BER_FLOOR, 0.6)
        # α/β 副标签 (右下角小字, 不标 σ²R)
        if sublabel != '—':
            ax.text(0.97, 0.97, sublabel, transform=ax.transAxes,
                    fontsize=7, ha='right', va='top', color='gray',
                    bbox=dict(boxstyle='round,pad=0.2', fc='white',
                              ec='gray', alpha=0.7))

    axes[0].set_ylabel('BER')
    # 单一图例 (第一个子图)
    axes[0].legend(loc='lower left', fontsize=7, framealpha=0.9)

    fig.tight_layout(w_pad=0.5)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PNG, bbox_inches='tight')
    fig.savefig(OUT_PDF, bbox_inches='tight')
    print(f'[saved] {OUT_PNG}')
    print(f'[saved] {OUT_PDF}')


if __name__ == '__main__':
    plot()
