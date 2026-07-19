from __future__ import annotations

import hashlib
from pathlib import Path

import yaml


LAB_ROOT = Path(__file__).parents[1]
ROOT = LAB_ROOT / "scout" / "P03-U19-residual-headroom"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def test_candidate_component_snapshot_fingerprints_real_files() -> None:
    snapshot = yaml.safe_load((ROOT / "candidate-components.v1.yaml").read_text(encoding="utf-8"))
    assert snapshot["status"] == "scout-candidate"
    assert snapshot["registry"] is False
    assert snapshot["queue_binding"] is None
    assert len(snapshot["components"]) == 4
    for component in snapshot["components"]:
        path = LAB_ROOT / component["path"]
        assert path.is_file()
        assert component["sha256"] == _sha(path)
        assert component["canonical"] is False


def test_scout_contract_and_readiness_report_close_only_csi_none_scout_gate() -> None:
    contract = yaml.safe_load((ROOT / "scout-contract.v2.yaml").read_text(encoding="utf-8"))
    report = yaml.safe_load((ROOT / "readiness-report.yaml").read_text(encoding="utf-8"))
    assert contract["status"] == "CLOSED"
    assert contract["current"] is False
    assert contract["outcome"]["primary_verdict"] == "P03_ANALYTIC_COVERAGE_GE_90"
    assert contract["sandbox_status"] == "NOT_ENTERED"
    assert contract["information_access"]["CSI_NONE"]["status"] == "BOUND_AND_SMOKED"
    assert contract["information_access"]["RECEIVER_ESTIMATED_CSI"]["status"] == "DECLARED_NOT_BOUND"
    assert report["interface_readiness_verdict"] == "P03_SCOUT_CONTRACT_READY"
    assert report["final_verdict"] == "P03_ANALYTIC_COVERAGE_GE_90"
    assert report["queue_created"] is False
    assert report["b004_started"] is False
    assert report["receiver_state_changed"] is False
    assert all(package["status"] == "PASS" for package in report["work_packages"])
    assert report["sandbox_prerequisites"] == "NOT_APPLICABLE_P03_STOPPED_WITHOUT_ML"
    assert report["post_probe_closure_reason"].startswith("Exact source recovery")
