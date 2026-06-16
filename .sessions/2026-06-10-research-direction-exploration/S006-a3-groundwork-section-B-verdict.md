# [S006] A3 进 Groundwork §B 判定 PASS + 机制定位边界锁定

> 2026-06-16 续 5 | 阶段: 方向探索（Groundwork §4a 维度 B + Step 3.5 补检索）| 状态: §B 通过，A3 可进剩余步骤
> 来源: H005 任务块 A3 | 方法: §4a 维度 B 空白零假设检查 + Phase B 补检索（子agent）

## 目标

闭合 H005 任务块 A3 的三个待闭合点：① 机制定位收窄（前馈 pilot CPE vs AGC 增量，需用户确认）② 三重障碍重评 + §4a 维度 B 空白零假设检查 ③ Phase B 补检索（频域导频音+FSO+湍流有无先例）。闭合后判 A3 能否进 Groundwork 剩余步骤。本轮是对话甲（A3），对话乙（N1 gain 门控）并行独立。

## 记录

### 执行实况（治理记录）

- **框架文件已读**（AGENTS.md 强制）：`stages/groundwork.md`（步骤编排 + 完成条件）+ `stages/gw-feasibility.md`（§4a 维度 A0/A'/A/B/D 全文）。本轮落在 §4a 维度 B（新颖性-可行性解耦，特别是第 4 项空白零假设检查）+ Step 3.5 定向补充检索
- **Handoff Trigger 5 验证**：3 条关键事实声称全 PASS——① A3 无物理死锁（Paillier `content.md:177/190/196/206` 直证）② Elzanaty 是 IM/DD（`content.md:43` 直证）③ cite=81 踩 TL-03（D005 Semantic Scholar abstract 直证）
- **闭合点1 需用户确认**：通过 AskUserQuestion 锁定边界，用户选"前馈 pilot CPE（推荐）"
- **闭合点3 子agent**：后台跑，≤600s 内完成无超时（R006 教训已吸收），4 个 query + 复用 6 个 archive，未下载论文（符合约束）
- **主对话交叉验证**（AGENTS.md 强制）：子agent 关键断言"无直接先例"经核——命中最接近的 3 篇（Xu 2019/Zhou 2022/Zhou 2023）确实各缺一环，归类为 abstract 推断未验证的已在 D006 标注

### 闭合点 1：A3 机制定位边界锁定（用户确认）

**锁定定义**：A3 = 导频做**前馈 CPE 替代 VV/AGC 后 PLL 的相位估计角色**；幅度补偿仍归 AGC，A3 不重复 AGC 功能。

**增量论点（物理成立，S005 已立，本轮确认纳入 D006）**：
- AGC 放大信号也放大噪声（Paillier `content.md:177` "the multiplicative gain of the AGC loop impacts equally the signal and the noise... in deep fades, both the signal and the noise are amplified"）→ deep fade 瞬态 SNR 不改善 → PLL 仍可能跌破 critical SNR 失锁
- **前馈导频 CPE 无环路稳定性约束，无 critical SNR 失锁风险** —— A3 真正增量价值，非冗余
- 排除版："导频补幅度衰减本身"与 AGC 冗余 = 存疑，已排除

### 闭合点 2：§4a 维度 B 空白零假设检查 + 三重障碍重评 —— 通过

**空白陈述**："在星地相干 FSO（intradyne）+ 大气湍流（Gamma-Gamma/相位屏 deep fade）下，用频域连续导频音做前馈 CPE、针对 deep fade 相位跳变做专门鲁棒性设计——这个具体组合无任何论文直接验证过增益。"

**空白零假设检查（§4a 维度 B 第 4 项，须列≥3 原因逐一反驳，任一暗示结构不适用则致命）**：

| # | 空白存在的候选原因 | 反驳/降级 | 判定 |
|---|---|---|---|
| 1 | "AGC+DPLL 已是强吸引子，导频无东西可补" | Paillier 自承 2.3dB BER penalty（`content.md:200`）+ critical SNR +5dB（`content.md:190`）+ 结论段 L206 **主动呼吁** open-loop 算法应被研究 | 反驳成立 |
| 2 | "AO 把湍流压到 negligible，导频冗余"（B1 死因迁移） | 不成立。A3 攻残余幅度闪烁的相位副产物（deep fade→SNR 骤降→相位估计方差暴增），非活塞相位。Paillier §IV-A/B 量化此为主导损伤 | 反驳成立 |
| 3 | "纯粹认识遗漏" | Valjus 2025 综述实测 pilot 在 OSL deep-fade 场景 4 比 VV+差分 +1dB（`10.1002_sat.1553` 笔记 L48）并推荐 data-aided 首选；Wang 2024 OE 已在相位屏湍流做帧导频 FOE。"导频抗 fade"不新，新的是具体技术组合 | 反驳成立，增强非平凡性 |
| 4 | "前馈 CPE 已知失效（TL-18 VV 失效）" | 降级为 MVE 验证项（BC-2）。A3 是导频驱动前馈非 VV 盲估计，失效机制不同 | 降级非致命 |

**维度 B 结论**：4 个原因全部反驳或降级，**无一个暗示 A3 结构上不适用**。新颖性-可行性解耦成立——既有"没人做过"（事实），又有"做了会更好"（Paillier 2.3dB 残留 + Valjus +1dB + open-loop 呼吁）。

**三重障碍量化确认**：

| 障碍 | handoff 初判 | 本轮量化确认（基于已读笔记） | 判定 |
|---|---|---|---|
| 多普勒时变 | 工程量 | LEO 多普勒 ±4.6 GHz / rate 85 MHz/s（Pech 2025 笔记）。主流方案发射端预补偿 + 数字 CFO 前馈（Valjus 笔记 L17），data-aided ±fs/2 全覆盖。CFO 块级估计，块（μs 级）内多普勒变化 <0.1MHz 远小于残频容限——无矛盾 | 工程量，无矛盾 |
| deep fade 相位跳变 | 工程量（A3 攻的目标） | Paillier critical SNR +5dB（`content.md:190`）+ BER penalty 2.3dB（`content.md:200`）量化此问题。前馈导频不依赖环路稳定（无失锁）。fade τ_c≈1ms vs 导频连续音/密集符号，时间分辨率远细于 fade 动态 | 工程量，A3 增量清晰 |
| 单孔径无分集 | 不是障碍 | Paillier 单 50cm 孔径 σ²_I=0.684 已工作。A3 是 DSP 不引入阵列硬件，不命中 D 排除列#2。**增益预期锚 Valjus +1dB 量级**（不能期待 Wang 4 支路 +19dB，那是分集贡献非 pilot 贡献） | 非性能墙，增益锚 +1dB |

### 闭合点 3：Phase B 补检索 —— 无直接先例

子agent 4 query（continuous-wave pilot tone CPE turbulence FSO / optical pilot tone phase noise gamma-gamma / pilot-assisted feedforward CPE FSO / RF pilot tone CPE FSO dB）+ 复用 6 archive。

**核心结论：无直接先例**。命中最接近 3 篇各缺一环：
1. **Xu 2019**（Appl. Sci. 9(21):4717）—— RF pilot tone→CPE 机制成立，但**光纤无湍流**
2. **Zhou 2022 JLT**（10.1109/JLT.2021.3102664）—— pilot tone 抗湍流成立，但**self-coherent 模态补偿非数字前馈 CPE**，dB 是模态/混频指标
3. **Zhou 2023**（IEEE 10061527）—— 同上，self-homodyne，20dB 是 O/E 混频效率非相位估计 dB

**三者交集空白**（频域连续 pilot tone + 数字前馈 CPE + 湍流 intradyne FSO + 相位估计 dB 增益）未被任何论文直接测量。**迁移非平凡性增强**（更适合硕士论文），物理可行性不受影响。

**两个警示**（已纳入 D006 边界约束）：
- **PASC 路线区分（BC-1）**：Zhou/McDonald 2025 已在湍流 FSO 大量用 pilot tone 但全 self-coherent。A3 须显式区分"数字前馈 CPE"vs"PASC 自动共轭补偿"
- **residual carrier 竞争（BC-3）**：Deng 2026 提出 residual carrier 替代 pilot tone。A3 须纳入 baseline 对照

**验证状态**：Xu 2019/Zhou 2022 abstract 经 Semantic Scholar 直证；"dB 属模态/混频非 CPE"归类是 abstract 推断未验证（下强结论前建议下载 Zhou 2023+McDonald 2025 正文确认，但不阻塞 §B 判定——abstract 措辞已足够支持"无 CPE-dB 先例"）。

### §B 综合判定：PASS（附 3 条边界约束）

A3 通过 gw-feasibility §4a 维度 B，进 Groundwork 剩余步骤。3 条边界约束须在 §4a 维度 A/D + Contract 处理（详见 D006 BC-1/BC-2/BC-3）。

### 关键认知沉淀（防下个对话重走老路）

- **§4a 维度 B 空白零假设检查 ≠ 只查"有没有人做过"**：B1 也过"没人做过"（R004 gap-driven 最强），但死在"为何空白"（PLL 带宽死锁，作者没建模是因为物理不成立）。A3 的"为何空白"4 个原因全反驳——这才是 §B 通过的真正依据，不是"无先例"本身
- **D003/D006 正反对照证明 D001 框架有效**：同框架 §4a，B1 死在维度 A/B 空白零假设（活塞相位 negligible），A3 通过（攻幅度主导损伤）。框架本身不需修订，正确区分了可行/不可行
- **"无直接先例"要细分**：A3 无直接先例≠全空白。pilot 抗 fade（Valjus +1dB）、pilot tone→CPE 机制（Xu）、pilot tone 抗湍流（PASC 系列）三块都已独立验证，A3 是"已知有效机制的新组合"，不是"没人想到的赌注"。这区别于 TL-04"陷阱空白"
- **单孔径增益预期必须锚单链路量级**：Wang 4 支路 +19dB 是分集贡献，单孔径 pilot 增益应锚 Valjus +1dB。避免把分集增益误当 pilot 增益写进预期（TL-15 消融精神）

## 决策引用

- **D006（新建，本轮）**：A3 §B PASS + 机制定位边界锁定 + 3 条边界约束（BC-1 PASC 区分 / BC-2 VV 失效不迁移 MVE 验证 / BC-3 residual carrier baseline）
- D001：执行（后续阶段链——§B 通过进 §4a 维度 A/A'/D + Step 5）
- D003：参照（B1 FAIL 正面对照，同框架反结果）
- D004：参照（互锁三章主轴，A3 这条腿基本立住）
- D005：无影响（N1 锚点纠正，本轮是对话甲 A3 不涉 N1）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。§4a 维度 B 空白零假设检查 + Step 3.5 补检索是 D001 后续阶段链 Groundwork 前置，属"系统性扫描找方向"原始目标。未进 §4a 维度 D（MVE）/ Contract / Execute，未改仿真代码/开题报告
- **范围变更**：无新增。§B 判定 + Phase B 补检索在 S004"S005 已记的预检→§B"范围内，Phase B 是 groundwork.md Step 3.5 明文必做项

## 后续

### A3 下一步（Groundwork 剩余步骤，未到 MVE）

按 groundwork.md 步骤编排 + gw-feasibility.md §4a 维度顺序：

1. **§4a 维度 A（结构优势论证）**——含 BC-1（vs PASC 路线增量）+ BC-3（vs residual carrier 增量）。须回答"导频前馈 CPE 相对 PASC/residual carrier 的结构性优势在哪"
2. **§4a 维度 A'（竞争维度分解）**——A3 是单目标（相位估计方差/BER），可能不需多维分解，但须确认
3. **§4a 维度 A0（问题-方法适配性）**——A3 是 DSP 非纯 ML，A0 的 ML 适配性问题需判断是否适用（可能大部分跳过，记跳过原因）
4. **§4a 维度 D（MVE）**——含 BC-2（VV deep fade 失效 vs 导频 CPE 不失效对比）。这是 A3 首次碰实验，须过 TL-25 起飞检查单
5. **Step 5 baseline 选定**——Valjus 2025 算法地图 + Paillier 2020 仿真基线
6. 4b（C/E 维度）→ Step 6/7

**未到 MVE**：维度 A/A'/A0 是分析性前置，做完才进维度 D MVE。D001 后续阶段链不变。

### 不做（Dead Ends）

- ❌ 跳过 BC-1/BC-2/BC-3 直接进 MVE（边界约束未处理前不进维度 D）
- ❌ 把 A3 pilot 增益预期锚 Wang 4 支路 +19dB（分集贡献，单孔径不成立）
- ❌ 把 TL-18 VV 失效当"A3 前馈也失效"预先判 FAIL（失效机制不同，须 MVE 验证）
- ❌ 找第 4/5 方向（用户已拦）
- ❌ 锁"互锁三章"叙事（A3 §B 过了但 N1 还在门控，未完全 PASS）
- ❌ 在未读框架文件前进下一步（AGENTS.md 强制——本轮已读 groundwork.md + gw-feasibility.md）
