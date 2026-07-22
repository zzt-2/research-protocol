# C12 GMI Soft-Output Scout — Synthesis v1

**Candidate:** C12 (soft_output_collapse_aware_llr)
**Batch:** c12-gmi-soft-output-scout v1
**Mechanism / metric:** SOFT-OUTPUT / GMI (information-theoretic mutual information) — distinct from C04/C09/C11 (hard-decision / PI-SER).
**Claim ceiling:** LOCAL_SLICE / DIAGNOSTIC
**Status:** EXECUTED (6 cells × 6 seeds, 3.8 s total wall time)

---

## 1. Scientific question

On the SAME fixed-μ CMA z-stream (Godard-with-z, μ=0.03, 11 taps, block=64, R²=1.32), does a **collapse-aware soft demapper** that models the 16QAM residual as a healthy/collapsed Gaussian **mixture** recover GMI on collapsed cells relative to a **standard max-log** soft demapper (single-Gaussian residual) — and does the **TX-truth oracle** soft demapper show headroom above both?

## 2. Semantic smoke — PASS (all 3 frozen checks)

| check | result |
|---|---|
| clean cell (snr25) standard GMI > 3.0 | **3.987** ✓ |
| collapsed cell (snr05) standard GMI notably lower | **0.471** (3.52 below clean) ✓ |
| oracle ≥ standard on both smoke cells | ✓ |

**Interpretation:** the soft-output evaluator is non-degenerate. The collapse DOES degrade soft-output mutual information dramatically (3.99 → 0.47 GMI on the worst cell). The question is whether that loss is *recoverable by the demapper's noise model*.

## 3. GMI table (histogram GMI, bits/symbol, mean over 6 seeds; ceiling = 4.0)

| cell | standard | mixture | oracle | Δ(mix−std) | Δ(ora−std) | rec |
|---|---|---|---|---|---|---|
| snr05-nominal-short  | 1.529 | 1.536 | 1.529 | +0.008 | +0.000 | — |
| snr15-nominal-short  | 3.373 | 3.414 | 3.371 | +0.042 | −0.001 | −30.5 |
| snr20-nominal-short  | 3.815 | 3.834 | 3.815 | +0.019 | +0.000 | — |
| snr25-nominal-short  | 3.985 | 3.988 | 3.988 | +0.003 | +0.003 | 1.00 |
| snr20-fg100-short    | 3.812 | 3.835 | 3.812 | +0.022 | +0.000 | — |
| snr15-fg1000-long    | 3.136 | 3.158 | 3.135 | +0.022 | −0.002 | −11.3 |

## 4. Macro adjudication (paired bootstrap, 36 cell×seed points)

| statistic | value | 95% CI | frac > 0 |
|---|---|---|---|
| **Δ(oracle − standard)** | **−0.0001** bits/sym | **[−0.0024, +0.0019]** | **0.08** |
| Δ(mixture − standard) | +0.019 bits/sym | [+0.008, +0.031] | 0.53 |
| macro recovery fraction | 1.00 | — | (only 1 cell has oracle headroom > 1e-6) |

## 5. Verdict — MECHANISM NEGATIVE for the soft-demapper premise

**The C12 collapse-aware soft demapper does NOT recover GMI on collapsed cells, because there is no soft-output headroom to recover.** The decisive evidence:

### 5a. Oracle headroom is zero (the Kill bound kills C12)
The truth-conditioned oracle soft demapper is statistically **indistinguishable** from the standard blind-variance max-log demapper: Δ(oracle − standard) = −0.0001, CI straddles zero, and only **8%** of (cell,seed) pairs show oracle > standard. On 5 of 6 cells the oracle Δ is exactly 0.0 to 3 decimals. **A perfect noise model recovers nothing** — the achievable soft-output ceiling on the CMA z-stream is already reached by the standard demapper.

This holds even though the oracle uses a **very different** noise variance. Direct measurement on the collapsed cell (snr05): the truth-conditioned variance is **2–11× larger** than the blind `z_calib−hard_16qam(z_calib)` variance (oracle_s2/blind_s2 = 11.3, 2.4, 11.1 across seeds), yet the GMI is identical (0.471 vs 0.471). **The reason is max-log scale-invariance**: in `LLR_k = min_{bit_k=0}|z−s|²/(2σ²) − min_{bit_k=1}|z−s|²/(2σ²)`, the `1/(2σ²)` is a *common scale* on all symbol distances, so it does not change *which* symbol is closest — it only rescales the LLR magnitude. The histogram GMI (primary, on raw LLR) is scale-robust, so a global variance change is invisible to it.

### 5b. The mixture's small positive Δ is an estimator artifact, not information recovery
The mixture demapper shows Δ(mixture − standard) = +0.019 with a nominally positive CI. But this **cannot be genuine mutual-information recovery**, for three independent reasons:

1. **It exceeds the oracle ceiling.** A blind demapper cannot recover more information than the truth-conditioned bound. Δ(mix−std) = +0.019 ≫ Δ(ora−std) = −0.0001. The mixture gain is *above* the physically-recoverable headroom — a signature of an estimator artifact, not a real signal.
2. **Only 53% of pairs are positive** (barely above a coin flip). A genuine mechanism operating on collapsed cells would concentrate positives there; instead the sign is near-random across all cells.
3. **The analytic GMI (calibration-sensitive) shows the mixture is *worse***: e.g. snr05 analytic std=1.20 vs mix=0.87; fg1000-long std=2.96 vs mix=2.61. The histogram estimator is fooled because the mixture rescales LLR magnitudes, which reshuffles equi-width bin occupancy without adding information; the analytic softplus GMI (which accounts for LLR calibration) correctly penalizes the mixture's miscalibrated LLRs.

### 5c. The mixture fit does not separate a healthy/collapsed mode
The fitted mixture component variances barely differ (e.g. snr05 Re-axis: var = [0.023, 0.042], ratio ~1.8×; snr15: [0.014, 0.017], ratio ~1.2×). The per-real-axis residual after carrier alignment is **not strongly bimodal** at the level the 2-component model can exploit. The "inner-ring collapse" that is dramatic in the *hard-decision* constellation scatter and in PI-SER does not manifest as a separable second mode in the *real-axis residual* that drives per-bit LLRs.

## 6. What this means for C12 and the portfolio

- **The collapse degrades GMI (soft-output MI), but the loss is NOT a demapper-modeling problem.** It is an *equalizer / uncorrected-distortion* loss baked into the CMA z-stream itself: the snr05 cell carries only ~1.5/4.0 bits/symbol of soft information regardless of how the residual noise is modeled. No soft demapper — standard, mixture, or oracle — can recover it.
- **This is a DIFFERENT and cleaner negative than C04/C09/C11.** Those operated on hard decisions / PI-SER and the affine/DD-LMS correction. C12 operates on soft outputs / GMI and closes the soft-output information-theoretic angle: the collapse is not soft-output-recoverable any more than it is hard-output-correctable. This reinforces the portfolio's recurring finding that the **CB1 collapse is a deep Godard-cost / equalizer property**, not a downstream demapper or noise-model deficiency.
- **C12 is not promoted.** The collapse-aware mixture demapper is a *non-mechanism* on this metric: the GMI loss is real but the soft-demapper noise model is not its cause and not its cure.

## 7. Alternative explanations tested (evidence integrity)

| alternative | status |
|---|---|
| evaluator degenerate (smoke) | ruled out — smoke PASS, GMI spans 0.47→3.99 |
| oracle path broken | ruled out — oracle variance differs 2–11× from blind yet is finite & truth-accurate; oracle GMI sane |
| histogram MI biased | cross-checked vs analytic GMI; analytic *confirms* mixture is not better (it is worse) |
| too few samples / seeds | 36 paired points, bootstrap CI computed; conclusion stable; short-cell N=512 (pooled 2-pol) is modest but the *zero oracle headroom* finding is cell-uniform, not a power issue |
| wrong carrier alignment | shared oracle-affine applied identically to all 3 demappers; isolates the noise-model comparison; collapse survives it (snr05 oracle-affine SER=0.875) |
| TX truth leaked into candidate | ruled out — identity gate `test_no_tx_truth_in_standard_or_mixture_signature` PASS; mixture uses only z_calib + alphabet |

## 8. Scope, limits, next

- **Executed:** 6 representative cells × 6 fresh seeds (71–76), disjoint from all prior batches. fixed-μ CMA, dual-pol, oracle-affine alignment, 3 demappers, histogram+analytic GMI.
- **Not executed / blocked:** FEC-coded BER/FER (needs absent FEC codec — commpy/sionna/galois; p04 EXTERNAL subset, deferred); finer mixture models (≥3 components); per-symbol (not per-real-axis) mixture; more cells / longer windows.
- **Claim ceiling:** LOCAL_SLICE / DIAGNOSTIC. The negative is locally robust (zero oracle headroom is cell-uniform) but a wider cell/seed sweep would be needed to *exclude* a soft-output-recoverable regime in some untested corner (e.g. very specific fade realizations). Given zero oracle headroom everywhere tested, such a regime is unlikely.
- **Next (informative, not a method win):** the GMI loss being equalizer-bound redirects attention back to the equalizer itself (the persistent CB1 collapse line) rather than to any output-side soft/coded demapper. The GMI soft-output evaluator built here is a **reusable asset** for any future coded/soft-output claim (it is the p04 HALF_DAY unblock, now implemented and smoke-verified).

## 9. Harvest assessment

- **C12 collapse-aware soft demapper (the candidate):** FAILURE_MECHANISM / LOCAL_SLICE — the mixture demapper does not recover GMI; no durable thesis value as a *method*.
- **Reusable asset — GMI soft-output evaluator:** REUSABLE_ASSET. The max-log + mixture + oracle demappers and the histogram/analytic GMI (pure numpy/scipy, ~250 lines, smoke-verified, 10/10 identity tests) unblock the p03.output.soft-or-coded axis at the GMI level and can support any future soft/coded comparison.
- **Mechanism insight — collapse is not soft-output-recoverable:** EVALUATION_INSIGHT / LOCAL_SLICE. The collapse's GMI loss is equalizer-bound, not demapper-bound; this is independent corroboration (from the information-theoretic side) of the CB1 collapse being a deep Godard-cost property. Consistent with C04/C09/C11 negatives from the hard-decision side.

---

*Artifacts: `artifacts/result.v1.json`. Contract: `batch-contract.v1.yaml`. Code: `src/soft_demap.py`, `src/gmi.py`, `src/run_gmi_scout.py`, `src/test_soft_demap_identity.py` (10/10 identity tests GREEN).*
