# Task Brief: S2 顺序门 reducer bounded repair 与正式执行

> 来源: S001 / D026 / CP015 / T131 blocker | 产出位置: `projects/thesis-fso/worker-logs/step-204-d0-s2-sequential-reducer-repair-and-run.md`
> 日期: 2026-08-11

## 0. 根因与唯一假设

根因已复现：现有 `statistics.reduce_s2` 是 S2 全联合 reducer，强制 2160 rows（B1/B2/O1 on + B1 off）；D025 的顺序门要求 B1/O1 PASS 前不得执行 B2，因此合法 B1/O1-only rows 只有 1620，full reducer 必然拒绝。`S2MethodRow` 无 NOT_EVALUATED 字段，制造 B2 占位会污染 absorption。

**唯一修复假设**：新增窄 `reduce_s2_damage_headroom`，只接受精确 1620 个既有 typed `S2MethodRow`（每 cluster 9×B1-on + 9×O1-on + 9×B1-off projections），复用 full reducer 对 damage/recoverability 的完全相同整数聚合公式，不生成 coverage/B2 字段，即可在不改科学口径下合法执行顺序门。

**否决条件**：若无法逐项证明新 reducer 的 damage/recoverability 与给 full reducer 补入任意合法 B2 rows 后对应两个字段完全一致，或需改 owner/schema/gate，则停止为 `SEQUENTIAL_GATE_INTERFACE_BLOCKER`，不得再修。

## 1. 任务

1. 保留 T131 的 expected RED（缺 `reduce_s2_damage_headroom`，1 failed/0.38s）。
2. TDD 新增最小 dataclass/reducer；exact 1620 coverage、10 seeds/3 cells/2 pol、9 fixtures、B1/O1 on + B1 off、9-to-1 off owner sharing；拒绝任何 B2 row、缺失/重复/额外 row。
3. damage/recoverability 公式逐字复用 `reduce_s2`；写 metamorphic test：把同一 B1/O1 rows 与合法 synthetic B2 rows合并给旧 full reducer，两个 reducer 的 damage/recoverability/cell counts/physical_off_computations exact equal。
4. bootstrap 仍用 owner 的 10,000 PCG64 seed-cluster percentile；不得改 gate。
5. GREEN 后继续 T131 full execution，exact 1620 raw rows；B2=`NOT_RUN`，不生成 coverage/absorption。
6. 15 分钟内 full run不完就启动 checkpointable background，回 PID/路径。
7. 不改 owner/schema/common/S1，不实现 S3/S4/C1，不 stage/commit/push。

## 2. 输出

- production：优先仅 `statistics.py` + `science.py`
- test：T131 focused S2 test file
- artifact：`artifacts/science/s2-damage-headroom/`
- report：step-204，含 RED/GREEN、full numbers/PID、两门 verdict、B2 NOT_RUN、三类 disposition、保护检查

## 3. 验收

- exact 1620 typed rows，no B2 rows
- old/new reducer damage/headroom equivalence test PASS
- damage/headroom point+CI+positive cells 可独立复算
- 任一门 FAIL 即终止，不运行 B2
