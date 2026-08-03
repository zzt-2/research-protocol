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
| 3 read | ✅/**STEP3_READ_COMPLETE_SEMANTIC_GATE_MISAPPLIED（D005 纠偏；旧 STEP3_NO_VALID_PROBLEM 已取代）**| 2026-08-03 | 本轮统一 commit | 本文件 + 5 read-notes + 直接竞品矩阵 + Q# 表（canonical 四判据重建：Q-A/Q-B SURVIVES 待 3.5 闭包）|
| 3.5 supplement | ✅（**STEP3_5_SURVIVES，S005/R003**；Q-A/Q-B 均 SURVIVES）| 2026-08-03 | 本轮统一 commit | R003 定向检索（Q-A/Q-B 各 6 query + 引用链 ~190 命中）+ 竞争闭包表（§十一）；Safi/L124 仍 BLOCKED |
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
> **判据标签 = canonical 四判据**（D005 纠偏）：判据1 具体技术矛盾(M-C-A 明确可证伪) | 判据2 方法产出形态 | 判据3 近期 baseline | 判据4 可量化对标。
> **旧自创标签（problem_truth/actionability/novelty/thesis_fit）已废止**（D005/R001）——`problem_truth` 把"已证伪"当 Step 3 判据=Step 4a/MVE 证据前移；`novelty` 不属四判据=Step 3.5/4a 职责前移。Step 3 只要求**文献支持、具体、可证伪**的失效假设 A，**不要求已用 MVE 证明退化**。

### 候选 Q# 评估（按 canonical 四判据，D005 重建）

#### Q-A（新建，预测驱动自适应编码的风险失配）

- M: **Galijasevic 2024** 的预测驱动 PBRL-LDPC 码率自适应（点预测信道状态 → 逐码字选码率；零阶/线性/二次多项式点预测，IM/DD lognormal，反馈延迟 0-4ms）[papers/_read_notes/Galijasevic_ojcoms_2024.md；content.md:19,55,66,114,288]
- C: 星地 FSO 中**反馈延迟与 CSI 估计误差同时存在 + 湍流具有深衰落尾部 + 真实 coded-chain 的 FER/码率门限高度非线性**（Nguyen2024 [content.md:81脚注2] 显式排除估计/量化误差仅建模反馈时延；Galijasevic 仅 error-free 反馈信道）
- A: **单一点预测值没有表达预测后验不确定性**。即使均值预测准确，尾部误差也可能经非线性 FER 门限放大，使"预测值→码率"产生系统性可靠性违约或 goodput 损失。失效位置可证伪：Galijasevic 的码率选择是预测增益的单值函数（查表），FER 门限对增益非线性——存在一个可构造的预测误差分布（重尾）使点预测选码系统性偏高 → FER 约束违约。
- 方法产出形态（判据2）: posterior-aware / risk-aware / outage-constrained code-rate rule（设计准则 + 算法 + 可引用的 outage/FER 闭式族）
- 近期 baseline（判据3）: Galijasevic 2024（OJCOMS，直接竞品）；须同时比较 Safi 2019 / Nguyen 2024 / L096
- 可量化对标（判据4）: FER 约束违约率、goodput、平均码率、功率、预测误差条件下的可靠性（产出 vs Galijasevic 点预测规则 head-to-head，同信道同 coded chain）
- 最强反驳（待 Step 3.5 闭包）: Safi 可能已覆盖 GG + estimation-error + adaptive coding/power；robust link adaptation / posterior-aware rate adaptation 文献可能已有 risk-aware action。
- 四判据初判（Step 3 层，不含 Step 3.5/4a 证据）:
  - 判据1 具体技术矛盾: **✅** — M(Galijasevic 点预测选码) / C(延迟+估计误差+深衰尾+非线性 FER) / A(点预测无后验，尾部误差经非线性门限放大致系统性违约) 三要素明确、句子级、可证伪。**不要求已用 MVE 证明退化**（FR-22；D005）。
  - 判据2 方法产出形态: **✅** — risk/posterior-aware code-rate rule 是可复用设计准则。
  - 判据3 近期 baseline: **✅** — Galijasevic 2024 是近期直接竞品（待 Step 3.5 确认是否有更近/risk-aware 直接竞品）。
  - 判据4 可量化对标: **✅** — FER 违约率/goodput/条件可靠性可对 Galijasevic head-to-head。
- **否决条件（留 Step 3.5/4a）**: 若 Step 3.5 发现 Safi 或 robust/posterior-aware link adaptation 文献**已实质解决**"预测不确定性下的码率选择"→ COVERED_BY_EXISTING_WORK；若 Step 4a 维度 D MVE 证明 coherent+GG+真实估计误差下点预测与 risk-aware 的 FER/goodput gap < 阈值 → 由 Step 4a Kill。
- **判定**: **Step 3 层 SURVIVES（待 Step 3.5 竞争闭包）**。不得因"尚无 MVE"否决（D005；brief 明示）。

#### Q-B（新建，相干星地 AMC 的动作位置-时间尺度失配）

- M: **L023** 将 TX modulation/power loading 与 RX detector switching 放在**同一个 per-frame CSI 反馈环**（coherent 外差，地面 MDM，自陈 receiver-directed adaptive loading 在 LEO 卫星不可行因往返 > Greenwood τ≈4ms）[papers/_read_notes/L023_jlt_2023.md；content.md:122,147,155,171,313]
- C: **LEO 星地链路 RTT 大于或接近信道相干时间；接收端可本地快速动作，发射端只能慢速获得反馈；同时存在 coded chain**
- A: **将 RX-local 快动作与 TX-side 慢动作绑定在同一个新鲜 CSI 控制环中**，会造成不可部署的信息契约：接收端动作可及时执行，发射端动作收到的状态已经过期。失效位置可证伪：L023 自陈 LEO 不可行（receiver-directed loading 往返 > Greenwood τ），即 L023 的 M 在 LEO 星地 C 下**已自认失效**。
- 方法产出形态（判据2）: RX-local fast adaptation + TX-side slow robust rate/power control 的**分层控制和接口**（设计准则 + 接口契约 + 可引用的时延-吞吐/outage 闭式族）
- 近期 baseline（判据3）: L023 / Nguyen / Galijasevic；L124 若取得全文必须作 coherent 直接竞品
- 可量化对标（判据4）: goodput、FER/outage、反馈开销、动作陈旧度、复杂度（产出 vs L023 单环方案 head-to-head，同 LEO 星地几何）
- 最强反驳（待 Step 3.5 闭包）: split-timescale / receiver-driven / hierarchical link adaptation 文献可能已解决；L023 可能因地面 MDM 场景而不是合法星地 baseline。
- 四判据初判（Step 3 层）:
  - 判据1 具体技术矛盾: **✅** — M(L023 单环 TX+RX) / C(LEO RTT≈/>相干时间，RX 快 TX 慢) / A(同环绑定致 TX 动作收过期状态) 明确可证伪（L023 自陈 LEO 不可行即为 A 的文献支持）。
  - 判据2 方法产出形态: **✅** — 分层控制接口是可复用设计准则。
  - 判据3 近期 baseline: **⚠→待 Step 3.5** — L023 是 coherent AMC 近期竞品，但场景是地面 MDM（自陈卫星失效）；须 Step 3.5 确认是否有合法星地 coherent split-timescale baseline。
  - 判据4 可量化对标: **✅** — goodput/outage/反馈开销/动作陈旧度可对 L023 head-to-head。
- **否决条件（留 Step 3.5/4a）**: 若 Step 3.5 发现 L023 因地面场景不是合法星地 baseline 且无其他 coherent 星地 AMC baseline → 判据3 失败；若 split-timescale/receiver-driven link adaptation 已实质解决 → COVERED_BY_EXISTING_WORK。
- **判定**: **Step 3 层 SURVIVES（待 Step 3.5 竞争闭包）**。不得因"尚无 MVE"否决。

#### Q1（原，IM/DD→coherent、lognormal→GG、UAV→ground 场景迁移）— 维持 WEAK_SCENARIO_MIGRATION 不晋级

- M: Nguyen2024 SAMP（IM/DD K-QAM, γ∝h², lognormal, sat-UAV）
- C/A: coherent(γ∝h) + GG + sat-ground 三者同时替换
- canonical 判据重判:
  - 判据1: **❌** — A 是"度量/湍流/几何改变导致需重做"，不是"现有方法在 C 下因 A 失效"。换参数重算 ≠ 失效假设（glossary 常见误用#3 "把没人做过 X 当问题"；FR-23）。这是**场景迁移工作**不是 M-C-A 失效矛盾。
  - 判据2/3/4: 形式上 ✅，但因判据1 不成立不晋级。
- **判定**: **WEAK_SCENARIO_MIGRATION，不自动晋级**（brief 明示）。

#### Q3（原，三层错配）— 维持 TOO_BROAD_MECHANICAL_COMBINATION 除非收窄

- M: Nguyen + Galijasevic 拼接；A: 信息源/时间尺度/目标函数三层错配（待证）
- canonical 判据重判:
  - 判据1: **❌（当前）** — A 是三机制拼接的叙述，**不是单一可证伪的失效假设**。需收窄成单一 baseline + 单一 load-bearing assumption + 单一可观察失效才能过判据1。
  - **可收窄路径**：Q-A 已收窄"预测后验缺失"单一切片（信息源错配的子集）；Q-B 已收窄"动作时间尺度失配"单一切片。Q3 作为宽集合不单独晋级。
- **判定**: **TOO_BROAD_MECHANICAL_COMBINATION，除非收窄**（brief 明示）。其可收窄子集已由 Q-A/Q-B 承接。

#### Q2（原，L096 self-id future work）— novelty 论据不再作 Step 3 terminal，但仍不晋级

- M: L096 IR-HARQ（perfect CSI 假设）；A: imperfect feedback 致 burst-loss Markov 闭式失效（L096 future work 自点 [content.md:507]）
- canonical 判据重判:
  - 判据1: **⚠→❌** — A 的"imperfect feedback 致闭式失效"是文献支持的可证伪假设（判据1 形式上可过），但**论文自列 future work ≠ novelty 自动失败**（D005/brief）——它只能作问题原料，仍须 Step 3.5 竞争闭包判断是否已被 Galijasevic 等实质解决。当前作为独立 Q# 不晋级，因其 coded-chain+imperfect-feedback 切片与 Q-A(Q-竞争闭包后)/Galijasevic 高度重叠，避免重复。
- **判定**: **不单独晋级**（切片被 Q-A 竞争闭包过程覆盖；future-work 原料性保留，Step 3.5 一并查）。

#### Q4（Safi 邻近切片）— 继续 BLOCKED

- **判定**: **BLOCKED_BY_MISSING_FULLTEXT** — Safi 全文缺失，A 无法从 abstract 确认（D003/D005）。abstract 级 M/C/A 仅作 bibliographic 参照，**禁据 abstract 推导失效机制**。Step 3.5 继续尝试合法获取。

#### Q5（L124 coherent-C 族）— 继续 BLOCKED

- **判定**: **BLOCKED_BY_MISSING_FULLTEXT** — L124 全文缺失（C_L124_FULLTEXT_BLOCKED），coherent-C 族**不得**通过问题/新颖性判断（D003）。Step 3.5 继续尝试合法获取；L124 全文到手后必须作 Q-A/Q-B 的 coherent 直接竞品重判。

### Q# 清单汇总（canonical 四判据，D005 重建）

| Q# | M | C | A | 判据1 矛盾 | 判据2 产出形态 | 判据3 近期baseline | 判据4 可量化对标 | Step 3 verdict | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| **Q-A** | Galijasevic 点预测选码 | 延迟+估计误差+深衰尾+非线性FER | 点预测无后验，尾部误差经非线性门限放大致系统性违约 | ✅ | ✅ risk/posterior-aware rule | ✅ Galijasevic（待3.5闭包） | ✅ FER违约率/goodput | **SURVIVES_STEP3（待3.5闭包）** | 不得因无MVE否决 |
| **Q-B** | L023 单环 TX+RX CSI 反馈 | LEO RTT≈/>相干时间，RX快TX慢 | 同环绑定致TX动作收过期状态 | ✅ | ✅ 分层控制接口 | ⚠ L023地面自陈卫星失效（待3.5） | ✅ goodput/outage/反馈开销 | **SURVIVES_STEP3（待3.5闭包）** | 不得因无MVE否决 |
| Q1 | Nguyen SAMP | coherent+GG+sat-ground | 度量/湍流/几何改变 | ❌（迁移非失效） | ✅ | ✅ | ✅ | **WEAK_SCENARIO_MIGRATION** | 不晋级 |
| Q3 | Nguyen+Galijasevic 拼接 | coherent+GG+coded+uncertain | 三层错配（待证） | ❌（宽集合非单一可证伪） | ⚠ | ⚠ | ⚠ | **TOO_BROAD_MECHANICAL_COMBINATION** | 子集已由Q-A/Q-B承接 |
| Q2 | L096 IR-HARQ | imperfect feedback | perfect-CSI闭式失效 | ⚠（future-work原料） | ✅ | ✅ | ✅ | **不单独晋级** | 切片被Q-A闭包覆盖 |
| Q4 | Safi2019 | coherent+sat-ground+coded | ?（abstract推不出） | — | — | — | — | **BLOCKED_BY_MISSING_FULLTEXT** | 3.5继续获取 |
| Q5 | L124 | GG+coded+sat-ground | ?（abstract推不出） | — | — | — | — | **BLOCKED_BY_MISSING_FULLTEXT** | 3.5继续获取 |

**Q-A / Q-B 在 Step 3 层 SURVIVES（待 Step 3.5 竞争闭包）。Step 3 不再是无 Q#——按 canonical 四判据存在 2 个候选问题。**

---

## 七、Step 3 终态判定

### STEP3_READ_COMPLETE_SEMANTIC_GATE_MISAPPLIED（D005 纠偏后终态）

**纠偏依据（D005/R001）**: 旧终态 STEP3_NO_VALID_PROBLEM（S004/V005）使用了**自创四判据标签** `problem_truth/actionability/novelty/thesis_fit` 作为 terminal gate，其中 `problem_truth` 被要求"A 的失效已证明"（=Step 4a/MVE 证据前移，违反 FR-22）、`novelty` 被当 Step 3 terminal 一列（=Step 3.5/4a 职责前移）。protocol 唯一合法四判据 owner = `stages/glossary.md` L22-31 + `templates.md` L301/L308/L311/L371（SHA256 + 行号见 R001）。按 canonical 四判据重判后，Step 3 终态修订为 **STEP3_READ_COMPLETE_SEMANTIC_GATE_MISAPPLIED**。

**保留（D004 继续有效）**: Step 2 PASS / 5 CORE 身份 / Safi·L124 全文 blocker / 全文精读事实提取 / 直接竞品矩阵 / 边界判定（L075 classification / L165 AO / L090 fixed-STTC）。

**Step 3 重建结论（canonical 四判据）**:
1. 5 篇 CORE 全文精读 + 3 边界 + 2 bibliographic 事实提取完整保留。
2. 直接竞品矩阵确认：**无一篇 confirmed 同时覆盖 coherent + GG + coded-chain + info-uncertainty 四要素**（事实保留）。
3. 按 canonical 四判据重建 Q#：**Q-A（预测驱动风险失配）+ Q-B（动作位置-时间尺度失配）在 Step 3 层 SURVIVES（待 Step 3.5 竞争闭包）**；Q1 场景迁移 / Q3 宽集合 / Q2 切片重叠 不单独晋级；Q4 Safi / Q5 L124 全文 BLOCKED。
4. **Step 3 不再是"无 Q#"**——存在 2 个 canonical 四判据形式上过的候选问题，但它们能否进 Step 4a 取决于 **Step 3.5 竞争闭包**（是否存在直接竞品已实质解决）。

### 处置（glossary"候选全被筛掉时"出口① → Step 3.5）

Step 3 终态触发 **Step 3.5 定向补充检索**（不是终点）。Q-A/Q-B 各需：≥2 组不同表述专属 query + forward/backward citation + 直接竞品/近邻竞品/反例三类筛选 + 优先近五年正式发表。详见 R003（Step 3.5 检索记录）+ 竞争闭包表（§十一）。

### 下一步合法动作（FR-22）

- **本轮执行 Step 3.5**（glossary 流程①；brief 授权）。终态只能为：SURVIVES_STEP3_5 / COVERED_BY_EXISTING_WORK / WEAK_SCENARIO_MIGRATION / BLOCKED_BY_MISSING_FULLTEXT / TOO_BROAD_OR_MECHANISM_UNPROVEN。
- **只有 ≥1 个 Q 为 SURVIVES_STEP3_5，下一合法动作才是 Step 4a**。**本轮不启动 Step 4a/MVE/方法设计/仿真**（brief 明示）。
- **若 Q-A/Q-B 都失败**: 不制造第三个弱 Q；终态 STEP3_5_NO_SURVIVING_PROBLEM；交用户决定调整 C / 换 AMC 子族 / 停止。

### Step 3.5 终态（R003 闭包后）

**STEP3_5_SURVIVES**：Q-A（带 Safi UNVERIFIED 尾巴）+ Q-B（带 scenario-migration + baseline 缺位风险）**均 SURVIVES_STEP3_5** → **存在 Step 4a 入口**。竞争闭包详见 §十一 + R003。**本轮到此停止，不启动 Step 4a**（brief 明示）。下一合法动作 = Step 4a（需新对话 + 用户授权），启动前应优先关闭 Q-A Safi 尾巴 + 评估 Q-B 自建信道模型可行性。

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
3. **Step 3 终态 STEP3_READ_COMPLETE_SEMANTIC_GATE_MISAPPLIED（D005）**：旧 STEP3_NO_VALID_PROBLEM 因用自创四判据标签（problem_truth 等）被取代；按 canonical 四判据 Q-A/Q-B 在 Step 3 层 SURVIVES（待 3.5 竞争闭包）。这不是"领域无问题"，也不是"Q-A/Q-B 已成立"——能否进 Step 4a 取决于 Step 3.5 竞争闭包结果。
4. **本轮未进 Step 4a/MVE/方法设计/仿真**（FR-22 硬门控；brief 明示到 Step 3.5 终态停止）。Step 3.5 是本轮执行的合法动作（glossary 空集处置流程①）。
5. **Q-A/Q-B 的 A 是文献支持、可证伪的失效假设，不是已证伪**——"已证伪"是 Step 4a/MVE 的事，Step 3 不要求（D005/R001；FR-22）。

---

## 十一、Step 3.5 竞争闭包表（D005/R003，Contract 引用源）

> 2 个并行子 agent 执行（Q-A/Q-B 各 6 专属 query + 引用链 + Safi/L124 获取），全部检索 JSON 在 `search-archive/2026-08-03/`（55 文件）。详见 `.sessions/2026-08-02-fso-amc-groundwork/R003-step35-targeted-search-and-closure.md`。

### 11.1 Q-A 闭包（预测驱动自适应编码的风险失配）

| paper | DOI/year | 同 M | 同 C | 解决 A | verdict |
|---|---|---|---|---|---|
| Nguyen2024 (TAES) | 10.1109/TAES.2024.3403809 / 2024 | 是 | 是 | **否**（点预测，outdated CSI 当动机非纳入码率规则） | PARTIAL_OVERLAP（最强近邻，A 留缝）|
| Galijasevic ICC 2024 | 10.1109/ICC51166.2024.10622619 / 2024 | 是（M 前身） | 部分 | 否 | PARTIAL_OVERLAP |
| Safi 2019 (TVT) | 10.1109/TVT.2019.2916843 / 2019 | 部分 | 是（FSO+est-error） | abstract 看不出 risk-aware | **UNVERIFIED**（全文 BLOCKED，FR-26）|
| ETRI 2026 rateless polar | 10.4218/etrij.2025-0461 / 2026 | 部分 | 部分 | 否 | DISTINCT |

**Q-A closure verdict = SURVIVES_STEP3_5**（带 Safi UNVERIFIED 尾巴）。无任何 FSO 文献做 posterior/risk-aware/outage-constrained code-rate rule under prediction error；Nguyen2024 点预测印证 A 开放。

### 11.2 Q-B 闭包（相干星地 AMC 动作位置-时间尺度失配）

| paper | DOI/year | 同 M | 同 C | 解决 A | verdict |
|---|---|---|---|---|---|
| L023 (JLT 2023) | 10.1109/JLT.2023.3242215 / 2023 | 是（M 本体） | **否**（terrestrial，自陈 LEO 不可行） | 否（单环，是 Q-B 解构对象） | PARTIAL_OVERLAP |
| Nguyen2024 (TAES) | 10.1109/TAES.2024.3403809 / 2024 | 部分（TX-only） | 是 | 部分（预测补偿非分层） | PARTIAL_OVERLAP |
| Slow/Fast AMC massive MIMO | 10.1049/cmu2.12389 / 2022 | 否（RF） | 否（RF） | **是（FAMC+SAMC 分层）** | DISTINCT（**RF split-timescale 先例，路径非空，未迁移 FSO/sat**）|
| L124 | 10.1364/oe.595557 / 2026 | 是（coherent AMC） | **否（terrestrial）** | 否 | PARTIAL_OVERLAP / UNVERIFIED（全文 BLOCKED）|
| L165 sat feeder coherent+AO | 10.1038/s41377-023-01201-7 / 2023 | 否（AO 层） | 部分（sat） | 否 | DISTINCT（boundary AO）|
| MaxSpecEff Coherent Terrestrial FSO (TCOMM 2026) | 10.1109/TCOMM.2026.3694829 / 2026 | 部分 | 否（terrestrial） | 否 | DISTINCT |

**Q-B closure verdict = SURVIVES_STEP3_5**（带 scenario-migration + baseline 缺位风险）。FSO/sat 域无分层契约直接竞品；RF massive-MIMO 先例（10.1049/cmu2.12389）证路径非空。**关键风险**：无合法 coherent 星地 AMC baseline（L023/L124/TCOMM2026/LCOMM2026 全 terrestrial；L165 sat 但 AO）→ Step 4a 量化对标需自建 coherent sat-ground GG 信道模型。

### 11.3 Step 3.5 终态

**Q-A + Q-B 均 SURVIVES_STEP3_5 → 存在 Step 4a 入口**（但本轮不启动，brief 明示到 Step 3.5 终态停止）。

**Safi/L124 全文获取**：均 3 路径失败仍 BLOCKED（Safi：tools/download all_failed + Unpaywall closed + 无作者稿；L124：tools/download all_failed + Optica HTTP 202 Radware JS-challenge + arXiv 0）。未绕过访问控制。

**Step 4a 前开放问题（非本轮终止条件）**：
1. Q-A Safi UNVERIFIED 尾巴：合法获取 Safi 全文关闭（IEEE 订阅/ILL）。
2. Q-B baseline 缺位：评估自建 coherent sat-ground GG 信道模型可行性（判据4 量化对标工程前提）。
3. Galijasevic DOI 异常（解析到 BELA 5G/6G）+ L023 backward citation 缺口：用正确 DOI/标题重跑 citation。
