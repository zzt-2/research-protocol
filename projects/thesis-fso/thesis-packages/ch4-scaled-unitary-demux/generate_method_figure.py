"""Generate the editable Ch4 method-flow SVG and its PNG preview."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


HERE = Path(__file__).resolve().parent
FIGURE_DIR = HERE / "figures"


def box(ax, x, y, w, h, text, face, edge, size=10, weight="normal"):
    patch = FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.03",
        facecolor=face, edgecolor=edge, linewidth=1.25
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, weight=weight)
    return patch


def arrow(ax, start, end, color, style="solid", width=1.7, mutation=11):
    ax.add_patch(FancyArrowPatch(
        start, end, arrowstyle="-|>", mutation_scale=mutation,
        linewidth=width, color=color, linestyle=style, shrinkA=2, shrinkB=2
    ))


def main() -> int:
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
        "svg.fonttype": "none",
        "axes.unicode_minus": False,
    })
    blue, orange, green, ink = "#23658C", "#C96B28", "#2D7A59", "#263746"
    pale_blue, pale_orange, pale_green = "#EAF3F8", "#FFF3E8", "#ECF6F0"
    fig, ax = plt.subplots(figsize=(11.0, 5.1))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5.1)
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.08, 0.15), 10.84, 4.8, boxstyle="round,pad=0.03,rounding_size=0.14", facecolor="#FBFCFD", edgecolor="#CBD5DF", linewidth=1.0))
    ax.axhspan(0.45, 2.25, color=pale_blue, alpha=0.88)
    ax.axhspan(2.30, 4.65, color=pale_orange, alpha=0.76)
    ax.text(0.30, 4.42, "短导频估计与控制流", color=orange, fontsize=11, weight="bold")
    ax.text(0.30, 1.98, "双偏振载荷数据流", color=blue, fontsize=11, weight="bold")
    ax.text(10.66, 4.66, "目标验证场景：静态 2×2 酉混合 + 公共尺度", ha="right", fontsize=8.2, color="#59636D")

    box(ax, 0.40, 2.35, 1.35, 1.15, "双偏振接收块\n$[r_x,r_y]^T$", "#F4F7F9", ink, 10, "bold")
    box(ax, 2.05, 3.18, 1.40, 0.78, "短平衡导频\n$X_p,\;Y_p$", "#FFF9F2", orange, 9.5)
    box(ax, 2.05, 1.02, 1.40, 0.78, "双偏振载荷\n$y=[y_x,y_y]^T$", "#F5FAFD", blue, 9.5)
    box(ax, 3.85, 3.18, 1.28, 0.78, "pilot-LS\n$\\hat H_{LS}$", "#FFF9F2", orange, 10, "bold")
    box(ax, 5.48, 2.92, 2.05, 1.30, "2×2 SVD 与缩放酉投影\n$\\hat H_{LS}=U\\Sigma V^H$\n$\\hat g=(s_1+s_2)/2$\n$\\hat H_{SU}=\\hat gUV^H$", "#FFF7EE", orange, 9.4, "bold")
    box(ax, 7.93, 1.02, 1.48, 1.18, "逆矩阵解复用\n$W=VU^H/\\hat g$\n$z=Wy$", "#F2F8F5", green, 9.8, "bold")
    box(ax, 9.72, 1.46, 0.92, 0.60, "Ch3 CPR\nX 路", pale_green, green, 8.8, "bold")
    box(ax, 9.72, 0.63, 0.92, 0.60, "Ch3 CPR\nY 路", pale_green, green, 8.8, "bold")

    arrow(ax, (1.75, 3.05), (2.05, 3.57), orange, "dashdot", 1.5)
    arrow(ax, (1.75, 2.65), (2.05, 1.41), blue, "solid", 2.2)
    arrow(ax, (3.45, 3.57), (3.85, 3.57), orange, "dashdot", 1.6)
    arrow(ax, (5.13, 3.57), (5.48, 3.57), orange, "dashdot", 1.6)
    arrow(ax, (6.50, 2.92), (8.37, 2.20), orange, "dashdot", 1.6)
    ax.text(7.75, 2.70, "估计 $W$", color=orange, fontsize=8.5, ha="center")
    arrow(ax, (3.45, 1.41), (7.93, 1.41), blue, "solid", 2.2)
    arrow(ax, (9.41, 1.67), (9.72, 1.76), blue, "solid", 1.9)
    arrow(ax, (9.41, 1.39), (9.72, 0.93), blue, "solid", 1.9)
    arrow(ax, (10.64, 1.76), (10.88, 1.76), blue, "solid", 1.8)
    arrow(ax, (10.64, 0.93), (10.88, 0.93), blue, "solid", 1.8)
    ax.text(10.88, 1.76, "$\\hat s_x$", va="center", fontsize=9, color=blue)
    ax.text(10.88, 0.93, "$\\hat s_y$", va="center", fontsize=9, color=blue)
    ax.text(2.08, 2.50, "可见诊断：$\\rho=s_1/s_2$；仅报告适用性，不驱动本章分支", fontsize=8.3, color="#6B4A31")
    ax.plot([0.35, 10.65], [2.27, 2.27], color="#D5DDE5", linewidth=0.9)
    ax.text(0.34, 0.27, "蓝色实线：载荷数据流    橙色点划线：导频估计/参数控制流", fontsize=8.3, color="#59636D")

    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURE_DIR / "ch4-method-flow.svg", bbox_inches="tight", pad_inches=0.03)
    fig.savefig(FIGURE_DIR / "ch4-method-flow.png", dpi=200, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)
    print("PASS: editable method SVG and PNG preview generated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
