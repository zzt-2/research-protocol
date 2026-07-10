# Handoff: 阶段 2 精读两批全完成 → 阶段 2.5 方法-改进矩阵

> 来源: S007-S008 | 交接目标: 阶段 2.5 方法-改进矩阵（INVARIANT 20）+ 阶段 3 判地三轴
> 文件名: H005-stage2-complete-to-stage2.5-matrix.md
> 日期: 2026-07-10

## 到哪了（状态）

**阶段 2 精读两批（ISI + AO-DSP）全完成**，产出 `projects/simulation/literature_notes.md`（L01-L06 + 综合分析 + 7 Q# 候选 Q1-Q7 + 两子地带对比）。**不判 Go/Kill 不判地**（守 D018）。

**7 Q# 候选汇总**：
- ISI（Q1-Q4）：晴空湍流致 ISI 物理前提待证 / IRS 相干迁移 / DFE-FDE-OFDM 排序 / 深衰落跟踪
- AO-DSP（Q5-Q7）：DSP 替代 AO 波前校正 / SIC 时域迁移 / 高阶调制残余补偿
- **共同硬伤**：2019+ baseline 判据普遍 ❌ + 场景不匹配

**两子地带核心结论（诚实，守 D018 不 Kill）**：

| 子地带 | 边界 | 场景适配 | baseline 凑池 | 物理前提 |
|---|---|---|---|---|
| ISI | ✅ | ❌ Ajam PD/IRS 双重不匹配 | ❌ | ⚠ 晴空湍流致 ISI 存疑 |
| AO-DSP | A支❌排除 / B+C支✅ | ❌ B+C支全多模 | ❌ | ⚠ 多模真实但单模不适用 |

**颗粒无收倾向**：在已读材料范围内，两子地带都凑不齐 baseline + 场景不匹配。**但这不是 Go/Kill 结论**（守 D018），是阶段 2 精读的诚实观察。

## 下一步干什么

**阶段 2.5 方法-改进矩阵**（INVARIANT 20，新对话第一件事）：
1. 横向汇总 ISI + AO-DSP 每个方法的所有改进路径 + 效果到 `projects/simulation/method-improvement-matrix.md`
2. **空格=机会**：找没人做过的改进路径
3. 空格进 Q# 候选前必验证"为什么没人做"（物理不成立/没人想到/别的领域做过）
4. 标"基于已读 N 篇，未读 M 篇可能覆盖"的覆盖度诚实标注

**阶段 3 判地三轴**（矩阵后）：
1. **物理有缝轴**：ISI 晴空 GG 湍流是否真致时域 ISI？（补查湍流信道 CIR 文献——sat.1553 口径说标量衰落无时域展宽）
2. **范围内轴**：AO-DSP 单模场景有没有信号域残余补偿真问题？（多模机制不迁移）
3. **够 D005 轴**：两子地带 dB 增量够"赢传统 baseline 几 dB"吗？
4. **三轴判读后**：换子地带（OFDM-FSO? DNN?）or 颗粒无收诚实记录（守"颗粒无收好过凑数"原始目标）

## 纪律（和下一步直接相关的约束）

1. **INVARIANT 20 方法-改进矩阵**：阶段 2.5 必须横向汇总，空格=机会但要验证"为什么没人做"
2. **D018 中性提取**：全摸完排优先级，不边做矩阵边 Kill
3. **profile "警惕急于给方向性结论"**：颗粒无收倾向不是 Kill 结论，阶段 3 才判地
4. **"颗粒无收好过凑数"**（原始目标 INVARIANT）：如果跑下来产不出够硬的方向，不算失败——证明诚实判在起作用
5. **INVARIANT 6**：判据 A（baseline 真失效）判缝移全文层，本批 abstract 论文标"二手"
6. **阶段 3 前补查**：晴空 GG 湍流致时域 ISI 物理判定（sat.1553 说不建模，需查湍流信道 CIR 文献）

## 关键事实（接收方需知道）

### 两子地带都凑不齐 baseline 的根因

**ISI**：
- 星地原生 ISI Trans 仅 Ajam TCOMM 2026 单篇（PD/IM-DD + IRS 几何，双重不匹配 + paywall）
- 光纤迁移 DFE/FDE Trans 池大但全 paywall，机制同构性（光纤色散 vs 星地湍流）无法核验

**AO-DSP**：
- 信号域论文全多模架构（Li 2022 SIC MDM / Fontaine 2019 12模 / Kim 2007 波前校正）
- 单模场景适配的 AO-DSP 信号域 Trans baseline **零篇**
- Paillier 系（唯一单模星地 Trans）按载波边界排除

### 颗粒无收倾向的诚实含义

这不是"方向不行"的结论（那是阶段 3 判地 + 阶段 4 Go/Kill 的事）。是**阶段 2 精读的诚实观察**：在已选的 ISI + AO-DSP 两子地带、已读材料范围内，baseline 凑不齐 + 场景不匹配。阶段 3 判读可能：
- (A) 真没缝 → 颗粒无收诚实记录（守原始目标）
- (B) 有缝但选样错过 → 换子地带（OFDM-FSO / DNN / 其他）
- (C) 窄缝可救 → 从 7 Q# 里挑窄缝抢救

### 待补查的物理前提（阶段 3 判读前）

**晴空 GG 湍流是否致时域 ISI？**
- sat.1553 综述口径：湍流是乘性标量衰落（scintillation），不建模时域 CIR 展宽
- Ajam ISI 来自 IRS 几何（非湍流），Lee ISI 来自 cloud 多散射（非晴空）
- **需补查**：湍流信道 CIR 文献（phase screen 仿真是否产生时域展宽？多径效应？）

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 不变量段 + 当前位置（S008 两批精读完）
- [ ] 已验证至少 3 条关键事实：
  - [ ] literature_notes.md 含 ISI + AO-DSP 两段（projects/simulation/literature_notes.md）
  - [ ] Paillier 载波边界确认（读 papers/_read_notes/10.1109_jlt.2020.3003561.md "DPLL 环路传递函数针对多普勒残频"）
  - [ ] Li 2022 SIC 信号域确认（读 papers/arxiv/2208.00836/content.md L71 "separate the MIMO decoder from the phase estimation"）
- [ ] 已检查 _registry.yaml depends_on
- [ ] 已确认范围未违反"明确不含"（不回头载波同步 / 不跳框架 / 不碰已排除子地带）
- [ ] **阶段 3 判地前先补查晴空湍流致 ISI 物理前提**

## 下一轮

**阶段 2.5 方法-改进矩阵（新对话）**：
1. 读必读清单（topic-index + literature_notes 两段 + H005 本文件 + INVARIANT 20）
2. 建 method-improvement-matrix.md：横向汇总 ISI（DFE/FDE/OFDM）+ AO-DSP（SIC/MMSE/DSP-AO）每方法改进+效果
3. 空格=机会，验证"为什么没人做"
4. 矩阵产出后 → 阶段 3 判地三轴（补查湍流 CIR + 三轴判读 + 换地 or 颗粒无收）

**不在阶段 2.5 做**：不判 Go/Kill（阶段 4）/ 不建代码（阶段 5 后）
