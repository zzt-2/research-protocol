# -*- coding: utf-8 -*-
"""Single-axis BER comparison for AWGN and three formal downlink regimes.

The plot consumes only the authority-checked 30-seed fixed result. Regimes are
encoded by color and CPR algorithms by line style; interpolation is only a
visual guide between formal samples.

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
    'legend': 6.5,
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
CURVE_SPECS = (
    {
        'ber_key': 'da',
        'label': 'DA',
        'color': C_DA,
        'linestyle': '-',
    },
    {
        'ber_key': 'nda',
        'label': 'NDA',
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
    'awgn': (5.0, 2.0),
    'weak': (5.0, 2.0),
    'moderate': (5.0, 2.0),
    'strong': (5.0, 2.0),
}
SCENE_COLORS = {
    'awgn': '#000000', 'weak': '#0072B2',
    'moderate': '#E69F00', 'strong': '#D55E00',
}
METHOD_STYLES = {'da': '-', 'nda': '--', 'oracle': ':'}


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
    snr = np.array(sorted(groups))
    # A zero count is not an exact zero BER. Plot a half-count estimate so the
    # log-scale curve remains finite without inventing an arbitrary floor.
    ber = np.array([(groups[x][0] if groups[x][0] else 0.5) / groups[x][1] for x in snr])
    return snr, ber


def validate_formal(payload):
    a = payload['authority']; hashes = a.get('imported_file_sha256', {})
    if a.get('authority_status') != 'formal' or a.get('route') != 'fixed': raise ValueError('fixed formal authority required')
    if a.get('params_sha256') != hashes.get('params.py'): raise ValueError('params hash mismatch')
    if a['grid']['scenes'] != SCENES or a['grid']['n_seeds'] != 30 or a['grid']['windows_per_seed'] != 400: raise ValueError('formal grid mismatch')


def smooth_curve(snr, ber, n_dense=200):
    """Interpolate for visual continuity (cubic in log-BER domain).

    Only used for the drawn solid curves; sample markers are intentionally omitted.
    """
    log_ber = np.log10(ber)
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

    ax.set_yscale('log')
    ax.set_title(TITLES[scene], fontsize=FONT_SIZES['title'], pad=4)
    major_interval, minor_interval = X_TICK_INTERVALS[scene]
    ax.set_xlim(5.0, 35.0)
    ax.set_xticks(np.arange(5.0, 36.0, 2.0))
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
    """Use a common log-BER range so all four panels are directly comparable."""
    ax.set_ylim(1e-6, 1)


def main():
    plt.rcParams.update(MPL_RCPARAMS)
    # A single axes keeps the four regimes and three receiver references in
    # one directly comparable coordinate system.  Regime is encoded by color;
    # receiver reference by line style (solid/dashed/dotted).
    fig, ax = plt.subplots(figsize=(3.5, 3.0))
    for scene in SCENES:
        for spec in CURVE_SPECS:
            snr, ber = merge_scene(scene, spec['ber_key'])
            if len(snr) == 0:
                continue
            snr_s, ber_s = smooth_curve(snr, ber)
            ax.plot(snr_s, ber_s, METHOD_STYLES[spec['ber_key']],
                    color=SCENE_COLORS[scene], linewidth=1.05,
                    label=f'{scene}:{spec["label"]}')
    ax.set_yscale('log')
    ax.set_xlim(5.0, 35.0)
    ax.set_xticks(np.arange(5.0, 36.0, 2.0))
    ax.set_ylim(1e-6, 1)
    ax.set_xlabel(r'Data-symbol $E_s/N_0$ [dB]', fontsize=FONT_SIZES['label'])
    ax.set_ylabel('Bit error rate (BER)', fontsize=FONT_SIZES['label'])
    ax.xaxis.set_minor_locator(MultipleLocator(1.0))
    ax.grid(True, which='major', color='#d0d0d0', alpha=0.55, linewidth=0.45)
    ax.grid(False, which='minor', axis='y')
    ax.tick_params(axis='both', which='major', labelsize=FONT_SIZES['tick'],
                   width=0.6, length=3)
    ax.tick_params(axis='both', which='minor', width=0.5, length=2)
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color=SCENE_COLORS[s], linewidth=1.1,
               label="AWGN" if s == "awgn" else s.title()) for s in SCENES
    ] + [
        Line2D([0], [0], color='black', linestyle=METHOD_STYLES[k],
               linewidth=1.1, label=k.upper()) for k in ('da', 'nda', 'oracle')
    ]
    ax.legend(handles=legend_elements, loc='lower left',
              bbox_to_anchor=(0.04, 0.03), ncol=2,
              fontsize=FONT_SIZES['legend'],
              frameon=True, framealpha=0.78, facecolor='white',
              edgecolor='#b0b0b0', borderpad=0.3, labelspacing=0.2,
              columnspacing=0.65, handlelength=1.25)
    fig.subplots_adjust(left=0.19, right=0.98, top=0.97, bottom=0.20)
    fig.savefig(OUT_PNG, dpi=300)
    fig.savefig(OUT_PDF)
    print(f'[saved] {OUT_PNG}')
    print(f'[saved] {OUT_PDF}')
    plt.close(fig)


if __name__ == '__main__':
    main()
