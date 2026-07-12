# [F001] 力度第二轮对照（F1）+ 图表定稿（F2）——战役收尾

> 2026-07-12 | 阶段：writing-campaign §2 收尾（D-F1F2，战役最后一个对话单元）| 状态：定稿
> 来源: H012 交接 | 标尺: R010 力度基准表 20 条 + 图表专项 | 正文: W001（§I/§II）+ W002（§III/§IV）+ W003（§V/Abstract）

## 调研问题

F1 拿 R010 力度基准表逐点对照全篇正文，看每个技术点讲多了还是少了；F2 每图标"表达什么论点"+ 画法 + 数据来源 + 对齐 R010 图表力度专项。修正原则：**只调力度和措辞，不改贡献/数字/口径/framing**。

## 发现

---

## F1：力度第二轮对照

### F1-A：R010 20 条基准逐条对照

每条格式：`[R010 基准行 | 正文实际 | 判定（对齐/多了/少了）| 修正动作]`

#### §I Introduction

| # | R010 基准 | 正文实际（W001 §I）| 判定 | 修正动作 |
|---|---|---|---|---|
| 1.1 | 背景介绍：1-2 段 ~8-15 行（对齐 Panasiewicz/Paillier）| 3 段（背景 2 段 + 贡献 1 段）共 ~15 行 | **对齐**（偏上限但段落分明）| 不动。3 段 = 背景铺陈 2 段（对齐 Paillier 3 段）+ 贡献 1 段，未超 15 行 |
| 1.2 | 贡献声明：散文式 2-3 句不用 bullet（5/5 篇）| 散文式 3 句（propose → selects → yielding），无 bullet | **对齐** | 不动 |
| 1.3 | 问题动机引出：1-2 句点出 DA/NDA trade-off gap | 第 2 段 2 句（DA 低 SNR 准 + 1.25dB 罚 / NDA 省带宽 + squaring loss）| **对齐** | 不动 |

#### §II System Model

| # | R010 基准 | 正文实际（W001 §II）| 判定 | 修正动作 |
|---|---|---|---|---|
| 2.1 | 信道模型：给 GG 模型名 + 块结构不给完整 PDF（1 段 + 1-2 公式）| "Gamma-Gamma block-fading channel [Al-Habash 2001]" + 块结构 N_blk=100 + αβ 值，**无 PDF** | **对齐** | 不动 |
| 2.2 | 帧结构-信号模型：文字描述 + pilot overhead 数字（1.25dB）| r_k 信号模型公式 + "one pilot every four symbols ... 1.25 dB SNR penalty" | **对齐** | 不动 |
| 2.3 | 估计器数学表述：直接给结论级（DA/NDA 进 §III）| SM 不放 DA/NDA 公式（留 §III）| **对齐** | 不动 |

#### §III Method

| # | R010 基准 | 正文实际（W002 §III）| 判定 | 修正动作 |
|---|---|---|---|---|
| 3.1 | 切换机制描述：文字 + 框图，不用伪代码（5/5 篇无伪代码）| 切换规则文字 "select θ̂_DA when γ_blk < γ_th, else θ̂_NDA"，无伪代码 | **对齐** | 不动 |
| 3.2 | 创新点定位：1-2 段说明，弱声明（对齐 Johst）不夸"新算法" | "rather than introducing a new estimator or a new closed-loop component; it adapts ... to the locally prevailing SNR" | **对齐**（弱声明到位）| 不动 |

**公式专项**：DA/NDA/per-block SNR 三公式直接给结论级（对齐 Panasiewicz），不推导（squaring loss 引 V&V 1983 文字结论）。**对齐** ✓

#### §IV Results

| # | R010 基准 | 正文实际（W002 §IV）| 判定 | 修正动作 |
|---|---|---|---|---|
| 4.1 | BER 曲线呈现：主图纵轴不硬凑 1e-5（对齐 Paillier）+ AWGN 理论线隐式 baseline（对齐 Johst）| §IV-A "plotted down to the minimum reliably estimable level"（中性措辞）+ "AWGN reference, included as an implicit baseline" | **对齐**（纵轴 TBD 标记区，措辞中性）| 不动（TBD 导师定）|
| 4.2 | 增益数字报法：正文 dB + 1 张增益汇总表（Tab.1 增量亮点）| §IV-B 正文报 dB + Tab.1 占位 "summarizes the net SNR gain" | **对齐** | 不动 |
| 4.3 | baseline 对比：DA/NDA 两曲线同图 + 文字段落说明，不专列对比节（5/5 篇无对比节）| §IV-A DA/NDA 曲线同图（Fig.2）+ 文字说明各自优势区，无对比专节 | **对齐** | 不动 |

#### §V Conclusion

| # | R010 基准 | 正文实际（W003 §V）| 判定 | 修正动作 |
|---|---|---|---|---|
| 5.1 | Conclusion：1 段 3-5 句（对齐 Johst/Le Bidan 一段式）| 1 段 3 句（复述贡献 + 弱湍流归零局限 + future）| **对齐** | 不动 |

#### 图表专项（F2 详查，此处先核对数量）

| 项 | R010 基准 | 正文实际 | 判定 |
|---|---|---|---|
| 图数 | 4-6 图（3/5 篇 6 张主流）| Fig.1-4 共 4 图 | **对齐**（在 4-6 范围内）|
| 表数 | 0-2 表（4/5 篇 0 表，加 1 表是增量亮点）| Tab.1 共 1 表 | **对齐**（增量亮点）|

**F1-A 总结**：R010 20 条基准 + 公式/图表专项，**全部对齐**。无"讲多了"或"讲少了"的硬性偏差——力度在 W1-W5 起草时已严格对齐 R010。F1-A 不触发正文修正。

---

### F1-B：8 条已知待查项处理

#### ① Intro [APCCAS 2022] 引用偏弱

**问题**：W001 §I 第 1 段末 "Carrier phase recovery (CPR) is therefore an essential block ... [APCCAS 2022][B11]"。句式参照 writing-patterns §5.7（来自 APCCAS 2022）没问题，但 APCCAS 2022 是 FPGA BPS 实现论文（方向相关度"中"），内容支撑 "CPR essential block" 偏弱。

**判定**：**多了**（引用不对口）

**修正**：删 [APCCAS 2022]，保留 [B11]（B11 是 NDA-ML 方法源头，L9 直接讲 CPE 是核心，对口）。句式 "essential block" 是领域通用 claim（writing-patterns §5.7 APCCAS 原句），删引用不影响句式合法性。

**替换**（W001 §I 第 1 段末）：
- 旧：`... introduced by the laser linewidth and the turbulent channel [APCCAS 2022][B11].`
- 新：`... introduced by the laser linewidth and the turbulent channel [B11].`

#### ② "single-estimator baseline" 不在术语表

**问题**：W002 §IV-B 末 "recovering the gain the single-estimator baseline forgoes"。R011 术语表无 "single-estimator baseline"。

**判定**：**多了**（自造合成短语，撞不变量 6 黑话禁令边缘）

**修正**：换描述性表达 "either estimator used alone"（非新术语，纯描述）。

**替换**（W002 §IV-B 末）：
- 旧：`... recovering the gain the single-estimator baseline forgoes whenever the two estimators disagree<!-- TBD ... -->.`
- 新：`... recovering the gain that either estimator used alone would forgo whenever the two estimators disagree<!-- TBD ... -->.`

#### ③ 26/29 在 Method+Results 各一次

**问题**：W002 §III 末 "selecting the locally optimal estimator in 26 of 29 operating points" + §IV-B 末 "the scheme selects the locally optimal estimator in 26"。Intro+Conclusion+Abstract 各一次是必要的（贡献声明/复述），Method+Results 重复。

**判定**：**多了**（Method 末那次可精简，留 §IV-B 数据出处）

**修正**：§III 末去掉 "selecting the locally optimal estimator in 26 of 29 operating points"，改为前瞻性表述（不报数字，把数字留 §IV-B 兑现）。这样 Method 讲机制，Results 讲数字，分工清晰。

**替换**（W002 §III 末）：
- 旧：`... it adapts an existing DA/NDA choice to the locally prevailing SNR, selecting the locally optimal estimator in 26 of 29 operating points.`
- 新：`... it adapts an existing DA/NDA choice to the locally prevailing SNR; the fraction of operating points in which this selection recovers the lower-BER estimator is quantified in Section IV-B.`

**注**：此修正联动 ⑤（"locally optimal" hedging）—— §III 末不再出现 "locally optimal estimator"，故 ⑤ 的 hedging 只需在 Intro/Results/Conclusion/Abstract 四处处理。

#### ④ 3 个 TBD 标记区

**问题**：W002 §IV-A 纵轴范围(D003) / §IV-A 1e-5 解读措辞 / §IV-B 标题数字口径(D004)。

**判定**：**F1 不碰**（导师反馈后处理），保持中性措辞 + 1.85 dB naive 锁定。

**动作**：不动。清单移交 H013 + 导师反馈后集中处理。

#### ⑤ "locally optimal estimator" 措辞风险（优先处理）

**问题**：29 个点里 3 个没选对（strong 高 SNR），严格说不是全点 "locally optimal"。五处正文（Intro/§III 末/§IV-B/Conclusion/Abstract）都用 "selects/selecting the locally optimal estimator in 26 of 29 operating points"。**最容易被审稿人挑**——"26 of 29" 本身承认 3 个没选对，却说 "locally optimal"，逻辑瑕疵。

**判定**：**多了**（措辞过强，逻辑瑕疵）

**修正策略**：保留 "26 of 29 operating points"（这是数据事实，R008 锁定），但把 "locally optimal estimator" 软化为 "the estimator with the lower BER" / "the locally better estimator"——这是可验证的客观事实（per-block 选 BER 低的那法），不声称"最优"。

**逐处替换**：
- **Intro 贡献句（W001 §I 第 3 段）**：
  - 旧：`The scheme selects the locally optimal estimator in 26 of 29 operating points, yielding ...`
  - 新：`The scheme selects the estimator with the lower bit error rate in 26 of 29 operating points, yielding ...`
- **§IV-B 末（W002）**（③ 已把 §III 末去掉，故此处保留但软化）：
  - 旧：`... the scheme selects the locally optimal estimator in 26, recovering ...`
  - 新：`... the scheme selects the lower-BER estimator in 26 of the 29 points, recovering ...`
- **Conclusion（W003 §V）**：
  - 旧：`The scheme selects the locally optimal estimator in 26 of 29 operating points, yielding ...`
  - 新：`The scheme selects the estimator with the lower bit error rate in 26 of 29 operating points, yielding ...`
- **Abstract（W003）**：
  - 旧：`The scheme selects the locally optimal estimator in 26 of 29 operating points, yielding ...`
  - 新：`The scheme selects the estimator with the lower bit error rate in 26 of 29 operating points, yielding ...`

**注**：R008 关键短语原话是 "selecting the locally optimal estimator in 26 of 29 operating points"。软化后语义不变（选 BER 低的 = 选局部更优的），但措辞更严谨可验证。**这是对 R008 措辞的精化（hedging），不是推翻 R008 的切换 framing**——切换仍是"自适应选优"，只是"选优"的措辞从主观"optimal"改为客观"lower BER"。

#### ⑥ Conclusion 跟 Intro 贡献句逐字重复

**问题**：W003 §V 第 1 句 "In this paper, we proposed a per-block SNR-driven estimator switching scheme that selects, for each fading block of a Gamma-Gamma satellite-to-ground channel, between a data-aided (DA) and a non-data-aided (NDA) carrier phase estimator." 跟 Intro 贡献句（W001 §I 第 3 段）几乎一字不差。

**判定**：**多了**（逐字重复，读感差；R010 §5 Johst/Le Bidan Conclusion 是换角度复述非逐字）

**修正**：Conclusion 从结果倒推方法（"to exploit this, we ..."），避免逐字重复 Intro 的"we propose"开头。

**替换**（W003 §V 第 1 句）：
- 旧：`In this paper, we proposed a per-block SNR-driven estimator switching scheme that selects, for each fading block of a Gamma-Gamma satellite-to-ground channel, between a data-aided (DA) and a non-data-aided (NDA) carrier phase estimator.`
- 新：`To exploit the complementary SNR regions in which the data-aided (DA) and non-data-aided (NDA) carrier phase estimators each excel, this paper introduced a per-block SNR-driven switching scheme that selects, for each fading block of a Gamma-Gamma satellite-to-ground channel, the estimator with the lower bit error rate.`

**联动**：此句已含 ⑤ 的软化（"the estimator with the lower bit error rate"），故 Conclusion 第 2 句（⑤ 替换）的 "selects the locally optimal estimator" 需相应调整——第 1 句已说"selects the estimator with the lower BER"，第 2 句直接接 "In 26 of 29 operating points this selection coincides with the lower-BER estimator, yielding ..."。

**Conclusion 替换后整段**（W003 §V）：
> To exploit the complementary SNR regions in which the data-aided (DA) and non-data-aided (NDA) carrier phase estimators each excel, this paper introduced a per-block SNR-driven switching scheme that selects, for each fading block of a Gamma-Gamma satellite-to-ground channel, the estimator with the lower bit error rate. In 26 of 29 operating points this selection coincides with the lower-BER estimator, yielding a net SNR gain of up to 1.85 dB in strong turbulence (naive, net of pilot overhead)¹, while the gain narrows toward zero ($+0.09$/$+0.18$/$+0.19$ dB, within the $30$-seed confidence interval) in weak turbulence and AWGN, where the two estimators perform nearly identically. Future work is underway to strengthen the switching criterion, to extend the evaluation to additional turbulence regimes, and to validate the scheme on uplink experimental data.

#### ⑦ Abstract 开头句略平

**问题**：W003 Abstract 第 1 句 "Coherent free-space optical links between satellites and optical ground stations rely on carrier phase recovery to track the laser-induced and turbulence-induced phase under Gamma-Gamma block fading." 事实陈述但不够抓人。

**判定**：**少了**（开头缺问题压力，对齐 writing-patterns §5.4 MWP 2022 三段式"兴起→动因→However 转折"会更抓人）

**修正**：从"湍流下 CPR 困难"切入，加问题压力。但 Abstract 篇幅紧（1 段 4 句），不能展开——只调第 1 句的切入角度。

**替换**（W003 Abstract 第 1 句）：
- 旧：`Coherent free-space optical links between satellites and optical ground stations rely on carrier phase recovery to track the laser-induced and turbulence-induced phase under Gamma-Gamma block fading.`
- 新：`Coherent free-space optical links between satellites and optical ground stations must track a rapidly varying carrier phase induced by laser linewidth and Gamma-Gamma atmospheric turbulence, making carrier phase recovery a critical receiver function.`

（"must track a rapidly varying ... making ... critical" 比 "rely on ... to track" 更有压力感，对齐 writing-patterns §5.2 "severely degrading" 的问题压力基调）

#### ⑧ §III "enjoys high accuracy" / "known noiselessly in modulation"

**问题**：W002 §III 第 1 段 "The DA estimator enjoys high accuracy at low SNR since the pilot is known noiselessly in modulation"。"enjoys" 口语化；"known noiselessly in modulation" 绕（noiselessly 修饰 known，语义不清）。

**判定**：**多了**（措辞口语化 + 绕）

**修正**：enjoys→achieves（中性动词）；known noiselessly→known exactly at the receiver（清晰）。

**替换**（W002 §III 第 1 段）：
- 旧：`The DA estimator enjoys high accuracy at low SNR since the pilot is known noiselessly in modulation, but spends ...`
- 新：`The DA estimator achieves high accuracy at low SNR since the pilot symbol is known exactly at the receiver, but spends ...`

---

### F1-C：修正汇总

| # | 待查项 | 判定 | 触发修正？| 改动文件 |
|---|---|---|---|---|
| ① | Intro [APCCAS 2022] 引用 | 多了 | ✅ 删引用 | W001 §I |
| ② | "single-estimator baseline" | 多了 | ✅ 换描述 | W002 §IV-B |
| ③ | 26/29 在 Method+Results 重复 | 多了 | ✅ §III 末精简 | W002 §III 末 |
| ④ | 3 个 TBD 标记区 | — | ❌ 不碰（导师定）| — |
| ⑤ | "locally optimal" 措辞风险 | 多了 | ✅ 四处软化 | W001 §I / W002 §IV-B / W003 §V / W003 Abstract |
| ⑥ | Conclusion-Intro 逐字重复 | 多了 | ✅ Conclusion 换角度 | W003 §V |
| ⑦ | Abstract 开头略平 | 少了 | ✅ 加问题压力 | W003 Abstract |
| ⑧ | "enjoys" / "known noiselessly" | 多了 | ✅ 措辞中性化 | W002 §III |

**共 7 项触发正文修正**（①②③⑤⑥⑦⑧），④ 不碰。修正后 26/29 + 1.85 dB naive 数字不动，切换 framing 仍统一"自适应选优"（⑤ 是 hedging 非推翻），TBD 不碰。

---

## F2：图表定稿

每图一段：**论点**（这张图表达什么）+ **画法**（怎么画）+ **数据来源** + **对齐 R010 图表专项**。基于 S006 已有四张样图，F2 只定规格不实际画。

### Fig.1 系统框图

- **论点**：系统架构——相干 FSO 接收机前端 + DA/NDA 双估计器并行 + per-block SNR 测量 + 切换选择器（γ_blk < γ_th ? DA : NDA）。一图讲清"系统在哪儿做切换"。
- **画法**：S006 已有 SVG。**检查项**：框图必须显式画出切换判据框（"γ_blk < γ_th ?" 判决节点 → 选 θ̂_DA 或 θ̂_NDA），不能只画两条平行估计器支路。这是本文贡献的可视化锚点。接收前端（光电转换 + 匹配滤波）→ 分两路：DA 支路（pilot 提取 + 公式1）+ NDA 支路（升 M₀ 幂 + 公式2）→ per-block SNR 测量（公式3）→ 切换选择器（γ_th 判决）→ 相位补偿输出。
- **数据来源**：无（框图，不含数据）
- **对齐 R010**：§3.1 "文字 + 框图，不用伪代码"——Fig.1 是切换机制的框图载体，与 §III 文字描述互补。对齐 Johst Fig.1 帧结构框图 + Le Bidan 多框图风格。

### Fig.2 BER 主图

- **论点**：DA/NDA 各自 BER vs SNR 分场景 + crossover 自然呈现（§IV-A 影响分析的载体）。一图讲清"湍流怎么影响两法各自的性能 + 两法各有优势区"。
- **画法**：S006 已有 3×2 纵向 6 子图（3 下行 weak/mod/strong + 2 上行 up_mod/up_str + AWGN）。每子图：DA BER 曲线 + NDA BER 曲线 + AWGN 理论线（隐式 baseline，对齐 Johst）+ HD-FEC 门限水平线（3.8e-3）。
  - **纵轴 TBD**（导师定，D003）：AWGN/weak/moderate 可到 1e-5；strong/uplink 最低 ~1e-4~1e-3（H002 实测）。**F2 设计时纵轴预留**，标"待导师定范围"——画到能画到的（对齐 Paillier），不强凑 1e-5。crossover 点在图中自然可读（两曲线交点）。
  - **横轴**：SNR (dB)，各场景扫描范围见 R012 参数表 A4（AWGN 5-20 / 湍流 5-26 dB）。
- **数据来源**：`projects/simulation/results/sc_nda_ml_main_30seed/` BER 数据（30seed 基准配置）
- **对齐 R010**：§4.1 "BER 主图纵轴不硬凑 1e-5（对齐 Paillier）+ AWGN 理论线隐式 baseline（对齐 Johst）"。6 子图对齐 Johst Fig.3（2 子图）/OECC-PSC Fig.2（3 子图）的多子图惯例。

### Fig.3 净增益方案

- **论点**：净增益量化归因——强湍流/上行显著（+1.26~1.85 dB naive）vs 弱湍流归零（+0.09/0.18/0.19，诚实）。一图讲清"切换的增益在哪些场景兑现"。
- **画法**：S006 已有方案 B（双线：fair 总 + naive 去导频）。**检查项**：主报 naive（D004），强湍流 3 行（strong/up_mod/up_str）高亮，弱湍流 3 行（awgn/weak/mod）归零诚实标注。可考虑柱状图（6 场景 × naive 增益）或双线图（fair vs naive 两线跨 6 场景）。**注**：若与 Tab.1 信息重复，可考虑 Fig.3 改为"切换 vs 固定 NDA 低 SNR 避险增益"（+1.3~2.3 dB，R012 #5）避免与 Tab.1 冗余——**待 F2 画时定**，看哪个论点更需图载体。
- **数据来源**：`_fair_gain_summary_30seed.json`（fair/naive 两口径，已代码行核验 fair=naive+1.249）
- **对齐 R010**：§4.2 "正文 dB + 1 张增益汇总表（Tab.1）"——Fig.3 是 Tab.1 的可视化补充（可选，若 Tab.1 够清晰可省 Fig.3 改画别的）。

### Fig.4 crossover

- **论点**：切换跨场景自动选优——data 口径多场景 BER 曲线叠加，crossover 点视觉呈现（weak 17.9 / mod 16.8 / strong 10.7 dB）。一图讲清"切换判据 γ_th 随湍流自动左移"。
- **画法**：S006 已有 v3 单图 6 条 BER 曲线叠加（data 口径）。**crossover 只呈现数据不附物理归因**（R009 不变量 7）——图本身**不带解释性标注**（如"左移是因为..."），只在 crossover 点标 SNR 数值（17.9/16.8/10.7 dB）。可加箭头标示左移趋势（纯数据观察，非物理归因）。
- **数据来源**：crossover weak 17.9 / mod 16.8 / strong 10.7 dB（R012 #8，data 口径线性插值交叉点）
- **对齐 R010**：§4.1 "crossover 在图中自然呈现" + §4.3 "DA/NDA 两曲线同图对比"。Fig.4 是切换"自适应选优"framing（R008）的可视化锚点。

### Tab.1 增益汇总

- **论点**：强湍流/上行净增益量化（增量亮点，4/5 篇 0 表，加 1 表强化数字呈现）。一表讲清"切换在强湍流/上行兑现多少 naive 增益"。
- **画法**：只强湍流 3 行 naive（strong +1.26 / up_mod +1.19 / up_str +1.85，R010 §4.2）。**考虑加列增加信息密度**（双栏下 3 行单薄）——建议列：场景 | α,β | 净增益 naive (dB) | 净增益 fair (dB) | 备注。fair 列作对照（透明呈现两口径，不藏），naive 列加粗（主报）。弱湍流 3 行可放备注或脚注（"+0.09/0.18/0.19 dB，CI 重叠归零"诚实标注）。**列名**："net gain (dB)"（R011 #34）。
- **数据来源**：R012 P2-B #1-3（strong/up_mod/up_str naive）+ #4（弱湍流归零）
- **对齐 R010**：§4.2 "正文报关键 dB + 1 张增益汇总表（Tab.1，只放强湍流 3 行 naive 口径）"——增量亮点。fair 列作透明对照是诚实底线（不变量 3），不违背"主报 naive"（naive 列加粗）。

---

## F2 图表力度对齐 R010 图表专项

| 项 | R010 基准 | F2 定稿 | 对齐？|
|---|---|---|---|
| 图数 | 4-6 图（3/5 篇 6 张主流）| Fig.1-4 共 4 图 | ✅（在 4-6 范围内，Fig.3 可选）|
| 表数 | 0-2 表（4/5 篇 0 表，加 1 表增量亮点）| Tab.1 共 1 表 | ✅（增量亮点）|
| 图风格 | 多子图主流（2-6 子图）| Fig.2 6 子图 / Fig.4 单图叠加 | ✅ |
| crossover | 图中自然呈现（§4.1）| Fig.4 crossover 点标数值不带归因 | ✅（R009 只呈现数据）|
| BER 纵轴 | 不硬凑 1e-5（对齐 Paillier）| TBD 导师定，画到能画到的 | ✅（中性）|
| AWGN baseline | 隐式理论线（对齐 Johst）| Fig.2 每子图加 AWGN 理论线 | ✅ |
| HD-FEC 门限 | BER 基准线 | Fig.2 加 3.8e-3 水平线 | ✅ |

**F2 总结**：5 项图表定稿（Fig.1-4 + Tab.1），论点/画法/数据/R010 对齐全清。图数 4（在 4-6 范围）+ 表 1（增量亮点），对齐 R010 图表专项。**F2 不实际画图**（S006 已有样图），只定规格供后续画图/转 LaTeX 用。

---

## 交叉检查（F1 修正后）

### ✅ 检查 1：术语仍跟 R011 一致（修正后）

| 修正项 | 修正后用词 | R011 对齐 | 一致？|
|---|---|---|---|
| ② "single-estimator baseline" → "either estimator used alone" | 描述性短语，非术语 | 不撞术语表（纯描述）| ✅ |
| ⑤ "locally optimal estimator" → "estimator with the lower BER" / "lower-BER estimator" | 描述性（选 BER 低的）| 不撞术语表（非新术语）| ✅ |
| ⑧ "enjoys"→"achieves" / "known noiselessly"→"known exactly at the receiver" | 标准动词 | 中性化，无新词 | ✅ |

**自造词残留检查**（修正后）：fair_gain / A4 / MSM / 伪地板 / 鲁棒性补丁 / single-estimator baseline / locally optimal estimator：❌ 全文无（②⑤ 修正已清除）✅

### ✅ 检查 2：数字仍跟 R012 一致（修正后）

| 数字 | 修正后仍出现？| 口径 | 一致？|
|---|---|---|---|
| 26 of 29 operating points | ✅ Intro/§IV-B/Conclusion/Abstract 四处（③ 删 §III 末，剩四处）| data | ✅ |
| 1.85 dB naive | ✅ Intro/§IV-B/Conclusion/Abstract 四处 | naive 标脚注 | ✅ |
| 1.26 / 1.19 dB | ✅ §IV-B（不动）| naive | ✅ |
| 0.09/0.18/0.19 | ✅ §IV-B + Conclusion（不动）| naive CI 重叠 | ✅ |
| crossover 17.9/16.8/10.7 | ✅ §IV-A（不动）| data | ✅ |
| 1.3~2.3 dB | ✅ §IV-B（不动）| net | ✅ |

**数字未变**——F1 只调措辞力度，26/29 + 1.85 dB naive 五处→四处（③ 删一处）但数字值和口径不动 ✅

### ✅ 检查 3：切换 framing 仍统一"自适应选优"（R008，修正后）

| 位置 | 修正后 framing | 一致？|
|---|---|---|
| Intro 贡献句 | "selects the estimator with the lower bit error rate in 26 of 29 operating points" | ✅ 自适应选优（⑤ hedging：lower BER = 局部更优，客观化）|
| §III 末 | （③ 删 "selecting the locally optimal estimator in 26 of 29"，改为前瞻引用 §IV-B）| ✅ 仍讲"adapts ... to the locally prevailing SNR"（自适应选优）|
| §IV-B 末 | "selects the lower-BER estimator in 26 of the 29 points" | ✅ 自适应选优 |
| Conclusion | "selects ... the estimator with the lower bit error rate" + "In 26 of 29 operating points this selection coincides with the lower-BER estimator" | ✅ 自适应选优 |
| Abstract | "selects the estimator with the lower bit error rate in 26 of 29 operating points" | ✅ 自适应选优 |

**⑤ hedging 说明**："locally optimal" → "lower BER" 是措辞严谨化（3 个点没选对就不能说"全点最优"），**不是推翻 R008 切换 framing**——切换仍是"per-block SNR 驱动的自适应选优"，只是"选优"的客观依据从主观"optimal"改为可验证的"lower BER"。framing 不变 ✅

**禁用措辞残留**："鲁棒性补丁" / "necessary closed-loop component" / "crossover 物理归因"：❌ 全文无 ✅

### ✅ 检查 4：TBD 标记区不动

| TBD 项 | F1 是否碰 | 状态 |
|---|---|---|
| ④ §IV-A 纵轴范围（D003）| ❌ 不碰 | 保持中性措辞 + TBD 注释 |
| ④ §IV-A 1e-5 解读措辞 | ❌ 不碰 | 保持 TBD 注释 |
| ④ §IV-B 标题数字口径（D004）| ❌ 不碰 | 保持 1.85 dB naive + TBD 注释 |

**3 个 TBD 标记区全未动**，导师反馈后集中处理 ✅

### ✅ 检查 5：F2 图表数对齐 R010

4 图（Fig.1-4）+ 1 表（Tab.1），在 R010 "4-6 图 + 0-2 表"范围内 ✅

**交叉检查全部通过 ✓（5 项）**

---

## 结论

D-F1F2 完成，**写作战役全部完成**。

**F1 力度第二轮**：R010 20 条基准逐条对照**全部对齐**（无硬性多了/少了偏差）；8 条已知待查项处理——7 项触发正文修正（①②③⑤⑥⑦⑧），④（3 个 TBD）不碰导师反馈后处理。修正原则严守：只调力度措辞，不改贡献/数字/口径/framing。⑤"locally optimal"→"lower BER" 是 hedging 非推翻 R008。

**F2 图表定稿**：5 项（Fig.1-4 + Tab.1）规格定稿，论点/画法/数据/R010 对齐全清。图数 4 + 表 1 对齐 R010 图表专项。F2 不实际画图（S006 已有样图），供后续画图/转 LaTeX 用。

**修正落地**：7 项修正已用 Edit 改 W001/W002/W003 对应位置（见下"修正落地记录"）。

## 修正落地记录（Edit 执行）

| # | 文件 | 位置 | 改动 |
|---|---|---|---|
| ① | W001 §I 第 1 段末 | `[APCCAS 2022][B11]` → `[B11]` | 删弱引用 |
| ② | W002 §IV-B 末 | `single-estimator baseline forgoes` → `that either estimator used alone would forgo` | 换描述 |
| ③ | W002 §III 末 | `selecting the locally optimal estimator in 26 of 29 operating points.` → `; the fraction of operating points in which this selection recovers the lower-BER estimator is quantified in Section IV-B.` | 精简 + 前瞻引用 |
| ⑤a | W001 §I 第 3 段 | `selects the locally optimal estimator` → `selects the estimator with the lower bit error rate` | 软化 |
| ⑤b | W002 §IV-B 末 | `selects the locally optimal estimator in 26` → `selects the lower-BER estimator in 26 of the 29 points` | 软化 |
| ⑤c+⑥ | W003 §V 整段 | 第 1 句换角度（从结果倒推）+ "locally optimal" 软化 | 换角度 + 软化 |
| ⑤d+⑦ | W003 Abstract | 第 1 句加问题压力 + "locally optimal" 软化 | 加压力 + 软化 |
| ⑧ | W002 §III 第 1 段 | `enjoys high accuracy ... known noiselessly in modulation` → `achieves high accuracy ... known exactly at the receiver` | 中性化 |

## 对决策的影响

- **不新建 D###**：本轮是力度对照 + 图表定稿（收尾），不改方向/架构决策。
- **⑤ 是 R008 措辞的精化非推翻**："locally optimal" → "lower BER" 是 hedging（3 个点没选对就不能说全点最优），切换 framing 仍统一"自适应选优"。如导师/审稿人质疑此 hedging，回查 R008/S007 data 口径选对率 26/29 的原始讨论。
- **修正全可逆**：每项修正旧文本在 F1-B 各条记录里，如需回退可恢复。

## 范围确认

- 本轮是否在 scope boundary 内：**是**。F1/F2 是 writing-campaign-plan §2 收尾活（力度对照 + 图表规格），在写作专题范围内，不跑实验不进 Contract。

## 后续

**写作战役全部完成**。正文 5 节 + Abstract + F1 修正 + F2 图表规格全齐。

下一步（**等导师反馈 + 投稿准备**）：
1. **等导师 3 项反馈**（卡 Results §IV TBD 标记区）：①10⁻⁵ 底线 A/B（D003）→ 纵轴范围 + 主卖点成立性 ②口径 fair/naive（D004 已倾向 naive）→ 标题数字 ③主对比文献 → 参考文献核心一条
2. **全篇通读**（F1 修正后整体读一遍，检查衔接/读感）
3. **转 LaTeX 投稿格式**（CCISP 双栏，段落调整 + 图表插入 + 参考文献 10-15 篇）

交接见 H013-campaign-complete.md。
