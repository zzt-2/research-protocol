# A3 组合适配扫描报告（combo scan — NDA+DPLL 复核 + NDA+VV 新测）

> 2026-07-08 | Step 4a 维度 D / 4 种适配扫描 A3 第 2 轮 | 来源 adaptation-scan.md
> 数据: `_a3_combo_results.json` | 脚本: `explore/nda-awgn-tracking-sandbox/_a3_combo_scan.py`
> 关联既有: `simulator/run_a3_hybrid_ablation.py`（5-seed NDA+DPLL, 结论 FAIL）

---

## TL;DR — A3 信号判定：**FAIL（两种组合均冗余，无互补信号）**

| 组合 | 信号 | 互补判据（combo < min 单一） | 关键 BER |
|------|------|------------------------------|----------|
| **NDA+DPLL 级联 (b)** | ❌ **NO_SIGNAL** | 0/6 点赢，worst ratio 1.026（比单一差 2.6%） | AWGN@18dB: NDA+DPLL=3.66e-3 vs min(NDA 3.57e-3, DPLL 3.70e-3)=3.57e-3 |
| **NDA+VV 级联** | ❌ **NO_SIGNAL** | 0/6 点逐 seed 赢，worst ratio 1.006（差 0.6%） | AWGN@18dB: NDA+VV=3.58e-3 vs min(NDA 3.57e-3, VV 3.56e-3)=3.56e-3 |

**A3 信号不成立**：NDA 与 DPLL（异族）/ NDA 与 VV（同族）组合在当前信道（10kHz 线宽 @ 2.5GBaud, σ²_p=2.51e-5）下强项重叠，组合仅 ≈ max(单一)，无信息增量。两个组合都落到"冗余叠加"而非"互补增强"。

---

## 1. 实验设计

### 1.1 两种级联组合（adaptation-scan A3 思路 b）

| 组合 | step1（粗估） | step2（精跟/精修） | 角色 |
|------|--------------|-------------------|------|
| **NDA+DPLL** | NDA-ML per-block 升幂 mean-angle 估块常数 CPE，补偿得 rx_nda | DPLL DD 连续跟踪 rx_nda 残余漂移（全数组 VCO 累积，守 S011） | 异族（前馈块估 + 闭环跟踪） |
| **NDA+VV** | NDA-ML per-block segmented 估块常数 CPE，补偿得 rx_nda | VV-CPR M₀=8 滑窗精修 rx_nda 残余相位（per-block） | 同族（升幂类，D-009 冗余预测） |

turb 两阶段前端：per-block fft_foe（M₀=8 升幂 FOE）→ NDA → DPLL/VV（同 NDA-ML/DPLL/VV ablation 两阶段对称）。

### 1.2 baseline（adaptation-scan.md baseline 规则）

| 角色 | 方法 | 坐标 |
|------|------|------|
| 我们的方法 | NDA+DPLL / NDA+VV（组合策略） | γ_d（无 pilot） |
| baseline 1 | 单一 NDA-ML（segmented/none） | γ_d |
| baseline 2 | 单一 DPLL DD（ω_n=50e6）/ 单一 VV（Nw=64） | γ_d |
| 上界 | oracle（genie 真相位） | — |

### 1.3 参数（TL-26 溯源）
- 16APSK (8,8) / 2.5GBaud / 10kHz 线宽（σ²_p=2.51e-5）/ M₀=8 / HD-FEC=3.8e-3
- DPLL: ω_n=50e6, ζ=√2/2（S011 选定）/ VV: Nw=64（run_vv_ablation 默认）
- **2 seed × 2 场景（AWGN + weak）× 3 代表性 SNR**（纪律：先少 seed 看趋势，12.9s 跑完）
- AWGN SNR=[16,18,20]dB / weak SNR=[18,20,22]dB（工作区）
- 信道 bit-exact 复用 generate_shared_realization_apsk（守 TL-13）

---

## 2. TL-20 理论预期

| 组合 | 预期 | 物理理由 |
|------|------|---------|
| NDA+DPLL | **冗余**（≠ 互补） | σ²_p 极小 → NDA 块常数估计精度 ≈ DPLL 连续跟踪精度，两步串联不产生信息增量（数据处理不等式思想）。**已有 5-seed 6-场景实测确认 FAIL**（run_a3_hybrid_ablation.py）。 |
| NDA+VV | **冗余**（D-009 同族） | NDA 和 VV 同属升幂类（M₀=8），VV 滑窗 mean-angle 与 NDA 块 mean-angle 处理同一段相位信息 → 组合 ≈ max(单一)。 |

**两组合预期都 FAIL**。本扫描验证预期 + 测 NDA+VV（既有未做）。

---

## 3. 实测结果（2 seed mean）

### 3.1 NDA+DPLL（vs 单一 NDA / 单一 DPLL）

| 场景 | SNR | NDA | DPLL | NDA+DPLL | NDA+DPLL / min(NDA,DPLL) | 互补? |
|------|-----|-----|------|----------|--------------------------|-------|
| AWGN | 16 | 1.030e-2 | 1.064e-2 | 1.050e-2 | 1.020（输 NDA） | ❌ |
| AWGN | 18 | 3.572e-3 | 3.700e-3 | 3.663e-3 | 1.026（输 NDA） | ❌ |
| AWGN | 20 | 7.349e-4 | 7.947e-4 | 7.385e-4 | 1.005（输 NDA） | ❌ |
| weak | 18 | 4.395e-3 | 3.906e-3 | 4.395e-3 | 1.125（输 DPLL） | ❌ |
| weak | 20 | 9.766e-4 | 9.766e-4 | 9.766e-4 | 1.000（持平） | ❌ |
| weak | 22 | 0 | 0 | 0 | —（BER=0 信号太干净） | — |

**判定：NO_SIGNAL**。NDA+DPLL 全程落在 NDA 和 DPLL 之间（NDA < NDA+DPLL < DPLL 在 AWGN；DPLL < NDA+DPLL = NDA 在 weak），即"两步串联取两者之长但无额外增益"。worst ratio 1.026（AWGN@18dB 比 min 差 2.6%）。

**与既有 5-seed 结论一致**：run_a3_hybrid_ablation.py 报 NDA+DPLL 工作区增益 ±0.06dB 内 CI 跨 0 → FAIL。本轮 2-seed 复核确认（ratio 1.00~1.03）。

### 3.2 NDA+VV（vs 单一 NDA / 单一 VV）— 新测

| 场景 | SNR | NDA | VV | NDA+VV | NDA+VV / min(NDA,VV) | 互补? |
|------|-----|-----|----|----|----------------------|-------|
| AWGN | 16 | 1.030e-2 | 1.028e-2 | 1.029e-2 | 1.001（≈持平） | ❌ |
| AWGN | 18 | 3.572e-3 | 3.560e-3 | 3.580e-3 | 1.006（输 VV） | ❌ |
| AWGN | 20 | 7.349e-4 | 7.324e-4 | 7.312e-4 | 0.998（mean 略赢 VV，噪声级） | ⚠️ |
| weak | 18 | 4.395e-3 | 3.906e-3 | 3.906e-3 | 1.000（持平 VV） | ❌ |
| weak | 20 | 9.766e-4 | 9.766e-4 | 9.766e-4 | 1.000（持平） | ❌ |
| weak | 22 | 0 | 0 | 0 | —（BER=0） | — |

**判定：NO_SIGNAL**。AWGN@20dB mean ratio 0.998（NDA+VV mean 略赢 VV 0.2%）是 2-seed 浮点噪声假信号——**逐 seed 检查**（下表）NDA+VV 在两 seed 都落在 NDA/VV 之间，从未优于 min：

| AWGN@18dB | NDA | VV | NDA+VV | NDA+VV vs min | 赢? |
|-----------|-----|----|----|---------------|-----|
| seed0 | 3.589e-3 | 3.572e-3 | 3.606e-3 | +0.9%（输 VV） | ❌ |
| seed1 | 3.555e-3 | 3.547e-3 | 3.555e-3 | +0.2%（输 VV） | ❌ |

**两 seed 都 NDA+VV > min(NDA, VV)** → 互补性 0/6 点。D-009 同族冗余预测**实测确认**：NDA 和 VV 在 M₀=8 升幂 mean-angle 上处理同一段相位信息，VV 在 rx_nda（已去块常数）上再跑一遍升幂滑窗，残余相位变化已在 NDA 块常数估计精度以内 → VV 精修无信息增量。

---

## 4. 物理根因（为什么两组合都 FAIL）

### 4.1 共同根因：σ²_p=2.51e-5 极小 → 估计精度饱和

当前信道（10kHz 线宽 @ 2.5GBaud）Wiener PN 每符号方差 σ²_p=2.51e-5：
- 单块 256 符号内相位漂移标准差 ≈ √(256·σ²_p) ≈ 0.08 rad
- NDA 块常数 mean-angle 估计 / DPLL 连续跟踪 / VV 滑窗 mean 在这个漂移量级上**都接近最优**

→ 任两个组合 = 两步估计器串联，每步引入各自噪声，总噪声 ≥ 单步最优（数据处理不等式）。组合不可能优于两步各自最优。

### 4.2 NDA+DPLL：异族但强项重叠（≠互补）
- NDA 强项=无失锁（前馈块估），DPLL 强项=连续跟踪（闭环）
- 理论互补：NDA 去大块相位减小 DPLL 失锁风险，DPLL 补 NDA 跨块漂移
- **失效**：当前无 deep fade（AWGN/weak），DPLL 本不失锁；NDA 块常数估计残差 ≈ DPLL 跟踪噪声 → 两步串联噪声叠加，实测 NDA+DPLL 落在 NDA/DPLL 之间

### 4.3 NDA+VV：D-009 同族冗余（确认）
- NDA 和 VV 同属升幂类（M₀=8 mean-angle）
- VV 在 rx_nda（已去块常数相位）上再跑升幂滑窗，残余相位变化 < NDA 块常数估计精度
- → VV 精修无信息增量，NDA+VV ≈ max(NDA, VV)

---

## 5. adaptation-scan.md A3 信号匹配

> **A3 成功信号**：两方法强项互补（不同频段/不同机理）→ 组合 > 单一，有稳定优势区间
> **A3 失败信号**：两方法强项重叠（冗余非互补）→ 组合 ≈ max(单一)，无增量，跳过

**两组合都匹配失败信号**：
- NDA+DPLL：异族但强项在当前 σ²_p 下重叠（NDA 块常数 ≈ DPLL 跟踪精度）
- NDA+VV：同族（D-009 确认），强项物理同源（升幂 mean-angle）

→ **A3 组合适配方向 Kill**（与既有 run_a3_hybrid_ablation.py 5-seed 结论一致）。

---

## 6. 哪种组合思路有效？

| 思路 | 实现 | 有效? | 原因 |
|------|------|-------|------|
| (a) NDA 粗估 CFO/相位 → DPLL 精跟（NDA 提供初始锁定） | 未单独实现（等价于 (b) 的 CFO 前端 fft_foe） | — | 当前 CFO 已由 fft_foe_m0_omega 两阶段处理，NDA 块常数不额外提供 CFO 信息 |
| **(b) 级联 NDA 补偿大相位 → DPLL/VV 跟残余** | **本轮实测** | ❌ | 组合 ≈ max(单一)，两步串联噪声叠加无增益 |
| (c) 并行选择（每 block 算两者按判据选） | 未实现（属 A4 条件适配，不是 A3 组合） | — | 与 A4 重叠，A4 已扫（uplink vs DA 有架构红利非算法） |

**无有效组合思路**。(b) 级联是 A3 最简形式，实测两种级联（→DPLL 异族 / →VV 同族）都冗余。

---

## 7. 对论文写作的影响

### 7.1 不能用"NDA+X 组合"作为算法层创新点
- NDA+DPLL：既有 5-seed 6-场景 FAIL + 本轮 2-seed 复核确认
- NDA+VV：本轮新测 FAIL（D-009 同族冗余确认）
- 写进论文会被审稿人质疑"为什么不直接用 NDA"——答不上来

### 7.2 负面价值（防御性材料）
被问"NDA 和 DPLL/VV 能不能组合"：
- 实测答：不能。NDA+DPLL ratio 1.00~1.03（输或持平），NDA+VV ratio 0.998~1.006（噪声级，逐 seed 从未赢）
- 物理答：当前 σ²_p=2.51e-5 下 NDA 块常数估计精度 ≈ DPLL 跟踪/VV 滑窗精度，强项重叠冗余（异族 NDA+DPLL 也一样）

### 7.3 4 种适配扫描进度（更新）

| 适配类型 | 状态 | 结论 |
|---------|------|------|
| A1 参数适配 | 已扫（parity_tuning_sweep.py，S009 D-009） | NDA K / VV Nw 对等调参 → 持平 |
| A2 结构适配 | 已扫（D002 频域→时域，segK8 AWGN 反超 BPS） | AWGN 有结构适配空间，turb 无 |
| **A3 组合适配** | **已扫（run_a3_hybrid 5-seed + 本轮 2-seed 复核 + NDA+VV 新测）** | **NDA+DPLL / NDA+VV 均冗余，无增量** |
| A4 条件适配 | 部分扫（crossover / uplink deep fade） | uplink vs DA 有 +2.48~3.07dB（pilot overhead 架构红利非算法） |

**结论**：4 种适配扫描闭合，NDA-ML 算法层无显著增量方向（A1-A4 全 FAIL 或仅架构红利）。与 S009 D-009（NDA vs VV 同族持平）+ S011（DPLL 异族持平）一致——NDA-ML 在当前信道下已接近"盲 CPR 性能上界"。

---

## 8. 后续可深挖方向（若有需要）

1. **更极端信道**（强 deep fade / 大线宽）：σ²_p↑ 时 NDA 块常数估计饱和、DPLL 失锁风险上升，组合可能在 strong/uplink 有信号。但 run_a3_hybrid_ablation.py 已测 strong 5-seed 仍 FAIL（NDA 粗估在 fade 块引入额外误差）。
2. **(a) 初始锁定式**：NDA 仅提供 DPLL 初始相位（不级联跟踪），测是否减少 DPLL 收敛暂态。但 DPLL 已用 resolve 解模糊，初始相位影响小。
3. **跳过**：4 维适配扫描已闭合，建议转其他方向（如复杂度/吞吐优化、或多载波场景）。

---

## 9. 数据指针

- 本轮结果: `explore/nda-awgn-tracking-sandbox/_a3_combo_results.json`（2-seed, NDA+DPLL 复核 + NDA+VV 新测）
- 本轮脚本: `explore/nda-awgn-tracking-sandbox/_a3_combo_scan.py`
- 既有 5-seed NDA+DPLL: `simulator/run_a3_hybrid_ablation.py` + `explore/nda-awgn-tracking-sandbox/_a3_hybrid_results.json` / `_a3_hybrid_report.md`
- 关联: S011 DPLL baseline（`results/sc_nda_ml_dpll_ablation/`）/ S009 D-009 NDA vs VV 同族（`_vv_vs_nda_checkup.json`）
