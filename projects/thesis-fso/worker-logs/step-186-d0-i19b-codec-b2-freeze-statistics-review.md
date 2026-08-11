# Step 186 — D0 I19B codec/B2/freeze/statistics independent review

> 2026-08-11 | senior independent reviewer | bounded shard | elapsed `~5m`

```text
VERDICT=FAIL
P0=0
P1=2
P2=1
AXES_CLOSED=2,3,4,5,7
UNRESOLVED=P1 HMM aggregate/authentication binding; P1 zero-variance all-impossible NaN; P2 codec cw_id coercion
STOP_REASON=ALL_ASSIGNED_FILES_AND_AXES_REVIEWED_WITHIN_15_MINUTE_LIMIT
```

## Axis conclusions

- Axis 2 — fresh decoder / exact decoder cost: **PASS in this shard**. `codec.py:155-164,178-193,279-330` caches only the backend object, supplies `message_state=None/warm_state=None` on every call, disables returned state, clamps at the decoder boundary, and receipts exact `20 * cw_batch`. RM evidence and step-171/184 remain consistent. The P2 below is metadata typing, not restart/cost arithmetic.
- Axis 3 — logical exposure: **PASS in scoped evidence**. Owner lines 741-826 freeze logical/materialized totals and distinguish exposure from execution; `schemas.py:338-358,547-563` enforces the per-row BP/cache identities; `statistics.py:259-304` preserves all ten S3 logical candidates and exact 88 changed/72 cached vector. Step-184 independently exercised the integrated cost guards without rerunning I05.
- Axis 4 — exact HMM aggregate / no ordinary-float winner: **FAIL (P1-1)**. `Fraction` selection and explicit ordinary-sum rejection are correct, but the reducer accepts unauthenticated aggregate fields and therefore can select a forged winner.
- Axis 5 — no-refit / non-dev fit: **FAIL (same P1-1)**. Static no-fit reachability is closed by DF11/I18, and caller-supplied `member_seeds` is restricted to 8000-8009, but those seeds are not cryptographically or structurally tied to the supplied chunks.
- Axis 7 — covariance identities / one-way decode / typed fail-closed: **FAIL (P1-2, P2-1)**. B201-B212 covariance and exactly-one-decode-per-polarization tests pass, but valid finite zero-variance all-impossible inputs return NaN, and codec CW identifiers are coerced rather than rejected.

## Strengths

- `codec.py:150-170,178-193,279-330` makes the Sionna version/BG/Z/interleaver contract explicit and keeps message state out of the API path while retaining exact batch and BP receipts.
- `b2.py:50-167,207-274,288-420` cleanly separates transition, moment variance, posterior, state-logsumexp/symbol-maxlog LLR, and one-way decode; covariance/rotation identities have direct focused tests.
- `freeze.py:179-294,446-529,651-845` uses exact rationals for winner keys, persists all candidate keys/raw hashes, and revalidates five+five+one documents at load.
- `statistics.py:110-378` is pure, typed, deterministic, cell-macro aware, and preserves DEV/TEST chronology markers without artifact I/O.
- Fresh focused guard: `52 passed in 19.92s` (`20.786s` wall), covering the full B2 and DF files plus SS03-SS10 nodes. No I05 five-file chain, science, or benchmark was run.

## Issues

### P1-1 — HMM selector trusts detached hashes and aggregate numerators

- Location: `projects/simulation/explore/coded-decoder-feedback/freeze.py:206-264`, `freeze.py:364-378`; contract requirements at owner lines 1546-1557 and 1571-1649.
- Why: `_hmm_candidates` canonicalizes only the typed row shape, then directly consumes `normalized_nll_exact_sum_*`. It never recomputes/checks `chunk_id`, `member_key_manifest_sha256`, `computation_ids_manifest_sha256`, or `content_sha256` against the owner axes/content. `fit_b2_statistics` validates the separate `member_seeds` argument but never binds it to those roots. Thus a row can retain all receipt/root fields while its exact sum is changed, altering the objective and potentially the frozen winner; arbitrary/non-dev member provenance is likewise indistinguishable.
- Fresh reproducer: changing only one typed row's numerator while leaving `content_sha256` and member root unchanged was accepted; objective changed from `1` to `6253/3`. This violates the owner's full typed chunk binding and runtime aggregate-content contract.
- Required repair: consume an authenticated runtime aggregate/content object or deterministically recompute and compare all group/member/computation/content commitments before selection; bind the dev seed axis through the recomputed member manifest. Add negative tests for numerator/content-root mismatch, group/chunk-id mismatch, and roots generated from a non-dev seed set.

### P1-2 — zero-variance all-impossible B2 paths return NaN instead of failing closed

- Location: `projects/simulation/explore/coded-decoder-feedback/b2.py:248-270` and `b2.py:342-359`.
- Why: when every hypothesis is impossible, normalization performs `-inf - (-inf)` in `pilot_state_posterior`, and `data_llr` subtracts two `-inf` log-marginals. Both return NaNs for finite, shape-valid inputs instead of an explicit `B2MathError`. This breaks the I14 no-NaN/fail-closed gate and can feed NaN LLRs toward decode.
- Fresh reproducers: (1) `data_llr(0.123+0.456j, uniform4, mu=1, n0=0, output_clip=None)` returned four NaNs; (2) two unmatched zero-variance pilots made `pilot_state_posterior(...)` return four NaNs.
- Required repair: detect an all-impossible normalization/bit partition before subtraction and raise `B2MathError` (or define and test a contract-approved deterministic terminal); add both regression cases.

### P2-1 — codec silently stringifies invalid CW identifiers

- Location: `projects/simulation/explore/coded-decoder-feedback/codec.py:286-293`.
- Why: `tuple(str(value) for value in cw_ids)` accepts integers and arbitrary objects, weakening the otherwise exact typed/fail-closed provenance boundary. `run_b2` rejects these before calling the codec, but direct B0/B1/codec callers are not protected by that wrapper.
- Required repair: require each ID to be an exact non-empty `str` before conversion/copy, and add RM negative coverage.

## Files read

```text
FILES_READ=
projects/thesis-fso/coded-decoder-feedback-groundwork/d0-implementation-plan.md (owner/I04/I05/I07/I10/I13/I14/I15/I19B sections)
projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml (lines 80-125,730-830,1480-1660,2060-2130)
projects/simulation/explore/coded-decoder-feedback/{codec.py,b2.py,freeze.py,statistics.py,schemas.py}
projects/simulation/tests/{test_d0_receiver_codec_methods.py,test_d0_b2_math.py,test_d0_dev_freeze.py,test_d0_schemas_statistics.py}
projects/thesis-fso/worker-logs/step-{171,174,177,179,181,184}-*.md
```

## Receipt SHA-256s

```text
RECEIPT_SHA256S=
step-171 896834e8d269276b934af0dc53cdb3b2ad9736184a81b13514b51757cb04c9bc
step-174 89a20da5b963da648c638eda7321039cdee4c17f63b6b1a3f3da48c8a5af22ca
step-177 58cbcab1209d22fd0d7aaa4aa0cde872362d6c05f8ced1f62f7d247857bb0177
step-179 7c1ed6d2b2e0d3dbfaf5d4ac5a1a901aa2dbb326fc0e9aa47a0888943808b03c
step-181 e28184abcc71d2c3f47772a9993417b129f526add71876cd71a6adb53e0276ef
step-184 f274160082fd376f34ccf777aba6eaafc98a439a0630a58aa231504c7017412d
```

## Protection

- Staging: `0`; `common/` status entries: `0`.
- P05 logs remain untracked and unchanged at `7843b048...4f11`, `735e4650...38b`, `c76887c6...34d`, `95a1d184...21de`.
- Reviewer modified no production, tests, session/index, staging, or protected logs; this review log is the only write.
- D0 science remains `NOT_RUN`; no BER/goodput/method-signal conclusion is made.
