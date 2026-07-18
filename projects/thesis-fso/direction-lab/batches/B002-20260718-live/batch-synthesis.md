# B002 batch synthesis

> status: COMPLETE_EXPLORATORY_ONLY
> verifier: verifier-report.md / V011

## Scope

B002 is a paired sandbox batch under the frozen dual-pol ground-to-satellite OSL contract. All candidates consumed the same 30 standard-CMA cells, seeds, causal feature rows, fixed-label/PI-BER metric contract, and resource budget. No test-only receipt or synthetic execution object is included in this synthesis.

## Findings

- The supervised linear and shallow nonlinear temporal detectors both satisfy the preregistered `ADVANCE_SPECIFIC` rule in the exact contract.
- The unlabeled control-domain reconstruction AE does not satisfy the advance rule and satisfies `RETIRE_SPECIFIC` because event recall is zero; its AUROC alone is not sufficient to advance it.
- These are mechanism-level observations at SNR 20 dB, QPSK, `f_g=30 Hz`, SOP rates `4e-6/1e-5`, length 100,000, and the stated train/test seeds. They do not establish cross-domain generalization or a method-family conclusion.

## Decision boundary

Retire `C24-SSL-AE-UNLABELED` for this exact mechanism/contract, retain the broader SSL/UL/reconstruction families as open candidates, and continue with other mechanism-distinct candidates. Do not revive the old label-filtered AE as an SSL claim. The two supervised candidates may proceed only to a separately scoped revalidation/fallback or next-batch design; this batch does not promote them to formal research material.

## Publication boundary

All numbers remain sandbox evidence. No automatic write to thesis, paper, abstract, or formal Groundwork materials is authorized.
