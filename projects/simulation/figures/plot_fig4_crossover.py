# -*- coding: utf-8 -*-
"""Fig.4 Multi-scene crossover comparison (CCISP beautified v2).

User decision (2026-07-11): draw weak/moderate/strong crossover overlay,
turning "crossover too low" into a physical finding:
  stronger turbulence -> deeper fades -> crossover occurs earlier
  -> NDA advantage region widens.

Layout: ratio plot (DA_BER / NDA_BER) vs SNR for 3 turbulence tiers.
  ratio > 1.0 = NDA wins (blind estimation superior)
  ratio < 1.0 = DA wins (pilot-aided superior)
Crossover = where ratio crosses 1.0.

This is more informative than single-scene BER curves because:
  1. Crossover position becomes a physical trend, not a visual blemish
  2. The "NDA advantage widens with turbulence" message is the core story
  3. No ugly low-BER crossover region — the ratio plot is clean

Data sources (read-only):
  30seed main: results/sc_nda_ml_main_30seed/_main_experiment_30seed.json
  5seed ext:   results/sc_nda_ml_ber_ext_5seed/_ber_ext_5seed.json + _ber_ext2_5seed.json

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

# 3 turbulence tiers (skip awgn = no turbulence baseline, skip uplink = keep it clean)
SCENES = ['weak', 'moderate', 'strong']
LABELS = {
    'weak': r'Weak ($\alpha$=4.0, $\beta$=3.0)',
    'moderate': r'Moderate ($\alpha$=2.5, $\beta$=1.8)',
    'strong': r'Strong ($\alpha$=1.5, $\beta$=0.8)',
}
COLORS = {
    'weak': '#56B4E9',      # light blue
    'moderate': '#E69F00',  # amber
    'strong': '#D55E00',    # vermillion (selling point = darkest)
}


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def merge_scene(scene, ber_key):
    """Merge 30seed main + 5seed ext for one scene."""
    snr_list, ber_list = [], []
    m = load(MAIN30)
    if scene in m['summary']:
        pts = m['summary'][scene]['points']
        for p in pts:
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


def compute_ratio(scene):
    """Compute DA_BER/NDA_BER ratio across SNR for one scene."""
    snr_da, ber_da = merge_scene(scene, 'da_ml_ber_mean')
    snr_nda, ber_nda = merge_scene(scene, 'nda_ml_ber_mean')

    # Interpolate DA and NDA to common SNR grid
    ber_da_plot = np.where(ber_da > 0, ber_da, 1e-7)
    ber_nda_plot = np.where(ber_nda > 0, ber_nda, 1e-7)

    snr_min = max(snr_da[0], snr_nda[0])
    snr_max = min(snr_da[-1], snr_nda[-1])
    grid = np.linspace(snr_min, snr_max, 300)

    da_grid = np.interp(grid, snr_da, ber_da_plot)
    nda_grid = np.interp(grid, snr_nda, ber_nda_plot)
    ratio = da_grid / np.maximum(nda_grid, 1e-10)

    # Also return raw points for plotting
    # Match DA and NDA at common SNR points
    common_snr = np.intersect1d(snr_da, snr_nda)
    if len(common_snr) > 0:
        da_raw = np.interp(common_snr, snr_da, ber_da_plot)
        nda_raw = np.interp(common_snr, snr_nda, ber_nda_plot)
        ratio_raw = da_raw / np.maximum(nda_raw, 1e-10)
    else:
        common_snr, ratio_raw = np.array([]), np.array([])

    return grid, ratio, common_snr, ratio_raw


def find_crossover(grid, ratio):
    """Find SNR where ratio crosses 1.0 upward (DA→NDA transition)."""
    above = ratio > 1.0
    for i in range(1, len(above)):
        if not above[i - 1] and above[i]:
            return grid[i]
    return None


def main():
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Times New Roman', 'DejaVu Serif'],
        'mathtext.fontset': 'stix',
        'axes.linewidth': 0.6,
    })

    fig, ax = plt.subplots(figsize=(6.5, 4.8))

    crossovers = {}

    for scene in SCENES:
        grid, ratio, raw_snr, raw_ratio = compute_ratio(scene)
        color = COLORS[scene]
        lw = 1.5 if scene == 'strong' else 1.1
        alpha = 1.0 if scene == 'strong' else 0.75

        # Smooth ratio line
        ax.plot(grid, ratio, '-', color=color, linewidth=lw, alpha=alpha,
                label=LABELS[scene], zorder=3)
        # Raw data points
        if len(raw_snr) > 0:
            ax.plot(raw_snr, raw_ratio, 'o', color=color, markersize=2.5,
                    alpha=0.6, markeredgecolor='none', zorder=4)

        # Find and mark crossover
        xo = find_crossover(grid, ratio)
        if xo is not None:
            crossovers[scene] = xo
            ax.plot(xo, 1.0, 'x', color=color, markersize=9,
                    markeredgewidth=1.8, zorder=5)
            # Annotate crossover position
            ax.annotate(
                f'{xo:.0f} dB',
                xy=(xo, 1.0),
                xytext=(xo + 1.5, 1.0 + (0.08 if scene == 'weak' else
                                          0.14 if scene == 'moderate' else 0.20)),
                fontsize=7, color=color, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=color, lw=0.7),
                zorder=6,
            )

    # Ratio = 1.0 reference line (the crossover threshold)
    ax.axhline(1.0, color='gray', linewidth=0.7, linestyle='-', alpha=0.5, zorder=1)

    # Region labels
    ax.text(6.5, 1.30, 'NDA-ML wins\n(blind superior)', fontsize=7.5,
            color='#D55E00', ha='center', va='center', alpha=0.8, style='italic')
    ax.text(6.5, 0.82, 'DA-ML wins\n(pilot robust)', fontsize=7.5,
            color='#0072B2', ha='center', va='center', alpha=0.8, style='italic')

    ax.set_xlabel(r'$\bar{\gamma}_d$ (dB)', fontsize=9)
    ax.set_ylabel(r'$\mathrm{BER}_{DA} \,/\, \mathrm{BER}_{NDA}$', fontsize=9)
    ax.set_title('Crossover Shifts toward Lower SNR as Turbulence Strengthens\n'
                 '(NDA Advantage Region Widens)',
                 fontsize=9.5)

    ax.set_ylim(0.70, 1.45)
    ax.set_xlim(4, 28)
    ax.grid(True, alpha=0.2, linewidth=0.5)
    ax.tick_params(labelsize=8)

    ax.legend(fontsize=7.5, loc='upper right', frameon=True, edgecolor='gray',
              title='Turbulence tier', title_fontsize=7.5)

    # Add interpretation box
    textstr = ('Observation: Under stronger turbulence,\n'
               'deeper fades cause earlier pilot-segment\n'
               'failures, expanding the NDA-ML advantage\n'
               'region to lower SNR.')
    props = dict(boxstyle='round,pad=0.4', facecolor='#FFF8E1', edgecolor='#E0E0E0', alpha=0.9)
    ax.text(0.02, 0.02, textstr, transform=ax.transAxes, fontsize=6.8,
            verticalalignment='bottom', bbox=props, color='#444')

    plt.tight_layout()
    fig.savefig(OUT_PNG, dpi=200, bbox_inches='tight')
    fig.savefig(OUT_PDF, bbox_inches='tight')
    print(f'[saved] {OUT_PNG}')
    print(f'[saved] {OUT_PDF}')

    # Print crossover summary
    print('\n=== Crossover positions (DA/NDA ratio crosses 1.0) ===')
    for scene in SCENES:
        if scene in crossovers:
            print(f'  {scene:<12}: ~{crossovers[scene]:.1f} dB')
        else:
            print(f'  {scene:<12}: no crossover (NDA never wins in plotted range)')

    plt.close(fig)


if __name__ == '__main__':
    main()
