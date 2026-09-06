# Step 087 Stage A: Ch4 formal execution seam implementation

> 2026-08-30 | T087 / D066 / V041 / CP028 | implementation and non-simulation tests only

## Scope and authority

1. Fresh task-control validation returned `PASS` for `CH4_FORMAL_EXECUTION_SEAM`, CP028, epoch 28.
2. The frozen scientific manifest remained byte-identical at SHA-256 `417f334844f9092b02bab5d6478381ae7a57e2ff9b4a385ba37707f601521079`.
3. Stage A implemented only the whitelisted formal runner, raw-only reducer, reducer entry, execution-lock builder and focused tests.
4. No ID29999 smoke, formal ID `30000..30127`, receiver simulation, formal raw/reduction, thesis result, execution-lock generation, scientific-manifest edit, production-core edit, governance edit, commit or push was performed.

## TDD evidence

- Initial RED: `15 failed in 0.31s`; all failures were the expected missing runner/reducer/freezer modules.
- First runner slice: `3 passed, 12 deselected`; fixed 119+1 grid, fixed populations/census, no scientific overrides, truth firewall and dual-lock authority were present.
- Independent static pre-review then found one P1: smoke incorrectly depended on the future tracked lock. The runner was repaired so smoke requires an explicitly injected OS-temporary lock outside every Git worktree, while formal production rejects any lock override and can only read the tracked lock.
- The next independent static review found three additional P1s and each was first reproduced as a real RED (`3 failed, 15 deselected`): lowest-grid equality had the wrong crossing precedence; a strong-scene record could reuse the weak-scene RNG namespace; and the canonical reducer entry did not recheck the locked Python/NumPy/platform environment. The fixes now give lowest `BER<=threshold` precedence as `BELOW_RANGE`, validate all seven PCG64 component spawn keys including scenario code and latent ID, and fail the reducer entry closed on any runtime-environment mismatch.
- Final Stage A focused suite after those repairs: `18 passed in 1.29s`.
- Five T087 Python files passed `py_compile`; fresh task-control remained `PASS`.

## Implemented boundary

- Runner: exact smoke/formal populations, 119 actual cells plus one no-row delta-zero reference per latent, five fixed public roles, tuned-B2 lookup only, B3 tau=1, separate O1 truth-only path, Q/R/g mismatch adapter, shared latent and cross-Np payload construction, resumable hash-bound checkpoints, dual-lock and environment fail-close checks.
- Reducer: no runner import and no historical aggregate input; exact header/population/census/role/tau/hash/truth/scene-pairing/delta-zero validation; count-derived Jeffreys curves; BELOW_RANGE/UNREACHED/EXACT_HIT/STABLE/CROSSING_UNSTABLE handling; registered whole-curve and cell-level PCG64 bootstrap; A/B/C/F grading over only C4_FWD and B3_PSC; non-bearing raw-derived mechanism/scene/pilot/mismatch summaries.
- Reducer entry: current on-disk scientific manifest, tracked execution lock, code/tests, frozen dependencies, Git base, raw and output artifact hashes are checked before canonical reduction and receipt publication.
- Lock builder: pure payload construction is separated from the only filesystem-writing `main()`; no lock exists after Stage A.

## Stage A verification snapshot

| Check | Result |
|---|---|
| focused T087 tests | `18/18 PASS` |
| five-file `py_compile` | PASS |
| T087 task-control | PASS |
| scientific manifest actual SHA | exact frozen SHA |
| reducer imports runner | no |
| tracked lock present | no |
| smoke/formal raw, aggregate or receipt present | no |

## Open gate

Stage A independent static review closed at `P0/P1/P2=0/0/3`. The three P2s are checkpoint self-digest rather than deterministic rebuild, future aggregate/receipt sequential replace recovery, and no direct numerical bootstrap regression test. They did not block the one-latent structural smoke.

## Stage B: unique ID29999 OS-temp smoke

The first Stage B attempt stopped before creating a lock or starting the runner: the inline temporary-lock builder had added only the seam to `sys.path`, so importing `projects.simulation.common.save_results` failed with `ModuleNotFoundError: params`. The controller and independent reviewer classified this as a preflight import-path failure that did not consume the one permitted ID29999 execution. No retry was made until a fresh explicit authorization arrived.

Under the new authorization, a new empty OS-temporary directory was created and checked against the complete live `git worktree list --porcelain` root set:

`C:\Users\zzt\AppData\Local\Temp\t087-ch4-formal-smoke-29f7792096f246caa682b9958a5824d7`

The repository root, `projects/simulation`, and seam were then added to `sys.path` in that order. `build_execution_lock()` bound the current four execution hashes, four frozen dependency hashes, HEAD and runtime environment; `save_results()` wrote only the temporary lock, and `runner.resolve_execution_lock_path()` plus `runner.verify_execution_authority()` passed before execution.

| Temporary lock binding | Value |
|---|---|
| lock SHA-256 | `e18239246d1bcbf9b7b54e238ecd0ecd27e277473fb37981bb53d0358fa34f70` |
| runner SHA-256 | `ad0cd1df63b9c715e3073027dffdb6767984661ebfce556093949d62b3f21784` |
| reducer SHA-256 | `f7a3049e98e2039d38771aa3c48f893049dc146f707957ba895476afab81c327` |
| reducer entry SHA-256 | `da1a6db75d5912de9b10c4eb656f7a0d4a073395392aaebc72e306c1c111e4a0` |
| tests SHA-256 | `97f4dbe85f74de18469e83b8375fd185b5471826a2952819675aee33a18bd215` |
| HEAD | `d3d98c6fc92642e4d6b964d086c1f3bea2018d1d` |
| environment | Python `3.11.9`; NumPy `2.4.3`; `Windows-10-10.0.26200-SP0` |

Exactly one runner command was issued with `--smoke`, the new OS-temp output directory and its temporary lock. No `--formal` invocation occurred.

- runner exit: `0`
- elapsed wall time: `3.030558 s`
- runner terminal: `FORMAL_SMOKE_STRUCTURAL_PASS`
- smoke raw SHA-256: `2210d9a5d8e7c846b821c9023fdda4cbac4360c17714a2b9d704dfaf4619e407`
- raw-only reducer census: top-level latents=`1`, scene latents=`3`, actual cells=`119`, arm rows=`595`, delta-zero references=`1`
- delta-zero H and all three reference observation hashes: exact identity; no reference rows
- grade: absent (`null`); `scientific_numbers_reported=false`
- temp directory contents after verification: only the temporary lock and smoke raw
- tracked `ch4_formal_execution_lock.json`, formal raw, aggregate and receipt: all absent

Stage B therefore closes as `FORMAL_SMOKE_STRUCTURAL_PASS`. This is structural evidence only and does not authorize formal IDs, a tracked execution lock, scientific grade, thesis numbers or prose.

## Stage C: tracked execution-lock freeze

The first uniquely authorized direct freezer invocation exposed a CLI-only import bootstrap defect before any file write: `from projects.simulation.common import save_results` raised `ModuleNotFoundError: projects`. The process stopped without retry; tracked lock, `.tmp` and all formal artifacts remained absent. An independent repair added only the direct-CLI import bootstrap and one regression test; ID29999 was not rerun. Independent adjudication accepted the unchanged runner/reducer/entry hashes and the previous smoke, and issued a new one-command freeze authorization.

The final pre-freeze evidence was fresh:

- focused tests: `19 passed in 4.54s`
- five-file `py_compile`: PASS
- task-control: PASS
- HEAD: `d3d98c6fc92642e4d6b964d086c1f3bea2018d1d`
- scientific manifest SHA-256: `417f334844f9092b02bab5d6478381ae7a57e2ff9b4a385ba37707f601521079`
- all four frozen dependency hashes: exact
- runner/reducer/reducer-entry hashes: exact matches to the accepted ID29999 smoke
- tracked lock, stale lock temporary, formal raw, aggregate and receipt: all absent

Exactly one newly authorized command was then issued:

`python projects/simulation/explore/ch4-scaled-unitary-pilot-ls/freeze_ch4_formal_execution_lock.py`

It exited `0` and uniquely generated the tracked execution lock with SHA-256:

`3942883a128f0e38b85d3785be570dc139c3a70c4e21b8986f98a3873a45a492`

Read-only post-freeze verification reproduced every binding from current files:

| Binding | Frozen value |
|---|---|
| schema | `t087.ch4-formal-execution-lock.v1` |
| authority | `T087/D066/V041` |
| checkpoint / epoch | `CP028 / 28` |
| base commit | `d3d98c6fc92642e4d6b964d086c1f3bea2018d1d` |
| scientific manifest | `417f334844f9092b02bab5d6478381ae7a57e2ff9b4a385ba37707f601521079` |
| formal runner | `ad0cd1df63b9c715e3073027dffdb6767984661ebfce556093949d62b3f21784` |
| formal reducer | `f7a3049e98e2039d38771aa3c48f893049dc146f707957ba895476afab81c327` |
| reducer entry | `da1a6db75d5912de9b10c4eb656f7a0d4a073395392aaebc72e306c1c111e4a0` |
| focused tests | `f7085ace191041628f2dac84269f06d2e1ce6add50cff326813502697fe42848` |
| production core | `c78d5303a38f3d6c3562ec5b4f0337cdaba6a2cb07330f31cdfbad3538827e60` |
| common demapper | `bff9873d10e5b68f1262fddcc24788e23630792e82a23a308f8eb5c48f431a10` |
| scaled-unitary | `868780505b55da7df979c75fe07f132bf52b8b8904c4ec88961fbbe38b052fd2` |
| params | `0e87c53364461478eddcd81426d8e04646270c3ea7aa717e3c3b28c5dd2a99e9` |
| environment | Python `3.11.9`; NumPy `2.4.3`; `Windows-10-10.0.26200-SP0` |
| populations | smoke=`[29999]`; formal=`30000..30127` |

`runner.verify_execution_authority(..., purpose="formal")` passed as a static authority check only. No formal runner invocation occurred. The stale `.tmp`, formal raw, aggregate and receipt remain absent.

Stage C stops here pending independent final lock review. The tracked lock must not be regenerated or automatically resigned, and the bound code/tests must not change.
