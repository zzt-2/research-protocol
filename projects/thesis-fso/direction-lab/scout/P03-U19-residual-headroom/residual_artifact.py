"""Build a P03 Scout-only residual diagnostic from receiver-visible inputs."""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from typing import Any

import numpy as np


SCHEMA_VERSION = "direction-lab.p03-residual-artifact.v1"
Z_WINDOW_SCHEMA = "direction-lab.p03-z-window.v1"
COMPARATOR_SCHEMA = "direction-lab.p03-analytic-comparator.v1"
COMPARATOR_ID = "analytic.qpsk-nearest.csi-none.v1"
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _decode_pairs(value: Any, expected_length: int, field: str) -> np.ndarray:
    pairs = np.asarray(value, dtype=np.float64)
    if pairs.shape != (expected_length, 2) or not np.isfinite(pairs).all():
        raise ValueError(f"{field} must be finite [real, imag] pairs aligned to the window")
    return np.asarray(pairs[:, 0] + 1j * pairs[:, 1], dtype=np.complex128)


def _complex_pair(value: complex) -> list[float]:
    return [float(np.real(value)), float(np.imag(value))]


def _conditional_stats(residual: np.ndarray, predicted: np.ndarray) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for symbol in sorted(np.unique(predicted), key=lambda item: (float(item.real), float(item.imag))):
        selected = residual[predicted == symbol]
        real_imag = np.column_stack((selected.real, selected.imag))
        if len(selected) == 1:
            covariance = np.zeros((2, 2), dtype=np.float64)
        else:
            covariance = np.asarray(np.cov(real_imag, rowvar=False, ddof=0), dtype=np.float64)
        label = f"{symbol.real:+.17g}{symbol.imag:+.17g}j"
        result[label] = {
            "predicted_symbol": _complex_pair(symbol),
            "count": int(len(selected)),
            "mean": _complex_pair(complex(np.mean(selected))),
            "real_imag_covariance": covariance.tolist(),
            "second_abs_moment": float(np.mean(np.abs(selected) ** 2)),
            "fourth_abs_moment": float(np.mean(np.abs(selected) ** 4)),
            "pseudo_second_moment": _complex_pair(complex(np.mean(selected ** 2))),
        }
    return result


def _canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _evaluation_section(metrics: Sequence[Mapping[str, Any] | None]) -> dict[str, Any]:
    fixed: list[float] = []
    pi: list[float] = []
    for index, item in enumerate(metrics):
        if item is None:
            continue
        if not isinstance(item, Mapping) or set(item) != {"fixed_label_ber", "pi_ber"}:
            raise ValueError(f"evaluation metrics for cell {index} must contain exactly fixed_label_ber and pi_ber")
        fixed_value = float(item["fixed_label_ber"])
        pi_value = float(item["pi_ber"])
        if not (np.isfinite(fixed_value) and 0.0 <= fixed_value <= 1.0):
            raise ValueError("fixed_label_ber must be finite and in [0, 1]")
        if not (np.isfinite(pi_value) and 0.0 <= pi_value <= 1.0):
            raise ValueError("pi_ber must be finite and in [0, 1]")
        fixed.append(fixed_value)
        pi.append(pi_value)
    if not fixed:
        return {
            "fixed_label_ber": {"status": "NOT_COMPUTED_INTERFACE_SMOKE", "values": []},
            "pi_ber": {"status": "NOT_COMPUTED_INTERFACE_SMOKE", "values": []},
            "causal_use": "FORBIDDEN",
        }
    return {
        "fixed_label_ber": {"status": "RECORDED_EVALUATION_ONLY", "values": fixed},
        "pi_ber": {"status": "RECORDED_EVALUATION_ONLY", "values": pi},
        "causal_use": "FORBIDDEN",
    }


def build_residual_artifact(
    cells: Sequence[Mapping[str, Any]],
    *,
    tail_energy_threshold: float,
    evaluation_metrics_by_cell: Sequence[Mapping[str, Any] | None],
    valid_domain: Mapping[str, Any],
    source_hashes: Mapping[str, str],
) -> dict[str, Any]:
    """Build a diagnostic artifact; no ML-headroom or performance claim is made."""

    threshold = float(tail_energy_threshold)
    if not np.isfinite(threshold) or threshold < 0.0:
        raise ValueError("tail energy threshold must be finite and non-negative")
    if not isinstance(cells, Sequence) or isinstance(cells, (str, bytes)) or not cells:
        raise ValueError("at least one runtime cell is required")
    if len(evaluation_metrics_by_cell) != len(cells):
        raise ValueError("evaluation_metrics_by_cell must align one-to-one with runtime cells")
    if not isinstance(valid_domain, Mapping) or not valid_domain:
        raise ValueError("valid_domain must be an explicit non-empty mapping")
    if not isinstance(source_hashes, Mapping) or not source_hashes:
        raise ValueError("source_hashes must be an explicit non-empty mapping")
    normalized_hashes: dict[str, str] = {}
    for name, digest in source_hashes.items():
        if not isinstance(name, str) or not name or not isinstance(digest, str) or not _SHA256_RE.fullmatch(digest):
            raise ValueError(f"source hash for {name!r} must be a lowercase SHA-256 digest")
        normalized_hashes[name] = digest

    per_cell: list[dict[str, Any]] = []
    all_residuals: dict[str, list[np.ndarray]] = {"zX": [], "zY": []}
    all_predictions: dict[str, list[np.ndarray]] = {"zX": [], "zY": []}
    all_joint_energy: list[np.ndarray] = []
    for cell_index, cell in enumerate(cells):
        if not isinstance(cell, Mapping) or set(cell) != {"z_window", "comparator"}:
            raise ValueError("runtime cell fields must be exactly z_window and comparator")
        window = cell["z_window"]
        comparator = cell["comparator"]
        if window.get("schema_version") != Z_WINDOW_SCHEMA:
            raise ValueError("runtime cell has an unsupported z-window schema")
        if comparator.get("schema_version") != COMPARATOR_SCHEMA:
            raise ValueError("runtime cell has an unsupported comparator schema")
        if comparator.get("comparator_id") != COMPARATOR_ID:
            raise ValueError("comparator_id is not the bound same-information comparator")
        if window.get("csi_access", {}).get("class") != "CSI_NONE" or comparator.get("csi_access_class") != "CSI_NONE":
            raise ValueError("only the closed CSI_NONE path is accepted")
        if comparator.get("receiver_state_changed") is not False:
            raise ValueError("comparator must not change receiver state")
        runtime_fields = comparator.get("input_contract", {}).get("runtime_fields")
        if not isinstance(runtime_fields, list) or not {"zX", "zY"}.issubset(runtime_fields):
            raise ValueError("comparator input contract lacks receiver-visible z fields")
        alignment_fields = ("sequence_id", "symbol_range", "shape", "decision_available_at_input_index")
        if any(window.get(field) != comparator.get(field) for field in alignment_fields):
            raise ValueError("z-window and comparator fields do not align")
        n = int(window["shape"][0])
        residual_by_stream: dict[str, np.ndarray] = {}
        mean_energy_by_stream: dict[str, float] = {}
        for stream in ("zX", "zY"):
            z = _decode_pairs(window["streams"][stream], n, f"z_window.{stream}")
            predicted = _decode_pairs(comparator["predicted_mean"][stream], n, f"comparator.{stream}")
            residual = np.asarray(z - predicted, dtype=np.complex128)
            declared_distance = np.asarray(comparator["squared_distance"][stream], dtype=np.float64)
            if declared_distance.shape != (n,) or not np.allclose(declared_distance, np.abs(residual) ** 2, rtol=0, atol=1e-14):
                raise ValueError("comparator distance does not align with the residual definition")
            residual_by_stream[stream] = residual
            mean_energy_by_stream[stream] = float(np.mean(np.abs(residual) ** 2))
            all_residuals[stream].append(residual)
            all_predictions[stream].append(predicted)
        joint_energy = np.abs(residual_by_stream["zX"]) ** 2 + np.abs(residual_by_stream["zY"]) ** 2
        all_joint_energy.append(np.asarray(joint_energy, dtype=np.float64))
        per_cell.append({
            "cell_index": cell_index,
            "sequence_id": window["sequence_id"],
            "symbol_range": dict(window["symbol_range"]),
            "mean_residual_energy": mean_energy_by_stream,
            "joint_mean_residual_energy": float(np.mean(joint_energy)),
            "tail_mass": float(np.mean(joint_energy > threshold)),
        })

    conditional = {
        stream: _conditional_stats(
            np.concatenate(all_residuals[stream]), np.concatenate(all_predictions[stream])
        )
        for stream in ("zX", "zY")
    }
    joint = np.concatenate(all_joint_energy)
    cell_energies = np.asarray([item["joint_mean_residual_energy"] for item in per_cell], dtype=np.float64)
    if len(cells) == 1:
        stability: dict[str, Any] = {"status": "NOT_ESTIMABLE_ONE_CELL", "cell_count": 1}
    else:
        mean_energy = float(np.mean(cell_energies))
        coefficient = 0.0 if mean_energy == 0.0 else float(np.std(cell_energies, ddof=0) / mean_energy)
        stability = {
            "status": "ESTIMATED",
            "cell_count": len(cells),
            "mean_joint_residual_energy_by_cell": cell_energies.tolist(),
            "coefficient_of_variation_mean_residual_energy": coefficient,
            "range_mean_residual_energy": float(np.max(cell_energies) - np.min(cell_energies)),
        }

    runtime_core: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "role": "SCOUT_INTERFACE_DIAGNOSTIC_NOT_PERFORMANCE",
        "residual_definition": "receiver_visible_z_minus_analytic_comparator_predicted_mean",
        "comparator_id": "analytic.qpsk-nearest.csi-none.v1",
        "csi_access_class": "CSI_NONE",
        "valid_domain": dict(valid_domain),
        "source_hashes": dict(sorted(normalized_hashes.items())),
        "causal_boundary": {
            "runtime_inputs": ["standard-CMA zX", "standard-CMA zY", "fixed known QPSK alphabet"],
            "evaluation_inputs_excluded": True,
            "receiver_state_changed": False,
        },
        "per_cell": per_cell,
        "conditional_moments": conditional,
        "tail": {
            "definition": "dual_pol_sum_abs_residual_squared_strictly_greater_than_threshold",
            "energy_threshold": threshold,
            "mass": float(np.mean(joint > threshold)),
            "sample_count": int(len(joint)),
        },
        "cross_cell_stability": stability,
        "interpretation_limit": "nonzero_residual_does_not_establish_ml_headroom",
    }
    runtime_hash = _canonical_hash(runtime_core)
    return {
        **runtime_core,
        "runtime_artifact_hash": runtime_hash,
        "evaluation_only": _evaluation_section(evaluation_metrics_by_cell),
    }
