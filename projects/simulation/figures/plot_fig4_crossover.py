# -*- coding: utf-8 -*-
"""Fig.4 observed DA/NDA BER crossovers across turbulence regimes.

The figure retains the six verified BER curves and uses two independent
visual encodings: scenario color and estimator line style.  Curves and
crossovers use the same piecewise-linear interpolation in log BER; the
observed crossovers are not switching thresholds.

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

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..'))

MAIN30 = os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_main_30seed', '_main_experiment_30seed.json')
EXT1 = os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_ber_ext_5seed', '_ber_ext_5seed.json')
EXT2 = os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_ber_ext_5seed', '_ber_ext2_5seed.json')
OUT_PNG = os.path.join(_HERE, 'ccisp_fig4_crossover.png')
OUT_PDF = os.path.join(_HERE, 'ccisp_fig4_crossover.pdf')

SCENES = ['weak', 'moderate', 'strong']
LABELS = {
    'weak': 'Weak',
    'moderate': 'Moderate',
    'strong': 'Strong',
}
COLORS = {
    'weak': '#0072B2',      # blue
    'moderate': '#E69F00',  # amber
    'strong': '#D55E00',    # vermillion
}
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


def log_linear_curve(snr, ber, n_dense=300):
    """Interpolate only between original samples, linearly in log BER."""
    ber_plot = np.where(ber > 0, ber, 1e-7)
    log_ber = np.log10(ber_plot)
    snr_u, idx = np.unique(snr, return_index=True)
    log_ber_u = log_ber[idx]
    snr_dense = np.linspace(snr_u[0], snr_u[-1], n_dense)
    return snr_dense, 10 ** np.interp(snr_dense, snr_u, log_ber_u)


def find_crossover(snr_da, ber_da, snr_nda, ber_nda):
    """Audit the first DA-to-NDA crossing by linear interpolation in log BER."""
    snr_min = max(np.min(snr_da), np.min(snr_nda))
    snr_max = min(np.max(snr_da), np.max(snr_nda))
    grid = np.union1d(snr_da, snr_nda)
    grid = grid[(grid >= snr_min) & (grid <= snr_max)]
    log_da = np.interp(grid, snr_da, np.log10(np.maximum(ber_da, 1e-10)))
    log_nda = np.interp(grid, snr_nda, np.log10(np.maximum(ber_nda, 1e-10)))
    delta = log_da - log_nda
    for i in range(1, len(grid)):
        if delta[i - 1] <= 0 < delta[i]:
            weight = -delta[i - 1] / (delta[i] - delta[i - 1])
            xo_snr = grid[i - 1] + weight * (grid[i] - grid[i - 1])
            xo_log_ber = log_da[i - 1] + weight * (log_da[i] - log_da[i - 1])
            return xo_snr, 10 ** xo_log_ber
    return None, None


def main():
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Times New Roman', 'DejaVu Serif'],
        'mathtext.fontset': 'stix',
        'axes.linewidth': 0.6,
        'pdf.fonttype': 42,
        'ps.fonttype': 42,
    })

    fig, ax = plt.subplots(figsize=(7.16, 4.0))

    crossovers = {}

    for scene in SCENES:
        color = COLORS[scene]
        snr_da, ber_da = merge_scene(scene, 'da_ml_ber_mean')
        snr_nda, ber_nda = merge_scene(scene, 'nda_ml_ber_mean')

        sd, bd = log_linear_curve(snr_da, ber_da)
        sn, bn = log_linear_curve(snr_nda, ber_nda)

        ber_da_plot = np.where(ber_da > 0, ber_da, 1e-7)
        ber_nda_plot = np.where(ber_nda > 0, ber_nda, 1e-7)

        # DA: solid line
        ax.plot(sd, bd, '-', color=color, linewidth=1.3)
        ax.plot(snr_da, ber_da_plot, 'o', color=color, markersize=2.5,
                alpha=0.6, markeredgecolor='none', zorder=4)

        # NDA: dashed line (same color)
        ax.plot(sn, bn, '--', color=color, linewidth=1.3)
        ax.plot(snr_nda, ber_nda_plot, 's', color=color, markersize=2.5,
                alpha=0.6, markeredgecolor='none', zorder=4)

        # Compute and mark the crossing from the same log-linear curves.
        # It is deliberately not labelled gamma_th.
        xo_snr, xo_ber = find_crossover(snr_da, ber_da, snr_nda, ber_nda)
        if xo_snr is not None:
            crossovers[scene] = xo_snr
            ax.plot(
                xo_snr,
                xo_ber,
                marker='o',
                linestyle='None',
                markersize=4.0,
                markerfacecolor='white',
                markeredgecolor=color,
                markeredgewidth=0.9,
                zorder=6,
            )
            label_offsets = {
                'weak': (0.35, 0.78),
                'moderate': (0.35, 1.22),
                'strong': (0.35, 1.18),
            }
            dx, y_scale = label_offsets[scene]
            ax.text(
                xo_snr + dx,
                xo_ber * y_scale,
                rf'$\approx {xo_snr:.1f}$ dB',
                fontsize=8.5,
                color=color,
                ha='left',
                va='center',
                zorder=7,
            )

    ax.set_yscale('log')
    ax.set_ylim(1e-4, 0.5)
    ax.set_xlim(4, 30)
    ax.set_xlabel(r'Average data-symbol SNR, $\bar{\gamma}_d$ (dB)', fontsize=9)
    ax.set_ylabel('Bit error rate (BER)', fontsize=9)
    ax.grid(True, which='major', alpha=0.2, linewidth=0.5)
    ax.grid(False, which='minor')
    ax.tick_params(labelsize=8.5)

    # Separate legends prevent a redundant 3 x 2 combination listing.
    from matplotlib.lines import Line2D
    scenario_handles = [
        Line2D([0], [0], color=COLORS[scene], linewidth=1.3, label=LABELS[scene])
        for scene in SCENES
    ]
    method_handles = [
        Line2D([0], [0], color='black', linestyle='-', linewidth=1.3,
               marker='o', markersize=3.0, label='DA'),
        Line2D([0], [0], color='black', linestyle='--', linewidth=1.3,
               marker='s', markersize=3.0, label='NDA'),
    ]
    scenario_legend = ax.legend(
        handles=scenario_handles,
        fontsize=8.5,
        loc='lower left',
        frameon=True,
        edgecolor='0.65',
        ncol=1,
        labelspacing=0.3,
        handletextpad=0.6,
        borderpad=0.4,
    )
    ax.add_artist(scenario_legend)
    ax.legend(
        handles=method_handles,
        fontsize=8.5,
        loc='lower left',
        bbox_to_anchor=(0.37, 0.0),
        frameon=True,
        edgecolor='0.65',
        ncol=1,
        labelspacing=0.3,
        handletextpad=0.6,
        borderpad=0.4,
    )

    plt.tight_layout()
    fig.savefig(OUT_PNG, dpi=300, bbox_inches='tight')
    fig.savefig(OUT_PDF, bbox_inches='tight')
    print(f'[saved] {OUT_PNG}')
    print(f'[saved] {OUT_PDF}')

    print('\n=== Computed crossovers (log-BER linear interpolation) ===')
    for scene in SCENES:
        if scene in crossovers:
            print(f'  {scene:<12}: {crossovers[scene]:.3f} dB')

    plt.close(fig)


if __name__ == '__main__':
    main()
