"""Raw-only T083 reducer and frozen A1 terminal."""

from __future__ import annotations

import hashlib
import inspect
import json
from collections.abc import Mapping, Sequence
from pathlib import Path

import numpy as np

from development import receiver_action


SEAM = Path(__file__).resolve().parent
MANIFEST_PATH = SEAM / "demapper_replay_manifest.json"
SOURCE_MANIFEST_PATH = SEAM / "confirmation_manifest.json"
SOURCE_RAW_PATH = SEAM / "confirmation_raw.json"
RAW_PATH = SEAM / "demapper_replay_raw.json"
AGGREGATE_PATH = SEAM / "demapper_replay_aggregate.json"
RECEIPT_PATH = SEAM / "demapper_replay_receipt.json"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def paired_bootstrap(candidate: Sequence[float], baseline: Sequence[float], *, seed: int, resamples: int) -> dict:
    c = np.asarray(candidate, dtype=np.float64)
    b = np.asarray(baseline, dtype=np.float64)
    if c.ndim != 1 or c.shape != b.shape or c.size == 0 or not np.all(np.isfinite(c)) or not np.all(np.isfinite(b)):
        raise ValueError("paired finite one-dimensional BER arrays required")
    difference = c - b
    rng = np.random.Generator(np.random.PCG64(int(seed)))
    indices = rng.integers(0, difference.size, size=(int(resamples), difference.size), dtype=np.int64)
    boot = difference[indices].mean(axis=1)
    lower, upper = np.quantile(boot, [0.025, 0.975])
    return {
        "mean_diff": float(difference.mean()),
        "ci_lower": float(lower),
        "ci_upper": float(upper),
        "clusters": int(difference.size),
        "candidate_window_wins": int(np.count_nonzero(difference < 0.0)),
    }


def classify_terminal(cells: Sequence[Mapping], pooled_np2: Mapping) -> str:
    np4 = [cell for cell in cells if int(cell["pilot_symbols_per_polarization"]) == 4]
    if len(np4) != 2:
        raise ValueError("gate requires exactly two Np=4 cells")
    passed = float(pooled_np2["ci_upper"]) < 0.0 and all(float(cell["comparison"]["ci_lower"]) <= 0.0 for cell in np4)
    return "DEMAPPER_REPLAY_PASS" if passed else "DEMAPPER_CORRECTION_SIGNAL_LOST"


def _arm_rows(windows: Sequence[Mapping], arm: str) -> list[Mapping]:
    result = []
    for window in windows:
        matches = [row for row in window["rows"] if row["arm"] == arm]
        if len(matches) != 1:
            raise ValueError(f"expected exactly one {arm} row")
        result.append(matches[0])
    return result


def validate_raw(raw: Mapping, manifest: Mapping, manifest_sha256: str) -> dict[str, int]:
    if raw.get("manifest_sha256") != manifest_sha256:
        raise ValueError("demapper replay manifest hash mismatch")
    if raw.get("schema_version") != "t083.demapper-replay-raw.v1":
        raise ValueError("demapper replay raw schema mismatch")
    if file_sha256(SOURCE_MANIFEST_PATH) != manifest["source"]["manifest_sha256"] or file_sha256(SOURCE_RAW_PATH) != manifest["source"]["raw_sha256"]:
        raise ValueError("historical source hash mismatch")
    if raw.get("source_hashes") != {"manifest_sha256": manifest["source"]["manifest_sha256"], "raw_sha256": manifest["source"]["raw_sha256"]}:
        raise ValueError("raw historical source hash mismatch")
    source_raw = load_json(SOURCE_RAW_PATH)
    if len(raw.get("cells", [])) != 4:
        raise ValueError("replay cell count mismatch")
    census = {"expected_windows": 0, "matched_seeds": 0, "matched_gains": 0, "matched_realization_hashes": 0, "matched_observation_hashes": 0, "matched_payload_bits": 0, "matched_mechanism_rows": 0}
    for new_cell, old_cell, frozen_cell in zip(raw["cells"], source_raw["cells"], manifest["cells"]):
        for key in ("cell_id", "snr_db", "pilot_symbols_per_polarization", "seed_base", "b1_eta", "b2_tau"):
            if new_cell[key] != old_cell[key] or new_cell[key] != frozen_cell[key]:
                raise ValueError(f"cell authority mismatch: {key}")
        if len(new_cell["windows"]) != 64 or len(old_cell["windows"]) != 64:
            raise ValueError("window population mismatch")
        for new, old in zip(new_cell["windows"], old_cell["windows"]):
            census["expected_windows"] += 1
            for key, count_key in (("seed", "matched_seeds"), ("gain", "matched_gains"), ("realization_hash", "matched_realization_hashes"), ("observation_hash", "matched_observation_hashes")):
                if new[key] != old[key]:
                    raise ValueError(f"historical identity mismatch: {key}")
                census[count_key] += 1
            if new["split"] != "demapper_replay" or new["payload_bits"] != old["rows"][0]["payload_bits"]:
                raise ValueError("payload/split identity mismatch")
            census["matched_payload_bits"] += 1
            if len(new["rows"]) != len(old["rows"]):
                raise ValueError("arm row count mismatch")
            for new_row, old_row in zip(new["rows"], old["rows"]):
                if (new_row["arm"], new_row["parameter"]) != (old_row["arm"], old_row["parameter"]):
                    raise ValueError("arm recipe mismatch")
                errors, bits = int(new_row["bit_errors"]), int(new_row["payload_bits"])
                if bits != new["payload_bits"] or not 0 <= errors <= bits or float(new_row["ber"]) != errors / bits:
                    raise ValueError("BER count mismatch")
                for metric in ("channel_nmse", "inverse_residual", "rho"):
                    if not np.isclose(new_row[metric], old_row[metric], rtol=0.0, atol=2e-15):
                        raise ValueError(f"historical mechanism mismatch: {metric}")
                if not all(np.isfinite(float(new_row[key])) for key in ("ber", "channel_nmse", "inverse_residual", "rho", "runtime_ns")):
                    raise ValueError("nonfinite metric")
                census["matched_mechanism_rows"] += 1
    if census["expected_windows"] != 256 or census["matched_mechanism_rows"] != 1280:
        raise ValueError("identity census incomplete")
    return {key: int(value) for key, value in census.items()}


def _summary(rows: Sequence[Mapping]) -> dict:
    errors = sum(int(row["bit_errors"]) for row in rows)
    bits = sum(int(row["payload_bits"]) for row in rows)
    return {
        "bit_errors": errors,
        "payload_bits": bits,
        "ber": float(errors / bits),
        "channel_nmse": float(np.mean([row["channel_nmse"] for row in rows])),
        "inverse_residual": float(np.mean([row["inverse_residual"] for row in rows])),
        "rho": float(np.mean([row["rho"] for row in rows])),
    }


def reduce_raw(raw: Mapping, manifest: Mapping, manifest_sha256: str) -> dict:
    census = validate_raw(raw, manifest, manifest_sha256)
    bootstrap = manifest["bootstrap"]
    cells = []
    pooled_c4, pooled_b2 = [], []
    for raw_cell in raw["cells"]:
        rows = {arm: _arm_rows(raw_cell["windows"], arm) for arm in ("B0", "B1", "B2", "C4", "O1")}
        comparison = paired_bootstrap([r["ber"] for r in rows["C4"]], [r["ber"] for r in rows["B2"]], seed=bootstrap["seed"], resamples=bootstrap["resamples"])
        if raw_cell["pilot_symbols_per_polarization"] == 2:
            pooled_c4.extend(r["ber"] for r in rows["C4"])
            pooled_b2.extend(r["ber"] for r in rows["B2"])
        cells.append({
            "cell_id": raw_cell["cell_id"],
            "snr_db": raw_cell["snr_db"],
            "pilot_symbols_per_polarization": raw_cell["pilot_symbols_per_polarization"],
            "windows": len(raw_cell["windows"]),
            "arms": {arm: _summary(arm_rows) for arm, arm_rows in rows.items()},
            "comparison": comparison,
        })
    pooled = paired_bootstrap(pooled_c4, pooled_b2, seed=bootstrap["seed"], resamples=bootstrap["resamples"])
    terminal = classify_terminal(cells, pooled)
    return {
        "schema_version": "t083.demapper-replay-aggregate.v1",
        "authority": manifest["authority"],
        "manifest_sha256": manifest_sha256,
        "raw_schema_version": raw["schema_version"],
        "identity_census": census,
        "cells": cells,
        "pooled_np2": pooled,
        "decision": {"terminal": terminal, "difference": "BER_C4_minus_BER_B2", "next_step": "independent raw recomputation" if terminal == "DEMAPPER_REPLAY_PASS" else "stop Ch4 production"},
    }


def _combined_test_hash() -> str:
    digest = hashlib.sha256()
    for path in sorted((SEAM / "tests").glob("test_*.py")):
        digest.update(path.name.encode("utf-8")); digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> int:
    from projects.simulation.common import save_results

    manifest = load_json(MANIFEST_PATH)
    raw = load_json(RAW_PATH)
    manifest_hash = file_sha256(MANIFEST_PATH)
    aggregate = reduce_raw(raw, manifest, manifest_hash)
    save_results(aggregate, str(AGGREGATE_PATH), "t083_demapper_replay_raw_only_reducer")
    signature = tuple(inspect.signature(receiver_action).parameters)
    if signature != ("arm", "x_pilots", "y_pilots", "y_payload", "parameter"):
        raise RuntimeError("deployable receiver truth firewall changed")
    receipt = {
        "schema_version": "t083.demapper-replay-receipt.v1",
        "authority": manifest["authority"],
        "base_commit": raw["base_commit"],
        "control_epoch": manifest["control_epoch"],
        "mission_checkpoint": manifest["mission_checkpoint"],
        "checks": {"raw_only_reduction": "PASS", "source_hashes": "PASS", "identity_256_of_256": "PASS", "mechanism_identity_1280_of_1280": "PASS", "schema_and_counts": "PASS", "truth_firewall": "PASS"},
        "identity_census": aggregate["identity_census"],
        "bootstrap": manifest["bootstrap"],
        "decision": aggregate["decision"],
        "hashes": {"manifest_sha256": manifest_hash, "source_manifest_sha256": file_sha256(SOURCE_MANIFEST_PATH), "source_raw_sha256": file_sha256(SOURCE_RAW_PATH), "raw_sha256": file_sha256(RAW_PATH), "aggregate_sha256": file_sha256(AGGREGATE_PATH), "runner_sha256": file_sha256(SEAM / "run_demapper_replay.py"), "reducer_sha256": file_sha256(Path(__file__)), "tests_sha256": _combined_test_hash()},
    }
    save_results(receipt, str(RECEIPT_PATH), "t083_demapper_replay_receipt")
    print(json.dumps(receipt["decision"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
