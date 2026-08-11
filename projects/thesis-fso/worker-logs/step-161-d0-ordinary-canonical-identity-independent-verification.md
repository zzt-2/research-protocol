# Step 161 — D0 ordinary canonical identity compiler independent verification

> 2026-08-10 | T115 | CP012 / D0_UNIT_TEST | fresh-context independent review

## Terminal

`FAIL — D0_ORDINARY_CANONICAL_IDENTITY_COMPILER_AUTHORITY_GAP`

`P0/P1/P2=0/1/0`

This is the first reproducible blocker. Per T115's immediate-stop rule, the verifier stopped before the broad mutation matrix and pytest suites. This FAIL does not authorize a benchmark or science.

## Finding first

### P1 — ordinary enumeration domains are not supplied by the authenticated owner view

`build_ordinary_identity_plan(owner_authority=...)` authenticates `D0OwnerIdentityAuthority`, but `_ordinary_raw_records` still obtains four identity-bearing domains outside that public owner view:

- local literal `aliases = ("hard", "mid", "clean")`;
- local literals `B = (32, 64)` and `Nw = (31, 61, 127)`;
- mutable module global `CANDIDATES`;
- mutable module global `S2_METHODS[0]` for the S2-off method value.

The final public `identity_binding` view contains typed descriptors that say these values participate in consumer/work keys, but it does not expose an exact authenticated alias order, candidate order, B order, Nw order, or S2-off method literal. The full YAML has scientific/raw-schema occurrences of several domains, but the API accepts only the narrowed owner authority view and does not read those full-owner paths. Production constants therefore become a second authority.

This is executable, not merely stylistic: while owner bytes and both owner-carried seals remained unchanged, rebinding `schemas.CANDIDATES` from its final ten-item tuple to another ten-item tuple with one unauthorized value caused the public factory to produce and the public assertion to accept a different canonical plan.

## Fresh reproduction

The reproduction imported only production public APIs and independently counted the graph. It did not import or call the author test helper, author mutation matrix, or step-160 PASS logic.

Environment:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONHASHSEED='0'
C:\Users\zzt\scoop\apps\python311\current\python.exe -B -
```

Procedure:

1. Load final `D0OwnerIdentityAuthority` from the frozen owner.
2. Build the baseline plan and independently count all seven projections.
3. Rebind only `schemas.CANDIDATES`, replacing its last value with `FORGED_NOT_IN_AUTHENTICATED_OWNER_VIEW` while keeping cardinality ten.
4. Build a second plan with the exact same owner object/seals and call the public `assert_ordinary_identity_plan` while the global remains rebound.
5. Restore the global and call the public assertion on the forged plan again.
6. Parse `_ordinary_raw_records` with `ast` to locate the four non-owner domains above.

Exit=`0`; stdout SHA-256=`bbf83ddcdfc11f6af7dcb94041445c9d124a91e6812493716dd515c6dc810861`.

```text
AUTHORITY_GAP_REPRODUCED baseline=42967/27487 forged=42967/27487 forged_candidate_computations=1080 same_owner_seals=true assert_accepts_while_global_tampered=True rejects_after_restore=True
STATIC_GAPS aliases_local_literal=True B_Nw_local_literals=True CANDIDATES_module_global=True S2_METHODS_module_global=True
COUNTS exact=True baseline_seconds=3.753 forged_seconds=3.983
```

Interpretation:

- Baseline projection counts did equal D018: `540/60`, `1620/1620`, `10800/10800`, `7200/3600`, `1200/600`, `21600/10800`, `7/7`; total=`42967/27487`.
- The forged plan preserved those exact counts and the same owner/identity seals.
- It contained `1080` S3 logical computations whose work key used a candidate absent from the authenticated public owner view.
- `assert_ordinary_identity_plan` accepted that graph while the mutable module global was rebound. Its fresh recompilation therefore reuses the same unauthenticated runtime authority rather than independently returning to owner authority.
- Restoring the global made the same forged graph fail, proving acceptance was controlled by module state, not owner bytes/seals.

## Minimum repair required

Add the missing enumeration domains to the authenticated identity owner and make the compiler consume only those owner fields:

1. exact ordered `cell_aliases = [hard, mid, clean]` for S2/S3;
2. exact S2-off `method_id` literal `GLOBAL_FOUR_ROTATION_DECODER_SELECTION`;
3. exact ordered ten-item S3 `candidate_ids` domain;
4. exact ordered BPS `B_values = [32, 64]` and `Nw_values = [31, 61, 127]`.

Then refresh owner/identity/loader seals and replace all four compiler-side sources with authenticated-view reads. The public assertion must recompile exclusively from that view. A required regression must rebind `CANDIDATES`/`S2_METHODS` and show either no effect or fail-closed behavior; same-cardinality value substitutions must not produce an accepted plan.

Do not repair this by adding a schemas source hash as parallel authority or by weakening T115 counts. Existing module constants may remain raw-row validation conveniences, but they cannot determine owner-authority-only identity enumeration.

## Matrix disposition

| T115 requirement | Result |
|---|---|
| Independent exact counts | PASS (`42967/27487`; all seven per-projection pairs exact) |
| Owner-only canonical enumeration | **FAIL (P1)** |
| Existing S2/BPS goldens and broader spot checks | NOT_RUN after first blocker |
| ≥32 mutation matrix | NOT_RUN after first blocker |
| recursive sharing / graph tamper matrix | NOT_RUN after first blocker |
| new API type-rejection matrix | NOT_RUN after first blocker |
| additive source-scope proof | PARTIAL: new slice located; authority leak blocks acceptance |
| new-file 4/4 and old four-file 53/53 pytest | NOT_RUN after first blocker |

## Protection

No production, test, owner, session, or prior log bytes were changed. Only this step-161 log was written.

| Artifact | SHA-256 |
|---|---|
| owner | `02d471a200a1dce17f2c43dd36ca90b050ebdc943c7c045483e816a07162d140` |
| contract.py | `50ae149a77588c34cedd2a2e8aab5078b6b4e3d4ea310ba85fe577f76f5ca170` |
| schemas.py | `e0770fb935b1a9fdfb822addf5cbecc94a148c1c6b28f312a7960298091906ec` |
| test_d0_ordinary_identity.py | `cda5bd2027a664136670b14f91715be3eea0d3826ce9f4f140823711a0dff485` |
| legacy schema tests | `a94731c3c9d44c1f0ba8ef1b27df578cbb9f982f3069f51786f3becc419dd4c9` |
| step-159 | `9821f06edf897412cac04ed8db69389b5ce20e7e4985120295f9d04fb701d762` |
| step-160 | `b6c671ffac63d2ab874d49a2dcc511d0af288e7599ba9781ba0e68b8ca973538` |

- HEAD=`715a65884b988ee737f21982f3bbf372860a1da8`
- staging entries=`0`
- P05=`4/4` unchanged
- pre-existing tracked cache census=`10/10`; verifier used `PYTHONDONTWRITEBYTECODE=1`
- `git diff --check` exit=`0` (existing line-ending notices only)
- no install, commit, push, stage, benchmark, science, defect smoke, MVE, or held-out execution

## Boundary

T114 final bytes are not accepted. I05 and FULL remain open. D0 remains `NOT_RUN`; method signal remains `NONE`.
