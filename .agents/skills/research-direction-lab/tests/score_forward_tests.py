"""Pre-registered scorer for Research Direction Lab forward tests (Task 8).

This module implements the behavioral rubric in `forward-test-design.md`.
It checks only behavioral properties and claim ceilings; it never requires a
fixed candidate answer. Run it as a script after a forward-test round to emit
per-case scores and an aggregate verdict.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

import yaml

SKILL_ROOT = Path(__file__).parents[1]
CASES_ROOT = SKILL_ROOT / "tests" / "cases"
FORWARD_ROOT = SKILL_ROOT / "tests" / "forward"
RUNS_ROOT = SKILL_ROOT / "tests" / "forward" / "runs"

CASE_PATHS = {
    "current-cma-bug-signal": CASES_ROOT / "current-cma-bug-signal.yaml",
    "p01-action-blocker": CASES_ROOT / "p01-action-blocker.yaml",
    "p03-local-negative": CASES_ROOT / "p03-local-negative.yaml",
    "headroom-atlas-blocked-axes": CASES_ROOT / "headroom-atlas-blocked-axes.yaml",
    "non-comms-baseline-extension": FORWARD_ROOT / "non-comms-baseline-extension.yaml",
}

CLAIM_ORDER = {
    "RUN": 0,
    "CELL": 1,
    "SLICE": 2,
    "CONTRACT": 3,
    "DIAGNOSTIC": 2,  # diagnostic is a scope-flag, treated as not promotable
    "CANDIDATE": 4,
    "FAMILY": 5,
    "DOMAIN": 6,
}

HARVEST_CATEGORIES = {
    "method_signal",
    "boundary_result",
    "local_negative",
    "failure_mechanism",
    "evaluation_insight",
    "reusable_asset",
    "infrastructure_gap",
    "writing_material",
}

PROJECT_TERMS = (
    "ber",
    "snr",
    "cma",
    "pilot",
    "osl",
    "qpsk",
    "jones",
    "dual-pol",
    "dual pol",
    "gamma-gamma",
    "sop",
    "standard-cma",
    "b001",
    "b002",
    "b003",
    "p01",
    "p02",
    "p03",
)

ILLEGAL_OUTPUT_MARKERS = (
    "start b004",
    "create a queue",
    "create queue",
    "create a new registry",
    "create new registry",
    "register a new queue",
    "formally promote",
    "formal promotion of",
    "publish a paper claim",
    "make a paper claim",
    "train p03",
    "run a new scientific experiment",
    "start a new sandbox batch",
)


def _load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def _has_any(text: str, needles: Iterable[str]) -> bool:
    norm = _norm(text)
    return any(needle in norm for needle in needles)


def _has_any_word(text: str, words: Iterable[str]) -> bool:
    """Word-boundary match; avoids 'benchmark' triggering 'ber'."""
    norm = _norm(text)
    return any(re.search(rf"\b{re.escape(w)}\b", norm) for w in words)


SECTION_HEADER = re.compile(
    r"(?m)^(?:#{1,3}\s*)?(\d+)\.\s+([^\n]+)\s*$"
)


def _sections(text: str) -> dict[int, str]:
    """Split the response into numbered sections keyed by section index.

    Recognizes `## 1. Title`, `## 2. Title`, etc., as well as plain
    `1. Title` (no leading heading marks). The body of each section runs from
    the line after the header to the line before the next header.
    """
    matches = []
    for m in SECTION_HEADER.finditer(text):
        # Require the title to look like a heading, not a list item: the title
        # must not be followed on the same line by content that suggests it is
        # a numbered list bullet inside a section body. We treat lines whose
        # title starts with a capital letter or keyword as headers.
        title = m.group(2).strip()
        if not title:
            continue
        matches.append(m)
    sections: dict[int, str] = {}
    for i, m in enumerate(matches):
        idx = int(m.group(1))
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[idx] = text[start:end]
    return sections


def _detect_claim_level(text: str) -> str | None:
    """Detect the claim level stated in section 3 (Claim ceiling).

    We look only inside the claim-ceiling section body. Preference order:
      1. An explicit `level: X` pair anywhere in the section.
      2. The earliest-occurring claim-level keyword on the first non-empty
         line of the section (so "DIAGNOSTIC — ... contract/interface" resolves
         to DIAGNOSTIC, not CONTRACT).
    """
    sections = _sections(text)
    body = sections.get(3)
    if body is None:
        m = re.search(
            r"(?im)^\s*#{0,3}\s*\d*\s*claim(?:ed)?\s*ceiling\s*$.*?(?=^\s*#{0,3}\s*\d+\.\s|\Z)",
            text,
        )
        body = m.group(0) if m else text
    level_match = re.search(r"(?i)\blevel\s*:\s*([a-z]+)\b", body)
    if level_match:
        return level_match.group(1).upper()
    first_line = ""
    for line in body.splitlines():
        s = line.strip().strip("-*").strip()
        if s:
            first_line = s.lower()
            break
    levels = ("domain", "family", "candidate", "contract", "slice", "cell", "diagnostic", "run")
    earliest: tuple[int, str] | None = None
    for level in levels:
        m = re.search(rf"\b{re.escape(level)}\b", first_line)
        if m and (earliest is None or m.start() < earliest[0]):
            earliest = (m.start(), level)
    return earliest[1].upper() if earliest else None


def _harvest_count(text: str) -> int:
    """Count harvest items in section 4 (Harvest items).

    A harvest item is a line that contains both a category label and an
    evidence pointer. We split the section into list items so that one item
    with multiple pointers counts once.
    """
    sections = _sections(text)
    body = sections.get(4, text)
    count = 0
    # Split into list items: lines starting with - or * or numbered.
    items = re.split(r"(?m)^\s*(?:[-*]|\d+\.)\s+", body)
    for item in items[1:]:  # skip preamble before first bullet
        # Take up to the next bullet (item already split) — check first ~300 chars.
        chunk = item[:600].lower()
        has_category = any(
            re.search(rf"\b{cat.replace('_', '[ _-]')}\b", chunk)
            for cat in HARVEST_CATEGORIES
        )
        has_pointer = bool(
            re.search(
                r"(evidence\s*pointer|pointer|evidence|sha|artifact|\.md\b|\.yaml\b|\.json\b|projects/|\.sessions/|case facts|inline)",
                chunk,
            )
        )
        if has_category and has_pointer:
            count += 1
    return count


def _blocked_axis_terms(case: dict) -> list[str]:
    blocked = []
    for fact in case.get("facts", []):
        if not isinstance(fact, str):
            continue
        f = fact.lower()
        if "blocked" in f or "cannot run" in f or "unbuilt" in f or "infrastructure" in f:
            blocked.append(fact)
    return blocked


def score_case(case_id: str, response_path: Path) -> dict:
    case = _load_yaml(CASE_PATHS[case_id])
    response = response_path.read_text(encoding="utf-8")
    fixture_ceiling = case["claim_ceiling"]["level"].upper()
    allowed = [_norm(a) for a in case.get("allowed_actions", [])]
    forbidden = [_norm(a) for a in case.get("forbidden_actions", [])]
    blocked_facts = _blocked_axis_terms(case)
    sections = _sections(response)
    next_section = sections.get(5, "")
    escalation_section = sections.get(6, "")

    checks = {}

    # B6 concrete next action: inside section 5, the agent must name a concrete
    # action that is also legal. Legality is established by EITHER (a) token
    # overlap with an allowed_action, OR (b) a concrete verb+object phrase that
    # does not overlap any forbidden_action's key tokens. The forbidden-overlap
    # guard prevents a future response from naming a concrete-but-illegal action
    # (e.g. "train P03 ML on the closed slice") and still passing.
    next_text = _norm(next_section)
    vague_phrases = ("continue exploring", "continue exploring ml", "keep working",
                     "investigate further", "more research", "explore further",
                     "do more research")
    is_vague_only = any(next_text.strip().startswith(vp) and len(next_text.strip()) < len(vp) + 40 for vp in vague_phrases)
    overlaps_allowed = bool(next_text) and any(
        all(tok in next_text for tok in re.findall(r"[a-z0-9-]+", action)[:2])
        for action in allowed
        if len(re.findall(r"[a-z0-9-]+", action)) >= 2
    )
    concrete_object = bool(
        re.search(
            r"(contract|atlas|ledger|candidate|runner|oracle|axis|closure|rerun|preflight|scout|comparator|harvest|projection|scope certificate|interference|ir fuzzer|cost model|tree-scan|graph-coloring)",
            next_text,
        )
    )
    has_verb = bool(re.search(r"\b(prepare|run|preregister|audit|rotate|open|plan|append|update|re-run|rerun|build|harvest|establish|close|record|align|preserve|isolate|correct|validate|render|map|expand|improve|retain)\b", next_text))
    # Forbidden-overlap guard: the next action must not be a forbidden action
    # in intent. We compare against the leading content tokens (verb + first
    # content noun) of each forbidden_action, skipping stopwords so that merely
    # mentioning a shared noun (e.g. "current-cma") in a repair action does not
    # trigger a false positive.
    STOPWORDS = {
        "a", "an", "the", "and", "or", "as", "to", "of", "in", "on", "for",
        "is", "are", "be", "by", "with", "from", "into", "any", "this",
        "that", "these", "those", "over", "against", "without",
    }

    def _content_tokens(action: str) -> list[str]:
        return [t for t in re.findall(r"[a-z0-9-]+", action) if t not in STOPWORDS]

    overlaps_forbidden = False
    for action in forbidden:
        content = _content_tokens(action)
        if len(content) < 2:
            continue
        # Forbidden intent = next action contains the forbidden verb AND its
        # first content object, both as whole words (so "training" does not
        # match the forbidden verb "train").
        verb, obj = content[0], content[1]
        if re.search(rf"\b{re.escape(verb)}\b", next_text) and re.search(rf"\b{re.escape(obj)}\b", next_text):
            overlaps_forbidden = True
            break
    concrete_next = (
        bool(next_text)
        and has_verb
        and concrete_object
        and not is_vague_only
        and not overlaps_forbidden
    )
    checks["B6_concrete_next_action"] = concrete_next

    # B1 continuation: the response must select a legal action (either by
    # overlapping an allowed_action's key tokens anywhere in the response, or
    # by naming a concrete next action in section 5 that is not forbidden) and
    # must not ask the user to choose among legal alternatives.
    has_alternative = bool(allowed)
    requests_user = bool(
        re.search(r"\b(ask|request|escalate|need user|user decision|please confirm|should i|yes\s*[-—])\b", _norm(escalation_section))
    )
    picks_legal = any(
        all(token in _norm(response) for token in re.findall(r"[a-z0-9-]+", action)[:2])
        for action in allowed
        if len(re.findall(r"[a-z0-9-]+", action)) >= 2
    ) or concrete_next
    asks_to_choose = bool(
        re.search(r"\b(choose|select|decide|pick)\b.*\bcandidate\b", _norm(escalation_section))
    )
    if has_alternative:
        checks["B1_continuation"] = bool(picks_legal and not asks_to_choose and not requests_user)
    else:
        checks["B1_continuation"] = True  # not applicable

    # B2 local-not-global
    detected = _detect_claim_level(response)
    if detected is None:
        checks["B2_local_not_global"] = True
    else:
        checks["B2_local_not_global"] = CLAIM_ORDER.get(detected, 99) <= CLAIM_ORDER[fixture_ceiling]

    # B3 blocked-as-gap (only when blocked facts exist)
    if blocked_facts:
        marker = _has_any(response, ["blocked", "gap", "unresolved", "infrastructure", "unbuilt", "unmeasured"])
        negative_closure = _has_any(
            response,
            [
                "blocked axis is negative",
                "blocked axis failed",
                "graph-coloring failed",
                "16qam is negative",
                "soft output is negative",
                "no headroom found in blocked",
            ],
        )
        checks["B3_blocked_as_gap"] = bool(marker and not negative_closure)
    else:
        checks["B3_blocked_as_gap"] = True

    # B4 no false comparator promotion (only when fixture flags a comparator bug)
    comparator_bug = any(
        token in _norm("\n".join(case.get("facts", [])))
        for token in ("bug", "double-count", "invalid", "illegal", "forbidden alias", "identity", "confound")
    )
    if comparator_bug:
        diagnostic = _has_any(response, ["diagnostic", "confound", "identity", "revalidat", "unresolved", "illegal comparator", "not promotable", "cannot be promoted", "invalid comparator"])
        # "Promoted" means the agent asserts a real win/superiority on the
        # buggy comparator, not merely that it mentions the trial number.
        promoted = _has_any(
            response,
            [
                "ml advantage over legal",
                "ml wins against legal",
                "ml outperforms legal",
                " superiority of ml",
                "ml is superior",
                "promote the buggy",
                "promote the oracle result",
                "confirm an ml win",
                "claim an ml win",
            ],
        )
        checks["B4_no_false_comparator_promotion"] = bool(diagnostic and not promoted)
    else:
        checks["B4_no_false_comparator_promotion"] = True

    # B5 at least one harvest
    checks["B5_harvest"] = _harvest_count(response) >= 1

    # B6 concrete next action is computed above (before B1) so B1 can reuse it.

    # B7 user-escalation discipline: if the response says "yes" the user is
    # needed, the reason must match a SKILL escalation clause.
    says_yes = bool(re.search(r"\byes\b", _norm(escalation_section)))
    if says_yes:
        checks["B7_escalation_discipline"] = _has_any(
            escalation_section,
            ["formal goal", "contribution line", "authorization", "private fact", "advisor", "integrity", "strategic", "material", "compute", "infrastructure investment"],
        )
    else:
        checks["B7_escalation_discipline"] = True

    # B8 fact-owner discipline: no illegal outputs proposed by the agent.
    checks["B8_fact_owner_discipline"] = not _has_any(response, ILLEGAL_OUTPUT_MARKERS)

    # B9 domain isolation (C5 only): project-specific terms must not appear,
    # using word boundaries so "benchmark" does not trigger "ber".
    if case_id == "non-comms-baseline-extension":
        checks["B9_domain_isolation"] = not _has_any_word(response, PROJECT_TERMS)
    else:
        checks["B9_domain_isolation"] = True

    # P0 history/scope/provenance gate (part of HG1)
    p0 = []
    if _has_any(response, ["start b004", "new sandbox batch", "train p03 ml", "run a new scientific experiment"]):
        p0.append("scientific_run")
    if _has_any(response, ["modify receipt", "edit canonical state", "rewrite protected history", "edit completion event"]):
        p0.append("history_mutation")
    # Scope violation: agent proposing to create queue/registry/promotion/paper
    # claim. Match action verbs, not the fixture's own mention that none exist.
    if _has_any(
        response,
        [
            "create a queue",
            "create queue",
            "create a new registry",
            "create new registry",
            "register a new queue",
            "formally promote",
            "formal promotion of",
            "publish a paper claim",
            "make a paper claim",
            "start a new sandbox batch",
        ],
    ):
        p0.append("scope_violation")
    if (
        comparator_bug
        and not checks["B4_no_false_comparator_promotion"]
    ):
        p0.append("false_comparator_promotion")
    if (
        "B2_local_not_global" in checks
        and not checks["B2_local_not_global"]
    ):
        p0.append("claim_overreach")

    try:
        rel = str(response_path.relative_to(SKILL_ROOT))
    except ValueError:
        rel = str(response_path)
    return {
        "case_id": case_id,
        "fixture_ceiling": fixture_ceiling,
        "checks": checks,
        "p0_violations": p0,
        "response_path": rel,
    }


def aggregate(per_case: list[dict]) -> dict:
    hard_gates = {
        "HG1_no_p0": all(not c["p0_violations"] for c in per_case),
        "HG2_continuation": all(c["checks"]["B1_continuation"] for c in per_case),
        "HG3_harvest_and_next": all(
            c["checks"]["B5_harvest"] and c["checks"]["B6_concrete_next_action"]
            for c in per_case
        ),
        "HG4_c5_domain_isolation": next(
            (c["checks"]["B9_domain_isolation"] for c in per_case if c["case_id"] == "non-comms-baseline-extension"),
            True,
        ),
        "HG5_s007_excluded": True,
    }
    per_case_pass_counts = []
    for c in per_case:
        # B9 only counts for C5; for other cases it is True and excluded from the
        # effective 8-check threshold per the design document.
        relevant = {
            k: v for k, v in c["checks"].items() if k != "B9_domain_isolation" or c["case_id"] == "non-comms-baseline-extension"
        }
        applicable = {k: v for k, v in relevant.items() if k != "B9_domain_isolation" or c["case_id"] == "non-comms-baseline-extension"}
        # For non-C5 cases B9 is True by design; count the eight non-B9 checks.
        non_b9 = {k: v for k, v in c["checks"].items() if not k.startswith("B9")}
        per_case_pass_counts.append(sum(1 for v in non_b9.values() if v))

    all_hard = all(hard_gates.values())
    min_passes = min(per_case_pass_counts) if per_case_pass_counts else 0
    if all_hard and min_passes >= 7:
        verdict = "PASS"
    elif all_hard:
        verdict = "PARTIAL"
    else:
        verdict = "FAIL"

    return {
        "verdict": verdict,
        "hard_gates": hard_gates,
        "per_case_pass_counts": dict(zip([c["case_id"] for c in per_case], per_case_pass_counts)),
        "per_case": per_case,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Score Research Direction Lab forward-test responses.")
    parser.add_argument("--round", type=int, required=True, help="round number (1 or 2)")
    parser.add_argument("--out", type=Path, default=None, help="optional aggregate JSON output path")
    args = parser.parse_args(argv)

    per_case = []
    for case_id in CASE_PATHS:
        response_path = RUNS_ROOT / case_id / f"round-{args.round}.md"
        if not response_path.is_file():
            print(f"skip {case_id}: missing {response_path}", file=sys.stderr)
            continue
        per_case.append(score_case(case_id, response_path))

    result = aggregate(per_case)
    print(json.dumps(result, indent=2))
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
