# Q-CMA-FADE 探索：CMA 深衰落发散 — 分析 + ML 缓解

> 方向: Q-CMA-FADE | 来源: D005（Q-DP2+Q-ML1 合并） | 状态: MVE-PASS | 创建: 2026-07-11
> 组织规范: `../SIM-ORG.md` | 物理真相源: `../SPEC.md`

## 研究问题

**M-C-A**：传统 CMA 均衡器在星地 GG 湍流深衰落下系数发散/收敛失败——sat.1553§6 **自认**"probability of the equalizer diverging ... has not been analyzed"（领域级空白），L-DP8 实证深衰落致系数发散（ACP 2025）。

**四判据**：全过（见 `projects/thesis-fso/literature_notes.md` Q-CMA-FADE 章节）。

**贡献两层**：
1. 分析层：量化 CMA 在 GG 深衰落下发散的概率/条件（补 sat.1553 空白）
2. 方法层：ML 均衡器深衰落下缓解发散 vs CMA（补 Qin/Nasr 实验缺口）

## MVE 契约（FR-11）

| 维度 | 内容 |
|------|------|
| **动作空间** | 无（分析型）/ 均衡器系数选择（方法型） |
| **决策粒度** | 逐符号均衡（符号级） |
| **对比范式** | vs 传统 CMA（发散概率 + BER + 收敛速度 + 深衰落恢复时间） |
| **测度/奖励** | 发散概率（主）+ BER + 收敛速度 + 恢复时间 |
| **先验 baseline（FR-14）** | 固定步长 CMA |
| **贡献目标 baseline（FR-15）** | Qin2025 VAE / Nasr2026 ANN（竞品） |
| **物理场景** | 星地 GG 湍流深衰落，双偏振相干 |

## Conditional 风险（MVE 前必查）

1. **FR-20 GG 时间域衰落模型需自建**——现有文献只给幅度 PDF，衰落持续时间/频率全缺失。MVE 前先建此模型。
2. **与 Qin 小组抢位**——增量定位必须扎实（真实深衰落 + 发散机制），避免换皮（TL-12/D006）
3. **FR-21 oracle 上界**——深衰落下 ML vs CMA 增益若 <0.5dB 需查（但这里测度不止 dB，还有发散概率）
4. **Freire2022 6 陷阱 checklist**（L-ML9）——实验必须遵守（jail window/PRBS 周期/BER 非 EVM/batch/复杂度 RMpS）

## 脚本清单

| 脚本 | 用途 | 状态 | 结果位置 |
|------|------|------|---------|
| gg_time_fading_model.py | FR-20 GG 时间域衰落模型生成+验证 | **PASS** (2026-07-11) | results/cma-fade-divergence/gg_time_validation.json |
| cma_divergence_scan.py | CMA 发散概率 vs {湍流,f_G,μ,tap} 扫描 | **PASS** (2026-07-11) | results/cma-fade-divergence/cma_divergence_scan_results.json |
| mve_cma_vs_ml.py | CMA vs ML 均衡深衰落对比 (三方: CMA/ML/oracle) | **PASS** (2026-07-11) | results/cma-fade-divergence/mve_cma_vs_ml_results.json |
| sup_stress_test.py | 压力测试 (16QAM/小步长CMA/ML SOP漂移) | **PASS** (2026-07-11) | results/cma-fade-divergence/sup_stress_test_results.json |
| r1_analytical_bound.py | R1: 发散半解析界推导+验证 | **PASS** (2026-07-11) | results/cma-fade-divergence/r1_analytical_bound_results.json |
| r4_fade_correlation.py | R4: 发散事件 vs AFD/LCR 相关性 | **PASS** (2026-07-11) | results/cma-fade-divergence/r4_fade_correlation_results.json |
| r5_drift_validation.py | R5: 系数漂移模型验证 (√n律) | **PASS** (2026-07-11) | results/cma-fade-divergence/r5_drift_validation_results.json |
| r2_cmma_divergence.py | R2: CMMA 多模发散扫描 (16QAM+QPSK) | **PASS** (2026-07-11) | results/cma-fade-divergence/r2_cmma_divergence_results.json |
| r7_freeze_quantification.py | R7: 被动冻结效果量化 (sat.1553[79]) | **PASS** (2026-07-11) | results/cma-fade-divergence/r7_freeze_results.json |
| r4_corrected_sop_rate.py | R4修正: 1krad/s SOP+10M符号重跑 | **PASS** (2026-07-11) | results/cma-fade-divergence/r4_corrected_results.json |
| r_lcr_mechanism.py | LCR机制验证: 发散vs衰落事件位置+剂量效应 | **PASS** (2026-07-12) | results/cma-fade-divergence/r_lcr_mechanism_results.json |
| r_lcr_ber_impact.py | LCR的BER影响: CMA跟踪滞后+ML优势验证 | **PASS** (2026-07-12) | results/cma-fade-divergence/r_lcr_ber_impact_results.json |
| ml_long_seq_failure.py | PROMPT-010: ML 长序列失效边界诊断 (Q1 N扫描/Q2 SOP扫描/Q3 机制对照) | **PASS** (2026-07-12) | results/cma-fade-divergence/ml_long_seq_failure_results.json |

## 参数溯源（FR-20）

关键物理参数（已补全，标文献来源）：

| 参数 | 值 | 来源 | 备注 |
|------|-----|------|------|
| GG 信道 (α,β) | weak(4,3)/mod(2.5,1.8)/strong(1.5,0.8)/uplink_strong(1.0,0.7) | params.py TurbulenceParams | F32/F33 |
| Greenwood 频率 f_G | 30-1000 Hz 扫描 | Greenwood 1977 + arxiv 2208.00836:51 | F33b, 守 C1 扫描 |
| 强度闪烁相干时间 τ_c | 0.16-5.3 ms (=1/(2πf_G)) | Conan 1995 JOSA A 12(7):1559 | F33b |
| 横风速度 v | 10 m/s 典型 | photonics10121312:566 | Bufton 模型 |
| Cn² 地面值 | 1e-15~1e-13 m⁻²ᐟ³ | photonics10121312:560 | H-V 剖面 |
| 强度功率谱滚降 | f⁻¹¹ᐟ³ | Tatarskii 1971 / Clifford 1971 | F24/F25 已覆盖 |
| AR(1) 块间相关 ρ | exp(-block·t_s/τ_c) | F3.28/F3.29 既有 | 实现见 _gg_time.py |
| **CMA 步长 μ** | 5e-4~1e-2 扫描 | sat.1553 §6.3 L760 "step size μ" | Godard 1980; Qin 2025 L263 隐含量级 |
| **CMA tap 数** | 11/22 | sat.1553 §6 L572 / Qin 2025 L263 (22 tap) | 信道脉冲响应长度定 |
| **恒模半径 R²** | 1.0 (QPSK) | Godard 1980: R=E[\|s\|⁴]/E[\|s\|²] | QPSK \|s\|=1 → R²=1 |
| **CMA 并行化因子** | 64 (block_size) | sat.1553 §6.3 L756 "parallelization factor of 64" | 块级更新模拟 FPGA 实现 |
| **ML 网络结构** | 8 实值 1D-CNN = 4 复蝴蝶 FIR | Qin 2025 L275/283 | 结构标来源, 不照搬 VAE 损失 |
| **ML tap 数** | 11 | sat.1553 Fig.13 (跟 CMA 对齐) | Qin 2025 L283 用 29 |
| **ML 学习率** | 0.005 | Qin 2025 L397 | + ReduceLROnPlateau |
| **ML batch size** | 1024 | Freire 2022 L349 | ≥1024 防 jail window |
| **ML 损失** | MSE 监督回归 | Freire 2022 陷阱 4 (MSE > CEL) | 不用 Qin 的 VAE ELBO (增量定位) |
| **ML SOP 速率** | 1 krad/s (4e-7 rad/sym) | sat.1553 §6.3 L778 "OSL SOP ~krad/s" | 真实 OSL 速率 (Step B 的 250 krad/s 过快) |
| **ML 复杂度 RMpS** | 88 (8×n_tap) | Freire 2022 L441 | = CMA RMpS (同 tap 数) |

## Step A 验证结果（2026-07-11，PASS）

**生成器**：`common/_gg_time.py::gg_time_envelope`（块内恒定，块间 AR(1) 相关，τ_c 控制相干时间）

**方法对比**（验证 GG PDF + ACF）：
| 方法 | 边缘 PDF (KS) | log-ACF[1] err | 适用 |
|------|--------------|----------------|------|
| **gar**（默认）| <0.006 全湍流档 ✓✓ | <2% | 全湍流强度（边缘精确）|
| lognormal | 0.046-0.149（强湍偏差大）| 0.00% 精确 ✓✓ | 弱中湍（log-ACF 精确）|

**验证结论**：
- 边缘 PDF (GAR)：PASS（KS<0.006，全湍流档精确 Gamma）
- 自相关 τ_c (lognormal log-ACF)：PASS（lag=1 误差 0.00%）
- 文献 τ_c 范围：PASS（1.59/5.31ms 落 sat.1553/s24248036 的 1-100ms 区间）
- **物理发现**：τ_c ≫ block·t_s（1.59ms vs 0.04µs = 4×10⁴ 倍）→ ρ>0.9999，单帧内近似准静态（与 sat.1553 L167 物理一致），时间动力学需序列长 ≫ τ_c/t_s 才显现

**FR-20 缺口状态**：已补全（f_G/τ_c 公式 + 数值全标来源 F33b）。Step B/C 可用。

## 复用的 common/ 模块

- `common._channel.gg_block` — GG 信道（块内恒定块间独立，**不改**——P4）
- `common._gg_time.gg_time_envelope` — **GG 时间域衰落模型（Step A 新建，块间 AR(1) 相关）**
- `common._cma` — **CMA 均衡器（Step B 新建，2×2 蝶形 + 1×1 退化，Godard 1980 公式溯源）**
- `common._equalizer` — MMSE 均衡（已有，不改）
- `common._modulation` — QPSK/16QAM + ber_eval
- `common._ml_equalizer` — **ML 均衡器（Step C 新建，8 实值 1D-CNN 蝶形 + MSE 监督，Qin 2025 L275/283 架构）**
- `common._experiment` — run_* 编排 + save_results

## Step B 验证结果（2026-07-11，PASS）

### 扫描配置

- **序列长度**: 5M 符号 @ 2.5 GBaud（覆盖 0.3~16 个 τ_c 周期，取决于 f_G）
- **试验数**: 3 seeds/组合（P_div 分辨率 0.33）
- **总组合**: 4 湍流档 × 4 f_G × 4 μ × 2 tap = 128 组合 × 3 seeds = 384 trials
- **发散判据**（TL-20 预定义）: 系数范数 |w| > 10×初始 OR 输出幅度 |z| > 1e3
- **CMA 实现**: 块级更新（block_size=64，sat.1553 §6.3 L756 并行化因子），2×2 蝶形 + SOP 旋转

### 核心发现

**1. 发散概率由步长 μ 主导（TL-20 理论预期验证）**

| μ 范围 | P_div 特征 | 物理解释 |
|--------|-----------|---------|
| μ ≤ 1e-3 | **≈0**（61/128 组合 P_div=0） | 漂移量 ∝ μ·σ_n·√N 低于发散阈值 |
| μ = 5e-3 | **0~1.0**（取决于 f_G/tap） | 临界区，发散与衰落频率/tap 数耦合 |
| μ = 1e-2 | **多数 P_div≥0.67** | 漂移量足够大，几乎必然超阈值 |

**2. f_G（衰落频率/AFD）是第二驱动因素**
- f_G=1000Hz（τ_c=0.16ms，衰落频繁但短）→ P_div 最高（μ=1e-2 时全湍流档 P_div=1.0）
- f_G=30Hz（τ_c=5.3ms，衰落少但长）→ P_div 最低
- 物理原因：f_G 大 → 5M 符号内经历的衰落事件更多 → 发散机会更多

**3. 湍流深度影响弱（TL-22 物理前提检查通过）**
- 预期：弱湍→强湍 P_div 单调上升
- 实际：P_div=1.0 组合计数 weak=8/moderate=5/strong=7/uplink_strong=6，**不单调**
- 物理解释：深衰落 h→0 时 r≈n（纯噪声），梯度 ∇w = μ·R²·n* **与 h 深度无关**——无论 h=0.001 还是 h=0.0001，接收信号都被噪声主导。湍流深度只影响深衰落的**频率** P(h<thr)，但在 5M 符号内即使弱湍也有足够深衰落事件
- **含义**：发散条件判据应表述为 (μ, f_G, tap) 组合，而非湍流强度

**4. tap 数影响：22 tap 比 11 tap 略易发散**
- μ=5e-3 tap=22 有 7 组合 P_div≥0.67 vs tap=11 仅 4 组合
- 物理原因：更多抽头 → 更多自由度 → 噪声驱动的随机游走维度更高 → 漂移更快

### 发散条件判据（补 sat.1553 §6.3 L778 空白）

**安全区**（P_div ≈ 0）：μ ≤ 1e-3，任意湍流/f_G/tap
**临界区**（P_div 0~1）：μ ≈ 5e-3，取决于 f_G 和 tap
**危险区**（P_div ≥ 0.67）：μ ≥ 1e-2 且 f_G ≥ 100 Hz

**sat.1553 空白补全状态**：sat.1553 自认"probability of the equalizer diverging ... has not been analyzed"——本扫描首次量化了 CMA 在 GG 深衰落下发散的概率，并给出条件判据（μ, f_G, tap 组合）。
- `common._experiment` — run_* 编排 + save_results

## Step C 验证结果（2026-07-11，PASS — Go）

### MVE 配置

- **序列长度**: 500K 符号 @ 2.5 GBaud
- **试验数**: 5 seeds/场景（P_div 分辨率 0.2）
- **场景**: 5 个（危险区×2 / 临界区×2 / 安全区×1），来自 Step B 发散条件判据
- **三方对照（C7）**: CMA（传统 baseline, FR-14）/ ML（我们的方法）/ oracle MMSE（完美 CSI: h+θ, 下界）
- **ML 实现**: 8 实值 1D-CNN 蝶形（Qin 2025 L275/283）+ MSE 监督回归（非 VAE, 守增量定位）
- **SOP 速率**: 1 krad/s（sat.1553 §6.3 真实 OSL 速率, 非 Step B 的 250 krad/s）
- **公平对照（Freire 6 陷阱）**: MTRS 非 PRBS / batch≥1024 / MSE 非 CEL / 训练测试分离 / BER 非 EVM / RMpS 报告

### 核心发现

**1. ML 在 CMA 发散条件下零发散（TL-20 理论预期验证 PASS）**

| 场景 | CMA P_div | ML P_div | CMA BER | ML BER | Oracle BER |
|------|-----------|----------|---------|--------|------------|
| 危险区 μ=1e-2 f_G=1000Hz (strong) | **0.60** | **0.00** | 0.087 | 0.007 | 0.006 |
| 危险区 μ=1e-2 f_G=1000Hz (uplink) | **0.40** | **0.00** | 0.039 | 0.0006 | 0.0003 |
| 临界区 μ=5e-3 f_G=100Hz | 0.00 | 0.00 | 0.099 | 0.099 | 0.097 |
| 临界区 μ=5e-3 f_G=300Hz | **0.20** | **0.00** | 0.017 | 0.001 | 0.0009 |
| 安全区 μ=1e-3 f_G=30Hz (对照) | 0.00 | 0.00 | 0.0001 | 0.0000 | 0.0000 |

**2. ML BER 接近 oracle 下界**
- 危险区: ML BER (0.007/0.0006) ≈ oracle BER (0.006/0.0003), 远好于 CMA (0.087/0.039)
- 临界 300Hz: ML BER (0.001) ≈ oracle (0.0009), 优于 CMA (0.017)
- 安全区: ML ≈ CMA ≈ oracle ≈ 0（简单情况, 非同族性警报）

**3. C8 祖师爷警报: 未触发**
- 安全区 ML≈CMA≈oracle→ 预期（安全区是"简单情况"）
- 危险区 ML >> CMA → 差异显著, 无数学同族性

**4. ML 发散机制解释**
- CMA 逐块梯度更新: 深衰落 h→0 时 r≈n, 梯度 ∇w=μ·R²·n* 噪声驱动 → 系数随机游走 → 漂移超阈值 → 不可恢复
- ML batch 梯度下降: 梯度对整个 batch 平均 → 单个深衰落样本噪声被 batch 稀释 → 漂移 ∝ μ·σ_n/√B 远小于 CMA
- ML 前馈推理（权重固定）不在线更新 → 不会"发散"（训练后权重稳定）

### Go/No-Go 判定

**Conditional Go**（D008 修正，原 D007 全场景 Go 被压力测试修正）:
- ✅ 16QAM 场景: CMA modulus mismatch 是结构性缺陷（μ=1e-3 安全步长也 BER 差），ML 显著优 → **Go**
- ⚠️ QPSK 场景: μ=1e-3 的小步长 CMA BER≈oracle（"用小步长就行"成立）→ **方向弱**
- ✅ ML SOP 漂移: ≤20° 容忍（比 Nasr ±4° 宽），45° 需重训练
- ⚠️ 新风险: pilot 开销不对称 / 增强基线缺失(CMMA) / 方法创新性不足 / 在线vs离线不对称

### Q-CMA-FADE 两层贡献完整状态

1. ✅ **分析层（Step A+B）**: CMA 发散概率 + 条件判据（补 sat.1553 §6.3 L778 空白）
2. ✅ **方法层（Step C）**: ML 均衡器在发散条件下保持稳定（补 Qin/Nasr 实验缺口）

**增量定位（不换皮）**:
- Qin 已做: VAEMR vs CMA 收敛速度 200× + 5dB 功率预算（单一中强湍流 r₀=0.4mm）
- 我们补: 发散概率界 + 发散条件判据 + ML 在发散条件下的鲁棒性对比（新测度: P_div + 恢复时间）
- 不做: 收敛速度对比（Qin 已做过）
- 不照搬: VAE ELBO 损失（用 MSE 监督, 结构标 Qin 来源）

## R1/R4/R5 分析层验证结果（2026-07-11，⚠️ 发现重大方向风险）

### R1: 发散半解析界 — 趋势对但量级差

**推导**：drift_per_fade = μ·R²·σ_n·√(AFD/(block_size·T_S))，P_single = 2·Q(threshold/σ_drift)，P_div = 1-(1-P_single)^{N_events}，N_events=LCR·T_obs

**验证**：
- 纯 √N 律（κ=1）极保守（预测 P_div≈0），需放大系数 κ≈2043 标定
- 标定后 R²=0.27，趋势一致性=0.857（单调方向预测准确）
- μ 维度 Spearman：model(+0.81) vs data(+0.76) 高度一致
- **结论**：界适合做 μ 安全选择/趋势门控，不适合精确 P_div 预测。单 κ 无法吸收湍流相关自放大动力学

### R4: 发散 vs AFD/LCR 相关性 — ⚠️ 深衰落触发模型被反证

**相关性（128 组合）**：
| 关系 | Pearson r | p-value |
|------|-----------|---------|
| P_div ~ log₁₀μ | **+0.749** | 2.7e-24 |
| P_div ~ f_G | +0.267 | 2.3e-3 |
| P_div ~ LCR | +0.173 | 0.051 |
| P_div ~ AFD | NaN* | — |

*AFD 在 5M 符号（2ms 观测窗口）下退化为 ≈0/∞，无法有效计算

**固定 μ 后 LCR 仅在高 μ（5e-3/1e-2）弱正相关（r=+0.46~0.49），低/中 μ 无相关**

**⚠️ 深衰落触发模型直接被反证**：
- 30% 发散在序列前 10% 就发生（51% 在前 25%）——发散极早，不可能是深衰落触发
- 发散检测点 h 中位 2.52（远高于 1）——CMA 权重已放大到使输出超范围
- μ=1e-2 固定下：diverged 全序列 min_h 中位 0.070 vs non-diverged 0.035——diverged 反而经历**更浅**衰落
- 57% 发散 trial 前窗口零深衰落事件（h<0.3）

**R4 结论**：发散是高 μ 下 CMA 数值不稳定（权重随机游走累积）的结果，与触发性的深衰落事件无因果关系。sat.1553 §6.3 L778 "deep fades → local optimum" 直觉在此参数空间不成立。

**方法论注记**：前窗口比较存在不公平（diverged 前窗口短 vs 非发散全序列），但"30% 前 10% 发散"+"pre_div_min_h 中位 2.43"不依赖窗口长度，确实说明发散不需深衰落触发。需排查：5M 符号窗口太短 / Step B 用 250 krad/s SOP 可能掩盖深衰落作用 / 发散判据 threshold=10× 可能太松。

### R5: 漂移模型验证 — √n 律部分有效

**方法**：48 trials 重跑保存完整 w_norm_traj，提取 6736 fade events

**R² 结果**：
| 阈值 | n 点 | R² | Pearson r | 比例斜率 k |
|------|------|----|-----------|-----------|
| h<0.1 | 3206 | 0.552 | 0.743 | 0.246 |
| h<0.3 | 3530 | 0.505 | 0.711 | 0.267 |

- non-diverged trials R²=0.653（干净轨迹），diverged trials R²=0.240（提前截断失真）
- **结论**：√n 趋势成立（r=0.74），但模型系统性高估实测漂移 3.9×（k≈0.25）。形式对但系数需校正（块平均梯度 mean() 比逐符号小 √block_size 倍 + w 初始非零自平衡负反馈）

### 三个结果的综合含义

| 声称 | 验证结果 | 对方向的影响 |
|------|---------|-------------|
| 发散概率可半解析预测 | R² 0.27，趋势 0.86 | 可做 μ 安全选择，不可精确预测 |
| 发散由 LCR 驱动非 AFD | **推翻**——μ 主导，LCR 仅高 μ 弱相关 | sat.1553 直觉在此参数空间不成立 |
| 系数漂移服从 √n 律 | R² 0.55，r=0.74 | 形式对但系数差 4× |
| **发散由深衰落触发** | **直接反证** | **⚠️ 方向核心叙事受挑战** |

**R5 vs R4 的张力**：R5 在深衰落事件内验证了 √n 漂移（r=0.74），但 R4 发现发散本身不靠深衰落触发。两者不矛盾——深衰落期间确实有 √n 漂移，但发散可在无深衰落时由高 μ 持续随机游走达到阈值。深衰落是**加剧因素**非**必要触发条件**。

## R2/R7/R4修正 第二批结果（2026-07-11，完整证据链形成）

### R2: CMMA 发散扫描 — 多模完全不降发散

**实现**：CMMAEqualizer2x2 继承 CMAEqualizer2x2，误差函数从单模 `e=R²-|z|²` 改为多模 `e=nearest_R2-|z|²`（16QAM 三环 [0.2,1.0,1.8]）。QPSK 退化 = 标准 CMA（bit-exact 验证通过）。

**P_div 对比**：32/32 配对组合 CMMA P_div = CMA P_div **完全相同**（0 差异）。发散时序几乎相同（div_idx 比值中位 1.025）。

**结论**：多模修复了星座失配，但**完全修不好高 μ 发散**。证实发散是 μ 驱动的数值不稳定结构性问题，而非单模 R² mismatch 引起。

### R7: 被动冻结 — 完全无效（ΔP_div=0 全 24 组合）

**实现**：CMAEqualizer2x2WithFreeze，h<threshold 时跳过梯度更新（只滤波）。

**实验 A**：24 组合 ΔP_div = 0.00——冻结零效果。即使冻结 59% 的块，P_div 仍不变。

**实验 B（SOP 代价）**：冻结 15.4% 的块，SOP 累计漂移 **1774°/trial**（不跟踪 SOP 导致巨大偏差）。

**实验 C（threshold 敏感性）**：P_div 不随 threshold 单调下降，即使冻结 53% 的块 P_div 仍 0.33。无 threshold 能消除发散。

**结论**：冻结完全无效——发散在 h 高时由随机游走累积突破阈值，冻结只在 h<thr 时停梯度，**打错了靶**。sat.1553 [79] Matsuda 2020"停 CMA 更新"直觉被证伪。

### R4 修正：原结论基本成立，LCR 作用被低估

**修正参数**：SOP_RATE 4e-7（1 krad/s, 真实值）+ N_SYMBOLS 10M（4ms, 原 5M=2ms）

**相关性对比**：
| 指标 | 修正(1krad/s,10M) | 原始(250krad/s,5M) |
|---|---|---|
| P_div vs μ | +0.697 | +0.749 |
| P_div vs LCR | **+0.420** | +0.173 |
| P_div vs f_G | +0.441 | +0.267 |

固定 μ=1e-3 时 P_div vs LCR 达 **r=+0.876**——LCR 是真实次级驱动。

**早发散比例（<10%）= 30%** 不变。Mann-Whitney p=0.9998（深衰落触发仍被拒）。AFD 10M 下可计算。

**结论**：μ 主导结论稳健（非 SOP 伪影），深衰落触发仍不成立，但 250 krad/s 掩盖了 LCR 的真实作用（+0.17→+0.42）。

### 完整证据链

| 实验 | 结果 | 裁决 |
|------|------|------|
| R2 CMMA | P_div 与 CMA 逐点相同 | 多模不降发散 → 非模失配引起 |
| R7 冻结 | ΔP_div=0 全 24 组合 | 停深衰落更新不防发散 → 非深衰落触发 |
| R4 修正 | μ 仍主导(r=0.70)，早发散 30% 不变 | 非 SOP 伪影 → R4 原结论成立 |
| R4 修正 | LCR +0.42，固定 μ 后 +0.88 | LCR 是真实次级驱动 |

**发散 = 高 μ 数值不稳定（主因，r=0.70）+ 衰落频率 LCR（次因，r=0.42，固定 μ 后 r=0.88）。深衰落是加剧因素非必要触发条件。所有基于"停深衰落更新"的缓解策略（冻结/CMMA）全部失效。**

## LCR 机制 + BER 影响验证（2026-07-12，方法层重新定位）

### LCR 机制：H1/H2 都不成立 — LCR 是伪相关

**TL-20 假设**：H1（重收敛累积：发散集中在恢复沿后）/ H2（边沿梯度突变：发散在跳变点触发）

**结果**：发散 **100% 发生在正常区**（h>thr 且远离衰落事件）。距最近 up-cross 中位 2530 block（25 万符号），<100 block 占 **0%**。H1 和 H2 都被拒绝。

**剂量-效应**：P_div vs LCR r=+0.96（p=0.002），单调递增。但这是**伪相关**——LCR 是"信道动力学快慢"的代理变量（高 f_G → 短 τ_c → 块间 h 波动大 → CMA 梯度方差大 → 数值不稳定），不是事件触发。

### BER 影响方法层重新定位 — ⚠️ 真价值出现

**CMA 跟踪滞后惩罚**：即使安全 μ=1e-3（几乎不发散），CMA BER 仍比 oracle 差 **2.9-2266×**。LCR 对 BER 有独立影响——不通过发散，而是通过在线更新的跟踪滞后。

**ML vs CMA vs Oracle 三方对比**（QPSK, strong, μ=1e-3, 6 f_G）：

| f_G (Hz) | CMA | ML | Oracle | ML/CMA 优势 |
|----------|-----|-----|--------|------------|
| 10 | 0.096 | **0.029** | 0.008 | 3.3× |
| 30 | 0.048 | **0.0003** | 0.0000 | 160× |
| 100 | 0.122 | **0.018** | 0.0003 | 6.8× |
| 300 | 0.091 | **0.009** | 0.0000 | 10× |
| 1000 | 0.152 | **0.094** | 0.053 | 1.6× |
| 3000 | 0.082 | **0.011** | 0.0025 | 7.5× |

**ML 在所有 6 个 f_G 都优于 CMA**（1.6-160×），2 个 f_G 达到/接近 oracle。

### 方法层重新定位

**原定位（已否证）**："ML 不发散 → 深衰落鲁棒性"——因果链断，ML 不发散是 trivial 前馈性质

**新定位（本轮发现）**："ML 避免 CMA 跟踪滞后惩罚"——CMA 在线更新在高 LCR 下 BER 恶化（2.9-2266× oracle），ML 固定权重无此惩罚。**非 trivial**——ML 离线训练学到信道统计，推理时无跟踪滞后。

## 下一步

1. ~~进 Step 4a 维度 D：先建 GG 时间域衰落模型（FR-20）~~ ✅ **Step A 完成（2026-07-11）**
2. ~~Step B：CMA 发散概率扫描（分析层）~~ ✅ **Step B 完成（2026-07-11）**
3. ~~Step C：ML 均衡器 MVE（方法层）~~ ✅ **Step C 完成（2026-07-11）** + 压力测试修正为 **Conditional Go (D008)**
4. ~~R1/R4/R5 分析层验证~~ ✅ **完成（2026-07-11）** — R4 反证深衰落触发，方向核心叙事受挑战
5. ~~第二批 R2/R7 执行~~ ✅ **完成（2026-07-11）** — CMMA 不降发散，冻结完全无效，R4修正确认 μ 主导+LCR 次级
6. **用户选 B，方法层重新定位完成**（S009）：
   - LCR 机制：H1/H2 都不成立，LCR 是伪相关（代理变量）
   - BER 影响：CMA 跟踪滞后惩罚（安全 μ 仍差 oracle 2.9-2266×），ML 全 f_G 优势（1.6-160×）
   - 方法层定位："ML 避免 CMA 跟踪滞后惩罚"（非 trivial）
   - 下一步：R10 补盲 VQ-VAE 做公平盲 vs 盲对比，或直接进 Contract
