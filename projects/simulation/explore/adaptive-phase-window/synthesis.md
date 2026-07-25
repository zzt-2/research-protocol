# Synthesis — B1 adaptive phase-estimation window (T007)

> GW Step 4a 维度 D MVE 综合报告.
> Authorization: D013 (epoch 9, ADAPTIVE_PHASE_WINDOW_METHOD_PACKAGE).
> Source closure: ./source-closure.yaml. Contract: ./contract.yaml. SPEC: ./MVE-SPEC.md.
> Verdict: **`KILL_NO_ADAPTIVE_WINDOW_SPACE`** (structural gate failed; Phase C
> not implemented, per task package).

## 1. What was run

Phase A (source-closure + MVE-SPEC + contract, frozen), Phase B1 (8 semantic
gates), Phase B2 (source-native AWGN+Wiener window-optimum sweep + GG block-
fading oracle-window headroom + structural KILL gate). Phase C (P1/P2/P3
methods) and Phase D (paired test) were **NOT executed** because the B2
structural gate failed; the task package forbids implementing methods after a
gate failure.

## 2. Phase B1 — semantic gates (all PASS)

| Gate | Result |
|---|---|
| noiseless_zero_phase | PASS (BER=0) |
| known_constant_phase (legal pi/2 resolve) | PASS (BER=0) |
| wiener_window_tradeoff (N=8 vs N=256 BER differs) | PASS |
| phase_sign_and_linewidth_variance (8x variance ratio, accumulates) | PASS |
| pi4_bias_and_pi2_ambiguity (QPSK+16-QAM bias = pi/4; legal pi/2 resolve) | PASS |
| pilot_data_mask_equal_energy (ratio 0.99; pilot count 128 = 15/16 rate) | PASS |
| no_future_no_truth (no tx_bits/h/theta/snr in deployable signatures) | PASS |
| window_path_varies (P1 low-SNR N=160 > high-SNR N=15) | PASS |

Source identity closes. No `BLOCKED_SOURCE_IDENTITY`.

## 3. Phase B2 — structural gate evidence

### 3.1 Best window N by cell (validation, 5 seeds, majority)

**QPSK** (AWGN+Wiener, sat.1553-native):

| SNR \ linewidth | clean (10kHz) | operational (20kHz) | adversarial (80kHz) |
|---|---|---|---|
| 10 dB | 128 | 16 | 64 |
| 14 dB | 16 | 16 | 64 |
| 18 dB | 16 | 16 | 64 |
| 22 dB | 16 | 64 | 64 |

**16-QAM** (high-SNR stress):

| SNR \ linewidth | clean | operational | adversarial |
|---|---|---|---|
| 10 dB | 256 | 256 | 128 |
| 14 dB | 256 | 128 | 64 |
| 18 dB | 128 | 128 | 64 |
| 22 dB | 64 | 64 | 64 |

### 3.2 E1 / E2 theoretical direction checks

- **QPSK**: E1 (SNR↓→N↑) passes 2/3 linewidths; **E2 (linewidth↑→N↓) passes 0/4 SNRs**. The best-N does NOT decrease with linewidth; it is roughly flat (16 or 64) across linewidths. → kill1 triggered.
- **16-QAM**: E1 passes 3/3; E2 passes 4/4. The best-N moves cleanly with both SNR and linewidth (256→64 as SNR rises; 256→64 as linewidth rises). → kill1 NOT triggered.

### 3.3 Receiver-visible feature predictability (kill4)

Spearman ρ of receiver-visible features vs the per-cell best N, across all
cells × seeds:

| Modulation | ρ(SNR_hat, best_N) | ρ(innov_hat, best_N) | feat_snr_ok (\|ρ\|≥0.5) | feat_innov_ok |
|---|---|---|---|---|
| QPSK | -0.074 | +0.240 | False | False |
| 16-QAM | -0.387 | +0.353 | False | False |

**Both modulations fail kill4**: no receiver-visible feature reaches |ρ|≥0.5.
The 16-QAM SNR_hat (ρ=-0.387) is the closest but still below threshold. The
innov_hat is weak in both cases — confirming D-011/A1's finding that raised-
power phase increments are AWGN-noise-dominated and do not track linewidth in
the satellite-FSO ECL range (10-80 kHz; σ²_p = 2π·Δν·T_S is tiny at 2.5 GBaud:
2.5e-5 at 10 kHz, 2e-4 at 80 kHz, so the per-window phase-tracking lag is
negligible vs the AWGN-noise-averaging term).

### 3.4 GG block-fading oracle-window headroom (kill3)

Per-block oracle (truth-assisted, legal per-block pi/2 resolve) vs fixed B*
(validation-aggregate best N), on the GG uplink-strong channel:

| Modulation | median gain (dB) | 20%-trimmed (dB) | non-collapse median |
|---|---|---|---|
| QPSK | +1.026 | +1.701 | +2.009 |
| 16-QAM | +0.413 | +1.403 | (see raw rows) |

**kill3 NOT triggered** for either modulation: there IS theoretical oracle
space (a per-block oracle that knows the truth could gain ~0.4-1.0 dB median
over the best fixed N). The oracle is correctly bounded (oracle BER ≤ B* BER
in every cell).

### 3.5 Universal fixed-N regret (kill2)

The AWGN+Wiener SNR grid (10-22 dB) does not bracket the HD-FEC waterfall
closely enough for any fixed N to reach BER=3.8e-3 at 10 dB for QPSK; the
required-SNR-at-FEC is NaN across the grid, so kill2 is **not testable** on
this slice (reported honestly as not triggered, not as passed). This is a
calibration gap in the source-native slice, not evidence either way.

## 4. Verdict

**`KILL_NO_ADAPTIVE_WINDOW_SPACE`** for both QPSK and 16-QAM.

- **QPSK**: kill1 (E2 direction fails: best N does not decrease with linewidth
  in the satellite-FSO ECL range) + kill4 (no receiver-visible feature
  predicts best N: ρ(SNR_hat)=-0.074, ρ(innov_hat)=+0.24).
- **16-QAM**: kill4 alone (no receiver-visible feature predicts best N:
  ρ(SNR_hat)=-0.387, ρ(innov_hat)=+0.353; both <0.5). The E1/E2 direction
  DOES hold for 16-QAM and there IS oracle space (median 0.4 dB), but no
  deployable receiver-visible feature can capture it.

## 5. Mechanism (why no deployable adaptive space)

The open problem (sat.1553 L440) posits that optimal N is a function of the
SNR/phase-noise ratio. The structural gate shows:

1. **The linewidth axis is nearly degenerate at satellite-FSO ECL linewidths.**
   At 2.5 GBaud, σ²_p = 2π·Δν·T_S is 2.5e-5 (10 kHz) to 2e-4 (80 kHz). For
   window N ≤ 256 symbols, the Wiener phase drift across the window is
   √(N·σ²_p) ≤ √(256·2e-4) ≈ 0.23 rad at 80 kHz — small relative to the AWGN
   phase noise a fixed N must average. So the linewidth-driven tracking-lag
   term that would push N down at high linewidth is weak in this regime. This
   is the same physics D-011/A1 found for NDA-ML block-length adaptation.

2. **The SNR axis does move the best N (E1 holds)**, but the receiver-visible
   SNR proxy (4th-power peak/floor) only reaches |ρ|≈0.39 vs best N for 16-QAM
   and |ρ|≈0.07 for QPSK — below the deployable |ρ|≥0.5 threshold. The best N
   is determined by per-realization fade/noise structure that a block-level
   SNR proxy cannot resolve.

3. **An oracle that knows the truth CAN gain 0.4-1.0 dB** (per-block N
   selection), but that gain is not capturable by any receiver-visible feature
   at deployable accuracy. This is exactly the failure mode the structural
   gate is designed to catch: theoretical headroom without a deployable handle.

## 6. What this closes and what it does NOT

- **Closes**: the B1 "adaptive phase-estimation window" candidate as a
  *deployable method* in the satellite-FSO ECL regime (10-80 kHz linewidth,
  2.5 GBaud, QPSK/16-QAM, Gamma-Gamma uplink-strong turbulence). No P1/P2/P3
  adaptive controller can be packaged.
- **Does NOT close**: (a) the sat.1553 open problem at HIGHER linewidths
  (200 kHz-1 MHz, the stress band we explicitly excluded as sole-primary); at
  those linewidths σ²_p grows 5-50x and the E2 axis may become deployable.
  But D-009 cross-validation established 10-80 kHz as the ECL measured-typical
  satellite-FSO regime, so this is not a primary-regime rescue. (b) The
  *negative* oracle headroom for 16-QAM at high SNR is a separate, smaller
  signal that does not by itself justify a method.

## 7. Reusable material (thesis harvest)

- **Defensive negative result**: a quantified answer to sat.1553's open
  problem in the primary regime — "no, in the satellite-FSO ECL regime there
  is no deployable receiver-visible feature that captures the per-block
  optimal-window gain; the theoretical 0.4-1.0 dB oracle headroom is not
  realizable without truth assistance." This is publishable as a negative-
  result paragraph and pre-empts a reviewer asking "why not adapt the window?"
- **Methodology**: the structural-gate pattern (theoretical direction check +
  oracle headroom + receiver-visible feature predictability, all pre-registered
  before any method is built) is a reusable template for any "adaptive
  parameter" candidate.
- **Physics insight**: the linewidth-degeneracy argument (σ²_p = 2π·Δν·T_S at
  ECL linewidths is too small for window-N to feel it within N≤256) is a
  reusable analytical anchor.

## 8. Anomalies

- The AWGN+Wiener SNR grid (10-22 dB) does not bracket the QPSK HD-FEC
  waterfall closely enough to test kill2 (universal-fixed regret) on this
  slice; reported as not-testable, not as passed.
- 16-QAM kill4 is "close" (ρ=-0.387 vs -0.5 threshold). A stronger block-level
  SNR estimator MIGHT cross the threshold, but the feature was pre-registered
  and frozen; re-engineering the feature to rescue the gate would violate the
  test-freeze rule. The honest verdict under the pre-registered feature set
  is KILL.

## 9. Raw artifact pointers

- `results/adaptive-phase-window/b2_raw_qpsk.jsonl`, `b2_raw_qam16.jsonl`
- `results/adaptive-phase-window/b2_result_qpsk.json`, `b2_result_qam16.json`
- `results/adaptive-phase-window/b2_log_qpsk.txt`, `b2_log_qam16.txt`
- SHA stamps (in result JSON header): source-closure.yaml, contract.yaml, MVE-SPEC.md
