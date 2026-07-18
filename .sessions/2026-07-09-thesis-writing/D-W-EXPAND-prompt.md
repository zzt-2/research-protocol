你是 CCISP 2026 论文写作专题的一个子对话执行者。本轮任务：D-W-EXPAND 正文加厚——补 R014 发现的缺口，从当前 ~1628 词加到目标 3000 词（+~1370 词）。

## 核心纪律（最高优先级）

**每个缺口补什么内容、补到什么粒度，必须先看对标集对应段落怎么写的，照看来的粒度补。绝对不拍脑袋。** 这是本轮存在的全部意义——R014 已经定位了缺口（对标集有我们没），本轮是把缺口填上，填的依据是对标集的写法，不是"我觉得该写什么"。

## 背景

正文 5 节 + Abstract 已写完（W001/W002/W003），但 R014 内容映射发现严重偏短（1628 词，比最精简会议对标集 OECC-PSC 2247 还少 28%）。偏短不在 Intro/Conclusion/Abstract（在范围内），集中在三个明确缺口 + §II SM 偏薄。目标加到 3000 词（对齐 Paillier 3025 体例最像会议标准稿，审稿人对单薄比略冗余更敏感）。

## 必读（读完再动手）
1. .sessions/2026-07-09-thesis-writing/R014-content-mapping.md —— **本轮核心依据**。重点读「产出 3 逐节缺口清单」（三个明确缺口 + 可选缺口）+「产出 2 内容地图」（每篇每节写什么，这是补内容的粒度参照）
2. .sessions/2026-07-09-thesis-writing/R010-strength-baseline-table.md —— 力度基准。加厚≠加力度，补内容仍守 R010 力度（公式仍直接给不推导）
3. .sessions/2026-07-09-thesis-writing/W001-intro-system-model.md —— 现有 §I+§II 正文（加厚的对象）
4. .sessions/2026-07-09-thesis-writing/W002-method-results.md —— 现有 §III+§IV 正文（加厚的对象）
5. .sessions/2026-07-09-thesis-writing/W003-conclusion-abstract.md —— 现有 §V+Abstract（结论：不动，R014 确认在范围）
6. .sessions/2026-07-09-thesis-writing/R011-terminology-symbol-formula.md —— 术语/符号/公式三表（补的内容照抄，不发明新词/新符号）
7. .sessions/2026-07-09-thesis-writing/R012-params-narrative.md —— 参数表 + 数字清单（§IV 实验设置段从这里取参数）
8. .sessions/2026-07-09-thesis-writing/R009-logic-chain-final.md —— 逻辑链（补的内容不超出有把握范围）

## 加厚目标（逐缺口，每个标了对标集参照）

### 缺口 1：§IV 实验设置段（5/5 对标集有，最容易，+~200 词）

**对标集参照**（R014 产出 2 已提取，你看 R014 的内容地图）：
- Le Bidan §V 段1：帧 4160(4.8%开销)/400训练+300捕获+512测量符号
- Johst §III 开头：100 MC 仿真
- Panasiewicz §III-B：VPI+Python 仿真工具
- Paillier §IV：SNR 10dB/初始频偏

**补什么**：在 §IV 开头（§IV-A 之前）加一段"Simulation Setup"。内容从 R012 参数表组织（不发明新参数）：30 seed 蒙特卡洛 / N_blocks=400（≥1e5 比特）/ SNR 扫描范围（AWGN 5-20dB / 湍流 5-26dB）/ 评估指标（BER + HD-FEC 3.8e-3 门限）/ 仿真工具或框架描述（如实，不编）。

**粒度参照**：对齐 Panasiewicz/Paillier 的设置段长度（~150-200 词），不超过 Le Bidan。一段，不分子节。

### 缺口 2：§III 替代方案对比 + 弃用理由（4/5 有，+~300 词）

**对标集参照**（R014 产出 2）：
- Le Bidan §IV-G：V&V 与 BPS 在 Es/N0<5dB 崩溃（V&V 四次方噪声放大、BPS 错误传播）→ 改用 pilot-ML+线性插值
- Johst §II 开头：blind(CMA)收敛慢/低 SNR 不稳/调制格式相关 → 选 DA 因独立于调制格式
- Panasiewicz §II-C：旧法 lookup table 增益依赖 Ps 致不稳 → 改进=MAF+atan2

**补什么**：在 §III 加一段"为什么用切换方案，而非纯 DA / 纯 NDA / 其他判据"。讨论三类替代方案各自的局限：
- 纯 DA 全场景：高 SNR 区付 1.25dB overhead 无收益（R009 逻辑链高 SNR NDA 净赢）
- 纯 NDA 全场景：低 SNR 区受 squaring loss（引 V&V 1983，R009 已定）
- 切换判据选择：为什么用 per-block SNR 作判据（而非 SNR 平滑估计/ genie-aided / 其他）

**⚠️ 红线（D002）**：讨论"切换优于纯 DA/纯 NDA"时，**绝对不能滑回"切换是必要环节"或"切换是闭环前提"**（D002 已推翻——切换净增益微弱，net gain +1.2dB 来自 NDA 架构本身不依赖切换）。正确措辞：切换是"在两法各自优势区自动选优"（R008/⑤ hedging 后 = 选 lower-BER estimator），不是"纯 DA/纯 NDA 不行所以必须切换"。切换 framing 仍是"自适应选优"。

**粒度参照**：对齐 Johst §II 开头的 DA vs blind 对比段（~200-250 词），不超过 Le Bidan §IV-G（太详细）。

### 缺口 3：§III 设计权衡讨论（5/5 有，+~250 词）

**对标集参照**（R014 产出 2）：
- Paillier §III-B：BLT=噪声敏感 vs 收敛速度权衡
- OECC §Proposed：sub-block 尺寸=复杂度/性能权衡
- Panasiewicz §III-A：Bn 优化 / 延迟分析

**补什么**：在 §III 补"设计权衡"。两类：
- **γ_th 阈值选择的权衡**：γ_th 设在哪？为什么？权衡是什么（太低=低 SNR 区误选 NDA 受 squaring loss / 太高=高 SNR 区误留 DA 付 overhead）？**注意：γ_th 的实际值和选择依据必须基于数据/代码，不能拍脑袋——如果代码里有 γ_th 的确定方式（如取 crossover SNR），照实写；如果没有明确依据，诚实写"γ_th is set to the measured crossover SNR for each turbulence regime"（R009 crossover 数据：weak 17.9/mod 16.8/strong 10.7）**
- **切换复杂度/代价**：per-block SNR 计算 + 估计器选择的计算开销。**注意：复杂度数字必须有依据**——如果你能从代码确认计算量（如"两次角度估计+一次比较"），照实写；如果不确定，给定性描述（"incurs negligible overhead: one SNR estimate and one comparison per block"），不编具体 FLOPs

**粒度参照**：对齐 Paillier §III-B 权衡段（~200 词）。

### 缺口 4：§II System Model 补充（+~250 词）

**对标集参照**：Paillier §II(399 词) / Panasiewicz §II-A/B(链路+湍流模型)

**补什么**：§II 当前 268 词偏薄（Paillier 399）。补：
- Gamma-Gamma 模型多一句解释（αβ 参数与湍流强度/Rytov 方差 σ²_R 的关系，引 Al-Habash 2001）——**注意：不给 GG PDF 公式**（R010 §2.1 已定给模型名+块结构不给 PDF，加厚≠加力度）
- 帧结构 pilot arrangement 多一句（为什么每 4 符号 1 pilot——对齐 B11 帧结构）
- 信号模型 r_k 公式后的参数解释补全（当前哪些参数解释了哪些没解释，对照 Paillier §II 看粒度）

**粒度参照**：对齐 Paillier §II(~400 词)。补到 §II ~400-450 词。

### 缺口 5：§I Introduction 补项目/标准化背景（3/5 可选缺口，+~150 词）

**对标集参照**：Le Bidan §I 段2(CNES/CCSDS) / Johst §I 段2(多孔径/100-200Gb/s 需求) / OECC §I(400ZR/1.6Tbps)

**补什么**：Intro 第 1 段背景补 1-2 句"星地 FSO 的容量需求/发展趋势"（如 LEO 星座 feeder 链路容量需求 → 相干 FSO 的必要性）。**注意：不编具体项目名/标准号**（如不编"CCSDS 某标准"——我们不是 Le Bidan 那种项目论文）。给通用趋势陈述（"high-data-rate feeder links"/"LEO constellations"），引已有文献（sat.1553 综述 / Paillier / Johst）。

**粒度参照**：对齐 Johst §I 段1-2 的背景厚度（~150-200 词），不超过 Le Bidan 项目级展开。

### 不补的（R014 确认不是缺口或设计选择）
- §V Conclusion / Abstract：不动（R014 确认在范围）
- §IV 现象解释：不补（R009 已定 crossover 不附归因，3/5 对标集有但我们选择不写=设计选择）
- §III 逐子模块：不硬补（我方方法本质简洁，R014 已打折）
- §II 链路几何：不补（块衰落仿真只依赖 αβ 不依赖几何，2/5 可选缺口）

## 执行方法

### 第一步：派子 agent 看对标集对应段落粒度（不拍脑袋的前提）

派 2 个子 agent 并发，提取对标集对应段落的**写法粒度**（不是内容，内容 R014 已提取；本轮要的是"怎么写"——句式/结构/展开方式）：

**agent A**：看 Le Bidan §IV-G + Johst §II 开头 + Panasiewicz §II-C 的"替代方案对比+弃用理由"写法。提取：对比用什么句式（"X suffers from ... [ref], therefore we adopt Y"）？弃用理由给多详细（一句话定性 vs 给数据）？对比段多长（词数）？返回 ≤400 词写法模式。

**agent B**：看 Paillier §III-B + OECC §Proposed 的"设计权衡"写法 + Le Bidan §V/Johst §III/Paillier §IV 的"实验设置段"写法。提取：权衡怎么表述（"X trades off against Y"）？设置段结构（参数列表 vs 散文）？返回 ≤400 词写法模式。

### 第二步：主线程按粒度补五个缺口

收到子 agent 写法模式后，主线程按粒度补：
- 缺口 1（§IV 实验设置段）：从 R012 参数表组织，照 agent B 提取的设置段结构
- 缺口 2（§III 替代方案对比）：照 agent A 提取的对比句式，守 D002 红线
- 缺口 3（§III 设计权衡）：照 agent B 提取的权衡写法，γ_th/复杂度有依据
- 缺口 4（§II 补充）：照 Paillier §II 粒度补 GG/pilot/参数解释
- 缺口 5（§I 背景）：照 Johst §I 背景粒度补 1-2 句趋势

每个缺口补完标词数。

### 第三步：词数核验

补完重新统计 W001/W002/W003 词数（用 wc -w，跟 R014 同方法），确认：
- 总词数到 ~3000（±100 可接受）
- 每节词数在对标集范围内（不超标）

### 第四步：交叉检查（加厚后一致性）
- 术语/符号仍跟 R011 一致（补的内容照抄三表，不发明新词/新符号）
- 数字仍跟 R012 一致（§IV 实验设置段参数跟参数表）
- 切换 framing 仍"自适应选优"（R008 + ⑤ hedging lower-BER），缺口 2 讨论替代方案时**禁滑回"切换必要"**（D002）
- crossover 只呈现数据不附归因（R009）——缺口 3 讨论 γ_th 时说"γ_th set to measured crossover SNR"，不解释为什么 crossover 左移
- 力度仍对齐 R010——补内容≠加力度，公式仍直接给不推导（§II 不补 GG PDF）
- 自造词零残留（grep 确认）

## 输出

**直接 Edit W001/W002/W003**（跟 F1 模式一样，加厚内容进原文件）。

另外新建一个审计记录：.sessions/2026-07-09-thesis-writing/W005-expand-record.md
格式：session note 模板。「记录」段列五个缺口各补了什么（旧→新，词数变化）+ 对标集粒度参照（agent A/B 返回的写法模式摘要）+ 词数核验总表（加厚前 1628 → 加厚后 ~3000，逐节）+ 交叉检查结果。

## 质量红线（必须守）
1. **不拍脑袋**——每个缺口补的内容/粒度有对标集参照（agent A/B 返回），不是"我觉得"
2. **D002 红线**——缺口 2 讨论替代方案时禁滑回"切换必要/闭环前提"，切换 framing = 自适应选优（R008 + ⑤ hedging）
3. **R009 红线**——crossover 只呈现数据不附归因；squaring loss 引 V&V 1983 不推导；γ_th 讨论说"set to measured crossover SNR"不解释为什么左移
4. **力度仍对齐 R010**——补内容≠加力度，§II 不补 GG PDF 公式，公式仍直接给结论级
5. **术语/符号跟 R011**——照抄三表，不发明新词/新符号
6. **数字跟 R012**——§IV 实验设置段参数跟参数表，γ_th 用 R009 crossover 数据（17.9/16.8/10.7）
7. **复杂度/γ_th 有依据**——不编 FLOPs，不确定给定性描述；γ_th 如无明确代码依据写"set to measured crossover SNR"
8. **切换 framing 统一 lower-BER**（⑤ hedging 后），不用 locally optimal
9. **守 FR-22**——不跑新实验，只读已有代码/数据/对标集

## 完成判据
- 五个缺口补完（§IV 实验设置段 / §III 替代方案对比 / §III 设计权衡 / §II 补充 / §I 背景）
- 总词数到 ~3000（±100），逐节核验
- 交叉检查通过（术语/数字/framing/crossover/力度/自造词 6 项）
- 审计记录 W005 完整（五缺口补了什么 + 对标集粒度参照 + 词数核验 + 交叉检查）

## 完成后做什么
1. 更新 topic-index.md「进展线索」新增 W005 条目 +「当前位置」标 D-W-EXPAND 完成、正文加厚到 3000 词、下一步全篇通读 + 等导师反馈。
2. commit（本对话统一提交一次，消息概括 D-W-EXPAND 加厚工作）。
