# [S010] N1 进 Groundwork §4a 维度 B 判定——CONDITIONAL GO（门控解除≠§B PASS 验证，#3 幅度需 MVE 闭合）

> 2026-06-17 续 6 | 阶段: N1 Groundwork §4a 维度 B | 状态: §B 判定 CONDITIONAL GO（非纯 PASS，强湍流幅度需 §D MVE 闭合）
> 来源: S008 汇总后用户选 N1 进 §B | 框架: gw-feasibility.md §4a 维度 B（空白零假设检查）
> 注: 原拟编号 S009，与对话甲 A3 §A0/A'/A 的 S009 冲突，改 S010

## 目标

执行 N1 Groundwork §4a 维度 B（新颖性-可行性解耦 + 空白零假设检查）。S008 判定互锁三章"取决于 N1 §B"——本轮闭合此变量。按 §B [MUST]：列出 ≥3 个空白存在的结构/技术原因逐一反驳，任一致命则降级。本轮**只做 §B（文献层预测），不做 §D MVE（实证验证属下一阶段）**。

## 记录

### 前置：§4a 框架适配性诊断

**关键发现：gw-feasibility.md §A0/A'/A 是 ML 方法中心化**（MDP 非平凡性 / ML 问题结构适配 / DL 结构优势 / DRL 先验对照），**N1 = 离线静态 PCS（确定性优化，非 ML）**，字面套用会误判 Kill。

映射方案（本轮适用，§A0/A'/A 的非 ML 完整映射留 §B 通过后补）：
- A0-2（ML 擅长特性）→ "问题是否需要非均匀分布设计"（是：湍流 SNR 非平稳，均匀 QAM 次优）
- A0-3（跨域 ML 先例）→ "≥2 篇同类非均匀分布设计在时变信道成功"（Tian 2021 + Elzanaty 2020 = 2 篇）
- A0-4（MDP 非平凡）→ "优化问题是否平凡"（不平凡：MB 参数搜索，Tian 用 PSO）
- A0-6（先验覆盖）→ uniform QAM 是先验，PS 已证 +1.3dB → uniform 非 ≥90% 最优
- **§B 空白零假设检查不需映射，直接适用**（非 ML 方法也可结构冗余）

### §B 空白零假设检查（5 候选原因，从 R007 4 限制 + 缺口性质导出）

| # | 空白存在原因（结构/技术性）| 反驳/降级 | 致命? |
|---|---|---|---|
| 1 | **低 SNR（=强湍流）gain 坍缩**：PS 需"分布整形空间"，极低 SNR 下噪声主导，任意输入分布趋同 → gain 趋零，N1 目标域（强湍流=低 SNR）结构上无效 | **方向上被反驳**：Tian 2021 结论原话"PS has a larger gain in the low SNR than that in the high SNR"——机制是高 SNR 下 capacity-achieving 分布趋均匀（gain 必趋零），低 SNR 反而 gain 大。**但幅度未确认**：正文直述的低 SNR AIR gain 仅 0.3-0.4 dB（<0.5dB 阈值），1.3-1.5dB SER/BER gain 在未隔离湍流强度（image-only 图）| **非致命**（方向反驳，幅度 AMBIGUOUS 需 MVE）|
| 2 | **PS gain 被 CPE 相位噪声吸收**（A3 边界问题）：相干 FSO 联合幅度闪烁+相位噪声，若 CPE（A3 领域）处理主导损伤，PS 幅度优化冗余（类比 nfv-sfc-vne SFC 被 action masking 吸收）| **被反驳**：正交物理量。A3 处理*相位*（残余相位闪烁+线宽，前馈导频），N1 处理*幅度/符号概率分布*（闪烁决定的每符号比特）。相位恢复不决定符号概率。Tian 2021 把 CPE 视为给定，在其上测 PS 幅度 gain。不被吸收 | **非致命** |
| 3 | **强吸引子**：uniform QAM 接近最优（A0-6 先验覆盖 ≥90%），PS 无空间 | **被实测证伪**：Tian 2021 PS 比 uniform 16-QAM +1.3 dB（post-FEC BER @1e-2）。固定 BER 下 1.3 dB SNR gain = uniform QAM 距最优有非平凡 gap。uniform 非 ≥90% 强吸引子 | **非致命** |
| 4 | **仅光纤 PCS**：FSO（湍流非高斯）使 PCS 不适用（MB 分布假设 AWGN）| **被反驳且对 N1 有利**：多个 FSO-specific 论文已存在（Tian 2021 相干 FSO GG / Deng 2026 相干 FSO GG+实验 / Elzanaty 2020 IM/DD FSO）。非仅光纤。AWGN-MB 不匹配*部分成立*——但 Tian 用 PSO 启发式优化非高斯信道 PMF，这*正是 N1 增量*（Elzanaty blind 离线 CDF 设计 vs Tian PSO 全搜索）| **非致命** |
| 5 | **单源可复现性**（R007 #4）：1.3dB 仅来自长春光机所 Wu Zhiyong 组 | **部分缓解**：Deng 2026（同组延续）+ Elzanaty 2020 IM/DD 1-2.5dB（独立组，不同检测但同物理基础幅度一致）。但无独立组相干 FSO 复现确认 1.3dB | **非致命**（真不确定性，需 MVE 复现）|

### §B 判定：CONDITIONAL GO

**0/5 原因致命**（§B 框架"任一致命则降级"未触发）。但**原因 1 幅度 AMBIGUOUS 是真实的**：正文唯一可直读的低 SNR（≈强湍流）gain 是 0.3-0.4 dB AIR，<0.5dB N1 阈值；1.3-1.5dB SER/BER gain 存在但在未隔离湍流的 image-only 图，无法确认为强湍流。

按 §4a 决策表对号：
- **不是 Go**（A0 通过+A'/A/B 无致命+MVE 通过）——MVE 未做
- **是 Conditional Go**（A0 通过+A'/A/B 无致命+MVE 部分通过"有退化但有解释和改善路径"——这里"部分通过"对应文献层 AMBIGUOUS，需 MVE 实证闭合幅度）

**§B 层面：N1 结构上可行（无致命原因），但强湍流幅度须 §D MVE 闭合**。这正是 §B 设计意图（维度 B=文献预测，维度 D=实证验证）。

### 关键诚实区分（重申 S008）

- **D005 门控解除** = "gain 数据存不存在"（答：存在，Tian 1.3dB）—— R007 已闭合
- **§4a 维度 B 判定** = "做了会不会更好 + 空白是否有结构原因"——本轮闭合，结论 CONDITIONAL GO
- **§4a 维度 D MVE** = "强湍流下 gain 幅度能否 ≥0.5dB 实证"——**未做，下一阶段**
- **§4a 维度 A0/A'/A**（非 ML 映射版）= "方法-问题适配/竞争维度/结构优势"——本轮只做映射诊断，完整执行留 §B 通过后下一轮

这三者层层递进，**不能跳步**（S002 跳步 dead end 教训）。

### 对互锁三章判定的影响

S008 判定"互锁取决于 N1 §B"。本轮 §B = CONDITIONAL GO（非纯 PASS）：
- **不是"互锁已成立"**——N1 §B 有 AMBIGUOUS 条件，需 MVE 闭合
- **不是"互锁已破产"**——N1 无致命结构原因，方向可行，只是幅度待验
- **精确表述**：互锁三章基础**从"取决于 N1 §B"细化为"取决于 N1 §D MVE（强湍流幅度）"**。地板（A3+2.2）仍不变。**重申 S004 教训原话：互锁是结果非前提——本轮 §B CONDITIONAL GO 只是"前提条件比 S004 时更充分"，不是"互锁已验证"，绝不锁叙事。**

## 决策引用

- D005：N1 门控解除（前置已闭合，本轮在其上做 §B）
- S008：互锁判定（本轮细化"取决于 §B"→"取决于 §D MVE"）
- gw-feasibility.md §4a 维度 B：空白零假设检查 [MUST] + §4a 决策表（Conditional Go 定义）
- **无新决策**（§B CONDITIONAL GO 是 §4a 决策表的既有分支，非新方向决策。若后续 §D MVE FAIL 才触发 D006 级降级决策）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。§4a 维度 B 是 D001 后续阶段链 Groundwork Step 4a 的明文必做项（gw-feasibility.md L107-120）。属原始目标"系统性扫描找方向"的可行性预判深化。未进 §D MVE（实证验证属下一阶段），未改仿真代码/开题报告，未碰 MVE/Contract/Execute
- 范围变更：无新增

## 后续

### N1 下一步（优先级排序）

1. **§4a 维度 D MVE**（关键路径）：验证"N1 强湍流（σ²_R>1）下 PS gain ≥0.5dB"假设。最小实例 = Gamma-Gamma 信道 + 16-QAM + 离线 MB 设计（Elzanaty blind 范式），vs uniform QAM，扫 σ²_R。pass/fail 预定义：强湍流区 SER/post-FEC BER gain ≥0.5dB。**这是闭合互锁三章的最后变量**
2. **§4a 维度 A0/A'/A**（非 ML 完整映射，可与 MVE 并行）：A0-1 性能间隙量化 / A' 竞争维度矩阵 / A 结构优势（vs Tian PSO 增量）
3. A3 §A（并行，已就绪）

### 不要做

- ❌ 把 §B CONDITIONAL GO 当 §B 纯 PASS（幅度 AMBIGUOUS，需 MVE）
- ❌ 锁定"互锁三章已成立"（N1 §D MVE 未过，S004 教训）
- ❌ 跳过 §D MVE 直接进 Contract（FR-11~15 + S002 跳步 dead end）
- ❌ 机械套用 ML 框架做 N1 §A0（会误判 Kill，本轮已诊断需非 ML 映射）

### 本轮已达单对话步骤上限（AGENTS.md 3 步规则）

本轮已做：H005 汇总(S008) + N1 §B 框架适配诊断 + §B 空白零假设检查 + §B 判定(S009) = 4 步。**§D MVE 应新开对话执行**（MVE 涉及子 agent 跑脚本+返回结果数字，独立工作量）。
