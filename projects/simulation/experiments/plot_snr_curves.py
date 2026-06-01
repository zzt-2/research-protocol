#!/usr/bin/env python3
"""Plot SNR vs BER curves from multi-seed sweep data.

Generates 3 subplots (weak / moderate / strong turbulence), each showing
4 method curves with 95% CI error bands on a log-scale Y axis.

Usage:
    cd /mnt/d/code/study/research-protocol
    ~/.venvs/torch/bin/python projects/simulation/experiments/plot_snr_curves.py
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
REPO_ROOT = Path("/mnt/d/code/study/research-protocol")
DATA_PATH = REPO_ROOT / "projects/simulation/results/sweep_20260601_181320.json"
DATA_PATH_BPS = REPO_ROOT / "projects/simulation/results/sweep_bps_10seed.json"
OUT_PATH = REPO_ROOT / "毕设/写作材料/figures/snr_sweep_curves.pdf"

METHODS = ["VV", "BPS", "DPLL", "KF_pilot", "Fixed"]
METHOD_LABELS = {"VV": "VV", "BPS": "BPS", "DPLL": "DPLL", "KF_pilot": "KF", "Fixed": "Fixed"}
METHOD_COLORS = {"VV": "#1f77b4", "BPS": "#9467bd", "DPLL": "#d62728", "KF_pilot": "#2ca02c", "Fixed": "#ff7f0e"}
TURBULENCE_ORDER = ["weak", "moderate", "strong"]
TURBULENCE_LABELS = {"weak": "Weak Turbulence", "moderate": "Moderate Turbulence", "strong": "Strong Turbulence"}

# BER floor for log axis (replace 0 with this)
BER_FLOOR = 1e-7


def load_data(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def extract_method_turb(key: str):
    """Split a key like 'VV_weak' into (method, turbulence)."""
    # Handle KF_pilot which contains an underscore
    for method in METHODS:
        if key.startswith(method + "_"):
            turbulence = key[len(method) + 1:]
            return method, turbulence
    return None, None


def plot_snr_curves(data: dict, bps_data: dict = None):
    results = dict(data["results"])
    if bps_data:
        results.update(bps_data["results"])

    fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

    for ax, turb in zip(axes, TURBULENCE_ORDER):
        for method in METHODS:
            key = f"{method}_{turb}"
            if key not in results:
                print(f"  [warn] missing key: {key}")
                continue

            snr_points = results[key]["snr_points"]
            snr_db = np.array([p["snr_db"] for p in snr_points])
            ber_mean = np.array([p["ber_mean"] for p in snr_points])
            ci_lo = np.array([p["ci_95"][0] for p in snr_points])
            ci_hi = np.array([p["ci_95"][1] for p in snr_points])

            # Floor zero values for log scale
            ber_mean = np.maximum(ber_mean, BER_FLOOR)
            ci_lo = np.maximum(ci_lo, BER_FLOOR)
            ci_hi = np.maximum(ci_hi, BER_FLOOR)

            color = METHOD_COLORS[method]
            label = METHOD_LABELS[method]

            ax.plot(snr_db, ber_mean, color=color, label=label, linewidth=1.8)
            ax.fill_between(snr_db, ci_lo, ci_hi, color=color, alpha=0.15)

        ax.set_yscale("log")
        ax.set_xlabel("SNR (dB)")
        ax.set_title(TURBULENCE_LABELS[turb])
        ax.grid(True, which="both", alpha=0.3, linestyle="--")
        ax.set_xlim(snr_db[0], snr_db[-1])
        ax.set_ylim(BER_FLOOR, 0.6)

    axes[0].set_ylabel("BER")
    axes[0].legend(loc="upper right", fontsize=9)

    fig.tight_layout()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PATH, dpi=300, bbox_inches="tight")
    print(f"Saved: {OUT_PATH}")
    plt.close(fig)


def main():
    print(f"Loading: {DATA_PATH}")
    data = load_data(DATA_PATH)
    print(f"  metadata: {data['metadata']['n_seeds']} seeds, "
          f"{data['metadata']['n_symbols']} symbols, "
          f"methods={data['metadata']['methods']}")
    bps_data = None
    if DATA_PATH_BPS.exists():
        print(f"Loading BPS: {DATA_PATH_BPS}")
        bps_data = load_data(DATA_PATH_BPS)
    plot_snr_curves(data, bps_data)


if __name__ == "__main__":
    main()
