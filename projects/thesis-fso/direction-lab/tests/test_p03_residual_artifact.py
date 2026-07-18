from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pytest


LAB_ROOT = Path(__file__).parents[1]
SCOUT_ROOT = LAB_ROOT / "scout" / "P03-U19-residual-headroom"


def _load(path: Path, name: str):
    assert path.is_file(), f"required component is absent: {path}"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _modules():
    adapter = _load(SCOUT_ROOT / "z_window_adapter.py", "p03_adapter_for_residual_test")
    comparator = _load(SCOUT_ROOT / "analytic_comparator.py", "p03_comparator_for_residual_test")
    residual = _load(SCOUT_ROOT / "residual_artifact.py", "p03_residual_artifact_test")
    return adapter, comparator, residual


def _cell(sequence_id: str, offset: float = 0.0) -> dict:
    adapter, comparator, _ = _modules()
    z_x = np.asarray([0.7 + 0.6j, -0.8 + 0.7j, -0.7 - 0.9j, 0.9 - 0.6j]) + offset
    z_y = z_x[::-1].copy()
    output = {
        "zX": z_x,
        "zY": z_y,
        "valid_mask": np.ones(4, dtype=bool),
        "blind_trace": [{"output_start": 30, "output_end": 34}],
        "diverged": False,
        "divergence_symbol": None,
        "provenance": {"implementation": "test-standard-cma"},
    }
    window = adapter.adapt_standard_cma_output(
        output,
        sequence_id=sequence_id,
        symbol_start=30,
        symbol_end=34,
        equalizer_taps=11,
        csi_access_class="CSI_NONE",
        source_id="standard-cma-test-seam",
        source_hash="a" * 64,
        receiver_estimated_csi=None,
    )
    analytic = comparator.compare_qpsk_csi_none(
        window, constellation_amplitude=1.0 / np.sqrt(2.0)
    )
    return {"z_window": window, "comparator": analytic}


def _build(cells: list[dict], evaluation: list[dict | None]):
    _, _, residual = _modules()
    return residual.build_residual_artifact(
        cells,
        tail_energy_threshold=0.25,
        evaluation_metrics_by_cell=evaluation,
        valid_domain={
            "scenario": "dual-pol ground-space OSL",
            "receiver": "standard-CMA",
            "modulation": "QPSK",
            "csi_access_class": "CSI_NONE",
            "purpose": "deterministic interface smoke only",
        },
        source_hashes={
            "standard_cma_runner": "1" * 64,
            "z_window_adapter": "2" * 64,
            "analytic_comparator": "3" * 64,
        },
    )


def test_residual_artifact_has_fixed_schema_moments_tail_and_one_cell_status() -> None:
    artifact = _build([_cell("cell-1")], [None])
    assert artifact["schema_version"] == "direction-lab.p03-residual-artifact.v1"
    assert artifact["role"] == "SCOUT_INTERFACE_DIAGNOSTIC_NOT_PERFORMANCE"
    assert artifact["residual_definition"] == "receiver_visible_z_minus_analytic_comparator_predicted_mean"
    assert artifact["csi_access_class"] == "CSI_NONE"
    assert artifact["tail"]["energy_threshold"] == 0.25
    assert 0.0 <= artifact["tail"]["mass"] <= 1.0
    assert artifact["cross_cell_stability"]["status"] == "NOT_ESTIMABLE_ONE_CELL"
    assert artifact["evaluation_only"]["fixed_label_ber"]["status"] == "NOT_COMPUTED_INTERFACE_SMOKE"
    assert artifact["evaluation_only"]["pi_ber"]["status"] == "NOT_COMPUTED_INTERFACE_SMOKE"
    for polarization in ("zX", "zY"):
        assert artifact["conditional_moments"][polarization]
        for stats in artifact["conditional_moments"][polarization].values():
            assert stats["count"] >= 1
            assert np.asarray(stats["real_imag_covariance"]).shape == (2, 2)
            assert np.isfinite(stats["second_abs_moment"])
            assert np.isfinite(stats["fourth_abs_moment"])


def test_evaluation_metrics_are_separate_and_do_not_change_runtime_hash() -> None:
    cell = _cell("cell-1")
    without_truth = _build([cell], [None])
    with_truth_a = _build([cell], [{"fixed_label_ber": 0.25, "pi_ber": 0.125}])
    with_truth_b = _build([cell], [{"fixed_label_ber": 0.5, "pi_ber": 0.375}])
    assert without_truth["runtime_artifact_hash"] == with_truth_a["runtime_artifact_hash"]
    assert with_truth_a["runtime_artifact_hash"] == with_truth_b["runtime_artifact_hash"]
    assert with_truth_a["evaluation_only"]["fixed_label_ber"]["values"] == [0.25]
    assert with_truth_a["evaluation_only"]["pi_ber"]["values"] == [0.125]
    assert with_truth_a["evaluation_only"]["fixed_label_ber"] != with_truth_a["evaluation_only"]["pi_ber"]


def test_cross_cell_stability_is_computable_but_not_promoted_to_performance() -> None:
    artifact = _build([_cell("cell-1"), _cell("cell-2", offset=0.02)], [None, None])
    stability = artifact["cross_cell_stability"]
    assert stability["status"] == "ESTIMATED"
    assert stability["cell_count"] == 2
    assert np.isfinite(stability["coefficient_of_variation_mean_residual_energy"])
    assert artifact["interpretation_limit"] == "nonzero_residual_does_not_establish_ml_headroom"


def test_builder_fails_closed_on_inline_evaluation_fields_or_alignment_mismatch() -> None:
    cell = _cell("cell-1")
    contaminated = dict(cell, fixed_label_ber=0.1)
    with pytest.raises(ValueError, match="runtime cell fields"):
        _build([contaminated], [None])
    mismatched = _cell("cell-2")
    mismatched["comparator"] = dict(mismatched["comparator"], sequence_id="wrong")
    with pytest.raises(ValueError, match="align"):
        _build([mismatched], [None])


def test_builder_rejects_unbound_oracle_comparator_identity() -> None:
    cell = _cell("cell-1")
    cell["comparator"] = dict(cell["comparator"], comparator_id="oracle.illegal.v1")
    with pytest.raises(ValueError, match="comparator_id"):
        _build([cell], [None])


def test_all_contract_values_are_explicit_and_validated() -> None:
    _, _, residual = _modules()
    cell = _cell("cell-1")
    with pytest.raises(TypeError):
        residual.build_residual_artifact([cell])
    with pytest.raises(ValueError, match="threshold"):
        residual.build_residual_artifact(
            [cell],
            tail_energy_threshold=-1.0,
            evaluation_metrics_by_cell=[None],
            valid_domain={"scenario": "x"},
            source_hashes={"adapter": "1" * 64},
        )
    with pytest.raises(ValueError, match="source hash"):
        residual.build_residual_artifact(
            [cell],
            tail_energy_threshold=0.25,
            evaluation_metrics_by_cell=[None],
            valid_domain={"scenario": "x"},
            source_hashes={"adapter": "not-a-hash"},
        )
