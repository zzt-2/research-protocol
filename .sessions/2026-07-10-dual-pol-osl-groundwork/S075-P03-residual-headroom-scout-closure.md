# [S075] P03 residual-headroom Scout closure

> 2026-07-19 | Direction Lab Scout diagnostic | 状态：A 出口，V030 独立终验 PASS

## 目标

在不进入 formal MVE/Contract/Execute、不触碰 B001–B003、不创建 B004/Queue/Registry、不训练 ML 的边界内，完成 P03/U19 source closure 恢复与最多 10-cell residual-headroom probe，并只给出预注册 A/B/C 或真实 P0 状态。

## 记录

有限 source archaeology 在一轮明确来源集合中找回历史 `_gg_time.py` 精确字节：SHA256 `92eaa6a6c92e72122a1921a0c844160bbf5b4ee7bc2527fc66da468187af9786`，来源为已知 linked worktree 的 mutable dirty 文件；P03/B001–B003 已登记 source closure 均记录该路径与 hash。该字节未直接作为 probe 依赖，而是固化为 raw Git blob `9155de058912593f487d95fb4e3aecf25ae1617c`，再由 commit `65db35bb15dd9b6da0ad05ea5835054ad4277485`、独立 patch SHA `4cd7007b...` 与混合行尾配方重建。

恢复后的 deterministic equivalence gate PASS：standard-CMA 身份为 Godard-with-z；CSI_NONE、shape/dtype/finiteness/time-boundary、oracle/future/post-hoc 拒绝均通过；历史 z-window SHA `3d99d4fef5f3749d2047816b8bc655affc207f307bafc808b6de887b88ca64f7` exact equal。旧 blocker 的 max z difference `0.21934995093323548` 保留为“不完整 committed-source candidate”的历史失败，不删除、不改写为 v3。

probe contract 冻结 seeds 11–20、10 cells、shared standard-CMA realization、CSI_NONE、calibration 128 symbols + evaluation 128 symbols；nearest-QPSK、blind complex 2×2 affine 使用相同 receiver-visible z，oracle affine 仅用于 post-hoc scoring。10/10 cells 的 nearest/blind/oracle fixed-label BER、PI-BER、fixed-label SER、PI-SER 均为 0；aggregate visible headroom=0，按预注册 zero-headroom rule coverage=1.0，触发 `P03_ANALYTIC_COVERAGE_GE_90`。

模拟 residual 并非全零：selected residual energy min/median/max=`0.008144/0.041559/0.111335`、CV=`0.703962`，2/10 cells tail mass 非零；blind affine 把跨 cell 平均模拟 residual energy从 `0.285582` 降到 `0.046682`，但没有任何 BER/SER 收益。这说明“非零 residual”不等于“可利用 decision headroom”。

两次完整运行的 6 个产物逐文件 SHA exact equal；正式 probe result SHA=`1232d1a47431f14729045c04beafe0836e531ad238f9bcb8e15462c2f7901cdd`。公共 simulator、params truth source、B001–B003 均未修改，B004 不存在。

迭代计数器：source recovery 1 轮；probe contract 1 版；scientific probe 2 次确定性重放；无参数调优、无参数域扩展。

## 决策引用

- D057：P03 在冻结 CSI_NONE hard-decision slice 触发 A 出口，停止且不训练 ML（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是。属于 D045 深耕基点—候选族—批量排跑的 Direction Lab Scout diagnostic；不是 formal MVE/Contract/Execute，未改变 S074 pilot-Jones Step3.5 的 formal 门控状态。

## 后续

V030 已由独立 verifier PASS。下一轮若继续，仅回 BatchPlan 选择既有候选族，本轮不选择或启动下一方向。
