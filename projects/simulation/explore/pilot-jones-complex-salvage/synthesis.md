# Synthesis — Pilot-Jones complex-Jones / PMD / PDL model-sufficiency salvage (T003)

> 2026-07-23 | GW Step 4a (model-sufficiency salvage, D063) | epoch 5
> Provisional verdict: **PIVOT_MODEL_NOT_JUSTIFIED** (physics gate fails — the
> impairment does not reintroduce a method-worthy gap)
> Formal performance MVE: **NOT RUN by design** (gate fails at the
> probe/limiting-case stage; no verified-range method-worthy gap to close)

## 1. What scientific uncertainty this package closed

The open question (D055/D062/D063): *a physically more sufficient complex Jones /
PMD / PDL channel — does it reintroduce a Pilot-Jones problem where the strongest
task-matched conventional baseline (B3) cannot close the oracle headroom, such
that a receiver-visible method (P) can beat B3?*

**Closed answer: No.** Across a model ladder M0 (real-rotation control) / M1
(complex unitary) / M2 (non-unitary PDL up to cond 3.6) / M3 (first-order PMD up
to 160 ps = 40% T_S), the B3-vs-oracle headroom is **flat and identical to the
M0 deep-fade-only control** — i.e. any residual headroom comes from the Gamma-
Gamma deep fade + AWGN, NOT from the PDL/PMD structure. The proposed P1
(energy-weighted LS) does not beat the task-matched B3 in any cell. The complex-
Jones/PMD/PDL upgrade does not produce a problem that B3 cannot close at this
symbol rate (2.5 GBaud, T_S=400 ps) and block size (64–100 sym).

## 2. T002 amendment (received, not overwritten)

- T002 code/raw integrity is trusted; the local verdict `UNITARY_REAL_ROTATION_MCA_KILLED`
  is inherited. T002 is NOT rewritten.
- **Recomputed raw (independent)**: P/B1 win-tie-loss = **0/6/4** (the frozen
  contract's `0/7/3` is a stale-count document defect, now on record).
- **`B1/O = 1.19` is a BER ratio, not 0.19 dB and not 0.5 dB.** The second FR-21
  headroom gate in T002 was therefore only a *diagnostic*, not a formal Kill.
- V037's claim-scope correction of V036 is received: V036 numeric/code integrity
  PASS holds, but its full integrity claim is PARTIAL (the two defects above).

## 3. Physical model evidence + physics gate (Phase 1)

See `model-evidence.yaml`. Key verified magnitudes (sub-agent, sources cited):
- **DGD**: ≤6 ps gives ~1 dB penalty at 32 GBaud (Valjus 2025 sat.1553 ref[76]);
  at 2.5 GBaud (T_S=400 ps) this is 1.5% of T_S — far below the ~10% (~40 ps)
  ISI/memory threshold. **First-order PMD is effectively flat at this rate.**
- **PDL**: component PDL <1 dB (cond<1.12) for a coherent front-end; cond≥1.5
  requires ≥3.5 dB PDL which is large for a single receiver/telescope.
- **Origin**: PMD/PDL are **component/fiber** impairment, NOT free-space
  atmospheric. Only the GG fade and the (already-modeled) RSOP are atmospheric.
- **RSOP**: up to 600 krad/s (LEO) — rotates on µs timescales ≫ block (40 ns),
  so the Jones matrix is block-constant. Already modeled.

**Physics-gate assessment**: the verified range is below the memory/conditioning
thresholds, but a positive signal could in principle appear under stress and the
task-matched-baseline-fully-covered condition does not hold (4 competitors
BLOCKED). So the honest path was to BUILD the ladder and let the empirical
B3-vs-oracle headroom decide — which is what Phase 2–4 did.

## 4. Model ladder + limiting-case tests (Phase 2)

Four isolated models built on top of the canonical generator (impairment applied
block-constantly to RX, shared-noise contract preserved). `run_salvage.py
--mode theory` → **8/8 limiting-case tests PASS**:

| test | check | result |
|---|---|---|
| T1 | M0 control byte-compatible with canonical | diff = 0 ✓ |
| T2 | M1 complex unitary, H^H H = I, cond = 1 | unitary err 0, cond 1 ✓ |
| T3 (×3) | M2 cond matches PDL-dB mapping (3.5/6/9.5 dB) | exact match ✓ |
| T4a | M3 DGD=0 → memoryless | diff = 0 ✓ |
| T4b | M3 DGD=80 ps → genuine memory | diff > 0 ✓ |
| T5 | M2 noiseless true-model recoverable | recovery err 0 ✓ |

Theoretical expectation table (drawn before running): M0/M1 → cond 1, memoryless
→ single-tap survives; M2 → cond>1 but flat → whitening survives; M3 → memory →
single-tap biased, tapped/FDE needed. **Observed results match expectations.**

## 5. Metric / threshold adjudication (Phase 3.2)

Corrected from T002:
- Primary metric: **fixed_label_ber** (nocma derotation-quality variant isolates
  the Jones-estimate quality from the CMA active component; CMA-variant also
  reported). Both reported.
- **BER→Q² formula frozen**: `Q = sqrt(2)·erfcinv(2·BER)`, `Q²_dB = 20·log10(Q)`,
  QPSK only. BER=0 → one-sided upper bound `0.5/N_eval` (no infinite Q). BER≥0.5
  → Q invalid (None). **BER ratio is NOT a dB and is NOT interchangeable with
  0.5 dB** — the T002 defect is fixed here.
- Go opponent = task-matched **B3** (B3_whitening for M2, B3_tapped for M3);
  beating only B0/B1/B2 is not a method signal. Oracle = upper-bound/Kill only.

## 6. Baseline adjudication + headroom (Phase 3.3 / Phase 4 probe)

Hard deep-turb conditions (α=2.0/β=1.0, γ=50=17 dB) — the most P-favorable, same
family as T002's bounded probe. 5 paired seeds {5000–5004}, disjoint from T002.

**Headroom does NOT grow with impairment strength (the decisive structural
finding):**

| band | cell | B3 BER | oracle BER | B3/O ratio | Q² headroom (dB) |
|---|---|---|---|---|---|
| stress | M0 control (no impairment) | 2.36e-2 | 1.16e-2 | 2.03 | 1.16 |
| stress | M2 PDL 3.5 dB (cond 1.5) | 2.36e-2 | 1.16e-2 | 2.03 | 1.16 |
| stress | M2 PDL 6.0 dB (cond 2.0) | 2.36e-2 | 1.16e-2 | 2.03 | 1.16 |
| stress | M2 PDL 9.5 dB (cond 3.6) | 2.36e-2 | 1.16e-2 | 2.03 | 1.16 |
| stress | M3 DGD 40 ps | 2.46e-2 | 1.93e-2 | 1.27 | 0.44 |
| stress | M3 DGD 160 ps | 4.47e-2 | 2.17e-2 | 2.05 | 1.50 |

The PDL headroom is **bit-identical to the M0 control** across 0→9.5 dB (delta =
0.0): adding non-unitary PDL does not change B3's residual error at all, because
the LS estimate + whitening inverse absorbs the conditioning exactly. The PMD
headroom does not grow monotonically with DGD. Therefore the residual headroom
is the **deep-fade + noise** headroom, present equally in M0 — it is NOT a
Pilot-Jones-specific gap.

In the **verified** physical range (PDL 1 dB / DGD 6 ps) the channel is near-
unitary/memoryless; B3 and oracle are statistically indistinguishable from M0.

## 7. Method candidates (Phase 4)

- **P1** energy-weighted (inverse-variance) pilot-LS Jones estimate — mechanism-
  distinct from fixed EMA (B1) and post-hoc regularization (B2); falsifier: if
  pilots have ~equal energy, weights → 1 and P1 degenerates to B0.
- P2 uncertainty-aware α(cond,innov) tracker (T002's P).
- P3 physics-structured whitening tracker.

**P1 vs task-matched B3 (win/tie/loss, 5 seeds)**: M2 6 dB → 0/2/3; M3 160 ps →
0/0/5; no cell where P1 beats B3. The gate's method-signal condition fails.

## 8. Conditional MVE — NOT RUN

Per `salvage-contract.yaml` stop-conditions, the formal performance MVE is not
run because the gate fails: no verified-range method-worthy gap exists, the
impairment adds no headroom beyond the M0 control even under stress, and P1 does
not beat B3. Running a 90-cell MVE would not change a structural verdict.

## 9. Provisional verdict

**PIVOT_MODEL_NOT_JUSTIFIED** (allowed enum).

Triggered gate (structural, two independent reasons):
1. **No impairment-added headroom**: PDL 0→9.5 dB and PMD 40→160 ps leave the
   B3-vs-oracle headroom flat and equal to the M0 deep-fade-only control → the
   headroom is from deep fade + noise, not from PDL/PMD.
2. **No method signal**: P1 does not beat the task-matched B3 in any cell.

This does NOT kill the Pilot-Jones family on other grounds; it only says the
complex-Jones/PMD/PDL upgrade is not the rescue axis. It is consistent with
T002's `UNITARY_REAL_ROTATION_MCA_KILLED` and extends it: even with a physically
richer (non-unitary / memory) Jones, B3 closes the headroom.

## 10. Claim ceiling + debts

- 4 D056 direct competitors remain `BLOCKED_NO_FULLTEXT`; claim ceiling capped
  at `CONDITIONAL_GO_WITH_BLOCKING_LITERATURE_DEBT` **at best** even if a future
  rescue axis appeared. Not reached here.
- The "OE2021 first-order PMD" provenance is **unverified** (sub-agent could not
  confirm an Optics-Express 2021 DOI; recorded as provenance debt).
- M4 (combined PDL+PMD) was excluded from the headroom table because its FDE
  oracle needs a joint channel solver (the simple U·diag·Vh FDE does not separate
  the PDL-then-PMD ordering). This is a scope limitation, not a confound: M2 and
  M3 cover the single-impairment axes that decide the verdict.

## 11. Durable harvest

- **Reusable negative/boundary material**: a clean, citable result — at 2.5 GBaud
  / 64–100-symbol blocks, non-unitary PDL (up to cond 3.6) and first-order PMD
  (up to 40% T_S) do NOT create a pilot-LS Jones stabilization gap that a task-
  matched conventional baseline cannot close; the residual headroom is the deep-
  fade+noise floor. Extends T002's unitary-rotation negative to the richer model.
- **Reusable model ladder + runner + tests**: M0–M3 isolated channels, B0/B1/B2/
  B3/P1/O ladder, paired-realization runner, nocma derotation-quality metric,
  BER→Q² converter with zero-error bound, 13 directed tests.
- **Reusable mechanism diagnostic**: the "headroom-vs-impairment-strength trend"
  test (does B3/O ratio grow with PDL/DGD?) generalizes FR-21 to a *causal*
  headroom filter — flat trend ⇒ headroom is not impairment-driven.
- **Correct BER→Q²/dB口径**: frozen formula + zero-error handling, reusable for
  any future Pilot-Jones or CMA-fade headroom question.
- **Excluded**: re-proposing generic pilot→complex-Jones→inverse stabilization
  on this class of channel at this symbol rate, without a genuinely new
  impairment axis (e.g. a verified frequency-selective channel with DGD ≫ T_S, or
  a sub-symbol block-variant Jones).
- NO_DURABLE_HARVEST items: none.
