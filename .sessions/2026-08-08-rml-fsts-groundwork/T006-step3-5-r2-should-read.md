# Task Brief: Step 3.5 R2 三篇新增建议读排除审计

> 来源: S003 | 产出位置: `projects/thesis-fso/worker-logs/step-3-5-rml-r2-should-read.md`
> 日期: 2026-08-09
> 唯一文档: 执行方只需本 T、目标 worktree 与 T003 receipt/raw

## 0. TL;DR（执行方先读）

你在 `D:/code/study/research-protocol/.worktrees/rdl-method-production-v2`。
**你的任务**：对 R1 新增 3 篇建议读做合法获取、identity 与必要全文动作审计，确认它们是否只是 estimator architecture adjacent，或是否隐藏 condition→lag/`B_L`/window action。

1. `10.1016/J.OPTCOM.2024.130981` — short-time-spectrum coarse FOE
2. `10.1109/ICAIT66450.2025.11353316` — low-complexity robust coherent scheme
3. `10.1109/JLT.2021.3063251` — joint OSNR/FO spectrum correlations

**产出**：worker-log + `search-archive/2026-08-09/rml-fsts-step3-5-r2-should-read-receipt.json`；qualified 全文才写 canonical read-note。

**最高纪律**：
1. abstract/metadata 只能初筛；动作终判必须有全文行号。全文不可得时标 blocker，不臆造。
2. 实测项目下载通道；可用官方 DOI/API/作者或机构合法副本。PDF 转换必须 `tools/convert`。
3. exact action=receiver-visible condition → lag/`B_L`/correlation-distance selection 或 condition-aware multi-lag weighting；spectrum/STFT/TS/OSNR estimator 本身不等于 exact。
4. 明确判 dev-frozen modulation/TS/power-conditioned single-lag lookup 是否被实现或实质吸收。
5. 不进入 Step 4a、不比较数值胜负、不设计方法、不改 p05/pyc/current views。

## 1. 背景（了解即可，不要对照评价）

Q1 与证据边界见 `search-archive/2026-08-09/rml-fsts-step3-5-search-citation-receipt.json`。R1 把这三篇列为 should-read，仅因标题/abstract 显示 FOE/spectrum/robustness 邻接；现在要关闭是否存在 exact action 的债务。

## 2. 任务详情

逐篇记录 title/DOI/year/source/path/SHA/bytes；全文提取 method action、information source、decision granularity、lag/window/block 参数、fixed/adaptive、condition inputs、online/offline、comparators，并裁为 exact / generic multi-lag / offline optimization / cheap lookup equivalent / architecture adjacent。每条承重结论附正文行号。

### 产出格式（强制）

1. `## Acquisition/identity table`
2. `## Fulltext action evidence`
3. `## Collision classification`
4. `## R2 disposition`：3 篇 should-read 是否关闭、残余 blocker
5. `## Files changed and boundaries`

Receipt 字段同 T005：status、attempts、source/path/SHA/bytes、action fields、classification、exact collision/cheap lookup boolean-or-unknown。

## 3. 已知陷阱

- JLT 2021 的“spectrum correlations”可能是按频谱位移估 FO/OSNR，不是 time-lag selector。
- short-time spectrum 的 window 是 STFT architecture 参数，不自动等于 FSTS lag/`B_L` action。
- “robust”与“low complexity”不是 condition-aware。

## 4. 验收

- [ ] 3/3 identity 与实际通道可复核。
- [ ] qualified 项有正文动作证据；不可得项不伪终判。
- [ ] cheap lookup 单列，无越界修改。

## 附：产出回传位置

- `projects/thesis-fso/worker-logs/step-3-5-rml-r2-should-read.md`
- `search-archive/2026-08-09/rml-fsts-step3-5-r2-should-read-receipt.json`
