"""Deterministic same-information comparators and post-hoc P03 scoring."""

from __future__ import annotations

from itertools import permutations
from typing import Any

import numpy as np


ROTATIONS = np.asarray([1.0 + 0.0j, 0.0 + 1.0j, -1.0 + 0.0j, 0.0 - 1.0j])
QPSK_AMPLITUDE = 1.0 / np.sqrt(2.0)


def hard_qpsk(samples: np.ndarray, amplitude: float = QPSK_AMPLITUDE) -> np.ndarray:
    values = np.asarray(samples, dtype=np.complex128)
    real = np.where(values.real >= 0.0, amplitude, -amplitude)
    imag = np.where(values.imag >= 0.0, amplitude, -amplitude)
    return np.asarray(real + 1j * imag, dtype=np.complex128)


def _affine_fit(inputs: np.ndarray, targets: np.ndarray, ridge: float) -> np.ndarray:
    x = np.asarray(inputs, dtype=np.complex128)
    y = np.asarray(targets, dtype=np.complex128)
    if x.ndim != 2 or y.shape != x.shape or x.shape[1] != 2 or len(x) < 3:
        raise ValueError("affine calibration requires aligned finite [N,2] arrays with N>=3")
    if not (np.isfinite(x).all() and np.isfinite(y).all()):
        raise ValueError("affine calibration arrays must be finite")
    penalty = float(ridge)
    if not np.isfinite(penalty) or penalty <= 0.0:
        raise ValueError("ridge must be finite and positive")
    design = np.column_stack((x, np.ones(len(x), dtype=np.complex128)))
    regularizer = np.eye(design.shape[1], dtype=np.complex128) * penalty
    regularizer[-1, -1] = 0.0
    return np.linalg.solve(design.conj().T @ design + regularizer, design.conj().T @ y)


def _affine_apply(inputs: np.ndarray, coefficients: np.ndarray) -> np.ndarray:
    x = np.asarray(inputs, dtype=np.complex128)
    if x.ndim != 2 or x.shape[1] != 2 or not np.isfinite(x).all():
        raise ValueError("affine evaluation input must be finite [N,2]")
    design = np.column_stack((x, np.ones(len(x), dtype=np.complex128)))
    output = np.asarray(design @ coefficients, dtype=np.complex128)
    if output.shape != x.shape or not np.isfinite(output).all():
        raise ValueError("affine comparator produced an invalid output")
    return output


def blind_affine_compare(z_calibration: np.ndarray, z_evaluation: np.ndarray, *, ridge: float) -> dict[str, Any]:
    """Fit a one-step complex affine map using z-derived QPSK pseudo-labels only."""
    calibration = np.asarray(z_calibration, dtype=np.complex128)
    pseudo_labels = hard_qpsk(calibration)
    coefficients = _affine_fit(calibration, pseudo_labels, ridge)
    corrected = _affine_apply(z_evaluation, coefficients)
    return {
        "corrected": corrected,
        "predicted": hard_qpsk(corrected),
        "coefficients": coefficients,
        "runtime_inputs": ["z_calibration", "z_evaluation", "known_QPSK_alphabet"],
        "receiver_state_changed": False,
    }


def oracle_affine_bound(
    z_calibration: np.ndarray,
    z_evaluation: np.ndarray,
    truth_calibration: np.ndarray,
    *,
    ridge: float,
) -> np.ndarray:
    """Evaluation-only affine upper bound; callers must never expose coefficients at runtime."""
    coefficients = _affine_fit(z_calibration, truth_calibration, ridge)
    return _affine_apply(z_evaluation, coefficients)


def _bits(symbols: np.ndarray) -> np.ndarray:
    values = np.asarray(symbols, dtype=np.complex128).reshape(-1)
    result = np.empty(2 * len(values), dtype=np.int8)
    result[0::2] = values.real < 0.0
    result[1::2] = values.imag < 0.0
    return result


def _best_stream_metrics(output: np.ndarray, truth: np.ndarray) -> tuple[float, float, complex]:
    target = np.asarray(truth, dtype=np.complex128)
    target_bits = _bits(target)
    best: tuple[float, float, complex] | None = None
    for rotation in ROTATIONS:
        decided = hard_qpsk(np.asarray(output, dtype=np.complex128) * rotation)
        ber = float(np.mean(_bits(decided) != target_bits))
        ser = float(np.mean(decided != target))
        candidate = (ber, ser, complex(rotation))
        if best is None or (candidate[0], candidate[1]) < (best[0], best[1]):
            best = candidate
    assert best is not None
    return best


def evaluate_dual_qpsk(z_x: np.ndarray, z_y: np.ndarray, s_x: np.ndarray, s_y: np.ndarray) -> dict[str, Any]:
    """Report phase-resolved fixed-label and full 2! permutation-invariant BER/SER separately."""
    outputs = (np.asarray(z_x), np.asarray(z_y))
    sources = (np.asarray(s_x), np.asarray(s_y))
    if any(value.ndim != 1 for value in (*outputs, *sources)):
        raise ValueError("dual QPSK evaluator requires one-dimensional streams")
    if len({len(value) for value in (*outputs, *sources)}) != 1:
        raise ValueError("dual QPSK evaluator streams must have equal length")
    candidates = []
    for assignment in permutations((0, 1)):
        per_output = [_best_stream_metrics(outputs[index], sources[assignment[index]]) for index in range(2)]
        candidates.append({
            "assignment": assignment,
            "ber": float(np.mean([row[0] for row in per_output])),
            "ser": float(np.mean([row[1] for row in per_output])),
            "rotations": [[float(row[2].real), float(row[2].imag)] for row in per_output],
        })
    fixed = next(row for row in candidates if row["assignment"] == (0, 1))
    invariant = min(candidates, key=lambda row: (row["ber"], row["ser"], row["assignment"]))
    return {
        "fixed_label_ber": fixed["ber"],
        "pi_ber": invariant["ber"],
        "fixed_label_ser": fixed["ser"],
        "pi_ser": invariant["ser"],
        "pi_assignment": ["sX" if index == 0 else "sY" for index in invariant["assignment"]],
        "fixed_rotations": fixed["rotations"],
        "pi_rotations": invariant["rotations"],
    }


def residual_statistics(corrected: np.ndarray, predicted: np.ndarray, *, tail_energy_threshold: float) -> dict[str, Any]:
    z = np.asarray(corrected, dtype=np.complex128)
    q = np.asarray(predicted, dtype=np.complex128)
    if z.shape != q.shape or z.ndim != 2 or z.shape[1] != 2:
        raise ValueError("residual arrays must be aligned [N,2]")
    residual = z - q
    joint_energy = np.sum(np.abs(residual) ** 2, axis=1)
    threshold = float(tail_energy_threshold)
    conditional: dict[str, dict[str, float | int]] = {}
    for symbol in sorted(np.unique(q), key=lambda value: (float(value.real), float(value.imag))):
        selected = residual[q == symbol]
        key = f"{symbol.real:+.12g}{symbol.imag:+.12g}j"
        conditional[key] = {
            "count": int(len(selected)),
            "mean_real": float(np.mean(selected.real)),
            "mean_imag": float(np.mean(selected.imag)),
            "second_abs_moment": float(np.mean(np.abs(selected) ** 2)),
            "fourth_abs_moment": float(np.mean(np.abs(selected) ** 4)),
        }
    return {
        "mean_joint_residual_energy": float(np.mean(joint_energy)),
        "tail_mass": float(np.mean(joint_energy > threshold)),
        "tail_energy_threshold": threshold,
        "conditional_moments": conditional,
    }


def _cv(values: list[float]) -> float:
    array = np.asarray(values, dtype=float)
    mean = float(np.mean(array))
    return 0.0 if mean == 0.0 else float(np.std(array, ddof=0) / abs(mean))


def summarize_probe(cells: list[dict[str, Any]]) -> dict[str, Any]:
    if len(cells) != 10:
        raise ValueError("the preregistered probe requires exactly 10 cells")
    visible = [float(row["visible_headroom"]) for row in cells]
    gains = [float(row["simple_analytic_gain"]) for row in cells]
    total_headroom = float(np.sum(visible))
    coverage = 1.0 if total_headroom == 0.0 else float(np.clip(np.sum(gains) / total_headroom, 0.0, 1.0))
    energies = [float(row["residual"]["mean_joint_residual_energy"]) for row in cells]
    tails = np.asarray([float(row["residual"]["tail_mass"]) for row in cells], dtype=float)
    by_symbol: dict[str, list[float]] = {}
    for row in cells:
        for symbol, stats in row["residual"]["conditional_moments"].items():
            by_symbol.setdefault(symbol, []).append(float(stats["second_abs_moment"]))
    symbol_cvs = {symbol: _cv(values) for symbol, values in by_symbol.items()}
    symbol_support = {symbol: len(values) for symbol, values in by_symbol.items()}
    summary = {
        "cell_count": len(cells),
        "aggregate_visible_headroom": total_headroom,
        "aggregate_simple_analytic_gain": float(np.sum(gains)),
        "aggregate_analytic_coverage": coverage,
        "cells_with_minimum_headroom": int(sum(value >= float(row["headroom_error_unit"]) for value, row in zip(visible, cells))),
        "median_visible_headroom": float(np.median(visible)),
        "residual_energy_cv": _cv(energies),
        "tail_mass_iqr": float(np.quantile(tails, 0.75) - np.quantile(tails, 0.25)),
        "conditional_second_moment_cv": symbol_cvs,
        "conditional_second_moment_max_cv": max(symbol_cvs.values(), default=float("inf")),
        "conditional_symbol_cell_support": symbol_support,
        "conditional_symbol_min_cell_support": min(symbol_support.values(), default=0),
    }
    return {**summary, **classify_probe(summary)}


def classify_probe(summary: dict[str, Any]) -> dict[str, Any]:
    coverage_pass = float(summary["aggregate_analytic_coverage"]) >= 0.90
    stable_checks = {
        "minimum_cells_with_headroom": int(summary["cells_with_minimum_headroom"]) >= 7,
        "median_visible_headroom": float(summary["median_visible_headroom"]) >= 0.01,
        "residual_energy_cv": float(summary["residual_energy_cv"]) <= 0.50,
        "tail_mass_iqr": float(summary["tail_mass_iqr"]) <= 0.10,
        "conditional_second_moment_max_cv": float(summary["conditional_second_moment_max_cv"]) <= 0.75,
        "conditional_symbol_min_cell_support": int(summary["conditional_symbol_min_cell_support"]) >= 8,
    }
    if coverage_pass:
        verdict = "P03_ANALYTIC_COVERAGE_GE_90"
    elif all(stable_checks.values()):
        verdict = "P03_RESIDUAL_MISMATCH_STABLE"
    else:
        verdict = "P03_RESIDUAL_UNSTABLE"
    return {"primary_verdict": verdict, "analytic_coverage_gate": coverage_pass, "stable_mismatch_checks": stable_checks}

