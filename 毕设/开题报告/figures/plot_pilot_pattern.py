#!/usr/bin/env python3
"""导频图案示意图 — 前置式 vs 均匀式导频对比。

Style: SimHei, 白底, 无标题, 与 plot_kaiti_figures.py 一致。
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.font_manager import fontManager

_FONT_PATH = "/mnt/c/Windows/Fonts/simhei.ttf"
if os.path.exists(_FONT_PATH):
    fontManager.addfont(_FONT_PATH)
plt.rcParams["font.sans-serif"] = ["SimHei"] + plt.rcParams["font.sans-serif"]
plt.rcParams["axes.unicode_minus"] = False

FIG_DIR = os.path.dirname(os.path.abspath(__file__))

N_BLOCKS = 16
PILOT_COLOR = '#0C5DA5'
DATA_COLOR = '#E0E0E0'
EDGE_COLOR = '#555555'
LABEL_COLOR = '#333333'


def draw_blocks(ax, y, pattern, block_w=1.0, block_h=0.6):
    """Draw a row of blocks. pattern: list of 'p' (pilot) or 'd' (data)."""
    for i, p in enumerate(pattern):
        color = PILOT_COLOR if p == 'p' else DATA_COLOR
        rect = plt.Rectangle((i * block_w, y), block_w * 0.92, block_h,
                              facecolor=color, edgecolor=EDGE_COLOR,
                              linewidth=0.8, zorder=2)
        ax.add_patch(rect)


def add_bracket(ax, x_start, x_end, y_top, label, color=LABEL_COLOR):
    """Draw a horizontal bracket above blocks with a label above it."""
    mid = (x_start + x_end) / 2
    bracket_y = y_top + 0.15
    # Horizontal line with short vertical ends
    ax.plot([x_start, x_start], [y_top, bracket_y], color=color, lw=0.8, zorder=3)
    ax.plot([x_end, x_end], [y_top, bracket_y], color=color, lw=0.8, zorder=3)
    ax.plot([x_start, x_end], [bracket_y, bracket_y], color=color, lw=0.8, zorder=3)
    ax.text(mid, bracket_y + 0.08, label, ha='center', va='bottom',
            fontsize=9, color=color, zorder=3)


def plot_pilot_comparison():
    # Patterns
    # 前置式: 4 pilot blocks at start, rest data
    preamble = ['p'] * 4 + ['d'] * (N_BLOCKS - 4)
    # 均匀式: pilots every 4 blocks
    uniform = []
    for i in range(N_BLOCKS):
        if i % 4 == 0:
            uniform.append('p')
        else:
            uniform.append('d')

    block_w = 1.0
    block_h = 0.55
    gap = 0.8  # vertical gap between two rows
    y_preamble = 1.0
    y_uniform = y_preamble - block_h - gap

    fig_w = N_BLOCKS * block_w + 1.5
    fig_h = abs(y_uniform) + block_h + 1.5
    fig, ax = plt.subplots(figsize=(fig_w * 0.38, fig_h * 0.45))

    # Draw blocks
    draw_blocks(ax, y_preamble, preamble, block_w, block_h)
    draw_blocks(ax, y_uniform, uniform, block_w, block_h)

    # Row labels (left side)
    ax.text(-0.5, y_preamble + block_h / 2, '前置式导频',
            ha='right', va='center', fontsize=10, color=LABEL_COLOR,
            fontweight='bold')
    ax.text(-0.5, y_uniform + block_h / 2, '均匀式导频',
            ha='right', va='center', fontsize=10, color=LABEL_COLOR,
            fontweight='bold')

    # Brackets for preamble pattern
    pilot_end = 4 * block_w * 0.92
    add_bracket(ax, 0, pilot_end, y_preamble + block_h, '导频')
    add_bracket(ax, pilot_end + 0.08, (N_BLOCKS - 1) * block_w + block_w * 0.92,
                y_preamble + block_h, '数据')

    # Brackets for uniform pattern — one period
    period_end = 4 * block_w * 0.92
    add_bracket(ax, 0, block_w * 0.92, y_uniform + block_h, '导频')
    add_bracket(ax, block_w, period_end, y_uniform + block_h, '数据')
    # Mark repeating structure
    ax.annotate('', xy=(period_end + 0.3, y_uniform + block_h / 2),
                xytext=(period_end + 0.1, y_uniform + block_h / 2),
                arrowprops=dict(arrowstyle='->', color=LABEL_COLOR, lw=1))
    ax.text(period_end + 0.6, y_uniform + block_h / 2, '重复',
            ha='left', va='center', fontsize=8, color=LABEL_COLOR)

    ax.set_xlim(-3.2, N_BLOCKS * block_w + 0.5)
    ax.set_ylim(y_uniform - 0.3, y_preamble + block_h + 0.8)
    ax.set_aspect('equal')
    ax.axis('off')

    fig.tight_layout(pad=0.3)
    out = os.path.join(FIG_DIR, '导频图案对比.png')
    fig.savefig(out, dpi=300, bbox_inches='tight')
    print(f"Saved: {out}")
    plt.close(fig)

    import shutil
    out_png = os.path.join(FIG_DIR, 'png', '导频图案对比.png')
    shutil.copy2(out, out_png)
    print(f"Copied to: {out_png}")


if __name__ == '__main__':
    plot_pilot_comparison()
