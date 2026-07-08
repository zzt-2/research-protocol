# 阶段 0.2 B11 行 33 假设核查

> B11-Q2 专题阶段 0.2 产出物 | 日期 2026-07-08 | 来源 S002
> 核查对象：B11 锚论文（10.1109_LPT.2024.3523478）行 33 假设"湍流/Doppler/CFO 已补偿"

## 结论（先讲）

**B11 行 33 "湍流/Doppler/CFO 已补偿" 是仿真简化（B11 没测湍流），不是物理假设（B11 没假设湍流可前置补偿）。**

- B11 **全文未建模 FSO 湍流信道**（grep turbulence/fading/gamma-gamma 全文仅 2 处：L15 引言背景 + L33 假设声明；无信道模型实现）
- B11 仿真信道 = **AWGN + Wiener 相位噪声**（L51 明示），不含湍流衰落
- L33 假设的作用 = **简化信号模型**（把湍流/指向/Doppler/CFO 从接收信号表达式里排除，只留 STO + CPE），不是论证"湍流可被前置补偿所以不需要建模"

**对 B11-Q2 的意义**：B11-Q2 加湍流信道验证 NDA-ML 是**真实物理缺口**——B11 声称适用于 FSO 但没测过湍流，B11-Q2 补这个验证维度。这正是开题 D001 的核心定位。

## 1. 行 33 原文 + 上下文

**L33 原文**（content.md，§II SIGNAL MODEL 开头）：
> "Assuming that the atmospheric turbulence effect, pointing error, Doppler shift and CFO have been totally compensated, the n-th received time-domain OFDM sample r(n) with the appearance of normalized STO and PN can be expressed as [Eq.1]"

**位置与作用**：
- 位于 §II SIGNAL MODEL 第一节，是**信号模型的起始假设**
- 作用：把接收信号 r(n) 简化为只含 STO（τ）+ CPE（φ）+ AWGN（w(n)），排除其他损伤
- 紧接其后（L37-51）给出 r(n) 的数学表达式 + OFDM 帧结构 + Wiener PN 模型

**这不是"物理假设"的证据**：
- 全文**无**"前置补偿方案"的设计/论证（没有 AO 算法/ATP/湍流补偿器的内容）
- 全文**无**"湍流可被补偿到什么程度"的讨论
- L33 是为了让 ML 估计器推导（§III）聚焦在 STO+CPE，是**数学建模的简化假设**，不是工程可行性的物理假设

## 2. B11 是否建模了湍流（核查）

**主线 grep B11 全文**（`papers/doi/10.1109_lpt.2024.3523478/content.md`）：

| 关键词 | 命中 | 含义 |
|---|---|---|
| turbulence | L15（引言）+ L33（假设） | 仅背景叙述 + 假设声明，无建模 |
| atmospheric | L15 + L33 | 同上 |
| fading | 0 | 无衰落建模 |
| gamma-gamma / gg | 0 | 无 GG 信道模型 |
| channel model | 0 | 无独立信道模型节 |

**B11 仿真信道**（§IV L51 + L155）：
- L51："θ(n) is the PN which is usually modelled as a Wiener process, where θ(n)−θ(n−1)=ν(n), ν(n)∼N(0,σ²_p) with σ²_p=2π·Δν·Ts... w(n) is the complex additive white Gaussian noise, with mean 0 and variance N₀"
- L155："Simulations are carried out via MATLAB... The DFT size is 256 and the CP length is 32-sample. The symbol rate is 25 GBaud."

→ **B11 信道 = AWGN + Wiener PN，无湍流衰落**。r(n) = X(n)·ejθ(n)·ej(2πτn/N) + w(n)，没有 h(n) 衰落项。

## 3. 判定：仿真简化 vs 物理假设

**是仿真简化**。理由：
1. **B11 没建模湍流**（grep 全文零信道模型）→ L33 不是"假设湍流可补偿后剩余影响"，是"根本没考虑湍流"
2. **L33 是信号模型简化假设**（数学上排除变量），不是工程可行性论证（物理上能否补偿）
3. **B11 团队定位**（D002 已查）：主体是 fiber CO-OFDM 相位噪声 ML 系列，B11 是 fiber+FSO 通用声明，FSO 部分未深入

**与"物理假设"的区别**：
- 物理假设 = "我假设湍流可以被前置 AO/ATP 补偿到可忽略程度，所以本文不建模"（隐含可行性论证）
- 仿真简化 = "本文信号模型只考虑 STO+CPE，其他损伤假设已处理"（纯数学简化，不论证可行性）

B11 属于后者。L33 的"totally compensated"是理想化简化词，没有配套的补偿方案或可行性分析。

## 4. 对 B11-Q2 的意义

**B11-Q2 加湍流验证是真实物理缺口**（不是"重复 B11 已做过的东西"）：
- B11 声称适用于 FSO（abstract "applicable to both fiber-optic and free space optical communications"）但**没测过湍流**
- B11 的 +2dB（vs DA ML，Fig.4）是在 **AWGN+PN** 信道下的结果，湍流下是否成立未知
- B11-Q2 加 Gamma-Gamma 湍流信道（复用 `common/_channel.py:gg_block`）重评 NDA-ML 是否保持增益——这是 B11 没做过的真实延伸

**与 NDA-ML B11-Q1 的衔接**：
- B11-Q1（step4a）已把 B11 从 OFDM 频域重定位到单载波时域（D002），并在 AWGN+湍流下验证 vs DA-ML +1.35~2.5dB（D005）
- B11-Q2 是在 B11-Q1 基础上**专门聚焦湍流维度的验证延伸**（B11-Q1 的湍流结果已含，B11-Q2 进一步做湍流下的 robustness 验证 + 与 VV/等权的湍流对照）

**注意**：B11-Q1（step4a D005）其实已经跑过湍流场景（weak/moderate/strong，D005 表里有 weak +1.20dB / moderate +1.92dB）。B11-Q2 的增量需在阶段 0.4 公平对照框架里明确——不能只是"重跑 B11-Q1 的湍流"，要有新验证维度（如 vs VV 的湍流鲁棒性对照，或 deep fade 下的行为分析）。

## 5. 残留问题（留阶段 0.3-0.4）

1. **B11-Q2 vs B11-Q1 湍流结果的增量**：B11-Q1 D005 已有湍流 fair gain 数字（weak +1.20 / moderate +1.92dB），B11-Q2 不能只是重复——需在阶段 0.4 明确新维度（如湍流下 vs VV 对照，或 deep fade robustness）
2. **湍流参数真相源**（阶段 0.5）：B11-Q2 的湍流参数（Cn²/σ²）必须从 common/_channel.py 继承（TL-13）+ 标文献来源（TL-26），不能自建
3. **"湍流已补偿"假设的工程现实**：真实星地 FSO 的湍流补偿靠 AO（自适应光学），AO 残余相位确实存在——B11-Q2 加湍流等于测"AO 补偿后残余湍流对 NDA-ML 的影响"，这个物理叙事要在论文里讲清

## 证据链

- B11 行 33 原文：`papers/doi/10.1109_lpt.2024.3523478/content.md` L33
- B11 引言湍流提及：L15
- B11 信道模型（AWGN+Wiener PN）：L51
- B11 仿真参数：L155（DFT 256 / CP 32 / 25GBaud）
- B11 无湍流建模：grep turbulence/fading/gamma-gamma 全文仅 L15+L33（主线核查）
- D002 B11 重定位：`step4a-mve-execution/decisions.md` L77 "B11 仿真未建模 FSO 信道（行 33 假设湍流/Doppler/CFO 已补偿）"
- D005 湍流结果：weak +1.20dB / moderate +1.92dB（step4a decisions.md D005 表）
