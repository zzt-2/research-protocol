# T029 — P02 cand_rank Operating-Regime Confirmation (Package P02)

> Task: T029-p02-cand-rank-operating-regime-confirmation
> Source: S003 / D039 campaign authorization; P01 produced `NO_DIAGNOSTIC_SIGNAL`
> but a documented conditional sub-population signal (cand_rank @ weak/低SNR
> +0.32~+0.43 dB vs adapter, held-out 30–49). P02 is the *fresh confirmation*
> of that operating-regime signal under a frozen, dev-adjudicated cheap alternative.
> Family: A_CPR_selector_robustness (same family as P01; consecutive=1, this is the
> permitted 2nd same-family package; P03 must switch family).
> Worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
> Python (anchor-provenance 3.11.9): `/c/Users/zzt/scoop/apps/python311/current/python`.
> Date: 2026-07-30

## 0. Package question (frozen)

Does cand_rank's advantage genuinely confine itself to the continuous operating
region "weak turbulence, low SNR, original-selector boundary mismatch" and beat
both the conventional pilot-SNR adapter AND the strongest cheap region-retuned
threshold? P02 must answer this with FRESH held-out seeds that never touched
P01 dev (0–9) / held-out (30–49) / historical pollution (71–80) / anchor (0–29).

## 1. Pre-registered target & boundary regions (frozen BEFORE any new test data)

**Primary target region (frozen):**
- turbulence = `weak`
- SNR ∈ {5, 7, 9} dB
- estimator = per-cell paired mean of cand_rank − conventional adapter

**Boundary / control region (frozen):**
- `weak` @ 11 dB  (P01 showed cand_rank decay to +0.111 here → expect drop-off)
- `moderate` @ {5, 7, 9} dB  (P01 showed +0.05~+0.12, well below MDE)
- nominal / mismatch-free control: every cell at δ=0 IS the mismatch-free
  control (the shared realization; adapter and cand_rank are both δ-invariant
  in their internal estimates, so the operating-regime contrast is tested at
  δ=0 rows which carry no SNR-mismatch).

**LOCK:** Do not delete any target cell or re-select a better subgroup after
seeing fresh numbers. All 3 target cells count; both boundary cells count.

## 2. Frozen method identities (verified line-for-line vs P01 source)

All candidates reuse the EXISTING frozen P01 implementations; P02 adds NO new
method logic. Identity is pinned by source path + function, not by re-derivation.

| role | frozen source (file:line) | deployable action |
|---|---|---|
| inherited selector | `_a4_switch_common768_30seed.py:97-107` `A.decide` | CV stage-1 + γ_eff stage-2 on biased γ̂ |
| conventional adapter | `_p01_adapter_and_candidates.py:106-114` `decide_adapter_pilot` | noncoherent-block pilot γ_est + original `A.decide`; δ-invariant |
| **candidate** | `_p01_adapter_and_candidates.py:205-217` `decide_cand_rank` | stage-1 boundary fixed at ref_snr_db=9.0 (γ-magnitude-FREE) + pilot-est stage-2 |
| **cheap alternative** | NEW wrapper `decide_adapter_weakretune` (see §3) | SAME conventional adapter structure but with ref_snr_db TUNED on dev only |
| true SNR bound | `_p01_phaseBC.py:84-88` `_oracle_decide_factory` | true γ fed to A.decide — UPPER BOUND only, excluded from every decide |

**Structural difference cand_rank vs cheap-alternative (MUST be clear):**
- cand_rank fixes ref_snr_db = 9.0 (frozen design constant, NOT tuned post-hoc).
- cheap-alternative reuses cand_rank's exact stage-1 structure but searches
  ref_snr_db ∈ {7,8,9,10,11} on DEV seeds 50–59, picks the dev-best, then
  evaluates that single frozen choice on held-out. This isolates whether
  cand_rank's 9.0 dB constant is itself the win, or whether any reasonable
  region-retune of the SAME conventional lever already captures the gain
  (→ PROBLEM_RESOLVED_BY_REGION_RETUNING). If there is no different
  deployable action between cand_rank and the retuned version, P02 cannot
  adjudicate a new method.

## 3. Cheap alternative — frozen dev-search protocol

`decide_adapter_weakretune(raw, gamma_hat_db, gamma_hat_lin, b)` =
cand_rank's body with `ref_snr_db` replaced by a module-global frozen at
dev-time. Search space (frozen, dev seeds 50–59, target cells only):
ref_snr_db ∈ {7.0, 8.0, 9.0, 10.0, 11.0}. Selection rule (frozen): pick the
ref maximizing the mean paired (retune − adapter) over the 3 target cells on
dev. Tie-break: smallest ref. Freeze that ref; never touch dev again.

## 4. Fresh confirmation discipline (frozen)

- **New seed ranges (disjoint from ALL prior use):**
  - dev (cheap-alt tuning + criterion exploration) = seed_index 50–59
  - fresh held-out test = seed_index 60–69  (30+ paired seeds: use 60–69 = 10
    per cell × 3 target cells = 30 paired; to guarantee ≥30 paired per the
    brief, RUN 60–89 i.e. 30 seeds per cell). **Final: held-out = 60–89.**
  - Verified disjoint from anchor 0–29, P01 dev 0–9, P01 held-out 30–49,
    pollution 71–80. NOTE 71–80 is inside 60–89 → EXCLUDE 71–80.
  - **Final held-out = seed_index {60..70} ∪ {81..89} = 30 seeds** (exclude
    the polluted 71–80). dev = 50–59.
- Same realization shared across methods (paired): one channel generation per
  (scene, γ_true, seed), all selectors evaluated on identical windows.
- raw rows + branch occupancy + selection error + gain + BER/Q saved.
- **primary estimand** = target-region cand_rank − conventional adapter,
  seed-cluster paired mean over the 3 target cells (n = 30 paired diffs).
- **MDE = +0.15 dB (frozen, SAME as P01 — do not lower the bar).**
- Report 95% paired Student-t CI, help/hurt/tie counts.
- Secondary (only after primary): per-cell and boundary analysis.

## 5. Adjudication order (frozen, applied in this exact sequence)

1. **Cheap region-retuned threshold already reaches cand_rank?**
   - If (cand_rank − retune) target-region mean ≤ MDE in magnitude AND the
     retune's own (retune − adapter) ≥ cand_rank's (cand_rank − adapter)
     within MDE → `PROBLEM_RESOLVED_BY_REGION_RETUNING`.
2. **cand_rank target-region confirmation (ALL must hold):**
   - paired mean ≥ +0.15 dB;
   - CI lower > 0;
   - ≥ 2/3 target cells direction-consistent (all positive, CI_low>0) AND no
     single cell carries the whole signal (remove best cell → pooled over
     remaining 2 still mean>0);
   - boundary/control shows no catastrophic degradation (no boundary cell
     where cand_rank − adapter < −0.5 dB with CI_high<0).
3. All hold → `BOUNDED_DIAGNOSTIC_METHOD_SIGNAL`.
4. Else → `NO_CONFIRMATION`.
5. Data / identity / information-boundary failure → `EXECUTION_INVALID`.

P01's old subgroup numbers MUST NOT add credit to P02; P02 only counts the
fresh held-out confirmation.

## 6. On confirmation success

Generate one bounded method card (same package): technical action, deployable
inputs, conventional adapter, cheap alternative, target operating region,
primary/fallback packaging, claim ceiling = `LOCAL_OPERATING_REGIME /
DIAGNOSTIC`. Must NOT be written as a formal paper victory or active carrier;
promotion needs GW Step 1–3/3.5/4a.

## 7. Verification & campaign

- Independent executor implements + runs.
- Independent verifier re-derives raw→aggregate, seed isolation, formula
  identity, cheap alternative, and the verdict.
- One in-package deterministic fix allowed.
- P02 valid → accepted_valid_packages → 2/10; family A consecutive → 2,
  then forced exit; P03 must switch mechanism family.

## 8. New-file discipline (P01 contract preserved)

New files ONLY; do NOT edit `common/`, `params.py`, `_a4_switch_common768_30seed.py`,
`_p01_adapter_and_candidates.py`, `_p01_cpr_snr_mismatch_probe.py`,
`_p01_phaseBC.py`, `_a4_branchrouted_30seed.py`, `sc_nda_ml_sim.py`, or the
anchor JSON. New P02 files under `explore/nda-awgn-tracking-sandbox/`:
- `_p02_operating_regime_probe.py` (fresh confirmation runner)
- `_p02_weakretune_adapter.py` (cheap alternative, dev-tuned ref)
- artifacts: `results/p02_cand_rank_operating_regime/{dev_tuning.json, heldout_confirmation.json}`
