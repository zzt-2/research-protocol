# [S078] Direction Lab Portfolio Autopilot 设计

> 2026-07-19 | 流程设计 | 独立审查 PASS，待实现计划

## 目标

解释为什么 Direction Lab 经常在单个局部结果后停下来，并设计一个能在不牺牲证据边界的前提下连续推进多个批次、多个机制族的最小控制面。

## 记录

现状审计确认：CandidateMap、BatchPlan、EvidenceGate、claim-scope 五级门和 Sandbox canonical reducer 已分别覆盖候选输入、批次计划、运行真实性、推理范围和完成态投影；缺口是组合级调度。现有 handoff 把 `LOCAL_NEGATIVE`、`INFRASTRUCTURE_BLOCKED`、critic FAIL 或局部正信号当成需要用户三选一的终点，导致工作在单候选尺度反复停机。

方案比较：

1. 只增强提示词：改动小但不能抵抗上下文压缩和同一 AI 自审偏差，否决。
2. 最小 Portfolio Autopilot：独立维护 campaign 合同、append-only events、可重建 state 和批次薄摘要，复用全部现有执行/证据 owner，采用。
3. 通用 DAG/插件/签名 registry：稳定但当前过度设计，延后。

目标设计见 `docs/superpowers/specs/2026-07-19-direction-lab-portfolio-autopilot-design.md`。首轮 shadow 冻结为至少 6 个有效批次、至少 3 个证据型机制族；首次覆盖前同族最多 2 批，每 2 批自动重排。启动前另需 portfolio-scope receipt 和预算充分性证明，防止先冻结偏窄候选池或预注册过小预算后“稳定跑偏/合法早停”。存在 runnable 候选时，单批失败、局部阻断、critic 退回和正信号都必须自动换路，不能请求用户方向拍板。

控制面只拥有组合预算、轮换与全局停机权。具体 runner、P03 Atlas token、EvidenceGate、claim-scope validator、Sandbox completion reducer 和 formal master-state 均保持原 owner。新增 science critic 与 evidence verifier 分离：复算正确不能替代统计口径、baseline/oracle 合法性、代表域和历史反例审查。

设计明确拒绝逐 cell event、raw result 复制、通用 runner 基类、自动文献全流程和 campaign/canonical 合并。每批只增加一个薄摘要；session 只记里程碑，避免文件体系继续按微步骤膨胀。有效批次使用 `scientific_question_id + artifact/assessment hash` 去重，capability-only 工作不计 6 批或 3 族，防止拆小批次刷数。

迭代计数器：设计方案第 1 轮；未进入实现或实验。

否决条件：若独立审查发现该最小层仍复制现有 owner、无法机器判定全局停机、或 6批/3族约束可以通过拆小批次刷数，则设计不得进入实现计划，必须先修订。

## 决策引用

- D060：采用最小 Portfolio Autopilot 作为 Direction Lab 长跑控制面（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是。它扩展 D045 的候选族批量排跑控制方式，不扩大 formal GW/Contract/Execute 或科学实验范围。

## 后续

独立 reviewer 首轮给出 PARTIAL，发现偏窄 CandidateMap、过小预算早停、批次拆分刷数和生产 6批/3族提前结束等 P0/P1；修订后第二轮 PASS，无残余 P0/P1。用户审阅设计后，再单独使用 writing-plans 产出实现计划；本轮不实现 `campaignctl`，不启动 shadow campaign。
