"""Run exactly the preregistered T069 four-cell paired development batch."""

from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from development import make_realization, oracle_action, receiver_action, score_action
from development_reducer import select_tuned_parameter


SEAM = Path(__file__).resolve().parent
MANIFEST_PATH = SEAM / "development_manifest.json"
CORRECTNESS_PATH = SEAM / "correctness_receipt.json"
RAW_PATH = SEAM / "development_raw.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    return {
        "arm": arm,
        "parameter": parameter,
        **metrics,
        "runtime_ns": runtime_ns,
    }


def _window(cell: dict, manifest: dict, window_id: int, tuned: dict | None) -> dict:
    seed = int(cell["seed_base"]) + int(window_id)
    realization = make_realization(
        float(cell["snr_db"]),
        int(cell["pilot_symbols_per_polarization"]),
        seed,
        int(manifest["signal_model"]["payload_symbols_per_polarization"]),
    )
    split = "tune" if tuned is None else "evaluation"
    if split == "tune":
        recipes = [
            ("B0", None),
            *(("B1", float(value)) for value in manifest["arms"]["B1"]["eta_grid"]),
            *(("B2", float(value)) for value in manifest["arms"]["B2"]["tau_grid"]),
            ("C4", None),
            ("O1", None),
        ]
    else:
        recipes = [
            ("B0", None),
            ("B1", float(tuned["B1"])),
            ("B2", float(tuned["B2"])),
            ("C4", None),
            ("O1", None),
        ]
    return {
        "window_id": int(window_id),
        "seed": seed,
        "split": split,
        "gain": float(realization["gain"]),
        "realization_hash": realization["realization_hash"],
        "observation_hash": realization["observation_hash"],
        "rows": [_row(arm, parameter, realization) for arm, parameter in recipes],
    }


def _run_cell(cell: dict, manifest: dict) -> dict:
    tune_start, tune_stop = manifest["population"]["tune_offsets"]
    eval_start, eval_stop = manifest["population"]["evaluation_offsets"]
    windows = [
        _window(cell, manifest, window_id, None)
        for window_id in range(int(tune_start), int(tune_stop) + 1)
    ]
    tune_rows = {
        arm: [
            row
            for window in windows
            for row in window["rows"]
            if row["arm"] == arm
        ]
        for arm in ("B1", "B2")
    }
    tuned = {
        "B1": select_tuned_parameter(tune_rows["B1"], manifest["arms"]["B1"]["eta_grid"]),
        "B2": select_tuned_parameter(tune_rows["B2"], manifest["arms"]["B2"]["tau_grid"]),
    }
    windows.extend(
        _window(cell, manifest, window_id, tuned)
        for window_id in range(int(eval_start), int(eval_stop) + 1)
    )
    print(f"{cell['cell_id']}: tuned B1 eta={tuned['B1']}, B2 tau={tuned['B2']}")
    return {**cell, "tuned_parameters": tuned, "windows": windows}


def main() -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    correctness = json.loads(CORRECTNESS_PATH.read_text(encoding="utf-8"))
    manifest_sha256 = _sha256(MANIFEST_PATH)
    if not correctness.get("all_pass") or correctness.get("terminal") != "CORRECTNESS_PASS":
        raise RuntimeError("C0-C5 did not pass; BER is forbidden")
    if correctness["hashes"]["manifest_sha256"] != manifest_sha256:
        raise RuntimeError("manifest changed after correctness receipt; BER is forbidden")
    cells = [_run_cell(cell, manifest) for cell in manifest["cells"]]
    raw = {
        "schema_version": "t069.scaled-unitary-raw.v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "authority": manifest["authority"],
        "base_commit": correctness["base_commit"],
        "control_epoch": manifest["control_epoch"],
        "mission_checkpoint": manifest["mission_checkpoint"],
        "manifest_sha256": manifest_sha256,
        "correctness_receipt_sha256": _sha256(CORRECTNESS_PATH),
        "correctness": {
            "all_pass": correctness["all_pass"],
            "terminal": correctness["terminal"],
            "gates": correctness["gates"],
        },
        "cells": cells,
    }
    RAW_PATH.write_text(
        json.dumps(raw, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote raw-only artifact: {RAW_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
