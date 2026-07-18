# V-13: 级联灵敏度 PASS 标准的合理性审查

> 2026-05-31 | phase1-research | ch3-cascade
> 审查 sim_cascade_robustness.py 中 PASS 条件的物理依据和合理性

---

## 1. 测试场景识别

### 1.1 Exp1 的 6 个场景

代码 `run_exp1()` (L207-229) 构造 6 个场景 = 3 湍流 x 2 多普勒条件：

```python
scenarios = [(t, e, fd) for t in ['weak','moderate','strong']
                          for e, fd in [('low',DOPPLER_HIGH),('high',DOPPLER_LOW)]]
```

| # | 场景标签 | 湍流 (α,β) | 仰角 | 多普勒率 | 物理含义 |
|---|---------|-----------|------|---------|---------|
| 1 | weak_low | 弱 (4.0, 3.0) | low | 150 MHz/s | 夜间低仰角 LEO 过境 |
| 2 | weak_high | 弱 (4.0, 3.0) | high | 30 MHz/s | 夜间高仰角 LEO 过境 |
| 3 | moderate_low | 中 (2.5, 1.8) | low | 150 MHz/s | 白天低仰角 LEO 过境 |
| 4 | moderate_high | 中 (2.5, 1.8) | high | 30 MHz/s | 白天高仰角 LEO 过境 |
| 5 | strong_low | 强 (1.5, 0.8) | low | 150 MHz/s | 恶劣天气低仰角 LEO 过境 |
| 6 | strong_high | 强 (1.5, 0.8) | high | 30 MHz/s | 恶劣天气高仰角 LEO 过境 |

每个场景测试 **固定 DPLL vs 自适应 DPLL**，比较 BER 增益。

### 1.2 Exp2 的场景（辅助）

Exp2 测试 Ch4 预补偿鲁棒性（AR 预测），但 H006 判定标准仅依赖 Exp1。Exp2 作为辅助证据，不参与 PASS/FAIL 判定。

---

## 2. PASS 条件详解

### 2.1 单场景级 PASS 条件

代码 L224：

```python
st = "PASS" if gain > 0.5 else ("WEAK" if gain > 0 else "NEG")
```

| 判定 | 条件 | 含义 |
|------|------|------|
| PASS | gain > 0.5 dB | 自适应方案 BER 显著低于固定方案 |
| WEAK | 0 < gain <= 0.5 dB | 自适应略优但工程意义不足 |
| NEG | gain <= 0 dB | 自适应不如固定（含两种 BER 相近的情况） |

其中 `gain = 10*log10(BER_fixed / BER_adaptive)` (L223)。

### 2.2 H006 全局判定标准

代码 `print_verdict()` (L355-374)，**固定在 SNR=20dB**：

| 等级 | 条件 | 含义 |
|------|------|------|
| Strong PASS | >= 4/6 PASS at NMSE=-10dB | 中等估计噪声下仍有效 |
| PASS | >= 4/6 PASS at NMSE=-15dB | 高质量估计下有效 |
| WEAK PASS | 2-3/6 PASS at NMSE=-15dB | 部分场景有效 |
| FAIL | 0-1/6 PASS at NMSE=-15dB | 方案不可行 |

### 2.3 Ch4 辅助判定

代码 L377-382：Ch4 在 NMSE=-10dB、N=500 采样时，预补偿增益 > 0.5 dB 则 PASS。这是独立判定，不参与 H006 总判定。

---

## 3. PASS 条件的物理依据审查

### 3.1 0.5 dB 阈值的合理性

**审查结论：基本合理，但存在宽松偏向。**

**支持 0.5 dB 合理性的论据：**

1. **工程意义**：0.5 dB SNR 增益等效于发射功率提升约 12%。在卫星激光通信链路预算中（典型链路余量 3-6 dB），0.5 dB 是可感知的改善。
2. **通信领域惯例**：无线通信文献中，调制/编码方案切换通常以 0.5 dB 为最小有意义差异（3GPP RAN1 实践）。
3. **测量精度**：典型 BER 测试在 10^-4 量级需要 ~10^5 符号才能区分 0.5 dB 差异，本仿真 Ns=2000 x 15 trials = 30000 符号，勉强够用。

**宽松偏向的证据：**

1. **弱湍流场景增益天花板低**：V-11 理论预测弱湍流自适应增益 0.5-1.5 dB（NMSE=-10dB）。当增益本身只有 0.5-1.5 dB 时，PASS 阈值设在 0.5 dB 意味着几乎所有非退化情况都能 PASS——区分力不足。
2. **15 trials 的统计置信度**：Ns=2000 符号/trial, BER 在 10^-4 量级时单 trial 约有 0.04 个错误比特——几乎所有 trial 都是 0 错误。此时 BER 估计实质上由少数非零 trial 主导，统计方差极大。gain > 0.5 dB 的判定在统计上不稳健。

**量化评估：**

- 在 BER ~0.015%（弱湍流 SNR=20dB）时，2000 符号中期望错误数 = 0.3 个。15 trials 总期望错误数 ~4.5 个。区分 0.5 dB 增益（~12% BER 差异）需要至少 ~30 个错误事件才达到 95% 置信度（二项分布正态近似）。**4.5 << 30，统计功效不足。**
- 在 BER ~1.9%（强湍流 SNR=20dB）时，2000 符号中期望错误数 = 38 个。15 trials 总期望 ~570 个。**统计功效充足。**

**结论：0.5 dB 阈值对强湍流场景有良好区分力，对弱湍流场景统计功效不足，容易出现假 PASS 或假 NEG。**

### 3.2 "4/6 at NMSE=-10dB" 标准的合理性

**审查结论：标准本身合理，但与底层 VV 公式 bug 存在交互影响。**

**合理的方面：**

1. 要求 4/6 而非 6/6，容许 2 个场景 FAIL——这覆盖了最困难的情况（如弱湍流低多普勒，自适应优势最小）。
2. 分层判定（Strong/PASS/WEAK/FAIL）提供渐进式结论，避免二元判断的信息丢失。
3. NMSE=-10dB 对应 ε 标准差 ~0.32（V-11 表 1.5），是"中等质量估计器"的典型值，具有工程实际意义。

**潜在问题：**

1. **SNR=20dB 单点**：H006 判定仅在 SNR=20dB。但代码实际运行了 SNR=15/20/25 dB（`run_exp1` L207），仅用 20dB 判定。如果自适应方案在 15dB 或 25dB 有不同表现，单点判定可能不够稳健。
2. **多普勒参数交叉**：`low` 对应 `DOPPLER_HIGH=150MHz/s`，`high` 对应 `DOPPLER_LOW=30MHz/s`。命名反直觉但代码正确（低仰角=大多普勒率）。这不影响判定但增加阅读混淆风险。

### 3.3 各场景预期 PASS/FAIL 的合理性

基于 V-11 理论模型（h 对消机制）和 SPEC.md §6.1 已验证数据：

| 场景 | NMSE=-20dB | NMSE=-15dB | NMSE=-10dB | NMSE=-5dB | 物理分析 |
|------|-----------|-----------|-----------|-----------|---------|
| weak_low | PASS (0.5-1dB) | PASS (0.5-1dB) | 边界 (0.3-0.8dB) | NEG | h 方差小，自适应优势有限；大多普勒给 DPLL 带来挑战 |
| weak_high | 边界 | WEAK | NEG | NEG | h 方差小 + 小多普勒，固定 DPLL 已近最优 |
| moderate_low | PASS (1-2dB) | PASS (1-2dB) | PASS (0.5-1.5dB) | 边界 | 中等 h 方差 + 大多普勒，自适应开始有明确优势 |
| moderate_high | PASS (0.5-1.5dB) | PASS (0.5-1dB) | 边界 | NEG | 中等 h 方差但小多普勒 |
| strong_low | PASS (2-4dB) | PASS (1.5-3dB) | PASS (1.5-3dB) | PASS (0.5-2dB) | 大 h 方差 + 大多普勒，自适应优势最大 |
| strong_high | PASS (2-4dB) | PASS (1.5-3dB) | PASS (1-2.5dB) | 边界 | 大 h 方差但小多普勒，优势略减 |

**H006 判定预测**：
- NMSE=-10dB: strong_low + strong_high + moderate_low + moderate_high = 4/6 PASS → **Strong PASS**
- 弱湍流两个场景在 NMSE=-10dB 可能不 PASS，但恰好被 4/6 标准容错

**合理性评估**：4/6 标准与理论预测一致——弱湍流是自适应方案的天花板场景（增益本来就小），4/6 允许这 2 个场景不 PASS。**这个标准的设计意图是验证"自适应在它应该有效的场景中确实有效"，而非"自适应在所有场景都有效"，逻辑自洽。**

---

## 4. VV 公式 Bug 对 PASS 结论的影响

### 4.1 Bug 位置

`sim_cascade_robustness.py` L138：

```python
pe = np.unwrap(np.angle(avg)*4)/4  # 公式 B（错误）
```

正确公式应为 `np.unwrap(np.angle(avg))/4`（公式 A）。

### 4.2 影响机制

Bug 影响载波恢复链中的 VV-CPR 步骤（`vv_cpr` 函数，被 `carrier_recovery` L152 调用）。

**关键问题：bug 影响 PASS 判定的方向是什么？**

1. **固定方案和自适应方案都经过 `carrier_recovery`**，都使用同一个有 bug 的 VV。
2. **PASS 判定基于 gain = BER_fixed / BER_adaptive**，即两种方案的 BER 比值。
3. 如果 bug 对两种方案的影响是对称的（同等恶化），则 gain 不变，PASS 判定不受影响。
4. 如果 bug 对两种方案的影响是不对称的，则 gain 会偏移。

### 4.3 不对称性分析

Bug 的 BER 影响与 **输入信号的残余相位漂移** 有关（V-12 量化验证）：
- 公式 B 在 FOE+VV only 下 BER 膨胀 1800x（弱湍流）
- 公式 B 在 FOE+DPLL+VV 下 BER 膨胀 1.3-20x

**但这里的 VV 不是独立工作——它在 DPLL 之后**（代码 L151-152）：

```python
rx_p, _ = dpll_track(rx_c, omega_n, FIXED_CFG['zeta'])  # DPLL first
rx_v, _ = vv_cpr(rx_p, FIXED_CFG['M_vv'])                # VV after DPLL
```

DPLL 吸收了大部分相位漂移后，VV 面对的残余相位变化小。根据 V-12 §3.3，完整链路（FOE+DPLL+VV）下公式 B 导致弱湍流 BER 20x 膨胀、强湍流 1.3x 膨胀。

**不对称性来源**：自适应方案使用 `omega_n = clip(B0*h_est, ...)`，固定方案使用 `omega_n = 8e6`。不同 omega_n 导致 DPLL 输出残余相位不同，进而 VV 面对的信号不同。

**具体影响方向**：
- **固定方案**（omega_n=8e6，非最优）：DPLL 残余相位较大 → VV 面对更多漂移 → 公式 B 偏差更大 → 固定方案 BER 被额外抬高
- **自适应方案**（omega_n 匹配信道）：DPLL 残余相位较小 → VV 面对更少漂移 → 公式 B 偏差更小 → 自适应方案 BER 影响更小

**结论：VV 公式 bug 倾向于抬高固定方案的 BER（相对于自适应方案），导致 gain 虚高，使 PASS 更容易获得。**

### 4.4 影响量级估计

V-12 表明完整链路下公式 B 对弱湍流 BER 膨胀 20x。但这 20x 是在"oracle omega_n"条件下。在 cascade 仿真中：

- 固定方案 omega_n=8e6（偏高），DPLL 残余相位 std 较大
- 自适应方案 omega_n 与信道匹配，DPLL 残余相位 std 较小

保守估计：公式 B 对固定方案的 BER 恶化因子约 1.5-5x（弱湍流），对自适应方案约 1.2-2x（弱湍流）。gain 虚高约 0.5-1.5 dB。

**对 H006 判定的影响**：
- 强湍流场景（自适应增益 2-4 dB）：bug 影响不足以改变 PASS/FAIL
- 中等湍流场景（增益 1-2 dB）：bug 可能使边界 case（本应 WEAK）变成 PASS
- 弱湍流场景（增益 0.3-1 dB）：bug 可能使本应 NEG 的变成 PASS

**最终结论：H006 的 Strong PASS（4/6 at NMSE=-10dB）可能因 VV bug 而多出 0-1 个 PASS 场景。如果修正 VV，预期结果可能是 3/6（WEAK PASS）或 4/6（PASS），而非 Strong PASS。判定等级可能需要下调一级。**

---

## 5. 量化锚点

### 锚点 1：弱湍流场景的统计功效缺口

- **条件**：weak_low, NMSE=-10dB, SNR=20dB
- BER ~0.018%（V-11 预测），Ns=2000 x 15 trials = 30000 符号
- 期望总错误数 = 30000 x 0.00018 = 5.4 个
- 区分 0.5 dB（12% BER 差异）所需错误数 ~30（二项分布 95% CI）
- **统计功效 < 20%**——判定结果基本是噪声驱动

### 锚点 2：强湍流场景的 PASS 稳健性

- **条件**：strong_low, NMSE=-10dB, SNR=20dB
- BER ~2.5%（V-11 预测），期望总错误数 = 30000 x 0.025 = 750 个
- 0.5 dB 对应 ~12% BER 差异，即 ~90 个错误差异
- **统计功效 > 99%**——PASS/FAIL 判定高度可靠
- 理论增益 1.5-3 dB 远超 0.5 dB 阈值，判定不敏感于 VV bug

### 锚点 3：VV bug 对 gain 的偏移量

- **条件**：弱湍流, SNR=20dB, 完整 FOE+DPLL+VV 链路
- 公式 B 对固定方案 BER 恶化 ~20x（V-12 §3.3），对自适应方案恶化 ~5x（估计，因 omega_n 更优）
- 假设真实 BER_fixed = 0.016%, BER_adaptive = 0.015%，真实 gain = 0.28 dB (NEG)
- bug 后 BER_fixed ≈ 0.32%, BER_adaptive ≈ 0.075%，bug gain = 10*log10(0.32/0.075) = 6.3 dB (PASS)
- **gain 偏移量约 6 dB，足以将 NEG 变为 PASS**
- 强湍流：公式 B 影响 1.3x（V-12），gain 偏移 < 0.5 dB，不改变判定

### 锚点 4：4/6 标准与理论预测的对齐度

- 理论预测 NMSE=-10dB 下 PASS 场景：strong_low, strong_high, moderate_low, moderate_high = 4 个
- 弱湍流 2 个场景理论预测边界或 NEG
- **4/6 标准精确匹配理论预测的 PASS 数量**，设计意图合理
- 但需注意：如果弱湍流某个场景因 VV bug 意外 PASS（变成 5/6），Strong PASS 仍然成立，只是虚高

---

## 6. 综合评估

### 6.1 各 PASS 条件合理性汇总

| 审查维度 | 评级 | 说明 |
|---------|------|------|
| 0.5 dB 阈值工程意义 | **合理** | 等效 12% 功率提升，通信领域有先例 |
| 0.5 dB 阈值统计可区分性 | **弱湍流不足，强湍流充分** | 需 Ns 增至 10000 或 trial 增至 50 |
| 4/6 场景计数 | **合理** | 与理论预测对齐，容错设计得当 |
| 分层判定（Strong/PASS/WEAK/FAIL） | **合理** | 提供渐进式结论 |
| SNR=20dB 单点 | **偏弱** | 应至少包含 15dB 和 25dB 验证 |
| Exp2 辅助判定（Ch4） | **偏弱** | NMSE=-10dB N=500 单点，不参与主判定 |
| VV 公式 bug 影响 | **重大** | 弱湍流 gain 可能虚高 1-6 dB，影响 H006 等级 |

### 6.2 核心发现

1. **PASS 条件设计逻辑自洽**：4/6 标准与 h 对消理论预测一致，分层判定有工程意义。
2. **弱湍流场景统计功效严重不足**：0.5 dB 阈值在 BER ~10^-4 量级下无法可靠区分，判定结果受噪声驱动。
3. **VV 公式 bug 是最严重问题**：公式 B 倾向于抬高固定方案 BER（不对称影响），使 PASS 更容易获得。H006 判定可能虚高一级（Strong PASS → PASS 或 PASS → WEAK PASS）。
4. **修正 VV 后的预期**：强湍流 2 个场景 PASS 稳定（增益 1.5-3 dB 远超阈值），中等湍流 2 个场景大概率 PASS，弱湍流 2 个场景大概率不 PASS。修正后预期 4/6 PASS at NMSE=-10dB（与 H006 PASS 等级一致，但可能不再是 Strong PASS）。

### 6.3 建议行动

1. **修正 VV 公式**：L138 改为 `np.unwrap(np.angle(avg))/4`，然后重新运行。
2. **增大弱湍流场景的统计量**：Ns 从 2000 增至 10000，或 trials 从 15 增至 50。
3. **补充 SNR=15dB 判定**：验证 PASS 结论在低 SNR 下是否稳健。
4. **记录 VV bug 修正前后的对比**：量化 bug 对 H006 判定的实际影响。

---

## 7. 对论文结论的影响

| 结论 | 当前状态 | VV 修正后预期 |
|------|---------|-------------|
| 自适应 DPLL 在 NMSE=-10dB 下 Strong PASS | H006 声称（可能因 bug 虚高） | 降为 PASS（4/6）或维持 Strong PASS |
| 自适应 DPLL 在 NMSE=-15dB 下 PASS | 依赖 VV bug 抬高 fixed 基线 | 可能降为 WEAK PASS |
| 强湍流自适应优势 1.5-3 dB | **不受影响**（bug 影响小） | 维持 |
| 弱湍流自适应优势 0.5-1 dB | **可能虚高** | 可能降至 0-0.5 dB（NEG/WEAK） |

**关键风险**：论文如果基于 VV bug 版本的仿真声称"自适应 DPLL 在所有湍流条件下有效"，修正后需要限缩为"中等及强湍流有效，弱湍流增益有限"。
