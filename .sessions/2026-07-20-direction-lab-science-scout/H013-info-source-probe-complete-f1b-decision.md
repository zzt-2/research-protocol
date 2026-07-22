# Handoff: 信息来源组合级 Probe 完成；F1-B model-based tracker 投资选择待用户

> 来源: S012 | 交接目标: 用户决策 F1-B 投资选择（A/B/C/D），或新对话续接执行
> 日期: 2026-07-22
> 文件名: H013-info-source-probe-complete-f1b-decision.md

## 到哪了（状态）

S012 完成信息来源组合级 Probe（D019/H012 的 next_action）。在 11-cell 16QAM dual-pol OSL atlas × fresh disjoint test seeds [141-150] 上，用冻结共享 contract 跑了三个 headroom/observability Probe：

- **F1-A channel-model prior → PASS**：scoring-only model-prior oracle（真 per-block Jones from h/θ → per-block MMSE）关闭 macro PI-SER headroom = **0.1329**（CI [+0.078,+0.196]），是 D018 blind-router 0.0037 的 **36×**；receiver-visible observability 强相关（max |r|=0.651，特征 z_amp_mean / cm_error_final）。model prior 是**不同信息源**，不是换盲 cost。
- **F3-A causal history → PASS**（次级）：历史 block CMA trace 对 collapse 提供 MI 增量 +0.060 bits、对 pi_ser 提供 R² 增量 +0.036（best=cm_error_trend）。历史确实增加条件信息。
- **F4-A decoder/soft → BOUNDARY**：corrected per-symbol σ² oracle 的 analytic GMI headroom 仅 +0.0089（**smoothing-fragile**：sm=2/8/32 = +0.033/+0.009/+0.002，CI 跨 0）；histogram-MI 完全复现 C12 scale-artifact（−0.021，scale-invariant）。F4-B coded-chain INFRASTRUCTURE_BLOCKED。**不建 F4-B**。

独立 verifier V009 CONFIRM（9 项：8 PASS + 1 PARTIAL，0 P0，1 P1 documented；headline 数字独立重算 bit-identical）。10/10 identity/smoke gate PASS。

**F1-B（dual-pol GG/SOP model-based tracker → MMSE）是 campaign 中第一个有合法 headroom + observability 双通过的正面方法候选**，有主结果潜力。但它需约一天新基建（现有 `_kf.py` 是 single-pol pilot-based，CB3 警告 silent Y-drop，不可直接复用）。依提示词 §六，最强候选需 ~1 天基建时**不直接建**，完成所有轻量 Probe 后统一交用户报告投资选择。

## 下一步干什么

**第一件事：用户在 A/B/C/D 四选项中决策**（见下方）。若选 A（推荐），新对话续接：建 dual-pol GG/SOP model-based tracker（KF/EKF on Jones 用 GG/SOP 模型先验）→ per-block MMSE 均衡器，在共享 contract 上跑 bounded Scout，公平对比 fixed-μ CMA μ=0.03 + blind_affine_compare_16qam；oracle 只作 Kill bound（FR-21/FR-25）。F1-A 的 0.133 headroom 是上界，F1-B 实际增益必低于此（tracker 不可能完美恢复 Jones）。

## 投资选择（交用户）

| 选项 | 内容 | 成本 | 风险 | 预期产出 |
|---|---|---|---|---|
| **A（推荐）** | F1-B bounded Scout：dual-pol GG/SOP model-based tracker → MMSE | ~1 天基建 + Scout | 中（EKF 在 fast SOP 下可能发散；文献 EKF 非占位但 OSL+dual-pol 组合未占） | 主结果潜力 |
| B | F3-B multi-block KF（GG AR(1) ρ≈0.99997）作 F1-B 次级组件 | ~半天 | 低 | 次级结果 |
| C | F2 pilot 撞车核查 + F2-A overhead 曲线 | ~半天（子 agent 文献）| 高（JLT2023/OE2021/... 很可能撞车）| 负面材料 |
| D | thesis pivot 到 harvest/负面论文 | 0 | 低 | 仅负面材料 |

## 纪律（和下一步直接相关）

- 不直接实现完整 EKF/particle filter 直到 F1-B Scout contract 冻结；不一次性建 pilot/coded chain/tracker 全部基建。
- 不复活 D018 blind-expert router、p03 pilot→Jones→inverse 微变体、C12 全局-σ² oracle、C16 非-FIR HOS。
- F1-B 的 Go 必须赢**公平传统 comparator**（fixed-μ CMA + blind_affine_compare_16qam）；oracle（F1-A 0.133）只作 Kill/headroom bound，不作 Go 判据（FR-25）。
- F4-A 的 +0.0089 GMI 是 smoothing-fragile，**不得当稳定 soft-info bound 引用**（verifier P1 caveat 已写入 result.json）。
- 物理"可用"门限必须有文献/标准来源；MDE=0.005/0.03 不是通信可用门限；无 FEC chain 时只报相对收益。
- 不因 F1-A PASS 就宣称"通信可用"或"ML 必胜"——F1-A 是 oracle 上界，F1-B 实际增益待 Scout。

## 必读（不超过 8 个）

1. `.sessions/2026-07-20-direction-lab-science-scout/topic-index.md`（不变量 + 当前位置）
2. 本文件 `H013-info-source-probe-complete-f1b-decision.md`
3. `projects/thesis-fso/direction-lab/scout/info-source-portfolio-probe/synthesis.v1.md`（排序 + 投资选择详）
4. `projects/thesis-fso/direction-lab/scout/info-source-portfolio-probe/candidate-map.v1.md`（四族候选 Map）
5. `projects/thesis-fso/direction-lab/scout/info-source-portfolio-probe/probe-contract.v1.yaml`（冻结共享 contract）
6. `projects/thesis-fso/direction-lab/scout/info-source-portfolio-probe/artifacts/F1-A-result.v1.json`（0.133 headroom + 0.65 obs）
7. `.sessions/2026-07-20-direction-lab-science-scout/decisions.md` 的 D020 + V009
8. `projects/thesis-fso/direction-lab/STATUS.v1.md`

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落。
- [ ] 已验证至少 3 条关键事实：
  - F1-A headroom `0.1329` + observability `|r|=0.651` → 从 F1-A-result.v1.json 重算；
  - F4-A analytic GMI headroom `+0.0089` + histogram `-0.021`（scale-invariant）→ 从 F4-A-result.v1.json 重算 + scale-invariance smoke；
  - test seeds `141-150` 与所有 prior disjoint → 查 probe-contract.v1.yaml。
- [ ] 已检查 `_registry.yaml` 的 depends_on/conflicts_with。
- [ ] 已确认当前范围不含 formal promotion、push、protected history 改动、blind-router/pilot-Jones/C12-global-σ²/C16 复活。

## git 状态

- worktree: `D:/code/study/research-protocol/.worktrees/direction-lab-capability-atlas`
- branch: `codex/direction-lab-capability-atlas`
- 本轮 consolidated commit 待提交（不 push）。接收时以 `git log -1` 核验实际 SHA。
