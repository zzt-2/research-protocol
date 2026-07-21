# Evidence and claims

Use this reference before running a batch, interpreting results, or changing a claim scope.

## Semantic smoke before scale

Before cells × seeds, tuning, or a full evidence chain, try to falsify the task itself. Select applicable checks and record `PASS`, `FAIL`, or justified `N/A`:

- objective, label, output, and final metric describe the same task;
- a constant or trivial solution cannot satisfy the objective while ignoring input;
- a no-op or identity configuration reproduces the unchanged system;
- output variance, output support, occupancy, or action diversity is non-degenerate;
- a tiny sample can be overfit when the mechanism is learnable;
- the simplest legal comparator can be reproduced;
- causal prefix and legal-information boundaries hold.

Project code owns formulas, thresholds, and domain-specific variants. If a cheaper implementation or task-semantic explanation survives, mark the run implementation-confounded and the candidate unresolved. More seeds, models, hyperparameters, hashes, or independent reruns do not repair semantic failure.

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
