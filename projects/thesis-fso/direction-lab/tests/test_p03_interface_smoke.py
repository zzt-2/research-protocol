from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import yaml


LAB_ROOT = Path(__file__).parents[1]
SCRIPT = LAB_ROOT / "scout" / "P03-U19-residual-headroom" / "run_interface_smoke.py"
CONTRACT = LAB_ROOT / "scout" / "P03-U19-residual-headroom" / "interface-smoke-contract.v1.yaml"


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_authentic_one_cell_smoke_isolated_and_deterministic(tmp_path: Path) -> None:
    first_dir = tmp_path / "first"
    second_dir = tmp_path / "second"
    command = ["python", str(SCRIPT), "--contract", str(CONTRACT), "--output-dir"]
    first = subprocess.run(command + [str(first_dir)], cwd=LAB_ROOT.parents[2], capture_output=True, text=True)
    assert first.returncode == 0, first.stdout + first.stderr
    second = subprocess.run(command + [str(second_dir)], cwd=LAB_ROOT.parents[2], capture_output=True, text=True)
    assert second.returncode == 0, second.stdout + second.stderr
    report_a = yaml.safe_load((first_dir / "smoke-report.yaml").read_text(encoding="utf-8"))
    report_b = yaml.safe_load((second_dir / "smoke-report.yaml").read_text(encoding="utf-8"))
    assert report_a["status"] == "PASS"
    assert report_a["authentic_standard_cma"] is True
    assert report_a["performance_experiment"] is False
    assert report_a["csi_access_class"] == "CSI_NONE"
    assert report_a["runtime_artifact_hash"] == report_b["runtime_artifact_hash"]
    assert report_a["component_artifact_hash"] == report_b["component_artifact_hash"]
    artifact_names = {
        "z_window": "z-window.json",
        "analytic_comparator": "analytic-comparator.json",
        "residual_artifact": "residual-artifact.json",
    }
    for key, name in artifact_names.items():
        assert report_a["artifact_hashes"][key] == _hash(first_dir / name)
    for name in (*artifact_names.values(), "source-closure.yaml"):
        assert (first_dir / name).is_file()
    assert not (first_dir / "evidence_ledger.jsonl").exists()
    assert not (first_dir / "manifest.json").exists()

    contract = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
    assert contract["n_symbols"] == 512
    for key in ("alpha", "beta", "f_g_hz", "sop_rate", "gamma_bar", "block", "t_s", "method", "seed", "cma_mu", "cma_taps", "r2", "cma_block_size", "eval_start", "eval_end", "tail_energy_threshold"):
        assert key in contract


def test_smoke_refuses_unbound_or_implicit_contract(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text("schema_version: direction-lab.p03-interface-smoke.v1\n", encoding="utf-8")
    result = subprocess.run(
        ["python", str(SCRIPT), "--contract", str(bad), "--output-dir", str(tmp_path / "out")],
        cwd=LAB_ROOT.parents[2], capture_output=True, text=True,
    )
    assert result.returncode != 0
    assert "missing explicit contract fields" in (result.stdout + result.stderr)
