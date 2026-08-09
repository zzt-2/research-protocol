# Task Brief: Step 3.5 本地证据与 exact-action 预筛

> 来源: S003 | 产出位置: `projects/thesis-fso/worker-logs/step-3-5-rml-local-evidence-audit.md`
> 日期: 2026-08-09
> 唯一文档: 执行方只需本 T 与目标 worktree 内现有仓库材料

## 0. TL;DR（执行方先读）

你在 `D:/code/study/research-protocol/.worktrees/rdl-method-production-v2`。Step 3 已完成，本轮只做 mandatory Step 3.5 文献竞争闭包。
**你的任务**：只读盘点现有 all-papers 索引、search receipts、papers/、既有 read-notes/worker-logs，筛出 2019+ 可能占用 Q1 exact action 或廉价等价动作的条目，并审计 Cheng/两篇 Optica/Tang/WiSEE 的本地证据状态。
**产出**：一份结构化本地证据审计，写入上述 worker-log；不要改其他文件。

**最高纪律**：
1. 不联网、不运行新搜索、不把 abstract/metadata 冒充全文。
2. exact action 固定为 receiver-visible condition → 在线/分区选择 lag、`B_L` 或 correlation distance；输出 condition-to-lag rule/curve family。
3. 必须区分 exact collision、generic multi-lag、offline parameter optimization、conditioned single-lag lookup 等价、architecture adjacent。
4. Tang/WiSEE 只报告 provenance 矛盾与可修证据，未修前不得承重。
5. 不进入 Step 4a，不讨论数值胜负，不设计 adaptive lag；不得触碰四个 `p05_run*.log`。

## 1. 背景（了解即可，不要对照评价）

Q1：M=Wang 2023 fixed-`B_L` FSTS two-stage FOE；C=固定 modulation/TS length/receiver-power bin 内不同 receiver-visible turbulence/branch/phase-reliability condition；A=若 condition 改变最优 lag/ranking，fixed design 不足。FACT 只有 fixed `B_L`、precision/range tradeoff、modulation/power/TS dependence、低功率退化；target crossover/failure/headroom 均 UNKNOWN。最强廉价替代是 dev-frozen modulation/TS/power-conditioned single-lag lookup。

## 2. 任务详情

### 2.1 要回答的问题

- 本地现有条目中，哪些实现了 adaptive/variable lag、multi-lag weighting、correlation-distance/window selection、condition-aware controller？
- 哪些只做 generic prior art、offline tuning 或相邻 CPR/combining？
- Cheng 2020、OE.505931、OE.448956、Tang 2022、WiSEE 2024 当前 identity/content/provenance 到哪一层？
- Wang 2023 与 Enhanced 2024 的 references 中有哪些直接种子可进入 citation-chain 子任务？

### 2.2 执行方式

用 `rg` 优先查 `search-archive/_index/all-papers.jsonl`、`search-archive/2026-08-08/`、`papers/`、`projects/thesis-fso/worker-logs/` 和本专题材料。每条承重陈述附文件+行号或 JSON key。不得逐篇全文重读；本任务只是本地预筛。

### 2.3 产出格式（强制）

1. `## 扫描范围与确定性命中数`
2. `## 五项债务状态表`：identity、metadata、content path、SHA/bytes（有则给）、provenance blocker
3. `## 候选动作分类表`：title/DOI/year/evidence level/action/information source/granularity/classification/exact? / evidence pointer
4. `## Wang/Enhanced backward seeds`
5. `## 对关键词矩阵的去重建议`（只指出现有覆盖，不新增方法论）
6. `## 结论边界`：只给 candidate list，不做 Step 3.5 terminal

## 3. 已知陷阱

- `all-papers` abstract 可以支持召回，不能支持全文动作终判。
- OE.505931 是 diversity combining+CPR，OE.448956 是 branch block phase correction；它们可能是 condition source 邻近，不自动等于 lag controller。
- 既有 oversampled-sync logs 中的 Cheng/Tang 角色属于另一问题，不能直接移植终判。

## 4. 验收

- [ ] 五项直接债务全部有确定性状态。
- [ ] 每个候选有 evidence level 与动作分类。
- [ ] 无 novelty/Go/Step4a 声称，无 p05 变更。

## 附：产出回传位置

`projects/thesis-fso/worker-logs/step-3-5-rml-local-evidence-audit.md`
