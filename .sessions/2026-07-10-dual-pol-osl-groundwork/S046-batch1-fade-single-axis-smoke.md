# [S046] Batch 1 Fade 单轴族首个短序列 smoke

> 2026-07-16 | Batch 1 执行 | PASS（smoke only）

## 目标

在 Batch 0.5 PASS 后，按 S041 的最低成本顺序验证 Fade 单轴族的三条单机制是否能进入统一 runner：standard-CMA baseline、fade-freeze、gradient-clip/trust-region。只验证实现、事件和 schema，不做性能 Go/Kill。

## 记录

新增 `batch1_fade_methods.py`，三变体共享同一含 Godard `z` 的 2×2 CMA 核心，每次只改变一个更新规则：

- `baseline`：与 prompt013 `run_cma_diagnostic(mode="standard")` 同输入逐数组 allclose；
- `fade_freeze`：`h_block < threshold_h` 时仅跳过更新；
- `gradient_clip`：联合四矩阵更新范数超过显式阈值时裁剪。

TDD 先 RED（模块不存在），后 GREEN。2×512-symbol smoke（seed 41/42）在统一 canonical realization、window grid、events、save_results 和共同 `valid_mask` 下完成。每个 seed 有效样本 480；threshold_h=2.0 的机制触发烟测中，baseline freeze/clip 计数为 0，freeze=15 blocks、clip=15 blocks；这是“机制确实触发”的工程性检查，不是性能结果。修正 FIR 首尾零填污染后，seed41 fixed/PI 从 0.0336914 修正为 0.0015625，seed42 从 0.0317383 修正为 0；该差异证明 valid-mask 门控不可省。

统一 runner 现在拒绝方法间不一致的 `valid_mask`，零有效窗口标记 excluded；metadata 含 `valid_samples`、runner source SHA 和 method source SHA。定向回归：`102 passed in 13.30s`；独立复核确认 smoke PASS。

## 决策引用

- D045：候选族先地图，再批量排跑。
- 无新决策；未对任何方法作性能 Go/Kill。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

下一轮先把 threshold_h、clip_norm 等真实参数按 pilot 分布和 S041 预注册合同冻结，再做少量 paired seed 性能批；不得把本次 threshold_h=2.0 触发烟测当成真实 Fade 结论。
