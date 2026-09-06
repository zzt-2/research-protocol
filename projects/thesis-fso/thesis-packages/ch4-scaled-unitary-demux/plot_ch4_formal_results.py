"""Generate publication-style Ch4 figures from the materialized formal CSVs."""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / "data"
FIGURE_DIR = HERE / "figures"
ENGINEERING_BER = 3.8e-3

METHOD_ORDER = ("B0", "B2_TUNED", "C4_FWD", "B3_PSC", "O1")
METHOD_NAMES = {
    "B0": "普通 LS",
    "B2_TUNED": "调参奇异值下限",
    "C4_FWD": "前向误差尺度",
    "B3_PSC": "导频重构尺度",
    "O1": "理想 CSI 参考（理论）",
}
STYLES = {
    "B0": dict(color="#6B7280", linestyle=":", marker="o", linewidth=1.25),
    "B2_TUNED": dict(color="#1F4E79", linestyle="-", marker="s", linewidth=1.45),
    "C4_FWD": dict(color="#D55E00", linestyle="-", marker="D", linewidth=1.65),
    "B3_PSC": dict(color="#009E73", linestyle="--", marker="^", linewidth=1.45),
    "O1": dict(color="#A0A4A8", linestyle="-.", marker="x", linewidth=1.05, alpha=0.72),
}
SCENE_NAMES = {"weak": "弱湍流", "moderate": "中等湍流", "strong": "强湍流"}
FIGURE_STEMS = (
    "ch4-formal-ber-curves",
    "ch4-formal-required-snr-gain",
    "ch4-formal-pilot-sensitivity",
    "ch4-formal-mechanism",
    "ch4-formal-robustness-boundary",
)


def configure_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "DejaVu Sans"],
            "axes.unicode_minus": False,
            "svg.fonttype": "none",
            "svg.hashsalt": "ch4-formal-figures-v1",
            "font.size": 8.5,
            "axes.titlesize": 9.5,
            "axes.labelsize": 9.0,
            "legend.fontsize": 7.7,
            "xtick.labelsize": 8.0,
            "ytick.labelsize": 8.0,
            "axes.linewidth": 0.8,
            "lines.markersize": 4.1,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )


def read_csv(name: str) -> list[dict[str, str]]:
    path = DATA_DIR / name
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"empty materialized data file: {path}")
    return rows


def f(row: dict[str, str], key: str) -> float:
    value = row[key]
    if value == "":
        return math.nan
    return float(value)


def add_grid(ax: plt.Axes, axis: str = "both") -> None:
    ax.grid(axis=axis, which="major", color="#D9DEE3", linewidth=0.6, alpha=0.85)
    ax.grid(axis=axis, which="minor", color="#EDF0F2", linewidth=0.45, alpha=0.75)
    ax.spines[["top", "right"]].set_visible(False)


def plot_line(
    ax: plt.Axes,
    x: Iterable[float],
    y: Iterable[float],
    method: str,
    *,
    label: str | None = None,
    markevery: int = 2,
) -> None:
    style = dict(STYLES[method])
    style.update(markerfacecolor="white", markeredgewidth=0.9, markevery=markevery)
    ax.plot(list(x), list(y), label=label or METHOD_NAMES[method], **style)


def save_figure(fig: plt.Figure, stem: str) -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    metadata = {"Creator": "Matplotlib", "Date": None}
    fig.savefig(FIGURE_DIR / f"{stem}.svg", bbox_inches="tight", metadata=metadata)
    fig.savefig(FIGURE_DIR / f"{stem}.png", dpi=240, bbox_inches="tight", metadata={"Software": "Matplotlib"})
    plt.close(fig)


def group_rows(rows: list[dict[str, str]], keys: tuple[str, ...]) -> dict[tuple[str, ...], list[dict[str, str]]]:
    grouped: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(row[key] for key in keys)].append(row)
    return grouped


def crossing(curve: list[tuple[float, float]]) -> tuple[str, float | None]:
    curve = sorted(curve)
    if curve[0][1] <= ENGINEERING_BER:
        return "BELOW_RANGE", None
    downward = [
        i
        for i in range(1, len(curve))
        if curve[i - 1][1] > ENGINEERING_BER and curve[i][1] <= ENGINEERING_BER
    ]
    if not downward:
        return "UNREACHED", None
    first = downward[0]
    upward = any(
        curve[i - 1][1] <= ENGINEERING_BER and curve[i][1] > ENGINEERING_BER
        for i in range(first + 1, len(curve))
    )
    if len(downward) != 1 or upward:
        return "UNSTABLE", None
    x0, y0 = curve[first - 1]
    x1, y1 = curve[first]
    if y1 == ENGINEERING_BER:
        return "STABLE", x1
    target = math.log10(ENGINEERING_BER)
    return "STABLE", x0 + (target - math.log10(y0)) * (x1 - x0) / (math.log10(y1) - math.log10(y0))


def plot_ber_curves(rows: list[dict[str, str]]) -> None:
    grouped = group_rows(rows, ("scene", "n_pilots", "method_code"))
    fig, axes = plt.subplots(1, 2, figsize=(7.25, 3.25), sharey=True, constrained_layout=True)
    for ax, n_pilots in zip(axes, (2, 4)):
        for method in METHOD_ORDER:
            group = sorted(grouped[("moderate", str(n_pilots), method)], key=lambda row: f(row, "snr_db"))
            if len(group) != 19:
                raise ValueError("formal BER panel requires the complete 5--41 dB grid")
            plot_line(
                ax,
                [f(row, "snr_db") for row in group],
                [f(row, "ber_jeffreys") for row in group],
                method,
                markevery=2,
            )
        ax.axhline(ENGINEERING_BER, color="#4B5563", linestyle=(0, (4, 2)), linewidth=0.9)
        ax.text(5.5, ENGINEERING_BER * 1.35, r"工程参考 BER = $3.8\times10^{-3}$", fontsize=7.2, color="#374151")
        ax.set_title(f"({chr(96 + n_pilots // 2)}) 每偏振导频符号数 $N_p={n_pilots}$")
        ax.set_xlabel("每偏振衰落前数据符号信噪比 / dB")
        ax.set_xlim(5, 41)
        ax.set_xticks(np.arange(5, 42, 4))
        ax.set_yscale("log")
        ax.set_ylim(1e-7, 4e-1)
        add_grid(ax)
    axes[0].set_ylabel("比特误码率（BER）")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="outside lower center", ncol=5, frameon=False)
    fig.suptitle("中等湍流下完整 BER–SNR 曲线（128 个配对随机簇）", fontsize=10.2)
    save_figure(fig, "ch4-formal-ber-curves")


def plot_required_snr_gain(rows: list[dict[str, str]]) -> None:
    order = [("C4_FWD", 2), ("B3_PSC", 2), ("C4_FWD", 4), ("B3_PSC", 4)]
    lookup = {(row["variant_code"], int(row["n_pilots"])): row for row in rows}
    fig, ax = plt.subplots(figsize=(5.9, 3.15), constrained_layout=True)
    x_centers = np.array([0.0, 1.0])
    width = 0.22
    for offset, method in ((-width / 1.7, "C4_FWD"), (width / 1.7, "B3_PSC")):
        selected = [lookup[(method, n)] for n in (2, 4)]
        gains = np.array([f(row, "gain_db") for row in selected])
        lower = gains - np.array([f(row, "ci95_lower_db") for row in selected])
        upper = np.array([f(row, "ci95_upper_db") for row in selected]) - gains
        x = x_centers + offset
        style = STYLES[method]
        ax.errorbar(
            x,
            gains,
            yerr=np.vstack([lower, upper]),
            fmt=style["marker"],
            color=style["color"],
            markerfacecolor="white",
            markeredgewidth=1.1,
            markersize=6.0,
            capsize=4,
            elinewidth=1.25,
            label=METHOD_NAMES[method],
            zorder=3,
        )
        ci_upper = np.array([f(row, "ci95_upper_db") for row in selected])
        for xi, value, upper_bound in zip(x, gains, ci_upper):
            ax.text(xi, upper_bound + 0.035, f"{value:.3f} dB", ha="center", va="bottom", fontsize=7.4, color=style["color"])
    ax.axhline(0.0, color="#374151", linewidth=0.8)
    ax.set_xticks(x_centers, ["$N_p=2$", "$N_p=4$"])
    ax.set_xlim(-0.45, 1.45)
    ax.set_ylim(0.0, 1.25)
    ax.set_ylabel("相对调参奇异值下限的所需 SNR 降低量 / dB")
    ax.set_title("工程参考 BER 下的所需 SNR 增益及 95% 置信区间")
    ax.legend(frameon=False, loc="upper right")
    add_grid(ax, axis="y")
    ax.text(
        0.01,
        0.02,
        "$N_p=4$ 为统计稳定的小幅优势；两种尺度判据结果接近",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=7.2,
        color="#4B5563",
    )
    save_figure(fig, "ch4-formal-required-snr-gain")


def plot_pilot_sensitivity(rows: list[dict[str, str]]) -> None:
    grouped = group_rows(rows, ("method_code",))
    fig, axes = plt.subplots(1, 2, figsize=(7.25, 3.25), constrained_layout=True)
    pilots = [2, 4, 8, 16]
    for method in METHOD_ORDER:
        group = sorted(grouped[(method,)], key=lambda row: int(row["n_pilots"]))
        if [int(row["n_pilots"]) for row in group] != pilots:
            raise ValueError("pilot-sensitivity CSV lacks a complete matched pilot grid")
        stable = [row["crossing_status"] == "STABLE" for row in group]
        if any(stable):
            y = [f(row, "required_snr_db") if ok else math.nan for row, ok in zip(group, stable)]
            plot_line(axes[0], pilots, y, method, markevery=1)
        plot_line(
            axes[1],
            pilots,
            [f(row, "fixed_snr_ber_jeffreys") for row in group],
            method,
            markevery=1,
        )
    axes[0].set_title("(a) 达到工程参考 BER 所需 SNR")
    axes[0].set_ylabel("所需 SNR / dB")
    axes[0].set_ylim(20, 26)
    axes[1].set_title("(b) 固定 25 dB 时的 BER")
    axes[1].set_ylabel("比特误码率（BER）")
    axes[1].set_yscale("log")
    axes[1].set_ylim(1e-4, 1e-2)
    axes[1].axhline(ENGINEERING_BER, color="#4B5563", linestyle=(0, (4, 2)), linewidth=0.9)
    for ax in axes:
        ax.set_xlabel("每偏振导频符号数 $N_p$")
        ax.set_xscale("log", base=2)
        ax.set_xticks(pilots, [str(value) for value in pilots])
        add_grid(ax)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="outside lower center", ncol=5, frameon=False)
    fig.suptitle("中等湍流下的导频长度敏感性（同条件配对）", fontsize=10.2)
    save_figure(fig, "ch4-formal-pilot-sensitivity")


def plot_mechanism(rows: list[dict[str, str]]) -> None:
    subset = [row for row in rows if row["n_pilots"] == "2"]
    grouped = group_rows(subset, ("method_code",))
    fig, axes = plt.subplots(1, 2, figsize=(7.25, 3.25), constrained_layout=True)
    for method in ("B0", "B2_TUNED", "C4_FWD"):
        group = sorted(grouped[(method,)], key=lambda row: f(row, "snr_db"))
        plot_line(
            axes[0],
            [f(row, "snr_db") for row in group],
            [f(row, "channel_nmse_mean") for row in group],
            method,
            markevery=2,
        )
    for method in ("B0", "B2_TUNED", "C4_FWD", "B3_PSC"):
        group = sorted(grouped[(method,)], key=lambda row: f(row, "snr_db"))
        plot_line(
            axes[1],
            [f(row, "snr_db") for row in group],
            [f(row, "inverse_residual_mean") for row in group],
            method,
            markevery=2,
        )
    axes[0].set_title("(a) 直接信道估计的归一化均方误差")
    axes[0].set_ylabel("信道 NMSE")
    axes[1].set_title("(b) 尺度处理后的求逆残差")
    axes[1].set_ylabel("归一化求逆残差")
    for ax in axes:
        ax.set_xlabel("每偏振衰落前数据符号信噪比 / dB")
        ax.set_xlim(5, 41)
        ax.set_xticks(np.arange(5, 42, 4))
        ax.set_yscale("log")
        add_grid(ax)
    for ax in axes:
        ax.legend(frameon=False, loc="upper right")
    fig.suptitle("中等湍流、$N_p=2$ 时的结构约束作用机制", fontsize=10.2)
    axes[0].text(0.02, 0.03, "仅比较直接信道估计量", transform=axes[0].transAxes, fontsize=7.0, color="#70757A")
    save_figure(fig, "ch4-formal-mechanism")


def plot_robustness_boundary(
    curve_rows: list[dict[str, str]], mismatch_rows: list[dict[str, str]]
) -> None:
    grouped_curves = group_rows(curve_rows, ("scene", "n_pilots", "method_code"))
    grouped_mismatch = group_rows(mismatch_rows, ("method_code",))
    fig, axes = plt.subplots(1, 2, figsize=(7.25, 3.25), constrained_layout=True)
    scenes = ("weak", "moderate", "strong")
    scene_x = np.arange(len(scenes), dtype=float)
    for method in ("B2_TUNED", "C4_FWD", "B3_PSC"):
        required: list[float] = []
        for scene in scenes:
            group = grouped_curves[(scene, "2", method)]
            status, value = crossing([(f(row, "snr_db"), f(row, "ber_jeffreys")) for row in group])
            required.append(value if status == "STABLE" and value is not None else math.nan)
        plot_line(axes[0], scene_x, required, method, markevery=1)
    axes[0].set_xticks(scene_x, [SCENE_NAMES[scene] for scene in scenes])
    axes[0].set_ylim(20, 35)
    axes[0].set_ylabel("达到工程参考 BER 所需 SNR / dB")
    axes[0].set_title("(a) 不同湍流强度，$N_p=2$")
    add_grid(axes[0])
    for method in METHOD_ORDER:
        group = sorted(grouped_mismatch[(method,)], key=lambda row: f(row, "delta"))
        plot_line(
            axes[1],
            [f(row, "delta") for row in group],
            [f(row, "ber_jeffreys") for row in group],
            method,
            markevery=1,
        )
    axes[1].axhline(ENGINEERING_BER, color="#4B5563", linestyle=(0, (4, 2)), linewidth=0.9)
    axes[1].set_yscale("log")
    axes[1].set_ylim(1e-4, 2e-1)
    axes[1].set_xlabel("非酉失配强度 $\delta$")
    axes[1].set_ylabel("比特误码率（BER）")
    axes[1].set_title("(b) 中等湍流、$N_p=2$、25 dB")
    add_grid(axes[1])
    handles, labels = axes[1].get_legend_handles_labels()
    fig.legend(handles, labels, loc="outside lower center", ncol=5, frameon=False)
    fig.suptitle("结构约束方法的适用性与边界（各场景内同条件比较）", fontsize=10.2)
    save_figure(fig, "ch4-formal-robustness-boundary")


def validate_existing_figures() -> None:
    for stem in FIGURE_STEMS:
        for suffix in ("svg", "png"):
            path = FIGURE_DIR / f"{stem}.{suffix}"
            if not path.exists() or path.stat().st_size < 1000:
                raise ValueError(f"missing or empty formal figure: {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true", help="check that expected outputs exist")
    args = parser.parse_args()
    configure_style()
    if args.check_only:
        validate_existing_figures()
        print("PASS: all formal Ch4 SVG/PNG outputs exist")
        return 0
    curves = read_csv("ch4-formal-ber-curves.csv")
    required = read_csv("ch4-formal-required-snr.csv")
    pilot = read_csv("ch4-formal-pilot-sensitivity.csv")
    mechanism = read_csv("ch4-formal-mechanism.csv")
    mismatch = read_csv("ch4-formal-mismatch.csv")
    plot_ber_curves(curves)
    plot_required_snr_gain(required)
    plot_pilot_sensitivity(pilot)
    plot_mechanism(mechanism)
    plot_robustness_boundary(curves, mismatch)
    validate_existing_figures()
    print("PASS: formal Ch4 figures generated from materialized CSVs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
