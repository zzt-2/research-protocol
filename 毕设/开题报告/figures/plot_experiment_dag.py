#!/usr/bin/env python3
"""Generate experiment DAG figure in Visio engineering style."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.path import Path
import numpy as np

# Visio style colors
BOX_COLOR = '#FFFFFF'
BOX_EDGE = '#333333'
GROUP_COLOR = '#F0F0F0'
TEXT_COLOR = '#000000'
ARROW_COLOR = '#333333'
CROSS_ARROW_COLOR = '#888888'
LABEL_COLOR = '#666666'

# No CJK fonts available, use English
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(1, 1, figsize=(14, 8))
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.axis('off')
fig.patch.set_facecolor('white')


def draw_exp_box(ax, x, y, w, h, label, title):
    """Draw a white rounded rectangle experiment box."""
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        facecolor=BOX_COLOR, edgecolor=BOX_EDGE, linewidth=1.5,
        zorder=3
    )
    ax.add_patch(box)
    ax.text(x + w/2, y + h*0.65, label, ha='center', va='center',
            fontsize=10, fontweight='bold', color=TEXT_COLOR, zorder=4)
    ax.text(x + w/2, y + h*0.28, title, ha='center', va='center',
            fontsize=7.5, color=TEXT_COLOR, zorder=4)


def draw_group_bg(ax, x, y, w, h, title):
    """Draw a light grey group background rectangle."""
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.05,rounding_size=0.05",
        facecolor=GROUP_COLOR, edgecolor='#BBBBBB', linewidth=1.0,
        zorder=1
    )
    ax.add_patch(box)
    ax.text(x + w/2, y + h - 0.15, title, ha='center', va='top',
            fontsize=10, fontweight='bold', color='#555555', zorder=2)


def draw_vert_arrow(ax, x, y1, y2, color=ARROW_COLOR, lw=1.5):
    """Draw a vertical arrow from (x,y1) down to (x,y2)."""
    ax.annotate('',
        xy=(x, y2), xytext=(x, y1),
        arrowprops=dict(
            arrowstyle='-|>', color=color, lw=lw,
            shrinkA=4, shrinkB=4,
            mutation_scale=12,
        ),
        zorder=2
    )


def draw_l_arrow(ax, x1, y1, x2, y2, label='', color=CROSS_ARROW_COLOR, lw=1.2):
    """Draw an L-shaped dashed arrow: right then down, or right then up."""
    mid_x = (x1 + x2) / 2
    # Horizontal segment then vertical segment
    ax.plot([x1, mid_x], [y1, y1], color=color, lw=lw, linestyle='--', zorder=2)
    ax.plot([mid_x, mid_x], [y1, y2], color=color, lw=lw, linestyle='--', zorder=2)
    # Arrowhead at end
    ax.annotate('',
        xy=(x2, y2), xytext=(mid_x, y2),
        arrowprops=dict(
            arrowstyle='-|>', color=color, lw=lw,
            shrinkA=0, shrinkB=4,
            mutation_scale=10,
        ),
        zorder=2
    )
    if label:
        ax.text(mid_x, (y1 + y2) / 2 + 0.1, label, ha='center', va='bottom',
                fontsize=7, color=LABEL_COLOR, fontstyle='italic', zorder=4,
                rotation=0)


# Box dimensions
W = 3.5
H = 0.9

# --- Group A ---
XA = 0.5
draw_group_bg(ax, XA - 0.15, 2.3, W + 0.3, 5.4, 'Group A: Channel Estimation Accuracy')

E1y = 6.5; E2y = 5.2; E3y = 3.9; E4y = 2.6

draw_exp_box(ax, XA, E1y, W, H, 'E1', 'NMSE Baseline Comparison')
draw_exp_box(ax, XA, E2y, W, H, 'E2', 'NMSE-BER Sensitivity Verification')
draw_exp_box(ax, XA, E3y, W, H, 'E3', 'Modulation Format Sensitivity')
draw_exp_box(ax, XA, E4y, W, H, 'E4', 'Carrier Sync Method Comparison (16-QAM)')

# --- Group B ---
XB = 5.0
draw_group_bg(ax, XB - 0.15, 2.3, W + 0.3, 5.4, 'Group B: Carrier Sync Analysis')

E5y = 6.5; E6y = 5.2; E7y = 3.9; E8y = 2.6

draw_exp_box(ax, XB, E5y, W, H, 'E5', 'Carrier Sync BER-SNR Full Curves')
draw_exp_box(ax, XB, E6y, W, H, 'E6', 'Parameter Sweep & Noise Decoupling')
draw_exp_box(ax, XB, E7y, W, H, 'E7', 'DPLL Analytical Design Guideline')
draw_exp_box(ax, XB, E8y, W, H, 'E8', 'Joint Design Space & Unlock Recovery')

# --- Group C ---
XC = 9.5
draw_group_bg(ax, XC - 0.15, 2.9, W + 0.3, 3.6, 'Group C: System-Level Validation')

E9y = 5.2; E10y = 3.2

draw_exp_box(ax, XC, E9y, W, H, 'E9', 'LDPC Coding Gain Baseline')
draw_exp_box(ax, XC, E10y, W, H, 'E10', 'Code-Aided Iterative Carrier Recovery')

# --- Arrows ---
# Group A internal (vertical, solid)
draw_vert_arrow(ax, XA + W/2, E1y, E2y + H)
draw_vert_arrow(ax, XA + W/2, E2y, E3y + H)
draw_vert_arrow(ax, XA + W/2, E3y, E4y + H)

# Group B internal (vertical, solid)
draw_vert_arrow(ax, XB + W/2, E5y, E6y + H)
draw_vert_arrow(ax, XB + W/2, E6y, E7y + H)
draw_vert_arrow(ax, XB + W/2, E7y, E8y + H)

# Group C internal (vertical, solid)
draw_vert_arrow(ax, XC + W/2, E9y, E10y + H)

# Cross-group arrows (dashed, L-shaped)
# E2 -> E5: from E2 right edge to E5 left edge (E2 y-center -> E5 y-center)
draw_l_arrow(ax, XA + W, E2y + H/2, XB, E5y + H/2, label='NMSE baseline')

# E4 -> E8: from E4 right edge to E8 left edge
draw_l_arrow(ax, XA + W, E4y + H/2, XB, E8y + H/2, label='Sync method')

# E5 -> E9: from E5 right edge to E9 left edge
draw_l_arrow(ax, XB + W, E5y + H/2, XC, E9y + H/2, label='Uncoded BER')

# E8 -> E10: from E8 right edge to E10 left edge
draw_l_arrow(ax, XB + W, E8y + H/2, XC, E10y + H/2, label='DPLL params')

plt.savefig('/mnt/d/code/study/research-protocol/毕设/开题报告/figures/fig_experiment_dag.png',
            dpi=300, bbox_inches='tight', facecolor='white')
print('Saved fig_experiment_dag.png')
