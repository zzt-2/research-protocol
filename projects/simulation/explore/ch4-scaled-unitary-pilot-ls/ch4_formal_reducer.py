"""Raw-only validation and statistics for the frozen T087 Ch4 population.

This module deliberately does not import the production runner.  The formal
grid is reconstructed independently from the immutable scientific manifest.
"""

from __future__ import annotations

import math
import re
from collections import defaultdict
from collections.abc import Mapping, Sequence

import numpy as np


SCENES = ("weak", "moderate", "strong")
PUBLIC_ROLES = ("B0", "B2_TUNED", "C4_FWD", "B3_PSC", "O1")
HEADLINE_VARIANTS = ("C4_FWD", "B3_PSC")
_SCENARIO_CODES = {"weak": 0, "moderate": 1, "strong": 2}
_COMPONENT_CODES = {
    "payload_bits": 0,
    "channel_q": 1,
    "gg_gain": 2,
    "pilot_noise": 3,
    "payload_noise": 4,
    "mismatch_left": 5,
    "mismatch_right": 6,
}
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def _sha(value: object, name: str) -> str:
    if not isinstance(value, str) or not _SHA256.fullmatch(value):
        raise ValueError(f"{name} hash must be a lowercase SHA-256")
    return value


def _delta_label(delta: float) -> str:
    return str(float(delta)).replace(".", "p")


def _formal_cell_specs(manifest: Mapping[str, object]) -> list[dict[str, object]]:
    snr_grid = [float(value) for value in manifest.get("snr_grid_db", [])]
    if snr_grid != [float(value) for value in range(5, 42, 2)]:
        raise ValueError("scientific SNR grid changed")
    slices = manifest.get("slices")
    if not isinstance(slices, Mapping):
        raise ValueError("scientific slices missing")
    np_by_scene = {
        "weak": list(slices.get("weak_full_curve_np", [])),
        "moderate": list(slices.get("moderate_full_curve_np", [])),
        "strong": list(slices.get("strong_full_curve_np", [])),
    }
    if np_by_scene != {"weak": [2], "moderate": [2, 4, 8, 16], "strong": [2]}:
        raise ValueError("scientific scene/Np slices changed")
    specs: list[dict[str, object]] = []
    for scene in SCENES:
        for n_pilots in np_by_scene[scene]:
            for snr_db in snr_grid:
                specs.append({
                    "cell_id": f"{scene}_np{n_pilots}_snr{int(snr_db)}_primary",
                    "kind": "primary",
                    "scene": scene,
                    "n_pilots": int(n_pilots),
                    "snr_db": float(snr_db),
                    "delta": None,
                })
    mismatch = slices.get("mismatch")
    if not isinstance(mismatch, Mapping) or [float(value) for value in mismatch.get("delta", [])] != [
        0.0, 0.05, 0.1, 0.2, 0.3, 0.4
    ]:
        raise ValueError("scientific mismatch grid changed")
    for delta in (0.05, 0.1, 0.2, 0.3, 0.4):
        specs.append({
            "cell_id": f"moderate_np2_snr25_delta{_delta_label(delta)}",
            "kind": "mismatch",
            "scene": "moderate",
            "n_pilots": 2,
            "snr_db": 25.0,
            "delta": delta,
        })
    specs.append({
        "cell_id": "mismatch_delta0_reference",
        "kind": "reference",
        "delta": 0.0,
        "references_cell_id": "moderate_np2_snr25_primary",
    })
    return specs


def expected_census(purpose: str) -> dict[str, int]:
    if purpose == "formal_smoke_non_thesis":
        clusters = 1
    elif purpose == "canonical_formal_production":
        clusters = 128
    else:
        raise ValueError("raw purpose is not registered")
    return {
        "top_level_latents": clusters,
        "scene_latents": 3 * clusters,
        "actual_cells": 119 * clusters,
        "arm_rows": 595 * clusters,
        "delta_zero_references": clusters,
    }


def _expected_ids(manifest: Mapping[str, object], purpose: str) -> list[int]:
    if purpose == "formal_smoke_non_thesis":
        return [29999]
    if purpose != "canonical_formal_production":
        raise ValueError("raw purpose is not registered")
    population = manifest.get("formal_population")
    if not isinstance(population, Mapping) or population.get("clusters") != 128:
        raise ValueError("formal population changed")
    interval = population.get("latent_ids")
    if not isinstance(interval, Mapping) or interval != {"start": 30000, "stop_inclusive": 30127}:
        raise ValueError("formal population IDs changed")
    return list(range(30000, 30128))


def _jeffreys(errors: int | np.ndarray, bits: int | np.ndarray):
    return (np.asarray(errors) + 0.5) / (np.asarray(bits) + 1.0)


def required_snr(
    snr_db: Sequence[float],
    values: Sequence[float | int],
    threshold: float,
    bits: Sequence[int] | None = None,
) -> dict[str, object]:
    """Evaluate the frozen crossing state and interpolate in log10(BER)."""
    x = np.asarray(snr_db, dtype=float)
    if x.ndim != 1 or len(x) < 2 or not np.all(np.isfinite(x)) or not np.all(np.diff(x) > 0):
        raise ValueError("SNR grid must be finite and strictly increasing")
    if bits is None:
        curve = np.asarray(values, dtype=float)
    else:
        errors_array = np.asarray(values)
        bits_array = np.asarray(bits)
        if errors_array.shape != x.shape or bits_array.shape != x.shape:
            raise ValueError("crossing count shape mismatch")
        if np.any(bits_array <= 0) or np.any(errors_array < 0) or np.any(errors_array > bits_array):
            raise ValueError("crossing counts invalid")
        curve = _jeffreys(errors_array, bits_array).astype(float)
    level = float(threshold)
    if curve.shape != x.shape or not np.all(np.isfinite(curve)) or np.any(curve <= 0) or not 0 < level < 1:
        raise ValueError("crossing curve/threshold invalid")
    if curve[0] <= level:
        status = "CROSSING_UNSTABLE" if np.any(curve[1:] > level) else "BELOW_RANGE"
        return {"status": status, "snr_required_db": None}
    exact = np.flatnonzero(curve == level)
    if exact.size:
        index = int(exact[0])
        if np.any(curve[index + 1 :] > level):
            return {"status": "CROSSING_UNSTABLE", "snr_required_db": None}
        return {"status": "EXACT_HIT", "snr_required_db": float(x[index])}
    if curve[-1] > level:
        status = "CROSSING_UNSTABLE" if np.any(curve[:-1] <= level) else "UNREACHED"
        return {"status": status, "snr_required_db": None}
    downward = [index for index in range(1, len(curve)) if curve[index - 1] > level >= curve[index]]
    if len(downward) != 1:
        return {"status": "CROSSING_UNSTABLE", "snr_required_db": None}
    index = downward[0]
    if np.any(curve[index + 1 :] > level):
        return {"status": "CROSSING_UNSTABLE", "snr_required_db": None}
    y0, y1, target = math.log10(curve[index - 1]), math.log10(curve[index]), math.log10(level)
    crossing = x[index - 1] + (target - y0) * (x[index] - x[index - 1]) / (y1 - y0)
    return {"status": "STABLE", "snr_required_db": float(crossing)}


def grade_ch4(
    curve_results: Mapping[str, Mapping[int, Mapping[str, object]]],
    cell_results: Sequence[Mapping[str, object]],
) -> str:
    """Apply only the frozen A/B/C/F rules to the two registered variants."""
    if not isinstance(curve_results, Mapping) or set(curve_results) != set(HEADLINE_VARIANTS):
        raise ValueError("grade variant key domain changed")
    checked: dict[str, dict[int, Mapping[str, object]]] = {}
    for variant in HEADLINE_VARIANTS:
        rows = curve_results[variant]
        if not isinstance(rows, Mapping) or set(rows) != {2, 4}:
            raise ValueError("grade requires exact moderate Np2/Np4 keys")
        checked[variant] = dict(rows)

    def valid(row: Mapping[str, object]) -> bool:
        return row.get("status") == "VALID" and all(
            math.isfinite(float(row.get(key)))
            for key in ("point_gain_db", "ci_lower_db", "ci_upper_db")
        )

    for variant in HEADLINE_VARIANTS:
        if all(valid(checked[variant][n]) and float(checked[variant][n]["ci_lower_db"]) > 0 for n in (2, 4)):
            return "A"
    for variant in HEADLINE_VARIANTS:
        for strong, other in ((2, 4), (4, 2)):
            a = checked[variant][strong]
            b = checked[variant][other]
            if (
                valid(a)
                and valid(b)
                and float(a["ci_lower_db"]) > 0
                and float(b["point_gain_db"]) >= 0
                and float(b["ci_lower_db"]) <= 0 <= float(b["ci_upper_db"])
            ):
                return "B"
    for row in cell_results:
        if (
            row.get("variant") in HEADLINE_VARIANTS
            and row.get("scene") == "moderate"
            and row.get("n_pilots") in (2, 4)
            and math.isfinite(float(row.get("ci_upper")))
            and float(row["ci_upper"]) < 0
        ):
            return "C"
    return "F"


def _validated_metrics(value: object, role: str) -> tuple[int, int, dict[str, object]]:
    if not isinstance(value, Mapping):
        raise ValueError("row metrics must be a mapping")
    required = {
        "bit_errors", "payload_bits", "ber", "channel_nmse", "inverse_residual",
        "rho", "public_scale", "psc_scale", "channel_nmse_semantics",
    }
    if not required.issubset(value):
        raise ValueError("row metrics schema incomplete")
    errors, bits = value["bit_errors"], value["payload_bits"]
    if isinstance(errors, (bool, np.bool_)) or not isinstance(errors, (int, np.integer)):
        raise ValueError("bit_errors must be an integer")
    if isinstance(bits, (bool, np.bool_)) or not isinstance(bits, (int, np.integer)):
        raise ValueError("payload_bits must be an integer")
    errors, bits = int(errors), int(bits)
    if bits != 32768 or not 0 <= errors <= bits or float(value["ber"]) != errors / bits:
        raise ValueError("row raw counts/BER inconsistent")
    for key in ("ber", "channel_nmse", "inverse_residual", "rho", "psc_scale"):
        if not math.isfinite(float(value[key])):
            raise ValueError("row metric is non-finite")
    public_scale = value["public_scale"]
    if public_scale is not None and not math.isfinite(float(public_scale)):
        raise ValueError("row public scale is non-finite")
    expected_semantics = "pre_calibration_inherited" if role == "B3_PSC" else "direct_estimate"
    if value["channel_nmse_semantics"] != expected_semantics:
        raise ValueError("channel NMSE semantics changed")
    return errors, bits, dict(value)


def _validate_header(
    raw: Mapping[str, object],
    manifest: Mapping[str, object],
    lock: Mapping[str, object],
    scientific_manifest_sha256: str,
    execution_lock_sha256: str,
) -> tuple[str, list[int]]:
    _sha(scientific_manifest_sha256, "scientific manifest")
    _sha(execution_lock_sha256, "execution lock")
    purpose = raw.get("purpose")
    if not isinstance(purpose, str):
        raise ValueError("raw purpose missing")
    expected_ids = _expected_ids(manifest, purpose)
    expected_header = {
        "schema_version": "t087.ch4-formal-raw.v1",
        "purpose": purpose,
        "authority": lock.get("authority"),
        "base_commit": lock.get("base_commit"),
        "control_epoch": lock.get("control_epoch"),
        "mission_checkpoint": lock.get("mission_checkpoint"),
        "scientific_manifest_sha256": scientific_manifest_sha256,
        "execution_lock_sha256": execution_lock_sha256,
        "truth_firewall": "O1_SEPARATE_TRUTH_ONLY_PATH",
        "latent_ids": expected_ids,
    }
    for key, expected in expected_header.items():
        if raw.get(key) != expected:
            label = "truth firewall" if key == "truth_firewall" else key
            raise ValueError(f"raw {label} mismatch")
    if lock.get("scientific_manifest_sha256") != scientific_manifest_sha256:
        raise ValueError("execution lock scientific manifest binding mismatch")
    if raw.get("execution_hashes") != lock.get("execution_hashes"):
        raise ValueError("raw execution hash binding mismatch")
    return purpose, expected_ids


def _validate_rows(
    rows: object,
    manifest: Mapping[str, object],
    scene: str,
    n_pilots: int,
) -> list[tuple[str, int, int, dict[str, object]]]:
    if not isinstance(rows, list) or len(rows) != 5:
        raise ValueError("arm row census invalid")
    runtime_roles = manifest.get("runtime_roles")
    if not isinstance(runtime_roles, Mapping):
        raise ValueError("runtime role manifest missing")
    tau = float(manifest["tuned_tau_by_scene_np"][f"{scene}_np{n_pilots}"])
    output = []
    for row, role in zip(rows, PUBLIC_ROLES):
        if not isinstance(row, Mapping):
            raise ValueError("role row is not a mapping")
        expected_runtime = runtime_roles[role]["runtime_arm"]
        expected_parameter = tau if role == "B2_TUNED" else runtime_roles[role]["parameter"]
        if row.get("public_role") != role or row.get("runtime_arm") != expected_runtime:
            raise ValueError("public/runtime role mapping invalid")
        if row.get("parameter") != expected_parameter:
            raise ValueError("role parameter mismatch")
        if row.get("validity") != "VALID":
            raise ValueError("invalid row invalidates the artifact")
        _sha(row.get("action_sha256"), "action")
        errors, bits, metrics = _validated_metrics(row.get("metrics"), role)
        output.append((role, errors, bits, metrics))
    return output


def _validate_rng_namespace(value: object, scene: str, latent_id: int) -> None:
    if not isinstance(value, Mapping) or set(value) != set(_COMPONENT_CODES):
        raise ValueError("RNG namespace component set invalid")
    scenario_code = _SCENARIO_CODES[scene]
    for name, component_code in _COMPONENT_CODES.items():
        metadata = value[name]
        expected_spawn_key = [84, 1, scenario_code, latent_id, component_code]
        if (
            not isinstance(metadata, Mapping)
            or set(metadata) != {"bit_generator", "entropy", "spawn_key"}
            or metadata.get("bit_generator") != "PCG64"
            or metadata.get("entropy") != 20260830
            or metadata.get("spawn_key") != expected_spawn_key
        ):
            raise ValueError(f"RNG namespace mismatch: {scene}/{latent_id}/{name}")


def _validate_raw(
    raw: Mapping[str, object],
    manifest: Mapping[str, object],
    lock: Mapping[str, object],
    *,
    scientific_manifest_sha256: str,
    execution_lock_sha256: str,
) -> tuple[dict[str, int], dict[tuple[int, str, int, float, str], tuple[int, int]], list[dict[str, object]]]:
    purpose, expected_ids = _validate_header(
        raw, manifest, lock, scientific_manifest_sha256, execution_lock_sha256
    )
    specs = _formal_cell_specs(manifest)
    actual_specs = [spec for spec in specs if spec["kind"] != "reference"]
    expected_by_scene = {
        scene: [spec for spec in actual_specs if spec["scene"] == scene] for scene in SCENES
    }
    latents = raw.get("latents")
    if not isinstance(latents, list) or len(latents) != len(expected_ids):
        raise ValueError("top-level latent census invalid")
    counts: dict[tuple[int, str, int, float, str], tuple[int, int]] = {}
    diagnostics: list[dict[str, object]] = []
    total_cells = total_rows = total_scene_latents = total_references = 0
    for record, latent_id in zip(latents, expected_ids):
        if not isinstance(record, Mapping) or record.get("latent_id") != latent_id:
            raise ValueError("top-level latent ordering/census invalid")
        scenes = record.get("scenes")
        if not isinstance(scenes, list) or [item.get("scene") for item in scenes if isinstance(item, Mapping)] != list(SCENES):
            raise ValueError("scene latent census/order invalid")
        primary_by_id: dict[str, Mapping[str, object]] = {}
        for scene_record, scene in zip(scenes, SCENES):
            if scene_record.get("latent_id") != latent_id:
                raise ValueError("scene latent pairing invalid")
            _validate_rng_namespace(scene_record.get("rng_namespace"), scene, latent_id)
            latent_hashes = scene_record.get("latent_hashes")
            expected_hash_keys = {
                "payload_bits", "channel_q", "gg_gain", "pilot_noise",
                "payload_noise", "mismatch_left", "mismatch_right",
            }
            if not isinstance(latent_hashes, Mapping) or set(latent_hashes) != expected_hash_keys:
                raise ValueError("latent hash key set invalid")
            for name, value in latent_hashes.items():
                _sha(value, f"latent {name}")
            turbulence = scene_record.get("turbulence")
            expected_turbulence = manifest["params_authority"]["resolved_scenes"][scene]
            if (
                not isinstance(turbulence, Mapping)
                or turbulence.get("scenario") != scene
                or float(turbulence.get("alpha")) != float(expected_turbulence["alpha"])
                or float(turbulence.get("beta")) != float(expected_turbulence["beta"])
            ):
                raise ValueError("turbulence snapshot mismatch")
            cells = scene_record.get("cells")
            expected_scene_specs = expected_by_scene[scene]
            if not isinstance(cells, list) or len(cells) != len(expected_scene_specs):
                raise ValueError("cell census invalid")
            observed_ids = [cell.get("cell_id") for cell in cells if isinstance(cell, Mapping)]
            if observed_ids != [spec["cell_id"] for spec in expected_scene_specs]:
                raise ValueError("cell census/order invalid")
            payload_hash_by_snr: dict[float, str] = {}
            for cell, spec in zip(cells, expected_scene_specs):
                for key, expected in spec.items():
                    if cell.get(key) != expected:
                        raise ValueError(f"cell contract mismatch: {spec['cell_id']}/{key}")
                if cell.get("latent_id") != latent_id or cell.get("latent_hashes") != latent_hashes:
                    raise ValueError("cell latent pairing/hash mismatch")
                _sha(cell.get("h_true_sha256"), "channel")
                observation_hashes = cell.get("observation_hashes")
                if not isinstance(observation_hashes, Mapping) or set(observation_hashes) != {
                    "x_pilots", "y_pilots", "y_payload"
                }:
                    raise ValueError("observation hash key set invalid")
                for name, value in observation_hashes.items():
                    _sha(value, f"observation {name}")
                if spec["kind"] == "primary":
                    prior = payload_hash_by_snr.setdefault(float(spec["snr_db"]), observation_hashes["y_payload"])
                    if prior != observation_hashes["y_payload"]:
                        raise ValueError("cross-Np payload observation hash mismatch")
                validated_rows = _validate_rows(
                    cell.get("rows"), manifest, scene, int(spec["n_pilots"])
                )
                for role, errors, bits, metrics in validated_rows:
                    key = (latent_id, scene, int(spec["n_pilots"]), float(spec["snr_db"]), role)
                    if spec["kind"] == "primary":
                        if key in counts:
                            raise ValueError("duplicate primary count key")
                        counts[key] = (errors, bits)
                    diagnostics.append({
                        "latent_id": latent_id,
                        "scene": scene,
                        "n_pilots": int(spec["n_pilots"]),
                        "snr_db": float(spec["snr_db"]),
                        "delta": spec.get("delta"),
                        "kind": spec["kind"],
                        "role": role,
                        **metrics,
                    })
                    total_rows += 1
                primary_by_id[spec["cell_id"]] = cell
                total_cells += 1
            total_scene_latents += 1
        reference = record.get("delta_zero_reference")
        primary = primary_by_id.get("moderate_np2_snr25_primary")
        if not isinstance(reference, Mapping) or primary is None:
            raise ValueError("delta-zero reference missing")
        expected_reference = {
            "cell_id": "mismatch_delta0_reference",
            "kind": "reference",
            "delta": 0.0,
            "references_cell_id": "moderate_np2_snr25_primary",
            "latent_id": latent_id,
            "h_true_sha256": primary.get("h_true_sha256"),
            "reference_observation_hashes": primary.get("observation_hashes"),
        }
        if dict(reference) != expected_reference or "rows" in reference:
            raise ValueError("delta-zero reference is not exact no-row identity")
        total_references += 1
    census = {
        "top_level_latents": len(latents),
        "scene_latents": total_scene_latents,
        "actual_cells": total_cells,
        "arm_rows": total_rows,
        "delta_zero_references": total_references,
    }
    if census != expected_census(purpose):
        raise ValueError("formal raw census mismatch")
    return census, counts, diagnostics


def _curve_arrays(
    counts: Mapping[tuple[int, str, int, float, str], tuple[int, int]],
    latent_ids: Sequence[int],
    scene: str,
    n_pilots: int,
    snr_grid: Sequence[float],
    role: str,
) -> tuple[np.ndarray, np.ndarray]:
    errors = np.empty((len(latent_ids), len(snr_grid)), dtype=np.int64)
    bits = np.empty_like(errors)
    for i, latent_id in enumerate(latent_ids):
        for j, snr_db in enumerate(snr_grid):
            errors[i, j], bits[i, j] = counts[(latent_id, scene, n_pilots, float(snr_db), role)]
    return errors, bits


def _whole_curve_comparison(
    counts: Mapping[tuple[int, str, int, float, str], tuple[int, int]],
    latent_ids: Sequence[int],
    snr_grid: Sequence[float],
    n_pilots: int,
    variant: str,
    manifest: Mapping[str, object],
) -> dict[str, object]:
    threshold = float(manifest["signal"]["engineering_reference_ber"])
    base_e, base_b = _curve_arrays(counts, latent_ids, "moderate", n_pilots, snr_grid, "B2_TUNED")
    var_e, var_b = _curve_arrays(counts, latent_ids, "moderate", n_pilots, snr_grid, variant)
    base_point = required_snr(snr_grid, base_e.sum(axis=0), threshold, base_b.sum(axis=0))
    var_point = required_snr(snr_grid, var_e.sum(axis=0), threshold, var_b.sum(axis=0))
    numeric = {"STABLE", "EXACT_HIT"}
    point_gain = None
    if base_point["status"] in numeric and var_point["status"] in numeric:
        point_gain = float(base_point["snr_required_db"] - var_point["snr_required_db"])
    bootstrap = manifest["whole_curve_bootstrap"]
    rng = np.random.Generator(np.random.PCG64(int(bootstrap["seed"])))
    resamples = int(bootstrap["resamples"])
    indices = rng.integers(0, len(latent_ids), size=(resamples, len(latent_ids)))
    base_e_r = base_e[indices].sum(axis=1)
    base_b_r = base_b[indices].sum(axis=1)
    var_e_r = var_e[indices].sum(axis=1)
    var_b_r = var_b[indices].sum(axis=1)
    gains = []
    for index in range(resamples):
        base_crossing = required_snr(snr_grid, base_e_r[index], threshold, base_b_r[index])
        var_crossing = required_snr(snr_grid, var_e_r[index], threshold, var_b_r[index])
        if base_crossing["status"] in numeric and var_crossing["status"] in numeric:
            gains.append(float(base_crossing["snr_required_db"] - var_crossing["snr_required_db"]))
    minimum = int(bootstrap["valid_gain_replicates_minimum"])
    if len(gains) < minimum or point_gain is None:
        return {
            "status": "CROSSING_UNSTABLE",
            "point_gain_db": point_gain,
            "ci_lower_db": None,
            "ci_upper_db": None,
            "valid_replicates": len(gains),
            "baseline_crossing": base_point,
            "variant_crossing": var_point,
        }
    confidence = float(bootstrap["confidence"])
    alpha = (1.0 - confidence) / 2.0
    lower, upper = np.quantile(np.asarray(gains), [alpha, 1.0 - alpha])
    return {
        "status": "VALID",
        "point_gain_db": point_gain,
        "ci_lower_db": float(lower),
        "ci_upper_db": float(upper),
        "valid_replicates": len(gains),
        "baseline_crossing": base_point,
        "variant_crossing": var_point,
    }


def _cell_comparisons(
    counts: Mapping[tuple[int, str, int, float, str], tuple[int, int]],
    latent_ids: Sequence[int],
    snr_grid: Sequence[float],
    manifest: Mapping[str, object],
) -> list[dict[str, object]]:
    bootstrap = manifest["cell_level_bootstrap"]
    seed = int(bootstrap["seed"])
    resamples = int(bootstrap["resamples"])
    confidence = float(bootstrap["confidence"])
    alpha = (1.0 - confidence) / 2.0
    output = []
    for variant in HEADLINE_VARIANTS:
        for n_pilots in (2, 4):
            for snr_db in snr_grid:
                differences = []
                for latent_id in latent_ids:
                    ve, vb = counts[(latent_id, "moderate", n_pilots, float(snr_db), variant)]
                    be, bb = counts[(latent_id, "moderate", n_pilots, float(snr_db), "B2_TUNED")]
                    differences.append(ve / vb - be / bb)
                values = np.asarray(differences, dtype=float)
                rng = np.random.Generator(np.random.PCG64(seed))
                indices = rng.integers(0, len(values), size=(resamples, len(values)))
                replicates = values[indices].mean(axis=1)
                lower, upper = np.quantile(replicates, [alpha, 1.0 - alpha])
                output.append({
                    "scene": "moderate",
                    "n_pilots": n_pilots,
                    "snr_db": float(snr_db),
                    "variant": variant,
                    "point_difference": float(values.mean()),
                    "ci_lower": float(lower),
                    "ci_upper": float(upper),
                })
    return output


def _raw_summaries(diagnostics: Sequence[Mapping[str, object]]) -> dict[str, object]:
    mechanism: defaultdict[str, list[float]] = defaultdict(list)
    by_scene: defaultdict[str, list[float]] = defaultdict(list)
    by_pilot: defaultdict[int, list[float]] = defaultdict(list)
    by_delta: defaultdict[str, list[float]] = defaultdict(list)
    for row in diagnostics:
        ber = float(row["ber"])
        mechanism[str(row["role"])].append(ber)
        by_scene[str(row["scene"])].append(ber)
        by_pilot[int(row["n_pilots"])].append(ber)
        if row.get("delta") is not None:
            by_delta[str(row["delta"])].append(ber)
    mean = lambda values: float(np.mean(values))
    return {
        "mechanism": {key: {"mean_window_ber": mean(values), "rows": len(values)} for key, values in sorted(mechanism.items())},
        "scene": {key: {"mean_window_ber": mean(values), "rows": len(values)} for key, values in sorted(by_scene.items())},
        "pilot": {str(key): {"mean_window_ber": mean(values), "rows": len(values)} for key, values in sorted(by_pilot.items())},
        "mismatch": {key: {"mean_window_ber": mean(values), "rows": len(values)} for key, values in sorted(by_delta.items())},
    }


def reduce_raw(
    raw: Mapping[str, object],
    manifest: Mapping[str, object],
    lock: Mapping[str, object],
    *,
    scientific_manifest_sha256: str,
    execution_lock_sha256: str,
) -> dict[str, object]:
    """Validate first; never row-drop or consume historical aggregates."""
    if not all(isinstance(value, Mapping) for value in (raw, manifest, lock)):
        raise ValueError("raw, manifest and lock must be mappings")
    census, counts, diagnostics = _validate_raw(
        raw,
        manifest,
        lock,
        scientific_manifest_sha256=scientific_manifest_sha256,
        execution_lock_sha256=execution_lock_sha256,
    )
    if raw["purpose"] == "formal_smoke_non_thesis":
        return {
            "schema_version": "t087.ch4-formal-smoke-aggregate.v1",
            "terminal": "FORMAL_SMOKE_STRUCTURAL_PASS",
            "census": census,
            "grade": None,
            "scientific_numbers_reported": False,
        }
    latent_ids = list(range(30000, 30128))
    snr_grid = [float(value) for value in manifest["snr_grid_db"]]
    curves = {
        variant: {
            n_pilots: _whole_curve_comparison(
                counts, latent_ids, snr_grid, n_pilots, variant, manifest
            )
            for n_pilots in (2, 4)
        }
        for variant in HEADLINE_VARIANTS
    }
    cells = _cell_comparisons(counts, latent_ids, snr_grid, manifest)
    grade = grade_ch4(curves, cells)
    return {
        "schema_version": "t087.ch4-formal-aggregate.v1",
        "terminal": "CH4_FORMAL_REDUCTION_COMPLETE",
        "census": census,
        "headline_curve_comparisons": curves,
        "paired_cell_comparisons": cells,
        "grade": grade,
        "chapter_gate": grade in {"A", "B"},
        "raw_derived_summaries": _raw_summaries(diagnostics),
        "scientific_manifest_sha256": scientific_manifest_sha256,
        "execution_lock_sha256": execution_lock_sha256,
    }
