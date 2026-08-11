# Task Brief: C1 Step 3.5 关键词矩阵补检

> 来源: S001 / D008 | 产出位置: `projects/thesis-fso/worker-logs/step-067-c1-step3_5-query-matrix.md`
> 日期: 2026-08-09

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 9
  action_class: TARGETED_SUPPLEMENT_SEARCH
  mission_checkpoint: CP009
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

在唯一证据 worktree `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2` 执行 mandatory Groundwork Step 3.5 round 1 关键词矩阵。目标是召回与 `detect/localize one within-frame phase slip → bounded segment/suffix candidate repair → decoder re-evaluation → no-op/fallback` 完整链直接相关的先行工作，不是重复证明 generic decoder-aided carrier recovery 已存在。

## 1. 纪律与边界

1. 先读 `stages/gw-supplement.md`、`tools-guide.md` §1–2、topic-index、D008 和 `projects/thesis-fso/literature_notes_coded_decoder_feedback.md`，再运行 task-control validator。
2. 文献检索优先使用项目 `tools/search` / `tools/blit`；每个 Python/搜索命令设置 `PYTHONDONTWRITEBYTECODE=1`。所有 JSON 只能写入 `search-archive/2026-08-09/`。
3. 不下载/精读全文，不改中央 owner/治理/代码，不运行实验，不 stage/commit/push，不触碰 p05。单 agent 15 分钟内收口。
4. 外部 web 仅在项目工具覆盖不足时使用；聊天不回灌 HTML。任何方法功能断言必须以 Semantic Scholar API 或 DOI/Crossref abstract 交叉验证；abstract 不支持则标 `AI推断，未验证`。

## 2. 查询矩阵

至少覆盖下列 **3 个方法变体**，每个交叉至少 **2 个 scenario/locality term**，总查询数 **≥8**，实际结果覆盖 **≥2 个真实来源**：

- decoder/code-aided cycle-slip detection or localization；
- FEC/LDPC syndrome/CRC-assisted phase-slip correction；
- segment/suffix/local phase-state reprocessing or bounded repair；
- 可加 iterative/turbo coded carrier recovery local state 作为第四变体。

scenario/locality terms 至少从以下选择两类：

- coherent optical / free-space optical / coherent FSO coded QAM/PSK；
- boundary / change point / local / segment / suffix / bounded reprocessing。

查询不能只是同义词机械替换；至少一组必须围绕 `cycle slip boundary + decoder evidence`，一组围绕 `local repair/redecode`，一组围绕 `syndrome/CRC + phase ambiguity`。

## 3. 筛选与完整链裁决

去重后给出最多 10 篇 shortlist；逐篇填：ID/title/year/venue/source、receiver-visible input、trigger、localization granularity、candidate action、decoder interaction、fallback、complexity/latency budget、output、abstract pointer、OA/fulltext status。

分类仅用：`MUST_FULLTEXT`、`SHOULD_FULLTEXT`、`STRONG_NEIGHBOR`、`BASELINE`、`IRRELEVANT`、`UNKNOWN`。标为 MUST/SHOULD 必须说明它可能命中哪一个完整链字段；不得因题名含 cycle slip/decoder 就自动晋级。

## 4. 产出与验收

- 原始/标注 JSON：`search-archive/2026-08-09/coded-decoder-c1-step3_5-qm-*.json`。
- worker log：`projects/thesis-fso/worker-logs/step-067-c1-step3_5-query-matrix.md`。

worker log 必须含完整 query/command/source receipt、≥8 查询矩阵、去重计数、≤10 shortlist 八字段表、abstract 交叉验证、round-1 新增 MUST/SHOULD 计数与下一轮新术语。

Terminal：`ROUND1_QUERY_MATRIX_COMPLETE` / `EXACT_CHAIN_CANDIDATE_FOUND` / `NO_NEW_MUST_SHOULD` / `SEARCH_EXECUTION_BLOCKED`。

聊天只回 terminal、新增 MUST/SHOULD 数、最强候选、JSON/worker-log 路径和异常；≤800 字。
