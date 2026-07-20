# Direction Lab Baseline Adjudication Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use subagent-driven-development or executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a pragmatic, domain-neutral baseline adjudication gate to Research Direction Lab, record the resulting method decision, and produce a continuation prompt for formal use.

**Architecture:** Keep `SKILL.md` as the small process router. Put judgment-heavy baseline selection in one on-demand reference, make only minimal cross-reference changes to the loop/portfolio/evidence/harvest documents, and validate the behavior with a pressure case before and after the revision. Project-specific CMA/16QAM facts remain in the science topic, not in the universal Skill.

**Tech Stack:** Markdown Skill references, YAML forward fixture, Python pytest/scorer, `.sessions/` governance records.

## Global Constraints

- A defensible baseline need not be SOTA; it must be correct, task-appropriate, widely used, fair, and adequate for the exact claim.
- Oracle evidence remains a bound/Kill tool, never the Go comparator.
- Do not run scientific experiments, create B004, train ML, or modify protected historical evidence.
- Do not duplicate the new process in `AGENTS.md`.
- Make one consolidated commit at the end; do not push.

---

### Task 1: Capture the failing behavior

**Files:**
- Create: `.agents/skills/research-direction-lab/tests/forward/pragmatic-baseline-adjudication.yaml`
- Create: `.agents/skills/research-direction-lab/tests/forward/runs/pragmatic-baseline-adjudication/round-red.md`
- Modify: `.agents/skills/research-direction-lab/tests/test_forward_fixtures.py`

- [ ] Run a fresh agent against the current Skill and raw 16QAM-like facts.
- [ ] Record whether it either promotes ML too early or demands an unnecessary SOTA sweep.
- [ ] Add the fixture contract and a failing structural/behavior test for the missing adjudication behavior.

### Task 2: Implement the minimal Skill revision

**Files:**
- Create: `.agents/skills/research-direction-lab/references/baseline-adjudication.md`
- Modify: `.agents/skills/research-direction-lab/SKILL.md`
- Modify: `.agents/skills/research-direction-lab/references/core-loop.md`
- Modify: `.agents/skills/research-direction-lab/references/candidate-portfolio.md`
- Modify: `.agents/skills/research-direction-lab/references/batch-and-atlas.md`
- Modify: `.agents/skills/research-direction-lab/references/evidence-and-claims.md`
- Modify: `.agents/skills/research-direction-lab/references/thesis-harvest.md`
- Modify: `.agents/skills/research-direction-lab/references/profiles/communications.md`

- [ ] Define the four candidate sources and `M under C because A` problem card.
- [ ] Define the pragmatic baseline ladder and the `PROBLEM_SURVIVES_CONVENTIONAL_BASELINE` gate.
- [ ] Define explicit stopping rules that avoid both weak-baseline promotion and SOTA chasing.
- [ ] Link the new reference from the core router without adding project semantics.

### Task 3: Validate and record governance

**Files:**
- Modify: `.sessions/2026-07-20-research-direction-lab-system/decisions.md`
- Modify: `.sessions/2026-07-20-research-direction-lab-system/S011-consumer-deployment-cutover.md`
- Modify: `.sessions/2026-07-20-research-direction-lab-system/topic-index.md`
- Modify: `.sessions/2026-07-20-research-direction-lab-system/voice.md`
- Modify: `.sessions/2026-07-20-direction-lab-science-scout/decisions.md`
- Modify: `.sessions/2026-07-20-direction-lab-science-scout/S002-cb1-baseline-atlas-headroom.md`
- Modify: `.sessions/2026-07-20-direction-lab-science-scout/topic-index.md`
- Modify: `.sessions/2026-07-20-direction-lab-science-scout/voice.md`

- [ ] Re-run a fresh agent with the revised Skill and retain its raw response.
- [ ] Run focused tests, full Skill tests, quick validation, and independent review.
- [ ] Record the method-level decision and the science-incident correction without rewriting historical evidence.
- [ ] Sync the verified Skill byte-for-byte to the global consumer path.
- [ ] Write a self-contained new-conversation prompt that starts with conventional-baseline adjudication and then continues batch exploration.

