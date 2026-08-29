"""Run exactly one T071 fixed-recipe fresh confirmation batch."""

from __future__ import annotations

import hashlib
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

from development import make_realization, oracle_action, receiver_action, score_action


SEAM = Path(__file__).resolve().parent
MANIFEST_PATH = SEAM / "confirmation_manifest.json"
RAW_PATH = SEAM / "confirmation_raw.json"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_frozen_development(manifest: dict) -> None:
    for name, expected in manifest["frozen_development_hashes"].items():
        actual = file_sha256(SEAM / name)
        if actual != expected:
            raise RuntimeError(f"frozen development artifact changed: {name}")


def _row(arm: str, parameter: float | None, realization: dict) -> dict:
    started = time.perf_counter_ns()
    if arm == "O1":
        action = oracle_action(realization["h_true"], realization["y_payload"])
    else:
        action = receiver_action(
            arm,
            realization["x_pilots"],
            realization["y_pilots"],
            realization["y_payload"],
            parameter,
        )
    runtime_ns = time.perf_counter_ns() - started
    metrics = score_action(action, realization["bits"], realization["h_true"])
    return {"arm": arm, "parameter": parameter, **metrics, "runtime_ns": runtime_ns}


def build_window(cell: dict, manifest: dict, window_id: int) -> dict:
    seed = int(cell["seed_base"]) + int(window_id)
    realization = make_realization(
        float(cell["snr_db"]),
        int(cell["pilot_symbols_per_polarization"]),
        seed,
        int(manifest["signal_model"]["payload_symbols_per_polarization"]),
    )
    recipes = [
        ("B0", None),
        ("B1", float(cell["b1_eta"])),
        ("B2", float(cell["b2_tau"])),
        ("C4", None),
        ("O1", None),
    ]
    return {
        "window_id": int(window_id),
        "seed": seed,
        "split": "confirmation",
        "gain": float(realization["gain"]),
        "realization_hash": realization["realization_hash"],
        "observation_hash": realization["observation_hash"],
        "rows": [_row(arm, parameter, realization) for arm, parameter in recipes],
    }


def build_raw(manifest: dict) -> dict:
    verify_frozen_development(manifest)
    windows_per_cell = int(manifest["population"]["windows_per_cell"])
    cells = []
    for cell in manifest["cells"]:
        windows = [build_window(cell, manifest, index) for index in range(windows_per_cell)]
        cells.append({**cell, "windows": windows})
        print(f"{cell['cell_id']}: completed {windows_per_cell} fixed confirmation windows")
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=SEAM,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    return {
        "schema_version": "t071.scaled-unitary-confirmation-raw.v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "authority": manifest["authority"],
        "base_commit": commit,
        "control_epoch": manifest["control_epoch"],
        "mission_checkpoint": manifest["mission_checkpoint"],
        "manifest_sha256": file_sha256(MANIFEST_PATH),
        "frozen_development_hashes": manifest["frozen_development_hashes"],
        "cells": cells,
    }


def main() -> int:
    from projects.simulation.common import save_results

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    raw = build_raw(manifest)
    save_results(raw, str(RAW_PATH), "t071_scaled_unitary_fixed_confirmation_raw")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
