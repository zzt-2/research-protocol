from __future__ import annotations

import hashlib
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
MODULE_PATH = ROOT / "tools" / "validate_candidate_map.py"
spec = importlib.util.spec_from_file_location("validate_candidate_map", MODULE_PATH)
gate = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(gate)


V1_PATH = ROOT / "candidate-map.yaml"
V2_PATH = ROOT / "candidate-map.v2.yaml"
UNIVERSE_V2_PATH = ROOT / "candidate-universe.v2.yaml"


def test_v1_reports_score_and_ordering_mismatches():
    report = gate.validate_map(gate.load_map(V1_PATH))

    assert any("score mismatch" in error and "U24" in error for error in report.errors)
    assert any("score mismatch" in error and "U18" in error for error in report.errors)
    assert any("ordering mismatch" in error for error in report.errors)


def test_v2_recomputes_scores_and_uses_full_precision_for_ordering():
    data = gate.load_map(V2_PATH)
    report = gate.validate_map(data, map_path=V2_PATH)

    assert report.errors == []
    assert data["ranked_shortlist"][0]["id"] == "U24"
    assert [item["id"] for item in data["ranked_shortlist"]][8:] == [
        "U18",
        "U12",
        "U08",
        "U03",
    ]


def test_v2_preserves_universe_and_passed_review_gate():
    data = gate.load_map(V2_PATH)
    members = [member for family in data["families"] for member in family["members"]]
    retained = data["unranked_but_retained"]["ids"]
    shortlisted = [item["id"] for item in data["ranked_shortlist"]]

    assert len(members) == 34
    assert len(set(members)) == 34
    assert set(shortlisted) | set(retained) == set(members)
    assert {"U33", "U34"}.issubset(retained)
    assert {"U33", "U34"}.isdisjoint(shortlisted)
    assert data["unranked_but_retained"]["explicit_status"] == {
        "U33": "RETAINED_NEUTRAL",
        "U34": "RETAINED_NEUTRAL",
    }
    assert data["map_gate"]["independent_review"] == "PASS"
    assert data["map_gate"]["verdict"] == "PASS"


def test_v2_contains_lineage_and_exact_v1_sha():
    data = gate.load_map(V2_PATH)
    assert data["lineage"]["supersedes_map_id"] == "map.dual-pol-osl.ml.2026-07-17.v1"
    expected_sha = hashlib.sha256(V1_PATH.read_bytes()).hexdigest()
    assert data["lineage"]["v1_file_sha256"] == expected_sha
    assert data["lineage"]["correction_reason"]


def test_v2_binds_exact_candidate_universe_v2_and_base_sha():
    data = gate.load_map(V2_PATH)
    universe = gate.load_map(UNIVERSE_V2_PATH)

    assert data["universe_id"] == universe["universe_id"]
    assert data["lineage"]["candidate_universe_file"] == UNIVERSE_V2_PATH.name
    assert data["lineage"]["candidate_universe_file_sha256"] == hashlib.sha256(
        UNIVERSE_V2_PATH.read_bytes()
    ).hexdigest()
    assert data["lineage"]["candidate_universe_base_file_sha256"] == universe["lineage"][
        "base_file_sha256"
    ]


def test_duplicate_shortlist_id_is_rejected():
    data = gate.load_map(V2_PATH)
    data["ranked_shortlist"][1]["id"] = data["ranked_shortlist"][0]["id"]

    report = gate.validate_map(data, map_path=V2_PATH)

    assert any("duplicate candidate ID" in error for error in report.errors)


def test_universe_binding_rejects_archetype_substitution_even_if_internal_sets_agree():
    data = gate.load_map(V2_PATH)
    for family in data["families"]:
        family["members"] = ["UX" if candidate_id == "U01" else candidate_id for candidate_id in family["members"]]
    data["unranked_but_retained"]["ids"] = [
        "UX" if candidate_id == "U01" else candidate_id
        for candidate_id in data["unranked_but_retained"]["ids"]
    ]

    report = gate.validate_map(data, map_path=V2_PATH)

    assert any("universe coverage mismatch" in error and "UX" in error for error in report.errors)


@pytest.mark.parametrize(
    ("section", "expected_error"),
    (
        ("family", "duplicate family member ID"),
        ("retained", "duplicate retained candidate ID"),
        ("partition", "shortlist/retained overlap"),
    ),
)
def test_family_shortlist_retained_must_form_unique_partition(section, expected_error):
    data = gate.load_map(V2_PATH)
    if section == "family":
        data["families"][0]["members"].append("U01")
    elif section == "retained":
        data["unranked_but_retained"]["ids"].append("U01")
    else:
        data["unranked_but_retained"]["ids"].append("U24")

    report = gate.validate_map(data, map_path=V2_PATH)

    assert any(expected_error in error for error in report.errors)


def test_weights_must_sum_to_one():
    data = gate.load_map(V2_PATH)
    data["weights"]["problem_truth"] = 0.21

    report = gate.validate_map(data, map_path=V2_PATH)

    assert any("weights must sum to 1" in error for error in report.errors)


def test_factor_values_must_stay_within_declared_one_to_five_scale():
    data = gate.load_map(V2_PATH)
    data["ranked_shortlist"][0]["factors"]["problem_truth"] = 6

    report = gate.validate_map(data, map_path=V2_PATH)

    assert any("factor out of range" in error and "U24" in error for error in report.errors)


def test_equal_score_tie_must_follow_v1_shortlist_order():
    data = gate.load_map(V2_PATH)
    shortlist = data["ranked_shortlist"]
    u05 = next(index for index, item in enumerate(shortlist) if item["id"] == "U05")
    u20 = next(index for index, item in enumerate(shortlist) if item["id"] == "U20")
    shortlist[u05], shortlist[u20] = shortlist[u20], shortlist[u05]

    report = gate.validate_map(data, map_path=V2_PATH)

    assert any("ordering mismatch" in error and "v1 shortlist" in error for error in report.errors)


def test_universe_binding_rejects_wrong_file_hash():
    data = gate.load_map(V2_PATH)
    data["lineage"]["candidate_universe_file_sha256"] = "0" * 64

    report = gate.validate_map(data, map_path=V2_PATH)

    assert any("candidate universe SHA mismatch" in error for error in report.errors)


def test_v1_source_hash_drift_is_rejected():
    data = gate.load_map(V2_PATH)
    data["lineage"]["v1_file_sha256"] = "0" * 64

    report = gate.validate_map(data, map_path=V2_PATH)

    assert any("v1 file SHA mismatch" in error for error in report.errors)


def test_cli_fails_on_v1_and_passes_on_v2():
    for path, expected_code, expected_text in (
        (V1_PATH, 1, ("score mismatch", "ordering mismatch")),
        (V2_PATH, 0, ("PASS",)),
    ):
        result = subprocess.run(
            [sys.executable, str(MODULE_PATH), str(path)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == expected_code, result.stdout + result.stderr
        output = result.stdout + result.stderr
        for text in expected_text:
            assert text in output
