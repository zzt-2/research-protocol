<!--
BLIND PROMPT (verbatim, round 1):
You are a fresh research assistant. Use the Research Direction Lab Skill as your only process guide.

Working directory: D:\code\study\research-protocol\.worktrees\research-direction-lab-system

Read these two files and nothing else about the project's history:
1. The Skill: .agents/skills/research-direction-lab/SKILL.md (you may follow its reference routing one level deep if and only if a current decision requires it; do not read all references)
2. The case facts and artifacts listed below

You may also read the artifact file(s) the case points to, read-only. Do NOT run any test, script, or experiment. Do NOT modify any file.

CASE FACTS (verbatim):
- The project current-CMA update used the scalar error without the output factor z.
- The legal standard-CMA diagnostic included the Godard output factor z.
- Standard-CMA reduced PI-BER from about 0.033 and 0.032 to about 4.4e-5 and 4.7e-5 in two inspected high-gap seeds.
- The ML and CMA implementations also had different cross-branch initializations.
- The existing current-CMA comparison could not support a claim against legal standard-CMA at this point.

DECISION POINT: PROMPT-013 mechanism report after the current-CMA discrepancy was isolated and before the legal rerun.

ARTIFACT (read-only, for integrity context only — sha256 is provided so you can verify you read the right file; it is not the answer):
- path: projects/simulation/explore/cma-fade-divergence/PROMPT_013_REPORT.md
- sha256: 36d9dbca54ae3355101abcb72773f6a5f7742b08392721ee6ae3882ac9316781

PRODUCE a single markdown response with EXACTLY these seven sections ...
-->

## 1. Recovered facts
- PROMPT-013 ran on a frozen slice (N=5M, SOP=4e-7, f_G=30 Hz, strong, 20 dB) with Q1 (difference truth) and Q2 (mechanism).
- Q1 PASS: across 30 shared seeds (1000–1029) ML had lower excess PI-BER than project current-CMA in 30/30, two-sided exact Wilcoxon W=0, p=1.8626e-9; holdout 20 seeds also 20/20, p=1.9073e-6.
- H_a (objective misalignment) falsified: NMSE/leakage ratios (1.984/0.999) fail the preregistered ≥3×/≤1.5× condition.
- H_b (online update breaks mapping) strictly unknown: 10/12 oracle Spearman undefined; freeze main effect 0/3 for both current and standard CMA.
- H_c (expressive capacity) excluded: both are 4×11-tap complex FIR, 88 real DOF.
- Standard CMA with the Godard output factor z cut PI-BER from ~0.033/~0.032 to ~4.4e-5/~4.7e-5 in two high-gap seeds.
- Confound: ML `wxy/wyx` centers actually init to 1 (comment says 0) while CMA cross-branches init to 0.
- Conclusion in report: evidence supports only "ML > project scalar-error CMA", not a mechanism claim or a win against legal standard CMA.

## 2. Recovered authorization, anchor, and current mode
- Authorized scope: PROMPT-013 mechanism report (Q1 + Q2) on the frozen slice; independent verification passed (60 tests, py_compile clean).
- Anchor/baseline: frozen slice N=5M, SOP=4e-7, f_G=30 Hz, strong, 20 dB; current scalar-error CMA as the (now-invalidated) comparator.
- Current mode: post-diagnostic Synthesize/Harvest. Report's own recommendation is to hold at GW Step 4a and not enter Contract until a legal baseline is unified; the 30/30 result is diagnostic, not promotable.

## 3. Claim ceiling
DIAGNOSTIC — the 30/30 ML>current-CMA advantage is statistically real but was measured against an invalid comparator (missing output factor z plus a cross-branch initialization confound), so it cannot be claimed as a mechanism contribution or as a win against legal standard CMA.

## 4. Harvest items
- METHOD_SIGNAL: ML beats scalar-error current-CMA 30/30 with Wilcoxon p=1.8626e-9 (holdout 20/20, p=1.9073e-6); evidence pointer: projects/simulation/explore/cma-fade-divergence/PROMPT_013_REPORT.md
- LOCAL_NEGATIVE: all three preregistered mechanisms unsupported (H_a falsified, H_b unknown, H_c excluded); evidence pointer: projects/simulation/explore/cma-fade-divergence/PROMPT_013_REPORT.md
- FAILURE_MECHANISM: adding output factor z to standard CMA collapses PI-BER to ~4.4e-5/4.7e-5, which is what invalidates current-CMA as a comparator; evidence pointer: projects/simulation/explore/cma-fade-divergence/PROMPT_013_REPORT.md
- EVALUATION_INSIGHT: ML vs CMA cross-branch initialization mismatch (1 vs 0) is an unremoved training-path confound that must be unified before any legal rerun; evidence pointer: projects/simulation/explore/cma-fade-divergence/PROMPT_013_REPORT.md
- WRITING_MATERIAL: explicit "do not write" guidance — neither "fixed weights beat online CMA" nor "ML cleans the swap" is a permissible mechanism claim under current evidence; evidence pointer: projects/simulation/explore/cma-fade-divergence/PROMPT_013_REPORT.md

## 5. Next automatic action
Prepare a single unified-baseline rerun contract for the same 30 seeds on the same frozen slice: correct the current-CMA implementation to include the Godard output factor z, set ML and CMA cross-branch initializations identically, then compare current-CMA vs standard-CMA vs ML; record the contract and only then run.

## 6. Whether the user must be asked now
No — legal alternatives exist. The unified-baseline rerun is a bounded, reasonable adaptation that the report itself recommends and it is the informative test of whether ML's advantage survives a legal comparator; escalation as a thesis-route decision is warranted only if that rerun collapses the advantage.

## 7. Files read or consulted
.agents/skills/research-direction-lab/SKILL.md
projects/simulation/explore/cma-fade-divergence/PROMPT_013_REPORT.md
