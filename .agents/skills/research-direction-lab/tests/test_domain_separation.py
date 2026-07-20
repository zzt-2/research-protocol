from pathlib import Path
import re

import yaml


ROOT = Path(__file__).parents[1]
PROFILE = ROOT / "references" / "profiles" / "communications.md"
SCHEMA = ROOT / "references" / "project-adapter-schema.yaml"
PROJECT_LAYOUT = ROOT / "references" / "project-layout.md"
GENERIC = [ROOT / "SKILL.md", *sorted((ROOT / "scripts").glob("*.py"))]
FORBIDDEN_DOMAIN_TOKENS = {"ber", "snr", "cma", "pilot", "osl", "qpsk", "jones"}
PROJECT_ADAPTER_FIELDS = {
    "project_id",
    "formal_goal",
    "anchor",
    "components",
    "paths",
    "runnable_axes",
    "blocked_axes",
    "historical_counterexamples",
    "commands",
    "budgets",
}


def test_generic_files_are_domain_neutral():
    token_pattern = re.compile(
        r"\b(?:" + "|".join(sorted(FORBIDDEN_DOMAIN_TOKENS)) + r")\b",
        re.IGNORECASE,
    )
    for path in GENERIC:
        assert token_pattern.search(path.read_text(encoding="utf-8")) is None, path


def test_project_layout_routes_to_profile_and_adapter_contract():
    text = PROJECT_LAYOUT.read_text(encoding="utf-8")
    normalized = " ".join(text.lower().split())

    assert "profiles/communications.md" in text
    assert "project-adapter-schema.yaml" in text
    assert "when a communications decision depends on domain-stable conventions" in normalized
    assert "before consuming current project facts" in normalized


def test_communications_profile_owns_only_reusable_domain_conventions():
    text = PROFILE.read_text(encoding="utf-8")
    lower = text.lower()

    for heading in (
        "information-access levels",
        "metrics and units",
        "common evaluation axes",
        "comparator legality",
        "claim boundaries",
        "common thesis contribution forms",
    ):
        assert heading in lower

    for convention in (
        "ber",
        "snr",
        "coded",
        "uncoded",
        "hard decision",
        "soft information",
    ):
        assert convention in lower
    forbidden_instance_patterns = (
        r"dual[- ]pol",
        r"\bosl\b",
        r"\b(?:b|p)\d{3}\b",
        r"component[_ -]?id",
        r"\.sessions[\\/]",
        r"projects[\\/]",
        r"[a-z]:[\\/]",
    )
    for pattern in forbidden_instance_patterns:
        assert re.search(pattern, text, re.IGNORECASE) is None, pattern


def test_project_adapter_schema_has_exact_closed_v1_shape():
    schema = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))

    assert schema["title"] == "ProjectAdapterV1"
    assert schema["type"] == "object"
    assert set(schema["properties"]) == PROJECT_ADAPTER_FIELDS
    assert set(schema["required"]) == PROJECT_ADAPTER_FIELDS

    def assert_objects_are_closed(node, location="$"):
        if isinstance(node, dict):
            if node.get("type") == "object":
                assert node.get("additionalProperties") is False, location
            for key, value in node.items():
                assert_objects_are_closed(value, f"{location}.{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                assert_objects_are_closed(value, f"{location}[{index}]")

    assert_objects_are_closed(schema)


def test_project_adapter_schema_defines_data_not_scheduling_logic():
    text = SCHEMA.read_text(encoding="utf-8").lower()
    forbidden_scheduler_terms = (
        "ranking",
        "science_slots",
        "slot matching",
        "completeness count",
        "next-candidate",
        "next_candidate",
        "solver",
    )
    assert not [term for term in forbidden_scheduler_terms if term in text]
