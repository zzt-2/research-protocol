# L05 全文精读：Yu et al., TVT 2023

> Groundwork Step 3 only | fresh-context reader | 2026-08-09
> 论文：*Joint Physical Layer Frame Optimization and Carrier Synchronization for Satellite Communications*
> 角色边界：C3 stepwise-correlation prior-art ceiling；不是 coherent-FSO 直接竞品，不承载 target defect、novelty 或 Go 判断。

## 0. 身份、canonical 路径与预检结论

**Verdict：PASS。** 派遣标题与正文首个实际论文 H2 完全一致（`papers/doi/10.1109_tvt.2022.3218937/content.md:5`），正文 DOI 为 `10.1109/TVT.2022.3218937`（同文件 `:23`），作者为 Zhongyang Yu 等（`:7`）。`source.meta.json` 的 `real_title` 错取期刊页眉，故其中 `title_check=mismatch` 不是论文身份冲突。

| 项 | 复核值 | 证据 |
|---|---|---|
| DOI / 来源 | `10.1109/TVT.2022.3218937`；IEEE Xplore 期刊正式版本 | `content.md:23`；页眉及版权信息 `:3,31-33` |
| canonical adapter | `D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/papers/doi/10.1109_tvt.2022.3218937/content.md` | 本轮实际读取路径 |
| shared source | `D:/code/study/research-protocol/papers/doi/10.1109_tvt.2022.3218937/source.md` | Step 3 receipt 的 L05 条目 |
| adapter receipt 指针 | `search-archive/2026-08-09/rml-fsts-step3-read-receipt.json` → `papers[id=L05]` | receipt：`preflight_status=PASS_5_OF_5`、L05 `verdict=PASS` |
| 字节 / SHA-256 | 两端均为 `72748` bytes；两端 SHA-256 均为 `97DB13AB40E6548AE70A01C12027B7085CA3123976353C5683DAE3350D8924A6` | 本轮 `Get-Item`/`Get-FileHash` 复算；receipt L05 条目 |
| title overlap | `1.0`；byte-identical=`true` | receipt L05 条目；`content.md:5` |
| 发表状态 | 已正式发表；2022-11-02 online publication，2023-03-14 current version | `content.md:17` |
| 发表渠道 | *IEEE Transactions on Vehicular Technology*, Vol. 72, No. 3 | `content.md:3` |
| 年份 | 卷期年份 2023；版权/DOI 年份 2022 | `content.md:3,17,31` |

## 1. 核心贡献与方法概述

### 1.1 核心贡献

1. 论文把标准 PSAM 推广为可调各 pilot/data block 长度的 G-PSAM，推导 CFO、TD、PO 的 DA/NDA/DA&NDA CRB，并用近似 DA&NDA CRB 与 control-variate method 给出 OG-PSAM 的低复杂度优化准则（`content.md:47-53,123-211`，§III，Eq. (3)–(14)）。
2. 论文以无偏 AC 值构造 frequency-phase decoupler，引入 impact factor `n`，把 CFO→PO 的串行 SFPE 改为并行 PFPE；随后用 M-PFPE 在 CFO 接近零时切回 SFPE 的 PO estimator，以减弱 PFPE self-noise（`content.md:227-369`，§IV，Eq. (15)–(28)，Table II）。
3. 论文提出确定性的 stepwise correlation CFO estimator：先用同一 pilot block 的两级 AC 获得宽捕获和较细估计，再用多对不相交 pilot blocks 的 CC 逐级消除残余 CFO；最终估计是两级 AC 与 CC 残差之和（`content.md:371-439`，§V，Eq. (29)–(37)）。

### 1.2 方法概述（2–3 句）

接收端在符号率采样后先移除已知 pilot modulation，形成单音加噪声序列 `z(k)`，再以 AC/CC 的 argument 构造 CFO 估计；frequency-phase decoupler 通过 `z(k)` 与特定 AC 值的共轭补偿，把有效时间原点移到 pilot 中部，使 PO 分支不再依赖先执行 CFO compensation（`content.md:229-339`，Eq. (15)–(27)）。CFO 分支依次执行 `AC1 → compensation → AC2 → compensation → CC residual refinements`，得到 coarse-to-fine 的 stepwise estimator；框架侧则用 OG-PSAM 拉开 pilot blocks、非均匀配置 data blocks，以换取更好的 CFO CRB 与 BER（`content.md:175-217,371-439`，Eq. (10)–(14), (29)–(37)）。

## 2. 七个结构化子表

### A. 真实信号输入

| 输入 | 内容 | 证据 |
|---|---|---|
| 原始接收样本 | `r(k)=s(k-τ)·exp(j(2π f_d T_s k+θ))+n(k)`，`k∈κ_p∪κ_c`；符号率采样，AWGN | `content.md:57-103`，§II，Eq. (1) |
| pilot 输入 | 多个不相交 pilot blocks `p_i`，长度 `L_i`，由 `κ_p` 索引；已知 pilot 用于 modulation removal | `content.md:85-103,127-135,227-245`，Eq. (15)–(18) |
| data 输入 | 多个 data blocks `c_j`，长度 `M_j`；长包 feedback 模式下 decoder posterior 形成软参考信号 | `content.md:85-121`，§II，Eq. (2) |
| decoupler 输入 | 第一 pilot block 的 `z(k)` 与 `R(α_1)`，其中 `α_1=(L_1-1)/(2n)` | `content.md:255-285`，Eq. (19)–(21) |
| stepwise CFO 输入 | 第一 pilot block 的 shift-AC 序列，以及第一块与后续 pilot blocks 之间的 CC 序列 | `content.md:371-427`，§V，Eq. (29)–(36) |

### B. 估计器 / 控制器输出（不是 action space）

| 模块 | 输出 | 证据 |
|---|---|---|
| timing front-end | `τ̂`（本文假设由稳健 timing estimator 获得，非本文核心） | `content.md:103,229-235`，Eq. (15) |
| 两级 AC | 初始 CFO `f̂_d,AC1` 与第二级 CFO `f̂_d,AC2` | `content.md:385-409`，Eq. (30)–(33) |
| 多级 CC | 每一级残差 `Δf̂_d,CC(i)` 及其和 `Δf̂_d,CC` | `content.md:411-427`，Eq. (34)–(36) |
| 最终 CFO | `f̂_d=f̂_d,AC1+f̂_d,AC2+Δf̂_d,CC` | `source.pdf` printed p.3525，Eq. (37)；转换正文 `content.md:429-431` 公式图缺失 |
| PFPE / M-PFPE | PO estimate `θ̂_P`；`n>1` 时用 Eq. (28) 修正；接近零 CFO 时 M-PFPE 采用 SFPE PO estimator | `content.md:325-369`，Eq. (25)–(28) |
| decoder | 估计数据 `d̂`；长包可经 fine CFO/PO feedback 迭代恢复 `d` | `content.md:103-121`，§II |

### C. 奖励 / 真实目标与评价量

**奖励：N/A（非学习型确定性 DSP；无 policy、reward 或训练过程）。**

| 类型 | 真实目标 / 评价量 | 公式或位置 |
|---|---|---|
| frame 优化目标 | 在 pilot/data 总长度与正整数约束下最小化 `CRB(f_d)_DA&NDA`；论文以最大化其倒数的等价形式并用 CVM 得出 block-length 次序 | `content.md:169-205`，§III-B，Eq. (9)–(13) |
| CFO 评价 | `RMSE(f̂_d)`，并与 DA CRB 对照 | `content.md:469-505`，Fig. 11–12 |
| PO 评价 | bias/average estimate 与 MSE，扫 `θ`、normalized CFO `f_dT_s` | `content.md:445-465`，Fig. 8–9 |
| end-to-end 评价 | BER vs. `E_b/N_0`；另给估计范围、pilot overhead 与乘加复杂度 | `content.md:467,523-587`，Fig. 10, 13–16；Table III |

### D. 建模假设、位置与迁移影响

| 假设 | 论文位置 | 对目标 coherent-FSO 迁移的影响 |
|---|---|---|
| satellite uplink 为 AWGN，单位平均符号能量；无衰落、湍流、空间分集或 AO | `content.md:57-93`，§II，Eq. (1) | **重大限制**：不能外推到星地 coherent-FSO 的 turbulence/AO/branch imbalance/shot-noise 场景。 |
| 符号率采样，TD 可由 pilot 在 CFO 存在时准确提取；后文聚焦 CFO+PO | `content.md:87-103` | 迁移时需另验 timing error、oversampling 与光接收前端误差；本文不提供这些鲁棒性证据。 |
| modulation removal 的 argument 近似要求高 SNR，`Re{v},Im{v}≈0` | `content.md:229-235`，Eq. (15)–(16) | 低接收功率下近似可能失效；本文并未建立 FSO 的 low-power lag-ranking crossover。 |
| PFPE 推导常忽略 `ψ'_k` / 假设高 SNR；有效 PO/CFO 范围由 `n,L_1` 决定 | `content.md:279-339,351-369`，Eq. (21)–(28) | `n` 形成确定的捕获范围/自噪声折中，但不是 target 条件化 lag 失败的证据。 |
| 数据符号等概独立；fine stage 依赖 decoder posterior / 正确统计平均 | `content.md:59-61,105-121,141` | 编码/软判决错误会反馈到估计器；光链路编码与 burst 结构不同需重建证据。 |
| OG-PSAM block 长度用引用 [37] 的 Monte-Carlo 参数选择法 | `content.md:209-211` | 给出参数选择入口但未报告算法细节/随机配置，迁移复现不闭合。 |

### E. 网络架构 / DSP 链、参数与复杂度

**网络架构：N/A（非神经网络、非 DRL/监督学习）。**

| 项 | 内容 | 证据 |
|---|---|---|
| DSP 链 | encode → modulate pilot/data → G/OG-PSAM multiplex → symbol-rate receive → demultiplex → modulation removal → stepwise CFO + PFPE PO → feedforward correction → demod/decode；长包可 soft feedback fine synchronization | `content.md:57-121`，§II，Fig. 1 |
| AC1 | `N'=1, α_1=1`，`f̂_d,AC1=[1/(2πT_s)]arg R'(1)`，范围 `|f̂_d,AC1T_s|≤1/2` | `content.md:385-397`；`source.pdf` printed p.3525，Eq. (30)–(31) |
| AC2 | `N'>1, α_1>1`，范围 `|f̂_d,AC2T_s|≤1/(N'+1)`，归一化系数 `1/[π(N'+1)T_s]` | `content.md:399-409`；Eq. (32)–(33) |
| CC stage | `α_1i=Σ_{j=1}^{i-1}(L_j+M_j)`；单级范围 `|Δf̂_d,CC(i-1)T_s|≤1/(2α_1i)`；循环至 `m'≤m-1` | `content.md:411-427`；Eq. (34)–(36) |
| PFPE 参数 | `α_1=(L_1-1)/(2n)`；`n=1` 时 `|f_dT_s|≤1/L_1` 且完整 `|θ|<π`；`n>1` 时 anti-CFO 范围扩大到 `n/L_1`，PO 范围缩小 | `content.md:255-285,351-367`；Eq. (19)–(28) |
| PO 乘法量 | PFPE PO estimator 只需 1 次 complex multiplication，SFPE 需 `L_1/n` 次（两者 CFO estimator 相同） | `content.md:325-339`，Table II |
| CFO 复杂度 | P&R、M&M 的 RMULTI 量级为 `L_p²`；本文估计器乘法量主要依赖 `m'≪L_p²`。Table III 数字单元在转换中为图片，不能从 canonical markdown 完整辨认 | `content.md:507-521`，Table III；`source.pdf` printed p.3528 |

### F. 适配性

| 类型 | 判断 | 证据边界 |
|---|---|---|
| 适配 1 | stepwise `AC wide-range → AC refine → multi-block CC residual refine` 是明确、可复用的 deterministic coarse-to-fine correlation 先例，可作为 RML-FSTS 的 C3 prior-art ceiling | `content.md:371-439`，Eq. (29)–(37) |
| 适配 2 | 明确展示 lag / separation（`α`）决定无模糊范围、估计精度与复杂度，适合约束未来多 lag 主张的措辞 | `content.md:243-251,373-439` |
| 不适配 1 | 场景是 satellite RF uplink + AWGN，不是 coherent-FSO；无 turbulence、space diversity、AO、received optical power 或 branch reliability | `content.md:57-93,589-591` |
| 不适配 2 | 本文没有检验固定 lag 在 modulation / training / received-power 条件下的 ranking crossover，也没有比较 conditioned single-lag lookup | 全文实验仅 `content.md:441-587`；该 target 命题不存在于本文 |
| 未来原料启示（非设计） | 若后续合法进入方法构造，任何“多 lag / 分级相关”贡献都必须显式区别于本文的固定 stepwise AC+CC 计算图，并对照同等 pilot overhead 与复杂度 | **INFERENCE**，由 §V prior-art 结构推得；不构成 novelty 或 Go 结论 |

### G. 本文自身问题 M/C/A 与 canonical 四判据

| 字段 | 内容 | 证据 |
|---|---|---|
| M | 标准 S-PSAM + SFPE；以及 M&M 单块 AC / P&R recursive multi-block AC 等 CFO estimator | `content.md:29-45`，§I |
| C | pilot/storage 受限、large Doppler/CFO 的 satellite uplink；短包与长包 | `content.md:15-25,41-45,441-443` |
| A | SFPE 的 PO stage 隐含要求前级 CFO 足够准确，残余 CFO 会累积为 phase ambiguity；现有 CFO estimator 存在捕获范围—精度—复杂度折中，S-PSAM 固定结构限制灵活性/CRB | `content.md:39-45,253-339`，Eq. (23)，§IV-B |
| A 定位 | 机制定位在 Eq. (23)：仅当 `|Δf_dT_s|≈0` 时 SFPE PO 工作良好；否则 argument 周期性导致 ambiguity。估计器折中定位在 §I 与 §V 开头 | `content.md:313-323,371-373` |
| 方法产出形态 | 可复用的 OG-PSAM frame-optimization 规则、PFPE/M-PFPE DSP 模块、stepwise AC+CC CFO algorithm | `content.md:47-53,175-217,305-439` |
| 判据 1：具体 M-C-A | ✅。M、受限 satellite uplink C、以及 frequency-to-phase coupling / estimator trade-off A 均明确且有解析式定位 | 上述 M/C/A 证据 |
| 判据 2：可复用方法产出 | ✅。产出为确定性 frame rule + decoupler + 7-step CFO 估计流程，不是纯分析描述 | §III–V，Eq. (10)–(37) |
| 判据 3：近期 baseline | ❌（按 2026 Step 3 严格口径）。实测核心 estimator baselines 是 M&M 1997 与 P&R 2011；S-PSAM/SFPE 为结构型基线，未给 2022–2026 同任务强近期 estimator 对比 | `content.md:43-45,469-521,639-673` |
| 判据 4：可量化对标 | ✅。RMSE/MSE/BER、CRB、捕获范围、pilot overhead 和复杂度均可量化 | `content.md:441-587`，Fig. 8–16，Table III |
| 本文自身四判据 | **3/4；不全过**。这只评价本文自身问题表述在当前口径下的可用性，不是 target Q 裁决 | FACT + 当前框架口径 |

## 3. 实验设置与通信参数

| 参数 | 论文设置 | 来源 |
|---|---|---|
| 链路 / 场景 | satellite uplink；feedforward 与 feedback carrier synchronization；短包和长包 | `content.md:57-59,523-525` |
| 信道 | complex AWGN，噪声方差 `N_0/2`；multipath Rician 仅列为未来工作 | `content.md:59,89-93,589` |
| 采样率 / 符号率 | 接收在 symbol rate 采样；未报告绝对 symbol rate、sample rate 或载波频率 | `content.md:87-89` |
| 未编码调制 | QPSK（§VI-A/B） | `content.md:441-443` |
| coded modulation 1 | `(225,173)` NB-LDPC over GF(16) + 16-QAM，短包 | `content.md:527-535` |
| coded modulation 2 | binary `(576,288)` LDPC（IEEE 802.16e）+ SCMA T4QAM，短包 | `content.md:537-555` |
| coded modulation 3 | binary `(6144,1024)` LDPC（3GPP）+ GMSK；`h=1/2, L=2, BT=0.5`（CCSDS），长包 | `content.md:557-581` |
| PFPE test frame | `L_1=11`；`n=1` 给 `|f_dT_s|<0.09, θ∈[-π,π)`，`n=2` 给 `|f_dT_s|<0.18, θ∈[-10π/11,10π/11)` | `content.md:445-459` |
| PFPE sweeps | Fig. 8：`E_b/N_0=9 dB`，`f_dT_s≤0.06` (`n=1`) / `≤0.15` (`n=2`)；Fig. 9：`θ=π/4`，CFO 扫 `[-0.09,0.09]` / `[-0.18,0.18]`；Fig. 10：`f_dT_s=0.4, M_c=128` | `content.md:455-467` |
| CFO-estimator frame | `m=3, L_p=60, M_c=680, η≈0.09`；OG：`(L1,M1,L2,M2,L3,Mr)=(23,80,14,600,23,0)`；S-PSAM：`(20,80,20,80,20,520)` | `content.md:469-503` |
| Example 1 frames | `L_p=45, M_c=225, η≈0.2`；OG1 `(18,50,9,175,18)`，OG2 `(15,50,15,175,15)`，S-PSAM `(15,112,15,113,15)` | `content.md:527-535`；缺失行由 `source.pdf` printed p.3528 核对 |
| Example 2 frames | `L_p=24, M_c=144, η≈0.16`；OG1 `(9,44,6,100,9)`，OG2 `(8,44,8,100,8)`，S-PSAM `(8,72,8,72,8)` | `content.md:537-553` |
| Example 3 frames | `L_p=300, M_c=6144, η≈0.05`；OG1 `(120,1536,60,4608,120)`；S-PSAM `(100,3072,100,3072,100)`；OG2 的完整 frame 行在转换中缺失 | `content.md:557-579` |
| feedback iterations | 5 | `content.md:581` |
| pilot-overhead scan | `η=0.01, 0.05, 0.1`，对应 pilot block 分别 20/100/200 symbols | `content.md:583-587` |
| CFO / phase noise | CFO 用 normalized `f_dT_s`；PO 用 `θ`；未建模 oscillator phase noise / linewidth | §II、§VI-A；全文未报告 phase-noise process |
| 接收功率 / SNR | 使用 `E_b/N_0`；明确数值 9 dB 出现在 Fig. 8/9/12 设置。未报告绝对接收功率，其他图的完整 sweep 点因图像转换缺失而不可辨认 | `content.md:457-459,505` |
| 湍流 / 空间分集 / AO | 均未报告、未建模 | AWGN model `content.md:57-93` |
| 参数来源 | DVB-S2 preamble、IEEE 802.16e LDPC、SCMA T4QAM、3GPP LDPC、CCSDS GMSK；frame block 选择依赖 [37] Monte-Carlo 方法 | `content.md:455,537-557,209-211` |

## 4. Baseline 逐项审计

| baseline / bound | 类型 | 本文如何使用 | 自实现 / 引用 / 无 |
|---|---|---|---|
| SFPE | 传统串行模式 | 与 PFPE 比 PO bias/MSE 与 overall BER；两者使用相同 Eq. (19) AC CFO estimator，PO 分别为 Eq. (23)/(26) | **本文自实现的结构型 baseline**；背景引用 [22]–[25]，但实验不是复现某一篇具体实现（`content.md:307-339,445-467`） |
| S-PSAM | 标准 frame baseline | 与 OG-PSAM 保持相同 `L_p/M_c`，比较 CFO RMSE 与 coded BER | **本文自实现**；结构引用 [20],[21]（`content.md:495-503,525-587`） |
| P&R estimator | recursive AC/Kalman CFO | 同一 pilot sequence 下比 RMSE、范围、复杂度 | **引用算法 [21] + 作者仿真实现**；未提供复现代码/调参细节（`content.md:43-45,505-521,673`） |
| M&M estimator | weighted AC CFO | 同上；主张本文消除其 phase ambiguity | **引用算法 [28] + 作者仿真实现**；未提供复现代码/调参细节（`content.md:43-45,505-521,641`） |
| DA CRB | 解析 bound | Fig. 11 对照 estimator RMSE，非可实现算法 | **本文公式计算**，Eq. (7)（`content.md:145-155,503`） |
| no-CFO optimal | synthetic oracle | coded BER 图中的“optimal performance” | **本文生成的理想上界**，非 baseline 方法（`content.md:535,581`） |

公平性边界：同一 frame 对 P&R/M&M/本文 estimator 的比较声明使用同一 `L_p` 且不借 data sequence（`content.md:505-507`）；OG vs S-PSAM 保持总 pilot/data 长度，但两者 block geometry 不同，这正是被测变量。论文没有报告各引用 estimator 的独立调参预算、实现核对或代码，因此“公平复现”只能记为部分闭合。

## 5. 关键实验结论

1. PFPE 在 CFO 不接近零时维持较好的 PO MSE/近似无偏，而 SFPE 因残余 CFO 累积产生显著偏差；CFO 接近零时 SFPE 反而优于 PFPE，促成 M-PFPE 切换（`content.md:457-465`，Fig. 8–9）。
2. 对 `f_dT_s=0.4, M_c=128` 的 overall BER，PFPE 优于 SFPE，且在给定 CFO range 内对 `n` 较不敏感（`content.md:467`，Fig. 10）。
3. `m=3,L_p=60,M_c=680` 时，本文 estimator+OG-PSAM 的 RMSE 相对其 S-PSAM 版本改善约一个数量级；在 9 dB、不同 CFO 下，本文 estimator、P&R、M&M 捕获范围都接近半 symbol rate，但本文精度最高（`content.md:495-505`，Fig. 11–12）。
4. coded BER：Example 1 在 BER `10^-5` 时 OG1/OG2 距 no-CFO 上界约 0.5/0.8 dB，而 S-PSAM 已出现 error floor；Example 2 在 BER `10^-6` 时 OG1/OG2 损失约 0.5–0.6 dB，S-PSAM 同样 error floor（`content.md:527-555`，Fig. 13–14）。
5. 长包 Example 3、5 次 feedback：BER `10^-4` 时 OG1/OG2 损失小于 0.5 dB，S-PSAM 损失大于 0.8 dB并趋向 error floor；增大 `η` 使 BER 逐渐靠近 no-CFO 上界（`content.md:573-587`，Fig. 15–16）。
6. 复杂度主张仅闭合到量级：P&R/M&M 的 RMULTI 为 `O(L_p²)`，本文主要随 `m'` 变化且 `m'≪L_p²`；Table III 的完整单元格未能由 canonical markdown 转换，故不抄录不可辨认的精确加乘数（`content.md:507-521`，Table III）。

## 6. 实现关键细节与转换限制

- modulation removal：`z(k)=r(k)s*(k-τ̂)=exp(j(2πf_dT_sk+θ))+v(k)≈exp(j arg z(k))`；末个近似要求高 SNR（§IV，Eq. (15)–(16)；`content.md:229-235`）。
- 无偏 AC：同 block 时 `w(α_i)=1/(L_i-α_i)`；CC：不同 blocks 时 `w(α_i0i1)=1/L_i0`，delay 为 block 间间隔和（Eq. (17)–(18)；`content.md:237-251`）。
- decoupler：`Z_k(n)=z(k)·R*((L_1-1)/(2n))`，把有效采样位置移至 `k'=k-(L_1-1)/(2n)`（Eq. (19)–(21)；`content.md:255-303`）。
- PFPE PO：Eq. (25) 对 `Z_k(n)` 求和再取 argument；Eq. (26) 给 `θ+πf_dT_s(1/n-1)` 的无模糊条件 `|f_dT_s|≤n/L_1`；Eq. (28) 用 `f̂_d` 校正 `n>1` 的相位项（`content.md:325-367`）。
- stepwise CFO：AC1 捕获半 symbol-rate，AC2 缩窄范围提高精度，CC 以越来越大的 pilot separation 对 residual 细化；每次估计后重补偿，最终按 Eq. (37) 求和（`content.md:385-431`；`source.pdf` printed p.3525）。
- frame optimizer 只给 block-length 次序/渐近规则；具体整数值由 [37] 的 Monte-Carlo selection 得到，本文未给足该选择算法的执行细节（`content.md:175-211`）。
- **转换限制**：canonical markdown 中 Eq. (3)–(14)、(17)–(37) 多数以“picture intentionally omitted”出现，Table I–III 亦为图片。本轮仅按授权用 shared `source.pdf` 核对 Eq. (15)–(37)、Example 1 缺失 frame 与 Table II/III；Table III 的细小数字单元仍不可可靠转录，因此只承重正文明确给出的量级结论。

## 7. 与 RML-FSTS 的关系及 source/target 证据边界

| 状态 | 陈述 | 依据 |
|---|---|---|
| **FACT / source-paper** | 本文已经公开了 stepwise correlation estimator：两级 single-block AC + 一组 multi-block CC residual refinements | §V，Eq. (29)–(37)，`content.md:371-439` |
| **FACT / source-paper** | correlation delay / pilot separation 控制无模糊范围，OG-PSAM geometry 能显著改变 CFO RMSE/BER | Eq. (17)–(18), (34)；Fig. 11–16，`content.md:243-251,495-587` |
| **FACT / source-paper** | 本文只在 satellite RF uplink AWGN 中验证；没有 coherent-FSO、turbulence、AO、spatial-diversity branch 或 received optical power 模型 | §II，`content.md:57-93` |
| **FACT / frozen task boundary，非 L05 证据** | source defect 仅指 Wang 2023 中 fixed lag/`BL` 随 modulation、training length、received power 而变及低功率 timing/FOE 退化；L05 不证明该 defect | T001 / 本次派遣边界；不得归因于本文 |
| **INFERENCE / target** | 本文构成 C3 prior-art ceiling：未来若使用 coarse-to-fine/multi-lag correlation，不能把“多级/多间隔融合”本身当作未有先例 | 从 §V 结构迁移出的 claim-boundary inference |
| **UNKNOWN / target** | 星地 coherent-FSO 中是否存在 lag-ranking crossover | 本文未做相应场景/条件扫描 |
| **UNKNOWN / target** | dev-frozen modulation/TS/receiver-power-conditioned single-lag lookup 是否失败 | 本文无该 comparator |
| **UNKNOWN / target** | RML-FSTS 的 target defect、headroom、novelty、Go/No-Go | 超出 Step 3 与本文证据范围 |

结论：L05 对 RML-FSTS 的唯一合法作用是**限制先验艺术与未来主张边界**。它不能证明 Wang 2023 的 source fixed-lag defect，更不能把 RF/AWGN 结果迁移成 coherent-FSO target defect；也不授权设计 RML-FSTS 或进入 Step 3.5/4a。

## 8. 适配 / 不适配 / 未来原料汇总

- **适配**：提供明确的 coarse-to-fine stepwise correlation DSP 计算图；提供 separation–range–accuracy–complexity 的解析约束，可作为对照/claim ceiling。
- **不适配**：无 coherent-FSO 物理；无 condition-dependent lag-ranking、fixed-lag regret 或 conditioned lookup 对照；关键 baseline 偏旧。
- **未来原料**：可复用其同 pilot-overhead、公平 frame geometry、RMSE/BER/complexity 三层评价维度，但这只是后续证据设计原料，不是本轮方案设计。

## 9. 开源代码

**UNKNOWN / 未报告。** canonical 正文没有 repository、supplementary code 或公开实现链接；因此只能陈述“论文正文未报告开源代码”，不能据此断言互联网不存在作者代码（全文检索位置：`content.md` 全文；参考文献止于 `:681`）。

## 10. 实验完备性（≤20 行）

1. Claims/scope：覆盖 frame CRB、PFPE/SFPE、CFO RMSE/复杂度、coded BER；限 satellite uplink AWGN。
2. seeds/次数：仅称每个点平均“massive independent trials”，未报告 trial 数与 random seed（`content.md:471`）。
3. error bar / CI / 统计检验：均未报告；图为均值曲线。
4. baseline 数量：主要 4 类——SFPE、S-PSAM、P&R、M&M；另有 DA CRB 与 no-CFO ideal bound。
5. baseline 来源：P&R [21]、M&M [28]、S-PSAM [20],[21]；SFPE 背景 [22]–[25]。
6. 公平性：P&R/M&M/本文 estimator 声明同 `L_p`、不借 data；OG/S-PSAM 总 pilot/data budget 相同；调参细节未报告。
7. 消融：有 PFPE vs SFPE、`n=1/2`、OG vs S-PSAM；没有逐级移除 AC1/AC2/CC 的组件消融。
8. 参数扫描：扫 `θ`、`f_dT_s`、`E_b/N_0`、pilot overhead `η`；`m'`,`N'` 等关键 stepwise 参数缺系统扫描。
9. 信道/参数来源：AWGN；DVB-S2/IEEE 802.16e/3GPP/CCSDS/SCMA 文献来源明确，绝对链路预算未报告。
10. 场景多样性：QPSK、16-QAM、SCMA、GMSK及短/长包；但信道始终 AWGN，未覆盖 Rician/FSO turbulence。
11. 复杂度：Table II/III 给 CMULTI/RMULTI/RADD 分析；无 wall-clock、memory 实测或硬件实现。
12. **Verification=2/3**：解析推导、CRB 和仿真趋势能内部交叉核对，但无代码、硬件结果或独立复现。
13. **Validation=2/3**：覆盖多种调制、编码与短/长包，但只有合成 AWGN，未覆盖 Rician、实测 satellite 或 coherent-FSO。
14. **Uncertainty=1/3**：无 CI/error bars/statistical test，仅“massive trials”定性说明。

## 11. 最终 Step 3 读者结论

L05 身份与 byte-identical canonical adapter 预检 **PASS**，全文精读字段完整到本任务要求。其确定性 DSP 贡献与实验足以把 stepwise AC+CC / multi-separation correlation 记为 C3 prior-art ceiling；但其 satellite-RF/AWGN 证据不能承担 coherent-FSO target defect、lag-ranking crossover、conditioned-single-lag failure、novelty 或 Go。本文自身 canonical 四判据为 **3/4**（近期 baseline 严格项失败），且本结论不推进 Step 3.5/4a。
