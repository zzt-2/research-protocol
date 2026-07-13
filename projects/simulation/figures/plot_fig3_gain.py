# -*- coding: utf-8 -*-
"""Generate CCISP Fig. 3: BER reduction relative to fixed NDA.

The plotted metric is

    10 * log10(P_b,NDA / P_b,sw),

where both BERs are evaluated at the same average data-symbol SNR. Positive
values therefore mean that per-block switching reduces BER. This is a
dB-scaled BER ratio, not an equal-BER horizontal shift metric.

Data source (read-only):
  explore/nda-awgn-tracking-sandbox/_a4_switch_30seed_fixed.json

Outputs:
  figures/ccisp_fig3_gain.pdf (vector) and .png (300 dpi preview)
"""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, ".."))
DATA_JSON = os.path.join(
    _SIM_ROOT,
    "explore",
    "nda-awgn-tracking-sandbox",
    "_a4_switch_30seed_fixed.json",
)
OUT_PNG = os.path.join(_HERE, "ccisp_fig3_gain.png")
OUT_PDF = os.path.join(_HERE, "ccisp_fig3_gain.pdf")

METRIC_FORMULA = "10*log10(P_b,NDA/P_b,sw) at the same average data-symbol SNR"
SCENES = ("weak", "moderate", "strong")
STYLES = {
    "weak": {"label": "Weak", "color": "#0072B2", "marker": "o"},
    "moderate": {"label": "Moderate", "color": "#E69F00", "marker": "s"},
    "strong": {"label": "Strong", "color": "#D55E00", "marker": "^"},
}


def load_scan(scene):
    """Return the SNR and BER-reduction arrays for one turbulence scene."""
    with open(DATA_JSON, "r", encoding="utf-8") as handle:
        points = json.load(handle)["summary"][scene]["points"]
    snr_db = [point["snr_db"] for point in points]
    ber_reduction_db = [point["switch_vs_nda_db_mean"] for point in points]
    return snr_db, ber_reduction_db


def main():
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
            "mathtext.fontset": "stix",
            "axes.linewidth": 0.6,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )

    fig, ax = plt.subplots(figsize=(3.5, 2.65))

    for scene in SCENES:
        snr_db, reduction_db = load_scan(scene)
        style = STYLES[scene]
        ax.plot(
            snr_db,
            reduction_db,
            color=style["color"],
            marker=style["marker"],
            linewidth=1.3,
            markersize=3.6,
            markerfacecolor="white",
            markeredgewidth=0.8,
            label=style["label"],
            zorder=3,
        )

    ax.axhline(0.0, color="#777777", linewidth=0.8, zorder=1)
    ax.set_xlabel(r"Average data-symbol SNR, $\bar{\gamma}_d$ (dB)", fontsize=9)
    ax.set_ylabel("BER reduction relative to fixed NDA (dB)", fontsize=9)
    ax.set_xlim(5, 26)
    ax.set_xticks([5, 10, 15, 20, 25])
    ax.tick_params(axis="both", which="major", labelsize=8.5, width=0.6, length=3)
    ax.minorticks_off()
    ax.grid(True, which="major", color="#d0d0d0", alpha=0.55, linewidth=0.45)
    ax.legend(
        fontsize=8.5,
        loc="upper right",
        frameon=True,
        edgecolor="#b0b0b0",
        fancybox=False,
        borderpad=0.35,
        handlelength=1.8,
    )

    fig.tight_layout(pad=0.45)
    fig.savefig(OUT_PDF, bbox_inches="tight")
    fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"[metric] {METRIC_FORMULA}")
    for scene in SCENES:
        snr_db, reduction_db = load_scan(scene)
        print(f"[{scene}] points={len(snr_db)} snr_db={snr_db}")
        print(f"[{scene}] ber_reduction_db={reduction_db}")
    print(f"[saved] {OUT_PDF}")
    print(f"[saved] {OUT_PNG}")


if __name__ == "__main__":
    main()
