from __future__ import annotations

import hashlib
from pathlib import Path

import yaml


ROOT = Path(__file__).parents[1]
V1_PATH = ROOT / "candidate-universe.yaml"
V2_PATH = ROOT / "candidate-universe.v2.yaml"


def load_universe(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    assert isinstance(data, dict)
    return data


def test_v2_is_lineage_safe_and_does_not_mutate_v1():
    data = load_universe(V2_PATH)

    assert data["schema_version"] == "direction-lab.candidate-universe.v2"
    assert data["lineage"]["supersedes_universe_id"] == (
        "universe.dual-pol-osl.ml.2026-07-17"
    )
    assert data["lineage"]["base_file_sha256"] == hashlib.sha256(
        V1_PATH.read_bytes()
    ).hexdigest()
    assert data["lineage"]["v1_immutable"] is True


def test_legacy_exclusions_become_conditional_neutral_candidates():
    data = load_universe(V2_PATH)
    reclassifications = {item["legacy_id"]: item for item in data["scope_reclassification"]}

    assert set(reclassifications) == {"F1", "G2", "U32"}
    for item in reclassifications.values():
        assert item["old_state"] == "known_out_of_scope_or_future_scope"
        assert item["new_state"] == "RETAINED_NEUTRAL"
        assert item["go_blocked_until_evidence"] is True
        assert item["scene_gate"]
        assert item["evidence_gap"]

    assert data["effective_coverage"]["inherited_archetypes"] == 32
    assert data["effective_coverage"]["added_archetypes"] == ["U33", "U34"]
    assert data["effective_coverage"]["total_archetypes"] == 34


def test_new_candidates_are_in_scene_but_not_ready_to_run():
    data = load_universe(V2_PATH)
    candidates = {item["id"]: item for item in data["candidate_archetypes_added"]}

    assert set(candidates) == {"U33", "U34"}
    assert candidates["U33"]["application_point"] == "AP27"
    assert candidates["U34"]["application_point"] == "AP28"
    for candidate in candidates.values():
        assert candidate["status"] == "RETAINED_NEUTRAL"
        assert candidate["run_gate"] == "BLOCKED_PENDING_SCENE_PARAMETERS_AND_EVIDENCE"
        assert candidate["scene_gate"]
        assert candidate["evidence_gap"]


def test_u32_is_retained_with_explicit_multi_aperture_parameters():
    data = load_universe(V2_PATH)
    u32 = next(item for item in data["scope_reclassification"] if item["legacy_id"] == "U32")

    required = set(u32["required_scene_parameters"])
    assert {"aperture_count", "branch_geometry", "branch_correlation"} <= required
    assert u32["new_state"] == "RETAINED_NEUTRAL"
