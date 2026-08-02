# Method production and mission review

Use this reference for a long-running RDL mission whose purpose includes
producing thesis-usable methods. Scientific safety remains mandatory, but a
valid Kill is not method progress.

## Positive method contract

Every active carrier needs one compact contract in its existing authority
owner:

- `positive_method_target` — the deployable technical change to build.
- `minimal_construct` — the smallest runnable method slice.
- `fair_comparator` — a conventional, task-matched baseline.
- `primary_packaging` — the strongest defensible thesis framing.
- `fallback_packaging` — a bounded adaptation, low-complexity rule, operating
  regime, robustness result, or complexity/performance trade-off.
- `next_positive_action` — the next action that creates or compares a method.

Run only the smallest identity preflight needed to check signal order, physical
timescale, comparator task, oracle meaning, and single-seed or aggregation
artifacts. When those checks pass, run `minimal_construct` in the same package.
Do not make method execution the unreachable last step behind repeated generic
headroom gates.

## Contribution tiers

Assign every thesis-facing entry one current tier.

### `THESIS_MAIN_METHOD`

Require a real deployable action; a fair, tuned, task-matched conventional
comparator; stable mechanism and evidence; and enough structure to state method
steps, primary results, and a boundary. The claim need not assert unbounded
field-wide novelty, but the contribution must remain distinguishable under its
declared scope.

### `THESIS_ENGINEERING_COMPONENT`

Admit a genuine implementation contribution when it reduces measurement,
compute, hardware, or latency at matched performance; improves bounded
robustness at matched cost; makes an interpretable system-specific adaptation;
or combines conventional parts into a real control or implementation action.
It still requires a real action, fair comparator, valid evidence, and scoped
claim. Identity behavior, artifacts, and privileged truth cannot create the
component.

### `SUPPORTING_MATERIAL`

Use for valid negatives, boundaries, failure mechanisms, evaluation insights,
partial infrastructure, and writing material. `SUPPORTING_MATERIAL` does not
become an active carrier. Invalidated evidence may document a failure lesson
but cannot supply contribution numbers. A valid negative is not method
progress, and a packaging boundary is not a METHOD_SIGNAL. An old claim and
its corrective amendment are one lineage, not two contributions.

## Pre-formal method factory

Use `PREFORMAL_METHOD_FACTORY` only when all of these are true:

- the mission is explicitly method-producing;
- there is no active scientific carrier;
- a current portfolio remap reports both `READY=0` and
  `NEEDS_SMALL_ADAPTER=0`;
- the remaining candidates are hypothesis-only or would need serial
  formalization before any construct can be compared.

At that gate, do not keep formalizing hypothesis-only candidates one by one.
Either run one bounded method-factory sprint or escalate the strategic
shortage. This lane is diagnostic discovery, not a Groundwork Step 4a MVE.
This is a hard routing choice: while the predicate remains true, do not prepare
another candidate-specific formalization task. Record factory routing or the
strategic shortage as the next legal action.

Before generating any factory task, the entry must pass a
**problem-bearing testbed preflight**. A family is not a valid entry merely
because it is untested, because a portfolio axis reads `REOPENED`, or because
the shared testbed once produced a signal elsewhere. Each of the four gates
below must hold, and each must cite `file:line` evidence in the simulator
source; any failure routes to `STRATEGIC_GATE` or `BLOCKED_TESTBED`, not to a
factory task:

1. **Physical degree of freedom exists** — the candidate's lever
   (e.g. update granularity, a tap structure, a cost term) corresponds to a
   realizable transformation the simulator source actually applies. A family
   that presupposes a physical effect the channel source does not model
   (e.g. frequency-selective sub-band processing when the source has no
   dispersion/multipath/FIR) fails this gate.
2. **Baseline's observed failure aligns with the candidate's point of action**
   — the frozen baseline's recorded failure mechanism (its synthesis,
   diagnostic, or adjudication) must name the same lever the candidate would
   move. "The baseline fails somewhere, and this family is untested" is not
   alignment.
3. **A named conventional comparator exists** — before construction, name one
   comparator that has identity (a specific conventional algorithm, not a
   placeholder or privileged method), is task-matched (same blind-equalization
   job), uses the same deployable runtime information (no privileged truth),
   and is independently tunable (its own frozen settings and validation
   budget). "The executor will freeze a comparator later" fails this gate.
4. **Each gate has `file:line` evidence** in the simulator, the baseline
   synthesis, or the authority record.

A testbed that previously produced a signal does not satisfy these gates for a
different family. Inherited `PROBLEM_SURVIVES_CONVENTIONAL_BASELINE` authorizes
a method Scout for the *same* problem slice; it does not waive this preflight.

**Shared anchor vs. identity parity.** The shared system anchor (identical
paired realization, modulation, metric, seed set) must be preserved. Identity
parity — keeping the *inherited baseline's* exact form (e.g. block-end update
granularity) — protects comparison continuity for already-run packages; it is
not a scientific ban on a *different conventional algorithm*. When a candidate
acts on a different (e.g. finer) execution step, choosing that step as the
task-matched conventional comparator is a legal, re-adjudicated comparator
change, not a reopen of a closed axis and not an identity-parity violation.

A method-factory sprint must:

1. reuse one already validated simulator/evaluator, the **current
   authority-approved and adequately tuned** task-matched conventional
   baseline, paired realization, and shared diagnostic seed set; a runnable
   historical anchor is insufficient when a later baseline correction exists;
2. freeze the runtime-visible input and output contract before construction;
3. deduplicate against prior/rejected constructs, then build 3–5 genuinely
   mechanism-distinct minimal constructs in one package;
4. run semantic smoke and a fair comparison in that same package;
5. record at least `CONSTRUCT_CREATED` or `FAIR_COMPARISON_RUN`, unless the
   shared testbed itself fails identity or fairness checks.

For a strict-causal construct, selection, fitting, gating, and normalization
must use only a calibration prefix or past state disjoint from the scored eval
window. Whole-window statistics cannot select or transform that same window.
Persist smoke results in the terminal result artifact; a separately executed
smoke whose receipt is overwritten does not close the package.

The only terminal outputs are:

- `DIAGNOSTIC_METHOD_SIGNAL` — at least one construct shows a stable,
  non-artifactual advantage worth formalizing. This requires that the construct
  stably beats a tuned, task-matched, same-information conventional
  comparator, and that the advantage is not attributable to tuning, a larger
  effective update budget, or a gradient-identity artifact (rule these out by
  ablation before judging signal).
- `NO_DIAGNOSTIC_SIGNAL` — the tested batch has no usable signal under the
  frozen slice;
- `PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR` — the tuned conventional
  comparator already removes the baseline's observed problem (e.g. a
  block-end-update collapse vanishes under a per-symbol update of the same
  canonical algorithm), and no new construct stably beats it. This is **not**
  a method signal and forms **no** active carrier; it is a causal adjudication
  of the suspected lever (the suspected cause was real, but a conventional
  algorithm already resolved it). When this holds, record the resolution and
  do not manufacture a signal with a weaker comparator.
- `BLOCKED_SHARED_TESTBED` — the common evaluator, baseline, or data contract
  cannot support a fair diagnostic comparison.

A sprint whose execution itself violates the contract (identity gate fails,
causality leaks and is not repaired, the comparator uses the wrong gradient
identity, smoke is clobbered and not closed, or the verifier rejects and one
in-package repair still cannot close) is `EXECUTION_INVALID`; it produces no
scientific terminal and no mission delta.

Diagnostic seeds, comparisons, and winners cannot support paper claims,
formal Go/Kill, or promotion. A winner must re-enter Groundwork at Step 1 and
complete Step 1–3/3.5/4a before formal experiment or thesis use. Do not use
this exception to reopen an explicitly rejected axis or to disguise
candidate-specific formalization as a factory sprint.

**Gate-2 evidence grade.** Gate 2 (baseline failure aligns with the candidate's
point of action) only proves the candidate's lever touches the same location
as the baseline's *observed* failure and that the lever is real. It does not
license treating a synthesis's mechanism attribution (e.g. "block-end update
geometry is the structural attractor cause") as a confirmed causal mechanism
when that attribution was rejected by an earlier review. State the suspected
lever as a hypothesis to be tested; the factory sprint is where its causality
is adjudicated, including via the `PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR`
outcome.

**Comparator implementation identity.** A comparator must execute the
canonical update defined by its cited implementation or formula. An
implementation missing a required state- or output-dependent factor is a
different algorithm and cannot impersonate the named comparator; it may only
show that the tested lever is real. Bind the implementation identity and tune
its settings independently on development data.

## Method-signal promotion preflight

After accepting a `METHOD_SIGNAL`, do one bounded promotion preflight before
serial Groundwork work. Reuse existing evidence to check:

- fit with the current thesis problem and a plausible chapter role;
- direct collision and accessible must-read sources;
- a real, task-matched comparator and the strongest cheap alternative;
- frozen estimand, claim ceiling, and evidence-closure budget;
- whether Step 1–3/3.5/4a can close without a chain of receipt-only repairs.

Record one outcome:

- `PROMOTION_WORKLINE_READY` — prepare one bounded formal workline that closes
  the remaining Groundwork gates;
- `HARVEST_ONLY` — preserve the bounded method card or writing asset without
  presenting it as a formal method;
- `STRATEGIC_GATE` — the only plausible promotion needs materially larger
  access, infrastructure, compute, or a thesis-scope decision.

Combine deterministic receipt repair with the scientific package it unlocks.
Run task-control and interface validation before assigning a scientific
checkpoint. A brief that never starts because its interface is invalid is a
setup incident, not an accepted method package and not a no-method increment.

## Separate science from mission progress

After every accepted package record both:

- `formal_science_disposition` — the local scientific or formal verdict.
- `mission_method_delta` — `NONE`, `CONSTRUCT_CREATED`,
  `FAIR_COMPARISON_RUN`, `METHOD_SIGNAL`, `PACKAGING_BOUNDARY`, or
  `PROMOTION_READY`.

A reliable negative, integrity repair, or provenance PASS may advance the
formal disposition while `mission_method_delta` remains `NONE`. Never describe
that combination as method-production progress.

Review mission progress as actual increments to the `main method / engineering
component / supporting portfolio`, not as a package total. Package count
describes exploration coverage only; it is not a success, completion, or
automatic-stop criterion. If the portfolio contains no method-bearing entry,
report a strategic shortage instead of manufacturing another package.

## Three record layers

Long-running RDL topics specialize ordinary session governance:

1. `topic-index.md` is the small current snapshot: original mission, scope,
   current control, latest checkpoint, and next legal action.
2. `mission-log.md` is the fixed long-horizon chain. Append one compact
   checkpoint per accepted package.
3. T, worker-log, artifacts, and commit hold package detail.

Do not use S notes as routine package receipts. Reserve them for substantial
discussion, phase audit, user correction, or a decision that cannot fit one
checkpoint.

Each mission-log checkpoint contains:

- package and evidence pointers;
- intent and mechanism/family;
- `formal_science_disposition`;
- `mission_method_delta`;
- same-axis, repair, and no-method streaks;
- `UNDERWEIGHT`, `ADEQUATE`, or `OVERWEIGHT`;
- `ALIGNED`, `DRIFT_RISK`, or `DRIFTED`;
- the next action and why it beats the best legal READY alternative.

Read the original mission and the complete checkpoint chain before preparing
the next T. Do not read every worker log unless a checkpoint needs audit.

## Drift and work-size review

These conditions trigger explicit reconsideration, not an automatic decision:

- Two same-axis packages with no method delta: compare the best READY
  alternative before continuing.
- Two repair or science-guard packages: a third needs a concrete explanation
  of why repair is more likely to produce a method.
- An `UNDERWEIGHT` package: the next package must close a decision uncertainty,
  run a method slice, or remove a genuine blocker and continue useful work in
  the same package.
- Repeated formal progress with method delta `NONE`: report the mission as
  stalled, not progressing.
- If the mission has no active carrier and a remap gives
  `READY=0 / NEEDS_SMALL_ADAPTER=0`, stop serial formalization. Select the
  pre-formal method factory or strategic escalation before preparing another
  hypothesis-only evidence package.

Classify package weight by decision value, not lines or compute:

- `UNDERWEIGHT` only discovers the next step or updates state.
- `ADEQUATE` closes one useful uncertainty, runs a minimal construct, or
  removes a hard blocker and proceeds.
- `OVERWEIGHT` mixes unrelated decisions until identity or claims cannot be
  reviewed independently.

Never use a fixed package count as a success criterion or automatic rotation
rule.

## Repair, rotation, and ownership

After a rejected scientific verdict, remain on the same axis only when the
defect is bounded and its repair is more likely to produce a method than the
best legal READY alternative. Otherwise preserve the diagnostic asset and
rotate.

The executor must not update formal or current owners. It writes only the
authorized implementation, worker log, artifacts, and commit. The master
accepts or rejects the evidence, updates owners, appends the mission
checkpoint, and then prepares the next task.

## Thesis-facing method card

An accepted `METHOD_SIGNAL` includes:

- technical action and deployable inputs;
- fair comparator and robust evidence;
- mechanism and cheap-alternative checks;
- operating boundary and claim ceiling;
- primary and fallback packaging;
- adaptation, promotion, or harvest pointer.

Negative results and evaluation insights remain useful supporting material,
but they do not become a main method merely because the process was rigorous.
