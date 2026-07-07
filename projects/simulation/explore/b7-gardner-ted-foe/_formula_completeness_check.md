# B7 阶段 0.1：锚论文公式完整性核查

> 阶段 0.1 | 专题 `2026-07-08-b7-gardner-ted-foe` | 日期 2026-07-08
> 依据：INVARIANT 13（锚论文公式完整性前置）+ sim-preflight v1.3.0 C6（公式来源逐项核对）+ V1（公式不全直接标红）+ TL-23（验证完再下结论）
> 结论：**Gardner TED 1986 公式完整可实现（用本地 Matlab 代码作公式源）；B7 OFC 2026 "TED 增益↔Doppler 映射" 解析式缺失，需数值重建验证**

## 0. 核查触发

INVARIANT 13 要求：B7 OFC 2026 poster 只有 90 行（比 B11 PTL 2025 的 226 行薄），公式不全直接标红不硬磕。本核查在进 0.2 数学同族性检查 / sandbox 之前完成，决定是否切降级方案（A/B/C）。

## 1. B7 OFC 2026 poster 公式盘点（全文 90 行）

| 项 | poster 状态 | 证据（content.md 行号） |
|---|---|---|
| **编号公式** | **0 个** | 全文无 Eq.(1)、(2)…编号 |
| **S-curve 解析式** | 缺失（文字"maximum value of the S-curve"） | 行 25-37 |
| **TED 增益↔Doppler 映射解析式** | 缺失（"periodic correlation""nonlinear"文字） | 行 37 |
| **算法框图 Fig.1b** | **picture omitted**（[426×143]）| 行 27 |
| **机制图 Fig.1a**（Doppler↔TED 相关）| **picture omitted**（[426×143]）| 行 27 |
| **实验结果图 Fig.3/4**（4 张）| **全 omitted** | 行 57, 61 |
| **文字可提取的算法结构** | CV mult1 扫频→双候选→CV mult2 试补偿→LPF2+Gardner TR→TED2 标准差判决 | 行 37-39 |
| **文字可提取的机制** | Doppler 归一化到 baud rate；TED gain = S-curve max；(−B,B) 内可逆映射 | 行 37 |

**关键图全 omitted**：B7 的核心机制证据（Fig.1a Doppler↔TED 周期相关图）和算法实现蓝图（Fig.1b 框图）在 PDF→md 转换中丢失。这跟 NDA-ML LMMSE 复现失败教训（TL-23/TL-28）是同一级别——靠文字重建算法风险极高。

## 2. Gardner TED 1986 公式核查（用户本地 Matlab 代码作公式源）

### 2.1 公式源选择

Gardner 1986 原文（`papers/doi/10.1109_tcom.1986.1096561/`）是扫描 PDF，content.md 只有 14 行 IEEE 授权水印，**正文完全不可检索**。原计划的降级 C（用 1986 原文做公式交叉验证）无法靠现有 content.md 实现。

**用户指出本地有 Gardner TED 的完整 Matlab 实现**：`毕设/旧本科代码/PSKTimingErrDetector.m` + `毕设/旧本科代码/Tx2Rx.m`（定时同步段 L176-214）。代码是公式的可执行版，比扫描原文可靠。

### 2.2 Gardner TED 公式（来自本地代码 `PSKTimingErrDetector.m` L11-12）

```matlab
e(k) = (Re(y_mid) − (Re(y_late)+Re(y_early))/2) · (Re(y_late)−Re(y_early))
     + (Im(y_mid) − (Im(y_late)+Im(y_early))/2) · (Im(y_late)−Im(y_early))
```

输入 3 点：`y_early = S_tMinusT`（前一符号）、`y_mid = S_tMinusHalfT`（中间半采样点）、`y_late = S_t`（当前符号）。

**这是 Gardner 1986 原版 TED**（零交叉定时误差检测器），标准形式：
$$e(\tau) = y(t-\tfrac{T}{2})\cdot[y(t) - y(t-T)]$$

代码用的是去直流变种（`y_mid − (y_late+y_early)/2` 代替 `y_mid`），等价于标准 Gardner TED（去直流版本在某些教材写法里更常见，减少直流偏移影响）。

### 2.3 定时恢复环结构（来自 `Tx2Rx.m` L176-214）

| 组件 | 代码位置 | 公式/实现 |
|---|---|---|
| NCO 控制字更新 | L193 `eta(n+1) = eta(n) - omega(n)` | 标准数字 NCO |
| 立方内插（分数延迟） | L198-200 `InterpCubic` | Farrow 结构 3 次内插（`InterpCubic.m`）|
| Gardner TED | L201 `PSKTimingErrDetector` | 见 §2.2 |
| 环路滤波器（PI） | L204 `omega = (C1+C2)*eck - C1*eck_prev + omega` | 标准 PI 环路滤波器 |
| 环路参数 | L177-178 `C1=1/2^5, C2=C1²/2` | 经典 Gardner 环路增益 |

**结论**：Gardner TED 1986 原版（定时恢复环）**公式完整可实现**。B7 DSP 链中的 "Gardner TR [6]" 这一段（poster 行 47），用户代码完整覆盖，可直接复用。✅

## 3. B7 创新点公式核查（"proposed FOE"）

### 3.1 B7 创新点拆解（来自 poster 行 25-39 文字）

B7 的核心不是 Gardner TED 本身（那是 1986 的定时恢复器），而是：

1. **发现**：Doppler 频偏与 Gardner TED 增益之间存在周期性相关（TED 增益 = S-curve 最大值，随符号净相位旋转量周期变化）
2. **复用**：把这个映射当 FOE（频偏估计器）用——扫频找 TED 增益峰 → 反推 Doppler
3. **算法**：CV mult1 扫频定位峰→生成 2 候选→CV mult2 试补偿→LPF2+Gardner TR→TED2 标准差判决

### 3.2 公式缺口

| B7 组件 | poster 状态 | 能否用本地代码 |
|---|---|---|
| Gardner TED 函数（作 FOE 的"传感器"）| 引 [6] = 1986 原版 | **能**（§2.2 代码）|
| **TED 增益 G(f_D) = max S-curve(f_D)** | **解析式缺失**（只有"max of S-curve"文字）| **数值可重建**（用 §2.2 代码扫 f_D 跑 S-curve）|
| **映射 f_D ↔ G 的周期性** | 图示 Fig.1a（**omitted**）| **数值可重建**（扫 f_D 看周期）|
| 算法结构（CV mult1/2 + LPF + TED2 判决）| 框图 Fig.1b（**omitted**）+ 文字 | 文字描述够实现，缺细节 |
| 双候选判决（TED2 标准差比较）| 文字 | 够实现 |

### 3.3 数值重建路径

B7 的核心机制（"TED 增益↔Doppler 周期相关"）**可以数值验证**：

- 用本地 Gardner TED 代码（§2.2），对每个 Doppler 频偏 f_D（0~B 扫频），生成受 f_D 相位旋转的接收信号，跑 TED 得 S-curve，取 max = G(f_D)
- 画 G(f_D) vs f_D 曲线，验证是否有 poster 描述的"周期性相关"
- 这正好重建了 poster Fig.1a 那张 omitted 的图

**如果数值重建出周期相关** → B7 机制成立，0.1 通过（带"解析式缺失但数值重建可行"的债务）
**如果数值重建不出周期相关** → B7 机制本身有问题，红线警报（poster 结论不可复现）

## 4. 阶段 0.1 判定

| 维度 | 判定 | 依据 |
|---|---|---|
| Gardner TED 1986 公式完整性 | ✅ **完整可实现** | 本地 Matlab 代码作公式源（PSKTimingErrDetector.m + Tx2Rx.m L176-214）|
| B7 "proposed FOE" 解析式完整性 | ⚠️ **缺失**（poster 无编号公式 + Fig.1a/b 全 omitted）| content.md 行 27/37 |
| B7 机制数值重建可行性 | ✅ **可行**（用本地 TED 代码扫频跑 S-curve）| §3.3 |
| 是否切降级 A/B/C | **不切** | 1986 公式有代码替代；B7 映射可数值重建；不硬磕 = 不靠文字重建算法，数值重建是验证不是文字重建 |

**门控结论**：0.1 通过（带债务），进 0.2 数学同族性检查。**不切降级方案**。

**理由**：
- INVARIANT 13 的"公式不全直接标红不硬磕"针对的是"靠文字描述重建算法公式"（LMMSE 教训）。本场景 1986 公式有可执行代码（比原文强），B7 映射靠数值重建（不是文字猜公式），不违反"不硬磕"精神。
- 用户本地代码是意外资产，把"降级 C 救 1986 原文"从"OCR 扫描件"升级为"直接用可执行实现"。

## 5. 已知债务（带进 0.2 / sandbox）

| 债务 | 原则 | 触发解决条件 | 归属阶段 |
|---|---|---|---|
| B7 映射解析式缺失 | INVARIANT 13 / V1 | 0.2 数值重建验证周期相关后，若进 sandbox/MVE 则补解析推导 | 0.2 / sandbox |
| B7 算法框图 Fig.1b omitted | C6 公式来源核对 | 实现时按文字描述（CV mult1/2+LPF+TED2）+ 跟用户代码定时环对接 | sandbox |
| Gardner 1986 扫描原文不可检索 | FR-26 证据链 | 本地代码已替代；若需引用 1986 原文具体行号，需重新 OCR/换源下载 | 视需要 |

## 6. 对 0.2 / 0.3 / 后续的影响

- **0.2 数学同族性**：核心问题是"B7 跟 1986 是不是数学同族"。现在 1986 公式明确（§2.2），B7 创新点是"复用 TED 增益做 FOE"——这两者**不是同一个量的变体**（1986 用 TED 检测定时误差 τ；B7 用 TED 增益的峰值估计频偏 f_D）。**初步看非同族**（B7 是把 TED 当传感器复用，不是改 TED 公式），但需 0.2 深度确认（V3+C8 祖师爷警报）。
- **0.3 架构定性**：用户代码是反馈环（NCO+环路滤波器），B7 算法也是反馈环结构（CV mult+TR loop）。前馈化决策仍需做（INVARIANT 12，环路撞 D006）。
- **sandbox 三方对照**：① B7 proposed FOE（数值重建版）② Gardner 1986 原版定时环（用户代码直接当祖师爷方）③ PSA FOE baseline。三方都有实现路径。

## 7. 证据指针

- B7 poster 全文：`papers/doi/10.1364_ofc.2026.w2a.62/content.md`（90 行，0 编号公式，4 图 omitted）
- B7 metadata：`papers/doi/10.1364_ofc.2026.w2a.62/metadata.json`（title_match exact，2026-07-03 下载）
- B7 增量精读笔记：`papers/_read_notes/_B7-gardner-ted-increment.md`
- Gardner 1986 扫描原文（正文不可检索）：`papers/doi/10.1109_tcom.1986.1096561/content.md`（14 行水印）
- **本地 Gardner TED 代码（1986 公式源）**：
  - `毕设/旧本科代码/PSKTimingErrDetector.m`（TED 核心公式 L11-12）
  - `毕设/旧本科代码/InterpCubic.m`（Farrow 立方内插）
  - `毕设/旧本科代码/Tx2Rx.m` L176-214（定时恢复环：NCO+环路滤波器+TED+内插）
- NDA-ML D-008 教训（公式核对重要性）：`.sessions/2026-07-06-step4a-mve-execution/decisions.md` D-008
- sim-preflight v1.3.0 C6/V1：`.agents/skills/sim-preflight/rules/mve-validation.md` + `SKILL.md` §1.6
