# Project layout and artifact ownership

Use this reference when creating or locating direction-lab artifacts. Adapt names to the host project while preserving one owner per fact.

```text
direction-lab/
├── STATUS.md
├── project.yaml
├── state/
│   ├── events.jsonl
│   └── current.yaml
├── portfolio/
│   ├── candidates.yaml
│   └── batches.yaml
├── batches/
│   └── <batch-id>/
│       ├── manifest.yaml
│       ├── artifacts/
│       ├── receipt.json
│       ├── verifier.md
│       └── synthesis.md
├── harvest/
│   ├── ledger.yaml
│   └── thesis-spines.md
├── registries/
│   ├── components.yaml
│   └── failures.yaml
├── tools/
├── tests/
└── archive/
```

## Ownership

- `project.yaml`: current project facts, anchor, paths, commands, axes, budgets, and protected history.
- `events.jsonl`: append-only execution and disposition facts.
- `current.yaml`: deterministic projection rebuilt from events.
- `candidates.yaml` and `batches.yaml`: active scientific portfolio and planned comparisons.
- batch directory: immutable contract, raw artifacts, receipt, verification, and bounded synthesis.
- `ledger.yaml`: harvest pointers, hashes, scope, and status; never raw result duplication.
- `thesis-spines.md`: a small set of evidence-backed writing routes.
- registries: component identities and known failures.
- `STATUS.md`: the only routine human entry point.

## Profile and adapter routing

Load `profiles/communications.md` when a communications decision depends on
domain-stable conventions. Validate the project adapter against
`project-adapter-schema.yaml` before consuming current project facts; the
schema defines shape, while the adapter supplies values.

## One-page status

Answer:

1. What is the formal goal and current authorization?
2. What is the anchor or baseline?
3. What is the current portfolio and which axes are blocked?
4. What did the latest completed batch establish scientifically?
5. Is work planning, preparing, running, synthesizing, blocked, or awaiting strategy?
6. What thesis material has been harvested?
7. What is the next automatic action?
8. What condition would require user strategy?

Keep routine recovery compact. Load detailed batch history only when a current decision needs it. Archive superseded portfolio versions, avoid per-cell prose files, keep raw data in artifacts, and keep process instructions in the Skill rather than project state.
