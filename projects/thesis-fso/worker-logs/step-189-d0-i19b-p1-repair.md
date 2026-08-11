# Step 189 — D0 I19B P1 minimal repair

> 2026-08-11 | implementation/TDD | hard stop `~15m`

```text
STATUS=DONE_IMPLEMENTATION
P1_CLOSURE=2/2_FOCUSED_GREEN
P0=0
P1=0_IN_FOCUSED_REPAIR_SCOPE
P2=1_DEFERRED_NONBLOCKING_CODEC_CW_ID_COERCION
SCIENCE=NOT_RUN
BENCHMARK=NOT_RUN
```

## Code changes

- `schemas.py`: exposed the narrow owner-derived `hmm_chunk_authority_binding` projection for deterministic chunk/member/computation commitment recomputation.
- `freeze.py`: HMM selection/fit now requires the frozen owner plus opaque runtime aggregate contents; it revalidates the exact owner manifest/dev seed axis, canonical runtime content, chunk id, member manifest, computation manifest, content commitment, exact numerator/denominator, member count, and exact content coverage. The detached `member_seeds` fit argument was removed.
- `b2.py`: pilot posterior normalization and data-LLR bit partitions now detect non-finite all-impossible mass before subtraction and raise `B2MathError`; no `-inf - -inf`, NaN, or warning escapes.
- Tests: added numerator-with-hashes-retained, content root, wrong group/chunk, non-dev member root, computation root, pilot all-impossible, and data-LLR all-impossible regressions; migrated legal HMM fixtures to owner/runtime-authenticated evidence.

## RED evidence

- Initial focused command: `7 failed in 5.44s` (`6.372s` wall).
  - HMM 5 cases failed because `schemas.hmm_chunk_authority_binding` did not exist.
  - The two initial B2 warning wrappers were incompatible with this pytest version; after correcting only the wrappers, both real regressions failed with `DID NOT RAISE B2MathError` (`2 failed in 0.54s`).

## GREEN evidence

- First focused production run: security/B2 cases `7 passed`; one existing DF assertion failed only because the new fail-closed path reported runtime-content mismatch before the historical member-count message (`7 passed, 1 failed in 16.91s`). Validation order was narrowed to preserve that contract.
- Combined full files (`test_d0_dev_freeze.py`, `test_d0_b2_math.py`, `test_d0_schemas_statistics.py`): `72 passed, 6 failed in 405.02s` (`406.326s` wall). All six failures were exact legacy message-regex mismatches; no behavioral failure occurred.
- Final minimal message repair focused run: `13 passed in 23.74s` (`24.792s` wall), covering the six former message failures plus all new HMM/B2 attack regressions.
- The 15-minute hard stop prevented a second complete three-file rerun after the message-only repair. Independent I19B verification must perform the one allowed final combined acceptance on these exact bytes.

## Final SHA-256

```text
schemas.py  aa22af0c0ae692f4b21a02a6f928d0e043d954f1393837c39640d2c511c72d1d
freeze.py   39b3f513cd3c18a692cec54e5051a5026ead9107a5cb6407f8710a08c5b0bb3a
b2.py       c732d866bb9455f66d47ee1bd458141e424716b98eb11eb98781eb5b7f2ad2d9
test_d0_dev_freeze.py 771981e29512711581ea637bd4cd821b26836b3da0c48bf1bb42c78a1503d2c5
test_d0_b2_math.py    a823eb20f87d8f77e4b123a7e4800e040ed5e848591bd42b7f704d83798096d9
```

## Protection

- P2 codec `cw_id` coercion: `DEFERRED_NONBLOCKING`; `codec.py` unchanged.
- No `common/`, session/governance, p05 logs, science, real benchmark, staging, commit, or push touched.
