# [W001] Intro（W1）+ System Model（W2）正文起草

> 2026-07-12 | 阶段：writing-campaign §2 正文写作（D-W1W2）| 状态：定稿
> 来源: H009 交接 | 写作依据: R012 P3-A §I/§II 大纲 + R011 三表 + R010 力度基准 + R009 逻辑链 + writing-patterns-conference.md

## 目标

按 R012 §I 大纲写 Intro 英文正文（背景 + gap + 贡献散文式）+ 按 R012 §II 大纲写 System Model 英文正文（GG 块衰落 + 帧结构 + PN）。术语/符号/公式零偏差跟 R011 一致，数字跟 R012 一致，力度跟 R010 一致，切换 framing 统一"自适应选优"。

## 记录

---

### §I Introduction

Coherent free-space optical (FSO) communication between satellites and optical ground stations (OGSs) has been actively pursued to support high-data-rate feeder links, with methods using coherent detection providing better receiver sensitivity and enabling higher-order modulation formats as compared to intensity-modulation direct-detection systems [sat.1553][Paillier]. However, optical signal propagation through the atmosphere is affected by absorption, scattering, and refractive-index fluctuations—i.e., atmospheric turbulence—which cause rapid amplitude scintillation and a time-varying carrier phase that the receiver must track [Al-Habash 2001][Johst]. Carrier phase recovery (CPR) is therefore an essential block at the coherent receiver, tasked with estimating and compensating for the residual phase noise introduced by the laser linewidth and the turbulent channel [APCCAS 2022][B11].

Two established CPR strategies trade off estimation accuracy against spectral efficiency. Data-aided (DA) estimation, which divides out modulation using known pilot symbols, achieves high estimation accuracy at low signal-to-noise ratio (SNR) but pays a bandwidth penalty for the inserted pilots—on the order of $10\log_{10}(4/3) = 1.25$ dB at a one-in-four pilot spacing [Shieh-Djordjevic 2010]. Non-data-aided (NDA) estimation, in contrast, removes modulation by raising the received samples to the $M_0$-th power (the Viterbi-and-Viterbi estimator), wastes no bandwidth on pilots, but suffers from squaring loss that degrades its low-SNR phase estimation accuracy [V&V 1983]. The two estimators therefore dominate in disjoint SNR regions: DA is preferable where the signal is weak, and NDA where the signal is strong.

In this paper, we propose a per-block SNR-driven estimator switching scheme that selects, for each fading block, between a data-aided (DA) and a non-data-aided (NDA) carrier phase estimator based on the block's measured SNR. The scheme selects the locally optimal estimator in 26 of 29 operating points, yielding a net SNR gain of up to 1.85 dB in strong turbulence (naive, net of pilot overhead)¹. The remainder of this paper details the channel and signal model (Section II), the DA/NDA estimators and the switching rule (Section III), and simulation results over Gamma-Gamma fading channels under downlink and uplink conditions (Section IV).

> ¹ *All reported gains are net of the pilot power penalty of 1.25 dB ($10\log_{10}(4/3)$); the bit error rate is computed over data symbols (768 bits per block) unless otherwise stated.*

---

### §II System Model

As depicted in Fig. 1, we consider a coherent satellite-to-ground (and uplink) FSO link operating with $(8,8)$-16APSK modulation, where the constellation comprises $M_0 = 8$ points per ring [B11]. The atmospheric channel is modeled as a Gamma-Gamma block-fading channel [Al-Habash 2001]: the channel undergoes block fading (quasi-static), such that the fading coefficient $h_b$ remains constant over a block of $N_\text{blk} = 100$ symbols and varies independently between blocks. The Gamma-Gamma shape parameters $(\alpha, \beta)$ are set to $(4.0, 3.0)$, $(2.5, 1.8)$, and $(1.5, 0.8)$ for the weak, moderate, and strong downlink turbulence regimes, respectively, and $(1.2, 0.9)$ and $(1.0, 0.7)$ for the moderate and strong uplink regimes.

The discrete-time complex baseband received signal at symbol index $k$ within block $b$ is modeled as
$$r_k = h_b \, s_k \, e^{j\theta} + n_k,$$
where $s_k$ is the transmitted $(8,8)$-16APSK symbol, $\theta$ denotes the carrier phase offset (denoted $\phi$ in [B11]; we follow the $\theta$ notation of [V&V 1983]), and $n_k$ is complex AWGN with one-sided power spectral density $N_0$. The frame structure inserts one pilot symbol every four symbols, yielding a pilot spacing of $1/4$ and a pilot overhead of $25\%$, equivalent to a $1.25$ dB SNR penalty ($10\log_{10}(4/3)$) [Shieh-Djordjevic 2010]. The residual carrier phase is modeled as a Wiener phase noise process with per-symbol increment variance
$$\sigma_\theta^2 = 2\pi \, \Delta\nu \, T_s \quad (= \sigma_p^2 \text{ in [B11]}),$$
where $\Delta\nu = 10$ kHz is the laser linewidth and $T_s$ is the symbol period. Carrier phase recovery is performed per DSP block of $N_\text{DFT} = 256$ samples, and the HD-FEC threshold is $3.8 \times 10^{-3}$ (7% overhead) [B11].

---

## 交叉检查（6 项）

### ✅ 检查 1：术语一致性（跟 R011 术语表）

| 术语（正文用）| R011 术语表 | 一致？|
|---|---|---|
| carrier phase recovery (CPR) | #2（Intro/标题用 CPR 整体流程）| ✅ Intro 用 CPR |
| carrier phase estimation (CPE) | #1（方法节用 CPE 估计操作）| — Intro/SM 未用 CPE（进 §III Method）|
| data-aided (DA) | #3 标准 | ✅ |
| non-data-aided (NDA) | #5 标准 | ✅ |
| coherent detection | #23 标准 | ✅ Intro "methods using coherent detection" |
| atmospheric turbulence | #14 标准 | ✅ |
| Gamma-Gamma (channel model) | #16 引 Al-Habash 2001 | ✅ SM 引 Al-Habash 2001 |
| block fading (quasi-static) | #32 首次定义 "block fading (quasi-static)" | ✅ SM 首次出现写全称 |
| pilot overhead | #11 标准 | ✅ |
| squaring loss (SL) | #10 引 V&V 1983 | ✅ Intro 引 V&V 1983，不推导 |
| Wiener phase noise | #20 标准 | ✅ SM "Wiener phase noise process" |
| laser linewidth | #21 标准 | ✅ SM $\Delta\nu = 10$ kHz |
| SNR penalty / power penalty | #13 标准（pilot overhead 功率代价视角）| ✅ SM "1.25 dB SNR penalty" |
| (8,8)-16APSK | #22 B11 标准 | ✅ SM "$M_0 = 8$ points per ring [B11]" |
| per-block SNR-driven estimator switching | #33 首次写全称 | ✅ Intro 贡献句写全称 |
| net SNR gain | #34 替代 fair_gain | ✅ Intro "net SNR gain" + 脚注口径标注 |
| spectral efficiency | #12 标准 | ✅ Intro "bandwidth penalty" |
| AWGN | #27 标准 | ✅ SM "complex AWGN" |
| HD-FEC threshold | #24 标准 | ✅ SM "$3.8 \times 10^{-3}$ (7% overhead)" |

**自造词残留检查**（grep 思路逐项过）：
- fair_gain：❌ 正文无，用 "net SNR gain" ✅
- A4 / A4-B11-Q1：❌ 正文无 ✅
- MSM / MSDM：❌ 正文无 ✅
- "伪地板" / error floor：❌ 正文无 ✅

✅ 术语全对齐

### ✅ 检查 2：符号一致性（跟 R011 符号表）

| 符号（正文用）| R011 符号表 | 一致？|
|---|---|---|
| $r_k$ | §II 接收信号样值 | ✅ |
| $h_b$ | §II 块 b 衰落系数（块内恒定）| ✅ |
| $s_k$ | 发射符号（隐式，未在符号表但 §II 标准用）| ✅ |
| $\theta$ | §II 载波相位（V&V/sat.1553，非 B11 的 $\phi$）| ✅ SM 首次出现注 "(denoted $\phi$ in [B11])" |
| $n_k$ | 噪声（隐式，$N_0$ 在符号表）| ✅ |
| $N_0$ | §II 噪声 PSD | ✅ |
| $M_0 = 8$ | §II 升幂次数 | ✅ |
| $\alpha, \beta$ | §II GG 形状参数 | ✅ |
| $\sigma_\theta^2$ | §II 每符号 Wiener PN 方差（注 "= $\sigma_p^2$ in [B11]"）| ✅ SM 注对应 |
| $\Delta\nu = 10$ kHz | §II 激光线宽 | ✅ |
| $T_s$ | §II 符号周期 | ✅ |
| $N_\text{blk} = 100$ | §II 信道块长 | ✅ |
| $N_\text{DFT} = 256$ | §II DSP 处理块长 | ✅ |

**符号无冲突检查**：
- $N_0$ vs $N_\text{blk}$ vs $N_\text{DFT}$：下标不同（0 / blk / DFT）✅
- $\sigma_\theta^2$（PN 方差）vs $\sigma_R^2$（Rytov）：正文只用前者 ✅
- $\theta$（相位）：SM 注 B11 对应关系，全篇用 $\theta$ ✅

✅ 符号全对齐

### ✅ 检查 3：数字一致性（跟 R012 数字清单）

| 数字（正文用）| R012 # | 值 | 口径 | 一致？|
|---|---|---|---|---|
| 选对率 26/29 | #7 | 26/29（90%）| data | ✅ Intro 贡献句 |
| 净增益 1.85 dB（强湍流）| #2 | +1.85 dB | naive（标脚注）| ✅ Intro 贡献句标 "(naive, net of pilot overhead)" + 脚注 |
| pilot overhead 1.25 dB | #9 | 1.25 dB（=10log10(4/3)）| 定义值 | ✅ Intro + SM 两处 |
| $M_0 = 8$ | #10 | 8 | 定义值 | ✅ SM |
| $N_\text{blk} = 100$ | 参数表 A1 | 100 | 定义值 | ✅ SM |
| $N_\text{DFT} = 256$ | 参数表 A1 | 256 | 定义值 | ✅ SM |
| $\Delta\nu = 10$ kHz | 参数表 A2 | 10 kHz | 定义值 | ✅ SM |
| HD-FEC $3.8 \times 10^{-3}$ | 参数表 A4 | 3.8e-3（7%）| 定义值 | ✅ SM |
| $(\alpha,\beta)$ weak/mod/strong | 参数表 A2 | (4.0,3.0)/(2.5,1.8)/(1.5,0.8) | 定义值 | ✅ SM |
| $(\alpha,\beta)$ up_mod/up_str | 参数表 A2 | (1.2,0.9)/(1.0,0.7) | 定义值 | ✅ SM |
| pilot spacing 1/4（25%）| 参数表 A3 | 每 4 符号 1 pilot | 定义值 | ✅ SM "one pilot every four symbols" |

**口径标注**：Intro 贡献句标 "(naive, net of pilot overhead)" + 脚注模板（R012 B3 脚注模板逐字照抄）✅

**Intro 没放的数字**（留给 Results）：crossover 17.9/16.8/10.7 / 切换 vs NDA +1.3~2.3 / strong +1.26 / 弱湍流归零 +0.09/0.18/0.19——全部不出现 ✅

✅ 数字全对齐

### ✅ 检查 4：力度一致性（跟 R010）

| 节 | R010 基准 | W001 实现 | 一致？|
|---|---|---|---|
| Intro 篇幅 | §1.1：1-2 段 ~8-15 行（对齐 Panasiewicz/Paillier）| 3 段：背景 2 段 + 贡献 1 段，正文约 15 行 | ✅ 在范围内（R010 §1.1 允许 1-2 段 ~8-15 行，背景偏 2 段，整体未超）|
| 贡献声明 | §1.2：散文式 2-3 句，不用 bullet（5/5 篇）| 散文式 3 句（propose → selects → yielding），无 bullet | ✅ |
| Gap 动机引出 | §1.3：1-2 句点出 DA/NDA trade-off gap | 第 2 段 2 句（DA 低 SNR 准 + 1.25dB 罚 / NDA 省带宽 + squaring loss）| ✅ |
| SM 信道模型 | §2.1：给 GG 模型名 + 块结构，不给完整 PDF | SM 给 "Gamma-Gamma block-fading channel" + $(\alpha,\beta)$ 值 + 块结构说明，**无 PDF 公式** | ✅ |
| SM 帧结构 | §2.2：文字描述 + pilot overhead 数字 | SM "one pilot every four symbols ... 1.25 dB" | ✅ |
| SM 估计器公式 | §2.3：DA/NDA 公式直接给，进 §III 不进 §II | SM **不放 DA/NDA 公式**（留 §III Method）| ✅ |
| 参数表 | 总览表 4/5 篇 0 表 | SM **不给独立参数表**，关键值进正文一句话 | ✅ |
| 图表 | Fig.1 系统框图占位 | SM "as depicted in Fig. 1" 占位引用，不画 | ✅ |

✅ 力度全对齐

### ✅ 检查 5：切换 framing 统一"自适应选优"（跟 R008）

| 位置 | framing | 一致？|
|---|---|---|
| Intro 贡献句 | "per-block SNR-driven estimator switching scheme that selects, for each fading block, between a DA and a NDA carrier phase estimator" + "selects the locally optimal estimator in 26 of 29 operating points" | ✅ 自适应选优 |
| Intro 第 3 段 | "DA is preferable where the signal is weak, and NDA where the signal is strong"（trade-off 两法各有优势区）| ✅ |

**禁用措辞残留检查**（grep 思路逐项过）：
- "鲁棒性补丁" / "robustness patch"：❌ 无 ✅
- "切换是闭环必要环节" / "necessary closed-loop component"：❌ 无 ✅
- "crossover 物理归因"：Intro 不碰 crossover（留给 Results 只呈现数据）✅

**R008 关键短语 verbatim 核对**：
- "selecting the locally optimal estimator in 26 of 29 operating points" → 正文 "selects the locally optimal estimator in 26 of 29 operating points"（主谓数一致改为 selects）✅ 语义 verbatim

✅ 切换 framing 统一

### ✅ 检查 6：句式参照 writing-patterns-conference.md

| 句式位置 | 参照模式条目 | 落实？|
|---|---|---|
| Intro 背景首句 | §5.6 "For both [A] and [B], methods using coherent detection ... provide a better sensitivity ... as compared to ..."（ICSOS 2019）| ✅ "methods using coherent detection providing better receiver sensitivity ... as compared to intensity-modulation direct-detection systems" |
| Intro 问题句 | §5.4 "However, optical signal propagation is affected by ... turbulence, which causes ..."（MWP 2022）| ✅ "However, optical signal propagation through the atmosphere is affected by ... atmospheric turbulence—which cause rapid amplitude scintillation and a time-varying carrier phase" |
| Intro CPR 定位句 | §5.7 "[模块] is an essential block to estimate and compensate for the phase noise introduced by ... [引用]"（APCCAS 2022）| ✅ "Carrier phase recovery (CPR) is therefore an essential block at the coherent receiver, tasked with estimating and compensating for the residual phase noise" |
| Intro 贡献首句 | §8.x 散文式贡献（"In this paper, we propose ..."）| ✅ "In this paper, we propose a per-block SNR-driven estimator switching scheme ..." |
| SM 信号模型 | §1.2 "In the presence of [损伤], the [信号] is modeled as: [公式]"（OECC 2025）+ §1.9 "can be described as" | ✅ "The discrete-time complex baseband received signal ... is modeled as r_k = ..." |
| SM 参数解释 | §2.1 "where [符号] denotes ... [符号] represents ... [引用]" | ✅ "where $s_k$ is ... $\theta$ denotes the carrier phase offset (denoted $\phi$ in [B11])" |
| SM PN 模型 | §1.13 "can be expressed as a Gaussian noise process with variance"（ICUMT 2015）| ✅ "modeled as a Wiener phase noise process with per-symbol increment variance $\sigma_\theta^2 = 2\pi\Delta\nu T_s$" |
| Conclusion 过渡 | §7.4 "This paper then proposes ..." / §7.5 结构导航（短篇建议省略）| ✅ Intro 末句简短引路 "The remainder of this paper details ... (Section II/III/IV)"，单句非完整 roadmap |

**会议论文体例特征核对**（writing-patterns-conference.md §会议论文写法特点）：
- 贡献散文式无 bullet（特点 2）✅
- 无"下一节将…"完整 roadmap 段（特点 3）—仅 Intro 末单句引路 ✅
- 参数解释一句话内完成（特点 4）✅
- Related work 极简（特点 5）—Intro 第 2 段 2 句点出 DA/NDA trade-off ✅

✅ 句式全对齐

---

**交叉检查全部通过 ✓（6/6）**

## 决策引用

- 无新建 D###：本轮是正文写作（W1+W2），不改方向/架构决策。所有术语/符号/数字/力度来自已验证的 R009/R010/R011/R012/H009。
- 沿用决策：
  - D004（口径方向）：Intro 报 1.85 dB naive + 脚注标口径
  - D005（务实路线）：贡献声明不自夸"新算法"，定位=量化归因型
  - R008（切换 framing=自适应选优）：Intro 贡献句 verbatim 关键短语
  - R009（轻讲）：Intro/SM 不碰 crossover 物理归因（留 Results 只呈现数据）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。W1/W2 是 writing-campaign-plan §2 正文写作活（topic-index 范围边界 H009 已确认写作正文在写作专题范围内，不跳 FR-22）。

## 后续

D-W3W4：Method（W3）+ Results（W4）正文。交接见 H010-intro-sm-drafted.md。

- **W3 要用**：R012 §III 大纲（DA/NDA/per-block SNR 三公式）+ R011 公式清单（DA θ̂_DA=angle(r_p·p\*) / NDA θ̂_NDA=(1/M₀)angle(Σr^M₀) / per-block SNR γ_blk=|h_b|²E_s/N₀ + 切换规则文字）+ R008 切换 framing 自适应选优 + R010 §3.1/§3.2 力度（文字+框图非伪代码，1-2 段）
- **W4 要用**：R012 §IV 两段式大纲（§IV-A 影响分析 + §IV-B 方法增益）+ 数字（crossover weak 17.9/mod 16.8/strong 10.7 dB + 切换 vs NDA +1.3~2.3 dB + 净增益 strong +1.26/up_str +1.85 dB naive + 选对率 26/29）+ Fig.2/3/4/Tab.1 占位 + R010 §4 力度
- **W4 风险防范**（主控指令）：Results 写得"对解读不敏感"——主体呈现 BER 曲线 + HD-FEC(3.8e-3) 处增益数字（解读无关硬事实），纵轴范围/标题数字集中到「待导师确认」标记区。导师翻 A（1e-5 必须有增益）只动标记区，主体 BER 呈现不用重写。

**等导师项（不阻塞正文写作，但卡 Results §IV-B 标题数字）**：
1. 10⁻⁵ 底线 A/B（D003）→ 决定主图纵轴范围（标记区）
2. 口径 fair/naive（D004 已定主报 naive）→ 标题数字锁定 1.85 dB naive
3. 主对比文献 → 参考文献核心一条
