"""
生成开题报告插图: Gamma-Gamma PDF / 导频图案对比 / 实验递进关系图
执行: ~/.venvs/torch/bin/python plot_p009_figures.py
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.font_manager import FontProperties
from scipy.special import gamma as gamma_func, kv
import os

# ── 全局字体: 从 Windows Fonts 直接加载 SimHei ──
_FONT_PATH = "/mnt/c/Windows/Fonts/simhei.ttf"
if os.path.exists(_FONT_PATH):
    _zh_font = FontProperties(fname=_FONT_PATH)
    # 同时注册到 matplotlib 全局，避免逐个传 fontproperties
    from matplotlib.font_manager import fontManager
    fontManager.addfont(_FONT_PATH)
    plt.rcParams["font.sans-serif"] = ["SimHei"] + plt.rcParams["font.sans-serif"]
else:
    _zh_font = FontProperties()
    plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


# ═══════════════════════════════════════════════════════════════
# 图1: Gamma-Gamma 三档湍流 PDF 曲线对比
# ═══════════════════════════════════════════════════════════════
def plot_fig_gg_pdf():
    fig, ax = plt.subplots(figsize=(8, 5))

    h = np.linspace(0.001, 4.0, 2000)

    configs = [
        (4.0, 3.0, "弱湍流 (α=4.0, β=3.0)", "royalblue", "-"),
        (2.5, 1.8, "中等湍流 (α=2.5, β=1.8)", "seagreen", "--"),
        (1.5, 0.8, "强湍流 (α=1.5, β=0.8)", "crimson", ":"),
    ]

    for alpha, beta, label, color, ls in configs:
        coef = 2.0 * (alpha * beta) ** ((alpha + beta) / 2.0) / (
            gamma_func(alpha) * gamma_func(beta)
        )
        exponent = (alpha + beta) / 2.0 - 1.0
        bessel_arg = 2.0 * np.sqrt(alpha * beta * h)
        pdf = coef * h**exponent * kv(np.abs(alpha - beta), bessel_arg)
        ax.plot(h, pdf, color=color, linestyle=ls, linewidth=2.2, label=label)

    ax.set_xlim(0, 4)
    ax.set_ylim(bottom=0)
    ax.set_xlabel("归一化辐照度 $h$", fontsize=13)
    ax.set_ylabel("概率密度 $f(h)$", fontsize=13)
    ax.legend(loc="upper right", fontsize=11, framealpha=0.9)
    ax.tick_params(labelsize=11)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    path = os.path.join(OUT_DIR, "fig_gg_pdf.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print(f"[OK] {path}")


# ═══════════════════════════════════════════════════════════════
# 图2: 导频图案对比示意图
# ═══════════════════════════════════════════════════════════════
def plot_fig_pilot_pattern():
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(-1.5, 21)
    ax.set_ylim(-1.0, 5.0)
    ax.set_aspect("equal")
    ax.axis("off")

    bw = 0.82   # 方块宽
    bh = 0.82   # 方块高
    gap = 0.12  # 方块间距
    pilot_color = "#3B6B8A"   # 深蓝灰 (导频)
    data_color  = "#D0D8E0"   # 浅灰 (数据)
    text_color  = "#222222"

    total_slots = 20

    def draw_blocks(y_center, is_pilot_func, label_text):
        """在 y_center 水平线上画一排方块，返回起始 x"""
        for i in range(total_slots):
            x = i * (bw + gap)
            color = pilot_color if is_pilot_func(i) else data_color
            rect = mpatches.FancyBboxPatch(
                (x, y_center - bh / 2), bw, bh,
                boxstyle="round,pad=0.04",
                facecolor=color, edgecolor="#555555", linewidth=0.7,
            )
            ax.add_patch(rect)
        # 左侧标签
        ax.text(
            -0.5, y_center, label_text,
            fontsize=12, fontweight="bold", color=text_color,
            ha="right", va="center",
        )

    # ── 上行: 前置式导频 ──
    y_top = 3.2
    n_pilot_front = 4
    draw_blocks(y_top, lambda i: i < n_pilot_front, "前置式导频")

    # "帧"标注 (上方)
    ax.annotate(
        "帧", xy=(0, y_top + bh / 2 + 0.08),
        xytext=(-1.2, y_top + bh / 2 + 0.55),
        fontsize=12, fontweight="bold", color=text_color,
        ha="center",
        arrowprops=dict(arrowstyle="-[, widthB=8.0", lw=1.2, color=text_color),
    )

    # 导频/数据 标注
    mid_pilot = (n_pilot_front - 1) * (bw + gap) / 2 + bw / 2
    ax.text(mid_pilot, y_top + bh / 2 + 0.15, "导频",
            fontsize=10, color=pilot_color, ha="center", va="bottom", fontweight="bold")
    mid_data_top = (n_pilot_front + total_slots - 1) * (bw + gap) / 2
    ax.text(mid_data_top, y_top + bh / 2 + 0.15, "数据",
            fontsize=10, color="#666666", ha="center", va="bottom")

    # ── 下行: 均匀式导频 ──
    y_bot = 1.0
    spacing = 5  # 每 5 个符号插一个导频
    draw_blocks(y_bot, lambda i: i % spacing == 0, "均匀式导频")

    # 间隔标注
    for k in range(min(3, total_slots // spacing)):
        x_start = k * spacing * (bw + gap)
        x_end = (k * spacing + spacing - 1) * (bw + gap) + bw
        y_arrow = y_bot - bh / 2 - 0.25
        if k == 0:
            # 在第一个间隔处标注 Δf
            ax.annotate(
                "", xy=(x_end, y_arrow), xytext=(x_start, y_arrow),
                arrowprops=dict(arrowstyle="<->", color="#B03030", lw=1.3),
            )
            ax.text(
                (x_start + x_end) / 2, y_arrow - 0.18,
                f"间隔 Δf = {spacing}",
                fontsize=10, color="#B03030", ha="center", va="top", fontweight="bold",
            )
        # 导频小标注
        px = k * spacing * (bw + gap) + bw / 2
        ax.text(px, y_bot - bh / 2 - 0.08, "P", fontsize=8, color=pilot_color,
                ha="center", va="top", fontstyle="italic")

    # 图例
    legend_pilot = mpatches.Patch(facecolor=pilot_color, edgecolor="#555555", label="导频符号")
    legend_data  = mpatches.Patch(facecolor=data_color,  edgecolor="#555555", label="数据符号")
    ax.legend(
        handles=[legend_pilot, legend_data],
        loc="lower right", fontsize=10, framealpha=0.9,
        bbox_to_anchor=(0.98, 0.02),
    )

    fig.tight_layout()
    path = os.path.join(OUT_DIR, "fig_pilot_pattern.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print(f"[OK] {path}")


# ═══════════════════════════════════════════════════════════════
# 图3: 三组10实验递进关系图
# ═══════════════════════════════════════════════════════════════
def plot_fig_experiment_dag():
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_xlim(-0.5, 14.5)
    ax.set_ylim(-0.5, 6.0)
    ax.set_aspect("equal")
    ax.axis("off")

    # 配色
    group_colors = ["#4A7FB5", "#5A9E6F", "#C07830"]   # 蓝/绿/橙
    box_color    = "#FFFFFF"
    border_color = "#666666"
    arrow_color  = "#444444"

    # 三组定义
    groups = [
        {
            "title": "组A: 信道估计精度\n与接收性能影响",
            "color": group_colors[0],
            "cx": 2.0,   # 组中心 x
            "experiments": [
                ("E1", "NMSE基线"),
                ("E2", "NMSE-BER\n灵敏度"),
                ("E3", "调制格式\n灵敏度"),
                ("E4", "16-QAM\n同步"),
            ],
        },
        {
            "title": "组B: 载波同步性能\n分析与设计准则",
            "color": group_colors[1],
            "cx": 7.0,
            "experiments": [
                ("E5", "BER-SNR\n曲线"),
                ("E6", "参数扫描+\n噪声解耦"),
                ("E7", "DPLL\n解析准则"),
                ("E8", "联合验证+\n失锁恢复"),
            ],
        },
        {
            "title": "组C: 扩展验证\n与系统级实验",
            "color": group_colors[2],
            "cx": 12.0,
            "experiments": [
                ("E9", "LDPC\n编码增益"),
                ("E10", "编码辅助\n载波恢复"),
            ],
        },
    ]

    bw = 1.55   # 实验框宽
    bh = 0.85   # 实验框高
    x_gap = 0.25
    y_center = 2.0

    group_rects = []

    for gi, g in enumerate(groups):
        n = len(g["experiments"])
        total_w = n * bw + (n - 1) * x_gap
        x_start = g["cx"] - total_w / 2

        # 组外框 (圆角矩形)
        gx0 = x_start - 0.35
        gy0 = y_center - bh / 2 - 0.55
        gw = total_w + 0.70
        gh = bh + 2.8
        group_bg = FancyBboxPatch(
            (gx0, gy0), gw, gh,
            boxstyle="round,pad=0.15",
            facecolor=g["color"], alpha=0.12,
            edgecolor=g["color"], linewidth=2.0,
        )
        ax.add_patch(group_bg)
        group_rects.append((gx0, gy0, gw, gh))

        # 组标题
        ax.text(
            g["cx"], y_center + bh / 2 + 1.85,
            g["title"],
            fontsize=11, fontweight="bold",
            color=g["color"], ha="center", va="center",
            linespacing=1.3,
        )

        # 实验方框
        prev_x_center = None
        for ei, (eid, elabel) in enumerate(g["experiments"]):
            ex = x_start + ei * (bw + x_gap)
            ey = y_center - bh / 2

            # 实验框
            exp_box = FancyBboxPatch(
                (ex, ey), bw, bh,
                boxstyle="round,pad=0.06",
                facecolor=box_color, edgecolor=g["color"],
                linewidth=1.3,
            )
            ax.add_patch(exp_box)

            # 实验编号 + 说明
            ax.text(ex + bw / 2, ey + bh * 0.62, eid,
                    fontsize=10, fontweight="bold", color=g["color"],
                    ha="center", va="center")
            ax.text(ex + bw / 2, ey + bh * 0.28, elabel,
                    fontsize=7.5, color="#333333",
                    ha="center", va="center", linespacing=1.1)

            cur_x_center = ex + bw / 2

            # 组内箭头 E_i -> E_{i+1}
            if prev_x_center is not None:
                ax.annotate(
                    "",
                    xy=(ex - 0.02, y_center),
                    xytext=(prev_x_center + bw / 2 + 0.02, y_center),
                    arrowprops=dict(
                        arrowstyle="-|>", color=g["color"],
                        lw=1.4, mutation_scale=12,
                    ),
                )
            prev_x_center = ex + bw / 2  # keep for next arrow

    # ── 组间箭头 A→B ──
    a_right = group_rects[0][0] + group_rects[0][2]
    b_left  = group_rects[1][0]
    ax.annotate(
        "",
        xy=(b_left + 0.1, y_center + 0.3),
        xytext=(a_right - 0.1, y_center + 0.3),
        arrowprops=dict(
            arrowstyle="-|>", color=arrow_color, lw=2.0, mutation_scale=15,
        ),
    )
    ax.text(
        (a_right + b_left) / 2, y_center + 0.75,
        "NMSE基线与\n灵敏度阈值",
        fontsize=9, color=arrow_color, ha="center", va="bottom",
        fontweight="bold", linespacing=1.2,
    )

    # ── 组间箭头 B→C ──
    b_right = group_rects[1][0] + group_rects[1][2]
    c_left  = group_rects[2][0]
    ax.annotate(
        "",
        xy=(c_left + 0.1, y_center + 0.3),
        xytext=(b_right - 0.1, y_center + 0.3),
        arrowprops=dict(
            arrowstyle="-|>", color=arrow_color, lw=2.0, mutation_scale=15,
        ),
    )
    ax.text(
        (b_right + c_left) / 2, y_center + 0.75,
        "未编码\nBER曲线",
        fontsize=9, color=arrow_color, ha="center", va="bottom",
        fontweight="bold", linespacing=1.2,
    )

    fig.tight_layout()
    path = os.path.join(OUT_DIR, "fig_experiment_dag.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print(f"[OK] {path}")


# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    plot_fig_gg_pdf()
    plot_fig_pilot_pattern()
    plot_fig_experiment_dag()
    print("\nAll 3 figures generated.")
