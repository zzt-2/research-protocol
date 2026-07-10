# -*- coding: utf-8 -*-
"""Fig.4 Crossover mechanism figure (CCISP beautified version).

Shows why estimator switching has physical basis: DA-ML wins at low SNR
(pilot robust), NDA-ML wins at high SNR (integration gain), crossover exists.

Data source: BER curves (NOT switch JSON, to avoid the 口径 mismatch where
switch_vs_NDA peak gains are actually in weak/moderate, not strong).
The crossover is visible in BER data: NDA da/nda ratio crosses 1.0 ~15dB.

Layout: 1 representative scene (strong) showing DA vs NDA BER curves
+ crossover annotation + optional switched curve.

Data sources (read-only):
  30seed main + 5seed ext (same as Fig.2)

Output: figures/ccisp_fig4_crossover.png + .pdf
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
OUT_PNG = os.path.join(_HERE, 'ccisp_fig4_crossover.png')
OUT_PDF = os.path.join(_HERE, 'ccisp_fig4_crossover.pdf')

C_DA = '#0072B2'
C_NDA = '#D55E00'
C_SW = '#009E73'
C_FEC = '#999999'
HD_FEC = 3.8e-3


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_pts(summary_block, ber_key):
    pts = summary_block['points']
    snr = [p['snr_db'] for p in pts]
    ber = [p[ber_key] for p in pts]
    order = np.argsort(snr)
    return np.array(snr)[order], np.array(ber)[order]


def merge_scene(scene, ber_key):
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
    return snr[order], ber[order]


def smooth_log(snr, ber, n_dense=300):
    """Cubic interpolation in log-BER domain for smooth curves."""
    ber_plot = np.where(ber > 0, ber, 1e-7)
    log_ber = np.log10(ber_plot)
    snr_u, idx = np.unique(snr, return_index=True)
    log_ber_u = log_ber[idx]
    kind = 'cubic' if len(snr_u) >= 4 else 'linear'
    f = interp1d(snr_u, log_ber_u, kind=kind, fill_value='extrapolate')
    snr_dense = np.linspace(snr_u[0], snr_u[-1], n_dense)
    return snr_dense, 10 ** f(snr_dense)


def find_crossover(snr_da, ber_da, snr_nda, ber_nda):
    """Find SNR where NDA crosses below DA (NDA starts winning).

    Returns crossover_snr or None. Uses dense interpolation of ratio.
    """
    # Build dense interpolated curves
    sd, bd = smooth_log(snr_da, ber_da, n_dense=500)
    sn, bn = smooth_log(snr_nda, ber_nda, n_dense=500)
    # Interpolate both to common grid
    snr_min = max(sd[0], sn[0])
    snr_max = min(sd[-1], sn[-1])
    grid = np.linspace(snr_min, snr_max, 500)
    da_grid = 10 ** np.interp(grid, sd, np.log10(np.maximum(bd, 1e-10)))
    nda_grid = 10 ** np.interp(grid, sn, np.log10(np.maximum(bn, 1e-10)))
    ratio = da_grid / np.maximum(nda_grid, 1e-12)
    # Find where ratio crosses 1.0 from below (NDA starts winning)
    above = ratio > 1.0
    crossings = []
    for i in range(1, len(above)):
        if not above[i - 1] and above[i]:
            crossings.append(grid[i])
    return crossings[0] if crossings else None


def main():
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Times New Roman', 'DejaVu Serif'],
        'mathtext.fontset': 'stix',
        'axes.linewidth': 0.6,
    })

    fig, ax = plt.subplots(figsize=(6.5, 4.5))

    scene = 'strong'
    snr_da, ber_da = merge_scene(scene, 'da_ml_ber_mean')
    snr_nda, ber_nda = merge_scene(scene, 'nda_ml_ber_mean')

    # Smooth curves
    sd, bd = smooth_log(snr_da, ber_da)
    sn, bn = smooth_log(snr_nda, ber_nda)

    ber_da_plot = np.where(ber_da > 0, ber_da, 1e-7)
    ber_nda_plot = np.where(ber_nda > 0, ber_nda, 1e-7)

    # Plot DA and NDA
    ax.plot(sd, bd, '-', color=C_DA, linewidth=1.3, label='DA-ML (pilot-aided)', zorder=3)
    ax.plot(sn, bn, '--', color=C_NDA, linewidth=1.3, label='NDA-ML (blind)', zorder=3)
    ax.plot(snr_da, ber_da_plot, 'o', color=C_DA, markersize=2.5, alpha=0.7, zorder=4)
    ax.plot(snr_nda, ber_nda_plot, 'o', color=C_NDA, markersize=2.5, alpha=0.7, zorder=4)

    # HD-FEC line
    ax.axhline(HD_FEC, color=C_FEC, linestyle='-.', linewidth=0.8, alpha=0.5, label=f'HD-FEC ({HD_FEC:.0e})')

    # Find and annotate crossover
    xover = find_crossover(snr_da, ber_da, snr_nda, ber_nda)
    if xover is not None:
        ber_at_xover = 10 ** np.interp(xover, sn, np.log10(bn))
        ax.axvline(xover, color='gray', linewidth=0.6, linestyle=':', alpha=0.5, zorder=1)
        ax.plot(xover, ber_at_xover, 'x', color='black', markersize=8, markeredgewidth=1.5, zorder=5)
        ax.annotate(
            f'Crossover\n$\\bar{{\\gamma}}_d$ ≈ {xover:.0f} dB',
            xy=(xover, ber_at_xover),
            xytext=(xover - 8, ber_at_xover * 0.05),
            fontsize=7.5, fontweight='bold', ha='center',
            arrowprops=dict(arrowstyle='->', color='black', lw=0.8),
            zorder=6,
        )
        # Region labels
        ax.text(xover - 5, 0.3, 'DA-ML wins\n(pilot robust\nat low SNR)',
                fontsize=7, color=C_DA, ha='center', va='center', alpha=0.8,
                style='italic')
        ax.text(xover + 8, 0.3, 'NDA-ML wins\n(block integration\ngain at high SNR)',
                fontsize=7, color=C_NDA, ha='center', va='center', alpha=0.8,
                style='italic')
    else:
        print('[warn] No crossover found in data range')

    # Switched curve (track the better of DA/NDA at each SNR)
    snr_min = max(sd[0], sn[0])
    snr_max = min(sd[-1], sn[-1])
    grid = np.linspace(snr_min, snr_max, 300)
    da_grid = 10 ** np.interp(grid, sd, np.log10(np.maximum(bd, 1e-10)))
    nda_grid = 10 ** np.interp(grid, sn, np.log10(np.maximum(bn, 1e-10)))
    switched = np.minimum(da_grid, nda_grid)  # lower BER = better
    ax.plot(grid, switched, '-', color=C_SW, linewidth=1.0, alpha=0.6,
            label='Switched (tracks optimum)', zorder=2)

    ax.set_yscale('log')
    ax.set_ylim(1e-4, 0.5)
    ax.set_xlabel(r'$\bar{\gamma}_d$ (dB)', fontsize=9)
    ax.set_ylabel('BER', fontsize=9)
    ax.set_title('Estimator Crossover under Strong Turbulence\n(Basis for Block-Effective-SNR Switching)',
                 fontsize=9.5)
    ax.legend(fontsize=7.5, loc='upper right', frameon=True, edgecolor='gray')
    ax.grid(True, which='major', alpha=0.2, linewidth=0.5)
    ax.grid(True, which='minor', alpha=0.08, linewidth=0.3)
    ax.tick_params(labelsize=8)

    plt.tight_layout()
    fig.savefig(OUT_PNG, dpi=200, bbox_inches='tight')
    fig.savefig(OUT_PDF, bbox_inches='tight')
    print(f'[saved] {OUT_PNG}')
    print(f'[saved] {OUT_PDF}')
    if xover is not None:
        print(f'[crossover] SNR ≈ {xover:.1f} dB, BER ≈ {ber_at_xover:.2e}')
    plt.close(fig)


if __name__ == '__main__':
    main()
