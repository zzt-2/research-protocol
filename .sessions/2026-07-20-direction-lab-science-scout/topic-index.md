# Topic Index: Direction Lab 首轮 SCIENCE_SCOUT 正式科学探索

> 状态: active | 创建: 2026-07-20 | 最后更新: 2026-07-20（D005：CB1 降为 DIAGNOSTIC/SLICE；H001 被 H002 取代；下一步先做轻量传统 baseline 裁决并继续 Portfolio）

## 专题信息

- **slug**: `2026-07-20-direction-lab-science-scout`
- **性质**: 正式科学探索（首轮 SCIENCE_SCOUT campaign），不是蓝图/治理/迁移专题
- **worktree**: `.worktrees/direction-lab-capability-atlas`（分支 `codex/direction-lab-capability-atlas`，从 `65db4ef`）
- **流程拥有者**: `.agents/skills/research-direction-lab/SKILL.md`（7-phase loop）

## 范围边界

### 原始目标（冻结，来自用户 2026-07-20 执行提示词）

在双偏振星地 OSL 接收机中的"合法 ML 信息增量"目标范围内，启动首轮正式 SCIENCE_SCOUT campaign：恢复 → Portfolio Refresh → Capability Leverage Atlas → 共享能力建设 → baseline/headroom 探针 → 多候选批量 Scout → synthesis → harvest → 自动轮换。如果首选共享能力不成立，自动回到 Portfolio 选择下一项；不在每个小步骤等待用户确认。

### 当前范围

- 授权状态从 `READ_ONLY_MIGRATION_PREVIEW` 迁移为本轮限定的 `SCIENCE_SCOUT`（新 campaign contract + 新状态投影，不改写历史 projection）；
- 在隔离 worktree 中执行 Portfolio Refresh、Capability Leverage Atlas、共享能力建设、baseline/headroom 仿真、小规模 ML Scout、synthesis、harvest、自动轮换；
- 处理 stale internal checksum / last_completed_batch pointer 等债务时显式登记，用新 projection/event 或明确迁移记录解决；
- 建立并维护 `formula-symbol-parameter-provenance.yaml`（公式/符号/参数来源硬门）。

### 明确不含

- 不修改或重跑 B001–B003、P03 Atlas 的原始历史字节；
- 不创建 legacy B004；
- 不把 Scout/Sandbox 数字自动写入论文正文；
- 不自动宣称 candidate/family/domain 级别结论；
- 不绕过 Groundwork/Contract/Execute 完成正式晋级；
- 不 push、不 merge、不修改 dirty 普通根 worktree；
- 不为让 ML 获胜而修改物理参数、baseline、指标或比较口径；
- 不复制 protected history 数字到新 ledger 而不重新 hash 绑定。

### 范围变更记录

（无；首轮启动）

## 不变量

- canonical baseline = `baseline.standard_cma.godard_z`（含 Godard z 因子），身份严格分离 current-CMA / no-z；不跨域宣称 standard-CMA 永不 swap。
- metric contract = `fixed_label_ber` + `permutation_invariant_ber` 双报；二者语义不得互换。
- B001–B003、P03 Atlas、canonical state、completion events、receipts 字节不可改；B004 不存在且本轮不创建 legacy B004。
- Sandbox/Scout 数字不自动晋级 Groundwork/Contract/Execute/论文；晋级须用户明确 strategy 决策。
- 主对话严禁 WebSearch/webReader；论文精读、web 查询、批量引用筛查必须子 agent 执行。
- 公式/符号/参数进入实现前必须建立 provenance（equation/page/section 精确出处，或标 `DERIVED_IN_PROJECT` + 交叉验证，或 `DEFINED_HERE`）。
- baseline 来源必须区分原始方法/权威复现/代表性使用，正文公式不可用标题联想替代。
- oracle/scoring-only 上界只作 Kill 工具（Step 4a 维度 D / FR-21），不当 Go 判据（FR-25）；Go 标准 = 赢传统未优化 baseline。

## 已确认结论

### 不变量

（首轮启动；尚未产生本专题的架构级不变量。继承自 anchor 的不变量见上节。）

### 其他结论

- CB1 证明当前单模 CMA/长度合同下存在 inner-ring collapse 与 scoring-only oracle gap，但尚未证明问题经过任务适配的传统 baseline 后仍存在。
- baseline 不必是当前 SOTA；一个来源闭环、广泛采用、任务适配且公平的 comparator 足以支撑有限主张。

## 进展线索

- **S001**：campaign 启动；恢复地基、核验 protected history、建立隔离 worktree `direction-lab-capability-atlas`、登记新专题；完成授权迁移（campaign-contract + authorization-projection）、Portfolio Refresh v1（12 维展开 + 8 新 seeds U45-U52 + 4 re-clusterings + 8 priority candidates）、Capability Leverage Atlas v1（5 bundles 评估，CB1 选为首选）、formula-symbol-parameter-provenance.yaml（11 公式/22 符号/14 参数）。D001 CB1 选择 / D002 授权迁移 / D003 provenance 硬门。
- **S002**：CB1 closure 实施（`_dual_pol_channel.py` 参数化 modulation，11/11 closure + 6/6 regression PASS）；baseline Atlas 运行（11 16QAM cells × 10 seeds）；**发现 10/11 cells headroom ≥ MDE，max 0.333**；独立验证 CONFIRM（clean-room verifier）；harvest H010-H015（POSITIVE_MECHANISM_SIGNAL / FAILURE_MECHANISM inner-ring-collapse / REUSABLE_ASSET closure / INFRASTRUCTURE_GAP _cma identity / EVALUATION_INSIGHT 16QAM PI-SER rotations / LOCAL_NEGATIVE snr=5）；D004 本轮不触发 ML Scout，记录 scoped positive + handoff H001。
- **S002 续接 / D005 / H002**：独立审计指出 comparator 任务适配和收敛不足；历史 Atlas 数字不删除，但证据级别收回 `DIAGNOSTIC/SLICE`。D005 取代 D004 的直接 ML 授权；H002 要求先做一个主传统 comparator + 必要廉价扩展的共享裁决，并行准备其他机制候选。

## 未决项

- ML Scout batch 未运行；H001 已 superseded，只有达到 `PROBLEM_SURVIVES_CONVENTIONAL_BASELINE` 后才授权。
- 轻量 baseline adjudication shared batch 尚未建立；主 comparator 的具体选择须有文献与实现闭环。
- `_cma.py:CMAEqualizer2x2` scalar-error 与 docstring/canonical "Godard-with-z" 不一致（H013 OPEN_ACKNOWLEDGED）。
- 16QAM R²=1.32 未 canonical 化（仅 CB1 closure 中定义）。
- P03 `claim-scope-validation-receipt.v1.yaml` SHA 与 `claim-scope-assessment.v1.yaml` 不匹配（pre-existing at base commit，与本轮无关）。
- stale `_dual_pol_channel.py` checksum（行尾差异）已在 authorization-projection.v1.yaml 登记。

## 当前位置

S002 及其充分性复核已完成。CB1 closure/Atlas/harvest 保留，但当前只支持 `DIAGNOSTIC/SLICE`；H002 是唯一续接入口。下一对话先做轻量 baseline adjudication shared batch，同时维护完整 Portfolio；不直接训练 ML。
