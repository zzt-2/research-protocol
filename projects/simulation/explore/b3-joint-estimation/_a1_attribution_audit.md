# 阶段 0.2 A1 归属核查（jphot+oe BUPT 课题组 claim 边界 + B3-Q2 增量）

> 来源: B3-Q2 S002 阶段 0.2 | 日期: 2026-07-08
> 门控对象: INVARIANT 12（A1 归属前置）+ 阶段 0.1 升级风险（增益归因：单链路 dB 来自 FOE 算法结构非协同）

---

## TL;DR（给主线/用户判定用）

| 核查项 | 结论 | 证据 |
|---|---|---|
| jphot/oe BUPT 课题组是否已 claim 联合机制 | **是，完整 claim**（FSTS 一套 TS 做 FS+两段式 FOE+MRC 后联合补偿）| jphot-L71/101/175/208/385 |
| jphot/oe 是否已 claim 两段式 FOE 的 BL² 降噪 | **是**（这是 jphot 核心贡献之一）| jphot-L175/208 |
| BUPT 课题组是否已发星地分集续作 | **否**（jphot 全文 0 提 LEO/satellite/Doppler）| jphot grep LEO/satellite = 0 命中 |
| **B3-Q2 增量空间** | **LEO Doppler 时变（破 jphot 缓变假设）+ 星地场景迁移** | jphot-L208 自承"drifts slowly"假设 |
| **🔴 A1 归属核心结论** | B3-Q2 的 dB 优势机制（两段式 FOE BL²）**已被 jphot claim**，B3-Q2 增量 = 场景迁移+加 Doppler 维度，**属迁移型非算法创新型** | 见下详 |

---

## 1. jphot/oe BUPT 课题组的 claim 边界（jphot 原文逐条）

### jphot 已 claim 的（B3-Q2 不能再 claim）

| claim 项 | 原文证据 | B3-Q2 是否可复用 |
|---|---|---|
| FSTS 一套 TS 同时做 FS + FOE | jphot-L71 "integrates the functions of FS and FOE" / L101 "TS is firstly used for FS ... TS is used again to complete FOE" | ❌ 已被 claim，B3-Q2 不能当新点 |
| 两段式 FOE（粗+细）| jphot-L175 "two-stage FOE approach is proposed" | ❌ 已被 claim |
| BL² 降噪（二阶 FOE 除以 BL）| jphot-L208 "divided by BL, reducing the effect of residual Gaussian phase noise Δθn by BL times" | ❌ **这是单链路 dB 优势的物理来源，已被 jphot claim** |
| 跨极化共轭消调制相位 | jphot-L101/L208 "Conjugate multiplication using the same symbols with spacing BL on both polarizations ... eliminate phase noise and the phase of the modulated signal" | ❌ 已被 claim |
| MRC 后联合补偿（共享 LO，无需每支路独立 DSP）| jphot-L101 "each diversity branch can jointly compensate for signal impairment after MRC without separate DSP for each branch" | ❌ 已被 claim |
| X/Y 极化交织共轭对称 TS 设计 | jphot-L107 TX_1st/TY_1st 共轭 + 块间交错 | ❌ 已被 claim |

### jphot 自承的假设/局限（B3-Q2 的增量切口）

| 假设/局限 | 原文证据 | B3-Q2 切口 |
|---|---|---|
| **频偏缓变假设** | jphot-L208 "since frequency offset **drifts slowly in practice**, the coarse FOE ... can be saved in a buffer for continuous use" | 🟢 **LEO Doppler 时变破坏缓变假设——jphot 自己承认这是假设，B3-Q2 加 Doppler 维度是合法切口** |
| 湍流相位缓变假设 | jphot-L160 "slow-varying quantities relative to the symbol rate" | 🟡 星地强湍 deep fade/相位跳变会破坏（笔记 L54 已点）|
| 强湍低功率 FOE 精度退化 | jphot-L309 "may exhibit lower estimation accuracy ... when the received optical power is low" | 🟡 星地功率受限放大此短板 |
| 不做 LEO/卫星/Doppler | jphot grep LEO/satellite/Doppler/orbit = **0 命中**（全文 0 提卫星场景）| 🟢 **场景迁移切口** |

### jphot 结论强调的 dB（再次坐实转录错误）

jphot-L385（Conclusion）："the receiver sensitivity of the proposed scheme's **two-branch MRC** is improved by 1.43 dB and 2.54 dB in weak turbulence and by **2.09 dB and 3.41 dB** in strong turbulence"

→ **论文结论自己用的就是 2 支路数字（2.09/3.41）**。note/verify 把它错标成"4 支路"是转录错误，进一步坐实。

---

## 2. BUPT 课题组是否已发星地分集续作

### 课题组识别
- jphot 作者：**Liqian Wang, Jichen Wang, Xinyu Tang**（BUPT）— `papers/_read_notes/10.1109_jphot.2023.3265847.md:3`
- oe 作者：**Liqian Wang, Kunfeng Liu, Siqi Zhang, Shuang Ding**（BUPT）— `papers/_read_notes/10.1364_oe.520452.md:3`
- 两篇同课题组（oe 引 jphot 为 [24]）

### 续作检索

**本地证据**：
- jphot 全文 0 提 LEO/satellite/Doppler/orbit（grep 确认）
- jphot 引用链中 oe.520452 ref[23] = D. Boyu 等 2016 中文 "frame synchronization and frequency offset estimation based on **optical satellite link**"（Laser Technolog.）—— BUPT 课题组引用链里有"光卫星链路 FS+FOE"的 2016 中文工作，但**不是分集续作，是单链路卫星 FS+FOE**

**web 检索**：本轮未派子 agent 深查 BUPT 课题组 2024+ 续作（超本轮 3 步预算）。**标注为未决项**，进阶段 0.3-0.6 或下一对话补查（建议派子 agent 查 Liqian Wang / Siqi Zhang 2024+ 的 IEEE/Optica 续作 + 张思齐学位论文是否同组）。

### 当前判定（基于本地证据）

- **BUPT 课题组锚论文（jphot/oe）不做卫星**（0 提 LEO/Doppler）
- **B3-Q2 星地+Doppler 场景迁移切口在锚论文层成立**（jphot 缓变假设 + 0 提卫星是真实缺口）
- ⚠️ **但需补查 2024+ 续作**（防 BUPT 课题组自己已发星地续作，吞掉 B3-Q2 增量）—— **标为待办**

---

## 3. B3-Q2 相对 jphot+oe 的增量够格性（D005 标准）

### 增量分解

| 增量类型 | 内容 | D005 够格？ |
|---|---|---|
| **算法机制增量** | 两段式 FOE / FSTS / BL² 降噪 / 跨极化共轭 | ❌ **已被 jphot claim，B3-Q2 无算法机制增量** |
| **场景迁移增量** | 地面 FSO → 星地 LEO（加 LEO Doppler 时变 + 星地湍流）| 🟡 迁移型，D005"赢传统 baseline 几 dB"下**边际够格但偏薄**（参照 B7/B11 的场景迁移模式）|
| **维度扩展增量** | FOE+CPE → 加 CFO/Doppler 成四参数联合 | 🟡 维度扩展，需 MVE 验证 Doppler 维度是否带来真增益（可能撞 D006 边界，见 0.3）|

### D005 够格判定

**诚实结论：B3-Q2 属迁移型+维度扩展型，算法机制无增量（jphot 已 claim 核心）。**

- D005 务实路线接受迁移型（参照 B7/B11 都是迁移+维度扩展）
- 但 INVARIANT 12 原担心"jphot+oe 已做联合"——核查后发现 jphot 做的是 **FS+FOE+MRC**，**未做 CPE 联合、未做 Doppler 维度、未做卫星场景**
- 所以 B3-Q2 增量空间 = **CPE 维度加入 + Doppler 维度加入 + 星地场景**（三选一或组合）
- **够格前提**：MVE 必须证明加 Doppler/CPE 维度后相对 jphot 的 FS+FOE 有**新增益**（不能只是搬 jphot 到星地测一遍）

### 🔴 首要风险升级（从 0.1 延续）

**增益归因风险**（0.1b 子 agent 发现，本轮核查坐实）：
- B3-Q2 单链路 dB 优势（1.17dB）来自 **FSTS 两段式 FOE 的 BL² 算法结构**
- 这个结构 **jphot 自己就 claim 了**（L175/L208）
- 所以"B3-Q2 联合估计 vs 分立管线"的 dB 优势，本质是 **"jphot 算法 vs 传统 TS"的优势**，不是"子系统协同联合"的增量
- **如果 B3-Q2 的 baseline = 传统分立 TS 管线（jphot 的 baseline）**，那 B3-Q2 ≈ 把 jphot 搬到星地，dB 优势是继承的不是新增的
- **如果 B3-Q2 的 baseline = jphot FSTS**（更公平），那 B3-Q2 必须靠"CPE 联合 + Doppler 维度"产生**新增益**，这个增益目前无锚（需 MVE）

### 对 baseline 选择的硬约束（进阶段 0.4 必须处理）

| baseline 选择 | B3-Q2 增益预期 | 公平性 |
|---|---|---|
| 传统分立 TS 管线（jphot baseline）| ~1.17dB（继承 jphot）| ❌ 不公平（B3-Q2 = jphot 搬星地，增益是 jphot 的）|
| **jphot FSTS（同算法结构）** | 需 MVE 验 CPE/Doppler 维度新增益 | ✅ 公平，但增益未知 |
| jphot FSTS + 传统 CPE | 需 MVE 验联合 CPE 增益 | ✅ 最公平 |

---

## 4. A1 归属核查结论

### INVARIANT 12 原担心核查

> INVARIANT 12："jphot+oe BUPT 课题组**已完成 FS+FOE+MRC 联合**（一套 TS 跨子模块复用）"

**核查 PASS**：jphot 确实做了 FS+FOE+MRC 联合（L101）。但需精确化：
- jphot 联合 = FS + FOE + MRC（三模块共享一套 TS）
- **jphot 未做 CPE 联合**（CPE 另用相位噪声估计 + DD-LMS 兜底，jphot-L101/L243）
- **jphot 未做 Doppler/CFO 维度**（缓变假设 L208）
- **jphot 未做卫星场景**（0 提 LEO）

### B3-Q2 增量空间（精确版）

B3-Q2 相对 jphot+oe 的合法增量（非 jphot 已 claim）：
1. **加 CPE 联合维度**（jphot 的 FSTS 只做 FS+FOE，CPE 独立）—— 协同扩展
2. **加 Doppler/CFO 维度**（破 jphot 缓变假设，jphot-L208 自承假设）—— 维度扩展，需注意 D006 边界（0.3）
3. **星地场景迁移**（jphot 是地面 FSO，0 提卫星）—— 场景迁移

### A1 归属判定：**B3-Q2 增量空间存在但偏薄（迁移+维度扩展型，非算法创新型）**

- 不够格 Kill（有合法增量切口：CPE 联合 + Doppler + 星地）
- 但**首要风险从"4 支路迁移"转移到"增益归因"**：B3-Q2 必须在 MVE 证明联合 CPE/Doppler 维度的新增益，不能只搬 jphot 算法到星地
- baseline 必须含 jphot FSTS（不能只比传统 TS，否则增益是继承的）

---

## 5. 待办（进 0.3-0.6 或下一对话）

1. **🔴 派子 agent 查 BUPT 课题组 2024+ 续作**（Liqian Wang / Siqi Zhang / Kunfeng Liu 2024+ IEEE/Optica 论文 + 张思齐学位论文是否同组）—— 防 BUPT 自己已发星地续作吞增量
2. **阶段 0.4 baseline 必须含 jphot FSTS**（不能只比传统 TS）—— 公平对照硬约束
3. **阶段 0.3 架构定性**：加 Doppler 维度的具体形态——前馈开环（不撞 D006）还是环路 TF（撞 D006 转 B3-Q3）
4. **修正转录错误**：note-L36 + `_cut-b1b2b3-verify.md:258-291` + S031 + INVARIANT 11 的"4 支路 +2~3dB"→"2 支路 +2~3dB，4 支路 0.7dB(4-QAM)/2.14dB(16-QAM)"

## 方法局限

- 本轮未派子 agent 查 BUPT 2024+ 续作（超 3 步预算），web 检索留待下一对话
- 张思齐学位论文与 BUPT 课题组关系未核查（jphot/oe 作者 Siqi Zhang 与张思齐是否同人未确认）
- CPE 联合维度的 dB 预期无锚（需 MVE 或进一步文献查）
