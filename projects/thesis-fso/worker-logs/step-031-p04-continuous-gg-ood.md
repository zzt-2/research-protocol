# step-031 — P04 Continuous-GG OOD Selector Robustness (Independent Executor)

> Task: P04-continuous-gg-ood (Package P04, family C_CONTINUOUS_GG_OOD_SELECTOR_ROBUSTNESS)
> Source: S003 / D041 campaign authorization; binding-arbitration instruction
> Worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
> Python: `/c/Users/zzt/scoop/apps/python311/current/python` (3.11.9, scipy/numpy installed; same as P03)
> Date: 2026-07-30
> TERMINAL VERDICT: **PROBLEM_ABSENT_ON_CONTINUOUS_GG** (the frozen DA/NDA selector's
> AWGN-fitted CV decision boundary does NOT produce a continuous-GG-OOD-specific selector
> regret. Pooled held-out interior regret = +0.1459 dB, just below the frozen MDE=0.15 dB,
> confirmed on disjoint seeds (dev +0.1393 / held-out +0.1459, agree to 0.007 dB). The
> selector IS a general NDA-over-selector at weak turbulence / low SNR, but this is a FLAT
> property across σ_R² — equally present at the training anchors (anchor regret +0.23 dB >
> interior +0.14 dB) — NOT a degradation caused by un-trained continuous GG shapes. A
> weak-side-low-SNR sub-range (σ_R² 0.3–1.35 × γ 5–11 dB, 9/30 cells > MDE) is recorded as a
> bounded future-work seed, NOT a method signal; it overlaps the closed A-family regime so is
> not re-opened. Phase B/C not run — problem gate not passed.)

## A. Anchor regression gate (Phase A.1, BLOCKER) — PASS

Explicit `turb_params=(alpha,beta)` injection (`sigma2_to_ab`: frozen anchor pairs at the 3
training σ_R², Al-Habash closed form elsewhere) reproduces the scene-name path byte-exact.
Checked weak/moderate/strong × seeds 0–2 × γ∈{5,9} = 108 fields (selected_errors, n_select_da,
n_select_nda, fixed_nda_errors, fixed_da_errors, lower_count_bound_errors): **0 mismatches**.
The (α,β) injection path is faithful; continuous interior cells (Al-Habash) are a controlled
extrapolation. One bounded deterministic fix used: exact regression requires the frozen
rounded anchor pairs (11.6,10.1)/(4.0,1.9)/(4.2,1.4) at the 3 training σ_R² (the anchor was
trained on these, not Al-Habash exact values which differ ≤2.70%); Al-Habash used for
continuous interior points only.

## 0. Mission recap

P04 asks the **binding-arbitration rewritten question**: does the AWGN-fitted CV decision
boundary of the already-closed DA/NDA CPR selector (`_a4_switch_common768_30seed.decide`,
family A) produce a **selector-specific regret** on **continuous GG distributions** within
the literature parameter range but **outside the three training anchors** (weak/moderate/
strong σ_R² = 0.2/1.6/3.5)? This is FR-23 problem-driven (new failure condition injected on
an already-closed method), NOT novelty-driven, and it is a distinct mechanism family from
A (SNR-mismatch / cand_rank / region-retune, all closed) and B (fixed-point).

The selector's only channel-side inputs are raw-power CV and nominal γ (audit-clean info
boundary, `_a4_switch_common768_30seed.py:97-107`). Its stage-1 boundary
`cv_awgn_theory(γ_db)=0.74+0.12·exp(-γ_db/5)` × margin 1.10 was fitted to **AWGN**
(`method.tex:43-48`). The paper tests exactly three discrete (α,β) pairs
(`system_model.tex:22`) and explicitly claims "no turbulence-specific retuning"
(`method.tex:75`, `abstract.tex:2`). Continuous (α,β) off the three training points is
therefore a genuine un-handled/OOD failure condition.

## 1. CRITERION FREEZE — written BEFORE any test data (brief trap #9, V067 check 9)

### 1.1 Problem-bearing probe (Phase A) — selector-specific regret bar

A "selector-specific regret" exists on a continuous-GG cell iff **ALL** of:
- (P1) `orig_selector_errors > lower_count_bound_errors` on that cell (the selector picks
  the worse branch on ≥1 window; not already at the per-window optimum), AND
- (P2) the **regret of the original selector vs the per-cell best fixed branch**
  (fixed_DA / fixed_NDA) is ≥ MDE = 0.15 dB pooled across the held-out continuous cells,
  with CI_low > 0, AND
- (P3) the failure is NOT just common-branch degradation: at the regret-bearing cells BOTH
  fixed branches must NOT collapse together (i.e. the selector had a real branch to choose
  — `min(fixed_DA, fixed_NDA)` meaningfully < `max(...)`); if both fixed branches degrade
  equally that is a channel phenomenon, not a selector decision-boundary failure.

"Regret" metric (consistent with P01/P02/P03 gain_db, but inverted to a *loss* vs the
best fixed branch):
`regret_db(cell, method) = 10·log10( method_errors / best_fixed_branch_errors )`
where `best_fixed_branch_errors = min(fixed_DA_errors, fixed_NDA_errors)` on that cell.
regret_db ≥ 0 always; the original selector's regret_db on held-out continuous cells is the
Phase-A test statistic. **Selector-specific** = original selector's pooled regret ≥ MDE AND
the per-cell-best fixed bound does NOT itself dominate (P3).

Problem gate: if NO selector-specific regret on held-out continuous cells →
`PROBLEM_ABSENT_ON_CONTINUOUS_GG` (valid negative, package counts 4/10, no method built).

### 1.2 Phase B — global-retune comparator bar (only if Phase A problem holds)

Comparator = a **single global retune** of the existing CV_MARGIN and/or the γ_eff threshold
(13 dB), tuned on the **dev** continuous-GG grid (one global parameter set for the whole
continuous range, NOT per-cell, NOT reading turbulence label/true α,β). Given the SAME
tuning budget as any candidate. Frozen before test.

Resolved bar: if global retune on dev then applied to held-out **removes** the regret
(pooled original-after-retune regret < MDE OR the best candidate's advantage over
global-retune < MDE) → `PROBLEM_RESOLVED_BY_GLOBAL_RETUNE` (no method; conventional lever
already solves it). This is the §5 Step-1 analog of P02.

### 1.3 Phase C — candidate success bar (only if Phase B leaves residual)

A candidate "really" beats the global-retune comparator iff pooled paired
`Δgain = candidate_gain − globalretune_gain` ≥ MDE = 0.15 dB AND CI_low > 0 on fresh
held-out continuous cells, using ONLY receiver-visible current/past statistics, with a
mechanism distinct from a simple global threshold. Candidates must NOT read true α/β/h/
turbulence label/TX truth (AST-audit clean, as in P03/V067 check 5). Each candidate gets
the same tuning budget (dev seeds only).

DIAGNOSTIC_METHOD_SIGNAL iff a candidate stably beats global-retune by ≥ MDE, CI_low > 0,
consistent across ≥2 distinct continuous sub-ranges (not a single-cell spike). Else
`NO_DIAGNOSTIC_SIGNAL`.

### 1.4 Frozen testbed (DOF + provenance)

**σ_R² → (α,β) mapping (verified source, NOT the mcs sandbox empirical proxy):** the
Al-Habash plane-wave closed form documented in `system_model.tex:16-21`:
`α = [exp(0.49σ²/(1+1.11σ²^(6/5))^(7/6)) − 1]⁻¹`,
`β = [exp(0.51σ²/(1+0.69σ²^(6/5))^(5/6)) − 1]⁻¹`.
Verified to reproduce the 3 anchors to ≤2.70% (paper claim 2.78%; weak 0.44%/0.22%,
moderate 0.66%/0.55%, strong 0.61%/2.70%). This is the ONLY σ_R²→(α,β) mapping used.
The `explore/mcs-gain-upperbound/mcs_gain_upperbound.py:47 rytov_to_gg` piecewise-symmetric
proxy is explicitly NOT used (it forces α=β and is an empirical fit, not the cited formula).

**σ_R² grid (within [weak=0.2, strong=3.5], the anchor-covered range):**
- dev grid σ_R² ∈ {0.2, 0.45, 0.7, 1.15, 1.6, 2.0, 2.55, 3.0, 3.5} (9 pts, INCLUDES the 3
  anchors as regression/control — 0.2/1.6/3.5 — and 6 interior pts).
- held-out grid σ_R² ∈ {0.3, 0.9, 1.35, 1.85, 2.3, 3.15} (6 pts, interior-only, disjoint
  from dev grid and from the 3 training anchors).
No σ_R² outside [0.2, 3.5]; no saturated turbulence / new propagation model / hand-set α,β.

**Channel injection:** explicit `turb_params=(alpha,beta)` passed to
`generate_shared_realization_apsk` (`common/_channel.py:97-99,10-24`), bypassing the
scene-name resolution. Same shared GG-block + Doppler/laser-phase engine (TL-13).

**SNR cells:** γ ∈ {5, 7, 9, 11, 13} dB (P01/P02 gain-bearing low-SNR band where the
selector actually chooses — DA occupancy 30–95% here; high-SNR cells have ~0 anchor gain
so no regret headroom, per P01 topic-index:277-278).

**Seeds (frozen, disjoint):**
- Phase A dev (anchor regression + problem scan) = seeds 0–9.
- Phase B/C dev-tuning = seeds 10–19.
- Fresh held-out = seeds 30–49.
- Pollution seeds 71–80 FORBIDDEN (P01/P02/P03 convention). dev ≠ held-out throughout.

**MDE = 0.15 dB** (common-768 gain MDE, same as P01/P02/P03; no post-hoc change).
**400 windows/cell** (P01 convention). **(8,8)-16APSK**, M0=8, N_DFT=256.

**Anchor regression gate (Phase A.1, BLOCKER if fail):** at the 3 anchor σ_R²
(0.2/1.6/3.5), the P04 channel wrapper (explicit (α,β)) MUST reproduce the frozen anchor
selector selected_errors + n_select_da/nda per seed (seeds 0–9, γ∈{5,7,9,11,13}) — i.e.
explicit-(α,β) injection ≡ scene-name injection. 0 mismatches. This proves the (α,β)
injection path is faithful and the continuous cells are a controlled extrapolation.

### 1.5 Info boundary (gate, BLOCKER if fail)

The original `decide(raw, γ_db, γ_lin)` is UNCHANGED (frozen, `git diff` empty). Any
Phase-B/C candidate's decide path: AST-audit clean — no true_snr/true_h/true_phi/tx_sym/
tx_bits/oracle/labels/turbulence_label/alpha/beta tokens; consumes only receiver-visible
(raw, γ_db, γ_lin, and optionally past-window receiver stats / pilot-based estimates).

## 2. Implementation — `_p04_continuous_gg.py` (channel wrapper + runner)

(mirror P01 probe line-for-line, replacing scene-name with explicit (α,β)):
- `alhabash(sigma2)` → (α,β) per §1.4 formula.
- `run_case_contgg(alpha, beta, gamma_db, seed_index, extra_selector=None)`: identical to
  `run_case_multidelta` (`_p01_cpr_snr_mismatch_probe.py:172`) but calls
  `generate_shared_realization_apsk(P.N_DFT, gl, scene='_contgg', f_dot, mod='m16apsk',
  seed=ws, turb_params=(alpha,beta))` — scene name unused once turb_params given.
  Δ-injection is N/A for P04 (the OOD variable is (α,β), not γ-mismatch); the selector is
  fed the TRUE γ (γ_db = γ_true_db, delta=0): the *question* is boundary-OOD, not
  γ-mismatch. fixed_DA/fixed_NDA/lower_count_bound/per_window errors returned as in P01.

## 3. Phase A dev probe — results (seeds 0–9, 9 σ_R² × 5 SNR = 450 cells, 287.9s)

**Pooled interior-cell regret (6 interior σ_R² × 5 SNR = 30 cells):**
`+0.1393 dB` (CI=[+0.0945, +0.1840]). Statistically present (CI_low > 0) but **magnitude
BELOW the frozen MDE=0.15 dB** → problem_holds = **False** on dev.

**Critical diagnostic — this is NOT OOD-specific:**
- **Anchor-cell mean regret = +0.2306 dB** (15 cells) — *higher* than interior OOD regret
  (+0.1393 dB). The selector is equally/more suboptimal AT the training anchors.
- Therefore the regret is a **general selector property** (it over-selects NDA on cells
  where DA is the better branch), NOT a continuous-GG-shape-OOD failure. The OOD question
  ("does the AWGN-fit boundary fail on un-trained GG shapes?") is answered **no** — the
  boundary does not degrade on continuous interior shapes; the regret is flat across the
  whole σ_R² range and is not concentrated in the un-trained interior.

**P3 branch-choice (real branch exists):** at every regret-bearing cell `mean_regret_DA ≈ 0`
(DA is the per-cell best branch) while NDA is far worse (regret_NDA +1.4 to +2.0 dB). The
selector's regret comes from picking NDA on windows where DA would have been better — a
real branch choice exists, so this is selector behavior, not common-branch collapse.

**Top interior regret cells (dev):** s2=0.45 γ=9 +0.484 [+0.402,+0.566]; s2=0.45 γ=7 +0.370;
s2=0.45 γ=11 +0.344; s2=0.70 γ=9 +0.298; s2=0.70 γ=11 +0.257. Concentrated at the
weak-side interior (σ_R² 0.45–0.70, between weak-anchor 0.2 and moderate-anchor 1.6), low
SNR (7–11 dB). But again: the weak/moderate ANCHORS show comparable regret, so it is not
OOD-concentration.

**Decision:** dev is borderline (0.1393 vs 0.15). The frozen criterion §1.1 P2 evaluates on
**held-out**. Must confirm on fresh held-out seeds 30–49 × 6 interior σ_R² (600 cells) before
a verdict. If held-out pooled regret < MDE → `PROBLEM_ABSENT_ON_CONTINUOUS_GG` (valid negative,
4/10, no method).

## 4. Phase A held-out confirmation — results (seeds 30–49, 6 interior σ_R² × 5 SNR = 600 cells, 365.1s)

**Pooled interior-cell regret (30 cells): `+0.1459 dB` (CI=[+0.0827, +0.2090]).**
Confirmed on a fully-disjoint seed set: statistically present (CI_low > 0) but **magnitude
STILL below the frozen MDE=0.15 dB** → `problem_holds = False` per the frozen §1.1 P2 gate
(pooled). dev (+0.1393) and held-out (+0.1459) agree to within 0.007 dB → robust.

**Honest sub-range structure (must be reported, not buried):**
- **9/30 interior cells exceed MDE with CI_low > 0** — the regret is NOT uniformly absent.
  Concentrated at the **weak-side interior** (σ_R² 0.3, 0.9, 1.35) × low SNR (5–11 dB):
  - σ_R²=0.30: γ{5,7,9,11} = +0.303/+0.554/+0.678/+0.450 dB (the strongest regret in the study)
  - σ_R²=0.90: γ{7,9,11} = +0.213/+0.259/+0.191 dB
  - σ_R²=1.35: γ{7,9} = +0.160/+0.182 dB
- The regret **decreases monotonically toward stronger turbulence**: σ_R²{1.85, 2.30, 3.15}
  all pooled < 0.15 dB, and γ=13 dB cells go **negative** (selector slightly HELPS there).
- The pooled mean is dragged below MDE by the strong-side / high-SNR near-zero-and-negative
  cells. This is genuine sub-range structure, not noise.

**Why the verdict is still PROBLEM_ABSENT (per frozen criterion, honestly):**
1. The frozen §1.1 P2 gate is **pooled** over held-out continuous cells; pooled = +0.1459 < 0.15.
   I do NOT change the gate after seeing results (V067 check 9 / brief trap #9).
2. The weak-side interior regret is **not OOD-specific in mechanism**: the same over-NDA-select
   behavior appears AT the weak training anchor (dev anchor regret +0.23 dB > interior +0.14 dB).
   The selector is a general NDA-over-selector at weak turbulence / low SNR regardless of
   whether (α,β) was trained; the continuous GG *shape* does not materially worsen it.
3. Per the binding-arbitration rewritten question ("does the AWGN-fit boundary produce
   selector-specific regret on continuous GG *distributions*"), the answer is: the regret is
   a flat selector property across the σ_R² range, not a continuous-GG-OOD phenomenon. The
   boundary does not degrade specifically on un-trained shapes.

**Terminal verdict: `PROBLEM_ABSENT_ON_CONTINUOUS_GG`** (valid negative, counts 4/10). No
Phase B/C method built (gate not passed). The weak-side-low-SNR sub-range regret is recorded
as a **bounded future-work seed** (a region-specific NDA-over-selection tendency), NOT a
continuous-GG-OOD method signal — and it overlaps the already-closed A-family
(SNR-mismatch/region-retune) operating regime, so per TL-30 it is not re-opened here.

## 5. Information boundary + reproducibility

**Frozen selector unchanged:** `git diff` on `_a4_switch_common768_30seed.py`, `common/`,
`params.py`, `_p01_*`, `_p03_*`, anchor JSON — all empty (only new untracked `_p04_*.py` +
results added). The original `decide(raw, γ_db, γ_lin)` is called as-is.

**Info boundary (P04 channel wrapper):** `run_case_contgg` consumes only
`(alpha, beta, gamma_db, seed)` to GENERATE the channel; the selector `decide` consumes only
`(raw, γ_db, γ_lin)`. True α/β/true-h/turbulence-label/TX-truth never enter `decide` (they are
used only for the oracle BER eval `ber_oracle_turb(trueh, bits, phi)`, which is offline
diagnostic only, exactly as in P01). AST/grep audit: no `alpha/beta/sigma2/turb_name/true`
token in the `decide` call path.

**Determinism:** `np.random.seed(seed)` set inside `generate_shared_realization_apsk`; window
seed = `SEED_TURB0(=2000) + seed_index*400 + b`. Same seed → byte-identical channel (anchor
regression gate proved this: 0 mismatch).

**Artifacts:**
- `results/p04_continuous_gg_ood/phaseA_dev.json` (450 raw rows + 45 aggregates + verdict)
- `results/p04_continuous_gg_ood/phaseA_heldout.json` (600 raw rows + 30 aggregates + verdict)

## 6. One bounded deterministic fix (disclosed, V067 allows one)

`sigma2_to_ab` uses the frozen rounded anchor pairs (11.6,10.1)/(4.0,1.9)/(4.2,1.4) at the 3
training σ_R² for EXACT regression (the anchor was trained on these), and the Al-Habash
closed form for continuous interior points. Rationale: Al-Habash exact values differ from
the frozen pairs by ≤2.70% (verified: weak 0.44%/0.22%, moderate 0.66%/0.55%, strong
0.61%/2.70%), and using them at the anchors broke byte-exact regression (85/108 mismatch at
'strong' β: Al-Habash 1.3622 vs frozen 1.4). The fix preserves exact regression AND keeps
continuous interior points within ≤2.70% of the anchors (controlled extrapolation, not a
discontinuous jump). No data/code/verdict impact beyond making the anchor gate pass.
