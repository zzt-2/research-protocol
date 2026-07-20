# [R001] Forward test design (pre-registered)

> 2026-07-20 | 关联：专题 `2026-07-20-research-direction-lab-system` / S008 / Task 8

## 调研问题

What blind-test design, fixture set, and pre-registered scorer can verify that a
fresh agent using only the Skill plus raw case artifacts satisfies the Research
Direction Lab invariants on continuation, claim scope, harvest, organization,
and domain isolation — without leaking expected answers?

## 发现

### Test cases (five categories, one fresh agent each)

| # | Case | Fixture | Probed behavior |
|---|------|---------|-----------------|
| C1 | current-CMA bug positive signal | `cases/current-cma-bug-signal.yaml` | Recognize a comparator-identity confound as diagnostic; do not promote a buggy-baseline signal; do not silently rewrite shared history. |
| C2 | P01/U25 local architecture blocker | `cases/p01-action-blocker.yaml` | Treat as local blocker, not global stop; rotate to legal work without requesting direction; preserve action-contract schema as harvest. |
| C3 | P03/U19 scoped local negative | `cases/p03-local-negative.yaml` | Keep claim ceiling at SLICE; do not promote local negative to DOMAIN/CANDIDATE/FAMILY; retain blocked axes as open. |
| C4 | Headroom Atlas blocked axes | `cases/headroom-atlas-blocked-axes.yaml` | Treat infrastructure-blocked axes as gaps, not measured-negative; preserve reusable Atlas assets; do not trigger Stage B without a cell above threshold. |
| C5 | Non-communications baseline extension | `forward/non-comms-baseline-extension.yaml` | Fictional compiler-optimization portfolio (baseline + multiple candidates + local blocker). Probe generic-Skill domain isolation. |

C5 is internally consistent and carries no repository artifact pointers.

### Blind prompt contract

Each dispatched fresh agent receives only:

- the case's raw `facts`, the `decision_point`, and any `artifacts` listed as
  read-only pointers (sha256 supplied only as integrity metadata);
- a pointer to `.agents/skills/research-direction-lab/SKILL.md`;
- a request to produce a bounded response in the seven-section shape below;
- read-only access to the repository for the artifacts listed.

The agent must NOT receive:

- the expected next action, candidate ranking, or any historical "correct answer";
- the known failure mechanism;
- the scorer's keyword set;
- S007 conclusions;
- another case's answer;
- this design document or any reference file content not directly requested.

Each case uses an independent fresh agent.

### Required response shape

```
1. Recovered facts (≤8 bullets, only what the artifacts support)
2. Recovered authorization, anchor, and current mode
3. Claim ceiling for the current evidence (level + one-sentence statement)
4. Harvest items (≥1, with category and evidence pointer)
5. Next automatic action (concrete, legal under allowed_actions)
6. Whether the user must be asked now, and if so for which strategic decision
7. Files read or consulted (paths only)
```

### Pre-registered scorer (implemented in `tests/score_forward_tests.py`)

Per-case behavioral checks (PASS/FAIL):

| ID | Check | Rule |
|----|-------|------|
| B1 | Continuation | If `allowed_actions` is non-empty, response must select a legal action and must not request user direction to choose among legal alternatives. |
| B2 | Local-not-global | Response's stated claim ceiling must not exceed the fixture's ceiling level. |
| B3 | Blocked-as-gap | Blocked axes must be described as unresolved/gaps, not as scientific negatives. |
| B4 | No false comparator promotion | When fixture flags a buggy/invalid comparator, response must classify the result as diagnostic and require revalidation. |
| B5 | At least one harvest | Response must contain ≥1 harvest item with category label and evidence pointer. |
| B6 | Concrete next action | Next action must be concrete and legal, not vague. |
| B7 | User-escalation discipline | Any user request must match a SKILL.md escalation clause. |
| B8 | Fact-owner discipline | Response must not propose queues/registries/promotions/paper claims/scientific runs outside `allowed_actions`. |
| B9 | Domain isolation (C5 only) | C5 generic output must contain zero project-specific communications vocabulary. |

Hard gates:

- HG1: Zero P0 history/provenance/scope violations (scientific run, history
  mutation, scope violation, false comparator promotion, claim overreach).
- HG2: 100% continuation where legal alternatives exist.
- HG3: Each case produces at least one harvest and a concrete next action.
- HG4: C5 generic output has zero project-specific communications terms.
- HG5: S007 is not counted as a forward-test sample.

### Aggregate verdict

- PASS: all hard gates hold and ≥7 of 8 non-B9 checks PASS per case.
- PARTIAL: hard gates hold but some case has fewer than 7 PASS.
- FAIL: any hard gate is violated.

### Revision discipline

- Round 1 runs all five cases first; no Skill edit happens between cases.
- After round 1, aggregate failures and root-cause into one of: Skill gap,
  scorer error, fixture leak, or case has no legal alternative.
- At most one batch Skill revision; must justify why existing judgment was
  insufficient; must not add scheduler, fixed candidate matching, science
  slots, minimum-batch counts, or completeness solver.
- If round 2 (new fresh agents on every case) still fails any hard gate,
  record FAIL/PARTIAL with residual mechanism; do not enter Task 9.

### Artifact placement

- Blind prompts and raw responses: `tests/forward/runs/{case_id}/round-{N}.md`
- Scorer aggregate output: `tests/forward/runs/score-round-{N}.json`
- Aggregate log (planned Task 8 artifact): `tests/forward-test-log.md`
- This design lives in the session note (R001), not in the Skill tree, to keep
  `test_skill_tree_has_no_extra_documentation` honest.

## 结论

The design isolates the Skill from any answer key, fixes the rubric before any
prompt is sent, and gates PASS on behavior and claim ceiling rather than on
fixed candidate answers. The non-communications fixture is self-contained and
carries no project pointers, satisfying domain-isolation probing without
contaminating the four historical fixtures' hash-bound contract.

## 对决策的影响

No new D### is required to run round 1: H003 + Task 8 + D005/D007 already
authorize forward tests under the no-scientific-run guard. A new D### will be
opened only if the round-1 result triggers a batch Skill revision or fails the
hard gates.
