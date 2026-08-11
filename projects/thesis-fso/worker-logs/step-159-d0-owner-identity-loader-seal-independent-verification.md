# Step 159 — D017 owner identity loader seal independent verification

> 2026-08-10 | T113 | CP012 / D0_UNIT_TEST | independent final-byte verification

## Scope and terminal

- Evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
- Frozen HEAD: `715a65884b988ee737f21982f3bbf372860a1da8`
- This verifier did not use step-158 PASS, its helper, mutation matrix, or diff assertion. It built a fresh public-view canonical oracle and a fresh mutation matrix.
- Only this step-159 log was written. No install, commit, push, stage, benchmark, science, defect smoke, MVE, or held-out execution occurred.

Terminal: `D017_OWNER_IDENTITY_LOADER_SEAL_INDEPENDENTLY_VERIFIED`

## Findings first

1. Fresh canonical oracle passed `1107` assertions: literals `128/128`, grid roots `3/3`, anchors `8/8`, D017 descriptor totals `32/41/49`, signatures `8/8`, and S4 check IDs `7/7`.
2. Final seals recomputed from current bytes/public frozen view exactly match owner `02d471a...`, identity `68d21b4a...`, and scientific projection `c61c88e...`.
3. Static source proof passed: `D0Contract` remains exactly four fields; the new loader performs its two owner reads and one `load_contract` call only inside the explicit loader function; channel has no owner-identity loader/view reachability and its three contract-bearing functions accept `D0Contract`.
4. Replacing the final owner and identity constants exactly once each with their old values reproduces source SHA `0df83a86...`; therefore the production change from the pre-source is exactly those two constants.
5. Fresh adversarial matrix passed `48/48` rejects (`40` serialized-owner mutations plus `8` dataclass/hash-spoof mutations), including old-owner/old-identity mixed seals, same-type descriptor swaps, phase/operation maps, S4, HMM reference, and grid changes. Wrong accept/reject=`0/0`.
6. Fresh I06 additive matrix passed `35` cases (`6` legal, `29` illegal; `25` frozen-contract mutations), mismatch=`0`; static channel reachability contains no new loader path.
7. Pytest: exact four nodes `4 passed`; mutation node `1 passed`; explicit four-file suite `53 passed`. No fail, error, skip, xfail, or pytest warning.

## Fresh commands and receipts

Environment for every Python/pytest invocation:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONHASHSEED='0'
C:\Users\zzt\scoop\apps\python311\current\python.exe -B ...
```

### Independent oracle and source reverse proof

The verifier was supplied through stdin and independently:

- converted only the public frozen `D0OwnerIdentityAuthority.identity_binding` view into canonical JSON;
- recomputed owner, identity, scientific projection, and all three grid roots;
- checked every indexed binary64 literal and both four-anchor views;
- hard-coded the D017 ordinary/HMM signatures, ordered descriptors, atom/source rules, S4 IDs, and HMM manifest reference from D017 rather than importing production private formula helpers;
- parsed `contract.py` and `channel.py` with `ast` for the static boundary checks;
- inverse-replaced the two final production constants.

Exit=`0`; stdout SHA-256=`ed9696602dbc7e91b16e79c75ee3a5bf03d2c1ee939260cb427da241baf972a2`.

```text
ORACLE_PASS assertions=1107 literals=128/128 roots=3/3 anchors=8/8 descriptors=32/41/49 signatures=8/8 s4=7/7
SEALS owner=02d471a200a1dce17f2c43dd36ca90b050ebdc943c7c045483e816a07162d140 identity=68d21b4af54e43e34f23e882a3ebf0be8393d67487877471a787a8e2b3d4371f science=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
SOURCE_REVERSE replacement_owner=1 replacement_identity=1 pre_contract=0df83a86105a9ff5f8c76d2d937b7ac2a99f51f7d97783f7d3f4260c4d5bfc94 D0Contract_fields=4 loader_reads=2 channel_contract_annotations=3
```

### Fresh mutation matrix

Each serialized-owner variant was created only in an auto-deleted system temporary directory. Dataclass variants were in memory. No author mutation helper or matrix was imported.

Exit=`0`; stdout SHA-256=`f7e1e94c2fb4f0a1ef5efc3ca8edcddd100c21b657b2bd27d358ea4adb02c186`.

```text
MUTATION_PASS mutations=48/48 yaml=40 dataclass=8 wrong_accept=0 wrong_reject=0
CATEGORIES hash_spoof=4 old_owner_identity_mix=3 same_type_swaps=3 phase_op_maps=10 S4=3 HMM_reference=8 grid=5 headers_sections=5
```

### Fresh I06 additive regression matrix

The independent matrix called only public frozen-contract/action guards. It accepted the original contract and five engineering/static actions, rejected four scientific actions, and rejected 25 distinct frozen-contract mutations.

Exit=`0`; stdout SHA-256=`0bb03866000103689b2a2707cb20f8e62c8e877f4070f180badd913e9240c634`.

```text
I06_ADDITIVE_PASS cases=35 legal=6 illegal=29 mismatch=0 no_new_loader_runtime_reachability=STATIC_PASS
I06_CONTRACT_FIELDS=4 mutated_contract_cases=25
```

### Pytest

```powershell
$py='C:\Users\zzt\scoop\apps\python311\current\python.exe'
& $py -B -m pytest -p no:cacheprovider -q `
  projects/simulation/tests/test_d0_contract_views.py::test_owner_identity_authority_exact_frozen_view `
  projects/simulation/tests/test_d0_contract_views.py::test_owner_identity_grid_commitments_recompute_exact `
  projects/simulation/tests/test_d0_contract_views.py::test_owner_identity_d017_descriptors_and_hmm_reference_exact `
  projects/simulation/tests/test_d0_contract_views.py::test_owner_identity_loader_preserves_existing_contract_runtime
& $py -B -m pytest -p no:cacheprovider -q `
  projects/simulation/tests/test_d0_contract_views.py::test_owner_identity_mutations_fail_closed
& $py -B -m pytest -p no:cacheprovider -q `
  projects/simulation/tests/test_d0_contract_views.py `
  projects/simulation/tests/test_d0_receiver_codec_methods.py `
  projects/simulation/tests/test_d0_schemas_statistics.py `
  projects/simulation/tests/test_d0_waveform_channel.py
```

Combined exit=`0`; combined stdout SHA-256=`ad292e045347c668785ea06160310fb8e12a0f4ed556a36afb17abf53e245287`.

```text
....                                                                     [100%]
4 passed in 1.52s
.                                                                        [100%]
1 passed in 5.91s
.....................................................                    [100%]
53 passed in 39.80s
```

## Begin/end protection

The following hashes were observed before verification and rechecked after all executable checks:

| Artifact | SHA-256 |
|---|---|
| owner | `02d471a200a1dce17f2c43dd36ca90b050ebdc943c7c045483e816a07162d140` |
| contract.py | `50ae149a77588c34cedd2a2e8aab5078b6b4e3d4ea310ba85fe577f76f5ca170` |
| test_d0_contract_views.py | `3da14d85a9a743726f985897ac65cd70f331069dcecdfefbd6d09296cba272be` |
| schemas.py | `a42ffa184d2db3cfa68775b9dc0b3aac60195bf34abfdf5e37732f398445e401` |
| test_d0_schemas_statistics.py | `a94731c3c9d44c1f0ba8ef1b27df578cbb9f982f3069f51786f3becc419dd4c9` |
| channel.py | `af32b357ad8f270cce0e8343f2437b23399f9ee6770907ad21ff1b23d2ea18b6` |
| decisions.md | `b20e8ffc5c28a0335ccf5da3791e3e462bbfdd7e1ed49682cc986350497a5bc8` |
| verifications.md | `beaa804651c37e0f2e33415bfc7cb2cf261f492f2121e9811696f34fa87dbfe8` |
| R001 | `1882c9d51a43a75efd3d56cb708edde2a1d88b06e850ba0dbe63821402095d37` |
| step-157 | `bfab0aac3434a9aae22adb7b5e0d5e3963b2b5c534d3fb18ef85db7311057b78` |
| step-158 | `8822c12890d083e1a0ca720c0e9ebca24489715d3ffd566e092acfeab03a3dc5` |

Protection summary:

- HEAD=`715a65884b988ee737f21982f3bbf372860a1da8`
- staging entries=`0`
- `git diff --check` exit=`0` (existing line-ending notices only; no whitespace error)
- pre-existing tracked cache census remains `10/10` `__pycache__`/`.pyc`; pytest ran with `-p no:cacheprovider` and `PYTHONDONTWRITEBYTECODE=1`
- P05 hashes unchanged `4/4`: `7843b048...`, `735e4650...`, `c76887c...`, `95a1d184...`
- Source/test/owner/session artifacts above remained byte-identical; only this log was added by T113.

## Severity and boundary

- `P0/P1/P2=0/0/0`
- This PASS closes only the D017 final-owner typed-loader seal refresh and permits handoff of that authority to the schema compiler.
- It does not close I05, authorize an engineering benchmark, run D0 science, establish a method signal, or authorize MVE/held-out/Contract/Execute.
