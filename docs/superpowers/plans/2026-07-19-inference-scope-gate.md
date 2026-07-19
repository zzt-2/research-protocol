# Direction Lab Inference Scope Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prevent cell- or slice-level evidence from silently retiring a domain or candidate family, and prevent zero visible headroom from being represented as measured analytic coverage.

**Architecture:** Add one generic YAML validation gate beside the existing CandidateMap and Queue validators. The gate validates an inference-scope assessment overlay, leaving immutable experiment contracts and raw artifacts untouched. Direction Lab process documentation owns the five-level `CELL → SLICE → DOMAIN → CANDIDATE → FAMILY` claim model; P03 receives a superseding assessment that preserves D057/V030 as historical evidence while reopening candidate- and family-level domain adequacy.

**Tech Stack:** Python 3, PyYAML, pytest, Markdown/YAML governance artifacts.

## Global Constraints

- Do not modify P03 probe raw artifacts, B001/B002/B003, canonical-state, or formal paper material.
- Preserve the historical zero-headroom `coverage=1.0` result as contract output; normalize it to `UNDEFINED_ZERO_HEADROOM` only in the inference-scope assessment layer.
- A local negative result may close a cell or slice but may not close a domain, candidate, or family without a valid exit certificate.
- Candidate-level exit certificates use only `MECHANISM_PROOF`, `REPRESENTATIVE_DOMAIN_COVERAGE`, or `STRONG_BASELINE_DOMINANCE`.
- Record the user correction and superseding decision through session-governance; do not delete D057/V030.
- Run RED before production implementation and perform independent verification before the single end-of-session commit.

---

### Task 1: Generic inference-scope validator

**Files:**
- Create: `projects/thesis-fso/direction-lab/tools/validate_inference_scope.py`
- Create: `projects/thesis-fso/direction-lab/tests/test_inference_scope_gate.py`

**Interfaces:**
- Consumes: a YAML mapping with `evidence_scope`, five-level `requested_verdicts`, `statistical_sensitivity`, `headroom`, `historical_counterexamples`, and `certificate`.
- Produces: `load_assessment(path) -> dict`, `validate_assessment(data) -> ValidationReport`, and a CLI returning 0 on PASS and 1 on FAIL.

- [ ] Write RED tests proving that zero headroom plus measured coverage `1.0` is rejected, a cell-local zero-headroom assessment with `measured_coverage: null` passes, missing four-level verdicts fail, and family exit without a certificate fails.
- [ ] Run `python -m pytest projects/thesis-fso/direction-lab/tests/test_inference_scope_gate.py -q` and confirm failure because the validator is absent.
- [ ] Implement the smallest validator that satisfies the declared schema and three hard gates.
- [ ] Re-run the focused tests and confirm PASS.

### Task 2: P03 superseding scope assessment

**Files:**
- Create: `projects/thesis-fso/direction-lab/scout/P03-U19-residual-headroom/inference-scope-assessment.v1.yaml`
- Modify: `projects/thesis-fso/direction-lab/scout/P03-U19-residual-headroom/residual-headroom-probe-status.yaml`
- Modify: `projects/thesis-fso/direction-lab/scout/P03-U19-residual-headroom/readiness-report.yaml`
- Modify: `projects/thesis-fso/direction-lab/batch-plan.v1.yaml`

**Interfaces:**
- Consumes: immutable P03 contract/result plus historical QPSK/16QAM/SNR/dynamics/sequence-length reversals.
- Produces: a validator-PASS overlay whose cell verdict is `NO_VISIBLE_HEADROOM`, domain/family verdicts remain unresolved/open, and candidate action is `KEEP_OPEN`.

- [ ] Add a RED fixture assertion that the repository P03 assessment passes and explicitly preserves the historical machine verdict without treating `1.0` as measured improvement.
- [ ] Run the focused test and confirm it fails while the assessment is absent.
- [ ] Add the assessment and update summaries by superseding interpretation only; do not edit raw probe artifacts.
- [ ] Re-run the focused tests and the existing P03 readiness tests.

### Task 3: Process owner and session lineage

**Files:**
- Modify: `projects/thesis-fso/direction-lab/process.md`
- Modify: `projects/thesis-fso/direction-lab/README.md`
- Modify: `.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md`
- Modify: `.sessions/2026-07-10-dual-pol-osl-groundwork/verifications.md`
- Modify: `.sessions/2026-07-10-dual-pol-osl-groundwork/topic-index.md`
- Modify: `.sessions/2026-07-10-dual-pol-osl-groundwork/voice.md`
- Modify: `.sessions/_registry.yaml`

**Interfaces:**
- Consumes: Task 1 validator semantics and Task 2 P03 overlay.
- Produces: one long-lived rule owner and a traceable supersession of D057's candidate-level stop interpretation.

- [ ] Add the four-level claim lattice, zero-headroom semantics, sensitivity declaration, historical-counterexample declaration, exit-certificate bases, and inference-scope verifier duty to `process.md`.
- [ ] Add a new D058 decision that supersedes only D057's candidate-level stop, preserves the tested-cell negative result, and records the user's verbatim correction in `voice.md`.
- [ ] Add a V031 verification entry after focused and regression checks.
- [ ] Update the entry summaries without turning the dormant governance pilot into the research state owner.

### Task 4: Verification and handoff prompt

**Files:**
- Create: `.sessions/2026-07-10-dual-pol-osl-groundwork/H###-p03-headroom-atlas.md` only if a formal handoff is needed by session-governance numbering rules; otherwise provide the prompt in the final response.

**Interfaces:**
- Consumes: validated scope gate and corrected P03 state.
- Produces: a new-task prompt for a baseline-only multi-domain Headroom Atlas, with no ML training.

- [ ] Run the focused scope-gate tests, P03 tests, relevant Direction Lab governance tests, compile checks, and the validator CLI on the P03 assessment.
- [ ] Independently verify B001/B002/B003 unchanged, B004 absent, raw P03 artifacts unchanged, and worktree diff limited to the planned files.
- [ ] Perform one end-of-session commit and report the exact test counts and remaining unrelated suite debt.
