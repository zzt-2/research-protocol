# [S008] 阶段 2 精读批次 2（AO-DSP 残余补偿）+ 两子地带对比

> 2026-07-10 | 阶段 2 精读批次 2 + 两子地带对比 | 状态：完成（AO-DSP 精读 + ISI×AO-DSP 对比，产 Q# 候选，不判 Go/Kill）
> 续接：S007（阶段 2 批次 1 ISI）

## 目标

精读 AO-DSP 残余补偿子地带（边界检查前置 → 信号域论文精读），M-C-A 提取 + Q# 候选 + 两子地带对比，**不判 Go/Kill 不判地**（守 D018 + INVARIANT 6）。

## 记录

### 1. 边界检查前置（PROMPT-002/H003/H004 最高优先级）

基于已有精读笔记 papers/_read_notes/10.1109_jlt.2020.3003561.md（载波同步 v2 阶段读）：

**Paillier 系 DSP 段余 = 载波 PLL（多普勒残频 + 残余载波相位），非信号域均衡**
- DPLL 环路传递函数针对多普勒残频 + 激光相位噪声设计，不针对湍流相位单独建模
- 分治架构：AO（光域湍流）‖ AGC（电域残余振幅）‖ DPLL（数字域多普勒残频+残余相位）
- **结论**：Paillier 2020 JLT（#34）+ Paillier 2019 ICSOS（#35）按红线排除（载波同步已完成不回头）

### 2. blit 下载尝试（用户提醒用 blit）

- **Li 2022 JLT SIC-DSP**：tools/search 找到 arXiv 2208.00836（OA）→ tools/download 成功（197 行全文）
- **Fontaine 2019 ECOC**：tools/download --doi 10.1049/cp.2019.1015 FAIL（paywall），blit IEEE 搜 "electronic wavefront" 0 命中（ECOC 是 IET 非 IEEE）
- **Kim 2007 EL**：S2 搜 0 命中 + blit IEEE 搜 0 命中（19 年老文，Electronics Letters 非 IEEE）
- **结论**：AO-DSP 信号域论文仅 Li 2022 有全文，Fontaine/Kim 靠 abstract/landscape 转述

### 3. 子 agent 精读 Li 2022 SIC-DSP（gw-read 流程）

子 agent 读 papers/arxiv/2208.00836/content.md，返回结构化提取（6 节，每声称标行号）：

**核心发现**：
- SIC 逐通道顺序解码 + 干扰消除（ỹ_k = y - Σĥ_i·s̃_i），比 MMSE 多利用自由度提升 SINR [L89-107]
- **边界判定 PASS**：carrier-asynchronous DSP 结构显式 "separate the MIMO decoder from the phase estimation, the channel estimation, and the ISI equalization" [L71]。SIC 属信号域（均衡层 IN），载波相位由独立模块处理
- **场景架构不匹配**：SIC 处理 inter-mode crosstalk（MDM 多模），依赖 N_r ≥ N_t 冗余接收通道。本场景单偏振单孔径单模 → 无 inter-mode crosstalk → SIC 无可消除对象
- 增益数据：弱湍流 SIC ~3dB penalty vs MMSE ~4.2dB；强湍流 SIC ~6.9dB vs MMSE 未达 HD-FEC [L139]。120 强湍流样本 BER 8.02×10⁻³→4.76×10⁻⁴，outage 48.3%→2.5% [L157/L161]

### 4. §7.2 主线 grep 核查（Li 2022 全 PASS）

| 核查项 | 结果 |
|---|---|
| SIC 信号域非载波域 | **PASS**（content.md L71 "separate the MIMO decoder from the phase estimation"） |
| SIC 处理 inter-mode crosstalk | **PASS**（L83 "inter-channel interference (ICI)"） |
| MDM 多模架构 | **PASS**（L11/L13 mode-division multiplexing + inter-mode crosstalk） |
| baseline MMSE 增益 | **PASS**（L139 弱湍流 3dB vs 4.2dB，强湍流 6.9dB vs 未达 HD-FEC） |

无造假。

### 5. AO-DSP 子地带 Q# 候选（3 条）

| Q# | 一句话 | 四判据初筛 |
|---|---|---|
| Q5 | DSP 替代 AO 校正波前畸变（Kim 2007 概念迁移单模 intradyne） | 矛盾❓/形态✅/baseline❌/对比❌ |
| Q6 | SIC 从多模迁移到单模+多时间采样（时域分集替代空间分集） | 矛盾❓/形态✅/baseline❌/对比❌ |
| Q7 | AO 校正后残余 piston 相位高阶调制（16-QAM）下信号域补偿 | 矛盾✅/形态✅/baseline❌/对比❌ + ⚠边界 |

共同硬伤：2019+ baseline ❌ + 场景架构不匹配（全多模，单模零适配 Trans）

### 6. 两子地带对比（ISI + AO-DSP）

| 维度 | ISI | AO-DSP |
|---|---|---|
| 边界 | ✅ | A支❌排除 / B+C支✅ |
| 场景适配 | ❌ Ajam PD/IRS 双重不匹配 | ❌ B+C支全多模 |
| baseline 凑池 | ❌ | ❌ |
| 物理前提 | ⚠ 晴空湍流致 ISI 存疑 | ⚠ 多模机制真实但单模不适用 |

**两子地带都 baseline 凑不齐 + 场景不匹配**。D004 筛选判据二选一结果：判据 A（凑池）两都❌ / 判据 B（缝潜力）Q# baseline ❌ / 判据 C（范围 in）两都⚠

### 7. 颗粒无收倾向（诚实，守"颗粒无收好过凑数"原始目标）

在已读材料范围内，两子地带都凑不齐 baseline + 场景不匹配 + Q# baseline 判据普遍 ❌。**但这不是 Go/Kill 结论**（守 D018），是阶段 2 精读的诚实观察。阶段 3 判读需回答：
1. ISI：晴空 GG 湍流是否真致时域 ISI？（物理前提判定）
2. AO-DSP：单模场景有没有信号域残余补偿的真问题？
3. 两子地带都不行 → 换其他子地带（OFDM-FSO? DNN?）还是颗粒无收？

## 决策引用

- 无新建 D###（本批只产 Q# 候选 + 初筛，不判 Go/Kill）
- 引用既有：D004（选 ISI+AO-DSP 精读）/ D018（中性提取）/ INVARIANT 6/19 / Paillier 载波边界（已有笔记）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（阶段 2 精读批次 2 + 两子地带对比，产 Q# 不判地）
- 守 ≤3 步：边界检查（复用已有笔记）→ blit下载+子agent精读 → 主线集成+核查+对比

## 后续

**阶段 2.5 方法-改进矩阵**（INVARIANT 20，新对话）：横向汇总 ISI + AO-DSP 每方法所有改进+效果，空格=机会
**阶段 3 判地三轴**（新对话）：①ISI 晴空湍流致 ISI 物理前提判定 ②AO-DSP 单模信号域残余补偿真问题 ③换子地带 or 颗粒无收

**待补查（阶段 3 前）**：
- 晴空 GG 湍流致时域 ISI 物理判定（查湍流信道 CIR 文献）
- sat.1553 是否提单模湍流致 ISI（§6 已读是 PolDemux 非 ISI）

**已知债务**：
- Fontaine 2019 ECOC 全文 paywall（仅 abstract）
- Kim 2007 EL 未下到（老文 abstract 缺失，信息靠 landscape 转述）
