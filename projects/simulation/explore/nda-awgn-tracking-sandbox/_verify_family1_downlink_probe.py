"""Independent verifier for the T017 Family-1 downlink diagnostic.

All decisions are recomputed from case-seed records in the probe JSON.  The
runner's ``cells`` summaries are checked but never used as verification input.
"""
from __future__ import annotations

import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PROBE = HERE / "_family1_downlink_probe.json"
REPORT = HERE / "_verify_family1_downlink_probe_report.json"

SCENES = ("weak", "moderate", "strong")
SNRS = (5.0, 13.0, 17.0, 19.0, 25.0)
SEED_INDICES = (0, 1, 2)
PARAM_SETS = ("old", "new_family1")
WINDOWS = 400
BITS_PER_WINDOW = 768
EXPECTED_CASES = 45
COUNT_FIELDS = (
    "fixed_nda_errors", "fixed_da_errors", "selected_errors", "oracle_errors",
    "n_select_da", "n_select_nda", "n_bits",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def key(row: dict[str, Any]) -> tuple[str, float, int]:
    return row["scene"], float(row["snr_db"]), int(row["seed_index"])


def cell_key(row: dict[str, Any]) -> tuple[str, float]:
    return row["scene"], float(row["snr_db"])


def expected_keys() -> set[tuple[str, float, int]]:
    return {(scene, snr, seed) for scene in SCENES for snr in SNRS for seed in SEED_INDICES}


def gain_db(fixed_nda: int, selected: int) -> float:
    if selected == 0:
        return math.inf if fixed_nda > 0 else 0.0
    if fixed_nda == 0:
        return -math.inf
    return 10.0 * math.log10(fixed_nda / selected)


def close(a: Any, b: Any, tol: float = 1e-12) -> bool:
    if isinstance(a, (int, str)) or isinstance(b, (int, str)):
        return a == b
    return finite_number(a) and finite_number(b) and math.isclose(a, b, rel_tol=tol, abs_tol=tol)


def aggregate(rows: list[dict[str, Any]]) -> dict[tuple[str, float], dict[str, Any]]:
    grouped: dict[tuple[str, float], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[cell_key(row)].append(row)
    output: dict[tuple[str, float], dict[str, Any]] = {}
    for ck, members in grouped.items():
        sums = {field: sum(int(row[field]) for row in members) for field in COUNT_FIELDS}
        n_bits = sums["n_bits"]
        fixed_nda = sums["fixed_nda_errors"]
        fixed_da = sums["fixed_da_errors"]
        selected = sums["selected_errors"]
        oracle = sums["oracle_errors"]
        output[ck] = {
            **sums,
            "fixed_nda_ber": fixed_nda / n_bits,
            "fixed_da_ber": fixed_da / n_bits,
            "selected_ber": selected / n_bits,
            "oracle_ber": oracle / n_bits,
            "selected_vs_fixed_nda_gain_db": gain_db(fixed_nda, selected),
            "fixed_winner": "da" if fixed_da < fixed_nda else "nda" if fixed_nda < fixed_da else "tie",
        }
    return output


def main() -> None:
    failures: list[str] = []
    data = json.loads(PROBE.read_text(encoding="utf-8"))

    required_top = {"authority_status", "contract", "parameters", "grid", "cases", "cells", "provenance", "_meta"}
    missing_top = sorted(required_top - set(data))
    if missing_top:
        failures.append(f"missing top-level fields: {missing_top}")
    if data.get("authority_status") != "diagnostic_probe_not_for_paper":
        failures.append("authority_status is not diagnostic_probe_not_for_paper")

    grid = data.get("grid", {})
    grid_ok = (
        tuple(grid.get("scenes", ())) == SCENES
        and tuple(float(x) for x in grid.get("snr_db", ())) == SNRS
        and tuple(grid.get("seed_indices", ())) == SEED_INDICES
        and grid.get("windows_per_case_seed") == WINDOWS
        and grid.get("common_bits_per_window") == BITS_PER_WINDOW
    )
    if not grid_ok:
        failures.append("grid does not match frozen T017 grid")

    params = data.get("parameters", {})
    parameter_checks: dict[str, Any] = {}
    for param_set in PARAM_SETS:
        scene_params = params.get(param_set, {})
        valid = set(scene_params) == set(SCENES)
        for scene in SCENES:
            pair = scene_params.get(scene)
            valid = valid and isinstance(pair, list) and len(pair) == 2 and all(finite_number(x) and x > 0 for x in pair)
        parameter_checks[param_set] = valid
        if not valid:
            failures.append(f"invalid/nonpositive/nonfinite parameters: {param_set}")

    expected = expected_keys()
    cases = data.get("cases", {})
    case_checks: dict[str, Any] = {}
    indexed: dict[str, dict[tuple[str, float, int], dict[str, Any]]] = {}
    all_case_values_valid = True
    seed_identity_ok = True
    for param_set in PARAM_SETS:
        rows = cases.get(param_set, [])
        keys = [key(row) for row in rows]
        unique_keys = set(keys)
        complete = len(rows) == EXPECTED_CASES and len(unique_keys) == EXPECTED_CASES and unique_keys == expected
        indexed[param_set] = {key(row): row for row in rows}
        local_value_ok = True
        local_seed_ok = True
        for row in rows:
            start = 2000 + int(row["seed_index"]) * WINDOWS
            seeds = row.get("window_seeds", [])
            expected_seeds = list(range(start, start + WINDOWS))
            local_seed_ok = local_seed_ok and (
                row.get("window_seed_start") == start
                and row.get("window_seed_end_inclusive") == start + WINDOWS - 1
                and row.get("n_windows") == WINDOWS
                and seeds == expected_seeds
                and len(set(seeds)) == WINDOWS
            )
            local_value_ok = local_value_ok and row.get("n_bits") == WINDOWS * BITS_PER_WINDOW
            local_value_ok = local_value_ok and all(
                isinstance(row.get(field), int) and not isinstance(row.get(field), bool) and row[field] >= 0
                for field in COUNT_FIELDS
            )
            local_value_ok = local_value_ok and row.get("n_select_da", -1) + row.get("n_select_nda", -1) == WINDOWS
            local_value_ok = local_value_ok and all(
                finite_number(row.get(field)) and 0 <= row[field] <= 1
                for field in ("fixed_nda_ber", "fixed_da_ber", "selected_ber", "oracle_ber")
            )
            local_value_ok = local_value_ok and all(
                math.isclose(row[f"{name}_ber"], row[f"{name}_errors"] / row["n_bits"], rel_tol=1e-12, abs_tol=1e-12)
                for name in ("fixed_nda", "fixed_da", "selected", "oracle")
            )
            local_value_ok = local_value_ok and all(
                row[field] <= row["n_bits"]
                for field in ("fixed_nda_errors", "fixed_da_errors", "selected_errors", "oracle_errors")
            )
            local_value_ok = local_value_ok and isinstance(row.get("realization_identity_sha256"), str) and len(row["realization_identity_sha256"]) == 64
        all_case_values_valid = all_case_values_valid and local_value_ok
        seed_identity_ok = seed_identity_ok and local_seed_ok
        case_checks[param_set] = {
            "count": len(rows), "unique_case_identities": len(unique_keys),
            "complete_expected_grid": complete, "values_valid": local_value_ok,
            "seed_formula_and_uniqueness": local_seed_ok,
        }
        if not complete:
            failures.append(f"{param_set} does not contain exactly the expected 45 identities")
        if not local_value_ok:
            failures.append(f"{param_set} contains invalid counts/BER/hash/denominator")
        if not local_seed_ok:
            failures.append(f"{param_set} contains invalid or duplicate window seeds")

    matched_old_new_seed_protocol = True
    if all(param_set in indexed for param_set in PARAM_SETS):
        for identity in expected:
            if identity not in indexed["old"] or identity not in indexed["new_family1"]:
                matched_old_new_seed_protocol = False
                continue
            old = indexed["old"][identity]
            new = indexed["new_family1"][identity]
            matched_old_new_seed_protocol = matched_old_new_seed_protocol and all(
                old.get(field) == new.get(field)
                for field in ("window_seed_start", "window_seed_end_inclusive", "window_seeds", "n_windows", "n_bits")
            )
    if not matched_old_new_seed_protocol:
        failures.append("old/new seed protocol or common denominator differs")

    ab_details: list[dict[str, Any]] = []
    ab_matched = 0
    for identity in sorted(expected):
        row = indexed.get("new_family1", {}).get(identity)
        route_b = row.get("route_b") if row else None
        fields = (
            "selected_errors", "n_select_da", "n_select_nda", "n_windows", "n_bits",
            "window_seed_start", "window_seed_end_inclusive", "realization_identity_sha256",
        )
        mismatches = [field for field in fields if not route_b or row.get(field) != route_b.get(field)]
        if route_b and not close(row.get("selected_ber"), route_b.get("selected_ber")):
            mismatches.append("selected_ber")
        matched = not mismatches
        ab_matched += int(matched)
        ab_details.append({"scene": identity[0], "snr_db": identity[1], "seed_index": identity[2], "matched": matched, "mismatches": mismatches})
    if ab_matched != EXPECTED_CASES:
        failures.append(f"A/B matched {ab_matched}/{EXPECTED_CASES}, expected 45/45")

    recomputed = {param_set: aggregate(cases.get(param_set, [])) for param_set in PARAM_SETS}
    saved_cells = {(row["scene"], float(row["snr_db"])): row for row in data.get("cells", [])}
    summary_mismatches: list[str] = []
    cell_matrix: list[dict[str, Any]] = []
    summary_fields = COUNT_FIELDS + (
        "fixed_nda_ber", "fixed_da_ber", "selected_ber", "oracle_ber",
        "selected_vs_fixed_nda_gain_db", "fixed_winner",
    )
    for ck in [(scene, snr) for scene in SCENES for snr in SNRS]:
        cell_out: dict[str, Any] = {"scene": ck[0], "snr_db": ck[1]}
        saved = saved_cells.get(ck)
        if saved is None:
            summary_mismatches.append(f"missing saved cell {ck}")
        for param_set in PARAM_SETS:
            metrics = recomputed[param_set].get(ck)
            cell_out[param_set] = metrics
            if metrics is None:
                summary_mismatches.append(f"missing recomputed cell {param_set} {ck}")
                continue
            saved_metrics = saved.get(param_set) if saved else None
            if not saved_metrics:
                summary_mismatches.append(f"missing saved summary {param_set} {ck}")
            else:
                bad = [field for field in summary_fields if not close(metrics[field], saved_metrics.get(field))]
                if bad:
                    summary_mismatches.append(f"summary mismatch {param_set} {ck}: {bad}")
        if cell_out.get("old") and cell_out.get("new_family1"):
            cell_out["new_minus_old_selected_errors"] = cell_out["new_family1"]["selected_errors"] - cell_out["old"]["selected_errors"]
            cell_out["fixed_winner_changed"] = cell_out["old"]["fixed_winner"] != cell_out["new_family1"]["fixed_winner"]
        cell_matrix.append(cell_out)
    if len(saved_cells) != 15:
        summary_mismatches.append(f"saved cells count is {len(saved_cells)}, expected 15")
    if summary_mismatches:
        failures.append("runner cell summaries do not match independent aggregation")

    new_cells = recomputed["new_family1"]
    both_branches_selected = (
        sum(v["n_select_da"] for v in new_cells.values()) > 0
        and sum(v["n_select_nda"] for v in new_cells.values()) > 0
    )
    winner_change_count = sum(
        recomputed["old"][ck]["fixed_winner"] != new_cells[ck]["fixed_winner"] for ck in new_cells
    )
    positive_gain_count = sum(v["selected_vs_fixed_nda_gain_db"] > 0 for v in new_cells.values())
    all_cells_same_branch_99 = any(
        all(v[f"n_select_{branch}"] / (3 * WINDOWS) >= 0.99 for v in new_cells.values())
        for branch in ("da", "nda")
    )

    gg_scintillation = {
        scene: 1 / params["new_family1"][scene][0] + 1 / params["new_family1"][scene][1]
        + 1 / (params["new_family1"][scene][0] * params["new_family1"][scene][1])
        for scene in SCENES
    } if parameter_checks.get("new_family1") else {}
    physical_severity_order_ok = bool(gg_scintillation) and gg_scintillation["weak"] < gg_scintillation["moderate"] < gg_scintillation["strong"]
    performance_severity_order_ok = all(
        new_cells[("strong", snr)]["selected_ber"] >= new_cells[("moderate", snr)]["selected_ber"] >= new_cells[("weak", snr)]["selected_ber"]
        for snr in SNRS
    ) if len(new_cells) == 15 else False
    strong_new_not_worse_than_old = all(
        new_cells[("strong", snr)]["selected_errors"] <= recomputed["old"][("strong", snr)]["selected_errors"]
        for snr in SNRS
    ) if len(new_cells) == 15 and len(recomputed["old"]) == 15 else False
    strong_numeric_direction_ok = physical_severity_order_ok and performance_severity_order_ok and strong_new_not_worse_than_old

    hard_correctness = not failures
    gates = {
        "1_ab_45_of_45_bit_exact": hard_correctness and ab_matched == EXPECTED_CASES,
        "2_both_branches_selected": both_branches_selected,
        "3_fixed_winner_changes": winner_change_count >= 1,
        "4_positive_gain_at_least_8_of_15": positive_gain_count >= 8,
        "5_no_global_99pct_single_branch_collapse": not all_cells_same_branch_99,
        "6_strong_severity_and_numeric_direction": strong_numeric_direction_ok,
    }
    if not hard_correctness:
        final = "BLOCKED"
    elif all(gates.values()):
        final = "DOWNLINK_ONLY_PROMISING"
    else:
        final = "REVISIT_BEFORE_FULL_RUN"

    report = {
        "overall": final,
        "authority_status": data.get("authority_status"),
        "independent_recomputation": True,
        "probe": {"path": str(PROBE), "sha256": sha256(PROBE)},
        "schema_and_integrity": {
            "missing_top_level_fields": missing_top,
            "grid_ok": grid_ok,
            "parameters": parameter_checks,
            "cases": case_checks,
            "all_case_values_valid": all_case_values_valid,
            "seed_formula_and_identity_ok": seed_identity_ok,
            "old_new_seed_protocol_matched": matched_old_new_seed_protocol,
            "saved_cell_summaries_match": not summary_mismatches,
            "summary_mismatches": summary_mismatches,
        },
        "ab_equivalence": {"matched": ab_matched, "expected": EXPECTED_CASES, "status": "PASS" if ab_matched == EXPECTED_CASES else "FAIL", "details": ab_details},
        "screening_inputs": {
            "winner_change_count": winner_change_count,
            "positive_selected_vs_fixed_nda_gain_cells": positive_gain_count,
            "new_total_select_da": sum(v["n_select_da"] for v in new_cells.values()),
            "new_total_select_nda": sum(v["n_select_nda"] for v in new_cells.values()),
            "all_cells_same_branch_at_least_99pct": all_cells_same_branch_99,
            "new_family1_gg_scintillation_index": gg_scintillation,
            "physical_severity_order_ok": physical_severity_order_ok,
            "performance_severity_order_ok": performance_severity_order_ok,
            "strong_new_not_worse_than_old_at_all_snrs": strong_new_not_worse_than_old,
        },
        "screening_gates": {name: "PASS" if passed else "FAIL" for name, passed in gates.items()},
        "hard_correctness_failures": failures,
        "recomputed_cells": cell_matrix,
        "verifier": {"path": str(Path(__file__).resolve()), "sha256": sha256(Path(__file__).resolve())},
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "overall": final, "ab": report["ab_equivalence"],
        "screening_inputs": report["screening_inputs"],
        "screening_gates": report["screening_gates"], "failures": failures,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
