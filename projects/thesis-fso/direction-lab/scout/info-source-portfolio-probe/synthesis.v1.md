# Information-Source Portfolio Probe — Synthesis v1

> 2026-07-22 | S012 / D020 / V009 | 独立 verifier CONFIRM (no P0; 1 P1 documented)
> Governed by D019/H012 + probe-contract.v1.yaml. Three headroom/observability Probes on the
> canonical 11-cell 16QAM dual-pol OSL atlas × fresh disjoint test seeds [141-150].

## TL;DR

四族信息来源（channel-model prior / sparse pilot / causal history / decoder-soft）中，**两族通过
headroom + observability 双门（F1-A model prior、F3-A causal history），一族是 BOUNDARY（F4-A decoder-soft：
headroom 存在但薄且 smoothing-fragile + 可部署版需 coded chain），一族待撞车核查（F2 pilot）。**
本轮最值得形成方法的是 **F1-B：可部署 model-based tracker**（dual-pol GG/SOP 状态估计 → MMSE 均衡），
其 oracle 上界（F1-A）显示 0.133 macro PI-SER headroom（远超 0.03 阈值，是 D018 blind-router 0.0037 的 36×），
且 receiver-visible observability 强相关（|r|=0.65）。

## 各 Probe 结果（独立 verifier 逐数字重算 bit-identical）

### F1-A — channel-model prior oracle headroom → PASS（headroom + observability）

| 指标 | 值 | 阈值/参照 |
|---|---|---|
| macro CMA PI-SER | 0.2959 | fixed-μ=0.03 anchor |
| macro oracle MMSE PI-SER | 0.1630 | scoring-only（真 h, θ + TX-truth calib）|
| **macro headroom** | **+0.1329** | ≥ 0.03 → PASS |
| headroom CI | [+0.078, +0.196] | lo > 0 |
| collapse 子集 headroom | +0.152 (7 cells, 61/110 realizations) | — |
| **max receiver-visible corr** | **\|r\|=0.651** | ≥ 0.1 → observability confirmed |
| 最强相关特征 | z_amp_mean / cm_error_final | — |

**科学含义**：用真信道状态（per-block h, θ → 精确 Jones → per-block MMSE）能关闭 0.133 PI-SER 余量，
这是 model-based tracker 的**上界**。关键是 receiver-visible 的 CMA trace 特征（z_amp、cm_error）与该
headroom 强相关（|r|=0.65），意味着 headroom 不只是噪声——deployable tracker 有合理机会从 receiver-visible
信号恢复部分状态信息。这**根本不同于** D018 的 blind-router（同类盲专家 oracle headroom 仅 0.0037，因为
MMA/DD-LMS 与 CMA 失效相关）。model-based tracker 用的是**不同信息源**（信道模型先验），不是换盲 cost。

### F3-A — causal temporal history information increment → PASS（conditional information）

| 指标 | 值 | 阈值 |
|---|---|---|
| max MI(block-0 features, collapse) | 0.000 bits | — |
| max MI(history features, collapse) | 0.060 bits | — |
| **MI increment (history − block-0)** | **+0.060 bits** | > 0.01 → PASS |
| best R²(block-0 → pi_ser) | 0.000 | — |
| best R²(history → pi_ser) | 0.036 (cm_error_trend) | — |
| **R² increment** | **+0.036** | > 0 → PASS |

**科学含义**：过去 block 的 CMA trace 统计量（特别是 cm_error 的趋势）对当前 realization 的 collapse/pi_ser
提供超出 block-0 的条件信息（+0.06 bits MI，+0.036 R²）。历史**确实增加信息**，不是 RNN 假设。但增量较小
（MI 0.06 bits < 1 bit），是次级信号，不如 F1-A 的 headroom 强。这与 H066"collapse 在 block-0 决定"不矛盾——
block-0 决定的是 collapse flag，历史增加的是对 pi_ser 幅度的预测力。

### F4-A — corrected soft/GMI oracle headroom → BOUNDARY（thin + fragile + infra-blocked）

| 指标 | 值 | 说明 |
|---|---|---|
| macro analytic GMI headroom | **+0.0089** bits/sym | CI lo +0.0041（>0）|
| macro histogram-MI GMI headroom | −0.021 | **scale-invariant（复现 C12 artifact）**|
| analytic scale-sensitive | True | 真上界 |
| histogram scale-sensitive | **False** | artifact 确认 |
| **smoothing 敏感性** | sm=2:+0.033, sm=8:+0.009, sm=32:+0.002 | **fragile（verifier P1）**|

**科学含义**：修正 C12 scale-artifact 后，analytic GMI 显示**很小且 smoothing-fragile** 的正 headroom（+0.009）。
histogram-MI 完全复现了 C12 artifact（scale-invariant）。verifier 独立确认：headroom 在 smoothing=32 时 CI 跨 0，
集中在低 SNR cells。这是**边界结果**，不是稳定 soft-info bound。deployable F4-B 需要 coded chain
（INFRASTRUCTURE_BLOCKED，无 FEC chain）。**不建 F4-B**，除非用户授权 coded chain 基建且先解决 smoothing 依赖。

### F2 — sparse/adaptive pilot → 撞车核查未跑（本轮范围外）

F2-A 需先做撞车核查（JLT 2023 / OE 2021 三-pilot RSOP / LCOMM 2026 / TCOM 2025 / JLT 2022-23 全是直接竞品）。
本轮 contract 只冻结了 F1-A/F3-A/F4-A 三个 headroom Probe（F2 的撞车核查是文献工作，需子 agent）。
p03 已确认 pilot→Jones→inverse→pre-CMA 微变体与旧 U05/U36/U52 机械等价（COLLISION）。F2 只有在改变
overhead/scheduling/causal state estimation/recovery 机制时才 distinct。

## 统一排序（8 维，Probe 后真实数据）

| 候选 | headroom | observability | 物理 | comparator | 基建 | 撞车 | 论文 | 可逆 | 结论 |
|------|----|----|----|----|----|----|----|----|----|
| **F1-B deployable tracker** | **0.133 (上界)** | **0.65** | rel | fixed-μ+blind_affine | MULTI_DAY | 中(EKF 非占位) | **主结果** | 高 | **首选 Scout** |
| F1-A oracle bound (done) | 0.133 | scoring | — | fixed-μ | DONE | 低 | 上界材料 | — | DONE |
| F3-B multi-block KF | +0.06 MI | 0.036 R² | rel | per-block blind | HALF_DAY | 中(与F1-B重叠) | 次级 | 高 | 次选 |
| F3-A history Probe (done) | +0.06 MI | done | — | block-0 | DONE | 低 | 方法论 | — | DONE |
| F4-B coded receiver loop | +0.009 GMI (fragile) | thin | coded BER | uncoded | **BLOCKED** | 中 | 主(若 coded) | 中 | 不建(需基建) |
| F4-A soft Probe (done) | +0.009 | boundary | — | max-log | DONE | 低 | 负面材料 | — | DONE |
| F2-A pilot overhead curve | ? | 模拟 | overhead≤10% | blind | SMALL | **高** | 次级/负面 | 中 | 需先撞车核查 |

## 自动推进决策（不逐个问用户）

依 contract verdict_criteria + 提示词 §六 自动规则：

1. **F1-A PASS（headroom + observability）→ 授权考虑 bounded Scout**。F1-B 是 MULTI_DAY 基建（约一天），
   **不在本轮直接建**（提示词：最强候选需约一天新基建时，完成所有轻量 Probe 后统一向用户报告投资选择）。
2. **F3-A PASS（conditional information）→ F3-B 是 HALF_DAY，可作为 F1-B 的次级组件**（多 block KF 用 GG AR(1) ρ）。
3. **F4-A BOUNDARY（thin + fragile + infra-blocked）→ 不建 F4-B**。记为负面/边界材料。
4. **F2 撞车核查未做 → 不进 F2 任何候选**，除非用户要求先做撞车核查。
5. **四族未全部无 headroom** → 不进入"全部无解"战略裁决。

**本轮不直接实现完整 EKF/particle filter**（提示词明禁）；不一次性建 pilot/coded chain/tracker 全部基建；
不复活 blind-expert router；不把 F4-A 的 fragile +0.009 当稳定 bound。

## ML 真实信息增量判断

- **F1（model prior）有真实信息增量**：oracle headroom 0.133 是用**不同信息源**（信道模型先验）关闭的，
  不是换盲 cost。receiver-visible observability |r|=0.65 证明该信息部分可从 CMA trace 恢复。
- **F3（history）有真实但小的信息增量**：+0.06 bits MI，历史确实增加条件信息。
- **F4（decoder/soft）信息增量存疑**：analytic +0.009 但 smoothing-fragile，可能部分是 per-symbol 噪声过拟合。
- 这与 D018 的"blind experts 失效相关"形成对照：**新增合法信息（model prior / history）确实能打破相关盲失效**，
  证明问题不是"所有接收方法无解"，而是"blind 同类专家无互补结构"。

## 可写进毕业论文的材料

**主结果（待 Scout 验证）**：F1-B model-based tracker 在 OSL GG+SOP 下相对公平传统 baseline 的 PI-SER 改善
（上界 0.133；deployable 版本的实际增益待 Scout）。这是首轮 SCIENCE_SCOUT campaign 中**第一个有合法 headroom
+ observability 双通过的正面方法候选**。

**次级结果**：
- F3-A 历史信息增量（+0.06 bits MI）——多 block 因果状态估计的方法论可行性。
- F1-A/F3-A 的 receiver-visible observability 分析（CMA trace 特征与 headroom 的相关性）。

**负面/边界材料**：
- F4-A decoder/soft 族：analytic GMI headroom 薄且 smoothing-fragile；histogram-MI 复现 C12 scale-artifact
  （方法论教训：scale-invariant 估计器不能当上界）。
- D018（前置）：blind 同类 FIR 专家路由无互补结构（headroom 0.0037）。
- D017（前置）：task-mismatched 专家 + 污染 seeds 制造假互补。

## 下一步投资选择（交用户决策）

本轮完成所有轻量 Probe 后，**统一向用户报告投资选择**（提示词 §六）：

| 选项 | 内容 | 成本 | 风险 | 预期产出 |
|---|---|---|---|---|
| **A（推荐）** | F1-B bounded Scout：dual-pol GG/SOP model-based tracker（KF/EKF on Jones）→ MMSE，公平对比 fixed-μ CMA + blind_affine_compare | ~1 天基建 + Scout | 中（EKF 在 fast SOP 下可能发散；文献 EKF 非占位但 OSL+dual-pol 组合未占） | 主结果潜力 |
| B | F3-B multi-block KF（用 GG AR(1) ρ≈0.99997）作 F1-B 次级组件 | ~半天 | 低 | 次级结果 |
| C | F2 pilot 撞车核查 + F2-A overhead 曲线（先查 JLT2023/OE2021/...）| ~半天（子 agent 文献）| 高（很可能撞车）| 负面材料 |
| D | thesis pivot 到 harvest/负面论文（放弃正面方法）| 0 | 低 | 仅负面材料 |

**推荐 A**：F1-A 的 0.133 headroom 是 campaign 中最强的正面信号，且 observability 强。F1-B 是唯一有
"合法 headroom + observability + 主结果潜力"的候选。但需用户授权约一天的 model-based tracker 基建投资
（现有 `_kf.py` 是 single-pol pilot-based，不可直接复用，CB3 警告 silent Y-drop）。

---

# AMENDMENT 2026-07-22 (S013 / D021 / V010 / V011) — 上文 TL;DR/排序/投资选择 RETRACTED

> 本文件 v1 正文（TL;DR、Probe 结果表、排序、可写论文材料、投资选择 A/B/C/D）建立于 D020 的 F1-A/F3-A
> PASS 解读。该解读已被 D021/V010/V011 撤回。正文保留为历史记录，**不作为当前结论**。

## 当前权威结论（取代上文 TL;DR）

**F1-A0 严格因果可观测性修复 Probe FAILED**（`repair-f1a0/`）。F1-B model-based tracker **不授权**（证据不足）。
**不建一天 tracker**。下一建议：**F2 collision check** 或转 harvest/负面边界论文。

## 上文被撤回的关键宣称（D021 §决策 1-7）

1. "per-block MMSE" → 降级为 oracle affine scoring-only bound（含 TX-truth calibration）。
2. F1 observability PASS → INVALIDATED（特征含未来 block，target 是事后 headroom 残差非信道状态）。
3. F3 conditional-MI PASS → INVALIDATED（marginal-MI max-difference，非 conditional MI）。
4. "ML 存在真实信息增量" / "第一个合法正面候选" / "授权一天基建" → 全撤回。

## F1-A0 修复 Probe 结果（详见 `repair-f1a0/artifacts/F1-A0-result.v1.json` + `scientific-critic-report.md`）

11 cells × 10 test seeds [161-170] = 110 raw rows（141-150 已被 D020 观察，禁作 final test）。宏观 PI-SER：

| 方法 | macro PI-SER | CI[lo,hi] | 备注 |
|---|---|---|---|
| CMA μ=0.03 (E0) | 0.3613 | [0.297,0.445] | 公平传统 comparator |
| blind_affine (CMA-fed) | 0.3556 | [0.284,0.449] | **critic L1：被 CMA 输出污染，raw-stream≈0.0000** |
| E1 CSI-only (no TX-truth) | 0.1681 | [0.072,0.278] | 纯 CSI genie |
| E2 budgeted pilot (32 pilots) | 0.7629 | [0.755,0.772] | **critic L2：实现破损（pilot 从未发送）** |
| E3 privileged (CSI+TX-truth) | 0.1787 | [0.076,0.297] | 旧 F1-A genie，仅归因 |
| causal_plugin (候选) | 0.1685 | [0.073,0.278] | ≈ E1 ≈ nopred |
| causal_plugin_nopred (control) | 0.1683 | [0.073,0.278] | g0 证明 prediction 无增量 |

**g0（prediction 增量）FAIL**：plugin vs nopred diff +0.00025，8 help/13 hurt/89 tie，binomial p≈0.38（不可区分于 coin flip）。
fixed_label_ser 与 pi_ser 110×7 bit-identical（g6 空洞，de-rotation 无 axis swap）。

## FAIL 的真实原因（V011 critic + 主线独立复核）

- **主导 confound 是物理非归因**：SOP rotation 在 256-symbol eval window 仅 **0.06°**（sop_rate=4e-6 → 1.02e-3 rad），
  de-rotation 近 identity，E1(真θ)≈causal_plugin(预测θ)≈nopred(θ≡0) 全塌缩 ~0.168。任何 tracker 在当前 atlas 都长一样。
- **"headroom"是 CMA μ 调参债**：μ=0.01→0.083 vs μ=0.03→0.369，blind CMA 仅靠 retune μ 关闭 ~60% gap-to-E1。
  0/110 rows diverged。是 D005/D007 已 flag 的 comparator 收敛债，非"CSI/TX-truth/model-prior 无价值"普适结论。
- **"TX-truth 无贡献"是 near-zero-rotation artifact**：E3=0.179 实际比 E1=0.168 更差 +0.011。

## 若未来重测 F1 家族须先做（V011）

1. high-SOP-rate cell atlas（rotation ≥ 几度，sop_rate ≫ 4e-6）；
2. μ-tuned CMA anchor（μ 在 validation 上 sweep 后冻结）；
3. raw-stream blind_affine（非 CMA-fed）；
4. 真 persistence/AR(1) baseline（g1 非代理）；
5. artifact 存 ridge 权重 + prefix-feature 向量 + per-sample h/theta（当前债务）。
