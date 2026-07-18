"""Replacement-batch runner with explicit provenance and contract gates.

This module intentionally leaves ``run_b001.py`` untouched.  B001 is an
immutable historical receipt; replacement batches use this runner and their
own static registry/queue lineage.
"""

from __future__ import annotations

import hashlib
import importlib.util
import inspect
import json
import platform
import sys
import uuid
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import Any, Callable, Mapping

import numpy as np
import yaml


HERE = Path(__file__).resolve()
LAB_ROOT = HERE.parents[1]
REPO_ROOT = HERE.parents[4]
SOURCE_ROOT = REPO_ROOT / ".worktrees" / "unified-batch-runner" / "projects" / "simulation"
DEFAULT_QUEUE = LAB_ROOT / "batch-queue.v2.yaml"
REQUIRED_CONTRACT = (
    "n_symbols", "block_size", "alpha", "beta", "f_g_hz", "snr_db",
    "modulation", "cma_mu", "cma_taps", "rates", "train_seeds", "test_seeds",
)
EXPLICIT_RUNTIME_CONTRACT = (
    "channel_block", "r2", "fade_threshold_h", "clip_norm", "t_s", "method",
)
EXPECTED_MODULATION = "QPSK"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _json(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json(v) for v in value]
    if isinstance(value, np.ndarray):
        return [_json(v) for v in value.tolist()]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, Path):
        return str(value)
    return value


def _load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _legacy() -> ModuleType:
    return _load_module(LAB_ROOT / "tools" / "run_b001.py", "direction_lab_legacy_b001")


def validate_contract(contract: Mapping[str, Any]) -> None:
    missing = [key for key in (*REQUIRED_CONTRACT, *EXPLICIT_RUNTIME_CONTRACT) if key not in contract]
    if missing:
        raise ValueError(f"replacement contract missing required fields: {missing}")
    if str(contract["modulation"]).upper() != EXPECTED_MODULATION:
        raise ValueError("replacement baseline supports QPSK only")
    if not np.isfinite(float(contract["snr_db"])):
        raise ValueError("snr_db must be finite")
    overlap = sorted(set(map(int, contract["train_seeds"])).intersection(map(int, contract["test_seeds"])))
    if overlap:
        raise ValueError(f"train/test seed overlap is forbidden: {overlap}")


def load_contract(queue_path: str | Path = DEFAULT_QUEUE, *, batch_id: str | None = None) -> dict[str, Any]:
    queue_path = Path(queue_path)
    with queue_path.open("r", encoding="utf-8") as handle:
        queue = yaml.safe_load(handle)
    batches = queue.get("batches", []) if isinstance(queue, Mapping) else []
    if not batch_id:
        raise ValueError("batch_id is required; implicit first-batch selection is forbidden")
    wanted = batch_id
    batch = next((item for item in batches if item.get("batch_id") == wanted), None)
    if batch is None:
        raise ValueError(f"batch is absent from queue: {wanted}")
    contract = dict(batch.get("shared_contract", {}))
    for key in ("problem_mca", "candidates", "preregistered_outcomes", "valid_domain", "metrics"):
        if key in batch:
            contract[key] = batch[key]
    contract.update({"queue_id": queue.get("queue_id"), "batch_id": batch.get("batch_id"),
                     "family_id": batch.get("family_id"), "archetype_id": batch.get("archetype_id"),
                     "title": batch.get("title"),
                     "baseline_id": contract.get("baseline_id", "baseline.standard_cma.godard_z")})
    contract["rates"] = [float(v) for v in contract.get("rates", [])]
    contract["train_seeds"] = [int(v) for v in contract.get("train_seeds", [])]
    contract["test_seeds"] = [int(v) for v in contract.get("test_seeds", [])]
    contract["eval_start"] = int(contract.get("eval_start", 0))
    contract["eval_end"] = int(contract.get("eval_end", contract.get("n_symbols", 0)))
    validate_contract(contract)
    if not 0 <= contract["eval_start"] < contract["eval_end"] <= int(contract["n_symbols"]):
        raise ValueError("invalid evaluation window")
    return contract


def _qpsk(symbols: Any) -> bool:
    values = np.asarray(symbols)
    return bool(values.size and np.allclose(np.abs(values.real), 1.0 / np.sqrt(2), atol=1e-7)
                and np.allclose(np.abs(values.imag), 1.0 / np.sqrt(2), atol=1e-7))


def _generator_adapter(generator: Callable[..., Any], contract: Mapping[str, Any]) -> Callable[..., Any]:
    """Require the generator to receive contract SNR and verify QPSK output."""
    gamma_bar = 10.0 ** (float(contract["snr_db"]) / 10.0)
    try:
        signature = inspect.signature(generator)
    except (TypeError, ValueError) as exc:
        raise TypeError("replacement generator signature must expose gamma_bar") from exc
    required_named = {"sop_rate", "seed", "block"}
    if not required_named.issubset(signature.parameters):
        raise TypeError("replacement generator must expose sop_rate, seed, and block")
    accepts_gamma = "gamma_bar" in signature.parameters or any(
        p.kind == inspect.Parameter.VAR_KEYWORD for p in signature.parameters.values())
    if not accepts_gamma:
        raise TypeError("replacement generator must accept explicit gamma_bar")

    def wrapped(n, alpha, beta, f_g, rate, seed, block):
        # Use names deliberately: the canonical signature places gamma_bar
        # immediately after seed, so passing block positionally would bind the
        # wrong physical quantity.
        realization = generator(n, alpha, beta, f_g, sop_rate=rate, seed=seed,
                                gamma_bar=gamma_bar, block=block)
        if not _qpsk(realization.get("sX")) or not _qpsk(realization.get("sY")):
            raise ValueError("shared realization is not canonical QPSK")
        return realization
    return wrapped


def run_paired_cell(rate: float, seed: int, contract: Mapping[str, Any], *,
                    realization_generator: Callable[..., Any],
                    baseline_runner: Callable[..., Mapping[str, Any]],
                    source_root: str | Path = SOURCE_ROOT) -> dict[str, Any]:
    validate_contract(contract)
    legacy = _legacy()
    return legacy.run_paired_cell(rate, seed, contract,
                                  realization_generator=_generator_adapter(realization_generator, contract),
                                  baseline_runner=baseline_runner, source_root=source_root)


def run_dataset(contract: Mapping[str, Any], *, realization_generator: Callable[..., Any],
                baseline_runner: Callable[..., Mapping[str, Any]],
                source_root: str | Path = SOURCE_ROOT) -> dict[str, Any]:
    validate_contract(contract)
    # Reuse only the paired-cell and feature primitives.  The legacy dataset
    # orchestrator is deliberately not called: it trains the label-filtered
    # CleanReconstructionDetector, which is invalid for the replacement batch.
    legacy = _legacy()
    generator = _generator_adapter(realization_generator, contract)
    rows, cells = [], []
    for split, seeds in (("train", contract["train_seeds"]), ("test", contract["test_seeds"])):
        for rate in contract["rates"]:
            for seed in seeds:
                cell = legacy.run_paired_cell(rate, int(seed), contract,
                                              realization_generator=generator,
                                              baseline_runner=baseline_runner,
                                              source_root=source_root)
                rows.extend([dict(row, split=split) for row in cell["rows"]])
                cells.append(dict(cell, split=split))
    if not rows:
        return {"rows": [], "cells": cells, "feature_names": [], "detectors": {}}
    ml = _load_module(LAB_ROOT / "tools" / "ml_detector_batch.py", "direction_lab_ml_detector_v2")
    ae = _load_module(LAB_ROOT / "tools" / "unlabeled_control_reconstruction.py", "direction_lab_unlabeled_ae_v2")
    feature_names = sorted(rows[0]["features"])
    train_rows = [row for row in rows if row["split"] == "train"]
    control_rate = min(float(v) for v in contract["rates"])
    x_train = np.asarray([[row["features"][name] for name in feature_names] for row in train_rows], dtype=float)
    y_train = np.asarray([row["label"] for row in train_rows], dtype=int)
    cells_train = np.asarray([row["cell_id"] for row in train_rows])
    calibration_rows = [row for row in train_rows if float(row["rate"]) == control_rate]
    x_cal = np.asarray([[row["features"][name] for name in feature_names] for row in calibration_rows], dtype=float)
    ids_cal = np.asarray([row["cell_id"] for row in calibration_rows])
    detectors = {}
    supervised = {"logistic": ml.LogisticDetector(seed=11).fit(x_train, y_train, cells_train),
                  "mlp": ml.ShallowMLPDetector(seed=11).fit(x_train, y_train, cells_train)}
    for name, detector in supervised.items():
        scores_cal = detector.predict_proba(x_cal) if detector.status == "FIT" else None
        threshold = ml.calibrate_threshold(scores_cal, np.asarray([row["label"] for row in calibration_rows]), ids_cal,
                                           control_false_alarm_budget=0.20) if scores_cal is not None else {"status": "INCONCLUSIVE", "threshold": None}
        detectors[name] = {"status": detector.status, "training_splits": ["train"],
                           "threshold_source": "control-rate-train-scores", "threshold": threshold, "metrics": {}}
    ae_fit_rows = calibration_rows
    x_ae = np.asarray([[row["features"][name] for name in feature_names] for row in ae_fit_rows], dtype=float)
    ids_ae = np.asarray([row["cell_id"] for row in ae_fit_rows])
    detector_ae = ae.UnlabeledControlReconstructionDetector(seed=11).fit(x_ae, ids_ae)
    scores_ae = detector_ae.predict_proba(x_cal) if detector_ae.status == "FIT" else None
    threshold_ae = ae.calibrate_unlabeled_cell_threshold(scores_ae, ids_cal, 0.20) if scores_ae is not None else {"status": "INCONCLUSIVE", "threshold": None}
    detectors["autoencoder"] = {"status": detector_ae.status, "training_splits": ["train"],
                                 "training_rates": [control_rate], "threshold_source": "unlabeled-control-rate-train-scores",
                                 "threshold": threshold_ae, "metrics": {}}
    for name, detector in [("logistic", supervised["logistic"]), ("mlp", supervised["mlp"]), ("autoencoder", detector_ae)]:
        threshold = detectors[name]["threshold"].get("threshold")
        if detector.status != "FIT" or threshold is None:
            continue
        for rate in contract["rates"]:
            test_rows = [row for row in rows if row["split"] == "test" and float(row["rate"]) == float(rate)]
            x_test = np.asarray([[row["features"][key] for key in feature_names] for row in test_rows], dtype=float)
            scores = detector.predict_proba(x_test)
            detectors[name]["metrics"][f"{float(rate):g}"] = ml.evaluate_scores(
                scores, np.asarray([row["label"] for row in test_rows]), np.asarray([row["cell_id"] for row in test_rows]),
                threshold, persistence_blocks=2)
    event_cells = legacy._persistent_event_cells([row for row in rows if row["split"] == "test"], persistence=2)
    control_train = [cell for cell in cells if cell["split"] == "train" and float(cell["rate"]) == control_rate]
    comparator_scores = np.asarray([float(trace["cm_error"]) for cell in control_train for trace in cell["trace"]], dtype=float)
    comparator_threshold = float(np.quantile(comparator_scores, 0.99)) if comparator_scores.size else None
    comparator_metrics = {}
    if comparator_threshold is not None:
        for rate in contract["rates"]:
            test_cells = [cell for cell in cells if cell["split"] == "test" and float(cell["rate"]) == float(rate)]
            trace_by_cell = {cell["cell_id"]: cell["trace"] for cell in test_cells}
            test_rows = [row for row in rows if row["split"] == "test" and float(row["rate"]) == float(rate)]
            scores = np.asarray([float(trace_by_cell[row["cell_id"]][int(row["block_index"])]
                                       ["cm_error"]) for row in test_rows], dtype=float)
            labels = np.asarray([row["label"] for row in test_rows], dtype=int)
            ids = np.asarray([row["cell_id"] for row in test_rows])
            comparator_metrics[f"{float(rate):g}"] = ml.evaluate_scores(
                scores, labels, ids, comparator_threshold, persistence_blocks=2
            ) if scores.size and labels.size == scores.size else {"status": "INCONCLUSIVE"}
    return _json({"rows": rows, "cells": cells, "feature_names": feature_names, "detectors": detectors,
                  "minimum_information": {"event_cells": len(event_cells),
                                           "positive_train_blocks": int(sum(row["label"] for row in train_rows))},
                  "comparator": {"role": "traditional-single-threshold-negative-control", "candidate": False,
                                  "threshold_source": "control-rate-train-scores", "threshold": comparator_threshold,
                                  "metrics": comparator_metrics}})


def _source_files(source_root: Path, queue_path: Path, map_path: Path, registry_path: Path) -> list[Path]:
    common = sorted((source_root / "common").glob("*.py"))
    prompt = source_root / "explore" / "cma-fade-divergence" / "prompt013_swap_mechanism_q2.py"
    controller = REPO_ROOT / "projects" / "simulation" / "verify" / "direction_lab_pilot" / "controller.py"
    universe = LAB_ROOT / "candidate-universe.v2.yaml"
    files = [*common, source_root / "params.py", prompt,
             source_root / "explore" / "cma-fade-divergence" / "ml_long_seq_failure.py",
             source_root / "explore" / "cma-fade-divergence" / "prompt012_longseq_audit.py",
             source_root / "explore" / "cma-fade-divergence" / "prompt013_swap_quality_q1.py",
             LAB_ROOT / "tools" / "ml_detector_batch.py", LAB_ROOT / "tools" / "unlabeled_control_reconstruction.py",
             LAB_ROOT / "tools" / "run_b001.py", HERE,
             controller, queue_path, map_path, registry_path,
             LAB_ROOT / "anchor.yaml", LAB_ROOT / "canonical-state.yaml", universe]
    result, seen = [], set()
    for path in files:
        path = Path(path).resolve()
        if path not in seen:
            if not path.exists():
                raise FileNotFoundError(f"source closure file is missing: {path}")
            seen.add(path)
            result.append(path)
    return result


def _runtime_import_files(roots: list[Path]) -> list[Path]:
    """Collect loaded project Python files instead of relying on a hand list."""
    resolved_roots = [Path(root).resolve() for root in roots]
    result: set[Path] = set()
    for module in list(sys.modules.values()):
        path_value = getattr(module, "__file__", None)
        if not path_value or not str(path_value).endswith((".py", ".pyc")):
            continue
        path = Path(path_value).resolve()
        if path.suffix == ".pyc":
            path = path.with_suffix(".py")
        if any(path == root or root in path.parents for root in resolved_roots) and path.exists():
            result.add(path)
    return sorted(result)


def _registry(path: Path) -> dict[str, dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        doc = yaml.safe_load(handle)
    components = doc.get("components", []) if isinstance(doc, Mapping) else []
    result = {str(item["id"]): dict(item) for item in components if isinstance(item, Mapping) and "id" in item}
    if not result:
        raise RuntimeError(f"component registry is empty: {path}")
    return result


def _runtime_registry(registry: Mapping[str, Mapping[str, Any]], expected: list[str]) -> dict[str, dict[str, Any]]:
    """Return exactly the declared registry entries without normalizing status."""
    missing = [key for key in expected if key not in registry]
    if missing:
        raise RuntimeError(f"static component registry missing entries: {missing}")
    return {key: dict(registry[key]) for key in expected}


def run_governed(*, queue_path: str | Path = DEFAULT_QUEUE, output_dir: str | Path,
                 batch_id: str | None = None,
                 realization_generator: Callable[..., Any] | None = None,
                 baseline_runner: Callable[..., Mapping[str, Any]] | None = None,
                 source_root: str | Path = SOURCE_ROOT, contract_override: Mapping[str, Any] | None = None,
                 allow_test_doubles: bool = False) -> dict[str, Any]:
    if contract_override is not None:
        raise RuntimeError("replacement runner forbids contract_override; edit the queued contract and re-gate")
    if (realization_generator is not None or baseline_runner is not None) and not allow_test_doubles:
        raise RuntimeError("injected generator/baseline are test-only; set allow_test_doubles=True explicitly")
    queue_path, output_dir, source_root = Path(queue_path), Path(output_dir), Path(source_root)
    output_dir.mkdir(parents=True, exist_ok=True)
    with queue_path.open("r", encoding="utf-8") as handle:
        queue = yaml.safe_load(handle)
    map_path = queue_path.with_name("candidate-map.v2.yaml")
    registry_path = queue_path.with_name("component-registry.v2.yaml")
    if not map_path.exists():
        raise RuntimeError(f"replacement map is missing: {map_path}")
    if not registry_path.exists():
        raise RuntimeError(f"replacement registry is missing: {registry_path}")
    with map_path.open("r", encoding="utf-8") as handle:
        map_doc = yaml.safe_load(handle)
    qgate, mgate = queue.get("queue_gate", {}), map_doc.get("map_gate", {})
    if queue.get("status") != "PASS" or qgate.get("verdict") != "PASS":
        raise RuntimeError("replacement RUN blocked: queue gate must be PASS")
    if map_doc.get("status") != "PASS" or mgate.get("verdict") != "PASS":
        raise RuntimeError("replacement RUN blocked: map gate must be PASS")
    contract = load_contract(queue_path, batch_id=batch_id)
    if realization_generator is None or baseline_runner is None:
        legacy = _legacy()
        if realization_generator is None:
            realization_generator = legacy._default_generator(source_root)
        if baseline_runner is None:
            baseline_runner, _ = legacy._default_runner(source_root)
    # Load detector modules before freezing the manifest so the closure records
    # the modules that the operation is permitted to import.
    _load_module(LAB_ROOT / "tools" / "ml_detector_batch.py", "direction_lab_ml_detector_v2")
    _load_module(LAB_ROOT / "tools" / "unlabeled_control_reconstruction.py", "direction_lab_unlabeled_ae_v2")
    batch = next(item for item in queue.get("batches", []) if item.get("batch_id") == contract["batch_id"])
    source_files = _source_files(source_root, queue_path, map_path, registry_path)
    for path in _runtime_import_files([source_root, LAB_ROOT / "tools", REPO_ROOT / "projects" / "simulation" / "verify"]):
        if path not in source_files:
            source_files.append(path)
    source_files.sort()
    source_snapshot = {str(path): _sha256(path) for path in source_files}
    source_hash = hashlib.sha256(json.dumps(source_snapshot, sort_keys=True).encode()).hexdigest()
    universe_path = LAB_ROOT / "candidate-universe.v2.yaml"
    governance_files = {queue_path.resolve(), map_path.resolve(), registry_path.resolve(),
                        (LAB_ROOT / "anchor.yaml").resolve(), (LAB_ROOT / "canonical-state.yaml").resolve(),
                        universe_path.resolve()}
    runtime_files = [p for p in source_files if p not in governance_files]
    detector_files = [LAB_ROOT / "tools" / "ml_detector_batch.py",
                      LAB_ROOT / "tools" / "unlabeled_control_reconstruction.py"]
    component_fp = hashlib.sha256("".join(_sha256(path) for path in detector_files).encode()).hexdigest()
    runner_fp = _sha256(HERE)
    prompt_path = source_root / "explore" / "cma-fade-divergence" / "prompt013_swap_mechanism_q2.py"
    baseline_fp = _sha256(prompt_path)
    metric_path = source_root / "common" / "_batch_metrics.py"
    metric_fp = _sha256(metric_path)
    registry = _registry(registry_path)
    component_id = "component.ml_degradation_detector.batch-v2"
    runner_id = "runner.direction_lab.replacement-v2"
    expected = {"baseline.standard_cma.godard_z": baseline_fp, component_id: component_fp,
                runner_id: runner_fp, "metric.dual_qpsk.fixed-plus-pi.v1": metric_fp}
    for component, fingerprint in expected.items():
        if component not in registry or registry[component].get("fingerprint") != fingerprint:
            raise RuntimeError(f"static component registry mismatch for {component}")
    controller_module = _load_module(REPO_ROOT / "projects" / "simulation" / "verify" / "direction_lab_pilot" / "controller.py", "direction_lab_controller_v2")
    candidate_specs = list(batch.get("candidates", []))
    manifest = {
        "run_id": f"{contract['batch_id']}-{uuid.uuid4().hex}", "batch_id": contract["batch_id"], "state": "BATCH_READY",
        "baseline_id": contract.get("baseline_id"), "component_id": component_id,
        "baseline_fingerprint": baseline_fp, "component_fingerprint": component_fp,
        "runner_fingerprint": runner_fp, "queue_hash": _sha256(queue_path), "source_snapshot": source_snapshot,
        "source_hash": source_hash, "source_import_closure": [str(path) for path in source_files],
        "code_closure": [str(path) for path in runtime_files],
        "contract_snapshot": [str(path) for path in (queue_path.resolve(), map_path.resolve(), registry_path.resolve(),
                                                       (LAB_ROOT / "anchor.yaml").resolve(),
                                                       (LAB_ROOT / "canonical-state.yaml").resolve(),
                                                       universe_path.resolve())],
        "metric_contract_id": "metric.dual_qpsk.fixed-plus-pi.v1", "sandbox_only": True, "promotion_allowed": False,
        "evidence_status": "EXPLORATORY", "destination": "evidence_ledger", "contract": dict(contract),
        "execution_mode": "TEST_DOUBLE" if allow_test_doubles else "PRODUCTION",
        "test_only": bool(allow_test_doubles),
        "environment_fingerprint": hashlib.sha256(f"{platform.platform()}|{sys.version}|{np.__version__}".encode()).hexdigest(),
        "family_id": batch.get("family_id"), "archetype_id": batch.get("archetype_id"),
        "candidate_ids": [item.get("candidate_id") for item in candidate_specs],
        "hypotheses": [item.get("hypothesis") for item in candidate_specs],
        "primary_metrics": contract.get("metrics", {}).get("primary", []),
        "diagnostic_metrics": contract.get("metrics", {}).get("diagnostics", []),
        "pass_kill_rules": batch.get("preregistered_outcomes", {}), "valid_domain": batch.get("valid_domain"),
        "registry_path": str(registry_path), "registry_hash": _sha256(registry_path),
        "execution_component_ids": list(expected),
    }
    runtime_registry = _runtime_registry(registry, list(expected))
    controller = controller_module.GovernanceController(registry=runtime_registry,
                                                         audit_path=output_dir / "controller-audit.jsonl")
    executed = controller.execute(manifest, action="RUN",
                                  operation=lambda: run_dataset(contract, realization_generator=realization_generator,
                                                                baseline_runner=baseline_runner, source_root=source_root))
    artifact_dir = output_dir / "artifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = artifact_dir / "result.json"
    artifact_path.write_text(json.dumps(_json(executed["result"]), indent=2, sort_keys=True), encoding="utf-8")
    artifact_pointer = {"path": str(artifact_path.relative_to(output_dir)),
                        "sha256": _sha256(artifact_path), "bytes": artifact_path.stat().st_size}
    executed_for_gate = dict(executed)
    executed_for_gate["artifact_pointer"] = artifact_pointer
    gate = controller_module.EvidenceGate(audit_path=output_dir / "controller-audit.jsonl",
                                           destinations={"evidence_ledger": output_dir / "evidence_ledger.jsonl"}).submit(executed_for_gate, destination="evidence_ledger")
    result = _json({"manifest": manifest, "execution": {k: v for k, v in executed.items() if k != "result"},
                    "artifact": artifact_pointer, "gate": gate})
    (output_dir / "manifest.json").write_text(json.dumps(_json(manifest), indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    status = {
        "schema_version": "direction-lab.execution-status.v1",
        "batch_id": contract["batch_id"],
        "run_id": manifest["run_id"],
        "manifest_hash": controller_module._manifest_hash(manifest),
        "result_hash": executed["result_hash"],
        "artifact": artifact_pointer,
        "evidence_gate": {key: gate.get(key) for key in ("accepted", "artifact_status", "trust_status", "decision_id")},
        "status": "COMPLETED_SANDBOX" if gate.get("accepted") else "COMPLETED_UNTRUSTED",
    }
    (output_dir / "execution-status.yaml").write_text(yaml.safe_dump(status, sort_keys=False), encoding="utf-8")
    return result


__all__ = ["load_contract", "validate_contract", "run_paired_cell", "run_dataset", "run_governed"]
