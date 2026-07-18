# B003 exploratory batch synthesis

> batch: B003 | run: B003-75778e4b4e4045388b5ee06e9b8e6649
> status: sandbox exploratory; not formal research or paper material
> verifier: `verifier-report.md` (independent PASS)

## Scope and comparison

B003 compared three mechanism-distinct receiver-side degradation detectors on the same 30 paired cells and unchanged standard-CMA Godard-Z baseline. The comparison is legal only for the exact shared contract recorded in the queue and verifier report. Fixed-label BER and permutation-invariant BER were both retained as required signal metrics; detector metrics are secondary exploratory diagnostics.

## Synthesis

The two supervised temporal detectors met the preregistered mechanism-level advance rule in this exact domain. The unlabeled control-domain reconstruction detector did not meet the preregistered recall/false-alarm rule and is retired for this concrete implementation and contract. The three outcomes are not a family-wide ranking: they identify two mechanisms worth re-testing under new contracts and one specific mechanism to stop carrying forward unchanged.

The event/control split also limits interpretation. The control-rate partition contains no event cells, so its event-discrimination AUROC/AUPRC/recall are undefined rather than zero; control false alarm and calibration remain meaningful diagnostics. The observed values do not establish cross-SNR, cross-turbulence-rate, cross-modulation, or sequence-length generalization.

## Follow-up queue implications

- Continue with a new, separately gated causal safe-fallback or revalidation candidate; do not silently reuse B003 numbers as a new batch.
- Preserve the supervised pair as exact-domain retained candidates, with a fresh hypothesis and contract before any next run.
- Do not expand the AE retirement to SSL/UL/generative families.
- Keep Candidate Universe open: v2 Map is an archetype partition, not a completeness proof.

## Promotion boundary

No result from B003 is written to thesis, paper, formal Groundwork, or other official material. Any future claim requires a new contract, independent verification, and an explicit formal-stage gate.
