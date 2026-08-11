# Handoff: A0 已独立通过，只进入冻结 D0 defect smoke

> 来源: S001 | 交接目标: 按 D010/V004/CP011 实现、测试并执行四 strata D0；不得提前建设 C1 policy
> 日期: 2026-08-10
> 文件名: H003-d0-defect-smoke-entry.md

## 已完成边界

A0/A′/A/B 的中央 report 与 D0 YAML 已经历 step-088→091 独立审查链；step-091 最终 `PASS / P0/P1/P2=0/0/0`，step-090 的 bootstrap/invalid replicate、S3 fusion 与 post-D0 safety 三项残余全部 CLOSED。D010/V004/CP011 只授权 `GROUNDWORK_STEP4A_D0_DEFECT_SMOKE`，当前 D0=`NOT_RUN`、method signal=`NONE`。科学数值 owner 是 `projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml`；report 只解释，不可另立第二套阈值。

## 不要做什么

1. D0 没有 trigger、accept/reject、fallback 或 applied local action；禁止把 C1-ext 偷渡进 diagnostic harness。
2. Natural 与 controlled strata 不池化；TruthView 只在输出冻结后给 evaluator，deployable score 只见 ReceiverView。
3. B0/B1/B2/O1 共享 pilot-bearing waveform、payload 与 symbol-time support；B1/B2 只用各自 dev seeds 调参并一次冻结，test 禁 best-of。
4. 四 strata 必须合取；任一关键 gate 失败即 C1 hard terminal，不调门槛、不扩大 candidate support、不先做 C1 抢救。
5. 四个 `p05_run*.log` 永不修改/暂存；不修改 `common/` 掩盖 testbed 身份；不 push。

## 必读

1. `.sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md` 的控制块、范围边界与不变量。
2. `.sessions/2026-08-09-coded-decoder-feedback-groundwork/decisions.md` D010 与 `verifications.md` V004。
3. `projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml`（唯一数值 owner）。
4. `projects/thesis-fso/coded-decoder-feedback-groundwork/step4a-a0-preflight.md` 与 `projects/thesis-fso/worker-logs/step-091-c1-a0-step090-narrow-verifier.md`。
5. sim-preflight skill、`stages/groundwork.md`、`stages/gw-feasibility.md`、`thesis-lessons.md` 速查表/最近三条、`code-quality.md`、`reference/sim-template/` 对应模板。

## 接口变更（如有代码改动）

无。当前只有 report/YAML/governance control metadata；尚未创建 D0 代码、测试或 raw rows。

## 失败数据附录（如涉及路线失败）

step-088=`FAIL 0/2/0`；step-089=`FAIL 0/3/0`；step-090=`FAIL 0/2/1`；step-091=`PASS 0/0/0`。前三次失败均为合同复刻/边界问题，不是科学 D0 失败；不得写成 defect/headroom 负结果。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| 自然 coherent-FSO local slip occurrence 未证 | S1 必须在无注入合法物理 cells 中建立 occurrence | UNKNOWN / NOT_RUN | S1 首批 240 frames，不足时只按合同扩至 600 |
| source-explicit B2 尚未实现 | B2 必须完整复刻声明的 pilot state/16QAM transfer，不得以名字代替 | CONTRACT_FROZEN / CODE_NOT_RUN | D0 implementation + source/static/unit verification |
| D0 工程预算仍是点估计 | 总工期不可超过 7.00d，且不得删 gate 挤预算 | 4.50d D0 + 2.00d post-D0 + 0.50d contingency | 实现前/每批后更新实际工时；必要工作超 7.00d 即 blocker |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|---|---|---|---|
| S1 natural occurrence | event trajectories ≥12，seed clusters ≥4，physical cells ≥2 | D0 YAML S1 | N/A（NOT_RUN） |
| S2 coded damage | macro ACWER delta ≥0.10，lower CI>0，至少2 cells point>0 | D0 YAML S2 | N/A（NOT_RUN） |
| S2 recoverability | recovery ≥0.10，lower CI>0，至少2 cells point>0 | D0 YAML S2 | N/A（NOT_RUN） |
| S2 B2 absorption | lower CI≥0.95=Kill；upper CI<0.90=nonabsorbed；中间区只按预冻结 practical signal | D0 YAML S2 | N/A（NOT_RUN） |
| S3 decoder information | fused top1≥0.25 且 lower CI>0.10；MRR increment≥0.10 且 lower CI>0 | D0 YAML S3 | N/A（NOT_RUN） |
| S4 diagnostic | identity、truth isolation、candidate isolation、finite deterministic scores、cost 全过 | D0 YAML S4 | N/A（NOT_RUN） |

## 下一轮

先按“必读”恢复约束，再按 TDD 写 D0 implementation plan/任务 brief。只实现 B0/B1/B2/O1 与 S1–S4 diagnostic harness、raw rows、bootstrap/aggregate/receipts，先跑 deterministic/unit tests，再把 D0 执行拆成每个子 agent ≤15 分钟的有界批次。

---
## 接收方验证（续接对话时必须完成）
- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称（列出验证了哪些）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反“明确不含”
