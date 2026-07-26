# MVE-SPEC — B1 adaptive phase-estimation window v2 (T008)

> GW Step 4a 维度 D MVE 规格书 (identity-repaired reproduction). Frozen BEFORE any primary run.
> Authorization: D001 (epoch 12, B1_IDENTITY_REPAIRED_METHOD_PACKAGE) / formal D013 / system D018 / CP007.
> Source closure: ./source-closure.yaml. Contract: ./contract.yaml. Seed census: ./seed-census.yaml.
> **GW Step 4a only. No Step 5/Contract/Execute. No T006 repair. No new fulltext.**

## 0. Why v2 (the 5 T007 identity gaps)

T007 returned `KILL_NO_ADAPTIVE_WINDOW_SPACE`. The live control (D001) and the
formal owner (master-state §2 bridge) did NOT receive that Kill because five
identity gaps were not closed:

| Gap | T007 defect | v2 closure (see contract.identity_gap_closures) |
|---|---|---|
| 1 baseline identity | `b2_structural_gate.py:343` picked `bstar_N = min(per_w_ber)` **per cell per seed from test truth** | B* = SINGLE N frozen on VALIDATION across ALL cells; test reads the frozen integer only |
| 2 required-SNR metric identity | `b2_structural_gate.py:387` hardcoded `slope=0.15` to fabricate dB | required-SNR interpolated from the REAL BER-vs-SNR curve at HD-FEC; UNRESOLVED_NO_CROSSING if no legal crossing |
| 3 oracle candidate identity | oracle candidate set / B* inclusion not fully closed | oracle candidate set == window_grid (same as all arms); B* is a member by construction (oracle <= B* BER per block) |
| 4 observability identity | no held-out exact-window accuracy / majority-fixed comparison | validation + held-out test BOTH report Spearman rho, exact-window acc, top-2 acc, MAJORITY-FIXED acc, regret |
| 5 feature premature Kill | family Killed on `|rho|<0.5` alone | rho is REPORTED, not a standalone KILL; if corrected oracle space survives §5, P1/P2/P3 MUST run |

Per TL-32 / FR-25: the oracle headroom is a KILL tool, NOT a Go judge. v2's Go
verdict is judged by the deployable method beating B* (the traditional fixed
window) by >=0.5 dB; the corrected oracle headroom is only the §5 KILL gate.

## 1. Problem (M-C-A, source-closed) — UNCHANGED

- **M** (baseline): fixed-window VV block-mean CPE and fixed pilot moving-average CPE (window N ∈ {8,16,32,64,128,256}, sat.1553 L434-435).
- **C** (condition): satellite-to-ground Gamma-Gamma turbulence causing large block-SNR swings (sat.1553 uplink σ_p²=0.25), with simultaneous laser Wiener phase noise (linewidth Δν, per-symbol variance σ²_p = 2π·Δν·T_S).
- **A** (adequacy gap): one fixed N cannot simultaneously average enough additive noise at low SNR (wants large N) and track fast Wiener phase drift at high phase-noise (wants small N). sat.1553 L440 names this the open problem and asks for dynamic-window methods + a quantified gain.

## 2. Theoretical expectations (falsifiable) — UNCHANGED

| Expectation | Statement | FAIL trigger |
|---|---|---|
| E1 | SNR ↓ (linewidth fixed) → optimal N ↑ | stable opposite trend, unexplained |
| E2 | linewidth/innov ↑ (SNR fixed) → optimal N ↓ | stable opposite trend, unexplained |
| E3 | no single fixed N within 0.3 dB of per-cell oracle across ALL primary working cells | single fixed N <0.3 dB regret everywhere |

## 3. Conditions (paper-sourced, no sole-200-kHz primary)

| Condition class | linewidth | role | source |
|---|---|---|---|
| clean / control | 10 kHz | primary | D-007 truth source, params.py LASER_LW |
| operational | 20 kHz | primary | D-009 ECL measured (Opt.Commun.129312) |
| adversarial-sourced | 80 kHz | primary | D-009 ECL measured (OE.520452) |
| stress (secondary only) | 200 kHz - 1 MHz | secondary | sat.1553 L438 design tolerance; NEVER sole positive signal |

## 4. Window grid (frozen, shared)

`W = {8, 16, 32, 64, 128, 256}`. Every method (P1/P2/P3), every fixed baseline
(B*, B-cond, pilot CPE, BPS), AND the per-block oracle draw N from W only. No
per-method grid. B* is a member of the oracle candidate set by construction.

## 5. Channels and overhead (identity-fair)

- AWGN+Wiener slice (B2 source-native sweep): static, flat-fading, densified SNR grid to bracket HD-FEC.
- Canonical GG block fading (primary): `common/_gg_time.gg_time_envelope` + canonical `_dual_pol_channel` semantics, uplink_strong (α,β)=(1.0,0.7), block=BLOCK=100, equal pilot overhead and equal total energy for all arms.
- Pilot CPE arm: finite moving average over N pilot phases; equal pilot overhead charged.
- CFO: compensated (sat.1553-style Δf≈0); only CPE + Wiener PN remain.

## 6. Seeds (fresh disjoint 8xxx — see seed-census.yaml)

- semantic_validation_seeds: `[8000, 8001]` (deterministic semantic gates)
- bstar/bcond/feature_mapping validation seeds: `[8000..8009]` (10 val — frozen B*, B-cond, P1/P2/P3 calibration)
- test seeds: `[8100..8119]` (20 test — frozen; paired-bootstrap denominator)
- disjoint: 8xxx is fully unused historically (verified by explore census)

## 7. Metrics

- **Primary**: required-SNR at BER=3.8e-3 (HD-FEC) interpolation difference (dB) per arm per cell from the REAL curve; paired raw BER / log-BER; paired wins (per-seed); bootstrap 95% CI (2000 resamples across test seeds); median and 20% trimmed mean; oracle-regret closure %.
- **Secondary**: Q² only where BER is well inside the working region; Q² forbidden to dominate when any seed BER ≥ 0.2.
- **Falsification**: report mean, median, trimmed mean, per-seed rows, collapse-sensitivity flag. Single seed/cell contributing >40% of aggregate gain → positive verdict auto-downgrades to `UNRESOLVED_OUTLIER_DOMINATED`.

## 8. Phase B identity smoke (§4 of T008 — required, all must PASS)

5 identity smokes (all must pass before primary):

1. **source/algorithm identity**: window formula, phase sign, 16-QAM fixed bias, legal π/2 ambiguity, linewidth→per-symbol variance — each closed.
2. **signal/information identity**: pilot & data traverse the SAME physical channel; deployable methods read NO tx bits / true SNR / true phase / true channel / future block / test labels.
3. **baseline identity**: B* = validation-frozen single N; B-cond = validation-frozen per-condition N; forbid per-seed/per-test/true-bits re-selection.
4. **oracle/metric identity**: oracle candidate set ⊇ B*; required-SNR from the REAL curve; actual window / oracle label / feature target aligned to same block/latency.
5. **observability identity**: validation + held-out test BOTH report Spearman ρ, exact-window acc, top-2 acc, majority-fixed acc, regret; no single marginal ρ overrules all receiver-visible info.

Additional: noiseless/known-phase/Wiener direction tests; window averaging-vs-tracking tradeoff; block boundary / causal prefix / latency / polarization order; input change → non-degenerate method output change; raw→aggregate independent recompute; deterministic subprocess; UTF-8; source hash.

## 9. Corrected space gate (§5 of T008 — oracle KILL only)

After identity smokes pass, recompute on validation + fresh diagnostic slice:

- B* and B-cond (validation-frozen);
- oracle per-condition / per-block window (candidate set = window_grid, B* ∈ set);
- per-cell regret, median, 20% trimmed mean, paired CI;
- out-of-work-region, collapse, single-seed-dominance.

STOP without P1/P2/P3 ONLY if (FR-21 oracle Kill tool, TL-32/FR-25):

- corrected oracle primary working-region median AND 20% trimmed required-SNR gain vs legal B* BOTH `<0.5 dB`; OR
- gain comes ONLY from BER≥0.2 / no-crossing / outlier-dominated cells.

Otherwise (even when current feature ρ is low) → MUST enter §10.

## 10. Phase C three bounded methods (only if §9 oracle space survives)

All mappings/thresholds/tables learned on VALIDATION only; test frozen.

1. **P1 physics-ratio rule** — receiver-visible `SNR_hat / phase_innovation_hat` → N ∈ W; direction follows E1/E2; validation-learned bounds + B* fallback; reads no oracle.
2. **P2 validation lookup + hysteresis** — bin `(SNR_hat, phase_innovation_hat, optional proved-increment trace)`; switch window across blocks only on hysteresis-boundary cross; report switch rate, latency, no-hysteresis ablation.
3. **P3 confidence-safe selector** — frozen ridge/logistic/shallow table on per-window regret/confidence; low-conf → B*; compare with majority-fixed, P1/P2, and direct oracle-label-replay leak check; NO deep learning framework.

Mechanism slice (before full primary paired test) MUST show:
- at least two physical conditions pick different N;
- P2 hysteresis reduces chatter vs no-hysteresis;
- P3 low-conf really falls back, does NOT degrade to oracle-label replay;
- block-boundary phase continuity does not jump when window switches.

Slice passes → run full primary paired test, do NOT open a "method next round".

## 11. Baseline ladder (Phase D)

- `B* fixed`: SINGLE N chosen on validation across ALL cells (gap1 closure).
- `B-cond fixed-per-condition`: one N per registered condition, chosen on validation.
- legal pilot moving-average CPE (own arm, equal overhead).
- validation-tuned BPS (own arm, B/Nw frozen on validation).
- oracle per-block N: KILL/headroom-only, NEVER a Go opponent.

## 12. Pre-registered verdict (Phase D)

- `METHOD_SIGNAL`: some P beats B* by ≥0.5 dB required-SNR gain in ≥2 non-stress primary conditions; paired-bootstrap 95% CI lower >0; paired win fraction ≥0.70 (frozen test-seed denominator); not negative vs B-cond; clean degradation ≤0.1 dB; closes ≥50% of oracle regret; single seed/cell share ≤40%.
- `PROMOTION_READY`: METHOD_SIGNAL + robust to B-cond/conventional estimator + ablation supports component + independent verifier recomputes same.
- `ROBUSTNESS_OR_PACKAGING_BOUNDARY`: below 0.5 dB but materially lowers worst-decile BER / cycle-slip / widens FEC coverage; secondary/boundary only.
- `METHOD_FAIL_WITH_SPACE`: corrected oracle space survives §9 but P1/P2/P3 cannot stably close it; negates ONLY this construct.
- `KILL_NO_ADAPTIVE_WINDOW_SPACE`: ONLY when §9 corrected robust working-region oracle headroom fails; NEVER from feature ρ alone.
- `UNRESOLVED`: FEC crossing / CI / identity does not close.

## 13. Identity / integrity guards (V001/V039-class defenses)

- receiver-visible method signatures MUST NOT carry tx_bits / true h / true phase / true SNR / oracle_best_N / test labels / future block;
- block-buffered methods read only the current block;
- every method's window path MUST vary with ≥2 input conditions;
- pi/4 bias corrected in deployable code; legal pi/2 global resolve ONLY in evaluator;
- single realization per (cell, seed), shared by all arms/oracle;
- raw → aggregate BER recomputation bit-identical;
- PYTHONUTF8=1 explicit for all file IO; deterministic subprocess fingerprint (no Python built-in hash()).
