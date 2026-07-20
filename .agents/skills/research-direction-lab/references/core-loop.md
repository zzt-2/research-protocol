# Core loop

Use this reference to execute and close each phase without turning the loop into a fixed scheduler.

## Phase contracts

| Phase | Required inputs | Required output | Closure question |
|---|---|---|---|
| Recover | canonical status, adapter, state, portfolio, latest synthesis, harvest summary | trusted anchor, authorization, uncertainties, current mode, first legal action | Can the next action be justified from current facts without inheriting stale conclusions? |
| Map | anchor, failures, assets, historical counterexamples, supported and blocked axes | candidate cards with lineage, information access, output, mechanism, scope, dependencies, cost, and unknowns | Is the portfolio broad enough for an informative comparison while remaining explicitly open? |
| Plan | candidate cards and shared scientific questions | batch cards, baseline adjudication, and any shared preparation sprint | Does each comparison answer a causal question under a legal and claim-adequate shared baseline? |
| Prepare and run | batch card, project commands, integrity tools | manifest, artifacts, receipt, execution facts | Were identity, provenance, information, metric, history, and exit boundaries protected? |
| Synthesize | verified artifacts, diagnostics, comparator facts, prior evidence | bounded result, alternative explanations, scope assessment, next options | What is the smallest defensible conclusion, and what remains unresolved? |
| Harvest | synthesis and artifact pointers | one or more ledger entries with evidence and scope | What durable scientific or thesis value was learned even if no candidate won? |
| Rotate or deepen | synthesis, portfolio, harvest, costs, blockers | explicit next action and rationale, or justified strategic escalation | Is another legal action more informative than stopping or deepening? |

## Operating principles

- Re-enter Recover after context loss, changed authorization, stale evidence, or a material user correction.
- Re-enter Map when repeated runs add no mechanism information, the current portfolio over-concentrates on one idea, or a new failure exposes an unmapped family.
- Design batches around shared causal questions, not paper titles or model names.
- Treat a baseline anomaly as a candidate source, not a Go signal. Use `baseline-adjudication.md` before authorizing method development, and stop once the bounded claim has a defensible conventional comparator.
- Separate execution verification from scientific criticism. Treat both as inputs to synthesis, not replacement process owners.
- Let observed information value and cost shape batch size. Treat any numeric batch-size suggestion as a local heuristic unless the project explicitly authorizes it.
- Close every cycle with updated status, harvest, and a concrete next action.
