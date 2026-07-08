# 阶段 0.3（闭环版）：架构重定性——[79] 式闭环 hold + 功率阈值 gate + power-boosted pilot

> 专题: 2026-07-08-b2-fade-freeze-pilot-fallback | 阶段: 1.5 步骤 1（0.3 重定性）
> 日期: 2026-07-08
> 守: D002（前馈化降级，[79] 式闭环 hold 不撞 D006）+ D003 救援路线 + V3 祖师爷（[79] 闭环 freeze 实现一致性）+ INVARIANT 15
> 取代: 阶段 0.3 `_architecture_decision.md` §5.1「前馈化 INVARIANT 级」（已被 D002 降级）
> 输入: D006 原文（`2026-06-20-problem-driven-redirection/decisions.md:313-355`）+ [79] L33（`_B2-deep-fade-freeze-increment.md:33`）+ 前馈版 sandbox 物理根因（`_sandbox_three_way.py:114-121` freeze_compensate_block 前馈开环）+ common/_recovery.py dpll_track 二阶 DPLL 结构

## 0. 重定性背景（为什么推翻前馈化）

前馈版 sandbox 三 Go 全 FAIL + Kill2 结构性成立（A_recover==C_recover 21 点全相同）。S004 主控核查发现根因：**前馈化砍掉了 [79] 闭环 freeze 的环路惯性**。

[79] L33 原文（`_B2-deep-fade-freeze-increment.md:33`）："FOE tracking 环路在 received power 下降时关闭 tracking（hold 上一估计值）"——[79] 是**闭环 tracking loop**，freeze 时环路滤波器 hold 住状态，fade 结束后环路从 hold 状态重新收敛（有惯性、有时间常数）。

前馈版 `freeze_compensate_block`（`_sandbox_three_way.py:114-121`）只 hold `(phi_last, omega_last)` 两个标量，砍掉了环路滤波器的积分器状态和收敛动力学 → 每块独立估计无跨块惯性 → A/C 非 fade 期 BER 序列完全相同 → N_recover A≈C。

D002 精读 D006 后修正：[79] 式闭环 hold（功率阈值 gate + 环路 TF 不感知湍流）**不撞 D006**。允许放松到闭环 hold。

## 1. 闭环 hold 的核心机制设计

### 1.1 [79] 式闭环 tracking loop（二阶 DPLL + 跨块状态）

**基础结构**：复用 common/_recovery.py `dpll_track` 的二阶 PI 环路滤波器，但改为**跨块状态传递**（前馈版每块独立）。

环路状态（跨块持久化）：
- `integrator`（积分器状态，二阶 DPLL 的频率记忆）
- `vco_phase`（VCO 当前相位，相位记忆）

每符号更新（非 fade 期，blind 驱动）：
```
mixed = rx[k] * exp(-j * vco_phase)
pd_out = angle(mixed^4) / 4          # 4th-power 鉴相（blind，不碰 φ_T）
integrator += c2 * pd_out
freq_out = c1 * pd_out + integrator
vco_phase += freq_out
```

每符号更新（非 fade 期，pilot 驱动，可选）：
```
mixed = rx[k] * exp(-j * vco_phase)
pd_out = angle(rx[k] * conj(pilot[k]))  # pilot 鉴相（不碰 φ_T）
integrator += c2 * pd_out
freq_out = c1 * pd_out + integrator
vco_phase += freq_out
```

**关键**：鉴相器输入是 `rx`（含载波相位 φ + 噪声），不是湍流相位 φ_T。`pd_out` 估的是载波相位误差（激光相位 + CFO 残余），不是湍流相位。**D006 不撞**（见 §2）。

### 1.2 fade 期 hold 机制（功率阈值 gate）

**完全 hold（方案 A，[79] 原版）**：
- fade 判定：`P_block = mean(|rx_block|²) < γ_th` → is_fade
- fade 期：冻结环路状态（`integrator`, `vco_phase` 不更新），用 hold 的 `vco_phase` 补偿当前块
- fade 结束（`P_block ≥ γ_th`）：环路从 hold 状态重新启动，自然收敛（有时间常数）

**partial hold + power-boosted pilot（方案 C，B2-Q2 救援版核心）**：
- fade 期：环路**仍运行**，但鉴相器切换到 power-boosted pilot 驱动（低噪声误差信号）
- power-boosted pilot 提供 SNR 更高的鉴相输入 → 环路收敛更快/估计更准
- fade 结束：切回 blind 驱动（非 fade 期无 pilot overhead）

### 1.3 完全 hold vs partial hold 的物理差异（救援版核心假设）

| 维度 | 完全 hold（A）| partial hold + power-boost（C）|
|---|---|---|
| fade 期环路状态 | 冻结（integrator/vco_phase 不变）| 运行（pilot 驱动更新）|
| fade 期相位跟踪 | 完全依赖 hold 值（fade 深 → hold 漂移）| pilot 持续跟踪（fade 期相位变化被跟住）|
| 恢复动力学 | 环路从 hold 重新收敛（时间常数 τ_loop）| 环路一直在跑，恢复更快（pilot 已跟住相位）|
| D006 | 不撞（功率 gate）| 不撞（pilot 鉴相不碰 φ_T）|

**救援核心假设（需 MVE 验证）**：C 的 partial hold + power-boost 能让 fade 结束后环路恢复**比 A 的完全 hold 更快**（因为 C 在 fade 期用 pilot 持续跟踪，环路状态没偏离；A 的 hold 状态在长 fade 后可能漂移，恢复需重新锁定）。

## 2. D006 不撞论证（V3 祖师爷边界核查）

### 2.1 D006 Kill 的精确动作（原文核查）

D006（`decisions.md:313-355`）Kill 的是："把**湍流相位 φ_T** 主动纳入载波同步算法设计"（无论 KF / 环路 TF / 其他数学工具）。具体被排除（`decisions.md:340-341`）：
- Q12 式"环路 H(z) 纳入 φ_T"
- B1 式"KF 状态扩维含 φ_T"
- 旧 B1"S024 KF 压力测试证伪"

### 2.2 闭环 hold 不撞 D006 的机制论证

闭环 hold 的环路 TF 是**固定的二阶 PI 滤波器**（c1/c2 由 omega_n/zeta 决定，不感知湍流）：
- `c1 = 2*zeta*wT`, `c2 = wT²`，其中 `wT = omega_n * T_S`（固定参数）
- 环路 TF `H(z)` 的输入是**鉴相器输出 pd_out**（载波相位误差），不是湍流相位 φ_T
- 门控用信号功率 `P < γ_th`（不用相位 φ_T）

**与 Q12/B1 的本质区别**：
- Q12/B1 = 把 φ_T 当算法状态/参数（KF 状态扩维 / H(z) 输入含 φ_T）
- 闭环 hold = 环路 TF 固定，只跟踪载波相位（φ = 激光相位 + CFO），fade 门控用功率

**仍禁的**（D006 真正禁的）：任何把 φ_T 当算法状态的闭环（如"环路 TF 随湍流强度自适应"或"KF 状态含 φ_T"）。闭环 hold 的环路参数是**固定的**（omega_n/zeta 预设），不随湍流变。

### 2.3 鉴相器输入核查（确认不碰 φ_T）

| 方案 | 鉴相器 | 输入 | 含 φ_T？ |
|---|---|---|---|
| A blind DPLL | `angle(mixed^4)/4` | rx（载波相位 φ + 噪声）| ❌ 否（估 φ 不估 φ_T）|
| C pilot DPLL | `angle(rx·conj(pilot))` | rx × pilot 共轭 | ❌ 否（估 φ 不估 φ_T）|

两种鉴相器都估**载波相位**（激光相位 + CFO 残余），不估**湍流相位**（φ_T 是慢变幅度/相位起伏，被 AGC + 均衡吸收，不进鉴相器）。

## 3. 三方对照设计（闭环版）

### 3.1 三方定义（V2 三方 + V3 祖师爷）

| 方案 | 非fade 期 | fade 期 | 角色 | 必须赢谁 |
|---|---|---|---|---|
| **A. 闭环完全 hold [79]** | blind DPLL 跟踪 | 完全 hold（冻结环路）| **祖师爷 baseline**（V3）| — |
| **B. 闭环 pilot 全程 + power-boost** | pilot DPLL + power-boost | pilot DPLL + power-boost | 消融（证明双模切换的增量）| — |
| **C. 闭环双模 + power-boost（B2-Q2）** | blind DPLL | pilot DPLL + power-boost | **提出方法** | **必须赢 A**（FR-15）|

### 3.2 power-boost 配置

- **power-boost factor β**：pilot 功率是 data 的 β 倍（β=2 即 3dB boost，待文献溯源定，见步骤 2）
- **power-boost 策略**：仅 fade 期（B2-Q2 原设计，overhead 小）/ 全程（B 消融，overhead 大）
- **公平对照**：fade 期 power-boost overhead = ρ_fade × η_p × (β−1)（仅 fade 期 boost 时），从全局扣

### 3.3 V3 祖师爷实现一致性核查清单（闭环版必过）

[79] 闭环 freeze 实现一致性（`_B2-deep-fade-freeze-increment.md:33`）：
- [ ] fade 期环路状态冻结（integrator/vco_phase 不更新）—— 不是前馈 hold 标量
- [ ] fade 结束后环路从 hold 状态重新收敛（有 PI 时间常数）—— 不是立即用当前 blind 估计
- [ ] 门控用信号功率 P < γ_th —— 不用相位
- [ ] 环路 TF 固定（omega_n/zeta 预设）—— 不感知湍流

**前馈版失败正是因为漏了前两条**（只 hold 标量，无环路收敛动力学）。

## 4. 动态恢复度量重设计（修 n_recover 退化）

### 4.1 前馈版 n_recover 度量退化（接收方验证发现）

前馈版 `compute_n_recover`（`_sandbox_three_way.py:291-340`）的退化机制：
- 稳态带 = `[0.9×steady_ber, 1.1×steady_ber]`（±10%）
- 高 SNR 下 steady_ber 极小（weak 26dB ~5e-4），±10% 带宽仅 ±5e-5
- 离散 BER 步长 ~1e-3（每块 256×4=1024 bit）→ 几乎不可能落 3 连块
- **所有 21 点命中 fallback**（L334 `n - trans_idx`），n_recover 只依赖 fade_state 与 BER 无关

**后果**：A_recover==C_recover 不是因为恢复动态一致，是度量退化。即使闭环版有真实恢复差异，不修度量也测不出。

### 4.2 闭环版 n_recover 度量重设计

**修复方案**：放宽稳态带判据 + 用滑窗均值代替离散逐块：

```python
def compute_n_recover_v2(per_block_ber, fade_state, steady_window=20, band=0.30):
    # 稳态 BER: 非 fade 块滑窗均值（排除热身）
    # 恢复判据: 滑窗均值落入 [1-band, 1+band]×steady（band=30% 比 10% 宽）
    # 滑窗长度 steady_window=20（平滑离散 BER 抖动）
```

**关键改动**：
1. `band` 从 10% 放宽到 30%（容纳离散 BER 抖动）
2. 用滑窗均值（window=20 块）代替逐块判据（平滑 1e-3 步长抖动）
3. 恢复 = 滑窗均值连续落入稳态带（不是逐块）

**阈值依据**：30% band 在 weak 26dB（steady ~5e-4）= ±1.5e-4，滑窗 20 块均值（~20480 bit）步长 ~5e-5，可落入。仍保持"显著恢复"语义（±30% 内算稳态）。

### 4.3 度量修复后的预期（闭环版才有意义）

修度量后，前馈版的 A_recover==C_recover 应**仍然成立**（前馈版无环路惯性，恢复动态确实一致——这是正确的物理结论）。闭环版则应出现 A_recover ≠ C_recover（环路惯性 + power-boost 加速收敛）。

**这是度量修复的验证**：修度量后前馈版 A==C 仍成立（物理一致）+ 闭环版 A≠C（环路恢复差异）→ 度量正确工作。

## 5. 风险跟踪（D003 救援路线 3 风险）

### 风险 1：power-boost overhead trade-off（物理可行性核心）

**TL-27 物理量级核算结论**（步骤 1 完成）：
- fade 块内 trade-off **净正**：β=2 时 pilot SNR +2.04dB vs data SNR −0.97dB → 净 +1.07dB
- 全帧 overhead **小**：仅 fade 期 boost，β=2 时 +0.16dB（ρ_fade=0.15）
- 全局 net fair gain **边缘区**（−0.09 ~ +0.32dB），取决于 fade 块 BER 斜率
- 实测斜率（−0.6 ~ −2.4 dB(BER)/dB(SNR)）比悲观假设陡 → 实际 net 可能更正

**门控结论**：net 不显著 <0（最坏 −0.09dB），**不触发红线「net<0 不跑 sandbox」**。可跑 sandbox 实测。但 **Go3 稳态 BER fair gain 预期仍 <0.5dB**（饱和池警示），救援重心在 Go1（动态恢复）+ Go2（范围扩展）。

### 风险 2：跟 [79] baseline 差异够格

闭环版 A = 完全 hold（[79] 原版），C = partial hold + power-boost。差异在 fade 期 pilot 驱动环路 vs 完全冻结。sandbox 要测 C 的恢复是否真比 A 快（+ 范围扩展）。

### 风险 3：sat.1553 口径

power-boosted pilot 是另一个物理机制（pilot 功率增强），不引 sat.1553 L440 +1dB（阶段 0.2 已确认口径错位）。增量独立 MVE。

## 6. 阶段 0.3（闭环版）结论

**架构定性完成**：
- **A = 闭环完全 hold [79]**（blind 二阶 DPLL + fade 期冻结环路状态）
- **C = 闭环双模 + power-boost**（非 fade blind DPLL / fade power-boosted pilot DPLL）
- **D006 不撞**：鉴相器估载波相位不估 φ_T，环路 TF 固定不感知湍流，门控用功率
- **度量修复**：n_recover v2（band 30% + 滑窗均值），修前馈版退化
- **power-boost 理论预期**：fade 块内净正，全局边缘，Go3 预期 <0.5dB，重心 Go1/Go2

**强度标签**：`DECIDED`（已决定，可讨论但需显式推翻）—— 闭环 hold 是 D002 降级后的设计选择，不是 INVARIANT。若闭环版 sandbox 仍 FAIL，可回退讨论。

**进阶段 0.4（闭环版）**：公平对照更新（power-boost overhead + 理论预期表）。

## 附：D006 不撞论证证据链（闭环版）

| 论点 | 证据 | 来源 |
|---|---|---|
| D006 Kill 的是"φ_T 纳入算法" | "联合建模进 DPLL 环路（把湍流相位 φ_T 纳入环路 TF）" | `decisions.md:324` |
| [79] 闭环 hold 是功率 gate 不是相位建模 | "FOE tracking 环路在 received power 下降时关闭 tracking" | `_B2-deep-fade-freeze-increment.md:33` |
| 闭环 DPLL 鉴相器估载波相位不估 φ_T | `pd_out = angle(mixed^4)/4`（blind）/ `angle(rx·conj(pilot))`（pilot）| common/_recovery.py:59-75 dpll_track |
| 环路 TF 固定不感知湍流 | `c1=2*zeta*wT, c2=wT²`（omega_n/zeta 预设）| common/_recovery.py:60-62 |
| 门控用功率不用相位 | `P_block = mean(|rx|²) < γ_th` | 本文件 §1.2 |
| D002 已开绿灯 | "[79] 式闭环 hold 不撞 D006" | decisions.md D002 §决策 |
