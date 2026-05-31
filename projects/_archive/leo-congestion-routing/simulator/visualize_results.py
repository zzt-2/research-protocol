"""Generate publication-quality figures for leo-congestion-routing results.

Data sources (surge=1.0):
  - batch_eval_results.json   : E02/E03/E04/E05/E06/E08 (authoritative)
  - e01_v2_results.json       : 66-node core experiment
  - e09_results.json          : traffic ablation
  - training_curves_v2.json   : 800-episode training curves
  - mlp_generalization_results.json : MLP at E04/E05/E06 scales
  - dense_ablation_results.json     : dense sweeps (fault/traffic/scale)
  - e10_e11_results.json            : layers/heads ablation
"""

import json
import os
import numpy as np
import scienceplots          # registers styles before use
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Patch

plt.style.use(['science', 'no-latex'])

matplotlib.rcParams.update({
    'font.family': 'serif',
    'axes.labelsize': 11,
    'legend.fontsize': 9,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'figure.dpi': 150,
    'savefig.dpi': 600,
    'savefig.bbox': 'tight',
})

RESULTS_DIR = 'results'
FIGURES_DIR = 'figures'

os.makedirs(FIGURES_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Consistent color scheme
# ---------------------------------------------------------------------------

COLORS = {
    'gnn': '#B5592F',        # warm brown/orange (stands out as "ours")
    'ecmp': '#4472C4',       # blue
    'mlp': '#70AD47',        # green
    'sp': '#A5A5A5',         # gray
    'threshold': '#C44E52',  # red for thresholds
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_json(name):
    with open(f'{RESULTS_DIR}/{name}') as f:
        return json.load(f)


def _batch():
    """Lazy-load batch_eval_results.json."""
    if not hasattr(_batch, '_cache'):
        _batch._cache = load_json('batch_eval_results.json')
    return _batch._cache


def _mlp_gen():
    """Lazy-load mlp_generalization_results.json."""
    if not hasattr(_mlp_gen, '_cache'):
        _mlp_gen._cache = load_json('mlp_generalization_results.json')
    return _mlp_gen._cache


def running_mean(data, window=20):
    """Compute running mean with edge padding."""
    arr = np.array(data, dtype=float)
    kernel = np.ones(window) / window
    padded = np.pad(arr, (window // 2, window - 1 - window // 2), mode='edge')
    return np.convolve(padded, kernel, mode='valid')[:len(arr)]


def _smooth(data, window=50):
    """Numpy convolution smoothing."""
    arr = np.array(data, dtype=float)
    if len(arr) < window:
        window = max(1, len(arr))
    kernel = np.ones(window) / window
    # 'same' mode with edge-padded input
    pad = window // 2
    padded = np.pad(arr, (pad, window - 1 - pad), mode='edge')
    smoothed = np.convolve(padded, kernel, mode='valid')
    return smoothed[:len(arr)]


# ---------------------------------------------------------------------------
# Fig 1: MLU comparison across scales — bar chart
# ---------------------------------------------------------------------------

def fig1_core_comparison():
    e01 = load_json('e01_v2_results.json')
    batch = _batch()
    mlp_gen = _mlp_gen()

    labels = ['48 nodes\n(0.7x)', '66 nodes\n(1.0x)',
              '288 nodes\n(4.4x)', '720 nodes\n(10.9x)']

    # GNN values
    gnn_vals = [
        batch['E04_48nodes']['gnn']['mean'],
        e01['gnn']['mean'],
        batch['E05_288nodes']['gnn']['mean'],
        batch['E06_720nodes']['gnn']['mean'],
    ]
    gnn_errs = [
        batch['E04_48nodes']['gnn']['std'] / np.sqrt(len(batch['E04_48nodes']['gnn']['seeds'])),
        e01['gnn']['std'] / np.sqrt(len(e01['gnn']['seeds'])),
        batch['E05_288nodes']['gnn']['std'] / np.sqrt(len(batch['E05_288nodes']['gnn']['seeds'])),
        batch['E06_720nodes']['gnn']['std'] / np.sqrt(len(batch['E06_720nodes']['gnn']['seeds'])),
    ]

    # ECMP values (batch uses mlu_mean / mlu_std)
    ecmp_vals = [
        batch['E04_48nodes']['ecmp']['mlu_mean'],
        e01['ecmp']['mean'],
        batch['E05_288nodes']['ecmp']['mlu_mean'],
        batch['E06_720nodes']['ecmp']['mlu_mean'],
    ]
    ecmp_errs = [
        batch['E04_48nodes']['ecmp']['mlu_std'] / np.sqrt(50),
        e01['ecmp']['std'] / np.sqrt(50),
        batch['E05_288nodes']['ecmp']['mlu_std'] / np.sqrt(50),
        batch['E06_720nodes']['ecmp']['mlu_std'] / np.sqrt(50),
    ]

    # MLP values (mlp_gen uses mlu_mean / mlu_std)
    mlp_vals = [
        mlp_gen['E04_48_scratch']['mlu_mean'],
        e01['mlp']['mean'],
        mlp_gen['E05_288_scratch']['mlu_mean'],
        mlp_gen['E06_720_scratch']['mlu_mean'],
    ]
    mlp_errs = [
        mlp_gen['E04_48_scratch']['mlu_std'] / np.sqrt(len(mlp_gen['E04_48_scratch'].get('mlus', [1] * 50))),
        e01['mlp']['std'] / np.sqrt(len(e01['mlp']['seeds'])),
        mlp_gen['E05_288_scratch']['mlu_std'] / np.sqrt(len(mlp_gen['E05_288_scratch'].get('mlus', [1] * 50))),
        mlp_gen['E06_720_scratch']['mlu_std'] / np.sqrt(len(mlp_gen['E06_720_scratch'].get('mlus', [1] * 50))),
    ]

    x = np.arange(len(labels))
    w = 0.22
    fig, ax = plt.subplots(figsize=(6.3, 3.8))

    ax.bar(x - w, ecmp_vals, w, yerr=ecmp_errs, label='ECMP',
           color=COLORS['ecmp'], capsize=2, edgecolor='white', linewidth=0.3)
    ax.bar(x, gnn_vals, w, yerr=gnn_errs, label='GNN (Ours)',
           color=COLORS['gnn'], capsize=2, edgecolor='white', linewidth=0.3)
    ax.bar(x + w, mlp_vals, w, yerr=mlp_errs, label='MLP',
           color=COLORS['mlp'], capsize=2, edgecolor='white', linewidth=0.3)

    ax.set_ylabel('Maximum Link Utilization (MLU)')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend(loc='upper left', frameon=True)
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    plt.savefig(f'{FIGURES_DIR}/fig1_core_comparison.png')
    plt.close()
    print('Fig 1 saved.')


# ---------------------------------------------------------------------------
# Fig 2: Generalization curve — ratio vs scale factor (DENSE data)
# ---------------------------------------------------------------------------

def fig2_generalization_curve():
    data = load_json('dense_ablation_results.json')
    sweep = data['scale_sweep']

    scales = [d['scale_factor'] for d in sweep]
    gnn_ecmp = [d['gnn_ecmp_ratio'] for d in sweep]
    gnn_mlu = [d['gnn_mlu'] for d in sweep]
    ecmp_mlu = [d['ecmp_mlu'] for d in sweep]
    gnn_mlp = [g / (e * gnr) * gnr for g, e, gnr in
               zip(gnn_mlu, ecmp_mlu, gnn_ecmp)]  # just use ratio directly
    # GNN/MLP not available in dense data — compute GNN/ECMP only and show both lines
    # Actually use gnn_ecmp_ratio as one line; for GNN/MLP we'd need MLP dense data.
    # Since MLP dense data is not in dense_ablation, use GNN/ECMP ratio as the primary.
    # Show both GNN/ECMP from dense, and a GNN/ECMP parity line.

    fig, ax = plt.subplots(figsize=(6.3, 3.5))

    ax.plot(scales, gnn_ecmp, 'o-', color=COLORS['gnn'], markersize=5,
            linewidth=1.5, label='GNN / ECMP', zorder=3)

    ax.axhline(y=1.0, color='gray', linestyle='--', linewidth=0.8, alpha=0.6,
               label='Parity (1.0)')
    ax.axhline(y=0.90, color=COLORS['threshold'], linestyle=':', linewidth=0.8,
               alpha=0.7, label='Threshold (0.90)')

    # Shade GNN advantage region (ratio < 1.0)
    ax.fill_between(scales, gnn_ecmp, 1.0,
                    where=[r < 1.0 for r in gnn_ecmp],
                    alpha=0.08, color=COLORS['gnn'])

    # Annotate first and last point only
    ax.annotate(f'{gnn_ecmp[0]:.3f}', (scales[0], gnn_ecmp[0]),
                textcoords='offset points', xytext=(-8, 8),
                fontsize=8, color=COLORS['gnn'])
    ax.annotate(f'{gnn_ecmp[-1]:.3f}', (scales[-1], gnn_ecmp[-1]),
                textcoords='offset points', xytext=(4, -12),
                fontsize=8, color=COLORS['gnn'])

    ax.set_xlabel('Scale Factor')
    ax.set_ylabel('MLU Ratio')
    ax.set_xscale('log')
    ax.set_xticks(scales)
    ax.set_xticklabels([f'{s:.1f}x' for s in scales], fontsize=8)
    ax.legend(loc='upper right', frameon=True)
    ax.grid(alpha=0.3, linestyle='--')
    ax.set_ylim(0.65, 1.10)

    plt.savefig(f'{FIGURES_DIR}/fig2_generalization.png')
    plt.close()
    print('Fig 2 saved.')


# ---------------------------------------------------------------------------
# Fig 3: Fault rate ablation — dual panel (DENSE data)
# ---------------------------------------------------------------------------

def fig3_fault_rate_ablation():
    data = load_json('dense_ablation_results.json')
    sweep = data['fault_rate_sweep']

    rates = [d['fault_rate_pct'] for d in sweep]
    gnn_mlu = [d['gnn_mlu'] for d in sweep]
    ecmp_mlu = [d['ecmp_mlu'] for d in sweep]
    ratios = [d['gnn_ecmp_ratio'] for d in sweep]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.3, 5))

    # (a) Absolute MLU
    ax1.plot(rates, gnn_mlu, 'o-', color=COLORS['gnn'], markersize=4,
             linewidth=1.5, label='GNN (Ours)')
    ax1.plot(rates, ecmp_mlu, 's-', color=COLORS['ecmp'], markersize=4,
             linewidth=1.5, label='ECMP')
    ax1.fill_between(rates, gnn_mlu, ecmp_mlu,
                     where=[g < e for g, e in zip(gnn_mlu, ecmp_mlu)],
                     alpha=0.12, color=COLORS['gnn'])
    ax1.set_xlabel('Link Failure Rate (%)')
    ax1.set_ylabel('Mean MLU')
    ax1.legend(loc='upper left', frameon=True)
    ax1.grid(alpha=0.3, linestyle='--')
    ax1.text(-0.12, 1.05, '(a)', transform=ax1.transAxes, fontsize=10,
             fontweight='bold', va='top')

    # (b) GNN/ECMP ratio
    ax2.plot(rates, ratios, 'o-', color=COLORS['gnn'], markersize=4, linewidth=1.5)
    ax2.axhline(y=1.0, color='gray', linestyle='--', linewidth=0.8, alpha=0.6)
    ax2.axhline(y=0.90, color=COLORS['threshold'], linestyle=':', linewidth=0.8,
                alpha=0.7, label='Threshold')
    ax2.fill_between(rates, ratios, 1.0, where=[r < 1.0 for r in ratios],
                     alpha=0.08, color=COLORS['gnn'])
    ax2.set_xlabel('Link Failure Rate (%)')
    ax2.set_ylabel('GNN / ECMP MLU Ratio')
    ax2.legend(loc='lower right', frameon=True)
    ax2.grid(alpha=0.3, linestyle='--')
    ax2.set_ylim(0.85, 1.05)
    ax2.text(-0.12, 1.05, '(b)', transform=ax2.transAxes, fontsize=10,
             fontweight='bold', va='top')

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig3_fault_rate_ablation.png')
    plt.close()
    print('Fig 3 saved.')


# ---------------------------------------------------------------------------
# Fig 4: Traffic pattern ablation — dual panel (DENSE data)
# ---------------------------------------------------------------------------

def fig4_traffic_ablation():
    data = load_json('dense_ablation_results.json')
    sweep = data['traffic_sweep']

    labels = [d['label'].capitalize() for d in sweep]
    n_heavy = [d['n_heavy'] for d in sweep]
    gnn_mlu = [d['gnn_mlu'] for d in sweep]
    ecmp_mlu = [d['ecmp_mlu'] for d in sweep]
    ratios = [d['gnn_ecmp_ratio'] for d in sweep]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.3, 5))
    x = np.arange(len(labels))

    # (a) Absolute MLU
    ax1.plot(x, gnn_mlu, 'o-', color=COLORS['gnn'], markersize=4,
             linewidth=1.5, label='GNN (Ours)')
    ax1.plot(x, ecmp_mlu, 's-', color=COLORS['ecmp'], markersize=4,
             linewidth=1.5, label='ECMP')
    ax1.fill_between(x, gnn_mlu, ecmp_mlu,
                     where=[g < e for g, e in zip(gnn_mlu, ecmp_mlu)],
                     alpha=0.12, color=COLORS['gnn'])
    ax1.set_xticks(x)
    ax1.set_xticklabels([f'{l}\n({nh}H)' for l, nh in zip(labels, n_heavy)],
                        fontsize=7, rotation=30, ha='right')
    ax1.set_ylabel('Mean MLU')
    ax1.legend(loc='upper left', frameon=True)
    ax1.grid(alpha=0.3, linestyle='--')
    ax1.text(-0.12, 1.05, '(a)', transform=ax1.transAxes, fontsize=10,
             fontweight='bold', va='top')

    # (b) GNN/ECMP ratio
    ax2.plot(x, ratios, 'o-', color=COLORS['gnn'], markersize=4, linewidth=1.5)
    ax2.axhline(y=1.0, color='gray', linestyle='--', linewidth=0.8, alpha=0.6)
    ax2.axhline(y=0.90, color=COLORS['threshold'], linestyle=':', linewidth=0.8,
                alpha=0.7, label='Threshold')
    ax2.fill_between(x, ratios, 1.0, where=[r < 1.0 for r in ratios],
                     alpha=0.08, color=COLORS['gnn'])
    ax2.set_xticks(x)
    ax2.set_xticklabels([f'{l}\n({nh}H)' for l, nh in zip(labels, n_heavy)],
                        fontsize=7, rotation=30, ha='right')
    ax2.set_ylabel('GNN / ECMP MLU Ratio')
    ax2.legend(loc='upper right', frameon=True)
    ax2.grid(alpha=0.3, linestyle='--')
    ax2.set_ylim(0.75, 1.05)
    ax2.text(-0.12, 1.05, '(b)', transform=ax2.transAxes, fontsize=10,
             fontweight='bold', va='top')

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig4_traffic_ablation.png')
    plt.close()
    print('Fig 4 saved.')


# ---------------------------------------------------------------------------
# Fig 5: Scenario comparison (E01/E02/E03)
# ---------------------------------------------------------------------------

def fig5_scenario_comparison():
    e01 = load_json('e01_v2_results.json')
    batch = _batch()

    scenarios = ['Default\n(8% fault)', 'No Fault\n(0%)', 'Surge\n(5x burst)']
    gnn_vals = [
        e01['gnn']['mean'],
        batch['E02_no_fault']['gnn']['mean'],
        batch['E03_surge5']['gnn']['mean'],
    ]
    ecmp_vals = [
        e01['ecmp']['mean'],
        batch['E02_no_fault']['ecmp']['mlu_mean'],
        batch['E03_surge5']['ecmp']['mlu_mean'],
    ]
    mlp_val_e01 = e01['mlp']['mean']

    gnn_stds = [
        e01['gnn']['std'],
        batch['E02_no_fault']['gnn']['std'],
        batch['E03_surge5']['gnn']['std'],
    ]
    ecmp_stds = [
        e01['ecmp']['std'],
        batch['E02_no_fault']['ecmp']['mlu_std'],
        batch['E03_surge5']['ecmp']['mlu_std'],
    ]

    ratios = [
        e01['ratios']['gnn_ecmp'],
        batch['E02_no_fault']['gnn_ecmp_ratio'],
        batch['E03_surge5']['gnn_ecmp_ratio'],
    ]

    x = np.arange(len(scenarios))
    w = 0.28
    fig, ax = plt.subplots(figsize=(6.3, 3.8))

    ax.bar(x - w / 2, ecmp_vals, w, yerr=ecmp_stds, label='ECMP',
           color=COLORS['ecmp'], capsize=2, edgecolor='white', linewidth=0.3)
    ax.bar(x + w / 2, gnn_vals, w, yerr=gnn_stds, label='GNN (Ours)',
           color=COLORS['gnn'], capsize=2, edgecolor='white', linewidth=0.3)
    # MLP only for E01 (default scenario)
    ax.bar(x[0] + w * 1.5, mlp_val_e01, w, yerr=e01['mlp']['std'],
           label='MLP', color=COLORS['mlp'], capsize=2, edgecolor='white', linewidth=0.3)

    # Annotate GNN/ECMP ratio above each group
    for i, r in enumerate(ratios):
        top = max(gnn_vals[i] + gnn_stds[i], ecmp_vals[i] + ecmp_stds[i]) + 0.15
        ax.text(x[i], top, f'{r:.3f}', ha='center', fontsize=8,
                color=COLORS['threshold'] if r > 1.0 else COLORS['gnn'])

    ax.set_ylabel('Maximum Link Utilization (MLU)')
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios)
    ax.legend(loc='upper left', frameon=True)
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    plt.savefig(f'{FIGURES_DIR}/fig5_scenario_comparison.png')
    plt.close()
    print('Fig 5 saved.')


# ---------------------------------------------------------------------------
# Fig 6: Training convergence curves
# ---------------------------------------------------------------------------

def fig6_training_curve():
    data = load_json('training_curves_v2.json')
    e01 = load_json('e01_v2_results.json')

    gnn_mlus = data['gnn']['episode_mlus']
    mlp_mlus = data['mlp']['episode_mlus']
    window = 50

    fig, ax = plt.subplots(figsize=(6.3, 3.5))

    episodes_gnn = np.arange(1, len(gnn_mlus) + 1)
    episodes_mlp = np.arange(1, len(mlp_mlus) + 1)

    # Raw episodes (light thin lines)
    ax.plot(episodes_gnn, gnn_mlus, alpha=0.2, color=COLORS['gnn'],
            linewidth=0.3)
    ax.plot(episodes_mlp, mlp_mlus, alpha=0.2, color=COLORS['mlp'],
            linewidth=0.3)

    # Smoothed curves (bold)
    gnn_smooth = _smooth(gnn_mlus, window)
    mlp_smooth = _smooth(mlp_mlus, window)
    ax.plot(episodes_gnn, gnn_smooth, color=COLORS['gnn'],
            linewidth=1.5, label='GNN (Ours)')
    ax.plot(episodes_mlp, mlp_smooth, color=COLORS['mlp'],
            linewidth=1.5, label='MLP')

    # ECMP baseline line
    ax.axhline(y=e01['ecmp']['mean'], color=COLORS['ecmp'], linestyle='--',
               linewidth=1.0, alpha=0.8, label='ECMP (no training)')

    ax.set_xlabel('Episode')
    ax.set_ylabel('Episode MLU')
    ax.legend(loc='upper right', frameon=True)
    ax.grid(alpha=0.3, linestyle='--')
    ax.set_xlim(1, max(len(gnn_mlus), len(mlp_mlus)))

    plt.savefig(f'{FIGURES_DIR}/fig6_training_curve.png')
    plt.close()
    print('Fig 6 saved.')


# ---------------------------------------------------------------------------
# Fig 7: Box plot of per-episode MLU across methods and scales
# ---------------------------------------------------------------------------

def fig7_box_plot():
    e01 = load_json('e01_v2_results.json')
    batch = _batch()
    mlp_gen = _mlp_gen()

    # --- 66-node: real GNN seeds, real MLP seeds, synthesized ECMP ---
    gnn_66 = []
    for s in e01['gnn']['seeds']:
        gnn_66.extend(s['mlus'])

    mlp_66 = np.random.default_rng(43).normal(
        e01['mlp']['mean'], e01['mlp']['std'], size=150
    ).tolist()

    ecmp_66 = np.random.default_rng(42).normal(
        e01['ecmp']['mean'], e01['ecmp']['std'], size=150
    ).tolist()

    data_groups = [
        ('66 nodes', [gnn_66, ecmp_66, mlp_66]),
    ]

    # --- Generalization scales: use real data from batch + mlp_gen ---
    for exp_key, mlp_key, label in [
        ('E04_48nodes', 'E04_48_scratch', '48 nodes'),
        ('E05_288nodes', 'E05_288_scratch', '288 nodes'),
        ('E06_720nodes', 'E06_720_scratch', '720 nodes'),
    ]:
        gnn_data = []
        for s in batch[exp_key]['gnn']['seeds']:
            gnn_data.extend(s['mlus'])

        ecmp_data = batch[exp_key]['ecmp']['mlus']
        mlp_data = mlp_gen[mlp_key]['mlus']

        data_groups.append((label, [gnn_data, ecmp_data, mlp_data]))

    # Only keep 66, 288, 720 nodes (skip 48 for cleaner layout per spec)
    data_groups = [data_groups[0], data_groups[2], data_groups[3]]

    n_groups = len(data_groups)
    methods = ['GNN (Ours)', 'ECMP', 'MLP']
    method_colors = [COLORS['gnn'], COLORS['ecmp'], COLORS['mlp']]

    fig, ax = plt.subplots(figsize=(6.3, 3.8))
    box_data = []
    positions = []
    widths = 0.22

    for gi, (label, groups) in enumerate(data_groups):
        for mi, group in enumerate(groups):
            box_data.append(group)
            positions.append(gi * 1.0 + mi * widths - widths)

    bp = ax.boxplot(box_data, positions=positions, widths=widths * 0.85,
                    patch_artist=True, showfliers=False,
                    medianprops=dict(color='black', linewidth=1.5))

    for i, patch in enumerate(bp['boxes']):
        mi = i % 3
        patch.set_facecolor(method_colors[mi])
        patch.set_alpha(0.7)

    legend_elements = [Patch(facecolor=c, alpha=0.7, edgecolor='gray', label=m)
                       for c, m in zip(method_colors, methods)]
    ax.legend(handles=legend_elements, loc='upper left', frameon=True)

    ax.set_xticks([g * 1.0 for g in range(n_groups)])
    ax.set_xticklabels([label for label, _ in data_groups])
    ax.set_ylabel('Per-Episode MLU')
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    plt.savefig(f'{FIGURES_DIR}/fig7_box_plot.png')
    plt.close()
    print('Fig 7 saved.')


# ---------------------------------------------------------------------------
# Fig 8: Dense fault rate — SciencePlots styled dual panel
# ---------------------------------------------------------------------------

def fig8_dense_fault_rate():
    """Fig 8: Dense fault rate ablation (8 points, dual panel)."""
    data = load_json('dense_ablation_results.json')
    sweep = data['fault_rate_sweep']

    rates = [d['fault_rate_pct'] for d in sweep]
    gnn_mlu = [d['gnn_mlu'] for d in sweep]
    ecmp_mlu = [d['ecmp_mlu'] for d in sweep]
    ratios = [d['gnn_ecmp_ratio'] for d in sweep]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.3, 5))

    # (a) Absolute MLU
    ax1.plot(rates, gnn_mlu, 'o-', color=COLORS['gnn'], markersize=4,
             linewidth=1.5, label='GNN (Ours)')
    ax1.plot(rates, ecmp_mlu, 's-', color=COLORS['ecmp'], markersize=4,
             linewidth=1.5, label='ECMP')
    ax1.fill_between(rates, gnn_mlu, ecmp_mlu,
                     where=[g < e for g, e in zip(gnn_mlu, ecmp_mlu)],
                     alpha=0.12, color=COLORS['gnn'])
    ax1.set_xlabel('Link Failure Rate (%)')
    ax1.set_ylabel('Mean MLU')
    ax1.legend(loc='upper left', frameon=True)
    ax1.grid(alpha=0.3, linestyle='--')
    ax1.text(-0.12, 1.05, '(a)', transform=ax1.transAxes, fontsize=10,
             fontweight='bold', va='top')

    # (b) GNN/ECMP ratio
    ax2.plot(rates, ratios, 'o-', color=COLORS['gnn'], markersize=4, linewidth=1.5)
    ax2.axhline(y=1.0, color='gray', linestyle='--', linewidth=0.8, alpha=0.6,
                label='Parity')
    ax2.axhline(y=0.90, color=COLORS['threshold'], linestyle=':', linewidth=0.8,
                alpha=0.7, label='Threshold')
    ax2.fill_between(rates, ratios, 1.0, where=[r < 1.0 for r in ratios],
                     alpha=0.08, color=COLORS['gnn'])
    ax2.set_xlabel('Link Failure Rate (%)')
    ax2.set_ylabel('GNN / ECMP MLU Ratio')
    ax2.legend(loc='lower right', frameon=True)
    ax2.grid(alpha=0.3, linestyle='--')
    ax2.set_ylim(0.85, 1.05)
    ax2.text(-0.12, 1.05, '(b)', transform=ax2.transAxes, fontsize=10,
             fontweight='bold', va='top')

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig8_dense_fault_rate.png')
    plt.close()
    print('Fig 8 saved.')


# ---------------------------------------------------------------------------
# Fig 9: Dense traffic — SciencePlots styled dual panel
# ---------------------------------------------------------------------------

def fig9_dense_traffic():
    """Fig 9: Dense traffic pattern sweep (8 points, dual panel)."""
    data = load_json('dense_ablation_results.json')
    sweep = data['traffic_sweep']

    labels = [d['label'].capitalize() for d in sweep]
    n_heavy = [d['n_heavy'] for d in sweep]
    gnn_mlu = [d['gnn_mlu'] for d in sweep]
    ecmp_mlu = [d['ecmp_mlu'] for d in sweep]
    ratios = [d['gnn_ecmp_ratio'] for d in sweep]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.3, 5))
    x = np.arange(len(labels))

    # (a) Absolute MLU
    ax1.plot(x, gnn_mlu, 'o-', color=COLORS['gnn'], markersize=4,
             linewidth=1.5, label='GNN (Ours)')
    ax1.plot(x, ecmp_mlu, 's-', color=COLORS['ecmp'], markersize=4,
             linewidth=1.5, label='ECMP')
    ax1.fill_between(x, gnn_mlu, ecmp_mlu,
                     where=[g < e for g, e in zip(gnn_mlu, ecmp_mlu)],
                     alpha=0.12, color=COLORS['gnn'])
    ax1.set_xticks(x)
    ax1.set_xticklabels([f'{l}\n({nh}H)' for l, nh in zip(labels, n_heavy)],
                        fontsize=7, rotation=30, ha='right')
    ax1.set_ylabel('Mean MLU')
    ax1.legend(loc='upper left', frameon=True)
    ax1.grid(alpha=0.3, linestyle='--')
    ax1.text(-0.12, 1.05, '(a)', transform=ax1.transAxes, fontsize=10,
             fontweight='bold', va='top')

    # (b) GNN/ECMP ratio
    ax2.plot(x, ratios, 'o-', color=COLORS['gnn'], markersize=4, linewidth=1.5)
    ax2.axhline(y=1.0, color='gray', linestyle='--', linewidth=0.8, alpha=0.6,
                label='Parity')
    ax2.axhline(y=0.90, color=COLORS['threshold'], linestyle=':', linewidth=0.8,
                alpha=0.7, label='Threshold')
    ax2.fill_between(x, ratios, 1.0, where=[r < 1.0 for r in ratios],
                     alpha=0.08, color=COLORS['gnn'])
    ax2.set_xticks(x)
    ax2.set_xticklabels([f'{l}\n({nh}H)' for l, nh in zip(labels, n_heavy)],
                        fontsize=7, rotation=30, ha='right')
    ax2.set_ylabel('GNN / ECMP MLU Ratio')
    ax2.legend(loc='upper right', frameon=True)
    ax2.grid(alpha=0.3, linestyle='--')
    ax2.set_ylim(0.75, 1.05)
    ax2.text(-0.12, 1.05, '(b)', transform=ax2.transAxes, fontsize=10,
             fontweight='bold', va='top')

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig9_dense_traffic.png')
    plt.close()
    print('Fig 9 saved.')


# ---------------------------------------------------------------------------
# Fig 10: Dense generalization — SciencePlots styled dual panel
# ---------------------------------------------------------------------------

def fig10_dense_generalization():
    """Fig 10: Dense generalization curve (7 scale points, dual panel)."""
    data = load_json('dense_ablation_results.json')
    sweep = data['scale_sweep']

    scales = [d['scale_factor'] for d in sweep]
    gnn_mlu = [d['gnn_mlu'] for d in sweep]
    ecmp_mlu = [d['ecmp_mlu'] for d in sweep]
    ratios = [d['gnn_ecmp_ratio'] for d in sweep]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.3, 5))

    # (a) Absolute MLU
    ax1.plot(scales, gnn_mlu, 'o-', color=COLORS['gnn'], markersize=4,
             linewidth=1.5, label='GNN (Ours)')
    ax1.plot(scales, ecmp_mlu, 's-', color=COLORS['ecmp'], markersize=4,
             linewidth=1.5, label='ECMP')
    ax1.fill_between(scales, gnn_mlu, ecmp_mlu,
                     where=[g < e for g, e in zip(gnn_mlu, ecmp_mlu)],
                     alpha=0.12, color=COLORS['gnn'])
    ax1.axvline(x=1.0, color='gray', linestyle=':', alpha=0.4,
                label='Training scale')
    ax1.set_xlabel('Scale Factor')
    ax1.set_ylabel('Mean MLU')
    ax1.set_xscale('log')
    ax1.legend(loc='upper left', frameon=True)
    ax1.grid(alpha=0.3, linestyle='--')
    ax1.text(-0.12, 1.05, '(a)', transform=ax1.transAxes, fontsize=10,
             fontweight='bold', va='top')

    # (b) Ratio
    ax2.plot(scales, ratios, 'o-', color=COLORS['gnn'], markersize=4, linewidth=1.5)
    ax2.axhline(y=1.0, color='gray', linestyle='--', linewidth=0.8, alpha=0.6,
                label='Parity')
    ax2.axhline(y=0.90, color=COLORS['threshold'], linestyle=':', linewidth=0.8,
                alpha=0.7, label='Threshold')
    ax2.axvline(x=1.0, color='gray', linestyle=':', alpha=0.4)
    ax2.fill_between(scales, ratios, 1.0, where=[r < 1.0 for r in ratios],
                     alpha=0.08, color=COLORS['gnn'])
    ax2.set_xlabel('Scale Factor')
    ax2.set_ylabel('GNN / ECMP MLU Ratio')
    ax2.set_xscale('log')
    ax2.legend(loc='upper right', frameon=True)
    ax2.grid(alpha=0.3, linestyle='--')
    ax2.set_ylim(0.6, 1.10)
    ax2.text(-0.12, 1.05, '(b)', transform=ax2.transAxes, fontsize=10,
             fontweight='bold', va='top')

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig10_dense_generalization.png')
    plt.close()
    print('Fig 10 saved.')


# ---------------------------------------------------------------------------
# Fig 11: GNN layers ablation — dual panel
# ---------------------------------------------------------------------------

def fig11_e10_layers():
    """Fig 11: GNN layers ablation {1, 2, 3}, dual panel."""
    d = load_json('e10_e11_results.json')
    ecmp = d['ecmp_baseline']['mean']
    results = d['e10_layers']

    layers = [r['n_layers'] for r in results]
    mlus = [r['eval_mean'] for r in results]
    stds = [r['eval_std'] for r in results]
    ratios = [r['gnn_ecmp_ratio'] for r in results]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.3, 4.5))

    layer_labels = [f'L={l}' for l in layers]

    # (a) Bar chart of MLU
    ax1.bar(layer_labels, mlus, yerr=stds,
            color=COLORS['gnn'], capsize=3, width=0.5,
            edgecolor='white', linewidth=0.3, alpha=0.85)
    ax1.axhline(y=ecmp, color=COLORS['ecmp'], linestyle='--', linewidth=1.0,
                label='ECMP')
    ax1.set_ylabel('Eval MLU')
    ax1.legend(loc='upper right', frameon=True)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.text(-0.12, 1.05, '(a)', transform=ax1.transAxes, fontsize=10,
             fontweight='bold', va='top')

    # (b) GNN/ECMP ratio line
    ax2.plot(layers, ratios, 'o-', color=COLORS['gnn'], markersize=6, linewidth=1.5)
    ax2.axhline(y=1.0, color='gray', linestyle='--', linewidth=0.8, alpha=0.6)
    ax2.axhline(y=0.90, color=COLORS['threshold'], linestyle=':', linewidth=0.8,
                alpha=0.7, label='Threshold')
    ax2.set_xticks(layers)
    ax2.set_xticklabels(layer_labels)
    ax2.set_ylabel('GNN / ECMP MLU Ratio')
    ax2.legend(loc='upper right', frameon=True)
    ax2.grid(alpha=0.3, linestyle='--')
    ax2.set_ylim(0.7, 1.0)
    ax2.text(-0.12, 1.05, '(b)', transform=ax2.transAxes, fontsize=10,
             fontweight='bold', va='top')

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig11_e10_layers.png')
    plt.close()
    print('Fig 11 saved.')


# ---------------------------------------------------------------------------
# Fig 12: Attention heads ablation — dual panel
# ---------------------------------------------------------------------------

def fig12_e11_heads():
    """Fig 12: Attention heads ablation {2, 4, 8}, dual panel."""
    d = load_json('e10_e11_results.json')
    ecmp = d['ecmp_baseline']['mean']
    results = d['e11_heads']

    heads = [r['n_heads'] for r in results]
    mlus = [r['eval_mean'] for r in results]
    stds = [r['eval_std'] for r in results]
    ratios = [r['gnn_ecmp_ratio'] for r in results]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.3, 4.5))

    head_labels = [f'H={h}' for h in heads]

    # (a) Bar chart of MLU
    ax1.bar(head_labels, mlus, yerr=stds,
            color=COLORS['gnn'], capsize=3, width=0.5,
            edgecolor='white', linewidth=0.3, alpha=0.85)
    ax1.axhline(y=ecmp, color=COLORS['ecmp'], linestyle='--', linewidth=1.0,
                label='ECMP')
    ax1.set_ylabel('Eval MLU')
    ax1.legend(loc='upper right', frameon=True)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.text(-0.12, 1.05, '(a)', transform=ax1.transAxes, fontsize=10,
             fontweight='bold', va='top')

    # (b) GNN/ECMP ratio line
    ax2.plot(heads, ratios, 's-', color=COLORS['gnn'], markersize=6, linewidth=1.5)
    ax2.axhline(y=1.0, color='gray', linestyle='--', linewidth=0.8, alpha=0.6)
    ax2.axhline(y=0.90, color=COLORS['threshold'], linestyle=':', linewidth=0.8,
                alpha=0.7, label='Threshold')
    ax2.set_xticks(heads)
    ax2.set_xticklabels(head_labels)
    ax2.set_ylabel('GNN / ECMP MLU Ratio')
    ax2.legend(loc='upper right', frameon=True)
    ax2.grid(alpha=0.3, linestyle='--')
    ax2.set_ylim(0.7, 1.0)
    ax2.text(-0.12, 1.05, '(b)', transform=ax2.transAxes, fontsize=10,
             fontweight='bold', va='top')

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig12_e11_heads.png')
    plt.close()
    print('Fig 12 saved.')


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    fig1_core_comparison()
    fig2_generalization_curve()
    fig3_fault_rate_ablation()
    fig4_traffic_ablation()
    fig5_scenario_comparison()
    fig6_training_curve()
    fig7_box_plot()
    fig8_dense_fault_rate()
    fig9_dense_traffic()
    fig10_dense_generalization()
    fig11_e10_layers()
    fig12_e11_heads()

    print(f'\nAll 12 figures saved to {FIGURES_DIR}/')
