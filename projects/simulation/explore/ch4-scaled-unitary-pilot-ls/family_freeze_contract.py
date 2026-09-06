"""Pure contracts used to freeze the T086 Ch4 scientific manifest."""

from __future__ import annotations

import copy
import math
import re
from collections.abc import Mapping, Sequence


SCENES = ("weak", "moderate", "strong")
PILOT_COUNTS = (2, 4, 8, 16)
TAU_GRID = (0.0, 0.25, 0.5, 0.75, 1.0)
EXPECTED_TAU_KEYS = {f"{scene}_np{n_pilots}" for scene in SCENES for n_pilots in PILOT_COUNTS}
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def _validated_curve(
    snr_db: Sequence[float], errors: Sequence[int], bits: Sequence[int]
) -> tuple[list[float], list[float]]:
    if len(snr_db) < 2 or len(snr_db) != len(errors) or len(errors) != len(bits):
        raise ValueError("curve arrays must have equal length >= 2")
    snr = [float(value) for value in snr_db]
    if not all(math.isfinite(value) for value in snr) or any(b <= a for a, b in zip(snr, snr[1:])):
        raise ValueError("SNR grid must be finite and strictly increasing")
    ber = []
    for index, (error, count) in enumerate(zip(errors, bits)):
        if isinstance(error, bool) or not isinstance(error, int):
            raise ValueError(f"errors[{index}] must be an integer")
        if isinstance(count, bool) or not isinstance(count, int):
            raise ValueError(f"bits[{index}] must be an integer")
        if count <= 0 or error < 0 or error > count:
            raise ValueError(f"curve has invalid counts at index {index}")
        ber.append((error + 0.5) / (count + 1.0))
    return snr, ber


def required_snr(
    snr_db: Sequence[float],
    errors: Sequence[int],
    bits: Sequence[int],
    *,
    threshold: float,
) -> dict[str, object]:
    """Apply the frozen Jeffreys-curve crossing state machine."""
    threshold = float(threshold)
    if not math.isfinite(threshold) or threshold <= 0.0:
        raise ValueError("threshold must be positive and finite")
    snr, ber = _validated_curve(snr_db, errors, bits)
    if ber[0] <= threshold:
        return {"status": "BELOW_RANGE", "snr_db": None}

    downward = [index for index in range(1, len(ber)) if ber[index - 1] > threshold and ber[index] <= threshold]
    if not downward:
        return {"status": "UNREACHED", "snr_db": None}
    first = downward[0]
    upward_after = any(ber[index - 1] <= threshold and ber[index] > threshold for index in range(first + 1, len(ber)))
    if len(downward) != 1 or upward_after:
        return {"status": "CROSSING_UNSTABLE", "snr_db": None}
    if ber[first] == threshold:
        return {"status": "EXACT", "snr_db": snr[first]}

    x0, x1 = snr[first - 1], snr[first]
    y0, y1 = math.log10(ber[first - 1]), math.log10(ber[first])
    target = math.log10(threshold)
    crossing = x0 + (target - y0) * (x1 - x0) / (y1 - y0)
    if not math.isfinite(crossing) or not x0 < crossing < x1:
        raise ValueError("invalid crossing interpolation")
    return {"status": "STABLE", "snr_db": float(crossing)}


def _gain_triplet(value: object) -> tuple[float, float, float] | None:
    if isinstance(value, Mapping):
        if value.get("status", "STABLE") not in {"STABLE", "EXACT"}:
            return None
        raw = (value.get("point"), value.get("lower"), value.get("upper"))
    else:
        raw = value
    if not isinstance(raw, (tuple, list)) or len(raw) != 3:
        return None
    triplet = tuple(float(item) for item in raw)
    return triplet if all(math.isfinite(item) for item in triplet) else None


def assign_grade(evidence: Mapping[str, object]) -> str:
    """Assign the exhaustive A/B/C/F outcome; invalid is a separate terminal."""
    if not isinstance(evidence, Mapping) or evidence.get("artifact_valid") is not True:
        return "CH4_FORMAL_INVALID"
    variants = evidence.get("variants", {})
    expected_variants = {"C4_FWD", "B3_PSC"}
    if not isinstance(variants, Mapping) or set(variants) != expected_variants:
        return "CH4_FORMAL_INVALID"
    for per_np in variants.values():
        if not isinstance(per_np, Mapping) or set(per_np) != {2, 4}:
            return "CH4_FORMAL_INVALID"

    for per_np in variants.values():
        if not isinstance(per_np, Mapping):
            continue
        np2 = _gain_triplet(per_np.get(2, per_np.get("2")))
        np4 = _gain_triplet(per_np.get(4, per_np.get("4")))
        if np2 is not None and np4 is not None and np2[1] > 0.0 and np4[1] > 0.0:
            return "A"
    for per_np in variants.values():
        if not isinstance(per_np, Mapping):
            continue
        np2 = _gain_triplet(per_np.get(2, per_np.get("2")))
        np4 = _gain_triplet(per_np.get(4, per_np.get("4")))
        if np2 is None or np4 is None:
            continue
        left = np2[1] > 0.0 and np4[0] >= 0.0 and np4[1] <= 0.0 <= np4[2]
        right = np4[1] > 0.0 and np2[0] >= 0.0 and np2[1] <= 0.0 <= np2[2]
        if left or right:
            return "B"

    cell_ci_uppers = evidence.get("cell_ci_uppers", {})
    if not isinstance(cell_ci_uppers, Mapping) or set(cell_ci_uppers) != expected_variants:
        return "CH4_FORMAL_INVALID"
    for values in cell_ci_uppers.values():
        if isinstance(values, Sequence) and not isinstance(values, (str, bytes)):
            for value in values:
                number = float(value)
                if not math.isfinite(number):
                    return "CH4_FORMAL_INVALID"
                if number < 0.0:
                    return "C"
    return "F"


def _validated_sha256(value: str, name: str) -> str:
    if not isinstance(value, str) or not _SHA256.fullmatch(value):
        raise ValueError(f"{name} must be a lowercase SHA-256")
    return value


def build_scientific_manifest(
    schema: Mapping[str, object],
    selections: Mapping[str, float],
    *,
    tuning_manifest_sha256: str,
    tuning_raw_sha256: str,
    tuning_aggregate_sha256: str,
    tuning_receipt_sha256: str,
    tuning_terminal: str,
) -> dict[str, object]:
    """Freeze tuning choices into the non-executable T086 scientific manifest."""
    if not isinstance(schema, Mapping):
        raise ValueError("schema must be a mapping")
    if schema.get("schema_version") != "t086.ch4-scientific-manifest-schema.v1":
        raise ValueError("unexpected scientific manifest schema")
    required_schema = {
        "base_commit", "frozen_code_hashes", "params_authority",
        "whole_curve_bootstrap", "cell_level_bootstrap", "execution_lock_interface",
    }
    if not required_schema.issubset(schema):
        raise ValueError("scientific schema is missing required frozen bindings")
    if not isinstance(selections, Mapping) or set(selections) != EXPECTED_TAU_KEYS:
        raise ValueError("scientific manifest requires exactly 12 scene x Np selections")
    checked: dict[str, float] = {}
    for key in sorted(selections):
        tau = float(selections[key])
        if tau not in TAU_GRID:
            raise ValueError(f"invalid tuned tau for {key}")
        checked[key] = tau

    built = copy.deepcopy(dict(schema))
    built["schema_version"] = "t086.ch4-scientific-manifest.v1"
    built["artifact_role"] = "frozen scientific design; T087 execution lock still required"
    built["tuned_tau_by_scene_np"] = checked
    if tuning_terminal != "CH4_B2_TUNING_ACCEPTED":
        raise ValueError("scientific manifest requires accepted tuning terminal")
    lineage = {
        "b2_tuning_manifest_sha256": _validated_sha256(tuning_manifest_sha256, "tuning_manifest_sha256"),
        "b2_tuning_raw_sha256": _validated_sha256(tuning_raw_sha256, "tuning_raw_sha256"),
        "b2_tuning_aggregate_sha256": _validated_sha256(tuning_aggregate_sha256, "tuning_aggregate_sha256"),
        "b2_tuning_receipt_sha256": _validated_sha256(tuning_receipt_sha256, "tuning_receipt_sha256"),
        "receipt_terminal": tuning_terminal,
        "selected_tau_by_scene_np": checked,
    }
    built["tuning_lineage"] = lineage
    built["execution_lock_interface"]["future_code_hash_values"] = None
    for forbidden_key in ("formal_runner_sha256", "formal_reducer_sha256", "formal_tests_sha256"):
        built.pop(forbidden_key, None)
    return built
