# Step 045 — 2A region-calibration authority reconciliation

> date: 2026-08-07 | task: T009 | authority: D037 / CP020 / epoch 33

## 任务边界

只执行 P01/P02/T004 authority reconciliation。没有修改 CCISP、`common/`、`params.py` 或正式论文正文；
没有重开 cand_rank/T004/P1/C3/AMC/coded-burst，也没有运行新 held-out。

## 执行记录

1. 完整恢复 system control、指定 D/T、inventory、P01/P02 logs/artifacts、T004 immutable commit 与
   thesis-lessons；新建 D037、CP020、S018、T009 并通过 task-control guard。
2. 以测试先行方式实现 deterministic recompute；直接遍历 P01/P02 raw rows，并从 commit
   `1140134e89e8b0571274944cb44471ab6403481f` 读取 T004 dev evidence。
3. caller-level 审计确认 P02 decide 无 region 参数、weak slice 使用 truth label 选择评分对象、实际动作只有
   一个全局 `ref_snr_db=11`；六项语义门仅 truth-not-in-decide 一项 PASS。
4. 语义门在 sim-preflight 前失败，故按 T009 停止 bounded confirmation。生成 reconciliation、主表、
   Ch4 不升格包与可编辑流程图。

## 关键事实

- P01：dev `0–9` / held-out `30–49`；恢复 4/5 harm cells；15 个 nominal-safety cells 中
  `weak@9` 是唯一达到 `-0.3 dB` material-degradation 门的 cell（1/15）。
- P02：dev `50–59` / held-out `60–70 ∪ 81–99`；互斥，但 30-seed 集合含观察首批结果后的 10-seed
  追加。weakretune-adapter `+0.45387 dB`，seed-cluster CI `[+0.43404,+0.47370]`；
  cand_rank-weakretune `-0.09609 dB`，seed-cluster CI `[-0.10275,-0.08942]`。
- T004 dev：B2 `+0.30846 dB`，M `+0.26750 dB`，M 低 `0.04096 dB`；pre-test gate `REJECT`，
  held-out artifacts 不存在。

## 产出

- `projects/simulation/results/2a_region_calibration_authority_reconciliation/`
- `projects/thesis-fso/direction-lab/harvest/region-calibrated-ccisp-authority-package.md`
- `projects/simulation/figures/ccisp_region_calibration_authority_reconciliation.{svg,png}`

## Terminal

`SUPPORTING_ONLY`。P01 adapter 与 P02 conventional tuning boundary 可保留；region-calibrated Ch4 方法不成立。
