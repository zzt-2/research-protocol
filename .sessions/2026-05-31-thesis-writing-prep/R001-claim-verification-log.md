# [R001] PPT/开题报告声称验证日志

> 2026-06-04 | 关联：开题答辩 PPT + kaiti-report.md §1.2
> 目的：系统验证所有学术声称的事实性，确保答辩和报告经得起追问

## 验证状态说明

- ✅ 已验证（有原文支撑）
- ⚠️ 部分准确（需修正描述）
- ❌ 不准确（需删除或重写）
- ❓ 待验证（未查原文）
- 📚 教科书级（无需查原文）

---

## HIGH：直接影响 PPT/报告文字正确性

> 这些声称如果错了，答辩时被追问会很被动

| # | 声称 | 出处 | 状态 | 问题 | 影响 |
|---|------|------|------|------|------|
| H1 | Safi 2019：功率与编码联合优化框架，用"单一衰减因子近似"估计误差 | P8口述 + kaiti-report §现状 | ❌ 不准确 | 原文用序列检测+高斯噪声模型，不是"单一衰减因子"。真实 limitation：高斯误差假设+未考虑反馈时延导致 CSI 过时 | P8口述稿+报告原文需修正 |
| H2 | Petkovic 2023：Málaga 湍流下 SER 框架 + DPLL 设计准则，但"假设精确 CSI" | P9口述 + kaiti-report §现状 | ❌ 不准确 | 原文核心就是 imperfect phase compensation (Tikhonov 模型)。真实 limitation：仅研究 DPLL 一种方法，假设相位噪声统计特性已知，未涉及 CSI 估计误差对 CPR 的影响 | P9口述稿+报告原文需修正 |
| H3 | Selim 2026："单一模块级优化无法保证系统级性能最优" | P8口述 + kaiti-report §现状 | ❌ 不适用 | 论文是 AO（自适应光学）综述"AO Survey: No Single Optimal Paradigm"，非信号处理领域。从 AO 推广到"各模块协同"属过度泛化。S003 已预警但未采纳 | **整句删除或换引用** |
| H4 | Brandao 2024：100 Gbps FSO 外场试验验证相干接收机端到端性能 | kaiti-report §现状 | ❌ 归因错误 | 论文核心是**发射端功率自适应**（LoRa 反馈），非接收端信道估计验证。S003 已标注"归因偏宽" | **删除"估计方案可行"推断** |
| H5 | E[1/h] 在 β<1 时发散 | P8 + kaiti-report | ✅ 已验证 | Andrews & Phillips 2005 标准结果，数值积分+解析双重确认。E[1/h]=Γ(α+(-1))Γ(β+(-1))/(Γ(α)Γ(β))，存在要求 α>1 且 β>1 | 无 |
| H6 | Paillier 2020：星地链路 DPLL 参数沿用 AWGN 公式 | P9口述 + kaiti-report | ✅ 已验证 | 原文确实基于 Gardner 标准二阶环路公式（ξ=1/√2, B_L），未针对湍流修正参数 | 无 |
| H7 | "编码辅助载波恢复在射频和光纤有坚实基础" (Oh 2001, Lottici 2004, Castrillon 2015) | P9口述 + kaiti-report §现状 | ✅ 已验证 | Oh 2001: turbo 码联合解码奠基(RF)；Lottici 2004: EM 算法完整框架(RF)；Castrillon 2015: 光纤相干 JIDD 验证(光纤) | P9方法探索层可用 |
| H8 | "多源相位噪声联合建模已有初步探索" (Ozbilgin 2025, Nguyen 2020) | kaiti-report §现状 | ⚠️ 部分准确 | Ozbilgin 2025 ✅确认。**Nguyen 2020 bib 条 DOI 错误**（10.1109/ACCESS.2020.2989012→应为 10.1109/ACCESS.2020.3036643），实际标题为"QAM/FSO with pointing misalignment and phase error over turbulence"，是性能分析非联合建模 | **修正 Nguyen bib + 调整描述** |

## HIGH（续）：Batch 2 全文扫描新发现

| # | 声称 | 出处 | 状态 | 问题 |
|---|------|------|------|------|
| H9 | @yaseen2024：导频辅助 MMSE 估计 | kaiti-report §1.2 表 | ❌ 引用错误 | 实际是可见光通信(VLC) ML 估计，非 FSO MMSE。领域不对 |
| H10 | @shi2025：DL 辅助载波恢复 | kaiti-report §1.2 表 | ❌ 缺失引用 | references.bib 中不存在该条目 |
| H11 | @yang2025：BPS 方法 | kaiti-report §1.2 表 | ⚠️ 归因不准 | 实际是通用低复杂度 CPE，非专门 BPS |
| H12 | @mcdonald2025：湍流抑制+NMSE降3dB | kaiti-report §1.2 表 | ⚠️ 需验证 | 实际是 800m 外场试验，"湍流抑制""3dB"需确认 |

## MEDIUM（续）：全文扫描中优先级

| # | 声称 | 出处 | 状态 | 问题 |
|---|------|------|------|------|
| H13 | @li2024jlt "强湍流条件" | kaiti-report §1.2 表 | ⚠️ 需验证 | 689Gbps 实验室验证，"强湍流"描述待确认 |
| H14 | @zhang2023kf + @sun2020 | kaiti-report §1.2 表 | ✅ 归因正确 | 自适应 Kalman 和 SR-UKF 确认 |
| H15 | @han2022jlt "未进一步分析" | kaiti-report §1.2 | ⚠️ 需验证 | Han 确实关注中断概率非载波同步，但需确认 |
| H16 | Selim 2026 再次出现 | kaiti-report §1.2 L95 | ❌ 已知问题 | 同 H3，需删除 |
| H17 | 多普勒 ±5GHz/40-150MHz/s 来源 | kaiti-report §1.2 L70 | ⚠️ 需验证 | 引用 fernandes2023，数值待确认 |
| H18 | 湍流参数来源 Andrews 2005 | kaiti-report §研究方案 | ✅ 合理 | 经典专著 |

## MEDIUM：时间线/方法表的事实性

> 这些如果错了不影响核心论点，但影响文献综述的可信度

| # | 声称 | 出处 | 状态 | 问题 |
|---|------|------|------|------|
| M1 | Khalighi 2014 综述 2378 引 | P5 时间线 | ✅ 准确 | 引用数随时间变化，PPT 建议不写具体数 |
| M2 | Elfiky 2024：DL 信道估计 MSE ≈ MMSE | P6 CE 表 | ⚠️ 待验证 | 需查原文确认"MSE≈MMSE"；实际是卫星光通信非纯 FSO |
| M3 | Mohammed 2026：CNN+BiLSTM 强湍流估计 | P5 时间线 | ✅ 准确 | 年份/方法/场景均确认 |
| M4 | Han 2022 JLT：CE 误差对 FSO 系统影响 | P5 时间线 | ✅ 准确 | 已有详细验证记录支持，IP1 对标确认 |
| M5 | Guan 2019：VV 应用于地面 FSO 相干通信 | P5 时间线 | ✅ 准确 | 中文论文，已弱化描述 |
| M6 | Paillier 2020："首个端到端 DPLL+AO+湍流联合分析" | P5 时间线注释 | ⚠️ 弱化可用 | "首个"有争议（Ozbilgin 2025 也做了类似工作），PPT 已弱化 |
| M7 | Neves 2023：CPR 综述含 DL | P5 时间线 | ✅ 准确 | 确认涵盖 BPS/VVPE/DPLL/Kalman/DL |
| M8 | Zhao 2025：联合多普勒+相位补偿 <0.5dB | P5 时间线 | ✅ 准确 | 星间场景(AWGN)，非湍流场景；<0.5dB 确认 |
| M9 | Taylor 2009：CPR 经典综述 435 引 | P5 时间线 | ✅ 准确 | JLT 2009，PLL vs 前馈理论框架 |
| M10 | Zhang 2018：LS/MMSE 在 OAM-FSO 验证 | P5 时间线 | ✅ 基本准确 | 实际是"LS+ZF/MMSE Equalization"，简化可接受 |
| M11 | Tanimura 2012：DPLL 闭环结构 | P5 时间线 | ❓ bib 缺失 | references.bib 中无 Tanimura 条目 |

## LOW：教科书级知识

> 这些是本领域常识，无需查原文，但表述需要准确

| # | 声称 | 出处 | 状态 |
|---|------|------|------|
| L1 | QPSK 四重旋转对称性 → 对相位误差有容忍度 | P8 口述 | 📚 |
| L2 | 16-QAM 对相位误差高度敏感 | P8 口述 | 📚 |
| L3 | Gardner 1979：PLL 环路带宽与跟踪误差折中 | P9 口述 | 📚 |
| L4 | Moeneclaey 1994：VV 最优窗口闭合公式 | P9 口述 | 📚 |
| L5 | VV：M-次幂非线性消除调制，算术平均估计相位 | P7 CPR 表 | 📚 |
| L6 | BPS：相位空间穷举搜索，复杂度随调制阶数剧增 | P7 CPR 表 | 📚 |
| L7 | DPLL：闭环反馈跟踪，环路滤波抑制噪声 | P7 CPR 表 | 📚 |

## 验证批次计划

### Batch 1（3 agents 并行）— HIGH 优先级 ✅ 完成

- **Agent A**：H3 Selim 2026 + H4 Brandao 2024 → **两处均有问题**（Selim 是 AO 综述非 SP；Brandao 是发射端非接收端）
- **Agent B**：H7 编码辅助三篇 + H8 多源相位噪声 → **H7 ✅ 全确认；H8 Nguyen bib DOI 错误**
- **Agent C**：H1 Safi + H2 Petkovic 修正方案 → **已找到准确 gap 描述建议**（见下方 Batch 1 关键发现）

### Batch 2（3 agents 并行）— MEDIUM 优先级 ✅ 完成

- **Agent D**（M1-M5）：✅ 4 准确 / 1 待验证（M2 Elfiky "MSE≈MMSE"）
- **Agent E**（M6-M11）：✅ 5 准确 / 1 弱化可用（M6 "首个"）/ 1 bib缺失（M11 Tanimura）
- **Agent F**（全文扫描）：发现 4 个新 HIGH（H9-H12）+ 6 个 MEDIUM（H13-H18）

### Batch 3 — 汇总修正

- 根据 Batch 1-2 结果，列出所有需修正的文件位置（PPT + kaiti-report）
- 提出修正文本

### Batch 3 — 汇总修正

- 根据 Batch 1-2 结果，列出所有需修正的文件位置（PPT + kaiti-report）
- 提出修正文本

## 附加关注点：PPT/第一章可能关键的信息

验证过程中同时留意：

1. **被引论文的实际 limitation 是否比我们描述的更/更不严重**——影响空白措辞强度
2. **是否有更近的同类工作（2024-2026）覆盖了我们声称的空白**——影响空白是否存在
3. **各论文的研究场景（FSO vs 光纤 vs RF）**——影响引用的合理性
4. **Petkovic 的 Málaga 模型与 GG 的关系**——确认"可退化为 GG"的数学条件
5. **Petkovic 实际的 limitation 是什么**——用于精确描述我们的差异化

## Batch 1 关键发现

### 必须删除/替换的引用

1. **Selim 2026 — 删除**：AO 综述论文，与信号处理无关。kaiti-report 中"单一模块级优化无法保证系统级性能最优"这一论断需换引用或改为不引用的通用表述。
2. **Brandao 2024 — 修正归因**：论文是发射端功率自适应，不能用来支撑"估计方案工程可行"。要么修正描述为"外场试验验证了 FSO 相干通信链路的工程可行性"（不提估计），要么换引用。

### 必须修正描述的引用

3. **Safi 2019 — 修正描述**：
   - 旧："用单一衰减因子近似估计误差的影响"
   - 新建议："通过高斯噪声模型分析估计误差对自适应传输的影响，但未区分不同信号处理方法对误差的灵敏度差异"
   - 真实 limitation：高斯误差假设 + 未考虑反馈时延
4. **Petkovic 2023 — 修正描述**：
   - 旧："假设信道状态信息精确已知"
   - 新建议："考虑了 PLL 相位噪声（Tikhonov 模型），但仅研究 DPLL 一种方法，且未涉及信道估计误差对载波恢复性能的影响"
   - 真实 limitation：(a) 仅 DPLL (b) 假设相位噪声统计已知 (c) 无 CSI 误差→CPR 影响
   - **高参考价值**：FSM 方法 + 误差地板分析 + "分析→设计准则"模式与我们的工作完全对标
   - Málaga→GG 条件：ρ→1, g→0 时 Málaga 退化为 GG

### Bib 错误

5. **Nguyen 2020 DOI 错误**：
   - bib 中：`10.1109/ACCESS.2020.2989012` ❌
   - 正确：`10.1109/ACCESS.2020.3036643`
   - 实际标题："Performance of Generalized QAM/FSO Systems With Pointing Misalignment and Phase Error Over Atmospheric Turbulence Channels"
   - 该论文是性能分析（pointing error + phase error + turbulence），不是"多源相位噪声联合建模"

### 额外发现（对 PPT/报告有用）

- Petkovic 论文中的 FSM（Fourier Series Method）收敛性分析、误差地板识别、设计参数提取方法，与我们的"分析→设计准则"模式高度一致，是方法论对标的好素材
- Code-aided 在 FSO 湍流场景确认为完全空白（三篇确认均在 RF/光纤），空白描述可以放心使用
- "多源相位噪声联合建模"的空白需要精确化——不是"从无到有"而是"从粗到精"（现有工作多为整体性建模，缺乏多源区分式分析）

## 变更记录

| 日期 | 变更 |
|------|------|
| 2026-06-04 | 创建。8 HIGH + 11 MEDIUM + 7 LOW 条目，3 批次验证计划。 |
| 2026-06-04 | Batch 1 完成。8 HIGH 中：✅ 3（H5/H6/H7），⚠️ 1（H8 Nguyen bib错），❌ 4（H1/H2描述错，H3/H4引用错）。新增 Batch 1 关键发现段。 |
| 2026-06-04 | Batch 2 完成。11 MEDIUM 中：✅ 8，⚠️ 2（M2/M6），❓ 1（M11）。全文扫描新增 H9-H18（4 HIGH+6 MEDIUM）。 |
