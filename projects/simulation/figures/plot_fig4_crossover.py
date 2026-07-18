# -*- coding: utf-8 -*-
"""Fig.4 observed DA/NDA BER crossovers across turbulence regimes.

The figure retains the six formal downlink BER curves and uses two independent
visual encodings: scenario color and estimator line style.  Curves and
crossovers use the same piecewise-linear interpolation in log BER; the
observed crossovers are not switching thresholds.

Data source (read-only): formal 30-seed fixed JSON only.

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

MAIN30 = os.path.join(_SIM_ROOT, 'results', 'ccisp_family1_fixed_30seed.json')
OUT_PNG = os.path.join(_HERE, 'ccisp_fig4_crossover.png')
OUT_PDF = os.path.join(_HERE, 'ccisp_fig4_crossover.pdf')

# Compact conference-column footprint; width and typography remain unchanged.
FIGSIZE_IN = (3.5, 2.85)
FONT_SIZES = {
    'title': 10.0,
    'label': 10.0,
    'tick': 9.0,
    'legend': 9.0,
    'annotation': 9.0,
}
MPL_RCPARAMS = {
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'Times', 'Nimbus Roman No9 L', 'DejaVu Serif'],
    'mathtext.fontset': 'stix',
    'text.usetex': False,
    'font.weight': 'normal',
    'axes.labelweight': 'normal',
    'axes.linewidth': 0.6,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
}

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
MARKERS = {'weak': 'o', 'moderate': 's', 'strong': '^'}
def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def merge_scene(scene, ber_key):
    m = load(MAIN30)
    validate_formal(m); groups = {}
    method = 'da' if ber_key.startswith('da') else 'nda'
    for row in m['raw']:
        if row['scene'] == scene:
            g = groups.setdefault(float(row['snr_db']), [0, 0]); g[0] += int(row[f'{method}_errors']); g[1] += int(row[f'{method}_bits'])
    snr = np.array(sorted(groups)); return snr, np.array([groups[x][0] / groups[x][1] for x in snr])


def validate_formal(payload):
    a = payload['authority']; hashes = a.get('imported_file_sha256', {})
    if a.get('authority_status') != 'formal' or a.get('route') != 'fixed': raise ValueError('fixed formal authority required')
    if a.get('params_sha256') != hashes.get('params.py'): raise ValueError('params hash mismatch')
    if a['grid']['scenes'] != ['awgn', 'weak', 'moderate', 'strong'] or a['grid']['n_seeds'] != 30 or a['grid']['windows_per_seed'] != 400: raise ValueError('formal grid mismatch')


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
    plt.rcParams.update(MPL_RCPARAMS)

    fig, ax = plt.subplots(figsize=FIGSIZE_IN)

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
        ax.plot(snr_da, ber_da_plot, MARKERS[scene], color=color, markersize=2.5,
                alpha=0.6, markeredgecolor='none', zorder=4)

        # NDA: dashed line (same color)
        ax.plot(sn, bn, '--', color=color, linewidth=1.3)
        ax.plot(snr_nda, ber_nda_plot, MARKERS[scene], color=color, markersize=2.5,
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
            ax.annotate(
                rf'${xo_snr:.1f}$ dB',
                xy=(xo_snr, xo_ber),
                xytext=(xo_snr + dx, xo_ber * y_scale),
                textcoords='data',
                fontsize=FONT_SIZES['annotation'],
                color=color,
                ha='left',
                va='center',
                arrowprops={'arrowstyle': '-', 'color': color,
                            'linewidth': 0.7, 'shrinkA': 2, 'shrinkB': 2},
                bbox={'facecolor': 'white', 'edgecolor': 'none', 'alpha': 0.8, 'pad': 0.1},
                zorder=7,
            )

    ax.set_yscale('log')
    ax.set_ylim(1e-4, 0.5)
    ax.set_xlim(5, 35)
    ax.set_xlabel(
        r'Data-symbol $E_s/N_0$ [dB]',
        fontsize=FONT_SIZES['label'],
    )
    ax.set_ylabel('Bit error rate (BER)', fontsize=FONT_SIZES['label'])
    ax.grid(True, which='major', alpha=0.2, linewidth=0.5)
    ax.grid(False, which='minor')
    ax.tick_params(labelsize=FONT_SIZES['tick'])

    # Keep scenario and method encodings separate; place both legend blocks
    # inside the upper-right data-sparse part of the axes.
    from matplotlib.lines import Line2D
    scenario_handles = [
        Line2D([0], [0], color=COLORS[scene], linewidth=1.3,
               marker=MARKERS[scene], markersize=3.0, label=LABELS[scene])
        for scene in SCENES
    ]
    method_handles = [
        Line2D([0], [0], color='black', linestyle='-', linewidth=1.3,
               label='DA'),
        Line2D([0], [0], color='black', linestyle='--', linewidth=1.3,
               label='NDA'),
    ]
    ax.legend(
        handles=scenario_handles + method_handles,
        fontsize=6.5,
        loc='upper center',
        bbox_to_anchor=(0.55, 0.98),
        frameon=True,
        framealpha=0.78,
        facecolor='white',
        edgecolor='#b0b0b0',
        ncol=5,
        columnspacing=0.42,
        labelspacing=0.25,
        handletextpad=0.25,
        borderpad=0.3,
        handlelength=1.0,
    )

    fig.subplots_adjust(left=0.20, right=0.97, top=0.97, bottom=0.19)
    fig.savefig(OUT_PNG, dpi=300)
    fig.savefig(OUT_PDF)
    print(f'[saved] {OUT_PNG}')
    print(f'[saved] {OUT_PDF}')

    print('\n=== Computed crossovers (log-BER linear interpolation) ===')
    for scene in SCENES:
        if scene in crossovers:
            print(f'  {scene:<12}: {crossovers[scene]:.3f} dB')

    plt.close(fig)


if __name__ == '__main__':
    main()
