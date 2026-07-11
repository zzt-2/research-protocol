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
| (待建) cma_divergence_scan.py | CMA 发散概率 vs 衰落深度扫描 | 待建 (Step B) | results/cma-fade-divergence/ |
| (待建) mve_cma_vs_ml.py | CMA vs ML 均衡深衰落对比 | 待建 (Step C) | results/cma-fade-divergence/ |

## 参数溯源（FR-20）

关键物理参数（已补全，标文献来源）：

| 参数 | 值 | 来源 | 备注 |
|------|-----|------|------|
| GG 信道 (α,β) | weak(4,3)/mod(2.5,1.8)/strong(1.5,0.8) | params.py TurbulenceParams | F32/F33 |
| Greenwood 频率 f_G | 30-1000 Hz 扫描 | Greenwood 1977 + arxiv 2208.00836:51 | F33b, 守 C1 扫描 |
| 强度闪烁相干时间 τ_c | 0.16-5.3 ms (=1/(2πf_G)) | Conan 1995 JOSA A 12(7):1559 | F33b |
| 横风速度 v | 10 m/s 典型 | photonics10121312:566 | Bufton 模型 |
| Cn² 地面值 | 1e-15~1e-13 m⁻²ᐟ³ | photonics10121312:560 | H-V 剖面 |
| 强度功率谱滚降 | f⁻¹¹ᐟ³ | Tatarskii 1971 / Clifford 1971 | F24/F25 已覆盖 |
| AR(1) 块间相关 ρ | exp(-block·t_s/τ_c) | F3.28/F3.29 既有 | 实现见 _gg_time.py |

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
- `common._equalizer` — MMSE 均衡（CMA 需在 Step B 新建 `_cma.py`）
- `common._modulation` — QPSK/16QAM + ber_eval
- `common._experiment` — run_* 编排 + save_results

## 下一步

1. ~~进 Step 4a 维度 D：先建 GG 时间域衰落模型（FR-20）~~ ✅ **Step A 完成（2026-07-11）**
2. **Step B：CMA 发散概率扫描**（分析层）—— 需先扩 CMA 均衡器到 `common/_cma.py`
3. Step C：ML 均衡器 MVE（方法层，vs CMA）—— 开新对话
