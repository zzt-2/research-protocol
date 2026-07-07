# B7 阶段 0.2：数学同族性 + B7 映射数值重建

> 阶段 0.2 | 专题 `2026-07-08-b7-gardner-ted-foe` | 日期 2026-07-08
> 依据：INVARIANT 11（Gardner TED 1986 数学同族性前置）+ sim-preflight v1.3.0 V2（三方对照）+ V3（祖师爷警报）+ V5（子 agent 归因独立核查）
> 结论：**0.2 通过，进 0.3。B7 机制数值验证成立 + 跟 1986 弱同族（共享工具不共享任务）+ 跟 VV/BPS 非同族。残留风险：B7 未给 TED_gain(f_D) 解析式，无法排除跟 Leven M-th-power FOE 等价**

## 0. 核查触发

INVARIANT 11 要求：Gardner TED 是 40 年前祖师爷方法（比 VV 1983 还老），B7 锚方法（OFC 2026 Gardner TED 复用 FOE）跟它比，**如果数学同族就是 NDA-ML D-008 陷阱重演**（vs VV 持平被当合理接受）。必须深度检查。

本阶段做两件事：
- **0.2a 数值重建**：用 Gardner TED 公式扫 Doppler 频偏，验证 B7 声称的"周期性相关"机制是否真实
- **0.2b 数学同族性分析**：B7 vs Gardner 1986 / VV / BPS 的数学关系

## 1. 0.2a 数值重建结论（B7 机制真实存在）

### 1.1 实验（子 agent 1 执行）

- 脚本：`_b7_map_reconstruction.py`（自写 RRC 成型 + Gardner TED + S-curve，未改 common/）
- 设置：25-Gbaud 单偏振 QPSK，RRC α=0.1，确定性频偏 `rx=tx·exp(j2πf_D t)`，Gardner `e(k)=Re{y_mid·(y*curr−y*prev)}`，S-curve = E[e(τ)] τ∈[0,T) 16 点，N_sym=1024，G = max|S-curve|
- 扫频：coarse 0-23 GHz（1GHz 间隔，对齐 poster）+ fine 0-3GHz（0.1GHz）+ diag 0-75GHz（验证周期）
- 噪声：无噪 + OSNR 17dB（poster 主测点，6× 噪声实现平均消除毛刺）

### 1.2 关键结论

**Q1: G(f_D) 随 f_D 是否周期变化？→ 是，周期 = baud rate B = 25 GHz**

| 条件 | FFT 主频能量占比（主线 V5 独立重算）| 测得周期 |
|---|---|---|
| 无噪 | **95.9%**（子 agent 报 94.5%，用 diag 76 点）| 24 GHz ≈ B |
| OSNR 17dB | **90.7%**（子 agent 报 87.1%）| 24 GHz ≈ B |

确定性铁证：`G_abs(0)=0.132142`（主线重算 = 子 agent 报 0.13214，bit-exact）。周期=符号率 B=25 GHz，吻合 poster "归一化到 baud rate"。

**Q2: 跟 poster "可逆映射"描述符相符吗？→ 部分不符**

poster 行 37 称"(−B,B) 内可逆"。主测段 0-23 GHz 数值显示：
- 无噪曲线 **U 形**：G 在 0→~13 GHz 单调降（0.132→0.007），~13→23 GHz 升（0.007→0.128）
- 单谷 1 转折点 → 同一 G 对应 2 个 f_D，**2:1 映射非单射**
- **这恰好是 poster Fig.1b "生成两个 Doppler 候选"的物理来源**（双候选算法自洽）
- poster "可逆"应理解为"半个周期 (0,B/2) 内单调可逆"，描述不精确但算法自洽

**Q3: 机制是否成立？→ 成立**

物理机制（子 agent 推测，标注）：f_D 在符号周期 T 引入净相位旋转 Δφ=2π·f_D·T，QPSK 星座旋转后相邻样本过零斜率被调制，Gardner S-curve 峰随 Δφ 以周期 f_D=B（Δφ=2π）变化，是 2π 相位模糊的时域表现。

### 1.3 V5 独立核查记录（子 agent 归因核查）

| 子 agent 报告 | 主线独立重算 | 判定 |
|---|---|---|
| G(0) = 0.13214 | G(0) = 0.132142（coarse[0]） | ✅ bit-exact |
| 周期 25.33 GHz | 周期 24 GHz（coarse 24 点 FFT）| ✅ 一致（采样点数差异）|
| 主频能量无噪 94.5% | 95.9%（coarse）/ 子 agent 用 diag | ✅ 一致量级 |
| U 形 1 转折点 @ ~13GHz | 最小值 @ 13GHz（G=0.006862）| ✅ 一致 |
| OSNR 17dB 6× 平均必要性 | 采纳（单次噪声会伪化周期判断）| ✅ 方法学合理 |

**V5 结论**：子 agent 原始数字可信，归因合理（标注推测）。机制真实性确认。

## 2. 0.2b 数学同族性分析结论

### 2.1 标签：(B) 弱同族

**vs Gardner 1986 = 弱同族（共享工具，不共享任务）**：

| 维度 | Gardner 1986（PSKTimingErrDetector.m / Tx2Rx.m L201）| B7（content.md L15/21/25/37）|
|---|---|---|
| 任务 | 定时恢复（输出 τ，调采样时刻）| **频偏估计（输出 f_D，补偿频偏）**|
| 输入 | 3 复采样点（prev, mid, curr）| 接收序列 + 扫频网格 (−B,B) |
| 输出 | 逐符号定时误差 e(τ) | 频偏估计 f̂_D |
| 后处理 | 环路滤波器→NCO（Tx2Rx.m L204）| 扫频 + S-curve 峰反演 + 双候选 + TED2 std 判决 |
| 底层公式 | `e = Re{mid·(curr−prev)*}` | 同（B7 内部用同一公式生成 S-curve）|

**任务正交**（FOE vs STR）+ **后处理结构不同构** → 非强同族 (C)。但**底层检测器公式共享** → 弱同族 (B)，不是非同族 (A)。

**vs VV / BPS = 非同族**：

| 维度 | VV（_recovery.py L78-88）| BPS（L91-118）| B7 |
|---|---|---|---|
| 任务 | CPR（相位 θ）| CPR（相位 θ）| **FOE（频偏 f_D）**|
| 核心运算 | `angle(mean(rx^M))/M` mean-angle | `argmin_b mean(|rx·e^{−jφ_b}−dec|²)` | `f̂_D = G⁻¹(max_τ S-curve)` 增益峰反演 |
| 升幂 | 是（M=4）| 否 | 否 |

**任务不同 + 核心运算无共享结构**。

### 2.2 关键反 NDA-ML 陷阱结论

NDA-ML 栽跟头的机制：跟 VV **同为 mean-angle 结构 + 同为 CPR 任务** → 数学等价 → "vs VV 持平"是 bug。

**B7 不存在这条陷阱路径**：
- 既不共享 mean-angle 运算（B7 用 S-curve 峰反演，不升幂取角）
- 也不共享 CPR 任务（B7 是 FOE）
- baseline 是 PSA FOE（content.md L19/47），不是 Gardner TR

→ **"B7 vs 谁持平 = 数学等价"的 bug 机制无法复现**。

## 3. 残留风险（带进 0.3 / sandbox）

| 风险 | 来源 | 触发降级 (B)→(C) 条件 | 处理 |
|---|---|---|---|
| **B7 未给 TED_gain(f_D) 解析式** | poster 仅图示（_B7 笔记 L21/L62）| 若解析式推出 B7 等价于 Leven M-th-power FOE [7] 或谱相关 FOE → 降级 (C) 强同族 | sandbox 前补解析推导；或在 MVE-SPEC 要求显式对比 Leven 2007 |
| 双候选 std 判决等价性 | poster 行 37 | 若 TED2 标准差消歧等价于已知载波频偏细估计算法 → B7 = 已知模块拼接 | sandbox 阶段做消融 |
| **poster "(−B,B) 可逆"描述不精确** | 0.2a 数值重建发现实际是 2:1 映射 | 不影响算法（双候选自洽），但写论文时要精确表述 | 论文写作时用"半周期单调可逆" |

## 4. 阶段 0.2 判定

| 维度 | 判定 | 依据 |
|---|---|---|
| B7 机制（周期相关）数值验证 | ✅ **成立** | G(f_D) 以 baud rate 周期，铁证 G(0)=0.132142，FFT 主频能量 >90% |
| B7 vs Gardner 1986 同族性 | ✅ **弱同族 (B)**（共享工具不共享任务）| 任务正交（FOE vs STR）+ 后处理不同构 |
| B7 vs VV/BPS 同族性 | ✅ **非同族** | 任务不同 + 运算无共享结构 + 无 NDA-ML 陷阱路径 |
| 是否进 0.3 | **是** | 0.2 通过，带残留风险（解析式缺失）|

**门控结论**：0.2 通过，进 0.3 架构定性。

**理由**：
- INVARIANT 11 要求的"深度数学同族性检查"已完成，结论 (B) 弱同族——不是 NDA-ML 式 (C) 强同族陷阱
- 0.2a 数值重建验证了 B7 机制真实存在（不是 poster 文字吹的）
- 残留风险（解析式缺失）通过 sandbox 前补解析推导 + Leven 对比处理，不阻塞 0.3

## 5. 对后续的影响

- **0.3 架构定性**：用户本地代码（Tx2Rx.m L176-214）是反馈环（NCO+环路滤波器），B7 算法也是反馈环（CV mult + TR loop）。前馈化决策仍需做（INVARIANT 12，环路撞 D006）。
- **sandbox 三方对照（V2+C7）**：① B7 proposed FOE（数值重建版）② Gardner 1986 定时环（用户代码当祖师爷方）③ PSA FOE baseline。三方都有实现路径。
- **论文叙事定位**（子 agent 建议）：明确把贡献定位为"**任务重赋值（TED: τ→f_D）+ 增益-频偏可逆映射的新机制**"，而非"新检测器公式"。
- **sandbox 红线警报条件**：若 sandbox 跑出"B7 vs Gardner 1986 定时环持平"→ 触发 V3+C8 祖师爷警报（但 0.2 已确认任务正交，持平可能性低）。

## 6. 证据指针

- **0.2a 数值重建**：
  - 脚本：`projects/simulation/explore/b7-gardner-ted-foe/_b7_map_reconstruction.py`
  - 数据：`_b7_map_results.json`（coarse/fine/diag 三种扫频 + S-curve 数组）
  - 图：`_b7_map_curve.png`
  - 摘要：`_b7_map_summary.md`
- **0.2b 数学同族性**：`projects/simulation/explore/b7-gardner-ted-foe/_lineage_check.md`（Q1/Q2/Q3 + 证据指针）
- **B7 poster 全文**：`papers/doi/10.1364_ofc.2026.w2a.62/content.md`
- **Gardner 1986 公式源**：`毕设/旧本科代码/PSKTimingErrDetector.m` L8-9（经典分支）/ L11-12（APSK 去DC 变体）
- **VV/BPS 实现**：`projects/simulation/common/_recovery.py` L78-88（VV）/ L91-118（BPS）
- **NDA-ML D-008 陷阱教训**：`.sessions/2026-07-06-step4a-mve-execution/decisions.md` D-008
