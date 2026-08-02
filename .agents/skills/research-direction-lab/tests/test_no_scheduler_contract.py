import ast
from pathlib import Path
import re

import pytest


SKILL_ROOT = Path(__file__).parents[1]
SCRIPTS = SKILL_ROOT / "scripts"
AUDIT = SKILL_ROOT.parents[2] / "projects/thesis-fso/direction-lab/control-migration-audit.md"

ALLOWED_DISPOSITIONS = {
    "KEEP_AS_UTILITY",
    "MOVE_TO_ADAPTER",
    "DELETE_SCHEDULER",
    "ARCHIVE_UNUSED",
}

EXPECTED_APIS = {
    "campaign_core.py": {
        "canonical_json",
        "content_hash",
        "campaign_root",
        "campaign_path",
        "validate_campaign",
        "admit_batch",
        "event_hash",
        "load_events",
        "append_events",
        "append_event",
        "reduce_campaign",
        "next_action",
        "may_stop",
        "render_state_bytes",
        "atomic_write_state",
        "ensure_state_consistent",
        "ValidationReport.passed",
    },
    "campaignctl.py": {
        "campaign_path",
        "command_preflight",
        "command_next",
        "command_record",
        "command_close",
        "build_parser",
        "main",
    },
}

EXPECTED_COMMANDS = {"preflight", "next", "record", "close"}

SCHEDULER_JUDGMENTS = {
    "validate_campaign",
    "admit_batch",
    "reduce_campaign",
    "next_action",
    "may_stop",
    "ensure_state_consistent",
    "command_preflight",
    "command_next",
    "command_record",
    "command_close",
    "build_parser",
    "main",
    "preflight",
    "next",
    "record",
    "close",
}

APPROVED_SCRIPT_APIS = {
    "append_event",
    "build_execution_receipt",
    "hash_bundle",
    "rebuild_state",
    "render_status",
    "validate_execution_receipt",
    "validate_receipt",
    "validate_task_control",
}

FORBIDDEN_SCHEDULER_NAMES = {
    "next_action",
    "match_slot",
    "work_conservation",
    "min_valid_batches",
    "min_evidence_families",
    "validate_campaign",
    "reduce_campaign",
    "may_stop",
    "ensure_state_consistent",
    "command_preflight",
    "command_next",
    "command_record",
    "command_close",
    "campaignctl",
    "science_slots",
    "resource_slot_id",
    "min_mechanism_branches",
    "precoverage_branch_cap",
    "portfolio_exhaustion_certified",
    "stop_legality",
}

FORBIDDEN_MODULES = {"campaign_core", "campaignctl"}
FORBIDDEN_COMMANDS = {"preflight", "next", "record", "close"}


def _audit_rows(markdown: str, marker: str) -> list[dict[str, str]]:
    rows = []
    for line in markdown.splitlines():
        if not line.startswith(f"| {marker} |"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        assert len(cells) == 9, f"malformed {marker} audit row: {line}"
        rows.append(
            dict(
                zip(
                    (
                        "marker",
                        "file",
                        "symbol",
                        "line",
                        "callers",
                        "domain_terms",
                        "state_mutation",
                        "scientific_judgment",
                        "disposition",
                    ),
                    cells,
                    strict=True,
                )
            )
        )
    return rows


def test_audit_inventories_every_public_api_and_cli_command():
    markdown = AUDIT.read_text(encoding="utf-8")
    api_rows = _audit_rows(markdown, "API")
    cli_rows = _audit_rows(markdown, "CLI")

    actual_apis: dict[str, set[str]] = {}
    for row in api_rows:
        actual_apis.setdefault(row["file"], set()).add(row["symbol"])
        assert re.fullmatch(r"[1-9][0-9]*", row["line"])
        assert row["callers"]
        assert row["domain_terms"]
        assert row["state_mutation"]
        assert row["scientific_judgment"] in {"YES", "NO"}
        assert row["disposition"] in ALLOWED_DISPOSITIONS

    assert actual_apis == EXPECTED_APIS
    assert {row["symbol"] for row in cli_rows} == EXPECTED_COMMANDS
    for row in cli_rows:
        assert row["file"] == "campaignctl.py"
        assert re.fullmatch(r"[1-9][0-9]*", row["line"])
        assert row["callers"]
        assert row["domain_terms"]
        assert row["state_mutation"]
        assert row["scientific_judgment"] == "YES"
        assert row["disposition"] in ALLOWED_DISPOSITIONS


def test_scheduler_judgments_are_never_kept_as_utilities():
    markdown = AUDIT.read_text(encoding="utf-8")
    rows = _audit_rows(markdown, "API") + _audit_rows(markdown, "CLI")
    by_symbol = {row["symbol"]: row for row in rows}

    for symbol in SCHEDULER_JUDGMENTS:
        assert by_symbol[symbol]["disposition"] != "KEEP_AS_UTILITY"


def _parents(tree: ast.AST) -> dict[ast.AST, ast.AST]:
    return {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}


def _allowed_recorded_fact_key(node: ast.Constant, parents: dict[ast.AST, ast.AST]) -> bool:
    parent = parents.get(node)
    return (
        node.value == "next_action"
        and isinstance(parent, ast.Call)
        and node in parent.args
        and isinstance(parent.func, ast.Attribute)
        and parent.func.attr == "get"
    )


def _semantic_scheduler_violations(tree: ast.AST, filename: str) -> list[str]:
    def words(identifier: str) -> set[str]:
        snake_case = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", identifier)
        return {part.lower() for part in re.split(r"[^A-Za-z0-9]+", snake_case) if part}

    def category(identifier: str) -> str | None:
        tokens = words(identifier)
        passive_render_terms = {"display", "format", "render", "report", "show"}
        active_decision_verbs = {
            "allocate",
            "allow",
            "assign",
            "can",
            "check",
            "choose",
            "decide",
            "dispatch",
            "find",
            "match",
            "may",
            "permit",
            "pick",
            "prove",
            "recommend",
            "reserve",
            "select",
            "should",
            "validate",
            "verify",
        }
        if (
            "recorded" in tokens
            and tokens & passive_render_terms
            and not tokens & active_decision_verbs
        ):
            return None
        selection_verbs = {
            "best",
            "choose",
            "order",
            "ordering",
            "pick",
            "prioritize",
            "priority",
            "rank",
            "ranking",
            "recommend",
            "score",
            "select",
            "selection",
            "sort",
            "sorted",
            "top",
            "winner",
        }
        allocation_verbs = {
            "allocate",
            "allocation",
            "assign",
            "assignment",
            "choose",
            "compatible",
            "compatibility",
            "dispatch",
            "find",
            "match",
            "matching",
            "pick",
            "reserve",
            "select",
            "selection",
        }
        completeness_terms = {
            "complete",
            "completeness",
            "coverage",
            "exhaust",
            "exhausted",
            "exhaustion",
        }
        proof_terms = {"check", "prove", "proof", "validate", "verification", "verify"}
        legality_terms = {
            "allow",
            "allowed",
            "can",
            "check",
            "decide",
            "decision",
            "eligible",
            "legality",
            "legal",
            "may",
            "permit",
            "permitted",
            "should",
            "validate",
        }

        if tokens & {"candidate", "candidates"} and tokens & selection_verbs:
            return "candidate-selection"
        if tokens & {"resource", "resources", "slot", "slots"} and tokens & allocation_verbs:
            return "resource-slot-allocation"
        if (
            "portfolio" in tokens and tokens & completeness_terms
        ) or ("coverage" in tokens and tokens & proof_terms):
            return "portfolio-completeness"
        if tokens & {"close", "stop", "termination", "terminate"} and tokens & legality_terms:
            return "stop-close-legality"
        return None

    violations: list[str] = []
    for node in ast.walk(tree):
        identifier: str | None = None
        kind: str | None = None
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            identifier = node.name
            kind = "helper"
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                identifier = node.func.id
            elif isinstance(node.func, ast.Attribute):
                identifier = node.func.attr
            kind = "call"

        if identifier is None or kind is None:
            continue
        semantic_category = category(identifier)
        if semantic_category is not None:
            violations.append(
                f"{filename}:{node.lineno}:{kind}:{semantic_category}:{identifier}"
            )
    return violations


@pytest.mark.parametrize(
    ("source", "expected_category"),
    [
        (
            """
def _select_best_candidate(portfolio):
    return portfolio[0]

def render_status(portfolio):
    return _select_best_candidate(portfolio)
""",
            "candidate-selection",
        ),
        (
            """
def _allocate_resource_slot(candidate, slots):
    return slots[0]

def render_status(candidate, slots):
    return _allocate_resource_slot(candidate, slots)
""",
            "resource-slot-allocation",
        ),
        (
            """
def _prove_portfolio_coverage(portfolio):
    return bool(portfolio)

def render_status(portfolio):
    return _prove_portfolio_coverage(portfolio)
""",
            "portfolio-completeness",
        ),
        (
            """
def _check_close_legality(state):
    return not state

def render_status(state):
    return _check_close_legality(state)
""",
            "stop-close-legality",
        ),
    ],
)
def test_semantic_scheduler_helpers_and_calls_are_rejected(source, expected_category):
    tree = ast.parse(source)

    violations = _semantic_scheduler_violations(tree, "mutation.py")

    assert any(f":helper:{expected_category}:" in violation for violation in violations)
    assert any(f":call:{expected_category}:" in violation for violation in violations)


def test_recorded_next_action_and_passive_status_rendering_are_not_scheduler_semantics():
    tree = ast.parse(
        """
def _render_recorded_candidate_ranking(state):
    return state.get("recorded_candidate_ranking")

def render_status(state, portfolio):
    recorded_next_action = state.get("recorded_next_action")
    event_next_action = state.get("next_action")
    recorded_ranking = _render_recorded_candidate_ranking(state)
    return recorded_next_action, event_next_action, recorded_ranking, portfolio
"""
    )

    assert _semantic_scheduler_violations(tree, "passive_status.py") == []


def test_skill_scripts_expose_only_the_approved_non_scheduler_surface():
    public_functions: set[str] = set()
    violations: list[str] = []

    for path in sorted(SCRIPTS.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        parents = _parents(tree)
        violations.extend(_semantic_scheduler_violations(tree, path.name))
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not node.name.startswith("_"):
                    public_functions.add(node.name)
                if node.name in FORBIDDEN_SCHEDULER_NAMES:
                    violations.append(f"{path.name}:{node.lineno}:function:{node.name}")
                for argument in (*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs):
                    if argument.arg in FORBIDDEN_SCHEDULER_NAMES:
                        violations.append(f"{path.name}:{argument.lineno}:argument:{argument.arg}")
            elif isinstance(node, ast.Attribute) and node.attr in FORBIDDEN_SCHEDULER_NAMES:
                violations.append(f"{path.name}:{node.lineno}:attribute:{node.attr}")
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[-1] in FORBIDDEN_MODULES:
                        violations.append(f"{path.name}:{node.lineno}:import:{alias.name}")
                    exposed_name = alias.asname or alias.name.split(".")[-1]
                    if exposed_name in FORBIDDEN_SCHEDULER_NAMES:
                        violations.append(f"{path.name}:{node.lineno}:import-binding:{exposed_name}")
            elif isinstance(node, ast.ImportFrom):
                if (node.module or "").split(".")[-1] in FORBIDDEN_MODULES:
                    violations.append(f"{path.name}:{node.lineno}:import:{node.module}")
                for alias in node.names:
                    exposed_name = alias.asname or alias.name
                    if exposed_name in FORBIDDEN_SCHEDULER_NAMES:
                        violations.append(f"{path.name}:{node.lineno}:import-binding:{exposed_name}")
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                if node.value in FORBIDDEN_SCHEDULER_NAMES and not _allowed_recorded_fact_key(node, parents):
                    violations.append(f"{path.name}:{node.lineno}:string:{node.value}")
                parent = parents.get(node)
                if (
                    node.value in FORBIDDEN_COMMANDS
                    and isinstance(parent, ast.Call)
                    and isinstance(parent.func, ast.Attribute)
                    and parent.func.attr == "add_parser"
                ):
                    violations.append(f"{path.name}:{node.lineno}:command:{node.value}")

        for statement in tree.body:
            if isinstance(statement, (ast.Assign, ast.AnnAssign)):
                targets = statement.targets if isinstance(statement, ast.Assign) else [statement.target]
                for target in targets:
                    if isinstance(target, ast.Name) and target.id in FORBIDDEN_SCHEDULER_NAMES:
                        violations.append(f"{path.name}:{target.lineno}:module-binding:{target.id}")

        normalized_source = path.read_text(encoding="utf-8").replace("\\", "/").lower()
        if "p03-residual-headroom" in normalized_source:
            violations.append(f"{path.name}:loads dirty scheduler worktree")

    assert public_functions == APPROVED_SCRIPT_APIS
    assert violations == []
