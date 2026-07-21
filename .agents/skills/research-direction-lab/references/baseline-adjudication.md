# Baseline adjudication

Use this reference when an anomaly, headroom probe, or candidate appears valuable only relative to an existing baseline.

## Adequacy, not prestige

A Go comparator need not be current SOTA. It must be:

- correctly identified and implemented;
- appropriate to the task, condition, information, and output;
- widely used or otherwise conventional in the relevant research community, supported by a canonical source plus independent representative uses;
- fairly configured for information, tuning, convergence, compute, data, and evaluation; and
- strong enough for the exact limited contribution claim.

Do not chase every recent method. Require current SOTA only when the proposed claim, venue convention, advisor requirement, or reviewer demand explicitly depends on it.

## Minimal baseline ladder

1. Keep the no-change or current chain as a diagnostic anchor.
2. Select one defensible, task-appropriate, widely used conventional baseline as the main Go comparator.
3. Add one obvious low-cost conventional extension only when it is known to address the observed failure directly.
4. Keep oracle or privileged-information methods as bounds and Kill tools, never Go comparators.

Stop expanding the ladder when the exact claim has a fair conventional comparator and the obvious cheap alternative explanation has been tested. More baselines may improve a later paper, but they are not a prerequisite for every Scout.

## Shared anchor and claim-specific fairness

Keep a **shared system anchor** for end-to-end comparison, but do not force candidates with different outputs to use one identical comparator list. Each detection, estimation, correction, or control claim also needs a **task-specific comparator** that performs the same job with the same legal information. The shared system anchor does not replace a detector baseline, a fixed control policy, or a conventional correction method.

Fairness means **equal tuning opportunity**, not identical hyperparameters. Give compared methods comparable search budget and validation evidence, freeze their selected settings before held-out evaluation, and check convergence using behavior appropriate to each method. Use paired data, seeds, metrics, and evaluation windows where the claim permits them to be shared.

Reuse a baseline record while task, information, output, condition, and claim remain unchanged. Re-adjudicate the affected layer when any of those change. If task fit, tuning, convergence, or information parity remains materially unresolved, keep the result diagnostic and state the limit.

## Adjudication state

An anomaly remains `DIAGNOSTIC` until identity, task fit, convergence, information parity, and the obvious conventional fix have been checked. If the problem remains materially visible, record:

`PROBLEM_SURVIVES_CONVENTIONAL_BASELINE`

Only this state authorizes an ML or new-method Scout for that problem slice. It does not itself prove that ML will win or widen the claim beyond the executed scope.

## Keep the portfolio moving

Baseline adjudication is one shared batch, not a new single-candidate full process. While it runs, prepare other mechanism-distinct candidates that reuse the same anchor or contract. Do not block the entire portfolio on an exhaustive comparator survey.

Record a baseline choice as:

`claim | shared system anchor | task-specific comparator | canonical source | representative uses | task fit | information parity | tuning opportunity | convergence | obvious extension considered | stop reason | unresolved limits`
