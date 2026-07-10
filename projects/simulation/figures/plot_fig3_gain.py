# -*- coding: utf-8 -*-
"""Fig.3 Net gain vs turbulence strength (CCISP beautified version).

Plan B from R007 sec3.3: draw all 6 scenes (increasing turbulence),
visually de-emphasize weak-turbulence scenes (lighter / dashed),
highlight strong-turbulence / uplink selling points (dark / bold + annotations).

Two metrics overlaid:
  - naive (net of pilot overhead): the "hard" number, recommended primary
  - fair  (including pilot power penalty): the "big" number, secondary

D004 口径: fair = naive + 1.249 dB (fair is the LARGER number).
  Verified: fair_comparison.py:109 gain_hdfec = (s_da_d + pilot_overhead_db) - s_nda_d

Data source (read-only):
  results/sc_nda_ml_main_30seed/_fair_gain_summary_30seed.json

Output: figures/ccisp_fig3_gain.png + .pdf
"""
import os
import json

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..'))
GAIN_JSON = os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_main_30seed', '_fair_gain_summary_30seed.json')
OUT_PNG = os.path.join(_HERE, 'ccisp_fig3_gain.png')
OUT_PDF = os.path.join(_HERE, 'ccisp_fig3_gain.pdf')

PILOT_OVERHEAD = 1.2493873660829993  # 10*log10(4/3), from JSON meta

# Scene order: increasing turbulence
SCENES = ['awgn', 'weak', 'moderate', 'strong', 'uplink_moderate', 'uplink_strong']
LABELS = ['AWGN', 'Weak', 'Moderate', 'Strong\n(down)', 'Uplink\nmod.', 'Uplink\nstrong']
SELLING_IDX = [3, 4, 5]  # strong, uplink_moderate, uplink_strong (0-indexed)

C_NAIVE = '#D55E00'   # vermillion (primary, harder number)
C_FAIR = '#0072B2'    # blue (secondary, bigger number)


def load_gain(scene):
    """Extract fair gain mean + CI95 for one scene.

    For HD-FEC-reachable scenes (awgn/weak/mod): use gain_mean_db / gain_ci95_db.
    For unreachable scenes (strong/uplink): use workregion_grand_mean / workregion_grand_ci95.
    """
    with open(GAIN_JSON, 'r', encoding='utf-8') as f:
        d = json.load(f)
    entry = d['fair_gain'][scene]

    if entry.get('hdfec_reachable'):
        fair_mean = entry['gain_mean_db']
        fair_ci = entry['gain_ci95_db']
    else:
        fair_mean = entry['workregion_grand_mean_db']
        fair_ci = entry['workregion_grand_ci95_db']

    # naive = fair - pilot_overhead (D004: fair is the LARGER number)
    naive_mean = fair_mean - PILOT_OVERHEAD
    naive_ci = [fair_ci[0] - PILOT_OVERHEAD, fair_ci[1] - PILOT_OVERHEAD]

    return {
        'fair_mean': fair_mean, 'fair_ci': fair_ci,
        'naive_mean': naive_mean, 'naive_ci': naive_ci,
    }


def main():
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Times New Roman', 'DejaVu Serif'],
        'mathtext.fontset': 'stix',
        'axes.linewidth': 0.6,
    })

    fig, ax = plt.subplots(figsize=(6.5, 4.5))

    x = np.arange(len(SCENES))

    # Extract data for all scenes
    data = [load_gain(s) for s in SCENES]

    fair_means = [d['fair_mean'] for d in data]
    fair_lo = [d['fair_ci'][0] for d in data]
    fair_hi = [d['fair_ci'][1] for d in data]
    naive_means = [d['naive_mean'] for d in data]
    naive_lo = [d['naive_ci'][0] for d in data]
    naive_hi = [d['naive_ci'][1] for d in data]

    fair_err = [np.array(fair_means) - np.array(fair_lo),
                np.array(fair_hi) - np.array(fair_means)]
    naive_err = [np.array(naive_means) - np.array(naive_lo),
                 np.array(naive_hi) - np.array(naive_means)]

    # --- fair line (secondary, blue, thinner) ---
    ax.errorbar(x, fair_means, yerr=fair_err, fmt='s-', color=C_FAIR,
                linewidth=1.2, markersize=4, capsize=3, capthick=0.8,
                label=f'Fair (incl. pilot penalty, +{PILOT_OVERHEAD:.1f} dB)',
                zorder=3, alpha=0.8)

    # --- naive line (primary, vermillion, thicker + bold markers at selling points) ---
    # Non-selling points: lighter, smaller markers
    non_sell_mask = np.array([i not in SELLING_IDX for i in range(len(x))])
    sell_mask = np.array([i in SELLING_IDX for i in range(len(x))])

    # Draw full naive errorbar line but style selling points differently
    ax.errorbar(x, naive_means, yerr=naive_err, fmt='o-', color=C_NAIVE,
                linewidth=1.5, markersize=5, capsize=3, capthick=0.8,
                label='Naive (net of pilot overhead)',
                zorder=4)

    # Overlay: highlight selling-point markers (bigger, with edge)
    ax.plot(x[sell_mask], np.array(naive_means)[sell_mask], 'o',
            color=C_NAIVE, markersize=8, markeredgecolor='white',
            markeredgewidth=1.2, zorder=5)

    # Annotate selling-point naive gains
    for idx in SELLING_IDX:
        val = naive_means[idx]
        ax.annotate(f'{val:+.2f} dB', xy=(x[idx], val),
                    xytext=(x[idx] + 0.15, val + 0.25),
                    fontsize=7, color=C_NAIVE, fontweight='bold',
                    arrowprops=dict(arrowstyle='-', color=C_NAIVE, lw=0.5),
                    zorder=6)

    # Visual de-emphasis: shade non-selling region
    ax.axvspan(-0.5, 2.5, alpha=0.04, color='gray', zorder=0)
    ax.text(1.0, ax.get_ylim()[1] if ax.get_ylim()[1] > 0 else 3.5,
            'Weak turbulence\n(gain ≈ 0, not reported)',
            fontsize=6.5, color='gray', ha='center', va='top',
            style='italic', alpha=0.7)

    # Zero reference line
    ax.axhline(0, color='gray', linewidth=0.5, linestyle='-', alpha=0.4)

    ax.set_xticks(x)
    ax.set_xticklabels(LABELS, fontsize=8)
    ax.set_ylabel('Net gain over DA-ML (dB)', fontsize=9)
    ax.set_xlabel('Turbulence scenario (increasing strength)', fontsize=9)
    ax.set_title('NDA-ML Net Gain vs. Turbulence Strength', fontsize=10)
    ax.legend(fontsize=7.5, loc='upper left', frameon=True, edgecolor='gray')
    ax.grid(True, axis='y', alpha=0.2, linewidth=0.5)
    ax.set_xlim(-0.5, len(SCENES) - 0.5)
    ax.tick_params(labelsize=8)

    plt.tight_layout()
    fig.savefig(OUT_PNG, dpi=200, bbox_inches='tight')
    fig.savefig(OUT_PDF, bbox_inches='tight')
    print(f'[saved] {OUT_PNG}')
    print(f'[saved] {OUT_PDF}')
    plt.close(fig)

    # Print verification table
    print('\n=== Gain data verification (D004: fair = naive + {:.3f} dB) ==='.format(PILOT_OVERHEAD))
    print(f'{"Scene":<18} {"fair":>7} {"naive":>7} {"naive_CI95":>16}')
    for i, s in enumerate(SCENES):
        d = data[i]
        ci_str = f'[{d["naive_ci"][0]:+.2f}, {d["naive_ci"][1]:+.2f}]'
        sell = ' <<<' if i in SELLING_IDX else ''
        print(f'{s:<18} {d["fair_mean"]:>+7.2f} {d["naive_mean"]:>+7.2f} {ci_str:>16}{sell}')


if __name__ == '__main__':
    main()
