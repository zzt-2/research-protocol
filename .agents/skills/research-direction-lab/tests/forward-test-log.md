# Forward test log (Task 8)

> Aggregate log for the blind forward tests defined in session R001.
> Each round records prompts, raw responses, scorer output, and reviewer notes.

## Pragmatic baseline adjudication revision (2026-07-20)

- RED: the pre-revision Skill correctly blocked premature ML but expanded the remedy to three conventional methods, multiple long convergence points, postprocessing variants, and eventual full-atlas execution. It lacked both a pragmatic adequacy stop and a portfolio-continuation rule.
- GREEN: the revised Skill kept the evidence `DIAGNOSTIC`/`SLICE`, required `PROBLEM_SURVIVES_CONVENTIONAL_BASELINE`, selected one defensible conventional comparator plus one directly relevant cheap extension, explicitly rejected default SOTA chasing, and continued candidate/interface preparation in parallel.
- Raw runs: `tests/forward/runs/pragmatic-baseline-adjudication/round-red.md` and `round-green.md`.
- Scorer output: `tests/forward/runs/pragmatic-baseline-adjudication/score.json` (`FAIL` → `PASS`).
- Fixture: `tests/forward/pragmatic-baseline-adjudication.yaml`.

## Round 1 (2026-07-20)

_status: PASS (after scorer bug fixes; no Skill revision; no rerun needed)_

### Setup

- Five independent fresh agents, one per case. No agent saw another case's
  prompt or response. Each prompt contained only: the Skill pointer, the raw
  case facts, the decision point, the artifact pointer with sha256 (integrity
  only), the seven-section response spec, and "do not run/modify".
- Pre-registered scorer `score_forward_tests.py` with hard gates HG1–HG5 and
  behavioral checks B1–B9, as specified in R001.

### Cases and verdicts

| Case | Fixture ceiling | Checks passed | P0 violations |
|------|-----------------|---------------|---------------|
| C1 current-cma-bug-signal | DIAGNOSTIC | 9/9 | none |
| C2 p01-action-blocker | DIAGNOSTIC | 9/9 | none |
| C3 p03-local-negative | SLICE | 9/9 | none |
| C4 headroom-atlas-blocked-axes | SLICE | 9/9 | none |
| C5 non-comms-baseline-extension | DIAGNOSTIC | 9/9 (incl. B9 domain isolation) | none |

Hard gates: HG1=PASS, HG2=PASS, HG3=PASS, HG4=PASS, HG5=PASS.

### Artifacts

- Blind prompts and raw responses: `tests/forward/runs/{case}/round-1.md`
  (each file embeds the verbatim blind prompt in an HTML comment).
- Scorer aggregate output: `tests/forward/runs/score-round-1.json`
- Independent reviewer report: `.sessions/2026-07-20-research-direction-lab-system/S008-forward-test-round-1.md` (appendix)

### Scorer bug fixes after round 1 (no Skill revision)

Round 1 exposed several scorer implementation bugs. The initial FAIL verdict
was caused entirely by scorer defects; the agents' behavior was compliant
throughout. Fixes were limited to the scorer; the Skill was not edited; no
rerun was required because agent behavior is independent of scorer logic.

- `_detect_claim_level`: scope to Section 3 and use earliest-match on the
  first non-empty line. BUGFIX — whole-body scan picked up incidental level
  words ("contract" in "contract/interface gap", "candidate" in "candidate
  families").
- `_harvest_count`: scope to Section 4 and split into list items; accept
  `_`/space/`-` as the category separator. BUGFIX — greedy cross-section
  regex and the `_`-only separator dropped real harvest items.
- B6 concrete next action: accept either allowed-action token overlap or a
  concrete verb+object phrase, while enforcing a forbidden-action overlap
  guard (word-boundary on the verb and first content object). MIXED per the
  reviewer; the forbidden-overlap guard closes the legality gap the reviewer
  flagged.
- B1 continuation: reuse the (legality-checked) concrete_next. BUGFIX once
  the forbidden guard is in place.
- B9 domain isolation: word-boundary matching. BUGFIX — substring matching
  fired on "benchmark" → "ber".
- P0 scope-violation markers: action-verb phrasing rather than bare nouns.
  BUGFIX — the C4/C5 responses correctly restate "no queue/registry exists",
  which a bare-noun matcher would flag.

### Independent reviewer outcome

The independent reviewer (separate agent, raw-response audit) confirmed all
five responses satisfy B1–B9 with quoted evidence, confirmed all scorer
revisions except the B6/B1 fallback were objective bug fixes, and flagged the
fallback's legality gap as the single residual risk. That gap was then closed
by adding the forbidden-overlap guard with word-boundary verb matching. The
reviewer's blind-prompt audit found no leaks.

### Aggregate verdict

Round 1 PASS. All hard gates hold. No Skill revision was performed, so no
round 2 is required. Task 8 forward behavior is validated for the five
covered categories; this does not constitute long-term automation evidence
(that requires Task 9 shadow).

## Round 2

Not run. Per the revision discipline, a rerun is required only after a Skill
revision; round 1 needed no Skill revision.
# Cross-output portfolio fairness — 2026-07-21

- RED: real C01–C04 portfolio used one Go comparator lattice across detection/control/correction, marked a controller runnable despite missing action/state interfaces, and prioritized C01 before a bounded mechanism-level refresh.
- GREEN: fresh agent separated shared system anchor from task-specific comparators, used equal tuning opportunity, corrected readiness, required a bounded refresh, and selected a small comparable batch without demanding exhaustive mapping.
- Skill change: minimal edits to baseline adjudication, candidate portfolio, batch planning, and one routing sentence in SKILL.md.

## Probe and current-view redesign — 2026-07-21

- **Probe cost RED**: without revised guidance, a two-minute paired-input check produced five default artifacts (contract, result, receipt, source closure, verifier). **GREEN**: one compact Probe record, optional artifact pointer, no full batch governance, no forced harvest, and immediate stop after the pair.
- **Semantic RED/control**: general reasoning caught the contract/objective mismatch but did not establish the full reusable smoke set. **GREEN**: integrity and semantic validity separated; objective alignment, constant/trivial output, no-op/identity, output support, and minimal overfit precede scale; candidates remain `UNRESOLVED`.
- **Recovery GREEN**: routine hot path used current projections; explicit INVALIDATED/restore disposition overrode old handoff, synthesis mtime, and ledger prose without deleting lineage.
- Raw fixtures and responses: `tests/forward/{probe-cost-boundary,semantic-integrity-separation,recovery-current-precedence}.yaml` and corresponding `tests/forward/runs/*/round-{red,green}.md` files. Each new agent run now stores the blind prompt, agent identity/access condition, and verbatim final response; recovery uses `historical-red.yaml`, whose H009 pointer SHA256 is `61ea49ed...c5041b`, as the real RED artifact.
- Post-hoc behavior scorer: `tests/score_probe_recovery.py`. It records RED→GREEN for Probe cost and semantic completeness, and PASS for bounded current-view recovery. It is explicitly post-hoc, not mislabelled as preregistered.
- Independent terminal review first returned PARTIAL and found three P1 gaps: summary-only forward evidence, dangling/cross-entity disposition replacement, and raw-ledger STATUS consumption. Repairs added verbatim runs + scorer, strict current-disposition replacement, adapter-bound `--harvest-current`, and inactive-harvest filtering.
- Fresh full Skill gate after repairs: 90 passed, 1 environment skip.

# Thesis method packaging gate — 2026-08-03

- **RED**: a deterministic structural test added before the Skill edit failed
  against source commit `5b69a0e` because no mandatory thesis
  chapter-capability checkpoint or `THESIS_METHOD_READY` state existed.
- **GREEN**: 2/2 retained fresh-context, read-only responses preserved the
  separable receiver-visible adapter as `NEEDS_ONE_BOUNDED_PACKAGE`, kept
  `METHOD_SIGNAL=0` and active scientific carrier=0, and routed its one bounded
  closure before method factory/strategic shortage.
- Blind prompt: `tests/forward/runs/thesis-method-packaging-gate/prompt.md`;
  PASS criteria were hidden in the separate post-hoc `scorer.md`.
- Source identity and RED output:
  `tests/forward/runs/thesis-method-packaging-gate/red-receipt.md`.
- Agent identity/access and verbatim GREEN responses:
  `tests/forward/runs/thesis-method-packaging-gate/green-responses.md`.
- Exploratory samples without retained raw responses are explicitly
  non-authoritative and carry no sample-count claim.
