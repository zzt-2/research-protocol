"""Run the preregistered P03 residual-headroom Scout without ML training."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import numpy as np
import yaml


HERE = Path(__file__).resolve()
SCOUT_ROOT = HERE.parent
REPO_ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()).resolve()


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _sha(path: Path) -> str:
    return hashlib.sha256(_canonical_source_bytes(path)).hexdigest()


def _canonical_source_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def _git_blob_oid(path: Path) -> str:
    return subprocess.run(
        ["git", "hash-object", "--stdin"],
        cwd=REPO_ROOT,
        input=_canonical_source_bytes(path),
        capture_output=True,
        check=True,
    ).stdout.decode("ascii").strip()


def _verify_runtime_snapshot(contract: dict[str, Any]) -> dict[str, Any]:
    """Bind every probe runtime dependency to an already-stored Git blob."""
    manifest_path = (SCOUT_ROOT / contract["runtime_source_snapshot"]).resolve()
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("immutability") != "each file is stored as an exact raw Git blob before scientific execution":
        raise RuntimeError("runtime source snapshot lacks the required immutability declaration")
    verified: list[dict[str, str]] = []
    for record in manifest.get("files", []):
        relative = Path(str(record["path"]))
        path = (SCOUT_ROOT / relative).resolve()
        if SCOUT_ROOT not in path.parents:
            raise RuntimeError(f"runtime snapshot path escapes Scout root: {relative}")
        digest = _sha(path)
        oid = _git_blob_oid(path)
        if digest != str(record["sha256"]) or oid != str(record["git_blob_oid"]):
            raise RuntimeError(f"runtime source snapshot mismatch: {relative}")
        subprocess.run(
            ["git", "cat-file", "-e", f"{oid}^{{blob}}"], cwd=REPO_ROOT,
            capture_output=True, text=True, check=True,
        )
        verified.append({"path": relative.as_posix(), "sha256": digest, "git_blob_oid": oid})
    if not verified:
        raise RuntimeError("runtime source snapshot is empty")
    manifest_oid = _git_blob_oid(manifest_path)
    subprocess.run(
        ["git", "cat-file", "-e", f"{manifest_oid}^{{blob}}"], cwd=REPO_ROOT,
        capture_output=True, text=True, check=True,
    )
    return {
        "manifest_path": manifest_path.relative_to(SCOUT_ROOT).as_posix(),
        "manifest_sha256": _sha(manifest_path),
        "manifest_git_blob_oid": manifest_oid,
        "files": verified,
    }


def _json(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json(item) for item in value]
    if isinstance(value, np.ndarray):
        return _json(value.tolist())
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, complex):
        return [float(value.real), float(value.imag)]
    return value


def _require_contract(contract: dict[str, Any]) -> None:
    required = {
        "schema_version", "contract_id", "mode", "performance_experiment", "b004", "ml_training",
        "queue_registry", "paper_material", "source_snapshot", "source_equivalence_contract",
        "runtime_source_snapshot", "seeds",
        "n_symbols", "alpha", "beta", "f_g_hz", "sop_rate", "gamma_bar", "block", "t_s", "method",
        "cma_mu", "cma_taps", "r2", "cma_block_size", "eval_start", "calibration_end", "eval_end",
        "fade_threshold_h", "clip_norm", "csi_access_class", "constellation_amplitude_per_axis",
        "affine_ridge", "tail_energy_threshold", "definitions", "exit_states", "valid_domain",
    }
    missing = sorted(required - set(contract))
    if missing:
        raise ValueError(f"probe contract missing explicit fields: {missing}")
    if contract["mode"] != "SCOUT_DIAGNOSTIC_ONLY" or contract["performance_experiment"] is not False:
        raise ValueError("probe must remain a Scout diagnostic")
    if any(bool(contract[key]) for key in ("b004", "ml_training", "queue_registry", "paper_material")):
        raise ValueError("probe contract requests a forbidden side effect")
    if contract["csi_access_class"] != "CSI_NONE":
        raise ValueError("only the closed CSI_NONE path is legal")
    if [int(seed) for seed in contract["seeds"]] != list(range(11, 21)):
        raise ValueError("probe seeds must be exactly 11 through 20")
    if not int(contract["eval_start"]) < int(contract["calibration_end"]) < int(contract["eval_end"]):
        raise ValueError("calibration and evaluation ranges must be non-empty and ordered")


def _decode_window(window: dict[str, Any]) -> np.ndarray:
    streams = []
    for name in ("zX", "zY"):
        pairs = np.asarray(window["streams"][name], dtype=np.float64)
        streams.append(np.asarray(pairs[:, 0] + 1j * pairs[:, 1], dtype=np.complex128))
    output = np.column_stack(streams)
    if output.shape != tuple(window["shape"]) or not np.isfinite(output).all():
        raise RuntimeError("z-window decode failed shape/dtype/finiteness gate")
    return output


def _cell(
    *,
    seed: int,
    contract: dict[str, Any],
    generator: Any,
    runner: Any,
    adapter: Any,
    evaluator: Any,
    run_b001_path: Path,
) -> dict[str, Any]:
    realization = generator(
        int(contract["n_symbols"]), float(contract["alpha"]), float(contract["beta"]), float(contract["f_g_hz"]),
        sop_rate=float(contract["sop_rate"]), seed=int(seed), gamma_bar=float(contract["gamma_bar"]),
        block=int(contract["block"]), t_s=float(contract["t_s"]), method=str(contract["method"]),
    )
    cfg = SimpleNamespace(
        mu=float(contract["cma_mu"]), taps=int(contract["cma_taps"]), r2=float(contract["r2"]),
        block_size=int(contract["cma_block_size"]), eval_start=int(contract["eval_start"]),
        eval_end=int(contract["eval_end"]), fade_threshold_h=float(contract["fade_threshold_h"]),
        clip_norm=float(contract["clip_norm"]),
    )
    raw = runner({"rX": realization["rX"], "rY": realization["rY"]}, cfg, variant="baseline", return_blind_trace=True)
    if raw.get("provenance", {}).get("gradient") != "Godard-with-z":
        raise RuntimeError("standard-CMA identity gate failed")
    sequence_id = f"p03-residual-headroom-seed-{seed}"
    window = adapter.adapt_standard_cma_output(
        raw,
        sequence_id=sequence_id,
        symbol_start=int(contract["eval_start"]),
        symbol_end=int(contract["eval_end"]),
        equalizer_taps=int(contract["cma_taps"]),
        csi_access_class="CSI_NONE",
        source_id="run_b001._default_runner",
        source_hash=_sha(run_b001_path),
        receiver_estimated_csi=None,
    )
    z = _decode_window(window)
    split = int(contract["calibration_end"]) - int(contract["eval_start"])
    z_calibration, z_evaluation = z[:split], z[split:]
    start, middle, end = int(contract["eval_start"]), int(contract["calibration_end"]), int(contract["eval_end"])
    truth_calibration = np.column_stack((realization["sX"][start:middle], realization["sY"][start:middle]))
    truth_evaluation = np.column_stack((realization["sX"][middle:end], realization["sY"][middle:end]))
    amplitude = float(contract["constellation_amplitude_per_axis"])
    nearest_corrected = z_evaluation
    nearest_predicted = evaluator.hard_qpsk(nearest_corrected, amplitude)
    blind = evaluator.blind_affine_compare(z_calibration, z_evaluation, ridge=float(contract["affine_ridge"]))
    oracle_corrected = evaluator.oracle_affine_bound(
        z_calibration, z_evaluation, truth_calibration, ridge=float(contract["affine_ridge"])
    )
    metrics = {
        "nearest_qpsk": evaluator.evaluate_dual_qpsk(
            nearest_predicted[:, 0], nearest_predicted[:, 1], truth_evaluation[:, 0], truth_evaluation[:, 1]
        ),
        "blind_affine": evaluator.evaluate_dual_qpsk(
            blind["predicted"][:, 0], blind["predicted"][:, 1], truth_evaluation[:, 0], truth_evaluation[:, 1]
        ),
        "oracle_affine_scoring_only": evaluator.evaluate_dual_qpsk(
            oracle_corrected[:, 0], oracle_corrected[:, 1], truth_evaluation[:, 0], truth_evaluation[:, 1]
        ),
    }
    nearest_residual = evaluator.residual_statistics(
        nearest_corrected, nearest_predicted, tail_energy_threshold=float(contract["tail_energy_threshold"])
    )
    blind_residual = evaluator.residual_statistics(
        blind["corrected"], blind["predicted"], tail_energy_threshold=float(contract["tail_energy_threshold"])
    )
    nearest_pi_ser = float(metrics["nearest_qpsk"]["pi_ser"])
    blind_pi_ser = float(metrics["blind_affine"]["pi_ser"])
    oracle_pi_ser = float(metrics["oracle_affine_scoring_only"]["pi_ser"])
    visible_headroom = max(nearest_pi_ser - oracle_pi_ser, 0.0)
    simple_gain = max(nearest_pi_ser - min(nearest_pi_ser, blind_pi_ser), 0.0)
    selected_residual = blind_residual if blind_pi_ser <= nearest_pi_ser else nearest_residual
    runtime_record = {
        "seed": int(seed),
        "sequence_id": sequence_id,
        "csi_access_class": "CSI_NONE",
        "calibration_range": {"start": start, "end_exclusive": middle},
        "evaluation_range": {"start": middle, "end_exclusive": end},
        "nearest_residual": nearest_residual,
        "blind_affine_residual": blind_residual,
    }
    return _json({
        "seed": int(seed),
        "standard_cma_calls": 1,
        "shared_realization": True,
        "runtime_record": runtime_record,
        "metrics": metrics,
        "visible_headroom": visible_headroom,
        "simple_analytic_gain": simple_gain,
        "analytic_coverage": 1.0 if visible_headroom == 0.0 else min(simple_gain / visible_headroom, 1.0),
        "headroom_error_unit": 1.0 / (2.0 * len(z_evaluation)),
        "residual": selected_residual,
        "residual_selection_for_scoring": "blind_affine" if blind_pi_ser <= nearest_pi_ser else "nearest_qpsk",
        "evaluation_only_truth_fields": ["sX", "sY"],
    })


def _history_guard() -> dict[str, bool]:
    batch_paths = [
        "projects/thesis-fso/direction-lab/batches/B001-20260717-live",
        "projects/thesis-fso/direction-lab/batches/B002-20260718-live",
        "projects/thesis-fso/direction-lab/batches/B003-20260718-live",
    ]
    changed = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", *batch_paths], cwd=REPO_ROOT).returncode != 0
    changed_index = subprocess.run(["git", "diff", "--cached", "--quiet", "HEAD", "--", *batch_paths], cwd=REPO_ROOT).returncode != 0
    b004 = any((REPO_ROOT / "projects/thesis-fso/direction-lab/batches").glob("B004*"))
    return {
        "B001_B002_B003_modified": bool(changed or changed_index),
        "B004_exists": bool(b004),
        "ML_trained": False,
        "queue_or_registry_created": False,
        "paper_material_written": False,
        "parameter_domain_expanded": False,
    }


def run(contract_path: Path, output_dir: Path) -> dict[str, Any]:
    contract_path = Path(contract_path).resolve()
    contract = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    _require_contract(contract)
    runtime_snapshot = _verify_runtime_snapshot(contract)
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    equivalence_module = _load(SCOUT_ROOT / "run_source_equivalence.py", "p03_probe_source_equivalence")
    evaluator = _load(SCOUT_ROOT / "probe_evaluator.py", "p03_probe_evaluator")
    equivalence_contract_path = SCOUT_ROOT / contract["source_equivalence_contract"]
    source_equivalence = equivalence_module.run(equivalence_contract_path, output_dir / "source-equivalence")
    equivalence_contract = yaml.safe_load(equivalence_contract_path.read_text(encoding="utf-8"))
    with equivalence_module.materialized_source(equivalence_contract) as (source_tree, materialization):
        archived_lab = source_tree / "projects/thesis-fso/direction-lab"
        run_b001_path = archived_lab / "tools/run_b001.py"
        run_b001 = _load(run_b001_path, "p03_probe_run_b001")
        adapter = _load(
            archived_lab / "scout/P03-U19-residual-headroom/z_window_adapter.py",
            "p03_probe_z_window_adapter",
        )
        source_root = source_tree / equivalence_contract["base_source_root"]
        generator = run_b001._default_generator(source_root)
        runner, _ = run_b001._default_runner(source_root)
        cells = [
            _cell(
                seed=int(seed), contract=contract, generator=generator, runner=runner,
                adapter=adapter, evaluator=evaluator, run_b001_path=run_b001_path,
            )
            for seed in contract["seeds"]
        ]
        loaded_closure = equivalence_module._source_closure(source_tree, materialization)
    summary = evaluator.summarize_probe(cells)
    guards = _history_guard()
    if any(guards.values()):
        raise RuntimeError(f"probe guard failed: {guards}")
    result = _json({
        "schema_version": "direction-lab.p03-residual-headroom-result.v1",
        "contract_id": contract["contract_id"],
        "source_equivalence": source_equivalence,
        "cells": cells,
        "summary": summary,
        "guards": guards,
        "interpretation_limit": "Scout diagnostic only; not MVE, Sandbox, Contract, Execute, or paper evidence",
    })
    payload = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=True, allow_nan=False) + "\n"
    (output_dir / "probe-result.json").write_text(payload, encoding="utf-8", newline="\n")
    (output_dir / "probe-summary.yaml").write_text(yaml.safe_dump(summary, sort_keys=False), encoding="utf-8", newline="\n")
    closure = {
        **loaded_closure,
        "immutable_probe_runtime_snapshot": runtime_snapshot,
        "probe_runtime_sources": {
            "run_residual_headroom_probe.py": _sha(HERE),
            "probe_evaluator.py": _sha(SCOUT_ROOT / "probe_evaluator.py"),
            "probe_contract": _sha(contract_path),
            "source_equivalence_contract": _sha(equivalence_contract_path),
        },
    }
    (output_dir / "source-closure.yaml").write_text(yaml.safe_dump(closure, sort_keys=False), encoding="utf-8", newline="\n")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, default=SCOUT_ROOT / "residual-headroom-probe-contract.v1.yaml")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.contract, args.output_dir)
    print(yaml.safe_dump(result["summary"], sort_keys=False))


if __name__ == "__main__":
    main()
