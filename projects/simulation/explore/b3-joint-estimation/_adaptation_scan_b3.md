# B3-Q2 适配扫描（adaptation-scan A1-A6，sandbox 前必扫）

> 来源: B3-Q2 对话 2（S003 续）| 日期: 2026-07-08
> 触发: 用户"有思路都可以试试" + S013 教训（NDA-ML 适配扫描 A1/A3 FAIL / A4 PASS，锁死单方法内部找增量全 FAIL，条件切换才出信号）
> 规则: `.claude/skills/sim-preflight/rules/adaptation-scan.md`
> 目的: 进 sandbox 前把所有可能的增量思路穷举出来，不只锁"B3-Q2 全条件赢 jphot FSTS"一条

---

## 为什么要扫（S013 教训）

当前 0.4 框架的 Go 判据 = `gain_vs_M2 > 0`（B3-Q2 全条件赢 jphot FSTS）。但：
- 0.1b CRB 推导显示 **CPE 联合全条件增益 ≈ 0dB**（等导频长度下 CRB 恒等）
- Doppler 维度无锚（jphot 缓变假设下"无害但也可能无益"）

→ **全条件赢判据可能过严**，会把"有优势区间但非全条件赢"的真信号误杀。

S013 的教训：NDA-ML 锁死"全条件赢"跑 9 个对话全堵死，最后是 A4 条件切换（crossover 区赢）才出信号。**B3-Q2 应该先扫一遍找所有可能的优势区间，不全押全条件赢。**

---

## 扫描对象

| 角色 | 方法 |
|---|---|
| 我们的方法 | M3 = B3-Q2 联合（FSTS + 两段式 FOE + CPE 联合复用 + Doppler 斜率前馈）|
| 主 baseline | M2 = jphot FSTS（FSTS + 两段式 FOE + 独立 CPE + DD-LMS，jphot-L243）|
| 弱 baseline | M1 = 传统分立 TS 管线 |
| 参照 | common fft_foe / vv_cpr / bps_cpr / da_ml（单支路估计器）|

---

## A1. 参数适配（方法关键参数随条件变最优？）

**扫描对象**：jphot FSTS 的 BL（块长）+ B3-Q2 Doppler 回归窗长

**信号线索（原文已给）**：
- jphot-L299 Fig.10："BL 增大估计精度先升后降，受调制格式、接收功率、TS 总长影响"。4-QAM/320sym 选 BL=20，16-QAM/320sym 选 BL=40
- jphot-L267 Fig.7：TS 长度 48→320 改善 3.47dB，320→800 只改善 0.48dB（边际递减）
- **BL 的二阶 FOE 估计范围被 BL 缩小**（jphot-L203："estimation range is reduced by BL times"）——BL 大=精度高但范围窄，BL 小=范围宽但精度低，这是天然 tradeoff

**信号判据候选**：BL 最优值是否随**湍流强度 / Doppler 动态强度**变？
- 低 SNR（强湍 deep fade）→ BL 小（保范围）还是 BL 大（保精度去噪）？jphot-L309 暗示低功率下 jphot 退化
- 高 Doppler → 块间频偏跳变大 → BL 需小（块内更接近常数）

**创新形态**：自适应 BL（按 per-block SNR / scintillation CV / Doppler 残余动态切换）+ Doppler 回归窗长自适应

**baseline**：固定 BL（jphot 的 BL=20/40）

**失败信号**：BL 全条件最优值固定 → 无自适应空间（像 NDA K=16 普适那样）

**⚠️ 风险**：S013 A1 FAIL 的根因是"K=16 普适"。B3-Q2 的 BL 是否也普适需 sandbox 验证——但 jphot 自己都说"BL 受多因素影响"，比 NDA-K 有更强的自适应线索。**中等可能性出信号。**

---

## A2. 结构适配（原场景结构假设在新场景不成立？）

**扫描对象**：jphot 从地面 FSO → 星地 LEO 场景，哪些结构假设失效

**信号线索（强，已确认）**：
- jphot-L208 "frequency offset **drifts slowly** in practice"（缓变假设）——LEO Doppler 时变直接破坏
- jphot-L160 "slow-varying quantities relative to the symbol rate"（湍流相位缓变）——星地强湍 deep fade 相位跳变破坏
- jphot 的 TS 结构是**块内常数频偏**假设（两段式估 Δf₁ + Δf₂），星地 LEO 块间频偏有真实斜率（f_dot），块内常数假设退化

**信号判据**：✅ **强信号**——jphot 自己承认的两个缓变假设在星地 LEO 都不成立

**创新形态**：
- Doppler 维度：加块间 Δf̂_k 序列线性回归 → f_dot 前向补偿（0.3 架构，前馈开环不撞 D006）
- 相位跳变鲁棒性：CPE 窗口在 deep fade 期间的行为（jphot DD-LMS 在 deep fade 会跟踪噪声？）

**baseline**：原 jphot 结构（块内常数频偏假设，搬星地不做调整）

**失败信号**：星地 Doppler 时变在块内（BL=20 符号 = 2ns@10GBaud）可忽略 → 结构假设仍成立 → 无调整空间

**判定**：✅ **已确认为 B3-Q2 主切口之一**（0.2 A1 归属 + 0.3 架构）。这是 A2 信号，B3-Q2 已经在用了。A2 扫描确认 B3-Q2 的 Doppler 维度是结构适配增量，不是凭空造的。

---

## A3. 组合适配（不同族方法能否组合互补？）

**扫描对象**：jphot FSTS（前馈块估计）+ 某闭环跟踪方法（DPLL/KF）

**信号线索（S013 反面教训，但 B3-Q2 场景不同）**：
- S013 NDA+DPLL 混合 FAIL（两方法强项重叠冗余）——但那是 AWGN/弱湍，σ²_p 极小
- B3-Q2 场景不同：星地强湍 deep fade + LEO Doppler 大动态。前馈块估计在 deep fade 期间会中断（低 SNR 估不准），闭环跟踪有记忆能跨 fade —— **这里可能有 S013 没有的互补性**

**⚠️ D006 红线**：组合进 PLL 环路 TF 联合建模 = 撞 D006。只能做"前馈块估计 + 前馈 Doppler 回归"组合，不能进环路

**信号判据**：deep fade 期间前馈块估计中断 + Doppler 大动态下块间斜率预测漂移 → 前馈组合能否互补？
- 候选组合 A：FSTS 两段式 FOE（块内）+ Doppler 斜率回归（块间）—— 这是 B3-Q2 当前 M3，已经是组合
- 候选组合 B：FSTS + 短时记忆滤波（deep fade 跨断用前一好块的估计外推）—— **新思路，但可能撞 D006 边界（记忆滤波若是 IIR 接近环路）**

**baseline**：单 FSTS（不组合 Doppler 回归）

**失败信号**：deep fade 期间前馈估计中断后，Doppler 回归也吃不到信号 → 两者强项重叠或都失效

**判定**：🟡 **中等**。组合 A 已是 M3 核心。组合 B（跨 fade 记忆外推）是新思路但 D006 边界风险高，暂列观察，不优先。

---

## A4. 条件适配（不同条件下方法间优势是否切换？）⭐ 主信号候选

**扫描对象**：B3-Q2（M3）vs jphot FSTS（M2）在不同条件下的优势关系

**信号线索（强，物理因果清晰）**：
- jphot-L208 自承"drifts slowly"假设 → **低 Doppler 条件下假设成立，jphot 够用；高 Doppler 条件下假设失效，B3-Q2 Doppler 维度发力**
- jphot-L309 "proposed algorithm may exhibit lower estimation accuracy when received optical power is low" → **低 SNR 条件下 jphot FSTS 退化，B3-Q2 联合 CPE（复用 FOE 中间量作先验）可能更稳**

**信号判据候选（两条 crossover 轴）**：

| crossover 轴 | 低端条件 | 高端条件 | 物理因果 |
|---|---|---|---|
| **Doppler 动态强度（f_dot）** | jphot 赢/持平（缓变假设成立，B3-Q2 Doppler 回归过拟合）| **B3-Q2 赢**（缓变假设失效，Doppler 斜率补偿产生真增益）| jphot-L208 自承假设 |
| **per-block 有效 SNR** | jphot FSTS 退化（L309），**B3-Q2 联合 CPE 可能赢**（FOE 共轭积先验帮 CPE）| 持平/微差（高 SNR 两种 CPE 都够）| jphot-L309 低功率退化 |

**创新形态**：基于 Doppler 残余动态检测的"B3-Q2 联合 vs jphot 分立"切换策略（高动态用联合，低动态用 jphot）

**baseline**：单一策略全条件（jphot FSTS 固定）

**失败信号**：全 Doppler 区间 B3-Q2 持平或输 jphot → 无 crossover

**判定**：⭐ **主信号候选**。这是 S013 A4 思路迁移到 B3-Q2 的核心。物理因果强（jphot 自承假设），crossover 轴明确（Doppler 动态强度）。

**🔴 与 NDA-ML A4 的差异化（防换皮）**：
- NDA-ML A4 crossover 轴 = per-block 有效 SNR（衰落深度，随机量，DA/NDA 按 pilot 可靠性切换）
- B3-Q2 A4 crossover 轴 = **Doppler 动态强度**（轨道运动时变速率，确定性量，联合/分立按频偏模型阶数切换）
- 两者物理量正交，crossover 机制不同（pilot 可靠性 vs 频偏模型阶数）—— 不算换皮
- **叙事必须显式区分**：NDA-ML 卖"SNR 驱动的 DA/NDA 切换"，B3-Q2 卖"动态强度驱动的联合/分立切换"

---

## A5. 评价维度适配（换评价维度，持平的方法是否分化？）

**扫描对象**：M2 vs M3 在 BER 之外的维度（outage / BER 方差 / 工作区范围）

**信号线索（弱-中）**：
- BER 均值持平 ≠ outage 概率持平。高 Doppler 下 B3-Q2 可能 BER 均值跟 jphot 持平，但 **outage 概率（P(BER>HD-FEC)）更低**（Doppler 斜率补偿减少大块突发错）
- per-block BER 方差：jphot 块间频偏跳变导致块间 BER 波动大，B3-Q2 斜率补偿后块间更平稳

**信号判据**：M2/M3 BER 均值持平时，outage 概率 / per-block BER 方差分化

**创新形态**：新评价维度下的优势论证（"高 Doppler 下联合估计的 outage 概率优势"）

**baseline**：同方法只换评价维度

**失败信号**：新维度也持平

**判定**：🟡 **弱-中等**。作为 A4 的补充——如果 A4 crossover 在 BER 均值上不明显，A5 outage 维度可能放大差异。**不优先单独跑，作为 A4 sandbox 的附加分析。**

---

## A6. 失效边界（各方法失效边界是否不同？）

**扫描对象**：M2（jphot FSTS）vs M3（B3-Q2 联合）的失效条件

**信号线索（强，物理因果清晰）**：
- jphot FSTS 失效边界：① 低 SNR（L309 低功率退化）② 高 Doppler（L208 缓变假设失效，块间频偏跳变累积成 CPE 窗口内线性漂移）
- B3-Q2 联合失效边界：① Doppler 斜率非线性的极端轨道段（前馈线性回归过拟合）② deep fade 期间前馈估计中断 + 斜率外推误差累积

**信号判据**：M2 在高 Doppler 失效，M3 在极端非线性 Doppler 失效 → **失效边界不同**

**创新形态**：失效边界分析 + 适用范围界定（"B3-Q2 联合估计在高动态星地下扩展了 jphot FSTS 的适用边界"）

**baseline**：各方法失效点对比

**失败信号**：失效边界相同

**判定**：✅ **强**。跟 A4 互补——A4 找 crossover（谁赢），A6 找失效边界（谁先崩）。**高 Doppler 是 jphot 的失效区**，B3-Q2 在这里不只是赢，是 jphot 直接崩。这比 A4 的"crossover"叙事更强（"失效边界扩展"比"条件切换"更好讲故事）。

---

## 扫描总结

| 维度 | 信号强度 | 物理因果 | 优先级 | 备注 |
|---|---|---|---|---|
| A1 参数适配（BL 自适应）| 中 | jphot 自承 BL 受多因素影响 | 🟡 次要 | S013 A1 FAIL 教训在，先验不高 |
| **A2 结构适配（Doppler 维度）** | **强** | jphot-L208 自承缓变假设 | ✅ **已用**（M3 核心）| 确认 B3-Q2 主切口合法性 |
| A3 组合适配（FSTS+跟踪）| 中 | S013 反面教训，B3-Q2 场景不同 | 🟡 观察 | 组合 B 跨 fade 记忆撞 D006 风险 |
| **A4 条件适配（Doppler crossover）** | **强** | jphot-L208 自承假设 | ⭐ **主信号** | 降级保底：全条件赢不了就找 crossover |
| A5 评价维度（outage）| 弱-中 | BER 均值 ≠ outage | 🟡 补充 | 作为 A4 sandbox 附加分析 |
| **A6 失效边界（高 Doppler）** | **强** | jphot-L208/L309 失效 | ✅ **强** | 跟 A4 互补，叙事比 crossover 更强 |

---

## 对 0.4 框架的修正建议（补进 `_fair_comparison_framework.md`）

**当前 Go 判据**：`gain_vs_M2 > 0`（全条件）→ 熔断 gain_vs_M2 ≤ 0 转 Kill

**修正为分层判据**（守 S013 教训 + A4/A6 信号）：

1. **第一层（全条件）**：sandbox 先跑全条件，gain_vs_M2 > 0 且 CPE/Doppler 贡献 ≥10% → **Go（强）**，进正式实验
2. **第二层（crossover 降级保底，A4）**：若第一层 FAIL（gain_vs_M2 ≤ 0 或接近 0），**不直接 Kill**，扫 Doppler 动态强度维度找 M2/M3 crossover。若存在高 Doppler 区 gain_vs_M2 > 0 且物理因果清晰（jphot 缓变假设失效）→ **Go（条件特长场景）**，卖点降级为"高动态条件下联合估计特长"
3. **第三层（失效边界，A6）**：若 crossover 也不明显，查 jphot 在高 Doppler 是否直接失效（BER 爆 / 估计发散）。若 jphot 失效而 B3-Q2 仍工作 → **Go（失效边界扩展）**，卖点为"扩展 jphot FSTS 的适用范围"
4. **Kill**：三层全 FAIL（全条件持平 + 无 crossover + 失效边界相同）→ 真 Kill

**这个分层判据把"全条件赢"从严判降级为第一层**，给 B3-Q2 在 A4/A6 出信号时留活路，且符合 D005 务实路线 + 导师"特长场景"标准（特长 = 高 Doppler 动态）。

---

## 方法局限（诚实标注）

1. **A1/A3 的失败先验高**：S013 NDA-ML 的 A1（参数自适应）A3（组合）全 FAIL，B3-Q2 虽场景不同但同属"单方法内部找增量"模式，不能高估
2. **A4 crossover 可能不存在**：jphot 缓变假设虽然在 LEO Doppler 下名义失效，但块内（BL=20 符号 = 2ns）频偏变化可能仍可忽略——需 sandbox 实测 f_dot 量级后确认块内假设是否真退化
3. **A6 失效边界扩展的"论文价值"**：扩展适用边界到 jphot 失效区，dB 可能很大（因为 jphot 爆了），但这个 dB 是"从崩到工作"不是"从工作到更好"，审稿人可能质疑——需 framing 为"鲁棒性"不是"增益"
4. **跟 NDA-ML A4 的换皮风险**：两个专题都走条件切换会有叙事撞车，必须用物理量正交（SNR vs Doppler 动态）显式区分

## 待 sandbox 验证的关键问题

1. **块内频偏变化量级**：f_dot × T_block（T_block = BL×Ts = 20×0.1ns = 2ns）的相位累积，是否真打破 jphot 块内常数假设？需 f_dot 精确值（0.5 债务）
2. **Doppler crossover 点**：M2/M3 BER 曲线在 f_dot 轴哪个值交叉？需 sandbox 扫 f_dot
3. **低 SNR 区 jphot 退化程度**：jphot-L309 说低功率退化，退化多少 dB？B3-Q2 联合 CPE 能补多少？
4. **outage 概率差异**（A5）：高 Doppler 下 M2/M3 outage 概率差多少？
