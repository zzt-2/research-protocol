# Ch4 Production Evidence Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: Use subagent-driven-development to implement this plan task-by-task. Every code task uses a fresh implementer and an independent reviewer; no task may run production before its upstream gate passes.

**Goal:** Build a corrected, reproducible Ch4 evidence seam and produce the figures, tables, statistics, and claim boundaries needed for a complete professional master-thesis method chapter.

**Architecture:** Preserve all T071 historical artifacts unchanged. Repair the shared hard demapper under tests, replay the exact historical observations to isolate its effect, then add a new task-specific production kernel with independent RNG substreams, exact latent pairing, balanced pilots for `Np=2/4/8/16`, a same-information scalar comparator, manifest-driven runners, raw-only reducers, and independent verification. Execute in gated order: historical replay → production-seam bridge → smoke/tuning → frozen production → reduction/figures → chapter package.

**Tech Stack:** Python 3, NumPy, SciPy where already available, pytest/unittest-compatible tests, JSON manifests/raw/receipts, Matplotlib, Git hashes and SHA-256 receipts.

---

## Global execution rules

- Worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`.
- Before every simulation-bearing task, reread `sim-preflight`, `thesis-lessons.md` quick table + latest three entries, `code-quality.md`, the active task brief and the frozen manifest.
- Do not modify `confirmation_*.json`, `development_*.json`, old reducers, or old plots.
- Use `apply_patch` for source/document edits. Generated JSON/CSV/figures may be written only by committed runner/reducer scripts.
- Each task begins with a failing test or a deterministic preflight proof and ends with fresh command output plus independent review.
- Stage only task-owned files. Preserve all unrelated dirty files listed in the active session state.
- Main thread integrates one campaign commit by amendment where safe; task worktrees may use one task commit each.

## Task 1: Repair the 16APSK hard-demapper contract

**Files:**

- Modify: `projects/simulation/common/_modulation.py`
- Create: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/tests/test_m16apsk_ml_demod.py`
- Create: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/demapper-correction-note.md`

**Step 1: Write failing tests**

- Assert all 16 normalized constellation points round-trip to their labels.
- Assert the frozen adversarial point at radius `0.9155` on the first inner ray maps to `0000` and equals brute-force nearest-neighbor.
- Assert a deterministic off-boundary complex cloud gives exactly the same labels as brute-force distance to all 16 points.

**Step 2: Prove the test currently fails**

Run from the Ch4 seam:

`python -m pytest tests/test_m16apsk_ml_demod.py -q`

Expected: at least the adversarial/global-ML test fails under the historical ring-threshold implementation.

**Step 3: Apply the minimal implementation fix**

Replace forced radius classification with `pick_outer = d_outer_min < d_inner_min`. Remove dead threshold variables; do not change constellation mapping, normalization, labels, tie behavior, or modulator.

**Step 4: Run focused and neighboring tests**

`python -m pytest tests/test_m16apsk_ml_demod.py tests/test_scaled_unitary.py tests/test_development.py tests/test_confirmation.py ../../tests/test_common.py ../../tests/test_ch4_apsk_ring_gated_rde.py ../../tests/test_ch4_apsk_ring_gated_rde_development.py ../../tests/test_ch5_apsk_llr_calibration_correctness.py -q`

From the repository root, run `rg -l "m16apsk_demod" projects/simulation -g "test_*.py"` and capture the result in the correction note. If later direct-caller tests appear, add them before the gate; do not run old research grids as regression tests.

Then run deterministic import/compile checks and `git diff --check`.

**Step 5: Record compatibility boundary**

Document the old behavior, minimal counterexample, why historical raw remains immutable, and that all new evidence uses the corrected contract. No BER claim in this task.

**Gate:** all tests pass and independent reviewer confirms the implementation equals full 16-point ML. Otherwise stop.

## Task 2: Isolate the demapper effect on historical observations

**Files:**

- Create: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/demapper_replay_manifest.json`
- Create: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/run_demapper_replay.py`
- Create: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/reduce_demapper_replay.py`
- Create: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/tests/test_demapper_replay.py`
- Generate: `demapper_replay_raw.json`, `demapper_replay_aggregate.json`, `demapper_replay_receipt.json`

**Step 1: Freeze the isolation contract**

Read historical `confirmation_manifest.json` and `confirmation_raw.json`; reuse exactly its cells, seed arithmetic, payload size, `development.make_realization` and receiver recipes. The new runner must refuse any changed cell/seed/action identity and must write only `demapper_replay_*` through `save_results()`.

**Step 2: Test observation identity**

- Reconstructed `realization_hash` and `observation_hash` must match historical raw for all 256 windows before scoring.
- Receiver action bytes for each deployable arm must remain deterministic.
- Only the demapper/scoring implementation hash may differ.
- Reducer recomputes pooled counts and paired CIs raw-only.

**Step 3: Run the isolated 4×64 replay once**

Independent verifier recomputes all four cells and pooled Np2 from raw without importing the reducer.

**Gate:** pooled Np2 C4−B2 CI upper `<0`, both Np4 `D=BER_C4-BER_B2` CI lower `<=0`, and 256/256 observation hashes identical. Otherwise terminal=`DEMAPPER_CORRECTION_SIGNAL_LOST` and stop before building the production seam.

## Task 3: Build the production kernel under TDD

**Files:**

- Create: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/production_core.py`
- Create: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/tests/test_production_core.py`
- Modify only if strictly needed: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/scaled_unitary.py`

**Step 1: Freeze public interfaces in tests**

Implement/test these interfaces:

- `balanced_pilots(n_pilots) -> complex ndarray[2,n_pilots]`
- `make_latent_window(scenario, latent_id, payload_symbols, max_pilots) -> dict`
- `observe_latent(latent, snr_db, n_pilots) -> dict`
- `receiver_action(arm, x_pilots, y_pilots, y_payload, parameter) -> dict`
- `score_action(action, bits, h_true) -> dict`
- `structure_mismatch_matrix(left, right, delta) -> ndarray[2,2]`

**Step 2: Test scientific invariants**

- `X_pX_p^H=N_pI` for `Np=2/4/8/16`.
- Bits/Q/Gamma–Gamma/pilot noise/payload noise have independent, reproducible hashes.
- Every substream records its deterministic `SeedSequence.spawn_key`; tests assert the full key namespace and exact replay, not merely unequal output hashes.
- Changing only SNR preserves all latent hashes and changes observations only through analytic noise scaling.
- Changing Np preserves bits/Q/g/payload-noise hashes and uses the frozen pilot-noise prefix/block rule.
- Weak/moderate/strong parameters resolve from `SimulationConfig().turbulence` and equal `(11.6,10.1)`, `(4.0,1.9)`, `(4.2,1.4)`; associated `0.2,1.6,3.5` are plane-wave Rytov variances, while the rounded-parameter Gamma–Gamma scintillation indices `1/alpha+1/beta+1/(alpha beta)` are about `0.193752,0.907895,1.122449`. Write the resolved snapshot and authority into every manifest instead of re-hardcoding it in the kernel.
- B2 `tau=1` and C4 share `UV^H`; their only difference is public scale.
- B3_PSC reads only receiver-visible pilots and applies a nonnegative-real scalar calibration after B2.
- B3_PSC implements `a=max(0,Re<tr(Zp^H Xp)>/||Zp||_F^2)` for `Zp=W_B2Yp`, with fail-closed handling of nonpositive/nonfinite denominator or nonfinite output.
- Mismatch construction uses `H_delta=g U diag(1+delta,1-delta)V^H/sqrt(1+delta^2)`, preserves average channel power, shares `U,V,g` across delta and changes the true singular-value ratio monotonically.
- Invalid matrices fail closed; no truth enters deployable action.

**Step 3: Implement minimally and run tests**

`python -m pytest tests/test_production_core.py tests/test_m16apsk_ml_demod.py tests/test_scaled_unitary.py -q`

**Gate:** invariants and reviewer pass. No experiment grid in this task.

## Task 4: Implement and run the production-seam bridge

**Files:**

- Create: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/corrected_anchor_manifest.json`
- Create: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/run_corrected_anchor.py`
- Create: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/reduce_corrected_anchor.py`
- Create: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/corrected_anchor_reducer.py`
- Create: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/tests/test_corrected_anchor.py`
- Generate: `corrected_anchor_raw.json`, `corrected_anchor_aggregate.json`, `corrected_anchor_receipt.json`

**Step 1: Manifest and schema tests**

Freeze resolved moderate `(4.0,1.9)`, `14/18 dB×Np=2/4`, 64 new latent windows/cell, B0/B2(tau=1)/B3_PSC/C4/O1, separate seeds/hashes, bootstrap seed/resamples, code/manifest hashes, base commit and no historical overwrite.

**Step 2: Runner/reducer tests**

- Checkpoint/resume is idempotent.
- Raw-only reducer ignores any precomputed aggregate.
- Pooled BER uses total bit counts.
- Paired CI resamples latent windows, not arms/cells independently.
- Receipt independently verifies manifest/raw/code hashes and truth firewall.

**Step 3: Smoke one latent window per cell**

Run the exact runner with a manifest-approved smoke override that writes only temporary/smoke outputs; check finite metrics and schema. Smoke numbers are non-thesis.

**Step 4: Run the fixed production-seam bridge**

Run the 4×64 batch once, reduce once, then have a fresh verifier recompute headline values directly from raw.

**Decision terminal:**

- `PRODUCTION_SEAM_BRIDGE_PASS`: pooled Np2 C4−B2 and C4−B3_PSC CI upper both `<0`, every Np4 `D=BER_C4-BER_comparator` CI lower `<=0`, full verification PASS.
- `CHEAP_COMPARATOR_NOT_CLEARED`: C4 does not significantly beat B3_PSC in pooled Np2 or significantly regresses in an Np4 cell; stop full production and return to chapter-identity discussion.
- `PRODUCTION_SEAM_BRIDGE_INVALID`: measurement seam fails; repair seam only, never extend science.

## Task 5: Smoke, tune B2 on disjoint data, and freeze production manifest

**Files:**

- Create: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/tune_b2.py`
- Create: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/production_manifest.json`
- Create: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/production-freeze.md`
- Create: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/tests/test_production_manifest.py`

**Step 1: Development-only tau tuning**

Use 32 disjoint latent windows for each formal `scene×Np` at development SNR `{15,25,35}` and `tau={0,.25,.5,.75,1}`. Freeze one tau per `scene×Np` by minimizing

`J(tau)=mean_snr log10((bit_errors_tau(snr)+0.5)/(payload_bits(snr)+1))`.

Exact ties select the numerically smallest tau. Save tuning receipt separately; never mix these windows into production and never tune per SNR.

**Step 2: End-to-end smoke**

Exercise SNR `5,15,25,35`, `Np=2/4/8/16`, three turbulence scenes, two mismatch levels, all arms, reducer and provisional plots with a very small frozen smoke population.

**Step 3: Freeze exact production cells**

Manifest must contain SNR grid/extension rule, 128 latent windows per formal cell, all resolved physical parameters, arm recipes, frozen tau, threshold authority, metrics, 5000-replicate bootstrap, hashes, checkpoint format and prohibited post-freeze changes. Freeze mismatch to moderate/Np2/25 dB and `delta={0,.05,.10,.20,.30,.40}`.

**Gate:** smoke is structurally valid, no overflow/empty crossing/schema error, and independent manifest reviewer passes. Smoke values remain prohibited from thesis.

## Task 6: Run resumable formal production

**Files:**

- Create: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/run_production.py`
- Create/update generated checkpoint and `production_raw.json` only through the runner.

**Step 1: Validate frozen authority**

Runner refuses to start if manifest/code/base hashes differ, demapper-replay receipt is not PASS, or production-seam-bridge receipt is not PASS.

**Step 2: Run slices in frozen order**

1. moderate full BER grid, Np2/4;
2. moderate pilot sweep, Np8/16 supplement;
3. weak/strong Np2 scene-summary supplement;
4. moderate mismatch supplement;
5. deterministic SNR extension only if the manifest rule triggers.

**Step 3: Checkpoint and monitor**

Checkpoint after every cell; resume skips only rows whose full identity/hash validates. Report progress by slice, not by interesting result. Do not inspect/plot partial results to change remaining cells.

**Gate:** expected cell/window counts and all hash/pairing checks pass.

## Task 7: Reduce formal evidence and generate the chapter figures/tables

**Files:**

- Create: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/production_reducer.py`
- Create: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/reduce_production.py`
- Create: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/tests/test_production_reducer.py`
- Modify: `projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/plot_ch4_results.py`
- Generate under: `projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/data/` and `figures/`

**Step 1: Test reducer math with synthetic fixtures**

- pooled counts;
- paired latent bootstrap;
- Jeffreys-smoothed `log10(BER_J)` crossing interpolation only within a bracket;
- joint-latent whole-curve bootstrap that recomputes both crossings and required-SNR gain in every replicate;
- `unreached` behavior;
- `CROSSING_UNSTABLE` if fewer than 95% replicates bracket both methods;
- AUC/scene summary rule;
- mismatch boundary rule;
- zero-error point display with a documented plotting floor without substituting the statistical value.

**Step 2: Reduce raw-only and emit machine-readable tables**

Write full curve CSV, required-SNR table, mechanism table, scene summary, mismatch summary, comparator identity table and a receipt with source hashes.

**Step 3: Generate final visual package**

- Keep Ch3-compatible typography, size, colors and exact SNR label.
- Use log BER axis and full frozen grid; never crop to two favorable points.
- Make B2/B3_PSC/C4 visually distinguishable; O1 visually secondary.
- Render vector PDF/SVG and 300 dpi PNG; visually inspect every output.

**Gate:** independent raw recomputation matches all headline values and visual review finds no misleading axis/legend/caption.

## Task 8: Independent scientific verification

**Files:**

- Create: `projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/production-verification.md`
- Generate: `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/production_receipt.json`

Verifier must not reuse the production reducer for headline numbers. It must independently check:

- manifest/raw/code hashes and exact population counts;
- common latent hashes across arms/SNR/Np;
- no truth leakage;
- demapper equals global ML on independent samples;
- B2 tuning split disjointness;
- BER/count arithmetic, paired CIs, threshold crossings, mechanism percentages and mismatch boundary;
- every figure/table number traces to raw;
- failure cells and cheap comparator are not omitted.

Terminal: `PASS`, `PARTIAL`, or `FAIL`; only PASS allows chapter packaging as formal evidence.

## Task 9: Rebuild the Ch4 thesis package

**Files:**

- Modify: `projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/fact-matrix.md`
- Modify: `projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/chapter-blueprint.md`
- Modify: `projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/algorithm-box.md`
- Modify: `projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/claim-and-citation-ledger.md`
- Modify: `projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/README.md`
- Modify/create final method and result figures/data tables under the package.

Update the chapter from old four-cell confirmation to the full evidence contract. Every paragraph-level claim gets a raw/code/authority pointer; every negative or absorbed result constrains the claim ceiling. Keep the final story ordered by problem → method → fairness → full performance → mechanism → robustness/boundary → complexity → Ch3 interface.

No thesis正文 is edited in this task. The output is a chapter-ready evidence and writing package.

## Task 10: Final independent chapter review and governance closeout

**Files:**

- Modify/create: `projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/independent-review.md`
- Update only after evidence: active `.sessions` decision/verification/controller/index/master-state records.

Use separate reviewers for:

1. scientific correctness and comparator fairness;
2. result reproducibility and raw arithmetic;
3. thesis-story/visual professionalism and cross-Ch3 terminology.

Run task-control validation, all focused tests, deterministic artifact checks, `git diff --check`, and exact staged-file audit. Close with one evidence-backed terminal:

- `CH4_PRODUCTION_PACKAGE_READY`;
- `CH4_CLAIM_LIMITED_BUT_WRITABLE`;
- `CH4_PRODUCTION_STOPPED`.
