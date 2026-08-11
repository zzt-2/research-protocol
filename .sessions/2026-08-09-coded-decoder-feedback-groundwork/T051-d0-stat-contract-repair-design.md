# Task Brief: D0 统计合同三项歧义的最小修复设计

> 来源: step-096 / D010 / D0 YAML | 产出位置: `projects/thesis-fso/worker-logs/step-097-d0-stat-contract-repair-design.md`
> 日期: 2026-08-10

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 11
  action_class: CONTRACT_STATIC_CHECK
  mission_checkpoint: CP011
```
<!-- RDL-TASK-CONTROL:END -->

## Hypothesis / 否决条件

- 假设：step-096 的三项 blocker 都是 machine-readable schema/estimand/cost-unit 遗漏；在不改变 population、seed、threshold、gate 或预算数字的前提下，可以用一组最小 YAML 字段唯一化。
- 否决条件：若唯一化必须改变任何科学阈值、删 gate、重分 seed、增加 test-time best-of，或不能同时满足 raw→summary 可复算与既有 counts，则判 `SCIENTIFIC_CONTRACT_REOPEN_REQUIRED`，不得给补丁草案。

## 任务

1. 完整读取 step-096、D0 YAML、step-090/091；寻找仓库内可复用的 typed raw schema/bootstrap/artifact pattern。
2. 针对 B1 raw schema、B2 cached twin、B3 S3 estimand/CI/cost，给**可直接粘贴进 YAML**的最小字段树与确切 enum/type/nullability/primary key/aggregation semantics。
3. 明确 S1 20/50 actual seed bootstrap、NumPy percentile `linear`；S2 60 physical off→540 logical projections→method rows/cost；S3 dev/test per-case RR/top1→cell→macro→seed-cluster CI 与 88-CW incremental cost。
4. 复算所有物理执行、逻辑 case、method row、CW decode 与 BP iteration 单位；区分 cached computation 和 cost ledger。
5. 给静态 verifier 断言清单和 verdict：`MINIMAL_REPAIR_READY / SCIENTIFIC_CONTRACT_REOPEN_REQUIRED / BUDGET_BLOCKER`。

## 边界

- 只写 `projects/thesis-fso/worker-logs/step-097-d0-stat-contract-repair-design.md`。
- 不改 owner/治理/源码/测试/结果；不运行 import/pytest/D0/仿真；不 web/search/download；不 commit/push；不触碰 p05。
- 12 分钟目标，15 分钟硬上限。

