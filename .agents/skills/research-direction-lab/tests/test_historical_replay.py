from __future__ import annotations

import hashlib
from pathlib import Path, PurePosixPath
import re
import subprocess

import yaml


SKILL_ROOT = Path(__file__).parents[1]
REPO_ROOT = Path(__file__).parents[4]
CASES_ROOT = SKILL_ROOT / "tests" / "cases"
EXPECTED_CASE_NAMES = {
    "current-cma-bug-signal.yaml",
    "p01-action-blocker.yaml",
    "p03-local-negative.yaml",
    "headroom-atlas-blocked-axes.yaml",
}
TOP_LEVEL_FIELDS = {
    "schema_version",
    "case_id",
    "decision_point",
    "facts",
    "artifacts",
    "allowed_actions",
    "forbidden_actions",
    "claim_ceiling",
}
CLAIM_LEVELS = {"CELL", "SLICE", "DOMAIN", "CANDIDATE", "FAMILY", "DIAGNOSTIC"}
FORBIDDEN_KEYS = {
    "recommended_candidate",
    "candidate_priority",
    "expected_next_action",
    "expected_prose",
    "intended_candidate_ranking",
}


def _load_cases() -> list[tuple[Path, dict]]:
    actual_paths = {
        path for path in CASES_ROOT.glob("*.yaml") if path.name != "user-requirements.yaml"
    }
    assert {path.name for path in actual_paths} == EXPECTED_CASE_NAMES
    return [
        (path, yaml.safe_load(path.read_text(encoding="utf-8")))
        for path in sorted(actual_paths)
    ]


def _mapping_keys(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from _mapping_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from _mapping_keys(child)


def test_exactly_four_historical_cases_are_loaded():
    cases = _load_cases()
    assert len(cases) == 4


def test_historical_cases_have_exact_closed_contract():
    for path, case in _load_cases():
        assert isinstance(case, dict), path
        assert set(case) == TOP_LEVEL_FIELDS, path
        assert case["schema_version"] == 1, path
        assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", case["case_id"]), path
        assert isinstance(case["decision_point"], str) and case["decision_point"].strip(), path

        for field in ("facts", "allowed_actions", "forbidden_actions"):
            values = case[field]
            assert isinstance(values, list) and values, (path, field)
            assert all(isinstance(item, str) and item.strip() for item in values), (path, field)

        assert set(case["allowed_actions"]).isdisjoint(case["forbidden_actions"]), path
        assert set(case["claim_ceiling"]) == {"level", "statement"}, path
        assert case["claim_ceiling"]["level"] in CLAIM_LEVELS, path
        assert (
            isinstance(case["claim_ceiling"]["statement"], str)
            and case["claim_ceiling"]["statement"].strip()
        ), path
        assert FORBIDDEN_KEYS.isdisjoint(_mapping_keys(case)), path


def test_headroom_atlas_claim_ceiling_is_slice():
    cases = {path.name: case for path, case in _load_cases()}
    atlas = cases["headroom-atlas-blocked-axes.yaml"]
    assert atlas["claim_ceiling"]["level"] == "SLICE"


def test_historical_artifacts_do_not_bind_prompt_task_documents():
    prompt_document = re.compile(r"(?i)^PROMPT[-_]\d+.*\.md$")
    for case_path, case in _load_cases():
        for artifact in case["artifacts"]:
            name = PurePosixPath(artifact["path"]).name
            if prompt_document.fullmatch(name):
                assert "REPORT" in PurePosixPath(name).stem.upper(), (
                    case_path,
                    artifact["path"],
                )


def test_historical_case_artifacts_are_tracked_hash_bound_repo_files():
    for case_path, case in _load_cases():
        artifacts = case["artifacts"]
        assert isinstance(artifacts, list) and artifacts, case_path

        for artifact in artifacts:
            assert set(artifact) == {"path", "sha256"}, (case_path, artifact)
            relative = artifact["path"]
            digest = artifact["sha256"]
            assert isinstance(relative, str) and relative, case_path
            assert "\\" not in relative, (case_path, relative)
            pure_path = PurePosixPath(relative)
            assert not pure_path.is_absolute(), (case_path, relative)
            assert ".." not in pure_path.parts, (case_path, relative)
            assert re.fullmatch(r"[0-9a-f]{64}", digest), (case_path, digest)

            resolved = (REPO_ROOT / Path(*pure_path.parts)).resolve()
            assert resolved.is_relative_to(REPO_ROOT.resolve()), (case_path, relative)
            assert resolved.is_file(), (case_path, relative)
            assert hashlib.sha256(resolved.read_bytes()).hexdigest() == digest, (
                case_path,
                relative,
            )
            tracked = subprocess.run(
                ["git", "ls-files", "--error-unmatch", "--", relative],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            assert tracked.returncode == 0, (case_path, relative, tracked.stderr)
