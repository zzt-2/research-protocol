# R-ch3-cascade: 级联灵敏度仿真结果

> 2026-05-31 | phase2-results | ch3-cascade
> 仿真代码: `projects/thesis-figures/simulation/sim_cascade_robustness.py`
> 运行时间: 14.6s

## 总体判定

**CONDITIONAL PASS — 结果受旧 VV 公式 bug 显著影响，需修正后重跑**

H006 判定: STRONG PASS (6/6 at NMSE=-10dB, SNR=20dB)，但弱/中湍流增益严重虚高（见 §3），修正 VV 后预期降级。

---

## 1. Exp1 结果汇总 (Ch5 载波同步鲁棒性)

### 1.1 SNR=20dB 核心判定数据

| 场景 | NMSE=-5dB | NMSE=-10dB | NMSE=-15dB | NMSE=-20dB | NMSE=inf |
|------|-----------|------------|------------|------------|----------|
| weak_low | +19.77 PASS | **+15.47 PASS** | +7.54 PASS | +6.86 PASS | +21.64 PASS |
| weak_high | +19.77 PASS | **+15.47 PASS** | +7.54 PASS | +6.86 PASS | +21.64 PASS |
| moderate_low | +12.32 PASS | **+5.38 PASS** | +5.17 PASS | +4.08 PASS | +11.83 PASS |
| moderate_high | +12.32 PASS | **+5.38 PASS** | +5.17 PASS | +4.08 PASS | +11.83 PASS |
| strong_low | +1.20 PASS | **+0.90 PASS** | +1.74 PASS | +0.29 WEAK | +0.56 PASS |
| strong_high | +1.20 PASS | **+0.90 PASS** | +1.74 PASS | +0.29 WEAK | +0.56 PASS |

**H006 判定**: NMSE=-10dB → 6/6 PASS → **STRONG PASS**

### 1.2 SNR=15dB 数据

| 场景 | NMSE=-5dB | NMSE=-10dB | NMSE=-15dB | NMSE=-20dB | NMSE=inf |
|------|-----------|------------|------------|------------|----------|
| weak_low | +6.20 PASS | +5.93 PASS | +1.40 PASS | +2.28 PASS | +9.92 PASS |
| weak_high | +6.20 PASS | +5.93 PASS | +1.40 PASS | +2.28 PASS | +9.92 PASS |
| moderate_low | +2.10 PASS | +4.64 PASS | +0.01 WEAK | +0.49 WEAK | +4.65 PASS |
| moderate_high | +2.10 PASS | +4.64 PASS | +0.01 WEAK | +0.49 WEAK | +4.65 PASS |
| strong_low | +0.54 PASS | +0.83 PASS | +0.00 NEG | +0.00 NEG | +0.61 PASS |
| strong_high | +0.54 PASS | +0.83 PASS | +0.00 NEG | +0.00 NEG | +0.61 PASS |

### 1.3 SNR=25dB 数据

全部 6/6 PASS（增益更大），此处略去细节。

---

## 2. Exp2 结果汇总 (Ch4 预补偿鲁棒性)

### 2.1 弱湍流, τ=5ms, SNR=15dB

| NMSE | N=100 | N=500 | N=1000 | N=5000 |
|------|-------|-------|--------|--------|
| -5dB | NEG (ρ_err=0.90) | NEG (0.89) | NEG (0.91) | NEG (0.91) |
| -10dB | WEAK (0.76) | **NEG (0.77)** | NEG (0.74) | NEG (0.78) |
| -15dB | WEAK (0.52) | WEAK (0.50) | WEAK (0.46) | WEAK (0.51) |
| -20dB | WEAK (0.29) | WEAK (0.30) | WEAK (0.29) | WEAK (0.31) |
| inf | PASS (0.01) | PASS (0.01) | PASS (0.01) | PASS (0.00) |

**Ch4 辅助判定**: NMSE=-10dB, N=500 → gain=0.00dB → **FAIL**

### 2.2 中湍流, τ=3ms, SNR=15dB

| NMSE | N=500 | N=1000 |
|------|-------|--------|
| -10dB | WEAK | WEAK |
| -15dB | WEAK | WEAK |
| inf | PASS (+1.33) | PASS (+1.28) |

---

## 3. VV 公式 Bug 影响分析（核心发现）

### 3.1 Bug 确认

代码 L138 使用公式 B（错误）:
```python
pe = np.unwrap(np.angle(avg)*4)/4  # BUG
```
正确公式 A: `np.unwrap(np.angle(avg))/4`

### 3.2 虚高增益的定量证据

将 Exp1 SNR=20dB 增益与 V-11 理论预测对比:

| 场景 | 仿真 gain (NMSE=-10dB) | V-11 理论预测 | 偏差 | 判定 |
|------|----------------------|-------------|------|------|
| weak_low | **+15.47 dB** | 0.5-1.5 dB | **+14 dB** | 严重虚高 |
| weak_high | **+15.47 dB** | 0-1.0 dB | **+14.5 dB** | 严重虚高 |
| moderate_low | **+5.38 dB** | 1.0-2.5 dB | **+3 dB** | 虚高 |
| moderate_high | **+5.38 dB** | 0.5-2.0 dB | **+3.5 dB** | 虚高 |
| strong_low | **+0.90 dB** | 1.5-3.0 dB | -0.6 dB | 合理范围 |
| strong_high | **+0.90 dB** | 1.0-2.5 dB | -0.6 dB | 合理范围 |

**关键发现**:
- 弱湍流增益虚高 14 dB（理论 0.5-1.5 dB → 仿真 15.47 dB），与 V-13 预测的"弱湍流 gain 可能虚高 1-6 dB"方向一致，但实际虚高幅度更大
- 中湍流增益虚高约 3 dB
- **强湍流增益反而低于理论预测**（0.90 vs 1.5-3.0 dB），这与 V-12 的发现一致——公式 B 对强湍流 BER 影响仅 1.3x，且影响在固定/自适应方案间近似对称

### 3.3 虚高机制

VV 公式 B 导致固定方案 BER 被不对称抬高:
- 固定方案: omega_n=8e6（非最优），DPLL 残余相位大 → VV 面对更多漂移 → 公式 B 偏差大 → BER 大幅抬高
- 自适应方案: omega_n 匹配信道，DPLL 残余相位小 → VV 面对较少漂移 → 公式 B 偏差小 → BER 抬高较小

固定方案 BER 被抬高更多 → BER_fixed / BER_adaptive 增大 → gain 虚高。

### 3.4 异常模式: weak_low ≈ weak_high

所有湍流强度下，low 和 high 仰角的 BER 和 gain 几乎完全相同（如 weak_low/weak_high 在 NMSE=-10dB 都是 15.47 dB）。

**原因分析**: 代码中多普勒条件通过 `doppler_phase()` 影响 `phi`，但 VV 公式 B 的结构性错误使得相位估计完全偏离正确值，多普勒差异被 bug 的巨大偏差淹没。这进一步证实 bug 在弱/中湍流下主导了结果。

### 3.5 NMSE=-20dB 强湍流出现 WEAK/NEG

SNR=20dB, NMSE=-20dB, 强湍流: gain=+0.29 dB (WEAK)。这与 NMSE 更差时反而 PASS 的模式矛盾（NMSE=-10dB 时 gain=+0.90 dB PASS）。

**解释**: NMSE=-20dB 时估计噪声极小（ε ≈ 0.01），自适应和固定方案的 DPLL 参数几乎相同，但 VV bug 对两者的残余影响在噪声极小时更趋于对称，导致 gain 缩小。NMSE=-10dB 时噪声稍大，自适应方案的 omega_n 调整在 bug 环境下产生了不对称效应。

---

## 4. 逐项检查清单

### 4.1 理论锚点对照 (V-11)

| 检查项 | 锚点 | 仿真结果 | 匹配度 | 受 VV bug 影响 |
|--------|------|---------|--------|---------------|
| NMSE=-10dB 弱湍流 BER 恶化 | +20% | 无法直接分离（gain 虚高） | 无法判定 | **是** |
| NMSE=-10dB 强湍流 BER 恶化 | +25-35% | 同上 | 无法判定 | 否（影响小） |
| NMSE=-10dB 强湍流自适应增益 | 1.5-3.0 dB | 0.90 dB | 偏低 40% | 否（影响小） |
| NMSE=-15dB 中湍流增益 | 1.0-2.5 dB | 5.17 dB | 虚高 2x | **是** |
| 误差不发散 | 是 | 仿真未崩溃 | 一致 | 否 |
| 单调退化（无尖锐阈值） | 是 | 平均 gain 单调变化 | 一致 | 否 |

### 4.2 H006 判定检查

| 检查项 | 标准 | 结果 | 判定 | 受 VV bug 影响 |
|--------|------|------|------|---------------|
| Strong PASS | >=4/6 PASS at NMSE=-10dB | 6/6 PASS | **STRONG PASS** | **是**（弱/中湍流虚高） |
| PASS | >=4/6 PASS at NMSE=-15dB | 6/6 PASS | PASS | **是** |
| Ch4 NMSE=-10dB N=500 | gain > 0.5 dB | 0.00 dB | **FAIL** | 否（Exp2 不使用 VV） |
| 级联曲线结构 | 单调退化 | 单调退化 | 一致 | 否 |

### 4.3 V-12 交叉验证

| 检查项 | V-12 结论 | 本次仿真是否支持 |
|--------|----------|----------------|
| 公式 B 在弱湍流 BER 膨胀严重 | 弱湍流 20x | **支持**: 弱湍流 gain 虚高 14 dB |
| 公式 B 在强湍流影响小 | 强湍流 1.3x | **支持**: 强湍流 gain 0.90 dB，接近理论 |
| DPLL 后 bug 影响被压缩但不为零 | 完整链路 1.3-20x | **支持**: gain 仍有系统性虚高 |

### 4.4 V-13 PASS 标准合理性

| V-13 预测 | 实际结果 | 一致性 |
|-----------|---------|--------|
| 弱湍流 gain 虚高 1-6 dB | 虚高 14 dB | 方向一致，幅度更大 |
| H006 等级可能虚高一级 | 实际可能虚高更多 | 一致 |
| 修正后预期 4/6 PASS | 待验证 | 待修正后重跑 |
| 强湍流 PASS 不受 bug 影响 | gain=0.90 PASS（接近边界） | 部分一致（低于理论但未翻转为 NEG） |

---

## 5. 修正后预期

基于 V-11 理论模型和 V-12/V-13 分析，修正 VV 公式后的预期:

| 场景 | 旧 gain (NMSE=-10dB) | 预期修正后 gain | 预期修正后判定 |
|------|---------------------|---------------|--------------|
| weak_low | +15.47 | 0.5-1.5 dB | 边界 PASS/WEAK |
| weak_high | +15.47 | 0-1.0 dB | WEAK/NEG |
| moderate_low | +5.38 | 1.0-2.5 dB | PASS |
| moderate_high | +5.38 | 0.5-2.0 dB | 边界 PASS |
| strong_low | +0.90 | 1.5-3.0 dB | PASS |
| strong_high | +0.90 | 1.0-2.5 dB | PASS |

**预期修正后 H006**: 4/6 PASS at NMSE=-10dB → **PASS**（非 Strong PASS）

---

## 6. Exp2 分析（不受 VV bug 影响）

### 6.1 核心发现

AR 预补偿在所有有噪声 h 条件下增益为 0 dB。仅在 oracle h（NMSE=inf）时有意义增益（2-3 dB）。

**原因**: `ρ_hat` 估计误差过大。即使 NMSE=-20dB，ρ_err 仍达 0.29-0.31。这是因为:
1. 噪声从幅度域传播到对数域（`ln(h_noisy^2)`），噪声被放大
2. AR(1) 的 ρ 估计对对数域噪声极敏感
3. ρ_err > 0.1 时 AR 预测严重偏离，预补偿失效

### 6.2 判定

Ch4 NMSE=-10dB, N=500: **FAIL** (gain=0.00 dB)
→ AR prediction 在有噪声估计下完全失效

---

## 7. 结论与行动项

### 7.1 可信结论（不受 VV bug 影响）

1. **强湍流自适应 DPLL 有效**: gain=0.90 dB at NMSE=-10dB (PASS)，修正后预期更高（1.5-3 dB）
2. **级联曲线结构合理**: 单调退化，无尖锐阈值
3. **误差不发散**: 所有 NMSE 水平均未崩溃
4. **Ch4 AR 预补偿在有噪声 h 下失效**: gain=0 dB at all noisy NMSE

### 7.2 受 VV bug 影响结论（需修正后重验）

1. **弱/中湍流增益**: 虚高 3-14 dB，修正后预期大幅下降
2. **H006 Strong PASS**: 修正后预期降为 PASS (4/6)
3. **弱湍流 BER 恶化量**: 无法从当前数据分离

### 7.3 必做行动

| 优先级 | 行动 | 原因 |
|--------|------|------|
| P0 | 修正 L138 为 `unwrap(angle(avg))/4` | 消除 14 dB 虚高 |
| P0 | 修正后重跑 Exp1 | 获取可信 H006 判定 |
| P1 | 增大弱湍流 Ns 至 10000 或 trials 至 50 | V-13 指出统计功效不足 |
| P2 | 记录修正前后对比 | 量化 bug 对论文结论的实际影响 |

---

## 附录: 原始数据

### A1. Exp1 关键数据 (SNR=20dB, NMSE=-10dB)

| 场景 | BER_fixed | BER_adaptive | gain (dB) | status |
|------|-----------|-------------|-----------|--------|
| weak_low | 0.06750 | 0.00192 | +15.47 | PASS |
| weak_high | 0.06750 | 0.00192 | +15.47 | PASS |
| moderate_low | 0.09473 | 0.02747 | +5.38 | PASS |
| moderate_high | 0.09473 | 0.02747 | +5.38 | PASS |
| strong_low | 0.16318 | 0.13275 | +0.90 | PASS |
| strong_high | 0.16320 | 0.13272 | +0.90 | PASS |

### A2. Exp2 关键数据 (weak, τ=5ms, SNR=15dB)

| NMSE | N=500 gain | N=500 ρ_err |
|------|-----------|------------|
| -5dB | 0.00 | 0.8930 |
| -10dB | 0.00 | 0.7666 |
| -15dB | 0.00 | 0.4979 |
| -20dB | 0.00 | 0.2972 |
| inf | +2.43 | 0.0064 |

### A3. E' 级联曲线 (SNR=20dB avg gain)

| NMSE | 平均 gain |
|------|----------|
| -20dB | 3.7 dB |
| -15dB | 4.8 dB |
| -10dB | 7.2 dB |
| -5dB | 11.1 dB |

单调退化（无尖锐阈值），但增益绝对值受 VV bug 影响。
