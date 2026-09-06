# Step 086: Ch4 direction-scale family production freeze

> 2026-08-30 | T086 / D065 / V040 / CP027 | development tuning, structural smoke and scientific-manifest freeze only

## Scope and authority

1. Fresh task-control validation returned `PASS` at authority base commit `d3d98c6fc92642e4d6b964d086c1f3bea2018d1d`.
2. T086 retained the frozen production core, common demapper and scaled-unitary implementation. Public roles were mapped before receiver execution as `B0->B0`, `B2_TUNED->B2`, `C4_FWD->C4`, `B3_PSC->B3_PSC`; O1 remained a separate `O1_TRUTH_ONLY` path.
3. Development tuning used weak/moderate/strong scenes, `Np=2/4/8/16`, SNR `15/25/35 dB`, tau candidates `0/0.25/0.5/0.75/1`, 32 shared latent IDs per scene and 4096 payload symbols per polarization.
4. No formal `30000..30127` production cell, thesis-number promotion, paper/manuscript edit, literature search, Groundwork repair, new candidate, commit or push was performed.

## TDD and independent review chronology

- Initial RED: `2 passed / 17 failed`; the reducer, scientific contract and structure-smoke helper modules were intentionally absent.
- First GREEN: `19/19`; the pure Jeffreys objective, exact tie rule, all-12-cell dominance stop, crossing states, grade states, mismatch identity, role mapping and scientific-manifest builder were present.
- Runner/raw-reducer RED added two expected missing-runner failures; later review-driven RED batches covered current-base locking, exact five-tau census, required four-SHA lineage, checkpoint save ordering, temp-only smoke, actual raw provenance, exact manifest authority, restricted grade variants and the executable ID21999 structure-smoke contract.
- Final frozen suite before receipt reissue: `27/27 passed`; all T086 Python files passed `py_compile`.
- Independent static pre-review cleared ID20999 and canonical tuning with `P0/P1=0/0`. Independent raw-only review later reproduced all 12 tau selections with maximum objective difference `0.0`, reproduced the READY terminal, and cleared the final package after a receipt-only test-hash repair.

## Development tuning execution

1. ID20999 tuning smoke ran only in OS temp:
   `C:\Users\zzt\AppData\Local\Temp\t086-b2-smoke-c26841ce047d4607a122c0d558c7fc99`.
   It returned `TUNING_SMOKE_STRUCTURAL_PASS`; census was `3` scene-latents, `36` observation cells and `252` arm rows. Smoke raw SHA was `5e6998fe37b22c876ecff4f0e2f91bb1b5cc86c4cc9fb244b403e62acfa39738`.
2. Canonical tuning IDs `21000..21031` ran exactly once in the frozen grid and completed in `28.448 s`. Census was `96` scene-latents, `1152` observation cells and `8064` arm rows. The checkpoint was deleted only after the atomic raw save succeeded.
3. Canonical raw SHA is `00161c4838a7543878fb191b667935608a242bbdc8ba2849dec4d324113fa315`.
4. Raw-only reduction returned receipt terminal `CH4_B2_TUNING_ACCEPTED` and development terminal `CH4_FAMILY_PRODUCTION_FREEZE_READY`; development numbers are explicitly non-thesis evidence.

Frozen tau map:

| Scene | Np=2 | Np=4 | Np=8 | Np=16 |
|---|---:|---:|---:|---:|
| weak | 1.0 | 1.0 | 1.0 | 1.0 |
| moderate | 0.5 | 1.0 | 1.0 | 1.0 |
| strong | 1.0 | 1.0 | 1.0 | 1.0 |

The tuned baseline did not satisfy the frozen all-12-cell dominance stop, so T086 was allowed to proceed to structure smoke and scientific-manifest freeze. This is not a claim that C4/B3 wins formal production.

## Formal-structure smoke

ID21999 ran only in OS temp:
`C:\Users\zzt\AppData\Local\Temp\t086-family-structure-b809beca903b482cafc993a7e8fda606`.

- Terminal: `STRUCTURE_SMOKE_PASS`.
- Census: `10` actual cells, one delta-zero reference and `50` arm rows.
- Delta zero: channel bytes and all three observation hashes were exactly identical to the moderate/Np2/25 dB primary cell; the reference stored no duplicate rows.
- Positive delta: the adapter used the same Q/R/g/bits/base pilot-noise/base payload-noise latent and changed only `D_delta`.
- Arms were exactly B0/B2_TUNED/C4_FWD/B3_PSC/O1, with O1 separated as `O1_TRUTH_ONLY`.
- Smoke raw SHA: `819680dbd0f640d1ae0e8187f1ab533c537a4f3bc5ef61b79332614a9f2f959f`.
- Smoke receipt SHA: `ea2e830760e5fbda99cc3dbfafece6545c77798d2012f8011dfdeeab92c240cd`.

No smoke artifact entered the repository or any Git worktree.

## Receipt repair and immutable bindings

The first accepted receipt predated the final test file by 82 seconds. Code/tests were then frozen after fresh `27/27` and `py_compile` PASS. The same immutable raw was reduced read-only again; its scientific aggregate content exactly matched the existing aggregate, and the aggregate file was not rewritten.

An initial comparison included the framework-added `_meta` object and therefore stopped before writing; excluding only that non-scientific save metadata produced exact equality. The receipt alone was reissued with current actual hashes.

| Artifact | SHA256 |
|---|---|
| B2 tuning manifest | `e35c418d176904b4048fe1b83fe22865e01223f51017953a6443776b8a6a312a` |
| B2 tuning raw | `00161c4838a7543878fb191b667935608a242bbdc8ba2849dec4d324113fa315` |
| B2 tuning aggregate | `9af3b3af134656863b6a39f8e2d927274d9a82fe0548c95e4dd49429da531378` |
| Final B2 tuning receipt | `afa9189499501a59d65fc549546dd7b88985555c38918cc9cc6b85dba147e2fc` |
| Frozen tests | `f0171ac05a2c5e81d357168051266c82f7441f7fc66e18d8bf452b31546bc182` |
| Tuning runner | `b818b17028aba7d00bfa1f924b81d397a36fdf04153879c89bfd2920e38d26ca` |
| Reducer core | `2d7513beff50190b6104feed43d9daf2baca9ac89e1e8b7dd94ae73b89d7e33b` |
| Reducer entry | `9f9eebed2f61859e52d8fdf7be31a7e042b232d688ffaf11bd40bbeb9d222105` |

Fresh read-only verification matched every recorded manifest/raw/aggregate/tests/runner/reducer hash to the current on-disk file.

## Scientific manifest freeze

`ch4_scientific_manifest.json` was generated once from the actual four accepted tuning artifacts and an explicit 12-entry tau map. Its SHA is:

`417f334844f9092b02bab5d6478381ae7a57e2ff9b4a385ba37707f601521079`

The manifest freezes:

- formal IDs `30000..30127`, 128 latent clusters shared across all slices;
- fixed SNR grid `5:2:41 dB`;
- moderate full curves at `Np=2/4/8/16`, weak/strong full curves at `Np=2`;
- moderate/Np2/25 dB mismatch `delta=0/0.05/0.10/0.20/0.30/0.40`, with delta zero as an exact primary-cell reference;
- whole-curve PCG64 cluster bootstrap seed `2026083007`, 5000 resamples and minimum 4500 valid gain crossings;
- cell-level paired PCG64 bootstrap seed `2026083008`, 5000 resamples, within-scene/Np latent clusters only;
- A/B/C/F grade rules, engineering reference BER `3.8e-3`, and positive gain sign `SNR_required(B2_TUNED)-SNR_required(variant)`;
- exact four-artifact lineage and accepted tau map.

All four lineage SHAs matched the current files. The execution interface remains `PENDING_T087_IMPLEMENTATION`; future runner/reducer/tests hashes are null, and T087 must bind the exact scientific-manifest SHA before its first formal cell.

## Final fresh verification

| Check | Result |
|---|---|
| focused T086 tests | `27 passed in 2.17s` |
| `py_compile` for six T086 Python files | PASS |
| fresh T086 task-control validator | PASS |
| manifest four-artifact lineage and accepted terminal | PASS |
| fixed ID/grid/slices/mismatch/statistics/grade inspection | PASS |
| smoke paths outside all Git worktrees; no tracked smoke pollution | PASS |
| `git diff --check` | PASS, except informational existing LF-to-CRLF warning for T086 task document |

## Files

1. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/b2_tuning_manifest.json`
2. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/run_b2_tuning.py`
3. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/b2_tuning_reducer.py`
4. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/reduce_b2_tuning.py`
5. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/run_family_structure_smoke.py`
6. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/family_freeze_contract.py`
7. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/freeze_ch4_scientific_manifest.py`
8. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/tests/test_direction_scale_family_freeze.py`
9. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/b2_tuning_raw.json`
10. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/b2_tuning_aggregate.json`
11. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/b2_tuning_receipt.json`
12. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/ch4_scientific_manifest_schema.json`
13. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/ch4_scientific_manifest.json`
14. `projects/thesis-fso/worker-logs/step-086-ch4-direction-scale-family-freeze.md`

## Implementer terminal

`CH4_FAMILY_PRODUCTION_FREEZE_READY`

This terminal authorizes no T087 or formal production by itself. It closes only the T086 bounded development-tuning, structure-smoke and scientific-manifest-freeze task.
