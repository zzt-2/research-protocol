# Worker Log: Pilot-Jones Step 4a big package

> 2026-07-23 | GW Step 4a (A0→A′→A/B→D) | T002 / S079 / D062 debt-waiver
> Provisional verdict: **KILL** (two structural gates) | Formal MVE: NOT RUN (gate KILL by design)

## Input baseline and authorization

- Worktree: `D:\code\study\research-protocol\.worktrees\research-direction-lab-longitudinal-test` (branch `codex/research-direction-lab-longitudinal-test`, HEAD `50528f2`, clean tree at start).
- Authorization: D062 (one-shot debt waiver) — H017 option (c). Step 3.5 stays `WAIVED_TO_STEP4A_WITH_BLOCKING_DEBT` (NOT PASS); the 4 D056 direct competitors stay `BLOCKED_NO_FULLTEXT`. One big package closes the scientific uncertainty "is Pilot-Jones worth continuing".
- Ceiling: positive result at most `CONDITIONAL_GO_WITH_BLOCKING_LITERATURE_DEBT`; never Step 5/Contract/Execute. Main opponent = conventional block/frame pilot Jones inversion (B2 family); oracle = upper-bound/Kill tool only (FR-25).
- Task-control: `validate_task_control.py` on T002 → **PASS** (epoch 4, action PILOT_JONES_STEP4A_PACKAGE).
- Inheritance check: D062 debt waiver correctly inherited — 4 papers remain BLOCKED throughout (not re-written as read). Step 3.5 remains WAIVED.

## Source closure and provenance debt

- Read-only source worktree `unified-batch-runner` — **not modified**. 7 expected SHAs all **MATCH** (pilot_assisted.py, pilot_integration_runner.py, batch1_fade_methods.py, _batch_metrics.py, 2 tests, historical JSON).
- **Known provenance break recorded**: historical JSON `pilot_6p_ema09_full24_N100k.json` claims `batch1_fade_methods.py` SHA `09b1fe2d...`, but the only on-disk file is `d8e280...`. The claimed source **cannot be exact-replayed** → the historical 15/15 is treated ONLY as a diagnostic prior, NOT a fresh MVE result, NOT Go evidence (T002 rule 5 + FR-26). It is a pilot-assisted-vs-blind(CMA) comparison, not a pilot-inversion-method comparison.
- New minimal closure built in this worktree (self-contained on current branch): `source-closure.yaml`, `metrics.py` (reimplemented fixed/PI BER), `pilot_jones_methods.py` (B0/B1/B2/P/O + standard Godard-z CMA core), `run_pilot_jones_mve.py` (paired-realization runner), `mve-contract.yaml`, `test_pilot_jones_step4a.py` (10 directed tests), `result.json`.
- Canonical generator re-traced to current branch: `_dual_pol_channel.generate_shared_realization_dp` (SHA `5cefac97...`), `_gg_time` (`d8e7929d...`), `params.SimulationConfig` (`0e87c533...`). Standard Godard-z CMA gradient `w += mu*(R2-|z|^2)*z*conj(r)` verified to include the z factor (vs the D017/D020 scalar-error variant).
- **Known simplification recorded**: channel 2×2 polarization mixing is a REAL rotation (`theta = sop_rate*arange(N)`, matrix `[[c,s],[-s,c]]`) → condition number ≡ 1 by construction. This is the SAME simplification as the source closure; it does not bias P-vs-B2 (all arms share it) but bounds the claim ceiling.

## Step 4a A0

- §0 four-criteria: all PASS at the form level (M-C-A complete; reusable output; recent baselines OE2021/LCOMM2026 full-text + 4 BLOCKED; quantifiable). Criterion 2/3 do NOT rely on "nobody did OSL".
- §1 six fatal checks: **TWO FATAL items fire** (details in feasibility_report.md Q2 section):
  1. No structural performance gap: B0→oracle gap fully absorbed by a single fixed EMA parameter (B1 EMA09 ≈ oracle; bit-equal on many seeds).
  2. FR-01 prior-coverage fatal: fixed EMA09 covers the main metric up to the oracle; B2a tikhonov is *worse* than B0; B2b condition_guard *identical* to B0 (never fires).
- A0 §2-5 supportive: receiver-visible info exists but has no signal to act on (cond ~ O(1)); prior silence of competitors is consistent with no OSL-specific structural failure; the structural reason competitors didn't do it is that a fixed smoother already reaches the ceiling.
- Semantic smoke (noiseless Jones recovery / singular-ill-conditioned / deep-fade / clean / causality / fixed-label-PI signature): all confirmed. Noiseless pilot-LS recovers theta (<3°); the channel never produces ill-conditioning (cond p50=1.10/p95=1.26/max=1.68 strong; p95=1.38 deep-turb probe).

## Step 4a A-prime / A / B

- A′ six competition dimensions: all either saturated by a simple baseline (per-block variance → B1; temporal lag → B1) or structurally absent (conditioning cond~1; deep-fade singularity h<0.1 frac=0). No method-worthy dimension left.
- A (structural advantage): no candidate can articulate a structural advantage because the channel does not exercise the dimensions that would distinguish a stabilization method.
- B (novelty-feasibility decoupling): novelty (OSL GG combination) exists but feasibility fails — "why better" cannot be answered because the hypothesized failure A is absent.

## Method candidates and selected method

- 3 mechanism-distinct candidates compared (NOT hyperparameter variants):
  1. **B1 fixed EMA09** — single fixed α=0.9 (current simple reference; NOT a new method).
  2. **B2a tikhonov / B2b condition_guard** — strongest cheap simple alternative (regularization / skip-on-cond).
  3. **P uncertainty-aware temporal tracker** — per-block α(cond, innovation) trust/memory schedule (proposed; structurally different from fixed EMA because α is a function of receiver-visible per-block state).
- Each candidate answered the 4 mandated questions (is it just EMA reparam? needs truth? explains deep-fade vs mismatch? strongest reviewer objection?).
- **Selected strongest proposed method: P**. Result: P does **not** beat B1 (hard-condition 10-seed: 0/10 P<B1 wins, 6/10 tie, 4/10 B1<P). α degenerates to ≈0.9 fixed because cond/innovation are flat on this channel. No candidate structurally beats fixed EMA / regularized LS → KILL mandated, no performance MVE (T002 §5.2).

## Frozen MVE contract

- `mve-contract.yaml` written and SHA frozen (`9acf655b...`) BEFORE the bounded probe: question/hypothesis/falsifier, method equations, information access, state lifecycle, metric signature, canonical generator, shared-realization rule, baseline ladder, parameter sources (FR-20, with adversarial deep-turb marked UNVERIFIED_RANGE), observed-seed exclusion (41-48), fresh validation (2000-2004) / test (3000-3009) seeds (disjoint), cells, primary/secondary metrics, pre-registered pass/fail thresholds, oracle/headroom gate, time budget, stop conditions, FR-11 architecture summary.
- Thresholds pre-registered (NOT post-hoc): Go = P beats B2 paired ≥8/10 + p<0.05; Kill = falsifier (a) cond~O(1), (b) B1→oracle headroom negligible, (c) P does not beat B2. Threshold sources: FR-21, gw-feasibility A0 §1, FR-25.

## Oracle / headroom gate

- B1 (strongest simple alternative) → true-theta oracle headroom: **negligible**.
  - Strong conditions: B1 == oracle bit-exact on most seeds.
  - Hard adversarial conditions (α=2.0,β=1.0,17dB, chosen to MAXIMIZE P headroom): B1 mean 5.3e-3 vs oracle 4.5e-3 (relative ~0.19, sub-order-of-magnitude; B1 equal-to-oracle on many seeds).
- Scoring oracle uses true theta only (no TX data, no future symbols); reported in fixed-label AND PI calibers (PI==fixed here, assignment_xy dominant).
- Pre-registered FR-21 kill (B1 within 2× of oracle) **fires**. Oracle is upper-bound/Kill tool only; NOT a Go opponent (FR-25). Headroom is not a TX-label/permutation calibration gap.

## MVE execution

- Formal 90-cell performance MVE: **NOT RUN** — by design (gate KILL), not a missing-result blocker.
- Two independent KILL gates fired at semantic-smoke + bounded-headroom stage:
  1. A0 §1 fatal + FR-01 prior-coverage fatal (no structural gap; hypothesized failure A absent; EMA09 covers main metric to oracle).
  2. FR-21 headroom KILL (B1→oracle headroom negligible).
- The failure is **structural** (cond~1 channel + B1==oracle), not statistical — full MVE would not change the verdict. Bounded 10-seed hard-condition probe (`result.json` `bounded_headroom_probe_rows`) gives the headroom number with sufficient precision.
- Executed under the frozen contract; paired-realization (one realization per cell+seed, shared by all arms); raw rows saved; each row carries config/source/contract SHA, realization fingerprint, information class, denominator.
- INDEPENDENT_AGENT_UNAVAILABLE note: integrity verifier and science critic below were executed in a separate general-purpose subagent context (P6 separation), not by this implementer.

## Integrity verification

Independent integrity verifier (separate subagent, P6 separation) checked (full report in `verifications.md` V036):
- source/contract/config SHAs: all match disk (7 source + contract + 6 closure files).
- raw→aggregate recompute: headroom stats recomputable from `bounded_headroom_probe_rows`.
- paired realization: one fingerprint per cell+seed, shared across arms (verified in tests).
- seeds disjoint: validation {2000-2004} ∩ test {3000-3009} ∩ observed {41-48} = ∅.
- mask/denominator: valid_data_samples = CMA-valid AND data-mask (pilots excluded); same for all arms.
- information access: deployable arms (B0/B1/B2/P) do not read sX/sY/h/theta; oracle reads true theta only (tagged). Test-enforced.
- protected history: STATUS.v1.md / project.v1.yaml / canonical-state.yaml / completion-events.jsonl byte-unchanged (4/4 SHA match baseline).
- tests + exact commands: `pytest test_pilot_jones_step4a.py` → 10 passed.
Conclusion: **PASS**.

## Science critic

Independent science critic (separate subagent, P6 separation) attacked (full report in V036):
- Scenario reskin? — No, but the *failure A* is structurally absent in the (real-rotation) channel, so the question is mooted at the channel-model level.
- EMA/regularization tuning? — P's α degenerates to ≈fixed; KILL is not a tuning artifact (0/10 wins on adversarial conditions chosen to favor P).
- Strongest simple comparator fair? — Yes; B2a/B2b given their best chance; B2a is worse than B0, B2b identical (honest, not weakened).
- Oracle sneaking Go? — No; oracle is upper-bound only, never a Go opponent.
- Fixed-label gain = assignment calibration? — No; PI==fixed (assignment_xy dominant); no permutation gap to exploit.
- GG/SOP params artificially inflated? — No; hard probe used adversarial deep-turb to MAXIMIZE P headroom and P still lost.
- MVE simplification weakening baseline? — No; the simplification (cond~1) DISfavors baselines B2 and FAVORS P, yet P still fails → KILL robust to the simplification.
- 4-paper debt impact on claim ceiling? — Caps any positive at CONDITIONAL_GO_WITH_DEBT; moot since gate fires on current channel.
- Clear algorithmic form? — P has a clear form but no signal to act on; no publishable method contribution.
Conclusion: **KILL is robust**; no avenue identified to rescue within scope.

## Provisional verdict

**KILL** (allowed enum; positive ceiling not reached). Pending master-control acceptance + user confirmation (D062 rule 6). Does NOT enter Step 5/Contract/Execute. Does NOT revive Scout/P03.

## Durable harvest

- Negative/boundary: structural-ill-conditioning argument — fixed EMA reaches oracle on unitary real-rotation channels, so no stabilization method is method-worthy *unless* the channel has genuine frequency-dependent PMD/PDL. Excludes the "pilot-LS stabilization" sub-family for this channel class.
- Reusable baseline ladder + runner/metrics + 10 directed tests — for the next pilot-Jones-style question.
- Reusable 5-min pre-MVE filter (cond-distribution + B1-vs-oracle headroom probe) for any "stabilize a matrix estimate" candidate (generalizes FR-21).
- Excluded method family: generic pilot→Jones→inverse + EMA/Tikhonov/condition-guard on unitary real-rotation channels.
- NO_DURABLE_HARVEST items: none.

## Changed files

- `projects/simulation/explore/pilot-jones-step4a/source-closure.yaml` (new)
- `projects/simulation/explore/pilot-jones-step4a/mve-contract.yaml` (new)
- `projects/simulation/explore/pilot-jones-step4a/synthesis.md` (new)
- `projects/simulation/explore/pilot-jones-step4a/metrics.py` (new)
- `projects/simulation/explore/pilot-jones-step4a/pilot_jones_methods.py` (new)
- `projects/simulation/explore/pilot-jones-step4a/run_pilot_jones_mve.py` (new)
- `projects/simulation/results/pilot-jones-step4a/result.json` (new; blocked manifest + gate evidence, not fabricated cells)
- `projects/simulation/tests/test_pilot_jones_step4a.py` (new; 10 directed tests)
- `projects/thesis-fso/worker-logs/step-002-pilot-jones-step4a-big-package.md` (new, this file)
- `projects/thesis-fso/feasibility_report.md` (appended Q2 section)
- `.sessions/2026-07-10-dual-pol-osl-groundwork/S079-pilot-jones-step4a-big-package.md` (new)
- Updated (state landing): `projects/thesis-fso/literature_notes.md`, `projects/thesis-fso/master-state.md`, `.sessions/2026-07-10-dual-pol-osl-groundwork/topic-index.md`, `.sessions/2026-07-10-dual-pol-osl-groundwork/verifications.md` (V036), `projects-overview.md`, Direction Lab 5 current views (formal routing/result only).

## Protected paths

Byte-unchanged (verified by SHA256 before/after): `projects/thesis-fso/direction-lab/STATUS.v1.md`, `project.v1.yaml`, `canonical-state.yaml`, `state/completion-events.jsonl`. B001–B003 / P03 Atlas untouched. `.agents/skills/` + controller untouched. Source worktree `unified-batch-runner` untouched (read-only, not modified/committed/cleaned).

## Commands and results

```text
# task control
python C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py \
  .sessions/2026-07-23-research-direction-lab-longitudinal-test/T002-pilot-jones-step4a-big-package.md
# -> PASS

# SHA verification (source worktree, read-only): 7/7 MATCH (incl. provenance break recorded)

# directed tests
python -m pytest projects/simulation/tests/test_pilot_jones_step4a.py -q
# -> 10 passed in 1.12s

# YAML/JSON parse: source-closure.yaml OK, mve-contract.yaml OK, result.json OK
# git diff --check: PASS (no whitespace errors)

# gate evidence (frozen smoke + bounded 10-seed headroom probe) in
# projects/simulation/results/pilot-jones-step4a/result.json
# P_beats_B1: 0/10 | B1_beats_P: 4/10 | tie: 6/10
# B1 mean 5.3e-3 vs oracle 4.5e-3 (rel headroom 0.19, sub-order-of-magnitude)
# cond p50/p95/max across probes: 1.19 / 1.38 / 3.99 (structurally well-conditioned)
# contract_sha256: 9acf655b18cdebb54b5a25175a381160ec9c0076c9e4dc8cb28dcf66ede72576
```

## Anomaly

- Historical `pilot_6p_ema09_full24` provenance break (batch1_fade_methods.py SHA mismatch) recorded and not replayed; the historical 15/15 is pilot-vs-blind, not pilot-inversion-vs-method, so it never supported a B2-beating claim.
- No other anomaly. The gate KILL is structural (real-rotation channel cond~1 + fixed EMA09 reaches oracle), not an infrastructure or statistical anomaly.
