# B001 Batch Synthesis — high-SOP causal ML degradation detector

> 2026-07-17 | sandbox observation | independent verifier PASS

## Evidence status

- Controller `RUN` and `EXECUTION` receipts are valid; EvidenceGate accepted the artifact as `TRUSTED/ACCEPTED`.
- 30 paired cells and 46,860 block rows were produced; every cell has one shared standard-CMA/Godard-with-z baseline call.
- Source closure is 17/17 SHA-consistent for this run, but the source is an uncommitted unified-runner worktree snapshot. This is sandbox evidence, not a formal canonical implementation.
- `fixed_label_ber` and `permutation_invariant_ber` are both present. The historical single-statistic threshold is an executable negative control, not a candidate revival.

## Preregistered-domain observations

| mechanism | test rate 1e-5 | local rule outcome | interpretation |
|---|---:|---|---|
| C24-SL-LINEAR | AUROC 0.9622865429; AUPRC 0.8469339; recall 1.00; control FA 0.20; lead 336 blocks | ADVANCE_SPECIFIC | Multi-trace supervised score detects persistent fixed-label degradation in this domain; no fallback BER benefit was tested. |
| C24-SL-MLP | AUROC 0.9577760316; AUPRC 0.8440742; recall 1.00; control FA 0.00; lead 135 blocks | ADVANCE_SPECIFIC | Meets the local rule; this does not prove it is better than linear because recall/FA/lead trade differently. |
| C24-SSL-AE | AUROC 0.8292932545; AUPRC 0.3469134; recall 0.00; control FA 0.40; lead 0 | RETIRE_SPECIFIC | Retire this clean-reconstruction mechanism for this contract; do not generalize to all self-supervised or generative methods. |
| historical threshold comparator | AUROC 0.9412255; AUPRC 0.6238694; recall 0.00; control FA 1.00 | negative control only | High block AUROC did not translate to persistent event recall at the preregistered control budget. |

The control rate `4e-6` produced no persistent test event cells. The batch therefore supports local discrimination evidence at `1e-5`, not cross-rate robustness.

## Mechanism-level synthesis

1. The positive signal is in supervised multi-trace temporal features, not a single threshold. This changes the historical detector mechanism.
2. The batch tested detection, not recovery. No candidate changed standard-CMA, labels, pilots, or BER denominators; no BER-improvement claim is licensed.
3. The autoencoder used control-rate training and clean-row filtering based on train labels; the verifier found no test leakage, but this is not a label-free deployment proof.
4. The two supervised mechanisms advance only as independent candidates. This is not a family-wide ML Go, a formal Step 4a decision, or a paper-ready result.

## Validity boundary and next legal action

Valid only for the exact B001 contract: dual-pol OSL GG strong turbulence, QPSK, 20 dB, `N=100000`, block 64, `alpha=4.2`, `beta=1.4`, `f_g=30 Hz`, standard-CMA `mu=0.001`/11 taps, rates `4e-6` and `1e-5`, train seeds 11–20, test seeds 41–45.

The next legal action is a fresh, separately gated paired revalidation of the two supervised detector mechanisms with a causal safe-fallback policy, or a new candidate family. Direct competitor/Step 3.5 conflicts remain unresolved. No result here may be copied into thesis or paper materials automatically.
