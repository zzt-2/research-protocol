#!/usr/bin/env python3
"""Generate 3 Chinese-labeled figures for the kaiti (proposal) report.

Style: SimHei Chinese font, white background, light grid, no titles.
Output: PNG only, Chinese filenames.

Fig 1: NMSE灵敏度曲线 — QPSK vs 16-QAM
Fig 2: 载波同步方法对比热力图 — VV/DPLL
Fig 3: DPLL环路自然频率设计曲线

Usage: ~/.venvs/torch/bin/python plot_kaiti_figures.py
"""

import json, os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
from matplotlib.colors import Normalize

# ── Chinese font: SimHei from Windows Fonts ──
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

FIG_DIR = os.path.dirname(os.path.abspath(__file__))


def load_json(path):
    with open(path) as f:
        return json.load(f)


# ======================================================================
# Figure 1: NMSE Sensitivity (single panel, moderate turbulence)
# ======================================================================

def plot_nmse_sensitivity():
    print("Generating: NMSE灵敏度曲线 ...")

    data = load_json(os.path.join(FIG_DIR, 'nmse_50seed.json'))

    nmse_keys = sorted(data['qpsk'].keys(), key=lambda x: float(x), reverse=True)
    valid_nmse = [float(k) for k in nmse_keys]
    valid_qpsk = [max(data['qpsk'][k]['ber_mean'], 1e-6) for k in nmse_keys]
    valid_qam16 = [max(data['qam16'][k]['ber_mean'], 1e-6) for k in nmse_keys]

    fig, ax = plt.subplots(figsize=(4.5, 3.2))

    ax.semilogy(valid_nmse, valid_qpsk, marker='o', color='#0C5DA5',
                label='QPSK (DPLL)', linewidth=1.5, markersize=5, zorder=3)
    ax.semilogy(valid_nmse, valid_qam16, marker='s', color='#FF2C00',
                label='16-QAM (DD-DPLL)', linewidth=1.5, markersize=5, zorder=3)

    ax.set_xlabel('信道估计 NMSE/dB')
    ax.set_ylabel('误码率')
    ax.set_ylim(bottom=1e-5, top=2)
    ax.set_yticks([1e-4, 1e-3, 1e-2, 1e-1, 1e0])
    ax.set_yticklabels([r'$10^{-4}$', r'$10^{-3}$', r'$10^{-2}$', r'$10^{-1}$', r'$10^{0}$'])
    ax.set_xlim(left=1, right=-22)
    ax.legend(fontsize=9, loc='upper left')
    ax.grid(True, alpha=0.3, which='both')

    # Highlight the contrast with shaded region
    ax.fill_between(valid_nmse, valid_qpsk, valid_qam16,
                    alpha=0.08, color='gray', zorder=1)
    # Annotate the gap at NMSE=0
    if valid_qam16[-1] / valid_qpsk[-1] > 10:
        ax.annotate('',
                    xy=(-1, valid_qam16[-1] * 1.3),
                    xytext=(-1, valid_qpsk[-1] * 0.7),
                    arrowprops=dict(arrowstyle='<->', color='#555555', lw=0.8))
        ratio = valid_qam16[-1] / valid_qpsk[-1]
        ax.text(1, np.sqrt(valid_qpsk[-1] * valid_qam16[-1]),
                f'{ratio:.0f}倍\n差距', fontsize=8,
                ha='left', va='center', color='#555555')

    fig.tight_layout()
    out = os.path.join(FIG_DIR, 'NMSE灵敏度曲线.png')
    fig.savefig(out, dpi=300, bbox_inches='tight')
    print(f"  Saved: {out}")
    plt.close(fig)


# ======================================================================
# Figure 2: Method Applicability — parameter design matters
# ======================================================================

def plot_method_heatmap():
    print("Generating: 方法对比热力图 ...")

    data = load_json(os.path.join(FIG_DIR, 'method_matrix_50seed.json'))

    methods = [
        'VV ($N_w$=64)\n(默认参数)',
        'VV ($N_w$=256)\n(优化参数)',
        'DPLL ($\\omega_n$=20 MHz)',
    ]
    turb_cols = ['弱湍流\n($\\alpha$=4.0)', '中等湍流\n($\\alpha$=2.5)', '强湍流\n($\\alpha$=1.5)']
    method_keys = ['vv64', 'vv256', 'dpll20m']
    turb_keys = ['weak', 'moderate', 'strong']

    ber_matrix = np.array([
        [data['results'][m][t]['ber_mean'] for t in turb_keys]
        for m in method_keys
    ])

    log_ber = np.log10(ber_matrix)

    fig, ax = plt.subplots(figsize=(5.5, 3.5))

    cmap = plt.cm.RdYlGn_r
    norm = Normalize(vmin=-4, vmax=0)

    im = ax.imshow(log_ber, cmap=cmap, norm=norm, aspect='auto')

    for i in range(len(methods)):
        for j in range(len(turb_cols)):
            val = ber_matrix[i, j]
            log_val = log_ber[i, j]

            if val >= 0.1:
                rect = plt.Rectangle((j - 0.5, i - 0.5), 1, 1,
                                     facecolor='#8B0000', edgecolor='white', linewidth=0.5)
                ax.add_patch(rect)
                ax.text(j, i, f'失败\n({val:.0%})',
                        ha='center', va='center', fontsize=7,
                        color='white', fontweight='bold')
            else:
                text_color = 'black' if log_val > -2 else 'white'
                if val < 1e-3:
                    label = f'{val:.1e}'
                elif val < 1e-2:
                    label = f'{val:.2%}'
                else:
                    label = f'{val:.1%}'
                ax.text(j, i, label, ha='center', va='center',
                        fontsize=7.5, color=text_color, fontweight='bold')

    ax.set_xticks(range(len(turb_cols)))
    ax.set_xticklabels(turb_cols, fontsize=9)
    ax.set_yticks(range(len(methods)))
    ax.set_yticklabels(methods, fontsize=9)

    cbar = fig.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
    cbar.set_label('误码率', fontsize=10)
    cbar.set_ticks([-4, -3, -2, -1, 0])
    cbar.set_ticklabels([r'$10^{-4}$', r'$10^{-3}$', r'$10^{-2}$', r'$10^{-1}$', r'$10^{0}$'])

    # Dynamic improvement ratio annotation (moderate column: vv64 vs vv256)
    improv_ratio = ber_matrix[0, 1] / ber_matrix[1, 1]
    ax.annotate('',
                xy=(1, 1.35), xytext=(1, 0.65),
                arrowprops=dict(arrowstyle='<->', color='#00B945', lw=1.5))
    ax.text(1.55, 1.0, f'{improv_ratio:.0f}倍\n改善',
            fontsize=7, ha='left', va='center', color='#00B945',
            fontweight='bold')

    fig.tight_layout()
    out = os.path.join(FIG_DIR, '方法对比热力图.png')
    fig.savefig(out, dpi=300, bbox_inches='tight')
    print(f"  Saved: {out}")
    plt.close(fig)


# ======================================================================
# Figure 3: DPLL omega_n Design Curves (with selected-point marker)
# ======================================================================

def plot_dpll_design():
    print("Generating: DPLL设计曲线 ...")

    data = load_json(os.path.join(FIG_DIR, 'dpll_omega_50seed.json'))

    omega_keys = sorted(data['results'].keys(), key=lambda x: int(x))
    omega_mhz = [int(k) for k in omega_keys]
    turb_keys = ['weak', 'moderate', 'strong']
    turb_labels = ['弱湍流', '中等湍流', '强湍流']
    turb_markers = {'weak': 'o', 'moderate': 's', 'strong': '^'}
    turb_colors = {'weak': '#0C5DA5', 'moderate': '#FF2C00', 'strong': '#00B945'}

    fig, ax = plt.subplots(figsize=(5, 3.5))

    for turb, label in zip(turb_keys, turb_labels):
        bers = [max(data['results'][k][turb]['ber_mean'], 1e-6) for k in omega_keys]
        ax.semilogy(omega_mhz, bers, marker=turb_markers[turb],
                    color=turb_colors[turb], label=label,
                    linewidth=1.2, markersize=5)

    # Vertical line at selected design point ωn=20MHz
    ax.axvline(x=20, color='#333333', linestyle='--', linewidth=0.8, alpha=0.7)
    ax.text(20, 3e-4, '$\\omega_n$ = 20 MHz\n(选定值)', fontsize=7,
            ha='center', va='bottom', color='#333333',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor='#999999', alpha=0.8))

    ax.set_xlabel(r'$\omega_n$/MHz')
    ax.set_ylabel('误码率')
    ax.set_xscale('log')
    ax.set_yticks([1e-4, 1e-3, 1e-2, 1e-1])
    ax.set_yticklabels([r'$10^{-4}$', r'$10^{-3}$', r'$10^{-2}$', r'$10^{-1}$'])
    ax.legend(fontsize=9, loc='best')
    ax.grid(True, alpha=0.3, which='both')
    ax.set_xlim(left=1, right=150)
    ax.set_ylim(bottom=1e-5, top=5e-1)

    fig.tight_layout()
    out = os.path.join(FIG_DIR, 'DPLL设计曲线.png')
    fig.savefig(out, dpi=300, bbox_inches='tight')
    print(f"  Saved: {out}")
    plt.close(fig)


# ======================================================================
# Main
# ======================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("开题报告插图 — 中文风格 (v3: SimHei, 白底, 无标题)")
    print("=" * 60)

    nmse_50 = os.path.exists(os.path.join(FIG_DIR, 'nmse_50seed.json'))
    matrix_50 = os.path.exists(os.path.join(FIG_DIR, 'method_matrix_50seed.json'))
    omega_50 = os.path.exists(os.path.join(FIG_DIR, 'dpll_omega_50seed.json'))
    print(f"  nmse_50seed.json: {'OK' if nmse_50 else 'MISSING'}")
    print(f"  method_matrix_50seed.json: {'OK' if matrix_50 else 'MISSING'}")
    print(f"  dpll_omega_50seed.json: {'OK' if omega_50 else 'MISSING'}")
    if not (nmse_50 and matrix_50 and omega_50):
        print("ERROR: Missing data files. Run simulation scripts first.")
        sys.exit(1)
    print()

    plot_nmse_sensitivity()
    print()
    plot_method_heatmap()
    print()
    plot_dpll_design()

    print("\n" + "=" * 60)
    print("All figures generated.")
    print("=" * 60)
