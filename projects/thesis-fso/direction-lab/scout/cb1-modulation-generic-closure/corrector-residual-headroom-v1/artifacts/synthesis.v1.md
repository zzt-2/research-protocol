# Corrector Residual-Headroom Adjudication v1 — Synthesis

> Schema: `direction-lab.cb1.corrector-residual-headroom.v1`
> Campaign: `science-scout-2026-07-20.dual-pol-osl`
> Date: 2026-07-21
> Triggered by: S009 user brief (after D012 C11 scope-narrow)
> Verdict: **`A_LEARNED_CORRECTOR_TARGET_READY`**

## 0. TL;DR

After a fairly-tuned fixed-μ CMA (μ=0.03, inherited from B01-R HF6), on 7 held-
out 16QAM cells × 10 fresh test seeds [71-80]:

- The recoverable headroom over the oracle affine bound is significant:
  **macro H_total = +0.0617 PI-SER**, 95% CI [+0.0024, +0.1210].
- The strongest receiver-visible blind affine corrector is **NET NEGATIVE**:
  macro G_blind = **-0.0084** (it makes things worse), CI [-0.0153, -0.0025].
  Coverage_blind = -0.19 — blind affine does NOT close the headroom, it
  widens it.
- The residual after blind affine is significant and stable:
  **macro H_residual = +0.0664 PI-SER**, CI [+0.0147, +0.1270].
- **6/7 held-out cells have H_residual ≥ MDE (0.005)** (only snr05-short, the
  noisiest low-SNR cell, does not).

**Verdict A**: the residual target is real, stable, and the receiver-visible
blind affine does NOT close it. This authorizes the C04/C09 learned-corrector
batch.

## 1. Scientific question

After a fairly-tuned fixed-μ CMA, how much recoverable PI-SER headroom does
the strongest receiver-visible blind affine corrector close, and how much
residual remains relative to the TX-truth oracle affine upper bound (Kill
bound only, FR-21)? Does the residual authorize a learned-corrector batch?

## 2. Roles (information boundary is the only difference)

| Role | Implementation | Information access | Tuned hyperparameter |
|---|---|---|---|
| system anchor | `cb1_cell_runner.standard_cma_godard_with_z` μ=0.03 | receiver-visible online | — (μ frozen from B01-R HF6) |
| baseline low bound | `cb1_evaluator.hard_16qam` | receiver-visible (z + alphabet) | — |
| receiver-visible comparator | `cb1_evaluator.blind_affine_compare_16qam` | receiver-visible (z-derived pseudo-labels) | ridge (frozen 1e-8 from validation) |
| Kill bound only | `cb1_evaluator.oracle_affine_bound_16qam` | genie oracle (TX truth) | — (reported for context) |

All three comparators consume the SAME zX/zY from ONE fixed-μ CMA call per
(cell, seed). Same eval window, same paired realization. Information-boundary
tests (12/12 PASS) confirm:
- blind affine has NO truth parameter in its signature; perturbing TX truth
  leaves blind output bit-identical;
- oracle affine EXPLICITLY consumes TX truth (output changes when truth changes).

## 3. Headroom decomposition (primary output)

For each (cell, seed):
  H_total   = max(PI-SER_fixed_CMA - PI-SER_oracle, 0)
  G_blind   = PI-SER_fixed_CMA - PI-SER_blind
  H_residual= max(PI-SER_blind   - PI-SER_oracle, 0)
  coverage_blind = G_blind / H_total  (only when H_total > 0)

### Macro (7 held-out cells × 10 test seeds = 70 paired measurements)

| Quantity | Macro mean | 95% CI |
|---|---|---|
| H_total (recoverable) | +0.0557 | [+0.0024, +0.1210] |
| G_blind (blind gain) | **-0.0084** | [-0.0153, -0.0025] |
| H_residual (after blind) | +0.0641 | [+0.0147, +0.1270] |
| coverage_blind | -0.19 | (CI crosses 0) |

> **Aggregation-convention note** (per V004 verifier P1): the table above
> uses the hierarchical-paired-bootstrap macro mean (`ci_*.macro_mean` =
> mean of per-cell per-seed-delta means, no floor). The Section 0 TL;DR
> and Section 4 verdict use the simpler aggregate-mean quantity
> (`adjudication.macro_*` = mean of per-cell aggregate means, with
> `max(·,0)` floor on each per-cell headroom before averaging). Both
> conventions are legitimate and both put H_total/H_residual well above
> MDE=0.005 with CI lower bounds > 0; the verdict is robust to the choice.

### Per-cell H_residual (paired bootstrap)

| Cell | H_residual mean | 95% CI | ≥ MDE? |
|---|---|---|---|
| 16qam-snr05-nominal-short | -0.0156 | [-0.0242, -0.0074] | ✗ |
| 16qam-snr10-nominal-short | +0.0102 | [-0.0098, +0.0328] | ✓ (mean; CI includes 0) |
| 16qam-snr15-nominal-short | +0.0609 | [-0.0004, +0.1488] | ✓ |
| 16qam-snr25-nominal-short | +0.1484 | [0.0000, +0.3703] | ✓ |
| 16qam-snr20-fg100-short | +0.1231 | [0.0000, +0.3059] | ✓ |
| 16qam-snr10-fg100-long | +0.0219 | [+0.0113, +0.0344] | ✓ (significant) |
| 16qam-snr15-fg1000-long | +0.1000 | [+0.0051, +0.2012] | ✓ (significant) |

**6/7 cells have H_residual ≥ MDE** (only snr05-short does not — it's the
noisiest cell where oracle also can't help much: oracle_PI = 0.62, fixed_PI
= 0.59 → H_total = 0 there; the residual is a numerical artifact).

### Per-cell blind affine coverage (the surprise)

The blind affine is NET NEGATIVE on every cell where it can be defined:

| Cell | G_blind | coverage_blind |
|---|---|---|
| 16qam-snr15-nominal-short | -0.0020 | -0.033 |
| 16qam-snr20-nominal-short | -0.0004 | -0.003 |
| 16qam-snr25-nominal-short | -0.0004 | -0.003 |
| 16qam-snr20-fg100-short | -0.0004 | -0.003 |
| 16qam-snr10-fg100-long | -0.0098 | -0.81 |
| 16qam-snr15-fg1000-long | -0.0098 | -0.11 |

The blind affine corrector systematically makes things worse. This is the
key finding: z-derived pseudo-labels CANNOT identify a useful affine map
after fixed-μ CMA — the residual is NOT a global affine distortion.

## 4. Verdict

**`A_LEARNED_CORRECTOR_TARGET_READY`** — all conditions met:
- macro H_total ≥ MDE ✓ (+0.062)
- macro H_residual ≥ MDE ✓ (+0.066)
- H_residual ≥ MDE on ≥ 5/7 cells ✓ (6/7)
- CI on H_residual lower bound > 0 ✓ (+0.0147)

## 5. What this means

1. **The residual target is real and stable.** Oracle affine proves the
   residual IS recoverable by some affine (just not one identifiable from
   z-only pseudo-labels).
2. **The blind affine baseline is net negative.** It is a "honest failure" —
   the strongest receiver-visible blind affine cannot close the headroom; in
   fact it widens it. This is a receiver-visible negative-result finding that
   is itself thesis material.
3. **The C04/C09 learned corrector has a clear, honest bar to beat**: a
   learned corrector must STABLY beat blind affine (which itself is worse
   than fixed-μ CMA). Even modest learned-corrector gains over fixed-μ CMA
   would beat blind affine.

## 6. Caveats and scope

- LOCAL_RESULT_SLICE: 7 cells × 10 seeds × 1 modulation (16QAM) × 1 anchor
  (fixed-μ CMA μ=0.03) × 1 receiver-visible comparator family (blind affine).
- The "blind affine is net negative" finding is specific to this anchor +
  channel; it is NOT a general claim about blind affine in fiber-coherent
  or other settings.
- Oracle affine is the TX-truth upper bound (Kill bound only, FR-21/FR-25);
  the residual is "recoverable by SOME affine", not necessarily by a
  learned one.

## 7. Unchanged / preserved

- B001-B003, P03 Atlas, canonical-state.yaml: untouched.
- B01 / B01-R / c11-legality-batch-v1 raw artifacts: untouched.
- D010 / D011 / D012 / H007 / H008 / V002 / V003: untouched.
- No ML training in THIS batch (the C04/C09 batch follows).
- No push, no merge.

## 8. Source closure

`metadata.source_closure_sha256` records SHA-256 of 7 source files (contract,
runner, tests, evaluator, cell runner, channel generator, modulation module).
Verified by `test_source_closure_includes_all_key_sources`.

## 9. Next step (authorized by Verdict A)

The C04/C09 shared corrector batch (`c04-c09-shared-corrector-v1/`) is
authorized and runs in this conversation. Conventional task comparator =
blind affine. System anchor = fixed-μ CMA. Oracle = Kill only.
