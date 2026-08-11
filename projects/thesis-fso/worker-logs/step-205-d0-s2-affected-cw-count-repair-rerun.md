# Step 205 — D0 S2 affected-CW count repair and exact rerun

STATUS=SCIENCE_FAIL_STOP

## Root cause and bounded repairs

- The first exact 1620-row S2 run was scientifically invalid because `_s2_row` wrote the suffix **bit-error count** into `affected_cw_errors`; 1311 rows consequently had `affected_cw_errors > affected_cw_total`.
- Focused RED used canonical `16×1024` information-bit arrays. For B04/B08/B12, two bit errors in one affected CW plus one in a second affected CW produced observed `3` instead of expected `2`: `3 failed in 6.59s`.
- Minimal GREEN computes `any(error)` along the 1024 information bits of each affected CW and counts affected CWs with at least one error. `information_bit_errors` remains the full-frame bit-error count. No clamp, schema change, metric change, population reduction, or gate change was used.
- Focused S2 after this repair: `7 passed in 1.55s`; combined S1/S2 regression: `13 passed in 3.11s`.
- The invalid S2 output directory was deleted in full and the exact workload was rerun from zero. It completed all 1620 rows with `0` errors-over-total and exact B04/B08/B12 totals `12/8/4`.
- Final artifact serialization then exposed a separate local blocker: the S2 raw sort key included boolean `jump_present`, while the frozen artifact writer accepts only finite string/int/float atoms. A focused RED reproduced the missing supported total-order key (`1 failed in 1.86s`). The local S2 runner now sorts by existing scalar identity fields including `projection_role`, `method_id`, `physical_case_id`, and `computation_id`; the generic artifact writer was not changed.
- Final focused S2: `8 passed in 1.95s`; final combined S1/S2 regression: `14 passed in 3.92s`.
- Finalization resumed from all `60/60` completed base clusters; no physical computation was rerun during finalization.

## Exact workload and independent validation

- typed rows: `1620/1620`
- unique row keys: `1620/1620`
- base seed/cell/polarization clusters: `60/60`
- physical B1-off computations: `60`
- B2 rows: `0`; `B2=NOT_RUN`
- affected-CW invariant violations: `0`
- affected totals by boundary: B04=`12`, B08=`8`, B12=`4`
- bootstrap: `10,000` valid replicates for each gate; invalid replicates=`0`

Independent typed reduction from the completed checkpoint reproduced:

| cell | B1-on errors/total | B1-off errors/total | O1-on errors/total | damage | recoverability |
|---|---:|---:|---:|---:|---:|
| hard | 1336/1440 | 1296/1440 | 1296/1440 | 0.02777777777777779 | 0.029940119760479042 |
| mid | 1240/1440 | 1188/1440 | 1188/1440 | 0.036111111111111205 | 0.041935483870967745 |
| clean | 889/1440 | 681/1440 | 846/1440 | 0.1444444444444445 | 0.048368953880764905 |

## Frozen gates

- B1 damage point: `0.06944444444444449`
- B1 damage 10k cluster-bootstrap CI: `[0.017361111111111122, 0.13055555555555556]`
- damage positive cells: `3/3`
- damage gate: **FAIL** because the frozen point threshold is `>=0.10` and the observed point is `0.06944444444444449`.
- O1 recoverability/headroom point: `0.04008151917073723`
- O1 recoverability 10k cluster-bootstrap CI: `[-0.11234968338626876, 0.19036462197308052]`
- recoverability positive cells: `3/3`
- recoverability gate: **FAIL** because the frozen point threshold is `>=0.10` and the CI lower bound must be `>0`; both conditions fail.

Therefore:

- `S2_VERDICT=FAIL`
- `B2=NOT_RUN`
- `formal_science_disposition=S2_DAMAGE_OR_HEADROOM_FAILED`
- `mission_method_delta=NONE`
- `thesis_method_disposition=NONE`
- next action under the frozen sequential contract: **scientific fail-stop; do not run S3/B2 absorption or later gates**.

## Artifacts

- raw: `projects/simulation/explore/coded-decoder-feedback/artifacts/science/s2-damage-headroom/s2-raw.jsonl`
  - SHA-256: `808bbe0124ef6846eefa0dd7c39feb0f974a5cb5b1166c3dab24d0242dd8e4bb`
- summary: `projects/simulation/explore/coded-decoder-feedback/artifacts/science/s2-damage-headroom/summary.json`
  - SHA-256: `62c9b7649a4ce16b330c0f0fd9d3f3ffa6dab2f3d32da1edad625e4c34a7bb9a`
- receipt: `projects/simulation/explore/coded-decoder-feedback/artifacts/science/s2-damage-headroom/receipt.json`
  - SHA-256: `ed2b73621ddcd6320784b3d9b9fd25fe13916c7042ef1c4007ab399f516d68ca`

## Protection

- No owner, schema, common module, gate, S1 artifact, S3/S4/C1 implementation, or B2 execution was changed.
- No workload dimension was reduced.
- No stage/commit/push was performed; protected P05 logs were not touched.
