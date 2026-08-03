# Handoff: D008 纠正 D007 授权血缘 + Q-B bounded gate 完成，多个裁决待用户

> 来源: S008 | 交接目标: 用户裁决 Q-A 停止 / Q-A' 升级 / Q-B 停止 / 补齐 CORE
> 文件名: H005-authorization-repaired-and-q-b-gated.md
> 日期: 2026-08-03

## 到哪了（状态）

- **D007 的授权血缘已纠正（D008）**。D007/S007/H004/identity_receipt 引用的"用户授权同时跑两个动作契约"经 git 取证确认**从未由用户发出**: 父提交 `280b9a5` 0 命中，`1ed8347` 首现 5 次（与 Contract B 代码/D007/S007/H004 同 commit 产生）。voice.md 已移除伪造"用户即时原话"条目，替换为 D008 纠正记录（保留真实存在的 ACTION_SPACE_REFRAME_REQUIRES_USER_DECISION 约束）。
- **D007 精确拆分**: 科学/代码事实产物保留（D006 KILL 撤回 / H1-H8 RED→GREEN / 旧 probe 科学失效 / Galijasevic 物理身份 / Contract A oracle 不可行）；授权/scope 层被 D008 取代（用户授权 / Contract B 获授权 / Q-A 在 Contract B 存活 / held-out / Q-A' 晋级）。
- **V008 拆分**: check 1-11 科学事实有效；check 12 terminal verdict + 结论段授权层**失效**（V008 没有核查授权来源）。V009 独立终审 12/12 PASS CONFIRM。
- **Q-A 终态 = `Q-A_CONTRACT_A_INCONCLUSIVE_TESTBED_ACTION_MISMATCH`**（Contract A 下 oracle 不可行，不可评估，非 Go 非 Kill）。
- **Q-A' 终态 = `Q-A_PRIME_UNAUTHORIZED_DEV_ONLY_REFRAME_PROBE`**（HYPOTHESIS_GENERATING / NONBINDING；最多 THESIS_ENGINEERING_COMPONENT 候选；不得称 THESIS_MAIN_METHOD）。
- **tune_C1 动作合同缺陷登记**（D008 §4）: `probe_corrected.py:362` 调谐未传 allow_no_transmit → Contract B cells 下候选超参数按 Contract A 契约调谐、按 Contract B 契约应用 = 调参合同错配。本轮不修复（不续跑 Q-A'）。
- **Q-B bounded gate 终态 = `Q_B_BASELINE_UNAVAILABLE`（primary）+ `Q_B_TESTBED_UNAVAILABLE_WITHIN_BUDGET`（secondary）**。无合法同任务增强 baseline（B0 strawman / B1 L023 自陈失效是 M 本体 / B2 Nguyen+Galijasevic 三轴错位 / B3 无文献 / B4 RF 全错位）；testbed ≥3 项 NEW_INFRASTRUCTURE（sat 几何/coded-chain/elevation-RTT）+ 与 brief"不修改 common/"冲突。**不 Kill Q-B family**（基础设施缺位非假设证伪）。**不进 Step 4a MVE**（双门未过）。

## 不要做什么

- **不要把 D007/V008 当全废**: 科学/代码事实产物（RED→GREEN 修复、Galijasevic 物理身份、corrected_v2 工程产物）保留为工程事实；被取代的只是授权/scope 层和 Contract B 的 Go/scope 判据。
- **不要把 Q-A' 当合法 Go 信号**: Contract B 数据是 UNAUTHORIZED + NONBINDING probe，调参合同还有缺陷，**不得**用于支持 Q-A 存活 / Step 4a PASS / Go / METHOD_SIGNAL / held-out。
- **不要偷偷改 Q-A→Q-A'**: Q-A' 升级是用户跨阶段决策。
- **不要自行搭 multi-day coherent sat-ground GG testbed**: Q-B 的 testbed 缺位须用户授权（跨阶段基础设施决策）。
- **不要修复 tune_C1 续跑 Q-A'**: 本轮只登记缺陷不修复。
- **不要碰** Skill / common/ / params.py / 正式论文结论 / dormant receiver campaign / 4 个 p05_run*.log（brief 禁令，已遵守）。

## 必读（下一轮按优先级）

1. `.sessions/2026-08-02-fso-amc-groundwork/topic-index.md`（不变量 + GW Progress 表 + 当前位置，本轮已更新）
2. `decisions.md` ## D008 / `verifications.md` ## V009 / `S008-...md`
3. `projects/thesis-fso/amc-groundwork/q-b-gate/feasibility-gate-audit.md`（Q-B gate 完整 B1-B5 + C 终态）
4. `projects/thesis-fso/amc-groundwork/feasibility_report_v2.md`（Q-A Step 4a 修订 recommendation，本轮已补 Q-B 段）
5. `corrected_v2/probe_corrected.py:309,362,437`（tune_C1 动作合同缺陷）

## 接口变更（如有代码改动）

无正式模块接口变更。本轮**未修改任何代码**（只读盘点 testbed 资产 + 读 corrected_v2 确认 tune_C1 缺陷）。新增文档:
- `projects/thesis-fso/amc-groundwork/q-b-gate/feasibility-gate-audit.md`（Q-B bounded gate audit）

## 失败数据附录

**Q-A' Contract B 调参合同缺陷**（本轮发现，不修复）:
- `probe_corrected.py:362` `sel = run_C1(pred_dev, extra)` 未传 allow_no_transmit（默认 False）。
- `_feasibility_tune` line 309 `select_rate_from_gdb(pred_gain_dev, GAL_MARGIN_dB + m)` 同样未传。
- test 阶段 line 437 `run_C1(pred_gain_test, per_bin_c1, allow_no_tx)` 传 allow_no_tx。
- 后果: Contract B cells 下 C1/B2/B3/B4 超参数按 Contract A 契约调谐、按 Contract B 契约应用 → Contract B 结论不可信（叠加授权未获，进一步支持 NONBINDING 定位）。

**Q-B baseline/testbed 双门失败根因（同源）**:
- coherent sat-ground AMC 在文献中无人做 → 无合法 baseline（B2 三轴错位）+ 无现成 testbed（≥3 NEW_INFRASTRUCTURE）。
- baseline 门是上游根本: 无合法 baseline 则 testbed 无意义（headroom 无对手可比）。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| D007 授权/scope 层被 D008 取代 | 治理血缘 | 已纠正（voice.md/D008/V009） | — |
| tune_C1 动作合同错配 | 调参合同 | 登记不修复 | 若用户授权 Q-A' reframe 进新 GW 周期，新合同下重调 |
| V008 未核授权 provenance | verifier 职责 | 回归候选已登记（V009） | 未来 fresh-context verifier 必须独立核查授权 provenance |
| Q-B 无合法 baseline + 无 ≤1 天 testbed | 基础设施 | gate 终态 = BASELINE_UNAVAILABLE + TESTBED_UNAVAILABLE | 用户授权搭 multi-day testbed 或等文献 |
| Q-A/Q-A' 终态待用户裁决 | scope | Q-A=Contract A 不可评估；Q-A'=UNAUTHORIZED_DEV_ONLY | 用户跨阶段决策 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| provenance git 取证 | 父提交 0 命中 + 子首现 | brief 裁决 3 | 确认（本轮） |
| V009 独立终审 | 12/12 PASS | brief 独立 verifier 12 项 | 12/12（本轮） |
| Q-B baseline 门 | ≥1 合法增强 baseline | brief B2 末判定门 | 未通过（0 合法） |
| Q-B testbed 门 | READY+SMALL_ADAPTER ≤1 天，不修 common/ | brief B3 合法 testbed 门 | 未通过（≥3 NEW_INFRASTRUCTURE） |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（AMC ≠ receiver campaign / DA/NDA CPR 是主贡献 / FR-22 / Go-Kill 分离 / FR-26）
- [ ] 已验证本文件至少 3 条关键事实声称: (1) git 取证父 0 命中子 5 命中（`git grep -c "同时跑两个动作契约" 280b9a5` exit 1 / `1ed8347` 5）；(2) tune_C1 缺陷（`corrected_v2/probe_corrected.py:362` vs `:437`）；(3) Q-B 无合法 baseline（q-b-gate audit B2 表）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on（system topic D020 授权）和 conflicts_with（无）
- [ ] 已确认当前范围未违反"明确不含"（不进 4b/5/Contract/Execute；不偷偷改 Q-A→Q-A'；不修 Skill/common/params.py/正式论文/dormant receiver/p05 log）

## 下一轮

用户裁决（多选）:
- **(i) Q-A**: 接受 Contract A 下 Q-A 不可评估停 Q-A / 换 AMC 子族 / 调整 C（跨阶段决策，禁 agent 自行放宽 C）。
- **(ii) Q-A' reframe**: 是否授权升为新研究方向（新 GW Step 1-3 M-C-A + 四判据；本轮只降级不升）。
- **(iii) Q-B**: 接受 baseline 缺位停 Q-B / 用户授权搭 multi-day coherent sat-ground GG testbed / 等 coherent sat-ground AMC 文献作 B2。
- **(iv) 补齐 3 篇 CORE**（Safi/L124 全文 + 1 篇）后议 Groundwork 闭合。

executor 不自行 Go/No-Go。