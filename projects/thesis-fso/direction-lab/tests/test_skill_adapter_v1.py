from __future__ import annotations

import copy
import hashlib
import importlib.util
from pathlib import Path
import subprocess
from typing import Any

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[4]
LAB = ROOT / "projects/thesis-fso/direction-lab"
SKILL = ROOT / ".agents/skills/research-direction-lab"
ADAPTER_PATH = LAB / "project.v1.yaml"
PORTFOLIO_PATH = LAB / "portfolio/current.v1.yaml"
LEDGER_PATH = LAB / "harvest/ledger.v1.yaml"
SPINES_PATH = LAB / "harvest/thesis-spines.v1.md"
STATUS_PATH = LAB / "STATUS.v1.md"
SCHEMA_PATH = SKILL / "references/project-adapter-schema.yaml"


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def validate_schema_subset(instance: Any, schema: dict[str, Any], at: str = "$") -> None:
    """Validate only the deterministic JSON-Schema subset used by this schema.

    This is deliberately not presented as official meta-schema validation.
    """

    expected = schema.get("type")
    type_checks = {
        "object": lambda value: isinstance(value, dict),
        "array": lambda value: isinstance(value, list),
        "string": lambda value: isinstance(value, str),
        "integer": lambda value: isinstance(value, int) and not isinstance(value, bool),
        "number": lambda value: isinstance(value, (int, float)) and not isinstance(value, bool),
    }
    if expected is not None and not type_checks[expected](instance):
        raise AssertionError(f"{at}: expected {expected}, got {type(instance).__name__}")

    if "enum" in schema and instance not in schema["enum"]:
        raise AssertionError(f"{at}: {instance!r} not in enum")

    if expected == "string" and len(instance) < schema.get("minLength", 0):
        raise AssertionError(f"{at}: string shorter than minLength")
    if expected in {"integer", "number"}:
        if "minimum" in schema and instance < schema["minimum"]:
            raise AssertionError(f"{at}: below minimum")
        if "exclusiveMinimum" in schema and instance <= schema["exclusiveMinimum"]:
            raise AssertionError(f"{at}: not above exclusiveMinimum")

    if expected == "array":
        if len(instance) < schema.get("minItems", 0):
            raise AssertionError(f"{at}: fewer than minItems")
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(instance):
                validate_schema_subset(item, item_schema, f"{at}[{index}]")

    if expected == "object":
        required = set(schema.get("required", []))
        missing = required - set(instance)
        if missing:
            raise AssertionError(f"{at}: missing required keys {sorted(missing)}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extra = set(instance) - set(properties)
            if extra:
                raise AssertionError(f"{at}: additional keys {sorted(extra)}")
        for key, value in instance.items():
            if key in properties:
                validate_schema_subset(value, properties[key], f"{at}.{key}")


def import_renderer():
    path = SKILL / "scripts/render_status.py"
    spec = importlib.util.spec_from_file_location("research_direction_render_status", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.render_status


def resolve_pointer(pointer: str) -> Path:
    return Path(pointer) if Path(pointer).is_absolute() else ROOT / pointer.split("#", 1)[0]


def assert_repo_contained_pointer(pointer: str) -> Path:
    path = Path(pointer.split("#", 1)[0])
    assert not path.is_absolute(), pointer
    assert ".." not in path.parts, pointer
    resolved = (ROOT / path).resolve(strict=True)
    resolved.relative_to(ROOT.resolve())
    return resolved


def test_adapter_closes_exactly_over_project_adapter_v1_schema() -> None:
    adapter = load_yaml(ADAPTER_PATH)
    schema = load_yaml(SCHEMA_PATH)
    validate_schema_subset(adapter, schema)
    assert set(adapter) == set(schema["required"]) == {
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


@pytest.mark.parametrize(
    "mutate,expected",
    [
        (lambda value: value.pop("project_id"), "missing required keys"),
        (lambda value: value.update({"mode": "READ_ONLY_MIGRATION_PREVIEW"}), "additional keys"),
        (lambda value: value.update({"budgets": "not-an-array"}), "expected array"),
        (lambda value: value["formal_goal"].update({"unexpected": True}), "additional keys"),
    ],
)
def test_schema_subset_rejects_missing_extra_and_type_errors(mutate, expected: str) -> None:
    adapter = load_yaml(ADAPTER_PATH)
    broken = copy.deepcopy(adapter)
    mutate(broken)
    with pytest.raises(AssertionError, match=expected):
        validate_schema_subset(broken, load_yaml(SCHEMA_PATH))


def test_projection_is_read_only_and_formal_science_is_blocked() -> None:
    adapter = load_yaml(ADAPTER_PATH)
    portfolio = load_yaml(PORTFOLIO_PATH)
    assert adapter["formal_goal"]["authorized_actions"] == ["READ_ONLY_MIGRATION_PREVIEW"]
    assert portfolio["mode"] == "READ_ONLY_MIGRATION_PREVIEW"
    assert portfolio["formal_authorization"]["status"] == "BLOCKED"
    assert portfolio["formal_authorization"]["science_authorized"] is False
    assert portfolio["no_new_experiment_running"] is True
    forbidden = " ".join(adapter["formal_goal"]["prohibited_actions"])
    assert all(token in forbidden for token in ("B004", "scientific", "promotion"))


def test_all_pointers_exist_and_protected_byte_guards_match_disk() -> None:
    adapter = load_yaml(ADAPTER_PATH)
    for source in adapter["anchor"]["parameter_sources"]:
        assert resolve_pointer(source["pointer"]).exists(), source
    for component in adapter["components"]:
        assert resolve_pointer(component["source_pointer"]).exists(), component
    guards = [c for c in adapter["components"] if c["role"].startswith("protected historical file")]
    assert guards
    before = {}
    for guard in guards:
        path = resolve_pointer(guard["source_pointer"])
        assert path.is_file(), guard["source_pointer"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        before[str(path)] = digest
        assert guard["identity_digest"] == digest

    required_fragments = (
        "canonical-state.yaml",
        "completion-events.jsonl",
        "state/projections/5967",
        "B001-20260717-live/manifest.json",
        "B002-20260718-live/manifest.json",
        "B003-20260718-live/manifest.json",
        "B003-20260718-live/execution-status.yaml",
        "B003-20260718-live/verifier-report.md",
        "B003-20260718-live/batch-synthesis.md",
        "P01-U25-action-contract/preflight-report.json",
        "atlas-closeout-assessment.v1.yaml",
        "stage-a-synthesis.md",
        "stage-a-verifier-report.md",
    )
    guarded = "\n".join(c["source_pointer"] for c in guards)
    assert all(fragment in guarded for fragment in required_fragments)

    for pointer in adapter["paths"].values():
        values = pointer if isinstance(pointer, list) else [pointer]
        for value in values:
            assert resolve_pointer(value).exists(), value
    for axis in adapter["runnable_axes"] + adapter["blocked_axes"]:
        assert resolve_pointer(axis["evidence_pointer"]).exists(), axis
    for item in adapter["historical_counterexamples"]:
        assert resolve_pointer(item["evidence_pointer"]).exists(), item

    after = {path: hashlib.sha256(Path(path).read_bytes()).hexdigest() for path in before}
    assert after == before


def test_durable_project_source_and_parameter_pointers_are_repo_relative_and_contained() -> None:
    adapter = load_yaml(ADAPTER_PATH)
    pointers = [source["pointer"] for source in adapter["anchor"]["parameter_sources"]]
    pointers += [component["source_pointer"] for component in adapter["components"]]
    for pointer in pointers:
        assert_repo_contained_pointer(pointer)

    with pytest.raises(AssertionError):
        assert_repo_contained_pointer(
            "D:/code/study/research-protocol/.worktrees/sibling/private-source.py"
        )


def test_declared_render_command_reproduces_status_on_stdout_without_writes() -> None:
    adapter = load_yaml(ADAPTER_PATH)
    command = next(item for item in adapter["commands"] if item["command_id"] == "render-read-only-status")
    argv = command["argv"]
    assert set(("--adapter", "--state", "--portfolio", "--harvest")) <= set(argv)
    before = {
        path.relative_to(LAB).as_posix(): (path.stat().st_size, path.stat().st_mtime_ns)
        for path in LAB.rglob("*")
        if path.is_file()
    }

    completed = subprocess.run(
        argv,
        cwd=ROOT / command["working_directory"],
        check=False,
        capture_output=True,
        timeout=command["timeout_seconds"],
    )

    assert completed.returncode == 0, completed.stderr.decode("utf-8", errors="replace")
    assert completed.stdout == STATUS_PATH.read_bytes()
    after = {
        path.relative_to(LAB).as_posix(): (path.stat().st_size, path.stat().st_mtime_ns)
        for path in LAB.rglob("*")
        if path.is_file()
    }
    assert after == before


def test_portfolio_preserves_scoped_facts_without_completeness_claim() -> None:
    portfolio = load_yaml(PORTFOLIO_PATH)
    assert portfolio["completeness_claim"] == "OPEN_PORTFOLIO_NO_COMPLETENESS_CLAIM"
    cards = {card["candidate_id"]: card for card in portfolio["candidates"]}
    assert cards["P03/U19"]["status"] == "P03_DOMAIN_ADEQUACY_UNRESOLVED"
    assert cards["P03/U19"]["claim_ceiling"] == "SLICE"
    assert cards["P03/U19"]["negative_scope"] == ["runnable_representative_subdomain"]
    assert set(cards["P03/U19"]["blocked_scope"]) == {
        "16QAM",
        "receiver_estimated_CSI_or_explicit_pilot",
        "soft_or_coded_output",
    }
    assert cards["P01/U25"]["status"] == "DEFERRED_ARCHITECTURE"
    assert cards["P01/U25"]["preflight"] == "P01_BLOCKED"
    assert cards["P02/U10"]["status"] == "NOT_RUNNABLE"

    b003 = next(batch for batch in portfolio["batch_history"] if batch["batch_id"] == "B003")
    assert b003["status"] == "COMPLETED_SANDBOX_VERIFIED"
    assert b003["status_source"].endswith("state/completion-events.jsonl")
    assert b003["raw_artifact_available_in_checkout"] is False
    assert b003["history_self_contained"] is False
    assert "raw artifact" in b003["artifact_availability_note"].lower()
    assert list((LAB / "batches").glob("B004*")) == []
    assert "B004" not in "\n".join(str(batch) for batch in portfolio["batch_history"])


def test_harvest_is_bounded_pointer_only_and_covers_source_map_h001_h009() -> None:
    ledger = load_yaml(LEDGER_PATH)
    entries = ledger["entries"]
    assert {entry["id"] for entry in entries} == {f"H{i:03d}" for i in range(1, 10)}
    assert {
        "FAILURE_MECHANISM",
        "INFRASTRUCTURE_GAP",
        "LOCAL_NEGATIVE",
        "EVALUATION_INSIGHT",
        "REUSABLE_ASSET",
    } <= {entry["category"] for entry in entries}
    for entry in entries:
        assert len(entry["finding"]) <= 420
        assert entry["artifact_pointers"]
        assert set(entry["artifact_pointers"]) == set(entry["source_hashes"])
        for pointer in entry["artifact_pointers"]:
            path = resolve_pointer(pointer)
            assert path.is_file(), pointer
            assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["source_hashes"][pointer]
        assert "raw_values" not in entry


def test_thesis_spines_declares_none_promoted_and_only_promotion_conditions() -> None:
    text = SPINES_PATH.read_text(encoding="utf-8")
    assert "当前无可晋级 thesis spine" in text
    assert "晋级条件" in text
    assert "READ_ONLY_MIGRATION_PREVIEW" in text
    assert "promotion effect: none" in text


def test_status_is_exact_renderer_output_and_answers_eight_recovery_questions() -> None:
    adapter = load_yaml(ADAPTER_PATH)
    portfolio = load_yaml(PORTFOLIO_PATH)
    harvest = load_yaml(LEDGER_PATH)
    status_state = portfolio["status_input"]
    expected = import_renderer()(adapter, status_state, portfolio, harvest)
    actual = STATUS_PATH.read_text(encoding="utf-8")
    assert actual == expected

    assert status_state["formal_authorization"] == "BLOCKED"
    assert "Formal status: BLOCKED" in actual
    assert "Currently allowed: READ_ONLY_MIGRATION_PREVIEW" in actual
    assert status_state["anchor_baseline"] == "baseline.standard_cma.godard_z"
    assert status_state["portfolio_and_blocked_axes"]
    assert status_state["latest_completed_batch"]["batch_id"] == "B003"
    assert status_state["current_mode"] == {
        "science": "AWAITING_STRATEGY",
        "migration": "READ_ONLY_MIGRATION_PREVIEW",
    }
    assert status_state["harvested_material"] == [f"H{i:03d}" for i in range(1, 10)]
    assert "no automatic scientific runner" in status_state["recorded_next_action"].lower()
    assert status_state["strategy_required_when"]
    assert status_state["no_new_experiment_running"] is True
    assert "no new experiment is running" in actual.lower()
    assert len(actual.splitlines()) <= 120
    assert len(actual.encode("utf-8")) <= 12_000
    for heading in (
        "1. Formal Goal and Authorization",
        "2. Anchor or Baseline",
        "3. Portfolio and Blocked Axes",
        "4. Latest Completed Scientific Result",
        "5. Current Mode",
        "6. Thesis Harvest",
        "7. Next Automatic Action",
        "8. Strategy Escalation Condition",
    ):
        assert heading in actual
    for forbidden_dump_key in (
        '"components"',
        '"source_hashes"',
        '"batch_history"',
        '"candidates"',
        "protected.b003-manifest",
    ):
        assert forbidden_dump_key not in actual
    for pointer in (
        adapter["paths"]["current_state"],
        adapter["paths"]["candidates"],
        adapter["paths"]["batches"],
        adapter["paths"]["harvest_ledger"],
        adapter["paths"]["thesis_spines"],
    ):
        assert pointer in actual
    for axis in adapter["blocked_axes"]:
        assert axis["axis_id"] in actual
