"""Statistical significance testing for LEO congestion routing experiments.

Provides bootstrap confidence intervals, paired bootstrap tests,
Wilcoxon signed-rank tests, and a master function that runs all
comparisons between GNN, ECMP, and MLP methods.

Only depends on numpy and scipy.stats.
"""

from __future__ import annotations

import numpy as np
from scipy import stats


def bootstrap_ci(
    data: list[float] | np.ndarray,
    n_bootstrap: int = 10000,
    ci: float = 0.95,
    rng: np.random.Generator | None = None,
) -> tuple[float, float, float]:
    """Compute bootstrap confidence interval for the mean.

    Args:
        data: List/array of observations (e.g. per-episode MLU values).
        n_bootstrap: Number of bootstrap resamples.
        ci: Confidence level (0.95 = 95% CI).
        rng: Optional numpy random generator for reproducibility.

    Returns:
        (mean, ci_lower, ci_upper)
    """
    arr = np.asarray(data, dtype=np.float64)
    if rng is None:
        rng = np.random.default_rng(42)

    n = len(arr)
    boot_means = np.empty(n_bootstrap)
    for i in range(n_bootstrap):
        sample = rng.choice(arr, size=n, replace=True)
        boot_means[i] = sample.mean()

    alpha = 1.0 - ci
    lo = np.percentile(boot_means, 100 * alpha / 2)
    hi = np.percentile(boot_means, 100 * (1 - alpha / 2))

    return float(arr.mean()), float(lo), float(hi)


def paired_bootstrap_test(
    a: list[float] | np.ndarray,
    b: list[float] | np.ndarray,
    n_bootstrap: int = 10000,
    rng: np.random.Generator | None = None,
) -> tuple[float, float, tuple[float, float]]:
    """Paired bootstrap test: is method A significantly better than B?

    Tests H0: mean(A) >= mean(B) vs H1: mean(A) < mean(B).
    For MLU (lower is better), A better than B means A < B.

    Args:
        a: Per-episode MLU values for method A.
        b: Per-episode MLU values for method B (same length, paired).
        n_bootstrap: Number of bootstrap resamples.
        rng: Optional numpy random generator.

    Returns:
        (p_value, effect_size_cohen_d, (ci_lower_diff, ci_upper_diff))
        where diff = mean(A) - mean(B).
    """
    a_arr = np.asarray(a, dtype=np.float64)
    b_arr = np.asarray(b, dtype=np.float64)
    assert len(a_arr) == len(b_arr), "Paired test requires equal-length arrays"

    if rng is None:
        rng = np.random.default_rng(42)

    n = len(a_arr)
    observed_diff = a_arr.mean() - b_arr.mean()

    # Cohen's d (paired: use std of differences)
    diffs = a_arr - b_arr
    pooled_std = diffs.std(ddof=1)
    cohens_d = float(observed_diff / pooled_std) if pooled_std > 0 else 0.0

    # Bootstrap on paired differences
    boot_diffs = np.empty(n_bootstrap)
    for i in range(n_bootstrap):
        idx = rng.choice(n, size=n, replace=True)
        boot_diffs[i] = a_arr[idx].mean() - b_arr[idx].mean()

    # p-value: fraction of bootstrap diffs <= 0 (if observed < 0, i.e. A better)
    # For a two-sided test we use |diff|
    p_value = float(np.mean(boot_diffs >= 0)) if observed_diff < 0 else float(np.mean(boot_diffs <= 0))
    # Ensure two-sided
    p_value = min(p_value * 2, 1.0)

    ci_lo = float(np.percentile(boot_diffs, 2.5))
    ci_hi = float(np.percentile(boot_diffs, 97.5))

    return p_value, cohens_d, (ci_lo, ci_hi)


def wilcoxon_test(
    a: list[float] | np.ndarray,
    b: list[float] | np.ndarray,
) -> tuple[float, float]:
    """Wilcoxon signed-rank test (non-parametric paired test).

    Suitable for small sample sizes (e.g. 3 per-seed mean MLUs).

    Args:
        a: Per-seed mean MLU values for method A.
        b: Per-seed mean MLU values for method B (same length, paired).

    Returns:
        (statistic, p_value)
    """
    a_arr = np.asarray(a, dtype=np.float64)
    b_arr = np.asarray(b, dtype=np.float64)
    assert len(a_arr) == len(b_arr), "Paired test requires equal-length arrays"

    # scipy wilcoxon requires at least 1 non-zero difference
    diff = a_arr - b_arr
    if np.all(diff == 0):
        return 0.0, 1.0

    # Use exact for small n, otherwise asymptotic
    result = stats.wilcoxon(a_arr, b_arr, alternative="two-sided")
    return float(result.statistic), float(result.pvalue)


def compute_all_stats(
    gnn_seeds: list[list[float]],
    ecmp_mlus: list[float],
    mlp_seeds: list[list[float]],
) -> dict:
    """Run all statistical tests comparing GNN vs baselines.

    Args:
        gnn_seeds: List of per-episode MLU lists, one per GNN seed.
                   e.g. [[mlu_s0_ep0, mlu_s0_ep1, ...], [mlu_s1_ep0, ...], ...]
        ecmp_mlus: Per-episode MLU values for ECMP baseline.
        mlp_seeds: List of per-episode MLU lists, one per MLP seed.

    Returns:
        Dict with all test results structured for reporting.
    """
    rng = np.random.default_rng(42)

    # Flatten per-episode MLUs across seeds
    gnn_all = np.concatenate(gnn_seeds).tolist()
    mlp_all = np.concatenate(mlp_seeds).tolist()
    ecmp_all = list(ecmp_mlus)

    # Per-seed means (for Wilcoxon)
    gnn_seed_means = [float(np.mean(s)) for s in gnn_seeds]
    mlp_seed_means = [float(np.mean(s)) for s in mlp_seeds]
    ecmp_arr = np.asarray(ecmp_all)
    ecmp_seed_means = [float(ecmp_arr[i * len(ecmp_arr) // len(gnn_seeds):(i + 1) * len(ecmp_arr) // len(gnn_seeds)].mean())
                       for i in range(len(gnn_seeds))]

    # Bootstrap CIs
    gnn_mean, gnn_ci_lo, gnn_ci_hi = bootstrap_ci(gnn_all, rng=rng)
    ecmp_mean, ecmp_ci_lo, ecmp_ci_hi = bootstrap_ci(ecmp_all, rng=rng)
    mlp_mean, mlp_ci_lo, mlp_ci_hi = bootstrap_ci(mlp_all, rng=rng)

    # Paired bootstrap: GNN vs ECMP
    # For pairing: align by episode index (truncate to min length, tile shorter if needed)
    n_pairs = min(len(gnn_all), len(ecmp_all))
    gnn_vs_ecmp_p, gnn_vs_ecmp_d, gnn_vs_ecmp_ci = paired_bootstrap_test(
        gnn_all[:n_pairs], ecmp_all[:n_pairs], rng=rng,
    )

    # Paired bootstrap: GNN vs MLP
    n_pairs = min(len(gnn_all), len(mlp_all))
    gnn_vs_mlp_p, gnn_vs_mlp_d, gnn_vs_mlp_ci = paired_bootstrap_test(
        gnn_all[:n_pairs], mlp_all[:n_pairs], rng=rng,
    )

    # Paired bootstrap: MLP vs ECMP
    n_pairs = min(len(mlp_all), len(ecmp_all))
    mlp_vs_ecmp_p, mlp_vs_ecmp_d, mlp_vs_ecmp_ci = paired_bootstrap_test(
        mlp_all[:n_pairs], ecmp_all[:n_pairs], rng=rng,
    )

    # Wilcoxon tests (per-seed means)
    gnn_ecmp_w_stat, gnn_ecmp_w_p = wilcoxon_test(gnn_seed_means, ecmp_seed_means)
    gnn_mlp_w_stat, gnn_mlp_w_p = wilcoxon_test(gnn_seed_means, mlp_seed_means)

    return {
        "gnn": {
            "mean": gnn_mean,
            "std": float(np.std(gnn_all, ddof=1)),
            "ci_95": (gnn_ci_lo, gnn_ci_hi),
            "n_episodes": len(gnn_all),
            "seed_means": gnn_seed_means,
        },
        "ecmp": {
            "mean": ecmp_mean,
            "std": float(np.std(ecmp_all, ddof=1)),
            "ci_95": (ecmp_ci_lo, ecmp_ci_hi),
            "n_episodes": len(ecmp_all),
        },
        "mlp": {
            "mean": mlp_mean,
            "std": float(np.std(mlp_all, ddof=1)),
            "ci_95": (mlp_ci_lo, mlp_ci_hi),
            "n_episodes": len(mlp_all),
            "seed_means": mlp_seed_means,
        },
        "paired_bootstrap": {
            "gnn_vs_ecmp": {
                "p_value": gnn_vs_ecmp_p,
                "cohens_d": gnn_vs_ecmp_d,
                "diff_ci_95": gnn_vs_ecmp_ci,
                "significant_005": gnn_vs_ecmp_p < 0.05,
            },
            "gnn_vs_mlp": {
                "p_value": gnn_vs_mlp_p,
                "cohens_d": gnn_vs_mlp_d,
                "diff_ci_95": gnn_vs_mlp_ci,
                "significant_005": gnn_vs_mlp_p < 0.05,
            },
            "mlp_vs_ecmp": {
                "p_value": mlp_vs_ecmp_p,
                "cohens_d": mlp_vs_ecmp_d,
                "diff_ci_95": mlp_vs_ecmp_ci,
                "significant_005": mlp_vs_ecmp_p < 0.05,
            },
        },
        "wilcoxon": {
            "gnn_vs_ecmp": {"statistic": gnn_ecmp_w_stat, "p_value": gnn_ecmp_w_p},
            "gnn_vs_mlp": {"statistic": gnn_mlp_w_stat, "p_value": gnn_mlp_w_p},
        },
    }


def format_results_table(stats: dict) -> str:
    """Format statistical results as a markdown table for the paper.

    Includes: method, mean MLU, 95% CI, vs ECMP (p, d), vs MLP (p, d).

    Args:
        stats: Output dict from compute_all_stats.

    Returns:
        Markdown-formatted table string.
    """
    lines = []

    # Header
    lines.append("### Statistical Significance Test Results")
    lines.append("")
    lines.append("| Method | Mean MLU | 95% CI | vs ECMP (p, d) | vs MLP (p, d) |")
    lines.append("|--------|----------|--------|-----------------|---------------|")

    def _fmt_ci(ci):
        return f"[{ci[0]:.4f}, {ci[1]:.4f}]"

    def _fmt_test(p, d, sig):
        marker = " *" if sig else ""
        return f"p={p:.4f}, d={d:.2f}{marker}"

    gnn = stats["gnn"]
    ecmp = stats["ecmp"]
    mlp = stats["mlp"]
    pb = stats["paired_bootstrap"]

    # GNN row
    lines.append(
        f"| GNN | {gnn['mean']:.4f} | {_fmt_ci(gnn['ci_95'])} "
        f"| {_fmt_test(pb['gnn_vs_ecmp']['p_value'], pb['gnn_vs_ecmp']['cohens_d'], pb['gnn_vs_ecmp']['significant_005'])} "
        f"| {_fmt_test(pb['gnn_vs_mlp']['p_value'], pb['gnn_vs_mlp']['cohens_d'], pb['gnn_vs_mlp']['significant_005'])} |"
    )

    # MLP row
    lines.append(
        f"| MLP | {mlp['mean']:.4f} | {_fmt_ci(mlp['ci_95'])} "
        f"| {_fmt_test(pb['mlp_vs_ecmp']['p_value'], pb['mlp_vs_ecmp']['cohens_d'], pb['mlp_vs_ecmp']['significant_005'])} "
        f"| -- |"
    )

    # ECMP row
    lines.append(
        f"| ECMP | {ecmp['mean']:.4f} | {_fmt_ci(ecmp['ci_95'])} "
        f"| -- | -- |"
    )

    lines.append("")
    lines.append("\\* p < 0.05 (paired bootstrap test, two-sided)")
    lines.append("")

    # Wilcoxon results
    lines.append("### Wilcoxon Signed-Rank Tests (per-seed means)")
    lines.append("")
    wx = stats["wilcoxon"]
    lines.append(f"- GNN vs ECMP: W = {wx['gnn_vs_ecmp']['statistic']:.1f}, p = {wx['gnn_vs_ecmp']['p_value']:.4f}")
    lines.append(f"- GNN vs MLP:  W = {wx['gnn_vs_mlp']['statistic']:.1f}, p = {wx['gnn_vs_mlp']['p_value']:.4f}")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Self-test with synthetic data
# ---------------------------------------------------------------------------

def _synthetic_test() -> None:
    """Verify stat_tests with synthetic data of known difference."""
    rng = np.random.default_rng(123)

    # GNN: mean=1.5, std=0.2 (better, lower MLU)
    # MLP: mean=2.0, std=0.3
    # ECMP: mean=2.2, std=0.25
    n_per_seed = 50
    n_seeds = 3

    gnn_seeds = []
    mlp_seeds = []
    ecmp_episodes = []
    for s in range(n_seeds):
        gnn_seed_data = rng.normal(1.5, 0.2, n_per_seed).tolist()
        mlp_seed_data = rng.normal(2.0, 0.3, n_per_seed).tolist()
        ecmp_data = rng.normal(2.2, 0.25, n_per_seed).tolist()
        gnn_seeds.append(gnn_seed_data)
        mlp_seeds.append(mlp_seed_data)
        ecmp_episodes.extend(ecmp_data)

    results = compute_all_stats(gnn_seeds, ecmp_episodes, mlp_seeds)
    table = format_results_table(results)

    print(table)

    # Basic sanity checks
    assert results["gnn"]["mean"] < results["mlp"]["mean"], "GNN should have lower MLU than MLP"
    assert results["gnn"]["mean"] < results["ecmp"]["mean"], "GNN should have lower MLU than ECMP"
    assert results["paired_bootstrap"]["gnn_vs_ecmp"]["p_value"] < 0.05, "GNN vs ECMP should be significant"
    assert results["paired_bootstrap"]["gnn_vs_mlp"]["p_value"] < 0.05, "GNN vs MLP should be significant"
    assert results["paired_bootstrap"]["gnn_vs_ecmp"]["cohens_d"] < 0, "Cohen's d should be negative (GNN better)"

    print("\n[ALL SYNTHETIC CHECKS PASSED]")
    return results


if __name__ == "__main__":
    _synthetic_test()
