# -*- coding: utf-8 -*-
"""Fig 2 v2: 照 A 篇 Fig7 画法重画 strong 场景单图 (3 线, 纵轴聚焦, 线细 marker 小).

对比 v1 的 4 子图横排, 这版单图聚焦, 让 deep fade 故事 (NDA 贴 oracle, DA 退化) 可见.

Usage:
    cd /d/code/study/research-protocol
    python projects/simulation/experiments/plot_fig2_v2_single.py
"""
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

_SIM_ROOT = Path(__file__).resolve().parents[1]
DATA = _SIM_ROOT / 'results' / 'sc_nda_ml_main_30seed' / '_main_experiment_30seed.json'
FIG_DIR = _SIM_ROOT / 'figures'
OUT_PNG = FIG_DIR / 'fig2_v2_strong_single.png'

# 字体: 学术 clean 风 (对标 A 篇)
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 11,
    'axes.labelsize': 12,
    'legend.fontsize': 10,
    'axes.linewidth': 0.8,
    'axes.grid': True,
    'grid.alpha': 0.2,
    'grid.linestyle': ':',
})

COLORS = {'da': '#D55E00', 'nda': '#0072B2', 'oracle': '#009E73'}
MARKERS = {'da': 's', 'nda': 'o', 'oracle': '^'}
LABELS = {
    'da': 'DA-ML (pilot-aided)',
    'nda': 'NDA-ML (blind, proposed)',
    'oracle': 'Oracle bound',
}
HD_FEC = 3.8e-3


def extract(data, scene):
    pts = data['summary'][scene]['points']
    snrs = np.array([p['snr_db'] for p in pts])
    out = {}
    for m in ('da', 'nda', 'oracle'):
        key = f'{m}_ml_ber_mean' if m != 'oracle' else 'oracle_ber_mean'
        ci_key = f'{m}_ml_ber_ci95' if m != 'oracle' else 'oracle_ber_ci95'
        mean = np.array([p[key] for p in pts])
        ci = np.array([p[ci_key] for p in pts])
        out[m] = (mean, ci[:, 0], ci[:, 1])
    return snrs, out


def plot():
    data = json.load(open(DATA, encoding='utf-8'))

    # === 单图, strong 场景, 纵轴聚焦工作区 ===
    fig, ax = plt.subplots(figsize=(5, 4))  # 单栏尺寸, 接近正方形 (对标 A 篇单栏)

    snrs, methods = extract(data, 'strong')

    # oracle 底层 (细虚线, 作参考界), DA/NDA 主线
    for m in ('oracle', 'da', 'nda'):
        mean, lo, hi = methods[m]
        if m == 'oracle':
            # oracle 画细虚线 + 空心 marker, 不抢主角
            ax.semilogy(snrs, mean, color=COLORS[m], marker=MARKERS[m],
                        markersize=4, markerfacecolor='white', markeredgewidth=1.2,
                        linestyle='--', linewidth=1.0, label=LABELS[m])
        else:
            # DA/NDA 主线: 线细 (1.2), marker 小 (4), 实心
            ax.semilogy(snrs, mean, color=COLORS[m], marker=MARKERS[m],
                        markersize=4.5, linewidth=1.2, label=LABELS[m])

    # HD-FEC 门限线
    ax.axhline(HD_FEC, color='gray', ls=':', lw=0.8)
    ax.text(26, HD_FEC * 0.55, 'HD-FEC 3.8e-3', fontsize=8, ha='right', va='top', color='gray')

    # 纵轴聚焦: strong 场景 BER 范围 2e-2 ~ 4e-1, 收到工作区
    ax.set_ylim(1e-2, 0.5)
    ax.set_xlim(4, 27)

    ax.set_xlabel(r'Received $\gamma_d$ (dB)')
    ax.set_ylabel('BER')
    ax.set_title('Strong turbulence ($\\alpha=1.5,\\beta=0.8$)', fontsize=11)
    ax.legend(loc='upper right', framealpha=0.95, edgecolor='0.8')

    # 标注 deep fade 证据: 在高 SNR 区 (20-26dB), NDA 比 DA 更贴近 oracle
    # 用箭头指示 "NDA closer to oracle"
    ax.annotate('', xy=(25, methods['nda'][0][-1]),
                xytext=(25, methods['oracle'][0][-1]),
                arrowprops=dict(arrowstyle='<->', color='green', lw=0.8, alpha=0.6))
    ax.text(25.3, (methods['nda'][0][-1] + methods['oracle'][0][-1]) / 2,
            'NDA\n→ oracle', fontsize=7, color='green', va='center')

    fig.tight_layout()
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PNG, dpi=200, bbox_inches='tight')
    print(f'[saved] {OUT_PNG}')


if __name__ == '__main__':
    plot()
