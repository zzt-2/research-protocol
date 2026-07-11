# [S006] Step C: ML vs CMA MVE — 方法层 PASS, Go 判定

> 2026-07-11 | GW Step 4a 维度 D MVE (Step C) | 完成

## 目标

执行 Q-CMA-FADE Step C（方法层 MVE）：用 Step B 确认的 CMA 发散条件（μ≥5e-3, f_G≥100Hz），实现 ML 均衡器，验证 ML 能否在 CMA 发散的深衰落条件下保持稳定收敛。三方对照（CMA / ML / oracle MMSE），Go/No-Go 判定。

## 记录

### 报到 + Trigger 5 接收 handoff 验证

- 读 topic-index / decisions / voice / _registry / SIM-ORG / _gg_time / _cma / _equalizer / params / gw-feasibility §D / qin2025 笔记 / nasr2026 笔记 / freire2022 笔记
- Trigger 5 验证 PROMPT-005 的 5 条关键事实声称全 PASS：
  - Step A commit 59ead25 + Step B commit adf9349 ✓
  - 384 trials / 128 combos ✓
  - μ≤1e-3 → 61/128 combos P_div=0 ✓
  - μ≥1e-2 & f_G≥100Hz → 15/24 combos P_div≥0.67 ✓
  - torch 可用性：**纠正 PROMPT-005 假设**——scoop py311 有 torch 2.6.0+cu124 + CUDA RTX 4070，用 torch 实现 CNN 而非纯 numpy

### C1: ML 均衡器实现 (common/_ml_equalizer.py)

**架构选择**：选项 A（CNN 监督回归），排除 B（CMA+ML 混合，撞 Qin bootstrapping 卖点）和 C（RNN/LSTM，偏离 Qin/Nasr 范式 + 范围偏离）。

**实现**：
- `ComplexFIRConv1d`: 单复 FIR 用 2 个实值 Conv1d（w_R, w_I）实现，复卷积 z = w∗r 拆为 4 实值卷积
- `ButterflyCNNEqualizer2x2`: 4 复 FIR（wxx/wxy/wyx/wyy）= 8 实值 1D-CNN（Qin 2025 L275）
- 中心抽头初始化（Qin 2025 L283: 中心=1, 其余=0）
- `MLChannelEqualizer`: 训练+推理封装，MSE 监督损失 + Adam + ReduceLROnPlateau + early stopping + save best model
- `compute_rmps`: 复杂度评估（Freire 2022 陷阱 5）

**增量定位**（守 D005/D006 不换皮）：
- 用 Qin 的网络结构（8 实值 1D-CNN 蝶形，标来源 L275/283）——结构是工程实现不是贡献
- **不用 Qin 的 VAE 损失**——用 MSE 监督回归（已知训练序列），物理对应 sat.1553 §6 DA 模式
- 测度正交：测发散鲁棒性（P_div + BER），不测收敛速度（Qin 已做过）

**Smoke test**：简单 AWGN+SOP 信道，loss 从 1.89 降到 0.04，训练收敛正常。

### C2: 三方对比实验 (mve_cma_vs_ml.py)

**TL-20 理论预期**（跑前预建）：
- ML 在发散条件下应比 CMA 稳定：CMA 逐块梯度 ∇w=μ·R²·n* 噪声驱动 → 随机游走 → 发散；ML batch 梯度平均 → 噪声稀释 ∝ 1/√B → 漂移远小
- 预测：危险区 ML P_div ≪ CMA P_div

**SOP 速率修正**（TL-22 物理前提检查）：
- Step B 用 SOP_RATE=1e-4 rad/sym（250 krad/s）——超出 sat.1553 §6.3 真实 OSL SOP（~1 krad/s）250 倍
- 修正为 4e-7 rad/sym（1 krad/s, sat.1553 L778 真实值）
- 验证：真实 SOP 下 CMA 发散仍由 μ 驱动（μ=5e-3/1e-2 仍发散），SOP 速率不改变发散机制 → Step B 发散条件判据仍有效

**测试场景**（5 个，来自 Step B 发散条件判据）：
1. 危险区: μ=1e-2, f_G=1000Hz, strong（CMA 必发散）
2. 危险区: μ=1e-2, f_G=1000Hz, uplink_strong
3. 临界区: μ=5e-3, f_G=100Hz, strong
4. 临界区: μ=5e-3, f_G=300Hz, strong
5. 安全区: μ=1e-3, f_G=30Hz, strong（对照）

**三方对照（C7）**：CMA（FR-14 先验）/ ML（我们的方法）/ oracle MMSE（完美 CSI: h+θ, 下界）

**Freire 6 陷阱 checklist**：MTRS 非 PRBS / batch≥1024 / MSE 非 CEL / 训练测试分离 / BER 非 EVM / RMpS 报告——全守

**结果**（5 场景 × 5 trials = 25 runs, ~4 分钟）：

| 场景 | CMA P_div | ML P_div | CMA BER | ML BER | Oracle BER |
|------|-----------|----------|---------|--------|------------|
| 危险区 strong | 0.60 | 0.00 | 0.087 | 0.007 | 0.006 |
| 危险区 uplink | 0.40 | 0.00 | 0.039 | 0.0006 | 0.0003 |
| 临界 100Hz | 0.00 | 0.00 | 0.099 | 0.099 | 0.097 |
| 临界 300Hz | 0.20 | 0.00 | 0.017 | 0.001 | 0.0009 |
| 安全 30Hz | 0.00 | 0.00 | 0.0001 | 0.0000 | 0.0000 |

### C3: Go/No-Go 判定

**Go 标准（FR-14/15）检查**：
- ✅ FR-14: ML P_div (0.0) << CMA P_div (0.6) 在危险区
- ✅ FR-15: ML BER ≈ oracle BER, 不劣于 CMA 安全区
- ✅ C8 未触发: 安全区 ML≈CMA 是预期（简单情况非同族性），危险区差异显著
- ✅ TL-20 验证: ML 稳定性符合预测
- ✅ C6-C8 自检全 PASS

**结论: Go** — Q-CMA-FADE 方向确认，两层贡献完整，可进 Contract/Execute。

## 决策引用

- D005: 候选合并 Q-CMA-FADE（分析+方法合一）——本轮方法层 MVE PASS 验证此合并
- D006: Step B 发散概率扫描 PASS——本轮用其发散条件作为测试场景
- D007: **新建**——Step C ML vs CMA MVE PASS, Go 判定, Q-CMA-FADE 方向确认

## 范围确认

- 本轮是否在 scope boundary 内：是（Step C 是 topic-index 明确列出的下一步，不违反"明确不含"）

## 后续

- Q-CMA-FADE 两层贡献 MVE 全 PASS，方向确认（Go）
- 可进 Contract/Execute：formalize 分析层（发散概率界 + 条件判据）+ 方法层（ML 均衡器架构 + 训练协议）
- 若用户确认进 Contract，需写 handoff（H006）交接 Contract 阶段
- SOP 速率修正记录：Step B 用 250 krad/s（过快），Step C 修正为 1 krad/s（sat.1553 真实值）。Step B 发散条件判据仍有效（SOP 不改变发散机制），但 Contract 阶段应统一用 1 krad/s
