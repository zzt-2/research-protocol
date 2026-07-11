# [R011] 用语+符号+公式三合一（D-P1 产出）

> 2026-07-11 | 关联：专题 2026-07-09-thesis-writing / writing-campaign-plan.md §2 P1 / H007 交接
> 数据来源：2 子 agent 并发查证（agent A = A 组 5 篇 content.md / agent B = C 组 B11 + sat.1553 content.md）+ `_recovery.py` 代码行核验 + `_b11_params.py` 参数符号

## 调研问题

论文全篇的英文零件（术语 / 符号 / 公式）一次定死，使 W1-W5 正文写作直接照抄无歧义。三张表互相耦合（"per-block SNR"既是术语也是符号 γ_blk），必须一次定完。

## 发现

### 表 1：术语表

分三类：①领域标准词（查证后直接用）；②我方需显式定义的词（A 组/C 组无人用或用法不同）；③自造词替换（不变量 6 黑话禁令）。

#### ① 领域标准词（查证通过，直接用）

| # | 英文词 | 中文释义 | 用法例句（英文原句）| 来源论文（哪篇哪节/行）| 是否标准 |
|---|---|---|---|---|---|
| 1 | carrier phase estimation (CPE) | 载波相位估计 | "data-aided carrier-phase estimation (CPE)" | Johst §I L50；OECC-PSC §I L17；**B11 Abstract L9（28×）**；sat.1553 §4 L385 | ✅ 标准。CPE 是估计操作的标准名 |
| 2 | carrier phase recovery (CPR) | 载波相位恢复（整体流程）| "carrier-phase recovery" | Johst L114；Le Bidan L666 | ✅ 标准。Intro/标题用 CPR（整体流程），方法节用 CPE（具体操作）|
| 3 | data-aided (DA) | 导频辅助 / 数据辅助 | "data-aided algorithms" | Johst L13；Le Bidan L369；OECC-PSC L25；B11 L27；sat.1553 L464 | ✅ 标准 |
| 4 | pilot-aided (PA) / pilot symbol | 导频辅助 / 导频符号 | "pilot-aided (PA) phase noise estimation" | OECC-PSC L25；B11 L29；Le Bidan L319-352 §III.B | ✅ 标准。DA/PA 同义，本论文统一用 DA（首次出现注明 = pilot-aided）|
| 5 | non-data-aided (NDA) | 盲类估计（不花导频）| "non-data-aided (NDA) frequency estimator" | Le Bidan L436 | ✅ 标准。本论文 NDA = Mth-power NDA-ML（见 #7）|
| 6 | blind estimation / blind equalization | 盲估计 / 盲均衡 | "blind equalization schemes" | Johst L29；Le Bidan L551/569；sat.1553 L464 | ✅ 标准。讨论 CMA 等非导频方法时用 blind；本论文 NDA 估计器不等于 blind（NDA-Mth-power ≠ CMA）|
| 7 | NDA-ML (non-data-aided maximum likelihood) | 非数据辅助最大似然估计 | "non-data-aided maximum likelihood (ML)" | **B11 Abstract L9（方法源头）** | ✅ 标准。本论文 NDA 估计器 = B11 的 NDA-ML |
| 8 | Mth-power estimator / raised to the M₀th power | 升 M 次幂估计器 | "raising the received spectrum to the M₀-th power" | B11 L29/L75；sat.1553 L470；Le Bidan L676；Panasiewicz L65 | ✅ 标准。NDA-ML 的实现方式 |
| 9 | V&V estimator (Viterbi-and-Viterbi) | V&V 估计器 | "the V&V is hindered by excessive noise amplification" | Le Bidan L675；Panasiewicz L71；sat.1553 L399 | ✅ 标准。Mth-power 估计器的经典命名，引 V&V 1983 |
| 10 | squaring loss (SL) | 平方损失（升幂放大相位估计误差）| "the so-called squaring loss (SL)" | Paillier §III L151（A 组唯一）；教科书 V&V 1983 | ✅ 标准（教科书术语）。A 组仅 Paillier 显式用，但 V&V 1983 IEEE TIT 是公认源头。引 V&V 1983，不推导 |
| 11 | pilot overhead | 导频开销（带宽代价）| "additional pilot overhead of ≈1%" | Johst L50；Le Bidan L51/L347 | ✅ 标准。本论文 25% overhead = 1.25 dB |
| 12 | spectral efficiency | 频谱效率 | "sacrifice spectral efficiency" | OECC-PSC L25；B11 L15/L27；sat.1553 L107 | ✅ 标准。pilot overhead 的频谱视角 |
| 13 | SNR penalty / power penalty | SNR 惩罚 / 功率惩罚 | "SNR penalties" / "power penalty of 0.42 dB" | OECC-PSC L111/L115；B11 L173；Panasiewicz L81；sat.1553 L167/L353 | ✅ 标准。pilot overhead 的功率代价视角。本论文 1.25 dB = pilot overhead 的 SNR penalty |
| 14 | atmospheric turbulence | 大气湍流 | "atmospheric turbulence" | Johst L193；Le Bidan L178；Panasiewicz L13；Paillier L39；B11 L15；sat.1553 L107 | ✅ 标准（全 7 篇都用）|
| 15 | fading / deep fade | 衰落 / 深衰落 | "deep fades will ineluctably appear" | Le Bidan L766；Panasiewicz L95；sat.1553 L790（"deep fading channels"）| ✅ 标准。**守不变量 5**：deep fade = BER 曲线斜率变缓，不是伪地板 |
| 16 | Gamma-Gamma (channel model) | Gamma-Gamma 信道模型 | — | A/C 组 0 篇用（FSO 接收机 DSP 论文不建湍流信道模型）；但 Al-Habash 2001 是 FSO 标准模型 | ✅ 标准（FSO 教科书模型）。A 组不用是因为它们不建信道模型，不是因为 GG 不标准。引 Al-Habash 2001 |
| 17 | scintillation index / Rytov variance | 闪烁指数 / Rytov 方差 σ²_R | "scintillation index σ_I²" | Johst L201；sat.1553 L149 | ✅ 标准。湍流强度度量，表参数时用 |
| 18 | SNR (signal-to-noise ratio) | 信噪比 | "signal-to-noise ratio (SNR)" | 全 7 篇 | ✅ 标准。横轴用 SNR(dB)（对齐 R010 §4.1）|
| 19 | BER (bit error rate) | 误比特率 | "bit-error ratio (BER)" | Johst L23；Le Bidan L716；Panasiewicz L13；OECC-PSC L61；B11 L143 | ✅ 标准。纵轴用 BER（对数）|
| 20 | phase noise (PN) / Wiener phase noise | 相位噪声 / Wiener 相位噪声 | "Wiener phase noise model" / "Wiener process" | Johst L102；Le Bidan L173；OECC-PSC L19；B11 L51 | ✅ 标准 |
| 21 | laser linewidth | 激光线宽 Δν | "linewidth of 200 kHz" / "combined laser linewidth (CLW)" | Johst L108；OECC-PSC L115；B11 L51（CLW）；sat.1553 L394 | ✅ 标准 |
| 22 | (8,8)-16APSK / M-APSK | (8,8)-16APSK 调制 | "(8,8)-16APSK" / "M-APSK … K rings, M₀ points" | **B11 L143/L29（方法源头，精确匹配我方调制）** | ✅ 标准。本论文调制 = B11 的 (8,8)-16APSK |
| 23 | coherent detection / coherent receiver | 相干检测 / 相干接收机 | "coherent" (implied throughout) | 全 7 篇（相干 FSO 是前提）| ✅ 标准 |
| 24 | FEC threshold / HD-FEC threshold | 前向纠错门限 | (implied in BER threshold context) | Johst L106（"DSP-outage threshold"）；B11 L181（"7% HD-FEC"）| ✅ 标准。BER 基准线（3.8e-3）|
| 25 | CRLB (Cramér-Rao lower bound) | 克拉美-罗下界 | "Cramér-Rao lower bound (CRLB)" | B11 L9/L133；sat.1553 L516（CRB）；Paillier L147 | ✅ 标准。性能界，引 B11 |
| 26 | cycle slip | 周期滑步 | "cycle slips" | Johst L98；Paillier L163；sat.1553 L408/L438 | ✅ 标准。CPR 失效模式（背景用）|
| 27 | AWGN (additive white Gaussian noise) | 加性高斯白噪声 | "AWGN" | (universal) | ✅ 标准 |
| 28 | frame structure / pilot spacing | 帧结构 / 导频间距 | "frame format" | Le Bidan §III.B L319-352；Johst §II.A | ✅ 标准。pilot spacing = 每 4 符号 1 pilot |
| 29 | modulation removal / remove modulation | 去调制 | (described in Mth-power context) | B11 L29；sat.1553 L470 | ✅ 标准（描述性短语）。DA 用除法去调制，NDA 用升幂去调制 |

#### ② 我方需显式定义的词（A/C 组无人用或无标准名）

| # | 英文词 | 中文释义 | 定义句（论文中首次出现时写）| 为什么需要显式定义 | 来源依据 |
|---|---|---|---|---|---|
| 30 | **per-block SNR** (γ_blk) | 每块信噪比 | "the per-block SNR γ_blk, defined as the signal-to-noise ratio measured over a single fading block of N_blk symbols within which the channel coefficient h is constant" | A/C 组 0 篇用此术语（Panasiewicz L85 "SNR level variations" 近义但非标准）。R009 决定不用 effective/instantaneous（instantaneous 误导）。sat.1553 L440 暗示 "optimal number of symbols is a function of SNR" 但未给术语 | R009 定稿；定义依据 = 块衰落信道模型（h 块内恒定）|
| 31 | **crossover** (crossing point) | BER 曲线交叉点 | "the crossover SNR γ_th, defined as the SNR at which the BER curves of the DA and NDA estimators intersect" | A/C 组 0 篇用 crossover 指 BER 交叉。需要定义是因为我方卖点之一（切换判据依据）| R009 定稿；数据事实（weak 17.9 / mod 16.8 / strong 10.7 dB）。**只呈现数据事实不附物理归因（不变量 7 / R009）** |
| 32 | **block fading** (quasi-static fading) | 块衰落 | "the channel undergoes block fading: the fading coefficient h remains constant over a block of N_blk symbols and varies independently between blocks" | A/C 组 0 篇用 block fading。sat.1553 L167 用 "quasi-static" + "coherence time"。Johst L92 "can be assumed as static"。"block fading" 是无线通信标准术语（Tse-Viswanath），FSO 论文多用 quasi-static 描述同一概念 | 定义依据 = sat.1553 quasi-static 概念 + 无线通信 block fading 标准定义。论文首次出现写 "block fading (quasi-static)"|
| 33 | **estimator switching** / adaptive estimator selection | 估计器切换 | "the receiver selects, for each block, the estimator with the lower expected BER based on the block's SNR γ_blk" | A/C 组 0 篇用 estimator switching。sat.1553 L440 "adaptive pilot rate" + L558 "avoid updating when signal quality degrades" 概念相关但术语不同。这是我方贡献描述词，非自造黑话（描述性：switch between estimators）| R008 贡献措辞："selecting the locally optimal estimator in 26 of 29 operating points"。首次出现写全称 "per-block SNR-driven estimator switching" |
| 34 | **net SNR gain** | 净 SNR 增益 | 脚注："net of the pilot power penalty of 1.25 dB (10log10(4/3)); BER computed over data symbols" | 替代自造词 fair_gain（S003）。"SNR gain" 标准但需注明 pilot overhead 口径（D004 教训）| SNR gain = B11 L191（"2 dB SNR gain"）；口径标注 = D004 |

#### ③ 自造词替换（不变量 6 黑话禁令，零容忍）

| 自造词（禁用）| 替换为 | 理由 |
|---|---|---|
| **fair_gain** | **net SNR gain** + 脚注（#34）| fair_gain 是自造合成词（S003 审计）。领域标准 = SNR gain + 显式标 pilot overhead 口径 |
| **A4** | **per-block SNR-driven estimator switching**（#33）| A4 是内部项目代号。论文用功能描述名 |
| **A4-B11-Q1** 等内部编号 | 禁用，全部用功能描述 | 内部编号不进论文 |
| **MSM / MSDM** | **禁用**（不引入）| MSDM 是 Wang 论文的决策指标（papers/doi/10.1364_oe.564097/），跟我们的 per-block SNR 切换不同构，不借用其缩写 |
| **"伪地板" / "error floor"**（deep fade 描述）| **禁用**，用 "slope reduction" / "deep fade"（不变量 5）| H002 推翻"伪地板"预判，BER 全程单调降 |

---

### 表 2：符号表

全篇统一无冲突。对齐 A 组 + B11 + sat.1553 惯例。参数值留给 P2 参数表，此表只定符号。

| 符号 | 含义 | 对齐惯例（别人用啥）| 首次出现节 |
|---|---|---|---|
| `r_k` | 第 k 个接收信号样值（复基带）| B11/sat.1553 用 r | §II System Model |
| `p` | 已知 pilot 符号（|p|=1 单位模）| Le Bidan/OECC-PSC pilot symbol | §II |
| `p*` | p 的复共轭 | 标准 | §III |
| `h_b` | 第 b 个信道块的衰落系数（块内恒定，块间独立）| 标准（wireless block fading）| §II |
| `θ` | 载波相位（真值）| **V&V 1983 / sat.1553 用 θ**（注：B11 用 φ，本论文从 V&V）| §II |
| `θ̂` | 载波相位估计 | sat.1553 θ̂ | §III Method |
| `θ̂_DA` | DA 估计器输出相位 | 本工作定义（H007 锁定）| §III |
| `θ̂_NDA` | NDA 估计器输出相位 | 本工作定义（H007 锁定）| §III |
| `M₀` | 升幂次数（=8，(8,8)-16APSK 每环点数）| **B11 L75-77 用 M₀**（`_b11_params.py:36 M0=8`）| §II |
| `γ` | 信噪比 SNR（Es/N₀）| 通用（A 组多用文本 "SNR"，γ 为公式中的标准符号）| §II |
| `γ_blk` | 每块 SNR（per-block SNR，定义见术语 #30）| 本工作定义 | §III |
| `γ_th` | 切换阈值 SNR（crossover，术语 #31）| 本工作定义 | §III |
| `α`, `β` | Gamma-Gamma 信道形状参数 | **Al-Habash 2001 标准**（`_b11_params.py:78-82`）| §II |
| `σ²_θ` | 每符号 Wiener 相位噪声方差 | **B11 用 σ²_p**；本工作因用 θ 表示相位故 σ²_θ（首次出现注明 "= σ²_p in [B11]"）| §II |
| `Δν` | 激光线宽 | sat.1553 L394 / OECC-PSC L115（`_b11_params.py:46 LASER_LW=10kHz`）| §II |
| `N₀` | 噪声单边功率谱密度 | 标准（注意：N₀ ≠ N_blk，下标 0 是噪声标准记法）| §II |
| `E_s` | 每符号能量 | Le Bidan/Paillier Es/N₀ | §II |
| `T_s` | 符号周期 | 标准（`_b11_params.py:48 T_S=1/R_SYM`）| §II |
| `R_sym` | 符号率 | 标准（`_b11_params.py:47 R_SYM=2.5e9`）| §II |
| `N_blk` | 信道块长度（h 恒定的符号数 =100）| 本工作定义（`_b11_params.py:39 CH_BLOCK=100`）| §II |
| `N_DFT` | DSP 处理块长度（=256，逐块恢复块大小）| **B11 L155 N_DFT=256**（`_b11_params.py:35`）| §II |
| `P_b` | 误比特率 BER | 标准（纵轴用文本 "BER"，公式用 P_b）| §IV Results |

**符号无冲突检查**：
- `N₀`（噪声 PSD）vs `N_blk`（信道块长）vs `N_DFT`（处理块长）：下标不同（0 / blk / DFT），无歧义 ✓
- `θ`（相位）vs `γ`（SNR）vs `h`（信道）：不同物理量不同字母 ✓
- `M₀`（升幂次数 =8）不与 `M` 冲突——论文中 M 仅在 "M-APSK"（调制族名）出现，公式中只用 M₀ ✓
- `σ²_θ`（PN 方差）vs `σ²_R`（Rytov 方差）：下标不同（θ / R），无歧义 ✓
- `α`/`β`（GG 参数）不与其他冲突 ✓

---

### 表 3：公式清单

粒度 = **直接给结论级**（对齐 R010 §2.3 / Panasiewicz）。每个公式 1 行 + 1 句话解释。不推导（squaring loss 引 V&V 1983）。

| # | 公式 | 物理含义 | 来源（代码行 / 文献）| 呈现粒度 |
|---|---|---|---|---|
| 1 | **θ̂_DA = angle(r_p · p\*)** | DA 估计器：用已知 pilot 符号 p 去除调制，取接收 pilot 样值 r_p 的相位。r_p = pilot 位置的接收样值，p* = conj(p)。| 代码 `_recovery.py:153`：`theta = np.angle(rx[pilot_idx] / pilot_sym)`（/pilot_sym = ·conj(pilot_sym) 当 |p|=1）| 直接给结论级。1 行 + 1 句话："removes modulation by dividing the received pilot sample by the known pilot symbol" |
| 2 | **θ̂_NDA = (1/M₀) angle(Σ_k r_k^{M₀})** | NDA 估计器：将块内所有接收样值升 M₀=8 次幂去除调制（M₀=8 对 (8,8)-16APSK 每环 8 点），取均值相位后除以 M₀ 恢复载波相位。| 代码 `_recovery.py:213,232-233`：`raised = rx ** M0` → `phi_raised = np.angle(raised.mean())` → `phi_est = phi_raised / M0`。M₀=8 = `_b11_params.py:36`（B11 L75-77）| 直接给结论级。1 行 + 1 句话："raises the received samples to the M₀-th power to remove modulation" |
| 3 | **γ_blk = |h_b|² · E_s / N₀** | 每块 SNR：信道块 b 内衰落系数 h_b 恒定，γ_blk 是该块的瞬时 SNR。接收端据此感知信道条件选择估计器。切换规则（文字，不编号）：select θ̂_DA when γ_blk < γ_th, else θ̂_NDA。| 定义依据：块衰落模型（术语 #32）+ `_b11_params.py:39 N_blk=100`（h 块内恒定）| 直接给结论级。1 行 + 1 句话定义 + 切换规则用文字（不用编号公式） |

**不进正文的公式**（系统模型参数，进 P2 参数表）：
- Gamma-Gamma PDF：参数 α/β 值进参数表，不给 PDF 公式（R010 §2.1 决定给模型名 + 块结构，不给完整 PDF）
- squaring loss 公式：引 V&V 1983 文字结论（"the Mth-power estimator suffers from squaring loss at low SNR [V&V 1983]"），不推导
- pilot overhead = 10log10(4/3) = 1.25 dB：文字给数字 + 引 Shieh-Djordjevic 2010，不编号为公式
- σ²_θ = 2πΔνT_s：参数定义级，进符号表说明，正文一句话带过

---

### 交叉一致性检查

三表交叉验证，确认无冲突：

#### 检查 1：公式中用的符号 = 符号表里定的

| 公式 | 用的符号 | 符号表对应 | 一致？|
|---|---|---|---|
| 公式 1 | θ̂_DA, r_p, p, p* | θ̂_DA(#符号表), r_k→r_p, p, p* | ✅ r_p 是 r_k 在 pilot 位置的特例，一致 |
| 公式 2 | θ̂_NDA, M₀, r_k | θ̂_NDA, M₀=8, r_k | ✅ |
| 公式 3 | γ_blk, h_b, E_s, N₀, γ_th | γ_blk, h_b, E_s, N₀, γ_th | ✅ |

#### 检查 2：术语表"显式定义"的词 = 公式清单有对应公式支撑

| 显式定义术语 | 对应公式 | 支撑？|
|---|---|---|
| per-block SNR (#30) | 公式 3（γ_blk = |h_b|²E_s/N₀）| ✅ 有定义公式 |
| crossover (#31) | 公式 3 切换规则（γ_th）| ✅ γ_th 在切换规则中出现 |
| net SNR gain (#34) | 无独立公式（结果数字，进 P2 表）| ✅ 不需要公式，是结果量 |
| block fading (#32) | 公式 3 前提（h_b 块内恒定）| ✅ 公式 3 的 h_b 定义支撑 |
| estimator switching (#33) | 公式 3 切换规则 | ✅ 切换规则 = "select θ̂_DA when γ_blk < γ_th, else θ̂_NDA" |

#### 检查 3：无自造词残留

| 自造词 | 表中处理 | 残留？|
|---|---|---|
| fair_gain | ③替换为 net SNR gain | ✅ 全表用 net SNR gain / SNR gain |
| A4 | ③替换为功能描述名 | ✅ 全表无 A4 |
| MSM / MSDM | ③禁用 | ✅ 全表无 |
| "伪地板" | ③禁用 | ✅ 术语 #15 deep fade 注明守不变量 5 |

#### 检查 4：同一符号不表两义 / 同一概念不用两符号

- SNR：统一用 `γ`（公式）/ "SNR"（文本），per-block 用 `γ_blk`，阈值用 `γ_th`。✅ 无两符号
- 相位：统一用 `θ`（真值）/ `θ̂`（估计）。B11 用 φ 但本论文从 V&V 用 θ，首次出现注明对应关系。✅ 无两符号（B11 的 φ 不进本论文）
- 升幂次数：统一 `M₀=8`。✅ 不用 M（M 仅在 M-APSK 族名出现）
- 块长：信道块 `N_blk=100`（h 恒定），处理块 `N_DFT=256`（DSP 恢复块）。✅ 两个不同概念两个不同符号，无混淆

**交叉一致性检查结论：全部通过 ✓**

---

## 结论

D-P1 用语+符号+公式三合一完成。三张表定死全篇英文零件：

1. **术语表**：34 词（29 标准 + 5 显式定义 + 5 自造词替换映射）。每个标准词标 A/C 组查证来源（哪篇哪行），自造词全标替换。重点决定：
   - CPE/CPR 分工：CPE = 估计操作（方法节），CPR = 整体流程（Intro/标题）
   - DA = pilot-aided（统一用 DA，首次出现注明）
   - per-block SNR + crossover + block fading + estimator switching + net SNR gain 五个词需显式定义（A/C 组无先例），均已给定义句
2. **符号表**：22 个符号，全篇统一无冲突。关键选择：相位用 θ/θ̂（从 V&V 1983/sat.1553，非 B11 的 φ，首次出现注明对应）；SNR 用 γ（文本写 "SNR"）；M₀=8（B11 惯例）
3. **公式清单**：3 个核心公式（DA/NDA/per-block SNR），全直接给结论级，标代码行溯源（`_recovery.py:153/213,232-233`）。系统模型参数不进正文公式（进 P2 参数表）

## 对决策的影响

- **不新建 D###**：本文件是 research note（D-P1 产出），不改方向/架构决策。所有术语查证基于已有 content.md（守 FR-22），符号选择基于代码 + A 组惯例。
- **口径标注待 P2 定**：net SNR gain 的具体口径（naive vs fair 报哪个为主）是 P2 活（D004 已定倾向 naive +1.26~1.85 dB），P1 只锁术语名 + 脚注模板。
- **θ vs φ 选择记录**：本论文选 θ（V&V/sat.1553）而非 B11 的 φ。W2 写 System Model 时首次出现注明 "θ (denoted φ in [B11])"。如 P3/W2 觉得跟 B11 对齐更重要可讨论切回 φ，但目前 θ 更通用。
- **守质量红线 6 条全过**：①不自造词（③表全替换）②不深挖（squaring loss 引 V&V）③口径标注（net gain 脚注模板）④守 FR-22（只读 content.md）⑤三表无冲突（交叉检查通过）⑥代码行溯源（DA/NDA 标 `_recovery.py` 行号）。
