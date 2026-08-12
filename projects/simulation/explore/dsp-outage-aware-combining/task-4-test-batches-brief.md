# Task 4 brief: execute frozen held-out batches

Worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`

Time limit: 15 minutes. This is scientific MVE execution. Do not edit source/design/tests/freeze receipt. Do not aggregate or interpret G1–G4. Do not commit.

Controller will assign one or more explicit 20-seed batches. For each assigned batch:

1. Verify HEAD contains chronology Commit 1 `cbb8a2d`.
2. Run strict tests and `audit_deployable_information_boundary()`; require PASS/empty.
3. Validate `freeze_receipt.json` from disk, require receipt SHA256 `5d958f8bc64320f0010937c1011d3fb5165d2194bded62f0ad81526e7a95242e`, `test_started=false`, and all 7 hashes current.
4. Confirm the exact output `artifacts/test/part-XX/raw.csv` does not exist.
5. Call `run_split('test', exact_assigned_seeds, part_dir, {'freeze_receipt_path': absolute_receipt_path})` once.
6. Validate raw contains only split=test, exact assigned seeds × all 18 canonical cells, one receiver hash per pair, complete branch/method schema. Frozen test rows must contain only B0, frozen B1=-8 dB, frozen B2 L=K, and O1—no candidate grid, no diagnostic action, no soft method.
7. Write `artifacts/test/part-XX/metadata.json` with seed list, raw rows/pairs/bytes/SHA256, receipt SHA, HEAD, tests/audit evidence, start/end UTC, and `scientific_interpretation=NOT_PERFORMED`.
8. Return exact counts/hash/timing. Do not inspect aggregate gates or claim any result.

Never overwrite an existing part. Do not touch unrelated dirty files, profile, papers, p05/coded artifacts, or governance.
