"""Tests for the non-communications forward fixture and the scorer.

These tests do not run the full forward round (that is a Task 8 operational
step). They verify the fixture is internally consistent, the scorer handles
synthetic PASS and FAIL responses, and the scorer itself does not introduce
forbidden scheduler concepts into generic scripts.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import yaml

ROOT = Path(__file__).parents[1]
FORWARD = ROOT / "tests" / "forward"
FORWARD_CASE = FORWARD / "non-comms-baseline-extension.yaml"
SCORER = ROOT / "tests" / "score_forward_tests.py"


def _load_scorer():
    spec = importlib.util.spec_from_file_location("score_forward_tests", SCORER)
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
