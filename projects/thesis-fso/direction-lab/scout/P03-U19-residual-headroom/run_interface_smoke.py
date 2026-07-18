"""Run the isolated, deterministic P03 interface smoke (never a batch runner)."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
import yaml


HERE = Path(__file__).resolve()
SCOUT_ROOT = HERE.parent
LAB_ROOT = SCOUT_ROOT.parents[1]
REPO_ROOT = LAB_ROOT.parents[2]
RUN_B001 = LAB_ROOT / "tools" / "run_b001.py"
DEFAULT_CONTRACT = SCOUT_ROOT / "interface-smoke-contract.v1.yaml"
_HISTORY_GUARD = {
    "b002_batch_synthesis": ("projects/thesis-fso/direction-lab/batches/B002-20260718-live/batch-synthesis.md", "4763eedb42675155c38162bf397e1eb42b1521e8b71a72c1c0a9d25742b33587"),
    "b002_status": ("projects/thesis-fso/direction-lab/batches/B002-20260718-live/execution-status.yaml", "3a23eb3ac82f3feae50e9bb120ec1f5f0fc8578d141bb2e715f254bca3e1557e"),
    "b002_manifest": ("projects/thesis-fso/direction-lab/batches/B002-20260718-live/manifest.json", "f1b4f205bdb3a40b518a36bdca5e8c02760a9613313d4d10b2b4fead22db4f98"),
    "b002_result": ("projects/thesis-fso/direction-lab/batches/B002-20260718-live/result.json", "bb291d4efb93d6bc7c2de4c9c110a4c7a519c19ad3827fbb3c51a7337f0fa22c"),
    "b002_verifier": ("projects/thesis-fso/direction-lab/batches/B002-20260718-live/verifier-report.md", "fba1fa36d1f3c13d914cabc7ee921657a09bffbb698c75ba2ef488868cb5681d"),
    "b003_batch_synthesis": ("projects/thesis-fso/direction-lab/batches/B003-20260718-live/batch-synthesis.md", "350960ca64ddb2a8b91d0aff733620d4ceb15d9d711751d2e089079657963adf"),
    "b003_status": ("projects/thesis-fso/direction-lab/batches/B003-20260718-live/execution-status.yaml", "5612a8187c5aa616528249eee3d30e3cf72b48f0afddd29a18e09b4fa011ba8d"),
    "b003_manifest": ("projects/thesis-fso/direction-lab/batches/B003-20260718-live/manifest.json", "5d4471fde14880f25c5674068059ce0b3b58cb750f8b0e0693100eaa74d1db13"),
    "b003_result": ("projects/thesis-fso/direction-lab/batches/B003-20260718-live/result.json", "865cf0c344808540f0b54cb91c82ddd33bec6b6bb8f280197407fe8de67e0bfc"),
    "b003_verifier": ("projects/thesis-fso/direction-lab/batches/B003-20260718-live/verifier-report.md", "12270bc372de6e69f4cd30fd6c6b58d033b098563d36dd48399e97388dbc8ba2"),
    "canonical_state": ("projects/thesis-fso/direction-lab/canonical-state.yaml", "5967ea38e676b46cb092c98060bec5b470b5a03625f21e65218cf3b2ae3a88af"),
}


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _json(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _json(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json(v) for v in value]
    if isinstance(value, np.ndarray):
        return _json(value.tolist())
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    return value


def _write_json(path: Path, value: Any) -> str:
    payload = json.dumps(_json(value), sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False) + "\n"
    encoded = payload.encode("utf-8")
    path.write_bytes(encoded)
    return hashlib.sha256(encoded).hexdigest()


def _require_contract(contract: dict[str, Any]) -> None:
    required = {
        "schema_version", "contract_id", "mode", "performance_experiment", "source_root",
        "n_symbols", "alpha", "beta", "f_g_hz", "sop_rate", "gamma_bar", "block", "t_s", "method",
        "seed", "cma_mu", "cma_taps", "r2", "cma_block_size", "eval_start", "eval_end",
        "fade_threshold_h", "clip_norm", "csi_access_class", "constellation_amplitude_per_axis",
        "tail_energy_threshold", "valid_domain", "forbidden_runtime_inputs",
    }
    missing = sorted(required - set(contract))
    if missing:
        raise ValueError(f"missing explicit contract fields: {missing}")
    if contract["mode"] != "interface_smoke_only" or contract["performance_experiment"] is not False:
        raise ValueError("contract must be an interface smoke and performance_experiment=false")
    if contract["csi_access_class"] != "CSI_NONE":
        raise ValueError("this smoke only binds the CSI_NONE comparator")
    if int(contract["eval_end"]) - int(contract["eval_start"]) <= 0:
        raise ValueError("evaluation range must be explicit and non-empty")


def _history_guard() -> dict[str, str]:
    observed: dict[str, str] = {}
    for label, (relative, expected) in _HISTORY_GUARD.items():
        path = REPO_ROOT / relative
        if not path.is_file():
            raise RuntimeError(f"history guard missing: {relative}")
        actual = _sha(path)
        if actual != expected:
            raise RuntimeError(f"history guard mismatch for {relative}: {actual} != {expected}")
        observed[label] = actual
    if (LAB_ROOT / "batches" / "B004").exists():
        raise RuntimeError("B004 must not exist or be started during interface smoke")
    return observed


def _source_closure(run_b001: Any, runner: Any, contract_path: Path, local_paths: list[Path], source_root: Path) -> dict[str, Any]:
    paths: set[Path] = {RUN_B001.resolve(), contract_path.resolve()}
    paths.update(path.resolve() for path in local_paths)
    for path_text in getattr(runner, "_source_files", ()):
        paths.add(Path(path_text).resolve())
    frozen = getattr(runner, "_frozen_module", None)
    if frozen is not None and getattr(frozen, "__file__", None):
        paths.add(Path(frozen.__file__).resolve())
    source_root = source_root.resolve()
    for module in list(sys.modules.values()):
        path_text = getattr(module, "__file__", None)
        if path_text:
            path = Path(path_text).resolve()
            if source_root in path.parents and path.suffix == ".py":
                paths.add(path)
    files = [{"path": str(path), "sha256": _sha(path)} for path in sorted(paths) if path.is_file()]
    return {"schema_version": "direction-lab.source-closure.v1", "files": files}


def run(contract_path: Path, output_dir: Path) -> dict[str, Any]:
    contract = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    if not isinstance(contract, dict):
        raise ValueError("contract must be a mapping")
    _require_contract(contract)
    history = _history_guard()
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    run_b001 = _load(RUN_B001, "p03_interface_smoke_run_b001")
    adapter = _load(SCOUT_ROOT / "z_window_adapter.py", "p03_interface_smoke_adapter")
    comparator = _load(SCOUT_ROOT / "analytic_comparator.py", "p03_interface_smoke_comparator")
    residual = _load(SCOUT_ROOT / "residual_artifact.py", "p03_interface_smoke_residual")
    source_root = (REPO_ROOT / contract["source_root"]).resolve()
    generator = run_b001._default_generator(source_root)
    runner, config_factory = run_b001._default_runner(source_root)
    realization = generator(
        int(contract["n_symbols"]), float(contract["alpha"]), float(contract["beta"]), float(contract["f_g_hz"]),
        sop_rate=float(contract["sop_rate"]), seed=int(contract["seed"]), gamma_bar=float(contract["gamma_bar"]),
        block=int(contract["block"]), t_s=float(contract["t_s"]), method=str(contract["method"]),
    )
    cfg = config_factory(
        mu=float(contract["cma_mu"]), taps=int(contract["cma_taps"]), r2=float(contract["r2"]),
        block_size=int(contract["cma_block_size"]), eval_start=int(contract["eval_start"]),
        eval_end=int(contract["eval_end"]), fade_threshold_h=float(contract["fade_threshold_h"]),
        clip_norm=float(contract["clip_norm"]),
    )
    receiver_input = {"rX": realization["rX"], "rY": realization["rY"]}
    raw_a = runner(receiver_input, cfg, variant="baseline", return_blind_trace=True)
    raw_b = runner(receiver_input, cfg, variant="baseline", return_blind_trace=True)
    source_hash = _sha(RUN_B001)
    window_a = adapter.adapt_standard_cma_output(
        raw_a, sequence_id="p03-interface-smoke-cell-001", symbol_start=int(contract["eval_start"]),
        symbol_end=int(contract["eval_end"]), equalizer_taps=int(contract["cma_taps"]),
        csi_access_class="CSI_NONE", source_id="run_b001._default_runner", source_hash=source_hash,
        receiver_estimated_csi=None,
    )
    window_b = adapter.adapt_standard_cma_output(
        raw_b, sequence_id="p03-interface-smoke-cell-001", symbol_start=int(contract["eval_start"]),
        symbol_end=int(contract["eval_end"]), equalizer_taps=int(contract["cma_taps"]),
        csi_access_class="CSI_NONE", source_id="run_b001._default_runner", source_hash=source_hash,
        receiver_estimated_csi=None,
    )
    if window_a != window_b:
        raise RuntimeError("standard-CMA repeated output is not deterministic")
    comparison = comparator.compare_qpsk_csi_none(
        window_a, constellation_amplitude=float(contract["constellation_amplitude_per_axis"])
    )
    comparison_repeat = comparator.compare_qpsk_csi_none(
        window_b, constellation_amplitude=float(contract["constellation_amplitude_per_axis"])
    )
    if comparison != comparison_repeat:
        raise RuntimeError("analytic comparator repeated output is not deterministic")
    artifact = residual.build_residual_artifact(
        [{"z_window": window_a, "comparator": comparison}],
        tail_energy_threshold=float(contract["tail_energy_threshold"]), evaluation_metrics_by_cell=[None],
        valid_domain=contract["valid_domain"], source_hashes={
            "standard_cma_runner": _sha(RUN_B001),
            "z_window_adapter": _sha(SCOUT_ROOT / "z_window_adapter.py"),
            "analytic_comparator": _sha(SCOUT_ROOT / "analytic_comparator.py"),
            "residual_artifact": _sha(SCOUT_ROOT / "residual_artifact.py"),
        },
    )
    closure = _source_closure(
        run_b001, runner, contract_path,
        [HERE, SCOUT_ROOT / "z_window_adapter.py", SCOUT_ROOT / "analytic_comparator.py", SCOUT_ROOT / "residual_artifact.py"],
        source_root,
    )
    z_hash = _write_json(output_dir / "z-window.json", window_a)
    comparator_hash = _write_json(output_dir / "analytic-comparator.json", comparison)
    residual_hash = _write_json(output_dir / "residual-artifact.json", artifact)
    (output_dir / "source-closure.yaml").write_text(yaml.safe_dump(closure, sort_keys=False), encoding="utf-8")
    component_hash = hashlib.sha256("".join(sorted(artifact["source_hashes"].values())).encode("ascii")).hexdigest()
    report = {
        "schema_version": "direction-lab.p03-interface-smoke-report.v1",
        "status": "PASS",
        "authentic_standard_cma": True,
        "performance_experiment": False,
        "csi_access_class": "CSI_NONE",
        "runtime_artifact_hash": artifact["runtime_artifact_hash"],
        "component_artifact_hash": component_hash,
        "artifact_hashes": {"z_window": z_hash, "analytic_comparator": comparator_hash, "residual_artifact": residual_hash},
        "source_closure_file": "source-closure.yaml",
        "history_guard": history,
        "checks": {
            "authentic_receiver_output": "PASS",
            "causal_z_window": "PASS",
            "oracle_future_posthoc_rejection": "PASS",
            "same_information_comparator": "PASS",
            "deterministic_rerun": "PASS",
            "one_cell_interface_only": "PASS",
        },
    }
    report_path = output_dir / "smoke-report.yaml"
    report_path.write_text(yaml.safe_dump(report, sort_keys=False), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = run(args.contract.resolve(), args.output_dir)
    except Exception as exc:  # command-line smoke must expose a crisp gate failure
        print(f"P03_INTERFACE_SMOKE_BLOCKED: {exc}", file=sys.stderr)
        return 2
    print(yaml.safe_dump(report, sort_keys=False), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
