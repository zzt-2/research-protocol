# [S013] 4 种适配扫描各方向实验日志

> 2026-07-08 | Step 4a 维度 D / 适配扫描实验 | 状态: 进行中（A3 已 FAIL，A1/A4 待返回）
> 来源: S012（4 种适配方法论 + 3 并行实验派发）续接

## 目标

记录 4 种适配扫描（adaptation-scan.md A1/A2/A3/A4）各方向实验的结果与判定。本日志是**各方向实验的聚合记录**，后续别的方向（A1 参数自适应 / A4 条件切换 / 其他）都追加到这里，不另开 S###。

## 记录

### A3 组合适配 — NDA-ML + DPLL DD 混合（FAIL）

**日期**: 2026-07-08
**适配类型**: A3 组合适配（不同族方法能否组合 + 互补性在哪）
**混合算法**: NDA-ML per-block 升幂 mean-angle 估块常数粗相位 → DPLL DD 连续跟踪残余漂移（全数组 VCO 累积）→ resolve M₀-fold 模糊。turb 两阶段先 per-block fft_foe 补 CFO。
**参数**: 16APSK / 2.5GBaud / 10kHz（σ²_p=2.51e-5）/ M₀=8 / DPLL ω_n=50e6（S011 选定）/ 5 seed × 6 场景（AWGN + weak/moderate/strong 下行 + uplink_moderate/uplink_strong 上行）。
**脚本/数据**: `simulator/run_a3_hybrid_ablation.py` / `explore/nda-awgn-tracking-sandbox/_a3_hybrid_results.json` / `_a3_hybrid_report.md` / `_a3_hybrid_curves.png`。

**结论**: **A3 信号 FAIL**（无额外增益，组合是冗余非互补）

**关键数据**（工作区 γ_d≥15dB grand mean，5 seed 95% CI）：

| 场景 | 混合 vs NDA | 混合 vs DPLL |
|------|------------|-------------|
| AWGN | +0.036 [+0.022,+0.049]（混合输 NDA，显著） | −0.044 [−0.061,−0.027]（混合赢 DPLL，显著） |
| weak | +0.012 [−0.002,+0.026]（持平） | −0.001 [−0.014,+0.012]（持平） |
| moderate | +0.006 [−0.005,+0.018]（持平） | +0.015 [+0.001,+0.029]（持平） |
| strong | +0.003 [−0.006,+0.012]（持平） | **+0.046 [+0.033,+0.058]（混合输 DPLL，显著）** |
| uplink | 单点 BER 0.10~0.14 远超 HD-FEC，无法算 gain | 同左 |

**TL-20 一致性自检 ALL PASS**：混合 ≥ oracle / < 3×NDA / < 3×DPLL / @18dB AWGN=3.56e-3 合理 → 实现正确，物理上确实无增量。

**互补性假设证伪**：
- 预期 strong/uplink deep fade 混合赢 DPLL（NDA 粗估避免失锁）→ 实测 strong 混合**统计显著输 DPLL 0.046dB**
- 物理根因：NDA 在 fade 块上估计误差大，传给 DPLL 后反而比 DPLL 直接跟踪原始信号更差——"避免失锁"变成"引入额外误差"
- AWGN 赢 DPLL 0.044dB 但输 NDA 0.036dB，只是取两者之长无额外增益

**物理根因**：当前信道 σ²_p=2.51e-5（10kHz@2.5GBaud）极小，单块 256 符号内 Wiener PN 漂移标准差 ≈ 0.08 rad，NDA 块常数 mean-angle 已接近最优；DPLL 跟的残余漂移跟自身环路噪声同一量级 → 两步串联无信息增量。匹配 adaptation-scan.md A3 失败信号"两方法强项重叠冗余非互补"。

**对论文写作的影响**：不能用"NDA+DPLL 混合"作算法层创新点（实测无额外增益 + 互补证伪）。但有负面价值作防御性材料——被问"能不能组合"时有实测 + 物理理由回答"不能"。

### A1 参数适配 — NDA K / VV Nw 自适应（待返回）

**状态**: 已在 S009 D-009 扫过对等调参（parity_tuning_sweep.py），NDA K / VV Nw 对等调参全场景持平。"自适应 K > 固定 K"实验提示词已给用户，待新对话返回。

### A4 条件适配 — DA/NDA 条件切换（待返回）

**状态**: 部分信号已扫——fair_gain 随湍流递增（1.35→1.71→uplink 更强），但 +dB 主要是 pilot overhead 架构红利非算法。"DA/NDA 条件切换 > 单一方法全 SNR"实验提示词已给用户，待新对话返回。

## 决策引用

- 无新建 D###（A3 FAIL 是技术验证结果，非方向决策；如要正式 Kill 整条适配策略建议主对话确认 A1/A4 后统一建 D-011）
- 引用既有：adaptation-scan.md A3（组合适配信号判据 + 失败信号）
- 引用既有：TL-20（先建理论预期）+ TL-23（验证完再判定）+ TL-13（共用信道 bit-exact）+ TL-29（多 seed 不单 seed 判定）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（4 种适配扫描在 Step 4a 维度 D 找增量方向，adaptation-scan.md FR-22 注解明确合规）
- 未跳框架（FR-22）：当前在 Step 4a 维度 D

## 后续

1. A1 / A4 实验结果返回后追加到本日志对应段落（不另开 S###）
2. 若 A1/A4 也 FAIL → 4 种适配扫描全闭合，NDA-ML 算法层无显著增量方向确认，需回主对话想别的方向
3. 若 A1/A4 任一 PASS → 追该方向，建 D-011 记录 Go 决策
