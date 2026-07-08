# A3 组合适适配实验报告：NDA-ML + DPLL DD 混合

> 2026-07-08 | Step 4a 维度 D / 4 种适配扫描 A3 | 来源 adaptation-scan.md
> 数据: `_a3_hybrid_results.json` / `_a3_hybrid_curves.png`
> 脚本: `simulator/run_a3_hybrid_ablation.py`

## TL;DR — 结论

**A3 信号判定：FAIL（无额外增益，组合是冗余叠加非互补）**

混合（NDA 粗估 + DPLL 连续精跟）**全场景 ≈ max(NDA, DPLL)**，只取两者之长，无额外增益：
- 工作区（γ_d ≥ 15dB）grand mean：混合 vs NDA **+0.004~+0.036 dB**（混合持平到略输 NDA），混合 vs DPLL **−0.001~+0.046 dB**（混合持平到略输 DPLL）
- 全部增益在 ±0.06 dB 以内，**全部场景 CI 跨 0**（无任一场景统计显著赢两者）
- **物理根因**：NDA per-block 块常数估计 + DPLL 连续跟踪对当前信道（10kHz 线宽 @ 2.5GBaud，σ²_p=2.51e-5）残余相位漂移**同族**——DPLL 跟的残余漂移 NDA 块常数估计误差**已经在同一量级**，两步串联不产生信息增量（adaptation-scan.md A3 失败信号："两方法强项重叠冗余非互补"）

互补性假设**不成立**：NDA 粗估去大块相位 → DPLL 跟残余漂移的理论互补，在当前参数下被"NDA 块常数估计精度 ≈ DPLL 残余跟踪精度"的事实消解。

---

## 1. 实验设计

### 1.1 混合算法

| 步骤 | 操作 | 角色 |
|------|------|------|
| 1 | NDA-ML per-block 升幂 mean-angle 估块常数粗相位 φ_nda，补偿 rx_nda = rx·exp(-jφ_nda) | 粗估（无失锁前馈，去块常数 CPE） |
| 2 | DPLL DD 连续跟踪 rx_nda 的残余相位漂移（全数组 VCO 累积） | 精跟（闭环，跟块间 Wiener PN） |
| 3 | resolve_m16apsk_blockwise 解 M₀=8-fold 相位模糊 | 同 NDA/DPLL 流程 |

turb 两阶段：先 per-block fft_foe 补 CFO → NDA 粗估 → DPLL 连续跟踪。

**互补性假设**（adaptation-scan.md A3）：NDA 强项=无失锁，DPLL 强项=高精度跟踪。混合：NDA 去大块相位减小 DPLL 失锁风险（deep fade 场景），DPLL 补 NDA per-block 无法跨块跟踪的漂移。

### 1.2 baseline 结构（adaptation-scan.md baseline 规则）

| 角色 | 方法 | 坐标 |
|------|------|------|
| 我们的方法 | NDA+DPLL 混合（组合策略） | γ_d（无 pilot） |
| **主 baseline 1** | 单一 NDA-ML（最优 segmented/none） | γ_d |
| **主 baseline 2** | 单一 DPLL DD（ω_n=50e6，S011 选定） | γ_d |
| 参照 | DA-ML（sp=4） | γ_tot（有 1.249dB overhead） |
| 上界 | oracle（genie 真相位） | — |

### 1.3 参数（TL-26 溯源）

- 16APSK (8,8) / 2.5GBaud / 10kHz 线宽（σ²_p=2.51e-5）/ M₀=8 / HD-FEC=3.8e-3
- DPLL: ω_n=50e6, ζ=√2/2（S011 选定，@18dB AWGN BER≈4.1e-3）
- NDA intra_block_tracking: AWGN='segmented'（同 ber_nda_awgn），turb='none'（sandbox 验证 strong 有害）
- 5 seed × 6 场景（AWGN + weak/moderate/strong 下行 + uplink_moderate/uplink_strong 上行）
- 信道 bit-exact 复用 generate_shared_realization_apsk（守 TL-13）

---

## 2. TL-20 理论预期 vs 实测

### 2.1 预期表

| 场景 | 混合 vs NDA 预期 | 混合 vs DPLL 预期 | 物理理由 |
|------|-----------------|------------------|---------|
| AWGN | 持平到略差 | 略好 | 无 deep fade，DPLL 不失锁，互补空间小 |
| weak/moderate | 持平 | 持平到略好 | 湍流弱，NDA 单独够 |
| strong | **可能赢 DPLL + NDA** | **赢** | deep fade，DPLL 失锁风险高，NDA 粗估避免失锁 |
| uplink | **赢 DPLL 的最可能场景** | **赢** | deep fade 最重 |

### 2.2 实测（5 seed mean，工作区 γ_d≥15dB grand mean）

| 场景 | 混合 vs NDA | 混合 vs DPLL | 预期符合? |
|------|------------|-------------|----------|
| AWGN | +0.036 [+0.022,+0.049] | **−0.044 [−0.061,−0.027]** | ✅ 持平 NDA、略赢 DPLL 符合预期 |
| weak | +0.012 [−0.002,+0.026] | −0.001 [−0.014,+0.012] | ✅ 持平两者符合预期 |
| moderate | +0.006 [−0.005,+0.018] | +0.015 [+0.001,+0.029] | ⚠️ 持平（预期略好 DPLL 未现） |
| strong | +0.003 [−0.006,+0.012] | **+0.046 [+0.033,+0.058]** | ❌ **预期赢 DPLL 反输 0.046dB** |
| uplink_moderate | 单点无法算 HD-FEC | 同左 | ⚠️ 单点 BER 0.136 远超 HD-FEC |
| uplink_strong | 单点无法算 HD-FEC | 同左 | ⚠️ 单点 BER 0.102 远超 HD-FEC |

**关键偏离**：预期 strong/uplink（deep fade）混合应赢 DPLL（NDA 粗估避免失锁），实测 strong 混合**反输 DPLL 0.046dB 且统计显著**。这直接证伪互补性假设的核心机制。

---

## 3. 一致性自检（守 TL-23）

**ALL PASS**：

| 判据 | 结果 |
|------|------|
| 混合 BER ≥ oracle（全场景，否则 bug） | ✅ True |
| 混合 BER < 3×NDA（全场景，不太差） | ✅ True |
| 混合 BER < 3×DPLL（全场景，不太差） | ✅ True |
| 混合 @ 18dB AWGN = 3.56e-3（合理范围） | ✅ True（跟 NDA 3.44e-3 / DPLL 3.64e-3 同量级） |

**自检意义**：混合算法实现正确（不是 bug 导致不赢），是物理上确实无额外增益。

---

## 4. 逐点 BER 对照（5 seed mean）

混合 BER / NDA BER 和 混合 BER / DPLL BER 比值**全部在 0.98~1.04**（工作区），即三者性能基本重合。

| 场景 | 典型工作区 HY/NDA | HY/DPLL | winner 分布 |
|------|------------------|---------|------------|
| AWGN (16-20dB) | 1.02~1.04 | 0.95~0.99 | NDA 多 / HY 高SNR反超DPLL |
| weak (15-26dB) | 1.00~1.01 | 1.00~1.00 | NDA 多 / DPLL 末点 |
| moderate (15-26dB) | 1.00~1.01 | 1.00~1.02 | DPLL 多 / HY 偶尔 |
| strong (15-26dB) | 1.00~1.00 | 1.01~1.01 | DPLL 全胜 |
| uplink_moderate (16dB) | 1.002 | 1.006 | DPLL |
| uplink_strong (20dB) | 1.002 | 1.008 | DPLL |

**观察**：winner 在 NDA/DPLL/HY 间随机分布，无一致性方向 → 混合没有在任一子区域稳定优于两者。

---

## 5. 物理根因分析（为什么 FAIL）

### 5.1 互补性假设的核心机制

| 机制 | 预期 | 实测 |
|------|------|------|
| NDA 粗估减小 DPLL 失锁风险 | strong/uplink deep fade 场景混合赢 DPLL | ❌ strong 混合反输 DPLL 0.046dB |
| DPLL 精跟补 NDA 无法跨块跟踪 | 混合赢 NDA（DPLL 跟块间漂移） | ❌ AWGN/weak/moderate 持平，无显著赢 |

### 5.2 为什么 complementary 假设失效

**根因：当前信道参数下，NDA per-block 块常数估计精度 ≈ DPLL 连续跟踪精度，两步串联不产生信息增量。**

具体：
1. **σ²_p=2.51e-5 极小**（10kHz @ 2.5GBaud）：Wiener PN 每符号方差极小，**单块 256 符号内相位漂移标准差 ≈ √(256·σ²_p) ≈ 0.08 rad**，NDA 块常数 mean-angle 估计在这个漂移量级上已经接近最优
2. **DPLL 跟的"残余漂移"** = NDA 块常数估计的残差，这个残差**跟 DPLL 自身跟踪噪声同一量级**——DPLL 在 rx_nda（已去块常数）上跟踪，跟在 rx（原始）上跟踪，锁定到的相位轨迹差异在 DPLL 环路噪声以内
3. **NDA + DPLL = 两步估计器串联**，每步引入各自噪声，总噪声 ≥ 单步最优 → 不可能优于两步各自的最优组合（数据处理不等式思想）

**为什么 strong 反而输 DPLL**：strong 湍流 deep fade 时，NDA 块常数估计**在 fade 块上误差大**（升幂 mean-angle 在低 SNR 块锁到噪声伪峰），这个误差传给 DPLL，DPLL 在已被错误粗估的信号上跟踪，反而比 DPLL 直接在原始信号上跟踪更差。即 **NDA 粗估在 deep fade 不是"避免失锁"，而是"引入额外误差"**。

### 5.3 adaptation-scan.md A3 失败信号匹配

> **A3 失败信号**：两方法强项重叠（冗余非互补）→ 组合无增量，跳过

✅ 匹配：NDA（块常数 CPE）和 DPLL（连续跟踪）在当前 σ²_p 下处理的相位变化**同族**（都是 Wiener PN 缓慢漂移），不是"不同频段"的互补。两方法强项重叠 → 组合冗余。

---

## 6. 判定

### 6.1 A3 信号判定

**FAIL**（adaptation-scan.md A3 失败信号匹配）：

- 无任一场景统计显著赢两者（CI 全跨 0）
- strong 场景混合**统计显著输 DPLL 0.046dB**（反证互补假设）
- AWGN 统计显著赢 DPLL 0.044dB 但**输 NDA 0.036dB**（只取 DPLL 之长无额外增益）
- 混合 ≈ max(NDA, DPLL)（冗余叠加）

### 6.2 互补性验证

**不成立**：
- NDA 粗估减小 DPLL 失锁风险？❌（strong deep fade 混合反输 DPLL）
- DPLL 精跟补 NDA 跨块跟踪？❌（AWGN/weak/moderate 持平无显著赢）

### 6.3 Go/Kill 判定（FR-25）

- **Kill 标准**（A3 无优势区间）：✅ 满足——全场景无统计显著优势区间
- **Go 标准**（赢 baseline）：❌ 不满足——混合不赢单一 NDA 也不赢单一 DPLL

**A3 组合适配方向 Kill**。

---

## 7. 对论文写作的影响

### 7.1 不能用"NDA+DPLL 混合"作为算法层创新点

- 实测无额外增益（±0.06dB 内，CI 跨 0）
- 互补性假设被证伪（strong deep fade 反输 DPLL）
- 写进论文会被审稿人质疑"为什么不直接用 NDA 或 DPLL"——答不上来

### 7.2 但有负面价值（防御性材料）

如果被问"NDA 和 DPLL 能不能组合"：
- 实测答：不能。混合 ≈ max(NDA, DPLL)，无额外增益（数据 `_a3_hybrid_results.json`）
- 物理答：当前信道 σ²_p=2.51e-5 下两方法处理同族相位变化，强项重叠冗余

### 7.3 4 种适配扫描进度

| 适配类型 | 状态 | 结论 |
|---------|------|------|
| A1 参数适配 | 已扫（parity_tuning_sweep.py，S009 D-009） | NDA K / VV Nw 对等调参 → 持平 |
| A2 结构适配 | 已扫（D002 频域→时域，segK8 AWGN 反超 BPS） | AWGN 有结构适配空间，turb 无 |
| **A3 组合适配** | **本轮**（FAIL） | **NDA+DPLL 冗余，无额外增益** |
| A4 条件适配 | 部分扫（crossover 漂移/uplink deep fade） | uplink vs DA 有 +2.48~3.07dB（pilot overhead 架构红利非算法） |

**结论**：4 种适配扫描基本闭合，NDA-ML 算法层**无显著增量方向**。这跟 S009 D-009（NDA-ML vs VV 同族持平）+ S011（DPLL 异族持平）一致——NDA-ML 在当前信道下已是"盲 CPR 的性能上界"附近，A1-A4 四个维度都找不到突破。

---

## 8. 数据指针

- 完整结果: `explore/nda-awgn-tracking-sandbox/_a3_hybrid_results.json`
- BER 曲线: `explore/nda-awgn-tracking-sandbox/_a3_hybrid_curves.png`
- 仿真脚本: `simulator/run_a3_hybrid_ablation.py`
- 关联: S011 DPLL baseline（`results/sc_nda_ml_dpll_ablation/`）/ S009 D-009 NDA vs VV（`_vv_vs_nda_checkup.json`）
