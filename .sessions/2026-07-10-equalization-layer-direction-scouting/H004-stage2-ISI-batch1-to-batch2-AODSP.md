# Handoff: 阶段 2 精读批次 1（ISI）完成 → 批次 2（AO-DSP 残余补偿）

> 来源: S007 | 交接目标: 阶段 2 精读批次 2 AO-DSP 残余补偿新对话
> 文件名: H004-stage2-ISI-batch1-to-batch2-AODSP.md
> 日期: 2026-07-10

## 到哪了（状态）

**阶段 2 精读批次 1（ISI 均衡子地带）完成**，产出 `projects/simulation/literature_notes.md` ISI 段（L01-L03 + 综合分析 + 4 Q# 候选）。**不判 Go/Kill 不判地**（守 D018）。

**材料现实（诚实）**：
- TCOMM 2026 Ajam（ISI 主题论文）**paywall 仅 abstract**（降级链全试失败：无 arXiv + GLOBECOM 2024 arXiv title-mismatch 错绑 LaTeX 模板）
- 光纤 DFE/FDE 迁移 Trans（20 篇）**全 paywall 仅 abstract**
- 仅 Ajam 2022 前置论文（arXiv OA）+ sat.1553 §6（OA）有全文

**3 个核心发现（诚实，守 D018 不 Kill 只标观察）**：
1. **Ajam 场景双重不匹配**：PD/IM-DD（非相干）+ IRS 几何诱导 ISI（非直射星地）。降级参考不当主 baseline
2. **baseline 凑不齐 D-010 标准 4 篇 Trans**：星地原生仅 Ajam 1 篇（PD+paywall），光纤迁移全 paywall 机制同构性存疑
3. **晴空 GG 湍流致 ISI 物理前提存疑**：sat.1553 综述（最权威）将湍流建模为乘性标量衰落，**不建模时域 CIR 展宽**。Ajam ISI 来自 IRS 几何，Lee 来自 cloud 多散射——晴空湍流致 ISI 未被主流文献建立（**B7 模式风险：解决不存在的问题**，留阶段 3 判读）

**4 Q# 候选**（共同硬伤：2019+ baseline 判据普遍 ❌）：Q1 湍流致 ISI 物理前提待证 / Q2 IRS 相干迁移 / Q3 DFE/FDE/OFDM 排序 / Q4 深衰落跟踪鲁棒性

## 下一步干什么

**阶段 2 精读批次 2（新对话第一件事）= AO-DSP 残余补偿**：
1. **⚠ 边界检查前置（最高优先，PROMPT-002 + H003 要求）**：精读 **Paillier 2020 JLT**（#34，DOI 10.1109/JLT.2020.3003561）+ Paillier 2019 ICSOS（#35），确认 DSP 段余是**载波 PLL** 还是**信号域**。**载波域 → 按红线排除**（载波同步已完成不回头）
2. 边界检查通过后，精读 **Li 2022 JLT SIC-DSP**（#40）+ **Fontaine 2019 ECOC**（#37）+ **Kim 2007 EL**（#38 扩写溯源）
3. 同样 M-C-A + Q#（≥3）+ §7.2 主线 grep 核查 + literature_notes AO-DSP 段
4. **下载预案**：JLT/ECOC/EL 大概率 paywall，靠 abstract + sat.1553 §6 + 已落盘 _read_notes（Paillier 10.1109_jlt.2020.3003561.md 已在 papers/_read_notes/）

**两批都完成后 → 阶段 2.5 方法-改进矩阵**（INVARIANT 20）→ 阶段 3 判地三轴

## 纪律（和下一步直接相关的约束）

1. **边界检查前置**：AO-DSP 批次 2 第一步必须核验 Paillier 载波边界，避免精读一批载波域论文白做
2. **INVARIANT 19 精读分层**：Trans 必精读作 baseline 主力；Letters/会议做扩写溯源不当主 baseline
3. **D018 中性提取**：全摸完排优先级，不边精读边 Kill
4. **≥3 Q# 候选**（禁单假设）
5. **INVARIANT 7 §7.2 三硬规则**：全文真实性 / 立场不可扭曲 / 孤证就是孤证 + 主线 grep 核查
6. **INVARIANT 6**：abstract 不判缝（判据 A 移全文层），但全文 paywall 时标"二手 abstract"不硬判
7. **不碰 MDCC/偏振/OAM/ISI**（D002/D003/D004 排除，本对话只做 AO-DSP）
8. **论文全文精读必须子 agent**（AGENTS.md 强制委托，≤900s）
9. **主对话禁 WebSearch**（走 tools/search + tools/blit）

## 关键事实（接收方需知道）

### ISI 批次 1 的 3 个核心风险（影响 AO-DSP 批次 2 的判读）

1. **Ajam 场景双重不匹配**（PD/IM-DD + IRS 几何）→ ISI 子地带 baseline 池主力失效，全靠光纤迁移但 paywall
2. **baseline 凑池高风险** → D-010 标准 4 篇 Trans 在 ISI 场景凑不齐
3. **晴空湍流致 ISI 物理前提存疑** → 若不成立，ISI 子地带整个塌方（B7 模式）。**阶段 3 判读前需补查湍流信道 CIR 文献**

### AO-DSP 批次 2 精读要点

- **Paillier 2020 JLT**（#34）AO+数字 PLL，**DSP 段余很可能是载波 PLL**（sat.1553 综述口径）。精读第一步核验边界
- **Paillier 已有精读笔记**：papers/_read_notes/10.1109_jlt.2020.3003561.md（载波同步 v2 阶段已读，可复用核验载波边界）
- 信号域残余论文：Fontaine 2019 ECOC（#37 多模数字补偿）/ Kim 2007 EL（#38 电子波前）/ Li 2022 JLT（#40 SIC-DSP，跨 MDM）

### 源状况债务（影响精读下载）

- **Exa 信用耗尽 + IEEE blit 近失效 + SerpAPI 未装** → 检索靠 S2+OpenAlex
- **JLT/ECOC/EL 大概率 paywall** → 精读下载主要靠 arXiv + OA PDF + Unpaywall + 已落盘 _read_notes
- sat.1553 §6（OA 全文）作均衡器理论参考可用

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 不变量段 + 当前位置（S007 ISI 批次 1 完成）
- [ ] 已验证至少 3 条关键事实：
  - [ ] literature_notes.md ISI 段存在（projects/simulation/literature_notes.md）
  - [ ] Ajam 场景确认 PD/IM-DD（读 papers/arxiv/2108.00291/content.md L57 "intensity modulation and direct detection"）
  - [ ] sat.1553 §6 确认湍流是标量衰落非时域展宽（读 papers/doi/10.1002_sat.1553/content.md L67-73 GG 乘性衰落）
- [ ] 已检查 _registry.yaml depends_on
- [ ] 已确认范围未违反"明确不含"（不回头载波同步 / 不碰 MDCC/偏振/OAM/ISI / 不跳框架）
- [ ] **AO-DSP 精读前先核验 Paillier 载波边界**（读 papers/_read_notes/10.1109_jlt.2020.3003561.md）

## 下一轮

**阶段 2 精读批次 2（新对话）= AO-DSP 残余补偿**：
1. 读必读清单（topic-index + decisions D002/D003/D004 + literature_notes ISI 段 + H004 本文件 + gw-read.md）
2. 边界检查前置：核验 Paillier DSP 段余载波/信号域
3. 精读 Li 2022 JLT SIC + Fontaine 2019 ECOC + Kim 2007 EL
4. M-C-A + Q#（≥3）+ §7.2 核查
5. 写 literature_notes AO-DSP 段 + S008 + 批次 2 收尾 handoff（交阶段 2.5 矩阵）

**不在阶段 2 做**：不判 Go/Kill（阶段 4）/ 不判地（阶段 3）/ 不建代码（阶段 5 后）/ 不碰已排除子地带
