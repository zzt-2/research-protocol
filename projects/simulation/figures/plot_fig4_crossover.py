# -*- coding: utf-8 -*-
"""Fig.4 Multi-scene BER crossover (CCISP v3: single plot, 6 lines).

User decision (2026-07-11): single plot with 6 BER curves.
  - 3 turbulence tiers: weak / moderate / strong (color-coded)
  - 2 estimators per tier: DA-ML (solid) / NDA-ML (dashed)
  - Crossover = where DA-solid crosses NDA-dashed (per color)

Message: crossover shifts left as turbulence strengthens
  weak ~19dB / moderate ~18dB / strong ~11dB
  -> NDA advantage region widens with turbulence

Data sources (read-only):
  30seed main + 5seed ext

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

SCENES = ['weak', 'moderate', 'strong']
LABELS = {
    'weak': r'Weak ($\alpha$=4.0, $\beta$=3.0)',
    'moderate': r'Moderate ($\alpha$=2.5, $\beta$=1.8)',
    'strong': r'Strong ($\alpha$=1.5, $\beta$=0.8)',
}
COLORS = {
    'weak': '#0072B2',      # blue
    'moderate': '#E69F00',  # amber
    'strong': '#D55E00',    # vermillion
}
HD_FEC = 3.8e-3


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def merge_scene(scene, ber_key):
    snr_list, ber_list = [], []
    m = load(MAIN30)
    if scene in m['summary']:
        for p in m['summary'][scene]['points']:
            snr_list.append(p['snr_db'])
            ber_list.append(p[ber_key])
    e1 = load(EXT1)
    if scene in e1['summary']:
        for p in e1['summary'][scene]['points']:
            snr_list.append(p['snr_db'])
            ber_list.append(p[ber_key])
    if os.path.exists(EXT2):
        e2 = load(EXT2)
        if scene in e2['summary']:
            for p in e2['summary'][scene]['points']:
                snr_list.append(p['snr_db'])
                ber_list.append(p[ber_key])
    snr = np.array(snr_list)
    ber = np.array(ber_list)
    order = np.argsort(snr)
    return snr[order], ber[order]


def smooth_log(snr, ber, n_dense=300):
    ber_plot = np.where(ber > 0, ber, 1e-7)
    log_ber = np.log10(ber_plot)
    snr_u, idx = np.unique(snr, return_index=True)
    log_ber_u = log_ber[idx]
    kind = 'cubic' if len(snr_u) >= 4 else 'linear'
    f = interp1d(snr_u, log_ber_u, kind=kind, fill_value='extrapolate')
    snr_dense = np.linspace(snr_u[0], snr_u[-1], n_dense)
    return snr_dense, 10 ** f(snr_dense)


def find_crossover(snr_da, ber_da, snr_nda, ber_nda):
    sd, bd = smooth_log(snr_da, ber_da, n_dense=500)
    sn, bn = smooth_log(snr_nda, ber_nda, n_dense=500)
    snr_min = max(sd[0], sn[0])
    snr_max = min(sd[-1], sn[-1])
    grid = np.linspace(snr_min, snr_max, 500)
    da_grid = 10 ** np.interp(grid, sd, np.log10(np.maximum(bd, 1e-10)))
    nda_grid = 10 ** np.interp(grid, sn, np.log10(np.maximum(bn, 1e-10)))
    above = da_grid > nda_grid  # DA BER higher = NDA wins
    for i in range(1, len(above)):
        if not above[i - 1] and above[i]:
            return grid[i], da_grid[i]
    return None, None


def main():
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Times New Roman', 'DejaVu Serif'],
        'mathtext.fontset': 'stix',
        'axes.linewidth': 0.6,
    })

    fig, ax = plt.subplots(figsize=(6.8, 5.0))

    crossovers = {}

    for scene in SCENES:
        color = COLORS[scene]
        snr_da, ber_da = merge_scene(scene, 'da_ml_ber_mean')
        snr_nda, ber_nda = merge_scene(scene, 'nda_ml_ber_mean')

        sd, bd = smooth_log(snr_da, ber_da)
        sn, bn = smooth_log(snr_nda, ber_nda)

        ber_da_plot = np.where(ber_da > 0, ber_da, 1e-7)
        ber_nda_plot = np.where(ber_nda > 0, ber_nda, 1e-7)

        # DA: solid line
        ax.plot(sd, bd, '-', color=color, linewidth=1.3,
                label=f'{LABELS[scene]} — DA-ML' if scene == 'weak' else '')
        ax.plot(snr_da, ber_da_plot, 'o', color=color, markersize=2.5,
                alpha=0.6, markeredgecolor='none', zorder=4)

        # NDA: dashed line (same color)
        ax.plot(sn, bn, '--', color=color, linewidth=1.3,
                label=f'{LABELS[scene]} — NDA-ML' if scene == 'weak' else '')
        ax.plot(snr_nda, ber_nda_plot, 's', color=color, markersize=2.5,
                alpha=0.6, markeredgecolor='none', zorder=4)

        # Mark crossover
        xo_snr, xo_ber = find_crossover(snr_da, ber_da, snr_nda, ber_nda)
        if xo_snr is not None:
            crossovers[scene] = xo_snr
            ax.plot(xo_snr, xo_ber, 'x', color=color, markersize=10,
                    markeredgewidth=2.0, zorder=6)
            # Label crossover SNR
            y_offset = 1.6 if scene == 'weak' else (1.8 if scene == 'moderate' else 1.4)
            ax.annotate(
                f'{xo_snr:.0f} dB',
                xy=(xo_snr, xo_ber),
                xytext=(xo_snr + 2, xo_ber * y_offset),
                fontsize=7, color=color, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=color, lw=0.7),
                zorder=7,
            )

    # HD-FEC reference
    ax.axhline(HD_FEC, color='gray', linestyle='-.', linewidth=0.8, alpha=0.5,
               label=f'HD-FEC ({HD_FEC:.0e})')

    ax.set_yscale('log')
    ax.set_ylim(1e-4, 0.5)
    ax.set_xlim(4, 30)
    ax.set_xlabel(r'$\bar{\gamma}_d$ (dB)', fontsize=9)
    ax.set_ylabel('BER', fontsize=9)
    ax.set_title('Crossover Shifts toward Lower SNR as Turbulence Strengthens',
                 fontsize=9.5)
    ax.grid(True, which='major', alpha=0.2, linewidth=0.5)
    ax.grid(True, which='minor', alpha=0.08, linewidth=0.3)
    ax.tick_params(labelsize=8)

    # Custom legend: 3 scene colors × 2 line styles + HD-FEC
    from matplotlib.lines import Line2D
    legend_elements = []
    for scene in SCENES:
        color = COLORS[scene]
        legend_elements.append(Line2D([0], [0], color=color, linestyle='-',
                                      linewidth=1.3,
                                      label=f'{LABELS[scene]}: DA-ML'))
        legend_elements.append(Line2D([0], [0], color=color, linestyle='--',
                                      linewidth=1.3,
                                      label=f'{LABELS[scene]}: NDA-ML'))
    legend_elements.append(Line2D([0], [0], color='gray', linestyle='-.',
                                  linewidth=0.8, label=f'HD-FEC ({HD_FEC:.0e})'))
    legend_elements.append(Line2D([0], [0], marker='x', color='gray',
                                  linestyle='None', markersize=8,
                                  markeredgewidth=1.5,
                                  label='Crossover (DA↔NDA)'))

    ax.legend(handles=legend_elements, fontsize=6.5, loc='lower left',
              frameon=True, edgecolor='gray', ncol=2,
              columnspacing=1.0, labelspacing=0.3,
              handletextpad=0.5, borderpad=0.4)

    plt.tight_layout()
    fig.savefig(OUT_PNG, dpi=200, bbox_inches='tight')
    fig.savefig(OUT_PDF, bbox_inches='tight')
    print(f'[saved] {OUT_PNG}')
    print(f'[saved] {OUT_PDF}')

    print('\n=== Crossover positions ===')
    for scene in SCENES:
        if scene in crossovers:
            print(f'  {scene:<12}: ~{crossovers[scene]:.1f} dB')

    plt.close(fig)


if __name__ == '__main__':
    main()
