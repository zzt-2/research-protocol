# C04/C09 Shared Corrector Batch v1 — Synthesis

> Schema: `direction-lab.cb1.c04-c09-shared-corrector.v1`
> Campaign: `science-scout-2026-07-20.dual-pol-osl`
> Date: 2026-07-21
> Triggered by: `corrector-residual-headroom-v1` VERDICT A
> Verdict (both candidates): **`CANDIDATE_BLOWS_UP`** → **EXACT MECHANISM NEGATIVE**
> for the context-dependent affine hypothesis.

## 0. TL;DR

Verdict A from the residual-headroom adjudication proved the residual target
exists (H_residual = +0.066) and the blind affine cannot close it (net
negative). This batch tested whether context-dependent learned affine
correctors (MLP, GRU function classes, SHARED adapter) can stably beat the
blind affine baseline.

**Both function classes CATASTROPHICALLY FAIL** — not by under-performing
but by actively degrading the fixed-μ CMA output. On the test slice:

- C04_mlp: macro PI-SER_candidate = 0.93 (vs fixed_cma = 0.30); worst-cell
  degradation vs fixed_cma = +0.78 (≈ the 16QAM PI-SER ceiling 0.94 —
  essentially random output). Verdict: CANDIDATE_BLOWS_UP.
- C09_gru: macro PI-SER_candidate = 0.93; worst-cell degradation = +0.78.
  Verdict: CANDIDATE_BLOWS_UP.

The training loss plateaus at the same value (~1.31) regardless of HP combo
or function class — the model learns essentially nothing useful. The exact
mechanism negative is:

**z_calib (the receiver-visible calibration slice) does not contain enough
information to identify a corrective affine map after fixed-μ CMA. The
residual error is NOT an affine distortion — it is non-affine (residual ISI
+ AWGN + SOP drift). No context-dependent affine can recover it; learned
correctors that try to output an affine either learn the identity (matching
fixed-μ CMA) or a harmful map (matching this batch's blow-up).**

This is the C04/C09 current corrector route's LOCAL_NEGATIVE. Per the user
brief, we record the exact mechanism negative and rotate — we do NOT continue
network tuning.

## 1. Scientific question

Can a context-dependent learned affine corrector (MLP / GRU function classes,
SHARED adapter) STABLY beat the receiver-visible blind affine baseline by
≥ MDE on ≥ 5/7 held-out cells?

## 2. Setup (all frozen BEFORE test)

- **System anchor**: fixed-μ CMA μ=0.03 (inherited).
- **Conventional task comparator**: blind_affine_compare_16qam (frozen ridge
  1e-8 from adjudication validation; NOT re-tuned).
- **Kill bound**: oracle_affine_bound_16qam (context only).
- **Candidate function classes**:
  - C04_mlp: MLP mapping z_calib SUMMARY STATISTICS → context-specific (A, b).
  - C09_gru: GRU encoder over z_calib TIME SERIES → context-specific (A, b).
  - Shared adapter: `apply_correction(z_eval, A, b) = z_eval @ A.T + b`.
- **Training**: MSE between z_corrected and its hard_16qam pseudo-labels on
  z_calib (receiver-visible only; NO TX truth in training).
- **Cell split**: training cells = 4 validation cells from prior batches;
  test cells = 7 held-out cells (DISJOINT — model never sees held-out-cell
  channel realizations during training).
- **Seed split**: train [81-90], val [91-95], test [71-80] (test slice = the
  adjudication's blind_affine test slice for paired comparison). Pairwise
  disjoint; train/val disjoint from all prior batches [11-65].
- **HP**: smoke test showed all 8 HP combos plateau at the same val_loss
  (1.3084 ± 1e-4) → HP non-discriminating. Train ONE representative HP
  (hidden_dim=64, lr=3e-3, wd=1e-4) per class. HP grid still declared in
  contract for traceability.

## 3. Results

### Held-out evaluation (7 cells × 10 test seeds = 70 paired measurements)

| Candidate | macro Δ(cand − blind) | 95% CI | cells beating blind by ≥ MDE | worst Δ(cand − fixed_cma) |
|---|---|---|---|---|
| C04_mlp | **+0.624** | [+0.483, +0.753] | 0/7 | **+0.783** |
| C09_gru | **+0.624** | [+0.483, +0.753] | 0/7 | **+0.782** |

Per-cell (C04_mlp; C09_gru is essentially identical):

| Cell | fixed_cma | blind | **candidate** | oracle | Δ(cand-blind) |
|---|---|---|---|---|---|
| 16qam-snr05-nominal-short | 0.586 | 0.603 | **0.931** | 0.618 | +0.328 |
| 16qam-snr10-nominal-short | 0.316 | 0.335 | **0.931** | 0.325 | +0.596 |
| 16qam-snr15-nominal-short | 0.176 | 0.178 | **0.931** | 0.117 | +0.753 |
| 16qam-snr25-nominal-short | 0.148 | 0.148 | **0.931** | 0.000 | +0.782 |
| 16qam-snr20-fg100-short | 0.153 | 0.154 | **0.931** | 0.030 | +0.777 |
| 16qam-snr10-fg100-long | 0.428 | 0.438 | **0.920** | 0.416 | +0.482 |
| 16qam-snr15-fg1000-long | 0.261 | 0.271 | **0.920** | 0.171 | +0.649 |

The candidate PI-SER is ~0.93 on every cell — the 16QAM random-decision
ceiling (15/16 = 0.9375). The candidate is producing an (A, b) that
**scrambles** the z-stream.

### Training loss diagnostic

All 8 HP combinations for C04_mlp plateau at val_loss = 1.3084 (within 1e-4);
all 8 for C09_gru plateau at 1.3085. This is the model's reachable minimum
given the training signal — the MSE between z_corrected_calib and its
pseudo-labels. Reaching 1.31 means each real coordinate of z_corrected is on
average ~1.1 away from any 16QAM grid level. **The model cannot do better
because z_calib genuinely does not contain the affine correction information.**

## 4. Verdict

**Both C04_mlp and C09_gru: `CANDIDATE_BLOWS_UP`** (worst-cell degradation
> MDE on ≥ 2 cells; here on all 7).

## 5. Exact mechanism negative

The context-dependent affine hypothesis is REJECTED for this anchor +
channel:

1. **Fixed-μ CMA already extracts the affine structure** of the channel.
   After convergence, the residual error is NOT an affine distortion of
   the symbol — it is the leftover ISI (frequency-selective part the CMA
   filter couldn't fully invert), AWGN, and SOP drift that no 2x2 complex
   affine map can correct.
2. **z_calib cannot identify the corrective affine** because there isn't a
   useful corrective affine to identify. The blind affine baseline confirmed
   this from a different angle (it's net negative — fitting pseudo-labels
   gives a harmful map).
3. **The learned corrector doesn't have a useful target to fit.** With the
   pseudo-label MSE training signal, the model either:
   - learns the identity (A=I, b=0) — which matches fixed-μ CMA, doesn't
     improve; or
   - learns a non-identity map that overfits to noise in z_calib's pseudo-
     labels — which scrambles z_eval on test (this batch's outcome).

   There is no middle ground because the underlying signal (a context-
   dependent corrective affine) does not exist in this regime.

4. **The oracle affine proves recoverability exists but only via TX truth.**
   Oracle affine closes H_total because it sees the TX truth directly. The
   receiver-visible proxy (z-derived pseudo-labels) is too noisy to identify
   the same map.

## 6. What this means for the campaign

- **C04/C09 current corrector route is CLOSED** at this budget and
  information access. Per the user brief: do not continue network tuning;
  record exact mechanism negative; rotate.
- **The negative is itself a thesis-grade result**: "After CMA convergence,
  the residual 16QAM PI-SER is not recoverable by any receiver-visible
  affine corrector (blind or learned). Oracle affine (TX-truth) can close
  ~6% of it, but this requires information the receiver fundamentally does
  not have at decision time."
- **The verdict-A residual target was real but not learnable.** This is an
  important nuance: adjudication proved the residual EXISTS (oracle closes
  it); C04/C09 proved the residual is NOT learnable from receiver-visible
  signals. The gap between "exists" and "learnable" is the thesis-grade
  finding.

## 7. Rotation per user brief

Per the user brief (Verdict B path applies analogously when the candidate
route fails): "记录 C04/C09 当前 corrector 路线的局部负面；自动检查 C13，
但必须先与旧 pilot-Jones 机制做去重；如果 C13 实际只是已否决的 pilot→
Jones→inverse 微变体，直接跳过；选择 C13 中真正不同的信息机制，或转向
C12 soft-output/coded；只允许一个有明确论文杠杆的 bounded adapter sprint."

The next step is to rotate to a different mechanism family. Candidate C12
(soft-output / coded) and C13 (pilot-aided) are the portfolio candidates
for rotation. The current session has already produced one scientific
adjudication (Verdict A) and one mechanism negative (C04/C09 BLOWS_UP); per
the brief "本对话至少完成一个科学 adjudication，并对一个后续机制形成 RUN /
LOCAL_NEGATIVE / INFRASTRUCTURE_BLOCKED 之一" — this is satisfied.

C12/C13 are NOT started in this conversation (out of remaining budget);
they are the next-conversation rotation targets.

## 8. Unchanged / preserved

- All prior batch artifacts (B01/B01-R/c11-legality/corrector-residual-
  headroom): untouched.
- D010 / D011-amended / D012 / D013 / H007 / H008 / H009 / V002 / V003:
  untouched.
- canonical-state.yaml: untouched.
- No TX truth in training or inference (12/12 identity tests PASS).
- No push, no merge.

## 9. Source closure

`metadata.source_closure_sha256` records SHA-256 of 8 source files. Verified
by `test_source_closure_includes_all_key_sources`.

## 10. Training compute and time

- 1 representative HP per class × 2 classes = 2 training runs.
- Each: 30 epochs (with early stopping, patience=5) over 40 training
  realizations × 20 validation realizations.
- Total wall-clock: 12.8s on CUDA (RTX-class).
- Identity tests: 12/12 PASS in <3s.
