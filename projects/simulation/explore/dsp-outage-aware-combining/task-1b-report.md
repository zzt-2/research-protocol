# Task 1B report: receiver-visible estimator and conventional arms

## Files changed

- `test_smoke.py`: added receiver-estimate schema, complex MRC formula, physical-frame, pilot-phase residual, no-valid, order/replay, truth-metamorphic, fixed-denominator BER, oracle separation, and positive/negative AST-boundary tests.
- `smoke_core.py`: added receiver-only branch estimation, known-training channel/SNR estimates, known-pilot phase interpolation and features, corrected equal-noise MRC, B0/B1/B2 arms, evaluator-only O1 subset enumeration, fixed-denominator pi/2-resolved BER, and executable AST audit.
- `task-1b-report.md`: this report.

## RED evidence

Initial Task 1B command, after adding the tests and before implementation:

```text
python -m pytest test_smoke.py -q
```

Collection failed as intended with `ImportError: cannot import name 'ArmOutput' from 'smoke_core'` (`1 error in 0.27s`). This was the expected missing-interface failure.

After the minimal implementation, the first full run produced `12 passed, 1 failed`; the failure was confined to the test's use of dataclass `!=` on NumPy arrays (`ValueError: truth value of an array is ambiguous`). The assertion was corrected to explicit array/tuple comparisons without changing production code.

The negative AST-audit test was then introduced and failed as intended with `TypeError: audit_deployable_information_boundary() takes 0 positional arguments but 1 was given`. The audit helper was minimally generalized to accept an optional function tuple and now proves it catches `TruthRecord` and `evaluate_subsets` references.

## GREEN evidence

Final commands:

```text
python -m pytest test_smoke.py -q
python -m py_compile smoke_core.py test_smoke.py
```

Result: `15 passed in 0.13s`; both commands exited 0 with no warnings or NaNs.

## Information-boundary result

- B0/B1/B2 accept only `BranchEstimate` tuples and fixed configuration scalars.
- Their call graph is limited to `_arm_output` and `combine_subset`; the AST gate reports no truth/evaluator symbols.
- A deliberately unsafe function referencing `TruthRecord` and `evaluate_subsets` is rejected by the same gate.
- Fixed `ReceiverFrame` plus fully changed truth metadata leaves estimates, selected subsets, no-valid flags, and complex outputs bit/float exact.
- O1 and pi/2 ambiguity resolution remain evaluator-only.

## Design deviations

The Task 1B brief requires each branch estimate to contain a receiver-visible phase-corrected raw payload. The implementation therefore performs known-pilot interpolation branch-locally before MRC. The broader design text also mentions a common pilot-only interpolation after combining; that additional post-combiner stage is not implemented in Task 1B and should be explicitly resolved by the controller before scientific execution rather than silently adding a second correction.

## Residual risks

- The estimator is intentionally minimal: normalized FSTS correlation, one LS training gain, and linear interpolation of unwrapped pilot phase. It is not a reproduction of Wang's complete synchronization/DSP chain.
- Estimated SNR uses FSTS residual power, which also contains unmodeled phase evolution; dev diagnostics must treat it as a receiver-visible proxy, not calibrated physical OSNR.
- O1 currently enumerates all non-empty subsets, which is bounded for frozen K=2/4 but must not be generalized to large K without a separate cost decision.
- Scientific invalid labels, raw rows, dev tuning, diagnostic fitting, freeze validation, and held-out execution remain out of Task 1B.
