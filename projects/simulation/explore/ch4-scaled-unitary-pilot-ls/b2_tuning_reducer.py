"""Fail-closed reduction helpers for the T086 B2 tuning population."""

from __future__ import annotations

import math
import re
from collections import defaultdict
from collections.abc import Mapping

import numpy as np


SCENES = ("weak", "moderate", "strong")
PILOT_COUNTS = (2, 4, 8, 16)
SNR_GRID = (15.0, 25.0, 35.0)
TAU_GRID = (0.0, 0.25, 0.5, 0.75, 1.0)
EXPECTED_CELLS = {(scene, n_pilots) for scene in SCENES for n_pilots in PILOT_COUNTS}
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def _count_pair(value: object, snr_db: float) -> tuple[int, int]:
    if not isinstance(value, (tuple, list)) or len(value) != 2:
        raise ValueError(f"SNR {snr_db:g} count must be an (errors, bits) pair")
    errors, bits = value
    if isinstance(errors, (bool, np.bool_)) or not isinstance(errors, (int, np.integer)):
        raise ValueError(f"SNR {snr_db:g} errors must be an integer")
    if isinstance(bits, (bool, np.bool_)) or not isinstance(bits, (int, np.integer)):
        raise ValueError(f"SNR {snr_db:g} bits must be an integer")
    errors, bits = int(errors), int(bits)
    if bits <= 0 or errors < 0 or errors > bits:
        raise ValueError(f"SNR {snr_db:g} has invalid binomial counts")
    return errors, bits


def mean_log10_jeffreys(rows: Mapping[float, tuple[int, int]]) -> float:
    """Return the equal-SNR objective; reject incomplete/invalid rows."""
    if not isinstance(rows, Mapping):
        raise ValueError("rows must be a mapping")
    normalized = {float(key): value for key, value in rows.items()}
    if set(normalized) != set(SNR_GRID):
        raise ValueError(f"rows must contain exactly SNR={list(SNR_GRID)}")
    values = []
    for snr_db in SNR_GRID:
        errors, bits = _count_pair(normalized[snr_db], snr_db)
        jeffreys = (errors + 0.5) / (bits + 1.0)
        value = math.log10(jeffreys)
        if not math.isfinite(value):
            raise ValueError("non-finite tuning objective")
        values.append(value)
    result = float(np.mean(values))
    if not math.isfinite(result):
        raise ValueError("non-finite tuning objective")
    return result


def select_tau(objectives: Mapping[float, float]) -> float:
    """Select the minimum objective, breaking an exact tie toward smaller tau."""
    if not isinstance(objectives, Mapping) or not objectives:
        raise ValueError("objectives must be a non-empty mapping")
    checked: dict[float, float] = {}
    for key, value in objectives.items():
        tau = float(key)
        objective = float(value)
        if tau not in TAU_GRID or not math.isfinite(objective):
            raise ValueError("objective contains an invalid tau or value")
        checked[tau] = objective
    if set(checked) != set(TAU_GRID):
        raise ValueError(f"objectives must contain exactly tau={list(TAU_GRID)}")
    return min(sorted(checked), key=lambda tau: checked[tau])


def development_terminal(cells: Mapping[tuple[str, int], Mapping[str, float]]) -> str:
    """Evaluate the frozen all-12-cell cheap-comparator dominance terminal."""
    if not isinstance(cells, Mapping) or set(cells) != EXPECTED_CELLS:
        raise ValueError("development terminal requires exactly all 12 scene x Np cells")
    all_weak = True
    any_strict = False
    for key in sorted(cells):
        row = cells[key]
        if not isinstance(row, Mapping) or set(row) != {"B2_TUNED", "C4_FWD", "B3_PSC"}:
            raise ValueError(f"invalid objective row for {key}")
        values = {name: float(value) for name, value in row.items()}
        if not all(math.isfinite(value) for value in values.values()):
            raise ValueError(f"non-finite objective row for {key}")
        tuned = values["B2_TUNED"]
        for rival in (values["C4_FWD"], values["B3_PSC"]):
            all_weak = all_weak and tuned <= rival
            any_strict = any_strict or tuned < rival
    if all_weak and any_strict:
        return "TUNED_BASELINE_DOMINATES_DEVELOPMENT"
    return "CH4_FAMILY_PRODUCTION_FREEZE_READY"


def _sha(value: object, name: str) -> str:
    if not isinstance(value, str) or not _SHA256.fullmatch(value):
        raise ValueError(f"{name} must be a lowercase SHA-256")
    return value


def _expected_rows() -> list[tuple[str, str, float | None]]:
    return [
        *(("B2_TUNED_CANDIDATE", "B2", tau) for tau in TAU_GRID),
        ("C4_FWD", "C4", None),
        ("B3_PSC", "B3_PSC", 1.0),
    ]


def _validated_metrics(value: object, *, expected_bits: int) -> tuple[int, int]:
    if not isinstance(value, Mapping):
        raise ValueError("row metrics must be a mapping")
    required = {"bit_errors", "payload_bits", "ber", "channel_nmse", "inverse_residual", "rho"}
    if not required.issubset(value):
        raise ValueError("row metrics schema is incomplete")
    errors, bits = _count_pair((value["bit_errors"], value["payload_bits"]), -1.0)
    if bits != expected_bits:
        raise ValueError("row payload bits are inconsistent")
    diagnostics = [float(value[key]) for key in ("ber", "channel_nmse", "inverse_residual", "rho")]
    if not all(math.isfinite(number) for number in diagnostics):
        raise ValueError("row metrics contain non-finite values")
    if diagnostics[0] != errors / bits:
        raise ValueError("row BER is inconsistent with raw counts")
    return errors, bits


def reduce_raw(raw: Mapping[str, object], manifest: Mapping[str, object], manifest_sha256: str) -> dict:
    """Validate and reduce the complete canonical tuning raw without row dropping."""
    if not isinstance(raw, Mapping) or not isinstance(manifest, Mapping):
        raise ValueError("raw and manifest must be mappings")
    _sha(manifest_sha256, "manifest_sha256")
    purpose = raw.get("purpose")
    if purpose == "canonical_tuning_non_thesis":
        expected_ids = list(range(21000, 21032))
    elif purpose == "tuning_preflight_smoke_non_thesis":
        expected_ids = [20999]
    else:
        raise ValueError("raw purpose is not registered")
    expected_header = {
        "schema_version": "t086.b2-tuning-raw.v1",
        "purpose": purpose,
        "authority": manifest.get("authority"),
        "base_commit": manifest.get("base_commit"),
        "control_epoch": manifest.get("control_epoch"),
        "mission_checkpoint": manifest.get("mission_checkpoint"),
        "manifest_sha256": manifest_sha256,
        "truth_firewall": "O1_ABSENT_FROM_TUNING_DEPLOYABLE_ROWS",
    }
    for key, expected in expected_header.items():
        if raw.get(key) != expected:
            raise ValueError(f"raw header mismatch: {key}")
    if raw.get("grid") != manifest.get("grid") or raw.get("code_hashes") != manifest.get("code_hashes"):
        raise ValueError("raw frozen grid/code binding mismatch")
    params = raw.get("params_authority")
    if not isinstance(params, Mapping) or params.get("path") != "projects/simulation/params.py":
        raise ValueError("raw params authority is missing")
    _sha(params.get("sha256"), "params authority SHA")

    grid = manifest["grid"]
    expected_bits = 2 * 4 * int(grid["payload_symbols_per_polarization"])
    expected_latent_keys = [(scene, latent_id) for scene in SCENES for latent_id in expected_ids]
    latents = raw.get("latents")
    if not isinstance(latents, list) or len(latents) != len(expected_latent_keys):
        raise ValueError(f"raw latent census is not 3 x {len(expected_ids)}")
    observed_latent_keys = [(record.get("scene"), record.get("latent_id")) for record in latents if isinstance(record, Mapping)]
    if observed_latent_keys != expected_latent_keys:
        raise ValueError("raw latent ordering/census/pairing changed")

    totals: defaultdict[tuple[str, int, float, str, float | None], list[int]] = defaultdict(lambda: [0, 0])
    observation_cells = 0
    arm_rows = 0
    for record in latents:
        scene = record["scene"]
        latent_id = record["latent_id"]
        if not isinstance(record.get("rng_namespace"), Mapping) or not record["rng_namespace"]:
            raise ValueError(f"rng namespace missing for {scene}/{latent_id}")
        hashes = record.get("latent_hashes")
        expected_hash_keys = {
            "payload_bits", "channel_q", "gg_gain", "pilot_noise", "payload_noise",
            "mismatch_left", "mismatch_right",
        }
        if not isinstance(hashes, Mapping) or set(hashes) != expected_hash_keys:
            raise ValueError(f"latent hashes invalid for {scene}/{latent_id}")
        for name, value in hashes.items():
            _sha(value, f"latent hash {name}")
        turbulence = record.get("turbulence")
        expected_turbulence = manifest["resolved_scenes"][scene]
        if not isinstance(turbulence, Mapping):
            raise ValueError(f"turbulence missing for {scene}/{latent_id}")
        if turbulence.get("scenario") != scene or (
            float(turbulence.get("alpha")) != float(expected_turbulence["alpha"])
            or float(turbulence.get("beta")) != float(expected_turbulence["beta"])
            or turbulence.get("authority") != manifest["turbulence_authority"]
        ):
            raise ValueError(f"turbulence snapshot mismatch for {scene}/{latent_id}")
        cells = record.get("cells")
        expected_cell_grid = [(n_pilots, snr_db) for n_pilots in PILOT_COUNTS for snr_db in SNR_GRID]
        if not isinstance(cells, list) or len(cells) != len(expected_cell_grid):
            raise ValueError(f"cell census invalid for {scene}/{latent_id}")
        observed_cell_grid = [
            (cell.get("pilot_symbols_per_polarization"), cell.get("snr_db"))
            for cell in cells if isinstance(cell, Mapping)
        ]
        if observed_cell_grid != expected_cell_grid:
            raise ValueError(f"cell grid/pairing invalid for {scene}/{latent_id}")
        for cell, (n_pilots, snr_db) in zip(cells, expected_cell_grid):
            if cell.get("scene") != scene or cell.get("cell_id") != f"{scene}_np{n_pilots}_snr{int(snr_db)}":
                raise ValueError(f"cell identity invalid for {scene}/{latent_id}")
            observation_hashes = cell.get("observation_hashes")
            if not isinstance(observation_hashes, Mapping) or set(observation_hashes) != {
                "x_pilots", "y_pilots", "y_payload"
            }:
                raise ValueError("observation hashes are invalid")
            for name, value in observation_hashes.items():
                _sha(value, f"observation hash {name}")
            rows = cell.get("rows")
            if not isinstance(rows, list) or len(rows) != 7:
                raise ValueError(f"rows census invalid for {scene}/{latent_id}/{n_pilots}/{snr_db}")
            observed_rows = [
                (row.get("public_role"), row.get("runtime_arm"), row.get("parameter"))
                for row in rows if isinstance(row, Mapping)
            ]
            if observed_rows != _expected_rows():
                raise ValueError(f"rows role/runtime mapping invalid for {scene}/{latent_id}/{n_pilots}/{snr_db}")
            for row in rows:
                if row.get("validity") != "VALID":
                    raise ValueError("invalid row invalidates the whole tuning artifact")
                _sha(row.get("action_sha256"), "action_sha256")
                errors, bits = _validated_metrics(row.get("metrics"), expected_bits=expected_bits)
                key = (scene, n_pilots, snr_db, row["public_role"], row["parameter"])
                totals[key][0] += errors
                totals[key][1] += bits
                arm_rows += 1
            observation_cells += 1

    windows_per_scene = len(expected_ids)
    expected_observation_cells = len(SCENES) * windows_per_scene * len(PILOT_COUNTS) * len(SNR_GRID)
    expected_rows = expected_observation_cells * 7
    if observation_cells != expected_observation_cells or arm_rows != expected_rows:
        raise ValueError("raw census changed")
    expected_total_bits = windows_per_scene * expected_bits
    selected: dict[str, float] = {}
    cell_objectives: dict[str, dict[str, object]] = {}
    dominance: dict[tuple[str, int], dict[str, float]] = {}
    for scene in SCENES:
        for n_pilots in PILOT_COUNTS:
            b2_objectives = {}
            for tau in TAU_GRID:
                counts = {}
                for snr_db in SNR_GRID:
                    errors, bits = totals[(scene, n_pilots, snr_db, "B2_TUNED_CANDIDATE", tau)]
                    if bits != expected_total_bits:
                        raise ValueError("B2 candidate aggregate bits are inconsistent")
                    counts[snr_db] = (errors, bits)
                b2_objectives[tau] = mean_log10_jeffreys(counts)
            tau = select_tau(b2_objectives)
            rivals = {}
            for role, parameter in (("C4_FWD", None), ("B3_PSC", 1.0)):
                counts = {}
                for snr_db in SNR_GRID:
                    errors, bits = totals[(scene, n_pilots, snr_db, role, parameter)]
                    if bits != expected_total_bits:
                        raise ValueError(f"{role} aggregate bits are inconsistent")
                    counts[snr_db] = (errors, bits)
                rivals[role] = mean_log10_jeffreys(counts)
            key = f"{scene}_np{n_pilots}"
            selected[key] = tau
            dominance[(scene, n_pilots)] = {
                "B2_TUNED": b2_objectives[tau], **rivals,
            }
            cell_objectives[key] = {
                "selected_tau": tau,
                "b2_candidate_objectives": {str(candidate): value for candidate, value in b2_objectives.items()},
                "selected_b2_objective": b2_objectives[tau],
                **{f"{role.lower()}_objective": value for role, value in rivals.items()},
            }
    terminal = development_terminal(dominance)
    return {
        "schema_version": "t086.b2-tuning-aggregate.v1",
        "authority": manifest["authority"],
        "purpose": f"{purpose}_raw_only_reduction",
        "base_commit": manifest["base_commit"],
        "control_epoch": manifest["control_epoch"],
        "mission_checkpoint": manifest["mission_checkpoint"],
        "manifest_sha256": manifest_sha256,
        "census": {
            "scene_latents": len(latents),
            "observation_cells": observation_cells,
            "arm_rows": arm_rows,
        },
        "selected_tau_by_scene_np": selected,
        "cell_objectives": cell_objectives,
        "decision": {
            "terminal": terminal,
            "development_numbers_are_thesis_evidence": False,
        },
    }
