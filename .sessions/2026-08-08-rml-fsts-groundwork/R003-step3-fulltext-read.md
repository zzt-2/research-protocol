# [R003] RML-FSTS Step 3 全文精读

> 2026-08-09 | 关联：2026-08-08-rml-fsts-groundwork / D004

## 调研问题

冻结的五篇 CORE 能否闭合全文事实提取、实验/写作对标与 canonical Q#，使 Step 3 在不前移 novelty、MVE 或 Go/No-Go 的前提下完成？

## Source preflight

- 5/5 title/DOI/path/SHA/bytes PASS；逐篇证据见 `search-archive/2026-08-09/rml-fsts-step3-read-receipt.json`。
- L04 canonical Markdown 缺 front matter，但同一冻结 `source.tar.gz!bare_jrnl.tex` 的 `\\title{}`、metadata DOI 与正文主题闭合。
- L05 shared `source.md` 与 worktree canonical adapter 均为 72,748 bytes、SHA256 `97DB13AB...4A6`；正文 H2/DOI 分别在 L5/L23。

## 五篇事实矩阵

| L# | 事实角色 | 能承重 | 不能承重 | reader |
|---|---|---|---|---|
| L01 Wang 2023 | C1/C2/C4 source FSTS | fixed `B_L`、precision/range tradeoff、低功率退化 | target crossover/failure | `worker-logs/step-3-rml-fsts-l01-reader.md` |
| L02 Enhanced 2024 | C2/C4 comparator | mixed TS、`TL` power/length threshold、MSE/BER/complexity | 星地 target defect | `...l02-reader.md` |
| L03 Morelli 2009 | C3 ceiling | multi-RX/multi-lag weighted correlation refinement | 2019+ baseline、FSO defect | `...l03-reader.md` |
| L04 Paillier 2020 | C4 physics | AO后幅相、AGC/DPLL、lock/BER penalty | FSTS/lag competitor | `...l04-reader.md` |
| L05 Yu 2023 | C3 ceiling | stepwise AC+CC、separation/range/precision | coherent-FSO defect | `...l05-reader.md` |

五篇均完成标准 16 字段、7 子表、通信参数和实验完备性；L01/L02/L04 另完成写作架构。完整条目在 literature owner、全局 read-notes 与 fresh reader logs。

## Source/target defect 边界

- **FACT**：Wang `B_L` 依赖 modulation/training length，且 fine-stage noise suppression 与 range 同时按 `B_L` 缩放；低功率 FS/FOE 会退化。Enhanced 的 `TL` 优劣阈值随 power/length 变化。
- **INFERENCE**：receiver-visible turbulence/branch/phase-reliability condition 可能改变 fixed lag 的 relative quality。
- **UNKNOWN**：星地 lag-ranking crossover、conditioned-single-lag failure、headroom、cheap comparator 胜负。
- strongest cheap alternative 继续为 dev-frozen modulation/TS/receiver-power-conditioned single-lag lookup；本轮不比较胜负。

## Baseline 与 prior-art ceiling

Wang 2023 是 target Q 的近期 M；Enhanced 2024 是 task-matched comparator。Morelli/Yu 限制“multi-lag weighted fusion / stepwise correlation”本身的主张，不能外推 target defect。Paillier 只约束 C4 transfer physics。Cheng/Dong/Electronics/OE.505931/OE.448956/Tang/WiSEE 保持直接竞品/证据债务，本轮未补件、未承重。

## 实验完备性/写作架构汇总

五篇 V/V'/U 均值为 `2.2/1.8/1.2`；共同优势是参数扫描与 bounded claim，共同盲点是 seed/CI/统计检验、公开代码与硬件复杂度不足。三篇标杆分别采用：Wang 的“TS→FS→FOE→complexity→system curves”、Enhanced 的“combined training→two tasks→simulation→limited experiment”、Paillier 的“physics→DSP interface→sanity check→real impairment→BER”。

## Canonical Q# 结果

| Q# | M | C | A | 产出形态 | 判据1 | 判据2 | 判据3 | 判据4 | 结果 | 证据状态 |
|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | Wang 2023 fixed-`B_L` FSTS | 固定 modulation/TS/power bin 内不同 receiver-visible condition | M 隐含假设同一 `B_L` 仍近似最优；若 turbulence/branch/phase reliability 改变最优 lag 或 lag ranking，fixed 设计将不足 | condition-to-lag design rule / reusable curve family | ✅ | ✅ | ✅ Wang 2023 exact recent M + Enhanced 2024 Optics Express task-matched 顶刊 comparator | ✅ MSE/BER/range/complexity | **4/4** | FACT+INFERENCE+UNKNOWN，A未由MVE证明也不要求本轮证明；Optics Express venue 口径见项目 D015/导师审查专题 authority |

Q1 通过只说明问题候选形成；A 是 M 所依赖、可能在 C 下被违反的假设，不是“问题不存在”的结论。novelty closure 属 Step 3.5，headroom/cheap comparator/oracle/MVE 属 Step 4a。

## Step 3 状态与理由

`✅ completed`：5/5 preflight、5/5全文字段与子表、五篇实验完备性、三篇写作架构、read-notes/read-log/owner/receipt 一致，且 1 条 target-relevant Q# 通过 canonical 四判据。Step 3.5 仍为 `⬜ NOT_STARTED`。

## 对决策的影响

新建 D004 记录 Step 3 completed、Q#=`1` 与下一合法动作；不建立新 terminal，不改变 object/package failure=`0/0`，不授权 Step 3.5/4a 或任何实验。
