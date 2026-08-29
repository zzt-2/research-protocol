"""Raw-only statistics and frozen terminal for the T085 A2 bridge."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

import numpy as np


ARMS = ("B0", "B2", "B3_PSC", "C4", "O1")
COMPARATORS = ("B2", "B3_PSC")
COMPONENT_CODES = {
    "payload_bits": 0,
    "channel_q": 1,
    "gg_gain": 2,
    "pilot_noise": 3,
    "payload_noise": 4,
    "mismatch_left": 5,
    "mismatch_right": 6,
}


def paired_bootstrap(differences: Sequence[float], *, seed: int, resamples: int) -> dict:
    values = np.asarray(differences, dtype=np.float64)
    if values.ndim != 1 or values.size == 0 or not np.all(np.isfinite(values)):
        raise ValueError("finite one-dimensional paired differences required")
    rng = np.random.Generator(np.random.PCG64(int(seed)))
    indices = rng.integers(0, values.size, size=(int(resamples), values.size), dtype=np.int64)
    draws = values[indices].mean(axis=1)
    lower, upper = np.quantile(draws, [0.025, 0.975])
    return {
        "mean_diff": float(values.mean()),
        "ci_lower": float(lower),
        "ci_upper": float(upper),
        "clusters": int(values.size),
        "candidate_window_wins": int(np.count_nonzero(values < 0.0)),
    }


def pooled_np2_bootstrap(
    differences: Mapping[int, Mapping[float, float]], *, seed: int, resamples: int
) -> dict:
    latent_ids = sorted(int(value) for value in differences)
    if latent_ids != list(range(20000, 20064)):
        raise ValueError("pooled Np2 requires exactly latent IDs 20000..20063")
    matrix = np.asarray(
        [[differences[latent_id][14.0], differences[latent_id][18.0]] for latent_id in latent_ids],
        dtype=np.float64,
    )
    if matrix.shape != (64, 2) or not np.all(np.isfinite(matrix)):
        raise ValueError("pooled Np2 requires two finite SNR rows per latent cluster")
    rng = np.random.Generator(np.random.PCG64(int(seed)))
    indices = rng.integers(0, 64, size=(int(resamples), 64), dtype=np.int64)
    draws = matrix[indices].mean(axis=(1, 2))
    lower, upper = np.quantile(draws, [0.025, 0.975])
    return {
        "mean_diff": float(matrix.mean()),
        "ci_lower": float(lower),
        "ci_upper": float(upper),
        "clusters": 64,
        "rows_per_cluster": 2,
        "candidate_cluster_wins": int(np.count_nonzero(matrix.mean(axis=1) < 0.0)),
    }


def _rows(cell: Mapping) -> dict[str, Mapping]:
    rows = cell.get("rows")
    if not isinstance(rows, list) or [row.get("arm") for row in rows] != list(ARMS):
        raise ValueError("arm row order/count mismatch")
    return {str(row["arm"]): row for row in rows}


def _validate_metric_row(row: Mapping, parameter: object) -> None:
    if row.get("parameter") != parameter or row.get("validity") != "VALID":
        raise ValueError("arm parameter/validity mismatch")
    metrics = row.get("metrics")
    required = {"bit_errors", "payload_bits", "ber", "channel_nmse", "inverse_residual", "rho"}
    if not isinstance(metrics, dict) or set(metrics) != required:
        raise ValueError("metric schema mismatch")
    errors = int(metrics["bit_errors"])
    bits = int(metrics["payload_bits"])
    if bits != 32768 or not 0 <= errors <= bits or float(metrics["ber"]) != errors / bits:
        raise ValueError("BER count mismatch")
    if not all(np.isfinite(float(metrics[key])) for key in ("ber", "channel_nmse", "inverse_residual", "rho")):
        raise ValueError("nonfinite metric")
    if row.get("public_scale") is not None and not np.isfinite(float(row["public_scale"])):
        raise ValueError("nonfinite public scale")
    if not np.isfinite(float(row.get("psc_scale"))) or float(row["psc_scale"]) < 0.0:
        raise ValueError("invalid PSC scale")
    action_hash = row.get("action_sha256")
    if not isinstance(action_hash, str) or len(action_hash) != 64:
        raise ValueError("action hash mismatch")
    if not isinstance(row.get("runtime_ns"), int) or int(row["runtime_ns"]) < 0:
        raise ValueError("runtime mismatch")


def validate_raw(raw: Mapping, manifest: Mapping, manifest_sha256: str) -> dict[str, int]:
    if raw.get("schema_version") != "t085.corrected-anchor-raw.v1":
        raise ValueError("raw schema mismatch")
    if raw.get("purpose") != "a2_bridge_non_thesis":
        raise ValueError("canonical purpose mismatch")
    for key in ("authority", "base_commit", "control_epoch", "mission_checkpoint", "scene", "cells", "payload_symbols_per_polarization", "max_pilots", "code_hashes"):
        expected = manifest["code_hashes"] if key == "code_hashes" else manifest[key]
        if raw.get(key) != expected:
            raise ValueError(f"raw/manifest mismatch: {key}")
    if raw.get("manifest_sha256") != manifest_sha256:
        raise ValueError("manifest hash mismatch")
    if raw.get("truth_firewall") != "O1_SEPARATE_TRUTH_ONLY_PATH":
        raise ValueError("truth firewall marker mismatch")
    latents = raw.get("latents")
    if not isinstance(latents, list) or [item.get("latent_id") for item in latents] != list(range(20000, 20064)):
        raise ValueError("latent census/order mismatch")
    census = {"latents": 0, "cell_rows": 0, "arm_rows": 0}
    for latent in latents:
        latent_id = int(latent["latent_id"])
        namespace = latent.get("rng_namespace")
        hashes = latent.get("latent_hashes")
        if not isinstance(namespace, dict) or set(namespace) != set(COMPONENT_CODES):
            raise ValueError("RNG namespace components mismatch")
        if not isinstance(hashes, dict) or set(hashes) != set(COMPONENT_CODES):
            raise ValueError("latent hash components mismatch")
        for name, code in COMPONENT_CODES.items():
            if namespace[name] != {
                "bit_generator": "PCG64", "entropy": 20260830,
                "spawn_key": [84, 1, 1, latent_id, code],
            }:
                raise ValueError("RNG namespace identity mismatch")
            if not isinstance(hashes[name], str) or len(hashes[name]) != 64:
                raise ValueError("latent component hash mismatch")
        turbulence = latent.get("turbulence")
        expected_turbulence = {
            "scenario": manifest["scene"]["name"],
            "alpha": manifest["scene"]["alpha"],
            "beta": manifest["scene"]["beta"],
            "scintillation_index": 1 / manifest["scene"]["alpha"] + 1 / manifest["scene"]["beta"] + 1 / (manifest["scene"]["alpha"] * manifest["scene"]["beta"]),
            "authority": manifest["scene"]["authority"],
        }
        if turbulence != expected_turbulence:
            raise ValueError("turbulence snapshot mismatch")
        cells = latent.get("cells")
        if not isinstance(cells, list) or len(cells) != 4:
            raise ValueError("per-latent cell count mismatch")
        by_key = {}
        for cell, frozen in zip(cells, manifest["cells"]):
            for key in ("cell_id", "snr_db", "pilot_symbols_per_polarization"):
                if cell.get(key) != frozen[key]:
                    raise ValueError(f"cell identity mismatch: {key}")
            observation_hashes = cell.get("observation_hashes")
            if not isinstance(observation_hashes, dict) or set(observation_hashes) != {"x_pilots", "y_pilots", "y_payload"}:
                raise ValueError("observation hash schema mismatch")
            if not all(isinstance(value, str) and value for value in observation_hashes.values()):
                raise ValueError("observation hash invalid")
            rows = _rows(cell)
            for arm in ARMS:
                _validate_metric_row(rows[arm], manifest["arms"][arm]["parameter"])
                census["arm_rows"] += 1
            by_key[(float(cell["snr_db"]), int(cell["pilot_symbols_per_polarization"]))] = cell
            census["cell_rows"] += 1
        for snr in (14.0, 18.0):
            np2 = by_key[(snr, 2)]
            np4 = by_key[(snr, 4)]
            if np2["observation_hashes"]["y_payload"] != np4["observation_hashes"]["y_payload"]:
                raise ValueError("same-SNR payload observation pairing mismatch")
            if _rows(np2)["O1"]["metrics"] != _rows(np4)["O1"]["metrics"]:
                raise ValueError("same-SNR O1 metric pairing mismatch")
        census["latents"] += 1
    if census != {"latents": 64, "cell_rows": 256, "arm_rows": 1280}:
        raise ValueError("raw census incomplete")
    return census


def _summary(rows: Sequence[Mapping]) -> dict:
    errors = sum(int(row["metrics"]["bit_errors"]) for row in rows)
    bits = sum(int(row["metrics"]["payload_bits"]) for row in rows)
    return {
        "bit_errors": errors,
        "payload_bits": bits,
        "ber": float(errors / bits),
        "channel_nmse": float(np.mean([row["metrics"]["channel_nmse"] for row in rows])),
        "inverse_residual": float(np.mean([row["metrics"]["inverse_residual"] for row in rows])),
        "rho": float(np.mean([row["metrics"]["rho"] for row in rows])),
        "public_scale_mean": None if all(row["public_scale"] is None for row in rows) else float(np.mean([row["public_scale"] for row in rows if row["public_scale"] is not None])),
        "psc_scale_mean": float(np.mean([row["psc_scale"] for row in rows])),
    }


def reduce_raw(raw: Mapping, manifest: Mapping, manifest_sha256: str) -> dict:
    census = validate_raw(raw, manifest, manifest_sha256)
    seed = int(manifest["bootstrap"]["seed"])
    resamples = int(manifest["bootstrap"]["resamples"])
    grouped = {cell["cell_id"]: {arm: [] for arm in ARMS} for cell in manifest["cells"]}
    cell_differences = {cell["cell_id"]: {arm: [] for arm in COMPARATORS} for cell in manifest["cells"]}
    pooled = {arm: {} for arm in COMPARATORS}
    for latent in raw["latents"]:
        latent_id = int(latent["latent_id"])
        for cell in latent["cells"]:
            cell_id = cell["cell_id"]
            rows = _rows(cell)
            for arm in ARMS:
                grouped[cell_id][arm].append(rows[arm])
            for comparator in COMPARATORS:
                difference = float(rows["C4"]["metrics"]["ber"] - rows[comparator]["metrics"]["ber"])
                cell_differences[cell_id][comparator].append(difference)
                if int(cell["pilot_symbols_per_polarization"]) == 2:
                    pooled[comparator].setdefault(latent_id, {})[float(cell["snr_db"])] = difference
    cells = []
    for frozen in manifest["cells"]:
        cell_id = frozen["cell_id"]
        cells.append({
            **frozen,
            "windows": 64,
            "arms": {arm: _summary(grouped[cell_id][arm]) for arm in ARMS},
            "comparisons": {
                comparator: paired_bootstrap(cell_differences[cell_id][comparator], seed=seed, resamples=resamples)
                for comparator in COMPARATORS
            },
        })
    pooled_summary = {
        comparator: pooled_np2_bootstrap(pooled[comparator], seed=seed, resamples=resamples)
        for comparator in COMPARATORS
    }
    np4 = [cell for cell in cells if int(cell["pilot_symbols_per_polarization"]) == 4]
    passed = all(pooled_summary[arm]["ci_upper"] < 0.0 for arm in COMPARATORS) and all(
        cell["comparisons"][arm]["ci_lower"] <= 0.0 for cell in np4 for arm in COMPARATORS
    )
    terminal = "PRODUCTION_SEAM_BRIDGE_PASS" if passed else "CHEAP_COMPARATOR_NOT_CLEARED"
    return {
        "schema_version": "t085.corrected-anchor-aggregate.v1",
        "authority": manifest["authority"],
        "manifest_sha256": manifest_sha256,
        "raw_schema_version": raw["schema_version"],
        "census": census,
        "cells": cells,
        "pooled_np2": pooled_summary,
        "metric_semantics": {"B3_PSC_channel_nmse": "inherited pre-calibration B2 estimate", "B3_PSC_inverse_residual": "post-calibration action"},
        "decision": {"terminal": terminal, "strict_comparators": list(COMPARATORS)},
    }
