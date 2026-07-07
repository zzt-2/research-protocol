# [S002] 对话 1 — 阶段 0.1 够格路径验证 + 0.2 dB/范围溯源核查

> 2026-07-08 | 阶段: 工作对话执行阶段 0.1-0.2（不写代码）| 状态: 完成，B5-Q1 够格走路径 C，交对话 2 执行 0.3-0.6

## 目标

承接主控对话 S001 + H001 派发，执行阶段 0.1（够格路径验证）+ 阶段 0.2（dB/范围溯源核查），不写代码。核心是验证 B5-Q1 范围优势（±4.5GHz vs 传统 ±312.5MHz，15× 范围扩展）在 D005 会议门槛下能不能当 Go 判据。

## 记录

### 报到 + 接收方验证（步骤 1）

session-governance Trigger 1 报到 + 读必读清单 1-7：
- 本专题 4 文件（topic-index 14 不变量 / H001 / S001 / decisions.md D001）
- B5 锚全文 content.md 252 行
- B5 详评 `_B5-...-increment.md` + `_cut-b4b5-verify.md` + `_cut-b4b5-paillier-pool.md` + `_cut-map-final-b1-b12.md`
- _registry.yaml（4 依赖全稳定）
- 上游 decisions.md（D005 务实路线 / D006 红线 / D009 checklist）+ S031（B5-Q1 排第二档 #6）
- profile.md（9 次防线 + 务实可毕业 + 委托技术判断）

接收方验证 4 条全打钩：
- topic-index 14 不变量已读（重点 11/12/13/14 B5 特殊）
- 3 条关键事实声称全 PASS（B5 本体无 dB 对比 / ±4.5GHz 多处一致 / B5 不撞 D006 前馈路径）
- _registry depends_on 4 依赖全稳定
- 范围未违反"明确不含"

### 阶段 0.1 够格路径验证（步骤 2，最高优先）

**0.1a 子 agent 核查 B5 锚全文范围优势具体指标**

派 Explore 子 agent 读 B5 锚 content.md 全文，提取范围优势指标 + 核查"本体无 dB 对比"声称 + 实验场景核查 + [60] Leven 7dB penalty 溯源。子 agent 产出后主线独立 grep 核查两个关键归因（守 INVARIANT 10 核查机制中性双向）：

1. **conclusion L167 不含 ±4.5GHz — 子 agent 归因 PASS**（主线 sed 验证 L163-168 conclusion 只复述 ±312.5MHz + ±250MHz）。H001 声称"四处含 conclusion"修正为"五处 L23×2/L29/L47/L143/L149，不含 conclusion"。这是 H001 的小事实错误，不影响范围优势核心判定。
2. **B5 锚全文无 7dB/penalty/Leven/[60] — 子 agent 归因 PASS**（主线 grep exit=1，B5 最大 ref [28]）。`_B5-...-increment.md:43` 的"[60] Leven 7dB penalty"数字不来自 B5 锚，是详评笔记引入的对照数字。

B5 范围优势指标全标行号（FR-26 读原文数值）：±4.5GHz（L23/L29/L47/L143/L149）/ σ<140MHz（L23/L47）/ 250MHz max（L149/L167）/ <5MHz（L149）/ ±312.5MHz 精估范围（L57/L95/L149/L167）/ BER 1e-3 −48dBm（L149）/ 56MHz/s（L147）/ 收敛 8 点第 4 次 16 点第 3 次（L129/L141）。

B5 vs 传统 baseline 对比形态：定性对比（"低复杂度/无 pilot/不依赖 MIMO DSP" L47/L167），**无"vs baseline 改善 X dB"定量对比**。`_cut-b4b5-verify.md:64-66` 声称 PASS。

B5 实验形态：B2B（L91）+ Intel Arria 10 FPGA（L93/L95/L109）+ 无湍流建模（L29 仅背景提）+ PM-QPSK 2.5GBaud（L23/L47/L89）。跟 B4 同 BUPT 团队 + 同 Arria 10 模板（`_cut-b4b5-paillier-pool.md:27,41` + `_cut-map-final-b1-b12.md:68,142`）。

**0.1b 够格路径 3 选项分析**

| 路径 | 判定 | 理由 |
|---|---|---|
| A（BUPT Arria 10 FPGA demo 会议模板）| 部分成立有缺陷 | 会议门槛放宽 + BUPT 模板对标确认绝对指标够格形态，但 B5 锚已发期刊，B5-Q1 需做出增量贡献不能"对标发会议" |
| B（补 dB 对比）| 风险路径单独不成立 | 任务环节错位风险（B5 粗 CFO vs [60] Leven 精细 FE）+ 结果可能不利风险（湍流下 B5 残频 dB 可能不如 [60] Leven）|
| C（鲁棒性维度）| **主够格路径成立有增量要求** | 范围 15× + 鲁棒性三维组合会议够格（B7 同模式 OFC 已发），但需在 B5 锚基础上做增量（加湍流验证）|

**0.1c 判定门控**

**B5-Q1 够格，走路径 C 为主 + 路径 A/B 补充，不转 Kill。**

够格叙事框架（会议级别）：
- 主叙事（路径 C）：B5 短时谱 FOE 在星地 LEO Doppler 场景下实现 15× 范围扩展 + 56MHz/s 跟踪稳定性 + 低接收功率鲁棒性，验证 B5 范围优势在湍流信道下仍成立
- 增量贡献（B5 锚 B2B 无湍流 → B5-Q1 加湍流验证）：对标 B11 加 FSO 湍流同模式
- 辅助维度（路径 A）：绝对指标对标 BUPT Arria 10 FPGA demo 会议模板
- sandbox 验证维度（路径 B）：在湍流下 vs [60] Leven 做残频/BER 对比，若 B5 有 dB 增量则叠加够格，若无则靠路径 C/A

判定依据：INVARIANT 11 路径 C 成立（B7 OFC 已发先例 + B5 范围 15× 比 B7 的 1.9× 更强）+ D005 会议门槛放宽 + FR-25 Go 标准=赢传统 baseline（范围 15× 超传统 ±312.5MHz 是结构性优势）+ 切法地图 §B.1/§C.2 确认鲁棒性维度够格路径。

**不转 Kill**：路径 C 明确成立，不是三条都不成立。**不直接当 Go 跑 MVE**（守红线 1）：够格路径验证 ≠ 直接当 Go，阶段 0.2-0.6 前置规约必须全做完才进 sandbox（INVARIANT 6 + profile 第 9 次防线）。

### 阶段 0.2 dB/范围溯源核查（步骤 3）

主线独立 grep 核查所有关键参数文献来源：

1. **±4.5GHz 五处一致 PASS**（L23×2/L29/L47/L143/L149，不含 conclusion L167——H001 小事实错误已修正）
2. **残频指标全读原文数值 PASS**（σ<140MHz / 250MHz / <5MHz / ±312.5MHz / BER 1e-3 −48dBm 全标行号）
3. **[60] Leven 7dB penalty 溯源 PASS**：数字来自 [60] Leven 原文 L123（differential decoding 无 FE 时 500MHz 频偏的 OSNR penalty），不是 B5 锚的数字。详评笔记 `_B5-...-increment.md:43` 标注正确
4. **残频上限公式 Δfm=fs/8N 溯源 PASS**：sat.1553 L549-553 引 [60] Leven 公式 27，B5 ±312.5MHz 精估范围跟此公式同族（N=1 时 fs/8）。B5 粗 CFO 定位跟 sat.1553 "粗补偿即可"结论一致
5. **B5 vs B4 dB 形态对照**：B5 比 B4 在 dB 维度更弱（B5 无 dB 对比，B4 有 ±920MHz @ 0.5dB 内部对照），但 B5 范围远大于 B4（±4.5GHz vs ±920MHz）
6. **饱和池警示适用性**：B5 走范围维度不直接跟饱和池 dB 竞争，但需 sandbox 验证范围优势在湍流下仍成立

B5Params 草稿前置 20 字段全溯源 PASS（_db_range_sourcing_audit.md §6 表），可直接进阶段 0.5 草拟。

### 产出物

1. `explore/b5-leo-doppler-spectrum-foe/_qualification_path_validation.md` — 阶段 0.1 够格路径验证（3 选项分析 + 判定门控 + 够格叙事框架）
2. `explore/b5-leo-doppler-spectrum-foe/_db_range_sourcing_audit.md` — 阶段 0.2 dB/范围溯源核查（20 字段参数真相源表 + [60] Leven 7dB 溯源 + 残频上限公式溯源）
3. S002 session note（本文件）
4. H002 handoff（交对话 2 执行 0.3-0.6）

## 决策引用

- D001（引用，不新建）：开 B5-Q1 专题 + 首验证够格路径策略。本轮 0.1 验证结果=路径 C 成立，B5-Q1 够格不转 Kill，是对 D001 的执行验证
- 无新建 D###（阶段 0.1-0.2 是验证核查，够格路径判定是 D001 的执行落地，不是新方向决策。若后续阶段 0.3-0.6 发现路径 C 前提崩塌再立 D###）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（阶段 0.1-0.2 前置规约核查，未写代码未进 sandbox）
- **守 profile 第 9 次"急于推进"防线**：阶段 0 六项规约全做完才进 sandbox，本轮只做 0.1-0.2，0.3-0.6 留下一对话
- **守 3 步上限**：本轮 3 步（①报到+读必读 ②阶段 0.1 够格路径验证 ③阶段 0.2 dB/范围溯源核查）
- **守核查机制中性双向**（INVARIANT 10）：子 agent 产出 + 主线独立 grep 核查，只信原始数字不信归因（conclusion L167 不含 ±4.5GHz + B5 锚无 7dB penalty 两个关键归因主线独立复核 PASS）
- **守 TL-26 + FR-26 + V6**：所有参数读原文数值不只引位置，20 字段全标行号
- **守工作对话角色边界**：只执行阶段 0.1-0.2 规约核查，不进 sandbox 不写 MVE 代码

## 后续

### 交对话 2 执行阶段 0.3-0.6（H002 交接）

1. **阶段 0.3 架构定性**（INVARIANT 13 B5 特殊）：湍流致功率波动归一化走前馈路径（合法不撞 D006），禁环路 TF 联合建模。**关键前提验证**：前馈归一化后 B5 范围优势是否仍成立（路径 C 的核心前提，若崩塌则红线警报）
2. **阶段 0.4 公平对照框架**（INVARIANT 14 + LEO Doppler 主题差异化）：baseline [60] Leven Mth-power 还是传统 FFT FOE？范围 fair gain 定义？工作点 BER 1e-3 还是 HD-FEC？B5（频域功率比）vs B7（定时域 TED）vs B4（双环）叙事定位
3. **阶段 0.5 参数真相源前置**：B5Params 草稿 20 字段全溯源已就绪（_db_range_sourcing_audit.md §6 表），参考 B7Params 扩写
4. **阶段 0.6 文件组织规约**：`explore/b5-leo-doppler-spectrum-foe/` 目录结构 + short_time_spectrum_foe 接口定义（参考 fft_foe_m0_omega sc_nda_ml_sim.py:137 作起点骨架）

### 主控对话跟进点

- 阶段 0.1 够格路径验证是否真对标了 BUPT Arria 10 FPGA demo 会议模板（不是绕过）——本轮路径 A 部分成立，路径 C 主够格，对标 B7 OFC 已发先例
- 阶段 0.2 的 dB/范围溯源是否全读原文数值——本轮 20 字段全标行号 PASS
- B5 vs B7/B4 的 LEO Doppler 主题差异化是否明确——留阶段 0.4 定

### 已知风险（交对话 2）

- **路径 C 增量贡献风险**：B5-Q1 加湍流验证后范围优势可能衰减（湍流致功率波动污染正负功率谱面积比），阶段 0.3 架构定性需验证前馈归一化后范围优势仍成立
- **路径 B 任务环节错位风险**：B5 粗 CFO vs [60] Leven 精细 FE 任务环节不同，补 dB 对比需论证公平性（0.2 已溯源 [60] Leven 7dB penalty 是 differential decoding 无 FE 场景，不是 B5 vs [60] Leven 直接对比基线）
- **饱和池竞争风险**（INVARIANT 12）：B5 走范围维度不直接跟饱和池 dB 竞争，但需 sandbox 验证
- **B5 锚已发期刊的 A1 归属风险**：B5-Q1 增量必须是论文外改进（加湍流 + vs baseline + 鲁棒性验证），路径 C"加湍流验证"是天然论文外切口
