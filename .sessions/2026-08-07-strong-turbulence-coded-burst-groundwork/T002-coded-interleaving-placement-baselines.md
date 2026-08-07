# Task Brief: coded FSO interleaving/placement 与 2019+ baseline 证据

> 来源: S001 | 产出位置: `.sessions/2026-08-07-strong-turbulence-coded-burst-groundwork/R002-coded-interleaving-placement-baselines.md`
> 日期: 2026-08-07
> 唯一文档: 执行方只依赖本文件、仓库内 `search-archive/`、`papers/` 和 `tools/search`

## 0. TL;DR（执行方先读）

你在指定 evidence worktree。任务是用最多 **4 组 query** 寻找 coded FSO 在 correlated fading/burst 条件下的 fixed interleaver、channel-aware mapping、parity/bit placement、frame segmentation 以及 2019+ task-matched baseline，形成碰撞证据，不做方法裁决。

最高纪律：

1. 先复用本地索引/全文；总 query 组数不得超过 4，分别对应下列四个技术面。
2. 论文必须按真实 action 分类；仅改 depth/B 的方法标“旧 4b#1 collision”，仅改 LLR 标定标“P08 collision”，选 MCS/码率标“AMC collision”。
3. 不能把 generic RF/block-fading placement 直接当 FSO baseline；可列 adjacent，但 task-matched 必须同任务/条件/信息/输出。
4. Web 断言必须用 S2/DOI abstract 交叉验证，每篇摘要 ≤500 词；不下载/精读全文。
5. 不运行脚本/仿真，不形成 Go/Kill/METHOD_SIGNAL/方法卡。

## 1. 背景

旧方向永久排除：B=27 depth switching、自适应交织深度、GG/coded-LLR calibration、AMC/MCS。新候选若存在，action 必须能改变译码输入错误分布，并且有 2019+ task-matched comparator。

## 2. 任务详情

### 2.1 四组 query

1. `coded free-space optical interleaving correlated turbulence fading burst errors`
2. `adaptive channel-aware interleaver codeword mapping optical wireless FSO`
3. `parity bit mapping fading blocks coded modulation burst channel optical wireless`
4. `coded FSO recent LDPC polar interleaver baseline correlated fading 2019 2026`

显式输出：

- `search-archive/2026-08-07/coded-fso-correlated-interleaving.json`
- `search-archive/2026-08-07/coded-fso-channel-aware-mapping.json`
- `search-archive/2026-08-07/coded-fso-parity-placement.json`
- `search-archive/2026-08-07/coded-fso-recent-baselines.json`

### 2.2 要回答的问题

- 2019+ 哪些论文真正执行 fixed/deep interleaving、adaptive depth、channel-aware permutation、codeword scheduling、parity/bit placement 或 segmentation？
- 每篇的 deployable information、真实 action、输出和 metric 是什么？
- 是否直接处理 temporal correlation/burst duration/coherence mismatch，而非独立 GG 样本或平均 outage？
- 哪些可作为 task-matched comparator，哪些只是 adjacent mechanism？
- A/B/C 三种预卡形态分别有无先例或明显 exact collision？不为凑数制造候选。

### 2.3 产出格式

R002 必须包含：4 组 query receipt；候选论文表（identity/year/venue/DOI/status/action/information/channel lifecycle/metric/证据指针）；collision receipt（旧4b#1/P08/AMC/generic prior art）；2019+ task-matched baseline 清单与不足；三种预卡形态的证据支持度（SUPPORTED/ADJACENT/UNSUPPORTED，不做保留裁决）；Step 2 CORE 候选与获取风险。

## 3. 已知陷阱

- 标题写 adaptive interleaving，真实 action 可能仍只是 depth/B switching。
- coded FSO 论文常按 symbol 独立采样 GG，不能据此声称有跨码字相关性。
- “burst error correction”可能只是外码纠错，不代表 interleaver/placement action。
- 旧 P08-R2 的 5G NR interleaver 是工程资产，不是本候选科学 baseline。

## 4. 验收

- [ ] query ≤4，source/count/output 路径闭合。
- [ ] 至少显式判断是否存在 2 篇 2019+ task-matched baseline。
- [ ] 每篇 action/信息/生命周期/metric 分开记录。
- [ ] collision receipt 可追到 DOI/abstract/本地路径。
- [ ] 不做方法裁决、不下载精读、不运行仿真。

## 附：产出回传位置

`.sessions/2026-08-07-strong-turbulence-coded-burst-groundwork/R002-coded-interleaving-placement-baselines.md`
