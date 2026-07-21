# Thesis harvest

Use this reference to assess durable value after a Probe or scientific batch. Assessment is mandatory; creating an item is not.

## Harvest categories

- `METHOD_SIGNAL` — a mechanism worth further development.
- `BOUNDARY_RESULT` — where a baseline or candidate works or fails.
- `LOCAL_NEGATIVE` — a scoped, evidence-backed negative.
- `FAILURE_MECHANISM` — a causal explanation of failure.
- `EVALUATION_INSIGHT` — a finding about metrics, comparators, scope, statistics, or oracle use.
- `BASELINE_ADJUDICATION` — why a conventional comparator was adequate, inadequate, or sufficient to stop further baseline expansion for a bounded claim.
- `REUSABLE_ASSET` — a runner, adapter, dataset, comparator, test, or analysis utility.
- `INFRASTRUCTURE_GAP` — a shared capability that blocks multiple valuable comparisons.
- `WRITING_MATERIAL` — evidence usable in motivation, methods, experiments, discussion, limitations, or future work.

## Ledger entry

Record:

`id | category | concise finding | evidence scope | claim ceiling | artifact pointers | source hashes | related candidates/batches | thesis destination | confidence | follow-up | status`

Keep raw data in artifacts and store pointers, hashes, and bounded summaries in the append-only ledger. Preserve negative and invalidated items with their reasons; do not erase lineage. Project `harvest/current.yaml` from explicit statuses such as `active`, `diagnostic`, `amended`, `superseded`, `retracted`, and `invalidated`; only the current view feeds thesis writing.

If no durable value exists, record `no_durable_harvest_reason` in the Probe or batch record instead of manufacturing a ledger item. A scientific interpretation, its raw numeric fact, and its reusable asset may receive different dispositions after review. Do not count an old claim and its corrective amendment as two independent contributions.

## Promote thesis spines

Create or update a candidate thesis spine only when multiple harvest items support a coherent problem, method, evidence plan, comparison story, and limitation boundary. Prefer a portfolio that can yield one main method contribution, one mechanism or boundary analysis, and one system/evaluation extension under a shared story. Keep competing spines visible until a strategic choice is needed.

Governance activity is not a scientific harvest by itself. Infrastructure becomes a harvest only when it is reusable, unlocks evidence, or teaches a bounded methodological lesson.
