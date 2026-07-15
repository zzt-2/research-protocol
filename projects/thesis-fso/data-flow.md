# 端到端数据流推演 — Q-CMA-FADE

> 产出阶段：Contract Step 4
> 用途：仿真器开发的设计文档，Execute 阶段对着此文件写代码
> 场景适配说明：8 步网络路由模板（星座配置→…→评估）不适用 Q-CMA-FADE（DSP 信号处理非网络），本文件按 DSP 信号流重构 8 步。每步标注真实代码来源（`common/*.py` + `explore/cma-fade-divergence/*.py`），不自创。

---

## 1. 信道配置 → 双偏振接收信号

- **输入**：GG 湍流参数 (α=1.5, β=0.8 strong) + Greenwood 频率 f_G (30/100/1000 Hz) + SOP_RATE (0 或 4e-7 rad/sym) + GAMMA_BAR (20dB=100) + 符号率 (2.5 GBaud, T_S=0.4ns) + 序列长度 N (2M/5M) + seed
- **处理**：
  1. τ_c = 1/(2π·f_G)（Conan 1995，`_gg_time.py:12`）
  2. GG 时间域包络 h = gg_time_envelope(N, α, β, τ_c)（块内恒定块间 AR(1) ρ=exp(-Δt/τ_c)≈0.99997，GAR 边缘 PDF，`_gg_time.py:106`）
  3. 两路独立 QPSK 符号 sX, sY（`gen_qpsk`，等概率 ±1±j）
  4. SOP 旋转角 θ = sop_rate·arange(N)（线性累积，`ml_long_seq_failure.py:162`）
  5. Jones 矩阵双偏振混合：
     - `rX = sqrt(h)·(cos(θ)·sX + sin(θ)·sY) + n_X`
     - `rY = sqrt(h)·(-sin(θ)·sX + cos(θ)·sY) + n_Y`
     （`ml_long_seq_failure.py:166-169`，2×2 旋转矩阵）
  6. AWGN：n_X, n_Y ~ CN(0, 1/(2·GAMMA_BAR))，X/Y 独立同分布
- **输出**：rX, rY ∈ ℂ^N（双偏振接收信号）, sX, sY ∈ ℂ^N（发送符号真值，监督用）, h ∈ ℝ^N（GG 包络，oracle/诊断用）, θ ∈ ℝ^N（SOP 角度，oracle 用）
- **维度检查**：rX/rY/sX/sY 同长 N；h/θ 同长 N；sop_rate=0 时 θ 全零（无 SOP 旋转对照，H1 验证用）

> **断层检查**：✅ 无。h 跨 seed 方差大（CV≈1.0，AR(1) 强相关致样本均值收敛慢，D012 seed-bias 债务）——这是统计特性非信号流断层，论文 limitations 标注。

## 2. 均衡器输入对齐

- **输入**：步骤 1 的 rX, rY（双偏接收）
- **处理**：三方均衡器（CMA / ML / oracle）接收**同一信道实现**（F1 数据同源）。三方输入维度完全一致：(rX, rY) 各 ℂ^N。
- **输出**：三方各自的输入接口已就绪
- **公平性**：`ber_vs_snr_scan.py:8,273-276` 确认三方共用 gen_channel 输出，仅均衡器实现不同。seed-bias 对三方同向偏置，比率免疫（D012）。

> **断层检查**：✅ 无。三方输入同源是 F1 的硬约束，代码已确认。

## 3. 均衡器处理（三方并行）

### B1 standard-CMA（2×2 蝶形，Godard 1980 含 z 因子）

- **输入**：rX, rY ∈ ℂ^N
- **处理**（`prompt019_mu_compress_mve.py` StandardCMA2x2，块级 2×2 蝶形）：
  1. 4 个复 FIR：wxx, wxy, wyx, wyy（各 n_tap=4 抽头）
  2. 中心抽头初始化：wxx/wyy 中心=1, wxy/wyx=0（`_cma.py:85-86`）
  3. 块级更新（block_size=64，sat.1553 §6.3 L756 并行化因子）：
     - 块内向量化滤波（`_cma.py:151-152`）：zX = wxx∗rX + wxy∗rY; zY = wyx∗rX + wyy∗rY
     - 块末梯度更新（`_cma.py:163-166`）：W += μ·mean(e·z·conj(r))，e = R²−|z|²，含 z 因子（标准 Godard）
  4. μ=1e-3（安全区，D006/D018）
- **输出**：zX, zY ∈ ℂ^N（均衡后符号）+ w_norm_traj + diverged 标志 + diverge_idx

### B4 ML（ButterflyCNNEqualizer2x2，Qin 2025 CNN）

- **输入**：rX, rY ∈ ℂ^N（训练段 early [0, 2.5M) + 测试段全段）
- **处理**（`_ml_equalizer.py`）：
  1. 8 实值 1D-CNN 实现 4 复蝴蝶 FIR（Qin 2025 L275/283）
  2. 训练：early 段 [0, n_train) 用 MSE 监督回归（sX, sY 作标签），lr=0.005, batch=1024, epoch 固定
  3. 推理：训练后权重**固定**，前馈均衡全段（不在线更新 → 不会发散）
- **输出**：zX, zY ∈ ℂ^N（全段均衡后符号）+ final_w_norm + loss 轨迹
- **信息泄露检查（F5）**：训练用 early [0, 2.5M)，测试指标用 late [4.375M, 5M)，无重叠 ✅

### B3 oracle MMSE（完美 CSI 下界）

- **输入**：rX, rY, h, θ, GAMMA_BAR
- **处理**（`ml_long_seq_failure.py:173` oracle_equalize）：
  1. 撤销 SOP 旋转：rX_u = cos(−θ)·rX + sin(−θ)·rY; rY_u = −sin(−θ)·rX + cos(−θ)·rY
  2. per-block MMSE 均衡（用完美 h）：zX = mmse_equalize(rX_u, h, GAMMA_BAR)
- **输出**：zX, zY ∈ ℂ^N（理论下界，仅分析层参考，不参与 Go/Kill，FR-25）

> **断层检查**：✅ 无。三方输出同为 (zX, zY) ℂ^N，可直接进同一评估管线。

## 4. 均衡器输出 → 判决 → 比特

- **输入**：zX, zY ∈ ℂ^N（三方各自输出）
- **处理**：
  1. QPSK 判决：Ĥ = sign(real(z)), Ĥ = sign(imag(z))（`qpsk_demap`）
  2. 比特恢复 → 与发送 bits 比对
- **输出**：原始 BER（per-stream，未消歧）

## 5. BER 计算（双口径，D018 强制）

- **输入**：zX, zY, sX, sY（步骤 3+4 产出）
- **处理**（`prompt012_longseq_audit.py:98` evaluate_outputs）：
  1. **fixed-label BER**（M2，主指标 FR-17）：直接固定流标签算 BER。swap 后 zX≈0.5（标签错配，非信息丢失）
  2. **PI-BER**（M1，辅指标）：穷举 2!×4×4 排列 + 相位消歧取最优 BER（`itertools.permutations((0,1))` × 4 相位旋转）。**需 pilot/帧头标识开销**完成流消歧（非免费）
  3. 相关性诊断：abs_corr(zX, sX), abs_corr(zX, sY)（swap 检测）
- **输出**：fixed_label_ber, permutation_invariant_ber, abs_corr 矩阵（2×2）, swap 分类（clean/degraded）

> **D018 强制**：任何性能结论 fixed/PI 必须并报。N=5M fixed≈0.5 是 clean swap（标签问题）非信息丢失；PI≈0.005-0.01 接近 oracle。
> **口径差异警示（D029 核验）**：`compute_ber_phase_corrected`（fixed-label 4 旋转口径）≠ D018 完整 PI-BER（2!×4×4 消歧）。引述历史数字时须标注口径。

## 6. 评估指标计算

- **输入**：步骤 5 的双口径 BER + 步骤 3 的发散标志/权重轨迹
- **处理**：
  - **M1 PI-BER**：步骤 5 已算（辅指标）
  - **M2 fixed-label BER**：步骤 5 已算（主指标，FR-17 领域首选 75%）
  - **M3 发散概率 P_div**：CMA 权重范数 > 10×init 的 trial 占比（`_cma.py:133` norm_thresh，D006 预注册）
  - **M4 PI ratio**：CMA PI-BER / oracle PI-BER（SOP 串扰恶化量化，D014）
- **输出**：per-trial 指标 → 跨 seed 聚合（均值 ± std / 配对 Wilcoxon p 值 / 胜场）

## 7. 统计聚合 + 假设检验

- **输入**：多 seed 的 per-trial 指标（E3 用 30 seeds，其他 5 seeds）
- **处理**：
  1. 均值 ± std
  2. 配对超额 PI-BER：ML_excess − CMA_excess（逐 seed）
  3. 双侧精确 Wilcoxon signed-rank（exact p，非 asymptotic——D022 核验确认 exact 正确）
  4. 胜场计数（ML < CMA 的 seed 数 / 总 seeds）
- **输出**：H1/H2 的 Go/No-Go 判据数字
  - H1：SOP×f_G 矩阵 ratio（prompt023 复现）
  - H2：ML 29/30 胜 standard-CMA, p=1.19e-6（D022，N=5M/f_G=30 窄域）

## 8. 跨参数泛化（适用域边界）

- **训练配置**：N=5M, f_G=30, SOP=4e-7, strong, 20dB, QPSK（H2 注册域）
- **推理/泛化配置**：维度变化及结论适用域
  - **N 变化（2M vs 5M）**：N=2M late SOP 漂移小→standard-CMA 完美锁定→ML 优势消失/反转（D023，f_G=1000 ML 仅 1/5 胜）。**结论：H2 仅限 N=5M**
  - **f_G 变化（30/100/1000）**：H1 SOP×f_G 矩阵覆盖三档（prompt023）；H2 仅 f_G=30 注册
  - **SOP_RATE 变化（0 vs 4e-7）**：H1 核心对照——SOP=0 ratio≈1.0 vs SOP>0 ratio 1.9-6.9×
  - **SNR 变化（10-40dB）**：E4 BER vs SNR 曲线（导师必须），CMA 高 SNR floor 0.03-0.10 vs ML/oracle→0
  - **调制变化（QPSK vs 16QAM）**：16QAM CMA modulus mismatch 结构性缺陷（BER 高 2.7×），但 ML/CMA gap 反预期小于 QPSK（D012 反预期）
- **处理方式**：ML 架构固定（权重随训练数据变），跨参数泛化靠**重新训练**（early 段）非架构自适应。D023 收窄：论文不得声称 ML 鲁棒优于 standard-CMA。

---

## [FR-13] 均衡能力表达力审计

> contract.md 的 FR-13 表格为 RL 动作空间设计。Q-CMA-FADE 是 DSP 信号处理非 RL，没有"动作空间"。适配为**均衡能力表达力审计**：逐 baseline 检查"均衡器能做什么决策"vs"ML 能做什么"，判断 ML ≥ / < / 可比。

| Baseline | Baseline 能做什么均衡决策 | ML（ButterflyCNNEqualizer2x2）能做什么 | ML ≥ Baseline？ |
|---|---|---|---|
| **B1 standard-CMA** | 在线块级梯度更新 4 FIR；恒模代价驱动；能实时跟踪 SOP 漂移（μ=1e-3 安全区）；但恒模多解地形下 SOP 旋转致权重跳 swap 盆地 | 前馈固定权重（early 段训练后冻结）；不能在线跟踪 SOP；但固定权重免疫恒模多解跳变（clean swap 后 PI≈oracle） | **可比（不同维度各有优劣）**：<br>• 在线跟踪能力：ML < CMA（CMA 能跟 SOP，ML 不能）<br>• swap 免疫：ML > CMA（固定权重不跳盆地）<br>• N=5M late SOP 漂移大→CMA 漂错解→ML 优（D022 29/30）<br>• N=2M late SOP 漂移小→CMA 完美锁定→ML 监督残余误差反更差（D023 f_G=1000 ML 1/5） |
| **B2 CMMA** | 多模代价（3 环）；16QAM 增强版 CMA | 同上（ML 不限星座阶数，直接回归星座点） | **≥（16QAM 场景）**：ML 不受 modulus mismatch 限制。但 QPSK CMMA=CMA 数学等价（R2=1.0，D013 逐 seed max diff=0.00） |
| **B3 oracle MMSE** | per-block LS 完美 CSI 最优；撤销 SOP + MMSE 均衡 | 有限训练数据监督学习信道逆 | **<（信息差）**：oracle 用完美 (h, θ)，ML 只见 (rX, rY)。这是**理论下界 vs 实际方法**的本质差距，预期且合理（FR-25 oracle 不做 Go 判据） |

### 门控判定

- **B1 可比（非严格 ≥ 也非严格 <）**：ML 与 standard-CMA 在不同维度各有优劣，须在 Contract 标注具体条件（D023 窄域）。
  - ✅ 条件 1 已标注：N=5M/f_G=30/SOP 漂移大时 ML 优（H2 注册域，D022 29/30）
  - ✅ 条件 2 已标注：N=2M/SOP 漂移小时 standard-CMA 完美锁定反超（D023，论文 limitation）
  - ✅ 与 success signal 评估场景一致（H2 明确限定 N=5M/f_G=30 窄域）
- **B2 ≥（16QAM）/ 等价（QPSK）**：通过
- **B3 <（预期，oracle 是下界参考）**：通过（FR-25，oracle 不参与 Go/Kill）

**结论**：FR-13 门控通过。ML < CMA 在跟踪能力是已知限制（D023 窄域），已在 Contract H2 适用边界 + Experiment E5（N=2M 扩参数域）显式标注。论文须诚实呈现 limitation，不得声称 ML 鲁棒优于 standard-CMA。

---

## [FR-16] 架构信息增量审计

> 对 ML（ButterflyCNNEqualizer2x2）用两个不同输入验证产生不同输出。诚实结论预期：ML 是 Qin 架构迁移，信息增量审计主要验证"监督学习确实让权重区别于初始化"。

### 审计对象

ML 核心组件 = ButterflyCNNEqualizer2x2（`_ml_equalizer.py:104`），4 复 FIR 蝶形。

### 输入 A vs 输入 B

- **输入 A**：训练前的 ML（中心抽头初始化，wxx/wyy 中心=1, wxy/wyx=0，等价 identity 通道）
  - zX_A = 1·rX + 0·rY = rX（直通，未均衡）
  - zY_A = 0·rX + 1·rY = rY
- **输入 B**：训练后的 ML（early 段 MSE 监督学习后，权重已调整）
  - zX_B = wxx_trained∗rX + wxy_trained∗rY（学习到信道逆）
  - zY_B = wyx_trained∗rX + wyy_trained∗rY

### 信息增量验证

| 检查项 | 输入 A（未训练） | 输入 B（训练后） | 有信息增量？ |
|---|---|---|---|
| zX 输出 | = rX（直通） | ≠ rX（均衡后）| ✅ 是 |
| BER（fixed） | ≈0.5（未均衡，随机） | <0.5（均衡成功时） | ✅ 是 |
| BER（PI） | ≈0.5 | 0.005-0.01（D022） | ✅ 是 |
| 交叉支路 wxy/wyx | =0（初始化） | ≠0（学到 SOP 补偿） | ✅ 是 |

### 诚实结论

- **信息增量存在**：训练后权重区别于初始化，输出从"直通未均衡"变为"均衡后"，BER 从 0.5 降到 0.005-0.01。监督学习确实让 ML 产生了初始化不具备的均衡能力。
- **但增量来源是监督学习数据，不是架构创新**：D022 已证 ML-original（4 FIR 中心全=1）vs ML-aligned（wxy/wyx=0）几乎无差（均值差 7.6e-7）——**初始化不是性能来源**。性能来自 early 段 MSE 监督学到的信道统计。
- **架构本身是 Qin 迁移**（F4 公平性声明）：ButterflyCNNEqualizer2x2 结构照搬 Qin 2025 L275/283，无架构创新。诚实标注"场景迁移 + 分析增量"，方法层卖点在 D022 窄域 PI 优势非架构新颖性。

**门控判定**：FR-16 通过。信息增量真实存在（训练前后输出不同），但增量属性是"监督学习数据驱动"非"架构创新"，已诚实标注（F4）。
