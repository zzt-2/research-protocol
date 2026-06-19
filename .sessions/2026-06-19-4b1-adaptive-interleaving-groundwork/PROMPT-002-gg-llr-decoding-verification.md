# PROMPT-002: (c) GG-LLR 译码改进候选 — 精读验证

> 新对话粘贴此提示词启动。本专题 = 2026-06-19-4b1-adaptive-interleaving-groundwork（4b#1 Kill 后重定方向探索）。
> 接续 S002（IM/DD 调研 + 译码改进候选发现）。
> 日期: 2026-06-19

---

## 怎么开始这个对话

你是 ZCode，正在帮用户做硕士论文方法方向重定。4b#1（信道感知自适应交织）已被 FR-21 三版门控 Kill（BER 增益 0dB）。S002 发现一个**绕开 4b#1 死法**的候选方向：**(c) GG 湍流信道感知译码（GG-PDF 接入 LLR）**。现在要精读验证这个候选的真实物理空间。

**第一步必须做的事（按优先级）**：

1. **报到**：调 session-governance skill（Trigger 1），确认本专题范围边界（active，S002 重定方向探索）
2. **读 S002**：`.sessions/2026-06-19-4b1-adaptive-interleaving-groundwork/S002-post-kill-redirection-exploration.md` —— 当前对话的发现记录，含 (c) 候选 + 3 个待验证风险
3. **读 H001**：`.sessions/2026-06-19-4b1-adaptive-interleaving-groundwork/handoffs/H001-redirection-after-4b1-kill.md` —— 4b#1 Kill 收尾 + 4 条殊途同归 + 重定方向纪律
4. **读必读文件**（见下）

## 本轮目标

**精读验证 (c) GG-LLR 译码改进的物理空间是否 >0.5dB**。这是定方向前的最后核查（FR-21 式门控，避免第二次撞物理天花板）。

核心验证任务（S002 后续段）：
1. **精读 Jiang 2023/2024**（Photonics 11(1):34, doi:10.3390/photonics11010034）—— 分清 dB 提升来自 LLR 接入 GG 还是 bit-interleave。**这是 (c) 成立的关键**：若主要来自 interleave，纯 LLR 空间可能 <0.5dB
2. **翻王秋悦/唐承茂 LLR 章节** —— 确认高斯 LLR 公式 + 未接 GG 的原文 + 有无隐含理由（SNR 范围内高斯近似够好？）
3. **快速纸笔估算** GG-LLR vs 高斯 LLR 失配量级（强湍流下是否 >0.5dB 对应的 LLR 差）
4. 若 (c) >0.5dB → 定方向进 Groundwork（FR-21 式门控：高斯 LLR baseline vs GG LLR 的 BER 上界）
5. 若 (c) <0.5dB → 回 S002 Q3 其他候选（(a) 换强湍流设定的编码+交织 / 译码保底方向）

## 必读文件（按优先级）

### 当前状态（必须读懂）
1. `S002-post-kill-redirection-exploration.md` —— 标题/体制约束澄清 + IM/DD 调研 + (c) 候选 + 3 个待验证风险
2. `handoffs/H001-redirection-after-4b1-kill.md` —— 4b#1 Kill + 殊途同归 + 重定方向纪律

### 候选 (c) 的证据链
3. `papers/downloads/2026-06-18-cnki-survey/LDPC编码在星地光通信中的性能仿真研究_王秋悦.md` —— **找 LLR 章节**，确认用高斯 LLR 未接 GG（王秋悦 L1302 自留展望"多元 LDPC 未做"也佐证译码侧有缝）
4. `papers/downloads/2026-06-18-cnki-survey/空空激光通信链路抗突发错误交织编码技术的研究与实现_唐承茂.md` —— **找 SCL 译码 LLR 章节**（L914-954 译码算法 + L1356/1362 定点量化），确认 LLR 高斯假设
5. Jiang 2023/2024（Photonics 11(1):34）—— **精读核心**，用 tools/search 或子 agent 查全文（DOI 10.3390/photonics11010034），分清 dB 来源

### 重定方向纪律
6. `decisions.md` D001 —— 4b#1 Kill 死因（BER 0dB + 时延无先例）+ 可复用资产（FR-21 三版门控方法学，新方向同样适用）
7. `verifications.md` V001 —— FR-21 三版验证范式（主脚本 MC + 唐承茂一手校准 + 敏感性瀑布排除伪信号）—— **(c) 验证也要用这套范式**
8. `voice.md` 2026-06-19 —— 用户硬约束（指标"都行"但**必须有可量化对比** + **必须有中文硕论先例**"不然很危险"）

### 上一专题（定方向）的教训
9. `../2026-06-17-thesis-method-redirection/decisions.md` D005 —— 增量改进定位（baseline 是别人做过的，改进点明确）
10. `../2026-06-17-thesis-method-redirection/decisions.md` D003 —— FPGA 当验证章（非方法章）

## 关键约束（必须遵守）

1. **增量改进定位**（D005，未推翻）：baseline = 王秋悦/唐承茂（高斯 LLR），改进 = GG-LLR。**不要追"空白"**
2. **必须有中文硕论先例**（用户硬约束）：(c) 的中文先例 = 王秋悦 2020 + 唐承茂 2025（都做译码但 LLR 未接 GG）。先例成立
3. **物理天花板 >0.5dB**（FR-21 教训）：精读 + 纸笔估算必须先确认 (c) 在星地 GG 湍流下 >0.5dB，再定方向
4. **绕开 4b#1 Lburst 天花板**：(c) 依赖"信道 PDF→LLR 公式"稳态链路，不依赖"突发统计→参数"动态链路。这是 (c) 优于 4b#1 的核心
5. **不撞红线**：LLR 计算是符号级软信息（FEC 内部），TL-03/04 针对载波同步符号级不迁移到译码层；不撞路由 D004 / D 排除列
6. **子 agent 强制委托**：Jiang 2023 精读 / web search 在子 agent；主对话只接收结构化摘要
7. **主对话严禁 WebSearch/webReader**（用 tools/search 或子 agent）

## 待验证的 3 个风险（S002 列出，本轮解决）

| # | 风险 | 验证方式 | 影响 |
|---|---|---|---|
| 1 | Jiang 2023 的 dB 提升来自 LLR 还是 interleave | 精读全文分清 | 若主要 interleave，纯 LLR <0.5dB |
| 2 | 王秋悦/唐承茂用高斯 LLR 有无隐含理由 | 翻他们 LLR 章节 + SNR 范围 | 若高斯够好，接 GG 改善有限 |
| 3 | GG-Meijer-G LLR 闭式复杂度 | 纸笔/查文献 | 推不出退数值积分/查表（比 4b#1 轻）|

## 开场怎么说

读完 S002 + H001 + 必读文件后，报到：
1. Session Start Confirmation（topic active / 范围 / 不变量 / voice）
2. 本轮验证计划（3 个风险逐个怎么验）
3. 第一步具体做什么（建议先派子 agent 精读 Jiang 2023 全文，因为风险#1 是 (c) 成立的关键）

---

## 附：候选 (c) 一句话定位

**(c) GG 湍流信道感知译码** = 把王秋悦/唐承茂的高斯 LLR 换成 GG-PDF 感知 LLR。
- baseline：王秋悦 2020 LDPC / 唐承茂 2025 Polar，都用 AWGN 高斯假设的 LLR
- 改进点：LLR 公式接入 GG 湍流统计（PDF→LLR）
- 创新论证："baseline 用高斯 LLR 失配真实湍流信道，我接 GG-LLR，BER 提升 X dB"
- 绕开 4b#1：不依赖 Lburst 动态量，稳态 LLR 失配即使信道静态也存在
- 先例：Jiang 2023 同族 0.96-1.66dB（待分清 LLR vs interleave 贡献）
