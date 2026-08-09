# Task Brief: C2 true-extrinsic soft-symbol CPR — Groundwork Step 1 检索

> 来源: S001 / D002 | 产出位置: `projects/thesis-fso/worker-logs/step-050-c2-step1-search.md`
> 日期: 2026-08-09
> 唯一文档: 执行方只需本任务书与其中列出的仓库文件

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 2
  action_class: GROUNDWORK_STEP1_SEARCH
  mission_checkpoint: CP002
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

在指定 evidence worktree 内完成 C2 路由的一轮广角 + 二轮定向 Step 1 检索与 AI 审查。目标不是证明“没人做过”，而是查清 exact-action competitor、problem-bearing conventional baseline、近期正式文献与可实现 comparator。

**候选合同**：`decoder L_post/L_apriori -> true L_ext -> on-air soft-symbol expectation/reliability -> one bounded continuous phase/CFO update -> re-demap/re-decode under matched total BP/front-end/latency budget`。

**禁止**：下载/精读全文、实现、实验、把摘要推断写成事实、把 FSO 空白写成问题、把 P08-R2 数字复活。

## 1. 必读与本地种子

- `stages/gw-search.md`
- `tools-guide.md` §1–2
- `.sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md`
- `projects/thesis-fso/worker-logs/step-048-decoder-feedback-candidate-recheck.md`
- `projects/thesis-fso/worker-logs/step-049-coded-chain-interface-readiness.md`
- `search-archive/_index/all-papers.jsonl`

本地种子必须核对但不得只靠元数据下科学结论：DOI `10.1109/access.2026.3653159`、`10.1109/iwcmc58020.2023.10182805`、`10.1109/tvt.2025.3600028` / arXiv `2309.12828`。

## 2. 查询合同

使用 `bash tools/search`，每次命令前设置 `PYTHONDONTWRITEBYTECODE=1`；`--mode academic --preset problem-driven --max-per-source 15 --top 40 --format json`，结果只能写入 `search-archive/2026-08-09/`。至少执行 3 组一轮查询，并在 AI 初筛后执行至少 2 组 C2 专属二轮查询：

1. decoder-aided / turbo carrier phase recovery + LDPC/FEC extrinsic soft symbols；
2. iterative demapping/decoding assisted synchronization + residual CFO/CPE；
3. coherent optical/FSO decoder feedback + strongest pilot/DD/iterative carrier baseline；
4. 二轮需围绕初筛中最直接 competitor 的 action、timing、information contract 与 comparator 公式重搜；不得只是改同义词。

实际结果须覆盖至少 3 个真实来源；若默认源不足 3 个，使用合规的 IEEE `tools/blit` 补充并仍写入日期目录。外部网页信息若调用，聊天不得回灌原文；每篇摘要 ≤500 词，并用 S2/DOI abstract 交叉验证功能断言。

## 3. AI 审查与提取

逐条基于 title+abstract+venue+year+citation+publication_status 写回原 JSON 的 `priority` 与 `priority_reason`。额外在报告中提取：

- exact input→action→output、decoder 信息时点、是否 true extrinsic；
- continuous phase/CFO update 还是仅 scalar calibration/list search；
- strongest conventional comparator、代码/公式可得性；
- optical/FSO transfer 是否只是场景迁移；
- 对 C2 的结论：EXACT_COLLISION / STRONG_NEIGHBOR / BASELINE / IRRELEVANT / UNKNOWN；
- 每条功能断言的 abstract/DOI/S2 pointer，abstract 不支持则标 `AI推断，未验证`。

## 4. 产出

- 原始并已标注 JSON：`search-archive/2026-08-09/coded-decoder-c2-*.json`（多文件允许，禁止根级散落）。
- 路由报告：`projects/thesis-fso/coded-decoder-feedback-groundwork/step1-c2-search-report.md`。
- worker-log：`projects/thesis-fso/worker-logs/step-050-c2-step1-search.md`。

报告必须含 query/command/source receipt、去重表、priority 分布、正式发表占比、必读候选、direct competitors、conventional baselines、两轮方向变化、C2 falsifier 判读、claim limitations 与给整合审查的 machine-readable candidate table。

## 5. 验收与 terminal

- [ ] 一轮 ≥3 query groups，二轮 ≥2 targeted groups。
- [ ] 每源请求上限/目标 ≥15，实际来源 ≥3；不足如实报。
- [ ] 每条有 AI priority/reason；未用 relevance_score 替代。
- [ ] 所有 direct-action 断言有 abstract-level 交叉验证。
- [ ] 不宣称 Step 1 总门 PASS；只裁 C2 route。

Terminal：`C2_ROUTE_SEARCH_COMPLETE` / `C2_EXACT_COLLISION_FOUND` / `C2_ROUTE_EVIDENCE_INSUFFICIENT` / `SEARCH_EXECUTION_BLOCKED`。

聊天只回 terminal、JSON/报告/worker-log 路径、5 条最承重事实与异常；总长 ≤1200 字。
