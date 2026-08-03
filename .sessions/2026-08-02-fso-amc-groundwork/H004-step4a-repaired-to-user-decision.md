# Handoff: Q-A Step 4a 科学完整性修复完成，Q-A' reframe 待用户裁决

> 来源: S007 | 交接目标: 用户裁决 Q-A' reframe / Contract A 停止 / fresh held-out MVE / 补齐 CORE
> 文件名: H004-step4a-repaired-to-user-decision.md
> 日期: 2026-08-03

## 到哪了（状态）

- **D006 的 Q-A KILL recommendation 科学层已撤回（D007）**。Phase A 用 10 个独立最小失败测试复现了 D006 依赖的 8 个承重缺陷（`corrected_v2/tests/red_receipt.json`，10/10 RED_OBSERVED）。最致命：B1 根本没用 per-rate margin（= B1 不是 Galijasevic baseline）；scoring 对齐 h_true[k] 而非预测目标 k+td；FER 被当 hard fail 而非 Galijasevic Eq.23 连续 Q 函数；per-turbulence dB-mean 重定心改了工作点。
- **Phase B 闭合物理身份**（fresh-context 子 agent 视觉核对 source.pdf，`identity_receipt.md`）：Galijasevic = OOK+APD / lognormal PSI=10 τ₀=10ms（**非 GG**）/ 16 率 8/9…8/77 / FER target **1e-6**（非旧 probe 的 1e-4）/ Eq.23 连续 / per-rate margin load-bearing / predictor target **k+td** / **论文未声明任何 outage/no-transmit 规则**。
- **Phase C corrected_v2 修复全 10 缺陷**（`probe_corrected.py` + `green_check.py` 10/10 GREEN）；独立 verifier 手工复算 1 trajectory 的 fer_mean/exp_goodput 与代码匹配 Δ<1e-12。
- **Phase D feasibility-first 重测两动作契约**（用户裁决"同时跑两个动作契约"，`probe_corrected_v2_raw.json` + `verdict_evaluator.py`）：
  - **Contract A（Galijasevic 原契，无 outage）**：27/27 cells = action-contract/operating-point 不可行（**所有方法含 oracle O1 的 fer_mean = 8e-3~2.2e-1 ≫ 1e-6**）。→ D006 的"outage floor 即使 oracle 不可达"是 action ladder 无 outage 动作 + 阈值跨域套用的产物，**不是 Q-A 假设失败**。
  - **Contract B（symmetric no-transmit = Q-A' reframe 候选）**：O1 feasible 27/27；C1 feasible 9/27（弱湍流 α=5）；2 cells C1 胜最强增强 baseline +5.1-6.7% goodput；18 中强湍流 = action/information gap。→ Q-A 假设**未被证伪**，是 reliability-throughput tradeoff（goodput 极低 0.001-0.011 因丢帧多），**非 Pareto loss**。
- **V008 独立 verifier 12/12 PASS CONFIRM**（3 小债务声明，不影响结论）。
- **held-out MVE 未跑**（须用户先决 Q-A'）。本轮停在 dev 阶段。

## 不要做什么

- **不要把 D006 当"AMC family 全死"**：D006 科学层已撤回；Q-A 在 Contract B 有 tradeoff 信号。
- **不要偷偷改 Q-A→Q-A'**：Contract B 加 no-transmit 实质改变 M（Galijasevic 无此 action）= 新问题，须新 GW Step 1-3 M-C-A + 四判据。本轮只把它标为 reframe 候选交用户。
- **不要跑 fresh held-out MVE**：须用户先裁决 Q-A'，且必须用全新不相交 seeds（旧 dev/test seeds 0-99 禁复用）。
- **不要删旧 probe_headroom.py / probe_headroom_raw.json / feasibility_report.md**：保留作 D006 历史 + RED 根因材料（已加 INVALIDATED_BY_D007 指针）。
- **不要碰** Skill / common/ / params.py / 正式论文结论 / dormant receiver campaign / 4 个 p05_run*.log（brief 禁令，已遵守）。

## 必读（下一轮按优先级）

1. `.sessions/2026-08-02-fso-amc-groundwork/topic-index.md`（不变量 + GW Progress 表 + 当前位置）
2. `projects/thesis-fso/amc-groundwork/feasibility_report_v2.md`（修订 recommendation + 两契约结果）
3. `projects/simulation/explore/amc-q-a-risk-aware-rate/corrected_v2/identity_receipt.md`（物理身份 + 动作裁决）
4. `decisions.md` ## D007 / `verifications.md` ## V008 / `S007-...md`
5. `corrected_v2/tests/red_receipt.json` + `green_receipt.json`（10 缺陷复现 + 修复证据）

## 接口变更（如有代码改动）

无正式模块接口变更（本轮全部在 explore/ corrected_v2 子目录，不动 common/params.py）。corrected_v2 新增文件（不取代正式仿真基建）:
- `probe_corrected.py`（两动作契约 probe）
- `verdict_evaluator.py`（feasibility-first 5 类评估）
- `tests/red_tests.py` + `red_receipt.json`（Phase A RED）
- `tests/green_check.py` + `green_receipt.json`（Phase C GREEN）
- `identity_receipt.md`（Phase B）
- `results/probe_corrected_v2_raw.json`（重测 raw）

## 失败数据附录

**D006 的"outage floor 5.74-19.79% 即使 oracle 不可达"** 是 action-contract artifact：
- Contract A（无 outage）O1 fer_mean = 8e-3（弱湍）~2.2e-1（强湍）— 全部 ≫ 1e-6，因 deep-fade 帧无 outage 动作可避。
- Contract B（加 no-transmit）O1 fer_mean = 7e-8~1.5e-7 — 全部 < 1e-6 feasible。→ 证明 floor 是缺 outage 动作的产物，非物理/假设失效。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| run_C0 占位（==B1） | ladder 完整 | 声明，未进 verdict | 若需 C0 naive 消融实现之 |
| B0 Contract B 忽略 allow_no_transmit | 动作对称 | 声明（strawman 下界） | 若需严格对称补之 |
| TAU_C_S=5ms / BLOCK_SYM=32000 | 参数溯源 | 声明 scenario-transfer | 若用户要复现 Galijasevic 用 τ₀=10ms + 1024-bit fade |
| GG (α,β) 无 Galijasevic 来源 | 参数溯源 | 声明 scenario-transfer | 若用户要 Galijasevic 原信道用 lognormal PSI=10 |
| 连续 FER 用单调近似非 Eq.23 全式 | 公式身份 | 声明（阈值处精确，中间单调插值） | 若需 Eq.23 APD-POD 全式接 APD 检测参数 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| RED 根因复现 | 10/10 RED_OBSERVED | brief Phase A | 10/10（本轮） |
| GREEN 修复 | 10/10 GREEN | brief Phase C | 10/10（本轮） |
| verifier 手工复算 | fer_mean/goodput Δ<1e-6 | brief Phase C + mve-validation V5 | MATCH Δ<1e-12（本轮） |
| metamorphic gate(a) | sig=0,td=0 → B1==O1 | brief Phase A T8 | PASS（本轮） |
| feasibility-first | 无 Pareto 残留 | brief Phase D | PASS（本轮） |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（AMC ≠ receiver campaign / DA/NDA CPR 是主贡献 / FR-22 / Go-Kill 分离 / FR-26）
- [ ] 已验证本文件至少 3 条关键事实声称：(1) Contract A 27/27 O1 fer_mean ≈ 8e-3~2.2e-1（查 probe_corrected_v2_raw.json）；(2) Contract B O1 feasible 27/27（查同文件）；(3) B1 margin load-bearing（查 green_receipt.json T2）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on（system topic D020 授权）和 conflicts_with（无）
- [ ] 已确认当前范围未违反"明确不含"（不进 4b/5/Contract/Execute；不偷偷改 Q-A→Q-A'；不动 Skill/common/params.py/正式论文/dormant receiver/p05 log）

## 下一轮

用户裁决四选一:
- **(i) Q-A' reframe**: 接受 Contract B 为新 M → 新 GW Step 1-3（新 Q-A' M-C-A + 四判据）。
- **(ii) Contract A 下 Q-A 不可评估停止**: 停 Q-A / 换 AMC 子族 / 调整 C（跨阶段决策）。
- **(iii) fresh held-out MVE**: 仅在用户决 Q-A' 后，用全新不相交 seeds（≠ 0-99）跑，冻结合同 + paired CI + 独立重算。
- **(iv) 补齐 3 篇 CORE** 后再议 Groundwork 闭合。

executor 不自行 Go/No-Go。
