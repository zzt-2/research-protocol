"""Deterministically recompute the existing P01/P02/T004 authority evidence.

This script reads immutable historical JSON and one historical Git commit.  It does
not call a simulator, generate a realization, or touch held-out seeds.
"""
from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import math
import subprocess
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev
from typing import Iterable

from scipy.stats import t


T004_COMMIT = "1140134e89e8b0571274944cb44471ab6403481f"
T004_DEV_PATH = "projects/simulation/results/2a_calibration_aware_cpr_closure/dev-results.json"
T004_FROZEN_PATH = "projects/simulation/results/2a_calibration_aware_cpr_closure/frozen-config.json"
T004_HELDOUT_PATHS = (
    "projects/simulation/results/2a_calibration_aware_cpr_closure/test-chronology.json",
    "projects/simulation/results/2a_calibration_aware_cpr_closure/heldout-raw.json",
    "projects/simulation/results/2a_calibration_aware_cpr_closure/heldout-summary.json",
)


def summarize(values: Iterable[float]) -> dict:
    vals = [float(value) for value in values]
    if not vals:
        raise ValueError("at least one seed-cluster value is required")
    center = mean(vals)
    if len(vals) == 1:
        half_width = 0.0
        sigma = 0.0
    else:
        sigma = stdev(vals)
        half_width = float(t.ppf(0.975, len(vals) - 1)) * sigma / math.sqrt(len(vals))
    return {
        "inference_unit": "seed_cluster",
        "n_clusters": len(vals),
        "mean_db": center,
        "std_db": sigma,
        "ci95": [center - half_width, center + half_width],
        "cluster_values_db": vals,
    }


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _git_json(repo_root: Path, commit: str, path: str) -> dict:
    payload = subprocess.check_output(
        ["git", "show", f"{commit}:{path}"], cwd=repo_root, text=True, encoding="utf-8"
    )
    return json.loads(payload)


def _git_path_exists(repo_root: Path, commit: str, path: str) -> bool:
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}:{path}"],
        cwd=repo_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _paired_by_seed(
    rows: list[dict],
    method_a: str,
    method_b: str,
    cells: set[tuple[str, float]],
    *,
    delta: float = 0.0,
) -> dict[int, float]:
    selected = {
        (row["scene"], float(row["gamma_true_db"]), int(row["seed_index"]), row["method"]):
        float(row["gain_db"])
        for row in rows
        if float(row["delta_db"]) == float(delta)
        and (row["scene"], float(row["gamma_true_db"])) in cells
        and row["method"] in {method_a, method_b}
    }
    seeds = sorted({key[2] for key in selected})
    by_seed: dict[int, float] = {}
    for seed in seeds:
        diffs = [
            selected[(scene, snr, seed, method_a)] - selected[(scene, snr, seed, method_b)]
            for scene, snr in sorted(cells)
        ]
        by_seed[seed] = mean(diffs)
    return by_seed


def _row_pair_summary(analysis_block: dict) -> dict:
    return {
        "inference_unit": "cell_seed_pair",
        "n_pairs": int(analysis_block["n_paired"]),
        "mean_db": float(analysis_block["mean_db"]),
        "ci95": [float(x) for x in analysis_block["ci95"]],
    }


def _p01_report(repo_root: Path) -> tuple[dict, list[dict]]:
    phase_a_path = repo_root / "projects/simulation/results/p01_cpr_snr_mismatch/phaseA_dev.json"
    phase_bc_path = repo_root / "projects/simulation/results/p01_cpr_snr_mismatch/phaseBC_heldout.json"
    phase_a = _load_json(phase_a_path)
    phase_bc = _load_json(phase_bc_path)

    dev_rows = phase_a["raw_rows"]
    heldout_rows = phase_bc["raw_rows"]
    dev_lookup = {
        (row["scene"], float(row["gamma_true_db"]), float(row["delta_db"]), int(row["seed_index"])):
        float(row["gain_db_common768"])
        for row in dev_rows
    }
    heldout_lookup = {
        (row["scene"], float(row["gamma_true_db"]), float(row["delta_db"]), int(row["seed_index"]), row["method"]):
        float(row["gain_db"])
        for row in heldout_rows
    }

    harm_rows: list[dict] = []
    for frozen in phase_a["harm_cells"]:
        scene = frozen["scene"]
        snr = float(frozen["gamma_true_db"])
        delta = float(frozen["delta_db"])
        dev_diffs = [
            dev_lookup[(scene, snr, delta, seed)] - dev_lookup[(scene, snr, 0.0, seed)]
            for seed in phase_a["seeds"]
        ]
        mismatch = summarize(dev_diffs)
        heldout_adapter_vs_d0 = [
            heldout_lookup[(scene, snr, delta, seed, "adapter_pilot")]
            - heldout_lookup[(scene, snr, 0.0, seed, "orig")]
            for seed in phase_bc["seeds"]
        ]
        heldout_adapter_vs_mismatch = [
            heldout_lookup[(scene, snr, delta, seed, "adapter_pilot")]
            - heldout_lookup[(scene, snr, delta, seed, "orig")]
            for seed in phase_bc["seeds"]
        ]
        residual = summarize(heldout_adapter_vs_d0)
        recovery = summarize(heldout_adapter_vs_mismatch)
        harm_rows.append(
            {
                "scene": scene,
                "snr_db": snr,
                "delta_db": delta,
                "dev_mismatch_drop": mismatch,
                "heldout_adapter_vs_d0": residual,
                "heldout_adapter_vs_mismatched_original": recovery,
                "strict_harm_resolved": residual["mean_db"] > -0.3,
            }
        )

    all_cells = {(row["scene"], float(row["gamma_true_db"])) for row in heldout_rows}
    safety = []
    for scene, snr in sorted(all_cells):
        values = [
            heldout_lookup[(scene, snr, 0.0, seed, "adapter_pilot")]
            - heldout_lookup[(scene, snr, 0.0, seed, "orig")]
            for seed in phase_bc["seeds"]
        ]
        result = summarize(values)
        result.update(
            {
                "scene": scene,
                "snr_db": snr,
                "material_degradation": result["mean_db"] <= -0.3 and result["ci95"][1] < 0,
            }
        )
        safety.append(result)

    report = {
        "source_hashes": {
            str(phase_a_path.relative_to(repo_root)).replace("\\", "/"): _sha256(phase_a_path),
            str(phase_bc_path.relative_to(repo_root)).replace("\\", "/"): _sha256(phase_bc_path),
        },
        "chronology": {
            "dev_seeds": phase_a["seeds"],
            "heldout_seeds": phase_bc["seeds"],
            "disjoint": set(phase_a["seeds"]).isdisjoint(phase_bc["seeds"]),
        },
        "harm_cell_count": len(harm_rows),
        "adapter_resolved_count": sum(row["strict_harm_resolved"] for row in harm_rows),
        "adapter_resolution_rate": sum(row["strict_harm_resolved"] for row in harm_rows) / len(harm_rows),
        "harm_cells": harm_rows,
        "safety_cells": safety,
        "material_safety_degradation_count": sum(row["material_degradation"] for row in safety),
        "deployable_identity": {
            "input": "receiver-known pilots in the current window",
            "action": "pilot-SNR estimate passed to the inherited CCISP decision",
            "truth_in_decide": False,
            "claim_ceiling": "local robustness adapter; not a new selector",
        },
    }
    return report, harm_rows


def _p02_source_identity(repo_root: Path, chosen_ref: float) -> dict:
    source_path = repo_root / "projects/simulation/explore/nda-awgn-tracking-sandbox/_p02_weakretune_adapter.py"
    probe_path = repo_root / "projects/simulation/explore/nda-awgn-tracking-sandbox/_p02_operating_regime_probe.py"
    source = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    function = next(
        node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "decide_adapter_weakretune"
    )
    args = [argument.arg for argument in function.args.args]
    has_scene_arg = any(name in {"scene", "region", "turbulence", "true_snr_db"} for name in args)
    return {
        "decide_signature": f"decide_adapter_weakretune({', '.join(args)})",
        "runtime_region_input": has_scene_arg,
        "evaluation_target_region": "TARGET_CELLS = weak@{5,7,9} dB in the probe; scene/SNR labels select the scored slice, not the decide action",
        "frozen_scalar_ref_snr_db": chosen_ref,
        "distinct_calibration_actions": 1,
        "actual_action": "one dev-frozen scalar reference applied to every evaluated cell",
        "truth_in_decide": False,
        "source_hashes": {
            str(source_path.relative_to(repo_root)).replace("\\", "/"): _sha256(source_path),
            str(probe_path.relative_to(repo_root)).replace("\\", "/"): _sha256(probe_path),
        },
    }


def _p02_report(repo_root: Path) -> dict:
    dev_path = repo_root / "projects/simulation/results/p02_cand_rank_operating_regime/dev_tuning.json"
    heldout_path = repo_root / "projects/simulation/results/p02_cand_rank_operating_regime/heldout_confirmation.json"
    dev = _load_json(dev_path)
    heldout = _load_json(heldout_path)
    target = {(str(scene), float(snr)) for scene, snr in heldout["cells"]["target"]}
    boundary = {(str(scene), float(snr)) for scene, snr in heldout["cells"]["boundary"]}
    all_cells = target | boundary
    rows = heldout["raw_rows"]

    wr_adp_clusters = _paired_by_seed(rows, "weakretune", "adapter_pilot", target)
    crank_wr_clusters = _paired_by_seed(rows, "cand_rank", "weakretune", target)
    primary_clusters = _paired_by_seed(rows, "cand_rank", "adapter_pilot", target)

    analysis = heldout["analysis"]
    branch_occupancy_change = []
    grouped = defaultdict(dict)
    for row in rows:
        if float(row["delta_db"]) == 0.0 and (row["scene"], float(row["gamma_true_db"])) in all_cells:
            grouped[(row["scene"], float(row["gamma_true_db"]), int(row["seed_index"]))][row["method"]] = row
    for key, methods in sorted(grouped.items()):
        if {"cand_rank", "weakretune"} <= methods.keys():
            branch_occupancy_change.append(
                int(methods["weakretune"]["n_select_da"]) - int(methods["cand_rank"]["n_select_da"])
            )

    boundary_weakretune_vs_adapter = []
    for cell in sorted(boundary):
        clusters = _paired_by_seed(rows, "weakretune", "adapter_pilot", {cell})
        boundary_weakretune_vs_adapter.append(
            {"scene": cell[0], "snr_db": cell[1], **summarize(clusters.values())}
        )

    return {
        "source_hashes": {
            str(dev_path.relative_to(repo_root)).replace("\\", "/"): _sha256(dev_path),
            str(heldout_path.relative_to(repo_root)).replace("\\", "/"): _sha256(heldout_path),
        },
        "chronology": {
            "dev_seeds": dev["dev_seeds"],
            "heldout_seeds": heldout["heldout_seeds"],
            "disjoint": set(dev["dev_seeds"]).isdisjoint(heldout["heldout_seeds"]),
            "historical_order": "P01 dev 0-9 -> P01 heldout 30-49 -> P02 dev 50-59 -> P02 heldout 60-99 excluding 71-80",
            "pristine_30_seed_heldout": False,
            "qualification": "the first held-out set contained 20 seeds; seeds 90-99 were appended after observing that result under the disclosed deterministic seed-count repair",
        },
        "cand_rank_minus_adapter": {
            **summarize(primary_clusters.values()),
            "reported_cell_seed_pair": _row_pair_summary(analysis["primary_cand_rank_minus_adapter"]),
        },
        "weakretune_minus_adapter": {
            **summarize(wr_adp_clusters.values()),
            "reported_cell_seed_pair": _row_pair_summary(analysis["cheap_alt_weakretune_minus_adapter"]),
        },
        "cand_rank_minus_weakretune": {
            **summarize(crank_wr_clusters.values()),
            "reported_cell_seed_pair": _row_pair_summary(analysis["cheap_alt_cand_rank_minus_weakretune"]),
        },
        "boundary_cells": analysis["boundary_cand_rank_minus_adapter"],
        "boundary_weakretune_minus_adapter_cluster_ci": boundary_weakretune_vs_adapter,
        "boundary_any_catastrophic": bool(analysis["boundary_any_catastrophic"]),
        "branch_occupancy_effect": {
            "comparison": "weakretune_vs_cand_rank",
            "cell_seed_clusters": len(branch_occupancy_change),
            "nonzero_occupancy_count": sum(delta != 0 for delta in branch_occupancy_change),
            "exact_per_window_command_identity_available": False,
            "note": "aggregate rows contain DA/NDA counts, not per-window command traces; nonzero occupancy proves count change but not exact command mismatch rate",
        },
        "deployable_region_identity": _p02_source_identity(repo_root, float(dev["chosen_ref_snr_db"])),
    }


def _map_apply(value: float, edges: list[float], offsets: list[float]) -> float:
    region = 0 if value < edges[0] else 1 if value < edges[1] else 2
    return float(value) + float(offsets[region])


def _ccisp_command(event: dict, calibrated_snr_db: float) -> str:
    cv_boundary = 0.74 + 0.12 * math.exp(-float(calibrated_snr_db) / 5.0)
    if float(event["raw_cv"]) < cv_boundary * 1.10:
        return "nda"
    gamma_lin = 10.0 ** (float(calibrated_snr_db) / 10.0)
    channel_power = max(float(event["raw_mean_power"]) - 1.0 / (2.0 * gamma_lin), 1e-6)
    return "da" if calibrated_snr_db + 10.0 * math.log10(channel_power) < 13.0 else "nda"


def _t004_row_gain(row: dict, method: str, tuning: dict) -> float:
    errors = {"B0": 0, method: 0}
    for event in row["windows"]:
        b0_command = _ccisp_command(event, float(row["nominal_snr_db"]))
        errors["B0"] += int(event[b0_command])
        if method == "B1":
            calibrated = float(row["nominal_snr_db"]) + float(tuning["B1"]["offset"])
        elif method == "B2":
            calibrated = _map_apply(
                float(row["nominal_snr_db"]), tuning["B2"]["edges"], tuning["B2"]["offsets"]
            )
        elif method == "M":
            calibrated = _map_apply(
                float(event["estimate_db"]), tuning["M"]["edges"], tuning["M"]["offsets"]
            )
        else:
            raise ValueError(method)
        command = _ccisp_command(event, calibrated)
        errors[method] += int(event[command])
    return 10.0 * math.log10(max(errors["B0"], 1) / max(errors[method], 1))


def _t004_report(repo_root: Path) -> tuple[dict, list[dict]]:
    dev = _git_json(repo_root, T004_COMMIT, T004_DEV_PATH)
    frozen = _git_json(repo_root, T004_COMMIT, T004_FROZEN_PATH)
    primary = {(scene, float(snr), float(delta)) for scene, snr, delta in frozen["primary"]}
    primary_rows = [
        row
        for row in dev["raw"]
        if (row["scene"], float(row["true_snr_db"]), float(row["delta_db"])) in primary
    ]
    tuning = frozen["tuning"]
    table: dict[str, dict] = {
        "original_B0": {
            "evidence_stage": "dev_only",
            "mean_db": 0.0,
            "ci95": [0.0, 0.0],
            "n_clusters": len(frozen["seed_ledger"]["dev"]),
            "action": "nominal receiver configuration",
        }
    }
    rows_for_csv = []
    for label, method in (("global_B1", "B1"), ("region_B2", "B2"), ("online_M", "M")):
        by_seed = defaultdict(list)
        for row in primary_rows:
            by_seed[int(row["seed"])].append(_t004_row_gain(row, method, tuning))
        summary = summarize(mean(values) for values in by_seed.values())
        summary["evidence_stage"] = "dev_only"
        summary["frozen_score_mean_over_cell_seed_rows_db"] = float(tuning[method]["score_db"])
        summary["action"] = {
            "B1": "one global +3 dB offset",
            "B2": "nominal-SNR regions [<7, 7-11, >=11] -> [+3,-3,-3] dB",
            "M": "current-pilot-estimate regions [<7, 7-11, >=11] -> [+3,+3,-3] dB",
        }[method]
        table[label] = summary
        rows_for_csv.append({"method": label, **summary})

    return (
        {
            "commit": T004_COMMIT,
            "dev_table": table,
            "online_minus_region_dev_db": table["online_M"]["mean_db"] - table["region_B2"]["mean_db"],
            "frozen_online_minus_region_score_db": float(tuning["M"]["score_db"])
            - float(tuning["B2"]["score_db"]),
            "heldout_paths": {path: _git_path_exists(repo_root, T004_COMMIT, path) for path in T004_HELDOUT_PATHS},
            "heldout_exists": any(_git_path_exists(repo_root, T004_COMMIT, path) for path in T004_HELDOUT_PATHS),
            "pretest_gate": "REJECT after the single allowed deterministic repair; no legal held-out result",
            "truth_boundary": "new dev caller was truth-isolated; historical P01/P02 BER path retained as diagnostic because branch preprocessing used true SNR",
        },
        rows_for_csv,
    )


def build_report(repo_root: Path) -> dict:
    repo_root = Path(repo_root).resolve()
    p01, harm_rows = _p01_report(repo_root)
    p02 = _p02_report(repo_root)
    t004, table_rows = _t004_report(repo_root)

    gate = {
        "deployment_region_input_known_or_visible": {
            "pass": False,
            "reason": "P02 decide has no region input; weak@5/7/9 is an evaluation slice selected with scene/true-SNR labels",
        },
        "truth_absent_from_decide": {
            "pass": True,
            "reason": "P02 decide uses raw samples, known pilots and one frozen scalar; true SNR is not passed into decide",
        },
        "reusable_region_rule_not_scalar": {
            "pass": False,
            "reason": "the implemented P02 action is one global dev-frozen ref_snr_db=11 scalar",
        },
        "at_least_two_regions_distinct_legal_actions": {
            "pass": False,
            "reason": "P02 has one calibration action and no runtime region selector",
        },
        "original_and_global_comparators": {
            "pass": False,
            "reason": "P02 compared original/adapter/cand_rank/weakretune but did not freeze a separate global-vs-region calibration ladder",
        },
        "complete_method_packaging_chain": {
            "pass": False,
            "reason": "a one-scalar retune cannot support the required region-rule ablation or load-bearing region-information figure",
        },
    }
    gate["all_pass"] = all(item["pass"] for item in gate.values())

    report = {
        "schema": "2a.region-calibration-authority-reconciliation.v1",
        "execution_type": "deterministic_recompute_only_no_simulation",
        "p01": p01,
        "p02": p02,
        "t004": t004,
        "semantic_gate": gate,
        "bounded_confirmation_run": False,
        "bounded_confirmation_reason": "semantic gate failed before sim-preflight: P02 is a truth-defined target slice plus one global scalar retune, not a deployable multi-region rule",
        "authority_reconciliation": {
            "P01": "receiver-visible local robustness adapter; separate from P02 and T004",
            "P02": "conventional one-scalar design/tuning rule; supporting evidence only, not a region-calibrated method",
            "T004": "online three-region calibration package remains REJECT at immutable pre-test gate; no held-out scientific null or positive",
        },
        "claim_ceiling": "P01 establishes a local receiver-visible robustness adapter and P02 establishes that ref=11 conventional retuning absorbs cand_rank on the frozen weak/low-SNR evaluation slice; no region-calibrated CCISP method extension is established",
        "terminal": "SUPPORTING_ONLY",
        "_csv_payload": {"p01_harm_rows": harm_rows, "t004_table_rows": table_rows},
    }
    return report


def _write_outputs(report: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_payload = report.pop("_csv_payload")
    (output_dir / "recomputed-evidence.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    with (output_dir / "p01-harm-cells.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "scene",
                "snr_db",
                "delta_db",
                "dev_mismatch_mean_db",
                "dev_mismatch_ci_low",
                "dev_mismatch_ci_high",
                "adapter_vs_d0_mean_db",
                "adapter_vs_d0_ci_low",
                "adapter_vs_d0_ci_high",
                "resolved",
            ]
        )
        for row in csv_payload["p01_harm_rows"]:
            mismatch = row["dev_mismatch_drop"]
            residual = row["heldout_adapter_vs_d0"]
            writer.writerow(
                [
                    row["scene"],
                    row["snr_db"],
                    row["delta_db"],
                    mismatch["mean_db"],
                    *mismatch["ci95"],
                    residual["mean_db"],
                    *residual["ci95"],
                    row["strict_harm_resolved"],
                ]
            )

    with (output_dir / "original-global-region-table.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.writer(handle)
        writer.writerow(["method", "evidence_stage", "mean_db", "ci95_low", "ci95_high", "n_seed_clusters", "action"])
        writer.writerow(["original_B0", "dev_only", 0.0, 0.0, 0.0, 6, "nominal receiver configuration"])
        for row in csv_payload["t004_table_rows"]:
            writer.writerow(
                [
                    row["method"],
                    row["evidence_stage"],
                    row["mean_db"],
                    *row["ci95"],
                    row["n_clusters"],
                    row["action"],
                ]
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[4])
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    report = build_report(args.repo_root)
    _write_outputs(report, args.output_dir)
    print(json.dumps({"terminal": report["terminal"], "semantic_gate": report["semantic_gate"]["all_pass"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
