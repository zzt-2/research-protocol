# Step 084: Ch4 production core TDD

> 2026-08-30 | T084 / D063 / V038 / CP025 | fresh implementer record

## Scope and authority

1. Startup task-control validator returned `PASS` for T084 at CP025.
2. Implementation used the frozen Task 3 interfaces and invariants. Turbulence `(alpha,beta)` is resolved at runtime from `projects/simulation/params.py::SimulationConfig().turbulence`; the kernel does not duplicate the three parameter pairs or Rytov-variance values.
3. Only the three T084 create-whitelist files were touched. `scaled_unitary.py`, common modulation/demapper, params, historical artifacts, runners, governance and chapter files were not modified.
4. No BER cell, A2 bridge, smoke, B2 tuning, production grid or thesis-number generation was run.

## TDD evidence

- RED command: `python -m pytest projects/simulation/explore/ch4-scaled-unitary-pilot-ls/tests/test_production_core.py -q`
- RED result: `19 errors in 0.42s`; every error had the same intended cause, `FileNotFoundError: production_core.py`. There was no collection syntax error or unrelated regression.
- First focused GREEN after minimal implementation: `19 passed in 1.41s`.
- A post-GREEN fail-closed audit added one test requiring arms without a single public singular scale to return `None`, not a nonfinite sentinel. It produced the intended RED (`1 failed, 19 passed`) against B0, followed by the minimal repair.
- Pre-review focused suite after that repair: `29 passed in 1.37s` for `test_production_core.py`, `test_m16apsk_ml_demod.py`, and `test_scaled_unitary.py`.

## Independent-review correctness repair

The first independent review returned `PRODUCTION_CORE_CORRECTNESS_INVALID`, P0/P1/P2=`0/1/1`: generated streams and formulas passed its independent oracles, but `_validated_latent` accepted mutated provenance metadata.

1. Repair RED: 17 focused mutation cases all failed with `DID NOT RAISE`. They cover a replaced namespace component key; mutated entropy/bit-generator; mutated scenario/latent/component words in the complete spawn key; all five turbulence snapshot fields; and invalid or namespace-inconsistent latent IDs.
2. Root cause: the consumer validator checked only field presence, while hashes protected arrays rather than the provenance metadata. The generator was unchanged.
3. Minimal repair: `_validated_latent` now validates the uint32 latent identity, reconstructs the seven expected namespaces from `scenario+latent_id`, requires exact metadata/key equality, re-resolves the central turbulence authority, and requires an exact snapshot.
4. Repair GREEN: the 17 mutation cases passed; the complete frozen suite then returned `46 passed in 1.38s`.
5. No stream, formula, generated array, receiver arm or scientific parameter changed.

### B3_PSC metric semantics

`B3_PSC.channel_nmse` is deliberately the inherited, **pre-calibration B2 channel-estimate NMSE**, because B3 retains B2 `h_hat`. The post-calibration receiver action is `a W_B2`; its action-level mechanism metric is `inverse_residual`. If later figures or tables include B3 mechanism metrics, they must label this distinction explicitly and must not describe the inherited NMSE as the final calibrated equivalent-channel estimate.

## Closed correctness contracts

1. Balanced pilots support exactly `Np=2/4/8/16`, satisfy `Xp Xp^H=Np I`, and freeze the `Np=2` block plus repeated `Np=4` block rule.
2. Seven named PCG64/SeedSequence streams freeze the full namespace `(84,1,scenario_code,latent_id,component_code)` for payload bits, channel Q, Gamma-Gamma gain, standardized pilot noise, standardized payload noise, mismatch left and mismatch right. Tests independently reconstruct the payload-bit stream from the recorded entropy and spawn key and require exact latent replay.
3. A latent window is independent of SNR and Np. Observation tests prove analytic noise rescaling across SNR, a frozen pilot-noise prefix across Np, and invariant bits/Q/gain/payload-noise hashes.
4. Weak/moderate/strong resolve to `(11.6,10.1)/(4.0,1.9)/(4.2,1.4)` from the central authority. Tests derive the rounded-parameter Gamma-Gamma scintillation indices `0.193752/0.907895/1.122449`; the kernel stores the resolved snapshot and authority pointer.
5. The `tau=1` B2 and C4 identities explicitly share `V U^H`; the test proves only their public scales differ.
6. `B3_PSC` inherits the B2 tau, computes the frozen pilot-only nonnegative-real closed form, scales the B2 payload action, and fails closed for invalid denominator/numerator/output. The deployable receiver signature and source contain no hidden-channel, bit or payload-decision access.
7. The mismatch constructor accepts `left=gU`, `right=V`, implements the frozen normalized diagonal, preserves average Frobenius power and produces the monotone analytic singular-value ratio.
8. Unsupported scenes/Np/arms, invalid parameters, malformed/nonfinite matrices, inconsistent latent hashes and invalid offline truth inputs fail closed.

## Verification commands

| Command | Result |
|---|---|
| final fresh focused three-file suite after review repair | `46 passed in 1.42s` |
| `python -m py_compile` on production core and its test | PASS |
| T084 task-control validator | PASS |

## Files

1. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/production_core.py`
2. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/tests/test_production_core.py`
3. `projects/thesis-fso/worker-logs/step-084-ch4-production-core-tdd.md`

## Implementer terminal

`IMPLEMENTER_GREEN_AWAITING_INDEPENDENT_REVIEW`

This is a correctness-only handoff. It does not authorize or claim A2, smoke, tuning, production, a BER result, or the final `PRODUCTION_CORE_CORRECTNESS_PASS` terminal.
