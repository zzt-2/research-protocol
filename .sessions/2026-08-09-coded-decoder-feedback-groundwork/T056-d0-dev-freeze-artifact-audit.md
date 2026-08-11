# Task Brief: D0 BPS/B2 dev-freeze artifact 与 estimand 窄审

> 来源: D0 v2 candidate / step-095–100 | 产出位置: `projects/thesis-fso/worker-logs/step-102-d0-dev-freeze-artifact-audit.md`
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

- 假设：v2 candidate 已足以从持久 artifact 独立复算 (a) 每 tuple 的 BPS pair、(b) 每 tuple 的 `(p_s,sigma_e2)`、(c) 最终唯一 B2 tuple；clean/controlled、cell/pol、sentinel与 net-goodput 权重均唯一，test path不可能 refit。
- 否决条件：若 required artifacts未列出 dev raw/freeze、net goodput的 delivered-bit定义不唯一、clean/controlled或target/sentinel权重不唯一、HMM aggregate不足以复算 grid winner、或两份合法实现可冻结不同参数，判 `DEV_FREEZE_CONTRACT_AMBIGUITY`。

## 任务

1. 完整读取 v2 YAML、asset report、step-095/096/097/099/100及相关 A0 sections；只审 dev freeze，不重审 scientific gates。
2. 逐字段做 owner→implementation→test→consumer→artifact 映射：common BPS grid、B2 statistic pair、B2 tuple。
3. 判断现有四张 typed table/computation ledger/required files 是否足以 raw→freeze exact recompute；列出缺失的最小 typed tables、PK、fields、invariants及 freeze JSON。
4. 独立冻结建议（只设计，不改 owner）：
   - delivered information bits / total transmitted symbols / net-goodput 的唯一公式；
   - clean与controlled各自使用哪些 polarization rows，sentinel是否进入 objective；
   - 12 cells、两 strata与 pol 的 aggregation顺序；
   - HMM grid可用 lossless chunk aggregate还是必须逐 trajectory raw，及 exact fields；
   - BPS/B2 tie-break所需 error字段。
5. 检查这些补充是否改变 seed/tuple/grid/threshold/gate/test-time best-of或预算暴露；给 `NO_SCIENTIFIC_REOPEN / SCIENTIFIC_REOPEN_REQUIRED`。
6. verdict=`DEV_FREEZE_ARTIFACTS_COMPLETE / MINIMAL_ADDITIVE_REPAIR_REQUIRED / SCIENTIFIC_REOPEN_REQUIRED / HARD_BLOCKER`；若需修复，给 owner-ready YAML 字段树。
7. 复核 candidate owner初末SHA、p05 4/4、staging；本任务只写 step-102。

## 边界

- 只写 `projects/thesis-fso/worker-logs/step-102-d0-dev-freeze-artifact-audit.md`。
- 只读；允许 parse/hash/算术，禁止 import项目、pytest、D0/仿真/benchmark、web/search/download、owner/源码/治理修改、commit/push、p05触碰。
- 10 分钟目标，15 分钟硬上限。

