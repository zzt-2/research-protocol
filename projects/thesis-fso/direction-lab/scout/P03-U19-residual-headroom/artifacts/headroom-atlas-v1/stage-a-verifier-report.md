# Independent Verifier Report — Headroom Atlas Stage A

> Verifier: independent code-review subagent (separate context, no prior involvement in the Atlas run)
> Date: 2026-07-19
> Verdict: **PASS**
> Subject: `projects/thesis-fso/direction-lab/scout/P03-U19-residual-headroom/artifacts/headroom-atlas-v1/stage-a-atlas.json`

## Verification scope

The verifier was asked to adversarially check five areas, recomputing cells directly from the frozen source closure (not via the gate) and cross-checking SHAs across receipt / audit / disk.

## Findings

### A. History guards — PASS
- B001/B002/B003 unmodified: `git diff --quiet HEAD` clean against `batches/B001-20260717-live`, `B002-20260718-live`, `B003-20260718-live`.
- Canonical baseline unmodified: `common/_dual_pol_channel.py`, `common/_gg_time.py`, `canonical-state.yaml` clean.
- B004 absent: no `B004*` under `batches/`.
- No ML/Queue/Registry added: only the new `headroom-atlas/` package, the gate test, and the artifacts dir were added; no training/queue/registry code anywhere in the new files.

### B. Gate binding integrity — PASS
- Assessment SHA `73c355f9…fb9f` matches across receipt, all 24 audit records, and disk.
- Validator SHA `ccdbd47c…3066` matches across receipt, all 24 audit records, and disk.
- Re-run of `tools/validate_claim_scope.py` on the pre-run assessment: PASS (exit 0).
- Audit log: 24 lines, all parse as JSON, **2 AUTHORIZED + 22 SUMMARY_WRITTEN** (2 runs × 11 cells), timestamps monotonic non-decreasing, 2 distinct nonces.

### C. Determinism — PASS (3 cells recomputed from scratch)
- `qpsk-snr05-nominal-short`: recomputed `LOCAL_NEGATIVE`, visible_headroom=0.0, n_error_events=18 — matches Atlas to last digit.
- `qpsk-snr20-nominal-short` (P03 v1 anchor): recomputed all-zero PI-SER for nearest/blind/oracle across all 10 seeds, n_error_events=0 — matches Atlas.
- `qpsk-snr15-fg1000-long`: recomputed `NON_DECISIVE` / `SUB_MDE_HEADROOM`, visible_headroom=`0.00039062500000000035` — **bit-identical** to Atlas.

### D. Aggregation sanity — PASS
- `n_advance_cells=0` reconciles with zero cells having `visible_headroom >= 0.005`.
- `max_visible_headroom=0.00039` equals the cell max.
- Sub-counts reconcile: 10 LOCAL_NEGATIVE + 1 NON_DECISIVE = 11 runnable; 6 zero-error/sensitivity-limited; 5 carry real error events.
- Exit `NO_HEADROOM_IN_REPRESENTATIVE_DOMAIN_WITH_CERTIFICATE` follows from "0 cells above MDE AND not all cells sensitivity-limited".

### E. P03 v1 anchor fidelity — PASS
- `qpsk-snr20-nominal-short` reproduces P03 v1 exactly: per-seed PI-SER = 0.0 for nearest/blind/oracle across seeds 11–20.
- Eval window `{eval_start: 133, calibration_end: 261, eval_end: 389}` matches the source-equivalence contract's frozen geometry.
- `n_error_events = 0`.

## Verifier-reported defects

None.

## Cross-references

- Independent gate-adversarial review (separate subagent, earlier in same session): 8 additional attack-vector tests added to `tests/test_headroom_atlas_gate.py`, all 19 gate tests pass, no holes found.
- Closeout claim-scope assessment `atlas-closeout-assessment.v1.yaml` PASSes the validator and carries its own content-addressed receipt `atlas-closeout-receipt.v1.yaml`.
