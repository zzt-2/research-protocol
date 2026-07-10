# 文献调研记录 — 星地湍流信道激光通信处理技术

> 硕士论文"星地湍流信道激光通信处理技术研究"
> 本文件 = GW Step 3 精读 + 综合分析产物（块 A 7 篇 + 块 B 补 6 篇，去重后 10 篇有效候选）。
> **路线**：D005 务实路线（Go=赢传统未优化 baseline 几 dB；FR-21 oracle 上界降级为参考；底线守四判据不可放水 / 不接受孤证标题联想）。
> **对手标准**：D004-a 传统未优化 baseline（不是 oracle 上界），跟同门学位论文套路对齐。
> **精读笔记溯源**：每篇详细结构化提取（14+ 字段 + 7 子表）见 `papers/_read_notes/{paper_id}.md`，`read-log.md` 有索引。
> **历史**：本文件前身为 2026-05-29 Step 1 检索时代版本（旧三章 Ch2/3/4 列表式），R001/D003 方法论起点校正后 Step 3 重走"地勘→选样→精读→综合分析"流程，本版 = 旧版完整重写（旧方向已被 D005 翻转，旧 Ch2-4 三章分法作废）。

## 调研概况

- **研究方向**：星地激光通信（标题对得上即可，湍流可去，处理技术取宽义）下的信号/信道/检测处理技术
- **检索工具**：tools/search（Semantic Scholar/OpenAlex）+ tools/blit（IEEE，Playwright 走系统代理）
- **检索关键词**（块 A + 块 B 补，H004/H005）：方案 A 8 词（Doppler/均衡/载波恢复/估计/PS/符号率/feeder/LEO downlink 等）+ landscape 主表（683 条，S004-S010 五轮地勘）选样
- **核心文献数**：10 篇精读（6 篇四判据全过 + 4 篇部分不过作方法借鉴）
- **调研日期**：2026-06-26（块 A 7 篇 + 块 B 补 6 篇同日完成）

## 步骤进度

| Step          | 状态 | 完成日期 | 备注 |
| ------------- | ---- | -------- | ---- |
| 1 检索        | ✅   | 2026-05-29 + S003-S010 地勘五轮 + **2026-07-10 双偏振 OSL 15查询穷举** | 早期 21+6 条 + 地勘 683 主表 + 双偏振 43 核心候选 8 子方向 |
| 2 获取        | ✅   | 2026-06-26 + **2026-07-10 双偏振 9篇+sat.1553** | H004 块 A 7 篇 + H005 块 B 6 篇 + 双偏振 9 篇成功(download+blit 两轮) |
| 3 精读        | ✅   | 2026-06-26 + **2026-07-10 双偏振 9篇+sat.1553§6补读** | 块 C 10 篇 + 载波同步 v2 35 Q# + **双偏振 9 篇+角度素材 schema 试用+3 Q#(Q-DP1/2/3)** |
| 3.5 补充      | 🔄部分 | 2026-06-27 + **2026-07-04 载波同步 v2 精读沉淀补强** | 检索✅+召回Q11-Q13✅，下载精读债务（Paillier2020JLT/Rustum2026/Tang2024/Mosnier2025/Viterbi1983）+ **B 档 12 候选精读沉淀补强（B1-B12 每点 ≤5 篇 cited-by + gw-read 14 字段+7 项笔记 + 35 Q# 过四判据，详见"载波同步 v2 精读沉淀"节）**| 块 D：盲区A/B定向补检索 + 召回旧B1资产 + **载波同步 v2 判读层 D017/D018 补强（专题 2026-07-02-carrier-sync-v2-deep-read）**|
| 4a 可行性     | 🔄部分 | 2026-06-28 | 块 E：每个 Q# 走 gw-feasibility A0/A'/A/B/D。**Q12 Kill(D006) / Q8切入点2 Kill(S017) / Q8切入点4B Kill(D008) / Q1 Kill(D010)**。暂 0 Go。待评：Q8切入点1/Q2/Q3/Q7/Q10 |
| 5 Baseline    | ⬜   |          | 块 F：Go 的 Q# 进 baseline 复现 |
| 4b 仿真可行性 | ⬜   |          | |
| 6 仿真器      | ⬜   |          | |
| 7 验证        | ⬜   |          | |

---

## 综合分析

### 现有方法分类

10 篇按技术路线分 5 类（每类含具体方法名）：

1. **载波恢复/频率估计（4 篇，主热区）**：两阶段 KF 递归估计（TS-KF, OE 2025 #1，状态 [ω,ϕ] 双 Q 解耦捕获/锁定）、二阶 DPLL+前馈级联（CPR 北理工, Electronics 2025 #2，Kd=4，ωn=20 Mrad/s，N=64 块平滑）、DSP 辅助 AFC 闭环（BUPT 2025 新1，CFR 前馈→LO 激光器粗调，±8GHz 跟踪）、联合自适应 PCS+符号率（JLT 2023 新4，Rs+H 联合调度）。共同范式：解耦"大范围捕获"与"精修锁定"两阶段，对抗 LEO 高动态多普勒（10-15 GHz 突发 + MHz/s 漂移）。

2. **均衡/检测（3 篇）**：adaptive MMSE for time-packed M-PAM（GC 2020 #3，LMS 自适应，唯一无 error floor）、多格式 data-aided DSP 均衡管线（WiSEE 2024 #6，两级 CFO+OFDM-MIMO 信道估计+两级 CPE，格式无关，开销 7.75%）、双偏振自相干三 PD 偏振解复用（ACCESS 2025 新3，1×3 PBS 解 H_eff 奇异）。共同范式：用训练/冗余/结构化接收换低 SNR 鲁棒性。

3. **概率整形（3 篇，⚠️ N1 同构风险）**：PS+符号率联合治 Doppler（JLT 2023 新4，PS 作使能件，增益来自 Rs 适配，**不同构 N1**）、PS+残余载波调制治湍流（LPT 2025 新5，RCM 相位共轭 + PS 抗幅度闪烁，**部分同构 N1**，PS/RCM 消融不全）、PS-QAM Gamma-Gamma 理论（Appl Sci 2021 新6，PMF 优化 + PEP 闭式，**高度同构 N1**，高 SNR>16dB uniform 反超 PS）。共同范式：用非均匀 PMF 逼近 Shannon 限抗低 SNR/闪烁。

4. **信道估计（1 篇，跨类）**：#6 data-aided 多格式 DSP（与均衡跨类，OFDM-MIMO ZF/MMSE 4000 符号训练估 θ）。

5. **检测架构（1 篇，跨类）**：#新3 三 PD 自相干（含光学架构 + DSP 偏振解复用，跨均衡/检测）。

### 已知局限（领域级空白原料，**非问题**，须经 Q# 转译）

> 注意：本节按 glossary.md 是空白（领域级新颖性原料），不能直接当研究起点。

10 篇的共同不足：

1. **场景缩窄与链路类型不匹配**：多篇用简化场景（#1/新2 真空星间无湍流、新5 地面短距 3km 等效、新3 35000km GEO 非 LEO、#6 3.2km 城市地面）。星地 LEO + 湍流 + Doppler 三者联合的端到端验证稀缺。

2. **PS 方向"增益趋零"陷阱**：纯 PS 整形增益在高 SNR 趋零（新6 L562 "16dB 后 uniform 反超"，新5 L205 "approaches uniform"），与已 Kill 的 N1（固定信道 PS gain≈0）同构。只有 PS + 另一具体机制治具体失效（如新4 符号率适配、新5 相位共轭）才有戏。

3. **baseline 不对称/缺直接 BER 对标**：#6 无与竞争性单格式 DSP 直接 head-to-head BER 曲线（C⚠️）、新1 无 BER-vs-baseline（C❌D❌，仅绝对灵敏度+资源表）、新5 无具体 dB 增益数字（D⚠️，仅 SD-FEC 阈值定性）。

4. **统计严谨性普遍不足**：10 篇无一报告 seeds 数、error bar、统计检验；多数单次仿真曲线。新2/新6 无 UQ。这是领域惯例（也是盲点，gw-read 实验完备性提取已记录）。

5. **实时性/工程落地缺口**：仅 #2（FPGA）和新1（FPGA 实时）有硬件验证，其余纯仿真。D005 务实路线下不强制硬件，但工程落地是未来工作高频项。

6. **湍流 + Doppler 联合建模缺失**：#1 假设真空无湍流、新2 真空、新4 Doppler 真实但湍流 Gamma-Gamma 数值叠加（非真实大气）、新3 准静态偏振假设。无一篇做湍流相位闪烁 + Doppler 频移的联合实时补偿。

### 2-3 年趋势

从发表年份（2020-2025）和方法演进推断：

1. **全数字 DSP 替代光学硬件**：新4（JLT 2023）明确论证"even if f_DS can be estimated and removed digitally, the baseband signal has already been subject to asymmetric electrical filtering"——倾向用全数字 DSP（Rs/PS 自适应）替代 OPLL/OIL 光学硬件应对 Doppler。#1/新1 沿此路线。

2. **多阶段解耦捕获-锁定**：#1（TS-KF 两子块 Q1/Q2）、#2（DPLL+前馈）、新1（CFR 粗调+四次方精调）、新2（粗 CFE + M-th power 精 CFE）——2023-2025 年多篇都采用"粗补偿大范围 + 精补偿锁定"两阶段结构，是领域主流范式。

3. **PS 作为使能件而非核心**：新4（2023）已把 PS 降为"单参数控熵以联合 Rs 保持固定比特率"的 enabler，核心创新转 Rs 适配。这预示纯 PS 增益方向（如新6）在领域内已被视为饱和/同构，PS+机制才有新意。

4. **自相干检测 + 数字偏振解复用兴起**：新3（2025）三 PD 方案消除两 PD 奇异，是 2024-2025 年自相干方向新进展（比 coherent 低复杂度，比 IM/DD 高灵敏度）。

5. **实时 FPGA 验证成为强信号**：#2（2025 FPGA）、新1（2025 FPGA）都在 2025 年补 FPGA 实时验证，预示领域对纯仿真可信度的要求在提高。

### 研究背景概述

**时间线脉络**：

- **2010s-2020**：经典 DSP 方法（Viterbi-Viterbi CPR、Diff-4th、Costas loop、OPLL）主导，但 LEO 高动态多普勒（±GHz 级 DFS）开始暴露传统 CFR 范围不足（±Rs/2 ≪ GHz）。Time-packing 检测（#3 GC 2020）开始系统对比 linear/MLSE。
- **2021-2023**：PS 概率整形从光纤移植到 FSO（新6 Appl Sci 2021 PS-QAM 理论、新4 JLT 2023 PCS+Rs）。两阶段 CFE（新2 ACCESS 2023）扩展 DS 补偿范围。
- **2024-2025**：①实时 FPGA 验证成主流（#2 CPR 北理工 2025、新1 BUPT 2025 Doppler 跟踪）；②自相干 + 数字偏振解复用兴起（新3 ACCESS 2025）；③多格式 data-aided DSP（#6 WiSEE 2024）抗低 SNR。

**核心技术挑战**（从 10 篇精读归纳）：

1. LEO 星地链路 Doppler 频移大（±15GHz 突发）、变化率高（MHz/s 量级）、且与 ADC/TIA 带宽限制耦合产生非对称电滤波惩罚。
2. 大气湍流致幅相联合损伤（Gamma-Gamma 强度闪烁 + Kolmogorov 相位畸变），且偏振旋转可能致检测奇异（新3 θ=45°）。
3. 低 SNR（接收功率 ≤−39 dBm）下传统前馈 CPR（Diff-4th/VV-BPS）因 cycle slip 产生突发错误，BER→0.5。
4. 高阶调制（16-QAM）+ 高动态 + 湍流三者联合下，单一固定参数方案难覆盖所有工况。

**本研究定位**（务实路线 D005）：在星地激光通信处理技术大背景下，找"现有传统未优化方法 M 在具体条件 C 下因假设 A 不够好"的改进空间，产出能赢传统 baseline 几 dB 的方法（跟同门王培森 NOMA 4.5dB / 李兀祺扩频 0.25-4dB / 弱信号同步 −2.8~−10dB 套路对齐）。具体子方向待块 E Go/No-Go 定。

### 研究问题清单 Q# [MUST]

> 问题定义见 `stages/glossary.md`（问题 = "现有方法 M 在条件 C 下因假设 A 失效/不足"，四判据）。
> 本表是 Contract Step 1 假设的**唯一合法引用来源**。
> **判据 A（D005 修正）**：不再要求"baseline 致命失效"，改为"baseline 在具体条件下不够好 + 有改进空间"。
> **链路匹配标注**：标题"星地"为范围约束（topic-index 不变量 6）。出范围的链路（星间 LEO-LEO / 地面短距）单独标 ⚠️链路。
> 6 篇四判据全过（#1/#2/#3/新2/新4/新6）来自 H005 候选池判定，4 篇部分不过（#6/新1/新3/新5）列 Q# 但标 ❌ 记录筛掉理由（防复现，glossary.md 常见误用 1）。
> **块 D 召回（2026-06-27）**：Q11/Q12/Q13 是旧 B1 方向资产召回（H004 选样漏召纠正），笔记源于 2026-06-16，D005 务实标准下重评。

| Q#   | M（失效/不足的现有方法） | C（条件） | A（失效假设） | 方法产出形态 | 判据1 矛盾 | 判据2 产出形态 | 判据3 近期baseline | 判据4 可量化对标 | 四判据 | 来源 |
|------|------|------|------|------|------|------|------|------|------|------|
| Q1 | 单阶段 KF / VV-BPS（固定单一 Q 配置） | LEO-LEO 相干 ISL，突发达 10 GHz + 慢漂 151 MHz/s，OSNR 18 dB | 单一 Q 不能同时兼顾"捕获期突发快变"（需大 Q）和"锁定期精调相位"（需小 Q 固定 ω）；VV-BPS 在 5/10GHz 突发下无法解调 | 递归 DSP 估计器（两阶段 KF + 参数设计准则） | ✅ M/C/A 明确 | ✅ 算法+准则 | ✅ VV-BPS（自实现同平台）+ Tang 2023 | ✅ BER-vs-OSNR、复杂度 ratio | **❌ Kill（D010，2026-06-28）**：范围双重出界（不变量6星地 + S007 ISL排除 + 真空无湍流）+ A1 方法归属错位（产出形态=论文自己的 TS-KF）+ C3 堵死抢救（搬星地撞 Q12/B1 换皮 D006）。A2 在 Q1 自身 ISL 场景反而过（Doppler 真硬动态）。**论文 TS-KF 降级 baseline 参考**（未来星地 Doppler 对照）。详见 decisions.md D010 | #1 §L131-135 |
| Q2 | Diff-4th（differential fourth-power）全前馈 CPR | 星间相干低 SNR（Eb/N0≤5.2 dB / ≤−39 dBm） | 全前馈平滑在低 SNR 下因 phase cycle slip 产生突发错误，D(Δθ̂) 超阈值，星座旋转 BER→0.5 | CPR 算法（二阶 DPLL+前馈级）+ ωn-N 选型准则 | ✅ M/C/A 明确 | ✅ 算法+准则 | ✅ Diff-4th[Leven 2007/Huang 2012/Tang 2023]（自实现） | ✅ LRMSE↔MCRLB、BER、复杂度三维 | **❌ Kill（D011，2026-06-28）**：死因=D010/Q1复刻——范围双重出界（不变量6星地+S007 ISL排除+无湍流）+ A1方法归属错位（产出形态=论文自己的二阶DPLL+前馈）+ C3撞Q12/B1换皮（KF替代loop filter搬星地=D006）。论文降级**方法借鉴+同实验室前作**（二阶DPLL+前馈结构/ωn-N准则可复用）。**登记「16-QAM CPR扩展」为待回看种子**（Q2自承仅QPSK未扩展16-QAM，未被D006堵死，留Step4a全评完后独立评估）。详见 decisions.md D011 | #2 §L39-40/278-284/371 |
| Q3 | 受限复杂度 Viterbi（Ns=4096）/ truncated MMSE（信道截断） | 光 feeder link IM/DD，time-packed M-PAM（M≥4，重叠 δ≥0.25） | 检测器复杂度受限 → 残余 ISI 无法消除 → error floor（Viterbi 受 trellis states 截断、truncated MMSE 受信道截断） | low-complexity linear detector 配置准则 + 性能曲线族 | ✅ M/C/A 明确 | ✅ 准则+曲线族 | ✅ M-PAM without overlapping(δ=0) + Viterbi[8/7]+MMSE[14]（自实现） | ✅ BER-SINR + throughput-cloud attenuation 曲线族 | **❌ Kill（D012，2026-06-28）**：范围双重出界（feeder系统级撞S007 + 无湍流建模，feeder辨析物理经大气但S007排系统级架构）+ A1方法归属错位（产出形态=论文自己的adaptive MMSE）。**C3未撞旧Kill**（Q3跟Q1/Q2唯一差别）但不构成salvage（A1+范围已双重硬门槛）。论文降级**方法借鉴**（time-packing+MMSE检测框架+SINR-BER闭式可复用）。详见 decisions.md D012 | #3 §L235/237 |
| Q4 | CMA 盲均衡 / BPS（单格式 DSP 管线） | 低 SNR 多格式（DP-4QAM 100Gb/s / DP-16QAM 200Gb/s）星地相关 FSO | 盲均衡与调制格式耦合，低 SNR 下失效；单格式管线无法跨格式复用 | 经典离线 DSP 均衡器算法（多格式 data-aided） | ✅ M/C/A 明确 | ✅ DSP 管线 | ⚠️ CMA/BPS 仅概念论证**无直接 head-to-head BER 对标**（仅内部 ZF/MMSE + AWGN 理论） | ✅ outage 阈值（仿真 0dB/实测 −1.2/−1.8 dB） | **未过**（C⚠️缺直接对标）作方法借鉴 | #6 §L29/113 |
| Q5 | 传统 VV 单四次方 CFR（固定 ±Rs/2 范围） | LEO 星地，高 DFS（±8 GHz，33-120 MHz/s），功率波动≥20dB | ±Rs/2（1.25GBaud 时 ±625 MHz）≪ GHz 级 DFS；ADC 带宽太窄无法过 GHz 偏移信号 | DSP 算法（实时 FPGA）+ 系统设计（AFC 闭环） | ✅ M/C/A 明确 | ✅ 算法+系统 | ❌ **无 BER-vs-baseline**（仅绝对灵敏度+资源表+定性） | ❌ 无 BER-vs-baseline 曲线 | **未过**（C❌D❌）作方法借鉴（BUPT 同国别，闭环 AFC 架构可复用） | 新1 §I/II |
| Q6 | 两 PD 双偏振自相干检测 | 星地/地星/星星 FSO，35000km，大气湍流致偏振旋转 θch | H_eff,2PD 在 θ=45°/135°/225°/315° 奇异（eq18），退化为单方程两未知，BER>0.1 | DSP 算法（信道估计/均衡/偏振解复用）+ 光学架构（三 PD） | ✅ M/C/A 明确 | ✅(部分) DSP 成分达标，含光学架构硬件改动 | ✅ DP-coherent（自实现同链路）+ 两 PD 自实现 | ✅ BER-vs-OSNR、BER-vs-透镜直径、BER-vs-旋转角 | **部分过**（B 部分）⚠️链路（GEO 非 LEO）作机制借鉴 | 新3 §III.B.2/D |
| Q7 | M-th power 单阶段 CFE（范围 = Rs/(2M)） | LEO-LEO OISL，DS 高达 10GHz，Nyquist 整形+过剩带宽，32GBaud PM | M=4 时 10GHz DS 需 80-GBaud 接收机（高于卫星预期）；过剩带宽增噪声损害 16-QAM（1.2dB 损耗） | DSP 算法（modified 两阶段 receiver）+ 系统可行性分析 | ✅ M/C/A 明确 | ✅ 算法+分析 | ✅ evaluated receiver[50]（Diniz 两阶段，自实现，1.2→0.9dB） | ✅ dB 损耗、SNR margin、补偿范围 ≥13GHz | **全过** ⚠️链路（LEO-LEO 星间真空，非星地） | 新2 §VI/VII |
| Q8 | 固定 80 Gbaud（不调符号率） | LEO-to-Earth 500km 星地 FSO，Doppler ±15GHz + Gamma-Gamma 湍流 | 固定 Rs 下 Doppler 使信号谱偏离基带被 TIA/ADC 单边滤除（非对称电滤波惩罚），即使数字估出 f_DS，baseband 信号已被硬件滤损 | DSP 自适应调制算法（Rs+H 联合调度查表，全数字无硬件改动） | ✅ M/C/A 明确 | ✅ 算法 | ✅ 固定 80Gbaud（自实现同链路同硬件） | ✅ ±15GHz 极端 Doppler 下 ABR ~600Gbps（vs 固定 ~100Gbps 增益） | **全过** ⚠️增益来自 Rs 适配**非 PS**（PS 在 proposed/baseline 都用，不同构 N1）⚠️FEC 假设理想 | 新4 §L145-173 |
| Q9 | 无相位补偿系统 / KK 接收机（依赖高功率 DC） | FSO 湍流信道（Gamma-Gamma 幅度 + Kolmogorov 相位） | KK 依赖 high-power DC 致 carrier power loss + 半频谱效率；无相位补偿下强湍流 BER 急剧恶化 | DSP 相位共轭补偿 + 调制器偏置配置（RCM，无新硬件） | ✅ M/C/A 明确 | ✅(DSP 成分) + RCM 半硬件 | ✅ 无相位补偿基线（自实现）+ uniform 对照 | ⚠️ SD-FEC 阈值对标有，**无具体 dB 增益数字**（定性低于阈值） | **未过**（D⚠️）⚠️部分同构 N1（PS 高 SNR 趋零）⚠️链路（地面短距非星地）作方法借鉴 | 新5 §L113-141/187/205 |
| Q10 | uniform QAM（固定均匀分布） | 相干 FSO Gamma-Gamma 湍流信道（低 SNR 段） | 固定均匀分布在低 SNR 远离 Shannon 容量（Shannon gap 大） | 编码调制方案（PMF 优化 + LDPC）+ 解析工具（PEP 闭式） | ✅ M/C/A 明确 | ✅ 方案+闭式 | ✅ uniform + MB 分布（自实现，同 16QAM/同 LDPC/同 GG） | ✅ 0.4dB(AIR)/1.3dB(post-FEC) | **全过** ⚠️**高度同构 N1**（高 SNR>16dB uniform 反超 PS 趋零，固定信道 gain≈0）⚠️纯仿真无硬件 | 新6 §L560/562 |
| Q11 | 固定参数 Z 变换 ODPLL（只建模多普勒相位斜坡 φ_D） | 星地 LEO 下行（419km）+ 高 Doppler rate（85 MHz/s）+ 大气湍流 | PLL 环路闭环传递函数 H(z) 只含多普勒残频激励，**不含湍流相位噪声 φ_T(t)**；用 1kHz-1MHz 正弦近似衰落（非 Gamma-Gamma/Rytov 真实统计），湍流相位扰动未建模 | DSP 联合建模方法（H(z) 扩展为 φ_D(t)+φ_T(t) 双激励输入）+ 稳态相位误差方差/失锁概率分析 | ✅ M/C/A 明确 | ✅ 模型+分析 | ✅ Pech 2025 单激励 ODPLL（自实现同链路）+ Paillier 2019 DPLL 分治架构 | ⚠️ Pech 2025 自身无数值 BER 曲线（仅 XOR 误差清零定性）+ 无 phase error variance 数值 | **部分过**（D⚠️ baseline 自身量化弱）⚠️旧 B1 方向（曾判"勉强>常识重做"，D005 下作 baseline 重评） | Pech2025 §L357 + Paillier2019conf §L55/75 |
| Q12 | 分治架构（AO 管湍流光域 + DPLL 管多普勒数字域，环路内不含湍流相位） | 星地 LEO 相干下行 + 大气湍流（Gamma-Gamma + 相位畸变）+ Doppler 残频（30-300 MHz） | 分治假设"AO 完全校正湍流振幅+相位、AGC 维持恒幅、DPLL 只管多普勒残频"——湍流相位被推给 AO 不进 PLL 环路传递函数 | DSP 联合建模方法（PLL 环路内联合 φ_D+φ_T）vs 分治架构对比 + AO 残差进环路的扰动建模 | ✅ M/C/A 明确 | ✅ 对比框架 | ✅ Paillier 2019 conf + **Paillier 2020 JLT（companion[9]完整版，端到端数值湍流仿真，证明分治够用）** | ✅ pull-in time、相位误差方差 vs CRB、BER penalty（湍流致 2.3dB）、AO penalty（-4.5dB）全量化 | **全过** ⚠️**JLT 版条件性细化（2026-06-27 块D精读）**：Paillier 证明"湍流相位对载波同步可忽略"但**依赖特定条件**（BPSK+10GBaud+理想timing+AGC恒幅+AO校正后piston相位~1ms慢于符号率）。**gap 修正**：不是"领域没人做联合建模"，是"Paillier 分治够用是条件性的，换条件（高阶调制/低SNR/无理想timing/强湍流快piston/上行链路）可能不成立"→ **潜在务实切入点（D005）：针对 Paillier 假设不适用的条件做改进，赢其分治 baseline 几 dB** | Paillier2019conf §L56-62 + **Paillier2020JLT §L195/205/189（companion完整版）** |
| Q13 | （综述级证据，非单一方法 Q#）现 OSL DSP 算法地图中"湍流仅作 SNR 分布参数，无湍流相位专用 DSP 模块；多普勒与湍流补偿在流水线中独立不交互" | OSL 全场景（ISL/下行/上行强弱湍流） | 综述假设"信道准静态"，湍流相位扰动未建模（相位噪声专指激光线宽）；前馈载波恢复（VV+CFO）分治处理，无联合算法 | — | ✅ 综述级 gap 证据 | N/A（综述非方法产出） | ✅ Valjus 2025 综述本身 + 4 场景 SNR penalty 全量化 | ✅ 4 场景 SNR penalty(dB) @ BER 1e-3 全表 | **支撑型**（不作独立 Go 候选，作 Q11/Q12 gap 的综述级背景论证 + 算法地图基线）⚠️综述推荐前馈非闭环 PLL，与联合建模切入角度不同 | Valjus2025 §4-5 |

**Q# 清单判定（块 C + 块 D 召回，块 E 才判 Go/No-Go）**：

- 6 篇四判据全过（Q1/Q2/Q3/Q7/Q8/Q10），但**全部带 ⚠️ 标注**——链路不匹配（Q1/Q7 LEO-LEO 星间、Q3 feeder link）、利益相关（Q2 同实验室）、增益来源非核心机制（Q8 PS 非 N1 但增益来自 Rs）、高度同构 N1（Q10 高 SNR 趋零）。
- 4 篇部分不过（Q4/Q5/Q6/Q9）作方法借鉴/机制启发用，不进 Contract Step 1 假设引用。
- **块 D 召回 3 篇（Q11/Q12/Q13）**：旧 B1 方向资产纠正漏召。Q12（Paillier 2019 conf 分治架构）四判据全过 + E 三检验 3/3，是盲区 A"联合建模"gap 的**最强 baseline 端证据**（分治范本）；Q11（Pech 2025 Z 变换 ODPLL）部分过 D⚠️（baseline 自身量化弱），作 Q12 的最新延续；Q13（Valjus 2025 综述）支撑型，给 gap 综述级强证据 + 算法地图基线。**三者共同指向同一 gap：星地 LEO + 湍流 + Doppler 联合 DSP 建模缺失**。

**Q# 综合观察线索（仅供块 E 参考，非结论，不塞方向给用户）**：

1. **Q8（PCS+Rs 治 Doppler）"同门范式"味道最浓**：场景约束（LEO Doppler + COTS 带宽限制）→ 现有方法失效（固定 Rs 被非对称滤波）→ 切入点（Rs+PS 联合适配），增益 ~100Gbps 量级硬。**但增益来自符号率适配非 PS**——块 E 提炼 Q# 角度时，"PS 方向"叙事要弱化，重心在"参数自适应对抗硬件带宽/Doppler 耦合"。
2. **Q5（Doppler 跟踪）虽 C/D 不过**，但方法形态（AFC 闭环 + CFR 前馈实时 FPGA）跟同门纯 DSP 范式最对路，BUPT 同国别团队。块 E 可考虑作"方法借鉴/对照"而非"直接 Q#"。
3. **PS 三篇（Q8/Q9/Q10）同构性梯度**：Q8（PS 作使能件，不同构 N1，增益来自 Rs 适配）> Q9（PS 半核心，部分同构，消融不全）> Q10（PS 纯核心，高度同构 N1，高 SNR 趋零）。块 E 提炼 PS 相关 Q# 角度时，**优先看 Q8 的"PS+另一机制治具体失效"角度，避开纯 PS gain**（Q10 已证同构 N1 无效路径）。
4. **链路匹配缺口（块 D Step 3.5 已部分修正）**：Q1/Q7 是 LEO-LEO 星间（真空无湍流），Q9 是地面短距，Q6 是 GEO 35000km。星地 LEO + 湍流 + Doppler 三者联合的端到端 Q# 在块 A/B 选样时漏召，但块 D 核查发现 **Pech 2025 + Valjus 2025 + Paillier 2019 conf 三篇早在 2026-06-16 已下载并精读（旧方向 B1 资产，H004 选样路径依赖漏召）**，已召回为 Q11/Q12/Q13（见下）。**盲区真实性质 = "分治架构成熟但联合建模空白"的稀疏前沿，非蓝海**：Paillier 系列（AO 管湍流 + DPLL 管多普勒的分治范式）是代表 baseline，Valjus 2025 综述给"没有任何算法联合处理二者"的综述级强证据。
5. **Q12（Paillier 分治→条件性改进）块 D 精读后最务实切入点（2026-06-27）**：Paillier 2020 JLT（companion 完整版）证明"湍流相位对载波同步可忽略"但**依赖特定条件**（BPSK+10GBaud+理想timing+AGC恒幅+piston~1ms慢于符号率）。**务实路线 D005 下不是"推翻 Paillier"（那是真缝）**，而是针对 Paillier 假设不适用的条件做改进——如高阶调制/低 SNR/无理想 timing/强湍流快 piston/上行链路场景下 DPLL 失效边界 + 联合建模增益。**传统 baseline = Paillier 分治 DPLL，Go 判据 = 赢它几 dB**。⚠️ 但块 E 必查：旧 B1 时期是否已试过类似角度（警惕 B1 换皮，见 decisions.md）。

**诚实预期（块 E 前置，非结论）**：

- 务实路线下 Go 判据 = 赢传统未优化 baseline 几 dB。Q1/Q2/Q7/Q8 都有 dB 量级增益对标传统 baseline，**形式上够 Go 门槛**。
- 但每个 Q# 都有 ⚠️（链路/利益相关/同构 N1/FEC 理想），块 E 走 gw-feasibility 维度 A0/A'/A/B/D 时要逐条诚实判定，**不放水**（topic-index 不变量 1）。
- 若块 E 判出 ≥1 个 Q# Go → 进块 F（Step 5-7 baseline 复现）。若全 ❌ → 回块 A 扩检索（glossary.md"候选全被筛掉时"）。

---

## 文献条目

> 每篇详细结构化提取（14+ 字段 + 7 子表）见 `papers/_read_notes/{paper_id}.md`。本节给精简版（核心贡献 + 方法 + baseline + 增益 + 适配性）。

### [L01] Robust two-stage Kalman filter (TS-KF) for LEO-LEO Doppler

- **DOI/来源**：10.1364/oe.553709
- **源文件路径**：papers/doi/10.1364_oe.553709/content.md
- **发表状态**：正式发表
- **发表渠道**：Optics Express（SCI Q2，IF 3.8）
- **年份/会议**：2025
- **核心贡献**：提出鲁棒两阶段 KF（TS-KF），用 Q1=diag[1e-10,1e-4]（捕获突发）+ Q2=diag[0,1e-4]（锁定，ω 固定）解耦两冲突需求；通过旋归一化建立 LEO-LEO LISL 多普勒模型，量化建立期突变（交点处 20 GHz）+ 维持期慢漂（151.73 MHz/s）。
- **方法概述**：类 EKF 递归估计器，状态 x_k=[ω_k,ϕ_k]，观测 h(x̂_k)=Re{Ŝ_k}²−Im{Ŝ_k}²。符号分大块（L1+L2=2¹⁶），两子块级联。
- **方法形态**：DSP 递归估计器（无在线学习）
- **使用的 Baseline 方法**：VV（自实现）/ VV-BPS（自实现，同平台）
- **关键结论**：10GHz 突发@18dB TS-KF BER<FEC，VV-BPS 无法解调；0.1GHz 小频偏 TS-KF 略输 VV-BPS（nuance）
- **与本研究关系**：方法可借鉴（两阶段解耦范式）
- **实现关键细节**：Q1=diag[1e-10,1e-4]，Q2=diag[0,1e-4]，R=diag[1e-1,1e-3]，L1+L2=2¹⁶，60 Gbaud PDM-QPSK，OSNR 18dB
- **适配性分析**：不适配=假设 Q/R 平稳 + 圆轨道 + v≪c，机动/椭圆/相对论场景需重建模；Q2_ω=0 对快变信道（如湍流附加相位）不鲁棒。改进方向=RL/自适应在线调整 Q,R（论文 L131 自承 Q,R 显著影响性能）
- **问题提取**：见 Q1（**❌ Kill D010**：范围双重出界 + A1 归属错位 + C3 撞 Q12/B1 换皮；论文降级 baseline 参考）
- **开源代码**：无
- **验证状态**：grep 核查 PASS（H005）

### [L02] Noise-Tolerant CPR (二阶 DPLL + 前馈) — 北理工同实验室

- **DOI/来源**：10.3390/electronics14020265
- **源文件路径**：papers/doi/10.3390_electronics14020265/content.md
- **发表状态**：正式发表
- **发表渠道**：Electronics（MDPI，SCI Q2/Q3）
- **年份/会议**：2025
- **核心贡献**：提出噪声容限 CPR：二阶反馈环（Kd=4 + 二阶 loop filter + NCO）粗跟踪残余多普勒 FO，级联前馈级（complex phase rotator + 块长 N=64 平滑）精估 Wiener 相位噪声。识别最优 ωn=20 Mrad/s、N=64。FPGA/ADC/DAC 硬件平台验证 10 MHz/s 跟踪。
- **方法概述**：两阶段联合：一阶反馈 DPLL（K1,K2 由 ωn 和 ξ=√2/2 解析给）+ 前馈块估计平滑。反馈环消 cycle slip，前馈级跟踪 Wiener 噪声。
- **方法形态**：DSP 算法（经典数字锁相环，与 Costas loop 同族）
- **使用的 Baseline 方法**：Diff-4th [Leven 2007/Huang 2012/Tang 2023]（自实现，主对比）/ MCRLB [D'Andrea 30]（理论）/ DQPSK（对比基准，损失 0.5dB@1e-5）
- **关键结论**：BER=6.7e-3@4.5dB vs 传统 0.25；乘法仅 36%；实验 BER 7.5e-4@-41dBm vs 0.48。⚠️ 收敛慢（ωn=13Mrad/s 需 37µs）⚠️ 仅 QPSK ⚠️ Doppler 场景简化
- **与本研究关系**：直接相关 + ⚠️**利益相关**（作者 Hu Chunyuan/Lin Yujie 为用户同实验室 BIT，既是 baseline 候选也是可借鉴前作，客观性需留意）
- **实现关键细节**：Kd=4，ωn=20 Mrad/s，N=64，ξ=√2/2，约束 ωnT≪1；Eb/N0≤5.2dB；10 MHz/s 跟踪；FPGA 验证
- **适配性分析**：不适配=收敛慢不适配突发/短帧；仅 QPSK，高阶调制 cycle slip 更复杂。改进方向=变 ωn 自适应 / KF[18] / 粒子滤波[19] 替代 loop filter
- **问题提取**：见 Q2（**❌ Kill D011**：范围双重出界+A1归属错位+C3撞Q12/B1换皮，死因=Q1复刻；论文降级方法借鉴+同实验室前作；**登记16-QAM CPR扩展为待回看种子**）
- **开源代码**：无
- **验证状态**：grep 核查 PASS（H004）

### [L03] Linear Time-Packing Detectors for Optical Feeder Link

- **DOI/来源**：10.23919/GC-ElecEng48342.2020.9286272
- **源文件路径**：papers/downloads/2026-06-26/9286272.md
- **发表状态**：正式发表
- **发表渠道**：GC Wkshps ElecEng（IEEE 会议）
- **年份/会议**：2020
- **核心贡献**：系统对比三种 time-packed M-PAM 检测器：Viterbi(MLSE, Ns=4096)、truncated MMSE（闭式）、adaptive MMSE（LMS 自适应）。核心发现：M≥4 且 δ 增大时 adaptive MMSE 唯一无 error floor，复杂度可控。
- **方法概述**：Ungerboeck 观测模型经 whitening filter 得因果 ISI 模型，构造卷积信道矩阵 H；三种检测器恢复符号。
- **方法形态**：DSP 检测（性能评估/对比研究型）
- **使用的 Baseline 方法**：M-PAM without overlapping (δ=0)（理想上界）/ Viterbi [Forney 8/Ungerboeck 9, 作者前作 7] / truncated MMSE [14]（自实现）
- **关键结论**：adaptive MMSE 在 8-PAM 唯一跟随 baseline；4-PAM δ=40% 优于 Viterbi；2-PAM 比 Viterbi ~1dB gap（nuance）
- **与本研究关系**：方法可借鉴（adaptive MMSE 范式）
- **实现关键细节**：feeder link IM/DD，M-PAM (M≥4)，δ≥0.25，ρ=0.15；Ns=4096；LMS 自适应
- **适配性分析**：不适配=光 feeder link 链路预算与射频不通用；Ns=4096 是本文 Viterbi 特例不能外推。改进方向=adaptive MMSE 的 L_w/µ/训练序列手工固定，可自适应/数据驱动选抽头
- **问题提取**：见 Q3（**❌ Kill D012**：范围双重出界feeder系统级+无湍流建模 + A1归属错位 + C3未撞旧Kill但不构成salvage；论文降级方法借鉴）
- **开源代码**：无
- **验证状态**：grep 核查 PASS（H004）

### [L04] Data-Aided Multi-Format DSP（信道估计）— C⚠️ 不过

- **DOI/来源**：10.1109/WiSEE61769.2024.10850117
- **源文件路径**：papers/downloads/2026-06-26/10850117.md
- **发表状态**：正式发表
- **发表渠道**：IEEE WiSEE（会议）
- **年份/会议**：2024
- **核心贡献**：多格式 data-aided DSP 管线（帧同步+两级 CFO+OFDM-MIMO 信道估计+两级 CPE），靠显式训练符号实现"格式无关"，开销 7.75%；SNR≥0dB 可靠，3.2km 城市实测 outage 阈值 DP-16QAM −1.2dB / DP-4QAM −1.8dB。
- **方法概述**：经典离线 DSP 均衡器（非 ML/RL），RTO 存 10µs burst 离线处理；训练符号使信道估计与 payload 解耦；CFO/CPE 两级（粗+精）。
- **方法形态**：DSP 离线均衡器管线
- **使用的 Baseline 方法**：CMA[10]（盲均衡，**仅概念论证无直接 BER 对比**）/ BPS[17]（内部精 CPE）/ MMSE（内部）/ AWGN-MQAM 理论。**⚠️无与竞争性单格式 DSP 直接 head-to-head**
- **关键结论**：32GBd SNR≥0dB 稳定；CFO ±400MHz + PN 200kHz 无 penalty；实测阈值 DP-16QAM −1.2dB
- **与本研究关系**：方法可借鉴（数据辅助 + 两级粗精补偿思想 + 逐帧静态假设适配动态大气）
- **实现关键细节**：32 GBd DP-4QAM(100Gb/s)/DP-16QAM(200Gb/s)，28% 开销，SD-FEC BER≤2e-2；帧 32768 符号，开销 7.75%，导频 1%；CFO 粗±500/精±62.5 MHz；3150m 城市 FSO 1550.12nm
- **适配性分析**：不适配=理想 MRC 未验证（L19）；帧长 ~1µs 静态对亚µs 相干时间强湍流可能失效；实测城市地面非星地。改进方向=数据辅助+OFDM 偏振正交可迁移；逐帧静态+重估适配动态跟踪
- **问题提取**：见 Q4（未过 C⚠️ 缺直接对标，作方法借鉴）
- **开源代码**：无
- **验证状态**：grep 核查 PASS（H004）

### [L05] Real-Time Doppler Tracking (BUPT) — C❌D❌ 不过

- **DOI/来源**：ieee-11350922（具体 DOI 正文未印）
- **源文件路径**：papers/blit-downloads/2026-06-26/11350922.md
- **发表状态**：正式发表
- **发表渠道**：IEEE（会议，具体名正文未印）
- **年份/会议**：2025
- **核心贡献**：DSP 辅助 AFC 算法（CFR 模块 FOE 前馈→热控 Rx 可调激光器闭环），补偿范围扩到 ±8GHz / 33-120 MHz/s，FPGA 实时验证；BER=1E-3 灵敏度 −53dBm，CFR 跟踪灵敏度 −64.8dBm，FPGA 开销极小（LUT+5%, DSP48+0）。
- **方法概述**：STK 跑真实 DFS 曲线（500km/倾角180°/赤道地面站），Tx 激光器步进扫频仿真 ±8GHz；CFR 的 FOE 输出 f_e 前馈给激光器，当 |f_e|≥Rs/4 时 LO 粗调使残余在四次方 CFR ±Rs/2 内。
- **方法形态**：DSP 算法（实时 FPGA）+ 系统设计（AFC 闭环）
- **使用的 Baseline 方法**：VV CFR[1]（定性引用）/ Almonacil[5] 64GBaud 16QAM（定性"不适合低速系统"）/ 自团队前期[6] Tang Opt.Lett.2024 2.5GBaud QPSK LEO-GEO（未重跑）/ 表 I 资源对比（自实现，仅资源维度）。**⚠️无量化 BER-vs-baseline**
- **关键结论**：±8GHz/33-120MHz/s 补偿（超真实 LEO-地链路）；BER 1E-3 灵敏度 −53dBm 代价极小；通用性声称（任意速率/调制，无导频无星历）但仅测 BPSK 1.25GBaud OBTB
- **与本研究关系**：直接相关（同链路类型 LEO 星地，实时 FPGA，DFS 补偿）+ 方法借鉴（AFC 闭环 + CFR 前馈架构可复用）
- **实现关键细节**：1.25 GBaud BPSK 单偏振 OBTB；f_threshold=Rs/4，残余 ±Rs/2（±625MHz）；FPGA LUT 209899(49%)，DSP48 848(20%)；STK 500km/倾角180°
- **适配性分析**：适配=闭环 AFC+CFR 前馈架构可复用；无导频无星历契合 SWaP。不适配=仅 OBTB+VOA 功率波动，无实时湍流/相位闪烁；仅 BPSK 单偏振。改进方向=扩双偏振高阶 + 注入真实大气湍流
- **问题提取**：见 Q5（未过 C❌D❌，作方法借鉴）
- **开源代码**：无
- **验证状态**：grep 核查 PASS（H005）

### [L06] Dual-Polarization Self-Coherent (三 PD) — B 部分过

- **DOI/来源**：10.1109/ACCESS.2025.3535789
- **源文件路径**：papers/doi/10.1109_ACCESS.2025.3535789/content.md
- **发表状态**：正式发表
- **发表渠道**：IEEE Access（SCI Q1/Q2，IF 3.4）
- **年份/会议**：2025
- **核心贡献**：揭示双偏振自相干（DP-SC）两 PD 接收在湍流致偏振旋转 θ=45°/135°/225°/315° 时 H_eff,2PD(eq18)奇异 BER>0.1；提出三 PD 接收方案（1×3 PBS 分 0°/45°/90°，DSP 两两选电流组合使 BER 最低）消除奇异，实现直接检测下数字偏振解复用无需手动偏振控制器。
- **方法概述**：DP-SC 发射机数字域注入频偏 Δf pilot carrier；接收 PBS→PD→BPF→ADC→baseband converter→DSP 信道估计（4000 符号估 θ）+ 均衡 + 偏振解复用。
- **方法形态**：DSP 算法 + 光学架构（混合），含机制分析（奇异性证明）
- **使用的 Baseline 方法**：DP-coherent（自实现同链路同参数）/ 两 PD DP-SC（自实现，被改进对象）/ SP self-coherent[4]（cited 定性）
- **关键结论**：下行中等湍流 BER=1E-3：coherent 需透镜 17.5cm，self-coherent 22.5cm（OSNR penalty 2.21dB）；上行弱湍流 penalty 3.76dB。⚠️ self-coherent 低 OSNR 落后 coherent 1.5-1.9dB；图9 三 PD BER 改进仅定性"substantially reduced"
- **与本研究关系**：直接相关（星地 DSP 信道估计/均衡/偏振解复用 + 机制分析 + baseline 候选）
- **实现关键细节**：35000km GEO，QAM-16，10 GSym/s；训练 4000 符号估 θ；Gamma-Gamma 闪烁 + 偏振旋转 θch + 偏振相关相移 Δφ；Hch eq1
- **适配性分析**：适配=Hch(eq1)+H-V/Gamma-Gamma 框架可直接用于星地 DSP 仿真器偏振/闪烁建模；训练-数据两阶段信道估计流程可复用。不适配=排除 beam wander + 上行"理想 tracking"；35000km GEO 准静态偏振对 LEO 短相干时间(ms)不成立。改进方向="两两选电流最低 BER"启发式 → 在线自适应均衡（LMS/RLS/CMA）跟踪 LEO 时变偏振
- **问题提取**：见 Q6（部分过 B 部分，⚠️链路 GEO 非 LEO，作机制借鉴）
- **开源代码**：无
- **验证状态**：grep 核查 PASS（H005）

### [L07] LEO-LEO DS Compensation (两阶段 CFE, ACCESS 2023, c=33)

- **DOI/来源**：10.1109/ACCESS.2023.3287501
- **源文件路径**：papers/blit-downloads/2026-06-26/10155111.md
- **发表状态**：正式发表
- **发表渠道**：IEEE Access（SCI Q1/Q2，IF 3.4）
- **年份/会议**：2023
- **核心贡献**：评估 QPSK/8-QAM/16-QAM @ 28/60/120 GBaud 在 4 个商业 LEO 星座适用性；推导 FNCs/AACs 多普勒频移特征上界；提出改进型全电子两阶段 DS 补偿接收机——滤波对称性粗 CFE + M-th power 精 CFE + 新 LPF 级减轻过剩带宽噪声。
- **方法概述**：Walker 星座 + 链路预算 + 散弹/ASE SNR；全电子接收机（粗对称性 CFE 与 CMA/RDE 均衡并行 → 频率补偿 → M-th power → BPS）。
- **方法形态**：DSP 算法 + 系统设计/可行性分析
- **使用的 Baseline 方法**：evaluated receiver[50]（Diniz 两阶段，自实现直接对比 图7）；M-th power[70]（定性引用）；OPLL[44-47]/Almonacil[48]（引用未跑）。**对称 ✅**（同链路 LEO-LEO OISL、同调制、同 32GBaud PM、同信道、同 FFT 窗）
- **关键结论**：10GHz 16-QAM 损耗 1.2dB(evaluated)→0.9dB(modified)；补偿范围升至 ≥13GHz（16-QAM），单纯精 CFE 为 8GHz（BPSK）；24GHz 接收机恢复 17.6GHz 基带+10GHz DS。⚠️仅仿真无硬件
- **与本研究关系**：方法可借鉴（两阶段 CFE + LPF 范式）
- **实现关键细节**：4 个商业 LEO 星座 A-D；DS 高达 10GHz(AAC)；Nyquist 整形 + 过剩带宽；32GBaud PM；Rs/(2M) 范围限制；M=4 时 10GHz 需 80-GBaud
- **适配性分析**：不适配=为真空 OISL 设计（无湍流/吸收），AWGN/散弹/ASE SNR 低估星地损伤；全电子后补偿需扩展接收带宽（24-28GHz）无实时/硬件证明。改进方向=加大气湍流 + 相位闪烁 + 硬件/FPGA 验证星地
- **问题提取**：见 Q7（全过，⚠️链路 LEO-LEO 星间真空非星地）
- **开源代码**：无
- **验证状态**：grep 核查 PASS（H005）

### [L08] PCS + 自适应符号率 治 Doppler (=landscape #580)

- **DOI/来源**：10.1109/JLT.2023.3281082
- **源文件路径**：papers/blit-downloads/2026-06-26/10138358.md
- **发表状态**：正式发表
- **发表渠道**：IEEE Journal of Lightwave Technology（SCI Q1，IF 4.7）
- **年份/会议**：2023
- **核心贡献**：首个联合自适应 PCS + 自适应符号率的全数字方法缓解 LEO-to-Earth FSO 链路 Doppler 致非对称电滤波惩罚；固定 600 Gbps 净比特率下调 Rs 和熵 H 维持性能；两场景验证（保证可靠性 70-99% / 最大化吞吐量）。
- **方法概述**：PCS 单参数控熵 + 调 Rs 联合保持 Rb 固定（式9）；无 Doppler 时用高 Rs，有 Doppler 非对称滤波时降 Rs 最小化滤波惩罚；大气湍流用 Gamma-Gamma 按衰减向量叠加到无湍流 SNR。
- **方法形态**：编码调制(PCS) + DSP 算法混合
- **使用的 Baseline 方法**：固定 80Gbaud（自实现，同链路同硬件）Fig.7b/10 直接对比；[29][30][31][32] 仅定性。**对称 ✅**。**注意**：PS 在 proposed 和 baseline 都用（两者都基于 M=64 QAM 模板），对比的是"符号率是否自适应"，**不是"用不用 PS"**
- **关键结论**：±15GHz 极端 Doppler 下 ABR 仍 ~600Gbps（vs 固定 80Gbaud ~100Gbps 增益）；最大化吞吐量场景提升 70Gbps。⚠️ FEC 假设理想（NGMI_th=R_FEC，ABR 为上界）；半物理（Doppler 真实 LO 频偏，湍流 GG 数值叠加非真实大气）；吞吐量场景假设理想逐比特重传
- **与本研究关系**：直接相关 + 方法借鉴（"参数自适应对抗硬件带宽/Doppler 耦合"角度）
- **实现关键细节**：LEO-to-Earth 500km（7.8km/s，45°倾角）；±15GHz Doppler；固定 Rb=600Gbps；M=64 QAM 模板；Rs+H 联合调度查表；Gamma-Gamma 湍流数值叠加
- **适配性分析**：不适配=依赖"固定比特率"约束（Rb=600Gbps 不变），变比特率/变吞吐量目标需重构；FEC 假设理想，真实系统需替换具体 SD-FEC。改进方向=论文 L281 自述加入指向误差、云遮挡、天气、多径及与 Doppler 相互作用
- **问题提取**：见 Q8（全过，⚠️增益来自 Rs 适配**非 PS**，不同构 N1）
- **开源代码**：无
- **验证状态**：grep 核查 PASS（H005）

### [L09] PS + RCM 治湍流 — D⚠️ 不过 + 部分同构 N1

- **DOI/来源**：10.1109/LPT.2025.3647750
- **源文件路径**：papers/doi/10.1109_LPT.2025.3647750/content.md
- **发表状态**：正式发表
- **发表渠道**：IEEE Photonics Technology Letters（SCI Q2，IF 2.5）
- **年份/会议**：2025
- **核心贡献**：提出 PS+残余载波调制（RCM）混合方案治湍流 FSO——RCM 通过 IQ 调制器偏置点略微偏离零点产生残余载波作内置相位参考（无需额外导频或高功率 DC），PS 重塑符号概率分布缓解湍流致强度闪烁；给出残余载波幅度 A_c 与偏置电压 V_bias 显式关系；PSO 离线优化 16-QAM 输入分布最大化 R_BMD；仿真+水池实验验证 BER 在中强湍流下仍低于 SD-FEC 阈值。
- **方法概述**：发射端 CCDM 生成 MB 分布 PS 符号 + IQ 调制器轻微偏置注入残余载波；接收端提取残余载波做相位共轭补偿湍流相位畸变，简化信道为"幅度变化+加噪"，PS 再抗幅度闪烁。
- **方法形态**：编码调制(PS) + DSP 算法(相位共轭) + 调制器偏置配置（无新硬件）
- **使用的 Baseline 方法**：无相位补偿系统（自实现 Fig.5）；uniform signaling（自实现 Fig.3）；AO[3]/多模[4]/导频[5]/KK[6]（引用仅定性）。**⚠️部分对称**——proposed=PS+RCM；baseline1=uniform+无补偿（两者既差 PS 又差 RCM）；baseline2=PS+无补偿。"PS on/off 在相同 RCM 下的纯 PS 增益未独立隔离"——**PS 方向潜在陷阱点**
- **关键结论**：PS-RCM 所有湍流条件下 BER 最低，强湍流仍低于 SD-FEC；LPF 带宽 100MHz、CSPR −20dB 最佳；相位补偿对小 r_0（强湍流）尤为关键。⚠️**PS/RCM 消融不完整增益归因存疑**；PS 增益高 SNR 趋零（N1 特征）；**无具体 dB 增益数字**
- **与本研究关系**：可借鉴（RCM 无额外硬件相位参考思路 + PSO 离线 PMF 优化）
- **实现关键细节**：FSO 地面短距（湍流水池物理模拟 / 等效率 3km 传播估算 C_n²）；5Gbaud PS-16QAM 1550nm；CCDM MB 分布；CSPR −20dB；LPF 100MHz；PSO 优化
- **适配性分析**：适配=PS 抗湍流强度闪烁、Gamma-Gamma/Kolmogorov 相位建模、PSO 离线 PMF 优化可移植。不适配=RCM 残余载波提取依赖"载波与信号谱分离"，星地 Doppler 频移会使载波谱移动破坏分离（本文未考虑 Doppler，地面短距场景）；5Gbaud 低速与星地 600Gbps 量级差距大。改进方向=论文未给（letter 篇幅短）
- **问题提取**：见 Q9（未过 D⚠️，⚠️部分同构 N1 + 链路地面短距，作方法借鉴）
- **开源代码**：无
- **验证状态**：grep 核查 PASS（H005）

### [L10] PS-QAM Gamma-Gamma 理论 — 高度同构 N1

- **DOI/来源**：10.3390/app11219805
- **源文件路径**：papers/doi/10.3390_app11219805/content.md
- **发表状态**：正式发表
- **发表渠道**：Applied Sciences（MDPI，SCI Q2/Q3）
- **年份/会议**：2021
- **核心贡献**：首次在 Gamma-Gamma 湍流信道下用启发式算法（粒子群类，随机惯性权重 + 变异 δ）优化 PS-QAM 的 PMF 以最大化 BMD 可达信息率 R_BMD；首次推导非均匀信号集在 Gamma-Gamma 信道下的闭式 PEP 表达式；Monte Carlo 证 PS 相对均匀分布在低 SNR 有 0.4dB(AIR)/1.3dB(post-FEC BER) 增益。
- **方法概述**：发射端 PRBS→CCDM 生成 PS-16QAM→DVB-S2 LDPC(码率2/3)→MZM；接收端 LLR+BMD 译码；启发式算法在 2 维对称空间离线搜索每个 SNR 的最优 PMF，适应度=MC 评估的 R_BMD。
- **方法形态**：编码调制（PMF 优化 + PEP 闭式）
- **使用的 Baseline 方法**：uniform 分布（自实现，主对比）；Maxwell-Boltzmann(MB) 分布（自实现）；Yao[11]/Wang[12]/Elzanaty[20]（引用仅讨论）。**对称 ✅**（同 16QAM、同 LDPC、同 GG、同 BMD，仅 PMF 不同）
- **关键结论**：PS H=3.7964 在 AIR ~1.8 bit/symbol 处比 uniform 增益 0.4dB；post-FEC BER=1e-2 处 ~1.3dB；Es/N0>6dB 后 PS 优于 MB；**16dB 后 uniform 反超**（L562）。⚠️**高度同构 N1**：(a)低 SNR 有增益(0.4-1.3dB)；(b)高 SNR 增益趋零 PMF 趋均匀；(c)16dB 后 uniform 反超。固定 SNR 点评估未体现时变信道动态适配——接近 N1"固定信道 gain≈0"
- **与本研究关系**：方法借鉴（PSO 离线 PMF 优化 + PEP 闭式工具）+ ⚠️**反面教材**（纯 PS gain 在固定/高 SNR 信道同构 N1 无效路径）
- **实现关键细节**：相干 FSO Gamma-Gamma 湍流；PS-16QAM；DVB-S2 LDPC 码率 2/3；CCDM；PSO 随机惯性权重 + 变异 δ；2 维对称空间搜索
- **适配性分析**：不适配=无 Doppler、无指向误差、无星地几何；完美 CSI 假设在星地时变信道不成立；纯仿真无硬件；信道模型 y=Gx+N 过简（无相位畸变建模）。改进方向=论文无明确未来工作段
- **问题提取**：见 Q10（全过四判据形式上，但⚠️**高度同构 N1** 实质风险——块 E 必查"增益是否依赖时变信道"）
- **开源代码**：无
- **验证状态**：grep 核查 PASS（H005）

---

## 写作架构参考（选做）

> 本轮块 C 不深入写作架构（重心在 Q# 清单）。块 F baseline 复现阶段再对 2-3 篇标杆做写作架构提取。此处仅记录候选与初步观察。

### 标杆论文候选

- **#2 CPR 北理工（Electronics 2025）**：同实验室同套路，motivation 结构（场景→Diff-4th 失效→二阶 DPLL+前馈切入）最对路，但 ⚠️ 利益相关需谨慎引用
- **#新4 PCS+Rs（JLT 2023, Q1）**：目标期刊 JLT，Doppler+全数字 DSP 叙事完整
- **#1 TS-KF（OE 2025, Q2）**：两阶段解耦范式写作清晰

### 共性模式（初步）

- **章节结构**：多数有独立 System Model / Problem Formulation / Algorithm Design 章节（#1/#2/#新4）
- **实验组织**：baseline 数 1-3 个，含传统方法 + 理论下界（MCRLB）；消融逐参数；多 SNR 全扫描
- **参数展示**：表格集中（#2 Table I 资源对比）+ 正文行内符号定义
- **图表**：系统模型图 + 算法框图 + BER-vs-SNR/OSNR 曲线 + 复杂度对比表

### 竞品共同引用但 GW 未覆盖的文献

- **Viterbi-Viterbi CPR 经典**（被 #1/#2/#新1 引用）：foundational，Step 3.5 可补
- **Diniz et al. 两阶段 CFE [50]**（被 #新2 引用）：DS 补偿前作
- **Paillier 2020**（AO 相干时间 τ_c~1ms，TL-26 教训来源）：已在 thesis-lessons 引用，确认本地有

---

## 实验完备性对标汇总

> 对 5 篇核心竞品（#1/#2/#3/#新2/#新4）提取实验完备性维度（每篇 ≤20 行见 `papers/_read_notes/`），此节为对标汇总。

### 领域实验惯例（从 5 篇归纳）

| 维度 | 领域惯例 | 盲点 |
|------|---------|------|
| 统计规范性 | **无一报告 seeds 数/error bar/统计检验**（10 篇全无） | 统计严谨性是领域普遍盲点 |
| Baseline 数量 | 1-3 个（含传统 + 理论下界） | #6/#新1 缺直接 head-to-head |
| 消融设计 | 逐参数扫描（ωn-N / Q1-Q2 / Rs-H） | #新5 PS/RCM 消融不全（陷阱） |
| 信道模型 | Gamma-Gamma 强度闪烁为主 | 相位畸变建模稀缺（仅 #新5 Kolmogorov） |
| 拓扑多样性 | 单链路（星地/星间/地面） | 无跨链路类型对比 |
| 复杂度报告 | 乘法/加法/LUT/DSP48（#2/#新1 有） | 部分仅定性 |
| VVUQ | Verification 强（理论推导 + 仿真双证）；Validation 中（多数仅仿真，#2/#新1 有 FPGA）；Uncertainty 弱（无 UQ） | UQ 是最大缺口 |

### 对标基准（Contract 阶段用）

- **统计规范性平均**：低（领域惯例无 seeds/error bar，本研究 Contract 阶段应补 ≥3 seeds + error bar 超越领域惯例）
- **Baseline 合规性平均**：中（多数自实现同平台对称，但 #6/#新1 缺直接对标是反面教材）
- **消融设计平均**：中高（逐参数是惯例，#新5 消融不全是陷阱，本研究必须做完整消融归因 TL-15）

---

## 载波同步 v2 精读沉淀（2026-07-04，B 档 12 候选补强）

> **来源专题**：`.sessions/2026-07-02-carrier-sync-v2-deep-read/`（承接原专题 S030 判读层收尾）
> **目的**：原块 A/B/C/D 的 10 篇精读 + Q1-Q13 已在 Step 4a 评过（Q1/Q2/Q3/Q8切入点2/4B/Q12 Kill）。本节是**载波同步子领域 B 档 12 候选的精读沉淀补强**——D017/D018 判读层虽拉了总表但每点只读 1 篇切入论文、B8-B12 五篇零精读笔记。本节补扎实：12 份 gw-read 14 字段+7 项结构化笔记 + 每点 ≤5 篇 cited-by 验证 + 综合分析。
> **守 D018 中性提取**：Q# 只标 D006/D005/范围三维，**不判 Go/Kill**（Go/Kill 留总表阶段用户排完优先级后对前几名做）。
> **35 Q# 计数修正**：S005 原报"26 Q#"是计数 bug（B1-B7=20 + B8 主判定+2=3 + B9×3 + B10×3 = 29，非 26）。本轮 +B11×3 +B12×3 = **35 Q#**。

### 载波同步 v2 综合分析

#### 现有方法分类（B 档 12 候选，按技术路线 6 类）

1. **DSP 前馈 FOE/CPE（5 篇，主热区）**：B5 短时谱粗 CFO（正负功率谱面积比，optcom 2024，±4.5GHz 覆盖 LEO Doppler）/ B7 Gardner TED 复用 FOE（TED 增益周期相关，OFC 2026，0.6dB+1.9×范围）/ B11 NDA-ML 联合 STO+CPE（升 M₀ 次幂盲去调制→单正弦 ML 闭式，PTL 2025，+2dB vs DA ML）/ B12 锚频域 CW pilot（in-band/out-of-band + improved 估计器≈MVU，TCOMM 2022）/ B10 pilot-RLS 联合 CFO+PN（h1→CFO/h0→PN，s11107 2024，高 CFO 10GHz 鲁棒）。共同范式：**前馈 DSP 处理，无环路 TF，不撞 D006**。

2. **OPLL 硬件锁相（2 篇）**：B6 Z-ODPLL（atan2 鉴相器 KD 与 Ps 解耦，全湍流态保锁 σ=2.6°/0.42dB/容 30ns）/ B4 双反馈环（外环 PADE 大动态 + 内环 V-V RFO 精补 + 前馈 V-V 相位，optcom 2023）。共同范式：**环路锁相，撞 D006 边界**（若环路 TF 联合建模则撞，只标不砍）。

3. **自相干架构绕过载波同步（2 篇，B8 特例）**：B8 RL+GS 自相干（square-law+LPF 自消除 CFO/相位噪声，PAM4 直接判决，**载波同步被绕过**）/ B9 虚拟载波自相干+DRE（数字域 DSP 插入 carrier tone，DRE 把量化噪声挤出带外，~3dB @ 3PNOB）。共同范式：**用架构消除载波恢复需求**，与 B1-B7/B10-B12 改进载波恢复正交。

4. **pilot-aided 高阶 QAM CPE（2 篇）**：B10 pilot-RLS（16-QAM，D011 种子"16-QAM CPR 扩展"落地）/ B12 MAP（256-QAM MAP Phase Recovery，OECC 2025，MAP vs PA 差 3.5dB）。共同范式：**pilot 驱动 + 高阶 QAM 相位估计**，D011 种子延伸。

5. **子系统协同（1 篇）**：B3 一套 FPT 跨 FOE+CPE+RSOP（jphot+oe 合并 +2~3dB 强湍 4 支路 / LCOMM B3 视角 +0.9dB Q）。范式：**跨子系统共享 pilot + 依赖解耦联合协同**。

6. **NDA-ML 盲估计（1 篇）**：B11 升 M₀ 次幂盲去调制（无 pilot 保留频谱效率）+ Wang[13] 单正弦 ML 闭式。范式：**NDA 盲估计**，区别于 pilot-aided。

#### 已知局限（领域级空白原料，**非问题**，须经 Q# 转译）

> 注意：本节按 glossary.md 是空白（领域级新颖性原料），不能直接当研究起点。

B 档 12 篇的共同不足：

1. **D006 边界模式重复 7 次**（B3-Q3/B6-Q2/B7-Q2/B9-Q3/B10-Q2/B11-Q2/B12-Q3）——"前馈/工具层不撞，环路 TF 联合建模则撞"是潜在一致性研究方向（湍流相位建模边界）。**这是 B 档最重要的结构性发现**。
2. **dB 增益集中第一梯队仅 3 个**（B3-Q2 +2~3dB / B9-Q1 ~3dB / B11-Q1 +2dB），其中 B9-Q1 baseline 是内部 w/o DRE 对照非传统相干载波同步，B11-Q1 仅 (8,8)-16APSK 成立。D005"赢传统 baseline 几 dB"硬达标的不多。
3. **范围 out 比例高**（35 Q# 中 ~9 个 out：B3-Q1 光纤 DSCM / B5-Q2 光纤 intradyne / B8×3 地面 FSO / B10-Q1/Q3 光纤 / B12-Q1/Q2 光纤 DCI）——星地 in/in 倾向是主体（~24/35 ≈ 69%）但 out 比例较块 A/B（Q1/Q7 LEO-LEO）更高。
4. **B8 特例"载波同步冗余"**——自相干绕过载波同步，与 B1-B7/B9-B12 改进载波恢复本质正交。提示"自相干架构替代传统载波同步链"是另一条潜在路线（B9 也走这条路 Q2），但 B8/B9 主场景都非星地。
5. **D011 种子"16-QAM CPR 扩展"落地**——B10（16-QAM pilot-RLS）+ B12 MAP（256-QAM MAP）+ ao.581648（PS-64QAM KRLS 承接，同作者团队 Deka/Krishnamurthy），pilot-RLS→KRLS 是核方法非线性升级。三者都光纤 out，迁移星地是 Q# 维度。
6. **统计严谨性普遍不足**：12 篇无一报告 seeds 数/error bar/统计检验（同块 A/B 领域惯例盲点）。
7. **多数未涉大气湍流**：B5/B7/B11/B12 锚全文无湍流建模（仅 Doppler/AWGN+激光线宽）；B4/B6/B3 含湍流但简化（Gamma-Gamma 数值叠加非真实大气）。湍流相位扰动对载波同步算法的影响是 open gap。

#### 2-3 年趋势（从 B 档发表年份 2022-2026 推断）

1. **DSP 前馈替代 OPLL 硬件**：B5/B7/B10/B11/B12 都是 DSP 前馈 FOE/CPE（2022-2026），仅 B4/B6 保留 OPLL 硬件锁相。趋势与块 A/B 一致（全数字 DSP 替代光学硬件）。
2. **NDA 盲估计兴起**：B11 NDA-ML（2025）保留频谱效率，区别于 pilot-aided（B10/B12）。2024-2026 年 NDA 方法开始系统化（Wu[11]/Hu[12] 经典理论锚 + B11 闭式解）。
3. **自相干架构成熟**：B8（JOCN 2023）+ B9（JLT 2023）+ apn DRE（2026）形成"自相干绕过载波同步"技术线，2023-2026 持续演进（DRE 量化噪声整形 + 虚拟载波）。
4. **高阶 QAM CPE 升级**：B10 pilot-RLS（2024）→ B12 MAP（2025）→ ao.581648 KRLS（PS-64QAM），pilot-RLS→MAP→KRLS 是"线性→贝叶斯→核方法"的估计器升级链，2024-2026 活跃。
5. **D006 边界模式持续出现**：7 次"前馈/工具层不撞，环路 TF 联合建模则撞"在 B 档重复，预示**湍流相位建模边界**是潜在一致性研究方向（但 Go/Kill 留用户）。

#### 研究背景概述（载波同步子领域时间线 + 核心挑战 + 本研究定位）

**时间线脉络**：

- **1980s-2000s**：经典 OPLL/Costas loop/V-V CPR 主导（Gardner TED 1986 / Viterbi-Viterbi 1983 / Leven M-th power 2007）。硬件锁相 + 前馈四次方是两大范式。
- **2010s-2020**：DSP 数字 FOE 兴起（PSA FOE Vieira 2023 / M-th power 两阶段 Diniz / Spalvieri pilot-aided）。OPLL 仍用于硬件锁相（Shoji OIPLL 2012 / Paillier AO+DPLL 2020 分治架构）。
- **2022-2026**：①DSP 前馈 FOE 系统化（B5 短时谱 / B7 Gardner TED 复用 / B11 NDA-ML 闭式 / B12 频域 CW pilot 理论框架）；②自相干架构绕过载波同步（B8 square-law+LPF / B9 虚拟载波+DRE）；③高阶 QAM CPE 升级（B10 pilot-RLS / B12 MAP / ao.581648 KRLS）；④子系统协同（B3 跨 FOE+CPE+RSOP）。

**核心技术挑战**（从 12 篇精读归纳）：

1. LEO 星地链路 Doppler 频移大（±GHz 级）+ 变化率高（MHz/s 量级），传统 ±Rs/2 范围不足（B5 ±4.5GHz / B7 0-23GHz / B4 ±920MHz@0.5dB）。
2. 大气湍流致幅相联合损伤，但多数载波同步算法未建模湍流相位（B5/B7/B11/B12 全文无湍流，仅 Doppler/AWGN+激光线宽）。
3. 高阶调制（16-QAM/256-QAM）+ 高 CFO + 高线宽下传统 BPS/V-V 失效（B10/B12 MAP 的切入点）。
4. D006 边界：湍流相位纳入环路 TF 联合建模被证伪（Q12 Paillier 分治够用条件性），但前馈层处理不撞——**7 次"前馈不撞/环路撞"模式**是潜在一致性研究方向。

**本研究定位**（务实路线 D005）：在星地激光通信载波同步子领域，B 档 12 候选 35 Q# 中找"现有传统未优化方法 M 在具体条件 C 下因假设 A 不够好"的改进空间。**第一梯队 dB 达标候选**（B3-Q2 +2~3dB / B9-Q1 ~3dB / B11-Q1 +2dB）是 Go 判据的硬证据候选，但各有条件性（B9 baseline 内部对照 / B11 仅 (8,8)-16APSK / B3-Q2 范围 in 但分集增益不可全迁）。**D006 边界模式 7 次**是潜在一致性研究方向（湍流相位建模边界）。Go/Kill 留总表阶段用户排完优先级后对前几名做。

#### 研究问题清单 [MUST]（B 档 35 Q# 汇总，过 glossary 四判据）

> 问题定义见 `stages/glossary.md`（问题 = "现有方法 M 在条件 C 下因假设 A 失效/不足"，四判据）。
> 本表是 Contract Step 1 假设的**唯一合法引用来源**（每个假设引用一个 Q#）。
> **D018 中性提取**：本表只标 D006/D005/范围三维 + 四判据逐条，**不判 Go/Kill**。Go/Kill 留总表阶段用户排完优先级后对前几名做。
> **判据 A（D005 修正）**：baseline 在具体条件下不够好 + 有改进空间（不要求"致命失效"）。
> **链路匹配标注**：标题"星地"为范围约束。出范围（光纤/地面 FSO/ISL）标 ⚠️链路。
> **dB 量级参考**：同门学位论文 2-4dB 区间。第一梯队 +2~3dB（B3-Q2/B9-Q1/B11-Q1）/ 第二梯队 +0.6~1dB+结构性优势 / 第三梯队待定量锚。

> **35 Q# 全表见 `.sessions/2026-07-02-carrier-sync-v2-deep-read/S006-conversation4-b11b12-eval.md` §B1-B12 全 12 点总表**（本表只列四判据全过 + 边际够格的候选，其余标"未过"记录筛掉理由防复现）。

**四判据全过候选**（D005 够格 + 范围 in/in 倾向 + 四判据 ✅）：

| Q# | M（失效/不足的现有方法） | C（条件） | A（失效假设） | 方法产出形态 | 判据1 | 判据2 | 判据3 | 判据4 | 来源 |
|----|------|------|------|------|------|------|------|------|------|
| **B3-Q2** | 传统分立 FOE+CPE+RSOP 管线（多套 pilot 独立） | 强湍流 FSO 4 支路分集 | 多套 pilot 独立致开销高+联合信息未利用 | DSP 联合协同算法（一套 TS 多 FOE+MRC） | ✅ | ✅ 算法 | ✅ 分立管线自实现 | ✅ +2~3dB / 复杂度降 75% | B3 jphot+oe |
| **B9-Q1** | w/o DRE 自相干 FSO（量化噪声未整形） | 地面 FSO 42m + 低分辨率 DAC（3 PNOB） | 低分辨率 DAC 量化噪声致 SNR 退化 | TX 侧量化噪声整形算法（DRE 动态量化+Viterbi） | ✅ | ✅ 算法 | ✅ w/o DRE 内部对照 | ✅ ~3dB @ 3PNOB（行 243/253）⚠️baseline 内部对照非传统相干载波同步 | B9 jlt.2023.3270673 ⚠️地面 FSO 待迁移星地 |
| **B11-Q1** | DA ML（单 pilot 符号 decision-aided，高星座密度判决错误传播）+ PA（频域 pilot subcarrier，无 STO 能力） | CO-OFDM M-APSK (8,8)-16APSK，25 GBaud，CLW 扫至 500kHz，7% HD-FEC | DA ML 高星座密度判决错误传播；PA 频谱效率低且无 STO | DSP 盲估计算法（NDA-ML 升 M₀ 次幂+单正弦 ML 闭式） | ✅ | ✅ 算法+闭式 | ✅ DA ML[10]+PA[8] 自实现 | ✅ +2dB SNR gain @ (8,8)-16APSK（行 181/191）⚠️仅 (8,8)-16APSK 成立，CLW 容限付 1dB cost；声明 FSO 但仿真未建模 FSO 信道 | B11 lpt.2024.3523478 ⚠️声明 in 仿真未验证 |

**边际够格候选**（D005 边际够格 + 范围 in 或结构性优势）：

| Q# | M-C-A 浓缩 | D005 | 范围 | 四判据 | 来源 |
|----|-----------|------|------|--------|------|
| **B1-Q1** | 自适应 window N（sat.1553 固定 + [60] N∝SNR；强湍 SNR 波动）| +1dB（pilot vs VV+diff）倾向够格但有风险 | in | 判据1-4 ✅（理论锚 [60] 背书）| B1 sat.1553 |
| **B2-Q2** | FOE freeze + pilot 双模切换（[79] blind freeze；fade 恢复期需快速重捕获）| +1dB（pilot 在 fade）倾向够格增量未量化 | in | 判据1-4 ✅ | B2 [79]+sat.1553 |
| **B7-Q1** | Gardner TED 复用 FOE（TED 增益周期相关，扫频+双候选+TED2 判决）| 0.6dB @ BER 2e-2 + 1.9×范围（0-23GHz）+ OSNR 10dB 边际够格 | in（星地 COSC）| 判据1-4 ✅（baseline PSA FOE 明确）| B7 ofc.2026.w2a.62 |
| **B10-Q1** | Pilot-RLS 联合 CFO+PN（h1→CFO/h0→PN，替代 BPS+4OPM；高 CFO 10GHz/高线宽 1.45MHz 鲁棒）| 无统一 dB gain，优势在范围/鲁棒性边际够格 | ⚠️out 光纤/待迁移星地 | 判据1-3 ✅ 判据4 ⚠️（无统一 dB）| B10 s11107-024 |
| **B5-Q1** | 短时谱粗 CFO（正负功率谱面积比，全文核验升级）| dB 维度不够格 / 范围结构性优势（±4.5GHz 覆盖 LEO Doppler）| in（星地 LEO 下行确证）| 判据1-3 ✅ 判据4 ⚠️（无 vs baseline dB）| B5 optcom.2024.130981 |
| **B6-Q1** | atan2 鉴相器 KD 与 Ps 解耦（全湍流态保锁，容 30ns 延迟）| 定性保锁 σ=2.6°/0.42dB + 容 30ns 边际够格（非几 dB）| in | 判据1-4 ✅（定性保锁是维度）| B6 Photonics2023 |
| **B12-Q2** | MAP 联合 ML/MAP 相位估计（256-QAM + AOPN + block-wise 并行）迁移星地高阶 QAM | MAP vs PA 差 3.5dB / vs PA ML 差 1dB 边际够格（同族 dB）| ⚠️out 光纤 DCI/待迁移星地 | 判据1-3 ✅ 判据4 ⚠️（同族 dB 非传统 V-V/BPS）| B12 MAP oecc-psc62146 |

**D006 边界候选**（7 次"前馈不撞/环路 TF 联合建模则撞"模式，只标不砍）：

| Q# | 边界描述 | D005 | 范围 | 来源 |
|----|---------|------|------|------|
| B3-Q3 | sat.1553 L790 跨子系统联合协同（若环路 TF 联合建模则撞）| 待定量锚（借 +0.9~3dB）| in | B3 |
| B6-Q2 | Z-ODPLL H(z) 建模（固定 Kd 掩盖 Ps 波动；Z 域纳入湍流则撞）| 不够格（工具）| N/A | B6 |
| B7-Q2 | TED 增益↔Doppler 映射湍流鲁棒性（环路 TF 联合建模则撞）| 待定量锚（借 0.42~0.66dB）| in | B7 |
| B9-Q3 | DRE 与载波同步正交性反向利用（纳入环路 H(z) 则撞）| 不够格 | in | B9 |
| B10-Q2 | Pilot-RLS 湍流鲁棒性（RLS 状态方程联合建模则撞）| 待定量锚 | in（星地 COSC 湍流）| B10 |
| **B11-Q2** | 湍流相位纳入 ML 似然（前馈不撞；环路 H(z) 联合建模则撞）| 待定量锚 | in（星地 FSO 湍流）| B11 |
| **B12-Q3** | 频域 CW pilot + MAP 时域 pilot 联合架构（联合状态方程纳入湍流+多普勒则撞）| 待定量锚 | in（星地 COSC 湍流）| B12 |

**未过四判据候选**（记录筛掉理由防复现，glossary.md 常见误用 1）：

| Q# | 未过理由 | 来源 |
|----|---------|------|
| B1-Q2 | sat.1553 自承"same pilot rate performs similarly"负面证据（判据4 ❌）| B1 |
| B2-Q1 | 0.6dB 陷阱（[79] vs 无 freeze 非增量）；≥1dB 存疑待全文（判据4 ⚠️）| B2 |
| B4-Q1 | optcom.2023 双反馈环无外部 dB 增量（判据4 ⚠️）| B4 |
| B4-Q3 | sat.1553 feedback open problem 无直接实例（判据2 ⚠️）| B4 |
| B5-Q2 | [60] Leven Mth-power 理论锚 范围 out 光纤 intradyne（范围硬门 ❌）| B5 |
| B5-Q3 | sat.1553 L558 粗 CFO 精度边界 待定量锚（判据4 ⚠️）| B5 |
| B5-Q4 | jlt.2023 频谱扫描视角参考 维度错位（判据4 ⚠️）| B5 |
| B6-Q3 | sin 鉴相器幅度衰落跨论文空白 待定量锚（判据4 ⚠️）| B6 |
| B7-Q3 | 双候选判决强噪声可靠性 鲁棒性证明非性能改进（判据2 ❌）| B7 |
| **B8 主判定** | **本篇无核心 Q#**：自相干绕过载波同步（载波同步冗余），与 B1-B7/B9-B12 正交（判据1-4 全 ❌ 不适用）| B8 |
| B8-Q1 | SCD mixing efficiency 前提失效 不够格/待定量（判据4 ❌）+ 范围 out 地面 FSO | B8 |
| B8-Q2 | SCD 调制格式边界 适用域边界非性能改进（判据2 ❌）+ 范围 out | B8 |
| B9-Q2 | 虚拟载波自相干湍流稳健性 待定量锚（判据4 ⚠️）| B9 |
| B10-Q3 | KRLS PS-64QAM ao.581648 待全文核验（摘要 4dB 无法溯源）| B10 |
| B11-Q3 | "FSO 适用"仿真验证缺口 验证范围非性能改进（判据2 ❌）| B11 |
| B12-Q1 | 频域 CW pilot 无 vs baseline dB gain（判据4 ❌ dB 维度）/ 结构性理论增量 | B12 锚 |

**Q# 清单判定（B 档 35 Q#）**：

- **四判据全过 3 个**（B3-Q2 / B9-Q1 / B11-Q1）—— 第一梯队 dB 达标（+2~3dB），但各有条件性（B9 baseline 内部对照 / B11 仅 (8,8)-16APSK + 仿真未建模 FSO / B3-Q2 范围 in 但分集增益不可全迁）。
- **边际够格 7 个**（B1-Q1 / B2-Q2 / B7-Q1 / B10-Q1 / B5-Q1 / B6-Q1 / B12-Q2）—— 第二梯队 dB 偏小或结构性优势，Go/Kill 留用户。
- **D006 边界 7 个**（B3-Q3/B6-Q2/B7-Q2/B9-Q3/B10-Q2/B11-Q2/B12-Q3）—— "前馈不撞/环路 TF 联合建模则撞"模式，潜在一致性研究方向（湍流相位建模边界），Go/Kill 留用户。
- **未过 18 个**（含 B8 主判定"无核心 Q#"）—— 记录筛掉理由防复现。

**Q# 综合观察线索（仅供用户排优先级参考，非结论，不塞方向给用户）**：

1. **第一梯队 dB 达标 3 个但各有条件性**：B3-Q2（+2~3dB 范围 in 但分集增益不可全迁）/ B9-Q1（~3dB 但 baseline 内部 w/o DRE 对照非传统相干载波同步）/ B11-Q1（+2dB 但仅 (8,8)-16APSK + 仿真未建模 FSO）。D005"赢传统 baseline 几 dB"硬达标，但 Go 判据要诚实评条件性。
2. **D006 边界模式 7 次是潜在一致性研究方向**——"湍流相位建模边界"（前馈层处理不撞，环路 TF 联合建模则撞）在 B 档 12 点中重复 7 次，是块 A/B/C/D（Q11/Q12 Paillier 分治）的延续。但 Go/Kill 留用户，本节只标模式。
3. **B8 特例"载波同步冗余"**——自相干绕过载波同步，提示"自相干架构替代传统载波同步链"是另一条潜在路线（B9 也走这条路 Q2），但 B8/B9 主场景都非星地。
4. **范围 out 比例较块 A/B 高**（~9/35 ≈ 26%）——B8×3 地面 FSO + B10×2/B12×2 光纤 + B3-Q1/B5-Q2 光纤。星地 in/in 倾向仍是主体（~24/35 ≈ 69%）。
5. **D011 种子"16-QAM CPR 扩展"落地**——B10（16-QAM pilot-RLS）+ B12 MAP（256-QAM）+ ao.581648（PS-64QAM KRLS），pilot-RLS→MAP→KRLS 升级链，但三者都光纤 out。

**诚实预期（总表阶段前置，非结论）**：

- 务实路线下 Go 判据 = 赢传统未优化 baseline 几 dB。B3-Q2/B9-Q1/B11-Q1 dB 达标，**形式上够 Go 门槛**。
- 但每个都有条件性（baseline 内部对照 / 仅特定调制 / 仿真未建模 FSO），用户排完优先级后对前几名判 Go/Kill 时要逐条诚实判定。
- D006 边界模式 7 次是潜在一致性研究方向，但 Go/Kill 留用户（本节守 D018 中性不判）。

### 载波同步 v2 文献条目（B 档 12 篇精简版）

> 每篇详细结构化提取（14+ 字段 + 7 子表）见 `papers/_read_notes/_B{N}-*.md`。

#### [L11] B1 pilot 窗口（sat.1553 + [60] Leven + [58] Martins）

- **DOI/来源**：10.1109/JLT.2024.3447553（sat.1553）+ 10.1109/LPT.2007.891893（[60] Leven）+ 10.1364/osac.438524（[58] Martins）
- **核心贡献**：sat.1553 LEO 星地相干 OSL pilot-aided 载波恢复（固定 phase-estimation window N）；[60] Leven Mth-power 理论锚（最优 N∝SNR）；[58] Martins 静态 pilot-rate×linewidth 优化。
- **关键 dB**：+1dB（sat.1553 pilot 场景4 vs VV+diff）/ 0.5dB 阈值（B1-Q2）
- **Q#**：B1-Q1（自适应 window N，倾向够格）/ B1-Q2（自适应 pilot rate，风险偏高）
- **笔记**：`papers/_read_notes/_B1-pilot-window-increment.md`（S003）

#### [L12] B2 deep fade 冻结（[79] Matsuda + sat.1553）

- **DOI/来源**：10.1117/12.2544050（[79] Matsuda SPIE 2020）+ sat.1553
- **核心贡献**：[79] FOE freeze 静态功率阈值 gate FOE（上行强湍 deep fade）；sat.1553 L440 自承"完全冻结在 SOP 漂移大时丢跟踪"。
- **关键 dB**：0.6dB（[79] vs 无 freeze 非增量，陷阱）/ +1dB（pilot 在 fade）
- **Q#**：B2-Q1（FOE freeze 自适应阈值，≥1dB 存疑）/ B2-Q2（freeze+pilot 双模切换，倾向够格）
- **笔记**：`papers/_read_notes/_B2-deep-fade-freeze-increment.md`（S003）

#### [L13] B3 子系统协同（LCOMM + jphot+oe + sat.1553 L790）

- **DOI/来源**：10.1109/JLT.2024.3447553（sat.1553 L790）+ 10.1364/jphot（jphot）+ 10.1364/oe（oe 合并）
- **核心贡献**：跨子系统共享 pilot + 依赖解耦联合协同（FOE+CPE+RSOP 一套 FPT）。jphot+oe 合并 +2~3dB 强湍 4 支路；LCOMM B3 视角 +0.9dB Q（光纤 DSCM out）。
- **关键 dB**：+2~3dB（jphot+oe）/ +0.9dB（LCOMM，范围 out 光纤 DSCM）
- **Q#**：B3-Q1（LCOMM 视角，够格但 out）/ B3-Q2（jphot+oe 合并，够格第一梯队）/ B3-Q3（sat.1553 L790 open problem，D006 边界）
- **笔记**：`papers/_read_notes/_B3-subsystem-coordination-increment.md`（S003）

#### [L14] B4 双反馈环（optcom.2023 + jlt.2023 PCS + sat.1553）

- **DOI/来源**：10.1364/optcom（optcom.2023 双反馈环）+ 10.1109/jlt.2023.3281082（jlt.2023 PCS）+ sat.1553
- **核心贡献**：optcom.2023 外环 PADE 大动态 + 内环 V-V RFO 精补 + 前馈 V-V 相位（±920MHz @ 0.5dB）；jlt.2023 PCS+符号率自适应（+70~100 Gbps 维度错位）。
- **关键 dB**：±920MHz @ 0.5dB / MSE 4×（optcom.2023）/ +70~100 Gbps（jlt.2023 维度错位）
- **Q#**：B4-Q1（双反馈环本体，部分）/ B4-Q2（jlt.2023 PCS 维度错位，够格）/ B4-Q3（sat.1553 feedback open problem，待定量）
- **笔记**：`papers/_read_notes/_B4-dual-feedback-loop-increment.md`（S003）

#### [L15] B5 短时谱粗 CFO（optcom.2024 全文核验 + [60] Leven + sat.1553 + jlt.2023）

- **DOI/来源**：10.1016/j.optcom.2024.130981（B5 锚 optcom 2024，全文 252 行）+ 10.1109/LPT.2007.891893（[60]）+ sat.1553 + jlt.2023
- **核心贡献**：分块 FFT + 正负功率谱面积比（式 2-4）+ 星历预测调 LO；盲估无 pilot 不依赖 MIMO DSP。全文核验升级：±4.5GHz 覆盖 LEO Doppler + 残频 <140MHz + 灵敏度 −48dBm@BER 1e-3。
- **关键 dB**：±4.5GHz（范围覆盖结构性优势）/ 残频 <140MHz / −48dBm@BER 1e-3 / 无 vs baseline dB（dB 维度不够格）
- **Q#**：B5-Q1（本体，范围结构性优势 in 星地 LEO 下行）/ B5-Q2（[60] Leven 理论锚，out 光纤）/ B5-Q3（sat.1553 粗 CFO 精度边界，待定量）/ B5-Q4（jlt.2023 视角参考，维度错位）
- **笔记**：`papers/_read_notes/_B5-short-time-spectrum-cfo-increment.md`（S003+全文核验段）

#### [L16] B6 Z-ODPLL（Photonics2023 + col202018 + IEICE Z-domain）

- **DOI/来源**：10.3390/photonics10050493（B6 锚 Photonics 2023）+ col202018（混合 OPLL）+ IEICE Z-domain Z-ODPLL 根基
- **核心贡献**：atan2 鉴相器 KD 与 Ps 解耦（全湍流态保锁 σ=2.6°/0.42dB + 容 30ns 延迟 vs sin 仅 6ns）；Z-ODPLL H(z) 建模（固定 Kd 掩盖 Ps 波动）。
- **关键 dB**：σ=2.6°/0.42dB + 容 30ns 延迟（定性保锁非几 dB）
- **Q#**：B6-Q1（atan2 鉴相器解耦，边际够格）/ B6-Q2（Z-ODPLL H(z) 建模，D006 边界工具 N/A）/ B6-Q3（sin 鉴相器跨论文空白，待定量）
- **笔记**：`papers/_read_notes/_B6-z-odpll-increment.md`（S003）

#### [L17] B7 Gardner TED（ofc.2026.w2a.62 + Gardner 1986 + backward refs 5）

- **DOI/来源**：10.1364/ofc.2026.w2a.62（B7 OFC 2026 poster，全文 90 行）+ 10.1109/tcom.1986.1096561（Gardner TED 1986）+ backward refs 5 篇
- **核心贡献**：Gardner TED 增益随符号净相位旋转量周期变化作 Doppler 指纹，扫频+双候选试补偿+TED2 标准差判决。0.6dB @ BER 2e-2 + 1.9×范围(0-23GHz) + OSNR 10dB 可解调。baseline = PSA FOE（Vieira 2023）。
- **关键 dB**：0.6dB @ BER 2e-2 / 1.9×范围（0-23GHz vs PSA FOE 0-12GHz）/ OSNR 10dB 可解调（常规失败点）
- **Q#**：B7-Q1（Gardner TED 复用 FOE，边际够格）/ B7-Q2（TED 增益湍流鲁棒性，D006 边界）/ B7-Q3（双候选判决可靠性，不够格）
- **笔记**：`papers/_read_notes/_B7-gardner-ted-increment.md`（S004）

#### [L18] B8 RL+GS 自相干（jocn.468220，载波同步冗余特例）

- **DOI/来源**：10.1364/jocn.468220（B8 JOCN 2023，全文 604 行）
- **核心贡献**：heterodyne + square-law + LPF 使 CFO/相位噪声自消除（Eq.6），PAM4 直接判决，**载波同步需求被绕过**（行 119 linewidth 不敏感）。与 B1-B7/B9-B12 本质正交。
- **关键 dB**：无 vs baseline dB gain（性能以 BER orders of magnitude 表达）
- **Q#**：**B8 主判定"无核心 Q#"**（载波同步冗余）+ B8-Q1（mixing efficiency 前提失效，不够格 out）/ B8-Q2（调制格式边界，不够格 out）
- **笔记**：`papers/_read_notes/_B8-rl-gs-self-coherent-increment.md`（S005）

#### [L19] B9 虚拟载波自相干+DRE（jlt.2023.3270673 + apn.3.3.036007）

- **DOI/来源**：10.1109/jlt.2023.3270673（B9 锚 JLT 2023，306 行）+ 10.1364/apn.3.3.036007（DRE Gold OA，用户手动下 440 行）
- **核心贡献**：DRE = Digital Resolution Enhancer（TX 侧动态量化+block-wise Viterbi 把量化噪声挤出带外）；虚拟载波 = 数字域 DSP 插入 carrier tone。自相干架构**用架构"绕开"传统载波同步链**。~3dB @ 3PNOB（行 243/253 四处一致）与 B3-Q2 +2~3dB 同量级第一梯队，但 baseline 是内部 w/o DRE 对照。
- **关键 dB**：~3dB @ 3PNOB / ~1dB @ 4 PNOB / ~0.5dB @ 5 PNOB / ~0.8dB long-term 含湍流（行 243/253）
- **Q#**：B9-Q1（DRE 迁移自相干 FSO 深湍流，够格量级达标 baseline 内部对照）/ B9-Q2（自相干绕开载波同步湍流稳健性，待定量）/ B9-Q3（DRE 正交性反向利用，D006 边界）
- **笔记**：`papers/_read_notes/_B9-virtual-carrier-dre-increment.md`（S005）

#### [L20] B10 16-QAM pilot-RLS（s11107-024 + ao.581648 D011 种子）

- **DOI/来源**：10.1007/s11107-024-01019-2（B10 锚 2024，318 行）+ 10.1364/ao.581648（ao.581648 PS-64QAM KRLS，Optica AO 订阅墙仍缺全文）
- **核心贡献**：导频驱动 RLS 把 CFO+PN 塞进同一线性回归（h1→CFO/h0→PN），128 pilot 训练后切 decision-directed 反馈环，替代 BPS+4OPM。高 CFO(10GHz)/高线宽(1.45MHz) 鲁棒。D011 种子"16-QAM CPR 扩展"落地，ao.581648 PS-64QAM KRLS 承接（同作者团队 Deka/Krishnamurthy）。
- **关键 dB**：复杂度 20RM+12RA/symbol（无统一 vs baseline dB gain）
- **Q#**：B10-Q1（Pilot-RLS 联合 CFO+PN，边际够格 out 光纤待迁移）/ B10-Q2（湍流鲁棒性，D006 边界）/ B10-Q3（ao.581648 KRLS，待全文核验摘要 4dB）
- **笔记**：`papers/_read_notes/_B10-16qam-pilot-rls-increment.md`（S005）

#### [L21] B11 NDA-ML STO+CPE（lpt.2024.3523478）

- **DOI/来源**：10.1109/LPT.2024.3523478（B11 PTL 2025，全文 226 行）
- **核心贡献**：NDA-ML 联合估计 STO+CPE 闭式解——升 M₀ 次幂盲去调制相位→STO+CPE 化为单正弦 freq+phase→Wang[13] ML 闭式 τ̂/φ̂。+2dB SNR gain @ (8,8)-16APSK @ 7% HD-FEC vs DA ML（行 181/191）。**前馈闭式 ML 无环路 TF 不撞 D006**。声明 FSO 但仿真未建模 FSO 信道（行 33 假设湍流/Doppler 已补偿）。
- **关键 dB**：+2dB SNR gain @ (8,8)-16APSK（行 181/191 双处一致）/ 1dB SNR cost 换 CLW 容限 / >2× PN variance tolerance / STO 概率 1 @ −10dB SNR
- **Q#**：B11-Q1（NDA-ML 联合 STO+CPE，够格量级达标下沿+2dB，条件性强仅 (8,8)-16APSK + 仿真未建模 FSO）/ B11-Q2（湍流相位纳入 ML 似然，D006 边界）/ B11-Q3（"FSO 适用"仿真验证缺口，不够格验证范围维度）
- **笔记**：`papers/_read_notes/_B11-nda-ml-sto-cpe-increment.md`（本轮 S006）

#### [L22] B12 频域 pilot（TCOMM.2022.3171809 + MAP oecc-psc62146）

- **DOI/来源**：10.1109/TCOMM.2022.3171809（B12 锚 TCOMM 2022，全文 590 行，"In-Band and Out-of-Band Frequency Domain Pilots"）+ 10.23919/oecc-psc62146.2025.11109607（MAP OECC/PSC 2025，用户 2026-07-04 手动下 150 行）
- **核心贡献**：B12 锚频域 CW pilot 前馈相位估计（in-band/out-of-band + improved 估计器≈MVU + 最优 SPR 解析，Chalmers Eriksson 团队）；MAP 联合 ML/MAP 相位估计（256-QAM + AOPN + block-wise 并行，BNU-HKBU Kam 团队）。MAP 是 B12 锚的 citer/对照方向（pilot-aided 大类下时域 vs 频域机制独立）。两篇均 out（通用/光纤 DCI），迁移星地是 Q# 维度。
- **关键 dB**：B12 锚无 vs baseline dB gain（仅内部估计器 vs CRLB；SPR 失效点 −10/10dB 行 429；18-19dB OSNR 仿真条件 行 517）/ MAP SNR penalty 4dB @ 100GBaud/150kHz vs PA ML 5dB / PA 7.5dB（行 115）
- **Q#**：B12-Q1（频域 CW pilot 迁移星地，dB 不够格/结构性理论增量 out）/ B12-Q2（MAP 迁移星地高阶 QAM，边际够格同族 dB out）/ B12-Q3（频域+时域 pilot 联合架构，D006 边界 in 星地湍流）
- **笔记**：`papers/_read_notes/_B12-freq-domain-pilot-increment.md`（本轮 S006）

### 载波同步 v2 B1-B12 全 12 点总表（35 Q#，D018 中性不判 Go/Kill）

> **🔴 守 D018 中性提取**——本表只标 D006/D005/范围三维，**不判 Go/Kill**。Go/Kill 是用户的，排完优先级后对前几名做。
> **35 Q# 计数修正**：S005 原报"26"是 bug，实际 B1-B10=29（B8 主判定+2=3 非"主+2=2"），+B11×3+B12×3=35。
> 详细 M-C-A + 三维判定见各 B 点笔记 `papers/_read_notes/_B{N}-*.md`。

| B 点 | Q# | M-C-A 浓缩 | 撞 D006 | D005 够格 | 范围 | 关键 dB/量级 |
|------|-----|-----------|--------|----------|------|------------|
| **B1 pilot 窗口** | B1-Q1 | 自适应 window N | 不撞 | 倾向够格（+1dB 有风险）| in | +1dB |
| | B1-Q2 | 自适应 pilot rate | 不撞 | 风险偏高（负面证据）| in | 0.5dB 阈值 |
| **B2 deep fade 冻结** | B2-Q1 | FOE freeze 自适应阈值 | 不撞 | ≥1dB 存疑待全文 | in | 0.6dB 陷阱 |
| | B2-Q2 | freeze+pilot 双模切换 | 不撞 | 倾向够格增量未量化 | in | +1dB |
| **B3 子系统协同** | B3-Q1 | LCOMM B3 视角 | 不撞 | 够格（+0.9dB）| **out 光纤 DSCM** | +0.9dB Q |
| | **B3-Q2** | jphot+oe 合并 | 不撞 | **够格（+2~3dB 第一梯队）**| in | **+2~3dB** |
| | B3-Q3 | sat.1553 L790 跨子系统 | **边界** | 待定量锚 | in | 借 +0.9~3dB |
| **B4 双反馈环** | B4-Q1 | optcom.2023 双反馈环本体 | 不撞（边界）| 部分 | in | ±920MHz@0.5dB |
| | B4-Q2 | jlt.2023 PCS+符号率自适应 | 不撞 | 够格（维度错位）| in | +70~100 Gbps |
| | B4-Q3 | sat.1553 feedback open problem | 不撞 | 待定量锚 | in（含 ISL 边界）| 无直接实例 |
| **B5 短时谱粗 CFO** | B5-Q1 | B5 本体短时谱粗 CFO（全文核验升级）| 否（前馈功率比全文无湍流）| 不够格 dB / 范围结构性优势 | **in 星地 LEO 下行确证** | ±4.5GHz / 残频<140MHz / −48dBm |
| | B5-Q2 | [60] Leven Mth-power 理论锚 | 不撞 | 够格 | **out 光纤 intradyne** | 7dB penalty |
| | B5-Q3 | sat.1553 L558 粗 CFO 精度边界 | 不撞 | 待定量锚 | in | 残频 10⁻³fs |
| | B5-Q4 | jlt.2023 频谱扫描 Doppler 视角 | 不撞 | 够格（维度错位）| in | +70~100 Gbps |
| **B6 Z-ODPLL** | B6-Q1 | atan2 鉴相器 KD 与 Ps 解耦 | 不撞 | 边际够格（定性保锁非几 dB）| in | σ=2.6°/0.42dB/容 30ns |
| | B6-Q2 | Z-ODPLL H(z) 建模 | **边界（只标不砍）**| 不够格（工具）| N/A | — |
| | B6-Q3 | sin 鉴相器幅度衰落跨论文空白 | 不撞 | 待定量锚 | in | 无 |
| **B7 Gardner TED** | B7-Q1 | Gardner TED 复用 FOE | 否 | 边际够格（0.6dB+1.9×范围/10dB）| in | 0.6dB@BER 2e-2 / 1.9×范围 |
| | B7-Q2 | TED 增益湍流鲁棒性 | **边界（只标不砍）**| 待定量锚 | in | 借 0.42~0.66dB |
| | B7-Q3 | 双候选判决强噪声可靠性 | 否 | 不够格 | in | 无 |
| **🔵 B8 RL+GS 自相干** | 🔵 **B8 主判定** | **本篇无核心 Q#**（载波同步被绕过）| 否（开环前馈）| **不适用** | **out 地面 FSO** | 无 vs baseline dB |
| | 🔵 B8-Q1 | SCD mixing efficiency 前提失效 | 否 | 不够格/待定量 | out 地面 FSO | 无 B8 dB |
| | 🔵 B8-Q2 | SCD 调制格式边界 | 否 | 不够格（适用域边界）| out 地面 FSO | 无 |
| **🔵 B9 虚拟载波自相干+DRE** | 🔵 **B9-Q1（核心）** | DRE 迁移自相干 FSO 深湍流 | 否（TX 预处理）| **够格（~3dB 第一梯队，baseline 内部对照）**| in 倾向→待迁移星地 | **~3dB** @ 3PNOB（行 243/253）|
| | 🔵 B9-Q2 | 自相干绕开载波同步湍流稳健性 | 否（自相干无 OPLL）| 待定量锚 | in 倾向→待迁移 | 无 |
| | 🔵 B9-Q3 | DRE 与载波同步正交性反向利用 | **边界** | 不够格 | in | 无 |
| **🔵 B10 16-QAM pilot-RLS** | 🔵 **B10-Q1（核心）** | Pilot-RLS 联合 CFO+PN | 否（DSP 自适应滤波）| 边际够格（范围/鲁棒性）| **out 光纤/待迁移星地** | 复杂度 20RM+12RA/symbol |
| | 🔵 B10-Q2 | Pilot-RLS 湍流鲁棒性 | **边界** | 待定量锚 | in（星地 COSC 湍流）| 无 |
| | 🔵 B10-Q3 | KRLS PS-64QAM ao.581648 | 否（待全文核验）| 待全文核验（摘要 4dB）| out 光纤/待迁移 | 4dB OSNR（摘要待核验）|
| **🔵 B11 NDA-ML STO+CPE** | 🔵 **B11-Q1（核心）** | NDA-ML 联合 STO+CPE 闭式估计 | 否（前馈闭式 ML 无环路 TF，行 33 假设湍流已补偿）| **够格（+2dB 下沿，与 B3-Q2 同量级）**——条件性强（仅 (8,8)-16APSK + CLW 容限付 1dB cost）| in 倾向（声明 FSO）→ 仿真未建模 FSO 信道 | **+2dB** SNR gain @ (8,8)-16APSK（行 181/191）|
| | 🔵 B11-Q2 | 湍流相位纳入 ML 似然 | **边界**（前馈不撞；环路 H(z) 联合建模则撞）| 待定量锚 | in（星地 FSO 湍流）—— 候选维度 | 无 |
| | 🔵 B11-Q3 | "FSO 适用"仿真验证缺口 | 否（验证范围维度）| 不够格（验证缺口非性能改进）| in 倾向→待验证 | 无新增 dB |
| **🔵 B12 频域 pilot** | 🔵 **B12-Q1（锚核心）** | 频域 CW pilot 前馈相位估计迁移星地 | 否（前馈频域处理）| 不够格 dB / 结构性理论增量（improved≈MVU + 最优 SPR 解析）| **out 通用模型/待迁移星地** | 无 vs baseline dB（SPR 失效点 −10/10dB 行 429）|
| | 🔵 B12-Q2（MAP 核心） | MAP 联合 ML/MAP 256-QAM 迁移星地高阶 QAM | 否（前馈时域 pilot+块并行）| 边际够格（同族 dB：MAP vs PA 差 3.5dB / vs PA ML 差 1dB）| **out 光纤 DCI/待迁移星地** | MAP SNR penalty 4dB @ 100GBaud/150kHz vs PA ML 5dB / PA 7.5dB（行 115）|
| | 🔵 B12-Q3 | 频域+时域 pilot 联合架构 | **边界**（前馈级联不撞；联合状态方程/环路 H(z) 纳入湍流+多普勒则撞）| 待定量锚 | in（星地 COSC 湍流）—— 候选维度 | 无 |

#### 总表统计（B 档 35 Q#，修正 S005 计数 bug）

| 维度 | 计数 | Q# 编号 |
|------|------|---------|
| **总 Q# 数** | **35** | B1-B7 原 20 + B8 主判定+2=3 + B9×3 + B10×3 + **🔵 B11×3 + B12×3** |
| **撞 D006 明确撞** | **0** | （sat.1553 L70 旧扩展归档不计）|
| **撞 D006 边界（只标不砍）** | **7** | B3-Q3 / B6-Q2 / B7-Q2 / B9-Q3 / B10-Q2 / **🔵 B11-Q2 / B12-Q3** |
| **D005 倾向够格** | **10** | B1-Q1 / B2-Q2 / B3-Q1 / **B3-Q2** / B4-Q2 / B5-Q2 / B5-Q4 / B6-Q1 + **🔵 B9-Q1 / B11-Q1** |
| **D005 边际够格** | **4** | B7-Q1 / B5-Q1 + **🔵 B10-Q1 / B12-Q2** |
| **D005 待定量锚** | **8** | B2-Q1 / B3-Q3 / B4-Q1（部分）/ B4-Q3 / B5-Q3 / B6-Q3 / B7-Q2 / B9-Q2 / B10-Q2 + **🔵 B11-Q2 / B12-Q3** |
| **D005 不够格/不适用/待全文** | **13** | B1-Q2 / B5-Q1 dB 维度 / B6-Q2 / B7-Q3 + **🔵 B8 主判定不适用 / B8-Q1 / B8-Q2 / B9-Q3 / B10-Q3 待全文 / B11-Q3 / B12-Q1** |
| **范围 out** | **9** | B3-Q1（光纤 DSCM）/ B5-Q2（光纤 intradyne）/ B6-Q2（N/A）+ **🔵 B8 主判定/Q1/Q2（地面 FSO）/ B10-Q1（光纤）/ B10-Q3（光纤）/ B12-Q1（通用）/ B12-Q2（光纤 DCI）** |
| **范围 in / in 倾向** | **26** | 其余（含 in 倾向待迁移 B9-Q1/Q2 + B10-Q1/B11-Q1/B12-Q2 候选维度）|

#### D005 够格梯度（中性排序，供用户排优先级参考，**不判 Go/Kill**）

> 本梯度只按"D005 够格"程度的客观证据强度排，**不判 Go/Kill**。Go/Kill 是用户的，排完优先级后对前几名做。

**第一梯队（有明确 dB 增益 + 范围 in/in 倾向，+2~3dB 同门达标）**：
- **B3-Q2**（+2~3 dB 强湍 4 支路，复杂度降 75%）—— dB 最高，范围 in
- **🔵 B9-Q1**（~3dB @ 3 PNOB DRE）—— **dB 与 B3-Q2 同量级**，但 baseline 是内部 w/o DRE 对照非传统相干载波同步，in 倾向待迁移星地深湍流
- **🔵 B11-Q1**（+2dB SNR gain @ (8,8)-16APSK vs DA ML）—— **dB 达标下沿**，条件性强（仅 (8,8)-16APSK + CLW 容限付 1dB cost + 仿真未建模 FSO），声明 in 但仿真未验证
- B3-Q1（+0.9 dB Q）—— 范围 out（光纤 DSCM 待迁移论证）
- B1-Q1 / B2-Q2（+1dB）—— in
- B5-Q2（7dB penalty）—— 范围 out（光纤 intradyne 待迁移）

**第二梯队（结构性优势，dB 偏小或维度错位）**：
- B7-Q1（0.6dB + 1.9× 范围 0–23GHz + OSNR 10dB 极限）—— in
- **🔵 B10-Q1**（无统一 dB gain，优势在范围/鲁棒性 BPS+4OPM 失效区）—— out 光纤 / 待迁移星地 in 候选
- **🔵 B12-Q2**（MAP vs PA 差 3.5dB / vs PA ML 差 1dB 同族 dB）—— out 光纤 DCI / 待迁移星地 in 候选
- B4-Q2 / B5-Q4（+70~100 Gbps 吞吐维度错位）—— in
- B5-Q1（±4.5GHz 覆盖 LEO Doppler）—— in
- B6-Q1（定性保锁 σ=2.6°/0.42dB + 30ns）—— in

**第三梯队（待定量锚 / open problem 级 / 待全文）**：
- B2-Q1 / B3-Q3 / B4-Q1 / B4-Q3 / B5-Q3 / B6-Q3 / B7-Q2 / B9-Q2 / B10-Q2 + **🔵 B11-Q2 / B12-Q3** + **🔵 B10-Q3 待全文（摘要 4dB）**

**第四梯队（风险偏高/不够格/不适用）**：
- B1-Q2 / B6-Q2 / B7-Q3 / B9-Q3 / B11-Q3 / B12-Q1 + **🔵 B8 主判定（无核心 Q# 自相干绕过载波同步）/ B8-Q1 / B8-Q2**

#### 关键观察（中性，辅助用户排优先级）

1. **🔵 B11-Q1 +2dB 跻身第一梯队**——继 B9-Q1 后**第二个达第一梯队量级**的非 B3 候选（+2dB vs DA ML @ 7% HD-FEC，行 181/191 双处一致）。与 B3-Q2 +2~3dB / B9-Q1 ~3dB 同量级，但条件性强（仅 (8,8)-16APSK + CLW 容限付 1dB cost + 声明 FSO 但仿真未建模 FSO 信道）。
2. **🔵 D006 边界模式扩展到 7 次**（原 5 + B11-Q2 + B12-Q3）——"前馈/工具层不撞，环路 TF 联合建模则撞"模式在 B 档 12 点中重复出现 7 次，是潜在一致性研究方向（湍流相位建模边界），与块 A/B/C/D（Q11/Q12 Paillier 分治）延续。
3. **🔵 B12 双视角**（锚 TCOMM 2022 + MAP OECC 2025）——B12 锚是频域 CW pilot 理论框架（improved 估计器≈MVU + 最优 SPR 解析），MAP 是时域 pilot-aided 256-QAM（MAP vs PA 差 3.5dB 同族 dB）。两篇 pilot-aided 大类下时域 vs 频域机制独立，MAP 是 B12 锚的 citer 非直接延伸。
4. **B8 特例"载波同步冗余"持续成立**——B8 自相干绕过载波同步（载波同步需求被整体消除），与 B1-B7/B9-B12 改进载波恢复正交。提示"自相干架构替代传统载波同步链"是另一条潜在路线，但 B8/B9 主场景都非星地。
5. **范围 out 比例较 S005 统计微调**（7→9/35 ≈ 26%）——新增 B12-Q1（通用模型 out）/ B12-Q2（光纤 DCI out）。星地 in/in 倾向仍是主体（26/35 ≈ 74%）。
6. **dB 量级 vs 同门学位论文**：同门 2-4dB 区间，本表第一梯队 B3-Q2 +2~3dB / B9-Q1 ~3dB / B11-Q1 +2dB 达标，B1-Q1/B2-Q2 +1dB 偏下沿，B7-Q1 0.6dB 偏低。**0.5dB 阈值**（D008 FR-21 参考）下，B6-Q1/B7-Q1 的 0.6dB 级刚过线。

---

## 双偏振 OSL 精读沉淀（2026-07-10，GW Step 3 双偏振空间解锁后重走）

> 背景：scenario-transfer-pivot D003 解锁双偏振空间后，按 FR-22 从 GW Step 1 重走地勘。本节是双偏振星地光通信 DSP 子方向的精读沉淀，与上方载波同步 v2 沉淀并存（不同搜索空间）。9 篇新精读 + sat.1553 §6 补读。精读笔记在 `papers/_read_notes/{paper_id}.md`。

### 双偏振 OSL 文献条目（9 篇精读）

#### [L-DP1] Multi-Aperture MIMO 2N×2 Adaptive Equalizer (JLT 2023, c=15, 10.1109/JLT.2023.3276637)
- 核心：复值 MIMO 2N×2 蝶形均衡器 + blind CMA，把多孔径偏振复用信号的偏振解复用+combining 统一为单个均衡设计。Ju 团队（青岛大学+CETC）。
- 双偏振处理：2N×2 MIMO 蝶形（N 个 2×2），共享 LO。
- 建模假设：Gamma-Gamma 强度闪烁(σ_I²=0.5/1)；2×2 偏振串扰矩阵；**湍流相位扰动/动态相干时间未建模**（准静态）。
- 问题 M-C-A：传统 combining(MRC/EGC/SC)单偏振无法对齐 PM 偏振态→需 MIMO 均衡（过 4/4 判据）。
- 角度素材：失效=维度缺失（单偏振算法无偏振态对齐）；方法族占点=**首创**多孔径 PM blind combining via single MIMO；open problem=大线宽需优化载波相位跟踪（未解决）。

#### [L-DP2] Blind skew compensation + widely linear equalizer (OE 2023, c=5, 10.1364/oe.498562)
- 核心：复值 MIMO 4N×2 WL 均衡器（加共轭支路），补偿 I/Q imbalance/skew + combining。Ju 团队姊妹篇。
- 双偏振处理：4N×2 WL（含共轭蝶形支路）。
- 建模假设：WL 信道（共轭项刻 I/Q 失衡）；被动线性湍流→严格线性 2×2；**湍流无 PDF 量化，相位扰动未建模**。
- 问题 M-C-A：SL 均衡器无共轭支路→不能处理 I/Q 失衡（过 4/4 判据）。
- 角度素材：失效=维度缺失（SL 无共轭支路）+能力不足（WL massive aperture 收敛退化）；open problem=massive aperture 超低 OSNR 抽头收敛精度+频域实现+PM-16QAM 快收敛（三连未解决）。

#### [L-DP3] 10 Gbps Coherent Receiver for FSO (RPIC 2023, c=3, 10.1109/RPIC59053.2023.10530744)
- 核心：标准光纤相干 DSP 流水线移植 FSO/OISL，删去 GVD 补偿。
- 问题 M-C-A：标准 DSP 移植 FSO，低 SNR+CFO+偏振旋转（过 2/4 判据，C/D 弱）。

#### [L-DP4] Gray-Coded DP-16QAM MIMO-FSO (JCNC 2025, c=3, 10.1155/jcnc/4243779)
- 核心：DP-16QAM + 4×4 MIMO 空间分集(EGC) + 完整 DSP（GSOS+CMA-RD+FOE+BPS），纯仿真。
- 建模假设：Gamma-Gamma(弱强)+天气模型；**PMD 建模为接收延迟项但未时变**；无 Doppler。
- 问题 M-C-A：DP-16QAM+MIMO 在 4 天气×弱强湍流（过 4/4 判据，最完整）。

#### [L-DP5] 56-GBaud GEO DP-QPSK Feeder DSP (ICSOS 2023, c=1, 10.1109/ICSOS59710.2023.10490279)
- 核心：定制 GEO feeder DSP（盲粗估+数据辅助精估混合）+ modified CMA 简化均衡器，E_s/N_0 低至 −6dB。
- 建模假设：6 类损伤（X-Y skew 15符号/PDL/SOP旋转/CFO/Wiener PN/ASE）；**湍流未显式仿真**（折入 SNR 余量）。
- 问题 M-C-A：定制 DSP 治极低 SNR 致 COTS 锁不上（过 2/4 判据）。
- 角度素材：open problem=深衰落跨帧挂起恢复（明确需进一步研究）。

#### [L-DP6] Data-Aided Multi-Format DSP (WiSEE 2024, c=0, 10.1109/WiSEE61249.2024.10850117)
- 核心：数据辅助多格式均衡器（OFDM 频域正交分偏振信道估计+ZF/MMSE+导频/BPS 两级 CPE），3.2km 外场验证。
- 双偏振处理：OFDM 子载波奇频=X/偶频=Y 频域正交。
- 问题 M-C-A：数据辅助多格式 DSP 治低 SNR 盲均衡不稳（过 3/4 判据）。

#### [L-DP7] Bootstrapping Blind Equalizer VAE (TCCN 2026, c=0, 10.1109/TCCN.2025.3631007)
- 核心：重导含非酉 DP-MIMO H+实器件损伤的 VAE ELBO 损失，VAELP(格点)/VAEMR(模值环)盲均衡器。8 层实值 1D-CNN。
- 建模假设：DP 频域 Jones 矩阵(静态旋转+DGD+GVD)；湍流=1m 物理湍流板(r0=0.4mm)非统计信道。
- 问题 M-C-A：VAE 变分推断替代 CMA 解决 DP FSO 实器件损伤下此前 VAE 失效（过 4/4 判据，全面基线对比 200×少迭代+5dB 功率预算）。

#### [L-DP8] Jitter-Resistant CMA (ACP 2025, c=0, 10.1109/ACP66871.2025.11350394)
- 核心：JR-CMA = CMA + AGC 稳功率 + 误差阈值重置防深衰落发散 + 自适应步长。
- 问题 M-C-A：三机制增强 CMA 抗 pointing jitter 致深衰落发散（过 3/4 判据，基线仅 CMA）。

#### [sat.1553 §6 补读] 偏振解复用/自适应均衡层
- §6 核心：2×2 蝶形自适应均衡器(N-tap/两级 1-N/N-1 三架构)+CMA/DA-LMS/MMSE，单孔径双偏振解复用。SOP 用 Jones 旋转 θ=ωt 建模。
- §6 关键 open problem：**CMA 在 scintillation fade 发散概率"未被分析"**（综述点名盲区）；SOP 模型过简化（§6.3 末明言）；step size μ 无理论最优。

### 角度素材跨篇聚合视图（D002 schema ⑥）

#### ① 失效点 × 性质矩阵（多命中格=强失效信号）

| 失效对象 \ 失效性质 | 维度缺失 | 能力不足 | 假设不成立 | 未被研究 |
|---|---|---|---|---|
| **算法（CMA/V&V/BPS）** | — | L-DP2(WL收敛退化) L-DP8(深衰落发散) | L-DP3(低SNR崩塌) L-DP5(V&V 4次幂放大) | **sat.1553§6(CMA fade发散未分析)** |
| **架构（单偏振combining/SL均衡）** | L-DP1(单偏振无偏振对齐) L-DP2(SL无共轭支路) | — | — | — |
| **假设（准静态信道）** | — | — | **9篇共性(湍流相位扰动/SOP-湍流耦合未建模)** | — |
| **COTS（400ZR/DVB-S2）** | — | L-DP5(低SNR帧捕获失败) | L-DP5/L-DP6(设计为高SNR干扰受限) | — |

**强信号**：①"假设—准静态信道—9篇共性"是跨所有论文的共同简化；②"算法—未被研究—CMA fade 发散"是 sat.1553 综述点名的领域共识盲区。

#### ② 方法族占点地图

| 方法族 | 占点密集度 | 代表论文 | 状态 |
|---|---|---|---|
| **自适应均衡/偏振解复用** | 🔴 高密度（撞车风险） | L-DP1/2/5/6/7/8 + sat.1553§6 | CMA/MIMO/WL/VAE 全占，Ju 团队主导多孔径子方向 |
| 载波同步（双偏振联合 CPE） | 🟡 中 | L-DP4(GSOS+CMA-RD) L-DP5(联合CPE) L-DP6(双偏振BPS) | 部分覆盖，非主创新点 |
| 信道估计 | 🟡 中 | L-DP6(OFDM频域正交) | data-aided 占点 |
| 定时同步 | ⚪ 低 | sat.1553§3 | 双偏振联合 TED 未专门研究 |

#### ③ open problem 聚合表（多篇独立指向=共识缝=最安全角度来源）

| open problem | 论文来源 | 独立性 | 共识度 |
|---|---|---|---|
| **动态 SOP 跟踪（连续漂移而非静态旋转角）** | sat.1553§6 + L-DP1 + L-DP2 + L-DP5 + L-DP6 | 5 篇独立（全静态建模） | ⭐⭐⭐ 最强共识缝 |
| **CMA 在 scintillation fade 发散概率未被分析** | sat.1553§6（综述点名）+ L-DP8(深衰落发散实证) | 综述+实证 | ⭐⭐⭐ |
| **湍流深衰落跨帧挂起恢复** | L-DP5(明确open) + L-DP6(DSP outage) | 2 篇独立 | ⭐⭐ |
| 时变 Doppler（LEO GHz/s 变化率）| L-DP3/L-DP5(均静态CFO) | 2 篇共性缺口 | ⭐⭐ |
| 真实星地链路验证 | L-DP3/4/5/6(均地面/仿真) | 4 篇共性缺口 | ⭐⭐（但非 DSP 算法贡献） |

#### ④ 根因层级 × 性质定位（一根因覆盖多现象=根方向）

**最强根方向**：**信道建模层 × 假设错/建模不足**——9 篇共性把湍流建模为准静态 SNR 分布，SOP-湍流耦合/动态相干时间未建模。这个根因覆盖了"CMA fade 发散""动态 SOP 跟踪缺失""湍流深衰落跨帧恢复"多个现象。从"逐个现象找方法"升级到"按根因聚类"=从信道建模的动态性入手。

#### ⑤ 切法 × idea 来源分布

| idea 来源 | 切法 | 论文 |
|---|---|---|
| 迁移驱动 | 架构替换（光纤2×2→FSO多孔径2N×2） | L-DP1/L-DP2 |
| 需求驱动 | 架构替换（COTS不适配→定制低SNR DSP） | L-DP5/L-DP6 |
| 理论驱动 | 工具借用（VAE变分推断替代CMA） | L-DP7 |
| 实证驱动 | 参数调度（CMA+AGC/重置/变步长） | L-DP8 |
| 组合驱动 | 联合建模（WL复分析×多孔径需求） | L-DP2 |

**高成功率路径**：迁移驱动+架构替换（L-DP1/2，Ju 团队两次成功）+ 需求驱动+架构替换（L-DP5/6，低 SNR 定制）。理论驱动（VAE）是最新但验证不充分。

### 研究问题清单 Q#（双偏振 OSL 子方向，过 glossary 四判据）

> 四判据：A=具体技术矛盾（非"没人做过"）B=有方法产出形态 C=有2019+baseline D=能做对比实验

| Q# | M-C-A（M=方法 C=条件场景 A=失效/不足） | A | B | C | D | 来源论文 |
|---|---|---|---|---|---|---|
| **Q-DP1** | M=动态SOP跟踪均衡器 C=双偏振星地湍流(连续SOP漂移) A=现有CMA/MIMO均衡假设准静态SOP(9篇共性)，动态SOP下系数跟踪滞后致偏振解复用失败 | ✅ | ✅(均衡器设计) | ✅(L-DP1/2/sat.1553) | ✅(动态vs静态SOP对比) | sat.1553§6+L-DP1/2/5/6 共识缝 |
| **Q-DP2** | M=CMA fade发散分析+鲁棒增强 C=双偏振星地GG湍流(闪烁深衰落) A=sat.1553点名"CMA在scintillation fade发散概率未被分析"，L-DP8实证深衰落致系数发散 | ✅ | ✅(发散概率界/鲁棒CMA) | ✅(L-DP8/sat.1553§6) | ✅(fade场景vs非fade) | sat.1553§6+L-DP8 |
| **Q-DP3** | M=湍流深衰落跨帧DSP恢复 C=双偏振星地(帧间湍流衰落) A=L-DP5点名"深衰落跨帧挂起恢复open"，L-DP6 DSP outage(BER>0.44锁定失败) | ✅ | ✅(恢复机制设计) | ✅(L-DP5/6) | ✅(有恢复vs无恢复) | L-DP5/6 |

### 双偏振 OSL 综合分析

**方法分类**（双偏振子方向 4 类）：
1. **偏振解复用/MIMO 均衡（6 篇，最密集）**：CMA 蝶形(L-DP1/2/5/8) + VAE(L-DP7) + data-aided(L-DP6)。Ju 团队主导多孔径扩展（2N×2→4N×2）。
2. **双偏振 FSO 相干系统 demo/分析（4 篇）**：标准光纤 DSP 移植/定制(L-DP3/5) + 系统性能分析(L-DP4/6)。
3. **载波同步（双偏振联合）**：sat.1553 §4/5 + L-DP4/5/6 的 CPE 组件（非主创新点）。
4. **神经网络盲均衡（1 篇，新兴）**：L-DP7 VAE。

**已知局限**（领域级空白原料，非问题）：
- 准静态信道假设是 9 篇共性简化（湍流相位扰动/SOP-湍流耦合未建模）
- CMA 在 scintillation fade 发散概率未被分析（sat.1553 点名）
- 动态 SOP 跟踪缺失（5 篇独立静态建模）
- 真实星地链路验证缺失（4 篇地面/仿真）

**2-3 年趋势**：
- 多孔径数字合并是 2023-2025 热点（Ju 团队连续两年两篇 JLT/OE）
- VAE/ML 盲均衡是 2025-2026 新兴（L-DP7 TCCN 最新）
- data-aided 替代 blind 在低 SNR 是共识方向（L-DP5/6 vs sat.1553 主张）
- CMA 鲁棒性增强（抗深衰落/jitter）持续有会议论文（L-DP8）

**D002 角度素材 schema 验证结论**（3 批 9 篇试用）：
- **可用**，信号提取充分。①失效点/②方法族占点/⑤切法最好填；③open problem 需摘英文原话+翻译工作量适中但信号最强。
- **改进建议**：④根因性质词表补"建模不足"（现只有假设错/能力不足，综述的"模型过简化"是第三态）；②"被继承"字段加"待查"兜底（cited-by 需外部数据）。
- 非 DRL 论文的状态/动作/奖励全填"不适用"冗余，可映射"等价代价函数/决策变量"。
- **验证通过，可进 gw-read.md**（守"先测不改协议"释放条件满足）。

---
