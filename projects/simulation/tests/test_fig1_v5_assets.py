"""Deterministic contract tests for the Fig. 1 v5 miniature assets."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
import subprocess
import sys
from xml.etree import ElementTree

import numpy as np
from PIL import Image


MODULE = "figures.fig1_v5_assets.generate_assets"
SVG_NAMES = (
    "constellation.svg",
    "block_fading.svg",
    "carrier_phase.svg",
    "awgn_iq.svg",
    "received_signal.svg",
)
ALL_NAMES = (*SVG_NAMES, "decision_regions.png", "manifest.json")


def _module():
    return importlib.import_module(MODULE)


def test_build_asset_data_uses_16apsk_and_fixed_realization_length():
    data = _module().build_asset_data()

    assert len(data["constellation"]) == 16
    assert len(np.unique(data["constellation"])) == 16
    assert len(data["h"]) == len(data["phi"]) == len(data["noise"]) == 256
    assert len(data["rx_raw"]) == 256


def test_block_fading_changes_only_at_100_and_200():
    h = _module().build_asset_data()["h"]
    change_points = np.flatnonzero(np.diff(h) != 0) + 1

    assert change_points.tolist() == [100, 200]
    assert [100, 100, len(h) - 200] == [100, 100, 56]


def test_noise_exactly_reconstructs_received_samples():
    data = _module().build_asset_data()
    reconstructed = (
        data["tx"]
        * np.sqrt(data["h"])
        * np.exp(1j * data["phi"])
        + data["noise"]
    )

    assert np.max(np.abs(reconstructed - data["rx_raw"])) < 1e-12


def test_decision_grid_contains_all_16_labels():
    labels = _module().build_asset_data()["decision_labels"]

    assert labels.shape == (401, 401)
    assert len(np.unique(labels)) >= 16


def test_render_assets_writes_parseable_self_contained_outputs(tmp_path: Path):
    _module().render_assets(tmp_path)

    assert {path.name for path in tmp_path.iterdir()} == set(ALL_NAMES)
    for name in SVG_NAMES:
        root = ElementTree.parse(tmp_path / name).getroot()
        assert root.attrib["viewBox"]
        local_names = {node.tag.rsplit("}", 1)[-1] for node in root.iter()}
        assert "text" not in local_names
        assert "foreignObject" not in local_names
        for node in root.iter():
            for attribute, value in node.attrib.items():
                if attribute.rsplit("}", 1)[-1] == "href":
                    assert value.startswith("#")

    with Image.open(tmp_path / "decision_regions.png") as image:
        assert image.width >= 400
        assert image.height >= 400

    manifest = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["provenance"] == {
        "purpose": "mechanism-only figure asset",
        "paper_result": False,
    }
    assert manifest["fixed_inputs"] == {
        "N": 256,
        "snr_db": 15.0,
        "scene": "moderate",
        "seed": 2000,
        "f_dot_source": "SimulationConfig().doppler.DOPPLER_HIGH",
    }
    assert set(manifest["source_files"]) == {
        "common/_modulation.py",
        "common/_channel.py",
        "params.py",
        "figures/fig1_v5_assets/generate_assets.py",
    }
    assert set(manifest["assets"]) == set(SVG_NAMES) | {"decision_regions.png"}
    assert all(entry["role"] for entry in manifest["assets"].values())
    received = manifest["assets"]["received_signal.svg"]
    assert received["source_data"] == "rx_raw"
    assert received["realization"] == "same fixed realization"


def test_script_entrypoint_runs_from_simulation_root():
    simulation_root = Path(__file__).resolve().parents[1]
    script = simulation_root / "figures" / "fig1_v5_assets" / "generate_assets.py"

    completed = subprocess.run(
        [sys.executable, str(script)],
        cwd=simulation_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
