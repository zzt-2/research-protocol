---
created: 2026-07-15
status: frozen
version: 1
frozen_date: 2026-07-15
stage: Contract S0-S5 全过 + 用户确认冻结（FR-17 主指标调整已确认）
---

# Research Contract — Q-CMA-FADE

> 本 Contract 冻结 Q-CMA-FADE 的研究假设和实验方案。
> GW Step 4a 完成后定型形态：分析层（强，7 项稳结论）+ 方法层（弱，D022 窄域 PI 优势）。
> **reframe 后叙事**（主控 2026-07-15 定）：旧叙事"ML 缓解发散"已被 D014 证伪。新叙事 = 分析层 D014（SOP 极化串扰是 BER 真因）+ 方法层 D022（ML PI 优势）焊在一起。

## Problem Reference

- **引用问题**：Q-CMA-FADE（由 Q-DP2 + Q-ML1 合并，D005）。M-C-A 过 glossary 四判据（literature_notes L1133-1142，全过最强）。
- **问题陈述**：
  - **M**（失效/不足的现有方法）：传统 CMA（Constant Modulus Algorithm）2×2 蝶形盲均衡器，在双偏振星地相干 FSO 场景下做偏振解复用
  - **C**（条件）：星地 GG 湍流深衰落 + SOP（State of Polarization）持续旋转
  - **A**（失效假设/不足）：CMA 恒模代价函数收敛点不唯一（任意酉旋转保恒模），SOP 持续旋转下权重跳到混淆 X/Y 偏振的次优解（polarization lock swap），导致 BER 恶化（SOP=0 时 CMA=oracle，SOP>0 时 ratio 1.9-6.9×，D014 决定性矩阵 + prompt023 复现）

> **reframe 说明**：GW 时 A 写的是"CMA 在深 fade 发散"（Q-DP2 原始叙事）。经 D014 主控独立诊断 + prompt023 系统化复现，**真因是 SOP 极化串扰不是发散**（发散由 μ 主导，是独立现象，D006/D010）。本 Contract 用修正后的 A。

## Hypothesis

**H1（分析层，强）**：在双偏振星地 GG 湍流 + SOP 旋转场景下，standard-CMA 的 BER 恶化**主要由 SOP 驱动的极化串扰（polarization lock swap）导致**，而非传统认为的跟踪滞后或深衰落触发发散。具体可量化预测：消除 SOP（SOP_RATE=0）后 CMA PI-BER/oracle ratio → 1.0（全 f_G 档）；存在 SOP（4e-7 rad/sym）时 ratio 升至 1.9-6.9×。

**H2（方法层，弱，窄域）**：在 N=5M/f_G=30/SOP=4e-7/strong/20dB/QPSK 参数域内，ML 均衡器（ButterflyCNNEqualizer2x2，Qin 2025 CNN 架构迁移）的 PI-BER **统计显著优于 standard-CMA**（预注册 29/30 胜，exact p=1.19e-6，D022）。

> **H2 适用边界**（D023 收窄，不得逾越）：H2 仅覆盖 N=5M/f_G=30 窄域。N=2M 下 ML 优势在多数参数点消失或反转（f_G=1000 ML 仅 1/5 胜）。论文不得声称 ML 鲁棒优于 standard-CMA。

## Success Signal

- **H1（分析层）PASS 标准**：SOP×f_G 矩阵复现（prompt023，5 seeds）确认 SOP=0 时 PI ratio≈1.0（全 f_G 档），SOP>0 时 ratio 显著>1.0。**已达**（prompt023 复现 PASS）。
- **H2（方法层）PASS 标准**：在注册参数域（N=5M/f_G=30/SOP=4e-7/strong/20dB/QPSK），ML 相对 standard-CMA 配对超额 PI-BER，双侧精确 Wilcoxon p<0.05 且 ML≥25/30 胜（D022 预注册）。**已达**（29/30，p=1.19e-6）。

## Failure Signal

> 独立定义，不是 success 的反面。

- **H1 FAIL**：SOP=0 时 PI ratio 显著>1.0（>1.5×），说明 SOP 不是主因（CMA 有其他独立瓶颈）。**未触发**。
- **H2 FAIL**：在注册参数域 standard-CMA vs ML 不满足主判据（p≥0.05 或 ML<25/30 胜），方法层卖点塌缩。**未触发**（已 PASS）。
- **适用域 FAIL**（D023）：论文若声称 ML 在窄域外鲁棒优于 standard-CMA → 超出证据范围 = failure。

## Baselines

> FR-25 Go/Kill 对手标准分离：Go 判据用传统未优化 baseline（standard-CMA），oracle 只做分析层上界参考。

- **B1: standard-CMA（2×2 蝶形，Godard 1980 含 z 因子）**（来源: Godard 1980 IEEE T-ASSP + sat.1553 §6.3）— 复现状态: ✅ 已复现（prompt019 StandardCMA2x2）— 交叉验证: CMA 是相干光 DSP 偏振解复用的**领域标准方法**（sat.1553 §6 主轴，被全部精读论文使用）
  - 注：D020/D021 修正了两个 baseline 混杂（current-CMA 缺 z 因子 + ML 交叉支路初始化），D022 统一合法 baseline 重比后 standard-CMA 是合法经典 CMA
- **B2: CMMA（Cascaded Multimodulus CMA）**（来源: R2/S011 实测）— 复现状态: ✅ 已复现 — 交叉验证: 16QAM 增强版 CMA。**非强 baseline**（16QAM 仅优 CMA 0.4-0.9%，QPSK 数学等价）
- **B3: oracle MMSE（完美 CSI 线性接收机下界）**（来源: 自实现 per-block LS 最优）— 复现状态: ✅ 已实现（prompt020 B2）— 交叉验证: 理论下界，不直接做 Go/Kill 判据（FR-25），只做分析层"距上界多远"参考
- **B4: ML（ButterflyCNNEqualizer2x2，Qin 2025 CNN）**（来源: Qin 2025 OFC L275/283 架构）— 复现状态: ✅ 已实现（_ml_equalizer.py）— **本研究的"提出方法"**（场景迁移 + MSE 监督，非架构创新）

## Metrics

> FR-17 审计后调整（PI-BER 首选率 0%，需补领域通行指标）。

- **M1: PI-BER（Polarization-Invariant BER，排列不变误码率）** — 穷举 2!×4×4 消歧取最优 BER（D018 口径）— 越低越好。**Q-CMA-FADE 主比较口径**。需 pilot/帧头标识开销（非免费性能）。[FR-17 领域首选率 0%（非标准命名），但底层消歧操作是领域事实常规。**降级为辅指标**]
- **M2: fixed-label BER（固定标签 BER）** — 直接固定流标签算 BER（swap 后≈0.5，标签错配非信息丢失）— 越低越好。[FR-17 领域首选率 75%，**领域通行首选指标，升级为主指标**]
- **M3: 发散概率 P_div** — CMA 权重范数>10×init 的 trial 占比（D006）— 越低越好。[FR-17 领域认可指标（CA-CMA #3 显式报告），**分析层核心指标**]
- **M4: PI ratio（CMA PI-BER / oracle PI-BER）** — SOP 极化串扰恶化量化（D014）— 越接近 1.0 越好。[分析层诊断指标，Q-CMA-FADE 特色]

> **D018 双口径强制**：任何性能结论 fixed/PI 必须并报。N=5M 的 fixed≈0.5 是交换（标签问题）非信息丢失；PI-BER 需 pilot/帧头开销。
> **FR-17 处置**：原拟 PI-BER 做主指标，审计后改 **fixed-label BER 做主指标（领域首选 75%）+ PI-BER 做辅指标（Q-CMA-FADE 特色诊断口径）+ 发散概率 + PI ratio 做分析层指标**。论文须说明 PI-BER 的消歧开销。

### [FR-19] 指标模型假设敏感性

| 指标 | 模型假设 | 选择理由 | 替代假设 |
|---|---|---|---|
| PI-BER | 穷举 2!×4×4 排列+相位消歧（假设接收端有 pilot/帧头标识） | D018 双口径强制，消除盲分离排列歧义 | fixed-label（无消歧，swap 后≈0.5）|
| 发散概率 P_div | 权重范数>10×init 判据 | D006 预注册 | threshold 2×/5×（D010 阈值敏感性已测）|
| oracle MMSE | per-block LS 最优（假设完美 CSI） | 线性接收机理论下界 | 有限 CSI MMSE（未测，Execute 可补）|

## Fairness Rules

- **F1 数据同源**：CMA/ML/oracle 使用**同一信道实现**（同 seed → 同 h → 同 theta），ber_vs_snr_scan.py:8,273-276 确认三方同信道。比率免疫 seed-bias。
- **F2 预处理同源**：三方共用 GG 信道生成（gen_channel），仅均衡器不同。
- **F3 超参搜索预算**：CMA μ=1e-3（安全区，D006/D018 确定，非调优结果）；ML 训练配置固定（Qin 2025 架构 + MSE 监督，lr/epoch 固定）。
- **F4 公平性声明（诚实标注）**：
  - **监督 vs 盲不公平**（D008 债务 1）：ML 用 MSE 监督（需 pilot），CMA 盲。PROMPT-014 盲 VQ-VAE gate 崩（D019 deferred），未做盲 vs 盲公平对比。**论文须声明**。
  - **初始化已统一**（D021/D022）：ML-original（4 FIR 中心全=1）vs ML-aligned（wxy/wyx=0）几乎无差（均值差 7.6e-7），初始化不是性能来源。
  - **方法照搬 Qin**（D008 债务 2）：ML 架构 = Qin 2025 ButterflyCNNEqualizer2x2，无架构创新。诚实标注"场景迁移 + 分析增量"。
- **F5 信息泄露检查**：oracle 用完美 CSI（h, theta）做 per-block LS，**仅作下界参考不参与 Go/Kill**（FR-25）。ML 训练用 early 段（[0, 2.5M)），测试用 late 段（[4.375M, 5M)），无信息泄露。

## Ablation Plan

| 编号 | 消融目标 | 预期影响方向 | 预期影响大小 |
|---|---|---|---|
| A1 | SOP_RATE=0（消除极化旋转）| CMA PI ratio → 1.0（H1 核心验证）| 大（ratio 从 1.9-6.9× 降到 1.0）|
| A2 | μ 扫描（1e-4~1e-2）| 发散概率 P_div 随 μ 主导变化 | 大（D006 μ 主导）|
| A3 | f_G 扫描（30/100/1000）| SOP>0 时 ratio 随 f_G 变化 | 中（D014 矩阵）|
| A4 | N 扫描（2M/5M）| ML 优势在 N=2M 消失/反转 | 大（D023 收窄，适用域边界）|
| A5 | 冻结 CMA 更新（R7）| ΔP_div=0（冻结无效）| 无（D010 已证）|

## Experiment List

| 编号 | 实验名 | 类型 | 优先级 | 状态 |
|---|---|---|---|---|
| E1 | SOP×f_G 决定性矩阵（H1 核心）| 核心 | P0 | ✅ prompt023 复现 PASS |
| E2 | 发散概率扫描（D006 分析层）| 核心 | P0 | ✅ 384 trials PASS |
| E3 | ML vs standard-CMA 30-seed 预注册（H2 核心）| 核心 | P0 | ✅ D022 PASS 29/30 p=1.19e-6 |
| E4 | BER vs SNR 曲线（导师必须）| 核心 | P0 | ✅ D012 4f_G×13SNR×5seeds |
| E5 | N=2M 扩参数域（D023 适用域边界）| 鲁棒 | P1 | ✅ 6 cells 5 seeds（反预期）|
| E6 | CMMA 对比（B2 增强 baseline）| 对比 | P1 | ✅ R2/S011 |
| E7 | 冻结/压μ/回滚响应式（D010/D026/D028）| 消融 | P2 | ✅ 三类全 FAIL（分析层贡献⑦）|
| E8 | 统计严谨性补强（≥30 seeds + error bar）| 鲁棒 | P1 | ⬜ 待 Execute（超领域惯例）|

## Simulation Config

**信道模型**：
- 双偏振相干 intradyne 单孔径单链路，GG 湍流幅度闪烁 + SOP 旋转
- GG 时间域衰落：gg_time_envelope（块内恒定块间 AR(1)，ρ=exp(-Δt/τ_c)，GAR 边缘 PDF）
- SOP 旋转：theta = sop_rate · arange(N)（线性累积，模拟机械振动/热漂移致 SOP）

**湍流参数**：
- strong 湍流：α=1.5, β=0.8（GG 分布参数，Rytovvar 强湍流区）
- f_G（Greenwood 频率）扫 30/100/1000 Hz
- τ_c = 1/(2π·f_G)（Conan 1995 相干时间）

**信号参数**：
- 调制：QPSK（主）+ 16QAM（辅，D008 modulus mismatch）
- 符号率：2.5 GBaud（T_S = 0.4ns）
- SNR：20dB（主，GAMMA_BAR=100）+ 10-40dB 扫（E4）
- N=5M 符号（主）/ N=2M（E5 适用域）
- CMA：block_size=64，μ=1e-3（安全区），2×2 蝶形 4 tap

**ML 配置**：
- ButterflyCNNEqualizer2x2（Qin 2025 OFC 架构，8 实值 1D-CNN 蝶形）
- 损失：MSE 监督（非 Qin VAE ELBO，简化）
- 训练：early 段 [0, 2.5M)，测试：late 段 [4.375M, 5M)

**SOP 参数**：
- SOP_RATE=4e-7 rad/sym（1 krad/s，sat.1553 §6.3 仿真值）
- SOP_RATE=0（H1 消除极化旋转对照）

## 数据集设计（自建）

### 参数空间

| 参数 | 取值范围 | 文献溯源 | 备注 |
|---|---|---|---|
| α, β（GG） | strong: 1.5, 0.8 | [来源: sat.1553 §6.3 strong 档] | Rytov 强湍流 |
| f_G | 30/100/1000 Hz | [计算: Greenwood 1977 f_G 公式] | τ_c=1/(2πf_G) |
| SOP_RATE | 0 / 4e-7 rad/sym | [来源: sat.1553 §6.3 仿真值] | ⚠️ 非实测，见 Parameter Provenance |
| N | 2M / 5M | [设计选择: D012 N=2M τ_c 比 0.13→0.5；D022 N=5M late slice] | |
| SNR | 10-40dB | [设计选择: 覆盖低-高 SNR] | |
| μ | 1e-4 ~ 1e-2 | [来源: Godard 1980 + D006 安全/临界/危险区] | |

### 数据规模和划分

- 每 cell：5-30 seeds（核心 E3 用 30 seeds，其他 5 seeds 探索）
- 划分：ML 训练 early [0, 2.5M) / 测试 late [4.375M, 5M)（无泄露，F5）

## Parameter Provenance

> FR-20 参数溯源审计。每个参数三选一标注。

| 参数 | 值 | 来源 | 备注 |
|---|---|---|---|
| α, β (GG strong) | 1.5, 0.8 | [来源: sat.1553 §6.3 L755 strong 档] | |
| f_G | 30/100/1000 Hz | [计算: Greenwood 1977 JOSA 67(3):390 + Andrews&Phillips 2005] | _gg_time.py:11 |
| τ_c | 1/(2π·f_G) | [来源: Conan 1995 JOSA A 12(7):1559] | _gg_time.py:12, 典型 1-100ms |
| ρ (AR(1)) | exp(-Δt/τ_c)≈0.99997 | [计算: Δt=block·t_s=64·0.4ns, τ_c≫Δt] | τ_c≫block·t_s 准静态 |
| **SOP_RATE** | **4e-7 rad/sym (1 krad/s)** | **[来源: sat.1553 §6.3 仿真值]** | **⚠️ 已知债务：非实测，是 sat.1553 §6.3 的仿真设定值。真实机械振动/热漂移致 SOP 实测速率缺失（D001/现有债务）。论文须诚实标注** |
| SOP_RATE=0 | 0 | [设计选择: H1 消除极化旋转对照诊断] | theta全0，prompt023 验证 |
| N | 5M / 2M | [设计选择: D012 物理前提检查 N=2M=0.5τ_c；D022 N=5M late slice] | |
| block_size | 64 | [来源: sat.1553 §6.3 L756 并行化因子] | |
| μ (CMA) | 1e-3 (安全区) | [来源: Godard 1980 + D006/D018 安全区审计] | D018 收紧：μ≤1e-3 非零风险（3/20 发散）|
| R2 (QPSK) | 1.0 | [计算: QPSK 恒模 R²=E[\|s\|⁴]/E[\|s\|²]=1] | |
| N_TAP | 4 (2×2 蝶形 = 4 复 FIR) | [来源: sat.1553 §6.3 + Godard 1980 蝶形结构] | |
| GAMMA_BAR | 100 (20dB) | [设计选择: 中高 SNR 主测试点] | |
| T_S | 0.4ns (2.5 GBaud) | [来源: sat.1553 §6.3 符号率] | |
| ML 架构 | ButterflyCNNEqualizer2x2 | [来源: Qin 2025 OFC L275/283] | 场景迁移非创新 |
| ML 损失 | MSE 监督 | [来源: Freire 2022 6 陷阱 checklist] | 非 Qin VAE ELBO |
| 发散判据 | norm>10×init | [来源: D006 预注册] | D010 阈值敏感性已测(2×/5×) |

> **所有 [ASSUMPTION] 已消除**。SOP_RATE 是已知债务（仿真值非实测），论文 limitations 标注。

## 声称-证据初步映射（Step 2）

| Claim | Type | Planned Experiment | Expected Evidence |
|---|---|---|---|
| C1: SOP 极化串扰是 CMA BER 恶化真因（非发散/跟踪滞后）| bounded | E1 SOP×f_G 矩阵 | prompt023: SOP=0 ratio≈1.0, SOP>0 ratio 1.9-6.9× |
| C2: 发散概率由 μ 主导（补 sat.1553 §6.3 L778 空白）| universal(条件域) | E2 384 trials 发散扫描 | D006: μ≤1e-3 安全区/μ≥1e-2 危险区 |
| C3: ML 在窄域 PI-BER 统计显著优于 standard-CMA | bounded(窄域) | E3 30-seed 预注册 | D022: 29/30, p=1.19e-6 |
| C4: 冻结/压μ/回滚三类响应式方法均无效 | universal(D3 维度) | E7 三类对比 | D010/D026/D028: 全 FAIL |
| C5: CMMA 不降发散（多模修星座不修 μ 发散）| universal | E6 R2 对比 | R2: 32/32 逐点相同 |

> **scope 审计**：C1/C3 bounded（特定参数域），C2/C4/C5 universal（条件域内普适）。C3 最窄（仅 N=5M/f_G=30），论文须诚实标注 limitation。

---

## Contract S0-S5 完成状态（冻结 2026-07-15）

- **S0（新颖性检索）**：✅ PASS — 复用 GW 29 篇精读 + R002/R005。reframe 后增量定位冻结：分析层 7 项 Qin/Nasr 全空白 + 方法层窄域 PI 优势 + 架构迁移诚实标注。不换皮。
- **S1（瓶颈诊断）**：✅ PASS — 引用 D014。瓶颈 = 恒模多解 SOP 跳变（表达力/结构性瓶颈），SOP=0 时 CMA=oracle 证明非架构瓶颈。
- **S2（指标模型审计）**：✅ PASS — FR-17 PI-BER 首选率 0% → 主指标改 fixed-label BER（75%），PI-BER 降辅指标。FR-19 模型假设记录。D018 双口径强制。
- **S3（参数溯源审计）**：✅ PASS — 所有 [ASSUMPTION] 消除。SOP_RATE 仿真值债务标注。D014 SOP=0 矩阵债务已补（prompt023 复现 PASS）。
- **S4（端到端推演）**：✅ PASS — data-flow.md 创建（8 步 DSP 信号流推演 + FR-13 均衡能力表达力审计 + FR-16 架构信息增量审计）。8 步全标真实代码来源。FR-13 门控通过（B1 可比窄域已标注 D023；B3 < oracle 预期 FR-25）。FR-16 门控通过（信息增量真实但来源是监督学习数据非架构创新，F4 诚实标注）。
- **S5（压力测试 + 反模式 + 实验完备性）**：✅ PASS — experiment_completeness_checklist.md 创建。5 问压力测试无致命风险；反模式 4 项 3 pass + 1 注意（反模式 3 已诚实标注 D023 非致命）；Tier 1 六项全 pass（T1-4 适配 DSP 单组件）。

## 冻结状态（2026-07-15，用户确认）

**Contract 冻结**。不可变字段：hypothesis（H1+H2）/ success_signal / failure_signal / fairness_rules / ablation_plan / experiment_list 结构。

**FR-17 冻结调整（用户确认）**：主指标 fixed-label BER（领域首选 75%），PI-BER 降辅指标（Q-CMA-FADE 特色诊断口径，须标 pilot/帧头开销）。D018 双口径强制保留。

**已知债务（冻结时标注，Execute/论文须处理）**：
1. 监督 vs 盲不公平（D008 债务 1）— F4 已标，论文 limitations
2. 方法照搬 Qin CNN（D008 债务 2）— F4 已标，诚实"场景迁移 + 分析增量"
3. seed-bias（h_mean CV≈1.0）— E8 待 Execute 补 30 seeds，论文 limitations
4. SOP_RATE 仿真值非实测 — Parameter Provenance 已标，论文 limitations
5. BER 10⁻⁵ 达不到 — 当前 PI-BER 2e-3~3e-2，S2 指标审计已处理（pre-FEC 口径）

**下一步**：Execute 阶段（H011 handoff 已写）。
