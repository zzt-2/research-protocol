# [S007] 阶段 2 精读批次 1（ISI 均衡子地带）——M-C-A 提取 + Q# 候选

> 2026-07-10 | 阶段 2 精读批次 1 | 状态：完成（ISI 子地带精读，产 Q# 候选 + 四判据初筛，不判 Go/Kill）
> 续接：S006（阶段 1.5 选地，D004 选 ISI+AO-DSP）

## 目标

精读 ISI 均衡子地带核心论文，按 gw-read 流程提取 M-C-A + 产 Q# 候选（≥3）+ 四判据初筛 + baseline 凑池评估。**不判 Go/Kill 不判地**（守 D018 + INVARIANT 6）。

## 记录

### 1. 下载现实（诚实标注）

- **TCOMM 2026 Ajam（ISI 主题论文）**：`bash tools/download --doi 10.1109/TCOMM.2025.3636084` → **FAIL all_failed（paywall）**
  - 降级链全试：无 arXiv 版（TCOMM 2026 OA=false）、GLOBECOM 2024 arXiv 2403.09365 **title-mismatch**（S2 元数据错绑到 LaTeX 模板，§7.2 核查 content.md 是"Seminar LaTeX example"非 FSO 论文）
  - **最终靠 abstract 提取**（search-archive JSON，S2+OpenAlex+seed 三重确认，abstract 含全部关键声称）
- **光纤 DFE/FDE 迁移 Trans**：`tools/search` 召回 20 篇（Falconer 2002 2432引 / Bulow 2008 108引 / Crivelli 2014 55引 / Zheng 2018 51引 等）
  - 试下 7 篇（Bulow/Zheng/Crivelli/Photonics2025/JLT2023/JLT2024/JLT2019）→ **全部 FAIL paywall**（JLT/TCOMM/OE/CommMag/Photonics 全闭源）
  - **最终靠 abstract 池 + sat.1553 §6 全文**
- **Ajam 团队 2022 前置论文**：`bash tools/download --arxiv 2108.00291` → **OK（OA 全文 650 行）**。提供 Ajam IRS-FSO 信道模型基础
- **sat.1553 §6**：已落盘全文（Open Access），光纤衍生均衡器理论参考

**材料现实**：
| 材料 | 状态 |
|---|---|
| Ajam TCOMM 2026（ISI 主题） | ⚠ abstract only（paywall） |
| Ajam 2022（信道模型前置） | ✅ 全文（arXiv OA） |
| sat.1553 §6（均衡器综述） | ✅ 全文（OA） |
| 光纤 DFE/FDE 迁移 Trans（20 篇） | ⚠ abstract only（全 paywall） |

### 2. 子 agent 精读 Ajam 2022（gw-read 流程）

子 agent 读 papers/arxiv/2108.00291/content.md，返回结构化提取（5 节，每声称标行号）：

**核心发现**：
- Ajam 2022 是 **IM/DD + OOK + PD square-law 直接检测**（[L57/L63/L13]），**非相干**
- IRS-FSO 信道模型 = Huygens-Fresnel 标量 GML（[L67-73]），h = h_a(GG湍流) × h_p(大气损耗) × h_irs(几何对准)
- **⚠ 关键：本论文无 ISI / 无时延色散 / 无 CIR**（§7.2 grep 确认全文无 "intersymbol/ISI/delay dispersion/channel impulse response"）
- 湍流是**乘性标量 GG 衰落**（功率 scintillation），**不建模时域展宽**
- QP 相位剖面比 LP 增益高达 12dB（[L478]）

### 3. 接收体制适配性核查（PROMPT-002 陷阱 1）

**确认陷阱 1**：Ajam TCOMM 2026（abstract）+ Ajam 2022（全文）双重确认 = **PD/IM-DD square-law 直接检测**，非 intradyne 相干。

场景双重不匹配：
1. **检测体制**：PD square-law（实数强度）vs intradyne 相干（复基带保留相位）—— ISI 数学结构不同构
2. **ISI 物理源**：Ajam ISI 来自 **IRS tile 光程差**（几何诱导）vs 本场景**直射星地无 IRS**

**结论**：Ajam 降级为"参考不当主 baseline"（守 D018 只标风险不 Kill）

### 4. §7.2 主线 grep 核查（3 篇全 PASS）

| 核查项 | 结果 |
|---|---|
| Ajam 2022 确认 PD/IM-DD | **PASS**（content.md L57 "intensity modulation and direct detection (IM/DD)" + L63 OOK + L13/47 photo detector） |
| Ajam 2022 确认无 ISI 讨论 | **PASS**（grep 全文无 "intersymbol/ISI/delay dispersion/channel impulse response"，仅 inter-link 空间串扰） |
| Ajam TCOMM 2026 abstract 关键声称 | **PASS**（OOK/PD/0.7ns/DFE/DCO-OFDM/10Gbps 全在 abstract 文本中） |

无造假。

### 5. Q# 候选（4 条，守 ≥3 禁单假设）

| Q# | 一句话 | 四判据初筛 |
|---|---|---|
| Q1 | 星地直射（无IRS）GG 湍流高速率是否产生可均衡时域 ISI？物理前提待证 | 矛盾❓/形态✅/baseline❌/对比✅ |
| Q2 | IRS-assisted 相干链路延迟色散 ISI（Ajam PD 版→相干版迁移） | 矛盾✅/形态✅/baseline❌/对比❌ |
| Q3 | DFE/FDE/OFDM 相干场景排序是否同 Ajam PD 场景 | 矛盾✅/形态✅/baseline❌/对比❌ |
| Q4 | 自适应均衡器深衰落跟踪鲁棒性（CMA 发散改进） | 矛盾✅/形态✅/baseline❌/对比✅ |

**共同硬伤**：2019+ baseline 判据普遍 ❌（星地 ISI 原生 Trans 仅 Ajam 单篇且 PD）

### 6. baseline 凑池可行性评估（D004 判据 A）

**❌ 凑不齐 D-010 标准 4 篇 Trans**：
- 星地原生 ISI Trans：仅 Ajam 1 篇（PD + paywall）
- 光纤迁移 DFE/FDE Trans：池大（Falconer/Bulow/Crivelli/Zheng）但**全 paywall 无全文**，机制同构性（光纤色散 vs 星地湍流）无法核验

### 7. 核心观察（守 D018，不 Kill）

**ISI 子地带在标准星地直射相干场景下物理前提存疑**：
- sat.1553 综述（最权威 OSL DSP）将湍流建模为**乘性标量衰落**（scintillation），**不建模时域 CIR 展宽**
- Ajam ISI 来自 IRS 几何（非湍流），Lee ISI 来自 cloud 多散射（非晴空）
- **晴空 GG 湍流致 ISI 的物理机制在主流文献中未被建立**——这是 B7 模式风险（解决不存在的问题），但守 D018 不 Kill，留阶段 3 判读

## 决策引用

- 无新建 D###（本批只产 Q# 候选 + 初筛，不判 Go/Kill）
- 引用既有：D004（选 ISI+AO-DSP 精读）/ D018（中性提取）/ INVARIANT 6（abstract 不判缝）/ INVARIANT 19（精读分层）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（阶段 2 精读批次 1，产 Q# 候选不判地）
- 守 ≤3 步：步骤1下载+找迁移 → 步骤2子agent精读 → 步骤3主线集成+核查+写note（H004 另算收尾）

## 后续

**阶段 2 批次 2（新对话）= AO-DSP 残余补偿**：
- ⚠ 边界检查前置：Paillier 2020 JLT DSP 段余是载波 PLL 还是信号域？载波域→排除
- 精读 Li 2022 JLT SIC + Fontaine 2019 ECOC + Kim 2007 EL（扩写溯源）
- 同样 M-C-A + Q# + §7.2 核查

**阶段 2.5（两批后）= 方法-改进矩阵**（INVARIANT 20）

**阶段 3 判读需补**：
- **晴空 GG 湍流是否致时域 ISI 的物理判定**——sat.1553 说不建模，但需查湍流信道 CIR 文献确认（本批未查）
- AO-DSP 批次 2 完成后两子地带对比判地

**已知债务**：
- TCOMM 2026 Ajam 全文 paywall 未读（DFE/OFDM 具体 BER 曲线未核验）
- 光纤迁移 baseline 全 paywall（机制同构性无法全文核验）
- 晴空湍流致 ISI 物理前提待阶段 3 补查
