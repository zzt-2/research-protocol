# P07 入口选择（NOT RUN — 本轮仅准备，不执行）

> 2026-07-31 | campaign 6/10 已完成（P06），P07 入口准备 | 状态: ENTRY-PREP-NOT-RUN
> 来源: D044/V070/CP035（P06 NO_CAUSAL_HISTORY_INCREMENT，E 族首包即关闭，第 5 族"≥5 族"达成）+ D039 campaign §4

## 背景（campaign 状态）

- accepted_valid=6/10；families_started = [A, B, C, D, E]（**5 族，"≥5 族"已达成**）；A/E 已关闭，B/C/D 连续=1。
- P01-P06 verdict 全 honest negative（NO_SIGNAL / RESOLVED_REGION / RESOLVED_UNIFORM / ABSENT / RESOLVED_BY_CONVENTIONAL / NO_CAUSAL_HISTORY_INCREMENT）：0 method signal。
- **P07 约束**：E 已关闭（禁第二个 evaluator-repair 包）、A 已关闭（达同族上限）；P07 可选 F/G/... 新族 或 B/C/D 第 2 包（连续≤2 允许）。禁重开所有 forbidden axis。

## P07 候选方向（下一对话 binding decision 确认，本轮不冻结）

> 不冻结具体入口——留给下一对话 binding decision。以下仅为机制空间扫描备注，非冻结设计。

已覆盖的 mechanism space：A=SNR 失配鲁棒性、B=定点资源协同、C=分布形状 OOD、D=在线适配、E=因果跨帧历史信息。
尚未触及的机制正交轴（候选）：
- **F. 同步/估计器交互族**（FOE 残差对 CPR 级联、定时偏移对 selector——注意 FOE-residual 子轴已被 T030 撤回关闭，需选不同子轴如 symbol-timing offset 对 selector decision）
- **G. 湍流场景边界族**（饱和/闪烁、上下行差异、多普勒谱形变——注意不可与已关闭轴重叠）
- **H. 调制/编码层族**（HD/SD-FEC 边界、APSK 环比——注意 P04 已撤回 16APSK 环比/湍流标签入口，需选不同子轴）

B/C/D 第 2 包（连续≤2 允许）：需注入新失效条件（FR-23），不可复现旧结果。

## 不运行（本轮纪律）

本轮（P06 端到端 + 治理更新 + 单次 commit）**不运行 P07**。下一对话由用户中转 P07 执行指令（binding decision），届时先过入口四门 preflight，通过后端到端跑 Phase 0→A→B→C。
