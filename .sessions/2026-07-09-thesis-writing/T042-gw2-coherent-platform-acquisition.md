# Task Brief: coherent FSO 共同平台全文获取与覆盖门

> 来源: S028 | 产出位置: `projects/thesis-fso/apsk-platform-groundwork/step2-coverage-report.md`
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

严格执行 GW Step 2：从 T039 的八篇 shortlist 中筛 8–12 篇，使用 `tools/download` / `tools/blit` / `tools/convert` 的既定三轮止损获取合法全文，逐篇核验 canonical identity、`content.md >= 50` 行和转换质量，形成覆盖报告。优先：Paillier 2020、Bernini 2022、Vieira 2023、Dong 2023、Roudas 2009、Faruk 2011、Faruk 2013、Kuschnerov 2009；已在库中的合格全文直接复用并核验，不重复下载。

## 边界

- 只做 acquire/convert/coverage，不精读方法、不写 Q#、不做 Step 3/3.5/4a。
- 不运行实验、不改仿真/Skill/controller/论文正文，不补新候选。
- 下载失败按 `gw-acquire.md` 三轮后停止并列入缺口；禁止网页全文抓取。
- 只提交本任务新增或规范更新的 `papers/**`、`papers/index.json`（若工具确有更新）和指定 coverage report；不要改 `.sessions/`。

## 验收

- ≥5 篇 qualified full text；正式/预印本身份与来源路径可核。
- 覆盖 Jones/unitary-PDL 边界、星地 CFO/相噪、大气偏振、receiver filter/skew 中至少三类；未覆盖项明确写 gap。
- 最终回报 commit、qualified/failed 数、coverage verdict 和阻塞 Step 3 的唯一缺口。
