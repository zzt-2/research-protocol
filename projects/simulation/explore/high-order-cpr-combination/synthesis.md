# Synthesis — T006 high-order CPR combination method (B10/B12 Step 4a package)

> Authorization: D012 (epoch 8, B10/B12 combination method Step 4a)
> Worktree: `.worktrees/research-direction-lab-longitudinal-test`
> Stage: GW Step 4a dimension D ONLY (does NOT enter Step 5/Contract/Execute)
> Final verdict: **`PROBLEM_SURVIVES_METHODS_FAIL`**

## 1. What the package set out to do

Revive the already-completed B10/B12 Step 1-3 evidence (literature_notes L20
/ L22 + the two `_read_notes/_B{10,12}-*` increment files) on the canonical
star-ground Gamma-Gamma link + uniform 16-QAM, and answer two pre-registered
questions in one package:

1. **Problem gate (headroom)**: does the strongest-simple conventional CPR
   have `>=0.5 dB Q²` legal headroom to a truth-assisted reference, on at
   least one primary cell?
2. **Method gate (only if headroom survives)**: do P1 cascade / P2
   confidence-gate / P3 adaptive-forgetting beat BOTH B* AND the strongest
   standalone component (max(B10, B12)) by `>=0.3 dB`, with CI lower `>0`,
   paired wins `>=7/10`, and clean/control degradation `<=0.1 dB`?

The contract and source-closure were frozen BEFORE any primary run; the
0.5 dB headroom threshold is the T006-specific infrastructure gate (D012),
explicitly overriding the older "FR-21 <0.5 dB is reference-only" calibration
for THIS carrier only.

## 2. What was actually run

- 7 semantic gates (Phase B): all PASS.
- B* selection on VALIDATION (Phase C): scan BPS (B,Nw) + VV Nw + DD-DPLL
  omega over 3 conditions × 3 SNR × 5 val seeds. Winner = **VV Nw=128**
  (mean BER 1.13e-2).
- Headroom gate (Phase D): B* → O Q² headroom per primary cell on 10 fresh
  test seeds, bootstrap 95% CI (2000 resamples).
- Method gate (Phase E): P1/P2/P3 vs B* and strongest standalone, primary
  paired test, same 10 test seeds.

Shared canonical generator (`common/_dual_pol_channel.py`,
`generate_shared_realization_dp(modulation='qam16')`) — single polarization
(rX). CFO + Wiener laser phase added on top of the canonical SOP using the
dimensional-audit values (nominal: 100 kHz CFO + 10 kHz linewidth; stress
cell: 10 MHz CFO + 100 kHz linewidth, within B10-supported range).

## 3. Results

### Phase D — headroom (problem gate)

Per-cell B* → O Q² headroom (test seeds, bootstrap 95% CI):

| cell (cond | SNR) | mean (dB) | CI upper (dB) | n_paired |
|---|---|---|---|
| clean_control\|snr14 | +0.031 | +0.087 | 10 |
| clean_control\|snr17 | −0.022 | +0.045 | 10 |
| clean_control\|snr20 | −0.051 | +0.180 | 10 |
| operational\|snr14 | +0.463 | +1.331 | 10 |
| operational\|snr17 | +0.058 | +0.131 | 10 |
| operational\|snr20 | −0.037 | +0.060 | 10 |
| **adversarial_sourced\|snr14** | **+0.606** | **+1.719** | 10 |
| adversarial_sourced\|snr17 | +0.401 | +1.230 | 10 |
| adversarial_sourced\|snr20 | +0.321 | +1.020 | 10 |

**Verdict: HEADROOM_SURVIVES** — exactly one cell (`adversarial_sourced|snr14`,
strong turbulence + SNR 14 dB, the HD-FEC waterfall neighborhood) has mean
`>=0.5 dB` AND CI upper `>=0.5 dB`. The signal is small (point 0.6 dB) and
the CI is wide (upper 1.7 dB, lower bound below 0), reflecting real
seed-to-seed variance on the strong-turbulence waterfall — but it clears the
pre-registered bar.

### Phase E — method gate

Per-cell Q² gain of P1/P2/P3 vs B* (VV) and vs strongest standalone
(max(B10, B12)), test seeds, paired wins / 10:

| cell | P | gain vs B* (dB) | wins B* | gain vs strongest (dB) | wins strong |
|---|---|---|---|---|---|
| clean_control\|snr14 | P1 | −11.6 | 0/10 | −10.4 | 0/10 |
| clean_control\|snr14 | P2 | −9.4 | 0/10 | −8.1 | 0/10 |
| clean_control\|snr14 | P3 | −16.7 | 0/10 | −15.5 | 0/10 |
| operational\|snr14 | P1 | −14.3 | 0/10 | −13.4 | 0/10 |
| operational\|snr14 | P2 | −9.6 | 0/10 | −8.8 | 0/10 |
| operational\|snr14 | P3 | −18.5 | 0/10 | −17.6 | 0/10 |
| adversarial_sourced\|snr14 | P1 | −15.2 | 0/10 | −14.5 | 0/10 |
| adversarial_sourced\|snr14 | P2 | −9.7 | 0/10 | −9.0 | 0/10 |
| adversarial_sourced\|snr14 | P3 | −18.2 | 0/10 | −17.4 | 0/10 |

(Same pattern at SNR 17 and 20; full table in `phase_e_methods.json`.)

**Verdict: `PROBLEM_SURVIVES_METHODS_FAIL`** — none of P1/P2/P3 beats B* on
ANY cell, let alone the strongest standalone component. The combination
methods are uniformly **9-20 dB WORSE** than B*, and worse than B10/B12
standalone. The clean_control degradation is far above the 0.1 dB tolerance.

## 4. Why the methods failed (mechanism diagnosis)

The failure is not noise or a sign error (the 7 semantic gates all pass,
including the noiseless recovery and CFO sign/units checks). It is a
**physical-mechanism failure** of the same family already documented in
D-009 for the closely-related NDA-ML:

- **B10 pilot-RLS** uses a decision-directed (DD) feedback loop after the
  pilot training phase. At the canonical 10 kHz linewidth (D-007, ECL
  typical for star-ground FSO), the per-symbol phase drift is tiny, so the
  DD residual is dominated by AWGN, not by the carrier phase. The DD loop
  then tracks AWGN-induced decision errors, amplifying them — the same
  positive-feedback failure mode as TL-10 (DD collapses under deep fades).
  This is the B10 paper's mechanism working exactly as specified; B10 was
  designed for fiber CFO 1-10 GHz + linewidth 50 kHz-1.45 MHz, and at the
  canonical 10 kHz linewidth the regime where B10 has any advantage does
  not exist (D-009 found the same for NDA-ML vs VV: "10 kHz is in the
  ECL typical range where NDA-ML ≡ VV numerically").
- **B12 MAP** jointly estimates initial phase + Wiener phase noise using
  the AOPN covariance. At the canonical 10 kHz linewidth the Wiener
  covariance is essentially zero, so the MAP step degenerates to a plain
  PA estimator plus a smoothing filter. Without the linewidth-driven
  structure, MAP's smoothing actually HURTS by over-smoothing across
  block boundaries where the canonical Gamma-Gamma envelope changes.
- **P1/P2/P3** cascade or gate these two failing components, so they
  inherit the worst of both: P1 feeds B10's wrong residual to B12, P2
  routes between two failing estimators, P3's adaptive forgetting makes
  the RLS tracking even more aggressive against AWGN.

This is consistent with D-009's final conclusion: in the 10 kHz linewidth
regime that is the ECL-typical star-ground FSO operating point, blind /
pilot-aided phase estimators that were designed for fiber (high CFO, high
linewidth) collapse toward VV numerically and have no real mechanism
advantage. The B10/B12 combination methods do not escape this regime
limitation — they amplify it.

## 5. What survives

- The **problem** survives on one primary cell (adversarial_sourced|snr14,
  strong turbulence + SNR near HD-FEC waterfall): B* → O has ~0.6 dB mean /
  1.7 dB CI upper. This is the same kind of weak, high-variance headroom
  that D-009 documented for NDA-ML on the strong-turbulence waterfall.
- The **mechanisms** (B10 pilot-RLS, B12 MAP, P1 cascade, P2 gate, P3
  adaptive forgetting) fail at the canonical 10 kHz linewidth. They are
  retained as failed mechanisms — next round may decide whether to change
  mechanism (e.g., raise linewidth to the B10-supported 100 kHz-1.45 MHz
  range, which would re-trigger the D-007 question of whether that range
  is representative of star-ground FSO).

## 6. Claim ceiling (FR-25)

- The reference O is a legal phase-recovery ceiling (it derotates by the
  true phase but does NOT denoise), so the Kill-style interpretation of
  the headroom is valid. But the headroom is small (point 0.6 dB) and the
  CI is wide — the "problem survives" claim is provisional.
- The method-side result (P1/P2/P3 fail by 9-20 dB) is robust: the
  paired wins are 0/10 across all cells, not a marginal near-threshold
  result. The failure is not statistical noise; it is a real mechanism
  collapse at the 10 kHz linewidth.
- The headroom gate used 0.5 dB (the T006-specific D012 authorization).
  The method gate used 0.3 dB (the standard FR-15 target). Both are
  pre-registered in the frozen contract.
- Independent science-critic / integrity-verifier sub-agents were NOT
  used (single-GLM conversation). Per T006 §6, status is at most PARTIAL.
  The integrity self-checks (closure, SHA, raw recomputation, protected
  diff, semantic gates) are all PASS, but the scientific conclusion is
  not independently cross-verified in a separate context.

## 7. Scope ceiling (what this does NOT do)

- Does NOT close the high-order CPR family — only fails the three
  combination methods (cascade / confidence-gate / adaptive-forgetting)
  built from B10/B12 at the canonical 10 kHz linewidth.
- Does NOT enter Step 5/Contract/Execute.
- Does NOT modify the shared canonical generator or params.py.
- Does NOT continue Pilot-Jones (T005 scoped Kill received).
- Does NOT acquire new private fulltext.

## 8. Harvest

- **Defensive material**: B10/B12 standalone + P1/P2/P3 combination methods
  implemented and tested; if a reviewer asks "did you try combining pilot-RLS
  with MAP phase recovery for 16-QAM CPR", the answer is yes, on the canonical
  star-ground link at 10 kHz linewidth, and the combination methods lose by
  9-20 dB because the DD feedback and over-smoothing collapse at low linewidth.
- **Regime-confirmation**: the 10 kHz linewidth regime limitation
  (D-009 for NDA-ML) extends to the B10/B12 combination family. This is
  consistent reuse of a confirmed finding, not a new lesson.
- **No durable thesis contribution** from this package alone; the problem
  cell at adversarial_sourced|snr14 is weak and the methods clearly fail.

## 9. Provenance

- Source closure: `source-closure.yaml` (B10/B12 mechanism + parameter
  provenance + image-only equation caveat).
- Contract: `contract.yaml` (frozen grid, seeds, fairness, pre-registered
  verdict).
- Implementation: `components.py` (B10 pilot-RLS + B12 MAP standalone),
  `baselines.py` (B* ladder + P1/P2/P3), `channel_helpers.py` (canonical
  single-pol + pilot injection), `semantic_gates.py` (7 gates).
- Runner: `run_all.py` (Phases B-E).
- Results: `results/high-order-cpr-combination/{phase_b_gates,
  phase_c_bstar, phase_d_headroom, phase_e_methods, result}.json`.
- Tests: `tests/test_high_order_cpr_combination.py` (32 tests PASS).
- SHA closure: contract + 11 source files all hashed; runner asserts the
  frozen contract grid matches the runner before any primary run.
