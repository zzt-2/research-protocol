# Handoff: 切换方案「跨场景自动选优」framing 专门研究

> 来源: S006（2026-07-10/11 D1 图表制作对话）| 交接目标: 开新对话专门验证「切换跨场景自动选优」framing 能不能成立
> 文件名: H005-switch-cross-scenario-framing-investigation.md
> 日期: 2026-07-11

## 到哪了（状态）

D1 图表制作对话中，用户看了 Fig.4（6 条 BER 曲线：3 场景 × DA/NDA）后提出新 framing：

> "不同湍流条件下，两种方法优势不同？有时候同样 SNR，同一个方法有的好有的差。切换的话，面对不同湍流条件能够及时用更好的？这个想法行不行？"

这个 framing 如果成立，比当前的任何说法都更有力——当前切换定位是"低 SNR 区避险鲁棒性补丁"（不变量 8），新 framing 是"跨工况自动选优"。

用户原话决定开专门对话深挖：

> "要不咱们开个对话专门研究一下？这个要是能行那比我们之前想的说法有力多了？只要真的能正确切换。交接文档一定要把现状写全。"

**我已做了数据核查，核心发现如下（新对话必须先消化这些再推进）**：

## 下一步干什么

新对话要回答的核心问题：**「切换跨场景自动选优」framing 能不能成立？需要什么条件成立？**

研究路径建议：
1. 先读本文件 §现状写全（特别是「关键数据矛盾」和「切换实际选了什么」）
2. 判断：当前切换判据（γ_eff 阈值 13dB）能不能改进，让它在所有场景都选对（像 strong 场景那样 7/7 正确）？
3. 如果能改进判据 → framing 成立，重写切换叙事（从"鲁棒性补丁"升级为"跨工况自适应"）
4. 如果不能（物理/工程限制）→ 回到现状 framing

**关键约束**：这是 GW Step 4a 维度 D 内的工作（A4 PASS 待 Go）。如果涉及"改判据重跑切换实验"= 回 step4a-mve-execution 专题，不在写作专题跑（守 FR-22）。但如果只是"分析现有数据 + 调判据参数不重跑"可以在本对话做。

## 纪律（和下一步直接相关的约束）

1. **守路 1**：不调参让数字变大（R003 已判天花板），但"改判据让切换选对"不是调参冲数字——是改进算法逻辑。需要判断这是否越界（如果是新算法 = 回 step4a 专题）
2. **D004 口径**：报任何增益前必查 `fair_comparison.py:109`（fair = naive + 1.249dB）。本次发现 DA BER 有两个口径（data/full），fair_gain 用的是 data 口径 + overhead 补偿，逻辑自洽
3. **不变量 8**：切换代码三 bug 已修复重跑（D002/H003）。旧 +0.27~0.48dB 永久禁用。当前可用数字 = vs 固定 NDA 低 SNR +1.3~2.3dB
4. **数据真实**：不 cherry-pick。新 framing 如果只在 data 口径成立（非公平），必须诚实标注

---

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（特别是 #7 故事根 / #8 切换数字 / #9 口径方向）
- [ ] 已验证本文件 §「切换实际选了什么」的表格（从 `_a4_switch_30seed_fixed.json` 核查 strong 场景 7/7 选对）
- [ ] 已验证 §「关键数据矛盾」的 DA BER 双口径（`da_ber_mean_full` vs `da_ber_mean_data`，比值 = 1024/768 = 1.333）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on（step4a-mve-execution，切换实验的产出源）
- [ ] 已确认当前范围未违反"明确不含"（不改算法/不跑新实验——除非回 step4a 专题）

---

## 现状写全（交接核心，新对话必读）

### 1. 关键数据矛盾：DA BER 有两个口径

**这是本次调查最重要的发现。两个数据源报的 DA BER 不同，导致 DA vs NDA 胜负翻转。**

| 口径 | 分母 | DA BER (strong@15dB) | 含义 | 谁用 |
|---|---|---|---|---|
| **data** | 768 bit（只 data 位）| 0.172 | DA 错误数/768，标准 info-BER | main30seed `da_ml_ber_mean` |
| **full** | 1024 bit（全块）| 0.129 | DA 错误数/1024，公平对比 | switchJSON `da_ber_mean_full` |

- **data / full = 1024/768 = 1.333** = pilot overhead（DA 每 4 符号插 1 pilot = 25% 开销）
- NDA BER 两个数据源完全一致（NDA 不发 pilot，full==data）
- 两个数据源的**原始错误计数位完全相同**（16 位有效数字一致），只是分母不同

**代码证据**：`_a4_switch_30seed_fixed.py:171-213`
- `da_full = e_d / n_blk_bits_full`（e_d = DA 在 data 位的错误数，n_blk_bits_full = N×1024）
- `da_data = e_d / n_data_bits`（n_data_bits = N×768）
- NDA: `e_n / n_blk_bits_full`（NDA 无 pilot，full==data）

**fair_gain 用哪个口径**：`fair_comparison.py:98-100` 输入的 `da_ml_ber` 是 data 口径（main30seed 存的），但 L109 `gain_hdfec = (s_da_d + pilot_overhead_db) - s_nda_d` 把 overhead 加回去补偿了。所以 fair_gain 逻辑自洽——+1.26dB（strong, naive）是真实的总功率增益。

### 2. 你的 framing 在两个口径下的成立性

| 口径 | NDA 赢的场景 | 「跨场景自动选优」成立？ |
|---|---|---|
| **data 口径**（768bit，DA BER 偏高）| AWGN 8/8 + weak/mod 4/7 + strong 5/7 + uplink 5-7/7 | ✅ 多场景有交叉，看起来成立 |
| **full 口径**（1024bit，公平对比）| strong 2/7 + up_mod 1/7 + up_str 3/7（仅 24-26dB 高 SNR）| ❌ 基本不成立（DA 几乎全场景赢）|

**风险**：如果用 data 口径画 BER 图支持你的 framing，审稿人一旦要求公平对比（full 口径），DA 几乎全程赢 NDA，framing 破。

### 3. 切换方案实际选了什么（公平口径 full）

| 场景 | 低 SNR 段 | 高 SNR 段 | 选对率 | vs 固定最优(DA) |
|---|---|---|---|---|
| AWGN | 全程 NDA ❌ | 全程 NDA ❌ | **0/8** | +14% BER（最差）|
| Weak | DA（5-15dB）| NDA（20-26dB）| 3/7 | +9% |
| Moderate | DA（5-15dB）| NDA（20-26dB）| 3/7 | +6% |
| **Strong** | DA（5-22dB）| NDA（24-26dB）| **7/7** ✅ | **-0.1%（≈理想）**|

**核心发现**：切换在 strong 场景完美工作（7/7 正确，≈理想切换），但在弱湍流场景判据失效。原因：判据用 γ_eff 阈值 13dB（`meta.gamma_eff_th=13.0`），弱湍流下 γ_eff 普遍 > 13dB 所以总选 NDA，但弱湍流下 DA（公平口径）其实更好。

### 4. 「如果能正确切换」的潜力

如果改进判据让所有场景都像 strong 那样 7/7 选对：
- 切换总 BER = 理想切换 = 每点选 min(DA,NDA)
- 这能实现"跨工况自动选优"——每场景每 SNR 都用最优方法

**这是你说的"比之前想法有力"的核心**。但需要研究：
- 当前判据（固定 γ_eff 阈值 13dB）为什么在弱湍流失效？
- 有没有场景自适应的判据（如 γ_eff 阈值跟 CV 变化系数联动）？
- 这算"调参"（守路 1 禁止）还是"改算法逻辑"（合法）？

### 5. Fig.4 现状

Fig.4 当前画法（`plot_fig4_crossover.py` v3）：单图 6 条 BER 曲线（3 场景 × DA/NDA），颜色区分场景（weak 蓝/mod 琥珀/strong 朱红），线型区分方法（DA 实/NDA 虚），crossover 标在交叉处。

**注意**：Fig.4 用的是 main30seed 的 data 口径 DA BER。如果切换到 full 口径，crossover 位置会大幅右移（NDA 赢区缩到只有 strong/uplink 高 SNR），Fig.4 的"crossover 随湍流左移"趋势会弱化。新对话需要决定 Fig.4 用哪个口径。

### 6. 数据文件位置

- 切换 30seed：`explore/nda-awgn-tracking-sandbox/_a4_switch_30seed_fixed.json`（含 `da_ber_mean_full` + `da_ber_mean_data` + `nda_ber_mean` + `switch_ber_mean`）
- BER 主实验：`results/sc_nda_ml_main_30seed/_main_experiment_30seed.json`（DA 用 data 口径）
- 口径代码：`simulator/fair_comparison.py:84-150`（`analyze_fair_gain` 函数）
- 切换代码：`explore/nda-awgn-tracking-sandbox/_a4_switch_30seed_fixed.py`（判据逻辑在 L171-213）
- fair_gain 汇总：`results/sc_nda_ml_main_30seed/_fair_gain_summary_30seed.json`

---

## 接口变更（如有代码改动）

无代码改动（本对话只产图表脚本 + 分析，不改算法代码）。

## 失败数据附录（如涉及路线失败）

无新路线失败。但本次发现切换判据在弱湍流失效（AWGN 0/8 选对）是一个**已存在的缺陷**，不是新失败——D002 记录的"切换无全场景增益"本质上就是这个判据失效的表现。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| 切换判据弱湍流失效 | 切换应跨场景自动选优 | AWGN 0/8 选对，weak/mod 3/7 | 本对话研究改进判据 |
| DA BER 双口径 | BER 应统一口径 | main30seed 用 data，switchJSON 用 full | 新对话决定正文/图用哪个口径 |
| Fig.4 口径选择 | 图应公平对比 | 当前用 data 口径（crossover 明显）| 新对话决定是否改 full 口径 |

## 下一轮

1. 读本文件 §现状写全（特别是「切换实际选了什么」7/7 表 + 「DA BER 双口径」）
2. 判断核心问题：改进判据让切换跨场景选对，算"调参"（禁止）还是"改算法"（合法但回 step4a）？
3. 如果合法 → 研究场景自适应判据（如 CV 联动 γ_eff 阈值），在现有 30seed 数据上验证能否提升选对率
4. 如果选对率能提到全场景 ≥6/7 → framing 成立，重写切换叙事
5. 如果不能 → 回到现状 framing（切换 = low-SNR 避险鲁棒性补丁），Fig.4 保持 crossover 机制图
