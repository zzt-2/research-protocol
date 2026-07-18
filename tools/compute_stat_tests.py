#!/usr/bin/env python3
"""
Compute bootstrap 95% CI and Welch's t-test for three thesis chapters.

Usage:
    cd /mnt/d/code/study/research-protocol
    ~/.venvs/torch/bin/python tools/compute_stat_tests.py

Output:
    - Printed tables to stdout
    - JSON files saved to each chapter's results directory
"""

import json
import numpy as np
from scipy import stats
from pathlib import Path

ROOT = Path("/mnt/d/code/study/research-protocol")
N_BOOT = 10000
ALPHA = 0.05
RNG = np.random.default_rng(42)


def bootstrap_ci(data, n_boot=N_BOOT, alpha=ALPHA, rng=RNG):
    """Compute bootstrap percentile CI for the mean."""
    data = np.asarray(data, dtype=float)
    n = len(data)
    boot_means = np.empty(n_boot)
    for i in range(n_boot):
        sample = rng.choice(data, size=n, replace=True)
        boot_means[i] = sample.mean()
    lo = np.percentile(boot_means, 100 * alpha / 2)
    hi = np.percentile(boot_means, 100 * (1 - alpha / 2))
    return float(lo), float(hi)


def welch_t(a, b):
    """Welch's t-test (two-sided). Returns t_stat, p_value."""
    t_stat, p_value = stats.ttest_ind(a, b, equal_var=False)
    return float(t_stat), float(p_value)


def format_row(name, values, ci, t_stat=None, p_val=None):
    """Format one result row."""
    mean = np.mean(values)
    std = np.std(values, ddof=1)
    ci_lo, ci_hi = ci
    sig = ""
    if p_val is not None:
        sig = "YES" if p_val < ALPHA else "no"
    t_str = f"{t_stat:.4f}" if t_stat is not None else "-"
    p_str = f"{p_val:.4f}" if p_val is not None else "-"
    return (
        f"{name:<40s} | {mean:.4f} +/- {std:.4f} | "
        f"[{ci_lo:.4f}, {ci_hi:.4f}] | {t_str:>10s} | {p_str:>10s} | {sig}"
    )


# ============================================================
# Ch1: GNN Routing
# ============================================================
def process_ch1():
    print("=" * 100)
    print("Ch1: GNN Routing - Statistical Tests")
    print("=" * 100)

    fpath = ROOT / "projects/leo-mega-constellation-gnn-routing/simulator/results/ch1_multi_seed_results.json"
    with open(fpath) as f:
        data = json.load(f)

    results = {"bootstrap_ci": {}, "welch_t": {}}

    header = (
        f"{'Metric':<40s} | {'mean +/- std':^18s} | "
        f"{'95% CI':^22s} | {'t-stat':>10s} | {'p-value':>10s} | sig"
    )
    print(header)
    print("-" * 100)

    # --- Bootstrap CI for each group ---
    groups = {
        "full (cross-scale)": "full",
        "same (single-scale)": "same",
        "A1 (no PE)": "A1",
        "A2 (single-scale)": "A2",
        "A3 (no PE + single-scale)": "A3",
    }

    group_stretch = {}
    group_delay = {}

    for label, key in groups.items():
        g = data[key]
        stretch_vals = np.array(g["mean_stretch"]["values"])
        delay_vals = np.array(g["mean_delay"]["values"])

        group_stretch[key] = stretch_vals
        group_delay[key] = delay_vals

        s_ci = bootstrap_ci(stretch_vals)
        d_ci = bootstrap_ci(delay_vals)

        results["bootstrap_ci"][key] = {
            "stretch": {"values": stretch_vals.tolist(), "mean": float(np.mean(stretch_vals)),
                        "std": float(np.std(stretch_vals, ddof=1)), "ci_95": list(s_ci)},
            "delay": {"values": delay_vals.tolist(), "mean": float(np.mean(delay_vals)),
                      "std": float(np.std(delay_vals, ddof=1)), "ci_95": list(d_ci)},
        }

        print(format_row(f"{label} stretch", stretch_vals, s_ci))
        print(format_row(f"{label} delay (ms)", delay_vals, d_ci))

    # --- Welch's t-tests ---
    print("\n--- Welch's t-tests ---")
    print(header)
    print("-" * 100)

    # full vs same: stretch
    t, p = welch_t(group_stretch["full"], group_stretch["same"])
    ci = bootstrap_ci(group_stretch["full"])
    results["welch_t"]["full_vs_same_stretch"] = {"t": t, "p": p, "significant": p < ALPHA}
    print(format_row("full vs same stretch", group_stretch["full"], ci, t, p))

    # full vs same: delay
    t, p = welch_t(group_delay["full"], group_delay["same"])
    ci = bootstrap_ci(group_delay["full"])
    results["welch_t"]["full_vs_same_delay"] = {"t": t, "p": p, "significant": p < ALPHA}
    print(format_row("full vs same delay", group_delay["full"], ci, t, p))

    # Ablations: full vs each ablation on stretch
    for ablation_key, ablation_label in [("A1", "A1 (no PE)"), ("A2", "A2 (single-scale)"), ("A3", "A3 (no PE+single)")]:
        t, p = welch_t(group_stretch["full"], group_stretch[ablation_key])
        ci = bootstrap_ci(group_stretch[ablation_key])
        results["welch_t"][f"full_vs_{ablation_key}_stretch"] = {"t": t, "p": p, "significant": p < ALPHA}
        print(format_row(f"full vs {ablation_label} stretch", group_stretch[ablation_key], ci, t, p))

    # Save
    out_path = ROOT / "projects/leo-mega-constellation-gnn-routing/simulator/results/stat_tests.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nSaved to {out_path}")
    return results


# ============================================================
# Ch2: LEO NTN Handover DRL
# ============================================================
def process_ch2():
    print("\n" + "=" * 100)
    print("Ch2: LEO NTN Handover DRL - Statistical Tests")
    print("=" * 100)

    base = ROOT / "projects/leo-ntn-handover-drl/results"

    def load_eval_files(prefix, seeds=(1, 2, 3)):
        """Load eval results from multiple seed files. Returns list of eval dicts (one per seed)."""
        all_eval = []
        for s in seeds:
            fpath = base / f"{prefix}_s{s}_results.json"
            with open(fpath) as f:
                d = json.load(f)
            # Each file has an "eval" list with 3 eval seeds.
            # We take the mean across eval seeds as the representative value for this train seed.
            eval_list = d["eval"]
            all_eval.append(eval_list)
        return all_eval

    def aggregate_metric(eval_seeds, metric_key, blocking_key=None):
        """
        Given list of eval lists (one per train seed), extract metric.
        For blocking, try both 'blocking' and 'mean_blocking_rate'.
        Returns array of per-seed means.
        """
        vals = []
        for eval_list in eval_seeds:
            seed_vals = []
            for ev in eval_list:
                if blocking_key and blocking_key == "blocking":
                    # Ch2 C6 uses "blocking", E4 uses "mean_blocking_rate"
                    v = ev.get("blocking", ev.get("mean_blocking_rate", None))
                elif blocking_key and blocking_key == "mean_blocking_rate":
                    v = ev.get("mean_blocking_rate", ev.get("blocking", None))
                else:
                    v = ev[metric_key]
                if v is not None:
                    seed_vals.append(v)
            vals.append(np.mean(seed_vals))
        return np.array(vals)

    results = {"bootstrap_ci": {}, "welch_t": {}}

    header = (
        f"{'Metric':<40s} | {'mean +/- std':^18s} | "
        f"{'95% CI':^22s} | {'t-stat':>10s} | {'p-value':>10s} | sig"
    )
    print(header)
    print("-" * 100)

    # --- Load data ---
    # E4 = GNN+DDQN (proposed), uses c_gnn_ddqn.py, has gnn_lr/T/out
    # C6 = MLP baseline, uses flat_dim, standard DDQN with MLP
    configs = {
        "20UE (d20)": {"gnn": "E4-20-d20", "mlp": "C6-20-d20"},
        "50UE (c15-d20)": {"gnn": "E4-50-c15-d20", "mlp": "C6-50-c15-d20"},
        "100UE size-gen (c25)": {"gnn": "E4-100-c25", "mlp": "C6-100-c25"},
    }

    all_data = {}

    for scenario, methods in configs.items():
        for method_label, prefix in methods.items():
            eval_data = load_eval_files(prefix)
            rewards = aggregate_metric(eval_data, "reward")
            blocking = aggregate_metric(eval_data, "blocking", blocking_key="blocking")

            all_data[(scenario, method_label)] = {
                "reward": rewards,
                "blocking": blocking,
            }

            # Bootstrap CI for reward
            r_ci = bootstrap_ci(rewards)
            b_ci = bootstrap_ci(blocking)

            key = f"{scenario}/{method_label}"
            results["bootstrap_ci"][key] = {
                "reward": {"values": rewards.tolist(), "mean": float(np.mean(rewards)),
                           "std": float(np.std(rewards, ddof=1)), "ci_95": list(r_ci)},
                "blocking": {"values": blocking.tolist(), "mean": float(np.mean(blocking)),
                             "std": float(np.std(blocking, ddof=1)), "ci_95": list(b_ci)},
            }

            print(format_row(f"{key} reward", rewards, r_ci))
            print(format_row(f"{key} blocking", blocking, b_ci))

    # --- Welch's t-tests: GNN vs MLP ---
    print("\n--- Welch's t-tests (GNN vs MLP) ---")
    print(header)
    print("-" * 100)

    for scenario in configs:
        gnn_r = all_data[(scenario, "gnn")]["reward"]
        mlp_r = all_data[(scenario, "mlp")]["reward"]
        gnn_b = all_data[(scenario, "gnn")]["blocking"]
        mlp_b = all_data[(scenario, "mlp")]["blocking"]

        t_r, p_r = welch_t(gnn_r, mlp_r)
        t_b, p_b = welch_t(gnn_b, mlp_b)

        ci_r = bootstrap_ci(gnn_r)
        ci_b = bootstrap_ci(gnn_b)

        key_r = f"{scenario}/gnn_vs_mlp_reward"
        key_b = f"{scenario}/gnn_vs_mlp_blocking"
        results["welch_t"][key_r] = {"t": t_r, "p": p_r, "significant": p_r < ALPHA}
        results["welch_t"][key_b] = {"t": t_b, "p": p_b, "significant": p_b < ALPHA}

        print(format_row(f"{scenario} GNN vs MLP reward", gnn_r, ci_r, t_r, p_r))
        print(format_row(f"{scenario} GNN vs MLP blocking", gnn_b, ci_b, t_b, p_b))

    # Save
    out_path = base / "stat_tests.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nSaved to {out_path}")
    return results


# ============================================================
# Ch3: HGAT DAG Offloading
# ============================================================
def process_ch3():
    print("\n" + "=" * 100)
    print("Ch3: HGAT DAG Offloading - Statistical Tests")
    print("=" * 100)

    base = ROOT / "projects/hgat-satellite-dag-offloading/simulator/results"

    # For learned models, we use the converged episode rewards.
    # The rewards are bimodal (converged ~-38 vs failed <-100k).
    # We use mean reward per seed as the summary statistic (same as results_summary.json).
    # For greedy/random baselines, they have 500 episodes each.

    results = {"bootstrap_ci": {}, "welch_t": {}}

    header = (
        f"{'Metric':<40s} | {'mean +/- std':^18s} | "
        f"{'95% CI':^22s} | {'t-stat':>10s} | {'p-value':>10s} | sig"
    )
    print(header)
    print("-" * 100)

    # Load per-seed mean rewards
    model_seeds = {"hgat": [42, 123, 456], "gcn": [42, 123, 456],
                   "graphsage": [42, 123, 456], "mlp": [42, 123, 456],
                   "greedy": [42, 123, 456], "random": [42, 123, 456]}

    model_means = {}
    for model, seeds in model_seeds.items():
        means = []
        for seed in seeds:
            fpath = base / f"{model}_seed{seed}.json"
            with open(fpath) as f:
                d = json.load(f)
            rewards = d["episode_rewards"]
            means.append(np.mean(rewards))
        model_means[model] = np.array(means)

    # Bootstrap CI for each model
    for model in ["hgat", "gcn", "graphsage", "mlp", "greedy", "random"]:
        vals = model_means[model]
        ci = bootstrap_ci(vals)
        results["bootstrap_ci"][model] = {
            "values": vals.tolist(), "mean": float(np.mean(vals)),
            "std": float(np.std(vals, ddof=1)), "ci_95": list(ci),
        }
        print(format_row(f"{model} mean reward", vals, ci))

    # Welch's t: HGAT vs each baseline
    print("\n--- Welch's t-tests (HGAT vs baselines) ---")
    print(header)
    print("-" * 100)

    hgat = model_means["hgat"]
    for baseline in ["gcn", "graphsage", "mlp", "greedy", "random"]:
        bvals = model_means[baseline]
        t, p = welch_t(hgat, bvals)
        ci = bootstrap_ci(hgat)
        results["welch_t"][f"hgat_vs_{baseline}"] = {
            "t": t, "p": p, "significant": p < ALPHA,
        }
        print(format_row(f"HGAT vs {baseline} reward", hgat, ci, t, p))

    # Save
    out_path = base / "stat_tests.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nSaved to {out_path}")
    return results


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    np.set_printoptions(precision=6)
    r1 = process_ch1()
    r2 = process_ch2()
    r3 = process_ch3()
    print("\n" + "=" * 100)
    print("All statistical tests completed.")
    print("=" * 100)
