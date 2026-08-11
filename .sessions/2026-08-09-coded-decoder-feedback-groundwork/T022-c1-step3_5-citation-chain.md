# Task Brief: C1 Step 3.5 核心竞品前后向引文链

> 来源: S001 / D008 | 产出位置: `projects/thesis-fso/worker-logs/step-068-c1-step3_5-citation-chain.md`
> 日期: 2026-08-09

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 9
  action_class: CITATION_CHAIN_ANALYSIS
  mission_checkpoint: CP009
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

在证据 worktree 对最高引用的 C1 核心 published competitor 做一次 backward + forward citation-chain audit，筛查至少 10 篇 abstracts，寻找 global finite decoder selection 之后出现的 within-frame slip localization / local repair / bounded re-decoding 完整链。

## 1. 纪律与种子选择

1. 先读 `stages/gw-supplement.md`、`tools-guide.md` §1–2、topic-index、D008、literature owner，以及 L02/L05 read notes：`papers/_read_notes/10.1109_tsp.2006.874844.md`、`papers/_read_notes/10.1109_twc.2004.837407.md`。
2. 运行 task-control validator。用可复核 citation-count source 判定 L02 与 L05 中哪个是最高引用 core competitor；若计数不可比/并列，则选择更直接的 finite-hypothesis L02，并解释，必要时两 seed 都扫。
3. 所有项目搜索/Python命令设置 `PYTHONDONTWRITEBYTECODE=1`；receipt/JSON 只能进 `search-archive/2026-08-09/`。不改中央文件、代码，不实验，不提交，不触碰 p05；15 分钟收口。
4. web/S2 结果由你消化，不回灌 HTML；方法断言必须由 S2/DOI abstract 交叉验证，不支持则标 `AI推断，未验证`。

## 2. 引文链合同

- **Backward**：从 seed 全文 references 中筛 carrier synchronization、phase ambiguity、iterative decoding/code-aided estimation 直接前作。
- **Forward**：用 Semantic Scholar 或等价可复核来源取 citing papers，围绕 cycle slip/localization/segment repair/decoder reprocessing 筛选。
- 合计筛查 **≥10 篇有 abstract 的记录**；forward 与 backward 都必须非空，若 API/元数据确实不提供则保留失败 receipt 并用第二合法来源补。
- 去重后最多列 10 篇高相关候选；标注方向、与 seed 的关系、abstract pointer、OA/fulltext identity。

逐候选比较完整八字段：input、trigger、localization、action、decoder interaction、fallback、budget、output。只有可能命中 local boundary + bounded local action + decoder interaction 的条目才能标 `MUST_FULLTEXT`；只做全局/固定窗 code-aided CPR 的降为 neighbor/baseline。

## 3. 产出与验收

- receipts/JSON：`search-archive/2026-08-09/coded-decoder-c1-step3_5-citation-*.json`。
- worker log：`projects/thesis-fso/worker-logs/step-068-c1-step3_5-citation-chain.md`。

worker log 必须含 seed 选择证据、forward/backward receipts、≥10 abstract screening table、MUST/SHOULD 数、≤10 shortlist 八字段、未解析身份/全文债与下一轮 terms。

Terminal：`CITATION_CHAIN_COMPLETE` / `EXACT_CHAIN_CANDIDATE_FOUND` / `NO_NEW_MUST_SHOULD` / `CITATION_CHAIN_BLOCKED`。

聊天只回 terminal、seed、forward/backward/总筛查数、新增 MUST/SHOULD、最强候选和路径；≤800 字。
