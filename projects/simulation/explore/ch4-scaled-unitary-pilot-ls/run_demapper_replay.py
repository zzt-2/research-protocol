"""T083 exact historical-observation replay with corrected global-ML scoring."""

from __future__ import annotations

import hashlib
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from development import action_bytes, make_realization, oracle_action, receiver_action, score_action


SEAM = Path(__file__).resolve().parent
SIM_ROOT = SEAM.parents[1]
MANIFEST_PATH = SEAM / "demapper_replay_manifest.json"
SOURCE_MANIFEST_PATH = SEAM / "confirmation_manifest.json"
SOURCE_RAW_PATH = SEAM / "confirmation_raw.json"
RAW_PATH = SEAM / "demapper_replay_raw.json"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_authority(manifest: dict) -> tuple[dict, dict]:
    source = manifest["source"]
    if file_sha256(SOURCE_MANIFEST_PATH) != source["manifest_sha256"]:
        raise RuntimeError("source confirmation manifest hash changed")
    if file_sha256(SOURCE_RAW_PATH) != source["raw_sha256"]:
        raise RuntimeError("source confirmation raw hash changed")
    source_manifest = load_json(SOURCE_MANIFEST_PATH)
    source_raw = load_json(SOURCE_RAW_PATH)
    for relpath, expected in manifest["corrected_code_hashes"].items():
        path = SIM_ROOT / relpath if relpath.startswith("common/") else SEAM / relpath
        if file_sha256(path) != expected:
            raise RuntimeError(f"corrected replay code hash changed: {relpath}")
    if manifest["cells"] != source_manifest["cells"]:
        raise RuntimeError("source cell recipe changed")
    if manifest["arms"] != source_manifest["arms"]:
        raise RuntimeError("source arm recipe changed")
    if manifest["population"] != source_manifest["population"]:
        raise RuntimeError("source population changed")
    return source_manifest, source_raw


def _action(arm: str, parameter: float | None, realization: dict):
    if arm == "O1":
        return oracle_action(realization["h_true"], realization["y_payload"])
    return receiver_action(
        arm,
        realization["x_pilots"],
        realization["y_pilots"],
        realization["y_payload"],
        parameter,
    )


def _checked_equal(actual, expected, label: str) -> None:
    if actual != expected:
        raise RuntimeError(f"historical identity mismatch: {label}")


def build_window(source_cell: dict, manifest: dict, window_id: int) -> dict:
    source = source_cell["windows"][window_id]
    seed = int(source_cell["seed_base"]) + int(window_id)
    realization = make_realization(
        float(source_cell["snr_db"]),
        int(source_cell["pilot_symbols_per_polarization"]),
        seed,
        int(manifest["payload_symbols_per_polarization"]),
    )
    _checked_equal(seed, source["seed"], "seed")
    _checked_equal(float(realization["gain"]), float(source["gain"]), "gain")
    _checked_equal(realization["realization_hash"], source["realization_hash"], "realization_hash")
    _checked_equal(realization["observation_hash"], source["observation_hash"], "observation_hash")

    rows = []
    for source_row in source["rows"]:
        arm = str(source_row["arm"])
        parameter = source_row["parameter"]
        started = time.perf_counter_ns()
        action = _action(arm, parameter, realization)
        runtime_ns = time.perf_counter_ns() - started
        metrics = score_action(action, realization["bits"], realization["h_true"])
        for metric in ("channel_nmse", "inverse_residual", "rho"):
            if not np.isclose(metrics[metric], source_row[metric], rtol=0.0, atol=2e-15):
                raise RuntimeError(f"historical mechanism mismatch: {arm}/{metric}")
        if metrics["payload_bits"] != source_row["payload_bits"]:
            raise RuntimeError(f"historical payload mismatch: {arm}")
        rows.append(
            {
                "arm": arm,
                "parameter": parameter,
                **metrics,
                "action_sha256": hashlib.sha256(action_bytes(action)).hexdigest(),
                "runtime_ns": runtime_ns,
            }
        )
    return {
        "window_id": int(window_id),
        "seed": seed,
        "split": "demapper_replay",
        "gain": float(realization["gain"]),
        "realization_hash": realization["realization_hash"],
        "observation_hash": realization["observation_hash"],
        "payload_bits": int(rows[0]["payload_bits"]),
        "rows": rows,
    }


def identity_census(manifest: dict, source_raw: dict) -> dict[str, int]:
    census = {
        "expected_windows": 0,
        "matched_seeds": 0,
        "matched_gains": 0,
        "matched_realization_hashes": 0,
        "matched_observation_hashes": 0,
        "matched_payload_bits": 0,
        "matched_mechanism_rows": 0,
    }
    for source_cell in source_raw["cells"]:
        for window_id, source in enumerate(source_cell["windows"]):
            replay = build_window(source_cell, manifest, window_id)
            census["expected_windows"] += 1
            census["matched_seeds"] += replay["seed"] == source["seed"]
            census["matched_gains"] += replay["gain"] == source["gain"]
            census["matched_realization_hashes"] += replay["realization_hash"] == source["realization_hash"]
            census["matched_observation_hashes"] += replay["observation_hash"] == source["observation_hash"]
            census["matched_payload_bits"] += replay["payload_bits"] == source["rows"][0]["payload_bits"]
            census["matched_mechanism_rows"] += len(replay["rows"])
    return {key: int(value) for key, value in census.items()}


def build_raw(manifest: dict, source_raw: dict) -> dict:
    cells = []
    for source_cell in source_raw["cells"]:
        windows = [build_window(source_cell, manifest, i) for i in range(len(source_cell["windows"]))]
        cells.append({key: source_cell[key] for key in source_cell if key != "windows"} | {"windows": windows})
        print(f"{source_cell['cell_id']}: replayed {len(windows)} exact historical observations")
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=SEAM, capture_output=True, text=True, check=True).stdout.strip()
    return {
        "schema_version": "t083.demapper-replay-raw.v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "authority": manifest["authority"],
        "base_commit": commit,
        "control_epoch": manifest["control_epoch"],
        "mission_checkpoint": manifest["mission_checkpoint"],
        "manifest_sha256": file_sha256(MANIFEST_PATH),
        "source_hashes": {"manifest_sha256": file_sha256(SOURCE_MANIFEST_PATH), "raw_sha256": file_sha256(SOURCE_RAW_PATH)},
        "corrected_code_hashes": manifest["corrected_code_hashes"],
        "cells": cells,
    }


def main() -> int:
    from projects.simulation.common import save_results

    manifest = load_json(MANIFEST_PATH)
    _, source_raw = verify_authority(manifest)
    save_results(build_raw(manifest, source_raw), str(RAW_PATH), "t083_historical_observation_demapper_replay_raw")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
