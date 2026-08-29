"""Raw-only validation and frozen terminal reduction for T071."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from pathlib import Path

import numpy as np


SEAM = Path(__file__).resolve().parent


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def paired_bootstrap(
    candidate: Sequence[float], baseline: Sequence[float], *, seed: int, resamples: int
) -> dict[str, float | int]:
    candidate_array = np.asarray(candidate, dtype=np.float64)
    baseline_array = np.asarray(baseline, dtype=np.float64)
    if (
        candidate_array.ndim != 1
        or candidate_array.shape != baseline_array.shape
        or candidate_array.size == 0
        or not np.all(np.isfinite(candidate_array))
        or not np.all(np.isfinite(baseline_array))
    ):
        raise ValueError("paired finite one-dimensional BER arrays required")
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


def _comparison(cell: Mapping) -> Mapping:
    return cell["comparisons"]["C4_vs_B2"]


def classify_terminal(cells: Sequence[Mapping], pooled_np2: Mapping) -> str:
    np2 = [cell for cell in cells if cell["pilot_symbols_per_polarization"] == 2]
    np4 = [cell for cell in cells if cell["pilot_symbols_per_polarization"] == 4]
    if len(np2) != 2 or len(np4) != 2:
        raise ValueError("terminal requires exactly two Np=2 and two Np=4 cells")
    significant_reverse = any(_comparison(cell)["ci_lower"] > 0.0 for cell in cells)
    confirmed = (
        all(_comparison(cell)["mean_diff"] < 0.0 for cell in np2)
        and pooled_np2["ci_upper"] < 0.0
        and any(_comparison(cell)["ci_upper"] < 0.0 for cell in np2)
        and all(_comparison(cell)["ci_lower"] <= 0.0 for cell in np4)
    )
    if confirmed and not significant_reverse:
        return "C4_CONFIRMED_STRUCTURED_SIGNAL"
    local_signal = (
        any(_comparison(cell)["ci_upper"] < 0.0 for cell in np2)
        or pooled_np2["ci_upper"] < 0.0
    )
    if local_signal and not significant_reverse:
        return "C4_CONFIRMATION_LOCAL_ONLY"
    return "C4_NOT_CONFIRMED"


def _expected_rows(cell: Mapping) -> list[tuple[str, float | None]]:
    return [
        ("B0", None),
        ("B1", float(cell["b1_eta"])),
        ("B2", float(cell["b2_tau"])),
        ("C4", None),
        ("O1", None),
    ]


def _row_key(row: Mapping) -> tuple[str, float | None]:
    parameter = row["parameter"]
    return str(row["arm"]), None if parameter is None else float(parameter)


def _validate_row(row: Mapping, payload_bits: int) -> None:
    numeric = (
        row["ber"],
        row["channel_nmse"],
        row["inverse_residual"],
        row["rho"],
        row["runtime_ns"],
    )
    if not all(np.isfinite(float(value)) for value in numeric):
        raise ValueError("nonfinite confirmation metric")
    errors = int(row["bit_errors"])
    bits = int(row["payload_bits"])
    if bits != payload_bits or not 0 <= errors <= bits:
        raise ValueError("payload BER numerator/denominator mismatch")
    if float(row["ber"]) != errors / bits:
        raise ValueError("raw BER is not reproducible from counts")
    if float(row["runtime_ns"]) < 0.0:
        raise ValueError("negative runtime")


def validate_raw(raw: Mapping, manifest: Mapping, manifest_sha256: str) -> None:
    if raw.get("schema_version") != "t071.scaled-unitary-confirmation-raw.v1":
        raise ValueError("confirmation raw schema mismatch")
    if raw.get("manifest_sha256") != manifest_sha256:
        raise ValueError("confirmation raw/manifest hash mismatch")
    if raw.get("frozen_development_hashes") != manifest["frozen_development_hashes"]:
        raise ValueError("frozen development hashes mismatch")
    for name, expected in manifest["frozen_development_hashes"].items():
        if file_sha256(SEAM / name) != expected:
            raise ValueError(f"frozen development artifact changed: {name}")
    development_manifest = load_json(SEAM / "development_manifest.json")
    development_seeds = {
        int(cell["seed_base"]) + offset
        for cell in development_manifest["cells"]
        for offset in range(int(development_manifest["population"]["windows_per_cell"]))
    }
    cells = raw.get("cells", [])
    if len(cells) != len(manifest["cells"]):
        raise ValueError("confirmation cell count mismatch")
    windows_per_cell = int(manifest["population"]["windows_per_cell"])
    payload_bits = 2 * 4 * int(manifest["signal_model"]["payload_symbols_per_polarization"])
    all_seeds: set[int] = set()
    realization_hashes: set[str] = set()
    observation_hashes: set[str] = set()
    for raw_cell, cell in zip(cells, manifest["cells"]):
        for key in (
            "cell_id",
            "snr_db",
            "pilot_symbols_per_polarization",
            "seed_base",
            "b1_eta",
            "b2_tau",
        ):
            if raw_cell[key] != cell[key]:
                raise ValueError(f"confirmation cell authority mismatch: {key}")
        windows = raw_cell.get("windows", [])
        if len(windows) != windows_per_cell:
            raise ValueError("confirmation window count mismatch")
        expected_rows = _expected_rows(cell)
        for window_id, window in enumerate(windows):
            expected_seed = int(cell["seed_base"]) + window_id
            if window["window_id"] != window_id or window["seed"] != expected_seed:
                raise ValueError("confirmation seed arithmetic mismatch")
            if window["split"] != "confirmation":
                raise ValueError("confirmation split mismatch")
            if expected_seed in development_seeds or expected_seed in all_seeds:
                raise ValueError("confirmation/development seed overlap or duplicate")
            all_seeds.add(expected_seed)
            realization_hashes.add(str(window["realization_hash"]))
            observation_hashes.add(str(window["observation_hash"]))
            if [_row_key(row) for row in window["rows"]] != expected_rows:
                raise ValueError("confirmation arm recipe mismatch")
            for row in window["rows"]:
                _validate_row(row, payload_bits)
    expected_population = len(cells) * windows_per_cell
    if len(all_seeds) != expected_population:
        raise ValueError("confirmation seed uniqueness mismatch")
    if len(realization_hashes) != expected_population:
        raise ValueError("confirmation realization hashes are not unique")
    if len(observation_hashes) != expected_population:
        raise ValueError("confirmation observation hashes are not unique")


def _arm_rows(windows: Sequence[Mapping], arm: str) -> list[Mapping]:
    rows = []
    for window in windows:
        matches = [row for row in window["rows"] if row["arm"] == arm]
        if len(matches) != 1:
            raise ValueError(f"expected one confirmation row for {arm}")
        rows.append(matches[0])
    return rows


def _arm_summary(rows: Sequence[Mapping], oracle_ber: float) -> dict[str, float | int]:
    errors = sum(int(row["bit_errors"]) for row in rows)
    bits = sum(int(row["payload_bits"]) for row in rows)
    ber = errors / bits
    return {
        "bit_errors": errors,
        "payload_bits": bits,
        "ber": float(ber),
        "channel_nmse": float(np.mean([row["channel_nmse"] for row in rows])),
        "inverse_residual": float(np.mean([row["inverse_residual"] for row in rows])),
        "rho": float(np.mean([row["rho"] for row in rows])),
        "runtime_ms": float(sum(float(row["runtime_ns"]) for row in rows) / 1.0e6),
        "oracle_headroom": float(ber - oracle_ber),
    }


def reduce_raw(raw: Mapping, manifest: Mapping, manifest_sha256: str) -> dict:
    validate_raw(raw, manifest, manifest_sha256)
    bootstrap = manifest["bootstrap"]
    development = load_json(SEAM / "development_aggregate.json")
    development_by_cell = {cell["cell_id"]: cell for cell in development["cells"]}
    cells = []
    pooled_candidate: list[float] = []
    pooled_baseline: list[float] = []
    for raw_cell in raw["cells"]:
        rows_by_arm = {
            arm: _arm_rows(raw_cell["windows"], arm)
            for arm in ("B0", "B1", "B2", "C4", "O1")
        }
        oracle_errors = sum(int(row["bit_errors"]) for row in rows_by_arm["O1"])
        oracle_bits = sum(int(row["payload_bits"]) for row in rows_by_arm["O1"])
        summaries = {
            arm: _arm_summary(rows, oracle_errors / oracle_bits)
            for arm, rows in rows_by_arm.items()
        }
        comparison = paired_bootstrap(
            [float(row["ber"]) for row in rows_by_arm["C4"]],
            [float(row["ber"]) for row in rows_by_arm["B2"]],
            seed=int(bootstrap["seed"]),
            resamples=int(bootstrap["resamples"]),
        )
        if raw_cell["pilot_symbols_per_polarization"] == 2:
            pooled_candidate.extend(float(row["ber"]) for row in rows_by_arm["C4"])
            pooled_baseline.extend(float(row["ber"]) for row in rows_by_arm["B2"])
        development_mean = development_by_cell[raw_cell["cell_id"]]["comparisons"][
            "C4_vs_B2"
        ]["mean_diff"]
        cells.append(
            {
                "cell_id": raw_cell["cell_id"],
                "snr_db": raw_cell["snr_db"],
                "pilot_symbols_per_polarization": raw_cell[
                    "pilot_symbols_per_polarization"
                ],
                "confirmation_windows": len(raw_cell["windows"]),
                "parameters": {"B1": raw_cell["b1_eta"], "B2": raw_cell["b2_tau"]},
                "arms": summaries,
                "comparisons": {"C4_vs_B2": comparison},
                "development_direction": {
                    "development_mean_diff": development_mean,
                    "same_sign": (comparison["mean_diff"] < 0.0)
                    == (development_mean < 0.0),
                },
            }
        )
    pooled_np2 = paired_bootstrap(
        pooled_candidate,
        pooled_baseline,
        seed=int(bootstrap["seed"]),
        resamples=int(bootstrap["resamples"]),
    )
    terminal = classify_terminal(cells, pooled_np2)
    return {
        "schema_version": "t071.scaled-unitary-confirmation-aggregate.v1",
        "authority": raw["authority"],
        "manifest_sha256": manifest_sha256,
        "raw_schema_version": raw["schema_version"],
        "cells": cells,
        "pooled_np2": pooled_np2,
        "decision": {
            "terminal": terminal,
            "claim_ceiling": "common-scale estimation evidence only; not a new polarization rotation",
            "primary_comparator": "B2 tau=1.0",
            "next_step": "independent raw recomputation in another context",
        },
    }
