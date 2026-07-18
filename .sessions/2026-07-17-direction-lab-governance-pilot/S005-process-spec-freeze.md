# [S005] Direction Lab 三层流程固化

> 2026-07-18 | 流程固化 | 已完成

## 目标

把 B001–B003 治理 pilot 中已经验证的控制边界，整理为项目级、可执行、未来可 skill 化的流程规范；降低后续每个机制批次的重复治理成本，同时保留脚本硬门和证据链。

## 记录

B003 的 EvidenceGate、33/33 source closure、lean ledger 和独立 verifier 均通过，但 B003 与 B002 的 U24 exact contract 指标重合。因此 B003 主要是治理复核，不是新的方法族研究证据。

现将流程分为三层：

- Scout：机制族全景、覆盖审计、实现盘点和 BatchPlan，不跑正式仿真；
- Sandbox Batch：共享 baseline/seed/指标合同下的成批验证；
- Promotion/Deep Evidence：只为稳定 winner 调用重型 GW/Contract 与正式材料门控。

新增项目级流程拥有者：`projects/thesis-fso/direction-lab/process.md`。README 和 implementation-plan 只保留入口与里程碑摘要。另记录 canonical-state 不能通过事后修改运行快照解决，后续须使用 completion event + state reducer。

## 决策引用

- D007：将 Direction Lab 固化为三层机制族批量流程（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是；未运行实验、未修改 baseline、未写正式材料。

## 后续

- 先完成 B003 state reconciliation；
- 对 v2 Universe 做机制级覆盖审计；
- 一次生成 3–5 个后续机制族 BatchPlan，再选择前置条件齐全且能产生新信息的批次运行。
