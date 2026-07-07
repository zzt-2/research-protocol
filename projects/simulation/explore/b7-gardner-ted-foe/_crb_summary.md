# B7 Gardner TED FOE — 经典频偏 ML CRB 下界 (FR-21 参考对照)

> sandbox 子 agent | 专题 `2026-07-07-b7-gardner-ted-foe` | 日期 2026-07-07
> 任务：推导 B7 FOE 的 CRB 下界，作 **FR-21 参考对照**（D005 降级，**非 Kill 门**）
> 耗时：脚本运行 <1 s；产物 3 个文件（脚本 / JSON / PNG / 本摘要）

## 1. CRB 公式（形式 + 来源 + 假设）

**信号模型**（与 `_ted_gain_analytic.py`、`content.md` L47 一致）：
```
rx(t) = s(t)·exp(j·2π·f_D·t) + n(t)
s(t) = RRC 成型 25 GBaud DP-QPSK,  roll-off 0.1;   n(t) = AWGN (OSNR 17/10 dB)
```

**B7 是间接估计**（Gardner TED 增益 `G(f̂)=K_max·|cos(πf̂/B)|` 扫频找峰反演 f̂_D，非直接 ML 频偏估计）。严格 CRB 推导复杂，故用**经典频偏 ML CRB 作参照下界**——B7 作为 NDA 次优间接估计，实际方差 ≥ 此 CRB。

**公式（★ 主结果）**：
```
var(f̂_D) ≥ CRB(f_D) = 12 / [ (2π)² · (E_s/N_0) · T_s² · N·(N²−1) ]   [Hz²]
std(f̂_D) ≥ sqrt(CRB)                                                  [Hz]
```
- **常数 12**（不是 6）：对应 f_D 与初相 φ 同时未知的情形（FOE 现实场景，相位未知）。6 是相位已知特例（不现实）。本任务用 12。
- **来源**（经典标准 DSP 文献，C6 溯源，非臆造）：
  - **Rife & Boorstijn 1974**, IEEE TASSP 22(2) — 单音频率+相位同时估计 ML CRB（常数 12 的原始来源）
  - **Kay 1993**, *Fundamentals of Statistical Signal Processing Vol I*, ch.15.7 — ML 频偏估计 CRB
  - **Mengali & D'Andrea 1997**, *Synchronization Techniques for Digital Receivers* §3.7
- **假设**：data-aided / 已知 s(t)（**绝对下界**）；AWGN；符号率采样 N 个符号（间隔 T_s）；相位未知（nuisance 积分掉）。
- **理论趋势**：大 N 极限 `N·(N²−1)≈N³` ⇒ `std ∝ 1/√SNR · N^(−3/2)`。

**OSNR → E_s/N_0**（光通信标准，B_ref=12.5 GHz 参考，0.1 nm）：
```
E_s/N_0 (linear) = OSNR (linear) · (2·B_ref)/R_SYM
25 GBaud: (2·12.5 GHz)/25 GHz = 1.0 恰好 ⇒ E_s/N_0_dB = OSNR_dB (巧合)
```

## 2. 关键数字（主线独立重算核对）

| 量 | 值 |
|---|---|
| **N=1024, OSNR=17 dB（B7 主测点）CRB std** | **59 415.7 Hz = 59.42 kHz = 5.942×10⁻⁵ GHz** |
| 同点 CRB 方差 var | 3.5302×10⁹ Hz² |
| **CRB / 扫频间隔 1 GHz** | **5.94×10⁻⁵**（CRB 比 1 GHz 小 **16 830 倍**）|
| N=1024, OSNR=10 dB（低 SNR）CRB std | 133.0 kHz = 1.33×10⁻⁴ GHz |

**独立重算核对**（主线可在 Python 一行复现）：
```python
import numpy as np
R=25e9; Ts=1/R; N=1024; EsN0=10**(17/10)*(2*12.5e9)/R
var = 12/((2*np.pi)**2*EsN0*Ts**2*N*(N**2-1))   # 3.530222e+09 Hz^2
std = np.sqrt(var)                                # 59415.675 Hz  ✓ bit-exact
```

## 3. CRB vs 扫频间隔 1 GHz 对比（瓶颈判定）

**CRB std（59 kHz）<< 扫频间隔 1 GHz**（小 16 830 倍）。
⇒ **B7 精度瓶颈是扫频量化（1 GHz 离散网格），不是理论 CRB 极限。**

- 扫频网格量化误差量级：±0.5 GHz（最近网格点距离）= 5×10⁵ kHz，比 CRB std 大 **~8400 倍**。
- 含义：B7 若需亚 GHz 精度，理论上可缩小扫频间隔达到——poster Fig.3b 已证实"初始估计后窄带重扫（如 7 GHz→6–8 GHz）"有效。当前 1 GHz 是**工程实现选择**，非 CRB 卡的。
- CRB 量级（10⁴–10⁵ Hz）vs B7 LEO Doppler 摆幅 ±100 MHz（content.md L47）：CRB 远小于 Doppler 幅度，估计 SNR 充足。

## 4. N sweep 趋势

`std ∝ N^α`，N≥512 拟合 **α = −1.500**（理论大 N −3/2 吻合，bit-exact，守 C6 公式自洽）。
CRB 随 N 翻倍降 √8≈2.83×（N=1024→2048 @17dB：59.4→21.0 kHz）。

| OSNR (dB) | N=256 | N=1024 | N=4096 |
|---|---|---|---|
| 10 | 1064 kHz | 133 kHz | 16.6 kHz |
| **17** | 475 kHz | **59.4 kHz** | 7.43 kHz |
| 20 | 337 kHz | 42.1 kHz | 5.26 kHz |

SNR 依赖：OSNR 10→17→20 dB（线性 10→50→100），CRB std ∝ 1/√SNR 降 √5→√10（N 固定）。

## 5. FR-21 参考结论（非 Kill 判据）

- **CRB 给出 B7 FOE 理论精度地板**（DA ML，乐观）：N=1024/OSNR=17dB 下 std ≈ 59 kHz。
- **B7 实际方差 ≥ CRB**（B7 是 NDA 间接估计，次优）。
- **B7 实际主导误差源 = 1 GHz 扫频量化网格**，比 CRB 大 ~10⁴ 倍量级——CRB 远不是 B7 的约束。
- **FR-21 = 参考对照**（D005）：CRB 数值回答"B7 FOE 离理论极限多远"——答案是**非常远**（理论空间巨大），但不作 Go/No-Go。B7 的 Go 判据 = 赢传统 baseline 几 dB（D005 务实路线）。
- **务实启示**：B7 当前 1 GHz 扫频对"估准 0–23 GHz 范围"足够（poster Fig.3a 实测准），若下游（MIMO/CPR）需更高精度可窄带重扫（Fig.3b 路径），CRB 不卡。

## 6. 证据指针

- 脚本：`projects/simulation/explore/b7-gardner-ted-foe/_crb_lower_bound.py`（自包含，不 import common/params）
- 数据：`_crb_results.json`（N×OSNR sweep + key_findings + CRB 公式溯源）
- 图：`_crb_curve.png`（左：CRB std vs N 三 OSNR + 1 GHz 水平线；右：CRB vs 1GHz/23GHz 量化对比）
- B7 poster：`papers/doi/10.1364_ofc.2026.w2a.62/content.md` L21/L47/L49（25 GBaud / roll-off 0.1 / OSNR 17 dB / 扫频 0–23 GHz 间隔 1 GHz）
- G(f_D) 解析（步骤 3）：`_ted_gain_analytic_results.json`（K_max=0.132142，周期 B=25 GHz）
- D005 FR-21 降级：`.sessions/2026-07-08-b7-gardner-ted-foe/decisions.md` D005
