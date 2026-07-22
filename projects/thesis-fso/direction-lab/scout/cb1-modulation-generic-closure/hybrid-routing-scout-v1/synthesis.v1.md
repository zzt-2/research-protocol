# Hybrid-Routing Scout v1 — Synthesis (Macro A → Verdict C)

> Schema: `direction-lab.cb1.hybrid-routing.v1`
> Campaign: `science-scout-2026-07-20.dual-pol-osl`
> Date: 2026-07-22
> Verdict: **COMPLEMENTARITY_INVALID** (for this specific hybrid contract; the algorithm-selection family stays open)

## 0. TL;DR

The hybrid-routing hypothesis ("legal FIR blind equalizers have complementary
failure modes; a receiver-visible router can exploit this") was tested with
**legal capability-aligned experts** (MMA Yang-Werner-Dumont, standalone cold-
start DD-LMS) — both sharing the 11-tap 2×2 butterfly FIR structure of the CMA
anchor — on **fresh disjoint test seeds [121-130]** (NOT the contaminated 71-80).

**Oracle complementarity headroom = 0.0037 macro PI-SER — 8× below the
preregistered 0.03 practical threshold.** MMA and DD-LMS fail in the *same*
realizations CMA fails (correlated failure modes), so there is no complementary
structure to route. The prior "26/37 complementarity" was an artifact of the
illegal C16 spatial-2×2 expert (task-mismatch) + contaminated seeds 71-80 +
post-hoc PI-SER oracle.

Per the frozen contract, headroom below threshold → **Verdict C**, and router
training is NOT initiated.

## 1. Setup (frozen in batch-contract.v1.yaml BEFORE reading results)

- Anchor: Godard CMA with z-factor, μ=0.03 (B01-R fair fixed-μ), 11-tap 2×2 butterfly FIR, block_size=64.
- Fallback 1 (legal): MMA (Yang-Werner-Dumont JSAC 2002), R_R²=R_I²=0.82, same 11-tap butterfly. μ tuned on validation seeds [101-105] → μ=0.003.
- Fallback 2 (legal): standalone cold-start DD-LMS (Sato 1975), same 11-tap butterfly. μ tuned → μ=0.1. (Cold-start DD-LMS did NOT diverge on test; μ=0.1 small enough.)
- Oracle: TX-truth 2×2 LS unmix (Kill bound ONLY, FR-21/FR-25).
- Validation seeds [101-105] for μ-tuning; Test seeds [121-130] (fresh, disjoint from all 6+ prior batches).
- 11 representative cells (5 SNR × turbulence/SOP × short/long).
- Identity tests: DD-LMS 5/5 PASS (no-op, complex-convention, causal-prefix, decision-feedback-causal, hard-decision centers). MMA verified per-axis modulus + 0.82 constants.
- Practical threshold: oracle headroom ≥ 0.03 (6× MDE=0.005) to justify a router.

## 2. Results (11 cells × 10 test seeds = 110 realizations)

| Macro PI-SER | CMA | MMA | DD-LMS | Oracle |
|---|---|---|---|---|
| value | **0.3972** | 0.5031 | 0.4319 | 0.2196 |

Oracle selectors (Kill/headroom bounds):

| Selector | macro | headroom over CMA | meets ≥0.03? |
|---|---|---|---|
| min(CMA, MMA) | 0.3963 | **0.0009** | NO |
| min(CMA, DD-LMS) | 0.3937 | **0.0035** | NO |
| min(CMA, MMA, DD-LMS) | 0.3935 | **0.0037** | NO |

Complementarity vs CMA (threshold MDE=0.005):
- MMA: better 5.5% / worse 58% / tie 36%
- DD-LMS: better 21% / worse 35% / tie 44%
- Collapse subset (CMA>0.3, n=61): MMA better 5/61, DD-LMS better 5/61. The fallbacks fail in the SAME collapse realizations as CMA.

Divergence: CMA 0/110, MMA 7/110 (long cells), DD-LMS 0/110.
Only 2/110 realizations show ANY expert beating CMA by >0.03.

## 3. Verdict: COMPLEMENTARITY_INVALID

The legal-expert oracle headroom (0.0037) is 8× below the practical threshold.
The diagnostic complementarity from C16 (26/37 HOS-better-in-collapse, oracle
selector 0.1928) does NOT survive legal experts + fresh seeds. **Mechanism: legal
FIR blind equalizers (Godard / MMA / DD-LMS) are all gradient descents on near-
common modulus/decision objectives, so they share correlated failure modes —
they collapse in the same realizations. There is no complementary failure
structure to route among these specific experts.**

This closes THIS specific hybrid contract (collapse-aware routing among legal
FIR blind equalizers on this OSL channel). It does NOT close the algorithm-
selection family: routing among a *mechanically more diverse* expert pool
(e.g., model-based tracker + blind; or pilot-aided + blind) is not tested and
remains open.

## 4. Why Macro B (router comparison) was NOT run

Per the frozen contract: "If no practical oracle headroom among legal experts at
the preregistered threshold → verdict C, and stop training router." With headroom
0.0037 (12% of threshold), there is nothing for ANY router — threshold, low-
complexity, or ML — to convert. Training a router would be "ML for ML's sake"
(prompt: "如果简单阈值已经达到 ceiling...不要为了 ML 而 ML"). Macro B is only
informative if headroom exists; here the oracle itself (the upper bound) is below
threshold, so no router can beat always-CMA.

## 5. Independent verifier (C3) — adversarial attack result

Independent agent (separate context) attacked the result on 8 checks: 8/8 PASS
(1 PARTIAL on μ-tuning that did not affect the outcome). Headline number
independently recomputed exactly (0.003693). Critically, the verifier tested the
"convenient conclusion" skepticism: CMA was given its STRONGEST μ (0.03), so the
test is biased TOWARD verdict C (low headroom), yet headroom is still 8× below
threshold — the result is robust. Mechanism confirmed: correlated failure modes
(verifier check 7). Two non-verdict-changing caveats logged: DD-LMS weight-norm
bug (fixed, 0 divergence on test), tune_mu used only seed 101 (proper 5-seed
changes headroom by 0.00003).

## 6. Thesis contribution assessment (Macro C2)

- **Method contribution** (collapse-aware routing): NOT established — verdict C.
- **ML contribution**: N/A — no router trained (no headroom).
- **Mechanism contribution**: the correlated-failure-mode finding is real but its
  QUALITATIVE form is known (Johnson 1998 CMA review; Qian 2002 parallel blind eq;
  Kuncheva ensemble theory: no diversity ⟹ no oracle gain). NOT novel as a mechanism.
- **System contribution**: N/A.
- **Evaluation contribution**: a measured negative bound (oracle headroom ≈ 0.004
  on dual-pol OSL GG+SOP) is a small, channel-specific negative-bounds result —
  publishable only as a minor negative/boundary note, NOT a primary thesis spine.
- **Negative material**: the C16-task-mismatch artifact + contaminated-seeds lesson
  (D017) + the correlated-failure-mode measurement are harvestable as negative material.

**Bottom line**: this hybrid-routing contract does NOT yield a thesis-grade method.
It yields a slice-level negative bound + a methodology lesson (do not build a routing
claim on a task-mismatched expert + reused seeds). The campaign's prior valid
negatives (C11 no-benefit, MMA<CMA, blind-affine harmful, the LOCAL_SLICE Godard-
collapse) remain the harvestable material.

## 7. Unchanged / preserved

- All prior artifacts untouched. No protected history modified.
- No TX truth in MMA/DD-LMS at runtime (verifier-confirmed). Oracle = Kill bound only.
- No push, no merge. One consolidated commit at end of session.
