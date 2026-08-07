# Handoff: Q1 Step 4a preflight EVIDENCE_GAP

> 来源: S002 | 交接目标: 用户批准后才可执行 ≤1 天 deterministic semantic smoke
> 文件名: H004-step4a-preflight-evidence-gap.md

## 已完成边界

- Q1 已完成 A0 §0–§6、A′/A/B 竞争分析和维度 D 的最小实验设计；维度 D 未执行。
- D009 记录受限范围变更；D010 冻结四类方法身份、单一贡献维度与 smoke 合同。
- 当前 terminal=`STEP4A_PREFLIGHT_EVIDENCE_GAP`：没有 B0/B1/B2 对 visible-only global joint oracle
  的差距数字或稳定误锁区；同 grid/score 下 B1 可能与 C 数学等价。
- V007 fresh-context 独立复验 PASS、blocker=`0`。JOCN 2026 全文不可得继续只限制 claim ceiling。

## 不要做什么

- 不把本 handoff 当 semantic smoke、MVE、testbed、方法实现或仿真的授权；用户未批准前不得派执行 T。
- 不把 B0 写成纯 timing-first：证据支持的强链是 coarse CFO 后做 MF/Lee timing，再做 frame/fine FOE/CPE。
- 不硬套 ML；不把一般 likelihood 非可分、“没人做过”或 JOCN 不可得当性能/新颖性证据。
- 不省略 B1/B2；若同信息同 score 的廉价方法覆盖 joint oracle ≥95%，必须 Kill/Pivot。
- 不修改 `projects/simulation/common/`、`params.py`、旧实验、Skill 或四个 `p05_run*.log`；不 push。

## 必读

1. `.sessions/2026-08-06-oversampled-coherent-sync-groundwork/topic-index.md`
2. `.sessions/2026-08-06-oversampled-coherent-sync-groundwork/decisions.md` D009–D010
3. `projects/thesis-fso/oversampled-sync-groundwork/step4a-preflight-discussion.md`
4. `.sessions/2026-08-06-oversampled-coherent-sync-groundwork/verifications.md` V007
5. `stages/gw-feasibility.md`（若用户批准执行，必须按维度 D 当轮重读）

## 接口变更（如有代码改动）

无。没有代码改动，只有 receiver-visible 信息合同和 truth-scoring 隔离合同的设计。

## 失败数据附录（如涉及路线失败）

无已执行实验数据。当前缺口是未测量，而不是负结果：B0/B1/B2/C-oracle gap、稳定错误峰区域和真实
计算量均待批准后的 semantic smoke 测量。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| coupled-acquisition 专门负面证据搜索未完成 | A0 §0 negative-evidence search | `EVIDENCE_GAP` | 用户批准 smoke 后、执行前完成本地有界核查；新 Web 检索须另行授权并由子 agent 执行 |
| exact preamble symbols 与完整 SNR 点尚未由单一来源冻结 | FR-20 参数溯源 | 只冻结 64-symbol sentinel 与最小 gap grid | 用户批准 smoke 后、执行前建立参数来源清单 |
| C 相对 B1/B2 的结构增量未成立 | 增强传统 baseline 必须同信息公平比较 | `EVIDENCE_GAP` | smoke 用共同 grid/score 测 B1/B2 coverage |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| identity / truth isolation | 无噪声 identity 全部命中；truth mutation 不改变 estimator 输出 | D010 / preflight report §4 | N/A（未运行） |
| 廉价覆盖 Kill 门 | B1 或 B2 覆盖 C-oracle 收益 ≥95% | 用户预注册退出条件 | N/A（未运行） |
| 实用增量 Kill 门 | C 对 B0 的 wrong-basin false-lock 相对改善 `G_C<5%` | D010 / 单一贡献维度 | N/A（未运行） |
| recommend micro-MVE 门 | 解析/surface 均非可分，稳定错误峰区至少跨 2×2 相邻 timing/CFO cells，C 对 B0 改善 ≥5%，且 B1/B2 覆盖 <95% | preflight report §4 | N/A（未运行） |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称（列出验证了哪些）
- [ ] 已检查 `_registry.yaml` 中本专题的 `depends_on` 和 `conflicts_with`
- [ ] 已确认当前范围未违反“明确不含”

## 下一轮

先让用户审阅 D010 的 semantic smoke 合同并明确批准或拒绝。只有明确批准后，才可新建受限执行任务，
按 `gw-feasibility.md` 维度 D 与 H004 阈值运行 ≤1 天 deterministic semantic smoke；否则保持
`STEP4A_PREFLIGHT_EVIDENCE_GAP`，不自动推进。
