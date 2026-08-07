#!/usr/bin/env python3
"""Recompute CCISP scheduling-only evidence directly from historical Git blobs.

The source package lives in a historical commit and is intentionally not
copied into the current branch.  This tool streams the raw performance and
timing JSON shards from ``git archive`` and derives only the float scheduling
lineage (A-F versus B-F).  Fixed-point fields are deliberately excluded.
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import tarfile
from collections import defaultdict
from pathlib import Path
from statistics import mean, median, stdev

from scipy.stats import t as student_t


RESULT_PREFIX = (
    "projects/simulation/results/"
    "2b_fixed_point_branch_routed_cpr_closure"
)
METHODS = ("A-F", "B-F")


def _raw_documents(repo_root: Path, source_commit: str):
    command = [
        "git",
        "archive",
        "--format=tar",
        source_commit,
        RESULT_PREFIX,
    ]
    process = subprocess.Popen(
        command,
        cwd=repo_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdout is not None
    assert process.stderr is not None
    try:
        with tarfile.open(fileobj=process.stdout, mode="r|") as archive:
            for member in archive:
                if not member.isfile() or not member.name.endswith(".json"):
                    continue
                if "/performance-" not in member.name and "/timing-" not in member.name:
                    continue
                fileobj = archive.extractfile(member)
                if fileobj is None:
                    raise RuntimeError(f"cannot read archived member: {member.name}")
                yield member.name, json.load(fileobj)
    finally:
        process.stdout.close()
    stderr = process.stderr.read().decode("utf-8", errors="replace")
    return_code = process.wait()
    if return_code != 0:
        raise RuntimeError(f"git archive failed ({return_code}): {stderr.strip()}")


def _cell_key(document: dict) -> tuple[str, float, int]:
    cell = document["cell"]
    return cell["scene"], float(cell["snr_db"]), int(cell["seed_index"])


def _one_sided_t_upper(values: list[float], confidence: float = 0.95) -> float:
    if len(values) < 2:
        raise ValueError("at least two clusters are required")
    critical = float(student_t.ppf(confidence, len(values) - 1))
    return mean(values) + critical * stdev(values) / math.sqrt(len(values))


def recompute_from_commit(repo_root: Path, source_commit: str) -> dict:
    repo_root = Path(repo_root).resolve()
    performance: dict[tuple[str, float, int], dict] = {}
    timing: dict[tuple[str, float, int], dict] = {}

    for name, document in _raw_documents(repo_root, source_commit):
        schema = document.get("schema")
        if schema == "t005.performance-shard.v1":
            target = performance
        elif schema == "t005.timing-shard.v1":
            target = timing
        else:
            continue
        key = _cell_key(document)
        if key in target:
            raise ValueError(f"duplicate shard for {key}: {name}")
        target[key] = document

    if set(performance) != set(timing):
        missing_timing = sorted(set(performance) - set(timing))
        missing_performance = sorted(set(timing) - set(performance))
        raise ValueError(
            "performance/timing key mismatch: "
            f"missing_timing={missing_timing[:3]}, "
            f"missing_performance={missing_performance[:3]}"
        )
    if not performance:
        raise ValueError("no raw performance shards found")

    windows_per_cell_values = {int(doc["cell"]["n_windows"]) for doc in performance.values()}
    if len(windows_per_cell_values) != 1:
        raise ValueError(f"mixed windows-per-cell values: {sorted(windows_per_cell_values)}")
    windows_per_cell = windows_per_cell_values.pop()
    total_windows = len(performance) * windows_per_cell

    command_mismatches = 0
    selected_output_mismatches = 0
    command_hash_mismatched_shards = 0
    selected_output_hash_mismatched_shards = 0
    ber_count_mismatched_cells = 0
    receipt_mismatched_cells = 0
    pooled = {method: {"errors": 0, "bits": 0} for method in METHODS}
    operations = {method: defaultdict(int) for method in METHODS}
    selected_branch_counts = {method: defaultdict(int) for method in METHODS}
    storage_peak = {method: defaultdict(int) for method in METHODS}

    for key, shard in performance.items():
        identity = shard["identity"]
        command_mismatches += int(identity["af_bf_command_mismatches"])
        selected_output_mismatches += int(identity["af_bf_selected_output_mismatches"])
        rows = {row["method"]: row for row in shard["methods"]}
        command_hash_mismatched_shards += int(
            rows["A-F"]["command_sha256"] != rows["B-F"]["command_sha256"]
        )
        selected_output_hash_mismatched_shards += int(
            rows["A-F"]["selected_output_sha256"]
            != rows["B-F"]["selected_output_sha256"]
        )
        ber_count_mismatched_cells += int(
            (
                int(rows["A-F"]["common768_errors"]),
                int(rows["A-F"]["common768_bits"]),
            )
            != (
                int(rows["B-F"]["common768_errors"]),
                int(rows["B-F"]["common768_bits"]),
            )
        )
        receipt_mismatched_cells += int(
            shard["receipt_sha256"] != timing[key]["receipt_sha256"]
        )
        for method in METHODS:
            row = rows[method]
            pooled[method]["errors"] += int(row["common768_errors"])
            pooled[method]["bits"] += int(row["common768_bits"])
            for key, value in row["operations"].items():
                operations[method][key] += int(value)
            for branch, value in row["branch_counts"].items():
                selected_branch_counts[method][branch] += int(value)
            for key, value in row["storage"].items():
                storage_peak[method][key] = max(storage_peak[method][key], int(value))

    timing_ratios_by_seed: dict[int, list[float]] = defaultdict(list)
    median_ns = {method: [] for method in METHODS}
    contended_samples = 0
    maximum_system_load = 0.0
    post_timing_loads: list[float] = []
    affinity_values: set[tuple[int, ...]] = set()
    thread_env_values: set[tuple[tuple[str, str], ...]] = set()
    warmups_per_method: set[int] = set()
    measured_repetitions: set[int] = set()

    for key, shard in timing.items():
        plan = shard["plan"]
        warmups_per_method.add(int(plan["warmups_per_method"]))
        measured_repetitions.add(int(plan["measured_repetitions"]))
        repetitions = shard["repetitions"]
        for method in METHODS:
            observed = [int(row["elapsed_ns"]) for row in repetitions if row["method"] == method]
            if len(observed) != int(plan["measured_repetitions"]):
                raise ValueError(f"invalid {method} repetition count for {key}: {len(observed)}")
            if float(median(observed)) != float(shard["medians_ns"][method]):
                raise ValueError(f"invalid {method} median for {key}")
        medians = shard["medians_ns"]
        for method in METHODS:
            median_ns[method].append(float(medians[method]))
        timing_ratios_by_seed[key[2]].append(float(medians["B-F"]) / float(medians["A-F"]))
        affinity_values.add(tuple(int(value) for value in shard["platform"]["affinity"]))
        thread_env_values.add(
            tuple(sorted((str(k), str(v)) for k, v in shard["platform"]["thread_env"].items()))
        )
        post_timing_loads.append(float(shard["platform"]["cpu_load_percent"]))
        for sample_name in ("before", "after"):
            sample = shard["contention"][sample_name]
            contended_samples += int(bool(sample["contended"]))
            maximum_system_load = max(maximum_system_load, float(sample["system_load_percent"]))

    cluster_ratios = [mean(values) for _, values in sorted(timing_ratios_by_seed.items())]
    ratio_point = mean(cluster_ratios)
    ratio_upper = _one_sided_t_upper(cluster_ratios)
    avg_batch_ms = {method: mean(values) / 1e6 for method, values in median_ns.items()}
    avg_window_us = {
        method: avg_batch_ms[method] * 1000.0 / windows_per_cell for method in METHODS
    }
    reductions = {
        key: 1.0 - operations["B-F"][key] / operations["A-F"][key]
        for key in operations["A-F"]
        if operations["A-F"][key] != 0
    }

    for method in METHODS:
        pooled[method]["ber"] = pooled[method]["errors"] / pooled[method]["bits"]

    return {
        "schema": "ccisp.single-branch-evidence-recompute.v1",
        "source": {
            "commit": source_commit,
            "raw_prefix": RESULT_PREFIX,
            "fixed_point_excluded": True,
        },
        "scope": {
            "cells": len(performance),
            "performance_shards": len(performance),
            "timing_shards": len(timing),
            "windows_per_cell": windows_per_cell,
            "total_windows": total_windows,
            "seed_clusters": len(cluster_ratios),
        },
        "identity": {
            "command_mismatches": command_mismatches,
            "selected_output_mismatches": selected_output_mismatches,
            "command_hash_mismatched_shards": command_hash_mismatched_shards,
            "selected_output_hash_mismatched_shards": selected_output_hash_mismatched_shards,
            "ber_count_mismatched_cells": ber_count_mismatched_cells,
            "performance_timing_receipt_mismatched_cells": receipt_mismatched_cells,
            "ber_equal": pooled["A-F"] == pooled["B-F"],
            "A-F": pooled["A-F"],
            "B-F": pooled["B-F"],
        },
        "timing": {
            "cluster_definition": "seed index; each cluster averages 3 scenes x 11 SNR cells",
            "bf_over_af_cluster_mean": ratio_point,
            "bf_over_af_one_sided95_upper": ratio_upper,
            "cluster_count": len(cluster_ratios),
            "average_400_window_batch_ms": avg_batch_ms,
            "average_per_window_us": avg_window_us,
            "latency_reduction_from_cluster_mean": 1.0 - ratio_point,
        },
        "branch_calls": {
            "A-F": {"da": total_windows, "nda": total_windows},
            "B-F": dict(sorted(selected_branch_counts["B-F"].items())),
            "total_reduction": 1.0 - total_windows / (2.0 * total_windows),
        },
        "selected_branch_counts": {
            method: dict(sorted(counts.items())) for method, counts in selected_branch_counts.items()
        },
        "operations": {
            method: dict(sorted(values.items())) for method, values in operations.items()
        },
        "operation_reduction": dict(sorted(reductions.items())),
        "storage_peak": {
            method: dict(sorted(values.items())) for method, values in storage_peak.items()
        },
        "timing_contract": {
            "contention_samples": len(timing) * 2,
            "contended_samples": contended_samples,
            "maximum_system_load_percent": maximum_system_load,
            "warmups_per_method_values": sorted(warmups_per_method),
            "measured_repetitions_values": sorted(measured_repetitions),
            "post_timing_cpu_load_max_percent": max(post_timing_loads),
            "post_timing_cpu_load_ge_60_count": sum(value >= 60.0 for value in post_timing_loads),
            "post_timing_load_is_non_gating": True,
            "affinity_values": [list(values) for values in sorted(affinity_values)],
            "thread_env_values": [dict(values) for values in sorted(thread_env_values)],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-commit", default="67970307a051dd8149e1a750498a20674dfcfe6f")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = recompute_from_commit(args.repo_root, args.source_commit)
    encoded = json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if args.output is None:
        print(encoded, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")


if __name__ == "__main__":
    main()
