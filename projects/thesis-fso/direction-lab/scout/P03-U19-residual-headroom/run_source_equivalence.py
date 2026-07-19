"""Rebuild the historical P03 source closure from a commit plus immutable override."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any, Iterator

import numpy as np
import yaml


HERE = Path(__file__).resolve()
SCOUT_ROOT = HERE.parent
REPO_ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()).resolve()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _canonical_bytes(value: Any) -> bytes:
    # Historical artifact was materialized in this Windows checkout with a
    # single CRLF terminator.  Preserve that byte contract for exact SHA gate.
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False) + "\r\n").encode("utf-8")


def _run(command: list[str], *, cwd: Path) -> None:
    completed = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(f"command failed ({completed.returncode}): {' '.join(command)}\n{completed.stdout}{completed.stderr}")


def _materialize_historical_line_endings(path: Path, lf_only_lines: list[int]) -> None:
    """Reproduce the recorded Windows mixed-EOL bytes without reading the dirty source."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if len(lines) != 199:
        raise RuntimeError(f"unexpected recovered _gg_time.py line count: {len(lines)}")
    lf_only = {int(value) for value in lf_only_lines}
    payload = b"".join(
        line.encode("utf-8") + (b"\n" if index in lf_only else b"\r\n")
        for index, line in enumerate(lines, start=1)
    )
    path.write_bytes(payload)


def _normalize_lf(path: Path) -> None:
    payload = path.read_bytes().replace(b"\r\n", b"\n")
    path.write_bytes(payload)


@contextlib.contextmanager
def materialized_source(contract: dict[str, Any]) -> Iterator[tuple[Path, dict[str, Any]]]:
    """Yield a clean source tree materialized from the frozen commit and patch blob."""
    simulation_commit = str(contract["simulation_source_commit"])
    orchestration_commit = str(contract["scout_orchestration_commit"])
    patch_path = (SCOUT_ROOT / contract["snapshot_patch"]).resolve()
    manifest_path = (SCOUT_ROOT / contract["snapshot_manifest"]).resolve()
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="p03-source-") as temporary:
        root = Path(temporary).resolve()
        archive = root / "simulation-source.zip"
        _run([
            "git", "archive", "--format=zip", f"--output={archive}", simulation_commit,
            "projects/simulation",
        ], cwd=REPO_ROOT)
        with zipfile.ZipFile(archive) as handle:
            handle.extractall(root)
        archive.unlink()
        archive = root / "scout-orchestration.zip"
        _run([
            "git", "archive", "--format=zip", f"--output={archive}", orchestration_commit,
            "projects/thesis-fso/direction-lab/tools/run_b001.py",
            "projects/thesis-fso/direction-lab/scout/P03-U19-residual-headroom/z_window_adapter.py",
            "projects/thesis-fso/direction-lab/scout/P03-U19-residual-headroom/analytic_comparator.py",
            "projects/thesis-fso/direction-lab/scout/P03-U19-residual-headroom/residual_artifact.py",
        ], cwd=REPO_ROOT)
        with zipfile.ZipFile(archive) as handle:
            handle.extractall(root)
        archive.unlink()
        orchestration_paths = [
            root / "projects/thesis-fso/direction-lab/tools/run_b001.py",
            root / "projects/thesis-fso/direction-lab/scout/P03-U19-residual-headroom/z_window_adapter.py",
            root / "projects/thesis-fso/direction-lab/scout/P03-U19-residual-headroom/analytic_comparator.py",
            root / "projects/thesis-fso/direction-lab/scout/P03-U19-residual-headroom/residual_artifact.py",
        ]
        for orchestration_path in orchestration_paths:
            _normalize_lf(orchestration_path)
        target = root / contract["materialized_override"]["path"]
        base_hash = sha256(target)
        allowed_base_hashes = {manifest["base"]["sha256"], manifest["base"]["windows_materialized_sha256"]}
        if base_hash not in allowed_base_hashes:
            raise RuntimeError(f"base _gg_time.py hash mismatch: {base_hash}")
        _run(["git", "apply", "--unsafe-paths", f"--directory={root}", str(patch_path)], cwd=REPO_ROOT)
        _materialize_historical_line_endings(target, manifest["materialized"]["lf_only_lines"])
        materialized_hash = sha256(target)
        expected = str(contract["materialized_override"]["sha256"])
        if materialized_hash != expected:
            raise RuntimeError(f"materialized _gg_time.py hash mismatch: {materialized_hash} != {expected}")
        blob_oid = subprocess.run(
            ["git", "hash-object", "--no-filters", str(target)], cwd=REPO_ROOT, capture_output=True, text=True, check=True
        ).stdout.strip()
        expected_oid = str(contract["materialized_override"]["git_blob_oid"])
        if blob_oid != expected_oid:
            raise RuntimeError(f"materialized Git blob mismatch: {blob_oid} != {expected_oid}")
        yield root, {
            "simulation_source_commit": simulation_commit,
            "scout_orchestration_commit": orchestration_commit,
            "base_git_blob_sha256": manifest["base"]["sha256"],
            "base_materialized_sha256": base_hash,
            "patch_sha256": sha256(patch_path),
            "snapshot_manifest_sha256": sha256(manifest_path),
            "materialized_sha256": materialized_hash,
            "materialized_git_blob_oid": blob_oid,
        }


def _verify_standard_cma_formula(module: Any) -> None:
    """Numerically identify the exact Godard-with-z update, not its label alone."""
    r_x = np.asarray([
        [1.0 + 0.2j, -0.4 + 0.7j, 0.3 - 0.9j],
        [0.2 - 0.5j, 0.8 + 0.1j, -0.6 + 0.4j],
        [-0.7 + 0.3j, 0.5 - 0.8j, 0.9 + 0.2j],
        [0.6 + 0.6j, -0.2 - 0.4j, 0.1 + 0.7j],
    ], dtype=np.complex128)
    r_y = np.asarray([
        [-0.3 + 0.4j, 0.9 - 0.1j, 0.2 + 0.5j],
        [0.7 + 0.2j, -0.5 + 0.6j, 0.4 - 0.3j],
        [0.1 - 0.8j, 0.3 + 0.9j, -0.7 + 0.2j],
        [-0.4 - 0.2j, 0.6 + 0.5j, 0.8 - 0.6j],
    ], dtype=np.complex128)
    z_x = np.asarray([0.3 + 0.8j, -0.6 + 0.2j, 0.9 - 0.4j, -0.2 - 0.7j])
    z_y = np.asarray([-0.5 + 0.6j, 0.4 + 0.3j, -0.8 - 0.1j, 0.7 - 0.5j])
    r2, mu = 1.0, 0.013
    scalar, standard = module._cma_deltas(r_x, r_y, z_x, z_y, r2, mu)
    e_x, e_y = r2 - np.abs(z_x) ** 2, r2 - np.abs(z_y) ** 2
    expected = {
        "wxx": mu * np.mean((e_x * z_x)[:, None] * np.conj(r_x), axis=0),
        "wxy": mu * np.mean((e_x * z_x)[:, None] * np.conj(r_y), axis=0),
        "wyx": mu * np.mean((e_y * z_y)[:, None] * np.conj(r_x), axis=0),
        "wyy": mu * np.mean((e_y * z_y)[:, None] * np.conj(r_y), axis=0),
    }
    for name in expected:
        np.testing.assert_allclose(standard[name], expected[name], rtol=0.0, atol=1e-15)
    if all(np.allclose(standard[name], scalar[name], rtol=0.0, atol=1e-15) for name in expected):
        raise RuntimeError("standard-CMA numeric identity collapsed to scalar-error update")


def _generate_window(source_tree: Path, contract: dict[str, Any], suffix: str) -> tuple[dict[str, Any], dict[str, Any]]:
    archived_lab = source_tree / "projects" / "thesis-fso" / "direction-lab"
    run_b001 = _load(archived_lab / "tools" / "run_b001.py", f"p03_recovered_run_b001_{suffix}")
    adapter = _load(
        archived_lab / "scout" / "P03-U19-residual-headroom" / "z_window_adapter.py",
        f"p03_recovered_adapter_{suffix}",
    )
    source_root = source_tree / contract["base_source_root"]
    generator = run_b001._default_generator(source_root)
    runner, config_factory = run_b001._default_runner(source_root)
    _verify_standard_cma_formula(runner._frozen_module)
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
    raw = runner(receiver_input, cfg, variant="baseline", return_blind_trace=True)
    if raw.get("provenance", {}).get("gradient") != "Godard-with-z":
        raise RuntimeError("baseline identity is not standard-CMA Godard-with-z")
    window = adapter.adapt_standard_cma_output(
        raw,
        sequence_id="p03-interface-smoke-cell-001",
        symbol_start=int(contract["eval_start"]),
        symbol_end=int(contract["eval_end"]),
        equalizer_taps=int(contract["cma_taps"]),
        csi_access_class="CSI_NONE",
        source_id="run_b001._default_runner",
        source_hash=sha256(archived_lab / "tools" / "run_b001.py"),
        receiver_estimated_csi=None,
    )
    return window, {"realization": realization, "raw": raw, "source_tree": source_tree}


def _source_closure(source_tree: Path, materialization: dict[str, Any]) -> dict[str, Any]:
    files: dict[str, str] = {}
    for module in list(sys.modules.values()):
        path_text = getattr(module, "__file__", None)
        if not path_text:
            continue
        path = Path(path_text).resolve()
        try:
            relative = path.relative_to(source_tree).as_posix()
        except ValueError:
            continue
        if path.is_file() and path.suffix == ".py":
            files[relative] = sha256(path)
    return {
        "schema_version": "direction-lab.p03-source-closure.v2",
        "simulation_source_commit": materialization["simulation_source_commit"],
        "scout_orchestration_commit": materialization["scout_orchestration_commit"],
        "materialized_override": {
            "path": "projects/simulation/common/_gg_time.py",
            "sha256": materialization["materialized_sha256"],
            "git_blob_oid": materialization["materialized_git_blob_oid"],
            "patch_sha256": materialization["patch_sha256"],
        },
        "loaded_project_files": [{"path": path, "sha256": digest} for path, digest in sorted(files.items())],
    }


def run(contract_path: Path, output_dir: Path) -> dict[str, Any]:
    contract_path = Path(contract_path).resolve()
    contract = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    with materialized_source(contract) as (source_tree, materialization):
        first, _ = _generate_window(source_tree, contract, "a")
        second, _ = _generate_window(source_tree, contract, "b")
        first_bytes = _canonical_bytes(first)
        second_bytes = _canonical_bytes(second)
        digest = hashlib.sha256(first_bytes).hexdigest()
        expected = str(contract["historical_z_window"]["sha256"])
        if first_bytes != second_bytes:
            raise RuntimeError("recovered source is not deterministic")
        if digest != expected:
            raise RuntimeError(f"historical z-window equivalence failed: {digest} != {expected}")
        (output_dir / "z-window.json").write_bytes(first_bytes)
        closure = _source_closure(source_tree, materialization)
        (output_dir / "source-closure.yaml").write_text(yaml.safe_dump(closure, sort_keys=False), encoding="utf-8")
    report = {
        "schema_version": "direction-lab.p03-source-equivalence-report.v1",
        "status": "PASS",
        "source_materialization": materialization,
        "equivalence": {
            "historical_z_window_sha256": expected,
            "z_window_sha256": digest,
            "exact_output_equal": True,
        },
        "checks": {
            "source_snapshot_sha256": "PASS",
            "materialized_git_blob_identity": "PASS",
            "godard_with_z_identity": "PASS",
            "godard_with_z_formula_numeric": "PASS",
            "shape_dtype_finiteness_time_boundary": "PASS",
            "csi_none": "PASS",
            "oracle_future_posthoc_rejection": "PASS",
            "deterministic_rerun": "PASS",
        },
        "scope": "source equivalence only; no performance or scientific conclusion",
    }
    (output_dir / "report.yaml").write_text(yaml.safe_dump(report, sort_keys=False), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, default=SCOUT_ROOT / "source-equivalence-contract.v1.yaml")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    print(yaml.safe_dump(run(args.contract, args.output_dir), sort_keys=False))


if __name__ == "__main__":
    main()
