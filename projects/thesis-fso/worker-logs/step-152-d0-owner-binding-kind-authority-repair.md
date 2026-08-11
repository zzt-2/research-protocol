# Step 152 — D0 owner binding-kind authority repair

> 2026-08-10 | T106 | `OWNER_BINDING_KIND_REPAIR_READY_FOR_INDEPENDENT_VERIFICATION`

## Scope

Owner-only additive repair for the eleven frozen `binding_kind` authority positions. No source, tests, session files, stage files, scientific fields, or frozen roots are authorized to change.

## Mandatory strict RED

Command semantics: Windows Python 3.11 with `PYTHONDONTWRITEBYTECODE=1` and `PYTHONHASHSEED=0`; parse the owner with a duplicate-key-rejecting PyYAML loader; assert that the global `exact_binding_kind`, all eight projection `exact_binding_kind` fields, and the two golden-input `binding_kind` fields are absent; hash the complete parsed pre-change structure; exit `23` only when all eleven required positions are absent.

```text
{"missing":11,"owner_sha256":"9f12cd11d210aef10c08848ccf42f39183f1ebf5f061d7203d3879335278990d","positions":[{"absent":true,"path":"payload_schemas.consumer_binding_manifest.exact_binding_kind"},{"absent":true,"path":"consumer_bindings.projections.S2_off.exact_binding_kind"},{"absent":true,"path":"consumer_bindings.projections.S2_on.exact_binding_kind"},{"absent":true,"path":"consumer_bindings.projections.S3.exact_binding_kind"},{"absent":true,"path":"consumer_bindings.projections.BPS.exact_binding_kind"},{"absent":true,"path":"consumer_bindings.projections.B2_clean.exact_binding_kind"},{"absent":true,"path":"consumer_bindings.projections.B2_controlled.exact_binding_kind"},{"absent":true,"path":"consumer_bindings.projections.HMM_chunk.exact_binding_kind"},{"absent":true,"path":"consumer_bindings.projections.S4.exact_binding_kind"},{"absent":true,"path":"golden_vectors.S2_off_nine_to_one.inputs.binding_kind"},{"absent":true,"path":"golden_vectors.BPS_dual_pol_shared.inputs.binding_kind"}],"prechange_structure_sha256":"bf41aeb5301991acba1cd3478c30fb6d6e171d394c84214e0b0894b2656d14f4","required":11,"strict_duplicate_key_parse":"PASS","terminal":"STRICT_RED_EXPECTED_MISSING_BINDING_KIND_AUTHORITY"}
stdout_payload_sha256=aa3d59b187b03758e36a0ab0cca4613fe4dec2877877302d666a32019004626b
process_exit_code=23
```

The RED condition is strict and expected: `11/11` frozen authority positions were absent, with no pre-existing conflicting value. The owner remained at SHA256 `9f12cd11d210aef10c08848ccf42f39183f1ebf5f061d7203d3879335278990d`.

## Repair receipt

Exactly eleven additive scalar lines were inserted:

- `payload_schemas.consumer_binding_manifest.exact_binding_kind`
- `consumer_bindings.projections.{S2_off,S2_on,S3,BPS,B2_clean,B2_controlled,HMM_chunk,S4}.exact_binding_kind`
- `golden_vectors.S2_off_nine_to_one.inputs.binding_kind`
- `golden_vectors.BPS_dual_pol_shared.inputs.binding_kind`

Every value is the exact YAML scalar `LOGICAL_COMPUTATION_ID`. No field-order schema, consumer projection, logical ID, binding list, golden root, scientific field, permission, or count was edited.

The post-change owner SHA256 is `ca2c8146dec5edec62984cdadf678d808291cb6b2a736fd99059651fc7a50535`.

## Fresh verification receipt

Command semantics: Windows Python 3.11 with `PYTHONDONTWRITEBYTECODE=1` and `PYTHONHASHSEED=0`; extract the complete step-151 full verifier in memory, update only its frozen receipts and the two manifest builders to consume the saved-input `binding_kind`, then add T106 checks for the eleven exact authority positions, authority-key census, exact line-addition reversal, and parsed-structure reversal. No temporary script was written. The process re-ran strict duplicate-key YAML parsing, the full literal/root/golden/mutation/count/static suite, scientific projection, permissions, approved anchors/aliases, frozen hashes, HEAD/staging, P05, cache census, and `git diff --check`.

```text
{"P0":0,"P1":0,"P2":0,"aliases":"2 anchors + 2 aliases PASS","assertions":738,"cache_census":[202,41,4],"counts":"6/6","failures":[],"golden_details":{"bps_logical_actual":"d0c1-35432848c9e7397e0ba59c5e816b7d2c7764dc403856fb692589a2305444e1cb","bps_logical_expected":"d0c1-35432848c9e7397e0ba59c5e816b7d2c7764dc403856fb692589a2305444e1cb","bps_manifest_actual":"51d43e149ceaa6467b97d94b6e7631591d1e049546d2ace03c1b2228f27c0a1f","bps_manifest_expected":"51d43e149ceaa6467b97d94b6e7631591d1e049546d2ace03c1b2228f27c0a1f","s2_logical_actual":"d0c1-c9cedfe83204c8f37286e0f8b81d1bb35ed21bf22d9ff36a69191c157dc1197c","s2_logical_expected":"d0c1-c9cedfe83204c8f37286e0f8b81d1bb35ed21bf22d9ff36a69191c157dc1197c","s2_manifest_actual":"ed1a72137f1b0bea3208ed46f482206c88ba101bc718cc69faec9246c58607b6","s2_manifest_expected":"ed1a72137f1b0bea3208ed46f482206c88ba101bc718cc69faec9246c58607b6"},"goldens":"10/10","literal_pass":"128/128","mismatch":0,"mutations":"15/15","owner_end_sha256":"ca2c8146dec5edec62984cdadf678d808291cb6b2a736fd99059651fc7a50535","owner_start_sha256":"ca2c8146dec5edec62984cdadf678d808291cb6b2a736fd99059651fc7a50535","permission_drift":"none","projection":"PASS","protection":"PASS","roots":"3/3","verdict":"OWNER_BINDING_KIND_REPAIR_READY_FOR_INDEPENDENT_VERIFICATION"}
stdout_payload_sha256=15ec97a25c15d29cbd9e14327ca1990078518e8b30fe8e305e81cd422cf3d3e8
process_exit_code=0
```

### Exact repair and drift proof

- Authority positions: `11/11` exact; recursive mapping-key census is exactly nine `exact_binding_kind` plus two `binding_kind`, all equal to `LOGICAL_COMPUTATION_ID`.
- Removing the eleven exact inserted lines from the post-change bytes restores pre-change owner SHA256 `9f12cd11d210aef10c08848ccf42f39183f1ebf5f061d7203d3879335278990d`.
- Removing the eleven fields from the parsed post-change document restores pre-change parsed-structure SHA256 `bf41aeb5301991acba1cd3478c30fb6d6e171d394c84214e0b0894b2656d14f4`.
- Scientific projection: PASS; permission drift: none; count drift: none; grid-root drift: none; approved YAML aliases: exactly two anchors plus two aliases.
- S2 manifest root: `ed1a72137f1b0bea3208ed46f482206c88ba101bc718cc69faec9246c58607b6` (`actual == expected`).
- BPS manifest root: `51d43e149ceaa6467b97d94b6e7631591d1e049546d2ace03c1b2228f27c0a1f` (`actual == expected`).

### Protection receipt

- HEAD: `715a65884b988ee737f21982f3bbf372860a1da8`; staging: empty.
- R001: `ff229de3305c179521474ea37e37a748ed2189d824d75e6779708ac89f3992dd`.
- decisions (contains D016): `ca4b7098e8b9ab77575b58ea2abed07e6e356566e38c0ed8901eb0cfabe0d6e7`.
- verifications (contains V010): `7f76040ffe3e9ca0d21abda03f72b8bcdd3ba3e5cc14d950051a892e55485bcb`.
- step-151: `c1b0f39ed0903735387d6d12aaf5963c6a400215da81fa649a4f0e9b9459e535`.
- schemas: `a42ffa184d2db3cfa68775b9dc0b3aac60195bf34abfdf5e37732f398445e401`; tests: `a94731c3c9d44c1f0ba8ef1b27df578cbb9f982f3069f51786f3becc419dd4c9`.
- P05 logs: `7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11`, `735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b`, `c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d`, `95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de`.
- Cache census: `202 *.pyc / 41 __pycache__ / 4 .pytest_cache`; `git diff --check`: PASS.
- No pytest, benchmark, science/MVE, install, stage, commit, or push was run.

## Terminal

`OWNER_BINDING_KIND_REPAIR_READY_FOR_INDEPENDENT_VERIFICATION`

This author-side terminal does not accept D015 and does not authorize schema implementation.
