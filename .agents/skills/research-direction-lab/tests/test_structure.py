from pathlib import Path
import re

import yaml


ROOT = Path(__file__).parents[1]
REFERENCE_NAMES = (
    "core-loop.md",
    "candidate-portfolio.md",
    "batch-and-atlas.md",
    "evidence-and-claims.md",
    "baseline-adjudication.md",
    "thesis-harvest.md",
    "recovery-and-rotation.md",
    "project-layout.md",
)
EXPECTED_REFERENCE_FILES = {ROOT / "references" / name for name in REFERENCE_NAMES}
ALLOWED_NESTED_FILES = {
    ROOT / "references" / "profiles" / "communications.md",
}
ALLOWED_MARKDOWN = {
    ROOT / "SKILL.md",
    *EXPECTED_REFERENCE_FILES,
    *ALLOWED_NESTED_FILES,
    ROOT / "tests" / "forward-test-log.md",
}


def test_only_routed_top_level_references_exist():
    reference_root = ROOT / "references"
    actual_files = set(reference_root.glob("*.md"))
    nested_files = {
        path
        for path in reference_root.rglob("*")
        if path.is_file() and path.parent != reference_root
    }

    missing = EXPECTED_REFERENCE_FILES - actual_files
    extra = actual_files - EXPECTED_REFERENCE_FILES
    if missing:
        raise AssertionError(
            f"missing routed references: {sorted(path.name for path in missing)}"
        )
    if extra:
        raise AssertionError(
            f"unexpected top-level references: {sorted(path.name for path in extra)}"
        )
    assert len(actual_files) == len(REFERENCE_NAMES)
    assert nested_files == ALLOWED_NESTED_FILES, (
        "unexpected nested references: "
        f"missing={sorted(str(path.relative_to(ROOT)) for path in ALLOWED_NESTED_FILES - nested_files)}, "
        f"extra={sorted(str(path.relative_to(ROOT)) for path in nested_files - ALLOWED_NESTED_FILES)}"
    )


def test_skill_has_single_level_references():
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    for name in REFERENCE_NAMES:
        assert f"references/{name}" in text


def test_skill_does_not_claim_project_state():
    core_files = [
        ROOT / "SKILL.md",
        *sorted(path for path in EXPECTED_REFERENCE_FILES if path.is_file()),
    ]
    absolute_or_project_path = re.compile(
        r"(?i)(?:[a-z]:[\\/]|/(?:home|mnt|users)/|\.sessions[\\/]|projects[\\/]|papers[\\/])"
    )
    serialized_state = re.compile(
        r"(?im)^\s*(?:project_id|last_completed_batch|current_batch|active_candidate|"
        r"run_status|last_event_head)\s*:"
    )
    concrete_record_id = re.compile(r"(?i)\b(?:b|s|d|v|h|r|p)\d{3}\b")

    for path in core_files:
        text = path.read_text(encoding="utf-8")
        assert absolute_or_project_path.search(text) is None, path
        assert serialized_state.search(text) is None, path
        assert concrete_record_id.search(text) is None, path


def test_skill_tree_has_no_extra_documentation():
    # Forward-test run recordings under tests/forward/runs/ are test data
    # (blind prompts + raw responses), not Skill documentation; they are
    # excluded from the documentation-set check.
    RUNS_DIR = ROOT / "tests" / "forward" / "runs"
    markdown_files = {
        path for path in ROOT.rglob("*.md") if RUNS_DIR not in path.parents
    }
    missing = ALLOWED_MARKDOWN - markdown_files
    extra = markdown_files - ALLOWED_MARKDOWN
    if missing or extra:
        raise AssertionError(
            "unexpected markdown set: "
            f"missing={sorted(path.name for path in missing)}, "
            f"extra={sorted(str(path.relative_to(ROOT)) for path in extra)}"
        )

    forbidden_names = re.compile(r"(?i)(?:^|[-_])(readme|changelog)(?:[-_.]|$)|guide")
    forbidden_docs = [
        path
        for path in ROOT.rglob("*")
        if path.is_file() and forbidden_names.search(path.name)
    ]
    assert not forbidden_docs, f"extra documentation is not allowed: {forbidden_docs}"


def test_all_user_requirements_have_unique_well_formed_cases():
    data = yaml.safe_load(
        (ROOT / "tests/cases/user-requirements.yaml").read_text(encoding="utf-8")
    )
    requirements = data["requirements"]
    expected_ids = {f"U{i:02d}" for i in range(1, 16)}
    actual_ids = {item["requirement_id"] for item in requirements}

    assert data["schema_version"] == 1
    assert len(requirements) == 15
    assert actual_ids == expected_ids
    assert len(actual_ids) == len(requirements)
    assert all(
        set(item) == {
            "requirement_id",
            "source_pointer",
            "scenario",
            "must_do",
            "must_not_do",
        }
        for item in requirements
    )
    assert all(
        isinstance(value, str) and value.strip()
        for item in requirements
        for value in item.values()
    )
