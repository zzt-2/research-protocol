# [S049] Prefix-stable generator small batch重跑

> 2026-07-16 | Batch 1 复核执行 | PASS（观察记录 only）

## 目标

用 D046 修复后的 GG generator 重跑 S047 同配置 small batch，清除旧 RNG 长度依赖对数值观察的污染。

## 记录

N=100000、seeds41–45、strong α=4.2/β=1.4、fG=30、SOP=4e-7；四臂 baseline/fade-freeze/clip-P99/clip-P95，共享 canonical realization 和 valid mask。顶层 config SHA=`b0ed363a…`，7 个 source SHA 全部逐文件一致，`observation_only_no_go_kill=true`。

独立审计：5 seeds、每 seed 4 臂、valid_samples=99968、window_grid=1563、全 JSON finite；freeze 全 0、diverged 全 false、fade 全 0；clip 仅 seed42 触发（P99=106 blocks，P95=858 blocks），其余为 0。由于当前域阈值 0.1 未产生 fade，freeze 仍无事件覆盖；本批不作性能结论。

## 决策引用

- D046：修复 GG 长度依赖，旧数值作废。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

freeze 需换能产生真实 `h<0.1` 的条件或单独阈值事件 smoke；clip 可进入下一轮正式 paired 性能候选，但需先写 Go/Kill 判据。
