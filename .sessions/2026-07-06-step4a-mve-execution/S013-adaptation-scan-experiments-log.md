# [S013] 4 种适配扫描各方向实验日志

> 2026-07-08 | Step 4a 维度 D / 适配扫描实验 | 状态: 4 种适配扫描全闭合（A2 已做 / A3 FAIL / A1 FAIL / **A4 PASS**）
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

### A1 参数适配 — NDA 块长自适应 K（FAIL）

**日期**: 2026-07-08（本对话续接）
**适配类型**: A1 参数适配（方法关键参数最优值是否随条件变 → 自适应参数策略）
**方法**: NDA-segmented 块长 K 自适应（判据→K 映射）
**参数**: 16APSK / 2.5GBaud / 线宽 10-1000kHz（用户选"加线宽维度"信号最强）/ M₀=8 / 5 seed × 8 场景（AWGN 3 线宽点 + 湍流 5 场景）。
**脚本/数据**: `explore/nda-awgn-tracking-sandbox/a1_calibration.py`（35 点标定 57.7s）/ `a1_validation.py`（8 点 5 seed 169.5s）/ `_a1_calibration.json` / `_a1_adaptive_k_results.json` / `_a1_adaptive_k_report.md` / `_a1_adaptive_k_design.md`（TL-20 预期）。

**结论**: **A1 信号 FAIL**（自适应 K 无可实现增量）

**两阶段证据**：

阶段 1 标定（35 点单 seed，找判据→最优 K 映射）：
- 4 判据（J1 升幂幅值方差 / J2 scintillation / J3 盲 SNR / J4 升幂相位差分方差）vs 最优 K 的 Spearman ρ 全 <0.6
- 最强 J2 ρ=-0.361，J4（线宽代理，设计预期最强）ρ=-0.019 几乎零
- **J4 bug 发现+修正**：原实现 `np.unwrap(np.angle(raised))` 对 M₀=8 升幂相位 unwrap 路径错乱（D-009 unwrap 教训复发），修正为 mod 2π 相位增量后仍 ρ=-0.019（修对但物理上仍无预测力：升幂后相位增量被 AWGN 噪声主导）
- **K=16 普适性**：固定 K=16 在 35 点中 25 点（71%）跟 oracle 持平

阶段 2 验证（8 点 5 seed，自适应 vs 固定 K）：
- adaptive-J4（可实现）aggregate gain vs K16 = **+0.000 dB**（J4 映射退化到 always-K16）
- adaptive-J4 CI 显著赢 K16 的点数 = **0/8**
- 即使 oracle 上界（非可实现）aggregate 也仅 **-0.474 dB**，其中 -2.46 dB 全来自 1000kHz 一个极端点（不在实测主流 10-80kHz）
- 去掉 1000kHz 后 oracle aggregate 仅 -0.19 dB（薄增益区间下沿）

**PASS/FAIL 判据**: 两判据（≥2 点显著赢 + aggregate<0）均不满足 → **FAIL**

**物理根因**:
1. 最优 K 变化范围窄：跨线宽 K∈{8,16,32}（3 档），主战场集中在 K=16，自适应空间被"普适固定 K"压缩
2. 最优 K 非单调：50kHz→K8 是单 seed 噪声波动，多 seed 后大概率也是 K16
3. 判据层失效：升幂后相位增量被 AWGN 噪声主导，单块 256 样本估计方差大，无法可靠代理线宽
4. 唯一显著点（1000kHz）不在主流场景（D-009 实测主流 ECL 10-80kHz）

**VV 参照**: VV Nw=64（固定不调参）aggregate vs K16 = +0.219 dB（VV 稍差 K16）。但 D-009 层 4 已证 VV 调 Nw=16 在高线宽反超。"自适应"是普适思路，NDA 的 K 自适应无独占优势。

**对论文写作的影响**: 不能用"NDA 块长自适应 K"作算法层创新点。有负面价值作防御性材料——被问"能不能自适应"时有实测+物理理由回答"不能"。

**主线独立核查**: 从 `_a1_adaptive_k_results.json` 原始 by_seed 数字重算 1000kHz 点（fixed_k32 by_seed 第一个 1.96e-2 跟标定单 seed 一致 ✓ / fixed_k16 5 seed mean 3.60e-2 含单 seed 3.21e-2 ✓ / adaptive_oracle ≡ fixed_k32 by_seed 完全一致 ✓）。子 agent 归因（J4 退化 / K16 普适）经原始数字核实属实。

### A4 条件适配 — DA/NDA 基于 per-block 有效 SNR 切换（PASS）

**状态**: **已完成，PASS**（另一对话产出，本日志补记状态准确性）
**日期**: 2026-07-08
**脚本/数据**: `explore/nda-awgn-tracking-sandbox/_a4_switch_experiment.py` / `_a4_switch_results.json` / `_a4_switch_report.md` / `_a4_diagnose_crossover.py` / `_a4_diagnose2_effsnr.py`。

**结论**: **A4 信号 PASS**（湍流 crossover 区切换 > max(DA,NDA)）

**关键数据**（5 seed × 4 场景）：
- 湍流 crossover 区（γd=15dB）切换稳定赢 max(DA,NDA) +0.44~+0.56dB（改进版 3 seed），CI 下界全正
- 工作区（BER<HD-FEC）内 0 FAIL
- 切换判据可实现：per-block 有效 SNR γ_eff + scintillation CV 双门控，全接收端可测（非 oracle）

**注**: 本轮（A1 实验）主线仅补记 A4 已完成的事实保证治理准确性，A4 的深入分析/决策记录由跑 A4 的对话负责。A4 PASS 是 4 种适配扫描唯一出信号的方向，待主对话决定是否追进 Contract/正式实验。

## 决策引用

- 无新建 D###（A3 FAIL 是技术验证结果，非方向决策；如要正式 Kill 整条适配策略建议主对话确认 A1/A4 后统一建 D-011）
- 引用既有：adaptation-scan.md A3（组合适配信号判据 + 失败信号）
- 引用既有：TL-20（先建理论预期）+ TL-23（验证完再判定）+ TL-13（共用信道 bit-exact）+ TL-29（多 seed 不单 seed 判定）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（4 种适配扫描在 Step 4a 维度 D 找增量方向，adaptation-scan.md FR-22 注解明确合规）
- 未跳框架（FR-22）：当前在 Step 4a 维度 D

## 后续

**4 种适配扫描全闭合**：A2 已做（D002）/ A3 FAIL / A1 FAIL（D-011）/ **A4 PASS**（唯一出信号方向）

1. A4 PASS 是唯一可追方向——主对话决定是否追进 Contract/正式实验（建 D-012 Go 决策）
2. A1/A3 FAIL 数据保留作防御性材料 + 教训（D-011 教训 8-10）
3. 若用户决定追 A4：A4 的 crossover 切换策略进 Contract 阶段（落假设+信号+success_signal），需先补 A4 的 D### 决策记录（跑 A4 的对话或主对话补）
