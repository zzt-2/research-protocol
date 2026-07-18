"""Same-information analytic comparator for the P03 CSI_NONE path."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import numpy as np


SCHEMA_VERSION = "direction-lab.p03-analytic-comparator.v1"
Z_WINDOW_SCHEMA = "direction-lab.p03-z-window.v1"
COMPARATOR_ID = "analytic.qpsk-nearest.csi-none.v1"


def _decode(window: Mapping[str, Any], stream: str) -> np.ndarray:
    pairs = np.asarray(window["streams"][stream], dtype=np.float64)
    expected = tuple(window["shape"])
    if len(expected) != 2 or expected[1] != 2 or pairs.shape != (expected[0], 2):
        raise ValueError(f"{stream} does not align with the z-window shape")
    if not np.isfinite(pairs).all():
        raise ValueError(f"{stream} contains non-finite values")
    return np.asarray(pairs[:, 0] + 1j * pairs[:, 1], dtype=np.complex128)


def _encode(array: np.ndarray) -> list[list[float]]:
    return np.column_stack((array.real, array.imag)).astype(np.float64).tolist()


def _hard_qpsk(samples: np.ndarray, amplitude: float) -> np.ndarray:
    # Explicit deterministic tie handling; np.sign would emit zero at the axes.
    real = np.where(samples.real >= 0.0, amplitude, -amplitude)
    imag = np.where(samples.imag >= 0.0, amplitude, -amplitude)
    return np.asarray(real + 1j * imag, dtype=np.complex128)


def compare_qpsk_csi_none(
    z_window: Mapping[str, Any],
    *,
    constellation_amplitude: float,
) -> dict[str, Any]:
    """Apply fixed QPSK nearest-neighbour decisions using z only.

    The known modulation alphabet is part of the comparator contract.  No
    channel estimate, transmitter sequence, label, or performance metric is
    read.  Receiver state is never modified.
    """

    if not isinstance(z_window, Mapping) or z_window.get("schema_version") != Z_WINDOW_SCHEMA:
        raise ValueError("unsupported z-window schema")
    csi_class = z_window.get("csi_access", {}).get("class")
    if csi_class != "CSI_NONE":
        raise ValueError("RECEIVER_ESTIMATED_CSI comparator is declared but not bound")
    amplitude = float(constellation_amplitude)
    if not np.isfinite(amplitude) or amplitude <= 0.0:
        raise ValueError("constellation amplitude must be finite and positive")

    streams: dict[str, np.ndarray] = {}
    predicted: dict[str, np.ndarray] = {}
    distances: dict[str, np.ndarray] = {}
    for name in ("zX", "zY"):
        streams[name] = _decode(z_window, name)
        predicted[name] = _hard_qpsk(streams[name], amplitude)
        distances[name] = np.asarray(np.abs(streams[name] - predicted[name]) ** 2, dtype=np.float64)
        if not np.isfinite(distances[name]).all():
            raise ValueError("comparator produced a non-finite distance")

    aggregate = float(np.mean(np.concatenate((distances["zX"], distances["zY"]))))
    return {
        "schema_version": SCHEMA_VERSION,
        "comparator_id": COMPARATOR_ID,
        "csi_access_class": "CSI_NONE",
        "sequence_id": z_window["sequence_id"],
        "symbol_range": dict(z_window["symbol_range"]),
        "decision_available_at_input_index": int(z_window["decision_available_at_input_index"]),
        "shape": list(z_window["shape"]),
        "dtype": "complex128_encoded_float64_pairs",
        "unit": z_window["unit"],
        "constellation": {
            "name": "QPSK",
            "amplitude_per_axis": amplitude,
            "known_at_receiver": True,
        },
        "tie_rule": "real_or_imag_equal_to_zero_maps_to_positive_amplitude",
        "predicted_mean": {name: _encode(predicted[name]) for name in ("zX", "zY")},
        "squared_distance": {name: distances[name].tolist() for name in ("zX", "zY")},
        "aggregate_mean_squared_distance": aggregate,
        "complexity": {
            "distance_evaluations_per_dual_pol_symbol": 8,
            "asymptotic_time": "O(N)",
            "state_memory": "O(1)",
        },
        "metrics": {
            "runtime_observable": ["squared_distance", "aggregate_mean_squared_distance"],
            "evaluation_metrics_are_external": True,
        },
        "input_contract": {
            "runtime_fields": ["zX", "zY", "symbol_range", "CSI_NONE"],
            "excluded_fields": ["TX truth", "true h", "true Jones", "future samples", "BER labels"],
        },
        "receiver_state_changed": False,
    }
