# Task Brief: Coded decoder-feedback Step 1 terminal 独立终验

> 来源: S001 / D003 / CP003 | 产出位置: `projects/thesis-fso/worker-logs/step-053-coded-decoder-terminal-verification.md`
> 日期: 2026-08-09

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 3
  action_class: VERIFY
  mission_checkpoint: CP003
```
<!-- RDL-TASK-CONTROL:END -->

## 目标

Fresh-context 验证 `STEP1_NO_METHOD_ACTION_SURVIVOR / NO_VALID_PROBLEM` 是否由可复算 evidence 支撑，并检查治理、范围、protected files 与下游冻结。不得新检索、全文、实现、实验或改变 scientific disposition。

## 必读

- 本专题 `topic-index.md`、`S001`、`decisions.md`、`mission-log.md`
- `projects/thesis-fso/master-state.md` coded decoder-feedback 控制段
- step-047–052 worker logs
- C1/C2 route reports、integrated report 与 integrated JSON
- route JSON 中承重 C1/C2 entries
- D028/D047/P05/F4-C 原始 pointers（只核边界是否被扩大）

## 验证项

1. JSON 可解析；65 annotated rows、46 hierarchical unique、39 published、6 must-read、7 sources、R2=2/2 可复算；解释 IDC 2007 长/短题名合并。
2. C2 receipt 支持 `extrinsic LLR→iterative ML phase estimation`；C1 official arXiv receipt 支持 `extrinsic model evidence→finite candidates→one selection`；TSP 2006 只作 strong neighbor。
3. replacement=0 的排除矩阵没有把 trigger、场景、mapping、ledger 或 scheduling 冒充新 action，也没有过度扩大 D028/D047/P05/F4-C。
4. `NO_VALID_PROBLEM` 是本专题 action-survivor terminal，不声称领域不存在问题、B2 已解决或 testbed 不可建。
5. topic/master/decision/mission 一致；Step 2/adapter 禁止；P08 ceilings 保持。
6. 没有 source/adapter/scientific artifact 改动；四个 `p05_run*.log` 未修改/暂存；五个 litsearch pyc 噪声不得纳入提交。

输出 P0/P1/P2 findings（无则 0/0/0）、逐项 PASS/FAIL、可执行修复、唯一 verdict=`PASS`/`FAIL`。硬上限 8 分钟；只写 step-053 worker-log，聊天 ≤800 字。
