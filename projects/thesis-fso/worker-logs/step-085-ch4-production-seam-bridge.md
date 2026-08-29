# Step 085: Ch4 fixed-A2 production-seam bridge

> 2026-08-30 | T085 / D064 / V039 / CP026 | bounded bridge execution and truthful provenance repair

## Scope and authority

1. Startup task-control validation returned `PASS` at base commit `5ec190ad8c8da14b5dba3b353bd23977b7429d8a`.
2. The frozen bridge used moderate Gamma-Gamma turbulence `(alpha,beta)=(4.0,1.9)`, SNR `14/18 dB`, `Np=2/4`, 64 shared latent IDs `20000..20063`, 4096 payload symbols per polarization, and the five frozen arms `B0/B2(tau=1)/B3_PSC(tau=1)/C4/O1`.
3. `O1` remained on a separate truth-only runner path; deployable `receiver_action` received only pilots, payload observations and the public arm parameter.
4. Work stopped at the frozen strict B2+B3 gate. No Task 5, formal production grid, thesis-number promotion, retuning, new candidate, Groundwork, chapter edit, commit or push was performed.

## TDD and review chronology

### Initial seam implementation

- Initial RED: `4 failed, 1 passed in 0.31s`; the runner and reducer files were intentionally absent.
- After minimal implementation, one synthetic fixture had an incorrect turbulence snapshot; correcting the fixture produced `56 passed in 2.64s` across the frozen seam/core/demapper/scaled-unitary suite.

### Checkpoint-integrity review repair

- Review identified two fail-open paths: checkpoint binding omitted runner identity, and completed checkpoint rows were reused without deterministic scientific-record validation.
- Repair RED: `5 failed, 5 deselected in 2.11s` (one missing runner-hash assertion plus four `DID NOT RAISE` mutations: namespace, latent hash, observation hash and arm metric).
- Minimal repair added `runner_sha256` to checkpoint binding and rebuilt/revalidated every reused record while excluding only diagnostic `runtime_ns`.
- Repair GREEN: `5 passed, 5 deselected in 2.18s`; then `56 passed in 2.64s` for the full frozen suite.

### Authority/reducer provenance review repair

- A later review found that raw reduction did not reject mutated `control_epoch/mission_checkpoint`, the reduction entry did not check actual HEAD and current frozen implementation hashes, and runner authority validation accepted non-frozen arm/bootstrap/code-hash structures.
- Repair RED: `11 failed, 10 deselected in 2.05s`.
- Minimal repair added exact raw control identity, HEAD/code-hash verification, exact arm dictionaries (including O1 access), exact bootstrap contract, and the exact required code-hash key set.
- Repair GREEN: `11 passed, 10 deselected in 1.47s`; then `67 passed in 2.66s` for the full frozen suite.

### Post-run generator identity repair

- The canonical raw finished at 14:18 under runner SHA `871ec566744cc678eb83c13aaf472609ecc0b77ce8f8e131ac2eaa063d30e91b`. At 14:20, the authority-only repair above changed the working runner SHA to `934bf414e63121c20a2c4b27b91eaf8b691bc531f122039130ca1081223bbc0d`.
- Root cause: the raw schema froze core/common/scaled-unitary hashes but did not carry its actual generator-runner hash. A later receipt therefore incorrectly used the current runner hash as a single undifferentiated binding.
- The exact post-run runner diff is confined to `verify_authority`: it replaces the two old partial checks (B2/B3 tau only; bootstrap seed/resample count only) with exact full-arm, full-bootstrap and exact code-key-set checks. It does not change latent construction, observation, receiver action, oracle action, scoring, record construction or raw serialization.
- Reversing that recorded patch in memory reconstructs SHA `871ec566744cc678eb83c13aaf472609ecc0b77ce8f8e131ac2eaa063d30e91b` exactly. Independent historical evidence is also retained in the pre-repair receipt and pytest checkpoint bindings.
- No repository snapshot of the old runner bytes is retained. Accordingly, the receipt now separates `actual_generator_runner_sha256` from `post_run_validation_runner_sha256`, marks raw/frozen-code binding `PASS`, and marks reproducible-generation binding `PARTIAL`. It does not claim a false full binding.
- Provenance repair RED: `1 failed, 21 deselected in 0.28s` because the receipt lacked these separated fields. GREEN after the minimal receipt contract change: `1 passed, 21 deselected in 0.14s`.

## Smoke and canonical execution

1. One-latent smoke used latent `19999` in the temporary directory `C:\Users\zzt\AppData\Local\Temp\t085-smoke-d3671cb57b9d4e9f9d1ca0c4215e69cb`; it returned `SMOKE_STRUCTURAL_PASS` and independent finite/shape/pairing checks passed. It is explicitly non-thesis evidence.
2. The canonical `4 x 64` raw was run exactly once and completed all latent IDs `20000..20063` in approximately 6.1 s. The raw SHA is `4ef32e16d4ce252634686e8e3dc6e0f94dbff4daad18ef12691b491c875e33ed`.
3. The first aggregate/receipt became invalid when the later reducer-provenance review tightened its validation. Those two derived files were moved recoverably to `C:\Users\zzt\AppData\Local\Temp\t085-pre-provenance-repair-994297fbeee04f398cc50b0197012ba2`.
4. The same immutable raw was reduced once more under the repaired reducer. The raw was not regenerated, mutated or replaced; its SHA remained identical before and after reduction.

## Exact canonical results

Each arm has `2,097,152` payload bits in each cell.

| Cell | B0 BER | B2 BER | B3_PSC BER | C4 BER | O1 BER |
|---|---:|---:|---:|---:|---:|
| 14 dB, Np=2 | 0.1056580544 | 0.0992503166 | 0.0917553902 | 0.0916032791 | 0.0633392334 |
| 14 dB, Np=4 | 0.0859007835 | 0.0819492340 | 0.0799245834 | 0.0785965919 | 0.0633392334 |
| 18 dB, Np=2 | 0.0471100807 | 0.0425825119 | 0.0391564369 | 0.0390577316 | 0.0248813629 |
| 18 dB, Np=4 | 0.0358486176 | 0.0339608192 | 0.0327191353 | 0.0322246552 | 0.0248813629 |

Paired C4-minus-comparator BER differences:

| Cell | vs B2 mean [95% CI], wins | vs B3_PSC mean [95% CI], wins |
|---|---|---|
| 14 dB, Np=2 | -0.00764704 [-0.01096228, -0.00448704], 45/64 | -0.00015211 [-0.00099999, +0.00070580], 28/64 |
| 14 dB, Np=4 | -0.00335264 [-0.00512222, -0.00174308], 45/64 | -0.00132799 [-0.00257543, -0.00004908], 36/64 |
| 18 dB, Np=2 | -0.00352478 [-0.00617222, -0.00125784], 36/64 | -0.00009871 [-0.00066235, +0.00043011], 19/64 |
| 18 dB, Np=4 | -0.00173616 [-0.00302129, -0.00063357], 30/64 | -0.00049448 [-0.00115443, +0.00022941], 21/64 |

Frozen pooled `Np=2` comparison (64 latent clusters, each resample carries both 14/18 dB rows):

- C4-B2: mean `-0.0055859089`, 95% CI `[-0.0083591759, -0.0030578673]`, wins `46/64`; strict B2 condition passes.
- C4-B3_PSC: mean `-0.0001254082`, 95% CI `[-0.0008006513, +0.0005495608]`, wins `29/64`; the upper confidence bound is positive, so the strict B3 condition fails.

The canonical terminal is therefore:

`CHEAP_COMPARATOR_NOT_CLEARED`

This is a scientific gate failure against B3_PSC, not a runtime failure, data-integrity failure, or permission to tune after seeing the result. B3's `channel_nmse` remains the inherited pre-calibration B2 estimate metric; the post-calibration action mechanism is represented by `inverse_residual` and must be labelled that way in any later analysis.

## Census and immutable bindings

- Census: 64 latent rows, 256 cell rows, 1280 arm rows.
- Same-SNR shared-payload hash pairs: `128/128`.
- Same-SNR O1 metric pairs: `128/128`.
- Manifest SHA: `d3ed6c7d887a7127850e310e2a6887eed5c99ec957f1a4b577282e1fbc518fde`.
- Raw SHA: `4ef32e16d4ce252634686e8e3dc6e0f94dbff4daad18ef12691b491c875e33ed`.
- Aggregate SHA before the final receipt-only provenance clarification: `8d2b21c59adc58c5e5a9ccdbb7f59986954ee1a86de1b43d3d6921cf24a2b46f`.
- Frozen production-core SHA: `c78d5303a38f3d6c3562ec5b4f0337cdaba6a2cb07330f31cdfbad3538827e60`.
- Frozen common demapper SHA: `bff9873d10e5b68f1262fddcc24788e23630792e82a23a308f8eb5c48f431a10`.
- Frozen scaled-unitary SHA: `868780505b55da7df979c75fe07f132bf52b8b8904c4ec88961fbbe38b052fd2`.

## Final fresh verification

| Check | Result |
|---|---|
| corrected-anchor + production-core + demapper + scaled-unitary tests | `68 passed in 2.86s` |
| `py_compile` for runner, reducer core/entry and seam test | PASS |
| fresh T085 task-control validator | PASS |
| receipt hashes, immutable raw SHA, terminal and `64/256/1280` census | PASS |
| canonical checkpoint absent | PASS |
| T071 confirmation, T083 demapper replay and T084/core historical paths unchanged from HEAD | PASS |
| exact T085 scoped whitelist | PASS |
| `git diff --check` | PASS |

## Files

1. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/corrected_anchor_manifest.json`
2. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/run_corrected_anchor.py`
3. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/corrected_anchor_reducer.py`
4. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/reduce_corrected_anchor.py`
5. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/tests/test_corrected_anchor.py`
6. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/corrected_anchor_raw.json`
7. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/corrected_anchor_aggregate.json`
8. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/corrected_anchor_receipt.json`
9. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/.gitattributes`
10. `projects/thesis-fso/worker-logs/step-085-ch4-production-seam-bridge.md`

## Implementer terminal

`CHEAP_COMPARATOR_NOT_CLEARED`

Task 5 remains frozen. This handoff reports the bounded T085 result and its provenance limitation; it does not promote the result into thesis evidence.
