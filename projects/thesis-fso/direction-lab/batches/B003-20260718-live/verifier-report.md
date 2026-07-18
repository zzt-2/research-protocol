# B003 independent post-run verifier report

> batch: B003 | run: B003-75778e4b4e4045388b5ee06e9b8e6649
> date: 2026-07-18 | scope: sandbox artifact/contract/evidence integrity
> verdict: PASS (exploratory only)

## Identity and evidence chain

- `manifest_hash`: `42d8061773f7ecb1d03912bd775dc18424a44a14b1943b97b664818634b6b5e6`
- `result_hash`: `c17ab94708307b82c0162b9e5d573971170869ec757dc6bb24ca62a83ac8e3cc`
- artifact: `artifacts/result.json`, SHA256 `a395ece10ed9eb084beae8d9bd2f49854d4220ba520f82bcf04d2ae0e43df6e0`, 107,859,566 bytes
- queue hash: `62cabb989e269af28697c5e4092cc9d984c92d15d7565d1bf0c461c3f0df5917`
- registry hash: `82fdb419de785568a3afe13666200aa17cde0abf56d9ae55848c70508bcddce9`
- runner fingerprint: `6f21dfe023ccb8e74876730bee8789353ef649ad2b976be63317420f298a9caf`
- EvidenceGate: `ACCEPTED/TRUSTED`; execution status: `COMPLETED_SANDBOX`

`evidence_ledger.jsonl` and `evidence-gate-audit.jsonl` each contain one lean record. The records contain receipt metadata, `manifest_hash`, `result_hash`, and `artifact_pointer`; neither contains full result rows. The root `result.json` is an envelope only; complete rows exist only under `artifacts/result.json`.

## Runtime and source closure

- 30 paired cells: 20 train and 10 test; exactly one standard-CMA baseline call per cell.
- Train seeds 11–20 and test seeds 41–45 do not overlap.
- Source import closure is 33/33: every listed path exists and its recorded SHA matches; closure includes the actual channel/CMA/metric modules, prompt013 standard-CMA entry, v3/v2/B001 runners, validator, controller, and governance snapshots.
- Baseline is `baseline.standard_cma.godard_z`; no current-CMA/no-z alias was used. All candidate components remain sandbox-only and promotion is disabled.

## Metric integrity and exact-domain observations

The exact B003 contract is dual-pol ground-to-satellite OSL GG turbulence, QPSK, SNR 20 dB, `f_g=30 Hz`, `alpha=4.2`, `beta=1.4`, 100,000 symbols, block size 64, CMA `mu=0.001`, 11 taps, control/event SOP rates `4e-6/1e-5`, `channel_block=100`, `r2=1`, `t_s=4e-10`, `method=gar`. No cross-SNR, cross-modulation, cross-length, or cross-`f_g` claim is valid.

- 46,860/46,860 rows have finite fixed-label BER, permutation-invariant BER, PI assignment, and 12 causal features.
- PI assignments: x→y 45,015; y→x 1,845. Positive labels: 7,561.
- The control-rate split has no event cells, so control-rate AUROC/AUPRC/recall are `None` by design, not missing-data contamination. ECE remains finite.
- Minimum-information checks identify 4 event cells and 6,279 positive train blocks.

## Mechanism-level outcomes

| Candidate | Exact-contract result | Observed diagnostics |
|---|---|---|
| C24-SL-LINEAR | `ADVANCE_SPECIFIC` | AUROC 0.9622865; AUPRC 0.8469339; event recall 1.0; lead 336; ECE 0.10461; control FA 0.20 |
| C24-SL-MLP | `ADVANCE_SPECIFIC` | AUROC 0.9577760; AUPRC 0.8440742; event recall 1.0; lead 135; ECE 0.10794; control FA 0.00 |
| C24-SSL-AE-UNLABELED | `RETIRE_SPECIFIC` | AUROC 0.8213859; AUPRC 0.3363064; event recall 0; lead 0; ECE 0.09325; control FA 0.40 |

These outcomes apply only to the named mechanisms under the exact B003 contract. The AE result does not kill SSL, unsupervised, reconstruction, or generative families; it retires this concrete mechanism/contract only. No number is promoted to formal research or paper material.

## Known state debt

`canonical-state.yaml:last_completed_batch` still points to B002. This was not edited after B003 because changing a source snapshot after execution would invalidate the recorded provenance of this run. The stale pointer is recorded for the next state-reconciliation step; it does not invalidate B003's artifact chain.
