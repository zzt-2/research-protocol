"""Deterministic recompute + plot of G1 stratified results.

Reads ONLY raw-rows.csv (no re-running of any simulation, no hand-copied points).
Statistics unit = seed-cluster: within one seed, average the paired
delta-PI-SER across the cells that belong to the same offline stratum, taking
ONE value per seed; 10k bootstrap 95% CI on the seed-level values.

PI-SER = permutation-invariant symbol error rate (defined in the thesis insert).
delta = method_pi_ser - baseline_pi_ser (baseline = tuned fixed-mu CMA identity).
Negative delta = improvement (lower error rate).

Usage:
    python plot_g1_stratified_results.py --verify    # assert frozen anchors
    python plot_g1_stratified_results.py             # render SVG + PNG + CSV
"""

from __future__ import annotations

import argparse
import csv
import os
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACTS = os.path.normpath(
    os.path.join(
        HERE,
        "..", "..", "scout", "g1-safe-gated-normalization-confirm", "artifacts",
    )
)
RAW = os.path.join(ARTIFACTS, "raw-rows.csv")

METHOD = "gated_scalar"
BASELINE = "baseline_cma_mu0p03"
ALWAYS_ON = "robust_scalar"          # frozen primary always-on comparator
COLLAPSE_LABEL = "inner_ring_recoverable_collapse"
HEALTHY_LABEL = "healthy"
MDE = 0.005
N_BOOT = 10000
RNG_SEED = 42                         # matches the authoritative result.json CI

# Frozen anchors (from V060 / result.json; the script must reproduce these).
ANCHORS = {
    "collapse_mean": -0.5597956730769231,
    "collapse_ci": [-0.6947115384615384, -0.40639648437500003],
    "collapse_help": 12,
    "collapse_hurt": 0,
    "healthy_g1_worst_degradation": 0.0,
    "healthy_g1_cluster_mean": -0.002840909090909091,
}


def load_rows(path: str):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def stratum_cells(rows, method, label):
    """Cells (for this method) whose offline_4category == label."""
    return {
        r["cell"]
        for r in rows
        if r["method"] == method and r["offline_4category"] == label
    }


def paired_delta(rows, method, baseline, label):
    """For each (cell,seed) in stratum `label`, delta = method - baseline.

    Returns dict[(cell, seed)] -> float.
    """
    base = {(r["cell"], r["seed"]): r["baseline_pi_ser"] for r in rows}
    out = {}
    for r in rows:
        if r["method"] != method or r["offline_4category"] != label:
            continue
        key = (r["cell"], r["seed"])
        out[key] = float(r["pi_ser"]) - float(base[key])
    return out


def seed_cluster_values(deltas):
    """Group by seed; equal-weight mean across cells within the seed."""
    by_seed = defaultdict(list)
    for (cell, seed), d in deltas.items():
        by_seed[seed].append(d)
    return {seed: float(np.mean(v)) for seed, v in by_seed.items()}


def bootstrap_ci(seed_vals, n_boot=N_BOOT, rng_seed=RNG_SEED):
    """Mean of seed values; 10k bootstrap 95% CI on the mean.

    Values are ordered by sorted seed id (string order, matching result.json),
    and the full (n_boot, n) index matrix is drawn in one batch; this
    reproduces the authoritative result.json CI (RNG_SEED=42).
    """
    arr = np.array([seed_vals[s] for s in sorted(seed_vals.keys())], dtype=float)
    n = arr.size
    mean = float(np.mean(arr))
    rng = np.random.default_rng(rng_seed)
    idx = rng.integers(0, n, size=(n_boot, n))
    boots = arr[idx].mean(axis=1)
    lo, hi = np.quantile(boots, [0.025, 0.975])
    return mean, float(lo), float(hi), arr


def help_hurt(seed_vals, mde=MDE):
    help_ = sum(1 for v in seed_vals.values() if v < -mde)
    hurt = sum(1 for v in seed_vals.values() if v > mde)
    return help_, hurt


def verify(rows):
    """Recompute frozen anchors; return (ok, report)."""
    d_coll = paired_delta(rows, METHOD, BASELINE, COLLAPSE_LABEL)
    sv_coll = seed_cluster_values(d_coll)
    mean, lo, hi, _ = bootstrap_ci(sv_coll)
    hpc, hrt = help_hurt(sv_coll)

    d_healthy = paired_delta(rows, METHOD, BASELINE, HEALTHY_LABEL)
    sv_healthy = seed_cluster_values(d_healthy)
    # healthy per-pair worst degradation over ALL healthy pairs (not just seeds)
    healthy_pair_worst = max(max(v for v in d_healthy.values()), 0.0)
    h_mean, _, _, _ = bootstrap_ci(sv_healthy)

    checks = []
    checks.append(("collapse_mean", abs(mean - ANCHORS["collapse_mean"]) < 1e-6, mean))
    checks.append((
        "collapse_ci_lo", abs(lo - ANCHORS["collapse_ci"][0]) < 5e-4, lo,
    ))
    checks.append((
        "collapse_ci_hi", abs(hi - ANCHORS["collapse_ci"][1]) < 5e-4, hi,
    ))
    checks.append(("collapse_help", hpc == ANCHORS["collapse_help"], hpc))
    checks.append(("collapse_hurt", hrt == ANCHORS["collapse_hurt"], hrt))
    checks.append((
        "healthy_g1_worst",
        abs(healthy_pair_worst - ANCHORS["healthy_g1_worst_degradation"]) < 1e-6,
        healthy_pair_worst,
    ))
    checks.append((
        "healthy_g1_cluster_mean",
        abs(h_mean - ANCHORS["healthy_g1_cluster_mean"]) < 1e-6,
        h_mean,
    ))
    ok = all(c[1] for c in checks)
    report = "\n".join(
        f"  [{'PASS' if c[1] else 'FAIL'}] {c[0]:24s} "
        f"computed={c[2]: .10f}  anchor={ANCHORS.get(c[0], ANCHORS.get('collapse_ci'))}"
        for c in checks
    )
    return ok, report, {
        "collapse": {"deltas": d_coll, "seed_vals": sv_coll,
                     "mean": mean, "ci": [lo, hi], "help": hpc, "hurt": hrt},
        "healthy": {"deltas": d_healthy, "seed_vals": sv_healthy,
                    "pair_worst": healthy_pair_worst, "cluster_mean": h_mean},
    }


def render(rows, data):
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.titleweight": "bold",
        "axes.labelsize": 9,
        "svg.fonttype": "none",   # keep text editable in SVG
    })

    fig, (axA, axB) = plt.subplots(1, 2, figsize=(10.0, 4.2),
                                   gridspec_kw={"width_ratios": [1.0, 1.0]})

    # ---- Panel (a): collapse stratum, per-seed delta + mean/CI ----
    coll = data["collapse"]
    sv = coll["seed_vals"]
    seeds_sorted = sorted(sv.keys(), key=int)
    vals = np.array([sv[s] for s in seeds_sorted], dtype=float)
    x = np.arange(len(seeds_sorted))
    axA.axhline(0, color="#666666", linewidth=0.8, zorder=1)
    axA.axhline(-MDE, color="#bbbbbb", linewidth=0.7, linestyle="--", zorder=1)
    # color: improvement (negative) vs MDE-band (tie)
    colors = ["#2c7fb8" if v < -MDE else "#999999" for v in vals]
    axA.scatter(x, vals, c=colors, s=26, zorder=3, edgecolors="white", linewidth=0.4)
    mean, lo, hi = coll["mean"], coll["ci"][0], coll["ci"][1]
    axA.errorbar([len(seeds_sorted) + 0.6], [mean],
                 yerr=[[mean - lo], [hi - mean]], fmt="D", color="#d95f0e",
                 markersize=6, capsize=4, linewidth=1.4, zorder=4,
                 label="cluster mean + 95% CI")
    axA.set_xticks(x)
    axA.set_xticklabels(seeds_sorted, fontsize=6.5, rotation=90)
    axA.set_xlim(-0.7, len(seeds_sorted) + 1.8)
    axA.set_xlabel("seed (cluster unit)")
    axA.set_ylabel(r"$\Delta$PI-SER vs tuned CMA  (negative = improvement)")
    axA.set_title("(a) Collapse stratum")
    axA.legend(loc="lower left", fontsize=7.5, framealpha=0.9)
    txt = (f"mean = {mean:+.4f}\n95% CI [{lo:+.4f}, {hi:+.4f}]\n"
           f"help / hurt = {coll['help']} / {coll['hurt']}  (MDE = {MDE})")
    axA.text(0.98, 0.97, txt, transform=axA.transAxes, ha="right", va="top",
             fontsize=7.2, bbox=dict(boxstyle="round,pad=0.3",
             facecolor="white", edgecolor="#cccccc", alpha=0.9))

    # ---- Panel (b): healthy stratum, per-pair degradation distribution ----
    # Compare gated_scalar vs always-on primary comparator (robust_scalar).
    g1_healthy = data["healthy"]["deltas"]            # method=gated_scalar
    ao_deltas = paired_delta(rows, ALWAYS_ON, BASELINE, HEALTHY_LABEL)
    g1_arr = np.array(sorted(g1_healthy.values()), dtype=float)
    ao_arr = np.array(sorted(ao_deltas.values()), dtype=float)
    axB.axhline(0, color="#666666", linewidth=0.8, zorder=1)
    axB.axhline(MDE, color="#d95f0e", linewidth=0.9, linestyle="--", zorder=2,
                label=f"MDE = {MDE} (safety threshold)")
    n = max(g1_arr.size, ao_arr.size)
    xx = np.arange(n)
    # gated_scalar: degradation distribution (positive = degradation)
    g1_pad = np.pad(g1_arr, (0, n - g1_arr.size), constant_values=np.nan)
    ao_pad = np.pad(ao_arr, (0, n - ao_arr.size), constant_values=np.nan)
    axB.scatter(xx, g1_pad, marker="o", s=20, color="#2c7fb8",
                edgecolors="white", linewidth=0.3, zorder=4,
                label="proposed gated layer")
    axB.scatter(xx, ao_pad, marker="x", s=26, color="#e7298a",
                linewidths=1.1, zorder=3,
                label="always-on normalization (robust_scalar)")
    worst_g1 = data["healthy"]["pair_worst"]
    axB.set_xlabel("healthy pair index (distribution viz only)")
    axB.set_ylabel(r"per-pair $\Delta$PI-SER  (positive = degradation)")
    axB.set_title("(b) Healthy stratum")
    axB.set_xlim(-0.7, n + 0.5)
    axB.legend(loc="upper left", fontsize=7.5, framealpha=0.9)
    hmean = data["healthy"]["cluster_mean"]
    txt2 = (f"proposed worst-pair degradation = {worst_g1:.4f}\n"
            f"proposed cluster mean = {hmean:+.4f}\n"
            f"pairs shown for distribution only (not stat. units)")
    axB.text(0.98, 0.05, txt2, transform=axB.transAxes, ha="right", va="bottom",
             fontsize=7.2, bbox=dict(boxstyle="round,pad=0.3",
             facecolor="white", edgecolor="#cccccc", alpha=0.9))

    fig.suptitle(
        "Stratified results on a local slice "
        "(collapse / healthy are offline-labeled condition subsets; "
        "CI = seed-cluster bootstrap 95%)",
        fontsize=8.5, y=0.995,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.96])

    svg = os.path.join(HERE, "g1-stratified-results.svg")
    png = os.path.join(HERE, "g1-stratified-results.png")
    fig.savefig(svg, format="svg")
    fig.savefig(png, format="png", dpi=200)
    plt.close(fig)
    return svg, png


def write_csv(rows, data):
    path = os.path.join(HERE, "g1-stratified-results.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["stratum", "seed", "cell", "method", "delta_pi_ser"])
        for stratum, key in [("collapse", "collapse"), ("healthy", "healthy")]:
            for (cell, seed), d in sorted(data[key]["deltas"].items(),
                                          key=lambda kv: (int(kv[0][1]), kv[0][0])):
                w.writerow([stratum, seed, cell, METHOD, f"{d:.10f}"])
        # always-on healthy deltas for panel (b) comparison
        ao = paired_delta(rows, ALWAYS_ON, BASELINE, HEALTHY_LABEL)
        for (cell, seed), d in sorted(ao.items(),
                                      key=lambda kv: (int(kv[0][1]), kv[0][0])):
            w.writerow(["healthy", seed, cell, ALWAYS_ON, f"{d:.10f}"])
        # summary rows
        w.writerow([])
        coll = data["collapse"]
        h = data["healthy"]
        w.writerow(["# summary", "method", "stratum", "stat", "value"])
        w.writerow(["# summary", METHOD, "collapse", "cluster_mean",
                    f"{coll['mean']:.10f}"])
        w.writerow(["# summary", METHOD, "collapse", "ci_lo",
                    f"{coll['ci'][0]:.10f}"])
        w.writerow(["# summary", METHOD, "collapse", "ci_hi",
                    f"{coll['ci'][1]:.10f}"])
        w.writerow(["# summary", METHOD, "collapse", "help", coll["help"]])
        w.writerow(["# summary", METHOD, "collapse", "hurt", coll["hurt"]])
        w.writerow(["# summary", METHOD, "healthy", "pair_worst",
                    f"{h['pair_worst']:.10f}"])
        w.writerow(["# summary", METHOD, "healthy", "cluster_mean",
                    f"{h['cluster_mean']:.10f}"])
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()

    rows = load_rows(RAW)
    ok, report, data = verify(rows)
    print("raw rows:", len(rows),
          "| collapse pairs:", len(data["collapse"]["deltas"]),
          "| healthy pairs:", len(data["healthy"]["deltas"]))
    print("verify:")
    print(report)
    if not ok:
        print("RESULT: BLOCKED_EVIDENCE_RECOMPUTE_CONFLICT "
              "(recompute deviates from frozen anchors; not rendering).")
        raise SystemExit(2)
    if args.verify:
        print("RESULT: PASS (all anchors reproduced within tolerance)")
        return
    svg, png = render(rows, data)
    csvp = write_csv(rows, data)
    print("rendered:", svg)
    print("rendered:", png)
    print("csv:", csvp)


if __name__ == "__main__":
    main()
