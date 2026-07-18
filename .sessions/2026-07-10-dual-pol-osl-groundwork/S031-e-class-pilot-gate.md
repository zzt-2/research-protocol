# [S031] E 类 pilot 前置检索与准入门

> 2026-07-16 | GW Step 1 + Step 4a 四判据 | DEFER

## 目标

检索 pilot-aided SOP/Jones matrix estimation 的直接先例，核查 D031 与四判据；仅在准入后实施 PROMPT-028。

## 记录

按 H013 执行 3 组主检索并扩展 2 组。事实核查后正确计数是：第一组 `e-pilot-sop-estimation.json` 由混合源返回 **10 条**，其余 4 组 arXiv 补检为 0；此前“5 组均 0”是错误陈述，现撤回。

逐条核查 10 条的题名/年份/venue/abstract/DOI，并用 Semantic Scholar 结构化检索交叉验证重点记录：2022 IEEE Network 综述（10.1109/MNET.005.2100604）明确覆盖 coherent PON enabling DSP；2018 JLT（10.1109/JLT.2017.2785341，检索记录原标 2017）含 pilot-aided 1-tap SOP estimation，但 API 无摘要；2023 JLT data-aided DSP（10.1109/JLT.2023.3243828）用 training sequence 快速收敛；**2023 JLT feed-forward FDE（10.1109/JLT.2023.3253383）直接以插入 pilot 估计信道并前馈补偿跟踪 fast SOP transient**；2024 JLT（10.1109/JLT.2023.3320905）用 pilot 连续跟踪 SOP/equalizer；2026 JLT（10.1109/JLT.2025.3640695）以共享 preamble 做 SOP tracking/adaptive polarization。原 10 条中的 2025 VAE、2026 NLI monitoring 与本机制不构成直接占点。

结论：coherent fiber/PON 中“pilot/data-aided SOP/Jones estimation + feed-forward/equalizer compensation”已有强同机制占点。FSO Gamma-Gamma/SOP lock-swap 是不同场景，可能保留应用验证价值，但当前不能证明方法增量；直接 FSO 覆盖与全文边界仍缺，故保持 DEFER。

| ID | 年份/venue/DOI 核验 | 摘要与相关性判断 |
|---|---|---|
| L001 | 2022 IEEE Network；10.1109/MNET.005.2100604 | 综述；本地 snippet 提及 pilot SOP/Jones，S2 摘要确认 coherent-PON DSP 范围，属综述证据 |
| L002 | 检索标 2017，S2 记录 2018 JLT；10.1109/JLT.2017.2785341 | pilot-aided 1-tap SOP；S2 无摘要，强邻近但需全文 |
| L003 | 2023 JLT；10.1109/JLT.2023.3243828 | training-sequence/data-aided coherent-PON DSP，强邻近 |
| L004 | 2025；venue/DOI 缺 | VAE blind demux，pilot 仅 CPR benchmark；非 E 直接占点 |
| L005 | 2025；venue/DOI 缺 | preamble/training 做 SOP/equalization；邻近，需全文 |
| L006 | 2025 IEEE TCOM；10.1109/TCOMM.2024.3522036 | pilot ML/EM/DA 估计与跟踪 ultra-fast RSOP，强占点 |
| L007 | 2023 JLT；10.1109/JLT.2023.3253383 | pilot 信道估计+feed-forward 补偿跟踪 fast SOP，最直接强占点 |
| L008 | 2026；venue/DOI 缺 | telecom pilots 联结 sensing/communication，提 SOP/equalizer training；非直接主方法 |
| L009 | 检索标 2026；venue/DOI 缺 | pilot-aided fast SOP/CMA；精确题名未被 S2 返回，相关 2024 JLT 10.1109/JLT.2023.3320905 已验证连续 pilot SOP tracking；原记录仍需全文 |
| L010 | 2026 JLT；10.1109/JLT.2026.3673676 | TS/pilot 用于 NLI monitoring，不是 SOP 补偿直接占点 |

### D031 过滤

PASS：pilot 位于 test 段，直接估计 SOP/Jones matrix 并前馈补偿，作用时刻能触及 late swap，不与训练段正交。

### 四判据

1. 问题真实：PASS。D014/D028 已验证 late SOP 驱动极化 swap。
2. 方法增量：UNRESOLVED。fiber/PON 同机制已强占点；FSO 迁移目前仅能主张场景验证价值，尚无超出既有 pilot/feed-forward 链的机制增量。
3. 可验证：PASS。D022 历史域可设计 L0、pilot 补偿、oracle-SOP、zero-comp 消融并报开销/fixed/PI。
4. 新颖性/硬撞车：UNRESOLVED。相邻 coherent-optical 同机制强占点成立；缺直接 FSO 全覆盖与关键全文，尚不能把“场景不同”升级为合法方法新颖性。

结论：2/4 与 4/4 未过，E 类 **DEFER**；不启动性能 MVE。PROMPT-028 gate 仅允许固化审计合同。否则会把 pilot 真值访问或 oracle-SOP 上界冒充 blind 方法，违反信息访问准入。

为补齐 H013 验收形式，创建并运行仅落审计元数据的 `projects/simulation/explore/cma-fade-divergence/prompt028_e_class_pilot_gate.py`；对应 `projects/simulation/results/cma-fade-divergence/prompt028_e_class_pilot_gate.json` 固化 5 个检索路径、D031/四判据、`performance_mve_run=false`、复活条件，以及 L0/pilot/oracle/no-pilot 的信息访问、双口径指标与状态生命周期合同。`performance_numbers=null`，未伪造性能结果。

### C→B→D→E 全类总结

- C：C1 在线微调 KILL；其余训练段机制受 D031 时序正交约束 defer。
- B：候选均因训练段架构无法直接触及 test late swap 而 defer。
- D：D036 历史域真实 MVE KILL（0/5 胜于 L0）。
- E：D031 通过，但检索证据链不足，四判据 2/4、4/4 unresolved，defer。

本轮没有方法层增强获得 Go；不把 defer 计作 Kill。

## 决策引用

- D037：E 类同机制强占点、FSO 迁移增量未证，四判据未准入（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是；仅 E 类 GW Step 1/准入审计，未修改 common/params.py。

## 后续

若续接 E 类，先补关键全文与直接 FSO 覆盖，证明超出既有 pilot/feed-forward 链的机制增量；只有 2/4、4/4 明确通过后才可启动 PROMPT-028 性能 MVE。gate 工件可保留。
