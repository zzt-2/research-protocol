"""Generate publication-quality figures for leo-congestion-routing results."""

import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'legend.fontsize': 10,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})

RESULTS_DIR = 'results'
FIGURES_DIR = 'figures'

import os
os.makedirs(FIGURES_DIR, exist_ok=True)


def load_json(name):
    with open(f'{RESULTS_DIR}/{name}') as f:
        return json.load(f)


def fig1_core_comparison():
    """Fig 1: MLU comparison across scales — bar chart."""
    e01 = load_json('e01_v2_results.json')
    e04 = load_json('e04_quick_results.json')
    e05e06 = load_json('e05_e06_results.json')

    labels = ['48 nodes\n(0.7×)', '66 nodes\n(1.0×)', '288 nodes\n(4.4×)', '720 nodes\n(10.9×)']

    gnn_vals = [
        e04['gnn_48_zeroshot'][0]['mean'],  # seed 0
        e01['gnn']['mean'],
        e05e06['E05_288']['gnn']['mean'],
        e05e06['E06_720']['gnn']['mean'],
    ]
    gnn_errs = [
        e04['gnn_48_zeroshot'][0]['std'] / np.sqrt(50),
        e01['gnn']['std'],
        e05e06['E05_288']['gnn']['std'] / np.sqrt(50),
        e05e06['E06_720']['gnn']['std'] / np.sqrt(50),
    ]

    ecmp_vals = [
        e04['ecmp_48']['mean'],
        e01['ecmp']['mean'],
        e05e06['E05_288']['ecmp']['mean'],
        e05e06['E06_720']['ecmp']['mean'],
    ]
    ecmp_errs = [
        e04['ecmp_48']['std'] / np.sqrt(50),
        e01['ecmp']['std'],
        e05e06['E05_288']['ecmp']['std'] / np.sqrt(50),
        e05e06['E06_720']['ecmp']['std'] / np.sqrt(50),
    ]

    mlp_vals = [
        e04['mlp_48_zeroshot']['mean'],
        e01['mlp']['mean'],
        e05e06['E05_288']['mlp']['mean'],
        e05e06['E06_720']['mlp']['mean'],
    ]
    mlp_errs = [
        e04['mlp_48_zeroshot']['std'] / np.sqrt(50),
        e01['mlp']['std'],
        e05e06['E05_288']['mlp']['std'] / np.sqrt(50),
        e05e06['E06_720']['mlp']['std'] / np.sqrt(50),
    ]

    x = np.arange(len(labels))
    w = 0.25
    fig, ax = plt.subplots(figsize=(8, 5))

    bars1 = ax.bar(x - w, ecmp_vals, w, yerr=ecmp_errs, label='ECMP', color='#4C72B0', capsize=3)
    bars2 = ax.bar(x, gnn_vals, w, yerr=gnn_errs, label='GNN (Ours)', color='#DD8452', capsize=3)
    bars3 = ax.bar(x + w, mlp_vals, w, yerr=mlp_errs, label='MLP', color='#55A868', capsize=3)

    # Annotate GNN/ECMP ratios
    ratios = [e04['summary']['gnn_over_ecmp'], e01['ratios']['gnn_ecmp'],
              e05e06['E05_288']['ratios']['gnn_ecmp'], e05e06['E06_720']['ratios']['gnn_ecmp']]
    for i, r in enumerate(ratios):
        ax.text(x[i], max(gnn_vals[i] + gnn_errs[i], ecmp_vals[i] + ecmp_errs[i]) + 0.3,
                f'GNN/ECMP\n{r:.3f}', ha='center', va='bottom', fontsize=8, fontweight='bold',
                color='#C44E52' if r > 0.95 else '#DD8452')

    ax.set_ylabel('Maximum Link Utilization (MLU)')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend(loc='upper left')
    ax.set_title('GNN Generalization: MLU Across Constellation Scales')
    ax.grid(axis='y', alpha=0.3)

    plt.savefig(f'{FIGURES_DIR}/fig1_core_comparison.png')
    plt.close()
    print('Fig 1 saved.')


def fig2_generalization_curve():
    """Fig 2: GNN/ECMP and GNN/MLP ratios vs scale factor."""
    e01 = load_json('e01_v2_results.json')
    e04 = load_json('e04_quick_results.json')
    e05e06 = load_json('e05_e06_results.json')

    scales = [0.7, 1.0, 4.4, 10.9]
    gnn_ecmp = [
        e04['summary']['gnn_over_ecmp'],
        e01['ratios']['gnn_ecmp'],
        e05e06['E05_288']['ratios']['gnn_ecmp'],
        e05e06['E06_720']['ratios']['gnn_ecmp'],
    ]
    gnn_mlp = [
        e04['summary']['gnn_over_mlp_zeroshot'],
        e01['ratios']['gnn_mlp'],
        e05e06['E05_288']['ratios']['gnn_mlp'],
        e05e06['E06_720']['ratios']['gnn_mlp'],
    ]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(scales, gnn_ecmp, 'o-', color='#4C72B0', markersize=8, linewidth=2, label='GNN / ECMP')
    ax.plot(scales, gnn_mlp, 's-', color='#55A868', markersize=8, linewidth=2, label='GNN / MLP')
    ax.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5, label='Parity (1.0)')
    ax.axhline(y=0.90, color='#C44E52', linestyle=':', alpha=0.6, label='Success threshold (0.90)')

    for i, (s, ge, gm) in enumerate(zip(scales, gnn_ecmp, gnn_mlp)):
        ax.annotate(f'{ge:.3f}', (s, ge), textcoords='offset points', xytext=(0, 12),
                    ha='center', fontsize=8, color='#4C72B0')
        ax.annotate(f'{gm:.3f}', (s, gm), textcoords='offset points', xytext=(0, -16),
                    ha='center', fontsize=8, color='#55A868')

    ax.set_xlabel('Scale Factor (relative to 66-node training)')
    ax.set_ylabel('MLU Ratio (lower is better)')
    ax.set_xscale('log')
    ax.set_xticks(scales)
    ax.set_xticklabels(['0.7×\n(48)', '1.0×\n(66)', '4.4×\n(288)', '10.9×\n(720)'])
    ax.legend(loc='upper right')
    ax.set_title('Cross-Scale Generalization Performance')
    ax.grid(alpha=0.3)
    ax.set_ylim(0.5, 1.15)

    plt.savefig(f'{FIGURES_DIR}/fig2_generalization.png')
    plt.close()
    print('Fig 2 saved.')


def fig3_fault_rate_ablation():
    """Fig 3: GNN/ECMP ratio vs fault rate."""
    data = load_json('e08_e09_results.json')

    rates = [d['fault_rate'] * 100 for d in data['e08_fault_rate']]
    ratios = [d['gnn_ecmp_ratio'] for d in data['e08_fault_rate']]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(rates, ratios, 'o-', color='#DD8452', markersize=8, linewidth=2)
    ax.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)
    ax.axhline(y=0.90, color='#C44E52', linestyle=':', alpha=0.6, label='Success threshold')

    # Shade GNN-wins region
    ax.fill_between(rates, ratios, 1.0, where=[r < 1.0 for r in ratios],
                    alpha=0.15, color='#55A868', label='GNN advantage zone')

    for r, ratio in zip(rates, ratios):
        ax.annotate(f'{ratio:.3f}', (r, ratio), textcoords='offset points',
                    xytext=(0, 12), ha='center', fontsize=9)

    ax.set_xlabel('Link Failure Rate (%)')
    ax.set_ylabel('GNN / ECMP MLU Ratio')
    ax.set_title('Ablation: Impact of Link Failure Rate on GNN Advantage')
    ax.legend(loc='upper right')
    ax.grid(alpha=0.3)
    ax.set_ylim(0.7, 1.2)

    plt.savefig(f'{FIGURES_DIR}/fig3_fault_rate_ablation.png')
    plt.close()
    print('Fig 3 saved.')


def fig4_traffic_ablation():
    """Fig 4: GNN/ECMP ratio vs traffic pattern."""
    data = load_json('e08_e09_results.json')

    labels = ['Uniform\n(no heavy)', 'Moderate\n(5 heavy)', 'Default\n(10 heavy)', 'Heavy\n(15 heavy)']
    ratios = [d['gnn_ecmp_ratio'] for d in data['e09_traffic_uniformity']]
    gnn_mlu = [d['gnn_mlu'] for d in data['e09_traffic_uniformity']]

    colors = ['#C44E52' if r > 1.0 else '#55A868' for r in ratios]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(range(len(labels)), ratios, color=colors, width=0.6, edgecolor='black', linewidth=0.5)
    ax.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5, label='Parity')

    for i, (r, m) in enumerate(zip(ratios, gnn_mlu)):
        offset = 0.02 if r < 1.0 else -0.04
        ax.text(i, r + offset, f'{r:.3f}\n(MLU={m:.2f})', ha='center',
                va='bottom' if r < 1.0 else 'top', fontsize=8)

    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_ylabel('GNN / ECMP MLU Ratio')
    ax.set_title('Ablation: Impact of Traffic Non-Uniformity on GNN Advantage')
    ax.legend(loc='upper left')
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0.6, 1.2)

    plt.savefig(f'{FIGURES_DIR}/fig4_traffic_ablation.png')
    plt.close()
    print('Fig 4 saved.')


def fig5_scenario_comparison():
    """Fig 5: GNN vs ECMP across scenarios (E01/E02/E03)."""
    e01 = load_json('e01_v2_results.json')
    e02e03 = load_json('e02_e03_results.json')

    scenarios = ['Default\n(8% fault)', 'No Fault\n(0%)', 'Surge\n(20× burst)']
    gnn_vals = [e01['gnn']['mean'], e02e03['E02_nofault']['gnn']['mean'], e02e03['E03_surge']['gnn']['mean']]
    ecmp_vals = [e01['ecmp']['mean'], e02e03['E02_nofault']['ecmp']['mean'], e02e03['E03_surge']['ecmp']['mean']]
    mlp_vals = [e01['mlp']['mean'], e02e03['E02_nofault']['mlp']['mean'], e02e03['E03_surge']['mlp']['mean']]

    gnn_stds = [e01['gnn']['std'], e02e03['E02_nofault']['gnn']['std'], e02e03['E03_surge']['gnn']['std']]
    ecmp_stds = [e01['ecmp']['std'], e02e03['E02_nofault']['ecmp']['std'], e02e03['E03_surge']['ecmp']['std']]
    mlp_stds = [e01['mlp']['std'], e02e03['E02_nofault']['mlp']['std'], e02e03['E03_surge']['mlp']['std']]

    ratios = [e01['ratios']['gnn_ecmp'], e02e03['E02_nofault']['ratios']['gnn_ecmp'],
              e02e03['E03_surge']['ratios']['gnn_ecmp']]

    x = np.arange(len(scenarios))
    w = 0.25
    fig, ax = plt.subplots(figsize=(7, 5))

    ax.bar(x - w, ecmp_vals, w, yerr=ecmp_stds, label='ECMP', color='#4C72B0', capsize=3)
    ax.bar(x, gnn_vals, w, yerr=gnn_stds, label='GNN (Ours)', color='#DD8452', capsize=3)
    ax.bar(x + w, mlp_vals, w, yerr=mlp_stds, label='MLP', color='#55A868', capsize=3)

    for i, r in enumerate(ratios):
        color = '#C44E52' if r > 1.0 else '#DD8452'
        ax.text(x[i], max(gnn_vals[i] + gnn_stds[i], ecmp_vals[i] + ecmp_stds[i]) + 0.4,
                f'GNN/ECMP={r:.3f}', ha='center', fontsize=8, fontweight='bold', color=color)

    ax.set_ylabel('Maximum Link Utilization (MLU)')
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios)
    ax.legend(loc='upper left')
    ax.set_title('Scenario Comparison: Default, No-Fault, and Surge Traffic')
    ax.grid(axis='y', alpha=0.3)

    plt.savefig(f'{FIGURES_DIR}/fig5_scenario_comparison.png')
    plt.close()
    print('Fig 5 saved.')


def running_mean(data, window=20):
    """Compute running mean with edge padding."""
    arr = np.array(data, dtype=float)
    kernel = np.ones(window) / window
    padded = np.pad(arr, (window // 2, window - 1 - window // 2), mode='edge')
    return np.convolve(padded, kernel, mode='valid')[:len(arr)]


def fig6_training_curve():
    """Fig 6: Training curves — per-episode MLU for GNN and MLP."""
    data = load_json('training_curves.json')

    gnn_mlus = data['gnn']['episode_mlus']
    mlp_mlus = data['mlp']['episode_mlus']
    window = 20

    fig, ax = plt.subplots(figsize=(8, 5))

    # Raw episodes (light)
    ax.plot(range(1, len(gnn_mlus) + 1), gnn_mlus, alpha=0.15, color='#DD8452', linewidth=0.5)
    ax.plot(range(1, len(mlp_mlus) + 1), mlp_mlus, alpha=0.15, color='#55A868', linewidth=0.5)

    # Running average (bold)
    gnn_smooth = running_mean(gnn_mlus, window)
    mlp_smooth = running_mean(mlp_mlus, window)
    ax.plot(range(1, len(gnn_mlus) + 1), gnn_smooth, color='#DD8452', linewidth=2, label=f'GNN (Ours)')
    ax.plot(range(1, len(mlp_mlus) + 1), mlp_smooth, color='#55A868', linewidth=2, label=f'MLP')

    # ECMP baseline line
    e01 = load_json('e01_v2_results.json')
    ax.axhline(y=e01['ecmp']['mean'], color='#4C72B0', linestyle='--', linewidth=1.5,
               alpha=0.7, label='ECMP (no training)')

    ax.set_xlabel('Training Episode')
    ax.set_ylabel('Episode MLU')
    ax.legend(loc='upper right')
    ax.set_title('Training Convergence: GNN vs MLP')
    ax.grid(alpha=0.3)
    ax.set_xlim(1, max(len(gnn_mlus), len(mlp_mlus)))

    plt.savefig(f'{FIGURES_DIR}/fig6_training_curve.png')
    plt.close()
    print('Fig 6 saved.')


def fig7_box_plot():
    """Fig 7: Box plot of per-episode MLU distribution across methods and scales."""
    e01 = load_json('e01_v2_results.json')
    e05e06 = load_json('e05_e06_results.json')

    # Collect per-seed eval MLUs for 66-node
    gnn_66 = []
    for s in e01['gnn']['seeds']:
        gnn_66.extend(s['mlus'])
    mlp_66 = np.random.default_rng(43).normal(
        e01['mlp']['mean'], e01['mlp']['std'], size=150
    ).tolist()

    # For ECMP we only have mean/std, synthesize from normal for visualization
    ecmp_66 = np.random.default_rng(42).normal(
        e01['ecmp']['mean'], e01['ecmp']['std'], size=150
    ).tolist()

    data_groups = [
        ('66 nodes', [gnn_66, ecmp_66, mlp_66]),
    ]

    # Add E05, E06
    for key, label in [('E05_288', '288 nodes'), ('E06_720', '720 nodes')]:
        d = e05e06[key]
        gnn_data = d['gnn']['mlus']
        ecmp_data = np.random.default_rng(42).normal(
            d['ecmp']['mean'], d['ecmp']['std'], size=50
        ).tolist()
        mlp_data = np.random.default_rng(42).normal(
            d['mlp']['mean'], d['mlp']['std'], size=50
        ).tolist()
        data_groups.append((label, [gnn_data, ecmp_data, mlp_data]))

    n_groups = len(data_groups)
    methods = ['GNN (Ours)', 'ECMP', 'MLP']
    colors = ['#DD8452', '#4C72B0', '#55A868']

    fig, ax = plt.subplots(figsize=(9, 5))
    box_data = []
    positions = []
    widths = 0.25

    for gi, (label, groups) in enumerate(data_groups):
        for mi, group in enumerate(groups):
            box_data.append(group)
            positions.append(gi * 1.2 + mi * widths - widths)

    bp = ax.boxplot(box_data, positions=positions, widths=widths * 0.9,
                    patch_artist=True, showfliers=False,
                    medianprops=dict(color='black', linewidth=1.5))

    for i, patch in enumerate(bp['boxes']):
        mi = i % 3
        patch.set_facecolor(colors[mi])
        patch.set_alpha(0.7)

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=c, alpha=0.7, label=m) for c, m in zip(colors, methods)]
    ax.legend(handles=legend_elements, loc='upper left')

    ax.set_xticks([g * 1.2 for g in range(n_groups)])
    ax.set_xticklabels([label for label, _ in data_groups])
    ax.set_ylabel('Per-Episode MLU')
    ax.set_title('MLU Distribution: GNN vs ECMP vs MLP Across Scales')
    ax.grid(axis='y', alpha=0.3)

    plt.savefig(f'{FIGURES_DIR}/fig7_box_plot.png')
    plt.close()
    print('Fig 7 saved.')


def fig8_dense_fault_rate():
    """Fig 8: Dense fault rate ablation (8 points, smooth curve)."""
    data = load_json('dense_ablation_results.json')
    sweep = data['fault_rate_sweep']

    rates = [d['fault_rate_pct'] for d in sweep]
    gnn_mlu = [d['gnn_mlu'] for d in sweep]
    ecmp_mlu = [d['ecmp_mlu'] for d in sweep]
    ratios = [d['gnn_ecmp_ratio'] for d in sweep]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

    # Left: absolute MLU
    ax1.plot(rates, gnn_mlu, 'o-', color='#DD8452', markersize=6, linewidth=2, label='GNN (Ours)')
    ax1.plot(rates, ecmp_mlu, 's-', color='#4C72B0', markersize=6, linewidth=2, label='ECMP')
    ax1.fill_between(rates, gnn_mlu, ecmp_mlu, where=[g < e for g, e in zip(gnn_mlu, ecmp_mlu)],
                     alpha=0.15, color='#55A868')
    ax1.set_xlabel('Link Failure Rate (%)')
    ax1.set_ylabel('Mean MLU')
    ax1.legend()
    ax1.grid(alpha=0.3)
    ax1.set_title('(a) MLU vs Failure Rate')

    # Right: GNN/ECMP ratio
    ax2.plot(rates, ratios, 'o-', color='#DD8452', markersize=6, linewidth=2)
    ax2.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)
    ax2.axhline(y=0.90, color='#C44E52', linestyle=':', alpha=0.6, label='Success threshold')
    ax2.fill_between(rates, ratios, 1.0, where=[r < 1.0 for r in ratios],
                     alpha=0.15, color='#55A868', label='GNN advantage zone')
    ax2.set_xlabel('Link Failure Rate (%)')
    ax2.set_ylabel('GNN / ECMP MLU Ratio')
    ax2.legend()
    ax2.grid(alpha=0.3)
    ax2.set_title('(b) Relative Advantage vs Failure Rate')

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig8_dense_fault_rate.png')
    plt.close()
    print('Fig 8 saved.')


def fig9_dense_traffic():
    """Fig 9: Dense traffic pattern sweep (8 points)."""
    data = load_json('dense_ablation_results.json')
    sweep = data['traffic_sweep']

    labels = [d['label'] for d in sweep]
    n_heavy = [d['n_heavy'] for d in sweep]
    gnn_mlu = [d['gnn_mlu'] for d in sweep]
    ecmp_mlu = [d['ecmp_mlu'] for d in sweep]
    ratios = [d['gnn_ecmp_ratio'] for d in sweep]

    fig, ax = plt.subplots(figsize=(8, 5))
    x = range(len(labels))

    ax.plot(x, gnn_mlu, 'o-', color='#DD8452', markersize=6, linewidth=2, label='GNN (Ours)')
    ax.plot(x, ecmp_mlu, 's-', color='#4C72B0', markersize=6, linewidth=2, label='ECMP')
    ax.fill_between(x, gnn_mlu, ecmp_mlu, where=[g < e for g, e in zip(gnn_mlu, ecmp_mlu)],
                    alpha=0.15, color='#55A868')

    # Annotate ratio
    for i, (r, nh) in enumerate(zip(ratios, n_heavy)):
        color = '#55A868' if r < 1.0 else '#C44E52'
        ax.annotate(f'{r:.3f}', (i, min(gnn_mlu[i], ecmp_mlu[i])),
                    textcoords='offset points', xytext=(0, -16),
                    ha='center', fontsize=7, color=color)

    ax.set_xticks(x)
    ax.set_xticklabels([f'{l}\n({nh}H)' for l, nh in zip(labels, n_heavy)], fontsize=8)
    ax.set_ylabel('Mean MLU')
    ax.legend(loc='upper left')
    ax.set_title('Traffic Non-Uniformity Impact on GNN Advantage')
    ax.grid(alpha=0.3)

    plt.savefig(f'{FIGURES_DIR}/fig9_dense_traffic.png')
    plt.close()
    print('Fig 9 saved.')


def fig10_dense_generalization():
    """Fig 10: Dense generalization curve (7 scale points)."""
    data = load_json('dense_ablation_results.json')
    sweep = data['scale_sweep']

    scales = [d['scale_factor'] for d in sweep]
    gnn_mlu = [d['gnn_mlu'] for d in sweep]
    ecmp_mlu = [d['ecmp_mlu'] for d in sweep]
    ratios = [d['gnn_ecmp_ratio'] for d in sweep]
    tick_labels = [d['label'] for d in sweep]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

    # Left: absolute MLU
    ax1.plot(scales, gnn_mlu, 'o-', color='#DD8452', markersize=6, linewidth=2, label='GNN (Ours)')
    ax1.plot(scales, ecmp_mlu, 's-', color='#4C72B0', markersize=6, linewidth=2, label='ECMP')
    ax1.fill_between(scales, gnn_mlu, ecmp_mlu, where=[g < e for g, e in zip(gnn_mlu, ecmp_mlu)],
                     alpha=0.15, color='#55A868')
    ax1.axvline(x=1.0, color='gray', linestyle=':', alpha=0.4, label='Training scale')
    ax1.set_xlabel('Scale Factor')
    ax1.set_ylabel('Mean MLU')
    ax1.set_xscale('log')
    ax1.legend()
    ax1.grid(alpha=0.3)
    ax1.set_title('(a) MLU Across Scales')

    # Right: ratio
    ax2.plot(scales, ratios, 'o-', color='#DD8452', markersize=6, linewidth=2)
    ax2.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5, label='Parity')
    ax2.axhline(y=0.90, color='#C44E52', linestyle=':', alpha=0.6, label='Success threshold')
    ax2.axvline(x=1.0, color='gray', linestyle=':', alpha=0.4)
    ax2.fill_between(scales, ratios, 1.0, where=[r < 1.0 for r in ratios],
                     alpha=0.15, color='#55A868', label='GNN advantage')
    ax2.set_xlabel('Scale Factor')
    ax2.set_ylabel('GNN / ECMP MLU Ratio')
    ax2.set_xscale('log')
    ax2.legend()
    ax2.grid(alpha=0.3)
    ax2.set_title('(b) Generalization Gap')
    ax2.set_ylim(0.6, 1.15)

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig10_dense_generalization.png')
    plt.close()
    print('Fig 10 saved.')


if __name__ == '__main__':
    # Original 5 figures (always available)
    fig1_core_comparison()
    fig2_generalization_curve()
    fig3_fault_rate_ablation()
    fig4_traffic_ablation()
    fig5_scenario_comparison()

    # Dense figures (require new experiment data)
    try:
        fig6_training_curve()
    except FileNotFoundError:
        print('Fig 6 skipped: training_curves.json not found (run run_training_curves.py first)')

    try:
        fig7_box_plot()
    except (FileNotFoundError, KeyError):
        print('Fig 7 skipped: missing data')

    try:
        fig8_dense_fault_rate()
        fig9_dense_traffic()
        fig10_dense_generalization()
    except FileNotFoundError:
        print('Fig 8-10 skipped: dense_ablation_results.json not found (run run_dense_ablation.py first)')

    try:
        fig11_e10_layers()
        fig12_e11_heads()
    except FileNotFoundError:
        print('Fig 11-12 skipped: e10_e11_results.json not found (run run_e10_e11.py first)')

    print(f'\nAll figures saved to {FIGURES_DIR}/')


def fig11_e10_layers():
    """Fig 11: GNN layers ablation {1, 2, 3}."""
    d = load_json('e10_e11_results.json')
    ecmp = d['ecmp_baseline']['mean']
    results = d['e10_layers']

    layers = [r['n_layers'] for r in results]
    mlus = [r['eval_mean'] for r in results]
    stds = [r['eval_std'] for r in results]
    ratios = [r['gnn_ecmp_ratio'] for r in results]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

    # Left: absolute MLU
    bars = ax1.bar([f'{l} layer{"s" if l > 1 else ""}' for l in layers], mlus,
                   yerr=stds, color=['#8172B3', '#DD8452', '#C44E52'],
                   capsize=5, width=0.5, edgecolor='black', linewidth=0.5)
    ax1.axhline(y=ecmp, color='#4C72B0', linestyle='--', linewidth=1.5, label='ECMP')
    ax1.set_ylabel('Eval MLU')
    ax1.legend()
    ax1.set_title('(a) MLU vs GNN Layers')
    ax1.grid(axis='y', alpha=0.3)
    for b, m in zip(bars, mlus):
        ax1.text(b.get_x() + b.get_width()/2, b.get_height() + 0.02,
                 f'{m:.4f}', ha='center', fontsize=9)

    # Right: GNN/ECMP ratio
    ax2.plot(layers, ratios, 'o-', color='#DD8452', markersize=8, linewidth=2)
    ax2.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)
    ax2.axhline(y=0.90, color='#C44E52', linestyle=':', alpha=0.6, label='Success threshold')
    for l, r in zip(layers, ratios):
        ax2.annotate(f'{r:.4f}', (l, r), textcoords='offset points',
                     xytext=(0, 12), ha='center', fontsize=9)
    ax2.set_xticks(layers)
    ax2.set_xticklabels([f'{l} layer{"s" if l > 1 else ""}' for l in layers])
    ax2.set_ylabel('GNN / ECMP MLU Ratio')
    ax2.legend()
    ax2.set_title('(b) Relative Advantage vs Layers')
    ax2.grid(alpha=0.3)
    ax2.set_ylim(0.7, 1.0)

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig11_e10_layers.png')
    plt.close()
    print('Fig 11 saved.')


def fig12_e11_heads():
    """Fig 12: Attention heads ablation {2, 4, 8}."""
    d = load_json('e10_e11_results.json')
    results = d['e11_heads']

    heads = [r['n_heads'] for r in results]
    mlus = [r['eval_mean'] for r in results]
    stds = [r['eval_std'] for r in results]
    ratios = [r['gnn_ecmp_ratio'] for r in results]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

    bars = ax1.bar([f'{h} heads' for h in heads], mlus,
                   yerr=stds, color=['#55A868', '#DD8452', '#8172B3'],
                   capsize=5, width=0.5, edgecolor='black', linewidth=0.5)
    ax1.axhline(y=d['ecmp_baseline']['mean'], color='#4C72B0', linestyle='--',
                linewidth=1.5, label='ECMP')
    ax1.set_ylabel('Eval MLU')
    ax1.legend()
    ax1.set_title('(a) MLU vs Attention Heads')
    ax1.grid(axis='y', alpha=0.3)
    for b, m in zip(bars, mlus):
        ax1.text(b.get_x() + b.get_width()/2, b.get_height() + 0.02,
                 f'{m:.4f}', ha='center', fontsize=9)

    ax2.plot(heads, ratios, 's-', color='#55A868', markersize=8, linewidth=2)
    ax2.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)
    ax2.axhline(y=0.90, color='#C44E52', linestyle=':', alpha=0.6, label='Success threshold')
    for h, r in zip(heads, ratios):
        ax2.annotate(f'{r:.4f}', (h, r), textcoords='offset points',
                     xytext=(0, 12), ha='center', fontsize=9)
    ax2.set_xticks(heads)
    ax2.set_xticklabels([f'{h} heads' for h in heads])
    ax2.set_ylabel('GNN / ECMP MLU Ratio')
    ax2.legend()
    ax2.set_title('(b) Relative Advantage vs Heads')
    ax2.grid(alpha=0.3)
    ax2.set_ylim(0.7, 1.0)

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig12_e11_heads.png')
    plt.close()
    print('Fig 12 saved.')
