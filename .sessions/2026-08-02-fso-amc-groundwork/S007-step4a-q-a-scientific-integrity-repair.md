# [S007] GW Step 4a — Q-A 科学完整性修复与正确重测（撤回 D006 科学 KILL）

> 2026-08-03 | 阶段: GW Step 4a 可行性预判修复（Phase A-F）| 状态: 完成 — D006 科学 KILL 撤回（D007），Q-A 在 Contract B 下存活为 reliability-throughput tradeoff，Q-A' reframe 待用户裁决

## 目标

执行用户 2026-08-03 主控裁决执行提示词：撤回 D006 的无效 Q-A KILL recommendation，用 RED→GREEN 方式修复原 Q-A testbed 的物理模型/baseline/目标函数/动作空间，闭合后用两动作契约正确重测。

## 记录

### Phase A — RED 根因复现（10/10 RED_OBSERVED）

10 个独立最小失败测试（`corrected_v2/tests/red_tests.py`），逐个观察 RED，保存 receipt（`red_receipt.json`）。每个测试只验证一个行为，导入 buggy 原 `probe_headroom.py`：

- **T1 prediction_target_alignment**（H1）: pred 预测 k+td 但 evaluate_decision 对齐 h_true[k]。RED ✅
- **T2 galijasevic_margin_is_load_bearing**（H2）: GAL_MARGIN_dB 定义但 B1 不用（dead code）。RED ✅
- **T3 c1_all_infeasible_fallback**（H3）: below-lowest 静默 clip，无声明 outage/infeasible fallback。RED ✅
- **T4 threshold_is_not_fer_one**（H4）: 低于阈值被当 FER=1 hard fail；实际 Eq.23 连续 Q 函数。RED ✅
- **T5 complete_action_ladder**（H5）: 码率/阈值/margin 值匹配论文但 margin 未在 B1 使用。RED ✅
- **T6 linear_mean_normalization**（H6）: GG 线性 E[h]=1 归一化但 probe 减 per-turbulence E[10log10 h] 重定心。RED ✅
- **T7 constrained_objective**（H8）: Pareto-only 判决忽略 feasibility-first。RED ✅
- **T8 oracle_dominance**: O1 infeasible 被错误归因为 Q-A 假设失败（实际是 action-contract gap）。RED ✅
- **T9 delayed_metamorphic**: td>0 future-truth flip 在 present-index scoring 下既不改 action 也不改 outcome。RED ✅
- **T10 action_fallback_semantics**: 无任何方法有 outage/no-transmit 动作。RED ✅

### Phase B — 物理与算法身份闭合

派 fresh-context subagent 视觉核对 Galijasevic source.pdf（`identity_receipt.md` §1）:
- modulation=OOK+APD（非 QAM/非 coherent）；PBRL-LDPC k=8192，72 codes designed，16-rate subset simulated（8/9…8/77）
- FER=Eq.(23) Polyanskiy normal approximation（direct Q-form，连续）；target=**1e-6**（非 1e-4）
- Table 1: 16 阈值 + 16 per-rate margin（load-bearing，p.7 自证）；threshold = gain-dB rel POD −53.9dBm
- predictor target=**k+td**（future）；feedback delay 1-4ms round-trip；channel=**lognormal PSI=10 τ₀=10ms**（非 GG）；**无 outage/no-transmit 规则声明**
- FER 模型身份可恢复（Eq.23 在 PDF）→ 非 BLOCKED_BY_FER_MODEL_IDENTITY

**动作空间裁决（用户决策 2026-08-03）**: "同时跑两个动作契约"——Contract A（Galijasevic 原契无 outage）+ Contract B（symmetric no-transmit，所有方法共享，= Q-A' reframe 候选）。

**参数 provenance 债务（声明）**: GG (α,β) 无 Galijasevic 来源（论文 lognormal PSI=10）= scenario-transfer；TAU_C_S=5ms vs τ₀=10ms；BLOCK_SYM=32000 近似。独立验证 GG E[h]=1.004-1.015（线性归一化正确）。

### Phase C — GREEN 修复（10/10 GREEN + verifier 手工复算 MATCH 1e-12）

`corrected_v2/probe_corrected.py` 修复全部 10 缺陷；`green_check.py` 10/10 PASS。独立 verifier 手工复算 1 trajectory（dev seed0, α=5,β=2,sig=0,td=0.1）: 手算 fer_mean=3.3703e-10 = 代码 3.3703e-10（Δ<1e-12），exp_goodput=0.419365079 = 代码（MATCH）。

### Phase D — feasibility-first 重判（5 类 cell）

`verdict_evaluator.py` 重定义判决问题为"在预注册可靠性约束下最大化可实现 goodput"（非 Pareto dominance）。两契约 × 27 cells × 9 methods 重测（`probe_corrected_v2_raw.json`）:

- **Contract A**: 27/27 = `5_ACTION_CONTRACT_OR_OPERATING_POINT_INFEASIBLE`。所有方法含 O1 fer_mean=8e-3~2.2e-1 ≫ 1e-6。→ action-contract gap，非 Q-A 失败。
- **Contract B**: O1 feasible 27/27（7e-8~1.5e-7）；C1 feasible 9/27（弱湍流 α=5）；2 cells C1 胜最强增强 baseline +5.1-6.7% goodput；18 中强湍流 = `4_ACTION_OR_INFORMATION_GAP`。→ Q-A 假设未证伪，是 reliability-throughput tradeoff 非 Pareto loss。

### Phase E — headroom gate（dev-only）

O1 在 Contract B 27/27 feasible + 巨大 headroom；C1 在 9/27 feasible。Gate PASS。**held-out MVE 不在本轮跑**——须用户先裁决 Q-A' reframe（Contract B 实质改变 M = 新问题，须新 GW 周期）。

### Phase F — fresh held-out MVE

**未执行**（待用户决 Q-A' 后）。本轮停在 dev 阶段，单 commit。

### 独立 verifier（V008）

fresh-context subagent 12/12 PASS → CONFIRM。3 小债务（C0 占位 / B0 Contract B 对称 / scenario-transfer 参数）全声明，不影响结论。

## 决策引用

- D001-D005（历史，有效）。
- **D006**: 科学层 KILL recommendation **被 D007 撤回**（D006 执行合规性保留）。
- **D007（新建）**: STEP4A_EXECUTION_INVALID_PHYSICS_AND_ALGORITHM — 撤回 D006 科学 KILL，Q-A 在 Contract B 下存活。
- **V007**: 科学层失效（验证本地合同一致性，未核对 corrected 物理身份）。
- **V008（新建）**: D007 独立终审 12/12 PASS CONFIRM。
- corrected_v2 产出: probe_corrected.py / identity_receipt.md / tests/red_tests.py + red_receipt.json / tests/green_check.py + green_receipt.json / verdict_evaluator.py / results/probe_corrected_v2_raw.json。
- feasibility_report_v2.md（新建，不覆盖旧 feasibility_report.md）。

## 范围确认

- 本轮是否在 scope boundary 内: **是**（Step 4a 科学完整性修复 + 正确重测，不动 Skill/common/params.py/正式论文/dormant receiver/4 p05 log；不进 4b/5/Contract/Execute；不偷偷改 Q-A→Q-A'，Contract B 明确标 reframe 候选交用户）。
- executor 不自行最终 Go/No-Go，提交 recommendation 待用户确认（已遵守）。

## 后续

- **本轮 Step 4a 终态 = D006 科学 KILL 撤回（D007）；Q-A 在 Contract B 存活为 tradeoff，Q-A' reframe 待用户裁决**。
- **未宣称 Groundwork 闭合**（5 CORE < ≥8 整体完成门）。
- **下一合法动作（待用户确认）**: (i) 接受 Q-A' reframe → 新 GW Step 1-3 M-C-A + 四判据（Contract B = 新 M）；(ii) 接受 Contract A 下 Q-A 不可评估 → 停止 Q-A / 换 AMC 子族；(iii) 跑 fresh held-out MVE 仅在用户决 Q-A' 后；(iv) 补齐 3 篇 CORE。
- **禁 agent 自行 Go/No-Go 或偷偷改 Q-A→Q-A'**。
