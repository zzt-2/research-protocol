# Method Card — B1 adaptive phase-estimation window v2 (T008)

> GW Step 4a 维度 D. Authorization: D001 (epoch 12) / formal D013 / system D018 / CP007.
> Verdict: `KILL_NO_ADAPTIVE_WINDOW_SPACE` (corrected oracle space collapsed; identity-repaired).

## Identity

- **name**: B1 adaptive phase-estimation window (block-buffered VV, receiver-visible adaptive N)
- **primary_packaging**: low-complexity dual-pol FSO adaptive phase-window CPE (NOT realized — see verdict)
- **fallback_packaging**: fixed-window regret + observability working-region boundary (realized)
- **stage**: GW Step 4a (does NOT enter Step 5/Contract/Execute)

## Problem (M-C-A, source-closed)

- **M** (baseline): fixed-window VV block-mean CPE and fixed pilot moving-average CPE, N ∈ {8,16,32,64,128,256} (sat.1553 L434-435).
- **C** (condition): satellite-to-ground Gamma-Gamma uplink-strong turbulence (σ_p²=0.25) with simultaneous laser Wiener phase noise (linewidth Δν; per-symbol variance σ²_p = 2π·Δν·T_S, T_S=4e-10).
- **A** (adequacy gap — the sat.1553 L440 open problem): one fixed N cannot simultaneously average enough additive noise at low SNR and track fast Wiener phase drift at high phase-noise. sat.1553 L440 explicitly asks for dynamic-window methods and a quantified gain.

## Construct (the three receiver-visible adaptive-window methods — pre-registered, NOT run)

- **P1 physics-ratio rule**: receiver-visible SNR_hat / phase_innovation_hat → N ∈ W; monotone clipped interpolation following E1 (SNR↓→N↑) and E2 (innov↑→N↓); validation-learned bounds; B* fallback.
- **P2 validation lookup + hysteresis**: validation-learned bin table on (SNR_hat, phase_innovation_hat); hysteresis on bin crossing to suppress chatter.
- **P3 confidence-safe selector**: frozen ridge/logistic/shallow table on validation-learned per-window regret; low-confidence → B* fallback.
- **forbidden inputs**: tx_bits, true_h, true_phase, true_snr, oracle_best_N, test_labels, future_block.

## Comparators (the fair ladder)

- **B\*** (validation global fixed): SINGLE N frozen on validation across all (modulation, condition, SNR) cells by lowest mean BER. Frozen value: QPSK = 256; 16-QAM = 256.
- **B-cond** (validation per-condition fixed): one N per registered condition, frozen on validation. Frozen value: QPSK {clean:128, operational:128, adversarial:256}; 16-QAM {all:256}.
- **pilot CPE**, **validation-tuned BPS** (defined; the §5 gate killed before Phase C, so these were not run on the primary).
- **oracle per-block** (truth-assisted; candidate set = W; B* is a member by construction; KILL/headroom-only, NEVER a Go opponent).

## Metrics (pre-registered)

- **primary** (always computable): paired raw BER / log-BER; paired wins; bootstrap 95% CI; median / 20% trimmed; oracle-regret closure.
- **required-SNR at HD-FEC** (real curve): REPORTED but UNRESOLVED_NO_CROSSING — the block-buffered VV BER floor ~7e-2 (shared common/_modulation pilot-overlay artifact + VV noise at block=100) is above 3.8e-3 in every primary cell, so HD-FEC is NOT reachable in this framework. The verdict uses log-BER + regret, not fabricated dB.
- **observability** (reported, gap4 closure): Spearman rho of each receiver-visible feature vs per-block oracle-best-N; exact-window acc; top-2 acc; MAJORITY-FIXED acc; regret.

## Working region

- modulation: QPSK (sat.1553-native) + uniform 16-QAM (canonical square)
- linewidths: 10 kHz (clean), 20 kHz (operational), 80 kHz (adversarial) — all paper-sourced (D-007/D-009); 200 kHz-1 MHz excluded as sole primary
- SNR: GG primary working region {12, 16, 20} dB; AWGN slice {10,14,18,22} dB
- block: canonical params.py BLOCK=100 (GG block-fading unit + adaptation unit)
- window grid W = {8,16,32,64,128,256} (shared by ALL arms + oracle candidate set)

## Verdict and why

`KILL_NO_ADAPTIVE_WINDOW_SPACE` (identity-repaired). The §5 corrected oracle
headroom (B-cond vs validation-frozen B*) collapsed:

| modulation | B* (global) | B-cond | median dB-equiv | 20% trimmed dB-equiv |
|---|---|---|---|---|
| QPSK   | 256 | {128, 128, 256} | **0.000** | **0.060** |
| 16-QAM | 256 | {256, 256, 256} | **0.000** | **0.000** |

Both modulations have median AND 20% trimmed < 0.5 dB by 8-15×. Confirmed on a
FRESH reserved test-seed slice (8100-8119): QPSK median 0.0000, 16-QAM 0.0000.
Per T008 §5 first stop condition, this permits KILL without implementing
P1/P2/P3 ("corrected oracle 空间确实消失").

**This KILL is NOT a feature-rho Kill (gap5 closure).** The KILL trigger is the
corrected headroom field. Observability is reported (QPSK rho=0 because the
per-block oracle is a constant — a symptom of the collapsed space, not the
Kill reason).

## Mechanism (why the space collapsed, identity-corrected)

1. **block-size dominance**: at canonical BLOCK=100, every window N ∈ {8..256}
   is applied to a 100-symbol block (N>=100 averages the whole block; N<100
   splits into mini-blocks). Because the Wiener phase drifts negligibly within
   a 100-symbol block at ECL linewidths (σ²_p = 2π·Δν·T_S = 2.5e-5 to 2e-4 →
   √(100·σ²_p) ≤ 0.045 rad at 80 kHz), the per-block phase is effectively
   constant and EVERY N gives nearly the same phase estimate. The window
   choice is dominated by the block size, not by N.
2. **linewidth-axis degeneracy**: at 10-80 kHz / 2.5 GBaud, σ²_p is so small
   that the linewidth-driven tracking-lag term (which would push N down at
   high linewidth) is negligible vs the AWGN-noise-averaging term. The E2
   direction (linewidth↑→N↓) is therefore nearly degenerate — same physics
   T007 found (and D-011/A1 for NDA-ML).
3. **BER-floor artifact**: the shared common/_modulation pilot-overlay (pilot
   symbols overwrite pilot positions but tx_bits still carry the original data
   bits) plus VV phase-estimation noise at block=100 floor the BER at ~7e-2,
   far above HD-FEC 3.8e-3. This makes required-SNR uncomputable, but does NOT
   change the relative headroom conclusion (the floor is common to all N).

## Complexity (the construct, if it had run)

- P1: O(L) per realization (L = symbols); 1-table lookup per block.
- P2: O(L) + hysteresis state; bin table size = n_snr_bins × n_innov_bins.
- P3: O(L) + per-bin regret table; shallow model only.
- All deployable; no deep learning framework.

## Reusable material (thesis harvest)

- **Defensive negative result** (identity-corrected, supersedes T007): in the
  satellite-FSO ECL regime (10-80 kHz, 2.5 GBaud, QPSK/16-QAM, GG uplink-strong,
  block=100), there is no receiver-visible adaptive-window space — the
  corrected B-cond-vs-B* headroom is 0.000 dB median / 0.000-0.060 dB trimmed
  across both modulations and the full fresh test-seed slice. Quantifies the
  sat.1553 L440 open problem in the primary regime.
- **Methodology**: the identity-corrected structural gate (validation-frozen
  B*/B-cond + real-curve metric + reported-but-not-killing observability) is a
  reusable template that distinguishes "feature cannot predict" (gap5, NOT a
  Kill) from "oracle space genuinely collapsed" (the legitimate Kill).
- **Physics insight**: at canonical block sizes and ECL linewidths, the window
  choice is dominated by the block size and the linewidth axis is degenerate;
  adaptive-window CPE is not a productive B1 direction in this regime.
