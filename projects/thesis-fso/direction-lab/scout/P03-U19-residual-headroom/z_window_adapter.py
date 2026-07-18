"""Causal adapter from the authentic standard-CMA seam to P03 z windows.

The adapter is deliberately strict: it consumes receiver-visible fields only,
requires every indexing/provenance argument explicitly, and emits JSON-safe
complex samples.  It does not compute or accept any evaluation result.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

import numpy as np


SCHEMA_VERSION = "direction-lab.p03-z-window.v1"
_ALLOWED_OUTPUT_FIELDS = {
    "zX",
    "zY",
    "valid_mask",
    "blind_trace",
    "diverged",
    "divergence_symbol",
    "provenance",
}
_FORBIDDEN_KEYS = {
    "sx",
    "sy",
    "bitsx",
    "bitsy",
    "tx_bits",
    "h",
    "true_h",
    "theta",
    "true_jones",
    "oracle_csi",
    "fixed_label_ber",
    "pi_ber",
    "permutation_invariant_ber",
    "post_hoc_ber",
    "future_window",
}
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _scan_forbidden(value: Any, path: str = "receiver_output") -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            normalized = str(key).lower()
            if normalized in _FORBIDDEN_KEYS:
                raise ValueError(f"forbidden field at {path}.{key}")
            _scan_forbidden(nested, f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, nested in enumerate(value):
            _scan_forbidden(nested, f"{path}[{index}]")


def _require_sha256(value: str, field: str) -> str:
    if not isinstance(value, str) or not _SHA256_RE.fullmatch(value):
        raise ValueError(f"{field} must be a lowercase SHA-256 hex digest")
    return value


def _complex_stream(value: Any, field: str) -> np.ndarray:
    array = np.asarray(value)
    if array.ndim != 1:
        raise ValueError(f"{field} must be one-dimensional")
    if not np.issubdtype(array.dtype, np.complexfloating):
        raise ValueError(f"{field} must have a complex dtype")
    array = np.asarray(array, dtype=np.complex128)
    if not np.isfinite(array.real).all() or not np.isfinite(array.imag).all():
        raise ValueError(f"{field} must contain only finite values")
    return array.copy()


def _encode_complex(array: np.ndarray) -> list[list[float]]:
    return np.column_stack((array.real, array.imag)).astype(np.float64).tolist()


def _validate_trace(trace: Any, symbol_start: int, symbol_end: int) -> None:
    if not isinstance(trace, list) or not trace:
        raise ValueError("blind_trace must be a non-empty list")
    completed_ranges: list[tuple[int, int]] = []
    for item in trace:
        if not isinstance(item, Mapping):
            raise ValueError("blind_trace entries must be mappings")
        if "output_start" not in item or "output_end" not in item:
            raise ValueError("blind_trace entry lacks output_start/output_end")
        start = int(item["output_start"])
        end = int(item["output_end"])
        if end <= start:
            raise ValueError("blind_trace range must be non-empty")
        completed_ranges.append((start, end))
    completed_ranges.sort()
    if completed_ranges[0][0] != symbol_start or completed_ranges[-1][1] != symbol_end:
        raise ValueError("future or incomplete window is not covered by blind_trace")
    cursor = symbol_start
    for start, end in completed_ranges:
        if start != cursor:
            raise ValueError("blind_trace ranges must cover the window contiguously")
        cursor = end
    if cursor != symbol_end:
        raise ValueError("future or incomplete window is not covered by blind_trace")


def _validate_estimated_csi(estimate: Any, decision_time: int) -> dict[str, Any]:
    if not isinstance(estimate, Mapping):
        raise ValueError("RECEIVER_ESTIMATED_CSI requires an estimate mapping")
    required = {
        "estimator_id",
        "source_id",
        "source_hash",
        "available_at_input_index",
        "gain_x",
        "gain_y",
        "noise_variance_x",
        "noise_variance_y",
    }
    missing = sorted(required - set(estimate))
    if missing:
        raise ValueError(f"receiver-estimated CSI missing fields: {missing}")
    source_id = str(estimate["source_id"])
    if "oracle" in source_id.lower() or "true" in source_id.lower():
        raise ValueError("oracle CSI source is forbidden")
    available_at = int(estimate["available_at_input_index"])
    if available_at > decision_time:
        raise ValueError("future receiver-estimated CSI is forbidden")
    source_hash = _require_sha256(str(estimate["source_hash"]), "CSI source_hash")
    result: dict[str, Any] = {
        "estimator_id": str(estimate["estimator_id"]),
        "source_id": source_id,
        "source_hash": source_hash,
        "available_at_input_index": available_at,
    }
    for gain_name in ("gain_x", "gain_y"):
        gain = np.asarray(estimate[gain_name], dtype=np.float64)
        if gain.shape != (2,) or not np.isfinite(gain).all():
            raise ValueError(f"{gain_name} must be a finite [real, imag] pair")
        result[gain_name] = gain.tolist()
    for variance_name in ("noise_variance_x", "noise_variance_y"):
        variance = float(estimate[variance_name])
        if not np.isfinite(variance) or variance < 0:
            raise ValueError(f"{variance_name} must be finite and non-negative")
        result[variance_name] = variance
    return result


def adapt_standard_cma_output(
    receiver_output: Mapping[str, Any],
    *,
    sequence_id: str,
    symbol_start: int,
    symbol_end: int,
    equalizer_taps: int,
    csi_access_class: str,
    source_id: str,
    source_hash: str,
    receiver_estimated_csi: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Adapt a completed, contiguous standard-CMA output window."""

    if not isinstance(receiver_output, Mapping):
        raise TypeError("receiver_output must be a mapping")
    _scan_forbidden(receiver_output)
    unknown = sorted(set(receiver_output) - _ALLOWED_OUTPUT_FIELDS)
    if unknown:
        raise ValueError(f"unsupported receiver output fields: {unknown}")
    required = {"zX", "zY", "valid_mask", "blind_trace", "provenance"}
    missing = sorted(required - set(receiver_output))
    if missing:
        raise ValueError(f"receiver output missing fields: {missing}")
    if not isinstance(sequence_id, str) or not sequence_id:
        raise ValueError("sequence_id must be explicit and non-empty")
    if not isinstance(symbol_start, int) or not isinstance(symbol_end, int):
        raise ValueError("symbol range must use explicit integer indices")
    if symbol_end <= symbol_start:
        raise ValueError("symbol range must be non-empty")
    if not isinstance(equalizer_taps, int) or equalizer_taps <= 0 or equalizer_taps % 2 == 0:
        raise ValueError("equalizer_taps must be an explicit positive odd integer")
    if not isinstance(source_id, str) or not source_id:
        raise ValueError("source_id must be explicit and non-empty")
    source_hash = _require_sha256(source_hash, "source_hash")

    z_x = _complex_stream(receiver_output["zX"], "zX")
    z_y = _complex_stream(receiver_output["zY"], "zY")
    expected_length = symbol_end - symbol_start
    if len(z_x) != expected_length or len(z_y) != expected_length:
        raise ValueError("z stream lengths must equal the explicit symbol range")
    mask = np.asarray(receiver_output["valid_mask"])
    if mask.ndim != 1 or mask.dtype != np.bool_ or len(mask) != expected_length:
        raise ValueError("valid_mask must be a bool vector matching the window")
    if not bool(mask.all()):
        raise ValueError("invalid or zero-padded receiver outputs are forbidden")
    _validate_trace(receiver_output["blind_trace"], symbol_start, symbol_end)

    decision_time = symbol_end + equalizer_taps // 2
    normalized_class = str(csi_access_class)
    if normalized_class == "CSI_NONE":
        if receiver_estimated_csi is not None:
            raise ValueError("CSI_NONE forbids any CSI payload")
        csi_access: dict[str, Any] = {"class": "CSI_NONE", "estimate": None}
    elif normalized_class == "RECEIVER_ESTIMATED_CSI":
        csi_access = {
            "class": normalized_class,
            "estimate": _validate_estimated_csi(receiver_estimated_csi, decision_time),
        }
    else:
        raise ValueError("csi_access_class must be CSI_NONE or RECEIVER_ESTIMATED_CSI")

    return {
        "schema_version": SCHEMA_VERSION,
        "sequence_id": sequence_id,
        "symbol_range": {"start": symbol_start, "end_exclusive": symbol_end},
        "decision_available_at_input_index": decision_time,
        "shape": [expected_length, 2],
        "dtype": "complex128_encoded_float64_pairs",
        "unit": "normalized_complex_baseband_symbol",
        "streams": {"zX": _encode_complex(z_x), "zY": _encode_complex(z_y)},
        "valid_mask": mask.tolist(),
        "csi_access": csi_access,
        "source_pointers": {
            "schema_version": {"source_id": SCHEMA_VERSION, "rule": "adapter output schema"},
            "sequence_id": {"source_id": "adapter_call", "field": "sequence_id"},
            "streams.zX": {"source_id": source_id, "source_hash": source_hash, "field": "zX"},
            "streams.zY": {"source_id": source_id, "source_hash": source_hash, "field": "zY"},
            "valid_mask": {"source_id": source_id, "source_hash": source_hash, "field": "valid_mask"},
            "symbol_range": {
                "source_id": source_id,
                "source_hash": source_hash,
                "fields": ["output_start", "output_end"],
            },
            "decision_available_at_input_index": {
                "source_id": source_id,
                "source_hash": source_hash,
                "rule": "end_exclusive + equalizer_taps // 2",
            },
            "shape": {"source_id": SCHEMA_VERSION, "rule": "[symbol_count, polarization_count=2]"},
            "dtype": {"source_id": SCHEMA_VERSION, "rule": "complex128 encoded as float64 pairs"},
            "unit": {"source_id": source_id, "source_hash": source_hash, "rule": "normalized receiver output"},
            "csi_access": {
                "source_id": "adapter_call" if normalized_class == "CSI_NONE" else csi_access["estimate"]["source_id"],
                "field": "csi_access_class",
            },
            "causal_boundary": {"source_id": SCHEMA_VERSION, "rule": "receiver-visible completed samples only"},
        },
        "causal_boundary": {
            "runtime_allowed": ["zX", "zY", "valid_mask", "receiver_estimated_CSI_if_declared"],
            "evaluation_only": ["TX truth", "fixed-label BER", "PI-BER"],
            "forbidden": ["true h", "true Jones", "future window", "post-hoc BER"],
        },
    }


def decode_stream(window: Mapping[str, Any], name: str) -> np.ndarray:
    """Decode one JSON-safe stream back to complex128 for downstream components."""

    if window.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("unsupported z-window schema")
    if name not in {"zX", "zY"}:
        raise ValueError("stream name must be zX or zY")
    pairs = np.asarray(window["streams"][name], dtype=np.float64)
    if pairs.ndim != 2 or pairs.shape[1] != 2 or not np.isfinite(pairs).all():
        raise ValueError(f"encoded {name} must be finite [real, imag] pairs")
    return np.asarray(pairs[:, 0] + 1j * pairs[:, 1], dtype=np.complex128)
