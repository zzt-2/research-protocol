"""PROMPT-016 trend plots from param sweep results.

画三张趋势图 (PI-BER vs 维度):
1. PI-BER vs f_G (CMA/ML/oracle 三线)
2. PI-BER vs SNR
3. QPSK vs 16QAM 对比

鲁棒性展示 (非 Go/No-Go 判据), N=2M, 5 seeds, error bar = 样本 SD.

用法:
  cd projects/simulation
  python explore/cma-fade-divergence/prompt016_plot_trends.py
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SIM_DIR = Path(__file__).resolve().parents[2]
RESULT_PATH = SIM_DIR / "results" / "cma-fade-divergence" / "prompt016_param_sweep.json"
OUT_DIR = SIM_DIR / "results" / "cma-fade-divergence" / "prompt016_figures"


def load():
    return json.loads(RESULT_PATH.read_text(encoding="utf-8"))


def by_id(summaries, cell_id):
    for s in summaries:
        if s["cell_id"] == cell_id:
            return s
    raise KeyError(cell_id)


def plot_fg_sweep(d):
    """Fig 1: PI-BER vs f_G (QPSK, 20dB)."""
    summaries = d["summaries"]
    fgs = [30.0, 100.0, 1000.0]
    cids = [f"fg{int(f)}_qpsk_snr20" for f in fgs]
    methods = ("standard-CMA", "ML-original", "oracle")
    colors = {"standard-CMA": "#1f77b4", "ML-original": "#d62728", "oracle": "#2ca02c"}
    markers = {"standard-CMA": "s", "ML-original": "o", "oracle": "^"}

    fig, ax = plt.subplots(figsize=(6, 4.2))
    for m in methods:
        means, stds = [], []
        for cid in cids:
            s = by_id(summaries, cid)
            means.append(s[m]["pi_ber_mean"])
            stds.append(s[m]["pi_ber_std"])
        ax.errorbar(fgs, means, yerr=stds, label=m, color=colors[m],
                    marker=markers[m], capsize=4, linewidth=1.6)
    ax.set_xscale("log")
    ax.set_xlabel(r"$f_G$ (Hz)")
    ax.set_ylabel("PI-BER (test-late)")
    ax.set_title("PI-BER vs Greenwood frequency $f_G$\n(QPSK, 20 dB, strong turb., N=2M, 5 seeds)")
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    out = OUT_DIR / "fig1_pi_ber_vs_fg.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def plot_snr_sweep(d):
    """Fig 2: PI-BER vs SNR (QPSK, f_G=30)."""
    summaries = d["summaries"]
    snrs = [20.0, 15.0, 10.0]
    cids = [f"fg30_qpsk_snr{int(s)}" for s in snrs]
    methods = ("standard-CMA", "ML-original", "oracle")
    colors = {"standard-CMA": "#1f77b4", "ML-original": "#d62728", "oracle": "#2ca02c"}
    markers = {"standard-CMA": "s", "ML-original": "o", "oracle": "^"}

    fig, ax = plt.subplots(figsize=(6, 4.2))
    for m in methods:
        means, stds = [], []
        for cid in cids:
            s = by_id(summaries, cid)
            means.append(s[m]["pi_ber_mean"])
            stds.append(s[m]["pi_ber_std"])
        ax.errorbar(snrs, means, yerr=stds, label=m, color=colors[m],
                    marker=markers[m], capsize=4, linewidth=1.6)
    ax.invert_xaxis()  # 高SNR在左 (常规)
    ax.set_xlabel("SNR (dB)")
    ax.set_ylabel("PI-BER (test-late)")
    ax.set_title("PI-BER vs SNR\n(QPSK, $f_G$=30 Hz, strong turb., N=2M, 5 seeds)")
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out = OUT_DIR / "fig2_pi_ber_vs_snr.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def plot_modulation(d):
    """Fig 3: QPSK vs 16QAM (f_G=30, 20dB)."""
    summaries = d["summaries"]
    qpsk = by_id(summaries, "fg30_qpsk_snr20")
    qam = by_id(summaries, "fg30_16qam_snr20")
    methods = ("standard-CMA", "ML-original", "oracle")
    colors = {"standard-CMA": "#1f77b4", "ML-original": "#d62728", "oracle": "#2ca02c"}

    fig, ax = plt.subplots(figsize=(6, 4.2))
    x = np.arange(len(methods))
    width = 0.35
    qpsk_means = [qpsk[m]["pi_ber_mean"] for m in methods]
    qpsk_stds = [qpsk[m]["pi_ber_std"] for m in methods]
    qam_means = [qam[m]["pi_ber_mean"] for m in methods]
    qam_stds = [qam[m]["pi_ber_std"] for m in methods]
    ax.bar(x - width/2, qpsk_means, width, yerr=qpsk_stds, label="QPSK",
           color="#4c72b0", capsize=4)
    ax.bar(x + width/2, qam_means, width, yerr=qam_stds, label="16QAM",
           color="#dd8452", capsize=4)
    ax.set_xticks(x)
    ax.set_xticklabels(methods)
    ax.set_ylabel("PI-BER (test-late)")
    ax.set_title("QPSK vs 16QAM\n($f_G$=30 Hz, 20 dB, strong turb., N=2M, 5 seeds)")
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    out = OUT_DIR / "fig3_qpsk_vs_16qam.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    d = load()
    print(f"loaded {len(d.get('summaries', []))} cell summaries")
    f1 = plot_fg_sweep(d)
    f2 = plot_snr_sweep(d)
    f3 = plot_modulation(d)
    print(f"figures:\n  {f1}\n  {f2}\n  {f3}")


if __name__ == "__main__":
    main()
