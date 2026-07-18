"""Governed replacement runner for the immutable v3 queue snapshot.

The historical B002/v2 runner is not modified.  This runner carries the
explicit six-field channel contract through the generator and baseline config,
and always submits a lean evidence envelope containing an artifact pointer.
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
DEFAULT_QUEUE = LAB_ROOT / "batch-queue.v3.yaml"
REQUIRED_CONTRACT = (
    "n_symbols", "block_size", "alpha", "beta", "f_g_hz", "snr_db",
    "modulation", "cma_mu", "cma_taps", "rates", "train_seeds", "test_seeds",
)
EXPLICIT_RUNTIME_CONTRACT = (
    "channel_block", "r2", "fade_threshold_h", "clip_norm", "t_s", "method",
)


def _load_sibling(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


_v2 = _load_sibling(LAB_ROOT / "tools" / "run_v2.py", "direction_lab_run_v2_for_v3")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _json(value: Any) -> Any:
    return _v2._json(value)


def validate_contract(contract: Mapping[str, Any]) -> None:
    missing = [key for key in (*REQUIRED_CONTRACT, *EXPLICIT_RUNTIME_CONTRACT) if key not in contract]
    if missing:
        raise ValueError(f"v3 contract missing required fields: {missing}")
    if str(contract["modulation"]).upper() != "QPSK":
        raise ValueError("v3 baseline supports QPSK only")
    if not np.isfinite(float(contract["snr_db"])):
        raise ValueError("snr_db must be finite")
    if not np.isfinite(float(contract["r2"])) or float(contract["r2"]) <= 0:
        raise ValueError("r2 must be finite and positive")
    if not np.isfinite(float(contract["fade_threshold_h"])) or float(contract["fade_threshold_h"]) < 0:
        raise ValueError("fade_threshold_h must be finite and non-negative")
    if not np.isfinite(float(contract["clip_norm"])) or float(contract["clip_norm"]) <= 0:
        raise ValueError("clip_norm must be finite and positive")
    if not np.isfinite(float(contract["t_s"])) or float(contract["t_s"]) <= 0:
        raise ValueError("t_s must be finite and positive")
    if not str(contract["method"]).strip():
        raise ValueError("method must be non-empty")
    overlap = sorted(set(map(int, contract["train_seeds"])).intersection(map(int, contract["test_seeds"])))
    if overlap:
        raise ValueError(f"train/test seed overlap is forbidden: {overlap}")


def load_contract(queue_path: str | Path = DEFAULT_QUEUE, *, batch_id: str | None = None) -> dict[str, Any]:
    if not batch_id:
        raise ValueError("batch_id is required; implicit first-batch selection is forbidden")
    contract = _v2.load_contract(queue_path, batch_id=batch_id)
    validate_contract(contract)
    return contract


def _generator_adapter(generator: Callable[..., Any], contract: Mapping[str, Any]) -> Callable[..., Any]:
    gamma_bar = 10.0 ** (float(contract["snr_db"]) / 10.0)
    try:
        signature = inspect.signature(generator)
    except (TypeError, ValueError) as exc:
        raise TypeError("v3 generator signature must be inspectable") from exc
    required = {"sop_rate", "seed"}
    if not required.issubset(signature.parameters):
        raise TypeError("v3 generator must expose sop_rate and seed")
    accepts_kwargs = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in signature.parameters.values())
    required_names = {"gamma_bar", "block", "t_s", "method"}
    if not accepts_kwargs and not required_names.issubset(signature.parameters):
        raise TypeError("v3 generator must accept explicit gamma_bar, block, t_s and method")

    def wrapped(n, alpha, beta, f_g, rate, seed, _block=None):
        kwargs = {
            "sop_rate": rate,
            "seed": seed,
            "gamma_bar": gamma_bar,
            "block": int(contract["channel_block"]),
            "t_s": float(contract["t_s"]),
            "method": str(contract["method"]),
        }
        realization = generator(n, alpha, beta, f_g, **kwargs)
        if not _v2._qpsk(realization.get("sX")) or not _v2._qpsk(realization.get("sY")):
            raise ValueError("shared realization is not canonical QPSK")
        return realization

    return wrapped


def _explicit_baseline_config(contract: Mapping[str, Any], config_cls: Callable[..., Any]) -> Any:
    return config_cls(
        mu=float(contract["cma_mu"]),
        taps=int(contract["cma_taps"]),
        r2=float(contract["r2"]),
        block_size=int(contract["block_size"]),
        eval_start=int(contract.get("eval_start", 0)),
        eval_end=int(contract.get("eval_end", contract["n_symbols"])),
        fade_threshold_h=float(contract["fade_threshold_h"]),
        clip_norm=float(contract["clip_norm"]),
    )


def _require_gate_acceptance(gate: Mapping[str, Any]) -> None:
    if gate.get("accepted") is not True:
        raise RuntimeError(
            f"EvidenceGate rejected v3 run: status={gate.get('artifact_status')}, "
            f"trust={gate.get('trust_status')}, reason={gate.get('reason')}"
        )


def run_paired_cell(rate: float, seed: int, contract: Mapping[str, Any], *,
                    realization_generator: Callable[..., Any],
                    baseline_runner: Callable[..., Mapping[str, Any]],
                    source_root: str | Path = SOURCE_ROOT) -> dict[str, Any]:
    validate_contract(contract)
    legacy = _v2._legacy()
    source_root = Path(source_root)
    if baseline_runner is None:
        baseline_runner, config_cls = legacy._default_runner(source_root)
    else:
        config_cls = lambda **kwargs: SimpleNamespace(**kwargs)
    metrics_module = legacy._load_module(source_root / "common" / "_batch_metrics.py", "direction_lab_v3_metrics")
    ml_module = legacy._load_module(LAB_ROOT / "tools" / "ml_detector_batch.py", "direction_lab_v3_ml")
    cfg = _explicit_baseline_config(contract, config_cls)
    realization = _generator_adapter(realization_generator, contract)(
        int(contract["n_symbols"]), float(contract["alpha"]), float(contract["beta"]),
        float(contract["f_g_hz"]), float(rate), int(seed), int(contract["channel_block"]),
    )
    output = baseline_runner(realization, cfg, variant="baseline", return_blind_trace=True)
    trace = list(output.get("blind_trace", []))
    matrix, names = legacy._features_from_trace(trace, ml_module)
    rows = []
    eval_start = int(contract.get("eval_start", 0))
    eval_end = int(contract.get("eval_end", contract["n_symbols"]))
    for index, trace_row in enumerate(trace):
        start = int(trace_row["output_start"])
        metric = legacy._metric_for_block(realization, output, start, int(contract["block_size"]),
                                          eval_start, eval_end, metrics_module)
        if metric is None:
            continue
        features = {name: float(matrix[index, col]) for col, name in enumerate(names)}
        if legacy.FORBIDDEN_FEATURE_KEYS.intersection(features):
            raise RuntimeError("forbidden non-causal feature entered v3 rows")
        rows.append({
            "cell_id": f"{float(rate):g}:{int(seed)}", "rate": float(rate), "seed": int(seed),
            "block_index": index, "output_start": start, "label": int(metric["fixed_label_ber"] > 0.0),
            "fixed_label_ber": float(metric["fixed_label_ber"]), "pi_ber": float(metric["pi_ber"]),
            "permutation_invariant_ber": float(metric["pi_ber"]), "assignment": metric["assignment"],
            "features": features,
        })
    return _json({"rate": float(rate), "seed": int(seed), "cell_id": f"{float(rate):g}:{int(seed)}",
                  "baseline_calls": 1, "trace": trace, "rows": rows,
                  "source_files": [str(Path(getattr(baseline_runner, "_source_files", ("unknown",))[0]))]})


def run_dataset(contract: Mapping[str, Any], *, realization_generator: Callable[..., Any],
                baseline_runner: Callable[..., Mapping[str, Any]],
                source_root: str | Path = SOURCE_ROOT) -> dict[str, Any]:
    validate_contract(contract)
    legacy = _v2._legacy()
    rows, cells = [], []
    for split, seeds in (("train", contract["train_seeds"]), ("test", contract["test_seeds"])):
        for rate in contract["rates"]:
            for seed in seeds:
                cell = run_paired_cell(float(rate), int(seed), contract,
                                       realization_generator=realization_generator,
                                       baseline_runner=baseline_runner, source_root=source_root)
                rows.extend([dict(row, split=split) for row in cell["rows"]])
                cells.append(dict(cell, split=split))
    if not rows:
        return {"rows": [], "cells": cells, "feature_names": [], "detectors": {}}
    ml = _v2._load_module(LAB_ROOT / "tools" / "ml_detector_batch.py", "direction_lab_v3_dataset_ml")
    ae = _v2._load_module(LAB_ROOT / "tools" / "unlabeled_control_reconstruction.py", "direction_lab_v3_dataset_ae")
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
    x_ae = x_cal
    detector_ae = ae.UnlabeledControlReconstructionDetector(seed=11).fit(x_ae, ids_cal)
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
            scores = np.asarray([float(trace_by_cell[row["cell_id"]][int(row["block_index"])] ["cm_error"]) for row in test_rows], dtype=float)
            labels = np.asarray([row["label"] for row in test_rows], dtype=int)
            ids = np.asarray([row["cell_id"] for row in test_rows])
            comparator_metrics[f"{float(rate):g}"] = ml.evaluate_scores(scores, labels, ids, comparator_threshold, persistence_blocks=2) if scores.size and labels.size == scores.size else {"status": "INCONCLUSIVE"}
    return _json({"rows": rows, "cells": cells, "feature_names": feature_names, "detectors": detectors,
                  "minimum_information": {"event_cells": len(event_cells), "positive_train_blocks": int(sum(row["label"] for row in train_rows))},
                  "comparator": {"role": "traditional-single-threshold-negative-control", "candidate": False,
                                  "threshold_source": "control-rate-train-scores", "threshold": comparator_threshold,
                                  "metrics": comparator_metrics}})


def run_governed(*, queue_path: str | Path = DEFAULT_QUEUE, output_dir: str | Path,
                 batch_id: str | None = None,
                 realization_generator: Callable[..., Any] | None = None,
                 baseline_runner: Callable[..., Mapping[str, Any]] | None = None,
                 source_root: str | Path = SOURCE_ROOT, contract_override: Mapping[str, Any] | None = None,
                 allow_test_doubles: bool = False) -> dict[str, Any]:
    if contract_override is not None:
        raise RuntimeError("v3 runner forbids contract_override; edit queued contract and re-gate")
    if (realization_generator is not None or baseline_runner is not None) and not allow_test_doubles:
        raise RuntimeError("injected generator/baseline are test-only; set allow_test_doubles=True explicitly")
    queue_path, output_dir, source_root = Path(queue_path), Path(output_dir), Path(source_root)
    output_dir.mkdir(parents=True, exist_ok=True)
    queue = yaml.safe_load(queue_path.read_text(encoding="utf-8"))
    map_path = queue_path.with_name("candidate-map.v2.yaml")
    registry_path = queue_path.with_name("component-registry.v3.yaml")
    map_doc = yaml.safe_load(map_path.read_text(encoding="utf-8"))
    validator_module = _v2._load_module(LAB_ROOT / "tools" / "validate_batch_queue.py", "direction_lab_v3_queue_validator")
    static_report = validator_module.validate_queue(queue, queue_path=queue_path)
    if not static_report.passed:
        raise RuntimeError(f"v3 queue binding gate failed: {static_report.errors}")
    if queue.get("status") != "PASS" or queue.get("queue_gate", {}).get("verdict") != "PASS":
        raise RuntimeError("v3 RUN blocked: queue gate must be PASS")
    if map_doc.get("status") != "PASS" or map_doc.get("map_gate", {}).get("verdict") != "PASS":
        raise RuntimeError("v3 RUN blocked: map gate must be PASS")
    contract = load_contract(queue_path, batch_id=batch_id)
    legacy = _v2._legacy()
    if realization_generator is None:
        realization_generator = legacy._default_generator(source_root)
    if baseline_runner is None:
        baseline_runner, _ = legacy._default_runner(source_root)
    _v2._load_module(LAB_ROOT / "tools" / "ml_detector_batch.py", "direction_lab_v3_detector")
    _v2._load_module(LAB_ROOT / "tools" / "unlabeled_control_reconstruction.py", "direction_lab_v3_ae")
    batch = next(item for item in queue.get("batches", []) if item.get("batch_id") == contract["batch_id"])
    source_files = _v2._source_files(source_root, queue_path, map_path, registry_path)
    source_files.append(HERE)
    source_files.extend(_v2._runtime_import_files([source_root, LAB_ROOT / "tools", REPO_ROOT / "projects" / "simulation" / "verify"]))
    source_files = sorted(set(Path(path).resolve() for path in source_files))
    source_snapshot = {str(path): _sha256(path) for path in source_files}
    source_hash = hashlib.sha256(json.dumps(source_snapshot, sort_keys=True).encode()).hexdigest()
    detector_files = [LAB_ROOT / "tools" / "ml_detector_batch.py", LAB_ROOT / "tools" / "unlabeled_control_reconstruction.py"]
    component_fp = hashlib.sha256("".join(_sha256(path) for path in detector_files).encode()).hexdigest()
    runner_fp = _sha256(HERE)
    baseline_fp = _sha256(source_root / "explore" / "cma-fade-divergence" / "prompt013_swap_mechanism_q2.py")
    metric_fp = _sha256(source_root / "common" / "_batch_metrics.py")
    registry = _v2._registry(registry_path)
    controller_path = REPO_ROOT / "projects" / "simulation" / "verify" / "direction_lab_pilot" / "controller.py"
    expected = {"baseline.standard_cma.godard_z": baseline_fp,
                "component.ml_degradation_detector.batch-v3": component_fp,
                "runner.direction_lab.replacement-v3": runner_fp,
                "metric.dual_qpsk.fixed-plus-pi.v1": metric_fp,
                "runner.direction_lab.replacement-v2-helper": _sha256(LAB_ROOT / "tools" / "run_v2.py"),
                "runner.direction_lab.legacy-b001-helper": _sha256(LAB_ROOT / "tools" / "run_b001.py"),
                "controller.direction_lab.pilot-v3": _sha256(controller_path),
                "validator.direction_lab.queue-gate-v3": _sha256(LAB_ROOT / "tools" / "validate_batch_queue.py")}
    for component, fingerprint in expected.items():
        if component not in registry or registry[component].get("fingerprint") != fingerprint:
            raise RuntimeError(f"static v3 registry mismatch for {component}")
    controller_module = _v2._load_module(controller_path, "direction_lab_controller_v3")
    manifest = {"run_id": f"{contract['batch_id']}-{uuid.uuid4().hex}", "batch_id": contract["batch_id"],
                "state": "BATCH_READY", "baseline_id": contract.get("baseline_id"),
                "component_id": "component.ml_degradation_detector.batch-v3", "baseline_fingerprint": baseline_fp,
                "component_fingerprint": component_fp, "runner_fingerprint": runner_fp,
                "queue_hash": _sha256(queue_path), "source_snapshot": source_snapshot, "source_hash": source_hash,
                "source_import_closure": [str(path) for path in source_files], "contract": dict(contract),
                "sandbox_only": True, "promotion_allowed": False, "evidence_status": "EXPLORATORY",
                "destination": "evidence_ledger", "execution_mode": "TEST_DOUBLE" if allow_test_doubles else "PRODUCTION",
                "test_only": bool(allow_test_doubles), "registry_hash": _sha256(registry_path),
                "registry_path": str(registry_path), "execution_component_ids": list(expected),
                "family_id": batch.get("family_id"), "archetype_id": batch.get("archetype_id")}
    runtime_registry = _v2._runtime_registry(registry, list(expected))
    controller = controller_module.GovernanceController(registry=runtime_registry, audit_path=output_dir / "controller-audit.jsonl")
    executed = controller.execute(manifest, action="RUN", operation=lambda: run_dataset(
        contract, realization_generator=realization_generator, baseline_runner=baseline_runner, source_root=source_root))
    artifact_dir = output_dir / "artifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = artifact_dir / "result.json"
    artifact_path.write_text(json.dumps(_json(executed["result"]), indent=2, sort_keys=True), encoding="utf-8")
    artifact_pointer = {"path": str(artifact_path.relative_to(output_dir)), "sha256": _sha256(artifact_path), "bytes": artifact_path.stat().st_size}
    envelope = dict(executed)
    envelope["artifact_pointer"] = artifact_pointer
    gate = controller_module.EvidenceGate(audit_path=output_dir / "controller-audit.jsonl",
                                          destinations={"evidence_ledger": output_dir / "evidence_ledger.jsonl"},
                                          require_artifact_pointer=True).submit(envelope, destination="evidence_ledger")
    _require_gate_acceptance(gate)
    result = _json({"manifest": manifest, "execution": {k: v for k, v in executed.items() if k != "result"},
                    "artifact": artifact_pointer, "gate": gate})
    (output_dir / "manifest.json").write_text(json.dumps(_json(manifest), indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    status = {"schema_version": "direction-lab.execution-status.v1", "batch_id": contract["batch_id"],
              "run_id": manifest["run_id"], "manifest_hash": controller_module._manifest_hash(manifest),
              "result_hash": executed["result_hash"], "artifact": artifact_pointer,
              "evidence_gate": {key: gate.get(key) for key in ("accepted", "artifact_status", "trust_status", "decision_id")},
              "status": "COMPLETED_SANDBOX" if gate.get("accepted") else "COMPLETED_UNTRUSTED"}
    (output_dir / "execution-status.yaml").write_text(yaml.safe_dump(status, sort_keys=False), encoding="utf-8")
    return result


__all__ = ["load_contract", "validate_contract", "_generator_adapter", "_explicit_baseline_config",
           "run_paired_cell", "run_dataset", "run_governed"]
