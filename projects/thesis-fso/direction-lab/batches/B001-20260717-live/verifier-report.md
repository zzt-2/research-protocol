# B001 independent verifier report

> Verdict: **PASS (sandbox evidence integrity)**
> Scope: read-only audit of the already completed B001 artifact; no simulation was rerun and no file other than this report was modified.

## Evidence and integrity checks

| Check | Result | Evidence |
|---|---|---|
| Controller RUN receipt | PASS | `controller-audit.jsonl`: RUN decision `decision-17fd2307a0f54e148293c03c1850aa7d`, `blocked=false`; execution event also `blocked=false`. |
| Manifest hash | PASS | `manifest.json`, `result.json`, controller receipt and evidence-gate record all hash to `f1ca08c13028ae5dc5166718b50b32280b9290260f00bdbd8d8e125f5039b1d8`. |
| Result hash | PASS | `execution.result_hash` and gate/ledger `result_hash` are `a592fca95a9e33efe7e4cbd3ce1d64dd8ffc4a8dcd24d15f24ad9a4185037853`; recomputed from `execution.result`. |
| Evidence gate | PASS | `evidence-gate-audit.jsonl`: `accepted=true`, `artifact_status=ACCEPTED`, `trust_status=TRUSTED`; one admitted decision, zero replay rejections and zero stale invalidations. |
| Source closure | PASS | `manifest.source_snapshot` has 17/17 existing files; every current SHA matches. Recomputed `source_hash` is `ce5cd9f82c1bc20cb390fcb3f9d6fda72e84d6b6f412b08e634f35a0a35bd142`. The ordered 17-file component fingerprint recomputes to `6869e52461a652f67bd3e5ce6a2e694e0aaff4f2710687a4f2743ffc62ef61e6`, matching `component-registry.yaml`. |
| Queue/map/registry closure | PASS | Queue SHA equals `queue_hash=8a7420f1d8da7d58a02eb1c311b0c05728912d2f51f3a9e595f93a152ea6c037`; queue/map IDs, B001 candidate IDs/specs, rates, train/test seeds, and baseline/component fingerprints match current `batch-queue.yaml`, `candidate-map.yaml`, and `component-registry.yaml`. Both queue and map gates are PASS. |

## Paired design and leakage audit

- `execution.result` contains exactly 30 cells, 30 `baseline_calls`, and 46,860 rows (1,562 rows per cell). The 30 cells are the two rates × 15 disjoint seeds; train seeds are 11–20 and test seeds are 41–45, with no seed overlap.
- The exact feature set is the 12 causal CMA-trace transforms: log, one-step delta, causal rolling mean, and causal rolling standard deviation for `cm_error`, `output_power`, and `update_norm`. No feature key is `h`, `theta`, `sX`, `sY`, transmitted symbols, true Jones/channel state, or a future-window statistic. `build_trace_features()` uses the inclusive prefix window ending at the current block.
- Both `fixed_label_ber` and `permutation_invariant_ber` (also `pi_ber`) are present and finite on every row. The assignment field contains both `(x,y)` and `(y,x)`, so the PI comparator is not a placeholder.
- The historical single-threshold comparator is explicitly `candidate=false` and has evaluated metrics at both rates (`status=EVALUATED`); it is a negative control, not a revived candidate.
- Logistic/MLP fit only on `split=train`; their score thresholds are calibrated from control-rate train scores. The autoencoder has `training_rates=[4e-6]` only, fits its representation on clean rows of that control-rate train subset, and also calibrates from control-rate train scores. No test row is used for fitting or threshold selection. The implementation uses train labels to identify clean/control cells; this is pre-registered oracle-label supervision, not test leakage.

## Minimum information and preregistered candidate verdicts

The artifact reports 4 persistent test event cells and 6,279 positive train blocks, satisfying the queue minimum-information rule. Applying the B001 rules only to the named mechanisms:

| Candidate | Sandbox test observation | Rule outcome |
|---|---|---|
| `C24-SL-LINEAR` | At event rate `1e-5`: recall 1.00, control-rate (`4e-6`) false alarm 0.20, AUROC 0.9622865429. | **ADVANCE_SPECIFIC** |
| `C24-SL-MLP` | At event rate `1e-5`: recall 1.00, control-rate (`4e-6`) false alarm 0.00, AUROC 0.9577760316. | **ADVANCE_SPECIFIC** |
| `C24-SSL-AE` | At event rate `1e-5`: recall 0.00, control-rate (`4e-6`) false alarm 0.40, AUROC 0.8292932545. | **RETIRE_SPECIFIC** (recall=0 rule) |

These are local mechanism outcomes only. They do **not** constitute a family-wide ML kill, a canonical-baseline change, a formal Go/Kill decision, or paper promotion.

## Valid-domain and publication boundary

All observations above are valid only for the exact B001 contract: dual-pol OSL GG strong turbulence, QPSK, 20 dB, `N=100000`, block 64, `alpha=4.2`, `beta=1.4`, `f_g=30 Hz`, standard CMA/Godard-with-z (`mu=0.001`, 11 taps), rates `4e-6` and `1e-5`, train seeds 11–20, test seeds 41–45. No cross-SNR, `f_g`, modulation, sequence-length, or deployment claim is licensed. The manifest is `sandbox_only=true`, `promotion_allowed=false`, and `evidence_status=EXPLORATORY`; none of these performance numbers may enter paper materials automatically.
