# Task Brief: D0 S2 damage/headroom 独立终验

> 来源: S001 / T131–T133 | 产出位置: `projects/thesis-fso/worker-logs/step-206-d0-s2-independent-verification.md`
> 日期: 2026-08-11

## 任务

只读验证 S2 final artifacts，不修代码、不复跑物理/decoder、不运行 B2。

1. raw 正好1620 unique rows，exact seeds8150–8159×hard/mid/clean×X/Y×(9 B1-on +9 O1-on +9 B1-off projections)；无B2 row。
2. typed parse + `reduce_s2_damage_headroom` fresh复算point/cell integers/off count；独立以10 seed blocks、PCG64 seed2026081001、10000 draws复算damage/recoverability CI、invalids、positive cells与gate。
3. damage gate：point≥0.10、lower>0、positive cells≥2；recoverability同。核对summary verdict。
4. 审查 affected-CW计数为16×1024 per-CW any-error且只数affected suffix，bit errors另计；focused fresh tests。
5. hash/owner/source/checkpoint/raw一致；B2确实NOT_RUN；owner/common/schema/S1/p05/staging未越界。
6. 给 `VERDICT=PASS|FAIL|INCOMPLETE` 表示证据包是否可信；另分列 `S2_SCIENCE_VERDICT=PASS|FAIL`。即使科学FAIL，证据验证可以PASS。
7. 写step-206，15分钟硬停，不commit/stage/push。

报告必须含P0/P1/P2、独立数字、两门判据、formal_science_disposition、mission_method_delta=NONE、thesis_method_disposition=NONE、next action=SCIENCE_TERMINAL若S2 fail。
