# step-029 — P02 cand_rank Operating-Regime Confirmation (Independent Executor)

> Task: T029-p02-cand-rank-operating-regime-confirmation (Package P02, family A_CPR_selector_robustness)
> Source: S003 / D039 campaign authorization; brief at
> `.sessions/2026-07-23-research-direction-lab-longitudinal-test/T029-p02-cand-rank-operating-regime-confirmation.md`
> Worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
> Python (anchor-provenance 3.11.9): `/c/Users/zzt/scoop/apps/python311/current/python`
> Date: 2026-07-30
> TERMINAL VERDICT: **PROBLEM_RESOLVED_BY_REGION_RETUNING** (P01's conditional sub-population
> signal does NOT survive as a distinct method — a dev-tuned region-retune of the SAME
> conventional lever captures and slightly exceeds cand_rank's gain).

## 0. Mission recap

P01 (CP030/V065) closed `NO_DIAGNOSTIC_SIGNAL` overall but documented a conditional
sub-population signal: cand_rank (γ-magnitude-free stage-1 boundary at fixed ref=9 dB +
pilot-est stage-2) beat the conventional pilot-SNR adapter by +0.32~+0.43 dB specifically
at weak-turbulence low-SNR cells, on P01 held-out seeds 30–49. P02 is the FRESH
confirmation of that operating-regime signal, with a frozen dev-adjudicated cheap
alternative (region-retuned threshold) that tests whether cand_rank's frozen 9 dB
constant is load-bearing.

## 1. CRITERION FREEZE — written BEFORE any new test data (T029 §1-§5)

**Frozen target region:** weak × {5,7,9} dB, δ=0 rows (mismatch-free control; adapter
and cand_rank are δ-invariant in their internal estimates).
**Boundary/control:** weak@11, moderate@{5,7,9} (4 cells).
**MDE frozen = +0.15 dB (same as P01; NOT lowered).** primary estimand = target-region
(cand_rank − adapter) paired mean over 3 cells × 30 seeds.

**Frozen method identities (reuse existing code, add NO new method logic):**
- inherited selector `A.decide`; conventional adapter `decide_adapter_pilot`;
- candidate `decide_cand_rank` (ref_snr_db=9.0 FIXED);
- cheap alternative `decide_adapter_weakretune` = cand_rank body with ref_snr_db
  replaced by a module-global frozen at dev-time;
- true SNR = oracle upper bound only, never in any deployable decide.

**Frozen §5 adjudication order:** (1) cheap-alt reaches cand_rank →
PROBLEM_RESOLVED_BY_REGION_RETUNING; (2) cand_rank target all-hold →
BOUNDED_DIAGNOSTIC_METHOD_SIGNAL; (3) else NO_CONFIRMATION; (4) EXECUTION_INVALID.

**Seed discipline (frozen, disjoint from ALL prior use):** dev=50–59; held-out
fresh test = {60..70}∪{81..89}∪{90..99} = 30 seeds (90–99 added by the
controller-authorized in-package deterministic fix — the original `{60..70}∪{81..89}`
text yields only 20 seeds; 90–99 is fully disjoint from anchor 0–29, P01 dev 0–9,
P01 held-out 30–49, dev 50–59, pollution 71–80).

## 2. Dev tuning (seeds 50–59, 3 target cells, δ=0) — `_p02_weakretune_adapter.py`

ref_snr_db search ∈ {7,8,9,10,11}, selection = max mean(weakretune − adapter) over
target cells, tie → smallest ref. Means monotone-increasing in ref:
7→0.222, 8→0.297, 9→0.369, 10→0.414, **11→0.462**. Chosen ref = **11.0 dB**
(unique argmax, no tie). cand_rank−adapter audit ref-invariant (+0.369 across all
refs — confirms cand_rank's 9.0 is a frozen constant, independent of the weakretune
search). Frozen ref=11.0; dev never touched again.

## 3. Fresh held-out confirmation (seeds 60–99\{71–80}, 7 cells, δ=0)

n = 30 seeds/cell (7350 raw rows total: 7 cells × 30 seeds × 7 δ × 5 methods incl oracle).

**PRIMARY — target-region cand_rank − adapter (n=90 paired = 3 cells × 30):**
mean **+0.3578 dB**, CI95 **[+0.3381, +0.3775]**, help/hurt/tie = **90/0/0**.
mean≥MDE ✓, CI_low>0 ✓.

**Per target cell (cand_rank − adapter):**
| cell | mean | CI95 | help/hurt/tie | beats by MDE? |
|---|---|---|---|---|
| weak@5 | +0.3665 | [+0.3449,+0.3881] | 30/0/0 | YES |
| weak@7 | +0.4279 | [+0.3978,+0.4580] | 30/0/0 | YES |
| weak@9 | +0.2790 | [+0.2506,+0.3075] | 30/0/0 | YES (CI_low>0; mean<0.15 fail only at strict pooled-cell reading, but CI_low>0) |

All 3/3 target cells positive, CI_low>0. Single-cell-dominance: drop best (weak@7) →
remaining-2 mean = **+0.3228**, still strongly positive → no single cell carries the signal.

**Cheap-alternative adjudication (target region):**
| comparison | mean | CI95 |
|---|---|---|
| weakretune − adapter | **+0.4539** | [+0.4333,+0.4744] |
| cand_rank − weakretune | **−0.0961** | [−0.1060,−0.0862] |

weakretune (dev-tuned ref=11) actually BEATS cand_rank (ref=9) by +0.096 dB.
|cand_rank − weakretune| = 0.0961 ≤ MDE(0.15) ✓.

**Boundary (cand_rank − adapter), no catastrophic (none < −0.5 & CI_high<0):**
weak@11 +0.0960; moderate@5 +0.0987; moderate@7 +0.1234; moderate@9 +0.1204. All
small positive, well below MDE — consistent with P01's "signal confined to weak/低SNR".

## 4. Terminal verdict: **PROBLEM_RESOLVED_BY_REGION_RETUNING**

§5 Step 1 fires unambiguously (both conditions hold with wide margin):
- |cand_rank − weakretune| = 0.0961 ≤ MDE = 0.15 ✓
- weakretune − adapter (0.4539) ≥ cand_rank − adapter − MDE (0.3578 − 0.15 = 0.2078) ✓

**Interpretation:** cand_rank's frozen design constant ref=9.0 dB is NOT load-bearing.
A dev-tuned region-retune of the SAME conventional lever (raise the stage-1 reference
from 9→11 dB, selected on independent dev seeds) captures and slightly exceeds
cand_rank's gain. There is no distinct deployable action between cand_rank and the
retuned version → cand_rank does NOT constitute a new diagnostic method and does NOT
earn a bounded method card or promotion. This is an honest bounded negative that
RESOLVES P01's conditional sub-population signal: it was real, but it collapses into
a cheap conventional threshold retune.

**Robustness note:** Even Step 2 (the stronger METHOD_SIGNAL bar) would also pass on
these numbers (mean≥MDE, CI_low>0, 3/3 cells positive, no single-cell dominance, no
boundary catastrophic). But the frozen order forces Step 1 first, which short-circuits
to PROBLEM_RESOLVED_BY_REGION_RETUNING. The 20-seed pre-fix run gave the same verdict
(primary +0.354); the 30-seed consolidation shifted numbers only marginally (+0.354→
+0.358), so the verdict is stable to the seed-count fix.

## 5. Key numbers (for controller relay)

- weakretune chosen ref (dev) = 11.0 dB (cand_rank equivalent = 9.0).
- target cand_rank − adapter = +0.3578 [+0.3381,+0.3775], 90/0/0.
- weakretune − adapter = +0.4539 [+0.4333,+0.4744] (weakretune > cand_rank).
- cand_rank − weakretune = −0.0961 [−0.1060,−0.0862], |mean| ≤ MDE.
- per-target-cell: weak@5 +0.3665, weak@7 +0.4279, weak@9 +0.2790.
- boundary (no catastrophic): weak@11 +0.096, mod@5 +0.099, mod@7 +0.123, mod@9 +0.120.

## 6. Discipline items

- Reproduction: verifier independently re-ran weak@7 seeds 60,61 → byte-identical
  selected_errors / branch occupancy to artifact (V08 PASS).
- true γ never in any deployable decide (V04 AST audit PASS; only oracle_true upper
  bound, excluded from all adjudication aggregates).
- Shared channel `generate_shared_realization_apsk` (TL-13); one generation per
  (scene,γ_true,seed), all selectors on identical windows.
- dev 50–59 / held-out 60–99\{71–80} isolation verified (V02 PASS); no collisions.
- New files only; `git diff --stat HEAD` empty on all frozen files (common/, params.py,
  _a4_switch_common768_30seed.py, _p01_adapter_and_candidates.py,
  _p01_cpr_snr_mismatch_probe.py, _p01_phaseBC.py, _a4_branchrouted_30seed.py,
  sc_nda_ml_sim.py, anchor JSON).
- One in-package deterministic fix (seed-count arithmetic) applied, disclosed in
  artifact `meta.seed_consolidation`; criteria/dev-ref/methods/MDE/§5 order unchanged.

**Artifacts:** `projects/simulation/results/p02_cand_rank_operating_regime/{dev_tuning.json,
heldout_confirmation.json}`. Source: `projects/simulation/explore/nda-awgn-tracking-sandbox/
{_p02_weakretune_adapter.py,_p02_operating_regime_probe.py}`. Elapsed ≈ 412s (dev 231s +
held-out 181s) + consolidation ~120s.
