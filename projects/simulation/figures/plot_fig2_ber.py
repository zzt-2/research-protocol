# -*- coding: utf-8 -*-
"""BER versus SNR for AWGN and three formal downlink regimes.

The 2x2 layout consumes only the authority-checked 30-seed fixed result.
Interpolation is only a visual guide between formal samples.

Output: figures/ccisp_fig2_ber.png + .pdf
"""
import os
import json

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from scipy.interpolate import interp1d

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..'))

MAIN30 = os.path.join(_SIM_ROOT, 'results', 'ccisp_family1_fixed_30seed.json')
OUT_PNG = os.path.join(_HERE, 'ccisp_fig2_ber.png')
OUT_PDF = os.path.join(_HERE, 'ccisp_fig2_ber.pdf')

FIGSIZE_IN = (3.5, 4.7)
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
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'axes.linewidth': 0.6,
}

# Scene order: AWGN followed by increasing downlink turbulence.
SCENES = ['awgn', 'weak', 'moderate', 'strong']
TITLES = {
    'awgn': '(a) AWGN',
    'weak': '(b) Weak turbulence',
    'moderate': '(c) Moderate turbulence',
    'strong': '(d) Strong turbulence',
}

# Colorblind-safe palette (Okabe-Ito inspired)
C_DA = '#0072B2'    # blue
C_NDA = '#D55E00'   # vermillion (orange-red)
C_OR = '#009E73'    # green
C_FEC = '#999999'   # gray for HD-FEC line

HD_FEC = 3.8e-3
CURVE_SPECS = (
    {
        'ber_key': 'da',
        'label': 'DA-ML',
        'color': C_DA,
        'linestyle': '-',
    },
    {
        'ber_key': 'nda',
        'label': 'NDA-ML',
        'color': C_NDA,
        'linestyle': '-',
    },
    {
        'ber_key': 'oracle',
        'label': 'Oracle',
        'color': C_OR,
        'linestyle': '-',
    },
)
X_TICK_INTERVALS = {
    'awgn': (5.0, 2.5),
    'weak': (10.0, 5.0),
    'moderate': (10.0, 5.0),
    'strong': (10.0, 5.0),
}


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def merge_scene(scene, ber_key):
    m = load(MAIN30)
    validate_formal(m); groups = {}
    for row in m['raw']:
        if row['scene'] == scene:
            g = groups.setdefault(float(row['snr_db']), [0, 0])
            g[0] += int(row[f'{ber_key}_errors']); g[1] += int(row[f'{ber_key}_bits'])
    snr = np.array(sorted(groups)); return snr, np.array([groups[x][0] / groups[x][1] for x in snr])


def validate_formal(payload):
    a = payload['authority']; hashes = a.get('imported_file_sha256', {})
    if a.get('authority_status') != 'formal' or a.get('route') != 'fixed': raise ValueError('fixed formal authority required')
    if a.get('params_sha256') != hashes.get('params.py'): raise ValueError('params hash mismatch')
    if a['grid']['scenes'] != SCENES or a['grid']['n_seeds'] != 30 or a['grid']['windows_per_seed'] != 400: raise ValueError('formal grid mismatch')


def smooth_curve(snr, ber, n_dense=200):
    """Interpolate for visual continuity (cubic in log-BER domain).

    Only used for the drawn solid curves; sample markers are intentionally omitted.
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


def plot_one(ax, scene, row, col):
    """Plot one A2 subplot: solid DA/NDA/oracle curves distinguished by color."""
    for spec in CURVE_SPECS:
        ber_key = spec['ber_key']
        color = spec['color']
        ls = spec['linestyle']
        snr, ber = merge_scene(scene, ber_key)
        if len(snr) == 0:
            continue

        # Smooth interpolated line
        snr_s, ber_s = smooth_curve(snr, ber)
        ax.plot(snr_s, ber_s, ls, color=color, linewidth=1.2, zorder=3)

    # HD-FEC reference line
    ax.axhline(HD_FEC, color=C_FEC, linestyle='-', linewidth=0.7,
               alpha=0.7, zorder=1)
    if scene == 'awgn':
        ax.text(0.97, HD_FEC, 'HD-FEC', transform=ax.get_yaxis_transform(),
                ha='right', va='bottom', color=C_FEC,
                fontsize=FONT_SIZES['annotation'])

    ax.set_yscale('log')
    ax.set_title(TITLES[scene], fontsize=FONT_SIZES['title'], pad=4)
    major_interval, minor_interval = X_TICK_INTERVALS[scene]
    ax.xaxis.set_major_locator(MultipleLocator(major_interval))
    ax.xaxis.set_minor_locator(MultipleLocator(minor_interval))
    ax.grid(True, which='major', color='#d0d0d0', alpha=0.55, linewidth=0.45)
    ax.grid(True, which='minor', axis='x', color='#e5e5e5', alpha=0.45,
            linewidth=0.3)
    ax.grid(False, which='minor', axis='y')
    ax.tick_params(axis='both', which='major', labelsize=FONT_SIZES['tick'], width=0.6, length=3)
    ax.tick_params(axis='both', which='minor', width=0.5, length=2)

    # Adaptive y-axis range
    set_yrange(ax, scene)

def set_yrange(ax, scene):
    """Adaptive y-axis: non-turbulence scenes to 1e-5, strong/uplink narrower."""
    if scene in ('awgn', 'weak', 'moderate'):
        ax.set_ylim(1e-6, 1)
    else:  # strong / uplink: deep fade, don't force 1e-5
        ax.set_ylim(1e-4, 0.5)


def main():
    plt.rcParams.update(MPL_RCPARAMS)

    fig, axes = plt.subplots(2, 2, figsize=FIGSIZE_IN, sharex=False, sharey=False)
    axes = axes.flatten()

    for idx, scene in enumerate(SCENES):
        plot_one(axes[idx], scene, row=idx // 2, col=idx % 2)

    # Shared A2 legend at bottom (color-only solid lines, no markers)
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D(
            [0],
            [0],
            color=spec['color'],
            linestyle=spec['linestyle'],
            linewidth=1.2,
            label=spec['label'],
        )
        for spec in CURVE_SPECS
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=3,
               fontsize=FONT_SIZES['legend'],
               bbox_to_anchor=(0.5, 0.006), frameon=False)

    fig.supxlabel(r'Data-symbol $E_s/N_0$ [dB]',
                  fontsize=FONT_SIZES['label'], y=0.115)
    fig.supylabel('Bit error rate (BER)', fontsize=FONT_SIZES['label'], x=0.015)
    fig.subplots_adjust(left=0.18, right=0.98, top=0.94, bottom=0.185,
                        wspace=0.36, hspace=0.32)
    fig.savefig(OUT_PNG, dpi=300)
    fig.savefig(OUT_PDF)
    print(f'[saved] {OUT_PNG}')
    print(f'[saved] {OUT_PDF}')
    plt.close(fig)


if __name__ == '__main__':
    main()
