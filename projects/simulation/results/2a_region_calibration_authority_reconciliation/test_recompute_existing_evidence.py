from pathlib import Path
import importlib.util

import pytest


HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "recompute_existing_evidence.py"


def test_recompute_script_exists():
    assert SCRIPT.is_file(), "deterministic recompute entry point is missing"


def load_module():
    spec = importlib.util.spec_from_file_location("recompute_existing_evidence", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cluster_summary_uses_seed_as_inference_unit():
    module = load_module()
    summary = module.summarize([0.1, 0.2, 0.3])
    assert summary["n_clusters"] == 3
    assert summary["mean_db"] == pytest.approx(0.2)
    assert summary["ci95"][0] < 0.2 < summary["ci95"][1]


def test_existing_evidence_recomputes_frozen_authority_numbers():
    module = load_module()
    repo_root = HERE.parents[3]
    report = module.build_report(repo_root)

    p01 = report["p01"]
    assert p01["adapter_resolved_count"] == 4
    assert p01["harm_cell_count"] == 5
    assert p01["material_safety_degradation_count"] == 1

    p02 = report["p02"]
    assert p02["weakretune_minus_adapter"]["mean_db"] == pytest.approx(0.4538673652)
    assert p02["weakretune_minus_adapter"]["ci95"] == pytest.approx(
        [0.4340368738, 0.4736978566]
    )
    assert p02["cand_rank_minus_weakretune"]["mean_db"] == pytest.approx(-0.0960851354)
    assert p02["cand_rank_minus_weakretune"]["ci95"] == pytest.approx(
        [-0.1027456689, -0.0894246019]
    )
    assert p02["deployable_region_identity"]["runtime_region_input"] is False
    assert p02["deployable_region_identity"]["distinct_calibration_actions"] == 1
    assert p02["chronology"]["pristine_30_seed_heldout"] is False
    assert p02["branch_occupancy_effect"]["comparison"] == "weakretune_vs_cand_rank"
    assert p02["branch_occupancy_effect"]["nonzero_occupancy_count"] == 207
    assert p02["branch_occupancy_effect"]["cell_seed_clusters"] == 210

    t004 = report["t004"]
    assert t004["dev_table"]["global_B1"]["mean_db"] == pytest.approx(0.1368759553)
    assert t004["dev_table"]["region_B2"]["mean_db"] == pytest.approx(0.3084554511)
    assert t004["dev_table"]["online_M"]["mean_db"] == pytest.approx(0.2674971826)
    assert t004["heldout_exists"] is False
    assert not any(t004["heldout_paths"].values())

    assert report["semantic_gate"]["all_pass"] is False
    assert report["terminal"] == "SUPPORTING_ONLY"
