# [S006] 对话 4：B11/B12 评点 + literature_notes 载波同步 v2 章节并入 + B1-B12 全 12 点总表最终合并

> 2026-07-04 | 精读沉淀补强·对话 4（评点收尾 B11/B12 + literature_notes 并入 + 总表最终合并）| 状态：B11/B12 评点完成 + literature_notes 载波同步 v2 章节并入完成 + B1-B12 全 12 点 35 Q# 总表落盘交用户排优先级
> 来源：H004（对话 4 任务）+ S005（B1-B10 总表，**计数 bug 修正 26→29**）+ S004（B1-B7 总表）+ 用户 7-4 手动下 B12 MAP 全文

## 目标

执行 H004 三件事：①B11 NDA-ML STO+CPE 评点（派 1 子 agent）②B12 频域 pilot 评点（派 1 子 agent，含用户新下 MAP 全文 150 行）③literature_notes 载波同步 v2 章节并入（综合分析+研究问题清单过四判据）+ B1-B12 全 12 点总表最终合并。守 3 步上限 + D018 中性提取 + FR-26 grep 核查 + 子 agent ≤15 分钟 + **主线不碰全文委托率 100%**（守对话 3 委托纠正纪律）。

## 记录

### 报到验证（Trigger 1+5）

- **Trigger 1（Session Start）**：topic-index 不变量 9 条确认；active topic conflicts = none；depends_on（2026-06-20-problem-driven-redirection）输出已满足；profile 最近纠偏 2026-07-04 S005"急于推进"+委托违规（第 7 次）；inflation check 本专题 5 S 文件（S001-S005），远未到 8 阈值。
- **Trigger 5（Handoff H004 接收）**：FR-26 主线独立 grep 核查 5 条关键事实全 PASS——
  - ① B11 锚 LPT.2024.3523478 全文落盘 PASS：`papers/doi/10.1109_LPT.2024.3523478/` content.md(22779B/226 行)+source.pdf(1.78MB)
  - ② B12 锚 TCOMM.2022.3171809 + MAP oecc-psc62146 全文落盘 PASS：TCOMM content.md(64256B/590 行)+source.pdf(1.32MB)；MAP content.md(17823B/150 行)+source.pdf(0.59MB) 7-4 到位
  - ③ B9-Q1 ~3dB @ 3PNOB（H004 报"行 241/253 四处一致"）PASS **行号微调**：实际 L243（"∼3 dB"主体句）+ L253（Conclusion 重述"∼3 dB, ∼1 dB, ∼0.5 dB"）+ L245（0.8dB long-term 含湍流）。L241 是引出句不含 dB 数字。核心数字全 PASS。
  - ④ B1-B10 总表计数 **bug 发现**：S005 报"26 Q#"实际 29（B1-B7=20 + B8 主判定+Q1+Q2=3 + B9×3 + B10×3 = 29，B8"主判定"是 1 个标"不适用"的占位也算 1 条 Q#）。本轮修正。
  - ⑤ ao.581648 仍缺（B10-Q3 待全文债务）PASS：无新下载，债务保留。

- **范围核查**：本轮 B11/B12 评点 + literature_notes 并入 + 总表合并都在 S001 v2"对话 4"动作内，未违反"明确不含"（不判 Go/Kill / 不预设 Q# / 不改框架 / 不出星地激光通信大背景）。

### 步骤 1：B11/B12 评点（2 子 agent 并发，主线不碰全文委托率 100%）

派 2 子 agent 并发（B11/B12 各 1，全 PASS ≤15 分钟：B11 592s / B12 519s），主线 FR-26 独立 grep 核查关键 dB 数字。**主线未读任何全文 content.md，只读子 agent 产出的增量笔记 + grep 核查行号**（守对话 3 委托纠正纪律）。

#### FR-26 核查 B11/B12 关键 dB 数字

| 子 agent 声称 | 主线 grep 核查结果 | 结论 |
|---|---|---|
| **B11 +2dB SNR gain @ (8,8)-16APSK @ 7% HD-FEC vs DA ML**（行 181/191 双处一致）| python grep B11 锚：L181 "DA ML method exhibits a 2 dB SNR drop compared to our ap" + L191 Conclusion "2 dB SNR gain" + L183 "over twice the PN variance tolerance" + L143 "15 dB SNR (8,8)-16APSK 500kHz CLW" | **PASS**（双处一致 + 量级与第一梯队 B3-Q2 +2~3dB 同量级下沿）|
| **B11 行 33 假设湍流/Doppler/CFO 已补偿**（不撞 D006 依据）| grep "compensated"：行 33 "atmospheric turbulence, pointing error, Doppler shift, and CFO are totally compensated" | **PASS**（B11 前馈闭式 ML + 行 33 假设，不撞 D006 成立）|
| **B12 锚无 vs baseline dB gain**（SPR 失效点 −10/10dB 行 429 / OSNR 18-19dB 行 517）| python grep B12 锚：L429 SPR 失效点 + L517 脚注 5 "18-19 dB OSNR" + L269 MVU + L519 improved 估计器假设 MVU | **PASS**（B12 锚全文无"赢 RF pilot/BPS/V-V X dB"对比，仅内部估计器 vs CRLB）|
| **B12 MAP SNR penalty 4dB @ 100GBaud/150kHz vs PA ML 5dB / PA 7.5dB**（行 115）| python grep B12 MAP：L115 "MAP estimator performs the best" + L113 "SNR=40dB" + L115 "150 kHz" + "100 GBaud" / "64 GBaud" / "256-QAM" 全在 | **PASS**（MAP dB 数字行 115 一处集中，子 agent 报正确）|
| **B12 锚标题"In-Band and Out-of-Band Frequency Domain Pilots"**（双频段 pilot 非单纯频域 pilot）| grep "in-band"/"out-of-band"：L5/L37/L43 标题+Index Terms 多处确认 | **PASS**（B12 锚是双频段带内+带外 pilot，机制比单纯频域 pilot 精细）|

#### B11 评点收获（3 Q#，+2dB 跻身第一梯队）

笔记：`papers/_read_notes/_B11-nda-ml-sto-cpe-increment.md`（103 行）
读了：B11 锚 lpt.2024.3523478（226 行）+ cited-by 10.3390_s25164906（HSR 覆盖，背景引用非技术延伸）

**B11 全称确认**：NDA-ML = Non-Data-Aided Maximum Likelihood（盲最大似然，不依赖 pilot）/ STO = Symbol Timing Offset（符号定时偏差）/ CPE = Common Phase Error（公共相位误差）。IEEE PTL 2025 Vol.37 No.10，UIC+浙工大+港中深/NUSRI（Kam 团队"相位噪声 ML 估计"系列）。

**核心机制**：升 M₀ 次幂盲去调制相位（M₀ξ(k) 为 2π 整数倍→零相位）→ STO+CPE 化为单复正弦的频率+相位估计 → 复用 Wang 2022 [13] 单正弦 ML 框架得闭式 τ̂/φ̂（Eq.12-16）。**前馈、无环、无 OPLL**，复杂度低于 PA+定时分离组合。

| Q# | M-C-A 浓缩 | 撞 D006 | D005 够格 | 范围 |
|---|---|---|---|---|
| **Q1（核心）** | NDA-ML 联合 STO+CPE 闭式估计：升 M₀ 次幂盲去调制→单正弦 freq+phase→Wang[13] ML 闭式 τ̂/φ̂；+2dB SNR gain @ (8,8)-16APSK @ 7% HD-FEC vs DA ML（行 181/191）；>2× PN 容限；STO 概率 1 @ −10dB SNR | 否（前馈闭式 ML 无环路 TF，行 33 假设湍流/Doppler 已补偿）| **够格（量级达标下沿）**——+2dB 与 B3-Q2 +2~3dB 同量级；**条件性强**：仅 (8,8)-16APSK 成立，(4,4)-8APSK/(4,4,4,4)-16APSK 下 DA ML 持平（行 181）；CLW 容限超 DA ML 需付 1dB SNR cost（行 191）| in 倾向（声明 FSO 行 9/191）→ 仿真未建模 FSO 信道（行 33/155），迁移待做 |
| Q2（边界）| 湍流相位纳入 ML 似然的 D006 边界：B11 行 33 假设湍流已补偿，Σ_ε 假设 \|R(k)\| 稳定；湍流致 \|R(k)\| 时变→ML 偏置？前馈 ML 纳入湍流不撞，环路 H(z) 联合建模则撞 | **边界**（前馈不撞；环路 H(z) 联合建模则撞，只标不砍）| 待定量锚（open problem，原文无湍流 dB）| in（星地 FSO 湍流）—— 候选维度，原文未涉 |
| Q3（范围）| "FSO 适用"声明的仿真验证缺口：B11 声明 FSO（行 5/9/191）但仿真仅通用 CO-OFDM 无 FSO 信道（行 33/155）；+2dB 在通用 OFDM 成立，FSO 湍流信道下未知 | 否（验证范围维度，不涉环路 TF）| 不够格（验证缺口非性能改进，无新增 dB）| in 倾向（声明 FSO）→ 待验证 |

**关键发现**：
1. **B11-Q1 +2dB 跻身第一梯队**——继 B9-Q1 后**第二个达第一梯队量级**的非 B3 候选（+2dB vs DA ML @ 7% HD-FEC，行 181/191 双处一致）。与 B3-Q2 +2~3dB / B9-Q1 ~3dB 同量级下沿。**但条件性强**：仅 (8,8)-16APSK 成立 + CLW 容限付 1dB cost + 声明 FSO 但仿真未建模 FSO 信道。
2. **B11 是改进载波恢复算法**（NDA 盲估计），区别于 B8/B9 自相干绕过载波同步。陷阱 1 规避（NDA-ML ≠ 载波同步被绕过）。
3. **baseline 是 DA ML [10] + PA [8]（DSP 数字 CPE/STO 法）**——B11 在"频域 NDA-ML CPE"赛道，与 B6（OPLL 鉴相器）/B4（PADE/V-V）/B7（Gardner TED FOE）/B10（pilot-RLS）正交。
4. **不撞 D006 且边界清晰**——前馈闭式 ML 无环路 H(z) + 行 33 显式假设湍流/Doppler/CFO 已补偿，PN 是激光线宽 Wiener（行 51）非湍流相位。Q2 标"边界"（前馈 ML 纳入湍流相位不撞；环路 H(z) 联合建模则撞）。
5. **cited-by 极边缘**——10.3390_s25164906（HSR 地对车 FSO 覆盖）把 B11 作 ref [7] 引于背景文献簇，与载波同步无关。

#### B12 评点收获（3 Q#，锚+MAP 双视角）

笔记：`papers/_read_notes/_B12-freq-domain-pilot-increment.md`（111 行）
读了：B12 锚 TCOMM.2022.3171809（590 行）+ **🔴 用户 7-4 手动下 MAP oecc-psc62146（150 行）** + cited-by 3 篇（COMST Phase Noise Survey 1288 行 / acp.ipoc63121 待核 / MAP 本体）

**B12 锚全称确认**：Estimation of Phase Noise Based on **In-Band and Out-of-Band Frequency Domain Pilots**（Gävert & Eriksson，Chalmers 理工 + Ericsson 高级专家，IEEE TCOMM 2022）。**双频段 pilot**（带内+带外）非单纯频域 pilot——机制比预期精细。MAP = Maximum A Posteriori Probability Phase Recovery for 256-QAM（OECC/PSC 2025，BNU-HKBU Kam 团队）。

**核心机制**：
- **B12 锚**：频域 CW pilot 前馈相位估计——pilot 注入已知 f_CW，RX 频移+LPF 提取，三种估计器（BLUE/ML/**improved 滤 phasor 而非相位避开 unwrap 噪声放大，近似 MVU**）。最优 SPR（signal-to-pilot ratio）解析推导（β 最大化 SNDR）。in-band vs out-of-band trade-off（pilot 功率 vs 带宽/容量）。**前馈结构无环路 TF、无 OPLL**。
- **MAP**：时域 pilot-aided 联合 ML/MAP 相位估计——信号分 N_block 块，每块首符作 pilot（PA 粗估）→ PA ML 细估 → 联合 ML（初始相位 θ）+ MAP（Wiener 相位噪声 θ_k）。AOPN 模型（AWGN 致相位噪声高斯近似 + Wiener 叠加）。block-wise 并行架构。

**MAP 与 B12 锚关系**：MAP 引 B12 锚作 Ref[4]（"pilot-aided methods sacrifice spectral efficiency [4]"），把 B12 锚标为"频域 pilot 牺牲频谱效率"的相关方向；MAP 自身算法源自 Wang Ref[5]（joint ML/MAP sinusoid）。**MAP = B12 锚的 citer/对照方向（pilot-aided 大类下，时域 vs 频域机制独立）**，非直接频域延伸。

| Q# | M-C-A 浓缩 | 撞 D006 | D005 够格 | 范围 |
|---|---|---|---|---|
| **Q1（B12 锚核心）** | 频域 CW pilot 前馈相位估计迁移星地：补 Doppler 致 pilot 频偏跟踪 + 湍流 non-Wiener 相位扰动纳入 σ_Δ² 扩展；无 vs baseline dB gain（仅内部估计器 vs CRLB）| 否（前馈频域处理；迁移后保持前馈不撞，环路 TF 联合建模则撞，只标不砍）| **不够格（dB 维度）/ 结构性理论增量**（improved ≈ MVU + 最优 SPR 解析）| out（通用模型）/ 待迁移星地 |
| **Q2（MAP 核心）** | MAP 联合 ML/MAP 256-QAM 迁移星地高阶 QAM：Wang [5] 框架已支持 joint ML（频率+相位）+ MAP（Wiener），Doppler 是 ML 部分自然扩展；MAP SNR penalty 4dB @ 100GBaud/150kHz（vs PA ML 5dB / PA 7.5dB，行 115）| 否（前馈时域 pilot + 块并行 ML/MAP；迁移后保持前馈不撞，环路 TF 联合建模则撞，只标不砍）| **边际够格（同族 dB）**——MAP vs PA 差 3.5dB 落 D005 区间，vs PA ML 差 1dB 边际；baseline 是同族非传统 V-V/BPS | out（光纤 DCI）/ 待迁移星地 |
| Q3（边界）| 频域 CW pilot（B12 锚）+ 时域 pilot-aided MAP（MAP）联合架构在星地湍流：双重导频优势互补，湍流相位扰动纳入联合估计器状态方程则撞 D006 | **边界**（前馈级联不撞；联合状态方程/环路 H(z) 纳入湍流+多普勒则撞，只标不砍）| 待定量锚（open problem，原文无湍流 dB）| in（星地 COSC 湍流）—— 候选维度，原文均未涉 |

**关键发现**：
1. **B12 锚核心 = 频域 CW pilot 前馈相位估计 + 最优 SPR 解析框架**——improved 估计器（滤 phasor 而非相位）近似 MVU，大动态范围趋近 CRLB。in-band vs out-of-band trade-off 是 B12 锚与 MAP 时域 pilot 的根本差异点。
2. **B12 锚 D005 dB 维度不够格**——全文无"赢 RF pilot/BPS/V-V X dB"对比（仅内部估计器 vs CRLB）。但理论贡献（最优 SPR 解析 + improved ≈ MVU）是结构性理论增量。
3. **MAP dB 增益真实但同族**——MAP vs PA 差 3.5dB / vs PA ML 差 1dB（行 115）。落 D005 区间但 baseline 是 PA/PA ML 同族内部（非传统 V-V/BPS/DD-PLL），需注明"同族 dB"。
4. **B12 锚 + MAP 均 out 范围**——B12 锚通用复基带（wireless+optical）无星地/湍流/Doppler；MAP 相干光 DCI 背景无星地/湍流/Doppler。机制迁移星地是 Q# 候选维度。
5. **D006 边界模式扩展到 7 次**（B3-Q3/B6-Q2/B7-Q2/B9-Q3/B10-Q2/**B11-Q2/B12-Q3**）——"前馈/工具层不撞，环路 TF 联合建模则撞"模式在 B 档 12 点中重复 7 次。

### 步骤 2：literature_notes 载波同步 v2 章节并入 + B1-B12 全 12 点总表最终合并

**🔴 本节守 D018 中性提取——只标 D006/D005/范围三维，不判 Go/Kill。**

并入 `projects/thesis-fso/literature_notes.md`（在原"实验完备性对标汇总"节后追加"载波同步 v2 精读沉淀"整节）：

1. **载波同步 v2 综合分析**（5 小节）：
   - 现有方法分类（B 档 12 候选按技术路线 6 类：DSP 前馈 FOE/CPE / OPLL 硬件锁相 / 自相干架构绕过 / pilot-aided 高阶 QAM CPE / 子系统协同 / NDA-ML 盲估计）
   - 已知局限（7 条共同不足，含 **D006 边界模式 7 次**是 B 档最重要结构性发现）
   - 2-3 年趋势（5 条，DSP 前馈替代 OPLL / NDA 盲估计兴起 / 自相干架构成熟 / 高阶 QAM CPE 升级 / D006 边界模式持续）
   - 研究背景概述（时间线 1980s-2026 + 核心挑战 4 条 + 本研究定位）
   - 研究问题清单 [MUST]（35 Q# 过 glossary 四判据：全过 3 / 边际够格 7 / D006 边界 7 / 未过 18）

2. **载波同步 v2 文献条目 L11-L22**（12 篇精简版，每篇核心贡献+方法+baseline+关键 dB+Q#+笔记路径）

3. **B1-B12 全 12 点总表（35 Q#，修正 S005 计数 bug 26→29→35）**：
   - 总 Q# 数 **35**（B1-B7=20 + B8 主+2=3 + B9×3 + B10×3 + **B11×3 + B12×3**）
   - 撞 D006 明确撞 **0** / **边界 7**（B3-Q3/B6-Q2/B7-Q2/B9-Q3/B10-Q2/**B11-Q2/B12-Q3**）
   - D005 倾向够格 **10**（含 **B9-Q1/B11-Q1 第一梯队**）/ 边际够格 **4**（含 **B10-Q1/B12-Q2**）/ 待定量锚 **8** / 不够格不适用 **13**
   - 范围 **out 9**（含 **B8×3 地面 FSO / B10×2/B12×2 光纤**）/ in 或 in 倾向 **26**
   - **D005 够格梯度中性排不判 Go/Kill**：第一梯队 B3-Q2 +2~3dB > **B9-Q1 ~3dB（baseline 内部对照）** > **B11-Q1 +2dB（条件性强）** > B1-Q1/B2-Q2 +1dB；第二梯队 B7-Q1/B10-Q1/B12-Q2 结构性优势

#### D005 够格梯度（中性，不判 Go/Kill）

**第一梯队（有明确 dB 增益 + 范围 in/in 倾向，+2~3dB 同门达标）**：
- **B3-Q2**（+2~3 dB 强湍 4 支路）—— dB 最高 in
- **🔵 B9-Q1**（~3dB @ 3 PNOB DRE）—— dB 与 B3-Q2 同量级，baseline 内部对照，in 倾向待迁移
- **🔵 B11-Q1**（+2dB SNR gain @ (8,8)-16APSK vs DA ML）—— **本轮新跻身**，条件性强（仅 (8,8)-16APSK + 仿真未建模 FSO），声明 in 但仿真未验证
- B3-Q1（+0.9dB Q）—— 范围 out 光纤 DSCM
- B1-Q1 / B2-Q2（+1dB）—— in
- B5-Q2（7dB penalty）—— 范围 out 光纤 intradyne

**第二梯队（结构性优势，dB 偏小或维度错位）**：
- B7-Q1（0.6dB + 1.9×范围 / OSNR 10dB）—— in
- **🔵 B10-Q1**（无统一 dB，范围/鲁棒性）—— out 光纤/待迁移星地
- **🔵 B12-Q2**（MAP vs PA 差 3.5dB 同族 dB）—— out 光纤 DCI/待迁移星地
- B4-Q2 / B5-Q4（+70~100 Gbps 维度错位）—— in
- B5-Q1（±4.5GHz 覆盖 LEO Doppler）—— in
- B6-Q1（定性保锁 σ=2.6°/0.42dB + 30ns）—— in

**第三梯队（待定量锚 / open problem 级 / 待全文）**：
- B2-Q1 / B3-Q3 / B4-Q1 / B4-Q3 / B5-Q3 / B6-Q3 / B7-Q2 / B9-Q2 / B10-Q2 + **🔵 B11-Q2 / B12-Q3** + **🔵 B10-Q3 待全文（摘要 4dB）**

**第四梯队（风险偏高/不够格/不适用）**：
- B1-Q2 / B6-Q2 / B7-Q3 / B9-Q3 / B11-Q3 / B12-Q1 + **🔵 B8 主判定（无核心 Q# 自相干绕过载波同步）/ B8-Q1 / B8-Q2**

#### 关键观察（中性，辅助用户排优先级）

1. **🔵 B11-Q1 +2dB 跻身第一梯队**——继 B9-Q1 后第二个达第一梯队量级的非 B3 候选。与 B3-Q2 +2~3dB / B9-Q1 ~3dB 同量级，但条件性强。
2. **🔵 D006 边界模式扩展到 7 次**（原 5 + B11-Q2 + B12-Q3）——"湍流相位建模边界"是潜在一致性研究方向（与块 A/B/C/D Q11/Q12 Paillier 分治延续）。Go/Kill 留用户。
3. **🔵 B12 双视角**（锚 TCOMM 2022 + MAP OECC 2025）——pilot-aided 大类下时域 vs 频域机制独立，MAP 是 B12 锚的 citer 非直接延伸。
4. **B8 特例"载波同步冗余"持续成立**——自相干绕过载波同步。
5. **范围 out 比例 9/35 ≈ 26%**（新增 B12-Q1/Q2）——星地 in/in 倾向仍是主体 26/35 ≈ 74%。
6. **dB 量级 vs 同门 2-4dB**：第一梯队 B3-Q2/B9-Q1/B11-Q1 达标，B1/B2 +1dB 偏下沿，B7 0.6dB 偏低。

## 决策引用

- **无新建 D###**（评点 + literature_notes 并入 + 总表最终合并，Q# 留总表阶段用户排完优先级后判 Go/Kill，符合 D018 中性提取）
- 引用既有：D017 / D018 / D006（7 边界只标不砍）/ D005 / **D011 种子"16-QAM CPR 扩展"经 B10+B12 MAP 落地延伸**

## 范围确认

- 本轮是否在 scope boundary 内：**是**（B11/B12 评点 + literature_notes 并入 + 总表最终合并都是 S001 v2"对话 4"动作；Q# 候选只提取不判 Go/Kill）
- **守 3 步上限**：本轮 3 步（①报到+FR-26 核查 H004 ②B11/B12 两点并发评点+grep 核查 ③literature_notes 并入+总表最终合并+写 S006/H005）
- 守子 agent ≤15 分钟：2 子 agent（B11 592s / B12 519s），全 PASS
- **守 D018 中性提取**：B11/B12 新增 6 Q#（含 B8 主判定"无核心 Q#"模式——B11 非"无核心"是改进盲估计）+ 总表 35 Q# 全标三维，不判 Go/Kill
- **🔴 委托纪律守住**：本轮 B11/B12 两点各 1 子 agent，**主线不碰任何全文 content.md**（只读子 agent 产出笔记 + grep 核查行号），委托率 100%（延续对话 3 纠正）

## 后续

### 交用户（排优先级 + 对前几名判 Go/Kill）

**B 档 12 候选精读沉淀补强专题使命达成**：
- 12 份 gw-read 14 字段+7 项结构化笔记全完成（B1-B12，含 B5/B7 全文核验升级 + B8/B9/B10/B11/B12 新写）
- 每点 ≤5 篇 cited-by 验证全完成（B7/B11 池极小各 1 篇已说明）
- literature_notes 载波同步 v2 章节并入完成（综合分析 5 节 + 35 Q# 过四判据 + 12 篇文献条目 L11-L22）
- B1-B12 全 12 点总表 35 Q# 落盘交用户排优先级

**下一步（用户侧）**：
1. **排优先级**：基于 D005 够格梯度（第一梯队 B3-Q2/B9-Q1/B11-Q1 / 第二梯队 B7-Q1/B10-Q1/B12-Q2 等）+ 范围 in/in 倾向 + D006 边界模式 7 次，排 B 档 35 Q# 的优先级
2. **对前几名判 Go/Kill**：排完优先级后，对前 3-5 名走 gw-feasibility A0/A'/A/B/D 维度判 Go/Kill（D009 checklist 启用）
3. **D006 边界模式决策**：7 次"前馈不撞/环路 TF 联合建模则撞"是潜在一致性研究方向（湍流相位建模边界），用户决定是否作为独立方向探索
4. **ao.581648 债务**：B10-Q3 4dB OSNR gain 仅摘要，用户如继续尝试手动下可补全文核验

### 关键提醒给用户

1. **B1-B12 全 12 点总表已落盘**（本 S006 §步骤 2 + literature_notes.md"载波同步 v2 精读沉淀"节）：35 Q# 全标三维中性不判 Go/Kill
2. **第一梯队 3 个 dB 达标候选**：B3-Q2 +2~3dB / B9-Q1 ~3dB / **B11-Q1 +2dB（本轮新跻身）**——但各有条件性（baseline 内部对照 / 仅特定调制 / 仿真未建模 FSO）
3. **D006 边界模式 7 次**：潜在一致性研究方向（湍流相位建模边界），Go/Kill 留用户
4. **范围 out 9 个**：B8×3 地面 FSO + B10×2/B12×2 光纤 + B3-Q1/B5-Q2 光纤——星地 in/in 倾向仍是主体 26/35
5. **B8 特例"载波同步冗余"**：自相干绕过载波同步，与改进载波恢复正交
6. **D011 种子"16-QAM CPR 扩展"落地延伸**：B10 pilot-RLS → B12 MAP → ao.581648 KRLS 升级链（三者都光纤 out，迁移星地是 Q# 维度）
7. **ao.581648 仍缺**：B10-Q3 4dB OSNR gain 待全文核验
8. **专题使命达成可转 closed**：12 篇笔记 + literature_notes 并入 + 35 Q# 总表全完成，精读沉淀补强使命结束。后续 Go/Kill 判定回原专题 2026-06-20-problem-driven-redirection 或新开 Step 4a 专题
