# [S055] Batch2 高速 SOP 盲失效检测侦察

> 2026-07-16 | Batch2 事件侦察 | 状态：FAIL（按退出条件截断）

## 目标

在 `sop_rate=1e-5` failure 域测试不泄漏 transmitted symbols 的逐 block 盲信号，判断是否有足够提前量进入 relock/recovery。

## 记录

结果文件：`projects/simulation/results/cma-fade-divergence/batch2_blind_detector_scout_sop4e-6-vs1e-5_seeds41-43_prefix_stable_v2.json`。新增 trace 仅含 `cm_error`、`output_power`、`update_norm`、`output_start`；BER 只作为 post-hoc oracle。

- `1e-5` seed41/43 有 oracle failure，first persistent blocks=1254/1286；seed42无事件。
- 阈值由 `4e-6` 控制组 pooled P99、连续2块触发。
- 三种盲信号对两个 oracle 事件提前召回均为 0/2，lead 均 null；每种信号在控制组 1/3 seed 误报。
- TDD 定向测试 3 passed；结果含 config/source SHA。

## 决策引用

- D047：高速 SOP failure 域最小事件侦察。
- D048：基础盲统计量无提前信息，停止该 detector 支线（待 V015 审计后登记）。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

不进入 recovery 性能跑；转 H 接受/分段恢复或更强状态跟踪候选，重新做候选级机制假设和最小验证。
