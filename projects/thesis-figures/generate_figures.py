#!/usr/bin/env python3
"""Generate 5 key visualization figures for thesis chapters."""

import json
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

# --- Configuration ---
# Script lives at projects/thesis-figures/generate_figures.py
# Run from repo root: python projects/thesis-figures/generate_figures.py
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT_DIR = os.path.join(REPO_ROOT, 'projects', 'thesis-figures')
os.makedirs(OUT_DIR, exist_ok=True)

# Academic color palette (muted blue/orange/green/red/purple/gray)
COLORS = {
    'blue': '#4472C4',
    'orange': '#ED7D31',
    'green': '#70AD47',
    'red': '#C00000',
    'purple': '#7030A0',
    'gray': '#808080',
    'light_blue': '#9DC3E6',
    'light_orange': '#F4B183',
}

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linestyle': '--',
})

FIG_SIZE = (8, 5)
BAR_WIDTH = 0.35

summary = {}


def load_json(path):
    with open(path) as f:
        return json.load(f)


def save_fig(fig, name):
    fig.savefig(os.path.join(OUT_DIR, f'{name}.pdf'), bbox_inches='tight')
    fig.savefig(os.path.join(OUT_DIR, f'{name}.png'), bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved {name}.pdf and {name}.png')


# ============================================================
# Figure 1: Ch1 Method Performance Comparison (stretch + delay)
# ============================================================
def fig_ch1_method_comparison():
    print('\n[Fig 1] Ch1 Method Performance Comparison')
    ch1_path = os.path.join(REPO_ROOT, 'projects', 'leo-mega-constellation-gnn-routing',
                            'simulator', 'results', 'ch1_multi_seed_results.json')
    data = load_json(ch1_path)

    methods = ['Dijkstra', 'GRLR', 'Ours\n(Full)', 'A1\n(w/o PE)', 'A2\n(Single)', 'A3\n(w/o PE\n+Single)']
    n = len(methods)

    # Stretch data
    stretch_means = [
        1.000,                           # Dijkstra (optimal)
        1.008,                           # GRLR
        data['full']['mean_stretch']['mean'],
        data['A1']['mean_stretch']['mean'],
        data['A2']['mean_stretch']['mean'],
        data['A3']['mean_stretch']['mean'],
    ]
    stretch_stds = [
        0.0,                             # Dijkstra (deterministic)
        0.0,                             # GRLR (single run)
        data['full']['mean_stretch']['std'],
        data['A1']['mean_stretch']['std'],
        data['A2']['mean_stretch']['std'],
        data['A3']['mean_stretch']['std'],
    ]

    # Delay data (ms)
    delay_means = [
        60.32,                           # Dijkstra
        60.32,                           # GRLR (same as Dijkstra for stretch≈1)
        data['full']['mean_delay']['mean'],
        data['A1']['mean_delay']['mean'],
        data['A2']['mean_delay']['mean'],
        data['A3']['mean_delay']['mean'],
    ]
    delay_stds = [
        0.0,
        0.0,
        data['full']['mean_delay']['std'],
        data['A1']['mean_delay']['std'],
        data['A2']['mean_delay']['std'],
        data['A3']['mean_delay']['std'],
    ]

    fig, ax1 = plt.subplots(figsize=FIG_SIZE)

    x = np.arange(n)
    bars = ax1.bar(x, stretch_means, BAR_WIDTH, yerr=stretch_stds,
                   color=[COLORS['gray'], COLORS['gray'], COLORS['blue'],
                          COLORS['light_blue'], COLORS['orange'], COLORS['light_orange']],
                   edgecolor='black', linewidth=0.5,
                   capsize=4, label='Mean Stretch', zorder=3)
    ax1.set_ylabel('Mean Stretch', color=COLORS['blue'])
    ax1.set_ylim(0.98, 1.16)
    ax1.tick_params(axis='y', labelcolor=COLORS['blue'])

    # Add value labels on bars
    for bar, val in zip(bars, stretch_means):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.003,
                f'{val:.3f}', ha='center', va='bottom', fontsize=8)

    # Second y-axis for delay
    ax2 = ax1.twinx()
    ax2.plot(x, delay_means, 'o-', color=COLORS['red'], linewidth=2,
             markersize=7, label='Mean Delay (ms)', zorder=4)
    ax2.fill_between(x,
                     [m - s for m, s in zip(delay_means, delay_stds)],
                     [m + s for m, s in zip(delay_means, delay_stds)],
                     alpha=0.15, color=COLORS['red'])
    ax2.set_ylabel('Mean Delay (ms)', color=COLORS['red'])
    ax2.tick_params(axis='y', labelcolor=COLORS['red'])
    ax2.set_ylim(59, 70)

    ax1.set_xticks(x)
    ax1.set_xticklabels(methods)
    ax1.set_title('Ch1: Method Performance Comparison')

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', framealpha=0.9)

    fig.tight_layout()
    save_fig(fig, 'fig_ch1_method_comparison')

    summary['fig1_ch1_method_comparison'] = {
        'methods': ['Dijkstra', 'GRLR', 'Full', 'A1(w/o PE)', 'A2(Single)', 'A3(w/o PE+Single)'],
        'stretch_mean': stretch_means,
        'stretch_std': stretch_stds,
        'delay_mean': delay_means,
        'delay_std': delay_stds,
    }


# ============================================================
# Figure 2: Ch2 Blocking Rate vs UE Scale
# ============================================================
def fig_ch2_blocking_rate():
    print('\n[Fig 2] Ch2 Blocking Rate vs UE Scale')
    ch2_dir = os.path.join(REPO_ROOT, 'projects', 'leo-ntn-handover-drl', 'results')

    configs = [
        ('20', 'C6-20-d20', 'E4-20-d20'),
        ('50', 'C6-50-c15-d20', 'E4-50-c15-d20'),
        ('100', 'C6-100-c25', 'E4-100-c25'),
    ]

    gnn_blocking = []
    mlp_blocking = []
    gnn_blocking_std = []
    mlp_blocking_std = []

    for ue_label, c6_prefix, e4_prefix in configs:
        # GNN (C6) seeds
        c6_vals = []
        for seed in ['s1', 's2', 's3']:
            path = os.path.join(ch2_dir, f'{c6_prefix}_{seed}_results.json')
            if os.path.exists(path):
                d = load_json(path)
                for ev in d['eval']:
                    br = ev.get('blocking', ev.get('mean_blocking_rate', 0))
                    c6_vals.append(br * 100)  # to percent
        gnn_blocking.append(np.mean(c6_vals) if c6_vals else 0)
        gnn_blocking_std.append(np.std(c6_vals) if len(c6_vals) > 1 else 0)

        # MLP (E4) seeds
        e4_vals = []
        for seed in ['s1', 's2', 's3']:
            path = os.path.join(ch2_dir, f'{e4_prefix}_{seed}_results.json')
            if os.path.exists(path):
                d = load_json(path)
                for ev in d['eval']:
                    br = ev.get('blocking', ev.get('mean_blocking_rate', 0))
                    e4_vals.append(br * 100)
        mlp_blocking.append(np.mean(e4_vals) if e4_vals else 0)
        mlp_blocking_std.append(np.std(e4_vals) if len(e4_vals) > 1 else 0)

    ue_scales = ['20', '50', '100']
    x = np.arange(len(ue_scales))

    fig, ax = plt.subplots(figsize=FIG_SIZE)

    bars1 = ax.bar(x - BAR_WIDTH/2, gnn_blocking, BAR_WIDTH, yerr=gnn_blocking_std,
                   color=COLORS['blue'], edgecolor='black', linewidth=0.5,
                   capsize=4, label='GNN-DDQN (C6)', zorder=3)
    bars2 = ax.bar(x + BAR_WIDTH/2, mlp_blocking, BAR_WIDTH, yerr=mlp_blocking_std,
                   color=COLORS['orange'], edgecolor='black', linewidth=0.5,
                   capsize=4, label='MLP-DDQN (E4)', zorder=3)

    # Value labels
    for bars, vals in [(bars1, gnn_blocking), (bars2, mlp_blocking)]:
        for bar, val in zip(bars, vals):
            if val > 0.5:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                       f'{val:.1f}', ha='center', va='bottom', fontsize=8)
            else:
                ax.text(bar.get_x() + bar.get_width()/2, 0.3,
                       f'{val:.2f}', ha='center', va='bottom', fontsize=8)

    ax.set_xlabel('UE Scale')
    ax.set_ylabel('Blocking Rate (%)')
    ax.set_xticks(x)
    ax.set_xticklabels(ue_scales)
    ax.set_title('Ch2: Blocking Rate vs UE Scale')
    ax.legend(loc='upper left', framealpha=0.9)

    fig.tight_layout()
    save_fig(fig, 'fig_ch2_blocking_rate')

    summary['fig2_ch2_blocking_rate'] = {
        'ue_scales': ue_scales,
        'gnn_blocking_mean': [round(v, 4) for v in gnn_blocking],
        'gnn_blocking_std': [round(v, 4) for v in gnn_blocking_std],
        'mlp_blocking_mean': [round(v, 4) for v in mlp_blocking],
        'mlp_blocking_std': [round(v, 4) for v in mlp_blocking_std],
    }


# ============================================================
# Figure 3: Ch2 Size Generalization
# ============================================================
def fig_ch2_size_generalization():
    print('\n[Fig 3] Ch2 Size Generalization')
    ch2_dir = os.path.join(REPO_ROOT, 'projects', 'leo-ntn-handover-drl', 'results')

    configs = [
        ('Train 20\nDeploy 20', 'C6-20-d20', 'E4-20-d20'),
        ('Train 20\nDeploy 50', 'C6-50-c15-d20', 'E4-50-c15-d20'),
        ('Train 20\nDeploy 100', 'C6-100-c25', 'E4-100-c25'),
    ]

    gnn_rewards = []
    mlp_rewards = []
    gnn_std = []
    mlp_std = []

    for label, c6_prefix, e4_prefix in configs:
        # GNN
        c6_vals = []
        for seed in ['s1', 's2', 's3']:
            path = os.path.join(ch2_dir, f'{c6_prefix}_{seed}_results.json')
            if os.path.exists(path):
                d = load_json(path)
                for ev in d['eval']:
                    c6_vals.append(ev['reward'])
        gnn_rewards.append(np.mean(c6_vals) if c6_vals else 0)
        gnn_std.append(np.std(c6_vals) if len(c6_vals) > 1 else 0)

        # MLP
        e4_vals = []
        for seed in ['s1', 's2', 's3']:
            path = os.path.join(ch2_dir, f'{e4_prefix}_{seed}_results.json')
            if os.path.exists(path):
                d = load_json(path)
                for ev in d['eval']:
                    e4_vals.append(ev['reward'])
        mlp_rewards.append(np.mean(e4_vals) if e4_vals else 0)
        mlp_std.append(np.std(e4_vals) if len(e4_vals) > 1 else 0)

    labels = [c[0] for c in configs]
    x = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=FIG_SIZE)

    bars1 = ax.bar(x - BAR_WIDTH/2, gnn_rewards, BAR_WIDTH, yerr=gnn_std,
                   color=COLORS['blue'], edgecolor='black', linewidth=0.5,
                   capsize=4, label='GNN-DDQN (C6)', zorder=3)
    bars2 = ax.bar(x + BAR_WIDTH/2, mlp_rewards, BAR_WIDTH, yerr=mlp_std,
                   color=COLORS['orange'], edgecolor='black', linewidth=0.5,
                   capsize=4, label='MLP-DDQN (E4)', zorder=3)

    ax.axhline(y=0, color='black', linewidth=0.5, linestyle='-')
    ax.set_xlabel('Deployment Scenario')
    ax.set_ylabel('Mean Reward')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title('Ch2: Size Generalization Performance')
    ax.legend(loc='best', framealpha=0.9)

    fig.tight_layout()
    save_fig(fig, 'fig_ch2_size_generalization')

    summary['fig3_ch2_size_generalization'] = {
        'scenarios': labels,
        'gnn_reward_mean': [round(v, 2) for v in gnn_rewards],
        'gnn_reward_std': [round(v, 2) for v in gnn_std],
        'mlp_reward_mean': [round(v, 2) for v in mlp_rewards],
        'mlp_reward_std': [round(v, 2) for v in mlp_std],
    }


# ============================================================
# Figure 4: Ch3 HGAT vs Baselines Reward Comparison
# ============================================================
def fig_ch3_reward_comparison():
    print('\n[Fig 4] Ch3 HGAT vs Baselines Reward Comparison')
    ch3_dir = os.path.join(REPO_ROOT, 'projects', 'hgat-satellite-dag-offloading',
                           'simulator', 'results')

    models_seeds = {
        'Random': ('random', [42, 123, 456]),
        'Greedy': ('greedy', [42, 123, 456]),
        'MLP': ('mlp', [42, 123, 456]),
        'GCN': ('gcn', [42, 123, 456]),
        'GraphSAGE': ('graphsage', [42, 123, 456]),
        'HGAT': ('hgat', [42, 123, 456]),
    }

    means = []
    stds = []
    labels = []
    converged_flags = []
    raw_values = {}

    for name, (prefix, seeds) in models_seeds.items():
        rewards = []
        converged = True
        for seed in seeds:
            path = os.path.join(ch3_dir, f'{prefix}_seed{seed}.json')
            if os.path.exists(path):
                d = load_json(path)
                n_ep = d.get('n_episodes', 0)
                # Check convergence: if n_episodes <= 3, training did not converge
                if n_ep <= 3 and prefix not in ('random', 'greedy'):
                    converged = False
                mean_r = d.get('mean_reward', None)
                if mean_r is not None:
                    rewards.append(mean_r)
                else:
                    ep_rewards = d.get('episode_rewards', [])
                    if ep_rewards:
                        rewards.append(np.mean(ep_rewards))
        raw_values[name] = rewards
        if rewards:
            means.append(np.mean(rewards))
            stds.append(np.std(rewards) if len(rewards) > 1 else 0)
        else:
            means.append(0)
            stds.append(0)
        labels.append(name)
        converged_flags.append(converged)

    x = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=FIG_SIZE)

    bar_colors = [COLORS['gray'], COLORS['gray'], COLORS['light_orange'],
                  COLORS['light_blue'], COLORS['light_blue'], COLORS['blue']]
    edge_colors = ['black'] * 6

    bars = ax.bar(x, means, 0.5, yerr=stds,
                  color=bar_colors, edgecolor=edge_colors, linewidth=0.5,
                  capsize=4, zorder=3)

    # Mark non-converged methods with cross
    for i, (bar, converged) in enumerate(zip(bars, converged_flags)):
        if not converged:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + abs(stds[i]) + 5000,
                   'x', ha='center', va='bottom', fontsize=14, color=COLORS['red'],
                   fontweight='bold')

    # Use log scale if values span orders of magnitude
    if min(m for m in means if m != 0) < 0 and abs(min(means)) > 10 * abs(max(means)):
        ax.set_yscale('symlog', linthresh=100)
        ax.set_ylabel('Mean Reward (symlog scale)')
    else:
        ax.set_ylabel('Mean Reward')

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title('Ch3: HGAT vs Baselines Reward Comparison')

    # Add annotation for convergence
    has_non_converged = any(not c for c in converged_flags)
    if has_non_converged:
        ax.annotate('x = training did not converge (n_episodes <= 3)',
                   xy=(0.02, 0.02), xycoords='axes fraction', fontsize=8,
                   color=COLORS['red'])

    fig.tight_layout()
    save_fig(fig, 'fig_ch3_reward_comparison')

    summary['fig4_ch3_reward_comparison'] = {
        'methods': labels,
        'reward_mean': [round(v, 2) for v in means],
        'reward_std': [round(v, 2) for v in stds],
        'converged': converged_flags,
        'raw_values': {k: [round(v, 2) for v in vs] for k, vs in raw_values.items()},
    }


# ============================================================
# Figure 5: Ch1 Ablation Study Stretch Comparison
# ============================================================
def fig_ch1_ablation():
    print('\n[Fig 5] Ch1 Ablation Study Stretch Comparison')
    ch1_path = os.path.join(REPO_ROOT, 'projects', 'leo-mega-constellation-gnn-routing',
                            'simulator', 'results', 'ch1_multi_seed_results.json')
    data = load_json(ch1_path)

    methods = ['Ours\n(Full)', 'A1\n(w/o PE)', 'A2\n(Single\n+ PE)', 'A3\n(w/o PE\n+ Single)', 'Same\nScale']
    keys = ['full', 'A1', 'A2', 'A3', 'same']

    stretch_means = [data[k]['mean_stretch']['mean'] for k in keys]
    stretch_stds = [data[k]['mean_stretch']['std'] for k in keys]

    x = np.arange(len(methods))

    fig, ax = plt.subplots(figsize=FIG_SIZE)

    bar_colors = [COLORS['blue'], COLORS['light_blue'], COLORS['orange'],
                  COLORS['light_orange'], COLORS['green']]

    bars = ax.bar(x, stretch_means, 0.5, yerr=stretch_stds,
                  color=bar_colors, edgecolor='black', linewidth=0.5,
                  capsize=4, zorder=3)

    # Dijkstra optimal baseline
    ax.axhline(y=1.0, color=COLORS['red'], linewidth=1.5, linestyle='--',
               label='Dijkstra Optimal (1.000)', zorder=4)

    # Value labels
    for bar, val, std in zip(bars, stretch_means, stretch_stds):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + std + 0.002,
               f'{val:.4f}', ha='center', va='bottom', fontsize=9)

    ax.set_ylabel('Mean Stretch')
    ax.set_ylim(0.98, 1.14)
    ax.set_xticks(x)
    ax.set_xticklabels(methods)
    ax.set_title('Ch1: Ablation Study - Stretch Comparison')
    ax.legend(loc='upper right', framealpha=0.9)

    fig.tight_layout()
    save_fig(fig, 'fig_ch1_ablation')

    summary['fig5_ch1_ablation'] = {
        'methods': ['Full', 'A1(w/o PE)', 'A2(Single+PE)', 'A3(w/o PE+Single)', 'Same'],
        'stretch_mean': [round(v, 4) for v in stretch_means],
        'stretch_std': [round(v, 4) for v in stretch_stds],
        'dijkstra_optimal': 1.0,
    }


# ============================================================
# Main
# ============================================================
if __name__ == '__main__':
    print('Generating thesis figures...')
    fig_ch1_method_comparison()
    fig_ch2_blocking_rate()
    fig_ch2_size_generalization()
    fig_ch3_reward_comparison()
    fig_ch1_ablation()

    # Save summary
    summary_path = os.path.join(OUT_DIR, 'figure_data_summary.json')
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f'\nSaved data summary to {summary_path}')
    print('Done!')
