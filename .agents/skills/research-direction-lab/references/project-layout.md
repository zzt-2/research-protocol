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
│   ├── current.yaml
│   └── history/
├── probes/
│   └── <probe-id>/
│       ├── record.yaml
│       └── artifacts/          # optional
├── batches/
│   └── <batch-id>/
│       ├── manifest.yaml
│       ├── artifacts/
│       ├── receipt.json          # conditional for Scout; required for Deep Evidence
│       ├── verifier.md           # conditional for Scout; required for Deep Evidence
│       └── synthesis.md
├── harvest/
│   ├── ledger.jsonl
│   ├── current.yaml
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
- `events.jsonl`: append-only execution and explicit disposition facts.
- `current.yaml`: sole machine current view, deterministically rebuilt from events.
- `portfolio/current.yaml`: active scientific portfolio; superseded versions move to `history/`.
- `probes/<probe-id>/record.yaml`: one compact Probe record. A Probe does not require a receipt, verifier, synthesis, or harvest item by default.
- batch directory: immutable contract, raw artifacts, bounded synthesis, plus conditional Scout or required Deep-Evidence integrity files.
- `ledger.jsonl`: append-only harvest lineage; never raw result duplication.
- `harvest/current.yaml`: current thesis-consumption view after explicit amendment, supersession, retraction, invalidation, or restoration.
- `thesis-spines.md`: a small set of evidence-backed writing routes.
- registries: component identities and known failures.
- `STATUS.md`: the only routine human entry point; it reads current projections, never raw history as current fact.

Scout receipt and verifier are conditional on actual provenance, execution, history, or claim risk; they are not folder-completeness requirements. Deep Evidence requires the full chain. A missing optional Scout file is not a governance failure when the batch record states why it was unnecessary.

When an adapter declares `paths.harvest_current`, the status CLI must be called with that exact `--harvest-current` path; a raw ledger is rejected as display input. Inactive `superseded`, `retracted`, and `invalidated` entries stay in lineage but are filtered from the current status view. Legacy adapters may keep the old input until their bounded current-view migration.

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

Keep routine recovery compact. The hot path is `STATUS.md`, `project.yaml`, `state/current.yaml`, `portfolio/current.yaml`, and `harvest/current.yaml`. Load detailed history only when a current decision or conflict needs it. Archive superseded portfolio versions, avoid per-cell prose files, keep raw data in artifacts, and keep process instructions in the Skill rather than project state. Session notes hold user voice, strategic decisions, major failures, and handoffs—not every Probe run.
