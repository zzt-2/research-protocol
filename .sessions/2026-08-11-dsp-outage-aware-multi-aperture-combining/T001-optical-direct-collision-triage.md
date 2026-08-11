# Task Brief: 光学/FSO direct-action collision 摘要级初筛

> 来源: S001 | 产出位置: 回传主线程，不写文件
> 日期: 2026-08-11
> 唯一文档: 本任务书 + 指定本地 JSON/论文元数据锚点

## 0. TL;DR

只读搜索结果的标题、摘要和元数据，逐条识别 coherent optical/FSO 中与 DSP-outage-aware multi-aperture combining 最接近的 direct competitor。

最高纪律：不联网、不下载、不全文精读、不实现、不仿真；Johst defect evidence 与 method novelty 分开；只做 Step 1 语义裁决。

## 1. 背景

候选动作是 receiver-visible DSP confidence → soft reliability shrinkage/abstention → robust combining。固定 SNR threshold discard/SC/GSC 已知是 comparator，不得称方法。

## 2. 任务详情

### 2.1 要回答的问题

1. 2019+ 光学/FSO 中是否存在 input/trigger/action/output 与上述 soft multi-source DSP-validity weighting 完整一致的 exact action。
2. Johst 2024、Wang 2023、Geisler 2016 和最近 2019+ direct competitor 的 identity/provenance。
3. 逐条将有意义候选分为 `DEFECT_EVIDENCE / HARD_COMPARATOR / SOFT_DIRECT / STRONG_NEIGHBOR / IRRELEVANT / UNKNOWN`。

### 2.2 执行方式

读取 `search-archive/2026-08-11/dsp-outage-multi-aperture-q1.json` 至 `q6.json`，以及用户已核实锚点的标题/元数据行；不得扩展检索。

### 2.3 产出格式

- 候选表：title/year/venue/DOI-or-URL/source_api/semantic class/理由。
- 最近 direct competitor 完整动作签名比较。
- exact collision：YES/NO/UNRESOLVED，仅限摘要证据。
- 质量风险与必读建议（至少 5 篇候选中的光学部分）。

## 3. 已知陷阱

- adaptive combining 不自动等于 DSP-validity weighting。
- phase alignment/estimator-changing 不自动等于 post-DSP branch admission。
- 搜索网页镜像不能替代正式论文 identity。

## 4. 验收

- [ ] 每个保留候选都有语义理由而非 relevance score。
- [ ] 问题证据、traditional comparator、potential extension 分开。
- [ ] collision 措辞不越过摘要级证据。

## 附：产出回传位置

直接回传当前主线程，限 1500 中文字。
