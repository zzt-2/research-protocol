# Task 1A bounded repair report

## Independent-review findings addressed

1. `ReceiverFrame.cell_id` leaked semantic cell identity into both the deployable DTO and receiver hash. The field and hash input were removed. Receiver DTOs now contain no string field/value carrying weak/moderate/strong or H0/H1/H2 labels; cell identity remains outside the receiver object.
2. The original seeded random-QPSK template plus matched-template timing score was not a faithful structural proxy for the Wang FSTS/Park synchronization mechanism. It was replaced by an explicit 320-symbol, `BN=16`, `BL=20` single-polarization Park/FSTS proxy: eight deterministic QPSK blocks followed by their conjugate, within-block and block-order reversed counterparts. Timing now uses the normalized correlation between conjugate-symmetric halves, not a known-template match.
3. `TruthRecord.branch_snr_db` ambiguously represented a nominal offset while Gamma-Gamma gain changed instantaneous received SNR. It is now split into `nominal_snr_offset_db` and evaluator-only `instantaneous_snr_db = nominal + 10log10(|gain|^2)`.

Existing Task 1B branch estimation, corrected MRC, fixed arms, oracle isolation, AST boundary audit, and metamorphic tests were retained.

## RED evidence

Before the repair:

```text
python -m pytest test_smoke.py -q
```

Result: `9 failed, 8 passed in 0.32s`. Failures explicitly covered the leaked `cell_id`, missing renamed/instantaneous SNR fields, random non-symmetric FSTS, matched-template sync signature, obsolete synthetic DTO construction, and stale truth metamorphism fields.

## GREEN evidence

After the bounded repair:

```text
python -m pytest . -q
```

Result: `17 passed in 0.18s`; no warnings or NaNs.

## Limitations

- The training sequence is an explicitly labeled single-polarization Park/FSTS proxy that preserves the published `BN/BL` and conjugate-symmetry mechanism; it is not an exact reconstruction of Wang's dual-polarization sequence.
- Gamma-Gamma triples and the K=4 heterogeneity replication remain `UNVERIFIED_RANGE` MVE settings.
- Park timing recovery is tested over the frozen 0..7 symbol window. Wider timing uncertainty and oversampled timing are outside this defect-only smoke.
