# [S015] A3 §4a 维度 D MVE Kill——AO 残余参数修正后挣扎失败

> 2026-06-17 续 9 | Groundwork §4a 维度 D (MVE) | 状态：Kill（D010 supersede D008）

## 目标

核实 S013/D008 Go 判定用的 AO 残余活塞相位参数（strong=300kHz）有无文献依据。若有 → 保真度风险收口；若无 → 重验或记债务。

## 记录

### 核实发现：AO 残余参数严重偏大

子 agent 检索超时（600s harness 上限），但**本地 Paillier 2020 正文（papers/arxiv/1911.11851/content.md）就给了直接依据**：

- §II 原话（verified）："the coherence time of the fluctuations are of the order of **1 ms**"
- "Most of the residual phase noise can be attributed to the **turbulent piston mode** which is not corrected by traditional adaptive optics systems [@Robert2016]"
- §V 原话："turbulent phase noise has **negligible impact** on the carrier synchronization process" + "DPLL is able to **maintain the lock** ... even in the presence of turbulence"

换算（Wiener：τ_c = 1/(2π·Δν)）：τ_c~1ms → Δν≈159Hz。

| 参数 | D008 用的 | Paillier 实测 | 偏差 |
|---|---|---|---|
| strong | 300 kHz | ~159 Hz | **大 1885 倍** |
| moderate | 100 kHz | ~53 Hz | 大 628 倍 |
| weak | 30 kHz | ~16 Hz | 大 188 倍 |

D008 的 14× raw→oracle gap 主要是这个虚高参数造的——等于自己设靶自己打。

### 修正参数重验

AO 参数改到 Paillier 量级（strong=159Hz）后重跑：
- raw→oracle gap 从 0.34 缩到 0.0025（缩小 136 倍）
- M1b pilot CPE gap_fill 大面积为负（strong γ=10dB = -697%，pilot 反而加噪声）
- AO 相位 64-symbol 块漂移仅 0.008 rad，pilot 估计噪声（CRLB 0.08-0.25 rad）远大于要追的相位

### 挣扎（两个口子全堵）

用户问"还能挣扎一下吗"，我评估成功率 20-30%，建议半小时试。用户选试。设硬截断。

**口子1（堵）**：补 AO 残余相位本身——Paillier 实测 negligible。

**口子2（本轮试，堵）**：加时变多普勒（LEO 多普勒斜率）强制 PLL 动态跟踪，赌 deep fade 瞬态 PLL 失锁。物理量级核算（_doppler_slope.py）：
- MVE 序列 N=8192 × T_S=1ns = **8.2μs**
- 8.2μs 内即使多普勒斜率 1MHz/s，序列内频偏变化仅 8.2Hz，累积相位误差 ~0
- 要 fft_foe 失效需斜率 **>7.4 GHz/s**（非真实残余量级，LEO 残余顶多 MHz/s）
- **MVE 时间尺度太短，时变多普勒来不及变化**

物理量级直接堵死，硬截断触发。

### 判定

**A3 §4a 维度 D MVE Kill（D010）。** D008 Go 作废。

A3 在 MVE 能模拟的时间尺度（μs 级）和真实 AO 残余参数下，信道里没有 pilot CPE 能补的时变相位损伤。与 N1 MVE FAIL（D007）同构。

## 决策引用

- D008（superseded）：A3 §D MVE Go——基于偏大 1885x 的 AO 残余参数，作废
- **D010（新建）**：A3 §D MVE Kill，两个挣扎口子全堵
- D007：N1 §D MVE FAIL——A3+N1 双 Kill，只剩 2.2 地板，第三腿待议

## 范围确认

- 本轮是否在 scope boundary 内：**是**（核实 S013/D008 参数依据 + 挣扎重验，都在 A3 §4a 维度 D 范围内）
- 无 scope change

## 后续

1. **教训沉淀**（用户要求）→ thesis-lessons.md 新增 TL-26/27（见下）
2. 战略重整：A3+N1 双 Kill，只剩 2.2 地板，需议第三腿（或承认只一腿）
3. A3 工程资产保留（explore/a3-pilot-cpe-mve/），pilot 注入 bug 调试教训 + Cheng 2013 Eq.5 迁移验证仍有价值
