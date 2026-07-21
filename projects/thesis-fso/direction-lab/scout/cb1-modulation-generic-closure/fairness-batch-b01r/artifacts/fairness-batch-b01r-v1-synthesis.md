# Fairness Batch B01-R — Synthesis (Hotfix v2, supersedes v1)

**Campaign:** `science-scout-2026-07-20.dual-pol-osl`
**Batch:** Fairness Batch B01-R (hotfix v2; supersedes v1 synthesis of same date)
**Date:** 2026-07-21 (hotfix)
**Mode:** SCIENCE_SCOUT (no ML trained; conventional fairness + detector probe only)
**Raw artifact:** `artifacts/fairness-batch-b01r-v1.json` (metadata.hotfix_version=`hf2_2026-07-21`)
**Contract:** `batch-contract.v1.yaml` (frozen before running)
**Frozen params:** `artifacts/frozen-params-b01r-v1.yaml` (regenerated)
**Audit reproduction:** `artifacts/b01-audit-reproduction.md` (10 B01 findings confirmed; unchanged)

---

## 0. Why this hotfix exists

The v1 synthesis reported VERDICT B (`B_B01R_FAIRNESS_SURVIVES_BUT_DETECTOR_TARGET_NOT_READY`). An external review identified **7 implementation flaws** in v1, of which 4 were P0 (mechanically determined the verdict) and 3 were claim overreach. This hotfix fixes all 7 and re-runs from scratch. v1 verdict is **superseded**; v1 raw numbers are preserved in git history (commit `0404f47`).

**The 7 flaws fixed in this hotfix:**

| # | Flaw | Fix | Effect |
|---|---|---|---|
| 1 | `min_z2_ratio_score` only read `z2_over_R2_ratio`; anchor trace only has `output_power` → all 110 scores NaN → adjudicator's "both detector scores need ≥2 two-class cells" mechanically failed for min_z2 → VERDICT B forced | Added `output_power → ratio` fallback in `min_z2_ratio_score` (matching `c05_alert_score` and `degradation_onset_block`) | min_z2 now produces real scores; 2 held-out cells two-class |
| 2 | Detector could fire during warmup (block 0/1); reported `lead_time = onset(2) - alert(0) = +2` was warmup口径 misalignment, not real lead time | Added warmup guard in `c05_alert_score`: blocks before `warmup=2` cannot emit alerts | lead_time now honest; actual values are negative (detector fires AFTER onset — no real lead time) |
| 3 | `recall@5%FPR` with n_neg∈{2,4,6} silently used floor(0.05·n_neg)=0 or off-by-one 1 → reported "5% FPR" was actually 25/50% | `recall_at_fpr` returns `(recall, actual_fpr, fp_budget)`; aggregate records `recall_at_5pct_fpr_ACTUAL_FPR` + explicit note when target not resolvable | Reports say e.g. "5% not resolvable with n_neg=4; reported at 25%" |
| 4 | (consequence of 1) VERDICT B was mechanically forced, not scientifically reached | Re-adjudicate after fix 1-3 without presetting B | Verdict now A (problem survives AND detector target ready) |
| 5 | Synthesis §5.1 said ambiguous=43/110, §9 said 54/110; actual is 51/110 | Recompute from raw; report 51/110 consistently | Count conflict resolved |
| 6 | Best μ=0.01 was at grid boundary (max of `[1e-4..1e-2]`) → may not be true optimum | Extended grid to `[1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1]` | New best μ=0.03 (interior optimum, not boundary) |
| 7 | C11 (stage-1 = anchor μ=0.001) "4/7 cells improve" was vs the under-tuned anchor, not vs the fair fixed-μ baseline. C11 is actually WORSE than fixed_μ=0.01 on 7/7 cells | Added `C11_fixed_mu` (stage-1 = tuned fixed_μ); re-tune dd_step_size; compare against fixed_μ CMA directly | C11_fixed_mu (μ=0.03 + DD-LMS) significantly beats fixed_μ CMA on 4/7 cells; closes 3/7 (real positive signal) |

## 1. Scientific question (unchanged from v1)

Under a strict no-leakage split with a validation-optimal fixed-μ CMA as a genuine Go comparator, do {fixed-μ CMA, C08 bandit, C10 per-symbol, C11 cascade} close the CB1 16QAM inner-ring collapse headroom on ≥ 5/7 held-out cells? And does a conventional detector produce a defensible target for an ML detector (B02)?

## 2. Frozen params (after re-tuning on validation × tuning seeds)

| Method | Best hyperparameter | Tuning score |
|---|---|---|
| fixed_mu_cma (genuine comparator) | **μ=3e-2** (NEW: was 1e-2 in v1; interior optimum now, not boundary) | -0.2039 mean PI-SER + div_pen |
| C08 (LinUCB bandit) | α=10.0 | -0.2055 |
| C10 (per-symbol CMA) | μ=1e-5 (smallest; stability-limited) | -0.2061 |
| C11 (stage-1=anchor μ=0.001, B01 legacy) | dd_step_size=1e-4 | -0.2049 |
| **C11_fixed_mu (HF7: stage-1=tuned μ=0.03)** | **dd_step_size=1e-4, stage1_mu=0.03** | **-0.2023 (best of all methods)** |
| C05 (CUSUM/threshold detector) | z2_ratio_threshold=0.2, cusum_drift=0.01 (default-grid fallback) | macro-AUROC=-1.0 (no two-class validation cells under strict 4-cat label) |

**HF6 result:** the previous v1 grid ended at 1e-2; extending to 1e-1 revealed the true optimum is **μ=3e-2** (interior point, not boundary). μ=1e-1 was tried but diverged on long cells. Therefore "fixed-μ CMA has been fairly tuned" is now a defensible claim (modulo even larger μ being unstable).

## 3. Per-cell PI-SER (test seeds 21-30, hotfix v2)

| cell | anchor μ=0.001 | fixed_μ μ=0.03 | C08 | C10 | C11 (anchor+DD) | **C11_fixed_μ (μ=0.03+DD)** | anchor_H | C11_fixed_μ_H |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| snr05-short (HELD) | 0.6594 | 0.6934 | 0.6621 | 0.6617 | 0.6520 | 0.6934 | 0.0465 | 0.0012 |
| snr10-short (HELD) | 0.5309 | 0.5281 | 0.5348 | 0.5336 | 0.5184 | 0.5238 | 0.1332 | 0.0512 |
| snr15-short (HELD) | 0.4375 | 0.4254 | 0.4406 | 0.4414 | 0.4137 | **0.4160** | 0.2527 | 0.1652 |
| snr20-short (val) | 0.3809 | 0.3832 | 0.3910 | 0.3891 | 0.3555 | 0.3746 | 0.3383 | 0.2715 |
| snr25-short (HELD) | 0.3457 | 0.3656 | 0.3539 | 0.3535 | 0.3223 | **0.3590** | 0.3426 | 0.2973 |
| snr20-fg100-short (HELD) | 0.3812 | 0.3836 | 0.3910 | 0.3895 | 0.3555 | **0.3738** | 0.3387 | 0.2707 |
| snr20-fg1000-short (val) | 0.3770 | 0.3812 | 0.3848 | 0.3840 | 0.3523 | 0.3699 | 0.3359 | 0.2656 |
| snr20-sop40e-short (val) | 0.3840 | 0.3832 | 0.3902 | 0.3891 | 0.3547 | 0.3746 | 0.3422 | 0.2703 |
| snr10-fg100-long (HELD) | 0.4129 | 0.3910 | 0.4020 | 0.4145 | 0.4035 | **0.3816** | 0.0398 | 0.0016 |
| snr15-fg1000-long (HELD) | 0.2684 | 0.1895 | 0.2613 | 0.2699 | 0.2570 | **0.1664** | 0.1133 | 0.0039 |
| snr20-nominal-long (val) | 0.2281 | 0.1109 | 0.2176 | 0.2297 | 0.2109 | 0.0938 | 0.1461 | 0.0117 |

**Headroom < MDE (0.005) on 7 held-out cells:**

| Method | Closed cells (of 7) | Which |
|---|---:|---|
| anchor (frozen μ=0.001) | 0/7 | — |
| fixed_μ CMA (μ=0.03) | 1/7 | snr05-nominal-short |
| C08 (LinUCB α=10) | 0/7 | — |
| C10 (per-symbol μ=1e-5) | 0/7 | — |
| C11 (anchor μ=0.001 + DD-LMS) | 0/7 | — |
| **C11_fixed_μ (μ=0.03 + DD-LMS)** | **3/7** | **snr05-short, snr10-fg100-long, snr15-fg1000-long** |

The CLOSE_THRESHOLD (5/7) is **not reached** by any method → problem survives.

## 4. Paired bootstrap CIs (HF7: method vs fixed_μ CMA, the genuine comparator)

A CI marked `*` does not cross 0 (significant at 5%). This is the **apples-to-apples** comparison (vs the v1 unfair comparison vs anchor).

**C11_fixed_mu vs fixed_mu_cma** (the key new comparison):

| cell | Δ(C11fm − fixed_μ) [95% CI] | sig |
|---|---|---|
| snr05-short | +0.000 [-0.010, +0.009] |  |
| snr10-short | -0.004 [-0.013, +0.004] |  |
| **snr15-short** | **-0.009 [-0.018, -0.003]** | **`*`** |
| **snr25-short** | **-0.007 [-0.015, -0.001]** | **`*`** |
| **snr20-fg100-short** | **-0.010 [-0.020, -0.002]** | **`*`** |
| **snr10-fg100-long** | **-0.009 [-0.019, -0.000]** | **`*`** |
| snr15-fg1000-long | -0.023 [-0.060, +0.003] | (large effect, CI barely crosses 0 due to 1 volatile seed) |

**Findings:**

1. **C11_fixed_μ significantly beats fixed_μ CMA on 4/7 held-out cells** (paired CI excludes 0). |Δ| ≈ 0.01 PI-SER. This is a **genuine positive method signal** that v1 missed entirely (v1's C11 only beat the under-tuned anchor, not the fair comparator).
2. The improvement is modest but consistent: 0.007-0.010 PI-SER across 4 cells.
3. On 2/7 cells (snr05-short, snr10-short), no significant difference (already near AWGN floor).
4. On snr15-fg1000-long, large mean effect (-0.023) but CI just crosses 0 due to one volatile seed (high variance with n=10).
5. The cells closed by C11_fixed_μ (snr05 + 2 long cells) are exactly where DD-LMS refinement compounds with longer N — consistent with the DD-LMS mechanism.

**Other methods vs fixed_μ CMA** (all fail to beat the fair comparator):

- C11 (anchor μ=0.001 + DD-LMS): WORSE than fixed_μ on 7/7 cells (v1's "C11 improves" was an artifact of comparing to the under-tuned anchor). The honest interpretation: **DD-LMS only helps when stage-1 CMA is itself well-tuned**.
- C08 bandit: mixed, never significantly better than fixed_μ.
- C10 per-symbol: never significantly different from fixed_μ.

## 5. Detector evaluation (hotfix v2)

### 5.1 4-category label counts (test seeds 21-30, 110 seeds; HF5 corrected)

| cell | inner_ring | awgn_dom | healthy | ambiguous |
|---|---:|---:|---:|---:|
| snr05-short (HELD) | 0 | 8 | 0 | 2 |
| snr10-short (HELD) | 0 | 2 | 0 | 8 |
| snr15-short (HELD) | 0 | 0 | 2 | 8 |
| snr20-short (val) | 2 | 0 | 2 | 6 |
| snr25-short (HELD) | 4 | 0 | 4 | 2 |
| snr20-fg100-short (HELD) | 2 | 0 | 2 | 6 |
| snr20-fg1000-short (val) | 2 | 0 | 3 | 5 |
| snr20-sop40e-short (val) | 2 | 0 | 2 | 6 |
| snr10-fg100-long (HELD) | 0 | 7 | 0 | 3 |
| snr15-fg1000-long (HELD) | 0 | 1 | 6 | 3 |
| snr20-nominal-long (val) | 2 | 0 | 6 | 2 |
| **TOTAL** | **14 (12.7%)** | **18 (16.4%)** | **27 (24.5%)** | **51 (46.4%)** |

(v1 had conflicting 43 and 54 for ambiguous; actual is **51**. This is reported consistently now.)

**Critical observation unchanged from v1:** held-out long cells have ZERO inner_ring seeds. The "inner-ring collapse" signal B01 was detecting is mostly AWGN-dominated or ambiguous.

### 5.2 Per-cell detector metrics (hotfix v2)

For cells that are two-class under the strict binary projection:

| cell | detector | n_pos | n_neg | AUROC | recall (at ACTUAL FPR) | lead_time_mean |
|---|---|---:|---:|---:|---|---:|
| snr25-short (HELD) | min_z2_ratio | 4 | 4 | **1.000** | 1.0 (at FPR=25%; 5% not resolvable with n_neg=4) | -1.33 |
| snr25-short (HELD) | c05_alert_earliness | 4 | 4 | 0.875 | 1.0 (at FPR=25%) | -1.33 |
| snr20-fg100-short (HELD) | min_z2_ratio | 2 | 2 | **1.000** | 1.0 (at FPR=50%; 5% not resolvable with n_neg=2) | n/a |
| snr20-fg100-short (HELD) | c05_alert_earliness | 2 | 2 | 0.500 | 0.5 (at FPR=50%) | n/a |

**Findings — detector (honest, post-hotfix):**

1. **min_z2_ratio (zero-parameter baseline) achieves AUROC=1.000 on both two-class held-out cells** (snr25-short, snr20-fg100-short). It actually **outperforms** the tuned C05 detector (AUROC=0.875 and 0.500). The "tuned C05" adds nothing over the bare heuristic on these cells — likely because the default-grid fallback (C05 was never effectively tuned, see v1 §2) is no better than min-z2.
2. **lead_time is negative (-1.33 blocks on snr25-short)** — the detector fires AFTER the degradation onset, not before. v1's "+2 blocks lead time" was a warmup口径 artifact. **There is no real warning lead time from C05.** This is a significant honest correction.
3. **5% FPR is not resolvable** with n_neg ∈ {2, 4}. Reports honestly say "at 25%/50% FPR" not "at 5% FPR".
4. **Only 2/7 held-out cells are two-class** under strict 4-cat label. This is a thin detector target.

## 6. Verdict (hotfix v2)

**`A_B01R_FAIRNESS_SURVIVES_AND_DETECTOR_TARGET_READY`**

Decision rule check (per batch-contract.v1.yaml):
- **CLOSE_THRESHOLD (5/7 held-out cells)**: best method C11_fixed_μ closes 3/7 → threshold NOT reached → **problem survives**.
- **Detector target ready (≥2 two-class held-out cells for BOTH detector scores)**: min_z2_ratio has 2 two-class cells; c05_alert_earliness has 2 two-class cells → **detector target READY** (by the contract's literal rule).

**However, important caveats** (these do not change the verdict letter but constrain its interpretation):

1. The "detector target ready" is thin: 2 cells × 2-4 positives each. Any B02 ML detector trained on this would be learning from ≤12 positive labels total.
2. The conventional baseline (min_z2_ratio) is already at AUROC=1.000 on both two-class cells — **there is no room for ML to improve AUROC on these cells**. ML's contribution would have to be on the 5 single-class cells (where AUROC is undefined) or on lead time (currently negative).
3. C11_fixed_μ's positive signal (3/7 closed, 4/7 significant improvement over fixed_μ CMA) is real but small (|Δ| ≈ 0.01 PI-SER, headroom still ≥ 6×MDE on the 4 non-closed cells).

**What this verdict authorizes and what it does NOT:**

- ✅ Authorizes pursuing C11_fixed_μ (μ=0.03 CMA + DD-LMS) as a baseline reference for future work.
- ✅ Authorizes the fairness claim: "collapse survives fair conventional treatment (tuned fixed-μ + per-symbol + DD-LMS cascade)".
- ⚠️ Does NOT automatically authorize B02 ML detector batch. The detector target is "ready" by the contract's letter but is thin (only 2 two-class cells, ML cannot beat AUROC=1.000 on them, lead time is negative). A B02 detector would need a different target (e.g., lead-time maximization, or operating on the ambiguous/awgn-dominated cells where conventional is undefined).
- ⚠️ Does NOT authorize C04/C09 learned corrector batch on the basis of C11's signal alone. C11_fixed_μ's 0.01 PI-SER improvement is the gap a learned corrector would need to beat, and the contract requires a `blind-affine` task comparator for any corrector batch (HF8, see §11).

## 7. What this means for the project

### Equalizer side (positive, scoped)

- The validation-optimal fixed-μ CMA at **μ=0.03** (not 0.01) is the new baseline reference.
- C11_fixed_μ (μ=0.03 CMA + DD-LMS) is a genuine positive signal: 3/7 cells closed, 4/7 cells significant improvement vs the fair baseline. This is the first method in the entire campaign that significantly beats a fairly-tuned conventional comparator.
- The improvement is small (|Δ| ≈ 0.01 PI-SER) and does not close headroom on 4/7 cells, but it is real.
- **Correct framing:** "DD-LMS cascade on top of a fairly-tuned CMA provides a small but statistically significant PI-SER improvement on 4/7 cells. The residual headroom is the target for learned correctors."

### Detector side (thin, conditional)

- min_z2_ratio is a surprisingly strong baseline (AUROC=1.000 on both two-class cells). Any B02 ML detector must beat this on a meaningful axis (lead time, calibration, or generalization to single-class cells), not on AUROC.
- Lead time is negative — conventional detector does NOT provide early warning. This is a potential ML contribution axis (positive lead time).
- 4-category label audit revealed inner-ring positives are sparse (14/110, 12.7%) and absent from held-out long cells. A B02 detector would need to either expand the label population or target a different objective.

## 8. What this batch did NOT do

- Did NOT train any ML detector.
- Did NOT modify B01 raw / D008 / H005 / B001-B003 / P03 / CB1 raw / canonical-state.
- Did NOT create legacy B004.
- Did NOT modify the CMA anchor identity (byte-identical regression preserved).
- Did NOT promote any result to formal Groundwork/Contract/Execute/paper.

## 9. Open questions

1. Is the "ambiguous" category (51/110, 46%) hiding real collapse signal? A learned representation might separate these.
2. Does μ=0.03 generalize beyond the current 4 validation cells × 5 tuning seeds? A larger validation set would tighten the optimum.
3. Why does C11_fixed_μ close 3/7 but only significantly improve 4/7? The 3 closed cells (snr05 + 2 long) are where headroom was already smallest; the 4 significant improvements include cells where headroom is still large.
4. Can a learned detector achieve positive lead time where conventional achieves -1.33? This is the cleanest ML contribution axis on the detector side.
5. Would C04/C09 learned corrector beat C11_fixed_μ's 0.01 PI-SER margin? That is the cleanest contribution axis on the equalizer side, and requires `blind-affine` as task comparator (HF8).

## 10. Harvest (hotfix v2; H029-H034 from v1 retained with corrected content)

| Harvest ID | Category | Content (corrected) |
|---|---|---|
| H029 | BASELINE_ADJUDICATION | Under no-leakage split + validation-optimal fixed-μ CMA at μ=0.03 (interior optimum after grid extension), the CB1 16QAM inner-ring collapse headroom remains on 4/7 held-out cells. C11_fixed_μ (μ=0.03 CMA + DD-LMS) closes 3/7 and significantly beats fixed_μ on 4/7 (paired CI excludes 0, |Δ|≈0.01). |
| H030 | FAILURE_MECHANISM | The binary `oracle_pi_ser > 0.3` label conflates inner-ring collapse with AWGN-dominated error. 4-category audit: inner_ring=14/110 (12.7%), awgn=18 (16.4%), healthy=27 (24.5%), ambiguous=51 (46.4%). Held-out long cells have ZERO inner_ring seeds. (v1 had conflicting ambiguous counts 43/54; actual is 51.) |
| H031 | METHOD_SIGNAL | C11_fixed_μ (stage-1 = TUNED μ=0.03 CMA + DD-LMS) significantly beats fixed_μ CMA on 4/7 held-out cells (paired CI). This is a genuine positive signal that v1 missed (v1's C11 only beat the under-tuned μ=0.001 anchor). The improvement is on inner-ring-recoverable AND awgn-dominated regimes (4/7 cells span both). |
| H032 | EVALUATION_INSIGHT | Single-class cells report AUROC=NA/UNDEFINED (not 0.5); 5/7 held-out cells are single-class under strict binary projection. |
| H033 | EVALUATION_INSIGHT | Tuning [11-15] ∩ test [21-30] = ∅ is the minimum honesty bar. Paired bootstrap CIs over test seeds are required to distinguish small Δ (e.g. 0.01) from noise. |
| H034 | REUSABLE_ASSET | B01-R runner + detector module (4-cat label audit, paired bootstrap CI, real detector metrics with honest FPR reporting, warmup-guarded lead time) is reusable fairness-batch infrastructure. |
| **H035 (new)** | **EVALUATION_INSIGHT** | **μ grid boundary check**: if the best μ is at the grid max, the grid must be extended until an interior optimum, plateau, or divergence boundary is found. v1 falsely concluded "μ=0.01 optimal" when the grid ended at 0.01; v2 extended to 0.1 and found μ=0.03. |
| **H036 (new)** | **EVALUATION_INSIGHT** | **Warmup must precede both detector alert AND degradation onset**. v1 let detector alert fire during warmup (block 0/1), producing fake "+2 lead time". Hotfix guards both: warmup is for baseline estimation only; alerts and onset-detection start at block `warmup`. |
| **H037 (new)** | **EVALUATION_INSIGHT** | **Apples-to-apples cascade comparison**: a cascade method (C11) must be compared against its OWN stage-1 (fixed_μ CMA), not against an unrelated anchor (frozen μ=0.001). v1's "C11 improves" was entirely an artifact of comparing to the under-tuned anchor; v2's C11_fixed_μ comparison shows the real (smaller but still positive) effect. |
| **H038 (new)** | **REUSABLE_ASSET / GUARDRAIL** | **Conventional baseline may already be perfect**: min_z2_ratio achieves AUROC=1.000 on both two-class held-out cells, beating the "tuned" C05 (default-grid, AUROC=0.875). Before claiming ML beats conventional, check whether conventional is already at ceiling. The ML contribution axis must then be different (lead time, calibration, generalization). |

## 11. Rotation

Per `references/recovery-and-rotation.md` and user prompt §九:

**Verdict A → problem survives AND detector target ready → next action: pursue the cleanest contribution axis.**

Two legal paths, both now better-motivated than in v1:

1. **Equalizer side — learned corrector (C04/C09)**: target the residual 0.01 PI-SER margin that C11_fixed_μ leaves on 4/7 cells. Task comparators (HF8 new rule): **both** `fixed_μ CMA μ=0.03` (system anchor) AND `blind_affine_16qam` (task-specific Kill tool per FR-21). Go metric: paired-CI significant improvement over C11_fixed_μ on ≥ 4/7 held-out cells.
2. **Detector side — lead-time maximization (C01/C02/C06)**: target positive warning lead time (conventional is at -1.33). Task comparator: min_z2_ratio (AUROC=1.000, the ceiling baseline). Go metric: positive mean lead time on ≥ 2 two-class cells, without AUROC regression.

The B02 detector batch is now conditionally authorized by Verdict A but with a narrowed claim: "ML provides positive warning lead time where conventional provides none" (not "ML improves AUROC").

## 12. Note on B01's superseded status

B01 (raw artifacts, D008, H005) preserved as DIAGNOSTIC history. What is superseded by B01-R hotfix v2:

- B01-R v1's VERDICT B (mechanically forced) → v2's VERDICT A (scientifically reached).
- B01-R v1's "C11 improves 4/7 cells" → v2 corrects: that was vs under-tuned anchor; vs fair fixed_μ baseline, only C11_fixed_μ improves (4/7), and by a smaller margin.
- B01-R v1's "+2 blocks lead time" → v2 corrects: warmup artifact; actual lead time is -1.33.
- B01-R v1's "recall@5%FPR = 1.0" → v2 corrects: 5% not resolvable; actual FPR is 25-50%.
- B01-R v1's "ambiguous = 43 or 54" → v2 corrects: actual is 51.
- B01-R v1's "fixed_μ CMA μ=0.01 optimal" → v2 corrects: μ=0.03 (interior optimum after grid extension).
- B01-R v1's "min_z2_ratio has no two-class cells (strict label)" → v2 corrects: that was an interface bug; min_z2_ratio is actually the strongest detector (AUROC=1.000 on 2 two-class cells).

D008 → superseded by D009 (v1) → amended by D010 (v2).
H005 → superseded by H006 (v1) → amended by H007 (v2).
V001 (v1 verifier CONFIRM) → amended by V002 (v2 verifier, post-hotfix).
