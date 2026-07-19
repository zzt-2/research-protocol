from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pytest
import yaml


LAB_ROOT = Path(__file__).parents[1]
SCOUT_ROOT = LAB_ROOT / "scout" / "P03-U19-residual-headroom"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_probe_contract_freezes_exact_slice_budget_and_exit_rules() -> None:
    contract = yaml.safe_load((SCOUT_ROOT / "residual-headroom-probe-contract.v1.yaml").read_text(encoding="utf-8"))
    assert contract["mode"] == "SCOUT_DIAGNOSTIC_ONLY"
    assert contract["performance_experiment"] is False
    assert contract["b004"] is False
    assert contract["ml_training"] is False
    assert contract["queue_registry"] is False
    assert contract["seeds"] == list(range(11, 21))
    assert len(contract["seeds"]) == 10
    assert contract["n_symbols"] == 512
    assert contract["alpha"] == 4.2 and contract["beta"] == 1.4
    assert contract["csi_access_class"] == "CSI_NONE"
    assert contract["source_snapshot"]["target_sha256"] == "92eaa6a6c92e72122a1921a0c844160bbf5b4ee7bc2527fc66da468187af9786"
    assert contract["runtime_source_snapshot"].endswith("runtime-source-snapshot.v1.yaml")
    assert contract["definitions"]["analytic_coverage"]["threshold"] == 0.90
    assert set(contract["exit_states"]) == {
        "P03_ANALYTIC_COVERAGE_GE_90",
        "P03_RESIDUAL_MISMATCH_STABLE",
        "P03_RESIDUAL_UNSTABLE",
    }


def test_runtime_source_identity_is_stable_across_checkout_line_endings(tmp_path: Path) -> None:
    runner = _load(SCOUT_ROOT / "run_residual_headroom_probe.py", "p03_probe_line_endings_test")
    lf = tmp_path / "source-lf.py"
    crlf = tmp_path / "source-crlf.py"
    lf.write_bytes(b"x = 1\ny = 2\n")
    crlf.write_bytes(b"x = 1\r\ny = 2\r\n")
    assert runner._sha(lf) == runner._sha(crlf)
    assert runner._git_blob_oid(lf) == runner._git_blob_oid(crlf)


def test_runtime_affine_comparator_rejects_truth_and_is_deterministic() -> None:
    evaluator = _load(SCOUT_ROOT / "probe_evaluator.py", "p03_probe_evaluator_runtime_test")
    z_cal = np.asarray([[1 + 1j, -1 + 1j], [1 - 1j, -1 - 1j], [-1 + 1j, 1 + 1j]]) / np.sqrt(2)
    z_eval = z_cal.copy()
    first = evaluator.blind_affine_compare(z_cal, z_eval, ridge=1e-6)
    second = evaluator.blind_affine_compare(z_cal, z_eval, ridge=1e-6)
    np.testing.assert_array_equal(first["corrected"], second["corrected"])
    assert first["runtime_inputs"] == ["z_calibration", "z_evaluation", "known_QPSK_alphabet"]
    with pytest.raises(TypeError):
        evaluator.blind_affine_compare(z_cal, z_eval, ridge=1e-6, tx_truth=z_eval)


def test_fixed_and_pi_metrics_remain_semantically_separate_and_ser_is_reported() -> None:
    evaluator = _load(SCOUT_ROOT / "probe_evaluator.py", "p03_probe_evaluator_metric_test")
    rng = np.random.default_rng(47)
    sx = evaluator.hard_qpsk(rng.standard_normal(32) + 1j * rng.standard_normal(32))
    sy = evaluator.hard_qpsk(rng.standard_normal(32) + 1j * rng.standard_normal(32))
    metrics = evaluator.evaluate_dual_qpsk(sy, sx, sx, sy)
    assert metrics["fixed_label_ber"] > 0.0
    assert metrics["pi_ber"] == 0.0
    assert metrics["fixed_label_ser"] > 0.0
    assert metrics["pi_ser"] == 0.0


def test_scientific_classifier_has_exact_a_b_c_precedence() -> None:
    evaluator = _load(SCOUT_ROOT / "probe_evaluator.py", "p03_probe_evaluator_classifier_test")
    base = {
        "cell_count": 10,
        "cells_with_minimum_headroom": 8,
        "median_visible_headroom": 0.02,
        "residual_energy_cv": 0.2,
        "tail_mass_iqr": 0.05,
        "conditional_second_moment_max_cv": 0.4,
        "conditional_symbol_min_cell_support": 9,
    }
    assert evaluator.classify_probe(dict(base, aggregate_analytic_coverage=0.91))["primary_verdict"] == "P03_ANALYTIC_COVERAGE_GE_90"
    assert evaluator.classify_probe(dict(base, aggregate_analytic_coverage=0.50))["primary_verdict"] == "P03_RESIDUAL_MISMATCH_STABLE"
    unstable = dict(base, aggregate_analytic_coverage=0.50, residual_energy_cv=0.8)
    assert evaluator.classify_probe(unstable)["primary_verdict"] == "P03_RESIDUAL_UNSTABLE"


def test_probe_runner_uses_one_shared_standard_cma_output_and_reports_required_metrics(tmp_path: Path) -> None:
    runner = _load(SCOUT_ROOT / "run_residual_headroom_probe.py", "p03_probe_runner_test")
    result = runner.run(
        contract_path=SCOUT_ROOT / "residual-headroom-probe-contract.v1.yaml",
        output_dir=tmp_path / "probe",
    )
    assert result["source_equivalence"]["status"] == "PASS"
    assert result["summary"]["primary_verdict"] in {
        "P03_ANALYTIC_COVERAGE_GE_90",
        "P03_RESIDUAL_MISMATCH_STABLE",
        "P03_RESIDUAL_UNSTABLE",
    }
    assert len(result["cells"]) == 10
    for cell in result["cells"]:
        assert cell["standard_cma_calls"] == 1
        assert set(cell["metrics"]) == {"nearest_qpsk", "blind_affine", "oracle_affine_scoring_only"}
        for metrics in cell["metrics"].values():
            assert {"fixed_label_ber", "pi_ber", "fixed_label_ser", "pi_ser"}.issubset(metrics)
        assert set(cell["runtime_record"]) == {
            "seed", "sequence_id", "csi_access_class", "calibration_range", "evaluation_range",
            "nearest_residual", "blind_affine_residual",
        }
        assert "truth" not in str(cell["runtime_record"]).lower()
    assert result["guards"] == {
        "B001_B002_B003_modified": False,
        "B004_exists": False,
        "ML_trained": False,
        "queue_or_registry_created": False,
        "paper_material_written": False,
        "parameter_domain_expanded": False,
    }
    closure = yaml.safe_load((tmp_path / "probe" / "source-closure.yaml").read_text(encoding="utf-8"))
    snapshot = closure["immutable_probe_runtime_snapshot"]
    assert snapshot["manifest_git_blob_oid"]
    assert {row["path"] for row in snapshot["files"]} == {
        "run_residual_headroom_probe.py",
        "probe_evaluator.py",
        "run_source_equivalence.py",
        "residual-headroom-probe-contract.v1.yaml",
        "source-equivalence-contract.v1.yaml",
        "source-snapshots/interface-smoke-v2/source-snapshot.v1.yaml",
        "source-snapshots/interface-smoke-v2/gg-time-prefix-stability.patch",
    }
