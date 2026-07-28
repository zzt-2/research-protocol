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
| 3.5 补充      | ⚠带债豁免 | 2026-06-27 起；2026-07-23 D062 更新 | 历史补充检索、Q11-Q13 召回与载波同步 v2 精读沉淀均保留；Pilot-Jones backward/收敛门已闭合，4 篇直接竞品保持 `BLOCKED_NO_FULLTEXT`。D062 只豁免进入 Step 4a，不记 PASS。|
| 4a 可行性     | 🔄T010 B10 source-native adaptive pilot-RLS | 2026-06-28 起；2026-07-26 D017 更新 | Pilot-Jones fixed complex component rescue axis 已由 T005/D066/V040 scoped Kill；T006 组合 verdict 因 source/channel/statistics 身份缺口被拒收。当前 D017 只激活 B10 source-native carrier：先重建 128 contiguous pilot→DD fixed B10，identity 过门后同包比较 innovation freeze/adaptive forgetting；不进 Step 5。|
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
| Q14 | standard-CMA always-online 后接 additive NN residual：`z_out=z_CMA+gφ(z_CMA,context)` | 当前 GG+SOP/线性双偏振 OSL 接收模型（先固定单一 C，待 4a） | CMA 在多幅度/PCS、SOP 或 fading 条件下的失配是否留下稳定、可辨识且非简单 DSP 可覆盖的残差 | 在线 CMA 前端 + 小型监督 residual head；与 CMA-only、raw-ML、fixed+PI、oracle 及简单 DSP 对照 | ✅ M/C/A 已由 S038 L01/L04/L05 组合具体化 | ⚠️ **UNKNOWN**：有 online CMA 与 `b−a` residual 的邻近证据，但无 additive-cascade 直接证据，且当前 GG+SOP 模型的残差信息增量未验证 | ✅ CMA/RDE/ML/VAE-LE 作为可实现 baseline | ✅ BER/SER/Q²、swap rate、收敛长度、MAC/latency 可统一量化 | **Step 3 暂存**：5/5 全文精读，均为 direct/adjacent 分类；四判据 1/3/4 PASS、2 UNKNOWN，禁止据此进入 Step 4a A0/MVE | S038 L01–L05 |

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
| **Q-DP4** | M=保留2×2蝶形CMA主均衡器+针对收敛后SOP驱动lock swap的防跳变方法 C=双偏振星地FSO(SOP持续旋转sop_rate=4e-7即1krad/s) A=恒模代价2×2收敛点不唯一(任意酉旋转保恒模)，SOP慢旋时已正确收敛的权重跳到混淆X/Y次优解 | ✅ | ✅(防swap判据/约束/补偿协议) | ✅(standard-CMA Godard1980 + CA-CMA2025/B'类增强) | ✅(swap概率/BER恢复/CMA-oracle比值) | D014(SOP串扰真因)+R007(B类=0)+R008(占点排除) |

> **Q-DP4 立项说明（2026-07-14 S021，GW Step 4a 维度 A0）**：S020 复盘确认 BER 真因=D014 SOP 驱动 polarization lock swap 后，R007 系统验证"保留 CMA、专攻收敛后 SOP 驱动跳变"=B 类真方法空白（117 命中 0 篇专题），R008 排除最危险两项占点（CA-CMA 静态+A类不占 / NPCA 整体替换不可移植不占）。本轮正式立 Q-DP4 并走 A0§0-§6 预检，**A0 通过（无致命，带 §3 警告+§6 张力）**。
>
> **差异化定位（不撞 D001/D016）**：
> - ≠ D001 Kill（Q-DP1"动态SOP跟踪失效"——均衡器够用）：Q-DP4 均衡器跟踪够用（不否认），但恒模代价让已收敛权重跳错解。D014 SOP×f_G 矩阵铁证：SOP=0 时 CMA/oracle ratio=1.0（跟踪没问题），SOP=4e-7 时升 1.9-7.9×（收敛后跳变）。
> - ≠ D016 Kill（"通用恒模多解解法在 FSO 复测"=A类静态复测）：Q-DP4 是"收敛**后**动态 SOP 驱动跳变"的**针对性**方法，非通用静态解法复测。R007/R008 确认 A 类静态解法成熟但不覆盖动态收敛后跳变。
> - B 类精确判据（保留 CMA 攻收敛后动态跳变）= 0 篇专题论文（R007），R008 排除最危险两项后仍成立。
>
> **方法形态（不预设 ML，A0§2 诚实判断）**：形态1 跳变检测+权重回滚（响应式）/ 形态2 预防性 cost 约束（CA-CMA J_XCA 持续运行形态的填补）/ 形态3 混合 SOP 跟踪补偿。可能是经典 DSP（形态2/3）或含 ML（形态1 检测器）。详见 R007 Q3。
>
> **增量定位修正（主控核验 S021 后，D018 双口径）**：原"防 swap 本身"（省帧头<1%）增量小。修正后定位"降 CMA PI-BER 6× 残余差距"——即使 swap 消歧后 CMA PI-BER 0.03174 仍比 ML 0.00523 差 6×（D018 数据），防跳变机制若同时降这 6× 则增量大。**形态2（预防性约束）为 D MVE 首选**（同时攻 swap+漂移）。须 MVE 证否 6× 差距来源。

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

## ML 在星地激光湍流的精读沉淀（2026-07-10，R001/R002 调研后攒材料）

> 来源：R001（ML 调制切换）+ R002（ML 全谱）开放调研 + GW Step 3 精读 6 篇。
> 精读笔记见 `papers/_read_notes/`：li2023 / hu2025 / blatter2025 / islam2025 / qin2025-vae / qin2026-vqvae。
> 守 FR-22：这是攒材料，未立 Q#，不判 Go/Kill。

### ML 应用点全谱（R002 第一轮 6 角度 + 第二轮 5 收敛）

| # | 应用点 | 成熟度 | 对口度 | 代表 |
|---|---|---|---|---|
| 1 | AO/波前校正/相位补偿 | ⭐最大最成熟 | 中 | Guo2022 综述(200引), Liu2019(130引) |
| 2 | 信道估计/衰落预测 | 新兴(低引小群体) | 低(见下) | Li2023, Islam2025, Nguyen2022 |
| 3 | 均衡/载波恢复/非线性补偿 | 光纤多FSO少 | **高(见下)** | Qin2025/2026, Blatter2025 |
| 4 | 调制格式识别 | 中 | 低 | SVM/监督ML |
| 5 | 调制切换/AMC | 中(R001已验物理天花板) | ❌ | ③0.09dB+N1 PS gain≈0 |
| 6 | 资源分配/RMSA | 最大但偏网络层 | 低 | DRL/Q-Learning |
| 7 | 光束跟踪/pointing | 2024-26爆发 | 中 | DRL/CNN |
| 8 | BER/QoT预测 | 中 | 中 | ANN/回归ML |
| 9 | 端到端autoencoder | 新兴/空白 | 低 | — |

### ML 精读文献条目（6 篇）

#### [L-ML1] EMD-Seq2Seq-LSTM 大气湍流多步预报 (Frontiers in Physics 2023, c=16, 10.3389/fphy.2023.1070762)
- **核心贡献**：EMD 把非线性非平稳湍流强度序列分解为 ≤5 个平稳 IMF，各用 Seq2Seq-LSTM 预测再重构。R²=0.95，全面优于 WRF/LSTM。
- **关键限制**：预测目标 = **10min 尺度统计强度**（Fried r0 量级），与符号级 DSP 时空尺度差 **3-6 个数量级**。
- **与本研究关系**：方法可借鉴（分解+预测架构），但**预测目标不对口**——不能直接喂符号级 DSP。
- **源文件**：papers/doi/10.3389_fphy.2023.1070762/content.md

#### [L-ML2] 星间相干 CPR 抗噪 (Electronics 2025, c=0, 10.3390/electronics14020265)
- **⚠️ 不是 ML**——是经典二阶 DPLL（Kd=4, ωn=20 Mrad/s, 前馈平滑 N=64）。归入"ML 载波恢复"是检索归类偏差。
- **价值**：低 SNR 抑制 cycle slip，算力仅 Diff-4th 的 36%/0.8%。**固定参数不自适应是暴露给 ML 的靶点**。
- **与本研究关系**：传统 baseline 参考（非 ML）。其固定参数瓶颈暗示 ML 自适应的切入点。
- **源文件**：papers/doi/10.3390_electronics14020265/content.md

#### [L-ML3] ANN 透明载波相位恢复 (IEEE PTL 2025, c=0, 10.1109/LPT.2025.3582338)
- **核心贡献**：**真正的 ML-CPR**。极坐标直方图(10×18)作特征消除调制格式依赖，小 MLP(32-16-8-8-1)回归相位。一次训练跨 uniform/PCS QAM 透明。CPU time 仅 2S-BPS 的 18%。
- **关键限制**：**信道模型无大气湍流**（仅 AWGN + Wiener PN）。星地湍流适配性是明确缺口。
- **与本研究关系**：直接相关——证明 ML-CPR 在相干 DSP 可行且有竞争力。**湍流场景是研究缺口**。
- **源文件**：papers/doi/10.1109_LPT.2025.3582338/content.md

#### [L-ML4] FSO 信道湍流预测 ML (IEEE Comm. Letters 2025, c=7~11, 10.1109/LCOMM.2025.3555162)
- **核心贡献**：XGBoost 仅用 OOK 接收波形（无额外硬件）对 172m 链路 6 级离散湍流分类 >98% 准确率。
- **关键限制**：产出是**分钟级 6 类离散湍流等级标签**，明确指向**链路层/网络层**（RF/FSO 切换、功率调整、outage 预警）。**未提 DSP 参数**。瞬态期(<1min)不可信。
- **与本研究关系**：仅供参考。与符号级 DSP 时间尺度差 6+ 数量级。
- **源文件**：papers/downloads/2026-07-10/10942318.md

#### [L-ML5] VAE 盲均衡 双偏相干 FSO (IEEE TCCN 2026, c=0, 10.1109/TCCN.2025.3631007)
- **注意**：双偏振视角笔记见 [L-DP7]。此处记 ML 均衡视角增量。
- **核心贡献**：VAEMR（模值环）盲均衡，ELBO 损失。相比 CMA **收敛快 200× + 功率预算 +5dB**。1m 湍流板实验始终最优。
- **关键限制**：信道含湍流但**单一中强强度**（r0=0.4mm 固定，未扫 scintillation index）。**深衰落优势未直接证明**。
- **与本研究关系**：直接竞品/baseline。4 判据全过（符号级✅/双偏相干✅/实测✅/替代DSP✅）。
- **源文件**：papers/downloads/2026-07-10/11237129.md

#### [L-ML6] VQ-VAE 盲 MIMO 均衡 FSO (IEEE TCOMM 2026, c=0, 10.1109/TCOMM.2026.3689182)
- **核心贡献**：L-ML5 升级——VQ-VAE（离散码本）+ 二阶 Hammerstein 非线性 + 4×4 MIMO 估 Rx skew。相比 4×4 CMA +2dB，相比 CMMA+DDLMS +10dB。TCOMM Q1。
- **关键限制**：同 L-ML5——湍流单一强度未扫，深衰落优势待量化。星地估算强湍(Cn²=1e-14)下 16QAM 仅 18km，余量紧。
- **与本研究关系**：直接竞品/baseline。ML 切入相干 FSO 均衡的最强现有工作。
- **源文件**：papers/downloads/2026-07-10/11501945.md

### 三个对口应用点的精读后判断

#### 应用点 A（衰落预测）——对口度低
- Li2023 + Islam2025 **均为分钟级统计强度预测**，喂链路层（AMC/功率/outage），**不喂符号级 DSP**
- **符号级衰落预测/CSI 估计**：精读范围内无对口论文（空白）
- 结论：若要做，需重新定义预测目标（从统计强度→符号级 CSI），是全新问题不是迁移

#### 应用点 B（ML 载波恢复）——对口度中-高，有明确缺口
- Blatter2025 证明 ML-CPR 在相干 DSP 可行（跨调制格式透明 + 复杂度低）
- **但信道模型无大气湍流**（仅 AWGN+PN）——这是明确研究缺口
- Hu2025 不是 ML（经典 DPLL），但其固定参数瓶颈暗示 ML 自适应切入点
- 结论：ML-CPR 在湍流场景是空白，有切入空间，但缺直接 baseline

#### 应用点 C（ML 均衡）——对口度高，最强候选
- Qin2025/2026 **4 判据全过**，是 ML 切入相干 FSO 均衡的直接竞品
- 共通缺口：**湍流强度单一未扫，深衰落优势未量化**——这正是可切入的实验空间
- 比 CMA 收敛快 200× + 5dB（Qin2025），+2dB（Qin2026 vs 4×4 CMA）
- 结论：若做 ML 方向，应用点 C 最有基础（有竞品对标 + 有明确实验缺口）

### ML 方向综合分析

1. **现有方法分类**：
   - 衰落预测：统计强度预测（Li/Islam，分钟级）→ 喂链路层；符号级 CSI 预测空白
   - ML-CPR：ANN 极坐标直方图回归（Blatter，光纤无湍流）
   - ML 均衡：VAE/VQ-VAE 盲均衡（Qin 小组，FSO 相干，湍流单一强度）
2. **已知局限**（新颖性原料非问题）：①统计预测时空尺度不匹配 DSP ②ML-CPR 无湍流验证 ③ML 均衡深衰落优势未量化
3. **2-3 年趋势**：ML 均衡从光纤非线性补偿（成熟）向 FSO 相干湍流迁移（Qin 2025-2026 刚起步）；ML-CPR 在光纤侧零散低引，FSO 湍流侧空白
4. **研究背景概述**：ML 在光通信物理层 DSP 的应用分两条线——光纤侧（非线性补偿/QoT，成熟）和 FSO 侧（湍流补偿/均衡/预测，新兴）。FSO 相干 + 湍流 + ML-DSP 的交叉点目前仅 Qin 小组 2 篇 + Blatter 1 篇（无湍流），是明确的稀疏区。

### ML 方向研究问题清单（过 glossary 四判据，攒材料不立 Q#）

> 守 D004：以下 Q# 仅作材料积累，不进 Step 4a / MVE，待全部候选材料攒齐后统一评估。

| Q# | M-C-A | 判据1(具体技术矛盾) | 判据2(有方法产出) | 判据3(有2019+baseline) | 判据4(能做对比) | 综合 |
|---|---|---|---|---|---|---|
| Q-ML1 | M=传统CMA均衡 C=星地GG湍流深衰落 A=CMA在深fade发散/收敛慢 | ✅(sat.1553自认发散未分析) | ✅(ML均衡器，Qin已证可行) | ✅(Qin2025/2026+CMA) | ✅(vs CMA dB+收敛速度) | **全过（最强）** |
| Q-ML2 | M=传统载波恢复(VV/BPS/DPLL) C=星地湍流致相位快变 A=固定参数不适应湍流动态 | ✅(Hu2025固定参数瓶颈) | ✅(ML-CPR，Blatter已证) | ⚠️(Blatter无湍流，baseline缺湍流验证) | ✅(vs VV/BPS) | 部分过（baseline缺口） |
| Q-ML3 | M=统计强度预测 C=星地湍流 A=分钟级预测无法喂符号级DSP | ✅(尺度差6+数量级) | ⚠️(需重定义预测目标) | ✅(Li2023/Islam2025) | ⚠️(对比对象不明) | 部分过（产出形态待定） |

---

### ML 精读文献条目补充（第三批，凑至 20 篇，2026-07-10）

#### [L-ML7] ESN 湍流衰落信道预测 (IEEE Access 2022, c=9, TV Nguyen)
- **核心贡献**：ESN（储备池随机固定+岭回归解析训练 O(N(1+M))）用 1.87km 实测 FSO 数据做信道增益单步预测，全面优于 AR/SVM。
- **关键限制**：IM/DD 非相干 + Ts=0.196ms **统计级**，喂 PHY 速率调度。不能喂符号级相干 DSP（差 3-6 数量级）。
- **与本研究关系**：仅供参考。再次确认应用点 A 衰落预测=统计级强度。
- **源文件**：papers/downloads/2026-07-10/9916027.md

#### [L-ML8] MLP 联合信道估计+检测 FSO-OFDM (2025, c=2, Zhou)
- **核心贡献**：5 层 MLP 端到端联合 MIMO-OFDM FSO 信道估计+检测，弱湍 vs LS-MMSE +0.5dB。
- **关键限制**：DCO-OFDM **强度调制非相干**；方法朴素（无 CNN/LSTM，派遣标题误导）；损失公式缺失。
- **源文件**：papers/downloads/2026-07-10/10807810.md

#### [L-ML9] NN 均衡器六大陷阱 (Nature Electron./JLT 2022, c=106, Freire)
- **核心贡献**：**警示性方法论**——NN 均衡器 6 大陷阱：①jail window（MSE 回归把星座硬编码网格线，EVM 虚高 6dB 但 BER 无改善）②PRBS<24 阶 NN 学数据生成规则非信道逆，必须 MTRS ③必须用 BER/Q 错误计数禁 EVM/ESNR ④分类 CEL 过拟合+梯度消失，回归 MSE 泛化好 ⑤batch<1024 致少数幅度级主导 ⑥参数数≠真实复杂度，须报 RMpS。
- **与本研究关系**：**实验纪律 checklist 圣经**——本研究 ML 均衡/ML-CPR 实验必须遵守这 6 条。
- **源文件**：papers/downloads/2026-07-10/9773034.md

#### [L-ML10] 聚类盲非线性均衡 CO-OFDM (PTL 2018, c=101, Giacoumidis)
- **核心贡献**：无监督 FLC/分层聚类做 CO-OFDM 盲非线性均衡，QPSK 3200km 比 IVSTF +2.5dB。
- **关键限制**：**光纤 Kerr 非线性非 FSO 湍流**；高阶 16QAM（16 簇）增益骤降至 0.4dB。
- **与本研究关系**：方法可借鉴（聚类盲均衡思路），场景不符。
- **源文件**：papers/downloads/2026-07-10/8125098.md

#### [L-ML11] NN 均衡+ML 相位恢复联合 (JLT 2025, c=23, Wang)
- **⚠️ "ML"=最大似然 CPE 非机器学习**；ML 部分是 NN 均衡器。
- **核心贡献**："NN 均衡+传统 decision-directed CPE 无缝集成"范式。BMLPR 比 NN+BPS 省 56.99% 复杂度 +0.5dB。
- **关键限制**：6400km **光纤**无湍流（Kerr+CD+Wiener PN）。
- **可迁移思想**：CPE 无缝集成范式。
- **源文件**：papers/downloads/2026-07-10/10945325.md

#### [L-ML12] Physics-informed CFO 自补偿 NN (2025, c=3, Sheng)
- **核心贡献**：physics-informed 把 CFO 补偿内嵌进 NN 联合梯度下降 + variation ratio 无监督观测器。
- **关键限制**：**RF/无线 AMR 领域**，无光无湍流（AWGN+Doppler）。
- **可迁移思想**：CFO 内嵌进 NN 的 physics-informed 范式。
- **源文件**：papers/downloads/2026-07-10/10908528.md

#### [L-ML13] Seq2Seq 盲 CFO 估计 (IEEE Access 2022, c=3, Davey)
- **核心贡献**：真 ML 盲 CFO（Seq2Seq CNN+BiLSTM 堆叠细化分辨率），短序列低 SNR 超 FFT/PLL。
- **关键限制**：**RF/IoT+混沌通信**，纯 AWGN 无湍流。
- **可迁移思想**：Seq2Seq 堆叠细化分辨率。
- **源文件**：papers/downloads/2026-07-10/9947074.md

#### [L-ML14] ANN 双偏振自相干 FSO 均衡 (OFC 2026, c=0, Nasr)
- **核心贡献**：3PD→QAM 直接映射 ANN 监督均衡（绕信道估计），比 MI 优 **2.31dB** + MZM 非线性鲁棒。
- **关键限制**：湍流仅 θ/ϕ 偏振混线（抽象均匀采样），**闪烁/光束漂移不建模**。
- **与本研究关系**：✅ **本批对口度最高**。与 Qin VAE 互补——Nasr=自相干 SC 监督，Qin=全相干 MIMO 盲均衡。**共同缺口=完整湍流信道下 ML 均衡**。
- **源文件**：papers/downloads/2026-07-10/11480095.md

#### [L-ML15] ML/DL 光通信综述 (2025, c=36, Amirabadi)
- **类型**：algorithm-centric 综述。
- **核心贡献**：ML 在光通信物理层 = NLE/信道估计/检测/湍流检测/AO 五类。FSO 湍流 ML 按湍流检测(CNN)/AO(ANN,CNN)/OAM(CNN)/信道估计(EM,GRU)/检测(DNN)归类。
- **关键结论**：open problem = 数据泛化/可解释性/计算集成/RL 落地。**FSO 物理层 ML-CPR + 双偏振均衡是综述未显式覆盖但可推断的缺口**。
- **与本研究关系**：定位基准 + 缺口佐证。
- **源文件**：papers/downloads/2026-07-10/11003870.md

#### [L-ML16] FSO 信道监测 ML (Optics Express 2021, c=52, Esmail)
- **核心贡献**：首个用 SVM/CNN+ADTS 异步特征在 ASE/湍流/指向误差多损伤共存下预测 OSNR/Cn²/ζ（R²≈0.98）。
- **关键限制**：**统计级监测**喂链路层，非符号级 DSP。高速 40Gbps+ 恶劣骤降。
- **与本研究关系**：仅供参考。应用点 D（性能监测）代表。
- **源文件**：papers/downloads/2026-07-10-ml2/esmail2021-fso-monitoring.md

#### [L-ML17] CVAE+BiLSTM 双频湍流建模 (Photonics 2025, c=3, Gao)
- **核心贡献**：CVAE+BiLSTM 双分支+gating **显式分离湍流双频**（高频闪烁/低频漂移），可微信道代理反演补偿使 BER 降 **79%**、实验近 0。
- **关键限制**：IM/DD 非相干、短距 30m 实验。
- **可迁移范式**：**可微信道代理反演**——最可迁移到相干 DSP 的思想（分离双频+代理反演）。
- **源文件**：papers/downloads/2026-07-10-ml2/gao2025-hybrid-turbulence.md

#### [L-ML18] 条件 GAN 相位校正 LG 模式 MDM FSO (Optics Comm. 2024, c=36, Agarwal)
- **核心贡献**：cGULnet（条件 GAN+ConvLSTM U-Net）做 LG 模式 MDM FSO 湍流相位校正，完整 Zernike 阶精确恢复，前 10 帧→预测后 3 帧，BER→3.8e-3 FEC 限。
- **关键限制**：DL 增强 AO 范式（OAM 层非相干 DSP）；正文受限（Elsevier paywall）。
- **可迁移范式**：条件 GAN 相位校正。
- **源文件**：papers/downloads/2026-07-10-ml2/agarwal2024-lg-turbulence.md（正文受限⚠️）

#### [L-ML19] 自相干检测+ML 综述 (Photonics 2023, c=11, Wu)
- **类型**：综述。SCD 自相干系统 6 架构 + ML 6 应用（非线性/IQ/PR/偏振/重建模/光计算）。
- **关键限制**：**纯光纤无 FSO**。
- **可迁移思想**：SCD 架构与 ML-DSP 范式可借鉴自相干 FSO。
- **源文件**：papers/downloads/2026-07-10-ml2/wu2023-selfcoherent.md

#### [L-ML20] GAN/BiLSTM/BNN FSO 信道建模对比 (JLT 2022, c=48, Chen)
- **核心贡献**：GAN/BiLSTM/BNN 三 DL 算法 FSO 信道建模对比，**GAN 最优**（KL/PDF/波形全面优），多条件适应。JLT Q1 标杆。
- **关键限制**：⚠️ **正文 IEEE paywall**（仅 abstract+intro），待补全文。
- **与本研究关系**：信道建模标杆参考。
- **源文件**：papers/downloads/2026-07-10-ml2/chen2022-jlt-fso-channel.md（正文受限⚠️）

### ML 方向综合分析（20 篇后更新）

1. **现有方法分类（更新）**：
   - **衰落预测/信道建模**（应用点 A，6 篇）：统计强度预测（Li/Islam/Nguyen，分钟-ms 级，喂链路层）+ 信道建模（Chen GAN/Gao 双频代理反演）。**符号级 CSI 预测喂相干 DSP 仍空白**。
   - **ML 载波恢复**（应用点 B，5 篇）：真 ML-CPR 仅 Blatter（光纤无湍流）。其余 Wang=光纤NN均衡、Sheng/Davey=RF CFO、Hu=经典DPLL。**湍流场景 ML 载波恢复全空白**。
   - **ML 均衡**（应用点 C，5 篇）：Qin VAE/VQ-VAE（全相干盲均衡）+ Nasr ANN（自相干监督）+ Giacoumidis 聚类（光纤）+ Freire caveats（方法论）。**FSO 相干湍流均衡仅 Qin/Nasr 3 篇，共同缺口=完整湍流信道（闪烁+偏振+光束漂移）下 ML 均衡**。
   - **DL 增强 AO/相位校正**（Agarwal/Gao）：条件 GAN/双频代理，可迁移范式。
   - **性能监测**（应用点 D，Esmail）：统计级，非符号 DSP。

2. **已知局限（新颖性原料非问题）**：
   - 统计预测时空尺度不匹配 DSP（A 点 4 篇一致结论）
   - ML-CPR 无湍流验证（Blatter 唯一真 ML-CPR）
   - ML 均衡深衰落优势未量化（Qin/Nasr 共同缺口）
   - FSO 物理 ML 主流是 IM/DD 辐照度/AO/监测，**相干架构+符号级 DSP 下的湍流补偿空白**（Amirabadi 综述佐证）

3. **2-3 年趋势（更新）**：
   - ML 均衡从光纤非线性补偿（成熟，Giacoumidis/Freire）向 FSO 相干湍流迁移（Qin/Nasr 2025-2026 刚起步）
   - ML-CPR 在光纤侧零散低引，FSO 湍流侧空白
   - DL 增强 AO（条件 GAN/双频）是 FSO 湍流 ML 最活跃子方向（Agarwal/Gao）

4. **跨论文可迁移范式（攒材料）**：
   - **可微信道代理反演**（Gao2025）：分离湍流双频+代理反演，最可迁移到相干 DSP
   - **条件 GAN 相位校正**（Agarwal2024）：Zernike 阶精确恢复
   - **Seq2Seq 堆叠细化**（Davey2022）：分辨率逐步细化
   - **VAE 盲均衡模值环**（Qin2025/2026）：已验证 vs CMA 有效
   - **ANN 极坐标直方图 CPR**（Blatter2025）：跨调制格式透明
   - **NN 均衡+CPE 无缝集成**（Wang2025）：联合范式
   - **physics-informed 内嵌**（Sheng2025）：物理约束进 NN

### ML 方向研究问题清单（20 篇后更新，攒材料不立 Q#）

> 守 D004：以下 Q# 仅作材料积累，不进 Step 4a / MVE。

| Q# | M-C-A | 判据1(具体技术矛盾) | 判据2(有方法产出) | 判据3(有2019+baseline) | 判据4(能做对比) | 综合 | 精读支撑 |
|---|---|---|---|---|---|---|---|
| **Q-ML1** | M=CMA均衡 C=星地GG湍流深衰落 A=CMA深fade发散/收敛慢 | ✅(sat.1553自认+L-DP8) | ✅(ML均衡Qin/Nasr已证) | ✅(Qin2025/2026+Nasr2026) | ✅(vs CMA dB+收敛) | **全过（最强）** | L-ML5/6/14 |
| Q-ML2 | M=传统CPR(VV/BPS/DPLL) C=星地湍流致相位快变 A=固定参数不适应 | ✅(Hu固定参数瓶颈) | ✅(Blatter已证ML-CPR可行) | ⚠️(Blatter无湍流，缺湍流baseline) | ✅(vs VV/BPS) | 部分过 | L-ML3/11/13 |
| Q-ML3 | M=统计强度预测 C=星地湍流 A=分钟级预测无法喂符号级DSP | ✅(尺度差6+数量级) | ⚠️(需重定义预测目标) | ✅(Li/Islam/Nguyen) | ⚠️(对比对象不明) | 部分过 | L-ML1/4/7 |
| **Q-ML4(新)** | M=传统湍流补偿(分块AO/统计) C=星地GG湍流双频(闪烁+漂移) A=未分离双频致补偿次优 | ✅(Gao双频分离证增益) | ✅(CVAE+BiLSTM代理反演) | ✅(Gao2025+Agarwal2024) | ✅(vs 不分离 BER-79%) | **全过** | L-ML17/18 |

### 候选合并：Q-DP2 + Q-ML1 → Q-CMA-FADE（2026-07-11，20 篇精读后）

> 来源 D005。精读后发现 Q-DP2（分析型）和 Q-ML1（方法型）是同一物理问题两个角度，合为一条故事线。

#### 合并后故事线

**M-C-A 核心**：传统 CMA 均衡器在星地 GG 湍流深衰落下系数发散/收敛失败——sat.1553§6 综述**自认**"probability of the equalizer diverging ... has not been analyzed"（领域级空白非 agent 联想），L-DP8 实证深衰落致系数发散（ACP 2025）。

**贡献形态（两层，分析+方法合一）**：
1. **分析层**：量化 CMA 在 GG 深衰落下发散的概率/条件（补 sat.1553 自认空白）——需自建 GG 时间域衰落模型
2. **方法层**：ML 均衡器在深衰落下缓解发散 vs 传统 CMA（补 Qin/Nasr 实验缺口——他们只测单一中强湍流强度 r0=0.4mm 固定，未扫 scintillation index，深衰落优势未量化）

#### 增量定位（为什么不换皮 TL-12/D006）

| 维度 | Qin/Nasr 已做（竞品） | 我们补的缺口（增量） |
|---|---|---|
| 湍流信道 | 单一中强强度 r0=0.4mm 固定，1m 湍流板 | **真实 GG 深衰落**（闪烁+偏振混叠+光束漂移完整建模） |
| 实验维度 | 单点 BER/收敛速度 | **发散概率 vs 衰落深度扫描**（他们没做的 scintillation index 扫描） |
| 物理机制 | 报现象（VAE 比 CMA 快 200×） | **解释为什么**（发散机制分析，sat.1553 自认空白） |
| baseline | vs CMA dB | vs CMA **发散概率 + 深衰落恢复时间**（新增测度） |

定位结论：**接近 Qin/Nasr（同方向，他们铺了"ML 均衡可行"），补他们的实验缺口（真实深衰落 + 发散机制），不是照搬 VAE 换场景**。符合 D005 务实路线 + 用户"和别人接近才好"偏好。

#### 四判据（合并后最强）

| 判据 | 证据 | 精读支撑 |
|---|---|---|
| 1 具体技术矛盾 | ✅ sat.1553 自认发散未分析 + L-DP8 实证 + CMA 在深 fade 收敛失败 | sat.1553§6, L-DP8 |
| 2 有方法产出 | ✅ 两层：发散概率界（分析）+ ML 均衡缓解（方法） | L-ML5/6/14 |
| 3 有 2019+ baseline | ✅ Qin2025/2026 VAE + Nasr2026 ANN + 传统 CMA/CMMA | L-ML5/6/10/14 |
| 4 能做对比 | ✅ vs CMA 发散概率 + dB + 收敛速度 + 深衰落恢复时间 | L-ML5/6/14 |

**综合：全过（最强候选）**

#### 风险（Conditional）

1. **GG 时间域衰落模型需自建**（FR-20 缺口，Q-DP2 原有风险继承）——现有文献只给幅度 PDF，衰落持续时间/频率全缺失
2. **与 Qin 小组抢位**——他们是活跃小组（2025-2026 连出），增量定位必须扎实（真实深衰落+发散机制）避免被说换皮
3. **"几 dB 量级"需 MVE 验证**——若深衰落下 ML 均衡 vs CMA 增益 <0.5dB 则 Go 不成立（FR-21 但这里测度不止 dB，还有发散概率）

---
## GW Step 3 正式精读补充（2026-07-17）

本批5篇均完成标题自检、全文精读和结构化笔记；逐篇笔记见：
`papers/_read_notes/10.1109_LCOMM.2026.3651445.md`、`10.1109_jphot.2021.3062727.md`、`10.1109_tcomm.2022.3171809.md`、`10.1109_JLT.2025.3533422.md`、`10.1109_jlt.2020.3042546.md`。此前4个失败 DOI 未冒充替代稿件。

### Step 3 进度与 L 条目索引

| L# | 论文 | 关系 | 结构化笔记 |
|---|---|---|---|
| L01 | LCOMM 2026 LPT/FPT-Jones-RSOP | 直接方法族竞品 | [read note](../../papers/_read_notes/10.1109_LCOMM.2026.3651445.md) |
| L02 | JPHOT 2021 M-CMA+NPCA | 盲式RSOP baseline | [read note](../../papers/_read_notes/10.1109_jphot.2021.3062727.md) |
| L03 | TCOMM 2022 CW pilot phase estimation | pilot功率/相位邻近理论 | [read note](../../papers/_read_notes/10.1109_tcomm.2022.3171809.md) |
| L04 | JLT 2025 dual-pol Costas PLL | 低复杂度硬件邻近 | [read note](../../papers/_read_notes/10.1109_JLT.2025.3533422.md) |
| L05 | JLT 2020 OFDM joint ML synchronization | pilot同步邻近 | [read note](../../papers/_read_notes/10.1109_jlt.2020.3042546.md) |

Step 3 本批状态：5/5 已精读；5/5 标题一致；5/5 有 baseline 或明确“无数字偏振 baseline”；5/5 完成七子表和实验完备性记录。Step 4a 入口候选为 Q1/Q2，Q3/Q4 仅作背景/参数依据。

### 方法分类与综合比较

1. **直接 pilot/Jones/RSOP 路线**：LCOMM 2026 的 LPT 在 DSCM 中用四路频域 pilot 功率谱消除偏振衰落，再直接求 Jones 矩阵；这是当前 OSL+6pilot+EMA09 的方法族直接竞品，但没有 GG 大气或稀疏时域 pilot。
2. **盲式自适应路线**：JPHOT 2021 用 M-CMA FIR+NPCA 盲估计逆混合矩阵，支持 5 Mrad/s 光纤 RSOP，给出 40% 级复杂度锚点；无 pilot，适合作为当前方案的传统强 baseline。
3. **pilot 相位/同步邻近路线**：TCOMM 2022 分析 CW pilot 的带内/带外功率分配；JLT 2020 用重复 OFDM training symbols 做 TO/CFO/CPO 联合 ML。两者可提供 pilot 功率、同步误差和开销审计先验，但不解决2×2 Jones。
4. **模拟低复杂度路线**：JLT 2025 集成双偏振 Costas PLL，展示无DSP载波恢复和功耗边界；不处理偏振矩阵与GG衰落。

### 已知局限、趋势与背景

共同局限是：直接 FPT/Jones 方案未评估大气 GG 深衰落；盲 NPCA/CMA 方案无 pilot 可观测性且缺少深衰落统计；pilot 理论多为单通道相位或AWGN/Wiener；硬件PLL受参考载波和cycle slip约束。2020→2022 的趋势是从训练符号同步走向频域 CW pilot 的功率/估计理论，2021→2026 则出现盲RSOP低复杂度和FPT-Jones高速跟踪并行发展，系统目标转向低功耗和高RSOP速率。当前研究定位是把这两类路线放入同一 OSL Gamma-Gamma 深衰落条件，量化传统 CMA/Jones 估计发散概率，并审计6pilot+EMA09的开销-稳定性折中。

### 研究问题清单（M-C-A + 四判据）

| Q# | M-C-A | 四判据 | 产出形态 |
|---|---|---|---|
| Q1 | M=传统盲CMA/Jones更新；C=OSL双偏振Gamma-Gamma深衰落与RSOP混合；A=深衰落使输入能量骤降，更新矩阵发散/失锁 | 1具体矛盾✅（JPHOT/Jones与本项目批次实证）；2方法产出✅（发散概率界+稳定跟踪器）；3有baseline✅（CMA、NPCA、LPT）；4可对比✅（发散率、恢复时间、BER/Q） | 分析+pilot辅助稳定均衡 |
| Q2 | M=传统短帧/块级稀疏pilot LS Jones inversion（不含本研究EMA稳定化）；C=OSL双偏振Gamma-Gamma衰落+高速时变SOP、pilot预算≤10%；A=短pilot在深衰落/快速SOP下矩阵病态或噪声抖动，导致fixed-label恢复不稳 | 1具体矛盾✅（S064 seed47与pilot-count对照）；2方法产出✅（稳定化跟踪器+开销-恢复曲线）；3baseline✅（传统LS/CMA、NPCA、LPT）；4可对比✅（pilot率、BER、Jones误差、发散/恢复） | **待Step4a复核**：问题已按D055改回现有M-C-A；不是“己方6pilot+EMA”的自证问题 |
| Q3 | M=频域FPT/Jones；C=光纤DSCM RSOP；A=偏振衰落污染CPE | 1✅；2✅；3✅；4✅，但与OSL迁移需验证 | 直接DSP竞品，不直接进MVE |
| Q4 | M=CW/OFDM pilot相位同步；C=AWGN/Wiener或CO-OFDM；A=pilot功率/带宽影响MSE/SNDR | 1✅；2✅；3✅；4✅，不含Jones/GG | 参数先验，不作为OSL主问题 |

Q1可直接作为Step4a候选；Q2已完成M-C-A纠正，四判据形式通过但需Step4a核查是否与LCOMM/Jones竞品构成同机制撞车；Q3/Q4为背景与参数依据，不单独触发新方向。

### Step 3.5 定向补检：直接竞品浅读（2026-07-17）

关键词矩阵第一轮6/6组合完成，共42条原始、41条canonical去重记录；实际有效来源为OpenAlex与Semantic Scholar两类（满足≥2源，**不含此前误记的Tavily**）。LCOMM 2026的引用链补检得到backward=19、forward=0；两组`FSO + Gamma-Gamma`精确组合检索均为0。第一轮新增必读4篇、建议读1篇，按`gw-supplement.md`“最后一轮新增=0”判据**尚未收敛**，必须用这5篇生成的新关键词执行第二轮定向检索。

5篇先完成题名、摘要和正式发表状态核验，结构化浅读记录见`search-archive/2026-07-16/step35-direct-read5.json`。随后provenance复核发现L08已由Firecrawl成功取得54KB完整HTML正文（metadata=`success/good`，含方法、实验、复杂度、结论与参考文献），现转正式全文精读；**LCOMM 2026（S069专篇精读）也已全文精读**（`papers/doi/10.1109_LCOMM.2026.3651445/content.md`，FPT→4路→Jones直接补偿，光纤场景无时域LS+EMA）。其余4篇仍无可读全文，只能作摘要级证据，不得断言其具体LS公式、EMA实现、pilot开销、复杂度或全文实验条件。

> **2026-07-22 更新（S074续接/D061/V035）**：Step 3.5 backward-chain 终验 **V035 PASS**（JLT2022 Crossref refs=21/screened=7/new=0，gw-supplement 判据#3 闭合）。但 4 篇直接竞品全文获取仍 **BLOCKED**：本轮 `tools/download --doi` 对 TCOMM2024.3522036 / JLT2025.3640695 / JLT2022.3224805 / JLT2023.3284489 四篇均 `all_failed`（non-OA IEEE paywalled）；OA scout 子 agent 验证 Semantic Scholar/Unpaywall/OpenAlex/arXiv 四源均 closed（无 arXiv 预印本、无 green-OA）。**4 篇全文无法合法获取**，标 `BLOCKED_NO_FULLTEXT`。Step 3.5 维持 PARTIAL（backward PASS + 收敛 PASS，但 D056 全文门 BLOCKED），不进 Step 4a。下一轮由用户裁决获取路径（机构 VPN / 作者邮件 / 带债豁免 / 等 OA）。**纠正 170c00c 审计错误**：LCOMM 2026 与 OE 2021 均已全文精读（非 abstract-only）。

| L# | 论文 | 摘要核验的方法 | 对Q2的影响 | 证据级别 |
|---|---|---|---|---|
| L06 | TCOMM 2025, DOI `10.1109/TCOMM.2024.3522036` | pilot-symbol ML估计RSOP，EM利用未知数据精化，decision-aided动态跟踪 | 直接覆盖低pilot、高速RSOP估计稳定性；仅光纤PDM场景 | **BLOCKED_NO_FULLTEXT**（浅读；2026-07-22 tools/download all_failed + OA scout 4源 closed） |
| L07 | JLT 2026, DOI `10.1109/JLT.2025.3640695` | 共享短preamble联合帧同步、FOE、SOP tracking和均衡预收敛 | 直接覆盖短训练块与SOP稳定估计；未核实GG/Jones-inverse/EMA | **BLOCKED_NO_FULLTEXT**（浅读；2026-07-22 tools/download all_failed + OA scout 4源 closed） |
| L08 | Optics Express 2021, DOI `10.1364/OE.419574` | 三个线性无关pilot tones，逐block平均并解析求RSOP矩阵后求逆；扫描PSR与block size | 与“稀疏pilot→块级矩阵→逆补偿”高度同构，是Q2最直接机制基线；明确已有短block增噪/长block失配权衡，但未覆盖OSL GG、LS病态、EMA、fixed-label | **全文精读完成**（`papers/_read_notes/10.1364_oe.419574.md`） |
| L09 | JLT 2022, DOI `10.1109/JLT.2022.3224805` | FPT提取传输矩阵与载波相位，并用滑动窗口平均跟踪 | 已覆盖pilot矩阵估计+时间平滑的核心链条，EMA本身不能作为贡献 | **BLOCKED_NO_FULLTEXT**（浅读；2026-07-22 tools/download all_failed + OA scout 4源 closed；V035 backward-chain refs 含此论文自身） |
| L10 | JLT 2023, DOI `10.1109/JLT.2023.3284489` | FPT联合偏振/载波恢复并处理IQ mixing等硬件失真 | 说明pilot/FPT鲁棒估计已有成熟竞争主线；OSL场景迁移不足以自动构成新问题 | **BLOCKED_NO_FULLTEXT**（浅读；2026-07-22 tools/download all_failed + OA scout 4源 closed） |

#### Step 3.5 对方法分类和Q2的修正

1. **generic机制已饱和**：pilot/FPT估计Jones或RSOP矩阵、逐block逆补偿、短训练序列预收敛、滑动时间平均均已有直接先例。L08全文还明确写出block内平均的短block增噪/长block失配权衡（content.md第249行附近），并报告PSR、block size、RSOP速率和复杂度。因此当前方案不能声称“首次pilot-assisted Jones tracking”，也不能以EMA替换SWA或block averaging作为新颖性。
2. **可保留的仅是待证问题，不是完整组合空白**：在dual-pol OSL Gamma-Gamma深衰落且pilot预算不超过10%时，传统短块pilot矩阵估计是否因观测SNR下降、条件数恶化或跨block动态失配而造成fixed-label恢复不稳；其价值必须由相同场景的直接强baseline和可诊断机制共同证明。
3. **Step 4a碰撞门加严**：L08/L09是首选直接机制baseline，L06是高动态强估计baseline，L01是近期Jones/FPT baseline。若Q2只能靠“换成大气场景”或“EMA参数不同”区分，则Kill；只有证明OSL GG引入竞品未处理、且足以改变最优估计/稳定化结构的失效机制，Q2才可能继续。
4. **未闭合债务**：其余4篇全文获取失败，尚不能比较其精确pilot overhead、矩阵估计形式和复杂度。此债务必须保留到可获取全文或Step 4a明确采用摘要支持范围内的保守判断；L08的全文证据已足以把“短block噪声/长block失配”列为已知竞争维度，不能再把它当作未被讨论的现象。

R2按5种方法变体×2类场景得到31 raw/25 unique；R3围绕JLT 2023 PDL/FPT及引用链得到50 raw/37 unique。R2/R3最后一轮新增必读/建议读均为0，三轮关键词检索收敛。最高引用直接竞品确定为JLT 2022 FPT（citation_count=36，高于OE 2021的19）：Semantic Scholar前向链25篇；Crossref publisher metadata给出21条backward references，经索引与摘要筛出7篇方法相关，均为已知候选，新增0。检索与引用链归档见`search-archive/2026-07-17/step35-r3-summary.json`及`step35-r3-jlt2022-backward-screened.json`。

当前Step 4a 后的Q2状态（2026-07-23 S079/T002/V036 更新）：**Provisional verdict = GATE_KILL（待主控+用户确认）**。D062 带债豁免大包已执行 A0/A′/A/B；D 性能 MVE 未运行——两条独立 Kill 门在 semantic-smoke + bounded headroom 阶段触发：(1) A0 §1 致命 + FR-01 先验覆盖致命——real-rotation 信道（theta=sop_rate·arange(N)，矩阵 [[c,s],[-s,c]]，cond≡1）使 Q2 假设失效 A（短pilot矩阵病态）**结构缺席**，固定 EMA09 已把主指标覆盖到 oracle；(2) FR-21 headroom Kill——B1→oracle headroom 可忽略（预注册 B1/O=1.19，亚一个数量级，多 seed bit-equal）。P（uncertainty-aware temporal tracker）不赢 B1（0/10 paired）。**KILL scope 限于 unitary real-rotation 信道实例化，不重构为杀 Pilot-Jones 方向本身**（science critic V036 KILL_WITH_CAVEAT：唯一 rescue 出包范围 = 升级 canonical 信道为带 PMD/PDL 的 complex Jones）。历史 EMA09 15/15 provenance 断裂已记录（batch1_fade_methods.py SHA mismatch），仅作 diagnostic prior 且为 pilot-vs-blind 比较非方法间比较。详见 feasibility_report.md Q2 节 + projects/simulation/explore/pilot-jones-step4a/synthesis.md。不进 Step 5/Contract/Execute。

> **2026-07-23 主控 amendment（V037/D063）**：T002 raw 的 P/B1 win-tie-loss 为 `0/6/4`，contract gate-outcome 残留 `0/7/3`；`B1/O=1.19` 是 BER ratio，未证明等价 `<0.5dB`，故第二条 FR-21 门降为 diagnostic。正式接收结论仅为 `UNITARY_REAL_ROTATION_MCA_KILLED`，Pilot-Jones family 仍 `UNRESOLVED`。D063 已授权 T003 用有来源的 complex Jones/PMD/PDL 模型、task-matched 2×2 tapped/FDE conventional baseline 和正确 Q²/headroom 口径重评；正面最高 Conditional Go，止于 Step 4a。

> **2026-07-23 T003 救活结果（S080）**：complex-Jones/PMD/PDL 模型充分性救活完成，**provisional verdict = `PIVOT_MODEL_NOT_JUSTIFIED`**。M0–M4 模型梯（8/8 limiting-case tests PASS）+ task-matched B3（whitening/tapped）+ 正确 BER→Q² 口径。**决定性结构发现**：在最 P-favorable 深衰落（α=2.0/β=1.0/17dB）下，B3-vs-oracle headroom 不随损伤强度增长（PDL 0→9.5dB/cond 1→3.6 与 M0 control 完全相同；PMD 40→160ps 不单调增长）→ 残余 headroom 来自深衰落+噪声非 PDL/PMD 结构。P1（energy-weighted LS）全 cell 不胜 B3。complex-Jones/PMD/PDL 升级在 2.5GBaud/64–100sym block 下不重新产生方法级 gap；T002 unitary-real-rotation 负面结论扩展为即便 richer Jones B3 仍关闭 headroom。Pilot-Jones family 仍 `UNRESOLVED`，不在本轴关闭。4 篇 D056 全文继续 BLOCKED；"OE2021 一阶 PMD" provenance 标 unverified 债务（sub-agent 未能确认 Optics-Express 2021 DOI）。详见 `projects/simulation/explore/pilot-jones-complex-salvage/synthesis.md`。不进 Step 5/Contract/Execute。

> **2026-07-23 主控失效 amendment（V038/D064）**：上一段仅保留为 T003 历史执行记录，科学结论全部 INVALIDATED。原因：PDL/PMD 施加于含噪 RX 导致可逆恒等；PMD pilot 未经过 FIR；B3 tapped 是 RX→RX 自预测；PMD oracle 被 B1 反超；decision 将 problem survival 与 P1 success 混合。不得引用 T003 的 M2/M3 数值、headroom 归因或 negative harvest。complex-Jones/PMD/PDL 继续 `UNRESOLVED`；D064/T004 在同一 Step 4a 内先闭合 semantic tests 再重评。

> **2026-07-24 T004 主控失效 amendment（V039/D065）**：T004 的工程语义修复
> 可复用，但正面 PDL problem gate 仍 INVALIDATED。原因不是 B3 方法弱，而是
> component Jones 每 64 symbols iid redraw 无物理时间尺度来源；固定器件反事实使
> PDL impairment-added headroom 降至 0.0146/0.00445 dB。B3 过拟合仅证明
> 6-pilot 下 arbitrary per-block 3-tap LS 零残差自由度，不得外推为真实系统普遍
> pilot-budget limit。另有 Python hash 与 contract/SHA 闭包债。complex axis 继续
> `UNRESOLVED / T005_TEMPORAL_ADJUDICATION_READY`，T005 不运行新方法。

> **2026-07-25 T005 closeout（S082/V040/D066）**：fixed/verified component 的
> 8 个 primary cells 最大 impairment-added point/CI upper 为
> `0.0804126817/0.2371961896 dB`，均低于 0.5 dB，故
> `COMPLEX_COMPONENT_RESCUE_AXIS_TEMPORAL_PRIMARY` scoped Kill。原 M3 reference
> 使用 MMSE regularization 而非 contract 声称的 exact inverse，Windows 默认 locale
> 也有 3 个 encoding failures，故 integrity PARTIAL；主控用真正的 unitary
> exact inverse 重算 40 个 M3 test realizations，BER 40/40 一致、无噪误差
> `1.13e-15`，scientific verdict 不变。Pilot-Jones 退出当前 carrier；4 篇全文债
> 和 entire-family 完备性不伪装为已闭合。

> **2026-07-25 carrier switch（step4a D012/S014）**：当前 Step 4a 转到 B10/B12
> 高阶调制 CPR 组合方法。B10/L20 与 B12/L22 的 Step 1–3 证据直接复用；T006
> 先做 equal-overhead strongest-simple CPR→truth-assisted headroom，存活后同包
> 评估 pilot-RLS→MAP residual cascade、confidence gate 和 adaptive-forgetting RLS。
>
> **2026-07-26 current amendment（formal D017 / live D006 / T010）**：上一段仅为
> T006 的历史派发记录，不再描述当前 Step 4a。T006 的 source identity、pilot/data
> channel 与 robust-statistics verdict 已被 V001 拒收，B10/B12 family 未 Kill，
> 但组合实现不得继续修复或充当 fixed B10。B1/T008 与 A4/T009 随后也分别因
> evaluator/source identity 阻断返回候选池。当前唯一 active carrier 是
> `B10_SOURCE_NATIVE_ADAPTIVE_RLS_CPR`：T010 从 B10 原文重建 128 contiguous
> pilot→DD fixed estimator；identity 通过后同包比较 innovation freeze、
> adaptive forgetting、amplitude-only cheap rule 与 conventional B*。2.5 GBd
> 星地 GG primary 仅为 `SOURCE_TRANSFER`；T010 独立派发审查通过前不运行，
> 且不进入 Step 5/Contract/Execute。

### 实验完备性对标汇总

| 论文 | 统计规范 | Baseline | 消融/扫描 | VVUQ(V/V/U) |
|---|---|---|---|---|
| LCOMM 2026 | 无多seed/CI | PTJ、MIMO+BPS | LPF、RSOP率、静态θ | 2/2/1 |
| JPHOT 2021 | 无多seed/CI | CMA+VVPE | LMS/RLS、RSOP、线宽 | 3/2/1 |
| TCOMM 2022 | 理论/曲线 | BLUE/ML | in/out-band、SPR、噪声 | 2/1/1 |
| JLT 2025 | BER窗口、无CI | 既有PLL定性 | 带宽、单/双偏振 | 3/2/1 |
| JLT 2020 | 仿真、无seed/CI | Schmidl/Minn/Park/CRLB | 联合/顺序、SNR/CPN/CD | 3/1/1 |

领域惯例是少量参数扫描和传统 baseline，几乎没有多 seed 统计或显著性检验；本项目 Contract 应补多 seed、固定标签、深衰落扫描和逐组件消融。

---

## Q15 Step 1–2 pending（2026-07-28，T021 / CP019，**非 Step 3 精读**）

> 来源：T021（CANDIDATE_FORMALIZATION，foreground epoch51 / CP019）。承接 T020/M4
> 工厂级诊断信号（D028/V053，claim ceiling = `DIAGNOSTIC_ONLY_NOT_FORMAL_GW_MVE`）。
> **本节只记录 Step 1 检索 + Step 2 公共全文获取/coverage-gap 状态与证据指针。**
> **Q15 四判据全部 UNKNOWN / NOT_ADJUDICATED**；不改全局 Step 3/3.5/4a 状态。
> 详细候选图与 coverage report 见 `search-archive/2026-07-28/q15-step1-candidate-map.md`
> 与 `worker-logs/step-021-q15-groundwork-step1-2.md`。

### Q15 暂定问题假说（**不是已过四判据的 Q#**，待 Step 3+ 检验）

- **M**: 固定参数 blind FIR CMA 及 always-on blind output calibration
- **C**: dual-pol 16QAM 接收机在部分随机实现/初始化下产生低功率 shell collapse
- **A**: 传统方法缺少 receiver-visible 的 collapse detector 与安全 identity fallback，
  或其固定归一化无法区分健康和塌缩输出
- **产出形态（待检验）**: prefix-gated identity/quantile-shell transport policy

### Step 1 检索状态（PASS，门全过）

| 门 | 阈值 | 实测 |
|---|---|---|
| unique | ≥20 | 129（11 query × 2 轮，4 线） |
| source | ≥3 | 3（Semantic Scholar + OpenAlex + IEEE/blit） |
| 必读 | ≥5 | 11 |
| published | ≥50% | 93.8% (121/129) |
| 技术路线 | ≥2 | 4（radius/MMA/shell；CMA singularity/restart/init；blind AGC/scale；distribution/quantile） |

priority 分布：必读 11 / 建议读 13 / 待确认 2 / 备选 16 / 排除 87。
证据指针：`search-archive/2026-07-28/q15-merged-annotated.json`（含 _priority/_q15_flags）+
`q15-step1-candidate-map.md`（direct collision D1–D6 + cheap alternative C1–C8 分表）。

**全仓既有 identity 命中**：Q14/S038（同族 adjacent，四判据 2 UNKNOWN，Step 3 暂存）+
L-DP8 JR-CMA（CMA+AGC+重置+变步长，cheap-alt 实证先例）+ sat.1553§6（领域共识盲区）+
L07（CMA/RDE 并行，范围 out）。

### Step 2 公共全文获取状态（8 成功 + 1 质量不达标 + 5 失败进 gap）

**成功获取（8 篇，content ≥50 行，title identity + SHA256 PASS）**:
- D2 Modified RDE high-order QAM (ECOC 2015) → `papers/doi/10.1109_ecoc.2015.7341620/`
- D5 Optimized blind eq PS high-order QAM (COL 2022) → `papers/doi/10.3788_col202220.080601/`
- C2 Adaptive filters: stable but divergent (EURASIP 2015) → `papers/doi/10.1186_s13634-015-0289-8/`
- D4 Likelihood-Based Selection RDE+pilot PS-QAM (JLT 2021) → `papers/downloads/2026-07-28/9492010.{pdf,md}`
- D4′ ECOC 2020 早期版 → `papers/downloads/2026-07-28/9333378.{pdf,md}`
- D3 A Novel Radius-Adjusted Approach (SPL 2006) → `papers/downloads/2026-07-28/1561206.{pdf,md}`
- D3′ ISCC 2005 长版 Hybrid Methods → `papers/downloads/2026-07-28/1493739.{pdf,md}`
- C6/L010 Blind Pol Demux shaped QAM temporal corr (JLT 2024) → `papers/downloads/2026-07-28/10251763.{pdf,md}`

**内容不达标（1，弃）**: 4458069 FPGA equalizer（IEEE 反爬 watermark-only，8 行）。

**下载失败进 coverage gap（5）**: D1 Shell-Partitioned MMA+Soft Switching (EUSIPCO 2007,
10.5281/zenodo.40308，**最关键 direct-collision 未知**)；C1 Null-Space Init (PIERS 2019)；
C3 MMA steady-state (Signal Processing 2014)；C4 Analytical MMA (IJDMB 2010)；L011
Time-Reverse Eq 16QAM PDM (Access 2021)。三轮止损（OA / force / IEEE-blit）均失败。

### Step 1–2 初步观察（**非四判据结论**，仅供主控 coverage gate）

- Q15 action space（prefix-gated identity/quantile-shell radius transport）**不是空白**：
  radius/shell 分区切换在 equalizer 层有成熟先例（已获取的 D2/D3/D4/D5）。
- Q15 差异化候选：(a) prefix-only 因果边界；(b) identity fallback 健康零回归；
  (c) post-proc frozen map 而非 equalizer 抽头/代价修改。
- **关键未知**：D1（shell-partitioned MMA + soft switching）全文缺失，摘要仅 1 行，
  无法确认 Q15 gated identity/transport 是否已被等价覆盖。
- **cheap-alt 未知**：C1/C3/C4 全文缺失，无法确认 cheaper 初始化/MMA 代价修复能否
  吸收 Q15 问题。

### Q15 四判据状态

| 判据 | 状态 |
|---|---|
| 1 具体技术矛盾（M-C-A） | **UNKNOWN**（M-C-A 是暂定假说，未由精读验证） |
| 2 方法产出形态 | **UNKNOWN**（prefix-gated policy 形态待 Step 3 验证信息增量） |
| 3 近期 baseline 可对标 | **UNKNOWN**（baseline 池待 Step 3 确认；CMA/MMA/RDE/restart 均候选） |
| 4 能做可量化对标 | **UNKNOWN**（PI-SER/BER 对比框架待 Step 3+ 确认） |
| **综合** | **NOT_ADJUDICATED**（Step 1–2 不判；禁入 Step 4a/MVE） |

### 范围确认

- 本轮在 Q15 Step 1–2 / T021 授权范围内（检索 + 公共全文获取 + coverage report）。
- **未**进入 Step 3 精读 / Step 3.5 / Step 4a / Contract / Execute / 任何实验。
- **未**改全局步骤进度表（上方"步骤进度"表的 Step 1/2/3/3.5/4a 行不变；Q15 是 RDL
  formal owner 下的独立 formalization 候选，不回写全局 GW 进度）。

### 后续（待主控 coverage gate 裁决）

主控可选：(a) 接受 D1/C1/C3/C4 债务进 Step 3 精读已获取 8 篇；(b) 要求用户手动获取
D1/C1/C3/C4 后再进 Step 3；(c) 因 D1 碰撞风险判 `BLOCKED_DIRECT_COLLISION`。
**worker log 终态**: `AWAITING_DELEGATED_COVERAGE_GATE`，mission_method_delta = `NONE`。

---

## Q15 Step 3 精读 + 综合分析（2026-07-28，T022 / CP020）

> 来源：T022（CANDIDATE_FORMALIZATION，foreground epoch52 / CP020）。承接 T021 的
> `AWAITING_DELEGATED_COVERAGE_GATE`（主控选 (a)：接受 D1/C1/C3/C4 债务进 Step 3 精读
> 已获取 8 篇）。本节是 GW Step 3 精读产物（6 篇独立核心 + 2 篇补充早期/长版）。
> **claim ceiling**：Q15 四判据最终状态、novelty、cheap-alt closure 因 D1/C1/C4 全文缺失
> 保持 `PENDING_STEP35`——**不是 formal Go/Kill**，不宣称 problem survives conventional
> baseline。详细逐篇笔记见 `papers/_read_notes/`，receipt 见
> `worker-logs/step-022-q15-step3-read.md`。
> **不改全局步骤进度表**（Q15 是 RDL formal owner 下的独立 formalization 候选）。

### Step 3 精读完成矩阵（6 独立核心 + 2 补充）

| ID | 角色 | 标题 Jaccard | title verdict | 行数 | 源路径 | 笔记 |
|---|---|---|---|---|---|---|
| D2 | modified RDE direct collision | 1.0 | PASS | 102 | papers/doi/10.1109_ecoc.2015.7341620/content.md | _read_notes/10.1109_ecoc.2015.7341620.md |
| D5 | distribution/K-means radius direct collision | 1.0 | PASS | 216 | papers/doi/10.3788_col202220.080601/content.md | _read_notes/10.3788_col202220.080601.md |
| C2 | CMA divergence theory | 1.0 | PASS | 647 | papers/doi/10.1186_s13634-015-0289-8/content.md | _read_notes/10.1186_s13634-015-0289-8.md |
| D4 | likelihood RDE direct collision (JLT 2021) | 1.0 | PASS | 418 | papers/manual/ieee-9492010-likelihood-rde/content.md | _read_notes/ieee-9492010-likelihood-rde.md |
| D3 | radius-adjusted switching direct collision (SPL 2006) | 1.0 | PASS | 682 | papers/manual/ieee-1561206-radius-adjusted-equalization/content.md | _read_notes/ieee-1561206-radius-adjusted-equalization.md |
| C6 | temporal-correlation/pr-MMA cheap alternative (=L010) | 1.0 | PASS | 514 | papers/manual/ieee-10251763-temporal-correlation-demux/content.md | _read_notes/ieee-10251763-temporal-correlation-demux.md |
| D4′ | (补充, D4 ECOC 2020 早期版, 非独立核心) | 1.0 | PASS | 112 | papers/manual/ieee-9333378-blind-rde-likelihood/content.md | _read_notes/ieee-9333378-blind-rde-likelihood.md |
| D3′ | (补充, D3 ISCC 2005 长版, 非独立核心) | 1.0 | PASS | 299 | papers/manual/ieee-1493739-hybrid-blind-equalization/content.md | _read_notes/ieee-1493739-hybrid-blind-equalization.md |

**独立核心计数：6 ≥ 5（gw-read 单步门槛 PASS）**。8 篇全部 title Jaccard=1.0 PASS，无
ABORT_TITLE_MISMATCH。D3′/D4′ 按 task 规则 5 不计独立核心数。

### 1. 机制与作用点分类 + Q15 同 action/information/problem 判定

按机制与作用点分 5 类：

| 类 | 代表论文 | 机制 | 作用点 |
|---|---|---|---|
| equalizer-internal switching | D3 (RMMA/RMDA, region-dependent µ_i/λ_i) | 半径分区选步长+误差模式权重 | equalizer 抽头更新（always-on） |
| output remap / radius reweighting | D2 (PRDE, P(r) scalar reweight) | 半径键控标量乘误差项 | equalizer 抽头更新（always-on, 软标量） |
| distribution-aware radius tracking | D5 (peak-density K-means), D4/D4′ (likelihood α-gated) | 从数据估半径/分布 或 likelihood 门控 payload 更新 | equalizer 抽头更新（D5 batch；D4 在线 pilot+payload 门控） |
| temporal-correlation alternative | C6 (FDJD-pr-MMA) | TX 注入时间相关 + RX 二阶统计分离 + pr-MMA | **TX 端修改 + RX pol-demux**（非 receiver-only） |
| divergence theory | C2 (l2-stability vs MSE) | 小增益定理 + SVD 逆发散测试 | 分析框架（非方法） |

**D2/D3/D4/D5 与 Q15 的同 action/information/problem 判定**：

- **同 action？** 部分是。D2/D3/D4/D5 都做"半径/shell-键控更新调制"——这与 Q15 M4
  (gated identity/quantile-shell transport) 的 *动作族* 同源。但 Q15 的动作是 **post-CMA
  frozen map + identity fallback**（输出端 frozen 映射，含"不修正"安全分支），而 D2-D5
  全部是 **equalizer 抽头/代价的 always-on 在线更新**，无 identity fallback、无 frozen map。
  → **动作族同源，但 Q15 的 identity-fallback 分支 + post-proc frozen map 是 D2-D5 未有的
  新动作元素**。
- **同 information boundary？** 否。D2-D5 全是 always-on 在线更新（用全窗/逐符号统计）；
  Q15 是 **prefix-only 因果边界**（128-sym prefix frozen，suffix 不进 selection）。D4 虽用
  pilot+payload 但 payload 仍在线更新，非 prefix-frozen。→ **信息边界不同**。
- **同 problem？** 部分是。D2-D5 解决的是"高阶/PS-QAM 下盲均衡跟踪/收敛"（PMD、SOP、
  amplitude-distribution）；Q15 解决的是"dual-pol 16QAM 内环 shell collapse 的部分恢复 +
  健康 prefix 零回归"。C6 经验示 CMA 对 shaped QAM ~50% 实现崩（实现依赖失败）——这是 Q15 C
  的**实证现象佐证**，但 C6 的解是 TX 端，Q15 的解是 receiver-only post-proc。→ **问题部分
  重叠（collapse 现象），但解决范式不同**。

**碰撞结论（基于已获取 6 核心，D1 全文缺失为关键未知）**：Q15 action space **不是空白**
（D2-D5 在 equalizer 层有 radius/shell-键控成熟先例）；但 Q15 的三差异化（prefix-only 因果
边界 + identity fallback 健康零回归 + post-proc frozen map）**未被 D2-D5 等价覆盖**。是否
被 **D1（shell-partitioned MMA + soft switching，全文缺失）** 等价覆盖仍未知 → collision
评估 **未闭合**，保持 `PENDING_STEP35`。

### 2. 现有方法已知局限（原文证据，非"尚无人做"空白）

| 局限 | 原文证据（论文+章节） |
|---|---|
| 半径/shell-键控切换服务**性能优化**非安全，无 collapse detector、无 identity fallback | D3 Sec.II/Sec.VII（"region 假设健康收敛轨迹，映射到 MSE 阶段"）；D2/D4/D5 均无 detector/fallback 字段 |
| 固定 PDF/归一化假设（D4/D4′）无法区分健康 vs 塌缩输出 | D4 Sec.II-E + D4′（"transmitted Maxwell-Boltzmann f(R_k) 假设已知固定"——正是 Q15 A 命名的失效假设） |
| CMA 对 shaped QAM 实现依赖失败（~50% 崩）但解需 TX 端修改 | C6 Sec.I + Fig.5a（"only ~half of realizations equalize"）+ Sec.VIII（"require filters at the transmitter"） |
| MSE 稳定 ≠ 无发散（固定参数 CMA 可名义稳定但最坏序列发散） | C2 Sec.8（"many practically relevant adaptive algorithms are non-robust although they are MSE-stable"） |
| PRDE 对 16QAM 无增益（Q15 的目标调制） | D2 Results（"PRDE gives no advantage over RDE for 16QAM"——显式负面结果） |
| D5 数据驱动半径估计假设内环保靠（正是 shell collapse 违反的） | D5 Sec.2（"用最内 5 环"）+ 适用边界（"requires innermost rings visible; extreme shell collapse untested"） |

**注意（FR-23）**：上表是新颖性原料（空白/局限，领域级），**不是问题**。必须经下方 Q15
problem table 转译成 M-C-A 矛盾、过四判据才是 Q#。

### 3. 最近 2-3 年趋势

样本：D4 (2021), D5 (2022), C6 (2024) 为近期（2021+）；D2 (2015), D3 (2006), C2 (2015) 为经典。

- **趋势 1（PS-QAM 盲均衡）**：从"固定 PDF 半径决策"(D2 2015 PRDE) → "likelihood 门控
  payload 更新"(D4 2021 LBS-RDE) → "数据驱动半径估计"(D5 2022 K-means)。方向是 **越来越
  少依赖发射端先验、越来越多从接收信号本身估统计**。证据：D2 用固定 P(r) LUT；D4 用已知
  f(R_k) 算 α 但门控 payload；D5 完全从接收直方图估 K 和 R_k。
- **趋势 2（shaped QAM CMA 失败的认知）**：从"高阶 QAM 跟踪差"(D2/D3) → "shaped QAM
  Gaussian 致 HOS 对比度消失"(C6 2024 峰度问题框架)。C6 首次系统量化 CMA 对 shaped QAM 的
  实现依赖失败率（~50%）。
- **趋势 3（解的位置）**：D2/D3/D4/D5 全在 **equalizer 抽头/代价**；C6 移到 **TX+RX 联合**
  （TX 注入相关）。**无一篇在 receiver-only post-proc frozen map 层做**（Q15 的位置）。

**样本充足性**：仅 3 篇 2021+（D4/D5/C6），**不足以强外推趋势**。标注 `INSUFFICIENT_EVIDENCE`
对"全面趋势"，但上述 3 条方向性观察有原文支撑。

### 4. 背景时间线、核心挑战、Q15 研究定位

**历史演进**：
- 1990s-2005：CMA/MMA 经典盲均衡（Godard CMA, Ready&Gooch RDE[9], Yang/Werner MMA[8]）；
  hybrid 方法（CMA+DD, dual-mode, BCMA, CCA）—— D3′(ISCC 2005) 综述。
- 2006：D3 radius-adjusted region switching（首次 radius-keyed 联合 µ/λ 切换）。
- 2010s：PS-QAM 商用化（Maxwell-Boltzmann, Kschischang&Pasupathy[20]）；RDE 对 PS 不适配
  暴露。
- 2015：D2 PRDE（概率半径加权）；C2 发散理论（l2 vs MSE）。
- 2020-2021：D4/D4′ likelihood-gated RDE（pilot+payload 门控）。
- 2022：D5 数据驱动半径估计（K-means）。
- 2024：C6 temporal-correlation pr-MMA（TX+RX 联合解 shaped QAM CMA 失败）。

**核心挑战**：高阶/PS-QAM 下盲均衡的 (a) 跟踪动态信道（PMD/SOP）；(b) 收敛可靠性（实现/
初始化依赖失败）；(c) fixed-normalization vs data-driven radius 的权衡。

**Q15 研究定位**：Q15 不在 equalizer 抽头/代价层（D2-D5 的位置），也不在 TX+RX 联合层
（C6 的位置），而在 **receiver-only post-CMA frozen map + identity fallback** 层。区分：
- **历史演进**：radius-keyed switching 思想源自 D3（2006），经 D2/D4/D5 演化到 PS-QAM。
- **当前 comparator**：D4（likelihood RDE，JLT 2021 Q1）+ D5（K-means，COL 2022）是最近
  PS-QAM 盲均衡 comparator；C6（pr-MMA，JLT 2024）是 shaped-QAM CMA 失败的最近实证。
- **候选包装**：Q15 差异化 = (a) prefix-only 因果边界（D2-D5/C6 全无）；(b) identity
  fallback 健康零回归（D2-D5/C6 全无安全分支）；(c) post-proc frozen map（D2-D5 是
  equalizer 内部，C6 是 TX+RX）。**这三点是否构成可辩护新颖性，待 D1 全文 + Step 3.5**。

### 5. Q15 三差异化的信息增量审计

| 差异化 | D2 | D3 | D4 | D5 | C6 | 信息增量判断 |
|---|---|---|---|---|---|---|
| prefix-only 因果边界（128-sym prefix frozen，suffix 不进 selection） | 无（always-on 全窗 P(r)） | 无（always-on 逐符号 R_n 选 region） | 部分（pilot+payload 但 payload 在线更新，非 prefix-frozen） | 无（batch 全块聚类） | 无（TX+RX，非 prefix） | **有增量**——无一篇做 prefix-only frozen selection（因果隔离） |
| identity fallback 健康零回归（gate 关闭 = bit-identical baseline） | 无（P(r) 恒更新） | 无（λ∈[0,1] 混合，绝不"不修正"） | 部分（α<α_th 丢样本但滤波器仍更新 pilot） | 无（重聚类后恒更新） | 无（pr-MMA 恒更新） | **有增量**——D3 λ 混合两误差但不产生"bit-identical passthrough"；D4 丢样本但 pilot 仍更新。无一篇保证健康 prefix 零回归 |
| post-proc frozen map（不改 equalizer 抽头/代价） | 否（改 RDE 代价） | 否（改抽头更新） | 否（改 RDE 更新） | 否（改半径喂 RDE） | 否（TX+RX pol-demux） | **有增量**——全部在 equalizer/代价/TX 层；Q15 在 post-proc 输出端 frozen map |

**结论**：三差异化相对 D2-D5/C6 **各有真实信息增量**（无一篇等价覆盖）。但这是相对**已获取
6 核心**的判断；**D1（shell-partitioned MMA + soft switching）全文缺失是关键未知**——若 D1
的 shell 分区 + soft switching 已含 identity 分支或 post-proc 映射，则增量缩水。

### 6. C2/C6 及各论文 baseline 是否表明 robust CMA/MMA/RDE 能更便宜吸收问题

| 候选 cheap-alt | 来源 | 能否吸收 Q15 问题（shell collapse） | 证据 |
|---|---|---|---|
| robust CMA（JR-CMA: AGC+重置+变步长） | L-DP8（既有 identity） | **部分**——AGC 稳功率 + 误差阈值重置可防深衰落发散，但 **无 collapse detector + 无 identity fallback**，无法保证健康零回归 | L-DP8 基线仅 CMA |
| 换 MMA/RDE 代价（D2 PRDE, D4 LBS-RDE） | D2/D4 | **部分**——PRDE 对 16QAM 无增益（D2 显式负面）；LBS-RDE 解 PMD/SOP 非 collapse | D2 Results; D4 scope |
| radius-adjusted switching（D3 RMMA/RMDA） | D3 | **部分**——region 切换服务性能优化非安全，假设健康轨迹 | D3 Sec.VII |
| equalizer state caching | C5（gap，未获取） | **未知**——全文缺失 | — |
| dual-mode switching（CMA+DD） | C7（gap） | **未知**——全文缺失 | — |
| CMA 初始化修复（null-space, GA） | C1/C8（gap） | **未知**——全文缺失，且 C1 解 MIMO>3 singularity 非 dual-pol 16QAM 内环 | — |
| temporal-correlation pr-MMA | C6 | **否**——需 TX 端修改，非 receiver-only；不解 collapse detector/fallback | C6 Sec.VIII |
| l2-stability 理论（步长界） | C2 | **否**——分析框架非方法；给步长界但不提供 detector/fallback | C2 Sec.8 |

**结论**：已获取论文中 **无一条 cheap-alt 能完整吸收 Q15 问题**（都缺 collapse detector +
identity fallback）。但 C1/C3/C4/C5（初始化/MMA 稳态/analytical MMA/state caching）全文
缺失，**无法确认这些 cheaper 路径能否吸收** → cheap-alt closure **保持 PENDING_STEP35**。

### 7. Baseline 出现频次/任务匹配矩阵 + 当前传统 comparator 候选

| Baseline | 出现论文 | 任务匹配（dual-pol 16QAM collapse） | 代码 | 推荐优先级 |
|---|---|---|---|---|
| CMA（fixed-µ FIR） | D2/D3/D4/D5/C6 全引 | ✅ 直接（Q15 的 M） | 无（经典，易自实现） | 1（Go comparator，传统未优化 baseline，FR-25） |
| RDE（标准 radius-directed） | D2/D4/D5 | ✅ 直接（Q15 post-proc 在 RDE 输出后） | 无（经典） | 1 |
| MMA / pr-MMA | D3/D5/C6 | ✅ 直接（shaped QAM 对口） | C6 部分（Optilux 仅信道模型） | 1 |
| DD-LMS（decision-directed） | D4 | ⚠️ 部分（D4 用作反馈 eq baseline） | 无 | 2 |
| STD-RDE（最近半径分配） | D4 | ✅ 直接 | 无 | 1 |
| CMA-MMA 两阶段 | C6 | ✅ 直接（C6 的 benchmark） | 无 | 1 |
| FDA-RDE（fully-data-aided） | D4 | ⚠️ oracle 上界（FR-25: 只作 Kill 工具非 Go） | 无 | 3（Kill 工具） |

**当前传统 comparator 候选**（FR-25: Go 判据 = 赢传统未优化 baseline）：
1. **fixed-µ CMA FIR**（Q15 的 M 本身，最直接 Go comparator）
2. **STD-RDE / CMA-RDE 两阶段**（radius-directed 主流）
3. **CMA-MMA / CMA-pr-MMA**（shaped QAM 对口，C6 benchmark）

oracle 上界（FDA-RDE）按 FR-25/FR-21 只作 Step 4a 维度 D 收尾 Kill 工具，**禁当 Go 判据**。

### 8. D3/D4/C6 写作架构汇总 + 可复用叙述骨架

**共性模式**：
- **章节结构**：D4 有独立 System Model(Sec III)+Algorithm Design(Sec II)；D3（letter）和 C6
  融合无独立章。**D4 的分离模式更适 Q15 期刊论文**。
- **参数展示**：D3 表驱动（4 表/4 页）；D4/C6 散落散文。**D3 的表驱动 + D4 的 Notation
  内嵌**是折中。
- **图表**：D4 9 图 0 表；C6 14 图 0 表；D3 4 图 4 表。**性能曲线(NGMI/MI/MSE vs SNR/DGD)
  + 决策区/块图**是标配。
- **实验组织**：D4 4 baseline + 多轴消融(POH×DGD×entropy×损伤×延迟)；C6 5 algo + CPRS
  on/off；D3 3 baseline + region 数。**D4 的多轴消融最完整**。
- **叙述**：D4/C6 "问题→先验分类→空白→我们思想" Intro；D3 紧密动机链。**贡献列表非
  bullet，织入散文**（letter/期刊均常见）。
- **公式**：变量内嵌引入；推导叙述在场；方程编号交叉引用。
- **参考**：D4 cite-then-build；C6 括号数值聚句末。**基础 ref（Godard CMA, Ready&Gooch
  RDE, Savory 数字相干, Kschischang PS）多未在 GW** → Step 3.5 补。

**可复用叙述骨架**（综合 D3/D4/C6）：
1. Intro: PS/高阶 QAM 商用动机 → 盲均衡挑战 → radius/shell-键控先验(D2-D5) → 空白(无
   prefix-only + identity fallback + post-proc) → Q15 贡献预览
2. System Model: dual-pol 16QAM 接收机 + fixed-µ CMA 内环 + shell collapse 现象定义
3. Algorithm Design: prefix-gated identity/quantile-shell transport policy + collapse
   detector + identity fallback
4. Experiments: vs fixed-µ CMA / STD-RDE / CMA-MMA（传统 comparator）+ FDA-RDE oracle 上界
   （Kill 工具）+ 消融（prefix 长度 / gate 阈值 / shell 数）

**经典段落仿写**（D4/C6）：
- D4 Sec IV-C 收尾："We conclude that a strong deviation from the AWGN assumption…has an
  impact on the blind operation…Nevertheless, the impairments values…are much larger than
  what is usually found…" → 仿写：定量适用边界作收尾结论。
- C6 Sec.I 峰度问题段："PCS-QAM signals tend to have a Gaussian distribution…separating a
  mixture of two iid Gaussian signals…is not possible…the contrast function…decreases or
  even vanishes…" → 仿写：先陈述常规方法失败的机制原因再提修复。

### 9. D2/D3/D4/D5/C6 实验完备性 benchmark 对标汇总

| 维度 | D2 | D3 | D4 | D5 | C6 | 领域惯例/盲点 |
|---|---|---|---|---|---|---|
| seeds/运行数 | 1($2^{18}$ sym) | 40(R)/1000(MSE) | 未明(D4′ 200) | 无 | 101 实现 | **多数无 error bars/CI/检验**——盲点 |
| baseline 矩阵 | 1(RDE) | 3(MCMA/CCA/CMA+SDD) | 4(CME/STD-RDE/FDA-RDE/DD-LMS) | 2(STD-CMMA/STD-RDE) | 5 algo | 数 1-5；**D4 最完整** |
| 公平调参声明 | 是(µ 扫) | 是(Table III) | 是(per-algo/SNR) | **否** | **否**(hand-tuned) | D5/C6 是盲点 |
| 消融 | 无正式 | region 数 | POH×DGD×entropy×损伤×延迟 | **无** | CPRS/MMA↔pr-MMA | **D5 无消融**——盲点 |
| 信道模型 | 真实光+理想化数字 pol 旋转 | SPIB 微波(真实场测量) | 仿真粗步双折射+Jones SOP | **真实光纤实验** | Optilux 一阶 PMD(理想化) | D5 V=3 最高；C6/D4 理想化 |
| 拓扑多样性 | 2 调制+仿/实 | 2 调制×7 SPIB | 单拓扑(30×100km) | 单链路/格式 | 单链路/格式 | **多低**——盲点 |
| 复杂度 | 理论(+2 实乘) | D3 无(D3′ FLOPS) | 无 O() | **无** | 理论 O() | **D4/D5 无**——盲点 |
| VVUQ | V2/V'2/U2 | V2/V'2/U2 | V2/V'1/U2 | V3/V'2/U1 | V2/V'2/U2 | **U 普遍弱**(无 CI/检验) |

**领域惯例**：多数用多实现/多条件但 **无统计检验、无 error bars**；baseline 数 1-5；复杂度
多仅理论 O()。**盲点**：统计显著性检验、拓扑多样性、推理延迟。

### 10. Q15 problem table（M-C-A + 四判据 + 证据指针 + 反证 + 未决债务）

> **纪律（task §3 纪律 3 + FR-23/FR-25）**：下表是 Step 3 精读后的 *暂定* problem formalization。
> D1/C1/C4 全文缺失使四判据最终状态、novelty、cheap-alt closure 保持 `PENDING_STEP35`。
> **不因 T020 有诊断信号自动 PASS**。不宣称 problem survives conventional baseline。

| 要素 | 内容 | 证据指针 | 状态 |
|---|---|---|---|
| **M** | fixed-parameter blind FIR CMA + always-on blind output calibration（标准 CMA-RDE 链） | D2/D3/D4/D5 全引 CMA；C6 示 CMA 对 shaped QAM 失败 | confirmed（精读验证） |
| **C** | dual-pol 16QAM 接收机在部分随机实现/初始化下产生低功率 shell collapse | C6 Fig.5a（~50% 实现崩）；C2 Sec.8（MSE 稳定但最坏序列发散）；T020/M4 诊断信号（DIAGNOSTIC_ONLY） | partial confirmed（C6 是 64QAM 非 16QAM；T020 是 diagnostic 非 formal） |
| **A** | 传统方法缺 receiver-visible collapse detector + 安全 identity fallback；或固定归一化无法区分健康 vs 塌缩输出 | D4 Sec.II-E（固定 f(R_k) 假设）；D3 Sec.VII（region 假设健康轨迹）；D2/D4/D5 无 detector/fallback 字段 | partial confirmed（精读确认 D2-D5 无 detector/fallback；但 D1 未知） |
| **产出形态（待检验）** | prefix-gated identity/quantile-shell transport policy（post-CMA frozen map + identity fallback） | Q15 假说；T020/M4 diagnostic | tentative（T020 是 diagnostic_only_non_formal） |

**四判据**：

| 判据 | 状态 | 理由 |
|---|---|---|
| 1 具体技术矛盾（M-C-A 完整） | ✅（形式过）| M/C/A 三要素明确，是句子级可解陈述 |
| 2 方法产出形态 | ⚠️ UNKNOWN→partial | prefix-gated policy 形态有 T020 diagnostic 支撑，但信息增量待 D1 + Step 3.5 验证（§5 示相对 D2-D5/C6 有增量，D1 未知） |
| 3 近期 baseline 可对标 | ✅（精读确认）| fixed-µ CMA / STD-RDE / CMA-MMA 是 2019+ 顶刊 comparator（D4 JLT2021/D5 COL2022/C6 JLT2024）|
| 4 能做可量化对标 | ✅（框架确认）| PI-SER/BER/NGMI vs fixed-µ CMA 可量化（D4 NGMI 框架可借鉴）|
| **综合** | **PENDING_STEP35** | 判据 2（信息增量）依赖 D1 全文；cheap-alt closure（§6）依赖 C1/C3/C4/C5 全文 |

**Q# 候选**：Q15 可形成 *暂定* Q# 候选（M-C-A 形式过判据 1/3/4，判据 2 partial）。但 **不
记为四判据全过的 Q#**，保持 `PENDING_STEP35`。不进 Contract Step 1 假设引用。

### 11. D1/C1/C4 缺失分别改变哪项结论 + Step 3.5 mandatory query/citation targets

| 缺失论文 | 改变哪项结论 | Step 3.5 mandatory target |
|---|---|---|
| **D1**（shell-partitioned MMA + soft switching, EUSIPCO 2007） | **最关键**。决定 Q15 的 shell-transport + gated action 是否已被 D1 等价覆盖（§5 信息增量审计、§10 判据 2、collision 闭合）。若 D1 的 shell 分区 + soft switching 已含 identity 分支或 post-proc 映射 → Q15 novelty 大幅缩水 | 必须获取 D1 全文（Zenodo OA flag 但 tools/download 解析失败；非 IEEE blit 不可用）。Step 3.5 query: "shell partitioned MMA soft switching identity fallback"；citation target: EUSIPCO 2007 Poznan proceedings |
| **C1**（null-space init CMA, PIERS 2019） | 决定"更便宜的 CMA 初始化修复"能否吸收 Q15 问题（§6 cheap-alt closure）。C1 解 MIMO>3 singularity 非 dual-pol 16QAM 内环，但需全文确认 | 获取 C1 全文（IEEE PIERS paywall；blit 标题搜不到）。Step 3.5 query: "null space initialization CMA singularity dual polarization" |
| **C4**（analytical MMA, IJDMB 2010） | 决定"换更聪明的 MMA 代价"能否吸收 Q15 问题（§6）。C4 是 analytical MMA batch+adaptive，比 MMA 更低残差 | 获取 C4 全文（Hindawi OA pdf_url 解析失败；非 IEEE）。Step 3.5 query: "analytical multimodulus algorithm blind demodulation time-varying MIMO" |
| (附带) C3（MMA steady-state, Signal Processing 2014） | 决定"MMA 稳态 EMSE"对标"换 MMA 代价就行吗"基线（§6） | 获取 C3 全文（Elsevier OA 解析失败） |

**Step 3.5 mandatory debt 总结**：D1（direct collision 闭合）+ C1/C3/C4（cheap-alt closure）
是 Step 3.5 必补。不做第四轮 D1/C1/C4 下载（task 纪律 6）；它们进入 Step 3.5 mandatory
query/citation targets，由主控/用户裁决获取路径（机构 VPN / 作者邮件 / 等 OA）。

### Q15 Step 3 终态

- **status**: `STEP3_CONTENT_COMPLETE_Q_PENDING_STEP35`（6 独立核心精读合格 ≥5 门槛；
  综合分析完整；暂定 Q# 候选形成但四判据 2 + cheap-alt closure pending D1/C1/C4）
- **mission_method_delta**: `NONE`（GW Step 3 精读是 formal 必经步骤，不冒充新方法进展）
- **未进入**: Step 3.5 / Step 4a / Contract / Execute / 任何实验
- **未宣称**: novelty / problem survives conventional baseline / Q15 四判据全过
- **未改**: 全局步骤进度表、`.sessions/**` owner/mission/log/decisions/master-state/current YAML

---

## Q15 Step 3.5 定向补充检索 + D1 精读（2026-07-28，T023 / CP021）

> 来源：T023（CANDIDATE_FORMALIZATION，foreground epoch53 / CP021）。承接 T022
> `STEP3_CONTENT_COMPLETE_Q_PENDING_STEP35`。本节闭合 D1 全文缺失 + cheap-alt closure
> 两项 Step 3 mandatory debt，并修正 D3 collision 解释。D1 全文经 EURASIP 官方公开 PDF
> 获取；定向检索 12 query/2 源/收敛。详细 receipt 见
> `worker-logs/step-023-q15-terminal-adjudication.md`。
> **claim ceiling**：Q15 四判据最终状态由本节闭合后，进 Step 4a 实证审判（Phase B）。
> **不改全局步骤进度表**（Q15 是 RDL formal owner 下的独立 formalization 候选）。

### A1. D1 正式纳入（EURASIP 官方公开 PDF）

**身份 receipt**：

| 字段 | 值 |
|---|---|
| 标题 | Joint Blind Adaptive Equalization Based on Shell Partitioned Multi-Modulus with Soft Switching and Orthogonal Basis for 256 and 1024 QAM |
| 作者 | Grzegorz Haza, Ryszard Makowski（Wroclaw University of Technology） |
| venue | EUSIPCO 2007, Poznan, Poland |
| DOI | 10.5281/zenodo.40308 |
| EURASIP 官方 PDF | https://www.eurasip.org/Proceedings/Eusipco/Eusipco2007/Papers/a4p-h07.pdf |
| 获取路径 | DOI tools/download FAIL（与 T021 一致）；EURASIP 官方 PDF 公开下载 → `papers/downloads/2026-07-28/` → `tools/pdf_convert.py` 转 md → canonical `papers/manual/eurasip-2007-d1-shell-partitioned-mma/` |
| SHA256(source.pdf) | `0e104edda9c418d4…`（5,293,869 bytes, %PDF-1.6 magic） |
| content.md 行数 | 271 |
| title_check | PASS（expected ↔ verified Jaccard=1.0） |

**D1 机制提取（子 agent 全文精读，逐项 + 章节/公式指针）**：

1. **Shell 定义**：D1 的 "shell" 是 **1-D PAM 级幅度子集**，不是 2-D |y|² 同心圆环。
   按 √M-PAM 分解，实/虚轴各取 Q=√M/2 个 level 子集 {G_R;k}、{G_I;l}，ML 判决边界，
   子集半径 R²_R;k = E[|a_R|²|subset]（§1.2）。对 256-QAM Q=8/轴。
2. **ShMMA 更新规则**：是 **stochastic-gradient 抽头更新代价**（eq.5 代价 → eq.6 梯度 →
   eq.24 滤波器系数 w(n) 更新），不是 post-proc 输出 remap / frozen map。
3. **Soft switching**：由 **Edge-MSE 估计器**（eq.10，指数衰减窗 λ_E=0.98，§4）驱动，
   在 EMSE 阈值 Jstart=10^-1.8、Jstop=10^-3.3 间用 switching 函数 T(x)（eq.11-13）平滑混合
   MMA 与 ShMMA 梯度。**always-on 在线 per-symbol**，用整个 running eval 流——**非
   prefix-frozen，无因果隔离**。
4. **Identity passthrough 分支**：**无**。两分支（MMA、ShMMA）都恒更新抽头；soft switch
   是连续混合，非"门关=零修改"。**无 frozen map，无 healthy 零回归保证**。
5. **Problem target**：256-QAM 与 1024-QAM，**SISO 单通道**（FIR 非最小相位 h，SNR=45dB，
   相位偏移 φ=π/6）。**不涉及 16QAM、不涉及 dual-pol、不涉及内环 shell collapse / 低功率失效**。
   问题是常规高阶收敛跟踪 / eye-opening。

**D1 与 Q15 的 action+information+problem 三维碰撞（核心裁决）**：

| Q15 维度 | D1 覆盖？ | 证据指针 |
|---|---|---|
| (a) prefix-only 因果边界（suffix 不进 selection/gate/scale） | **NO** | Edge-MSE（eq.8/10）+ switch（eq.11-13）用整个 running eval 流，指数窗——无 disjoint calibration prefix，无因果隔离 |
| (b) identity fallback 分支（healthy prefix gate 选 identity） | **NO** | 无 identity/passthrough 分支；两分支恒更新抽头；soft switch 连续混合永不零修改（§2.2 eq.13） |
| (c) post-proc frozen 输出 remap（suffix 的 monotone radius map） | **NO** | D1 是抽头更新代价函数（eq.5→6→24），非输出变换；无"frozen" |
| (d) dual-pol 16QAM 内环 shell collapse 恢复 | **NO** | 目标 256/1024-QAM SISO；16QAM、dual-pol、collapse/低功率失效均未涉及（§4） |
| (e) gain/constellation normalization | **PARTIAL** | ShMMA 半径 R²_R;k/R²_I;l 隐式强制每 shell 目标功率（软归一化），但织入抽头更新代价，非独立归一化级（§1.2） |

**碰撞裁决**：**NONE**。D1 是**完全不同的机制**——在线 adaptive equalizer 抽头更新代价
（ShMMA）+ MMA/ShMMA 梯度 soft blend，针对 **SISO 256/1024-QAM 收敛**。Q15 是 **post-equalizer、
prefix-frozen、identity-fallback 输出变换**，针对 **dual-pol 16QAM collapse 恢复**。两者仅在
"shell"一词（且 D1 的 shell 是 1-D PAM 级幅度子集，非 2-D 半径环）和模糊的"调制相关半径
目标"上重合。**判据 2 的 D1 等价覆盖威胁解除**。

### A2. 定向检索（12 query / 2 源 / 收敛）

按 Step 3.5 矩阵（方法轴 × 问题轴）构造 12 组合，覆盖 conventional normalization /
regional-sliced MMA / dual-mode gated / post-eq radial calibration / collapse & scale
ambiguity。结构化源 = Semantic Scholar + OpenAlex（≥2）。每个组合结果存
`projects/thesis-fso/search-archive/2026-07-28/q15-step35-{slug}.json`。

| slug | query | hits |
|---|---|---|
| q15-step35-m1-agc-16qam | blind gain control amplitude normalization 16QAM coherent receiver | 4 |
| q15-step35-m2-agc-blind-equal-const | automatic gain control blind equalization constellation normalization | 5 |
| q15-step35-m3-radius-shell-partitioned | radius directed equalization multimodulus shell partitioned blind | 1 |
| q15-step35-m4-regional-sliced-mma | regional sliced multimodulus algorithm blind equalization | 2 |
| q15-step35-m5-dual-mode-gated-identity | dual mode gated blind equalization switching identity bypass | 2 |
| q15-step35-p6-dp-16qam-collapse | dual polarization 16QAM collapse singularity blind equalization | **0** |
| q15-step35-p7-receiver-prefix-scale-ambiguity | receiver prefix blind scale ambiguity calibration | 4 |
| q15-step35-p8-cma-inner-ring-collapse-lowpower | CMA inner ring collapse low power 16QAM | 1 |
| q15-step35-p9-posteq-radial-quantile | post equalization radial quantile calibration QAM | **0** |
| q15-step35-a1-rms-normalize-recover-collapse | RMS constellation normalization recover low power stream coherent | 6 |
| q15-step35-a2-monotone-radius-calibration-output | monotone radius calibration receiver output transform QAM | **0** |
| q15-step35-a3-identity-fallback-postcmA | post CMA identity fallback zero regression safety policy equalizer | **0** |

**收敛证据**：4 条最 Q15-specific 的吸收威胁轴 query（p6 dual-pol 16QAM collapse、p9 post-eq
radial quantile、a2 monotone radius output transform、a3 post-CMA identity fallback）**全 0
命中**。第 1 轮 method-axis（M1-M5）只返回 generic AGC/DSP/抽头更新（多在已知集或 off-topic）。
新增 must-read = **0**。**满足 gw-supplement 收敛判据（最后一轮新增必读/建议读=0）**。

**D1 引用链（双向）**：
- **前向（被引）**：**0**（S2 citationCount=0 + OpenAlex cited_by_count=0，filter=cites 交叉验证）。
  D1 是未被引叶节点——无新增前向竞品。
- **后向（参考文献）**：11 条。对 Q15 最相关的 foundation：
  - Lee 2000 "Shell partition-based joint blind equalization for QAM systems"（10.1109/30.846661）—
    D1 引用的 ShCMA [4] 源头；
  - Yang 2002 "The multimodulus blind equalization and its generalized algorithms"（10.1109/jsac.2002.1007381）—
    MMA 基础；
  - Godard 1980 "Self-Recovering Equalization and Carrier Tracking"（10.1109/tcom.1980.1094608）—
    CMA 基础。
  均为经典基础 ref，非 Q15 直接竞品。

### A3. 综合结论修正

1. **D3 collision 等级修正**：D3 的 `R_n=|z_n−ŝ_n|` 是 **decision-error radius**（z_n 到其
   hard-decision ŝ_n 的距离），**不是星座 shell radius**。D3 的 "regions" 是绕星座点的同心圆
   （MSE 阶段代理），不是 |z| 功率环。其机制仍是 **抽头更新**（µ_i/λ_i region 切换），
   非 output remap。→ collision 从 "HIGH（思想源头）/ shell radius" 下修为
   "decision-error-radius region switching（抽头更新层）"。这不改变 D3 与 Q15 信息边界
   不同（D3 always-on 全窗 vs Q15 prefix-only）的结论，仅修正 R_n 的物理含义。
2. **D1 不再列"全文缺失"**：已精读，collision = NONE（见 A1）。
3. **Q15 判据 1 修正**：M-C-A 句子级成立（M/C/A 三要素明确、可解）。Step 3.5 检索显示
   无论文直接记录 dual-pol 16QAM 内环 collapse + 接收端恢复（p6=0、p8=1 低优），但 Step 3.5
   已尽检索义务且 D1 零碰撞。**按主控授权的宽松解读，判据 1 = PASS**（句子级 M-C-A 成立 +
   检索尽 + D1 无等价覆盖；C 的直接发表证据缺失由 T020 diagnostic + C6 现象佐证补强，进入
   Step 4a 实证闭合而非文献闭合）。
4. **Q15 判据 2 修正**：D1 零碰撞解除判据 2 的 D1 等价覆盖威胁。但判据 2 仍只能由
   **可执行构造 + 相对合法常规链的信息增量** 支持——prefix-only / identity fallback /
   post-proc 的结构差异**不自动当信息增量**。T020 M1 振幅公式错误（功率比直接乘复振幅，缺
   平方根）+ evaluator 不恢复尺度，使 M4 收益可能只是补常规 gain normalization。
   → 判据 2 = **PARTIAL**，**必须由 Phase B 正确归一化 comparator 实证裁决**。
5. **判据 3/4 保持 PASS**：fixed-µ CMA / STD-RDE / CMA-MMA 是 2019+ 顶刊 comparator（存在
   comparator）；PI-SER/BER 可量化对标（框架确认）。但判据 3 PASS 仅表示 comparator 存在，
   **不表示 comparator 已公平实现**——correct sqrt-normalization comparator 尚未在 T020 出现，
   是 Phase B 必测项。

### Q15 四判据表（Step 3.5 修正后）

| 判据 | 状态 | 理由 | 证据指针 |
|---|---|---|---|
| 1 具体技术矛盾（M-C-A） | ✅ PASS | M/C/A 三要素明确，句子级可解；Step 3.5 检索尽 + D1 零碰撞；主控授权宽松解读 | 本节 A3.3；A2 收敛表 |
| 2 方法产出形态 | ⚠️ PARTIAL | D1 零碰撞解除等价覆盖威胁；但 prefix-only/identity/post-proc 结构差异不自动当信息增量，须 Phase B correct-normalization 实证 | 本节 A3.4；M1 振幅公式 audit（worker log §B0） |
| 3 近期 baseline 可对标 | ✅ PASS | fixed-µ CMA / STD-RDE / CMA-MMA 是 2019+ 顶刊 comparator（D4 JLT2021/D5 COL2022/C6 JLT2024） | lit notes §7（Step 3） |
| 4 能做可量化对标 | ✅ PASS | PI-SER/BER/NGMI vs fixed-µ CMA 可量化 | lit notes §7 |
| **综合** | **3 PASS + 1 PARTIAL** | 判据 2 由 Phase B Step 4a 实证闭合 | — |

**Q# 状态**：Q15 在 Step 3.5 后 3 判据 PASS + 判据 2 PARTIAL。**判据 2 的实证闭合是 Phase B
Step 4a 维度 D 的核心任务**：用 correct pooled/per-pol sqrt-RMS + gated scalar + robust scalar
等正确归一化 comparator，裁决 M4 收益是否只是补常规 gain normalization（吸收）还是非线性
monotone radius map 的独立信息增量。**Phase B 之前不记为四判据全过 Q#**。

### Step 3.5 cheap-alt closure

| 候选 | 来源 | 吸收 Q15？ | 证据 |
|---|---|---|---|
| robust CMA（JR-CMA） | L-DP8 | 部分（防深衰落发散，无 detector/fallback） | L-DP8 |
| correct pooled sqrt-RMS normalization | 本节 Phase B 必测 | **未知——Phase B 实证** | M1 audit |
| correct per-pol sqrt-RMS normalization | 本节 Phase B 必测 | **未知——Phase B 实证** | M1 audit |
| gated scalar（M4 gate + correct scale） | 本节 Phase B 必测 | **未知——Phase B 实证** | M1 audit |
| robust scalar（median/trimmed） | 本节 Phase B 必测 | **未知——Phase B 实证** | M1 audit |
| 换 MMA/RDE 代价 | D2/D4 | 部分（PRDE 对 16QAM 无增益[D2]） | D2 Results |
| radius-adjusted switching（D3） | D3 | 部分（decision-error-radius region 切换，抽头更新非 output remap） | D3 §VII |
| temporal-correlation pr-MMA | C6 | 否（需 TX 端，非 receiver-only） | C6 §VIII |

**cheap-alt closure**：已获取论文无一条完整吸收 Q15；C1/C3/C4 全文缺失但 Step 3.5 定向检索
（m4 regional-sliced MMA=2、m3 shell-partitioned=1）未发现能改变判断的直接竞品。
**吸收威胁的核心未知 = correct normalization comparator 是否吸收**，由 Phase B 实证闭合。

### Q15 Step 3.5 终态

- **status**: `STEP35_CONVERGED_D1_ZERO_COLLISION_Q2_PENDING_PHASE_B`（检索收敛、
  D1 零碰撞、cheap-alt closure 完成；判据 1/3/4 PASS、判据 2 PARTIAL 待 Phase B 实证）
- **mission_method_delta**: `NONE`（Step 3.5 是 formal 必经步骤，不冒充新方法进展）
- **进入**: Phase B Step 4a 条件式审判（correct-normalization 吸收裁决）
- **D1 debt 闭合**；cheap-alt closure 完成（C1/C3/C4 缺失不影响目标判断）
- **未改**: 全局步骤进度表、`.sessions/**` owner/mission/log/decisions/master-state/current YAML

---

## Q15 Step 4a 终局审判结果（2026-07-28，T023 / CP021）

> 来源：T023 Phase B（条件式 Groundwork Step 4a 维度 D）。承接 Q15 Step 3.5
> （`STEP35_CONVERGED_D1_ZERO_COLLISION_Q2_PENDING_PHASE_B`）。本节闭合判据 2 的
> 实证裁决。隔离目录 `direction-lab/scout/q15-step4a-normalization-adjudication/`，
> 详细数字见该目录 `synthesis.md` 与 `artifacts/result.json`。

### 判据 2 实证闭合：FAIL（被吸收）

用 correct pooled/per-pol sqrt-RMS + gated-scalar ablation + robust scalar
（median）四个正确归一化 comparator 对 M4 做终局公平审判（7 cells × 40 seeds =
old 201-220 + fresh 241-260，seed-cluster 聚合，10k bootstrap 95% CI，MDE=0.005）：

| slice | baseline | M4 | 最强 correct（robust_scalar） | M4 vs robust |
|---|---|---|---|---|
| old 201-220 | 0.3143 | 0.2317 | **0.2232** | M4 输 +0.0085（>MDE） |
| fresh 241-260 | 0.4150 | 0.2830 | **0.2686** | M4 输 +0.0144（>MDE） |

**M4 在两个 slice 都输给最强正确归一化**，方向稳定（无符号翻转）。
gated_scalar_ablation（M4 gate + correct scale）≈ M4（overall 0.2513 vs 0.2574）→
map 不提供 gate+scale 之外的增量。correct scalar 在 healthy 上退化 0.016-0.027 < MDE，
是可用 conventional comparator。

**吸收机制**：collapse 是纯幅度尺度（z=c·s），correct sqrt 已 audit 精确恢复（SER=0
for all c）。M4 的非线性 monotone radius map 无法 beat 精确标量恢复，quantile 锚
引入轻微畸变致略输。M4 的 gate identity-on-healthy（healthy-worst Δ=0.0）是真实安全
属性，但 correct scalar 的 healthy 退化已 < MDE，故 always-on correct normalization
是公平 conventional comparator，problem 未 survive。

### Q15 四判据最终表

| 判据 | Step 3.5 状态 | Step 4a 终态 | 理由 |
|---|---|---|---|
| 1 具体技术矛盾 | PASS | PASS | M-C-A 句子级成立（不推翻） |
| 2 方法产出形态 | PARTIAL | **FAIL** | 实证：M4 输给 correct normalization 两 slice；map 无 gate+scale 外增量；problem 未 survive conventional baseline |
| 3 近期 baseline 可对标 | PASS | PASS | comparator 存在（correct normalization 已公平实现） |
| 4 能做可量化对标 | PASS | PASS | PI-SER 可量化 |
| **综合** | 3P+1PARTIAL | **判据 2 FAIL → Kill** | Q15 被 conventional normalization 吸收 |

### Q15 终态

- **status**: `Q15_ABSORBED_BY_CONVENTIONAL_NORMALIZATION_NO_GO`（判据 2 实证 FAIL）
- **mission_method_delta**: `NONE`（可靠负面 + evaluator/normalization 方法论教训，非方法）
- **未进入**: Step 5 / Contract / Execute / 论文声称
- **未给**: Step 4a recommendation / thesis-facing method card / 第四个 Q15 repair
- **Q15 退出**：本包后无 Q15 repair/factory 包
- **可回收**：evaluator/normalization 方法论教训（post-CMA output transform comparator
  族 MUST 含 correct pooled+per-pol sqrt-RMS 作 floor；功率比乘复振幅 bug 在
  rotation-only evaluator 下静默）
