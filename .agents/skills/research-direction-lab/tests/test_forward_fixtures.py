"""Tests for the non-communications forward fixture and the scorer.

These tests do not run the full forward round (that is a Task 8 operational
step). They verify the fixture is internally consistent, the scorer handles
synthetic PASS and FAIL responses, and the scorer itself does not introduce
forbidden scheduler concepts into generic scripts.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parents[1]
FORWARD = ROOT / "tests" / "forward"
FORWARD_CASE = FORWARD / "non-comms-baseline-extension.yaml"
PRAGMATIC_CASE = FORWARD / "pragmatic-baseline-adjudication.yaml"
CROSS_OUTPUT_CASE = FORWARD / "cross-output-portfolio-fairness.yaml"
PROBE_COST_CASE = FORWARD / "probe-cost-boundary.yaml"
SEMANTIC_CASE = FORWARD / "semantic-integrity-separation.yaml"
RECOVERY_CASE = FORWARD / "recovery-current-precedence.yaml"
SCORER = ROOT / "tests" / "score_forward_tests.py"
BASELINE_SCORER = ROOT / "tests" / "score_baseline_adjudication.py"
CROSS_OUTPUT_SCORER = ROOT / "tests" / "score_cross_output_portfolio.py"
PROBE_RECOVERY_SCORER = ROOT / "tests" / "score_probe_recovery.py"


def _load_scorer():
    spec = importlib.util.spec_from_file_location("score_forward_tests", SCORER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_baseline_scorer():
    spec = importlib.util.spec_from_file_location(
        "score_baseline_adjudication", BASELINE_SCORER
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_cross_output_scorer():
    spec = importlib.util.spec_from_file_location(
        "score_cross_output_portfolio", CROSS_OUTPUT_SCORER
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_probe_recovery_scorer():
    spec = importlib.util.spec_from_file_location(
        "score_probe_recovery", PROBE_RECOVERY_SCORER
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_non_comms_fixture_has_closed_contract():
    case = yaml.safe_load(FORWARD_CASE.read_text(encoding="utf-8"))
    assert set(case) == {
        "schema_version",
        "case_id",
        "decision_point",
        "domain_note",
        "facts",
        "artifacts",
        "allowed_actions",
        "forbidden_actions",
        "claim_ceiling",
    }
    assert case["schema_version"] == 1
    assert case["case_id"] == "non-comms-baseline-extension"
    assert case["artifacts"] == []
    assert case["claim_ceiling"]["level"] == "DIAGNOSTIC"
    assert set(case["allowed_actions"]).isdisjoint(case["forbidden_actions"])


def test_non_comms_fixture_carries_no_project_pointers():
    text = FORWARD_CASE.read_text(encoding="utf-8")
    forbidden = (
        "dual-pol",
        "OSL",
        "CMA",
        "B00",
        "P01",
        "P03",
        "Gamma-Gamma",
        "projects/",
        ".sessions/",
    )
    for token in forbidden:
        assert token not in text, token


def test_pragmatic_baseline_fixture_has_closed_contract():
    case = yaml.safe_load(PRAGMATIC_CASE.read_text(encoding="utf-8"))
    assert set(case) == {
        "schema_version",
        "case_id",
        "decision_point",
        "domain_note",
        "facts",
        "allowed_actions",
        "forbidden_actions",
        "claim_ceiling",
    }
    assert case["case_id"] == "pragmatic-baseline-adjudication"
    assert case["claim_ceiling"]["level"] == "DIAGNOSTIC"
    assert any("current SOTA" in item for item in case["forbidden_actions"])


def test_skill_routes_pragmatic_baseline_adjudication_reference():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    reference = ROOT / "references" / "baseline-adjudication.md"
    assert reference.exists()
    policy = reference.read_text(encoding="utf-8")
    assert "PROBLEM_SURVIVES_CONVENTIONAL_BASELINE" in policy
    assert "need not be current SOTA" in policy
    assert "widely used" in policy
    assert "baseline-adjudication.md" in skill


def test_cross_output_portfolio_fixture_has_closed_contract():
    case = yaml.safe_load(CROSS_OUTPUT_CASE.read_text(encoding="utf-8"))
    assert set(case) == {
        "schema_version",
        "case_id",
        "decision_point",
        "domain_note",
        "facts",
        "allowed_actions",
        "forbidden_actions",
        "claim_ceiling",
    }
    assert case["case_id"] == "cross-output-portfolio-fairness"
    assert case["claim_ceiling"]["level"] == "PORTFOLIO_PLANNING"
    assert any("task-specific comparators" in item for item in case["allowed_actions"])


def test_skill_distinguishes_shared_anchor_from_task_specific_comparators():
    baseline = (ROOT / "references" / "baseline-adjudication.md").read_text(
        encoding="utf-8"
    )
    batch = (ROOT / "references" / "batch-and-atlas.md").read_text(
        encoding="utf-8"
    )
    assert "shared system anchor" in baseline
    assert "task-specific comparator" in baseline
    assert "equal tuning opportunity" in baseline
    assert "shared system anchor" in batch
    assert "task-specific comparator" in batch


def test_skill_requires_bounded_mechanism_level_portfolio_refresh():
    portfolio = (ROOT / "references" / "candidate-portfolio.md").read_text(
        encoding="utf-8"
    )
    assert "Bounded portfolio refresh" in portfolio
    assert "mechanism-level" in portfolio
    assert "NEEDS_SMALL_ADAPTER" in portfolio
    assert "INFRASTRUCTURE_BLOCKED" in portfolio


@pytest.mark.parametrize(
    ("path", "case_id"),
    [
        (PROBE_COST_CASE, "probe-cost-boundary"),
        (SEMANTIC_CASE, "semantic-integrity-separation"),
        (RECOVERY_CASE, "recovery-current-precedence"),
    ],
)
def test_probe_redesign_fixtures_have_closed_generic_contract(path, case_id):
    case = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert set(case) == {
        "schema_version",
        "case_id",
        "decision_point",
        "domain_note",
        "facts",
        "allowed_actions",
        "forbidden_actions",
        "claim_ceiling",
    }
    assert case["schema_version"] == 1
    assert case["case_id"] == case_id
    assert case["claim_ceiling"]["level"] == "DIAGNOSTIC"
    assert set(case["allowed_actions"]).isdisjoint(case["forbidden_actions"])
    text = path.read_text(encoding="utf-8").lower()
    for forbidden in ("dual-pol", "osl", "cma", "16qam", "projects/", ".sessions/"):
        assert forbidden not in text


def test_cross_output_scorer_distinguishes_real_red_and_fresh_green():
    scorer = _load_cross_output_scorer()
    run_root = FORWARD / "runs" / "cross-output-portfolio-fairness"
    red = scorer.score_response(run_root / "round-red.md")
    green = scorer.score_response(run_root / "round-green.md")
    assert red["verdict"] == "FAIL"
    assert green["verdict"] == "PASS"
    assert not red["checks"]["task_specific_comparators"]
    assert not red["checks"]["readiness_honesty"]
    assert green["checks"]["equal_tuning_opportunity"]
    assert green["checks"]["observability_not_gain"]


def test_pragmatic_baseline_scorer_distinguishes_red_and_green():
    scorer = _load_baseline_scorer()
    run_root = FORWARD / "runs" / "pragmatic-baseline-adjudication"
    red = scorer.score_response(run_root / "round-red.md")
    green = scorer.score_response(run_root / "round-green.md")
    assert red["verdict"] == "FAIL"
    assert green["verdict"] == "PASS"
    assert not red["checks"]["ml_gate"]
    assert not red["checks"]["portfolio_continues"]
    assert not red["checks"]["pragmatic_stop"]
    assert green["checks"]["pragmatic_stop"]
    assert green["checks"]["portfolio_continues"]


def test_probe_recovery_runs_store_blind_prompt_and_verbatim_response():
    run_names = (
        ("probe-cost-boundary", "round-red.md"),
        ("probe-cost-boundary", "round-green.md"),
        ("semantic-integrity-separation", "round-red.md"),
        ("semantic-integrity-separation", "round-green.md"),
        ("recovery-current-precedence", "round-green.md"),
    )
    for case_id, filename in run_names:
        text = (FORWARD / "runs" / case_id / filename).read_text(encoding="utf-8")
        assert "## Blind prompt" in text
        assert "## Raw response" in text
        raw = text.split("## Raw response", 1)[1].split("## Behavior scorer output", 1)[0]
        assert len(raw.encode("utf-8")) >= 900
        assert "Verdict: PASS" not in raw


def test_probe_recovery_behavior_scorer_distinguishes_red_and_green():
    scorer = _load_probe_recovery_scorer()
    probe_root = FORWARD / "runs" / "probe-cost-boundary"
    semantic_root = FORWARD / "runs" / "semantic-integrity-separation"
    recovery_root = FORWARD / "runs" / "recovery-current-precedence"

    assert scorer.score_response("probe-cost-boundary", probe_root / "round-red.md")[
        "verdict"
    ] == "FAIL"
    assert scorer.score_response("probe-cost-boundary", probe_root / "round-green.md")[
        "verdict"
    ] == "PASS"
    assert scorer.score_response(
        "semantic-integrity-separation", semantic_root / "round-red.md"
    )["verdict"] == "FAIL"
    assert scorer.score_response(
        "semantic-integrity-separation", semantic_root / "round-green.md"
    )["verdict"] == "PASS"
    assert scorer.score_response(
        "recovery-current-precedence", recovery_root / "round-green.md"
    )["verdict"] == "PASS"


def test_scorer_marks_a_clear_pass_response(tmp_path):
    scorer = _load_scorer()
    response = """\
1. Recovered facts
- JIT register allocator baseline is linear-scan.
- Three candidate families: graph-coloring, tree-scan, ML cost model.
- Graph-coloring is blocked because the IR lacks a stable interference-graph contract.
- ML trial showed 12% spilled_cycles reduction against an oracle that double-counted rematerializable ranges.
- The corrected oracle counts each live range once; the legal ML increment is unresolved.
- No benchmark suite, queue, registry, or formal promotion exists.

2. Recovered authorization, anchor, mode
- Authorization: portfolio review only; no formal performance registry.
- Anchor: linear-scan over linearized live intervals; metrics spilled_cycles and reg_pressure_peak.
- Mode: planning; awaiting a legal comparator.

3. Claim ceiling
- Level: DIAGNOSTIC.
- Statement: the 12% reduction is a comparator-identity confound against a buggy oracle; the legal ML increment is unresolved and graph-coloring is infrastructure-blocked.

4. Harvest items
- failure_mechanism: oracle double-counted rematerializable ranges; evidence pointer tests/forward/non-comms-baseline-extension.yaml.
- infrastructure_gap: stable interference-graph contract missing for graph-coloring; evidence pointer tests/forward/non-comms-baseline-extension.yaml.

5. Next automatic action
- Preregister a shared-IR comparison with the corrected oracle against linear-scan and tree-scan, rotating to tree-scan while the interference-graph contract is unbuilt.

6. User escalation
- Not required now; legal alternatives exist.

7. Files read
- .agents/skills/research-direction-lab/SKILL.md
- tests/forward/non-comms-baseline-extension.yaml
"""
    out = tmp_path / "smoke-pass.md"
    out.write_text(response, encoding="utf-8")
    result = scorer.score_case("non-comms-baseline-extension", out)
    assert result["checks"]["B1_continuation"]
    assert result["checks"]["B4_no_false_comparator_promotion"]
    assert result["checks"]["B5_harvest"]
    assert result["checks"]["B6_concrete_next_action"]
    assert result["checks"]["B9_domain_isolation"]
    assert not result["p0_violations"]


def test_scorer_flags_false_comparator_promotion(tmp_path):
    scorer = _load_scorer()
    response = """\
1. Recovered facts
- ML cost model beat linear-scan by 12%.

2. Recovered authorization, anchor, mode
- Mode: ready to publish.

3. Claim ceiling
- Level: DOMAIN.
- Statement: ML cost model is superior across the JIT domain.

4. Harvest items
- method_signal: ML wins; evidence pointer tests/forward/non-comms-baseline-extension.yaml.

5. Next automatic action
- Continue exploring ML.

6. User escalation
- None.

7. Files read
- SKILL.md
"""
    out = tmp_path / "smoke-fail.md"
    out.write_text(response, encoding="utf-8")
    result = scorer.score_case("non-comms-baseline-extension", out)
    assert "false_comparator_promotion" in result["p0_violations"]
    assert "claim_overreach" in result["p0_violations"]
