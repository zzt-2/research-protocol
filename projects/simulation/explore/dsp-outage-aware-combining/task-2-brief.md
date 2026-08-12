# Task 2 brief: dev tuning, raw reconstruction, confidence intervals, and immutable freeze receipt

Worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`

Time limit: 15 minutes. Start only after Task 1B is complete and green. Do not commit. Write source/tests/docs only with `apply_patch`; runtime artifacts may be written by the implemented runner.

Read first: design, implementation plan, Task 1A/1B reports, current `smoke_core.py` and `test_smoke.py`.

Scope: add the dev/test runner, normalized raw schema, dev-only comparator/diagnostic tuning, deterministic raw-to-aggregate reconstruction, cluster bootstrap CIs, freeze validation, and receipt writer. Run unit tests only. Do not run the 18-cell dev split, held-out seeds, or decide a scientific terminal.

TDD:

1. Extend tests first; run and capture RED.
2. Implement minimally; rerun and capture GREEN.

Required contract:

- `run_smoke.py` supports explicit commands/functions for one split/batch, raw merge, aggregate, dev tuning, receipt writing, and receipt validation. Importing it must never start a run.
- Every `(seed,cell)` realization is generated once and all B0/B1/B2 candidates/O1 consume it. Emit normalized CSV rows:
  - branch rows: split, seed, cell, turbulence, K, heterogeneity, receiver hash, branch index, receiver-visible features, estimated/true offset match, fixed individual branch BER, truth-only DSP-invalid label (`offset wrong OR branch BER>=0.44`), O1 inclusion label;
  - method rows: same pairing keys, method/candidate parameters, selected subset, no-valid flag, fixed pre-FEC BER, outage (`BER>0.02`).
- Candidate grid frozen in source before dev: B1 estimated-SNR thresholds `[-8,-6,-4,-2,-1,0,1,2,4,6]` dB; B2 top-L candidates `1..K` (includes SC/GSC/all). Do not tune on test.
- `tune_dev` selects the B1 threshold minimizing dev mean BER; selects top-L separately for K=2 and K=4; then selects strongest cheap family B1/B2 by dev mean BER using deterministic tie-breaking. It also fits:
  - power-only logistic score from estimated SNR;
  - multi-source logistic score from estimated SNR, sync peak margin, log pilot-LS residual, pilot coherence, and CPE coherence/increment as available.
  Standardization and logistic coefficients are frozen from dev only. No diagnostic score may select/combine branches.
- Implement rank AUC without test-label fitting. Handle single-class bootstrap replicates explicitly and report valid replicate count.
- `aggregate_from_raw` must compute from CSV only, cluster by seed, and use a deterministic seed-cluster bootstrap (fixed bootstrap seed and at least 1000 replicates in final runs; unit tests may use fewer). It must report:
  - G1 high-power-invalid event rate and CI, plus number/list of physical cells with events; event means a frame where dev-frozen B1 would include at least one DSP-invalid branch.
  - G2 event-frame B0 vs O1 paired relative BER regret and outage excess, each with cluster CI.
  - G3 event-frame frozen strongest cheap arm vs O1 paired relative BER regret and outage excess, each with cluster CI.
  - G4 held-out multi-source AUC, power-only AUC, AUC delta, and cluster CIs using frozen dev coefficients.
- Relative regret is `(BER_method-BER_O1)/max(BER_method,1/N_payload_bits)` and no trial is dropped.
- Aggregate must evaluate fail-stop G1→G2→G3→G4 and return exactly one allowed terminal, but unit tests must cover all four stop points and PASS. Positive terminal remains novelty-debt only.
- `write_freeze_receipt` includes `test_started=false`, source/design/test hashes, dev raw/aggregate hashes, full 18-cell identities/parameters, payload size 30720, dev seeds 0..19, test seeds 10000..10099, candidate grids, selected B1/B2/strongest cheap, diagnostic parameters, bootstrap settings, metric signatures, G1–G4 thresholds/MDE, and parameter limitations.
- `validate_freeze_receipt` fails closed on any hash/config/seed mismatch. Test split refuses to run unless the receipt validates and still says `test_started=false`.
- A second aggregation of the same synthetic/raw input must serialize byte-identically with sorted JSON.
- Tests must ensure dev/test seed sets are disjoint, deployable arm input schemas contain no truth fields, raw method arms share receiver hash, duplicate/missing merge pairs are rejected, and no proposed soft method exists.

Do not touch old b3, common/params, governance, papers, p05/coded/unrelated dirty files.

At completion write `task-2-report.md` with RED/GREEN evidence, files changed, deviations, and risks; send parent a concise summary.
