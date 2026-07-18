from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path

import numpy as np
import pytest
import yaml


MODULE_PATH = Path(__file__).parents[1] / "tools" / "run_v2.py"
spec = importlib.util.spec_from_file_location("run_v2", MODULE_PATH)
run_v2 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(run_v2)


def _contract(**updates):
    result = {
        "n_symbols": 256, "block_size": 64, "alpha": 4.2, "beta": 1.4,
        "f_g_hz": 30.0, "snr_db": 20.0, "modulation": "QPSK",
        "cma_mu": 0.001, "cma_taps": 11, "rates": [4e-6, 1e-5],
        "train_seeds": [11], "test_seeds": [41], "eval_start": 0, "eval_end": 256,
        "channel_block": 100, "r2": 1.0, "fade_threshold_h": 0.1,
        "clip_norm": 1.0, "t_s": 1.0, "method": "standard-cma-godard-z",
    }
    result.update(updates)
    return result


def test_load_contract_requires_explicit_batch_id(tmp_path):
    queue = tmp_path / "queue.yaml"
    queue.write_text("batches:\n  - batch_id: B001\n    shared_contract: {}\n", encoding="utf-8")
    with pytest.raises(ValueError, match="batch_id is required"):
        run_v2.load_contract(queue)


def test_validate_contract_rejects_implicit_runtime_fields():
    contract = _contract()
    contract.pop("channel_block")
    with pytest.raises(ValueError, match="channel_block"):
        run_v2.validate_contract(contract)


def test_runtime_registry_preserves_declared_status():
    registry = {"x": {"id": "x", "status": "sandbox-candidate", "fingerprint": "abc"}}
    result = run_v2._runtime_registry(registry, ["x"])
    assert result["x"]["status"] == "sandbox-candidate"


def test_runtime_import_closure_includes_loaded_project_modules(tmp_path):
    module_path = tmp_path / "loaded_module.py"
    module_path.write_text("VALUE = 1\n", encoding="utf-8")
    module = importlib.util.module_from_spec(importlib.util.spec_from_file_location("loaded_for_closure", module_path))
    module.__file__ = str(module_path)
    run_v2.sys.modules["loaded_for_closure"] = module
    try:
        assert module_path.resolve() in run_v2._runtime_import_files([tmp_path])
    finally:
        run_v2.sys.modules.pop("loaded_for_closure", None)


def test_validate_contract_rejects_seed_overlap_and_non_qpsk():
    with pytest.raises(ValueError, match="overlap"):
        run_v2.validate_contract(_contract(test_seeds=[11]))
    with pytest.raises(ValueError, match="QPSK"):
        run_v2.validate_contract(_contract(modulation="16QAM"))


def test_generator_adapter_passes_linear_snr_and_checks_constellation():
    calls = []

    def generator(n, alpha, beta, f_g, sop_rate, seed, gamma_bar=None, block=None):
        calls.append(gamma_bar)
        s = np.ones(n, dtype=complex) * (1 + 1j) / np.sqrt(2)
        return {"sX": s, "sY": s}

    wrapped = run_v2._generator_adapter(generator, _contract())
    wrapped(4, 1, 1, 1, 1, 1, 1)
    assert calls == [100.0]


def test_generator_adapter_rejects_legacy_generator_without_explicit_gamma():
    def legacy_generator(n, alpha, beta, f_g, rate, seed, block):
        return {"sX": np.ones(n), "sY": np.ones(n)}

    with pytest.raises(TypeError, match="sop_rate|gamma_bar"):
        run_v2._generator_adapter(legacy_generator, _contract())


def test_source_closure_contains_dynamic_common_helpers_and_controller(tmp_path):
    queue = tmp_path / "queue.yaml"
    mapping = tmp_path / "map.yaml"
    registry = tmp_path / "registry.yaml"
    for path in (queue, mapping, registry):
        path.write_text("{}", encoding="utf-8")
    files = {path.name for path in run_v2._source_files(run_v2.SOURCE_ROOT, queue, mapping, registry)}
    assert {"__init__.py", "_channel.py", "_modulation.py", "_recovery.py", "_kf.py"}.issubset(files)
    assert "controller.py" in files
    assert "run_b001.py" in files
    assert "unlabeled_control_reconstruction.py" in files


def test_v2_autoencoder_public_apis_have_no_event_label_argument():
    path = Path(__file__).parents[1] / "tools" / "unlabeled_control_reconstruction.py"
    module_spec = importlib.util.spec_from_file_location("unlabeled_ae", path)
    module = importlib.util.module_from_spec(module_spec)
    assert module_spec.loader is not None
    module_spec.loader.exec_module(module)
    assert list(inspect.signature(module.UnlabeledControlReconstructionDetector.fit).parameters) == ["self", "x", "cell_ids"]
    assert list(inspect.signature(module.calibrate_unlabeled_cell_threshold).parameters) == ["scores", "cell_ids", "false_alarm_budget"]
    x = np.tile(np.array([[0.1, 0.2], [0.2, 0.1]], dtype=float), (5, 1))
    ids = np.array(["a", "a", "b", "b", "c", "c", "d", "d", "e", "e"])
    detector = module.UnlabeledControlReconstructionDetector(min_samples=2).fit(x, ids)
    assert detector.status == "FIT"
    scores = detector.predict_proba(x)
    result = module.calibrate_unlabeled_cell_threshold(scores, ids, 0.2)
    assert result["status"] == "CALIBRATED"


def test_v2_dataset_uses_unlabeled_autoencoder_path():
    def generator(n, alpha, beta, f_g, sop_rate, seed, gamma_bar=None, block=None):
        assert gamma_bar == 100.0
        s = np.ones(n, dtype=complex) * (1 + 1j) / np.sqrt(2)
        return {"rX": s, "rY": s, "sX": s, "sY": s, "h": np.ones(n)}

    def baseline(realization, cfg, variant="baseline", return_blind_trace=True):
        trace = [{"output_start": start, "cm_error": 0.1 + start / 256.0,
                  "output_power": 1.0, "update_norm": 0.01}
                 for start in range(0, 256, 64)]
        return {"zX": realization["sX"], "zY": realization["sY"],
                "valid_mask": np.ones(256, dtype=bool), "blind_trace": trace,
                "diverged": False, "divergence_symbol": None}

    result = run_v2.run_dataset(_contract(), realization_generator=generator,
                                baseline_runner=baseline)
    assert set(result["detectors"]) == {"logistic", "mlp", "autoencoder"}
    assert result["detectors"]["autoencoder"]["threshold_source"].startswith("unlabeled-")


def test_v2_governed_run_requires_static_registry_match(tmp_path):
    root = Path(__file__).parents[1]
    queue = tmp_path / "batch-queue.v2.yaml"
    mapping = tmp_path / "candidate-map.v2.yaml"
    registry = tmp_path / "component-registry.v2.yaml"
    queue.write_text((root / "batch-queue.yaml").read_text(encoding="utf-8")
                     .replace("n_symbols: 100000", "n_symbols: 256")
                     .replace("train_seeds: [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]", "train_seeds: [11]")
                     .replace("test_seeds: [41, 42, 43, 44, 45]", "test_seeds: [41]")
                     .replace("      rates: [0.000004, 0.00001]", "      rates: [0.000004, 0.00001]\n      channel_block: 100\n      r2: 1.0\n      fade_threshold_h: 0.1\n      clip_norm: 1.0\n      t_s: 1.0\n      method: standard-cma-godard-z"), encoding="utf-8")
    mapping.write_text((root / "candidate-map.v2.yaml").read_text(encoding="utf-8").replace("status: GATE_PENDING", "status: PASS").replace("verdict: PENDING", "verdict: PASS"), encoding="utf-8")
    registry_doc = yaml.safe_load((root / "component-registry.v2.yaml").read_text(encoding="utf-8"))
    next(item for item in registry_doc["components"] if item["id"] == "runner.direction_lab.replacement-v2")["fingerprint"] = run_v2._sha256(run_v2.HERE)
    registry.write_text(yaml.safe_dump(registry_doc, sort_keys=False), encoding="utf-8")

    def generator(n, alpha, beta, f_g, sop_rate, seed, gamma_bar=None, block=None):
        s = np.ones(n, dtype=complex) * (1 + 1j) / np.sqrt(2)
        return {"rX": s, "rY": s, "sX": s, "sY": s, "h": np.ones(n)}

    def baseline(realization, cfg, variant="baseline", return_blind_trace=True):
        trace = [{"output_start": start, "cm_error": 0.1 + start / 256.0,
                  "output_power": 1.0, "update_norm": 0.01}
                 for start in range(0, 256, 64)]
        return {"zX": realization["sX"], "zY": realization["sY"],
                "valid_mask": np.ones(256, dtype=bool), "blind_trace": trace,
                "diverged": False, "divergence_symbol": None}

    accepted = run_v2.run_governed(queue_path=queue, batch_id="B001", output_dir=tmp_path / "accepted",
                                   realization_generator=generator, baseline_runner=baseline,
                                   allow_test_doubles=True)
    assert accepted["gate"]["accepted"] is True
    assert accepted["manifest"]["execution_mode"] == "TEST_DOUBLE"
    assert accepted["manifest"]["test_only"] is True
    status_doc = yaml.safe_load((tmp_path / "accepted" / "execution-status.yaml").read_text(encoding="utf-8"))
    assert status_doc["batch_id"] == "B001"
    assert status_doc["status"] == "COMPLETED_SANDBOX"
    with pytest.raises(RuntimeError, match="registry"):
        document = yaml.safe_load(registry.read_text(encoding="utf-8"))
        next(item for item in document["components"] if item["id"] == "component.ml_degradation_detector.batch-v2")["fingerprint"] = "deadbeef"
        registry.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
        run_v2.run_governed(queue_path=queue, batch_id="B001", output_dir=tmp_path,
                            realization_generator=generator, baseline_runner=baseline,
                            allow_test_doubles=True)


def test_v2_governed_rejects_injected_execution_objects_by_default(tmp_path):
    with pytest.raises(RuntimeError, match="test-only"):
        run_v2.run_governed(queue_path=tmp_path / "missing.yaml", output_dir=tmp_path,
                            realization_generator=lambda: None, baseline_runner=lambda: None)


def test_v2_governed_rejects_even_empty_contract_override(tmp_path):
    with pytest.raises(RuntimeError, match="contract_override"):
        run_v2.run_governed(queue_path=tmp_path / "missing.yaml", output_dir=tmp_path,
                            contract_override={})


def test_v2_default_production_uses_real_generator_and_standard_cma(tmp_path):
    root = Path(__file__).parents[1]
    queue = tmp_path / "batch-queue.v2.yaml"
    mapping = tmp_path / "candidate-map.v2.yaml"
    registry = tmp_path / "component-registry.v2.yaml"
    queue.write_text((root / "batch-queue.yaml").read_text(encoding="utf-8")
                     .replace("n_symbols: 100000", "n_symbols: 256")
                     .replace("train_seeds: [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]", "train_seeds: [11]")
                     .replace("test_seeds: [41, 42, 43, 44, 45]", "test_seeds: [41]")
                     .replace("      rates: [0.000004, 0.00001]", "      rates: [0.000004, 0.00001]\n      channel_block: 100\n      r2: 1.0\n      fade_threshold_h: 0.1\n      clip_norm: 1.0\n      t_s: 1.0\n      method: standard-cma-godard-z"), encoding="utf-8")
    mapping.write_text((root / "candidate-map.v2.yaml").read_text(encoding="utf-8").replace("status: GATE_PENDING", "status: PASS").replace("verdict: PENDING", "verdict: PASS"), encoding="utf-8")
    registry_doc = yaml.safe_load((root / "component-registry.v2.yaml").read_text(encoding="utf-8"))
    next(item for item in registry_doc["components"] if item["id"] == "runner.direction_lab.replacement-v2")["fingerprint"] = run_v2._sha256(run_v2.HERE)
    registry.write_text(yaml.safe_dump(registry_doc, sort_keys=False), encoding="utf-8")
    result = run_v2.run_governed(queue_path=queue, batch_id="B001", output_dir=tmp_path / "production")
    assert result["gate"]["accepted"] is True
    assert result["manifest"]["execution_mode"] == "PRODUCTION"
    assert result["manifest"]["test_only"] is False
    assert "metric.dual_qpsk.fixed-plus-pi.v1" in result["manifest"]["execution_component_ids"]
