# -*- coding: utf-8 -*-
"""画 BER 补点图: 30seed 主区间 + 5seed 补点(两轮)合并, 6 场景.

图 2 主图: BER vs SNR, 6 子图 (awgn/weak/moderate/strong/uplink_moderate/uplink_strong),
每子图 DA/NDA/oracle 三线. 主区间(30seed)实线, 补点(5seed)虚线 + 不同 marker, 标 1e-5 线.

对标: W24 Fig15-17 (多子图 + FEC 线). 全英文 (CCISP 直接用).
"""
import os
import sys
import json

import numpy as np
import matplotlib.pyplot as plt

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..'))

MAIN30 = os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_main_30seed', '_main_experiment_30seed.json')
EXT1 = os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_ber_ext_5seed', '_ber_ext_5seed.json')
EXT2 = os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_ber_ext_5seed', '_ber_ext2_5seed.json')
OUT_PNG = os.path.join(_SIM_ROOT, 'figures', 'fig2_ber_ext_merged.png')
OUT_PDF = os.path.join(_SIM_ROOT, 'figures', 'fig2_ber_ext_merged.pdf')

SCENES = ['awgn', 'weak', 'moderate', 'strong', 'uplink_moderate', 'uplink_strong']
TITLES = {
    'awgn': r'(a) AWGN (no turbulence)',
    'weak': r'(b) Weak turb. ($\alpha$=4.0, $\beta$=3.0)',
    'moderate': r'(c) Moderate turb. ($\alpha$=2.5, $\beta$=1.8)',
    'strong': r'(d) Strong turb. ($\alpha$=1.5, $\beta$=0.8)',
    'uplink_moderate': r'(e) Uplink mod. ($\alpha$=1.2, $\beta$=0.9)',
    'uplink_strong': r'(f) Uplink strong ($\alpha$=1.0, $\beta$=0.7)',
}


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_pts(summary, scene, ber_key):
    """从 summary 提取 (snr[], ber[]) 对, 返回 sorted by snr."""
    pts = summary[scene]['points']
    snr = [p['snr_db'] for p in pts]
    ber = [p[ber_key] for p in pts]
    # 排序
    order = np.argsort(snr)
    return np.array(snr)[order], np.array(ber)[order]


def merge_main_ext(scene, ber_key):
    """合并 30seed 主区间 + 5seed 补点(两轮). 返回 (main_snr, main_ber), (ext_snr, ext_ber)."""
    m = load(MAIN30)
    e1 = load(EXT1)
    main_s, main_b = extract_pts(m['summary'], scene, ber_key)
    ext_s_list, ext_b_list = [], []
    # 第一轮补点 (该场景存在则取)
    if scene in e1['summary']:
        s, b = extract_pts(e1['summary'], scene, ber_key)
        ext_s_list.extend(s)
        ext_b_list.extend(b)
    # 第二轮补点 (只有 strong/uplink)
    if os.path.exists(EXT2):
        e2 = load(EXT2)
        if scene in e2['summary']:
            s, b = extract_pts(e2['summary'], scene, ber_key)
            ext_s_list.extend(s)
            ext_b_list.extend(b)
    # 排序去重 (按 snr)
    if ext_s_list:
        order = np.argsort(ext_s_list)
        ext_s = np.array(ext_s_list)[order]
        ext_b = np.array(ext_b_list)[order]
        return (main_s, main_b), (ext_s, ext_b)
    return (main_s, main_b), (np.array([]), np.array([]))


def plot_one(ax, scene):
    """单子图: DA/NDA/oracle 三线, 主实线 + 补虚线."""
    color_da = '#1f77b4'
    color_nda = '#d62728'
    color_or = '#2ca02c'

    for ber_key, label, color, marker in [
        ('da_ml_ber_mean', 'DA-ML', color_da, 's'),
        ('nda_ml_ber_mean', 'NDA-ML', color_nda, 'o'),
        ('oracle_ber_mean', 'Oracle', color_or, '^'),
    ]:
        (ms, mb), (es, eb) = merge_main_ext(scene, ber_key)
        # 主区间: 实线 (只画 BER>0 的点; 0 值用分辨率下限替代避免 log 报错)
        mb_plot = np.where(mb > 0, mb, 2.4e-6)  # 分辨率下限 ~1/409600
        ax.plot(ms, mb_plot, '-', color=color, linewidth=1.8, label=label, zorder=3)
        # 补点: 虚线 + marker
        if len(es) > 0:
            eb_plot = np.where(eb > 0, eb, 2.4e-6)
            ax.plot(es, eb_plot, '--', color=color, linewidth=1.5, marker=marker,
                    markersize=4.5, zorder=4)

    # FEC 参考线
    ax.axhline(3.8e-3, color='gray', linestyle=':', linewidth=1, alpha=0.7)
    # 1e-5 线 (导师要求展示到)
    ax.axhline(1e-5, color='purple', linestyle=':', linewidth=0.8, alpha=0.5)

    ax.set_yscale('log')
    ax.set_title(TITLES[scene], fontsize=10)
    ax.set_xlabel('SNR / $\\bar{\\gamma}$ (dB)', fontsize=9)
    ax.set_ylabel('BER', fontsize=9)
    ax.grid(True, which='both', alpha=0.25)
    ax.tick_params(labelsize=8)


def main():
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    axes = axes.flatten()

    for idx, scene in enumerate(SCENES):
        plot_one(axes[idx], scene)

    # 统一图例 (取第一个子图的线)
    handles, labels = axes[0].get_legend_handles_labels()
    # 加 FEC 和 1e-5 线的图例
    from matplotlib.lines import Line2D
    handles.append(Line2D([0], [0], color='gray', linestyle=':', label='HD-FEC 3.8e-3'))
    handles.append(Line2D([0], [0], color='purple', linestyle=':', label='1e-5'))
    handles.append(Line2D([0], [0], color='black', linestyle='-', linewidth=1.8, label='30-seed (main)'))
    handles.append(Line2D([0], [0], color='black', linestyle='--', linewidth=1.5, label='5-seed (extension)'))
    labels = labels[:3] + ['HD-FEC 3.8e-3', '1e-5', '30-seed (main)', '5-seed (extension)']
    fig.legend(handles, labels, loc='upper center', ncol=6, fontsize=9,
               bbox_to_anchor=(0.5, 0.995), frameon=True)

    # 调整每个子图纵轴范围按场景自适应
    for idx, scene in enumerate(SCENES):
        ax = axes[idx]
        if scene in ('awgn', 'weak'):
            ax.set_ylim(1e-6, 1)
        elif scene == 'moderate':
            ax.set_ylim(1e-6, 1)
        else:  # strong/uplink
            ax.set_ylim(1e-4, 0.5)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    os.makedirs(os.path.dirname(OUT_PNG), exist_ok=True)
    fig.savefig(OUT_PNG, dpi=150, bbox_inches='tight')
    fig.savefig(OUT_PDF, bbox_inches='tight')
    print(f"[保存] {OUT_PNG}")
    print(f"[保存] {OUT_PDF}")
    plt.close(fig)


if __name__ == '__main__':
    main()
