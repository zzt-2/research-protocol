# Step 149 — D0 owner canonical identity contract retry

> 2026-08-10 | T103 | PASS

## Prechange frozen receipt

- HEAD: `715a65884b988ee737f21982f3bbf372860a1da8`
- staging entries: `0`
- owner SHA256: `c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d`
- R001 SHA256: `679e437b052f5b664f2aae1a42f7268482612c396d9a613d6ea6c18e1d285a4d`
- D015 decisions SHA256: `376c3e740a6e4987734bcb64ebf96ffe417d5566ce4342a01e2f20ca2f5674b0`
- V009 verifications SHA256: `16957db808e656f5c13bb982aa3c4477846f6264af2668abbe6ad85207d6d56f`
- step-148 SHA256: `c089a52190988b7695e6df66a153984ef1bf06f8ade98132a63145490eea31af`
- schemas.py SHA256: `a42ffa184d2db3cfa68775b9dc0b3aac60195bf34abfdf5e37732f398445e401`
- step-147 SHA256: `a08213733ba451cca0e66da4a5582b455aed071b296abb448d05dd760821041f`
- P05 SHA256: `7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11`, `735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b`, `c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d`, `95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de`
- cache census: `202 *.pyc / 41 __pycache__ / 4 .pytest_cache`

## Mandatory prechange RED

Environment: Windows Python 3.11, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONHASHSEED=0`.

Command semantics: a standalone `yaml.SafeLoader` subclass rejected duplicate mapping keys, canonicalized the parsed owner with UTF-8 JSON (`sort_keys`, compact separators, `ensure_ascii=false`, `allow_nan=false`), asserted the top-level D015 block and ten required sections, and exited `23` when absent.

```text
strict_duplicate_key_parse=PASS
prechange_structure_sha256=8071705e449e29f88d6dd33022b7d5cae56b36ddc78e26ab83861f48ac65a439
required_assertions=11
missing=identity_binding_contract
RED=EXPECTED_MISSING_D015_IDENTITY_BINDING_CONTRACT
exit_code=23
```

The exact UTF-8 output above, joined with LF and no trailing newline, has SHA256 `b0cc0ad7ea95757ad0bec29c8c168cead721c1dd18fc49c98ae9b510a1097cd4`.

Owner editing had not begun when this RED receipt was written.

## Postchange verification

Terminal: `OWNER_IDENTITY_CONTRACT_READY_FOR_INDEPENDENT_VERIFICATION`.

The complete additive block was inserted once, after `statistical_contract_repair` and before `strata`. An initial static attempt caught a literal leading `+` on the block key; that character-level transfer defect was corrected before any PASS claim, and the entire verifier was rerun from final bytes.

Final author-side static result:

```text
strict_duplicate_key_parse=PASS
assertions=330
mismatches=0
grid_literals=122+6
grid_roots=3/3
golden_classes=8/8
count_formulas=6/6
postremove_structure_sha256=8071705e449e29f88d6dd33022b7d5cae56b36ddc78e26ab83861f48ac65a439
scientific_field_drift=none
cache_census=202/41/4
owner_sha256=9f12cd11d210aef10c08848ccf42f39183f1ebf5f061d7203d3879335278990d
errors=[]
```

The independent script regenerated the 122 NumPy 2.4.3 `p_s` literals and six sigma literals, all three grid commitments, four HMM chunk/member/computation manifests, S2 nine-to-one, BPS dual-pol sharing, the synthetic runtime exact-sum content root, and all six ledger formulas. It did not import production digest/key helpers.

## Final protection receipt

- exact top-level placement: `statistical_contract_repair < identity_binding_contract < strata` — PASS
- owner key count: exactly one — PASS
- frozen R001/D015/V009/step-148/schemas.py/step-147 hashes — PASS
- four P05 hashes — PASS
- HEAD: `715a65884b988ee737f21982f3bbf372860a1da8` — PASS
- staging entries: `0` — PASS
- cache census: `202 *.pyc / 41 __pycache__ / 4 .pytest_cache` — unchanged
- `git diff --check`: exit `0`
- owner trailing-whitespace matches: `0`
- writes performed: owner YAML and this step-149 log only
- pytest/benchmark/science/MVE/web/install/commit/push/stage: none

The PASS ceiling is owner readiness only. D015 schema bindings remain forbidden until a separate verifier accepts the final owner bytes.
