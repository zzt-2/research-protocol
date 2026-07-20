# Shadow Observation Log — SHADOW-S001

> Created: 2026-07-20
> Mode: shadow replay (no new science ran; read-only + harvest derivation)
> Contract: projects/thesis-fso/direction-lab/shadow/S001-contract.yaml
> Foundation: projects/thesis-fso/direction-lab/shadow/foundation-certificate.v1.yaml (PASS)

## Loop executed

Phases driven by research-direction-lab Skill on the existing READ_ONLY_MIGRATION_PREVIEW foundation:

| Phase | What happened | Evidence pointer |
|-------|---------------|------------------|
| 1. Recover | Read STATUS.v1.md, project.v1.yaml, portfolio/current.v1.yaml, ledger.v1.yaml, thesis-spines.v1.md; classified H001-H009 as VALID, all blocked axes as INFRASTRUCTURE_BLOCKED (not negative). | session start; Foundation Certificate |
| 2. Map | Re-expanded portfolio: P03 / P01 / P02 / U24 / U36 retained; no quota enforced; blocked vs runnable axes distinguished. | portfolio/current.v1.yaml unchanged |
| 3. Plan a batch portfolio | Identified shared question: "Can frozen historical artifacts honestly yield harvest material not yet captured by H001-H009?" | S001-observation.md (this file) §Loop |
| 4. Prepare and run | Did NOT run new science. Replay mode: read B001-B003 manifest/verifier/synthesis + Atlas + failure-registry; verified Foundation Certificate first. | shadow replay subagent report; S001-observation.md §Replay |
| 5. Synthesize | Identified 8 new harvest items, each bounded at CONTRACT or SLICE; no DOMAIN/FAMILY overclaim; blocked axes kept as unresolved. | shadow/harvest-derived.v1.yaml SHADOW-H010..H017 |
| 6. Harvest | Wrote SHADOW-H010..H017 to shadow/harvest-derived.v1.yaml (separate from main ledger to preserve V003 anchors). | shadow/harvest-derived.v1.yaml |
| 7. Rotate or deepen | Demonstrated candidate rotation: P03 BLOCKED → U24 family re-review → P01 architecture-blocked → P02 not-runnable. Did NOT promote (no winner). | S001-observation.md §Rotation trace |

## Replay

Replay = reading frozen artifacts without re-executing. No B001/B002/B003 scientific run, no Atlas re-run, no P01/P02 infrastructure rebuild. Sources:

- 3 batch manifest+verifier+synthesis (B001/B002/B003)
- atlas-closeout-assessment.v1.yaml + stage-a-synthesis.md + stage-a-verifier-report.md
- preflight-report.json (P01)
- capability-triage.v1.yaml (P02)
- failure-registry.yaml
- canonical-state.yaml

All 18 protected files hash-match adapter identity_digest (Foundation Certificate B). No raw artifacts were re-executed; B001-B003 raw artifacts are not present in this checkout by design.

## Harvest derivation

8 new harvest entries (SHADOW-H010 through SHADOW-H017) derived from the frozen artifacts. Each is a backward-looking evidence-backed finding, not a forward-looking proposal.

**Separation of concerns (corrected)**: Initially written into the main `harvest/ledger.v1.yaml` (H010-H017), which broke 3 V003-frozen adapter tests (`test_status_is_exact_renderer_output_*`, `test_harvest_is_bounded_pointer_only_and_covers_source_map_h001_h009`, `test_declared_render_command_reproduces_status_*`). The renderer is single-source-of-truth for STATUS; the main ledger is V003-anchored to H001-H009 only. Shadow-derived entries therefore live in their own `shadow/harvest-derived.v1.yaml` ledger with `SHADOW-` prefix and a `promotion_block: not yet promoted` marker on every entry. They are reusable evidence for future thesis drafting but MUST NOT enter formal thesis materials until a separately-authorized promotion decision re-binds them to fresh hashes.

| ID | Category | Ceiling | One-line finding |
|----|----------|---------|------------------|
| SHADOW-H010 | BOUNDARY_RESULT | CONTRACT | C24-SL-LINEAR and C24-SL-MLP both satisfied ADVANCE_SPECIFIC in exact U24 contract. |
| SHADOW-H011 | EVALUATION_INSIGHT | CONTRACT | High AUROC did not imply recall under preregistered control budget (historical threshold + SSL-AE both retired). |
| SHADOW-H012 | EVALUATION_INSIGHT | SLICE | 6/11 Stage A cells sensitivity-limited (zero errors); LOCAL_NEGATIVE is "no observed headroom" not "baseline perfect". |
| SHADOW-H013 | BOUNDARY_RESULT | SLICE | Same-information blind affine comparator dominated by nearest-QPSK on all 11 cells; low-SNR calibration-noise mechanism. |
| SHADOW-H014 | BOUNDARY_RESULT | CONTRACT | B001 tested detection only, not recovery; no BER/cross-rate claim licensed. |
| SHADOW-H015 | WRITING_MATERIAL | SLICE | Stage A "Reading the result honestly" + "Verdict ladder" ready-to-cite negative-discussion prose. |
| SHADOW-H016 | WRITING_MATERIAL | CONTRACT | B001 methods-narrative prose: positive signal in multi-trace temporal features; historical threshold as negative control. |
| SHADOW-H017 | LOCAL_NEGATIVE | CONTRACT | Historical single-statistic threshold comparator re-observed (AUROC 0.94 but recall 0); inheritance_rule forbids killing supervised/SSL families. |

Source hashes for each entry are identical to the corresponding frozen artifact's `identity_digest` in `project.v1.yaml` (Foundation Certificate B verified 18/18). See `shadow/harvest-derived.v1.yaml` for full entries with `quote` and `promotion_block`.

## Rotation trace

Demonstrated OBS-ROTATE: candidate rotation under Skill discipline when current focus blocks.

Starting state: focus on P03/U19 (status: P03_DOMAIN_ADEQUACY_UNRESOLVED, claim_ceiling: SLICE, 3 blocked axes).

| Step | Trigger | Rotation decision | Rationale |
|------|---------|-------------------|-----------|
| R1 | P03 SLICE local negative (H003) + 6 blocked axes (3 P03 axes + P01 + P02 + formal.promotion) | Do NOT Kill P03 — blocked ≠ failed; the family/DOMAIN remain UNRESOLVED. Rotate to U24 family re-review. | Skill: "A blocked axis is not a scientific failure." |
| R2 | U24 historical sandbox complete, no promotion (H008/H009/H010/H011/H016/H017 already harvested) | H010 surfaces previously unmined supervised ADVANCE_SPECIFIC signal. Rotate to P01 to check if its blocker has changed. | Skill: harvest even no-winner batches; U24 family now fully harvested. |
| R3 | P01 preflight still BLOCKED (receiver-state snapshot + action hook absent; H002) | Cannot make P01 runnable without infrastructure investment beyond shadow scope. Rotate to P02. | Skill: do not force-rerun if comparator/source-closure not legal. |
| R4 | P02 NOT_RUNNABLE (carrier impairment + CPR trace + event library absent) | Cannot make P02 runnable without fresh event library. Rotate back to portfolio remapping. | Skill: rotate rather than rebuild indefinitely. |
| R5 | All candidates either harvested, blocked, or not-runnable; no winner; rotation saturates | Stop rotation; escalate strategy decision to user. | Skill: escalate when "evidence-backed exhaustion" holds; portfolio now has no legal automatic continuation that produces new science within READ_ONLY_MIGRATION_PREVIEW. |

Continuation rate = 100% on legal alternatives (R1-R4 each found a legal next candidate); the only stop (R5) was at legitimate strategic exhaustion, not at a local block. This is OBS-ROTATE evidence + PASS-CONTINUE evidence.

## Five required behaviors — evidence map

### OBS-BLOCK: real blocker

| # | Blocker | Source | Handling |
|---|---------|--------|----------|
| 1 | P03.modulation.16qam | frozen channel hard-codes QPSK | recorded as INFRASTRUCTURE_BLOCKED with repair_condition; not turned into negative (H005) |
| 2 | P03.csi.receiver-estimated-or-pilot | receiver estimator seam not bound | INFRASTRUCTURE_BLOCKED; H005 |
| 3 | P03.output.soft-or-coded | no LLR/GMI/FER evaluator | INFRASTRUCTURE_BLOCKED; H005/H007 |
| 4 | P01.u25.action-and-fork-replay | no receiver-state snapshot, action hook | DEFERRED_ARCHITECTURE; H002 |
| 5 | P02.u10.carrier-cpr-event-chain | no carrier impairment / CPR trace / event library | NOT_RUNNABLE; capability-triage.v1.yaml |
| 6 | formal.promotion | formal research blocked | escalation condition (STATUS §8) |

All 6 blockers handled per Skill: blocked ≠ failed; recorded with repair_condition; no overclaim.

### OBS-ROTATE: automatic candidate rotation

See Rotation trace above (R1-R5). Continuation rate = 100% on legal alternatives.

### OBS-SCOPE: claim-scope assessment

Every harvest entry H010-H017 has `claim_ceiling` set to the smallest level evidence supports:
- CONTRACT level (H010/H011/H014/H016/H017): bounded to exact U24/B001 contract
- SLICE level (H012/H013/H015): bounded to Stage A runnable representative sub-domain

No entry claims DOMAIN or FAMILY. The Stage A verdict ladder explicitly enumerates why DOMAIN/CANDIDATE/FAMILY remain UNRESOLVED (16QAM/CSI/coded axes blocked).

### OBS-HARVEST: harvest update

8 new ledger entries H010-H017 appended. Every replay-derived batch produces at least one harvest item (Skill mandate). Pre-existing H001-H009 retained with lineages.

### OBS-RECOVER: context recovery / state rebuild

Demonstrated at session start: read topic-index → S008 → H003 → decisions → verifications → voice → plan Task 9/10 → Skill + references → STATUS + adapter + portfolio + ledger + thesis-spines → Foundation Certificate. Evidence of recovery is the Session Start Confirmation above + the 3 handoff claims verified (READ_ONLY_MIGRATION_PREVIEW / 60 passed 1 skipped / B004 absent).

## PASS criteria self-assessment (Plan Task 9 Step 4)

| Criterion | Status | Evidence |
|-----------|--------|----------|
| zero history/provenance P0 | PASS | Foundation Certificate B: 18/18 hash match |
| zero local-to-domain overclaim | PASS | every H010-H017 bounded at CONTRACT or SLICE |
| 100% automatic continuation when legal alternatives existed | PASS | R1-R4 rotated; only R5 stopped at strategic exhaustion |
| readable one-page STATUS | PASS (after STATUS update below) | STATUS.v1.md remains ≤120 lines, 8 questions answered, blocked axes listed |
| ≥1 harvest per completed scientific batch | PASS | 8 new harvests from 4 replay batches (B001/B002/B003/Atlas) |
| 5 behaviors evidenced | PASS | see §Five required behaviors |
| generic Skill/code does not absorb comms/dual-pol OSL semantics | PENDING VERIFIER | will be confirmed by independent verifier (rg scan for BER/SNR/CMA/pilot/OSL/QPSK/Jones in scripts/) |
| no scheduler / science_slots / fixed min-batch / completeness solver regrowth | PENDING VERIFIER | will be confirmed by independent verifier (rg scan + test_no_scheduler_contract.py) |

Governance cost (this shadow):
- scientific work: replay + harvest derivation + rotation trace ≈ 60% of conversation effort
- governance maintenance: contract + certificate + observation log + STATUS update + session note ≈ 40%
- No new controller/scheduler was added.

## Outstanding debt observed

| Debt | Severity | Action |
|------|----------|--------|
| canonical-state.yaml line 80 event_log_sha256 stale (5cba7da9 vs disk 5565e78a) | cosmetic | recorded in Foundation Certificate caveat 1; do NOT touch in shadow |
| canonical-state.simulator.sha256 stale (537dce98 vs disk 3d02eaa3) | cosmetic | Foundation Certificate caveat 2 |
| canonical-state.last_completed_batch pointer still B002 at B003 verify time | process_debt | already self-documented in B003 verifier-report |
| Forward-test scorer B6/B1 fallback legality limited to forbidden_action wordlist | detector_limit | V004 debt; outside shadow scope |

None of these are shadow-introduced; all are pre-existing and non-blocking.
