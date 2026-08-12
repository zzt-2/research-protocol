# Task 1B brief: receiver-visible estimation, conventional arms, and information-boundary gates

Worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`

Time limit: 15 minutes. Start only after Task 1A is complete and green. Do not commit. Write files only with `apply_patch`.

Read first:

- `projects/simulation/explore/dsp-outage-aware-combining/design.md`
- `projects/simulation/explore/dsp-outage-aware-combining/implementation-plan.md`
- `projects/simulation/explore/dsp-outage-aware-combining/task-1a-report.md`
- current `smoke_core.py` and `test_smoke.py`

Scope: extend the isolated sandbox with receiver-visible branch estimation, corrected conventional MRC, fixed hard alternatives, scoring helpers, AST/runtime information gates. Do not implement a proposed soft validity method, dev/test runner, or run scientific samples.

Required TDD chronology:

1. Extend `test_smoke.py` first with focused tests; run and capture RED.
2. Implement minimally; run and capture GREEN.

Required tests and behavior:

- `BranchEstimate` contains receiver-visible values only: estimated offset, sync peak/margin, estimated complex channel, estimated SNR/power, pilot-LS residual, pilot coherence, CPE increment/coherence, and phase-corrected raw payload sequence. No truth fields.
- Estimate branch-local FS offset from the known FSTS and align the actual received samples. Estimate complex channel from known training. Estimate pilot phase from known periodic pilots and interpolate a receiver-visible phase correction. Features use only `ReceiverFrame` plus these estimates.
- Correct equal-noise MRC for a selected subset is
  `sum(conj(g_hat_k) * r_corrected_k) / (sum(abs(g_hat_k)**2) + eps)`.
  Explicitly test it against a hand-computed complex example and ensure no legacy truth-h/ZF-like formula is used.
- Deployable arm functions must accept only receiver-visible estimates/configuration, never `TruthRecord`:
  - B0: all-branch corrected conventional MRC.
  - B1: fixed dev-provided estimated-SNR threshold; no-valid output is explicit.
  - B2: fixed dev-provided top-L / GSC rule; no-valid output is explicit.
- Truth-aware O1 may live in a clearly separate evaluator function/module boundary and may enumerate non-empty subsets to minimize fixed-denominator payload BER. It is diagnostic/scoring only and cannot be called by B0/B1/B2.
- Fixed pre-FEC BER excludes known pilots, uses all payload bits as denominator, supports deterministic pi/2 ambiguity resolution only in the evaluator, and never drops failed trials.
- Runtime metamorphic gate: for a fixed `ReceiverFrame`, replacing/flipping all truth-only metadata must leave B0/B1/B2 receiver outputs, subset decisions, and receiver-visible features bit/float exact unchanged.
- Method-order/replay invariance: B0/B1/B2 outputs do not depend on invocation order.
- Static AST/call-graph audit should fail if deployable functions reference/import truth-only symbols or call O1/evaluator helpers. Provide an executable audit helper used by tests.
- Add at least one synthetic no-valid case and one physical generated-frame finite-output case.

Do not touch old b3, `common/`, `params.py`, governance, papers, unrelated dirty files, p05, or coded artifacts.

At completion write `projects/simulation/explore/dsp-outage-aware-combining/task-1b-report.md` with files changed, RED/GREEN evidence, any design deviations, and residual risks. Then send the parent a concise summary.
