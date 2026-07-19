from __future__ import annotations

import hashlib
import importlib.util
import subprocess
from pathlib import Path

import yaml


LAB_ROOT = Path(__file__).parents[1]
REPO_ROOT = LAB_ROOT.parents[2]
SCOUT_ROOT = LAB_ROOT / "scout" / "P03-U19-residual-headroom"
SNAPSHOT_ROOT = SCOUT_ROOT / "source-snapshots" / "interface-smoke-v2"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_recovered_source_snapshot_is_content_addressed_and_provenance_bearing(tmp_path: Path) -> None:
    manifest = yaml.safe_load((SNAPSHOT_ROOT / "source-snapshot.v1.yaml").read_text(encoding="utf-8"))
    patch_path = SNAPSHOT_ROOT / "gg-time-prefix-stability.patch"
    assert manifest["status"] == "IMMUTABLE_SOURCE_SNAPSHOT"
    assert manifest["base"]["simulation_commit"] == "65db35bb15dd9b6da0ad05ea5835054ad4277485"
    assert manifest["base"]["scout_orchestration_commit"] == "c38ff0d6648d5320d49ea199acbed68e14e40065"
    assert manifest["base"]["sha256"] == "1ffd6af106181a6e589d674e0508bb8cc0ea3496e2dae1f7364bb47f2a842db5"
    assert manifest["patch"]["sha256"] == _sha(patch_path)
    assert manifest["materialized"]["sha256"] == "92eaa6a6c92e72122a1921a0c844160bbf5b4ee7bc2527fc66da468187af9786"
    assert manifest["materialized"]["git_blob_oid"] == "9155de058912593f487d95fb4e3aecf25ae1617c"
    assert subprocess.run(
        ["git", "cat-file", "-e", f"{manifest['materialized']['git_blob_oid']}^{{blob}}"],
        cwd=REPO_ROOT,
    ).returncode == 0
    assert len(manifest["provenance_attestations"]) >= 4


def test_source_equivalence_gate_reconstructs_historical_z_window(tmp_path: Path) -> None:
    module = _load(SCOUT_ROOT / "run_source_equivalence.py", "p03_source_equivalence_test")
    report = module.run(
        contract_path=SCOUT_ROOT / "source-equivalence-contract.v1.yaml",
        output_dir=tmp_path / "equivalence",
    )
    assert report["status"] == "PASS"
    assert report["source_materialization"]["materialized_sha256"] == "92eaa6a6c92e72122a1921a0c844160bbf5b4ee7bc2527fc66da468187af9786"
    assert report["equivalence"]["z_window_sha256"] == "3d99d4fef5f3749d2047816b8bc655affc207f307bafc808b6de887b88ca64f7"
    assert report["equivalence"]["exact_output_equal"] is True
    assert report["checks"]["godard_with_z_identity"] == "PASS"
    assert report["checks"]["godard_with_z_formula_numeric"] == "PASS"
    assert report["checks"]["deterministic_rerun"] == "PASS"
    closure = yaml.safe_load((tmp_path / "equivalence" / "source-closure.yaml").read_text(encoding="utf-8"))
    assert closure["simulation_source_commit"] == "65db35bb15dd9b6da0ad05ea5835054ad4277485"
    assert closure["scout_orchestration_commit"] == "c38ff0d6648d5320d49ea199acbed68e14e40065"
    assert closure["materialized_override"]["sha256"] == "92eaa6a6c92e72122a1921a0c844160bbf5b4ee7bc2527fc66da468187af9786"
