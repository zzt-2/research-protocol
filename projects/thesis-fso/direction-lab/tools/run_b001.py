"""Governed paired runner for Direction Lab B001.

This module is deliberately a small orchestration seam.  The simulator and
standard CMA implementation are loaded from the frozen unified-batch-runner
worktree; this file never edits the canonical registry or baseline.
"""

from __future__ import annotations

import hashlib
import importlib
import importlib.util
import json
import platform
import sys
import uuid
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Callable, Mapping

import numpy as np
import yaml


HERE = Path(__file__).resolve()
LAB_ROOT = HERE.parents[1]
REPO_ROOT = HERE.parents[4]
DEFAULT_SOURCE_ROOT = REPO_ROOT / ".worktrees" / "unified-batch-runner" / "projects" / "simulation"
DEFAULT_QUEUE = LAB_ROOT / "batch-queue.yaml"

REQUIRED_CONTRACT = (
    "n_symbols", "block_size", "alpha", "beta", "f_g_hz", "snr_db",
    "modulation", "cma_mu", "cma_taps", "rates", "train_seeds", "test_seeds",
)
FORBIDDEN_FEATURE_KEYS = {"h", "theta", "sX", "sY"}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


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
    if isinstance(value, (Path,)):
        return str(value)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise TypeError(f"result is not JSON serializable: {type(value).__name__}")


def load_contract(queue_path: str | Path = DEFAULT_QUEUE, *, override: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Read the B001 contract; required run parameters are never defaulted."""
    with Path(queue_path).open("r", encoding="utf-8") as handle:
        queue = yaml.safe_load(handle)
    batches = queue.get("batches", []) if isinstance(queue, Mapping) else []
    batch = next((item for item in batches if item.get("batch_id") == "B001"), None)
    if batch is None:
        raise ValueError("B001 is absent from batch queue")
    contract = dict(batch.get("shared_contract", {}))
    contract["queue_id"] = queue.get("queue_id")
    contract["batch_id"] = batch.get("batch_id")
    contract["family_id"] = batch.get("family_id")
    contract["archetype_id"] = batch.get("archetype_id")
    contract["title"] = batch.get("title")
    for key in ("problem_mca", "candidates", "preregistered_outcomes", "valid_domain", "metrics"):
        if key in batch:
            contract[key] = batch[key]
    contract["baseline_id"] = contract.get("baseline_id", "baseline.standard_cma.godard_z")
    # The queue names the complete sequence; the CMA adapter's valid samples
    # are selected from that sequence, with no hidden numerical defaults.
    if override:
        contract.update(dict(override))
    missing = [key for key in REQUIRED_CONTRACT if key not in contract]
    if missing:
        raise ValueError(f"B001 contract missing required fields: {missing}")
    contract["rates"] = [float(v) for v in contract["rates"]]
    contract["train_seeds"] = [int(v) for v in contract["train_seeds"]]
    contract["test_seeds"] = [int(v) for v in contract["test_seeds"]]
    contract["eval_start"] = int(contract.get("eval_start", 0))
    contract["eval_end"] = int(contract.get("eval_end", contract["n_symbols"]))
    if not 0 <= contract["eval_start"] < contract["eval_end"] <= int(contract["n_symbols"]):
        raise ValueError("invalid evaluation window in B001 contract")
    return contract


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load frozen module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _default_runner(source_root: Path):
    source_root = Path(source_root).resolve()
    prompt_path = source_root / "explore" / "cma-fade-divergence" / "prompt013_swap_mechanism_q2.py"
    for name in [name for name in sys.modules if name == "common" or name.startswith("common.")]:
        sys.modules.pop(name, None)
    sys.path.insert(0, str(source_root))
    module = _load_module(prompt_path, "direction_lab_frozen_prompt013")
    if sys.path and sys.path[0] == str(source_root):
        sys.path.pop(0)
    def runner(realization, cfg, variant="baseline", return_blind_trace=True):
        if variant != "baseline":
            raise ValueError("B001 baseline adapter only accepts variant='baseline'")
        late_start, late_end = int(cfg.eval_start), int(cfg.eval_end)
        diagnostic = module.run_cma_diagnostic(
            np.asarray(realization["rX"]), np.asarray(realization["rY"]), mode="standard",
            mu=float(cfg.mu), n_tap=int(cfg.taps), r2=float(cfg.r2), block_size=int(cfg.block_size),
            late_slice=(late_start, late_end), fork_at=late_start,
        )
        online = diagnostic["online"]
        z_x, z_y = np.asarray(online["zX"]), np.asarray(online["zY"])
        valid = np.zeros(late_end - late_start, dtype=bool)
        traces = []
        half = int(cfg.taps) // 2
        for item in diagnostic.get("trace", []):
            start = int(item["output_start"])
            left, right = max(start, late_start), min(start + int(cfg.block_size), late_end)
            if left >= right:
                continue
            valid[left - late_start:right - late_start] = True
            block_x = z_x[left - late_start:right - late_start]
            block_y = z_y[left - late_start:right - late_start]
            traces.append({
                "output_start": start, "output_end": int(item.get("output_end", start + cfg.block_size)),
                "cm_error": float(np.mean((float(cfg.r2) - np.abs(block_x) ** 2) ** 2 +
                                          (float(cfg.r2) - np.abs(block_y) ** 2) ** 2)),
                "output_power": float(np.mean(np.abs(block_x) ** 2 + np.abs(block_y) ** 2)),
                "update_norm": float(item["standard_with_z_update_norm"]),
            })
        return {"zX": z_x, "zY": z_y, "valid_mask": valid, "blind_trace": traces,
                "diverged": False, "divergence_symbol": None,
                "provenance": {"implementation": str(prompt_path),
                                "entry": "run_cma_diagnostic(mode='standard')",
                                "gradient": "Godard-with-z"}}
    runner._source_files = (str(prompt_path),)
    runner._frozen_module = module
    return runner, (lambda **kwargs: SimpleNamespace(**kwargs))


def _default_generator(source_root: Path):
    """Import the shared-realization generator from the frozen source tree."""
    source_root = Path(source_root).resolve()
    old_common = {name: module for name, module in sys.modules.items()
                  if name == "common" or name.startswith("common.")}
    for name in old_common:
        sys.modules.pop(name, None)
    sys.path.insert(0, str(source_root))
    try:
        module = importlib.import_module("common._dual_pol_channel")
        return module.generate_shared_realization_dp
    finally:
        if sys.path and sys.path[0] == str(source_root):
            sys.path.pop(0)


def _features_from_trace(trace: list[Mapping[str, Any]], ml_module):
    arrays = {key: np.asarray([float(row[key]) for row in trace], dtype=float)
              for key in ("cm_error", "output_power", "update_norm")}
    matrix, names = ml_module.build_trace_features(arrays, window=8)
    return matrix, names


def _metric_for_block(realization, output, start: int, block_size: int, eval_start: int, eval_end: int, metrics_module):
    left, right = max(start, eval_start), min(start + block_size, eval_end)
    if left >= right:
        return None
    tx_x = np.asarray(realization["sX"])[left:right]
    tx_y = np.asarray(realization["sY"])[left:right]
    z_x = np.asarray(output["zX"])
    z_y = np.asarray(output["zY"])
    offset = 0 if len(z_x) == len(realization["sX"]) else eval_start
    mask = np.asarray(output.get("valid_mask", np.ones(len(z_x), dtype=bool)))
    mask = mask[left - offset:right - offset]
    if not np.any(mask):
        return None
    return metrics_module.evaluate_dual_qpsk(tx_x[mask], tx_y[mask],
                                             z_x[left - offset:right - offset][mask],
                                             z_y[left - offset:right - offset][mask])


def _persistent_event_cells(rows: list[Mapping[str, Any]], persistence: int = 2) -> set[str]:
    result = set()
    for cell_id in sorted({str(row["cell_id"]) for row in rows}):
        flags = [int(row["label"]) == 1 for row in sorted(
            (row for row in rows if row["cell_id"] == cell_id),
            key=lambda row: int(row["block_index"]),
        )]
        run = 0
        for flag in flags:
            run = run + 1 if flag else 0
            if run >= persistence:
                result.add(cell_id)
                break
    return result


def run_paired_cell(rate: float, seed: int, contract: Mapping[str, Any], *,
                    realization_generator: Callable[..., Any] | None = None,
                    baseline_runner: Callable[..., Mapping[str, Any]] | None = None,
                    source_root: str | Path = DEFAULT_SOURCE_ROOT) -> dict[str, Any]:
    """Generate one realization, execute standard CMA once, and emit cell rows."""
    source_root = Path(source_root)
    if realization_generator is None:
        realization_generator = _default_generator(source_root)
    if baseline_runner is None:
        baseline_runner, config_cls = _default_runner(source_root)
    else:
        config_cls = lambda **kwargs: SimpleNamespace(**kwargs)
    metrics_module = _load_module(source_root / "common" / "_batch_metrics.py", "direction_lab_frozen_metrics")
    ml_module = _load_module(LAB_ROOT / "tools" / "ml_detector_batch.py", "direction_lab_ml_detector")
    eval_start = int(contract.get("eval_start", 0))
    eval_end = int(contract.get("eval_end", contract["n_symbols"]))
    cfg = config_cls(mu=float(contract["cma_mu"]), taps=int(contract["cma_taps"]),
                     r2=1.0, block_size=int(contract["block_size"]),
                     eval_start=eval_start, eval_end=eval_end,
                     fade_threshold_h=float(contract.get("fade_threshold_h", 0.1)), clip_norm=1.0)
    realization = realization_generator(
        int(contract["n_symbols"]), float(contract["alpha"]), float(contract["beta"]),
        float(contract["f_g_hz"]), float(rate), int(seed), block=int(contract.get("channel_block", 100)),
    )
    output = baseline_runner(realization, cfg, variant="baseline", return_blind_trace=True)
    trace = list(output.get("blind_trace", []))
    matrix, names = _features_from_trace(trace, ml_module)
    rows = []
    for index, trace_row in enumerate(trace):
        start = int(trace_row["output_start"])
        metric = _metric_for_block(realization, output, start, int(contract["block_size"]),
                                   eval_start, eval_end, metrics_module)
        if metric is None:
            continue
        features = {name: float(matrix[index, col]) for col, name in enumerate(names)}
        if FORBIDDEN_FEATURE_KEYS.intersection(features):
            raise RuntimeError("forbidden non-causal feature entered B001 rows")
        rows.append({
            "cell_id": f"{float(rate):g}:{int(seed)}", "rate": float(rate), "seed": int(seed),
            "block_index": index, "output_start": start, "label": int(metric["fixed_label_ber"] > 0.0),
            "fixed_label_ber": float(metric["fixed_label_ber"]), "pi_ber": float(metric["pi_ber"]),
            "permutation_invariant_ber": float(metric["pi_ber"]),
            "assignment": metric["assignment"], "features": features,
        })
    return _json({
        "rate": float(rate), "seed": int(seed), "cell_id": f"{float(rate):g}:{int(seed)}", "baseline_calls": 1,
        "summary": {"rate": float(rate), "seed": int(seed), "blocks": len(rows),
                     "positive_blocks": int(sum(row["label"] for row in rows)),
                     "fixed_label_ber_mean": float(np.mean([row["fixed_label_ber"] for row in rows])) if rows else None,
                     "pi_ber_mean": float(np.mean([row["pi_ber"] for row in rows])) if rows else None},
        "trace": [{key: float(value) if key != "output_start" else int(value)
                   for key, value in item.items()} for item in trace],
        "rows": rows,
        "source_files": [str(Path(getattr(baseline_runner, "_source_files", ("unknown",))[0]))],
    })


def _load_ml_module():
    return _load_module(LAB_ROOT / "tools" / "ml_detector_batch.py", "direction_lab_ml_detector_dataset")


def run_dataset(contract: Mapping[str, Any], *, realization_generator=None,
                baseline_runner=None, source_root: str | Path = DEFAULT_SOURCE_ROOT) -> dict[str, Any]:
    """Run all paired cells, then fit/calibrate detectors without test leakage."""
    rows, cells = [], []
    train_set = set(int(v) for v in contract["train_seeds"])
    test_set = set(int(v) for v in contract["test_seeds"])
    for split, seeds in (("train", contract["train_seeds"]), ("test", contract["test_seeds"])):
        for rate in contract["rates"]:
            for seed in seeds:
                cell = run_paired_cell(rate, int(seed), contract,
                                       realization_generator=realization_generator,
                                       baseline_runner=baseline_runner,
                                       source_root=source_root)
                cell_rows = [dict(row, split=split) for row in cell["rows"]]
                rows.extend(cell_rows)
                cells.append(dict(cell, split=split))
    ml = _load_ml_module()
    feature_names = sorted(rows[0]["features"]) if rows else []
    train_rows = [row for row in rows if row["split"] == "train"]
    x_train = np.asarray([[row["features"][name] for name in feature_names] for row in train_rows], dtype=float)
    y_train = np.asarray([row["label"] for row in train_rows], dtype=int)
    train_cells = np.asarray([row["cell_id"] for row in train_rows])
    control_rate = min(float(v) for v in contract["rates"])
    detectors = {}
    for name in ("logistic", "mlp", "autoencoder"):
        fit_rows = train_rows if name != "autoencoder" else [row for row in train_rows if row["rate"] == control_rate]
        if not fit_rows:
            detectors[name] = {"status": "INCONCLUSIVE", "training_splits": ["train"],
                               "threshold_source": "control-rate-train-scores", "metrics": {}}
            continue
        x_fit = np.asarray([[row["features"][key] for key in feature_names] for row in fit_rows], dtype=float)
        y_fit = np.asarray([row["label"] for row in fit_rows], dtype=int)
        cells_fit = np.asarray([row["cell_id"] for row in fit_rows])
        detector = ml.fit_candidates(x_fit, y_fit, cells_fit, seed=11)[name]
        calibration_rows = [row for row in train_rows if row["rate"] == control_rate]
        x_cal = np.asarray([[row["features"][key] for key in feature_names] for row in calibration_rows], dtype=float)
        scores_cal = detector.predict_proba(x_cal) if detector.status == "FIT" else None
        if scores_cal is None:
            detectors[name] = {"status": detector.status, "training_splits": ["train"],
                               "training_rates": sorted({row["rate"] for row in fit_rows}),
                               "threshold_source": "control-rate-train-scores", "metrics": {}}
            continue
        threshold = ml.calibrate_threshold(scores_cal,
                                           np.asarray([row["label"] for row in calibration_rows]),
                                           np.asarray([row["cell_id"] for row in calibration_rows]),
                                           control_false_alarm_budget=0.20)
        metrics = {}
        for rate in contract["rates"]:
            test_rows = [row for row in rows if row["split"] == "test" and row["rate"] == float(rate)]
            x_test = np.asarray([[row["features"][key] for key in feature_names] for row in test_rows], dtype=float)
            scores = detector.predict_proba(x_test)
            metrics[f"{float(rate):g}"] = ml.evaluate_scores(
                scores, np.asarray([row["label"] for row in test_rows]),
                np.asarray([row["cell_id"] for row in test_rows]), threshold["threshold"], persistence_blocks=2,
            ) if scores is not None and threshold["threshold"] is not None else {"status": "INCONCLUSIVE"}
        detectors[name] = {"status": detector.status, "training_splits": ["train"],
                           "training_rates": sorted({row["rate"] for row in fit_rows}),
                           "threshold_source": "control-rate-train-scores", "threshold": threshold,
                           "metrics": metrics}
    event_cells = _persistent_event_cells([row for row in rows if row["split"] == "test"], persistence=2)
    control_train = [cell for cell in cells if cell["split"] == "train" and float(cell["rate"]) == control_rate]
    comparator_scores = np.asarray([float(trace["cm_error"]) for cell in control_train for trace in cell["trace"]], dtype=float)
    comparator_threshold = float(np.quantile(comparator_scores, 0.99)) if comparator_scores.size else None
    comparator_metrics = {}
    if comparator_threshold is not None:
        for rate in contract["rates"]:
            test = [cell for cell in cells if cell["split"] == "test" and float(cell["rate"]) == float(rate)]
            trace_by_cell = {cell["cell_id"]: cell["trace"] for cell in test}
            test_rows = [row for row in rows if row["split"] == "test" and row["rate"] == float(rate)]
            scores = np.asarray([float(trace_by_cell[row["cell_id"]][int(row["block_index"])]
                                       ["cm_error"]) for row in test_rows], dtype=float)
            labels = np.asarray([row["label"] for row in test_rows], dtype=int)
            ids = np.asarray([row["cell_id"] for row in test_rows])
            comparator_metrics[f"{float(rate):g}"] = ml.evaluate_scores(
                scores, labels, ids, comparator_threshold, persistence_blocks=2,
            ) if scores.size and labels.size == scores.size else {"status": "INCONCLUSIVE"}
    return _json({"rows": rows, "cells": cells, "feature_names": feature_names,
                  "detectors": detectors,
                  "minimum_information": {"event_cells": len(event_cells),
                                           "positive_train_blocks": int(sum(row["label"] for row in train_rows))},
                  "comparator": {"role": "traditional-single-threshold-negative-control",
                                  "candidate": False,
                                  "threshold_source": "control-rate-train-scores",
                                  "threshold": comparator_threshold,
                                  "metrics": comparator_metrics}})


def run_governed(*, queue_path: str | Path = DEFAULT_QUEUE, output_dir: str | Path,
                 realization_generator=None, baseline_runner=None,
                 contract_override: Mapping[str, Any] | None = None,
                 source_root: str | Path = DEFAULT_SOURCE_ROOT) -> dict[str, Any]:
    """Execute B001 through controller RUN and submit only to evidence ledger."""
    queue_path, output_dir, source_root = Path(queue_path), Path(output_dir), Path(source_root)
    output_dir.mkdir(parents=True, exist_ok=True)
    with queue_path.open("r", encoding="utf-8") as handle:
        queue_doc = yaml.safe_load(handle)
    map_path = queue_path.with_name("candidate-map.yaml")
    with map_path.open("r", encoding="utf-8") as handle:
        map_doc = yaml.safe_load(handle)
    queue_gate = queue_doc.get("queue_gate", {}) if isinstance(queue_doc, Mapping) else {}
    map_gate = map_doc.get("map_gate", {}) if isinstance(map_doc, Mapping) else {}
    queue_ok = queue_doc.get("status") == "PASS" and queue_gate.get("verdict") == "PASS"
    map_ok = map_doc.get("status") == "PASS" and map_gate.get("verdict") == "PASS"
    if not queue_ok or not map_ok:
        raise RuntimeError("B001 RUN blocked: queue/map gate must both be PASS")
    contract = load_contract(queue_path, override=contract_override)
    batch_record = next(item for item in queue_doc.get("batches", []) if item.get("batch_id") == "B001")
    candidate_specs = list(batch_record.get("candidates", []))
    controller_module = _load_module(REPO_ROOT / "projects" / "simulation" / "verify" / "direction_lab_pilot" / "controller.py", "direction_lab_controller_b001")
    prompt_path = source_root / "explore" / "cma-fade-divergence" / "prompt013_swap_mechanism_q2.py"
    source_files = [
        source_root / "common" / "_dual_pol_channel.py",
        source_root / "common" / "_gg_time.py",
        source_root / "common" / "_config.py",
        source_root / "common" / "_experiment.py",
        source_root / "common" / "_ml_equalizer.py",
        source_root / "common" / "_cma.py",
        source_root / "common" / "_equalizer.py",
        source_root / "params.py",
        prompt_path,
        source_root / "explore" / "cma-fade-divergence" / "ml_long_seq_failure.py",
        source_root / "explore" / "cma-fade-divergence" / "prompt012_longseq_audit.py",
        source_root / "explore" / "cma-fade-divergence" / "prompt013_swap_quality_q1.py",
        source_root / "common" / "_batch_metrics.py",
        LAB_ROOT / "tools" / "ml_detector_batch.py", HERE,
        queue_path, queue_path.with_name("candidate-map.yaml"),
    ]
    component_fp = hashlib.sha256("".join(_sha256(path) for path in source_files).encode()).hexdigest()
    source_snapshot = {str(path): _sha256(path) for path in source_files}
    source_hash = hashlib.sha256(json.dumps(source_snapshot, sort_keys=True).encode()).hexdigest()
    manifest = {
        "run_id": f"B001-{uuid.uuid4().hex}", "batch_id": "B001", "state": "BATCH_READY",
        "baseline_id": "baseline.standard_cma.godard_z", "component_id": "component.ml_degradation_detector.batch-v1",
        "baseline_fingerprint": _sha256(prompt_path),
        "component_fingerprint": component_fp, "queue_hash": _sha256(queue_path),
        "source_snapshot": source_snapshot, "source_hash": source_hash,
        "source_import_closure": "prompt013 module import closure frozen by per-file SHA above; no runtime source outside this list is permitted",
        "metric_contract_id": "metric.dual_qpsk.fixed-plus-pi.v1", "sandbox_only": True,
        "promotion_allowed": False, "evidence_status": "EXPLORATORY", "destination": "evidence_ledger",
        "contract": dict(contract),
        "parameter_sources": {
            "foundation": [".sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md#D040",
                           ".sessions/2026-07-10-dual-pol-osl-groundwork/verifications.md#V006"],
            "physical": {"source": str(source_root / "params.py"),
                          "assumption": "SimulationConfig.experiment.GAMMA_BAR_DEFAULT is used by the frozen generator"},
        },
        "environment_fingerprint": hashlib.sha256(
            f"{platform.platform()}|{sys.version}|{np.__version__}".encode()).hexdigest(),
        "direction_id": "dual-pol-osl", "family_id": batch_record.get("family_id"),
        "archetype_id": batch_record.get("archetype_id"),
        "candidate_ids": [item.get("candidate_id") for item in candidate_specs],
        "hypotheses": [item.get("hypothesis") for item in candidate_specs],
        "primary_metrics": contract.get("metrics", {}).get("primary", []),
        "diagnostic_metrics": contract.get("metrics", {}).get("diagnostics", []),
        "pass_kill_rules": batch_record.get("preregistered_outcomes", {}),
        "valid_domain": batch_record.get("valid_domain"),
        "equivalence_provenance": {
            "source_pointer": str(prompt_path),
            "entry": "run_cma_diagnostic(mode='standard')",
            "gradient": "Godard-with-z",
            "evidence_pointer": ".sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md#D040",
        },
    }
    registry = {
        manifest["baseline_id"]: {"status": "canonical", "fingerprint": manifest["baseline_fingerprint"]},
        manifest["component_id"]: {"status": "canonical", "fingerprint": component_fp},
    }
    controller = controller_module.GovernanceController(registry=registry, audit_path=output_dir / "controller-audit.jsonl")
    executed = controller.execute(manifest, action="RUN",
                                  operation=lambda: run_dataset(contract,
                                                               realization_generator=realization_generator,
                                                               baseline_runner=baseline_runner,
                                                               source_root=source_root))
    gate = controller_module.EvidenceGate(
        audit_path=output_dir / "controller-audit.jsonl",
        destinations={"evidence_ledger": output_dir / "evidence_ledger.jsonl"},
    ).submit(executed, destination="evidence_ledger")
    result = _json({"manifest": manifest, "execution": executed, "gate": gate})
    (output_dir / "manifest.json").write_text(json.dumps(_json(manifest), indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    return result


__all__ = ["load_contract", "run_paired_cell", "run_dataset", "run_governed"]
