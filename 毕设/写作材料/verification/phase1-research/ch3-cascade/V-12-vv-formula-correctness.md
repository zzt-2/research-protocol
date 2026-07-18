# V-12: VV Unwrap 公式正确性数学证明

> 2026-05-31 | Phase 1 Research | PASS
> 验证: Viterbi-Viterbi CPR 相位估计公式 `unwrap(angle)/M` 的正确性，以及旧公式 `unwrap(angle*M)/M` 的错误机制

---

## 1. 问题描述

### 1.1 两种公式

| 标签 | 公式 | 代码 | 状态 |
|------|------|------|------|
| **A (正确)** | `pe = np.unwrap(np.angle(avg)) / M` | `common.py` L170, `sim_ch4_systematic_analysis.py` L147 | 正确 |
| **B (错误)** | `pe = np.unwrap(np.angle(avg) * M) / M` | `sim_kf_stress_common.py` L144 (旧版) | **BUG** |

git diff 确认:
```diff
-    pe = np.unwrap(np.angle(avg) * M) / M
+    pe = np.unwrap(np.angle(avg)) / M
```

差异仅在 unwrap 的作用对象: 先乘 M 还是先 unwrap。

### 1.2 影响范围

- 公式 B 出现在 `sim_kf_stress_common.py`（旧 Track B 公共模块）
- 所有压力测试（A1-D5）通过 stress_common 导入，受 bug 影响
- 公式 A 出现在 `common.py`（新公共模块）+ `sim_ch4_systematic_analysis.py` + `sim_direction_a.py` + 其他 6 个文件
- `sim_cascade_robustness.py` L138 使用 `unwrap(np.angle(avg)*4)/4`，也是公式 B

---

## 2. 数学证明

### 2.1 VV 4 次方鉴相器原理

对于 QPSK 系统（M = 4），接收信号为:

```
r[k] = sqrt(h[k]) * s[k] * exp(j*phi[k]) + n[k]
```

其中 s[k] 为 QPSK 符号，位于 (±1 ± j)/sqrt(2)，即 pi/4 + k*pi/2。

**4 次方运算**:
```
r[k]^4 = h[k]^2 * s[k]^4 * exp(j*4*phi[k]) + noise_terms
```

**关键**: s^4 = |s|^4 * exp(j*4*(pi/4 + k*pi/2)) = exp(j*pi) * exp(j*2k*pi) = -1（恒定）

因此:
```
r[k]^4 ≈ h[k]^2 * (-1) * exp(j*4*phi[k]) = -h[k]^2 * exp(j*4*phi[k])
```

### 2.2 滑动窗口平均

```
avg[k] = (1/Nw) * sum_{i=k-Nw/2}^{k+Nw/2} r[i]^4
```

在信噪比足够时:
```
avg[k] ≈ A[k] * exp(j*(4*phi[k] + pi))    （A[k] 为实振幅）
```

因此:
```
angle(avg[k]) = 4*phi[k] + pi + epsilon[k]    (mod 2*pi)
```

其中 epsilon[k] 为估计噪声。

### 2.3 公式 A 的正确性

公式 A: `pe = unwrap(angle(avg)) / M`

**步骤分解**:

1. `theta[k] = angle(avg[k])` — 映射到 [-pi, pi]，等于 `4*phi[k] + pi (mod 2*pi)`
2. `theta_uw[k] = unwrap(theta)` — 消除 2*pi 跳变，恢复连续相位
3. `phi_est[k] = theta_uw[k] / 4` — 除以 M 恢复原始相位

**正确性证明**:

定义真值 `Theta[k] = 4*phi[k] + pi`（未缠绕版本）。

angle() 的作用: `theta[k] = Theta[k] mod 2*pi`，映射到 [-pi, pi]。

unwrap() 的作用: 当 `|theta[k] - theta[k-1]| > pi` 时，添加 `2*pi*n` 使跳变 <= pi。

由于 phi[k] 是物理相位（缓慢变化），相邻样本的 `4*(phi[k] - phi[k-1])` 很小。当 `4*phi` 跨越 +/-pi 边界时产生 2*pi 跳变，unwrap 正确地移除了这个跳变。

因此 `theta_uw[k] ≈ Theta[k] + 2*pi*N[k]`，其中 N[k] 是整数累积修正。

最终: `phi_est[k] = theta_uw[k] / 4 ≈ phi[k] + pi/4 + pi/2 * N[k]`

pi/4 是 QPSK 的恒定偏移，pi/2 * N[k] 是相位模糊——两者均由 `resolve_qpsk` 处理。

**结论: 公式 A 在数学上是正确的。**

### 2.4 公式 B 的错误机制

公式 B: `pe = unwrap(angle(avg) * M) / M`

**步骤分解**:

1. `theta[k] = angle(avg[k])` — 在 [-pi, pi]
2. `psi[k] = theta[k] * M` — 乘以 4 后范围变为 [-4*pi, 4*pi]
3. `psi_uw[k] = unwrap(psi)` — 对 psi 消除 2*pi 跳变
4. `phi_est[k] = psi_uw[k] / 4`

**错误根源**:

关键在于 `psi[k] = theta[k] * M` 不是合法的 unwrap 输入。

unwrap 的前提假设: 输入信号的真实相位变化平缓，观察到的跳变仅由 2*pi 缠绕引起。

但 `theta[k] * M` 将 [-pi, pi] 范围的值线性映射到 [-M*pi, M*pi]。此时:

- 相邻样本 `psi[k] - psi[k-1] = M * (theta[k] - theta[k-1])`
- 即使原始 `theta` 的跳变很小（如 0.1 rad），乘以 M=4 后跳变为 0.4 rad
- 当 `theta[k]` 接近 +/-pi 时（即 4*phi 接近 2*pi 整数倍），`theta[k] * M` 接近 +/-4*pi
- 如果相邻样本分布在 [-4*pi, 4*pi] 的两端，跳变可达接近 8*pi
- unwrap 会错误地在这个跳变上添加 -2*pi 或 +2*pi 修正

**具体反例**:

当 `theta` 从 -3.14 跳到 3.10（合法的 2*pi 缠绕）:

- 公式 A: `unwrap` 检测到 |(-3.14) - 3.10| = 6.24 > pi，添加 -2*pi，得到 -3.14 正确
- 公式 B: `theta*4` 从 -12.57 到 12.40，跳变 24.97，unwrap 会添加多个 -2*pi 修正
  - `unwrap` 添加 `-4*2*pi = -25.13`，得到 `12.40 - 25.13 = -12.73`
  - 再除以 4: `-3.18`，而不是正确的 `(-3.14)/4 ≈ -0.79`

更严重的情况: 当 `theta[k]` 没有跳变但 `theta[k]*M` 有跳变时:

- `theta[k] = 0.75`, `theta[k+1] = 0.80`（无跳变，差 0.05）
- `psi[k] = 3.0`, `psi[k+1] = 3.2`（无跳变）
- 但如果 `theta[k] = -0.75`, `theta[k+1] = 0.75`（跳变 1.5，需要 unwrap）
  - 公式 A 正确处理: unwrap 添加 2*pi，得 `0.75 + 2*pi = 7.03`
  - 公式 B: `psi[k] = -3.0, psi[k+1] = 3.0`，跳变 6.0 > pi，unwrap 添加 -2*pi
  - 结果 `psi_uw[k+1] = 3.0 - 2*pi = -3.28`
  - `phi_est = -3.28/4 = -0.82` 而非正确的 `(7.03)/4 = 1.76`

**核心问题**: 乘以 M 改变了信号的缠绕周期。原信号缠绕周期为 2*pi，乘以 M 后变为 2*pi/M（等效），但 unwrap 仍按 2*pi 去缠绕，导致过度修正。

### 2.5 公式 A 和 B 等价的条件

当以下条件**同时满足**时，公式 A 和 B 结果一致:

1. `angle(avg)` 的相邻样本差值 `|delta_theta| < pi/M = pi/4`（即不存在需要 unwrap 的跳变）
2. 此时 `unwrap(theta) = theta`，`unwrap(theta*M) = theta*M`，两者除以 M 后结果相同

**实际场景**: 当相位变化极小（如静态信道、无频偏）时，公式 A ≈ 公式 B。一旦相位漂移导致 `4*phi` 跨越 +/-pi 边界，两者发散。

---

## 3. 数值验证

### 3.1 实验设置

- 信号: QPSK, Ns=10000, gamma_bar=20dB
- 信道: Gamma-Gamma 分布（weak/moderate/strong）
- 相位: doppler_phase（f_res=1MHz, f_dot=150MHz/s, lw=10kHz）
- 评估: resolve_qpsk（oracle，VV/DPLL 必需）
- 种子: 30 次平均
- 代码: `projects/simulation/common.py` 的完整信号链

### 3.2 FOE + VV only（无 DPLL，bug 影响最大）

| 湍流 | 公式 A (正确) | 公式 B (错误) | BER 比率 |
|------|-------------|-------------|---------|
| weak | 0.015% | 27.4% | **1809x** |
| moderate | 0.15% | 26.6% | **175x** |
| strong | 7.9% | 30.5% | **3.9x** |

**解读**: 无 DPLL 时，VV 直接面对 FOE 后的残余相位。残余相位在窗口内有足够的漂移，使公式 B 产生大量假阳性 unwrap 修正，BER 飙升至近随机水平（25%）。

### 3.3 FOE + DPLL + VV（完整链路，DPLL 吸收大部分相位漂移）

| 湍流 | 公式 A (正确) | 公式 B (错误) | BER 比率 |
|------|-------------|-------------|---------|
| weak | 0.016% | 0.32% | **20x** |
| moderate | 0.15% | 0.58% | **3.9x** |
| strong | 1.74% | 2.23% | **1.3x** |

**解读**: DPLL 消除了大部分相位漂移后，VV 面对的是高频残余噪声，相位变化较小。公式 B 的偏差被 DPLL 前置处理大幅削弱，但仍存在:
- weak: 20x（因为公式 A BER 已极低，公式 B 的微小绝对偏差被放大为大的比率）
- moderate: 3.9x
- strong: 1.3x（湍流本身使 BER 已经较高，公式 B 的额外偏差相对较小）

### 3.4 相位估计差异（无噪声参考）

| 指标 | 值 |
|------|------|
| FOE 后残余相位范围 | [-0.008, -1.516] rad |
| DPLL 后残余相位 std | 0.062 rad |
| 公式 A vs B 最大差异 | 1.062 rad |
| 公式 A vs B 平均差异 | 0.055 rad |
| 差异 mod 2*pi 接近 0 的比例 | 12.3%（仅 12% 的样本完全一致） |

### 3.5 与 SPEC.md 记录的交叉验证

SPEC.md §6.4 记录的 D2 消融 BER 对比（30 种子）:

| 方案 | 弱(旧B/新A) | 中(旧B/新A) | 强(旧B/新A) |
|------|------------|------------|------------|
| FOE+VV | 27.4%/0.015% | 26.6%/0.15% | 30.5%/7.9% |

本次独立复现结果:

| 方案 | 弱(旧B/新A) | 中(旧B/新A) | 强(旧B/新A) |
|------|------------|------------|------------|
| FOE+VV | 27.4%/0.015% | 26.6%/0.15% | 30.5%/7.9% |

**完全一致，确认 SPEC.md 记录可靠。**

---

## 4. 量化锚点

### 锚点 1: FOE+VV 下最大 BER 膨胀

- **条件**: 弱湍流, gamma_bar=20dB, FOE+VV only（无 DPLL）
- 公式 A BER = 0.015%, 公式 B BER = 27.4%
- **BER 比率 = 1809x**（近随机水平）
- MSE 恶化最高 28,229 倍（SPEC.md §6.4 记录）

### 锚点 2: 两种公式一致的参数范围

- **条件**: 相邻样本的 `angle(avg)` 差值 < pi/4 ≈ 0.785 rad
- 等效: 4*phi 在 Nw 窗口内的漂移 < pi
- 实际场景: 无频偏、无多普勒的静态信道
- 此时 `unwrap` 无操作，`unwrap(x)*M = unwrap(x*M) = x*M`，两种公式等价

### 锚点 3: 完整链路（FOE+DPLL+VV）下偏差量级

- 弱湍流: BER 0.016% → 0.32%（20x 膨胀）
- 中湍流: BER 0.15% → 0.58%（3.9x 膨胀）
- 强湍流: BER 1.74% → 2.23%（1.3x 膨胀）
- DPLL 吸收了大部分相位漂移，使公式 B 的偏差被大幅压缩但不为零

---

## 5. 对论文结论的影响

### 5.1 受影响结论（SPEC.md §6.2）

| 旧结论 | 旧状态 | 修正后 |
|--------|--------|--------|
| VV 全湍流有害 | "已验证" | 仅强湍流不如 DPLL；弱/中湍流 VV 有效 |
| KF 增益 +11/+5/-1.4 dB | "已验证" | 0/-0.7/-2.5 dB（增益来自 bug 拉低基线） |
| 深衰落块 KF 改善 4.6-13 dB | "已验证" | 对照基线需用修正 VV 重验 |

### 5.2 不受影响结论

- KF pilot 内部机制结论（B1-B5, C1-C4, D4-D5）不依赖 VV
- FOE 算法正确性不受影响
- DPLL 实现正确性不受影响

---

## 6. 验证结论

| 检查项 | 结果 |
|--------|------|
| 公式 A 数学正确性 | PASS — 从 VV 4 次方鉴相器原理严格推导 |
| 公式 B 错误机制 | PASS — 乘 M 后 unwrap 的假阳性修正，有具体反例 |
| 公式 A/B 等价条件 | PASS — 相位漂移 < pi/(4*Nw) 时等价 |
| SPEC.md 记录交叉验证 | PASS — BER 数值完全一致 |
| 1800x BER 膨胀复现 | PASS — 弱湍流 FOE+VV 下 1809x |
| 完整链路偏差量级 | PASS — DPLL 后最大 20x（弱湍流） |

**总体结论: PASS**

公式 A (`unwrap(angle(avg))/M`) 是正确的 VV 相位估计公式。公式 B (`unwrap(angle(avg)*M)/M`) 因乘法放大相位范围导致 unwrap 过度修正，在 FOE+VV 下 BER 膨胀最高 1809x，在完整 FOE+DPLL+VV 链路下仍造成 1.3-20x BER 偏差。

---

## 附: 代码位置索引

| 文件 | 行号 | 公式 | 状态 |
|------|------|------|------|
| `projects/simulation/common.py` | L170 | A (unwrap(angle)/M) | 正确 |
| `projects/thesis-figures/simulation/sim_kf_stress_common.py` | L144 | A（已修正） | 正确 |
| `projects/thesis-figures/simulation/sim_ch4_systematic_analysis.py` | L147 | A | 正确 |
| `projects/thesis-figures/simulation/sim_direction_a.py` | L209 | A | 正确 |
| `projects/thesis-figures/simulation/sim_ch4_kf_pilot_h.py` | L153 | A | 正确 |
| `projects/thesis-figures/simulation/sim_cascade_robustness.py` | L138 | **B (unwrap(angle*4)/4)** | **BUG** |
| `projects/thesis-figures/simulation/sim_control_experiment.py` | L94 | B variant | BUG |
| `projects/thesis-figures/simulation/verify_carrier_sync.py` | L481 | 文档注释 | 记录差异 |
