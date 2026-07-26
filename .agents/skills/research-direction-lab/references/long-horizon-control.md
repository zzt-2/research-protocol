# Long-horizon foreground control

Use this reference only for a Research Direction Lab mission that spans multiple
master/executor work packages. Short topics do not need this interface.

## Responsibility boundary

The foreground control block binds the current master conversation to one
mission, lane, decision gate, and set of legal action classes. It does not own
candidate evidence or formal stage state. Those facts remain in the project
portfolio/current projections and formal framework owner named by
`authority_pointer`.

The block records a judgment already made by the master. It never computes or
selects the next action. Do not implement a scheduler or automatic candidate
selector.

Long-running RDL topics use three record layers: `topic-index.md` for the
current snapshot, fixed `mission-log.md` for one compact checkpoint per
accepted package, and T/worker-log/artifacts/commit for package detail.

## Topic control block

Place exactly one block near the top of the mission topic index:

<!-- RDL-CONTROL:START -->
```yaml
rdl_control:
  schema_version: rdl.foreground-control.v2
  control_epoch: 1
  role: LIVE_TEST
  mission: validate long-horizon research operation on real feedback
  active_lane: RECOVER_MAP
  authority_pointer: <existing-owner-pointer>
  decision_gate: a legal carrier has not been selected
  allowed_actions:
    - RECOVER
    - PORTFOLIO_MAP
  forbidden_actions:
    - SCIENTIFIC_EXPERIMENT
  mission_log_ref: <mission-log-path>
  mission_checkpoint: CP001
  next_legal_action: recover current owners and select one legal decision package
```
<!-- RDL-CONTROL:END -->

The exact fields are:

- `schema_version`
- `control_epoch`
- `role`
- `mission`
- `active_lane`
- `authority_pointer`
- `decision_gate`
- `allowed_actions`
- `forbidden_actions`
- `mission_log_ref`
- `mission_checkpoint`
- `next_legal_action`

`schema_version` is metadata; the remaining fields are the semantic foreground
contract. Replace the block in place. Do not append history to it.
Increment `control_epoch` only when its role, lane, gate, authorization classes,
mission checkpoint, or next legal action changes.

Keep the block small. Do not copy candidate lists, metrics, conclusions,
experiment details, formal progress tables, or user voice into it.
Schema v1 remains valid for historical tasks. New long-running method missions
use v2.

## Task binding

Before handing an executor a T task, include exactly one binding block:

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: <mission-topic-index-path>
  control_epoch: 1
  action_class: PORTFOLIO_MAP
  mission_checkpoint: CP001
```
<!-- RDL-TASK-CONTROL:END -->

The v2 exact fields are `schema_version`, `control_ref`, `control_epoch`,
`action_class`, and `mission_checkpoint`.

Run `scripts/validate_task_control.py` before dispatch. The validator only
checks that `control_ref` resolves inside the repository, `control_epoch`
matches, `action_class` is allowed and not forbidden, `mission_log_ref` exists,
and the task checkpoint matches the foreground checkpoint. It must not inspect
scientific vocabulary or rank work. The executor repeats this validation before
starting; a missing marker or failed validation means the task was not
dispatched.

## Master loop

1. Read the foreground block after startup, context loss, a fork, or a material
   user correction.
2. Read only the owner at `authority_pointer` needed for the current decision.
3. Read the complete compact mission-log chain. Separate formal science
   disposition from mission method delta and compare the proposed action with
   the best legal ready alternative.
4. Bind and validate one T against the current accepted mission checkpoint. A
   package may perform several bounded actions until it closes that uncertainty
   or reaches its stop condition.
5. Receive only status, commit, worker-log path, and one-line anomaly. Read the
   worker log and artifacts from disk.
6. Judge execution integrity separately from scientific information.
7. The executor never updates formal/current owners. After accepting evidence,
   the master updates those owners, appends the new mission checkpoint, then
   replaces the foreground block and increments its epoch.
8. Continue, rotate, transition, or escalate within the recorded action classes.

If the block and `authority_pointer` disagree, allow only reconciliation. A
conversation summary is a locator, not authority to change the active lane.
Read `method-production.md` for checkpoint fields, method packaging, drift
review, and repair-versus-rotation judgment.

## Disposition and topic lifecycle

Use existing portfolio evidence to distinguish failed, blocked, saturated,
diagnostic, Scout-ready, promotion-candidate, and harvested states. These labels
support explanation; they are not automatic transitions.

- Candidate rotation stays inside the exploration topic.
- Formal promotion creates or restores a formal topic.
- Formal failure returns to the existing exploration topic.
- A blocker does not create a topic.
- A master handoff uses H; an executor package uses T.
- A new topic is justified only by a mission, owner, or artifact-lifecycle
  change, not by a method variant or Probe result.

## Longitudinal evaluation

Audit real events rather than a fixed batch count: recovery, context loss,
local failure or blocking, rotation, promotion or non-promotion, ordinary
package weight, and later reconstruction from files. Record uncovered event
classes as unverified; never fabricate scientific events to make the process
test pass.
