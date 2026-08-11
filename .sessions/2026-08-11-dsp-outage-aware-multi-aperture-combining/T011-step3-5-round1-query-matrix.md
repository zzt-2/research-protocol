# Task Brief: Step 3.5 Round 1 query matrix

> 来源: S004 | 产出位置: `projects/thesis-fso/worker-logs/step-3-5-dsp-outage-round1-query-matrix.md`
> 日期: 2026-08-11
> 唯一文档: 本 brief + 指定仓库工具/已有 search index

## 0. TL;DR

在 worktree `D:/code/study/research-protocol/.worktrees/rdl-method-production-v2` 用 `bash tools/search` 完成 Q001 的第一轮系统 query matrix，并逐条语义筛查。

**产出**：唯一 worker log；原始 JSON 放 `search-archive/2026-08-11/step3-5-dsp-r1-*.json`。

**最高纪律**：

1. 只检索/筛查，不下载、不全文精读、不设计方法、不判最终 terminal。
2. 主张只能来自 title/abstract/metadata；abstract 不支持的标 `UNKNOWN`。
3. 必须分别统计 S2/OpenAlex 实际贡献；调用成功但 0 条不算贡献源。
4. 不把宽泛 adaptive combining、hard discard、SC/GSC、known-OSNR admission、pilot attenuation weight、2N×2 equalizer 当 Q001 exact collision。

## 1. 背景

Q001 冻结：Wang 2023 实际顺序 `per-branch FSTS FS/alignment + branch phase correction -> MRC -> shared pol-demux/FOE`；C 为 pre-MRC 支路功率与 branch-local FS/phase validity 异质；候选 action 仅 `receiver-visible branch-local validity -> bounded reliability/abstention -> combined sequence + no-valid flag`。完整 post-all-FS/CE/CPE 版本 excluded。

## 2. 任务详情

### 2.1 Query matrix

执行下列 8 个 query（4 个方法/动作变体 × optical/direct 与 robust-diversity/problem 场景），每个用 `--sources s2 openalex --mode academic --max-per-source 20 --top 40 --year-from 2000`：

1. `post DSP branch reliability lock aware combining coherent optical diversity`
2. `frame synchronization confidence branch admission multi aperture coherent receiver`
3. `phase validity cycle slip aware diversity combining branch selection`
4. `bounded abstaining MRC invalid branch outlier robust diversity combining`
5. `DSP outage aware multi aperture coherent FSO combining`
6. `reliability weighted MRC synchronization error phase error diversity receiver`
7. `robust MRC channel estimation outlier branch rejection generalized selection combining`
8. `confidence weighted coherent combining free space optical aperture branch`

输出命名 `step3-5-dsp-r1-q01.json` 至 `q08.json`。

### 2.2 去重与 AI 语义筛查

- DOI 优先、否则 normalized title 去重；报告 raw、unique、formal/unknown、source contribution。
- 每条候选亲自读 title+abstract，分类：`MUST / SHOULD / MAY / REJECT`。
- MUST/SHOULD 仅当 abstract 显示 receiver-visible reliability/confidence/lock/phase validity **实际驱动** weight/admission/abstention；仅分析 BER、仅信道幅度权重、仅选择合并泛论均不得升级。
- 对 MUST/SHOULD 抽取 provisional signature：input、branch position/order、trigger、weight/admission/abstention、no-valid flag、stateful、output、相对 Q001 的可能类别。
- 最多回传 10 篇 MUST/SHOULD；其余按 reject reason 计数。

### 2.3 输出格式

1. command/query receipt（8/8、源、raw/unique）；
2. method×scenario coverage matrix；
3. ≤10 candidate table（title/year/venue/DOI/source/abstract-supported facts/provisional signature/class）；
4. reject taxonomy；
5. Round 1 `new MUST/SHOULD` 数与建议的最小 Round 2 query（只列，不执行）。

## 3. 已知陷阱

- `reliability MRC` 常只是 LS/MMSE BER 分析；必须确认 reliability 是否进入 action。
- `adaptive combining` 常只适应 channel amplitude，不等于 DSP validity。
- `cycle slip detection` 若不连接 branch admission/weight，只是 feature neighbor。
- S2 citation/related 假阳性不能在本任务当 exact citation/action。

## 4. 验收

- [ ] 8 queries 全执行，S2/OpenAlex 实际贡献源≥2
- [ ] raw/unique/source counts 可机械复核
- [ ] 每个 MUST/SHOULD 有 abstract-supported provisional signature
- [ ] 没有下载/精读/terminal/方法设计

## 附：产出回传位置

`projects/thesis-fso/worker-logs/step-3-5-dsp-outage-round1-query-matrix.md`
