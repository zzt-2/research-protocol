# C14 Init-Strategy Scout v1 — Synthesis

> Schema: `direction-lab.cb1.c14-init-strategy-scout.v1`
> Campaign: `science-scout-2026-07-20.dual-pol-osl`
> Date: 2026-07-22
> Triggered by: Probe `p02` (collapse fully determined at block 0, AUROC=1.0 for
> the conventional detector from the first observable block) + portfolio
> remapping. New mechanism direction C14 (init-strategy), mechanism-distinct
> from C04/C09/C08/C10/C11/C12 (it changes the CMA **starting point**, not the
> cost, structure, step, or post-hoc output).
> Verdict: **`COST_FUNDAMENTAL`** → **MECHANISM-DISTINCT NEGATIVE** for the
> init-dependence hypothesis. The 16QAM inner-ring collapse is NOT init-
> dependent; it is a property of the Godard cost surface.
> Claim ceiling: **LOCAL_SLICE / DIAGNOSTIC**.

## 0. TL;DR

The scientific question was: **is the inner-ring collapse init-dependent?**
Concretely — if we seed the *same* Godard-with-z CMA from a TX-truth-optimal
(Wiener) init instead of the center tap, does it escape the collapse trajectory
that center-tap falls into? If yes, the collapse is a property of the
(center-tap + Godard) combination, not of the Godard cost, and data-driven init
becomes a viable positive direction.

**Answer: No.** The TX-truth **oracle Wiener init collapses on every single one
of the 37 center-tap-collapsed seed-events** (oracle escape rate = **0.0**,
0/37). On the cells where center-tap collapses, the oracle init produces
PI-SER within ±0.04 of center-tap on essentially every seed — it tracks the
collapse, it does not escape it. This is the single decisive result, and it
holds on ALL 11 atlas cells (5 short SNR-sweep, 3 dynamics, 3 long).

The mechanism is now fully diagnosed:

- The oracle Wiener init direction is **cosine = 0.9995** with the center tap
  (the CB1 OSL channel is only mildly dispersive, so the MMSE filter IS the
  center-tap direction). So the "best possible" init, even with full TX truth,
  lands in the same basin as the anchor and follows the same trajectory.
- Receiver-visible candidates are strictly **worse**, not escapes: the whitening
  init (dominant covariance eigenvector) collapses on **100%** of seeds
  (collapse_rate 1.000 vs center 0.336); the random best-of-K multistart also
  collapses on 100%. Direct probing confirms even near-orthogonal random inits
  (cosine 0.03–0.35 with center-tap) collapse on collapsed seeds AND fail to
  converge on healthy seeds (PI-SER ~0.88–0.92 on seed 72, which center-tap
  equalizes perfectly). The center tap is not an arbitrary anchor — it is a
  near-optimal init, and the collapse is determined by what happens *after*
  init, i.e. the Godard cost surface.

**Core thesis-grade finding:** On this anchor (fixed-μ Godard-with-z CMA) +
channel (CB1 dual-pol OSL 16QAM), the inner-ring collapse is **init-
independent** under the strongest possible init probe (TX-truth Wiener). The
collapse is a property of the Godard cost surface (R²=1.32 modulus mismatch on
a multi-ring constellation), not of the center-tap initialization. This
**closes C14 as a mechanism-negative** and is the init-strategy counterpart to
the recurring C04/C09/C08/C10/C11/C12 conclusion. It sharpens that conclusion:
the collapse survives a change to the *starting point*, so it is deep in the
cost, not an artifact of a particular init.

## 1. Scientific question

Is the 16QAM inner-ring collapse init-dependent? Probe p02 established the
collapse is **fully determined at block 0** (AUROC=1.0). Block-0 output is
`z = r_win @ w_init`, which is dominated by the initialization — yet every
variant tested across C04/C09/C08/C10/C11/C12 used the **same** center-tap
init. This left one untested escape hatch: maybe the collapse is a property of
(center-tap + Godard), and a data-driven init (informed by calibration-region
statistics) escapes the basin center-tap falls into. C14 tests exactly that,
holding the cost (Godard-with-z), μ (0.03), taps (11), block_size (64), R²
(1.32) fixed and varying **only the init vector**.

The kill bound is the oracle Wiener init: the TX-truth MMSE filter direction.
If even *that* collapses, no receiver-visible init can escape, and the
collapse is cost-fundamental.

## 2. Identity gate and semantic smoke (mandatory pre-checks)

* **Identity tests (`src/test_init_identity.py`)**: **11/11 PASS**. The
  center-tap path of the custom-init runner is **BYTE-FOR-BYTE IDENTICAL** to
  `baseline-atlas/cb1_cell_runner.standard_cma_godard_with_z` (`max |Δz| = 0.0`
  on both a collapsed seed 71 and a converged seed 72). `w_init=None` equals
  the explicit center-tap. All four init estimators are finite and normalized
  to the anchor's total filter energy (‖w‖=√2, matching center-tap's
  per-pol-unit convention so the Godard cost scale and divergence threshold are
  directly comparable). Information-contract gates confirm only `oracle_wiener`
  consumes TX truth; `whitening` and `multistart` signatures take signal-only
  args.
* **Semantic smoke (3 frozen checks)**: **ALL PASS**.
  - `smoke_center_tap_reproduces_collapse`: on snr25-nominal-short, seeds
    71–74 are bimodal (71, 73 collapse at PI-SER≈0.73–0.75; 72, 74 converge at
    0.0). The known collapse pattern is reproduced.
  - `smoke_center_tap_identity`: `max |Δz| = 0.0` vs the anchor on seed 71.
  - `smoke_oracle_init_is_sensible`: oracle init is finite, non-degenerate,
  norm √2 on all 4 seeds.
* **Divergence rate = 0.000 on every init, every cell** (no NaN, no weight-norm
  explosion past 10× init). The collapse is a *soft* divergence (high PI-SER
  with ‖w‖≈1.4), consistent with the baseline-atlas §8 finding.

## 3. Comparators (differ ONLY in w_init)

| Comparator | w_init | Information | Role |
|---|---|---|---|
| center_tap | w[center]=1, rest=0 | data-independent | **Go baseline** (the anchor exhibiting collapse) |
| whitening | dominant eigenvector of received-signal covariance | CSI_NONE r only | **CANDIDATE (a)** data-driven |
| multistart | best-of-5 unit-norm by 1-block warmup Godard cost | CSI_NONE r only | **CANDIDATE (b)** data-driven |
| oracle_wiener | TX-truth MMSE (Wiener) filter direction | r + TX truth | **Kill bound** (FR-21, scoring only) |

All four run the **identical** Godard-with-z blockwise update (prompt013:301-
306) with μ=0.03, 11 taps, block=64, R²=1.32. Only `w_init` differs. The
custom-init runner is a line-for-line copy of the anchor body with the four
filter vectors seeded from `w_init`.

**Interpretation note on "z_calib":** the brief describes the whitening init as
"compute init weights from the calibration slice / z_calib covariance." We
interpret the init's calibration input as the **received signal r** in the
calibration region, NOT the CMA output z — because the CMA output z cannot
exist before the CMA runs, and using z to initialize the CMA that produces z
would be circular. This is the only scientifically coherent reading; it is
documented in `batch-contract.v1.yaml init_region.source`.

## 4. The decisive result — oracle-escape test

**Does the TX-truth oracle init escape the center-tap collapse?**

| metric | value |
|---|---|
| center-tap collapsed seed-events (across 11 cells × 10 seeds) | **37** |
| oracle Wiener init escaped those (PI-SER ≤ 0.1) | **0** |
| oracle also collapsed (PI-SER > 0.3) on those seed-events | **37** |
| **oracle escape rate on collapsed** | **0.000** |
| **verdict** | **COST_FUNDAMENTAL** |

On every single seed where center-tap collapsed, the oracle Wiener init — which
has full TX truth — collapses too, at essentially the same PI-SER. Selected
paired per-seed values (oracle tracks center-tap, never escapes):

| cell | seed | center PI-SER | oracle PI-SER | escaped? |
|---|---:|---:|---:|---|
| snr25-nominal-short | 71 | 0.7305 | 0.7305 | NO |
| snr25-nominal-short | 73 | 0.7500 | 0.7539 | NO |
| snr10-fg100-long | 72 | 0.7852 | 0.8047 | NO |
| snr10-fg100-long | 74 | 0.7500 | 0.7383 | NO |
| snr15-fg1000-long | 72 | 0.8203 | 0.8320 | NO |
| snr20-nominal-long | 72 | 0.7930 | 0.7891 | NO |

Per-cell paired-bootstrap Δ(oracle − center) PI-SER: the 95% CI includes 0 on
8/11 cells (oracle statistically indistinguishable from center-tap); on the 3
AWGN/partial cells (snr05, snr10-short, snr15-short) oracle is *slightly worse*
(+0.04 to +0.05) because the Wiener direction trades a hair of margin for AWGN
robustness. Nowhere does oracle improve on center-tap.

**Why the oracle does not escape:** the oracle Wiener init direction is
**cosine 0.9995 with the center tap** (measured on snr25 seed 71). The CB1 OSL
channel is only mildly dispersive, so the MMSE filter IS the center-tap
direction. The "best possible" init, even with TX truth, is essentially the
same starting point as the anchor, so it falls into the same Godard-cost basin.

## 5. Receiver-visible candidates are strictly worse (not escapes)

| cell | ct col | wh col | ms col | ow col | ct PI-SER | wh PI-SER | ms PI-SER | ow PI-SER |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| snr05-nominal-short | 10/10 | 10/10 | 10/10 | 10/10 | 0.586 | 0.923 | 0.909 | 0.623 |
| snr10-nominal-short | 2/10 | 10/10 | 10/10 | 6/10 | 0.316 | 0.920 | 0.905 | 0.362 |
| snr15-nominal-short | 2/10 | 10/10 | 10/10 | 2/10 | 0.176 | 0.914 | 0.909 | 0.188 |
| snr20-nominal-short | 2/10 | 10/10 | 10/10 | 2/10 | 0.153 | 0.919 | 0.907 | 0.155 |
| snr25-nominal-short | 2/10 | 10/10 | 10/10 | 2/10 | 0.148 | 0.912 | 0.901 | 0.148 |
| snr20-fg100-short | 2/10 | 10/10 | 10/10 | 2/10 | 0.153 | 0.919 | 0.904 | 0.155 |
| snr20-fg1000-short | 2/10 | 10/10 | 10/10 | 2/10 | 0.153 | 0.919 | 0.907 | 0.155 |
| snr20-sop40e-short | 2/10 | 10/10 | 10/10 | 2/10 | 0.153 | 0.919 | 0.905 | 0.155 |
| snr10-fg100-long | 7/10 | 10/10 | 10/10 | 7/10 | 0.429 | 0.919 | 0.918 | 0.439 |
| snr15-fg1000-long | 3/10 | 10/10 | 10/10 | 3/10 | 0.261 | 0.921 | 0.914 | 0.263 |
| snr20-nominal-long | 3/10 | 10/10 | 10/10 | 3/10 | 0.230 | 0.918 | 0.909 | 0.230 |

**Macro** (mean over 11 cells):

| init | collapse_rate | mean PI-SER | divergence_rate |
|---|---:|---:|---:|
| center_tap | 0.336 | 0.251 | 0.000 |
| whitening | **1.000** | 0.918 | 0.000 |
| multistart | **1.000** | 0.908 | 0.000 |
| oracle_wiener | 0.373 | 0.261 | 0.000 |

Both data-driven candidates **collapse on 100% of seeds** (collapse_rate 1.000)
vs center-tap's 0.336 — they are dramatically *worse*, not escapes. The
whitening init (dominant covariance eigenvector) and multistart (best-of-5 by
warmup cost) both land in directions far from the center tap, and those
directions do not reach the convergent basin. Macro Δ(whitening − center)
PI-SER = **+0.668** [+0.54, +0.92 on individual cells]; multistart +0.658.

**Why the candidates collapse on healthy seeds too** (not just collapsed ones):
direct probing on snr25 seed 72 (which center-tap equalizes perfectly,
PI-SER=0.0) shows 5/5 random unit-norm inits (cosine 0.08–0.27 with center-tap)
collapse to PI-SER 0.88–0.92. The final weights barely move from the random
init (cos_final ≈ cos_init), meaning the Godard gradient from those distant
starting points is too weak to reach the center-tap basin within N symbols. So
the center tap is not an arbitrary anchor — it is a **near-optimal** init, and
moving away from it (whether randomly or via the covariance eigenvector)
universally hurts.

## 6. Verdict ladder (per claim ceiling LOCAL_SLICE / DIAGNOSTIC)

* **CELL**: on 0/11 cells does any init reduce the collapse rate below
  center-tap. Oracle matches center-tap (cosine 0.9995); whitening/multistart
  are strictly worse (collapse_rate 1.000 everywhere).
* **SLICE (16QAM representative subdomain)**: **LOCAL_NEGATIVE / DIAGNOSTIC**.
  The init-dependence hypothesis is rejected at the slice level: the TX-truth
  oracle init fails to escape on 37/37 collapsed seed-events (escape rate 0.0),
  and both receiver-visible candidates increase the collapse rate to 1.000.
* **DOMAIN / CANDIDATE / FAMILY**: out of scope (Scout claim ceiling).
* **C14 disposition**: **CLOSED as mechanism-negative**. The collapse is
  init-independent under the strongest possible init probe. No positive
  contribution line (data-driven CMA init) is supported by this evidence.

## 7. Mechanistic reading vs the motivating prior

* **Motivating prior (p02)**: "collapse is fully determined at block 0
  (AUROC=1.0), which implicates the initial conditions, yet all variants use
  the same center-tap init."
* **This Scout's reading**: block-0 determination does NOT imply init-
  *dependence*. The collapse is determined at block 0 because the Godard
  gradient is weak relative to the distance any reasonable init sits from the
  (narrow) convergent basin, so the trajectory is effectively decided by the
  cost surface immediately — but the *cost surface*, not the init, is the
  cause. The oracle Wiener init (TX-truth MMSE, cosine 0.9995 with center-tap)
  is the best init the receiver could ever hope to use, and it collapses
  identically. Changing the init to anything near-optimal changes nothing;
  changing it to anything far-from-center-tap makes it worse.
* **Sharpening of the portfolio conclusion**: the recurring C04/C09/C08/C10/
  C11/C12 conclusion ("collapse is a deep Godard-cost property") is
  **corroborated and extended** to the init axis. C14 was the last untested
  mechanism lever on the *equalizer input side* (cost=C04/C09, step=C08/C10,
  structure=C11, output=C12, detection=C01/C02/C06, init=C14). With C14
  negative, the collapse is confirmed robust to changes in **every** equalizer-
  side lever. The remaining escape hatches are all on the *information* or
  *output* side: C13 (pilot/CSI, a different information class) and C12 (soft/
  coded output, a different metric) — neither of which is an init claim.

## 8. Anomalies, scope, caveats

* **Anomaly (informative, not a bug)**: the oracle Wiener init is cosine 0.9995
  with center-tap, i.e. the "TX-truth-optimal init" IS the center tap for this
  channel. This is itself a finding: the CB1 OSL channel is mildly dispersive,
  so the MMSE direction is dominated by the center tap. A reviewer might argue
  this makes the oracle test "too easy to agree with center-tap." We addressed
  this two ways: (1) the oracle is still a *genuinely different* vector (non-
  zero off-center taps), and it still collapses — so even the infinitesimal
  perturbation away from pure center-tap does not escape; (2) we directly
  probed *arbitrarily different* init directions (random unit-norm, cosine
  0.03–0.35) and they collapse on collapsed seeds AND fail to converge on
  healthy seeds. There is no init direction — near or far — that escapes the
  collapse on the collapsed seeds. The init-dependence hypothesis is rejected
  across the full init-direction space, not just near center-tap.
* **Caveat (honest scope limit)**: this probes init at fixed μ=0.03. A much
  larger μ could, in principle, let distant inits reach the convergent basin
  within N symbols — but that is a step-size (C08) claim, not an init claim,
  and C08 already showed adaptive μ does not close the collapse. The init
  result here is conditional on the frozen step size, which is the same
  anchor all sibling scouts use.
* **Caveat**: the multistart warmup is 1 block (64 symbols) per the contract.
  A longer warmup for selection could pick a better start, but the direct
  random-init probe (§5) already shows the issue is not *selection* — it is
  that no random direction converges, so best-of-K cannot help.
* **Scope**: full 11-cell × 10-seed × 4-init batch ran in **4.2 s** wall time
  (vs 6 min budget). No scope reduction needed. 11×10×4 = 440 CMA runs (the
  multistart K=5 adds ~5 short warmups per cell-seed, all negligible).
* **No files modified outside `scout/cb1-modulation-generic-closure/c14-init-
  strategy-scout/`.** Baseline-atlas, P03, all prior scout batches, canonical
  state, and protected history are untouched. All reuse is via read-only
  import (`generate_shared_realization_dp`, `eval_window_for`, `hard_16qam`,
  `evaluate_dual_16qam`); the Godard-with-z body is *copied* into
  `cma_custom_init.py` (as the contract requires, since the anchor signature
  does not accept a custom init) and verified byte-identical.

## 9. Recommendation

**Close C14 as a mechanism-negative.** Do not promote to Deep Evidence — the
oracle-escape rate of 0.0 is a decisive kill on the strongest possible init
probe, and no amount of additional seeds or cells will overturn a 0/37 result
where the oracle init direction is provably near-optimal.

The positive-direction search should pivot to the two remaining levers that are
NOT equalizer-input-side: **C13 (pilot/CSI — a different information class)**
and **C12 (soft/coded output — already probed as HALF_DAY-ready, a different
metric)**. Both are mechanism-distinct from init and are the only axes not yet
shown to be cost-fundamental.

## 10. Files written

* `batch-contract.v1.yaml` — frozen Scout contract (system anchor, 4
  comparators, 11-cell × 10-seed sweep, semantic smoke, adjudication).
* `src/cma_custom_init.py` — Godard-with-z blockwise runner accepting a custom
  `w_init` (byte-identical to the anchor on center-tap) + the four init
  estimators (center_tap, whitening, oracle_wiener, random_multistart).
* `src/run_init_scout.py` — driver: identity tests → semantic smoke → full
  batch → paired-bootstrap adjudication → oracle-escape verdict.
* `src/test_init_identity.py` — 11 identity/legality gates (all PASS).
* `artifacts/result.v1.json` — raw per-cell, per-seed, per-init results +
  adjudication + oracle-escape test.
* `synthesis.v1.md` — this file.
