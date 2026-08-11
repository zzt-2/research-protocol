# Step 206 — D0 S2 damage/headroom independent verification

VERDICT=PASS

S2_SCIENCE_VERDICT=FAIL

## Scope

- Read-only verification of the final S2 artifacts from step-205.
- No physical/channel/decoder execution, code repair, parameter change, B2 execution, staging, commit, or push was performed.

## Findings first

- `P0=0`, `P1=0`, `P2=0`.
- The evidence package is internally consistent and independently reproducible: `VERDICT=PASS`.
- The frozen S2 conjunction does not pass: `S2_SCIENCE_VERDICT=FAIL`.
- Damage fails only its point threshold: point `0.06944444444444449 < 0.10`; CI lower `0.017361111111111122 > 0` and positive cells `3/3` pass.
- Recoverability fails both its point and CI-lower thresholds: point `0.04008151917073723 < 0.10`; CI lower `-0.11234968338626876 <= 0`; positive cells `3/3` passes.
- Consequently the frozen sequential contract requires `SCIENCE_TERMINAL`; B2/S3/S4/C1 and `FAIR_COMPARISON_RUN` remain unrun.

## Exact population and typed reduction

- Raw rows: `1620/1620`; unique frozen row keys: `1620/1620`.
- Domain: exact seeds `8150..8159` x cells `{hard,mid,clean}` x polarizations `{X,Y}` = `60` base clusters.
- Every cluster contains exactly `9` B1-on + `9` O1-on + `9` B1-off projections over the frozen nine fixtures.
- B2 rows: `0`; summary and receipt both declare `b2_disposition=NOT_RUN`.
- Fresh `schemas.row_from_mapping("s2_method", ...)` parsed all `1620` rows. Fresh `reduce_s2_damage_headroom` returned `physical_off_computations=60` and:

| cell | B1-on errors/total | B1-off errors/total | O1-on errors/total | damage | recoverability |
|---|---:|---:|---:|---:|---:|
| hard | `1336/1440` | `1296/1440` | `1296/1440` | `0.02777777777777779` | `0.029940119760479042` |
| mid | `1240/1440` | `1188/1440` | `1188/1440` | `0.036111111111111205` | `0.041935483870967745` |
| clean | `889/1440` | `681/1440` | `846/1440` | `0.1444444444444445` | `0.048368953880764905` |

- Independent arithmetic, separate from the reducer, reproduced macro damage `0.06944444444444449` and macro recoverability `0.04008151917073723` exactly.
- Affected-CW invariants: `affected_cw_errors > affected_cw_total` violations=`0`; `affected_cw_total != 16-boundary_after_cw` violations=`0`; `information_bit_total != 16384` violations=`0`.
- Each cluster's nine B1-off projections share exactly one `(physical_case_id, computation_id, result_receipt_sha256)` owner.

## Independent paired bootstrap

Independent code grouped the raw rows into the exact ten seed blocks, instantiated `numpy.random.Generator(numpy.random.PCG64(2026081001))`, drew `10,000` ten-block resamples per metric, and used linear 2.5/97.5 percentiles.

| metric | point | 95% CI | valid/invalid | positive cells | frozen gate |
|---|---:|---:|---:|---:|---|
| B1 damage | `0.06944444444444449` | `[0.017361111111111122, 0.13055555555555556]` | `10000/0` | `3/3` | **FAIL** (`point < 0.10`) |
| O1 recoverability | `0.04008151917073723` | `[-0.11234968338626876, 0.19036462197308052]` | `10000/0` | `3/3` | **FAIL** (`point < 0.10`, `lower <= 0`) |

These values exactly match `summary.json`; its `S2_VERDICT=FAIL` is therefore correct.

## Affected-codeword semantics and focused tests

- The receipt-bound source computes the boolean error matrix over `16 x 1024` information bits, slices only `errors[boundary:]`, applies per-codeword `any(error)` over the 1024 bits, then counts affected codewords. `information_bit_errors` separately counts all bit errors in the complete frame.
- The focused test constructs two bit errors in one affected codeword and one in another, plus one pre-boundary bit error. It requires `affected_cw_errors=2` and `information_bit_errors=4` for boundaries B04/B08/B12.
- Fresh focused suite: `python -m pytest projects/simulation/tests/test_d0_science_s2.py -q` -> `8 passed in 1.98s`.

## Artifact and protection checks

- `s2-raw.jsonl` SHA-256: `808bbe0124ef6846eefa0dd7c39feb0f974a5cb5b1166c3dab24d0242dd8e4bb` = receipt.
- `summary.json` SHA-256: `62c9b7649a4ce16b330c0f0fd9d3f3ffa6dab2f3d32da1edad625e4c34a7bb9a` = receipt.
- `science.py` SHA-256: `3887e70f738fed2a7f0961a8cc9920094da83c634545f8f50b15d018c3e1cf08` = receipt.
- Owner contract SHA-256: `f159efae6c25dff94b1f3a9da4b88993277cfbd864c42a493ae3ef5bd72b067b` = receipt.
- Receipt `git_head=4e126c7fed28b0f3226f8b674c568dbc760a89fc` = fresh `git rev-parse HEAD`.
- Checkpoint contains `1620` rows and is an exact row multiset match to final raw; the final raw has no missing, duplicate, or extra row.
- Owner YAML, `common/`, `params.py`, and `schemas.py` are clean in scoped git status. Staging is empty.
- S1 artifact hashes remain: raw `e9a5f2ad3e8ebea9d238ecfdac54b88160d4fbe4273314c9a1dcfd39fa5e75ad`, summary `51acd5afeb37507f0ffe6f60f24ec1f6df0e9d11eb79e60a7d15d4b5dda592b4`, receipt `318b80f75fa7707d2a34f8bb5a3be5977bd9ec7cef55bb100bdce02ab558be56`.
- Protected P05 hashes remain 4/4 anchored: `7843b048...f11`, `735e4650...38b`, `c76887c6...34d`, `95a1d184...21de`.

## Severity ledger

- P0: none.
- P1: none.
- P2: none.

## Disposition

- `formal_science_disposition=S2_DAMAGE_OR_HEADROOM_FAILED`
- `mission_method_delta=NONE`
- `thesis_method_disposition=NONE`
- `next_action=SCIENCE_TERMINAL`
- Do not run B2 absorption, decoder-information increment, S4, C1, or `FAIR_COMPARISON_RUN` under the frozen sequential contract.
