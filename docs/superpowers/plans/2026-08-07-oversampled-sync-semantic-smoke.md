# Oversampled Coherent Sync Q1 Semantic Smoke Implementation Plan

> **For executor:** Follow T015 exactly. This is a Groundwork Step 4a dimension-D Probe, not a formal MVE or testbed. Use test-first development and do not commit.

**Goal:** Implement and run the frozen ≤1-day deterministic semantic smoke that decides whether a visible-only coupled `(frame, tau, CFO)` grid estimator has structure not already captured by strong sequential, timing-bank, or coordinate-refinement DSP baselines.

**Architecture:** Add one isolated Probe under `projects/simulation/explore/oversampled-coherent-sync-q1/`. A pure core owns the receiver-visible data contract, RRC waveform/templates, profiled normalized GLRT score, lexicographic tie-break, B0/B1/B2/C estimators, metrics, and terminal reducer. A thin runner owns one-time paired realization generation, truth-only scoring, deterministic timing, plots, and artifacts. No import or mutation of `projects/simulation/common/`, `params.py`, or old experiment state.

**Stack:** Python 3.11, NumPy, SciPy, Matplotlib, pytest. CPU only.

---

## Task 1: Freeze the executable contract and provenance

**Files:**
- Read: `projects/thesis-fso/oversampled-sync-groundwork/step4a-preflight-discussion.md`
- Create: `projects/simulation/explore/oversampled-coherent-sync-q1/README.md`
- Create: `projects/simulation/explore/oversampled-coherent-sync-q1/semantic_smoke_core.py`
- Test: `projects/simulation/tests/test_oversampled_coherent_sync_q1.py`

1. Write tests for a complete manifest and strict separation between `ReceiverVisible` and `TruthMetadata`.
2. Run the focused pytest file and retain the expected RED evidence caused by the missing implementation.
3. Implement immutable config/data objects and manifest validation only.
4. Freeze the following executable choices in code and README:
   - 56 GBd, 2 sps, QPSK, RRC beta 0.1; RRC span 10 symbols is a diagnostic implementation choice.
   - 64-symbol fixed-seed QPSK preamble, seed `20260807`; exact literature symbols are unavailable, so this is a semantic diagnostic only.
   - TX/RX full RRC convolution, explicit aggregate group delay, fixed extended observation window, and `d=0` at the centered matched-filter template reference plane.
   - Truth grids: residual `d={-8,0,8}` samples, `tau={-0.4,-0.2,0,0.2,0.4}` samples, CFO `={-100,-50,0,50,100}` MHz; coarse stress uses CFO `={-5,+5}` GHz and is not pooled into the primary metric.
   - Common hypothesis grids: `d=-10..10` samples in steps of 1, the same five tau hypotheses, residual CFO `=-150..150` MHz in 50 MHz steps; coarse-stress CFO `={-5,-2.5,0,2.5,5}` GHz.
   - One diagnostic noisy slice at -6 dB using master seed `20260808`; seed per cell is the first 64 bits of SHA256(`master_seed|cell_id`). It is a numerical stress anchor, not an occurrence distribution.
   - Score equality tolerance `64 * eps(float64) * observation_length`; score ties inside that tolerance use the lexicographically smallest `(d,tau,cfo)`.
5. Re-run the focused tests for the first GREEN checkpoint.

## Task 2: Implement waveform, common score, and semantic gates test-first

**Files:**
- Modify: `projects/simulation/explore/oversampled-coherent-sync-q1/semantic_smoke_core.py`
- Modify: `projects/simulation/tests/test_oversampled_coherent_sync_q1.py`

1. Add failing tests for RRC unit-energy normalization, zero-impairment reconstruction, timing sign, CFO sign/Hz units, frame reference, fixed observation length, and normalized-score bounds.
2. Implement local RRC taps, fixed-seed QPSK preamble, pulse shaping, fractional-delay injection, integer frame placement, CFO injection, matched filtering/templates, and the profiled normalized GLRT:
   `abs(x^H r)^2 / (||x||^2 ||r||^2)`.
3. Generate each cell once; estimators receive only the frozen visible object. Store truth separately for scoring.
4. Add failing then passing tests for:
   - identical `realization_id`, `rx_sha256`, and window/grid hashes across all methods;
   - hidden-truth mutation leaves four estimator outputs, traces, and compute counters byte-identical;
   - identity returns `(0,0,0)` for B0/B1/B2/C;
   - score/tie-break consistency.
5. If any identity/information/score gate cannot pass without changing the frozen contract, stop as `SEMANTIC_INVALID`; do not emit a science terminal.

## Task 3: Implement B0/B1/B2/C without truth access

**Files:**
- Modify: `projects/simulation/explore/oversampled-coherent-sync-q1/semantic_smoke_core.py`
- Modify: `projects/simulation/tests/test_oversampled_coherent_sync_q1.py`

1. Add synthetic-cube tests before each method implementation.
2. Implement B0 as the strengthened staged common-score chain:
   - coarse CFO: profile over all frame hypotheses at `tau=0`;
   - timing: profile over frame at the selected CFO;
   - frame/fine CFO: jointly optimize frame and the selected CFO plus its immediately adjacent CFO bins at the selected tau;
   - no stage may revisit a discarded tau branch.
3. Implement B1 as the operational exhaustive timing bank: for every tau branch, run the same frame/CFO search on the complete common grid, then choose the global terminal score. This is intentionally the same candidate set and score as C-grid; its equality with C is the structural question, not a test fixture trick.
4. Implement B2 as coordinate refinement initialized by B0: update tau at fixed `(d,cfo)`, then jointly update `(d,cfo)` at fixed tau; accept non-decreasing common-score moves; stop at a fixed point or after 8 iterations.
5. Implement C-oracle as the visible-only global argmax over the complete frozen 3-D grid. It must never read truth and performs no genie/continuous refinement.
6. Instrument explicit complex MACs, FFT calls/sizes, interpolation calls, candidate-score calls, visited candidates, and deterministic traces. Wall time is measured separately by the runner.
7. Prove in tests that B1 and C have equal cubes/argmax/tie-break on the common-grid equivalence slice, and that B2 obeys monotonicity and the stop rule.

## Task 4: Implement scoring, topology diagnostics, and terminal reducer

**Files:**
- Modify: `projects/simulation/explore/oversampled-coherent-sync-q1/semantic_smoke_core.py`
- Modify: `projects/simulation/tests/test_oversampled_coherent_sync_q1.py`

1. Add failing tests for exact-index false-lock semantics, `miss=None`, integer-count coverage arithmetic, B0-zero headroom, stable 2x2 detection, layer isolation, and every reducer boundary.
2. Define the primary population as the complete 75-cell residual grid at each reported noise layer. Stress cells remain separate. Acquisition success is exactly `1-R_FL`.
3. A stable error region requires an axis-adjacent 2x2 tau/CFO block at fixed frame, layer, and SNR whose four cells share the same wrong-basin `(d,tau,cfo)` label. Do not pool across layers or frames.
4. Compute and report, but do not use as a standalone pre-registered kill threshold, the finite-difference local tau/CFO Hessian cross ratio and additive-interaction residual of the profiled surface. Exact factorization within numerical tolerance may count as `SEPARABLE`; otherwise near-separability remains diagnostic because no physical threshold was frozen.
5. Reducer priority:
   - failed identity/paired/truth/score gates -> `SEMANTIC_INVALID` and no science terminal;
   - incomplete required residual population -> `STEP4A_PREFLIGHT_EVIDENCE_GAP`;
   - B0 false locks zero, B1/C grid equivalence, exact separability, no stable 2x2 region, `G_C<5%`, or either coverage `>=95%` -> `STEP4A_PREFLIGHT_KILL_OR_PIVOT`;
   - only analytic and surface nonseparability + stable region + `G_C>=5%` + both coverages `<95%` -> `STEP4A_PREFLIGHT_RECOMMEND_MICRO_MVE`;
   - otherwise -> `STEP4A_PREFLIGHT_EVIDENCE_GAP`.
6. Run the entire focused pytest file.

## Task 5: Add runner, execute the bounded grid, and write artifacts

**Files:**
- Create: `projects/simulation/explore/oversampled-coherent-sync-q1/run_semantic_smoke.py`
- Create at runtime: `projects/simulation/explore/oversampled-coherent-sync-q1/artifacts/manifest.json`
- Create at runtime: `projects/simulation/explore/oversampled-coherent-sync-q1/artifacts/observations.jsonl`
- Create at runtime: `projects/simulation/explore/oversampled-coherent-sync-q1/artifacts/truth.jsonl`
- Create at runtime: `projects/simulation/explore/oversampled-coherent-sync-q1/artifacts/method_results.jsonl`
- Create at runtime: `projects/simulation/explore/oversampled-coherent-sync-q1/artifacts/ambiguity_surfaces.npz`
- Create at runtime: `projects/simulation/explore/oversampled-coherent-sync-q1/artifacts/ambiguity_surface.png`
- Create at runtime: `projects/simulation/explore/oversampled-coherent-sync-q1/artifacts/summary.json`
- Create at runtime: `projects/simulation/explore/oversampled-coherent-sync-q1/artifacts/terminal.json`
- Create at runtime: `projects/simulation/explore/oversampled-coherent-sync-q1/artifacts/provenance.json`
- Create at runtime: `projects/simulation/explore/oversampled-coherent-sync-q1/artifacts/tdd-evidence.jsonl`
- Create: `projects/thesis-fso/worker-logs/step-015-q1-semantic-smoke.md`
- Create: `projects/thesis-fso/oversampled-sync-groundwork/semantic-smoke-report.md`

1. Add a CLI with `--identity-only`, `--run-grid`, and explicit `--output-dir`; reject any output path outside the Probe directory.
2. Run identity-only first. A nonzero exit stops the package as `SEMANTIC_INVALID`.
3. Run the residual noiseless, residual -6 dB diagnostic, and separate ±5 GHz stress grids. Every cell supplies one immutable sample array to all methods.
4. Warm up each method, then measure five same-process calls per representative layer/cell and store the median plus raw timings. Do not fabricate library FFT MAC counts; report FFT calls/sizes separately.
5. Save full common surfaces once per cell, visited masks/paths per method, hashes, config, dependency versions, script SHA256, and current HEAD. Plot the profiled tau/CFO ambiguity surface and mark truth/top-1/wrong basin for the worst B0 cell plus identity.
6. Write the worker log and scientific report facts-first. Do not call a method “novel”, do not generalize diagnostic false-lock frequencies into field probabilities, and do not recommend a formal MVE unless the exact reducer returns the allowed recommend terminal.

## Task 6: Deterministic executor self-check and handoff

**Files:**
- Verify all files above only; do not modify governance files.

Run from the evidence worktree:

```powershell
python -m pytest projects/simulation/tests/test_oversampled_coherent_sync_q1.py -q
python projects/simulation/explore/oversampled-coherent-sync-q1/run_semantic_smoke.py --identity-only
python projects/simulation/explore/oversampled-coherent-sync-q1/run_semantic_smoke.py --run-grid --output-dir projects/simulation/explore/oversampled-coherent-sync-q1/artifacts
git diff --check
git status --short
```

Return the exact test counts, artifact hashes, run terminal, method false-lock counts/rates, `G_C`, coverages, stable-region result, B1/C equivalence result, compute ledger, warnings, and changed-file allowlist. Do not commit or push.

## Task 7: Independent verification and governance closeout

After the executor returns, the main controller creates a separate verifier task. The verifier must independently check task-control, tests, artifact referential integrity, receiver/truth separation, reducer arithmetic, protected paths/log hashes, and report consistency. Only after verifier PASS may the main controller write D012/V008/H005, update formal/RDL control, and make the conversation's single commit.
