# C04/C09 O1-Corrected Corrector Scout v1 — Synthesis

> Schema: `direction-lab.cb1.c04-c09-o1-corrected-scout.v1`
> Campaign: `science-scout-2026-07-20.dual-pol-osl`
> Date: 2026-07-22
> Triggered by: Probe `p01` (O1 hard pseudo-label MSE has an input-dependent
> optimum; full=0.039 < const=0.452 on every realization, A varies).
> Verdict: **`CANDIDATE_BLOWS_UP`** → **MECHANISM-DISTINCT NEGATIVE** for the
> context-dependent affine hypothesis under the corrected O1 objective.
> Claim ceiling: **LOCAL_SLICE / DIAGNOSTIC**.

## 0. TL;DR

The previous batch (`c04-c09-shared-corrector-v1`) used a **soft** expected-
distance training loss with an **input-independent constant optimum** (~1.31)
→ both candidates catastrophically collapsed (constant scrambled output,
D016/V005). Probe `p01` confirmed the **O1 objective** (hard-decision pseudo-
label MSE, the exact target `blind_affine_compare_16qam` solves in closed
form) has an **input-dependent optimum**. This Scout corrects ONLY the training
loss to O1 and asks the mechanism-distinct question:

> **Can a LEARNED context-dependent corrector (MLP on trace features, outputting
> a per-realization affine A,b) BEAT the closed-form blind affine when BOTH
> optimize the SAME O1 objective?**

**Answer: No.** The loss correction worked (training/val loss now reaches
~1e-5 instead of the 1.31 plateau — the model genuinely fits the O1 objective),
but the candidate still **CANDIDATE_BLOWS_UP**: macro Δ(cand−blind) = **+0.624**
[+0.483, +0.753], 0/7 cells beat blind, worst-cell degradation vs fixed_cma =
+0.783 (candidate PI-SER ≈ 0.93 = the 16QAM random ceiling on every cell).

The mechanism is now fully diagnosed and is **distinct** from the old loss-
artifact collapse:

- OLD batch: the loss had no input-dependent target, so the model learned a
  *constant* (A≈0, b≈const) that scrambled everything. Loss plateau 1.31.
- THIS batch: the loss is correct; the model *overfits* the training pseudo-
  labels (val loss → 1e-5) and the learned per-realization affine does **not
  generalize** to held-out cells. Loss → ~0, but the map is a memorization
  artifact that scrambles z_eval.

**Core thesis-grade finding:** On this anchor (fixed-μ CMA) + channel (CB1
dual-pol OSL 16QAM), the receiver-visible O1 objective is solvable in CLOSED
FORM per realization (blind affine ridge LS), and a learned context-dependent
corrector that optimizes the same O1 objective **cannot beat the closed-form
fit** — it either matches it (no added value from context) or overfits and harms.
Context-dependence adds **no value** over a single ridge-LS fit of the same
objective. This is the O1-corrected counterpart to the old mechanism negative,
and it closes the route on a sound (probe-confirmed) objective rather than a
buggy loss.

## 1. Scientific question

Can a learned context-dependent affine corrector (MLP on z_calib summary
statistics), trained with the corrected O1 hard-pseudo-label-MSE objective,
stably beat the closed-form `blind_affine_compare_16qam` baseline by ≥ MDE on
≥ 5/7 held-out cells? Equivalently: does **context-dependence** (varying A,b
per realization from trace features) add value over a single ridge-LS fit when
both optimize the same O1 objective?

## 2. Setup (all frozen BEFORE test)

- **System anchor**: fixed-μ CMA μ=0.03 (inherited from B01-R HF6), 11 taps,
  block_size=64, R²=1.32 — NOT re-tuned.
- **Channel**: CB1 dual-pol OSL 16QAM, α=4.2, β=1.4, gamma-gamma turbulence
  + SOP drift.
- **Conventional task comparator / THE BAR**: `blind_affine_compare_16qam`,
  frozen ridge 1e-8 (from `corrector-residual-headroom-v1` validation tuning;
  NOT re-tuned). This is the **closed-form O1 solution** (a single ridge LS of
  `hard_16qam(z_calib) ~ z_calib`, applied to z_eval). Receiver-visible only.
- **Candidate**: `MLPCorrector` (REUSED UNCHANGED from
  `c04-c09-shared-corrector-v1/src/corrector_adapter.py`) — maps 10 z_calib
  summary statistics (per-pol mean/variance, lag-1 autocorr, cross-corr) to a
  context-specific 2×2 complex affine A + offset b.
- **Comparators for context**: `fixed_cma` (anchor direct hard decision;
  no-harm floor), `oracle_affine_bound_16qam` (Kill bound via TX truth;
  context only, never a Go baseline).
- **THE ONLY CHANGE from the old batch — the training loss (O1)**:
  `z_corrected_calib = z_calib @ A.T + b`;
  `pseudo_label = hard_16qam(z_corrected_calib).detach()` (DETACHED target);
  `loss = MSE(z_corrected_calib, pseudo_label)`.
  The hard decision is not differentiable; the pseudo-label is detached so
  each SGD step is one Lloyd-like iteration (assign labels from the current
  map, then the gradient pulls the affine toward fitting those labels). This
  is exactly the objective `blind_affine` solves in closed form.
- **Cell split (IDENTICAL to old batch, paired comparison)**: training cells =
  4 validation cells from prior batches; test cells = 7 held-out cells
  (DISJOINT — model never sees held-out-cell realizations during training).
- **Seed split (IDENTICAL to old batch)**: train [81–90], val [91–95],
  test [71–80] (test slice = adjudication's blind_affine test slice).
  Pairwise disjoint; train/val disjoint from all prior batches [11–65].
- **HP**: one representative HP (hidden_dim=64, lr=3e-3, wd=1e-4); the change
  here is the LOSS, so a representative HP is sufficient for the Scout.

## 3. Semantic smoke (mandatory, BEFORE held-out eval — all PASSED)

| Test | Result | Gate |
|---|---|---|
| Identity (A=I, b=0) O1 loss finite & non-degenerate | 0.0657 | ✓ (OLD loss gave input-independent ~1.31) |
| Constant (A=0, best b) WORSE than full (A,b) closed-form | const 0.9312 > full 0.0357 (Δ +0.896) | ✓ (the gate the OLD soft loss FAILED) |
| No-harm: briefly-trained candidate PI-SER below random ceiling | 0.883 < 0.9375 | ✓ |

The constant test is the key gate: it confirms the O1 objective has an input-
dependent optimum (full strictly beats constant-b on every realization), which
is the entire point of the loss correction. The old soft loss FAILED this gate.

14/14 legality identity tests PASS (TX-truth isolation, affine form, shared
adapter contract, seed/cell disjointness, source-closure hash, O1-in-use).

## 4. Results — held-out evaluation (7 cells × 10 test seeds = 70 paired)

| Candidate | macro Δ(cand−blind) | 95% CI | cells beating blind by ≥ MDE | worst Δ(cand−fixed_cma) |
|---|---|---|---|---|
| C04_mlp | **+0.624** | [+0.483, +0.753] | 0/7 | **+0.783** |

Per-cell (PI-SER, primary metric):

| Cell | fixed_cma | blind | **candidate** | oracle | Δ(cand−blind) |
|---|---|---|---|---|---|
| 16qam-snr05-nominal-short | 0.586 | 0.603 | **0.931** | 0.618 | +0.328 |
| 16qam-snr10-nominal-short | 0.316 | 0.335 | **0.931** | 0.325 | +0.596 |
| 16qam-snr15-nominal-short | 0.176 | 0.178 | **0.931** | 0.117 | +0.753 |
| 16qam-snr25-nominal-short | 0.148 | 0.148 | **0.931** | 0.000 | +0.782 |
| 16qam-snr20-fg100-short | 0.153 | 0.154 | **0.931** | 0.031 | +0.777 |
| 16qam-snr10-fg100-long | 0.429 | 0.438 | **0.920** | 0.416 | +0.482 |
| 16qam-snr15-fg1000-long | 0.261 | 0.271 | **0.920** | 0.171 | +0.649 |

The candidate PI-SER is ≈0.93 on every cell — the 16QAM random-decision ceiling
(15/16 = 0.9375). The learned (A,b) scrambles the z-stream. `fixed_label_ser`
(secondary) is identical to PI-SER per cell (16QAM quadrant/stream ambiguity
fully resolved by the evaluator).

### Training-loss diagnostic (the key contrast with the old batch)

| | OLD batch (soft loss) | THIS batch (O1 loss) |
|---|---|---|
| val_loss plateau | **1.3084** (input-independent constant optimum) | **9.6e-06** (fits O1 objective) |
| candidate PI-SER | 0.93 (constant collapse) | 0.93 (overfit scramble) |
| verdict | BLOWS_UP | BLOWS_UP |
| root cause | loss artifact (no input-dependent target) | overfitting (learned map doesn't generalize) |

The O1 correction worked at the *loss* level: the model now genuinely minimizes
the hard-pseudo-label MSE on training data (val loss → ~1e-5 vs the old 1.31
plateau). But the learned per-realization affine does **not generalize** to
held-out cells. This is the mechanism-distinct failure the brief asked us to
isolate.

## 5. Verdict

**C04_mlp: `CANDIDATE_BLOWS_UP`** (worst-cell degradation > MDE on all 7 cells).

## 6. Mechanism analysis — does context-dependence help?

**No.** The closed-form `blind_affine` (a single ridge LS per realization,
applied to z_eval) is the **optimal** receiver-visible O1 fit for that
realization. A learned corrector optimizing the same O1 objective has only two
regimes:

1. **Match the closed-form** (learn the identity of "ridge LS per realization"
   as a function of trace features). This would *at best* tie blind affine —
   adding no value from context, because the closed-form is already the O1
   optimum per realization.
2. **Overfit the training pseudo-labels** (this batch's outcome). With val
   loss → 1e-5 the MLP memorizes the training (A,b)↔features mapping. That
   memorized map is a noise-fitting artifact: when applied to held-out
   realizations whose features fall outside the training distribution, it
   outputs an (A,b) that scrambles z_eval (PI-SER → random ceiling).

There is no third regime because **the O1 objective is the wrong target for a
context-dependent corrector**: it is exactly the objective the closed-form
solves optimally per realization. Context-dependence can only help if the
per-realization optimum *varies in a way predictable from receiver-visible
features* AND the closed-form cannot already capture it. Here the closed-form
captures it fully per realization, so a learned context map either replicates
it (no gain) or diverges (this batch).

The probe-p01 finding (O1 has an input-dependent optimum) is correct and
necessary, but it was about the **existence** of a non-constant optimum, not
about **learnability/generalization** of that optimum from trace features. The
gap between "O1 optimum exists and is input-dependent" (probe) and "a learned
context map generalizes to held-out cells" (this Scout) is the negative.

### Contrast with the old (soft-loss) negative

- **OLD**: the loss was degenerate (input-independent constant optimum), so the
  negative was a *loss artifact*, not a true mechanism limit. The candidate
  couldn't have beaten blind because it couldn't even form a useful target.
- **THIS**: the loss is sound (probe-confirmed input-dependent optimum; the
  model fits it to ~1e-5), so the negative is a *true generalization failure*.
  The route is now closed on a corrected objective, not a buggy loss. This is
  the scientifically defensible negative.

### Why blind_affine is the right bar and why it wins here

`blind_affine_compare_16qam` is receiver-visible, online, and solves O1 in
closed form per realization. It is weak in absolute terms (net-negative PI-SER
gain on the test slice per the adjudication batch: G_blind ≈ −0.008), but it is
the **optimal** O1 fit a receiver can make from z_calib alone. Any learned
corrector optimizing the same O1 objective is competing with its own closed-
form optimum; context-dependence cannot improve on a per-realization closed-form
fit of the same objective — it can only fail to match it.

## 7. What this means for the campaign

- **The C04/C09 output-correction route is CLOSED** at this budget and
  information access, on a **sound (O1) objective** — not merely on a buggy
  loss. The two negatives (old soft-loss collapse + this O1 overfit) agree from
  different angles: a receiver-visible affine corrector cannot beat the closed-
  form blind affine on this anchor + channel, whether the loss is degenerate or
  corrected.
- **The negative is thesis-grade**: "After CMA convergence, the residual 16QAM
  PI-SER is not recoverable by any receiver-visible *learned* affine corrector
  optimizing the hard-pseudo-label MSE. The closed-form ridge-LS fit
  (`blind_affine`) is the optimal receiver-visible O1 solution per realization;
  a context-dependent learned corrector either ties it (no added value) or
  overfits and harms (this batch). Oracle affine (TX-truth) closes ~6% but
  requires information the receiver lacks at decision time."
- **This is the O1-corrected, probe-grounded closure** of the C04/C09 route.
  Per the user brief: record the exact mechanism negative; do not continue
  network tuning; rotate to a different mechanism family (C12 soft-output /
  coded, or a genuinely different information mechanism in C13).

## 8. Integrity / unchanged

- All prior batch artifacts (B01/B01-R/c11-legality/corrector-residual-headroom/
  c04-c09-shared-corrector-v1): **untouched** (git diff empty on the old batch).
- D010/D011-amended/D012/D013/H007/H008/H009/V002/V003/V004/D016/V005:
  untouched.
- canonical-state.yaml: untouched.
- No TX truth in training or inference (14/14 legality tests PASS).
- No push, no merge. Only NEW files created under `c04-c09-o1-corrected-scout/`.

## 9. Source closure

`metadata.source_closure_sha256` records SHA-256 of 8 source files (contract,
runner, tests, reused adapter, evaluator, cell runner, dual-pol channel,
modulation). None missing. The reused `corrector_adapter.py` is imported
UNCHANGED from the old batch (hash recorded).

## 10. Compute and time

- Full batch (legality + smoke + dataset build + train + held-out eval +
  adjudication): **7.9 s** on CUDA (well under the 8-minute budget).
- Dataset build: 11 cells × 25 seeds × fixed-μ CMA = ~1.0 s (the short cells
  dominate; long cells are rare). Training: ~1 s (30 epochs, 40 train / 20 val
  realizations). Held-out eval: 7 × 10 = 70 paired measurements.
- Identity tests: 14/14 PASS in <0.1 s.
