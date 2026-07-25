# MVE-SPEC — B1 adaptive phase-estimation window (T007)

> GW Step 4a 维度 D MVE 规格书. Frozen BEFORE any primary run.
> Authorization: D013 (epoch 9, ADAPTIVE_PHASE_WINDOW_METHOD_PACKAGE).
> Source closure: ./source-closure.yaml. Contract: ./contract.yaml.
> Modulation: uniform QPSK (sat.1553-native) + uniform 16-QAM (canonical-project
> high-SNR stress). Channel: canonical Gamma-Gamma block fading + Wiener PN.
> **No Step 5 / Contract / Execute. No T006 repair. No new fulltext.**

## 1. Problem (M-C-A, source-closed)

- **M** (baseline): fixed-window VV block-mean CPE and fixed pilot moving-average
  CPE (window N ∈ {8,16,32,64,128,256}, sat.1553 L434-435).
- **C** (condition): satellite-to-ground Gamma-Gamma turbulence causing large
  block-SNR swings (sat.1553 uplink σ_p²=0.15/0.25), with simultaneous laser
  Wiener phase noise (linewidth Δν, per-symbol variance σ²_p = 2π·Δν·T_S).
- **A** (inadequacy): one fixed N cannot simultaneously average enough additive
  noise at low SNR (wants large N) and track fast Wiener phase drift at high
  phase-noise (wants small N). sat.1553 L440 names this the open problem and
  explicitly asks for dynamic-window methods and a quantified gain.
- **Source**: sat.1553 content.md L440 (verbatim in source-closure.yaml).

## 2. Theoretical expectations (falsifiable)

| Expectation | Statement | FAIL trigger |
|---|---|---|
| E1 | SNR ↓ (linewidth fixed) → optimal N ↑ | stable opposite trend, unexplained |
| E2 | linewidth ↑ (SNR fixed) → optimal N ↓ | stable opposite trend, unexplained |
| E3 | no single fixed N is within 0.3 dB of per-cell oracle across ALL primary working cells | single fixed N <0.3 dB regret everywhere |

## 3. Conditions (paper-sourced, no sole-200-kHz primary)

| Condition class | linewidth | role | source |
|---|---|---|---|
| clean / control | 10 kHz | primary | D-007 truth source, sat.1553 L438 low end |
| operational | 20 kHz | primary | D-009 ECL measured (Opt.Commun.129312) |
| adversarial-sourced | 80 kHz | primary | D-009 ECL measured (OE.520452) |
| stress (secondary only) | 200 kHz-1 MHz | secondary | sat.1553 L438 design tolerance; never sole positive signal |

## 4. Window grid (frozen, shared)

`W = {8, 16, 32, 64, 128, 256}`. Every method (P1/P2/P3) and every fixed
baseline (B*/fixed-per-condition) draws N from W only. No per-method grid.

## 5. Channels and overhead (identity-fair)

- AWGN + Wiener PN slice (B2 source-native sweep): static, flat-fading. Used to
  read the E1/E2 trend cleanly before adding block fading.
- Canonical GG block fading (primary): `common/_dual_pol_channel` generator with
  `modulation='qam16'`/`'qpsk'`, the canonical GG time envelope, the canonical
  block size, equal pilot overhead and equal total energy for all arms.
- Pilot CPE arm: finite moving average over N pilot phases; equal pilot overhead
  charged to every arm that uses pilots.
- CFO: compensated (sat.1553-style, assume Δf≈0); only CPE + Wiener PN remain.

## 6. Seeds (disjoint from T002-T006)

- semantic_validation_seeds: `[7800, 7801]` (deterministic semantic gates)
- structural_validation_seeds: `[7800, 7801, 7802, 7803, 7804]` (5 val; window sweep + E1/E2 + oracle headroom)
- structural_test_seeds: `[7900, 7901, 7902, 7903, 7904, 7905, 7906, 7907, 7908, 7909]` (10 test, disjoint)
- method_validation_seeds: same 5 val (frozen B*, P1/P2/P3 mapping/tables)
- method_test_seeds: same 10 test (frozen config reused, no test tuning)
- disjoint: T005 used 74xx/75xx, T006 used 76xx/77xx → 78xx/79xx are fresh.

## 7. Metrics

- **Primary**: required-SNR at BER=3.8e-3 (HD-FEC) interpolation difference (dB)
  per arm per cell; paired raw BER / log-BER; paired wins (per-seed);
  bootstrap 95% CI (2000 resamples across test seeds); median and 20% trimmed
  mean (defend against outlier collapse seeds).
- **Secondary**: Q² only where BER is well inside the working region; Q² is
  forbidden to dominate when any seed BER ≥ 0.2 (collapse sensitivity check).
- **Falsification**: report mean, median, trimmed mean, per-seed rows, and a
  collapse-sensitivity flag. If a single seed contributes >40% of the aggregate
  gain, the positive verdict auto-downgrades to `UNRESOLVED_OUTLIER_DOMINATED`.

## 8. Phase B structural KILL gate (pre-method)

KILL `KILL_NO_ADAPTIVE_WINDOW_SPACE` if ANY of:
1. optimal N's direction vs SNR/linewidth disagrees with E1/E2 in the majority
   of cells, with no component-level explanation;
2. one fixed N's required-SNR regret < 0.3 dB across ALL primary working cells;
3. oracle per-block N gain vs fixed B* has median or 20% trimmed gain < 0.5 dB,
   OR the signal comes only from cells with BER ≥ 0.2 (collapse / out-of-work);
4. optimal N varies but receiver-visible features have held-out prediction
   Spearman |rho| < 0.5 AND exact-window accuracy does not beat the
   majority-fixed baseline.

On KILL: still write raw rows, tests, synthesis, worker-log; do NOT implement C.

## 9. Phase C three bounded methods (only if gate passes)

All mappings / thresholds / tables learned on VALIDATION only; test frozen.

1. **P1 analytic ratio rule** — map receiver-visible `SNR_hat / phase_innovation_hat`
   to N ∈ W via a monotone analytic rule with hard upper/lower bounds; direction
   MUST follow E1/E2; must NOT read the oracle-best N.
2. **P2 validation lookup + hysteresis** — bin `(SNR_hat, phase_innovation_hat)`
   into a validation-learned lookup table; switch window across blocks only when
   a hysteresis boundary is crossed (report switch rate and latency vs the
   no-hysteresis version).
3. **P3 confidence-safe controller** — validation-learned per-window regret /
   confidence picks N; LOW confidence MUST fall back to fixed B*; no test labels;
   frozen ridge / logistic / shallow table ONLY (no deep learning framework).

Mechanism slice (before full primary paired test) MUST show:
- at least two physical conditions pick different N;
- P2 hysteresis reduces chatter vs the no-hysteresis version;
- P3 low-confidence really falls back, and does NOT degrade to oracle-label replay;
- block-boundary phase continuity does not jump when the window switches.

## 10. Baseline ladder (Phase D)

- `B* fixed`: single N chosen on validation across all conditions.
- `fixed-per-condition`: one N per registered condition, chosen on validation.
- legal pilot moving-average CPE (own arm, equal overhead).
- validation-tuned BPS (own arm, B/Nw frozen on validation).
- oracle per-block N: KILL-only bound, never a Go opponent.

## 11. Pre-registered verdict (Phase D)

- `GO_ADAPTIVE_WINDOW_METHOD`: some P beats `B* fixed` by ≥ 0.5 dB required-SNR
  gain in ≥ 2 non-stress primary conditions, with 95% CI lower bound > 0 OR
  paired wins ≥ 7/10; NOT worse than `fixed-per-condition`; clean-condition
  degradation ≤ 0.1 dB; closes ≥ 50% of the oracle-window regret.
- `ROBUSTNESS_ONLY`: below 0.5 dB but materially lowers worst-decile BER /
  cycle-slip or widens FEC-working coverage; secondary/defensive material only.
- `METHOD_FAIL_WITH_SPACE`: oracle window space exists but P1/P2/P3 cannot
  reliably close it.
- `KILL_NO_ADAPTIVE_WINDOW_SPACE`: Phase B structural gate failed.
- `UNRESOLVED` / `UNRESOLVED_OUTLIER_DOMINATED`: FEC crossing / CI / identity
  does not close; or a single seed contributes > 40% of the aggregate gain.

## 12. Identity / integrity guards (V001-class defenses)

- receiver-visible method signatures MUST NOT carry tx_bits / true h / true
  phase / true SNR;
- block-buffered methods read only the current block (no future leakage);
- every method's window path MUST vary with at least two input conditions;
- the T006 pi/4-bias / 8-rotation mismatch is forbidden (tests enforce pi/4
  bias correction + legal pi/2 global resolve only);
- raw → aggregate BER recomputation must be bit-identical;
- PYTHONUTF8=1 explicit for all file IO; deterministic subprocess fingerprint
  (no Python built-in hash() of objects).
