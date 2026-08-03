# Feasibility Report v2 — Q-A Step 4a 科学完整性修复后正确重测

> **Owner**: AMC 独立专题 `2026-08-02-fso-amc-groundwork`（S007/D007/V008）。
> 创建: 2026-08-03 | 阶段: GW Step 4a 修复 | 状态: **D006 科学 KILL 撤回（D007）；Q-A 在 Contract B 存活为 reliability-throughput tradeoff；Q-A' reframe 待用户裁决**。
> **取代**: 旧 `feasibility_report.md` 的科学层结论（旧报告加 INVALIDATED_BY_D007 指针，**不删不改内容**，保留作 D006 历史证据）。
> canonical owner: `stages/gw-feasibility.md` §A0/A′/A/B/D；本报告不覆盖旧 receiver `feasibility_report.md`。

## 0. 为什么需要 v2

D006 的 Q-A KILL recommendation 建立在 8 个承重缺陷上（Phase A T1-T10 全部 RED_OBSERVED，`corrected_v2/tests/red_receipt.json`）。最致命:
- B1 未用 per-rate margin → **B1 不是 Galijasevic baseline**（D006 "C1 0/27 Pareto-dominate B1" 比较的是错误 B1）。
- scoring 对齐 h_true[k] 而非 h_true[k+td]（预测目标是 k+td）。
- FER 被当 hard fail（实际 Galijasevic Eq.23 连续 Q 函数；threshold-violation ≠ FER=1）。
- per-turbulence dB-mean 重定心改了工作点。
- "outage floor 即使 oracle 不可达" = action ladder 无 outage 动作 + 阈值表跨域套 GG 归一化辐照度的产物，非 Q-A 假设失败。

主控裁决（用户 2026-08-03 执行提示词）: 撤回 D006 科学 KILL，RED→GREEN 修复后用两动作契约正确重测。

## 1. 物理与算法身份（Phase B，identity_receipt.md）

经 fresh-context subagent 视觉核对 Galijasevic source.pdf:
- OOK+APD / PBRL-LDPC k=8192 / 16 rates 8/9…8/77 / FER target **1e-6** / Eq.23 连续 / per-rate margin load-bearing / predictor target **k+td** / feedback 1-4ms / **lognormal PSI=10 τ₀=10ms（非 GG）** / **无 outage 规则声明**。

**动作空间裁决（用户 2026-08-03）**: "同时跑两个动作契约":
- **Contract A** = Galijasevic 原契（16 率，below-lowest force lowest = Galijasevic 隐式行为）。
- **Contract B** = symmetric no-transmit（全方法共享 no-tx 动作 = **Q-A' reframe 候选**，需用户裁决升为新研究方向）。

## 2. Phase C GREEN 修复（corrected_v2/probe_corrected.py）

10/10 GREEN（`tests/green_receipt.json`）。独立 verifier 手工复算 1 trajectory fer_mean/exp_goodput 匹配代码 Δ<1e-12。

## 3. Phase D feasibility-first 重测（target FER 1e-6）

`probe_corrected_v2_raw.json`（27 cells × 9 methods × 2 contracts），`verdict_evaluator.py` 5 类分类:

### Contract A（Galijasevic 原契，无 outage）
| 指标 | 值 |
|------|----|
| cell 分类 | **27/27 = `5_ACTION_CONTRACT_OR_OPERATING_POINT_INFEASIBLE`** |
| O1 feasible | **0/27**（fer_mean 8e-3~2.2e-1 ≫ 1e-6）|
| C1 feasible | 0/27 |
| 任何方法 feasible | 0/27 |

**结论**: 在 Galijasevic 原动作契约下，1e-6 目标对**所有方法含 oracle** 结构不可达 = **action-contract/operating-point gap，不是 Q-A 假设失败**。D006 把它当 Q-A KILL 理由 = T8 RED 缺陷（已撤回）。

### Contract B（symmetric no-transmit = Q-A' reframe 候选）
| 指标 | 值 |
|------|----|
| O1 feasible | **27/27**（fer 7e-8~1.5e-7 < 1e-6）|
| C1 feasible | **9/27**（弱湍流 α=5 cells）|
| cell 分类 | 4× `6_PROBLEM_RESOLVED_BY_CONVENTIONAL_BASELINE` + 2× `1_C1_BEATS_BASELINE_+5-7%` + 3× `1_BOTH_FEASIBLE_C1_+2-3%` + 18× `4_ACTION_OR_INFORMATION_GAP` |

**结论**: Q-A 假设**未被证伪**: C1 在弱湍流 9 cells feasible，其中 2 cells 胜最强增强 baseline B2/B3/B4 +5.1-6.7% goodput。但 goodput 极低（0.001-0.011）因 no-transmit 丢帧多 = **reliability-throughput tradeoff，非 Pareto loss**。verifier 细化: 信号微弱，不构成决定性 Go；"存活"≠"已验证"。

## 4. Phase E headroom gate（dev-only）

O1 在 Contract B 27/27 feasible + 巨大 headroom；C1 在 9/27 feasible。Gate PASS（存在可行 deployable method + oracle headroom > 5%）。**held-out MVE 不在本轮跑**——须用户先裁决 Q-A' reframe。

## 5. Step 4a 修订决策（recommendation，待用户确认）

**recommendation = D006 科学 KILL 撤回（D007）；Q-A 状态修订**:

- **Contract A 下 Q-A 不可评估**（oracle 本身不可行 = action-contract gap）。
- **Contract B 下 Q-A 存活为 reliability-throughput tradeoff**（非 Pareto loss），但信号微弱（9/27 feasible，2 cells 胜 baseline 5-7%）。
- **Q-A' reframe（Contract B）实质改变 M** = 新问题，须新 GW Step 1-3 M-C-A + 四判据。**交用户裁决**。

依据: MVE 证据驱动（非 oracle-Kill）；feasibility-first 评估（非 Pareto-only）；profile "务实可毕业"（Q-A 未被证伪即不 Kill，但也不虚报 Go）。

**不 Kill family**: Q-A 在 Contract B 有 tradeoff 信号；2 reframe 路径 open。

## 6. 可回收产出

- corrected_v2 probe（两动作契约 + feasibility-first 评估 + 连续 FER）可复用于任何后续 AMC rate-selection 问题。
- **outage-floor 诊断修正**: D006 的 "5.7-19.8% outage floor" 是 action-ladder 无 outage + 跨域阈值套用的产物；corrected_v2 在 Contract B 加 no-transmit 后 O1 27/27 feasible，证明 floor 是 action-contract artifact 非 Q-A 失效。
- baseline ladder（B0-B5+C0/C1+O1/O2）+ feasibility-first 5 类评估方法论。
- 10 RED 测试 + identity receipt 是可复用的"testbed 完整性审查"模板。

## 7. Q-B 状态 & Groundwork 整体门

- **Q-B**: A0§0 判据3 致命暂存（无合法 coherent 星地 AMC baseline），未变。
- **Groundwork 整体完成门**: ≥8 篇；当前 5 CORE。**即使本轮修订也不宣称 Groundwork 闭合**。
- **Safi/L124 全文 BLOCKED**: Q-A 修订后 Safi UNVERIFIED 尾巴不再是阻塞；L124 coherent-C 族身份闭合仍 open。

## 8. 下一步合法动作（待用户确认）

- **(i) Q-A' reframe**: 接受 Contract B 为新 M → 新 GW Step 1-3（新 Q-A' M-C-A + 四判据）。
- **(ii) Contract A 下 Q-A 不可评估停止**: 停 Q-A / 换 AMC 子族 / 调整 C（跨阶段决策，禁 agent 自行放宽 C）。
- **(iii) fresh held-out MVE**: 仅在用户决 Q-A' 后，用全新不相交 seeds 跑（冻结合同 + paired CI + 独立重算）。
- **(iv) 补齐 3 篇 CORE** 后再议 Groundwork 闭合。

**禁止**: agent 自行 Go/No-Go；偷偷改 Q-A→Q-A'；把 Q-A Contract B tradeoff 当决定性 Go。

## 附录: 关键证据指针

- corrected probe: `projects/simulation/explore/amc-q-a-risk-aware-rate/corrected_v2/probe_corrected.py`
- corrected raw: `projects/simulation/results/amc_q_a_risk_aware_rate/probe_corrected_v2_raw.json`
- RED receipt: `corrected_v2/tests/red_receipt.json`（10/10 RED_OBSERVED）
- GREEN receipt: `corrected_v2/tests/green_receipt.json`（10/10 GREEN）
- identity receipt: `corrected_v2/identity_receipt.md`（Galijasevic PDF 视觉核对）
- verdict evaluator: `corrected_v2/verdict_evaluator.py`
- V008 verifier: `.sessions/2026-08-02-fso-amc-groundwork/verifications.md` ## V008（12/12 PASS CONFIRM）
- 旧（INVALIDATED）: `projects/thesis-fso/amc-groundwork/feasibility_report.md`（D006，科学层被 D007 取代，保留历史）+ `probe_headroom.py`/`probe_headroom_raw.json`（buggy original，保留作 RED 证据）
