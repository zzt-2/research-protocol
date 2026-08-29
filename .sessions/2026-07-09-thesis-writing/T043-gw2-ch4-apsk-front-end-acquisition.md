# Task Brief: Ch4 APSK 前端候选全文获取与覆盖门

> 来源: S028 | 产出位置: `projects/thesis-fso/apsk-front-end-groundwork/step2-coverage-report.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 2
  action_class: GROUNDWORK_ACQUIRE
  mission_checkpoint: CP002
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

严格执行 GW Step 2，为 C4-2 ring-aware semi-blind refinement 与 C4-1 scaled-unitary pilot-LS 获取 comparator/邻居全文。候选池以 T040 为准，优先 Godard 1980、Yang 2002、Ready/Gooch RDE、Xu 2013 APSK hybrid、Fatadin 2009、Kikuchi 2011；允许从 T040 JSON 中替换无法获取者，但不得扩成新方向。使用项目下载工具并按三轮止损，逐篇核验 identity、内容行数和转换质量，输出覆盖报告。

## 边界

- 只做 Step 2；不精读公式、不形成 Q#、不决定 C4-1/C4-2 Go/Kill。
- 不实现、不实验、不改仿真/Skill/controller/论文正文，不派生方法。
- 只提交本任务新增或规范更新的 `papers/**`、`papers/index.json`（若工具确有更新）和指定 coverage report；不要改 `.sessions/`。

## 验收

- ≥5 篇 qualified full text。
- 必须覆盖：CMA/MMA/RDE canonical 中至少两类；APSK 直接使用至少一篇；coherent/Jones 或 pilot/DD comparator 至少一篇。
- 单列未获取的 direct collision / main comparator，以及它会限制 C4-1 或 C4-2 哪个结论。
- 最终回报 commit、qualified/failed 数、coverage verdict 和阻塞 Step 3 的唯一缺口。
