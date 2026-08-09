# Task Brief: Coded decoder-feedback Step 1 独立整合与替代动作裁决

> 来源: S001 / D002 / step-050–051 | 产出位置: `projects/thesis-fso/worker-logs/step-052-step1-integrated-adjudication.md`
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

你是 fresh-context integrated reviewer。禁止新广搜、全文下载、实现或实验。基于 C1/C2 route JSON、报告和原始 concept/dead-end 证据，独立完成：

1. 两项 exact-action collision 的摘要级复核；
2. 合并去重后的 canonical Step 1 质量门；
3. strongest comparator / direct competitor 冻结；
4. 用户允许的“旧卡均不合格时最多两张 replacement sketch”审查；
5. 给出唯一 terminal 和下一合法动作。

执行与审查必须分离：不得因为 route agent 写了 `EXACT_COLLISION` 就照抄；也不得因为 Ch4 需要方法而降低动作身份门。

## 1. 必读

- `stages/gw-search.md`
- `.sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md`
- `projects/thesis-fso/worker-logs/step-048-decoder-feedback-candidate-recheck.md`
- `projects/thesis-fso/worker-logs/step-049-coded-chain-interface-readiness.md`
- `projects/thesis-fso/worker-logs/step-050-c2-step1-search.md`
- `projects/thesis-fso/worker-logs/step-051-c1-step1-search.md`
- `projects/thesis-fso/coded-decoder-feedback-groundwork/step1-c2-search-report.md`
- `projects/thesis-fso/coded-decoder-feedback-groundwork/step1-c1-search-report.md`
- `search-archive/2026-08-09/coded-decoder-c1-*.json`
- `search-archive/2026-08-09/coded-decoder-c2-*.json`
- `projects/thesis-fso/direction-lab/harvest/ch4-decoder-feedback-method-preflight.md`
- D028/D047、P05、F4-C 原始证据指针（从 step-048 下钻）

## 2. 独立复核

至少复核：

- C2：DOI `10.1109/TWC.2004.837407` 的摘要是否真的支持 `turbo decoder extrinsic LLR -> iterative ML phase estimation`，以及 2025 FCN / 2026 ACCESS 是否只是邻近还是覆盖同类反馈动作。
- C1：arXiv `2511.21340` 的 official abstract receipt 是否真的支持 `decoder extrinsic model evidence -> symmetry-derived finite candidates -> one selection`；TSP 2006 是否只凭题名过度推断。
- 每项 collision 分为 `CORE_ACTION_EXACT`、`STRONG_NEIGHBOR`、`NOT_VERIFIED`；不得声称公式/预算逐行等价，除非证据真支持。

可以用已有 JSON/local index 做复核；若承重摘要 receipt 本身缺失，允许至多 2 次官方 arXiv/DOI/S2 abstract 定点查询，仅用于核证，不扩 corpus。每篇返回摘要 ≤500 词，不抓 HTML/全文。

## 3. Integrated Step 1 质量门

合并 C1/C2 全部 annotated rows，按 DOI→arXiv→normalized title 去重，保存 `search-archive/2026-08-09/coded-decoder-step1-integrated.json`。报告实际值：

- unique ≥20；actual source families ≥3；必读 ≥5；正式发表 ≥50%；路线 ≥2；
- C1/C2 各自有 ≥2 组二轮定向检索；
- exact/strong action claim 都有 abstract-level pointer；
- 旧而承重的 direct competitor 可保持“备选”，但必须进入 Step 2 shortlist；不得为过门改 priority。

质量门 PASS 只代表 corpus 足以裁候选，不代表存在 survivor。

## 4. Replacement sketch 门（最多 2，允许为 0）

只有 C1/C2 core action 均被确认 collision 时才执行。基于已检索 direct competitors 与现有 coded-chain，检查最多两张不同动作的 replacement sketch。每张必须同时满足：

- 具体 M-C-A，不是“没有 decoder feedback”或“FSO 没人做”；
- receiver-visible input→**不同的 carrier-recovery action**→output；
- 不只是换 syndrome/extrinsic trigger、阈值、场景、一次/多次、soft-symbol mapping、公平账本或计算调度；
- 不撞 C1/C2、C3/D047 recovery、D028 rollback、F4-C relabel、P08 scalar、P05 CMA、CCISP/Ch5 scheduling；
- 指定 direct competitor、strongest conventional comparator、cheap alternative、adapter BOM、主图/消融/falsifier；
- 当前 corpus 对其至少有 problem/action evidence；否则 reject，不凭想象制造对象。

如果没有合格 replacement，输出 0；不要为了继续而制造卡。若有 1–2 张，仅标 `HYPOTHESIS_ONLY` 并要求返回 Step 1 定向检索，不得直接进 Step 2。

## 5. 产出与 terminal

- integrated JSON：`search-archive/2026-08-09/coded-decoder-step1-integrated.json`
- report：`projects/thesis-fso/coded-decoder-feedback-groundwork/step1-integrated-adjudication.md`
- worker-log：`projects/thesis-fso/worker-logs/step-052-step1-integrated-adjudication.md`

报告包含 collision adjudication、dedup/quality receipt、must-read/Step2 shortlist、replacement matrix、canonical mapping、claim limitations、master verification list。

唯一 terminal：

- `STEP1_SURVIVOR_READY_FOR_STEP2`（原卡仍有合法 survivor）；
- `STEP1_REPLACEMENT_REQUIRES_TARGETED_SEARCH`（产生 1–2 张真正不同 replacement）；
- `STEP1_NO_METHOD_ACTION_SURVIVOR`（corpus 足够且 0 replacement，映射 canonical `NO_VALID_PROBLEM` / 不建设 adapter）；
- `STEP1_EVIDENCE_INSUFFICIENT`；
- `EXECUTION_INVALID`。

硬上限 12 分钟；禁止新 broad query。聊天只回 terminal、三路径、碰撞判定、质量门数字、replacement 数量和 5 条承重事实。
