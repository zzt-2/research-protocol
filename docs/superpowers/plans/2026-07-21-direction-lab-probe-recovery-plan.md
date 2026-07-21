# Direction Lab Probe and Recovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a lightweight Probe layer and authoritative current-view recovery to Research Direction Lab without introducing a scheduler or project semantics.

**Architecture:** Keep the existing Skill as process owner. Update four existing references rather than adding another documentation layer; extend tests and only the deterministic state reducer where explicit disposition projection is needed. Keep project budgets and scientific thresholds outside the generic core.

**Tech Stack:** Markdown Skill references, YAML fixtures, Python 3, pytest.

## Global Constraints

- One consolidated commit at conversation close; no push.
- No new scientific experiment or old artifact mutation.
- Generic core contains no communications/project identifiers, formulas, parameters, or scientific thresholds.
- No scheduler, fixed candidate count, science slot allocator, or automatic candidate ranking.
- RED must precede Skill behavior edits; code changes use TDD.

---

### Task 1: Preserve RED behavior evidence

**Files:**
- Create: `.agents/skills/research-direction-lab/tests/forward/probe-cost-boundary.yaml`
- Create: `.agents/skills/research-direction-lab/tests/forward/semantic-integrity-separation.yaml`
- Create: `.agents/skills/research-direction-lab/tests/forward/runs/probe-cost-boundary/round-red.md`
- Create: `.agents/skills/research-direction-lab/tests/forward/runs/semantic-integrity-separation/round-red.md`

**Interfaces:** Consumes raw historical failure shapes; produces blind baseline artifacts for later GREEN comparison.

- [ ] Write behavior fixtures without expected verdict leakage.
- [ ] Save fresh-agent RED responses verbatim.
- [ ] Record which checks failed and which passed.

### Task 2: Add structural tests before Skill edits

**Files:**
- Modify: `.agents/skills/research-direction-lab/tests/test_structure.py`
- Modify: `.agents/skills/research-direction-lab/tests/test_forward_fixtures.py`
- Modify: `.agents/skills/research-direction-lab/tests/test_safety_tools.py`

**Interfaces:** Produces requirements for Probe vocabulary, semantic-before-scale order, current-view precedence, no mandatory Probe receipt/verifier/harvest, and explicit state dispositions.

- [ ] Add failing tests for Probe/Scout/Deep Evidence routing and anti-bloat output.
- [ ] Add failing reducer tests for completed→stale and explicit disposition replacement.
- [ ] Run targeted pytest and confirm failures cite missing behavior.

### Task 3: Implement minimal Skill/reference changes

**Files:**
- Modify: `.agents/skills/research-direction-lab/SKILL.md`
- Modify: `.agents/skills/research-direction-lab/references/core-loop.md`
- Modify: `.agents/skills/research-direction-lab/references/evidence-and-claims.md`
- Modify: `.agents/skills/research-direction-lab/references/project-layout.md`
- Modify: `.agents/skills/research-direction-lab/references/recovery-and-rotation.md`
- Modify: `.agents/skills/research-direction-lab/references/thesis-harvest.md`

**Interfaces:** Defines work intensity, promotion, semantic smoke, current precedence, directory ownership and harvest disposition; does not define project thresholds.

- [ ] Add concise three-intensity routing to SKILL.md.
- [ ] Define Probe one-record contract and promotion criteria in core-loop.
- [ ] Put semantic smoke before evidence scaling in evidence-and-claims.
- [ ] Define current-view/lineage and anti-inflation layout in project-layout/recovery.
- [ ] Replace mandatory harvest creation with mandatory harvest assessment.
- [ ] Run structure/domain/no-scheduler tests.

### Task 4: Extend deterministic disposition projection

**Files:**
- Modify: `.agents/skills/research-direction-lab/scripts/rebuild_state.py`
- Test: `.agents/skills/research-direction-lab/tests/test_safety_tools.py`

**Interfaces:** Consumes explicit events only; produces completed/stale current sets plus latest explicit entity dispositions. It never selects a scientific status.

- [ ] Make STALE remove a subject from current completed IDs.
- [ ] Add explicit `DISPOSITION` events with entity kind/id/status/reason/replacement pointer.
- [ ] Project only the latest explicit disposition per entity.
- [ ] Run targeted tests and keep no-scheduler test green.

### Task 5: GREEN forward tests and recovery rehearsal

**Files:**
- Create: `.agents/skills/research-direction-lab/tests/forward/runs/probe-cost-boundary/round-green.md`
- Create: `.agents/skills/research-direction-lab/tests/forward/runs/semantic-integrity-separation/round-green.md`
- Create: `.agents/skills/research-direction-lab/tests/forward/runs/recovery-current-precedence/round-green.md`
- Modify: `.agents/skills/research-direction-lab/tests/forward-test-log.md`

**Interfaces:** Fresh agents receive the revised Skill plus raw fixtures, not intended answers.

- [ ] Run fresh-agent cases and save raw responses.
- [ ] Check Probe does not create full Evidence artifacts.
- [ ] Check integrity PASS cannot override semantic FAIL.
- [ ] Check current projection overrides stale handoff/mtime.
- [ ] Independently review outputs and record remaining loopholes.

### Task 6: Deploy, document and hand off

**Files:**
- Update: `.sessions/2026-07-20-research-direction-lab-system/S012-probe-recovery-redesign-intake.md`
- Update: `.sessions/2026-07-20-research-direction-lab-system/decisions.md`
- Update: `.sessions/2026-07-20-research-direction-lab-system/verifications.md`
- Update: `.sessions/2026-07-20-research-direction-lab-system/topic-index.md`
- Update: `.sessions/2026-07-20-research-direction-lab-system/voice.md`
- Create: `.sessions/2026-07-20-research-direction-lab-system/H004-probe-recovery-system-ready.md`

**Interfaces:** Produces the next-conversation recovery entry and a directly usable large-campaign prompt.

- [ ] Run full Skill tests, quick validation, YAML/compile checks and protected-scope audit.
- [ ] Sync repo Skill to the global consumer path and verify byte identity.
- [ ] Run independent verifier.
- [ ] Record final design/verification and update registry.
- [ ] Commit once and provide the user prompt.
