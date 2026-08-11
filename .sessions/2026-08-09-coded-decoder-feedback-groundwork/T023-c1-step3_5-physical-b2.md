# Task Brief: C1 Step 3.5 coherent-optical/FSO 物理 occurrence 与 strongest B2

> 来源: S001 / D008 | 产出位置: `projects/thesis-fso/worker-logs/step-069-c1-step3_5-physical-b2.md`
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

补齐 Q1 条件 C 的物理证据与 Step 4a strongest cheap/conventional B2 候选：查 coherent optical / coherent FSO coded receiver 中 cycle slip、phase jump/piecewise ambiguity 的发生机制、模型与可引用参数，同时查 pilot/BPS/DD/FEC-assisted 的最强传统吸收方案。只做文献补检与候选排序，不把物理存在直接改写成 decoder-local repair 可行。

## 1. 纪律与边界

1. 先读 `stages/gw-supplement.md`、`stages/gw-feasibility.md` 的 A0/维度A输入要求、`domain-comms.md` 载波恢复相关段、`tools-guide.md` §1–2、topic-index、D008、literature owner。
2. 运行 task-control validator；项目搜索/Python命令设置 `PYTHONDONTWRITEBYTECODE=1`，JSON 只进 `search-archive/2026-08-09/`。
3. 至少使用 2 个真实来源。主通道用 `tools/search` / `tools/blit`；必要 web 由你消化且不回灌 HTML。所有功能/参数断言以 S2/DOI abstract 交叉验证；参数若只来自正文线索则标 `FULLTEXT_REQUIRED`。
4. 不下载/精读全文，不改中央 owner/治理/代码，不实验，不 stage/commit/push，不触碰 p05；15 分钟收口。

## 2. 必答问题

### A. 物理 occurrence/model

- coherent optical 与 coherent FSO 中 cycle slip / phase jump / phase ambiguity 的直接成因：laser phase noise/linewidth、low SNR/fade、decision error propagation、pilot spacing 或 estimator loss of lock；区分有文献事实与推断。
- 常见建模粒度：symbol-level phase noise、discrete ±`2π/M` symmetry jump、piecewise-constant phase offset、slip rate/burst/window/boundary；记录可引用数值、调制、码型、SNR/linewidth/normalized linewidth 与来源。
- 哪些参数足以形成一个不依赖 truth 的 Step 4a stress slice；哪些必须全文核实，不得拍参数。

### B. strongest B2 与 complete-chain candidates

- blind phase search / pilot-aided CPR / differential coding / hard-DD or soft-DD PLL / FEC-assisted slip correction 中，哪一个是任务匹配且同信息可实现的 strongest conventional B2；说明选择理由、输入、动作、预算和 failure mode。
- 查找是否已有 `detect/localize slip → segment/suffix correction → FEC/decoder re-evaluation → fallback` 的 exact/near-exact complete chain。
- 最多给 10 篇优先候选，标 `MUST_FULLTEXT` / `SHOULD_FULLTEXT` / `PHYSICAL_SOURCE` / `B2_BASELINE` / `NEIGHBOR` / `IRRELEVANT`，并给 OA/全文可得性。

## 3. 产出与验收

- 原始/标注 JSON：`search-archive/2026-08-09/coded-decoder-c1-step3_5-physical-b2-*.json`。
- worker log：`projects/thesis-fso/worker-logs/step-069-c1-step3_5-physical-b2.md`。

worker log 必须含 query/command/source receipts、物理事实/参数表、B2 完整八字段、≤10 shortlist、abstract crosscheck、MUST/SHOULD/OA 数与 Step 4a 可用/不可用参数边界。

Terminal：`PHYSICAL_B2_SEARCH_COMPLETE` / `EXACT_CHAIN_CANDIDATE_FOUND` / `PHYSICAL_EVIDENCE_INSUFFICIENT` / `SEARCH_EXECUTION_BLOCKED`。

聊天只回 terminal、物理来源数、MUST/SHOULD 数、provisional strongest B2、最强 exact-chain candidate 与路径；≤800 字。
