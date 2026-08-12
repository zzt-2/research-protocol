# Step 4a worker log: DSP-outage-aware multi-aperture defect smoke

## Scope

仅验证 Q001 defect；未实现候选 soft method、未运行 fair comparison。

## Chronology

- pre-test freeze commit: `cbb8a2d`
- dev: 20×18=360 pairs，6480 rows
- held-out: 5×20 seeds，100×18=1800 pairs，12600 rows
- independent verifier: PASS，critical/major/minor=`0/0/1`

## Frozen results

- G1 occurrence: `0.0311111`, CI `[0.0233333,0.0394444]`, FAIL
- G2 B0 regret: `0.00111399`, CI `[-0.00378538,0.00494708]`; outage excess `0`, FAIL
- G3 B2 regret: `0.00111399`, CI `[-0.00390701,0.00506245]`, diagnostic FAIL
- G4 AUC delta: `0.000464392`, CI `[-0.000674602,0.00169164]`, diagnostic FAIL
- terminal: `PROBLEM_ABSENT_OR_TOO_SMALL`

## Disposition

formal science disposition、mission_method_delta、thesis_method_disposition 分别为 `PROBLEM_ABSENT_OR_TOO_SMALL`、`NONE`、`NO_METHOD / NO_CH4_CONTRIBUTION`。
