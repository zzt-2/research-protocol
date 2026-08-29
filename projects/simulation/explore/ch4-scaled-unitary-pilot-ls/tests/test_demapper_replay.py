from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest


SEAM = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SEAM))


def _load(name: str):
    path = SEAM / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"t083_{name}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _manifest() -> dict:
    return json.loads((SEAM / "demapper_replay_manifest.json").read_text(encoding="utf-8"))


def _source_raw() -> dict:
    return json.loads((SEAM / "confirmation_raw.json").read_text(encoding="utf-8"))


def test_manifest_freezes_source_recipe_and_gate():
    manifest = _manifest()
    source_manifest = json.loads(
        (SEAM / "confirmation_manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["schema_version"] == "t083.demapper-replay.v1"
    assert manifest["authority"] == "T083/D062/V037"
    assert manifest["source"]["manifest"] == "confirmation_manifest.json"
    assert manifest["source"]["raw"] == "confirmation_raw.json"
    assert manifest["cells"] == source_manifest["cells"]
    assert manifest["arms"] == source_manifest["arms"]
    assert manifest["population"] == source_manifest["population"]
    assert manifest["bootstrap"] == {
        "rng": "PCG64",
        "seed": 2026083005,
        "resamples": 5000,
        "confidence": 0.95,
        "stream_rule": "reset seed for each named paired comparison",
    }
    assert manifest["gate"]["pooled_np2_ci_upper"] == "<0"
    assert manifest["gate"]["each_np4_ci_lower"] == "<=0"


def test_single_window_reconstructs_exact_historical_observation_and_mechanisms():
    runner = _load("run_demapper_replay")
    manifest = _manifest()
    source_cell = _source_raw()["cells"][0]
    replay = runner.build_window(source_cell, manifest, window_id=0)
    source = source_cell["windows"][0]

    assert replay["seed"] == source["seed"]
    assert replay["gain"] == source["gain"]
    assert replay["realization_hash"] == source["realization_hash"]
    assert replay["observation_hash"] == source["observation_hash"]
    assert replay["payload_bits"] == source["rows"][0]["payload_bits"]
    for new_row, old_row in zip(replay["rows"], source["rows"]):
        assert (new_row["arm"], new_row["parameter"]) == (
            old_row["arm"], old_row["parameter"]
        )
        for metric in ("channel_nmse", "inverse_residual", "rho"):
            assert new_row[metric] == pytest.approx(old_row[metric], rel=0, abs=2e-15)


def test_full_256_identity_census_without_writing_artifacts():
    runner = _load("run_demapper_replay")
    manifest = _manifest()
    census = runner.identity_census(manifest, _source_raw())
    assert census == {
        "expected_windows": 256,
        "matched_seeds": 256,
        "matched_gains": 256,
        "matched_realization_hashes": 256,
        "matched_observation_hashes": 256,
        "matched_payload_bits": 256,
        "matched_mechanism_rows": 1280,
    }


def test_paired_bootstrap_and_frozen_gate():
    reducer = _load("reduce_demapper_replay")
    result = reducer.paired_bootstrap(
        [0.01, 0.02, 0.03, 0.04],
        [0.02, 0.03, 0.04, 0.05],
        seed=2026083005,
        resamples=5000,
    )
    assert result["clusters"] == 4
    assert result["mean_diff"] == pytest.approx(-0.01)
    assert result["ci_upper"] < 0

    cells = [
        {"pilot_symbols_per_polarization": 2, "comparison": {"ci_lower": -1e-3}},
        {"pilot_symbols_per_polarization": 4, "comparison": {"ci_lower": -1e-3}},
        {"pilot_symbols_per_polarization": 2, "comparison": {"ci_lower": -1e-3}},
        {"pilot_symbols_per_polarization": 4, "comparison": {"ci_lower": 0.0}},
    ]
    assert reducer.classify_terminal(cells, {"ci_upper": -1e-4}) == "DEMAPPER_REPLAY_PASS"
    cells[-1]["comparison"]["ci_lower"] = 1e-6
    assert (
        reducer.classify_terminal(cells, {"ci_upper": -1e-4})
        == "DEMAPPER_CORRECTION_SIGNAL_LOST"
    )


def test_reducer_rejects_noncanonical_manifest_hash_and_ignores_old_aggregate():
    reducer = _load("reduce_demapper_replay")
    with pytest.raises(ValueError, match="manifest hash"):
        reducer.reduce_raw({"manifest_sha256": "wrong"}, _manifest(), "expected")
