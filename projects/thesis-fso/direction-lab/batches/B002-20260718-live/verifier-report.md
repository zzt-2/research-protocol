# B002 independent verifier report

> verdict: PASS (artifact/contract/evidence integrity only)
> run: B002-15309cc700804776a45740786101a6ae

## Verified

- Controller and EvidenceGate: `ACCEPTED/TRUSTED`; manifest/result hashes match the receipt and ledger.
- Production mode: `test_only=false`, `sandbox_only=true`, `promotion_allowed=false`, `evidence_status=EXPLORATORY`.
- 30 cells (20 train, 10 test), one standard-CMA baseline call per cell, 46,860 block rows; seeds 11–20 and 41–45 are disjoint.
- Source snapshot/import closure: 31/31 files present and SHA-matching; registry and four component fingerprints match.
- Every row has finite fixed-label BER and permutation-invariant BER; 12 features are causal receiver/CMA traces only.
- Minimum information: 4 event cells and 6,279 positive train blocks.
- The unlabeled AE fit API consumes `x, cell_ids` only; threshold calibration consumes `scores, cell_ids, budget` only. Labels appear only in supervised training or post-hoc evaluation.

## Mechanism-level outcomes in the exact contract

| Candidate | Event AUROC | Event recall | Control FA | Lead blocks | Contract outcome |
|---|---:|---:|---:|---:|---|
| C24-SL-LINEAR | 0.9622865 | 1.00 | 0.20 | 336 | ADVANCE_SPECIFIC |
| C24-SL-MLP | 0.9577760 | 1.00 | 0.00 | 135 | ADVANCE_SPECIFIC |
| C24-SSL-AE-UNLABELED | 0.8213859 | 0.00 | 0.40 | 0 | RETIRE_SPECIFIC |

The AE result retires this exact mechanism/contract only. It is not a family-wide SSL, generative, or reconstruction-method kill. The two advances are not cross-domain generalization claims.

## Boundary

This report validates the sandbox artifact and preregistered decision rules. It does not release formal Groundwork Step 4a, paper material, or any cross-SNR/modulation/turbulence/length claim.
