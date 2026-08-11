# Task Brief: RF 传统动作与 receiver-visible validity 特征初筛

> 来源: S001 | 产出位置: 回传主线程，不写文件
> 日期: 2026-08-11
> 唯一文档: 本任务书 + 指定本地搜索 JSON

## 0. TL;DR

只读标题、摘要与元数据，识别 robust MRC under estimation error/outlier、hybrid SC/MRC、GSC 中哪些是 task-matched cheap alternative，哪些只是邻接先例，并核查可见 validity 特征。

最高纪律：不联网、不下载、不全文精读、不实现、不仿真；不借 decoder/FEC flag 重开 coded C1；不因廉价替代存在而想象式 Kill。

## 1. 背景

目标系统是 post-DSP multi-aperture coherent FSO combining。候选特征包括 pilot-LS residual、frame-sync peak margin、CPE coherence/cycle-slip metric、可选 decoder/FEC flag。

## 2. 任务详情

### 2.1 要回答的问题

1. Hard branch admission/SC/GSC 的最强传统 comparator 动作是什么。
2. Reliability-weighted/robust MRC 是否有直接的 soft shrinkage/action 先例；与目标任务是 exact、task-matched cheap alternative 还是 strong neighbor。
3. 上述四类 receiver-visible feature 中，哪些在搜索摘要的一手文献中被实际使用，哪些只是合理候选但未被当前证据支持。
4. 是否有 temporal/hysteretic admission 的明确时序物理前提。

### 2.2 执行方式

读取 `search-archive/2026-08-11/dsp-outage-multi-aperture-q1.json` 至 `q6.json`。逐条语义初筛，不按 relevance score 代替判断。

### 2.3 产出格式

- 候选表：title/year/venue/identity/source_api/class/action/why.
- 两路线对照：A hard comparator；B soft potential extension；可选 C temporal。
- features evidence 表：USED / CANDIDATE_ONLY / ABSENT。
- collision/relevance 风险与至少 2 篇 RF/传统必读建议。

## 3. 已知陷阱

- channel-estimation error 性能分析不等于改变合并权重。
- generalized selection 的固定 top-L/threshold action 是 comparator，不是 potential extension。
- GNSS cycle-slip 和非通信 outlier 文献通常只是 irrelevant。

## 4. 验收

- [ ] 保留候选逐条给 semantic class 和动作理由。
- [ ] cheap alternative 与 potential extension 分开。
- [ ] 未被当前摘要支持的 feature 明确标 CANDIDATE_ONLY。

## 附：产出回传位置

直接回传当前主线程，限 1500 中文字。
