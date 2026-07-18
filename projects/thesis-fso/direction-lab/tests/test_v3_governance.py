from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import sys
from pathlib import Path

import pytest
import numpy as np
import yaml


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "batch-queue.v3.yaml"
REGISTRY = ROOT / "component-registry.v3.yaml"
RUNNER = ROOT / "tools" / "run_v3.py"
VALIDATOR_PATH = ROOT / "tools" / "validate_batch_queue.py"


def _load_validator():
    spec = importlib.util.spec_from_file_location("direction_lab_queue_gate_v3", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _queue():
    return yaml.safe_load(QUEUE.read_text(encoding="utf-8"))


def test_v3_snapshot_binds_explicit_runtime_contract_and_current_runner():
    queue = _queue()
    shared = queue["batches"][0]["shared_contract"]
    required = {"channel_block", "r2", "fade_threshold_h", "clip_norm", "t_s", "method"}
    assert required <= set(shared)
    assert queue["queue_gate"]["runner"] == "projects/thesis-fso/direction-lab/tools/run_v3.py:run_governed"
    actual = hashlib.sha256(RUNNER.read_bytes()).hexdigest()
    assert queue["queue_gate"]["runner_sha256"] == actual
    assert queue["queue_gate"]["registry_sha256"] == hashlib.sha256(REGISTRY.read_bytes()).hexdigest()


def test_v3_registry_binds_direct_runtime_helpers_and_controller():
    registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    entries = {item["id"]: item for item in registry["components"]}
    expected = {
        "runner.direction_lab.replacement-v2-helper": ROOT / "tools" / "run_v2.py",
        "runner.direction_lab.legacy-b001-helper": ROOT / "tools" / "run_b001.py",
        "validator.direction_lab.queue-gate-v3": ROOT / "tools" / "validate_batch_queue.py",
        "controller.direction_lab.pilot-v3": ROOT.parents[2] / "projects" / "simulation" / "verify" / "direction_lab_pilot" / "controller.py",
    }
    for component_id, path in expected.items():
        assert component_id in entries
        assert entries[component_id]["fingerprint"] == hashlib.sha256(path.read_bytes()).hexdigest()


def test_v3_validator_rejects_missing_explicit_runtime_contract():
    queue = _queue()
    shared = queue["batches"][0]["shared_contract"]
    shared.pop("method")
    report = _load_validator().validate_queue(queue, queue_path=QUEUE)
    assert not report.passed
    assert any("explicit runtime" in error.lower() and "method" in error for error in report.errors)


def test_v3_validator_requires_truthful_runtime_field_effects():
    queue = _queue()
    effects = queue["batches"][0]["shared_contract"]["runtime_field_effects"]
    assert effects["fade_threshold_h"]["effect"] == "audit_only"
    assert effects["clip_norm"]["effect"] == "audit_only"
    assert all(
        effects[field]["effect"] == "operative"
        for field in ("channel_block", "r2", "t_s", "method")
    )

    effects["fade_threshold_h"]["effect"] = "operative"
    report = _load_validator().validate_queue(queue, queue_path=QUEUE)
    assert not report.passed
    assert any("runtime_field_effects" in error and "fade_threshold_h" in error for error in report.errors)


def test_v3_validator_rejects_implicit_top_level_batch_selection():
    queue = _queue()
    queue.pop("batch_id")
    report = _load_validator().validate_queue(queue, queue_path=QUEUE)
    assert report.errors
    assert any("batch_id" in error and "explicit" in error.lower() for error in report.errors)


def test_v3_runner_requires_batch_id_and_rejects_contract_override():
    spec = importlib.util.spec_from_file_location("direction_lab_run_v3", RUNNER)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    with pytest.raises(ValueError, match="batch_id is required"):
        module.load_contract(QUEUE)
    with pytest.raises(RuntimeError, match="contract_override"):
        module.run_governed(queue_path=QUEUE, output_dir=ROOT / "batches" / "V3-test", batch_id="B003",
                            contract_override={"method": "test"})


def test_v3_explicit_runtime_fields_reach_generator_and_baseline_config():
    spec = importlib.util.spec_from_file_location("direction_lab_run_v3_explicit", RUNNER)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    contract = {
        "snr_db": 20,
        "n_symbols": 100,
        "cma_mu": 0.002,
        "cma_taps": 13,
        "block_size": 64,
        "eval_start": 2,
        "eval_end": 99,
        "channel_block": 123,
        "r2": 0.75,
        "fade_threshold_h": 0.23,
        "clip_norm": 0.91,
        "t_s": 4e-10,
        "method": "gar",
    }
    calls = {}

    def generator(n, alpha, beta, f_g, *, sop_rate, seed, gamma_bar, block, t_s, method):
        calls["generator"] = {"gamma_bar": gamma_bar, "block": block, "t_s": t_s, "method": method}
        return {"sX": [(1 + 1j) / 2**0.5], "sY": [(1 + 1j) / 2**0.5]}

    wrapped = module._generator_adapter(generator, contract)
    wrapped(1, 4.2, 1.4, 30.0, 1e-5, 7, 123)
    assert calls["generator"] == {"gamma_bar": 100.0, "block": 123, "t_s": 4e-10, "method": "gar"}
    config = module._explicit_baseline_config(contract, lambda **kwargs: kwargs)
    assert config == {"mu": 0.002, "taps": 13, "r2": 0.75, "block_size": 64,
                      "eval_start": 2, "eval_end": 99, "fade_threshold_h": 0.23, "clip_norm": 0.91}


def test_strict_evidence_gate_rejects_result_without_artifact_pointer(tmp_path: Path):
    controller_path = ROOT.parents[2] / "projects" / "simulation" / "verify" / "direction_lab_pilot" / "controller.py"
    spec = importlib.util.spec_from_file_location("direction_lab_controller_v3", controller_path)
    controller_module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = controller_module
    spec.loader.exec_module(controller_module)
    manifest = {
        "run_id": "B003-test",
        "baseline_id": "baseline.standard_cma.godard_z",
        "component_id": "component.ml_degradation_detector.batch-v3",
        "baseline_fingerprint": "base",
        "component_fingerprint": "component",
        "state": "BATCH_READY",
        "sandbox_only": True,
        "promotion_allowed": False,
        "evidence_status": "EXPLORATORY",
    }
    controller = controller_module.GovernanceController(
        registry={
            "baseline.standard_cma.godard_z": {"status": "canonical", "fingerprint": "base"},
            "component.ml_degradation_detector.batch-v3": {"status": "sandbox-candidate", "fingerprint": "component"},
        },
        audit_path=tmp_path / "controller-audit.jsonl",
    )
    envelope = controller.execute(manifest, action="RUN", operation=lambda: {"signal": "synthetic"})
    gate = controller_module.EvidenceGate(
        audit_path=tmp_path / "controller-audit.jsonl",
        destinations={"evidence_ledger": tmp_path / "evidence.jsonl"},
        require_artifact_pointer=True,
    )
    verdict = gate.submit(envelope, destination="evidence_ledger")
    assert verdict["accepted"] is False
    assert verdict["artifact_status"] == "ORPHAN"
    assert not (tmp_path / "evidence.jsonl").exists()


def test_strict_evidence_gate_accepts_pointer_only_and_writes_lean_ledger(tmp_path: Path):
    controller_path = ROOT.parents[2] / "projects" / "simulation" / "verify" / "direction_lab_pilot" / "controller.py"
    spec = importlib.util.spec_from_file_location("direction_lab_controller_v3_positive", controller_path)
    controller_module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = controller_module
    spec.loader.exec_module(controller_module)
    manifest = {
        "run_id": "B003-positive",
        "baseline_id": "baseline.standard_cma.godard_z",
        "component_id": "component.ml_degradation_detector.batch-v3",
        "baseline_fingerprint": "base",
        "component_fingerprint": "component",
        "state": "BATCH_READY",
        "sandbox_only": True,
        "promotion_allowed": False,
        "evidence_status": "EXPLORATORY",
    }
    controller = controller_module.GovernanceController(
        registry={
            "baseline.standard_cma.godard_z": {"status": "canonical", "fingerprint": "base"},
            "component.ml_degradation_detector.batch-v3": {"status": "sandbox-candidate", "fingerprint": "component"},
        },
        audit_path=tmp_path / "controller-audit.jsonl",
    )
    envelope = controller.execute(manifest, action="RUN", operation=lambda: {"signal": "synthetic"})
    artifact = tmp_path / "artifacts" / "result.json"
    artifact.parent.mkdir()
    artifact.write_bytes(b"artifact")
    envelope["artifact_pointer"] = {
        "path": "artifacts/result.json",
        "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(),
        "bytes": artifact.stat().st_size,
    }
    gate = controller_module.EvidenceGate(
        audit_path=tmp_path / "controller-audit.jsonl",
        destinations={"evidence_ledger": tmp_path / "evidence.jsonl"},
        require_artifact_pointer=True,
    )
    verdict = gate.submit(envelope, destination="evidence_ledger")
    assert verdict["accepted"] is True
    record = json.loads((tmp_path / "evidence.jsonl").read_text(encoding="utf-8").splitlines()[0])
    assert "result" not in record
    assert record["artifact_pointer"] == envelope["artifact_pointer"]


def test_strict_evidence_gate_rejects_unverifiable_artifact_pointer(tmp_path: Path):
    controller_path = ROOT.parents[2] / "projects" / "simulation" / "verify" / "direction_lab_pilot" / "controller.py"
    spec = importlib.util.spec_from_file_location("direction_lab_controller_v3_pointer", controller_path)
    controller_module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = controller_module
    spec.loader.exec_module(controller_module)
    manifest = {
        "run_id": "B003-pointer",
        "baseline_id": "baseline.standard_cma.godard_z",
        "component_id": "component.ml_degradation_detector.batch-v3",
        "baseline_fingerprint": "base",
        "component_fingerprint": "component",
        "state": "BATCH_READY",
        "sandbox_only": True,
        "promotion_allowed": False,
        "evidence_status": "EXPLORATORY",
    }
    controller = controller_module.GovernanceController(
        registry={
            "baseline.standard_cma.godard_z": {"status": "canonical", "fingerprint": "base"},
            "component.ml_degradation_detector.batch-v3": {"status": "sandbox-candidate", "fingerprint": "component"},
        },
        audit_path=tmp_path / "controller-audit.jsonl",
    )
    envelope = controller.execute(manifest, action="RUN", operation=lambda: {"signal": "synthetic"})
    envelope["artifact_pointer"] = {"path": "../escape.json", "sha256": "bad", "bytes": 1}
    verdict = controller_module.EvidenceGate(
        audit_path=tmp_path / "controller-audit.jsonl",
        destinations={"evidence_ledger": tmp_path / "evidence.jsonl"},
        require_artifact_pointer=True,
    ).submit(envelope, destination="evidence_ledger")
    assert verdict["accepted"] is False
    assert verdict["artifact_status"] == "ORPHAN"


def test_v3_paired_cell_passes_explicit_fields_to_real_call_boundaries():
    spec = importlib.util.spec_from_file_location("direction_lab_run_v3_paired", RUNNER)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    contract = {
        "n_symbols": 8, "block_size": 4, "alpha": 4.2, "beta": 1.4,
        "f_g_hz": 30.0, "snr_db": 20.0, "modulation": "QPSK",
        "cma_mu": 0.002, "cma_taps": 3, "rates": [4e-6],
        "train_seeds": [11], "test_seeds": [41], "channel_block": 123,
        "r2": 0.75, "fade_threshold_h": 0.23, "clip_norm": 0.91,
        "t_s": 4e-10, "method": "gar", "eval_start": 0, "eval_end": 8,
    }
    seen = {}

    def generator(n, alpha, beta, f_g, *, sop_rate, seed, gamma_bar, block, t_s, method):
        seen["generator"] = {"block": block, "t_s": t_s, "method": method}
        qpsk = np.full(n, (1 + 1j) / np.sqrt(2), dtype=complex)
        return {"sX": qpsk, "sY": qpsk, "rX": qpsk, "rY": qpsk}

    def baseline(realization, cfg, variant="baseline", return_blind_trace=True):
        seen["baseline"] = {"r2": cfg.r2, "fade_threshold_h": cfg.fade_threshold_h, "clip_norm": cfg.clip_norm}
        trace = [{"output_start": start, "cm_error": 0.1, "output_power": 1.0, "update_norm": 0.01}
                 for start in range(0, 8, 4)]
        return {"zX": realization["sX"], "zY": realization["sY"],
                "valid_mask": np.ones(8, dtype=bool), "blind_trace": trace,
                "diverged": False, "divergence_symbol": None}

    module.run_paired_cell(4e-6, 41, contract, realization_generator=generator, baseline_runner=baseline)
    assert seen["generator"] == {"block": 123, "t_s": 4e-10, "method": "gar"}
    assert seen["baseline"] == {"r2": 0.75, "fade_threshold_h": 0.23, "clip_norm": 0.91}


def test_v3_gate_acceptance_is_hard_failure():
    spec = importlib.util.spec_from_file_location("direction_lab_run_v3_gate", RUNNER)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    with pytest.raises(RuntimeError, match="EvidenceGate"):
        module._require_gate_acceptance({"accepted": False, "artifact_status": "ORPHAN"})


def test_v3_governed_smoke_writes_source_closure_and_lean_artifacts(tmp_path: Path):
    spec = importlib.util.spec_from_file_location("direction_lab_run_v3_smoke", RUNNER)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    lab_dir = tmp_path / "projects" / "thesis-fso" / "direction-lab"
    (lab_dir / "tools").mkdir(parents=True)
    queue_path = lab_dir / "batch-queue.v3.yaml"
    queue = _queue()
    queue["status"] = "PASS"
    queue["queue_gate"]["independent_review"] = "PASS"
    queue["queue_gate"]["verdict"] = "PASS"
    queue["queue_gate"]["verifier_scope"] = "v3 smoke test"
    queue["queue_gate"]["verifier_evidence"] = ".sessions/2026-07-17-direction-lab-governance-pilot/verifications.md#V012"
    shared = queue["batches"][0]["shared_contract"]
    shared.update({"n_symbols": 256, "rates": [4e-6], "train_seeds": [11], "test_seeds": [41]})
    queue_path.write_text(yaml.safe_dump(queue, sort_keys=False), encoding="utf-8")
    shutil.copy2(ROOT / "batch-queue.v2.yaml", lab_dir / "batch-queue.v2.yaml")
    shutil.copy2(ROOT / "candidate-universe.v2.yaml", lab_dir / "candidate-universe.v2.yaml")
    shutil.copy2(ROOT / "candidate-map.v2.yaml", lab_dir / "candidate-map.v2.yaml")
    shutil.copy2(REGISTRY, lab_dir / "component-registry.v3.yaml")
    shutil.copy2(ROOT / "tools" / "ml_detector_batch.py", lab_dir / "tools" / "ml_detector_batch.py")
    shutil.copy2(ROOT / "tools" / "unlabeled_control_reconstruction.py", lab_dir / "tools" / "unlabeled_control_reconstruction.py")

    def generator(n, alpha, beta, f_g, *, sop_rate, seed, gamma_bar, block, t_s, method):
        qpsk = np.full(n, (1 + 1j) / np.sqrt(2), dtype=complex)
        return {"sX": qpsk, "sY": qpsk, "rX": qpsk, "rY": qpsk}

    def baseline(realization, cfg, variant="baseline", return_blind_trace=True):
        trace = [{"output_start": start, "cm_error": 0.1, "output_power": 1.0, "update_norm": 0.01}
                 for start in range(0, 256, 64)]
        return {"zX": realization["sX"], "zY": realization["sY"],
                "valid_mask": np.ones(256, dtype=bool), "blind_trace": trace,
                "diverged": False, "divergence_symbol": None}

    output_dir = tmp_path / "smoke-output"
    result = module.run_governed(queue_path=queue_path, batch_id="B003", output_dir=output_dir,
                                 realization_generator=generator, baseline_runner=baseline,
                                 allow_test_doubles=True)
    assert result["gate"]["accepted"] is True
    assert result["manifest"]["test_only"] is True
    closure = set(result["manifest"]["source_import_closure"])
    assert any(path.endswith("run_v3.py") for path in closure)
    assert any(path.endswith("run_v2.py") for path in closure)
    assert any(path.endswith("run_b001.py") for path in closure)
    assert any(path.endswith("validate_batch_queue.py") for path in closure)
    assert any(path.endswith("controller.py") for path in closure)
    ledger = json.loads((output_dir / "evidence_ledger.jsonl").read_text(encoding="utf-8").splitlines()[0])
    assert "result" not in ledger
    assert ledger["artifact_pointer"]["path"].replace("\\", "/") == "artifacts/result.json"
    artifact = output_dir / ledger["artifact_pointer"]["path"]
    assert artifact.is_file()
    assert (output_dir / "execution-status.yaml").is_file()
