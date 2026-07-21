# Candidate portfolio

Use this reference when creating, expanding, consolidating, or ranking research candidates.

## Map an open portfolio

Expand around the anchor along independent lenses appropriate to the domain:

- processing point or intervention location;
- information available at decision time, with evaluation-only information marked separately;
- output or action type;
- mechanism family;
- operating-condition and evaluation axes.

Populate the map from four complementary sources:

- reviews, strong papers, open problems, and citation neighborhoods;
- verified failures or boundary behavior of existing baselines, after bug and comparator checks;
- intervention points across the full system or processing chain; and
- transferable mechanisms from adjacent mature systems.

Normalize a problem candidate as `method M is inadequate under condition C because mechanism A`, then state the legal information, output or action, metric, and conventional comparator. Also inspect existing assets, historical counterexamples, missing comparators, and shared capabilities. Record uncovered angles without claiming the map is complete.

## Candidate card

Record only decision-useful fields:

`id | M-C-A problem | question | source | lineage | mechanism | information access | output | supported scope | blocked scope | baseline | comparator | diagnostics | dependencies | cost | thesis form | evidence pointers | claim ceiling | status`

Keep scientific vocabulary in domain profiles or project adapter values. Keep the generic card structure domain-neutral.

## Bounded portfolio refresh

Before heavy implementation, run a **Bounded portfolio refresh** when the active map is narrowly clustered around one mechanism, contains only a few inherited ideas, or marks readiness from shared data rather than executable interfaces. Expand at the **mechanism-level**, not by multiplying model names or hyperparameter variants. Reuse prior reviews, failure registries, system intervention points, adjacent mechanisms, assets, and blocked counterexamples; perform targeted candidate-specific literature work only where it can change ranking or comparator choice.

Classify readiness from evidence:

- `READY`: implementation, legal input/output contract, comparator, evaluator, and runnable entry exist;
- `NEEDS_SMALL_ADAPTER`: the mechanism and shared assets exist, with one bounded interface or adapter missing;
- `INFRASTRUCTURE_BLOCKED`: a real state, action, data, evaluator, or source-closure capability is absent;
- `HYPOTHESIS_ONLY`: the mechanism is plausible but lacks candidate-specific evidence or an implementation path.

The refresh is a short map-building step, not an exhaustive survey or an obligation to implement the whole map. After it exposes mechanism-distinct alternatives, select a small comparable `READY` batch and start. Keep the remaining map open for rotation.

## Consolidate and rank with judgment

- Merge micro-variants that answer the same question through a shared interface; retain variant identity inside the family.
- Split candidates when they use materially different information, outputs, comparators, failure hypotheses, or claim scopes.
- Rank by expected information value, thesis relevance, baseline legality, diversity from current evidence, dependency leverage, reversibility, and cost.
- Treat claimed readiness as an auditable fact; shared inputs or reusable code alone do not make a candidate runnable.
- Prefer a portfolio that can distinguish mechanisms over many near-duplicate variants.
- Preserve lineage when deferring, merging, reviving, or invalidating a candidate.

Do not use fixed family quotas, resource-slot matching, or a completeness proof. A portfolio is a living map that supports the next informative comparison.
