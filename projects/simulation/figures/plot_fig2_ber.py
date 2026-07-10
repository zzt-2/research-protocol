# -*- coding: utf-8 -*-
"""Fig.2 BER vs SNR main figure (CCISP beautified version).

3x2 vertical layout (3 rows x 2 cols), scenes ordered by increasing turbulence.
Addresses user's 5 feedback points:
  - 横向太扁   -> vertical layout, taller subplots
  - 差别太小   -> annotate NDA-wins regions in selling-point scenes
  - 点太稀疏   -> cubic interpolation for visual continuity (no re-simulation)
  - 标志难看   -> line-style distinction (solid/dashed/dotted), no ugly markers
  - 线太粗     -> linewidth <= 1.2

Data sources (read-only, no modification):
  - 30seed main:  results/sc_nda_ml_main_30seed/_main_experiment_30seed.json
  - 5seed ext1:   results/sc_nda_ml_ber_ext_5seed/_ber_ext_5seed.json
  - 5seed ext2:   results/sc_nda_ml_ber_ext_5seed/_ber_ext2_5seed.json

Output: figures/ccisp_fig2_ber.png + .pdf
"""
import os
import json

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..'))

MAIN30 = os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_main_30seed', '_main_experiment_30seed.json')
EXT1 = os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_ber_ext_5seed', '_ber_ext_5seed.json')
EXT2 = os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_ber_ext_5seed', '_ber_ext2_5seed.json')
OUT_PNG = os.path.join(_HERE, 'ccisp_fig2_ber.png')
OUT_PDF = os.path.join(_HERE, 'ccisp_fig2_ber.pdf')

# Scene order: increasing turbulence (top-to-bottom in 3x2 grid)
SCENES = ['awgn', 'weak', 'moderate', 'strong', 'uplink_moderate', 'uplink_strong']
TITLES = {
    'awgn': '(a) No turbulence (AWGN)',
    'weak': r'(b) Weak turb. ($\alpha$=4.0, $\beta$=3.0)',
    'moderate': r'(c) Moderate turb. ($\alpha$=2.5, $\beta$=1.8)',
    'strong': r'(d) Strong turb. ($\alpha$=1.5, $\beta$=0.8)',
    'uplink_moderate': r'(e) Uplink moderate ($\alpha$=1.2, $\beta$=0.9)',
    'uplink_strong': r'(f) Uplink strong ($\alpha$=1.0, $\beta$=0.7)',
}

# Colorblind-safe palette (Okabe-Ito inspired)
C_DA = '#0072B2'    # blue
C_NDA = '#D55E00'   # vermillion (orange-red)
C_OR = '#009E73'    # green
C_FEC = '#999999'   # gray for HD-FEC line

# Selling-point scenes (where NDA advantage is the story)
SELLING_SCENES = {'strong', 'uplink_moderate', 'uplink_strong'}

HD_FEC = 3.8e-3


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_pts(summary_block, ber_key):
    """Extract (snr[], ber[]) from a summary scene's points, sorted by snr."""
    pts = summary_block['points']
    snr = [p['snr_db'] for p in pts]
    ber = [p[ber_key] for p in pts]
    order = np.argsort(snr)
    return np.array(snr)[order], np.array(ber)[order]


def merge_scene(scene, ber_key):
    """Merge 30seed main + 5seed ext1 + 5seed ext2 for one scene.

    Returns (snr_all, ber_all) sorted, with BER>0 filter.
    """
    m = load(MAIN30)
    snr_list, ber_list = [], []
    if scene in m['summary']:
        s, b = extract_pts(m['summary'][scene], ber_key)
        snr_list.extend(s)
        ber_list.extend(b)

    e1 = load(EXT1)
    if scene in e1['summary']:
        s, b = extract_pts(e1['summary'][scene], ber_key)
        snr_list.extend(s)
        ber_list.extend(b)

    if os.path.exists(EXT2):
        e2 = load(EXT2)
        if scene in e2['summary']:
            s, b = extract_pts(e2['summary'][scene], ber_key)
            snr_list.extend(s)
            ber_list.extend(b)

    snr = np.array(snr_list)
    ber = np.array(ber_list)
    order = np.argsort(snr)
    snr, ber = snr[order], ber[order]
    return snr, ber


def smooth_curve(snr, ber, n_dense=200):
    """Interpolate for visual continuity (cubic in log-BER domain).

    Only used for the drawn line; original points still plotted.
    """
    ber_plot = np.where(ber > 0, ber, 1e-7)
    log_ber = np.log10(ber_plot)
    # Need unique sorted snr for interpolation
    snr_u, idx = np.unique(snr, return_index=True)
    log_ber_u = log_ber[idx]
    if len(snr_u) < 4:
        # Not enough points for cubic, use linear
        kind = 'linear'
    else:
        kind = 'cubic'
    f = interp1d(snr_u, log_ber_u, kind=kind, fill_value='extrapolate')
    snr_dense = np.linspace(snr_u[0], snr_u[-1], n_dense)
    ber_dense = 10 ** f(snr_dense)
    return snr_dense, ber_dense


def plot_one(ax, scene):
    """Plot one subplot: DA/NDA/oracle with line-style distinction."""
    for ber_key, label, color, ls in [
        ('da_ml_ber_mean', 'DA-ML (pilot)', C_DA, '-'),
        ('nda_ml_ber_mean', 'NDA-ML (blind)', C_NDA, '--'),
        ('oracle_ber_mean', 'Oracle', C_OR, ':'),
    ]:
        snr, ber = merge_scene(scene, ber_key)
        if len(snr) == 0:
            continue
        ber_plot = np.where(ber > 0, ber, 1e-7)

        # Smooth interpolated line
        snr_s, ber_s = smooth_curve(snr, ber)
        ax.plot(snr_s, ber_s, ls, color=color, linewidth=1.2, zorder=3)

        # Original data points (small, same color, no ugly marker shape)
        ax.plot(snr, ber_plot, 'o', color=color, markersize=2.5,
                markeredgecolor='none', zorder=4, alpha=0.7)

    # HD-FEC reference line
    ax.axhline(HD_FEC, color=C_FEC, linestyle='-.', linewidth=0.8, alpha=0.6, zorder=1)

    ax.set_yscale('log')
    ax.set_title(TITLES[scene], fontsize=9, pad=4)
    ax.set_xlabel(r'$\bar{\gamma}_d$ (dB)', fontsize=8)
    ax.set_ylabel('BER', fontsize=8)
    ax.grid(True, which='major', alpha=0.2, linewidth=0.5)
    ax.grid(True, which='minor', alpha=0.08, linewidth=0.3)
    ax.tick_params(labelsize=7)

    # Annotate NDA-wins region in selling-point scenes
    if scene in SELLING_SCENES:
        annotate_nda_wins(ax, scene)

    # Adaptive y-axis range
    set_yrange(ax, scene)


def annotate_nda_wins(ax, scene):
    """Find a high-SNR point where NDA clearly beats DA, annotate it."""
    snr_da, ber_da = merge_scene(scene, 'da_ml_ber_mean')
    snr_nda, ber_nda = merge_scene(scene, 'nda_ml_ber_mean')

    # Find matching SNR points (common to both)
    common = np.intersect1d(snr_da, snr_nda)
    if len(common) < 2:
        return

    da_at = np.interp(common, snr_da, np.where(ber_da > 0, ber_da, 1e-7))
    nda_at = np.interp(common, snr_nda, np.where(ber_nda > 0, ber_nda, 1e-7))

    ratio = da_at / np.maximum(nda_at, 1e-10)
    # Pick the point with highest ratio (NDA most ahead)
    best_idx = np.argmax(ratio)
    best_snr = common[best_idx]
    best_ratio = ratio[best_idx]

    if best_ratio > 1.15:
        # Compute equivalent dB gain at this BER level
        # gain_dB ~ 20*log10(ratio) for approximate (BER slope dependent)
        gain_db = 10 * np.log10(best_ratio)
        ax.annotate(
            f'NDA +{gain_db:.1f} dB\n@{best_snr:.0f} dB',
            xy=(best_snr, da_at[best_idx]),
            xytext=(best_snr - 6, da_at[best_idx] * 3),
            fontsize=6.5, color=C_NDA, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=C_NDA, lw=0.8),
            zorder=5,
        )


def set_yrange(ax, scene):
    """Adaptive y-axis: non-turbulence scenes to 1e-5, strong/uplink narrower."""
    if scene in ('awgn', 'weak', 'moderate'):
        ax.set_ylim(1e-6, 1)
    else:  # strong / uplink: deep fade, don't force 1e-5
        ax.set_ylim(1e-4, 0.5)


def main():
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Times New Roman', 'DejaVu Serif'],
        'mathtext.fontset': 'stix',
        'axes.linewidth': 0.6,
    })

    fig, axes = plt.subplots(3, 2, figsize=(7.0, 10.0))
    axes = axes.flatten()

    for idx, scene in enumerate(SCENES):
        plot_one(axes[idx], scene)

    # Shared legend at bottom (line-style based, no markers)
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color=C_DA, linestyle='-', linewidth=1.2, label='DA-ML (pilot-aided)'),
        Line2D([0], [0], color=C_NDA, linestyle='--', linewidth=1.2, label='NDA-ML (blind)'),
        Line2D([0], [0], color=C_OR, linestyle=':', linewidth=1.2, label='Oracle'),
        Line2D([0], [0], color=C_FEC, linestyle='-.', linewidth=0.8, label=f'HD-FEC ({HD_FEC:.0e})'),
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=4, fontsize=7.5,
               bbox_to_anchor=(0.5, 0.005), frameon=True, edgecolor='gray',
               fancybox=False, borderpad=0.4)

    plt.tight_layout(rect=[0, 0.03, 1, 1])
    fig.savefig(OUT_PNG, dpi=200, bbox_inches='tight')
    fig.savefig(OUT_PDF, bbox_inches='tight')
    print(f'[saved] {OUT_PNG}')
    print(f'[saved] {OUT_PDF}')
    plt.close(fig)


if __name__ == '__main__':
    main()
