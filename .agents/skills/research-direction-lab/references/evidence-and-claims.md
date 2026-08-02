# Evidence and claims

Use this reference before running a batch, interpreting results, or changing a claim scope.

## Executable semantic gates before scale

Before scaling seeds or cells, starting Scout or Deep Evidence, or freezing a
`METHOD_SIGNAL`, select every applicable gate below and execute a falsifying
test. A source citation or checklist answer does not substitute for observed
behavior.

- `parameter_injection` — perturb the contracted parameter with a sentinel or
  two-value test and trace it to the callee that creates the physical or task
  realization. A label, serialized field, or matching argument name is not
  evidence of injection.
- `hidden_truth_metamorphic` — hold deployable observations fixed, change only
  hidden-truth metadata, and require the deployable action and output to remain
  unchanged. Traverse the complete caller-to-callee graph recursively.
- `state_lifecycle` — trace initialization, reset, generator calls, and the
  intended continuity span. Confirm continuity with a state trace or an
  appropriate dependence diagnostic; independent samples do not establish a
  trajectory.
- `metric_information` — expose the metric population, numerator, denominator,
  exclusion point, and aggregation. Privileged truth may enter only an allowed
  training location or final scoring boundary. A truth-resolved metric cannot
  be presented as a deployable fixed-label metric.
- `real_action_and_cost` — show that the action changes real state, output, or
  caller path, and derive cost from the actual call trace. Execute routing,
  stopping, or savings in the measured path rather than simulating it after a
  full run; a reported counter is not a caller trace. For a scale or
  normalization action, repeat scoring with invariant downstream evaluation
  and decompose system change from evaluator sensitivity; a changed tensor
  alone does not establish a method action.

For each selected gate, record exactly:

`applicability | executable test | observed result | artifact pointer | PASS/FAIL/N/A reason`

All applicable gates must PASS before work may scale seeds or cells, freeze a
METHOD_SIGNAL, or enter promotion. A FAIL keeps the claim diagnostic or invalid
until the executable path is repaired; statistics cannot repair a semantic
FAIL.

Use the same contract to test objective/output/metric alignment, whether a
constant or trivial solution can ignore the input, whether a no-op or identity
reproduces the unchanged system, output support and action diversity,
learnability on a tiny sample, the simplest legal comparator, and
legal-information boundaries. Project code owns formulas, thresholds, and
domain-specific variants.

When provenance risk warrants a receipt, use the small execution-receipt
schema: `contract_hashes`, `source_hashes`, `test_started`, `seed_ledger`,
`pre_test_state`, and `post_test_state`. Build and validate it with
`scripts/validate_receipt.py`; any contract or source hash mismatch fails
closed. This receipt protects chronology and identity, not scientific quality.

## Protect evidence integrity

Before execution, bind the formal goal and batch question to:

- baseline and component identity;
- source closure and artifact provenance;
- information available during training, operation, evaluation, and oracle analysis;
- metric definition, units, aggregation, and uncertainty method;
- comparator legality and configuration parity;
- comparator adequacy for the exact contribution claim, including task fit and convergence;
- protected history and preregistered exits.

Treat deterministic integrity failures as binding. Repair them within the scientific contract or mark evidence untrusted, stale, unknown, or invalid. Integrity PASS proves artifact fidelity, not scientific-semantic validity.

## Separate facts from interpretation

Record execution facts and verifier findings before scientific synthesis. Then test at least these explanations:

- the intended mechanism caused the diagnostic and primary-metric changes;
- extra information, an easier contract, or an illegal comparator created the difference;
- a bug fix repaired the baseline rather than adding a research contribution;
- sampling variation, selection, or metric aggregation explains the signal;
- the result applies only to the executed cell or slice.

A result against a buggy, invalid, task-mismatched, or materially under-converged baseline is diagnostic. Revalidate using `baseline-adjudication.md`; only `PROBLEM_SURVIVES_CONVENTIONAL_BASELINE` permits a method Scout, and it remains scoped evidence rather than a method win.

## Set the claim ceiling

Use the smallest level supported by evidence:

`RUN | CELL | SLICE | CONTRACT | CANDIDATE | FAMILY | DOMAIN`

State what was tested, what was not tested, which axes are blocked, which counterexamples remain, and what evidence would justify widening the claim. Never turn a blocked axis into negative evidence or a local signal into domain closure.

Invoke the project's deeper evidence workflow when preparing novelty, contribution, broad negative, formal parameter, competitor, or large-sample claims. Reuse existing evidence and fill only the missing links.
