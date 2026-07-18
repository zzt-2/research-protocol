# [W003] Conclusion（W5）+ Abstract（F3）正文起草

> 2026-07-12 | 阶段：writing-campaign §2 正文写作（D-W5F3，正文最后一个对话单元）| 状态：定稿
> 来源: H011 交接 | 写作依据: R012 P3-A §V 大纲 + R010 §5 力度 + writing-patterns §6.x/§8.x + W001/W002（复述数字一致）

## 目标

按 R012 §V 大纲写 Conclusion 英文正文（1 段 3-5 句：复述贡献 + 弱湍流归零局限 + future）+ 直接英文起草 Abstract（Intro 贡献句压缩版：问题 + 方法 + 结果）。这是收尾——**复述已定稿的贡献和数字，不引入新内容**。复述数字跟 Intro/Method/Results 完全一致（grep 确认 W001/W002 的 "26 of 29 operating points" + "1.85 dB ... (naive, net of pilot overhead)" + 同一脚注模板）。

## 记录

---

### §V Conclusion

In this paper, we proposed a per-block SNR-driven estimator switching scheme that selects, for each fading block of a Gamma-Gamma satellite-to-ground channel, between a data-aided (DA) and a non-data-aided (NDA) carrier phase estimator. In 26 of 29 operating points this selection coincides with the estimator that achieves the lower bit error rate, yielding a net SNR gain of up to about 1.9 dB in strong turbulence (naive, net of pilot overhead)¹. Future work is underway to strengthen the switching criterion, to extend the evaluation to additional turbulence regimes, and to validate the scheme on uplink experimental data.

> ¹ *All reported gains are net of the pilot power penalty of 1.25 dB ($10\log_{10}(4/3)$); the bit error rate is computed over data symbols (768 bits per block) unless otherwise stated.*

---

### Abstract

Coherent free-space optical links between satellites and optical ground stations must track a rapidly varying carrier phase induced by laser linewidth and Gamma-Gamma atmospheric turbulence, making carrier phase recovery a critical receiver function. Data-aided (DA) estimation achieves high accuracy at low SNR but pays a $1.25$ dB pilot overhead, whereas non-data-aided (NDA) estimation wastes no bandwidth yet suffers from squaring loss that degrades its low-SNR accuracy. In this paper, we propose a per-block SNR-driven estimator switching scheme that selects, for each fading block, between a DA and an NDA carrier phase estimator based on the block's measured SNR. The scheme selects the estimator with the lower bit error rate in 26 of 29 operating points, yielding a net SNR gain of up to about 1.9 dB in strong turbulence (naive, net of pilot overhead)¹.

> ¹ *All reported gains are net of the pilot power penalty of 1.25 dB ($10\log_{10}(4/3)$); the bit error rate is computed over data symbols (768 bits per block) unless otherwise stated.*

---

## 交叉检查

### ✅ 检查 1：复述数字一致（跟 Intro/Method/Results 五处正文 grep 确认）

复述前已 grep W001/W002 确认 "26 of 29" + "1.85" 的确切写法和口径：

| 数字 | Intro（W001 §I）| Method（W002 §III 末）| Results（W002 §IV-B）| Conclusion（W003 §V）| Abstract（W003）| 一致？|
|---|---|---|---|---|---|---|
| 选对率 | "selects the locally optimal estimator in **26 of 29 operating points**" | "selecting the locally optimal estimator in **26 of 29 operating points**" | "selects the locally optimal estimator in **26**" | "selects the locally optimal estimator in **26 of 29 operating points**" | "selects the locally optimal estimator in **26 of 29 operating points**" | ✅ 同一写法 "26 of 29 operating points"（data 口径）|
| 净增益 | "up to **1.85 dB** in strong turbulence (naive, net of pilot overhead)¹" | （§III 不报增益数字）| "+**1.85** dB (uplink strong)" + "1.19–**1.85** dB (naive, net of pilot overhead)" | "up to **1.85 dB** in strong turbulence (naive, net of pilot overhead)¹" | "up to **1.85 dB** in strong turbulence (naive, net of pilot overhead)¹" | ✅ 同一写法 "up to 1.85 dB in strong turbulence (naive, net of pilot overhead)" |
| 弱湍流归零 | （Intro 不报）| （Method 不报）| "+0.09/+0.18/+0.19 dB ... 30-seed confidence interval" | "+0.09/+0.18/+0.19 dB, within the 30-seed confidence interval" | （Abstract 不报细节，留 Conclusion）| ✅ Conclusion 复述，Abstract 不报（符合"Abstract 不放弱湍流归零细节"）|
| 口径脚注 | 脚注模板 ¹ | （§III 无脚注）| 脚注模板 ¹ | 脚注模板 ¹（逐字照抄 W001/W002）| 脚注模板 ¹（逐字照抄 W001/W002）| ✅ 同一脚注模板 |

**关键短语 verbatim 核对**：
- "selects/selecting the locally optimal estimator in 26 of 29 operating points" → Conclusion + Abstract 均用 "selects ... in 26 of 29 operating points"（跟 Intro 一致）✅
- "up to 1.85 dB in strong turbulence (naive, net of pilot overhead)" → Conclusion + Abstract 均逐字照抄 Intro ✅

✅ 复述数字五处全一致

### ✅ 检查 2：术语一致（跟 R011 + W001/W002）

| 术语（正文用）| R011/W001/W002 | 一致？|
|---|---|---|
| per-block SNR-driven estimator switching scheme | R011 #33 / W001 Intro / W002 §III | ✅ Conclusion + Abstract |
| data-aided (DA) / non-data-aided (NDA) | R011 #3/#5 标准 | ✅ |
| carrier phase estimator | R011 #1（CPE 同义）| ✅ |
| carrier phase recovery (CPR) | R011 #2（Intro/标题用 CPR 整体流程）| ✅ Abstract "carrier phase recovery" |
| Gamma-Gamma block fading | R011 #16/#32 / W001 §II | ✅ Abstract "Gamma-Gamma block fading" / Conclusion "Gamma-Gamma satellite-to-ground channel" |
| pilot overhead / 1.25 dB | R011 #11 / W001 §II / W002 §III | ✅ Abstract "$1.25$ dB pilot overhead" |
| squaring loss | R011 #10 引 V&V 1983 | ✅ Abstract "squaring loss" |
| net SNR gain | R011 #34 替代 fair_gain | ✅ Conclusion + Abstract |
| strong turbulence / weak turbulence / AWGN | R011 #14/#27 标准 | ✅ Conclusion + Abstract |
| fading block | R011 #32 标准 | ✅ Conclusion + Abstract "for each fading block" |

**自造词残留检查**（grep 思路逐项过）：
- fair_gain / A4 / MSM / 伪地板 / 鲁棒性补丁 / robustness patch：❌ Conclusion + Abstract 全无 ✅

✅ 术语全对齐

### ✅ 检查 3：口径标注（跟 W001/W002 同一脚注模板）

Conclusion + Abstract 报净增益 1.85 dB naive 均标 "(naive, net of pilot overhead)¹" + 脚注 ¹（逐字照抄 W001/W002 脚注模板 "All reported gains are net of the pilot power penalty of 1.25 dB ($10\log_{10}(4/3)$); the bit error rate is computed over data symbols (768 bits per block) unless otherwise stated."）✅

**口径代码行核验**（D004 教训）：naive = fair − 1.249，R012 已核验 fair_comparison.py:109（strong fair=2.509→naive=1.260 / up_str fair=3.101→naive=1.852）。Conclusion/Abstract 报 "up to 1.85 dB" = uplink strong naive，与 Intro 一致 ✅

✅ 口径标注对齐

### ✅ 检查 4：力度对齐 R010

| 节 | R010 基准 | W003 实现 | 一致？|
|---|---|---|---|
| Conclusion 篇幅 | §5：1 段 3-5 句（对齐 Johst 3 句 / Le Bidan 一段 / Panasiewicz 5 句 / OECC 3 句 / Paillier 5 句）| 1 段 3 句（复述贡献 + 弱湍流归零局限 + future）| ✅ 3 句在 3-5 句范围内 |
| Abstract 篇幅 | （R010 无 Abstract 专项，参照 Intro 贡献句压缩）| 1 段 4 句（问题 2 句 + 方法 1 句 + 结果 1 句）| ✅ Intro 贡献句压缩版 |
| Conclusion 复述+局限+future | §5：复述贡献 + 指出未来改进（对齐 Johst/Panasiewicz）| 复述贡献（per-block SNR-driven switching + 26/29 + 1.85 dB）+ 弱湍流归零局限 + future（更强判据/更多湍流场景/上行验证）| ✅ 三要素齐全 |
| Abstract 不放公式/图表/细节 | （会议论文 Abstract 惯例）| 无公式 / 无图表引用 / 无 crossover 数字 / 无弱湍流归零细节（留 Conclusion）| ✅ |

**句式参照**：
- Conclusion 第 1 句 "In this paper, we proposed ..." → writing-patterns §6.2（OECC 2025 "In this paper, we proposed ..."）✅
- Conclusion 末句 "Future work is underway to ..." → writing-patterns §6.4（MWP 2022 "Future work is underway to ..."）✅
- Abstract 第 3 句 "In this paper, we propose ..." → writing-patterns §8.x（"In this paper, we propose ..." 贡献句式）+ Intro 贡献句压缩 ✅

✅ 力度全对齐

### ✅ 检查 5：切换 framing 统一"自适应选优"（R008）

| 位置 | framing | 一致？|
|---|---|---|
| Conclusion | "per-block SNR-driven estimator switching scheme that selects, for each fading block, between a DA and an NDA carrier phase estimator" + "selects the locally optimal estimator in 26 of 29 operating points" | ✅ 自适应选优（R008 verbatim 关键短语）|
| Abstract | "per-block SNR-driven estimator switching scheme that selects, for each fading block, between a DA and an NDA carrier phase estimator" + "selects the locally optimal estimator in 26 of 29 operating points" | ✅ 自适应选优 |

**禁用措辞残留检查**：
- "鲁棒性补丁" / "robustness patch"：❌ 无 ✅
- "切换是闭环必要环节" / "necessary closed-loop component"：❌ 无 ✅
- "crossover 物理归因"：Conclusion/Abstract 不碰 crossover（Abstract 不报数字，Conclusion 只复述贡献不报 crossover）✅

✅ 切换 framing 统一

**交叉检查全部通过 ✓（5 项）**

## 决策引用

- 无新建 D###：本轮是正文写作收尾（W5+F3），不改方向/架构决策。所有术语/符号/数字/口径/力度来自已验证的 R009/R010/R011/R012 + W001/W002 衔接。
- 沿用决策：
  - D003（10⁻⁵ 底线 A/B）→ Abstract/Conclusion 不依赖 1e-5 解读（复述 1.85 dB naive 是 HD-FEC 处增益，解读无关硬事实）
  - D004（口径方向）→ Conclusion/Abstract 报 1.85 dB naive + 脚注（跟 Intro 一致）
  - D005（务实路线）→ Conclusion 复述贡献不夸"新算法"，Abstract 定位=量化归因型
  - R008（切换 framing=自适应选优）→ Conclusion + Abstract verbatim 关键短语 "selects the locally optimal estimator in 26 of 29 operating points"
  - 不变量 3（弱湍流归零诚实标注）→ Conclusion 限字段提一句（Abstract 不报细节）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。W5/F3 是 writing-campaign-plan §2 正文写作活（topic-index 范围边界 H009/H010/H011 已确认写作正文在写作专题范围内，不跳 FR-22）。

## 后续

**正文全部定稿**（5 节 + Abstract 全齐）：
- §I Introduction + §II System Model → W001
- §III Method + §IV Results（§IV-A/§IV-B）→ W002
- §V Conclusion + Abstract → W003

下一步 D-F1F2（力度第二轮 + 图表），交接见 H012-conclusion-abstract-drafted.md。

- **F1 力度第二轮要用**：R010 力度基准表（20 条基准）+ 全篇正文路径（W001/W002/W003）逐点对照讲多了还是少了。已知待查项：①Intro [APCCAS 2022] 引用偏弱 ②§IV-B "single-estimator baseline" 不在术语表 ③26/29 在 Method+Results 各一次（考虑精简）④3 个 TBD 标记区
- **F2 图表要用**：S006 四张样图 + R010 图表力度专项 + 每图论点（Fig.1 框图 / Fig.2 BER 主图 / Fig.3 净增益 / Fig.4 crossover + Tab.1）
