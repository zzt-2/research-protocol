# Literature Notes — 仿真项目（均衡层方向侦察）

> 专题: 2026-07-10-equalization-layer-direction-scouting
> 阶段: GW Step 2/3 精读（批次 1 ISI 均衡子地带，2026-07-10）
> 纪律: INVARIANT 6（abstract 不判缝，全文层才判判据 A）/ INVARIANT 7（§7.2 三硬规则）/ INVARIANT 19（Trans 必精读作主力）/ D018（中性提取不边摸边 Kill）

---

## ISI 均衡子地带（批次 1，2026-07-10）

> **源债务诚实标注**：Ajam TCOMM 2026（ISI 主题论文，唯一星地 ISI Trans）**paywall 下不到全文**，本批靠 abstract + Ajam 团队 2022 前置论文（arXiv OA 全文）+ sat.1553 §6 综述全文提取。TCOMM 2026 的均衡器实验细节（ZF-LE/DFE/DCO-OFDM 具体 BER 曲线）未核验，标"二手 abstract"。

### [L01] Modeling & Mitigation of ISI in High Rate IRS-Assisted FSO

- DOI/来源：10.1109/TCOMM.2025.3636084（**TCOMM 2026，paywall 无全文**）
- 源文件路径：**无全文**（abstract 来自 search-archive/2026-07-10/irs-reconfigurable-intelligent-surface-free-space-optical-in.json，S2+OpenAlex+seed 三重确认）
- **发表状态**：正式发表（IEEE TCOMM 2026）
- **发表渠道**：IEEE Transactions on Communications（SCI Q1 Trans）
- 年份：2026
- 核心贡献：建立 IRS-assisted FSO 系统（**square-law PD 接收**）端到端线性模型，推导 IRS 诱导延迟色散的解析 CIR，揭示 IRS 几何/相位剖面与延迟展宽关系。对比 OOK+ZF-LE / OOK+DFE / DCO-OFDM 三均衡方案 [abstract]
- 方法概述：基于 IRS 反射几何推导 CIR；1m² 方形 IRS 面内反射最大延迟展宽 ~0.7ns（>10Gbps 致 ISI）；延迟展宽近似独立于 IRS 相位剖面，但聚焦/二次相位剖面接收功率大于线性剖面 [abstract]
- 实验设置：abstract 未给 BER 曲线细节，仅给结论排序。**二手 abstract**
- 使用的 Baseline 方法：
  - OOK+ZF-LE（zero forcing linear equalizer）：线性均衡，性能最差 [abstract]
  - DCO-OFDM（DC-clipped optical OFDM）：优于 OOK+ZF-LE [abstract]
  - OOK+DFE（decision feedback equalizer）：**始终优于 DCO-OFDM** [abstract]
- 关键结论：IRS 诱导延迟色散可通过接收端均衡缓解；DFE > DCO-OFDM > ZF-LE [abstract]
- 与本研究关系：**⚠ 场景不匹配风险（最高优先级）**——见下"接收体制适配"
- 实现关键细节：abstract 未给具体数值（均衡器抽头数/BER 曲线/SNR 点）。**全文 paywall，细节未核验**
- 开源代码：未知（abstract 未提）
- 验证状态：abstract 已 §7.2 核查（关键声称全在 abstract 文本中，PASS）

#### 接收体制适配性分析（PROMPT-002 陷阱 1 核查）

**⚠ 关键发现：Ajam 是 IM/DD square-law PD 接收，非 intradyne 相干**

abstract 明确："an IRS-assisted FSO system employing a **square-law photo detector (PD) receiver** can be modeled as a linear end-to-end system"。Ajam 团队 2022 前置论文（arXiv 2108.00291 全文 §7.2 核查）进一步确认：
- 信号模型 = IM/DD（intensity modulation / direct detection）[content.md L57]
- 调制 = OOK（on-off keying，实数基带强度）[L63]
- 接收 = 透镜 + PD（square-law，检测光强 |E|²）[L13/L47]

**与本专题场景（单偏振 intradyne 相干 QPSK 复基带）的差异**：
1. **检测体制不同构**：PD square-law 检测光强（实数），intradyne 相干检测复基带（保留相位）。PD 的 ISI 是实数强度卷积，相干 ISI 是复基带卷积——数学结构不同
2. **调制不同构**：Ajam 用 OOK（1 bit/symbol，实数），本场景用 QPSK/16-QAM（复基带）
3. **IRS 延迟色散 vs 大气湍流时域展宽**：Ajam 的 ISI 源是 **IRS 不同 tile 光程差**（几何诱导），本场景星地直射链路**无 IRS**。大气湍流致时域展宽在 Ajam 2022 前置论文中**未建模**（湍流是乘性标量 GG 衰落，无 CIR 时延扩展，[L67-73]）[全文 §7.2 核查]

**结论（守 D018，不 Kill 只标风险）**：Ajam TCOMM 2026 的 ISI 机制（IRS 几何诱导延迟色散 + PD/IM-DD）**跟本专题场景（intradyne 相干 + 直射星地 + 无 IRS）双重不匹配**。降级为"**参考不当主 baseline**"（守 INVARIANT 19 精读分层——但这里不是档级问题，是场景机制不匹配）。主力 baseline 池需另寻。

---

### [L02] Modeling and Design of IRS-Assisted Multilink FSO Systems（Ajam 团队前置论文）

- DOI/来源：10.1109/tcomm.2022.3163767（arXiv 2108.00291 OA 版全文）
- 源文件路径：papers/arxiv/2108.00291/content.md（650 行，全文已落盘 §7.2 核查 PASS）
- **发表状态**：正式发表（IEEE TCOMM 2022）
- **发表渠道**：IEEE Transactions on Communications（SCI Q1 Trans）
- 年份：2022
- 核心贡献：基于 Huygens-Fresnel 原理建立 IRS-FSO 点对点解析信道模型（GML），引入"中间场"概念修正远场近似失效。提出 TD/IRSD/IRSH 三种 IRS 多链路共享协议 [content.md L127-176, L289-301]
- 方法概述：IRS 分 Q 个 tile，每 tile 带连续相位剖面（LP 线性 / QP 二次）；反射场由 Huygens-Fresnel 积分求和；端到端信道 h = h_a(GG 湍流) × h_p(大气损耗) × h_irs(几何对准)，**全是标量** [L67-73]
- 实验设置：10⁶ 次信道实现，对比解析 GML vs Huygens-Fresnel 数值积分 vs 远场近似 [L444-446, L476]
- 使用的 Baseline 方法：
  - 远场近似（Fraunhofer）：本文证其在 km 级 FSO 失效（远场距离 d_f=32.7km）[L164]
  - 几何光学（前作）：忽略 IRS 尺寸/透镜尺寸 [L7]
  - TD/IRSD/IRSH 三协议互为对照 [L289-301]
- 关键结论：QP 相位剖面比 LP 增益高达 12dB [L478]；无对准误差时 IRSD 最优，有误差时 IRSH 更鲁棒 [L492]
- 与本研究关系：**信道模型前置参考**——提供 Ajam 团队 IRS-FSO 几何/场论基础，但**不含 ISI/时延色散**（§7.2 核查：全文无 "intersymbol/ISI/delay dispersion/channel impulse response"）
- 实现关键细节：GG 湍流参数 (α,β)；OOK 调制；AWGN σ_w²；远场距离 d_f=32.7km [L63, L73, L164]
- 开源代码：无
- 验证状态：全文已 §7.2 核查（IM/DD + OOK + PD 确认 PASS / 无 ISI 讨论确认 PASS）

#### 问题提取（M-C-A）

- **M（方法）**：IRS-FSO Huygens-Fresnel 解析信道模型（标量 GML，LP/QP 相位剖面）
- **C（条件）**：IRS-assisted 多链路 NLOS FSO，IM/DD + OOK + PD 接收，GG 湍流
- **A（失效原因）**：**不适用**——本论文是信道建模论文，不是均衡论文，baseline 无"失效"概念。它的局限是"**未建模时域延迟色散**"（纯空间/功率标量模型），这个局限正是 TCOMM 2026 补的
- **四判据初筛**：❌（不是均衡问题，是信道模型；作为 ISI 机制的参考不当 Q# 起点）

---

### [L03] sat.1553 §6 Adaptive Equalizer（综述，光纤衍生均衡理论参考）

- DOI/来源：10.1002/sat.1553（IJSCN 2025 综述，已落盘全文）
- 源文件路径：papers/doi/10.1002_sat.1553/content.md（§6 L561-760）
- **发表状态**：正式发表（Open Access）
- **发表渠道**：International Journal of Satellite Communications and Networking
- 年份：2025
- 核心贡献：系统综述相干 OSL 的自适应均衡器架构（butterfly PolDemux / 两级结构 / MMSE / LMS / CMA / DA-LMS / FDE 实现）[§6 L561-760]
- 方法概述：
  - **butterfly 均衡器**（4 FIR wxx/wxy/wyx/wyy 做 PolDemux）[L566-572]——**本专题单偏振不适用**
  - MMSE 准则 W = D(I/SNR + HᴴH)⁻¹Hᴴ [L660 Eq.43]
  - LMS 迭代自适应 / CMA 盲均衡 / DA-LMS 数据辅助 [L677-715]
  - **FDE**：仅作 butterfly 滤波器复杂度优化手段（频域实现 N-tap FIR），**非 SC-FDE ISI 均衡** [L582]
- 实验设置：4 OSL 场景仿真，SNR penalty vs BER 10⁻³，QPSK
- 关键结论：DA-LMS/CMA 跟踪 >10⁻⁵ rad/symbol（28GBaud 下 ~300krad/s）；深衰落场景 3/4 penalty 略大于静态场景 1 [§6.1 分析]
- 与本研究关系：**均衡器架构参考**——但 §6 核心是 **PolDemux butterfly**（双偏振），本场景单偏振。FDE 仅作实现优化非 ISI 均衡。**§6 不直接给 ISI 均衡 baseline**
- 实现关键细节：CAZAC 训练序列 [L627]；CMA μ=0.0005/0.0001；DA-LMS μ=0.002/0.001 [L760]；两阶段均衡器 6ps DGD 致 1dB penalty（32GBaud DP-QPSK）[L572]
- 开源代码：无（综述）
- 验证状态：全文已 §7.2 核查

#### 问题提取（M-C-A）

- **M（方法）**：相干 OSL 自适应均衡器综述（butterfly PolDemux + MMSE/LMS/CMA/DA-LMS + FDE 实现）
- **C（条件）**：DP-QPSK 相干 OSL，GG 湍流（SOP 旋转 + DGD + PDL）
- **A（失效原因）**：**综述级，无单一 baseline 失效**。隐含的挑战：深衰落期 CMA 发散到局部最优 [L582]
- **四判据初筛**：❌（综述不是具体问题；§6 核心是 PolDemux 非 ISI，不匹配本场景单偏振）

---

## 综合分析（ISI 均衡子地带，批次 1）

### 1. 现有方法分类

ISI 均衡子地带在星地 FSO 场景下**极度稀疏**，呈"孤证 + 跨域迁移"格局：

| 类别 | 方法 | 代表 | 场景适配 |
|---|---|---|---|
| **IRS 诱导 ISI**（Ajam 新切口） | OOK+ZF-LE / OOK+DFE / DCO-OFDM | Ajam TCOMM 2026 (#29) | ⚠ PD/IM-DD + IRS 几何，非相干非直射 |
| **IRS 延迟色散建模** | 4×4 镜面阵列光程差 | Rittler 2026 (#30) | PD，范围出界参考 |
| **IRS-delay VLC** | IRS 阵列时延频域特性 | Chen 2023 (#31) | VLC 非 FSO，出界参考 |
| **云散射 ISI + channel shortening** | Viterbi/ML 序列检测 | Lee&Kavehrad 2006/2009 (#32#33) | 老文 15+ 年，cloud 多散射非湍流 |
| **DPSK + BM-CMA** | set-membership CMA | Zhang 2018 (#20) | 孤证，云散射致 ISI |

**光纤迁移 baseline 池（凑 D-010 4 篇 Trans 的主力来源）**：
- 搜索召回 20 篇光纤 DFE/FDE/EDC Trans（Bulow 2008 JLT 108引 / Crivelli 2014 TCSI 55引 / Zheng 2018 OE 51引 / Falconer 2002 CommMag 2432引 等），**全部 paywall 下不到全文**（JLT/TCOMM/OE/CommMag 全闭源）。仅有 abstract。
- **⚠ 机制同构性疑虑（诚实）**：光纤 ISI 源 = 色散（CD/PMD，确定性长时延扩展），星地 ISI 源 = IRS 延迟色散（Ajam）或云多散射（Lee）。DFE/FDE 原理（时域/F域反卷积）通用，但**触发 ISI 的物理条件不同**。迁移 baseline 要论证"机制同构"，但全文 paywall 无法核验。

### 2. 已知局限（从 abstract/综述提取，非全文层）

1. **ISI 子地带 baseline 池薄**：星地原生仅 Ajam TCOMM 2026 单篇 Trans（+ Rittler/Chen 出界 + Lee 老文）。D-010 标准 4 篇 Trans 凑不齐
2. **Ajam 场景不匹配**：PD/IM-DD + IRS 几何诱导 ISI ≠ intradyne 相干 + 直射星地。机制双重不匹配（检测体制 + ISI 物理源）
3. **湍流致时域 ISI 未被建模**：sat.1553 §6 综述（最权威 OSL DSP 综述）的均衡器章节是 **PolDemux butterfly**（双偏振 SOP 跟踪），**不含 ISI/时域色散均衡**。GG 湍流在所有已读论文中是**乘性标量衰落**（功率 scintillation），**未建模致 ISI 的时域 CIR 展宽**
4. **光纤迁移 baseline 全 paywall**：凑池主力来源（光纤 DFE/FDE）全文下不到，机制同构性无法全文核验

### 3. 2-3 年趋势

- IRS-FSO 是 2021+ 新兴方向（Ajam 团队 TCOMM 2022 建模 → GLOBECOM 2024 延迟色散 → TCOMM 2026 ISI 均衡），但**聚焦 IRS 场景的 ISI**，非直射星地
- 星地相干 OSL 的 DSP 研究重心在 **载波恢复（CFO/CPE）+ PolDemux**（sat.1553 §3-6），**ISI 均衡不是活跃切口**
- 光纤领域 DFE/FDE/EDD 是成熟大池（Falconer 2002 2432引 / Bulow 2008 108引），但已是基础理论，新增量在非线性补偿非 ISI

### 4. 研究背景概述

星地激光通信的信号处理分三层（sat.1553 §1）：定时恢复 → 载波同步 → 均衡。前两层（定时/载波）在本专题上游已全 Kill（B2/B3-Q2/B5/B7）。均衡层又分 PolDemux（双偏振，D002 排除）和 ISI 均衡（本批）。

ISI 均衡在星地场景的核心问题是：**什么物理机制在星地链路产生 ISI？**
- 光纤：色散（CD 确定性 + PMD 随机）→ 经典 EDC/DFE/FDE 大池
- 星地 IRS：IRS tile 光程差（Ajam）→ 但本场景无 IRS
- 星地直射：**大气湍流是否致时域 ISI？** —— sat.1553 综述口径：湍流是乘性标量衰落（scintillation），**不建模时域展宽**。Lee&Kavehrad 2006 的 ISI 来自 cloud 多散射（非晴空湍流）

**诚实结论（守 D018，不 Kill 只标观察）**：在已读材料范围内，**星地晴空 GG 湍流致 ISI 的物理机制未被主流文献建立**。这是 ISI 子地带的核心风险——不是"baseline 不够强"，是"**触发 ISI 的物理前提在标准星地场景下可能不成立**"（B7 模式风险：解决不存在的问题）。

### 5. 研究问题清单（Q# 候选，初筛，≥3 条禁单假设）

> **守 INVARIANT 6**：以下 Q# 是 abstract + 综述 + 前置论文层推断，**不是判据 A 全文层结论**。TCOMM 2026 全文 paywall 未读，机制细节待证。守 D018 全摸完排优先级不 Kill。

| Q# | 问题（M-C-A） | 四判据初筛 | 来源 |
|---|---|---|---|
| **Q1** | 星地直射链路（无 IRS）下，**多径/大气湍流是否在高速率（>10Gbps）产生可均衡的时域 ISI**？M=DFE/FDE，C=单偏振 intradyne 相干 + GG 湍流 + 高速率，A=**待证**（sat.1553 综述说湍流是标量衰落无时域展宽，但 Lee 2006 cloud 多散射有 ISI，晴空湍流待查） | 具体矛盾❓ / 方法形态✅(DFE/FDE) / 2019+ baseline❌(星地原生薄) / 能对比✅(光纤迁移) | sat.1553 §6 + Ajam + Lee |
| **Q2** | 若星地直射不产生 ISI，**IRS-assisted 星地链路**（加 IRS 反射面）的延迟色散 ISI 能否迁移到相干接收？M=DFE/FDE 相干版，C=intradyne 相干 + IRS，A=Ajam 只做了 PD/IM-DD 版，相干版 ISI 机制不同构（复基带 vs 实数强度） | 具体矛盾✅(PD vs 相干缺口) / 方法形态✅ / 2019+ baseline❌(Ajam 孤证且 PD) / 能对比❌(无相干 IRS-ISI baseline) | Ajam TCOMM 2026 |
| **Q3** | **DFE vs FDE vs OFDM 在星地湍流信道的性能排序**是否跟 Ajam PD 场景（DFE>DCO-OFDM>ZF-LE）一致？相干场景排序可能不同。M=三方案相干版对比，C=intradyne 相干 + ISI 信道，A=Ajam 排序仅在 PD 下验证，相干下待证 | 具体矛盾✅ / 方法形态✅ / 2019+ baseline❌ / 能对比❌(无相干 ISI 对比) | Ajam abstract |
| **Q4** | **自适应均衡器在湍流深衰落期的跟踪鲁棒性**——sat.1553 提到 CMA 深衰落发散到局部最优 [L582]。自适应 ISI 均衡器（LMS/DD-LMS）在 GG 深衰落下是否失效，能否改进？M=衰落鲁棒自适应均衡，C=GG 深衰落 + ISI，A=CMA/LMS 深衰落发散 | 具体矛盾✅(深衰落发散) / 方法形态✅(variable step/freeze) / 2019+ baseline❌(sat.1553 是 2025 综述但非 ISI 专) / 能对比✅ | sat.1553 §6 L582 |

**Q# 初筛观察（守 D018，不 Kill）**：
- 4 条 Q# 共同的硬伤：**2019+ baseline 判据普遍 ❌**（星地 ISI 原生 Trans 仅 Ajam 单篇且 PD，光纤迁移 baseline 全 paywall 无法核验机制同构）
- Q1 最根本：**星地直射 GG 湍流致 ISI 的物理前提待证**（sat.1553 综述口径说不成立）。如果物理前提不成立，Q1-Q3 全部塌方（B7 模式）
- Q4 是唯一不依赖"湍流致 ISI 物理前提"的切口（深衰落跟踪鲁棒性），但偏自适应算法层非 ISI 机制层，且 sat.1553 已提 variable step size [L760]

### 6. baseline 凑池可行性评估（D004 筛选判据 A）

| 判据 | 评估 |
|---|---|
| **A. baseline 凑池**（D-010 标准 4 篇 Trans） | **❌ 凑不齐**。星地原生 ISI Trans 仅 Ajam 1 篇（且 PD 非 + paywall）。光纤迁移 DFE/FDE Trans 池大（Falconer/Bulow/Crivelli/Zheng 等）但**全 paywall 无全文**，机制同构性（光纤色散 vs 星地湍流）无法全文核验。标"光纤迁移，机制待验证" |

**诚实结论**：ISI 子地带 baseline 凑池**高风险**。D-010 标准 4 篇 Trans 在星地场景凑不齐，靠光纤迁移但全文下不到 + 机制同构性存疑。

---

## ISI 子地带批次 1 总结（交阶段 2.5 矩阵 + 阶段 3 判读）

> **守 INVARIANT 6 + D018：不判 Go/Kill 不判地，只产 Q# 候选 + 四判据初筛 + 观察记录。**

**核心发现（诚实）**：
1. **ISI 子地带在标准星地直射相干场景下物理前提存疑**：sat.1553 综述（最权威 OSL DSP）将湍流建模为乘性标量衰落（scintillation），**不建模时域 CIR 展宽**。Ajam ISI 来自 IRS 几何（非湍流），Lee ISI 来自 cloud 多散射（非晴空）。**晴空 GG 湍流致 ISI 的物理机制在主流文献中未被建立**
2. **Ajam（唯一星地 ISI Trans）场景双重不匹配**：PD/IM-DD（非相干）+ IRS 几何（非直射）。降级参考不当主 baseline
3. **baseline 凑池高风险**：D-010 标准 4 篇 Trans 凑不齐，光纤迁移全 paywall + 机制同构性存疑

**与 AO-DSP 子地带（批次 2）对比待阶段 3**：两子地带 baseline 都薄，但 ISI 的物理前提风险（湍流是否致 ISI）比 AO-DSP 的载波边界风险更根本。阶段 3 判读需回答：**如果湍流不致 ISI，ISI 子地带整个塌方**（B7 模式：解决不存在的问题）。

**⚠ 未闭合点（诚实债务）**：
- TCOMM 2026 Ajam 全文未读（paywall）—— DFE/OFDM 具体 BER 曲线、均衡器抽头数、SNR 增益未核验
- 光纤 DFE/FDE 迁移 baseline 全文全 paywall —— 机制同构性无法全文核验
- **晴空 GG 湍流是否致时域 ISI 的物理判定**——sat.1553 综述说不建模，但需查湍流信道 CIR 文献确认（本批未查，阶段 3 判读前补）

---

## AO-DSP 残余补偿子地带（批次 2，2026-07-10）

> **边界检查前置（PROMPT-002 + H003 + H004 最高优先级）已完成**：Paillier 系（AO + DPLL）DSP 段余 = 载波 PLL（多普勒残频+残余载波相位），**非信号域均衡**，按红线排除。本批只精读**信号域残余补偿**论文。

### 边界检查结论（Paillier 系排除）

基于已有精读笔记 papers/_read_notes/10.1109_jlt.2020.3003561.md（载波同步 v2 阶段读）：
- **Paillier 2020 JLT**（#34）：AGC + DPLL 分治架构。DPLL 环路传递函数针对**多普勒残频 + 激光相位噪声**设计，不针对湍流相位单独建模。残余 piston 相位进 DPLL（载波域 track）
- **结论**：Paillier 系 DSP 段余 = **载波 PLL**（载波同步层），**非信号域均衡**。按红线排除（载波同步已完成不回头）
- Paillier 2019 ICSOS（#35）同 #34 会议先导版，同排除

---

### [L04] Enhanced Atmospheric Turbulence Resiliency With SIC-DSP in MDM FSO

- DOI/来源：10.1109/JLT.2022.3209092（arXiv 2208.00836 OA 全文，197 行）
- 源文件路径：papers/arxiv/2208.00836/content.md（全文已落盘 §7.2 核查 PASS）
- **发表状态**：正式发表（IEEE JLT 2022）
- **发表渠道**：IEEE Journal of Lightwave Technology（SCI Q1 Trans）
- 年份：2022
- 核心贡献：实验验证 SIC（successive interference cancellation）MIMO 解码算法在 MDM FSO 中的湍流鲁棒性增强。提出 carrier-asynchronous DSP 结构，分离 MIMO 解码器与相位估计/信道估计/ISI 均衡 [content.md L71]
- 方法概述：
  - SIC 逐通道顺序解码，解码第 k 通道前减去已解码前 k-1 通道的干扰贡献（ỹ_k = y - Σĥ_i·s̃_i）[L89-90]
  - 减除后用修改版 MMSE 接收器 [L93-94]，最优解码序排列抑制误差传播 [L91]
  - 比 MMSE 多利用自由度（第 k 通道可用 k 维正交补 vs MMSE 的 1 维），SINR 更高 [L107]
- 实验设置：实验 + SLM 仿真湍流（von Kármán 相位屏，~400-500m 信道）。5 个发射空间模式（LP 模）× 双偏振 = 10 通道；接收 6-mode MSPL 最多 12 通道。DP-QPSK 34.46 GBaud，线速率 689.23 Gbit/s。强湍流 r₀=0.8mm（D/r₀=10.5）/ 弱 r₀=3.0mm（D/r₀=2.8），各 120 相位屏 [L31/L51]
- 使用的 Baseline 方法：
  - **MMSE MIMO 均衡器**：传统线性 MIMO 解码 [L17]。弱湍流 penalty ~4.2dB vs SIC ~3dB；强湍流 MMSE 未达 HD-FEC 限 vs SIC ~6.9dB [L139]
- 关键结论：120 强湍流样本平均 BER MMSE 8.02×10⁻³ → SIC 4.76×10⁻⁴ [L157]；outage 概率 48.3% → 2.5% [L161]。6×12 配置更优：BER 1.56×10⁻⁴→2.86×10⁻⁶，outage 1.67%→0% [L173]
- 与本研究关系：**⚠ 边界 PASS 但场景架构不匹配**——见下"场景适配"
- 实现关键细节：carrier-asynchronous DSP 结构 [L71]；RRC 滚降 0.1；训练序列 1680 符号；导频每 9 数据符号 1 个 [L31]；50 GSa/s / 23GHz 示波器 [L35]
- 开源代码：无
- 验证状态：全文已 §7.2 核查（信号域/inter-mode/MDM/MMSE 增益全 PASS）

#### 边界判定（最高优先级）

**PASS —— SIC 属信号域（均衡层 IN），非载波同步层**

论文显式提出 carrier-asynchronous DSP 结构"**separate the MIMO decoder from the phase estimation, the channel estimation, and the ISI equalization**" [L71]。载波相位 Φ 由独立 phase estimation 模块处理 [L69-75]；SIC 是其下游的信号域 inter-mode crosstalk 消除。**不撞载波同步红线**。

#### 场景适配性分析

**⚠ 架构不匹配（非边界问题，是场景问题）**：
1. **SIC 处理 inter-mode crosstalk**（多模 MDM 模间串扰），依赖 N_r ≥ N_t 冗余接收通道分集 [L19/L109]
2. 本场景**单偏振单孔径单模式** → **无多模式 → 无 inter-mode crosstalk → SIC 无可消除对象**
3. 湍流在 MDM 中致 inter-mode crosstalk [L13]；在单模中致 scintillation / beam wander / phase fluctuation [L13]——**机制不同构**（空间域串扰 vs 标量幅度/相位起伏）
4. **降级参考**：SIC 对单模场景无可迁移性（需要多模冗余通道前提）

#### 问题提取（M-C-A）

- **M（方法）**：SIC MIMO 解码（逐通道顺序解码 + 干扰消除）
- **C（条件）**：MDM FSO 多模链路（5模×双偏振），相干 DP-QPSK，GG 湍流致 inter-mode crosstalk
- **A（失效原因）**：MMSE 在 fading 信道（信道矩阵非酉）性能退化 [L17]，SIC 利用冗余自由度提升 SINR
- **四判据初筛**：矛盾✅(MMSE 失效) / 形态✅(SIC) / 2019+ baseline✅(MMSE JLT) / 能对比✅ —— **但场景 out（单模无 inter-mode crosstalk）**

---

### [L05] Digital Turbulence Compensation of FSO with Multimode Optical Amplifier（Fontaine 2019 ECOC）

- DOI/来源：10.1049/cp.2019.1015（**ECOC 2019 会议，paywall 仅 abstract**）
- 源文件路径：**无全文**（abstract 来自 search-archive/2026-07-10/fontaine-multimode-digital-coherent-reception-turbulence-com.json）
- **发表状态**：正式发表（ECOC 2019 会议论文）
- **发表渠道**：European Conference on Optical Communication（顶会，但会议非 Trans）
- 年份：2019
- 核心贡献：用 12-spatial mode 数字相干接收 + 多模预放做数字湍流补偿，称"≈ ideal lossless AO" [abstract]
- 方法概述：12 模数字相干叠加补偿湍流。多模预放提供 6dB 灵敏度提升 [abstract]
- 实验设置：**abstract 仅**，细节未核验
- 使用的 Baseline 方法：传统单模检测 [abstract]
- 关键结论：12 模相干叠加将中位 BER 从 0.1 降到 1×10⁻⁵ [abstract]
- 与本研究关系：**⚠ 多模架构不匹配**（同 Li 2022，需多模冗余通道）+ **会议非 Trans**（INVARIANT 19 红线：会议不当主 baseline）
- 实现关键细节：abstract 未给（全文 paywall）
- 开源代码：未知
- 验证状态：abstract 已核验（关键声称全在 abstract 文本中）

#### 场景适配性（abstract 层）

**⚠ 双重不匹配**：
1. **多模架构**：12-spatial mode 数字相干，需多模接收——本场景单模单孔径
2. **会议非 Trans**（INVARIANT 19 红线）：ECOC 会议，不能当主 baseline，只能当思路来源（DSP 替代 AO 概念）

---

### [L06] Electronic Wavefront Correction for PSK FSO（Kim 2007 EL）

- DOI/来源：**未找到**（Electronics Letters 2007，S2/blit 均未召回，19 年老文）
- 源文件路径：**无**（landscape #38 标"abstract 缺失，老文"）
- **发表状态**：正式发表（Electronics Letters，Letters 级）
- 年份：2007
- 核心贡献：**相干检测 + DSP 替代 AO 校正波前畸变**（奠基概念），10Gbit/s BPSK 实验 [landscape #38]
- 方法概述：landscape 转述——DSP 电子域校正波前，替代光学 AO 硬件
- 与本研究关系：**奠基概念参考**（DSP 替代 AO），但 **Letters 级 + 19 年老文 + abstract 缺失**，按 INVARIANT 19 不当主 baseline
- 验证状态：**未核验**（论文未下到，信息全部来自 landscape 转述，标"二手 landscape"）

---

## 综合分析（AO-DSP 残余补偿子地带，批次 2）

### 1. 现有方法分类

AO-DSP 残余补偿子地带分三支（landscape §子地带 7 已分，精读后细化）：

| 类别 | 方法 | 代表 | 边界判定 | 场景适配 |
|---|---|---|---|---|
| **A 分工式**（AO 校正 + DSP 补残余） | AO + 数字 PLL | Paillier 2020 JLT (#34) | ❌ **载波 PLL 排除** | — |
| **B 替代式**（DSP 替代 AO 硬件） | 多模数字相干叠加 | Fontaine 2019 ECOC (#37) / Kim 2007 EL (#38) | ✅ 信号域 | ⚠ 多模架构不匹配 |
| **C MIMO 解码式**（DSP 消 inter-mode crosstalk） | SIC / MMSE MIMO | Li 2022 JLT SIC (#40) | ✅ 信号域 | ⚠ 多模架构不匹配 |

**关键发现**：AO-DSP 子地带的信号域论文（B/C 支）**全是多模架构**（MDM/multi-mode），依赖多模冗余通道。本场景**单偏振单孔径单模**，无 inter-mode crosstalk → B/C 支无可消除对象。**A 支（Paillier 载波 PLL）按红线排除**。

### 2. 已知局限

1. **AO-DSP 信号域 baseline 全是多模架构**：Li 2022 SIC（MDM 5模×双偏振）/ Fontaine 2019（12模数字相干）/ Kim 2007（波前校正）。单模场景无可迁移性
2. **Paillier 系（A 支）按载波边界排除**：DSP 段余 = 载波 PLL，不是均衡层
3. **多模 vs 单模的机制差异**：多模中湍流致 inter-mode crosstalk（空间域串扰，SIC 可消）；单模中湍流致 scintillation（标量幅度衰落，无空间域串扰可消）

### 3. baseline 凑池可行性评估（D004 筛选判据 A）

**❌ 凑不齐 D-010 标准 4 篇 Trans**：
- 信号域论文全是多模架构（Li 2022 JLT SIC ✅ Trans 但场景 out / Fontaine 2019 会议非 Trans / Kim 2007 Letters 老文）
- 单模场景适配的 AO-DSP 信号域 Trans baseline **零篇**
- Paillier 系（唯一单模星地 Trans）按载波边界排除

---

## 两子地带对比总结（ISI + AO-DSP，交阶段 2.5 矩阵 + 阶段 3 判读）

> **守 INVARIANT 6 + D018：不判 Go/Kill 不判地，只产观察 + Q# 候选。**

### 对比表

| 维度 | ISI 均衡（批次 1） | AO-DSP 残余补偿（批次 2） |
|---|---|---|
| **边界** | ✅ 不撞载波（信号域时域均衡） | A 支❌载波PLL排除 / B+C支✅信号域 |
| **场景适配** | ❌ Ajam PD/IM-DD + IRS 几何双重不匹配 | ❌ B+C 支全多模架构（单模无可消对象） |
| **baseline 凑池** | ❌ 凑不齐（Ajam 1篇PD+paywall，光纤迁移全paywall） | ❌ 凑不齐（信号域全多模，单模适配 Trans 零篇） |
| **物理前提** | ⚠ **晴空湍流致 ISI 未被主流文献建立**（sat.1553 口径：标量衰落无时域展宽） | ⚠ 多模 inter-mode crosstalk 机制成立，但单模不适用 |
| **B7 风险** | 高（解决不存在的问题——晴空湍流可能不致 ISI） | 中（多模机制真实，但单模场景不匹配） |
| **Q# 候选** | 4 条（Q1-Q4，共同硬伤 baseline❌） | 见下 |

### AO-DSP 子地带 Q# 候选（初筛，≥3 条）

| Q# | 问题（M-C-A） | 四判据初筛 | 来源 |
|---|---|---|---|
| **Q5** | 单模星地相干下，**DSP 替代 AO 校正波前畸变**（Kim 2007 概念迁移到单模 intradyne）可行性？M=电子波前校正 DSP，C=单模 intradyne 相干 + GG 湍流，A=AO 硬件复杂/慢 → DSP 替代。**但 Kim 2007 是 Letters 老文 abstract 缺失，机制待证** | 矛盾❓/形态✅/baseline❌(Kim Letters老文)/对比❌ | Kim 2007 |
| **Q6** | SIC/MIMO 解码从多模迁移到**单模 + 多时间采样**（用时间分集替代空间分集）？M=时域 SIC，C=单模 + 多时间窗，A=**待证**（时域分集能否替代空间冗余） | 矛盾❓/形态✅/baseline❌/对比❌ | Li 2022 迁移 |
| **Q7** | AO 校正后残余 piston 相位在**高阶调制（16-QAM）**下是否需信号域补偿（非载波 PLL）？M=信号域残余补偿，C=16-QAM + AO 校正后，A=Paillier 证 BPSK 下 DPLL 够用，16-QAM 边界待证。**但撞载波边界风险**（残余相位本质是载波域） | 矛盾✅/形态✅/baseline❌/对比❌ + ⚠边界 | Paillier 笔记 |

**Q# 初筛观察（守 D018）**：
- AO-DSP 3 Q# 共同硬伤：2019+ baseline ❌ + 场景架构不匹配（全多模，单模零适配 Trans）
- Q7 撞载波边界风险最高（残余相位本质是载波域，Paillier 已证 BPSK 够用）

### 两子地带共同结论（诚实，守 D018 不 Kill）

**两子地带都 baseline 凑不齐 + 场景不匹配**：
1. **ISI**：Ajam PD/IRS 双重不匹配 + 晴空湍流致 ISI 物理前提存疑
2. **AO-DSP**：信号域全多模架构（单模零适配）+ Paillier 系载波边界排除

**D004 筛选判据二选一的结果**：
- 判据 A（baseline 凑池）：**两子地带都 ❌**（D-010 标准 4 篇 Trans 凑不齐）
- 判据 B（缝潜力）：**两子地带 Q# 共同硬伤 = 2019+ baseline ❌ + 场景不匹配**
- 判据 C（范围 in）：ISI ⚠（晴空湍流致 ISI 物理前提待证）/ AO-DSP ⚠（多模 vs 单模）

**⚠ 颗粒无收倾向（守"颗粒无收好过凑数"原始目标）**：在已读材料范围内，两子地带都**凑不齐 baseline + 场景不匹配 + Q# baseline 判据普遍 ❌**。但这不是 Go/Kill 结论（守 D018），是**阶段 2 精读的诚实观察**。阶段 3 判读需回答：
1. ISI：晴空 GG 湍流是否真致时域 ISI？（物理前提判定，补查湍流信道 CIR 文献）
2. AO-DSP：单模场景有没有信号域残余补偿的真问题？（多模机制不迁移）
3. 两子地带都不行 → 均衡层换其他子地带（OFDM-FSO? DNN?）还是颗粒无收？

---

> **下一步**：阶段 2.5 方法-改进矩阵（INVARIANT 20，横向汇总）→ 阶段 3 判地三轴
