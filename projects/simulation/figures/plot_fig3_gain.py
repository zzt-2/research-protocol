# -*- coding: utf-8 -*-
"""Generate CCISP Fig. 5: common-data-payload BER reduction of the
received-power-aware selector relative to fixed NDA.

The plotted metric is the common-768 BER reduction

    G_C = 10 * log10(R_C,NDA / R_C,SW),

where R_C,NDA and R_C,SW are the BERs of fixed NDA and of the selector
output, both evaluated on the same frozen 768-bit common data payload
(the 192 non-pilot symbols per processing window). Both branches share
one bit population, so a positive value is a fair, same-population BER
reduction at the common average data-symbol SNR.

Data source (read-only): the formal A/B verifier report, whose 33 points are
recomputed from paired 30-seed route-A raw records.

Outputs:
  figures/ccisp_fig3_gain.pdf (vector) and .png (300 dpi preview)
"""
import json
import math
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, ".."))
DATA_JSON = os.path.join(
    _SIM_ROOT, "results", "ccisp_family1_formal_verification.json",
)
OUT_PNG = os.path.join(_HERE, "ccisp_fig3_gain.png")
OUT_PDF = os.path.join(_HERE, "ccisp_fig3_gain.pdf")

# Compact conference-column footprint; width and typography remain unchanged.
FIGSIZE_IN = (3.5, 2.85)
FONT_SIZES = {
    "title": 10.0,
    "label": 10.0,
    "tick": 9.0,
    "legend": 9.0,
    "annotation": 9.0,
}
MPL_RCPARAMS = {
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "Nimbus Roman No9 L", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "text.usetex": False,
    "font.weight": "normal",
    "axes.labelweight": "normal",
    "axes.linewidth": 0.6,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
}

METRIC_FORMULA = (
    "10*log10(R_C,NDA/R_C,SW) on the common 768-bit data payload, "
    "at the same average data-symbol SNR"
)
SCENES = ("weak", "moderate", "strong")
EXPECTED_SNR_DB = {float(value) for value in range(5, 26, 2)}
X_MAJOR_TICKS = [5, 9, 13, 17, 21, 25]
EXPECTED_N_SEEDS = 30
STYLES = {
    "weak": {"label": "Weak", "color": "#0072B2", "marker": "o"},
    "moderate": {"label": "Moderate", "color": "#E69F00", "marker": "s"},
    "strong": {"label": "Strong", "color": "#D55E00", "marker": "^"},
}


def load_figure_data(path=DATA_JSON):
    """Load and validate all 33 paired-seed means and their 95% t-CIs."""
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if payload.get("status") != "PASS" or payload.get("a_b_exact_cells") != 990:
        raise ValueError("formal verification PASS/990 required")
    authority_path = os.path.join(_SIM_ROOT, "results", "ccisp_family1_selector_a_30seed.json")
    with open(authority_path, "r", encoding="utf-8") as handle:
        authority = json.load(handle)["authority"]
    hashes = authority.get("imported_file_sha256", {})
    if authority.get("authority_status") != "formal" or authority.get("route") != "A": raise ValueError("route-A formal authority required")
    if authority.get("params_sha256") != hashes.get("params.py"): raise ValueError("params hash mismatch")
    grid = authority["grid"]
    if grid["scenes"] != list(SCENES) or set(grid["snr_db"]) != EXPECTED_SNR_DB or grid["n_seeds"] != 30 or grid["windows_per_seed"] != 400: raise ValueError("formal grid mismatch")
    summary = {scene: [] for scene in SCENES}
    for point in payload["paired_statistics"]: summary[point["scene"]].append(point)

    figure_data = {}
    for scene in SCENES:
        points = summary[scene]
        if len(points) != len(EXPECTED_SNR_DB):
            raise ValueError(
                f"{scene}: expected {len(EXPECTED_SNR_DB)} points, "
                f"got {len(points)}"
            )

        rows = []
        for point in points:
            snr_db = float(point["snr_db"])
            paper = point
            if paper["n_seed_units"] != EXPECTED_N_SEEDS:
                raise ValueError(
                    f"{scene}@{snr_db:g}: expected n_seeds={EXPECTED_N_SEEDS}, "
                    f"got {paper['n_seed_units']}"
                )

            mean = float(paper["mean_gain_db"])
            low = float(paper["ci95_low_db"])
            high = float(paper["ci95_high_db"])
            if not all(math.isfinite(value) for value in (mean, low, high)):
                raise ValueError(f"{scene}@{snr_db:g}: non-finite mean or CI")
            if not low <= mean <= high:
                raise ValueError(
                    f"{scene}@{snr_db:g}: CI does not contain mean "
                    f"({low}, {mean}, {high})"
                )
            rows.append((snr_db, mean, low, high))

        snr_set = {row[0] for row in rows}
        if snr_set != EXPECTED_SNR_DB:
            raise ValueError(
                f"{scene}: expected SNRs {sorted(EXPECTED_SNR_DB)}, "
                f"got {sorted(snr_set)}"
            )

        rows.sort(key=lambda row: row[0])
        figure_data[scene] = {
            "snr_db": [row[0] for row in rows],
            "mean_gain_db": [row[1] for row in rows],
            "ci95_low_db": [row[2] for row in rows],
            "ci95_high_db": [row[3] for row in rows],
        }

    return figure_data


def main():
    plt.rcParams.update(MPL_RCPARAMS)

    fig, ax = plt.subplots(figsize=FIGSIZE_IN)
    figure_data = load_figure_data()

    for scene in SCENES:
        data = figure_data[scene]
        snr_db = data["snr_db"]
        reduction_db = data["mean_gain_db"]
        yerr = [
            [mean - low for mean, low in zip(reduction_db, data["ci95_low_db"])],
            [high - mean for mean, high in zip(reduction_db, data["ci95_high_db"])],
        ]
        style = STYLES[scene]
        ax.errorbar(
            snr_db,
            reduction_db,
            yerr=yerr,
            color=style["color"],
            marker=style["marker"],
            linewidth=1.3,
            markersize=3.6,
            markerfacecolor="white",
            markeredgewidth=0.8,
            elinewidth=0.8,
            capsize=2.5,
            capthick=0.8,
            label=style["label"],
            zorder=3,
        )

    ax.axhline(
        0.0, color="#777777", linestyle="--", linewidth=0.8, zorder=1
    )
    ax.set_xlabel(
        r"Data-symbol $E_s/N_0$ [dB]", fontsize=FONT_SIZES["label"]
    )
    ax.set_ylabel(
        "Common-payload BER-ratio\nreduction, $G_{\\mathcal{C}}$ [dB]",
        fontsize=FONT_SIZES["label"],
    )
    ax.set_xlim(4.5, 25.5)
    ax.set_xticks(X_MAJOR_TICKS)
    ci_values = [
        value
        for scene in SCENES
        for key in ("ci95_low_db", "ci95_high_db")
        for value in figure_data[scene][key]
    ]
    data_low = min(0.0, min(ci_values))
    data_high = max(0.0, max(ci_values))
    span = data_high - data_low
    margin = max(0.04, 0.08 * span)
    ax.set_ylim(data_low - margin, data_high + margin)
    ax.tick_params(
        axis="both", which="major", labelsize=FONT_SIZES["tick"], width=0.6, length=3
    )
    ax.minorticks_off()
    ax.grid(True, which="major", color="#d0d0d0", alpha=0.55, linewidth=0.45)
    ax.legend(
        fontsize=FONT_SIZES["legend"],
        loc="upper right",
        ncol=1,
        frameon=True,
        framealpha=0.78,
        facecolor="white",
        edgecolor="#b0b0b0",
        borderpad=0.3,
        handlelength=1.5,
        labelspacing=0.25,
    )

    fig.subplots_adjust(left=0.22, right=0.97, top=0.97, bottom=0.20)
    fig.savefig(OUT_PDF)
    fig.savefig(OUT_PNG, dpi=300)
    plt.close(fig)

    print(f"[metric] {METRIC_FORMULA}")
    for scene in SCENES:
        data = figure_data[scene]
        print(f"[{scene}] points={len(data['snr_db'])}")
        for snr_db, mean, low, high in zip(
            data["snr_db"],
            data["mean_gain_db"],
            data["ci95_low_db"],
            data["ci95_high_db"],
        ):
            print(
                f"  snr_db={snr_db:g} mean_gain_db={mean:.15g} "
                f"ci95=[{low:.15g}, {high:.15g}]"
            )
    print(f"[saved] {OUT_PDF}")
    print(f"[saved] {OUT_PNG}")


if __name__ == "__main__":
    main()
