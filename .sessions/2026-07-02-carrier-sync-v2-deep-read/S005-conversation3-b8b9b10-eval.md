# [S005] 对话 3：B8/B9/B10 评点 + B1-B10 总表续填

> 2026-07-04 | 精读沉淀补强·对话 3（评点 B8/B9/B10 + 续填总表）| 状态：B8/B9/B10 评点完成，B1-B10 总表 26 Q# 落盘
> 来源：H003（对话 3 任务）+ S004（B1-B7 总表 20 Q#）+ 用户 7-4 手动下 B9 DRE 全文

## 目标

执行 H003：B8/B9/B10 三点评点（3 子 agent 并发，**纠正对话 2 主线自读全文违规**）+ 续填总表 B8-B10 + B11/B12 预登记。守 3 步上限 + D018 中性提取 + FR-26 grep 核查 + 子 agent ≤15 分钟。

## 记录

### 报到验证（Trigger 1+5）

- **Trigger 1（Session Start）**：topic-index 不变量 9 条确认；active topic conflicts = none；depends_on（2026-06-20-problem-driven-redirection）输出已满足；profile 最近纠偏 2026-07-02 S030"急于推进"第 7 次；inflation check 本专题 4 S 文件（S001-S004）远未到阈值。
- **Trigger 5（Handoff H003 接收）**：FR-26 主线独立 grep 核查 3 条关键事实全 PASS——
  - ① B7 评点 0.6dB/1.9×/10dB PASS：S004 §步骤 1 落盘 + B7 增量笔记 `_B7-gardner-ted-increment.md` 真实存在
  - ② B5 全文核验 ±4.5GHz/<140MHz/−48dBm PASS：S004 §步骤 2 落盘 + B5 增量笔记追加段存在
  - ③ 总表 20 Q# PASS：S004 §步骤 3 B1×2+B2×2+B3×3+B4×3+B5×4+B6×3+B7×3 = 20

### 🔴 对话 2 违规自纠（用户纠偏"派一个 subagent？不是计划至少二十个？"）

**用户纠偏原话**："你接着干吧然后，你就派一个 subagent？不是计划至少二十个？"

**违规识别**：对话 2 B5 全文核验我**主线自己读了 content.md 252 行写笔记**，违反 AGENTS.md「子 agent 强制委托」第 1 条（"论文全文精读 → 子 agent 读 content.md"）。H002 写"B5 任务量小主线可直接做"本身就违规，我当时没纠正执行了，是错的。

**根因**：
1. 把"任务量小"误当"豁免委托"——AGENTS.md 第 1 条无任务量豁免条款，**论文全文精读一律子 agent**
2. "至少二十个"——整个专题 12 点每点 ≤5 篇精读，按 gw-read 强制委托每篇/每点评点都该子 agent 化，总量确实应该是几十个量级。我之前按"B 点"派（1 子 agent 评 1 点）已经偏粗，本轮 B5 更少（0 个）
3. 对话 2 只派 1 个子 agent（B7）+ 主线自读 B5 = 委托率 50%，远低于"至少二十个"预期

**本轮纠正**：B8/B9/B10 三点各派 1 子 agent（3 并发），**主线不碰任何全文**，只接收子 agent 结构化摘要 + FR-26 独立 grep 核查关键声称。本轮委托率 100%（3/3）。

### 步骤 1：B8/B9/B10 三点评点（3 子 agent 并发）

派 3 子 agent 并发（B8/B9/B10 各 1，全 PASS ≤15 分钟：B8 225s / B9 347s / B10 194s），主线 FR-26 独立 grep 核查。

#### FR-26 核查 B8/B9/B10 关键声称

| 子 agent 声称 | 主线核查结果 | 结论 |
|---|---|---|
| **B8 全文无 dB 性能数字** | python grep：B8 锚有 23 次 dB（多在参数表 L296-352：−130dBm 背景光 / 5dB MZM 损耗 / −35dBm 接收灵敏度 / 7.5dB/km 衰减）+ 64 次 BER。**无"vs baseline 改善 X dB"增益对比**（性能以 BER 表达）| **核心结论 PASS，措辞修正**：续填总表用"无 vs baseline dB 增益，性能以 BER orders of magnitude 表达"（非"全文无 dB"）|
| **B9 ~3dB/~1dB/~0.5dB @ 3/4/5 PNOB** | content.md 行 241+253 双处："~3 dB SNR gain (3-PNOB)"+"~1 dB and ~0.5 dB (4,5-PNOB)" + 行 249 "~0.8 dB long-term 含湍流" + Conclusion 重述 | **PASS**（四处一致）|
| **B10 ao.581648 全文缺仅摘要，4dB 仅作引用不溯源** | ao.581648 content.md 仅 12 行，含 abstract + "Full PDF unavailable" 声明 + abstract 明确"4 dB OSNR gain vs FFT+BPS" | **PASS**（B10 处理正确：标待全文核验不脑补）|

#### B8 评点收获（主判定"无核心 Q#" + 2 相邻/边界 Q#）

笔记：`papers/_read_notes/_B8-rl-gs-self-coherent-increment.md`（106 行）
读了：jocn.468220（B8 锚 604 行）+ photonics10050493（cited-by，wavefront distortion）+ lcomm.2024.3511129（GS 主题）+ jocn.503484（仅摘要跳过）

**B8 全称确认**：RL=Reinforcement Learning（强化学习）/ GS=Geometric Shaping（几何整形）/ SCD=Self-Canceling coherent Detection（自消除相干检测）。重庆邮电大学 Liu 等，JOCN Vol.15 No.1 Jan 2023。

**核心机制**：heterodyne 相干检测后，IF 信号经 square-law device + LPF，使频偏 w_if 与相位噪声 ϕ 在基带"自消除"（Eq.6 行 99-103），PAM4 因四幅度均正可直接从平方信号判决——**载波同步需求被绕过**（行 119 "no stringent requirements for laser linewidth"）。

| Q# | M-C-A 浓缩 | 撞 D006 | D005 够格 | 范围 |
|---|---|---|---|---|
| **主判定** | **本篇无核心 Q#**：square-law+LPF 使 CFO/相位噪声自消除（Eq.6 行 99-103），PAM4 直接判决，载波同步被整体绕过 | 否（开环前馈，无环路 TF）| 不适用（无载波同步候选）| out（地面 FSO）|
| Q1（相邻）| SCD mixing efficiency 前提失效：B8 假设 G 常数（行 193），photonics10050493 实测湍流致 η 仅 36-68%→G 波动→PAM4 判决域漂移；B8 未建模 | 否 | 不够格/待定量（B8 无 vs baseline dB gain，借 photonics 3dB mixing gain 差参考）| out（地面 FSO）|
| Q2（边界）| SCD 调制格式边界：自消除依赖"信息只调强度"（行 93），PAM4 一维成立；QAM/PSK 二维 square-law 后相位丢失失效，载波同步回归 | 否 | 不够格（适用域边界非性能改进）| out（地面 FSO）|

**关键发现**：
1. **B8 与 B1-B7 本质正交**——B1-B7 改进载波恢复，B8 用自相干架构消除载波恢复需求
2. B8 主场景地面 FSO 1km（Cn² 10⁻¹⁷~10⁻¹³），**非星地/ISL/feeder**，严格 out
3. cited-by 给 GS 维度 0.65dB shaping gain 参考（lcomm.2024 IM/DD 非相干）+ photonics 3dB mixing gain 参考

#### B9 评点收获（3 个 Q#，~3dB 与 B3-Q2 同量级）

笔记：`papers/_read_notes/_B9-virtual-carrier-dre-increment.md`（115 行）
读了：jlt.2023.3270673（B9 锚 306 行）+ apn.3.3.036007（用户新下 DRE Gold OA 440 行）+ lpt.2026.3655104（cited-by）+ s24248036（survey 泛指）

**DRE 全称确认**：**Digital Resolution Enhancer（数字分辨率增强器）**——TX 侧动态量化（DQ）+ block-wise Viterbi 求 MSQE(qeff) 最小，把量化噪声从带内挤到带外。虚拟载波 = 数字域 DSP 插入的 carrier tone（非光 CW / 非 RF / 非训练序列），满足 square-law 后最小相位条件→DC-Value/KK 相位重建前提。

**核心机制**：B9 自相干架构**用架构"绕开"传统载波同步链**——虚拟载波同源数字域→无独立 LO→无 OPLL/Costas/V-V 需求；载波相位靠 RX-DSP DC-Value 后处理重建。DRE 是 TX 侧量化噪声整形，**与载波同步正交**。

| Q# | M-C-A 浓缩 | 撞 D006 | D005 够格 | 范围 |
|---|---|---|---|---|
| **Q1（核心）** | DRE 量化噪声整形迁移到自相干 FSO 深湍流链：B9 仅地面 42m clear weather 验证；湍流致 CSPR/h(l) 时变→DRE 失效？需联合 CSPR 自适应+湍流 h(l) 在线估计；~3dB @ 3PNOB（行 241/253）| 否（TX 预处理，不涉环路 TF）| **够格（量级达标）**——~3dB 与 B3-Q2 +2~3dB 同量级，但 baseline 是"w/o DRE 内部对照"非"赢传统相干载波同步 baseline"，需注明 | in 倾向（地面 FSO）→待迁移（星地深湍流）|
| Q2 | 虚拟载波自相干"绕开"载波同步的湍流稳健性：CSPR≥P_signal,max 稳定是 DC-Value 相位重建前提；深湍流致 CSPR 失稳→相位重建失败？自相干 vs 传统 OPLL 深湍流对照待补 | 否（自相干无 OPLL 环路）| 待定量锚（B9 未给 vs 传统 OPLL 的 dB 对比）| in 倾向→待迁移 |
| Q3 | DRE 与载波同步正交性的反向利用：DRE u(n) 优先保护 carrier tone 相位→提升 CCF/DC-Value 稳健性；若目标函数纳入 RX 载波相位环路 H(z) 则撞 D006 | **边界**（TX 预处理不撞；纳入环路 H(z) 则撞，只标不砍）| 不够格（机制探索无 dB 锚）| in |

**关键发现**：~3dB/~1dB/~0.5dB SNR @ 3/4/5 PNOB（行 241+253）+ ~0.8dB 长期测量含湍流（行 249）。范围——B9 主场景地面 42m FSO，apn 是 O-band IM/DD 数据中心 out。

#### B10 评点收获（3 个 Q#，ao.581648 全文缺）

笔记：`papers/_read_notes/_B10-16qam-pilot-rls-increment.md`（101 行）
读了：s11107-024-01019-2（B10 锚 318 行）+ ao.581648（仅摘要 12 行，全文缺）

**核心机制**：导频驱动 RLS 把 CFO+PN 塞进同一个线性回归（h1,k→2πΔfTs 学频率，h0,k 学相位偏置），128 pilot 训练后切 decision-directed 反馈环，单 DSP 模块联合估计替代 BPS+4OPM 两段式。高 CFO(10GHz)/高线宽(1.45MHz) 鲁棒，复杂度 20RM+12RA/symbol。

| Q# | M-C-A 浓缩 | 撞 D006 | D005 够格 | 范围 |
|---|---|---|---|---|
| **Q1（核心）** | Pilot-RLS 联合 CFO+PN（h1→CFO/h0→PN，导频+decision-directed 反馈环）：BPS+4OPM 高 CFO/高线宽失效区 RLS 保 FEC limit，10GHz CFO/1.45MHz 线宽，复杂度 20RM+12RA/symbol | 否（DSP 自适应滤波，非 OPLL 环路 TF）| 边际够格（无统一 X dB gain，优势在范围/鲁棒性，迁移星地定量待评）| out（光纤原文）/待迁移星地（in 候选）|
| Q2 | Pilot-RLS 湍流鲁棒性：B10 仅 Kerr 非线性相位噪声验证，Ps 衰落致硬判错→反馈环发散？RLS 状态方程纳入湍流+多普勒联合建模则撞 D006 | **边界**（前馈归一化不撞；RLS 状态方程联合建模则撞，只标不砍）| 待定量锚（open problem，原文无湍流 dB）| in（星地 COSC 湍流）——候选维度，原文未涉 |
| Q3 | KRLS+ZA-BPS PS-64QAM（ao.581648）：FFT+BPS 高 shaping factor 失效，KRLS 非线性升级 pilot-RLS，摘要称 4dB OSNR gain + 8000km——**全文缺待核验** | 否（待全文核验）| 待全文核验（摘要 4dB，无法溯源行号）| out（光纤）/待迁移 |

**关键发现**：D011 种子"16-QAM CPR 扩展"经 B10 落地，ao.581648 承接至 PS-64QAM（同作者团队 Deka/Krishnamurthy）。B10+ao.581648 均光纤 out，未涉湍流/星地，机制迁移星地为 Q# 维度。baseline 是 BPS+4OPM（DSP 数字法），与 B6 OPLL/B4 PADE 正交。

### 步骤 2：B1-B10 总表续填（续 S004，加 B8/B9/B10 共 +6 Q#）

**🔴 本表守 D018 中性提取——只标三维不判 Go/Kill。**

汇总 B1-B10 十点共 **26 个 Q# 候选**（B1-B7 原 20 + B8 主判定+2 + B9×3 + B10×3 = 26）：

#### B1-B10 总表（26 个 Q# 候选，B8/B9/B10 新增标 🔵）

| B 点 | Q# | M-C-A 浓缩 | 撞 D006 | D005 够格 | 范围 | 关键 dB/量级 |
|------|-----|-----------|--------|----------|------|------------|
| **B1 pilot 窗口** | B1-Q1 | 自适应 window N（sat.1553 固定 + [60] N∝SNR；强湍 SNR 波动）| 不撞 | 倾向够格但有风险 | in | +1dB（pilot vs VV+diff）|
| | B1-Q2 | 自适应 pilot rate | 不撞 | 风险偏高（自承负面证据）| in | 0.5dB 阈值 |
| **B2 deep fade 冻结** | B2-Q1 | FOE freeze 自适应阈值 | 不撞 | ≥1dB 存疑待全文 | in | 0.6dB（[79] vs 无 freeze 非增量）|
| | B2-Q2 | freeze + pilot 双模切换 | 不撞 | 倾向够格增量未量化 | in | +1dB（pilot 在 fade）|
| **B3 子系统协同** | B3-Q1 | LCOMM B3 视角（一套 FPT 跨三子模块）| 不撞 | 够格（+0.9dB）| **out（光纤 DSCM）** | +0.9dB Q |
| | B3-Q2 | jphot+oe 合并（一套 TS 多 FOE+MRC）| 不撞 | 够格（+2~3dB）| in | +2~3 dB |
| | B3-Q3 | sat.1553 L790 跨子系统（open problem 级）| 边界 | 待定量锚 | in | 借 +0.9~3 dB |
| **B4 双反馈环** | B4-Q1 | optcom.2023 双反馈环本体 | 不撞（边界）| 部分 | in | ±920 MHz @ 0.5 dB / MSE 4× |
| | B4-Q2 | jlt.2023 PCS+符号率自适应 | 不撞 | 够格（维度错位）| in | +70~100 Gbps |
| | B4-Q3 | sat.1553 feedback open problem | 不撞 | 待定量锚 | in（含 ISL 边界）| 无直接实例 |
| **B5 短时谱粗频偏** | B5-Q1 | B5 本体短时谱粗 CFO（全文核验升级）| 否（前馈功率比+星历，全文无湍流）| **不够格（dB 维度）/ 结构性优势（范围维度）** | **in（星地 LEO 下行确证）** | ±4.5GHz / 残频 <140MHz / −48dBm@BER 1e-3 |
| | B5-Q2 | [60] Leven Mth-power 理论锚 | 不撞 | 够格 | **out（光纤 intradyne）** | OSNR <9dB 与频偏无关 / 7dB penalty |
| | B5-Q3 | sat.1553 L558 粗 CFO 精度边界 | 不撞 | 待定量锚 | in | 残频 10⁻³fs |
| | B5-Q4 | jlt.2023 频谱扫描 Doppler 视角参考 | 不撞 | 够格（维度错位）| in（视角参考）| +70~100 Gbps |
| **B6 Z-ODPLL** | B6-Q1 | atan2 鉴相器 KD 与 Ps 解耦 | 不撞 | 边际够格（定性保锁非几 dB）| in | σ=2.6°/0.42dB / 容 30ns |
| | B6-Q2 | Z-ODPLL H(z) 建模 | **边界（只标不砍）** | 不够格（工具）| N/A | — |
| | B6-Q3 | sin 鉴相器幅度衰落跨论文空白 | 不撞 | 待定量锚 | in | 无 |
| **B7 Gardner TED** | B7-Q1 | Gardner TED 复用 FOE | 否 | 边际够格（0.6dB+1.9×范围/10dB）| in | 0.6dB @ BER 2e-2 / 1.9× 范围（0–23GHz）|
| | B7-Q2 | TED 增益↔Doppler 映射湍流鲁棒性 | **边界（只标不砍）** | 待定量锚 | in | 借 0.42~0.66dB |
| | B7-Q3 | 双候选判决强噪声可靠性 | 否 | 不够格 | in | 无 |
| **🔵 B8 RL+GS 自相干** | 🔵 **B8 主判定** | **本篇无核心 Q#**：square-law+LPF 自消除 CFO/相位噪声，PAM4 直接判决，载波同步被绕过 | 否（开环前馈）| **不适用**（无载波同步候选）| **out（地面 FSO）** | 无 vs baseline dB gain（性能以 BER orders of magnitude）|
| | 🔵 B8-Q1 | SCD mixing efficiency 前提失效（湍流致 G 波动，相邻候选）| 否 | 不够格/待定量（借 photonics 3dB mixing gain 差参考）| out（地面 FSO）| 无 B8 dB |
| | 🔵 B8-Q2 | SCD 调制格式边界（PAM4 一维 vs QAM 二维失效）| 否 | 不够格（适用域边界非性能改进）| out（地面 FSO）| 无 |
| **🔵 B9 虚拟载波自相干+DRE** | 🔵 **B9-Q1（核心）** | DRE 量化噪声整形迁移自相干 FSO 深湍流（B9 仅地面 42m 验证；~3dB @ 3PNOB）| 否（TX 预处理）| **够格（量级达标）**——~3dB 与 B3-Q2 同量级，但 baseline 是内部 w/o DRE 对照非传统相干载波同步 | in 倾向（地面 FSO）→待迁移（星地深湍流）| **~3dB** @ 3PNOB（行 241/253）+ ~1dB/0.5dB（4/5 PNOB）+ 0.8dB 长期含湍流 |
| | 🔵 B9-Q2 | 虚拟载波自相干"绕开"载波同步的湍流稳健性 | 否（自相干无 OPLL）| 待定量锚（未给 vs 传统 OPLL dB）| in 倾向→待迁移 | 无 |
| | 🔵 B9-Q3 | DRE 与载波同步正交性的反向利用 | **边界**（TX 预处理不撞；纳入环路 H(z) 则撞，只标不砍）| 不够格 | in | 无 |
| **🔵 B10 16-QAM pilot-RLS** | 🔵 **B10-Q1（核心）** | Pilot-RLS 联合 CFO+PN（h1→CFO/h0→PN，导频+decision-directed），替代 BPS+4OPM；高 CFO(10GHz)/高线宽(1.45MHz) 鲁棒 | 否（DSP 自适应滤波非 OPLL 环路 TF）| 边际够格（无统一 X dB gain，优势在范围/鲁棒性）| **out（光纤原文）/待迁移星地（in 候选）** | 复杂度 20RM+12RA/symbol |
| | 🔵 B10-Q2 | Pilot-RLS 湍流鲁棒性（Ps 衰落致硬判错→反馈环发散？）| **边界**（前馈归一化不撞；RLS 状态方程联合建模则撞，只标不砍）| 待定量锚（原文无湍流 dB）| in（星地 COSC 湍流）——候选维度 | 无 |
| | 🔵 B10-Q3 | KRLS+ZA-BPS PS-64QAM（ao.581648，D011 种子延伸）| 否（待全文核验）| **待全文核验**（摘要 4dB 无法溯源行号）| out（光纤）/待迁移 | 4dB OSNR gain（摘要，待全文核验）|

#### 总表统计更新（B1-B10 共 26 Q#）

| 维度 | 计数 | Q# 编号 |
|------|------|---------|
| **总 Q# 数** | **26** | B1-B7 原 20 + B8 主判定+2 + B9×3 + B10×3 |
| **撞 D006 明确撞** | **0** | （sat.1553 L70 旧扩展归档不计）|
| **撞 D006 边界（只标不砍）** | **5** | B3-Q3 / B6-Q2 / B7-Q2 / **🔵 B9-Q3** / **🔵 B10-Q2** |
| **D005 倾向够格** | **9** | B1-Q1 / B2-Q2 / B3-Q1 / B3-Q2 / B4-Q2 / B5-Q2 / B5-Q4 / B6-Q1 + **🔵 B9-Q1** |
| **D005 边际够格** | **3** | B7-Q1 / B5-Q1 + **🔵 B10-Q1** |
| **D005 待定量锚** | **6** | B2-Q1 / B3-Q3 / B4-Q1（部分）/ B4-Q3 / B5-Q3 / B6-Q3 / B7-Q2 + **🔵 B9-Q2 / B10-Q2** |
| **D005 风险偏高/不够格/待全文** | **6** | B1-Q2 / B5-Q1 dB 维度 / B6-Q2 / B7-Q3 + **🔵 B8 主判定不适用 / B8-Q1 / B8-Q2 / B9-Q3 / B10-Q3 待全文** |
| **范围 out** | **7** | B3-Q1（光纤 DSCM）/ B5-Q2（光纤 intradyne）/ B6-Q2（N/A）+ **🔵 B8 主判定/Q1/Q2（地面 FSO）/ B10-Q1（光纤）/ B10-Q3（光纤）** |
| **范围 in / in 倾向** | **18** | 其余（含 in 倾向待迁移 B9-Q1/Q2 + B10-Q1 候选维度）|

#### D005 够格梯度更新（中性，不判 Go/Kill）

**第一梯队（有明确 dB 增益 + 范围 in/in 倾向）**：
- **B3-Q2**（+2~3 dB 强湍 4 支路）—— dB 最高 in
- **🔵 B9-Q1**（~3dB @ 3 PNOB DRE）—— **dB 与 B3-Q2 同量级**，但 baseline 是内部 w/o DRE 对照非传统相干载波同步，in 倾向待迁移星地深湍流
- B3-Q1（+0.9 dB Q）—— **范围 out（光纤 DSCM）**
- B1-Q1 / B2-Q2（+1dB）—— in
- B5-Q2（7dB penalty）—— **范围 out（光纤 intradyne）**

**第二梯队（结构性优势，dB 偏小或维度错位）**：
- B7-Q1（0.6dB + 1.9× 范围 / OSNR 10dB）—— in
- B4-Q2 / B5-Q4（+70~100 Gbps 吞吐维度错位）—— in
- **🔵 B10-Q1**（无统一 dB gain，优势在范围/鲁棒性 BPS+4OPM 失效区）—— **out 光纤 / 待迁移星地 in 候选**
- B5-Q1（±4.5GHz 覆盖 LEO Doppler）—— in
- B6-Q1（定性保锁 σ=2.6°/0.42dB + 30ns）—— in

**第三梯队（待定量锚 / open problem 级 / 待全文）**：
- B2-Q1 / B3-Q3 / B4-Q1 / B4-Q3 / B5-Q3 / B6-Q3 / B7-Q2 + **🔵 B9-Q2 / B10-Q2** + **🔵 B10-Q3 待全文（摘要 4dB）**

**第四梯队（风险偏高/不够格/不适用）**：
- B1-Q2 / B6-Q2 / B7-Q3 + **🔵 B8 主判定（无核心 Q# 自相干绕过载波同步）/ B8-Q1 / B8-Q2 / B9-Q3**

#### 关键观察更新（中性，辅助排优先级）

7. **🔵 B8 是"载波同步冗余"特例**——自相干自消除使载波同步被整体绕过（B1-B7+B9-B10 都在改进载波恢复，B8 用架构消除需求）。范围 out（地面 FSO）。这提示"自相干架构替代传统载波同步链"是另一条潜在路线（B9 也走这条路 Q2），但 B8/B9 主场景都非星地。
8. **🔵 B9-Q1 ~3dB 跻身第一梯队**——与 B3-Q2 +2~3dB 同量级，但 baseline 是"w/o DRE 内部对照"非"赢传统相干载波同步 baseline"，D005 标尺下需注明；范围 in 倾向待迁移星地深湍流。
9. **🔵 D006 边界模式扩展到 5 个**（B3-Q3/B6-Q2/B7-Q2/B9-Q3/B10-Q2）——"前馈/工具层不撞，环路 TF 联合建模则撞"模式在 B 档 12 点中重复出现 5 次，是潜在一致性研究方向（湍流相位建模边界）。
10. **🔵 B10 + ao.581648 是 D011 种子"16-QAM CPR 扩展"的落地+延伸**——B10（16-QAM pilot-RLS）+ ao.581648（PS-64QAM KRLS 承接），同作者团队，pilot-RLS→KRLS 是核方法非线性升级。但两者都光纤 out，迁移星地是 Q# 维度。
11. **范围 out 比例上升**（3→7/26 ≈ 27%）——B8（3 个地面 FSO）+ B10（2 个光纤）新增 5 个 out。星地 in/in 倾向仍是主体（18/26 ≈ 69%）。

### 步骤 3：B11/B12 预登记（用户新下 B12 MAP 全文）

**🔴 用户新下 `papers/doi/10.23919_oecc-psc62146.2025.11109607/`（B12 MAP Phase Recovery 256-QAM，150 行，2026-07-04 到位）**——原 IEEE 订阅墙已解决。

预登记（详细评点交对话 4）：
- **B11 NDA-ML STO+CPE**：锚 LPT.2024.3523478（226 行）+ cited-by 1 篇 s25164906（边缘）—— 锚极新 cited-by 仅 1，B11 评点靠锚全文 + M-APSK/NDA ML 经典
- **B12 频域 pilot**：锚 TCOMM.2022.3171809（590 行）+ cited-by 3 篇 + **B12 MAP 全文 150 行用户新下**（OECC/PSC 2025，MAP Phase Recovery 256-QAM）

## 决策引用

- **无新建 D###**（评点 + 续填总表，Q# 留总表阶段用户排优先级后判 Go/Kill，符合 D018 中性提取）
- 引用既有：D017 / D018 / D006（5 边界只标不砍）/ D005

## 范围确认

- 本轮是否在 scope boundary 内：**是**（B8/B9/B10 评点 + 续填总表都是 S001 v2"对话 3"动作；Q# 只提取不判 Go/Kill）
- **守 3 步上限**：本轮 3 步（①报到+违规自纠 ②B8/B9/B10 三点并发评点+grep 核查 ③续填总表+B11/B12 预登记+写 S005/H004）
- 守子 agent ≤15 分钟：3 子 agent（B8 225s / B9 347s / B10 194s），全 PASS
- **守 D018 中性提取**：B8/B9/B10 新增 6 Q#（含 B8 主判定"无核心 Q#"）+ 总表 26 Q# 全标三维，不判 Go/Kill
- **🔴 委托纠正**：本轮 B8/B9/B10 三点各 1 子 agent，主线不碰全文，委托率 100%（纠正对话 2 B5 主线自读违规）

## 后续

### 交对话 4（B11/B12 评点 + literature_notes 载波同步 v2 章节并入）

**对话 4 必读**：
1. 本 S005（B8/B9/B10 评点 + **B1-B10 总表 26 Q#**）
2. S004（B1-B7 总表 20 Q# + B7/B5 详评）+ S003（B1-B6 17 Q#）
3. topic-index 不变量 9 条 + S001 v2 规划
4. H004（本轮 handoff，下一步具体任务）
5. gw-read.md（14 字段+7 项）+ **templates.md literature_notes 模板（综合分析+研究问题清单格式）**
6. 原专题 H020（总表 + 排优先级辅助信息）

**对话 4 任务**（B11/B12 评点 + literature_notes 并入）：
- **B11 NDA-ML STO+CPE**：派子 agent 读 LPT.2024.3523478（226 行）+ cited-by，写 B11 增量笔记
- **B12 频域 pilot**：派子 agent 读 TCOMM.2022.3171809（590 行）+ cited-by + **B12 MAP 全文 150 行**（用户新下），写 B12 增量笔记
- **literature_notes 载波同步 v2 章节并入**：全 12 篇笔记完成后，按 gw-read 综合分析模板（方法分类/已知局限/Q# 候选/baseline 对称性）写综合分析 + 研究问题清单
- **B1-B12 全 12 点总表合并**（B1-B10 26 Q# + B11/B12 待评）交用户最终排优先级

### 关键提醒给对话 4

1. **B1-B10 总表已落盘**（本 S005 §步骤 2）：对话 4 评完 B11/B12 后合并全 12 点最终总表
2. **B11/B12 全文到位**：B11 锚 LPT.2024.3523478（226 行）+ B12 锚 TCOMM.2022.3171809（590 行）+ **B12 MAP oecc-psc62146 全文 150 行用户新下**
3. **ao.581648 仍缺**（B10-Q3 待全文核验）：B10-Q3 4dB OSNR gain 仅摘要，对话 4 如用户继续尝试手动下可补
4. **D006 边界模式 5 次**（B3-Q3/B6-Q2/B7-Q2/B9-Q3/B10-Q2）：对话 4 literature_notes 并入时这是潜在一致性研究方向（湍流相位建模边界）
5. **委托纪律**：对话 4 B11/B12 评点继续各派子 agent，主线不碰全文
6. **B8 特例**：B8 主判定"无核心 Q#"（自相干绕过载波同步），literature_notes 并入时 B8 单独标"载波同步冗余路线"
7. **dB 量级参考**：第一梯队 B3-Q2/B9-Q1 +2~3dB；B1/B2 +1dB；B7 0.6dB+范围；B10 无统一 dB（范围鲁棒性）
