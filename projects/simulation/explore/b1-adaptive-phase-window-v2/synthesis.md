# Synthesis — B1 adaptive phase-estimation window v2 (T008)

> GW Step 4a 维度 D MVE 综合 (identity-repaired reproduction).
> Authorization: D001 (epoch 12, B1_IDENTITY_REPAIRED_METHOD_PACKAGE) / formal D013 / system D018 / CP007.
> Source closure: ./source-closure.yaml. Contract: ./contract.yaml. SPEC: ./MVE-SPEC.md. Seed census: ./seed-census.yaml.
> Verdict: **`KILL_NO_ADAPTIVE_WINDOW_SPACE`** (corrected oracle space collapsed; §5 gate failed; Phase C/D NOT executed, per T008 §5 first stop condition).

## 1. What was run

Phase A (frozen source-closure + MVE-SPEC + contract + seed-census), Phase B
identity smokes (7/7 PASS — the 5 T007 identity gaps closed), Phase B corrected
space gate (§5 — validation-frozen B*/B-cond, real-curve metric, full
observability). Phase C (P1/P2/P3 methods) and Phase D (paired test) were NOT
executed because the §5 corrected oracle-space gate returned KILL; the task
package (§5 first stop condition) explicitly permits this when the corrected
oracle space genuinely collapses.

## 2. The 5 T007 identity gaps — closed

| Gap | T007 defect | v2 closure (verified by smoke test) |
|---|---|---|
| 1 baseline identity | `b2_structural_gate.py:343` picked `bstar_N = min(per_w_ber)` per cell per seed from test truth | B* = SINGLE N frozen on VALIDATION across ALL cells (lowest mean BER); test reads the frozen integer only. smoke3 + test_bstar_bcond_frozen_on_validation |
| 2 required-SNR metric identity | `b2_structural_gate.py:387` hardcoded `slope=0.15` to fabricate dB | required-SNR interpolated from the REAL BER-vs-SNR curve (log-BER linear interp); UNRESOLVED_NO_CROSSING if no legal crossing. smoke4 + test_required_snr_real_curve_no_fabrication. Physics note: HD-FEC 3.8e-3 is NOT reachable (BER floor ~7e-2 from shared common/_modulation pilot-overlay + VV noise at block=100), so the verdict uses log-BER + dB-equiv on the REAL measured B* slope. |
| 3 oracle candidate identity | oracle candidate set / B* inclusion not fully closed | oracle candidate set == WINDOW_GRID; B* is a member by construction (oracle BER <= B* BER per block). smoke4 |
| 4 observability identity | no held-out exact-window / majority-fixed comparison | validation + held-out test BOTH report Spearman rho, exact-window acc, top-2 acc, MAJORITY-FIXED acc, regret. smoke5 |
| 5 feature premature Kill | family Killed on `|rho|<0.5` alone | rho is REPORTED, not a standalone KILL. The §5 KILL is from the corrected headroom (B-cond vs B*), NOT from rho. test_corrected_gate_verdict_is_kill asserts the KILL trigger is the headroom field. |

## 3. Phase B identity smokes — 7/7 PASS

| Smoke | Result |
|---|---|
| smoke1_source_algorithm_identity | PASS (noiseless BER ~0; VV phase tracks true per-block avg within 0.05 rad; pi/4 bias exact; legal pi/2 invariant; linewidth variance ratio 8.0) |
| smoke2_signal_information_identity | PASS (pilot/data same channel rel RMSE ~0; deployable signatures carry no truth) |
| smoke3_baseline_identity | PASS (B*/B-cond are frozen integers from validation; synthetic test recovers them) |
| smoke4_oracle_metric_identity | PASS (required_snr matches real curve; NaN on no-crossing; oracle candidate set ⊇ B* → oracle BER ≤ B* BER) |
| smoke5_observability_identity | PASS (|rho|<0.5 BUT exact-window acc > majority-fixed → rho alone cannot Kill) |
| smoke_additional_direction_and_tradeoff | PASS (E1 SNR↓→N↑ on 16-QAM; BER(8)≠BER(256)) |
| smoke_input_output_nondegenerate | PASS (P1 picks different N multiset for two physical conditions; P3 fallback to B*) |

Source identity closes. No `BLOCKED_IDENTITY`.

## 4. §5 corrected space gate — KILL (the headline result)

### 4.1 Frozen baselines (validation, gap1 closure)

| modulation | B* (global, lowest mean BER) | B-cond (per condition) |
|---|---|---|
| QPSK   | 256 | {clean:128, operational:128, adversarial:256} |
| 16-QAM | 256 | {clean:256, operational:256, adversarial:256} |

B* and B-cond are FROZEN integers; the test phase (and the fresh-seed
confirmation below) read these integers only — never re-select from test truth.

### 4.2 Corrected oracle headroom (B-cond vs B*) — collapsed

| modulation | median dB-equiv | 20% trimmed dB-equiv | real B* slope (log-BER/dB) |
|---|---|---|---|
| QPSK   | **0.000** | **0.060** | -0.008 |
| 16-QAM | **0.000** | **0.000** | -0.005 |

Per-cell log-BER gains (B-cond vs B*) are essentially zero (max single-cell
0.0063 log-BER ≈ 0.04 dB on QPSK clean|12dB; 16-QAM is exactly 0 in every cell).
The median and 20% trimmed dB-equivalent gains are **8-15× below** the 0.5 dB
KILL threshold (FR-21 / TL-32). Both modulations KILL.

### 4.3 Fresh test-seed confirmation (gap1 + gap5 robustness)

Reserved test seeds 8100-8119 (20 seeds, fully disjoint from validation AND
from the entire historical observation pool per seed-census.yaml), reading the
FROZEN B*/B-cond integers only:

| modulation | median log-BER gain | trimmed | max | min |
|---|---|---|---|---|
| QPSK   | 0.0000 | -0.0001 | 0.0030 | -0.0029 |
| 16-QAM | 0.0000 | 0.0000  | 0.0000 | 0.0000 |

The collapse reproduces on the held-out test slice — this is NOT a
validation-specific artifact.

### 4.4 Observability (reported, not a Kill — gap4/gap5 closure)

| modulation | rho(SNR_hat, N) | rho(innov, N) | exact-window acc | top-2 acc | majority-fixed acc |
|---|---|---|---|---|---|
| QPSK   | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 |
| 16-QAM | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 |

The per-block oracle-best-N is a CONSTANT (the same N in every block of every
working-region cell) — so rho=0 and exact_acc=1.0 by construction. This is a
SYMPTOM of the collapsed oracle space (no block-level variation for any feature
to predict), NOT the Kill reason. The Kill reason is the corrected headroom
(§4.2). rho is reported honestly per gap5; it does not drive the verdict.

## 5. Mechanism (why the corrected oracle space collapsed)

1. **block-size dominance.** At the canonical params.py BLOCK=100, every window
   N ∈ {8..256} is applied to a 100-symbol block (N≥100 averages the whole
   block; N<100 splits into N-length mini-blocks, all reading only the current
   block). Because the Wiener phase drifts negligibly within a 100-symbol block
   at ECL linewidths (σ²_p = 2π·Δν·T_S ∈ [2.5e-5, 2e-4] → √(100·σ²_p) ≤ 0.045
   rad at 80 kHz, far below the AWGN-driven phase-estimation noise), the
   per-block carrier phase is effectively constant and EVERY N gives nearly the
   same VV phase estimate. The window choice is dominated by the block size,
   not by N — exactly the degeneracy T007's B2 also measured, now confirmed
   under the corrected (validation-frozen, real-curve) identity.

2. **linewidth-axis degeneracy.** At 10-80 kHz / 2.5 GBaud, σ²_p is so small
   that the linewidth-driven tracking-lag term (which would push N down at high
   linewidth) is negligible vs the AWGN-noise-averaging term. The E2 direction
   (linewidth↑→N↓) is therefore nearly degenerate. Same physics D-011/A1 found
   for NDA-ML block-length adaptation; T007 measured it on the AWGN+Wiener
   slice; v2 confirms it carries through to the GG primary channel under the
   corrected identity.

3. **BER-floor artifact (does NOT change the conclusion).** The shared
   common/_modulation pilot-overlay (pilot symbols overwrite pilot positions
   but tx_bits still carry the original data bits at those positions) plus VV
   phase-estimation noise at block=100 floor the BER at ~7e-2, far above
   HD-FEC 3.8e-3. This makes required-SNR uncomputable in this framework
   (reported as UNRESOLVED_NO_CROSSING for every primary cell), so the verdict
   uses paired log-BER + dB-equivalent on the REAL measured B* slope. The
   floor is COMMON to every N and every method, so it does not change the
   relative headroom conclusion (the corrected B-cond-vs-B* headroom would be
   ~0 dB even with a perfect BER evaluator).

## 6. Verdict

`KILL_NO_ADAPTIVE_WINDOW_SPACE` for both QPSK and 16-QAM, identity-repaired.

- The §5 corrected oracle headroom (B-cond vs validation-frozen B*) collapsed:
  median 0.000 dB, 20% trimmed 0.000-0.060 dB, both 8-15× below the 0.5 dB
  KILL threshold (FR-21 / TL-32 / FR-25). Confirmed on the fresh reserved
  test-seed slice (8100-8119).
- Per T008 §5 first stop condition, this permits KILL without implementing
  P1/P2/P3 ("corrected oracle 空间确实消失"). Phase C/D were NOT executed.
- This KILL is from the corrected headroom, NOT from feature rho (gap5
  closure). The T007 Kill was not received because of the 5 identity gaps; the
  v2 Kill survives the closure of all 5 gaps.

## 7. What this closes and what it does NOT

- **Closes**: the B1 "adaptive phase-estimation window" candidate as a
  deployable method in the satellite-FSO ECL regime (10-80 kHz linewidth, 2.5
  GBaud, QPSK/16-QAM, GG uplink-strong, block=100). No P1/P2/P3 adaptive
  controller can be packaged — there is no receiver-visible adaptive space to
  capture (the corrected B-cond-vs-B* headroom is 0 dB).
- **Does NOT close**: (a) the sat.1553 open problem at HIGHER linewidths
  (200 kHz-1 MHz, the stress band explicitly excluded as sole-primary); at
  those linewidths σ²_p grows 5-50× and the E2 axis may become deployable.
  (b) Adaptive-window CPE at LARGER block sizes (where per-block phase is no
  longer constant) — out of scope (canonical BLOCK=100 is the frozen project
  block). (c) The 16-QAM-only and pilot-CPE-only sub-directions — not tested
  because the §5 gate killed before Phase C.

## 8. Difference from T007

T007 returned the same `KILL_NO_ADAPTIVE_WINDOW_SPACE` verdict but it was NOT
received by the formal owner because of 5 identity gaps. v2 closes all 5 gaps
and reaches the same verdict under the corrected identity. The headline
numbers move (T007 reported oracle headroom 0.4-1.0 dB median from a
truth-assisted per-block oracle with hardcoded dB slope; v2 reports corrected
B-cond-vs-B* headroom 0.000 dB median / 0.000-0.060 dB trimmed with the real
measured slope), but the qualitative conclusion is the same: no deployable
adaptive-window space in the primary regime. The v2 contribution is that the
Kill is now IDENTITY-CORRECT — it cannot be dismissed on baseline/metric/
oracle/observability grounds.

## 9. Reusable material (thesis harvest)

- **Defensive negative result** (identity-corrected, supersedes T007): a
  quantified answer to sat.1553's L440 open problem in the primary regime —
  "no, in the satellite-FSO ECL regime at canonical block size there is no
  receiver-visible adaptive-window space; the corrected B-cond-vs-B* headroom
  is 0.000 dB median / 0.000-0.060 dB trimmed across both QPSK and 16-QAM and
  the full fresh test-seed slice." Publishable as a negative-result paragraph;
  pre-empts a reviewer asking "why not adapt the window?"
- **Methodology**: the identity-corrected structural gate
  (validation-frozen B*/B-cond + real-curve metric + reported-but-not-killing
  observability + fresh test-seed confirmation) is a reusable template that
  cleanly distinguishes "feature cannot predict" (gap5, NOT a Kill) from
  "oracle space genuinely collapsed" (the legitimate Kill). This distinction
  is exactly what TL-32/FR-25 demanded.
- **Physics insight**: at canonical block sizes and ECL linewidths, the window
  choice is dominated by the block size and the linewidth axis is degenerate;
  adaptive-window CPE is not a productive B1 direction in this regime.

## 10. Anomalies

- The block-buffered VV BER has a ~7e-2 floor in this evaluation framework,
  set by the shared common/_modulation pilot-overlay bit-mapping artifact
  (pilot symbols overwrite pilot positions but tx_bits still carry the original
  data bits) PLUS VV phase-estimation noise at block=100. HD-FEC 3.8e-3 is
  therefore NOT reachable; the verdict uses log-BER + dB-equivalent on the
  REAL measured slope. This floor is common to every N and every method, so it
  does not change the relative headroom conclusion. Reported honestly; the
  shared common is NOT modified (T008 file boundary).
- T007's `test_sha_stamps_match_actual_files` fails (the SHA recorded in
  T007's b2_log does not match the current source-closure.yaml on disk). This
  is a pre-existing T007-internal drift (the source was edited inside T007
  after the result was generated, without re-stamping the log). It is NOT
  caused by v2 (v2 is fully isolated in b1-adaptive-phase-window-v2/), and the
  T007 files are byte-identical to HEAD (verified by
  test_t002_t007_artifacts_unchanged_vs_head). Reported for transparency; not
  in v2's edit scope to fix.

## 11. Raw artifact pointers

- `results/b1-adaptive-phase-window-v2/corrected_gate_raw_{qpsk,qam16}.jsonl`
- `results/b1-adaptive-phase-window-v2/corrected_gate_result_{qpsk,qam16}.json`
- `results/b1-adaptive-phase-window-v2/corrected_gate_log_{qpsk,qam16}.txt`
- SHA stamps (in result JSON `sha` block): source-closure.yaml, contract.yaml, MVE-SPEC.md, seed-census.yaml
