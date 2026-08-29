from __future__ import annotations

import hashlib
import importlib.util
import inspect
import json
import sys
from pathlib import Path


SEAM = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SEAM))


def _load(name: str):
    path = SEAM / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"t071_{name}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _comparison(mean: float, lower: float, upper: float) -> dict[str, float]:
    return {"mean_diff": mean, "ci_lower": lower, "ci_upper": upper}


def _cell(n_pilots: int, comparison: dict[str, float]) -> dict:
    return {
        "pilot_symbols_per_polarization": n_pilots,
        "comparisons": {"C4_vs_B2": comparison},
    }


def test_manifest_freezes_t071_recipe_and_development_hashes():
    manifest = json.loads((SEAM / "confirmation_manifest.json").read_text(encoding="utf-8"))

    assert manifest["schema_version"] == "t071.scaled-unitary-confirmation.v1"
    assert manifest["mission_checkpoint"] == "CP012"
    assert [cell["cell_id"] for cell in manifest["cells"]] == [
        "snr14_np2",
        "snr14_np4",
        "snr18_np2",
        "snr18_np4",
    ]
    assert [cell["seed_base"] for cell in manifest["cells"]] == [7000, 7100, 7200, 7300]
    assert [cell["b1_eta"] for cell in manifest["cells"]] == [0.01, 0.001, 0.001, 0.01]
    assert [cell["b2_tau"] for cell in manifest["cells"]] == [1.0, 1.0, 1.0, 1.0]
    assert manifest["population"] == {"windows_per_cell": 64, "split": "confirmation"}
    assert manifest["bootstrap"] == {
        "rng": "PCG64",
        "seed": 2026083004,
        "resamples": 2000,
        "confidence": 0.95,
        "stream_rule": "reset seed for each named paired comparison",
    }
    for name, digest in manifest["frozen_development_hashes"].items():
        assert digest == _sha256(SEAM / name)


def test_confirmation_artifact_line_endings_are_checkout_stable():
    attributes = (SEAM / ".gitattributes").read_text(encoding="utf-8").splitlines()

    assert "confirmation_manifest.json text eol=lf" in attributes
    for name in (
        "confirmation_raw.json",
        "confirmation_aggregate.json",
        "confirmation_receipt.json",
    ):
        assert f"{name} text eol=crlf" in attributes


def test_confirmation_runner_is_fixed_recipe_and_truth_firewalled():
    runner = _load("run_confirmation")
    development = _load("development")
    manifest = json.loads((SEAM / "confirmation_manifest.json").read_text(encoding="utf-8"))
    cell = dict(manifest["cells"][0])
    small_manifest = json.loads(json.dumps(manifest))
    small_manifest["signal_model"]["payload_symbols_per_polarization"] = 32

    window = runner.build_window(cell, small_manifest, window_id=0)

    assert window["seed"] == 7000
    assert window["split"] == "confirmation"
    assert [(row["arm"], row["parameter"]) for row in window["rows"]] == [
        ("B0", None),
        ("B1", 0.01),
        ("B2", 1.0),
        ("C4", None),
        ("O1", None),
    ]
    assert tuple(inspect.signature(development.receiver_action).parameters) == (
        "arm",
        "x_pilots",
        "y_pilots",
        "y_payload",
        "parameter",
    )


def test_frozen_terminal_classifier_covers_all_three_scientific_terminals():
    reducer = _load("confirmation_reducer")

    confirmed_cells = [
        _cell(2, _comparison(-0.003, -0.005, -0.001)),
        _cell(4, _comparison(-0.001, -0.002, 0.001)),
        _cell(2, _comparison(-0.002, -0.004, 0.0002)),
        _cell(4, _comparison(0.0001, -0.001, 0.001)),
    ]
    assert reducer.classify_terminal(
        confirmed_cells, _comparison(-0.0025, -0.004, -0.0005)
    ) == "C4_CONFIRMED_STRUCTURED_SIGNAL"

    local_cells = [
        _cell(2, _comparison(-0.002, -0.004, -0.0002)),
        _cell(4, _comparison(0.0, -0.001, 0.001)),
        _cell(2, _comparison(0.001, -0.001, 0.003)),
        _cell(4, _comparison(0.0, -0.001, 0.001)),
    ]
    assert reducer.classify_terminal(
        local_cells, _comparison(-0.0005, -0.002, 0.001)
    ) == "C4_CONFIRMATION_LOCAL_ONLY"

    no_signal_cells = [
        _cell(2, _comparison(0.001, -0.001, 0.003)),
        _cell(4, _comparison(0.0, -0.001, 0.001)),
        _cell(2, _comparison(0.001, -0.001, 0.003)),
        _cell(4, _comparison(0.0, -0.001, 0.001)),
    ]
    assert reducer.classify_terminal(
        no_signal_cells, _comparison(0.001, -0.001, 0.003)
    ) == "C4_NOT_CONFIRMED"


def test_significant_reverse_result_cannot_be_local_only():
    reducer = _load("confirmation_reducer")
    cells = [
        _cell(2, _comparison(-0.002, -0.004, -0.0002)),
        _cell(4, _comparison(0.002, 0.0001, 0.004)),
        _cell(2, _comparison(-0.001, -0.003, 0.001)),
        _cell(4, _comparison(0.0, -0.001, 0.001)),
    ]

    assert reducer.classify_terminal(
        cells, _comparison(-0.0015, -0.003, -0.0001)
    ) == "C4_NOT_CONFIRMED"


def test_pooled_np2_bootstrap_uses_all_128_paired_windows():
    reducer = _load("confirmation_reducer")
    candidate = [0.01] * 64 + [0.02] * 64
    baseline = [0.012] * 64 + [0.023] * 64

    result = reducer.paired_bootstrap(candidate, baseline, seed=2026083004, resamples=2000)

    assert result["clusters"] == 128
    assert result["mean_diff"] < 0.0
    assert result["ci_upper"] < 0.0
