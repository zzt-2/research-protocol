# A1 参数适配实验报告 — NDA-ML 块长自适应 K

> 日期: 2026-07-08 | 来源: adaptation-scan.md A1 参数适配 | 状态: **FAIL**
> 数据: `_a1_calibration.json`（35 点标定）+ `_a1_adaptive_k_results.json`（8 点 5 seed 验证）
> 脚本: `a1_calibration.py`（57.7s）+ `a1_validation.py`（169.5s）
> 设计: `_a1_adaptive_k_design.md`（TL-20 理论预期 + 实验矩阵）

## 一句话结论

**FAIL — 自适应 K 策略无可实现增量。** 自适应-J4（可实现版）在 8 点中 0 点显著赢固定 K=16，aggregate gain = 0.000 dB（退化到 always-K16）。即使 oracle 上界（每场景选真实最优 K，非可实现）aggregate 也仅 -0.474 dB，且其中 -2.46 dB 全部来自 1000kHz 一个极端点（不在实测主流星地 FSO 10-80kHz 区间）。去掉 1000kHz 后 oracle aggregate 仅 -0.190 dB。

→ **A1 参数适配方向无信号，跳过（adaptation-scan.md 失败信号命中：最优值不随条件变 → 无自适应空间）。**

## 实验设计回顾（adaptation-scan.md A1）

**核心问题**：NDA-ML 块长 K 的最优值是否随条件变化？自适应 K 是否优于固定 K？

**M-C-A**：方法 M=NDA-segmented 块内 CPE，条件 C=线宽/湍流/SNR，策略 A=自适应 K。
**baseline 结构**（adaptation-scan.md 规则）：方法=自适应 K 策略 / 主 baseline=固定 K（同族不同策略）/ 参照=VV / 上界=oracle K。

**TL-20 理论预期 5 锚点偏离情况**：

| 锚点 | 预期 | 实测 | 判定 |
|---|---|---|---|
| E1: A1 信号（最优 K 随条件变 ≥4×） | K 变化 8→32 | 跨线宽 K∈{8,16,32}，变化 4×但非单调 | ⚠️ 弱信号（仅边界变）|
| E2: 自适应赢固定 K=1 ≥+1dB | — | aggregate +0.736 dB（自适应赢 K=1）| ✅ 但无意义（K=1 本就弱）|
| E3: 自适应赢固定 K=8 ≥+0.3dB | — | aggregate +0.177 dB（K=8 接近 K=16）| ❌ 不达 |
| **E4: 自适应赢固定 K=32 >0** | **关键** | **oracle -0.474（仅靠 1000kHz），J4 可实现版 +0.000** | **❌ FAIL** |
| **E5: 判据-K 映射 \|ρ\|≥0.6** | **关键** | **最强 \|ρ\|=0.36（J2），J4 修正后 ρ=-0.019** | **❌ FAIL** |

**E4+E5 双 FAIL → A1 无可实现增量，判定 FAIL。**

## 阶段 1 标定结果（35 点单 seed）

### 4 判据 vs 最优 K 相关性

| 判据 | 物理意义 | Spearman ρ | Pearson r | 判定 |
|---|---|---|---|---|
| J2 scintillation index | 湍流功率波动 | **−0.361**（最强）| −0.496 | ❌ <0.6 |
| J1 升幂幅值方差 | 幅值波动 | −0.345 | −0.461 | ❌ |
| J3 盲 SNR (dB) | 信噪比 | +0.325 | +0.359 | ❌ |
| J4 升幂相位差分方差 | 线宽代理 | −0.019（**修正后**）| +0.012 | ❌ 几乎零 |

**无判据达 |ρ|≥0.6 可靠映射阈值。**

### J4 bug 发现 + 修正

**原实现 bug**：`phase = np.unwrap(np.angle(raised))`，M₀=8 升幂后 `M₀·θ` 极易超 2π，unwrap 路径错乱 → J4 跨线宽几乎不变（10kHz→3.13, 1000kHz→3.12），与线宽代理预期完全相反。

**修正**：不 unwrap，用 mod 2π 相位增量：
```python
ang = np.angle(raised)  # [-π,π]
dang = (np.diff(ang) + np.pi) % (2*np.pi) - np.pi
j4 = np.var(dang)
```

**修正后仍 ρ=-0.019**——unwrap bug 是真的，但修对后 J4 仍无预测力。根因：升幂后相位增量方差被 AWGN 噪声主导（非线宽），单块 256 样本估计方差大。

### 核心发现：K=16 普适性

固定 K=16 在 35 标定点中 **25 点（71%）跟 oracle 持平**（|rel|≤5%）。oracle 明显赢 K=16 的 10 点集中在：
- 1000kHz AWGN（K=32 比 K=16 好 39%）
- 低 SNR（14dB）部分点（K=4 比 K=16 好）
- 湍流场景（K=1-2 比 K=16 好一点，但都在 0.3dB 内）

**K=8/16/32 三档判据值（J2 median 0.557-0.559）完全重叠不可分**——主战场无法分桶。

## 阶段 2 验证结果（8 点 × 5 seed）

### 完整 gain_vs_K16 表（dB，负=自适应/该方法好）

| 场景 | oracle | adapt-J4 | adapt-SNR | K=1 | K=8 | K=32 | VV |
|---|---|---|---|---|---|---|---|
| AWGN 10kHz/18dB | −0.08 | +0.00 | −0.05 | +0.23 | −0.07 | +2.00 | −0.05 |
| AWGN 100kHz/18dB | +0.00 | +0.00 | +0.59 | +3.66 | +0.09 | +2.35 | +0.23 |
| **AWGN 1000kHz/18dB** | **−2.46** | **+0.00** | **+2.97** | +3.23 | +2.21 | **−2.46** | +2.43 |
| weak/12dB | −0.15 | +0.00 | −0.15 | −0.15 | −0.13 | +0.24 | −0.13 |
| moderate/16dB | −0.36 | +0.00 | −0.33 | −0.36 | −0.23 | +0.71 | −0.26 |
| strong/20dB | −0.34 | +0.00 | −0.32 | −0.33 | −0.22 | +0.51 | −0.24 |
| uplink_moderate/16dB | −0.18 | +0.00 | −0.16 | −0.17 | −0.13 | +0.25 | −0.12 |
| uplink_strong/20dB | −0.21 | +0.00 | −0.19 | −0.21 | −0.10 | +0.30 | −0.13 |

### Aggregate gain vs K=16（8 点平均，dB）

| 方法 | aggregate | 说明 |
|---|---|---|
| **adaptive_oracle** | **−0.474** | 上界（非可实现），其中 −2.46 dB 全来自 1000kHz |
| adaptive_j4（可实现）| **+0.000** | **退化到 always-K16**（J4 映射无预测力）|
| adaptive_snr（可实现）| +0.294 | SNR 映射比 K16 差 |
| fixed_k1 | +0.736 | K=1 全场景最弱 |
| fixed_k8 | +0.177 | K=8 接近 K=16 |
| fixed_k32 | +0.488 | K=32 在低线宽灾难（+2.0~+2.35 dB）|
| vv_nw64 | +0.219 | VV 默认参，作参照 |

### PASS/FAIL 判据核对

- ❌ **自适应-J4 CI 显著赢 K=16 的点数 = 0/8**（要求 ≥2）—— J4 映射退化到 always-K16，gain 恒 0
- ❌ **aggregate gain_vs_K16 = +0.000 dB**（要求 <0）—— 可实现自适应不优于最强固定 K
- **两判据均不满足 → FAIL**

### oracle 上界拆解（即使非可实现也只值 -0.474 dB）

```
AWGN1000kHz:  -2.463 dB  <<< 唯一显著（K=32 vs K=16）
moderate:     -0.363 dB
strong:       -0.335 dB
uplink_strong:-0.214 dB
uplink_mod:   -0.178 dB
weak:         -0.155 dB
AWGN10kHz:    -0.082 dB
AWGN100kHz:   +0.000 dB
---
aggregate:    -0.474 dB
去掉1000kHz:  -0.190 dB  ← 真实主流场景自适应上界
```

**即使有完美 oracle 判据，去掉 1000kHz 极端点后自适应上界仅 -0.19 dB**（会议级 <0.5dB 薄增益区间，D005 Conditional 区间下沿）。且这 -0.19 dB 还需要完美判据（实际判据 ρ<0.6 无法实现）。

## VV 参照结论

VV Nw=64 aggregate vs K=16 = +0.219 dB（VV 稍差于 K=16）。但 D-009 层 4 已证 VV 调 Nw=16 在高线宽反超。**本实验 VV 用固定 Nw=64（不调参）作参照**，结论：
- 自适应 oracle（-0.474）> VV（+0.219）：上界赢 VV
- 自适应 J4（+0.000 ≡ K16）也赢 VV（+0.219）：固定 K=16 本身就比 VV 默认参好
- 但 VV 若也自适应（Nw 随线宽调），D-009 层 4 数据显示 VV Nw=16 在 1000kHz 赢 NDA K=32

→ **"自适应"是普适思路（VV 也能自适应），NDA 的 K 自适应无独占优势。**

## 失败根因分析（adaptation-scan.md 防坑核对）

1. **最优 K 变化范围窄**：跨线宽 K∈{8,16,32}（3 档），非 {1,2,4,...,32}（6 档）。主战场集中在 K=16，自适应空间被"普适固定 K"压缩。
2. **最优 K 非单调**：10kHz→K16, 50kHz→K8, 100kHz→K16。50kHz 的 K=8 是噪声波动（单 seed），多 seed 后大概率也是 K=16。非单调关系使判据映射难拟合。
3. **判据层失效**：4 判据 |ρ|全 <0.6，J4（理论最强线宽代理）修正后仍 ρ=-0.019。根因：升幂后相位增量被 AWGN 噪声主导，单块 256 样本估计方差大，无法可靠代理线宽。
4. **唯一显著点不在主流场景**：1000kHz 是唯一 oracle 显著赢 K=16 的点，但 D-009 已确认实测主流星地 FSO 用 ECL 10-80kHz，1000kHz 是 Valjus 设计容限上界非典型值。

## adaptation-scan.md 防坑清单核对

- [x] 没锁死单一方法内部找增量（A1 扫的是 K 策略，A2/A3/A4 待后续扫描）
- [x] A1 扫描覆盖 NDA + VV 两方法参数
- [x] baseline 是"不做适配的版本"（固定 K），不是弱方法（K=16 是标定发现的最强普适固定）
- [x] 优势区间有明确理由（线宽变化致最优 K 变化）——但区间太窄 + 判据失效
- [x] C1 关键参数扫描（线宽 6 点 + SNR 5 点 + 湍流 5 场景 = 35 标定点）
- [x] C6 公式来源（nda_segmented_eq 复用 parity 脚本，已验证）
- [x] C7 三方对照（自适应 / 固定 K / VV 参照 + oracle 上界）
- [x] TL-20 理论预期（5 锚点，E4/E5 FAIL）
- [x] TL-29 多 seed（5 seed 主结果）
- [x] 只改 explore/nda-awgn-tracking-sandbox/，未动 common/simulator/params
- [x] 未用 dpll_track（4 次方鉴相器）

## 数据指针

- 标定数据: `explore/nda-awgn-tracking-sandbox/_a1_calibration.json`（35 点单 seed，4 判据 + 全 K BER）
- 验证数据: `explore/nda-awgn-tracking-sandbox/_a1_adaptive_k_results.json`（8 点 5 seed，自适应 vs 固定）
- 标定脚本: `explore/nda-awgn-tracking-sandbox/a1_calibration.py`
- 验证脚本: `explore/nda-awgn-tracking-sandbox/a1_validation.py`（含 J4 修正）
- 设计文档: `explore/nda-awgn-tracking-sandbox/_a1_adaptive_k_design.md`（TL-20 + 实验矩阵）
- 前序 K 扫描: `explore/nda-awgn-tracking-sandbox/_parity_tuning_sweep.json`（D-009 35 点）

## 对 adaptation-scan 的回答

> adaptation-scan.md："在我们的场景下，任意参数条件下，某个方法是否存在优于另一个明确有力的 baseline 的区间，且能给出明确理由？"

**A1 维度答案：不存在。** NDA-ML 块长 K 的自适应策略在当前场景（16APSK + 星地湍流 + 10-1000kHz 线宽）下：
- 无可实现判据能可靠预测最优 K（|ρ|<0.6 全部）
- 即使 oracle 上界也仅 -0.474 dB（去掉极端 1000kHz 后 -0.19 dB）
- 固定 K=16 是普适强 baseline（71% 场景跟 oracle 持平）

**A1 失败信号命中（adaptation-scan.md）：** "最优值不随条件变 → 无自适应空间"——部分命中：最优 K 确实随线宽变（E1 弱信号成立），但变化范围窄 + 判据无法捕捉 → 自适应无可实现空间。

## 下一步建议（供主线决策，不自行推进）

A1 FAIL 后，adaptation-scan 还有 A2/A3/A4 三个维度待扫：
- **A2 结构适配**：D002 已做（频域→时域），不能重复卖
- **A3 组合适配**：NDA 前馈无失锁 + DPLL 闭环高精度 → 混合（DPLL 异族 baseline 已立住，有数据基础）
- **A4 条件适配**：低 SNR DA 赢 / 高 SNR 强湍流 NDA 赢 → 切换（D005 数据有 crossover 信号）

A3/A4 比 A1 更可能出信号（方法级切换比参数级切换空间大）。但需用户确认是否继续 4 种适配扫描，还是转其他方向。
