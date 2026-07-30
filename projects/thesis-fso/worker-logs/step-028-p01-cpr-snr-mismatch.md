# step-028 — P01 CPR Selector SNR-Mismatch Robustness (Independent Executor)

> Task: T028-p01-cpr-selector-snr-mismatch-robustness (Package P01)
> Source: S003 / D039 campaign authorization; brief at
> `.sessions/2026-07-23-research-direction-lab-longitudinal-test/T028-p01-cpr-selector-snr-mismatch-robustness.md`
> Worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
> Python (verified against anchor provenance 3.11.9): `/c/Users/zzt/scoop/apps/python311/current/python`.
  The torch venv `Scripts/python.exe` lacks `pydantic` and is Python 3.14 → NOT used.
> Date: 2026-07-30
> TERMINAL VERDICT (recommendation): **NO_DIAGNOSTIC_SIGNAL** (with a documented
  conditional sub-population signal — see §6).

## 0. Mission recap

Diagnose whether the **frozen DA/NDA CPR selector** (method.tex already written, anchor
`ccisp_family1_selector_a_30seed.json`) suffers **substantial harm** when the receiver
holds a biased nominal SNR `γ̂_dB = γ_true_dB + δ` instead of the true SNR. The original
selector's `decide(rx, gamma_db, gamma_lin)` consumes nominal γ in two places:
stage-1 CV boundary `cv_awgn_theory(gamma_db)`; stage-2 noise subtraction
`1/(2*gamma_lin)` + γ_eff vs 13 dB. Both are corrupted by a biased γ̂.

New files only (no edits to common/, params.py, or original selector):
- `projects/simulation/explore/nda-awgn-tracking-sandbox/_p01_cpr_snr_mismatch_probe.py`
- `projects/simulation/explore/nda-awgn-tracking-sandbox/_p01_adapter_and_candidates.py`
- `projects/simulation/explore/nda-awgn-tracking-sandbox/_p01_repro_check.py`
- `projects/simulation/explore/nda-awgn-tracking-sandbox/_p01_smoke_check.py`
- `projects/simulation/explore/nda-awgn-tracking-sandbox/_p01_estimator_calib.py`
- `projects/simulation/explore/nda-awgn-tracking-sandbox/_p01_phaseA_dev.py`
- `projects/simulation/explore/nda-awgn-tracking-sandbox/_p01_phaseBC.py`
- artifacts: `projects/simulation/results/p01_cpr_snr_mismatch/{phaseA_dev.json,phaseBC_heldout.json}`

## 1. CRITERION FREEZE — written BEFORE running any test cell (T028 §2.1, trap #7)

**Substantial harm (frozen):** In cells where anchor common-768 gain ≥ 0.5 dB
(weak/moderate/strong @ 5–13 dB), mean paired-seed gain drops ≥ 0.3 dB vs δ=0
AND paired Student-t 95% CI upper bound < 0 dB.
- `Δgain(δ)` = per-seed `10·log10(nda_common768/selected_common768)(δ) − ...(0)`.
- harm ⇔ `mean(Δgain(δ)) ≤ −0.3 dB` AND `CI95_high(Δgain(δ)) < 0`.
- Threshold rationale: 0.3 dB ≈ 25–37% of the original 0.8–1.5 dB scale → clearly
  above noise, not noise-level. Only δ ∈ {±1,±2,±3} dB judged.
- Main cells = 15: weak/moderate/strong × {5,7,9,11,13} dB.

**Phase C MDE (frozen before C):** candidate must beat adapter by mean ≥ 0.15 dB
(~10–20% of gain scale) AND paired CI_low > 0, pooled across all main cells on
held-out seeds. (Brief does not fix MDE; 0.15 dB chosen as a principled fraction of
the 0.3 dB harm threshold. Sensitivity: even at MDE=0.10 the verdict logic holds —
see §6.)

**Seed discipline (frozen):** dev = seed_index 0–9 (anchor subset, reproduction +
criterion exploration). fresh held-out test = seed_index 30–49. dev ≠ final test.

## 2. Environment & reproduction evidence

- Channel: `generate_shared_realization_apsk` (TL-13 shared). seed formula
  `ws = P.SEED_TURB0 + seed_index*400 + b`, SEED_TURB0=2000, N_WINDOWS=400.
- common-768: pilot at `np.arange(0,256,4)`=64, data = 192 sym × 4 bit = 768 bit/window.

### 2.1 Reproduction (Phase A.1) — `_p01_repro_check.py`

`run_case_mismatch(scene, γ_true, δ=0, seed)` mirrors
`run_ccisp_family1_selector_a_30seed.py::run_case` line-for-line for δ=0. Ran 3 scenes ×
{5,9,13,25} dB × seeds 0–9 = **120 cells**.

**Result: 120 / 120 EXACT match** on `selected_errors`, `n_select_da`, `n_select_nda`,
`fixed_nda_errors`, `fixed_da_errors`, `lower_count_bound_errors`,
`true_oracle_errors`, `true_oracle_bits`. Zero mismatches. Per-cell ≈ 0.8 s.

## 3. Phase A — problem-bearing probe

### 3.1 Semantic smoke (Phase A.4) — `_p01_smoke_check.py` — PASS
- **multidelta fast-path equivalence**: 7/7 δ values exact-match `run_case_mismatch`.
- **δ=0 identity**: selection error rate vs δ=0 baseline = 0; gain retention = 0 ✓.
- **δ→+∞**: at γ̂_dB ≥ 17 dB stage-2 `γ̂_dB+10log10(h)` exceeds 13 → ALL windows NDA
  (400/400) ✓. **δ→−∞**: stage-1 CV threshold rises → almost all windows NDA ✓.
- **IMPORTANT GENUINE PROPERTY (not a bug)**: branch occupancy is NON-monotone in δ.
  DA occupancy peaks around δ≈+1..+2 then falls. Cause (verified analytically): the two
  stages respond oppositely to rising γ̂ — stage-1 threshold FALLS (fewer NDA via
  stage-1) while stage-2 γ_eff RISES (more NDA via stage-2). At low SNR positive bias
  net-pushes DA; at high SNR it net-pushes NDA. The brief's "δ→+∞ → NDA" holds at the
  extreme endpoint; the intermediate curve is genuinely non-monotone across all cells.

### 3.2 Dev mismatch scan (Phase A.5) — `_p01_phaseA_dev.py` → `phaseA_dev.json`
15 main cells × 7 δ × dev seeds 0–9. Anchor (δ=0) common-768 gains reproduce the brief's
head tuple (weak@9 +1.53, weak@7 +1.37, moderate@9 +1.01, etc.).

**PROBLEM PRESENT. 5 substantial-harm cells (all at the δ=±3 extremes):**

| cell | δ | gain(δ) | Δgain vs δ=0 | CI95 | 
|---|---|---|---|---|
| weak@5dB | −3 | +0.54 | **−0.339** | [−0.365, −0.313] |
| weak@7dB | −3 | +0.98 | **−0.393** | [−0.438, −0.347] |
| weak@9dB | −3 | +1.20 | **−0.324** | [−0.368, −0.279] |
| weak@11dB | +3 | +0.54 | **−0.704** | [−0.764, −0.644] |
| moderate@13dB | +3 | +0.47 | **−0.344** | [−0.499, −0.189] |

Mechanism: δ=−3 harms low-SNR high-gain cells (stage-2 noise subtraction
`1/(2γ_lin)` blows up at low γ_lin → over-suppresses DA → too much NDA where DA helps).
δ=+3 harms higher-SNR cells (stage-2 `γ̂_dB+10log10(h)` crosses 13 → forces NDA where DA
helps). At δ=+1/+2 the selector slightly GAINS (positive bias at low SNR pushes more DA).
Harm is asymmetric and concentrated at the extremes.

### 3.3 Held-out Phase A reproduction (seeds 30–49, from `phaseBC_heldout.json` orig method)
All 5 harm cells reproduce on fresh held-out seeds (weak@11dB δ=+3 even worse: −0.601 dB,
CI [−0.682, −0.521]). Problem confirmed real, not a dev artifact. → proceed to Phase B.

## 4. Phase B — conventional adapter

### 4.1 Estimator calibration — `_p01_estimator_calib.py`
Three receiver-visible pilot SNR estimators measured against true γ (estimator never sees
true γ):
- **coherent** (`h=|mean(e)|²`, `σ²=mean|e−mean(e)|²`): bias −4 to −11 dB (fading eats
  the coherent average).
- **M2M4 moments** (`σ²=(M4−M2²)/(2M2)`): bias −4 to −11 dB.
- **noncoherent block-wise** (`h_blk=mean|e|²`, `σ²=−h_blk+√(h_blk²+Var)`): bias **−1.7
  to −3.6 dB** — least biased. Chosen as the primary adapter.

**Key finding: no receiver-visible SNR estimator is unbiased under optical turbulence
fading.** All carry a systematic negative bias comparable to or larger than the
δ-mismatch being studied. This is the inherent limit and is part of the honest result.

### 4.2 Adapter result — `_p01_phaseBC.py` → `phaseBC_heldout.json` (seeds 30–49)
Adapter = noncoherent-block pilot estimator + original `decide` rule. δ-INVARIANT by
construction (ignores γ̂), so it removes the δ-dependence entirely.

| harm cell | δ | orig(δ-mismatched) | adapter | adapter Δ vs δ=0 base | resolved? |
|---|---|---|---|---|---|
| weak@5dB | −3 | +0.560 | +0.746 | −0.172 | YES |
| weak@7dB | −3 | +0.993 | +1.113 | −0.268 | YES |
| weak@9dB | −3 | +1.239 | +1.241 | **−0.323** | **NO** |
| weak@11dB | +3 | +0.573 | +0.957 | −0.217 | YES |
| moderate@13dB | +3 | +0.504 | +0.706 | −0.127 | YES |

**Adapter is a net WIN over the δ-mismatched original at every harm cell** (+0.002 to
+0.384 dB) and eliminates δ-dependence. BUT it does NOT fully resolve the strict harm
criterion: weak@9dB sits at −0.323 dB because the adapter's own ≈−2.5 dB estimation bias
is a fixed floor it pays at every cell (range −0.05 to −0.32 dB across all main cells;
only weak@9dB crosses −0.3). → residual harm → proceed to Phase C.

(Sanity: oracle_true ≡ δ=0 original at every cell — 0 mismatches. The δ=0 original
selector already achieves the true-gamma oracle bound.)

## 5. Phase C — robust candidates vs adapter (held-out seeds 30–49)

5 mechanism-different candidates, each receiver-visible only (verified: every `A.decide`
call uses pilot estimate or biased γ̂, never true γ; true γ only in the oracle bound):
1. `cand_uncertainty` — blend nominal γ̂ with pilot est, guard stage-2.
2. `cand_minimax` — worst-case-over-[γ̂−2,γ̂+2] branch, fallback to pilot est.
3. `cand_conf_gate` — near-13dB-threshold fallback to pilot est.
4. `cand_rank` — γ-magnitude-FREE stage-1 boundary at fixed reference SNR (9 dB) +
   pilot-est stage-2.
5. `cand_hysteresis` — EMA-smoothed γ̂ then original decide.

**Pooled paired candidate-vs-adapter (n=300 cell-seed pairs, δ=0 rows):**

| candidate | mean Δ vs adapter | CI95 | stable beat (≥0.15 & CI_low>0)? |
|---|---|---|---|
| cand_uncertainty | +0.073 | [+0.066, +0.080] | no |
| cand_minimax | +0.061 | [+0.055, +0.066] | no |
| cand_conf_gate | +0.112 | [+0.101, +0.123] | no |
| **cand_rank** | **+0.136** | **[+0.121, +0.151]** | **no** (CI_low>0 but mean<0.15) |
| cand_hysteresis | +0.129 | [+0.118, +0.140] | no |

All 5 statistically beat the adapter (CI_low>0) but NONE clear MDE=0.15 dB pooled.

**Per-cell cand_rank vs adapter** reveals the signal is concentrated:

| cell | adapter | cand_rank | Δmean | CI95 | beats by MDE? |
|---|---|---|---|---|---|
| weak@5dB | +0.715 | +1.029 | +0.385 | [+0.359,+0.411] | YES |
| weak@7dB | +1.163 | +1.500 | +0.432 | [+0.406,+0.458] | YES |
| weak@9dB | +1.264 | +1.526 | +0.323 | [+0.289,+0.357] | YES |
| weak@11dB | +1.318 | +1.342 | +0.111 | [+0.077,+0.144] | no |
| weak@13dB | +0.324 | +0.329 | +0.014 | [−0.008,+0.036] | no (CI crosses 0) |
| moderate@* | … | … | +0.05 to +0.12 | all CI>0 | no |
| strong@* | … | … | +0.03 to +0.09 | all CI>0 | no |

cand_rank's advantage is LARGE and STABLE at weak-turbulence low-SNR (the sub-population
where the original stage-1 boundary is most miscalibrated) but small/absent elsewhere.

**cand_rank reference-SNR ablation** (ref ∈ {7,9,11} dB, seeds 30–39): the weak/low-SNR
win is ROBUST to the reference choice (grows with ref; not cherry-picked). cand_rank uses
a single fixed design constant + the same pilot estimator as the adapter — no extra info,
no per-cell tuning, no oracle.

## 6. Terminal verdict: **NO_DIAGNOSTIC_SIGNAL** (with documented conditional signal)

**Reasoning (strict brief criterion):**
- Phase A: PROBLEM PRESENT (5 harm cells, reproduced on held-out).
- Phase B: adapter does NOT fully resolve (weak@9dB −0.323 dB bias floor) → Phase C.
- Phase C: no candidate STABLY beats the adapter by ≥MDE=0.15 dB pooled on held-out
  (cand_rank closest at +0.136, CI_high grazes 0.151). → **NO_DIAGNOSTIC_SIGNAL**.

**Documented conditional finding (not a METHOD_SIGNAL, a seed for future work):**
`cand_rank` (γ-magnitude-free stage-1 boundary) produces a large, stable,
mechanism-distinct improvement (+0.32 to +0.43 dB, CI>0) specifically at
**weak-turbulence low-SNR cells** — exactly where Phase A harm is worst and where the
adapter's bias floor bites. It does not constitute a uniform stable win over the
conventional adapter, so it is not promoted to a diagnostic method, but the
sub-population signal is real and robust to the reference-SNR design constant.

**Sensitivity of verdict to MDE:** at MDE=0.10 dB, cand_rank WOULD clear the pooled bar
(mean +0.136, CI_low +0.121). The verdict hinges on the MDE choice; I froze 0.15 dB
prereq (a conservative fraction of the 0.3 dB harm threshold) and the strict reading
gives NO_DIAGNOSTIC_SIGNAL. The controller may re-adjudicate if it judges 0.10 dB more
appropriate; the underlying numbers are in the artifacts either way.

**Net deployment takeaway:** the conventional pilot-SNR adapter is the practical
recommendation — it is δ-invariant (robust to the entire ±3 dB mismatch range) and a net
win over the mismatched original at every harm cell, at the cost of a small fixed bias
(≤0.32 dB). The original selector is NOT robust to ±3 dB SNR mismatch on its own.

## 7. Key numbers (for controller relay)

Anchor (δ=0) common-768 gains, held-out: weak@9 +1.56, weak@7 +1.38, weak@5 +0.92,
weak@11 +1.18; moderate@9 +1.03, moderate@7 +0.82; strong@9 +0.79.

Worst harm (orig, held-out): weak@11dB δ=+3 → +0.57 dB (Δ −0.60), weak@7dB δ=−3 → +0.99
(Δ −0.39).

Adapter at harm cells (held-out): +0.75/+1.11/+1.24/+0.96/+0.71 dB (resolves 4/5; weak@9
bias floor −0.32).

Best candidate cand_rank at harm cells: +1.03/+1.50/+1.53/+1.34/+0.75 dB — beats adapter
+0.32 to +0.43 dB at weak@5/7/9 but not elsewhere.

No EXECUTION_INVALID blockers. All discipline items satisfied: reproduction exact,
criterion frozen pre-test, true γ never in decide (only signal-gen + offline BER +
oracle bound), shared channel, dev/test seed isolation, paired Student-t CI matching
anchor `ci_t`.
