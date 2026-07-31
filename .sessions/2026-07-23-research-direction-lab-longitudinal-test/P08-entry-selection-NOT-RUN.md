# P08 入口选择（NOT RUN — 本轮仅准备，不执行）

> 2026-07-31 | campaign 7/10 已完成（P07），P08 入口准备 | 状态: ENTRY-PREP-NOT-RUN
> 来源: D045/V071/CP036（P07 NO_DIAGNOSTIC_METHOD_SIGNAL，F 族首包未关闭）+ D039 campaign §4

## 背景（campaign 状态）

- accepted_valid=7/10；families_started = [A, B, C, D, E, F]（**6 族**，"≥5 族"已达成）；A/E 已关闭，B/C/D/F 连续=1。
- P01-P07 verdict 全 honest negative（NO_SIGNAL / RESOLVED_REGION / RESOLVED_UNIFORM / ABSENT / RESOLVED_BY_CONVENTIONAL / NO_CAUSAL_HISTORY_INCREMENT / NO_DIAGNOSTIC_METHOD_SIGNAL）：0 method signal。
- **P07 是迄今机制最完整的负面**：问题真实成立（Phase A +0.9-1.0 dB）→ 常规 AGC 部分缓解未解决（Phase B +0.77-0.90 dB）→ 方法候选无增量（Phase C 4 候选无一稳定超 causal-RMS）。
- **P08 约束**：A/E 已关闭；P08 可选 G/... 新族 或 B/C/D/F 第 2 包（连续≤2 允许）。禁重开所有 forbidden axis；P07 的 F/G/H（timing-offset/scenario/FEC-APSK）子轴已撤回不得换名重开。

## P08 候选方向（下一对话 binding decision 确认，本轮不冻结）

> 不冻结具体入口——留给下一对话 binding decision。以下仅为机制空间扫描备注，非冻结设计。

已覆盖的 mechanism space：A=SNR 失配鲁棒性、B=定点资源协同、C=分布形状 OOD、D=在线适配、E=因果跨帧历史信息、F=AGC/ADC 动态范围。
尚未触及的机制正交轴（候选）：
- **G. 检测/判决反馈层族**（hard-decision confidence、slicer-error 监控、cycle-slip 早期预警——注意 U10 cycle-slip early warning 在 candidate-universe，但须选不同子轴避免重入已关闭检测线 D051）
- **H. 信道估计器鲁棒性族**（pilot 密度失配、KF 状态噪声模型漂移——注意须区别于已撤回的 FOE-residual 轴）
- **I. 时变 SOP 跟踪族**（fast SOP 下的 CMA 收敛/跟踪误差——注意须区别于已关闭 Pilot-Jones / 已撤回 P05-D）

B/C/D/F 第 2 包（连续≤2 允许）：需注入新失效条件（FR-23），不可复现旧结果。例如 F 族第 2 包可换 ADC 子轴（如 non-uniform ADC、adaptive-bit-allocation），但**不得换名重开 P07 的 timing-offset/scenario/FEC 子轴**。

## 不运行（本轮纪律）

本轮（P07 端到端 + 治理更新 + 单次 commit）**不运行 P08**。下一对话由用户中转 P08 执行指令（binding decision），届时先过入口四门 preflight（problem-bearing testbed / 机制族正交 / comparator 合法 / 物理自由度可作用），通过后端到端跑 Phase 0→A→B→C。
