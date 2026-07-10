# Handoff: 阶段 1.5 选地完成 → 阶段 2 精读（ISI 均衡 + AO-DSP 残余补偿）

> 来源: S006 | 交接目标: 阶段 2 精读新对话（ISI + AO-DSP 两子地带精读再筛）
> 文件名: H003-stage2-precise-read-ISI-AODSP.md
> 日期: 2026-07-10

## 已完成边界

**阶段 0-1.5 全部完成**：
- 阶段 0 流程规划（S001）+ 索引机制（S002-S003）
- 阶段 1 地勘前置（S004-S005，6 组检索，landscape 完整版 ~46 篇 + 8 子地带 + 4 死地）
- 阶段 1.5 选地（S006）：
  - **场景确认**：单偏振 intradyne 单孔径单链路星地 GG 湍流（代码核查）
  - **D002 排除 MDCC + 偏振**（架构不匹配）
  - **D003 双偏振倾向伪需求**（Toyoshima 2009 实测 DOP 99.4%，大气几乎不退偏，B7 风险）
  - **D004 选 ISI 均衡 + AO-DSP 残余补偿都进精读**

**做到哪一步**：选地完成。**下一步是阶段 2 精读，不是判 Go/Kill 不是建代码**。

## 下一步干什么

**阶段 2 精读批次 1 = ISI 均衡子地带**（新对话第一件事）：
1. 下载 + 精读 **TCOMM 2026 Ajam**（ISI in IRS-FSO，landscape #29，唯一星地 ISI Trans）—— M-C-A 提取
2. 找光纤领域 DFE/FDE 经典 Trans 迁移作 baseline（凑 D-010 标准 4 篇）—— 这是 ISI 子地带 baseline 池主力来源
3. Lee & Kavehrad 2006/2009（channel shortening+Viterbi 老孤证，#32#33）快速过
4. M-C-A 提取 + 四判据初筛 + §7.2 主线 grep 核查
5. **判据 A（baseline 真失效）留到全文层**（守 INVARIANT 6，地勘只标了 🟢🟡🔴 粗判）

**阶段 2 精读批次 2 = AO-DSP 残余补偿**（批次 1 后）：
1. **⚠ 边界检查前置（最高优先）**：精读 Paillier 2020 JLT（#34）+ Paillier 2019 ICSOS（#35），确认 DSP 残余是载波 PLL 还是信号域。**若是纯载波域 → 按红线排除**（载波同步已完成不回头）
2. 若边界检查通过，精读 Li 2022 JLT SIC-DSP（#40）+ Fontaine 2019 ECOC（#37）+ Kim 2007 EL（#38 扩写溯源）
3. 只留信号域残余补偿论文作 baseline

## 不要做什么

1. **不要精读 MDCC / 偏振均衡 / OAM-MIMO**（D002/D003 已排除：MDCC 多孔径冲突 / 偏振单偏振不匹配 + 双偏振伪需求 / OAM 死地）
2. **不要把 AO-DSP Paillier 系当均衡层 baseline 不核查边界**（DSP 段余可能是载波 PLL，精读第一步必须核验）
3. **不要用 abstract 的 🟢🟡🔴 当 Go/Kill**（INVARIANT 6，判缝移全文层）
4. **不要单假设验证**（6 次 Kill 教训，Q#-A 模式禁）—— 精读要提取多 Q# 候选
5. **不要边精读边 Kill**（profile durable + D018，全摸完排优先级）
6. **不要跳框架**（FR-22，阶段 2 精读 → 阶段 2.5 矩阵 → 阶段 3 判读 → 阶段 4 Go/No-Go，不跳）
7. **不要本对话超 3 步**（AGENTS.md，本对话已严重超载，精读务必分对话）

## 必读（新对话开始时按优先级读）

1. `.sessions/2026-07-10-equalization-layer-direction-scouting/topic-index.md` —— 20 不变量 + 当前位置（D002/D003/D004）
2. `.sessions/2026-07-10-equalization-layer-direction-scouting/decisions.md` —— **D002（场景适配）/ D003（双偏振伪需求）/ D004（选 ISI+AO-DSP）必读**
3. `projects/simulation/landscape-equalization.md` —— **ISI 主表 #29-33 / AO-DSP 主表 #34-40**
4. `.sessions/2026-07-10-equalization-layer-direction-scouting/S006-site-selection-and-scenario-screening.md` —— 选地全过程
5. `stages/gw-read.md` —— 精读流程规范（GW Step 3）
6. `papers/doi/10.1002_sat.1553/content.md` —— sat.1553 综述（已落盘，§6 偏振段 + 均衡器段，精读 baseline 参考）

## 关键事实（接收方需知道）

### 场景设定（代码核查确认，不可假设）
- **单偏振 intradyne 单孔径单链路**星地 GG 湍流
- 论文标题："星地激光通信信号处理关键技术研究"
- 用户诉求："符合标题 + 不很难做"

### ISI 子地带精读要点
- **TCOMM 2026 Ajam**（#29）是唯一星地 ISI Trans，DOI 10.1109/TCOMM.2025.3636084
- Ajam 是 IRS-FSO PD 接收（非相干？），精读要确认是否跟 intradyne 相干场景匹配
- baseline 池薄 → 光纤 DFE/FDE 迁移是主力（光纤里 DFE/FDE 是成熟大池）

### AO-DSP 子地带精读要点（边界风险）
- **Paillier 2020 JLT**（#34）AO+数字 PLL，**DSP 残余很可能是载波 PLL**（sat.1553 综述口径）
- 精读第一步：核验 Paillier DSP 残余是载波域还是信号域。**载波域 → 排除**（载波同步已完成）
- 信号域残余论文：Fontaine 2019 ECOC（#37 多模数字补偿）/ Kim 2007 EL（#38 电子波前）/ Li 2022 JLT（#40 SIC-DSP，但跨 MDM）

### 源状况债务（影响精读下载）
- Exa 信用耗尽 + IEEE blit 近失效 + SerpAPI 未装
- 精读下载主要靠 arXiv + OA PDF + Unpaywall，付费墙是常态
- TCOMM 2026 / JLT 2020 等 Trans 大概率 paywall，可能需用户机构权限

## 接口变更（代码改动）

无（精读阶段不写代码）

## 已知债务（原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| ISI/AO-DSP Trans 基线薄 | D-010 标准 4 篇 Trans baseline | 原生 Trans 各 1-2 篇 | 阶段 2 精读时从光纤领域迁移补 |
| AO-DSP Paillier 载波边界 | 不回头载波同步（红线）| 标边界警示 | 阶段 2 批次2 第一步核验 |
| Exa/IEEE blit 召回能力下降 | 检索全覆盖 | 靠 S2+OpenAlex | 精读下载用 arXiv/OA/Unpaywall |
| 本对话严重超载 | 单对话 ≤3 步 | 跑了地勘两批+筛查+验证+选地 | 阶段 2 严守分对话 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 不变量段落 + D002/D003/D004
- [ ] 已验证至少 3 条关键事实：
  - [ ] 场景 = 单偏振（读 _modulation.py:6 确认 qpsk_mod 返回 1D）
  - [ ] landscape ISI 主表 #29-33 + AO-DSP #34-40 存在
  - [ ] D003 引用 Toyoshima 2009 DOP 99.4% 数据真实（来源 Optica 出版商缓存）
- [ ] 已检查 _registry.yaml depends_on
- [ ] 已确认范围未违反"明确不含"（不回头载波同步 / 不碰 MDCC/偏振/OAM / 不跳框架）
- [ ] **AO-DSP 精读前先核验 Paillier 载波边界**

## 下一轮

**阶段 2 精读批次 1（新对话）= ISI 均衡**：
1. 读必读 6 件
2. 下载 TCOMM 2026 Ajam + 找光纤 DFE/FDE 迁移 Trans
3. 子 agent 精读（gw-read 流程）→ M-C-A 提取 + Q# 候选
4. §7.2 主线 grep 核查
5. 写 S007 + 批次 2 handoff

**不在阶段 2 做**：不判 Go/Kill（阶段 4）/ 不建代码（阶段 5 后）/ 不碰 MDCC/偏振/OAM（已排除）
