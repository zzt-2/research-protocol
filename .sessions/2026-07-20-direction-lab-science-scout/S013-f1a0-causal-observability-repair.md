# [S013] F1-A0 严格因果可观测性修复 Probe — FAIL（D021/V010/V011）；F1-B 不建，转 F2

> 2026-07-22 | SCIENCE_SCOUT（S012/D020/H013 续接，受 D021 驱动） | 状态: 本轮完成，交用户裁决 F2 vs 收尾

## 目标

执行用户 2026-07-22 提示词 §一-§九：(1) 对 S012/D020/V009/H013 做确定性科学语义纠偏（D021）；(2) 执行一个不超过半天的 F1-A0 causal observability repair Probe；(3) 给出是否值得再投资一天 tracker 的新证据。

## 记录

### 0. 环境核验（session-governance Trigger 1/5）

- 提示词声明 HEAD=bf620b3 / 分支 codex/direction-lab-capability-atlas。主 worktree 当前在 `feat/title-consistency-check`（HEAD=97473a2），但目标 artifact 在 git worktree `D:/code/study/research-protocol/.worktrees/direction-lab-capability-atlas`（HEAD=bf620b3，clean）。**全程在该 worktree 操作，不动主 worktree**。
- 续接 H013：独立核验 3 条事实 PASS（F1-A headroom 0.1329、test seeds 141-150 disjoint、state/portfolio/harvest YAML 可解析）。

### 1. 确定性纠偏（提示词 §一）— D021 + V010

源码级审计确认提示词列的 11 项科学缺口全部成立（逐条 `file:line` 定位，见 D021 §理由）：
- F1 genie 同时用 true h/θ + TX-truth LS calibration（`probe_shared.py:136-175 mmse_equalize_oracle`，L148 + L168）→ 重分类 `PRIVILEGED_CSI_PLUS_TX_CALIBRATION_GENIE_GAP`。
- F1 observability 特征读全流 trace（含未来 block）；target 是事后 headroom 残差非信道状态（`run_f1a_model_prior.py:77-99,155-166`）。
- F3 是 marginal-MI max-difference 非 conditional MI（`run_f3a_history.py:195-196`）。
- blind_affine_compare_16qam contract 声明但 Probe 从未调用（grep src 无）。
- F1 artifact 未存 fixed-label metric + 无 raw rows。
- F1/F3 artifact 的 F4 source hash 与当前源码不一致（`adf8559556cf` vs `b91731e9c26f`）。
- V009 未审科学层（只审 integrity）；STATUS.v1.md 在 bf620b3 实际 +9/-4 diff（与 "protected unchanged" 矛盾）；canonical/project.v1 ownership 冲突未解。
- D021 amends D020（不删不改）；撤回 "per-block MMSE/observability PASS/conditional-MI PASS/正面候选/授权一天基建" 等 7 项宣称，原始数值保留。

### 2. F1-A0 修复 Probe 设计（提示词 §二-§六）— contract + failing-first tests

- 冻结 `repair-f1a0/probe-contract.v1.yaml`：E0-E3 信息源拆分（E1 纯 CSI genie 禁 TX-truth / E2 exact Jones + budgeted 固定 pilot / E3 旧 privileged 仅归因）；严格因果 prefix 特征（index<cut）；val[151-155]/test[161-170]（141-150 已观察禁作 final test）；grouped cell bootstrap CI；pass_gate g1-g6。
- 写 15 个 failing-first tests（`test_f1a0_invariants.py`）先于实现：future-leakage invariant / target-alignment（target=state 非 headroom）/ blind_affine 实际调用 / dual metric / val-test-prior disjoint / test 不参与 feature selection / raw→aggregate / source-hash 闭包 / E1 无 TX-truth。

### 3. F1-A0 执行（子 agent）+ 主线独立复核

- 子 agent 实现 `repair_shared.py` + `run_f1a0_causal.py`，15/15 tests PASS，跑全量（11 cells × 10 test seeds = 110 rows）。
- **子 agent verdict = FAIL**（g0 prediction 无增量）。
- **主线独立复核**（FR-26，不盲信子 agent）：重跑 tests 15/15 PASS；artifact 110 raw rows + 2 src hash 全 MATCH；cma_pi_ser_macro 从 raw rows 重算 diff 0.00e+00；g0 8/13/89 split + binomial 核查；per-cell E1≈E3≈plugin≈nopred 核查；SOP rotation 0.06° 物理核查。

### 4. 独立 scientific critic（子 agent）+ 主线复核其 2 最强攻击 — V011

critic verdict = **HOLDS（但证据基础被重写，2 子结论 OVERTURNED）**。5 attack landed：
- **L1（最强）**：blind_affine 跑在 CMA 损坏的 z-stream → g1/g2 comparator 失效。**主线复核 CONFIRM**：raw-stream blind_affine ≈ 0.0000 vs CMA-fed ≈ 0.83。
- **L2**：E2 budgeted pilot 实现破损（pilot 接收端合成、信道从未发送）→ E2=0.76 是噪声非 pilot 性能。
- **L3**：g6 空洞（PI==fixed-label bit-identical 110×7）。
- **L4**：**主线复核 CONFIRM** "CMA 发散"不准确；μ=0.01→0.083 vs μ=0.03→0.369，是 μ 调参债（D005/D007 已 flag），0/110 diverged。
- **L5**：g1 非真 persistence baseline。
- SURVIVED：因果性/未来泄漏（N1）、E1 无 TX-truth 泄漏（N2）、g0 FAIL 真实（N3，binomial p≈0.38）。
- **主导 confound（C1）**：rotation 0.06° 使预测任务近空，F1-A0 是 F1 家族弱测试 by construction。

### 5. 收尾

- D021 措辞精化（V011 要求）："CMA-anchor-bad（发散）" → "CMA μ 调参不当（已知债）+ rotation 近零使 atlas 无法测 F1 家族"。
- 最终诚实裁决：**F1-A0 FAIL 存活，不建 tracker，转 F2**。但非"model-prior 无价值"普适结论。
- 未改 protected history / STATUS.v1.md / canonical-state；无 push。

## 决策引用

- D021：F1-A 科学语义纠偏 + 重分类 + 授权 F1-A0（新建；末段 V011 后精化措辞）
- D020：被 D021 amends（不删不改；原始数值保留）
- V010：F1-A integrity 独立核验 PARTIAL（新建）
- V011：F1-A0 科学 critic 复核 HOLDS-with-refinement（新建）
- H013：前置 handoff（接收方验证 PASS）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。纠偏 + F1-A0 修复 Probe 是 D021 明确授权；未触碰"明确不含"（不改 protected history/STATUS.v1.md/canonical-state；不复活 blind-router/pilot-Jones/C12/C16；不 push；不建 EKF/PF/GRU/NN/完整 tracker）。
- 专题膨胀：本专题现 13 个 S###（S013 新建）；仍 < 15 阈值。

## 后续

- **交用户裁决**：(a) 转 F2 collision check（pilot 家族，JLT2023/OE2021/LCOMM2026/TCOM2025/JLT2022-23 撞车核查）；或 (b) 收尾转负面/harvest 论文；或 (c) 若坚持重测 F1 家族——须先换 high-SOP-rate cell atlas + μ-tuned CMA + raw-stream blind_affine + 真 persistence/AR(1) baseline（V011 列的 5 项 "what would change the conclusion"）。
- 未决债务（交主控）：STATUS.v1.md "protected unchanged vs +9/-4 diff" 矛盾；canonical/project.v1 ownership 冲突（D021 gap #10/#11，本轮只记录未改）。
