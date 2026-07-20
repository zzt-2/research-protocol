# Architecture: Research Direction Lab

> Status: REAL (documented after V005 PASS, Task 10 cutover, D008)
> Mode: doc-steward architecture mode — every entity/relationship anchored to real files
> Single process owner: `.agents/skills/research-direction-lab/SKILL.md`

## Purpose

Sustain open-ended research-direction exploration across batches, context recovery, local blockers, evidence scopes, and thesis-material accumulation — without turning it into a fixed scheduler.

The Skill (`research-direction-lab`) is the single process owner for long-running exploration: recover intent and state, organize an open candidate portfolio, plan informative batches, interpret bounded evidence, harvest reusable thesis material, and keep work moving until a strategic decision is genuinely required.

## Top-level responsibilities (one owner per fact)

| Responsibility | Owner (real path) | Role |
|----------------|-------------------|------|
| Open-ended research process | `.agents/skills/research-direction-lab/SKILL.md` | 7-phase loop, candidate portfolio, batch/atlas, evidence/claims, harvest, recovery/rotation, project-layout (7 references) |
| Deterministic integrity tools | `.agents/skills/research-direction-lab/scripts/` | `hash_bundle.py`, `validate_receipt.py`, `append_event.py`, `rebuild_state.py`, `render_status.py` — guards only, no scheduler logic |
| Communications domain profile | `.agents/skills/research-direction-lab/references/profiles/communications.md` | Information-access levels, metrics/units, comparator legality, claim boundaries, thesis forms |
| Project adapter (current facts) | `projects/{name}/direction-lab/project.v1.yaml` (e.g., `projects/thesis-fso/direction-lab/project.v1.yaml`) | Anchor, components, paths, runnable/blocked axes, budgets, protected history digests |
| One-page status (daily human entry) | `projects/{name}/direction-lab/STATUS.v1.md` | Renderer output of 8 questions; single source via `render_status.py` |
| Compact state projection | `projects/{name}/direction-lab/state/projections/*.yaml` | Deterministic projection from `events.jsonl` |
| Append-only execution events | `projects/{name}/direction-lab/state/completion-events.jsonl` | Hash-chained execution/disposition facts |
| Active portfolio | `projects/{name}/direction-lab/portfolio/current.v1.yaml` | Candidate cards, batch history, blocked axes, recorded next action |
| Thesis harvest ledger | `projects/{name}/direction-lab/harvest/ledger.v1.yaml` | H### entries with evidence scope, claim ceiling, source hashes |
| Thesis spines | `projects/{name}/direction-lab/harvest/thesis-spines.v1.md` | Evidence-backed writing routes; promotion requires multiple converging harvests |
| Frozen batch artifacts | `projects/{name}/direction-lab/batches/B###-slug/` | Immutable manifest, artifacts, receipt, verifier-report, batch-synthesis |
| Adapter schema | `.agents/skills/research-direction-lab/references/project-adapter-schema.yaml` | Closed v1 shape consumed by adapter instances |
| Governance (sessions) | `.sessions/2026-07-20-research-direction-lab-system/` | Blueprint, plan, decisions D001-D008, verifications V001-V005 |

## Process boundary

- **Direction Lab** = pre-promotion candidate discovery and batch screening layer.
- **Groundwork → Contract → Execute** (see `stages/groundwork.md`, `stages/contract.md`, `stages/execute.md`) = formal scientific evidence layer.
- A promoted candidate **must** still pass Groundwork/Contract/Execute (FR-22 unchanged).
- Scout/Sandbox numbers **do not** auto-enter thesis or canonical baseline.

## What this architecture does NOT encode (by design)

These were explicitly removed in D001 — they re-grow complexity:

- `science_slots`, fixed minimum batch counts, `completeness_solver`
- `resource_match` / candidate-resource matching as a closed constraint
- A controller/state machine that owns stop-legality or candidate selection
- Project-specific semantics in generic Skill or scripts (BER/SNR/CMA/pilot/OSL/QPSK/Jones belong only in `references/profiles/communications.md` and test fixtures)
- A scheduler/if-then decision tree replacing scientific judgment

Verified by `test_no_scheduler_contract.py` (8 tests, all PASS as of V005).

## Verification evidence (V001-V005)

| Task | Verifier | Verdict | Date |
|------|----------|---------|------|
| Task 1-3 Skill+Profile+Adapter | V001 | PASS | 2026-07-20 |
| Task 4-5 safety tools + historical replay | V002 | PASS | 2026-07-20 |
| Task 6-7 read-only projection + scheduler audit | V003 | PASS | 2026-07-20 |
| Task 8 fresh-agent blind forward tests (5 cases) | V004 | PASS | 2026-07-20 |
| Task 9 live shadow (5 behaviors, foundation cert) | V005 | PASS | 2026-07-20 |

Independent verifier commands are reproducible from each V### entry in `.sessions/2026-07-20-research-direction-lab-system/verifications.md`.

## Relationship to superseded artifacts

| Artifact | Status | Note |
|----------|--------|------|
| `C:/Users/zzt/.agents/skills/method-family-batch-exploration/SKILL.md` | SUPERSEDED 2026-07-20 (D008/V005) | Retained verbatim; new work uses `research-direction-lab` |
| `projects/thesis-fso/direction-lab/process.md` (DL-Process v0.4) | SUPERSEDED 2026-07-20 (D008/V005) | Retained as project-instance history; new work loads `research-direction-lab` Skill first |
| Governance pilot `2026-07-17-direction-lab-governance-pilot` | dormant | controller/scheduler lessons absorbed into D001 |
| Old scheduler code (campaign/controller/science_slots) | audited, not deleted | 23 functions + 1 property + 4 CLI audited; all scheduler semantics marked not-KEEP |

## Known non-blocking debt (post-V005)

- `canonical-state.yaml` internal stale self-checksums (`event_log_sha256`, `simulator.sha256`) — protected digests are correct; internal self-checksums are stale. Cleanup at formal activation.
- `canonical-state.last_completed_batch` pointer still B002 at B003 verify time — self-documented in B003 verifier-report.
- Windows symlink dynamic test skip (V002/V003 debt) — POSIX `flock` and Windows symlink branches need dynamic coverage before cross-platform CI.
- Forward-test scorer B6/B1 fallback legality limited to forbidden_action wordlist (V004 debt) — detector limitation, not a defect.

## Change log

- 2026-07-20: created (D008/V005, Task 10 cutover). Architecture is real, not target design.
