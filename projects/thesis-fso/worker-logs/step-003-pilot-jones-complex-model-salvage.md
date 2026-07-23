# Worker Log: Pilot-Jones complex-model salvage

> 2026-07-23 | GW Step 4a (model-sufficiency salvage) | T003 / D063 / epoch 5
> branch: codex/research-direction-lab-longitudinal-test | HEAD start: 68c1fd8

## Input baseline and D063 authorization

- Worktree: `D:\code\study\research-protocol\.worktrees\research-direction-lab-longitudinal-test`
- Branch: `codex/research-direction-lab-longitudinal-test`; start HEAD `68c1fd8`
  ("authorize complex Jones salvage package"); T002 execution commit
  `0b642e9317d4494c481ecf4f1e8ceb07c866c04c`.
- Authorization: formal D063 (receive T002 local Kill `UNITARY_REAL_ROTATION_MCA_KILLED`,
  do NOT receive a family Kill; authorize a bounded model-sufficiency + method-
  salvage package stopping at a Step 4a provisional verdict).
- Read-before-act: T brief, master-state §2 + method-layer reopen track,
  D055/D056/D061/D062/D063, S079, V036, V037, T002 closures (source-closure /
  mve-contract / synthesis / pilot_jones_methods / run_pilot_jones_mve / result /
  directed tests), literature_notes Pilot-Jones + PMD/PDL/Jones entries,
  glossary / groundwork / gw-feasibility, thesis-lessons (TL-20/22/23/26/27/30-33),
  code-quality + sim-template, sim-preflight SKILL + rules/mve-validation +
  rules/adaptation-scan.

## T002 amendment

- T002 code/raw integrity trusted; local verdict inherited unchanged.
- **Independent raw recompute**: P/B1 win-tie-loss = **0/6/4** (contract's
  `0/7/3` is a stale-count document defect, recorded not overwritten).
- B1 mean `0.005308261178836862`, P mean `0.005335549069145674`, oracle mean
  `0.0044654026343545344`; `B1/O = 1.1887...` — a BER **ratio**, NOT 0.19 dB and
  NOT 0.5 dB. T002's second FR-21 gate is therefore a diagnostic only.
- V037 claim-scope correction of V036 received: numeric/code integrity PASS, full
  integrity claim PARTIAL. `PILOT_JONES_FAMILY_KILLED` NOT supported.

## Physical model evidence

- `model-evidence.yaml` answers Q1–Q7 with file:line / DOI / section sources.
- Verified magnitudes (sub-agent, sources cited): DGD ≤6 ps (Valjus 2025
  sat.1553 ref[76]) = 1.5% of T_S=400 ps → memoryless at 2.5 GBaud; component
  PDL <1 dB → cond<1.12; RSOP ≤600 krad/s (LEO) → block-constant Jones.
- Origin: PMD/PDL are component/fiber impairment, NOT free-space atmospheric.
- Physics gate: verified range is below the memory/conditioning thresholds, but
  the task-matched-baseline-fully-covered condition does not hold (4 competitors
  BLOCKED) → build the ladder and let the empirical headroom decide.

## Parameter provenance

All from `params.py` / sat.1553 / Gu 2022, tagged VERIFIED / APPROXIMATE /
UNVERIFIED_STRESS_ONLY in `model-evidence.yaml` parameter_table. Stress ranges
(PDL 3.5/6/9.5 dB → cond 1.5/2/3; DGD 40/80/160 ps → 10/20/40% T_S) are tagged
`UNVERIFIED_STRESS_ONLY` and cannot support a positive verdict.

## Model ladder and limiting-case tests

Built `complex_jones_channel.py` (M0 real-rotation control / M1 complex unitary /
M2 non-unitary PDL / M3 first-order PMD via 2×2 sinc-FIR / M4 combined) on top of
the canonical generator, impairment applied block-constantly preserving the
shared-noise contract. `run_salvage.py --mode theory` → **8/8 limiting-case
tests PASS** (M0 byte-compatible; M1 cond=1 unitary; M2 cond matches PDL-dB
exactly at 3.5/6/9.5 dB; M3 DGD=0 memoryless & DGD=80 ps has memory; M2 noiseless
recoverable).

## Metric and threshold adjudication

- Primary: `fixed_label_ber` (nocma derotation-quality variant isolates Jones-
  estimate quality from the CMA active component; CMA variant also reported).
- BER→Q² frozen: `Q=sqrt(2)·erfcinv(2·BER)`, `Q²_dB=20·log10(Q)`, QPSK only;
  BER=0 → `0.5/N_eval` upper bound; BER≥0.5 → None. BER ratio ≠ dB (T002 defect
  fixed). Verified by `test_ber_to_q2_known_values_and_zero_handling`.

## Task-matched baseline adjudication

- B3 = task-matched conventional: **B3_whitening** (polar-decomposition/
  whitening regularized inverse) for M2 PDL; **B3_tapped** (2×2 tapped LS,
  n_taps=3) for M3 PMD. Go opponent = B3; oracle = upper-bound/Kill only.
- Beating only single-tap B0/B1/B2 is NOT a method signal (T003 rule 4).

## Oracle / headroom gate

- Oracle fixed during execution: it must invert BOTH the component Jones J_b AND
  the SOP rotation R(theta) (a joint deployable estimator fits J_b@R(theta)
  together); inverting only J_b left R(theta) uncompensated and made the oracle
  spuriously worse than B3 — caught and fixed (TL-22 component trace), regression-
  guarded by `test_oracle_inverts_both_jones_and_sop_rotation`.
- Headroom reported as B3/O BER ratio AND Q² headroom (oracle − B3) dB.

## Method candidates

- P1 energy-weighted (inverse-variance) pilot-LS Jones estimate (mechanism-
  distinct from fixed EMA / post-hoc regularization); P2 α(cond,innov) tracker
  (T002's P); P3 whitening tracker. Selected strongest = P1.

## Conditional MVE

- NOT RUN. The gate fails at the probe stage: no verified-range method-worthy
  gap; impairment adds no headroom beyond the M0 deep-fade-only control even
  under stress; P1 does not beat B3. Per `salvage-contract.yaml` stop-conditions
  a formal MVE would not change a structural verdict.

## Integrity verification

Independent recompute (P6 separation):
- source SHA chain: generator/gg_time/params/channel/baselines/methods/runner all
  MATCH result.json `source_sha256`; contract SHA MATCH (dfc7f19e…).
- raw→aggregate recompute (M0_control_stress nocma) bit-exact.
- seeds {5000–5004} disjoint from T002 excluded {41-48, 2000-2004, 3000-3009}.
- theory 8/8 PASS; formal_mve_run=False.
- protected paths byte-unchanged (see below).
- 13/13 directed tests PASS (`pytest tests/test_pilot_jones_complex_salvage.py`).

## Science critic

Adversarial attacks on `PIVOT_MODEL_NOT_JUSTIFIED`:
1. **Fiber-problem swap?** PMD/PDL are component impairment, but retained GG fade
   + RSOP keep it an OSL problem; impairment magnitudes bounded by verified
   satellite-component values (not fiber-long-haul). Swap risk controlled →
   verdict survives.
2. **PDL/PMD physically correlated?** Modeled independently (worst case); a
   correlated model would only reduce the (already zero) added headroom → verdict
   survives.
3. **Single-tap strawman?** No — B3 is task-matched (whitening for PDL, tapped
   for PMD); single-tap B0/B1 are NOT the Go opponent → verdict survives.
4. **B3 under-tuned?** B3_whitening kappa and B3_tapped taps are validation-grade;
   the headroom is FLAT (identical to M0) so no tuning closes a gap that is
   structurally absent → verdict survives.
5. **P1 = RLS/Kalman/FDE alias?** P1 is inverse-variance-weighted LS (reliability-
  aware), distinct; and it loses to B3 anyway → moot.
6. **Oracle illegitimately strong?** Oracle uses true J + true theta only (no TX
   data, no future); for M3 the FDE oracle is the true ceiling → fair.
7. **Positive signal only under stress?** There is NO positive signal even under
   stress (headroom flat = M0) → verdict survives a fortiori.
8. **4-paper debt limits novelty?** Caps a future ceiling at
   CONDITIONAL_GO_WITH_DEBT; not reached here → moot.
Verdict `PIVOT_MODEL_NOT_JUSTIFIED` is robust.

## Provisional verdict

**PIVOT_MODEL_NOT_JUSTIFIED** (allowed enum). The complex-Jones/PMD/PDL model
upgrade does not reintroduce a method-worthy Pilot-Jones gap at 2.5 GBaud /
64–100-symbol blocks; B3 closes the headroom and the residual is the deep-fade+
noise floor. Does NOT enter Step 5/Contract/Execute; the Pilot-Jones family is
not closed on other grounds (remains `PILOT_JONES_FAMILY_UNRESOLVED` awaiting a
genuinely new axis, e.g. verified DGD ≫ T_S frequency-selective channel or
sub-symbol block-variant Jones).

## Durable harvest

- Negative/boundary material: complex-Jones/PMD/PDL does not rescue Pilot-Jones
  at this rate (extends T002's unitary-rotation negative).
- Reusable: model ladder M0–M3, B0/B1/B2/B3/P1/O ladder, paired runner, nocma
  metric, BER→Q² converter with zero-error bound, 13 directed tests.
- Reusable diagnostic: headroom-vs-impairment-strength trend test (generalizes
  FR-21 to a causal headroom filter).
- Correct BER→Q²/dB口径 (reusable).

## Changed files

Added (new):
- `projects/simulation/explore/pilot-jones-complex-salvage/model-evidence.yaml`
- `projects/simulation/explore/pilot-jones-complex-salvage/salvage-contract.yaml`
- `projects/simulation/explore/pilot-jones-complex-salvage/synthesis.md`
- `projects/simulation/explore/pilot-jones-complex-salvage/complex_jones_channel.py`
- `projects/simulation/explore/pilot-jones-complex-salvage/conventional_baselines.py`
- `projects/simulation/explore/pilot-jones-complex-salvage/salvage_methods.py`
- `projects/simulation/explore/pilot-jones-complex-salvage/run_salvage.py`
- `projects/simulation/explore/pilot-jones-complex-salvage/run_all.py`
- `projects/simulation/results/pilot-jones-complex-salvage/result.json` (+ theory.json,
  smoke.json, probe_verified.json, probe_stress.json)
- `projects/simulation/tests/test_pilot_jones_complex_salvage.py`
- `.sessions/2026-07-10-dual-pol-osl-groundwork/S080-pilot-jones-complex-model-salvage.md`
- `projects/thesis-fso/worker-logs/step-003-pilot-jones-complex-model-salvage.md`

Updated (per result, formal routing/result only):
- `projects/thesis-fso/feasibility_report.md` (Q2 salvage note)
- `projects/thesis-fso/literature_notes.md` (T003 amendment line)
- `projects/thesis-fso/master-state.md` (method-layer reopen track)
- `.sessions/2026-07-10-dual-pol-osl-groundwork/topic-index.md` (current position)
- `projects-overview.md` (thesis-fso current view)

## Protected paths

Byte-unchanged (SHA verified, baseline == final):
- `projects/thesis-fso/direction-lab/STATUS.v1.md`  701004b5…
- `projects/thesis-fso/direction-lab/project.v1.yaml`  73f71f3e…
- `projects/thesis-fso/direction-lab/canonical-state.yaml`  56abf96c…
- `projects/thesis-fso/direction-lab/state/completion-events.jsonl`  5565e78a…
- `projects/simulation/explore/pilot-jones-step4a/mve-contract.yaml`  3ff819ef…
- `projects/simulation/results/pilot-jones-step4a/result.json`  11f6a28d…
- shared canonical generator / common/ / params.py: NOT modified.
- protected history / Skill / controller: NOT modified.

## Commands and results

```
# theory limiting-case tests
python projects/simulation/explore/pilot-jones-complex-salvage/run_salvage.py \
  --mode theory --contract-sha <sha> --out .../theory.json
# -> 8/8 PASS

# full pipeline + decision
python projects/simulation/explore/pilot-jones-complex-salvage/run_all.py
# -> theory 8/8 PASS; smoke 8 rows; probe_verified 16 rows; probe_stress 30 rows
# -> verdict PIVOT_MODEL_NOT_JUSTIFIED

# directed tests
cd projects/simulation && python -m pytest tests/test_pilot_jones_complex_salvage.py -q
# -> 13 passed
```

## Anomaly

During execution the memoryless oracle was found spuriously WORSE than the
deployable B3 (TL-22): it inverted only the component Jones J_b, leaving the SOP
rotation R(theta) uncompensated, whereas a joint deployable LS estimator fits
J_b@R(theta) together. Caught by the headroom-vs-M0 sanity check, root-caused
(component-level trace), fixed (derotate_oracle now inverts both J_b and
R(-theta)), and regression-guarded by a directed test. M4 (combined PDL+PMD) was
excluded from the headroom table because its FDE oracle needs a joint channel
solver — a scope limitation, not a confound (M2/M3 cover the deciding axes).
