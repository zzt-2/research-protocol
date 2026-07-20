# CB1 Modulation-Generic Closure — Baseline Atlas v1 Synthesis

**Campaign:** `science-scout-2026-07-20.dual-pol-osl`
**Scope:** CB1 modulation-generic closure — 16QAM axis unblocked (was INFRASTRUCTURE_BLOCKED in P03 Stage A).
**Mode:** SCOUT_BASELINE_DIAGNOSTIC_ONLY (no ML trained; baseline only).
**Date:** 2026-07-20.
**Raw artifact:** `artifacts/cb1-baseline-atlas-v1.json`.

---

## 1. Scientific question

P03 Stage A found **0/11 QPSK cells** with measurable headroom against the strongest legal non-ML baseline (LOCAL_NEGATIVE everywhere). The 16QAM axis was INFRASTRUCTURE_BLOCKED because the P03 frozen source closure hard-coded QPSK. CB1 unblocks 16QAM. **Does 16QAM have headroom where QPSK did not?**

Mechanistic prior (D008 Sup-1; `explore/cma-fade-divergence/ber_16qam_vs_fg.py:19-23`): 16QAM CMA BER is higher than QPSK due to modulus mismatch (R²=1.32 vs the actual multi-ring constellation), suggesting 16QAM may have **more** headroom.

## 2. Identity gate and QPSK regression (mandatory pre-checks)

* **Standard-CMA identity gate (gradient = `Godard-with-z`)**: PASS on every cell (11/11 16QAM cells, 1/1 QPSK anchor).
* **Critical implementation note (anomaly, see §7)**: `common/_cma.py:CMAEqualizer2x2` implements the **scalar-error** gradient (`Δw ∝ (R²−|z|²)·r*`), NOT Godard-with-z. The protected-history runner (`tools/run_b001._default_runner`) obtains Godard-with-z via `prompt013.run_cma_diagnostic(mode='standard')` (`Δw ∝ (R²−|z|²)·z·r*`, prompt013:301-306). To pass the identity gate truthfully, this Atlas re-implements the Godard-with-z blockwise update directly in `cb1_cell_runner.standard_cma_godard_with_z` (Option B in the task brief; Option A would have produced a false identity-gate stamp).
* **Byte-identity check vs prompt013 reference**: my `standard_cma_godard_with_z` produces **max |Δz| = 0.0** on the P03 v1 anchor cell across seeds 11/12/15/20 vs `prompt013.run_cma_diagnostic(mode='standard')`. This is the strongest possible identity evidence — bit-for-bit reproduction of the protected-history CMA.
* **QPSK anchor regression** (P03 v1: snr=20 dB, f_g=30 Hz, sop=4e-6, N=512, seed=11): **PI-SER = 0.000000**, fixed-label SER = 0.000000, oracle PI-SER = 0.000000. **PASS** — reproduces P03 v1 exactly. Wiring is correct.

## 3. Baseline lattice (all same-information, no ML)

Mirrors P03 Stage A `strongest_legal_non_ml_baseline`:

| Comparator | Information | Role |
|---|---|---|
| nearest-16QAM (`hard_16qam`) | CSI_NONE z only | **Go baseline** for any future ML (strongest legal non-ML) |
| blind affine (one-step ridge fit to z-derived 16QAM pseudo-labels) | CSI_NONE z + calibration-slice pseudo-labels | Strongest preregistered same-information simple comparator |
| oracle affine (one-step ridge fit to TX truth) | calibration TX truth | **Kill tool / scoring-only upper bound** (FR-21); defines visible headroom; never a Go baseline (FR-25) |

**Visible headroom** = `nearest_pi_ser − oracle_pi_ser` (the gap a learned detector could plausibly close).
**Simple gain** = `nearest_pi_ser − min(nearest_pi_ser, blind_pi_ser)` (what the same-information simple comparator already captures).

16QAM PI-SER evaluator: 4 quadrant rotations {+1,+j,−1,−j} (16QAM 90° rotational symmetry) × 2! stream permutation = 8 candidates, min over (BER, SER). BER per-bit via `qam16_demod`; SER per-symbol. Pre-registered MDE = 0.005 per symbol. Rule-of-three 95% upper bound for zero-error cells.

## 4. Per-cell results (11 cells × 10 paired seeds)

| cell_id | snr (dB) | f_g (Hz) | sop_rate | N | nearest PI-SER | blind PI-SER | oracle PI-SER | visible headroom | decision_class |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 16qam-snr05-nominal-short | 5 | 30 | 4e-6 | 512 | 0.6621 | 0.6797 | 0.6887 | 0.0000 | LOCAL_NEGATIVE |
| 16qam-snr10-nominal-short | 10 | 30 | 4e-6 | 512 | 0.4875 | 0.4828 | 0.4164 | 0.0711 | **ADVANCE** |
| 16qam-snr15-nominal-short | 15 | 30 | 4e-6 | 512 | 0.3645 | 0.3543 | 0.1437 | 0.2207 | **ADVANCE** |
| 16qam-snr20-nominal-short | 20 | 30 | 4e-6 | 512 | 0.3332 | 0.3148 | 0.0223 | 0.3109 | **ADVANCE** |
| 16qam-snr25-nominal-short | 25 | 30 | 4e-6 | 512 | 0.3328 | 0.3004 | 0.0000 | **0.3328** | **ADVANCE** |
| 16qam-snr20-fg100-short | 20 | 100 | 4e-6 | 512 | 0.3344 | 0.3164 | 0.0215 | 0.3129 | **ADVANCE** |
| 16qam-snr20-fg1000-short | 20 | 1000 | 4e-6 | 512 | 0.3410 | 0.3293 | 0.0199 | 0.3211 | **ADVANCE** |
| 16qam-snr20-sop40e-short | 20 | 30 | 4e-5 | 512 | 0.3328 | 0.3133 | 0.0223 | 0.3105 | **ADVANCE** |
| 16qam-snr10-fg100-long | 10 | 100 | 4e-6 | 8192 | 0.4273 | 0.4023 | 0.3727 | 0.0547 | **ADVANCE** |
| 16qam-snr15-fg1000-long | 15 | 1000 | 4e-6 | 8192 | 0.3219 | 0.3238 | 0.1742 | 0.1477 | NON_DECISIVE |
| 16qam-snr20-nominal-long | 20 | 30 | 4e-6 | 8192 | 0.3055 | 0.3145 | 0.0730 | 0.2324 | NON_DECISIVE |

* 10/11 cells have visible headroom ≥ MDE (0.005). Only the snr=5 cell is LOCAL_NEGATIVE (oracle affine cannot help when AWGN dominates — oracle PI-SER = 0.69, worse than nearest).
* 8/11 cells ADVANCE (visible headroom ≥ MDE AND blind affine captures some).
* 2/11 cells NON_DECISIVE (long cells: visible headroom large but blind affine does NOT capture — `blind_pi_ser > nearest_pi_ser`, i.e., the simple comparator actively hurts on under-converged z; no evidence a same-information simple method can close the gap, so the schema requires NON_DECISIVE rather than ADVANCE).
* 1/11 LOCAL_NEGATIVE (snr=5).
* 0/11 DIVERGENT (no NaN / weight-norm explosions; CMA either converges or collapses to inner ring — see §5).

## 5. Mechanism — bimodal CMA convergence failure on 16QAM

Per-seed breakdown of the strongest cell (`16qam-snr25-nominal-short`, all 10 seeds):

| seed | nearest PI-SER | oracle PI-SER |
|---:|---:|---:|
| 11 | 0.0000 | 0.0000 |
| 12 | 0.7734 | 0.0000 |
| 13 | 0.0000 | 0.0000 |
| 14 | 0.0000 | 0.0000 |
| 15 | 0.0000 | 0.0000 |
| 16 | 0.7070 | 0.0000 |
| 17 | 0.3438 | 0.0000 |
| 18 | 0.0000 | 0.0000 |
| 19 | 0.7266 | 0.0000 |
| 20 | 0.7773 | 0.0000 |

**The headroom is bimodal and per-seed**: 5/10 seeds the standard-CMA converges to PI-SER ≈ 0; 4/10 seeds it collapses to PI-SER ≈ 0.7+; 1/10 partial. Direct diagnosis on seed=12: `E[|z|²]=0.16` (vs the CMA target R²=1.32), and the hard decisions hit only the 4 inner-ring points (|s|²=0.2 each), completely missing the 12 outer points. This is the classic **"CMA collapses to the inner ring"** local-minimum failure mode for non-constant-modulus constellations (the Godard cost surface has local minima for 16QAM, and certain channel realizations drive the equalizer into them).

The oracle affine, fit to TX truth on a 50%-of-eval-window calibration slice, perfectly recovers all 10 collapsed seeds at snr=25 (`oracle PI-SER = 0.0000` on every seed). The "headroom" a learned detector could close is precisely: **detect when standard-CMA has collapsed and apply a corrective affine map**.

This is the canonical U19 residual-aware detection signal — the CMA trace features (cm_error, output_power, update_norm) carry clear signatures of collapse (e.g., `cm_error` stays ~1.0 instead of decaying, `E[|z|²]` is far below R²), so a learned detector trained on those features should in principle be able to flag the collapse and trigger re-convergence or fallback.

## 6. Verdict ladder (per P03 schema; claim ceilings per campaign-contract.v1.yaml)

* **CELL**: 10/11 cells show visible headroom ≥ MDE; 8 ADVANCE, 2 NON_DECISIVE, 1 LOCAL_NEGATIVE. Strongest cell `16qam-snr25-nominal-short` reaches visible headroom = 0.3328 (66× MDE).
* **SLICE (16QAM representative subdomain)**: **LOCAL_HEADROOM_FOUND**. Unambiguous: 8 ADVANCE cells span the SNR sweep (10/15/20/25 dB), the dynamics sweep (f_g=30/100/1000, sop=4e-6/4e-5), and one long cell (snr=10, f_g=100, N=8192). Visible headroom is consistently 0.05–0.33, far above MDE=0.005. Sensitivity is PASS (10 paired seeds per cell; n_error_events > 0 on every ADVANCE cell so rule-of-three is not the binding constraint).
* **DOMAIN**: UNRESOLVED — per claim ceiling, DOMAIN exit requires all blocked axes closed (only 16QAM is closed here; receiver-estimated CSI and soft/coded output remain INFRASTRUCTURE_BLOCKED) AND a scope certificate. Not requested in this baseline-only task.
* **CANDIDATE / FAMILY**: OPEN — per claim ceilings, requires mechanism proof and legal-comparator adjudication. Not in scope for this baseline Atlas.

**ML Scout trigger**: **YES** — the campaign contract authorizes `batch_ML_scout_conditional_on_headroom` only if headroom > MDE on some cell. 10/11 cells meet that bar. The next step (out of scope for this baseline-only task) would be a Stage B ML Scout batch training a residual-aware detector on the CMA trace features, evaluated against nearest-16QAM as the Go baseline. This Atlas provides the preregistered target (visible headroom up to 0.33) and the mechanism (collapse detection).

## 7. Mechanistic reading vs prior

* **Prior**: "16QAM CMA BER is higher than QPSK due to modulus mismatch, suggesting 16QAM may have MORE headroom." (D008 Sup-1)
* **Confirmed on the runnable domain, but with a sharper mechanism than the prior stated.** 16QAM PI-SER is dramatically higher than QPSK (P03 v1 QPSK anchor: PI-SER = 0.000000; 16QAM snr=20 short: PI-SER = 0.3332). And 16QAM headroom is correspondingly much larger (P03 QPSK: 0/11 cells with headroom; 16QAM: 10/11 cells with headroom up to 0.33).
* **Sharper mechanism**: the modulus-mismatch story is correct but incomplete. The dominant driver is not uniform modulus-mismatch noise — it is **bimodal per-seed CMA convergence failure** (collapse to the inner ring on ~40-50% of seeds at high SNR). The modulus mismatch creates a Godard cost surface with local minima for 16QAM that QPSK (constant modulus) does not have; certain channel realizations drive CMA into those minima. The oracle affine can perfectly undo the collapse given TX-truth calibration, proving the information is present in the receiver-visible z — it just needs a smarter (learned) detector to recover it.
* **Where headroom lives**: SNR region 10–25 dB (waterfall-to-high). At snr=5, AWGN dominates and even the oracle affine cannot help (oracle PI-SER = 0.69 > nearest). At snr=10–25, the collapse mechanism dominates and headroom is 0.05–0.33. Dynamics (f_g, sop) and observation length (N) are second-order: the snr=20 short cells across f_g=30/100/1000 and sop=4e-6/4e-5 all cluster at headroom ≈ 0.31, suggesting the collapse is driven by the initial channel realization (seed) and the CMA's local-minumum structure, not by tracking dynamics.
* **Long cells are more subtle**: at N=8192 the CMA has more time to converge, so the collapse rate is lower (4/10 vs 5/10 at N=512), but when it does collapse the affine fit on a longer under-converged z is less effective — hence the 2 NON_DECISIVE long cells where blind affine slightly hurts.

## 8. Anomalies, divergences, scope

* **Anomaly (resolved, see §2)**: `common/_cma.py:CMAEqualizer2x2` implements the scalar-error gradient, not Godard-with-z. Using it directly (Option A in the task brief) would have produced a false `gradient == 'Godard-with-z'` identity stamp. Resolved by implementing Godard-with-z directly (`cb1_cell_runner.standard_cma_godard_with_z`), verified byte-identical to the prompt013 reference (max |Δz| = 0.0). This is the Option B fallback explicitly anticipated by the task brief. **Recommendation**: consider clarifying `_cma.py`'s docstring to note it implements the scalar-error variant, or adding a `gradient='Godard-with-z'` variant to `_cma.py`, so future CB1-style work doesn't re-trip this. (Out of scope to modify here — `_cma.py` and `_modulation.py` are frozen.)
* **Divergences**: 0/110 cell-seed runs hit the formal divergence criteria (no NaN, no weight-norm explosion past 10× init). However, the "collapse to inner ring" failure mode is a **soft divergence** that does NOT trip the `_cma.py` divergence thresholds (the weight norm stays ~1.4 ≈ init, |z| stays < 1e3). This is reported as high PI-SER, not as DIVERGENT. This is honest: the formal divergence detector does not catch this failure mode, which is itself a finding (the divergence criterion may need to include "E[|z|²] far below R²" as a soft-divergence signal — relevant for the U19 detector design).
* **Scope**: full 11-cell × 10-seed sweep ran in 1.4 s wall time (vs 15 min budget) — no scope reduction needed.
* **QPSK regression**: PASS (PI-SER = 0.0 exactly on P03 v1 anchor, identity gate PASS, byte-identical CMA to prompt013).
* **No files modified outside `scout/cb1-modulation-generic-closure/baseline-atlas/`.** P03, canonical-state, portfolio, STATUS, B001-B003, `_modulation.py`, `_cma.py` all untouched.

## 9. Files written

* `baseline-atlas/cb1_evaluator.py` — modulation-aware 16QAM evaluators (reuses P03 `_affine_fit`/`_affine_apply` via read-only import).
* `baseline-atlas/cb1_cell_runner.py` — standard-CMA (Godard-with-z) cell runner, identity gate, per-cell decision schema.
* `baseline-atlas/_run_smoke.py` — driver (QPSK regression + full 16QAM Atlas).
* `baseline-atlas/artifacts/cb1-baseline-atlas-v1.json` — raw per-cell, per-seed results.
* `baseline-atlas/artifacts/cb1-baseline-atlas-v1-synthesis.md` — this file.
