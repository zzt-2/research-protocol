from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import yaml


LAB_ROOT = Path(__file__).parents[1]
SCRIPT = LAB_ROOT / "scout" / "P03-U19-residual-headroom" / "run_interface_smoke.py"
CONTRACT = LAB_ROOT / "scout" / "P03-U19-residual-headroom" / "interface-smoke-contract.v1.yaml"
RECOVERY_SCRIPT = LAB_ROOT / "scout" / "P03-U19-residual-headroom" / "run_source_equivalence.py"
RECOVERY_CONTRACT = LAB_ROOT / "scout" / "P03-U19-residual-headroom" / "source-equivalence-contract.v1.yaml"


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_authentic_one_cell_smoke_isolated_and_deterministic(tmp_path: Path) -> None:
    first_dir = tmp_path / "first"
    second_dir = tmp_path / "second"
    command = ["python", str(RECOVERY_SCRIPT), "--contract", str(RECOVERY_CONTRACT), "--output-dir"]
    first = subprocess.run(command + [str(first_dir)], cwd=LAB_ROOT.parents[2], capture_output=True, text=True)
    assert first.returncode == 0, first.stdout + first.stderr
    second = subprocess.run(command + [str(second_dir)], cwd=LAB_ROOT.parents[2], capture_output=True, text=True)
    assert second.returncode == 0, second.stdout + second.stderr
    report_a = yaml.safe_load((first_dir / "report.yaml").read_text(encoding="utf-8"))
    report_b = yaml.safe_load((second_dir / "report.yaml").read_text(encoding="utf-8"))
    assert report_a["status"] == "PASS"
    assert report_a["equivalence"]["exact_output_equal"] is True
    assert report_a["equivalence"] == report_b["equivalence"]
    assert report_a["checks"]["godard_with_z_identity"] == "PASS"
    assert report_a["checks"]["csi_none"] == "PASS"
    assert report_a["checks"]["deterministic_rerun"] == "PASS"
    for name in ("z-window.json", "source-closure.yaml", "report.yaml"):
        assert (first_dir / name).is_file()
        assert _hash(first_dir / name) == _hash(second_dir / name)
    contract = yaml.safe_load(RECOVERY_CONTRACT.read_text(encoding="utf-8"))
    assert contract["n_symbols"] == 512
    for key in ("alpha", "beta", "f_g_hz", "sop_rate", "gamma_bar", "block", "t_s", "method", "seed", "cma_mu", "cma_taps", "r2", "cma_block_size", "eval_start", "eval_end"):
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
