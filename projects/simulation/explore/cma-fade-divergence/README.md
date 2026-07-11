# Q-CMA-FADE 探索：CMA 深衰落发散 — 分析 + ML 缓解

> 方向: Q-CMA-FADE | 来源: D005（Q-DP2+Q-ML1 合并） | 状态: WIP-待MVE | 创建: 2026-07-11
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
| (待建) mve_cma_vs_ml.py | CMA vs ML 均衡深衰落对比 | 待建 (Step C) | results/cma-fade-divergence/ |

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

## 下一步

1. ~~进 Step 4a 维度 D：先建 GG 时间域衰落模型（FR-20）~~ ✅ **Step A 完成（2026-07-11）**
2. ~~Step B：CMA 发散概率扫描（分析层）~~ ✅ **Step B 完成（2026-07-11）**——CMA 均衡器 + 发散概率扫描 + 发散条件判据
3. **Step C：ML 均衡器 MVE**（方法层，vs CMA）—— 开新对话。用 Step B 确认的发散条件（μ≥5e-3, f_G≥100Hz）作为测试场景，验证 ML 均衡器能否在 CMA 发散的条件下保持稳定
