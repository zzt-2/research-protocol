# Task Brief: D0 合同到测试、统计与批次架构映射

> 来源: D010 / V004 / H003 / D0 YAML | 产出位置: `projects/thesis-fso/worker-logs/step-096-d0-contract-test-stat-map.md`
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

## 目标

只读把 D0 YAML 的 S1–S4、统计、raw-row、seed 与预算合同映射成最小模块/测试/批次计划，独立查找数量、estimand、CI、分母和资源成本矛盾。不得重审已被 step-091 接受的设计优劣，只检查可执行性和接口完备性。

## 必读

- `projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml`
- `projects/thesis-fso/coded-decoder-feedback-groundwork/step4a-a0-preflight.md`
- `projects/thesis-fso/worker-logs/step-090-c1-a0-contract-v3-verifier.md`
- `projects/thesis-fso/worker-logs/step-091-c1-a0-step090-narrow-verifier.md`
- `projects/simulation/DESIGN-modular-split.md`
- `projects/simulation/tests/INTEGRATION_PLAN.md`
- 现有 `common/_experiment.py`、`tests/test_experiment_json_encoding.py` 与 P08-R2 run/verify 的结果 schema/统计实现

## 必答

1. 从 YAML 逐字段生成实现矩阵：owner field → module/function → unit test → S1/S2/S3/S4 consumer → artifact field。
2. 复算 12 population cells、S1 240→600 frames/1200 pol trajectories、S2 60×9+60、S3 540 cases/88 CW decodes/47,520、S4 60；指出任何 count ambiguity。
3. 给 10,000 次 PCG64 seed-cluster percentile bootstrap 的纯函数接口、NA/zero denominator/9500/0.05/双 terminal 处理和 equal-cell macro 规则。
4. 给 raw-row schema validator、seed disjointness、all-strata conjunct、no pooling、artifact atomic write/hash/source receipt 的测试清单。
5. 估算最重单元与 batch 划分，确保每个执行 agent ≤15 分钟；给可以提前静态/小样本 fail-fast 的闸门，但不得删减任何科学 gate。
6. 建议最少文件树与 TDD task 拆分；标注接口依赖和可并行/不可并行关系。
7. verdict=`EXECUTABLE_AS_FROZEN / CONTRACT_AMBIGUITY / BUDGET_BLOCKER`，发现问题须给最小修订，不直接改 owner。

## 约束与产出

- 只写 `projects/thesis-fso/worker-logs/step-096-d0-contract-test-stat-map.md`。
- 不修改任何既有文件，不创建源码/测试/结果，不运行 D0、仿真、pytest/import probe。
- 不使用 web/search/download，不 commit/push，不触碰 p05。
- 12 分钟目标，15 分钟硬上限。

