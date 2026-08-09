# Task Brief: Step 1 自动镜像逐条处置与 integrated v2 重算

> 来源: S001 / D003 / T007 / CP003 | 产出位置: `projects/thesis-fso/worker-logs/step-054-step1-mirror-evidence-repair.md`
> 日期: 2026-08-09
> 唯一文档: 执行方只需本任务书与其中列出的仓库文件

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

修复 T007 唯一科学证据 P1：把未进入 T006 的 28-result 自动镜像逐条处置，连同全部 `coded-decoder-c1-*` / `coded-decoder-c2-*` route JSON 重建可追溯的 integrated v2，并重新裁决 `replacement` 与 terminal。不得为了维持 D003 而反向标注；如果镜像确实提供新 carrier-recovery action，必须如实改变结果。

## 硬边界

- 禁止任何新检索、网络请求、全文获取、Step 2、adapter、实现、实验和论文方法声称。
- 只使用现有 JSON 的 metadata/abstract、route reports/logs、integrated report 和本地 `search-archive/_index/all-papers.jsonl`；不得凭题名补写摘要没有支持的机制。
- 不覆盖原自动镜像 `search-archive/2026-08-09/code-aided-phase-ambiguity-finite-phase-hypothesis-ldpc-deco.json`。
- 对证据不足的记录标 `UNKNOWN`，不能用推断强行归入 irrelevant。
- 硬上限 12 分钟；优先先落 JSON，再写报告/日志。记录开始与结束时间。

## 必读

- `.sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md`
- `.sessions/2026-08-09-coded-decoder-feedback-groundwork/decisions.md` 的 D003
- `projects/thesis-fso/worker-logs/step-053-coded-decoder-terminal-verification.md`
- `projects/thesis-fso/coded-decoder-feedback-groundwork/step1-integrated-adjudication.md`
- `search-archive/2026-08-09/coded-decoder-step1-integrated.json`
- `search-archive/2026-08-09/code-aided-phase-ambiguity-finite-phase-hypothesis-ldpc-deco.json`
- 全部 `search-archive/2026-08-09/coded-decoder-c1-*.json` 与 `coded-decoder-c2-*.json`

## 逐条处置合同

对自动镜像全部 28 条原始记录保留原字段，并补齐：

- `priority` 与 `priority_reason`；
- `mirror_disposition`，只能为 `DUPLICATE`、`IRRELEVANT`、`CORE_ACTION_EXACT`、`STRONG_NEIGHBOR`、`BASELINE`、`UNKNOWN`；
- `relation_reason`：说明它是否以及如何涉及 coded decoder evidence、phase/CFO estimation、finite hypotheses 或 carrier-recovery action；
- `claim_ceiling`：明确摘要最多支持什么，不支持什么；
- `provenance`：原镜像路径、row index、可用 ID 和摘要来源。

重复判定按 DOI→arXiv→规范化题名；输出中保留 alias，不静默删除。保存为：

`search-archive/2026-08-09/coded-decoder-c1-r1q0-aggregate-mirror-reviewed.json`

必须报告 28/28 是否完成、与旧 integrated 的 exact overlap 数、各 disposition 计数和 `UNKNOWN` 列表。

## Integrated v2 合同

把 reviewed mirror 与全部 prefixed C1/C2 JSON 合并到：

`search-archive/2026-08-09/coded-decoder-step1-integrated.json`

至少包含：`schema_version`、完整 input path 清单、每条 provenance、hierarchical canonical key、aliases、route membership、mirror disposition、priority、published 状态、source family、collision/replacement relevance、全部 unresolved unknown，以及可复算 counts。不得只附 summary 而丢失 rows。

重新给出：

1. raw annotated、hierarchical unique、published、must-read、source families、R2 query coverage；
2. C1/C2 collision 是否仍成立；
3. 镜像中是否存在与 C1/C2/C3/D047/P08/P05/CCISP/Ch5 不同且有 corpus evidence 的 carrier-recovery action；
4. replacement 数量及逐项理由；
5. terminal：`STEP1_NO_METHOD_ACTION_SURVIVOR`、`STEP1_REPLACEMENT_REQUIRES_TARGETED_SEARCH`、`STEP1_EVIDENCE_INSUFFICIENT` 或 `EXECUTION_INVALID`。

若存在 `UNKNOWN` 且会影响 replacement=0，terminal 必须是 `STEP1_EVIDENCE_INSUFFICIENT`，不能保留 `NO_VALID_PROBLEM`。

## 产出

1. reviewed mirror JSON（新建）；
2. integrated JSON（升级为 v2）；
3. 在 `projects/thesis-fso/coded-decoder-feedback-groundwork/step1-integrated-adjudication.md` 追加 “T007 evidence repair” receipt；
4. `projects/thesis-fso/worker-logs/step-054-step1-mirror-evidence-repair.md`，含起止时间、实际命令/退出码、28/28 覆盖、重算数字、结果是否改变 D003、唯一 terminal。

聊天只回 terminal、四个路径、28 条处置计数、integrated v2 数字、replacement 数量和最多 5 条承重事实。
