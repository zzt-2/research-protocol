"""Generate the editable Ch4 method-flow SVG and its PNG preview."""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


HERE = Path(__file__).resolve().parent
FIGURE_DIR = HERE / "figures"


def box(ax, x, y, w, h, text, face, edge, *, size=9.0, weight="normal", linestyle="solid"):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.035",
        facecolor=face,
        edgecolor=edge,
        linewidth=1.25,
        linestyle=linestyle,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, weight=weight)
    return patch


def arrow(ax, start, end, color, *, style="solid", width=1.7, mutation=11):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=mutation,
            linewidth=width,
            color=color,
            linestyle=style,
            shrinkA=2,
            shrinkB=2,
        )
    )


def main() -> int:
    mpl.rcParams["svg.hashsalt"] = "ch4-direction-scale-method-flow-v2"
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
            "svg.fonttype": "none",
            "axes.unicode_minus": False,
        }
    )
    blue, orange, green, purple, ink = "#23658C", "#BC6428", "#2D7657", "#6A5687", "#263746"
    pale_blue, pale_orange, pale_green, pale_purple = "#EAF3F8", "#FFF3E8", "#ECF6F0", "#F2EEF7"

    fig, ax = plt.subplots(figsize=(14.0, 6.5))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6.5)
    ax.axis("off")
    ax.add_patch(
        FancyBboxPatch(
            (0.08, 0.12),
            13.84,
            6.18,
            boxstyle="round,pad=0.03,rounding_size=0.14",
            facecolor="#FBFCFD",
            edgecolor="#CBD5DF",
            linewidth=1.0,
        )
    )

    ax.text(0.30, 6.02, "短导频驱动的方向—尺度解耦偏振解复用", color=ink, fontsize=12.0, weight="bold")
    ax.text(13.68, 6.02, "目标场景：静态 2×2 酉混合 + 公共尺度", ha="right", fontsize=8.2, color="#59636D")

    box(ax, 0.35, 3.95, 1.25, 1.05, "接收导频\n$X_p,\;Y_p$", pale_orange, orange, size=9.8, weight="bold")
    box(
        ax,
        1.95,
        3.86,
        2.25,
        1.23,
        "无约束导频 LS\n$\\hat H_{LS}=Y_pX_p^H$\n$\\cdot(X_pX_p^H)^{-1}$",
        "#FFF9F2",
        orange,
        size=9.0,
        weight="bold",
    )
    box(
        ax,
        4.55,
        3.74,
        2.30,
        1.48,
        "共同方向提取\n$\\hat H_{LS}=U\\,\\mathrm{diag}(s_1,s_2)V^H$\n$Q=UV^H$",
        "#FFF8F0",
        orange,
        size=9.0,
        weight="bold",
    )
    arrow(ax, (1.60, 4.48), (1.95, 4.48), orange, style="dashdot", width=1.7)
    arrow(ax, (4.20, 4.48), (4.55, 4.48), orange, style="dashdot", width=1.7)

    ax.text(8.53, 5.68, "并列实验支路，非运行时切换", ha="center", fontsize=8.7, color="#5A4A3D", weight="bold")
    box(
        ax,
        7.20,
        4.45,
        2.62,
        0.95,
        "前向误差尺度（主方法）\n$\\hat g_F=(s_1+s_2)/2$\n$W_F=Q^H/\\hat g_F$",
        pale_green,
        green,
        size=8.5,
        weight="bold",
    )
    box(
        ax,
        7.20,
        3.08,
        2.62,
        1.10,
        "导频重构尺度（强变体）\n$W_0=Q^H/s_1$\n$\\hat a=\\max(0,\\mathrm{Re}\\langle W_0Y_p,X_p\\rangle_F/\\|W_0Y_p\\|_F^2)$\n$W_P=\\hat aW_0$",
        pale_purple,
        purple,
        size=7.55,
        weight="bold",
        linestyle="dashdot",
    )
    box(
        ax,
        7.20,
        1.72,
        2.62,
        1.05,
        "独立调参奇异值下限（基线）\n$\\tilde s_i=\\max(s_i,\\tau s_1)$\n$W_\\tau=V\\,\\mathrm{diag}(1/\\tilde s_i)U^H$",
        pale_blue,
        blue,
        size=8.0,
        weight="bold",
        linestyle="dashed",
    )

    for y in (4.93, 3.63, 2.25):
        arrow(ax, (6.85, 4.48), (7.20, y), orange, style="dashdot", width=1.45)

    box(ax, 10.18, 2.78, 1.28, 1.05, "当前比较支路\n$Z=WY$", "#F3F8FB", ink, size=9.0, weight="bold")
    for y in (4.93, 3.63, 2.25):
        arrow(ax, (9.82, y), (10.18, 3.30), ink, style="dotted", width=1.25)

    box(ax, 0.35, 0.72, 2.25, 0.90, "双偏振载荷\n$Y=[y_x,y_y]^T$", pale_blue, blue, size=9.6, weight="bold")
    ax.plot([2.60, 10.82], [1.17, 1.17], color=blue, linewidth=2.1)
    arrow(ax, (10.82, 1.17), (10.82, 2.78), blue, width=2.1)

    ax.add_patch(
        FancyBboxPatch(
            (11.82, 0.55),
            1.84,
            2.32,
            boxstyle="round,pad=0.03,rounding_size=0.06",
            facecolor="#FAFBFC",
            edgecolor="#6A7680",
            linewidth=1.1,
            linestyle="dashed",
        )
    )
    ax.text(12.74, 2.61, "Ch3 每偏振 CPR 接口", ha="center", fontsize=8.2, weight="bold", color="#4D5963")
    ax.text(12.74, 0.74, "模块接口；未联合验证", ha="center", fontsize=7.7, color="#6A3E35")
    box(ax, 12.02, 1.42, 0.68, 0.60, "$z_x$\nCPR", pale_green, green, size=7.8, weight="bold")
    box(ax, 12.82, 1.42, 0.64, 0.60, "$z_y$\nCPR", pale_green, green, size=7.8, weight="bold")
    arrow(ax, (11.46, 3.40), (12.36, 2.02), blue, width=1.55)
    arrow(ax, (11.46, 3.16), (13.14, 2.02), blue, width=1.55)

    ax.text(
        0.38,
        0.28,
        "蓝色实线：载荷数据流    橙色点划线：导频估计/参数控制    支路线型：主方法 / 强变体 / 调参基线",
        fontsize=8.0,
        color="#59636D",
    )

    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    svg_path = FIGURE_DIR / "ch4-method-flow.svg"
    png_path = FIGURE_DIR / "ch4-method-flow.png"
    fig.savefig(svg_path, bbox_inches="tight", pad_inches=0.03, metadata={"Date": None, "Creator": "Ch4 method figure generator"})
    fig.savefig(png_path, dpi=200, bbox_inches="tight", pad_inches=0.03, metadata={"Software": "Ch4 method figure generator"})
    plt.close(fig)
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text("\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n", encoding="utf-8")
    print("PASS: editable method SVG and PNG preview generated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
