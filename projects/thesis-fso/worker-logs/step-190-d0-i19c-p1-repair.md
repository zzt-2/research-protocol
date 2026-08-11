# Step 190 — D0 I19C three-P1 minimal repair

> 2026-08-11 | implementation/TDD | bounded repair; no real benchmark/science

## STATUS

`DONE`

- P0/P1 after author verification: `0/0` for the three scoped I19C findings.
- Production changes: `artifacts.py`, `benchmark.py`.
- Test changes: `test_d0_artifacts_cost_s4.py`, `test_d0_engineering_benchmark.py`.
- No `common/`, session, owner YAML, P05, staging, commit, push, or scientific execution mutation.

## ROOT CAUSES AND REPAIRS

1. **P1-1 atomic pointer cleanup**: `CURRENT.json` could already have crossed `os.replace` while `pointer_committed` was still false, so exception cleanup deleted the reachable generation. The pointer write now records the actual `replaced` event through an internal wrapper; cleanup removes a generation only when replacement never occurred. A post-replace root-directory-fsync injection now proves the newly pointed generation remains complete and readable.
2. **P1-2 watchdog**: the old implementation called the operation synchronously, then classified elapsed time. It now runs the operation in a Windows-compatible `spawn` process and terminates/joins the worker at the deadline; partial values cannot escape. The I20 default remains exactly `720` seconds. A real one-second operation under a `0.20 s` test deadline is terminated near the deadline and never writes its completion marker.
3. **P1-3 owner digest binding**: the caller-controlled SHA string was removed. Engineering manifests and receipts now accept the authenticated `D0OwnerIdentityAuthority`, run its frozen-authority validator, bind the manifest to its exact `owner_sha256`, and copy that authoritative digest into the receipt. A dataclass-replaced fake authority is rejected. Observed authoritative owner SHA: `f159efae6c25dff94b1f3a9da4b88993277cfbd864c42a493ae3ef5bd72b067b`.

## TDD RECEIPTS

### RED

- Post-replace atomic injection: failed because `CURRENT.json` named a generation deleted by cleanup (`FileNotFoundError`).
- Hard watchdog/typed authority focused run: the authority-based benchmark setup errored because production still required bare `D0Contract`; the old watchdog also had no process boundary.
- Combined initial RED command: `1 failed, 2 errors in 3.29s`.

### GREEN

- The three direct regression behaviors are included in the fresh AC+EB whole-file run below; all were GREEN there.
- AC + EB whole files: `54 passed in 34.35s`.
- Affected CV06–08 + DF11 focused: `6 passed in 6.27s`.
- AC + EB + CV + DF whole files: exit `0`; `111` collected tests; elapsed `116.62s`.
- A redundant second CV+DF-only invocation hit the outer shell `120s` command timeout without a pytest failure report; it does not replace the earlier successful four-file run and was not retried under the bounded repair.
- Observed verification-command runtime total: approximately `5m20s`; no `720s` benchmark was executed.

## FINAL SHA256

- `artifacts.py`: `b032c45cee3dee133bc5242d1d06f7be027181c89374965cbdd1cc42eacd7ea4`
- `benchmark.py`: `9b314bc23c60165580e687c48e5834200de9cc4287ed1b47b0c53c1274caed2b`
- `test_d0_artifacts_cost_s4.py`: `62944263d464d60d45e85a09188a476e11a059cef5f3a359df0852b76dfa708a`
- `test_d0_engineering_benchmark.py`: `c7d786b97daf167af277c30d30fd12e9d23620061edc4b7a91c0fc3b59576670`

## NEXT

Run the single allowed fresh independent I19C acceptance over these final bytes. I19D and I20 remain unauthorized until that acceptance and the subsequent integration gate pass.
