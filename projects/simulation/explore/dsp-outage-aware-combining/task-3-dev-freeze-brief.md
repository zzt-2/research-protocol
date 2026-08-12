# Task 3 brief: execute dev split and prepare immutable freeze artifacts

Worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`

Time limit: 15 minutes. Scientific MVE execution is delegated. Do not run held-out test seeds. Do not commit; controller owns chronology Commit 1.

Preconditions:

- Read design, implementation plan, Task2 repair report.
- Run `python -W error -m pytest projects/simulation/explore/dsp-outage-aware-combining -q`; require all tests green.
- Run `smoke_core.audit_deployable_information_boundary()`; require empty tuple.
- Confirm `artifacts/dev/raw.csv`, dev aggregate and freeze receipt do not already exist. If any exist, stop and report; never overwrite.

Execution:

1. Invoke `run_split('dev', DEV_SEEDS, artifacts/dev, frozen=None)` exactly once. This is 20 disjoint dev seeds × 18 cells with payload 30,720 symbols.
2. Read raw CSV and run strict `tune_dev`; write `artifacts/dev/aggregate.json` as a sorted JSON object containing:
   - complete frozen tuning output;
   - dev row/pair counts and exact coverage;
   - dev-only diagnostic AUCs clearly labeled NON-TEST/NON-SCIENTIFIC;
   - finite coefficient/range audit;
   - tests/audit evidence.
   Do not run G1–G4 or claim a scientific terminal from dev.
3. Re-read raw and independently rerun `tune_dev`; require byte-identical sorted JSON for the frozen tuning object.
4. Inspect selected threshold/top-L/strongest family and logistic coefficient finiteness. If nonfinite, absurdly singular, coverage incomplete, or strict validator fails, stop without creating receipt.
5. Write `freeze_receipt.json` once via `write_freeze_receipt` with exact required source manifest keys:
   - `design`: design.md
   - `implementation_plan`: implementation-plan.md
   - `smoke_core`: smoke_core.py
   - `run_smoke`: run_smoke.py
   - `test_smoke`: test_smoke.py
   plus dev raw/aggregate supplied to the function.
   Use 2000 bootstrap replicates; receipt must say `test_started=false`.
6. Validate receipt from disk; then recompute every hashed file SHA256 independently and compare.
7. Write `task-3-dev-freeze-report.md` with commands/timing, row/pair counts, frozen B1/top-L/strongest cheap, dev-only AUCs, coefficient audit, receipt path/hash, and explicit statement `HELD_OUT_NOT_STARTED`.

Do not edit source/design/tests/governance. Runtime artifacts and report only. Do not touch unrelated dirty files, p05/coded artifacts, profile, papers, pycache beyond sandbox caches. Return concise evidence to parent.
