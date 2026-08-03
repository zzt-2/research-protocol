# Literature Notes — 星地相干 FSO 自适应编码调制 (AMC) Groundwork

> **Owner**: AMC 独立专题 `2026-08-02-fso-amc-groundwork`（D001）。**不覆盖** receiver 专题的 `literature_notes.md`（197KB receiver 产物，独立文件）。
> 创建: 2026-08-03（GW Step 3，S004/D004） | 最后更新: 2026-08-03
> 精读范围: 5 篇 CORE 全文（L023/L096/L146/Galijasevic/Nguyen2024）+ 边界 3 篇（L165 AO / L090 fixed-STTC / L075 classification）+ bibliographic 2 篇（Safi2019 abstract-only / L124 abstract-only，全文 BLOCKED）
> 每篇详细 read-note 在 `papers/_read_notes/{paper_id}.md`

## 步骤进度表（FR-22，与 master-state GW Progress 表一致）

| Step | 状态 | 完成日期 | commit | 产出 |
| ---- | ---- | -------- | ------ | ---- |
| 1 search | ✅（ACCEPTED_AFTER_BOUNDED_INTEGRITY_REPAIR, D002/V002） | 2026-08-02 | S003 commit | R001 landscape + shortlist 12 |
| 2 acquire | ✅（**STEP2_PASS_WITH_COHERENT_C_FAMILY_BLOCKED, D004/V005**）| 2026-08-03 | 本轮统一 commit | 5 CORE 全文（L023/L096/L146/Galijasevic/Nguyen2024）；C 族 BLOCKED |
| 3 read | ✅/**⚠ STEP3_VERDICT 见下**（本轮）| 2026-08-03 | 本轮统一 commit | 本文件 + 5 read-notes + 直接竞品矩阵 + Q# 表 |
| 3.5 supplement | ⬜ | | | 进 Step 4a 前必 ✅ |
| 4a feasibility | ⬜ | | | |

---

## 一、精读条目（CORE 5 篇，按 family 分组）

### Family A — MCS/功率控制（delayed/uncertain CSI 分支 + instantaneous-CSI 分支）

#### [Nguyen2024] Adaptive Rate/Power Control With ML-Based Channel Prediction for Optical Satellite Systems
- DOI/来源: 10.1109/TAES.2024.3403809 | 正式发表 | IEEE TAES 60(5):7498-7509, 2024 (Q1)
- 源文件路径: papers/doi/10.1109_taes.2024.3403809/content.md
- 发表状态/渠道: 正式发表 / IEEE TAES（引用目标顶刊）
- 核心贡献: 提出 SAMP（suboptimal adaptive modulation and power）方案，LEO 卫星在固定等时长 slot 内联合调整 K-QAM 星座阶数（K∈{4,8,16,32,64,128}）与 EDFA 离散发射功率，满足速率/outage/BER/Pmax 约束下最小化功耗；提出 multistep-prediction ESN 预测 CSI 克服 LEO 反馈时延（>相干时间），解析推导平均功率与能量效率。
- 方法概述: RX(UAV) 用 ESN 从 M=20 历史信道增益预测 N 步未来 CSI 反馈；TX 据预测 CSI 选 channel state j 与 transmission mode i，输出(Pt,j, K_Aj)。SAMP 通过 Alg.2-4 确定信道状态门限 h、模式门限 h*、关系向量 A。
- 实验设置: K={4,8,16,32,64,128}；速率 0.6/1/1.2Gb/s；zenith 50°/60°；σ_R²∈{0.0075,0.1020}；jitter 11.15-20.07μrad；ESN input=20/hidden=50/output=1，采样 1ms，837500 样本；对比 SVM/LSTM/GRU。
- Baseline: AM[6]（固定功率变星座）/ 理想 AMP[16]（连续功率上界）/ SAMP（本文）；ML: ESN vs SVM[34]/LSTM[35]/GRU[36]
- 关键结论: AM↔AMP/SAMP gap≈0.85dB @1Gb/s zenith 50°；SAMP 接近理想 AMP；ESN 在反馈时延下提升 EE ~110/160Mb/J，训练时间远<LSTM/GRU 精度相近。
- 与本研究关系: **直接竞品（family-A delayed-CSI/predictive rate+power）**
- 实现关键细节: ESN reservoir 状态更新 eq(10) `r̃(n)=f(W_i·[1;x(n)]+W·r(n-1))`，`r(n)=(1-α)r(n-1)+αr̃(n)`；输出 eq(9) `y(n)=W_o·[1;x(n);r(n)]`；训练 ridge `W_o=(XX^T+βI)^{-1}Y X^T` eq(13)。瞬时 BER `BER_j(h)=0.2·exp(-3·Pt,j²·h²/(2·σn²·(K_Aj-1)))` → **γ∝h²（IM/DD 风格，非 coherent）**。
- 开源代码: 无
- 验证状态: Crossref API 独立验证身份（title/authors/venue/vol/issue/pages/year/publisher 逐字段匹配）；SHA256 迁移一致。
- **关键覆盖缺口**: 非 coherent / 非 GG（弱 lognormal）/ 无 coded chain（HARQ 仅 related work[8]）/ sat-to-UAV 非 sat-ground / info uncertainty 仅反馈时延（排除估计/量化误差）。

#### [L146] Robust Joint Optimization for Efficient and Reliable FSO/RF Satellite-UAV-Terrestrial Networks With Random Fading and Imperfect Channel Information
- DOI/来源: 10.1109/JIOT.2025.3600439 | 正式发表 | IEEE IoT-J 12(21), 2025 (Q1)
- 源文件路径: papers/doi/10.1109_jiot.2025.3600439/content.md
- 核心贡献: FSO/RF SUTIN 下，imperfect CSI（Gaussian est error σ²=σ_n²/(N·P_t)）+ 随机 fading 下联合优化 MCS 模式选择 + 功率 + UAV 轨迹，最大化吞吐 s.t. FER + CSI 不确定性约束；推导 imperfect CSI 下 FER/速率闭式 + MCS 切换阈值闭式；DDPG(JOMPT) 解高维非凸。
- 与本研究关系: **adjacent（info-uncertainty 模块高度可移植，但 IM/DD+lognormal+无 coded chain）**
- **关键覆盖缺口**: 非 coherent（IM/DD 强度调制）/ 非 GG（lognormal）/ 无 HARQ/coded chain（coding rate 仅 3GPP MCS 表条目）/ sat-UAV-terrestrial 非纯星地。
- 详见 papers/_read_notes/L146_jiot_2025.md

#### [Galijasevic 2024] Predicting Channel Conditions for Adaptive LDPC Coding in a Fading Free-Space Optical Channel
- DOI/来源: 10.1109/OJCOMS.2024.011100 | 正式发表 | IEEE OJCOMS 2024 (gold OA)
- 源文件路径: papers/doi/10.1109_ojcoms.2024.011100/content.md
- 核心贡献: 零阶/线性/二次多项式预测未来衰落信道增益，动态选 PBRL LDPC 码率（16 离散 8/9…8/77，全集 72，k=8192），LEO 相干时间 10ms + 反馈延迟 0-4ms 下最大化吞吐。
- 与本研究关系: **adjacent/boundary（coded-chain + info-uncertainty 维度高度重合，但 IM/DD+lognormal+无 HARQ）**
- **关键覆盖缺口**: 非 coherent（IM/DD+OOK）/ 非 GG（lognormal）/ 无 HARQ / 仅码率无调制阶数自适应。
- 详见 papers/_read_notes/Galijasevic_ojcoms_2024.md

### Family A — instantaneous-CSI 分支（coherent 近邻）

#### [L023] Adaptive Transceiver Design for High-capacity Multi-modal FSO...
- DOI/来源: 10.1109/JLT.2023.3242215 | 正式发表 | IEEE/OSA JLT 41(11):3397-3406, 2023 (Top-Scoreed)
- 源文件路径: papers/doi/10.1109_jlt.2023.3242215/content.md
- 核心贡献: 自适应多模 FSO 收发机，TX 按 per-mode SNR 做 bit/power loading（Chow 算法），RX 动态选 MIMO 检测器（MMSE/SIC/MLD/SIC-MLD），商用器件 590Gbit/s/λ。
- 与本研究关系: **adjacent（coherent AMC-FSO 同族，但地面 MDM 非 satellite，自陈卫星失效）**
- **关键覆盖缺口**: 非 GG（von Kármán 相位屏）/ 无真实编码链（FEC 仅阈值）/ 无 info uncertainty / 地面 MDM（非 satellite，论文自陈 receiver-directed adaptive loading 在 LEO 卫星不可行）。
- 详见 papers/_read_notes/L023_jlt_2023.md

### Family B — HARQ-IR/rate adaptation

#### [L096] On the Design of FSO-Based Satellite Systems Using IR-HARQ With Rate Adaptation
- DOI/来源: 10.1109/TVT.2021.3127193 | 正式发表 | IEEE TVT 71(1), 2022 (Q1)
- 源文件路径: papers/doi/10.1109_tvt.2021.3127193/content.md
- 核心贡献: LEO sat-ground FSO 的 IR-HARQ + 自适应速率跨层设计，RCPC + sliding-window ARQ，subcarrier M_n-QAM 多模式，FSMC + burst-loss 闭式推导 throughput/EE/avg-delay。
- 与本研究关系: **adjacent/boundary（coded-chain RCPC IR-HARQ 强相关，但 lognormal+IM/DD+perfect CSI）**
- **关键覆盖缺口**: 非 coherent（IM/DD subcarrier QAM）/ 非 GG（lognormal）/ **无 CSI/information 不确定性（假设反馈完美，imperfect feedback = future work）**。
- 详见 papers/_read_notes/L096_tvt_2022.md

---

## 二、边界条目（不计核心，仅供边界/参照）

| paper | 判定 | 理由（file:line 见 read-note） |
|---|---|---|
| L075 | **CLASSIFICATION**（dead-end#8） | CNN+BiLSTM+Attention softmax 分类器 on RX STFT spectrogram，5 类调制标签，confusion-matrix eval + true-label 监督；无 CSI 反馈环，"adaptive modulation"是 framing 非 runtime AMC [content.md:15,175,211,217,337] |
| L165 | **BOUNDARY_AO** | adaptive action = AO 波前校正（Shack-Hartmann + 97-actuator DM 1.5kHz），调制 PM-16/64-QAM 固定 per measurement 比较 not switch [content.md:11,82,86,99,180] |
| L090 | **BOUNDARY_FIXED_SCHEME** | 4-state STTC + coherent QPSK，"adaptive orthogonality controller"= 数学 ξ-parameterization（design-time config），无 CSI 反馈/无 runtime AMC [content.md:9,119,163,165,211] |

---

## 三、Bibliographic-only 条目（全文 BLOCKED，不得推导实现细节）

### [Safi2019] PROVISIONAL_DIRECT_COMPETITOR（abstract-only，IEEE paywall 无全文）
- DOI 10.1109/TVT.2019.2916843 | IEEE TVT 68(8):7566-7577, 2019 | Safi, Sharifi, Dabiri, Ansari, Cheng | cite 58
- abstract-inferred M/C/A（**未从全文验证**）:
  - M: 现有 FSO 自适应方案（固定/单一 coding-power）
  - C: **Gamma-Gamma 湍流 + channel-estimation error（observation-window-length 依赖）**
  - A: 估计误差随窗口长度变化，现有方案未联合 coding+power 适配 → BER/outage 退化
  - action（abstract-inferred）: joint/standalone adaptive coding-rate + TX power control，power-min 优化 under BER/outage/peak-power，closed-form throughput
- **无法从 abstract 确定**（须全文）: CSI 反馈机制/时延、编码族（LDPC/RS/conv）、是否同时适配调制阶数、baseline 集、所有数值、检测类型（IM/DD vs coherent）、优化方法、pointing 是否含。
- **约束**: 实现细节不可从 abstract 推导；Step 3 问题提取不得据 abstract 推 Safi 的具体方法空间。**很可能已覆盖"GG + estimation-error + adaptive coding/power"**（用户执行提示词明示），不得把此宽泛问题包装成空白。

### [L124] C_FAMILY_BIBLIOGRAPHIC（abstract-only，Optica bot-block 无全文）
- DOI 10.1364/oe.595557 | Optics Express 34(14):26128, 2026 (gold OA VOR) | "Physics-informed adaptive transmission for coherent FSO: multi-dimensional amplitude-phase statistics"
- abstract-level verified: coherent FSO + AMC（modulation selection）+ 多维 CSI 向量 {SNR, scintillation index, phase variance} + "physics-informed"（amplitude-phase 统计）。
- **无法从 abstract 确定**（须全文）: coding chain（FEC/rate adaptation?）、信道模型（GG? joint amplitude-phase?）、satellite vs terrestrial、反馈时延/CSI 反馈机制、baseline 集、确切 action 空间（仅 modulation? +coding? +power?）、所有数值。
- **约束（D003）**: C 族身份闭合**须全文**；无全文时 coherent-C 族 Q# **不得**过 novelty closure。本轮 Step 3 不得用 abstract/题目推导 L124 的 coding/CSI/channel/方法空间。

---

## 四、直接竞品矩阵（CORE 5 + Safi abstract）

> 目标场景: **星地 coherent FSO + Gamma-Gamma + coded chain + information uncertainty**。✓=覆盖该维度并与目标一致，✗=缺失/不一致，△=部分。

| paper | scenario | coherent | turbulence | coding/HARQ (in action) | CSI uncertainty | feedback delay | prediction | action | timescale | metric | deployability |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Nguyen2024** | LEO-sat→UAV(<1km) | ✗ IM/DD K-QAM (γ∝h²) | ✗ lognormal 弱 | ✗ 无（HARQ 仅 related work） | △ 仅反馈时延（排除估计误差） | ✓ 数 ms>相干<1ms | ✓ ESN 多步 | rate(K)+power(EDFA) | per-burst | power-min, EE | ✓ runtime TX |
| **L096** | LEO sat-ground | ✗ IM/DD subcarrier M-QAM | ✗ lognormal | ✓ RCPC IR-HARQ（码率{4/5,1/2,1/3}） | ✗ 完美反馈（imperfect=future work） | ✗（assumed perfect） | ✗ | rate(M-QAM)+IR-HARQ | per-slot | throughput, EE, delay | ✓ runtime TX |
| **L146** | sat-UAV-terrestrial (FSO/RF) | ✗ IM/DD 强度 QAM | ✗ lognormal | ✗（coding rate 仅 MCS 表） | ✓ Gaussian σ²=1/N | △ 论证可忽略（未给值） | ✗ | MCS+power+轨迹(DDPG) | per-slot | throughput, FER | ✓ runtime TX |
| **Galijasevic** | LEO sat FSO | ✗ IM/DD OOK | ✗ lognormal | ✓ PBRL LDPC（72 码率） | △ 仅反馈延迟（无估计误差） | ✓ 0-4ms, 相干10ms | ✓ 0/1/2次多项式 | LDPC code-rate | per-codeword | throughput (% zero-delay) | ✓ runtime TX |
| **L023** | 地面 MDM-FSO（自陈卫星失效） | ✓ coherent 外差 | ✗ von Kármán 相位屏 | ✗（FEC 仅阈值） | ✗（无建模） | △ 自陈 LEO 不可行 | ✗ | mod(2/4/8-QAM)+power+RX检测器 | per-frame | rate, OSNR, complexity | ✓ runtime（地面） |
| **Safi2019** (abstract) | FSO（场景未确认） | ?（未确认） | ✓ **Gamma-Gamma** | △ adaptive coding-rate（族未确认） | ✓ **channel-estimation error**（窗口长度依赖） | ? | ? | coding-rate + TX power | ? | power-min, BER, outage, closed-form | ?（abstract 推不出） |

**矩阵结论**:
1. **没有任何一篇同时覆盖 coherent + GG + coded chain + info uncertainty 四要素**。每篇都缺 2-3 个核心维度。
2. **最接近的组合**是 Safi（GG + estimation-error + coding/power，abstract 级），但全文缺失无法确认 coherent/coding 族/baseline；Galijasevic（coded-chain + prediction + feedback-delay）+ L146（info-uncertainty 模块）+ Nguyen（delayed-CSI + predictive rate+power）三者拼接近邻 family-A。
3. **coherent + GG 同时出现的论文**：仅 L023（coherent，但 von Kármán 非 GG，地面非卫星）和 L124（coherent，abstract 级，channel/coding 未知）。**无一篇 confirmed 同时 coherent + GG + runtime AMC**。
4. 这些宽泛问题（rate/power、HARQ-rate、coding-rate+prediction）**已被 Nguyen/L096/Galijasevic/Safi 覆盖**，**禁止重新命名为空白**（D003 + 用户执行提示词明示）。

---

## 五、综合分析

### 5.1 现有方法分类

按 action + condition 组合：
1. **rate+power AMC under delayed CSI**（family-A 核心）: Nguyen2024（SAMP + ESN，sat-UAV，lognormal，IM/DD）— 已覆盖"过期 CSI + ML 预测 + 联合 rate/power"。
2. **HARQ-IR + rate under perfect CSI**（family-B）: L096（RCPC IR-HARQ + M-QAM，sat-ground，lognormal，IM/DD，FSMC）。
3. **predictive coded-rate under feedback delay**（family-A coded 分支）: Galijasevic（PBRL LDPC + 多项式预测，LEO，lognormal，IM/DD，OCT/DVB-S2 对接）。
4. **robust MCS under estimation error**（family-A uncertain 分支）: L146（DDPG + Gaussian σ²=1/N，sat-UAV-terrestrial，lognormal，IM/DD，无 HARQ）。
5. **coherent MDM adaptive transceiver**（family-A instantaneous 分支）: L023（Chow loading + MIMO 检测器选择，地面，von Kármán，coherent）— 自陈卫星失效。
6. **（abstract 级）GG + estimation-error + adaptive coding/power**: Safi2019。

### 5.2 已知局限（领域级空白，新颖性原料，**非问题**）

- **所有 IM/DD AMC 工作（Nguyen/L096/Galijasevic/L146）都用 lognormal 弱湍流**，无一篇用 Gamma-Gamma。原因是 LEO 弱湍流（σ_R²<1）工程论证。中/强湍流（GG）下的 AMC 是否成立是 open。
- **所有 family-A IM/DD 工作的 info uncertainty 建模不完整**: Nguyen/Galijasevic 仅建模反馈时延（排除估计误差），L096 假设完美反馈，仅 L146 建模 Gaussian 估计误差但无反馈时延。
- **coherent + runtime AMC 真实存在的 confirmed 论文 = 0**: L023 coherent 但地面+自陈卫星失效；L124 coherent 但 abstract 级全文 BLOCKED。
- **HARQ/编码链与 coherent + GG 从未 confirmed 共存**: L096/Galijasevic 有 coded chain 但 IM/DD+lognormal；无 confirmed coherent+GG+coded-chain。
- **预测器与编码链从未联合 confirmed**: Nguyen 预测驱动 rate+power（无编码），Galijasevic 预测驱动 code-rate（无调制阶数+无 HARQ），L096 完美 CSI。

### 5.3 2-3 年趋势

- **反馈时延/CSI 不确定性显式化**: 2022 L096 还假设完美反馈（future work 提 imperfect），2024 Nguyen/Galijasevic 显式建模反馈时延+预测，2025 L146 显式建模 Gaussian 估计误差 → 趋势是从 perfect-CSI 向 uncertain-CSI 演进。
- **预测器从无 → 多项式 → ESN/LSTM**: 2022 无预测（L096），2024 Galijasevic 多项式、Nguyen ESN+对比 LSTM/GRU/SVM → ML 预测成标配。
- **coherent sat-ground AMC 仍是空白**: L023（2023）做 coherent AMC 但地面+自陈卫星失效；L124（2026）coherent AMC 但 abstract 级。coherent+sat+runtime AMC 无 confirmed 工作。
- **coded chain（LDPC/HARQ）与 IM/DD OOK 强绑定**: Galijasevic/L096 coded chain 都在 IM/DD+OOK/subcarrier-QAM；coherent 检测下的 coded-chain AMC 未 confirmed。

### 5.4 研究背景概述（支撑论文绪论 1.1）

**领域脉络**:
- 早期 FSO AMC（2010s）: Perlot/de Cola adaptive rate [9]、Spellmeyer multirate DPSK [10]、adaptive PPM [11]、Geisler AM+coding coherent LEO 实验 [12]、德国 adaptive rate by elevation [13]、[14] variable-rate hardware。基础是固定功率 + 单一维度 rate 适配。
- 中期（2019-2022）: Safi2019（GG + estimation-error + coding/power，abstract 级）、L096（IR-HARQ + rate + FSMC，perfect CSI）。
- 近期（2023-2025）: L023（coherent MDM AMC，地面）、Nguyen2024（ESN 预测 + rate/power SAMP）、Galijasevic（PBRL LDPC + 多项式预测）、L146（robust DDPG + estimation error）、L124（coherent physics-informed AMC，abstract 级）。

**核心技术挑战**:
1. LEO 卫星反馈时延（数 ms）> 相干时间（<1ms），CSI 过期是 AMC 失效主因（Nguyen/L096 future work）。
2. coherent 检测 vs IM/DD 的信息度量差异（γ∝h vs γ∝h²），coherent 下相位/振幅统计使 CSI 更高维（L124 physics-informed）。
3. Gamma-Gamma 中/强湍流下 AMC 是否仍有 headroom（所有 confirmed 工作都在弱 lognormal）。

**本研究定位**: 目标"星地 coherent FSO + GG + coded chain + info uncertainty"是 5 维度同时成立的切片。confirmed 文献中无一覆盖，但每个子维度都有近邻工作（rate+power / HARQ-rate / coded-rate+prediction / robust MCS / coherent MDM / GG+est-error）。研究问题必须建立在**现有近邻 M 在目标 C 下因具体 A 失效**，不是"没人做过 coherent+GG+AMC"（那是空白，FR-23）。

---

## 六、研究问题清单（[MUST]，逐条过 glossary 四判据）

> 问题定义见 `stages/glossary.md`（问题四判据 + 三概念对照表）。
> 每个 Q# 必须有具体 M（现有方法）+ C（具体条件）+ A（失效假设），最强直接竞品，机制差异，否决条件，证据缺口。
> **Step 3 终态二选一**: ≥1 个 Q# 四判据全过 = STEP3_PASS_WITH_VALID_Q；无 Q# 全过 = STEP3_NO_VALID_PROBLEM。

### 候选 Q# 评估

#### Q1: coherent 检测下，Nguyen 式 delayed-CSI + ESN-prediction 驱动的 rate+power SAMP，在 GG 中/强湍流 + sat-ground 几何下是否因 BER 度量（γ∝h² IM/DD → γ∝h coherent）+ 湍流强度（弱 lognormal → GG）+ 几何（sat-UAV → sat-ground）三者同时改变而失效？

- M: Nguyen2024 的 SAMP（IM/DD K-QAM, γ∝h², lognormal, sat-UAV）
- C: coherent 检测（γ∝h）+ Gamma-Gamma 中/强湍流 + sat-ground 固定站几何
- A: Nguyen 的瞬时 BER 公式 `0.2exp(-3Pt²h²/(2σn²(K-1)))` 依赖 γ∝h²（IM/DD SQNR-M²），coherent 下 γ∝h 使门限 h* 与功率分配 Pt(h) 关系完全改变；lognormal 弱湍流 σ_R²≤0.1020 的门限设计在 GG 中/强（σ_R²>1）下信道动态范围扩大，SAMP 的 N 离散功率级 + M 调制模式分配失效；sat-UAV(<1km) 的 Beckmann pointing 与 sat-ground（数百-数千 km）的 pointing 统计不同
- 最强直接竞品: **Nguyen2024**（family-A delayed-CSI/predictive rate+power 的 confirmed 直接竞品）
- 机制差异: coherent γ∝h vs Nguyen IM/DD γ∝h² → BER 度量重写；GG vs lognormal → 信道 PDF 与 FSMC/状态划分重做；sat-ground vs sat-UAV → pointing 模型替换
- 四判据:
  - problem_truth (M-C-A 完整可解): **⚠ 部分** — M、C 明确，但 A 的"失效"需证明 coherent+GG 下 Nguyen 的 SAMP 门限/分配**真的退化**（不是简单换参数重算）。目前 A 是"度量改变导致需重做"，不是"现有方法在 C 下性能退化"——**这是迁移工作而非失效证明**。
  - actionability: ✅（coherent+GG 下 SAMP 重设计 + ESN 预测，产出 algorithm + 设计准则）
  - novelty: ⚠ — Nguyen 已覆盖 delayed-CSI+预测+rate+power 的**机制**；coherent+GG 的差异是**场景迁移**，机制 novelty 弱（TL-04/TL-12/FR-23：换条件≠新问题）
  - thesis_fit: ✅（可量化对标 Nguyen 的 SAMP 在 coherent+GG 重做后的版本 vs Nguyen IM/DD lognormal 版本？**但对比对象不同场景，不是 head-to-head**）
- **否决条件**: 若 coherent+GG 下重做 SAMP 后只是参数变化（门限重算、PDF 替换），无新的失效机制 → FAIL（机制 novelty 不足，TL-12"延伸"路线需证明出 bug 概率低但不是新问题）。
- **证据缺口**: 需证明 coherent γ∝h + GG 下，Nguyen 的 SAMP **存在 Nguyen 未识别的失效模式**（如预测误差在 GG 深衰落下放大、离散功率级在 GG 动态范围下不够、BER 门限在 coherent 下与 IM/DD 行为质变），而非仅参数重算。**当前证据不足以区分"迁移"与"失效"**。
- **判定**: **未过**（problem_truth 部分 + novelty 受限）。不进 Contract。

#### Q2: L096 的 IR-HARQ + rate 跨层设计假设完美 CSI/反馈，在 GG + sat-ground + 反馈时延>相干时间下，是否因 imperfect feedback 导致 IR-HARQ 的 burst-loss Markov 模型（基于 perfect ACK/NAK）失效，且 RCPC 增量冗余在过期 CSI 下无法正确选码率？

- M: L096（IR-HARQ-SW + RCPC + M-QAM，perfect CSI 假设，lognormal）
- C: GG 中/强湍流 + sat-ground + 反馈时延>相干时间 + imperfect ACK/NAK + coherent 检测
- A: L096 的 burst-loss Markov 模型（eq.25-28，Viterbi 距离谱）假设 CRC 完美检错 + ACK/NAK 无误 + 含 CSI [content.md:103,119]；过期 CSI + imperfect ACK/NAK 下，状态转移矩阵 P 与稳态 π 失真，throughput/EE/delay 闭式不再成立；future work 明确点名 imperfect feedback [content.md:507]
- 最强直接竞品: **L096**（family-B coded-chain direct competitor）+ Galijasevic（coded-chain + 预测，但 IM/DD）
- 机制差异: L096 perfect-CSI 闭式 → 目标 imperfect-feedback 下 burst-loss Markov 重做（ACK/NAK error + delayed CSI 进转移矩阵）
- 四判据:
  - problem_truth: **⚠** — A 的"imperfect feedback 导致闭式失效"成立，但 L096 future work 已**明确预留**这个口子 [content.md:507]，即 L096 已识别此局限。**已被现有工作 self-identified 的局限 → 新颖性弱**（glossary：已知局限是新颖性原料不是问题，须转译 M-C-A；这里转译后 M=L096 自己，C=imperfect feedback，A=自己 future work → 是"补完 future work"而非"现有方法失效"）。
  - actionability: ✅（imperfect-feedback burst-loss Markov 重做 + 闭式）
  - novelty: **❌** — L096 future work 已点名；Galijasevic 已在 coded-chain + feedback-delay 做了预测驱动（虽 IM/DD）。补 L096 的 future work + 换 GG+coherent = 组合迁移，机制 novelty 不足。
  - thesis_fit: ⚠
- **否决条件**: A 是 L096 self-identified future work → 自动 FAIL novelty（glossary 常见误用#1：把已知局限当问题）。
- **判定**: **未过**（novelty ❌，A 是 self-identified future work）。

#### Q3（cross-gap 候选，**待证假设**）: 现有预测驱动 rate/power 或 code-rate 控制（Nguyen/Galijasevic），在 coherent + GG + 真实 coded-chain + 接收机可见且不确定的 CSI + 反馈时延**共同存在**时，是否因**信息源 / 时间尺度 / 目标函数错配**而失效？

- M: Nguyen2024（rate+power SAMP + ESN，单维度 action）+ Galijasevic（code-rate + 多项式预测，单维度 action）
- C: coherent（γ∝h）+ GG 中/强 + 真实 coded-chain（LDPC/HARQ）+ CSI 不确定（估计误差+反馈时延+量化）+ sat-ground
- A: （**待证**）现有预测器只驱动单一 action（Nguyen 驱动 rate+power 无编码，Galijasevic 驱动 code-rate 无调制阶数无 HARQ），在 coded-chain + coherent + GG 共存时，预测的 CSI 量（IM/DD lognormal 信道增益 h）与 coherent 所需的 CSI 量（复振幅+相位统计，L124 physics-informed）不同 → 信息源错配；编码链的码字时间尺度（µs）与信道相干时间（<1ms）与反馈时延（ms）三层时间尺度嵌套，单一预测器无法同时服务 → 时间尺度错配；目标函数（Nguyen power-min / Galijasevic throughput）未含 coded-chain 的 FER/重传代价 → 目标函数错配。
- 最强直接竞品: **Nguyen2024 + Galijasevic**（二者机制拼接的近邻）+ Safi2019（abstract 级 GG+est-error+coding/power）+ L096（coded-chain perfect CSI）
- 机制差异: 三层错配（信息源/时间尺度/目标函数）需新的联合预测-控制架构
- 四判据:
  - problem_truth: **❌（当前）** — A 的"三层错配导致失效"是**假设**，无 confirmed 因果失效机制。brief 明示"若只是把 Nguyen、Galijasevic、Safi、L096 的要素机械拼接，必须 FAIL；只有存在具体因果失效机制和可区分 action 才能形成 Q#"。当前 A 是机制拼接的推测，**未证**。
  - actionability: ⚠（联合架构可设计，但需先证失效）
  - novelty: ⚠（每子维度有近邻，联合 novelty 依赖失效证明）
  - thesis_fit: ⚠
- **否决条件**: brief 明示 — 若只是机械拼接要素（信息源/时间尺度/目标函数的"错配"是叙述而非 proven 因果），必须 FAIL。需先证 coherent+GG+coded-chain 共存下，Nguyen/Galijasevic 的预测-控制**确实存在具体可观测的失效**（如预测 MSE 在 GG 深衰落爆炸、code-rate 选择在 coherent 度量下系统性偏移）。
- **证据缺口**: 需 oracle/MVE 级证据证明三层错配**确实导致失效**——但这是 Step 4a/MVE 的事，**Step 3 无权做**（FR-22）。当前仅文献精读，无法证明失效。
- **判定**: **未过**（problem_truth ❌ — A 是待证假设非 confirmed 失效；按 brief 机械拼接 FAIL）。

#### Q4（Safi 邻近切片，**abstract-blocked**）: Safi2019 的 adaptive coding+power under GG + estimation-error，在 coherent 检测 + sat-ground + 反馈时延 + 真实 coded-chain 下是否失效？

- **判定**: **未过（abstract-blocked）** — Safi 全文缺失，A 无法从 abstract 确认。按 brief + D003，Safi 邻近切片**不得**通过 novelty closure；只能用 abstract 级 M/C/A 作 bibliographic 参照。**禁据 abstract 推导 Safi 的失效机制**。

#### Q5（coherent-C 族，**C-family blocked**）: L124 的 physics-informed coherent AMC，在 GG + coded-chain + sat-ground 下是否失效？

- **判定**: **未过（C-family blocked）** — L124 全文缺失（C_L124_FULLTEXT_BLOCKED），coherent-C 族**不得**通过问题/新颖性判断（D003 第 4/5 点）。本轮只能用 abstract 级 bibliographic 信息，**禁推导** L124 的 coding/CSI/channel/方法空间。

### Q# 清单汇总

| Q# | M | C | A | problem_truth | actionability | novelty | thesis_fit | 最强竞品 | 判定 |
|---|---|---|---|---|---|---|---|---|---|
| Q1 | Nguyen SAMP | coherent+GG+sat-ground | 度量/湍流/几何改变 | ⚠部分 | ✅ | ⚠迁移 | ✅但非head-to-head | Nguyen2024 | **未过**（迁移非失效） |
| Q2 | L096 IR-HARQ | GG+sat-ground+imperfect feedback | perfect-CSI 闭式失效 | ⚠ | ✅ | ❌self-id future work | ⚠ | L096 | **未过**（A=self-identified） |
| Q3 | Nguyen+Galijasevic 拼接 | coherent+GG+coded+uncertain+delay | 三层错配（待证） | ❌（待证假设） | ⚠ | ⚠ | ⚠ | Nguyen+Galijasevic | **未过**（机械拼接 FAIL） |
| Q4 | Safi2019 | coherent+sat-ground+coded+delay | ?（abstract 推不出） | ❌abstract-blocked | — | — | — | Safi | **未过**（abstract-blocked） |
| Q5 | L124 | GG+coded+sat-ground | ?（abstract 推不出） | ❌C-family-blocked | — | — | — | L124 | **未过**（C-blocked） |

**无 Q# 四判据全过。**

---

## 七、Step 3 终态判定

### STEP3_NO_VALID_PROBLEM（当前轮诚实终态）

**依据**:
1. 5 篇 CORE 全文精读 + 3 边界 + 2 bibliographic 完成结构化提取（每篇 read-note 含 M-C-A + 四判据 + file:line 证据）。
2. 直接竞品矩阵确认：**无一篇 confirmed 同时覆盖 coherent + GG + coded-chain + info-uncertainty 四要素**；每篇缺 2-3 维度；rate/power（Nguyen）、HARQ-rate（L096）、coded-rate+prediction（Galijasevic）、robust-MCS（L146）等宽泛问题**已被覆盖**，禁止重命名为空白。
3. 5 个候选 Q# 逐条过四判据，**无一全过**：
   - Q1/Q2 是场景迁移（coherent+GG 替换 IM/DD+lognormal）或补 self-identified future work，机制 novelty 不足（TL-04/TL-12/FR-23）；
   - Q3 是机械拼接要素的待证假设，brief 明示 FAIL；
   - Q4/Q5 全文 BLOCKED，不得据 abstract 推导失效（D003）。
4. 按 glossary"候选全被筛掉时"处置流程 + 用户执行提示词"若无 Q# 全过，终态为 STEP3_NO_VALID_PROBLEM，不包装空白、不设计方法"——**诚实终止问题提取**。

**这不是"领域无问题"的结论**，而是"本轮精读范围（5 CORE + 边界 + abstract）内无四判据全过的 Q#"。两个关键全文缺失（Safi/L124）可能改变判断；且 coherent+GG+coded-chain 的联合失效机制需 Step 4a/MVE 级证据（FR-22 禁 Step 3 做）。

### 处置（按 glossary"候选全被筛掉时"）

1. **先回 gw-search 扩关键词重检索（Step 3.5）**: 当前精读库可能偏窄。需补检索: (a) coherent FSO + Gamma-Gamma + adaptive modulation/coding 的直接竞品（确认 L124 之外是否有）；(b) coherent 检测下 CSI 反馈/预测的 AMC 工作；(c) Gamma-Gamma 中/强湍流下 AMC headroom 的分析论文；(d) **L124 + Safi 全文获取**（用户手动，关键身份闭合）。
2. **扩检索后仍空 → 上报用户决策**: 可能 C 条件（coherent + GG + coded-chain + sat-ground + info-uncertainty 五要素同时锁死）本身太窄，换任何模块都撞同一物理事实（LEO 反馈时延>相干时间 + coherent CSI 更高维 + GG 动态范围大）。需用户/导师决定是否调整 C 条件或换子方向。**禁止 agent 自己拍板放宽 C 条件**（跨阶段决策）。

### 下一步合法动作（FR-22）

- **不进 Step 3.5（supplement）**: glossary 流程是"候选全空 → 回 Step 3.5 扩检索"，但本轮 Step 3 已在 topic 范围内诚实终止。Step 3.5 是**下一轮**的合法动作（需新对话 + 用户授权扩检索范围 + 优先获取 Safi/L124 全文）。
- **禁进 Step 4a/MVE/方法设计/仿真**: 无 Q# 全过，FR-22 硬门控禁止。
- **本轮到此停止**（用户执行提示词"到 Step 3 终态停止"）。

---

## 八、写作架构参考（选做，2 篇标杆）

> 选文标准: 与方向最接近 + 发表在目标顶刊。选 Nguyen2024（TAES，family-A 直接竞品）+ L096（TVT，family-B coded-chain 直接竞品）。

### Nguyen2024 (TAES)
- 章节结构: I Intro（Related works + Motivation + Contributions C1-C3 + Table I literature comparison）/ II System & Channel Model（attenuation+turbulence lognormal + pointing Beckmann + composite）/ III Proposed Adaptive Rate with Power Control（AMP ideal + SAMP discrete + Alg.1-4 + avg-power/EE 闭式）/ IV Numerical Results / V Conclusion。
- 独立 System Model + Problem Formulation（§III）+ Algorithm Design（Alg.1-4）章节。
- 参数展示: Table II 集中展示；符号行内定义。
- 图表: Table I literature comparison（关键，对标定位）、系统模型图、BER/EE vs 参数曲线、ESN vs ML 预测对比。
- Intro 论证: 背景（LEO+FSO）→ 问题（outdated CSI）→ 空白（adaptive rate/power with ML prediction not available）→ 贡献 C1-C3。
- 贡献列表: 3 条（SAMP 方案 / multistep ESN + ML 对比 / 数值结果验证）。
- 公式: 连续编号；BER/优化目标/闭式完整推导；ESN 状态更新 + ridge 训练显式。
- 参考密度: Intro 高（AMC 文献综述），Method/Experiment 中。

### L096 (TVT)
- 章节结构: I Intro / II System & Channel（lognormal + pointing + FSMC）/ III IR-HARQ + Rate Adaptation Design（RCPC + sliding window + burst-loss Markov）/ IV Performance Analysis（throughput/EE/delay 闭式）/ V Numerical / VI Conclusion。
- 独立 System Model + Performance Analysis 章节。
- 图表: FSMC 转移图、burst-loss Markov 图、throughput/EE/delay vs 参数曲线。
- 公式: 连续编号；FSMC 转移 + burst-loss 联合解码失败上界（Viterbi 距离谱）完整推导。
- Intro 论证: 背景 → IR-HARQ 在 LEO 长 RTT 的问题 → SW vs sliding-window → 贡献。

**可仿写模式**: Table I/II literature comparison + 独立 System Model + Algorithm（编号 Alg.）+ 闭式 Performance Analysis + Numerical。Intro 的"背景→问题→空白→贡献 C1-CN"四段式。

### 共同引用基础文献（未覆盖，喂 Step 3.5）
- Nguyen[9] Perlot/de Cola adaptive rate LEO、[12] Geisler AM+coding coherent LEO 实验、[16] terrestrial joint rate+power、[22] LEO 相干时间<1ms 测量。
- L096[12,13] IR-HARQ-SW、[15] pure sliding-window ARQ。
- Galijasevic[8] Nguyen 2020 Asilomar Raptor/punctured LDPC、[20] PBRL。
- → Step 3.5 补检索这些基础文献的近期延伸 + coherent+GG+AMC 直接竞品。

---

## 九、实验完备性对标汇总（3-5 篇核心竞品）

| 维度 | Nguyen2024 | L096 | Galijasevic | L146 | L023 |
|---|---|---|---|---|---|
| 声称清单 scope | bounded（specific zenith/rate/jitter） | bounded（H/zenith/Cn2） | bounded（td/PSI） | bounded（N/pilot） | bounded（r0） |
| 统计规范性 | MC 837500 样本，无 error bar | MC 10^6 slots，无 error bar | 理论积分+少量 MC | DDPG 收敛曲线，无 error bar | 12 湍流实现，无统计检验 |
| Baseline 矩阵 | 3 AMC + 4 ML 预测器 | 3 ARQ 方案 + 多 mother code | 2（zero-delay + 固定码率） | 5（NCU/nonadaptive/PPO/DQN/random） | 4 检测器 + 有无 loading |
| 消融设计 | 预测器对比（ESN vs ML） | mother code 对比 | 预测阶数 0/1/2 | robust vs NCU（CSI 不确定性消融） | 检测器组合消融 |
| 信道模型 + 参数来源 | lognormal（[29]实测）+ Beckmann | lognormal + Farid-Hranilovic | lognormal FIR + APD 实测[21] | lognormal[27] + Nakagami | von Kármán 相位屏 |
| 拓扑多样性 | sat-UAV 单链路 | sat-ground 单链路（多 H/zenith） | LEO 单链路（多 td） | sat-UAV-terrestrial 双跳 | 地面点对点 MDM |
| 复杂度报告 | ESN 训练时间 vs LSTM/GRU | 无 FLOPs | polyfit + 查表（低） | DDPG O(M·params) | SIC-MLD vs MLD 一个数量级 |
| VVUQ（V/V/U）| V2 V2 U2（MC 验证闭式） | V2 V2 U2 | V2 V1 U1 | V1 V2 U2 | V2 V2 U1 |

**领域惯例与盲点**:
- 惯例: MC 仿真验证闭式（Nguyen/L096）；Table I literature comparison（Nguyen）；多 zenith/H 扫描（L096/L146）。
- 盲点: **无一篇做统计检验/error bar**（领域通病）；复杂度报告参差（仅 Nguyen/Galijasevic/L023 给相对复杂度）；coherent+GG 场景无 confirmed 实验对标。

**Contract 阶段对标基准（平均值）**: 统计规范性 1/3（无 error bar）、Baseline 数 ~3-5、消融设计 1-2 维、信道模型多源但全 lognormal/von Kármán（无 GG confirmed）。

---

## 十、诚实边界声明

1. 本 Step 3 基于 5 CORE 全文 + 3 边界 + 2 abstract-only。**Safi2019（abstract-only）+ L124（abstract-only）全文缺失**，二者的 M-C-A 是 abstract-inferred，**不可据 abstract 推导失效机制**（FR-26）。
2. **coherent + GG + coded-chain + info-uncertainty 五要素同时 confirmed 的工作 = 0**。这是文献事实，但"五要素同时锁死"的 C 条件可能物理上太窄（需 Step 3.5/4a 验证或用户决策放宽）。
3. STEP3_NO_VALID_PROBLEM 是**本轮精读范围**的结论，不是"领域无问题"的终极判断。获取 Safi/L124 全文 + Step 3.5 扩检索后可能改变。
4. 本轮**未进 Step 3.5/4a/MVE/方法设计/仿真**（FR-22 硬门控；无 Q# 全过禁进 Step 4a）。
