# Batch portfolios and scope atlas

Use this reference to plan comparable work and decide whether local evidence warrants scope expansion.

## Batch card

Define:

`question | candidates | shared baseline | domain slice | legal comparator | diagnostics | cost | dependencies | preregistered exit | claim ceiling`

Include a no-change baseline, one defensible widely used task-appropriate conventional comparator, one obvious low-cost extension when it directly addresses the diagnosed failure, a small set of mechanism-distinct candidates sharing the contract, and only the ablations needed to distinguish the stated hypotheses. Current SOTA is not a default prerequisite. Choose size from information value and cost; do not enforce a global count.

Before a gap becomes method-worthy, apply `baseline-adjudication.md`. Keep the result diagnostic until `PROBLEM_SURVIVES_CONVENTIONAL_BASELINE` is supported. Baseline checks and preparation of other reusable candidates may proceed in the same portfolio cycle.

## Shared preparation sprint

Combine setup tasks when they establish one shared baseline, adapter, evaluator, source closure, or smoke check. A sprint is complete when the batch can run safely or when evidence shows the shared dependency is not worth building. Do not stop for user approval after each interface task.

Keep setup bounded. If work serves only one deferred candidate or repeatedly fails to unlock scientific comparisons, return to the portfolio instead of extending a generic controller.

## Scope assessment

After a local positive, local negative, or near-ceiling baseline, record:

- executed conditions and uncertainty;
- runnable but uncovered conditions;
- infrastructure-blocked conditions;
- relevant historical positive and negative counterexamples;
- current claim ceiling;
- most informative next axis.

Treat blocked conditions as unresolved, not failed. If an important counterexample lies in blocked scope, keep any broader candidate or family conclusion open.

## Atlas expansion

1. Use a small representative covering set across supported axes to locate possible headroom or failure regions.
2. Expand seeds, resolution, training, or additional axes only where the first stage shows mechanism-relevant structure or where a broader claim needs evidence.

The atlas maps evidence boundaries. It does not certify portfolio completeness or impose a universal stopping count.
