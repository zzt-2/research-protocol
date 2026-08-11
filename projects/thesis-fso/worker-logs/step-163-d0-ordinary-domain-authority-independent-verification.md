# Step 163 — D0 ordinary domain authority independent verification

> 2026-08-10 | T117 | CP012 / D0_UNIT_TEST | independent final-byte verification

## Terminal

`D0_ORDINARY_DOMAIN_AUTHORITY_REPAIR_INDEPENDENTLY_VERIFIED`

`P0/P1/P2=0/0/0`

This PASS accepts only the D019/T116 ordinary-domain projection and compiler rewiring. I05/FULL, provenance, HMM, raw FULL positive, benchmark, and science remain open.

## Findings first

1. A fresh extractor read the existing raw owner paths directly and independently rebuilt the 15-field canonical domain payload. SHA-256 exactly matched `15c88476676b727ba338d4cb5acc196dce336f3856818c1557bcfb729b6d0c69`; every raw domain value/order matched the frozen typed view.
2. Owner bytes and the pre-existing owner/scientific/identity seals remained exactly `02d471a...`, `c61c88e...`, and `68d21b4a...`. `D0Contract` remains four fields; the new domain view is a frozen, slotted dataclass; loader I/O remains explicit.
3. Nine independent runtime attacks passed: replacements of `CANDIDATES`, `S2_METHODS`, `FIXTURES`, `POL`, `TUPLES`, `S4_CHECK_IDS`, plus equal-cardinality `ALIASES`, `B_VALUES`, and `NW_VALUES` shadows. For each attack, build plus public assertion and the restored build were object-equal to the baseline.
4. Fresh owner-wrapper/domain matrix rejected `22/22` dataclass and seal mutations; wrong accept/reject=`0/0`.
5. Independent enumeration recomputed every typed consumer PK, work key, phase, operation, and `d0c1-*` ID: bindings=`42967/42967`, computations=`27487/27487`, all seven per-projection counts exact.
6. S2 and BPS logical-ID/consumer-manifest goldens each passed `2/2`; all seven grouping laws passed; two fresh graphs shared zero nonprimitive objects; left-graph tampering did not affect the right graph and was rejected by public fresh recompilation.
7. Static AST found no parallel domain globals, domain strings, or B/Nw literals in `_ordinary_raw_records`; ordinary dataclasses contain no cache/source/HMM/raw-FULL fields. The legacy FULL factory keeps its four-keyword signature. Explicit legacy regression passed `54/54`.
8. Pytest passed `22/22` contract+ordinary and `54/54` explicit old four-file tests, with zero fail/error/skip/xfail/warning.

## Fresh verifier receipts

All commands used:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONHASHSEED='0'
C:\Users\zzt\scoop\apps\python311\current\python.exe -B ...
```

No author test helper, author mutation matrix, or author PASS was used as an oracle.

### Domain, attacks, mutations, and static scope

The stdin verifier independently extracted:

- `controlled_fixture.cells` key order;
- statistical-contract polarization, fixture, candidate, S2-method, and S4-check enums;
- dev-freeze tuple/B/Nw order;
- six ordinary table record-type domains.

It then executed nine attack/restore cycles, 22 wrapper/domain mutations, and AST scope checks.

Exit=`0`; elapsed=`123.1 s`; stdout SHA-256=`b47c2f5881f012b42299685a277c3bd0434d19f4024d9855cf2f09c08bfc28ba`.

```text
DOMAIN_AUTHORITY_PASS assertions=86 seal=15c88476676b727ba338d4cb5acc196dce336f3856818c1557bcfb729b6d0c69 raw_fields=15/15 global_attacks=9/9 mutations=22/22 wrong_accept=0 wrong_reject=0 baseline=42967/27487 attack_seconds=77.225
STATIC_PASS D0_fields=4 loader_reads=2 FULL_signature=unchanged ordinary_scope=no_cache_source_HMM_raw owner_science_identity_seals=unchanged
```

### Full independent identity oracle

The second stdin verifier generated all seven raw-PK domains from the authenticated public domain/contract views, applied the raw owner descriptors independently, encoded canonical JSON locally, and compared every final plan object.

Exit=`0`; elapsed=`21.9 s`; stdout SHA-256=`0b8a34401d3d39cc2e5eadb075e567fdeac945bab5eeba73843786a86b332cf6`.

```text
IDENTITY_ORACLE_PASS assertions=438227 bindings=42967/42967 computations=27487/27487 per_projection=7/7 S2_golden=2/2 BPS_golden=2/2 grouping=7/7 nonprimitive_sharing=0 tamper_rejected=True build_seconds=3.713/4.006
```

Combined independent assertions=`438313`.

### Pytest

```powershell
$py='C:\Users\zzt\scoop\apps\python311\current\python.exe'
& $py -B -m pytest -p no:cacheprovider -q `
  projects/simulation/tests/test_d0_contract_views.py `
  projects/simulation/tests/test_d0_ordinary_identity.py
& $py -B -m pytest -p no:cacheprovider -q `
  projects/simulation/tests/test_d0_contract_views.py `
  projects/simulation/tests/test_d0_waveform_channel.py `
  projects/simulation/tests/test_d0_receiver_codec_methods.py `
  projects/simulation/tests/test_d0_schemas_statistics.py
```

Combined exit=`0`; elapsed=`201.1 s`; stdout SHA-256=`a1134bb78125fd0b45d6b39aa1e58e71033a8ded44a90873a7a8658f62a329ea`.

```text
......................                                                   [100%]
22 passed in 159.11s (0:02:39)
......................................................                   [100%]
54 passed in 39.60s
```

## Exact counts and spot checks

| Projection | bindings | logical IDs | grouping |
|---|---:|---:|---|
| S2-off | 540 | 60 | nine fixtures to one ID |
| S2-on | 1620 | 1620 | one-to-one; three operations |
| S3 | 10800 | 10800 | one-to-one; two phases |
| BPS | 7200 | 3600 | X/Y pair shares one ID |
| B2-clean | 1200 | 600 | X/Y pair shares one ID |
| B2-controlled | 21600 | 10800 | two row polarizations share one ID |
| S4 | 7 | 7 | exact seven-item owner order |
| **Total** | **42967** | **27487** | exact |

## Begin/end protection

| Artifact | SHA-256 |
|---|---|
| owner | `02d471a200a1dce17f2c43dd36ca90b050ebdc943c7c045483e816a07162d140` |
| contract.py | `cb16867116324bcacb373869649322958749ec56888e1fea1f8bb0b35e58853a` |
| schemas.py | `1d782ea4fdf187ad8c57646a65bd025de0b8a3c588c03f5e939d94063ac79a20` |
| contract tests | `ea37c7707db3f8a22ba0a6a9b97a6a88a7b458e474b906b001a0751f3b7ee4e5` |
| ordinary tests | `fdf9d8c1454d748d8b6eb681abc5f2ef2b783cf361f3610ce81c490542a7c19e` |
| waveform tests | `f14cac811b0c68458eb62bbd37578d5dcf592c97cbd4c2ae92765d2e897e01e1` |
| codec tests | `4045a68843400518c999db836533528c1452af9c5f8b9e940c2fd24b24b90348` |
| legacy schema tests | `a94731c3c9d44c1f0ba8ef1b27df578cbb9f982f3069f51786f3becc419dd4c9` |
| step-161 | `8014dbbcdd93bbfdc63b7f2c5a3afff50fbfcf4eb725ffc3deab7683e2e80071` |
| step-162 | `5b59821262d54fc010d6e7e1b46b22d02c6a154052defb1a6de8fa5e1fa848b5` |

- HEAD=`715a65884b988ee737f21982f3bbf372860a1da8`
- staging entries=`0`
- P05 hashes unchanged=`4/4`
- pre-existing tracked cache census=`10/10`; no test cache/bytecode writes were enabled
- `git diff --check` exit=`0` (existing line-ending notices only)
- only this step-163 log was written by T117
- no install, stage, commit, push, benchmark, science, defect smoke, MVE, or held-out execution

## Boundary

T116 final bytes are accepted for D019 only. This does not close I05 or FULL and does not alter D0=`NOT_RUN` or method signal=`NONE`.
