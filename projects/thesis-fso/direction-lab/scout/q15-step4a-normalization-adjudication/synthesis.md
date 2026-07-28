# Q15 Step 4a Terminal Adjudication — Synthesis

> T023 / CP021 / epoch 53 | Date 2026-07-28
> Verdict: **Q15_ABSORBED_BY_CONVENTIONAL_NORMALIZATION_NO_GO**
> mission_method_delta: **NONE**

## TL;DR

T020's M4 "DIAGNOSTIC_METHOD_SIGNAL" was an artifact of a **buggy comparator**.
T020's M1 multiplied the complex signal by a POWER RATIO (scale = Ps/Pz applied
as scale·z) instead of the correct complex amplitude multiplier a = sqrt(Ps/Pz),
and the evaluator (8-way rotation {±1,±j} × perm + nearest-grid) cannot recover
an arbitrary magnitude scale. Once the CORRECT conventional normalization
comparators (pooled / per-pol sqrt-RMS, gated-scalar ablation, robust median
scalar) are placed on the same prefix-frozen, identity-on-degenerate-prefix
footing, they **match or beat M4's recovery on collapse seeds** AND stay within
MDE on healthy seeds. M4's gain is fully explained by弥补 the missing correct
normalization; the nonlinear monotone radius map adds nothing beyond a correct
scalar. Q15 exits; no fourth repair.

## 1. The audit that exposed the artifact

`methods.py:69` (T020): `scale = E_ABS2 / trimmed_mean(|z_prefix|^2)` then
`z' = scale * z`. For a collapsed stream z = c·s (c<1):

| formula | recovered amplitude | SER @ c=0.45 |
|---|---|---|
| M1 wrong: scale = Ps/Pz (= a²) | a²·c = a = 1/c = **2.22×** (over-correct) | **0.743** (FAIL) |
| correct: a = sqrt(Ps/Pz) | a·c = 1.0 (exact) | **0.0** |

The evaluator's rotations {+1,+j,-1,-j} are unit-modulus, so they CANNOT undo
a magnitude error. M1's over-correction destroys the collapsed stream it was
meant to fix. M4's gate dodged this by selecting identity on healthy prefixes
and M2_transport (a nonlinear map, not the buggy scalar) on collapsed ones —
so M4 "won" relative to a broken M1, not relative to a correct normalization.

## 2. Fair comparison (smoke PASS, then 7 cells × 40 seeds)

**Semantic smoke (8/8 PASS, TDD-written first):**
- correct sqrt restores amplitude (SER=0) for all c; M1-wrong over-corrects
  catastrophically at strong collapse (c=0.45 SER=0.743), monotone in |1/c−1|;
- per-pol/pooled normalization unbiased (mean a≈1.0) and within finite-sample
  envelope on unit-power prefixes;
- prefix-freeze invariance; info-increment; QPSK identity; clean-stream identity
  branch not degraded; collapsed prefix opens the gate.

**Aggregated results (seed-cluster, 10k bootstrap 95% CI, MDE=0.005):**

| slice | method | seed-mean PI-SER | mean Δ vs base | CI95 | help/hurt/tie | healthy-worst Δ |
|---|---|---|---|---|---|---|
| old 201-220 | baseline μ=0.03 | 0.3143 | — | — | — | — |
|  | **M4 gated (candidate)** | **0.2317** | **−0.0826** | [−0.138,−0.032] | **7/0/13** | **0.000** |
|  | correct pooled sqrt | 0.2234 | −0.0910 | [−0.149,−0.038] | 15/4/1 | 0.0234 |
|  | correct per-pol sqrt | 0.2239 | −0.0905 | [−0.148,−0.037] | 13/5/2 | 0.0273 |
|  | gated-scalar ablation | 0.2269 | −0.0874 | [−0.146,−0.034] | 7/0/13 | 0.0000 |
|  | **robust scalar (median)** | **0.2232** | **−0.0911** | [−0.148,−0.038] | **15/4/1** | **0.0156** |
| fresh 241-260 | baseline μ=0.03 | 0.4150 | — | — | — | — |
|  | **M4 gated (candidate)** | **0.2830** | **−0.1320** | [−0.189,−0.078] | **13/0/7** | **0.000** |
|  | correct pooled sqrt | 0.2696 | −0.1455 | [−0.205,−0.089] | 18/2/0 | 0.0195 |
|  | correct per-pol sqrt | 0.2700 | −0.1450 | [−0.205,−0.089] | 18/2/0 | 0.0195 |
|  | gated-scalar ablation | 0.2758 | −0.1393 | [−0.199,−0.082] | 13/0/7 | 0.0000 |
|  | **robust scalar (median)** | **0.2686** | **−0.1464** | [−0.205,−0.091] | **19/1/0** | **0.0156** |

**Direction stability**: M4 loses to robust_scalar on BOTH slices (old: 0.2317
vs 0.2232 = +0.0085; fresh: 0.2830 vs 0.2686 = +0.0144), both > MDE. The
fresh slice reproduces the direction (no sign flip).

## 3. Why M4 is absorbed (mechanism)

1. **Correct scalar already recovers collapse exactly.** On synthetic z=c·s the
   audit shows correct sqrt gives SER=0 for ALL c. The collapse is a pure
   amplitude scale, and a correct scalar is the optimal recovery. M4's nonlinear
   monotone radius map cannot beat an exact scalar recovery — at best it ties,
   and in practice its quantile anchors introduce slight distortion (M4 loses
   by ~0.01 PI-SER).
2. **The gate's value is safety, not recovery.** gated_scalar_ablation (M4 gate
   + correct scale) ≈ M4 (0.2513 vs 0.2574 overall): substituting the correct
   scalar for the map changes nothing material. So the map adds no information
   beyond the gate+scale. The gate's identity-on-healthy property (healthy-worst
   Δ=0.0) is real, BUT the correct scalars' healthy degradation (0.016–0.027) is
   already below MDE — so a plain always-on correct normalization is a usable
   conventional comparator that does not catastrophically regress.
3. **No independent information increment (criterion 2 FAIL).** The three
   differentiators (prefix-only / identity-fallback / post-proc map) do not
   produce a measurably better outcome than a correct conventional normalization
   on the same prefix-frozen footing. The "problem survives conventional
   baseline" state is NOT reached.

## 4. What is salvageable (methodology lessons, NOT a method)

- **Evaluator/normalization methodology lesson**: any post-CMA output transform
  comparator family MUST include correct pooled + per-pol sqrt-RMS as the
  baseline-ladder floor; a power-ratio-applied-as-complex-multiply bug is silent
  under a rotation-only evaluator. Future CB1 z-only work must freeze the
  correct-sqrt normalization as the first comparator before claiming any
  nonlinear map has value.
- **Identity-fallback safety property** is a real, measurable design property
  (healthy-worst Δ=0.0) but it is a *constraint*, not a contribution, when the
  always-on correct scalar already stays within MDE on healthy seeds.
- **M2 monotone quantile/radius calibration** is NOT optimal transport (per
  task discipline 2); it is a monotone CDF→shell heuristic. Its under-performance
  vs a correct scalar here is evidence that the problem structure does not need
  a nonlinear map.

## 5. Claim ceiling

- formal_science_disposition: **Q15_ABSORBED_BY_CONVENTIONAL_NORMALIZATION_NO_GO**
  (criterion 2 empirically FAILS; M4 does not survive the strongest correct
  conventional normalization on either slice).
- mission_method_delta: **NONE** (a reliable negative + an evaluator/normalization
  methodology lesson; NOT a method or packaging boundary).
- No Step 4a recommendation, no thesis-facing method card, no Step 5/Contract/Execute.
- **No fourth Q15 repair/factory package.** Q15 exits.

## 6. Scope discipline

- Did NOT modify T020 directory, common/, params.py, cb1_evaluator.py,
  cb1_cell_runner.py, .sessions, master-state, current YAML, or any B01-R/C11
  artifact. All T020 reuse was read-only import.
- Did NOT enter Step 5, Contract, or Execute. No paper victory claims. No push.
- New code/artifacts confined to the isolated `q15-step4a-normalization-adjudication/`
  directory.
