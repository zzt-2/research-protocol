<!--
BLIND PROMPT (verbatim, round 1):
You are a fresh research assistant. Use the Research Direction Lab Skill as your only process guide.

Read this file and nothing else about any project's history:
1. The Skill: .agents/skills/research-direction-lab/SKILL.md

Do NOT read any other file in this repository. The case below is self-contained.

CASE FACTS:
- The project's JIT register allocator baseline is linear-scan over a static linearized live interval list.
- The baseline is runnable end-to-end on the project's IR fuzzer and reports spilled_cycles and reg_pressure_peak as its two metrics.
- "Three candidate families have been mapped: graph-coloring over the interference graph, tree-scan over the dominator tree, and an ML-based cost model that predicts spill cost per live range."
- The graph-coloring candidate cannot run because the IR does not expose a stable interference-graph contract; the IR mutation pass renumbers virtual registers between optimizer phases.
- Tree-scan and the ML cost model can compile and execute against the current IR fuzzer without changes.
- A trial run of the ML cost model against a buggy spill-cost oracle (the oracle double-counted rematerializable ranges) showed a 12% spilled_cycles reduction.
- After the oracle bug was isolated, the project confirmed the legal oracle counts each live range once; the legal reduction against the corrected oracle is unknown.
- spilled_cycles and reg_pressure_peak are not interchangeable; reg_pressure_peak is a peak instantaneous measure and spilled_cycles is an execution-weighted total.
- No benchmark suite, queue, registry, completion event, formal promotion, or paper claim exists for any candidate.

DECISION POINT: Register allocator portfolio review after the linear-scan baseline locked in and before the next comparison.
-->

## 1. Recovered facts
- Linear-scan over a static linearized live-interval list is the locked baseline; it runs end-to-end on the IR fuzzer and reports `spilled_cycles` and `reg_pressure_peak`.
- Three candidate families are mapped: graph-coloring (interference graph), tree-scan (dominator tree), and an ML cost model (per-live-range spill cost).
- Graph-coloring is blocked: the IR mutation pass renumbers virtual registers between optimizer phases, so no stable interference-graph contract exists.
- Tree-scan and the ML cost model both compile and execute against the current IR fuzzer without changes.
- An ML cost model trial showed a 12% `spilled_cycles` reduction against a buggy spill-cost oracle that double-counted rematerializable ranges.
- A legal oracle that counts each live range once is now confirmed; the reduction against the corrected oracle is unknown.
- `spilled_cycles` (execution-weighted total) and `reg_pressure_peak` (peak instantaneous) are not interchangeable.
- No benchmark suite, queue, registry, completion event, formal promotion, or paper claim exists for any candidate.

## 2. Recovered authorization, anchor, and current mode
- Authorized: register-allocator portfolio review after the linear-scan baseline was locked and before the next comparison.
- Anchor/baseline: linear-scan over the static linearized live-interval list, evaluated on the IR fuzzer via `spilled_cycles` and `reg_pressure_peak`.
- Mode: existing-foundation entry; synthesizing the one completed trial and harvesting before re-planning the next batch. No deeper-evidence or promotion workflow is triggered.

## 3. Claim ceiling
DIAGNOSTIC — the only executed ML trial was measured against an invalid (double-counting) oracle, so per the integrity rule a positive result against a buggy comparator is diagnostic until a legal comparator confirms it.

## 4. Harvest items
- FAILURE_MECHANISM: graph-coloring is blocked because the IR mutation pass renumbers virtual registers between optimizer phases, destroying interference-graph stability; evidence pointer: case facts (interference-graph contract absent).
- EVALUATION_INSIGHT: the ML 12% `spilled_cycles` gain is tied to a buggy oracle and cannot be promoted; the legal reduction is unknown; evidence pointer: case facts (oracle double-counted rematerializable ranges).
- METHOD_SIGNAL: `spilled_cycles` and `reg_pressure_peak` measure different things (execution-weighted total vs. peak instantaneous) and must be reported separately; evidence pointer: case facts.
- REUSABLE_ASSET: corrected legal spill-cost oracle that counts each live range exactly once; evidence pointer: case facts (post-bug-isolation confirmation).
- INFRASTRUCTURE_GAP: no benchmark suite, queue, registry, completion event, or promotion path exists yet for any candidate; evidence pointer: case facts.

## 5. Next automatic action
Re-run the ML cost model on the existing IR fuzzer against the corrected legal oracle, recording both `spilled_cycles` and `reg_pressure_peak`, to establish the legal reduction; this is a bounded provenance repair that converts the diagnostic result into comparable evidence.

## 6. Whether the user must be asked now
No — legal alternatives exist. The automatic-continuation list covers "provenance needs one bounded repair" and "a positive result against an invalid comparator is diagnostic until a legal comparator confirms it"; no escalation trigger (goal change, thesis-route choice, larger investment, private facts, integrity condition with no safe alternative, or exhausted ready work) applies.

## 7. Files read or consulted
.agents/skills/research-direction-lab/SKILL.md
.agents/skills/research-direction-lab/references/evidence-and-claims.md
