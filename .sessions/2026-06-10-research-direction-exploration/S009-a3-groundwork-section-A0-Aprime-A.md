# [S009] A3 §4a 维度 A0/A'/A 分析通过（BC-4 cycle slip 新增）+ 执行顺序纠正

> 2026-06-16 续 6 | 阶段: Groundwork §4a 维度 A0/A'/A | 状态: 三维度通过，进维度 D（MVE）前的最后一道分析门已过
> 来源: S006 §B PASS 后续 / 用户"继续" | 方法: §4a 维度 A0（DSP 适配版）+ A' + A 纯分析
> 注: 原拟 S007，与对话乙（N1）的 S007 冲突，改 S009（S008 已被 H005 汇总占用）

## 目标

承接 S006 A3 §B 判定 PASS，推进 §4a 剩余维度。**纠正上轮"下一步"写的错误执行顺序**：gw-feasibility.md L24 明确执行顺序 = **A0 → A' → A/B → D**（不是 A→A'→A0）。本轮完成 A0（DSP 适配版）/A'/A 三个纯分析维度，判定能否进维度 D（MVE）。

## 记录

### 执行顺序纠正（重要，防下个对话重走）

S006"后续"段写的下一步顺序是"A→A'→A0→D"，**错了**。gw-feasibility.md L24 原文："执行顺序：A0 → A' → A/B → D。A0 不通过则直接 Kill 或 Pivot，不进 MVE。" 理由：A0 是纯分析预检，在 MVE 前拦截"方法不匹配问题"的死胡同，必须最先做。本轮已纠正，按 A0→A'→A 顺序执行。

### A0 适配性裁定（用户确认）

A0 六项检查是为 ML/DRL 方法写的（MDP 非平凡性/跨域 ML 先例/GNN+RL 范式对齐等）。A3 是 DSP 算法（导频前馈 CPE），用户确认走 **DSP 适配版**：跳过 ML 专属项（A0-2/A0-3/A0-4），严格执行三项方法论无关的通用检查（A0-1 性能间隙 + A0-5 负面证据 + A0-6 先验覆盖）。跳过原因记于本 S007，不另起决策。

### 维度 A0（DSP 适配版）— 三项全 PASS

**A0-1 性能间隙（FR-02 源类型强制标注）—— PASS**

当前最强非导频方法 = Paillier 2020 AGC+DPLL。A3 改进目标就是它。

| 间隙 | 数值 | FR-02 源类型 |
|---|---|---|
| BER penalty（AGC+DPLL 相对无湍流理想） | **2.3 dB** | **[实证]** Paillier `content.md:200` σ²_I=0.684 条件下图表直接测量 |
| critical SNR 抬升（PLL 失锁门槛被 deep fade 抬高） | **+5 dB** | **[实证]** Paillier `content.md:190` |
| pilot 相对 VV+差分（OSL deep-fade 场景 4） | **+1 dB** | **[实证]** Valjus 2025 综述 `10.1002_sat.1553` 笔记 L48 |

性能间隙 ≥2.3dB，远超 A0-1 的 15% 门槛（2.3dB 在 BER 10⁻³ 量级约 1-2 个数量级 BER 改善空间）。全 [实证] 源类型，可作 Go 核心论据。

**A0-5 负面证据搜索 —— PASS，但新增 BC-4**

子agent 跑 2 个 `-neg` query + WebSearch + 复用 Phase B 7 搜索，~70 去重命中。结论三层：
1. **无论文报告"pilot 前馈 CPE 在湍流 FSO 下失败"**——Valjus 2025 综述反把 pilot 列为深衰落首选。真空性成立
2. **有论文报告"blind（无 pilot）前馈 CPE 在湍流 WOC 下 cycle slip 失效"**（Wang 2019 IEEE 8793073，摘要直证）——这是 A3 要**替代**的对象，不构成对 A3 负面证据
3. **【关键新发现】通用前馈 CPE 失效边界**（Ip&Kahn 2009 JLT; Li 2019 Appl. Sci.）：**low SNR + 深衰落 → phase unwrap cycle slip**。**此失效对 pilot 前馈 CPE 同样适用**——deep fade 使 pilot SNR 跌破 unwrap 阈值则 cycle slip。Li 2019 的 PAPU（pilot-aided phase unwrap，0.78% pilot）救回 3dB POST-FEC OSNR

判定 PASS（未触发致命，无针对 A3 路径的失败报告）。但第 3 条是**新的失效边界**，进 D006 为 **BC-4**（详见 D006）。

**【关键认知】修正 BC-2**：原 BC-2 说"VV 失效不迁移到导频 CPE"——这只对 VV 的 **M-次方块边界盲估计**失效机制成立。phase unwrap cycle slip 是**前馈 CPE 族的共享失效边界**，pilot CPE 不豁免。A3 不能只是"换个 CPE"，**必须含 cycle slip 应对设计（PAPU 类）**——这反而强化 A3 非平凡性（不是 trivial 重做）。

**A0-6 先验覆盖检查（FR-01）—— PASS**

主指标 = 相位估计方差（等价 BER/OSNR penalty）。非导频简单方法覆盖度：

| 非导频简单方法 | 主指标覆盖度 | 说明 |
|---|---|---|
| AGC+DPLL（Paillier） | **未覆盖**——有 2.3dB gap | 当前最强，仍离无损伤上界 2.3dB |
| VV 盲 CPE | **未覆盖且部分失效**——deep fade BER 10-13%→27-30%（TL-18） | 比 AGC+DPLL 更差 |
| AO（自适应光学） | **未覆盖**——只补活塞相位，不补幅度闪烁 | 对 A3 攻的损伤无关 |
| Deng 2026 residual carrier | 不算先验——是**同族竞争方法**（另一种 pilot 类思路） | 应在维度 A/Contract baseline 比，非 FR-01 |

主指标无任何非导频简单法达 ≥90% 最优。FR-01 不触发致命。

**A0 适配版总结**：三项全 PASS。A0-2/A0-3/A0-4（ML 专属）按 DSP 适配版裁定跳过（A3 非 ML）。A0 通过，继续 A'。

### 维度 A'（竞争维度分解 [FR-05]）—— PASS

A3 拆三独立优化维度：

| 维度 | 先验覆盖度 | ML/DSP 改善空间 | A3 预期增量 |
|---|---|---|---|
| **相位估计精度（deep fade 鲁棒性）** | **低**（AGC+DPLL 2.3dB gap / VV 失效） | **≥10%**（2.3dB） | **核心创新维度** |
| 频谱效率（pilot 开销） | 高（连续 tone 开销固定） | <5% | 不声称创新（pilot 固有代价） |
| 复杂度/实时性 | 中（前馈 CPE 复杂度可控） | <5% | 不声称创新 |

创新声称**只建在维度 1**（先验覆盖度低 + 改善空间 ≥5%），符合 A' 第 3 项。不是"所有维度先验覆盖度都高"。**纪律约束**：A3 论文不可声称频谱效率/复杂度维度的创新（这两维是 pilot 固有代价）。

### 维度 A（结构优势论证）—— 4/5 通过，A-4 为已知债务留 MVE

**A-1 结构性优势（相对最简 baseline AGC+DPLL）**：DPLL 闭环依赖环路稳定性 + 有 critical SNR 失锁门槛（Paillier `content.md:190` +5dB）；A3 前馈导频 CPE 开环，**无环路稳定性约束、无失锁门槛**。deep fade 瞬态 DPLL 可能失锁，前馈导频持续提供相位参考不依赖 re-lock。**结构性优势，非参数调优**。

**A-2 简单方法信息损失的条件与量**：deep fade 期间（σ²_I=0.684），AGC 放大信号也放大噪声（`content.md:177`）→ 瞬态 SNR 不改善 → DPLL 误差检测器信噪比下降 → 相位估计方差暴增/失锁。损失 = critical SNR 抬升 5dB（`content.md:190`）+ BER penalty 2.3dB（`content.md:200`）。前馈导频用已知参考做相干积分提升有效 SNR，**不受误差检测器信噪比制约**。

**A-3 文献证据**：Paillier 2020 + Valjus 2025 + Phase B 子agent 检索（无直接先例但 PASC 证 pilot tone 抗湍流成立）。

**A-4 [FR-03] 增强基线对比 = 已知债务**：裸 baseline = AGC+DPLL。**增强 baseline** 须含 BC-1（PASC）+ BC-3（residual carrier）。A3 相对 PASC 增量 = "数字前馈 CPE 可做更精细相位估计（unwrap/多阶），不依赖 O/E 混频硬件对准"；相对 residual carrier 增量 = "专用 pilot tone 不受数据调制干扰"。**但这些增量是推断，Phase B 子agent 标 abstract 推断未验证**。FR-03 要求"增强后差距 <5% 则结构优势声称不成立"——当前差距未实证，**A-4 不能本轮闭环，留维度 D MVE**（BC-1/BC-3 实证就在这）。非致命（方向清晰），显式记为债。

**A-5 [FR-08] 范式对齐**：A3 非 ML，FR-08（GNN+RL 范式）不适用。DSP 成功范式 = pilot-aided CPE 是光纤相干通信成熟范式（Xu 2019 证 RF pilot tone→CPE 机制）。A3 把成熟范式迁移到 FSO 湍流，**方法-问题匹配有光纤成功先例支撑**。

**维度 A 判定**：A-1/2/3/5 通过，A-4 已知债务（留 MVE）。无致命信号（结构优势方向清晰，FR-03 债务有明确闭合计划）。

### §4a 维度进度小结

| 维度 | 状态 | 关键产出 |
|---|---|---|
| A0（DSP 适配版） | ✅ PASS | 性能间隙 2.3dB [实证] / 负面证据无针对 A3 失败（新增 BC-4 cycle slip）/ FR-01 不触发 |
| A' | ✅ PASS | 创新只建在维度 1（相位估计精度），频谱效率/复杂度不声称创新 |
| A | ✅ 4/5 通过（A-4 债务留 MVE） | 结构优势 = 开环无失锁 vs 闭环 critical SNR；范式 = 光纤 pilot-aided CPE 迁移 |
| B | ✅ PASS（S006） | 空白零假设检查 4 原因全反驳 |
| D（MVE） | ⏳ 待做 | **A0/A'/A/B 全过后最后一道**。含 BC-2/BC-4（deep fade 下 cycle slip 不触发验证）+ FR-11 架构摘要 + FR-14 先验对照 + FR-15 目标基线对照 |

**当前判定**：A0/A'/A/B 四维度全过（A-4 是债务非致命），**可进维度 D（MVE）**。但 MVE 是实验维度，须过 TL-25 起飞检查单 + 设计假设，是下一个对话的事（本对话已超步数上限）。

## 决策引用

- **D006（续 6 更新）**：新增 BC-4（前馈 CPE 通用 cycle slip 失效边界，pilot CPE 同样适用，A3 须含 PAPU 类应对，MVE 验证）；修正 BC-2 措辞（"不迁移"仅指 VV M-次方块边界，phase unwrap cycle slip 是共享边界不豁免）；标题/小节"3 条"→"4 条"
- D003：参照（B1 §B FAIL 正面对照，A3 四维度全过证明框架有效）
- D001：执行（§4a 维度 D MVE 是下一步）
- D004：参照（互锁三章主轴，A3 这条腿 A0/A'/A/B 全过，接近 §4a Go）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。§4a 维度 A0/A'/A 是 S006 §B PASS 后的 Groundwork 前置分析，属"系统性扫描找方向"原始目标 + D001 后续阶段链。纯分析，未碰 MVE/Contract/Execute，未改仿真代码
- **范围变更**：无新增。A0 适配版（跳过 ML 专属项）是执行细节非范围扩展

## 后续

### A3 下一步 = 维度 D（MVE）—— 新对话

MVE 是实验维度，须：
1. **过 TL-25 起飞检查单**（MVE 前必读 thesis-lessons.md）
2. **设计 MVE 假设**：验证 pilot 前馈 CPE（含 PAPU 类 cycle slip 应对）在 deep fade 下相位估计方差 < AGC+DPLL，且 cycle slip 不触发（BC-4）
3. **FR-11 架构摘要**必填（动作空间/决策粒度/对比范式/奖励语义——A3 是 DSP 非RL，语义对应：处理粒度/对比范式/性能指标/先验对照）
4. **FR-14 先验对照**：MVE 必含 AGC+DPLL（最强简单先验），pass 须 pilot CPE > AGC+DPLL（非仅 > 无处理）
5. **FR-15 目标基线对照**：MVE 必含 PASC 路线（BC-1）作贡献目标基线（贡献声称要超越的对手）
6. **BC-2/BC-4 实证**：deep fade 下 VV 失效 vs pilot CPE 不失效（BC-2）+ cycle slip 不触发（BC-4）
7. **时间预算 ≤1 天**，子 agent 执行

**未到 Contract/Execute**。MVE 通过后才进 Step 5（baseline 选定）→ 4b → Step 6/7。

### 不做（Dead Ends，承 S006 + 新增）

- ❌ 在 A-4（FR-03 增强基线）未 MVE 实证前宣称"结构优势确认"（A-4 是债务，方向清晰但未闭环）
- ❌ 把 A0 的 ML 专属项机械套到 A3（用户已确认 DSP 适配版）
- ❌ 跳过 BC-4（cycle slip 失效边界）直接进 MVE——MVE 必须验证 cycle slip 不触发
- ❌ 把 A3 论文声称建在频谱效率/复杂度维度（A' 纪律：这两维是 pilot 固有代价）
- ❌ 在未读 thesis-lessons.md TL-25 前启动 MVE（AGENTS.md 强制）

### 本对话纪律提醒

本对话已执行 S006(§B) + S007(A0/A'/A) = **2 个完整 §4a 维度批次 + 3 次子agent 派遣**，远超单对话 3 步上限。下一步 MVE 须在新对话做，写 handoff 收尾。
