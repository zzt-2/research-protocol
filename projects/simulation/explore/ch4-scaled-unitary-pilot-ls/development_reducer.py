"""Raw-only validation, aggregation, bootstrap CI, and terminal for T069."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path

import numpy as np


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def select_tuned_parameter(
    rows: Iterable[Mapping[str, float | int]], grid: Sequence[float]
) -> float:
    """Minimize tune-only pooled BER; exact ties prefer stronger regularization."""
    totals = {float(value): [0, 0] for value in grid}
    for row in rows:
        parameter = float(row["parameter"])
        if parameter not in totals:
            raise ValueError("unregistered tuning parameter")
        totals[parameter][0] += int(row["bit_errors"])
        totals[parameter][1] += int(row["payload_bits"])
    if any(bits <= 0 for _, bits in totals.values()):
        raise ValueError("every registered parameter needs tune payload bits")
    rates = {value: errors / bits for value, (errors, bits) in totals.items()}
    best = min(rates.values())
    return max(value for value, rate in rates.items() if rate == best)


def paired_bootstrap(
    candidate: Sequence[float],
    baseline: Sequence[float],
    *,
    seed: int,
    resamples: int,
) -> dict[str, float | int]:
    """Candidate-minus-baseline paired window bootstrap with a reset PCG64 stream."""
    candidate_array = np.asarray(candidate, dtype=np.float64)
    baseline_array = np.asarray(baseline, dtype=np.float64)
    if (
        candidate_array.ndim != 1
        or candidate_array.shape != baseline_array.shape
        or candidate_array.size == 0
        or not np.all(np.isfinite(candidate_array))
        or not np.all(np.isfinite(baseline_array))
    ):
        raise ValueError("paired finite one-dimensional window BER arrays required")
    difference = candidate_array - baseline_array
    rng = np.random.Generator(np.random.PCG64(int(seed)))
    indices = rng.integers(
        0, difference.size, size=(int(resamples), difference.size), dtype=np.int64
    )
    boot = difference[indices].mean(axis=1)
    lower, upper = np.quantile(boot, [0.025, 0.975])
    return {
        "mean_diff": float(difference.mean()),
        "ci_lower": float(lower),
        "ci_upper": float(upper),
        "clusters": int(difference.size),
        "candidate_window_wins": int(np.count_nonzero(difference < 0.0)),
    }


def _row_key(row: Mapping) -> tuple[str, float | None]:
    parameter = row["parameter"]
    return str(row["arm"]), None if parameter is None else float(parameter)


def _expected_keys(manifest: Mapping, split: str, tuned: Mapping[str, float]):
    if split == "tune":
        return {
            ("B0", None),
            *(("B1", float(value)) for value in manifest["arms"]["B1"]["eta_grid"]),
            *(("B2", float(value)) for value in manifest["arms"]["B2"]["tau_grid"]),
            ("C4", None),
            ("O1", None),
        }
    return {
        ("B0", None),
        ("B1", float(tuned["B1"])),
        ("B2", float(tuned["B2"])),
        ("C4", None),
        ("O1", None),
    }


def _validate_row(row: Mapping, payload_bits: int) -> None:
    numeric = (
        row["ber"],
        row["channel_nmse"],
        row["inverse_residual"],
        row["rho"],
        row["runtime_ns"],
    )
    if not all(np.isfinite(float(value)) for value in numeric):
        raise ValueError("nonfinite raw metric")
    errors = int(row["bit_errors"])
    bits = int(row["payload_bits"])
    if bits != payload_bits or not 0 <= errors <= bits:
        raise ValueError("payload BER numerator/denominator mismatch")
    if float(row["ber"]) != errors / bits:
        raise ValueError("raw BER is not reproducible from counts")
    if float(row["runtime_ns"]) < 0.0:
        raise ValueError("negative runtime")


def validate_raw(raw: Mapping, manifest: Mapping, manifest_sha256: str) -> None:
    """Fail closed on manifest, population, split, pairing, grid, and finiteness."""
    if raw.get("schema_version") != "t069.scaled-unitary-raw.v1":
        raise ValueError("raw schema mismatch")
    if raw.get("manifest_sha256") != manifest_sha256:
        raise ValueError("raw/manifest hash mismatch")
    correctness = raw.get("correctness", {})
    if not correctness.get("all_pass") or correctness.get("terminal") != "CORRECTNESS_PASS":
        raise ValueError("BER raw lacks a passing C0-C5 prerequisite")
    raw_cells = raw.get("cells", [])
    if len(raw_cells) != len(manifest["cells"]):
        raise ValueError("cell count mismatch")
    payload_bits = 2 * 4 * int(manifest["signal_model"]["payload_symbols_per_polarization"])
    window_count = int(manifest["population"]["windows_per_cell"])
    tune_start, tune_stop = (int(value) for value in manifest["population"]["tune_offsets"])
    eval_start, eval_stop = (
        int(value) for value in manifest["population"]["evaluation_offsets"]
    )
    if (
        tune_start != 0
        or tune_stop + 1 != eval_start
        or eval_stop + 1 != window_count
    ):
        raise ValueError("manifest tune/evaluation split is not exhaustive and disjoint")

    for raw_cell, cell in zip(raw_cells, manifest["cells"]):
        for key in ("cell_id", "snr_db", "pilot_symbols_per_polarization", "seed_base"):
            if raw_cell[key] != cell[key]:
                raise ValueError(f"cell authority mismatch: {key}")
        windows = raw_cell.get("windows", [])
        if len(windows) != window_count:
            raise ValueError("window count mismatch")
        realization_hashes: set[str] = set()
        observation_hashes: set[str] = set()
        tune_rows = {"B1": [], "B2": []}
        for expected_id, window in enumerate(windows):
            if int(window["window_id"]) != expected_id:
                raise ValueError("window id/order mismatch")
            if int(window["seed"]) != int(cell["seed_base"]) + expected_id:
                raise ValueError("window seed mismatch")
            expected_split = "tune" if expected_id <= tune_stop else "evaluation"
            if window["split"] != expected_split:
                raise ValueError("window split mismatch")
            realization_hashes.add(str(window["realization_hash"]))
            observation_hashes.add(str(window["observation_hash"]))
            keys = [_row_key(row) for row in window["rows"]]
            if len(keys) != len(set(keys)):
                raise ValueError("duplicate arm/parameter row")
            for row in window["rows"]:
                _validate_row(row, payload_bits)
                if expected_split == "tune" and row["arm"] in tune_rows:
                    tune_rows[str(row["arm"])].append(row)
        if len(realization_hashes) != window_count or len(observation_hashes) != window_count:
            raise ValueError("window realization/observation hashes must be unique")
        selected = {
            "B1": select_tuned_parameter(tune_rows["B1"], manifest["arms"]["B1"]["eta_grid"]),
            "B2": select_tuned_parameter(tune_rows["B2"], manifest["arms"]["B2"]["tau_grid"]),
        }
        if {key: float(value) for key, value in raw_cell["tuned_parameters"].items()} != selected:
            raise ValueError("runner tuning does not reproduce from raw tune rows")
        for window in windows:
            expected = _expected_keys(manifest, window["split"], selected)
            if set(_row_key(row) for row in window["rows"]) != expected:
                raise ValueError("arm/parameter grid mismatch")


def _arm_rows(windows: Sequence[Mapping], arm: str) -> list[Mapping]:
    rows = []
    for window in windows:
        matches = [row for row in window["rows"] if row["arm"] == arm]
        if len(matches) != 1:
            raise ValueError(f"expected one evaluation row for {arm}")
        rows.append(matches[0])
    return rows


def _arm_summary(rows: Sequence[Mapping], oracle_ber: float) -> dict[str, float | int]:
    errors = sum(int(row["bit_errors"]) for row in rows)
    bits = sum(int(row["payload_bits"]) for row in rows)
    ber = float(errors / bits)
    return {
        "bit_errors": errors,
        "payload_bits": bits,
        "ber": ber,
        "channel_nmse": float(np.mean([row["channel_nmse"] for row in rows])),
        "inverse_residual": float(np.mean([row["inverse_residual"] for row in rows])),
        "rho": float(np.mean([row["rho"] for row in rows])),
        "runtime_ms": float(sum(float(row["runtime_ns"]) for row in rows) / 1.0e6),
        "oracle_headroom": float(ber - oracle_ber),
    }


def _comparison(
    candidate_rows: Sequence[Mapping], baseline_rows: Sequence[Mapping], manifest: Mapping
) -> dict[str, float | int]:
    bootstrap = manifest["bootstrap"]
    return paired_bootstrap(
        [float(row["ber"]) for row in candidate_rows],
        [float(row["ber"]) for row in baseline_rows],
        seed=int(bootstrap["seed"]),
        resamples=int(bootstrap["resamples"]),
    )


def _signal_gate(cells: Sequence[Mapping], comparison_name: str) -> bool:
    np2 = [cell for cell in cells if cell["pilot_symbols_per_polarization"] == 2]
    np4 = [cell for cell in cells if cell["pilot_symbols_per_polarization"] == 4]
    if len(np2) != 2 or len(np4) != 2:
        raise ValueError("terminal requires exactly two Np=2 and two Np=4 cells")
    improvement = any(cell["comparisons"][comparison_name]["ci_upper"] < 0.0 for cell in np2)
    np2_nonregression = all(
        cell["comparisons"][comparison_name]["ci_lower"] <= 0.0 for cell in np2
    )
    np4_nonregression = all(
        cell["comparisons"][comparison_name]["ci_lower"] <= 0.0 for cell in np4
    )
    return improvement and np2_nonregression and np4_nonregression


def classify_terminal(cells: Sequence[Mapping], manifest: Mapping) -> dict[str, str | None]:
    """Apply only the preregistered T069 terminal ladder."""
    strongest_deployable_errors = 0
    oracle_errors = 0
    for cell in cells:
        summaries = cell["arms"]
        deployable = min(("B0", "B1", "B2", "C4"), key=lambda arm: (summaries[arm]["ber"], arm))
        strongest_deployable_errors += int(summaries[deployable]["bit_errors"])
        oracle_errors += int(summaries["O1"]["bit_errors"])
    if strongest_deployable_errors <= oracle_errors:
        terminal = "NO_METHOD_SIGNAL"
        winner = None
    elif _signal_gate(cells, "C4_vs_strongest"):
        terminal = "C4_STRUCTURED_SIGNAL"
        winner = "C4"
    else:
        total_errors = {
            arm: sum(int(cell["arms"][arm]["bit_errors"]) for cell in cells)
            for arm in ("B1", "B2")
        }
        simple_winner = "B1" if total_errors["B1"] <= total_errors["B2"] else "B2"
        if _signal_gate(cells, f"{simple_winner}_vs_B0"):
            terminal = "SIMPLE_ROBUST_LS_SIGNAL"
            winner = simple_winner
        else:
            relevant = ("C4_vs_strongest", "B1_vs_B0", "B2_vs_B0")
            np2_negative = any(
                cell["comparisons"][name]["mean_diff"] < 0.0
                for cell in cells
                if cell["pilot_symbols_per_polarization"] == 2
                for name in relevant
            )
            np4_regression = any(
                cell["comparisons"][name]["ci_lower"] > 0.0
                for cell in cells
                if cell["pilot_symbols_per_polarization"] == 4
                for name in relevant
            )
            terminal = "LOCAL_ONLY" if np2_negative or np4_regression else "NO_METHOD_SIGNAL"
            winner = None
    return {
        "terminal": terminal,
        "grade": manifest["terminal_rules"]["grade_map"][terminal],
        "winner": winner,
        "only_next_step": manifest["terminal_rules"]["only_next_step"][terminal],
    }


def reduce_raw(raw: Mapping, manifest: Mapping, manifest_sha256: str) -> dict:
    """Rebuild every aggregate and the terminal from raw window rows only."""
    validate_raw(raw, manifest, manifest_sha256)
    aggregate_cells = []
    for raw_cell in raw["cells"]:
        evaluation = [window for window in raw_cell["windows"] if window["split"] == "evaluation"]
        rows_by_arm = {arm: _arm_rows(evaluation, arm) for arm in ("B0", "B1", "B2", "C4", "O1")}
        oracle_errors = sum(int(row["bit_errors"]) for row in rows_by_arm["O1"])
        oracle_bits = sum(int(row["payload_bits"]) for row in rows_by_arm["O1"])
        oracle_ber = oracle_errors / oracle_bits
        summaries = {
            arm: _arm_summary(rows, oracle_ber) for arm, rows in rows_by_arm.items()
        }
        strongest = "B1" if summaries["B1"]["ber"] <= summaries["B2"]["ber"] else "B2"
        comparisons = {
            "C4_vs_B0": _comparison(rows_by_arm["C4"], rows_by_arm["B0"], manifest),
            "C4_vs_B1": _comparison(rows_by_arm["C4"], rows_by_arm["B1"], manifest),
            "C4_vs_B2": _comparison(rows_by_arm["C4"], rows_by_arm["B2"], manifest),
            "B1_vs_B0": _comparison(rows_by_arm["B1"], rows_by_arm["B0"], manifest),
            "B2_vs_B0": _comparison(rows_by_arm["B2"], rows_by_arm["B0"], manifest),
        }
        comparisons["C4_vs_strongest"] = dict(comparisons[f"C4_vs_{strongest}"])
        comparisons["C4_vs_strongest"]["baseline"] = strongest
        aggregate_cells.append(
            {
                "cell_id": raw_cell["cell_id"],
                "snr_db": raw_cell["snr_db"],
                "pilot_symbols_per_polarization": raw_cell["pilot_symbols_per_polarization"],
                "evaluation_windows": len(evaluation),
                "tuned_parameters": raw_cell["tuned_parameters"],
                "strongest_B1_B2": strongest,
                "arms": summaries,
                "comparisons": comparisons,
            }
        )
    decision = classify_terminal(aggregate_cells, manifest)
    return {
        "schema_version": "t069.scaled-unitary-aggregate.v1",
        "authority": raw["authority"],
        "manifest_sha256": manifest_sha256,
        "raw_schema_version": raw["schema_version"],
        "cells": aggregate_cells,
        "decision": decision,
    }


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
