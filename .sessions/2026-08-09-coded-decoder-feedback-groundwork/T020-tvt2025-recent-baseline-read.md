# Task Brief: TVT 2025 code-aided CFO/CPO 顶刊 baseline 全文精读

> 来源: S001 / D007 | 产出位置: `papers/_read_notes/2309.12828.md` + `projects/thesis-fso/worker-logs/step-066-tvt2025-recent-baseline-read.md`
> 日期: 2026-08-09

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 8
  action_class: FULLTEXT_READ
  mission_checkpoint: CP008
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

在证据 worktree `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2` 获取并精读 **Code-Aided CFOs and CPOs Estimation in Cooperative Satellite Communication**，正式 DOI `10.1109/TVT.2025.3600028`，arXiv `2309.12828`。任务只回答：它能否作为 Q1 判据3的 2019+ 顶刊具体 baseline，以及是否已经覆盖 local slip 完整 repair 链。

## 1. 纪律

1. 先读 `stages/gw-acquire.md`、`stages/gw-read.md`、`stages/glossary.md`、`domain-comms.md §1.1` 并运行 task-control validator。
2. 优先 `tools/download --arxiv 2309.12828`，再核 DOI/正式版 identity；title/作者/方法若预印本与 TVT 正式版 materially mismatch，必须分开说明，不能混版。
3. 全文精读 method/algorithm/experiment/conclusion；摘要不承担 criterion3 或 collision。
4. 不改中央 owner/治理/代码，不运行实验，不提交，不触碰 p05；15 分钟收口。

## 2. 必答

- code-aided evidence 的精确定义、CFO/CPO state、candidate/search/iteration 时序、global/local 粒度、decoder calls、fallback、clean behavior、复杂度与实验 baseline。
- 论文是否是 2019+ **正式顶刊**、是否包含可复现具体 M，能否承担 Q1 criterion3；只给 venue/metadata 不够，必须正文身份与算法都闭合。
- 是否检测 within-frame cycle slip boundary、只修 segment/suffix、clean no-op、failure fallback；逐项填写完整八字段签名。
- 输出 `criterion3_verdict ∈ {PASS_RECENT_TOP_JOURNAL_BASELINE, FAIL_NOT_TASK_MATCHED, UNRESOLVED}` 与 `collision_verdict ∈ {EXACT_COMPLETE_CHAIN, PARTIAL_CORE_ONLY, STRONG_NEIGHBOR, NOT_COMPARABLE, UNRESOLVED_FULLTEXT}`。

## 3. 产出

- `papers/_read_notes/2309.12828.md`
- `projects/thesis-fso/worker-logs/step-066-tvt2025-recent-baseline-read.md`

worker log 含 validator、获取/title/DOI/版本对应、正文行数、≤10条事实、criterion3/collision、缺口、耗时和保护检查。
