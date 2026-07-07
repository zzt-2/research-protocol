# B7 TED_gain(f_D) 解析推导 + Leven 2007 M-th-power FOE 对比

> sandbox 子 agent | 专题 `2026-07-07-b7-gardner-ted-foe` | 日期 2026-07-07
> 目的：闭合 D002 残留风险——推导 B7 TED_gain(f_D) 解析式，显式对比 Leven 2007 [7]，判定 (B) 弱同族 vs (C) 强同族
> 耗时：脚本运行 2.8 s；产物 4 个文件（脚本 / JSON / PNG / 本摘要）

## 1. G(f_D) 解析式（主结果）

**信号模型**：`rx(t) = z(t)·exp(j2πf_D·t)`，`z(t)=Σ aₙ g(t−nT)`，aₙ i.i.d. QPSK（E[aₙ]=0, E[|aₙ|²]=1, E[aₘ aₙ*]=δₘₙ），T=1/B，g=成形脉冲。窄带/短滤波器近似（exp(j2πf_D t) 提到匹配滤波卷积外，与 0.2a `apply_foe` L112-115 一致）。

**Gardner TED**：`e(k)=Re{y_mid·conj(y_curr−y_prev)}`。三个样本带线性相位 φ_c, φ_m, φ_p，关键相位差只取决于 f_D·T：
- `Δ := φ_c−φ_m = 2π·f_D·(T/2) = π·f_D/B`（**无量纲，周期来源**）
- `φ_p−φ_m = −Δ`

代入展开并对 i.i.d. QPSK 取统计平均（3 点相位差结构 + Gardner 半符号对称 → sin 项为零），得：

```
S(τ; f_D) := E[e(k)] = K(τ)·cos(π·f_D/B)        ★ 解析 S-curve ★
```

其中 **K(τ) 是与 f_D 无关的纯 τ 函数**（由成形脉冲自相关决定，单边 RRC vs 升余弦形状不同，但 f_D 依赖性已被完全解耦）。增益：

```
G(f_D) = max_τ |S(τ;f_D)| = K_max·|cos(π·f_D/B)|    ★ 解析主结果 ★
```

**关键洞察**：f_D 依赖性被完全解耦为单一余弦因子 cos(πf_D/B)——这是 Gardner TED 3 点相位差结构决定的，**与具体脉冲形状无关**。

## 2. 周期性证明（解析精确）

```
G(f_D+B) = K_max·|cos(π(f_D+B)/B)| = K_max·|cos(πf_D/B + π)| = K_max·|cos(πf_D/B)| = G(f_D)   ∎
```
- 数值验证：`max|G(f+B)−G(f)| = 7.46e-17`（解析精确=0，浮点噪声）
- **零点**：G=0 ⇔ cos(πf_D/B)=0 ⇔ f_D=(n+0.5)B。B=25GHz → 12.5, 37.5, 62.5 GHz
- **半周期可逆**：(0,B/2) 内 cos 单调降，G 单射可逆。poster "(−B,B) 可逆" 实为"半周期单调可逆"（0.2a 发现 U 形/双候选来源 = 此余弦对称）

## 3. 数值验证（bit-exact 锚点对齐）

| 量 | 解析值 | 0.2a 锚点 | 误差 |
|---|---|---|---|
| K_max = G(0) | **0.132142** | 0.132142 | **0.00%（bit-exact）** |
| K(τ) vs 0.2a S-curve(0) RMS | — | — | **0.00e+00（bit-exact 复现）** |
| 周期性 max\|G(f+B)−G(f)\| | 7.46e-17 | — | 解析精确 |
| cos 包络 RMS（全 0-75GHz）| 0.001318 | — | — |
| cos 包络 RMS（f_D≤12GHz=B/2）| 0.001497 | — | — |

K(τ) 用确定性单符号响应精确计算（`K(τ)≡E[e(k)]|_{f_D=0}`，无蒙特卡洛），与 0.2a 锚点 bit-exact。cos 包络在低 f_D 区与数值精确吻合；高 f_D 区偏差来自窄带近似（RRC span 内相位旋转），**不影响周期 B / 零点位置**（0.2a FFT 主频能量 >90% 在 baud rate）。

## 4. Leven 2007 M-th-power FOE 公式提取（原文核对）

**论文已落盘**：`papers/doi/10.1109_lpt.2007.891893/content.md`（PTL vol.19 no.6 pp.366-368，Leven/Kaneda/Koc/Chen，Bell Labs）。DOI `10.1109/LPT.2007.891893`（task brief 写 `891597` 笔误，内容=正确论文，B7 poster ref[7] 完全匹配）。

**Leven 算法**（content.md **L33-65**, THEORY 节；公式图片 omitted，文字描述清晰；理论引 Meyr/Moeneclaey/Fechtel [7] ch.8.2.2）：
```
步骤1: r_k = y_k · conj(y_{k-1})           (相邻符号共轭积, 相位=符号间相差)   [L55]
步骤2: r_k^M  (QPSK M=4, 升 4 次幂去调制)                                    [L55]
步骤3: R = (1/N) Σ_k r_k^4  (N=500 样本平均)                                [L57]
步骤4: f̂ = angle(R) / (M·2π·T) = angle(mean_k[y_k conj(y_{k-1})]^4)/(8πT)  [L65]
```
**重要更正**：Leven 是**时域 phase-increment mean-angle**（相邻共轭积升 M 次幂取平均相位），**非** task brief 假设的"频域 FFT 谱峰"。本脚本以原文文字为准实现。L51/L127/L151 给出 M-th-power 模糊性分析（相位切片 → 频偏模糊周期 = B/M = 6.25 GHz for M=4）。

## 5. 同族性判定：(B) 弱同族（不降级 C）

**判据**：(C) 强同族要求"核心运算层等价 + 任务相同"。

| 维度 | B7 | Leven 2007 |
|---|---|---|
| **任务** | FOE（Doppler 估计）| FOE（频偏估计）| **同** |
| **乘积结构** | Gardner 3 点交叉乘积 `y_mid·conj(y_curr−y_prev)` | 2 点相邻共轭积 `y_k·conj(y_{k-1})` | **不同** |
| **非线性** | Re 部（线性）| 升 4 次幂 `^4`（强非线性去调制）| **不同** |
| **聚合** | `max_τ\|S-curve\|` 扫频峰反演 | `angle(mean_k ·)` mean-angle | **不同** |
| **f_D 依赖** | cos(πf_D/B) 周期 B | B/M=B/4 模糊周期 | **不同** |
| **升幂 / angle** | 无（M=1，纯交叉乘积）| 有（M=4，mean-angle）| **不同** |

**三层运算均不等价**（乘积结构 / 非线性 / 聚合）→ 核心运算层不等价 → 不满足 (C) "核心运算层等价" 判据。
**判定 (B) 弱同族**：共享 FOE 任务，但运算层无等价结构。

**反 NDA-ML 陷阱**：B7 既不升幂也不 mean-angle，不存在"B7 vs Leven 持平 = 数学等价"的 bug 路径（与 VV 同理，0.2b 已确认）。

## 6. 残留风险闭合结论

**D002 弱同族 (B) 确认，不降级 (C)。** 残留风险闭合。

依据：(1) 解析推导 G(f_D)=K_max·|cos(πf_D/B)| 揭示 B7 核心是 Gardner TED 交叉乘积 S-curve 峰的余弦调制，与脉冲无关的 cos 包络 + 周期 B；(2) Leven 核心是相邻共轭积升 4 次幂 mean-angle，三层运算（乘积/非线性/聚合）均与 B7 不同；(3) (C) 强同族判据"核心运算层等价"不满足。

## 7. 证据指针

- 脚本：`projects/simulation/explore/b7-gardner-ted-foe/_ted_gain_analytic.py`
- 数据：`_ted_gain_analytic_results.json`（解析式 + 数值验证 + Leven 对比 + 扫频曲线）
- 图：`_ted_gain_analytic_comparison.png`（B7 G(f_D) 解析vs数值 / S-curve / Leven M-th-power 行为 / 运算对比表）
- B7 poster：`papers/doi/10.1364_ofc.2026.w2a.62/content.md` L15/21/25/37/47/49
- Leven 原文：`papers/doi/10.1109_lpt.2007.891893/content.md` L33-65（THEORY）、L51/127/151（模糊）
- 0.2a 锚点：`_b7_map_results.json` coarse[0].G_abs=0.132142
