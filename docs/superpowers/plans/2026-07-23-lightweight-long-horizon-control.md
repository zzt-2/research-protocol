# Lightweight Long-Horizon Control Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `test-driven-development` for the guard and `session-governance` for `.sessions/` changes. This plan is executed inline in the current isolated worktree; no subagent dispatch is authorized.

**Goal:** Implement the R003 v0.1 foreground-lane binding with one small topic control block, one deterministic T authorization guard, and one isolated longitudinal-test mission entry.

**Architecture:** RDL mission topics keep a machine-readable nine-field control block at the top of `topic-index.md`. A small validator checks only that a T references the current control epoch and an allowed action class; it never ranks candidates or interprets scientific content. Existing Direction Lab current projections, formal `master-state.md`, H/T, worker logs, and artifacts remain the sole owners of their current facts.

**Tech Stack:** Markdown/YAML, Python 3 standard library + PyYAML, pytest.

## Global Constraints

- Do not select Pilot-Jones or any other scientific carrier during implementation.
- Do not run simulations, literature searches, MVE, Probe, Scout, or formal stage transitions.
- Do not create a scheduler, automatic candidate selector, per-fork manifest, or parallel current state.
- The control block stores action control only; it must not duplicate candidate metrics or formal scientific state.
- The guard validates `control_ref`, `control_epoch`, and `action_class` only.
- Ordinary work packages remain T + worker-log + optional artifact + commit; no S/D/V/H bundle.
- The live test uses one branch/worktree, not one worktree per package.
- Follow the repository rule of one consolidated commit for this conversation; do not make per-task commits.

---

### Task 1: RED tests for topic control and T authorization

**Files:**
- Create: `.agents/skills/research-direction-lab/tests/test_long_horizon_control.py`
- Create after RED: `.agents/skills/research-direction-lab/scripts/validate_task_control.py`

**Interfaces:**
- Consumes topic Markdown containing `RDL-CONTROL:START/END` and YAML key `rdl_control`.
- Consumes task Markdown containing `RDL-TASK-CONTROL:START/END` and YAML key `rdl_task_control`.
- Produces `validate_task_control(repo_root: Path, task_path: Path) -> list[str]`.

- [ ] **Step 1: Write failing parser/validator tests**

Tests must define these six concrete behaviors:

- `test_matching_epoch_and_allowed_action_passes`: valid topic/task fixtures return `[]`;
- `test_stale_epoch_is_rejected`: task epoch 0 against control epoch 1 returns `["stale_control_epoch"]`;
- `test_forbidden_action_is_rejected_even_if_listed_allowed`: an overlapping forbidden action returns `["forbidden_action:SCIENTIFIC_DISPATCH"]`;
- `test_missing_control_reference_is_rejected`: a nonexistent referenced topic returns `["missing_control_ref:.sessions/example/missing.md"]`;
- `test_control_block_rejects_unknown_or_missing_fields`: exact schema errors name the missing/extra field;
- `test_task_reference_cannot_escape_repo_root`: `../outside.md` returns `["control_ref_outside_repo"]`.

Fixtures use a nine-field control object:

```yaml
schema_version: rdl.foreground-control.v1
control_epoch: 1
role: SYSTEM_DESIGN
mission: design and validate the long-horizon protocol
active_lane: PROTOCOL_IMPLEMENTATION
authority_pointer: .sessions/example/decisions.md#D001
decision_gate: implementation not verified
allowed_actions: [PROTOCOL_IMPLEMENTATION, PROTOCOL_VERIFICATION]
forbidden_actions: [SCIENTIFIC_DISPATCH]
next_legal_action: implement and verify the minimal guard
```

The task object is:

```yaml
schema_version: rdl.task-control.v1
control_ref: .sessions/example/topic-index.md
control_epoch: 1
action_class: PROTOCOL_IMPLEMENTATION
```

- [ ] **Step 2: Run RED**

Run:

```powershell
python -m pytest .agents/skills/research-direction-lab/tests/test_long_horizon_control.py -q
```

Expected: collection/import failure because `validate_task_control.py` does not exist.

- [ ] **Step 3: Implement the minimal validator**

The script must:

1. extract exactly one marked YAML block from each Markdown file;
2. require exact field sets for `rdl_control` and `rdl_task_control`;
3. resolve `control_ref` inside `repo_root` and reject traversal/symlink escape;
4. compare integer epochs;
5. reject an action in `forbidden_actions`;
6. require the action in `allowed_actions`;
7. return stable sorted error strings;
8. expose a CLI returning exit 0 for PASS and exit 1 with one error per line for FAIL.

It must not import project code, inspect candidate names, or mutate files.

- [ ] **Step 4: Run GREEN and full safety regression**

```powershell
python -m pytest .agents/skills/research-direction-lab/tests/test_long_horizon_control.py -q
python -m pytest .agents/skills/research-direction-lab/tests -q
```

Expected: new tests PASS; full suite remains at least `90 passed, 1 skipped` plus the new tests.

---

### Task 2: Document the protocol in the single process owner

**Files:**
- Create: `.agents/skills/research-direction-lab/references/long-horizon-control.md`
- Modify: `.agents/skills/research-direction-lab/SKILL.md`
- Modify: `.agents/skills/research-direction-lab/tests/test_structure.py`
- Modify: `.agents/skills/research-direction-lab/tests/test_no_scheduler_contract.py`
- Modify: `.sessions/2026-07-20-research-direction-lab-system/topic-index.md`

**Interfaces:**
- Produces the exact control/task block schemas consumed by Task 1.
- Adds only RDL-long-running-mission routing; it does not change generic session-governance templates.

- [ ] **Step 1: Add failing structural assertions**

Tests require:

- `SKILL.md` routes long-running mission recovery to `long-horizon-control.md`;
- the new reference contains the exact nine control fields and three task fields;
- it explicitly says candidate facts/formal state remain in existing owners;
- it prohibits controller/scheduler behavior;
- it defines topic lifecycle: candidate rotation stays in exploration; formal promotion creates/restores formal topic; formal failure returns to existing exploration.

- [ ] **Step 2: Run RED**

```powershell
python -m pytest .agents/skills/research-direction-lab/tests/test_structure.py .agents/skills/research-direction-lab/tests/test_no_scheduler_contract.py -q
```

Expected: FAIL because the reference and routing do not exist.

- [ ] **Step 3: Add minimal Skill/reference text**

`SKILL.md` receives:

- startup instruction to read a present RDL foreground block before project current state;
- requirement that context loss or fork re-enters foreground recovery;
- task dispatch requirement to validate the T control binding;
- one reference-routing line.

`long-horizon-control.md` owns:

- control/task block schemas;
- role/lane/gate semantics;
- update order: scientific owner first, control block second;
- disposition meanings;
- topic lifecycle;
- single decision-uncertainty package;
- user four-item relay;
- explicit non-goals.

The system topic control block is inserted at the top with:

- role `SYSTEM_DESIGN`;
- active lane `PROTOCOL_IMPLEMENTATION`;
- allowed actions `PROTOCOL_IMPLEMENTATION`, `PROTOCOL_VERIFICATION`, `LIVE_TEST_PREPARATION`;
- forbidden actions `SCIENTIFIC_DISPATCH`, `SKILL_SCIENCE_CAMPAIGN`, `FORMAL_STAGE_CHANGE`;
- `next_legal_action` to verify and prepare the live-test mission.

- [ ] **Step 4: Run GREEN and full regression**

```powershell
python -m pytest .agents/skills/research-direction-lab/tests/test_structure.py .agents/skills/research-direction-lab/tests/test_no_scheduler_contract.py -q
python -m pytest .agents/skills/research-direction-lab/tests -q
```

Expected: all tests PASS with no scheduler/domain leakage.

---

### Task 3: Create the longitudinal-test mission and fork handoff

**Files:**
- Create: `.sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md`
- Create: `.sessions/2026-07-23-research-direction-lab-longitudinal-test/S001-live-test-activation.md`
- Create: `.sessions/2026-07-23-research-direction-lab-longitudinal-test/H001-fork-live-test.md`
- Create: `.sessions/2026-07-23-research-direction-lab-longitudinal-test/voice.md`
- Modify: `.sessions/_registry.yaml`
- Modify: `.sessions/2026-07-20-research-direction-lab-system/S014-post-r002-live-recovery-failure.md`
- Modify: `.sessions/2026-07-20-research-direction-lab-system/decisions.md`
- Modify: `.sessions/2026-07-20-research-direction-lab-system/topic-index.md`
- Modify: `.sessions/2026-07-20-research-direction-lab-system/voice.md`

**Interfaces:**
- The live topic control block begins at epoch 1, role `LIVE_TEST`, lane `RECOVER_MAP`.
- Its authority pointers reference current project/formal owners; it does not activate science.
- H001 binds the fork to this topic and requires three factual checks.

- [ ] **Step 1: Create the live mission within the existing registry rules**

The original goal is to validate the long-horizon protocol on real research feedback while keeping the user on a four-item relay.

Initial allowed actions:

```yaml
- RECOVER
- PORTFOLIO_MAP
- STATE_RECONCILIATION
- TASK_BRIEF_PREPARATION
```

Initial forbidden actions:

```yaml
- SCIENTIFIC_EXPERIMENT
- FORMAL_STAGE_CHANGE
- SKILL_EDIT
- INFRASTRUCTURE_BUILD
```

The decision gate is “a legal scientific carrier and first decision package have not yet been selected from current authoritative state.”

- [ ] **Step 2: Record adoption without fabricating scientific authorization**

Add D017 only after Tasks 1–2 tests pass. D017 adopts the lightweight interface and explicitly states:

- system design completion does not authorize any scientific candidate;
- the fork first performs Recover/Map under the live topic;
- science authorization must come from the existing owner named by `authority_pointer`.

Record the triggering user voice already captured for D016; do not duplicate the zero-information “继续吧”.

- [ ] **Step 3: Validate session structure and control binding**

Run:

```powershell
python -c "import yaml, pathlib; yaml.safe_load(pathlib.Path('.sessions/_registry.yaml').read_text(encoding='utf-8'))"
python .agents/skills/research-direction-lab/scripts/validate_task_control.py --help
git diff --check
```

Manually confirm:

- topic-index contains original goal/current scope/explicit exclusions/invariants/current position;
- S001 contains all five anchors;
- H001 contains status/next/discipline and receiver verification;
- registry `depends_on` points to the system topic and `conflicts_with` is empty.

---

### Task 4: Consumer sync and final verification

**Files:**
- Sync changed `.agents/skills/research-direction-lab/` files to `C:\Users\zzt\.agents\skills\research-direction-lab\`.
- Modify only if verification finds a defect: files from Tasks 1–3.

**Interfaces:**
- Repo Skill is the source; global consumer copy must be byte-identical for every changed Skill file.

- [ ] **Step 1: Run repository validation**

```powershell
python -m pytest .agents/skills/research-direction-lab/tests -q
python C:\Users\zzt\.codex\skills\.system\skill-creator\scripts\quick_validate.py .agents/skills/research-direction-lab
python -m compileall -q .agents/skills/research-direction-lab/scripts
git diff --check
```

- [ ] **Step 2: Sync and verify hashes**

Copy only after repository tests pass. Verify all non-cache repo/global Skill files have identical relative paths and SHA256.

- [ ] **Step 3: Run installed-consumer smoke**

Run the new control tests against the global Skill and validate the live-test topic block from the repository worktree.

- [ ] **Step 4: Consolidated commit**

Review `git diff --stat`, `git diff --name-status`, and protected-path status. Create one commit summarizing protocol design, guard, live-test entry, and governance records. Do not push.
