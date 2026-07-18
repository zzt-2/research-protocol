# [S060] E/H 候选接口盘点

> 2026-07-16 | 候选切换准备 | 状态：PASS（接口盘点，未跑实验）

## 目标

Stokes pilot 退出后，盘点 E pilot-assisted 与 H 接受式方案的真实可实现接口，避免直接跳到不可因果的 recovery。

## 记录

E 族：`generate_shared_realization_dp()` 已有 `rX/rY/sX/sY/h/theta/bits`；`MLChannelEqualizer.train` 是整段监督接口，不是在线 pilot；旧 `insert_pilots/run_kf_pilot` 只适配单偏振 schema。需要新增 dual pilot 注入器、data mask、2×2 assignment/phase/SOP estimator。最小候选：每 64-symbol CMA block 前 4 个已知 QPSK pilot，开销 6.25%，与无 pilot standard-CMA 同 realization 对照。

H 族：现有 fade/recovery evaluator 依赖 `h` 或 post-hoc BER，属于 oracle；Stokes/eigen 在新 seed 上不稳定，不能直接做盲接受方案。因此 H 暂作为 oracle 标注，不进入长 recovery。

## 决策引用

- D051：优先 E pilot-assisted SOP/Jones 估计。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

先按 TDD 实现 dual pilot 注入/估计最小 seam，跑短 pilot；pilot overhead>10%、无 fixed-label/recovery 改善或依赖 post-hoc truth 即停止。
