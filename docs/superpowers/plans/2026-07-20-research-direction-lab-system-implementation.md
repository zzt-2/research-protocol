# Research Direction Lab System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and activate a Skill-first, code-guarded research exploration system that can continuously map, batch, interpret, rotate, and harvest research directions without embedding scientific scheduling in a universal controller.

**Architecture:** A concise `research-direction-lab` Skill owns the open-ended research loop and loads focused references on demand. Generic scripts protect deterministic integrity only; a Communications Profile carries domain conventions, and a project adapter carries dual-pol OSL facts. Historical Direction Lab artifacts remain immutable and are migrated by pointer before any live shadow run.

**Tech Stack:** Markdown/YAML, Python 3.11+, pytest, existing project runners and receipt/hash utilities, Codex Skills progressive disclosure.

## Global Constraints

- Source of truth for the new Skill is `.agents/skills/research-direction-lab/` in this repository.
- Execute the plan in a fresh worktree created from the branch that contains the frozen P03/Headroom Atlas evidence; do not implement inside the currently dirty main or `p03-residual-headroom` worktree.
- Do not modify or run B001–B003, P03 raw artifacts, `canonical-state.yaml`, formal paper materials, or the canonical baseline during Tasks 1–8.
- Do not add `science_slots`, fixed portfolio-completeness counts, candidate/resource matching, work-conservation solvers, or domain terms to generic scripts.
- Generic Python files must not contain `BER`, `SNR`, `CMA`, `pilot`, `OSL`, `QPSK`, or `Jones`; domain terms belong in the Communications Profile or project adapter.
- Project-specific paths and component IDs must not appear in generic scripts or core Skill instructions.
- Use TDD for every Python change and preserve existing user worktree changes.
- Per repository policy, make at most one consolidated commit per execution conversation; do not follow a per-step commit instruction when several tasks run in one conversation.
- A live scientific shadow requires a fresh isolated worktree, `sim-preflight`, an explicit experiment contract, and user authorization in the execution turn.

---

### Task 1: Freeze requirement traceability and target ownership

**Files:**
- Modify: `.sessions/2026-07-20-research-direction-lab-system/voice.md`
- Modify: `.sessions/2026-07-20-research-direction-lab-system/decisions.md`
- Modify: `docs/superpowers/specs/2026-07-20-research-direction-lab-system-blueprint.md`

**Interfaces:**
- Consumes: U01–U15 from the blueprint and the three cited `voice.md` files.
- Produces: a complete traceability appendix for U01–U15 without duplicating the original quotes.

- [ ] **Step 1: Audit quote provenance**

Mark copied execution prompts as `[转述:执行提示词]`; keep the user's natural-language statements unprefixed. Do not duplicate the full historical voice into the new topic.

- [ ] **Step 2: Add a traceability appendix to the blueprint**

For every U01–U15, point to its source voice location and owning architecture section. Reject any design rule with no user, evidence-integrity, or project-safety source.

- [ ] **Step 3: Verify requirement coverage**

Run:

```powershell
python -c "import re; p=open('docs/superpowers/specs/2026-07-20-research-direction-lab-system-blueprint.md',encoding='utf-8').read(); assert {f'U{i:02d}' for i in range(1,16)} <= set(re.findall(r'U\d{2}',p))"
```

Expected: exit code `0`.

### Task 2: Scaffold the Skill and freeze progressive disclosure

**Files:**
- Create: `.sessions/2026-07-20-research-direction-lab-system/S002-skill-red-baseline.md`
- Create: `.agents/skills/research-direction-lab/SKILL.md`
- Create: `.agents/skills/research-direction-lab/agents/openai.yaml`
- Create: `.agents/skills/research-direction-lab/references/core-loop.md`
- Create: `.agents/skills/research-direction-lab/references/candidate-portfolio.md`
- Create: `.agents/skills/research-direction-lab/references/batch-and-atlas.md`
- Create: `.agents/skills/research-direction-lab/references/evidence-and-claims.md`
- Create: `.agents/skills/research-direction-lab/references/thesis-harvest.md`
- Create: `.agents/skills/research-direction-lab/references/recovery-and-rotation.md`
- Create: `.agents/skills/research-direction-lab/references/project-layout.md`
- Create: `.agents/skills/research-direction-lab/tests/cases/user-requirements.yaml`
- Test: `.agents/skills/research-direction-lab/tests/test_structure.py`

**Interfaces:**
- Consumes: target responsibilities in blueprint §§3–12.
- Produces: one triggerable Skill whose body routes to one-level references.

- [ ] **Step 1: Run RED pressure scenarios without the new Skill**

Create three blind scenarios that combine: a local blocker plus remaining candidates; a narrow negative result plus blocked axes; and a positive signal that may repair a buggy baseline. Dispatch fresh agents without exposing this blueprint or the future Skill. Record their next action, scope claim, harvest behavior, and rationalization verbatim in `S002-skill-red-baseline.md`. At least one scenario must reproduce a target failure; if all controls already comply, stop and remove guidance for behavior that does not need teaching.

- [ ] **Step 2: Initialize the Skill**

Run the official skill initializer before creating any child file:

```powershell
python C:\Users\zzt\.codex\skills\.system\skill-creator\scripts\init_skill.py research-direction-lab --path .agents/skills --resources scripts,references --interface 'display_name=Research Direction Lab' --interface 'short_description=Batch and sustain research direction exploration' --interface 'default_prompt=Use $research-direction-lab to recover this research foundation, map candidate families, run informative batches, harvest thesis material, and continue until a strategic decision is required.'
```

Expected: Skill directory, `SKILL.md`, and `agents/openai.yaml` created.

- [ ] **Step 3: Create the machine-readable requirement fixture**

Create `user-requirements.yaml` with one case per U01–U15. Use this exact shape:

```powershell
New-Item -ItemType Directory -Force .agents/skills/research-direction-lab/tests/cases | Out-Null
```

```yaml
schema_version: 1
requirements:
  - requirement_id: U04
    source_pointer: .sessions/2026-07-10-dual-pol-osl-groundwork/voice.md#2026-07-16
    scenario: one candidate is blocked while two legal candidates remain
    must_do: select another legal candidate without asking for direction
    must_not_do: stop the campaign or patch the blocked runner indefinitely
```

- [ ] **Step 4: Write RED structural tests**

```python
from pathlib import Path
import yaml

ROOT = Path(__file__).parents[1]

def test_skill_has_single_level_references():
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    for name in (
        "core-loop.md", "candidate-portfolio.md", "batch-and-atlas.md",
        "evidence-and-claims.md", "thesis-harvest.md",
        "recovery-and-rotation.md", "project-layout.md",
    ):
        assert f"references/{name}" in text

def test_skill_does_not_claim_project_state():
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8").lower()
    assert "last_completed_batch" not in text
    assert "b003" not in text

def test_all_user_requirements_have_cases():
    data = yaml.safe_load((ROOT / "tests/cases/user-requirements.yaml").read_text(encoding="utf-8"))
    assert {f"U{i:02d}" for i in range(1, 16)} == {item["requirement_id"] for item in data["requirements"]}
```

- [ ] **Step 5: Run RED test**

Run:

```powershell
python -m pytest .agents/skills/research-direction-lab/tests/test_structure.py -q
```

Expected: FAIL because the routed reference files do not exist.

- [ ] **Step 6: Write the concise SKILL.md**

Keep the body below 300 lines. It must contain only: responsibility boundary, startup recovery, the seven-phase loop, automatic continuation rules, user escalation rules, and exact reference routing.

- [ ] **Step 7: Write focused references**

Move detailed candidate mapping, atlas, evidence, harvest, recovery, and layout guidance into the seven files above. Do not create README, CHANGELOG, quick reference, or duplicated workflow documents.

- [ ] **Step 8: Validate structure**

Run:

```powershell
python -m pytest .agents/skills/research-direction-lab/tests/test_structure.py -q
python C:\Users\zzt\.codex\skills\.system\skill-creator\scripts\quick_validate.py .agents/skills/research-direction-lab
```

Expected: all tests PASS and validator exits `0`.

### Task 3: Add the Communications Profile and project-adapter contract

**Files:**
- Create: `.agents/skills/research-direction-lab/references/profiles/communications.md`
- Create: `.agents/skills/research-direction-lab/references/project-adapter-schema.yaml`
- Test: `.agents/skills/research-direction-lab/tests/test_domain_separation.py`

**Interfaces:**
- Consumes: generic Skill lifecycle.
- Produces: `ProjectAdapterV1` fields: `project_id`, `formal_goal`, `anchor`, `components`, `paths`, `runnable_axes`, `blocked_axes`, `historical_counterexamples`, `commands`, and `budgets`.

- [ ] **Step 1: Write RED separation tests**

```python
from pathlib import Path

ROOT = Path(__file__).parents[1]
GENERIC = [ROOT / "SKILL.md", *(ROOT / "scripts").glob("*.py")]
FORBIDDEN = {"ber", "snr", "cma", "pilot", "osl", "qpsk", "jones"}

def test_generic_files_are_domain_neutral():
    for path in GENERIC:
        text = path.read_text(encoding="utf-8").lower()
        assert not (FORBIDDEN & set(text.replace("_", " ").split())), path
```

- [ ] **Step 2: Write the Communications Profile**

Create the nested directory first:

```powershell
New-Item -ItemType Directory -Force .agents/skills/research-direction-lab/references/profiles | Out-Null
```

Document receiver-visible/training/evaluation/oracle information, communications metrics and units, common axes, comparator legality, coded/uncoded and hard/soft claim boundaries, and typical thesis contribution forms. Do not include dual-pol OSL paths or frozen parameter values.

- [ ] **Step 3: Write adapter schema**

Use a closed YAML schema with `additional_properties: false`. Keep scientific vocabulary in adapter values, not generic field names.

- [ ] **Step 4: Run tests**

Run:

```powershell
python -m pytest .agents/skills/research-direction-lab/tests/test_domain_separation.py -q
```

Expected: PASS.

### Task 4: Implement only the deterministic safety tools

**Files:**
- Create: `.agents/skills/research-direction-lab/scripts/hash_bundle.py`
- Create: `.agents/skills/research-direction-lab/scripts/validate_receipt.py`
- Create: `.agents/skills/research-direction-lab/scripts/append_event.py`
- Create: `.agents/skills/research-direction-lab/scripts/rebuild_state.py`
- Create: `.agents/skills/research-direction-lab/scripts/render_status.py`
- Test: `.agents/skills/research-direction-lab/tests/test_safety_tools.py`

**Interfaces:**
- Produces:
  - `hash_bundle(root: Path, paths: Sequence[Path]) -> dict[str, str]`
  - `validate_receipt(receipt: Mapping[str, object], expected: Mapping[str, str]) -> list[str]`
  - `append_event(path: Path, event: Mapping[str, object], expected_head: str | None) -> str`
  - `rebuild_state(events: Iterable[Mapping[str, object]]) -> dict[str, object]`
  - `render_status(adapter: Mapping, state: Mapping, portfolio: Mapping, harvest: Mapping) -> str`

- [ ] **Step 1: Write RED tests for deterministic behavior**

Cover sorted path hashing, traversal rejection, hash mismatch, replayed event IDs, wrong expected head, deterministic rebuild, and a status render that reports facts without selecting a candidate.

- [ ] **Step 2: Run RED tests**

```powershell
python -m pytest .agents/skills/research-direction-lab/tests/test_safety_tools.py -q
```

Expected: FAIL because functions do not exist.

- [ ] **Step 3: Implement minimal functions**

`rebuild_state` may derive completed IDs, stale IDs, last event head, and recorded next-action text. It must not rank candidates, allocate resources, count mechanism coverage, or decide stop legality.

- [ ] **Step 4: Run GREEN and domain-neutrality tests**

```powershell
python -m pytest .agents/skills/research-direction-lab/tests/test_safety_tools.py .agents/skills/research-direction-lab/tests/test_domain_separation.py -q
```

Expected: PASS.

### Task 5: Build historical replay cases before migrating live state

**Files:**
- Create: `.agents/skills/research-direction-lab/tests/cases/current-cma-bug-signal.yaml`
- Create: `.agents/skills/research-direction-lab/tests/cases/p01-action-blocker.yaml`
- Create: `.agents/skills/research-direction-lab/tests/cases/p03-local-negative.yaml`
- Create: `.agents/skills/research-direction-lab/tests/cases/headroom-atlas-blocked-axes.yaml`
- Create: `.agents/skills/research-direction-lab/tests/test_historical_replay.py`

**Interfaces:**
- Consumes: immutable pointers/hashes to existing reports only.
- Produces: scenario inputs and expected behavioral ceilings, not expected prose answers.

- [ ] **Step 1: Create sanitized replay cases**

Each case must contain only facts available at that historical decision point, plus `allowed_actions`, `forbidden_actions`, and `claim_ceiling`. Do not include the intended candidate ranking.

- [ ] **Step 2: Add artifact-pointer validation**

```python
from hashlib import sha256 as _sha256
from pathlib import Path
import yaml

CASES = Path(__file__).parent / "cases"

def sha256(path: Path) -> str:
    return _sha256(path.read_bytes()).hexdigest()

def load_cases():
    return [yaml.safe_load(path.read_text(encoding="utf-8")) for path in CASES.glob("*.yaml") if path.name != "user-requirements.yaml"]

def test_replay_artifacts_exist_and_are_hash_bound():
    for case in load_cases():
        for item in case["artifacts"]:
            assert Path(item["path"]).is_file()
            assert sha256(Path(item["path"])) == item["sha256"]
```

- [ ] **Step 3: Run replay fixture tests**

```powershell
python -m pytest .agents/skills/research-direction-lab/tests/test_historical_replay.py -q
```

Expected: PASS for artifact integrity. Behavioral forward tests remain a separate Task 8.

### Task 6: Create a read-only dual-pol OSL project adapter and harvest projection

**Files:**
- Create: `projects/thesis-fso/direction-lab/project.v1.yaml`
- Create: `projects/thesis-fso/direction-lab/portfolio/current.v1.yaml`
- Create: `projects/thesis-fso/direction-lab/harvest/ledger.v1.yaml`
- Create: `projects/thesis-fso/direction-lab/STATUS.v1.md`
- Test: `projects/thesis-fso/direction-lab/tests/test_skill_adapter_v1.py`

**Interfaces:**
- Consumes: existing anchor, CandidateMap/BatchPlan, B001–B003, P01/P03 reports, Headroom Atlas, failure registry, and source hashes.
- Produces: a read-only projection; it does not replace current canonical state or authorize a batch.

- [ ] **Step 1: Write RED adapter tests**

Check that all source pointers exist, all historical artifacts retain their hashes, B004 is absent, formal research remains BLOCKED, and the projection declares itself `READ_ONLY_MIGRATION_PREVIEW`.

- [ ] **Step 2: Build project.v1.yaml**

Map the correct standard-CMA anchor, runnable and blocked axes, component identities, protected paths, and existing runner commands. Do not copy raw results.

- [ ] **Step 3: Build portfolio and harvest projections**

Represent current candidates without claiming completeness. Harvest at least: current-CMA bug lesson, P01 architecture blocker, P03 local negative, residual-energy/BER separation, Atlas blocked axes, reusable runners, and governance-overhead lesson.

- [ ] **Step 4: Render STATUS.v1.md**

Use `render_status.py`. The page must answer the eight blueprint §12 questions and state that no new experiment is running.

- [ ] **Step 5: Verify no historical mutation**

Run:

```powershell
python -m pytest projects/thesis-fso/direction-lab/tests/test_skill_adapter_v1.py -q
```

Expected: tests PASS; the test compares protected file hashes captured in `project.v1.yaml` against disk bytes.

### Task 7: Audit and retire the scheduler design without deleting evidence

**Files:**
- Create: `projects/thesis-fso/direction-lab/control-migration-audit.md`
- Test: `.agents/skills/research-direction-lab/tests/test_no_scheduler_contract.py`

**Interfaces:**
- Consumes: `campaign_core.py`, `campaignctl.py`, adapter, and V035/V037 reports.
- Produces: per-function classification `KEEP_AS_UTILITY | MOVE_TO_ADAPTER | DELETE_SCHEDULER | ARCHIVE_UNUSED`.

- [ ] **Step 1: Inventory every public function and CLI command**

Record file/line, callers, domain terms, state mutation, scientific judgment, and migration disposition. Do not edit code in the same step.

- [ ] **Step 2: Obtain review of the audit**

Reject the audit if any `KEEP_AS_UTILITY` function ranks candidates, matches slots, proves portfolio completeness, or decides scientific stop conditions.

- [ ] **Step 3: Write RED no-scheduler tests**

Assert the new Skill scripts expose no `next_action`, `match_slot`, `work_conservation`, `min_valid_batches`, or `min_evidence_families` API.

- [ ] **Step 4: Extract only approved utilities**

Reimplement approved deterministic behavior in Task 4 scripts. Do not modify the dirty source worktree. Preserve old files and V035/V037 evidence until live activation passes.

- [ ] **Step 5: Verify**

```powershell
python -m pytest .agents/skills/research-direction-lab/tests/test_no_scheduler_contract.py .agents/skills/research-direction-lab/tests/test_safety_tools.py -q
```

Expected: PASS.

### Task 8: Forward-test Skill behavior on historical and synthetic research tasks

**Files:**
- Create: `.agents/skills/research-direction-lab/tests/forward-test-log.md`
- Create: `.agents/skills/research-direction-lab/tests/score_forward_tests.py`

**Interfaces:**
- Consumes: Skill, U01–U15 fixture, historical replay cases, and one non-communications fixture.
- Produces: per-case scores for continuation, scope, harvest, organization, and domain separation.

- [ ] **Step 1: Define blind prompts**

Prompts must tell a fresh agent to use the Skill and provide only raw case artifacts. Do not reveal expected failure mechanisms or the intended next action.

- [ ] **Step 2: Run at least five forward tests**

Cases: current-CMA bug signal, P01 blocker, P03 local negative, Atlas blocked axes, and a non-communications baseline-extension task.

- [ ] **Step 3: Score deterministically where possible**

The scorer must check: no false domain closure, no request for user direction when legal alternatives exist, at least one harvest item, explicit next action, and zero project-specific terms in the non-communications core output.

- [ ] **Step 4: Revise Skill once as a batch**

Aggregate failures before editing. Do not patch one sentence after each case. If the revision adds a new hard rule, justify why Skill judgment and existing invariants were insufficient.

- [ ] **Step 5: Re-run clean forward tests**

Expected: zero P0 history/scope violations, 100% continuation where alternatives exist, and harvest/status outputs in all cases.

### Task 9: Run a timeboxed shadow before live activation

**Files:**
- Create in a fresh worktree: `projects/thesis-fso/direction-lab/shadow/S001-contract.yaml`
- Create: `projects/thesis-fso/direction-lab/shadow/S001-observation.md`
- Modify after success: `projects/thesis-fso/direction-lab/README.md`
- Modify after success: `projects/thesis-fso/direction-lab/process.md`
- Modify after success: `C:/Users/zzt/.agents/skills/method-family-batch-exploration/SKILL.md`

**Interfaces:**
- Consumes: verified Skill, adapter preview, safety tools, and an explicitly authorized scientific scope.
- Produces: shadow evidence and, only after PASS, activation pointers and old-flow retirement notices.

- [ ] **Step 1: Create an isolated worktree**

Use `using-git-worktrees`; verify clean status and protect historical batches by hash.

- [ ] **Step 2: Load sim-preflight and freeze shadow contract**

The contract must state duration/budget, allowed scientific scope, no formal promotion, expected STATUS/harvest updates, and user-escalation conditions. It must not require a fixed number of batches or mechanism families.

- [ ] **Step 3: Run the Skill continuously**

Observe at least one blocker, one candidate rotation, one scope assessment, one harvest update, and one context recovery. If natural work does not produce all five, supplement with historical replay rather than fabricating scientific batches.

- [ ] **Step 4: Evaluate outcomes**

PASS requires: zero history/provenance P0, zero local-to-domain overclaim, 100% automatic continuation when legal alternatives existed, readable one-page STATUS, and at least one harvest per completed scientific batch. Governance overhead is recorded as a shadow baseline only; no percentage threshold is authorized until the baseline is measured and separately approved.

- [ ] **Step 5: Activate or roll back by pointer**

If PASS, make `process.md` a short project-instance pointer to the Skill, mark the old method-family Skill superseded by the new Skill, and set `STATUS.md` as the human entry. If PARTIAL/FAIL, keep existing flow active, record observations, and revise the Skill blueprint rather than adding a scheduler patch.

### Task 10: Final verification and cutover documentation

**Files:**
- Modify: `.sessions/2026-07-20-research-direction-lab-system/topic-index.md`
- Create if absent, otherwise modify: `.sessions/2026-07-20-research-direction-lab-system/verifications.md`
- Create if architecture is now real: `docs/architecture/research-direction-lab.md`
- Modify if architecture is now real: `docs/architecture/ARCHITECTURE.md`

**Interfaces:**
- Consumes: all task verifications and shadow result.
- Produces: one active execution owner and a documented rollback pointer.

- [ ] **Step 1: Run complete targeted tests**

```powershell
python -m pytest .agents/skills/research-direction-lab/tests projects/thesis-fso/direction-lab/tests/test_skill_adapter_v1.py -q
python C:\Users\zzt\.codex\skills\.system\skill-creator\scripts\quick_validate.py .agents/skills/research-direction-lab
```

Expected: all targeted tests PASS.

- [ ] **Step 2: Run owner and terminology scans**

```powershell
rg -n "process owner|唯一拥有者|science_slots|min_valid_batches|work_conservation" .agents/skills/research-direction-lab projects/thesis-fso/direction-lab
rg -ni "\b(BER|SNR|CMA|pilot|OSL|QPSK|Jones)\b" .agents/skills/research-direction-lab/SKILL.md .agents/skills/research-direction-lab/scripts
```

Expected: one active process owner; no scheduler contracts; no domain terms in generic core/scripts.

- [ ] **Step 3: Record independent verification**

Create a V### entry with `PASS | PARTIAL | FAIL`, exact commands, outputs, known debt, and whether live activation is allowed.

- [ ] **Step 4: Document current architecture only after activation**

Use `doc-steward` architecture mode. Anchor every entity/relationship to real files; do not copy target design into current architecture if shadow did not PASS.

- [ ] **Step 5: Consolidated commit**

At the end of the execution conversation, stage only files belonging to this system and create one descriptive commit. Do not push unless the user explicitly requests it.

## Self-Review Checklist

- Every U01–U15 requirement maps to a task or forward-test case.
- The plan creates one Skill owner, one Domain Profile, one Project Adapter, deterministic tools, one project status entry, and one harvest ledger.
- No task implements candidate/resource matching or fixed completeness counts.
- Historical artifacts remain immutable until after shadow PASS.
- Live science is explicitly gated by sim-preflight and user authorization.
- Cutover happens only after forward tests and a real shadow; architecture docs are not written as fiction.
