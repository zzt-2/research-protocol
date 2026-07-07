# B7 Gardner TED 复用 FOE 数学同族性检查

> 检查日期: 2026-07-07 | 任务: 判定 B7（ofc.2026.w2a.62，Gardner TED 复用做 FOE）跟 Gardner 1986 / VV / BPS 是否"数学同族"
> 纪律: 只读不改；每结论附行号；不做 Go/Kill 判断（主线/用户职责）；只做数学同族性分析
> 参考教训: NDA-ML 栽在跟 VV 强同族（mean-angle 等价）→ "vs VV 持平"被误读为合理结果实为 bug。本检查确认 B7 是否落入同类陷阱。

---

## Q1: B7 vs Gardner 1986

### 1986 原版 TED 公式（PSKTimingErrDetector.m）

函数签名（L1）：`x = PSKTimingErrDetector(S_tMinusT, S_tMinusHalfT, S_t, M)` —— 输入 3 个采样点（前一符号 `S_tMinusT`、半符号点 `S_tMinusHalfT`、当前符号 `S_t`）。

**经典 Gardner PSK 分支**（L8-9，当前被注释，但即 1986 原版形式）：
```
x = y_Re(2)*(y_Re(3)-y_Re(1)) + y_Im(2)*(y_Im(3)-y_Im(1));
```
即 `e(τ) = Re{ y_mid · (y_curr − y_prev)* }` —— 中间样本与"相邻符号差"的共轭乘积，取实部+虚部分量求和。**无升幂、无 angle、无窗口平均**。

**当前激活的 APSK 分支**（L11-12）是去 DC 的 Modified Müller-Müller 变体（中间点减去前后均值），仍属 Gardner 族 3 点检测器，输入/输出同构。

Tx2Rx.m L201 `eck(mk) = PSKTimingErrDetector(...)` + L204-207 环路滤波器 `omega(n+1) = (C1+C2)*eck(mk) − C1*eck(mk-1) + omega(n)` 证明：**1986 原版用途 = 逐符号瞬时定时误差 e(τ)，喂 NCO 驱动定时恢复环**（调采样时刻，不涉频偏）。

### B7 用 TED 干什么

- content.md **L15（Abstract）**："Based on the correlation between Doppler shifts and the Gardner TED, we propose a novel **frequency offset estimation algorithm**."
- **L21**："we propose a novel FOE algorithm that **estimates the Doppler shift by calculating the Gardner TED gain**."
- **L25**："We numerically investigate the relationship between **Doppler shift and Gardner TED gain**".
- **L37**："the **TED gain is obtained by calculating the maximum value of the S-curve** ... a clear **periodic correlation** exists ... enables the establishment of a **mapping** between the two within the range (−B, B)"。

**结论**：B7 用 TED **估计频偏 f_D**（不是定时误差 τ）。机制 = TED 增益（S-curve 最大值）随 Doppler 周期变化 → 在 (−B, B) 内建 TED_gain ↔ f_D 映射 → 扫频定位峰 → 双候选试补偿 → TED2 标准差判决（L37）。

### 输入/输出/数学运算是否同构？

| 维度 | Gardner 1986（PSKTimingErrDetector.m / Tx2Rx.m L201） | B7（content.md L15/21/25/37） |
|---|---|---|
| **输入量** | 3 个复采样点 (prev, mid, curr)（L1, L3） | 接收序列 + 频率扫描网格 (−B, B) + 间隔 f₁（L37） |
| **输出量** | 逐符号定时误差标量 e(τ)（驱动 NCO 调采样时刻，Tx2Rx.m L201/204） | 频偏估计 f̂_D（content.md L21） |
| **数学运算** | Re{mid·(curr−prev)*} 共轭乘积（L8-9），瞬时、逐符号 | 内部仍算同一 e_k 得 S-curve → **取 max_τ E[e_k]**（L37 "maximum value of the S-curve"）→ 反演映射 → 双候选 std 比较 |
| **同构？** | **否** | 输入基数不同（3 点 vs 序列+网格）、输出不同（τ vs f_D）、核心运算不同（瞬时乘积 vs S-curve 峰值+反演） |

### 关键判定（Q1）

B7 的"复用 FOE"是**算法层创新（把同一公式用在不同任务上）**，不是单纯参数调度/场景迁移。证据：
- 任务切换：1986 = 定时恢复（输出 τ，调采样），B7 = 频偏估计（输出 f_D，补偿频偏）—— **任务正交**。
- 输出量物理含义不同：e(τ) vs f̂_D。
- 后处理结构不同：1986 = 环路滤波器→NCO（Tx2Rx.m L204）；B7 = 扫频 + S-curve 峰检测 + 双候选 + TED2 std 判决（content.md L37）。

但**底层检测器公式共享**：B7 内部仍计算 Gardner 1986 的同一 e_k 以得到 S-curve（"Gardner TED gain" 即 1986 检测器的统计特性）。所以是"**共享工具，不共享任务**"——非强同族（C），属弱同族（B）。

---

## Q2: B7 vs VV / BPS

### VV 数学形式（_recovery.py L78-88）

```python
M = 4                                    # L79
raised = rx**M                            # L80: 升 M 次幂（去调制）
avg = np.convolve(raised, ker, 'same')    # L86: 滑窗平均（mean）
pe = np.unwrap(np.angle(avg)) / M         # L87: angle(mean) / M
```
**VV = `pe = (1/M)·angle( mean_window( rx^M ) )`**：升幂去调制 + 窗口平均 + 取角 + 除 M。**任务 = 载波相位恢复 CPR**（估 θ，非频偏）。核心 = **mean-angle of M-th power**。

### BPS 数学形式（_recovery.py L91-118）

```python
phases = 2π·arange(B)/B                   # L99: B 个测试相位网格
rotated = rx·exp(−1j·phases)              # L102: 逐相位旋转
dec = hard_decision(rotated)              # L103: 硬判决
dist = |rotated − dec|²                   # L104: 判决距离度量
metrics[b] = conv(dist, ker, 'same')      # L108-110: 滑窗平均
best_b = argmin(metrics)                  # L112: 选最小距离相位
pe = unwrap(4·pe_raw)/4                   # L116: M=4 去模糊
```
**BPS = `pe = argmin_b mean_window( |rx·e^{−jφ_b} − dec(·)|² )`**：暴力相位搜索 + 硬判决距离 + 窗口平均 + argmin。**任务 = CPR**（同 VV，但避开升幂用 brute-force + decision）。核心 = **argmin of mean decision-distance**（非 mean-angle）。

### B7 跟 VV/BPS 是否同族？

| 维度 | VV（L80/86/87） | BPS（L99/102-104/112） | B7（content.md L21/37） |
|---|---|---|---|
| **任务** | CPR（相位 θ） | CPR（相位 θ） | **FOE（频偏 f_D）** |
| **核心运算** | `angle(mean(rx^M))/M` mean-angle | `argmin_b mean(|rx·e^{−jφ_b}−dec|²)` 判决距离最小化 | `f̂_D = G⁻¹(max_τ S-curve)` 增益峰反演映射 |
| **升幂？** | 是（M=4） | 否 | 否 |
| **angle/argmin？** | angle | argmin | 都不是（用 max + 反演） |
| **统计量** | rx^M（去调制幂） | 硬判决欧氏距离 | Gardner 共轭乘积 e_k 的 S-curve 峰 |

**任务不同**（FOE vs CPR）；**数学运算层面无共享结构**：
- VV 的 mean-angle 结构 B7 没有（B7 不升幂、不取角、不做窗口平均的相位提取）。
- BPS 的 decision-distance 结构 B7 没有（B7 不硬判决、不搜相位网格最小化距离）。
- B7 的核心是"Gardner 交叉乘积 e_k = Re{mid·(curr−prev)*} 的 S-curve 峰值随频偏周期变化"，这是一个**检测器增益/幅度量随物理量（频偏）的可逆单调/周期映射**，跟 VV/BPS 的"相位提取"是两套机制。

唯一共性 = 三者都是"对样本做非线性变换 + 某种平均/聚合 + 提取估计"——这是所有盲估计器的公共伞，**不构成同族证据**。

**关键反 NDA-ML 陷阱结论**：NDA-ML 栽跟头是因为它跟 VV **同为 mean-angle 结构 + 同为 CPR 任务** → 数学等价 → "vs VV 持平"是 bug。B7 **既不共享 mean-angle 运算，也不共享 CPR 任务**，不存在"vs VV 持平 = 数学等价"的陷阱路径。

---

## Q3: 同族判定

### 标签: **(B) 弱同族**

### 理由

1. **vs Gardner 1986 = 弱同族（共享工具，不共享任务）**：
   - 共享：B7 内部使用 1986 的同一 Gardner TED 公式 e_k = Re{mid·(curr−prev)*}（PSKTimingErrDetector.m L8-9）来生成 S-curve。
   - 不共享：任务（FOE vs TED）、输出量（f_D vs τ）、后处理（扫频+峰反演+双候选 vs 环路滤波+NCO）。
   - 输入/输出/运算**不同构**（见 Q1 表）→ 非强同族（C）。

2. **vs VV / BPS = 非同族**：
   - 任务不同（FOE vs CPR）。
   - 核心运算无共享结构：VV=mean-angle of rx^M（L80/86/87）；BPS=argmin decision-distance（L99/112）；B7=S-curve 峰反演映射（content.md L37）。
   - **不存在 NDA-ML 式 mean-angle 等价陷阱**。

3. **综合**：B7 是真正的"算法复用创新"——把 1986 的定时检测器公式复用到频偏估计任务上，且跟 VV/BPS 的相位恢复数学无运算层等价。**复用创新真实存在**（不是换皮/换参数），但因底层公式继承自 1986，定为 (B) 弱同族而非 (A) 非同族。

### 若未来证据推向 (C)，拉开差距的条件

当前判 (B)，但**若出现以下任一**，则降级为 (C) 强同族（需重新定位贡献）：
- **条件 1（TED 增益↔f_D 映射等价于已知 FOE）**：若 B7 的"S-curve 峰随频偏周期变化"经推导等价于某个已知 FOE 数学（如 M-th-power 频率估计 Leven 2007 [7]、或谱相关/平方谱 FOE），则 B7 = 换皮。**当前 poster 未给闭合解析式（_B7 笔记 L21/L62）**，无法证伪等价性——这是残留风险点，建议主线要求 B7 给出 TED_gain(f_D) 解析式并显式对比 Leven M-th-power。
- **条件 2（双候选 std 判决等价于已有判决）**：若 TED2 标准差消歧等价于已知载波频偏细估计算法，则 B7 的"复用"= 已知模块拼接。
- **条件 3（基准对比被污染）**：若 B7 的 baseline 选 Gardner TR alone 而非 PSA FOE，且"B7 vs Gardner TR"持平 → 即同族 bug。**当前 baseline 是 PSA FOE（content.md L19/47，Vieira 2023），非 Gardner TR**，故此条件不成立。

**拉开差距的正道**：明确把贡献定位为"**任务重赋值（TED: τ→f_D）+ 增益-频偏可逆映射的新机制**"，而非"新检测器公式"；并补 TED_gain(f_D) 解析式以排除条件 1 的等价性。

---

## 关键证据指针

- **1986 公式源**：`毕设/旧本科代码/PSKTimingErrDetector.m` L1（签名）、L8-9（经典 Gardner PSK 分支 e=Re{mid·(curr−prev)*}）、L11-12（激活的 APSK 去DC 变体）；TR 环用途 `毕设/旧本科代码/Tx2Rx.m` L201（eck=PSKTimingErrDetector）、L204-207（环路滤波→NCO）。
- **B7 任务描述（FOE，非 TED）**：`papers/doi/10.1364_ofc.2026.w2a.62/content.md` L15（Abstract FOE）、L21（estimates Doppler by TED gain）、L25（Doppler↔TED gain 关系）、L37（TED gain=max S-curve，(−B,B) 映射，双候选+TED2 std 判决）。
- **VV 实现**：`projects/simulation/common/_recovery.py` L78-88，关键 L80（rx**M 升幂）、L86（conv 窗口平均=mean）、L87（angle(avg)/M = mean-angle）。
- **BPS 实现**：`projects/simulation/common/_recovery.py` L91-118，关键 L99（B 测试相位）、L102-104（旋转+硬判+距离）、L108-110（窗口平均）、L112（argmin）、L116（M=4 unwrap）。
- **B7 baseline = PSA FOE（非 VV/BPS/Gardner TR）**：content.md L19（PSA FOE 引入）、L47（PSA FOE 同条件测试）；DSP 链中 VV/BPS 未出现，CPR 用通用占位（L47 "carrier phase recovery (CPR)"，未指明算法）。
