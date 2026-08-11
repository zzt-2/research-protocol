# Step 193 — D0 I20 real-runner direct-script bootstrap repair

> 2026-08-11 | implementation repair | DONE

## Scope

- Only changed `projects/simulation/explore/coded-decoder-feedback/benchmark.py` and `projects/simulation/tests/test_d0_engineering_benchmark.py`.
- Did not run the frozen formal `--watchdog-seconds 720` command outside the existing EB12 test, did not run S1–S4 science, and did not touch `common/` or the four `p05_run*.log` files.

## RED

- Direct script startup used a temporary output and non-formal `--watchdog-seconds 5` argument.
- Result: exit 1 in 2.4 s before CLI parsing.
- Failure: `receiver.py` imported `common._recovery`, but direct script startup did not expose the simulation root; `ModuleNotFoundError: No module named 'common'`.
- Automated regression RED: `test_eb13_direct_script_cli_bootstraps_simulation_imports` failed 1/1 for the same traceback.

## Repair

- Removed the eager module-level `receiver` import.
- `_RealEngineeringWorker` now imports `receiver` only inside the real worker construction boundary, temporarily adds the simulation root for that import, and removes it immediately afterward.
- The frozen CLI authority check remains exact (`ENGINEERING_THROUGHPUT_V1`, root seed `900000001`, watchdog `720`); no persistent global `sys.path` modification was introduced.

## GREEN

- Focused direct-script regression: `1 passed in 1.13s`.
- Full command: `python -m pytest projects\\simulation\\tests\\test_d0_engineering_benchmark.py -q --durations=5`.
- Result: `30 passed in 44.64s`; EB12 real runner call: `15.62s`.
- Actual required slice counts asserted from landed JSONL/receipt: decoder batches `4` (`4/8/12/16`), BPS pairs `6`, unique B2 views `10`, HMM primitive+aggregate rows `1`, atomic JSONL `1`, atomic receipt `1`.
- Forbidden science/fit token scan in production benchmark: `0` matches.
- Owner authority SHA256: `f159efae6c25dff94b1f3a9da4b88993277cfbd864c42a493ae3ef5bd72b067b`; EB10/EB12 verify exact receipt authority binding, complete disjoint work partition, the 4.5/5.0-day PASS boundary, and the 5.1-day hard-blocker boundary.

## Review disposition

- P0/P1: `0/0` found in this repair scope.
- `benchmark.py` SHA256: `4f49fa9f81d05b0af5a4a55ad9fd07cc5a69a7c2cc7ddc2be7cac01dbd45c040`.
- `test_d0_engineering_benchmark.py` SHA256: `1bdd8dd5ab98f6d8e54bb92fe04dec13f2635c1f6e2093aa705861147bbc6c7e`.
- Ready for one independent merged acceptance; no author-review-rereview loop requested.
