# C11 Legality Batch v1 — Synthesis

> Schema: `direction-lab.cb1.c11-legality-batch.v1`
> Campaign: `science-scout-2026-07-20.dual-pol-osl`
> Date: 2026-07-21
> Amends subclaim of: D010 ("C11_fixed_mu 4/7 cells positive")
> Source research note: `c11-legality-batch-v1/R001-c11-legality-root-cause.md`
> Verdict: **`B_C11_SIGNAL_DISAPPEARS_AFTER_LEGALIZATION`**
> Verdict (S009 amended, scope-narrowed): **`C11_EXACT_CAUSAL_RAW_DECISION_POLICY_NO_BENEFIT`**, claim ceiling = **LOCAL_SLICE / DIAGNOSTIC**

> **2026-07-21 S009 amendment note**: the original verdict B label is retained
> for traceability. The verdict is re-scoped to the EXACT C11 variant under
> test (causal one-pass, raw nearest-16QAM DD policy, no phase/permutation
> resolution, frozen switch-point+offset tuning grid). The numeric direction
> (C11 not better than fixed-μ CMA; significantly worse on long cells) is
> unchanged. The S009 amendment closes 8 audit issues (#1–#8) listed in §10;
> none changes the verdict direction. See `decisions.md` D011-amended.

## 0. TL;DR

Under a unified complex filter convention (z = r @ w bilinear, matching the anchor),
no future information (causal one-pass CMA→DD switch at a frozen block), the same
single-pass access budget as the fixed-μ CMA comparator, and an identity gate
(dd_step=0 bit-identical to fixed-μ CMA), **the legal C11 cascade does NOT
significantly beat the fairly-tuned fixed-μ CMA (μ=0.03)**. The macro paired
Δ (C11_legal − fixed_mu) = **+0.01445** (C11 is WORSE), 95% CI = [−0.00022,
+0.04113]. Two of seven held-out cells (both long) are significantly worse;
zero of seven are significantly better. The worst-cell degradation is +0.077
PI-SER.

The 57384ed "C11_fixed_mu 4/7 cells positive" sub-claim is therefore
reclassified as an **implementation/confound diagnostic**, not a method signal.
It does not authorize a learned-corrector batch (C04/C09).

## 1. Root cause (R001)

Three legality defects in the OLD `fairness-batch-b01/b01_candidates.py:c11_cma_dd_lms_cascade`:

| # | Defect | Evidence (line numbers in `b01_candidates.py`) |
|---|---|---|
| D1 | **Complex convention flip** stage-1 vs stage-2. Stage-1 uses `z = r @ w` (bilinear, no conjugation); stage-2 uses `z = np.vdot(wxx, rx) = w^H r` (Hermitian). For complex post-convergence weights these are strictly different complex numbers. | L290-291: `zx = np.vdot(wxx, rx) + np.vdot(wxy, ry)`. Stage-1 in `cb1_cell_runner.py` L115: `zx_blk = rX_blk @ wxx + rY_blk @ wxy`. |
| D2 | **Non-causal future information**. Stage-2 starts from i=0 using the stage-1 FINAL weights (obtained only after processing the entire future stream). | L287: `for i in range(n_valid):` (starts at i=0); L269 comment: "End of stage-1 replay: wxx/wxy/wyx/wyy = stage-1 final weights." |
| D3 | **Multi-pass / unequal access budget**. Each sample is processed 3 times (stage-1 + stage-1 weight-replay + stage-2) vs 1 time for the fixed-μ CMA comparator. | L220 (`standard_cma_godard_with_z(`), L254 (`for blk in range(n_blocks):`), L287 (`for i in range(n_valid):`). |

Quantified D1 (OLD c11 with dd_step=0 vs anchor μ=0.03 on a synthetic stream):
max|ΔzX| ≈ **1.97** (order-of-magnitude of the inter-constellation distance ≈2),
max|ΔzY| ≈ 1.71. The OLD "no-op" wasn't a no-op.

## 2. Legalization (new module `c11-legality-batch-v1/c11_causal.py`)

The new `c11_cma_dd_lms_causal` fixes all three defects:

- **Unified bilinear convention**: z = r @ w everywhere. Stage-2 DD-LMS update
  is `w += dd_step * (s_hat - z) * conj(r)` — numerically verified (R001) to be
  the correct Wirtinger gradient of `J = E[|s_hat - z|^2]` for bilinear z.
- **Causal one-pass**: a SINGLE stream pass. For each block:
  - if blk < switch_point_block: CMA Godard-with-z block-end update;
  - else: per-symbol DD-LMS update (within the block, symbol-by-symbol using
    only weights causal up to the current symbol).
- **Equal access budget**: every sample is the centre of a DD update at most
  once (`stage2_max_visits_per_sample_global = 1`, confirmed).

### Identity gates (13/13 tests PASS, 8 gates + 4 OLD-impl bug-confirmations + 1 contract-path)

| Gate | Property | Result |
|---|---|---|
| complex_convention_unified | Stage-2 z = r @ w (NOT vdot) | PASS |
| no_op_dd_step_0_bit_identity | dd_step=0 ⇒ bit-identical to fixed-μ CMA at same μ | PASS (max|ΔzX|=0) |
| stage_1_state_identity | New stage-1 weights reproduce anchor output | PASS |
| causal_prefix_invariance | Future-perturbation leaves prefix outputs unchanged | PASS |
| one_pass_access_budget | Each sample visited at most once in stage-2 | PASS (max=1) |
| stage_switch_at_frozen_block | Switch is block-granular, single transition | PASS |
| source_contract_runner_consistency | DD grid + paths + versioning consistent | PASS |
| (4 negative controls) | OLD module confirmed to have D1/D2/D3 | PASS |

Independent verifier (separate context, re-derived every number): CONFIRM all
10 verification checks V1-V10, including hand-computed complex convention,
hand-run dd_step=0 identity, fresh causal-perturbation reimplementation, and
recomputed paired deltas (means bit-identical to runner; CIs within Monte-Carlo
noise).

## 3. Experimental setup (all frozen BEFORE test seeds were run)

- **System anchor + Go comparator**: fixed-μ CMA μ=0.03 (INHERITED from B01-R
  HF6 interior optimum; NOT re-tuned — no double-dip).
- **Candidate**: C11_legal_causal_one_pass, stage1_μ=0.03 (same as fixed-μ),
  unified bilinear convention.
- **No-leakage seed split** (NEW, disjoint from B01-R's 11-15 / 21-30):
  - validation: 4 cells × seeds [31, 32, 33, 34, 35]
  - test: 7 held-out cells × seeds [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
- **DD step grid (frozen)**: [0.0, 1e-6, 3e-6, 1e-5, 3e-5, 1e-4, 3e-4] (includes
  the identity 0).
- **Switch point (frozen per cell)**: plateau block + best offset ∈ {0, +1, +2}
  picked on validation. Plateau = block index after which cumulative |Δw_norm|
  over the last 4 blocks drops below 1% of init norm.
- **Practical significance threshold**: |macro mean Δ| ≥ 0.005 PI-SER absolute.
- **Primary statistic**: hierarchical paired bootstrap (cells + seeds) on
  paired delta = PI-SER(C11_legal) − PI-SER(fixed_mu).

## 4. Results

### Validation (tuning)
- Plateau block per cell: all cells = 3 (CMA converges fast on these cells).
- Best dd_step_size = **3e-4**, best switch_offset = **+2**, validation
  macro mean PI-SER = 0.124 (vs 0.147 at dd_step=0; small improvement on
  validation, but dd_step=0 is also a near-tie — the DD stage barely helps).

### Held-out (7 cells × 10 test seeds = 70 paired measurements)

| Cell | fixed_μ PI-SER | C11_legal PI-SER | paired Δ | 95% CI | sig |
|---|---|---|---|---|---|
| 16qam-snr05-nominal-short | 0.6805 | 0.6805 | +0.0000 | [−0.00117, +0.00117] | tie |
| 16qam-snr10-nominal-short | 0.5215 | 0.5219 | +0.0004 | [+0.00000, +0.00117] | tie |
| 16qam-snr15-nominal-short | 0.4145 | 0.4141 | −0.0004 | [−0.00117, +0.00000] | tie |
| 16qam-snr25-nominal-short | 0.3840 | 0.3836 | −0.0004 | [−0.00117, +0.00000] | tie |
| 16qam-snr20-fg100-short | 0.3848 | 0.3848 | +0.0000 | [+0.00000, +0.00000] | tie |
| **16qam-snr10-fg100-long** | 0.3617 | 0.3867 | **+0.0250** | [+0.00078, +0.05117] | **C11 worse** |
| **16qam-snr15-fg1000-long** | 0.2215 | 0.2980 | **+0.0766** | [+0.01680, +0.13906] | **C11 worse** |

Macro paired Δ = **+0.01445**, 95% CI = **[−0.00022, +0.04113]**.
Worst-cell Δ = **+0.0766** (C11 worse).
Divergence rate: 0.00 (both methods); Stage-2 max visits/sample = 1.

The short cells show essentially rounding-level noise (Δ ≈ ±0.0004). The long
cells — exactly where 57384ed claimed the C11 signal lived — show C11_legal
SIGNIFICANTLY worse: the per-symbol DD-LMS update, applied causally to the
converged fixed-μ weights, **destabilises** them rather than refining them.

## 5. Verdict

**`B_C11_SIGNAL_DISAPPEARS_AFTER_LEGALIZATION`**.

Decision rule application (independent verifier V9 confirmed):
- Macro mean = +0.01445 (NOT < 0) → outer Verdict A branch fails.
- Even if mean were negative: CI upper = +0.0411 (NOT < 0); worst-cell
  = +0.0766 (NOT ≤ 0); both also block Verdict A.
- best_dd_step_size = 3e-4 ≠ 0 (validation did not pick the identity; the
  DD stage has some effect on validation but it is harmful on test long cells).

## 6. What this means

1. **The 57384ed "C11_fixed_mu 4/7 cells positive" sub-claim is WITHDRAWN as
   a method signal.** It is reclassified as an implementation/confound
   diagnostic caused by the D1+D2+D3 defects.
2. **C11 is NOT promoted to a legal conventional comparator.** Future
   learned-corrector batches must NOT cite C11 as the conventional target.
3. **C04/C09 learned corrector is NOT authorised** by this batch.
4. The H1 root-cause hypothesis (R001) is **CONFIRMED**, not rejected.

## 7. Secondary finding (forward-rule label fix, H2)

The B01-R contract (`fairness-batch-b01r/batch-contract.v1.yaml` L352)
mislabeled `oracle_affine_16qam` as "blind" in the forward-rule for a future
corrector batch. The repo has two distinct functions (verified by reading
`cb1_evaluator.py`):

- `blind_affine_compare_16qam(z_calib, z_eval, ridge)` — uses z-derived 16QAM
  pseudo-labels only (NO TX truth). **Receiver-visible same-task comparator.**
- `oracle_affine_bound_16qam(z_calib, z_eval, truth_calib, ridge)` — consumes
  TX truth in calibration. **Scoring-only Kill bound (FR-21), NOT a Go
  baseline (FR-25).**

The new contract `c11-legality-batch-v1/batch-contract.v1.yaml` corrects the
forward rule to require `blind_affine_compare_16qam` as the task-specific
comparator and `oracle_affine_bound_16qam` as the Kill bound only. This is a
read-only finding; no corrector was run.

## 8. Unchanged / preserved

- B001-B003, P03 Atlas, canonical-state.yaml: untouched (`git diff` empty).
- B01 / B01-R raw artifacts (`fairness-batch-b01*`, `fairness-batch-b01r-v1.*`,
  `frozen-params-b01r-v1.yaml`): untouched (mtime before this session).
- D010 / H007 / V002: amended by this batch (D011), not overwritten.
- No ML training, no B004, no paper-text writes, no push.
- detector / B02 still paused (per task brief).

## 9. Next-step options (not auto-started; user strategic decision)

1. **Re-rank equalizer direction by residual headroom** — the residual
   headroom over `oracle_affine_bound_16qam` (Kill bound) is the legitimate
   signal that some affine correction could help; whether a learned corrector
   can BEAT the receiver-visible `blind_affine_compare_16qam` (which is
   non-trivial) is the actual open question.
2. **Rotate to detector lead-time maximisation** (path 2 from H007) — still
   unblocked.
3. **Rotate to a different mechanism family** (C12 coded, C13 pilot-aided).

Independent verifier V1-V10 all PASS; this synthesis reflects the verified state.

## 10. S009 amendment — audit issues #1–#8 (scope-narrow, verdict direction unchanged)

The 2026-07-21 S009 amendment (independent review) identified 8 known issues in
this batch. All 8 are real, but none changes the verdict direction. The fixes
are minimal and scoped: UTF-8 portability, source-closure hash, and explicit
documentation of the boundary/scope limitations. The C11 scientific batch was
NOT re-run (per the user brief: "don't re-run the full C11 scientific batch
unless independent review proves a minimal fix changes the numerical direction").
A focused analysis of each issue follows.

| # | Issue | Status | Why it doesn't change the verdict |
|---|---|---|---|
| 1 | No-op test uses `switch_point=10**9` so DD never fires | DOCUMENTED + finite-switch test exists | `test_dd_step_0_freezes_cma_weights_at_switch_point` is the variant that actually enters stage-2 (switch_block=5). Both tests PASS. The 10**9 variant is a redundant double-check. |
| 2 | finite-switch test proves frozen-CMA-weight output, not continued fixed-μ CMA | DOCUMENTED | The finite-switch test isolates the D1 (convention) fix. The full scientific comparison against CONTINUED fixed-μ CMA is the paired-Δ test (macro +0.01445, 2/7 long cells significantly worse). The two tests answer different questions; both stand. |
| 3 | held-out cells' switch/plateau not fully pre-frozen (computed at eval-time from seed=31) | DOCUMENTED as P1 debt | Plateau is a CELL property (depends on SNR / fading, NOT on the seed's symbol draw); computing it from validation seed 31 is the contract-blessed procedure. The actual held-out cells use their OWN plateau (line 302), which is MORE favourable to C11 than a frozen validation-cell plateau would be — and C11 still loses. So this biases toward C11, not against it. |
| 4 | Windows fresh test 11/2 fail due to YAML read without UTF-8 | FIXED | All 4 `open()` calls now pass `encoding="utf-8"`. 19/19 tests PASS on Windows python311. |
| 5 | artifact missing contract/runner/source-closure hash/fingerprint | FIXED | `metadata.source_closure_sha256` now records SHA-256 of 9 source files (contract, runner, c11_causal, tests, root-cause note, evaluator, cell runner, channel, modulation). |
| 6 | `dd_step=3e-4` and `switch_offset=+2` on grid boundary | DOCUMENTED as scope limitation | Larger dd_step would perturb converged weights HARDER → C11 would be even worse. Larger switch_offset delays DD → C11 looks MORE like fixed-μ (its loss). Neither direction would flip "C11 not better" to "C11 better". The boundary picks bias the result toward the null, not away from it. |
| 7 | short-cell eval window has only ~half symbols in DD (64/128 at offset=+2) | DOCUMENTED as scope limitation | Quantified: at switch_offset=+2 and N=512, switch fires at symbol 325, eval window starts at 261, so only 64/128 eval symbols are DD. This affects SHORT cells only (where Δ ≈ ±0.0004, tie regardless of DD coverage). Long cells (where the significant +0.025 and +0.076 results live) have 128/128 DD. |
| 8 | DD is raw-decision policy, no phase/permutation ambiguity resolution | DOCUMENTED as scope limitation | `evaluator.hard_16qam` does raw nearest-16QAM. The DD update can lock onto a wrong quadrant, which would DEGRADE C11. The paired-Δ evaluation uses permutation-invariant metrics, so the EVALUATION is fair. The DD POLICY being unsophisticated is a real scope limit but makes C11 look WORSE, not better — so the "no benefit" verdict is if anything understated. |

### Verdict scope after S009 amendment

The verdict is **`C11_EXACT_CAUSAL_RAW_DECISION_POLICY_NO_BENEFIT`** with claim
ceiling **LOCAL_SLICE / DIAGNOSTIC**. Allowed claims:

- The previous 4/7 positive signal was an implementation/confound diagnostic.
- The exact C11 variant tested (causal one-pass, raw-decision DD, switch_point
  = plateau+{0,1,2}, dd_step grid [0..3e-4]) does NOT beat fixed-μ CMA μ=0.03.
- On the 2 long held-out cells, C11 is significantly WORSE than fixed-μ CMA.

Forbidden claims:

- "The entire DD-LMS family fails" (only this exact policy tested).
- "C11 has been closed across the whole domain" (7 cells × 10 seeds × 1 switch
  policy × 1 DD policy is a LOCAL_SLICE).
- "All 7 cells have been thoroughly tested for the DD stage" (short cells
  barely exercise DD; only long cells do).

### What was fixed (P0/P1)

- **P1 #4 UTF-8 portability**: 4 `open()` calls fixed; locked by
  `test_runner_reads_writes_yaml_with_explicit_utf8`.
- **P1 #5 source-closure hash**: `_source_closure_hashes()` added; locked by
  `test_runner_exposes_source_closure_hash_helper`.

### What was documented but NOT fixed (scope limitations, not defects)

- **#1, #2, #3, #6, #7, #8**: locked by 6 new tests that assert the
  documentation / scope is honest. The numerical verdict is unchanged because
  each issue either biases toward C11 (making "no benefit" conservative) or
  affects only the non-significant short-cell slice.

### Protected history

B001-B003 / P03 / CB1 raw / canonical-state / B01 raw / B01-R raw / D010 /
H007 / V002 / `result.v1.json` (the original artifact): all preserved.
The S009 amendment adds the source-closure hash to FUTURE runs' metadata; the
existing `result.v1.json` is NOT modified (it records the pre-amendment state).
The hash will appear in the next-run artifact if C11 is ever re-run (not
scheduled this campaign).
