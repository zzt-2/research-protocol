# [W002] Method（W3）+ Results（W4）正文起草

> 2026-07-12 | 阶段：writing-campaign §2 正文写作（D-W3W4）| 状态：定稿
> 来源: H010 交接 | 写作依据: R012 P3-A §III/§IV 大纲 + R011 公式清单/符号表 + R010 §3/§4 力度 + R009 逻辑链 + writing-patterns-conference.md + W001（衔接术语/符号/口径/footnote）

## 目标

按 R012 §III 大纲写 Method 英文正文（DA/NDA/per-block SNR 三公式 + 切换规则文字 + 创新点弱声明）+ 按 R012 §IV 两段式大纲写 Results 英文正文（§IV-A 影响分析 + §IV-B 方法增益）。**W4 是导师 3 项反馈（10⁻⁵/口径/baseline）的落点，必须写得"对解读不敏感"**——主体放解读无关硬事实（BER 曲线 + HD-FEC 增益 + crossover + 选对率），标记区放纵轴范围/标题数字/1e-5 解读。术语/符号/口径/footnote 跟 W001 完全衔接。Intro 贡献句承诺的 26/29 + 1.85dB naive 在 W4 Results 兑现。

## 记录

---

### §III Method

We consider two carrier phase estimators that operate independently on each fading block, differing only in how they remove the modulation from the received samples. The data-aided (DA) estimator removes modulation by dividing the received pilot sample $r_p$ by the known pilot symbol $p$, and takes its argument:
$$\hat{\theta}_\text{DA} = \angle(r_p \cdot p^{*}). \tag{1}$$
The non-data-aided (NDA) estimator instead raises every sample in the block to the $M_0$-th power, averages, and scales the resulting argument by $1/M_0$:
$$\hat{\theta}_\text{NDA} = \frac{1}{M_0} \angle\Big(\textstyle\sum_k r_k^{M_0}\Big), \tag{2}$$
where $M_0 = 8$ for $(8,8)$-16APSK (one period per ring). The DA estimator enjoys high accuracy at low SNR since the pilot is known noiselessly in modulation, but spends $25\%$ of the bandwidth on pilots ($1.25$ dB overhead); the NDA estimator wastes no bandwidth yet suffers from squaring loss that degrades its phase-estimation accuracy at low SNR [V&V 1983]. The two estimators therefore dominate in disjoint SNR regions.

To exploit this complementarity, the receiver measures the per-block SNR
$$\gamma_\text{blk} = |h_b|^{2} \, E_s / N_0, \tag{3}$$
i.e., the SNR over a single fading block of $N_\text{blk}$ symbols within which the channel coefficient $h_b$ is constant, and selects the estimator with the lower expected bit error rate: select $\hat{\theta}_\text{DA}$ when $\gamma_\text{blk} < \gamma_\text{th}$, and $\hat{\theta}_\text{NDA}$ otherwise. Here $\gamma_\text{th}$ is the crossover SNR at which the BER curves of the two estimators intersect. The scheme thus performs a per-block, SNR-driven selection between the DA and NDA estimators rather than introducing a new estimator or a new closed-loop component; it adapts an existing DA/NDA choice to the locally prevailing SNR, selecting the locally optimal estimator in 26 of 29 operating points.

---

### §IV Results

#### §IV-A Impact of Turbulence on DA and NDA Performance

Figure 2 reports the bit error rate $P_b$ versus SNR for the DA and NDA estimators across the six considered regimes (weak, moderate, and strong downlink turbulence; moderate and strong uplink turbulence; and the AWGN reference), with BER curves plotted down to the minimum reliably estimable level for each regime<!-- TBD: 纵轴范围待导师定（D003）——AWGN/weak/moderate 可到 1e-5，strong/uplink 最低 ~1e-4~1e-3（H002 实测），是否硬凑 1e-5 待定 -->. The AWGN reference, included as an implicit baseline, shows the largest gap between the two estimators in favor of NDA, since the absence of fading removes the DA estimator's low-SNR advantage. As turbulence strengthens, the DA and NDA curves intersect: the two estimators are each preferable in a distinct SNR region, and the crossover SNR $\gamma_\text{th}$ moves to lower SNR as turbulence grows, decreasing from $17.9$ dB (weak) through $16.8$ dB (moderate) to $10.7$ dB (strong)<!-- TBD: crossover 只呈现数据事实，不附物理归因（R009 不变量 7）——为什么左移没搞清，不解释 -->. Below $\gamma_\text{th}$ the DA estimator yields the lower BER; above it the NDA estimator does. This crossover structure is precisely what the per-block switching rule exploits.

#### §IV-B Gain of the Switching Scheme

Table I summarizes the net SNR gain of the proposed scheme relative to a fixed NDA estimator, measured at the $7\%$ HD-FEC threshold of $3.8 \times 10^{-3}$¹. Two regimes are distinguished. *Low-SNR avoidance:* in the low-SNR region ($\gamma_\text{blk} < \gamma_\text{th}$), selecting the DA estimator avoids the NDA estimator's squaring-loss-driven degradation, yielding a net SNR gain of $1.3$–$2.3$ dB over a fixed NDA estimator (CI lower bounds uniformly positive). *Strong-turbulence net gain:* in the strong-turbulence and uplink regimes the scheme attains a net SNR gain of $1.19$–$1.85$ dB (naive, net of pilot overhead), specifically $+1.26$ dB (downlink strong), $+1.19$ dB (uplink moderate), and $+1.85$ dB (uplink strong). In the weak-turbulence and AWGN regimes the net gain narrows to $+0.09$/$+0.18$/$+0.19$ dB, consistent with zero within the $30$-seed confidence interval; this near-zero gain is reported transparently rather than suppressed. Across all 29 operating points, the scheme selects the locally optimal estimator in 26, recovering the gain the single-estimator baseline forgoes whenever the two estimators disagree<!-- TBD: 标题/数字口径待导师定（D004）——Intro 已锁 1.85 dB naive，如导师要 fair 口径（+1.25 dB → 3.10 dB）或解读 A（BER=1e-5 处）数字，标题与该句需同步调整 -->.

> ¹ *All reported gains are net of the pilot power penalty of 1.25 dB ($10\log_{10}(4/3)$); the bit error rate is computed over data symbols (768 bits per block) unless otherwise stated.*

---

## 交叉检查（6 项 + W001 衔接）

### ✅ 检查 0：跟 W001 衔接（术语/符号/口径/footnote）

| 衔接项 | W001（Intro+SM）| W002（Method+Results）| 一致？|
|---|---|---|---|
| 相位符号 | θ（V&V，注 "(denoted φ in [B11])"）| θ̂_DA / θ̂_NDA（θ 的估计）| ✅ 同 θ 体系 |
| PN 方差符号 | σ²_θ = 2πΔνT_s（注 "= σ²_p in [B11]"）| （§III 不复述，§IV 不碰）| ✅ 不冲突 |
| M₀ | 8（(8,8)-16APSK 每环 8 点）| 8（公式 2 "M₀ = 8 for (8,8)-16APSK"）| ✅ |
| r_k / h_b / N₀ / E_s | §II 定义 | §III 公式 2 用 r_k；公式 3 用 h_b/E_s/N₀ | ✅ |
| pilot overhead 1.25 dB | §II "1.25 dB SNR penalty ($10\log_{10}(4/3)$)" | §III "$25\%$ ... $1.25$ dB overhead"；§IV 脚注 | ✅ |
| net SNR gain 脚注 | §I 脚注 ¹ 模板 | §IV-B 脚注 ¹ 模板（逐字照抄 W001）| ✅ |
| HD-FEC 3.8e-3 | §II "$3.8 \times 10^{-3}$ (7% overhead)" | §IV-B "$7\%$ HD-FEC threshold of $3.8 \times 10^{-3}$" | ✅ |
| Intro 承诺兑现 | §I 贡献句 "26/29 ... up to 1.85 dB (naive)" | §III 末 "26 of 29" + §IV-B "+1.85 dB (uplink strong, naive)" | ✅ 兑现 |
| DA/NDA trade-off | §I 第 2 段 "DA preferable where signal weak, NDA where strong" | §III 第 1 段 "dominate in disjoint SNR regions" | ✅ 一致 |

✅ W001 衔接全对齐

### ✅ 检查 1：术语一致性（跟 R011 + W001）

| 术语（正文用）| R011/W001 | 一致？|
|---|---|---|
| data-aided (DA) / non-data-aided (NDA) estimator | #3/#5 标准 | ✅ §III |
| carrier phase estimator | #1 CPE 同义（方法节用 CPE/estimator）| ✅ §III "carrier phase estimators" |
| squaring loss | #10 引 V&V 1983 | ✅ §III "squaring loss ... [V&V 1983]" 不推导 |
| pilot overhead | #11 标准 | ✅ §III "$25\%$ ... $1.25$ dB overhead" |
| per-block SNR (γ_blk) | #30 定义 "the SNR over a single fading block of N_blk symbols within which h is constant" | ✅ §III 公式 3 定义句逐字对齐 |
| crossover (γ_th) | #31 定义 "SNR at which BER curves of DA and NDA intersect" | ✅ §III "crossover SNR at which the BER curves of the two estimators intersect" + §IV-A 用 |
| estimator switching / per-block SNR-driven selection | #33 首次写全称 "per-block SNR-driven estimator switching" | ✅ §III 末 "per-block, SNR-driven selection" |
| net SNR gain | #34 替代 fair_gain | ✅ §IV-B "net SNR gain" + 脚注口径 |
| bit error rate $P_b$ | R011 符号表 P_b（§IV Results 用）| ✅ §IV-A "$P_b$ versus SNR" |
| HD-FEC threshold | #24 标准（3.8e-3, 7%）| ✅ §IV-B |
| AWGN (reference/baseline) | #27 标准 | ✅ §IV-A "AWGN reference ... implicit baseline" |
| fading / fading block | #15/#32 标准 | ✅ §III "single fading block of N_blk symbols" |
| turbulence / downlink / uplink | #14 标准 | ✅ §IV-A "weak/moderate/strong downlink ... moderate/strong uplink" |

**自造词残留检查**：
- fair_gain / A4 / MSM / 伪地板 / 鲁棒性补丁 / robustness patch：❌ 全文无 ✅

✅ 术语全对齐

### ✅ 检查 2：符号一致性（跟 R011 符号表）

| 符号（正文用）| R011 符号表 | 一致？|
|---|---|---|
| $\hat{\theta}_\text{DA}$ | §III DA 估计器输出相位（本工作定义）| ✅ 公式 1 |
| $\hat{\theta}_\text{NDA}$ | §III NDA 估计器输出相位（本工作定义）| ✅ 公式 2 |
| $r_p$ | §II r_k（pilot 位置的特例）| ✅ 公式 1（R011 注 "r_p 是 r_k 在 pilot 位置的特例"）|
| $p, p^*$ | §II 已知 pilot 符号 + 复共轭 | ✅ 公式 1 |
| $r_k$ | §II 接收信号样值 | ✅ 公式 2 |
| $M_0 = 8$ | §II 升幂次数 | ✅ 公式 2 |
| $\gamma_\text{blk}$ | §III 每块 SNR（本工作定义）| ✅ 公式 3 |
| $h_b$ | §II 块 b 衰落系数 | ✅ 公式 3 |
| $E_s, N_0$ | §II | ✅ 公式 3 |
| $\gamma_\text{th}$ | §III 切换阈值 SNR（本工作定义）| ✅ §III 切换规则 + §IV-A |
| $P_b$ | §IV BER | ✅ §IV-A "$P_b$ versus SNR" |

**符号无冲突**：θ̂_DA / θ̂_NDA（下标区分）/ γ_blk / γ_th（下标区分）/ N₀ vs N_blk vs N_DFT（下标区分，§III/§IV 仅 N₀ 出现）✅

✅ 符号全对齐

### ✅ 检查 3：数字一致性（跟 R012 P2-B）

| 数字（正文用）| R012 # | 值 | 口径 | 一致？|
|---|---|---|---|---|
| crossover weak/mod/strong | #8 | 17.9 / 16.8 / 10.7 dB | data（线性插值交叉点）| ✅ §IV-A |
| 切换 vs 固定 NDA 低 SNR | #5 | +1.3~2.3 dB | net（CI 下界全正）| ✅ §IV-B "low-SNR avoidance" |
| 净增益 downlink strong | #1 | +1.26 dB | naive（= fair 2.509 − 1.249）| ✅ §IV-B |
| 净增益 uplink moderate | #3 | +1.19 dB | naive（= fair 2.443 − 1.249）| ✅ §IV-B |
| 净增益 uplink strong | #2 | +1.85 dB | naive（= fair 3.101 − 1.249）| ✅ §IV-B（Intro 承诺兑现）|
| 弱湍流/AWGN 净增益 | #4 | +0.09 / +0.18 / +0.19 dB | naive（CI 重叠归零，诚实标注）| ✅ §IV-B "reported transparently rather than suppressed" |
| 切换选对率 | #7 | 26/29 | data | ✅ §III 末 + §IV-B |
| pilot overhead | #9 | 1.25 dB（=10log10(4/3)）| 定义值 | ✅ §III + §IV 脚注 |
| HD-FEC 门限 | 参数表 A4 | 3.8e-3（7%）| 定义值 | ✅ §IV-B |
| M₀ | #10 | 8 | 定义值 | ✅ §III 公式 2 |

**未出现的数字（确认不写）**：
- 切换 vs 固定 DA（R012 #6）：❌ 不写（导师第 3 点，多数 CI 跨 0 不显著）✅
- fair 口径数字（2.509/3.101 等）：❌ 正文不报 fair 大数，只报 naive 小数 + 脚注说明口径 ✅

**口径标注**：§IV-B 脚注 ¹ 逐字照抄 W001 脚注模板（net of 1.25 dB pilot penalty / 768 bits per block）✅

✅ 数字全对齐

### ✅ 检查 4：力度一致性（跟 R010 §3/§4）

| 节 | R010 基准 | W002 实现 | 一致？|
|---|---|---|---|
| Method 篇幅 | §3：1-2 段（R012 §III）| 2 段（DA/NDA 一段 + per-block SNR/切换/定位一段）| ✅ |
| 估计器公式粒度 | §2.3：直接给结论级（对齐 Panasiewicz），1 行 + 1 句话 | 公式 1/2 各 1 行 + 1 句话解释，不推导 | ✅ |
| squaring loss | §2.3：引 V&V 1983 文字结论不推导 | §III "squaring loss ... [V&V 1983]" 一句话 | ✅ |
| 切换机制描述 | §3.1：文字 + 框图，不用伪代码（5/5 篇无伪代码）| §III 切换规则文字描述 "select θ̂_DA when ... else ..."，无伪代码 | ✅ |
| 创新点定位 | §3.2：弱声明（对齐 Johst），不夸"新算法" | §III 末 "rather than introducing a new estimator or a new closed-loop component; it adapts ... to the locally prevailing SNR" | ✅ 定位=量化归因型，弱声明 |
| Results BER 主图 | §4.1：纵轴不硬凑 1e-5（对齐 Paillier），加 AWGN 理论线隐式 baseline（对齐 Johst）| §IV-A "plotted down to the minimum reliably estimable level"（中性措辞）+ "AWGN reference, included as an implicit baseline" | ✅ 纵轴不硬凑 1e-5（中性措辞）+ AWGN 隐式 baseline |
| 增益数字报法 | §4.2：正文 dB + Tab.1 增量亮点 | §IV-B 正文报 dB（1.26/1.19/1.85/1.3~2.3）+ Tab.1 占位 | ✅ |
| baseline 对比 | §4.3：DA/NDA 两曲线同图对比融 Results 文字段，不专列对比节（5/5 篇无对比节）| §IV-A DA/NDA 曲线同图（Fig.2）+ 文字说明各自优势区，无对比专节 | ✅ |
| Tab.1 | §4.2：只强湍流 3 行 naive（增量亮点）| Tab.1 占位 "summarizes the net SNR gain ... strong-turbulence and uplink"，正文给 3 个 naive 值 | ✅ |

✅ 力度全对齐

### ✅ 检查 5：切换 framing 统一"自适应选优"（R008）

| 位置 | framing | 一致？|
|---|---|---|
| §III 切换规则描述 | "per-block, SNR-driven selection between the DA and NDA estimators" + "adapts an existing DA/NDA choice to the locally prevailing SNR, selecting the locally optimal estimator in 26 of 29 operating points" | ✅ 自适应选优（R008 verbatim 关键短语 "selecting the locally optimal estimator in 26 of 29"）|
| §IV-B 选对率 | "selects the locally optimal estimator in 26, recovering the gain the single-estimator baseline forgoes" | ✅ 自适应选优 |

**禁用措辞残留检查**：
- "鲁棒性补丁" / "robustness patch"：❌ 无 ✅
- "切换是闭环必要环节" / "necessary closed-loop component"：❌ 无（§III 明确 "rather than ... a new closed-loop component"）✅
- "crossover 物理归因"：§IV-A 只报数字（17.9/16.8/10.7）不解释为什么左移（标 TBD 注释）✅

✅ 切换 framing 统一

### ✅ 检查 6：crossover 只呈现数据不附物理归因（R009 不变量 7）

| 位置 | 实现 | 一致？|
|---|---|---|
| §IV-A crossover 描述 | "the crossover SNR γ_th moves to lower SNR as turbulence grows, decreasing from 17.9 dB (weak) through 16.8 dB (moderate) to 10.7 dB (strong)" | ✅ 只陈述数据事实（左移 + 数字）|
| §IV-A crossover 归因 | （无）—— TBD 注释标"为什么左移没搞清，不解释" | ✅ 不附物理归因 |

✅ crossover 只呈现数据

**交叉检查全部通过 ✓（6 项 + W001 衔接）**

---

## Results 风险防范落实说明（主体 vs 标记区）

按主控指令，Results 写得"对解读不敏感"——导师翻解读 A（BER=1e-5 处必须有增益，D003 已证 strong/uplink 到不了 1e-5 + 增益在 BER→0 数学坍塌）时主体不用重写，只动标记区。

### 主体（对解读不敏感，导师翻 A 也不用重写）

| 内容 | 解读无关性依据 |
|---|---|
| BER 曲线呈现（Fig.2，6 子图）| 纯数据事实——画到能画到的，不强凑 1e-5（对齐 Paillier，R004/H002）|
| **HD-FEC(3.8e-3) 处增益数字**（Tab.1 + §IV-B）| **解读无关硬事实**——pre-FEC 基准 1e-3 是领域通行（R004 结论），strong/uplink +1.26~1.85 dB naive 在 HD-FEC 门限处测，不依赖 1e-5 解读 |
| crossover 数字（17.9/16.8/10.7 dB）| 纯数据（线性插值交叉点）|
| 切换选对率 26/29 | 纯数据（data 口径）|
| 切换 vs 固定 NDA 低 SNR +1.3~2.3 dB | 纯数据（net 口径，CI 下界全正）|
| 弱湍流归零诚实标注（+0.09/0.18/0.19 CI 重叠）| 纯数据（诚实底线，不变量 3）|

**措辞策略**：主体正文用中性措辞——"BER curves are plotted down to the minimum reliably estimable level for each regime"（中性，不说"down to 1e-5"也不说"down to 1e-3"），这样无论导师定纵轴画到哪，主体措辞不动。

### 标记区（集中放「待导师确认」，导师翻 A 只动这里）

| TBD 项 | 位置 | 导师反馈后动作 |
|---|---|---|
| 主图纵轴范围（1e-3 还是尝试 1e-5）| §IV-A HTML 注释 `<!-- TBD: 纵轴范围待导师定（D003） -->` | 导师定 A=硬凑 1e-5（需补点）/ B=画到能画到的（主体不动，删 TBD）|
| 1e-5 底线解读（A=必须 pre-FEC 达到 / B=post-FEC 预期）| §IV-A HTML 注释 `<!-- TBD: crossover 只呈现数据 ... -->`（隐含 1e-5 解读关联）| 导师定 A/B 后，§IV-A 措辞微调（如 B 加"consistent with post-FEC operation"）|
| 标题数字（1.85 dB naive / fair 3.10 dB / 解读 A 数字）| §IV-B 末 HTML 注释 `<!-- TBD: 标题/数字口径待导师定（D004） -->` | 导师定 fair/naive（D004 已倾向 naive）/ 解读 A 数字后，标题 + §IV-B 末句同步 |

**标记方式**：HTML 注释 `<!-- TBD: ... -->`（LaTeX/Word 转 PDF 不渲染，但 .md 源可见），F 阶段或导师反馈后集中处理。

### 防范效果

- 导师翻解读 A（最坏情况）：主体（BER 曲线 + HD-FEC 增益 + crossover + 选对率）**全部不用重写**，只动 3 个 TBD 标记区（纵轴范围 + 1e-5 措辞 + 标题数字）
- 导师翻解读 B（最可能，R004 证据支撑）：删 3 个 TBD 标记，主体措辞已是中性，直接定稿

## 决策引用

- 无新建 D###：本轮是正文写作（W3+W4），不改方向/架构决策。所有术语/符号/数字/力度来自已验证的 R009/R010/R011/R012 + W001 衔接。
- 沿用决策：
  - D003（10⁻⁵ 底线 A/B）→ §IV-A 纵轴范围 + 1e-5 措辞进标记区（TBD），主体中性措辞不依赖解读
  - D004（口径方向）→ §IV-B 主报 naive（1.26/1.19/1.85 dB）+ 脚注口径 + 标题数字 TBD
  - D005（务实路线）→ §III 创新点弱声明（"rather than introducing a new estimator"），定位=量化归因型
  - R008（切换 framing=自适应选优）→ §III + §IV-B verbatim 关键短语 "selecting the locally optimal estimator in 26 of 29"
  - R009（轻讲）→ §IV-A crossover 只呈现数据不附归因（标 TBD）；§III squaring loss 引 V&V 1983 不推导
  - 导师第 3 点（vs 导频输不写）→ §IV-B 不报切换 vs 固定 DA（R012 #6 不进论文）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。W3/W4 是 writing-campaign-plan §2 正文写作活（topic-index 范围边界 H009/H010 已确认写作正文在写作专题范围内，不跳 FR-22）。

## 后续

D-W5F3：Conclusion（W5）+ Abstract（F3）。交接见 H011-method-results-drafted.md。

- **W5 要用**：R012 §V 大纲（1 段 3-5 句：复述贡献 per-block SNR 驱动切换 + 26/29 + 1.85 dB naive + 弱湍流归零局限 + future）+ Intro/Method/Results 已写的贡献句/数字（复述要一致）+ R010 §5 力度（1 段，对齐 Johst/Le Bidan）+ writing-patterns §6.x Conclusion 句式
- **F3 要用**：Abstract 直接英文起草（参照 Intro 贡献句 + writing-patterns §8.x "In this paper, we propose ..."）+ 关键数字（26/29 + 1.85 dB naive）
- **标记区清单**（W4 Results 3 个 TBD，F 阶段或导师反馈后集中处理）：①§IV-A 纵轴范围（D003）②§IV-A 1e-5 解读措辞 ③§IV-B 标题数字口径（D004）
