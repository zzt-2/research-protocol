# Step 187 — D0 I19C artifacts / benchmark / scope review

> 2026-08-11 | independent bounded code review | 15-minute hard stop

## VERDICT

`FAIL`

- P0/P1/P2: `0/3/0`
- Focused guards: `59 passed in 13.66s` (`14.8137534s` process wrapper), but two direct negative probes reproduced uncaught contract failures.
- No production, test, owner, session, index, common, P05, staging, commit, real benchmark, or science mutation was made. This log is the sole write.

## P0

None.

## P1

### P1-1 — post-replace pointer failure destroys the last readable bundle

- File: `projects/simulation/explore/coded-decoder-feedback/artifacts.py:356`, `:360`, `:558`, `:561-563`
- Why: `_write_bytes_atomic()` replaces `CURRENT.json` before directory fsync/read-back can fail. `write_bundle_atomic()` sets `pointer_committed=True` only after that helper returns; therefore a post-replace fsync error enters the `not pointer_committed` cleanup and deletes the generation already named by the new pointer. This violates old-complete-target preservation and fail-closed atomic publication.
- Fresh probe: injected an `OSError` only for the bundle-root directory fsync. Result was `OLD_POINTER_PRESERVED=False`, `CURRENT_VALID=False`; validation failed because `CURRENT.json` named a deleted generation.
- Coverage gap: AC failure tests stop before pointer replacement (`test_d0_artifacts_cost_s4.py:225-244`) and do not inject the post-replace/pre-return failure window.

### P1-2 — the 720-second watchdog does not enforce a hard stop

- File: `projects/simulation/explore/coded-decoder-feedback/benchmark.py:277-296`
- Why: `watchdog_call()` invokes `operation()` synchronously and only measures elapsed time after it returns. A hung/very slow real benchmark can exceed 720 seconds arbitrarily; the function merely labels the eventual result `INCOMPLETE`. This does not implement owner `watchdog_minutes: 12` (`d0-defect-smoke-contract.yaml:2546-2550`) or plan I17's watchdog gate.
- Fresh probe: a 1.2-second operation under a 1-second watchdog returned only after `1.203s`; `WATCHDOG_STATUS=INCOMPLETE` but `HARD_STOP_ENFORCED=False`.
- Coverage gap: EB07 uses a fake clock around an immediately returning lambda (`test_d0_engineering_benchmark.py:184-196`), so it proves post-hoc classification, not interruption.

### P1-3 — `owner_budget_sha256` is caller-declared, not bound to owner bytes

- File: `projects/simulation/explore/coded-decoder-feedback/benchmark.py:366-383`, `:435-455`; `projects/simulation/tests/test_d0_engineering_benchmark.py:262-282`
- Why: receipt construction checks only lowercase-hex shape. It never receives/recomputes owner bytes, never compares the digest with the loaded contract owner, and `EngineeringManifest` carries no owner digest. The passing EB10 path deliberately supplies `"a" * 64`, while the actual owner SHA is `f159efae6c25dff94b1f3a9da4b88993277cfbd864c42a493ae3ef5bd72b067b`. A syntactically valid receipt can therefore claim an unrelated budget authority while still becoming `ENGINEERING_THROUGHPUT_PASS`.
- Consequence: the otherwise correctly encoded four budget equations and eight-field owner record are not exact-bound to the authoritative seven-day budget.

## P2

None.

## Strengths

- `artifacts.py:145-192,376-404,469-556,588-672` canonicalizes exact UTF-8 JSON/JSONL bytes, validates before writes, hashes landed bytes, and publishes the data receipt after all data artifacts.
- `benchmark.py:317-349,403-455` strictly validates all eight owner runtime fields, partitions completed/remaining work IDs, uses exact `float.hex()` projection binding, and implements the frozen four budget equations with exact 7.00-day ceiling behavior.
- `benchmark.py:500-525` exposes only the frozen engineering CLI and refuses execution without an injected runner; `verify.py` keeps scientific verdict fixed to `None`.
- Fresh AC/EB/CV06–08/DF11 guards were green: `59/59`; final reviewed source/test hashes exactly match step-184's manifest.
- Staging is empty; `common/` has zero status entries; the four protected P05 logs remain untracked/unstaged with their step-184 hashes.

## Issues

See P1-1 through P1-3. No axes 1–7 or A/B technical shard conclusions were reopened.

## AXES_CLOSED

- Axis 8 (atomic exact bytes / receipt-last): `OPEN — P1-1`.
- Axis 9 (watchdog / seven-day budget / owner binding): `OPEN — P1-2, P1-3`.
- Axis 10 (no-science / scope / import-time I/O): `CLOSED` for reviewed final bytes.
- Protection items: `CLOSED` for staging/common/P05/no-science/import-time I/O; governance files are dirty pre-existing project state, and this reviewer did not modify them.

## FILES_READ

- Owner/control/artifact/budget: `projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml` (control 1-35; dev artifact 827-1064; write anchor 2055-2084; budget 2521-2562).
- Plan/state: H005, topic-index scope/invariants, master-state entry, `d0-implementation-plan.md` I19C/I20 clauses.
- Production: `artifacts.py`, `verify.py`, `benchmark.py`.
- Tests: AC01–12, EB01–11, CV06–08, DF11 in the four named D0 test files.
- Receipts: step-176, step-182, step-183, step-184.
- Complete current manifest: `git status --porcelain=v1 -uall` (303 entries: `.sessions` 130, D0 production 13, D0 tests 9, common 0, protected P05 4); step-184's 13-production/eight-test hash manifest was checked against current final bytes.

## RECEIPT_SHA256S

- step-176: `805bda45108524daaa7eaaa5080fe6cb03f96f1a5128bffd67cd400c6c1673cf`
- step-182: `f749a225bac5694020dbbe57e2856ccde80ac493b77987523bf1e984b564f2f5`
- step-183: `5c10fa3c3f140e2627b0abaf5f48342e7c2f9703990621b41df176b91f5f01c8`
- step-184: `f274160082fd376f34ccf777aba6eaafc98a439a0630a58aa231504c7017412d`

## UNRESOLVED

- Repair P1-1 with a post-replace failure state that never deletes the generation reachable from the landed pointer, plus a direct regression injection after pointer replacement.
- Replace the post-hoc timer with a real enforceable 720-second termination boundary suitable for the I20 execution model.
- Bind the benchmark budget digest to authoritative owner bytes (or an owner-loaded typed authority) and reject any caller-declared mismatch.
- I19D and I20 remain unauthorized until the affected I19C axes receive the one allowed minimal repair and fresh independent acceptance.

## STOP_REASON

`SHARD_COMPLETE_WITH_NEW_P1` — axes 8–10 and all requested protection items were examined within the 15-minute box; stopped on three reproducible P1 findings rather than broadening into fixes or A/B re-review.
