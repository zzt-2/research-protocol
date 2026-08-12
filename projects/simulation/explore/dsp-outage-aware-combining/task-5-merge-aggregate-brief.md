# Task 5 brief: merge frozen held-out raw and compute the unique scientific terminal

Worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`

Time limit: 15 minutes. Do not edit source/design/tests/receipt. Do not commit. Runtime result/report files only.

1. Verify HEAD=`cbb8a2d`, 43 tests pass, recursive information audit empty, receipt SHA/hash/test_started=false all valid.
2. Independently verify part-00..04 metadata and raw hashes; require disjoint exact seeds 10000..10099, each 20×18 pairs and frozen method schema.
3. Confirm merged targets do not exist. Call `merge_raw` over the five raw files to `artifacts/test/raw.csv` with exact `TEST_SEEDS` and 18 cell IDs.
4. Verify merged raw: 100 seeds ×18=1800 pairs; expected 12,600 rows (5×2520); exact one receiver hash/pair; no duplicates/missing; only test split and frozen arms.
5. Load `frozen` from receipt and call strict `aggregate_from_raw(..., bootstrap_replicates=2000, bootstrap_seed=20260811)` exactly once for the official aggregate. Write sorted `artifacts/test/aggregate.json` and `terminal.json`.
6. Independently reread merged raw and recompute a second aggregate in memory with the same frozen contract; require byte-identical sorted JSON. Do not change thresholds, models, seeds, cells, MDEs, event definitions, or gate order.
7. Record G1–G4 point estimates, 95% cluster CIs/valid replicates, pass flags, and the unique fail-stop terminal. If G1/G2 fail, later gates may be reported diagnostically but terminal must remain the first fail-stop. Preserve novelty debt regardless.
8. Write `task-5-merge-aggregate-report.md` with hashes/counts, exact commands, G1–G4, terminal, and explicit claim ceiling (problem candidate only if all pass; never method/novelty/Go).

Do not modify governance or interpret beyond the frozen terminal. Do not touch unrelated dirty files.
