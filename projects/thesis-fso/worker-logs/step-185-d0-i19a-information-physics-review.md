# Step 185 — D0 I19A information/physics independent review

> 2026-08-11 | senior independent reviewer | bounded shard | hard stop <15 min

## Required schema

```text
VERDICT=FAIL
P0=0
P1=2
P2=1
AXES_CLOSED=1,6,7
UNRESOLVED=none within the assigned shard; fixes and re-review are outside this read-only task
STOP_REASON=assigned files and axes 1/6/7 closed before the 15-minute hard stop
```

## FILES_READ

- Owner physical/information-flow sections in `projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml` and the I01/I03/I06/I09/I12/I19A sections of `d0-implementation-plan.md`.
- Production: `contract.py`, `waveform.py`, `channel.py`, `receiver.py`, `methods.py`.
- Tests: relevant CV/WC/RM sections in `test_d0_contract_views.py`, `test_d0_waveform_channel.py`, `test_d0_receiver_codec_methods.py`.
- Receipts: step-171, step-175, step-178, step-183, step-184.

## RECEIPT_SHA256S

| Receipt | SHA-256 |
|---|---|
| step-171 | `896834e8d269276b934af0dc53cdb3b2ad9736184a81b13514b51757cb04c9bc` |
| step-175 | `0db0010fd70d1561e4bd024b38be42b5b6228f0afd5948ef10b2140b73716057` |
| step-178 | `8e3d3826a3b78bf3805357de965893e1c93473b32f1f7a6b28e4ed8e51e93542` |
| step-183 | `5c10fa3c3f140e2627b0abaf5f48342e7c2f9703990621b41df176b91f5f01c8` |
| step-184 | `f274160082fd376f34ccf777aba6eaafc98a439a0630a58aa231504c7017412d` |

All five assigned production hashes and all three assigned test hashes match the final-byte identities recorded by step-184.

## Strengths

- `contract.py:194-401,480-538` recursively rejects truth-bearing aliases and derives per-polarization `RSS/31` from receiver observations; the WC negative family exercises nested aliases and forged noise receipts.
- `channel.py:135-174,228-299` implements the owner linewidth equation, theta0 rule, shared phase/fade, independent per-polarization AWGN and explicit per-real versus complex noise fields. `test_d0_waveform_channel.py:322-513` checks the actual materialized arrays and exact equations rather than receipt strings alone.
- `waveform.py:284-316` and `receiver.py:173-219` restrict rotations to the legal four states, preserve the sentinel polarization, include later pilots in the persistent suffix, split even-prefix state selection from odd-prefix residual estimation, and keep `C_post` out of the equalizer signature.
- Assigned focused guards remained GREEN: 5 selected CV/WC/RM behavior tests passed in `11.07s`; no I05 chain, science, or real benchmark was run.

## Issues

### P1 — The materialized ReceiverView bypasses the scalar receiver front end

- **Location:** `channel.py:379-397`, especially `381-382`; expected primitives are in `receiver.py:71-219`.
- **Why:** `build_views()` writes the raw channel samples directly into both `received_samples` and `equalized_samples`, and writes an all-zero `common_cpr_phase_trace`. It never calls prefix calibration, scalar visible-power equalization, common BPS, or global symmetry resolution. Therefore the only production factory joining the shared physical realization to `ReceiverView` labels an unprocessed stream as equalized and presents a fictitious zero CPR trace. Any downstream deployable path consuming these fields is not the owner-defined receiver-visible path, so a FAIR comparison or throughput run would measure the wrong interface.
- **Independent dynamic evidence:** on a real owner-loaded 14 dB/20 kHz materialization, `equalized_samples.tobytes()==received_samples.tobytes()` was `True`, `common_cpr_phase_trace==0` was `True`, while the observation-derived receiver noise estimates were positive (`[0.03548995940276505, 0.03650547380101225]`).
- **Test gap:** `test_d0_waveform_channel.py:322-405` verifies shapes, disjoint truth, and the physical equation but never asserts that the real `build_views()` output traversed `receiver.py`; RM01-RM06 test the primitives only in isolation.

### P1 — O1 accepts forged public exact-type objects without an authenticated seal

- **Location:** `methods.py:68-82,160-170,221-244`; inadequate negative at `test_d0_receiver_codec_methods.py:607-619`.
- **Why:** `FrozenDeployableOutputs` and `ControlledFixture` are publicly constructible dataclasses. `evaluate_o1_inverse()` authenticates neither provenance nor identity; it checks only exact type and the caller-controlled `is_frozen` boolean. A caller can construct `FrozenDeployableOutputs(b0=object(), b1=object())` and an arbitrary exact `ControlledFixture`, then invoke O1 without `freeze_deployable_outputs()` and without the authenticated deployment seal repaired in step-183. This violates the owner rule that O1 is evaluator-only after authentic deployable-output sealing.
- **Independent dynamic evidence:** the forged exact-type objects above were accepted and returned `O1Result(evaluator_only=True)` with fixture id `FORGED`. The current RM negative passes only `object()` as `frozen_outputs`; CV06/CV08 authenticate the separate `verify.DeploymentSeal` evaluator path and do not close this O1 entry point.

### P2 — Physical construction still relies on silent source defaults

- **Location:** owner `physical_realization.constructor_policy`; `channel.py:228-239,251-265,337-365`.
- **Why:** the owner says `all_fields_explicit_no_silent_source_defaults`, but `realize_supplied_waveform()` defaults `symbol_rate_baud`, `alpha`, `beta`, `f_g_hz`, and `block_symbols`; `build_views()` supplies only symbol rate and silently inherits the other four. Current default numbers match the owner, so this is not presently a numeric mismatch, but the physical identity is not call-site explicit and can drift independently of the loaded contract.
- **Test gap:** WC calls the defaulted constructor and checks resulting formulas; it does not reject omitted physical fields or prove they were resolved from the owner.

## Axis conclusions

- **Axis 1 — information/truth boundary:** FAIL due to the forgeable O1 boundary. The recursive ReceiverView truth denylist and the step-183 authenticated truth-correctness evaluator are strengths but do not authenticate `methods.evaluate_o1_inverse()`.
- **Axis 6 — physical/math correctness:** FAIL due to the receiver-visible integration bypass; isolated RSS/31, per-real/complex variance, linewidth, no-SOP, shared-realization, scalar-unit and legal-rotation formulas otherwise match the owner.
- **Axis 7 — tests measure real behavior:** FAIL. WC exercises real channel arrays and RM exercises real receiver primitives, but no assigned test connects the two; the O1 negative also tests a wrong type rather than an exact-type forgery.

## Protection checks

- Pre-write staging count: `0`; no `common/` status entry; the four `p05_run*.log` files remained the same untracked protected files and were neither modified nor staged.
- This reviewer modified no production, test, session, index, owner, common, or protected P05 file. The only write is this log.
- D0 science remains `NOT_RUN`; method signal remains `NONE`; I20 and FAIR comparison remain unauthorized.

