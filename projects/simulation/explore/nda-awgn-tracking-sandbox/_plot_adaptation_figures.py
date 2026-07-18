# -*- coding: utf-8 -*-
"""画 4 种适配扫描关键图（3 子图）.

Fig 1: fair_gain 递增链（6 场景, 5 seed CI 误差棒）
Fig 2: A4 切换 BER 曲线（crossover 区场景，切换 vs DA vs NDA vs oracle）
Fig 3: A4 crossover 区增益柱状图（γd=15dB, 5 seed CI）
"""
import os
import sys
import json

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# 中文字体（Windows）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))

# 数据
main = json.load(open(os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_main', '_fair_gain_summary.json')))
main_ber = json.load(open(os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_main', '_main_experiment_5seed.json')))
up = json.load(open(os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_uplink', '_uplink_summary.json')))
up_ber = json.load(open(os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_uplink', '_uplink_5seed.json')))
a4 = json.load(open(os.path.join(_HERE, '_a4_switch_results.json')))
a4_imp = json.load(open(os.path.join(_HERE, '_a4_improved_cv_results.json')))

plt.rcParams.update({'font.size': 10, 'axes.grid': True, 'grid.alpha': 0.3})

fig, axes = plt.subplots(1, 3, figsize=(20, 5.5))

# =============================================================================
# Fig 1: fair_gain 递增链
# =============================================================================
ax = axes[0]
labels = ['AWGN', 'weak', 'moderate', 'strong\n(下行)', 'uplink\nmoderate', 'uplink\nstrong']
rytov = [0, 0.029, 0.1, 0.2, 0.15, 0.25]
gains = []
cis = []
for sc in ['awgn', 'weak', 'moderate', 'strong']:
    e = main['fair_gain'][sc]
    g = e.get('gain_mean_db') or e.get('workregion_grand_mean_db')
    ci = e.get('gain_ci95_db')
    if not ci or ci[0] is None:
        ci = e.get('workregion_grand_ci95_db')
    gains.append(g)
    cis.append(ci)
for sc in ['uplink_moderate', 'uplink_strong']:
    e = up['fair_gain'][sc]
    g = e.get('workregion_grand_mean_db') or e.get('gain_mean_db')
    ci = e.get('workregion_grand_ci95_db') or e.get('gain_ci95_db')
    gains.append(g)
    cis.append(ci)

gains = np.array(gains)
lo = np.array([c[0] for c in cis])
hi = np.array([c[1] for c in cis])
err_lo = gains - lo
err_hi = hi - gains

x = np.arange(len(labels))
colors = ['#2196F3', '#4CAF50', '#FF9800', '#F44336', '#9C27B0', '#795548']
bars = ax.bar(x, gains, color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
ax.errorbar(x, gains, yerr=[err_lo, err_hi], fmt='none', ecolor='black',
            capsize=5, capthick=1.5, lw=1.5)
ax.axhline(0, color='gray', ls='--', lw=0.8)
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=8.5)
ax.set_ylabel('fair gain @ HD-FEC (dB)', fontsize=11)
ax.set_title('(a) NDA-ML vs DA-ML: gain 随湍流递增\n(正 = NDA 赢, 5 seed 95% CI)', fontsize=10.5)
for i, (g, r) in enumerate(zip(gains, rytov)):
    ax.text(i, g + 0.12, f'{g:+.2f}', ha='center', fontsize=9, fontweight='bold')

# 在 x 轴下方标 Rytov
ax2 = ax.twiny()
ax2.set_xlim(ax.get_xlim())
ax2.set_xticks(x)
ax2.set_xticklabels([f'σ²R={r}' for r in rytov], fontsize=7.5, color='gray')
ax2.tick_params(top=False)

# =============================================================================
# Fig 2: A4 切换 BER 曲线 — 选 moderate（crossover 最明显）
# =============================================================================
ax = axes[1]
# 用改进版基准配置 geth13_cvmar1.1 的 moderate
imp_mod = a4_imp['results']['geth13.0_cvmar1.1']['moderate']
snrs = [p['snr_db'] for p in imp_mod]
nda = [p['nda_ber'] for p in imp_mod]
da = [p['da_ber'] for p in imp_mod]
sw = [p['switch_ber'] for p in imp_mod]

ax.semilogy(snrs, nda, 'o-', color='#2196F3', label='始终 NDA-ML', lw=1.8, markersize=6)
ax.semilogy(snrs, da, 's-', color='#FF9800', label='始终 DA-ML', lw=1.8, markersize=6)
ax.semilogy(snrs, sw, 'D-', color='#E91E63', label='DA/NDA 切换 (我们的方法)', lw=2.2, markersize=7)

# 标 crossover 区
ax.axvspan(13, 17, alpha=0.12, color='green', label='crossover 区')
ax.axhline(3.8e-3, color='k', ls=':', lw=1, label='HD-FEC 3.8e-3')

ax.set_xlabel(r'$\gamma_d$ (dB)', fontsize=11)
ax.set_ylabel('BER', fontsize=11)
ax.set_title('(b) moderate 湍流: 切换策略在 crossover 区\n超越始终 DA / 始终 NDA', fontsize=10.5)
ax.legend(fontsize=7.5, loc='upper right')
ax.set_ylim(1e-3, 1)
ax.set_xlim(4, 27)

# 标注 crossover 区增益
for p in imp_mod:
    if p['snr_db'] == 15.0:
        ax.annotate(f'+{p["switch_vs_max_db"]:.2f}dB\nvs max(DA,NDA)',
                    xy=(15, p['switch_ber']), xytext=(15.5, p['switch_ber'] * 0.3),
                    fontsize=8, color='#E91E63', fontweight='bold',
                    arrowprops=dict(arrowstyle='->', color='#E91E63', lw=1.2))

# =============================================================================
# Fig 3: A4 crossover 区增益柱状图（5 seed 原版, γd=15dB）
# =============================================================================
ax = axes[2]
scenes = ['weak', 'moderate', 'strong']
sv_means = []
sv_cis = []
for sc in scenes:
    for p in a4['summary'][sc]['points']:
        if p['snr_db'] == 15.0:
            sv_means.append(p['switch_vs_max_db_mean'])
            sv_cis.append(p['switch_vs_max_db_ci95'])

sv_means = np.array(sv_means)
lo = np.array([c[0] for c in sv_cis])
hi = np.array([c[1] for c in sv_cis])

x = np.arange(len(scenes))
colors3 = ['#4CAF50', '#FF9800', '#F44336']
bars = ax.bar(x, sv_means, color=colors3, alpha=0.8, edgecolor='black', linewidth=0.5, width=0.5)
ax.errorbar(x, sv_means, yerr=[sv_means - lo, hi - sv_means], fmt='none',
            ecolor='black', capsize=6, capthick=1.5, lw=1.5)

ax.axhline(0.2, color='green', ls='--', lw=1.2, label='用户阈值 0.2dB')
ax.axhline(0, color='gray', ls='-', lw=0.5)
ax.set_xticks(x)
ax.set_xticklabels([f'{s}\n(γd=15dB)' for s in scenes], fontsize=9.5)
ax.set_ylabel('切换 vs max(DA,NDA) (dB)', fontsize=11)
ax.set_title('(c) crossover 区增益: 切换策略\n稳定超越始终 DA / 始终 NDA (5 seed 95% CI)', fontsize=10.5)
for i, (m, c) in enumerate(zip(sv_means, sv_cis)):
    ax.text(i, m + 0.04, f'{m:+.2f}', ha='center', fontsize=10, fontweight='bold')
    ax.text(i, -0.12, f'CI[{c[0]:+.2f},{c[1]:+.2f}]', ha='center', fontsize=7, color='gray')
ax.legend(fontsize=8, loc='upper right')
ax.set_ylim(-0.15, 0.8)

fig.suptitle('4 种适配扫描实验结果: A4 条件适配 PASS（crossover 区 +0.35~0.56dB, 工作区 0 FAIL）',
             fontsize=12.5, y=1.02)
fig.tight_layout()
png = os.path.join(_HERE, '_adaptation_scan_figures.png')
fig.savefig(png, dpi=150, bbox_inches='tight')
print(f'[保存] {png}')
