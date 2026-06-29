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
| 1 检索        | ✅   | 2026-05-29 + S003-S010 地勘五轮（landscape 683 主表） | 早期 21+6 条 + 地勘 683 主表 |
| 2 获取        | ✅   | 2026-06-26 | H004 块 A 7 篇 + H005 块 B 6 篇，OA + IEEE(blit) |
| 3 精读        | ✅   | 2026-06-26 | **本轮块 C 完成**：10 篇精读 + 综合分析 + Q# 清单 |
| 3.5 补充      | 🔄部分 | 2026-06-27 | 检索✅+召回Q11-Q13✅，下载精读债务（Paillier2020JLT/Rustum2026/Tang2024/Mosnier2025/Viterbi1983）| 块 D：盲区A/B定向补检索 + 召回旧B1资产 |
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
