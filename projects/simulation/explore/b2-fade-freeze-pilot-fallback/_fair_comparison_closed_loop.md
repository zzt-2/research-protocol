# 阶段 0.4（闭环版）：公平对照更新——power-boost overhead + 理论预期表

> 专题: 2026-07-08-b2-fade-freeze-pilot-fallback | 阶段: 1.5 步骤 1（0.4 重审）
> 日期: 2026-07-08
> 守: TL-20（先建理论预期）+ TL-27（挣扎前物理量级核算）+ D003 风险 1（power-boost overhead trade-off，net<0 不跑 sandbox）+ INVARIANT 13（饱和池难出区）
> 取代: 阶段 0.4 `_fair_comparison_framework.md` §3（pilot overhead 摊薄）的前馈版口径 + §6 判定门控（救援版重心调整）
> 输入: 阶段 0.3 闭环版架构 + power-boost 物理量级核算（本文件 §1）+ 前馈版 sandbox fade 块 BER 斜率实测

## 0. 更新背景

前馈版 `_fair_comparison_framework.md` 的 pilot overhead 是"ρ_fade × 1.249dB"（等功率 pilot）。闭环版引入 power-boost（β>1），overhead 公式改变。且救援版判定重心从 Go3（稳态 BER fair gain）转到 Go1（动态恢复）+ Go2（范围扩展）。

## 1. power-boost overhead trade-off 理论预期表（TL-20/TL-27 核算）

### 1.1 物理模型

fade 块内，固定总能量 E_tot（公平对照基准）：
- pilot 占空比 η_p = 0.25（spacing=4，step4a 继承）
- data 占空比 η_d = 0.75
- power-boost factor β：pilot 功率是 data 的 β 倍
- 归一化：`P_d = E_tot_per_sym / (η_d + η_p·β)`
- 数据 SNR：`SNR_d ∝ 1/(η_d + η_p·β)`（boost 拉低数据 SNR）
- pilot SNR：`SNR_p ∝ β/(η_d + η_p·β)`（boost 提升 pilot SNR）

### 1.2 理论预期表（β vs trade-off）

| β (boost) | pilot SNR 增益 | data SNR 损失 | fade 块内净 | 全帧 overhead (ρ_fade=0.15) |
|---|---|---|---|---|
| 1.0（等功率，前馈版）| 0 dB | 0 dB | 0 dB | 0 dB |
| 2.0（3dB boost）| +2.04 dB | −0.97 dB | +1.07 dB | +0.16 dB |
| 3.0（4.8dB boost）| +3.01 dB | −1.76 dB | +1.25 dB | +0.31 dB |
| 4.0（6dB boost）| +3.59 dB | −2.43 dB | +1.16 dB | +0.46 dB |
| 6.0（7.8dB boost）| +4.26 dB | −3.52 dB | +0.74 dB | +0.75 dB |

**关键结论**：
1. fade 块内 trade-off **净正**（β=2~4 时净 +1.07~+1.25dB），β>4 后边际递减（data SNR 损失追上 pilot 增益）
2. 全帧 overhead **小且缓增**（β=2 时仅 0.16dB，β=4 时 0.46dB）—— 因为仅 fade 期 boost（ρ_fade=0.15）
3. **最优 β ≈ 2-3**（fade 块内净正最大 + overhead 最小）

### 1.3 全局 net fair gain 量级核算（决定是否跑 sandbox 的红线门控）

全局 BER = 0.85×nonfade_ber + 0.15×fade_ber。fade 块 BER 改善只占 ρ_fade=15% 权重，但 overhead 从全局扣。

实测 fade 块 BER 斜率（前馈版，工作区 15-26dB）：
- weak: −1.15 ~ −2.41 dB(BER)/dB(SNR)（陡）
- moderate: −0.87 ~ −1.26 dB(BER)/dB(SNR)（中）
- strong: −0.61 ~ −0.96 dB(BER)/dB(SNR)（缓）

β=2 时 net fair gain 量级（fade 块 BER 改善 vs 全帧 overhead）：

| 场景 | fade 块 BER 改善（估）| 全局 BER gain | 扣 overhead | net |
|---|---|---|---|---|
| weak 高 SNR（斜率陡）| fade BER ×0.88 | +0.15~0.32dB | −0.16dB | **−0.01 ~ +0.16dB** |
| moderate 中 SNR（斜率中）| fade BER ×0.93 | +0.10~0.14dB | −0.16dB | **−0.06 ~ −0.02dB** |
| strong 低 SNR（斜率缓）| fade BER ×0.96 | +0.07~0.10dB | −0.16dB | **−0.09 ~ −0.06dB** |

**门控结论（D003 风险 1）**：
- net 在 **−0.09 ~ +0.16dB**（边缘区），**不显著 <0**（最坏 −0.09dB）
- **不触发红线「net<0 不跑 sandbox」**——可跑 sandbox 实测
- **但 Go3 稳态 BER fair gain 预期仍 <0.5dB**（饱和池警示 + net 边缘）→ 救援重心在 Go1（动态恢复）+ Go2（范围扩展）

## 2. 公平对照更新（闭环版三方）

### 2.1 三方总能量对比（@ 相同信息率，power-boost 仅 fade 期）

| 方案 | 非 fade 期 | fade 期 | 总能量 SNR γ_tot |
|---|---|---|---|
| A. 闭环完全 hold [79] | blind DPLL（0% overhead）| 完全 hold（0% overhead）| γ_d |
| B. 闭环 pilot 全程 + power-boost | pilot DPLL + β boost | pilot DPLL + β boost | γ_d + η_p·β/η_d（全帧，大 overhead）|
| C. 闭环双模 + power-boost | blind DPLL（0%）| pilot DPLL + β boost | γ_d + ρ_fade·η_p·(β−1)（摊薄，小 overhead）|

### 2.2 fair gain 计算更新

**测度 1：稳态 BER fair gain @ HD-FEC**（Go3，预期边缘）：
```
gain_A = (γ_d,A @ HD-FEC) − (γ_d,C + ρ_fade·η_p·(β−1) @ HD-FEC)
```
PASS 标准：≥0dB（不退化）。**预期 PARTIAL**（net 边缘，可能 +0.0~0.2dB）。

**测度 2：动态恢复时间**（Go1，救援核心）：
```
gain_recover = N_recover,A − N_recover,C
```
PASS 标准：gain_recover ≥ ΔN_min（闭环版才有意义，度量修复后 v2 算）。**这是救援版主要希望**。

**测度 3：范围扩展（strong）**（Go2）：
```
C 在 strong 某 OSNR 点可达 HD-FEC 而 A 不可达
```
PASS 标准：strong 某 OSNR 点 C < 3.8e-3 而 A ≥ 3.8e-3。power-boost 提升 fade 块 pilot 估计精度 → 可能扩 C 可达性。

### 2.3 power-boost 策略决策

**决策：仅 fade 期 power-boost（B2-Q2 原设计）**，不用全帧固定。
- 理由 1：全帧 power-boost overhead 太大（β=2 全帧 = η_p·β/η_d = 0.67dB vs 仅 fade 期 0.16dB）
- 理由 2：B2-Q2 命题是"fade 期 pilot 辅助"，非 fade 期不需要 pilot（blind 够用）
- 理由 3：仅 fade 期 boost 的 overhead 随 ρ_fade 自适应（strong ρ_fade 可能不同）

## 3. 判定门控更新（救援版重心调整）

### 3.1 Go 标准（FR-25，赢传统 baseline，任一满足即 Go）

闭环版 sandbox 后，**任一满足即 Go**（D005 多维够格）：
1. **Go1 动态恢复**：闭环版 C<A 显著（gain_recover ≥ ΔN_min）—— **救援核心目标**
2. **Go2 范围扩展**：power-boost 扩 C 可达性（strong 某 OSNR C 可达 HD-FEC 而 A 不可达）
3. **Go3 稳态 BER fair gain**：≥0.5dB @ HD-FEC —— **预期 PARTIAL（net 边缘），bonus 非 main**

**重心调整**：救援版主要希望 Go1 + Go2，Go3 预期不够格（饱和池 + net 边缘）。若 Go1+Go2 够格，Go3 PARTIAL 不影响 Go 判定。

### 3.2 Kill 标准（任一满足即报主控 Kill）

1. 闭环版动态恢复仍 A≈C（环路惯性 + power-boost 没加速收敛）→ 救援核心失败
2. power-boost overhead 吃掉所有 fade 块估计精度提升（net fair gain ≤0，实测确认）
3. 闭环版 C 全局 BER 退化（比前馈版还差）

## 4. 阶段 0.4（闭环版）结论

**公平对照更新完成**：
- power-boost 理论预期表落盘（β=2-3 最优，fade 块内净 +1.07~1.25dB，全帧 overhead +0.16~0.31dB）
- 全局 net fair gain 量级核算完成（−0.09~+0.16dB，边缘，不触发红线 Kill）
- 三方总能量对比更新（仅 fade 期 power-boost，overhead = ρ_fade·η_p·(β−1)）
- 判定重心调整（Go1 动态恢复 + Go2 范围扩展为主，Go3 稳态 BER 为辅）

**进阶段 0.5（闭环版）**：参数扩（power_boost_factor + 闭环环路参数，文献溯源）。
