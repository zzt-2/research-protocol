# Task Brief: 低仰角强湍流与时间相关 burst 物理证据

> 来源: S001 | 产出位置: `.sessions/2026-08-07-strong-turbulence-coded-burst-groundwork/R001-physical-and-temporal-evidence.md`
> 日期: 2026-08-07
> 唯一文档: 执行方只依赖本文件、仓库内 `search-archive/`、`papers/` 和 `tools/search`

## 0. TL;DR（执行方先读）

你在 `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`。任务是用最多 **2 组 query** 判断：低仰角星地 FSO 是否有一手物理依据支持合法强湍流/GG/闪烁参数，以及 temporal correlation/coherence/burst span 是否可能接近固定 interleaver/codeword span。

产出一份只含事实、来源分级和未决项的 R001；不要做方法裁决。

最高纪律：

1. 先复用本地索引/全文，再调用 `bash tools/search`；总 query 组数不得超过 2。
2. 严格区分外场测量、链路预算/物理推导、仿真设计参数、人为 stress 参数；不得把仿真 `α/β` 冒充真实 occurrence。
3. 功能/贡献断言若来自 Web，必须用 S2/DOI abstract 交叉验证；每篇摘要 ≤500 词。主产物必须给本地 JSON/全文路径或 DOI。
4. 不下载/精读全文，不运行仿真，不改 `common/`、`params.py`、旧结果、Skill 或 `p05_run*.log`。
5. 不形成 Go/Kill/METHOD_SIGNAL；只回答证据是否足以支撑 Step 1 承重门。

## 1. 背景

旧 4b#1 永久事实：LEO 中弱湍流下 `Lburst=60–428`，B=27 容量约 810，0/15 仰角超容，自适应-vs-static BER 上界 0 dB。用户仅授权更换物理条件 C 为“一手证据支持的低仰角强湍流/outage 切片”，不授权任意极端参数。

## 2. 任务详情

### 2.1 问题

- 目标星地/卫星 FSO 在合法低仰角条件下，有哪些一手测量或可追溯物理推导支持强湍流、GG、闪烁指数、Rytov variance、coherence time 或 fade duration？
- 这些参数是否明确绑定仰角、路径、地面站/大气条件，而非仅作 simulation stress？
- temporal correlation/burst span 能否量化到 symbols/ms/codewords，并与约 810-symbol 固定 span 比较？
- 证据是否足以区分可恢复 burst 与整个 coherence block outage？

### 2.2 执行方式

1. `rg` 检索 `search-archive/_index/all-papers.jsonl`、`search-archive/**`、`papers/**/content.md` 中的 low elevation/strong turbulence/Gamma-Gamma/correlation/coherence/fade duration/burst error。
2. 只在缺口存在时执行两组：
   - Q1 `satellite space-ground FSO low elevation strong turbulence Gamma-Gamma field measurement scintillation`
   - Q2 `satellite optical link temporal correlation coherence time fade duration burst error turbulence`
3. 每组显式输出：
   - `search-archive/2026-08-07/strong-turbulence-low-elevation.json`
   - `search-archive/2026-08-07/strong-turbulence-temporal-burst.json`
4. 对承重来源核 identity/DOI/year/venue/abstract；能读本地全文时只抽取相关段落和行号，不做全篇精读。

### 2.3 产出格式

R001 必须包含：检索 receipt（2 组 query、source/count/输出路径）；来源分级表；每个参数的数值、单位、目标场景、证据类型、原文/abstract 指针；physical-support gate 的 PASS/FAIL/UNKNOWN；temporal-span gate 的 PASS/FAIL/UNKNOWN；不可恢复 outage 风险；候选 CORE 清单；未决/失败获取清单。结论不得超出 abstract/相关段落。

## 3. 已知陷阱

- “low elevation”与“strong turbulence”在同一论文中出现不等于参数由该场景实测。
- Gamma-Gamma `α/β` 常被人为设为 weak/moderate/strong，必须标 simulation/stress。
- coherence time、fade duration、burst length 不可互换；换算必须列数据率/符号率假设，否则标不可比较。
- outage 概率上升不等于 interleaving 可修复。

## 4. 验收

- [ ] query ≤2，路径合规，列 source/count。
- [ ] 每个承重数值都有 DOI/本地路径/行号或 abstract 指针。
- [ ] 四类证据分清，仿真参数未冒充 occurrence。
- [ ] 给出与 810-symbol span 的可比较性或明确 UNKNOWN。
- [ ] 无方法裁决、无仿真、无越界改动。

## 附：产出回传位置

`.sessions/2026-08-07-strong-turbulence-coded-burst-groundwork/R001-physical-and-temporal-evidence.md`
