"""Derive the T071 Ch4 confirmation table and figures from raw evidence only.

This script deliberately does not read confirmation_aggregate.json or development
artifacts.  It reproduces the frozen pooled-BER and paired-window bootstrap
statistics from confirmation_raw.json and checks the D052/V027 anchors.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
RAW = REPO / "projects/simulation/explore/ch4-scaled-unitary-pilot-ls/confirmation_raw.json"
CSV_PATH = HERE / "data/ch4-confirmation-summary.csv"
FIGURE_DIR = HERE / "figures"
ARMS = ("B0", "B1", "B2", "C4", "O1")
BOOTSTRAP_SEED = 2026083004
BOOTSTRAP_RESAMPLES = 2000

V027 = {
    "snr14_np2": (-0.00609922, -0.00954738, -0.00306168, 0.0737),
    "snr14_np4": (-0.00188351, -0.00354064, -0.00019817, 0.0262),
    "snr18_np2": (-0.00324726, -0.00548053, -0.00143516, 0.0838),
    "snr18_np4": (-0.00112247, -0.00216106, -0.00026414, 0.0506),
}
V027_POOLED = (0.06076145, 0.05608821, -0.00467324, -0.00686385, -0.00282661, 0.0769)


def paired_bootstrap(candidate: np.ndarray, baseline: np.ndarray) -> tuple[float, float, float]:
    difference = np.asarray(candidate, dtype=np.float64) - np.asarray(baseline, dtype=np.float64)
    rng = np.random.Generator(np.random.PCG64(BOOTSTRAP_SEED))
    indices = rng.integers(
        0, difference.size, size=(BOOTSTRAP_RESAMPLES, difference.size), dtype=np.int64
    )
    lower, upper = np.quantile(difference[indices].mean(axis=1), [0.025, 0.975])
    return float(difference.mean()), float(lower), float(upper)


def derive_rows(raw_path: Path = RAW) -> list[dict[str, object]]:
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    if raw.get("schema_version") != "t071.scaled-unitary-confirmation-raw.v1":
        raise ValueError("unexpected confirmation raw schema")
    rows: list[dict[str, object]] = []
    pooled = {arm: [] for arm in ARMS}
    seen_seeds: set[int] = set()
    for cell in raw["cells"]:
        windows = cell["windows"]
        if len(windows) != 64:
            raise ValueError(f"{cell['cell_id']} does not contain 64 windows")
        per_arm = {arm: [] for arm in ARMS}
        counts = {arm: [0, 0] for arm in ARMS}
        for window in windows:
            seed = int(window["seed"])
            if seed in seen_seeds or window["split"] != "confirmation":
                raise ValueError("duplicate seed or non-confirmation row")
            seen_seeds.add(seed)
            observed = tuple(row["arm"] for row in window["rows"])
            if observed != ARMS:
                raise ValueError(f"arm order/coverage mismatch: {observed}")
            for item in window["rows"]:
                arm = item["arm"]
                errors, bits = int(item["bit_errors"]), int(item["payload_bits"])
                if bits != 32768 or float(item["ber"]) != errors / bits:
                    raise ValueError("raw BER numerator/denominator mismatch")
                counts[arm][0] += errors
                counts[arm][1] += bits
                per_arm[arm].append(float(item["ber"]))
        ber = {arm: counts[arm][0] / counts[arm][1] for arm in ARMS}
        mean, lower, upper = paired_bootstrap(
            np.asarray(per_arm["C4"]), np.asarray(per_arm["B2"])
        )
        relative = (ber["B2"] - ber["C4"]) / ber["B2"]
        rows.append(
            {
                "row_type": "cell",
                "cell_id": cell["cell_id"],
                "snr_db": int(cell["snr_db"]),
                "pilot_symbols_per_polarization": int(cell["pilot_symbols_per_polarization"]),
                "confirmation_windows": len(windows),
                **{f"{arm}_ber": ber[arm] for arm in ARMS},
                "C4_minus_B2_mean": mean,
                "ci95_lower": lower,
                "ci95_upper": upper,
                "relative_reduction_vs_B2": relative,
            }
        )
        if int(cell["pilot_symbols_per_polarization"]) == 2:
            for arm in ARMS:
                pooled[arm].extend(per_arm[arm])
    if len(seen_seeds) != 256:
        raise ValueError("confirmation must contain 256 unique seeds")
    pooled_ber = {arm: float(np.mean(pooled[arm])) for arm in ARMS}
    mean, lower, upper = paired_bootstrap(np.asarray(pooled["C4"]), np.asarray(pooled["B2"]))
    rows.append(
        {
            "row_type": "pooled_np2",
            "cell_id": "pooled_np2",
            "snr_db": "14+18",
            "pilot_symbols_per_polarization": 2,
            "confirmation_windows": 128,
            **{f"{arm}_ber": pooled_ber[arm] for arm in ARMS},
            "C4_minus_B2_mean": mean,
            "ci95_lower": lower,
            "ci95_upper": upper,
            "relative_reduction_vs_B2": (pooled_ber["B2"] - pooled_ber["C4"])
            / pooled_ber["B2"],
        }
    )
    return rows


def verify_v027(rows: list[dict[str, object]]) -> None:
    for row in rows[:4]:
        expected = V027[str(row["cell_id"])]
        actual = (
            float(row["C4_minus_B2_mean"]),
            float(row["ci95_lower"]),
            float(row["ci95_upper"]),
        )
        if not np.allclose(actual, expected[:3], atol=5e-9, rtol=0.0):
            raise AssertionError(f"{row['cell_id']} differs from V027: {actual} vs {expected[:3]}")
        if round(float(row["relative_reduction_vs_B2"]), 4) != expected[3]:
            raise AssertionError(f"{row['cell_id']} relative reduction differs from D052/V027")
    pooled = rows[4]
    actual = (
        float(pooled["B2_ber"]),
        float(pooled["C4_ber"]),
        float(pooled["C4_minus_B2_mean"]),
        float(pooled["ci95_lower"]),
        float(pooled["ci95_upper"]),
        float(pooled["relative_reduction_vs_B2"]),
    )
    if not np.allclose(actual[:5], V027_POOLED[:5], atol=5e-9, rtol=0.0):
        raise AssertionError(f"pooled Np=2 differs from V027: {actual}")
    if round(actual[5], 4) != V027_POOLED[5]:
        raise AssertionError("pooled Np=2 relative reduction differs from D052/V027")


def write_csv(rows: list[dict[str, object]], path: Path = CSV_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            rendered = {
                key: f"{value:.10f}" if isinstance(value, float) else value
                for key, value in row.items()
            }
            writer.writerow(rendered)


def plot(rows: list[dict[str, object]]) -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
            "svg.fonttype": "none",
            "axes.unicode_minus": False,
            "font.size": 9.0,
        }
    )
    cells = rows[:4]
    labels = [f"{r['snr_db']} dB\n$N_p$={r['pilot_symbols_per_polarization']}" for r in cells]
    x = np.arange(len(cells), dtype=float)
    width = 0.18
    styles = {
        "B0": ("#9AA0A6", "//", "普通 LS (B0)"),
        "B2": ("#2B6F98", "", "$\\tau=1$ SV-floor (B2)"),
        "C4": ("#D97732", "xx", "缩放酉投影 (C4)"),
        "O1": ("#4F8A6B", "..", "真实信道逆 (O1, oracle)"),
    }
    fig, ax = plt.subplots(figsize=(8.8, 4.4), constrained_layout=True)
    for offset, arm in zip((-1.5, -0.5, 0.5, 1.5), styles):
        color, hatch, label = styles[arm]
        ax.bar(
            x + offset * width,
            [float(row[f"{arm}_ber"]) for row in cells],
            width,
            color=color,
            edgecolor="#263746",
            linewidth=0.7,
            hatch=hatch,
            label=label,
            zorder=3,
        )
    for index, row in enumerate(cells):
        top = max(float(row[f"{arm}_ber"]) for arm in styles)
        relative = 100.0 * float(row["relative_reduction_vs_B2"])
        ax.text(index, top + 0.0032, f"C4 vs B2: −{relative:.2f}%", ha="center", va="bottom", fontsize=8)
    ax.set_ylabel("Payload BER（64 个 paired windows 合并）")
    ax.set_xticks(x, labels)
    ax.set_ylim(0.0, 0.10)
    ax.grid(axis="y", color="#D8DEE4", linewidth=0.7, zorder=0)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(ncol=2, loc="upper right", frameon=False)
    ax.text(
        0.01,
        0.98,
        "Confirmation：所有四格均展示；纵轴从 0 起",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=8,
        color="#4A5560",
    )
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURE_DIR / "ch4-ber-comparison.svg")
    fig.savefig(FIGURE_DIR / "ch4-ber-comparison.png", dpi=200)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    rows = derive_rows()
    verify_v027(rows)
    if not args.check_only:
        write_csv(rows)
        plot(rows)
    print("PASS: raw-only CSV/figure derivation matches D052/V027")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
