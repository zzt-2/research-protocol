"""Pure preregistered reducers for T067 bounded development."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence

import numpy as np


def select_tuned_value(
    rows: Iterable[Mapping[str, float | int]],
    *,
    tune_window_ids: Sequence[int],
    value_key: str,
    metric_key: str,
    tie_tolerance: float,
) -> float:
    """Maximize tune-only mean metric; exact/near ties prefer more shrinkage."""
    allowed = {int(value) for value in tune_window_ids}
    grouped: dict[float, list[float]] = {}
    for row in rows:
        if int(row["window_id"]) not in allowed:
            continue
        value = float(row[value_key])
        grouped.setdefault(value, []).append(float(row[metric_key]))
    if not grouped or any(len(values) != len(allowed) for values in grouped.values()):
        raise ValueError("tuning rows must cover every tune window for every value")
    means = {value: float(np.mean(metrics)) for value, metrics in grouped.items()}
    best = max(means.values())
    return max(value for value, score in means.items() if score >= best - tie_tolerance)


def paired_bootstrap_summary(
    candidate: Sequence[float],
    baseline: Sequence[float],
    *,
    seed: int,
    resamples: int,
    lower_is_better: bool = False,
) -> dict:
    """Paired window-cluster difference with one PCG64 bootstrap stream."""
    candidate_array = np.asarray(candidate, dtype=np.float64)
    baseline_array = np.asarray(baseline, dtype=np.float64)
    if (
        candidate_array.ndim != 1
        or candidate_array.shape != baseline_array.shape
        or candidate_array.size == 0
        or not np.all(np.isfinite(candidate_array))
        or not np.all(np.isfinite(baseline_array))
    ):
        raise ValueError("paired finite one-dimensional window metrics required")
    difference = candidate_array - baseline_array
    rng = np.random.Generator(np.random.PCG64(seed))
    indices = rng.integers(
        0, difference.size, size=(int(resamples), difference.size), dtype=np.int64
    )
    bootstrap = difference[indices].mean(axis=1)
    return {
        "mean_diff": float(difference.mean()),
        "ci": [float(value) for value in np.quantile(bootstrap, [0.025, 0.975])],
        "wins": int(
            np.count_nonzero(difference < 0.0)
            if lower_is_better
            else np.count_nonzero(difference > 0.0)
        ),
        "clusters": int(difference.size),
    }


def _gmi_signal(comparison: Mapping[str, Mapping]) -> bool:
    return float(comparison["gmi"]["ci"][0]) > 0.0


def _ber_noninferior(comparison: Mapping[str, Mapping]) -> bool:
    return float(comparison["ber"]["ci"][1]) <= 0.0


def classify_round1(
    comparisons: Mapping[str, Mapping], *, strongest_comparator: str
) -> dict[str, str | None]:
    """Apply T067 Round-1 terminals without post-hoc threshold changes."""
    if strongest_comparator not in {"B2", "B3"}:
        raise ValueError("strongest comparator must be B2 or B3")
    c1_strong = comparisons[f"C1_vs_{strongest_comparator}"]
    if _gmi_signal(c1_strong) and _ber_noninferior(c1_strong):
        return {
            "terminal": "C1_SIGNAL",
            "winner": "C1",
            "strongest_comparator": strongest_comparator,
        }
    simple_signals = [
        arm
        for arm in ("B2", "B3")
        if _gmi_signal(comparisons[f"{arm}_vs_B1"])
        and _ber_noninferior(comparisons[f"{arm}_vs_B1"])
    ]
    if simple_signals:
        winner = "B2" if "B2" in simple_signals else "B3"
        return {
            "terminal": "SIMPLE_MIGRATION_SIGNAL",
            "winner": winner,
            "strongest_comparator": strongest_comparator,
        }
    if any(_gmi_signal(comparisons[f"{arm}_vs_B1"]) for arm in ("B2", "B3", "C1")):
        return {
            "terminal": "GMI_ONLY_SIGNAL",
            "winner": None,
            "strongest_comparator": strongest_comparator,
        }
    return {
        "terminal": "NO_METHOD_SIGNAL",
        "winner": None,
        "strongest_comparator": strongest_comparator,
    }


def classify_provisional_grade(points: Sequence[Mapping[str, Mapping]]) -> str:
    """Grade the frozen Round-2 winner against B1 over exactly three cells."""
    if len(points) != 3:
        raise ValueError("T067 provisional grade requires exactly three SNR points")
    ber_clear = sum(float(point["ber"]["ci"][1]) < 0.0 for point in points)
    gmi_not_worse = all(float(point["gmi"]["ci"][1]) >= 0.0 for point in points)
    if ber_clear >= 2 and gmi_not_worse:
        return "PROVISIONAL_A/B"
    if ber_clear or any(float(point["gmi"]["ci"][0]) > 0.0 for point in points):
        return "PROVISIONAL_C"
    return "D"


def _inclusive_ids(spec: Mapping[str, int]) -> tuple[int, ...]:
    return tuple(range(int(spec["start"]), int(spec["stop_inclusive"]) + 1))


def validate_round1_windows(windows: Sequence[Mapping], manifest: Mapping) -> None:
    """Fail closed on the frozen Round-1 population and fairness invariants."""
    round1 = manifest["round1"]
    if len(windows) != int(round1["windows"]):
        raise ValueError("round1 must contain exactly 64 windows")
    expected_seeds = _inclusive_ids(round1["seeds"])
    tune_ids = set(_inclusive_ids(round1["tune_window_ids"]))
    eval_ids = set(_inclusive_ids(round1["evaluation_window_ids"]))
    if tune_ids & eval_ids or tune_ids | eval_ids != set(range(len(windows))):
        raise ValueError("manifest tune/evaluation split must be disjoint and exhaustive")
    expected_parameters = {
        "B1": {None},
        "B2": {None},
        "B3": {float(value) for value in round1["tuning"]["B3_shrinkage"]},
        "C1": {float(value) for value in round1["tuning"]["C1_kappa"]},
    }
    config_hashes: set[str] = set()
    realization_hashes: set[str] = set()
    bundle_hashes: set[str] = set()
    for expected_id, (window, expected_seed) in enumerate(zip(windows, expected_seeds)):
        if int(window["window_id"]) != expected_id:
            raise ValueError("window id/order mismatch")
        if int(window["seed"]) != expected_seed:
            raise ValueError("window seed mismatch")
        expected_split = "tune" if expected_id in tune_ids else "evaluation"
        if window["split"] != expected_split:
            raise ValueError("window split mismatch")
        if int(window["pilot_symbols_per_polarization"]) != 64:
            raise ValueError("pilot count mismatch")
        if int(window["payload_symbols_per_polarization"]) != 192:
            raise ValueError("payload count mismatch")
        if window["per_pol_point_counts"] != [[4] * 16, [4] * 16]:
            raise ValueError("per-point count mismatch")
        observed: dict[str, set[float | None]] = {name: set() for name in expected_parameters}
        for row in window["rows"]:
            arm = row["arm"]
            if arm not in observed:
                raise ValueError("unregistered arm")
            parameter = None if row["parameter"] is None else float(row["parameter"])
            observed[arm].add(parameter)
            numeric = [
                row["gmi"], row["ber"], row["nll"], row["condition_max"],
                row["floor_rate"], row["runtime_s"],
            ]
            if not all(np.isfinite(float(value)) for value in numeric):
                raise ValueError("nonfinite metric")
            if int(row["payload_bits"]) != 1536:
                raise ValueError("payload bit denominator mismatch")
            if not 0 <= int(row["bit_errors"]) <= int(row["payload_bits"]):
                raise ValueError("bit error numerator mismatch")
        if observed != expected_parameters:
            raise ValueError("arm parameter grid mismatch")
        config_hashes.add(str(window["config_hash"]))
        realization_hashes.add(str(window["realization_hash"]))
        bundle_hashes.add(str(window["bundle_hash"]))
    if len(config_hashes) != 1:
        raise ValueError("round1 config hash mismatch")
    if len(realization_hashes) != len(windows):
        raise ValueError("round1 realization hashes must be unique")
    if len(bundle_hashes) != len(windows):
        raise ValueError("round1 bundle hashes must be unique")


def _row_for(window: Mapping, arm: str, parameter: float | None) -> Mapping:
    matches = [
        row
        for row in window["rows"]
        if row["arm"] == arm
        and (
            (parameter is None and row["parameter"] is None)
            or (
                parameter is not None
                and row["parameter"] is not None
                and float(row["parameter"]) == float(parameter)
            )
        )
    ]
    if len(matches) != 1:
        raise ValueError(f"expected one row for {arm}/{parameter}")
    return matches[0]


def _arm_summary(rows: Sequence[Mapping]) -> dict:
    return {
        "mean_gmi": float(np.mean([row["gmi"] for row in rows])),
        "mean_ber": float(np.mean([row["ber"] for row in rows])),
        "held_out_nll": float(np.mean([row["nll"] for row in rows])),
        "payload_bits": int(sum(int(row["payload_bits"]) for row in rows)),
        "bit_errors": int(sum(int(row["bit_errors"]) for row in rows)),
        "condition_max": float(max(float(row["condition_max"]) for row in rows)),
        "floor_rate": float(np.mean([row["floor_rate"] for row in rows])),
        "runtime_s": float(sum(float(row["runtime_s"]) for row in rows)),
    }


def _comparison(candidate: Sequence[Mapping], baseline: Sequence[Mapping], manifest: Mapping) -> dict:
    bootstrap = manifest["bootstrap"]
    return {
        "gmi": paired_bootstrap_summary(
            [row["gmi"] for row in candidate],
            [row["gmi"] for row in baseline],
            seed=int(bootstrap["seed"]),
            resamples=int(bootstrap["resamples"]),
        ),
        "ber": paired_bootstrap_summary(
            [row["ber"] for row in candidate],
            [row["ber"] for row in baseline],
            seed=int(bootstrap["seed"]),
            resamples=int(bootstrap["resamples"]),
            lower_is_better=True,
        ),
    }


def reduce_round1(windows: Sequence[Mapping], manifest: Mapping) -> dict:
    """Rebuild the complete Round-1 terminal from raw window rows only."""
    validate_round1_windows(windows, manifest)
    tune = [window for window in windows if window["split"] == "tune"]
    evaluation = [window for window in windows if window["split"] == "evaluation"]
    tuning = manifest["round1"]["tuning"]
    c1_rows = [
        {"window_id": window["window_id"], "value": row["parameter"], "gmi": row["gmi"]}
        for window in tune
        for row in window["rows"]
        if row["arm"] == "C1"
    ]
    b3_rows = [
        {"window_id": window["window_id"], "value": row["parameter"], "gmi": row["gmi"]}
        for window in tune
        for row in window["rows"]
        if row["arm"] == "B3"
    ]
    tune_ids = tuple(int(window["window_id"]) for window in tune)
    c1_value = select_tuned_value(
        c1_rows,
        tune_window_ids=tune_ids,
        value_key="value",
        metric_key="gmi",
        tie_tolerance=float(tuning["tie_tolerance"]),
    )
    b3_value = select_tuned_value(
        b3_rows,
        tune_window_ids=tune_ids,
        value_key="value",
        metric_key="gmi",
        tie_tolerance=float(tuning["tie_tolerance"]),
    )
    selected = {
        "B1": [_row_for(window, "B1", None) for window in evaluation],
        "B2": [_row_for(window, "B2", None) for window in evaluation],
        "B3": [_row_for(window, "B3", b3_value) for window in evaluation],
        "C1": [_row_for(window, "C1", c1_value) for window in evaluation],
    }
    summaries = {arm: _arm_summary(rows) for arm, rows in selected.items()}
    b2 = summaries["B2"]
    b3 = summaries["B3"]
    strongest = (
        "B2"
        if b2["mean_gmi"] >= b3["mean_gmi"] - float(tuning["tie_tolerance"])
        and b2["mean_ber"] <= b3["mean_ber"] + float(tuning["tie_tolerance"])
        else max(("B2", "B3"), key=lambda arm: (summaries[arm]["mean_gmi"], -summaries[arm]["mean_ber"]))
    )
    comparisons = {
        "B2_vs_B1": _comparison(selected["B2"], selected["B1"], manifest),
        "B3_vs_B1": _comparison(selected["B3"], selected["B1"], manifest),
        "C1_vs_B1": _comparison(selected["C1"], selected["B1"], manifest),
        "C1_vs_B2": _comparison(selected["C1"], selected["B2"], manifest),
        "C1_vs_B3": _comparison(selected["C1"], selected["B3"], manifest),
    }
    verdict = classify_round1(comparisons, strongest_comparator=strongest)
    return {
        "schema_version": "t067.structured-covariance-development.aggregate.v1",
        "authority": manifest["authority"],
        "round1_windows": len(windows),
        "tune_windows": len(tune),
        "evaluation_windows": len(evaluation),
        "tuning": {"C1_kappa": c1_value, "B3_shrinkage": b3_value},
        "arms": summaries,
        "comparisons": comparisons,
        "strongest_comparator": strongest,
        "terminal": verdict["terminal"],
        "winner": verdict["winner"],
        "round2_authorized": verdict["terminal"] in {"C1_SIGNAL", "SIMPLE_MIGRATION_SIGNAL"},
        "bootstrap": dict(manifest["bootstrap"]),
        "split": {
            "tune_window_ids": [int(window["window_id"]) for window in tune],
            "evaluation_window_ids": [int(window["window_id"]) for window in evaluation],
            "disjoint": True,
        },
        "hashes": {
            "unique_config_hashes": len({window["config_hash"] for window in windows}),
            "unique_realization_hashes": len({window["realization_hash"] for window in windows}),
            "unique_bundle_hashes": len({window["bundle_hash"] for window in windows}),
        },
    }


__all__ = [
    "classify_provisional_grade",
    "classify_round1",
    "paired_bootstrap_summary",
    "reduce_round1",
    "select_tuned_value",
    "validate_round1_windows",
]
